"""Package 9: strain, wear and carrying away (freesail/physics/strain.py)."""

from __future__ import annotations

import copy
import math
import random
import statistics

import pytest

from freesail.api.session import make_world
from freesail.core.rng import Rng
from freesail.core.world import Scenario
from freesail.evolutions import Runner
from freesail.physics import strain as S
from freesail.physics.sails import compute_sail_forces
from freesail.physics.strain import apply_strain, failure_probability, strain_state
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import LineState, SailState
from freesail.ship.stub import OrderError
from tests.test_ship_loader import MINIMAL

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CARRIED_AWAY_KINDS = {"line.parted", "spar.carried_away", "sail.blown_out"}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def minimal_ship():
    return ship_from_dict(copy.deepcopy(MINIMAL), "minimal")


def load(part, ratio: float, rating: float = 10.0) -> None:
    """Put a load on a part as a multiple of its rating (giving it one if the
    ship file gave none)."""
    if part.rating_kn <= 0:
        part.rating_kn = rating
    part.load_kn = ratio * part.rating_kn


def tick(ship, seconds: int, stream=None) -> list:
    """Apply strain for so many one-second ticks with the loads left as they
    are (no physics), returning the notes."""
    notes = []
    for _ in range(seconds):
        apply_strain(ship, 1.0, stream)
        notes.extend(ship.drain_notes())
    return notes


def kinds(notes):
    return [n[1] for n in notes]


def texts(notes):
    return [n[2] for n in notes]


def steady_wind(from_deg: float, knots: float) -> Wind:
    return Wind(WindParams.from_nautical(from_deg, knots, 0.0, 0.0), random.Random(0))


def set_sails(ship, ids, brace_deg: float = 0.0, sheet_deg: float = 30.0) -> None:
    for s in ship.sails.values():
        s.state = SailState.FURLED
    for sid in ids:
        ship.sails[sid].state = SailState.SET
    for sp in ship.spars.values():
        if sp.is_yard:
            limit = sp.brace_limit if sp.brace_limit > 0 else math.pi / 2
            sp.brace_angle = math.copysign(min(abs(math.radians(brace_deg)), limit), brace_deg)
    for s in ship.sails.values():
        if s.is_fore_and_aft:
            s.sheet_angle = math.radians(sheet_deg)


def frigate_with_wind(sails, knots=15.0, brace_deg=45.0):
    """The frigate with the wind 70° on the starboard bow, yards braced 45°
    (chord 45° off the bow, so the square sails draw), and the physics loads
    written once, so the strain rule has something to judge."""
    ship = load_ship(FRIGATE)
    ship.dyn.heading = 0.0
    set_sails(ship, sails, brace_deg=brace_deg)
    wind = steady_wind(70.0, knots)
    compute_sail_forces(ship, wind)
    return ship, wind


# ---------------------------------------------------------------------------
# the rule: decay, warnings, chance and certainty
# ---------------------------------------------------------------------------


def test_nothing_happens_at_or_below_the_rating():
    ship = minimal_ship()
    mast = ship.spars["mast"]
    load(mast, 1.0)
    notes = tick(ship, 600)
    assert mast.condition == 100.0 and not mast.wrecked
    assert notes == []


@pytest.mark.parametrize(
    "ratio,per_minute", [(1.1, 0.2), (1.25, 0.5), (1.5, 1.0), (2.0, 2.0), (3.0, 4.0)]
)
def test_condition_decays_at_two_points_per_minute_per_unit_over_the_rating(ratio, per_minute):
    ship = minimal_ship()
    mast = ship.spars["mast"]
    load(mast, ratio)
    tick(ship, 60)
    assert mast.condition == pytest.approx(100.0 - per_minute)
    tick(ship, 120)
    assert mast.condition == pytest.approx(100.0 - 3 * per_minute)
    assert not mast.wrecked


def test_condition_decay_scales_with_dt():
    a, b = minimal_ship(), minimal_ship()
    load(a.spars["mast"], 1.5)
    load(b.spars["mast"], 1.5)
    apply_strain(a, 60.0)
    tick(b, 60)
    assert a.spars["mast"].condition == pytest.approx(b.spars["mast"].condition)


