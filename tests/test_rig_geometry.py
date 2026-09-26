"""Package 21: rig geometry (spec 3b §2 to §5).

Brace limits and the head and after yards' trim (§2), the catharpins (§3), the
bowlines (§4) and the adjacent-yard clearance (§5), on both reference ships.
Until the generator carries the topsail bowlines (the patch in the package
report), the schooner's are added here to an in-memory copy of her file, so
the bowline machinery is tried on both rigs; everything else runs on the ship
files as they are.

The compatibility rule (spec 3b §1) is tested by tests/test_known_truths.py
and tests/test_hands.py themselves; here, that a ship given none of the new
orders keeps milestone 3's state exactly (no bowline hauled, no catharpins in,
every rating factor one), and that the new work fits one watch of either ship.
"""

from __future__ import annotations

import math
import random
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import bill, hands
from freesail.evolutions import EVOLUTIONS, Runner
from freesail.evolutions import trim as yard_trim
from freesail.orders import verbs
from freesail.orders.complete import suggestions
from freesail.physics import sails as sail_physics
from freesail.physics import strain
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import (
    CATHARPIN_GAIN_DEG,
    LineState,
    SailState,
    lower_yards,
    sync_catharpins,
)
from freesail.ship.stub import OrderError

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
GAIN = units.deg_to_rad(CATHARPIN_GAIN_DEG)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def schooner_with_bowlines():
    """The schooner with her fore topsail's bowlines, as the generator patch adds them."""
    data = yaml.safe_load((ROOT / SCHOONER).read_text(encoding="utf-8"))
    have = {ln["id"] for ln in data["lines"]}
    for side in ("starboard", "larboard"):
        if f"fore.topsail.bowline.{side}" in have:
            continue  # the generator carries them already
        data["lines"].append(
            {
                "id": f"fore.topsail.bowline.{side}",
                "class": "bowline",
                "of": "fore.topsail",
                "side": side,
                "rating_kn": 9.7,
            }
        )
    return ship_from_dict(data, "schooner with bowlines")


def bare(path: str | None = None, ship=None):
    """A ship with a runner and no physics or crew: orders and evolutions only."""
    ship = ship if ship is not None else load_ship(path)
    return ship, Runner(ship)


def make_wind(from_deg: float = 0.0, knots: float = 10.0) -> Wind:
    params = WindParams.from_nautical(from_deg, knots, gustiness=0.0, variability=0.0)
    return Wind(params, random.Random(0))


def run_runner(ship, runner, wind, stepper=None, max_ticks: int = 6000) -> list:
    """Tick the runner (and a stand-in for the physics, if given) until idle."""
    notes = []
    for _ in range(max_ticks):
        if not runner.in_progress():
            break
        runner.step(ship, 1.0, wind)
        if stepper is not None:
            stepper(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
    assert not runner.in_progress(), "still at work"
    return notes


def by_the_wind(ship, off_deg: float = 50.0, wind_from_deg: float = 0.0) -> None:
    """Close-hauled on the starboard tack: wind on the starboard bow, plain sail set,
    every yard braced sharp up."""
    ship.dyn.heading = units.wrap_2pi(units.deg_to_rad(wind_from_deg - off_deg))
    ship.dyn.apparent_wind_angle = units.deg_to_rad(off_deg - 8.0)
    ship.dyn.apparent_wind_speed = 8.0
    ship.dyn.speed = units.knots_to_ms(5.0)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for y in ship.spars.values():
        if y.is_yard:
            y.brace_angle = y.brace_limit


def world(path: str, heading: float = 300.0, knots: float = 15.0, speed: float = 5.0):
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
    )
    return make_world(7, path, scenario)


def ticks(w, n: int, trim_every: int = 0) -> None:
    for i in range(n):
        if trim_every and i % trim_every == 0:
            w.submit("trim sails")
        w.tick()


def log_texts(w, kind: str | None = None) -> list[str]:
    return [e.text for e in w.log if kind is None or e.kind == kind]


