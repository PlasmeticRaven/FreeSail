"""Package 31: the sea and the ship's motion (spec M5 §4, §5; freesail/world/sea.py,
freesail/physics/motion.py).

The sea's build and decay against the open-sea relations; the swell a passing low leaves
behind; the words at each height; the motion's three numbers on the beam, ahead and
astern; each consequence in isolation (a reef in a smooth and a heavy sea; the strain in a
smooth sea unchanged; the head-sea loss; the glass pumping; the hooks for 5b inert); the
windage under bare poles measured; the readings, the dialect, the lines, the roll-up, the
snapshot and the console; a replay. Truth 56 and the day under systems alone are in
test_known_truths.py.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

import pytest

from freesail import units
from freesail.api import queries
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core import events
from freesail.core.events import Event, Severity
from freesail.core.world import Scenario, World
from freesail.crew import hands
from freesail.physics import motion as M
from freesail.physics import sails as S
from freesail.physics.motion import Motion, Particulars
from freesail.ship.parts import HelmMode, SailState
from freesail.standing.grammar import parse_condition
from freesail.world import sea as SEA
from freesail.world.sea import Sea
from tests.test_weather import gate_systems

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
T0 = datetime(1805, 6, 1, 4, 0)


def kn(knots: float) -> float:
    return units.knots_to_ms(knots)


def blow(sea: Sea, hours: float, knots: float, from_deg: float, start: datetime | None = None):
    """Feed the sea a steady wind for so many hours, a minute at a time, from where it is."""
    t = start or sea.now
    for minute in range(1, int(hours * 60) + 1):
        sea.tick(t + timedelta(minutes=minute), kn(knots), units.deg_to_rad(from_deg))
    return sea


def sea_of(hours: float, knots: float, from_deg: float = 0.0) -> Sea:
    """A sea raised from nothing by a wind of so many knots for so many hours."""
    sea = Sea(T0, 0.0, units.deg_to_rad(from_deg))
    return blow(sea, hours, knots, from_deg)


# ---------------------------------------------------------------------------
# the sea: build, decay, the swell, the words
# ---------------------------------------------------------------------------


def test_the_full_sea_is_pierson_moskowitz_and_the_period_the_open_sea_relation():
    """Hs = 0.0247 U^2 and Tp = 0.785 U for the fully developed sea (the constants worked
    from the spectrum; docs/dev/TuningNotes.md, M5a): fifteen knots make a sea of a metre
    and a half given a day, forty-five thirteen metres; the wind sea's period from its
    height by SEA_PERIOD_PER_ROOT_M, steeper than the developed relation's 5.0."""
    assert SEA.SEA_FULL_M_PER_MS2 * kn(15.0) ** 2 == pytest.approx(1.47, abs=0.02)
    assert SEA.SEA_FULL_M_PER_MS2 * kn(45.0) ** 2 == pytest.approx(13.2, abs=0.2)
    sea = sea_of(48.0, 15.0)
    assert sea.sea_m == pytest.approx(1.47, abs=0.02)
    assert sea.sea_period_s == pytest.approx(SEA.SEA_PERIOD_PER_ROOT_M * math.sqrt(1.47), abs=0.05)
    assert 3.6 <= SEA.SEA_PERIOD_PER_ROOT_M <= 5.0


def test_the_sea_builds_by_the_lag_and_decays_faster_than_it_builds():
    """A first-order lag: after SEA_BUILD_HOURS of a steady wind the sea is 63 per cent of
    its limit; the wind dropped, it decays with SEA_DECAY_HOURS, and the words say so
    ("the sea going down")."""
    full = SEA.SEA_FULL_M_PER_MS2 * kn(30.0) ** 2
    sea = sea_of(SEA.SEA_BUILD_HOURS, 30.0)
    assert sea.sea_m == pytest.approx(full * (1.0 - math.exp(-1.0)), rel=0.02)
    peak = sea.sea_m
    blow(sea, SEA.SEA_DECAY_HOURS, 0.0, 0.0)
    assert sea.sea_m == pytest.approx(peak * math.exp(-1.0), rel=0.02)
    assert SEA.SEA_DECAY_HOURS < SEA.SEA_BUILD_HOURS
    # a scenario opens on a sea already up, SEA_START_SHARE of the wind's full sea
    fresh = Sea(T0, kn(20.0), 0.0)
    assert fresh.sea_m == pytest.approx(
        SEA.SEA_START_SHARE * SEA.SEA_FULL_M_PER_MS2 * kn(20.0) ** 2
    )


