"""Package 19: the evolution catalogue to forty (spec M3 §6).

Every file loads and carries its crew line and source; the twenty milestone 2
files keep their durations; each new evolution runs on the ship that has the
parts and leaves the states the spec says; the orders reach the right
evolution on both ships; and the gale of gate M2 item 9 loses nothing when the
topgallant masts are sent down at once (the mechanism behind truth 23).

Sail and spar work is run with the runner alone and a physics that does
nothing, as in tests/test_evolutions.py; the ship-handling scripts (box-haul,
lie a-try, scud, back and fill) and the gale are run through the real world.
"""

from __future__ import annotations

import math
import random
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail import orders, units
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.crew import bill, hands
from freesail.evolutions import EVOLUTIONS, Runner
from freesail.evolutions.scripts import SCRIPTS, spare_sails
from freesail.physics.sails import _lateral_offset, compute_sail_forces
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from freesail.ship.stub import OrderError

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
EVOLUTION_DIR = Path(__file__).resolve().parents[1] / "data" / "evolutions"

NEW = [
    "send_down_topgallant_masts",
    "sway_up_topgallant_masts",
    "send_down_topgallant_yards",
    "cross_topgallant_yards",
    "strike_topmasts",
    "fid_topmasts",
    "rig_out_studdingsail_boom",
    "rig_in_studdingsail_boom",
    "unbend_sail",
    "bend_sail",
    "shift_sail",
    "goose_wing",
    "boxhaul",
    "wear_short_round",
    "lie_a_try",
    "scud",
    "back_and_fill",
    "loose_sails_to_dry",
    "furl_all",
]

# The milestone 2 timings, frozen (spec M3 §1): step durations, or a script's timing.
M2_TIMINGS = {
    "brace": [45.0],
    "fill_away": {
        "brace_s": 45.0,
        "helm_deg": 20.0,
        "fill_off_deg": 55.0,
        "fall_off_timeout_s": 180.0,
    },
    "furl_gaff": [90.0, 120.0],
    "furl_jibheaded": [45.0, 90.0],
    "furl_square": [60.0, 150.0],
    "heave_to": {"brace_s": 45.0, "helm_deg": 15.0},
    "reef_gaff": [45.0, 180.0, 60.0],
    "reef_square": [60.0, 150.0, 90.0],
    "set_gaff": [60.0, 120.0, 30.0],
    "set_jibheaded": [30.0, 60.0, 15.0],
    "set_square": [90.0, 60.0, 120.0, 30.0],
    "set_studding": [90.0, 120.0, 30.0],
    "shake_out_gaff": [30.0, 120.0, 60.0],
    "shake_out_square": [45.0, 120.0, 90.0],
    "tack": {
        "brace_s": 45.0,
        "stays_timeout_s": 180.0,
        "min_speed_kn": 0.8,
        "steady_deg": 5.0,
        "steady_timeout_s": 300.0,
    },
    "take_in_gaff": [90.0],
    "take_in_jibheaded": [45.0],
    "take_in_square": [60.0, 45.0],
    "take_in_studding": [90.0, 60.0],
    "wear": {
        "brace_rate_deg_s": 0.35,
        "wear_timeout_s": 900.0,
        "wear_estimate_s": 480.0,
        "steady_deg": 5.0,
    },
}

# Steps that are work aloft in the milestone 2 files (spec M3 §3.3). Work on the jib-boom
# is not counted aloft: it moved truths 12 and 17 through the crew factor.
ALOFT_STEPS = {
    "set_square": {"loose"},
    "furl_square": {"furl"},
    "reef_square": {"reef"},
    "shake_out_square": {"shake_out"},
    "furl_gaff": {"furl"},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_wind(from_deg: float = 0.0, knots: float = 3.0) -> Wind:
    params = WindParams.from_nautical(from_deg, knots, gustiness=0.0, variability=0.0)
    return Wind(params, random.Random(0))


def run(runner, ship, wind, max_ticks: int = 6000) -> list:
    """Tick the runner (no physics) until nothing is in progress; the notes."""
    notes = []
    ticks = 0
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return notes


def kinds(notes) -> list[str]:
    return [n[1] for n in notes]


def texts(notes) -> list[str]:
    return [n[2] for n in notes]


def bare(path: str):
    ship = load_ship(path)
    return ship, Runner(ship), make_wind()


def evolution_ids(ship) -> list[str]:
    return [i.evo.id for i in ship.extra["evolutions"].instances]


def world(path: str, knots: float, heading: float, speed: float = 4.0):
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
    )
    return make_world(7, path, scenario)