def test_strain_warning_once_per_part_per_ten_minutes():
    ship = minimal_ship()
    mast = ship.spars["mast"]
    yard = ship.spars["topsail.yard"]
    load(mast, 1.2)
    load(yard, 1.3)
    notes = tick(ship, 1500)  # twenty-five minutes
    warnings = [n for n in notes if n[1] == "strain.warning"]
    assert [n[3] for n in warnings] == ["mast", "topsail.yard"] * 3  # t = 1 s, 601 s, 1201 s
    assert all(n[0] == "notable" for n in warnings)
    assert warnings[0][2] == "Mast working under the press of sail."
    assert warnings[0][4]["ratio"] == pytest.approx(1.2)
    assert warnings[1][2] == "Topsail yard working under the press of sail."


def test_warning_wording_grows_dire_over_one_and_a_half():
    ship = minimal_ship()
    load(ship.spars["mast"], 1.6)
    load(ship.lines["topsail.yard.halyard"], 1.6)
    load(ship.lines["topsail.yard.brace.larboard"], 1.2)
    ship.sails["topsail"].state = SailState.SET
    load(ship.sails["topsail"], 1.6)
    ship.sails["mainsail"].state = SailState.SET
    load(ship.sails["mainsail"], 1.2)
    notes = tick(ship, 1)
    by_subject = {n[3]: n[2] for n in notes if n[1] == "strain.warning"}
    assert by_subject["mast"].startswith("Mast bending like a whip")
    assert (
        by_subject["topsail.yard.halyard"]
        == "Topsail yard halyard stranding; it will not hold much longer."
    )
    assert by_subject["topsail.yard.brace.larboard"] == (
        "Larboard topsail yard brace bar-taut and surging on the pin."
    )
    assert by_subject["topsail"].startswith("Topsail stretched drum-tight")
    assert by_subject["mainsail"] == "Mainsail straining at the bolt-ropes."


def test_without_a_stream_nothing_fails_by_chance():
    ship = minimal_ship()
    mast = ship.spars["mast"]
    load(mast, 3.0)  # p per substep would be 0.0045: near-certain within ten minutes
    notes = tick(ship, 600)
    assert not mast.wrecked
    assert mast.condition == pytest.approx(60.0)
    assert "spar.carried_away" not in kinds(notes)


def test_carries_away_for_certain_when_condition_reaches_zero():
    ship = minimal_ship()
    mast = ship.spars["mast"]
    mast.condition = 1.0
    load(mast, 1.5)  # one point a minute
    notes = tick(ship, 59)
    assert not mast.wrecked and mast.condition > 0
    notes += tick(ship, 1)
    assert mast.condition == 0.0 and mast.wrecked
    urgent = [n for n in notes if n[1] == "spar.carried_away"]
    assert len(urgent) == 1 and urgent[0][0] == "urgent" and urgent[0][3] == "mast"
    # nothing more is said of a wreck, and it carries no load
    assert tick(ship, 100) == []
    assert mast.load_kn == 0.0


def test_failure_probability_follows_the_rule():
    assert failure_probability(1.5) == 0.0
    assert failure_probability(1.0) == 0.0
    p_sub = 0.002 * 0.5**2
    assert failure_probability(2.0) == pytest.approx(1 - (1 - p_sub) ** 4)
    assert failure_probability(2.0, dt=0.25) == pytest.approx(p_sub)
    assert failure_probability(2.5) > failure_probability(2.0) > failure_probability(1.6) > 0


def test_probability_at_a_fixed_seed_gives_a_known_tick():
    ship = minimal_ship()
    halyard = ship.lines["topsail.yard.halyard"]
    ship.sails["topsail"].state = SailState.SET
    load(halyard, 2.0)
    p = failure_probability(2.0)
    # the part draws one number per tick; it parts on the first draw under p
    oracle = random.Random(42)
    expected = 1
    while oracle.random() >= p:
        expected += 1
    stream = random.Random(42)
    parted_at = None
    for t in range(1, 20000):
        apply_strain(ship, 1.0, stream)
        if halyard.state is LineState.PARTED:
            parted_at = t
            break
    assert parted_at == expected
    assert ship.sails["topsail"].state is SailState.IN_THE_GEAR
    notes = ship.drain_notes()
    assert [n for n in notes if n[1] == "line.parted"][0][2] == (
        "Topsail yard halyard parted; the yard came down on the cap "
        "and the topsail hangs in the gear."
    )


