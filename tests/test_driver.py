"""Package 75, the engine's driver step (B3.5; docs/design/Design-ShipsEngineExtensions.md §17,
§16 item 8): the driver of the 64 and the 74, Steel's driver boomsail.

The driver is a four-sided sail on the mizzen mast: its luff laced to the mast, its head along
the mizen yard and on past the yard's peak on Steel's driver yard, its foot spread on a boom
over the stern (Steel 1794 vol. I, DRIVER BOOMSAIL, OCR l. 13816-13843). It is class `lateen`
cut at the mast, the course's class and key, so the physics reads it with the gaff's curve and
trim through `Sail.curve_class` (B3.1), and its boom by its role, as every fore-and-aft sail's
(Ext §17.4: nothing in `freesail/physics/` or `data/sail_classes.yaml` changes). It is filed in
the mizen course's place and starts in the sail room; it is bent by "shift the mizen for the
driver", the storm mizzen's way, Steel's second way "instead of the mizen" (l. 24523-24538),
and shifted back as *Venus* bent her mizen again in 1794 (Jackson vol. 1, OCR l. 11064-11076).
Bent, it is her driver on every path that works one (`drives_aft`, Ext §3.5).

The engine's change is one membership (Ext §17.4): two sails bent in one place are rivals
(`scripts._in_each_others_place`), so the storm mizzen, also in the course's place, is never
bent beside the driver; `orders/storm.py`'s own copy of the rule calls it. And `set_lateen`
wants the sail's boom standing (Ext §16 item 8), which the course, naming none, never asks.

No file of the eight carries a lateen naming a boom (`tests/test_rig_classing.py`, the probe),
and no file names one place twice but for a driver's (below, on every file), so nothing filed
moves; no sail is in its own place, so none is shifted for itself. The tests run on the fixture
`frigate_with_driver()` alone (`tests/rig_fixtures.py`), the 0E frigate with the 64's driver on
her boom. The 64 carries her own since B1's `DRIVER` flip at her stage B, and her own cases are
in `tests/test_indefatigable.py`.

The boom goes with the sail (Ext §17.11, the owner's choice, "with the shift"): out only while
the driver is bent, on the engine's own `Spar.rigged_out`, filed on the driver's boom alone
(`scripts.driver_boom`). Its class stays `boom`, so `RIGGED_IN_CLASSES`, `studding_work` and
`StuddingSailsIn` never touch it: it does not come in for a tack or a wear, and it stays out
while the driver is brailed. The evidence is thin and the judgement plain: Steel's p. 49 column
gives her no driver boom ("0 0"), Steel bends the driver "as a temporary matter" (OCR l.
24523-24538), and Lever has it "set like a lower Studding Sail" (OCR l. 9904); no source says what
became of the boom while the mizen drew. 120 s each way, judgement. Nothing in `freesail/physics/`
or `freesail/combat/` reads the state, so the stowed boom keeps its windage at its file's place
and can be hit by a shot: a small untruth, said plainly and accepted there. A boom whose file
does not say `rigged_out` is worked as it was, which keeps the key inert until a ship's file
carries it: the toggle, below, is the proof.
"""

from __future__ import annotations

import math
import pickle
import random
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from rig_fixtures import DRIVER_CANVAS_NO, frigate_with_driver, frigate_with_driver_doc, write_ship

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.storm import _in_its_place, shorten_sail_lines
from freesail.physics import strain
from freesail.physics.sails import compute_sail_forces
from freesail.physics.wind import Wind, WindParams
from freesail.ship import parts
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState
from freesail.ship.stub import OrderError
from freesail.world.ships import (
    POLAR_ANGLES_DEG,
    POLAR_WINDS_KN,
    _balanced_speed_ms,
    _rigged_for_plain_sail,
    _trim_for,
    polar_of,
)

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = ROOT / "data" / "ships" / "frigate-36.yaml"
DRIVER = "mizzen.driver"
COURSE = "mizzen.course"
STORM = "storm_mizzen"
BOOM = "mizzen.boom"
YARD = "mizzen.yard"

# The gaff's sheet range (`evolutions.trim.TRIM_RANGE`), which a sail cut at the mast takes.
GAFF_FLOOR_DEG, CEILING_DEG = 18.0, 85.0
# Thirty degrees of apparent wind on the larboard bow: the gaff's best angle, 25 degrees off,
# is below its floor, so a sheet trimmed for it lies at the floor.
CLOSE = math.radians(-30.0)
# The course's canvas, the frigate's spanker's (`rig_fixtures._mizen_course`).
COURSE_CANVAS_NO = 2

# The shift's phases and their times at the file's (`data/evolutions/shift_sail.yaml`, all
# judgement): a drawing sail taken in, unbent, sent down while the new one is swayed up, bent
# and set; a furled one shifted where it hangs. The driver's boom goes with it, 120 s each way
# (`scripts.DRIVER_BOOM_S`, judgement; Ext §17.11): rigged out before the driver is bent, and
# rigged in after it is unbent.
SHIFT_S = {"take_in": 90, "unbend": 180, "send_up": 150, "bend": 240, "set": 120}
SHIFT_OUT_S = {
    "take_in": 90,
    "unbend": 180,
    "send_up": 150,
    "rig_out_boom": 120,
    "bend": 240,
    "set": 120,
}
SHIFT_BACK_S = {
    "take_in": 90,
    "unbend": 180,
    "rig_in_boom": 120,
    "send_up": 150,
    "bend": 240,
    "set": 120,
}

LIGHT_AIRS = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))


def _bare(ship: Ship, awa: float = CLOSE) -> Runner:
    """A bare ship's runner, the deck reading `awa` of apparent wind, enough to trim to."""
    runner = Runner(ship)
    ship.dyn.apparent_wind_angle = awa
    ship.dyn.apparent_wind_speed = 6.0
    return runner


def _run(runner: Runner, ship: Ship, max_ticks: int = 3000) -> tuple[int, list]:
    """Tick the runner (no physics) until nothing is in hand: the ticks and the notes."""
    ticks, notes = 0, []
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return ticks, notes


def _phases(runner: Runner, ship: Ship, max_ticks: int = 3000) -> tuple[dict, list]:
    """Tick the runner as `_run` does: the phases of the work in hand, each with its ticks in
    the order they ran (`None`, work that is not in phases), and the notes."""
    taken: dict[str | None, int] = {}
    notes, ticks = [], 0
    while runner.in_progress() and ticks < max_ticks:
        phase = getattr(runner.instances[0].script, "phase", None) if runner.instances else None
        taken[phase] = taken.get(phase, 0) + 1
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return taken, notes


def _where_it_hangs(phases: dict[str, int]) -> dict[str, int]:
    """A shift's phases with the old sail furled: not taken in, and the new one left furled."""
    return {name: s for name, s in phases.items() if name not in ("take_in", "set")}


def _ran(taken: dict) -> list:
    return list(taken.items())


def _refusal(ship: Ship, text: str) -> str:
    with pytest.raises(OrderError) as e:
        orders.handle(ship, text)
    return str(e.value)


def _deg(angle: float) -> float:
    return round(math.degrees(abs(angle)), 3)


def _in_the_room(ship: Ship) -> list[tuple[str, int | None]]:
    """The spares of the course and the driver in the sail room, with their canvas."""
    room = parts.sail_room(ship)
    return [(s.kind, s.canvas_no) for s in room.sails if s.kind in (COURSE, DRIVER)]


def _set_and_drawing(ship: Ship, awa: float = CLOSE) -> Runner:
    """The bent fixture's driver set by its own evolution, `awa` off the apparent wind."""
    runner = _bare(ship, awa)
    orders.handle(ship, "set the driver")
    _run(runner, ship)
    assert ship.sails[DRIVER].is_set
    return runner


