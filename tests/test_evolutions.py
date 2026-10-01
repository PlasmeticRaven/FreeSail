"""Package 7: the evolution registry, runner and data files.

Physics is stubbed throughout. Three stub steppers stand in for it: one
that does nothing, one that turns the ship toward the ordered heading at a
fixed rate, and one that turns but loses her way. The runner is stepped
before the stub each tick, as the World will step it before the physics.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable

import pytest
import yaml

from freesail import units
from freesail.evolutions import EVOLUTIONS, Runner, expr, part_name, registry, weather_factor
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship
from freesail.ship.parts import HelmMode, LineState, SailState
from freesail.ship.stub import OrderError

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SHIPS = [FRIGATE, SCHOONER]

REQUIRED = [
    "set_square",
    "take_in_square",
    "furl_square",
    "reef_square",
    "shake_out_square",
    "set_gaff",
    "take_in_gaff",
    "reef_gaff",
    "shake_out_gaff",
    "set_jibheaded",
    "take_in_jibheaded",
    "set_studding",
    "take_in_studding",
    "brace",
    "tack",
    "wear",
    "heave_to",
    "fill_away",
]

Stepper = Callable[..., None]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_wind(from_deg: float = 90.0, knots: float = 3.0) -> Wind:
    params = WindParams.from_nautical(from_deg, knots, gustiness=0.0, variability=0.0)
    return Wind(params, random.Random(0))


def still(ship, dt, wind) -> None:
    """Physics that does nothing."""


def deck_reading(ship, wind) -> None:
    ship.dyn.apparent_wind_angle = units.relative_bearing(ship.dyn.heading, wind.direction_from)


def turner(rate_deg_s: float, speed_kn: float = 5.0) -> Stepper:
    """Physics that turns the ship toward the ordered heading at a fixed rate
    and keeps her speed, reporting the true wind as the apparent wind."""

    def stepper(ship, dt, wind) -> None:
        d = ship.dyn
        error = units.wrap_pi(d.target_heading - d.heading)
        step = units.deg_to_rad(rate_deg_s) * dt
        turn = error if abs(error) <= step else math.copysign(step, error)
        d.heading = units.wrap_2pi(d.heading + turn)
        d.speed = units.knots_to_ms(speed_kn)
        deck_reading(ship, wind)

    return stepper


def staller(rate_deg_s: float, dies_in_s: float) -> Stepper:
    """Physics that turns but loses all way over `dies_in_s` seconds."""
    turn = turner(rate_deg_s)
    start = {}

    def stepper(ship, dt, wind) -> None:
        speed0 = start.setdefault("speed", ship.dyn.speed)
        turn(ship, dt, wind)
        start["t"] = start.get("t", 0.0) + dt
        ship.dyn.speed = max(0.0, speed0 * (1 - start["t"] / dies_in_s))

    return stepper


def hangs_in_stays(rate_deg_s: float, at_deg: float = 20.0, dies_in_s: float = 0.0) -> Stepper:
    """Physics that turns until her head is `at_deg` off the wind, then hangs; with
    `dies_in_s` her way then dies away over that many seconds (package 32e)."""
    turn = turner(rate_deg_s)
    hung = {}

    def stepper(ship, dt, wind) -> None:
        rel = units.relative_bearing(ship.dyn.heading, wind.direction_from)
        if abs(rel) > units.deg_to_rad(at_deg):
            turn(ship, dt, wind)
        elif dies_in_s > 0:
            speed0 = hung.setdefault("speed", ship.dyn.speed)
            hung["t"] = hung.get("t", 0.0) + dt
            ship.dyn.speed = max(0.0, speed0 * (1 - hung["t"] / dies_in_s))
        deck_reading(ship, wind)

    return stepper


def run(runner, ship, wind, stepper=still, max_ticks: int = 3000) -> tuple[int, list]:
    """Tick until nothing is in progress. Returns (ticks, notes)."""
    notes = []
    ticks = 0
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, wind)
        stepper(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
        ticks += 1
    return ticks, notes


def kinds(notes) -> list[str]:
    return [n[1] for n in notes]


def texts(notes) -> list[str]:
    return [n[2] for n in notes]


def close_hauled_on_starboard(ship, wind, off_deg: float = 55.0, speed_kn: float = 5.0) -> None:
    """Put the ship by the wind on the starboard tack with way on her."""
    ship.dyn.heading = units.wrap_2pi(wind.direction_from - units.deg_to_rad(off_deg))
    ship.dyn.speed = units.knots_to_ms(speed_kn)
    deck_reading(ship, wind)
    assert ship.dyn.tack == "starboard"


def set_sail(runner, ship, wind, sail_id: str) -> None:
    cls = ship.sails[sail_id].cls
    runner.start(ship, f"set_{cls}", sail_id)
    run(runner, ship, wind)
    assert ship.sails[sail_id].state is SailState.SET


# ---------------------------------------------------------------------------
# The registry and the data files
# ---------------------------------------------------------------------------


def test_registry_has_every_required_evolution_with_source_and_crew():
    for eid in REQUIRED:
        evo = EVOLUTIONS[eid]
        assert evo.source, eid
        assert "Luce" in evo.source or "Lever" in evo.source, eid
        assert evo.crew, eid
        assert evo.steps or evo.script, eid


def test_registry_rejects_bad_files():
    good = {
        "id": "x",
        "applies_to": {"class": "square"},
        "steps": [{"do": "a", "duration_s": 1}],
        "source": "Luce 1866, ch. XXIII",
    }
    registry.parse_evolution(good)
    with pytest.raises(registry.EvolutionFileError, match="source"):
        registry.parse_evolution({**good, "source": ""})
    with pytest.raises(registry.EvolutionFileError, match="Cannot read"):
        registry.parse_evolution({**good, "preconditions": ["sail.state =="]})
    with pytest.raises(registry.EvolutionFileError, match="dotted attribute"):
        registry.parse_evolution({**good, "steps": [{"do": "a", "sets": {"sail": "set"}}]})
    with pytest.raises(registry.EvolutionFileError, match="either"):
        registry.parse_evolution({**good, "steps": []})
    with pytest.raises(registry.EvolutionFileError, match="not both"):
        registry.parse_evolution({**good, "script": "tack"})
    # package 29b: only an all-hands evolution belays the work in hand, and says so plainly
    with pytest.raises(registry.EvolutionFileError, match="hands: all"):
        registry.parse_evolution({**good, "belays": True, "crew": {"hands": 12}})
    with pytest.raises(registry.EvolutionFileError, match="true or false"):
        registry.parse_evolution({**good, "belays": "yes", "crew": {"hands": "all"}})
    assert registry.parse_evolution({**good, "belays": True, "crew": {"hands": "all"}}).belays


def test_only_the_manoeuvres_belay_the_work_in_hand():
    """The owner's ruling of 2026-09-29 at gate 4c: a call for all hands is a pool action;
    "Ready about!" and its kind stop the sail work in hand, a reef or a furl does not."""
    all_hands = {e.id for e in EVOLUTIONS.values() if str(e.crew.get("hands")) == "all"}
    belaying = {e.id for e in EVOLUTIONS.values() if e.belays}
    assert belaying == {
        "tack",
        "wear",
        "boxhaul",
        "wear_short_round",
        "lie_a_try",
        "come_to_anchor",
    }
    assert {"reef_square", "furl_all", "send_down_topgallant_masts"} <= all_hands - belaying


def test_nominal_durations_are_realistic():
    """A topsail from furled is a few minutes' work; a jib is quick; a reef is longer."""
    topsail = sum(s.duration_s for s in EVOLUTIONS["set_square"].steps if s.do != "haul_aboard")
    assert 180 <= topsail <= 420
    assert EVOLUTIONS["set_jibheaded"].nominal_duration_s <= 150
    assert 240 <= EVOLUTIONS["reef_square"].nominal_duration_s <= 480
    assert EVOLUTIONS["brace"].steps[0].duration_s == 45
    assert EVOLUTIONS["tack"].timing["brace_s"] == 45