def test_the_gale_of_a_day_raises_a_heavy_sea_that_a_low_leaves_behind_as_swell():
    """A day's gale of forty knots from the south-west, then the wind falls light: the
    wind sea dies over hours while the swell it left decays over SWELL_DECAY_HOURS, from
    the same quarter, and the words go from a very heavy sea to a heavy sea to a heavy
    swell to a long swell from the south-westward."""
    sea = sea_of(24.0, 40.0, 225.0)
    assert sea.state in ("heavy", "very heavy") and "heavy" in sea.words
    peak_m = sea.reading().height_m
    words = [sea.words]
    for _ in range(18):
        blow(sea, 1.0, 3.0, 225.0)
        if sea.words != words[-1]:
            words.append(sea.words)
    r = sea.reading()
    assert r.swell_m > 1.5 * r.sea_m
    assert r.swell_m == pytest.approx(peak_m * math.exp(-18.0 / SEA.SWELL_DECAY_HOURS), rel=0.1)
    assert r.swell_period_s > sea.sea_period_s
    assert SEA.quarter_words(r.swell_from_rad) == "the south-westward"
    assert words[0].endswith("heavy sea") and "swell from the south-westward" in words[-1]
    assert any(w.startswith("a heavy swell") for w in words), words
    # the swell is the record's strongest hour, decayed from its hour
    assert sea.swell()[0] == r.swell_m
    # a day and a half on it is all but gone, by its decay and not by the record's end
    blow(sea, 18.0, 3.0, 225.0)
    assert sea.words in ("a smooth sea", "a moderate sea")
    assert sea.reading().swell_m < SEA.SWELL_FROM_M
    assert sea.reading().swell_m == pytest.approx(peak_m * math.exp(-3.0), rel=0.1)


def test_a_swell_across_the_wind_makes_a_confused_sea_and_the_two_add_as_squares():
    """The wind veers eight points after a gale: the new sea builds across the old one's
    swell, the words say a confused sea, and the height is the root of the sum of the
    squares (the trains' energies add); a swell running with the sea is the same water."""
    sea = sea_of(12.0, 35.0, 270.0)
    blow(sea, 3.0, 25.0, 0.0)  # the wind now from the north, the swell from the west
    r = sea.reading()
    assert r.confused and r.words.startswith("a ") and "confused sea" in r.words
    assert "the swell from the westward" in r.words
    assert r.height_m == pytest.approx(math.hypot(r.sea_m, r.swell_m))
    assert abs(units.wrap_pi(r.swell_from_rad - r.sea_from_rad)) > units.points_to_rad(
        SEA.CROSS_SEA_POINTS
    )
    # the wind sea is the part of the sea along the wind now: the old sea is the swell's
    assert r.sea_from_rad == sea.wind_from == pytest.approx(0.0)
    assert 0.0 < r.sea_m < r.swell_m and r.sea_m < sea.vector_m
    with_it = sea_of(12.0, 35.0, 270.0)
    blow(with_it, 3.0, 25.0, 270.0)
    rr = with_it.reading()
    assert not rr.confused and rr.height_m == pytest.approx(max(rr.sea_m, rr.swell_m))
    assert rr.sea_m == pytest.approx(with_it.vector_m)


@pytest.mark.parametrize(
    "height, state, phrase",
    [
        (0.2, "smooth", "a smooth sea"),
        (1.0, "moderate", "a moderate sea"),
        (2.0, "short", "a short chopping sea"),
        (4.0, "heavy", "a heavy sea"),
        (7.0, "very heavy", "a very heavy sea"),
    ],
)
def test_the_words_at_each_height_are_the_periods_and_never_a_number(height, state, phrase):
    assert SEA.sea_state_word(height) == state
    sea = Sea(T0, 0.0, 0.0)
    sea._hx, sea._hy = 0.0, height  # the wind sea alone, from the north
    sea._reading = None
    assert sea.words == phrase and sea.state == state
    assert not any(ch.isdigit() for ch in sea.words)
    assert state in SEA.SEA_STATE_WORDS
    for words, source in SEA.SEA_WORDS_SOURCES.items():
        assert source and ("Falconer" in source or "Luce" in source or "spec" in source), words


def test_the_quarter_words_name_eight_quarters():
    assert SEA.quarter_words(units.deg_to_rad(270.0)) == "the westward"
    assert SEA.quarter_words(units.deg_to_rad(300.0)) == "the north-westward"
    assert SEA.quarter_words(units.deg_to_rad(359.0)) == "the northward"
    assert SEA.quarter_words(units.deg_to_rad(112.0)) == "the eastward"
    assert SEA.quarter_words(units.deg_to_rad(113.0)) == "the south-eastward"


# ---------------------------------------------------------------------------
# the motion: three numbers, on the beam, ahead and astern
# ---------------------------------------------------------------------------


def settled(sea: Sea, heading_deg: float, particulars: Particulars | None = None) -> Motion:
    m = Motion(particulars or Particulars())
    for _ in range(10 * 60):
        m.tick(1.0, sea, units.deg_to_rad(heading_deg))
    return m