# ---------------------------------------------------------------------------
# The shift and the one place (Ext §17.3, §17.4)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("drawing", [True, False])
def test_the_mizen_is_shifted_for_the_driver_and_back_each_to_its_end(drawing):
    """Ext §17.3, §17.7 and §17.11: "shift the mizen for the driver" runs `shift_sail` on the
    course, the storm mizzen's way. A drawing course is taken in, unbent, sent down while the
    driver is swayed up, the boom rigged out, the driver bent and set: 900 s at the file's times
    (780 s before the boom's phase), the hands' factor 1 with no company aboard. A furled course
    is shifted where it hangs, in 690 s (570), and the driver left furled. Back, the boom comes
    in after the driver is unbent, the same times. While the driver is bent the sail room holds
    the course's canvas, No. 2, in the driver's spare's stead, so the count of spares stands;
    shifted back, the same, the driver's No. 5 below again."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    course, driver = ship.sails[COURSE], ship.sails[DRIVER]
    spares = scripts.spare_sails(ship)
    assert driver.state is SailState.UNBENT and course.state is SailState.FURLED
    assert _in_the_room(ship) == [(DRIVER, DRIVER_CANVAS_NO)]
    if drawing:
        course.state = SailState.SET
    left = "set" if drawing else "furled"
    for text, (old, old_name, old_no), (new, new_name, new_no), phases, whole in (
        (
            "shift the mizen for the driver",
            (course, "mizzen", COURSE_CANVAS_NO),
            (driver, "driver", DRIVER_CANVAS_NO),
            SHIFT_OUT_S,
            900 if drawing else 690,
        ),
        (
            "shift the driver for the mizen",
            (driver, "driver", DRIVER_CANVAS_NO),
            (course, "mizzen", COURSE_CANVAS_NO),
            SHIFT_BACK_S,
            900 if drawing else 690,
        ),
    ):
        _kind, _words, data = orders.handle(ship, text)
        assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [
            ("shift_sail", old.id)
        ]
        taken, notes = _phases(runner, ship)
        want = phases if drawing else _where_it_hangs(phases)
        assert _ran(taken) == list(want.items()), text
        assert sum(taken.values()) == whole, text
        assert [n[2] for n in notes if n[1] == "sail.shifted"] == [
            f"Shifted the {old_name}; the {new_name} bent (No. {new_no} canvas, new) and "
            f"{left}, {spares} spare sails left in the sail room."
        ]
        assert old.state is SailState.UNBENT
        assert new.state is (SailState.SET if drawing else SailState.FURLED)
        assert _in_the_room(ship) == [(old.id, old_no)]
        assert scripts.spare_sails(ship) == spares
        assert ship.sails[STORM].state is SailState.UNBENT


def test_the_driver_is_bent_only_by_the_shift_while_the_course_is_bent():
    """Ext §17.3: "bend the driver" with the course bent is refused by `_SailWork._rival` in its
    existing words, which name the shift."""
    ship = frigate_with_driver()
    _bare(ship)
    assert _refusal(ship, "bend the driver") == (
        "The mizzen driver: The mizzen is bent in the driver's place; unbend it first, or shift "
        "the mizzen for the driver."
    )


def test_the_storm_mizzen_and_the_driver_are_rivals_for_the_courses_place():
    """Ext §17.4, the one-place rule: the storm mizzen and the driver are each filed in the
    course's place, so each holds the other's (`_in_each_others_place`). With the driver bent,
    "bend the storm mizzen" (and "bend the mizen") is refused in words naming the driver, and
    "shift the driver for the storm mizzen" runs; with the storm mizzen bent, "bend the driver"
    is refused naming it, and the shift back runs. `orders/storm.py` finds the rival by the same
    rule (`_in_its_place`). Measured on the rule's absence (the old `_in_each_others_place`
    patched in): "bend the storm mizzen" bent it beside the driver, the two bent together, and
    the shift was refused, "The storm mizzen is not bent in the driver's place"."""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    course, driver, storm = (ship.sails[s] for s in (COURSE, DRIVER, STORM))
    assert scripts._in_each_others_place(driver, storm)
    assert scripts._in_each_others_place(storm, driver)
    assert _in_its_place(ship, storm) is driver
    assert _refusal(ship, "bend the storm mizzen") == (
        "The storm mizzen: The driver is bent in the storm mizzen's place; unbend it first, or "
        "shift the driver for the storm mizzen."
    )
    assert _refusal(ship, "bend the mizen") == (
        "The mizzen course: The driver is bent in the mizzen's place; unbend it first, or shift "
        "the driver for the mizzen."
    )
    _kind, _words, data = orders.handle(ship, "shift the driver for the storm mizzen")
    assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [("shift_sail", DRIVER)]
    _run(runner, ship)
    assert (course.state, driver.state, storm.state) == (
        SailState.UNBENT,
        SailState.UNBENT,
        SailState.FURLED,
    )
    assert _in_its_place(ship, driver) is storm
    assert _refusal(ship, "bend the driver") == (
        "The mizzen driver: The storm mizzen is bent in the driver's place; unbend it first, or "
        "shift the storm mizzen for the driver."
    )
    orders.handle(ship, "shift the storm mizzen for the driver")
    _run(runner, ship)
    assert (driver.state, storm.state) == (SailState.FURLED, SailState.UNBENT)


@pytest.mark.parametrize(
    "path", sorted((ROOT / "data" / "ships").glob("*.yaml")), ids=lambda p: p.stem
)
def test_on_every_file_the_one_place_rule_is_the_rule_it_was(path):
    """Ext §17.4: inert on the files. Each names a place once at most, a driver's place left
    aside (thirteen `in_place_of` keys on the eight, and the storm mizzen's on each of the 64's
    and the razee's files), so for every two sails of every file, and for every sail with
    itself, the rule widened to one shared place answers as it did before. The one answer it may
    move is the one it was widened for, two sails in one place with a driver among them (a
    lateen cut at the mast naming a boom): the 64's driver and her storm mizzen since B1's
    `DRIVER` flip at her stage B, as on the fixture.
    Measured without the rule's `a is not b`: on all ten files a sail filed in another's place
    held its own, and "shift the storm mizzen for the storm mizzen" answered "The storm mizzen
    is bent already." (below, the words it had)."""
    ship = load_ship(str(path))
    drivers = {s.id for s in ship.sails.values() if s.cut_at_mast and ship.spar_of_role(s, "boom")}
    places = [
        s.in_place_of
        for s in ship.sails.values()
        if s.in_place_of is not None and s.id not in drivers
    ]
    assert len(places) == len(set(places)), places
    for a in ship.sails.values():
        for b in ship.sails.values():
            old = a.in_place_of == b.id or b.in_place_of == a.id
            shared = a is not b and a.in_place_of is not None and a.in_place_of == b.in_place_of
            if shared and drivers & {a.id, b.id}:
                assert scripts._in_each_others_place(a, b), (a.id, b.id)
            else:
                assert scripts._in_each_others_place(a, b) is old, (a.id, b.id)


@pytest.mark.parametrize(
    "path, sail",
    [(FRIGATE, "storm mizzen"), (ROOT / "data" / "ships" / "lugger.yaml", "storm jib")],
    ids=["frigate-36", "lugger"],
)
def test_no_sail_is_shifted_for_itself_in_the_words_it_had(path, sail):
    """The gate (Ext §1, §11: no existing file's behaviour moves): the occasional sail bent in
    its working sail's place and shifted for itself is refused at `ShiftScript.check`'s place
    check, in the words it had before package 75, which name the remedy; and so is the driver
    on the fixture. With the one-place rule true of a sail and itself these answered "The storm
    mizzen is bent already." and "The storm jib is bent already."."""
    ship = load_ship(str(path))
    occasional = scripts._sail_named(ship, sail)
    ship.sails[occasional.in_place_of].state = SailState.UNBENT
    occasional.state = SailState.FURLED
    _bare(ship)
    assert _refusal(ship, f"shift the {sail} for the {sail}") == (
        f"The {sail}: The {sail} is not bent in the {sail}'s place; shift the {sail} for another "
        "of its kind."
    )
    ship = frigate_with_driver(bent=True)
    _bare(ship)
    assert _refusal(ship, "shift the driver for the driver") == (
        "The mizzen driver: The driver is not bent in the driver's place; shift the driver for "
        "another of its kind."
    )


def test_the_driver_is_not_set_on_a_wrecked_boom_and_the_course_never_asks_for_one():
    """Ext §16 item 8: `set_lateen` wants the sail's boom standing, as `set_gaff` does. With the
    boom wrecked the driver is refused, and a boom carried away while it is being set fails the
    set; the course names no boom (`spar_of_role` none) and sets as before. Measured without
    the line: the driver set on its wrecked boom in 90 s, as the course does."""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    ship.spars[BOOM].wrecked = True
    assert _refusal(ship, "set the driver") == "The mizzen driver: the driver's boom is wrecked."
    ship.spars[BOOM].wrecked = False
    orders.handle(ship, "set the driver")
    for _ in range(20):
        runner.step(ship, 1.0, LIGHT_AIRS)
    ship.spars[BOOM].wrecked = True
    _ticks, notes = _run(runner, ship)
    assert "Could not set the driver: the driver's boom is wrecked." in [n[2] for n in notes]
    assert not ship.sails[DRIVER].is_set
    ship = frigate_with_driver()
    runner = _bare(ship)
    ship.spars[BOOM].wrecked = True
    assert ship.spar_of_role(ship.sails[COURSE], "boom") is None
    orders.handle(ship, "set the mizen")
    ticks, _notes = _run(runner, ship)
    assert ship.sails[COURSE].is_set and ticks == 90


# ---------------------------------------------------------------------------
# The boom rigged out with the driver (Ext §17.11)
# ---------------------------------------------------------------------------


def test_the_boom_is_in_with_the_driver_in_the_sail_room_and_out_while_it_is_bent():
    """Ext §17.11: filed rigged in, it stays in however the course is worked; filed bent, it is
    out, and it stays out while the driver is set, brailed and furled. `driver_boom` finds it
    from the driver alone: the course and the storm mizzen name no boom."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    boom = ship.spars[BOOM]
    assert ship.sails[DRIVER].state is SailState.UNBENT and boom.rigged_out is False
    assert scripts.driver_boom(ship, ship.sails[DRIVER]) is boom
    assert scripts.driver_boom(ship, ship.sails[COURSE]) is None
    assert scripts.driver_boom(ship, ship.sails[STORM]) is None
    for text in ("set the mizen", "trim the mizen", "take in the mizen", "furl the mizen"):
        orders.handle(ship, text)
        _run(runner, ship)
        assert boom.rigged_out is False, text
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    boom = ship.spars[BOOM]
    assert ship.sails[DRIVER].state is SailState.FURLED and boom.rigged_out is True
    for text in ("set the driver", "trim the driver", "take in the driver", "furl the driver"):
        orders.handle(ship, text)
        _run(runner, ship)
        assert boom.rigged_out is True, text


def test_the_boom_goes_out_before_the_bend_and_comes_in_after_the_unbend():
    """Ext §17.11, tick by tick, the phase in hand, the boom out, the driver bent, each change
    once. Shifted to the driver, or bent, the boom is out before the bend begins and the driver
    bent when it ends; shifted from it, or unbent, the driver is unbent first and the boom in
    when `rig_in_boom` ends. So the driver is never bent with the boom in."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    boom, driver = ship.spars[BOOM], ship.sails[DRIVER]

    def changes(text: str) -> list[tuple[str, bool, bool]]:
        orders.handle(ship, text)
        script = runner.instances[0].script
        seen = [(script.phase, boom.rigged_out, driver.state is not SailState.UNBENT)]
        while runner.in_progress():
            runner.step(ship, 1.0, LIGHT_AIRS)
            ship.drain_notes()
            now = (script.phase, boom.rigged_out, driver.state is not SailState.UNBENT)
            if now != seen[-1]:
                seen.append(now)
        return seen

    assert changes("shift the mizen for the driver") == [
        ("unbend", False, False),
        ("send_up", False, False),
        ("rig_out_boom", False, False),
        ("bend", True, False),
        ("done", True, True),
    ]
    assert changes("shift the driver for the mizen") == [
        ("unbend", True, True),
        ("rig_in_boom", True, False),
        ("send_up", False, False),
        ("bend", False, False),
        ("done", False, False),
    ]
    orders.handle(ship, "unbend the mizen")
    _run(runner, ship)
    assert changes("bend the driver") == [
        ("send_up", False, False),
        ("rig_out_boom", False, False),
        ("bend", True, False),
        ("done", True, True),
    ]
    assert changes("unbend the driver") == [
        ("unbend", True, True),
        ("lower", True, True),
        ("rig_in_boom", True, False),
        ("done", False, False),
    ]


def test_bend_the_driver_and_unbend_it_take_the_boom_and_the_course_leaves_it():
    """Ext §17.11, old beside new at the file's times: "bend the driver" send_up 120, rig_out_boom
    120, bend 240, the whole 480 s (360); "unbend the driver" unbend 180, lower 90, rig_in_boom
    120, the whole 390 s (270). "Bend the mizen" and "unbend the mizen" are as they were, 360 and
    270 s, and the boom is not touched. The log says the boom's work in the period's words, as
    `rig_out_studdingsail_boom.yaml` says its own."""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    boom = ship.spars[BOOM]
    orders.handle(ship, "unbend the driver")
    taken, notes = _phases(runner, ship)
    assert _ran(taken) == [("unbend", 180), ("lower", 90), ("rig_in_boom", 120)]
    assert "Rigged in the driver boom." in [n[2] for n in notes]
    assert boom.rigged_out is False and ship.sails[DRIVER].state is SailState.UNBENT
    orders.handle(ship, "bend the mizen")
    taken, notes = _phases(runner, ship)
    assert _ran(taken) == [("send_up", 120), ("bend", 240)]
    assert boom.rigged_out is False and not any("boom" in n[2] for n in notes)
    orders.handle(ship, "unbend the mizen")
    taken, notes = _phases(runner, ship)
    assert _ran(taken) == [("unbend", 180), ("lower", 90)]
    assert boom.rigged_out is False and not any("boom" in n[2] for n in notes)
    orders.handle(ship, "bend the driver")
    taken, notes = _phases(runner, ship)
    assert _ran(taken) == [("send_up", 120), ("rig_out_boom", 120), ("bend", 240)]
    assert "Rigged out the driver boom." in [n[2] for n in notes]
    assert boom.rigged_out is True and ship.sails[DRIVER].state is SailState.FURLED


def test_the_storm_mizzen_is_shifted_with_the_boom_going_only_for_the_driver():
    """Ext §17.11: the phase goes by the sail shifted. From the driver to the storm mizzen the boom
    comes in, 690 s; from the storm mizzen to the driver it goes out, 690 s; between the course
    and the storm mizzen it is not touched, 570 s, as it was. The storm mizzen and the driver both
    hold the course's place (Ext §17.4)."""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    boom = ship.spars[BOOM]
    orders.handle(ship, "shift the driver for the storm mizzen")
    taken, _notes = _phases(runner, ship)
    assert _ran(taken) == list(_where_it_hangs(SHIFT_BACK_S).items())
    assert sum(taken.values()) == 690 and boom.rigged_out is False
    orders.handle(ship, "shift the storm mizzen for the driver")
    taken, _notes = _phases(runner, ship)
    assert _ran(taken) == list(_where_it_hangs(SHIFT_OUT_S).items())
    assert sum(taken.values()) == 690 and boom.rigged_out is True
    ship = frigate_with_driver()
    runner = _bare(ship)
    boom = ship.spars[BOOM]
    orders.handle(ship, "shift the mizen for the storm mizzen")
    taken, notes = _phases(runner, ship)
    assert _ran(taken) == [("unbend", 180), ("send_up", 150), ("bend", 240)]
    assert boom.rigged_out is False and not any("boom" in n[2] for n in notes)


def test_a_driver_shifted_for_another_keeps_the_one_boom_out():
    """Ext §17.11 read for the case its table does not name: "shift the driver" with another
    driver in the sail room is the one boom for both sails, so neither phase runs and the boom
    stays out, the 570 s it was. (Rigged in and out again it would be 240 s of no work.)"""
    doc = frigate_with_driver_doc(bent=True)
    doc["crew"]["stores"]["sails"].append(
        {"kind": DRIVER, "canvas_no": DRIVER_CANVAS_NO, "condition": 100}
    )
    ship = ship_from_dict(doc, "tests/test_driver.py:two-drivers")
    runner = _bare(ship)
    orders.handle(ship, "shift the driver")
    taken, _notes = _phases(runner, ship)
    assert _ran(taken) == [("unbend", 180), ("send_up", 150), ("bend", 240)]
    assert ship.spars[BOOM].rigged_out is True and ship.sails[DRIVER].state is SailState.FURLED


def _carry_away_the_boom(ship: Ship) -> None:
    """The boom carried away as a shot or the strain does it, the driver with it in the part
    graph, bent or in the sail room (`strain._wreck_spar`, `Ship.dependents`)."""
    strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[BOOM], 2.0)
    ship.drain_notes()