def ticks(w, n: int) -> None:
    for _ in range(n):
        w.tick()


def events(w, kind: str) -> list:
    return [e for e in w.log if e.kind == kind]


def off_wind(w) -> float:
    return abs(math.degrees(units.wrap_pi(w.ship.dyn.heading - w.wind.direction_from)))


# ---------------------------------------------------------------------------
# The files
# ---------------------------------------------------------------------------


def test_the_catalogue_reaches_forty_and_every_file_loads():
    assert len(EVOLUTIONS) >= 39  # forty-one less the two routine orders (spec M3 §6)
    for eid in NEW:
        evo = EVOLUTIONS[eid]
        assert "Luce" in evo.source, eid
        assert "hands" in evo.crew, eid
        assert evo.steps or evo.script in SCRIPTS, eid
    for eid, evo in EVOLUTIONS.items():
        assert "hands" in evo.crew, f"{eid} has no hands in its crew line"
        hands = evo.crew["hands"]
        assert hands == "all" or isinstance(hands, int), eid
        if hands == "all":
            assert evo.crew.get("stations") == ["all hands"], eid


def test_milestone_2_timings_are_unchanged():
    for eid, want in M2_TIMINGS.items():
        evo = EVOLUTIONS[eid]
        if isinstance(want, list):
            assert [s.duration_s for s in evo.steps] == want, eid
        else:
            assert evo.timing == want, eid


