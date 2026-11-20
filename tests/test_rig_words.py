"""Package 90, A2: the words of a rig with no yards, mended at their cause.

The going-about evolutions and their kin said "brace in the after yards", "braced up", "braced
sharp up", "Hands to the after braces" and "square the yards" whatever the rig, so that a lugger,
whose lug yards are no braced yards (`Spar.is_yard`), was told to brace in her after yards and
was braced up, and the cutter, the smack and the two schooners, whose yards are head yards alone,
braced up after yards they have not. A line that names a braced yard or its braces is now said
only where she has one, read from the yards the evolution swings (`scripts.head_and_after_yards`,
`scripts.has_braced_yards`, `scripts.braces_manned`), for every rig. The words put in their place
are JUDGEMENT. Words only: every tick, every event's kind and every trace of heading, speed and
position the same, old beside new over all eighteen files (docs/dev/TuningNotes.md, "Package 90,
A2").

Each test enters by the door the behaviour is met at: a ship file loaded as the game loads it,
and an order given as a player gives it, from the lugger transcripts' settle
(`tests/test_settee.py`: seed 7, 15 knots from the north, her head 292.5 degrees, plain sail braced
sharp up and trimmed, 2,400 s), or the anchor's own road (`tests/test_anchor.py`: Carrick Road;
and off Falmouth in three fathoms and a half, where a boat lies to her grapnel).
Two lines no order of a player's reaches on a rig with no braced yard (measured: a lugger is by
the wind for every course she is put about for, and tacks or gybes by the helm; she did not miss
stays at the settle in four knots, and in three she has not way enough to stay) are taken by the
runner's door, as `tests/test_evolutions.py` takes them on the frigate.
"""

from __future__ import annotations

import io
import math
import random
import re
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import Runner, scripts
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship

LUGGER = "data/ships/lugger.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"

# The eighteen files committed at A2, each with the braces her going about mans, as filed: the
# five boats and the lugger have no braced yard; the cutter, the smack and the two schooners have
# head yards alone; the rest have after yards too (the hermaphrodite brig's main topsail and
# topgallant yards on her schooner's main among them). Named, not globbed, so that a file added
# later is no move of this guard.
BRACES_AS_FILED = {
    "bilander": "after braces",
    "boat-cutter-23": "sheets",
    "boat-cutter-28": "sheets",
    "boat-launch-25": "sheets",
    "boat-launch-31": "sheets",
    "boat-yawl-16": "sheets",
    "brig": "after braces",
    "cutter": "head braces",
    "frigate-36": "after braces",
    "hermaphrodite-brig": "after braces",
    "lugger": "sheets",
    "merchant-brig": "after braces",
    "privateer-schooner": "head braces",
    "razee-44": "after braces",
    "seventy-four": "after braces",
    "sixty-four": "after braces",
    "smack": "head braces",
    "topsail-schooner": "head braces",
}


@pytest.mark.parametrize(("name", "braces"), sorted(BRACES_AS_FILED.items()))
def test_every_file_is_read_for_the_braces_it_has(name, braces):
    """The key, read off every committed file as loaded: the yards the evolutions swing, and so
    the braces their words name, and whether she has a braced yard to be said braced at all."""
    ship = load_ship(f"data/ships/{name}.yaml")
    head, after = scripts.head_and_after_yards(ship)
    assert scripts.braces_manned(ship) == braces
    assert scripts.has_braced_yards(head, after) == (braces != "sheets")
    assert bool(after) == (braces == "after braces")


# ---------------------------------------------------------------------------
# By the player's door
# ---------------------------------------------------------------------------