def _with_a_spare_boom(bent: bool = False) -> Ship:
    """The fixture with a spare of the boom's class on the booms: `frigate-36.yaml` has none."""
    doc = frigate_with_driver_doc(bent)
    doc["crew"]["stores"]["spare_spars"]["boom"] = 1
    return ship_from_dict(doc, "tests/test_driver.py:spare-boom")


def _clear_and_replace_the_boom(runner: Runner, ship: Ship) -> None:
    runner.start(ship, "clear_wreck", BOOM, {"part": BOOM})
    _run(runner, ship)
    runner.start(ship, "shift_spar", BOOM, {"part": BOOM})
    _run(runner, ship)
    assert not ship.spars[BOOM].wrecked


def test_a_driver_is_refused_on_a_boom_carried_away_in_the_wrecks_words():
    """Ext §17.11, closing §17.10 item 6 for the driver: "shift the mizen for the driver" set it
    on a wrecked boom. Now it is refused in `_wreck_refusal`'s words, naming the driver (it lies in
    the sail room, so it hangs in no wreck), while the wreck hangs and after it is cleared, and
    nothing moves: the course as it was, the room as it was. "Bend the driver" was refused
    already, and stands. The spare lands rigged in. The other sails' gap stands: `driver_boom` is
    the only way in, and a sail's shift over any other wrecked spar is as it was."""
    ship = _with_a_spare_boom()
    runner = _bare(ship)
    course, driver, boom = ship.sails[COURSE], ship.sails[DRIVER], ship.spars[BOOM]
    course.state = SailState.SET
    room = _in_the_room(ship)
    _carry_away_the_boom(ship)
    assert boom.wrecked and driver.wrecked and not course.wrecked
    assert _refusal(ship, "shift the mizen for the driver") == (
        "The mizzen course: The wreck of the driver boom still hangs aloft; cut it away and shift "
        "the driver boom for a spare before the driver can be bent."
    )
    assert _refusal(ship, "bend the driver") == (
        "The mizzen driver went with the mizzen boom when it carried away; cut away the wreck, "
        "then shift the mizzen boom for a spare."
    )
    # from the storm mizzen's side the same, whichever sail holds the place
    course.state, ship.sails[STORM].state = SailState.UNBENT, SailState.FURLED
    assert _refusal(ship, "shift the storm mizzen for the driver") == (
        "The storm mizzen: The wreck of the driver boom still hangs aloft; cut it away and shift "
        "the driver boom for a spare before the driver can be bent."
    )
    course.state, ship.sails[STORM].state = SailState.SET, SailState.UNBENT
    runner.start(ship, "clear_wreck", BOOM, {"part": BOOM})
    _run(runner, ship)
    assert boom.wrecked and boom.sent_down
    assert _refusal(ship, "shift the mizen for the driver") == (
        "The mizzen course: The driver boom is carried away; shift it for a spare first."
    )
    assert course.state is SailState.SET and driver.state is SailState.UNBENT
    assert _in_the_room(ship) == room and boom.rigged_out is False
    runner.start(ship, "shift_spar", BOOM, {"part": BOOM})
    _run(runner, ship)
    assert not boom.wrecked and boom.rigged_out is False
    # the key absent, the shift is taken as it was (Ext §17.10 item 6)
    ship = ship_from_dict(_key_absent(), "tests/test_driver.py:toggle")
    _bare(ship)
    _carry_away_the_boom(ship)
    assert orders.handle(ship, "shift the mizen for the driver")[0] == "evolution.started"


def test_a_driver_hit_on_the_booms_is_whole_again_with_the_spare():
    """Ext §17.11: the stowed boom can be hit. The driver, in the sail room all along and marked
    with the wreck by the part graph, is whole again when the wreck is cleared, and the spare's
    gear reeves its lines, so it can be bent and it draws. Old beside new: `driver.wrecked` stood
    through the spare, 4 of its lines unrove, the log saying "the driver may be bent to it again"
    while "bend the driver" answered "The mizzen driver is wrecked." and the shift set a sail that
    never drew (`is_set` false) and could not be taken in. With no key on the file it is as it
    was, the frigate's ringtail's gap, which stands for its own ruling."""
    ship = _with_a_spare_boom()
    runner = _bare(ship)
    course, driver, boom = ship.sails[COURSE], ship.sails[DRIVER], ship.spars[BOOM]
    course.state = SailState.SET
    _carry_away_the_boom(ship)
    assert driver.wrecked and driver.state is SailState.UNBENT
    assert any(ln.wrecked for ln in ship.lines.values() if ln.of == DRIVER)
    runner.start(ship, "clear_wreck", BOOM, {"part": BOOM})
    _run(runner, ship)
    assert not driver.wrecked and boom.sent_down
    assert _refusal(ship, "shift the mizen for the driver") == (
        "The mizzen course: The driver boom is carried away; shift it for a spare first."
    )
    assert _refusal(ship, "bend the driver") == (
        "The mizzen driver: The driver boom is carried away; shift it for a spare first."
    )
    runner.start(ship, "shift_spar", BOOM, {"part": BOOM})
    _run(runner, ship)
    assert not any(ln.wrecked for ln in ship.lines.values() if ln.of == DRIVER)
    orders.handle(ship, "shift the mizen for the driver")
    _run(runner, ship)
    assert driver.is_set and not driver.wrecked and boom.rigged_out is True
    orders.handle(ship, "take in the driver")
    _run(runner, ship)
    assert driver.state is not SailState.SET

    doc = _key_absent()
    doc["crew"]["stores"]["spare_spars"]["boom"] = 1
    ship = ship_from_dict(doc, "tests/test_driver.py:toggle")
    runner = _bare(ship)
    _carry_away_the_boom(ship)
    _clear_and_replace_the_boom(runner, ship)
    assert ship.sails[DRIVER].wrecked


