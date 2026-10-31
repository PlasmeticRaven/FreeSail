"""Package 75, the engine's lateen step (B3.1; docs/design/Design-ShipsEngineExtensions.md §3,
§10.2): the lateen class finished, with the mizen course of the 64 and the 74 cut at the mast.

The course is a lateen sail on a lateen yard, its luff laced to the mizzen mast and its head to
the yard abaft the mast, marked `cut_at_mast` (Ext §3.1). In the physics it is a gaff sail: every
lookup of a sail's curve or trim by its class reads `Sail.curve_class`, the gaff's for it, so its
sheet runs between the gaff's 18 and 85 degrees by every route that works it. In the handling it
is the ship's driver (Ext §3.5): hauled aft at helm's a-lee with the bowline braced to leeward
(Steel 1794 vol. II p. 316), brailed up hove to, brailed at "up helm" and hauled out by the wind,
taken in at the gale's third reef, set after the cast. Its yard is no braced yard (Ext §3.3): the
mizen yard has vangs in place of braces (Falconer 1780, VANGS and BRACE), and no order braces it.
Its own evolutions set it, brail it up, furl it on its yard aloft, reef it, shake the reef out and
trim its sheet (Ext §3.6). A whole lateen, with no key (a later package's tartane, Ext §3.7), keeps
the lateen's own curve and trim, and is no driver.

None of the eight files carries a lateen (`tests/test_rig_classing.py`, the probe), so the tests
run on the fixture `frigate_with_mizen_yard()` (`tests/rig_fixtures.py`): the frigate-36 with her
spanker, gaff and boom replaced by the 64's mizen course on its yard, and a spritsail yard and a
sprit-topsail yard under her bowsprit. Every test sails the fixture whole, those two yards with
it: the engine's bowsprit step (B3.2, Ext §4; `tests/test_bowsprit_yards.py`) keeps them out of
the classing, and the manoeuvres swing them with the head yards.
"""

from __future__ import annotations

import importlib.util
import math
import random
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
from rig_fixtures import frigate_with_mizen_yard, frigate_with_mizen_yard_doc, write_ship

from freesail import orders
from freesail.api.session import make_world
from freesail.combat.hits import _spar_weight
from freesail.core.world import Scenario
from freesail.evolutions import EVOLUTIONS, Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders import resolve
from freesail.orders.storm import shorten_sail_lines
from freesail.physics.sails import SAIL_CLASSES, _read_rig, _sail_windage_area, _square_rigged
from freesail.physics.wind import Wind, WindParams
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import Booms, Sail, SailState
from freesail.ship.schema import YARD_LIKE_CLASSES
from freesail.ship.stub import OrderError
from freesail.world.ships import _trim_for

ROOT = Path(__file__).resolve().parents[1]
COURSE = "mizzen.course"
YARD = "mizzen.yard"
# the yards under the bowsprit (B3.2's, Ext §4): head yards, no mast's
SPRIT_YARDS = ("spritsail.yard", "sprit_topsail.yard")

# The gaff's sheet range (`evolutions.trim.TRIM_RANGE`), which the course cut at the mast takes,
# against the lateen's own floor, which a whole lateen keeps (Ext §3.1).
GAFF_FLOOR_DEG, CEILING_DEG = 18.0, 85.0
LATEEN_FLOOR_DEG = 8.0
# Thirty degrees of apparent wind on the larboard bow: each class's best angle (25 degrees off
# the wind) is below both floors, so a sheet trimmed for it lies at its class's floor.
CLOSE = math.radians(-30.0)


def _frigate_doc(whole_lateen: bool = False) -> dict:
    """The fixture whole; `whole_lateen`, its course a whole lateen, the key taken out."""
    doc = frigate_with_mizen_yard_doc()
    if whole_lateen:
        next(s for s in doc["sails"] if s["id"] == COURSE).pop("cut_at_mast")
    return doc


def _ship(whole_lateen: bool = False) -> Ship:
    return ship_from_dict(_frigate_doc(whole_lateen), "fixture.yaml")


def _bare(ship: Ship, awa: float = CLOSE) -> Runner:
    """A bare ship's runner, the deck reading `awa` of apparent wind, enough to trim to."""
    runner = Runner(ship)
    ship.dyn.apparent_wind_angle = awa
    ship.dyn.apparent_wind_speed = 6.0
    return runner


LIGHT_AIRS = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))


def _run(runner: Runner, ship: Ship, max_ticks: int = 3000) -> tuple[int, list]:
    """Tick the runner (no physics) until nothing is in hand: the ticks and the notes."""
    ticks, notes = 0, []
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return ticks, notes