def test_the_roll_period_is_the_ships_own_from_her_beam_and_her_stability():
    frigate = Particulars.of(make_world(7, FRIGATE).ship)
    schooner = Particulars.of(make_world(7, SCHOONER).ship)
    assert frigate == Particulars(11.7, 1.3, 41.8)
    assert frigate.roll_period_s == pytest.approx(8.2, abs=0.1)
    assert schooner.roll_period_s == pytest.approx(5.8, abs=0.1)
    assert Particulars.of(World(seed=1).ship) == Particulars()  # the point ship: the frigate's


def test_the_motions_three_numbers_on_the_beam_ahead_and_astern():
    """A heavy sea from the north on the frigate: the roll is greatest on the beam and
    least ahead and astern, the pitch the other way, the heave the same on every heading;
    each relaxes with MOTION_TIME_CONSTANT_S; nothing moves her on the plane."""
    sea = sea_of(6.0, 40.0, 0.0)
    beam, ahead, astern = settled(sea, 90.0), settled(sea, 0.0), settled(sea, 180.0)
    assert beam.roll_deg > 2.0 * ahead.roll_deg and ahead.roll_deg == pytest.approx(astern.roll_deg)
    assert ahead.pitch_deg > 2.0 * beam.pitch_deg and ahead.pitch_deg == pytest.approx(
        astern.pitch_deg
    )
    assert beam.pitch_deg == pytest.approx(0.0, abs=0.01)
    assert beam.heave_m == pytest.approx(ahead.heave_m) == pytest.approx(astern.heave_m)
    assert beam.heave_m > 1.0 and beam.roll_deg <= M.ROLL_MAX_DEG
    assert beam.words.startswith("rolling") and ahead.words.startswith("pitching")
    assert "into it" in ahead.words and "under her stern" in astern.words
    # the time constant: a motion from rest is 63 per cent of its target after it
    m = Motion(Particulars())
    target = m.targets(sea, units.deg_to_rad(90.0))[0]
    for _ in range(int(M.MOTION_TIME_CONSTANT_S)):
        m.tick(1.0, sea, units.deg_to_rad(90.0))
    assert m.roll_deg == pytest.approx(target * (1.0 - math.exp(-1.0)), rel=0.02)
    # a smooth sea: easy
    assert settled(sea_of(1.0, 3.0), 90.0).words == "easy"
    # the words, by the numbers
    assert M.motion_words(1.0, 1.0) == ("easy", "easy", False)
    assert M.motion_words(20.0, 1.0) == ("rolling heavily", "rolling", True)
    assert M.motion_words(20.0, 10.0) == ("labouring heavily", "labouring", True)
    assert (
        M.motion_words(1.0, 10.0, following=True)[0] == "pitching heavily, the sea under her stern"
    )


def test_the_motion_on_the_ship_reads_from_the_sea_the_world_keeps():
    """With systems alone the world keeps the sea and the motion, the ship's physics reads
    the motion through `ship.extra["motion"]`, and nothing moves her on the plane by it:
    two frigates in the same wind, one with the sea kept and one without, sail the same
    course to within the head-sea loss."""
    sc = gate_systems()
    w = make_world(7, FRIGATE, sc)
    assert w.sea is not None and w.motion is not None and w.ship.extra["motion"] is w.motion
    w.run(600)
    assert w.motion.roll_deg > 0.0 and w.readings["motion"]["words"] != ""
    none = Scenario.from_dict(sc.to_dict())
    none.sea = False
    v = make_world(7, FRIGATE, none)
    assert v.sea is None and "motion" not in v.ship.extra
    assert v.readings["sea"] is None and v.readings.words("sea") == R.NO_SEA_WORDS
    # a fixed wind keeps no sea unless the scenario asks
    assert World(seed=1).sea is None
    asked = World(seed=1, scenario=Scenario(sea=True))
    assert asked.sea is not None and asked.readings["sea"]["state"] in SEA.SEA_STATE_WORDS
    # the pinned day keeps none (the truths' fixture), the day under systems does
    from freesail.world.scenarios import load_scenario

    assert load_scenario("data/scenarios/gate-4c-day.yaml").scenario.sea is None
    pinned = World(seed=7, scenario=load_scenario("data/scenarios/gate-4c-day.yaml").scenario)
    assert pinned.sea is None
    systems = World(seed=7, scenario=load_scenario("data/scenarios/gate-5a-day.yaml").scenario)
    assert systems.sea is not None


# ---------------------------------------------------------------------------
# the consequences, each in isolation
# ---------------------------------------------------------------------------