def test_a_driver_is_refused_over_a_mizen_yard_carried_away_from_the_storm_mizzens_side():
    """Ext §17.11, closing §17.10 item 6 for the driver: its head is on the yard as its foot is on
    the boom. The course hangs on the yard, so `_find` refuses its shift; the storm mizzen hangs
    on the mast alone, and old beside new, "shift the storm mizzen for the driver" was taken over
    a yard carried away: the driver set and wrecked in the wreck, or, the wreck cleared, furled on
    a yard lying on deck, the boom out, and no order left to bring either back, the storm mizzen
    lost with it, since no spare lateen yard is carried. Now it is refused in `_wreck_refusal`'s
    words, and nothing moves. The key absent, it is taken as it was, and the other sails' gap
    stands."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    storm_mizzen, boom = ship.sails[STORM], ship.spars[BOOM]
    ship.sails[COURSE].state = SailState.UNBENT
    storm_mizzen.state = SailState.FURLED
    room = _in_the_room(ship)
    strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[YARD], 2.0)
    ship.drain_notes()
    assert not boom.wrecked and not storm_mizzen.wrecked
    assert _refusal(ship, "shift the storm mizzen for the driver") == (
        "The storm mizzen: The wreck of the mizzen yard still hangs aloft; cut it away and shift "
        "the mizzen yard for a spare before the driver can be bent."
    )
    runner.start(ship, "clear_wreck", YARD, {"part": YARD})
    _run(runner, ship)
    assert _refusal(ship, "shift the storm mizzen for the driver") == (
        "The storm mizzen: The mizzen yard is carried away; shift it for a spare first."
    )
    assert storm_mizzen.state is SailState.FURLED and boom.rigged_out is False
    assert ship.sails[DRIVER].state is SailState.UNBENT and _in_the_room(ship) == room

    ship = ship_from_dict(_key_absent(), "tests/test_driver.py:toggle")
    _bare(ship)
    ship.sails[COURSE].state = SailState.UNBENT
    ship.sails[STORM].state = SailState.FURLED
    strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[YARD], 2.0)
    ship.drain_notes()
    assert orders.handle(ship, "shift the storm mizzen for the driver")[0] == "evolution.started"


@pytest.mark.parametrize("unbent_first", [True, False], ids=["unbent", "cut-out"])
def test_a_boom_carried_away_is_passed_over_and_its_spare_lands_rigged_in(unbent_first):
    """Ext §17.11: with the boom carried away under the driver, "unbend the driver" is unbend and
    lower, 270 s, and no hands go to a boom that is gone; or the wreck's own clearing takes the
    sail out to the sail room. Either way the driver is below, so the spare boom lands rigged in,
    and the course can be bent with no boom beside it. (Measured without the line in
    `ShiftSparScript`: the spare stood rigged out with the driver in the sail room.)"""
    ship = _with_a_spare_boom(bent=True)
    runner = _bare(ship)
    boom, driver = ship.spars[BOOM], ship.sails[DRIVER]
    _carry_away_the_boom(ship)
    assert driver.wrecked and driver.state is SailState.FURLED and boom.rigged_out is True
    if unbent_first:
        orders.handle(ship, "unbend the driver")
        taken, notes = _phases(runner, ship)
        assert _ran(taken) == [("unbend", 180), ("lower", 90)]
        assert not any("Rigged in" in n[2] for n in notes)
        assert driver.state is SailState.UNBENT
    _clear_and_replace_the_boom(runner, ship)
    assert driver.state is SailState.UNBENT and boom.rigged_out is False
    orders.handle(ship, "bend the mizen")
    _run(runner, ship)
    assert ship.sails[COURSE].state is SailState.FURLED and boom.rigged_out is False
    orders.handle(ship, "shift the mizen for the driver")
    taken, _notes = _phases(runner, ship)
    assert _ran(taken) == list(_where_it_hangs(SHIFT_OUT_S).items())
    assert driver.state is SailState.FURLED and not driver.wrecked and boom.rigged_out is True


@pytest.mark.parametrize("wreck", ["rags", "yard"])
def test_the_boom_comes_in_when_the_wrecks_own_clearing_takes_the_driver_down(wreck):
    """Ext §17.11's rule, the boom out only while the driver is bent, on the two ways the driver
    goes below with its boom standing: its rags cut away, or the mizen yard carried away over it,
    each by the wreck's own order. The boom comes in with the sail, in that order's own time, so
    that the course can be bent with no boom beside it. (Measured without the line in
    `ClearWreckScript`: the boom stood out with the driver gone.)"""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    boom, driver = ship.spars[BOOM], ship.sails[DRIVER]
    part = DRIVER if wreck == "rags" else YARD
    if wreck == "rags":
        driver.state = SailState.BLOWN_OUT
    else:
        strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[YARD], 2.0)
        ship.drain_notes()
        assert driver.wrecked and not boom.wrecked
    runner.start(ship, "clear_wreck", part, {"part": part})
    _run(runner, ship)
    assert driver.state is SailState.UNBENT and not boom.wrecked and boom.rigged_out is False


@pytest.mark.parametrize(
    "text, phase, out",
    [
        ("shift the mizen for the driver", "rig_out_boom", False),
        ("shift the driver for the mizen", "rig_in_boom", True),
    ],
    ids=["going-out", "coming-in"],
)
def test_a_boom_carried_away_in_its_own_phase_is_passed_over(text, phase, out):
    """Ext §17.11: the boom carried away while the hands are at it stays as it lay, no line says
    it was rigged, and the work runs to its end, leaving what a shot a minute later would: the
    new sail bent, and any driver in the wreck, to be cut out by the wreck's own order."""
    ship = _with_a_spare_boom(bent=out)
    runner = _bare(ship)
    orders.handle(ship, text)
    script = runner.instances[0].script
    while script.phase != phase:
        runner.step(ship, 1.0, LIGHT_AIRS)
    for _ in range(10):
        runner.step(ship, 1.0, LIGHT_AIRS)
    ship.drain_notes()
    _carry_away_the_boom(ship)
    assert script.phase == phase
    _ticks, notes = _run(runner, ship)
    assert not any("Rigged" in n[2] for n in notes)
    assert ship.spars[BOOM].rigged_out is out
    assert [n[1] for n in notes][-1] == "sail.shifted"


def _belayed_at(ship: Ship, text: str, phase: str, before: str | None = None) -> Runner:
    """The work of `text` on a bare ship, belayed by the captain's word a few ticks into `phase`."""
    runner = _bare(ship)
    if before is not None:
        orders.handle(ship, before)
        _run(runner, ship)
    orders.handle(ship, text)
    script = runner.instances[0].script
    while script.phase != phase:
        runner.step(ship, 1.0, LIGHT_AIRS)
    for _ in range(5):
        runner.step(ship, 1.0, LIGHT_AIRS)
    ship.drain_notes()
    assert script.phase == phase
    assert orders.handle(ship, "belay that")[0] == "work.belayed"
    assert not runner.in_progress()
    return runner


@pytest.mark.parametrize(
    "bent, before, text, phase, out",
    [
        (False, None, "shift the mizen for the driver", "send_up", False),
        (False, None, "shift the mizen for the driver", "rig_out_boom", False),
        (False, None, "shift the mizen for the driver", "bend", False),
        (False, "unbend the mizen", "bend the driver", "send_up", False),
        (False, "unbend the mizen", "bend the driver", "rig_out_boom", False),
        (False, "unbend the mizen", "bend the driver", "bend", False),
        (True, None, "shift the driver for the mizen", "unbend", True),
        (True, None, "shift the driver for the mizen", "rig_in_boom", False),
        (True, None, "shift the driver for the mizen", "send_up", False),
        (True, None, "unbend the driver", "unbend", True),
        (True, None, "unbend the driver", "lower", True),
        (True, None, "unbend the driver", "rig_in_boom", False),
    ],
)
def test_belayed_the_boom_does_not_stand_out_over_no_driver(bent, before, text, phase, out):
    """Ext §17.11's rule, the boom out only while the driver is bent, through "belay that" (the
    runner's `belay`, `_belay_held_work` coming to anchor being the same). Belayed with the driver
    below, the hands bring the boom in, in the belay's own time. Old beside new: with no hook on
    `_SailWork`, a belay in `bend` or in `rig_in_boom` left it standing out, "rig in" refused naming
    the bending, the bending refused for the canvas drawn at `send_up`, and the course bent again
    beside it for the voyage. Bent, the driver keeps it: the belay is before the sail is below."""
    ship = frigate_with_driver(bent=bent)
    _belayed_at(ship, text, phase, before)
    boom, driver = ship.spars[BOOM], ship.sails[DRIVER]
    assert boom.rigged_out is out
    assert boom.rigged_out is (driver.state is not SailState.UNBENT)
    if not out:
        assert _refusal(ship, "rig in the driver boom").startswith("The driver boom goes out")


def test_belayed_the_course_bends_again_with_no_boom_beside_it():
    """The owner's complaint of §17.10 item 10, by the belay's road: the shift belayed in its last
    phase but one, the course can be bent again and the boom is in beside it, and stays in. The
    answer is the runner's words for the sail, unmoved. The driver's canvas drawn at `send_up` is
    not given back, on any sail: an older gap, for the lead."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    orders.handle(ship, "shift the mizen for the driver")
    script = runner.instances[0].script
    while script.phase != "bend":
        runner.step(ship, 1.0, LIGHT_AIRS)
    assert ship.spars[BOOM].rigged_out is True
    assert orders.handle(ship, "belay that")[1] == (
        "Belayed shifting the mizzen; the mizzen left unbent."
    )
    assert ship.spars[BOOM].rigged_out is False
    orders.handle(ship, "bend the mizen")
    _run(runner, ship)
    assert ship.sails[COURSE].state is SailState.FURLED and ship.spars[BOOM].rigged_out is False


def test_belayed_the_key_absent_stands_as_it_stood_and_a_boom_carried_away_is_passed_over():
    """The hook goes through `driver_boom`, so a file with no key moves nothing, a boom with no
    key standing out as it did; and a boom carried away is left as it lay, for its spare to land
    rigged in, as `_rig_boom` leaves it."""
    ship = ship_from_dict(_key_absent(), "tests/test_driver.py:toggle")
    _belayed_at(ship, "shift the mizen for the driver", "bend")
    assert ship.spars[BOOM].rigged_out is True
    ship = frigate_with_driver()
    runner = _bare(ship)
    orders.handle(ship, "shift the mizen for the driver")
    script = runner.instances[0].script
    while script.phase != "bend":
        runner.step(ship, 1.0, LIGHT_AIRS)
    _carry_away_the_boom(ship)
    orders.handle(ship, "belay that")
    assert ship.spars[BOOM].wrecked and ship.spars[BOOM].rigged_out is True


def test_rig_out_and_rig_in_on_the_drivers_boom_are_refused_naming_the_shift():
    """Ext §17.11: "rig out" and "rig in" on that boom, by any of its names, are refused in words
    naming the shift that does it, from whichever sail holds the place; with nothing bent there,
    the bending. Before the step, and on a boom that does not file the key, "You rig out studding
    sail booms; the mizzen boom is a boom.", which a gaff sail's boom keeps."""
    goes = "The driver boom goes out and comes in with the driver, not by itself; "
    ship = frigate_with_driver()
    runner = _bare(ship)
    for verb in ("rig out", "rig in"):
        for name in ("driver boom", "spanker boom", "mizzen boom"):
            assert _refusal(ship, f"{verb} the {name}") == goes + "shift the mizzen for the driver."
    assert not runner.in_progress() and ship.spars[BOOM].rigged_out is False
    ship.sails[COURSE].state = SailState.UNBENT
    assert _refusal(ship, "rig out the driver boom") == goes + "bend the driver."
    ship.sails[STORM].state = SailState.FURLED
    assert (
        _refusal(ship, "rig in the driver boom") == goes + "shift the storm mizzen for the driver."
    )
    ship = frigate_with_driver(bent=True)
    _bare(ship)
    for verb in ("rig out", "rig in"):
        assert (
            _refusal(ship, f"{verb} the driver boom") == goes + "shift the driver for the mizzen."
        )
    assert ship.spars[BOOM].rigged_out is True
    wrong_kind = "You rig out studding sail booms; the mizzen boom is a boom."
    ship = ship_from_dict(_key_absent(), "tests/test_driver.py:toggle")
    _bare(ship)
    assert _refusal(ship, "rig out the driver boom") == wrong_kind
    ship = load_ship(str(FRIGATE))
    _bare(ship)
    assert _refusal(ship, "rig out the spanker boom") == wrong_kind