def test_aloft_flags_are_on_the_steps_aloft():
    for path in sorted(EVOLUTION_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        aloft = {s["do"] for s in data.get("steps") or [] if s.get("aloft")}
        assert aloft == ALOFT_STEPS.get(data["id"], aloft), data["id"]
        for step in data.get("steps") or []:
            assert isinstance(step.get("aloft", False), bool), data["id"]
    for eid in ALOFT_STEPS:
        assert ALOFT_STEPS[eid], eid
    # scripts name their aloft phases in params, and each is a phase with a timing
    for eid in NEW:
        evo = EVOLUTIONS[eid]
        for phase in evo.params.get("aloft") or []:
            assert f"{phase}_s" in evo.timing, (eid, phase)


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_the_new_crew_lines_fit_one_watch_of_either_ship(path):
    """Each new evolution that asks for the watch gets every hand it asks for at the
    rating it asks for, from either watch, by day or by night, on either ship: so it
    runs at its file's pace (the compatibility rule for the new files)."""
    w = make_world(7, path, Scenario())
    crew = w.ship.extra["crew"]
    for hour in (1, 4, 9, 13, 21):
        deck = bill.on_deck(crew, datetime(1805, 6, 1, hour, 0, 0))
        for eid in NEW:
            evo = EVOLUTIONS[eid]
            want = hands.CrewRequest.from_mapping(evo.crew)
            if want.all_hands or want.wants_none:
                continue
            aloft = any(step.aloft for step in evo.steps)
            for mast in (None, "fore", "main", "mizzen"):
                for sailor in crew.sailors:
                    sailor.at = None
                got = hands.request(crew, deck, "x", want, mast, aloft=aloft)
                assert got.outcome == hands.ENOUGH, (path, hour, eid, got.got, got.wanted)
                assert hands.crew_factor(got, want, aloft) == 1.0, (path, hour, eid)


# ---------------------------------------------------------------------------
# The routine's two
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Studding sail booms
# ---------------------------------------------------------------------------


def test_rigging_a_boom_in_and_out_gates_the_studding_sail():
    ship, runner, wind = bare(FRIGATE)
    boom = ship.spars["fore.topmast.studdingsail_boom.starboard"]
    sail = "fore.topmast.studdingsail.starboard"
    assert boom.rigged_out  # as milestone 2 had them
    runner.start(ship, "set_square", "fore.topsail")
    run(runner, ship, wind)
    with pytest.raises(OrderError, match="rigged out already"):
        runner.start(ship, "rig_out_studdingsail_boom", boom.id)
    runner.start(ship, "rig_in_studdingsail_boom", boom.id)
    notes = run(runner, ship, wind)
    assert not boom.rigged_out
    assert "Rigged in the starboard fore topmast studdingsail boom." in texts(notes)
    with pytest.raises(OrderError, match="boom is rigged in; rig it out first"):
        runner.start(ship, "set_studding", sail)
    runner.start(ship, "rig_out_studdingsail_boom", boom.id)
    run(runner, ship, wind)
    assert boom.rigged_out
    runner.start(ship, "set_studding", sail)
    run(runner, ship, wind)
    assert ship.sails[sail].is_set
    with pytest.raises(OrderError, match="studding sail set; take it in first"):
        runner.start(ship, "rig_in_studdingsail_boom", boom.id)


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_rig_orders_take_the_boom_or_its_sail(path):
    ship = make_ship(path)
    orders.handle(ship, "rig in the starboard fore topmast studdingsail boom")
    assert evolution_ids(ship) == ["rig_in_studdingsail_boom"]
    orders.handle(ship, "rig in the larboard fore topmast studdingsail")
    assert [i.subject_id for i in ship.extra["evolutions"].instances] == [
        "fore.topmast.studdingsail_boom.starboard",
        "fore.topmast.studdingsail_boom.larboard",
    ]
    with pytest.raises(OrderError, match="You rig out studding sail booms"):
        orders.handle(ship, "rig out the fore topsail")


def test_the_schooner_has_no_lower_studdingsail_boom_and_says_so():
    ship = make_ship(SCHOONER)
    with pytest.raises(OrderError, match="no such part as the fore lower studdingsail boom"):
        orders.handle(ship, "rig out the starboard fore lower studdingsail boom")


# ---------------------------------------------------------------------------
# Goose-winging
# ---------------------------------------------------------------------------


def test_goose_wing_hauls_up_the_lee_clew_and_set_hauls_it_aboard():
    ship, runner, wind = bare(FRIGATE)
    runner.start(ship, "set_square", "main.course")
    run(runner, ship, wind)
    runner.start(ship, "goose_wing", "main.course")
    notes = run(runner, ship, wind)
    assert ship.sails["main.course"].state is SailState.GOOSE_WINGED
    assert "sail.goose_winged" in kinds(notes)
    with pytest.raises(OrderError, match="Only a course or a topsail"):
        runner.start(ship, "goose_wing", "main.royal")
    runner.start(ship, "set_square", "main.course")
    run(runner, ship, wind)
    assert ship.sails["main.course"].state is SailState.SET
    runner.start(ship, "goose_wing", "main.course")
    run(runner, ship, wind)
    runner.start(ship, "take_in_square", "main.course")
    run(runner, ship, wind)
    assert ship.sails["main.course"].state is SailState.IN_THE_GEAR
    # Luce's own case: from the gear, the weather clew hauled aboard
    runner.start(ship, "goose_wing", "main.course")
    notes = run(runner, ship, wind)
    assert ship.sails["main.course"].state is SailState.GOOSE_WINGED
    assert any("weather clew" in t for t in texts(notes))


def test_a_goose_winged_sail_draws_half_its_area_out_to_windward():
    ship = load_ship(FRIGATE)
    wind = make_wind(0.0, 15.0)
    ship.dyn.heading = units.deg_to_rad(270.0)  # wind on the starboard beam
    sail = ship.sails["fore.course"]
    sail.state = SailState.SET
    compute_sail_forces(ship, wind)
    full_area, full_side = sail.area_effective_m2, sail.side_force_kn
    sail.state = SailState.GOOSE_WINGED
    forces = compute_sail_forces(ship, wind)
    assert sail.area_effective_m2 == pytest.approx(0.5 * full_area)
    assert sail.side_force_kn == pytest.approx(0.5 * full_side, rel=1e-6)
    # its centre lies a quarter of the yard out to windward, the side still set: its
    # thrust there turns her head away from the wind, which is what Luce wants of it
    yard = ship.spars["fore.yard"]
    assert _lateral_offset(ship, sail, units.deg_to_rad(90.0)) == pytest.approx(
        0.25 * yard.length_m
    )
    assert _lateral_offset(ship, sail, units.deg_to_rad(-90.0)) == pytest.approx(
        -0.25 * yard.length_m
    )
    assert forces.thrust_n != 0.0
    assert sail.load_kn > 0.0


# ---------------------------------------------------------------------------
# Bending, unbending and shifting sails
# ---------------------------------------------------------------------------


def test_unbend_and_bend_keep_the_count_of_spare_sails():
    ship, runner, wind = bare(FRIGATE)
    assert spare_sails(ship) == 3  # no crew section in the ship file: the default
    runner.start(ship, "unbend_sail", "fore.royal")
    notes = run(runner, ship, wind)
    assert ship.sails["fore.royal"].state is SailState.UNBENT
    assert spare_sails(ship) == 4  # a sound sail goes down to the sail room
    assert "Unbent the fore royal; 4 spare sails in the sail room." in texts(notes)
    with pytest.raises(OrderError, match="unbent; bend a sail to the yard first"):
        runner.start(ship, "set_square", "fore.royal")
    runner.start(ship, "bend_sail", "fore.royal", {"sail": "fore.royal"})
    notes = run(runner, ship, wind)
    assert ship.sails["fore.royal"].state is SailState.FURLED
    assert spare_sails(ship) == 3
    assert "sail.bent" in kinds(notes)
    with pytest.raises(OrderError, match="bent already"):
        runner.start(ship, "bend_sail", "fore.royal")


def test_shift_sail_uses_a_spare_and_refuses_when_none_are_left():
    ship, runner, wind = bare(FRIGATE)
    ship.sails["fore.royal"].state = SailState.BLOWN_OUT
    ship.sails["main.royal"].state = SailState.BLOWN_OUT
    ship.extra["spare_sails"] = 1
    runner.start(ship, "shift_sail", "fore.royal")
    notes = run(runner, ship, wind)
    assert ship.sails["fore.royal"].state is SailState.FURLED
    assert spare_sails(ship) == 0
    assert "sail.shifted" in kinds(notes)
    assert any("0 spare sails left" in t for t in texts(notes))
    with pytest.raises(OrderError, match="There is no spare sail left in the sail room"):
        runner.start(ship, "shift_sail", "main.royal")
    with pytest.raises(OrderError, match="set; take it in before shifting it"):
        ship.sails["mizzen.royal"].state = SailState.SET
        runner.start(ship, "shift_sail", "mizzen.royal")


def test_spare_sails_come_from_the_crew_section_when_the_ship_has_one():
    ship = load_ship(FRIGATE)
    ship.spec = SimpleNamespace(crew=SimpleNamespace(stores={"spare_sails": 5}))
    assert spare_sails(ship) == 5
    ship = load_ship(FRIGATE)
    ship.spec = SimpleNamespace(crew=SimpleNamespace(stores=SimpleNamespace(spare_sails=2)))
    assert spare_sails(ship) == 2


def test_sail_orders_for_bending_on_both_ships():
    ship = make_ship(FRIGATE)
    ship.sails["fore.royal"].state = SailState.BLOWN_OUT
    orders.handle(ship, "shift the fore royal")
    assert evolution_ids(ship) == ["shift_sail"]
    orders.handle(ship, "unbend the main royal")
    ship.sails["main.course"].state = SailState.SET
    orders.handle(ship, "goose-wing the main course")
    assert evolution_ids(ship)[1:] == ["unbend_sail", "goose_wing"]
    with pytest.raises(OrderError, match="only a square sail is bent"):
        orders.handle(ship, "bend the jib")
    with pytest.raises(OrderError, match="no clews to goose-wing"):
        orders.handle(ship, "goose wing the spanker")
    schooner = make_ship(SCHOONER)
    schooner.sails["fore.topsail"].state = SailState.SET
    orders.handle(schooner, "goose wing the topsail")
    assert evolution_ids(schooner) == ["goose_wing"]
    with pytest.raises(OrderError, match="no such part as the main course"):
        orders.handle(schooner, "goose-wing the main course")


# ---------------------------------------------------------------------------
# Spars up and down
# ---------------------------------------------------------------------------


def test_send_down_and_sway_up_the_topgallant_masts_on_the_frigate():
    ship, runner, wind = bare(FRIGATE)
    for sid in ("fore.royal", "fore.topgallant", "flying_jib"):
        ship.sails[sid].state = SailState.SET
    runner.start(ship, "send_down_topgallant_masts", "ship")
    notes = run(runner, ship, wind)
    for mast in ("fore", "main", "mizzen"):
        for spar in ("topgallant_mast", "royal_mast", "topgallant.yard", "royal.yard"):
            assert ship.spars[f"{mast}.{spar}"].sent_down, (mast, spar)
        assert not ship.spars[f"{mast}.topmast"].sent_down
    assert ship.spars["fore.topgallant.studdingsail_boom.starboard"].sent_down
    for sid in ("fore.royal", "fore.topgallant", "flying_jib"):
        assert ship.sails[sid].state is SailState.FURLED, sid
    assert "spar.sent_down" in kinds(notes)
    assert any("Clewed up the fore topgallant" in t for t in texts(notes))
    # nothing on them can be set; a spar sent down carries no load
    with pytest.raises(OrderError, match="wrecked or sent down"):
        runner.start(ship, "set_square", "fore.royal")
    with pytest.raises(OrderError, match="sent down already"):
        runner.start(ship, "send_down_topgallant_masts", "ship")
    runner.start(ship, "sway_up_topgallant_masts", "ship")
    notes = run(runner, ship, wind)
    assert not any(s.sent_down for s in ship.spars.values())
    assert "spar.swayed_up" in kinds(notes)
    with pytest.raises(OrderError, match="aloft already"):
        runner.start(ship, "sway_up_topgallant_masts", "ship")


def test_the_light_yards_alone():
    ship, runner, wind = bare(FRIGATE)
    runner.start(ship, "send_down_topgallant_yards", "ship")
    run(runner, ship, wind)
    assert ship.spars["main.royal.yard"].sent_down and ship.spars["main.topgallant.yard"].sent_down
    assert not ship.spars["main.topgallant_mast"].sent_down
    assert ship.sails["flying_jib"].state is SailState.FURLED  # on the mast's stay: stands
    runner.start(ship, "cross_topgallant_yards", "ship")
    run(runner, ship, wind)
    assert not any(s.sent_down for s in ship.spars.values())


def test_topmasts_are_struck_only_with_the_topgallant_masts_down_and_no_sail_on_them():
    ship, runner, wind = bare(FRIGATE)
    with pytest.raises(OrderError, match="Send down the topgallant masts first"):
        runner.start(ship, "strike_topmasts", "ship")
    runner.start(ship, "send_down_topgallant_masts", "ship")
    run(runner, ship, wind)
    ship.sails["main.topsail"].state = SailState.SET
    with pytest.raises(OrderError, match="main topsail is set; take it in before striking"):
        runner.start(ship, "strike_topmasts", "ship")
    ship.sails["main.topsail"].state = SailState.IN_THE_GEAR
    runner.start(ship, "strike_topmasts", "ship")
    notes = run(runner, ship, wind)
    assert all(ship.spars[f"{m}.topmast"].sent_down for m in ("fore", "main", "mizzen"))
    assert ship.spars["main.topsail.yard"].sent_down
    assert ship.sails["main.topsail"].state is SailState.FURLED
    assert "Struck the fore topmast, the main topmast and the mizzen topmast." in texts(notes)
    with pytest.raises(OrderError, match="Fid the topmasts first"):
        runner.start(ship, "sway_up_topgallant_masts", "ship")
    runner.start(ship, "fid_topmasts", "ship")
    run(runner, ship, wind)
    assert not ship.spars["main.topmast"].sent_down
    assert not ship.spars["main.topsail.yard"].sent_down
    assert ship.spars["main.topgallant_mast"].sent_down  # still on deck


def test_the_schooner_sends_down_her_one_topgallant_mast():
    ship = make_ship(SCHOONER)
    orders.handle(ship, "send down the topgallant masts")
    assert evolution_ids(ship) == ["send_down_topgallant_masts"]
    runner = ship.extra["evolutions"]
    run(runner, ship, make_wind())
    assert ship.spars["fore.topgallant_mast"].sent_down
    assert ship.spars["fore.topgallant.yard"].sent_down
    assert not ship.spars["main.topmast"].sent_down
    with pytest.raises(OrderError, match="sent down already"):
        orders.handle(ship, "send down the topgallant mast")


def test_a_ship_without_the_masts_says_what_she_has():
    ship, runner, wind = bare(SCHOONER)
    for sid in ("fore.topgallant_mast",):
        ship.spars[sid].wrecked = True  # carried away: she has none left to send down
    with pytest.raises(OrderError) as refused:
        runner.start(ship, "send_down_topgallant_masts", "ship")
    text = str(refused.value)
    assert text.startswith("She has no topgallant masts to send down; her masts are")
    assert "the fore mast, fore topmast" in text and "main mast and main topmast" in text


@pytest.mark.parametrize(
    "order, evo",
    [
        ("send down the topgallant masts", "send_down_topgallant_masts"),
        ("down topgallant masts", "send_down_topgallant_masts"),
        ("send down the topgallant yards", "send_down_topgallant_yards"),
        ("box haul", "boxhaul"),
        ("boxhaul", "boxhaul"),
        ("box-haul the ship", "boxhaul"),
        ("wear short round", "wear_short_round"),
        ("lie a-try", "lie_a_try"),
        ("lie to under the main topsail", "lie_a_try"),
        ("scud", "scud"),
        ("scud before it", "scud"),
        ("back and fill", "back_and_fill"),
        ("loose the sails to dry", "loose_sails_to_dry"),
        ("loose sails to dry", "loose_sails_to_dry"),
        ("furl all", "furl_all"),
        ("furl all sails", "furl_all"),
    ],
)
def test_whole_ship_orders_start_their_evolution(order, evo):
    ship = make_ship(FRIGATE)
    ship.sails["main.topsail"].state = SailState.SET
    ship.dyn.speed = units.knots_to_ms(4.0)
    orders.handle(ship, order)
    assert evolution_ids(ship) == [evo]


def test_sway_up_and_fid_orders_start_their_evolution():
    ship, runner, wind = bare(FRIGATE)
    runner.start(ship, "send_down_topgallant_masts", "ship")
    run(runner, ship, wind)
    orders.handle(ship, "sway up the topgallant masts")
    assert evolution_ids(ship) == ["sway_up_topgallant_masts"]
    run(runner, ship, wind)
    runner.start(ship, "send_down_topgallant_yards", "ship")
    run(runner, ship, wind)
    orders.handle(ship, "cross the topgallant yards")
    assert evolution_ids(ship) == ["cross_topgallant_yards"]
    run(runner, ship, wind)
    runner.start(ship, "send_down_topgallant_masts", "ship")
    run(runner, ship, wind)
    runner.start(ship, "strike_topmasts", "ship")
    run(runner, ship, wind)
    orders.handle(ship, "fid the topmasts")
    assert evolution_ids(ship) == ["fid_topmasts"]


# ---------------------------------------------------------------------------
# Routine sail work
# ---------------------------------------------------------------------------


def test_loose_sails_to_dry_and_furl_all():
    ship, runner, wind = bare(FRIGATE)
    ship.sails["main.topsail"].state = SailState.SET
    runner.start(ship, "loose_sails_to_dry", "ship")
    notes = run(runner, ship, wind)
    loosed = [s for s in ship.sails.values() if s.state is SailState.LOOSED]
    assert len(loosed) == 15  # every furled sail but the ten studding sails
    assert all(s.cls != "studding" for s in loosed)
    assert "Loosed 15 sails to dry." in texts(notes)
    runner.start(ship, "furl_all", "ship")
    notes = run(runner, ship, wind)
    assert all(s.state is SailState.FURLED for s in ship.sails.values())
    assert "sail.furled" in kinds(notes)
    with pytest.raises(OrderError, match="Every sail is furled already"):
        runner.start(ship, "furl_all", "ship")
    with pytest.raises(OrderError, match="Every sail is furled already"):
        orders.handle(ship, "furl all")
    ship.dyn.apparent_wind_speed = units.knots_to_ms(30.0)
    with pytest.raises(OrderError, match="It blows too hard to loose sails to dry"):
        runner.start(ship, "loose_sails_to_dry", "ship")


def test_wear_under_bare_poles_is_wear_with_no_sail_set():
    ship = make_ship(FRIGATE)
    ship.dyn.speed = units.knots_to_ms(2.0)
    orders.handle(ship, "wear under bare poles")
    assert evolution_ids(ship) == ["wear"]
    assert ship.extra["evolutions"].instances[0].params["bare_poles"] is True
    ship = make_ship(FRIGATE)
    ship.sails["fore.topsail"].state = SailState.SET
    with pytest.raises(OrderError, match=r"She has sail set \(fore topsail\)"):
        orders.handle(ship, "wear under bare poles")


# ---------------------------------------------------------------------------
# Handling the ship, with the physics
# ---------------------------------------------------------------------------


def close_hauled_frigate():
    w = world(FRIGATE, 15.0, 293.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 900)
    w.submit("keep her full")
    ticks(w, 300)
    return w


def test_box_hauling_brings_her_round_on_her_heel():
    w = close_hauled_frigate()
    assert w.ship.dyn.tack == "starboard"
    w.submit("box haul")
    least_u = 0.0
    for _ in range(900):
        w.tick()
        least_u = min(least_u, w.ship.dyn.u)
        if events(w, "ship.box_hauled"):
            break
    done = events(w, "ship.box_hauled")
    assert done, [e.text for e in w.log[-10:]]
    assert least_u < 0.0  # she made a sternboard
    assert w.ship.dyn.tack == "larboard"
    minutes = (done[0].tick - 1200) / 60.0
    assert 4.0 <= minutes <= 12.0
    assert any("Brace abox the head yards" in e.text for e in w.log)
    assert w.ship.sails["main.course"].is_set and w.ship.sails["mizzen.spanker"].is_set


def test_the_schooner_box_hauls_too():
    w = world(SCHOONER, 12.0, 300.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 800)
    w.submit("box haul")
    ticks(w, 900)
    assert events(w, "ship.box_hauled")
    assert w.ship.dyn.tack == "larboard"


def test_lying_a_try_in_a_gale_with_the_topgallant_masts_down():
    w = world(FRIGATE, 30.0, 290.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 700)
    w.submit("send down the topgallant masts")
    ticks(w, 2000)
    w.submit("lie a-try")
    ticks(w, 1500)
    assert events(w, "ship.hove_to")
    set_now = sorted(s.id for s in w.ship.sails.values() if s.is_set)
    assert set_now == ["fore.topmast_staysail", "main.topsail"]
    assert 45.0 <= off_wind(w) <= 70.0  # about five points off
    assert abs(units.ms_to_knots(w.ship.dyn.u)) < 2.5
    with pytest.raises(OrderError, match="lying to already"):
        w.ship.extra["evolutions"].start(w.ship, "lie_a_try", "ship")
    w.submit("fill away")
    ticks(w, 600)
    assert events(w, "ship.filled_away")


def test_scudding_puts_the_wind_on_the_quarter():
    w = world(FRIGATE, 30.0, 290.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 700)
    w.submit("scud")
    ticks(w, 600)
    assert events(w, "ship.scudding")
    assert 160.0 <= off_wind(w) <= 170.0
    assert not w.ship.sails["mizzen.spanker"].is_set


def test_backing_and_filling_keeps_her_place_and_leaves_her_lying_to():
    w = world(FRIGATE, 12.0, 290.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 700)
    w.submit("back and fill")
    speeds = []
    for _ in range(900):
        w.tick()
        speeds.append(units.ms_to_knots(w.ship.dyn.u))
    assert events(w, "ship.hove_to")
    assert "hove_to" in w.ship.extra
    assert max(speeds[300:]) < 4.0  # she never gets going
    backed = [e for e in w.log if e.text.startswith("Backed the main topsail")]
    filled = [e for e in w.log if e.text.startswith("Filled the main topsail")]
    assert len(backed) == 3 and len(filled) == 2


# ---------------------------------------------------------------------------
# The gale of gate M2 item 9: the mechanism behind truth 23
# ---------------------------------------------------------------------------

LOST = ("spar.carried_away", "sail.blown_out", "line.parted")


def the_gale(*first_orders: str):
    """Gate M2 item 9: the frigate, seed 7, 35 knots from north, heading west,
    all sail made and braced up, the sails trimmed every ten minutes."""
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=35.0, ship_heading_deg=270.0)
    w = make_world(7, FRIGATE, scenario)
    for text in ("make all sail", "brace up on the starboard tack", *first_orders):
        w.submit(text)
    for i in range(1800):
        if i in (600, 1200):
            w.submit("trim sails")
        w.tick()
    return w


def test_the_gale_carries_away_the_royals_without_sending_anything_down():
    w = the_gale()
    lost = [e for e in w.log if e.kind in LOST]
    assert any("royal" in (e.subject or "") for e in lost)


def test_sending_down_the_topgallant_masts_at_once_loses_nothing_in_thirty_minutes():
    w = the_gale("send down the topgallant masts")
    assert [e.text for e in w.log if e.kind in LOST] == []
    assert w.ship.spars["fore.royal.yard"].sent_down
    assert not w.ship.sails["fore.royal"].is_set
    # all hands: the sail work in hand was belayed, and the royals refused after
    belayed = [e for e in w.log if e.kind == "evolution.belayed"]
    assert any("fore topgallant" in e.text for e in belayed)
    assert any(
        e.kind == "evolution.failed" and e.text.startswith("Could not set the fore royal")
        for e in w.log
    )
    assert events(w, "spar.sent_down")