def heavy_sea_aboard(world: World, knots: float = 45.0, hours: float = 24.0, from_deg=0.0):
    """Put a gale's sea of so many hours into a world's `sea` and let the motion settle."""
    assert world.sea is not None
    start = world.clock.ship_time - timedelta(hours=hours)
    world.sea._record.clear()  # the gale's hours are the record now
    world.sea._last_record = start
    blow(world.sea, hours, knots, from_deg, start=start)
    world.sea.now = world.clock.ship_time
    world.sea._reading = None
    for _ in range(600):
        world.motion.tick(1.0, world.sea, world.ship.heading)
    return world


def test_the_crew_factor_aloft_rises_with_the_roll_and_not_in_a_smooth_sea():
    """`hands.seaway_factor`: 1.0 to SEAWAY_FACTOR_TABLE's first row (a smooth sea and no
    sea are the same), the table between, aloft above the deck, the last row beyond."""
    first = hands.SEAWAY_FACTOR_TABLE[0][0]
    assert hands.seaway_factor(0.0, True) == hands.seaway_factor(first, True) == 1.0
    assert hands.seaway_factor(0.0, False) == 1.0
    last = hands.SEAWAY_FACTOR_TABLE[-1]
    assert (
        hands.seaway_factor(90.0, True) == last[1] and hands.seaway_factor(90.0, False) == last[2]
    )
    rolls = [row[0] for row in hands.SEAWAY_FACTOR_TABLE]
    for a, b in zip(rolls, rolls[1:], strict=False):
        mid = 0.5 * (a + b)
        assert (
            hands.seaway_factor(a, True)
            <= hands.seaway_factor(mid, True)
            <= hands.seaway_factor(b, True)
        )
        assert hands.seaway_factor(mid, True) >= hands.seaway_factor(mid, False) >= 1.0
    # through crew_factor, on any request
    from tests.test_hands import sailor

    want = hands.CrewRequest(hands=4, rating=hands.Rating.ORDINARY)
    men = [sailor(i, hands.Rating.ORDINARY, hands.Station.AFTERGUARD) for i in range(4)]
    got = hands.Assignment("x", 4, men)
    assert hands.crew_factor(got, want, aloft=True) == 1.0
    assert hands.crew_factor(got, want, aloft=True, roll_deg=15.0) == hands.seaway_factor(
        15.0, True
    )
    assert hands.crew_factor(got, want, aloft=False, roll_deg=15.0) == hands.seaway_factor(
        15.0, False
    )


def reef_ticks(world: World) -> int:
    """Ticks from 'reef the fore topsail' to the reef taken, on a frigate under plain sail."""
    start = world.clock.tick
    world.submit("reef the fore topsail")
    for _ in range(3600):
        world.tick()
        if any(e.kind == "sail.reefed" and e.tick > start for e in world.log.since(start)):
            return world.clock.tick - start
    raise AssertionError("the reef was not taken in an hour")


def frigate_under_plain_sail(sea: bool, knots: float = 15.0) -> World:
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=90.0,
        ship_speed_kn=4.0,
        sea=sea,
        start_time=datetime(1805, 6, 1, 10, 0),
    )
    w = make_world(7, FRIGATE, sc)
    for sid in w.ship.groups["plain sail"]:
        w.ship.sails[sid].state = SailState.SET
    w.run(120)
    return w


def test_a_reef_takes_half_as_long_again_in_a_heavy_sea_as_in_a_smooth_one():
    """The consequence in isolation (truth 56 sails the gale for it): the same frigate on a
    beam reach reefs her fore topsail with no sea kept, in a smooth sea (the same to the
    tick: the table's first row) and in the sea a gale of a day left on her beam, the last
    half as long again (the roll's table, aloft above all)."""
    quick = reef_ticks(frigate_under_plain_sail(sea=False))
    smooth = frigate_under_plain_sail(sea=True, knots=8.0)
    assert smooth.sea.state == "smooth" and smooth.motion.roll_deg < hands.SEAWAY_FACTOR_TABLE[0][0]
    assert reef_ticks(smooth) == reef_ticks(frigate_under_plain_sail(sea=False, knots=8.0))
    heavy = heavy_sea_aboard(frigate_under_plain_sail(sea=True), knots=40.0)
    assert heavy.sea.state in ("heavy", "very heavy") and heavy.motion.roll_deg > M.ROLL_HEAVY_DEG
    slow = reef_ticks(heavy)
    assert 1.4 <= slow / quick <= 1.7, (quick, slow)