# ---------------------------------------------------------------------------
# Compatibility: a ship given none of the new orders is as she was
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_a_ship_starts_as_milestone_3_left_her(path):
    ship = load_ship(path)
    for ln in ship.lines.values():
        if ln.cls == "bowline":
            assert ln.state is LineState.FREE and not ln.bowline_hauled
    for sp in ship.spars.values():
        assert not sp.swiftered_in and sp.rating_factor == 1.0
        assert sp.brace_limit == sp.rigged_brace_limit
    assert sync_catharpins(ship) == []  # nothing to bring in, nothing changed
    for sp in ship.spars.values():
        assert sp.brace_limit == sp.rigged_brace_limit


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_close_hauled_forces_are_unchanged_without_bowlines(path):
    """The sail model with no bowline hauled is milestone 2's to the last newton: the
    new coefficient path gives the class tables' values at every angle."""
    for cls in sail_physics.SAIL_CLASSES.values():
        for deg in range(0, 91, 3):
            a = units.deg_to_rad(deg)
            assert cls.coefficients(a) == cls.coefficients(a, 0.0)


# ---------------------------------------------------------------------------
# §2: the head and after yards
# ---------------------------------------------------------------------------


def test_the_after_yards_stand_sharper_only_as_their_rigging_allows():
    ship = load_ship(FRIGATE)
    yards = [y for y in ship.spars.values() if y.is_yard]
    targets = {y.id: y.brace_limit for y in yards}
    out, diff = yard_trim.stagger(ship, targets)
    # braced sharp up, every yard is at its limit already: nothing is eased or forced,
    # and the difference named is the rigging's (none on the files before the Fincham
    # limits of spec 3b §2.1, two degrees after them)
    assert out == targets
    main, fore = ship.spars["main.yard"].brace_limit, ship.spars["fore.yard"].brace_limit
    assert diff == pytest.approx(units.rad_to_deg(main - fore))
    # with the main yard's rigging allowing more than it is asked, it is braced up to
    # AFTER_YARDS_SHARPER_DEG beyond the fore, and the fore is not eased for it
    ship.spars["main.yard"].brace_limit = fore + units.deg_to_rad(5.0)
    targets["main.yard"] = fore
    out, diff = yard_trim.stagger(ship, targets)
    assert out["fore.yard"] == pytest.approx(fore)
    assert out["main.yard"] == pytest.approx(fore + units.deg_to_rad(3.0))
    assert diff == pytest.approx(3.0)
    assert yard_trim.difference_words(diff) == "the after yards three degrees sharper"


def test_head_yards_sharper_eases_the_after_yards(monkeypatch):
    ship = load_ship(FRIGATE)
    targets = {y.id: y.brace_limit for y in ship.spars.values() if y.is_yard}
    out, diff = yard_trim.stagger(ship, targets, head_sharper=True)
    three = units.deg_to_rad(3.0)
    assert out["fore.yard"] == pytest.approx(targets["fore.yard"])
    assert out["main.yard"] == pytest.approx(targets["fore.yard"] - three)
    assert out["mizzen.crossjack.yard"] == pytest.approx(targets["fore.yard"] - three)
    assert out["main.topsail.yard"] == pytest.approx(targets["fore.topsail.yard"] - three)
    assert yard_trim.difference_words(diff) == "the head yards three degrees sharper"
    # the switch that eases the head yards instead (off: see trim.EASE_HEAD_YARDS)
    monkeypatch.setattr(yard_trim, "EASE_HEAD_YARDS", True)
    out, diff = yard_trim.stagger(ship, targets)
    assert out["fore.yard"] == pytest.approx(targets["main.yard"] - three)
    assert diff == pytest.approx(3.0)


def test_brace_sharp_up_names_the_difference_and_head_yards_sharper_reverses_it():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    ship.spars["main.mast"].swiftered_in = True  # the main yard braces four degrees more
    _, text, _ = orders.handle(ship, "brace sharp up")
    main = ship.spars["main.yard"].rigged_brace_limit + GAIN
    words = yard_trim.difference_words(units.rad_to_deg(main - ship.spars["fore.yard"].brace_limit))
    assert words.startswith("the after yards") and words.endswith("degrees sharper")
    assert text.startswith(f"Braced up for the starboard tack, {words}.")
    started = {i.subject_id: i.params["target_angle"] for i in runner.instances}
    assert started["main.yard"] == pytest.approx(ship.spars["main.yard"].rigged_brace_limit + GAIN)
    assert started["fore.yard"] == pytest.approx(ship.spars["fore.yard"].brace_limit)
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    _, text, data = orders.handle(ship, "brace sharp up with the head yards sharper")
    assert "the head yards three degrees sharper" in text
    started = {i.subject_id: i.params["target_angle"] for i in runner.instances}
    three = units.deg_to_rad(3.0)
    assert started["main.yard"] == pytest.approx(ship.spars["fore.yard"].brace_limit - three)
    assert started["fore.yard"] == pytest.approx(ship.spars["fore.yard"].brace_limit)