@pytest.mark.parametrize("bent", [True, False], ids=["out", "in"])
def test_the_boom_is_left_by_studding_work_and_the_studding_sail_booms_are_not(bent):
    """Ext §17.11: its class stays `boom`, so `studding_work` and `StuddingSailsIn`, the first
    work of a tack or a wear, never touch it, out or in; a studding sail boom out beside it is
    still taken in."""
    ship = frigate_with_driver(bent)
    boom = ship.spars[BOOM]
    assert boom.cls == "boom" and boom.cls not in parts.RIGGED_IN_CLASSES
    assert scripts.studding_work(ship) == ([], [])
    assert not scripts.StuddingSailsIn(ship).needed
    other = next(s for s in ship.spars.values() if s.cls == "studdingsail_boom")
    other.rigged_out = True
    assert scripts.studding_work(ship) == ([], [other])
    work = scripts.StuddingSailsIn(ship)
    assert work.advance(scripts.BOOMS_IN_S, 1.0) and other.rigged_out is False
    assert boom.rigged_out is bent


def test_nothing_in_the_physics_or_the_gunnery_reads_the_boom_rigged_in():
    """Ext §17.11, plainly: the stowed boom keeps its windage at its file's place and can be hit
    by a shot, as every studding sail boom rigged in can. A small untruth, accepted, since mending
    it would need a read in `physics/`: a read of it is a change of the design."""
    for folder in ("physics", "combat"):
        reads = [
            p.name
            for p in (ROOT / "freesail" / folder).rglob("*.py")
            if "rigged_out" in p.read_text(encoding="utf-8")
        ]
        assert reads == [], folder


def test_the_boom_and_its_key_come_through_a_pickle():
    """The pickles as they are: no new field (Ext §17.11). `driver_boom` reads the key off the
    file's spec, which a plain pickle of the ship keeps with it, and the boom's state with the
    spar. The checkpoint's own route is the next two cases."""
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    orders.handle(ship, "unbend the driver")
    _run(runner, ship)
    ship.extra.pop("evolutions", None)
    again = pickle.loads(pickle.dumps(ship))
    assert again.spars[BOOM].rigged_out is False
    assert scripts.driver_boom(again, again.sails[DRIVER]) is again.spars[BOOM]


def _at_the_checkpoint(world, tmp_path):
    """The world written and read back by the checkpoint's own route, `_Pickler` and `_Unpickler`
    (Ext §12 lens 7), its hooks rebound."""
    path = replay.write_checkpoint(world, tmp_path / "driver.ckpt")
    return replay.read_checkpoint(path)[1]


def _lines_since(world, start: int) -> list:
    return [(e.tick, e.kind, e.text) for e in _after(world, start)]


def _the_shift_in_hand(world) -> scripts.ShiftScript:
    runner = world.ship.extra["evolutions"]
    return next(i.script for i in runner.instances if isinstance(i.script, scripts.ShiftScript))


def test_the_boom_and_its_key_come_through_a_checkpoint_at_rest_and_in_its_own_phase(tmp_path):
    """No new field (Ext §17.11), by the checkpoint's own route. At rest the boom's state and the
    key come back. Read in the middle of `rig_out_boom`, the shift carries on and ends as the
    world that was not written ends: the same lines at the same ticks, the same states."""
    world = _fair_wind_world(tmp_path)
    back = _at_the_checkpoint(world, tmp_path)
    assert back.ship.spars[BOOM].rigged_out is False
    assert scripts.driver_boom(back.ship, back.ship.sails[DRIVER]) is back.ship.spars[BOOM]
    start = world.clock.tick
    assert world.submit("shift the mizen for the driver").kind == "order.accepted"
    script = _the_shift_in_hand(world)
    while script.phase != "rig_out_boom":
        world.tick()
    for _ in range(20):
        world.tick()
    back = _at_the_checkpoint(world, tmp_path)
    assert _the_shift_in_hand(back).phase == "rig_out_boom"
    assert back.ship.spars[BOOM].rigged_out is False
    for w in (world, back):
        for _ in range(900):
            w.tick()
        assert w.ship.spars[BOOM].rigged_out is True and w.ship.sails[DRIVER].is_set
    assert _lines_since(back, start) == _lines_since(world, start)
    assert any("Rigged out the driver boom." in line[2] for line in _lines_since(back, start))


def test_a_checkpoint_from_before_the_key_keeps_the_old_words_and_phases(tmp_path):
    """Ext §12 lens 7, the checkpoint of a ship whose file had no key: the boom stands out, as it
    did, `driver_boom` is None, and the shift runs the old phases in the old words. Nothing asks a
    saved game to move until its file carries the key."""
    world = _fair_wind_world(tmp_path, _key_absent())
    back = _at_the_checkpoint(world, tmp_path)
    ship = back.ship
    boom, driver = ship.spars[BOOM], ship.sails[DRIVER]
    assert boom.rigged_out is True and scripts.driver_boom(ship, driver) is None
    answer = back.submit("rig out the driver boom")
    assert "You rig out studding sail booms; the mizzen boom is a boom." in answer.text
    start = back.clock.tick
    assert back.submit("shift the mizen for the driver").kind == "order.accepted"
    script = _the_shift_in_hand(back)
    taken = [script.phase]
    for _ in range(1500):
        back.tick()
        if script.phase != taken[-1]:
            taken.append(script.phase)
        if script.phase == "done":
            break
    assert taken == [*SHIFT_S, "done"]
    assert driver.is_set and boom.rigged_out is True
    assert not any("Rigged" in line[2] for line in _lines_since(back, start))


# -- The toggle, the lead's proof: the key absent against present on the fixture -------------


def _key_absent(bent: bool = False) -> dict:
    doc = frigate_with_driver_doc(bent)
    del next(s for s in doc["spars"] if s["id"] == BOOM)["rigged_out"]
    return doc


def _all_but_the_booms_state(ship: Ship) -> dict:
    """Every part's whole state as the ship holds it, the boom's `rigged_out` left out, and the
    sail room."""
    state = {pid: dict(vars(part)) for pid, part in ship.parts.items()}
    del state[BOOM]["rigged_out"]
    state["the sail room"] = [
        (s.kind, s.canvas_no, s.condition) for s in parts.sail_room(ship).sails
    ]
    return state


# What a player does with the driver, on a bare ship from the course set: every order the
# step touches and its neighbours, and the refusals of the place and of the reef.
TOGGLE_ORDERS = (
    "shift the mizen for the driver",
    "trim the driver",
    "reef the driver",
    "bend the mizen",
    "take in the driver",
    "set the driver",
    "take in the driver",
    "furl the driver",
    "shift the driver for the storm mizzen",
    "bend the driver",
    "shift the storm mizzen for the driver",
    "set plain sail",
    "shift the driver for the mizen",
    "take in the mizen",
    "unbend the mizen",
    "bend the driver",
    "unbend the driver",
    "bend the mizen",
    "shift the mizen for the storm mizzen",
    "shift the storm mizzen for the mizen",
)
# Where the key adds a phase, and which.
TOGGLE_PHASES = {
    0: "rig_out_boom",
    8: "rig_in_boom",
    10: "rig_out_boom",
    12: "rig_in_boom",
    15: "rig_out_boom",
    16: "rig_in_boom",
}


def _said(notes: list) -> list:
    """The log's notes, each with what it says and carries but for the work's `elapsed_s`."""
    return [(*note[:4], {k: v for k, v in note[4].items() if k != "elapsed_s"}) for note in notes]


def _worked_through(doc: dict) -> list[dict]:
    ship = ship_from_dict(doc, "tests/test_driver.py:toggle")
    runner = _bare(ship)
    ship.sails[COURSE].state = SailState.SET
    out = []
    for text in TOGGLE_ORDERS:
        try:
            answer = orders.handle(ship, text)
        except OrderError as e:
            answer = str(e)
        taken, notes = _phases(runner, ship)
        out.append(
            {
                "answer": answer,
                "taken": taken,
                "notes": notes,
                "state": _all_but_the_booms_state(ship),
                "boom out": ship.spars[BOOM].rigged_out,
            }
        )
    return out


def test_the_toggle_on_the_bare_ship_moves_the_booms_state_and_its_two_phases_and_nothing_else():
    """The lead's proof (Ext §17.11, the note of 2026-10-30), on the fixture, the key absent
    against present, through every order the step touches. Each answer is the same, each sail,
    spar and line the same at every order's end in every field, the sail room the same, and each
    log line but the boom's own; the phases are the same but the boom's, 120 s where the driver
    goes on or off. Absent the boom stands out all the voyage, as it did before the step; present
    it is out only while the driver is bent. The step's refusals are the key's too, and said where
    they are tested: "rig out" and "rig in" on the boom, and the shift onto a boom carried away."""
    present = _worked_through(frigate_with_driver_doc())
    absent = _worked_through(_key_absent())
    for i, (text, new, old) in enumerate(zip(TOGGLE_ORDERS, present, absent, strict=True)):
        assert new["answer"] == old["answer"], text
        assert new["state"] == old["state"], text
        added = {k: v for k, v in new["taken"].items() if k not in old["taken"]}
        assert added == ({TOGGLE_PHASES[i]: 120} if i in TOGGLE_PHASES else {}), text
        assert {k: v for k, v in new["taken"].items() if k not in added} == old["taken"], text
        rigged = [n for n in new["notes"] if n[2].startswith("Rigged ")]
        assert len(rigged) == len(added), text
        unrigged = [n for n in new["notes"] if n not in rigged]
        assert _said(unrigged) == _said(old["notes"]), text
        assert old["boom out"] is True, text
        driver_bent = new["state"][DRIVER]["state"] is not SailState.UNBENT
        assert new["boom out"] is driver_bent, text