def test_mean_time_to_failure_matches_the_rule():
    ratio = 2.5
    p = failure_probability(ratio)  # about 0.008 per tick
    ticks = []
    for seed in range(200):
        ship = minimal_ship()
        mast = ship.spars["mast"]
        load(mast, ratio)
        stream = random.Random(seed)
        t = 0
        while not mast.wrecked:
            t += 1
            apply_strain(ship, 1.0, stream)
        ticks.append(t)
    mean = statistics.mean(ticks)
    assert abs(mean - 1 / p) < 0.2 * (1 / p), mean


def test_the_ship_rng_stream_is_used_when_present():
    ship = minimal_ship()
    ship.extra["rng"] = Rng(7)
    mast = ship.spars["mast"]
    load(mast, 2.2)
    t = 0
    while not mast.wrecked:
        t += 1
        apply_strain(ship, 1.0, random.Random(0))  # the passed stream is ignored
    oracle = Rng(7).stream("strain")
    expected = 1
    while oracle.random() >= failure_probability(2.2):
        expected += 1
    assert t == expected
    assert ship.extra["rng"].stream_names() == ["strain"]


def test_same_seed_same_outcome():
    def drive(seed):
        ship = minimal_ship()
        ship.extra["rng"] = Rng(seed)
        load(ship.spars["mast"], 1.9)
        load(ship.lines["topsail.yard.halyard"], 2.1)
        ship.sails["topsail"].state = SailState.SET
        return tick(ship, 3000)

    assert drive(5) == drive(5)
    assert drive(5) != drive(6)


# ---------------------------------------------------------------------------
# consequences on the reference ships
# ---------------------------------------------------------------------------


def test_parted_halyard_drops_the_yard_and_the_sail_hangs_in_the_gear():
    ship, wind = frigate_with_wind(["fore.topsail", "main.topsail"])
    halyard = ship.lines["fore.topsail.yard.halyard"]
    assert halyard.load_kn > 0
    halyard.condition = 0.0
    load(halyard, 1.2)
    notes = tick(ship, 1)
    assert halyard.state is LineState.PARTED
    assert ship.sails["fore.topsail"].state is SailState.IN_THE_GEAR
    (note,) = [n for n in notes if n[1] == "line.parted"]
    assert note[0] == "urgent" and note[3] == "fore.topsail.yard.halyard"
    assert note[2] == (
        "Fore topsail yard halyard parted; the yard came down on the cap "
        "and the fore topsail hangs in the gear."
    )
    assert note[4]["affected"] == ["fore.topsail"]
    # no drive from a sail in the gear, and the parted line takes no load
    compute_sail_forces(ship, wind)
    assert ship.sails["fore.topsail"].force_kn == 0.0
    tick(ship, 1)
    assert halyard.load_kn == 0.0
    # it cannot be set again: the hoist goes via the parted halyard
    runner = Runner(ship)
    runner.start(ship, "set_square", "fore.topsail")
    for _ in range(600):
        runner.step(ship, 1.0, wind)
    assert ship.sails["fore.topsail"].state is not SailState.SET
    assert any("halyard is parted" in n[2] for n in ship.drain_notes())


def test_parted_peak_halyard_drops_the_gaff():
    ship = load_ship(SCHOONER)
    ship.sails["main.sail"].state = SailState.SET
    peak = ship.lines["main.gaff.peak_halyard"]
    peak.condition = 0.0
    load(peak, 1.1)
    notes = tick(ship, 1)
    assert ship.sails["main.sail"].state is SailState.IN_THE_GEAR
    assert texts(notes)[-1] == (
        "Main gaff peak halyard parted; the gaff came down and the mainsail hangs in the brails."
    )


def test_parted_jib_halyard_brings_the_sail_down():
    ship = load_ship(FRIGATE)
    ship.sails["jib"].state = SailState.SET
    halyard = ship.lines["jib.halyard"]
    halyard.condition = 0.0
    load(halyard, 1.1)
    notes = tick(ship, 1)
    assert ship.sails["jib"].state is SailState.IN_THE_GEAR
    assert texts(notes)[-1] == "Jib halyard parted; the jib came down in a heap."