def test_trim_sails_on_a_wind_staggers_and_off_the_wind_does_not():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    _, text, _ = orders.handle(ship, "trim sails with the head yards sharper")
    assert "the head yards three degrees sharper" in text
    assert "trimmed the sheets" in text  # the words about the yards leave the sheets in
    targets = {i.subject_id: i.params["target_angle"] for i in runner.instances}
    three = units.deg_to_rad(3.0)
    assert targets["main.yard"] == pytest.approx(targets["fore.yard"] - three)
    # a wind abaft the beam: trimmed to the wind, all alike, nothing named
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    ship.dyn.apparent_wind_angle = units.deg_to_rad(120.0)
    _, text, _ = orders.handle(ship, "trim sails with the head yards sharper")
    assert "sharper" not in text and "alike" not in text


def test_the_schooner_has_head_yards_only_and_nothing_is_staggered():
    ship, runner = bare(SCHOONER)
    by_the_wind(ship)
    _, text, _ = orders.handle(ship, "brace sharp up")
    assert "sharper" not in text and "alike" not in text
    targets = {i.subject_id: i.params["target_angle"] for i in runner.instances}
    for yid, t in targets.items():
        assert t == pytest.approx(ship.spars[yid].brace_limit)


# ---------------------------------------------------------------------------
# §3: the catharpins
# ---------------------------------------------------------------------------


def test_swiftering_in_the_main_catharpins_gains_the_main_yard_four_degrees():
    ship, runner = bare(FRIGATE)
    wind = make_wind()
    main_yard = ship.spars["main.yard"]
    rigged = main_yard.brace_limit
    _, text, data = orders.handle(ship, "swifter in the catharpins on the main")
    assert data["subjects"] == ["main.mast"]
    assert text == "Boatswain's party to the main mast shrouds; reeve the swifter."
    notes = run_runner(ship, runner, wind)
    assert ship.spars["main.mast"].swiftered_in
    assert notes[-1][2] == (
        "Swiftered in the catharpins on the main mast; the main yard will brace four "
        "degrees sharper."
    )
    sync_catharpins(ship)
    assert main_yard.brace_limit == pytest.approx(rigged + GAIN)
    # only the lower yard: the topmast rigging is not touched
    for yid in ("main.topsail.yard", "fore.yard", "mizzen.crossjack.yard"):
        assert ship.spars[yid].brace_limit == ship.spars[yid].rigged_brace_limit
    # every reader sees it: the brace order, a level-0 haul, the brace evolution
    orders.handle(ship, "brace the main yard sharp up")
    inst = [i for i in runner.instances if i.subject_id == "main.yard"][-1]
    assert inst.params["target_angle"] == pytest.approx(rigged + GAIN)
    run_runner(ship, runner, wind)
    assert main_yard.brace_angle == pytest.approx(rigged + GAIN)
    # about twenty minutes a mast, before the weather and the hands
    assert EVOLUTIONS["swifter_in_catharpins"].nominal_duration_s == pytest.approx(1200.0)
    assert EVOLUTIONS["ease_catharpins"].nominal_duration_s == pytest.approx(1200.0)


def test_easing_the_catharpins_brings_a_sharp_yard_in_and_says_so():
    w = world(FRIGATE)
    ship = w.ship
    ship.spars["main.mast"].swiftered_in = True
    ticks(w, 2)  # the strain model keeps the limits with the masts each tick
    main_yard = ship.spars["main.yard"]
    assert main_yard.brace_limit == pytest.approx(main_yard.rigged_brace_limit + GAIN)
    main_yard.brace_angle = main_yard.brace_limit
    ship.spars["main.mast"].swiftered_in = False  # as the ease evolution's middle step does
    ticks(w, 2)
    assert main_yard.brace_angle == pytest.approx(main_yard.rigged_brace_limit)
    came_in = [t for t in log_texts(w, "yard.braced") if "lower shrouds went out" in t]
    rigged = round(units.rad_to_deg(main_yard.rigged_brace_limit))
    assert came_in == [
        f"Main yard came in to {rigged}° from {rigged + 4}° as the lower shrouds went out."
    ]