# ---------------------------------------------------------------------------
# The expression language
# ---------------------------------------------------------------------------


class _Thing:
    def __init__(self):
        self.state = SailState.FURLED
        self.reefs = 1
        self.limit = 0.5
        self._secret = 1

    def method(self):
        return 1


def _env(**names):
    return expr.Env(names, {"double": lambda x: 2 * x, "pair": lambda a, b: [a, b]})


def test_expressions_evaluate_without_eval():
    t = _Thing()
    env = _env(sail=t, params={"n": 2})
    ev = lambda s: expr.evaluate_text(s, env)  # noqa: E731
    assert ev("sail.state == furled") is True
    assert ev("sail.state in [furled, loosed]") is True
    assert ev("sail.state not in [set]") is True
    assert ev("sail.reefs + params.n * 2") == 5
    assert ev("-sail.limit") == -0.5
    assert ev("double(sail.reefs) >= 2 and not sail.reefs > 5") is True
    assert ev("false or sail.reefs == 1") is True
    assert ev("pair(1, 'a')") == [1, "a"]
    assert ev("params.missing") is None
    assert ev("(1 + 2) * 3 / 3") == 3
    assert ev("unknown_word") == "unknown_word"


def test_expressions_refuse_unsafe_things():
    t = _Thing()
    env = _env(sail=t)
    with pytest.raises(expr.ExpressionError):
        expr.evaluate_text("sail._secret", env)
    with pytest.raises(expr.ExpressionError):
        expr.evaluate_text("sail.method", env)
    with pytest.raises(expr.ExpressionError):
        expr.evaluate_text("sail.method()", env)
    with pytest.raises(expr.ExpressionError):
        expr.evaluate_text("__import__('os')", env)
    with pytest.raises(expr.ExpressionError):
        expr.parse("sail.state = furled")
    with pytest.raises(expr.ExpressionError):
        expr.parse("sail.state in")
    with pytest.raises(expr.ExpressionError):
        expr.parse("1 +* 2")


# ---------------------------------------------------------------------------
# The runner on the reference ships, with physics that does nothing
# ---------------------------------------------------------------------------


def test_runner_registers_itself():
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    assert ship.extra["evolutions"] is runner
    assert runner.in_progress() == []


@pytest.mark.parametrize("path", SHIPS)
def test_every_sail_runs_its_evolutions_to_completion(path):
    ship = load_ship(path)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)  # light airs: weather factor 1.0
    for sail in ship.sails.values():
        cls = sail.cls
        if cls == "studding":
            continue  # after the square sails below
        if sail.state is SailState.UNBENT:
            # milestone 3b: storm canvas starts in the sail room and is bent before it is
            # set; tests/test_canvas.py bends and sets every one of them
            continue
        assert sail.state is SailState.FURLED
        text = runner.start(ship, f"set_{cls}", sail.id)
        assert part_name(ship, sail.id) in text
        ticks, notes = run(runner, ship, wind)
        assert sail.state is SailState.SET, sail.id
        assert "sail.set" in kinds(notes)
        assert kinds(notes)[0] == "evolution.started"
        # A course skips the hoist step, so it is quicker than the file's total.
        assert 60 <= ticks <= EVOLUTIONS[f"set_{cls}"].nominal_duration_s
        if sail.reef_bands:
            runner.start(ship, f"reef_{cls}", sail.id)
            _, notes = run(runner, ship, wind)
            assert sail.reefs == 1 and sail.state is SailState.SET
            assert "sail.reefed" in kinds(notes)
            assert any("1 reef" in t for t in texts(notes))
            runner.start(ship, f"shake_out_{cls}", sail.id)
            _, notes = run(runner, ship, wind)
            assert sail.reefs == 0
            assert "sail.reef_shaken_out" in kinds(notes)
        runner.start(ship, f"take_in_{cls}", sail.id)
        _, notes = run(runner, ship, wind)
        assert sail.state is not SailState.SET
        assert "sail.taken_in" in kinds(notes)
        runner.start(ship, f"furl_{cls}", sail.id)
        _, notes = run(runner, ship, wind)
        assert sail.state is SailState.FURLED
        assert "sail.furled" in kinds(notes)
    # Studding sails need the sail on their yard set first.
    for sail in ship.sails.values():
        if sail.cls != "studding" or sail.state is SailState.UNBENT:
            continue  # milestone 3b: ringtail, save-alls, water sail: tests/test_canvas.py
        on_yard = ship.sail_of(ship.yard_of(sail))
        if not on_yard.is_set:
            with pytest.raises(OrderError, match="until the sail on its yard is set"):
                runner.start(ship, "set_studding", sail.id)
            set_sail(runner, ship, wind, on_yard.id)
        boom = ship.spar_of_role(sail, "boom")
        if not boom.rigged_out:  # milestone 3b: the booms start rigged in (spec 3b §7)
            with pytest.raises(OrderError, match="boom is rigged in; rig it out first"):
                runner.start(ship, "set_studding", sail.id)
            runner.start(ship, "rig_out_studdingsail_boom", boom.id)
            run(runner, ship, wind)
        runner.start(ship, "set_studding", sail.id)
        _, notes = run(runner, ship, wind)
        assert sail.state is SailState.SET and "sail.set" in kinds(notes)
        runner.start(ship, "take_in_studding", sail.id)
        _, notes = run(runner, ship, wind)
        assert sail.state is SailState.FURLED and "sail.taken_in" in kinds(notes)
    assert runner.in_progress() == []


def test_courses_are_set_without_a_halyard_and_topsails_with_one():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)
    runner.start(ship, "set_square", "fore.course")
    course_ticks, _ = run(runner, ship, wind)
    runner.start(ship, "set_square", "fore.topsail")
    topsail_ticks, _ = run(runner, ship, wind)
    assert course_ticks < topsail_ticks  # no hoist for a course
    assert 120 <= course_ticks <= 300
    assert 180 <= topsail_ticks <= 420


def test_close_reef_caps_at_the_reef_bands():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    set_sail(runner, ship, wind, "main.topsail")
    runner.start(ship, "reef_square", "main.topsail", {"reefs": 99})
    _, notes = run(runner, ship, wind)
    assert ship.sails["main.topsail"].reefs == ship.sails["main.topsail"].reef_bands == 3
    assert any("3 reefs" in t for t in texts(notes))
    with pytest.raises(OrderError, match="close reefed already"):
        runner.start(ship, "reef_square", "main.topsail")