def _settle(path: str) -> bytes:
    """The lugger transcripts' settle (`tests/test_settee.py`), as a checkpoint to sail from."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, path, scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    for i in range(2400):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    return replay.checkpoint_bytes(world)


def _from(settled: bytes):
    world = replay._Unpickler(io.BytesIO(settled)).load()
    replay._rebind(world)
    return world


def _lines(world, orders: list[tuple[str, int]]) -> list[tuple[int, str]]:
    """Each order given and sailed so many seconds: every line after the first order but the
    leeway's and the bells', with its tick after it."""
    start, n0 = world.clock.tick, len(world.log.all())
    for order, seconds in orders:
        world.submit(order)
        world.run(seconds)
    return [
        (e.tick - start, e.text)
        for e in world.log.all()[n0:]
        if e.kind not in ("ship.leeway", "clock.bell")
    ]


BRACES = re.compile(r"\bbrac|\byards?\b|\bsquare", re.IGNORECASE)


@pytest.fixture(scope="module")
def lugger() -> bytes:
    return _settle(LUGGER)


@pytest.fixture(scope="module")
def cutter() -> bytes:
    return _settle(CUTTER)


def test_the_lugger_hove_to_and_filled_away_mans_her_sheets_and_is_braced_by_no_line(lugger):
    """Old: "Hands to the after braces; heave to.", "Fill away; man the after braces.", "Braced
    the yards full." and "Filled away on the starboard tack; braced full and steering WNW
    (292°)."; every tick as it was."""
    got = _lines(_from(lugger), [("heave to", 600), ("fill away", 60)])
    assert got == [
        (0, "Order: heave to."),
        (1, "Lowered the foresail and the mainsail."),
        (1, "Hauled flat aft the mizen sheet; the jib sheet to windward; helm a-lee."),
        (1, "Hands to the sheets; heave to."),
        (
            86,
            "Hove to on the starboard tack, under her fore-and-aft canvas, jib sheet to windward, "
            "helm a-lee.",
        ),
        (600, "Order: fill away."),
        (601, "Hauled aft the head sheets; kept the helm a-lee to let her fall off."),
        (601, "Fill away; man the sheets."),
        (601, "Right the helm."),
        (602, "Filled away on the starboard tack; steering WNW (292°)."),
    ]


def test_the_lugger_filled_away_for_a_course_is_trimmed_not_braced(lugger):
    """Old: "... braced full and steering WSW (250°), the course ordered."; the same tick."""
    got = _lines(_from(lugger), [("heave to", 600), ("fill away and steer 250", 240)])
    done = [(t, line) for t, line in got if line.startswith("Filled away")]
    assert done == [
        (777, "Filled away on the starboard tack; steering WSW (250°), the course ordered.")
    ]
    assert not [line for _, line in got if BRACES.search(line)]


def test_the_lugger_scudding_stands_by_no_braces(lugger):
    """Old: "Up helm; brace in the yards as she goes off." and "Up helm; stand by the braces.
    Bear up and scud."; scudding at 48 s as before."""
    got = _lines(_from(lugger), [("scud", 60)])
    assert got == [
        (0, "Order: scud."),
        (1, "Up helm."),
        (1, "Up helm. Bear up and scud."),
        (48, "Scudding before it, the wind on the starboard quarter, steering S by W (195°)."),
    ]


def test_the_lugger_put_about_for_a_course_is_trimmed_for_it(lugger):
    """`steer` across the wind's eye from close-hauled (a course she is put about for), ended
    on it and too near the wind for it. Old: "Tacked; braced up on the starboard tack, ...";
    and no line of her tack or her wear, ordered or for a course, names a brace or a yard."""
    world = _from(lugger)
    got = _lines(world, [("tack ship", 300), ("steer 300", 400)])
    ends = [line for _, line in got if line.startswith("Tacked")]
    assert ends == [
        "Tacked; full and by on the larboard tack, heading ENE (68°).",
        "Tacked; trimmed on the starboard tack, heading WNW (292°), full and by.",
    ]
    worn = _lines(_from(lugger), [("wear ship", 300)])
    assert not [line for _, line in got + worn if BRACES.search(line)]