def test_the_strain_reads_the_motion_as_an_extra_load_and_is_unchanged_in_a_smooth_sea():
    """The load factor is exactly 1.0 without a sea and within its dead band, so the loads
    the strain model judges are the sails model's own; in a heavy sea the spars and the
    gear are judged harder by the roll and the pitch, the canvas as before."""
    at_rest = Motion(Particulars())
    assert at_rest.load_factor == 1.0
    at_rest.roll_deg = M.STRAIN_DEAD_BAND_DEG
    assert at_rest.load_factor == 1.0
    rolling = Motion(Particulars())
    rolling.roll_deg, rolling.pitch_deg = 22.0, 12.0
    expected = 1.0 + M.STRAIN_ROLL_PER_DEG * 20.0 + M.STRAIN_PITCH_PER_DEG * 10.0
    assert rolling.load_factor == pytest.approx(min(expected, M.STRAIN_FACTOR_MAX))
    rolling.roll_deg = 90.0
    assert rolling.load_factor == M.STRAIN_FACTOR_MAX
    # on the frigate: the loads judged in a smooth sea are the loads with no sea kept
    a = frigate_under_plain_sail(sea=False, knots=8.0)
    b = frigate_under_plain_sail(sea=True, knots=8.0)
    assert b.motion.load_factor == 1.0 and b.sea.state == "smooth"
    a.run(60)
    b.run(60)
    for pid, part in a.ship.parts.items():
        assert part.load_kn == pytest.approx(b.ship.parts[pid].load_kn, rel=1e-9), pid
    # and harder in a heavy sea, spars and lines, not the canvas
    a = frigate_under_plain_sail(sea=False)
    c = heavy_sea_aboard(frigate_under_plain_sail(sea=True))
    factor = c.motion.load_factor
    assert factor > 1.05
    c.run(1)
    a.run(1)
    from freesail.ship.parts import Sail, Spar

    for pid, part in a.ship.parts.items():
        other = c.ship.parts[pid]
        if part.load_kn <= 0.0 or other.load_kn <= 0.0:
            continue
        if isinstance(part, Sail):
            assert other.load_kn == pytest.approx(part.load_kn, rel=0.05), pid
        elif isinstance(part, Spar):
            assert other.load_kn > part.load_kn * 1.03, pid


def test_the_hull_loses_speed_in_a_head_sea_by_a_small_factor():
    """The frigate close-hauled on the starboard tack, the sea a gale left on her bow: her
    speed falls by the added resistance (HEAD_SEA_RESISTANCE_PER_M by the sea's height and
    the square of the cosine of its angle on the bow), a small factor; nothing on the beam
    or astern."""

    def sail(sea_from_deg: float | None, heading: float = 80.0) -> World:
        sc = Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=15.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=heading,
            ship_speed_kn=6.0,
            sea=sea_from_deg is not None,
        )
        w = make_world(7, FRIGATE, sc)
        w.submit("set plain sail")
        for i in range(1200):
            if i % 120 == 0:
                w.submit("trim sails")
            w.tick()
        if sea_from_deg is not None:
            # the swell a gale left, from right ahead or right astern of her course
            heavy_sea_aboard(w, 35.0, 12.0, from_deg=sea_from_deg)
        for i in range(900):
            if i % 120 == 0:
                w.submit("trim sails")
            w.tick()
        return w

    calm = units.ms_to_knots(sail(None).ship.dyn.speed)
    assert calm > 5.0
    head = sail(80.0)
    astern = sail(260.0)
    assert head.motion.resistance_factor > 1.15
    assert units.ms_to_knots(head.ship.dyn.speed) < 0.93 * calm
    assert units.ms_to_knots(head.ship.dyn.speed) > 0.7 * calm
    assert astern.motion.resistance_factor == 1.0
    assert units.ms_to_knots(astern.ship.dyn.speed) == pytest.approx(calm, rel=0.03)


def test_the_glass_pumps_by_a_hundredth_or_two_in_a_seaway():
    """`Glass.read` scales its noise by the motion's `pumping`, never past
    GLASS_PUMP_MAX_IN: at rest the readings stay within half a hundredth of the pressure,
    in a heavy seaway within two, and beyond half a hundredth some of the time."""
    from freesail.world.weather import GLASS_NOISE_IN, GLASS_PUMP_MAX_IN, Glass, inches

    still, rolling = Glass(seed=7), Glass(seed=7)
    heavy = Motion(Particulars())
    heavy.roll_deg, heavy.pitch_deg = 15.0, 8.0
    assert heavy.pumping > 2.0 and Motion(Particulars()).pumping == 1.0
    spread_still, spread_rolling = [], []
    for minute in range(120):
        t = T0 + timedelta(minutes=minute)
        spread_still.append(abs(still.read(1015.0, t) - inches(1015.0)))
        spread_rolling.append(abs(rolling.read(1015.0, t, heavy.pumping) - inches(1015.0)))
    assert max(spread_still) <= GLASS_NOISE_IN + 0.005  # rounded to the hundredth
    assert max(spread_rolling) <= GLASS_PUMP_MAX_IN + 0.005
    assert max(spread_rolling) > max(spread_still)
    assert Glass(seed=7).read(1015.0, T0, 1000.0) == pytest.approx(inches(1015.0), abs=0.025)