def test_step_logs_and_start_text_are_in_log_voice():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    text = runner.start(ship, "set_square", "fore.topsail")
    assert text == "Hands aloft to loose the fore topsail."
    _, notes = run(runner, ship, wind)
    assert texts(notes) == [
        "Hands aloft to loose the fore topsail.",
        "Laid aloft and loosed the fore topsail.",
        "Set the fore topsail.",
    ]
    assert [n[0] for n in notes] == ["routine", "routine", "notable"]
    assert notes[-1][3] == "fore.topsail"
    assert notes[-1][4]["evolution"] == "set_square"


# ---------------------------------------------------------------------------
# Preconditions
# ---------------------------------------------------------------------------


def test_preconditions_reject_with_a_sentence():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    with pytest.raises(OrderError, match="no such evolution"):
        runner.start(ship, "splice_the_mainbrace", "fore.topsail")
    with pytest.raises(OrderError, match="no part called 'fore.tops'l'"):
        runner.start(ship, "set_square", "fore.tops'l")
    with pytest.raises(
        OrderError, match="The spanker is a gaff sail; 'set_square' is for a square sail"
    ):
        runner.start(ship, "set_square", "spanker")
    with pytest.raises(OrderError, match="The fore topsail is a square sail, not a yard"):
        runner.start(ship, "brace", "fore.topsail")
    with pytest.raises(OrderError, match="order for the ship"):
        runner.start(ship, "tack", "fore.topsail")
    with pytest.raises(OrderError, match="needs a part"):
        runner.start(ship, "set_square", "ship")
    with pytest.raises(
        OrderError, match="The fore topsail is furled; there is nothing to take in."
    ):
        runner.start(ship, "take_in_square", "fore.topsail")
    with pytest.raises(OrderError, match="The fore topgallant has no reef bands."):
        set_sail(runner, ship, wind, "fore.topgallant")
        runner.start(ship, "reef_square", "fore.topgallant")
    with pytest.raises(OrderError, match="The fore topgallant is set already."):
        runner.start(ship, "set_square", "fore.topgallant")
    with pytest.raises(OrderError, match="has no reef in it"):
        set_sail(runner, ship, wind, "fore.topsail")
        runner.start(ship, "shake_out_square", "fore.topsail")
    assert runner.in_progress() == []


def test_wrecked_spar_rejects_at_start_and_fails_mid_way():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    ship.spars["main.topgallant_mast"].sent_down = True
    with pytest.raises(OrderError, match="yard or mast is wrecked or sent down"):
        runner.start(ship, "set_square", "main.royal")
    ship.spars["main.topgallant_mast"].sent_down = False
    runner.start(ship, "set_square", "main.royal")
    for _ in range(100):
        runner.step(ship, 1.0, wind)
    ship.spars["main.topmast"].wrecked = True
    _, notes = run(runner, ship, wind)
    assert "evolution.failed" in kinds(notes)
    assert (
        "Could not set the main royal: the main royal's yard or mast is wrecked" in texts(notes)[-1]
    )
    assert ship.sails["main.royal"].state is not SailState.SET


def test_a_parted_halyard_refuses_the_set_and_parting_midway_fails_the_hoist():
    """A sail is not set on a parted halyard (package 31b: the set is refused in words
    that name the line and the remedy); a halyard that parts while the topmen are
    loosing the sail fails the hoist as it always did (the step's `via`)."""
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    wind = make_wind()
    halyard = ship.lines["fore.topsail.yard.halyard"]
    halyard.state = LineState.PARTED
    with pytest.raises(OrderError, match="fore topsail yard halyard is parted and must be rove"):
        runner.start(ship, "set_square", "fore.topsail")
    assert runner.in_progress() == []
    halyard.state = LineState.BELAYED
    runner.start(ship, "set_square", "fore.topsail")
    for _ in range(30):
        runner.step(ship, 1.0, wind)
    halyard.state = LineState.PARTED  # parts while the sail is being loosed
    _, notes = run(runner, ship, wind)
    assert kinds(notes)[-1] == "evolution.failed"
    assert "fore topsail yard halyard is parted" in texts(notes)[-1]
    assert ship.sails["fore.topsail"].state is SailState.SHEETED


# ---------------------------------------------------------------------------
# Serialisation and concurrency
# ---------------------------------------------------------------------------


def test_two_evolutions_on_one_subject_are_serialised():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)
    runner.start(ship, "set_square", "main.topsail")
    text = runner.start(ship, "reef_square", "main.topsail")
    assert text == (
        "'Reef the main topsail' will follow 'set the main topsail', which the hands are still at."
    )
    snapshot = runner.in_progress()
    assert [s["step"] for s in snapshot] == ["loose", "waiting"]
    assert snapshot[1]["waiting"] is True
    ticks, notes = run(runner, ship, wind)
    order = [t for t in texts(notes) if t.startswith(("Set the", "All hands reef", "Reefed"))]
    assert order == [
        "Set the main topsail.",
        "All hands reef the main topsail.",
        "Reefed the main topsail; now set, 1 reef.",
    ]
    total = (
        EVOLUTIONS["set_square"].nominal_duration_s
        - 30
        + EVOLUTIONS["reef_square"].nominal_duration_s
    )
    assert ticks == pytest.approx(total, abs=3)


def test_queued_evolution_whose_precondition_fails_is_logged_not_raised():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    runner.start(ship, "set_square", "main.topsail")
    runner.start(ship, "set_square", "main.topsail")  # queued; will find it set already
    _, notes = run(runner, ship, wind)
    assert kinds(notes).count("sail.set") == 1
    assert kinds(notes)[-1] == "evolution.failed"
    assert "is set already" in texts(notes)[-1]


def test_different_subjects_run_together():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)
    for sail in ("fore.topsail", "main.topsail", "mizzen.topsail", "jib"):
        runner.start(ship, f"set_{ship.sails[sail].cls}", sail)
    assert len(runner.in_progress()) == 4
    ticks, _ = run(runner, ship, wind)
    assert ticks == 270  # loose 90 + sheet home 60 + hoist 120; the jib finished long before
    assert all(
        ship.sails[s].is_set for s in ("fore.topsail", "main.topsail", "mizzen.topsail", "jib")
    )


def test_brace_waits_for_a_tack_that_holds_the_yards():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(knots=10.0)
    close_hauled_on_starboard(ship, wind)
    runner.start(ship, "tack", "ship")
    text = runner.start(ship, "brace", "main.topsail.yard", {"target_deg": 0})
    assert "will follow" in text and "tack ship" in text
    assert runner.in_progress()[1]["step"] == "waiting"


# ---------------------------------------------------------------------------
# The weather factor
# ---------------------------------------------------------------------------


def test_weather_factor_values():
    kn = units.knots_to_ms
    deg = units.deg_to_rad
    assert weather_factor(kn(2), 0.0) == 1.0
    assert weather_factor(kn(30), 0.0) == pytest.approx(1.5)
    assert weather_factor(0.0, deg(25)) == pytest.approx(1.5)
    assert weather_factor(kn(30), deg(25)) == pytest.approx(2.0)
    assert weather_factor(kn(60), deg(-40)) == pytest.approx(2.0)
    assert 1.0 < weather_factor(kn(17), deg(10)) < 2.0