def test_every_lower_mast_and_the_refusals():
    ship, runner = bare(FRIGATE)
    _, _, data = orders.handle(ship, "swifter in the catharpins")
    assert data["subjects"] == ["fore.mast", "main.mast", "mizzen.mast"]
    fresh, _ = bare(FRIGATE)
    with pytest.raises(OrderError, match="The catharpins on the main mast are not swiftered in"):
        orders.handle(fresh, "ease the catharpins on the main")
    fresh.spars["main.mast"].swiftered_in = True
    with pytest.raises(
        OrderError, match="The catharpins on the main mast are swiftered in already"
    ):
        orders.handle(fresh, "swifter in the main catharpins")
    _, _, data = orders.handle(fresh, "ease the catharpins")  # the one mast that has them in
    assert data["subjects"] == ["main.mast"]
    schooner, _ = bare(SCHOONER)
    with pytest.raises(OrderError, match="She has no mizzen mast"):
        orders.handle(schooner, "swifter in the catharpins on the mizzen")


def test_the_schooner_swifters_in_and_gains_nothing_in_the_braces():
    ship, runner = bare(SCHOONER)
    wind = make_wind()
    assert [lower_yards(ship, ship.spars[m]) for m in ("fore.mast", "main.mast")] == [[], []]
    _, _, data = orders.handle(ship, "swifter in the fore catharpins")
    assert data["subjects"] == ["fore.mast"]
    notes = run_runner(ship, runner, wind)
    assert ship.spars["fore.mast"].swiftered_in
    assert "she has no yard on the lower mast there to brace the sharper" in notes[-1][2]
    sync_catharpins(ship)
    for y in ship.spars.values():
        if y.is_yard:
            assert y.brace_limit == y.rigged_brace_limit


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_a_mast_swiftered_in_is_rated_down_athwartships(path):
    """On a wind the load is nearly all athwartships, so the mast is judged against
    nearly CATHARPIN_RATING_FACTOR of its rating: a sixth harder or so. Running
    before it, hardly at all."""
    w = world(path, heading=300.0)
    w.submit("call all hands")  # the schooner's watch alone sets her sails one at a time
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    ticks(w, 900, trim_every=120)
    mast = w.ship.spars["main.mast"] if path == FRIGATE else w.ship.spars["fore.mast"]
    assert mast.rating_factor == 1.0
    mast.swiftered_in = True
    ticks(w, 5)
    f = strain.CATHARPIN_RATING_FACTOR
    on_mast = [s for s in w.ship.sails.values() if s.force_kn > 0 and w.ship.mast_of(s) is mast]
    s = sum(abs(x.side_force_kn) for x in on_mast) / sum(x.force_kn for x in on_mast)
    assert s > 0.8  # on a wind the pull is mostly athwartships
    assert mast.rating_factor == pytest.approx(1 / math.sqrt(1 - s * s + (s / f) ** 2))
    assert f <= mast.rating_factor < 0.9
    assert mast.strain_ratio == pytest.approx(mast.load_kn / (mast.rating_kn * mast.rating_factor))
    # before the wind the shrouds bear little of it
    w2 = world(path, heading=180.0)
    w2.submit("set the topsails")
    w2.submit("brace the yards square")
    ticks(w2, 500)
    mast2 = w2.ship.spars[mast.id]
    mast2.swiftered_in = True
    ticks(w2, 5)
    assert mast2.rating_factor > 0.97


def test_a_strained_mast_with_its_catharpins_in_says_so():
    ship = load_ship(FRIGATE)
    mast = ship.spars["main.mast"]
    mast.swiftered_in = True
    mast.load_kn = 1.2 * mast.rating_kn
    mast.rating_factor = 0.86
    st = strain.strain_state(ship)
    strain._warn(ship, st, mast, mast.strain_ratio)
    text = ship.drain_notes()[-1][2]
    assert text.endswith("working under the press of sail, the catharpins swiftered in.")


def test_a_swung_lower_yard_swings_the_catharpins_gain_further():
    ship = load_ship(FRIGATE)
    ship.dyn.apparent_wind_angle = math.pi  # dead aft: the yard would lie fore and aft
    yard = ship.spars["main.yard"]
    strain._swing_yard(ship, yard)
    assert abs(yard.brace_angle) == pytest.approx(strain.SWUNG_YARD_MAX)
    ship.spars["main.mast"].swiftered_in = True
    sync_catharpins(ship)
    strain._swing_yard(ship, yard)
    assert abs(yard.brace_angle) == pytest.approx(strain.SWUNG_YARD_MAX + GAIN)