def _lockstep(worlds: list, ticks: int, boom: bool) -> None:
    """Tick the two worlds, the key's and the key absent's; its boom as `boom` at every tick, and
    the other's out at every tick."""
    for _ in range(ticks):
        for world in worlds:
            world.tick()
        assert worlds[0].ship.spars[BOOM].rigged_out is boom
        assert worlds[1].ship.spars[BOOM].rigged_out is True


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_the_toggle_under_way_is_equal_to_the_last_figure_through_a_tack_a_wear_and_hove_to(
    tmp_path, bent
):
    """The toggle with the physics: the fixture whole at seed 7, the key present and absent, the
    driver bent and set (the boom out in both), or in the sail room under the course (the boom in
    against out). Through a tack, a wear and a heave-to, one after another, the boom never moves,
    and the two worlds' logs, every line at its tick, and her dynamics and every part's whole
    state at the end, are equal to the last figure: nothing reads the state. Measured: the
    driver tacked in 471 s, its wear given up at the wear's limit of 900 s ("she would not come
    round", with or without the key) and hove to in 299; the course 181, 900 (the same) and 320."""
    worlds = [
        _world(tmp_path / "with", bent, doc=frigate_with_driver_doc(bent)),
        _world(tmp_path / "without", bent, doc=_key_absent(bent)),
    ]
    for text, ticks in (("tack ship", 500), ("wear ship", 920), ("heave to", 340)):
        assert [w.submit(text).kind for w in worlds] == ["order.accepted", "order.accepted"], text
        _lockstep(worlds, ticks, bent)
    logs = [[(e.tick, e.kind, e.text) for e in w.log] for w in worlds]
    assert logs[0] == logs[1]
    assert any(e[1] == "ship.tacked" for e in logs[0])
    assert any(e[1] == "ship.hove_to" for e in logs[0])
    assert any("Up helm; brail up" in e[2] for e in logs[0])
    assert vars(worlds[0].ship.dyn) == vars(worlds[1].ship.dyn)
    assert _all_but_the_booms_state(worlds[0].ship) == _all_but_the_booms_state(worlds[1].ship)


# ---------------------------------------------------------------------------
# The driver's paths (Ext §3.5, §17.3)
# ---------------------------------------------------------------------------


def test_the_drivers_lists_take_the_driver_bent_and_never_while_it_is_in_the_sail_room():
    """Ext §17.4, the paths read: `drives_aft` takes the driver by `cut_at_mast`, and with it
    `after_gaff_sails` (hove to), `boom_sails` (in stays), `_after_sail` (box-hauling) and
    `after_gaff_sails_all` (the cast), which lists the sail of the place unbent too, as it lists
    the brig's storm trysail; `_set_fore_and_aft` sets none unbent. `shorten sail` takes the
    driver in at the third reef as it does the course (`orders.storm`), and leaves it at the
    second. In the sail room the driver is in none of the working lists, and the course is her
    driver."""
    ship = frigate_with_driver()
    course, driver = ship.sails[COURSE], ship.sails[DRIVER]
    course.state = SailState.SET
    for listed in (scripts.after_gaff_sails, scripts.boom_sails):
        assert listed(ship) == [course]
    assert scripts._after_sail(ship)[-1:] == [course]
    assert scripts.after_gaff_sails_all(ship) == [course, driver]
    course.state = SailState.FURLED
    ship.dyn.apparent_wind_angle = math.radians(-60.0)
    scripts._set_fore_and_aft(ship, scripts.after_gaff_sails_all(ship), "larboard")
    assert course.is_set and driver.state is SailState.UNBENT and driver.sheet_angle == 0.0

    ship = frigate_with_driver(bent=True)
    course, driver = ship.sails[COURSE], ship.sails[DRIVER]
    assert scripts.after_gaff_sails_all(ship) == [course, driver]
    assert scripts.driver_words(ship, []) == "the driver"
    ship.dyn.apparent_wind_angle = math.radians(-60.0)
    scripts._set_fore_and_aft(ship, scripts.after_gaff_sails_all(ship), "larboard")
    assert driver.is_set and course.state is SailState.UNBENT
    assert _deg(driver.sheet_angle) == pytest.approx(35.0, abs=0.01)
    assert yard_trim.read_sheet(ship, driver).side == 1  # the larboard tack's lee: starboard
    for listed in (scripts.after_gaff_sails, scripts.boom_sails):
        assert listed(ship) == [driver]
    assert scripts._after_sail(ship)[-1:] == [driver]
    assert scripts.driver_words(ship, scripts.after_gaff_sails(ship)) == "the driver"
    for sid in ship.groups["plain sail"]:
        if ship.sails[sid].state is not SailState.UNBENT:
            ship.sails[sid].state = SailState.SET
    topsails = [ship.sails[s] for s in ("fore.topsail", "main.topsail", "mizzen.topsail")]
    for sl in topsails:
        sl.reefs = 1
    assert not any("driver" in line for line in shorten_sail_lines(ship, 30.0))
    for sl in topsails:
        sl.reefs = 2
    assert shorten_sail_lines(ship, 40.0)[:3] == [
        "take in the main course",
        "reef the fore course, one reef",
        "take in the mizzen driver",
    ]


def _world(tmp_path, bent: bool, knots: float = 15.0, doc: dict | None = None):
    """The fixture whole in a fifteen-knot northerly on the starboard tack, sixty degrees off
    the wind, under plain sail and settled with the yards trimmed, as `tests/test_lateen.py`
    settles the course; `bent`, with the driver bent in the course's place and set by name
    (it is in "occasional sails" alone, never "plain sail": Ext §17.2). `doc`, the fixture as
    a test has changed it, written in `tmp_path`, which is made."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=300.0,
        ship_speed_kn=4.0,
    )
    Path(tmp_path).mkdir(parents=True, exist_ok=True)
    doc = doc if doc is not None else frigate_with_driver_doc(bent)
    world = make_world(7, write_ship(doc, tmp_path, "driver"), scenario)
    for text in ("set plain sail", "brace sharp up on the starboard tack"):
        world.submit(text)
    if bent:
        world.submit("set the driver")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    after_sail = world.ship.sails[DRIVER if bent else COURSE]
    assert after_sail.is_set
    return world


def _after(world, start: int) -> list:
    return [e for e in world.log if e.tick > start]


def _until(world, words: str, ticks: int) -> int:
    """Tick until a line with `words` is logged: its tick. The boom does not move meanwhile (Ext
    §17.11): out through every manoeuvre with the driver bent, in with it in the sail room."""
    start = world.clock.tick
    boom = world.ship.spars[BOOM]
    out = boom.rigged_out
    for _ in range(ticks):
        world.tick()
        assert boom.rigged_out is out
        hit = [e for e in _after(world, start) if words in e.text]
        if hit:
            return hit[0].tick
    raise AssertionError(f"no '{words}' in {ticks} ticks: {[e.text for e in _after(world, start)]}")


def _untouched(world) -> None:
    """The driver in the sail room as it started: unbent, its sheet never worked."""
    driver = world.ship.sails[DRIVER]
    assert driver.state is SailState.UNBENT and driver.sheet_angle == 0.0


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_in_stays_the_after_sail_is_hauled_aft_at_helms_a_lee(tmp_path, bent):
    """Steel 1794 vol. II p. 316, as the course (B3.1): at helm's a-lee the driver's sheet is
    flat aft at the gaff's floor and the words name it; its yard is not braced. In the sail
    room the driver is untouched, and the course is hauled aft. The boom stays out through the
    whole tack with the driver bent, in with it below (Ext §17.11), and no line rigs it in: the
    first work of a tack is the studding sail booms' alone."""
    world = _world(tmp_path, bent)
    after_sail = world.ship.sails[DRIVER if bent else COURSE]
    start = world.clock.tick
    world.submit("tack ship")
    _until(world, "Helm's a-lee", 400)
    line = next(e.text for e in _after(world, start) if "Helm's a-lee" in e.text)
    name = "driver" if bent else "mizzen"
    assert f"haul aft the {name} sheet and brace the bowline to leeward" in line, line
    assert after_sail.is_set and _deg(after_sail.sheet_angle) == pytest.approx(
        GAFF_FLOOR_DEG, abs=0.01
    )
    assert world.ship.spars[YARD].brace_angle == 0.0
    if not bent:
        _untouched(world)
    _until(world, "Tacked;", 600)
    assert world.ship.spars[BOOM].rigged_out is bent
    assert not any("boom" in e.text and "Rig" in e.text for e in _after(world, start))


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_hove_to_the_after_sail_is_brailed_up(tmp_path, bent):
    """Hove to with the main topsail to the mast the driver is brailed up (`after_gaff_sails`),
    as the course is; in the sail room it is untouched. The boom stays out with the driver
    brailed, and in with it below (Ext §17.11)."""
    world = _world(tmp_path, bent)
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(600):
        world.tick()
        assert world.ship.spars[BOOM].rigged_out is bent
    texts = [e.text for e in _after(world, start)]
    assert any(e.kind == "ship.hove_to" for e in _after(world, start)), texts
    name = "driver" if bent else "mizzen"
    assert any(f"brailed up the {name}" in t for t in texts), texts
    assert world.ship.sails[DRIVER if bent else COURSE].state is SailState.IN_THE_GEAR
    if not bent:
        _untouched(world)


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_wearing_the_after_sail_is_brailed_at_up_helm_and_hauled_out_by_the_wind(tmp_path, bent):
    """Steel 1794 vol. II pp. 321-322, as the course: brailed at "up helm", in the gear while
    she goes round, hauled out by the wind on the new tack. In the sail room the driver is
    untouched throughout. The boom stays out with the driver brailed, the whole way round, and
    in with it below (Ext §17.11)."""
    world = _world(tmp_path, bent)
    after_sail = world.ship.sails[DRIVER if bent else COURSE]
    name = "driver" if bent else "mizzen"
    start = world.clock.tick
    world.submit("wear ship")
    up_tick = _until(world, "Up helm", 200)
    assert after_sail.state is SailState.IN_THE_GEAR
    up = next(e.text for e in _after(world, start) if "Up helm" in e.text)
    assert f"brail up the {name}" in up, up
    going_round = []
    for _ in range(1500):
        world.tick()
        assert world.ship.spars[BOOM].rigged_out is bent
        if not bent:
            _untouched(world)
        if any(f"Haul out the {name}!" in e.text for e in _after(world, up_tick)):
            break
        going_round.append(after_sail.state)
    else:
        raise AssertionError(f"no 'Haul out the {name}!' in 1500 ticks")
    assert going_round and set(going_round) == {SailState.IN_THE_GEAR}
    assert after_sail.is_set and world.ship.dyn.tack == "larboard"


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_getting_under_way_the_after_sail_bent_is_set_after_the_cast(tmp_path, bent):
    """Getting under way from the road at seed 7 (`tests/test_lateen.py`'s, Falmouth's outer
    road): when she has cast, the driver, bent, is set and the words name it; in the sail room
    it is not set, and the cast sets the course (`after_gaff_sails_all` lists both;
    `_set_fore_and_aft` sets only a sail furled, loosed or brailed)."""
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
    world = make_world(7, write_ship(frigate_with_driver_doc(bent), tmp_path, "driver"), scenario)
    world.run(60)
    assert world.submit("let go the best bower").kind == "order.accepted"
    world.run(900)
    after_sail = world.ship.sails[DRIVER if bent else COURSE]
    assert after_sail.state is SailState.FURLED
    assert world.submit("get under way").kind == "order.accepted"
    cast = _until(world, "right the helm", 3600)
    line = next(e.text for e in world.log if e.tick == cast and "right the helm" in e.text)
    name = "driver" if bent else "mizzen"
    assert line.endswith(f"right the helm, brace round the head yards, set the {name}."), line
    assert after_sail.is_set
    if bent:
        assert world.ship.sails[COURSE].state is SailState.UNBENT
    else:
        _untouched(world)