def _deg(angle: float) -> float:
    return round(math.degrees(abs(angle)), 3)


def _under_plain_sail(ship: Ship) -> Ship:
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship


# ---------------------------------------------------------------------------
# The class, the curve and the yard (Ext §3.1-§3.3)
# ---------------------------------------------------------------------------


def test_the_fixtures_classing_is_the_frigates_row_with_the_course_her_driver():
    """Ext §10.2: the classing of the fixture whole, its yards under the bowsprit with it,
    equals the frigate's row of the golden table (`tests/test_rig_classing.py`), her driver and
    her boom sail the mizen course where they were the spanker: the head yards on the masts the
    fore's four, the two under the bowsprit beside them (B3.2's place 2); the lateen yard no
    working yard and none of the after yards."""
    ship = _under_plain_sail(_ship())
    assert [m.id for m in scripts._masts_with_yards(ship)] == [
        "fore.mast",
        "main.mast",
        "mizzen.mast",
    ]
    head, after = scripts.head_and_after_yards(ship)
    on_masts = [y for y in head if not ship.under_bowsprit(y)]
    assert (len(on_masts), len(after)) == (4, 8)
    assert [y.id for y in head if ship.under_bowsprit(y)] == list(SPRIT_YARDS)
    assert YARD not in {y.id for y in scripts.working_yards(ship)}
    assert ship.mast_of(scripts.yards_to_back(ship)[0]).id == "main.mast"
    assert _square_rigged(ship) is True
    targets = {y.id: y.brace_limit for y in scripts.working_yards(ship)}
    assert yard_trim.stagger(ship, targets)[1] == pytest.approx(2.0, abs=0.05)
    assert [s.id for s in scripts.after_gaff_sails(ship)] == [COURSE]
    assert [s.id for s in scripts.boom_sails(ship)] == [COURSE]
    assert [s.id for s in scripts.after_gaff_sails_all(ship)] == [COURSE]
    assert scripts.dipping_lugs(ship) == []


def test_the_lateen_yard_is_no_braced_yard_but_still_a_yard_to_send_down():
    """Ext §3.3: `Spar.is_yard` is a braced yard alone; the lateen yard is called a lateen yard
    in the orders' words, stays a yard for the yard work (`YARD_LIKE_CLASSES`), and is weighted
    aloft as a yard is when shot flies through the rigging. Carried away, its wreck is sent
    down and a spare swayed aloft and crossed, as a yard is (`ShiftSparScript`), in a yard's
    time (`SPAR_WORK`: each phase twice its base time)."""
    ship = frigate_with_mizen_yard()
    yard = ship.spars[YARD]
    assert yard.cls == "lateen_yard" and not yard.is_yard
    assert ship.spars["mizzen.crossjack.yard"].is_yard
    assert resolve.kind_of(yard) == "lateen yard"
    assert "lateen_yard" in YARD_LIKE_CLASSES
    assert _spar_weight(yard) == _spar_weight(ship.spars["mizzen.crossjack.yard"]) == 2.0
    runner = _bare(ship)
    ship.extra["booms"] = Booms(counts={"lateen_yard": 1})
    yard.wrecked = True
    _kind, _words, data = orders.handle(ship, "cut away the mizzen yard")
    assert [e["evolution"] for e in data["evolutions"]] == ["clear_wreck"]
    _run(runner, ship)
    assert yard.sent_down
    _kind, _words, data = orders.handle(ship, "shift the mizzen yard")
    assert [e["evolution"] for e in data["evolutions"]] == ["shift_spar"]
    ticks, notes = _run(runner, ship)
    assert "Swayed aloft and crossed the new mizzen yard." in [n[2] for n in notes]
    assert ticks == 2 * (60 + 120 + 90)  # got up, swayed and rigged at a yard's work
    assert not yard.wrecked and not yard.sent_down