# ---------------------------------------------------------------------------
# §4: the bowlines
# ---------------------------------------------------------------------------


def test_a_hauled_bowline_flattens_the_luff_and_eases_the_drag():
    sq = sail_physics.SAIL_CLASSES["square"]
    gain = units.deg_to_rad(sail_physics.BOWLINE_LUFF_GAIN_DEG)
    at_luff = sq.luff_angle
    # at and below the luff angle the curve is read four degrees on ...
    for deg in (10.0, 14.0, units.rad_to_deg(at_luff)):
        a = units.deg_to_rad(deg)
        assert sq.coefficients(a, gain)[0] == pytest.approx(sq.coefficients(a + gain)[0])
        assert sq.coefficients(a, gain)[1] == pytest.approx(
            (1 - sail_physics.BOWLINE_DRAG_REDUCTION) * sq.coefficients(a)[1]
        )
    # ... and a full sail draws as before (from the curve's peak, 40 degrees since 3b)
    for deg in (40.0, 45.0, 60.0):
        a = units.deg_to_rad(deg)
        assert sq.coefficients(a, gain) == sq.coefficients(a)


@pytest.mark.parametrize("which", ["frigate", "schooner"])
def test_the_weather_bowline_brings_the_luff_angle_down_while_braced_up(which):
    ship = load_ship(FRIGATE) if which == "frigate" else schooner_with_bowlines()
    by_the_wind(ship)
    wind = make_wind(from_deg=0.0, knots=15.0)
    sail_id = "fore.course" if which == "frigate" else "fore.topsail"
    sail = ship.sails[sail_id]
    sail_physics.compute_sail_forces(ship, wind)
    luff0, thrust0 = ship.extra["luff_angle"], sail.thrust_kn
    weather = ship.line_of(sail, "bowline", "starboard")
    lee = ship.line_of(sail, "bowline", "larboard")
    lee.state, lee.hauled = LineState.BELAYED, 1.0  # a hauled lee bowline holds nothing
    sail_physics.compute_sail_forces(ship, wind)
    assert sail_physics.hauled_weather_bowline(ship, sail) is None
    assert ship.extra["luff_angle"] == pytest.approx(luff0)
    weather.state, weather.hauled = LineState.BELAYED, 1.0
    sail_physics.compute_sail_forces(ship, wind)
    assert sail_physics.hauled_weather_bowline(ship, sail) is weather
    assert ship.extra["luff_angle"] < luff0
    assert sail.thrust_kn > thrust0
    # it takes a tenth of its sail's pull; the sheets, braces and halyards are not it
    assert weather.load_kn == pytest.approx(sail_physics.BOWLINE_LOAD_FRACTION * sail.force_kn)
    assert weather not in ship.sheets_of(sail) + ship.braces_of(ship.yard_of(sail))
    assert weather.cls not in sail_physics.HALYARD_CLASSES


@pytest.mark.parametrize("which", ["frigate", "schooner"])
def test_bowlines_slack_when_the_yard_is_braced_in(which):
    ship = load_ship(FRIGATE) if which == "frigate" else schooner_with_bowlines()
    by_the_wind(ship)
    wind = make_wind(from_deg=0.0, knots=15.0)
    sail_id = "fore.course" if which == "frigate" else "fore.topsail"
    sail = ship.sails[sail_id]
    line = ship.line_of(sail, "bowline", "starboard")
    line.state, line.hauled = LineState.BELAYED, 1.0
    yard = ship.yard_of(sail)
    yard.brace_angle = units.deg_to_rad(sail_physics.BOWLINE_SLACK_ANGLE_DEG + 1.0)
    sail_physics.compute_sail_forces(ship, wind)
    assert line.bowline_hauled
    yard.brace_angle = units.deg_to_rad(sail_physics.BOWLINE_SLACK_ANGLE_DEG - 1.0)
    sail_physics.compute_sail_forces(ship, wind)
    assert not line.bowline_hauled and line.state is LineState.FREE
    note = ship.drain_notes()[-1]
    assert note[1] == "line.slacked"
    assert "a bowline will not stand off the wind" in note[2]