def test_the_hooks_for_5b_are_numbers_that_nothing_reads_yet():
    sea = sea_of(24.0, 40.0)
    calm = Sea(T0, 0.0, 0.0)
    assert calm.horizon_nm(30.0) == pytest.approx(2.08 * math.sqrt(30.0))
    assert sea.horizon_nm(30.0) < calm.horizon_nm(30.0)
    assert sea.horizon_nm(1.0) == pytest.approx(2.08)  # never below a metre of eye
    m = Motion(Particulars())
    assert m.sight_error_factor == 1.0
    m.roll_deg, m.pitch_deg = 15.0, 5.0
    assert m.sight_error_factor == pytest.approx(1.0 + M.SIGHT_ERROR_PER_DEG * 20.0)


# ---------------------------------------------------------------------------
# windage under bare poles (M4 open item 7), measured
# ---------------------------------------------------------------------------


def bare_poles(knots: float, heading_deg: float, minutes: int = 30, helm: str = "amidships"):
    """The frigate under bare poles in a steady wind from the north, from rest."""
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading_deg,
    )
    w = make_world(7, FRIGATE, sc)
    for s in w.ship.sails.values():
        s.state = SailState.FURLED
    w.ship.dyn.helm_mode = HelmMode.RUDDER
    w.ship.dyn.target_rudder = 0.0 if helm == "amidships" else -units.deg_to_rad(35.0)
    w.run(minutes * 60)
    return w


def test_windage_under_bare_poles_is_measured_and_recorded():
    """M4 open item 7: the frigate under bare poles in fifteen knots dead astern makes
    about three knots (2.9 measured before this package and after it: the rig's windage
    was not moved, docs/dev/TuningNotes.md, M5a, says why against Steel 1794 and
    Falconer 1780), eight in a strong gale; lying a-hull with the wind abeam she drifts
    to leeward at under a knot and a half, which is Luce's "drifting bodily to leeward"."""
    running = bare_poles(15.0, 180.0)
    assert 2.5 <= units.ms_to_knots(running.ship.dyn.u) <= 3.2
    forces = S.compute_sail_forces(running.ship, running.wind)
    assert forces.windage_drag_n == pytest.approx(forces.thrust_n, rel=0.01)  # windage alone
    assert 7.0 <= units.ms_to_knots(bare_poles(45.0, 180.0).ship.dyn.u) <= 9.0
    # lying a-hull she comes up and falls off between four and seven points (54 to 110
    # degrees of heading, the wind at north), now with sternway, now without; the drift is
    # read over her last ten minutes (package 37p: a single tick's way, read before, fell
    # on whichever side of the swing the half hour ended, and the keel's grip astern moved
    # it; the drift is south-west at 0.8 knots with it and without it)
    a_hull = bare_poles(15.0, 90.0, minutes=20, helm="a-lee")
    d = a_hull.ship.dyn
    x0, y0 = d.x, d.y
    a_hull.run(600)
    dx, dy = d.x - x0, d.y - y0
    leeward = units.ms_to_knots(math.hypot(dx, dy) / 600.0)
    assert 0.2 <= leeward <= 1.5, leeward
    bearing = math.degrees(math.atan2(dx, dy)) % 360.0
    assert 135.0 <= bearing <= 270.0, bearing  # bodily to leeward, not ahead


# ---------------------------------------------------------------------------
# readings, the dialect, the lines, the roll-up, the snapshot and the console
# ---------------------------------------------------------------------------


def test_the_readings_on_both_ships_and_the_absent_pattern():
    frigate = make_world(7, FRIGATE, gate_systems())
    schooner = make_world(7, SCHOONER, gate_systems())
    for w in (frigate, schooner):
        w.run(300)
        r = w.readings
        sea, motion = r["sea"], r["motion"]
        assert sea["state"] in SEA.SEA_STATE_WORDS and sea["words"].startswith("a ")
        assert motion["state"] in M.MOTION_STATE_WORDS and r.words("motion") == motion["words"]
        assert r.words("sea") == sea["words"]
        assert sea["height_m"] > 0 and sea["period_s"] > 0
        assert motion["roll_period_s"] == pytest.approx(w.motion.roll_period_s, abs=0.1)
    assert (
        frigate.readings["motion"]["roll_period_s"] != schooner.readings["motion"]["roll_period_s"]
    )
    bare = World(seed=1)
    assert bare.readings["sea"] is None and bare.readings["motion"] is None
    assert bare.readings.words("sea") == R.NO_SEA_WORDS
    assert bare.readings.words("motion") == R.NO_SEA_WORDS
    from freesail.agents.tools import readings_words

    words = readings_words(frigate)
    assert {"sea", "motion"} <= set(words) and words["sea"] == frigate.sea.words
    assert [r.kind for r in R.REGISTRY.by_words("the sea")] == ["sea"]
    assert R.REGISTRY.get("motion").words == ("the motion", "the ship's motion")