def test_the_course_draws_on_the_gaffs_curve_and_is_furled_with_its_windage():
    """Ext §3.1: the physics' two lookups read `curve_class`: the curve driving the course is
    the gaff's, and its windage furled the gaff's; a whole lateen keeps the lateen's row."""
    ship = _under_plain_sail(_ship())
    ship.dyn.apparent_wind_angle = math.radians(-60.0)
    yard_trim.set_sheet_angle(ship, ship.sails[COURSE], math.radians(35.0))
    drawing = {d.sail.id: d for d in _read_rig(ship).drawing}
    assert drawing[COURSE].cls is SAIL_CLASSES["gaff"]
    course = ship.sails[COURSE]
    course.state = SailState.FURLED
    assert _sail_windage_area(ship, course) == pytest.approx(
        course.area_m2 * SAIL_CLASSES["gaff"].furled_windage
    )
    whole = _under_plain_sail(_ship(whole_lateen=True))
    yard_trim.set_sheet_angle(whole, whole.sails[COURSE], math.radians(35.0))
    drawing = {d.sail.id: d for d in _read_rig(whole).drawing}
    assert drawing[COURSE].cls is SAIL_CLASSES["lateen"]


# ---------------------------------------------------------------------------
# No order braces the lateen yard (Ext §3.3)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "brace the mizzen yard square",
        "square the mizzen yard",
        "brace the mizzen yard sharp up",
        "brace the mizzen yard aback",
        "trim the mizzen yard",
    ],
)
def test_bracing_the_mizen_yard_is_refused_with_the_vangs_words(text):
    ship = frigate_with_mizen_yard()
    Runner(ship)
    with pytest.raises(OrderError) as e:
        orders.handle(ship, text)
    assert str(e.value) == (
        "The mizzen yard is a lateen yard, not a yard; the lateen sail on it is not braced; it "
        "is trimmed with its sheet and vangs."
    )


@pytest.mark.parametrize(
    "text", ["square the yards", "brace sharp up", "brace the mizzen yards sharp up", "trim sails"]
)
def test_the_braces_orders_and_the_trims_leave_the_lateen_yard_alone(text):
    """The orders that brace every yard, or the mizzen's, and `trim sails` brace every yard but
    the lateen yard, which stays at 0 when the work is done; so does the polar's trim, which the
    promotion's takes (`world.ships._trim_for`, `world.crews`)."""
    ship = _under_plain_sail(frigate_with_mizen_yard())
    runner = _bare(ship)
    _kind, _words, data = orders.handle(ship, text)
    braced = [e["subject"] for e in data["evolutions"] if e["evolution"] == "brace"]
    assert braced and "mizzen.crossjack.yard" in braced and YARD not in braced
    _run(runner, ship)
    assert ship.spars[YARD].brace_angle == 0.0
    _trim_for(ship, math.radians(-70.0))
    assert ship.spars[YARD].brace_angle == 0.0
    assert ship.spars["mizzen.crossjack.yard"].brace_angle != 0.0


# ---------------------------------------------------------------------------
# The course's sheet, the gaff's 18-85 degrees by every route (Ext §3.1, §3.6)
# ---------------------------------------------------------------------------


def _routes(whole_lateen: bool) -> dict[str, float]:
    """The course's sheet, degrees, after each route that works it, thirty degrees off the
    apparent wind: set, `trim the mizen`, `trim sails`, `draw the mizen`, `draw_sheets`, the
    tack's haul aft (`sheets_to`), the tending lying to bringing her up, and the polar's trim;
    and the sheet's floor and ceiling (`trim.sheet_geometry`)."""
    ship = _ship(whole_lateen)
    course = ship.sails[COURSE]
    runner = _bare(ship)
    out: dict[str, float] = {}

    def ease() -> None:
        yard_trim.set_sheet_angle(ship, course, math.radians(60.0))

    orders.handle(ship, "set the mizen")
    _run(runner, ship)
    out["set"] = _deg(course.sheet_angle)
    for text in ("trim the mizen", "trim sails", "draw the mizen"):
        ease()
        orders.handle(ship, text)
        _run(runner, ship)
        out[text] = _deg(course.sheet_angle)
    ease()
    scripts.draw_sheets(ship, [course])
    out["draw_sheets"] = _deg(course.sheet_angle)
    ease()
    scripts.sheets_to(ship, scripts.boom_sails(ship), None, None)
    out["hauled aft"] = _deg(course.sheet_angle)
    ease()
    scripts._work_lying_to_sheets(ship, {"sign": 1.0}, 1.0, False)
    out["lying to"] = _deg(course.sheet_angle)
    ease()
    _trim_for(ship, CLOSE)
    out["polar"] = _deg(course.sheet_angle)
    geo = yard_trim.sheet_geometry(ship, course)
    out["floor"], out["ceiling"] = _deg(geo.floor), _deg(geo.ceiling)
    return out