@pytest.mark.parametrize("which", ["frigate", "schooner"])
def test_haul_the_weather_bowlines_is_work_for_hands(which):
    ship = load_ship(FRIGATE) if which == "frigate" else schooner_with_bowlines()
    ship, runner = bare(ship=ship)
    by_the_wind(ship)
    wind = make_wind()
    _, text, data = orders.handle(ship, "steady out the bowlines")
    assert text.startswith("Steady out the bowlines!")
    # the weather bowline of every sail that has them: the courses' (and, with the
    # generator patch, the topsails'), the schooner's fore topsail's
    want = [ln.id for ln in ship.lines.values() if ln.cls == "bowline" and ln.side == "starboard"]
    assert "fore.course.bowline.starboard" in want if which == "frigate" else want
    assert data["subjects"] == want
    assert {e["evolution"] for e in data["evolutions"]} == {"haul_bowline"}
    notes = run_runner(ship, runner, wind)
    for lid in want:
        assert ship.lines[lid].bowline_hauled
    assert notes[-1][2].startswith("Steadied out the starboard")
    assert EVOLUTIONS["haul_bowline"].nominal_duration_s == pytest.approx(60.0)
    if which == "frigate":
        # "haul the fore bowline" is the weather one when no side is said
        with pytest.raises(OrderError, match="starboard fore course bowline is hauled out already"):
            orders.handle(ship, "haul the fore bowline")


def test_bowline_refusals_say_why():
    ship, _ = bare(FRIGATE)
    by_the_wind(ship)
    with pytest.raises(OrderError, match="lee side of the fore yard"):
        orders.handle(ship, "haul the lee fore bowline")
    ship.sails["main.course"].state = SailState.FURLED
    with pytest.raises(OrderError, match="main course is furled; there is no leech to haul out"):
        orders.handle(ship, "haul the main bowline")
    ship.spars["fore.yard"].brace_angle = units.deg_to_rad(20.0)
    with pytest.raises(OrderError, match="braced in to 20°; a bowline will not stand off"):
        orders.handle(ship, "haul the weather fore bowline")


def test_let_go_and_ease_the_bowlines_at_the_pin():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    for side in ("starboard",):
        for m in ("fore", "main"):
            ln = ship.lines[f"{m}.course.bowline.{side}"]
            ln.state, ln.hauled = LineState.BELAYED, 1.0
    kind, text, _ = orders.handle(ship, "let go the weather bowlines")
    assert kind == "line.let_go" and runner.instances == []
    assert not any(ln.bowline_hauled for ln in ship.lines.values())
    ln = ship.lines["fore.course.bowline.starboard"]
    ln.state, ln.hauled = LineState.BELAYED, 1.0
    kind, _, _ = orders.handle(ship, "ease the weather fore bowline")
    assert kind == "line.eased" and not ln.bowline_hauled
    # Luce's word for letting them go
    ln.state, ln.hauled = LineState.BELAYED, 1.0
    orders.handle(ship, "clear away the bowlines")
    assert ln.state is LineState.FREE


def test_a_parted_bowline_leaves_the_sail_drawing_and_says_so():
    ship = load_ship(FRIGATE)
    by_the_wind(ship)
    ln = ship.lines["fore.course.bowline.starboard"]
    ln.state, ln.hauled = LineState.BELAYED, 1.0
    strain._part_line(ship, strain.strain_state(ship), ln, 2.0)
    assert ship.sails["fore.course"].state is SailState.SET
    assert not ln.bowline_hauled
    assert ship.drain_notes()[-1][2] == (
        "Starboard fore course bowline parted; the foresail lifting at the weather leech."
    )


def _turner(rate_deg_s: float = 0.4, speed_kn: float = 5.0):
    """Physics that turns the ship toward the ordered heading at a fixed rate."""

    def stepper(ship, dt, wind) -> None:
        d = ship.dyn
        error = units.wrap_pi(d.target_heading - d.heading)
        step = units.deg_to_rad(rate_deg_s) * dt
        d.heading = units.wrap_2pi(
            d.heading + (error if abs(error) <= step else math.copysign(step, error))
        )
        d.speed = units.knots_to_ms(speed_kn)
        d.apparent_wind_angle = units.relative_bearing(d.heading, wind.direction_from)

    return stepper