def test_weather_lengthens_an_evolution():
    calm_ship = load_ship(SCHOONER)
    calm = Runner(calm_ship)
    calm.start(calm_ship, "set_square", "fore.topsail")
    calm_ticks, _ = run(calm, calm_ship, make_wind(knots=3.0))

    hard_ship = load_ship(SCHOONER)
    hard_ship.dyn.heel = units.deg_to_rad(25)
    hard = Runner(hard_ship)
    hard.start(hard_ship, "set_square", "fore.topsail")
    hard_ticks, _ = run(hard, hard_ship, make_wind(knots=30.0))
    assert hard_ticks == pytest.approx(2 * calm_ticks, abs=2)
    assert hard_ship.sails["fore.topsail"].is_set


# ---------------------------------------------------------------------------
# Bracing
# ---------------------------------------------------------------------------


def test_brace_ramps_the_yard_over_the_step():
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)
    ship.dyn.apparent_wind_angle = units.deg_to_rad(50)  # starboard tack
    yard = ship.spars["fore.topsail.yard"]
    runner.start(ship, "brace", yard.id, {"target_deg": 30})
    angles = []
    while runner.in_progress():
        runner.step(ship, 1.0, wind)
        angles.append(yard.brace_angle)
    assert len(angles) == 45
    assert angles == sorted(angles)
    assert angles[21] == pytest.approx(units.deg_to_rad(30) * 22 / 45)
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(30))
    _, notes = [], ship.drain_notes()
    assert notes[-1][1] == "yard.braced" and "30° from square" in notes[-1][2]

    runner.start(ship, "brace", yard.id, {"target_deg": 90, "tack": "larboard"})
    run(runner, ship, wind)
    assert yard.brace_angle == pytest.approx(-yard.brace_limit)  # capped at the limit, other tack
    runner.start(ship, "brace", yard.id, {"target_deg": 0})
    run(runner, ship, wind)
    assert yard.brace_angle == pytest.approx(0.0)
    with pytest.raises(OrderError, match="not a yard"):
        runner.start(ship, "brace", "main.gaff")


# ---------------------------------------------------------------------------
# Tack, wear, heave to, fill away
# ---------------------------------------------------------------------------


def test_tack_needs_way_and_a_close_hauled_course():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind()
    close_hauled_on_starboard(ship, wind, speed_kn=1.0)
    with pytest.raises(OrderError, match="not way enough on her to stay: 1.0 kn"):
        runner.start(ship, "tack", "ship")
    close_hauled_on_starboard(ship, wind, off_deg=100.0, speed_kn=6.0)
    with pytest.raises(OrderError, match="not close-hauled"):
        runner.start(ship, "tack", "ship")


@pytest.mark.parametrize("path", SHIPS)
def test_tack_succeeds_when_the_ship_turns(path):
    ship = load_ship(path)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    for y in ship.spars.values():
        if y.is_yard:
            y.brace_angle = y.brace_limit  # braced up on the starboard tack
    text = runner.start(ship, "tack", "ship")
    assert text == "All hands about ship."
    ticks, notes = run(runner, ship, wind, turner(0.4))
    assert kinds(notes)[-1] == "ship.tacked"
    assert "braced up on the larboard tack" in texts(notes)[-1]
    words = texts(notes)
    if path == FRIGATE:
        assert words.index("Rise tacks and sheets. Mainsail haul.") < words.index(
            "Let go and haul."
        )
    else:
        # a vessel with no after yards has no "mainsail haul" (package 32e)
        assert "Let go and haul." in words and not any("Mainsail haul" in w for w in words)
    # The stub's turn rate sets the time; a frigate should take five to ten minutes.
    assert 240 <= ticks <= 600
    assert ship.dyn.tack == "larboard"
    new_course = units.wrap_2pi(wind.direction_from + 6 * units.POINT)
    assert abs(units.wrap_pi(ship.dyn.heading - new_course)) <= units.deg_to_rad(5)
    for y in ship.spars.values():
        if y.is_yard:
            assert y.brace_angle == pytest.approx(-y.brace_limit), y.id
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert runner.in_progress() == []


def test_tack_misses_stays_when_she_loses_her_way():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    old_heading = ship.dyn.heading
    for y in ship.spars.values():
        if y.is_yard:
            y.brace_angle = y.brace_limit
    runner.start(ship, "tack", "ship")
    ticks, notes = run(runner, ship, wind, staller(0.4, dies_in_s=60))
    # package 32e: her way gone with her head more than a point off the wind is a plain
    # miss, said at once; the yards are then squared as a brace with hands and time, and
    # the evolution ends when they are square and she has fallen off
    missed = [n for n in notes if n[1] == "ship.missed_stays"]
    assert len(missed) == 1 and missed[0][0] == "urgent"
    assert "lost her way before her head came up to the wind" in missed[0][2]
    assert "square the yards" in missed[0][2]
    assert kinds(notes)[-1] == "ship.fell_off"
    assert "fell off on the starboard tack" in texts(notes)[-1]
    assert "ship.tacked" not in kinds(notes)
    missed_at = next(i for i, n in enumerate(notes) if n[1] == "ship.missed_stays")
    assert missed_at < len(notes) - 1  # the squaring took time after the miss
    assert 60 <= ticks <= 200
    for y in ship.spars.values():
        if y.is_yard:
            assert y.brace_angle == pytest.approx(0.0), y.id  # squared, ready for a wear
    assert ship.dyn.target_heading == pytest.approx(old_heading)
    assert runner.in_progress() == []


def test_tack_misses_stays_when_she_hangs_head_to_wind():
    """Package 32e: her way gone within a point of the wind, she hangs in stays and is
    given Luce's recovery (the helm kept a-lee, the head sheets to windward); hung for
    the file's stays_timeout_s from the moment her way went, she has missed stays."""
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    runner.start(ship, "tack", "ship")
    ticks, notes = run(runner, ship, wind, hangs_in_stays(1.0, at_deg=8.0, dies_in_s=30))
    words = texts(notes)
    assert any(w.startswith("Her way is gone; she hangs in stays. Helm kept a-lee") for w in words)
    missed = [n for n in notes if n[1] == "ship.missed_stays"]
    assert len(missed) == 1 and "hung in stays and would not come round" in missed[0][2]
    assert kinds(notes)[-1] == "ship.fell_off"
    # about 47 s to come up to eight degrees off, 22 s more for her way to go and the
    # fifteen the rule waits, then 180 s in stays, then the yards squared over brace_s
    assert 280 <= ticks <= 360, ticks


@pytest.mark.parametrize("path", SHIPS)
def test_wear_comes_round_the_other_way(path):
    ship = load_ship(path)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind, off_deg=67.5)
    for y in ship.spars.values():
        if y.is_yard:
            y.brace_angle = y.brace_limit
    headings = []

    def record(s, dt, w):
        turner(0.5)(s, dt, w)
        headings.append(s.dyn.heading)

    runner.start(ship, "wear", "ship")
    ticks, notes = run(runner, ship, wind, record)
    assert kinds(notes)[-1] == "ship.wore"
    assert "larboard tack" in texts(notes)[-1]
    assert 360 <= ticks <= 720  # six to twelve minutes
    assert ship.dyn.tack == "larboard"
    new_course = units.wrap_2pi(wind.direction_from + 6 * units.POINT)
    assert abs(units.wrap_pi(ship.dyn.heading - new_course)) <= units.deg_to_rad(5)
    # She went round stern through the wind: at some point she was running.
    downwind = units.wrap_2pi(wind.direction_from + math.pi)
    assert min(abs(units.wrap_pi(h - downwind)) for h in headings) < units.deg_to_rad(3)
    for y in ship.spars.values():
        if y.is_yard:
            assert y.brace_angle == pytest.approx(-y.brace_limit, abs=0.02), y.id