def test_the_courses_sheet_keeps_the_gaffs_floor_by_every_route():
    """Ext §10.2: cut at the mast, the course lies at the gaff's floor by every route that works
    its sheet, and a whole lateen at the lateen's by the same: the floor and ceiling every route
    is held within (`trim.sheet_geometry`) are its curve class's. The "lying to" route is the
    tending's bringing her up, the sheet hauled to its floor (`_work_lying_to_sheets`); a ship
    hove to brails her driver up, and only a brig's is eased. Each route clamps to that floor
    here, so it cannot show which class's trim the route itself looks up; the orders' decisions
    below do (risk 4, Ext §13)."""
    cut = _routes(whole_lateen=False)
    assert cut.pop("floor") == GAFF_FLOOR_DEG and cut.pop("ceiling") == CEILING_DEG
    assert cut == dict.fromkeys(cut, GAFF_FLOOR_DEG), cut
    whole = _routes(whole_lateen=True)
    assert whole.pop("floor") == LATEEN_FLOOR_DEG and whole.pop("ceiling") == CEILING_DEG
    hauled_aft = whole.pop("hauled aft")  # a whole lateen is no boom sail: nothing hauled
    assert hauled_aft == 60.0
    assert whole.pop("lying to") == 60.0  # nor kept lying to
    assert whole == dict.fromkeys(whole, LATEEN_FLOOR_DEG), whole


def test_the_courses_sheet_is_trimmed_free_within_the_gaffs_ceiling():
    """Sixty degrees and a hundred and thirty off the apparent wind: the gaff's trim, 35 degrees
    and its ceiling of 85, as the frigate's spanker would be. (The lateen's trim is the same
    there: this is the free trim, not the class's.)"""
    ship = _ship()
    course = ship.sails[COURSE]
    course.state = SailState.SET
    for awa, want in ((math.radians(-60.0), 35.0), (math.radians(-130.0), 85.0)):
        scripts.draw_sheets(ship, [course], None, awa)
        assert _deg(course.sheet_angle) == pytest.approx(want, abs=0.01)
        assert _deg(course.sheet_angle) == pytest.approx(
            _deg(yard_trim.wanted_sheet_angle("gaff", awa)), abs=0.01
        )


# Thirty-eight degrees of apparent wind on the larboard bow: the gaff wants its floor, 18
# degrees, and the lateen 13, above its own floor of 8 (each class 25 degrees off the wind).
# Only between 33 and 43 degrees off do the two classes' trims differ
# (`trim.wanted_sheet_angle`), so only there does a trim looked up by the wrong class show.
BETWEEN_FLOORS = math.radians(-38.0)
LATEEN_WANTS_DEG = 13.0


def _at_the_gaffs_floor(whole_lateen: bool) -> tuple[Ship, Sail, Runner]:
    """The course set under plain sail, its sheet at the gaff's floor, 38 degrees off."""
    ship = _under_plain_sail(_ship(whole_lateen))
    course = ship.sails[COURSE]
    runner = _bare(ship, BETWEEN_FLOORS)
    yard_trim.set_sheet_angle(ship, course, math.radians(GAFF_FLOOR_DEG))
    return ship, course, runner


@pytest.mark.parametrize("whole_lateen", [False, True])
def test_the_orders_find_the_courses_trim_by_its_curve_class(whole_lateen):
    """Risk 4 (Ext §13), a `curve_class` lookup missed: thirty-eight degrees off, with its sheet
    at the gaff's floor, the course cut at the mast stands as trimmed to `trim the mizen` and
    `trim sails` and is drawing already to `draw the mizen` (`orders.verbs`' `_trim` and
    `_draw` read the gaff's trim). Read by its own class, the lateen's, it would be trimmed and
    drawn on to 13 degrees, as a whole lateen's sheet is."""
    want = LATEEN_WANTS_DEG if whole_lateen else GAFF_FLOOR_DEG
    for text in ("trim the mizen", "trim sails"):
        ship, course, runner = _at_the_gaffs_floor(whole_lateen)
        _kind, words, data = orders.handle(ship, text)
        trims = [e for e in data["evolutions"] if e["evolution"] == "trim_lateen_sheet"]
        started = {e["subject"] for e in trims}
        assert (COURSE in started) is whole_lateen, (text, words)
        if text == "trim the mizen" and not whole_lateen:
            assert words == "The sheet of the mizzen course stands as trimmed."
        _run(runner, ship)
        assert _deg(course.sheet_angle) == pytest.approx(want, abs=0.01), text
    ship, course, _runner = _at_the_gaffs_floor(whole_lateen)
    if whole_lateen:
        _kind, words, _data = orders.handle(ship, "draw the mizen")
        assert words.startswith("Let draw the mizzen course; the lee sheet hauled aft"), words
    else:
        with pytest.raises(OrderError, match="^The mizzen course is drawing already.$"):
            orders.handle(ship, "draw the mizen")
    assert _deg(course.sheet_angle) == pytest.approx(want, abs=0.01)