@pytest.mark.parametrize("which", ["frigate", "schooner"])
@pytest.mark.parametrize("evolution", ["tack", "wear"])
def test_going_about_lets_the_bowlines_go_and_steadies_them_out_again(which, evolution):
    ship = load_ship(FRIGATE) if which == "frigate" else schooner_with_bowlines()
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    by_the_wind(ship, off_deg=55.0 if evolution == "tack" else 67.5, wind_from_deg=90.0)
    ship.dyn.apparent_wind_angle = units.relative_bearing(ship.dyn.heading, wind.direction_from)
    sails = ["fore.course", "main.course"] if which == "frigate" else ["fore.topsail"]
    for sid in sails:
        ln = ship.line_of(ship.sails[sid], "bowline", "starboard")
        ln.state, ln.hauled = LineState.BELAYED, 1.0
    runner.start(ship, evolution, "ship")
    notes = run_runner(ship, runner, wind, _turner(0.4 if evolution == "tack" else 0.5))
    words = [n[2] for n in notes]
    let_go = {
        "tack": "Rise tacks and sheets. Mainsail haul; let go the bowlines.",
        "wear": (
            "Stand by to wear ship. Up helm; clear away the bowlines; brace in the after yards."
        ),
    }[evolution]
    steady = "Haul taut the lifts and weather braces. Steady out the bowlines."
    assert let_go in words and steady in words
    assert words.index(let_go) < words.index(steady)
    assert ship.dyn.tack == "larboard"
    for sid in sails:
        sail = ship.sails[sid]
        assert ship.line_of(sail, "bowline", "larboard").bowline_hauled
        assert not ship.line_of(sail, "bowline", "starboard").bowline_hauled


def test_going_about_without_bowlines_says_nothing_of_them():
    ship = load_ship(FRIGATE)
    runner = Runner(ship)
    wind = make_wind(from_deg=90.0, knots=10.0)
    by_the_wind(ship, off_deg=55.0, wind_from_deg=90.0)
    ship.dyn.apparent_wind_angle = units.relative_bearing(ship.dyn.heading, wind.direction_from)
    runner.start(ship, "tack", "ship")
    words = [n[2] for n in run_runner(ship, runner, wind, _turner())]
    assert "Rise tacks and sheets. Mainsail haul." in words
    assert not any("bowline" in w for w in words)


# ---------------------------------------------------------------------------
# §5: adjacent yards
# ---------------------------------------------------------------------------


def test_the_clearance_is_computed_from_the_yards_with_a_floor():
    ship = load_ship(FRIGATE)
    lower, upper = ship.spars["main.yard"], ship.spars["main.topsail.yard"]
    arc = (upper.length_m / 2) / (lower.length_m / 2)
    assert verbs.adjacent_yard_max_diff(lower, upper) == pytest.approx(arc)
    assert 35.0 < units.rad_to_deg(arc) < 50.0
    lower.length_m = 10 * upper.length_m  # a short yard over a long one: the floor
    assert verbs.adjacent_yard_max_diff(lower, upper) == pytest.approx(
        units.deg_to_rad(verbs.ADJACENT_YARD_FLOOR_DEG)
    )


def test_bracing_one_yard_away_from_its_neighbour_is_refused_in_words():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    apart = round(units.rad_to_deg(ship.spars["main.yard"].brace_limit))
    most = round(
        units.rad_to_deg(
            verbs.adjacent_yard_max_diff(ship.spars["main.yard"], ship.spars["main.topsail.yard"])
        )
    )
    with pytest.raises(OrderError) as info:
        orders.handle(ship, "brace the main topsail yard square")
    assert str(info.value) == (
        "The main topsail yard cannot be braced so far from the main yard while the main "
        f"topsail is set ({apart}° apart, {most}° at most); brace the main yards together, "
        "or clew up the main topsail."
    )
    assert runner.instances == []
    # the whole mast together is no trouble, nor is the yard alone with the sails
    # between it and its neighbours in
    orders.handle(ship, "brace the main yards square")
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    ship.sails["main.topsail"].state = SailState.FURLED
    ship.sails["main.topgallant"].state = SailState.FURLED
    orders.handle(ship, "brace the main topsail yard square")
    assert [i.subject_id for i in runner.instances] == ["main.topsail.yard"]