def test_wear_gives_up_when_she_will_not_pay_off():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    runner.start(ship, "wear", "ship")
    ticks, notes = run(runner, ship, wind, still)
    assert kinds(notes)[-1] == "evolution.failed"
    assert "would not come round" in texts(notes)[-1]
    assert ticks == 901


@pytest.mark.parametrize(
    "path, backed_sail, backed_yard",
    [
        (FRIGATE, "main.topsail", "main.topsail.yard"),
        (SCHOONER, "fore.topsail", "fore.topsail.yard"),
    ],
)
def test_heave_to_and_fill_away(path, backed_sail, backed_yard):
    ship = load_ship(path)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    with pytest.raises(OrderError, match="She is not hove to."):
        runner.start(ship, "fill_away", "ship")
    no_sail = "No sail is set on the" if path == FRIGATE else "No head sail is set to haul"
    with pytest.raises(OrderError, match=no_sail):
        runner.start(ship, "heave_to", "ship")
    set_sail(runner, ship, wind, backed_sail)
    for y in ship.spars.values():
        if y.is_yard:
            y.brace_angle = y.brace_limit
    with pytest.raises(OrderError, match="She is on the starboard tack"):
        runner.start(ship, "heave_to", "ship", {"tack": "larboard"})
    runner.start(ship, "heave_to", "ship", {"tack": "starboard"})
    ticks, notes = run(runner, ship, wind)
    assert ticks == pytest.approx(45 * weather_factor(wind.effective_speed, 0.0), abs=2)
    assert kinds(notes)[-1] == "ship.hove_to"
    assert f"Hove to, {part_name(ship, backed_sail)} to the mast, helm a-lee." == texts(notes)[-1]
    yard = ship.spars[backed_yard]
    assert yard.brace_angle == pytest.approx(-yard.brace_limit)  # aback
    if path == FRIGATE:
        # full, at its own limit (since milestone 3b the limits differ by mast and level)
        mizzen = ship.spars["mizzen.topsail.yard"]
        assert mizzen.brace_angle == pytest.approx(mizzen.brace_limit)
    assert ship.dyn.helm_mode is HelmMode.RUDDER and ship.dyn.target_rudder > 0
    assert backed_yard in ship.extra["hove_to"]["yards"]
    with pytest.raises(OrderError, match="hove to already"):
        runner.start(ship, "heave_to", "ship")

    runner.start(ship, "fill_away", "ship")
    _, notes = run(runner, ship, wind)
    assert kinds(notes)[-1] == "ship.filled_away"
    assert yard.brace_angle == pytest.approx(yard.brace_limit)
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert "hove_to" not in ship.extra


# ---------------------------------------------------------------------------
# Snapshot, names, determinism
# ---------------------------------------------------------------------------


def test_in_progress_snapshot_counts_down():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(knots=3.0)
    runner.start(ship, "set_square", "fore.topsail")
    first = runner.in_progress()[0]
    assert first["id"] == "set_square" and first["subject"] == "fore.topsail"
    assert first["step"] == "loose"
    assert first["remaining_s"] == pytest.approx(300)  # every step, including conditional ones
    for _ in range(100):
        runner.step(ship, 1.0, wind)
    second = runner.in_progress()[0]
    assert second["step"] == "sheet_home"
    assert second["remaining_s"] == pytest.approx(200)


def test_part_names_for_the_log():
    ship = load_ship(FRIGATE)
    assert part_name(ship, "fore.topsail") == "fore topsail"
    assert part_name(ship, "mizzen.spanker") == "spanker"
    assert part_name(ship, "fore.course") == "foresail"
    assert (
        part_name(ship, "fore.topmast.studdingsail.starboard")
        == "starboard fore topmast studdingsail"
    )
    assert part_name(ship, "fore.topmast_staysail") == "fore topmast staysail"
    schooner = load_ship(SCHOONER)
    assert part_name(schooner, "main.sail") == "mainsail"


def test_same_orders_give_the_same_log():
    def play():
        ship = load_ship(FRIGATE)
        runner = Runner(ship)
        wind = make_wind(from_deg=90.0, knots=12.0)
        close_hauled_on_starboard(ship, wind)
        runner.start(ship, "set_square", "fore.topsail")
        runner.start(ship, "set_gaff", "mizzen.spanker")
        _, notes = run(runner, ship, wind)
        runner.start(ship, "tack", "ship")
        _, more = run(runner, ship, wind, turner(0.5))
        return notes + more

    assert play() == play()


# ---------------------------------------------------------------------------
# Package 30b: clearing a wreck, spare spars (playtest 10, findings 1 and 2)
# ---------------------------------------------------------------------------

LARBOARD_BOOM = "fore.topmast.studdingsail_boom.larboard"
LARBOARD_STUNSL = "fore.topmast.studdingsail.larboard"


def carried_away(ship, spar_id: str) -> None:
    """Carry a spar away as the strain model does: it and everything on it wrecked."""
    from freesail.physics import strain

    strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[spar_id], 2.0)
    ship.drain_notes()


def wrecked_schooner(sail_state: SailState = SailState.SET):
    """The schooner of playtest 10: the larboard fore topmast studding-sail boom carried
    away with its studding sail set on it, hanging to leeward."""
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    ship.sails[LARBOARD_STUNSL].state = sail_state
    ship.spars[LARBOARD_BOOM].rigged_out = True
    carried_away(ship, LARBOARD_BOOM)
    return ship, runner


def clear(runner, ship, part: str, knots: float = 12.0, **params) -> list:
    runner.start(ship, "clear_wreck", part, {"part": part, **params})
    _, notes = run(runner, ship, make_wind(knots=knots), max_ticks=20000)
    return notes


def cleared_line(notes) -> str:
    done = [n for n in notes if n[1] == "wreck.cleared"]
    assert len(done) == 1
    return done[0][2]


def test_the_booms_hold_each_ship_files_spare_spars_by_class():
    """Spare spars as a store by class (`parts.booms`), from the ship files the generator
    writes: the frigate's after Luce 1866 ch. XVII 'Stowing Booms', the schooner's by
    judgement after Luce and Chapelle; the store's comment names its source."""
    from freesail.ship.parts import booms

    frigate = booms(load_ship(FRIGATE))
    assert frigate.counts == {
        "topmast": 2,
        "topgallant_mast": 2,
        "yard": 2,
        "studdingsail_boom": 4,
        "jib_boom": 1,
        "flying_jib_boom": 1,
    }
    schooner = booms(load_ship(SCHOONER))
    assert schooner.counts == {"topmast": 1, "yard": 1, "studdingsail_boom": 2}
    assert len(frigate) == 12 and len(schooner) == 4
    for path in SHIPS:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        head = text[: text.index("    spare_spars:")].rsplit("\n", 2)[-2]
        assert "Luce 1866 ch. XVII" in head and "'Stowing Booms'" in head
    assert schooner.inventory_lines() == [
        "The booms hold 4 spare spars: 1 topmast, 1 yard and 2 studding-sail booms."
    ]