def test_the_dialect_reads_the_sea_and_the_motion_for_nothing():
    """`when the sea is heavy then ...` is a book's line (spec M5 §5), on a ship with a sea
    kept or without; the words compared are the state words, 'heavy' holding for a very
    heavy sea and 'rolling' for rolling heavily."""
    from freesail.orders.errors import OrderError
    from freesail.standing.rules import Clause, Comparison

    ship = make_world(7, SCHOONER).ship
    c = parse_condition("the sea is heavy", ship)
    assert (c.clauses[0].reading, c.clauses[0].comparison.value) == ("sea", "heavy")
    assert parse_condition("the sea is chopping", ship).clauses[0].comparison.value == "short"
    assert parse_condition("the sea is a cross sea", ship).clauses[0].comparison.value == "confused"
    assert parse_condition("the sea is not smooth", ship).clauses[0].comparison.op == "is_not"
    c = parse_condition("the motion is rolling heavily and the sea is very heavy", ship)
    assert [(x.reading, x.comparison.value) for x in c.clauses] == [
        ("motion", "rolling heavily"),
        ("sea", "very heavy"),
    ]
    assert parse_condition("the ship's motion is easy", ship).clauses[0].reading == "motion"
    assert parse_condition("the motion is labouring heavily", ship).clauses[0].comparison.value == (
        "labouring"
    )
    for text, words in (
        ("the sea exceeds 3", "cannot be"),
        ("the sea is blue", "cannot be 'blue'"),
        ("the motion is under 30 knots", "cannot be"),
    ):
        with pytest.raises(OrderError, match=words):
            parse_condition(text, ship)
    # no sea kept: the condition reads false, and its words say why
    w = make_world(7, SCHOONER)
    assert not c.holds(w.readings)
    heavy = Clause("sea", Comparison("is", "heavy", "heavy"), "x", (), "the sea")
    assert R.NO_SEA_WORDS in heavy.describe(w.readings)
    # kept: the state words
    v = heavy_sea_aboard(frigate_under_plain_sail(sea=True))
    view = v.readings
    assert heavy.holds(view) and v.readings["sea"]["state"] == "very heavy"
    assert Clause("sea", Comparison("is", "very heavy", "very heavy"), "x", (), "the sea").holds(
        view
    )
    assert not Clause("sea", Comparison("is", "smooth", "smooth"), "x", (), "the sea").holds(view)
    rolling = Clause("motion", Comparison("is", "rolling", "rolling"), "x", (), "the motion")
    assert rolling.holds(view) and view["motion"]["heavy"]
    assert Clause("motion", Comparison("is", "heavy", "heavy"), "x", (), "the motion").holds(view)
    assert not Clause("motion", Comparison("is", "easy", "easy"), "x", (), "the motion").holds(view)


def test_a_standing_order_on_the_sea_fires_as_the_sea_gets_up():
    """The frigate under the day's low from the evening: the sea gets up with the gale, and
    a rule on it fires (spec M5 §5)."""
    sc = gate_systems()
    sc.start_time = datetime(1805, 6, 1, 19, 0)
    w = make_world(7, FRIGATE, sc)
    w.submit('standing order "sea": when the sea is heavy then steer 200')
    w.run(4 * 3600)
    fired = [e for e in w.log if e.kind == "order.accepted" and "By standing order 'sea'" in e.text]
    assert fired and w.readings["sea"]["state"] in ("heavy", "very heavy")


