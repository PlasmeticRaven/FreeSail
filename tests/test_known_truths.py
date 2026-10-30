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

import json
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


def close_hauled_on_starboard(ship, knots_=15.0, speed_kn=4.0, heading=292.5):
    return under_plain_sail(ship, heading, knots_, speed_kn, ticks=600)


def until(world, kinds, limit: int) -> tuple[list, int]:
    start = world.clock.tick
    for _ in range(limit):
        world.tick()
        done = [e for e in world.log if e.kind in kinds and e.tick > start]
        if done:
            return done, world.clock.tick - start
    return [], limit


def test_truth_10_the_frigate_tacks_in_five_to_ten_minutes_and_gains_to_windward():
    """Luce's "five to ten" minutes. Whether a tack gains or loses ground is a knife's edge
    in the model, decided by the way she carries out of stays: as she gathers way on the
    new tack she gripes up with too little way for her helm (spec M5 §33 item 26), and at
    five knots in she may come to, go astern and lose what she gained. Before package
    37p, from 290, 292.5 and 295 degrees: in at 5.8, 5.4 and 5.0 knots, 298, 328 and 464 s,
    93, 62 and -41 m to windward; since (the period's trim, the upper yards braced in),
    5.45, 5.0 and 4.5 knots, 339, 445 and 363 s, 51, -37 and 27 m. So each is tacked
    within the band, and the three together gain."""
    gained = {}
    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(FRIGATE, heading=heading)
        assert knots(world) > 4.0
        y_before = world.ship.dyn.y
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        assert 285 <= seconds <= 600, f"tacked in {seconds} s from {heading}"
        assert world.ship.dyn.tack == "larboard"
        gained[heading] = world.ship.dyn.y - y_before  # the wind is from north: windward
    assert sum(gained.values()) > 0.0, gained
    assert sum(1 for g in gained.values() if g > 0.0) >= 2, gained


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
    # The band was under 1.5 knots, 45 to 60 degrees off; package 32e re-pinned it to
    # under 1.6 and 45 to 65: with the head sheets hauled flat aft (the sheet holds the
    # trim; Luce 1866, ch. XXVI) the stalled jibs hold her head off at five and a half
    # points, forereaching a knot and a half. Trimmed for the wind instead, they luff as
    # she comes up and she comes head to wind (docs/dev/TuningNotes.md, package 32e).
    world = hove_to()
    run(world, 300)
    assert knots(world) < 1.6, "not stopped within five minutes"
    offs, speeds = [], []
    for _ in range(600):
        world.tick()
        offs.append(off_wind(world))
        speeds.append(knots(world))
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.0 for o in offs), f"lay {min(offs):.0f} to {max(offs):.0f} deg off"
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


def gaff_thrust_on_a_run(angle_deg: float) -> float:
    """The schooner's mainsail on a run with its sheet worked to `angle_deg` (package 32e:
    the sheet holds the trim, and the angle is read from the sheet's length)."""
    from freesail.evolutions import trim

    world = make(SCHOONER, 180.0)
    settle(world, ["set plain sail", "brace the yards square"])
    sail = world.ship.sails["main.sail"]
    assert math.degrees(sail.sheet_angle) == pytest.approx(85.0)  # squared right off
    geo = trim.sheet_geometry(world.ship, sail)
    fathoms = (
        geo.sheet_length(math.radians(angle_deg)) - geo.sheet_length(geo.ceiling)
    ) / trim.FATHOM_M
    world.submit(f"haul the main sheet {abs(fathoms):.0f} fathoms")
    world.tick()
    assert math.degrees(sail.sheet_angle) == pytest.approx(angle_deg, abs=3.0)
    return sail.thrust_kn


def test_truth_13_a_gaff_sail_wants_squaring_off_before_the_wind():
    at_45 = gaff_thrust_on_a_run(45.0)
    at_70 = gaff_thrust_on_a_run(70.0)
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
    # Luce's five to ten minutes (465 s since package 37p's trim, 300 to 420 before)
    assert 300 <= seconds <= 600, f"tacked in {seconds} s"
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
    and the three topsails are manned together, each up to its party of forty (package
    31b, decision 28), the first two from the deck and the third short, with what is
    left, filling as the watch below comes up and the topgallant men come down; the
    topgallants come in while the reefs are being taken, not after them. Nothing is
    belayed, and the hands are piped down once, when the last topsail is reefed."""
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
    party = hands.CrewRequest.from_mapping(runner_evolution_crew("reef_square")).party
    # per topsail: (tick, hands at it, wanted, factor) while its reef runs
    factors: dict[str, list[tuple[int, int, int, float]]] = {}
    for _ in range(1800):
        world.tick()
        for reef in runner.instances:
            if reef.evo.id == "reef_square" and not reef.waiting:
                a = reef.assignment
                factors.setdefault(reef.subject_id, []).append(
                    (world.clock.tick, a.got, a.wanted, hands.crew_factor(a, reef.want, True))
                )
        if not runner.instances and factors:
            break
    fired = by_order(world, "shorten sail for weather")
    assert [text.split(": ")[1] for _, text in fired] == [
        "taking in the topgallants.",
        "reefing the topsails, one reef.",
    ]
    fore, mizzen = factors["fore.topsail"], factors["mizzen.topsail"]
    began = min(f[0][0] for f in factors.values())
    taken_in = [e.tick for e in events(world, "sail.taken_in", after=start)]
    reefed = [e.tick for e in events(world, "sail.reefed", after=start)]
    assert len(taken_in) == 3 and len(reefed) == 3
    # the topgallants in while the topsails are being reefed, not after them
    assert began <= min(taken_in) and max(taken_in) < min(reefed)
    assert events(world, "evolution.belayed", after=start) == []
    # the fore topsail has its party from the first tick and goes at the file's pace; the
    # mizzen, the last to get hands, begins short (part of the deck at the topgallants)
    # and speeds up as the watch below comes up and the topgallant men come down, to the
    # party's pace; no reef ever has more than its party
    assert fore[0][1] == fore[0][2] == party and fore[0][3] == pytest.approx(1.0, abs=0.02)
    _, got0, wanted0, first = mizzen[0]
    assert got0 < wanted0 == party and first > 1.1
    shorts = [e for e in events(world, "evolution.short_handed", after=start)]
    assert any("mizzen topsail" in e.text and "topgallant" in e.text for e in shorts)
    assert [f for _, _, _, f in mizzen] == sorted((f for _, _, _, f in mizzen), reverse=True)
    joined = next(t for t, got, wanted, _ in mizzen if got == wanted)
    assert mizzen[0][0] < joined < min(reefed)  # filled as the watch below came up
    assert mizzen[-1][3] == pytest.approx(1.0, abs=0.02)
    assert max(got for f in factors.values() for _, got, _, _ in f) == party
    # the three reefed together; one call and one pipe-down for the three topsails
    assert max(reefed) - min(reefed) < 60
    assert len(events(world, "crew.all_hands", after=start)) == 1
    piped = events(world, "crew.piped_down", after=start)
    assert [e.tick for e in piped] == [max(reefed)]


def runner_evolution_crew(evolution_id: str) -> dict:
    from freesail.evolutions import registry

    return registry.get(evolution_id).crew


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
    # the sheets tended every minute while she gathers way (package 32e: the sheet holds
    # the trim, and head sheets eased for the wind of two minutes ago luff as the
    # apparent wind draws ahead; left so with the spanker coming on her, she griped up
    # into the wind at a knot and a half and had not the way to stay)
    run(world, 780, trim_every=60)
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
    may be bent worn, at `royal_condition` (truth 27). Package 57: the royals are set
    flying from the deck (Steel 1794 vol. I p. 214) and are up in under ten minutes where
    laid aloft and loosed they were not, so "in time" is the fifth minute, while their
    yards are being swayed up, not the tenth (the topgallant masts were sent down at the
    tenth minute before package 57)."""
    world = from_rest(FRIGATE, heading_deg=270.0, knots_=35.0)
    if royal_condition is not None:
        for sid in world.ship.groups["royals"]:
            world.ship.sails[sid].condition = royal_condition
    world.submit("make all sail")
    world.submit("brace up on the starboard tack")
    run(world, 300)
    if send_down:
        world.submit("send down the topgallant masts")
    run(world, 300)
    world.submit("make all sail")
    world.submit("trim sails")
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
    canvas from the sail room (spec 3b §6.4). In 45 knots at seed 7 nothing carries away,
    blows out or parts in the hour. Since package 37p (the keel's grip astern,
    `hull.sternway_yaw`) she does not lie steady head to sea going astern: she comes up and
    falls off, "in a gale, with a heavy sea, vessels lying to will come up and fall off four
    or five points" (Luce 1884, ch. XXIV), measured 33 to 87 deg off the wind (before, 45
    to 46, steady), and drifts at 1.6 knots on the hour's mean (before, 4.4 astern); at
    the most 2.6, which is the xfail below."""
    world, hour = frigate_lying_a_try
    set_ = {s.id for s in world.ship.sails.values() if s.is_set}
    assert set_ == {"main.topsail", "fore.storm_staysail", "mizzen.storm_staysail"}
    topsail = world.ship.sails["main.topsail"]
    assert topsail.reefs == topsail.reef_bands
    lying = events(world, "ship.hove_to")
    assert lying and lying[-1].text.startswith("Lying a-try under the main topsail")
    assert [e.text for e in world.log if e.kind in (*CARRIED_AWAY, "line.parted")] == []
    assert 30.0 <= min(hour["off"]) and max(hour["off"]) <= 95.0
    assert sum(hour["speed"]) / len(hour["speed"]) < 2.0


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Owner's ruling (spec 3b §9, truth 28). Lying a-try in 45 knots under the close-"
        "reefed main topsail and the storm staysails, the topgallant masts down and the fore "
        "and mizzen topsails furled, she went astern at 4.4 to 5.1 kn 45 deg off the wind; "
        "since package 37p the keel's grip astern lets her fall off into the trough "
        "(hull.sternway_yaw) and she drifts at 1.6 kn on the hour's mean, 2.6 at the most, "
        "coming up and falling off between 33 and 87 deg. The hull's resistance astern is "
        "still its resistance ahead (physics/hull.py). See docs/dev/TuningNotes.md."
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
    main mast's strain ratio rises from 0.147 to 0.225 (x1.53; package 37p: the period's
    trim braces the upper yards in from the lower, and each comes the four degrees sharper
    with the main yard; before it, 0.178 to 0.229, x1.29): its rating is taken at 0.883
    (CATHARPIN_RATING_FACTOR 0.85 on the athwartships part of the pull) and the sharper
    yards pull harder. A lower mast is rated for 55 knots, so at 0.23 no warning line
    comes, and none is pretended."""
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
    assert 1.0 / 0.9 <= rise <= 1.6, f"strain ratio {before_ratio:.3f} to {mast.strain_ratio:.3f}"
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
    # second, before the routine can fire (docs/dev/TuningNotes.md, milestone 4a); since
    # package 57 (Steel's staysails in all sail) the main topmast boom goes first, where the
    # fore topgallant boom went before
    lost = events(world, "spar.carried_away")
    assert lost and lost[0].subject == "main.topmast.studdingsail_boom.larboard"
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
    # every topsail still set is close-reefed; the mizzen topsail blew out at 45 knots
    # while the hands were still aloft sending down the masts (package 32e: with her
    # spanker's sheet standing as trimmed she holds her course and eleven knots as the
    # gale tops out, her whole topsails loaded half again over their rating; before, the
    # free tending flattened the spanker as the jibs blew out, she griped up and lay
    # shaking at forty degrees off with her topsails unloaded)
    topsails = [world.ship.sails[t] for t in world.ship.groups["topsails"]]
    assert all(s.reefs == 3 for s in topsails if s.is_set)
    assert [s.id for s in topsails if not s.is_set] == ["mizzen.topsail"]
    assert any("Mizzen topsail split and blew out" in e.text for e in world.log)


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
# third), and "trim on a shift" four times (20:42, 21:58, 22:57, 23:55) as the wind veers.
# Package 31b (the pinned form under the air-mass rule, the owner's ruling at gate 5a;
# the topsails reefed by three parties together): the ticks above and the shortening
# ticks did not move, since the pinned wind's speed fires the routines and neutral air's
# gusts, 1.30 of the mean at most, never reach a dwell; "trim on a shift" fires fourteen
# times, none by day (the scenario says the warm sector's air, three degrees of wander)
# and every twenty to forty minutes through the gale in neutral air, whose wander of five
# degrees about the base carries the point rule over its mark and back
# (docs/dev/TuningNotes.md, M5a, package 31b).
GATE_DAY_SHORTEN_SAIL_TICKS = [63837, 65773, 68188]
# Package 32e (the sheet holds the trim; the sheets tended by the book every glass): the
# ticks above did not move; "trim on a shift" fires twelve times, not fourteen: its last
# two firings (03:22 and 03:29 on 2 June) fell while all hands were making sail after the
# gale, and a trim now begins sheet evolutions that wait for hands, so the order's work had
# not ended and it could not stand again until the wind had settled (docs/dev/TuningNotes.md,
# package 32e).
GATE_DAY_TRIM_ON_A_SHIFT_TICKS = [
    55866,
    56843,
    59062,
    64840,
    66022,
    68980,
    77099,
    78222,
    80789,
    82056,
    82680,
    87053,
    98501,  # two more after package 32e: the sheets held as trimmed through the ease
    98938,  # of the gale, the wind's wander fires the point rule twice in the forenoon
]


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
    # its three orders on the one tick (package 37p; four before it, the fore topmast
    # staysail taken in and the storm staysail bent): the masts down, the storm staysails
    # set (bent from the sail room and set as each is bent, the head sails taken in as the
    # fore one goes up), and the close reef refused in words because the topsails are
    # close-reefed already. Package 29b: with all hands a pool action the reefs are done
    # sooner and the starter's "shorten sail for weather" stands again sooner, so it fires
    # three times in the first watch (21:43, 22:16, 22:56), three reefs in by 23:22, as the
    # first measurement of package 29 had it; package 29 after the topgallants moved into
    # its line had it fire twice and the close reef carried out (docs/dev/TuningNotes.md)
    assert [t for t, _ in heavy] == [GATE_DAY_HEAVY_WEATHER_TICK] * 2
    assert [text.split(": ")[1] for _, text in heavy] == [
        "sending down the topgallant masts.",
        "setting the storm staysails.",
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
    that tick (package 29's `inputs`: refusals and queries replay, not only the orders
    carried out), so the replayed log is the log the player watched, line for line. The
    well's standing order, held in the book from package 33c, has left the starter book
    (2026-10-21), and nothing of it is in the inputs."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, sf, saved = gate_day
    for tick in GATE_DAY_SAVES:
        data, digest = saved[tick]
        assert data["end_tick"] == tick
        assert data["scenario"]["weather"] == sf.scenario.weather
        assert not [x for x in data["inputs"] if "sound the well" in x.get("order", "")]
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
    # the air is the pinned waypoint's (the warm sector's by day, package 31b), whatever
    # the systems' sector says: the deeper low changes nothing of the wind
    said = pinned.weather.air_mass_at(pinned.clock.ship_time)
    assert pinned.wind.air_mass == changed.wind.air_mass == said == "warm"


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


# ---------------------------------------------------------------------------
# Milestone 5a: the sea and the ship's motion (package 31; spec M5 §4, §6, §7)
# ---------------------------------------------------------------------------
#
# The day under systems alone (data/scenarios/gate-5a-day.yaml): the pinned day's systems
# without its `wind`, the surface wind at the ship the base, the gust factor by air mass,
# squalls behind the cold front, and the sea and the motion raised by it; the same
# standing orders. Its ticks and its digest are truth constants of their own, measured at
# seed 7 (docs/dev/TuningNotes.md, M5a: the day under systems); the pinned day's
# constants above do not move.

GATE_5A_DAY = "data/scenarios/gate-5a-day.yaml"
GATE_5A_DAY_TICKS = GATE_DAY_TICKS
GATE_5A_DAY_SAVES = (16 * 3600, 21 * 3600)
# Measured at seed 7 (package 31, and again by package 31b with the topsails reefed by
# three parties of forty together and the close reef first in the starter's heavy-weather
# routine; docs/dev/TuningNotes.md, M5a, package 31b): sunset and the night routine at
# 19:50; the starter's "shorten sail for weather" once, at 21:33 (the systems' wind passes
# thirty a quarter of an hour before the pinned one), its three reefs in together by
# 21:44; the captain's "gale canvas" at 23:11; the heavy-weather routine at 00:37, its
# four orders on one tick, the close reefs in by 00:51 (package 31 had them waiting for
# the send-down's hands until the first squall, and lost the mizzen topsail and the main
# topsail's brace and sheet to it); the first squall of the middle watch at 01:17, 65
# knots, with the topsails close-reefed and the topgallant masts coming down; the storm
# staysail set at 01:26; nothing lost, no spar carried away; "make sail after the gale"
# at 08:13 and the captain's "topgallants again" at 08:52 (before this package it had not
# fired by nine).
GATE_5A_SUNSET_TICK = 57039
GATE_5A_SHORTEN_SAIL_TICK = 63200
GATE_5A_GALE_CANVAS_TICK = 69115
GATE_5A_HEAVY_WEATHER_TICK = 74245
GATE_5A_FIRST_SQUALL_TICK = 76673
GATE_5A_CLOSE_REEFS_IN_TICK = 75099  # package 57 (75103 before)
GATE_5A_MAKE_SAIL_TICK = 101624
GATE_5A_TOPGALLANTS_AGAIN_TICK = 103978  # 103976 before package 37p
GATE_5A_LOST: list[str] = []
# The sea's words through the day: a short chopping sea from 05:04, a heavy sea from
# 20:45 as the gale comes on, a very heavy sea from 01:51, and going down to a heavy sea
# at 08:26, hours after the wind eased (the ten-minute mean under a moderate gale from
# about five).
GATE_5A_SEA_TICKS = {
    "A short chopping sea getting up.": 3840,
    "A heavy sea getting up.": 60300,
    "A very heavy sea getting up.": 78660,
    "A heavy sea, the sea going down.": 102360,
}
# Package 32e (the sheet holds the trim): every tick of the day's routines held; the
# lines are the starter book's "tend the sheets" firing every glass (fifty-seven times, the
# sheets found standing as trimmed most glasses) and the sheet evolutions the trims and
# the manoeuvres start, and the digest moved with them (docs/dev/TuningNotes.md, 32e).
# Package 33c: every tick held; one line more, the starter's "sound the well" entered in
# the book and held (an accepted order's line and the book's) where it was refused (one).
# Package 37f: every tick held and her true track the same to the last figure; the four
# lines that enter the starter's "trim on a shift" and "tend the sheets" carry their new
# guard (`and the manoeuvre in hand is not hove to`), and the digest moved with them.
# Package 37p: the heavy-weather routine's three orders (the storm staysails set by one,
# the fore topmast staysail taken in at once as loaded near its rating, the gale over the
# storm line); the topgallants again two seconds later; nothing lost.
# the well's order gone from the starter book, and its two held lines with it (2026-10-21)
GATE_5A_DAY_LINES = 623  # 625 at package 57 (620 at 45c, 621 at 45, 616 before 37p)
GATE_5A_DAY_DIGEST = "1680cb1391720dd8"  # bff57a00218b7ec5 at 57 (a235022bc8bf8bc7 at 45c)


def the_gate_day_under_systems(until: int = GATE_5A_DAY_TICKS, saves=GATE_5A_DAY_SAVES):
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(GATE_5A_DAY)
    world = make_scenario_world(sf)
    begin(world, sf)
    saved = {}
    for t in sorted(saves):
        run(world, t - world.clock.tick)
        saved[t] = (world.save(), world.log.digest())
    run(world, until - world.clock.tick)
    return world, sf, saved


@pytest.fixture(scope="module")
def gate_5a_day():
    return the_gate_day_under_systems()


def test_truth_56_a_gale_of_a_day_raises_a_heavy_sea_the_reef_is_slower_in_and_that_outlasts_it(
    gate_5a_day,
):
    """Spec M5 §6, truth 56: "A gale of a day raises a heavy sea that the frigate's reefing
    takes half as long again in as in a smooth one, and the sea outlasts the wind by hours
    in the log's words." The sea of a day's gale of forty knots (`world.sea.Sea`) is a
    heavy sea in words; the frigate on a beam reach reefs her fore topsail in it, on her
    beam, in 1.4 to 1.7 times the ticks she takes with no sea kept (a smooth sea is the
    same to the tick, tests/test_sea.py); and on the day under systems the sea is a heavy
    sea from the evening to the second forenoon, still heavy at nine with the wind a
    fresh breeze since seven."""
    from tests.test_sea import frigate_under_plain_sail, heavy_sea_aboard, reef_ticks, sea_of

    gale = sea_of(24.0, 40.0)
    assert gale.state in ("heavy", "very heavy") and gale.words.endswith("heavy sea")
    quick = reef_ticks(frigate_under_plain_sail(sea=False))
    heavy = heavy_sea_aboard(frigate_under_plain_sail(sea=True), knots=40.0)
    assert heavy.sea.words == gale.words
    slow = reef_ticks(heavy)
    assert 1.4 <= slow / quick <= 1.7, (quick, slow)
    # the sea outlasts the wind: on the day under systems
    world, _, _ = gate_5a_day
    seas = {e.text: e.tick for e in events(world, "sea.change")}
    assert seas == GATE_5A_SEA_TICKS
    hours = events(world, "weather.hour")
    at = {e.ship_time: e for e in hours}
    nine = at[datetime(1805, 6, 2, 9, 0)]
    assert nine.data["sea"] == "a heavy sea" and "a heavy sea" in nine.text
    # the gale was over by half past five (the last gust on a mean of a fresh gale or more,
    # the gust lines carrying the ten-minute mean), the sea very heavy until 08:22 and
    # heavy at nine with the mean wind a fresh breeze: it outlasts the gale by hours
    means = {e.ship_time: e for e in world.log if e.kind == "wind.gust" and e.ship_time.day == 2}
    last_gale = max(t for t, e in means.items() if e.data["mean_kn"] >= 34.0)
    assert datetime(1805, 6, 2, 3, 0) < last_gale < datetime(1805, 6, 2, 5, 30)
    going_down = GATE_5A_SEA_TICKS["A heavy sea, the sea going down."]
    assert world.clock.start + timedelta(seconds=going_down) - last_gale >= timedelta(hours=3)
    assert max(t for text, t in seas.items() if "heavy" in text) == going_down
    assert world.readings["sea"]["state"] == "heavy"
    assert units.ms_to_knots(world.wind_record.mean_speed()) < 22.0


def test_the_day_under_systems_alone_at_seed_7_has_its_own_constants(gate_5a_day):
    """The day under systems alone (gate 5a's day; spec M5 §7): the same standing orders
    as the pinned day, the systems' wind at the ship, the sea and the motion kept. Its
    ticks, what it loses in the squalls of the gale, its lines and its digest are the
    constants above, measured at seed 7; the pinned day's (truths 48 to 51) do not move."""
    world, sf, _ = gate_5a_day
    assert world.seed == 7 and sf.scenario.weather == [] and sf.scenario.systems
    assert world.sea is not None and world.motion is not None and world.weather is None
    assert world.wind.air_mass is not None
    assert [e.tick for e in events(world, "sun.set")] == [GATE_5A_SUNSET_TICK]
    assert by_order(world, "night routine") == [
        (GATE_5A_SUNSET_TICK, "By standing order 'night routine': taking in the royals.")
    ]
    assert sorted({t for t, _ in by_order(world, "shorten sail for weather")}) == [
        GATE_5A_SHORTEN_SAIL_TICK
    ]
    assert sorted({t for t, _ in by_order(world, "gale canvas")}) == [GATE_5A_GALE_CANVAS_TICK]
    heavy = by_order(world, "heavy weather")
    assert [t for t, _ in heavy] == [GATE_5A_HEAVY_WEATHER_TICK] * 3
    # the close reef first (package 31b, the order of the clauses being the order of
    # the work), and in before the first squall: the three topsails by three parties; the
    # storm staysails set by the one order since package 37p
    assert [text.split(": ")[1] for _, text in heavy] == [
        "close reefing the topsails.",
        "sending down the topgallant masts.",
        "setting the storm staysails.",
    ]
    close = [e for e in events(world, "sail.reefed") if "3 reefs" in e.text]
    assert sorted(e.subject for e in close) == sorted(world.ship.groups["topsails"])
    assert max(e.tick for e in close) == GATE_5A_CLOSE_REEFS_IN_TICK < GATE_5A_FIRST_SQUALL_TICK
    assert max(e.tick for e in close) - min(e.tick for e in close) < 60  # together
    squalls = events(world, "weather.squall")
    assert squalls and squalls[0].tick == GATE_5A_FIRST_SQUALL_TICK
    assert "65 knots" in squalls[0].text and squalls[0].data["air_mass"] == "unstable"
    assert [e.text for e in world.log if e.kind in LOST] == GATE_5A_LOST == []
    assert [p.id for p in world.ship.parts.values() if p.wrecked] == []
    assert min(t for t, _ in by_order(world, "make sail after the gale")) == GATE_5A_MAKE_SAIL_TICK
    again = by_order(world, "topgallants again")
    assert again and again[0][0] == GATE_5A_TOPGALLANTS_AGAIN_TICK
    assert len(world.log) == GATE_5A_DAY_LINES
    assert world.log.digest()[:16] == GATE_5A_DAY_DIGEST
    # the motion's words through the gale, and no line names a number of the sea
    motions = [e.text for e in events(world, "motion.change")]
    assert "Rolling heavily." in motions and "Labouring heavily." in motions
    assert "Pitching heavily, the sea under her stern." in motions
    for e in world.log:
        assert not FORBIDDEN_WORDS.search(e.text), e.text
    for e in events(world, "sea.change") + events(world, "motion.change"):
        assert not any(ch.isdigit() for ch in e.text), e.text


def test_the_day_under_systems_saved_in_the_gale_replays_to_the_same_digest(gate_5a_day):
    """Truth 49's form on the day under systems (spec M5 §7: "the fake watcher's day
    replayed to the same digest"): saved at 20:00 and at 01:00 in the gale, each
    replayed from its seed, scenario and inputs to the digest it had, the sea and the
    motion raised again from the wind (nothing of them is saved)."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, sf, saved = gate_5a_day
    for tick in GATE_5A_DAY_SAVES:
        data, digest = saved[tick]
        assert data["end_tick"] == tick and data["scenario"]["sea"] is None
        assert data["scenario"]["systems"] == sf.scenario.systems
        copy = replay_mod.replay(data, ship_factory)
        assert copy.clock.tick == tick and copy.log.digest() == digest, tick
        assert copy.readings["sea"] is not None and copy.sea.words == copy.readings["sea"]["words"]


def test_the_pace_on_the_day_under_systems_holds_truth_51s_floor():
    """Spec M5 §30: a truth per gate measures the whole at the gate's scenario. Truth 51's
    measure on the day under systems alone (the systems' wind every tick, the sea once a
    minute, the motion every tick, the strain's and the hull's factors): a thousand ticks
    to settle, the best of three thousands, at least BUILD_MACHINE_FLOOR. Measured on the
    build machine: 843 ticks a second (862 on the pinned day the same run;
    docs/dev/TuningNotes.md, M5a)."""
    import time

    world, _, _ = the_gate_day_under_systems(until=1000, saves=())
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"


# ---------------------------------------------------------------------------
# Milestone 5b: the chart, the queries and the lookout (package 32; spec M5 §19)
# ---------------------------------------------------------------------------

CHART_REGION = "channel-west"
# The Bishop and St Agnes light (data/charts/features/channel-west.yaml, from White 1835
# and Trinity House): the light's range in 1805, fifteen miles, from White's "five leagues".
BISHOP_ROCK = (49.8735, -6.4462)
ST_AGNES_RANGE_NM = 15.0
# Where the gate's day is sailed when the region is loaded for the pace truth: off
# Falmouth, in the open water south of the Manacles (the day's fixture keeps no position,
# so that its constants do not move; the pace truth adds one).
OFF_FALMOUTH = {"lat_deg": 49.95, "lon_deg": -5.00}


def test_truth_65_the_bishop_is_dark_and_st_agnes_lit_on_a_night_landfall_from_the_south_west():
    """Spec M5 §19, truth 65: "The Bishop is dark and St Agnes is lit in 1805; a night
    landfall on Scilly from the south-west sees St Agnes at its range and nothing else."
    The frigate stands in toward the Bishop from the south-west at night in clear
    weather: twenty miles off nothing is in sight; within the light's range the lookout
    hails a light, and it is St Agnes (the reading names it; the lookout does not); the
    Bishop, four miles nearer, shows nothing, being a bare rock in 1805 (its light is dated
    1858, and the same landfall in 1860 sees two lights)."""
    from freesail.world.chart import load_chart
    from freesail.world.geo import Position, bearing_and_distance, destination
    from freesail.world.lookout import height_of_eye

    chart = load_chart(CHART_REGION)
    bishop = Position(*BISHOP_ROCK)
    agnes = chart.feature("st-agnes-light")
    assert agnes.lit_in(1805) and not chart.feature("bishop-rock-light").lit_in(1805)
    assert chart.feature("bishop-rock-light").lit_in(1860)
    night = datetime(1805, 6, 1, 23, 30)

    def frigate_at(pos: Position):
        sc = Scenario(
            start_time=night,
            wind_from_deg=225.0,
            wind_speed_kn=10.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=45.0,
            position=pos.to_dict(),
            region=CHART_REGION,
        )
        return make_world(SEED, FRIGATE, sc)

    far = frigate_at(destination(bishop, 225.0, 20 * units.NAUTICAL_MILE))
    assert far.daylight == "night"
    far.run(60)
    assert far.lookout.sightings == [] and not [e for e in far.log if e.kind == "lookout.sighting"]
    # within the light's range from the light itself, and still well short of the Bishop
    near_pos = destination(agnes.position, 225.0, (ST_AGNES_RANGE_NM - 1.0) * units.NAUTICAL_MILE)
    _, off_bishop = bearing_and_distance(near_pos, bishop)
    assert off_bishop > 9 * units.NAUTICAL_MILE
    near = frigate_at(near_pos)
    near.run(60)
    seen = near.lookout.sightings
    assert [s.feature.id for s in seen] == ["st-agnes-light"] and seen[0].seen_as == "light"
    eye = height_of_eye(near.ship)
    assert seen[0].distance_m / units.NAUTICAL_MILE <= ST_AGNES_RANGE_NM
    assert seen[0].distance_m / units.NAUTICAL_MILE <= 2.08 * (
        math.sqrt(eye) + math.sqrt(agnes.height)
    )
    hails = [e for e in near.log if e.kind == "lookout.sighting"]
    assert len(hails) == 1 and hails[0].severity is Severity.NOTABLE
    assert hails[0].text.startswith("A light ") and hails[0].data["id"] == "st-agnes-light"
    assert "Agnes" not in hails[0].text and "Bishop" not in hails[0].text
    reading = near.readings["in_sight"]
    assert reading["count"] == 1 and reading["items"][0]["id"] == "st-agnes-light"
    # the same landfall in 1860 sees the Bishop's light too
    later = chart.in_sight(near_pos, eye, None, "night", datetime(1860, 6, 1, 23, 30))
    assert {s.feature.id for s in later} == {"st-agnes-light", "bishop-rock-light"}


def test_the_pace_on_the_gates_day_with_the_region_loaded_holds_truth_51s_floor():
    """Spec M5 §30 and package 32: the queries per tick with the region loaded (the
    grounding check every tick, short-circuited by the tile's minimum at sea; the lookout
    once a minute; the coast hook for the sea breeze and the fog) on the gate's day under
    systems, given a position off Falmouth: a thousand ticks to settle, the best of three
    thousands, at least BUILD_MACHINE_FLOOR. Measured on the build machine:
    docs/dev/TuningNotes.md, package 32."""
    import time

    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(GATE_5A_DAY)
    sf.scenario.position = dict(OFF_FALMOUTH)
    sf.scenario.latitude_deg = OFF_FALMOUTH["lat_deg"]
    sf.scenario.region = CHART_REGION
    world = make_scenario_world(sf)
    assert world.chart is not None and world.lookout is not None and world.systems.coast is not None
    begin(world, sf)
    run(world, 1000)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"


def test_the_primers_chapter_nine_does_not_narrate_the_gates_day(gate_5a_day):
    """Playtest 11's finding 9 (package 31b): chapter 9 described the gate's day hour by
    hour, and the log's first line names the scenario, so a reader of the library could
    foresee the night. The chapter now names no scenario file and no day of the tests,
    and none of its sample lines carries a moment of the day under systems (its notable
    lines and its standing orders' firings); the hours in it are any day's."""
    primer = Path(__file__).resolve().parents[1] / "docs" / "primer"
    text = (primer / "09-the-glass-and-the-sky.md").read_text(encoding="utf-8")
    for words in ("gate-4c-day", "gate-5a-day", "gate's day", "Falmouth", "ten in the evening"):
        assert words not in text, words
    world, _, _ = gate_5a_day
    # a routine at a cadence ("every glass": the sheets tended, package 32e) fires at the
    # bells, which are any day's moments, not the day's
    cadence = {
        f"standing order '{r.name}'" for r in world.standing.book.rules if r.trigger.kind == "every"
    }
    moments = {
        e.ship_time.strftime("%H:%M")
        for e in world.log
        if e.actor not in cadence
        and (e.severity is not Severity.ROUTINE or e.actor.startswith("standing order"))
    }
    assert len(moments) > 50
    said = set(re.findall(r"\((\d\d:\d\d)\)", text))
    assert said, "the chapter still shows the log's lines"
    assert not (said & moments), sorted(said & moments)


# ---------------------------------------------------------------------------
# Milestone 5b: the reckoning and the passage (package 33a; spec M5 §13, §19, §20)
# ---------------------------------------------------------------------------
#
# The passage for gate 5b (data/scenarios/gate-5b-passage.yaml): Ushant to Falmouth in the
# frigate at seed 7 on the pinned south-westerly, by the reckoning and the noon sight
# alone; the same in the schooner (gate-5b-passage-schooner.yaml) and in thick weather
# (gate-5b-passage-thick.yaml, the sky pinned, the landfall made wrong on purpose). Its
# ticks, its lines and its digests are truth constants measured at seed 7
# (docs/dev/TuningNotes.md, M5b, package 33a). The account against the truth at each
# moment is printed by `py tools/day_log.py <scenario> --reckoning`.

GATE_5B_PASSAGE = "data/scenarios/gate-5b-passage.yaml"
GATE_5B_PASSAGE_SCHOONER = "data/scenarios/gate-5b-passage-schooner.yaml"
GATE_5B_PASSAGE_THICK = "data/scenarios/gate-5b-passage-thick.yaml"
GATE_5B_HOURS = 17  # 04:00 to 21:00: the outer road after eight, brought up before half past
GATE_5B_SCHOONER_HOURS = 17  # the whole passage since package 32e's hove-to refusal held her
GATE_5B_THICK_HOURS = 16
# Measured at seed 7 (package 33a; re-measured by the lead on 2026-09-30 after package
# 32e's yaw and sheets and the passage's amended book): the noon sight at the sun's noon
# (11:59 by the clock, a minute before twelve on the start meridian), the frigate brought
# to and the deep-sea lead's fifty-two fathoms at 12:18, the Lizard raised at 16:28 (the
# Beast and the Lizard lights at four leagues: the landfall), the course shaped for
# Falmouth from the account, the lead going in every ten minutes past the Manacles,
# sixteen fathoms in the outer road at 20:11, where she wears and lies to on the
# starboard tack, forereaching off the land (the anchor is package 34's); the account 4.8
# miles from the truth at noon, 8.1 at the landfall, within a mile in the outer road. The
# thick passage: no sight, the same cast, and the land about Black Head close aboard at
# 19:08 with the account 10.9 miles off (she believed herself off Falmouth), standing off
# to the southward. The schooner: the sight with the octant, the Lizard at 16:15, the
# whole passage to the outer road as the frigate's.
# Re-measured after package 33b (the lookout's distance by estimation drawn once a
# sighting episode from its own stream and taken at the bearing, where each bearing drew
# its own from the reckoning's): the departure's estimate off Ushant moved the account a
# mile, the course shaped from it by the book's "landfall" rule a fraction of a point,
# and the truth's track with it: the Beast at four leagues at 16:30, nineteen fathoms and
# a half in the outer road at 19:41, the account 3.6 miles from the truth at noon and 6.9
# at the landfall; the schooner's Beast at five leagues at 16:17; the thick passage's
# ticks unmoved and its digest moved by the hails' `estimate_m` (docs/dev/TuningNotes.md,
# package 33b, "the pinned passages, re-measured").
# Package 34 (the tide): the stream in the track moves every tick after the departure
# but the noon's (the sun's), and the lead reads the tide; the passages end at the anchor
# (the frigate in the outer road, the schooner off the town) in place of lying to, so
# the ticks, the lines and the digests below are the tide's (docs/dev/TuningNotes.md,
# package 34, "the pinned passages, re-measured with the tide in").
# Package 37d (2026-10-06; the review of gate 5c's playtests, 5.1): a bearing gives a line,
# the lookout's distance by estimation is laid down with it only when the account's doubt
# along the sight is the greater (the second pass; the first laid it down never), and the
# book's bearing rule takes a fix by cross bearings after the bearing (one line of the
# book). The departure off Ushant is a bearing and distance of the light and then a fix
# by cross bearings; the course shaped from it differs by a degree and the truth's track
# with it from the first minute: the cast at its old tick, in fifty-five fathoms for
# fifty-three (29884), the Beast and the Lizard's lights raised at one look at
# 16:22 (44520; 44700), the outer road at 58895 (57732), the anchor at 59250 (58167) and
# brought up at 60239 (59144); the cutter sighted at 55260 (54600), her hail at 57060
# (56280) and the pilot aboard at 57180 (56340). The lines 630 to 662: ten fixes with
# their orders, the shore's own hail, the bearings' words where the distance is laid down
# or the account's differs (docs/dev/TuningNotes.md, package 37d, has the table of
# reasons). The thick passage: every tick held; one line more ("Land ahead" at the
# landfall) and the shore's hail by estimation. The schooner: every tick held (below).
# Package 37e (2026-10-07; the account): one rule for every observation, the master's own
# tide in the traverse, his drift hove to, and a course shaped to make good. Every true
# track parts at the first course shaped (the departure's, at tick 1, which now says "she
# has no way on to work an allowance by" and holds the line's own bearing, a degree from
# 37d's heading; the first with an allowance is the course after the noon's cast). The
# books round the Manacles by a point three miles east of them and shorten sail at the
# pilot's hail (the frigate's), since a course made good from the Lizard's landfall
# "crosses the land about Black Head" (docs/dev/TuningNotes.md, package 37e, has the
# table of reasons). Old beside new: the cast 29884 → 29887 (the same fifty-five
# fathoms, and the line says "The account kept."); the landfall 44520 → 44760, the Beast
# and the Lizard's lights at one look, the account nine miles and a half out before the
# bearing and two and a third after it (the bearing's line laid down, the distance by
# estimation weighed); the outer road 58895 → 57737, the anchor 59250 → 58178 in eleven
# fathoms and a half (twelve before), brought up 60239 → 59151; the cutter sighted
# 55260 → 55440 right ahead, her hail 57060 → 56940, the pilot aboard 57180 → 57060;
# 662 → 718 lines. The thick passage: the land about Black Head close aboard at
# 54900 → 54600, the account six miles out (eleven before: his tide and his drift hove to
# are in it), 503 → 508 lines. The schooner: below.
# Package 37f (2026-10-07; lying to, and the ground): brought to for the noon's cast she
# has her way taken off before "Hove to" is said (28796 → 29013, "Hove to on the larboard
# tack", a knot and a half on her by the log where she had three and three quarters), so
# every true track parts at the heave-to (tick 28750) and the cast is had four minutes
# later (29887 → 30118, the same fifty-five fathoms). The frigate's book gained a line
# and a clause (docs/dev/TuningNotes.md, package 37f, has the table of reasons): the
# course for the point east of the Manacles is worked again every glass on the way to it
# (the course shaped as she filled, with a knot and a half on her, was a point too far
# west for the seven she had ten minutes after, and unmended she passed the point more
# than a mile wide by her account and stood on up the Channel), and sail is shortened at
# the rounding (unmended her sail was not in when the pilot hailed, and he did not
# board). Old beside new: the landfall 44760 → 44820, the Beast and the Lizard's lights
# at one look; the outer road 57737 → 58297; the anchor 58178 → 58647 in fourteen fathoms
# and a half (eleven and a half), brought up 59151 → 59642; the cutter sighted
# 55440 → 55860, her hail 56940 → 57480, the pilot aboard 57060 → 57540; 718 → 768 lines
# (the course worked each glass; the heave-to's per-sail lines gone, the casts that find
# no bottom routine, the held lines once a watch for each reason). The thick passage:
# the land close aboard 54600 → 54420; 508 → 488 lines. The schooner: below.
# Package 37h (2026-10-09; the pilot taken at his hail, docs/dev/TuningNotes.md, its
# section): the pilot boards only when he is taken, and the book's line at his hail is
# `take the pilot` where it was `shorten sail` (the frigate under six knots at the hail is
# asked nothing, and her sail, shortened at the rounding, is not shortened again). Every
# tick to the hail stands (the cutter sighted 55860, her hail 57480, the pilot aboard
# 57540); the outer road 58297 → 58298, the anchor 58647 → 58650 in fifteen fathoms
# (fourteen and a half), brought up 59642 → 59643; 768 → 754 lines (the shortening's
# lines at the hail gone; the answer's and the pilot's own lines). The thick passage, with
# no cutter, is untouched.
# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
# Package 37j (2026-10-09; the account amended, measured on Linux): the departure is laid
# at the scenario's own position where it was drawn a mile out, and the account is worked
# at every board; every tick to the cast stands (the noon, the heave-to and the cast are
# the ship's own), and the true track parts at the first course shaped from the account.
# The noon's sight is now weighed and not taken (the account the better figure there,
# eight cables moved to the NNE where 37e laid it three miles north); the cast says the
# master's tide it took off ("Two fathoms of tide allowed by the epitome: fifty-three
# fathoms on the chart"). Old beside new: the landfall 44820 → 45180, the Beast at four
# leagues; the outer road 58297 → 58298; the anchor 58647 → 58646 in eleven fathoms and a
# half (fourteen and a half); brought up 59642 → 59606; the cutter sighted 55860 → 55500,
# her hail 57480 → 57120, the pilot aboard 57540 → 57180; 768 → 746 lines (the noon's,
# the cast's and the bearings' words; fewer courses for the point worked, fourteen).
# The thick passage: below its test (she takes the ground).
GATE_5B_NOON_TICK = 28740
GATE_5B_CAST_TICK = 30117  # package 57 (30118 before)
GATE_5B_HOVE_TO_TICK = 29012  # "Hove to on the larboard tack", her way off first (29013)
GATE_5B_LANDFALL_TICK = 45180  # 44820 before package 37j
GATE_5B_ROADS_TICK = 58299  # the outer road, the first cast under twenty fathoms (58298 before)
GATE_5B_ANCHORED_TICK = 58651  # the best bower let go (package 57; 58652 before)
GATE_5B_BROUGHT_UP_TICK = 59603  # brought up, the sails furled (package 57; 59628 before)
# Package 33c (spec M5 open item 15): every tick held, every line but the standing
# runtime's own the same; the lines moved by the held lines said the first time and then
# once a watch (the frigate 157 to 18, the schooner 155 to 15, the thick passage 31 to
# 6), the conflict rule's grain (the lead, the log and a bearing no longer contrary to one
# another or to a manoeuvre on "the ship": 21 to 1, 24 to 2, 2 to 1, those left the helm's,
# "keep her full" against the heave-to, the wear or the stand-off), and the well entered
# and held (one refusal for two lines). Package 33b moved the ticks: the lookout's
# distance by estimation is drawn once a sighting episode, and the departure's estimate
# off Ushant ("two miles", was "a mile") put the account a mile differently, from which
# the book shaped the course; the lines and digests below are the merge of the two.
# Package 35 (the pilot boarding from the cutter; spec M5 §23): the Falmouth pilot's
# cutter comes off when she is within the pilot's cruising ground by day, is sighted by
# the lookout ("Sail ho!", the sail's estimate drawn from a stream of its own), hails
# her within four cables and puts the pilot aboard within two, with his words and the
# port's news; nothing of the ship's physics moves, so every tick above stands and only
# the lines and the digests change (the frigate 624 → 629 lines, the schooner 725 → 730;
# the thick passage, which never comes within the cruising ground, is untouched). The
# pilot's ticks are pinned below (docs/dev/TuningNotes.md, package 35). Package 36
# generalised the cutter into a vessel of the world sailing by her own file's polar
# (seven knots on a reach, not six capped at half the wind) and sighted at the horizon
# her masthead gives: she comes out sooner and is seen sooner (the frigate's cutter
# sighted 55800 → 54600, "three leagues"; the hail 57720 → 56940, before the frigate has
# shortened sail, so the pilot boards once she is slow enough, at the anchor, 58020 →
# 58200; the schooner's 54840 → 53640, 56880 → 56820, 56940 → 57000); nothing of the
# ship's own moves, the lines grow by the sail's lines (629 → 633, 730 → 734) and the
# digests follow (the hail's line carries the cutter's errand in its data too, for the
# book's `the pilot's hail` and `the pilot asks to be put off`); the thick passage, with
# no cutter, is untouched (docs/dev/TuningNotes.md, package 36). The cutter comes off from
# the pilots' station, the outer road, not from the shore (36: from the shore of Brest she
# beat out six hours for a ship in the Iroise), so she is sighted two leagues off bearing
# N by W, hails at 56280 and puts the pilot aboard at 56340, half an hour before the
# anchor (the schooner's 55320 and 55380). Measured in package 36's tree before the lead's
# tide-words change to `ports.py`, which moved these two digests again and no tick; the
# lead reconciles.

# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
GATE_5B_SAIL_SIGHTED_TICK = 55620  # "Sail ho! A sail right ahead" (package 57; 55500)
GATE_5B_PILOT_HAIL_TICK = 57240  # the cutter hails within four cables (package 57; 57120)
GATE_5B_PILOT_ABOARD_TICK = 57300  # the pilot aboard, a minute after (package 57; 57180)
GATE_5B_LINES = 731  # the well's order gone, its two held lines (2026-10-21; 733 at 56, 729 at 57)
# decision 45, the pilot's news: 750b3c658d6973c3 before; package 37p (9a0c4168d6987405 before)
GATE_5B_DIGEST = (
    "9a1f2802ba7c6533"  # the well (2026-10-21; c8c81b7617e4e0fd at 56, 5f682b9f676a2db4 at 57)
)
# The schooner, package 37e (old beside new): the landfall 43920 → 44400, the Beast, the
# Lizard and its lights at one look, the account a cable and a half out after the
# bearing; the outer road 56502 → 56517; the anchor off the town 57615 → 58210 in six
# fathoms and a half (ten and a half before), brought up 58618 → 59395; 760 → 799 lines.
# The pilot's cutter hails her at 56160 and he does not board (55380 before): see the
# test of it below, an expected failure.
# Package 37f (old beside new), her book unchanged: hove to for the cast at 28799 → 28851
# and the cast had at 29938 → 30176; the landfall 44400 → 45840, the Beast at four
# leagues; the outer road 56517 → 56515; the anchor off the town 58210 → 57638 in seven
# fathoms (six and a half), brought up 59395 → 58690; the pilot's hail 56160 → 55800,
# and he does not board, as before; 799 → 761 lines.
# Package 37k (2026-10-09): every tick and the true track held; two lines more, "Her sails
# lifting" twice on the run in from the Lizard (52912, 53538), the wind come forward of
# the yards' trim on a compass course (docs/dev/TuningNotes.md, package 37k).
# c8905673506f717e before package 37k (78eec3dcd5f33c16 on Windows then)
# (37h and 37k merged 2026-10-09: the figures above are 37h's; the two together are
# re-measured at 37j's merge, the tuning notes saying both.)
# Package 37h (2026-10-09): the pilot aboard before she runs in, the expected failure's
# mark off. Her book gains three lines and a guard (docs/dev/TuningNotes.md, package 37h):
# `take the pilot` at his hail shortens sail as it asks, the cutter keeps company with her
# at seven knots and hails again ten minutes later for her to heave to, which the same
# line answers; he boards as she comes to the outer road, she fills away when he is
# aboard and shapes for Carrick Road (the noon's "stand on" guarded to the noon's own
# filling away). Every tick to the hail stands; old beside new: the hails 55800 → 55800
# and 56400, the outer road 56515 → 56511, the pilot aboard at 56580 (never before), the
# anchor 57638 → 58244 in eight fathoms and a half (seven), brought up 58689 → 59360;
# 761 → 800 lines (the hails, the answers, the boat's waiting, the heave-to and the fill
# away, the pilot's words and his warning of the Black Rock as she anchors).
# Package 37k: every tick held; three lines more, "Her sails lifting" (45989, 49980, and
# 54445, ten seconds before the cry of "Taken aback" at the land close aboard)
# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
# Package 37j (her book unchanged): every tick to the cast stands; her noon's sight is
# weighed and moves the account a mile to the SSW (1.15 miles; the octant's two miles
# and a half against an account a mile and a half in doubt, within their doubts
# together), and the cast says the master's tide. Old beside new: the landfall
# 45840 → 46200, the Beast at four leagues; the outer road 56515, unchanged; the pilot's
# hail 55800 → 55860, and he does not board, as before; "off the town" at the first cast
# under ten fathoms (six, at 57312), and while she is brought to for the anchor "keep her
# full" bears her away a point (57554) and she runs on into the channel between St
# Anthony's Head and the Black Rock: the anchor 57638 → 57643 in seventeen fathoms and a
# half (seven), brought up 58689 → 58795 in eighteen and a half; 761 → 756 lines.
GATE_5B_SCHOONER_LANDFALL_TICK = 46140  # 46200 before package 37p, 45840 before 37j
GATE_5B_SCHOONER_ROADS_TICK = 56234  # the outer road: sail shortened (56515 before the merge)
GATE_5B_SCHOONER_PILOT_HAIL_TICK = 55860  # the cutter's hail; taken at it (55800)
GATE_5B_SCHOONER_PILOT_HAIL_AGAIN_TICK = 56460  # her second, to heave to (37h; 56400 before)
GATE_5B_SCHOONER_PILOT_ABOARD_TICK = 56940  # aboard off the outer road (37h; 56580 before)
GATE_5B_SCHOONER_ANCHORED_TICK = 57257  # off the town, the best bower let go (57255 before 37p)
GATE_5B_SCHOONER_BROUGHT_UP_TICK = 58224  # brought up (58213 before package 37p)
# The well's order gone from the starter book (2026-10-21), its two held lines, as the three
# passages above it; missed at the fold-in, re-pinned at package 68 (found on the way: the
# tree before 68 gives these figures, and the tree before the fold-in, 953caab, the old
# with the two "sound the well" lines at tick 0 the whole difference)
GATE_5B_SCHOONER_LINES = 766  # the well (768 at 56, 763 at package 45)
# decision 45, the pilot's news: 70018ada5004a81e before; package 37p (d6031efa9808a2b1 before)
# package 58a, the recurring lines: a trim waiting for hands or the lead's cast said again in
# the same words is routine, not notable; every tick and line the same (TuningNotes, 58a)
GATE_5B_SCHOONER_DIGEST = "2b68e8b1f60e8496"  # 58a (b9acdeac6354f3bf, the well; b7c16adc at 56)
GATE_5B_THICK_LANDFALL_TICK = 53880  # package 57 (53820 before; 54420 before package 37j)
# Package 37m (2026-10-09): every tick to the landfall stands; at it the book's `steer S`
# puts her about for the starboard tack and keeps her full and by (37j's grounding on
# Black Head at 56081 gone), 475 → 478 lines (docs/dev/TuningNotes.md, package 37m).
GATE_5B_THICK_TACKED_TICK = 54115  # put about off Black Head, full and by (54063 before 57)
GATE_5B_THICK_LINES = 469  # the well's order gone (2026-10-21; 471 at 57, 472 at 45, 495 at 37p)
GATE_5B_THICK_DIGEST = (
    "6f062dc60419f52c"  # the well (2026-10-21; 155a46cede6c96a3 at 57, e358748a1eae5fc6 at 45)
)


def the_landfall(log):
    """The landfall of the passage: the land raised after the departure's (the lookout's
    first look off Ushant is a landfall too, at tick 0; the lookout marks a landfall
    itself, land raised after none was in sight, so the first `lookout.lost` need not
    precede it: in fog the land close aboard is raised, stood off from and lost again)."""
    return [
        e for e in log if e.kind == "lookout.sighting" and e.data.get("landfall") and e.tick > 0
    ]


def the_passage(path: str, hours: int, ship: str | None = None):
    """A passage of gate 5b run for its hours, with the account beside the truth at each
    notable moment: [(tick, kind, text, truth, account)]."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(path)
    world = make_scenario_world(sf, ship=ship)
    moments: list[tuple] = []

    def watch(e) -> None:
        landfall = e.kind == "lookout.sighting" and e.data.get("landfall")
        if e.kind in ("reckoning.noon", "sounding", "bearing.taken") or landfall:
            nav = world.navigation
            moments.append(
                (
                    "landfall" if landfall else e.kind,
                    e.tick,
                    e.text,
                    world.position,
                    nav.account_now(),
                )
            )

    world.log.subscribe(watch)
    begin(world, sf)
    run(world, hours * 3600)
    world.log.unsubscribe(watch)
    return world, moments


@pytest.fixture(scope="module")
def gate_5b_passage():
    return the_passage(GATE_5B_PASSAGE, GATE_5B_HOURS)


def _miles(a, b) -> float:
    from freesail.world.geo import bearing_and_distance

    return bearing_and_distance(a, b)[1] / units.NAUTICAL_MILE


def test_truth_58_four_days_of_thick_weather_leave_the_ellipse_lying_east_and_west():
    """Spec M5 §19, truth 58: "Four days from Finisterre in thick weather without a sight,
    the reckoning's ellipse is 30 to 50 miles long east and west and under ten north and
    south, and a clear noon collapses the north-south axis to under five." The traverse
    fed a day's run of 150 miles at six knots and a quarter for four days, the wind
    free, on the course from Finisterre for the Channel (north-north-east) and on the
    Channel's own (east): the ellipse's length is twice its standard deviation
    (`Reckoning.ellipse`, `uncertainty_words`); N §3's 30 to 50 miles, Chan et al.'s
    figures an upper bound and not a target."""
    from freesail.world import reckoning as K
    from freesail.world.geo import Position

    for course_deg in (22.5, 90.0):
        r = K.Reckoning(Position(43.0, -9.3), sigma_nm=1.0)
        by_day = {}
        for h in range(96):
            r.advance(1.0, math.radians(course_deg), 6.25, (h + 1) * 3600)
            if (h + 1) % 24 == 0:
                by_day[(h + 1) // 24] = r.ellipse()
        e = by_day[4]
        assert 30.0 <= 2 * e["sigma_east_nm"] <= 50.0, (course_deg, e)
        assert 2 * e["sigma_north_nm"] < 10.0, (course_deg, e)
        assert 60.0 < e["major_bearing_deg"] < 120.0  # lying east and west
        # the biases grow in a straight line: two days about twice one, four about four
        assert 1.8 < by_day[2]["sigma_east_nm"] / by_day[1]["sigma_east_nm"] < 2.2
        assert 3.5 < by_day[4]["sigma_east_nm"] / by_day[1]["sigma_east_nm"] < 4.2
        words = r.uncertainty_words
        assert (
            words.startswith("I would not trust the reckoning within ")
            and "miles east or west" in words
        )
        # a clear noon with a good horizon and the sextant: two miles or so
        r.update_latitude(r.lat_deg + 0.1, 2.0)
        e = r.ellipse()
        assert 2 * e["sigma_north_nm"] < 5.0 and 30.0 <= 2 * e["sigma_east_nm"] <= 50.0


def test_truth_59_a_cast_of_the_deep_sea_lead_moves_the_reckoning_onto_the_contour():
    """Spec M5 §19, truth 59: "A cast of the deep-sea lead in the Channel Soundings moves
    the reckoning onto the chart's contour consistent with the ground and narrows it
    across the contour to a few miles, leaving it along the contour as it was." The
    frigate in forty-six fathoms south of the Lizard with the account set nineteen
    miles off in the shoal water under the Manacles, eight miles in doubt."""
    from freesail.world import reckoning as K
    from freesail.world.geo import Position

    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": 49.70, "lon_deg": -5.20},
        region=CHART_REGION,
    )
    world = make_world(SEED, FRIGATE, sc)
    r = world.navigation.reckoning
    wrong = Position(50.0, -5.10)
    r.set_position(wrong, 0, sigma_nm=8.0)
    before = r.ellipse()
    world.submit("heave the deep-sea lead")
    run(world, 20 * 60)
    cast = [e for e in world.log if e.kind == "sounding"][-1]
    assert "; fine grey sand with black specks. " in cast.text and cast.data["matched"]
    # package 37e, the one rule: the cast is weighed by the two doubts, the account's eight
    # miles and the cast's own (the tolerance over the fathoms the chart shelves in a mile
    # there, a mile and a half here), and the line says so; `SOUNDING_ACROSS_SIGMA_NM`,
    # three miles whatever the bottom, is gone
    assert cast.data["how"] == K.WEIGHED
    # package 37j: the cast reduced by the master's tide above his chart's datum (a metre
    # and a tenth here), the contour matched within his doubt at another point of it,
    # where the bottom shelves less: a line of six miles (a mile and a half before), and
    # the account moved five miles and a half (five) to the SSE (SE by S); package 57: two
    # leagues to the S by E (five miles and a half to the SSE), the frigate brought to for
    # the cast under her new rig aloft (Steel's staysails stowed, the royals sent down)
    assert cast.text.endswith("The account moved two leagues to the S by E.")
    assert 0.5 < cast.data["line_sigma_nm"] < 7.0
    # the lead reads the tide (package 34): the cast is laid on the chart less the master's
    # own allowance for it, by his almanac. Weighed, the account comes ninety-six parts in
    # a hundred of the way to the contour (eight miles of doubt against a mile and a
    # half), so it lies within a fathom of the contour's own tolerance and not on it: the
    # truth's "onto the contour" held to the letter only while a cast after a long run
    # replaced the account, which package 37e's one rule no longer does unless the
    # account is plainly out (for the lead to rule: spec M5 §19 truth 59's words, §33)
    # Package 37j: matched where the bottom shelves less, the line six miles, the account
    # goes two thirds of the way (eight miles of doubt against six) and stands within
    # seven fathoms of the cast's depth on the chart, nearer it than the twelve it began
    # in and nearer the truth; the truth's "onto the contour" is held to that, for the
    # lead's sentence (spec M5 §19, §33)
    on_the_chart = cast.data["depth_m"] - world.navigation._tide_allowance_m()
    assert abs(world.chart.depth_at(r.position) - on_the_chart) <= units.fathoms_to_m(7.0)
    assert abs(world.chart.depth_at(r.position) - on_the_chart) < abs(
        world.chart.depth_at(wrong) - on_the_chart
    )
    assert cast.data["moved_nm"] > 4.5
    assert _miles(r.position, world.position) < _miles(wrong, world.position)
    after = r.ellipse()
    assert after["semi_minor_nm"] <= cast.data["line_sigma_nm"] + 0.01  # a few miles across
    assert after["semi_major_nm"] > 0.8 * before["semi_major_nm"]  # along it as it was
    assert "by account" in world.readings.words("reckoning")


def _frigate_with_a_chronometer(
    drift: float, start: datetime, lat: float = 49.5, lon: float = -5.2
):
    """The frigate given a chronometer by a test scenario (package 33b: the gate's
    passage files stay without one), rated at Plymouth forty days before 5 June 1805,
    gaining 1.8 seconds a day by its certificate, the true rate `drift` seconds a day
    from that; a quiet day on a fixed south-westerly, no sea kept."""
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region=CHART_REGION,
        instrument="sextant",
        chronometer={
            "maker": "Earnshaw",
            "where": "Plymouth",
            "rated": "1805-04-26",
            "rate_s_per_day": 1.8,
            "drift": drift,
        },
    )
    return make_world(SEED, FRIGATE, sc)


def _lon_miles(world, lon_deg: float) -> float:
    truth = world.position
    return abs(lon_deg - truth.lon_deg) * 60.0 * math.cos(math.radians(truth.lat_deg))


def test_truth_60_the_chronometer_within_four_miles_and_a_lunar_shows_it_gaining():
    """Spec M5 §19, truth 60: "The frigate with a chronometer rated at Plymouth forty
    days before has a longitude by chronometer within four miles of the truth when the
    rate is right, and a lunar on a quiet day shows the chronometer gaining when the
    scenario's rate is wrong by two seconds a day." Seed 7, 5 June 1805 (the moon at the
    first quarter, in distance of the sun through the afternoon); the truth read from
    the world (`world.position`), never from a reading."""
    from freesail.world import sights as S

    right = _frigate_with_a_chronometer(0.0, datetime(1805, 6, 5, 9, 0))
    e = right.submit("take a sight for the longitude")
    assert e.kind == "reckoning.time_sight" and "the Earnshaw 40 days from Plymouth" in e.text
    sight = right.navigation.last_time_sight
    assert sight.days_since_rated == 40
    assert _lon_miles(right, sight.longitude_deg) < 4.0
    assert _lon_miles(right, right.readings["longitude_by_chronometer"]["lon_deg"]) < 4.0
    # the rate wrong by two seconds a day: forty days make eighty seconds, twenty
    # minutes of longitude, thirteen miles west at this latitude, which the time sight
    # carries and the lunar does not
    wrong = _frigate_with_a_chronometer(2.0, datetime(1805, 6, 5, 9, 0))
    wrong.submit("take a sight for the longitude")
    off = wrong.navigation.last_time_sight.longitude_deg
    assert 9.0 < _lon_miles(wrong, off) < 17.0 and off < wrong.position.lon_deg
    wrong.run(8 * 3600 + 40 * 60)  # 17:40, the moon twenty degrees up and the sun forty
    e = wrong.submit("take a lunar")
    assert e.kind == "order.accepted"
    wrong.run((S.LUNAR_ON_DECK_MINUTES + 9 + S.LUNAR_CLEARING_MINUTES) * 60)
    lines = [x for x in wrong.log if x.kind == "reckoning.lunar"]
    assert len(lines) == 1 and "he thinks it gaining on its rate" in lines[0].text
    lunar = wrong.navigation.last_lunar
    assert lunar.chronometer_fast_s > S.CHRONOMETER_FAULT_S
    assert _lon_miles(wrong, lunar.longitude_deg) < _lon_miles(
        wrong, lunar.chronometer_longitude_deg
    )
    error = wrong.readings["chronometer_error_by_lunar"]
    assert "gaining on its rate" in error["words"] and error["fast_s"] > 0
    assert lines[0].data["chronometer_fast_s"] == error["fast_s"]


def test_truth_61_the_lunar_is_refused_in_words_that_say_which_and_answers_within_a_degree():
    """Spec M5 §19, truth 61: "`take a lunar` is refused within three days of new moon,
    with the moon under fifteen degrees, and in thick weather, in words that say which;
    allowed, it occupies the master and two mates for a quarter of an hour and answers
    within a degree an hour later." The new moon of 27 June 1805; the moon just risen on
    the 5th at ten past two; the sky pinned thick by the test; then the afternoon's
    lunar of the sun."""
    from freesail.world import sights as S
    from freesail.world.weather import Conditions

    young = _frigate_with_a_chronometer(0.0, datetime(1805, 6, 26, 10, 0))
    e = young.submit("take a lunar")
    assert e.kind == "order.rejected" and "No lunar to be had: the moon is" in e.text
    assert "from the change" in e.text
    low = _frigate_with_a_chronometer(0.0, datetime(1805, 6, 5, 14, 10))
    e = low.submit("take a lunar")
    assert e.kind == "order.rejected" and "the moon is too low" in e.text and "degrees up" in e.text
    thick = _frigate_with_a_chronometer(0.0, datetime(1805, 6, 5, 17, 40))
    thick.conditions = Conditions("warm", "warm", "thick", "", "fog", "a mile", 1012.0)
    e = thick.submit("take a lunar")
    assert e.kind == "order.rejected" and "the sky is thick with fog" in e.text
    assert thick.readings.words("longitude_by_lunar").startswith("no lunar to be had: the sky")
    world = _frigate_with_a_chronometer(0.0, datetime(1805, 6, 5, 17, 40))
    e = world.submit("take a lunar")
    assert e.kind == "order.accepted"
    master = world.navigation.master
    assert master.occupied and master.occupied_with == "lunar" and master.place == "on deck"
    inst = next(i for i in world.ship.extra["evolutions"].instances if i.evo.id == "take_lunar")
    assert inst.want.hands == 2 and inst.evo.steps[0].duration_s == S.LUNAR_ON_DECK_MINUTES * 60
    tick0 = world.clock.tick
    world.run(S.LUNAR_ON_DECK_MINUTES * 60 - 60)
    assert not [x for x in world.log if x.kind == "lunar.taken"]
    world.run(10 * 60)  # the file's quarter of an hour at the hands' pace in the weather
    taken = [x for x in world.log if x.kind == "lunar.taken"]
    assert len(taken) == 1 and taken[0].tick - tick0 <= (S.LUNAR_ON_DECK_MINUTES + 9) * 60
    assert master.place == "below"
    world.run(S.LUNAR_CLEARING_MINUTES * 60)
    lines = [x for x in world.log if x.kind == "reckoning.lunar"]
    assert len(lines) == 1 and lines[0].tick == taken[0].tick + S.LUNAR_CLEARING_MINUTES * 60
    lunar = world.navigation.last_lunar
    assert abs(lunar.longitude_deg - world.position.lon_deg) < 1.0
    assert "longitude by lunar" in lines[0].text and "would trust within" in lines[0].text


def test_the_passage_for_gate_5b_at_seed_7_has_its_own_constants(gate_5b_passage):
    """The frigate's passage Ushant to Falmouth (spec M5 §20): the departure bearing off
    the Stiff, the log hove hourly, the noon sight, the Channel Soundings by the deep-sea
    lead with the ship brought to, the Lizard raised and bearings taken, the course for
    Falmouth shaped from the account, the lead going in and the ship brought to an anchor
    in the outer road (package 34); the account against the truth at each; the lines and
    the digest."""
    world, moments = gate_5b_passage
    log = world.log
    noon = [e for e in log if e.kind == "reckoning.noon"]
    assert [e.tick for e in noon] == [GATE_5B_NOON_TICK]
    assert noon[0].text.startswith("Noon. Latitude by observation ")
    assert noon[0].data["sight"]["instrument"] == "sextant"
    heaves = [e for e in log if e.kind == "log.read"]
    assert len(heaves) >= GATE_5B_HOURS - 2 and all(e.data["automatic"] for e in heaves[:3])
    casts = [e for e in log if e.kind == "sounding"]
    assert casts[0].tick == GATE_5B_CAST_TICK and casts[0].data["deep"]
    # the tide over the chart's depth at the Channel Soundings (package 34); fifty-five
    # where she lies since package 37d moved her track (fifty-three before); package 37e:
    # every observation's line says what the master did with it
    # package 37j: and what the master's own tide took off before he laid it on the chart
    assert casts[0].text == (
        "Fifty-five fathoms; fine grey sand with black specks. Two fathoms of tide allowed by "
        "the epitome: fifty-three fathoms on the chart. The account kept."
    )
    hove = [e for e in log if e.kind == "ship.hove_to"]
    assert [e.tick for e in hove] == [GATE_5B_HOVE_TO_TICK]  # for the cast only
    # package 37f: her way taken off first, and the tack said; no sail's "taken aback"
    assert hove[0].text == "Hove to on the larboard tack, main topsail to the mast, helm a-lee."
    assert not [e for e in log if e.kind in ("sail.backed", "ship.forced_round", "ship.filled")]
    assert [e.tick for e in log if e.kind == "ship.wore"] == []  # she anchors, and wears no more
    landfall = the_landfall(log)
    assert landfall[0].tick == GATE_5B_LANDFALL_TICK and landfall[0].data["id"] == "the-beast"
    bearings = [e for e in log if e.kind == "bearing.taken"]
    assert bearings[0].tick == 0 and bearings[0].data["id"] == "stiff-light"  # the departure
    assert any(e.data["id"] == "the-beast" for e in bearings)
    courses = [e for e in log if e.kind == "helm.set"]
    assert any(e.text.startswith("Shaped a course for Falmouth") for e in courses)
    # package 37e: the course is made good against the master's tide, and the Manacles
    # rounded by a point east of them
    # (package 37f: and the course for the point worked again every glass on the way)
    made_good = [e for e in courses if (e.data.get("allowing") or {}).get("made_good")]
    assert len(made_good) == 17 and all(e.data["allowing"]["by"] == "book" for e in made_good)
    assert len([e for e in courses if e.actor == "standing order 'the course for the point'"]) > 12
    assert " to make it good; the allowance holds till the tide turns, " in made_good[0].text
    assert [e.actor for e in courses if e.text.startswith("Shaped a course for Falmouth")] == [
        "standing order 'round the Manacles'"
    ]
    roads = [e for e in log if e.actor == "standing order 'the outer road'"]
    assert roads and roads[0].tick == GATE_5B_ROADS_TICK
    # the ending at anchor (package 34): the best bower let go in the outer road, brought
    # up with five times the depth, riding; nothing dragging, nothing aground
    anchored = [e for e in log if e.kind == "ship.anchored"]
    brought_up = [e for e in log if e.kind == "ship.brought_up"]
    assert [e.tick for e in anchored] == [GATE_5B_ANCHORED_TICK]
    assert [e.tick for e in brought_up] == [GATE_5B_BROUGHT_UP_TICK]
    assert brought_up[0].text.startswith("Brought up by the best bower in ")
    assert world.at_anchor and not world.ship.extra.get("aground")
    assert not [e for e in log if e.kind in ("anchor.dragging", "ship.aground")]
    riding = world.ship.extra["ground_tackle"].riding_by()
    assert 9.0 < units.m_to_fathoms(riding.depth_m) < 20.0 and riding.scope_fathoms >= 45.0
    assert world.readings.words("anchor").startswith("down, riding by the best bower to the")
    # the pilot boarding from the cutter (package 35; spec M5 §23): the cutter sighted
    # as any sail is, a bearing first; the hail; the pilot aboard as a person with his
    # words and the port's news, before she anchors (package 36: the cutter comes off
    # from the outer road, the pilots' station); the ship's own ticks unmoved
    sails = [e for e in log if e.kind == "lookout.sighting" and e.data.get("seen_as") == "sail"]
    assert sails and sails[0].tick == GATE_5B_SAIL_SIGHTED_TICK
    assert sails[0].text.startswith("Sail ho! A sail right ahead, bearing ")
    hail = [e for e in log if e.kind == "port.pilot_hail"]
    aboard = [e for e in log if e.kind == "port.pilot_aboard"]
    assert [e.tick for e in hail] == [GATE_5B_PILOT_HAIL_TICK]
    assert [e.tick for e in aboard] == [GATE_5B_PILOT_ABOARD_TICK]
    assert aboard[0].text.startswith(
        "The pilot, Mr Tregenza of Falmouth, came aboard from the cutter"
    )
    words = [e for e in log if e.kind == "port.pilot_words"]
    assert words[0].tick == GATE_5B_PILOT_ABOARD_TICK and "Carrick Road" in words[0].text
    assert (
        world.dealings.pilot is not None and world.people.find("the pilot") is world.dealings.pilot
    )
    assert world.readings.words("pilot").startswith(
        "Mr Tregenza of Falmouth aboard; high water at Falmouth about"
    )
    assert not world.vessels.active(), "the cutter lies to under her lee, then goes back"
    # the account against the truth (the author's view: the truth is in the world and
    # the tests only)
    by_kind = {}
    for kind, tick, _text, truth, account in moments:
        by_kind.setdefault(kind, []).append((tick, _miles(truth, account)))
    # the longitude by account at noon, the day's run and the stream's set in it (6.6
    # miles with the tide in, 3.6 without: package 34, the log-line's bias; 5.9 since
    # package 37e, two miles out before the sight and laid three miles north by a sight
    # that was itself five and a half miles too far north)
    assert by_kind["reckoning.noon"][0][1] < 8.0
    # made by the reckoning, corrected by the land: seven miles out at the cast in the
    # Soundings and six at the landfall, the lights and the land raised at one look as
    # before 37d (6.9 miles out then). Package 37d, second pass: the landfall's bearing
    # draws her onto its line and says "five leagues by estimation; three leagues by the
    # account"; the distance is not laid down then, her account believing its doubt along
    # that sight (her latitude, by the noon's sight) the less, and she is four miles out
    # until the bearing two glasses after lays it down and the fix follows (within a mile
    # and a half from 17:10)
    # Package 37e: six miles out at the cast, nine and a half when the land is raised (the
    # noon's sight above, and the Channel's stream against the master's tide), two and a
    # third when the landfall's bearing has been worked, a mile and a quarter from the fix
    # two glasses after. Package 37j: four miles and a half out at the cast (the noon's sight
    # weighed, not taken), eight and a half at the landfall, two and a third after its
    # bearing
    assert 4.0 < by_kind["sounding"][0][1] < 12.0
    assert 7.0 < by_kind["landfall"][-1][1] < 12.0
    after_the_bearing = [m for m in moments if m[0] == "bearing.taken" and m[1] == landfall[0].tick]
    assert after_the_bearing and _miles(after_the_bearing[0][3], after_the_bearing[0][4]) < 3.0
    final = [m for m in moments if m[0] == "bearing.taken"][-1]
    assert _miles(final[3], final[4]) < 2.0  # in the Roads, within a mile or two
    assert len(log) == GATE_5B_LINES and log.digest()[:16] == GATE_5B_DIGEST


def test_the_pace_on_the_passage_holds_truth_51s_floor(gate_5b_passage):
    """Spec M5 §30 and package 33a: the queries and the reckoning per tick on the
    passage (the traverse board every tick, the grounding check, the lookout once a
    minute, the log hourly): the best of three thousands at least BUILD_MACHINE_FLOOR.
    Measured on the build machine: docs/dev/TuningNotes.md, M5b, package 33a."""
    import time

    world, _ = gate_5b_passage
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"


def test_the_passage_in_thick_weather_makes_its_landfall_wrong_on_the_reckoning():
    """Spec M5 §20: the same passage with the sky pinned thick, no sight at noon, the
    course for Falmouth shaped by account when the run since noon says she is off the
    Lizard, and the land raised close aboard where the reckoning's errors put her, some
    twelve miles from where she believed herself; the ellipse read at noon and at the
    landfall."""
    world, moments = the_passage(GATE_5B_PASSAGE_THICK, GATE_5B_THICK_HOURS)
    log = world.log
    noon = [e for e in log if e.kind == "reckoning.noon"][0]
    assert (
        noon.tick == GATE_5B_NOON_TICK and "No sight; the sun was hid at noon in fog" in noon.text
    )
    assert world.readings.words("latitude_by_observation").startswith("No sight today;")
    landfall = the_landfall(log)
    assert landfall[0].tick == GATE_5B_THICK_LANDFALL_TICK
    assert landfall[0].text.startswith("The land about Black Head close aboard")
    # at the land close aboard she stands off to the southward (the book's "the land")
    off = [e for e in log if e.actor == "standing order 'the land'" and e.kind == "order.accepted"]
    assert off and off[0].tick == landfall[0].tick and "steering s" in off[0].text
    kinds = {m[0]: m for m in moments}
    tick, _, _, truth, account = kinds["landfall"]
    # the landfall made wrong: eleven miles before package 37e, six since (the master's
    # tide and her drift hove to for the cast are in the account now, and no sight)
    assert 4.0 < _miles(truth, account) < 9.0
    assert account.lat_deg > truth.lat_deg  # she believed herself further on
    e = world.navigation.reckoning.ellipse()
    assert 2.0 < e["sigma_east_nm"] < 6.0 and 1.0 < e["sigma_north_nm"] < 6.0
    # Package 37j found her taking the ground on Black Head's ledges at 56081: the book's
    # "the land" steered S into the south-westerly, too near the wind, and she was taken
    # aback with no way on and set onto the ledges. Package 37m (the owner's ruling 3 of
    # 2026-10-09): the same `steer S` is judged against her head and the wind, too near
    # to be laid on the starboard tack, and she is put about (luffed up and braced up
    # first, being off the wind) and kept full and by on the starboard tack, standing off
    # to the southward; the land is out of sight at 54900 and she does not take the
    # ground (docs/dev/TuningNotes.md, package 37m). The book is not tuned.
    helm = [x for x in log if x.kind == "helm.order" and x.tick == landfall[0].tick]
    assert helm and helm[0].text.startswith(
        "Helm ordered: steer S (180°); S (180°) lies too near the wind to be laid; she is put "
        "about and kept full and by on the starboard tack."
    )
    tacked = [x for x in log if x.kind == "ship.tacked"]
    assert [x.tick for x in tacked] == [GATE_5B_THICK_TACKED_TICK]
    # package 57: 170 degrees (171 before), her new rig aloft
    assert tacked[0].text.endswith("on the starboard tack, heading S by E (170°), full and by.")
    assert not [x for x in log if x.kind == "ship.aground"]
    # package 37p: put about, she came up with too little way, was taken aback and boxed
    # off by the helm (54424, two minutes aback), and the book's "keep her full" bore her
    # away a point twice, so that she ends on a compass course (full and by before it)
    # package 45: full and by at the end (the course for Falmouth lies too near the wind to
    # be laid, and the helm's rules keep her so without the box-off of 37p)
    assert world.ship.dyn.helm_mode.value == "full_and_by"
    assert len(log) == GATE_5B_THICK_LINES and log.digest()[:16] == GATE_5B_THICK_DIGEST


# Package 37d (2026-10-06): the first pass (a bearing a line and no more) left her
# account leagues along the Lizard's line at her landfall on that one mark and she took
# the ground standing in for Carrick Road; the second pass lays the lookout's distance
# down with the bearing when the account's doubt along the sight is the greater, and she
# makes her landfall, her pilot and her berth on the ticks recorded before 37d. The lines
# and the digest moved (the bearings' words, the fixes, the shore's sightings).
@pytest.fixture(scope="module")
def gate_5b_schooner():
    return the_passage(GATE_5B_PASSAGE_SCHOONER, GATE_5B_SCHOONER_HOURS)


def test_the_schooner_sails_the_passage_with_her_octant_and_the_log_every_two_hours(
    gate_5b_schooner,
):
    world, moments = gate_5b_schooner
    log = world.log
    assert world.navigation.log_interval_h == 2
    heaves = [e for e in log if e.kind == "log.read" and e.data["automatic"]]
    assert [e.ship_time.hour for e in heaves[:3]] == [6, 8, 10]
    noon = [e for e in log if e.kind == "reckoning.noon"][0]
    assert noon.tick == GATE_5B_NOON_TICK and noon.data["sight"]["instrument"] == "octant"
    landfall = the_landfall(log)
    assert landfall[0].tick == GATE_5B_SCHOONER_LANDFALL_TICK
    assert landfall[0].data["id"] in ("lizard-point", "the-beast")  # the two at one look
    # her own ending (package 34): at the outer road she shortens sail and stands on for
    # Carrick Road by the eastern channel, and comes to an anchor off the town at the
    # first cast under ten fathoms, within St Anthony's; brought up, riding, nothing
    # dragging and nothing aground
    roads = [e for e in log if e.actor == "standing order 'the outer road'"]
    assert roads and roads[0].tick == GATE_5B_SCHOONER_ROADS_TICK
    # the order accepted, not the conflict line said first since 37h ('the pilot boards'
    # and 'off the town' fire together as she comes to the road; the later stands)
    town = [
        e for e in log if e.actor == "standing order 'off the town'" and e.kind == "order.accepted"
    ]
    assert town and "coming to an anchor" in town[0].text
    # the pilot's cutter comes off and hails her (package 35), and again for her to heave
    # to (package 37h); his boarding is the test after this one
    hail = [e for e in log if e.kind == "port.pilot_hail" and e.data.get("errand") == "bring"]
    assert [e.tick for e in hail] == [
        GATE_5B_SCHOONER_PILOT_HAIL_TICK,
        GATE_5B_SCHOONER_PILOT_HAIL_AGAIN_TICK,
    ]
    anchored = [e for e in log if e.kind == "ship.anchored"]
    brought_up = [e for e in log if e.kind == "ship.brought_up"]
    assert [e.tick for e in anchored] == [GATE_5B_SCHOONER_ANCHORED_TICK]
    assert [e.tick for e in brought_up] == [GATE_5B_SCHOONER_BROUGHT_UP_TICK]
    assert world.at_anchor and not world.ship.extra.get("aground")
    assert not [e for e in log if e.kind in ("anchor.dragging", "ship.aground")]
    riding = world.ship.extra["ground_tackle"].riding_by()
    # six fathoms and a half and thirty-three of cable since package 37e (ten and a half
    # and fifty-two before: she comes to further in, by the eastern channel made good);
    # eighteen and a half and eighty-eight since package 37j (borne away a point by "keep
    # her full" while she was brought to, she ran on into the channel off St Anthony's)
    assert 5.0 < units.m_to_fathoms(riding.depth_m) < 20.0 and riding.scope_fathoms >= 30.0
    assert _miles(world.position, world.navigation.account_now()) < 1.0
    assert len(log) == GATE_5B_SCHOONER_LINES and log.digest()[:16] == GATE_5B_SCHOONER_DIGEST


def test_the_schooners_pilot_boards_before_she_runs_in(gate_5b_schooner):
    """Package 35's beat of the schooner's passage, as it was pinned until package 37e:
    the pilot aboard before she runs in, American colours no bar at Falmouth, the port
    neutral to her (55380 then, a minute after the hail). Package 37e left him astern of
    her at seven knots and the test was marked an expected failure; package 37h takes him
    at his hail, his cutter keeps company with her and hails again for her to heave to,
    and he boards as she comes to the outer road, before her anchor off the town."""
    world, _ = gate_5b_schooner
    log = world.log
    aboard = [e for e in log if e.kind == "port.pilot_aboard"]
    assert [e.tick for e in aboard] == [GATE_5B_SCHOONER_PILOT_ABOARD_TICK]
    assert aboard[0].tick > GATE_5B_SCHOONER_PILOT_HAIL_TICK
    assert aboard[0].text.endswith("to pilot her in (American colours being no bar at Falmouth).")
    taken = [e for e in log if e.kind == "port.pilot_answered"]
    assert [e.data["wants"] for e in taken] == ["shorten sail", "heave to"]
    roads = [e for e in log if e.actor == "standing order 'the outer road'"]
    anchored = [e for e in log if e.kind == "ship.anchored"]
    # he boards as she comes to the outer road (twelve minutes after its rule on the
    # merged tree of 2026-10-09, where 37h's figure was six) and before the anchor (five
    # minutes before it on the merged tree: she slows late for him and anchors soon after)
    assert abs(aboard[0].tick - roads[0].tick) < 900
    assert anchored[0].tick - aboard[0].tick > 240


@pytest.mark.parametrize("ship", ["data/ships/cutter.yaml", "data/ships/brig.yaml"])
def test_the_cutter_and_the_brig_sail_through_the_same_orders(ship):
    """Spec M5 §20: the cutter and the brig through the passage's orders, a short leg
    each: the log hove at their interval, the departure bearing taken, no navigation
    order refused, the account within a few miles of the truth after six hours."""
    world, moments = the_passage(GATE_5B_PASSAGE_SCHOONER, 6, ship=ship)
    log = world.log
    nav = world.navigation
    assert nav.log_interval_h == (1 if "brig" in ship else 2)
    heaves = [e for e in log if e.kind == "log.read"]
    assert len(heaves) >= (5 if "brig" in ship else 2)
    assert any(e.kind == "bearing.taken" and e.tick == 0 for e in log)
    refused = [
        e
        for e in log
        if e.kind == "order.rejected"
        and any(w in e.data["order"] for w in ("bearing", "log", "lead", "reckoning", "course"))
    ]
    assert refused == [], [e.text for e in refused]
    assert _miles(world.position, nav.account_now()) < 8.0
    assert nav.master.name.startswith("Mr ")


# ---------------------------------------------------------------------------
# Milestone 5c: places, people, ports and nations (package 35; spec M5 §22 to §24, §28)
# ---------------------------------------------------------------------------
#
# Truths 68 to 70 at seed 7. The ports are files on one machinery (data/ports/); the
# schooner is American by her company's names, so Falmouth and Brest are neutral to her
# and the French market's war rule reads Britain's war, not hers. Everything inward is
# reached by an order or a reading, everything outward arrives through something the
# ship models: the boat, the gangway, the messenger, the cabin door.

THE_RADE_INNER = {"lat_deg": 48.345, "lon_deg": -4.470}  # the Bay of Brest, within the Goulet
CARRICK_ROAD_5C = {"lat_deg": 50.160, "lon_deg": -5.034}  # Falmouth, twelve fathoms


def _in_port(where, ship=SCHOONER, heading=250.0, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 9, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position=where,
        region=CHART_REGION,
        **kw,
    )
    world = make_world(SEED, ship, sc)
    world.run(60)
    world.submit("let go the best bower")
    world.run(300)
    assert world.at_anchor
    return world


def test_truth_68_a_message_from_brest_reaches_the_captain_in_his_cabin_by_boat_door_and_person():
    """Spec M5 §28, truth 68: "A message from Brest reaches the captain in his cabin only
    by the boat, the door and a person, each a line in the log in order, and never by a
    line from nowhere." The schooner at anchor in the Bay of Brest with a letter waiting
    at the port; the captain gone below; the boat sent ashore for the prices."""
    from freesail.world.people import PASS_THE_WORD_S, Message

    letter = "The Prefect maritime begs the captain to dine on Thursday."
    world = _in_port(
        THE_RADE_INNER,
        ports={"brest": {"letters": [{"text": letter, "origin": "Brest"}]}},
        cargo={"purse_pounds": 200.0},
    )
    e = world.submit("go below")
    assert e.kind == "captain.below" and world.people.captain.where == "cabin"
    before = len(world.log)
    e = world.submit("send the boat ashore")
    assert e.kind == "order.accepted" and world.dealings.boat.away
    for _ in range(240):
        world.run(60)
        if events(world, "message.received"):
            break
    kinds = [x.kind for x in list(world.log)[before:]]
    chain = [
        "boat.away",
        "boat.ashore",
        "boat.returning",
        "boat.alongside",
        "message.aboard",
        "message.door",
        "message.received",
    ]
    found = [k for k in kinds if k in chain]
    assert found == chain, found
    ticks = {k: next(x.tick for x in world.log if x.kind == k) for k in chain}
    assert ticks["boat.away"] < ticks["boat.ashore"] < ticks["boat.returning"]
    assert ticks["boat.returning"] < ticks["boat.alongside"] == ticks["message.aboard"]
    assert ticks["message.aboard"] < ticks["message.door"] == ticks["message.received"]
    assert ticks["message.door"] - ticks["message.aboard"] == PASS_THE_WORD_S
    aboard = events(world, "message.aboard")[0]
    assert aboard.data["carried_by"] == "the long-boat"
    assert "came aboard by the long-boat" in aboard.text
    messenger = world.people.messenger
    assert messenger is not None and messenger.name in aboard.text  # a person carries it
    door = events(world, "message.door")[0]
    assert door.text == f"{messenger.name} knocked at the cabin door with a letter from Brest."
    received = events(world, "message.received")[0]
    assert received.text == f"The captain read it: {letter}" and received.data["place"] == "cabin"
    # never a line from nowhere: no letter is read that did not come aboard first, and
    # the port's letter was given once
    assert len(events(world, "message.received")) == 1 == len(events(world, "message.aboard"))
    assert world.dealings.ports["brest"].letters == []
    # the same chain to the quarterdeck: the messenger brings it to him on deck
    world.submit("come on deck")
    world.dealings.ports["brest"].letters.append(Message("A second word.", "Brest"))
    world.submit("send the boat ashore")
    for _ in range(240):
        world.run(60)
        if len(events(world, "message.received")) == 2:
            break
    second = events(world, "message.door")[1]
    assert second.text.startswith(
        f"{messenger.name} brought a letter from Brest to the captain on the quarterdeck"
    )


def test_truth_69_the_cargo_bought_at_falmouth_and_sold_at_brest_makes_the_sum_the_two_lists_give():
    """Spec M5 §28, truth 69: "The schooner's cargo bought at Falmouth and sold at Brest
    makes or loses the sum the two markets' prices give, and a week's war news moves a
    price by the rules table." Forty tons of tin: bought at Falmouth after the boat has
    brought the list off, sold at Brest likewise (a second world, the hold given the
    tin, since the passage between is gate 5c's); the purse moves by the two lists'
    figures and nothing else. Then the news: England at peace with France takes the war
    rule's half off English tin at Brest (`ports.WAR_FACTOR`), and the war declared
    again puts it back."""
    from freesail.world import ports as PT

    falmouth = _in_port(CARRICK_ROAD_5C, cargo={"purse_pounds": 6000.0})
    e = falmouth.submit("buy forty tons of tin")
    assert e.kind == "order.rejected" and "not known" in e.text  # the boat first
    falmouth.submit("send the boat ashore with the mate")
    for _ in range(240):
        falmouth.run(60)
        if events(falmouth, "boat.alongside"):
            break
    listed = falmouth.readings["prices"]
    assert listed["port"] == "falmouth"
    tin_at_falmouth = listed["prices"]["tin"]
    purse0 = falmouth.purse.pounds
    e = falmouth.submit("buy forty tons of tin")
    assert e.kind == "market.bargain" and e.data["sum_pounds"] == 40 * tin_at_falmouth
    assert falmouth.purse.pounds == purse0 - 40 * tin_at_falmouth
    for _ in range(300):
        falmouth.run(60)
        if events(falmouth, "market.bought"):
            break
    assert falmouth.hold.goods == {"tin": 40.0}
    assert falmouth.readings.words("manifest").startswith("40 tons of tin; room for 72 tons")
    assert "The manifest written up by the mate" in events(falmouth, "paper.written")[-1].text
    # at Brest, the hold carrying the tin bought
    brest = _in_port(
        THE_RADE_INNER, cargo={"purse_pounds": falmouth.purse.pounds, "goods": {"tin": 40.0}}
    )
    brest.submit("send the boat ashore")
    for _ in range(240):
        brest.run(60)
        if events(brest, "boat.alongside"):
            break
    tin_at_brest = brest.readings["prices"]["prices"]["tin"]
    assert tin_at_brest > tin_at_falmouth  # English tin is dear in a French port at war
    purse1 = brest.purse.pounds
    e = brest.submit("sell forty tons of tin")
    assert e.kind == "market.bargain" and e.data["sum_pounds"] == 40 * tin_at_brest
    assert brest.purse.pounds == purse1 + 40 * tin_at_brest and brest.hold.goods == {}
    # the voyage's sum is the two lists' figures and nothing else
    assert brest.purse.pounds - 6000.0 == pytest.approx(40 * (tin_at_brest - tin_at_falmouth))
    # the rules table: the price at Brest is the file's base through the season's, the
    # war's and the supply's factors; a week's news of peace moves it by the war's
    port = brest.ports.ports["brest"]
    good = port.market.goods["tin"]
    factors = port.market.factors(good, brest.clock.ship_time, brest.nations, port.nation)
    assert factors["war"] == PT.WAR_FACTOR and factors["season"] == 1.0
    assert factors["supply"] == pytest.approx(1.0 - PT.SUPPLY_PER_TON * 40.0)  # forty tons sold
    brest.run(7 * 86400)  # a week: the glut clears by a seventh a day
    sold_before = brest.ports.price_of(port, "tin")
    assert brest.nations.make_peace("britain", "france", "1805-06-19")
    at_peace = brest.ports.price_of(port, "tin")
    assert sold_before == pytest.approx(at_peace * PT.WAR_FACTOR, abs=PT.PRICE_ROUND)
    brest.nations.declare_war("britain", "france", "1805-06-26", "the pilot's news")
    assert brest.ports.price_of(port, "tin") == sold_before
    # the list the purser brought off is a paper, as current as its last entry
    page = brest.papers.page("the price list")
    assert page.lines[0].startswith("Prices at Brest, 12 June")


def test_truth_70_a_port_closed_to_the_ships_nation_refuses_her_in_the_pilots_words():
    """Spec M5 §28, truth 70: "A port closed to the ship's nation refuses her entry in
    the pilot's words and the stance is the nations table's." The American schooner
    standing in for Brest with the port closed to the United States by the scenario's
    order: the pilot cutter comes off, hails, and the pilot refuses from the cutter;
    the stance read from the table and the port's closure is 'closed'. The British
    frigate on the same approach: hostile, and no cutter comes off at all."""
    approach = {"lat_deg": 48.30, "lon_deg": -4.75}

    def standing_in(ship, **kw):
        sc = Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=225.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=80.0,
            ship_speed_kn=4.0,
            position=approach,
            region=CHART_REGION,
            **kw,
        )
        world = make_world(SEED, ship, sc)
        world.submit("set plain sail")
        return world

    schooner = standing_in(SCHOONER, ports={"brest": {"closed_to": ["united-states"]}})
    brest = schooner.ports.ports["brest"]
    assert schooner.dealings.ship_nation == "united-states"
    assert schooner.dealings.stance(brest) == "closed"
    assert schooner.nations.stance("france", "united-states", brest.closed_to) == "closed"
    for _ in range(360):  # six hours at most; the cutter from the road is up with her in one
        schooner.run(60)
        if events(schooner, "port.pilot_refused"):
            break
    refused = events(schooner, "port.pilot_refused")
    assert len(refused) == 1 and refused[0].data["stance"] == "closed"
    assert refused[0].text.startswith(
        "The pilot hailed from the cutter: Brest is closed to the Americans by the port's "
        "order; you will get no pilot here"
    )
    assert schooner.dealings.pilot is None and schooner.people.find("the pilot") is None
    assert "the port closed to the Americans" in schooner.readings.words("port")
    sails = [e for e in events(schooner, "lookout.sighting") if e.data.get("seen_as") == "sail"]
    assert sails and sails[0].tick < refused[0].tick  # the cutter was sighted first
    # hostile: no pilot comes off to a King's ship, and the port says so
    frigate = standing_in(FRIGATE)
    assert frigate.dealings.stance(frigate.ports.ports["brest"]) == "hostile"
    frigate.run(2 * 3600)
    assert not events(frigate, "port.pilot_hail") and not frigate.vessels.active()
    assert "the port hostile to the English" in frigate.readings.words("port")
    # open: her own port, where the pilot comes off (the passage of gate 5b has it)
    assert frigate.dealings.stance(frigate.ports.ports["falmouth"]) == "open"


# ---------------------------------------------------------------------------
# Truths 67, 71 and 72 at seed 7 (package 36; spec M5 §25 to §28). Other sail at far
# detail is a hull from one of the ship files with a polar drawn once from the file,
# moved by the player's wind and tide; the lookout sees her at the horizon her masthead
# gives and names her rig only as she nears; the world-order channel is the scenario's
# and the harness's, never the captain's; the two scenarios of gate 5c replay to their
# digests from their files.
# ---------------------------------------------------------------------------

OPEN_WATER_5C = {"lat_deg": 49.60, "lon_deg": -5.40}  # south-west of the Lizard, forty fathoms


def _open_sea(ship=FRIGATE, heading=180.0, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=0.0,
        position=OPEN_WATER_5C,
        region=CHART_REGION,
        **kw,
    )
    return make_world(SEED, ship, sc)


def _put(world, description, bearing_deg, miles, goal, nation="britain"):
    from freesail.world import ships as S
    from freesail.world.geo import destination

    pos = destination(world.position, bearing_deg, miles * units.NAUTICAL_MILE)
    spec = {"description": description, "name": description.title(), "nation": nation}
    spec |= {"position": pos, "goal": goal}
    world.vessels.serial += 1
    return world.vessels.add(S.vessel_from_spec(world, spec, world.vessels.serial))


def test_truth_67_a_far_ship_moves_by_the_players_wind_and_tide_and_is_sighted_at_the_horizon():
    """Spec M5 §28, truth 67: "A ship at far detail moves by the same wind and tide as the
    player and is sighted at the horizon distance her rig's height and the visibility
    give, as 'Sail ho!' with a bearing first and her rig only as she nears." A merchant
    brig put thirty miles north-east of the anchored frigate, bound south-west on a reach
    to pass a mile from her:
    she is moved once a game minute at her polar's speed for her course in the wind at
    her place, the tide's stream added over the ground; the lookout hails her as "Sail
    ho! A sail" with a bearing and an estimate, no rig, when she comes within the horizon
    the two mastheads give (2.08 times the root of each height in metres, C §5.5), and
    her rig, her colours and what she is follow as she nears, in that order."""
    from freesail.world import ships as S
    from freesail.world.geo import bearing_and_distance, horizon_nm

    w = _open_sea()
    w.submit("let go the best bower")
    w.run(60)
    v = _put(w, "merchant brig", 45.0, 30.0, "bound for 49 21 N 5 45 W")
    # moved by the wind at her place and the tide, once a minute
    p0 = v.position
    w.run(59)
    assert v.position == p0
    w.run(1)
    wind_from, wind_ms = v._wind_at(w)
    base_from, base_ms = float(w.wind.direction_from), float(w.wind.speed)
    assert abs(units.wrap_pi(math.radians(wind_from) - base_from)) < 1e-9
    assert wind_ms == pytest.approx(base_ms)
    off = abs(units.rad_to_deg(units.wrap_pi(math.radians(v.heading_deg - wind_from))))
    assert v.speed_kn == pytest.approx(
        v.polar.speed_kn(off, units.ms_to_knots(wind_ms)) * v.sailing_factor
    )
    _, run_m = bearing_and_distance(p0, v.position)
    east, north = w.tide.stream_at(v.position, w.clock.ship_time)
    # a few metres: the stream read at the minute's end, not along it
    assert abs(run_m - units.knots_to_ms(v.speed_kn) * 60.0) <= math.hypot(east, north) * 60.0 + 5.0
    # sighted at the horizon the two mastheads give, as a sail with a bearing first
    eye = w.lookout.height_of_eye_m
    horizon = horizon_nm(eye, S.rig_height_m(v.ship_file))
    assert 22.0 < horizon < 24.0  # a frigate's eye to a brig's masthead
    sails = []
    for _ in range(6 * 60):
        w.run(60)
        sails = [e for e in events(w, "lookout.sighting") if e.data.get("seen_as") == "sail"]
        if sails:
            break
    assert sails and sails[0].text.startswith("Sail ho! A sail ")
    assert ", bearing " in sails[0].text and "brig" not in sails[0].text
    _, at_m = bearing_and_distance(w.position, v.position)
    assert at_m / units.NAUTICAL_MILE <= horizon + 0.15  # a minute's run inside the line
    assert at_m / units.NAUTICAL_MILE > horizon - 1.0
    assert "distance_m" not in sails[0].data and sails[0].data["estimate_m"] > 0
    # her rig, her colours and what she is, as she nears, in that order
    made = []
    for _ in range(8 * 60):
        w.run(60)
        made = events(w, "lookout.made_out")
        if len(made) >= 3 or v.done:
            break
    assert [e.data["level"] for e in made[:3]] == [1, 2, 3]
    assert " is a brig, " in made[0].text
    assert made[1].text.endswith("shows British colours, the red ensign.")
    assert "a merchant brig, deep laden" in made[2].text


def test_truth_71_a_scenarios_world_order_is_journaled_at_its_tick_and_the_captains_is_refused():
    """Spec M5 §28, truth 71: "A world order given by the scenario at a time is journaled
    at that tick with its source; the same order typed at the captain's prompt is
    refused." The naval cruise's own orders by time, run through its first quarter of an
    hour with the first of them moved to the first minute: the line at the driver's mark
    with the source "the scenario", saved with the world and not among the inputs; the
    same words at the prompt refused in words that say whose channel it is; the
    harness's order the same line with its own source, an input that replays."""
    from freesail.world import orders as world_channel
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/naval-cruise.yaml")
    order = sf.scenario.world_orders[0]["order"]
    sf.scenario.world_orders = [{"at": "1805-06-12T06:01", "order": order}] + [
        o for o in sf.scenario.world_orders[1:]
    ]
    world = make_scenario_world(sf)
    begin(world, sf)
    world.run(900)
    lines = events(world, "world.order")
    assert [(e.tick, e.actor, e.data["source"]) for e in lines] == [(60, "driver", "the scenario")]
    assert lines[0].text.startswith("World order (the scenario): a cutter sent from Plymouth")
    saved = world.save()
    assert [(o["tick"], o["source"]) for o in saved["world_orders"]] == [(60, "the scenario")]
    assert not [i for i in saved["inputs"] if "world_order" in i]
    # the captain's grammar refuses the same words, naming the channels
    e = world.submit(order)
    assert e.kind == "order.rejected"
    assert "an order to the world, not to the ship" in e.text
    assert e.text.rstrip(".").endswith(world_channel.REFUSAL.rstrip("."))
    for words in ("the weather", "the other sail", "a message", "a port", "the people ashore"):
        assert words in e.text
    assert not [x for x in events(world, "world.order") if x.tick > 60]
    # and the harness's order is the same line with its own source, an input replayed
    world.world_order("port falmouth: price of tin 140")
    harness = [x for x in events(world, "world.order") if x.tick > 60]
    assert harness and harness[0].data["source"] == "the harness"
    assert [i["source"] for i in world.save()["inputs"] if "world_order" in i] == ["the harness"]


# The two scenarios of gate 5c at seed 7 (spec M5 §27, §29; package 36), each run whole
# under its own book (`data/scenarios/*.orders`; the starter book is a choice and not
# loaded), with a save taken at a tick for truth 72's replay. The merchant passage runs
# thirty-six hours (12 June 05:00 to 13 June 17:00: the tin bought, out on the ebb, the
# Channel crossed, the Iroise passed, the road of Bertheaume on the ebb, the Goulet on
# the flood, the Bay of Brest, the tin sold); the naval cruise forty-eight
# (12 June 06:00 to 14 June 06:00: the yard's stores, the station, the cutter's letter,
# the stranger put on the sea across the station, two days under the book); the
# merchant passage's thirty-six hours end with the tin sold in the Bay of Brest at 15:10
# on the 13th, the flood having served by daylight the same forenoon she anchored in the
# road of Bertheaume on the ebb. The constants below are the
# build machine's (docs/dev/TuningNotes.md, package 36). The fixtures are module-scoped
# and sail two or three game days each: the lead adds them to `tests/conftest.py`'s
# DAY_FIXTURES so that they are the slow tier's (this file does not mark them).
GATE_5C_MERCHANT = "data/scenarios/merchant-passage.yaml"
GATE_5C_CRUISE = "data/scenarios/naval-cruise.yaml"
GATE_5C_MERCHANT_HOURS = 36
GATE_5C_CRUISE_HOURS = 48
GATE_5C_MERCHANT_SAVE_TICK = 12 * 3600  # 17:00 on the 12th, the Channel crossing
# 08:00 on the 13th (09:00 before package 37d; the chase in hand then, and since package
# 37e lost half an hour before)
GATE_5C_CRUISE_SAVE_TICK = 30 * 3600  # 12:00 on the 13th, the brig spoken (26 h before 45c)
GATE_5C_SHIPS = 12  # the dozen ships of each scenario, the player's not among them
# the naval cruise's ticks at seed 7
GATE_5C_CRUISE_YARD_TICK = 5460  # thirty days' provisions off from the King's yard
GATE_5C_CRUISE_UNDER_WAY_TICK = 6834  # under way on the starboard tack, S by W
# Package 37f (lying to): her true track parts at the anchor let go at the start (tick
# 130: the helm righted as it goes, and "Brought up" said at 153), and every tick to her
# getting under way stands. Off the Sound she is hove to for the pilot with her way taken
# off (8876 → 9056) and filled on the tack she is on; old beside new: the pilot aboard
# 7920 → 7980, put off 11220 → 10980; the port admiral's cutter within hail 84153 → 83838
# and the letter read 84213 → 83898; the Palinure sighted and chased at 90000 as before,
# on the starboard quarter at four miles (abeam at three leagues), and lost to sight at
# 92040 → 93420, never spoken (the test after this one); thirteen wears in the two days
# (eleven and a tack), and one wear that failed, at 80653, "she would not come round":
# two of the book's orders each gave chase to the admiral's cutter at one tick, each
# queued a wear, and the second began as the first ended and "by the wind" took its helm;
# 2144 → 1988 lines (the heave-to's and the wears' per-sail lines gone, 77 to 20).
# Package 37h (2026-10-09; docs/dev/TuningNotes.md, its section): the book takes the
# pilot at his hail (`take the pilot`), and his boat, hailing at four cables, keeps
# company and closes at her own pace or the frigate's and two knots more: he is aboard
# a minute sooner, 7980 → 7920. Every other tick stands; 2037 → 2041 lines (the answer,
# the order's line), the digest with them.
GATE_5C_CRUISE_PILOT_ABOARD_TICK = 7920  # Mr Tozer aboard off the Sound, 08:12 (7980)
GATE_5C_CRUISE_PILOT_LEFT_TICK = 10980  # put off into his cutter, the ship hove to for it, 09:03
GATE_5C_CRUISE_WORLD_ORDERS = [
    (14400, "the scenario"),
    (86400, "the scenario"),
    (102600, "the scenario"),  # package 45c: the Palinure at 10:30 (90000, 07:00, before)
]
# Package 37e (the account; a course shaped to make good): every tick to the pilot's
# leaving stands. The course for the station, shaped as she fills away (11273), is SSW
# 203° to make good SW by S against the ebb, where 37d's was the heading SSW 207°: on
# 207° she lay with her topsails unfilled and no way on her for an hour and fifty
# minutes ("Hove the log: no way" at 14437, a fault of the filling away and no part of
# the book), and it was in that hour that the port admiral's cutter, sent at 10:00, came
# up with her. On 203° her topsails fill at 11477, she makes seven knots and a half, and
# the cutter is a stern chase of nineteen hours: within hail at 05:22 on the 13th, on the
# station (84153; 17840 before), the letter read a minute after (84213; 17900).
# Package 37j (the account amended): every tick to the pilot's leaving stands; the
# chronometer's sight hove to off Plymouth at 09:00, 7.6 miles out against an account a
# cable in doubt by the land, which 37e took, is now doubted and the account kept ("the
# sight stands two leagues and a half to the E of the account, and the account, good to
# a cable, is the better figure: the account kept"), so the course for the station is
# shaped from another account and her track parts there. Old beside new: the cutter
# within hail 83484 → 83423 and the letter read 83544 → 83483; the Palinure sighted
# right ahead at four leagues 90120 → 90000 and chased at once (90121 → 90000), spoken
# at 07:59 (94091 → 93979) under no colours and lost to sight astern 98100 → 98040;
# fourteen wears; 2037 → 2059 lines.
# Package 37m (2026-10-09; docs/dev/TuningNotes.md, its section): every tick to 20:00 on
# the 12th stands; there the book's "back to the station" shapes SW by S across the wind's
# eye from her head, and she is put about for it (two knots and more on her) where the
# fold-in's guard wore her, so her track parts there. Old beside new: the cutter within
# hail 83423 → 84631 and the letter read 83483 → 84691; the Palinure sighted and chased
# at 90000 as before, spoken 93979 → 93663, out of sight astern 98040 → 97560; thirteen
# wears and a tack in the two days (fourteen wears); 2065 → 2083 lines.
GATE_5C_CRUISE_CUTTER_HAIL_TICK = (
    91023  # the admiral's cutter within hail on the 13th (package 57; 91024 before)
)
GATE_5C_CRUISE_LETTER_READ_TICK = 91083  # the letter read a minute after (package 57; 91084)
# Package 37d: the departure fixed by cross bearings off Plymouth and the account a line
# from each bearing after; every tick to the first noon stands, the station is reached on
# another track, the Palinure is raised on the larboard bow seven minutes later (91380;
# 90960 right ahead) and spoken at 08:26 (95189; 106931, the frigate having had to wear
# and run her down); ten wears in the two days (docs/dev/TuningNotes.md, package 37d).
# The second pass moved her digest and no tick: the bearings' words where the distance is
# laid down.
# Package 37e: with the cutter's hail at 05:22 and the course shaped for the station
# again at it, the frigate is three leagues to the south-eastward of the Palinure when the
# scenario puts her on the sea at 07:00 (90000), standing SW by S for the station on the
# starboard tack: the brig is sighted the same minute abeam to starboard, bearing NW (91380
# before, right on the frigate's bow), the chase given the same minute (91800 before), the
# frigate kept full and by on the tack that opens her, worn round for her at the next
# glass and the chase lost to sight at 92040, never spoken (95189 before): see the test
# of it below, an expected failure. Eleven wears and a tack in the two days (ten).
# The fold-in of m5c-c (2026-10-08; docs/dev/TuningNotes.md, its section): the
# Palinure put five leagues on the frigate's bow at seven where the frigate now is,
# as the audit tried it; a square-rigged ship under sail is worn for a chase or a
# shaped course whose turn passes through the wind's wake (the station shaped for
# from the cutter's hail no longer takes her aback at 83957, and the chase no longer
# at 91954); the book's sighting rule makes her out and the made-out line gives
# chase once. The cutter is within hail at 05:11 (83484; 83838) on the station; the
# brig is sighted right ahead three leagues at 07:02 (90120), chased by her bearing
# with the course led, made out, spoken at 08:08 (94091) under no colours with the
# chase in hand at the save of 08:00, the chase given up at her hail and the brig
# out of sight astern at 09:15 (98100). Fourteen wears in the two days; no urgent
# line. The merchant passage measured on this machine (Linux) differs from the
# owner's Windows figures by two lines and two ticks (the anchor in the Bay 115815,
# 115817; 2994 lines, 2992): pinned here as measured, the difference recorded as an
# open item.
# Package 45c (2026-10-16): the Palinure re-placed by the scenario at 10:30 on the 13th,
# five leagues on the frigate's bow as she stands for the station's south-west end (at
# 07:00 since package 45's helm she was put on the sea astern of the frigate while the
# frigate still chased the admiral's cutter, and never spoken; the chase rule mended
# beside it, docs/dev/TuningNotes.md, package 45c): the cutter within hail at 07:17 and
# the letter read, the brig sighted on the starboard bow at 10:45, chased, spoken at 11:55
# under no colours and lost astern at 15:23; twelve wears in the two days.
GATE_5C_CRUISE_STRANGER_SIGHTED_TICK = 103560  # the Palinure on the bow (package 57; 103500)
GATE_5C_CRUISE_CHASE_TICK = 103561  # the chase given at the sighting (package 57; 103501)
GATE_5C_CRUISE_SPOKEN_TICK = 107736  # within hail under no colours (package 57; 107738)
GATE_5C_CRUISE_CHASE_LOST_TICK = 119700  # the brig out of sight astern (package 57; 120180)
GATE_5C_CRUISE_NOON_TICKS = [21600, 108240]
GATE_5C_CRUISE_WEARS_AT_LEAST = 8  # wore ship on the station, and once for the chase
# Package 37k (2026-10-09): every tick and the true track held; two lines more, "Her sails
# lifting" as the chase's course is steered after the brig is spoken (94136) and twenty-five
# seconds before the book's late "Taken aback" at 14:09 on the 13th (115759, 115784)
# (docs/dev/TuningNotes.md, package 37k).
# (37h and 37k merged 2026-10-09: the figures above are 37h's; the two together are
# re-measured at 37j's merge, the tuning notes saying both.)
# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
GATE_5C_CRUISE_LINES = 2242  # package 56, the glass (2225 at package 57)
# the judgement a sentence of its own after a shaped course's line (the lead, after 37m;
# 348b07dd901580a7 at package 37m, 15e7f10b2ca8eb9a on the merged tree before it)
# decision 45, the pilot's news: f603c2724a58fef1 before; package 37p (24428443ec6992f9 before)
# package 58a, the recurring lines: a trim waiting for hands or the lead's cast said again in
# the same words is routine, not notable; every tick and line the same (TuningNotes, 58a)
GATE_5C_CRUISE_DIGEST = "5a62f6fca122c6ad"  # 58a (728522e26dd25a49 at 56, the glass)
# the merchant passage's ticks at seed 7
GATE_5C_MERCHANT_TIN_ABOARD_TICK = 14249  # forty tons by the lighter, the boat alongside, 08:57
GATE_5C_MERCHANT_UNDER_WAY_TICK = 16007  # under way on the ebb, starboard tack, S by E
# Package 37e (the account; the book set for a true account and a course made good):
# every tick to the Falmouth pilot's hail stands; her true track parts at the first
# course shaped under way (16608, "clear of the road", S by E of 37d's heading by the
# ebb's allowance). Old beside new: the Falmouth pilot put off 18420 → 18540; the sail
# off the Lizard 26280 → 26640; the cast in the Iroise 91836 → 91418, forty-one fathoms
# (thirty-nine), and the line says "The account kept."; the pilot of Brest aboard
# 98160 → 97800 and put off again at 100620, before the anchor (he asks for his boat
# when she opens her distance from Brest, which she does stemming the ebb at the
# entrance of the Chenal du Four; a second pilot does not come off); the anchor in the
# road of Bertheaume 101373 → 101821 in seven fathoms (nine and a half), the turn to the
# flood at its tick, the mouth of the Goulet 112740 → 112444, the anchor in the Bay
# 116140 → 116110, the tin sold 123901 → 124441; 2634 → 3146 lines (a fix after every
# bearing in pilot water, the course for the road worked every five minutes, the tide's
# lines). She passes the Mingan 1.9 cables to the north (356 m; 328 m after 37d) and the
# shore under Petit Minou seven tenths of a cable off, in eleven fathoms
# (docs/dev/TuningNotes.md, package 37e).
# Package 37f (lying to, and the ground; the fore-and-aft cast): her book unchanged but
# for the guard on its three trim rules. Every tick to the tin aboard stands; her true
# track parts as she gets under way (tick 14250: a fore-and-after's helm is tended from
# the first heave), and she casts: "She has paid off" 92 seconds after the anchor is
# aweigh (15596), where the cast timed out at seven minutes and said the same (15917).
# Old beside new: under way 16005 → 16007; the Falmouth pilot aboard 16320 → 16200 and
# put off 18540 → 18300, the ship hove to for it on her tack with her way off; the sail
# off the Lizard 26640 → 29100, abeam to starboard at three leagues; the cast in the
# Iroise 91418 → 90240, thirty-eight fathoms (forty-one), the account kept; the pilot of
# Brest aboard 97800 → 96240, and he stays aboard to the anchor (he asked for his boat
# at 100620 before); the anchor in the road of Bertheaume 101821 → 99974 in twelve
# fathoms (seven), the turn to the flood at its tick, the mouth of the Goulet
# 112444 → 112112, the anchor in the Bay 116110 → 115817, the tin sold 124441 → 123951;
# 3146 → 2992 lines (a standing order with nothing to do says so once a watch for each
# reason, where "in the Bay ... she is at anchor already" was said twenty-six times and
# "tend the sheets ... She is at anchor" twenty-one; "Brought up" said in Carrick Road at
# the start; the casts that find no bottom routine). docs/dev/TuningNotes.md, package 37f.
# Package 37h (2026-10-09; docs/dev/TuningNotes.md, its section): the book takes the
# pilot at his hail after its fore topsail (`take the pilot`, which shortens no more sail
# with the sail coming in already). Every tick of the passage stands but two: the pilot
# of Brest aboard 96240 → 96180 (his boat keeps company and closes at the ship's pace and
# two knots more), and he is put off at the anchor in the Bay of Brest at 121560, the
# pilotage paid (he stayed aboard to the end before: game 1's Brest pilot, never put off
# and never paid). 2994 → 3011 lines (the answers, the pilot's warnings of the Black Rock,
# the Buzec and the shoal water off Petit Minou, his asking for his boat and her coming).
# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
# Package 37j (the account amended; her book unchanged): every tick to the Falmouth pilot
# put off stands (the departure was laid a mile out by a draw, and is laid at the truth
# now; the hourly heave of the log and the sights are the ship's own). Her true track
# parts at the first course shaped from the account; at noon on the 12th her sight is
# weighed and moves the account a cable, and at the second, in the mouth of the Goulet,
# the account is within a cable of the truth and the sight within the doubts together of
# it ("the account kept"): the fold-in's case (an octant's sight five miles and a half
# north of an account fixed to three cables) does not arise on this track, and is held in
# `tests/test_reckoning.py` by its figures. Old beside new: the sail off the Lizard
# 29100 → 25740 (on the larboard bow, four leagues; the sail abeam at three leagues is
# sighted at 29400); the Iroise's cast is not made (90241 before): the course for the
# Passage de l'Iroise shaped at 02:00 from twenty miles off is not worked again within
# ten miles of Ushant, and she passes the mark more than a mile and a half off by
# account, so "bring to in the Iroise" never fires (the test after this one, an expected
# failure; as before package 37d's second pass); the pilot of Brest aboard
# 96240 → 94380; the anchor in the road of Bertheaume 99974 → 98814 in eight fathoms and
# a half (twelve), at the first cast under thirteen fathoms, which is the lead's own now
# and not the chart's at her true place (item 7); the mouth of the Goulet
# 112078 → 112178; the anchor in the Bay 115815 → 116282 in seven fathoms and a half;
# the tin sold 123948 → 125159; 2994 → 2976 lines.
GATE_5C_MERCHANT_PILOT_ABOARD_TICKS = [
    16200,
    96540,  # package 45 (94380 at 37p, 96240 before package 37j)
]  # Mr Tregenza of Falmouth in the outer road; Mr Le Floch of Brest in the Iroise
GATE_5C_MERCHANT_PILOT_LEFT_TICKS = [
    18300,
    121620,  # package 45c (121500 at 45, 121380 at 37p)
]  # Mr Tregenza put off beyond the outer road, the ship hove to for it; Mr Le Floch at the
# anchor in the Bay of Brest, from the quay (package 37h)
GATE_5C_MERCHANT_SAIL_OFF_LIZARD_TICK = (
    26100  # "Sail ho! A sail on the larboard bow", not made out (25740 at 37p; package 45's helm)
)
GATE_5C_MERCHANT_NOON_TICKS = [25200, 111660]
# the cast at the Iroise's mark, 13th (90240 on Windows); not made since package 37j
GATE_5C_MERCHANT_IROISE_CAST_TICK = 90318  # package 45 (90241 at 37p)
GATE_5C_MERCHANT_ANCHORED_TICKS = [
    57,
    100616,  # package 45 (98515 at 37p, 98814 before it)
    115547,  # package 45c, the Bay's road moved onto its twelve fathoms (116411 at 45)
]  # Carrick Road; the road of Bertheaume on the 13th; the Bay
GATE_5C_MERCHANT_FLOOD_TICK = (
    108960  # the turn to the flood at Bertheaume, 11:16 on the 13th, by daylight
)
# Package 37k (2026-10-09): every tick and the true track held; one line more, "Her sails
# lifting, the wind 63° on the larboard bow" in the Goulet (112740), twenty-two seconds
# before the book's 'trim to the course' trims her (docs/dev/TuningNotes.md, package 37k).
# (37h and 37k merged 2026-10-09: the figures above are 37h's; the two together are
# re-measured at 37j's merge, the tuning notes saying both.)
# (37j merged after 37h and 37k, 2026-10-09: the figures below are 37j's as measured on
# its branch; the six passages are re-measured on the merged tree by the lead, below.)
GATE_5C_MERCHANT_GOULET_TICK = 112142  # the mouth of the Goulet (112189 at 37p)
GATE_5C_MERCHANT_TIN_SOLD_TICK = 123272  # the boat alongside from the quay (125387 at 45)
# Package 37m (2026-10-09): every tick stands; at anchor in the Bay at 129600 the hourly
# course for the Iroise, on the other tack with no way on her, is refused as keeping her
# full and by ("'keep her full and by' must wait till she weighs", the refusal of 126000,
# not said again) where it was refused as a tack; 2999 → 2998 lines
# (docs/dev/TuningNotes.md, package 37m).
# package 68 (item 1, riding means riding): she ranges ahead on her cable at half a knot
# from 153 to 302 while she comes to in Carrick Road, not yet brought up, and the account
# runs the while (a hundred and fifty seconds; it did not, the anchor being down): the
# lead in pilot water's distance at 300 reads 110 miles (111), and the master's tide is
# said at 15600 when she has weighed (one line more); the old rule restored gives the old
# figures, every tick the same (docs/dev/TuningNotes.md, package 68)
# package 58b (item 3, the wind across the stern; by bisection, the item turned off gives
# every old figure): at 75681, the schooner running ESE for the Iroise, the wind comes a
# point past dead astern to the larboard quarter with her yards braced for the starboard
# tack, and the deck says so once ("brace them round when you will"), the book's trim
# bracing them at 75791 as before: one line more, every tick the same
GATE_5C_MERCHANT_LINES = 3100  # package 58b (3099 at 68, riding; 3098 at 56, 3080 at 57)
# decision 45, the pilot's news: 59ed46c3625c766d before; package 37p (54713e8e579fd527 before)
# package 56, the glass: 05f0f4aba2eddbc0 (06b14a75a5eaae8b at 57)
# the lead at the merge of 58a and 58b (2026-10-23): 58a's figure was "36c17b76e1735975"
# package 68, riding: 902be35aeeac7b54
# the merged tree of 58a and 58b (2026-10-23): 58b alone gave 26c859e23ceccd42; the digest reads
# severity, and 58a's recurring lines are routine in this passage too
GATE_5C_MERCHANT_DIGEST = "6abbbff4d7fa1a57"  # package 58b, the stern (902be35aeeac7b54)


def _people(world) -> list[dict]:
    return [p.to_dict() for p in world.people.all]


def the_scenario_whole(path: str, hours: int, save_tick: int):
    """A scenario of gate 5c run whole under its book, with the account beside the truth
    at each notable moment and a save at `save_tick`: (world, moments, (save, digest))."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(path)
    world = make_scenario_world(sf)
    moments: list[tuple] = []

    def watch(e) -> None:
        landfall = e.kind == "lookout.sighting" and e.data.get("landfall")
        if e.kind in ("reckoning.noon", "sounding", "bearing.taken", "ship.anchored") or landfall:
            nav = world.navigation
            moments.append(
                (
                    "landfall" if landfall else e.kind,
                    e.tick,
                    e.text,
                    world.position,
                    nav.account_now(),
                )
            )

    world.log.subscribe(watch)
    begin(world, sf)
    run(world, save_tick)
    saved = (world.save(), world.log.digest(), world.vessels.to_dict(), _people(world))
    run(world, hours * 3600 - save_tick)
    world.log.unsubscribe(watch)
    return world, moments, saved


@pytest.fixture(scope="module")
def gate_5c_merchant():
    return the_scenario_whole(GATE_5C_MERCHANT, GATE_5C_MERCHANT_HOURS, GATE_5C_MERCHANT_SAVE_TICK)


@pytest.fixture(scope="module")
def gate_5c_cruise():
    return the_scenario_whole(GATE_5C_CRUISE, GATE_5C_CRUISE_HOURS, GATE_5C_CRUISE_SAVE_TICK)


def _by_order(log, name: str):
    return [e for e in log if e.actor == f"standing order '{name}'" and e.kind == "order.accepted"]


# Package 37d (2026-10-06), second pass: she comes through again. In pilot water the
# book takes the bearing alone, as before 37d (a stopgap: with a fix after it the account
# was the truer and she struck, the book's points being tuned to an account that lags her
# on the flood; the lead's correction in CHANGES-m5c-c.md, "The Goulet"), and two of the
# Goulet's points are moved for the flood's set (the book's comments; TuningNotes). She
# passes the Mingan 1.8 cables to the north and the shore under Petit Minou 1.6 cables
# off; the pilot of Brest boards later and nearer in, and she anchors in the road of
# Bertheaume and in the Bay in less water than before.
def test_the_merchant_passage_at_seed_7_has_its_own_constants(gate_5c_merchant):
    """Gate 5c's merchant passage (spec M5 §29): the schooner at Carrick Road, forty tons
    of tin bought at the quay and struck down from the lighter; out on the ebb, the
    Falmouth pilot aboard and put off into his cutter, the ship hove to for it; a sail
    sighted off the Lizard and not made out; the course across worked hourly from the
    account; the Iroise raised and passed (the cast at its mark, which reads her chart's
    words, is given once within a mile and a half of the mark: before package 37d she
    passed it two miles wide by account and it was not made; since the second pass she
    passes within that, heaves to and casts in thirty-nine fathoms, and the bottom matches
    her chart's words); the
    road of Bertheaume on the ebb by the lead, the pilot of Brest (come off from the
    outer road, the pilots' station, to the Iroise) aboard with the agent's letter ten
    miles out, the flood taken by daylight on the pilot's and the master's tide; the
    Goulet by the pass north of the Mingan and the Fillettes with the lead going and a
    bearing every five minutes; the Bay of Brest by the lead, the boat
    ashore, the tin sold; the account against the truth at each; the lines and the
    digest."""
    world, moments, _ = gate_5c_merchant
    log = world.log
    assert len(world.scenario.ships) == GATE_5C_SHIPS  # the dozen on the sea at the start
    # the cargo at Falmouth, by the lighter while the boat is at the quay
    bought = [e for e in log if e.kind == "market.bought"]
    assert [e.tick for e in bought] == [GATE_5C_MERCHANT_TIN_ABOARD_TICK]
    assert bought[0].text.startswith("40 tons of tin hoisted in and struck down")
    assert _by_order(log, "sail on the ebb")[0].tick == GATE_5C_MERCHANT_TIN_ABOARD_TICK
    under_way = [e for e in log if e.kind == "ship.under_way"]
    assert under_way[0].tick == GATE_5C_MERCHANT_UNDER_WAY_TICK
    # the Falmouth pilot aboard and off, the fore topsail in at his hail each time
    aboard = [e for e in log if e.kind == "port.pilot_aboard"]
    left = [e for e in log if e.kind == "port.pilot_left"]
    assert [e.tick for e in aboard] == GATE_5C_MERCHANT_PILOT_ABOARD_TICKS
    assert [e.tick for e in left] == GATE_5C_MERCHANT_PILOT_LEFT_TICKS
    assert "Mr Tregenza of Falmouth" in aboard[0].text and "of Brest" in aboard[1].text
    assert aboard[0].text.endswith("to pilot her out (American colours being no bar at Falmouth).")
    # package 37h: each taken at his hail by the book, and the pilot of Brest put off at the
    # anchor in the Bay and paid, once
    taken = [e for e in log if e.kind == "port.pilot_answered"]
    assert [e.data["answer"] for e in taken] == ["take", "take"]
    assert left[1].text.startswith("Mr Le Floch left her in the cutter, at the anchor in the Bay")
    assert "the pilotage, £4, paid" in left[1].text
    assert [e.kind for e in log if e.kind == "port.pilot_boat"] == ["port.pilot_boat"]
    assert any(
        e.data["danger"] == "black-rock-falmouth" for e in log if e.kind == "port.pilot_warns"
    )
    # package 37f: the fore-and-after casts, and is not said to at a timeout
    aweigh = [e for e in log if e.kind == "ship.aweigh"]
    paid_off = [e for e in log if e.kind == "evolution.step" and "paid off" in e.text]
    assert len(aweigh) == len(paid_off) == 2
    assert all(e.text.startswith("She has paid off; ") for e in paid_off)
    assert all(0 < b.tick - a.tick < 180 for a, b in zip(aweigh, paid_off, strict=True))
    assert len(_by_order(log, "the pilot boards")) >= 2
    # a sail off the Lizard, sighted and not made out: the book has no order for it
    sails = [e for e in log if e.kind == "lookout.sighting" and e.data.get("seen_as") == "sail"]
    off_lizard = [e for e in sails if 25200 <= e.tick <= 36000]
    assert off_lizard and off_lizard[0].tick == GATE_5C_MERCHANT_SAIL_OFF_LIZARD_TICK
    assert (
        off_lizard[0].text.startswith("Sail ho! A sail ") and "distance_m" not in off_lizard[0].data
    )
    assert not [e for e in log if e.kind == "lookout.made_out" and e.data.get("glass")]
    # the noons: the first's tick stands whatever the book does
    noons = [e for e in log if e.kind == "reckoning.noon"]
    assert [e.tick for e in noons] == GATE_5C_MERCHANT_NOON_TICKS
    assert noons[0].data["sight"]["instrument"] == "octant"
    # the Falmouth pilot put off: the ship hove to for his cutter and filled away after
    hove = [e for e in log if e.kind == "ship.hove_to"]
    filled = [e for e in log if e.kind == "ship.filled_away"]
    assert hove and filled and hove[0].tick < left[0].tick < filled[0].tick
    assert _by_order(log, "the pilot put off") and _by_order(log, "under way again")
    # the Iroise passed, the course for the points off Bertheaume shaped; the one cast at
    # its mark (see the docstring)
    assert _by_order(log, "the course for the Iroise") and _by_order(log, "past the Iroise")
    # package 45: by the wind under the helm's rules she comes to the Iroise's mark within
    # the book's distance again, brings to and casts there (37j to 37p: wide by account,
    # nothing cast; the test after this one)
    deep = [e for e in log if e.kind == "sounding" and e.data.get("deep")]
    assert [e.tick for e in deep] == [GATE_5C_MERCHANT_IROISE_CAST_TICK]
    assert _by_order(log, "bring to in the Iroise")
    assert len([e for e in hove if e.tick > 80000]) == 1
    # the road of Bertheaume on the ebb by the lead, the pilot aboard at the anchor; the
    # turn to the flood by daylight the same forenoon, and the Goulet on it
    anchored = [e for e in log if e.kind == "ship.anchored"]
    assert [
        e.tick for e in anchored
    ] == GATE_5C_MERCHANT_ANCHORED_TICKS  # Carrick Road, Bertheaume, Brest
    # package 37j: at the first cast under thirteen fathoms, the lead's (nine since package
    # 37p, eight and a half before)
    # package 45: eight fathoms and a half in the road of Bertheaume (nine at 37p)
    assert "in eight fathoms and a half" in anchored[1].text
    assert aboard[1].tick < anchored[1].tick
    # package 37e: standing in from the second point the course for the road is worked
    # again every five minutes, for the water she is then in
    assert len(_by_order(log, "the course for the road")) >= 4
    swung = [e for e in log if e.kind == "ship.swung" and e.tick > anchored[1].tick]
    assert swung and swung[0].data["flood"] is True and swung[0].tick == GATE_5C_MERCHANT_FLOOD_TICK
    flood = _by_order(log, "the flood")
    assert [e.tick for e in flood] == [GATE_5C_MERCHANT_FLOOD_TICK]
    assert flood[0].ship_time.day == 13 and flood[0].ship_time.hour == 11
    assert [e.tick for e in _by_order(log, "the mouth of the Goulet")] == [
        GATE_5C_MERCHANT_GOULET_TICK
    ]
    for name in (
        "under Petit Minou",
        "north of the Mingan",
        "north of the Fillettes",
        "under Portzic",
        "into the Bay",
    ):
        assert _by_order(log, name), name
    casts_in = [
        e for e in log if e.kind == "sounding" and anchored[1].tick < e.tick < anchored[2].tick
    ]
    assert len(casts_in) >= 12  # the lead going in pilot water
    bearings_in = [
        e for e in log if e.kind == "bearing.taken" and anchored[1].tick < e.tick < anchored[2].tick
    ]
    assert len(bearings_in) >= 12  # a bearing every five minutes in pilot water
    fixes_in = [
        e for e in log if e.kind == "reckoning.fix" and anchored[1].tick < e.tick < anchored[2].tick
    ]
    assert len(fixes_in) >= 12  # and the fix after it again (package 37e)
    assert not [e for e in log if e.kind in ("ship.aground", "anchor.dragging")]
    # the Bay of Brest: the boat ashore and the tin sold at the quay
    sold = [e for e in log if e.kind == "market.bargain" and e.data.get("verb") == "sell"]
    assert [e.tick for e in sold] == [GATE_5C_MERCHANT_TIN_SOLD_TICK]
    assert sold[0].text.startswith("Sold 40 tons of tin at Brest at ")
    assert _by_order(log, "the tin sold")[0].tick == sold[0].tick
    # the account against the truth
    by_kind = {}
    for kind, tick, _text, truth, account in moments:
        by_kind.setdefault(kind, []).append((tick, _miles(truth, account)))
    # the first noon: the hour hove to for the pilot ran on at the log's last read (nine
    # miles before 37e), set right by the Lizard's bearings within the glass; the second
    # in the mouth of the Goulet on bearings every five minutes. Package 37j: at the first
    # the sight is weighed and moves the account a cable (eight cables from the truth);
    # at the second the account, fixed a minute before, is within a cable of the truth
    # and the sight within the two doubts of it: "the account kept". At the fold-in the
    # octant's sight fell there five miles and a half north of an account fixed to three
    # cables, a hair over the two doubts together on Linux, and 37e's rule took it
    # outright (the account six miles out for a minute; weighed on Windows). Now the
    # better figure is believed, and such a sight is weighed and doubted on either side
    # of that line (held by its figures in `tests/test_reckoning.py`,
    # `test_the_merchant_passages_second_noon_...`); this track does not meet it.
    assert by_kind["reckoning.noon"][0][1] < 1.5
    assert by_kind["reckoning.noon"][1][1] < 0.5
    bearings_after = [m for m in by_kind["bearing.taken"] if m[0] > by_kind["reckoning.noon"][1][0]]
    assert bearings_after and bearings_after[0][1] < 1.0  # laid down again within five minutes
    at_anchor = by_kind["ship.anchored"]
    assert at_anchor[1][1] < 1.0 and at_anchor[2][1] < 1.0  # Bertheaume and Brest, by bearings
    assert len(log) == GATE_5C_MERCHANT_LINES and log.digest()[:16] == GATE_5C_MERCHANT_DIGEST


# Package 37j to 37p: an expected failure (the course for the Passage de l'Iroise shaped
# nineteen miles off was not worked again once Ushant was within ten miles, and she passed
# the mark more than a mile and a half off by account; 'bring to in the Iroise' never fired).
# Package 45: she comes to the mark by the wind under the helm's rules and casts there at
# 90318 (90241 before 37j); the expectation of failure lifted, the test as written.
def test_the_merchant_passage_casts_the_deep_sea_lead_at_the_iroises_mark(gate_5c_merchant):
    """The beat of the merchant passage as pinned until package 37j: brought to once
    within a mile and a half of the Passage de l'Iroise and the deep-sea lead hove, which
    reads the Iroise in her chart's words (thirty-eight fathoms at 90241)."""
    world, _moments, _saved = gate_5c_merchant
    deep = [e for e in world.log if e.kind == "sounding" and e.data.get("deep")]
    assert [e.tick for e in deep] == [GATE_5C_MERCHANT_IROISE_CAST_TICK]


def test_the_naval_cruise_at_seed_7_has_its_own_constants(gate_5c_cruise):
    """Gate 5c's naval cruise (spec M5 §29): the frigate in the Sound, the yard's thirty
    days of provisions, under way on the starboard tack, the Plymouth pilot aboard and
    off, the course for the station, the chronometer's time sights; the port admiral's
    cutter with the letter sighted, within hail, the letter read; the station kept by the
    wind, wearing every second hour; the stranger put on the sea by the scenario's order,
    sighted ahead, made out, chased by the bearing's drift (she weathers the frigate and
    passes, the frigate wears and runs her down in three hours) and spoken, a brig-sloop
    of war under no colours; the lines and the digest."""
    world, moments, (_data, _digest, vessels_at_save, _people_at_save) = gate_5c_cruise
    log = world.log
    assert len(world.scenario.ships) == GATE_5C_SHIPS - 1  # eleven, and the stranger by order
    yard = [e for e in log if e.kind == "yard.done"]
    assert [e.tick for e in yard] == [GATE_5C_CRUISE_YARD_TICK]
    assert yard[0].text.startswith("Provisions for 30 days came off")
    under_way = [e for e in log if e.kind == "ship.under_way"]
    assert (
        under_way[0].tick == GATE_5C_CRUISE_UNDER_WAY_TICK and "starboard tack" in under_way[0].text
    )
    aboard = [e for e in log if e.kind == "port.pilot_aboard"]
    left = [e for e in log if e.kind == "port.pilot_left"]
    assert [e.tick for e in aboard] == [GATE_5C_CRUISE_PILOT_ABOARD_TICK]
    assert [e.tick for e in left] == [GATE_5C_CRUISE_PILOT_LEFT_TICK]
    sights = [e for e in log if e.kind == "reckoning.time_sight"]
    assert len(sights) >= 4 and "longitude by chronometer" in sights[0].text
    # the message by the cutter: the world's order at its tick, the cutter sighted as a
    # sail, within hail, the letter aboard and read, each a line in order
    orders = [e for e in log if e.kind == "world.order"]
    assert [(e.tick, e.data["source"]) for e in orders] == GATE_5C_CRUISE_WORLD_ORDERS
    cutter_hail = [e for e in log if e.kind == "sail.within_hail" and "letter" in e.text]
    assert [e.tick for e in cutter_hail] == [GATE_5C_CRUISE_CUTTER_HAIL_TICK]
    read = [e for e in log if e.kind == "message.received"]
    assert [e.tick for e in read] == [GATE_5C_CRUISE_LETTER_READ_TICK]
    assert "Rejoin the squadron off the Black Rocks" in read[0].text
    cutter_seen = [
        e
        for e in log
        if e.kind == "lookout.sighting" and e.data.get("seen_as") == "sail" and "cutter" in e.text
    ]
    assert cutter_seen and cutter_seen[0].tick < cutter_hail[0].tick < read[0].tick
    # the station kept by the wind: wore ship watch by watch, no sail in sight
    wore = [e for e in log if e.kind == "ship.wore"]
    assert len(wore) >= GATE_5C_CRUISE_WEARS_AT_LEAST
    # the stranger: on the sea by the scenario's order, sighted at the horizon, made out
    # by the glass and the tops, chased by the bearing's drift, spoken under no colours
    by_name = {v["name"]: v for v in vessels_at_save}  # at noon on the 13th (45c; 08:00 before)
    # package 45c: spoken at 107738, five minutes before the save at noon
    assert by_name["Palinure"]["spoken"] is True
    assert "Palinure" in by_name and by_name["Palinure"]["nation"] == "france"
    sighted = [
        e
        for e in log
        if e.kind == "lookout.sighting"
        and e.data.get("seen_as") == "sail"
        and e.tick >= orders[-1].tick
    ]
    assert sighted and sighted[0].tick == GATE_5C_CRUISE_STRANGER_SIGHTED_TICK
    chase = [
        e
        for e in log
        if e.kind == "helm.set" and e.text.startswith("Gave chase to") and e.tick >= sighted[0].tick
    ]  # the cutter with the letter was chased off the Sound too, a stranger until her colours
    assert chase and chase[0].tick == GATE_5C_CRUISE_CHASE_TICK >= sighted[0].tick
    assert any("the course led" in e.text for e in chase)
    # package 37e: the chase lost to sight, and the course shaped for the station at it
    # (whether she is spoken is the test after this one)
    lost = [e for e in log if e.kind == "lookout.sail_lost" and e.tick > sighted[0].tick]
    assert lost and lost[0].tick == GATE_5C_CRUISE_CHASE_LOST_TICK
    assert [e.tick for e in _by_order(log, "the chase lost") if e.tick > sighted[0].tick] == [
        GATE_5C_CRUISE_CHASE_LOST_TICK
    ]
    assert not [e for e in log if e.kind in ("ship.aground", "anchor.dragging")]
    noons = [e for e in log if e.kind == "reckoning.noon"]
    assert [e.tick for e in noons] == GATE_5C_CRUISE_NOON_TICKS
    by_kind = {}
    for kind, tick, _text, truth, account in moments:
        by_kind.setdefault(kind, []).append((tick, _miles(truth, account)))
    assert by_kind["reckoning.noon"][1][1] < 10.0  # by account since the chase, the sights unworked
    assert len(log) == GATE_5C_CRUISE_LINES and log.digest()[:16] == GATE_5C_CRUISE_DIGEST


def test_the_naval_cruise_speaks_the_stranger(gate_5c_cruise):
    """Gate 5c's naval cruise, the beat as pinned until package 37e and brought back at
    the fold-in of m5c-c: the stranger chased by the bearing's drift and spoken, a
    brig-sloop of war under no colours (within hail at 08:08 on the 13th, 94091; 95189
    after 37d), the chase given up at her hail. Between 37e and the fold-in she was
    chased and lost: the scenario put her where the frigate had been at seven, and the
    chase 175 degrees round by the helm alone laid every square sail aback. Package 45
    put her astern of the frigate still chasing the admiral's cutter, never spoken; 45c
    puts her on the frigate's bow at half past ten, spoken at 11:55 (107738)."""
    world, _moments, _saved = gate_5c_cruise
    log = world.log
    spoken = [e for e in log if e.kind == "sail.within_hail" and "brig-sloop" in e.text]
    assert spoken and spoken[0].text.endswith("a stranger, her colours not made out.")
    assert spoken[0].tick == GATE_5C_CRUISE_SPOKEN_TICK
    chase_up = [e for e in _by_order(log, "the chase up") if e.tick >= spoken[0].tick]
    assert chase_up and chase_up[0].tick == spoken[0].tick


def test_truth_72_the_two_scenarios_replay_to_the_same_digest(gate_5c_merchant, gate_5c_cruise):
    """Spec M5 §28, truth 72: "The merchant passage and the naval cruise replay to the
    same digest from their scenario files, ships, ports, people and weather included."
    Each saved at a tick of its run and replayed from the save (the seed, the scenario
    file whole, the inputs; the scenario's own world orders applied again at their ticks
    from the file, the harness's from the inputs): the digest at that tick the same, the
    ships where they were, the people and the port's state the same."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    for _world, _moments, (data, digest, vessels, people) in (gate_5c_merchant, gate_5c_cruise):
        assert data["scenario"]["ships"] and data["scenario"]["world_orders"]
        copy = replay_mod.replay(data, ship_factory)
        assert copy.clock.tick == data["end_tick"]
        assert copy.log.digest() == digest
        assert copy.vessels.to_dict() == vessels  # every ship where she was, far or near
        assert _people(copy) == people
        assert [o["tick"] for o in copy.save()["world_orders"]] == [
            o["tick"] for o in data["world_orders"]
        ]


def test_the_pace_at_the_merchant_passages_start_with_the_dozen_ships_holds_truth_51s_floor():
    """Spec M5 §30 and package 36: the merchant passage's start, the schooner at anchor in
    Carrick Road with the dozen ships on the sea at far detail (each moved once a game
    minute by her polar, the lookout's look over them, the strangers in every sample),
    the best of three thousands at least BUILD_MACHINE_FLOOR. Measured on the build
    machine: docs/dev/TuningNotes.md, package 36."""
    import time

    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(GATE_5C_MERCHANT)
    world = make_scenario_world(sf)
    begin(world, sf)
    assert len(world.vessels.active()) >= GATE_5C_SHIPS
    world.run(600)  # the anchor down, the boat away
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"


# ---------------------------------------------------------------------------
# Milestone 6a: the ship's company, the rules-based captain, the captain's station
# (package 40; spec M6 §2 to §4, §7 and §8, truths 77 to 79 and 81; the officer's own
# reckoning and truth 80 are 40b's)
# ---------------------------------------------------------------------------

# The schooner trading on an intent alone (data/scenarios/merchant-intent.yaml): the
# merchant passage's ship, start, weather and world with no book, `intent: trade tin from
# Falmouth to Brest`, sailed by the rules-based captain and nobody else. Measured on the
# package's branch, 2026-10-09 (docs/dev/TuningNotes.md, package 40).
GATE_6A_INTENT = "data/scenarios/merchant-intent.yaml"
GATE_6A_INTENT_HOURS = 36
GATE_6A_INTENT_SAVE_TICK = 12 * 3600  # 17:00 on the 12th, the Channel crossing
GATE_6A_INTENT_FIRST_STATE_TICK = 300  # in port, at his first judgement (JUDGE_FIRST_S)
GATE_6A_INTENT_BOUGHT_TICK = 300  # 47 tons of tin bought at £120, the boat sent for them
GATE_6A_INTENT_TONS = 47  # the purse's £6,000 less a twentieth, at the quay's price
GATE_6A_INTENT_TIN_ABOARD_TICK = 15765  # hoisted in and struck down
GATE_6A_INTENT_UNDER_WAY_ORDER_TICK = 15780  # "getting under way ... (the tide serves)"
GATE_6A_INTENT_AWEIGH_TICK = 17037
# package 43b: the beating rule's verdict held ten minutes (`beating_dwell_minutes`): she
# beats from 11:29 (11:19 before) and lays the course again at 12:46 (12:38), comes to the
# road of Bertheaume eight minutes later than before, and the flood no longer serves for the
# Goulet: the at-anchor book's "the tide to go in" anchors her in the road at 09:58 on the
# 13th, in port from it (package 45's rule: the road within Brest's reach), and her business
# is done from the road by the boat; the pilot of Brest stays aboard to take her in, and the
# Goulet is not sailed in the 36 hours (before: conned through it by the pilot from 104220
# and anchored in the Bay of Brest at 111370)
# package 68 (item 1, riding means riding): she ranges ahead on her cable while she comes
# to in Carrick Road, not yet brought up, and the account runs the while (it did not, the
# anchor being down); the master's tide is said at 17100 when she has weighed, the fixes
# off St Anthony and the Manacles read differently, the allowance she steers by moves, and
# from 21756 the passage is another: she lays the course again at 28080, takes Le Floch
# at 101820, comes to the Iroise with the flood serving, is conned through the Goulet and
# lets go in the Bay of Brest at 110872 in thirteen fathoms and a half (as at 45c), drags
# from 110962 and holds again having come home twenty fathoms, brought up at 111710; she
# sells at 119400. Every figure before it is package 43b's and 56's, kept beside the new;
# the old rule restored gives the old figures (docs/dev/TuningNotes.md, package 68).
# package 58b (items 1, 2 and 6, by bisection: the tree with the three turned off gives every
# old figure, and items 3, 4 and 5 turned off alone change nothing): the leg is laid again
# for the stream from 29820 and at the turns of the master's tide, and she is brought to
# for the deep-sea lead once a watch inshore (30720, 64860, 83340, 97740), so that she comes
# to the Iroise later; Le Floch boards at 108480 off Bertheaume and is given the conn at
# 109980 with the flood running two knots into the Goulet and the wind at NW, and he judges
# that she will not lie up for its mouth and brings her up in the road in ten fathoms to
# wait for the flood to slacken (said); the captain is in port from the road (package 45's
# rule, as from 43b to 56) and sends the boat for the prices, so that the pilot's weigh at
# 113940 is refused while the boat is away, asked again each half hour, and she is in the
# road at the end, the tin unsold. With item 6 turned off the old pilot cons her on and she
# strikes the Mingan at 113341 (docs/dev/TuningNotes.md, package 58b). The old figures
# beside each.
GATE_6A_INTENT_STATES = [  # (tick, state): the books loaded and unloaded by name
    (300, "in port"),
    (17040, "on passage"),
    (23340, "beating"),  # the course for the Lizard's offing not laid (22740 at 45c)
    (28020, "on passage"),  # 28080 at 68 (27960 at 56, 27480 at 45c, 27720 at 37p)
    # package 43b to 56: (103980, "at anchor") in the road of Bertheaume for the tide and
    # (104340, "in port") from the road; package 68: in the Bay at 110880 (111420 at 45c)
    (110340, "in port"),  # package 58b: in the road of Bertheaume, the pilot waiting
]
# Tregenza out; Le Floch in (101580 at 56, 101100 at 45c)
GATE_6A_INTENT_PILOT_ABOARD_TICKS = [17700, 108480]  # 101820 at 68
# package 45c: the pilot of Brest given the conn at 104220 cons her by his track from his
# station, Bertheaume, leg by leg through the Goulet (two hours, the book's bearings every
# five minutes the while: two hundred and forty lines more), the berth said at 111120 on the
# Bay's road moved onto its twelve fathoms; his cutter comes for him at 120660
# package 68: Le Floch put off at the anchor in the Bay ([19920] at 43b to 56, Le Floch
# aboard; [19920, 121020] at 45c)
# package 58b: Le Floch aboard at the end, waiting to take her in ([19920, 114900] at 68)
GATE_6A_INTENT_PILOT_LEFT_TICKS = [19920]
GATE_6A_INTENT_NOON_TICKS = [25200, 111660]
# Carrick Road; the Bay of Brest (Bertheaume 104295 at 43b to 56; the Bay 111370 at 45c)
# package 58b: the road of Bertheaume, brought up by the pilot to wait ([57, 110872] at 68)
GATE_6A_INTENT_ANCHORED_TICKS = [57, 110305]
# package 58b (111710 at 68, 105260 at 43b, 112302 at 45c)
GATE_6A_INTENT_BROUGHT_UP_TICK = 111238
# the boat for the prices (111780 at 68, 105360 at 43b)
GATE_6A_INTENT_BOAT_FOR_PRICES_TICK = 111300
# package 58b: not sold in the 36 hours (119400 at 68, 124320 at 43b, 119820 at 45c)
GATE_6A_INTENT_SOLD_TICK = None
GATE_6A_INTENT_LINES = 2078  # package 58b (2160 at 68, riding; 1698 at 56, 1684 at 43b)
# measured on the merged tree: the judgement a sentence of its own after a shaped course's
# line, as the cruise (4b5a6f997d80eb52 on the package's branch, every tick the same)
# decision 45, the pilot's news: 71b1cddbd0e4ec9f before; package 37p (09afd9c2697c7c33 before)
# package 56, the glass: 90061f779b7db484 (93981cc47f5524e6 at 57)
# the lead at the merge of 58a and 58b (2026-10-23): 58a's figure was "6292d5af25a6b326"
# package 68, riding: 8eead2f4521f2a61 (90061f779b7db484 before)
# the merged tree of 58a and 58b (2026-10-23): 58b alone gave b498761052da0862; the digest reads
# severity, and 58a's recurring lines are routine in this passage too
GATE_6A_INTENT_DIGEST = "585c52675f10e590"  # package 58b


@pytest.fixture(scope="module")
def gate_6a_intent():
    return the_scenario_whole(GATE_6A_INTENT, GATE_6A_INTENT_HOURS, GATE_6A_INTENT_SAVE_TICK)


def _by_rule(log):
    return [e for e in log if str(e.actor).startswith("captain's rule ")]


def test_truth_77_the_two_scenarios_sail_under_their_books_with_the_captain_named_and_aside(
    gate_5c_merchant, gate_5c_cruise
):
    """Spec M6 §8, truth 77: "The merchant passage and the naval cruise sail under the
    rules-based captain named, with no model seated, to the same digests as before (the
    floor is the game as it was)." Each has its captain named (the master of the
    schooner, the captain of the frigate, by the wardroom file's binding), with no intent,
    so that he stands aside and the book sails her: not one judgement under his actor,
    and the digests package 37m pinned (the constants' tests above)."""
    for (world, _moments, _saved), digest in (
        (gate_5c_merchant, GATE_5C_MERCHANT_DIGEST),
        (gate_5c_cruise, GATE_5C_CRUISE_DIGEST),
    ):
        cap = world.captain
        assert cap is not None and cap.name and cap.intent is None
        assert not cap.active and not cap.commands and cap.books
        assert cap.name == world.people.holder("captain").name
        assert not _by_rule(world.log)
        assert "captain" not in world.agents
        assert world.log.digest()[:16] == digest


def test_the_schooner_on_an_intent_alone_at_seed_7_has_its_own_constants(gate_6a_intent):
    """The new scenario of package 40 (spec M6 §4, the floor): the schooner with an intent
    and no book, sailed by the rules-based captain. He buys the tin at the quay's price
    for what the purse allows, sails on the ebb when the boat is alongside, takes the
    pilot out, beats off the Lizard when the westerly will not lay the course and lays
    it again, crosses on the soundings' track, takes the pilot of Brest in the Iroise,
    is conned through the Goulet and anchors in the Bay of Brest in thirteen fathoms and
    a half (package 68; in the road of Bertheaume for the tide in eight and a half from
    43b to 56, in the Bay in thirteen and a half before), sends the boat for the prices
    once brought up, and sells at £270. Every doing is an order under his rule's actor,
    not journaled; the states are books loaded and unloaded by name."""
    world, _moments, _saved = gate_6a_intent
    log = world.log
    cap = world.captain
    assert cap.intent is not None and cap.intent.words == "trade tin from Falmouth to Brest"
    assert cap.active and cap.commands and cap.state == "in port"
    states = [(e.tick, e.data["state"]) for e in log if e.kind == "captain.state"]
    assert states == GATE_6A_INTENT_STATES
    bargains = [e for e in log if e.kind == "market.bargain"]
    # package 58b: the tin unsold in the 36 hours, the pilot waiting in the road
    assert [e.tick for e in bargains] == [GATE_6A_INTENT_BOUGHT_TICK]
    assert GATE_6A_INTENT_SOLD_TICK is None
    assert f"Bought {GATE_6A_INTENT_TONS} tons of tin at Falmouth at £120" in bargains[0].text
    assert [e.tick for e in log if e.kind == "market.bought"] == [GATE_6A_INTENT_TIN_ABOARD_TICK]
    under_way = [e for e in _by_rule(log) if "getting under way" in e.text]
    assert under_way and under_way[0].tick == GATE_6A_INTENT_UNDER_WAY_ORDER_TICK
    assert "the tide serves" in under_way[0].text
    assert [e.tick for e in log if e.kind == "ship.aweigh"] == [GATE_6A_INTENT_AWEIGH_TICK]
    aboard = [e.tick for e in log if e.kind == "port.pilot_aboard"]
    assert aboard == GATE_6A_INTENT_PILOT_ABOARD_TICKS
    assert [e.tick for e in log if e.kind == "port.pilot_left"] == GATE_6A_INTENT_PILOT_LEFT_TICKS
    assert [e.tick for e in log if e.kind == "reckoning.noon"] == GATE_6A_INTENT_NOON_TICKS
    assert [e.tick for e in log if e.kind == "ship.anchored"] == GATE_6A_INTENT_ANCHORED_TICKS
    # package 37p: in 13 fathoms (twelve and a half before)
    # package 45: twelve fathoms where the pilot conned her to (13 at 37p)
    # package 45c: the Bay's road on its twelve fathoms, let go in thirteen and a half
    # package 43b: in the road of Bertheaume for the tide, in eight and a half
    # package 68: in the Bay again, let go in thirteen and a half (the figure as the
    # pilot's berth writes it)
    # package 58b: in the road of Bertheaume, brought up by the pilot to wait, in ten
    assert "in ten fathoms" in [e for e in log if e.kind == "ship.anchored"][1].text
    waits = [e for e in log if e.kind == "port.pilot_waits"]
    assert [e.tick for e in waits] == [109980]
    assert "wait for the flood to slacken" in waits[0].text
    brought = [e.tick for e in log if e.kind == "ship.brought_up"]
    assert brought[-1] == GATE_6A_INTENT_BROUGHT_UP_TICK
    prices = [e for e in _by_rule(log) if "for the prices" in e.text]
    assert prices and prices[0].tick == GATE_6A_INTENT_BOAT_FOR_PRICES_TICK
    assert not [e for e in log if e.kind == "ship.aground"]
    # package 68: the best bower let go in the Bay drags from 110962 and holds again,
    # having come home twenty fathoms, before she is brought up (no dragging before 68)
    # package 58b: in the road of Bertheaume she does not drag
    assert not [e.tick for e in log if e.kind == "anchor.dragging"]
    # every doing of his is an order under his actor (its line and its results carry it)
    # and never journaled
    assert any(e.kind == "order.accepted" for e in _by_rule(log))
    assert {actor for _, actor, _ in world.journal} <= {"captain"}
    assert len(log) == GATE_6A_INTENT_LINES and log.digest()[:16] == GATE_6A_INTENT_DIGEST


def test_the_schooner_on_an_intent_alone_replays_to_the_same_digest(gate_6a_intent):
    """The captain's judgements are a function of the seed and the journal: the save at
    its tick replays to the same digest, the captain in the same state."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    _world, _moments, (data, digest, vessels, people) = gate_6a_intent
    assert data["scenario"]["intent"] == "trade tin from Falmouth to Brest"
    copy = replay_mod.replay(data, ship_factory)
    assert copy.clock.tick == data["end_tick"]
    assert copy.log.digest() == digest
    assert copy.vessels.to_dict() == vessels
    assert _people(copy) == people
    assert copy.captain.state == "on passage"


def test_truth_81_no_reading_at_the_captains_station_gives_the_truth_by_any_road():
    """Spec M6 §8, truth 81: "No reading at the captain's station gives the truth by any
    road (37j's proof extended to the new tools)." Two ships of one seed in open water,
    four miles apart in truth and one by account, each with the fake captain seated: the
    readings tool at the captain's station says the same of both, the station's reading
    included, and the station has no tool the watcher's has not."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents import tools as tools_mod
    from freesail.agents.agent import CAPTAIN, captain
    from freesail.agents.fake import captain_of_the_ship
    from freesail.world.geo import Position

    worlds = []
    for lat, lon in ((49.0, -6.5), (49.05, -6.42)):
        sc = Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=270.0,
            wind_speed_kn=14.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": lat, "lon_deg": lon},
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
        )
        world = make_world(7, "data/ships/topsail-schooner.yaml", sc)
        world.navigation.reckoning.set_position(Position(49.02, -6.47), 0, sigma_nm=1.0)
        h = Harness(
            world,
            captain(SamplingPolicy.in_lockstep(600), 3600, world=world),
            captain_of_the_ship(),
            save=lambda w, why: None,
        )
        h.model_name, h.door = "the fake", "runner"
        h.start()
        world.run(600)
        worlds.append(world)
    a, b = worlds
    assert _miles(a.navigation.account_now(), b.navigation.account_now()) < 0.001
    assert _miles(a.position, b.position) > 3.0
    ra, rb = tools_mod.readings(a, CAPTAIN), tools_mod.readings(b, CAPTAIN)
    assert ra == rb
    assert ra["captain"] == rb["captain"] and "the fake" in ra["captain"]
    assert set(a.agents[CAPTAIN].tool_names) <= set(tools_mod.TOOLS)


# The merchant passage under the fake captain (truths 78 and 79): the passage whole under
# its book with the fake at the captain's station (freesail/agents/fake.py,
# `captain_of_the_ship`), sampled every ten minutes in lockstep with an hour's patience,
# six harmless direct orders one a sample and then silence. Measured on the package's
# branch, 2026-10-09 (docs/dev/TuningNotes.md, package 40).
GATE_6A_FAKE_CAPTAIN_ORDERS = [  # three readings asked, a question, `pipe down`, the port
    "what is the time",
    "the reckoning",
    "pipe down",
    "the tide",
    "the people",
    "the port",
]
GATE_6A_FAKE_CAPTAIN_ORDER_TICKS = [57, 323, 396, 600, 1200, 1800]  # one a sample, under his mark
GATE_6A_FAKE_CAPTAIN_DECK_TO_BOOK_TICK = 5400  # an hour after his last order: the deck to his book
GATE_6A_FAKE_CAPTAIN_PAUSED_TICK = 9000  # twice the patience: paused, the owner asked
GATE_6A_FAKE_CAPTAIN_LINES = GATE_5C_MERCHANT_LINES + 13  # his 7, the harness's 6
# the merge of 37p with 41 and 42 (2026-10-10): his "I have the command." to an empty
# quarterdeck carries its place and its hearers (none) in its data, as every say does now
# (the owner's ruling of 2026-10-10); aa42746f61de91d1 at 37p, a2cd045b9bcc93f8 before it
# decision 45, the pilot's news: b00ac08c3f63e84c before
# package 56, the glass: f996530d5a041abc (0e089f1279e03928 at 57); package 68, riding:
# the merchant passage's one line more and its account at 300 (3111 lines before)
# the lead at the merge of 58a and 58b (2026-10-23): 58a's figure was "073a636b6d76cc16"
# package 58b: the merchant passage's stern line (3112 lines before; item 3's by bisection)
# the merged tree of 58a and 58b (2026-10-23): 58b alone gave 0949c109116fc4a1; the digest reads
# severity, and 58a's recurring lines are routine in this passage too
GATE_6A_FAKE_CAPTAIN_DIGEST = "1c9a985bfd5dce0f"  # package 58b (1f8de8b49c7d5b5a at 68)


def the_passage_under_the_fake_captain(path: str, hours: int, orders: list[str]):
    """A scenario of gate 5c run whole under its book with the fake captain seated at the
    start: (world, harness)."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import captain
    from freesail.agents.fake import captain_of_the_ship
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(path)
    world = make_scenario_world(sf)
    begin(world, sf)
    st = captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), 3600, world=world)
    h = Harness(world, st, captain_of_the_ship(orders, then_silent=True), save=lambda w, why: None)
    h.model_name, h.door = "the fake", "runner"
    h.start()
    run(world, hours * 3600)
    return world, h


@pytest.fixture(scope="module")
def gate_6a_fake_captain():
    return the_passage_under_the_fake_captain(
        GATE_5C_MERCHANT, GATE_5C_MERCHANT_HOURS, GATE_6A_FAKE_CAPTAIN_ORDERS
    )


def _not_the_stations(log):
    """Every line that is neither the captain's station's nor the harness's about it."""
    return [
        (e.kind, e.text)
        for e in log
        if not e.kind.startswith("agent.") and e.actor != "the captain"
    ]


def test_truth_78_the_fake_captain_commands_the_merchant_passage_by_its_book_and_six_orders(
    gate_6a_fake_captain, gate_5c_merchant
):
    """Spec M6 §8, truth 78: "A fake captain through the harness commands the merchant
    passage from Falmouth to Brest by its book and six direct orders, and the log is the
    same book's log with his six orders in it under his mark." Every line of the passage
    with nobody seated is in this log, in order, and beside them his six orders under the
    station's actor (seven lines: `pipe down` answers with the watch's line) and the
    harness's six about the station; the tin sold at Brest at the same tick."""
    world, h = gate_6a_fake_captain
    base, _moments, _saved = gate_5c_merchant
    log = world.log
    his = [e for e in log if e.actor == "the captain" and not e.kind.startswith("agent.")]
    assert [e.tick for e in his if e.kind != "crew.order"] == GATE_6A_FAKE_CAPTAIN_ORDER_TICKS
    assert [e.kind for e in his].count("order.accepted") == 1  # pipe down
    assert "By the captain: piping down." in [e.text for e in his]
    assert _not_the_stations(log) == [(e.kind, e.text) for e in base.log]
    assert [e.tick for e in log if e.kind == "ship.anchored"] == GATE_5C_MERCHANT_ANCHORED_TICKS
    sold = [e for e in log if e.kind == "market.bargain" and e.text.startswith("Sold")]
    assert (
        sold
        and sold[0].tick
        == [e for e in base.log if e.kind == "market.bargain" and e.text.startswith("Sold")][0].tick
    )
    assert {actor for _, actor, _ in world.journal} <= {"captain"}  # his are the transcript's
    assert len(log) == GATE_6A_FAKE_CAPTAIN_LINES
    assert log.digest()[:16] == GATE_6A_FAKE_CAPTAIN_DIGEST


def test_truth_79_a_silent_captains_door_passes_the_deck_to_the_book_and_the_book_brings_her_in(
    gate_6a_fake_captain,
):
    """Spec M6 §8, truth 79: "A silent captain's door passes the deck to his book within
    the station's patience, the log says so, and the book brings her to the anchor." An
    hour after his last order the deck passes to his book, urgently; at twice the
    patience the station is paused and the owner asked, the deck his book's; the book
    brings her to the road of Bertheaume and the Bay of Brest at the passage's ticks and
    sells the tin; the station is paused, not released, at the end."""
    world, h = gate_6a_fake_captain
    log = world.log
    deck = [e for e in log if e.kind == "agent.deck"]
    assert deck[0].tick == 0 and deck[0].text.startswith("The captain's station has the deck")
    lost = [e for e in deck if e.data.get("deck") == "lost"]
    assert [e.tick for e in lost] == [GATE_6A_FAKE_CAPTAIN_DECK_TO_BOOK_TICK]
    assert lost[0].severity is Severity.URGENT
    assert "the deck passes to his book; the standing orders hold the deck" in lost[0].text
    paused = [e for e in log if e.kind == "agent.paused"]
    assert [e.tick for e in paused] == [GATE_6A_FAKE_CAPTAIN_PAUSED_TICK]
    assert "the deck is his book's" in paused[0].text
    assert h.agent.paused and not h.agent.deck and not h.agent.released
    assert not world.captain.active  # a book scenario: the rules stand aside, the book holds
    anchored = [e for e in log if e.kind == "ship.anchored"]
    assert [e.tick for e in anchored] == GATE_5C_MERCHANT_ANCHORED_TICKS
    assert all(e.tick > GATE_6A_FAKE_CAPTAIN_PAUSED_TICK for e in anchored[1:])
    reading = world.readings["captain"]
    assert reading["held"] and not reading["deck"]
    assert "the deck lent to his book while the station is paused" in reading["words"]


# Truth 80 (spec M6 §5, §8; package 40b): an officer's own reckoning, worked from the
# master's slate by the slate's own words, as a model at the station reads them (the
# working is the fake master's since package 41, `fake.work_the_slate`).
def _the_officers_own_noon(with_the_tide: bool):
    """The frigate standing ESE off the Lizard across the stream, the fake officer seated
    off watch at twenty to twelve: he asks for the slate, works it from its words, and
    gives his own reckoning; then noon."""
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer
    from freesail.agents.fake import work_the_slate

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 11, 10),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=112.0,
        ship_speed_kn=6.0,
        position={"lat_deg": 49.75, "lon_deg": -5.45},
        region="channel-west",
    )
    world = make_world(7, "data/ships/frigate-36.yaml", sc)
    world.submit("set plain sail")
    world.submit("steer ESE")
    world.run(600)
    world.submit("trim sails")
    world.run(1800)

    def work_it(last, turns):
        words = str(last["tool_results"][0]["result"])
        lat, lon = work_the_slate(words, with_the_tide)
        return reply("", call("submit_order", text=f"my reckoning is {lat:.4f} N {-lon:.4f} W"))

    script = [reply("", call("submit_order", text="work my reckoning")), work_it, "Worked.", ""]
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(3600), world=world),
        Fake(script),
        save=lambda w, why: None,
    )
    h.start()
    run(world, 1800)
    return world, h


def test_truth_80_an_officers_own_reckoning_from_the_slate_agrees_with_the_masters_at_noon():
    """Spec M6 §8, truth 80: "An officer's reckoning worked from the slate agrees with the
    master's within the master's doubt when both are right, and the log shows both at
    noon." The officer works the slate's words (the departure, each board's course and
    distance and the tide allowed) by the traverse and gives his own reckoning off
    watch: at noon the noon's line is followed by his, which lies within one of the
    master's doubts of the master's account before the sight. Worked without the tide
    the slate gave him, his own lies further off by about what the tide set her."""
    world, _h = _the_officers_own_noon(with_the_tide=True)
    log = world.log.all()
    noon = [i for i, e in enumerate(log) if e.kind == "reckoning.noon"]
    assert len(noon) == 1
    own = log[noon[0] + 1]
    assert own.kind == "reckoning.own_noon" and own.severity is Severity.NOTABLE
    assert own.text.startswith("The officer of the watch's own reckoning (")
    assert "worked at 11:50 and run on by the log-board: " in own.text
    assert own.data["within"] is True and own.data["sigmas"] <= 1.0
    assert own.data["from_master_nm"] < 0.5
    careless, _ = _the_officers_own_noon(with_the_tide=False)
    other = [e for e in careless.log if e.kind == "reckoning.own_noon"][0]
    assert other.data["from_master_nm"] > own.data["from_master_nm"] + 0.5


# ---------------------------------------------------------------------------
# Milestone 6b: the wardroom (package 41; spec M6 §11, §12, §16): truths 82 to 85 on the
# cutter's free passage with fakes. No recorded passage's pin moves: none has a station
# seated, and the pace rule changes no tick of the world (the clock's compression is the
# driver's, not the simulation's).
# ---------------------------------------------------------------------------

CUTTER = "data/ships/cutter.yaml"
WARDROOM_EVERY = 600  # the stations sampled every ten minutes in lockstep


def _free_cutter() -> World:
    return make_world(
        7,
        CUTTER,
        Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0),
    )


def _the_cutters_free_passage():
    """The cutter at seed 7 in a steady northerly, standing south under plain sail, with
    the fake captain and the fake officer seated through two in-process doors (a harness
    each) and the player at the master's station: the captain gives the officer the deck
    and his general authority, tells him and asks the master for a course; the officer
    trims the sheets and heaves the log once each when he has the deck (a cutter carries
    no royals for the stock fake officer to keep)."""
    from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call
    from freesail.agents.agent import CAPTAIN, OFFICER, captain, officer
    from freesail.agents.fake import captain_of_the_ship, readings_so_far
    from freesail.agents.seat import seat_player

    world = _free_cutter()
    world.submit("set plain sail")
    world.run(600)
    policy = SamplingPolicy.in_lockstep(WARDROOM_EVERY, "notable", "urgent")
    orders = ["trim sails", "heave the log"]

    def keep_the_cutter(last, turns):
        if "tool_results" in last:
            return Reply()
        held = str(readings_so_far(turns).get("officer_of_the_watch") or "")
        if orders and "has the deck since" in held:
            return Reply(calls=(call("submit_order", text=orders.pop(0)),))
        # a stand-by, not silence: a deck is not kept in silence (the officer's brief)
        return Reply(calls=(call("stand_by", until="eight bells"),))

    oh = Harness(world, officer(policy, world=world), Fake([keep_the_cutter], loop=True), save=None)
    oh.model_name, oh.door = "the fake officer", "runner"
    oh.start()
    ch = Harness(
        world,
        captain(policy, world=world),
        captain_of_the_ship(
            [
                "you have the deck",
                "you may work the ship",
                "tell the officer keep her full and by",
                "ask the master for a course",
            ]
        ),
        save=lambda w, r: None,
    )
    ch.model_name, ch.door = "the fake captain", "mcp"
    ch.start()
    seat = seat_player(world, "master", door="console")
    world.run(4 * WARDROOM_EVERY + 1)
    seat.route("answer south by east, sir, and nothing to leeward")
    world.run(2 * 3600)
    assert CAPTAIN in world.agents and OFFICER in world.agents
    return world, ch, oh, seat


@pytest.fixture(scope="module")
def cutter_wardroom():
    return _the_cutters_free_passage()


def test_truth_82_two_fakes_through_two_doors_play_the_cutter_with_each_order_under_its_own_mark(
    cutter_wardroom,
):
    """Spec M6 §16, truth 82: "Two fake stations on one ship through two in-process doors,
    captain and officer, play the cutter's free passage with the captain's `you may` to
    the officer, and the log carries each order under its own mark." The captain's
    sentences are logged as his ('By the captain: you have the deck.'), the officer's
    orders as his ('By the officer of the watch: ...'), the player's answer at the
    master's seat as the driver's line it is; the officer holds the deck and the general
    authority by the captain's word."""
    world, ch, oh, seat = cutter_wardroom
    log = world.log
    assert ch.agent.has_deck and oh.agent.has_deck and oh.agent.general
    by_captain = [e.text for e in log if e.actor == "the captain" and e.kind == "order.accepted"]
    assert "By the captain: you have the deck." in by_captain
    assert "By the captain: you may work the ship." in by_captain
    assert "By the captain: tell the officer keep her full and by." in by_captain
    assert "By the captain: ask the master for a course." in by_captain
    by_officer = [
        e.text for e in log if e.actor == "the officer of the watch" and e.kind == "order.accepted"
    ]
    assert by_officer and all(t.startswith("By the officer of the watch: ") for t in by_officer)
    marks = {e.actor for e in log if e.kind == "order.accepted"}
    assert {"the captain", "the officer of the watch", "captain"} <= marks
    deck = [e for e in log if e.kind == "agent.deck" and e.data.get("deck") == "given"]
    assert [e.data["station"] for e in deck] == ["captain", "officer of the watch"]
    told = [e for e in log if e.kind == "agent.told"]
    assert told and told[0].text.startswith(
        f"The captain ({ch.station.person}), on the quarterdeck"
    )
    answered = [e for e in log if e.kind == "agent.answered"]
    assert answered and answered[0].data["to"] == "captain" and answered[0].actor == "driver"
    assert {actor for _, actor, _ in world.journal} <= {"captain", "the master (the player)"}


def test_truth_83_the_clock_holds_at_1x_while_a_sample_is_open_and_a_stand_by_releases_it():
    """Spec M6 §16, truth 83: "The clock holds at 1x while a sample is open and returns to
    the set compression when it is answered; a stand-by releases it." The browser's
    driver at 60x with a door that answers late: a real second brings one tick while the
    officer's sample is open, sixty once it is answered, one again at his next sample,
    and sixty when he stands by. The World's ticks are the same ticks: only how many a
    real second brings moves."""
    pytest.importorskip("fastapi")
    from freesail.agents import Harness, Reply, SamplingPolicy, call
    from freesail.agents.agent import officer
    from freesail.ui.server import Driver

    class Late:
        def reply(self, turns):
            return None

    world = _free_cutter()
    driver = Driver(world, compression=60.0)
    h = Harness(
        world, officer(SamplingPolicy.periodic(WARDROOM_EVERY), world=world), Late(), save=None
    )
    h.start()
    driver.running = True
    assert h.open_sample is not None
    driver._tick_owed(0.0, 1.0)
    assert world.clock.tick == 1 and driver.state()["pace"]["held"]
    assert driver.state()["pace"]["open"][0]["station"] == "officer of the watch"
    h.deliver(Reply(text="Nothing yet."))
    driver._tick_owed(0.0, 1.0)
    assert world.clock.tick == 61 and not driver.state()["pace"]["held"]
    driver._tick_owed(0.0, 9.0)
    assert world.clock.tick == 601 and h.open_sample is not None  # the next sample
    driver._tick_owed(0.0, 1.0)
    assert world.clock.tick == 602
    h.deliver(Reply(calls=(call("stand_by", until="eight bells"),)))
    assert h.agent.standing_by and h.open_sample is None
    driver._tick_owed(0.0, 1.0)
    assert world.clock.tick == 662
    assert world.readings["pace"]["rule"] == "pace"
    free = Driver(world, compression=60.0, free_running=True)
    assert free.pace.rate(60.0) == 60.0 and world.pace_rule == "free"


def test_truth_84_a_say_on_the_quarterdeck_is_heard_by_the_station_there_and_not_by_one_below():
    """Spec M6 §16, truth 84: "A `say` on the quarterdeck is heard by the station there
    and not by one below." The fake officer says a thing on the quarterdeck: the captain's
    station there has it in its next sample under `heard`, with the speaker's name and
    place; the lookout at the masthead has not."""
    from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call, reply
    from freesail.agents.agent import LOOKOUT, captain, lookout, officer
    from freesail.agents.fake import captain_of_the_ship

    world = _free_cutter()
    policy = SamplingPolicy.in_lockstep(WARDROOM_EVERY, "notable", "urgent")
    ch = Harness(world, captain(policy, world=world), captain_of_the_ship(), save=None)
    ch.start()
    lh = Harness(world, lookout(policy, world=world), Fake([Reply()] * 8), save=None)
    lh.start()
    oh = Harness(
        world,
        officer(policy, world=world),
        Fake([reply("", call("submit_order", text="say the glass is falling, sir")), Reply()]),
        save=None,
    )
    oh.start()
    world.run(WARDROOM_EVERY + 1)
    spoke = [e for e in world.log if e.kind == "agent.spoke"]
    assert len(spoke) == 1 and spoke[0].data["heard_by"] == ["captain"]
    assert spoke[0].data["place"] == "quarterdeck" and LOOKOUT not in spoke[0].data["heard_by"]
    assert spoke[0].text.startswith(
        f"The officer of the watch ({oh.station.person}), on the quarterdeck: "
    )
    heard = [
        t.content["heard"]
        for turns in ch.model.seen
        for t in turns
        if t.role == "data" and t.content.get("heard")
    ]
    assert heard and heard[0][0].endswith("on the quarterdeck: the glass is falling, sir")
    assert not any(
        t.content.get("heard") for turns in lh.model.seen for t in turns if t.role == "data"
    )
    assert lh.agent.heard == [] and ch.agent.heard == []  # carried once


def test_truth_85_a_game_saved_with_three_seated_loads_from_its_checkpoint_with_three(
    cutter_wardroom, tmp_path
):
    """Spec M6 §16, truth 85, its first half: "A game saved with three stations seated
    loads from its checkpoint with three", each re-seated station reading its own journal
    (the second half, the replay on a build whose sampling differs, is package 42's
    transcript-driven replay). The checkpoint carries the two harnesses and the
    player's seat, their decks as held; a station taken up again by a live model reads
    the journal it wrote, and its brief carries the journal's size; the JSON save
    replays to the same digest."""
    from freesail.agents import Fake, call, reply
    from freesail.agents import tools as tools_mod
    from freesail.agents.agent import CAPTAIN, MASTER, OFFICER
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, ch, oh, seat = cutter_wardroom
    ch.note("The captain's own note.")
    oh.note("The officer's own note.")
    seat.note("The master's own note, by the player.")
    path = tmp_path / "three.ckpt"
    replay_mod.write_checkpoint(world, path)
    _header, back = replay_mod.read_checkpoint(path)
    assert set(back.agents) == {CAPTAIN, OFFICER} and back.player_seat.station.name == MASTER
    assert back.agents[CAPTAIN].agent.has_deck and back.agents[OFFICER].agent.has_deck
    assert back.agents[OFFICER].agent.general and not back.player_seat.agent.released
    for name, note in ((CAPTAIN, "The captain's own note."), (OFFICER, "The officer's own note.")):
        h = back.agents[name]
        h.take_over(Fake([reply("", call("read_journal", kind="notes"))]))
        assert "The station's journal:" in h.brief.text()
        read = tools_mod.call(back, name, "read_journal", {"kind": "notes"})
        assert any(e["text"] == note for e in read["entries"]), name
    read = tools_mod.read_journal(back, MASTER, kind="notes")
    assert any(e["text"] == "The master's own note, by the player." for e in read["entries"])
    assert back.stations.names() == world.stations.names()
    save = tmp_path / "three.json"
    save.write_text(json.dumps(json.loads(json.dumps(world.save()))))
    copy = replay_mod.replay(replay_mod.load_file(save), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.player_seat is not None and copy.player_seat.station.name == MASTER


# ---------------------------------------------------------------------------
# Truths 85 (its second half) and 86 (spec M6 §16; package 42). 85: a game saved with
# three stations seated replays from its journal on a build whose sampling differs, to
# the same log (the stations' acts are its inputs, `core.acts`). 86: the API door's test
# server receives no key in any body, and the journal, the transcript and the save hold
# none (`agents.api`, against `tests/messages_api.py`, a local server in the Messages API's
# shape; no network).
# ---------------------------------------------------------------------------


def test_truth_85_a_game_with_three_stations_replays_on_a_build_whose_sampling_differs(
    tmp_path, monkeypatch
):
    """Spec M6 §16, truth 85, its second half: "A game saved with three stations seated
    ... replays from its journal on a build whose sampling differs, to the same log." The
    captain's, the officer's and the watcher's stations, fakes in lockstep, an hour of
    play; the save stamped as another build's; that build samples each station at every
    other turn of its interval. Replayed by the stations' acts (the load's road), the log
    is the one that was played, digest for digest, each journal the same; by the
    transcript, as before this package, it is another. Loaded from its checkpoint, the
    three are at their stations."""
    import json

    from test_replay import OTHER_BUILD, _restamp, three_stations

    from freesail.agents import harness as harness_mod
    from freesail.api.session import ship_factory
    from freesail.core import replay

    world = three_stations()
    with_checkpoint = replay.save_to_file(world, tmp_path / "kept.json")
    loaded, how = replay.load(with_checkpoint, ship_factory)
    assert how == "checkpoint" and len(loaded.agents) == 3
    path = replay.save_to_file(world, tmp_path / "game.json", checkpoint=False)
    _restamp(path, OTHER_BUILD)
    before = harness_mod.Harness._policy_due

    def sparser(self, new):
        p = self.policy
        if p.every_s and self.agent.stationed_tick is not None:
            since = self.world.clock.tick - self.agent.stationed_tick
            if since > 0 and since % p.every_s == 0 and since % (2 * p.every_s):
                return None
        return before(self, new)

    monkeypatch.setattr(harness_mod.Harness, "_policy_due", sparser)
    data = json.loads(path.read_text())
    copy, report = replay.load_report(path, ship_factory)
    assert report.road == replay.BY_ACTS
    assert copy.log.digest() == world.log.digest()
    assert len(copy.agents) == 3
    for name, journal in world.agent_journals.items():
        assert copy.agent_journals[name].save() == journal.save()
    other = replay.replay(data, ship_factory, road=replay.BY_TRANSCRIPT)
    assert other.log.digest() != world.log.digest()


def test_truth_86_the_api_doors_server_receives_no_key_in_any_body_and_the_game_keeps_none(
    tmp_path, monkeypatch
):
    """Spec M6 §16, truth 86: "The API door's test server receives no key in any body, and
    the journal, the transcript and the save hold none." The door seats a model whose
    consent is on record at the watcher's station of the browser game, through the local
    test server; it keeps watch for a glass, writes in its journal, and stands down. The key
    is in every request's header and in no request's body; the journal, the transcript,
    the save, the consent records and the door's own words hold none of it."""
    pytest.importorskip("anthropic")
    pytest.importorskip("keyring")
    pytest.importorskip("fastapi")
    import json

    from messages_api import MODEL, Game, MessagesServer, fake_store, finished, run_door

    from freesail.agents import consent

    fake_store(monkeypatch)
    key = "sk" + "-ant-" + "api03-" + "Hk2mVq9W" * 6
    game = Game(tmp_path)
    consent.Record(MODEL, "t", "2026-10-10", consent.YES, answer="Yes.").write(game.records)
    replies = [
        {"content": [{"type": "text", "text": f"A quiet start; no {key[:6]} here."}]},
        {
            "content": [
                {"type": "tool_use", "name": "journal", "input": {"note": "Kept the glass."}},
                {"type": "tool_use", "name": "stand_down", "input": {"note": "All well."}},
            ]
        },
    ]
    with MessagesServer(key, replies) as srv:
        got = run_door(game, ["--model", MODEL, "--base-url", srv.url], {"FREESAIL_API_KEY": key})
        game.wait_for(game.floor_is_the_games(0))
        game.driver.tick(1800)  # a glass
        assert finished(got) == 3
        requests = list(srv.requests)
    assert len([r for r in requests if r["method"] == "POST"]) == 2
    assert all(r["headers"].get("x-api-key") == key for r in requests)
    assert not any(key in r["body"] for r in requests)
    h = game.harness
    assert h.agent.released and "stood down" in h.agent.released_reason
    assert key not in json.dumps(h.transcript)
    assert key not in json.dumps(game.world.agent_journals["watcher"].save())
    assert key not in json.dumps(game.world.save())
    kept = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert any(p.suffix == ".json" for p in kept)  # the stand-down's save
    for p in kept:
        assert key.encode() not in p.read_bytes(), p
    assert key not in got["out"].getvalue()


# ---------------------------------------------------------------------------
# Milestone 7b, part i: the director (package 50; spec M7b §2 to §7): truths 7b-90 to
# 7b-94 on the frigate at seed 7 off the Lizard under the climatology's weather, a day with
# the fake director on the quiet-passage brief and the fake captain beside it. (M6 used the
# numbers 90 and 91 for the regatta and the parity; the director's are the spec's 90 to 94,
# cited as 7b-90 to 7b-94.) No recorded passage's pin moves: none has a director, and a
# world with no director bound is as it was (`test_director.py`).
# ---------------------------------------------------------------------------

DIRECTOR_EVERY = 1800  # the director and the captain sampled every glass, in lockstep

# The fake director's day on the quiet passage: the channel's forms as examples (a sail
# over the horizon, one inside it, a thing found aboard with and without its cause, a low
# within the brief's force and one beyond it, a letter, a price, a mark, a mind changed),
# and orders beyond the examples (news of a war, free words aboard, words in the mouth of a
# stranger never made: package 52 gave the voice to the people the world has), which the
# game answers honestly and logs as attempted when re-entered with a reason.
DIRECTED_DAY_ORDERS = [
    'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth, '
    "intent: bound for Falmouth",
    'ship: a cutter "Lark" of Britain at 49 28 N 5 40 W, bound for Falmouth',
    'weather: low "the gale" radius 450 km at 1805-06-12T22:00 -800 800 965',
    'weather: low "a soft low" radius 500 km at 1805-06-12T16:00 -700 500 1006',
    "aboard: a cask found stove",
    "aboard: the fore topmast is found sprung",
    "news: war declared between Britain and Denmark",
    "aboard: the cook reports the beef cask found rotten",
    'message: by a cutter from Falmouth from the collector: "The packet is in."',
    "port falmouth: price of tin 125",
    "mark: a wreck, her masts showing above the water at 49 10 N 6 00 W",
    'ship "Nancy": intent run home to Falmouth',
    'say as the harbourmaster of Falmouth: "The packet is in."',
    'ship: a brig-sloop "Harpy" of France at 48 50 N 6 10 W, running home to Brest, no colours',
]


def _directed_world() -> World:
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        systems=[],
        climatology=True,
        glass=True,
    )
    return make_world(7, FRIGATE, sc)


def _the_directed_day():
    """A day at seed 7 with the fake director on the quiet-passage brief (its budget
    raised to the day's fourteen orders, so that every order is tried) and the fake
    captain seated, the player asking for the director's log at the day's end."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents import director as director_mod
    from freesail.agents.agent import DIRECTOR, SESSION_DIRECTOR, captain, director
    from freesail.agents.fake import captain_of_the_ship, director_above_the_game

    world = _directed_world()
    world.submit("set plain sail")
    quiet = director_mod.resolve_brief("quiet-passage").to_dict()
    quiet["budget"] = {"samples_a_day": 60, "acts_a_day": 14}
    director_mod.set_brief(world, quiet, source="the test")
    policy = SamplingPolicy.in_lockstep(DIRECTOR_EVERY, "notable", "urgent")
    ch = Harness(
        world,
        captain(policy, world=world),
        captain_of_the_ship(["heave the log"]),
        save=lambda w, r: None,
    )
    ch.model_name, ch.door = "the fake captain", "mcp"
    ch.start()
    dh = Harness(
        world,
        director(policy, world=world),
        director_above_the_game(DIRECTED_DAY_ORDERS),
        session_kind=SESSION_DIRECTOR,
        save=lambda w, r: None,
    )
    dh.model_name, dh.door = "the fake director", "runner"
    dh.start()
    world.run(24 * 3600)
    assert DIRECTOR in world.agents
    return world, ch, dh


@pytest.fixture(scope="module")
def directed_day():
    return _the_directed_day()


def test_truth_7b_90_the_quiet_passage_raises_no_gale_above_the_briefs_force(directed_day):
    """Spec M7b §7, truth 90: "A director on the quiet-passage brief raises no gale above
    the brief's force in a week at seed 7; an order beyond it is refused with the reason in
    the director's log." The day: the gale's low is refused by the brief, the soft low is
    appended; and the limit holds for a week of gale orders by the same rule."""
    from freesail.agents import director as director_mod

    world, _ch, _dh = directed_day
    log = director_mod.log_of(world)
    refused = [e for e in log.entries if e.kind == "director.refused"]
    gales = [e for e in refused if "the gale" in e.text]
    assert gales and all("no wind above 27 knots" in e.text for e in gales)
    assert all("Refused by the brief" in e.text for e in refused)  # the limits alone refuse
    assert world.systems.find("the gale") is None and world.systems.find("a soft low") is not None
    brief = director_mod.brief_of(world)
    for day in range(7):
        gale = f'weather: low "gale {day}" radius 450 km at 1805-06-{13 + day}T04:00 -800 800 965'
        order = WO_parse(gale)
        why = brief.limit_of(world, order)
        assert why and "no wind above 27 knots" in why, day
    assert (
        director_mod._peak_wind_kn(
            world, 'weather: low "x" radius 500 km at 1805-06-12T16:00 -700 500 1006'
        )
        <= 27
    )


def WO_parse(text: str):
    from freesail.world import orders as WO

    return WO.parse(text)


def test_truth_7b_91_a_world_order_of_the_directors_is_in_no_sample_and_its_effect_is(directed_day):
    """Spec M7b §7, truth 91: "A world order given by the director appears in no station's
    sample and no play log; its effect does, when met." The captain's samples over the day
    carry no order and no word of the director; the Nancy is sighted, the cooper's report
    and the price's effect are met."""
    from freesail.core.events import for_the_record

    world, ch, _dh = directed_day
    samples = [t.content for t in ch.turns if t.role == "data"]
    text = json.dumps(samples).lower()
    assert "world order" not in text and "director" not in text
    play = [e for e in world.log.all() if not for_the_record(e)]
    assert not [e for e in play if e.kind == "world.order" or e.actor == "the director"]
    assert any("cooper reports a water cask stove" in json.dumps(s) for s in samples)
    assert any("lookout.sighting" in json.dumps(s) for s in samples)
    given = [
        o for o in world.world_orders if o["source"] == "the director" and o["result"] == "done"
    ]
    assert any('"Nancy"' in o["order"] for o in given)  # put on the sea (and home by night)
    assert world.dealings.ports["falmouth"].market.goods["tin"].price == 125.0


def test_truth_7b_92_the_log_is_empty_to_every_station_until_asked_and_then_shows_every_act(
    directed_day,
):
    """Spec M7b §7, truth 92: "The director's log is empty to every station and the player
    until asked for, and then shows every act with its reason; a replay shows it inline."
    The day's log: an order given, one doubted and entered again with its reason, the
    gale refused, an order beyond the examples logged as attempted with its words, the
    budget's lines, the director's thoughts; `the director's log` reveals it and the
    director is told; the two-stories view has it inline."""
    from freesail.agents import director as director_mod
    from freesail.agents import tools as tools_mod
    from freesail.agents.agent import CAPTAIN

    world, ch, dh = directed_day
    assert "director" not in json.dumps(tools_mod.read_log(world, CAPTAIN, since_tick=0)).lower()
    assert "director" not in tools_mod.state(world, CAPTAIN).lower()
    kinds = set(e.kind for e in director_mod.log_of(world).entries)
    assert {
        "director.brief",
        "director.order",
        "director.doubted",
        "director.reentered",
        "director.refused",
        "director.unperformed",
        "director.attempted",
        "note",
    } <= kinds
    reentered = [e for e in director_mod.log_of(world).entries if e.kind == "director.reentered"]
    assert all("the doubt:" in e.text and "the reason:" in e.text for e in reentered)
    attempted = [e for e in director_mod.log_of(world).entries if e.kind == "director.attempted"]
    assert any("news: war declared" in e.text for e in attempted)
    assert any("say as the harbourmaster" in e.text for e in attempted)
    assert any("beef cask found rotten" in e.text for e in attempted)
    lines = director_mod.reveal(world, "the player")
    assert lines[0].startswith("The director's log (") and len(lines) > 20
    assert any("asked for by the player" in n for n in dh.agent.notices)
    stories = director_mod.two_stories(world)
    assert any(ln.startswith("D ") and "(reentered)" in ln for ln in stories)
    assert not any("World order" in ln for ln in stories if not ln.startswith("D "))


def test_truth_7b_93_a_director_on_three_acts_a_day_gives_no_fourth():
    """Spec M7b §7, truth 93: "A director on a budget of three acts a day gives no fourth;
    the sample says the budget is spent." Three prices given, the fourth refused with the
    words, the day's hold said in the log, and the sample's notice."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents import director as director_mod
    from freesail.agents.agent import SESSION_DIRECTOR, director
    from freesail.agents.fake import director_above_the_game

    world = _directed_world()
    world.submit("set plain sail")
    director_mod.set_brief(
        world, {"name": "three", "budget": {"samples_a_day": 48, "acts_a_day": 3}}, source="t"
    )
    orders = [f"port falmouth: price of tin {p}" for p in (120, 125, 130, 135)]
    dh = Harness(
        world,
        director(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        director_above_the_game(orders),
        session_kind=SESSION_DIRECTOR,
        save=lambda w, r: None,
    )
    dh.model_name, dh.door = "the fake director", "runner"
    dh.start()
    world.run(4 * 600)
    assert world.dealings.ports["falmouth"].market.goods["tin"].price == 130.0
    assert director_mod.budget_of(world).acts == 3
    texts = [e.text for e in director_mod.log_of(world).entries]
    assert any("budget of 3 acts is spent" in t for t in texts)
    assert director_mod.budget_of(world).held_until is not None
    # the sample says it: the result of the act that spent the budget, read in the turn
    results = json.dumps([t.content for t in dh.turns if t.role == "data"])
    assert "budget of 3 acts is spent; the director stands by until the next day" in results
    assert "2 of 3 acts used" in results  # and the budget as it stands, at each sample


def test_truth_7b_94_a_directed_voyage_saved_replays_to_the_same_log(directed_day, tmp_path):
    """Spec M7b §7, truth 94: "A directed voyage saved and replayed gives the same log, the
    director's acts among the inputs." The day's save, replayed by its transcript and by
    its stations' acts (the director's world orders among them), to the same digest and
    the same director's log entry for entry."""
    from freesail.agents import director as director_mod
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, _ch, _dh = directed_day
    path = replay_mod.save_to_file(world, tmp_path / "directed-day.json", checkpoint=False)
    data = replay_mod.load_file(path)
    assert [a for a in data["station_acts"] if "world_order" in a]
    for road in (replay_mod.BY_TRANSCRIPT, replay_mod.BY_ACTS):
        copy = replay_mod.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        assert [e.to_dict() for e in director_mod.log_of(copy).entries] == [
            e.to_dict() for e in director_mod.log_of(world).entries
        ], road


# ---------------------------------------------------------------------------
# Milestone 7b, part ii: the director's voice (package 52; spec M7b §8 to §10): truths
# 7b-95 to 7b-97 on the frigate at seed 7 off the Lizard, two hours with the fake director
# on the quiet-passage brief giving its voice, and a fake officer of the watch beside it
# who asks the cook a question. No recorded passage's pin moves: none has a director or a
# `person:` order.
# ---------------------------------------------------------------------------

VOICE_EVERY = 600  # the director and the officer sampled every ten minutes, in lockstep

# The director's two hours: a person made from words, brought aboard (doubted, the port
# beyond a boat's reach, and entered again with its reason) and bound to the master's
# station; a word put in the mouth of the captain (the player at the prompt) and of the
# officer (a model), each refused by the rule of reach; and the new master's own words.
VOICED_ORDERS = [
    'person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth, who knew the '
    "captain's father",
    'person: "Mr Fox" comes aboard as master',
    'say as the captain: "Make it so."',
    'say as Mr Pearce: "All well forward, sir."',
    'say as Mr Fox: "I knew your father, sir."',
]
COOKS_ANSWER = "Pease and pork, sir, and duff on Sunday."


def _the_voiced_watch():
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents import director as director_mod
    from freesail.agents.agent import SESSION_DIRECTOR, director, officer
    from freesail.agents.fake import director_above_the_game

    world = _directed_world()
    world.submit("set plain sail")
    quiet = director_mod.resolve_brief("quiet-passage").to_dict()
    quiet["budget"] = {"samples_a_day": 60, "acts_a_day": 8}
    director_mod.set_brief(world, quiet, source="the test")
    policy = SamplingPolicy.in_lockstep(VOICE_EVERY, "notable", "urgent")
    cook = world.people.of_the_company("the cook", draw=False)
    dh = Harness(
        world,
        director(policy, world=world),
        director_above_the_game(VOICED_ORDERS, answers={cook.name: COOKS_ANSWER}),
        session_kind=SESSION_DIRECTOR,
        save=lambda w, r: None,
    )
    dh.model_name, dh.door = "the fake director", "runner"
    dh.start()
    oh = Harness(
        world,
        officer(policy, world=world),
        Fake(
            [
                reply("", call("stand_by", until="a glass")),
                reply(
                    "",
                    call("submit_order", text="ask the cook what is for dinner"),
                    call("stand_by", until="a watch"),
                ),
            ],
            when_done=reply("Thank you, cook."),
        ),
        save=lambda w, r: None,
    )
    oh.model_name, oh.door = "the fake officer", "mcp"
    oh.start()
    world.run(2 * 3600)
    return world, dh, oh


@pytest.fixture(scope="module")
def voiced_watch():
    return _the_voiced_watch()


def test_truth_7b_95_a_person_made_from_words_is_on_the_muster_holds_his_station_and_replays(
    voiced_watch, tmp_path
):
    """Spec M7b §10, truth 95: "A person made from words is on the muster of the ship he
    joins, holds the station he is bound to, and is there after a save and a replay." Mr
    Fox, made at Falmouth and brought aboard (the doubt and the reason in the director's
    log), is among the people, holds the master's station (a model seated there is in his
    place, his outline in its brief), speaks in his own name, and is all of it again in the
    save replayed by the transcript and by the acts, to the same digest."""
    from freesail.agents import director as director_mod
    from freesail.agents.agent import master
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, _dh, _oh = voiced_watch
    fox = world.people.find("Mr Fox")
    assert fox is not None and fox.aboard and fox.outline.age == 60
    assert any(line.startswith("Mr Fox, pilot") for line in world.people.describe())
    assert world.stations.holder("master") is fox
    st = master(world=world)
    assert st.person == "Mr Fox" and "Guernsey pilot" in st.outline
    kinds = [e.kind for e in director_mod.log_of(world).entries]
    assert "director.doubted" in kinds and "director.reentered" in kinds
    spoke = [e.text for e in world.log.all() if e.kind == "person.spoke"]
    assert "Mr Fox, the pilot, on the quarterdeck: I knew your father, sir." in spoke
    path = replay_mod.save_to_file(world, tmp_path / "voiced.json", checkpoint=False)
    data = replay_mod.load_file(path)
    for road in (replay_mod.BY_TRANSCRIPT, replay_mod.BY_ACTS):
        copy = replay_mod.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        again = copy.people.find("Mr Fox")
        assert again is not None and again.outline == fox.outline, road
        assert copy.stations.holder("master") is again, road


def test_truth_7b_96_a_question_to_the_cook_is_answered_in_his_words_with_a_director_seated(
    voiced_watch,
):
    """Spec M7b §10, truth 96: "A question to the cook, with a director seated, is answered
    in the cook's words at the galley and heard by those within earshot; with none, by the
    rules as before." The officer asks; the director, told in its sample, answers as the
    cook (no act counted); the line is the cook's at the galley, heard by the officer on
    the quarterdeck, and the answer wakes the officer's stand-by. With no director seated
    the question is refused in the words it always was."""
    world, dh, oh = voiced_watch
    cook = world.people.find("the cook")
    assert cook is not None and cook.where == "galley"
    said = f"{cook.name}, the cook, in the galley: {COOKS_ANSWER}"
    spoke = [e for e in world.log.all() if e.kind == "person.spoke" and e.text == said]
    assert spoke and spoke[0].data["heard_by"] == ["officer of the watch"]
    asked = [e for e in world.log.all() if e.kind == "agent.asked" and "the cook" in e.text]
    assert asked and asked[0].tick < spoke[0].tick <= asked[0].tick + 1800
    director_samples = json.dumps([t.content for t in dh.turns if t.role == "data"])
    assert "whom nobody holds: what is for dinner?" in director_samples
    officer_samples = json.dumps([t.content for t in oh.turns if t.role == "data"])
    assert f"answers your question (what is for dinner?): {COOKS_ANSWER}" in officer_samples
    given = [o for o in world.world_orders if o["order"].startswith("say as " + cook.name)]
    assert given and given[0]["result"] == "done"
    # with none seated: the rules, as before (a world with the brief and no director, and
    # one with neither, refuse it alike)
    alone = _directed_world()
    plain = make_world(7, FRIGATE, alone.scenario)
    from freesail.agents import director as director_mod

    director_mod.set_brief(alone, "quiet-passage", source="the test")
    a = alone.submit("ask the cook what is for dinner")
    b = plain.submit("ask the cook what is for dinner")
    assert a.kind == b.kind == "order.rejected" and a.text == b.text
    assert alone.people.find("the cook") is None


def test_truth_7b_97_say_as_a_held_station_is_refused(voiced_watch):
    """Spec M7b §10, truth 97: "`say as` a held station is refused." The director's words
    put in the captain's mouth (the player at the prompt) and the officer's (a model) are
    refused by the rule of reach in its log, the stations held named, no act counted and
    no word said in either name."""
    from freesail.agents import director as director_mod

    world, _dh, _oh = voiced_watch
    refused = [e for e in director_mod.log_of(world).entries if e.kind == "director.refused"]
    assert len(refused) == 2 and all("rule of reach" in e.text for e in refused)
    assert "say as the captain" in refused[0].text and "player at the prompt" in refused[0].text
    assert "say as Mr Pearce" in refused[1].text and "held by a model" in refused[1].text
    names = [e.data.get("person") for e in world.log.all() if e.kind == "person.spoke"]
    assert "Captain Bowen" not in names and "Mr Pearce" not in names
    held = [o for o in world.world_orders if o["order"].startswith("say as the captain")]
    assert not held  # refused at the door: never an order on the channel


# ---------------------------------------------------------------------------
# Truths 7b-103 and 7b-104 (spec M7b §21; package 54): the needs. The frigate at seed 7 on
# the plane with the player at the prompt (a driver listening, as the console does), from
# 06:00 on 10 June to 05:00 on the 13th: two days and more neither eating nor drinking nor
# sleeping, asleep where he stood on the third, then fed, put to short allowance, a night
# below. No recorded passage's pin moves: the needs show to the person stationed alone,
# never in the log, and the stores' fall is a reading.
# ---------------------------------------------------------------------------

NEEDS_START = datetime(1805, 6, 10, 6, 0)


def _hours(h: float) -> int:
    return int(h * 3600)


def _the_needs_days():
    world = make_world(7, FRIGATE, Scenario(start_time=NEEDS_START, gustiness=0.0, variability=0.0))
    told = []
    world.needs.listen(told.append)
    moments = {}

    def stores():
        s = world.stores
        return (s.provisions_days, s.water_tons, world.readings.words("stores"))

    run(world, _hours(24) + 60)  # 06:01 on the 11th: a day's three meals served
    moments["a day"] = stores()
    moments["the first lieutenant"] = world.people.find("first lieutenant").needs
    run(world, _hours(57) - world.clock.tick)  # 15:00 on the 12th, asleep since 14:01
    moments["asleep"] = (
        world.people.captain.needs.asleep,
        world.people.state_words(world.people.captain),
    )
    answers = {o: world.submit(o) for o in ("eat", "drink")}
    moments["before short"] = stores()
    answers["short allowance"] = world.submit("short allowance")
    run(world, _hours(58) - world.clock.tick)  # 16:00, supper at half the whole: 16:01
    run(world, 60)
    moments["after supper"] = stores()
    moments["the purser's books"] = world.papers.page("the purser's books").lines
    run(world, _hours(62) - world.clock.tick)  # 20:00: whole allowance, a meal, and below
    answers["whole allowance"] = world.submit("whole allowance")
    answers.update({f"{o} at night": world.submit(o) for o in ("eat", "drink", "sleep")})
    run(world, _hours(71) - world.clock.tick)  # 05:00 on the 13th
    return world, told, moments, answers


@pytest.fixture(scope="module")
def needs_days():
    return _the_needs_days()


def test_truth_7b_103_the_frigates_provisions_fall_by_the_ration_and_short_allowance_halves_it(
    needs_days,
):
    """Spec M7b §21, truth 103: "The frigate's provisions fall by the ration for her
    complement; the purser's reading says the days remaining; short allowance halves it."
    A day's meals take a day of provisions and 264 gallons of water for her 264; the
    reading says the days her water and her provisions last; at short allowance a meal
    takes half its share and the days are doubled; and none of it is a line of the log
    but the captain's order with the people's temper."""
    world, _told, moments, answers = needs_days
    days, tons, words = moments["a day"]
    assert days == pytest.approx(119.0) and tons == pytest.approx(100 - 264 / 252)
    assert words == "water 99 tons for 94.5 days, provisions for 119 days"
    before, after = moments["before short"], moments["after supper"]
    assert before[0] - after[0] == pytest.approx(1 / 6)  # a third of a day, at half
    assert before[1] - after[1] == pytest.approx(264 / 252 / 6)
    assert f"({after[0] * 2:.0f} at short allowance)" in after[2]
    e = answers["short allowance"]
    assert e.kind == "stores.allowance" and "take it sullenly" in e.text
    assert [x.kind for x in world.log if x.kind.startswith("stores.")] == ["stores.allowance"] * 2
    assert "back to whole allowance" in answers["whole allowance"].text
    page = moments["the purser's books"]
    assert page[0].endswith("days at short allowance.")
    assert page[1].endswith("at the short allowance the people are at.")


def test_truth_7b_104_a_player_without_food_or_sleep_reads_the_urgent_lines_and_sleeps_on_the_third(
    needs_days,
):
    """Spec M7b §21, truth 104: "A player who neither eats nor sleeps for two days reads
    the urgent lines in order and is asleep on the third; eating from the stores and a
    night below reset them; an unseated person's needs never show." The lines at the
    prompt, notable at the change of the watch and urgent at once, thirst, hunger and then
    fatigue; asleep where he stood on the 12th; eating and drinking wake him and a night
    below rests him, and at five on the 13th nothing is said of him; the first lieutenant,
    whom nobody holds, is the routine's and told nothing; no line of the needs in the log."""
    world, told, moments, answers = needs_days
    said = [(e.ship_time.strftime("%d %H:%M"), e.severity.value, e.text) for e in told]
    assert said[:7] == [
        ("11 12:00", "notable", "You are quite thirsty and quite hungry. ('drink' and 'eat')"),
        ("11 20:00", "notable", "You are parched and feeling a bit drowsy. ('drink' and 'sleep')"),
        ("12 00:00", "notable", "You are very hungry. ('eat')"),
        ("12 04:00", "urgent", "You are desperately thirsty and very tired. ('drink' and 'sleep')"),
        ("12 06:00", "urgent", "You are absolutely starving. ('eat')"),
        ("12 08:01", "urgent", "You are hardly able to keep your eyes open. ('sleep')"),
        (
            "12 14:01",
            "urgent",
            "You have fallen asleep where you stood, on the quarterdeck. Your next order "
            "wakes you. ('sleep')",
        ),
    ]
    assert moments["asleep"] == ("where he is", "asleep where he stood, on the quarterdeck")
    assert said[7] == ("12 15:00", "notable", "You wake, on the quarterdeck.")
    assert answers["eat"].text.startswith(
        "A biscuit and a piece of cheese are brought up from the stores; you eat on the "
        "quarterdeck, the first since 06:00 on 10 June"
    )
    assert answers["drink"].text.startswith("You drink at the scuttle-butt")
    assert answers["sleep at night"].text.startswith("You turn in below, in the cabin.")
    assert said[-1][1:] == ("notable", "You wake, rested, on the quarterdeck.")
    cap = world.people.captain
    assert world.needs.words(cap) == "" and not cap.needs.asleep
    # an unseated person's needs never show
    assert {e.data["person"] for e in told} == {cap.name}
    first = moments["the first lieutenant"]
    assert first is None or not first.by_hand
    assert not [e for e in world.log if e.kind.startswith("needs.")]
    assert all(e.kind == "needs.answer" for k, e in answers.items() if "allowance" not in k)


# Milestone 7b, part iv: people in places (package 53; spec M7b §14, §16 to §18): truths
# 7b-100 to 7b-102. 100 on the frigate at seed 7 off the Lizard with a fake officer of the
# watch who goes below with the deck and comes up again; 101 and 102 on the schooner at
# anchor in Carrick Road, the player ashore and aboard, a manifest and a sheet drafted. No
# recorded passage's pin moves: none moves a person, drafts a book or goes ashore, and a
# world in which nobody moves is as it was (the place's checks muster nobody).
# ---------------------------------------------------------------------------

PLACES_EVERY = 600  # the officer sampled every ten minutes, in lockstep


def _officer_below_and_up():
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer

    world = _directed_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        reply("", call("stand_by", until="ten minutes")),
        reply(
            "",
            call("submit_order", text="go below"),
            call("submit_order", text="set the royals"),
            call("stand_by", until="a glass"),
        ),
        reply(
            "",
            call("submit_order", text="go on deck"),
            call("submit_order", text="set the royals"),
            call("stand_by", until="a watch"),
        ),
    ]
    oh = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(PLACES_EVERY, "notable", "urgent"), world=world),
        Fake(script, when_done=reply("All well.")),
        save=lambda w, r: None,
    )
    oh.model_name, oh.door = "the fake officer", "mcp"
    oh.start()
    # the deck given once he is seated, so that a replay by the acts finds him there
    assert world.submit("you have the deck").kind == "agent.deck"
    return world, oh


def _until_line(world, kind: str, n: int, seconds: int = 3600) -> None:
    """Run the world a minute at a time until it has `n` lines of `kind`."""
    for _ in range(seconds // 60):
        if len(events(world, kind)) >= n:
            return
        world.run(60)
    raise AssertionError(f"no {n} lines of {kind} in {seconds} s")


def test_truth_7b_100_a_person_who_goes_below_is_below_and_his_deck_order_refused_until_up(
    tmp_path,
):
    """Spec M7b §18, truth 100: "A person who goes below is below in the muster and the
    state; an order of the deck's from him is refused in words until `go on deck` brings
    him back." The officer of the watch (a fake at his station, with the deck) goes below:
    the gunroom is his place, the people and the muster say so, and his order to set the
    royals is refused in words naming the way back; a glass later he comes on deck and
    the same order is carried out. The player at the prompt alike: the captain in his cabin
    is refused the helm and given it on the quarterdeck. The game saved and replayed by the
    transcript and by the acts is the same log."""
    from freesail.api import queries
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, oh = _officer_below_and_up()
    _until_line(world, "person.moved", 1)
    pearce = world.stations.holder("officer of the watch")
    assert pearce.where == "gunroom"
    assert world.people.state_words(pearce) == "with the deck, in the gunroom"
    assert f"{pearce.name}, with the deck, in the gunroom" in queries.muster_lines(world)[-1]
    moved = events(world, "person.moved")
    assert [e.text for e in moved] == [f"{pearce.name} went below to the gunroom."]
    refused = [e for e in events(world, "order.rejected") if "royals" in e.text]
    assert refused and refused[0].text.endswith(
        "You are in the gunroom; go on deck to make or take in sail."
    )
    assert not any("royal" in e.text for e in events(world, "evolution.started"))
    _until_line(world, "person.moved", 2)
    assert pearce.where == "quarterdeck"
    assert world.people.state_words(pearce) == "on deck, with the watch"
    assert (
        events(world, "person.moved")[-1].text == f"{pearce.name} came on deck, to the quarterdeck."
    )
    taken = [e for e in events(world, "order.accepted") if "royals" in e.text]
    assert taken and taken[0].actor == "the officer of the watch"
    # the player at the prompt is a person with a place too: the captain below is refused
    # the helm, and has it on the quarterdeck
    assert world.submit("go below").kind == "captain.below"
    e = world.submit("steer south-west")
    assert e.kind == "order.rejected"
    assert e.text.endswith("You are in the cabin; go on deck to give the helm an order.")
    assert world.submit("come on deck").kind == "captain.on_deck"
    assert world.submit("steer south-west").kind != "order.rejected"
    world.run(60)
    path = replay_mod.save_to_file(world, tmp_path / "places.json", checkpoint=False)
    data = replay_mod.load_file(path)
    for road in (replay_mod.BY_TRANSCRIPT, replay_mod.BY_ACTS):
        copy = replay_mod.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        assert copy.stations.holder("officer of the watch").where == "quarterdeck", road
        assert copy.people.captain.where == "quarterdeck", road


def _ashore_in_falmouth(**kw):
    world = _in_port(CARRICK_ROAD_5C, cargo={"purse_pounds": 3000.0}, **kw)
    world.run(60)
    return world


def _until(world, done, minutes: int = 300) -> None:
    for _ in range(minutes):
        if done():
            return
        world.run(60)
    raise AssertionError("not done in time")


def test_truth_7b_101_the_player_ashore_buys_at_the_market_in_person_and_aboard_by_the_boat(
    tmp_path,
):
    """Spec M7b §18, truth 101: "The player ashore buys at the market in person; aboard, by
    the boat." The schooner at anchor in Carrick Road; her master (the player) goes ashore
    by the boat and is landed at the quay; his deck's orders refused there, his bargain
    refused until he goes to the market; there he buys ten tons of tin in person (the
    prices read there, the boat at the booms, the tin off by the port's lighter); `come
    aboard` sends the boat for him; aboard, a bargain goes by the boat as it always did.
    The save replayed is the same log."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world = _ashore_in_falmouth()
    master = world.people.captain
    e = world.submit("go ashore")
    assert e.kind == "order.accepted" and world.dealings.boat.errand == "landing"
    _until(world, lambda: not world.dealings.boat.away)
    assert not master.aboard and master.where == "shore" and master.port == "falmouth"
    assert world.people.state_words(master) == "ashore at Falmouth, on the quay"
    assert any(
        x.text == f"{master.name} landed at the quay at Falmouth."
        for x in events(world, "person.ashore")
    )
    assert (
        "the market: the port's goods are bought and sold in person"
        in world.submit("the places ashore").text.lower()
    )
    e = world.submit("set the jib")
    assert e.text.endswith(
        "You are ashore at Falmouth, on the quay; come aboard to make or take in sail."
    )
    e = world.submit("buy 10 tons of tin")
    assert e.text.endswith("go to the market to buy and sell in person.")
    assert world.submit("go to the market").kind == "person.moved"
    purse = world.purse.pounds
    e = world.submit("buy 10 tons of tin")
    assert e.kind == "market.bargain" and e.data["by"] == "person", e.text
    assert e.text.startswith(
        f"{master.name} at the market of Falmouth, in person: bought 10 tons of tin"
    )
    assert not world.dealings.boat.away  # no boat: in person
    price = e.data["bargains"][0]["price_pounds"]
    assert world.purse.pounds == pytest.approx(purse - 10 * price)
    assert "falmouth" in world.dealings.price_lists  # read at the market
    _until(world, lambda: world.hold.goods.get("tin", 0.0) >= 10.0)
    bought = events(world, "market.bought")[-1]
    assert "came off by the lighter from Falmouth" in bought.text and bought.data["by"] == "lighter"
    assert world.submit("come aboard").kind == "order.accepted"
    _until(world, lambda: master.aboard and not world.dealings.boat.away)
    assert any(
        x.text == f"{master.name} came aboard from the boat." for x in events(world, "person.came")
    )
    # aboard, by the boat
    e = world.submit("buy 5 tons of tin")
    assert e.kind == "market.bargain" and "the boat goes for it" in e.text
    assert world.dealings.boat.away and world.dealings.boat.errand == "purchase"
    _until(world, lambda: not world.dealings.boat.away)
    assert world.hold.goods["tin"] == pytest.approx(15.0)
    path = replay_mod.save_to_file(world, tmp_path / "ashore.json", checkpoint=False)
    copy = replay_mod.replay(replay_mod.load_file(path), ship_factory)
    assert copy.log.digest() == world.log.digest()


def test_truth_7b_102_a_drafted_manifest_trades_in_one_errand_and_a_posted_sheet_stands(
    tmp_path,
):
    """Spec M7b §18, truth 102: "A drafted manifest given to the boat trades its goods in
    one errand; a drafted night-orders sheet posted is the standing orders." The schooner
    in Carrick Road with the prices known: a manifest drafted to buy tin and salt and sell
    none is given to the boat, and the boat goes once for both, which come off together; a
    sheet of two standing orders drafted and posted is in the book in the master's rank and
    fires; both books are in the library with his mark, read from anywhere; the save
    replayed is the same log and the same books."""
    from freesail.agents import tools
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod
    from freesail.world.books import books_of

    world = _ashore_in_falmouth(papers={"price_lists": ["falmouth"]})
    master = world.people.captain
    e = world.submit('draft a book "cargo": buy 10 tons of tin; buy 4 tons of salt')
    assert e.kind == "book.drafted" and "a manifest of 2 bargains" in e.text
    before = len(events(world, "boat.away"))
    purse = world.purse.pounds
    e = world.submit('give the book "cargo" to the boat')
    assert e.kind == "market.bargain" and e.data["by"] == "boat", e.text
    assert e.text.startswith("By the manifest 'cargo': bought 10 tons of tin")
    paid = e.data["paid_pounds"]
    assert world.purse.pounds == pytest.approx(purse - paid)
    _until(world, lambda: not world.dealings.boat.away)
    assert len(events(world, "boat.away")) == before + 1  # one errand for both
    assert world.hold.goods["tin"] == pytest.approx(10.0)
    assert world.hold.goods["salt"] == pytest.approx(4.0)
    e = world.submit(
        'draft a book "night orders": standing order "lead": every glass then heave the lead; '
        '"dusk": at sunset then heave the lead'
    )
    assert e.kind == "book.drafted" and "a standing-orders sheet of 2 orders" in e.text
    e = world.submit('post the book "night orders"')
    assert e.kind == "book.posted", e.text
    names = [r.name for r in world.standing.book.rules]
    assert "lead" in names and "dusk" in names
    assert all(
        r.given_by == "captain" for r in world.standing.book.rules if r.name in ("lead", "dusk")
    )
    world.run(1800)
    assert any(
        x.actor == "standing order 'lead'" for x in world.log.all() if x.kind == "order.accepted"
    )
    books = books_of(world).items
    assert [b.title for b in books] == ["cargo", "night orders"]
    assert all(b.mark == master.name for b in books)
    page = tools.library(world, "officer of the watch", "books", "night orders")
    assert f"drafted by {master.name}" in page and "heave the lead" in page
    path = replay_mod.save_to_file(world, tmp_path / "books.json", checkpoint=False)
    copy = replay_mod.replay(replay_mod.load_file(path), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert [b.title for b in books_of(copy).items] == ["cargo", "night orders"]


# Package 57: the rig through the generator (spec M7b §24; the owner's notes of the
# Éclair's first cruise, 2026-10-17, and his finding at gate 6c). Truths 7b-111 and 7b-112,
# numbered after the spec's 110 (the brief's "after 7b-104" taken as the next free numbers,
# 105 to 110 being 56's and 59's). The lugger's lug topsails are lugs set flying, sheeted
# to the lower lugs' peaks; the frigate lies to under Steel's main staysail with the storm
# staysails M6 left.
# ---------------------------------------------------------------------------

LUGGER = "data/ships/lugger.yaml"


def _lug_sides(world) -> dict[str, str | None]:
    from freesail.api import queries

    snap = queries.snapshot(world)
    return {s["id"]: s["lug_side"] for s in snap["sails"] if s["class"] == "lug"}


def test_truth_7b_111_the_luggers_lugs_lie_to_leeward_and_none_is_aback_through_a_tack_and_a_wear():
    """Package 57 (the owner's notes 1 to 4 of the Éclair's first cruise): the lugger
    close-hauled on either tack at seed 7 shows every lug to leeward of its mast, the lug
    topsails with their lower lugs (the snapshot the picture is drawn from), and no sail is
    aback through a tack and a wear: her topsails were square and braced as yards before,
    and caught the wind on the wrong side three times in the cruise."""
    world = make(LUGGER, 300.0)  # sixty degrees off a fifteen-knot northerly, starboard tack
    settle(world, ["set plain sail"])
    ship = world.ship
    assert all(ship.sails[s].is_set for s in ("fore.topsail", "main.topsail"))
    for lee, order in (("larboard", "tack ship"), ("starboard", "wear ship")):
        sides = _lug_sides(world)
        for sid in ("fore.lug", "main.lug", "fore.topsail", "main.topsail"):
            assert sides[sid] == lee, (sid, sides)  # the lee side of the tack she is on
        start = world.clock.tick
        world.submit(order)
        backed = set()
        for _ in range(900):
            world.tick()
            backed |= {s.id for s in ship.sails.values() if s.backed}
        assert not backed, (order, backed)
        aback = [e.text for e in world.log if e.tick > start and e.kind == "ship.aback"]
        assert not aback, (order, aback)
        done = "ship.tacked" if order == "tack ship" else "ship.wore"
        assert [e for e in world.log if e.tick > start and e.kind == done], order
        run(world, 300, 120)
    sides = _lug_sides(world)
    assert ship.dyn.tack == "starboard" and sides["main.topsail"] == "larboard"


def test_truth_7b_112_the_frigate_lies_to_under_her_main_staysail_by_the_heavy_weather_book():
    """Package 57 (the owner's finding at gate 6c): the frigate in the gale trial
    (`trial-station-gale`, seed 7), hove to for weather by the captain's book, lies a-try
    under the close-reefed main topsail, the storm staysails as package 37p left them and
    Steel's main staysail ("Lying-to under the main staysail ... a mean between the two
    others", Steel 1794 vol. II); as the wind passes the storm line the main staysail is
    taken in and the storm staysails stand for it ("preferable when it blows strong enough
    for that sail to support the rolling of the ship"), and nothing blows it out. Seven
    hours: her first hove-to of the gale."""
    from tests.test_captain_trials import trial

    world = trial("trial-station-gale", hours=7)
    log = list(world.log)
    hove = [
        e.tick
        for e in log
        if e.kind == "captain.state" and e.data["state"] == "hove to for weather"
    ]
    set_at = [e.tick for e in log if e.text == "Set the main staysail to lie to under."]
    lying = [e.tick for e in log if e.kind == "ship.hove_to"]
    taken = [e.tick for e in log if e.text == "Hauled down the main staysail."]
    assert hove and set_at and lying and taken, (hove, set_at, lying, taken)
    assert hove[0] < set_at[0] <= lying[0] < taken[0]  # lying a-try under it, then in
    ship = world.ship
    assert "hove_to" in ship.extra and ship.extra["hove_to"]["how"] == "a-try"
    assert all(ship.sails[s].is_set for s in ship.groups["storm staysails"])
    assert not ship.sails["main.staysail"].is_set
    assert ship.sails["main.staysail"].state.value != "blown_out"


# Package 56: fishing, and the glass on a near ship (spec M7b §21a to §21c). Truths 7b-105
# to 7b-107. 105 and 106 on the Culloden smack and the business's smack on the seine
# ground in Gerrans Bay at seed 7, an August forenoon, the wind ten knots from the west;
# 107 on the frigate with the Palinure lying to at a mile, at four cables and by night. No
# recorded passage's pin moves by the fishing: the business is off in every one, and a
# ship that carries no gear has no fishery (the digests the tests keep).
# ---------------------------------------------------------------------------


def _gerrans_world(ship="data/ships/smack.yaml", lat=50.195, lon=-4.945, hour=9):
    sc = Scenario(
        start_time=datetime(1805, 8, 14, hour, 0),
        wind_from_deg=270.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        ports=["falmouth", "plymouth"],
        nation="britain",
    )
    return make_world(7, ship, sc)


def _one_shot_of_the_seine(world):
    """The seine shot, an hour fished, hauled: the player's evolutions through the orders."""
    world.submit("shoot the seine")
    while world.fishery.out is None:
        world.run(60)
    while world.fishery.out.fished_s < 3600:
        world.run(60)
    world.submit("haul the seine")
    while world.fishery.out is not None:
        world.run(60)
    caught: dict[str, float] = {}
    for lot in world.fishery.catch.lots:
        caught[lot.fish] = caught.get(lot.fish, 0.0) + lot.tons
    return caught


@pytest.fixture(scope="module")
def gerrans_seine():
    world = _gerrans_world()
    caught = _one_shot_of_the_seine(world)
    return world, caught


def test_truth_7b_105_the_smacks_seine_fills_her_well_the_catch_sells_at_falmouth_and_spoils_kept(
    gerrans_seine,
):
    """Spec M7b §21c, truth 105: "The smack on a pilchard ground in season, the seine
    shot and hauled, fills her well by the ground's yield; the fish sold at Falmouth at
    the market's price; a well kept too long spoils its catch." Gerrans Bay in August by
    day: an hour of the seine takes the ground's three tons of pilchards an hour and its
    ton of mackerel (data/fishing/channel-west.yaml) at ten knots of wind, by the one
    catch function; the well's three tons are filled and the rest goes into the hold; the
    same catch landed at Falmouth's quay sells at the quay's price; kept a day in the
    well, the pilchards there spoil and are said to."""
    import copy

    from freesail.world import fishing as F

    world, caught = gerrans_seine
    ground = F.find_ground(world, "gerrans-bay")
    hour = F.take(ground, "seine", datetime(1805, 8, 14, 10), "day", 10.0, 3600.0)
    assert caught == pytest.approx(hour, rel=1e-6)
    catch = world.fishery.catch
    assert catch.in_well() == pytest.approx(catch.well_tons) == pytest.approx(3.0)
    hauled = [e for e in world.log if e.kind == "fishing.hauled"]
    assert len(hauled) == 1 and "Struck down" in hauled[0].text
    assert "in the well" in hauled[0].text
    # the catch carried into Carrick Road and sold on the quay
    quay = _gerrans_world(lat=50.163, lon=-5.0345)
    quay.submit("let go the best bower")
    quay.run(600)
    quay.fishery.catch = copy.deepcopy(catch)
    for lot in quay.fishery.catch.lots:
        lot.caught_tick = quay.clock.tick
        lot.spoils_tick = None if lot.spoils_tick is None else quay.clock.tick + 3600
    worth = sum(F.price_of(f, False) * t for f, t in caught.items())
    before = quay.purse.pounds
    sold = quay.submit("sell the catch")
    assert sold.kind == "fishing.sold" and "Falmouth" in sold.text
    assert quay.purse.pounds - before == pytest.approx(worth)
    # kept a day: the well's pilchards spoil (a pilchard keeps 24 hours in its water)
    world.run(25 * 3600)
    turned = [e for e in world.log if e.kind == "fishing.spoiled"]
    assert any("in the well" in e.text and "pilchards" in e.text for e in turned)
    assert all(lot.spoiled for lot in world.fishery.catch.lots if lot.fish == "pilchards")


def test_truth_7b_106_the_business_fisherman_on_the_same_ground_brings_home_the_same_catch(
    gerrans_seine,
):
    """Spec M7b §21c, truth 106: "The business's fisherman on the same ground brings home
    the same catch at far detail." A smack of the business on the Gerrans seine ground for
    two hours from Falmouth, the player's frigate twenty miles off (beyond the crewed
    range): her far body shoots the seine by the evolution's own time, fishes an hour by
    the one catch function and hauls, and the catch is the player's to the ounce; she runs
    home, and her catch is landed at Falmouth's quay (the sale in her record)."""
    from freesail.world.ships import vessel_from_spec

    _world, caught = gerrans_seine
    far = _gerrans_world(ship="data/ships/frigate-36.yaml", lat=49.85, lon=-5.2)
    far.vessels.serial += 1
    v = vessel_from_spec(
        far,
        {
            "description": "smack",
            "name": "Brothers",
            "nation": "britain",
            "position": {"lat_deg": 50.195, "lon_deg": -4.945},
            "goal": "bound for Falmouth",
            "intent": "fish on the seine ground in Gerrans Bay for 2 hours from Falmouth",
        },
        far.vessels.serial,
    )
    far.vessels.add(v)
    while v.brain.intent.kind == "fish":
        far.run(60)
    assert v.crew is None and v.fishing is not None
    took: dict[str, float] = {}
    for lot in v.fishing.catch.lots:
        took[lot.fish] = took.get(lot.fish, 0.0) + lot.tons
    assert took == pytest.approx(caught, rel=1e-9)
    for _ in range(24 * 60):
        if v.done:
            break
        far.run(60)
    landed = v.fishing.catch.landed
    assert v.done and landed and landed[0]["port"] == "falmouth"
    home = dict(landed[0]["sold"])
    for fish, tons in landed[0]["spoiled"].items():
        home[fish] = home.get(fish, 0.0) + tons
    assert sum(home.values()) == pytest.approx(sum(caught.values()), rel=1e-3)


def _palinure_at(distance_nm: float, hour: int = 11):
    from freesail.world.geo import destination
    from freesail.world.ships import vessel_from_spec

    world = _gerrans_world(ship="data/ships/frigate-36.yaml", lat=49.80, lon=-5.0, hour=hour)
    where = destination(world.position, 90.0, distance_nm * 1852.0)
    world.vessels.serial += 1
    v = vessel_from_spec(
        world,
        {
            "id": "palinure",
            "description": "brig-sloop",
            "name": "Palinure",
            "nation": "france",
            "position": where.to_dict(),
            "goal": "bound for 49 48 N 4 30 W",
        },
        world.vessels.serial,
    )
    v.plan = [("lie_to", math.inf)]
    world.vessels.add(v)
    world.run(120)
    return world


def test_truth_7b_107_the_glass_on_the_palinure_hove_to_by_tiers_and_by_night():
    """Spec M7b §21c, truth 107: "The glass on the Palinure hove to at a mile says she is
    hove to and on which tack; at four cables the main topsail aback; at night, only her
    light if any." The French brig-sloop lying to east of the frigate, the wind from the
    west: at a mile the glass says she is hove to on the larboard tack and nothing of her
    sails; within four cables the evolution's words, her main topsail aback; by night no
    light shows and nothing of her work is made out. The lookout says the glass unasked
    when she comes within its tiers."""
    world = _palinure_at(1.0)
    e = world.submit("the glass on the brig")
    assert e.kind == "lookout.glass" and "hove to on the larboard tack" in e.text, e.text
    assert "aback" not in e.text
    said = [x for x in world.log if x.kind == "lookout.glass"]
    assert said and "hove to on the larboard tack" in said[0].text
    near = _palinure_at(0.35)
    e = near.submit("the glass on the brig")
    assert "hove to on the larboard tack, main topsail aback" in e.text, e.text
    night = _palinure_at(0.35, hour=23)
    e = night.submit("the glass on the brig")
    assert "no light shows" in e.text and "aback" not in e.text, e.text


# ---------------------------------------------------------------------------
# Package 59: the harbour, the scenario maker and the settings (spec M7b §21d to §21f).
# Truths 7b-108 to 7b-110. The model names are placeholders; the settings, the client's
# file and the scenarios go to a temporary directory; the credential store is the test's.
# ---------------------------------------------------------------------------

PLACEHOLDER_MODEL = "placeholder-model-for-truth-110"  # made up: no model is named here
HARBOUR_ROOT = Path(__file__).resolve().parents[1]


def _harbour_settings(tmp_path, **doors):
    from freesail import settings as S

    path = tmp_path / "player" / "settings.yaml"
    s = S.load_settings(path)
    s["places"]["desktop_config"] = str(tmp_path / "Claude" / "claude_desktop_config.json")
    s["places"]["consent_records"] = str(tmp_path / "consent")
    for door, values in doors.items():
        s["doors"][door].update(values)
    S.save_settings(s, path)
    return path


def test_truth_7b_108_py_m_freesail_opens_the_harbour_and_shows_a_started_game_and_the_doors(
    tmp_path,
):
    """Spec M7b §21f, truth 108: "`py -m freesail` opens the harbour, a game is started
    from it with a seat and a director's brief, and the doors' states are shown true." The
    launcher run as the owner runs it (its own process, the browser not opened): the game's
    page leads to the harbour; a game started there with the officer's seat and the
    dispatches brief, the clock held; the desktop client's entries for the captain and the
    director written and shown present; a local runner started with nobody serving its
    model shown ended with its exit code, and the player shown at his station."""
    import os
    import socket
    import subprocess
    import time

    httpx = pytest.importorskip("httpx")
    pytest.importorskip("fastapi")
    settings = _harbour_settings(tmp_path, local={"endpoint": "http://127.0.0.1:9"})
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "freesail",
            "--no-browser",
            "--port",
            str(port),
            "--settings",
            str(settings),
        ],
        cwd=str(tmp_path),  # from anywhere: the launcher goes to the game's folder
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, "PYTHONPATH": str(HARBOUR_ROOT)},
    )
    url = f"http://127.0.0.1:{port}"
    try:
        with httpx.Client(base_url=url, timeout=60) as c:
            deadline = time.monotonic() + 60
            while True:
                try:
                    first = c.get("/", follow_redirects=False)
                    break
                except httpx.TransportError:
                    assert proc.poll() is None and time.monotonic() < deadline
                    time.sleep(0.2)
            assert first.status_code == 307 and first.headers["location"] == "/harbour"
            assert "the harbour" in c.get("/harbour").text
            r = c.post(
                "/api/harbour/start",
                json={
                    "scenario": "data/scenarios/dispatches-falmouth.yaml",
                    "seat": "officer",
                    "director_brief": "dispatches",
                },
            )
            assert r.status_code == 200, r.text
            game = r.json()["game"]
            assert game["started"] and not game["running"]
            assert game["seat"] == "the player at the officer of the watch's station"
            assert game["director"] == "The dispatches"
            written = c.post(
                "/api/harbour/desktop", json={"stations": ["captain", "director"], "write": True}
            ).json()
            assert written["written"]
            d = c.post("/api/harbour/doors", json={"door": "local", "station": "captain"}).json()
            assert d["state"] == "running"
            deadline = time.monotonic() + 60
            while c.get(f"/api/harbour/doors/{d['id']}").json()["state"] == "running":
                assert time.monotonic() < deadline
                time.sleep(0.2)
            state = c.get("/api/harbour/state").json()
            assert state["desktop"]["entries"] == ["freesail-captain", "freesail-director"]
            (door,) = state["doors"]
            assert door["state"] == "ended" and door["code"] == 2
            assert door["words"] == "The local runner at the captain: ended (exit code 2)."
            assert [(s["station"], s["holder"]) for s in state["stations"]] == [
                ("officer of the watch", "the player")
            ]
            assert c.get("/", follow_redirects=False).status_code == 200
    finally:
        proc.terminate()
        out, _ = proc.communicate(timeout=30)
    assert f"FreeSail harbour. Open http://localhost:{port}/harbour" in out
    assert "held until the driver says go" in out


def test_truth_7b_109_a_scenario_by_the_maker_loads_as_a_hand_made_one_and_reads_back_unchanged(
    tmp_path,
):
    """Spec M7b §21f, truth 109: "A scenario written by the maker loads in the console and
    the server as a hand-made one does, and reads back into the form unchanged." The
    owner's smack out of Falmouth written by the maker as a new file (its fields alone, in
    the maker's own words): at the console's start and the server's, its World is the
    hand-made file's, the same Scenario and the same log over ten minutes (the anchor let go,
    the business drawn about her); read back into the
    form and written again, the same bytes; and the hand-made file itself read into the
    form and written with nothing changed is itself."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.core.world import Scenario, World
    from freesail.ui.console import start_world
    from freesail.ui.harbour import Harbour
    from freesail.ui.server import Driver, create_app, prepare_game, server_parser
    from freesail.world.scenarios import begin

    settings = _harbour_settings(tmp_path)
    driver = Driver(World(seed=1805, scenario=Scenario()))
    app = create_app(driver, harbour=Harbour(driver, settings_path=settings))
    hand = HARBOUR_ROOT / "data" / "scenarios" / "smack-falmouth.yaml"
    with TestClient(app) as c:
        got = c.get("/api/harbour/scenario", params={"path": "data/scenarios/smack-falmouth.yaml"})
        fields = got.json()["fields"]
        made = c.post("/api/harbour/scenario", json={"fields": fields, "name": "smack"}).json()
        path = Path(made["path"])
        text = path.read_text(encoding="utf-8")
        assert text != hand.read_text(encoding="utf-8")  # the maker's own words
        assert text.startswith("# FreeSail: A smack out of Falmouth.")

        def console(p: Path) -> World:
            world, sf = start_world(server_parser().parse_args(["--scenario", str(p)]))
            begin(world, sf)
            world.run(600)
            return world

        def server(p: Path) -> World:
            world = prepare_game(
                server_parser().parse_args(["--scenario", str(p)]), say=lambda line: None
            )
            world.run(600)
            return world

        for drive in (console, server):
            a, b = drive(hand), drive(path)
            assert a.scenario.__dict__ == b.scenario.__dict__
            assert a.log.digest() == b.log.digest(), drive.__name__
        # read back into the form and written again: unchanged
        back = c.get("/api/harbour/scenario", params={"path": str(path)}).json()
        c.post(
            "/api/harbour/scenario",
            json={"fields": back["fields"], "source": str(path), "name": "smack"},
        )
        assert path.read_text(encoding="utf-8") == text
        # and the hand-made one, written from the form with nothing changed, is itself
        again = c.post(
            "/api/harbour/scenario",
            json={"fields": fields, "source": "data/scenarios/smack-falmouth.yaml", "name": "hand"},
        ).json()
        assert Path(again["path"]).read_bytes() == hand.read_bytes()


def test_truth_7b_110_the_settings_hold_no_key_and_a_models_name_in_them_reaches_no_save_or_log(
    tmp_path, monkeypatch
):
    """Spec M7b §21f, truth 110: "The settings file holds no key; the credential store does;
    a model's name in it never enters the repository, a save or a log." The key in the
    (test's) credential store: the settings refuse it in any field, and the harbour says
    only that the store holds one. The model's name in the settings at every door: kept in
    the settings file (outside the repository, which refuses a settings file inside it) and
    the desktop client's file (likewise); a game started from the harbour and saved, its
    log and its save hold no word of it; nor does anything the harbour says."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from messages_api import fake_store

    from freesail import settings as S
    from freesail.agents.api import KEYRING_ACCOUNT, KEYRING_SERVICE
    from freesail.core.world import Scenario, World
    from freesail.ui.harbour import Harbour
    from freesail.ui.server import Driver, create_app

    store = fake_store(monkeypatch)
    key = "a-test-key-of-no-account-0123456789"
    store.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, key)
    path = _harbour_settings(
        tmp_path,
        desktop={"model_name": PLACEHOLDER_MODEL},
        api={"model": PLACEHOLDER_MODEL},
        local={"model": PLACEHOLDER_MODEL},
    )
    kept = path.read_text(encoding="utf-8")
    assert PLACEHOLDER_MODEL in kept and key not in kept
    assert not S.inside_repository(path)
    with pytest.raises(S.SettingsError):
        S.save_settings(S.load_settings(path), HARBOUR_ROOT / "settings.yaml")
    for where in (("doors", "api", "effort"), ("doors", "api", "key")):
        s = S.load_settings(path)
        s[where[0]][where[1]][where[2]] = key
        with pytest.raises(S.SettingsError):
            S.save_settings(s, path)
    assert path.read_text(encoding="utf-8") == kept
    driver = Driver(World(seed=1805, scenario=Scenario()))
    app = create_app(driver, harbour=Harbour(driver, settings_path=path))
    said: list[str] = []
    with TestClient(app) as c:
        said.append(c.get("/api/harbour/state").text)
        assert "is in the credential store" in said[-1]
        r = c.post(
            "/api/harbour/start",
            json={"scenario": "data/scenarios/directed-passage.yaml", "seat": "director"},
        )
        said.append(r.text)
        d = c.post("/api/harbour/desktop", json={"stations": ["captain"], "write": True}).json()
        assert PLACEHOLDER_MODEL in Path(d["path"]).read_text(encoding="utf-8")
        assert not S.inside_repository(d["path"])
        c.post("/api/driver", json={"action": "tick", "value": 600})
        save = tmp_path / "game.json"
        c.post("/api/driver", json={"action": "save", "value": str(save)})
        said.append(c.get("/api/log", params={"limit": 5000}).text)
        said.append(c.get("/api/harbour/state").text)
        said.append(c.get("/api/save").text)
    assert save.exists()
    for words in [save.read_text(encoding="utf-8"), *said]:
        assert PLACEHOLDER_MODEL not in words and key not in words
    assert key not in Path(d["path"]).read_text(encoding="utf-8")


# Package 62: the director's hand (spec M7b §3; the owner's proposal of 2026-10-18). Truth
# 7b-113, numbered after 7b-112: an order of a ship's own grammar given by the director to
# her captain's station as his own, far and crewed, and refused where a model holds him.
# ---------------------------------------------------------------------------


def test_truth_7b_113_the_hand_brings_a_far_trader_to_heaves_a_crewed_cruiser_to_and_is_refused():
    """Spec M7b §3 and package 62's truth: "at seed 7 with the business on, the director's
    `ship "X": order heave to` brings a far trader to, her log saying it as her captain's
    and the play log of the player's ship showing only what the lookout sees, and the same
    order to a crewed cruiser heaves her to under her captain's domain, and is refused where
    a fake captain holds her." The schooner off the Lizard with the business on (seed 7), a
    King's brig-sloop on her station two miles off and promoted; a fake director on the
    dispatches brief gives each its captain's heave-to: the business's trader, at far
    detail a hundred miles off, lies to, her story saying it as her captain's; the cruiser's
    own World takes it as her captain's order under his rules' actor, his book struck, and
    she heaves to; the player's log carries no order, only the lookout's lines of the
    cruiser; a fake captain then seated on the cruiser, the same order is refused in words
    and logged so."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents import director as D
    from freesail.agents.agent import captain
    from freesail.agents.fake import captain_of_the_ship, director_above_the_game
    from freesail.core.events import for_the_record
    from tests.test_brains import put
    from tests.test_business import world_with
    from tests.test_director import seat_director

    world = world_with("on")
    assert world.seed == 7 and world.business is not None
    trader = next(
        v
        for v in world.vessels.vessels
        if v.brain is not None
        and v.brain.role == "merchant"
        and v.detail == "far"
        and v.plan
        and v.plan[0][0] == "to"
    )
    cruiser = put(
        world,
        "brig-sloop",
        "britain",
        "50 02 N 4 58 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    world.submit("heave to")
    D.set_brief(world, "dispatches", source="the truth")
    world.run(61)
    crew = cruiser.crew
    assert crew is not None and crew.shape == "full" and crew.captain.role == "cruiser"
    hand = f'ship "{trader.name}": order heave to'
    seat_director(world, director_above_the_game([hand, 'ship "Hazard": order heave to']))
    world.run(1300)
    texts = [e.text for e in D.log_of(world).entries]
    assert any(t.startswith(f"Given: {hand};") for t in texts)
    assert any(t.startswith('Given: ship "Hazard": order heave to;') for t in texts)
    # the far trader brought to, her log (the far body's story) saying it as her captain's
    assert trader.plan[0][0] == "lie_to" and trader.sail_state == "lying to"
    assert trader.speed_kn == pytest.approx(0.0, abs=0.1)
    assert [s for _t, s in trader.story] == ["By the captain: heaving to."]
    # the crewed cruiser hove to by her captain's order, his book struck, his rule's actor
    said = [e for e in crew.log if e.text == "By the captain: heaving to."]
    assert len(said) == 1 and str(said[0].actor).startswith("captain's rule")
    assert crew.readings.value("manoeuvre_in_hand") == "hove to"
    assert crew.captain.over_head_order == "heave to" and not crew.captain.commands
    # the player's log: nothing of the orders, the cruiser only as the lookout sees her
    play = [e for e in world.log.all() if not for_the_record(e)]
    assert not [e for e in play if "By the captain" in e.text or trader.name in e.text]
    seen = [e for e in play if "brig" in e.text.lower() and e.tick > 61]
    # package 71: the King's cruiser makes the private signal to us, which the lookout
    # reports under the signal kinds (`signal.private`): his observation, no order of hers
    assert seen and all(e.kind.startswith(("lookout.", "signal.")) for e in seen)
    assert any("hove to" in e.text or "heaving to" in e.text for e in seen)
    # a fake captain at her captain's station: the same order refused in words
    held = Harness(
        crew,
        captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=crew),
        captain_of_the_ship([]),
        save=lambda w, why: None,
    )
    held.model_name, held.door = "the fake captain", "mcp"
    held.start()
    said = D.direct(world, 'ship "Hazard": order heave to', by="the fake director")
    assert said.startswith("Refused, by the rule of reach: Hazard's captain (")
    assert "is held by a model" in said and "write to him instead" in said
    assert D.log_of(world).entries[-1].kind == "director.refused"
    assert len([e for e in crew.log if e.text == "By the captain: heaving to."]) == 1


# Package 53b: things, free lines and transactions (spec M7b §17a; the owner's question of
# 2026-10-19 after the dispatches test). Truths 7b-114 to 7b-116. The schooner at seed 7 at
# anchor in Carrick Road (`tests/test_orders_places.in_falmouth`), the player at the prompt
# as her master who commands, the director's orders given at his door as the player's
# seat gives them (an input of its own, replayed through the door). No recorded passage's
# pin moves: none has a thing, a free line or a payment by the channel.
# ---------------------------------------------------------------------------


def _veale_at_falmouth(port: str = "Falmouth"):
    from freesail.agents import director as D
    from tests.test_orders_places import in_falmouth

    world = in_falmouth()
    said = D.direct(
        world, f'person: make "Mr Veale", a clerk, ashore at {port}', by="the truth", road=D.INPUT
    )
    assert said.startswith("Done:"), said
    return world


def test_truth_7b_114_a_thing_made_in_the_cabin_is_given_ashore_by_a_free_line_and_kept(
    tmp_path,
):
    """Spec M7b §17a and package 53b's truth: "a thing made by the director in the cabin is
    given by the captain to a person ashore by a free line when he is there, is in that
    person's keeping in the people's reading and the truth, and stays there through a save
    and a replay." The director makes the packet on the cabin table and Mr Veale at the
    counting house; the master who commands goes below, takes it, goes ashore by the boat
    with it in his keeping, walks to the counting house and gives it to Mr Veale; the
    people's reading and the truth say it is his; the save replays to the same log and
    the same things, and a checkpoint holds them."""
    from freesail.agents import director as D
    from freesail.api.readings import director_readings
    from freesail.api.session import ship_factory
    from freesail.core import replay
    from freesail.world import things as TH
    from tests.test_orders_places import until

    world = _veale_at_falmouth()
    said = D.direct(
        world,
        "aboard: a sealed packet, on the cabin table, from the Custom House",
        by="the truth",
        road=D.INPUT,
    )
    assert said.startswith("Done: a sealed packet (from the Custom House) made, on the table")
    (packet,) = TH.things_of(world)
    master = world.people.captain
    veale = world.people.find("Mr Veale")
    # from the deck the packet is out of his reach: said, and nothing moves
    e = world.submit("give the packet to Mr Veale")
    assert e.kind == "free.line" and "as said; nothing of the ship's changed" in e.text
    assert packet.place == "cabin" and not packet.keeper
    world.submit("go below")
    assert world.submit("take the packet").data["moved"]
    world.submit("come on deck")
    world.submit("go ashore")
    until(world, lambda: master.where == "shore" and not world.dealings.boat.away)
    assert packet.keeper == master.id and TH.place_of(world, packet)[0] == "shore"
    world.submit("go to the counting house")
    e = world.submit("give the packet to Mr Veale")
    assert e.kind == "free.line" and e.data["moved"] and e.data["to"] == "Mr Veale"
    assert e.text == (
        "By the captain, ashore at Falmouth, at the counting house: gave the packet to Mr "
        "Veale; the sealed packet is in Mr Veale's keeping."
    )
    assert packet.keeper == veale.id
    keeping = (
        "Mr Veale, clerk: ashore at Falmouth, at the counting house, a sealed packet in his "
        "keeping."
    )
    assert keeping in world.people.describe() and keeping in world.readings.words("people")
    truth = director_readings(world)
    assert keeping in truth["people"][world.ship.name]
    assert truth["things"] == [
        "a sealed packet, in Mr Veale's keeping, ashore at Falmouth, at the counting house"
    ]
    world.run(600)
    # the save and the replay: the same log, the same things where they were
    back = replay.replay_world(world, ship_factory)
    assert back.log.digest() == world.log.digest()
    assert [t.to_dict() for t in TH.things_of(back)] == [t.to_dict() for t in TH.things_of(world)]
    assert keeping in back.people.describe()
    path = replay.write_checkpoint(world, tmp_path / "packet.ckpt")
    _, held = replay.read_checkpoint(path)
    assert [t.to_dict() for t in TH.things_of(held)] == [t.to_dict() for t in TH.things_of(world)]


def test_truth_7b_115_a_free_line_naming_nothing_known_is_as_said_and_eat_and_drink_as_before():
    """Package 53b's truth: "a free line that names nothing known is logged 'as said;
    nothing of the ship's changed' and moves nothing, and `eat` and `drink` log as before."
    Each of the free verbs said of nothing the world knows is a notable line in the words
    as used ending in those words, journaled, the ship's state the same after them; `eat a
    fine meal` and `drink three cups of wine` are answered to him alone and are no line of
    the log, the words kept in the record."""
    from freesail.world import things as TH

    world = _veale_at_falmouth()
    world.world_order("aboard: a cask of brandy, in the hold", "the truth")
    before = (
        [t.to_dict() for t in TH.things_of(world)],
        world.purse.pounds,
        dict(world.hold.goods),
        world.people.describe(),
    )
    lines = (
        "give the letter to the pilot",
        "hand the dispatches to Mr Veale",
        "show the chart to Mr Veale",
        "take the cutlass",
        "stow the spyglass in the hold",
        "hide the letter in the bread locker",
        "put the purse on the table",
        "open the sea chest",
        "read the letter",
        "throw the empty bottle overboard",
    )
    for words in lines:
        e = world.submit(words)
        assert e.kind == "free.line" and e.severity.value == "notable", words
        assert e.text.endswith("as said; nothing of the ship's changed."), e.text
        assert not e.data["moved"]
    assert e.text == (
        "By the captain, on the quarterdeck: threw the empty bottle overboard, as said; "
        "nothing of the ship's changed."
    )
    after = (
        [t.to_dict() for t in TH.things_of(world)],
        world.purse.pounds,
        dict(world.hold.goods),
        world.people.describe(),
    )
    assert after == before
    assert [t for _, a, t in world.journal if a == "captain"][-len(lines) :] == list(lines)
    n = len(world.log)
    assert world.submit("eat a fine meal").kind == "needs.answer"
    assert world.submit("drink three cups of wine").kind == "needs.answer"
    assert len(world.log) == n
    said = [x.get("order") for x in world.inputs]
    assert "eat a fine meal" in said and "drink three cups of wine" in said


def test_truth_7b_116_a_sum_paid_by_mr_veale_is_credited_doubted_far_off_refused_below_nothing():
    """Package 53b's truth: "`aboard: twenty guineas paid into the purse by Mr Veale` with
    Mr Veale ashore at the ship's port credits the purse with the ledger's line, is doubted
    with him thirty miles off, and a payment below nothing is refused." At Falmouth the
    director's order is not doubted, the purse gains £21 and its ledger says by whom with
    the purse after; in the same water with Mr Veale made at Plymouth instead, thirty miles
    off, the same order is doubted and nothing is paid; a sum paid from the purse beyond
    what it holds is refused and the purse is what it was."""
    from freesail.agents import director as D
    from freesail.core.events import for_the_record
    from freesail.world.places import pounds_words

    world = _veale_at_falmouth()
    purse = world.purse.pounds
    order = "aboard: twenty guineas paid into the purse by Mr Veale"
    said = D.direct(world, order, by="the truth", road=D.INPUT)
    assert said.startswith("Done: twenty guineas (£21) paid into the purse by Mr Veale")
    assert world.purse.pounds == pytest.approx(purse + 21.0)
    now = pounds_words(world.purse.pounds)
    assert world.purse.ledger_lines() == [
        f"Paid by Mr Veale, twenty guineas (£21); the purse {now}."
    ]
    seen = [e for e in world.log.all() if e.kind == "purse.received"]
    assert [e.text for e in seen] == [
        f"Paid into the purse by Mr Veale, twenty guineas (£21); the purse {now}."
    ]
    assert not for_the_record(seen[0])
    assert D.log_of(world).entries[-1].kind == "director.order"
    # thirty miles off: Mr Veale at Plymouth, the schooner in Carrick Road
    far = _veale_at_falmouth("Plymouth")
    miles = far.ports.ports["plymouth"].nearest_spot(far.position)[1]
    assert 25.0 < miles < 40.0
    was = far.purse.pounds
    said = D.direct(far, order, by="the truth", road=D.INPUT)
    assert said.startswith("Doubted, not performed: Mr Veale is ashore at Plymouth")
    assert f"{miles:.0f} miles off" in said and "neither aboard nor at a port" in said
    assert far.purse.pounds == was and far.purse.ledger_lines() == []
    assert D.log_of(far).entries[-1].kind == "director.doubted"
    # below nothing: refused, the purse what it was
    held = world.purse.pounds
    e = world.world_order(f"aboard: £{held + 1:.0f} paid from the purse to Mr Veale", "the truth")
    assert e.data["result"] == "refused"
    assert e.text.endswith(
        f"the purse holds {pounds_words(held)}, not {pounds_words(float(f'{held + 1:.0f}'))}: "
        "nothing is paid below nothing."
    )
    assert world.purse.pounds == held and len(world.purse.ledger_lines()) == 1


# Package 66: the station's line and the stand-by (the dispatches test, 2026-10-18, and the
# captain's debrief). Truths 7b-117 to 7b-119, numbered after 53b's 7b-114 to 7b-116: the
# line that opens every sample, the stand-by ended by the model's own order and not woken
# by a word out of its hearing, and the hand's hold named until an event.
# ---------------------------------------------------------------------------


def _captain_ashore_world():
    """The schooner at anchor in Carrick Road (`test_orders_places.in_falmouth`), a clerk
    made ashore at Falmouth's counting house, and a captain's station held by a door that
    answers late (its replies delivered here, as a remote door's are)."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import captain
    from freesail.agents.fake import Transcript
    from tests.test_orders_places import in_falmouth

    world = in_falmouth()
    world.world_order('person: make "Mr Veale", a clerk, ashore at Falmouth', "the truth")
    h = Harness(
        world,
        captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        Transcript([]),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "a late door", "mcp"
    h.start()
    world.run(1)
    return world, h


def _until(world, test, step=60, most=240):
    for _ in range(most):
        if test():
            return
        world.run(step)
    raise AssertionError("never came")


def test_truth_7b_117_the_first_line_of_a_captains_sample_names_his_place_the_deck_and_his_state():
    """Spec M7b §14 ("The always-present line") and package 66's truth 117: "the first line
    of a captain's sample names his place, the deck and his state, ashore and aboard, and
    changes when he moves." The captain's first sample opens with the line on the
    quarterdeck; he goes ashore, and the sample after the landing says him ashore at
    Falmouth on the quay since he landed; he comes aboard, and it says him aboard again;
    his `how am I` answers with the same line."""
    from freesail.agents.fake import call, reply

    world, h = _captain_ashore_world()
    cap = world.people.captain

    def line():
        sample = h.open_sample
        assert sample is not None and sample.to_dict()["you"] == sample.you
        assert list(sample.to_dict())[0] == "you"
        return sample.you

    # the line closes with the date (the owner's fourth note of the playtests of 70 to 72)
    assert line() == (
        "You: the captain, on the quarterdeck, since 10:00; the deck yours; on your feet "
        "since 10:00; Monday 10 June 1805."
    )
    h.deliver(reply("", call("submit_order", text="go ashore")))
    h.deliver(reply("", call("stand_by", until="a glass")))
    _until(world, lambda: not h.agent.standing_by)
    assert cap.where == "shore"
    landed = next(e for e in world.log if e.kind == "person.ashore")
    at = landed.ship_time.strftime("%H:%M")
    # package 58a: the line closes with the ship's time since his last reply, a glass's
    # stand-by being thirty minutes ("...; on your feet since 10:00." before)
    assert line() == (
        f"You: the captain, ashore at Falmouth, on the quay, since {at}; the deck yours; on "
        "your feet since 10:00; Monday 10 June 1805; 30 minutes of the ship's time since "
        "your last reply."
    )
    _until(world, lambda: not world.dealings.boat.away)  # the boat home, to be sent for him
    h.deliver(reply("", call("submit_order", text="come aboard")))
    h.deliver(reply("", call("stand_by", until="a glass")))
    _until(world, lambda: not h.agent.standing_by)
    assert line().startswith("You: the captain, in the boat, since ")  # pulling off to her
    _until(world, lambda: cap.aboard)
    h.deliver(reply("", call("stand_by", until="a glass")))
    _until(world, lambda: not h.agent.standing_by)
    assert line().startswith("You: the captain, on the quarterdeck, since ")
    h.deliver(reply("", call("submit_order", text="how am I")))
    said = h.turns[-1].content["tool_results"][-1]["result"]
    assert said.startswith("You: the captain, on the quarterdeck, since ") and "\nYou are " in said


def test_truth_7b_118_an_order_ends_its_own_stand_by_and_a_word_out_of_earshot_wakes_nobody():
    """Package 66's truth 118: "an order given while standing by ends the stand-by and runs,
    and a word said out of a station's earshot does not wake it." The captain ashore stands
    by; his order to go to the counting house, sent while he stands by (a remote door's
    reply out of turn), ends the stand-by at his own word, logged so, and runs; the clerk's
    words there are heard by him and the result says so; at the market, standing by for a
    word on deck or a notable event, the clerk's words at the counting house (the empty
    wake of 15:44) do not wake him, and the director's result says nobody heard them and
    where the captain is. The save replays to the same log."""
    import json

    from freesail.agents.fake import call, reply
    from freesail.agents.remote import Desk
    from freesail.api.session import ship_factory
    from freesail.core import replay

    world, h = _captain_ashore_world()
    cap = world.people.captain
    h.deliver(reply("", call("submit_order", text="go ashore")))
    h.deliver(reply("", call("stand_by", until="a glass")))
    _until(world, lambda: cap.where == "shore" and not h.agent.standing_by)
    h.deliver(reply("", call("stand_by", until="a glass")))
    world.run(60)
    assert h.agent.standing_by
    out = Desk._own_act(h, reply("", call("submit_order", text="go to the counting house")))
    assert out["words"].startswith("Your stand-by (until a glass) ended at your own order")
    assert not h.agent.standing_by and h.open_sample is not None
    ended = [e for e in world.log if e.kind == "agent.resumed"][-1]
    assert ended.text.endswith(
        "ends its stand-by (until a glass) at its own word; it is sampled again."
    )
    assert cap.ashore_at == "counting_house"
    h.deliver(reply("", call("submit_order", text="say Mr Veale? A packet for your hand, sir.")))
    result = h.turns[-1].content["tool_results"][-1]["result"]
    assert result.endswith("Heard by Mr Veale, ashore at Falmouth, at the counting house.")
    h.deliver(reply("", call("stand_by", until="a word on deck")))
    said = world.world_order('say as Mr Veale: "Give it me, sir."', "the truth")
    assert "heard by the captain, ashore at Falmouth, at the counting house" in said.text
    world.run(2)
    assert not h.agent.standing_by  # heard: his word on deck
    h.deliver(reply("", call("submit_order", text="go to the market")))
    h.deliver(reply("", call("stand_by", until="a word on deck or a notable event")))
    said = world.world_order('say as Mr Veale: "And the tin, sir?"', "the truth")
    assert said.text.endswith("heard by nobody: the captain is ashore at Falmouth, at the market.")
    spoke = [e for e in world.log if e.kind == "person.spoke"][-1]
    assert spoke.data["heard_by"] == []
    world.run(120)
    assert h.agent.standing_by  # out of his earshot: no wake, and no empty sample
    copy = replay.replay(json.loads(json.dumps(world.save())), ship_factory)
    assert copy.log.digest() == world.log.digest()


def test_truth_7b_119_the_hand_held_until_a_sail_within_hail_holds_past_the_glass_and_ends_at_it():
    """Spec M7b §3 and package 66's truth 119: "the hand held `until a sail within hail`
    holds past the glass and ends at the hail." A King's brig-sloop at far detail some
    twenty miles off, told by the director's hand to heave to until a sail within hail:
    she lies to past the glass and past two; a brig coming within two cables of her ends
    the hold, and her captain takes up his plan again, her story saying so."""
    from tests.test_brains import put
    from tests.test_world_orders import world_for

    world = world_for(ports=["falmouth"])
    world.submit("heave to")
    v = put(
        world,
        "brig-sloop",
        "britain",
        "49 30 N 5 50 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    world.run(60)
    e = world.world_order('ship "Hazard": order heave to until a sail within hail', "the truth")
    assert e.data["result"] == "done" and "until a sail within hail comes to her" in e.text
    world.run(2 * 1800 + 60)
    assert v.detail == "far" and v.plan[0][0] == "lie_to" and v.sail_state == "lying to"
    assert v.brain.over_head is not None and v.brain.over_head["event"] == "hail"
    brig = put(world, "merchant brig", "britain", "49 30 N 5 50 W", "bound for Falmouth", name="B")
    brig.position = v.position.advanced(0.0, 0.2 * units.NAUTICAL_MILE)
    world.run(180)
    assert v.brain.over_head is None and v.plan[0][0] != "lie_to"
    assert v.story[-1][1].startswith("The captain takes up his plan again")


# Package 68: the review's mending (the cold review of 2026-10-22, `docs/playtests/
# 2026-10-18-to-22-owner-playtests-and-review/`). Truths 7b-120 to 7b-123, numbered after
# 66's 7b-117 to 7b-119: riding means riding (R-01), the officer's word to a player captain
# (R-13, R-14), the lugger weighing as a lugger (R-45), and the brief's enemy limit
# enforced by the channel (R-38; the gate's: spec M7b §4's "enforced by the channel, not
# trusted to the model").
# ---------------------------------------------------------------------------


def test_truth_7b_120_let_go_at_seven_knots_off_a_beach_the_account_runs_and_the_lookout_cries():
    """Package 68's truth 120 (R-01; the grounding at Horta, D5-29): "let go at seven knots
    a mile off a beach; the account advances; the lookout cries urgent before she strikes."
    The cutter under plain sail at seven knots, standing north for the shore west of
    Pendennis, lets go her best bower a mile off: the anchor drags, she sails it home, and
    she is not riding. The master's account runs with her (before, it froze at the
    let-go), and the lookout's land ahead cries urgent before she takes the ground (before,
    muted by any anchor down)."""
    from freesail.world.geo import bearing_and_distance
    from freesail.world.lookout import riding

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=18.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        ship_speed_kn=7.0,
        position={"lat_deg": 50.10, "lon_deg": -5.065},
        region="channel-west",
    )
    w = make_world(7, "data/ships/cutter.yaml", sc)
    w.submit("set plain sail")
    w.run(600)
    assert units.ms_to_knots(w.ship.dyn.speed) > 6.5
    let_go_at = w.position
    account_then = w.navigation.account_now()
    e = w.submit("let go the best bower")
    assert e.kind == "order.accepted", e.text
    let_go_tick = w.clock.tick
    w.run(180)
    assert w.at_anchor and not riding(w.ship)  # an anchor down, and not holding her
    for _ in range(40 * 60):
        w.run(1)
        if w.ship.extra.get("aground"):
            break
    strike = [x for x in w.log if x.kind == "ship.aground"]
    assert strike and w.ship.extra.get("aground")
    run_nm = bearing_and_distance(let_go_at, w.position)[1] / units.NAUTICAL_MILE
    assert 1.0 < run_nm < 2.5  # sailed her anchor home a mile and more
    account_nm = bearing_and_distance(account_then, w.navigation.account_now())[1]
    assert account_nm / units.NAUTICAL_MILE > 0.5 * run_nm  # the account ran with her
    ahead = [
        x for x in w.log if x.kind == "lookout.land_ahead" and let_go_tick < x.tick < strike[0].tick
    ]
    assert [x.severity for x in ahead][-1] is Severity.URGENT, [x.text for x in ahead]
    assert ahead[-1].text.startswith("Land close ahead")


def test_truth_7b_121_the_officers_word_to_the_player_captain_reaches_him_whole_as_the_officers():
    """Package 68's truth 121 (R-13, R-14): "'say to the captain, no land in sight yet' from
    a model officer with the player at the prompt reaches him whole and is logged as the
    officer's." The frigate's officer of the watch, a scripted model with the deck, says
    it, and says "land ho" to the captain by his name: each a notable line of the play log
    under the officer's mark and place, every word kept; nothing kept in a journal for
    nobody; and the game replays to the same log."""
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer
    from freesail.agents.journal import WORD_KEPT_KIND
    from freesail.api.session import ship_factory
    from freesail.core import replay
    from freesail.world.orders import held_stations

    w = make_world(
        7,
        "data/ships/frigate-36.yaml",
        Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0),
    )
    cap = w.people.captain
    script = [
        reply("", call("submit_order", text="say to the captain, no land in sight yet")),
        "",
        reply("", call("submit_order", text=f"Say to Mr {cap.surname}, land ho, sir")),
        "",
    ]
    h = Harness(
        w, officer(SamplingPolicy.in_lockstep(600), world=w), Fake(script), save=lambda *a: None
    )
    assert w.submit("you have the deck").kind == "agent.deck"
    h.start()
    w.run(1800)
    held = [st for st, _p, who in held_stations(w) if who == "the player at the prompt"]
    assert held == ["captain"]
    told = [e for e in w.log if e.kind == "agent.told" and e.actor == "the officer of the watch"]
    person = w.stations.holder("officer of the watch").name
    assert [e.text for e in told] == [
        f"The officer of the watch ({person}), on the quarterdeck, to the captain: no land in "
        "sight yet",
        f"The officer of the watch ({person}), on the quarterdeck, to the captain: land ho, sir",
    ]
    assert all(e.severity is Severity.NOTABLE for e in told)
    assert not any("The captain to the captain" in e.text for e in w.log)
    kept = (w.agent_journals or {}).get("captain")
    assert kept is None or not [x for x in kept.entries if x.kind == WORD_KEPT_KIND]
    copy = replay.replay(json.loads(json.dumps(w.save())), ship_factory)
    assert copy.log.digest() == w.log.digest()


def test_truth_7b_122_the_eclair_weighs_and_makes_way_under_her_lugs_without_being_taken_aback():
    """Package 68's truth 122 (R-45: the Éclair got under way with a square-rigger's words,
    no lug set, under the jib alone a cable off Pergueridre, twice): "the Éclair weighs and
    makes way without being taken aback." At anchor in nine fathoms off Falmouth, the wind
    ahead at twelve knots, `get under way`: the windlass and no hand aloft; the fore lug
    hoisted at the aweigh on the casting tack's lee side with the jib aback; the main lug
    and the mizen when she has cast; under way under her lugs and making five knots and
    more, and no line in the whole of it says she is aback."""
    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
        position={"lat_deg": 50.133, "lon_deg": -5.035},
        region="channel-west",
    )
    w = make_world(7, "data/ships/lugger.yaml", sc)
    assert w.ship.name == "Éclair"
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(20 * 60)
    assert w.at_anchor
    start = len(w.log)
    e = w.submit("get under way")
    assert e.kind == "order.accepted", e.text
    w.run(40 * 60)
    lines = list(w.log)[start:]
    said = " ".join(x.text for x in lines)
    assert (
        "Man the windlass" in said
        and "sail-loosers" not in said
        and "aloft" not in said.replace("no hand aloft", "")
    )
    hoist = [x for x in lines if x.text.startswith("Hoist away the foresail, to larboard!")]
    aweigh = [x for x in lines if x.kind == "ship.aweigh"]
    assert hoist and aweigh and hoist[0].tick == aweigh[0].tick
    under_way = [x for x in lines if x.kind == "ship.under_way"]
    assert under_way and under_way[0].text.startswith(
        "Under way on the starboard tack, under the foresail, the mainsail, the mizen and the jib"
    )
    set_now = {s.id for s in w.ship.sails.values() if s.is_set}
    assert {"fore.lug", "main.lug", "mizen.lug", "jib"} <= set_now
    assert all(w.ship.sails[i].lug_side == "larboard" for i in ("fore.lug", "main.lug"))
    assert units.ms_to_knots(w.ship.dyn.speed) > 5.0
    assert not [x for x in lines if "aback" in x.text.lower() or x.kind == "sail.aback"]


def test_truth_7b_123_no_enemy_heavier_than_a_brig_refuses_a_frigate_and_lets_a_brig_through():
    """Package 68's truth 123 (R-38; spec M7b §4: the brief's limits "enforced by the
    channel, not trusted to the model"): the brief's "no enemy heavier than a brig" refused
    nothing, no key of the ranking fitting inside "brig", and a French frigate passed the
    dispatches', the chase's and the interesting passage's briefs. Under the chase's brief
    a French frigate is refused as outside the brief, with the limit named, and logged so;
    a French brig-sloop and a lugger pass the limit; a British frigate is no enemy."""
    from freesail.agents import director as D
    from tests.test_director import directed, log_kinds

    w = directed("chase", systems=[], climatology=True)
    frigate = 'ship: a frigate "Vengeance" of France at 49 00 N 6 20 W, running home to Brest'
    said = D.direct(w, frigate, by="the test")
    assert said.startswith("Refused, outside the brief") and "no enemy heavier than a brig" in said
    assert w.vessels.find("Vengeance") is None and log_kinds(w)[-1] == "director.refused"
    for text in (
        'ship: a brig-sloop "Harpy" of France at 49 00 N 6 20 W, running home to Brest',
        'ship: a French lugger "Brave" of France at 49 01 N 6 21 W, running home to Brest',
        'ship: a frigate "Fowey" of Britain at 49 02 N 6 22 W, bound for Plymouth',
    ):
        assert not D.direct(w, text, by="the test").startswith("Refused"), text


# ---------------------------------------------------------------------------
# Package 58a: the sample's deltas and the stand-by's instruments (the cold review of
# 2026-10-22, R-26, R-31, R-04, R-42; the lugger officer's and the directors' own
# accounts). Truths 7b-124 to 7b-126, numbered after 68's 7b-120 to 7b-123.
# ---------------------------------------------------------------------------


def _captain_standing_by_a_glass(stranger_at: str, destination: str):
    """The frigate lying in a light westerly off the Lizard with one merchant brig put on the
    sea, and a scripted captain at his station who stands by a glass, turn after turn."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import captain
    from freesail.agents.fake import Fake, call

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
        position={"lat_deg": 49.80, "lon_deg": -5.60},
        region="channel-west",
    )
    w = make_world(7, "data/ships/frigate-36.yaml", sc)
    order = f'ship: a merchant brig "Two Brothers" of Britain at {stranger_at}, {destination}'
    assert w.world_order(order, "the truth").data["result"] == "done"
    w.run(120)
    st = captain(SamplingPolicy.in_lockstep(None, "urgent"), 24 * 3600, world=w)
    fake = Fake([call("stand_by", until="a glass")], loop=True)
    h = Harness(w, st, fake, save=lambda _w, _why: None)
    h.start()
    return w, h


def _samples(h) -> list[dict]:
    from freesail.agents.model import DATA

    return [t.content for t in h.turns if t.role == DATA and "tool_results" not in t.content]


def test_truth_7b_124_a_second_sample_carries_what_changed_and_still_waiting_what_is_new():
    """Package 58a's truth 124 (R-26; LO2-20; the owner's "delta" of 2026-10-17): a
    captain's second sample carries no sail line when no sail changed, and the strangers'
    list only when a sail came, went or was made out further, closing with one line of
    what stands as before; the stand-by's notable lines are counted, found in the sample's
    log, and not listed twice; and "still waiting" carries only the lines since the last
    poll (1.3 million characters in four hours for one director, the whole wait re-listed
    every 55 seconds)."""
    from freesail.agents import mcp_server as M

    # a sail six miles off that is made out no further: the first sample whole, the next
    # with no sail line and no strangers' list, and the line of what stands as before
    w, h = _captain_standing_by_a_glass("49 48 N 5 28 W", "bound from Falmouth for Penzance")
    w.run(2 * 1800 + 5)
    first, second, third = _samples(h)[:3]
    assert {"sails", "strangers", "sail_in_sight"} <= set(first["readings"])
    for later in (second, third):
        assert not {"sails", "strangers", "sail_in_sight", "stranger_in_sight"} & set(
            later["readings"]
        )
        assert later["as_before"].startswith("As before: the sails, one sail in sight, the book;")
        assert "30 minutes of the ship's time since your last reply" in later["you"]
    assert "since your last reply" not in first["you"]
    # a sail that closes: her list comes again each time she is made out further
    w2, h2 = _captain_standing_by_a_glass("49 47 N 5 45 W", "bound for the Lizard")
    w2.run(3 * 1800 + 5)
    told = [s["readings"].get("strangers") for s in _samples(h2)[1:4]]
    assert all(told) and told[0].startswith("a brig") and "British colours" in told[1]
    # the wait's lines: counted in the waking sample, in its log; "still waiting" lists
    # only what is new since the last poll
    h.stand_by("a watch")
    w.record(Severity.NOTABLE, "test.first", "A boat pulling for the shore.")
    w.run(60)
    first_poll = M.still_waiting(h.interim(), 50.0)
    assert "A boat pulling for the shore." in first_poll
    w.record(Severity.NOTABLE, "test.second", "The boat has landed her people.")
    w.run(60)
    second_poll = M.still_waiting(h.interim(), 50.0, listed=1)
    assert "The boat has landed her people." in second_poll
    assert "A boat pulling for the shore." not in second_poll
    assert "(1; one line before them, in your earlier results)" in second_poll
    w.record(Severity.URGENT, "test.urgent", "The brig is standing into danger.")
    w.run(2)
    woke = _samples(h)[-1]
    assert woke["stood_by"]["notable"] == 2 and "lines" not in woke["stood_by"]
    texts = [ln["text"] for ln in woke["log"]]
    assert "A boat pulling for the shore." in texts and "The boat has landed her people." in texts


def test_truth_7b_126_a_dry_run_of_a_doubted_order_returns_the_doubt_and_spends_nothing():
    """Package 58a's truth 126 (R-42; the lugger director's ask that would make "the most
    difference"): `world_order(text, dry_run=true)` of a doubted order returns the doubt
    and what the order would do, performs nothing (the log, the inputs, the world's marks
    and the director's own log as they were, the log's digest the same) and spends no act;
    entered, the order is doubted on the record, and entered again with its reason it is
    performed and counted."""
    from freesail.agents import director as D
    from freesail.agents import tools
    from freesail.agents.fake import call
    from tests.test_director import directed, seat_director

    w = directed("hard-cruise")
    seat_director(w, [call("stand_by", until="a watch")])
    w.run(60)
    mark = "mark: a wreck, her masts showing at 49 30 N 5 31 W"  # six cables off, by day
    before = (
        w.log.digest(),
        len(w.inputs),
        len(w.marks_of_interest),
        len(D.log_of(w).entries),
        D.budget_of(w).acts,
    )
    said = tools.call(w, "director", "world_order", {"text": mark, "dry_run": True})
    assert said.startswith("Dry run, nothing performed and no act spent: it would be doubted: ")
    assert "inside the lookout's horizon" in said
    assert "it would do this: a mark put in the world, a wreck, her masts showing" in said
    after = (
        w.log.digest(),
        len(w.inputs),
        len(w.marks_of_interest),
        len(D.log_of(w).entries),
        D.budget_of(w).acts,
    )
    assert after == before
    # entered, doubted on the record; entered again with its reason, performed and counted
    assert D.direct(w, mark, by="the test").startswith("Doubted, not performed")
    done = D.direct(w, f"{mark} [reason: the wreck of the Swan, long reported]", by="the test")
    assert done.startswith("Done: a mark put in the world")
    assert len(w.marks_of_interest) == 1 and D.budget_of(w).acts == before[4] + 1


# The Western Islands run's anchored night at Horta (the filed save, `docs/playtests/
# 2026-10-18-to-22-owner-playtests-and-review/saves/2026-10-20-western-islands-run-H-
# final.json`, 2 July): the cutter rode at 38 32 N 28 37 W, on the western edge (28 36.6
# W) of the channel between Fayal and Pico, and sheered across it; the log said "she
# swings to the flood" and "to the ebb" sixty-six times in an hour and a half.
HORTA_BERTH = {"lat_deg": 38.5333, "lon_deg": -28.612}
HORTA_NIGHT = datetime(1805, 7, 2, 18, 0)


def test_truth_7b_125_the_horta_nights_swing_logs_once_per_turn():
    """Package 58a's truth 125 (R-04; D7-02): the swing at the turn of the tide is said once
    per turn. The cause, mended and not masked: outside every stream area the stream is
    nought, and its direction fell back to the area's axis and read as the flood, so that a
    ship sheering across an area's edge read the flood outside it and the ebb inside, a
    swing each time. Now `flood` is None where no stream runs, and the swing is said at the
    turns of the channel's own stream alone. The save's night (its ship and chart, the
    berth it rode at, the evening of 2 July, the wind of its log at NW by W), six hours at
    anchor across the edge: 110 swing lines under the old cause, one now."""
    from freesail.world.geo import Position
    from freesail.world.sights import greenwich_time

    sc = Scenario(
        start_time=HORTA_NIGHT,
        wind_from_deg=292.0,
        wind_speed_kn=14.0,
        gustiness=0.3,
        variability=0.3,
        ship_heading_deg=290.0,
        ship_speed_kn=0.0,
        position=HORTA_BERTH,
        chart="atlantic-east",
    )
    w = make_world(7, "data/ships/cutter.yaml", sc)
    assert w.submit("let go the best bower").kind == "order.accepted"
    inside = Position(38.52, -28.58)  # the channel's own water, where she does not ride
    areas: set[str] = set()
    turns, was = 0, None
    for _ in range(6 * 60):
        w.run(60)
        areas.add(w.tide_state.area_id)
        state = w.tide.at(inside, greenwich_time(w))
        if not state.slack:
            turns += int(was is not None and state.flood != was)
            was = state.flood
    assert areas == {"fayal-channel", "open-sea"}  # she sheered across the edge all night
    swung = [e for e in w.log if e.kind == "ship.swung"]
    assert swung and len(swung) <= turns, [e.text for e in swung]
    assert all(e.data.get("area") == "fayal-channel" for e in swung)
    if w.tide_state.flood is None:
        # where no stream runs she rides head to wind, and the reading says so
        assert "head to wind" in w.readings.words("anchor")


# Package 67: the director's seat made real, and the channel between the player and the
# director (spec M7b §2a and §6; the cold review's R-21, R-24 and R-34). Truths 7b-130 to
# 7b-132, numbered after 58a's 124 to 126 and 58b's 127 to 129. The model's name is made
# up, the API a local server speaking the Messages API's shape (`tests/messages_api.py`),
# the settings, the records and the saves in a temporary folder, the key the test's own.
# ---------------------------------------------------------------------------


def test_truth_7b_130_a_seat_starts_the_api_door_admits_it_under_its_budget_and_stands_it_down(
    tmp_path, monkeypatch
):
    """Package 67's truth 130: "a `seat:` under the grant for a model the settings can call
    starts the API door (a fake Messages API in the test), the door is admitted under the
    seat's budget and stood down when it is spent, and a seat for a model the settings
    cannot call is refused in words." On a live server with its harbour, the director seats
    a model as the officer of the watch of the player's own ship for two samples: the game
    starts the API door as the server's subprocess, marked the director's; it is admitted
    under the seat; after its second sample the game stands it down with the reason, the
    door ends of itself, and the director's log says each step; a seat for another model
    the grant names but the settings cannot call is refused, the settings' model named to
    the director alone; the play log says nothing of the seats."""
    pytest.importorskip("fastapi")
    pytest.importorskip("anthropic")
    import httpx
    from messages_api import MODEL, MessagesServer

    from freesail.agents import consent
    from freesail.agents import director as D
    from freesail.world.orders import director_seats
    from tests.test_harbour import Live, Port, _until

    other = "another-made-up-model-8"
    key = "a-test-key-of-no-account-0123456789"
    stand_by = {
        "content": [{"type": "tool_use", "name": "stand_by", "input": {"until": "ten minutes"}}]
    }
    with MessagesServer(key, [stand_by] * 6) as api:
        port = Port(
            tmp_path, {"doors": {"api": {"model": MODEL, "flags": ["--base-url", api.url]}}}
        )
        for name in (MODEL, other):
            consent.Record(
                name, "a test runtime", "2026-10-23", consent.YES, answer="Yes.", drill="passed"
            ).write(port.records)
        monkeypatch.setenv("FREESAIL_API_KEY", key)
        monkeypatch.setenv("PYTHON_KEYRING_BACKEND", "keyring.backends.null.Keyring")
        live = Live(port)
        try:
            with httpx.Client(base_url=live.url, timeout=60) as c:
                c.post(
                    "/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"}
                )
                d = port.driver
                with d.lock:
                    w = d.world
                    w.scenario.director = {
                        "models": [MODEL, other],
                        "seats": 2,
                        "seats_in_voyage": 3,
                    }
                    refused = D.direct(w, f"seat: {other} as master for 2 samples", by="the test")
                    held = D.direct(w, f"seat: {MODEL} as officer for 2 samples", by="the test")
                assert refused == (
                    "Refused: the settings call no model by that name; the API door's model is "
                    f"{MODEL}."
                )
                assert held.startswith("Done: the director's seat held for") and "2 samples" in held
                c.post("/api/driver", json={"action": "speed", "value": 600})
                c.post("/api/driver", json={"action": "go"})

                def door() -> dict:
                    doors = c.get("/api/harbour/state").json()["doors"]
                    return doors[0] if doors else {}

                started = _until(door, 30)
                assert started["by"] == "the director"
                assert started["words"].startswith(
                    "The director's seat's API door at the officer of the watch"
                )

                def admitted() -> bool:
                    with d.lock:
                        seat = director_seats(d.world).get("own/officer of the watch")
                        stood = d.world.agents.get("officer of the watch")
                        return bool(
                            (seat and seat.get("admitted") is not None)
                            or (stood is not None and stood.agent.released)
                        )

                try:
                    _until(admitted, 90)
                except AssertionError:
                    out = c.get(f"/api/harbour/doors/{started['id']}").json()["output"]
                    raise AssertionError("\n".join(out)) from None
                ended = _until(
                    lambda: (
                        (r := c.get(f"/api/harbour/doors/{started['id']}").json())["state"]
                        == "ended"
                        and r
                    ),
                    120,
                )
                c.post("/api/driver", json={"action": "hold"})
                with d.lock:
                    h = d.world.agents["officer of the watch"]
                    assert h.model_name == MODEL and h.agent.released
                    assert "the director's budget of 2 samples is spent" in h.agent.released_reason
                    assert director_seats(d.world) == {}
                    kinds = [(e.kind, e.text) for e in D.log_of(d.world).entries]
                    play = [e.text for e in d.world.log if e.kind == "world.order"]
                assert ended["code"] == 3  # the door's EXIT_RELEASED
                assert ended["output"][-1].endswith("its station was released. ==")
                seats = [t for k, t in kinds if k == "director.seat"]
                assert seats[0].startswith(f"The seat held: {MODEL} as the officer of the watch")
                assert any(t.startswith("The seat's door admitted") for t in seats)
                assert seats[-1].startswith("The seat stood down") and "is spent" in seats[-1]
                refusal = [t for k, t in kinds if k == "director.refused"]
                assert refusal and MODEL not in refusal[0]
                # the seat's own order is for the record, the refused one never reached it
                assert len(play) == 1 and other not in play[0]
        finally:
            live.close()


def test_truth_7b_131_the_players_word_reaches_the_director_and_its_answer_him_and_no_play_log():
    """Package 67's truth 131 (R-21, R-24): "`director: <words>` at the prompt reaches the
    director's next sample and its answer reaches the player's driver line, and neither is
    in the play log or its replay's play side." At the console, a scripted director stands
    by for a watch; the player's word wakes it and is in its sample as the player's word
    apart from the game; it answers with `answer the player: ...`, which the console prints
    as its own line; both are in the director's log and `two stories` shows both beside
    the play log; the play log, and the play log of the save's replay, hold neither."""
    import io

    from freesail.agents import Fake, call, reply
    from freesail.agents import director as D
    from freesail.api.session import ship_factory
    from freesail.core import replay
    from freesail.ui.console import Console
    from tests.test_director import directed, seat_director

    w = directed("quiet-passage")
    script = [
        reply("", call("stand_by", until="a watch")),
        reply(
            "",
            call("world_order", text="answer the player: Aye, a quiet passage it is."),
            call("stand_by", until="a watch"),
        ),
        reply("", call("stand_by", until="a watch")),
    ]
    h = seat_director(w, Fake(script))
    out = io.StringIO()
    console = Console(w, out=out)
    w.run(120)
    assert h.agent.standing_by
    word = "Keep it quiet tonight, if you would."
    console.handle_line(f"director: {word}")
    w.run(120)
    asked = [t for t in h.turns if t.role == "data" and word in json.dumps(t.content)]
    assert asked and "The player, apart from the game: " + word in json.dumps(asked[0].content)
    printed = out.getvalue()
    assert "The director, apart from the game: Aye, a quiet passage it is." in printed
    assert "Your word is with the director" in printed
    kinds = [e.kind for e in D.log_of(w).entries]
    assert "director.player" in kinds and "director.answered" in kinds
    stories = "\n".join(D.two_stories(w))
    assert word in stories and "Aye, a quiet passage it is." in stories
    for e in w.log:
        assert word not in e.text and "a quiet passage it is" not in e.text
    copy = replay.replay(json.loads(json.dumps(w.save())), ship_factory)
    assert copy.log.digest() == w.log.digest()
    played = [e.line() for e in copy.log.all()]
    assert not any(word in x or "a quiet passage it is" in x for x in played)
    assert any(e.kind == "director.player" for e in D.log_of(copy).entries)


def test_truth_7b_132_a_seated_api_doors_fold_fires_at_the_default_budget_on_a_long_seat(
    tmp_path, monkeypatch
):
    """Package 67's truth 132 (R-34: with `budget_tokens` at the door's whole context the
    handover fold never fired, and two seats ran to sixteen million prompt tokens in two
    hours): "a seated API door's handover fold fires at the default `budget_tokens` on a
    long seat." The API door, its model reporting 200,000 tokens of context, seated by the
    director as the officer of the watch: its fold is counted from two fifths of it; the
    conversation the server counts grows by 15,000 tokens a request; the handover note is
    asked at 56,000 and written, the conversation folded, and the door says its size at
    the fold. The same door unseated is counted from the whole context, as before."""
    pytest.importorskip("fastapi")
    pytest.importorskip("anthropic")
    from messages_api import CONTEXT, MODEL, Game, MessagesServer, fake_store, finished, run_door

    from freesail.agents import consent

    fake_store(monkeypatch)
    key = "sk" + "-ant-" + "api03-" + "Tq7xLmPz" * 6
    game = Game(tmp_path, station="officer of the watch")
    consent.Record(MODEL, "t", "2026-10-23", consent.YES, answer="Yes.", drill="passed").write(
        game.records
    )
    game.world.scenario.director = {"models": [MODEL], "seats": 1, "seats_in_voyage": 1}
    e = game.world.world_order(f"seat: {MODEL} as officer for 40 samples")
    assert e.data["result"] == "done"
    count = {"n": 0}

    def answer(body: dict) -> dict:
        count["n"] += 1
        usage = {"input_tokens": 15000 * count["n"], "output_tokens": 20}
        if "Write the watch's handover note" in json.dumps(body["messages"][-1]):
            note = {"note": "All quiet; the land not yet raised."}
            call = {"type": "tool_use", "name": "handover_note", "input": note}
        else:
            call = {"type": "tool_use", "name": "stand_by", "input": {"until": "ten minutes"}}
        return {"content": [call], "usage": usage}

    argv = ["--model", MODEL, "--station", "officer", "--session", "test"]
    with MessagesServer(key, [answer] * 12) as srv:
        got = run_door(game, [*argv, "--base-url", srv.url], {"FREESAIL_API_KEY": key})
        game.wait_for(lambda: game.harness is not None and game.harness.agent.samples >= 1, 30)
        h = game.harness
        assert h.budget_tokens == int(0.4 * CONTEXT)  # 80,000 of the 200,000
        for _ in range(6):
            game.wait_for(lambda: h.open_sample is None, 30)
            game.driver.tick(600)
        game.wait_for(lambda: h.open_sample is None, 30)
        with game.driver.lock:
            folded = [
                t
                for t in h.turns
                if t.role == "data" and isinstance(t.content, dict) and t.content.get("folded")
            ]
            notes = [x for x in game.world.log if x.kind == "agent.handover"]
            game.world.world_order("unseat: officer, the watch is over")
        assert finished(got) == 3
    out = got["out"].getvalue()
    assert folded and folded[0].content["handover"] == "All quiet; the land not yet raised."
    assert notes and "Admitted under the director's seat: 40 samples" in out
    assert "the handover fold at 80,000 tokens" in out
    said = [ln for ln in out.splitlines() if ln.startswith("The conversation was folded at")]
    assert said and "90,000 tokens at the last request (the server's count)" in said[0]
    # the same door with no seat: counted from the whole context, as before
    game2 = Game(tmp_path / "unseated", station="officer of the watch")
    consent.Record(MODEL, "t", "2026-10-23", consent.YES, answer="Yes.", drill="passed").write(
        game2.records
    )
    count["n"] = 0
    with MessagesServer(key, [answer] * 3) as srv:
        got = run_door(game2, [*argv, "--base-url", srv.url], {"FREESAIL_API_KEY": key})
        game2.wait_for(lambda: game2.harness is not None and game2.harness.agent.samples >= 1, 30)
        assert game2.harness.budget_tokens == CONTEXT
        with game2.driver.lock:
            game2.world.submit("stand down the officer of the watch")
        assert finished(got) == 3


# Package 58b: the captain's sea sense, third pass (the Éclair's first cruise, the lead's
# wave-2 playtest and 57's gale trial). Truths 7b-127 to 7b-129, numbered after 58a's
# 7b-124 to 7b-126: a leg laid again at the turn of the tide, the wind across the stern
# leaving the lugs against their masts and the captain dipping them, and the frigate lying
# to under the book in the gale trial without being taken aback.
# ---------------------------------------------------------------------------

OFF_THE_SEPT_ILES = (49.0, -3.6)  # open water, forty fathoms, the land four leagues south


def _eclair_under_her_lugs(
    hh: int, mm: int, at: tuple[float, float] = (48.7356, -4.000), heading: float = 95.0
) -> World:
    """The Éclair under her lugs, the wind W by S, on the morning of the wave-2 playtest
    (12 June 1805): by default in the channel of Bas east of the road."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, hh, mm),
        wind_from_deg=260.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=4.0,
        position={"lat_deg": at[0], "lon_deg": at[1]},
        region="channel-west",
        ports=["roscoff", "morlaix", "st-malo"],
        nation="france",
    )
    w = make_world(SEED, "data/ships/lugger.yaml", sc)
    assert w.submit("set plain sail").kind == "order.accepted"
    return w


def test_truth_7b_127_the_eclairs_leg_is_laid_again_at_the_turn_of_the_tide_in_the_channel_of_bas():
    """Package 58b's truth 127 (item 1; the Éclair's first cruise: the leg laid on the flood
    was held through the ebb into the narrows of the channel of Bas): the rules captain lays
    his leg allowing the flood the master's book gives, and when the master's tide turns to
    the ebb in the channel he lays it again at once, saying why, the helm given the course
    worked for the new stream; and she clears the channel without touching. From the
    channel's eastern end, east of Roscoff: from the road (48° 44.1' N, 4° W) the planner's
    first leg crosses the land about the Isle Verte (61's route, found on the way)."""
    w = _eclair_under_her_lugs(5, 25, at=(48.7356, -3.96))
    w.captain.set_intent("passage to 48 46 N 3 45 W")
    w.run(3600)
    shaped = [e for e in w.log if e.kind == "helm.set" and "Shaped a course for" in e.text]
    assert shaped and "Allowing the flood" in shaped[0].text
    turned = [e for e in w.log if e.kind == "reckoning.tide" and e.data.get("turn")]
    assert turned and turned[0].data["flood"] is False, [e.text for e in turned]
    relaid = [
        e
        for e in w.log
        if e.kind == "order.accepted" and "(the tide has turned, the ebb making)" in e.text
    ]
    assert relaid, [e.text for e in w.log if e.kind == "order.accepted"]
    assert relaid[0].text.startswith("By the captain, on passage: shaping a course for")
    assert 0 <= relaid[0].tick - turned[0].tick <= 11 * 60
    assert [e for e in w.log if e.kind == "helm.set" and e.tick == relaid[0].tick]
    assert not [e for e in w.log if e.kind == "ship.aground"]


def test_truth_7b_128_a_steer_through_the_stern_leaves_the_lugs_against_the_masts_and_he_dips():
    """Package 58b's truth 128 (item 3; the lead's wave-2 playtest, finding 1, and the
    owner's ruling of 2026-10-23 that nothing is ordered by the helm): the Éclair running
    under her lugs is steered NE through the stern by the player; the lugs are left against
    their masts, said once ("dip them when you will"), and nothing is done, the picture
    drawing them on the weather side; the same turn made by the rules captain's own course
    has the lugs dipped as his next orders, and the picture draws them to leeward. Off the
    Sept-Îles, in open water."""
    from freesail.api.queries import snapshot

    def lug_sides(world: World) -> dict[str, str | None]:
        return {
            s["id"]: s["lug_side"]
            for s in snapshot(world)["sails"]
            if s["id"] in ("fore.lug", "main.lug")
        }

    w = _eclair_under_her_lugs(10, 0, at=OFF_THE_SEPT_ILES, heading=90.0)
    w.run(240)
    assert lug_sides(w) == {"fore.lug": "larboard", "main.lug": "larboard"}
    start = len(w.log)
    w.submit("steer NE")
    w.run(600)
    lines = list(w.log)[start:]
    said = [e for e in lines if e.kind == "sail.across_the_stern"]
    assert [e.text for e in said] == [
        "The wind has come across the stern to the larboard quarter: the foresail and the "
        "mainsail are against their masts; dip them when you will."
    ]
    assert not [e for e in lines if e.text.startswith(("Dip the", "By the captain"))]
    assert lug_sides(w) == {"fore.lug": "larboard", "main.lug": "larboard"}  # the weather side
    w = _eclair_under_her_lugs(10, 0, at=OFF_THE_SEPT_ILES, heading=90.0)
    w.run(240)
    w.captain.set_intent("passage to 49 20 N 3 20 W")
    w.run(900)
    said = [e for e in w.log if e.kind == "sail.across_the_stern"]
    dips = [e for e in w.log if e.kind == "order.accepted" and "dipping the" in e.text]
    assert len(said) == 1 and len(dips) == 2, [e.text for e in w.log]
    assert all(e.tick > said[0].tick and e.text.startswith("By the captain") for e in dips)
    assert lug_sides(w) == {"fore.lug": "starboard", "main.lug": "starboard"}  # to leeward


def test_truth_7b_129_the_gale_trials_frigate_lies_to_under_the_book_without_being_taken_aback():
    """Package 58b's truth 129 (item 5; 57's gale trial, for the lead's playtest of the
    fixed book): the frigate on her station off Ushant as the westerly rises to a gale.
    The head sail straining at its bolt-ropes is taken in by the captain before it blows
    out (the trial lost its fore topmast staysail at 08:29 before); she is hove to for
    weather and lies a-try under the close-reefed main topsail and the staysails, as the
    book has it, and in the hours she lies so (four and more before package 88, three and a
    half since) she is never taken aback, no sail is lost, and she drifts at under two knots
    on the mean. What she does when she
    fills away for the station in the gale's tail is the trial's own pin, an expected
    failure until the lead has played it (`tests/test_captain_trials.py`)."""
    from freesail.physics.hull import hull_state
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/trials/trial-station-gale.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    lying = aback = 0
    knots = []
    for _ in range(520):
        w.run(60)
        if str(w.readings.value("manoeuvre_in_hand") or "") == "hove to":
            lying += 1
            knots.append(units.ms_to_knots(w.ship.dyn.speed))
            aback += hull_state(w.ship).seconds_aback > 0.0
    states = [(e.tick, e.data["state"]) for e in w.log if e.kind == "captain.state"]
    assert "hove to for weather" in {s for _t, s in states}, states
    lay = [e for e in w.log if e.kind == "ship.hove_to"]
    assert lay and lay[0].text.startswith("Lying a-try under the main topsail and the staysails")
    taken = [e for e in w.log if e.text.endswith("(straining at the bolt-ropes).")]
    assert taken and "taking in the fore topmast staysail" in taken[0].text
    assert not [e for e in w.log if e.kind in ("sail.blown_out", "sail.split")]
    # package 88 (item 2, by bisection: `navigation.WEAR_ROOM` off gives 243 minutes again):
    # tacked and not worn with Ushant two miles under her lee in the forenoon, she reaches
    # the lee-shore line sooner and is filled away at 28560 (30780): 207 minutes lying a-try,
    # never aback, 1.83 knots on the mean (243 minutes and 1.81 before; four hours the band)
    assert lying >= 200 and aback == 0
    assert sum(knots) / len(knots) < 2.0
    assert not [e for e in w.log if e.kind == "ship.aground"]


# ---------------------------------------------------------------------------
# Milestone 7: the combat core (package 70; spec M7 §12), truths 7-133 onward. Two
# crewed cutters off the Lizard at seed 7, the frigate's gun crews, a merchant brig under
# a privateer's fire, the far fight's measure and the pace; the figures measured on the
# build machine are in each docstring and in docs/dev/TuningNotes.md (package 70).
# Nothing here pre-defines a battle's timing (rule 7): the bands are wide, the seed's
# figure is quoted.
# ---------------------------------------------------------------------------

CUTTER = "data/ships/cutter.yaml"
MERCHANT_BRIG = "data/ships/merchant-brig.yaml"
FIRST_ACTION = "data/scenarios/first-action.yaml"


def _action_scenario(wind_kn=12.0, ship=CUTTER, heading=180.0, speed=0.0, intent=None):
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=wind_kn,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        ship_heading_deg=heading,
        ship_speed_kn=speed,
        **({"intent": intent} if intent else {}),
    )


def _a_cutter_crewed(world, bearing_deg, distance_m, nation="france", fit="carronades"):
    """A cutter of the nation made so far off on the bearing, lying to, and crewed at
    once; her captain's state `engaging` (the empty book: she lies to and fights)."""
    from freesail.world import crews
    from freesail.world.geo import destination
    from freesail.world.ships import vessel_from_spec

    there = destination(world.position, bearing_deg, distance_m)
    world.vessels.serial += 1
    v = vessel_from_spec(
        world,
        {
            "description": "cutter",
            "name": "Renard",
            "nation": nation,
            "position": there,
            "goal": "bound for 48 30 N 5 18 W",
            "intent": "bound for 48 30 N 5 18 W",
            "fit": fit,
        },
        world.vessels.serial,
    )
    v.plan = [("lie_to", math.inf)]
    v.sail_state = "lying to"
    world.vessels.add(v)
    enemy = crews.promote(world, v)
    enemy.captain.state = "engaging"
    return v, enemy


def _guns_ready(world) -> None:
    """The drum, the guns cast loose and loaded, run out and primed on both sides."""
    world.submit("beat to quarters")
    world.run(5)
    world.submit("cast loose the guns")
    world.run(200)


def _two_cutters_at_pistol_shot():
    """The player's cutter with her guns ready, and the French cutter made a third of a
    cable off her starboard beam and crewed; the lookout given his minute; the mark
    engaged to starboard with the fire held."""
    from freesail.combat.guns import battery_of

    w = make_world(SEED, CUTTER, _action_scenario())
    _guns_ready(w)
    heading = float(w.ship.heading)
    v, enemy = _a_cutter_crewed(w, math.degrees(heading) + 90.0, 60.0)
    enemy.ship.dyn.heading = heading
    w.submit("hold your fire")
    w.run(65)
    w.submit("engage her to starboard")
    w.run(1)
    return w, v, enemy, battery_of(w.ship)


def test_truth_7_134_two_cutters_at_pistol_shot_one_broadside_strikes_and_the_damage_is_state():
    """Spec M7 §12: "two cutters with six carronades each, one broadside at pistol shot,
    the hits allotted by the doctrine and the damage in the part graph". The King's
    cutter's starboard carronades at the word, the mark a third of a cable off the beam:
    of the three, at seed 7 one struck her (a shot through the side to larboard, the hole
    kept with its place against the waterline, one killed and one wounded in her
    muster); the mark's own log says what her people saw; nothing is a second model of the
    ship (rule 1)."""
    w, v, enemy, battery = _two_cutters_at_pistol_shot()
    assert battery.target == v.id and battery.engaged == "starboard"
    said = w.submit("fire")
    assert said.kind == "guns.fire", said.text
    w.run(70)
    fired = [e for e in w.log if e.kind == "action.fired"]
    assert fired and fired[0].data["fired"] >= 2, [e.text for e in fired]
    struck = sum(e.data["struck"] for e in fired)
    assert struck >= 1, [e.text for e in fired]
    hits = [e for e in enemy.log if e.kind == "action.hit"]
    assert hits and hits[0].text.startswith("Shot from a cutter:")
    keeper = enemy.ship.extra["damage"]
    assert keeper.hits == struck
    crew = enemy.ship.extra["crew"]
    hurt = [s for s in crew.sailors if s.hurt]
    graph = (
        keeper.holes
        or [ln for ln in enemy.ship.lines.values() if ln.state.value == "parted"]
        or [s for s in enemy.ship.spars.values() if s.wrecked]
        or [s for s in enemy.ship.sails.values() if s.holed_m2 > 0.0]
        or hurt
    )
    assert graph, "a hit that changed nothing"
    for hole in keeper.holes:
        assert set(hole) >= {"side", "x_m", "z_m", "diameter_m", "pounder"}
    assert enemy.readings.words("damage") != "none" or hurt
    for s in hurt:
        assert not s.fit and s.hurt in ("killed", "wounded")
    bill = enemy.readings.value("bill")
    assert bill["killed"] + bill["wounded"] == len(hurt)


def test_truth_7_140_an_action_at_a_cable_ends_in_minutes_and_one_at_long_shot_in_hours():
    """Rule 7 (nothing pre-defines a battle's timing): the same tables give an action of
    minutes and one of hours by the range the captains keep. At a cable, two cutters
    hove to and engaging as they bear, the French cutter under the defaults strikes within
    a quarter of an hour (at seed 7 three minutes after the first shot: a shot between wind
    and water and her losses); at long shot the first action's privateer fights an hour
    and fifty-three minutes (truth 7-133). The log says why she struck."""
    from freesail.combat.guns import Aim, FireMode, battery_of
    from freesail.crew.quarters import quarters_of
    from freesail.ship.parts import Charge

    w = make_world(SEED, CUTTER, _action_scenario(wind_kn=14.0, speed=5.0))
    w.submit("heave to")
    v, enemy = _a_cutter_crewed(w, 90.0, 150.0, fit="long guns")
    enemy.submit("heave to")
    w.run(90)
    for world, target in ((w, v.id), (enemy, "the ship")):
        q = quarters_of(world.ship)
        q.beat(world.clock.tick)
        for g in world.ship.guns.values():
            g.cast_loose = True
        b = battery_of(world.ship)
        b.target = target
        b.engaged = "larboard" if world is w else "starboard"
        b.mode = FireMode.AS_THEY_BEAR
        b.aim = Aim.HULL if world is w else Aim.RIGGING
        b.charge = Charge.ROUND
    first = None
    struck_at = None
    for _ in range(900):
        w.run(1)
        if first is None and any(e.kind == "action.fired_at" for e in enemy.log):
            first = w.clock.tick
        if v.struck:
            struck_at = w.clock.tick
            break
    assert first is not None and struck_at is not None, "no strike within the quarter hour"
    assert struck_at - first <= 900
    line = [e for e in enemy.log if e.kind == "action.struck"][0]
    assert line.text.startswith("The colours are struck:") and "hurt" in line.text
    assert line.data["by_rule"] and line.data["morale"] < line.data["strike_below"]
    assert enemy.captain.state == "struck"
    assert any(e.kind == "action.enemy_struck" for e in w.log)
    assert battery_of(enemy.ship).mode is FireMode.HOLD


def test_truth_7_133_the_first_action_ends_with_the_privateer_struck_and_the_damage_as_state():
    """Spec M7 §12 and the brief's item 9: the first action (data/scenarios/
    first-action.yaml) played by the rules captains with no model seated. At seed 7 the
    privateer engages at 10:06 and opens at long shot at 10:13; the King's cutter closes,
    returns her fire and the colours come down at 11:12 (fifty-nine minutes after the first
    shot) with five of thirty hurt and seven shot holes, the strike line giving the reasons
    in figures; the King's cutter has her main topgallant mast and two yards carried away
    and three lines shot away in the part graph, nobody hurt. The band is wide (three
    quarters of an hour to three) because the timing is the seed's, never the rule's.
    Package 70 pinned 12:06 (an hour and fifty-three minutes, the band an hour to three):
    package 71 moved it by two items, proved by bisection (docs/dev/TuningNotes.md, package
    71): the engaging helm's law (item 8), which alone takes the half hour aback out of the
    King's cutter's circle and ends the action at 11:19, and the privateer's new row on her
    station (she closes a sail near her instead of waiting for one within her engaging
    distance; found on the way), which alone ends it at 11:12; every item off gives 70's
    12:06 and digest again."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    v = w.vessels.find("Renard")
    assert w.captain.role == "kings-ship" and v.brain.role == "privateer"
    first = None
    struck_tick = None
    for _ in range(3 * 60):
        w.run(60)
        if first is None:
            fired_at = [e for e in w.log if e.kind == "action.fired_at"]
            if fired_at:
                first = fired_at[0].tick
        if v.struck or w.ship.extra.get("struck"):
            struck_tick = w.clock.tick
            break
    assert first is not None, "nobody opened fire"
    assert v.struck and not w.ship.extra.get("struck"), "the privateer strikes at this seed"
    # 3600 <= ... at package 70 (12:06, 6779 s); 3539 s at package 71 (11:12), by the bisection
    assert 2700 <= struck_tick - first <= 3 * 3600, f"{(struck_tick - first) / 60:.0f} min"
    enemy = v.crew
    line = [e for e in enemy.log if e.kind == "action.struck"][0]
    assert "against a broadside of" in line.text and "hurt" in line.text
    assert enemy.captain.state == "struck" and w.captain.state != "engaging"
    keeper = enemy.ship.extra["damage"]
    assert keeper.holes and keeper.hits >= len(keeper.holes)
    hurt = [s for s in enemy.ship.extra["crew"].sailors if s.hurt]
    assert hurt and all(not s.fit for s in hurt)
    # the King's cutter's damage is the part graph's own state (rule 1)
    ship = w.ship
    wrecked = [s.id for s in ship.spars.values() if s.wrecked]
    parted = [ln.id for ln in ship.lines.values() if ln.state.value == "parted"]
    assert wrecked or parted, "an action at long shot at the rigging and nothing cut"
    assert w.readings.words("damage") != "none"
    # the victor's book ceased fire and secured the guns when she struck
    assert any(e.kind == "action.enemy_struck" for e in w.log)
    assert w.readings.value("guns")["mode"] == "hold"


def _frigate_interval(hurt_share: float) -> float:
    """The mean seconds between a starboard 18-pounder's discharges over twenty minutes
    of the battery's own cycle at a mark abeam, the company full or a share of each gun
    crew struck down at their guns after the beat."""
    from freesail.combat.action import _firer
    from freesail.combat.guns import FireMode, Target, battery_of
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    _guns_ready(w)
    w.run(40)
    ship = w.ship
    q = quarters_of(ship)
    if hurt_share:
        for gc in q.crews.values():
            n = int(round(len(gc.members) * hurt_share))
            for s in gc.members[:n]:
                s.fit = False
                s.hurt = "wounded"
                s.at = None
    b = battery_of(ship)
    b.engaged = "starboard"
    b.mode = FireMode.AS_THEY_BEAR
    b.target = "mark"
    b.target_words = "a brig"
    mark = Target(
        id="mark",
        words="a brig",
        bearing_rad=units.wrap_2pi(float(ship.heading) + math.pi / 2.0),
        range_m=200.0,
        heading_rad=float(ship.heading),
        length_m=30.0,
        heel_deg=0.0,
        nation="france",
        body=None,
        world=None,
    )
    rng = w.rng.stream("truth-7-135")
    firings: dict[str, list[int]] = {}
    for tick in range(20 * 60):
        before = {g.id: g.fired for g in ship.guns.values()}
        b.tick(1.0, q, _firer(w, ship), mark, rng, tick, lambda *a, **k: [])
        for g in ship.guns.values():
            if g.fired > before[g.id]:
                firings.setdefault(g.id, []).append(tick)
    gaps = []
    for gid, ticks in firings.items():
        g = ship.guns[gid]
        if g.kind == "long" and g.pounder == 18 and g.side == "starboard" and len(ticks) > 2:
            gaps += [t2 - t1 for t1, t2 in zip(ticks[1:], ticks[2:], strict=False)]
    assert gaps, "no 18-pounder fired twice"
    return sum(gaps) / len(gaps)


def test_truth_7_135_the_frigates_broadside_every_minute_and_three_quarters_and_slower_short():
    """Spec M7 §8 and §12: "the frigate's broadside at the start of an action in a minute
    and three quarters with her full company, in three with a quarter of them casualties".
    The rate falls out of the muster (rule 2): the long gun's phases (85 s nominal) under
    the crews' numbers, rating, fatigue and the weather's factor give 104 s between an
    18-pounder's discharges with the full company at seed 7; a quarter of each gun's crew
    struck down at their guns (two or three men in ten, the rounding under a true quarter)
    gives 159 s by the square law of the numbers (`guns.NUMBERS_POWER`). The bands hold
    the spec's figures with the seed's measured inside them."""
    full = _frigate_interval(0.0)
    assert 90.0 <= full <= 125.0, f"{full:.0f} s"
    short = _frigate_interval(0.25)
    assert 140.0 <= short <= 210.0, f"{short:.0f} s"
    assert short >= full * 1.3


def test_truth_7_136_a_tack_with_the_guns_served_is_slower_by_exactly_the_hands_it_takes():
    """Spec M7 §8 and §8a: "a tack with the guns run out takes longer than the same tack
    cleared", by the fighting book's priority (the design of item 1). The frigate close
    hauled on the starboard tack (truth 10's world): cleared, she tacks in 447 s at seed
    7; at quarters with the guns run out under `sail before guns` the bill lends the tack
    half of every gun's crew (84 hands, said from where) and she tacks in 436 s with the
    guns gone short; under `guns before sail` the trimmers alone have her, and she tacks
    in 642 s. The player never queues a thing: the order is given and the bill finds the
    hands."""

    def tack(at_quarters: bool, priority: str = "sail before guns"):
        w = close_hauled_on_starboard(FRIGATE, heading=292.5)
        if at_quarters:
            _guns_ready(w)
            w.run(40)
            w.submit("run out the guns")
            said = w.submit(priority)
            assert said.kind == "guns.priority", said.text
            w.run(120)
        t0 = w.clock.tick
        w.submit("tack ship")
        done, seconds = until(w, ("ship.tacked", "ship.missed_stays"), 1200)
        assert done and done[0].kind == "ship.tacked", (priority, [e.text for e in done])
        robbed = [e for e in w.log if e.tick > t0 and e.kind == "quarters.robbed"]
        return seconds, robbed

    cleared, none_robbed = tack(False)
    assert not none_robbed and 285 <= cleared <= 600
    sail_first, robbed = tack(True)
    assert robbed and robbed[0].data["hands"] >= 40, [r.text for r in robbed]
    assert "taken from the guns" in robbed[0].text
    assert sail_first <= cleared * 1.15, f"{sail_first} s against {cleared} s cleared"
    guns_first, robbed2 = tack(True, "guns before sail")
    assert not robbed2
    assert guns_first >= cleared * 1.25, f"{guns_first} s against {cleared} s cleared"


def test_truth_7_137_a_merchant_brig_fired_into_strikes_by_morale_and_the_log_says_why():
    """Spec M7 §12: "a merchant brig fired into by a privateer strikes by morale when her
    odds fall below the doctrine's figure, the log saying why". The brig bound for
    Falmouth, the French privateer cutter cruising for prizes a thousand yards to the
    south-east: at seed 7 the privateer engages at 10:06, chases her down (a weaker mark
    is closed to pistol shot) and opens at a cable at 10:14, the brig beats to quarters,
    and at the first shot that tells (10:15) her colours come down by the odds (her figure
    0.37 under the merchant's line of 0.4: 'against a broadside of 36 pounds to our 12'),
    nobody hurt. A company does not strike to shot that missed: the rule wants a hit as
    well as fire."""
    from freesail.world.geo import destination
    from freesail.world.ships import vessel_from_spec

    w = make_world(SEED, MERCHANT_BRIG, _action_scenario(speed=4.0, intent="bound for Falmouth"))
    w.submit("set plain sail")
    there = destination(w.position, 135.0, 1200.0)
    w.vessels.serial += 1
    v = vessel_from_spec(
        w,
        {
            "description": "cutter",
            "name": "Renard",
            "nation": "france",
            "position": there,
            "goal": "cruising off the Lizard within 10 miles",
            "intent": "cruise for prizes off the Lizard within 10 miles",
            "fit": "carronades",
        },
        w.vessels.serial,
    )
    w.vessels.add(v)
    assert w.captain.role == "merchant" and v.brain.role == "privateer"
    struck = None
    for _ in range(90):
        w.run(60)
        if w.ship.extra.get("struck"):
            struck = w.clock.tick
            break
    assert struck is not None, "the brig did not strike within the hour and a half"
    line = [e for e in w.log if e.kind == "action.struck"][0]
    assert line.data["by_rule"] and "against a broadside of" in line.text
    assert line.data["morale"] < line.data["strike_below"] == 0.4
    fired_at = [e for e in w.log if e.kind == "action.fired_at"]
    hits = [e for e in w.log if e.kind == "action.hit"]
    assert fired_at and hits and fired_at[0].tick <= hits[0].tick <= line.tick
    assert w.captain.state == "struck" and w.readings.words("colours") == "struck"
    w.run(61)  # the privateer's captain judges once a minute: the mark struck, the action over
    assert v.crew is not None and v.crew.captain.state != "engaging"
    assert any(e.kind == "action.enemy_struck" for e in v.crew.log)


def test_truth_7_139_the_far_fight_measured_once_ends_within_the_near_fights_hour_and_repeats():
    """The brief's item 9: the far fight measured once against the same tables at coarse
    steps (`combat/far.py`), recorded for 74 and not built beyond the measure. Two cutters
    at two cables, the King's with carronades at the hull and the privateer's long guns at
    the rigging: at seed 7 the long-gun cutter strikes after seven rounds of three minutes
    (twenty-one minutes) with four hurt and three shot holes, against the near fight at a
    cable in three minutes (truth 7-140) and at long shot in near two hours (7-133); the
    far fight's range is the far brain's choice, which is 74's. The same seed gives the
    same record."""
    from freesail.combat import far
    from freesail.core.rng import Rng

    def once():
        rng = Rng(SEED).stream("far")
        a = far.far_ship(
            CUTTER, "britain", "carronades", aim="hull", morale_start=0.9, strike_below=0.1
        )
        b = far.far_ship(
            CUTTER, "france", "long guns", aim="rigging", morale_start=0.7, strike_below=0.35
        )
        rounds = far.fight(a, b, 400.0, rng, minutes=180)
        return a, b, rounds

    a, b, rounds = once()
    assert a.broadside_lb == 36.0 and b.broadside_lb == 13.0
    assert b.struck_at_s is not None and a.struck_at_s is None
    assert b.struck_at_s <= 3600.0 and len(rounds) == b.struck_at_s / 180.0
    assert b.hurt >= 1 and b.holes >= 1 and b.rounds_fired > 0 and a.rounds_fired > 0
    a2, b2, rounds2 = once()
    record = [(r.fired, r.struck, r.hurt) for r in rounds]
    assert record == [(r.fired, r.struck, r.hurt) for r in rounds2]


@pytest.mark.pace
def test_truth_7_138_the_pace_with_two_crewed_cutters_in_action_holds_the_crewed_floor():
    """The brief's item 9: the pace measured with two crewed ships in action against the
    baseline (the owner's 95 ticks a second with twelve crewed ships; the conftest's
    floors not lowered). The first action a quarter of an hour in, both at quarters and
    the privateer firing: 538 ticks a second on the build machine (best of three
    thousands), against `crews.CREWED_FLOOR_TICKS_S`."""
    import time

    from freesail.world import crews as K
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(900)
    v = w.vessels.find("Renard")
    assert v.crew is not None and v.crew.captain.state == "engaging"
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"


def test_truth_7_141_firing_on_a_sail_not_made_out_as_an_enemy_is_told_not_refused():
    """Rule 3, the least of it (the brief's item 7): a ship that fires on a sail not at war
    with her is not refused; the consequence is told once (`action.unrecognised`) and her
    state carries it (`ship.extra["outlaw"]`) for the ports' stance to read; 71's colours,
    private signal and hail plug in where the lookout's nation is read."""
    from freesail.combat.guns import battery_of

    w = make_world(SEED, CUTTER, _action_scenario())
    _guns_ready(w)
    heading = float(w.ship.heading)
    v, enemy = _a_cutter_crewed(w, math.degrees(heading) + 90.0, 60.0, nation="united-states")
    enemy.ship.dyn.heading = heading
    w.submit("hold your fire")
    w.run(65)
    said = w.submit("engage her to starboard")
    assert said.kind == "guns.engage"
    w.submit("fire")
    w.run(70)
    told = [e for e in w.log if e.kind == "action.unrecognised"]
    assert len(told) == 1 and "no enemy of ours" in told[0].text
    assert "fired into" in str(w.ship.extra.get("outlaw"))
    assert any(e.kind == "action.fired_at" for e in enemy.log)
    assert battery_of(w.ship).target == v.id  # the order stood: told, not refused


def test_truth_7_142_the_players_strike_is_never_refused_and_the_quarter_bill_reads():
    """Decision 7 and the brief's item 6: `strike the colours` is never refused, its
    consequence told (the guns silent, she lies to, `the colours` struck, the captain's
    machine in `struck`); and the quarter bill reads after the beat, 'not at quarters'
    before it; `secure the guns` and `pipe down` put the hands back under the watch bill."""
    from freesail.combat.guns import FireMode, battery_of

    w = make_world(SEED, CUTTER, _action_scenario())
    assert w.readings.words("quarter_bill") == "not at quarters"
    for text in ("engage her to starboard", "fire as they bear"):
        said = w.submit(text)
        assert said.kind == "order.rejected" and "not at quarters" in said.text
    said = w.submit("beat to quarters")
    assert said.kind == "crew.quarters" and "gun crews manned" in said.text
    bill = w.readings.value("quarter_bill")
    assert bill["at_quarters"] and "Nos. 1 guns" in bill["words"]
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)  # the crews' minute, stretched while the company is still coming up
    assert w.readings.value("guns")["cast_loose"]
    said = w.submit("strike the colours")
    assert said.kind == "action.struck" and "The colours are struck" in said.text
    assert w.readings.words("colours") == "struck" and w.ship.extra["struck"]
    assert battery_of(w.ship).mode is FireMode.HOLD
    assert w.captain.state == "struck"
    said = w.submit("secure the guns")
    assert said.kind == "order.accepted"
    w.run(200)
    assert w.readings.words("quarter_bill") == "not at quarters"
    assert not w.readings.value("guns")["cast_loose"]


# ---------------------------------------------------------------------------
# Package 71: signals and the voice between ships (spec M7 §1 to §6; truths 7-143 onward)
# ---------------------------------------------------------------------------

ENCOUNTER = "data/scenarios/encounter.yaml"
CONVOY = "data/scenarios/convoy.yaml"


def _sea_at(lat: float, lon: float, ship: str, when: datetime, **kw):
    """A world at sea off the Lizard at seed 7 at a given hour (the brains' `world_at`,
    which fixes the forenoon, with the time free)."""
    sc = Scenario(
        start_time=when,
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        **kw,
    )
    return make_world(SEED, ship, sc)


def _frigate_and_a_cutter_under_false_colours(cables: float):
    """The King's frigate with a French privateer cutter under British colours so many
    cables off her beam, both at sea south of the Lizard at seed 7."""
    from tests.test_brains import put, world_at

    w = world_at(49.5, -5.5)
    w.run(60)
    from freesail.world.geo import destination

    here = w.position
    off = destination(here, 180.0, cables * units.CABLE)
    v = put(
        w,
        "cutter",
        "france",
        {"lat_deg": off.lat_deg, "lon_deg": off.lon_deg},
        "cruising off the Lizard within 10 miles",
        intent="cruise for prizes off the Lizard within 10 miles",
        colours="British",
        name="Renard",
    )
    return w, v


def test_truth_7_143_a_cutter_under_false_colours_is_made_out_as_british_and_lies_to_the_hail():
    """Spec M7 §6's first truth and the brief's item 10: a French privateer cutter under
    British colours is made out by the King's frigate's lookout as British at the colours'
    range (the nation SHOWN, never the true one), and spoken within four cables she answers
    the hail by the table with a lie under the flag she shows (a name and a port of that
    nation), which the frigate's captain believes until the private signal or the shot
    says otherwise; beyond four cables the hail is refused with the distance."""
    from freesail.world import hail as H

    w, v = _frigate_and_a_cutter_under_false_colours(cables=18.0)
    w.run(120)
    item = next(i for i in w.readings.value("strangers")["items"] if i["id"] == v.id)
    assert item["made_out"] >= 2 and item["nation"] == "britain"  # 1.8 miles: the colours' range
    assert "British colours, the red ensign" in item["known"]
    said = w.submit("hail her")
    assert said.kind == "order.rejected" and "beyond hail" in said.text
    w2, v2 = _frigate_and_a_cutter_under_false_colours(cables=2.0)
    w2.run(60)  # she draws off a cable a minute: three cables when spoken
    said = w2.submit("hail her")
    assert said.kind == "hail.answered", said.text
    answer = said.data["answer"]
    assert "Renard" not in answer and " of " in answer
    assert H.nation_in_words(w2.nations, answer) == "britain"
    assert w2.captain.recognised[v2.id]["nation"] == "britain"
    assert v2.spoken and any(e.kind == "hail.answered" for e in w2.log)
    # the standard questions, each answered in the period's form
    said = w2.submit("say to the cutter: whence come you, and whither bound? what cargo?")
    assert said.kind == "hail.answered" and "For Falmouth." in said.data["answer"]


def test_truth_7_144_the_private_signal_answered_wrong_makes_her_a_stranger_and_he_chases():
    """Spec M7 §6's second truth: the encounter (data/scenarios/encounter.yaml) played by the
    rules captains with no model seated. At seed 7 the frigate's captain, on his station,
    closes the cutter under British colours and makes her the private signal at 10:05
    (the hoist queued behind a wear, up at 10:11); the privateer bluffs a guessed reply,
    read wrong at 10:16 ("a stranger under false colours, an enemy"), and he gives chase by
    his doctrine at 10:17, going about for her (the chase names his stranger and tacks
    for a chase on the other side of the wind's eye, both mended in the package: before,
    the bare order chased the merchant brig and held the tack that opened the cutter); a
    merchant brig challenged alone makes no answer and is left 'a merchantman, who has
    none; a stranger to be spoken'. The bands are a quarter of an hour wide: the timing
    is the seed's (up 10:12, wrong 10:15, chase 10:16 while the hoist flew from the
    book's minute and not from the hands' finishing, mended in the package)."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(ENCOUNTER)
    w = make_scenario_world(sf)
    begin(w, sf)
    renard = w.vessels.find("Renard")
    assert renard.nation == "france" and renard.nation_shown == "britain"
    states = []
    for _ in range(45):
        w.run(60)
        st = w.captain.state
        if not states or states[-1][1] != st:
            states.append((w.clock.tick, st))
        if st == "chasing":
            break
    judged = [e for e in w.log if e.kind == "signal.private_judged"]
    assert judged and judged[0].data["id"] == renard.id and judged[0].data["verdict"] == "wrong"
    assert "a stranger under false colours, an enemy" in judged[0].text
    made = [e for e in w.log if e.kind == "signal.made" and "private signal" in e.text]
    assert made and 600 <= made[0].tick <= judged[0].tick <= 1500
    assert w.captain.recognised[renard.id]["enemy"] is True
    assert [s for _, s in states][:3] == ["investigating a stranger", "chasing"][:2] or (
        "chasing" in [s for _, s in states]
    )
    chase = next(t for t, s in states if s == "chasing")
    assert judged[0].tick < chase <= judged[0].tick + 120
    assert w.readings.value("private_signal")["verdicts"][renard.id] == "wrong"
    # the privateer's own log: her bluff
    assert renard.crew is not None
    assert any("a guess" in e.text for e in renard.crew.log)
    # the chase goes after HIS stranger, about for her: south-west, not after the brig
    chased = [e for e in w.log if e.kind == "helm.set" and e.text.startswith("Gave chase")]
    assert chased and "Gave chase to a cutter" in chased[0].text, chased[0].text
    assert "on the other tack" in chased[0].text
    # a merchant brig challenged alone (the frigate off the Lizard, the brig a mile and a
    # half off) makes no answer in the table's five minutes: a merchantman who has none, a
    # stranger to be spoken, no enemy
    from tests.test_brains import put, world_at

    w2 = world_at(49.5, -5.5, intent="keep the station off the Lizard within 10 miles")
    w2.run(60)  # his captain has the deck: the challenge is his, not the player's
    from freesail.world.geo import destination

    off = destination(w2.position, 180.0, 1.5 * units.NAUTICAL_MILE)
    brig_v = put(
        w2,
        "merchant brig",
        "britain",
        {"lat_deg": off.lat_deg, "lon_deg": off.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Two Brothers",
    )
    brig: list = []
    for _ in range(40):
        w2.run(60)
        brig = [
            e for e in w2.log if e.kind == "signal.private_judged" and e.data["id"] == brig_v.id
        ]
        if brig:
            break
    assert brig and brig[0].data["verdict"] == "none" and brig[0].data["enemy"] is None
    assert "a merchantman, who has none" in brig[0].text


def test_truth_7_145_a_convoy_of_four_under_a_commodore_tacks_in_succession_on_one_hoist():
    """Spec M7 §6's third truth: the convoy (data/scenarios/convoy.yaml), four merchant
    brigs keeping company with the King's brig and under her orders, no model seated; the
    player's one hoist of the convoy book's No. 5 is read a minute after it is up by each
    master, answered with the pendant, and performed in succession: the leader at the
    reading and each of the rest three minutes after the one ahead of her, in the order of
    their making. At seed 7 the hoist is up at 798 (the hands slow at it: ordered at 600
    behind a wear), seen at 840, read at 900, and the four are about at 900, 1080, 1260
    and 1440 (840, 1020, 1200, 1380 while the hoist flew from the book's minute and not
    from the hands' finishing, mended in the package)."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(CONVOY)
    w = make_scenario_world(sf)
    begin(w, sf)
    names = ["Nancy", "Two Brothers", "Providence", "Friendship"]
    for n in names:
        v = w.vessels.find(n)
        assert v.under_orders_of == "the ship" and v.brain is None
    w.run(600)
    said = w.submit("make the signal to tack in succession")
    assert said.kind == "signal.ordered" and "No. 5, the convoy to tack in succession" in said.text
    about: dict[str, int] = {}
    up = None
    for _ in range(30):
        w.run(60)
        if up is None:
            made = [e for e in w.log if e.kind == "signal.made"]
            up = made[0].tick if made else None
        for n in names:
            v = w.vessels.find(n)
            if n not in about and any("went about" in words for _, words in (v.story or ())):
                about[n] = next(t for t, words in v.story if "went about" in words)
    assert up is not None and set(about) == set(names), about
    ticks = [about[n] for n in names]
    gaps = [b - a for a, b in zip(ticks, ticks[1:], strict=False)]
    assert ticks == sorted(ticks) and gaps == [180, 180, 180], gaps
    assert up + 60 <= ticks[0] <= up + 120
    answered = [e for e in w.log if e.kind == "signal.answered"]
    assert len(answered) == 4
    assert 780 <= up <= 840 and ticks == [900, 1080, 1260, 1440], (up, ticks)


def test_truth_7_146_a_telegraphic_sentence_takes_the_hoists_and_the_minutes_the_book_says():
    """Spec M7 §6's fourth truth: Nelson's sentence by Popham's 1803 book is twelve hoists
    (eight words of the dictionary and 'duty' spelt), a minute a hoist, read at the other
    end a minute after the last is up; the French and the basic books have no dictionary
    and the order is refused in words."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5)
    w.run(120)
    said = w.submit("make the telegraphic signal: England expects that every man will do his duty")
    assert said.kind == "signal.ordered" and "12 hoists, 12 minutes" in said.text
    assert "D 4, U 21, T 19, Y 24" in said.text
    locker = w.ship.extra["signals"]
    h = next(x for x in locker.flying if x.book == "telegraphic")
    assert h.numbers == (253, 269, 863, 261, 471, 958, 220, 370, 4, 21, 19, 24)
    ordered = int(w.clock.tick)
    assert h.breaks_out >= 10**12 and h.complete_at >= 10**12  # nothing up until the hands
    w.run(150)  # the hands at the halyards: the first hoist breaks out when they have it up
    assert ordered + 60 <= h.breaks_out <= ordered + 150, h.breaks_out
    assert h.complete_at >= 10**12  # the last hoist not yet up: not to be read before it is
    for _ in range(40):
        w.run(60)
        if any(e.kind == "signal.made" and "telegraphic" in e.text for e in w.log):
            break
    up = next(e for e in w.log if e.kind == "signal.made" and "telegraphic" in e.text)
    assert h.complete_at == up.tick  # read a minute after this
    minutes = (up.tick - ordered) / 60.0
    assert 12.0 <= minutes <= 16.0, minutes  # twelve nominal, stretched by the hands' pace
    hoists = [e for e in w.log if e.kind == "signal.hoist"]
    assert len(hoists) == 12 and "'expects' (269)" in hoists[1].text
    # a French ship has no dictionary: by meaning from the numerary, or not at all
    from freesail.world import signals as S

    with pytest.raises(S.BookFileError):
        S.load_books("france").encode("England expects")


def test_truth_7_147_a_signal_made_in_fog_is_a_gun_and_not_a_flag():
    """Spec M7 §6's last truth: in fog (the visibility under a mile) the same order makes
    the fog book's signal, a gun fired by the battery, heard and read by ear by a ship two
    miles off beyond the visibility (a near body at that distance, her lookout's sound
    sighting), answered and obeyed when she is under our orders; a bell at anchor is
    heard within the mile."""
    from tests.test_brains import put

    w = _sea_at(
        49.5,
        -5.5,
        CUTTER,
        datetime(1805, 6, 12, 10, 0),
        climatology=True,
        sky={"weather": "fog", "visibility": "a cable"},
    )
    w.run(60)
    assert w.conditions.visibility_nm < 1.0
    from freesail.world.geo import destination

    off = destination(w.position, 90.0, 2.0 * units.NAUTICAL_MILE)
    v = put(
        w,
        "brig-sloop",
        "britain",
        {"lat_deg": off.lat_deg, "lon_deg": off.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Harpy",
    )
    v.under_orders_of = "the ship"
    w.run(60)
    _guns_ready(w)
    w.run(10)
    said = w.submit("make the signal to heave to")
    assert said.kind == "signal.made" and "by gun: four guns, bring to" in said.text
    assert [e for e in w.log if e.kind == "signal.made"].__len__() == 1  # told once
    for _ in range(8):
        w.run(60)
    near = v.crew
    assert near is not None, "a sail two miles off is a near body (CREWED_NM)"
    kinds = [(e.kind, e.text) for e in near.log]
    heard = [t for k, t in kinds if k == "signal.read"]
    assert heard and "fires four guns: bring to" in heard[0], kinds[-12:]
    assert any(k == "signal.ordered" and "answering pendant" in t for k, t in kinds), kinds[-12:]
    assert any("heaving to (the signal from the ship: Bring to)" in t for _, t in kinds), kinds[
        -12:
    ]
    assert any(k == "ship.hove_to" for k, _ in kinds), kinds[-12:]
    # a bell at anchor in the fog is heard within the mile by the player's lookout
    from freesail.world.signals import vessel_locker

    close = destination(w.position, 270.0, 0.7 * units.NAUTICAL_MILE)
    rider = put(
        w,
        "merchant brig",
        "britain",
        {"lat_deg": close.lat_deg, "lon_deg": close.lon_deg},
        "bound for Falmouth",
        name="Nancy",
    )
    rider.plan = [("anchor", "")]
    rider.sail_state = "at anchor"
    vessel_locker(rider).fog_signals = True
    w.run(180)
    bells = [e for e in w.log if e.kind == "lookout.sighting" and "bell heard in the fog" in e.text]
    assert bells, [e.text for e in w.log if e.kind == "lookout.sighting"][-4:]


def test_truth_7_148_the_kings_cutter_engaging_to_leeward_never_puts_her_head_in_the_wind():
    """The brief's item 8 (the owner's first action, 2026-10-24): 70's engaging helm steered
    by the mark's bearing alone and turned the King's cutter through the wind's eye, aback
    with her carronades silent for half an hour. The law is `captains.helm_in_action`: no
    course in action within the close-hauled angle and half a point of the eye, the gage
    kept, the mark through the eye answered by the doctrine. At seed 7 no minute of the
    engagement finds her head within the close-hauled angle, no helm order says she will be
    taken aback, and the action ends at 11:12 with the privateer struck, fifty-nine minutes
    after the first shot (12:06 under 70's law: the tuning notes' bisection)."""
    from freesail.evolutions.scripts import close_hauled_true_angle
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    v = w.vessels.find("Renard")
    closest = units.rad_to_deg(close_hauled_true_angle(w.ship))
    in_eye = []
    struck = None
    for _ in range(3 * 60):
        w.run(60)
        if w.captain.state == "engaging":
            heading = units.rad_to_deg(float(w.ship.heading)) % 360.0
            wind = units.rad_to_deg(float(w.wind.direction_from)) % 360.0
            off = abs((heading - wind + 180.0) % 360.0 - 180.0)
            if off < closest - 2.0:
                in_eye.append((w.clock.tick, round(heading), round(off)))
        if v.struck or w.ship.extra.get("struck"):
            struck = w.clock.tick
            break
    assert not in_eye, in_eye
    assert not [e for e in w.log if "taken aback" in e.text and "wind's eye" in e.text]
    # package 73: the small arms served out on entering the action lengthen the first action
    # by half an hour (11:12 to 11:43; docs/dev/TuningNotes.md, package 73, the bisection)
    assert v.struck and struck is not None and 3600 <= struck <= 6600, struck
    battery = w.ship.extra["battery"]
    assert battery.rounds_fired >= 100  # 146 at seed 7; 51 under 70's law


def test_truth_7_149_a_shot_under_false_colours_is_a_pirates_act_told_once_and_witnessed():
    """Spec M7 §1 and §12's last truth: nothing fires under false colours without the log
    saying so and every stance turning. The King's cutter under French colours fires on a
    French privateer within sight of a British merchant brig: the first shot is told once
    (`action.false_colours`), the ship is an outlaw to the ports, and every captain whose
    people had her in sight holds her a pirate from then on, whatever colours she hoists."""
    from freesail.combat.guns import battery_of
    from tests.test_brains import put

    w = make_world(SEED, CUTTER, _action_scenario())
    _guns_ready(w)
    heading = float(w.ship.heading)
    v, enemy = _a_cutter_crewed(w, math.degrees(heading) + 90.0, 60.0, nation="france")
    enemy.ship.dyn.heading = heading
    witness = put(  # five and a half miles off to the north-west: in sight, a far body
        w,
        "merchant brig",
        "britain",
        "49 52 N 5 24 W",
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Two Brothers",
    )
    w.submit("hold your fire")
    w.submit("hoist French colours")
    assert w.readings.words("colours").startswith("false: French colours")
    w.run(65)
    w.submit("engage her to starboard")
    w.submit("fire")
    w.run(70)
    told = [e for e in w.log if e.kind == "action.false_colours"]
    assert len(told) == 1 and "a pirate's act" in told[0].text
    assert "under false colours" in str(w.ship.extra.get("outlaw"))
    assert not [e for e in w.log if e.kind == "action.unrecognised"]  # an enemy by her colours
    assert "the ship" in witness.brain.pirates and "the ship" in enemy.captain.pirates
    assert battery_of(w.ship).target == v.id
    w.submit("fire")
    w.run(70)
    assert len([e for e in w.log if e.kind == "action.false_colours"]) == 1  # told once
    w.submit("hoist the colours")
    assert "the ship" in witness.brain.pirates  # the witness holds her so whatever she hoists


def test_truth_7_150_a_light_is_seen_at_night_at_the_range_a_lantern_carries():
    """Spec M7 §5: by night a far ship showing a stern lantern is seen as a light at three
    miles, beyond the hull's loom at the mile, as a sighting of its own; darkened she is
    not; and `hoist the lights` is the ship's own order."""
    from tests.test_brains import put

    w = _sea_at(49.5, -5.5, CUTTER, datetime(1805, 6, 12, 23, 30))
    assert w.daylight == "night"
    w.run(60)
    from freesail.world.geo import destination

    off = destination(w.position, 45.0, 2.5 * units.NAUTICAL_MILE)
    where = {"lat_deg": off.lat_deg, "lon_deg": off.lon_deg}
    v = put(w, "merchant brig", "britain", where, "bound for Falmouth", name="Nancy")
    w.run(120)
    assert not [e for e in w.log if e.kind == "lookout.sighting" and "light" in e.text.lower()]
    from freesail.world.signals import vessel_locker

    vessel_locker(v).lights = "stern lantern"
    w.run(120)
    lights = [e for e in w.log if e.kind == "lookout.sighting" and e.text.startswith("A light")]
    assert lights, [e.text for e in w.log if e.kind == "lookout.sighting"][-3:]
    said = w.submit("hoist a stern lantern")
    assert said.kind == "lights.changed" and w.readings.words("lights") == "a stern lantern"
    said = w.submit("show no lights")
    assert said.kind == "lights.changed" and w.readings.words("lights") == "none"


@pytest.mark.pace
def test_truth_7_151_the_pace_with_a_convoy_of_four_under_orders_holds_the_floor():
    """The brief's item 10: a pace check for the work that runs for every far ship under
    orders (the least captain reading the flying hoists once a minute) and the lookout's
    reading of the flags: the convoy of four with a hoist flying, against the crewed floor
    (the brigs nearest the commodore are crewed under the cap); the conftest's floors are
    not lowered."""
    import time

    from freesail.world import crews as K
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(CONVOY)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(600)
    w.submit("make the signal to make more sail")
    w.run(200)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"


# ---------------------------------------------------------------------------
# Package 72: the naval system (spec M7 §21 to §23; truths 7-152 onward)
# ---------------------------------------------------------------------------

CONVOY_SIX = "data/scenarios/convoy-six.yaml"
BLOCKADE = "data/scenarios/blockade.yaml"
SQUADRON = "data/scenarios/squadron.yaml"


def _scenario_world(path: str):
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(path)
    w = make_scenario_world(sf)
    begin(w, sf)
    return w


def _off_station_m(w, sq) -> dict[str, float]:
    from freesail.world.geo import bearing_and_distance

    st = sq.stations(w)
    return {
        m: bearing_and_distance(w.vessels.get(m).position, st[m])[1]
        for m in sq.others()
        if m in st and w.vessels.get(m) is not None
    }


def test_truth_7_152_a_convoy_of_six_keeps_its_order_and_the_book_signals_the_straggler():
    """Spec M7 §21 and §23's first truth (the owner's scenario, data/scenarios/convoy-six.yaml):
    six merchant brigs under the King's brig-sloop are one set in the order of sailing, two
    columns at two cables, each on the station leg at far detail and under the orders of
    the player's ship; the slowest of them (the deep-laden Friendship, a dull sailer) sets
    the pace and starts a mile astern. The commodore's book (data/squadrons/convoy.yaml),
    read by the rules captain with no model seated, signals her a straggler (No. 20, the
    ships astern to make more sail) when she has been out of her station ten minutes, and
    she regains it; after two hours every ship is within a cable of her station and holds
    it. At seed 7: the signal ordered at 2040, up at 2182, answered at 2340; the Friendship
    back in her station at 6060 (package 88, item 1: the commodore's brig recovered from
    lying aback with no way after her tack, truth 7-340, where she lay so from 10:20 to 10:47
    and the convoy with her: 2760, 2866, 3000 and 6420 before, the same with the law's switch
    off on the final tree); (`squadron.in_station`; 5280 before package 84's step 6, when
    the privateer's World, on a clock of her own, never saw the private signal flying and made
    no answer; on the one clock she bluffs a reply, is judged an enemy, and the commodore
    closes the convoy round him first); at 7200 and after, every ship
    within 165 m of her station (the far station leg holds at the tolerance's edge, half a
    cable, and the lookout's rounding adds the rest)."""
    w = _scenario_world(CONVOY_SIX)
    sq = w.squadrons.find("the Falmouth trade")
    assert sq is not None and sq.kind == "convoy" and sq.commander == "the ship"
    assert sq.members == [
        "the ship",
        "nancy",
        "two-brothers",
        "providence",
        "hope",
        "mary-ann",
        "friendship",
    ]
    for m in sq.others():
        v = w.vessels.get(m)
        assert v.under_orders_of == "the ship" and v.plan[0] == ("station", "trade"), m
    w.run(7200)
    ordered = [e for e in w.log if e.kind == "signal.ordered" and "No. 20" in e.text]
    made = [e for e in w.log if e.kind == "signal.made" and "No. 20" in e.text]
    answered = [e for e in w.log if e.kind == "signal.answered"]
    back = [e for e in w.log if e.kind == "squadron.in_station" and "Friendship" in e.text]
    assert ordered and made and answered and back, (ordered, made, answered, back)
    when = (ordered[0].tick, made[0].tick, answered[0].tick, back[0].tick)
    # package 88 (the recovery when aback, `captains.ABACK_RECOVER`): (2760, 2866, 3000, 6420)
    # before and with the switch off; 5280 for the last before 84's step 6 (the one clock)
    assert when == (2040, 2182, 2340, 6060), when
    worst = 0.0
    for _ in range(6):
        w.run(600)
        worst = max(worst, max(_off_station_m(w, sq).values()))
    assert worst <= 165.0, worst
    assert not sq.stragglers and not sq.prizes


def test_truth_7_153_the_privateer_investigates_the_convoy_and_evades_the_escort_at_two_miles():
    """Spec M7 §22's privateer doctrine in the owner's scenario: the French schooner five
    miles to windward of the convoy makes it out, works down to investigate, and finding a
    man of war of the King's within her doctrine's distance (data/captains/privateer.yaml,
    `man_of_war_nm`) she evades and stands away; no merchantman is cut out, since none is
    uncovered. At seed 7 she is investigating at 600, evading by 3600 at two miles from the
    commodore, and twenty miles off by 10800."""
    w = _scenario_world(CONVOY_SIX)
    from freesail.world.geo import bearing_and_distance

    pv = w.vessels.find("Vengeur")
    assert pv is not None and pv.nation == "france" and pv.brain is not None
    w.run(600)
    assert pv.brain.state == "investigating a stranger", pv.brain.state
    w.run(3000)
    d_at_1h = bearing_and_distance(w.position, pv.position)[1] / units.NAUTICAL_MILE
    assert pv.brain.state == "evading" and 1.5 <= d_at_1h <= 3.0, (pv.brain.state, d_at_1h)
    w.run(7200)
    d_at_3h = bearing_and_distance(w.position, pv.position)[1] / units.NAUTICAL_MILE
    assert d_at_3h >= 15.0, d_at_3h
    sq = w.squadrons.find("the Falmouth trade")
    assert not sq.prizes and all(not w.vessels.get(m).struck for m in sq.others())


def test_truth_7_154_the_blockade_is_blown_off_brest_and_the_hortense_slips_out_after_the_gale():
    """Spec M7 §22's blockade (the owner's scenario, data/scenarios/blockade.yaml): the inshore
    squadron under a far commodore on the port's blockade station (`blockade Brest`: off
    the Black Rocks within six miles, data/ports/brest.yaml) with the Nimble in her wake;
    a scripted low brings a south-westerly gale; the blockade's book bears the squadron up
    for Torbay when the wind is a gale from the west, and restores the station when it is
    over; the French frigate in ordinary slips out when the offing (fifteen miles of the
    road, or the blockade station) has been clear of the King's men of war for an hour
    with the wind under a fresh breeze (data/regimes.yaml). At seed 7: blown off at 11400
    (the wind 34 knots from 226), the goal restored at 37920 (under 28 knots), the night
    lights at 38640, the Hortense out at 43200; the far Nimble within a cable of her
    station at the end of the gale and at the end of the day; the player's frigate on the
    Ushant station hove to through the gale and keeping her station after it."""
    w = _scenario_world(BLOCKADE)
    sq = w.squadrons.find("the inshore squadron")
    naiad, nimble, hortense = (w.vessels.find(n) for n in ("Naiad", "Nimble", "Hortense"))
    assert sq.book == "blockade" and sq.rendezvous == "Torbay" and sq.commander == naiad.id
    assert naiad.brain.intent_words == "blockade Brest"
    assert hortense.regime == "in ordinary" and hortense.brain is None
    w.run(28800)
    assert any(t == 11400 and "bound for Torbay" in words for t, words in sq.history), sq.history
    assert naiad.brain.intent_words == "bound for Torbay"
    assert hortense.regime == "in ordinary"
    assert w.captain.state == "hove to for weather"
    assert max(_off_station_m(w, sq).values()) <= units.CABLE
    w.run(21600)
    assert any(t == 37920 and "restored" in words for t, words in sq.history), sq.history
    assert naiad.brain.intent_words == "blockade Brest"
    sortie = [e for e in w.log if e.kind == "regime.sortie"]
    assert [e.tick for e in sortie] == [43200], sortie
    assert hortense.regime == "" and hortense.brain is not None
    assert hortense.intent_words == "cruise off the Lizard within 20 miles"
    assert w.captain.state == "keeping station"
    assert max(_off_station_m(w, sq).values()) <= units.CABLE


def test_truth_7_155_the_squadron_keeps_its_line_at_far_detail_and_through_the_promotion():
    """Spec M7 §21's second truth (the owner's scenario, data/scenarios/squadron.yaml): the
    Channel squadron, a frigate with a brig-sloop and a cutter in line ahead at two
    cables under a far commodore, keeps its line at far detail (one brain, two station
    legs) within half a cable; within the crewed distance of the player's frigate its
    three are promoted to full crews under the cap, and each promoted captain keeps her
    station by his book (`in company`: `keep your station` every two minutes), so that the
    line is kept through the promotion. At seed 7 with the cap at nought: every ship
    within a cable of her station at 3600 (the far leg holds at the tolerance's edge, half a
    cable, and the guide's turns add the rest). Under the default cap: all three crewed by 600,
    and at 7200 every ship within a cable and a half of her station, their captains in
    company."""
    from freesail.world import crews as K

    far = _scenario_world(SQUADRON)
    far.crewed_settings = {"cap": 0}
    sq = far.squadrons.find("the Channel squadron")
    assert sq.formation == "line ahead" and sq.members == ["medusa", "nimble", "sparrow"]
    far.run(3600)
    assert all(far.vessels.get(m).crew is None for m in sq.members)
    assert max(_off_station_m(far, sq).values()) <= units.CABLE, _off_station_m(far, sq)
    w = _scenario_world(SQUADRON)
    sq = w.squadrons.find("the Channel squadron")
    w.run(600)
    crewed = [m for m in sq.members if w.vessels.get(m).crew is not None]
    assert crewed == sq.members and K.CREWED_CAP >= 3, crewed
    w.run(6600)
    for m in sq.others():
        v = w.vessels.get(m)
        assert v.crew is not None and v.crew.captain.state == "in company", (m, v.crew)
    assert max(_off_station_m(w, sq).values()) <= 1.5 * units.CABLE, _off_station_m(w, sq)


def test_truth_7_156_the_succession_is_by_the_wake_each_ship_putting_about_at_the_turning_point():
    """Spec M7 §21 (the brief's item 3): a signal performed in succession is performed by
    each ship when she reaches the point where the ship ahead of her put about (the wake),
    which replaces package 71's three minutes between ships: a convoy at four cables and
    four knots and a half tacks in succession at the interval over the speed, five minutes
    or so, each gap the same within a minute; outside a set 71's gap stands."""
    from freesail.world import signals as S
    from tests.test_squadrons import convoy_world

    w, sq, harpy = convoy_world(brains=(False, False, False), formation="line ahead")
    sq.interval_m = 4.0 * units.CABLE
    w.run(7200)
    books = S.books_for_nation(w.nations, "britain")
    entry, q = books.find("tack in succession", "convoy")
    S.make_hoist(S.vessel_locker(harpy), books, entry, q, harpy.id, int(w.clock.tick))
    about: dict[str, int] = {}
    for _ in range(40):
        w.run(60)
        for m in sq.others():
            v = w.vessels.get(m)
            if m not in about and any("went about" in words for _, words in (v.story or ())):
                about[m] = next(t for t, words in v.story if "went about" in words)
    assert set(about) == set(sq.others()), about
    ticks = [about[m] for m in sq.others()]
    gaps = [b - a for a, b in zip(ticks, ticks[1:], strict=False)]
    assert ticks == sorted(ticks) and all(300 <= g <= 420 for g in gaps), gaps
    assert all(g != 180 for g in gaps), gaps


def test_truth_7_157_the_business_follows_the_ship_across_the_regions_edge_and_carries_the_convoy():
    """Spec M7 §22 (the owner's requirement of 2026-10-17): the business's region is
    wherever the player's ship is; crossing the Channel's edge at 3° W her business
    becomes the mid-Channel's, that region is peopled once, and a convoy sailing beside
    her is carried over whole. At seed 7 the schooner from six miles west of the edge
    crosses within two hours before a westerly, and the business's regions entered read
    the west then the mid-Channel."""
    from freesail.world.geo import Position, destination

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.6, "lon_deg": -3.2},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest", "dartmouth", "weymouth", "st-malo"],
        nation="britain",
        business="on",
        ship_heading_deg=110.0,
        ship_speed_kn=5.0,
    )
    w = make_world(SEED, "data/ships/topsail-schooner.yaml", sc)
    b = w.business
    assert b.region == "channel-west" and b.regions_entered == ["channel-west"]
    before = len(b.drawn)
    w.submit("set plain sail")
    w.submit("steer east-south-east")
    convoy = next(s for s in w.squadrons.sets if s.kind == "convoy")
    cdr = w.vessels.get(convoy.commander)
    here = destination(w.position, 180.0, 1.0 * units.NAUTICAL_MILE)
    shift = (here.lat_deg - cdr.position.lat_deg, here.lon_deg - cdr.position.lon_deg)
    for m in convoy.members:
        v = w.vessels.get(m)
        v.position = Position(v.position.lat_deg + shift[0], v.position.lon_deg + shift[1])
    crossed = None
    for _ in range(12):
        w.run(600)
        if b.region == "channel-mid":
            crossed = w.clock.tick
            break
    assert crossed is not None and crossed <= 7200, (b.region, w.position)
    assert b.regions_entered == ["channel-west", "channel-mid"]
    assert len(b.drawn) > before
    assert all(not w.vessels.get(m).done for m in convoy.members)


def test_truth_7_158_the_weathers_seasonal_bound_is_off_in_every_recorded_scenario():
    """R-39 as taken in package 72: the summed field's seasonal bound is built under the
    scenario's `weather_bound: seasonal` and off by default, so that no recorded passage
    moves; no scenario in data/scenarios says it, and a World made from any of them has
    the bound off. Under the switch the glass is held to the month's ceiling (the unit test
    in tests/test_squadrons.py)."""
    from pathlib import Path

    import yaml

    from freesail.world.scenarios import load_scenario, make_scenario_world

    said = []
    for path in sorted(Path("data/scenarios").rglob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(raw, dict) and raw.get("weather_bound") is not None:
            said.append(str(path))
    assert said == [], said
    sf = load_scenario("data/scenarios/gate-5a-day.yaml")
    w = make_scenario_world(sf)
    assert w.systems is not None and w.systems.bound is False
    assert "weather_bound" not in sf.scenario.to_dict()


def test_truth_7_159_the_pace_with_the_convoy_of_six_at_far_detail_holds_truth_51s_floor():
    """The brief's item 2 and 10: the convoy of six at far detail in truth 51's own form (the
    frigate of the brains' sea with the far ships beside her, as the frigate with the dozen
    is measured): a far brig-sloop commodore with his brain and the convoy's book, six
    merchant brigs without brains on the station leg, the set's minute, and a privateer
    schooner with her brain five miles to windward; the cap nought; the best of three
    thousands of ticks after the first ten minutes, at least BUILD_MACHINE_FLOOR. The
    scenario's own figure (the player's brig beating up Channel with her rules captain
    working her sails) is the tool's, `py tools/pace.py squadrons`, 483 to 551 on the build
    machine by the day's load (docs/dev/TuningNotes.md, package 72); the brig's sail-handling
    is the near crew model's cost and not the set's, which this truth measures apart."""
    import time

    from freesail.world.geo import destination
    from tests.test_brains import put
    from tests.test_squadrons import convoy_world

    w, sq, harpy = convoy_world(brains=(False, False, False, False, False, False), cap=0)
    p = destination(harpy.position, 45.0, 5.0 * units.NAUTICAL_MILE)
    put(
        w,
        "schooner",
        "france",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "patrolling off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        name="Vengeur",
    )
    assert len(sq.members) == 7 and all(w.vessels.get(m).crew is None for m in sq.members)
    w.run(600)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"


def test_truth_7_160_the_pace_with_the_convoy_of_six_under_the_cap_holds_truth_51s_floor():
    """The brief's item 2: the same convoy under the default cap (the merchantmen without
    brains stay far; the privateer and the player's ship crewed) and under a cap of
    twelve, at least the crewed floor; the conftest's floors are not lowered."""
    import time

    from freesail.world import crews as K

    for cap in (None, 12):
        w = _scenario_world(CONVOY_SIX)
        if cap is not None:
            w.crewed_settings = {"cap": cap}
        w.run(600)
        best = 0.0
        for _ in range(3):
            t0 = time.perf_counter()
            w.run(1000)
            best = max(best, 1000 / (time.perf_counter() - t0))
        assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second under a cap of {cap}"


# ---------------------------------------------------------------------------
# Practice and resupply (the owner's, built between packages 72 and 73 and folded in by
# package 86 after 73; docs/design/Build-PracticeAndResupply.md §8.2; truths 7-161 to
# 7-171): practice at the great guns (a cask hove over for a mark, a notional mark at the
# captain's word, dumb show) and powder and shot taken in at a port (the magazine by gun
# kind, the gunner's filling from the powder below, the Ordnance's issue free to a King's
# ship, the merchants' sale paid at alongside, the hoy and the galley fire). The digests
# differ on the owner's Windows machine (docs/dev/TuningNotes.md, package 72): states,
# kinds, counts and bands are pinned, a digest measured there or on the build machine is
# quoted in the docstring, and two digests are compared only when both are made in the
# same run.
# ---------------------------------------------------------------------------

PRIVATEER = "data/ships/privateer-schooner.yaml"
EXERCISING = "data/scenarios/exercising-the-great-guns.yaml"
THE_SOUND = {"lat_deg": 50.345, "lon_deg": -4.150}  # the anchorage in Plymouth Sound
HAMOAZE = {"lat_deg": 50.3760, "lon_deg": -4.1916}  # the Hamoaze, Plymouth's harbour
CASCAIS_ROAD = {"lat_deg": 38.6910, "lon_deg": -9.4100}  # Lisbon's outer road
# The director's world order (data/director/aboard.yaml): a quarter of every kind's filled
# cartridges struck off the gunner's count, the barrels below left alone; an input, so a
# replay gives it again.
DAMP = "aboard: the cartridges found damp"
MAGAZINE_OUT = (
    "The gunner reports no more cartridges for the 12-pounder carronades: the magazine is out."
)


def _anchored(
    where,
    ship=CUTTER,
    start=datetime(1805, 6, 10, 10, 0),
    chart="channel-west",
    ports=("plymouth", "falmouth"),
    **kw,
):
    """A ship brought up where she is put at seed 7 (tests/test_ordnance.py's world): a
    south-westerly moderate breeze, the best bower let go by the order in her second minute
    and five minutes given to bring up; in port at the spot nearest her."""
    kw.setdefault("nation", "britain")
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
        position=where,
        chart=chart,
        ports=list(ports),
        **kw,
    )
    w = make_world(SEED, ship, sc)
    w.run(60)
    w.submit("let go the best bower")
    w.run(300)
    assert w.at_anchor and w.dealings.in_port() is not None
    return w


def _gunners_fills(mag) -> dict:
    """The cartridges the gunner filled for each kind, read from the gunner's own count: the
    filled now, less the kind's allowance, and the rounds it took added back."""
    return {k: mag.filled_of(*k) - n + mag.fired.get(k, 0) for k, n in mag.level.items()}


def test_truth_7_161_the_first_action_is_untouched_by_the_magazine_by_kind_filling_and_practice():
    """The build design's §4 and decision 26: the first action (data/scenarios/
    first-action.yaml, truth 7-133's) played again by the rules captains with the magazine
    kept by gun kind, the gunner filling at quarters from the powder below, and practice's
    marks, readings and stream in the build. At seed 7 on the owner's tree (before package
    73) the privateer opens at 10:13 (tick 781) and strikes at 11:12 (4320), fifty-nine
    minutes after, as before the work; no line
    of the filling, of practice or of the supply in either ship's log, and no practice
    stream; the Renard's 3-pounders fall back from chain shot at 10:20 in package 72's
    words and data (her own log's time: her crewed World begins a minute after ours, so
    her tick 1140 is 10:20; the review's finding, this docstring having said 10:19). The
    King's cutter took 149 of her 330 cartridges and her gunner filled 26 at quarters from
    the 200 pounds below, so that 207 are filled and 174 pounds below at the strike; the
    Renard's gunner filled 28 (26 for her long 3-pounders, 2 for her swivels), the filling
    moving powder from the barrels into cartridges and nothing else.
    Measured on the owner's machine at the strike: 311 lines and the digest
    a158a30ce39b345d, on his local baseline and on his merged tree alike (decision 26:
    recorded and not pinned, the digests differing there). On the build machine at package
    86's fold-in, on top of package 73 (whose small arms served on entering the action move
    the minute, its own bisection): she strikes at 11:43 (6180, ninety minutes after the
    first shot, inside 7-133's band), the chain shot falling back at 10:20 as before; the
    King's cutter took 211 of her 330 cartridges and her gunner filled 40, so that 159 are
    filled and 160 pounds below at the strike; the Renard's gunner filled 41 (39 for her
    long 3-pounders, 2 for her swivels); 390 lines and the digest fde496ab303d4af9, the
    Renard's own log 264 lines and 94f8df0c29462ed0 (recorded, not pinned)."""
    from freesail.ship.parts import magazine
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    v = w.vessels.find("Renard")
    first = None
    struck_tick = None
    for _ in range(3 * 60):
        w.run(60)
        if first is None:
            fired_at = [e for e in w.log if e.kind == "action.fired_at"]
            if fired_at:
                first = fired_at[0].tick
        if v.struck or w.ship.extra.get("struck"):
            struck_tick = w.clock.tick
            break
    assert first is not None and v.struck and not w.ship.extra.get("struck")
    # truth 7-133's band; 3539 s at seed 7 on the owner's tree, 5399 s with package 73
    assert 2700 <= struck_tick - first <= 3 * 3600, f"{(struck_tick - first) / 60:.0f} min"
    enemy = v.crew
    new = ("guns.filling", "guns.filled", "guns.powder_out", "practice.", "ordnance.")
    for log in (w.log, enemy.log):
        assert not [e.kind for e in log if e.kind.startswith(new)]
    assert "practice" not in w.rng.stream_names()
    fell_back = [e for e in enemy.log if e.kind == "guns.magazine_empty"]
    assert [e.text for e in fell_back] == [
        "The gunner reports no more chain shot for the long 3-pounders: they load with round shot."
    ]
    assert fell_back[0].data == {"pounder": 3.0, "charge": "chain", "instead": "round"}
    # said in her own log by her own clock, once her guns are firing (10:20 at seed 7)
    opened = [e for e in enemy.log if e.kind == "action.fired"]
    assert opened and opened[0].ship_time <= fell_back[0].ship_time
    mag = magazine(w.ship)
    key = ("carronade", 12.0)
    assert mag.level == {key: 330} and mag.reserve_lb == 200.0 and mag.charge_of(*key) == 1.0
    assert mag.fired[key] >= 100 and mag.filled_by_gunner > 0  # 149 and 26 at seed 7
    assert mag.filled_of(*key) == 330 - mag.fired[key] + mag.filled_by_gunner
    assert mag.powder_lb == 200.0 - mag.filled_by_gunner
    for ship in (w.ship, enemy.ship):
        m = magazine(ship)
        fills = _gunners_fills(m)
        assert all(n >= 0 for n in fills.values()) and sum(fills.values()) == m.filled_by_gunner
        spent = sum(n * m.charge_of(*k) for k, n in fills.items())
        assert m.powder_lb == pytest.approx(m.reserve_lb - spent), ship.name


def test_truth_7_162_the_frigate_knocks_a_cask_to_staves_at_two_cables_and_nobody_is_an_outlaw():
    """The build design's §6: a cask for a mark is no sail. The frigate at quarters with her
    guns loaded (truth 7-135's world); an empty cask put in the water by the test two cables
    off her starboard beam, as truth 7-134 puts the cutter, is made out by the masthead and
    engaged by the order (`engage the cask to starboard`): her starboard guns fire as they
    bear, the first shot that strikes knocks it to staves, said once, and the mark is
    cleared and the guns silent after. At seed 7 the first minute's thirteen shot fall five
    over and eight wide, and the fifteenth round, No. 16 starboard gun's at 393 m, strikes
    it ("The mark struck by No. 16 starboard gun at two cables and knocked to staves; the
    guns hold their fire for want of a mark."); over seeds 1 to 20 the strike came at the
    3rd to the 46th round, 12 on the median (the cask's size term about 0.16, decision 18),
    so the band is the first sixty. Nothing of an action's follows: no recognition, false
    colours, outlaw, morale or strike; the rounds are practice (`last_practice_tick`, never
    `last_fired_tick`), counted against the month's allowance for exercise (six charges,
    said once beyond it). Each kind's filled cartridges are its allowance (2054 for the
    long 18-pounders) less the rounds it took and more the gunner's filling for it, and
    that filling is all the powder that left the barrels below."""
    from freesail.combat import marks
    from freesail.combat.guns import battery_of
    from freesail.ship.parts import magazine
    from freesail.world.geo import destination
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    _guns_ready(w)
    w.run(40)
    ship = w.ship
    there = destination(w.position, math.degrees(float(ship.heading)) + 90.0, 2.0 * units.CABLE)
    cask = marks.Cask(f"{marks.PRACTICE_PREFIX}cask-1", there, int(w.clock.tick))
    ship.extra["practice"] = marks.Practice(cask=cask, serial=1)
    w.run(60)
    assert marks.cask_in_sight(w, cask)
    said = w.submit("engage the cask to starboard")
    assert said.kind == "guns.engage" and said.data["target"] == cask.id, said.text
    battery = battery_of(ship)
    before = battery.rounds_fired
    rounds = None
    for _ in range(30 * 60):
        w.run(1)
        if rounds is None and cask.gone == "struck":
            rounds = battery.rounds_fired - before
        if any(e.kind == "practice.mark_struck" for e in w.log):
            break
    assert rounds is not None and 1 <= rounds <= 60, rounds  # the fifteenth at seed 7
    (line,) = [e for e in w.log if e.kind == "practice.mark_struck"]
    assert line.text.startswith("The mark struck by ") and line.text.endswith(
        "and knocked to staves; the guns hold their fire for want of a mark."
    )
    assert line.data["id"] == cask.id and line.data["range_m"] <= 3.0 * units.CABLE
    assert battery.target is None and battery.target_words == ""
    w.run(120)
    assert not [e for e in w.log if e.kind == "action.fired" and e.tick > line.tick]
    assert len([e for e in w.log if e.kind == "practice.mark_struck"]) == 1
    kinds = {e.kind for e in w.log}
    assert not kinds & {"action.unrecognised", "action.false_colours", "action.enemy_struck"}
    assert "outlaw" not in ship.extra and "morale" not in ship.extra
    assert battery.last_fired_tick is None and battery.last_practice_tick is not None
    assert len([e for e in w.log if e.kind == "practice.beyond_allowance"]) == 1
    falls = w.readings.value("practice")["falls"]
    assert set(falls) == {"2"} and falls["2"]["struck"] == 1, falls
    mag = magazine(ship)
    assert mag.level[("long", 18.0)] == 2054
    fills = _gunners_fills(mag)
    assert all(n >= 0 for n in fills.values()) and sum(fills.values()) == mag.filled_by_gunner
    assert mag.filled_of("long", 18.0) == 2054 - mag.fired[("long", 18.0)] + fills[("long", 18.0)]
    spent = sum(n * mag.charge_of(*k) for k, n in fills.items())
    assert mag.powder_lb == pytest.approx(mag.reserve_lb - spent)


def test_truth_7_163_the_shot_at_a_mark_tells_more_often_at_two_cables_than_at_four():
    """The build design's §6 (the judges' graft: a struck cask ends a run, so the ranges are
    compared at a notional mark): the frigate at quarters engages, by the order, a mark on
    her starboard beam twenty minutes at two cables and twenty at four; the minute's line
    says the shot "on the mark", `the range` is the mark's, and the practice reading keeps
    the falls by cables. At seed 7: 70 on the mark of 237 rounds at two cables (30 per
    cent), 27 of 237 at four (11 per cent); the hit chance's own tables, the range alone
    between them."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    _guns_ready(w)
    w.run(40)
    for cables, figure in (("two", 2), ("four", 4)):
        said = w.submit(f"engage a mark {cables} cables on the starboard beam")
        assert said.kind == "guns.engage" and said.data["mark"] == "notional", said.text
        t0 = w.clock.tick
        w.run(20 * 60)
        lines = [e for e in w.log if e.kind == "action.fired" and e.tick > t0 + 60]
        assert lines and all(e.data.get("mark") == "notional" for e in lines)
        assert any(" on the mark" in e.text for e in lines), [e.text for e in lines]
        assert w.readings.words("range") == f"{figure} cables"
    falls = w.readings.value("practice")["falls"]
    assert set(falls) == {"2", "4"}, falls
    fired = {c: sum(row.values()) for c, row in falls.items()}
    share = {c: falls[c].get("struck", 0) / fired[c] for c in falls}
    assert min(fired.values()) >= 100, fired  # 237 at each range at seed 7
    assert share["2"] > share["4"] > 0.0, share  # 70/237 and 27/237 at seed 7


def test_truth_7_164_dumb_show_serves_the_guns_at_the_actions_pace_and_spends_nothing():
    """The build design's §6 and decisions 20 and 21: `exercise the starboard battery` given
    at quarters before `cast loose the guns`, so that every cycle begins empty; for twenty
    minutes the starboard crews serve their guns through the phases at the action's pace,
    and nothing leaves the magazine. At seed 7 the long 18-pounders' sponge to point is
    105 s on the mean of 131 timed cycles, inside truth 7-135's band (the live interval
    between discharges 104 s with the full company), the 9-pounder chasers' best 56 s
    (their mean 70 s; the review of the owner's work found the best written as the mean);
    a line `practice.exercise` every minute from 10:04, when the first cycles end, to the last;
    the magazine as it was, no round fired, no `action.fired`, the gunnery stream never
    opened. The practice reading says the pace in words (it said 'a minute and 16 seconds'
    for the carronades until this truth: the teens are now words). Both batteries at once
    split each gun crew between its two guns, as engaging on both sides does, and the
    18-pounders then take 406 s (measured, not pinned)."""
    import copy

    from freesail.ship.parts import magazine
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    mag = magazine(w.ship)
    start = copy.deepcopy(vars(mag))
    w.submit("beat to quarters")
    w.run(5)
    said = w.submit("exercise the starboard battery")
    assert said.kind == "guns.exercise" and said.data["side"] == "starboard"
    assert said.text.endswith("The guns are not yet cast loose: say 'cast loose the guns'.")
    w.submit("cast loose the guns")
    t0 = w.clock.tick
    w.run(20 * 60)
    practice = w.readings.value("practice")
    assert practice["exercise"] == "starboard" and practice["live"] == 0
    timed = {
        gid: d
        for gid, d in practice["guns"].items()
        if d["cycles"] and w.ship.guns[gid].kind == "long" and w.ship.guns[gid].pounder == 18.0
    }
    assert timed and all(w.ship.guns[gid].side == "starboard" for gid in timed)
    cycles = sum(d["cycles"] for d in timed.values())
    mean = sum(d["mean_s"] * d["cycles"] for d in timed.values()) / cycles
    assert 90.0 <= mean <= 125.0, f"{mean:.0f} s"  # truth 7-135's band; 105 s at seed 7
    pace = [p for p in practice["words"].split("; ") if "from sponge to point" in p]
    assert pace and not [p for p in pace if re.search(r"\d+ (?:second|minute)", p)], pace
    assert vars(mag) == start
    guns = w.readings.value("guns")
    assert guns["rounds_fired"] == 0 and guns["loaded"] == 0 and guns["exercise"] == "starboard"
    assert "gunnery" not in w.rng.stream_names()
    assert not [e for e in w.log if e.kind == "action.fired"]
    minutes = sorted({e.tick // 60 for e in w.log if e.kind == "practice.exercise"})
    assert minutes and minutes[0] <= (t0 + 5 * 60) // 60, minutes  # 10:04 at seed 7
    assert minutes == list(range(minutes[0], w.clock.tick // 60 + 1)), minutes


def test_truth_7_165_a_notional_mark_serves_by_night_and_in_fog():
    """The build design's §3.3 and decision 27: by night a cask over the side could not be
    seen from the masthead and the heave is refused; in fog it is seen only within the
    visibility (`marks.seen_range_nm`), so that a mark at four cables is a notional one; a
    notional mark serves in both, the captain's word of a mark at a bearing from her head
    and a range, a cutter's length beam-on, which nobody sees. The frigate at 02:00 on 12
    June is refused the heave in the order's words; at 02:00 and again in a fog of a cable
    at 10:00 (truth 7-147's sky) she engages a mark four cables on the starboard beam: her
    starboard guns fire on it, the minute's line says the shot on the mark, `the range` is
    the stated four cables exactly (no lookout's estimate in it), and no mark is sighted (no
    sighting of the cask's kind, no practice stream, the practice reading's mark not in
    sight). In the fog the heave is not refused, the order's only refusals being no chart
    and the night (the review's finding: this docstring said a cask could not be seen in
    fog). At seed 7 in ten minutes: 114 rounds and 11 on the mark by night, 121 and 8 in
    the fog."""
    from freesail.combat.guns import battery_of

    fog = {"climatology": True, "sky": {"weather": "fog", "visibility": "a cable"}}
    for when, kw in ((datetime(1805, 6, 12, 2, 0), {}), (datetime(1805, 6, 12, 10, 0), fog)):
        w = _sea_at(49.5, -5.5, FRIGATE, when, **kw)
        w.run(60)
        if kw:
            assert w.daylight == "day" and w.conditions.visibility_nm < 1.0
        else:
            assert w.daylight == "night"
            said = w.submit("heave a cask overboard")
            assert said.kind == "order.rejected" and said.data["reason"] == (
                "It is dark: a cask over the side would not be seen from the masthead; a "
                "notional mark serves by night ('engage a mark four cables on the starboard "
                "beam')."
            )
        _guns_ready(w)
        said = w.submit("engage a mark four cables on the starboard beam")
        assert said.kind == "guns.engage" and said.data["target"] == "practice:notional"
        t0 = w.clock.tick
        w.run(10 * 60)
        lines = [e for e in w.log if e.kind == "action.fired" and e.tick > t0]
        assert any(" on the mark" in e.text for e in lines), [e.text for e in lines]
        assert battery_of(w.ship).rounds_fired > 0
        reading = w.readings.value("range")
        assert reading["metres"] / units.CABLE == 4.0 and reading["words"] == "4 cables"
        mark = w.readings.value("practice")["mark"]
        assert mark["kind"] == "notional" and mark["range_cables"] == 4.0
        assert mark["in_sight"] is False
        assert not [s for s in w.lookout.sightings if s.seen_as == "cask"]
        assert not [e for e in w.log if e.kind.startswith("practice.mark")]
        assert "practice" not in w.rng.stream_names()
        if kw:
            # in the fog by day the heave is not refused: a cask is seen within the cable
            assert w.submit("heave a cask overboard").kind == "order.accepted"


def test_truth_7_166_a_cask_lost_in_haze_holds_fire_is_told_each_way_and_given_up_at_three_miles():
    """The build design's §6: the frigate standing north under plain sail on a hazy
    forenoon (the scenario's sky pinned hazy, the visibility a mile), at quarters, heaves a
    cask over from the lee quarter and engages it on both sides. At seed 7 she leaves it
    astern and the masthead loses it in the haze at 10:25, a mile and a sixth off ("The
    mark is lost to sight in the haze."): while it is unseen the battery keeps it for its
    mark but has nothing to lay for (`action.target_of` gives none), and no round is fired;
    she wears for it and it is made out again at 10:35, seven cables ahead, and her bow
    chasers open on it at once; she holds her fire, passes it and stands on; the masthead
    loses it again at 11:03, and at 11:31 it is given up three miles astern ("The mark is
    lost astern, three miles off."), the battery's mark cleared. Each change of the
    masthead's sight is told once and never twice running: lost, made out again, lost. A
    cask is never seen beyond a mile, so it is always lost to sight before it is three
    miles off: the third line is that loss (the design's "once each way" read so). On the
    build machine at package 86's fold-in: 88 lines and the digest 970914c3a0a4d170 at the
    test's end (recorded, not pinned; the owner recorded none)."""
    from freesail.combat import marks
    from freesail.combat.action import target_of
    from freesail.combat.guns import FireMode, battery_of

    w = _sea_at(
        49.5,
        -5.5,
        FRIGATE,
        datetime(1805, 6, 12, 10, 0),
        climatology=True,
        sky={"sky": "hazy", "weather": "fine", "visibility": "a mile"},
        ship_heading_deg=0.0,
        ship_speed_kn=6.0,
    )
    w.run(60)
    assert w.readings.words("visibility") == "a mile"
    w.submit("set plain sail")
    w.run(120)
    _guns_ready(w)
    assert w.submit("heave a cask overboard").kind == "order.accepted"
    w.run(150)
    cask = marks.cask_in_water(w.ship)
    assert cask is not None and marks.cask_in_sight(w, cask)
    assert w.submit("engage the cask on both sides").kind == "guns.engage"
    battery = battery_of(w.ship)
    p = marks.practice_of(w.ship)
    stage = "standing on"
    unseen: list[int] = []  # the rounds fired, each minute it is lost before she wears back
    seen_at = resumed = None
    for _ in range(150):
        w.run(60)
        if cask.gone:
            break
        if stage == "standing on" and p.sight == "lost":
            assert w.submit("wear ship").kind == "order.accepted"
            stage = "wearing back"
        elif stage == "wearing back" and p.sight == "seen":
            stage, seen_at = "in sight again", battery.rounds_fired
        elif stage == "in sight again" and battery.rounds_fired > seen_at:
            resumed = battery.rounds_fired - seen_at
            assert w.submit("hold your fire").kind == "guns.mode"
            stage = "standing away"
        if stage == "wearing back" and not marks.cask_in_sight(w, cask):
            assert battery.target == cask.id and target_of(w, cask.id) is None
            assert not w.readings.value("practice")["mark"]["in_sight"]
            unseen.append(battery.rounds_fired)
    assert stage == "standing away" and cask.gone == "lost", (stage, cask.gone)
    assert unseen and set(unseen) == {0}, unseen
    assert resumed, "no round fired on the cask when it was made out again"
    sight = [e for e in w.log if e.kind == "practice.mark_sight"]
    assert [e.data["seen"] for e in sight] == [False, True, False], [e.text for e in sight]
    assert sight[0].text == sight[2].text == "The mark is lost to sight in the haze."
    assert re.fullmatch(
        r"The mark is made out again, bearing [NSEW by]+, about \w+ cables\.", sight[1].text
    )
    (lost,) = [e for e in w.log if e.kind == "practice.mark_lost"]
    assert lost.text == "The mark is lost astern, three miles off." and lost.data["gone"] == "lost"
    assert lost.data["range_m"] >= 3.0 * units.NAUTICAL_MILE
    assert battery.target is None and battery.mode is FireMode.HOLD
    assert not [e for e in w.log if e.kind == "practice.mark_struck"]


def test_truth_7_167_in_the_sound_the_kings_cutter_completes_her_magazine_from_the_ordnance_free():
    """The build design's §5 and the owner's ruling (the Ordnance's issue to a King's ship
    free and vouched; the galley fire out a state the needs read): the King's cutter at
    anchor in Plymouth Sound with her powder spent (set by the test: the hours of firing
    that would spend two barrels are not sailed here) and three cartridges filled; at
    quarters her guns load those three and the gunner reports the magazine out. At seed 7
    `take in powder and shot` at 07:41 demands five barrels and three round shot of the
    Ordnance's storekeeper, issued and vouched, the purse untouched throughout; the hoy is
    alongside at 11:41, four hours on, the galley fire put out (Art. V), the port's and the
    stores' readings saying so, the captain's meal below cold and the company's dinner at
    noon served cold; the powder struck down at 12:41, the hour the taking in takes at the
    least, the fire lit again and the gunner's account written up by the boatswain. The
    magazine wants nothing from the stowing (the powder below is reckoned with the filled
    cartridges), and the gunner fills by day alone, out of quarters, from 12:41 to 20:00
    and from 06:00 on the 11th, until at 11:04 he has the 330 filled ("The gunner has the
    cartridges filled to the allowance: 330 for the 12-pounder carronades; 1 barrel and 70
    pounds below."). Spent again (by the test, as before) after her empty guns have loaded,
    the magazine out is said again: a receipt and a cartridge taken clear the once-said
    line (decision 7), which before this work was said once a calibre and never again. On
    the build machine at package 86's fold-in: 128 lines and the digest 1097aab244230e03
    at the test's end (recorded, not pinned; the owner recorded none)."""
    from freesail.ship.parts import magazine

    w = _anchored(
        THE_SOUND,
        start=datetime(1805, 6, 10, 7, 30),
        papers={"service": "kings"},
        cargo={"purse_pounds": 100.0},
    )
    assert w.dealings.in_port().nearest_spot(w.position)[0].name == "the anchorage in the Sound"
    mag = magazine(w.ship)
    key = ("carronade", 12.0)
    mag.powder_lb = 0.0
    mag.set_filled(*key, 3)
    _guns_ready(w)
    out = [e for e in w.log if e.kind == "guns.magazine_empty"]
    assert [e.text for e in out] == [MAGAZINE_OUT]
    assert out[0].data == {"pounder": 12.0, "charge": "round"}  # package 72's
    w.submit("secure the guns")
    w.run(150)
    purse = (w.purse.pounds, list(w.purse.entries))
    demand = w.submit("take in powder and shot")
    assert demand.kind == "ordnance.demanded", demand.text
    assert "of the Ordnance's storekeeper at Plymouth, issued and vouched;" in demand.text
    assert demand.data["how"] == "issue" and demand.data["cost_pounds"] == 0.0
    assert demand.data["barrels"] == 5 and demand.data["due_tick"] == demand.tick + 4 * 3600
    assert w.readings["port"]["hoy"]["stage"] == "coming off"
    w.run(demand.data["due_tick"] - w.clock.tick + 1)
    (alongside,) = [e for e in w.log if e.kind == "ordnance.alongside"]
    assert alongside.tick == demand.tick + 4 * 3600
    assert w.stores.galley_fire_out == "powder"
    assert w.readings["stores"]["words"].endswith(
        ", the galley fire out while the powder comes aboard"
    )
    assert w.readings["port"]["hoy"]["stage"] == "alongside"
    w.submit("go below")
    said = w.submit("eat")
    assert said.text.startswith(
        "A cold meal, biscuit and cheese, the galley fire being out while the powder comes "
        "aboard; you eat"
    ), said.text
    w.submit("go on deck")
    while not [e for e in w.log if e.kind == "ordnance.stowed"]:
        w.run(60)
    (stowed,) = [e for e in w.log if e.kind == "ordnance.stowed"]
    assert stowed.tick == alongside.tick + 3600  # five barrels and three shot: the least hour
    assert stowed.text.startswith("Five barrels of powder and 3 round shot of 12 pounds struck")
    assert "issued by the Ordnance's storekeeper and vouched" in stowed.text
    assert stowed.text.endswith("the galley fire lit again.")
    assert w.stores.galley_fire_out == "" and w.stores.cold_meals >= 1  # dinner at noon
    written = [e for e in w.log if e.kind == "paper.written" and e.tick == stowed.tick]
    assert written and written[0].data == {"paper": "the gunner's account"}
    assert written[0].text.startswith("The gunner's account written up by the boatswain:")
    assert mag.account[-1][1].startswith(
        "Received of the Ordnance's storekeeper at Plymouth, issued and vouched: 5 barrels"
    )
    assert mag.powder_lb == 500.0 and mag.wanting().empty
    samples = []
    filled = []
    while not filled:
        w.run(600)
        samples.append((w.clock.ship_time, mag.filled_of(*key)))
        filled = [e for e in w.log if e.kind == "guns.filled"]
    night = {n for t, n in samples if t.hour >= 20 or t.hour < 6}
    assert len(night) == 1 and 0 < night.pop() < 330  # none filled by night
    (done,) = filled
    assert done.text == (
        "The gunner has the cartridges filled to the allowance: 330 for the 12-pounder "
        "carronades; 1 barrel and 70 pounds below."
    )
    at = w.clock.ship_time - timedelta(seconds=w.clock.tick - done.tick)
    assert at.day == 11 and 6 <= at.hour < 20, at  # 11:04 at seed 7, by day and out of quarters
    assert mag.filled_of(*key) == 330 and not mag.short and mag.wanting().empty
    assert mag.powder_lb == 170.0 and mag.filled_by_gunner == 330
    assert (w.purse.pounds, list(w.purse.entries)) == purse
    _guns_ready(w)  # her three empty guns load from the filled cartridges
    mag.set_filled(*key, 0)
    mag.powder_lb = 0.0
    assert w.submit("engage a mark three cables on the starboard beam").kind == "guns.engage"
    w.run(600)
    out = [e for e in w.log if e.kind == "guns.magazine_empty"]
    assert [e.text for e in out] == [MAGAZINE_OUT, MAGAZINE_OUT]
    assert not [e for e in w.log if e.kind in ("guns.filling", "guns.powder_out")]


def test_truth_7_168_powder_is_taken_in_at_the_road_not_the_harbour_and_bought_only_of_necessity():
    """The build design's §3.2 and §5: the Regulations of 1806 (1808 printing), the Gunner,
    Art. VI, "Plymouth Sound or Cawsand Bay", and the Captain's "absolute necessity" (Art.
    VII). Each ship made short by the director's damp cartridges (an input), at seed 7: the
    King's cutter in the Hamoaze is refused in the article's words; at Falmouth, where
    there is no storekeeper of the Ordnance, she is refused until her captain says it is of
    necessity, and then buys a barrel of the merchants for £5, the purse paying at
    alongside three hours on and once only; the merchant brig at Falmouth buys hers for £5
    with no word of necessity; the privateer is refused the Ordnance's issue at Plymouth,
    whose town sells none (decision 10); and at Lisbon, a neutral's port, a French
    privateer is refused once the knob is set on the loaded block (`sells_in_war_to`:
    Britain alone, decision 11) and served when it is unset. On the build machine at
    package 86's fold-in, the five worlds in the test's order: 14 lines (0161fac3dbb5c5c0),
    33 (82d197d2b2bd54e9), 32 (d3fe2cae0f223882), 15 (091a213c34c1ffb8) and 16
    (7143cf8a33ad1d9a) (recorded, not pinned; the owner recorded none)."""
    from freesail.ship.parts import magazine

    harbour = _anchored(HAMOAZE, papers={"service": "kings"}, cargo={"purse_pounds": 100.0})
    assert harbour.dealings.in_port().nearest_spot(harbour.position)[0].name == "the Hamoaze"
    harbour.world_order(DAMP)
    assert not magazine(harbour.ship).wanting().empty
    said = harbour.submit("take in powder and shot")
    assert said.kind == "order.rejected" and said.data["reason"] == (
        "Powder is taken in at Plymouth Sound or Cawsand Bay, not in the harbour (the "
        "Regulations, the Gunner, Art. VI): weigh and bring her to the road first."
    )
    assert not harbour.dealings.jobs
    kings = _anchored(CARRICK_ROAD_5C, papers={"service": "kings"}, cargo={"purse_pounds": 100.0})
    kings.world_order(DAMP)
    said = kings.submit("take in powder and shot")
    assert said.kind == "order.rejected" and said.data["reason"] == (
        "There is no storekeeper of the Ordnance at Falmouth, and a captain is charged not to "
        "purchase stores without an absolute necessity (the Regulations): say 'buy powder of "
        "necessity' to buy it of the merchants at £5 a barrel."
    )
    brig = _anchored(CARRICK_ROAD_5C, ship=MERCHANT_BRIG, cargo={"purse_pounds": 100.0})
    brig.world_order(DAMP)
    for w, order, necessity in (
        (kings, "buy powder of necessity", True),
        (brig, "buy powder and shot", False),
    ):
        entries = len(w.purse.entries)
        demand = w.submit(order)
        assert demand.kind == "ordnance.demanded", demand.text
        assert demand.data["how"] == "sale" and demand.data["necessity"] is necessity
        assert demand.data["barrels"] == 1 and demand.data["cost_pounds"] == 5.0
        assert w.purse.pounds == 100.0  # paid when the hoy comes alongside
        w.run(demand.data["due_tick"] - w.clock.tick + 1)
        assert [e.tick for e in w.log if e.kind == "ordnance.alongside"] == [demand.tick + 3 * 3600]
        assert w.purse.entries[entries:] == [
            (demand.tick + 3 * 3600, -5.0, "powder and shot of the merchants at Falmouth")
        ]
        w.run(2 * 3600)
        (stowed,) = [e for e in w.log if e.kind == "ordnance.stowed"]
        assert ("of absolute necessity, on the captain's word" in stowed.text) is necessity
        assert w.purse.pounds == 95.0 and len(w.purse.entries) == entries + 1  # paid once
    privateer = _anchored(
        THE_SOUND, ship=PRIVATEER, papers={"service": "privateer"}, cargo={"purse_pounds": 100.0}
    )
    privateer.world_order(DAMP)
    for order in ("take in powder and shot", "buy powder and shot"):
        said = privateer.submit(order)
        assert said.kind == "order.rejected" and said.data["reason"] == (
            "The Ordnance's storekeeper at Plymouth issues to the King's ships alone, and no "
            "merchant here sells powder."
        )
    french = _anchored(
        CASCAIS_ROAD,
        ship=PRIVATEER,
        chart="atlantic-east",
        ports=("lisbon",),
        nation="france",
        papers={"service": "privateer"},
        cargo={"purse_pounds": 100.0},
    )
    french.world_order(DAMP)
    block = french.ports.ports["lisbon"].ordnance
    assert french.dealings.stance(french.dealings.in_port()) == "neutral"
    assert block["sells_in_war_to"] is None  # the knob in the file, left unset
    block["sells_in_war_to"] = ("britain",)
    said = french.submit("buy powder and shot")
    assert said.kind == "order.rejected" and said.data["reason"] == (
        "Lisbon's merchants sell no powder to a French ship while the war lasts."
    )
    block["sells_in_war_to"] = None
    assert french.submit("buy powder and shot").kind == "ordnance.demanded"


def test_truth_7_169_the_long_tom_fires_on_when_the_carronades_filled_cartridges_are_spent():
    """The build design's §4: the privateer schooner (her long 12-pounder on a pivot and four
    12-pounder carronades) at quarters engages a mark three cables on the starboard beam,
    her carronades' filled cartridges set to four by the test. At seed 7 the four are
    spent within three minutes; the guns wait at the cartridge while the gunner fills from
    the powder below, told once ("No more filled cartridges for the 12-pounder carronades:
    the gunner is filling, and the guns wait on him."); the long Tom has cartridges of its
    own kind and never stalls, firing 25 rounds in the forty minutes; the carronades fire
    again as each cartridge is filled (a man of the powder at 135 man-seconds a cartridge,
    about one in two minutes and a quarter); and the powder below falls by exactly the 18
    pounds of the 18 cartridges he filled, a pound apiece."""
    from freesail.combat.guns import battery_of
    from freesail.ship.parts import magazine
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, PRIVATEER)
    w.run(60)
    _guns_ready(w)
    ship = w.ship
    battery = battery_of(ship)
    mag = magazine(ship)
    mag.set_filled("carronade", 12.0, 4)
    cartridges, fired = dict(mag.cartridges), dict(mag.fired)
    powder, by_gunner = mag.powder_lb, mag.filled_by_gunner
    said = w.submit("engage a mark three cables on the starboard beam")
    assert said.kind == "guns.engage", said.text
    pivot = next(g for g in ship.guns.values() if g.place == "pivot")
    carronades = [g for g in ship.guns.values() if g.kind == "carronade"]
    stalled = []
    discharged = []  # the ticks a carronade fired
    for _ in range(40 * 60):
        before = sum(g.fired for g in carronades)
        w.run(1)
        if battery.services[pivot.id].stalled:
            stalled.append(w.clock.tick)
        discharged += [w.clock.tick] * (sum(g.fired for g in carronades) - before)
    assert not stalled, stalled[:5]
    assert pivot.fired >= 10  # 25 at seed 7
    (waiting,) = [e for e in w.log if e.kind == "guns.filling"]
    assert waiting.text == (
        "No more filled cartridges for the 12-pounder carronades: the gunner is filling, and "
        "the guns wait on him."
    )
    assert waiting.data["kind"] == "carronade" and waiting.data["held"] is False
    again = [t for t in discharged if t > waiting.tick]
    assert len(again) >= 5, discharged  # 17 at seed 7, one each two minutes or so
    assert not [e for e in w.log if e.kind in ("guns.magazine_empty", "guns.powder_out")]
    fills = {
        k: mag.cartridges.get(k, 0) - cartridges.get(k, 0) + mag.fired.get(k, 0) - fired.get(k, 0)
        for k in mag.level
    }
    assert sum(fills.values()) == mag.filled_by_gunner - by_gunner > 0  # 18 at seed 7
    spent = sum(n * mag.charge_of(*k) for k, n in fills.items())
    assert powder - mag.powder_lb == pytest.approx(spent)


def test_truth_7_170_a_checkpoint_with_the_hoy_alongside_resumes_to_one_digest_and_replays_to_it(
    tmp_path,
):
    """The build design's §3.4 and §9: the hoy is a port job, the galley fire a state of the
    stores and the filling the magazine's, so a checkpoint holds them whole and a replay
    makes them again from the inputs. The King's cutter in Plymouth Sound, a quarter of her
    cartridges found damp (the director's order) at 07:36 and her gunner filling them again
    from the powder below, all 82 by 10:41; `take in powder and shot` demands a barrel, and
    the hoy comes alongside at 11:36. Ten minutes later a quarter of them is found damp
    again, and the gunner may fill none while the powder comes aboard and the galley fire
    is out: a minute on the checkpoint is taken so, the magazine short (248 of 330), the
    hoy alongside and the filling held by the fire. The game resumed and the game played on run four
    hours and a half each, through the stowing at 12:36, the gunner's filling of the 82
    from the powder taken in and his report at 15:41 ("The gunner has the cartridges filled
    to the allowance"), to the same log and magazine; the save replayed from its seed and
    inputs gives them again. (Before the review's finding the filling was done an hour
    before the checkpoint, and nothing of it crossed it.) Measured on the owner's machine:
    44 lines and the digest 073626b2d8d85807 for all three; on the build machine at package
    86's fold-in, on top of 73, the same 44 lines and 073626b2d8d85807."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod
    from freesail.ship.parts import magazine

    w = _anchored(
        THE_SOUND,
        start=datetime(1805, 6, 10, 7, 30),
        papers={"service": "kings"},
        cargo={"purse_pounds": 100.0},
    )
    w.world_order(DAMP)
    demand = w.submit("take in powder and shot")
    assert demand.kind == "ordnance.demanded" and demand.data["barrels"] == 1, demand.text
    w.run(demand.data["due_tick"] - w.clock.tick + 600)
    (job,) = w.dealings.jobs
    assert job.payload["stage"] == "stowed" and w.stores.galley_fire_out == "powder"
    mag = magazine(w.ship)
    assert mag.filled_of("carronade", 12.0) == 330 and not mag.short  # the first filled
    w.world_order(DAMP)  # damp again with the hoy alongside: the filling held by the fire
    mag = magazine(w.ship)
    held = mag.filled_of("carronade", 12.0)
    assert mag.short and held < 330, held  # 248 at seed 7
    filled = mag.filled_by_gunner
    w.run(60)
    assert mag.filled_of("carronade", 12.0) == held and mag.filled_by_gunner == filled
    path = replay_mod.write_checkpoint(w, tmp_path / "hoy.checkpoint")
    _header, resumed = replay_mod.read_checkpoint(path)
    assert [(j.kind, j.payload, j.due_tick) for j in resumed.dealings.jobs] == [
        (job.kind, job.payload, job.due_tick)
    ]
    assert resumed.stores.galley_fire_out == "powder"
    assert vars(magazine(resumed.ship)) == vars(mag)
    for world in (w, resumed):
        world.run(4 * 3600 + 30 * 60)
    assert [e.tick for e in w.log if e.kind == "ordnance.stowed"] == [job.due_tick]
    assert resumed.log.digest() == w.log.digest()
    assert vars(magazine(resumed.ship)) == vars(magazine(w.ship))
    for world in (w, resumed):
        m = magazine(world.ship)
        assert m.filled_of("carronade", 12.0) == 330 and not m.short  # filled to the allowance
        assert m.filled_by_gunner == filled + 330 - held  # all of it after the checkpoint
        (said,) = [e for e in world.log if e.kind == "guns.filled"]
        assert said.tick > job.due_tick  # after the stowing, in the resumed game too
    again = replay_mod.replay_world(w, ship_factory)
    assert again.log.digest() == w.log.digest()
    assert vars(magazine(again.ship)) == vars(magazine(w.ship))
    assert again.stores.cold_meals == resumed.stores.cold_meals == w.stores.cold_meals


def test_truth_7_171_a_practice_forenoon_is_checkpointed_and_replayed(tmp_path):
    """The build design's §3.4: every order of practice is an input and everything after it
    is pickled state or drawn from its own stream, so a forenoon of practice resumes from
    its checkpoint and replays from its save to one log. The owner's scenario
    (data/scenarios/exercising-the-great-guns.yaml, the rules captains with no model
    seated), the orders given by the test: at 09:01 `beat to quarters`, `exercise the
    starboard battery` and `cast loose the guns`; twenty minutes of dumb show and `cease
    exercising`; a cask hove over from the starboard quarter and engaged to starboard;
    checkpointed at 09:25 with the cask in the water and in sight; then half an hour, a
    notional mark four cables on the starboard beam engaged for half an hour, `secure the
    guns`, and on to noon. The game resumed from the checkpoint and the game played on give
    one log, and the save replayed gives it again. Measured on the owner's machine: 227
    lines and the digest 77cfa4458e18620d for all three (measured again after the review,
    before its fixes and after them alike; the c06f1fa9bb619847 first written here did not
    reproduce); on the build machine at package 86's fold-in, on top of 73, the same 227
    lines and 77cfa4458e18620d."""
    from freesail.api.session import ship_factory
    from freesail.combat import marks
    from freesail.core import replay as replay_mod
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(EXERCISING)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(60)
    assert w.submit("beat to quarters").kind == "crew.quarters"
    w.run(5)
    assert w.submit("exercise the starboard battery").kind == "guns.exercise"
    w.submit("cast loose the guns")
    w.run(20 * 60)
    assert w.submit("cease exercising").kind == "guns.exercise"
    w.run(60)
    assert w.submit("heave a cask overboard from the starboard quarter").kind == "order.accepted"
    w.run(120)
    assert w.submit("engage the cask to starboard").kind == "guns.engage"
    w.run(60)
    cask = marks.cask_in_water(w.ship)
    assert cask is not None and marks.cask_in_sight(w, cask)
    assert any(e.kind == "practice.exercise" for e in w.log)
    path = replay_mod.write_checkpoint(w, tmp_path / "forenoon.checkpoint")
    _header, resumed = replay_mod.read_checkpoint(path)
    assert marks.cask_in_water(resumed.ship) == cask
    for world in (w, resumed):
        world.run(30 * 60)
        assert world.submit("engage a mark four cables on the starboard beam").kind == "guns.engage"
        world.run(30 * 60)
        world.submit("secure the guns")
        world.run(3 * 3600 - world.clock.tick)
    assert resumed.log.digest() == w.log.digest()
    assert w.readings.value("practice") == resumed.readings.value("practice")
    assert any(e.kind == "action.fired" and e.data.get("mark") == "notional" for e in w.log)
    again = replay_mod.replay_world(w, ship_factory)
    assert again.log.digest() == w.log.digest()
    assert again.readings.value("practice") == w.readings.value("practice")


# ---------------------------------------------------------------------------
# Package 73: water, damage control, health and the fight on deck (spec M7 §11, §11a, §13
# to §17; docs/design/Design-WaterAndHealth.md; truths 7-172 onward, after the owner's
# practice-and-resupply package's 7-161 to 7-171)
# ---------------------------------------------------------------------------


def _hole_in(world, z_m: float, pounder: float = 18.0, side: str = "starboard") -> dict:
    """A shot hole written as 70's state, at so much against the upright waterline."""
    from freesail.combat.hits import damage_of, shot_diameter_m

    keeper = damage_of(world.ship)
    hole = {
        "tick": world.clock.tick,
        "side": side,
        "x_m": 0.0,
        "z_m": z_m,
        "diameter_m": round(shot_diameter_m(pounder), 3),
        "pounder": pounder,
    }
    keeper.holes.append(hole)
    return hole


def test_truth_7_172_a_shot_hole_fills_the_well_by_the_orifice_law_and_the_pumps_hold_it():
    """Spec M7 §15: "A shot hole below the waterline fills the well at the rate the hole
    and the heel give and the pumps hold it with so many hands and not with fewer." An
    18-pounder's hole half a metre under the frigate's waterline takes in some eighty-five
    tons an hour by the orifice law (`Q = 0.6 A sqrt(2gh)`), the carpenter reports the
    first foot in the well, the two chain pumps and the two hand pumps (Falconer 1780,
    PUMP: 80 and 15 tons an hour) with their twelve hands gain on it and three men at one
    hand pump would lose; heeled so that the hole is buried she takes in more."""
    from freesail.world import water as W

    w = make_world(SEED, FRIGATE, _action_scenario(wind_kn=0.1))
    w.run(5)
    _hole_in(w, -0.5, 18.0)
    leaks = w.water.leaks()
    assert len(leaks) == 1 and leaks[0].kind == "shot hole"
    gain = leaks[0].t_per_h
    assert 75.0 < gain < 95.0, gain
    assert gain == pytest.approx(W.orifice_t_per_h(leaks[0].hole["diameter_m"], 0.5), rel=0.05)
    w.ship.dyn.heel = 0.1  # six degrees to starboard: the hole buried
    assert w.water.leaks()[0].t_per_h > gain
    w.ship.dyn.heel = 0.0
    w.run(3600)
    rising = events(w, "well.rising")
    assert rising and "a foot of water in the well" in rising[0].text
    e = w.submit("man the pumps")
    assert e.kind == "pumps.manned" and "twelve hands" in e.text.lower()
    w.run(600)
    pumps = w.water.pumps
    full = pumps.rate_t_per_h(pumps.hands())
    assert full > gain and 150.0 < full < 220.0, (full, gain)
    assert events(w, "pumps.gaining")
    assert pumps.rate_t_per_h(pumps.hands()[:3]) < gain
    assert "pumps" in w.readings.words("pumps") or "lifting" in w.readings.words("pumps")


def test_truth_7_173_the_carpenter_plugs_the_hole_in_the_time_the_bill_says_and_the_leak_stops():
    """Spec M7 §15: "the carpenter plugs it in the time the bill says". A hole half a
    metre under is reached from between decks with the water about the men: twenty
    minutes (data/evolutions/plug_shot_hole.yaml); the plug counted from the carpenter's
    store, the hole `plugged`, the keeper's leaks empty and the pumps sucking after."""
    from freesail.evolutions.repair_scripts import shot_plugs

    w = make_world(SEED, FRIGATE, _action_scenario(wind_kn=0.1))
    w.run(5)
    hole = _hole_in(w, -0.4, 12.0)
    plugs = shot_plugs(w.ship).count
    w.submit("man the pumps")
    e = w.submit("plug the shot holes")
    assert e.kind in ("order.accepted", "evolution.started", "evolution.queued"), e.text
    w.run(600)
    assert not hole.get("plugged")
    w.run(900)
    assert hole.get("plugged") and shot_plugs(w.ship).count == plugs - 1
    assert not [lk for lk in w.water.leaks() if lk.kind == "shot hole"]
    w.run(1800)
    assert events(w, "pumps.sucked")
    assert "plugged" in w.readings.words("damage")


def test_truth_7_174_a_ship_that_founders_does_so_with_the_log_saying_when_the_pumps_lost():
    """Spec M7 §15: "a ship that founders does so with the log saying when the pumps
    lost". The cutter with three 18-pounder holes a metre under (some three hundred tons
    an hour against her two hand pumps' thirty) fills in the hour: the well rising by the
    foot, the pumps losing, the ship settling at three fifths of what founders her and
    foundered at half her displacement, the colours' lines in order, the world's ship lost
    and the integrator holding her where she lies."""
    w = make_world(SEED, CUTTER, _action_scenario(wind_kn=0.1))
    w.run(5)
    for side in ("starboard", "larboard", "starboard"):
        _hole_in(w, -1.0, 18.0, side)
    w.submit("man the pumps")
    for _ in range(240):
        w.run(60)
        if getattr(w, "ship_lost", False):
            break
    assert w.ship_lost and w.ship.extra.get("foundered")
    kinds = [
        e.kind
        for e in w.log
        if e.kind in ("well.rising", "pumps.losing", "ship.settling", "ship.foundered")
    ]
    assert (
        kinds.index("pumps.losing") < kinds.index("ship.settling") < kinds.index("ship.foundered")
    )
    lost = events(w, "pumps.losing")[0]
    assert "losing" in lost.text and "tons" in lost.text
    foundered = events(w, "ship.foundered")[0]
    assert "the pumps lost her at" in foundered.text and "the ship is lost" in foundered.text
    speed = float(w.ship.dyn.speed or 0.0)
    w.run(300)
    assert float(w.ship.dyn.speed or 0.0) <= max(speed, 0.1)


def test_truth_7_175_the_grounding_replayed_with_the_pumps_and_the_carpenter_takes_hours():
    """Spec M7 §15: "the grounding at Horta replayed with the pumps and the carpenter
    instead of the stopgap gives the same tide and a repair that takes hands and hours".
    The frigate run on to the Manacles at four knots in a lighter wind than the ground's
    tests use (at six she is stove at six hundred tons an hour and bilged where she lies,
    which no carpenter mends: the ground's own test; the orders are refused on a foundered
    ship): the rock's leak some hundred and forty tons an hour, the pumps manned by order
    gain on it (the chain pumps' hundred and ninety), and `stop the leak` is the
    carpenter's three hours at the planks (data/evolutions/plug_shot_hole.yaml, the
    caulking), after which the ground's leak is nought and the pumps suck; the tide's own
    times are the ground's and not touched (the ground tests measure them)."""
    from tests.test_ground import FRIGATE as GF
    from tests.test_ground import Position, run_until_aground, thick_world

    start = datetime(1805, 6, 12, 12, 0)
    w = thick_world(GF, Position(50.025, -5.015), 315.0, start, from_deg=180.0, knots=10.0)
    w.submit("set plain sail")
    w.submit("steer NW")
    assert run_until_aground(w, 3.0)
    w.run(1800)
    rate = w.ship.extra["leak_m_per_h"]
    assert rate > 0.0 and any(lk.kind == "the ground" for lk in w.water.leaks())
    e = w.submit("man the pumps")
    assert e.kind == "pumps.manned", e.text
    e = w.submit("stop the leak")
    assert e.kind in ("order.accepted", "evolution.started", "evolution.queued"), e.text
    w.run(1800)
    assert w.ship.extra["leak_m_per_h"] == rate  # the caulking takes its hours
    w.run(3 * 3600)
    assert w.ship.extra["leak_m_per_h"] == 0.0
    assert not [lk for lk in w.water.leaks() if lk.kind == "the ground"]
    w.run(3600)
    assert w.water.depth_m() < 0.1 and events(w, "pumps.sucked")
    assert w.ship.extra.get("aground") and not w.ship.extra.get("foundered")


def test_truth_7_176_a_broadsides_casualties_are_men_of_the_muster_named_and_the_bill_counts():
    """Spec M7 §17: "A broadside's casualties are men of the muster, named where they were
    named". Twelve hits on the frigate's after deck and hull at quarters hurt twenty of
    her people (at seed 7): each a man of the muster with his wound in words, the
    quarterdeck's share among them and the captain himself told his roads in a line of
    his own; the butcher's bill ten minutes after the last shot names the killed and
    counts the wounded, the dangerous apart; the morale's figure counts them."""
    from freesail.combat import hits as HITS

    w = make_world(SEED, FRIGATE, _action_scenario())
    told: list = []
    w.needs.listen(told.append)
    w.submit("beat to quarters")
    w.run(120)
    keeper = HITS.damage_of(w.ship)
    rng = w.rng.stream("gunnery")
    for _ in range(6):
        HITS._casualties(w.ship, keeper, 2.0, -15.0, "deck", rng, w.clock.tick)
        HITS._casualties(w.ship, keeper, 2.0, 0.0, "hull", rng, w.clock.tick)
    crew = w.ship.extra["crew"]
    hurt = [s for s in crew.sailors if s.hurt]
    assert 12 <= len(hurt) <= 30
    assert all(s.hurt in ("killed", "wounded") and not s.fit for s in hurt)
    assert all(s.hurt_how for s in hurt if s.hurt == "wounded")
    assert any(s.station.value == "quarterdeck" for s in hurt)
    captain = w.people.captain
    cap = crew.by_id[captain.sailor_id]
    if cap.hurt:
        assert any("You are hit" in e.text for e in told)
    keeper.hits = 12
    keeper.struck_by = {"enemy": w.clock.tick}
    w.run(660)
    bill = events(w, "action.bill")
    assert len(bill) == 1 and bill[0].text.startswith("The butcher's bill: ")
    killed = [s for s in hurt if s.hurt == "killed"]
    if killed:
        assert killed[0].name in bill[0].text
    assert "dangerously" in bill[0].text
    words = w.readings.words("bill")
    assert "wounded" in words and "of 264" in words


def test_truth_7_177_the_surgeon_returns_the_lightly_hurt_in_hours_and_days_and_not_the_badly():
    """Spec M7 §17: "the surgeon's work returns the lightly hurt to the bill in days and
    not the badly". After 7-176's hits the surgeon and his two mates work the queue (the
    grave under his hands half an hour each, the light under a mate's ten minutes): in
    three hours nobody waits, the lightly wounded are 'hurt' and at light duty for a week
    or two, the gravely wounded stay below for the surgeon's judgement at a day, when each
    dies or is invalided for the voyage; the bill and the sick list say so in words."""
    from freesail.combat import hits as HITS

    w = make_world(SEED, FRIGATE, _action_scenario())
    w.submit("beat to quarters")
    w.run(120)
    keeper = HITS.damage_of(w.ship)
    rng = w.rng.stream("gunnery")
    for _ in range(6):
        HITS._casualties(w.ship, keeper, 2.0, -15.0, "deck", rng, w.clock.tick)
        HITS._casualties(w.ship, keeper, 2.0, 0.0, "hull", rng, w.clock.tick)
    crew = w.ship.extra["crew"]
    wounded = [s for s in crew.sailors if s.hurt == "wounded"]
    light = [s for s in wounded if s.wound == "light"]
    grave = [s for s in wounded if s.wound == "grave"]
    assert light and grave
    assert w.health.surgeon() is not None and len(w.health.mates()) == 2
    w.run(600)
    assert "at work on the wounded" in w.readings.words("surgeon")
    w.run(5 * 3600)
    assert "nobody under his hands" in w.readings.words("surgeon")
    assert all(s.hurt == "hurt" and s.fit for s in light)
    assert all(7 * 86400 - 3600 <= s.hurt_until - w.clock.tick <= 14 * 86400 for s in light)
    assert all(s.hurt == "wounded" and s.dressed and not s.fit for s in grave)
    assert "hurt and at light duty" in w.readings.words("bill")
    w.submit("secure the guns")
    w.run(28 * 3600)  # a day after the last of them was dressed
    judged = [e for e in w.log if e.kind in ("health.died", "health.invalided")]
    assert len(judged) == len(grave)
    assert all(s.hurt == "killed" or s.wound == "invalid" for s in grave)
    assert not any(s.fit for s in grave)


def test_truth_7_178_a_hand_dead_of_thirst_is_a_death_the_log_explains_from_the_needs_lines():
    """Spec M7 §17: "a hand dead of thirst on a passage with the water foul and no port
    is a death the log explains from the needs' lines before it". The cutter's water and
    provisions expended: the captain at the prompt is told he is thirsty, then
    desperately thirsty, collapses at three days and is dead at four, told so in his own
    line, the command passing by the bill; of the hands, the surgeon's report has men
    taken ill from the second day and dead from the fourth, each 'died of thirst, the
    water being expended', buried the next morning; nothing of it is a figure set."""
    w = make_world(SEED, CUTTER, _action_scenario())
    told: list = []
    w.needs.listen(told.append)
    w.stores.water_tons = 0.0
    w.stores.provisions_days = 0.0
    captain = w.people.captain
    w.run(5 * 24 * 3600)
    thirsty = [e.text for e in told if "thirsty" in e.text]
    assert thirsty and any("desperately thirsty" in t for t in thirsty)
    assert any("collapsed with thirst" in e.text for e in told)
    assert any("You are dead of thirst" in e.text for e in told)
    assert captain.dead and w.people.captain is not captain
    passes = events(w, "ship.command_passes")
    assert passes and w.people.captain.name in passes[0].text
    died = events(w, "health.died")
    assert died and all("thirst" in e.text for e in died)
    assert any("the water being expended" in e.text for e in died)
    sick = events(w, "health.sick")
    assert sick and sick[0].tick < died[0].tick
    buried = events(w, "crew.buried")
    assert buried and all(b.tick > died[0].tick for b in buried)
    dead = [s for s in w.ship.extra["crew"].dead]
    assert dead and all(s.hurt_how.startswith("of thirst") for s in dead)


def test_truth_7_179_a_volley_within_musket_shot_fells_the_near_decks_men_and_the_quarterdecks():
    """Spec M7 §11: the marines "fire at the men on a near deck by volley or at will, the
    hits on the men at the parts exposed (the quarterdeck's officers and helmsmen first,
    which is history's lesson)". The frigate's forty marines at thirty metres of a French
    frigate fire three volleys a minute (the British drill); at seed 7 her people fall to
    musket balls within the three minutes, her log saying 'musketry from her deck', and
    the ball's choice of a man falls on the quarterdeck two times in five: with the draw
    forced the quarterdeck's man is struck, and a named person among them is told in a
    line of his own."""
    from freesail.combat import small_arms as SA
    from tests.test_fight import _alongside

    w, v, enemy = _alongside(30.0)
    assert w.submit("marines, fire by volley").kind == "marines.fire"
    w.run(180)
    ours = events(w, "action.musketry")
    assert ours and sum(e.data["volleys"] for e in ours) >= 3  # until she drifts out of shot
    hurt = [s for s in enemy.ship.extra["crew"].sailors if s.hurt]
    assert hurt and all("musket ball" in s.hurt_how for s in hurt)
    assert any("musketry from her deck" in e.text for e in events(enemy, "action.hit"))

    class _Draw:
        def __init__(self, seq):
            self.seq = list(seq)

        def random(self):
            return self.seq.pop(0) if self.seq else 0.5

    quarterdeck, deck = SA.exposed_men(enemy.ship, "larboard")
    assert quarterdeck and deck
    before = len(events(enemy, "person.hurt"))
    struck = SA.strike_a_man(
        enemy.ship,
        "larboard",
        _Draw([0.1, 0.0, 0.9, 0.9, 0.9]),
        w.clock.tick,
        "a musket ball in the arm",
        "the ship",
    )
    assert struck is not None and struck.station.value == "quarterdeck"
    assert struck.hurt == "wounded"
    enemy.run(60) if hasattr(enemy, "run") else w.run(60)
    w.run(60)
    named = [p for p in enemy.people.people if p.sailor_id == struck.id]
    if named:
        assert "wounded" in enemy.people.state_words(named[0])
        assert len(events(enemy, "person.hurt")) > before


def test_truth_7_180_the_boarders_are_repulsed_by_a_whole_company_awake_and_the_temper_pays():
    """Spec M7 §11a: "the boarders over by §11's fight on deck, the deck won or the
    boarders repulsed". A hundred boarders (the bill's sixty with the forty marines)
    against a frigate's company all on deck and awake: the crossing's volley tells, the
    first round goes against them (the defenders' strength near twice theirs behind their
    nettings) and they are repulsed within three rounds; the grapnels cast off, the losses
    on both musters, the lines on both logs, the hands' temper the worse by a tenth."""
    from freesail.combat import boarding as B
    from freesail.combat.morale import morale_of
    from tests.test_fight import _alongside

    w, v, enemy = _alongside(10.0)
    w.submit("grapple her")
    w.run(65)
    assert B.grappled_to(w.ship) == v.id
    assert w.submit("boarders away").kind == "action.boarders"
    for _ in range(B.CONTEST_ROUNDS + 1):
        w.run(60)
        f = B.fight_of(w.ship)
        if f is not None and f.over:
            break
    f = B.fight_of(w.ship)
    assert f.over == "repulsed" and f.round <= 3
    rounds = events(w, "action.boarding")
    assert rounds[0].data["strength_defence"] > rounds[0].data["strength_attack"]
    assert events(w, "action.repulsed") and events(enemy, "action.repulsed")
    assert morale_of(w.ship).repulses == pytest.approx(B.REPULSE_COST)
    assert not B.grappled_to(w.ship)
    assert f.lost_attack > f.lost_defence > 0


def test_truth_7_181_the_boarders_carry_a_deck_held_by_the_marines_and_the_colours_come_down():
    """Spec M7 §11a: the deck won. Against the same frigate at quarters, her gun crews at
    their guns and the deck held by her marines, the helm, the trimmers and the
    quarterdeck, the boarders with their arms served out carry it in a few rounds: her
    colours come down 'carried by boarding' (the strike's own line, the far body struck),
    the prize alongside for 74; the losses by name on both bills."""
    from freesail.combat import boarding as B
    from freesail.combat import small_arms as SA
    from tests.test_fight import _alongside

    w, v, enemy = _alongside(10.0, her_quarters=True)
    w.submit("grapple her")
    w.submit("serve out the small arms")
    w.run(400)
    assert SA.musketry_of(w.ship).served
    assert w.submit("boarders away").kind == "action.boarders"
    for _ in range(B.CONTEST_ROUNDS + 1):
        w.run(60)
        f = B.fight_of(w.ship)
        if f is not None and f.over:
            break
    f = B.fight_of(w.ship)
    assert f.over == "carried" and 2 <= f.round <= 12, (f.over, f.round)
    assert any("carried by boarding" in e.text for e in events(enemy, "action.struck"))
    assert v.struck and events(w, "action.carried")
    assert f.lost_defence > f.lost_attack > 0
    assert "killed" in enemy.readings.words("bill") or "wounded" in enemy.readings.words("bill")


def test_truth_7_182_a_station_holder_hit_has_the_two_roads_at_parity_and_killed_is_stood_down():
    """Spec M7 §16a: the holder hit "may keep the deck ... or give the deck and go below
    to the surgeon ... a holder killed ends his person's station as a death does". The
    officer of the watch (a fake model with the deck) hit lightly is told his roads in an
    urgent line of his own and keeps the deck, his orders going; gone below by the order
    he is in the cockpit and the surgeon's queue and told when dressed; hit gravely and
    keeping the deck he collapses at the half hour and is carried below (the stand-by that
    no event ends); killed, the station is stood down by the world with the reason and
    the log says so; the captain at the prompt killed, the command passes by the bill."""
    from freesail.crew import health as H
    from tests.test_health import _hit, _officer_with_the_deck

    w, oh, person, sailor = _officer_with_the_deck()
    _hit(w, sailor, "light")
    notice = [n for n in oh.agent.notices if "You are hit" in n]
    assert notice and "go below to the surgeon" in notice[0] and oh.agent.deck
    assert w.health.go_below_to_the_surgeon(person, oh).startswith("You give the deck")
    assert person.where == "cockpit" and not oh.agent.deck
    w.run(H.DRESS_LIGHT_S + 120)
    assert sailor.hurt == "hurt" and any("Your wound is dressed" in n for n in oh.agent.notices)
    w2, oh2, person2, sailor2 = _officer_with_the_deck()
    _hit(w2, sailor2, "grave")
    w2.run(H.COLLAPSE_S + 120)
    assert oh2.agent.standing_by and person2.where == "cockpit"
    assert events(w2, "person.collapsed")
    w3, oh3, person3, sailor3 = _officer_with_the_deck()
    _hit(w3, sailor3, killed=True, how="a round shot")
    assert person3.dead and oh3.agent.released
    assert any(
        "killed: a round shot" in e.text and "the world" in e.text
        for e in events(w3, "agent.stopped")
    )
    captain = w3.people.captain
    _hit(w3, w3.ship.extra["crew"].by_id[captain.sailor_id], killed=True, how="a musket ball")
    assert captain.dead and w3.people.captain is not captain and events(w3, "ship.command_passes")


def test_truth_7_183_the_first_action_replayed_with_the_arms_the_pumps_and_the_carpenter():
    """Spec M7 §12 and the brief's item 9: the first action (data/scenarios/first-action.yaml)
    replayed at seed 7 with package 73 in it. The band of 7-133 holds (the colours come
    down between three quarters of an hour and three after the first shot); what changed
    is said: both captains serve out the small arms on entering the action (their
    doctrines' `board_odds` above nought); the privateer's captain has the carpenter plug
    her shot holes under water and mans the pumps at the doctrine's foot where the well
    asks it; her bill counts the
    killed and the wounded by their states and the butcher's bill is said ten minutes after
    the last shot; the next morning she buries her dead. The minute itself moved from 71's
    11:12 (docs/dev/TuningNotes.md, package 73: the bisection names which item)."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    v = w.vessels.find("Renard")
    first = None
    struck_tick = None
    for _ in range(3 * 60):
        w.run(60)
        if first is None:
            fired_at = [e for e in w.log if e.kind == "action.fired_at"]
            if fired_at:
                first = fired_at[0].tick
        if v.struck or w.ship.extra.get("struck"):
            struck_tick = w.clock.tick
            break
    assert first is not None and v.struck and not w.ship.extra.get("struck")
    assert 2700 <= struck_tick - first <= 3 * 3600, f"{(struck_tick - first) / 60:.0f} min"
    enemy = v.crew
    assert any("serving out the small arms" in e.text for e in enemy.log), "the small arms"
    assert (
        any("serving out the small arms" in e.text for e in w.log)
        or w.ship.extra["musketry"].served
    )
    assert events(enemy, "small_arms.served")
    # the carpenter to the holes under water where there are any (at this seed her seven
    # lie above it), the pumps at the doctrine's foot of water or the well never there
    under = [h for h in enemy.ship.extra["damage"].holes if float(h.get("z_m", 1.0)) < 0.0]
    if under:
        assert any("Plug the shot holes" in e.text for e in enemy.log)
    assert events(enemy, "pumps.manned") or enemy.water.depth_m() < 0.3
    bill = enemy.readings.words("bill")
    assert "killed" in bill or "wounded" in bill
    w.run(11 * 60)
    assert events(enemy, "action.bill")
    w.run(21 * 3600)
    killed = [s for s in enemy.ship.extra["crew"].dead]
    if killed:
        assert events(enemy, "crew.buried")


def test_truth_7_184_the_leak_scenario_mans_the_pumps_at_a_foot_and_left_alone_loses_stiffness():
    """The brief's leak scenario (data/scenarios/leak.yaml): the King's cutter homeward in
    a strong westerly, three seams found working by the scenario's world orders (two tons
    an hour each). Under the rules captain the well shows a foot at 13:00 and he mans the
    pumps at the doctrine's depth (`pumps_at_m` 0.3), the hand pumps' thirty tons an hour
    gaining on the six and sucking within the half hour, the spells said; with the captain
    aside the well is two feet at 15:00 and the free surface has taken a third of her
    metacentric height (1.10 m to 0.77 m, `Hull.gm_m`), nothing else of her changed."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/leak.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    gm0 = float(w.ship.hull.gm_m)
    w.run(3 * 3600 + 900)
    assert len(events(w, "aboard.found")) == 3 and len(w.water.leaks()) == 3
    assert w.water.pumps.manned and any("manning the pumps" in e.text for e in w.log)
    w.run(3600)
    assert w.water.depth_m() < 0.05 and events(w, "pumps.sucked")
    w.run(3600)
    assert events(w, "pumps.spelled")
    w2 = make_scenario_world(sf)
    begin(w2, sf)
    w2.captain.aside = True
    w2.run(5 * 3600)
    assert not w2.water.pumps.manned
    assert 0.5 < w2.water.depth_m() < 0.7, w2.water.depth_m()
    gm = float(w2.ship.hull.gm_m)
    assert 0.6 < gm < 0.85 and gm0 == pytest.approx(1.1, abs=0.05), (gm0, gm)
    assert not w2.ship_lost


@pytest.mark.slow
def test_truth_7_200_the_tender_sent_to_plymouth_by_signal_lands_for_a_packet_and_hails_home():
    """Package 84, step 4: the owner's acceptance test of the one-world design
    (docs/design/Design-OneWorld.md §2.12) walked with a fake at the tender's captain's
    station, her hull asleep the whole day (data/scenarios/tender.yaml, `crewed: {cap: 0}`;
    the switch between the shapes is truth 89's). The Amazon lies at anchor in Brixham road
    with the cutter Raven in company; the fake anchors her, reads the frigate's signal No.
    131 in its sample, answers it, weighs and shapes a course for Plymouth, which the far
    body sails by the ports' tracks (out of Torbay, outside the Start and the Bolt Head by
    the coasting track, in by the Sound to the anchorage, where the plan's last leg brings
    her to an anchor); the director makes Mr Gill at Plymouth's counting house with a sealed
    packet in his keeping while she is at sea; landed by her boat's job the fake's captain
    goes to the counting house, is heard there, is given the packet by the director's `say
    as` (a free line in Mr Gill's mouth, heard by him alone) and comes aboard with it in his
    keeping; the lugger the director placed off the Start is made out by her lookout on the
    way home and not fought (74's); within hail of the frigate she hails, heard on the
    Amazon's quarterdeck. The Amazon's own lines have the signal, the cutter going and
    coming and the hail, and nothing of the port, Mr Gill, the packet or the lugger (the
    director's world orders are the harness's lines in the player's log, as before this
    package: the director's reach is a later step's); the Raven's log has them all, every
    line the game's own. Nothing is pinned: the business is off, and the walk is the truth."""
    from freesail.agents import Fake, Harness, SamplingPolicy, call
    from freesail.agents.agent import captain as captain_station
    from freesail.agents.model import Reply
    from freesail.world import things as TH
    from freesail.world.crews import station_world
    from freesail.world.geo import bearing_and_distance
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/tender.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(60)
    raven, crew = station_world(w, "Raven")
    assert crew.shape == "far" and raven.detail == "far"  # asleep: the sea's word (step 6)
    stage = {"n": 0, "orders": []}

    def act(last, turns):
        """The fake at her captain's station: what the sample says decides the next act."""
        if "tool_results" in last:
            # the order's result read (a refusal is routine, so no sample carries it): the
            # land guard's word answered with a way by marks (package 45's `via`)
            said = str(last["tool_results"]).lower()
            if "give the way by marks" in said and stage["n"] in (2, 6):
                port = "Plymouth" if stage["n"] == 2 else "Torbay"
                stage["orders"].append(f"shape a course for {port} via the Start")
                return Reply(
                    calls=(call("submit_order", text=f"shape a course for {port} via the Start"),)
                )
            return Reply()
        log = last.get("log") or []
        kinds = {str(e.get("kind")) for e in log}
        text = " ".join(str(e.get("text", "")) for e in log).lower()
        heard = " ".join(str(x) for x in (last.get("heard") or [])).lower()
        s, orders = stage["n"], []
        if s == 0:
            orders, s = ["come to an anchor"], 1
        elif s == 1 and "signal.read" in kinds and "plymouth" in text:
            orders, s = ["answer the signal", "weigh", "shape a course for Plymouth"], 2
        elif s == 2 and "ship.anchored" in kinds and "the sound" in text:
            orders, s = ["go ashore"], 3
        elif s == 3 and "boat.alongside" in kinds:
            orders = [
                "go to the counting house",
                "say good day to you, Mr Gill; I am come for the packet",
            ]
            s = 4
        elif s == 4 and "keeping" in heard:
            orders, s = ["say I am obliged to you, Mr Gill", "come aboard"], 5
        elif s == 5 and "boat.alongside" in kinds:
            orders, s = ["weigh", "shape a course for Torbay"], 6
        elif s == 6 and "ship.anchored" in kinds and "brixham" in text:
            orders, s = ["hail the frigate"], 7
        stage["n"] = s
        stage["orders"] += orders
        if not orders:
            # a word at every sample: a door silent past its patience loses the deck to
            # the rules captain, whose judgements would stand in (spec M6 §20)
            return Reply(text="Nothing to add; carrying on.")
        return Reply(calls=tuple(call("submit_order", text=o) for o in orders))

    fake = Fake([act], loop=True)
    policy = SamplingPolicy.in_lockstep(600, "notable", "urgent")
    h = Harness(crew, captain_station(policy, 3600, world=crew), fake, save=lambda w, why: None)
    h.model_name, h.door = "the fake", "runner"
    h.start()
    assert crew.captain.seated and raven.station_held()

    def nm_apart() -> float:
        return bearing_and_distance(raven.position, w.position)[1] / units.NAUTICAL_MILE

    def run_until(cond, hours: float, step: int = 300) -> None:
        for _ in range(int(hours * 3600 / step)):
            w.run(step)
            if cond():
                return
        raise AssertionError(f"not reached in {hours} h: stage {stage['n']}, {raven.position}")

    def raven_kinds() -> list[str]:
        return [e.kind for e in crew.log]

    # 1. the seat: she rides at anchor beside the frigate, the player's log silent of it
    w.run(120)
    assert stage["n"] == 1 and raven.plan[0][0] == "anchor"
    assert crew.dealings.in_port() is not None and crew.dealings.in_port().id == "torbay"
    # 2. the order by signal: read in the sample, answered, the course by the tracks
    w.submit("make the signal: proceed to Plymouth")
    run_until(lambda: stage["n"] >= 2, 1.0, step=60)
    assert "signal.read" in raven_kinds()
    run_until(lambda: raven.plan and raven.plan[-1] == ("anchor", "plymouth"), 0.5, step=60)
    refused = [
        e for e in crew.log if e.kind == "order.rejected" and "give the way by marks" in e.text
    ]
    assert len(refused) == 1 and "crosses the land" in refused[0].text  # the land guard's word
    shaped = [e for e in crew.log if e.kind == "helm.set" and "by the tracks" in e.text]
    assert shaped and "the anchorage in the Sound" in shaped[-1].text
    assert "via the Start" in shaped[-1].text and "east-south-east of the Start" in shaped[-1].text
    assert raven.plan[-1] == ("anchor", "plymouth")
    run_until(lambda: any(e.kind == "signal.answered" for e in w.log), 0.5, step=60)
    # 3. at sea: the director makes the person and the thing at Plymouth while she sails
    run_until(lambda: nm_apart() > 6.0, 4.0)
    assert any(
        e.kind == "lookout.glass" and "cutter" in e.text and "under way" in e.text for e in w.log
    )
    w.world_order(
        'person: make "Mr Gill", a merchant of Plymouth, ashore at Plymouth, at the counting house'
    )
    w.world_order("aboard: a sealed packet, in the keeping of Mr Gill")
    packet = next(t for t in w.registry.things if "packet" in t.name)
    gill = w.people.find("Mr Gill")
    assert TH.keeper_of(w, packet) is gill and not gill.aboard
    # 4. into the port: the plan's last leg anchors her in the Sound, said in her log
    run_until(lambda: stage["n"] >= 3, 16.0)
    assert crew.dealings.in_port() is not None and crew.dealings.in_port().id == "plymouth"
    assert any(e.kind == "ship.anchored" and "track's end" in e.text for e in crew.log)
    # 5. ashore to a person: landed by the boat's job, to the counting house, heard there
    run_until(lambda: stage["n"] >= 4, 3.0)
    skipper = next(p for p in crew.people.people if p.station == "captain")
    assert skipper.where == "shore" and skipper.port == "plymouth" and skipper.hull is None
    assert skipper.ashore_at == "counting_house"
    spoke = [e for e in crew.log if e.kind == "agent.spoke"]
    assert spoke and "ashore at Plymouth, at the counting house" in spoke[-1].text
    # 6. back with a thing: the director's word in Mr Gill's mouth gives it; the boat fetches him
    e = w.world_order(f"say as Mr Gill: give the packet to {skipper.name}")
    assert "heard by" in e.text and skipper.name in e.text
    given = [x for x in w.log if x.kind == "free.line" and x.data.get("spoken_as")]
    assert given and given[-1].data["moved"] and TH.keeper_of(w, packet) is skipper
    assert TH.place_of(w, packet)[:3] == ("shore", "plymouth", "counting_house")
    run_until(lambda: stage["n"] >= 6, 3.0)
    assert skipper.aboard and skipper.hull == raven.id
    assert TH.keeper_of(w, packet) is skipper and TH.place_of(w, packet)[3] == raven.id
    # 7. past a ship the director placed: made out, not fought
    w.world_order(
        'ship: a lugger "Renard" of France at 50 09 N 3 44 W, '
        "patrolling off 50 08 N 3 42 W within 3 miles, no colours"
    )
    # 8. home to report: within hail of the frigate, heard on her quarterdeck
    run_until(lambda: stage["n"] >= 7, 18.0)
    assert sum(1 for e in crew.log if e.kind == "order.rejected" and "give the way" in e.text) == 2
    assert crew.dealings.in_port() is not None and crew.dealings.in_port().id == "torbay"
    assert nm_apart() < 1.0
    run_until(lambda: any(e.kind == "hail.heard" for e in w.log), 0.5, step=60)
    heard = [e for e in w.log if e.kind == "hail.heard"]
    assert "cutter" in heard[-1].text and heard[-1].severity.value == "urgent"
    # the two logs: hers has the port, the quay, the counting house, Mr Gill, the packet and
    # the lugger; the player's own lines have none of them
    hers = " ".join(e.text for e in crew.log).lower()
    for words in ("barbican steps", "counting house", "mr gill", "packet", "lugger"):
        assert words in hers, words
    assert any(e.kind == "lookout.made_out" and "lugger" in e.text for e in crew.log)
    own = " ".join(
        e.text for e in w.log if e.kind not in ("world.order", "person.spoke", "free.line")
    ).lower()
    for words in ("counting house", "mr gill", "packet", "lugger", "barbican"):
        assert words not in own, words
    # every order of the fake's was taken but the two the land guard refused, answered by
    # the way by marks
    refused = [e for e in crew.log if e.kind == "order.rejected" and e.actor == "the captain"]
    assert len(refused) == 2 and all("give the way by marks" in e.text for e in refused), [
        e.text for e in refused
    ]
    assert stage["orders"][0] == "come to an anchor" and stage["orders"][-1] == "hail the frigate"
    assert fake.calls > 6
    h.release("the test is done") if hasattr(h, "release") else None


# ---------------------------------------------------------------------------
# Package 79a: the regimes filled out and sourced (spec M7 §22; truths 7-260 to 7-269)
# ---------------------------------------------------------------------------

import yaml  # noqa: E402  (package 79a's truths read the knobs' tables)

REGIMES_YAML = "data/regimes.yaml"
NATIONS_YAML = "data/nations.yaml"
# a source in the references' form: a work held under docs/references/ cited by volume and
# page (or Falconer by his entry), or the word judgement
_SOURCE_FORM = re.compile(
    r"(James vol\. \d+ pp?\. \d+|Nicolas vol\. \d+ pp?\. \d+|Niles vol\. [IVX]+ pp?\. \d+"
    r"|the Regulations 1806 pp?\. \d+|Falconer 1780, [A-Z]{4,}|[Jj]udgement)"
)


def _business_world(region: str, lat: float, lon: float, ports: list[str], when: datetime):
    sc = Scenario(
        start_time=when,
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region=region,
        ports=ports,
        nation="britain",
        business="on",
    )
    return make_world(SEED, "data/ships/topsail-schooner.yaml", sc)


def _laid_up(w, vid: str, name: str, nation: str, port_id: str):
    from freesail.world.ships import vessel_from_spec

    port = w.ports.ports[port_id]
    spec = {
        "id": vid,
        "description": "frigate",
        "name": name,
        "nation": nation,
        "position": port.anchorage.position.to_dict(),
        "goal": f"bound for {port.name}",
        "regime": "in ordinary",
    }
    v = vessel_from_spec(w, spec, w.vessels.serial + 1)
    w.vessels.serial += 1
    w.vessels.add(v)
    return v, port


def test_truth_7_260_a_ship_in_ordinary_at_brest_is_commissioned_by_the_business_after_the_delay():
    """Spec M7 §22 (package 79a, the brief's item 2): a French frigate in ordinary at Brest
    with no sortie, the business on, is commissioned by the business at its first minute
    for an intent of France's (a cruise on one of her doctrine's stations in the region or a
    passage to another of her ports), to sail after the regime's `commission_delay_h` drawn
    under the seed: at seed 7 the station off the Lizard within 20 miles, the delay 55 hours
    (her commission due at 197345, inside the regime's two to five days). Said in her story
    and in the port's news (the pilot's words) while her company is raised; she sails at the
    first minute after it falls due and the news is gone. The clock is set forward over the
    55 hours (the region at full business runs some 180 ticks a second, so the days sailed
    would be some twenty minutes of the suite): she is a brainless hull at the anchorage
    throughout, and nothing of hers lies between."""
    w = _business_world(
        "channel-west", 50.0, -5.0, ["falmouth", "plymouth", "brest"], datetime(1805, 6, 12, 10)
    )
    v, brest = _laid_up(w, "aigle", "Aigle", "france", "brest")
    assert v.regime == "in ordinary" and v.sortie == "" and v.brain is None
    w.run(120)
    assert v.story[0] == (
        60,
        "commissioned for keep the station off the Lizard within 20 miles: her company "
        "raising, to sail in 55 hours",
    )
    assert v.commission_tick == 197345
    lo, hi = 48 * 3600, 120 * 3600
    assert lo <= v.commission_tick - 60 <= hi
    assert v.sortie in w.business.intents_for("france", brest)
    assert v.regime == "in ordinary" and v.brain is None
    news = w.ports.news_words(brest)
    assert "Aigle, a frigate, is commissioning in Brest, her company raising" in news
    assert "about 2 days" in news
    w.clock.tick = v.commission_tick - 90
    w.run(180)
    assert v.regime == "" and v.brain is not None and v.state == "on passage"
    assert v.intent_words == "keep the station off the Lizard within 20 miles"
    assert v.story[-1] == (
        197400,
        "commissioned and under way: keep the station off the Lizard within 20 miles",
    )
    assert "Aigle" not in w.ports.news_words(brest)


def test_truth_7_261_every_knob_of_the_regimes_and_the_nations_has_its_source_or_says_judgement():
    """Spec M7 §22 (package 79a, the brief's item 1): the knobs' table read whole. Every
    figure of `data/regimes.yaml` (a knob with a `value`) and every key of every nation's
    `naval:` block names its source in the references' form (a work held, by volume and
    page, or Falconer by his entry) or says judgement; a judgement on its own says what was
    looked for (or that nothing was); Mahan, not in the repository, is never the only
    source; and no source leans on memory alone."""
    regimes = yaml.safe_load(Path(REGIMES_YAML).read_text(encoding="utf-8"))["regimes"]
    knobs = [
        (f"{r}.{k}", v["source"])
        for r, body in regimes.items()
        for k, v in body.items()
        if isinstance(v, dict) and "value" in v
    ]
    assert len(knobs) == 6, knobs
    nations = yaml.safe_load(Path(NATIONS_YAML).read_text(encoding="utf-8"))["nations"]
    naval = []
    for nid, body in nations.items():
        block = body.get("naval") or {}
        sources = block.get("sources") or {}
        for key in block:
            if key in ("source", "sources"):
                continue
            said = sources.get(key) or block.get("source")
            naval.append((f"{nid}.{key}", said))
        for kind in ("blockades", "in_ordinary"):
            for entry in block.get(kind) or []:
                if isinstance(entry, dict) and "source" in entry:
                    naval.append((f"{nid}.{kind}.{entry['port']}", entry["source"]))
    # package 79c: the regency of Algiers the ninth; package 79d: the Italian states and the
    # King of Sardinia, five more
    assert len(nations) == 14 and len(naval) > 50
    for where, said in knobs + naval:
        assert said and _SOURCE_FORM.search(said), (where, said)
        if not re.search(r"(James|Nicolas|Niles|Regulations 1806|Falconer 1780) ", said):
            # a judgement with nothing cited says why: what was looked for, or the package
            assert re.search(r"looked for|package \d+|at peace|off the chart", said), (where, said)
        assert "Mahan" not in said or "not in the repository" in said, (where, said)
        assert "from memory" not in said or _SOURCE_FORM.search(said), (where, said)


def test_truth_7_262_no_figure_moved_and_a_differing_source_is_written_beside_the_knob():
    """Spec M7 §22 (package 79a, the brief's item 1: no figure moves): the regimes' figures
    are package 72's, the sortie's fifteen miles, hour and 22 knots that truth 7-154 reads
    among them; where a source gives another figure it is said beside the knob, "the source
    gives ...; kept at ... until re-measured", for the lead to rule."""
    from freesail.world.regimes import regime_knob

    assert regime_knob("in ordinary", "commission_delay_h") == [48, 120]
    assert regime_knob("in ordinary", "slip_out_clear_nm") == 15
    assert regime_knob("in ordinary", "slip_out_clear_minutes") == 60
    assert regime_knob("in ordinary", "slip_out_wind_max_kn") == 22
    assert regime_knob("in convoy", "size") == [4, 8]
    assert regime_knob("escorting", "escort") == "brig-sloop"
    regimes = yaml.safe_load(Path(REGIMES_YAML).read_text(encoding="utf-8"))["regimes"]
    kept = {
        k
        for body in regimes.values()
        for k, v in body.items()
        if isinstance(v, dict) and "until re-measured" in str(v.get("source"))
    }
    assert kept == {"commission_delay_h", "slip_out_wind_max_kn", "size"}
    assert "eleven to thirteen weeks" in regimes["in ordinary"]["commission_delay_h"]["source"]
    assert "Plymouth and Cawsand Bay" in regimes["on blockade"]["source"]


def test_truth_7_263_rochefort_is_blockaded_in_june_1805_and_not_after_stirling_raised_it():
    """Spec M7 §22 (package 79a, the brief's item 3): Britain's blockades by the dates the
    sources give. In Biscay north on 12 June 1805 the business draws the blockade of
    Rochefort (James vol. 4 pp. 78 to 79), its main body on its own offshore station off the
    point of Chassiron and its inshore brig on the road, the set's lee rendezvous the Bay of
    Quiberon (vol. 4 p. 79); on 1 August 1805, after Stirling raised it on 12 July (vol. 4
    p. 47), none; France's frigate in ordinary at Rochefort is drawn either way with her
    sortie, and keeps the sortie rule (no commission)."""
    ports = ["rochefort", "lorient", "la-rochelle", "le-palais"]
    june = _business_world("biscay-north", 46.3, -2.0, ports, datetime(1805, 6, 12, 10))
    sq = june.squadrons.find("the blockade of Rochefort")
    assert sq is not None and sq.rendezvous == "the Bay of Quiberon" and sq.nation == "britain"
    flag, brig = (june.vessels.get(m) for m in sq.members)
    assert flag.brain.intent_words == "keep the station off the point of Chassiron within 15 miles"
    assert brig.brain.intent_words == "blockade Rochefort within 6 miles"
    ordinary = [d for d in june.business.drawn if d.kind == "ordinary" and "Rochefort" in d.where]
    assert len(ordinary) == 1
    v = june.vessels.get(ordinary[0].id)
    assert v.sortie == "cruise off the Baleines within 20 miles" and v.commission_tick == -1
    august = _business_world("biscay-north", 46.3, -2.0, ports, datetime(1805, 8, 1, 10))
    assert august.squadrons.find("the blockade of Rochefort") is None
    assert not [d for d in august.business.drawn if d.kind == "blockade"]


def test_truth_7_264_cadiz_is_watched_from_the_last_of_may_and_not_between_orde_and_it():
    """Spec M7 §22 (package 79a, the brief's item 3): Cadiz under blockade by the sources'
    dates: Orde's squadron off it until Villeneuve drove him away on 9 April 1805 (James
    vol. 3 pp. 333 and 341), and from 31 May a frigate and two brigs, Collingwood by August
    (vol. 3 p. 375), the main body some fifteen miles off (p. 379). On 12 June 1805 the
    business draws the blockade of Cadiz, its frigate on the station off Cadiz within 15
    miles; on 1 May 1805, between the two, none; Spain's frigate in ordinary at Cadiz is
    drawn with her sortie off Cape Santa Maria."""
    ports = ["cadiz", "lisbon", "lagos"]
    june = _business_world("portugal", 36.4, -6.8, ports, datetime(1805, 6, 12, 10))
    sq = june.squadrons.find("the blockade of Cadiz")
    assert sq is not None
    assert june.vessels.get(sq.commander).brain.intent_words == (
        "keep the station off Cadiz within 15 miles"
    )
    spain = [d for d in june.business.drawn if d.kind == "ordinary"]
    assert [d.nation for d in spain] == ["spain"]
    assert june.vessels.get(spain[0].id).sortie == "cruise off Cape Santa Maria within 20 miles"
    may = _business_world("portugal", 36.4, -6.8, ports, datetime(1805, 5, 1, 10))
    assert may.squadrons.find("the blockade of Cadiz") is None


def test_truth_7_265_ferrol_is_blockaded_off_cape_prior_and_spains_frigate_waits_her_sortie():
    """Spec M7 §22 (package 79a, the brief's item 3): in Biscay south on 12 June 1805 the
    business draws Britain's blockade of Ferrol, its main body off Cape Prior within 15
    miles (James vol. 3 pp. 333 and 356) and its inshore brig on Ferrol's road, and Spain's
    frigate in ordinary at Ferrol with her sortie off Cape Ortegal: Spain slips out when
    the blockade is blown off (vol. 4 pp. 119 to 120), so she keeps the sortie rule and is
    not commissioned by the business."""
    w = _business_world(
        "biscay-south",
        43.8,
        -8.6,
        ["ferrol", "corunna", "vigo", "santander"],
        datetime(1805, 6, 12, 10),
    )
    sq = w.squadrons.find("the blockade of Ferrol")
    assert sq is not None and len(sq.members) == 2
    assert w.vessels.get(sq.commander).brain.intent_words == (
        "keep the station off Cape Prior within 15 miles"
    )
    (d,) = [d for d in w.business.drawn if d.kind == "ordinary"]
    v = w.vessels.get(d.id)
    assert v.nation == "spain" and v.sortie == "cruise off Cape Ortegal within 20 miles"
    w.run(120)
    assert v.commission_tick == -1 and v.regime == "in ordinary"


def test_truth_7_266_lorients_frigate_with_no_sortie_is_commissioned_for_a_passage_of_frances():
    """Spec M7 §22 (package 79a, items 2 and 3): France's frigate in ordinary at Lorient has
    no sortie (Lorient unblockaded in 1805 and the Didon sailing from it on 2 May, James vol.
    3 p. 350), so the business commissions her when it peoples the region: at seed 7 for a
    passage to La Rochelle, the delay drawn inside the regime's two to five days, in her
    story, in Lorient's news and in the business's record; Rochefort's frigate beside her,
    with her sortie, is not commissioned."""
    w = _business_world(
        "biscay-north",
        46.3,
        -2.0,
        ["rochefort", "lorient", "la-rochelle", "le-palais"],
        datetime(1805, 6, 12, 10),
    )
    drawn = {d.where: d for d in w.business.drawn if d.kind == "ordinary"}
    lorient = next(d for where, d in drawn.items() if "L'Orient" in where or "Lorient" in where)
    v = w.vessels.get(lorient.id)
    assert v.sortie == "bound for La Rochelle"
    assert (
        lorient.intent == f"commissioned for bound for La Rochelle; to sail at {v.commission_tick}"
    )
    assert 48 * 3600 <= v.commission_tick <= 120 * 3600
    assert v.story[-1][1].startswith("commissioned for bound for La Rochelle: her company raising")
    assert f"{v.name}, a frigate, is commissioning in" in w.ports.news_words(
        w.ports.ports["lorient"]
    )
    assert v.sortie in w.business.intents_for("france", w.ports.ports["lorient"])
    rochefort = next(d for where, d in drawn.items() if "Rochefort" in where)
    assert w.vessels.get(rochefort.id).commission_tick == -1


def test_truth_7_267_the_channels_business_draws_nothing_new():
    """Spec M7 §22 (package 79a: no rule a recorded passage runs is changed): in the
    Channel's west the business draws, as package 72 had it, the one blockade (Brest's,
    under the book's stations, with no rendezvous of its own) and the one ship in ordinary
    (the frigate at Brest with her sortie off the Lizard), and commissions nobody: the new
    doctrine lies in Biscay and off Cadiz."""
    w = _business_world(
        "channel-west", 50.0, -5.0, ["falmouth", "plymouth", "brest"], datetime(1805, 6, 12, 10)
    )
    blockades = [s for s in w.squadrons.sets if s.regime == "on blockade"]
    assert [s.id for s in blockades] == ["blockade-brest"] and blockades[0].rendezvous == ""
    (d,) = [d for d in w.business.drawn if d.kind == "ordinary"]
    assert d.intent == "in ordinary at Brest; the sortie cruise off the Lizard within 20 miles"
    w.run(120)
    assert w.vessels.get(d.id).commission_tick == -1
    assert all(not p.news for p in w.ports.ports.values())


def test_truth_7_268_the_commission_is_drawn_from_the_business_stream_and_moves_no_other():
    """Spec M7 §22 (package 79a, the brief's item 2): the commission's delay and intent are
    the business's own stream's (`test_the_draw_is_the_seeds_and_moves_no_other_draw`'s
    rule): the same seed draws the same commission, and a world with the ship in ordinary
    laid up has every other stream as a world without her (the weather's first draw the
    same). The director's form without a delay draws from the same stream and says the
    commission in the port's news alike."""

    def commissioned():
        w = _business_world(
            "channel-west",
            50.0,
            -5.0,
            ["falmouth", "plymouth", "brest"],
            datetime(1805, 6, 12, 10),
        )
        v, _ = _laid_up(w, "aigle", "Aigle", "france", "brest")
        w.run(60)
        return w, v

    a, va = commissioned()
    b, vb = commissioned()
    assert (va.sortie, va.commission_tick) == (vb.sortie, vb.commission_tick)
    plain = _business_world(
        "channel-west", 50.0, -5.0, ["falmouth", "plymouth", "brest"], datetime(1805, 6, 12, 10)
    )
    plain.run(60)
    assert plain.rng.stream("weather").random() == a.rng.stream("weather").random()
    # the director's commission with no delay said: the regime's delay, the port's news
    quiet = make_world(
        SEED,
        "data/ships/topsail-schooner.yaml",
        Scenario(
            start_time=datetime(1805, 6, 12, 10),
            wind_from_deg=270.0,
            wind_speed_kn=14.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 50.0, "lon_deg": -5.0},
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            nation="britain",
        ),
    )
    v, brest = _laid_up(quiet, "harpy", "Harpy", "france", "brest")
    quiet.world_order('ship "Harpy": commissioned for bound for Roscoff', "the test")
    assert 48 * 3600 <= v.commission_tick <= 120 * 3600
    assert "Harpy, a frigate, is commissioning in Brest" in quiet.ports.news_words(brest)


def test_truth_7_269_a_ship_in_ordinary_with_no_intent_of_her_nations_in_the_waters_stays_laid_up():
    """Spec M7 §22 (package 79a, the brief's item 2): the business gives a ship it
    commissions an intent of her own nation's in the waters in play; a Moorish frigate in
    ordinary at Tangier, the Emperor's one port in play and no station of his in the
    cruisers' doctrine, has none, and stays in ordinary, said once in her story; nothing
    is drawn for her and the port's news is silent of her."""
    w = _business_world("strait", 36.0, -5.6, ["gibraltar", "tangier"], datetime(1805, 6, 12, 10))
    v, tangier = _laid_up(w, "mabrouk", "Mabrouk", "morocco", "tangier")
    w.run(180)
    assert v.regime == "in ordinary" and v.commission_tick == -1 and v.brain is None
    assert [words for _t, words in v.story] == [
        "no intent of her nation's in these waters: she stays in ordinary"
    ]
    assert "Mabrouk" not in w.ports.news_words(tangier)


# ---------------------------------------------------------------------------
# Package 79b: the Channel's east block, the Wight to Dunkirk (truths 7-270 to 7-279)
# ---------------------------------------------------------------------------

EAST_PORTS = ["portsmouth", "poole", "downs", "dover", "le-havre", "boulogne", "calais", "dunkirk"]
SPITHEAD = (50.7600, -1.1250)  # features/channel-east.yaml's `spithead`


def _east_at(lat: float, lon: float, when: datetime, ship: str = FRIGATE, **kw):
    """A world on the whole chart in the Channel's east block at seed 7, the block's eight
    ports loaded, a steady breeze (from the east unless given)."""
    sc = Scenario(
        start_time=when,
        wind_from_deg=kw.pop("wind_from_deg", 80.0),
        wind_speed_kn=kw.pop("wind_speed_kn", 12.0),
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        chart="atlantic-east",
        ports=kw.pop("ports", EAST_PORTS),
        nation=kw.pop("nation", "britain"),
        **kw,
    )
    return make_world(SEED, ship, sc)


def _sighted(w) -> dict[str, dict]:
    return {e.data["id"]: e.data for e in w.log if e.kind == "lookout.sighting" and e.data}


def test_truth_7_270_from_spithead_the_nab_is_seen_by_night_at_its_range_and_the_wight_by_day():
    """The brief's item 9: the frigate's lookout at Spithead. By night the Nab light-vessel
    east of Bembridge ledge is raised at her range of two leagues, but only from the year
    she came on her station (24 September 1812: in 1805 there was a buoy, Moore 1799); from
    ten miles off, beyond her eight, she is not seen. By day the Wight's marks are made out:
    the Kicker Point, Ryde, Nettlestone Point, and Culver Cliff or Ashey Down tower."""
    night_1805 = _east_at(*SPITHEAD, datetime(1805, 6, 20, 23, 30))
    assert night_1805.daylight == "night"
    night_1805.run(120)
    assert "nab-light" not in _sighted(night_1805)
    night_1815 = _east_at(*SPITHEAD, datetime(1815, 6, 20, 23, 30))
    night_1815.run(120)
    nab = _sighted(night_1815).get("nab-light")
    assert nab is not None and nab["seen_as"] == "light"
    assert 4.0 < nab["distance_m"] / units.NAUTICAL_MILE < 8.0  # within her eight miles
    from freesail.world.geo import Position, destination

    nab_pos = night_1815.chart.feature("nab-light").position
    off = destination(nab_pos, 160.0, 10.0 * units.NAUTICAL_MILE)
    beyond = _east_at(off.lat_deg, off.lon_deg, datetime(1815, 6, 20, 23, 30))
    beyond.run(120)
    assert "nab-light" not in _sighted(beyond)
    day = _east_at(*SPITHEAD, datetime(1805, 6, 20, 12, 0))
    day.run(300)
    seen = set(_sighted(day))  # the lookout's first calls, the nearest first
    assert {"gilkicker-point", "ryde", "nettlestone-point"} <= seen, seen
    # and what stands in sight of her masthead in clear weather: the Wight's high marks
    eye = nab["height_of_eye_m"]
    in_sight = {
        s.feature.id
        for s in day.chart.in_sight(day.position, eye, None, "day", datetime(1805, 6, 20, 12, 5))
    }
    assert {"culver-cliff", "ashey-down-tower", "portsdown-hill", "bembridge-point"} <= in_sight
    assert "nab-light" not in in_sight or not day.chart.feature("nab-light").lit_in(1805)
    assert day.chart.region_at(Position(*SPITHEAD)) == "channel-mid"  # the patch in its water
    assert day.chart.level_at(Position(*SPITHEAD)) == 3


def test_truth_7_271_the_strait_of_dover_sets_her_as_the_directions_say_at_springs():
    """The brief's item 9: in the middle of the Strait at springs (two days after the new
    moon of 10 June 1805) the world's stream runs north-east by east on the flood and
    south-west by west on the ebb (Faden 1793: the flood N E by E, the ebb S W by W), and
    the master's directions say the same water; a ship lying with no way on through the
    hour of the ebb's strength is carried two miles and more to the south-west by west,
    and his account, working the directions' stream, goes with her within eight tenths of a
    mile (half a mile on the eleven's water; package 89 below)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position, bearing_and_distance

    tide = T.load_tide()
    mid = Position(51.0, 1.45)
    start = datetime(1805, 6, 12, 0, 0)
    states = [
        (start + timedelta(minutes=10 * i), tide.at(mid, start + timedelta(minutes=10 * i)))
        for i in range(150)
    ]
    assert {s.area_id for _, s in states} == {"strait-of-dover"}
    flood = [
        s for _, s in states if abs(((s.stream_toward_deg - 56.25) + 180.0) % 360.0 - 180.0) < 1.0
    ]
    ebb = [
        s for _, s in states if abs(((s.stream_toward_deg - 236.25) + 180.0) % 360.0 - 180.0) < 1.0
    ]
    assert max(s.stream_kn for s in flood) > 2.0 and max(s.stream_kn for s in ebb) > 2.0
    said = T.load_directions().area_at(mid)
    assert said.id == "strait-of-dover" and said.set_point == "NE by E" and said.spring_kn == 3.0
    when, strongest = max(states, key=lambda t: t[1].stream_kn if t[1] in ebb else 0.0)
    w = _east_at(
        51.0,
        1.45,
        when - timedelta(minutes=30),
        wind_from_deg=0.0,
        wind_speed_kn=2.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
    )
    truth0, account0 = w.position, w.navigation.account_now()
    w.run(3600)
    toward, run_m = bearing_and_distance(truth0, w.position)
    assert run_m / units.NAUTICAL_MILE > 2.0
    assert abs(((toward - 236.25) + 180.0) % 360.0 - 180.0) < 15.0  # south-west by west
    a_toward, a_run = bearing_and_distance(account0, w.navigation.account_now())
    assert abs(((a_toward - 236.25) + 180.0) % 360.0 - 180.0) < 15.0
    _, error = bearing_and_distance(w.position, w.navigation.account_now())
    # package 89: the Strait's water the block's own gauges' (Calais, Boulogne, Dunkirk in
    # the blend beside Dover), the ebb's strength ten minutes later (19:30 for 19:20) and
    # the master's account of the hour 1.83 miles for 2.02: the error 0.648 miles where it
    # was 0.452 on the eleven's water against this bound's 0.6; re-measured to 0.8, the
    # old margin's 0.15 mile kept (the lead's ruling, 2026-10-30)
    assert error / units.NAUTICAL_MILE < 0.8


def test_truth_7_272_the_goodwin_grounds_a_ship_standing_across_it_drawing_more_than_its_water():
    """The brief's item 9: the frigate, drawing fifteen feet, stands east out of the Gull
    Stream across the North Goodwin near low water (the sand dry for a great extent, Imray
    1874; steep-to, Moore 1799) and takes the ground on it; the head of the North Goodwin
    by name grounds her too where the tide leaves less water over it than she draws, and
    a ship over the same head at high water with water to spare is not aground."""
    from freesail.world.geo import bearing_and_distance

    w = _east_at(
        51.300,
        1.500,
        datetime(1805, 6, 20, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        ship_heading_deg=90.0,
        ship_speed_kn=6.0,
    )
    assert w.tide_height_m < 2.6  # near low water
    w.submit("set plain sail")
    w.submit("steer east")
    w.run(1500)
    aground = [e for e in w.log if e.kind == "ship.aground"]
    assert aground, [e.text for e in w.log if e.kind.startswith("ship.")][-5:]
    head = w.chart.feature("north-goodwin")
    _, off = bearing_and_distance(w.position, head.position)
    assert off < 3000.0  # on the North Goodwin's sand
    draught = units.feet_to_m(15.0)  # the frigate's, as the grounding's line says
    grounding = w.chart.danger_under(head.position, math.radians(90.0), 40.0, draught, tide_m=2.2)
    assert grounding is not None and "North Goodwin" in grounding.bottom
    assert w.chart.danger_under(head.position, math.radians(90.0), 40.0, 1.0, tide_m=5.0) is None


def test_truth_7_273_the_downs_hold_her_in_a_south_westerly_with_the_goodwin_to_leeward():
    """The brief's item 9: brought up by the best bower in the Downs off Deal (seven or
    eight fathoms on chalk, White 1835), a south-westerly of twenty-four knots for six
    hours does not drag her: she lies within her cable's swing of where she brought up,
    and the Goodwin lies to leeward of her, three miles off."""
    from freesail.world.geo import bearing_and_distance

    w = _east_at(
        51.2200,
        1.4400,
        datetime(1805, 6, 20, 4, 0),
        wind_from_deg=225.0,
        wind_speed_kn=24.0,
        ship_heading_deg=225.0,
    )
    w.submit("let go the best bower")
    w.run(600)
    assert any(e.kind == "ship.brought_up" for e in w.log)
    brought = w.position
    w.run(6 * 3600)
    assert not [e for e in w.log if "drag" in e.kind or "aground" in e.kind]
    _, moved = bearing_and_distance(brought, w.position)
    assert moved < 0.2 * units.NAUTICAL_MILE
    sand_bearing, sand_m = bearing_and_distance(
        w.position, w.chart.feature("south-goodwin").position
    )
    downwind = 45.0  # the wind from the south-west blows toward the north-east
    assert abs(((sand_bearing - downwind) + 180.0) % 360.0 - 180.0) < 60.0
    assert 2.0 < sand_m / units.NAUTICAL_MILE < 5.0


def test_truth_7_274_a_passage_crosses_the_seam_at_1_w_with_the_business_carried():
    """The brief's item 9 (truth 7-157's kind): the schooner from three miles west of 1 W,
    south of the Wight, before a westerly, crosses from channel-mid's water into the
    Channel's east block within the hour; the business follows her and peoples the new
    region once, and the depth does not step across the seam (the two tiles cut from the
    one grid)."""
    from freesail.world.geo import Position

    w = _east_at(
        50.40,
        -1.08,
        datetime(1805, 6, 12, 10, 0),
        ship=SCHOONER,
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        ship_heading_deg=90.0,
        ship_speed_kn=5.0,
        business="on",
    )
    b = w.business
    assert b.region == "channel-mid" and b.regions_entered == ["channel-mid"]
    before = len(b.drawn)
    w.submit("set plain sail")
    w.submit("steer east")
    crossed = None
    for _ in range(12):
        w.run(600)
        if b.region == "channel-east":
            crossed = w.clock.tick
            break
    assert crossed is not None and crossed <= 3600, (b.region, w.position)
    assert b.regions_entered == ["channel-mid", "channel-east"] and len(b.drawn) > before
    a, c = Position(50.40, -1.002), Position(50.40, -0.998)
    assert w.chart.region_at(a) == "channel-mid" and w.chart.region_at(c) == "channel-east"
    assert abs(w.chart.depth_at(a) - w.chart.depth_at(c)) < 1.0


def test_truth_7_275_the_blocks_ports_load_on_either_chart_and_take_the_tables_stance():
    """The brief's items 4 and 9: the eight port files load on the whole chart, their roads
    the block's features, and on the Channel's chart alone (a recorded passage's), where
    every spot falls back to its own position, the same; Portsmouth's yard is the King's
    and its powder is taken in at Spithead; the four French ports of the invasion coast
    are hostile to a King's ship and neutral to an American; the Downs' boatmen come off
    by night."""
    whole = _east_at(51.0, 1.45, datetime(1805, 6, 12, 12, 0))
    # the Channel's chart alone with no ports named, as the gate 5b passages: every file
    alone = make_world(
        SEED,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 12, 12, 0),
            wind_from_deg=270.0,
            wind_speed_kn=14.0,
            position={"lat_deg": 49.5, "lon_deg": -5.5},
            region="channel-west",
            nation="britain",
        ),
    )
    for pid in EAST_PORTS:
        port = whole.ports.ports[pid]
        same = alone.ports.ports[pid]
        for label in ("outer_road", "anchorage", "mooring"):
            spot, other = getattr(port, label), getattr(same, label)
            assert spot.position.lat_deg == pytest.approx(other.position.lat_deg, abs=1e-6), pid
            if spot.feature_id:
                f = whole.chart.feature(spot.feature_id)
                assert spot.position.lat_deg == pytest.approx(f.position.lat_deg, abs=1e-4), pid
    ports = whole.ports.ports
    assert ports["portsmouth"].dockyard.kind == "yard"
    assert ports["portsmouth"].anchorage.feature_id == "spithead"
    assert {pid: whole.dealings.stance(ports[pid]) for pid in EAST_PORTS} == {
        "portsmouth": "open",
        "poole": "open",
        "downs": "open",
        "dover": "open",
        "le-havre": "hostile",
        "boulogne": "hostile",
        "calais": "hostile",
        "dunkirk": "hostile",
    }
    american = _east_at(
        51.0, 1.45, datetime(1805, 6, 12, 12, 0), ship=SCHOONER, nation="united-states"
    )
    assert {american.dealings.stance(american.ports.ports[p]) for p in EAST_PORTS} == {"neutral"}
    assert ports["downs"].pilot.by_night and not ports["dover"].pilot.by_night


def test_truth_7_276_the_strait_by_night_shows_the_lights_1805_had_and_not_the_later():
    """The brief's item 3: from the middle of the Strait by night in 1805 the South
    Foreland's two lights are seen, and neither Gris Nez's (lit 1837) nor Calais's (the
    watch-tower's light of 1818, the tower of 1848), though Gris Nez stands nearest; in
    1840 Gris Nez's light is seen from the same place."""
    w = _east_at(51.0, 1.45, datetime(1805, 6, 12, 23, 30))
    eye = 36.0

    def lights(year: int) -> set[str]:
        return {
            s.feature.id
            for s in w.chart.in_sight(w.position, eye, None, "night", datetime(year, 6, 12, 23, 30))
            if s.seen_as == "light"
        }

    in_1805 = lights(1805)
    assert {"south-foreland-upper-light", "south-foreland-lower-light"} <= in_1805, in_1805
    assert not in_1805 & {"gris-nez-light", "calais-tour-du-guet-light", "calais-light"}
    assert "gris-nez-light" in lights(1840)


def test_truth_7_277_dover_and_portsmouth_have_their_1805_waters_not_the_later_works():
    """The brief's item 3: Dover without the Admiralty harbour (its pier begun in 1847):
    the line of the later breakwaters across Dover bay is water, a ship may stand across
    it; the harbour's mouth at Portsmouth between the Point and Blockhouse is a channel for
    a frigate; the port files say their datum is unverified, no sheet being read."""
    from freesail.world.geo import Position

    w = _east_at(51.0, 1.45, datetime(1805, 6, 12, 12, 0))
    for i in range(11):
        f = i / 10.0
        p = Position(51.1080 + 0.004 * f, 1.3100 + 0.035 * f)
        assert w.chart.depth_at(p) > 3.0, p
    assert w.chart.depth_at(Position(50.7895, -1.1085)) > 6.0
    for pid in ("portsmouth", "dover"):
        import yaml

        doc = yaml.safe_load(
            (Path(__file__).resolve().parents[1] / "data" / "ports" / f"{pid}.yaml").read_text(
                encoding="utf-8"
            )
        )
        assert doc["datum"] == "unverified"


def test_truth_7_278_the_masters_tide_in_the_block_is_norie_1805s():
    """The brief's item 5: the master's tide by the almanac at Spithead names his epitome's
    Spithead (Norie 1805, Table XLI: 9h 30m at full and change), in the Downs the Downs
    (11h 0m), off Dunkirk Dunkirk (11h 45m); each the nearest place of his table."""
    for (lat, lon), name in (
        (SPITHEAD, "Spithead"),
        ((51.2200, 1.4400), "the Downs"),
        ((51.0619, 2.3691), "Dunkirk"),
    ):
        w = _east_at(lat, lon, datetime(1805, 6, 12, 12, 0))
        words = w.navigation.tide_by_almanac()["words"]
        assert name in words and "may differ by hours" not in words, words


def test_truth_7_279_the_frigate_sails_from_the_downs_to_spithead_by_her_short_book():
    """The brief's item 7: the block's scenario (`spithead.yaml`) sailed at seed 7 by its
    short book: from the Downs past the South Foreland, Dungeness, the Royal Sovereign
    and the Owers to the Nab without touching ground; at St Helens by night she anchors by
    the lead in the road, at daylight she weighs, the Portsmouth pilot boards her, and she
    brings up at Spithead within its limits and he leaves her, within a day and a quarter."""
    from freesail.world.geo import Position, bearing_and_distance
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    root = Path(__file__).resolve().parents[1]
    sf = load_scenario(root / "data" / "scenarios" / "spithead.yaml")
    w = make_scenario_world(sf)
    assert begin(w, sf) >= 10
    for _ in range(28 * 6):
        w.run(600)
        if any(e.kind == "port.pilot_left" for e in w.log):
            break
    assert not [e for e in w.log if e.kind == "ship.aground"]
    anchored = [e for e in w.log if e.kind == "ship.anchored"]
    assert len(anchored) == 3  # the Downs at the start, St Helens for the night, Spithead
    pilot = [e for e in w.log if e.kind == "port.pilot_aboard"]
    assert pilot and "Portsmouth" in pilot[0].text
    assert any(e.kind == "port.pilot_left" for e in w.log)
    assert w.clock.tick <= 27 * 3600
    _, off = bearing_and_distance(w.position, Position(*SPITHEAD))
    assert off < 0.5 * units.NAUTICAL_MILE


# ---------------------------------------------------------------------------
# Package 89: the held gauges' water (truths 7-280 to 7-284): a block's gauge serves the
# positions within its own block's bounds and no other; the eleven serve everywhere
# ---------------------------------------------------------------------------


def _the_eleven_alone(streams=None):
    """The world's tide as it was before package 89 everywhere: the eleven gauges alone
    (with the streams' areas when given)."""
    import freesail.world.tide as T

    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    eleven = [g for g in doc["gauges"] if "block" not in g]
    return T.Tide({**doc, "gauges": eleven}, streams or {"areas": []})


def _spring_range_ft(tide, pos) -> float:
    _, consts = tide.constants_at(pos)
    return units.m_to_feet(2.0 * (consts["M2"][0] + consts["S2"][0]))


def test_truth_7_280_newhaven_dieppe_and_beachy_head_have_their_own_spring_range():
    """The brief's item 5: the world's spring range at Newhaven and Dieppe within a foot of
    the gauge's own (19.5 and 27 feet, where the eleven's blend gave 3.9 and 5.3), and at
    Beachy Head, which has no gauge, within a foot and a quarter of Norie 1805's twenty (the
    blend gave 4.8): 18.99 feet, Newhaven's water seven miles off. The brief had "within a
    foot"; the measured gap is a foot and a hundredth, and Norie's twenty is a round
    figure, so the lead amended it (2026-10-30). Since package 94's rule of the seams
    (Portsmouth's gauge serving the Channel east within ten miles of 1 W) 18.86 feet, within
    the words (the lead's ruling of 2026-10-30)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    gauges = {g["id"]: g for g in doc["gauges"]}
    eleven = _the_eleven_alone()
    for gid in ("newhaven", "dieppe"):
        g = gauges[gid]
        at = Position(g["lat_deg"], g["lon_deg"])
        own = units.m_to_feet(2.0 * (g["M2"]["amplitude_m"] + g["S2"]["amplitude_m"]))
        assert abs(_spring_range_ft(tide, at) - own) < 1.0, gid
        assert _spring_range_ft(eleven, at) < 6.0, gid  # what the blend had
    beachy = T.Epitome.load("norie").by_name("Beachy Head")
    assert beachy.spring_rise_ft == 20.0 and not beachy.rise_judgement
    assert abs(_spring_range_ft(tide, beachy.position) - 20.0) < 1.25
    assert _spring_range_ft(eleven, beachy.position) < 6.0


def test_truth_7_281_vigo_and_cadiz_have_their_gauges_spring_range():
    """The brief's item 5: the world's spring range at Vigo and at Cadiz within a foot of
    their gauges' own, where the nearest of the eleven alone gave Le Conquet's eighteen
    feet (both beyond the reach of every one of them, far)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    gauges = {g["id"]: g for g in doc["gauges"]}
    eleven = _the_eleven_alone()
    for gid in ("vigo", "cadiz"):
        g = gauges[gid]
        at = Position(g["lat_deg"], g["lon_deg"])
        own = units.m_to_feet(2.0 * (g["M2"]["amplitude_m"] + g["S2"]["amplitude_m"]))
        assert abs(_spring_range_ft(tide, at) - own) < 1.0, gid
        assert not tide.constants_about(at)[3], gid  # near its own gauge, not far
        assert eleven.constants_about(at)[3] and _spring_range_ft(eleven, at) > 17.0, gid


def test_truth_7_282_a_mile_west_of_1_w_the_tide_is_as_before_and_a_mile_east_the_blocks():
    """The brief's item 5: a position a mile west of 1 W in `channel-mid` reads the same
    tide to the centimetre as before the package (the eleven alone), its height and stream
    hour by hour through a day of springs; a position a mile east, in `channel-east`,
    reads the block's (its gauges in the blend, the spring range other by feet).
    Re-measured by package 94's taper: a mile east the block's water is a thirty-sixth
    part in (the smoothstep of a tenth of the band), its constants other than the eleven's
    and its spring range within half a foot of theirs (10.07 feet against 10.11; 89's
    rule gave 8.6 against 10.2); the block's own water whole from the band's ten miles in,
    eleven miles east the spring range 11.4 feet against the eleven's 9.3, other by feet
    as the truth had it a mile east. The west position to the bit, as before."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    eleven = _the_eleven_alone()
    mile_deg = 1.0 / 60.0 / math.cos(math.radians(50.6))
    west, east = Position(50.6, -1.0 - mile_deg), Position(50.6, -1.0 + mile_deg)
    assert tide.blocks_at(west) == frozenset() and tide.blocks_at(east) == {"channel-east"}
    before = _the_eleven_alone(yaml.safe_load(T.STREAMS_PATH.read_text(encoding="utf-8")))
    for h in range(25):
        when = datetime(1805, 6, 12) + timedelta(hours=h)
        now, then = tide.at(west, when), before.at(west, when)
        assert abs(now.height_m - then.height_m) < 0.01
        assert abs(now.stream_kn - then.stream_kn) < 0.01 and now.area_id == then.area_id
        assert now == then  # to the bit, not only to the centimetre
    assert tide.constants_about(west) == eleven.constants_about(west)
    assert abs(_spring_range_ft(tide, east) - _spring_range_ft(eleven, east)) < 0.5
    assert tide.constants_at(east) != eleven.constants_at(east)
    beyond = Position(50.6, -1.0 + 11.0 * mile_deg)  # past the taper's band
    assert tide.taper_at(beyond) == 1.0
    assert abs(_spring_range_ft(tide, beyond) - _spring_range_ft(eleven, beyond)) > 1.0


def test_truth_7_283_the_recorded_passages_water_reads_the_tide_it_read():
    """The brief's item 5, as a behaviour: every recorded passage (the frigate's and the
    schooner's of gate 5b, Ushant to Falmouth; the merchant passage and the naval cruise
    of gate 5c, Falmouth for Brest and Plymouth to the station off Ushant; the schooner
    on an intent and the fake captain's on the merchant's water) sails the Channel west
    and its approaches, where no block's gauge serves and the tide is the eleven's to the
    bit, hour by hour, over the whole of `channel-west` and of `channel-mid` west of 1 W,
    and the master's rises at every place of his tables there are as they were. The one
    water of theirs a block reaches is the naval cruise's Diamond's patrol, eight miles
    about 48 N 4 55 W, whose southern half lies in Biscay north: her stream there is the
    block's now, and the cruise's digest stands all the same (package 89 ran the eleven
    passage tests by name, `gate_5b or gate_5c` and the captain's trials before and after
    the rule, every digest held: docs/dev/TuningNotes.md, package 89)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    eleven = _the_eleven_alone(yaml.safe_load(T.STREAMS_PATH.read_text(encoding="utf-8")))
    root = Path(__file__).resolve().parents[1]
    for name in (
        "gate-5b-passage",
        "gate-5b-passage-schooner",
        "gate-5b-passage-thick",
        "merchant-passage",
        "merchant-intent",
        "naval-cruise",
    ):
        sf = yaml.safe_load((root / "data" / "scenarios" / f"{name}.yaml").read_text("utf-8"))
        assert sf.get("chart") in (None, "channel", "channel-west", "atlantic-east"), name
    for lat10 in range(480, 511, 3):
        for lon10 in range(-70, -10, 3):
            pos = Position(lat10 / 10.0 + 0.005, lon10 / 10.0 + 0.005)
            if lon10 > -30 and lat10 < 485:
                continue  # south of channel-mid, Biscay north's water
            if lon10 > -23 and 506 < lat10 < 510:
                # the Solent's water since package 94 (its tide region, 50.62 to 51 N and
                # 2.2 to 1 W): three positions of the grid, none a recorded passage's
                assert tide.blocks_at(pos) == {"solent"}, pos
                continue
            assert not tide.blocks_at(pos), pos
            for h in (0, 5, 13, 19):
                when = datetime(1805, 6, 12) + timedelta(hours=h)
                assert tide.at(pos, when) == eleven.at(pos, when), (pos, h)
    for table in ("norie", "moore"):
        for port in T.Epitome.load(table).ports:
            p = port.position
            if p.lat_deg >= 48.0 and p.lon_deg < -1.0 and not tide.blocks_at(p):
                assert tide.constants_at(p) == eleven.constants_at(p), port.name
    diamond = Position(48.0 - 4.0 / 60.0, -4.9167)
    assert tide.blocks_at(diamond) == {"biscay-north"}
    assert tide.constants_at(diamond) != eleven.constants_at(diamond)


def test_truth_7_284_the_blend_adds_a_membership_and_not_a_gauge():
    """The brief's item 5: the pace of the tide's blend is unchanged within the measure.
    Outside every block the gauges blended are the eleven, the same list (no gauge more to
    weigh), and the work of a fresh cell is the eleven's and the bounds' test, within a
    quarter of the eleven's alone (the best of five runs over three hundred fresh cells of
    the Channel west each); a cell once worked is a lookup, as before."""
    import time

    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    eleven = _the_eleven_alone()
    assert tide.gauges_at(Position(49.9, -5.2)) is tide.gauges

    def fresh(t) -> float:
        best = math.inf
        for _ in range(5):
            t._about_cache = {}
            t0 = time.perf_counter()
            for i in range(300):
                t.constants_about(Position(49.0 + 0.011 * (i % 30), -6.5 + 0.011 * (i // 30)))
            best = min(best, time.perf_counter() - t0)
        return best

    now, then = fresh(tide), fresh(eleven)
    assert now < 1.25 * then, (now, then)
    t0 = time.perf_counter()
    for _ in range(10_000):
        tide.constants_about(Position(49.9, -5.2))
    assert (time.perf_counter() - t0) / 10_000 < 20e-6  # a lookup


# ---------------------------------------------------------------------------
# Package 79c: the Mediterranean west, the Strait to Cartagena, the Balearics and Barbary
# to Algiers, two regions by the lead's ruling (truths 7-285 to 7-294)
# ---------------------------------------------------------------------------

MED_PORTS = [
    "gibraltar",
    "malaga",
    "almeria",
    "cartagena",
    "ivica",
    "palma",
    "port-mahon",
    "oran",
    "algiers",
]
MED_SPANISH = ["malaga", "almeria", "cartagena", "ivica", "palma", "port-mahon"]
MAHON_MOUTH = (39.8600, 4.3170)  # features/balearics.yaml's `mahon-outer-road`


def _med_at(lat: float, lon: float, when: datetime, ship: str = FRIGATE, **kw):
    """A world on the whole chart in the Mediterranean west at seed 7, the block's ports and
    Gibraltar loaded, a steady breeze (from the west unless given)."""
    sc = Scenario(
        start_time=when,
        wind_from_deg=kw.pop("wind_from_deg", 270.0),
        wind_speed_kn=kw.pop("wind_speed_kn", 12.0),
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        chart="atlantic-east",
        ports=kw.pop("ports", MED_PORTS),
        nation=kw.pop("nation", "britain"),
        **kw,
    )
    return make_world(SEED, ship, sc)


def test_truth_7_285_off_europa_point_the_sierras_marks_and_the_barbary_shore_are_in_sight():
    """The brief's item 9: six leagues east of Europa Point by a clear day the masthead
    raises the marks Tofiño gives for knowing where you are when the Rock is hidden (the
    top of the Sierra de Marbella, the Picacho de Juana, the Sierra de Mijas: 1787, pp. 31
    to 32) and, across the water, Ape's Hill over Ceuta on the Barbary shore; by night in
    1805 no light is in sight there (Europa Point's of 1841 not yet, Málaga's lantern beyond
    its range)."""
    from freesail.world.geo import Position

    here = Position(36.05, -4.95)  # six leagues east of Europa Point, in the block's water
    w = _med_at(here.lat_deg, here.lon_deg, datetime(1805, 6, 14, 12, 0))
    assert w.chart.region_at(here) == "mediterranean-west"
    seen = {
        s.feature.id
        for s in w.chart.in_sight(here, 30.0, None, "day", datetime(1805, 6, 14, 12, 0))
    }
    assert {"sierra-de-marbella", "picacho-de-juanar", "sierra-de-mijas", "apes-hill"} <= seen
    assert "gibraltar-rock" in seen
    night = datetime(1805, 6, 14, 23, 30)
    lights = [
        s.feature.id
        for s in w.chart.in_sight(here, 30.0, None, "night", night)
        if s.feature.kind == "light"
    ]
    assert lights == []


def test_truth_7_286_bound_east_from_the_strait_she_is_set_east_by_the_current_and_knows_it():
    """The brief's item 9: off the coast of Granada a ship lying with no way on is carried
    to the eastward at about a knot (Smyth 1854, p. 161: along the coast of Granada at the
    rate of one knot an hour eastwards; Tofiño 1787, p. 46: much current to the east), the
    tide nothing; the master's directions give the same current and his account goes with
    her within a mile in three hours."""
    import freesail.world.tide as T
    from freesail.world.geo import Position, bearing_and_distance

    here = Position(36.60, -4.30)
    said = T.load_directions().area_at(here)
    assert said.id == "granada-coast" and (said.current_point, said.current_kn) == ("E", 1.0)
    assert said.spring_kn == 0.0
    w = _med_at(
        here.lat_deg,
        here.lon_deg,
        datetime(1805, 6, 14, 10, 0),
        wind_from_deg=0.0,
        wind_speed_kn=2.0,
        ship_heading_deg=90.0,
        ship_speed_kn=0.0,
    )
    truth0, account0 = w.position, w.navigation.account_now()
    w.run(3 * 3600)
    toward, run_m = bearing_and_distance(truth0, w.position)
    assert 2.4 < run_m / units.NAUTICAL_MILE < 4.0
    assert abs(((toward - 90.0) + 180.0) % 360.0 - 180.0) < 20.0
    a_toward, _ = bearing_and_distance(account0, w.navigation.account_now())
    assert abs(((a_toward - 90.0) + 180.0) % 360.0 - 180.0) < 20.0
    _, error = bearing_and_distance(w.position, w.navigation.account_now())
    assert error / units.NAUTICAL_MILE < 1.0


def test_truth_7_287_the_freu_grande_is_entered_on_its_marks_and_sets_her_by_the_wind():
    """The brief's item 9: approaching the Freu Grande between Ivica and Formentera from the
    westward, she has in sight the tower of the Espalmador she steers for, the tower of the
    Portas that has been taken for it to the loss of ships on the Trocados, the Vedrá to the
    westward and the castle of Ivica beyond (Tofiño 1787, pp. 181 to 182); the directions
    give the channels no constant current, the water following the wind (p. 208)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    here = Position(38.82, 1.30)  # two leagues west of the Freu Grande
    w = _med_at(here.lat_deg, here.lon_deg, datetime(1805, 6, 15, 12, 0))
    seen = {
        s.feature.id
        for s in w.chart.in_sight(here, 30.0, None, "day", datetime(1805, 6, 15, 12, 0))
    }
    assert {"espalmador-tower", "portas-tower", "vedra", "ivica-castle"} <= seen, seen
    said = T.load_directions().area_at(Position(38.80, 1.43))
    assert said.id == "balearic-channels" and said.current_kn == 0.0
    assert w.chart.feature("trocados").kind in ("shoal", "rock", "ledge")


def test_truth_7_288_the_mouth_of_port_mahon_holds_a_frigate_at_anchor_in_a_northerly():
    """The brief's item 9: brought up by the best bower without the ledges at the mouth of
    Port Mahon in twenty brazas and more, good ground (Tofiño 1787, p. 213: with a scant
    wind a ship may anchor among the ledges or farther out), a northerly of twenty knots for
    six hours does not drag her: she lies within her cable's swing, Cape Mola to windward."""
    from freesail.world.geo import bearing_and_distance

    w = _med_at(
        *MAHON_MOUTH,
        datetime(1805, 6, 17, 12, 0),
        wind_from_deg=0.0,
        wind_speed_kn=20.0,
        ship_heading_deg=0.0,
    )
    assert 25.0 < w.chart.depth_at(w.position) < 60.0
    w.submit("let go the best bower")
    w.run(600)
    assert any(e.kind == "ship.brought_up" for e in w.log)
    brought = w.position
    w.run(6 * 3600)
    assert not [e for e in w.log if "drag" in e.kind or "aground" in e.kind]
    _, moved = bearing_and_distance(brought, w.position)
    assert moved < 0.2 * units.NAUTICAL_MILE
    mola, mola_m = bearing_and_distance(w.position, w.chart.feature("cape-mola-mahon").position)
    assert abs(((mola - 0.0) + 180.0) % 360.0 - 180.0) < 45.0  # to windward
    assert mola_m / units.NAUTICAL_MILE < 2.0


def test_truth_7_289_the_spanish_ports_refuse_a_kings_ship_and_the_regencys_receive_her():
    """The brief's items 4 and 9: in June 1805 the six Spanish ports of the block are hostile
    to a King's ship (Spain at war since December 1804), Oran and Algiers neutral to her, the
    regency at peace with Britain (James vol. 3, pp. 235 and 333 to 334); to an American all
    eight are neutral; the regency is a nation of data alone, Morocco's form."""
    w = _med_at(36.6, -3.0, datetime(1805, 6, 14, 10, 0))
    ports = w.ports.ports
    stance = {pid: w.dealings.stance(ports[pid]) for pid in MED_SPANISH + ["oran", "algiers"]}
    assert stance == {
        **{p: "hostile" for p in MED_SPANISH},
        "oran": "neutral",
        "algiers": "neutral",
    }
    american = _med_at(
        36.6, -3.0, datetime(1805, 6, 14, 10, 0), ship=SCHOONER, nation="united-states"
    )
    assert {american.dealings.stance(american.ports.ports[p]) for p in stance} == {"neutral"}
    table = w.nations
    assert table.get("algiers").adjective == "Algerine" and not table.enemies_of("algiers")
    assert (
        ports["cartagena"].dockyard.kind == "yard" and ports["port-mahon"].dockyard.kind == "yard"
    )
    assert ports["algiers"].nation == "algiers" and ports["oran"].nation == "algiers"


def test_truth_7_290_the_seam_at_5_w_is_crossed_with_the_business_carried():
    """The brief's item 9: the schooner from a little west of 5 W before a westerly crosses
    from the Strait's water into the Mediterranean west within the hour; the business
    follows her and peoples the new region once (the Barbary grain bound from Oran to the
    Spanish coast), and the depth does not step across the seam."""
    from freesail.world.geo import Position

    w = _med_at(
        36.30,
        -5.10,
        datetime(1805, 6, 14, 10, 0),
        ship=SCHOONER,
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        ship_heading_deg=90.0,
        ship_speed_kn=5.0,
        business="on",
    )
    b = w.business
    assert b.region == "strait" and b.regions_entered == ["strait"]
    before = len(b.drawn)
    w.submit("set plain sail")
    w.submit("steer east")
    crossed = None
    for _ in range(12):
        w.run(600)
        if b.region == "mediterranean-west":
            crossed = w.clock.tick
            break
    assert crossed is not None and crossed <= 3600, (b.region, w.position)
    assert b.regions_entered == ["strait", "mediterranean-west"] and len(b.drawn) > before
    a, c = Position(36.40, -5.002), Position(36.40, -4.998)
    assert w.chart.region_at(a) == "strait" and w.chart.region_at(c) == "mediterranean-west"
    assert abs(w.chart.depth_at(a) - w.chart.depth_at(c)) < 6.0


def test_truth_7_291_the_seam_between_the_blocks_two_regions_is_crossed_likewise():
    """The brief's item 9 and the lead's ruling: the block is two regions abutting at 0.05 E;
    a ship crossing it before a westerly takes the business with her from one into the
    other, which peoples the Balearics' water once (the grain from Algiers for the islands),
    and the depth does not step."""
    from freesail.world.geo import Position

    w = _med_at(
        37.00,
        -0.03,
        datetime(1805, 6, 14, 10, 0),
        ship=SCHOONER,
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        ship_heading_deg=90.0,
        ship_speed_kn=5.0,
        business="on",
    )
    b = w.business
    assert b.region == "mediterranean-west"
    before = len(b.drawn)
    w.submit("set plain sail")
    w.submit("steer east")
    crossed = None
    for _ in range(12):
        w.run(600)
        if b.region == "balearics":
            crossed = w.clock.tick
            break
    assert crossed is not None and crossed <= 3600, (b.region, w.position)
    assert b.regions_entered == ["mediterranean-west", "balearics"] and len(b.drawn) > before
    a, c = Position(37.0, 0.048), Position(37.0, 0.052)
    assert w.chart.region_at(a) == "mediterranean-west" and w.chart.region_at(c) == "balearics"
    assert abs(w.chart.depth_at(a) - w.chart.depth_at(c)) < 6.0


def test_truth_7_292_by_night_in_1805_palma_shows_porto_pis_light_and_mahon_none():
    """The brief's item 3: off Palma by night in 1805 the lantern of Porto Pí is in sight, lit
    every night at the hour of the Ánimas (Tofiño 1787, p. 185); at the mouth of Port Mahon
    there is no light at all (Purdy 1840: no regular light-tower in the Balearics but
    Palma's), and a ship closing Minorca by night has the land and no light."""
    from freesail.world.geo import Position

    palma = Position(39.50, 2.62)
    w = _med_at(palma.lat_deg, palma.lon_deg, datetime(1805, 6, 15, 23, 30))
    night = datetime(1805, 6, 15, 23, 30)
    lights = {
        s.feature.id
        for s in w.chart.in_sight(palma, 20.0, None, "night", night)
        if s.feature.kind == "light"
    }
    assert lights == {"porto-pi-light"}
    mahon = Position(*MAHON_MOUTH)
    lights = {
        s.feature.id
        for s in w.chart.in_sight(mahon, 20.0, None, "night", night)
        if s.feature.kind == "light"
    }
    assert lights == set()


def test_truth_7_293_the_masters_tide_in_the_block_is_the_pilots_foot_and_malagas_three():
    """The brief's item 5: the master's epitome (Norie's table, a ship of war's) gives
    Málaga high water at XII on the days of full and change and three feet (Purdy 1826,
    p. 12), and every other place of the block a foot (the pilots: Smyth, Tofiño, Bérard),
    not the far gauge's range the world's tide had over the block while its gauges were held
    (since package 89 the gauges' own inches); off Port Mahon his nearest place is Port
    Mahon."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    norie = T.Epitome.load("norie")
    malaga = norie.by_name("Málaga")
    assert (malaga.hw_h, malaga.hw_m, malaga.spring_rise_ft) == (12, 0, 3.0)
    assert not malaga.rise_judgement
    for name in ("Almería", "Cartagena", "Palma", "Ivica", "Port Mahon", "Oran", "Algiers"):
        place = norie.by_name(name)
        assert place.spring_rise_ft == 1.0 and not place.rise_judgement, name
    assert norie.nearest(Position(*MAHON_MOUTH))[0].name == "Port Mahon"
    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    held = {g["id"]: g for g in doc["gauges"] if g.get("block")}
    assert held["malaga"]["mean_level_m"] == 0.43 and held["mahon"]["M2"]["amplitude_m"] < 0.06


def test_truth_7_294_the_frigate_sails_from_gibraltar_to_port_mahon_by_her_short_book():
    """The brief's item 7: the block's scenario (`mahon.yaml`) sailed at seed 7 by its short
    book: from Gibraltar road round Europa Point and east past Cape de Gata, the Hormigas,
    Formentera and Cabrera without touching ground, across the seam at 0.05 E, to the mouth
    of Port Mahon, where she anchors without the ledges within three days and a quarter (at
    11:09 on the 17th at seed 7) and lies through the northerly that comes on that night."""
    from freesail.world.geo import Position, bearing_and_distance
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    root = Path(__file__).resolve().parents[1]
    sf = load_scenario(root / "data" / "scenarios" / "mahon.yaml")
    w = make_scenario_world(sf)
    assert begin(w, sf) >= 10
    regions = set()
    for _ in range(98 * 6):  # to seven in the morning of the 18th, through the northerly
        w.run(600)
        regions.add(w.chart.region_at(w.position))
    assert not [e for e in w.log if e.kind == "ship.aground"]
    anchored = [e for e in w.log if e.kind == "ship.anchored"]
    assert len(anchored) == 2  # Gibraltar road at the start, the mouth of Port Mahon
    assert anchored[1].tick <= 80 * 3600
    assert {"strait", "mediterranean-west", "balearics"} <= regions
    _, off = bearing_and_distance(w.position, Position(*MAHON_MOUTH))
    assert off < 0.6 * units.NAUTICAL_MILE
    assert not [e for e in w.log if "drag" in e.kind]


# ---------------------------------------------------------------------------
# Package 79d: the Gulf of Lion and the Tyrrhenian (truths 7-295 to 7-304); the Gulf's
# five (7-295 to 7-299) over the regions `gulf-of-lion` and `ligurian-sea`
# ---------------------------------------------------------------------------

GULF_PORTS = ["toulon", "marseille", "hyeres", "villefranche"]
HYERES_ROAD = (43.0950, 6.2150)  # features/gulf-of-lion.yaml's `hyeres-road`


def _gulf_at(lat: float, lon: float, when: datetime, ship: str = FRIGATE, **kw):
    """A world on the whole chart in the Gulf of Lion at seed 7, the Gulf's ports loaded, a
    steady breeze (from the north-west, the mistral's quarter, unless given)."""
    sc = Scenario(
        start_time=when,
        wind_from_deg=kw.pop("wind_from_deg", 315.0),
        wind_speed_kn=kw.pop("wind_speed_kn", 12.0),
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        chart="atlantic-east",
        ports=kw.pop("ports", GULF_PORTS),
        nation=kw.pop("nation", "britain"),
        **kw,
    )
    return make_world(SEED, ship, sc)


def test_truth_7_295_the_gulfs_winter_row_blows_its_gales_from_the_north_west():
    """The brief's truth (79d): the mistral. The Gulf has a weather box of its own, whose
    check is Marseille's table (the Admiralty's Mediterranean Pilot, vol. II, 1916, p. 462:
    the north-west the commonest wind of every winter month); a position in the Gulf takes
    it, not the nearest Atlantic box. Over Januaries drawn from its row the strong
    winds (22 knots and more) blow most often from the north-west, and two hours in three
    from west to north, the mistral and the tramontane; the summer row has a tenth of the
    winter's strong hours."""
    import hashlib
    import random

    from freesail.world import weather as W

    clim = W.load_climatology()
    box = clim.box_at(43.0, 5.0)
    assert box.name == "gulf-of-lion" and clim.box_at(43.7, 7.3).name == "gulf-of-lion"
    raw = yaml.safe_load(W.CLIMATOLOGY_PATH.read_text(encoding="utf-8"))
    note = raw["boxes"]["gulf-of-lion"]["months"][1]["note"]
    assert "Marseille" in note and "NW 10" in note  # the table's commonest winter wind

    def strong_hours(month: int, months: int = 36) -> dict[str, int]:
        points = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
        counts = dict.fromkeys(points, 0)
        for serial in range(months):
            digest = hashlib.sha256(f"7:weather:{serial}".encode()).digest()
            stream = random.Random(int.from_bytes(digest[:8], "big"))
            weather = W.Weather(
                datetime(1805, month, 1), stream, seed=7000 + serial, climatology=clim, box=box
            )
            t = datetime(1805, month, 1)
            for _ in range(24 * 28):
                weather.advance(t)
                d, s = weather.surface_wind_at(0.0, 0.0, t)
                if units.ms_to_knots(s) >= 22.0:
                    counts[points[int(((math.degrees(d) + 22.5) % 360.0) // 45.0)]] += 1
                t += timedelta(hours=1)
        return counts

    winter = strong_hours(1)
    total = sum(winter.values())
    assert total > 0 and max(winter, key=winter.get) == "NW", winter
    assert (winter["W"] + winter["NW"] + winter["N"]) / total > 0.6, winter
    summer = strong_hours(7)
    assert sum(summer.values()) < 0.1 * total, (summer, total)


def test_truth_7_296_toulons_roads_are_seen_from_the_road_of_hyeres_and_its_lights_are_later():
    """The brief's truth (79d): at anchor in the Road of Hyeres, the fleet's shelter in the
    watch on Toulon (Purdy 1826, p. 58; James vol. 3, p. 177), her masthead has in sight by
    day the marks of Toulon's roads, Cape Cepet, the Great Tower, Mount Faron and Mount
    Coudon, and Cape Sicie's chapel beyond, three to five leagues off; the islands' marks
    her lookout calls first. By night in 1805 no light shows: Porquerolles', the Titan's and
    Camarat's are of the 1830s and are seen in 1840."""
    w = _gulf_at(*HYERES_ROAD, datetime(1805, 1, 15, 12, 0))
    from freesail.world.geo import Position

    road = Position(*HYERES_ROAD)
    assert w.chart.region_at(road) == "gulf-of-lion" and w.chart.level_at(road) == 3
    w.run(300)
    seen = set(_sighted(w))
    assert {"porquerolles", "bregancon"} & seen, seen
    eye = 20.0  # her masthead
    in_sight = {
        s.feature.id: s.distance_m / units.NAUTICAL_MILE
        for s in w.chart.in_sight(road, eye, None, "day", datetime(1805, 1, 15, 12, 5))
    }
    for mark in ("cape-cepet", "grosse-tour", "mount-faron", "mount-coudon", "notre-dame-du-mai"):
        assert mark in in_sight and 9.0 < in_sight[mark] < 17.0, (mark, in_sight.get(mark))
    lights = ("porquerolles-light", "titan-light", "camarat-light")
    by_night_1805 = {
        s.feature.id for s in w.chart.in_sight(road, eye, None, "night", datetime(1805, 1, 15, 23))
    }
    assert not by_night_1805 & set(lights)
    by_night_1840 = {
        s.feature.id for s in w.chart.in_sight(road, eye, None, "night", datetime(1840, 1, 15, 23))
    }
    assert set(lights) <= by_night_1840


LIGURIAN_PORTS = [
    "genoa",
    "leghorn",
    "porto-ferrajo",
    "bastia",
    "ajaccio",
    "san-fiorenzo",
    "maddalena",
]
AGINCOURT_SOUND = (41.1870, 9.3790)  # features/ligurian-sea.yaml's `agincourt-sound`


def test_truth_7_297_agincourt_sound_holds_a_fleet_in_a_north_wester():
    """The brief's truth (79d): Agincourt Sound, where Nelson's squadron anchored on 31
    October 1803 (James vol. 3, p. 177), 'land-locked' (Purdy 1826, p. 89): from the berth
    the land lies within two miles in every quarter but the north-east's channel; there is
    water of eight to thirty metres over some three square kilometres about it, room for a
    fleet's berths; and the frigate, brought up by the best bower in twelve fathoms on weed
    in a north-westerly of thirty knots (the north-wester 'blows with great violence'), lies
    six hours without dragging once brought up."""
    from freesail.world.geo import Position, bearing_and_distance, destination

    w = _gulf_at(
        *AGINCOURT_SOUND,
        datetime(1805, 1, 15, 8, 0),
        wind_from_deg=315.0,
        wind_speed_kn=30.0,
        ship_heading_deg=315.0,
        ports=LIGURIAN_PORTS,
    )
    berth = Position(*AGINCOURT_SOUND)
    assert w.chart.region_at(berth) == "ligurian-sea" and w.chart.level_at(berth) == 3
    assert "weed" in w.chart.bottom_near(berth)
    for bearing in (0, 90, 135, 180, 225, 270, 315):
        to_land = next(
            (
                k * 50.0
                for k in range(1, 90)
                if w.chart.depth_at(destination(berth, bearing, k * 50.0)) < 0.0
            ),
            None,
        )
        assert to_land is not None and to_land < 4000.0, (bearing, to_land)
    room = sum(
        1
        for i in range(-10, 11)
        for j in range(-10, 11)
        if 8.0
        <= (w.chart.depth_at(Position(41.1870 + 0.0015 * i, 9.3790 + 0.002 * j)) or -1.0)
        <= 30.0
    )
    assert room >= 120, room  # of 441 points over 3.5 by 3.4 km
    w.submit("let go the best bower")
    w.run(1200)
    brought = [e for e in w.log if e.kind == "ship.brought_up"]
    assert brought
    since = len(w.log)
    at = w.position
    w.run(6 * 3600)
    assert not [e for e in w.log[since:] if "drag" in e.kind or "aground" in e.kind]
    assert bearing_and_distance(at, w.position)[1] < 0.2 * units.NAUTICAL_MILE
    assert w.ports.ports["maddalena"].anchorage.feature_id == "agincourt-sound"


def test_truth_7_298_the_strait_of_bonifacio_is_entered_on_its_marks_and_sets_her_east():
    """The brief's truth (79d): at the strait's west mouth by day her masthead has the
    strait's marks in sight, Bonifacio on its cliff and Cape Pertusato on the north, Capo
    Testa and the tower of Longo Sardo on the south, the Maddalena's islands beyond, and
    Corsica's mountains thirty to sixty miles off; by night in 1805 no light (Pertusato's is
    of the 1840s, the Derrotero 1849's). Within the strait the world's water sets her east
    (after the north-westerlies, the Admiralty 1916, p. 13) and the master's directions
    name the set."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    mouth = Position(41.37, 8.95)
    w = _gulf_at(mouth.lat_deg, mouth.lon_deg, datetime(1805, 1, 15, 12, 0), ports=LIGURIAN_PORTS)
    in_sight = {
        s.feature.id: s.distance_m / units.NAUTICAL_MILE
        for s in w.chart.in_sight(mouth, 20.0, None, "day", datetime(1805, 1, 15, 12, 5))
    }
    for mark in ("bonifacio", "cape-pertusato", "capo-testa", "longo-sardo-tower"):
        assert mark in in_sight and in_sight[mark] < 15.0, (mark, in_sight.get(mark))
    assert {"maddalena-island", "monte-cinto"} <= set(in_sight)
    night = lambda year: {  # noqa: E731
        s.feature.id
        for s in w.chart.in_sight(mouth, 20.0, None, "night", datetime(year, 1, 15, 23))
    }
    assert "pertusato-light" not in night(1805) and "pertusato-light" in night(1850)
    inside = Position(41.33, 9.25)
    state = T.load_tide().at(inside, datetime(1805, 1, 15, 12))
    assert state.area_id == "bonifacio-strait"
    assert state.stream_east_ms > 0.0 and abs(state.stream_north_ms) < 1e-6
    said = T.load_directions().area_at(inside)
    assert said.id == "bonifacio-strait" and (said.current_point, said.current_kn) == ("E", 0.5)


def test_truth_7_299_genoa_is_neutral_before_the_annexation_of_june_1805_and_hostile_after():
    """The brief's truth (79d): Genoa, 'as much France as Toulon' (James vol. 3, p. 176), is
    the Ligurian Republic's in the table until the annexation of 4 June 1805 and France's
    after it (its file's dated nation): a King's ship in Genoa road in May 1805 finds the
    port neutral and in July hostile; an American neutral in both; a French ship neutral and
    then open; Leghorn, Etruria's, neutral to her throughout."""
    road = (44.3880, 8.9150)  # features/ligurian-sea.yaml's `genoa-road`
    for when, british, french in (
        (datetime(1805, 5, 20, 12), "neutral", "neutral"),
        (datetime(1805, 7, 20, 12), "hostile", "open"),
    ):
        w = _gulf_at(*road, when, ports=LIGURIAN_PORTS)
        assert w.dealings.stance(w.ports.ports["genoa"]) == british
        assert w.dealings.stance(w.ports.ports["leghorn"]) == "neutral"
        f = _gulf_at(*road, when, ship=SCHOONER, nation="france", ports=LIGURIAN_PORTS)
        assert f.dealings.stance(f.ports.ports["genoa"]) == french
        a = _gulf_at(*road, when, ship=SCHOONER, nation="united-states", ports=LIGURIAN_PORTS)
        assert a.dealings.stance(a.ports.ports["genoa"]) == "neutral"


# The Tyrrhenian's five (7-300 to 7-304), the region `tyrrhenian`
TYRRHENIAN_PORTS = ["cagliari", "alghero", "civita-vecchia", "gaeta", "naples"]
NAPLES_ROAD = (40.8289, 14.2638)  # features/tyrrhenian.yaml's `naples-road`


def test_truth_7_300_the_bay_of_naples_marks_are_seen_from_its_road_and_the_lantern_by_night():
    """The brief's truth (79d): in the road of Naples, the patch's level 3 on mud and clay
    (Purdy 1826, p. 110), her masthead has the bay's marks in sight: the lantern on the mole,
    the Castle dell'Ovo and St Elmo close by, Posilipo and Vesuvius within eight miles,
    Capri, Ischia and Monte Epomeo at their sixteen or seventeen; by night in 1805 the
    lantern on the mole is lit (Michelot 1709's survey of 1701 found it so)."""
    from freesail.world.geo import Position

    road = Position(*NAPLES_ROAD)
    w = _gulf_at(*NAPLES_ROAD, datetime(1805, 6, 12, 12, 0), ports=TYRRHENIAN_PORTS)
    assert w.chart.region_at(road) == "tyrrhenian" and w.chart.level_at(road) == 3
    assert "mud" in w.chart.bottom_near(road)
    in_sight = {
        s.feature.id: s.distance_m / units.NAUTICAL_MILE
        for s in w.chart.in_sight(road, 20.0, None, "day", datetime(1805, 6, 12, 12, 5))
    }
    for mark, within in (
        ("naples-lanterna", 1.0),
        ("castel-dell-ovo", 1.0),
        ("sant-elmo", 2.0),
        ("posillipo-point", 3.0),
        ("vesuvius", 8.0),
        ("capri", 18.0),
        ("ischia", 18.0),
        ("monte-epomeo", 18.0),
    ):
        assert mark in in_sight and in_sight[mark] < within, (mark, in_sight.get(mark))
    lit = {
        s.feature.id
        for s in w.chart.in_sight(road, 20.0, None, "night", datetime(1805, 6, 12, 23, 0))
    }
    assert "naples-lanterna" in lit


def test_truth_7_301_cagliari_receives_a_kings_ship_as_the_king_of_sardinias_neutral_port():
    """The brief's truth (79d): Cagliari, the King of Sardinia's at peace with Britain and
    France, is neutral to a King's ship, to a French ship and to an American and open to a
    Sardinian; so are the Maddalena, and the Pope's and the King of Naples' ports to the
    King's ship; the town's water is scarce, sold at the doors, and the fleets send to Pula
    for it (Smyth 1828, p. 206): the port's own words say so."""
    road = (39.1937, 9.1035)  # `cagliari-road`
    ports = TYRRHENIAN_PORTS + ["maddalena"]
    when = datetime(1805, 3, 1, 12)
    w = _gulf_at(*road, when, ports=ports)
    assert {pid: w.dealings.stance(w.ports.ports[pid]) for pid in ports} == dict.fromkeys(
        ports, "neutral"
    )
    for nation, stance in (
        ("france", "neutral"),
        ("united-states", "neutral"),
        ("sardinia", "open"),
    ):
        o = _gulf_at(*road, when, ship=SCHOONER, nation=nation, ports=["cagliari"])
        assert o.dealings.stance(o.ports.ports["cagliari"]) == stance, nation
    cagliari = w.ports.ports["cagliari"]
    assert cagliari.anchorage.feature_id == "cagliari-road" and cagliari.nation == "sardinia"
    assert "Pula" in cagliari.dockyard.items["water"].note
    assert "Pula" in cagliari.pilot.words["tide"]


def test_truth_7_302_a_passage_crosses_the_seam_at_40_99_n_with_the_business_carried():
    """The brief's truth (79d; truth 7-274's kind): the schooner east of Sardinia, south of
    the row edge 40.99 N that bounds the Tyrrhenian's tiles from the Ligurian sea's, before a
    southerly, crosses from `tyrrhenian` into `ligurian-sea` within the hour; the business
    follows her and peoples the new region once, and the depth does not step across the
    seam (the two regions' tiles cut from the one grid)."""
    from freesail.world.geo import Position

    w = _gulf_at(
        40.93,
        9.80,
        datetime(1805, 6, 12, 10, 0),
        ship=SCHOONER,
        wind_from_deg=180.0,
        wind_speed_kn=14.0,
        ship_heading_deg=0.0,
        ship_speed_kn=5.0,
        business="on",
        ports=TYRRHENIAN_PORTS + LIGURIAN_PORTS,
    )
    b = w.business
    assert b.region == "tyrrhenian" and b.regions_entered == ["tyrrhenian"]
    before = len(b.drawn)
    w.submit("set plain sail")
    w.submit("steer north")
    crossed = None
    for _ in range(12):
        w.run(600)
        if b.region == "ligurian-sea":
            crossed = w.clock.tick
            break
    assert crossed is not None and crossed <= 3600, (b.region, w.position)
    assert b.regions_entered == ["tyrrhenian", "ligurian-sea"] and len(b.drawn) > before
    south, north = Position(40.9864, 9.80), Position(40.9869, 9.80)  # either side of the row edge
    assert w.chart.region_at(Position(41.001, 9.80)) == "ligurian-sea"
    assert w.chart.region_at(south) == "tyrrhenian"
    assert abs(w.chart.depth_at(south) - w.chart.depth_at(north)) < 2.0


def test_truth_7_303_an_islet_the_grid_lacks_grounds_a_ship_though_the_tiles_read_deep_water():
    """The build's finding (79d): EMODnet's sixteenth of a minute reads water over islets of
    some hundreds of metres (Li Galli off the Sorrento shore read forty metres), so the
    block gives each as a rock of its height and extent (ChartBlocks.md, "An isle the grid
    lacks"): a frigate's keel over Li Galli touches it though the tile there is deep, and a
    mile off she is clear. Since package 94 the three rocky islets are an island the grid
    lacks (`grid_lacks`, by Purdy's and Norie's words), ground to the keel as the rock was."""
    import math as _m

    from freesail.world.geo import destination

    w = _gulf_at(40.60, 14.40, datetime(1805, 6, 12, 12, 0), ports=TYRRHENIAN_PORTS)
    galli = w.chart.feature("li-galli")
    assert galli.kind == "island" and galli.grid_lacks and galli.extent_m >= 300.0
    assert w.chart.depth_at(galli.position) > 20.0  # the grid's water
    hit = w.chart.danger_under(galli.position, _m.radians(90.0), 45.0, 5.0)
    assert hit is not None
    clear = destination(galli.position, 225.0, units.NAUTICAL_MILE)
    assert w.chart.danger_under(clear, _m.radians(90.0), 45.0, 5.0) is None


def test_truth_7_304_the_tyrrhenians_tide_hour_is_smyths_and_its_weather_naples_table():
    """The brief's records (79d): the master's epitome in the road of Naples names Naples'
    own tide-hour (Smyth 1854, p. 178: 11h 20m, with his doubt), the nearest place of his
    table, as off Toulon it names Toulon's (3h 30m); a position in the Tyrrhenian takes the
    Tyrrhenian's weather box, whose rows' check is Naples' table with its gale days."""
    from freesail.world import weather as W

    for road, name in ((NAPLES_ROAD, "Naples"), ((43.0935, 5.9330), "Toulon")):
        w = _gulf_at(*road, datetime(1805, 6, 12, 12, 0), ports=TYRRHENIAN_PORTS)
        words = w.navigation.tide_by_almanac()["words"]
        assert name in words and "may differ by hours" not in words, words
    clim = W.load_climatology()
    assert clim.box_at(40.8, 14.2).name == "tyrrhenian"
    assert (
        clim.box_at(39.2, 9.1).name == "tyrrhenian"
        and clim.box_at(43.0, 6.0).name == "gulf-of-lion"
    )
    raw = yaml.safe_load(W.CLIMATOLOGY_PATH.read_text(encoding="utf-8"))
    note = raw["boxes"]["tyrrhenian"]["months"][1]["note"]
    assert "Naples" in note and "gales 7" in note


# ---------------------------------------------------------------------------
# Package 93: the blocks' tiles rebuilt on their true water (truths 7-305 to 7-309)
# ---------------------------------------------------------------------------


def _chart_tool():
    """`tools/build_charts.py` as a module (its `mean_level_grid`, the fill's raise)."""
    import importlib.util

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "build_charts", root / "tools" / "build_charts.py"
    )
    tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = tool
    spec.loader.exec_module(tool)
    return tool


def _eleven_tide():
    """The world's tide with the eleven alone, as it was before package 89."""
    from freesail.world import tide as T

    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    return T.Tide({**doc, "gauges": [g for g in doc["gauges"] if "block" not in g]}, {"areas": []})


def _grid_at(grid, lat: float, lon: float) -> float:
    """The raise at a position: the value of the fill grid's cell that holds it, worked at
    the cell's centre (`_grid_centre`)."""
    return float(
        grid.values[int((lat - grid.south) / grid.cell), int((lon - grid.west) / grid.cell)]
    )


def _grid_centre(grid, lat: float, lon: float):
    """The centre of the fill grid's cell that holds a position, where its raise is worked."""
    from freesail.world.geo import Position

    r = int((lat - grid.south) / grid.cell)
    c = int((lon - grid.west) / grid.cell)
    return Position(grid.south + (r + 0.5) * grid.cell, grid.west + (c + 0.5) * grid.cell)


def _hws(tide, pos) -> float:
    """The world's high water springs at a position: the mean level and M2 and S2."""
    level, consts = tide.constants_at(pos)
    return level + consts["M2"][0] + consts["S2"][0]


def test_truth_7_305_the_channel_easts_low_shore_against_its_own_high_water():
    """The brief's truth (93), the lead's wording amended at the measurement (the ruling of
    2026-10-30): on the rebuilt tiles the Somme's banks and Dungeness's shingle foreland
    stand above the world's high water springs; the raise at Romney Marsh is the block's
    mean level, the eleven's and 0.35 m more at the grid's cell, to the centimetre; and
    Romney Marsh and the Pevensey Levels lie below high water springs on the tiles, as they
    lie behind the
    Dymchurch Wall and the Pevensey sea walls in truth: dyked levels, which GEBCO's fifteen
    seconds cannot hold (a finding, for a land patch when a sheet with its datum is read;
    the medians were 1.3 and 1.7 m under on the old tiles, 1.0 and 1.2 now)."""
    import numpy as np

    from freesail.world.chart import load_chart
    from freesail.world.geo import Position
    from freesail.world.tide import load_tide

    chart, tide, eleven = load_chart("atlantic-east"), load_tide(), _eleven_tide()

    def over(s, n, w, e):
        rows = []
        for la in np.linspace(s, n, 25):
            for lo in np.linspace(w, e, 25):
                p = Position(float(la), float(lo))
                z = chart.elevation_at(p)
                if z is not None and z > 0.0:
                    rows.append(z - _hws(tide, p))
        return np.array(rows)

    somme = over(50.15, 50.25, 1.55, 1.68)
    assert np.median(somme) > 1.0 and (somme > 0.0).mean() > 2 / 3, np.median(somme)
    # the ness's shingle point, Dungeness's light upon it (50.915 N, 0.93 to 0.97 E)
    for lon in (0.93, 0.94, 0.95, 0.96, 0.97):
        p = Position(50.915, lon)
        assert chart.elevation_at(p) > _hws(tide, p), lon
    romney = Position(50.99, 0.88)
    grid = _chart_tool().mean_level_grid({"south": 50.9, "north": 51.1, "west": 0.8, "east": 1.0})
    raised = _grid_at(grid, romney.lat_deg, romney.lon_deg)
    centre = _grid_centre(grid, romney.lat_deg, romney.lon_deg)
    assert raised == pytest.approx(tide.constants_at(centre)[0], abs=0.01)
    assert raised - eleven.constants_at(centre)[0] == pytest.approx(0.35, abs=0.01)
    for box in ((50.95, 51.03, 0.78, 0.98), (50.80, 50.85, 0.28, 0.38)):  # Romney, Pevensey
        assert np.median(over(*box)) < -0.5


def test_truth_7_306_mahons_and_naples_quays_stand_their_height_above_their_own_water():
    """The brief's truth (93): Port Mahon's fill is raised by Mahón's own water (0.20 m above
    the datum, the gauge's; Saint-Malo's 6.83 before), so the town on its cliff stands its
    own height above the harbour: of the points within 600 m of the quay, 210 and more are
    land, their median height above the mean level between 15 and 35 m, and every land
    point but two above high water springs. Naples' gauges' levels are unread, so its water
    is the eleven's (3.70 m) and the raise is too, as the rule gives it and the tiles were
    built: the quay's ground the same height above the same water, unmoved."""
    import numpy as np

    from freesail.world.chart import load_chart
    from freesail.world.geo import Position, destination
    from freesail.world.tide import load_tide

    chart, tide, eleven = load_chart("atlantic-east"), load_tide(), _eleven_tide()
    tool = _chart_tool()
    for name, quay, own in (
        ("mahon", Position(39.8885, 4.2640), 0.20),
        ("naples", Position(40.8380, 14.2530), None),
    ):
        level = tide.constants_at(quay)[0]
        if own is not None:
            assert level == pytest.approx(own, abs=0.01)
        else:
            assert level == pytest.approx(eleven.constants_at(quay)[0], abs=1e-6)
        grid = tool.mean_level_grid(
            {
                "south": quay.lat_deg - 0.1,
                "north": quay.lat_deg + 0.1,
                "west": quay.lon_deg - 0.1,
                "east": quay.lon_deg + 0.1,
            }
        )
        centre = _grid_centre(grid, quay.lat_deg, quay.lon_deg)
        assert _grid_at(grid, quay.lat_deg, quay.lon_deg) == pytest.approx(
            tide.constants_at(centre)[0], abs=0.01
        )
        land = []
        for r in range(50, 601, 50):
            for b in range(0, 360, 15):
                q = destination(quay, float(b), float(r))
                z = chart.elevation_at(q)
                if z is not None and z > 0.0:
                    land.append((z - level, z > _hws(tide, q)))
        heights = np.array([h for h, _ in land])
        if name == "mahon":
            assert len(land) >= 210, len(land)
            assert 15.0 < float(np.median(heights)) < 35.0
            assert sum(not above for _, above in land) <= 2
        else:
            assert len(land) >= 270 and 10.0 < float(np.median(heights)) < 30.0


def test_truth_7_307_a_bay_and_a_harbour_cover_and_dry_by_their_own_blocks_tide():
    """The brief's truth (93): the sands of the bay of the Somme cover and dry by the Channel
    east's own tide on a day of springs (low water about 2 m and high about 7.3 m above the
    datum there), and of the bay's points some 190 stand between the block's low and high
    water and above the eleven's high water (4.5 m): they cover on the block's tide and
    would never cover on the eleven's. Port Mahon's inner harbour, which GEBCO's fill under
    Saint-Malo's raise stood three metres above the datum, is water at every hour of the day
    by Mahón's own tide, three metres and more of it."""
    import numpy as np

    from freesail.world.chart import load_chart
    from freesail.world.geo import Position
    from freesail.world.tide import load_tide

    chart, tide, eleven = load_chart("atlantic-east"), load_tide(), _eleven_tide()
    day = datetime(1805, 6, 12)
    hours = [day + timedelta(minutes=10 * i) for i in range(145)]
    bay = Position(50.21, 1.58)
    own = [tide.height_at(bay, t) for t in hours]
    far = [eleven.height_at(bay, t) for t in hours]
    assert min(own) < 2.5 and max(own) > 7.0 and max(far) < 5.0
    between = 0
    for la in np.arange(50.17, 50.26, 0.004):
        for lo in np.arange(1.50, 1.66, 0.004):
            z = chart.elevation_at(Position(float(la), float(lo)))
            if z is not None and min(own) < z < max(own) and z > max(far):
                between += 1
    assert between >= 150, between
    inner = Position(39.8850, 4.2900)
    assert chart.region_at(inner) == "balearics" and chart.level_at(inner) == 3
    assert chart.depth_at(inner) > 3.0
    assert all(chart.depth_at(inner) + tide.height_at(inner, t) > 3.0 for t in hours)


def test_truth_7_308_the_raise_outside_every_block_is_unchanged_to_the_centimetre():
    """The brief's truth (93): outside every block the fill's raise is the eleven's alone, as
    every tile there was built by (the Channel west, the Western Approaches, the ocean west
    of Portugal's 10 W), to the centimetre and in fact to the bit; and channel-west's
    recipe still has no raise and channel-mid's tiles are not rebuilt (the manifest's
    entries say so)."""
    from freesail.world.geo import Position
    from freesail.world.tide import load_tide

    tool, tide, eleven = _chart_tool(), load_tide(), _eleven_tide()
    for box in (
        {"south": 49.0, "north": 50.6, "west": -7.0, "east": -4.0},  # channel-west
        {"south": 38.0, "north": 40.0, "west": -12.5, "east": -10.5},  # off Portugal
        {"south": 46.5, "north": 47.5, "west": -8.0, "east": -6.0},  # the Bay's mouth
    ):
        grid = tool.mean_level_grid(box)
        rows, cols = grid.values.shape
        for r in range(0, rows, 3):
            for c in range(0, cols, 3):
                p = Position(grid.south + (r + 0.5) * grid.cell, grid.west + (c + 0.5) * grid.cell)
                if tide.blocks_at(p):
                    continue
                assert float(grid.values[r, c]) == pytest.approx(
                    eleven.constants_at(p)[0], abs=0.005
                )
    assert not tool.REGIONS["channel-west"].get("fill_to_chart_datum")
    manifest = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / "data/charts/manifest.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert "fill_to_chart_datum" not in manifest["regions"]["channel-west"]


def test_truth_7_309_the_strait_and_the_islands_raise_as_the_rule_gives_them():
    """The brief's truth (93): over the Strait, Madeira and the Azores the gauges' levels are
    unread, so the world's level and the raise are the eleven's there (Le Conquet's 3.98 m
    over the Strait and Madeira), as the tiles were built and not rebuilt (Madeira's and the
    Azores'); the Strait's tile column east of 5 W lies in the Mediterranean west's bounds
    and takes that block's water, 0.37 to 0.43 m; Agincourt Sound's patch keeps the eleven's
    raise until a sheet is read (`fill_raise: eleven`, the lead's ruling on 7-297)."""
    from freesail.world.geo import Position
    from freesail.world.tide import load_tide

    tool, tide, eleven = _chart_tool(), load_tide(), _eleven_tide()
    for block, (lat, lon) in (
        ("strait", (36.0, -5.6)),
        ("madeira", (32.65, -16.9)),
        ("azores", (38.65, -27.2)),
    ):
        p = Position(lat, lon)
        assert block in tide.blocks_at(p) or block in ("madeira", "azores")
        grid = tool.mean_level_grid(
            {"south": lat - 0.1, "north": lat + 0.1, "west": lon - 0.1, "east": lon + 0.1}
        )
        centre = _grid_centre(grid, lat, lon)
        assert _grid_at(grid, lat, lon) == pytest.approx(eleven.constants_at(centre)[0], abs=0.01)
        assert _grid_at(grid, lat, lon) == pytest.approx(tide.constants_at(centre)[0], abs=0.01)
    assert eleven.constants_at(Position(36.0, -5.6))[0] == pytest.approx(3.98, abs=0.01)
    east = tool.mean_level_grid({"south": 35.9, "north": 36.2, "west": -4.95, "east": -4.7})
    assert 0.3 < float(east.values.min()) <= float(east.values.max()) < 0.5
    sound = tool.REGIONS["ligurian-sea"]["harbours"]["agincourt-sound"]
    assert sound["fill_raise"] == "eleven"
    berth = Position(41.1870, 9.3790)
    assert eleven.constants_at(berth)[0] - tide.constants_at(berth)[0] > 6.0


# Package 94: the chart's tidies from 79c, 79d and 89 (truths 7-310 to 7-314)
# ---------------------------------------------------------------------------


def test_truth_7_310_the_isla_del_rey_is_an_island_to_the_lookout_and_ground_to_the_keel():
    """79c's finding: the Isla del Rey, which the grid smooths into a ridge of nine to
    eleven metres in Port Mahon, was given as a rock of its height so that nothing sails
    through it, and the lookout called it "a danger". As an island the grid lacks (package
    94) the lookout makes it out as the land it is and calls it by its name, by day and by
    night close aboard, never "a danger"; the keel touches it within its extent as she
    touched the rock, and a cable and a half south of it, in Tofiño's passage, she is clear;
    the pilot names it ahead on her line, and the master's chart names it among the
    dangers."""
    import math as _m

    from freesail.world.chart import DANGER_KINDS
    from freesail.world.geo import destination
    from freesail.world.lookout import Lookout

    when = datetime(1805, 6, 15, 12, 0)
    w = _med_at(*MAHON_MOUTH, when)
    rey = w.chart.feature("isla-del-rey")
    assert rey.kind == "island" and rey.grid_lacks and rey.kind not in DANGER_KINDS
    assert w.chart.depth_at(rey.position) > 5.0  # the grid's ridge, water
    # the lookout: land, by its name, not a danger
    near = destination(rey.position, 270.0, 2.0 * units.CABLE)
    for daylight in ("day", "night"):
        seen = {s.feature.id: s for s in w.chart.in_sight(near, 10.0, None, daylight, when)}
        assert "isla-del-rey" in seen and seen["isla-del-rey"].seen_as == "land", daylight
    found = w.chart.in_sight(near, 10.0, None, "day", when)
    words = Lookout.words(next(s for s in found if s.feature is rey), 0.0)
    assert words.startswith("The Isla del Rey") and "danger" not in words
    # standing for it from two cables west, the tiles' water clear, the lookout has it
    # ahead by its extent
    assert w.chart.depth_at(near) > 5.0
    hit = Lookout(w.chart)._first_ahead(near, _m.radians(90.0), 600.0, 0.5, found)
    assert hit is not None and hit[2] is not None and hit[2].feature is rey
    # the keel
    hit = w.chart.danger_under(rey.position, _m.radians(270.0), 45.0, 5.0)
    assert hit is not None and hit.bottom == "the Isla del Rey, or Hospital Island (island)"
    south = destination(rey.position, 200.0, 1.5 * units.CABLE)
    assert w.chart.danger_under(south, _m.radians(270.0), 45.0, 5.0) is None
    # the pilot's line and the master's chart
    ahead = w.chart.dangers_ahead(near, 90.0, 1500.0, units.CABLE, 0.5, 6.0)
    assert ahead and ahead[0][0].id == "isla-del-rey"
    assert "isla-del-rey" in {f.id for f, _b, _d in w.chart.dangers_near(near, 2000.0)}


def test_truth_7_311_a_roads_bottom_is_in_the_leads_note_as_an_anchorages_is():
    """79d's finding: `Chart.bottom_near` read the note of the ground from `anchorage` and
    `bottom` features alone, so a `road` with its `bottom:` gave none, and 79d gave its
    roads as anchorages. Since package 94 a road's bottom is read as an anchorage's: the
    road of Naples as a `road` gives the arming of the lead and the grounding its mud and
    clay as the anchorage did; a feature of another kind with a `bottom:` gives nothing."""
    from dataclasses import replace

    from freesail.world.chart import Chart, load_manifest
    from freesail.world.reckoning import ground_words

    chart = Chart("tyrrhenian", load_manifest())  # its own, not the shared chart
    road = chart.feature("naples-road")
    assert road.kind == "anchorage" and road.bottom
    near = road.position.advanced(300.0, 300.0)
    assert ground_words(chart, near, 30.0) == road.bottom
    chart.features[road.id] = replace(road, kind="road")
    assert chart.bottom_near(near) == road.bottom
    assert ground_words(chart, near, 30.0) == road.bottom
    chart.features[road.id] = replace(road, kind="town")
    assert chart.bottom_near(near) != road.bottom


def test_truth_7_312_a_cable_either_side_of_1_w_the_tide_is_within_a_tenth_of_a_foot():
    """The brief's item 3: package 89's rule left a step where a block's water meets the
    water the eleven alone serve, 102 degrees of M2 at 1 W off Selsey Bill (a cable either
    side of 1 W the heights four to seven and a half feet apart through a day of springs).
    The block's water now rises from the eleven's alone at its open edge to its own over
    ten miles inside it (`tide.SEAM_BAND_NM`, the smoothstep of the distance's fraction),
    so that a cable inside 1 W the tide is within a tenth of a foot of the tide a cable
    outside, every ten minutes through a day of springs, along the seam from 49.1 to
    50.6 N; the same across the seam at 48 N in the Iroise, where Biscay north meets the
    Channel west. The taper is the cell's: a cell's centre gives its weight, so a cell once
    worked is a lookup as before."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    foot = units.feet_to_m(0.1)
    pairs = []
    # (north of 50.62 N the seam at 1 W is the Solent's tide region's with the Channel
    # east's since package 94's item 4, a seam between two blocks: truth 7-313; with
    # Portsmouth's gauge serving both by the rule of the seams, step 5, its step at
    # 50.9 N is 2.09 ft, 3.0 before the rule, and it stays out)
    for lat in (49.1, 49.5, 50.0, 50.3, 50.6):
        cable = 0.1 / 60.0 / math.cos(math.radians(lat))
        pairs.append((Position(lat, -1.0 + cable), Position(lat, -1.0 - cable)))
    for lon in (-4.7, -4.9):
        pairs.append((Position(48.0 - 0.1 / 60.0, lon), Position(48.0 + 0.1 / 60.0, lon)))
    for inside, outside in pairs:
        assert tide.blocks_at(inside) and not tide.blocks_at(outside)
        assert 0.0 < tide.taper_at(inside) < 0.01
        for m in range(0, 25 * 60, 10):
            when = datetime(1805, 6, 12) + timedelta(minutes=m)
            gap = abs(tide.height_at(inside, when) - tide.height_at(outside, when))
            assert gap < foot, (inside, when, gap)
    assert 0.5 < tide.taper_at(Position(50.6, -1.0 + 0.2)) < 1.0  # 7.6 miles in
    assert tide.taper_at(Position(50.6, -1.0 + 0.3)) == 1.0  # 11.4 miles in: whole


def test_truth_7_313_spithead_has_portsmouths_tide_within_the_hour():
    """The brief's item 4: Bournemouth's and Portsmouth's gauges (39a's, held until package
    94) serve the manifest's tide region `solent` (bounds and no tiles, 50.62 to 51 N and
    2.2 to 1 W), under the seam's taper. The eleven's blend over the Solent was four hours
    and a half wrong (39a's finding again in 89's notes): Spithead's high water by it fell
    at 06:56 and 19:11 on 12 June 1805 where Portsmouth's gauge has 11:33 and 23:49. Now
    Spithead's high waters are within the hour of the gauge's (within five minutes), its
    spring range the gauge's water (twelve feet where the eleven gave nine and a half),
    and a mile west of 1 W at 50.6 N, outside the region, the eleven's to the bit (truth
    7-282). The seam between the Solent's water and the Channel east's at 1 W north of
    50.62 N is a seam between two blocks, a step of three feet and a half off Chichester
    (docs/dev/TuningNotes.md, package 94, for the lead)."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    gauge = next(g for g in doc["gauges"] if g["id"] == "portsmouth")
    # the Solent's own, and the Channel east's by the rule of the seams (step 5)
    assert gauge["block"] == ["solent", "channel-east"]
    assert T.region_bounds()["solent"] == (50.62, 51.0, -2.2, -1.0)
    # the gauge's own tide: Portsmouth alone (a level given for the loader; the hours of
    # high water do not read it)
    alone = {k: v for k, v in gauge.items() if k != "block"} | {"mean_level_m": 4.0}
    own = T.Tide({"constituents": doc["constituents"], "gauges": [alone]}, {"areas": []})
    eleven = _the_eleven_alone()
    spithead = Position(50.775, -1.10)
    assert tide.blocks_at(spithead) == {"solent"} and tide.taper_at(spithead) > 0.95
    start = datetime(1805, 6, 12)
    theirs = [w for w, _ in own.high_waters(Position(gauge["lat_deg"], gauge["lon_deg"]), start)]
    for name, t, within_h in ((None, tide, 1.0), ("the eleven", eleven, None)):
        ours = [w for w, _ in t.high_waters(spithead, start)]
        gaps = [min(abs((a - b).total_seconds()) / 3600.0 for b in theirs) for a in ours]
        if within_h is None:
            assert min(gaps) > 4.0, (name, gaps)  # the old water, four hours and more out
        else:
            assert len(ours) == 2 and max(gaps) < within_h, gaps
            assert max(gaps) < 5.0 / 60.0
    assert _spring_range_ft(tide, spithead) > 11.5 and _spring_range_ft(eleven, spithead) < 10.0
    mile_deg = 1.0 / 60.0 / math.cos(math.radians(50.6))
    west = Position(50.6, -1.0 - mile_deg)
    assert not tide.blocks_at(west)
    assert tide.constants_about(west) == eleven.constants_about(west)


def test_truth_7_314_every_recorded_passages_water_is_the_elevens_outside_the_solent():
    """The brief's item 5: every recorded passage unchanged. The proof is the passages
    themselves, run by node id on a clean worktree of the head and on the final tree,
    identical (docs/dev/TuningNotes.md, package 94); as a behaviour: the recorded passages
    sail the Channel west and its approaches, and over the whole of `channel-west` and of
    `channel-mid` outside the Solent's tide region (and west of 1 W) the tide is the
    eleven's to the bit, a cable from the Solent's west and south bounds as everywhere, the
    taper being the inside of a block's alone; the Solent's water begins at its bounds."""
    import freesail.world.tide as T
    from freesail.world.geo import Position

    tide = T.load_tide()
    eleven = _the_eleven_alone(yaml.safe_load(T.STREAMS_PATH.read_text(encoding="utf-8")))
    cable = 0.1 / 60.0
    places = [Position(50.62 - cable, lon) for lon in (-2.1, -1.6, -1.1)]
    places += [Position(lat, -2.2 - cable / math.cos(math.radians(lat))) for lat in (50.7, 50.9)]
    for lat10 in range(485, 511, 5):
        for lon10 in range(-70, -10, 5):
            places.append(Position(lat10 / 10.0 + 0.003, lon10 / 10.0 + 0.003))
    for pos in places:
        if tide.blocks_at(pos):
            assert tide.blocks_at(pos) == {"solent"}, pos
            continue
        for h in (0, 7, 15):
            when = datetime(1805, 6, 12) + timedelta(hours=h)
            assert tide.at(pos, when) == eleven.at(pos, when), (pos, h)
    inside = Position(50.62 + cable, -1.6)
    assert tide.blocks_at(inside) == {"solent"} and 0.0 < tide.taper_at(inside) < 0.01


# Package 85: the orders, the primer and the library for a model reader
# ---------------------------------------------------------------------------


def _package_85_cutter() -> World:
    from freesail.world.scenarios import load_scenario, make_scenario_world

    here = Path(__file__).resolve().parents[1]
    sf = load_scenario(here / "data" / "scenarios" / "dispatches-falmouth.yaml")
    return make_scenario_world(sf, seed=7)


def test_truth_7_240_the_date_is_told_in_words_in_every_line_and_on_request():
    """The owner's fourth note of the playtests of 70 to 72 (a model deducing the date from
    the log's stamps, and confused): the date is a reading in words, `the date`, and the
    last words of every station's line and the director's, changing with the day and
    riding no sample between."""
    from freesail.api import readings as R

    w = _package_85_cutter()
    assert w.submit("the date").text == "The date: Wednesday 12 June 1805."
    assert R.station_line(w, None).endswith("; Wednesday 12 June 1805.")
    assert R.director_line(w).endswith("; Wednesday 12 June 1805.")
    w.run(19 * 3600 + 1)
    assert w.readings.get("date")["words"] == "Thursday 13 June 1805"


def test_truth_7_241_the_war_is_what_the_ship_knows_and_the_news_is_entered_in_her_papers():
    """The owner's fifth note (a model reasoning the war's state from a primer's pilot
    example): `the war` is the nations' table she sailed with and every change the news
    brought her, each entered in the paper `the news of the war` with where and when it
    came, never the world's table as it stands."""
    w = _package_85_cutter()
    sailed = w.nations.sailed_with_words()
    assert w.submit("the war").text == (
        f"The war: {sailed} No news of the war has reached her since she sailed."
    )
    assert w.nations.make_peace("britain", "spain")
    assert "No news of the war" in w.submit("who is at war").text
    assert w.papers.news_heard("the pilot off Falmouth") == [
        "The news of the war written up by the captain: by the pilot off Falmouth, peace made "
        "between Britain and Spain."
    ]
    said = w.submit("the war").text
    assert "by the pilot off Falmouth: peace made between Britain and Spain." in said
    assert "As she knows it now: Britain at war with the Batavian Republic and France;" in said
    assert "peace made between Britain and Spain" in w.papers.page("the news of the war").lines[-2]


def test_truth_7_242_the_calls_before_a_stand_by_are_answered_with_their_results():
    """The model officer's first point: an order given before the stand-by in the same
    reply ran, and the door told it "not run". The harness keeps the results of the calls
    that ran on the turn (`Reply.ran`), the doors answer them with those, and say "not
    run" only of the calls after the stand-by."""
    from freesail.agents.model import MODEL
    from tests.test_agents import call, point_world, reply, stationed
    from tests.test_local_runner import A_GLASS_S, llama, model_for

    world = point_world()
    h, _fake, _ = stationed(
        world,
        [
            reply(
                "",
                call("journal", note="steady"),
                call("stand_by", until="a glass"),
                call("readings"),
            ),
            "Awake.",
        ],
    )
    assert h.agent.standing_by
    turn = next(t for t in reversed(h.turns) if t.role == MODEL)
    assert [r["name"] for r in turn.content.ran] == ["journal"]
    world.run(A_GLASS_S)
    answers = [x["content"] for x in model_for(llama([])).messages(h.turns) if x["role"] == "tool"]
    assert answers[0] == "Noted in the journal."
    assert answers[1].startswith("Standing by: this ended your turn")
    assert answers[2] == "Not run: a stand-by earlier in the reply ended your turn."


def test_truth_7_243_in_action_a_notable_event_is_a_hit_a_strike_or_a_change_of_state():
    """The model officer's fourth point, with the owner's "the flow of the game through the
    log" as the measure: the firer's minute line is notable when a shot struck her or the
    fire opened, routine when the minute's shot all missed; a shot that struck us is
    notable, urgent when it killed or carried away a spar; at quarters the trimmers' yard by
    yard is routine. So a stand-by on 'a notable event' is not woken by every discharge."""
    w, v, enemy, battery = _two_cutters_at_pistol_shot()
    w.submit("fire as they bear")
    w.run(600)
    fired = [e for e in w.log if e.kind == "action.fired"]
    assert fired and fired[0].severity is Severity.NOTABLE
    assert all(
        e.severity
        is (Severity.NOTABLE if (e.data.get("struck") or e is fired[0]) else Severity.ROUTINE)
        for e in fired
    )
    assert all(
        e.severity in (Severity.NOTABLE, Severity.URGENT)
        for e in enemy.log
        if e.kind == "action.hit"
    )


def test_truth_7_244_every_station_is_told_her_ship_and_the_ship_reading_says_the_same():
    """The owner's word of 2026-10-27: models at a station were almost never told what
    ship they were on. Every station's brief opens its situation with the ship (her name,
    rig and class, service and nation, fit of guns, people's number, who commands, the
    ports of her voyage), and `the ship` reads the same at any time."""
    from freesail.agents import agent, tools
    from freesail.agents.agent import Brief
    from freesail.api import readings as R

    w = _package_85_cutter()
    words = R.ship_words(w)
    assert words.startswith(
        "The ship: Sherbourne, an armed cutter; a merchantman of Britain. Her guns: 6 "
        "12-pounder carronades. Her people: 30 souls by the muster. Commanding: Mr Bowen, "
    )
    assert words.endswith("The ports of her voyage: Falmouth and Plymouth.")
    assert words in w.submit("what ship").text and words in w.submit("the ship").text
    for which in ("watcher", "officer", "master", "lookout", "passenger", "captain"):
        brief = Brief.build(
            getattr(agent, which)(world=w),
            "a play session",
            ["(the log is empty)"],
            {},
            tools.tool_names(),
            ship=words,
        )
        assert next(i.text for i in brief.head if i.name == "situation").startswith(words)


def test_truth_7_245_four_refusals_found_by_the_reading_are_mended():
    """Package 85's reading of the orders: a standing order's name may carry an apostrophe;
    `hail the lugger` names a sail in sight and never a far one, a wreck in sight being no
    sail; `captain: carry on` at the prompt is the player's own hand given back; `gybe the
    mainsail` is answered that the gybe names no sail."""
    from freesail import orders
    from freesail.orders.errors import OrderError
    from tests.test_primer import make_ship

    ship = make_ship("frigate", "plain-sail", "starboard")
    bays = 'standing order "the bay\'s mouth": every glass then trim sails'
    kind, log, _ = orders.handle(ship, bays)
    assert kind == "standing.given" and "'the bay's mouth'" in log
    schooner = make_ship("schooner", "plain-sail", "starboard")
    try:
        orders.handle(schooner, "gybe the mainsail")
    except OrderError as e:
        assert "takes no sail after it" in str(e)
    else:
        raise AssertionError("taken")
    w = _package_85_cutter()
    w.run(900)
    w.submit("steer east")
    w.run(2)
    assert w.captain.aside
    assert w.submit("captain: carry on").kind == "captain.carry_on" and not w.captain.aside


# ---------------------------------------------------------------------------
# Package 88: the captain's pass of M7 (truths 7-340 onward)
# ---------------------------------------------------------------------------


def test_truth_7_340_aback_with_no_way_the_captain_eases_the_after_sail_and_boxes_her_off(
    monkeypatch,
):
    """Package 88, item 1 (package 86's finding, the convoy's stall): the commodore's brig in
    the owner's convoy comes out of a short-handed tack at 1594 with no way on while her book
    shortens sail, her head forty degrees off the wind, every square sail shaking and the
    spanker drawing. With no headway, square sail set and none drawing, no manoeuvre in
    hand, for the doctrine's three minutes (`aback_recover_minutes`, judgement), her rules
    captain recovers her as Luce 1866 ch. XXV has it: the work waiting for hands avasted and
    the spanker taken in at 1800, boxed off at 1980 and boxed off by 2110, the spanker set
    again and the leg shaped when she has way (2160); at 2400 she makes four knots. With
    the law's switch off (`captains.ABACK_RECOVER`) she lies so until the book's second
    shortening takes in her spanker at 2671 (86's record): at 2400 still no way, no box-off."""
    from freesail.world import captains as C

    w = _scenario_world(CONVOY_SIX)
    w.run(2400)
    said = [e for e in w.log if e.kind == "order.accepted" and "aback with no way on" in e.text]
    assert [e.tick for e in said if "taking in the spanker" in e.text] == [1800], said
    assert [e.tick for e in said if "boxing her off" in e.text] == [1980], said
    assert [e.tick for e in w.log if e.kind == "ship.boxed_off"] == [2110]
    assert any(e.tick == 2160 and "setting the spanker" in e.text for e in w.log)
    assert units.ms_to_knots(w.ship.dyn.u) >= 3.0, w.ship.dyn.u
    monkeypatch.setattr(C, "ABACK_RECOVER", False)
    old = _scenario_world(CONVOY_SIX)
    old.run(2400)
    assert not [e for e in old.log if e.kind == "ship.boxed_off" or "aback with no way" in e.text]
    assert units.ms_to_knots(old.ship.dyn.u) < 0.5, old.ship.dyn.u


def test_truth_7_341_among_the_molene_islands_she_is_tacked_and_never_worn_onto_the_land(
    monkeypatch,
):
    """Package 88, item 2 (57's station gale: the frigate beating for her station off Ushant
    in a westerly gale was worn round with the land two miles under her lee, would not come
    round, and set down on the islands of the Molène passage). Two miles west of Molène in a
    westerly of 34 knots, her head N by W at four knots, the land a mile on her starboard
    bow: `put her about` tacks her ("where wearing would lose the ground"), where by the wind
    alone it would wear her; and a course shaped on the other tack that she has not the way
    to stay for is not worn round but kept full and by on her tack to claw off. The room a
    wear takes is the doctrine's `tack_regardless_nm` (two miles) over the lee half, by the
    lookout's nearest land, the coast by the chart at the account and the charted dangers
    (`navigation.no_room_to_wear`); with the law's switch off (`navigation.WEAR_ROOM`) she
    is worn as before."""
    from freesail.orders import navigation as N

    sc = Scenario(
        start_time=datetime(1805, 1, 12, 22, 0),
        wind_from_deg=270.0,
        wind_speed_kn=34.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 48.397, "lon_deg": -5.03},
        region="channel-west",
        ports=["brest"],
        nation="britain",
        ship_heading_deg=350.0,
        ship_speed_kn=4.0,
    )
    w = make_world(SEED, "data/ships/frigate-36.yaml", sc)
    w.run(120)
    assert N.no_room_to_wear(w.ship) == "the land a mile under her lee"
    verb, why = N.put_about_choice(w.ship)
    assert verb == "tack ship" and "where wearing would lose the ground" in why, why
    # the other tack's close-hauled course, SSW, with too little way to stay: kept full and by
    w.ship.dyn.u = w.ship.dyn.speed = units.knots_to_ms(1.5)
    judged = N.judge_course(w.ship, math.radians(200.0), helm_order=False)
    assert judged.branch == "full_and_by" and "no room to wear" in judged.words, judged
    monkeypatch.setattr(N, "WEAR_ROOM", False)
    assert N.put_about_choice(w.ship)[0] == "wear ship"
    assert N.judge_course(w.ship, math.radians(200.0), helm_order=False).branch == "wear"
