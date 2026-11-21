"""Package 90, A2: the words of a rig with no yards, mended at their cause.

The going-about evolutions and their kin said "brace in the after yards", "braced up", "braced
sharp up", "Hands to the after braces" and "square the yards" whatever the rig, so that a lugger,
whose lug yards are no braced yards (`Spar.is_yard`), was told to brace in her after yards and
was braced up, and the cutter, the smack and the two schooners, whose yards are head yards alone,
braced up after yards they have not. A line that names a braced yard or its braces is now said
only where she works them, read from the yards the evolution swings (`scripts.head_and_after_yards`,
`scripts.braces_worked`, `scripts.braces_manned`), for every rig. A2's second pass (the lead's
nudge 34): on a rig without after yards the words follow the square sails set, not the yards
crossed, so that with none set she has the lugger's words, her sheets' (the smack under her
mainsail, fore staysail and jib was told to man her head braces and lay hove to by her sheets);
a vessel of one mast mans "the braces", not head braces; and the scud says its up-helm once. The
eight rigs with after yards say every line as before, whatever they have set. The words put in
their place are JUDGEMENT. Words only: every tick, every event's kind and every trace of heading,
speed and position the same, old beside new over all eighteen files (docs/dev/TuningNotes.md,
"Package 90, A2").

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
from freesail.ship.parts import SailState

LUGGER = "data/ships/lugger.yaml"
CUTTER = "data/ships/cutter.yaml"
SMACK = "data/ships/smack.yaml"
BRIG = "data/ships/brig.yaml"
# The anchor's two roads on the region's own chart (a scenario's `chart:` naming the region
# alone, `world.chart.chart_holding`, as only a test should): the same water, depths and holding
# as the whole chart that holds it, read in two seconds where the whole chart takes four more
# (A2's second pass: the lead's five-second line; `region: channel-west` before it)
ROAD_CHART = "channel-west"

# The eighteen files committed at A2, each with the braces her going about mans with every square
# sail on her braced yards set: the five boats and the lugger have no braced yard, and man their
# sheets; the cutter and the smack, of one mast, their braces ("head braces" before A2's second
# pass); the two schooners, whose yards are on the fore, their head braces; the rest have after
# yards too, and man their after braces (the hermaphrodite brig's main topsail and topgallant
# yards on her schooner's main among them). As filed, no sail set, the ten without after yards
# man their sheets and the eight their after braces. Named, not globbed, so that a file added
# later is no move of this guard.
BRACES_SQUARE_SET = {
    "bilander": "after braces",
    "boat-cutter-23": "sheets",
    "boat-cutter-28": "sheets",
    "boat-launch-25": "sheets",
    "boat-launch-31": "sheets",
    "boat-yawl-16": "sheets",
    "brig": "after braces",
    "cutter": "braces",
    "frigate-36": "after braces",
    "hermaphrodite-brig": "after braces",
    "lugger": "sheets",
    "merchant-brig": "after braces",
    "privateer-schooner": "head braces",
    "razee-44": "after braces",
    "seventy-four": "after braces",
    "sixty-four": "after braces",
    "smack": "braces",
    "topsail-schooner": "head braces",
}


@pytest.mark.parametrize(("name", "braces"), sorted(BRACES_SQUARE_SET.items()))
def test_every_file_is_read_for_the_braces_it_has(name, braces):
    """The key, read off every committed file as loaded (no sail set) and with every square sail
    on her braced yards set: the yards the evolutions swing, and so the braces their words name,
    and whether her braces are worked at all (`braces_worked`). Old (A2): the key as filed
    alone, "head braces" for the cutter, the smack and the two schooners whatever was set."""
    ship = load_ship(f"data/ships/{name}.yaml")
    head, after = scripts.head_and_after_yards(ship)
    assert bool(after) == (braces == "after braces")
    assert scripts.braces_manned(ship) == ("after braces" if after else "sheets")
    assert scripts.braces_worked(ship, head, after) == bool(after)
    for y in head + after:
        sail = ship.sail_of(y)
        if sail is not None and sail.cls == "square":
            sail.state = SailState.SET
    assert scripts.braces_manned(ship) == braces
    assert scripts.braces_worked(ship, head, after) == (braces != "sheets")
    assert scripts.one_masted(ship) == (braces == "braces" or name.startswith("boat-"))


# ---------------------------------------------------------------------------
# By the player's door
# ---------------------------------------------------------------------------


def _settle(path: str, seconds: int = 2400) -> bytes:
    """The lugger transcripts' settle (`tests/test_settee.py`), as a checkpoint to sail from;
    the brig's half as long (A2's second pass: the lead's five-second line), her words read
    there whole, every one as at 2,400 s."""
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
    for i in range(seconds):
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


@pytest.fixture(scope="module")
def smack() -> bytes:
    """The smack under plain sail, her mainsail, fore staysail and jib: no square sail set."""
    return _settle(SMACK)


@pytest.fixture(scope="module")
def brig() -> bytes:
    return _settle(BRIG, 1200)


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
    Bear up and scud."; and the up-helm said once (A2's second pass: "Up helm." and at once "Up
    helm. Bear up and scud." in A2); scudding at 48 s as before."""
    got = _lines(_from(lugger), [("scud", 60)])
    assert got == [
        (0, "Order: scud."),
        (1, "Up helm."),
        (1, "Bear up and scud."),
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


def test_the_cutter_wears_without_after_yards_and_hove_to_mans_her_braces(cutter):
    """The cutter has head yards and no after yards, on her one mast, her topsail set. Old:
    "Stand by to wear ship. Up helm; brace in the after yards.", "Hands to the after braces;
    heave to." and "Fill away; man the after braces."; and "Hands to the head braces; heave to."
    and "Fill away; man the head braces." in A2 (A2's second pass: a vessel of one mast has no
    head braces; the test was `..._mans_her_head_braces`); her yards squared and braced up as
    before, every tick the same, and "the yards", not "the head yards" (A2's second pass, its
    point 3 at its cause: "Wind aft. Squared the head yards; ..." before it)."""
    worn = _lines(_from(cutter), [("wear ship", 600)])
    assert (1, "Stand by to wear ship. Up helm.") in worn
    aft = [line for _, line in worn if line.startswith("Wind aft")]
    assert aft == [
        "Wind aft. Squared the yards; shifted over the sheets; hauled out and braced up."
    ]
    assert [line for _, line in worn if line.startswith("Wore ship")] == [
        "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)."
    ]
    hove = _lines(_from(cutter), [("heave to", 600), ("fill away", 120)])
    assert (1, "Hands to the braces; heave to.") in hove
    assert any(line == "Fill away; man the braces." for _, line in hove)
    assert any(
        line.startswith("Filled away on the starboard tack; braced full and ") for _, line in hove
    )
    for line in [x for _, x in worn + hove]:
        assert "after yards" not in line and "after braces" not in line, line
        assert "head braces" not in line, line


def test_the_cutter_with_her_square_sails_in_lies_to_her_sheets(cutter):
    """A2's second pass: her topsail taken in, no square sail set, she is hove to, filled away
    and worn by her sheets and has the lugger's words. Old (A2): "Hands to the head braces;
    heave to.", "Fill away; man the head braces.", "Fallen off; braced the yards full.",
    "Filled away on the starboard tack; braced full and steering WNW (292°).", "Wind aft. Squared
    the head yards; shifted over the sheets; hauled out and braced up." and "Wore ship; braced
    sharp up on the larboard tack, heading ENE (68°)."; every tick as it was."""
    taken_in = [("take in the square sails", 300)]
    hove = _lines(_from(cutter), [*taken_in, ("heave to", 600), ("fill away", 60)])
    assert [(t, line) for t, line in hove if t >= 300] == [
        (300, "Order: heave to."),
        (301, "Hauled flat aft the mainsail sheet; the foresail sheet to windward; helm a-lee."),
        (301, "Hands to the sheets; heave to."),
        (
            447,
            "Hove to on the starboard tack, under her fore-and-aft canvas, foresail sheet to "
            "windward, helm a-lee.",
        ),
        (900, "Order: fill away."),
        (901, "Hauled aft the head sheets; kept the helm a-lee to let her fall off."),
        (901, "Fill away; man the sheets."),
        (916, "Fallen off; right the helm."),
        (917, "Filled away on the starboard tack; steering WNW (292°)."),
    ]
    worn = _lines(_from(cutter), [*taken_in, ("wear ship", 600)])
    assert (301, "Stand by to wear ship. Up helm.") in worn
    assert (338, "Wind aft. Shifted over the sheets.") in worn
    assert (759, "Wore ship; full and by on the larboard tack, heading ENE (68°).") in worn


def test_the_cutter_box_hauled_braces_up_no_after_yards(cutter):
    """Old: "Wind aft; braced up the after yards; shifted over the sheets. Haul out the
    mainsail!"; and her yards and braces said without "head", a vessel of one mast (A2's second
    pass, its point 3 at its cause: "Ready about. Helm's a-lee; checked the lee head braces."
    and "Brace abox the head yards!" before it), every tick the same."""
    got = _lines(_from(cutter), [("box haul", 600)])
    said = [line for _, line in got]
    assert "Wind aft; shifted over the sheets. Haul out the mainsail!" in said
    assert "Ready about. Helm's a-lee; checked the lee braces." in said
    assert any(line.endswith("Brace abox the yards!") for line in said)
    assert not [line for line in said if "head yards" in line or "head braces" in line]
    assert not [line for line in said if "after yards" in line]


def test_the_cutter_boxed_off_round_by_the_stern_braces_up_no_after_yards(cutter):
    """Box her off (A2's second pass: the case the lead asked for), gone round by the stern from
    the settle, as a box-haul ends. Old: "Wind aft; braced up the after yards; shifted over the
    sheets. Haul out the mainsail!"; and "Up mainsail! Brace abox the head yards!" and "Box her
    off! Stand by the head braces." before its point 3 at its cause, a vessel of one mast having
    no head yards; every tick the same."""
    got = _lines(_from(cutter), [("box her off", 600)])
    assert (1, "Up mainsail! Brace abox the yards!") in got
    assert (1, "Box her off! Stand by the braces.") in got
    assert (58, "Wind aft; shifted over the sheets. Haul out the mainsail!") in got
    assert (99, "Boxed her off; braced sharp up on the starboard tack, full and by.") in got
    assert not [line for _, line in got if "after yards" in line]


def test_the_smack_under_her_fore_and_aft_canvas_lies_to_her_sheets(smack):
    """A2's second pass, the lead's case: the smack under her mainsail, fore staysail and jib, no
    square sail set, hove to and filled away by her sheets. Old (A2): "Hands to the head braces;
    heave to.", "Fill away; man the head braces.", "Fallen off; braced the yards full." and
    "Filled away on the starboard tack; braced full and steering WNW (292°)."; every tick as it
    was."""
    got = _lines(_from(smack), [("heave to", 600), ("fill away", 60)])
    assert got == [
        (0, "Order: heave to."),
        (1, "Only three hands to heave to; there are no more on deck."),
        (1, "Hauled flat aft the mainsail sheet; the foresail sheet to windward; helm a-lee."),
        (1, "Hands to the sheets; heave to."),
        (
            163,
            "Hove to on the starboard tack, under her fore-and-aft canvas, foresail sheet to "
            "windward, helm a-lee.",
        ),
        (600, "Order: fill away."),
        (601, "Only three hands to fill away; there are no more on deck."),
        (601, "Hauled aft the head sheets; kept the helm a-lee to let her fall off."),
        (601, "Fill away; man the sheets."),
        (610, "Fallen off; right the helm."),
        (611, "Filled away on the starboard tack; steering WNW (292°)."),
    ]


def test_the_smack_under_her_fore_and_aft_canvas_wears_and_scuds_by_her_sheets(smack):
    """Old (A2): "Wind aft. Squared the head yards; shifted over the sheets; hauled out and
    braced up.", "Wore ship; braced sharp up on the larboard tack, heading ENE (68°).", "Up helm;
    brace in the yards as she goes off." and "Up helm; stand by the braces. Bear up and scud.";
    every tick as it was, and no line naming a brace or a yard."""
    worn = _lines(_from(smack), [("wear ship", 600)])
    assert (1, "Stand by to wear ship. Up helm.") in worn
    assert (34, "Wind aft. Shifted over the sheets.") in worn
    assert (456, "Wore ship; full and by on the larboard tack, heading ENE (68°).") in worn
    scud = _lines(_from(smack), [("scud", 60)])
    assert [(t, line) for t, line in scud if not line.startswith("Only")] == [
        (0, "Order: scud."),
        (1, "Up helm."),
        (1, "Bear up and scud."),
    ]
    assert not [line for _, line in worn + scud if BRACES.search(line)]


def test_a_ship_with_after_yards_says_them_as_before(brig):
    """The brig: her wear's first line and her heave-to's and fill-away's braces as they were
    (A2's second pass: the settle a module's, half as long, for the five-second line)."""
    worn = _lines(_from(brig), [("wear ship", 60)])
    assert any(line.endswith("; brace in the after yards.") for _, line in worn)
    hove = _lines(_from(brig), [("heave to", 600), ("fill away", 120)])
    said = [line for _, line in hove]
    assert "Hands to the after braces; heave to." in said
    assert "Fill away; man the after braces." in said
    assert any(
        line.startswith("Filled away on the starboard tack; braced full and ") for line in said
    )


def test_a_ship_with_after_yards_and_her_square_sails_in_says_them_as_before(brig):
    """A2's second pass: the eight rigs with after yards say every line as before, whatever they
    have set; the brig with her square sails in, worn and scudding."""
    taken_in = [("take in the square sails", 300)]
    worn = _lines(_from(brig), [*taken_in, ("wear ship", 120)])
    said = [line for _, line in worn]
    assert "Stand by to wear ship. Up helm; brail up the spanker; brace in the after yards." in said
    assert (
        "Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up."
    ) in said
    scud = [line for _, line in _lines(_from(brig), [*taken_in, ("scud", 10)])]
    assert "Up helm; brailed up the spanker; brace in the yards as she goes off." in scud
    assert "Up helm; stand by the braces. Bear up and scud." in scud


def _shot_away(ship, which: str) -> None:
    """A mast shot away with everything on it (the checker's harness): her foremost lower mast,
    the one abaft it, or all of them, her bowsprit standing."""
    masts = sorted([sp for sp in ship.spars.values() if sp.cls == "mast"], key=lambda m: -m.x_m)
    for mast in masts if which == "all" else [masts[0] if which == "fore" else masts[1]]:
        mast.wrecked = True
        for part in ship.dependents(mast):
            part.wrecked = True


@pytest.mark.parametrize("which", ["main", "fore"])
def test_a_brig_dismasted_with_her_square_sails_in_says_her_words_as_before(brig, which):
    """A2's second pass, its third commit (the checker's finding 1): a rig built with after yards
    keeps A2's words when she has lost a mast, whatever she has set (`after_yards_as_built`).
    The brig, her square sails in and her main (or her fore) shot away, by the player's door:
    her heave-to's, fill-away's, wear's and scud's lines as at 5c5e04be, line for line and tick
    for tick (measured there). Before it, read from the yards she had left, she was given the
    lugger's: "Hands to the sheets; heave to.", "Right the helm.", "Wind aft. Shifted over the
    sheets." and "Up helm." and "Bear up and scud."."""
    world = _from(brig)
    world.submit("take in the square sails")
    world.run(300)
    _shot_away(world.ship, which)
    cut = replay.checkpoint_bytes(world)
    if which == "main":
        assert _lines(_from(cut), [("heave to", 600), ("fill away", 120)]) == [
            (0, "Order: heave to."),
            (1, "The fore topmast staysail sheet to windward; helm a-lee."),
            (1, "Hands to the head braces; heave to."),
            (
                600,
                "Hove to on the starboard tack, under her fore-and-aft canvas, fore topmast "
                "staysail sheet to windward, helm a-lee.",
            ),
            (600, "Order: fill away."),
            (601, "Hauled aft the head sheets; kept the helm a-lee to let her fall off."),
            (601, "Fill away; man the head braces."),
            (601, "Braced the yards full."),
            (602, "Filled away on the starboard tack; braced full and steering WNW (292°)."),
        ]
    aft = "Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up."
    assert aft in [line for _, line in _lines(_from(cut), [("wear ship", 600)])]
    assert _lines(_from(cut), [("scud", 60)]) == [
        (0, "Order: scud."),
        (1, "Up helm; brace in the yards as she goes off."),
        (1, "Up helm; stand by the braces. Bear up and scud."),
    ]


def test_the_smack_under_her_fore_and_aft_canvas_box_hauls_and_boxes_off_by_no_braces(smack):
    """A2's second pass, its third commit (the checker's finding 2): the box-haul family follows
    the square sails set as the tack and the wear do. The smack under plain sail, no square sail
    set, box-hauled, boxed off and worn short round: her yards swung abox bare, the lines say the
    helm and the mainsail hauled up, and she ends full and by. Old: "Ready about. Helm's a-lee;
    checked the lee braces.", "Up mainsail! Brace abox the yards!", "Box her off! Stand by the
    braces.", "Box-hauled; braced sharp up on ...", "Boxed her off; braced sharp up on ..." and
    "Wore short round; braced sharp up on ..."; every tick as it was."""
    hauled = _lines(_from(smack), [("box haul", 600)])
    assert (1, "Ready about. Helm's a-lee.") in hauled
    assert (24, "Up mainsail!") in hauled
    assert (177, "Box-hauled; full and by on the larboard tack, heading ENE (68°).") in hauled
    boxed = _lines(_from(smack), [("box her off", 600)])
    assert (1, "Up mainsail!") in boxed and (1, "Box her off!") in boxed
    assert (114, "Boxed her off; trimmed on the starboard tack, full and by.") in boxed
    worn = _lines(_from(smack), [("wear short round", 600)])
    assert (1, "Up mainsail!") in worn
    assert (114, "Wore short round; full and by on the larboard tack, heading ENE (68°).") in worn
    for _, line in hauled + boxed + worn:
        assert not BRACES.search(line), line


def test_the_lugger_brought_up_squares_no_yards():
    """The anchor's road (`tests/test_anchor.py`: Carrick Road, 12 knots from the south-west,
    her head 335), on the region's own chart (`ROAD_CHART`). Old: "Brought up. Stations for
    furling sail; square the yards."; the frigate's line as it was (`tests/test_anchor.py`)."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=335.0,
        ship_speed_kn=3.0,
        position={"lat_deg": 50.160, "lon_deg": -5.034},
        chart=ROAD_CHART,
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
    ship's (the bars, the sail-loosers, a jib she has not): another cause, not this step's. On
    the region's own chart (`ROAD_CHART`), and got under way once the come-to-anchor is done
    (her brought-up line at 978 s; at 2,400 s before A2's second pass, the same lines)."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=8.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=335.0,
        ship_speed_kn=2.0,
        position={"lat_deg": 50.152, "lon_deg": -5.040},
        chart=ROAD_CHART,
    )
    world = make_world(7, "data/ships/boat-launch-31.yaml", scenario)
    world.submit("set the lug")
    world.run(60)
    got = _lines(world, [("come to an anchor", 1200), ("get under way", 1100)])
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


def _on_starboard(off_deg: float, path: str = LUGGER):
    ship = load_ship(path)
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


@pytest.mark.parametrize(
    ("topsail", "squared", "fell_off"),
    [
        (SailState.FURLED, False, "She fell off on the starboard tack, to try again or to wear."),
        (
            SailState.SET,
            True,
            "Squared the yards; she fell off on the starboard tack, to try again or to wear.",
        ),
    ],
    ids=["no square sail set", "her topsail set"],
)
def test_the_cutter_missing_stays_squares_her_yards_only_with_a_square_sail_set(
    topsail, squared, fell_off
):
    """A2's second pass, by the runner's door (the lugger's miss above): the cutter's head yards
    squared in words, in the urgent line and the fallen-off line, only with a square sail set.
    Old (A2): "square the yards" and "Squared the yards; she fell off ..." whatever she had set;
    with her topsail set as before."""
    ship, runner, wind = _on_starboard(55.0, CUTTER)
    ship.sails["topsail"].state = topsail
    runner.start(ship, "tack", "ship")
    notes = _run(runner, ship, wind, _turner(0.4, dies_in_s=60))
    missed = [n for n in notes if n[1] == "ship.missed_stays"]
    assert len(missed) == 1 and ("square the yards" in missed[0][2]) == squared
    assert notes[-1][1] == "ship.fell_off" and notes[-1][2] == fell_off


def _hanger(rate_deg_s: float, at_deg: float, dies_in_s: float):
    """Physics that turns her until her head is `at_deg` off the wind, then lets her way die
    over `dies_in_s` (`tests/test_evolutions.py`'s `hangs_in_stays`)."""
    turn = _turner(rate_deg_s)
    hung: dict = {}

    def stepper(ship, dt, wind) -> None:
        rel = units.relative_bearing(ship.dyn.heading, wind.direction_from)
        if abs(rel) > units.deg_to_rad(at_deg):
            turn(ship, dt, wind)
        else:
            speed0 = hung.setdefault("speed", ship.dyn.speed)
            hung["t"] = hung.get("t", 0.0) + dt
            ship.dyn.speed = max(0.0, speed0 * (1 - hung["t"] / dies_in_s))
            _deck(ship, wind)

    return stepper


@pytest.mark.parametrize(
    ("path", "topsail", "aback"),
    [
        (CUTTER, "topsail", "the yards aback to box her off"),
        ("data/ships/topsail-schooner.yaml", "fore.topsail", "the head yards aback to box her off"),
    ],
    ids=["the cutter, of one mast", "the topsail schooner, of two"],
)
def test_hung_in_stays_a_one_master_lays_her_yards_aback_not_her_head_yards(path, topsail, aback):
    """A2's second pass, by the runner's door (`tests/test_evolutions.py`'s hang): her topsail
    set, hung in stays, the cutter's yards are laid aback in words as "the yards", a vessel of one
    mast having no head yards; the schooner's as before. Old: "the head yards aback to box her
    off" of both."""
    ship, runner, wind = _on_starboard(45.0, path)
    ship.sails[topsail].state = SailState.SET
    runner.start(ship, "tack", "ship")
    notes = _run(runner, ship, wind, _hanger(1.0, 8.0, 30.0))
    hung = [n[2] for n in notes if n[2].startswith("Her way is gone; she hangs in stays.")]
    assert hung == [f"Her way is gone; she hangs in stays. Helm kept a-lee; {aback}."]


@pytest.mark.parametrize(
    ("name", "which"),
    [
        ("brig", "main"),
        ("brig", "fore"),
        ("hermaphrodite-brig", "main"),
        ("hermaphrodite-brig", "fore"),
        ("bilander", "main"),
        ("bilander", "fore"),
        ("seventy-four", "all"),
        ("sixty-four", "all"),
        ("razee-44", "all"),
        ("brig", "all"),
    ],
)
def test_a_rig_built_with_after_yards_is_read_as_built_whatever_she_has_lost(name, which):
    """A2's second pass, its third commit (the checker's finding 1), at the reader: a rig built
    with after yards (`after_yards_as_built`, every braced yard as filed) is read by A2's own
    readers when a mast is shot away, her square sails in (as loaded): her braces worked while
    she has a braced yard left, A2's `has_braced_yards`; her braces manned A2's way; and the scud
    braces in every working yard, the yards under the bowsprit of the 74, the 64 and the razee
    with every mast gone among them (A2's `working_yards`). Before it, read from the yards she
    had left, the brig with her main gone was given the lugger's sheets, and the 74 with her masts
    gone was told nothing of the spritsail yards the scud still braces in."""
    ship = load_ship(f"data/ships/{name}.yaml")
    _shot_away(ship, which)
    head, after = scripts.head_and_after_yards(ship)
    assert scripts.after_yards_as_built(ship)
    assert scripts.braces_worked(ship, head, after) == bool(head or after)
    a2 = "after braces" if after else "head braces" if head else "sheets"
    assert scripts.braces_manned(ship) == a2
    braced_in = bool(scripts.working_yards(ship))
    assert scripts.ScudScript(ship, {}, {})._braces_worked() == braced_in
    runner = Runner(ship)
    said = runner.start(ship, "scud", "ship")
    notes = [n[2] for n in ship.drain_notes()]
    if braced_in:
        assert said == "Up helm; stand by the braces. Bear up and scud."
        assert "Up helm; brace in the yards as she goes off." in notes
    else:
        # no braced yard left (the brig with every mast gone): A2's "Up helm." twice, the
        # bare repeat kept on a rig built with after yards, whose lines do not move
        assert said == "Up helm. Bear up and scud."
        assert "Up helm." in notes


def test_a_rig_of_head_yards_alone_with_nothing_to_draw_meets_her_with_the_helm():
    """A2's second pass, its third commit (the checker's point 3), by the runner's door: the cutter
    as loaded, no square sail and no head sail set, put about: her head yards hauled round bare,
    the line the helm's, which is given her new course then (JUDGEMENT). Old: "Let go and haul."
    whatever she had set."""
    ship, runner, wind = _on_starboard(55.0, CUTTER)
    runner.start(ship, "tack", "ship")
    said = [n[2] for n in _run(runner, ship, wind, _turner(0.4))]
    assert "Meet her with the helm." in said
    assert not [line for line in said if "Let go and haul" in line]