def test_a_ship_file_gives_its_spare_spars_by_class_or_as_a_count():
    from freesail.ship.loader import ship_from_dict
    from freesail.ship.parts import booms
    from freesail.ship.schema import ShipFileError

    with open(SCHOONER, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    doc["crew"]["stores"]["spare_spars"] = 3
    ship = ship_from_dict(doc)
    assert ship.spec.crew.stores.spare_spars == 3 and ship.spec.crew.stores.spars is None
    store = booms(ship)
    assert len(store) == 3 and store.have("topmast") == 3  # spars the carpenter fits to any
    doc["crew"]["stores"]["spare_spars"] = {"topmast": 1, "mizzen": 2}
    with pytest.raises(ShipFileError, match="'mizzen', which is not a spar class"):
        ship_from_dict(doc)


def test_cutting_away_a_boom_saves_the_whole_sail_and_sends_the_remains_down():
    """Playtest 10's wreck: cut away, the studding sail (whole) goes to the sail room and
    the boom's remains on deck; the log says what was saved and that nothing went over
    the side; the wreck no longer drags."""
    from freesail.physics.sails import _sail_windage_area, _spar_windage_area
    from freesail.ship.parts import sail_room

    ship, runner = wrecked_schooner()
    boom, sail = ship.spars[LARBOARD_BOOM], ship.sails[LARBOARD_STUNSL]
    before = len(sail_room(ship))
    assert _spar_windage_area(boom) > 0.0  # the wreck drags
    notes = clear(runner, ship, LARBOARD_STUNSL)  # the sail named: the whole wreck is cleared
    assert cleared_line(notes) == (
        "Cleared the wreck of the larboard fore topmast studdingsail boom: its remains sent "
        "down on deck; the larboard fore topmast studdingsail saved to the sail room; nothing "
        "went over the side. The booms hold 2 spare studding-sail booms."
    )
    assert texts(notes)[0] == (
        "Clear away the wreck of the larboard fore topmast studdingsail boom! Hands aloft "
        "with burtons and tripping-lines."
    )
    assert boom.wrecked and boom.sent_down and not boom.rigged_out
    assert sail.state is SailState.UNBENT and not sail.wrecked
    room = sail_room(ship)
    assert len(room) == before + 1 and room.sails[-1].kind == LARBOARD_STUNSL
    assert _sail_windage_area(ship, sail) == 0.0 and _spar_windage_area(boom) == 0.0
    data = [n for n in notes if n[1] == "wreck.cleared"][0][4]
    assert data["saved"] == [LARBOARD_STUNSL] and data["over_the_side"] == []


def test_the_part_graph_keeps_the_wreck_until_a_spare_replaces_the_spar():
    """A boom gone means no studding sail on it: the sail is not bent nor its boom rigged
    out until `shift` puts a spare in the boom's place, and the refusals say so."""
    ship, runner = wrecked_schooner()
    clear(runner, ship, LARBOARD_BOOM)
    with pytest.raises(OrderError, match="boom is carried away; shift it for a spare first"):
        runner.start(ship, "bend_sail", LARBOARD_STUNSL, {"sail": LARBOARD_STUNSL})
    with pytest.raises(OrderError, match="is carried away"):
        runner.start(ship, "rig_out_studdingsail_boom", LARBOARD_BOOM)
    with pytest.raises(OrderError, match="cleared already; shift the larboard"):
        runner.start(ship, "clear_wreck", LARBOARD_BOOM, {"part": LARBOARD_BOOM})


def test_shifting_a_spar_takes_a_spare_of_its_class_and_its_sail_may_be_bent_again():
    from freesail.ship.parts import booms

    ship, runner = wrecked_schooner()
    clear(runner, ship, LARBOARD_BOOM)
    boom = ship.spars[LARBOARD_BOOM]
    halyard = ship.lines[f"{LARBOARD_STUNSL}.halyard"]
    assert halyard.wrecked  # the gear went with the wreck
    runner.start(ship, "shift_spar", LARBOARD_BOOM, {"part": LARBOARD_BOOM})
    ticks, notes = run(runner, ship, make_wind(knots=3.0))
    # a boom's shift in light airs: got up 60 s, landed in its irons 120 s, rigged 90 s
    assert ticks == pytest.approx(60 + 120 + 90, abs=3)
    assert not boom.wrecked and not boom.sent_down and not boom.rigged_out
    assert boom.condition == 100.0
    assert not halyard.wrecked  # rove afresh
    assert booms(ship).counts["studdingsail_boom"] == 1
    assert texts(notes)[-1] == (
        "Shifted the larboard fore topmast studdingsail boom for a spare, 1 spare "
        "studding-sail boom left on the booms; the larboard fore topmast studdingsail may be "
        "bent to it again."
    )
    assert kinds(notes)[-1] == "spar.shifted"
    runner.start(ship, "bend_sail", LARBOARD_STUNSL, {"sail": LARBOARD_STUNSL})
    run(runner, ship, make_wind(knots=3.0))
    assert ship.sails[LARBOARD_STUNSL].state is SailState.FURLED
    runner.start(ship, "rig_out_studdingsail_boom", LARBOARD_BOOM)
    run(runner, ship, make_wind(knots=3.0))
    assert boom.rigged_out


def test_a_shift_is_refused_in_words_until_it_can_be_done():
    from freesail.ship.parts import booms

    ship, runner = wrecked_schooner()
    # playtest 10's "rig in" of the boom carried away: the refusal names the way out
    with pytest.raises(OrderError, match="carried away; clear the wreck and shift it for a"):
        runner.start(ship, "rig_in_studdingsail_boom", LARBOARD_BOOM)
    with pytest.raises(OrderError, match="still hangs aloft; cut it away first"):
        runner.start(ship, "shift_spar", LARBOARD_BOOM, {"part": LARBOARD_BOOM})
    with pytest.raises(OrderError, match="The main boom is sound; only a spar carried away"):
        runner.start(ship, "shift_spar", "main.boom", {"part": "main.boom"})
    clear(runner, ship, LARBOARD_BOOM)
    booms(ship).counts["studdingsail_boom"] = 0
    with pytest.raises(OrderError) as refused:
        runner.start(ship, "shift_spar", LARBOARD_BOOM, {"part": LARBOARD_BOOM})
    assert str(refused.value) == "No spare studding-sail boom aboard; the dockyard must supply one."


def test_the_whole_wreck_is_cleared_whichever_part_of_it_is_named():
    """A topmast carried away takes the spars above it and their sails: naming the royal
    clears the topmast's wreck, every spar sent down and every whole sail saved; each
    spar is then shifted in turn, the topmast first."""
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    ship.sails["fore.topsail"].state = SailState.SET
    carried_away(ship, "fore.topmast")
    yard = {"part": "fore.topsail.yard"}
    with pytest.raises(OrderError, match="fore topmast still hangs aloft; cut it away first"):
        runner.start(ship, "shift_spar", "fore.topsail.yard", yard)
    line = cleared_line(clear(runner, ship, "fore.royal"))
    gone = [s for s in ship.spars.values() if s.wrecked]
    assert {s.id for s in gone} >= {"fore.topmast", "fore.topsail.yard", "fore.royal.yard"}
    assert all(s.sent_down for s in gone)
    assert not any(s.wrecked for s in ship.sails.values())
    assert ship.sails["fore.topsail"].state is SailState.UNBENT
    assert line.startswith("Cleared the wreck of the fore topmast: its remains sent down")
    assert "the fore topsail" in line and "nothing went over the side" in line
    with pytest.raises(OrderError, match="went with the fore topmast; shift the fore topmast"):
        runner.start(ship, "shift_spar", "fore.topsail.yard", yard)
    runner.start(ship, "shift_spar", "fore.topmast", {"part": "fore.topmast"})
    _, more = run(runner, ship, make_wind(knots=3.0))
    assert "the fore topsail yard" in texts(more)[-1]
    assert "carried away with it, are still to be shifted" in texts(more)[-1]
    runner.start(ship, "shift_spar", "fore.topsail.yard", yard)
    run(runner, ship, make_wind(knots=3.0))
    runner.start(ship, "bend_sail", "fore.topsail", {"sail": "fore.topsail"})
    run(runner, ship, make_wind(knots=3.0))
    runner.start(ship, "set_square", "fore.topsail")
    run(runner, ship, make_wind(knots=3.0))
    assert ship.sails["fore.topsail"].is_set


def test_the_rags_of_a_sail_blown_out_go_over_the_side():
    from freesail.ship.parts import sail_room

    ship, runner = wrecked_schooner(SailState.BLOWN_OUT)
    before = len(sail_room(ship))
    line = cleared_line(clear(runner, ship, LARBOARD_BOOM))
    assert "the rags of the larboard fore topmast studdingsail over the side" in line
    assert len(sail_room(ship)) == before
    # a sail blown out on spars that stand: its rags alone are cut away
    other = load_ship(SCHOONER)
    r = Runner(other)
    other.sails["fore.topsail"].state = SailState.BLOWN_OUT
    line = cleared_line(clear(r, other, "fore.topsail"))
    assert line == "Cleared the wreck of the fore topsail: its rags cut adrift and over the side."
    assert other.sails["fore.topsail"].state is SailState.UNBENT


def test_a_lower_mast_carried_away_is_cut_adrift_with_all_it_carries():
    """The wreck of a lower mast lies in the water and is cut adrift (Luce 1884, ch. XXXI:
    "When a mast goes over the side, first, get clear of the wreck"): its spars and its
    sails are lost, and `send down` is refused for it in words."""
    from freesail.ship.parts import sail_room

    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    ship.sails["mizzen.topsail"].state = SailState.SET
    carried_away(ship, "mizzen.mast")
    down = {"part": "mizzen.mast", "send_down": True}
    with pytest.raises(OrderError, match="went over the side; its wreck cannot be sent down"):
        runner.start(ship, "clear_wreck", "mizzen.mast", down)
    with pytest.raises(OrderError, match="went over the side with the mizzen mast"):
        runner.start(ship, "unbend_sail", "mizzen.topsail", {"sail": "mizzen.topsail"})
    before = len(sail_room(ship))
    notes = clear(runner, ship, "mizzen.mast")
    assert any(t.startswith("Cut the lanyards and lashings") for t in texts(notes))
    line = cleared_line(notes)
    assert line.startswith("Cleared the wreck of the mizzen mast: cut adrift and over the side")
    assert line.endswith("There is no spare lower mast aboard.")
    assert len(sail_room(ship)) == before  # nothing saved
    assert ship.sails["mizzen.topsail"].state is SailState.UNBENT
    storm = ship.sails["storm_mizzen"]  # in the sail room all along
    assert storm.state is SailState.UNBENT and not storm.wrecked
    with pytest.raises(OrderError, match="No spare lower mast aboard"):
        runner.start(ship, "shift_spar", "mizzen.mast", {"part": "mizzen.mast"})


def test_unbend_cuts_a_wrecked_sail_out_of_the_wreck():
    """`unbend` of a wrecked sail (every verb refused a wrecked part before): cut clear of
    the wreck where it hangs, lowered and stowed; the boom's wreck is still to clear."""
    from freesail.ship.parts import sail_room

    ship, runner = wrecked_schooner()
    before = len(sail_room(ship))
    runner.start(ship, "unbend_sail", LARBOARD_STUNSL, {"sail": LARBOARD_STUNSL})
    _, notes = run(runner, ship, make_wind(knots=12.0))
    sail = ship.sails[LARBOARD_STUNSL]
    assert sail.state is SailState.UNBENT and not sail.wrecked
    assert len(sail_room(ship)) == before + 1
    assert (
        "Cut the larboard fore topmast studdingsail clear of the wreck, lowered it on deck "
        "and stowed it in the sail room."
    ) in texts(notes)
    assert not ship.spars[LARBOARD_BOOM].sent_down  # the boom's wreck still hangs
    line = cleared_line(clear(runner, ship, LARBOARD_BOOM))
    assert line.startswith(
        "Cleared the wreck of the larboard fore topmast studdingsail boom: its remains sent "
        "down on deck; nothing went over the side."
    )


def test_clearing_a_wreck_takes_hands_and_time_and_the_weather_stretches_it():
    """An evolution in the M3 form: its hands asked of the watch, its phases stretched by
    the weather factor (spec §8.4) and the crew factor, as every evolution's are."""
    from freesail.api.session import make_world

    times = []
    for knots in (3.0, 30.0):
        ship, runner = wrecked_schooner()
        runner.start(ship, "clear_wreck", LARBOARD_BOOM, {"part": LARBOARD_BOOM})
        ticks, _ = run(runner, ship, make_wind(knots=knots))
        times.append(ticks)
    # steadied 60 s, the sail cut out 120 s, the boom's remains sent down 90 s
    assert times[0] == pytest.approx(270, abs=3)
    assert times[1] > 1.4 * times[0]
    world = make_world(3, SCHOONER)
    carried_away(world.ship, LARBOARD_BOOM)
    world.submit("cut away the wreck of the larboard fore topmast studdingsail boom")
    world.tick()
    busy = world.ship.extra["evolutions"].in_progress()
    assert busy and busy[0]["id"] == "clear_wreck" and busy[0]["hands"] >= 1


def test_clearing_and_shifting_give_the_same_log_every_time():
    from freesail.api.session import make_world

    def play():
        world = make_world(5, SCHOONER)
        carried_away(world.ship, LARBOARD_BOOM)
        world.submit("clear the wreck")
        world.run(600)
        world.submit("shift the larboard fore topmast studdingsail boom for a spare")
        world.run(600)
        return [(e.tick, e.kind, e.text) for e in world.log]

    first = play()
    assert any(k == "spar.shifted" for _, k, _ in first)
    assert first == play()


# ---------------------------------------------------------------------------
# A parted line rove afresh, or spliced (package 31b; playtest 11's finding 7)
# ---------------------------------------------------------------------------


def _frigate_under_plain_sail():
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=90.0,
        ship_speed_kn=4.0,
    )
    w = make_world(7, FRIGATE, sc)
    w.ship.extra["evolutions"].clock = w.clock
    w.submit("set plain sail")
    w.run(1200)
    return w


