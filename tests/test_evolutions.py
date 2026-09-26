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


def hangs_in_stays(rate_deg_s: float) -> Stepper:
    """Physics that turns until her head is twenty degrees off the wind, then hangs."""
    turn = turner(rate_deg_s)

    def stepper(ship, dt, wind) -> None:
        rel = units.relative_bearing(ship.dyn.heading, wind.direction_from)
        if abs(rel) > units.deg_to_rad(20):
            turn(ship, dt, wind)
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


def test_parted_halyard_fails_the_hoist():
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    wind = make_wind()
    ship.lines["fore.topsail.yard.halyard"].state = LineState.PARTED
    runner.start(ship, "set_square", "fore.topsail")
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
    assert words.index("Rise tacks and sheets. Mainsail haul.") < words.index("Let go and haul.")
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
    assert kinds(notes)[-1] == "ship.missed_stays"
    assert notes[-1][0] == "urgent"
    assert "lost her way" in texts(notes)[-1]
    assert "fell off on the starboard tack" in texts(notes)[-1]
    assert "ship.tacked" not in kinds(notes)
    assert ticks < 120
    for y in ship.spars.values():
        if y.is_yard:
            assert y.brace_angle == 0.0, y.id  # squared, ready for a wear
    assert ship.dyn.target_heading == pytest.approx(old_heading)
    assert runner.in_progress() == []


def test_tack_misses_stays_when_she_hangs_head_to_wind():
    ship = load_ship(SCHOONER)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    close_hauled_on_starboard(ship, wind)
    runner.start(ship, "tack", "ship")
    ticks, notes = run(runner, ship, wind, hangs_in_stays(1.0))
    assert kinds(notes)[-1] == "ship.missed_stays"
    assert "hung in stays" in texts(notes)[-1]
    assert ticks == 181


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
    with pytest.raises(OrderError, match="No sail is set on the"):
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
