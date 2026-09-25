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
"""

from __future__ import annotations

import math

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario

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


def run(world, ticks: int, trim_every: int = 0) -> None:
    for i in range(ticks):
        if trim_every and i % trim_every == 0:
            world.submit("trim sails")
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


def pointing_sweep(ship, start_off=80, stop_off=44) -> list[dict]:
    """Steer up two degrees at a time until she can no longer hold three knots."""
    world = under_plain_sail(ship, 360.0 - start_off)  # starboard tack
    rows = []
    off = start_off
    while off >= stop_off:
        world.submit(f"steer {360 - off}")
        run(world, 300, trim_every=100)
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
    warnings = [e for e in events(world, "strain.warning") if "topgallant" in (e.subject or "")]
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
    assert 300 <= seconds <= 600, f"tacked in {seconds} s"
    assert world.ship.dyn.tack == "larboard"
    assert world.ship.dyn.y > y_before  # the wind is from north: north is windward


def test_truth_10_she_misses_stays_when_put_about_under_three_knots():
    world = close_hauled_on_starboard(FRIGATE, knots_=8.0, speed_kn=2.0)
    assert 2.0 <= knots(world) < 3.0
    world.submit("tack ship")
    done, _ = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in done] == ["ship.missed_stays"]
    assert done[0].severity.value == "urgent"
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


def studding_sail_gain(heading_deg: float) -> float:
    world = under_plain_sail(FRIGATE, heading_deg, knots_=10.0)
    plain = knots(world)
    world.submit("set the studdingsails, both sides")
    run(world, 600, trim_every=120)
    world.submit("set the studdingsails, both sides")  # those that waited for the sail beside them
    run(world, 900, trim_every=120)
    assert sum(1 for s in world.ship.sails.values() if s.cls == "studding" and s.is_set) == 10
    return 100.0 * (knots(world) / plain - 1.0)


def test_truth_14_studding_sails_help_on_a_broad_reach_and_not_close_hauled():
    assert 15.0 <= studding_sail_gain(135.0) <= 30.0
    assert studding_sail_gain(67.5) < 5.0


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