# ---------------------------------------------------------------------------
# The evolutions and their words (Ext §3.6)
# ---------------------------------------------------------------------------


def test_each_lateen_evolution_runs_to_its_end():
    """Set, reef, shake out, take in and furl, in turn, from furled (as
    `tests/test_evolutions.py` runs every class's): each to its end, in about its file's time,
    with its log; set and hauled out with no hoist, the yard standing."""
    ship = frigate_with_mizen_yard()
    course = ship.sails[COURSE]
    runner = _bare(ship)
    assert course.state is SailState.FURLED and course.reef_bands == 1
    runner.start(ship, "set_lateen", COURSE)
    ticks, notes = _run(runner, ship)
    assert course.state is SailState.SET and ticks == 90  # cleared away, hauled out
    assert [n[2] for n in notes][-1] == "Set the mizzen."
    assert ticks <= EVOLUTIONS["set_lateen"].nominal_duration_s
    assert not any(step.via for step in EVOLUTIONS["set_lateen"].steps)  # no hoist
    for evo, kind, ended in (
        ("reef_lateen", "sail.reefed", "Reefed the mizzen; now set, 1 reef."),
        ("shake_out_lateen", "sail.reef_shaken_out", "Shook the reef out of the mizzen; now set."),
        ("take_in_lateen", "sail.taken_in", "Took in the mizzen; brailed up to its yard."),
        ("furl_lateen", "sail.furled", "Furled the mizzen on its yard."),
    ):
        runner.start(ship, evo, COURSE)
        _ticks, notes = _run(runner, ship)
        assert [n[1] for n in notes][-1] == kind and [n[2] for n in notes][-1] == ended, evo
    assert course.state is SailState.FURLED and course.reefs == 0


def test_the_lateen_evolutions_files_say_what_they_are():
    """The furl's work is aloft on the yard (Falconer 1780, YARD: the woldings); the take-in
    brails it to the gear; the trim is the sheet's script; each names its source and asks
    for hands of the afterguard."""
    furl = EVOLUTIONS["furl_lateen"]
    assert [(s.do, s.aloft) for s in furl.steps] == [("brail_up", False), ("furl", True)]
    assert [s.do for s in EVOLUTIONS["take_in_lateen"].steps] == ["brail_up"]
    assert EVOLUTIONS["trim_lateen_sheet"].script == "trim_sheet"
    for eid in (
        "set_lateen",
        "take_in_lateen",
        "furl_lateen",
        "reef_lateen",
        "shake_out_lateen",
        "trim_lateen_sheet",
    ):
        evo = EVOLUTIONS[eid]
        assert evo.applies_to == {"class": "lateen"} and evo.source, eid
        assert "afterguard" in evo.crew["stations"], eid


@pytest.mark.parametrize(
    "text, evolution",
    [
        ("set the mizen", "set_lateen"),
        ("brail up the mizen", "take_in_lateen"),
        ("brail in the mizen", "take_in_lateen"),
        ("clew up the mizen", "take_in_lateen"),
        ("haul up the mizen", "take_in_lateen"),
        ("lower the mizen", "take_in_lateen"),
        ("take in the mizen", "take_in_lateen"),
        ("furl the mizen", "furl_lateen"),
        ("reef the mizen", "reef_lateen"),
        ("trim the mizen", "trim_lateen_sheet"),
    ],
)
def test_the_mizens_orders_start_its_own_evolutions(text, evolution):
    """Ext §3.6: the vocabulary's rows for the lateen. "Furl the mizen" furls it aloft on its
    yard (E6), where a gaff sail keeps package 37l's refusal; "brail up the mizen" and the
    other take-in words of a sail brailed to its yard are taken."""
    ship = frigate_with_mizen_yard()
    runner = _bare(ship)
    course = ship.sails[COURSE]
    if evolution != "set_lateen":
        course.state = SailState.SET
        yard_trim.set_sheet_angle(ship, course, math.radians(60.0))  # eased, to be trimmed
    _kind, _words, data = orders.handle(ship, text)
    assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [(evolution, COURSE)]
    if evolution in ("take_in_lateen", "furl_lateen"):
        assert scripts.being_handed(ship, course)  # in HANDING_EVOLUTIONS: never laid aback
    _run(runner, ship)