def test_parted_sheet_frees_the_sail_until_it_is_set_again():
    ship, wind = frigate_with_wind(["main.topsail"])
    sail = ship.sails["main.topsail"]
    yard = ship.spars["main.topsail.yard"]
    topmast = ship.spars["main.topmast"]
    drawing_thrust = sail.thrust_kn
    assert drawing_thrust > 0
    sheet = ship.lines["main.topsail.sheet.larboard"]
    sheet.condition = 0.0
    load(sheet, 1.1)
    notes = tick(ship, 1)
    assert sheet.state is LineState.PARTED
    assert sail.state is SailState.LOOSED
    assert "main.topsail" in strain_state(ship).flogging
    (note,) = [n for n in notes if n[1] == "line.parted"]
    assert note[0] == "urgent"
    assert note[2] == (
        "Larboard main topsail sheet parted; the main topsail flogging itself to ribbons."
    )
    # flogging: no drive, a fifth of the cloth, and the yard loaded double that
    compute_sail_forces(ship, wind)
    assert sail.thrust_kn == 0.0 and yard.load_kn == 0.0
    apply_strain(ship, 1.0)
    assert sail.area_effective_m2 == pytest.approx(0.2 * sail.area_m2)
    assert sail.force_kn > 0
    assert yard.load_kn == pytest.approx(2.0 * sail.force_kn)
    assert topmast.load_kn == pytest.approx(2.0 * sail.force_kn)
    # setting the sail sheets it home again and the flogging stops
    runner = Runner(ship)
    runner.start(ship, "set_square", "main.topsail")
    for _ in range(600):
        runner.step(ship, 1.0, wind)
    assert sail.state is SailState.SET
    compute_sail_forces(ship, wind)
    apply_strain(ship, 1.0)
    assert "main.topsail" not in strain_state(ship).flogging
    assert sail.thrust_kn == pytest.approx(drawing_thrust, rel=0.05)


def test_parted_brace_lets_the_yard_swing_to_the_wind():
    ship, wind = frigate_with_wind(["main.topsail"])
    sail = ship.sails["main.topsail"]
    yard = ship.spars["main.topsail.yard"]
    drawing_thrust = sail.thrust_kn
    assert drawing_thrust > 0
    brace = ship.lines["main.topsail.yard.brace.larboard"]
    brace.condition = 0.0
    load(brace, 1.1)
    notes = tick(ship, 1)
    assert brace.state is LineState.PARTED
    (note,) = [n for n in notes if n[1] == "line.parted"]
    assert note[0] == "urgent"
    assert note[2] == (
        "Larboard main topsail yard brace parted; the main topsail yard swung round to the wind."
    )
    # the chord lies along the apparent wind: 70° on the starboard bow -> braced 20° for it
    awa = ship.dyn.apparent_wind_angle
    assert yard.brace_angle == pytest.approx(math.pi / 2 - abs(awa))
    assert yard.brace_angle > 0
    compute_sail_forces(ship, wind)
    assert abs(sail.thrust_kn) < 0.1 * drawing_thrust
    # it keeps following the wind, on either tack, and cannot go past the rigging
    ship.dyn.apparent_wind_angle = -math.radians(30)
    apply_strain(ship, 1.0)
    assert yard.brace_angle == pytest.approx(-math.radians(60))
    ship.dyn.apparent_wind_angle = math.radians(150)
    apply_strain(ship, 1.0)
    assert yard.brace_angle == pytest.approx(math.radians(60))
    ship.dyn.apparent_wind_angle = math.radians(3)
    apply_strain(ship, 1.0)
    assert yard.brace_angle == pytest.approx(S.SWUNG_YARD_MAX)


def test_parted_stay_brings_its_staysail_down():
    ship = load_ship(FRIGATE)
    ship.sails["flying_jib"].state = SailState.SET
    stay = ship.lines["flying_jib.stay"]
    stay.condition = 0.0
    load(stay, 1.1)
    notes = tick(ship, 1)
    assert ship.sails["flying_jib"].state is SailState.IN_THE_GEAR
    assert texts(notes)[-1] == "Flying jib stay parted; the flying jib came down with it."


