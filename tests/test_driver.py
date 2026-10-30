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
moves; no sail is in its own place, so none is shifted for itself. The tests run
on the fixture `frigate_with_driver()` alone (`tests/rig_fixtures.py`), the 0E frigate with the
64's driver on her boom: the 64's file carries none until B1's `DRIVER` flip at her stage B.
"""

from __future__ import annotations

import math
import random
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from rig_fixtures import DRIVER_CANVAS_NO, frigate_with_driver, frigate_with_driver_doc, write_ship

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.storm import _in_its_place, shorten_sail_lines
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
# and set; a furled one shifted where it hangs.
SHIFT_S = {"take_in": 90, "unbend": 180, "send_up": 150, "bend": 240, "set": 120}

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
    """Ext §17.3 and §17.7: "shift the mizen for the driver" runs `shift_sail` on the course,
    the storm mizzen's way. A drawing course is taken in, unbent, sent down while the driver is
    swayed up, the driver bent and set: 780 s at the file's times, the hands' factor 1 with no
    company aboard. A furled course is shifted where it hangs, in 570 s, and the driver left
    furled. While the driver is bent the sail room holds the course's canvas, No. 2, in the
    driver's spare's stead, so the count of spares stands; shifted back, the same, the
    driver's No. 5 below again."""
    ship = frigate_with_driver()
    runner = _bare(ship)
    course, driver = ship.sails[COURSE], ship.sails[DRIVER]
    spares = scripts.spare_sails(ship)
    assert driver.state is SailState.UNBENT and course.state is SailState.FURLED
    assert _in_the_room(ship) == [(DRIVER, DRIVER_CANVAS_NO)]
    if drawing:
        course.state = SailState.SET
    left = "set" if drawing else "furled"
    phases = list(SHIFT_S) if drawing else ["unbend", "send_up", "bend"]
    for text, (old, old_name, old_no), (new, new_name, new_no) in (
        (
            "shift the mizen for the driver",
            (course, "mizzen", COURSE_CANVAS_NO),
            (driver, "driver", DRIVER_CANVAS_NO),
        ),
        (
            "shift the driver for the mizen",
            (driver, "driver", DRIVER_CANVAS_NO),
            (course, "mizzen", COURSE_CANVAS_NO),
        ),
    ):
        _kind, _words, data = orders.handle(ship, text)
        assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [
            ("shift_sail", old.id)
        ]
        ticks, notes = _run(runner, ship)
        assert ticks == sum(SHIFT_S[p] for p in phases), text
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
    lateen cut at the mast naming a boom): the 64's driver and her storm mizzen from B1's
    `DRIVER` flip. No file has one yet; the fixture written out as a file has, and holds.
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


def _world(tmp_path, bent: bool, knots: float = 15.0):
    """The fixture whole in a fifteen-knot northerly on the starboard tack, sixty degrees off
    the wind, under plain sail and settled with the yards trimmed, as `tests/test_lateen.py`
    settles the course; `bent`, with the driver bent in the course's place and set by name
    (it is in "occasional sails" alone, never "plain sail": Ext §17.2)."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=300.0,
        ship_speed_kn=4.0,
    )
    world = make_world(7, write_ship(frigate_with_driver_doc(bent), tmp_path, "driver"), scenario)
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
    """Tick until a line with `words` is logged: its tick."""
    start = world.clock.tick
    for _ in range(ticks):
        world.tick()
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
    room the driver is untouched, and the course is hauled aft."""
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


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_hove_to_the_after_sail_is_brailed_up(tmp_path, bent):
    """Hove to with the main topsail to the mast the driver is brailed up (`after_gaff_sails`),
    as the course is; in the sail room it is untouched."""
    world = _world(tmp_path, bent)
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(600):
        world.tick()
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
    untouched throughout."""
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


def _fair_wind_world(tmp_path):
    """The fixture with the driver in the sail room, in a ten-knot northerly with the wind on
    her starboard quarter, 120 degrees off (Steel's "light fair winds", l. 13819-13821), under
    plain sail, the yards trimmed, settled twenty minutes at seed 7."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=240.0,
        ship_speed_kn=4.0,
    )
    world = make_world(7, write_ship(frigate_with_driver_doc(), tmp_path, "driver"), scenario)
    world.submit("set plain sail")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    return world


def test_truth_7_230_the_driver_is_the_spanker_to_the_physics_and_shifts_in_about_13_minutes(
    tmp_path,
):
    """Truth 7-230 (Build-Ships.md §15; Ext §17.7; the lead's allotment of 2026-10-29): *the
    driver, filed as the frigate's spanker, is the spanker to the physics, and the shift of the
    mizen for the driver takes about thirteen minutes.* Steel's driver boomsail is bent "instead
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
       while the driver is swayed up, the driver bent and set, in that order; each phase
       between its file's time and a quarter more (measured 102, 206, 171, 274 and 137 s against
       90, 180, 150, 240 and 120: her hands and the weather's factor, 1.13-1.14); the whole
       between thirteen and sixteen minutes (measured 890 s, fourteen minutes and fifty
       seconds; 780 s at the file's times). The course's canvas goes down to the sail room and
       the count of spares stands. "Trim sails" trims the driver free to the wind (measured
       60.8 degrees, 84 degrees of apparent wind) and it draws ahead as her after sail. (The
       shift sets it where its own sheet lies, flat aft at the gaff's floor, as it sets the
       frigate's storm mizzen at its own: `ShiftScript`, "its sheet and yard stand as the old
       sail's did". Measured, not pinned.)

    **Left for B1** (Ext §17.7; Build-Ships.md §2.6): the clauses on the 64 herself, measured at
    her stage B with `DRIVER = True` on `sixty-four.yaml`: her shift at her own company; her
    polar with the driver bent and set above the course's from 90 to 150 degrees in ten knots,
    pinned only if it holds (on this fixture, the 64's driver and course on the frigate's hull,
    it holds: 5.75, 5.57 and 4.47 kn against 5.60, 5.38 and 4.39, the driver bringing 59, 38 and
    10 kN m more weather helm; measured, not pinned here); and the driver hauled aft at helm's
    a-lee and brailed up hove to on her file (on the fixture: the manoeuvre tests above). Seed 7,
    the owner's machine."""
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
    assert world.submit("shift the mizen for the driver").kind == "order.accepted"
    ends: dict[str, int] = {}
    for _ in range(1500):
        world.tick()
        now = world.clock.tick
        seen = (
            ("take_in", course.state is SailState.IN_THE_GEAR),
            ("unbend", course.state is SailState.UNBENT),
            ("send_up", DRIVER not in [kind for kind, _no in _in_the_room(ship)]),
            ("bend", driver.state is not SailState.UNBENT),
            ("set", driver.is_set),
        )
        for phase, done in seen:
            if done and phase not in ends:
                ends[phase] = now
        if driver.is_set:
            break
    began = next(
        e.tick for e in _after(world, start) if e.kind == "evolution.started" and "shift" in e.text
    )
    assert list(ends) == list(SHIFT_S), ends
    marks = [began, *(ends[phase] for phase in SHIFT_S)]
    took = {phase: marks[i + 1] - marks[i] for i, phase in enumerate(SHIFT_S)}
    for phase, seconds in SHIFT_S.items():
        assert seconds <= took[phase] <= 1.25 * seconds, took
    whole = ends["set"] - began
    assert 13 * 60 <= whole <= 16 * 60, whole
    shifted = [e for e in _after(world, start) if e.kind == "sail.shifted"]
    assert len(shifted) == 1 and shifted[0].tick == ends["set"]
    assert course.state is SailState.UNBENT
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