def test_a_take_in_word_of_another_sail_is_refused_in_the_mizens_words():
    ship = frigate_with_mizen_yard()
    _bare(ship)
    ship.sails[COURSE].state = SailState.SET
    with pytest.raises(OrderError) as e:
        orders.handle(ship, "haul down the mizen")
    assert str(e.value) == (
        "A lateen sail is brailed up, not hauled down; say 'brail up the mizzen course' or 'take "
        "in the mizzen course'."
    )


def test_the_mizen_is_bent_unbent_and_shifted_from_the_sail_room():
    """The vocabulary's bend, unbend and shift rows for a lateen (Ext §3.6): the fixture's
    storm mizzen is bent in the course's place, so the shift has its case."""
    ship = frigate_with_mizen_yard()
    runner = _bare(ship)
    _kind, _words, data = orders.handle(ship, "unbend the mizen")
    assert [e["evolution"] for e in data["evolutions"]] == ["unbend_sail"]
    _run(runner, ship)
    assert ship.sails[COURSE].state is SailState.UNBENT
    _kind, _words, data = orders.handle(ship, "bend the mizen")
    assert [e["evolution"] for e in data["evolutions"]] == ["bend_sail"]
    _run(runner, ship)
    assert ship.sails[COURSE].state is SailState.FURLED
    _kind, _words, data = orders.handle(ship, "shift the mizen for the storm mizzen")
    assert [e["evolution"] for e in data["evolutions"]] == ["shift_sail"]
    _run(runner, ship)
    assert ship.sails["storm_mizzen"].state is not SailState.UNBENT
    assert ship.sails[COURSE].state is SailState.UNBENT


def test_a_whole_lateen_loads_sets_brails_and_furls_on_its_own_floor_and_drives_nothing():
    """Ext §3.7: a lateen with no key (the tartane's, a later package's) loads, is set on the
    lateen's floor, brailed up and furled by the same files, and is no driver and no boom
    sail; at helm's a-lee nothing hauls it aft."""
    ship = _ship(whole_lateen=True)
    course = ship.sails[COURSE]
    assert not course.cut_at_mast and course.curve_class == "lateen"
    runner = _bare(ship)
    for text, state in (
        ("set the mizen", SailState.SET),
        ("brail up the mizen", SailState.IN_THE_GEAR),
        ("set the mizen", SailState.SET),
    ):
        orders.handle(ship, text)
        _run(runner, ship)
        assert course.state is state, text
    assert _deg(course.sheet_angle) == LATEEN_FLOOR_DEG
    _under_plain_sail(ship)
    assert scripts.after_gaff_sails(ship) == [] and scripts.after_gaff_sails_all(ship) == []
    assert scripts.boom_sails(ship) == [] and not scripts.drives_aft(course)
    orders.handle(ship, "furl the mizen")
    _run(runner, ship)
    assert course.state is SailState.FURLED


def test_the_driver_is_called_the_spanker_only_while_it_is_a_gaff_sail():
    """Ext §3.5, the words: the log lines that name the driver say "the spanker" when every
    driver is a gaff sail (the frigate's, as always; a fore-and-after's, none at all, as before)
    and name the sail otherwise. With none set, the drivers bent say which: the fixture's
    course furled is still 'the mizzen', not a spanker she has not got; unbent, nothing names
    it, and the words are as they were."""
    frigate = frigate_with_mizen_yard()
    filed = _under_plain_sail(load_ship("data/ships/frigate-36.yaml"))
    assert scripts.driver_words(filed, scripts.after_gaff_sails(filed)) == "the spanker"
    assert scripts.driver_words(filed, []) == "the spanker"
    assert scripts.driver_words(load_ship("data/ships/cutter.yaml"), []) == "the spanker"
    course = frigate.sails[COURSE]
    assert scripts.driver_words(frigate, [course]) == "the mizzen"
    assert course.state is SailState.FURLED
    assert scripts.driver_words(frigate, []) == "the mizzen"
    course.state = SailState.UNBENT
    assert scripts.driver_words(frigate, []) == "the spanker"


# ---------------------------------------------------------------------------
# The gale and the cast: the driver's lists (Ext §3.5)
# ---------------------------------------------------------------------------