def test_carried_away_spar_wrecks_everything_above_it():
    ship, wind = frigate_with_wind(
        ["fore.topsail", "fore.topgallant", "fore.royal", "main.topsail"], knots=20.0
    )
    before = compute_sail_forces(ship, wind)
    mast = ship.spars["fore.topgallant_mast"]
    assert mast.load_kn > 0
    mast.condition = 0.0
    load(mast, 1.1)
    notes = tick(ship, 1)
    assert mast.wrecked
    wrecked = {p.id for p in ship.parts.values() if p.wrecked}
    assert {
        "fore.topgallant_mast",
        "fore.royal_mast",
        "fore.topgallant.yard",
        "fore.royal.yard",
        "fore.topgallant",
        "fore.royal",
        "fore.topgallant.yard.halyard",
        "fore.royal.sheet.larboard",
        "fore.topgallant.studdingsail_boom.starboard",
    } <= wrecked
    assert not ship.spars["fore.topmast"].wrecked
    assert not ship.sails["fore.topsail"].wrecked
    (note,) = [n for n in notes if n[1] == "spar.carried_away"]
    assert note[0] == "urgent" and note[3] == "fore.topgallant_mast"
    assert note[2].startswith(
        "Fore topgallant mast carried away; the fore topgallant and fore royal, with the "
    )
    assert "fore royal mast" in note[2] and note[2].endswith("hanging to leeward.")
    assert set(note[4]["wrecked"]) == wrecked - {"fore.topgallant_mast"}
    # the wrecked sails give no force; the wreck adds windage (three times a furled sail's)
    after = compute_sail_forces(ship, wind)
    assert ship.sails["fore.topgallant"].force_kn == 0.0
    assert ship.sails["fore.royal"].force_kn == 0.0
    assert ship.sails["fore.topsail"].force_kn > 0
    assert after.windage_drag_n > before.windage_drag_n
    assert after.thrust_n < before.thrust_n
    # the wreck is not judged again and carries no load
    assert tick(ship, 100) == []
    assert mast.load_kn == 0.0 and ship.spars["fore.royal.yard"].load_kn == 0.0
    # and nothing can be set on it, even were the hands to get the cloth in
    runner = Runner(ship)
    with pytest.raises(OrderError, match="set already"):
        runner.start(ship, "set_square", "fore.royal")
    ship.sails["fore.royal"].state = SailState.IN_THE_GEAR
    with pytest.raises(OrderError, match="wrecked"):
        runner.start(ship, "set_square", "fore.royal")
    assert strain_state(ship).snapshot()["carried_away"] == ["fore.topgallant_mast"]


def test_carried_away_yard_names_its_sail():
    ship, _ = frigate_with_wind(["main.royal"])
    yard = ship.spars["main.royal.yard"]
    yard.condition = 0.0
    load(yard, 1.1)
    notes = tick(ship, 1)
    assert texts(notes)[-1] == (
        "Main royal yard carried away in the slings; the main royal hanging to leeward."
    )
    assert ship.sails["main.royal"].wrecked and ship.sails["main.royal"].is_set is False


def test_sail_blows_out_over_one_point_eight_of_its_cloth():
    ship, wind = frigate_with_wind(["main.royal"])
    sail = ship.sails["main.royal"]
    load(sail, 1.79)
    notes = tick(ship, 1)
    assert sail.state is SailState.SET and kinds(notes) == ["strain.warning"]
    load(sail, 1.81)
    notes = tick(ship, 1)
    assert sail.state is SailState.BLOWN_OUT
    (note,) = [n for n in notes if n[1] == "sail.blown_out"]
    assert note[0] == "urgent" and note[3] == "main.royal"
    assert note[2] == "Main royal split and blew out of the bolt-ropes."
    compute_sail_forces(ship, wind)
    assert sail.force_kn == 0.0 and sail.area_effective_m2 == 0.0
    assert tick(ship, 10) == []
    runner = Runner(ship)
    with pytest.raises(OrderError, match="blown out"):
        runner.start(ship, "set_square", "main.royal")


def test_sail_below_one_point_eight_only_wears_without_a_stream():
    ship, _ = frigate_with_wind(["main.royal"])
    sail = ship.sails["main.royal"]
    load(sail, 1.7)
    tick(ship, 60)
    assert sail.state is SailState.SET
    assert sail.condition == pytest.approx(100.0 - 1.4)