def test_the_cutter_wears_without_after_yards_and_hove_to_mans_her_head_braces(cutter):
    """The cutter has head yards and no after yards. Old: "Stand by to wear ship. Up helm; brace
    in the after yards.", "Hands to the after braces; heave to." and "Fill away; man the after
    braces."; her head yards squared and braced up as before, every tick the same."""
    worn = _lines(_from(cutter), [("wear ship", 600)])
    assert (1, "Stand by to wear ship. Up helm.") in worn
    aft = [line for _, line in worn if line.startswith("Wind aft")]
    assert aft == [
        "Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up."
    ]
    assert [line for _, line in worn if line.startswith("Wore ship")] == [
        "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)."
    ]
    hove = _lines(_from(cutter), [("heave to", 600), ("fill away", 120)])
    assert (1, "Hands to the head braces; heave to.") in hove
    assert any(line == "Fill away; man the head braces." for _, line in hove)
    assert any(
        line.startswith("Filled away on the starboard tack; braced full and ") for _, line in hove
    )
    for line in [x for _, x in worn + hove]:
        assert "after yards" not in line and "after braces" not in line, line


def test_the_cutter_box_hauled_braces_up_no_after_yards(cutter):
    """Old: "Wind aft; braced up the after yards; shifted over the sheets. Haul out the
    mainsail!"; "Brace abox the head yards!" as it was."""
    got = _lines(_from(cutter), [("box haul", 600)])
    said = [line for _, line in got]
    assert "Wind aft; shifted over the sheets. Haul out the mainsail!" in said
    assert any(line.endswith("Brace abox the head yards!") for line in said)
    assert not [line for line in said if "after yards" in line]


def test_a_ship_with_after_yards_says_them_as_before():
    """The brig: her wear's first line and her heave-to's and fill-away's braces as they were."""
    settled = _settle(BRIG)
    worn = _lines(_from(settled), [("wear ship", 60)])
    assert any(line.endswith("; brace in the after yards.") for _, line in worn)
    hove = _lines(_from(settled), [("heave to", 600), ("fill away", 120)])
    said = [line for _, line in hove]
    assert "Hands to the after braces; heave to." in said
    assert "Fill away; man the after braces." in said
    assert any(
        line.startswith("Filled away on the starboard tack; braced full and ") for line in said
    )


def test_the_lugger_brought_up_squares_no_yards():
    """The anchor's road (`tests/test_anchor.py`: Carrick Road, 12 knots from the south-west,
    her head 335). Old: "Brought up. Stations for furling sail; square the yards."; the
    frigate's line as it was (`tests/test_anchor.py`)."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=335.0,
        ship_speed_kn=3.0,
        position={"lat_deg": 50.160, "lon_deg": -5.034},
        region="channel-west",
    )
    world = make_world(7, LUGGER, scenario)
    world.submit("set plain sail")
    world.run(240)
    got = _lines(world, [("come to an anchor", 431)])
    assert (430, "Brought up. Stations for furling sail.") in got


def test_a_boat_at_her_grapnel_squares_and_lays_abox_no_yard():
    """The launch off Falmouth in three fathoms and a half, brought up to her grapnel and got
    under way again by the fore-and-after's road. Old: "Brought up. Stations for furling sail;
    square the yards.", "... its sheet to windward! The topsail yard abox. Helm a-lee for the
    stern-board." and "She has paid off; right the helm, draw the jib, haul aft the main sheet,
    brace round the topsail yard."; every tick as it was. The rest of that road's words are a
    ship's (the bars, the sail-loosers, a jib she has not): another cause, not this step's."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=8.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=335.0,
        ship_speed_kn=2.0,
        position={"lat_deg": 50.152, "lon_deg": -5.040},
        region="channel-west",
    )
    world = make_world(7, "data/ships/boat-launch-31.yaml", scenario)
    world.submit("set the lug")
    world.run(60)
    got = _lines(world, [("come to an anchor", 2400), ("get under way", 1100)])
    said = [line for _, line in got]
    assert "Brought up. Stations for furling sail." in said
    assert (
        "Let go the downhauls, hoist away the jib, its sheet to windward! Helm a-lee for the "
        "stern-board."
    ) in said
    assert "She has paid off; right the helm, draw the jib, haul aft the main sheet." in said
    assert any(line.startswith("Under way on the starboard tack") for line in said)
    assert not [line for line in said if BRACES.search(line)]