# ---------------------------------------------------------------------------
# The sheet, the reef and the words (Ext §17.3, §17.4)
# ---------------------------------------------------------------------------


def test_the_drivers_sheet_keeps_the_gaffs_range_by_every_route_on_its_boom():
    """Ext §17.3 and §17.7: thirty degrees off the apparent wind the driver's sheet lies at the
    gaff's floor by every route that works it (set, `trim the driver`, `trim sails`, `draw the
    driver`, `draw_sheets`, the tack's haul aft, the tending lying to, the polar's trim), and
    is trimmed free to the gaff's 35 degrees at sixty off and to its ceiling at a hundred and
    thirty. Its geometry is the boomed one (`trim.sheet_geometry`): the boom's length and
    height, half its horse, the spanker sheet's two parts; the course's, beside it, is a loose
    foot's."""
    ship = frigate_with_driver(bent=True)
    driver = ship.sails[DRIVER]
    runner = _set_and_drawing(ship)
    out = {"set": _deg(driver.sheet_angle)}

    def ease() -> None:
        yard_trim.set_sheet_angle(ship, driver, math.radians(60.0))

    for text in ("trim the driver", "trim sails", "draw the driver"):
        ease()
        orders.handle(ship, text)
        _run(runner, ship)
        out[text] = _deg(driver.sheet_angle)
    ease()
    scripts.draw_sheets(ship, [driver])
    out["draw_sheets"] = _deg(driver.sheet_angle)
    ease()
    scripts.sheets_to(ship, scripts.boom_sails(ship), None, None)
    out["hauled aft"] = _deg(driver.sheet_angle)
    ease()
    scripts._work_lying_to_sheets(ship, {"sign": 1.0}, 1.0, False)
    out["lying to"] = _deg(driver.sheet_angle)
    ease()
    _trim_for(ship, CLOSE)
    out["polar"] = _deg(driver.sheet_angle)
    assert out == dict.fromkeys(out, GAFF_FLOOR_DEG), out
    for awa, want in ((math.radians(-60.0), 35.0), (math.radians(-130.0), CEILING_DEG)):
        scripts.draw_sheets(ship, [driver], None, awa)
        assert _deg(driver.sheet_angle) == pytest.approx(want, abs=0.01)
    geo = yard_trim.sheet_geometry(ship, driver)
    boom = ship.spars[BOOM]
    assert (_deg(geo.floor), _deg(geo.ceiling)) == (GAFF_FLOOR_DEG, CEILING_DEG)
    assert geo.boomed and geo.parts == 2
    assert (geo.arm_m, geo.offset_m, geo.height_m) == (
        boom.length_m,
        0.5 * boom.horse_m,
        boom.height_m,
    )
    assert not yard_trim.sheet_geometry(ship, ship.sails[COURSE]).boomed


def test_reefing_the_driver_is_refused():
    """Ext §17.2-§17.3: Steel names no reef band in the driver; `_sail_check` refuses "reef" on
    a sail with none."""
    ship = frigate_with_driver(bent=True)
    _set_and_drawing(ship)
    assert _refusal(ship, "reef the driver") == (
        "The mizzen driver has no reef bands; it is set whole or not at all."
    )


def test_the_words_of_the_driver_in_the_sail_room_and_of_plain_sail_with_it_bent():
    """Ext §17.3's table, as it has them. "Set the driver" in the sail room is refused as the
    frigate's storm mizzen is (`_sail_check`; untrue while the course is on the yard, and left:
    §17.10 item 4). With the driver bent, "set plain sail" and "make all sail" set every sail of
    their groups but the after sail: the course is reported unbent, and the driver, in
    "occasional sails" alone, is not set; it is set by name."""
    ship = frigate_with_driver()
    _bare(ship)
    assert _refusal(ship, "set the driver") == (
        "The mizzen driver is unbent; there is no sail on the yard. Bend one first."
    )
    ship = frigate_with_driver(bent=True)
    runner = _bare(ship)
    unbent = "the mizzen course is unbent; there is no sail on the yard. Bend one first"
    for text in ("set plain sail", "make all sail"):
        _kind, words, _data = orders.handle(ship, text)
        assert unbent in words, words
        _run(runner, ship)
        assert ship.sails[DRIVER].state is SailState.FURLED, text
    assert all(ship.sails[s].is_set for s in ship.groups["plain sail"] if s != COURSE), "plain sail"


def test_the_yards_sail_is_the_course_while_the_driver_is_bent():
    """Ext §17.4 and risk 6 (§17.9): `sail_of(mizzen.yard)` is the first sail filed on the yard,
    the course, whichever is bent, as the lugger's main lug is beside her taille-vent. The words
    that read it, recorded with the driver bent and set: the yard's hint names the course; "send
    down the mizzen yard" is refused for a sound yard, naming no sail; "take in the mizen" is
    answered that the course is unbent (true of the course; §17.10 item 4)."""
    ship = frigate_with_driver(bent=True)
    _set_and_drawing(ship)
    assert ship.sail_of(ship.spars[YARD]) is ship.sails[COURSE]
    assert _refusal(ship, "set the mizzen yard") == (
        "You set sails; the mizzen yard is a lateen yard. Did you mean the mizzen course?"
    )
    assert _refusal(ship, "send down the mizzen yard") == (
        "The mizzen yard stands sound; only a spar carried away is sent down by itself."
    )
    assert _refusal(ship, "take in the mizen") == (
        "The mizzen course is unbent; there is no sail on the yard. Bend one first."
    )


# ---------------------------------------------------------------------------
# The physics (Ext §17.5): the frigate's polar row, and row 3' as a test
# ---------------------------------------------------------------------------

# The angles off the wind of Ext §3.2's and §17.5's rows, in fifteen knots.
ANGLES_DEG = (50, 60, 90, 120, 150)
WIND_KN = 15.0
# Ext §3.2's first row, the frigate's spanker as filed: her balanced speed, knots.
SPANKER_ROW_KN = (2.21, 4.29, 8.19, 7.86, 6.53)


def _row(ship: Ship) -> list[tuple[float, float]]:
    """Ext §17.5's method: at each angle the polar's balanced speed in fifteen knots
    (`_balanced_speed_ms`), and the sails' yaw moment there, the yards and sheets trimmed as
    the polar trims them: (knots, kN m), + turning her head toward a wind on her starboard bow
    (weather helm)."""
    out = []
    tw = units.knots_to_ms(WIND_KN)
    for a in ANGLES_DEG:
        u = _balanced_speed_ms(ship, a, WIND_KN)
        ship.dyn.u = ship.dyn.speed = u
        ship.dyn.v = 0.0
        theta = math.radians(a)
        awa = math.atan2(math.sin(theta) * tw, math.cos(theta) * tw + u)
        ship.dyn.apparent_wind_angle = awa
        _trim_for(ship, awa)
        wind = Wind(WindParams.from_nautical(a, WIND_KN, 0.0, 0.0), random.Random(0))
        forces = compute_sail_forces(ship, wind)
        out.append((units.ms_to_knots(u), forces.yaw_moment_nm / 1000.0))
    return out


def _spanker_refiled() -> Ship:
    """`frigate-36.yaml` with her spanker re-filed as the driver's model (Ext §17.5 row 3'): a
    lateen cut at the mast on a lateen yard of the gaff's length, height and rating in the
    gaff's place, its foot on her boom, the gaff's lines on the yard (its throat halyard the
    jeers, its peak halyard a lift), the outhaul a tack. Its area, centre, reefs and canvas are
    the spanker's, its id too, so every group, alias and the storm mizzen's place stand. Its
    corners (tack at the jaws, throat at the gaff's height on the mast's raked line) are for the
    schema alone: no physics reads a lateen's corners. No class table is patched: B3.1's
    lookups read `curve_class`."""
    doc = yaml.safe_load(FRIGATE.read_text(encoding="utf-8"))
    spars = {s["id"]: s for s in doc["spars"]}
    gaff, mast, boom = spars["mizzen.gaff"], spars["mizzen.mast"], spars[BOOM]
    doc["spars"][doc["spars"].index(gaff)] = {
        "id": YARD,
        "class": "lateen_yard",
        "on": "mizzen.mast",
        "length_m": gaff["length_m"],
        "height_m": gaff["height_m"],
        "rating_kn": gaff["rating_kn"],
    }
    spanker = next(s for s in doc["sails"] if s["id"] == "mizzen.spanker")
    del spanker["gaff"]
    rake = math.tan(math.radians(mast["rake_deg"]))
    jaws, throat = boom["height_m"], gaff["height_m"]
    tack_x, throat_x = mast["x_m"] - rake * jaws, mast["x_m"] - rake * throat
    spanker.update(
        {
            "class": "lateen",
            "yard": YARD,
            "cut_at_mast": True,
            "corners_m": [
                [round(tack_x, 2), jaws],
                [round(throat_x, 2), throat],
                [round(throat_x - 0.8 * gaff["length_m"], 2), throat + 0.6 * gaff["length_m"]],
                [round(tack_x - 0.9 * boom["length_m"], 2), jaws],
            ],
        }
    )
    renamed = {"throat_halyard": "halyard", "peak_halyard": "lift"}
    for line in doc["lines"]:
        if line["of"] == "mizzen.gaff":
            line["of"] = YARD
            line["class"] = renamed.get(line["class"], line["class"])
        elif line["id"] == "mizzen.spanker.outhaul":
            line["class"] = "tack"
    doc["aliases"]["spanker gaff"] = YARD
    ship = ship_from_dict(doc, "frigate-36.yaml")
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship


def test_the_frigates_polar_row_is_the_spankers_row_of_ext_3_2():
    """Ext §17.7: on the final tree `frigate-36.yaml`'s polar (`polar_of`) in fifteen knots at
    50, 60, 90, 120 and 150 degrees is §3.2's first row, 2.21, 4.29, 8.19, 7.86 and 6.53 kn."""
    row = polar_of(str(FRIGATE)).speeds_kn[POLAR_WINDS_KN.index(WIND_KN)]
    assert tuple(row[POLAR_ANGLES_DEG.index(a)] for a in ANGLES_DEG) == SPANKER_ROW_KN


def test_the_driver_filed_as_the_spanker_is_the_spanker_to_the_physics():
    """Ext §17.5 row 3', as a test: the frigate's spanker re-filed as a lateen cut at the mast
    on a lateen yard in the gaff's place and on her boom, unpatched, sails as the spanker: her
    balanced speed and her sails' yaw moment at the five angles equal row 1, the spanker as
    filed, within 0.01 kn and 1 kN m. Measured, the two rows are the same to the last figure:
    2.209, 4.293, 8.192, 7.862, 6.531 kn; -45.35, -14.91, 101.97, 88.60, -31.34 kN m."""
    refiled = _spanker_refiled()
    sail = refiled.sails["mizzen.spanker"]
    assert sail.cls == "lateen" and sail.cut_at_mast and sail.curve_class == "gaff"
    assert refiled.spar_of_role(sail, "boom") is refiled.spars[BOOM]
    filed = _row(_rigged_for_plain_sail(str(FRIGATE)))
    model = _row(refiled)
    assert [round(kn, 2) for kn, _yaw in filed] == list(SPANKER_ROW_KN)
    for (kn1, yaw1), (kn3, yaw3), a in zip(filed, model, ANGLES_DEG, strict=True):
        assert abs(kn3 - kn1) <= 0.01, (a, kn1, kn3)
        assert abs(yaw3 - yaw1) <= 1.0, (a, yaw1, yaw3)


# ---------------------------------------------------------------------------
# Truth 7-230 (the lead's allotment, 2026-10-29)
# ---------------------------------------------------------------------------


def _fair_wind_world(tmp_path, doc: dict | None = None):
    """The fixture with the driver in the sail room, in a ten-knot northerly with the wind on
    her starboard quarter, 120 degrees off (Steel's "light fair winds", l. 13819-13821), under
    plain sail, the yards trimmed, settled twenty minutes at seed 7. `doc`, the fixture as a test
    has changed it."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=240.0,
        ship_speed_kn=4.0,
    )
    doc = doc if doc is not None else frigate_with_driver_doc()
    world = make_world(7, write_ship(doc, tmp_path, "driver"), scenario)
    world.submit("set plain sail")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    return world


def _shifted_under_way(world, phases: dict[str, int]) -> tuple[dict[str, int], int]:
    """ "Shift the mizen for the driver" on the settled world, the phases `phases` seen ending in
    their order by what each changes: each phase's ticks, and the tick the whole began."""
    ship = world.ship
    course, driver, boom = ship.sails[COURSE], ship.sails[DRIVER], ship.spars[BOOM]
    start = world.clock.tick
    assert world.submit("shift the mizen for the driver").kind == "order.accepted"
    ends: dict[str, int] = {}
    for _ in range(1500):
        world.tick()
        seen = {
            "take_in": course.state is SailState.IN_THE_GEAR,
            "unbend": course.state is SailState.UNBENT,
            "send_up": DRIVER not in [kind for kind, _no in _in_the_room(ship)],
            "rig_out_boom": boom.rigged_out,
            "bend": driver.state is not SailState.UNBENT,
            "set": driver.is_set,
        }
        for phase in phases:
            if seen[phase] and phase not in ends:
                ends[phase] = world.clock.tick
        if driver.is_set:
            break
    began = next(
        e.tick for e in _after(world, start) if e.kind == "evolution.started" and "shift" in e.text
    )
    assert list(ends) == list(phases), ends
    marks = [began, *(ends[phase] for phase in phases)]
    return {phase: marks[i + 1] - marks[i] for i, phase in enumerate(phases)}, began


def test_the_toggle_on_the_shift_under_way_moves_its_time_by_the_booms_phase(tmp_path):
    """The toggle at her company: the fixture under plain sail in ten knots 120 degrees off at seed
    7. The boom's phase, between its file's time and a quarter more, is what the key adds: each
    other phase takes what it took without the key within a tick or two. Measured, old beside
    new: 102, 206, 171, 274 and 137 s, 890 s the whole, without; the same five with 137 s for the
    boom between the third and the fourth, 1,027 s the whole, with."""
    (tmp_path / "with").mkdir()
    (tmp_path / "without").mkdir()
    with_key = _fair_wind_world(tmp_path / "with")
    without = _fair_wind_world(tmp_path / "without", _key_absent())
    took, began = _shifted_under_way(with_key, SHIFT_OUT_S)
    took_old, began_old = _shifted_under_way(without, SHIFT_S)
    assert began == began_old
    assert 120 <= took["rig_out_boom"] <= 150
    for phase, seconds in took_old.items():
        assert abs(took[phase] - seconds) <= 2, (phase, took, took_old)
    assert abs(sum(took.values()) - sum(took_old.values()) - took["rig_out_boom"]) <= 4
    assert with_key.ship.spars[BOOM].rigged_out is True
    assert without.ship.spars[BOOM].rigged_out is True


def test_truth_7_230_the_driver_is_the_spanker_to_the_physics_and_shifts_in_about_15_minutes(
    tmp_path,
):
    """Truth 7-230 (Build-Ships.md §15; Ext §17.7, §17.11; the lead's allotment of 2026-10-29): *the
    driver, filed as the frigate's spanker, is the spanker to the physics, and the shift of the
    mizen for the driver takes about fifteen minutes*: about thirteen until its boom went with it
    (Ext §17.11, the lead's approval of 2026-10-30). Steel's driver boomsail is bent "instead
    of the mizen, ... exactly the same, only the foot of the sail is extended on the boom"
    (Steel 1794 vol. I, OCR l. 24536-24538), in light fair winds (l. 13819-13821); *Venus* split
    her spanker, unbent it and bent the mizen (Jackson, *Logs* vol. 1, OCR l. 11064-11076).

    1. **Row 3'** (Ext §17.5): the spanker re-filed in memory as a lateen cut at the mast, on a
       lateen yard in the gaff's place and on her boom, has her balanced speed and her sails'
       yaw moment at 50, 60, 90, 120 and 150 degrees in fifteen knots equal to the spanker's as
       filed within 0.01 kn and 1 kN m (measured equal to the last figure: 2.21, 4.29, 8.19,
       7.86, 6.53 kn; -45, -15, 102, 89, -31 kN m).
    2. **The shift at her company**: the fixture (`frigate_with_driver()`, the frigate's company
       with the 64's driver and course) under plain sail in ten knots 120 degrees off, at seed
       7. "Shift the mizen for the driver": the course, drawing, is taken in, unbent, sent down
       while the driver is swayed up, the boom rigged out, the driver bent and set, in that
       order; each phase between its file's time and a quarter more (measured 102, 206, 171,
       137, 274 and 137 s against 90, 180, 150, 120, 240 and 120: her hands and the weather's
       factor, 1.13-1.14); the whole between fifteen and nineteen minutes (measured 1,027 s,
       seventeen minutes and seven seconds; 900 s at the file's times). **Old beside new** (Ext
       §17.11, the boom's phase of 120 s by the hands' factor, and nothing else): five phases to
       six; the band of the whole, thirteen to sixteen minutes to fifteen to nineteen; measured
       890 s to 1,027 s; 780 s to 900 s at the file's times. The course's canvas goes down to
       the sail room and the count of spares stands. "Trim sails" trims the driver free to the
       wind (measured 59.6 degrees, 83 degrees of apparent wind; 60.8 and 84 before the boom's
       phase, her way a little changed by the 137 s) and it draws ahead as her after sail. (The
       shift sets it where its own sheet lies, flat aft at the gaff's floor, as it sets the
       frigate's storm mizzen at its own: `ShiftScript`, "its sheet and yard stand as the old
       sail's did". Measured, not pinned.)

    **The clauses on the 64 herself** (Ext §17.7; Build-Ships.md §2.6) are B1's, in
    `tests/test_indefatigable.py`, on `sixty-four.yaml` since her stage B: her shift at her own
    company; her polar with the driver bent and set above the course's from 90 to 150 degrees in
    ten knots (on this fixture, the 64's driver and course on the frigate's hull, it holds: 5.75,
    5.57 and 4.47 kn against 5.60, 5.38 and 4.39, the driver bringing 59, 38 and 10 kN m more
    weather helm; measured, not pinned here); and the driver hauled aft at helm's a-lee and
    brailed up hove to on her file. Her band moves with her regeneration, when her file carries
    the key. Seed 7, the owner's machine."""
    filed = _row(_rigged_for_plain_sail(str(FRIGATE)))
    model = _row(_spanker_refiled())
    for (kn1, yaw1), (kn3, yaw3) in zip(filed, model, strict=True):
        assert abs(kn3 - kn1) <= 0.01 and abs(yaw3 - yaw1) <= 1.0

    world = _fair_wind_world(tmp_path)
    ship = world.ship
    course, driver = ship.sails[COURSE], ship.sails[DRIVER]
    assert course.is_set and driver.state is SailState.UNBENT
    spares = scripts.spare_sails(ship)
    start = world.clock.tick
    took, began = _shifted_under_way(world, SHIFT_OUT_S)
    for phase, seconds in SHIFT_OUT_S.items():
        assert seconds <= took[phase] <= 1.25 * seconds, took
    whole = sum(took.values())
    assert 15 * 60 <= whole <= 19 * 60, whole
    shifted = [e for e in _after(world, start) if e.kind == "sail.shifted"]
    assert len(shifted) == 1 and shifted[0].tick == began + whole
    assert course.state is SailState.UNBENT and ship.spars[BOOM].rigged_out is True
    assert _in_the_room(ship) == [(COURSE, COURSE_CANVAS_NO)]
    assert scripts.spare_sails(ship) == spares
    assert world.submit("trim sails").kind == "sail.trimmed"
    for _ in range(200):
        world.tick()
    assert scripts.after_gaff_sails(ship) == [driver]
    assert driver.is_set and driver.thrust_kn > 0.0
    want = yard_trim.wanted_sheet_angle(driver.curve_class, ship.dyn.apparent_wind_angle)
    assert _deg(driver.sheet_angle) == pytest.approx(_deg(want), abs=5.0)
    assert GAFF_FLOOR_DEG < _deg(driver.sheet_angle) < CEILING_DEG