def test_the_log_says_the_sea_when_its_words_change_and_the_rollup_says_it_by_the_hour():
    sc = gate_systems()
    sc.start_time = datetime(1805, 6, 1, 18, 0)
    w = World(seed=7, scenario=sc)
    w.run(7 * 3600)
    seas = [e for e in w.log if e.kind == "sea.change"]
    assert seas and all(e.severity is Severity.ROUTINE for e in seas)
    assert any("getting up" in e.text for e in seas)
    assert all(e.text[0].isupper() and e.text.endswith(".") for e in seas)
    assert all(e.data["state"] in SEA.SEA_STATE_WORDS for e in seas)
    motions = [e for e in w.log if e.kind == "motion.change"]
    assert motions and all(
        e.text.endswith(".") and e.data["state"] in M.MOTION_STATE_WORDS for e in motions
    )
    # no two motion lines within the hold
    from freesail.core.world import MOTION_WORDS_HOLD_S

    assert all(
        b.tick - a.tick >= MOTION_WORDS_HOLD_S for a, b in zip(motions, motions[1:], strict=False)
    )
    hours = [e for e in w.log if e.kind == "weather.hour"]
    assert all(e.data["sea"] == e.data["sea"] and "sea" in e.text for e in hours)
    # the roll-up
    t = datetime(1805, 6, 1, 22, 0)

    def ev(kind, text, data=None, minute=0):
        return Event(
            tick=minute * 60,
            ship_time=t + timedelta(minutes=minute),
            severity=Severity.ROUTINE,
            kind=kind,
            text=text,
            data=data or {},
        )

    hour = ev(
        "weather.hour",
        "Overcast, rain; the glass 29.72; a heavy sea, rolling heavily.",
        {
            "sky": "overcast",
            "weather": "rain",
            "glass_in": 29.72,
            "sea": "a heavy sea",
            "motion": "rolling heavily",
        },
    )
    got_up = ev("sea.change", "A heavy sea getting up.", {"sea": "a heavy sea"}, minute=20)
    rolled = ev("motion.change", "Rolling heavily.", {"motion": "rolling heavily"}, minute=40)
    text = events.summarise([hour, got_up, rolled]).text
    assert "a heavy sea, rolling heavily" in text and "a heavy sea getting up" in text
    assert "rolling heavily" in text and text.endswith("3 routine entries.")
    # the whole day's roll-up carries the sea by the hour
    shown = events.rollup(w.log.all(), 300, so_far=True)
    rolls = [x for x in shown if isinstance(x, events.Rollup)]
    assert any(" sea" in r.text for r in rolls)


def test_the_snapshot_and_the_console_carry_the_sea_and_the_motion():
    w = make_world(7, FRIGATE, gate_systems())
    w.run(61)
    wx = queries.snapshot(w)["weather"]
    assert wx["sea"] == w.sea.words and wx["motion"] == w.motion.words
    assert wx["sea_height_m"] > 0 and wx["roll_deg"] >= 0.0 and wx["sea_from"] is not None
    lines = w.summary_lines()
    sea_line = [ln for ln in lines if ln.startswith("A ") and " sea" in ln or "swell" in ln]
    assert sea_line and sea_line[0].endswith(".") and w.motion.words in sea_line[0]
    assert "from the" in sea_line[0]
    bare = World(seed=1)
    assert queries.snapshot(bare)["weather"]["sea"] is None
    assert queries.snapshot(bare)["weather"]["sea_words"] == R.NO_SEA_WORDS
    assert not any(" sea" in ln for ln in bare.summary_lines())
    # nothing a player reads names a number of the Douglas scale or a metre
    for ln in lines:
        assert " m " not in ln and "metre" not in ln


def test_the_sea_is_deterministic_and_a_replay_raises_it_again():
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    sc = gate_systems()
    a, b = World(seed=7, scenario=sc), World(seed=7, scenario=sc)
    for _ in range(6):
        a.run(3600)
        b.run(3600)
        assert (
            a.readings["sea"] == b.readings["sea"] and a.readings["motion"] == b.readings["motion"]
        )
    assert a.log.digest() == b.log.digest()
    assert a.save()["scenario"]["sea"] is None
    copy = replay_mod.replay(a.save(), ship_factory)
    assert copy.log.digest() == a.log.digest() and copy.readings["sea"] == a.readings["sea"]
    other = World(seed=8, scenario=sc)
    other.run(6 * 3600)
    assert other.readings["sea"]["height_m"] != a.readings["sea"]["height_m"]


def test_the_scenario_file_says_whether_the_sea_is_kept(tmp_path):
    from freesail.world.scenarios import load_scenario

    base = (
        "name: x\nstart: 1805-06-01T04:00\nweather:\n  wind:\n"
        "    - {at: 1805-06-01T04:00, from_deg: 270, knots: 17}\n"
    )
    pinned = tmp_path / "pinned.yaml"
    pinned.write_text(base, encoding="utf-8")
    sf = load_scenario(pinned)
    assert sf.scenario.sea is None and not any("sea" in ln for ln in sf.lines())
    assert World(seed=1, scenario=sf.scenario).sea is None
    kept = tmp_path / "kept.yaml"
    kept.write_text(base + "  sea: true\n", encoding="utf-8")
    sf = load_scenario(kept)
    assert sf.scenario.sea is True and any("The sea" in ln for ln in sf.lines())
    assert World(seed=1, scenario=sf.scenario).sea is not None
    sf = load_scenario("data/scenarios/gate-5a-day.yaml")
    assert sf.scenario.sea is None and any("The sea" in ln for ln in sf.lines())