def test_the_gale_takes_in_the_course_at_the_third_reef():
    """`shorten sail`'s after sail (`orders.storm`, Luce 1884 p. 476): with the topsails going
    to their third reef the mainsail is hauled up and the driver taken in; at the second the
    course is left drawing, never reduced as a course (it is not in "courses": Ext §3.4)."""
    ship = _under_plain_sail(_ship())
    topsails = [s for s in ship.sails.values() if s.id.endswith(".topsail") and s.is_set]
    for sl in topsails:
        sl.reefs = 1
    assert not any("mizzen" in line for line in shorten_sail_lines(ship, 30.0))
    for sl in topsails:
        sl.reefs = 2
    lines = shorten_sail_lines(ship, 40.0)
    assert lines[:3] == [
        "take in the main course",
        "reef the fore course, one reef",
        "take in the mizzen course",
    ]


def test_the_cast_sets_the_course_with_its_sheet_drawn():
    """After the cast a ship sets her driver (`after_gaff_sails_all`, `_set_fore_and_aft`): the
    course, furled or brailed, is set and its sheet drawn to leeward of the tack at the gaff's
    trim."""
    ship = _ship()
    course = ship.sails[COURSE]
    ship.dyn.apparent_wind_angle = math.radians(-60.0)
    for state in (SailState.FURLED, SailState.IN_THE_GEAR):
        course.state = state
        scripts._set_fore_and_aft(ship, scripts.after_gaff_sails_all(ship), "larboard")
        assert course.is_set and _deg(course.sheet_angle) == pytest.approx(35.0, abs=0.01)
        assert yard_trim.read_sheet(ship, course).side == 1  # the larboard tack's lee: starboard


def test_the_rating_pass_rates_a_course_cut_at_the_mast_at_the_gaffs_peak():
    """Ext §10.2: the generator's rating pass (`tools/gen_ships.py`, `Builder.rate_spars`)
    loads the mizen yard with the course at the peak of the class whose curve drives it, the
    gaff's 1.29 (`PEAK_COEFF`); a whole lateen at the lateen's 1.25."""
    spec = importlib.util.spec_from_file_location(
        "gen_ships_for_lateen", ROOT / "tools" / "gen_ships.py"
    )
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    rated = {}
    for whole in (False, True):
        doc = _frigate_doc(whole_lateen=whole)
        yard = next(s for s in doc["spars"] if s["id"] == YARD)
        yard["rating_kn"] = gen.DesignLoad(1.0, 30.0)
        gen.Builder.rate_spars(SimpleNamespace(doc=doc, notes={}))
        course = next(s for s in doc["sails"] if s["id"] == COURSE)
        area, height = course["area_m2"], course["centre_height_m"]
        cls = "lateen" if whole else "gaff"
        want = round(gen.static_kn([(area, height, cls)], 30.0) * gen.SUSTAINED_FRACTION, 1)
        assert yard["rating_kn"] == want and type(yard["rating_kn"]) is float, cls
        rated[cls] = yard["rating_kn"]
    assert gen.PEAK_COEFF["gaff"] == 1.29 and gen.PEAK_COEFF["lateen"] == 1.25
    assert rated["gaff"] > rated["lateen"]


# ---------------------------------------------------------------------------
# The manoeuvres (Ext §3.5): the fixture sailing, seed 7
# ---------------------------------------------------------------------------