# ---------------------------------------------------------------------------
# By the runner's door: the two lines no order of a player's reaches on a rig with no braced yard
# ---------------------------------------------------------------------------


def _wind(from_deg: float = 90.0, knots: float = 10.0) -> Wind:
    return Wind(
        WindParams.from_nautical(from_deg, knots, gustiness=0.0, variability=0.0), random.Random(0)
    )


def _deck(ship, wind) -> None:
    ship.dyn.apparent_wind_angle = units.relative_bearing(ship.dyn.heading, wind.direction_from)


def _turner(rate_deg_s: float, dies_in_s: float | None = None):
    """Physics that turns her toward the ordered heading at a fixed rate and keeps her speed, or
    loses it over `dies_in_s` (`tests/test_evolutions.py`'s `turner` and `staller`)."""
    state: dict = {}

    def stepper(ship, dt, wind) -> None:
        d = ship.dyn
        error = units.wrap_pi(d.target_heading - d.heading)
        step = units.deg_to_rad(rate_deg_s) * dt
        d.heading = units.wrap_2pi(
            d.heading + (error if abs(error) <= step else math.copysign(step, error))
        )
        speed0 = state.setdefault("speed", units.knots_to_ms(5.0))
        state["t"] = state.get("t", 0.0) + dt
        d.speed = speed0 if dies_in_s is None else max(0.0, speed0 * (1 - state["t"] / dies_in_s))
        _deck(ship, wind)

    return stepper


def _run(runner, ship, wind, stepper) -> list:
    notes = []
    for _ in range(3000):
        if not runner.in_progress():
            break
        runner.step(ship, 1.0, wind)
        stepper(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
    return notes


def _on_starboard(off_deg: float):
    ship = load_ship(LUGGER)
    wind = _wind()
    ship.dyn.heading = units.wrap_2pi(wind.direction_from - units.deg_to_rad(off_deg))
    ship.dyn.speed = units.knots_to_ms(5.0)
    _deck(ship, wind)
    return ship, Runner(ship), wind


def test_the_lugger_put_about_for_a_course_from_off_the_wind_is_luffed_up_not_braced_up():
    """Old: "Luff up and brace up: she is brought by the wind to go about."; the frigate's line
    as it was (`tests/test_evolutions.py`)."""
    ship, runner, wind = _on_starboard(120.0)
    runner.start(ship, "tack", "ship", {"course_deg": 200.0})
    notes = _run(runner, ship, wind, _turner(0.4))
    said = [n[2] for n in notes]
    assert said[0] == "Luff up: she is brought by the wind to go about."
    assert notes[-1][1] == "ship.tacked" and "braced" not in said[-1]


def test_the_lugger_missing_stays_squares_no_yards():
    """Her way gone before her head came to the wind (`tests/test_evolutions.py`'s miss). Old:
    "Squared the yards; she fell off on the starboard tack, to try again or to wear."; the
    urgent line squared none before it either."""
    ship, runner, wind = _on_starboard(55.0)
    runner.start(ship, "tack", "ship")
    notes = _run(runner, ship, wind, _turner(0.4, dies_in_s=60))
    missed = [n for n in notes if n[1] == "ship.missed_stays"]
    assert len(missed) == 1 and "square the yards" not in missed[0][2]
    assert notes[-1][1] == "ship.fell_off"
    assert notes[-1][2] == "She fell off on the starboard tack, to try again or to wear."