def test_aback_is_one_rule_and_small_trims_always_pass():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    # laid aback braces the whole mast: the adjacent rule has nothing to say
    orders.handle(ship, "back the main topsail")
    assert len(runner.instances) == 4
    # a few degrees between neighbours is the floor's business, never refused
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    orders.handle(ship, "haul the weather main topsail brace")
    orders.handle(ship, "haul the weather main topsail brace")
    assert ship.spars["main.topsail.yard"].brace_angle == pytest.approx(
        ship.spars["main.topsail.yard"].brace_limit - units.deg_to_rad(10.0)
    )


def test_hauling_a_brace_step_by_step_meets_the_rule():
    ship, _ = bare(FRIGATE)
    by_the_wind(ship)
    with pytest.raises(OrderError, match="The main topsail yard cannot be braced so far from"):
        for _ in range(20):
            orders.handle(ship, "haul the starboard main topsail brace")


def test_the_schooner_topsail_and_topgallant_yards():
    ship, runner = bare(SCHOONER)
    by_the_wind(ship)
    with pytest.raises(OrderError, match="fore topgallant yard cannot be braced so far"):
        orders.handle(ship, "brace the fore topgallant yard square")
    ship.sails["fore.topgallant"].state = SailState.FURLED
    orders.handle(ship, "brace the fore topgallant yard square")
    assert [i.subject_id for i in runner.instances] == ["fore.topgallant.yard"]


def test_an_order_given_already_counts_where_the_yard_is_going():
    ship, runner = bare(FRIGATE)
    by_the_wind(ship)
    ship.sails["main.topgallant"].state = SailState.FURLED  # only the topsail between
    # the main yard braced up to 30 degrees: 28 apart from the topsail yard, within its
    # clearance; then the topsail yard square is 30 from where the main yard is going,
    # though 55 from where it lies now
    orders.handle(ship, "brace the main yard up")
    orders.handle(ship, "brace the main topsail yard square")
    assert [i.subject_id for i in runner.instances] == ["main.yard", "main.topsail.yard"]


# ---------------------------------------------------------------------------
# The files, the words and the hands
# ---------------------------------------------------------------------------


def test_the_new_evolutions_load_with_sources_and_crew_lines():
    for eid in ("swifter_in_catharpins", "ease_catharpins", "haul_bowline"):
        evo = EVOLUTIONS[eid]
        assert evo.source and isinstance(evo.crew["hands"], int)
    assert [s.aloft for s in EVOLUTIONS["swifter_in_catharpins"].steps] == [True, False, True]
    assert not any(s.aloft for s in EVOLUTIONS["haul_bowline"].steps)


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_the_new_work_fits_one_watch_of_either_ship(path):
    w = make_world(7, path, Scenario())
    crew = w.ship.extra["crew"]
    for hour in (1, 4, 9, 13, 21):
        deck = bill.on_deck(crew, datetime(1805, 6, 1, hour, 0, 0))
        for eid in ("swifter_in_catharpins", "ease_catharpins", "haul_bowline"):
            evo = EVOLUTIONS[eid]
            want = hands.CrewRequest.from_mapping(evo.crew)
            aloft = any(step.aloft for step in evo.steps)
            for sailor in crew.sailors:
                sailor.at = None
            got = hands.request(crew, deck, "x", want, "main", aloft=aloft)
            assert got.outcome == hands.ENOUGH, (path, hour, eid, got.got, got.wanted)


def test_the_new_words_complete():
    ship = load_ship(FRIGATE)
    assert "swifter in the catharpins on the main" in suggestions(
        ship, "swifter in the catharpins on", 20
    )
    assert any(s.startswith("ease the catharpins") for s in suggestions(ship, "ease the cath", 20))
    assert any("bowline" in s for s in suggestions(ship, "steady out the fore b", 20))
    assert any("head yards sharper" in s for s in suggestions(ship, "trim sails w", 20))


def test_the_same_orders_give_the_same_log():
    def voyage():
        w = world(FRIGATE)
        w.submit("set plain sail")
        w.submit("brace sharp up on the starboard tack")
        ticks(w, 400, trim_every=120)
        w.submit("haul the weather bowlines")
        w.submit("swifter in the catharpins on the main")
        ticks(w, 1600, trim_every=200)
        w.submit("tack ship")
        ticks(w, 700)
        return [(e.tick, e.kind, e.text) for e in w.log]

    first = voyage()
    assert first == voyage()
    texts = [t for _, _, t in first]
    assert any(t.startswith("Steadied out the starboard") for t in texts)
    assert any(t.startswith("Swiftered in the catharpins on the main mast") for t in texts)