def test_a_parted_sheet_is_rove_afresh_from_the_coil_and_the_sail_set_again():
    """The refusal of playtest 11 ("it must be spliced or rove afresh") now names an order
    that exists: `reeve a new <line>` takes its fathoms from the boatswain's store, holds
    the sail so a `set` given behind it waits its turn, and leaves the line whole at the
    file's rating; meanwhile the sail is refused for setting and for sheeting home, so a
    sail is never sheeted on a sheet that is gone."""
    from freesail.evolutions import scripts
    from freesail.ship.parts import cordage

    w = _frigate_under_plain_sail()
    ship = w.ship
    runner = ship.extra["evolutions"]
    sheet = ship.lines["fore.topsail.sheet.larboard"]
    rating = sheet.rating_kn
    sheet.state = LineState.PARTED
    ship.sails["fore.topsail"].state = SailState.LOOSED  # as the strain model leaves it
    store = cordage(ship)
    assert store.fathoms == 600.0  # the frigate's file: five coils
    e = w.submit("the boatswain's store")
    assert e.kind == "query.cordage"
    assert e.text == "The boatswain's store holds 600 fathoms of spare cordage."
    e = w.submit("set the fore topsail")
    assert e.kind == "order.rejected"
    assert e.text.endswith(
        "The fore topsail: the larboard fore topsail sheet is parted and must be rove afresh."
    )
    e = w.submit("sheet home the fore topsail")
    assert e.kind == "order.rejected" and "reeve a new one before" in e.text
    e = w.submit("reeve a new fore topsail sheet")
    assert e.kind == "order.rejected" and "Which fore topsail sheet" in e.text
    n0 = len(w.log)
    e = w.submit("reeve the larboard fore topsail sheet afresh")
    assert e.kind == "order.accepted"
    e = w.submit("set the fore topsail")
    assert e.kind == "order.accepted"  # queued behind the reeve, which holds the sail
    snap = {s["subject"]: s for s in runner.in_progress()}
    assert snap["fore.topsail.sheet.larboard"]["hands"] == 6
    assert snap["fore.topsail"]["waiting"] is True
    w.run(1200)
    assert runner.in_progress() == []
    texts = [ev.text for ev in list(w.log)[n0:]]
    wants = scripts.line_fathoms(ship, sheet)
    assert wants == 30.0
    assert (
        "Reeve a new larboard fore topsail sheet! Rouse up the coil from the boatswain's store."
        in texts
    )
    assert (
        "Roused up the coil and measured off 30 fathoms for the new larboard fore topsail sheet."
        in texts
    )
    rove = [ev for ev in list(w.log)[n0:] if ev.kind == "line.rove"]
    assert len(rove) == 1 and rove[0].severity.value == "notable"
    assert rove[0].text == (
        "Rove a new larboard fore topsail sheet; the fore topsail may be sheeted home and set. "
        "570 fathoms of spare cordage left in the boatswain's store."
    )
    assert rove[0].data["fathoms"] == 30.0 and rove[0].data["splice"] is False
    assert sheet.state is LineState.BELAYED and sheet.rating_kn == rating
    assert store.fathoms == 570.0
    assert ship.sails["fore.topsail"].state is SailState.SET
    # the line's log line comes after the reeve began and before the set began
    kinds = [ev.kind for ev in list(w.log)[n0:]]
    assert kinds.index("line.rove") < kinds.index("sail.set")