def _world(tmp_path, heading_deg: float = 300.0, knots: float = 15.0):
    """The fixture whole in a fifteen-knot northerly on the starboard tack, sixty degrees off
    the wind, under plain sail and settled with the yards trimmed, as the truths settle the
    frigate (`tests/test_known_truths.py`)."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading_deg,
        ship_speed_kn=4.0,
    )
    world = make_world(7, write_ship(_frigate_doc(), tmp_path, "mizen"), scenario)
    for text in ("set plain sail", "brace sharp up on the starboard tack"):
        world.submit(text)
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    assert world.ship.sails[COURSE].is_set
    return world


def _after(world, start: int) -> list:
    return [e for e in world.log if e.tick > start]


def _until(world, words: str, ticks: int) -> int:
    """Tick until a line with `words` is logged: its tick."""
    start = world.clock.tick
    for _ in range(ticks):
        world.tick()
        hit = [e for e in _after(world, start) if words in e.text]
        if hit:
            return hit[0].tick
    raise AssertionError(f"no '{words}' in {ticks} ticks: {[e.text for e in _after(world, start)]}")


def test_in_stays_the_course_is_hauled_aft_at_helms_a_lee_with_the_bowline_to_leeward(tmp_path):
    """Steel 1794 vol. II p. 316: "haul the mizen out, while you put at the same time the helm
    a-lee, ... brace the bowline quite to leeward", the yard not changed. At helm's a-lee the
    course's sheet is flat aft at the gaff's floor, the words say so, and its yard is not
    braced."""
    world = _world(tmp_path)
    course = world.ship.sails[COURSE]
    start = world.clock.tick
    world.submit("tack ship")
    _until(world, "Helm's a-lee", 400)
    line = next(e.text for e in _after(world, start) if "Helm's a-lee" in e.text)
    assert "haul aft the mizzen sheet and brace the bowline to leeward" in line, line
    assert course.is_set and _deg(course.sheet_angle) == pytest.approx(GAFF_FLOOR_DEG, abs=0.01)
    assert world.ship.spars[YARD].brace_angle == 0.0


def test_hanging_in_stays_the_course_is_hauled_over_to_windward_with_no_boom(tmp_path):
    """Ext §3.5: a boom sail is hauled over to windward if she hangs in stays (`boom_sails`,
    `TackScript._hang`), and so is the course, by its sheet: the words name the sail, not a
    boom the mizen has not got (the frigate's are "the spanker boom hauled over to windward",
    `tests/test_staying.py`). The tack is made to hang at helm's a-lee, as though her way were
    gone then, to read its words and the course's sheet."""
    world = _world(tmp_path)
    course = world.ship.sails[COURSE]
    world.submit("tack ship")
    _until(world, "Helm's a-lee", 400)
    runner = world.ship.extra["evolutions"]
    (tack,) = [i.script for i in runner.instances if isinstance(i.script, scripts.TackScript)]
    assert tack.booms == [course]
    tack._hang()
    (line,) = [n[2] for n in world.ship.drain_notes() if "hangs in stays" in n[2]]
    assert line.endswith("; the mizzen hauled over to windward."), line
    assert "boom" not in line
    assert yard_trim.read_sheet(world.ship, course).side == 1  # the old weather: starboard


def test_hove_to_the_course_is_brailed_up(tmp_path):
    """Hove to with the main topsail to the mast the driver is brailed up (`after_gaff_sails`;
    package 10's frigate, which came head to wind with sternway with it set)."""
    world = _world(tmp_path)
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(600):
        world.tick()
    texts = [e.text for e in _after(world, start)]
    assert any(e.kind == "ship.hove_to" for e in _after(world, start)), texts
    assert any("brailed up the mizzen" in t for t in texts), texts
    assert world.ship.sails[COURSE].state is SailState.IN_THE_GEAR


def test_wearing_the_course_is_brailed_at_up_helm_and_hauled_out_by_the_wind(tmp_path):
    """Steel 1794 vol. II pp. 321-322: the mizen hauled up as she bears up, hauled out once the
    wind is on the new quarter: brailed at "up helm", in the gear while she goes round, set
    again by the wind on the new tack."""
    world = _world(tmp_path)
    course = world.ship.sails[COURSE]
    start = world.clock.tick
    world.submit("wear ship")
    up_tick = _until(world, "Up helm", 200)
    assert course.state is SailState.IN_THE_GEAR
    up = next(e.text for e in _after(world, start) if "Up helm" in e.text)
    assert "brail up the mizzen" in up, up
    going_round = []  # the course's state each tick until it is hauled out
    for _ in range(1500):
        world.tick()
        if any("Haul out the mizzen!" in e.text for e in _after(world, up_tick)):
            break
        going_round.append(course.state)
    else:
        raise AssertionError("no 'Haul out the mizzen!' in 1500 ticks")
    assert going_round and set(going_round) == {SailState.IN_THE_GEAR}
    assert course.is_set and world.ship.dyn.tack == "larboard"


def test_getting_under_way_the_course_is_set_after_the_cast(tmp_path):
    """Getting under way from the road at seed 7 (`tests/test_anchor.py`'s outer road in
    Falmouth): when she has cast, the head yards are braced round and the driver set, the
    words naming the course, not a spanker she has not got."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
        position={"lat_deg": 50.133, "lon_deg": -5.035},
        region="channel-west",
    )
    world = make_world(7, write_ship(_frigate_doc(), tmp_path, "mizen"), scenario)
    world.run(60)
    assert world.submit("let go the best bower").kind == "order.accepted"
    world.run(900)
    assert world.ship.sails[COURSE].state is SailState.FURLED
    assert world.submit("get under way").kind == "order.accepted"
    cast = _until(world, "right the helm", 3600)
    line = next(e.text for e in world.log if e.tick == cast and "right the helm" in e.text)
    assert line.endswith("right the helm, brace round the head yards, set the mizzen."), line
    assert world.ship.sails[COURSE].is_set