def test_sent_down_spars_carry_no_load():
    ship, wind = frigate_with_wind(["main.topsail", "main.topgallant", "main.royal"], knots=30.0)
    tg_mast = ship.spars["main.topgallant_mast"]
    assert tg_mast.load_kn > 0
    tg_mast.sent_down = True
    compute_sail_forces(ship, wind)
    assert tg_mast.load_kn == 0.0
    assert ship.sails["main.topgallant"].force_kn == 0.0
    # even a load written on it by hand is wiped, and it is never judged
    tg_mast.load_kn = 100 * tg_mast.rating_kn
    tg_mast.condition = 0.0
    notes = tick(ship, 5)
    assert tg_mast.load_kn == 0.0 and not tg_mast.wrecked
    assert [n for n in notes if n[3] == "main.topgallant_mast"] == []


# ---------------------------------------------------------------------------
# truth 9 on the reference ships, through the World
# ---------------------------------------------------------------------------


def sailing_world(path, group, knots, seed=1, brace_deg=58.0, awa_true_deg=90.0, gusty=False):
    """A world with the ship on a reach (wind on the larboard beam) under the
    named group of sails, with the strain stream wired as the session
    composer will wire it. The yards are braced sharp up: with package 10's
    curves (no lift under ten degrees of attack, the peak at thirty-five) a
    beam reach wants the yards nearly sharp up, and at the 40 degrees this
    helper used before the sails all but shiver and load nothing."""
    scenario = Scenario(
        wind_from_deg=90.0,
        wind_speed_kn=knots,
        gustiness=0.3 if gusty else 0.0,
        variability=0.3 if gusty else 0.0,
        ship_heading_deg=(90.0 + awa_true_deg) % 360,
    )
    world = make_world(seed, path, scenario)
    ship = world.ship
    ship.extra["rng"] = world.rng
    set_sails(ship, ship.groups[group], brace_deg=-brace_deg, sheet_deg=35.0)
    return world


def carried_away(world):
    return [e for e in world.log if e.kind in CARRIED_AWAY_KINDS]


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_nothing_carries_away_in_twenty_knots_under_plain_sail(path):
    world = sailing_world(path, "plain sail", 20.0)
    world.run(20 * 60)
    assert carried_away(world) == []
    assert world.log.of_kind("strain.warning") == []
    assert all(p.condition == 100.0 for p in world.ship.parts.values())


def test_something_carries_away_in_thirty_five_knots_under_all_sail():
    world = sailing_world(FRIGATE, "all sail", 35.0)
    world.run(20 * 60)
    events = carried_away(world)
    assert events, "nothing carried away in 35 knots under all sail"
    assert any(e.kind in {"spar.carried_away", "sail.blown_out"} for e in events)
    assert all(e.severity.value == "urgent" for e in events)
    assert world.log.of_kind("strain.warning")  # the log complained first
    first = world.log.of_kind("strain.warning")[0]
    assert first.tick < events[0].tick
    # the wreck is recorded for the snapshot and a later `cut away`
    snap = strain_state(world.ship).snapshot()
    assert snap["carried_away"] or snap["blown_out"]
    assert any(p.wrecked for p in world.ship.parts.values()) or snap["blown_out"]


def test_the_log_is_deterministic_with_gear_carrying_away():
    a = sailing_world(FRIGATE, "all sail", 35.0, seed=3, gusty=True)
    b = sailing_world(FRIGATE, "all sail", 35.0, seed=3, gusty=True)
    a.run(15 * 60)
    b.run(15 * 60)
    assert carried_away(a)
    assert a.log.digest() == b.log.digest()
    assert a.state() == b.state()
    assert a.rng.stream_names() == ["strain", "wind"]


def test_ratio_of_the_weakest_part_on_the_reference_ships():
    """Documents where the draft ratings put the reference ships (see the
    package 9 report); package 8 and 10 move these numbers."""
    world = sailing_world(FRIGATE, "plain sail", 20.0)
    world.run(10 * 60)
    worst = max(p.strain_ratio for p in world.ship.parts.values())
    assert worst < 1.0
    world = sailing_world(FRIGATE, "all sail", 35.0)
    world.ship.extra.pop("rng")  # judge the loads without anything carrying away
    peak = {}
    for _ in range(5 * 60):
        world.tick()
        for p in world.ship.parts.values():
            peak[p.id] = max(peak.get(p.id, 0.0), p.strain_ratio)
    assert peak["fore.topgallant_mast"] > 1.5
    assert peak["main.royal.yard"] > 1.5