def test_a_splice_costs_no_cordage_and_leaves_the_line_an_eighth_the_weaker():
    """ "Ropes reeving through blocks are joined by a long splice ... the splice is weaker
    than the main part of the rope by about one-eighth" (Luce 1884, ch. II): a spliced
    brace is whole at seven eighths of its rating, the coil untouched, and its yard, which
    swung to the wind when the brace parted, may be braced again."""
    from freesail.physics.strain import strain_state
    from freesail.ship.parts import cordage

    w = _frigate_under_plain_sail()
    ship = w.ship
    brace = ship.lines["main.topsail.yard.brace.larboard"]
    rating = brace.rating_kn
    brace.state = LineState.PARTED
    strain_state(ship).swung.add("main.topsail.yard")
    before = cordage(ship).fathoms
    n0 = len(w.log)
    e = w.submit("splice the larboard main topsail brace")
    assert e.kind == "order.accepted"
    w.run(900)
    assert brace.state is LineState.BELAYED
    assert brace.rating_kn == pytest.approx(rating * 7 / 8)
    assert cordage(ship).fathoms == before
    assert "main.topsail.yard" not in strain_state(ship).swung
    rove = [ev for ev in list(w.log)[n0:] if ev.kind == "line.rove"]
    assert rove[0].text == (
        "Spliced the larboard main topsail yard brace, an eighth the weaker for it; the main "
        "topsail yard may be braced again."
    )
    assert rove[0].data["splice"] is True and rove[0].data["fathoms"] == 0.0


def test_reeving_is_refused_in_words_for_a_sound_line_standing_rigging_and_an_empty_store():
    from freesail.ship.parts import cordage

    w = _frigate_under_plain_sail()
    ship = w.ship
    e = w.submit("reeve a new starboard main brace")
    assert e.kind == "order.rejected"
    assert e.text.endswith(
        "The starboard main yard brace is sound and rove; only a parted line is rove afresh."
    )
    e = w.submit("splice the main stay")
    assert e.kind == "order.rejected" and "standing rigging" in e.text and "not rove" in e.text
    e = w.submit("reeve a new fore topsail")
    assert e.kind == "order.rejected" and "lines" in e.text
    # of two sheets named, the sound one is refused and the parted one rove
    ship.lines["fore.topsail.sheet.larboard"].state = LineState.PARTED
    e = w.submit("reeve new fore topsail sheets")
    assert e.kind == "evolution.started"  # one of the two rove: the line says which
    assert e.text.endswith(
        "Not done: the starboard fore topsail sheet is sound and rove; only a parted line is "
        "rove afresh."
    )
    w.run(900)
    # the store short of the length: a splice is the way, and the refusal says so
    cordage(ship).fathoms = 20.0
    ship.lines["main.course.sheet.starboard"].state = LineState.PARTED
    e = w.submit("reeve a new starboard main sheet")
    assert e.kind == "order.rejected"
    assert e.text.endswith(
        "There are but 20 fathoms of spare cordage in the boatswain's store; a new starboard "
        "main course sheet wants 30. Splice it instead."
    )
    cordage(ship).fathoms = 0.0
    e = w.submit("reeve the starboard main sheet afresh")
    assert e.kind == "order.rejected" and "no spare cordage" in e.text
    e = w.submit("the cordage")
    assert e.text.startswith("The boatswain's store has no spare cordage")
    e = w.submit("splice the starboard main sheet")
    assert e.kind == "order.accepted"


def test_the_schooners_lines_take_less_rope_and_her_store_is_her_own():
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    from freesail.evolutions import scripts
    from freesail.ship.parts import cordage

    w = make_world(7, SCHOONER, Scenario(gustiness=0.0, variability=0.0))
    ship = w.ship
    assert cordage(ship).fathoms == 150.0  # her file
    sheet = ship.lines["fore.topsail.sheet.larboard"]
    assert scripts.line_fathoms(ship, sheet) == 19.0  # 30 fathoms scaled by her length
    assert scripts.line_fathoms(ship, ship.lines["fore.topsail.yard.halyard"]) == 25.0
