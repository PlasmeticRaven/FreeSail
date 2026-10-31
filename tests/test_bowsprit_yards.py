"""Package 75, the engine's bowsprit step (B3.2; docs/design/Design-ShipsEngineExtensions.md §4,
§10.2): the yards under the bowsprit (D8(b)), the 64's, the 74's and the bilander's.

The spritsail yard is slung under the bowsprit near the cap and the sprit-topsail yard under the
jib-boom near its end (Steel 1794 vol. I pp. 196-197; Lavery I27-I30). Each is a yard of class
`yard` with a square sail, braced within its limit by name and by the orders that brace every
yard, and set, taken in, furled and reefed by the square sail's own evolutions (Ext §4.1,
§4.3). Their chains root at the bowsprit, so until this step the bowsprit was counted as a mast
with yards, the foremost: the head yards were the two sprit yards, "mainsail haul" swung the
fore yards, a schooner with them was square-rigged (Ext §4.2, observed). One predicate,
`Ship.under_bowsprit`, read at nine places, keeps them out of every count of masts and levels:
the masts with yards; the head and after yards, the sprit yards among the head yards; whether
she is square-rigged; the helm's mark; the stagger, the trim by level and the heavy weather's
ease, where each keeps its own target; `trim sails`' judgement of a wind; the light sails
clewed up hove to and backing and filling; `shorten sail`'s first lines; and the windage of a
spar, where its sail is.

None of the eight files carries a yard under the bowsprit (`tests/test_rig_classing.py`, the
probe), so the tests run on the fixtures of `tests/rig_fixtures.py`, whose frigate carries both
yards cut to the contract, and on three of the eight files with the two yards added in memory, as
Ext §4.2's observation added them. No ship of the eight moves: the golden classing table
(`tests/test_rig_classing.py`), and the places read on the eight below.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import pytest
import yaml
from rig_fixtures import (
    SPRIT_BRACE_LIMIT_DEG,
    frigate_with_driver,
    frigate_with_mizen_yard,
    frigate_with_mizen_yard_doc,
    write_ship,
)

from freesail import orders
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.storm import bowsprit_sail_lines, shorten_sail_lines
from freesail.physics.sails import (
    SAIL_CLASSES,
    _spar_places,
    _square_rigged,
    compute_sail_forces,
)
from freesail.physics.wind import Wind, WindParams
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState
from freesail.world.ships import _balanced_speed_ms, polar_of

ROOT = Path(__file__).resolve().parents[1]
YARDS = ("spritsail.yard", "sprit_topsail.yard")
SAILS = ("spritsail", "sprit_topsail")
SPRIT = set(YARDS) | set(SAILS)
LIMIT_DEG = float(SPRIT_BRACE_LIMIT_DEG)  # the fixture's sprit yards' limit, 30 degrees

# The eight files of the golden classing table (`tests/test_rig_classing.py`).
EIGHT = (
    "frigate-36",
    "brig",
    "merchant-brig",
    "cutter",
    "topsail-schooner",
    "privateer-schooner",
    "smack",
    "lugger",
)

# The golden table's rows (`tests/test_rig_classing.py`, Ext §10.1) of the three files Ext §4.2
# observed with the yards added: the masts with yards, the head yards on them and the after
# yards, the mast backed, square-rigged, the stagger (degrees), the driver, the boom sails and
# the dipping lugs.
ROWS: dict[str, tuple] = {
    "frigate-36": (
        ["fore.mast", "main.mast", "mizzen.mast"],
        (4, 8),
        "main.mast",
        True,
        2.0,
        ["mizzen.spanker"],
        ["mizzen.spanker"],
        [],
    ),
    "brig": (
        ["fore.mast", "main.mast"],
        (4, 4),
        "main.mast",
        True,
        2.0,
        ["main.spanker"],
        ["main.spanker"],
        [],
    ),
    "topsail-schooner": (["fore.mast"], (2, 0), "fore.mast", False, None, [], ["main.sail"], []),
}
# The fixtures carry them cut to the contract: the frigate's row, her driver and her boom sail
# the mizen course cut at the mast (B3.1; the driver's fixture with the driver in the sail room).
FIXTURE_ROW = (
    ["fore.mast", "main.mast", "mizzen.mast"],
    (4, 8),
    "main.mast",
    True,
    2.0,
    ["mizzen.course"],
    ["mizzen.course"],
    [],
)


def _with_the_sprit_yards(name: str) -> Ship:
    """`data/ships/<name>.yaml` with a spritsail yard under its bowsprit and a sprit-topsail yard
    under its jib-boom, each with a square sail in "all sail" alone, added in memory as Ext
    §4.2's observation added them. The classing reads their classes and chains, not their places:
    each hangs a metre under its spar near its end, as long, rated and canvassed as the fore
    topsail and the fore topgallant, braced within the fixture's limit."""
    doc = yaml.safe_load((ROOT / "data" / "ships" / f"{name}.yaml").read_text(encoding="utf-8"))
    spars = {s["id"]: s for s in doc["spars"]}
    sails = {s["id"]: s for s in doc["sails"]}
    deck = doc["hull"]["deck_height_m"]
    bowsprit, jib_boom = spars["bowsprit"], spars["jib_boom"]
    cap = bowsprit["x_m"] + bowsprit["length_m"]
    end = cap + jib_boom["length_m"]
    for yard, sail, on, x, like in (
        ("spritsail.yard", "spritsail", "bowsprit", cap - 1.0, "fore.topsail"),
        ("sprit_topsail.yard", "sprit_topsail", "jib_boom", end - 1.0, "fore.topgallant"),
    ):
        height = spars[on]["height_m"] - 1.0
        doc["spars"].append(
            {
                "id": yard,
                "class": "yard",
                "on": on,
                "x_m": round(x, 1),
                "length_m": spars[f"{like}.yard"]["length_m"],
                "height_m": round(height, 1),
                "brace_limit_deg": SPRIT_BRACE_LIMIT_DEG,
                "rating_kn": spars[f"{like}.yard"]["rating_kn"],
            }
        )
        doc["sails"].append(
            {
                "id": sail,
                "class": "square",
                "yard": yard,
                "area_m2": sails[like]["area_m2"],
                "x_m": round(x, 1),
                "centre_height_m": round(deck + height - 1.0, 1),
            }
        )
        doc["groups"]["all sail"].append(sail)
    return ship_from_dict(doc, f"{name} with the yards under the bowsprit")


def _under_plain_sail(ship: Ship, *more: str) -> Ship:
    for sid in [*ship.groups["plain sail"], *more]:
        ship.sails[sid].state = SailState.SET
    return ship


def _classing(ship: Ship) -> tuple:
    """The golden table's fields (`tests/test_rig_classing.py`), the head yards counted on the
    masts: the yards under the bowsprit are head yards too (place 2), and no mast's."""
    head, after = scripts.head_and_after_yards(ship)
    to_back = scripts.yards_to_back(ship)
    targets = {y.id: y.brace_limit for y in scripts.working_yards(ship)}
    _, stagger = yard_trim.stagger(ship, targets)
    return (
        [m.id for m in scripts._masts_with_yards(ship)],
        (len([y for y in head if not ship.under_bowsprit(y)]), len(after)),
        ship.mast_of(to_back[0]).id if to_back else None,
        _square_rigged(ship),
        None if stagger is None else round(stagger, 1),
        [s.id for s in scripts.after_gaff_sails(ship)],
        [s.id for s in scripts.boom_sails(ship)],
        [s.id for s in scripts.dipping_lugs(ship)],
    )


def _bare(ship: Ship, awa: float) -> Runner:
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
    return round(math.degrees(angle), 3)


# ---------------------------------------------------------------------------
# The classing (Ext §4.2, places 1, 2, 3 and 5)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", list(ROWS))
def test_with_the_yards_added_each_row_is_the_row_as_filed(name):
    """Ext §10.2: with a spritsail yard and a sprit-topsail yard added, every field of the
    frigate's, the brig's and the topsail schooner's rows equals the row as filed (risk 5: the
    brig's "mainsail haul" swinging her fore yards, the schooner hove to as a square-rigger).
    The two yards are head yards, and the schooner's are her only other yards."""
    ship = _under_plain_sail(_with_the_sprit_yards(name))
    assert {pid for pid in ship.parts if ship.under_bowsprit(pid)} == SPRIT
    assert _classing(ship) == ROWS[name]
    head, after = scripts.head_and_after_yards(ship)
    assert [y.id for y in head if ship.under_bowsprit(y)] == list(YARDS)
    assert not any(ship.under_bowsprit(y) for y in after)
    assert not any(ship.under_bowsprit(y) for y in scripts.yards_to_back(ship))


@pytest.mark.parametrize("fixture", [frigate_with_mizen_yard, frigate_with_driver])
def test_the_fixtures_classing_is_the_frigates_row_with_the_sprit_yards_present(fixture):
    """The task's own: the fixture whole, its spritsail yards present, classes as the frigate's
    row with the mizen course her driver (B3.1); the head yards are the fore's four and the two
    under the bowsprit, in the file's order."""
    ship = _under_plain_sail(fixture())
    assert _classing(ship) == FIXTURE_ROW
    head, _after = scripts.head_and_after_yards(ship)
    assert [y.id for y in head] == [
        "fore.yard",
        "fore.topsail.yard",
        "fore.topgallant.yard",
        "fore.royal.yard",
        *YARDS,
    ]
    assert [y.id for y in scripts.after_square_yards(ship)] == [
        "mizzen.topsail.yard",
        "mizzen.topgallant.yard",
        "mizzen.royal.yard",
        "mizzen.crossjack.yard",
    ]
    courses = [s.id for s in scripts.lowest_square_sails(ship)]
    assert courses == ["fore.course", "main.course"]  # a spritsail is no course


@pytest.mark.parametrize(
    "name, jib", [("cutter", "jib"), ("smack", "jib"), ("lugger", "flying_jib")]
)
def test_under_bowsprit_is_false_for_every_jib(name, jib):
    """Ext §4.2: a jib's chain may root at the bowsprit too (the cutter's and the smack's jib on
    the traveller, the lugger's flying jib), and the predicate names the yards and their square
    sails alone. On the fixture no jib, staysail or spar of the head is under the bowsprit, and
    the four parts that are are the two yards and their sails."""
    ship = load_ship(f"data/ships/{name}.yaml")
    assert ship.mast_of(jib).cls == "bowsprit" and not ship.under_bowsprit(jib)
    ship = frigate_with_mizen_yard()
    assert {pid for pid in ship.parts if ship.under_bowsprit(pid)} == SPRIT
    assert not any(ship.under_bowsprit(s) for s in ship.sails.values() if s.is_fore_and_aft)
    for sid in ("bowsprit", "jib_boom", "flying_jib_boom"):
        assert ship.mast_of(sid).id == "bowsprit" and not ship.under_bowsprit(sid)


# ---------------------------------------------------------------------------
# The trims (places 5 and 6): each keeps its own target
# ---------------------------------------------------------------------------


def _trimmed(ship: Ship, text: str, awa_deg: float) -> tuple[str, dict[str, float]]:
    """`text` given with `awa_deg` of apparent wind on the larboard bow and worked to its end:
    its words and the yards' angles from square, degrees, unsigned."""
    runner = _bare(ship, math.radians(-awa_deg))
    _kind, words, _data = orders.handle(ship, text)
    _run(runner, ship)
    return words, {y.id: abs(_deg(y.brace_angle)) for y in scripts.working_yards(ship)}


@pytest.mark.parametrize(
    "text, heavy, sharper",
    [("trim sails", False, 2), ("trim sails", True, 3), ("brace sharp up", False, 2)],
)
def test_on_a_wind_each_sprit_yard_keeps_its_own_target(text, heavy, sharper):
    """Ext §4.2 place 5: thirty-eight degrees of apparent wind, plain sail and the sprit sails
    set. The trims brace the after yards sharper than the head yards and say so, as the
    frigate's (Fincham 1843, art. 94: two degrees, three in heavy weather with the head yards
    eased), and each yard under the bowsprit to its own limit: never braced in a level from the
    other (`trim.by_level`), never staggered as a mast's yards, the head mast's (`trim.stagger`),
    never eased as a mast's lowest yard in heavy weather, the topsails at their third reef
    (`trim.eased_lowest`). Measured on the rule's absence: the spritsail yard braced in to 28
    degrees (18.75 in heavy weather), and no stagger named."""
    ship = _under_plain_sail(frigate_with_mizen_yard(), *SAILS)
    if heavy:
        for sid in ("fore.topsail", "main.topsail", "mizzen.topsail"):
            ship.sails[sid].reefs = 3
        assert yard_trim.heavy_weather_trim(ship)
    words, angle = _trimmed(ship, text, 38.0)
    assert f"the after yards {('two', 'three')[sharper - 2]} degrees sharper" in words, words
    assert angle["main.yard"] - angle["fore.yard"] == pytest.approx(sharper, abs=0.01)
    assert [angle[y] for y in YARDS] == [LIMIT_DEG, LIMIT_DEG]


def test_trim_sails_judges_the_wind_by_the_masts_lowest_yards_alone():
    """Ext §4.2 place 6: `trim sails` is on a wind when every mast's lowest yard wants to go
    sharper than it can (package 37p), and a yard under the bowsprit is no mast's. The sprit
    yards' limit raised to 85 degrees, beyond the fore yard's 62, and the wind 55 degrees on
    the bow: the masts' yards want more than their limits, the sprit yards less than theirs.
    She is on a wind: each level braced in from the one below (Luce 1884, p. 418) and the after
    yards staggered, the sprit yards at their own target. Measured on the rule's absence: off
    the wind, the fore topsail yard at its limit, 64 degrees, beyond its course's."""
    doc = frigate_with_mizen_yard_doc()
    for s in doc["spars"]:
        if s["id"] in YARDS:
            s["brace_limit_deg"] = 85
    ship = _under_plain_sail(ship_from_dict(doc, "fixture.yaml"), *SAILS)
    words, angle = _trimmed(ship, "trim sails", 55.0)
    assert "the after yards two degrees sharper" in words, words
    assert angle["fore.topsail.yard"] == pytest.approx(angle["fore.yard"] - 2.0, abs=0.01)
    want = 90.0 - (55.0 - math.degrees(SAIL_CLASSES["square"].peak_alpha))
    assert want < 85.0 and [angle[y] for y in YARDS] == pytest.approx([want, want], abs=0.01)


# ---------------------------------------------------------------------------
# The helm's mark (place 4) and the windage (place 9)
# ---------------------------------------------------------------------------


def _by_the_wind(*sets: str, off_deg: float = 60.0) -> Ship:
    """The fixture with `sets` set, at its balanced speed `off_deg` off a 15-knot wind, the
    yards and sheets trimmed as the polar trims them, the forces read once."""
    ship = frigate_with_mizen_yard()
    for sid in sets:
        ship.sails[sid].state = SailState.SET
    _balanced_speed_ms(ship, off_deg, 15.0)
    wind = Wind(WindParams.from_nautical(off_deg, 15.0, 0.0, 0.0), random.Random(0))
    compute_sail_forces(ship, wind)
    return ship


def test_the_helms_mark_is_never_a_sail_under_the_bowsprit():
    """Ext §4.2 place 4: a sail under the bowsprit is none of the helm's marks (package 37p:
    the highest square sail set lifting first, the rest the warning). Its yard's level would be
    a course's, and lifting first it would be her warning: measured on the rule's absence, the
    spritsail was the helm's rest under plain sail, and with the sprit sails alone set her mark.
    With the courses and the sprit sails the courses are the mark and the rest; with the sprit
    sails alone she has no mark, as a ship with no square sail drawing has none."""
    plain = list(frigate_with_mizen_yard().groups["plain sail"])
    ship = _by_the_wind(*plain, *SAILS)
    assert ship.sails["spritsail"].is_set and ship.sails["spritsail"].force_kn > 0.0
    assert ship.extra["helm_mark_sail"] == "mizzen.topgallant"
    assert ship.extra["helm_rest_sail"] == "fore.course"
    ship = _by_the_wind("fore.course", "main.course", *SAILS)
    assert (ship.extra["helm_mark_sail"], ship.extra["helm_rest_sail"]) == (
        "fore.course",
        "main.course",
    )
    ship = _by_the_wind(*SAILS)
    assert _square_rigged(ship) and ship.sails["sprit_topsail"].force_kn > 0.0
    assert not {"helm_mark", "helm_mark_sail", "helm_rest"} & set(ship.extra)


def test_the_windage_of_a_yard_under_the_bowsprit_is_where_its_sail_is():
    """Ext §4.2 place 9: each yard's windage acts at its own station (`_spar_x`), where its sail
    hangs (the spritsail's centre under its yard; the sprit topsail's between its yard and the
    spritsail yard's arms), not at the bowsprit's heel; every other spar's as before, a child at
    its root's (the jib-boom at the bowsprit's heel, a topsail yard at its mast)."""
    ship = frigate_with_mizen_yard()
    clr = ship.hull.spec.clr_x_m
    lever = {spar.id: lev for spar, _height, lev in _spar_places(ship)}
    for yard in YARDS:
        assert lever[yard] == pytest.approx(ship.spars[yard].x_m - clr)
    sprit, sprit_top = (ship.spars[y].x_m for y in YARDS)
    assert ship.sails["spritsail"].x_m == pytest.approx(sprit)
    assert sprit < ship.sails["sprit_topsail"].x_m < sprit_top
    bowsprit = ship.spars["bowsprit"].x_m
    assert bowsprit < sprit - 5.0
    assert lever["jib_boom"] == lever["flying_jib_boom"] == pytest.approx(bowsprit - clr)
    assert lever["fore.topsail.yard"] == pytest.approx(ship.spars["fore.mast"].x_m - clr)


# ---------------------------------------------------------------------------
# The handling (Ext §4.3): the manoeuvres at seed 7, shortening sail
# ---------------------------------------------------------------------------


def _world(tmp_path, *sprits: str, knots: float = 15.0):
    """The fixture whole in a fifteen-knot northerly on the starboard tack, sixty degrees off
    the wind, under plain sail (and `sprits`) and settled with the yards trimmed, as the truths
    settle the frigate (`tests/test_known_truths.py`)."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=300.0,
        ship_speed_kn=4.0,
    )
    world = make_world(7, write_ship(frigate_with_mizen_yard_doc(), tmp_path, "sprit"), scenario)
    for text in ("set plain sail", "brace sharp up on the starboard tack"):
        world.submit(text)
    for sid in sprits:
        world.submit(f"set the {sid.replace('_', ' ')}")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    for sid in sprits:
        assert world.ship.sails[sid].is_set, sid
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


def _angles(world) -> dict[str, float]:
    return {y: round(_deg(world.ship.spars[y].brace_angle), 1) for y in YARDS}


def _script(world, kind):
    runner = world.ship.extra["evolutions"]
    (script,) = [i.script for i in runner.instances if isinstance(i.script, kind)]
    return script


def test_in_stays_they_swing_with_the_head_yards_and_mainsail_haul_swings_the_after_yards(
    tmp_path,
):
    """Ext §4.3 and §10.2: at "mainsail haul" the main and mizzen yards swing, and only they; at
    "let go and haul" the yards under the bowsprit swing with the head yards (`TackScript`,
    `head_and_after_yards`), each to its own sharp-up limit on the new tack. Lever has the
    spritsail yard topped the contrary way at "mainsail haul" (l. 9386); the horizontal swing
    stands in for the topping (Plainly, Ext §4.4)."""
    world = _world(tmp_path)
    assert _angles(world) == dict.fromkeys(YARDS, LIMIT_DEG)
    world.submit("tack ship")
    _until(world, "Mainsail haul", 400)
    tack = _script(world, scripts.TackScript)
    swung = {y.id for y in tack.swing.yards}
    assert swung == {y.id for y in tack.after}
    assert {world.ship.mast_of(y).id for y in tack.swing.yards} == {"main.mast", "mizzen.mast"}
    assert set(YARDS) <= {y.id for y in tack.head}
    _until(world, "Let go and haul", 600)
    assert _angles(world) == dict.fromkeys(YARDS, LIMIT_DEG)  # held through the mainsail haul
    assert [y.id for y in tack.swing.yards] == [y.id for y in tack.head]
    _until(world, "Tacked", 900)
    assert world.ship.dyn.tack == "larboard"
    assert _angles(world) == dict.fromkeys(YARDS, -LIMIT_DEG)
    assert _deg(world.ship.spars["fore.yard"].brace_angle) < -LIMIT_DEG


def test_wearing_they_follow_the_wind_with_the_head_yards(tmp_path):
    """Ext §4.3: wearing, the yards under the bowsprit follow the wind with the head yards
    (`follow_wind`), as Lever's spritsail is kept set and braced until she comes to (l.
    9722-9725): square as the wind comes aft, braced up on the new tack when she has worn."""
    world = _world(tmp_path, *SAILS)
    world.submit("wear ship")
    _until(world, "Up helm", 200)
    wear = _script(world, scripts.WearScript)
    fore = ["fore.yard", "fore.topsail.yard", "fore.topgallant.yard", "fore.royal.yard"]
    assert [y.id for y in wear.head] == [*fore, *YARDS]
    assert not set(YARDS) & {y.id for y in wear.after}
    least = LIMIT_DEG
    for _ in range(1500):
        world.tick()
        least = min(least, *(abs(a) for a in _angles(world).values()))
        if any(e.kind == "ship.wore" for e in world.log):
            break
    assert least < 1.0  # squared with the head yards as the wind came aft
    assert world.ship.dyn.tack == "larboard"
    assert _angles(world) == dict.fromkeys(YARDS, -LIMIT_DEG)
    assert all(world.ship.sails[s].is_set for s in SAILS)


def test_hove_to_their_sails_are_clewed_up_and_their_yards_kept_full(tmp_path):
    """Ext §4.3 place 7: hove to, the sprit sails are clewed up with the light head sails (Luce
    1866, ch. XXVI, "settle down the top-gallant sails and royals, or clew them up", carried to
    them by judgement: left set a spritsail pays her head off), their yards among those kept
    full and braced up for the tack; she lies to. The log names them in a list, as Ext §4.3
    gives it; a ship with nothing under her bowsprit keeps the words she always had."""
    world = _world(tmp_path, *SAILS)
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(600):
        world.tick()
    texts = [e.text for e in _after(world, start)]
    assert "Clewed up the fore topgallant, the spritsail and the sprit topsail." in texts
    assert any(e.kind == "ship.hove_to" for e in _after(world, start)), texts
    assert all(world.ship.sails[s].state is SailState.IN_THE_GEAR for s in SAILS)
    assert _angles(world) == dict.fromkeys(YARDS, LIMIT_DEG)


def test_backing_and_filling_their_sails_are_hauled_up(tmp_path):
    """Ext §4.2 place 7: backing and filling, as for heaving to, the courses are hauled up, the
    driver brailed and the light sails forward clewed up (`BackAndFillScript`), the sprit sails
    with them."""
    world = _world(tmp_path, *SAILS)
    start = world.clock.tick
    world.submit("back and fill")
    world.tick()
    (hauled,) = [e.text for e in _after(world, start) if e.text.startswith("Hauled up ")]
    assert hauled.endswith("the spritsail and the sprit topsail."), hauled
    assert all(world.ship.sails[s].state is SailState.IN_THE_GEAR for s in SAILS)


def test_shorten_sail_takes_them_in_first_and_never_reefs_them():
    """Ext §4.3 place 8: `shorten sail` takes in each set sail under the bowsprit first, the
    outermost first (Lever 1808, l. 9962-9966, with the royals as it freshens), before the
    vocabulary's list; they are none of the courses or topsails, so the gale's reduction never
    reefs them. Not set, there is no line for them."""
    ship = _under_plain_sail(frigate_with_mizen_yard(), *SAILS)
    assert bowsprit_sail_lines(ship) == ["take in the sprit topsail", "take in the spritsail"]
    runner = _bare(ship, math.radians(-60.0))
    _kind, _words, data = orders.handle(ship, "shorten sail")
    started = [(o["data"]["evolutions"][0]["evolution"], o["order"]) for o in data["orders"]]
    assert started[:2] == [
        ("take_in_square", "take in the sprit topsail"),
        ("take_in_square", "take in the spritsail"),
    ]
    reefed = [o["order"] for o in data["orders"] if o["order"].startswith("reef")]
    assert reefed and not any("sprit" in line for line in reefed)
    _run(runner, ship)
    assert all(ship.sails[s].state is SailState.IN_THE_GEAR for s in SAILS)
    assert bowsprit_sail_lines(ship) == []
    gale = _under_plain_sail(frigate_with_mizen_yard(), *SAILS)
    for sid in ("fore.topsail", "main.topsail", "mizzen.topsail"):
        gale.sails[sid].reefs = 2
    lines = shorten_sail_lines(gale, 45.0)
    assert lines and not any("sprit" in line for line in lines)


# ---------------------------------------------------------------------------
# The spritsail's work (Ext §4.3): its evolutions, its pull large and by the wind, the polar
# ---------------------------------------------------------------------------


def test_each_sprit_sail_is_set_with_its_own_gear_and_worked_as_a_square_sail():
    """Ext §4.1, §4.3: the square sail's evolutions, unchanged. The spritsail hangs in slings
    and "has no halyard": set as a course is, loosed, sheeted home and its tack hauled aboard,
    no hoist; the sprit topsail's halyard works its traveller out, as a topsail yard is hoisted
    (Falconer 1780, SPRITSAIL-TOPSAIL). Each is reefed, shaken out, taken in and furled to its
    end; the spritsail's two reef bands are reefed as any square sail's (Plainly, Ext §4.4)."""
    ship = frigate_with_mizen_yard()
    runner = _bare(ship, math.radians(-150.0))
    assert ship.halyard_of("spritsail") is None and ship.halyard_of("sprit_topsail") is not None
    took = {}
    for sid in SAILS:
        assert ship.sails[sid].state is SailState.FURLED
        _kind, _words, data = orders.handle(ship, f"set the {sid.replace('_', ' ')}")
        assert [e["evolution"] for e in data["evolutions"]] == ["set_square"]
        took[sid], notes = _run(runner, ship)
        assert ship.sails[sid].state is SailState.SET
        assert notes[-1][2] == f"Set the {sid.replace('_', ' ')}."
    assert took == {"spritsail": 90 + 60 + 30, "sprit_topsail": 90 + 60 + 120}
    spritsail = ship.sails["spritsail"]
    assert spritsail.reef_bands == 2
    for text, state, reefs in (
        ("reef the spritsail, one reef", SailState.SET, 1),
        ("shake out the reefs in the spritsail", SailState.SET, 0),
        ("take in the spritsail", SailState.IN_THE_GEAR, 0),
        ("furl the spritsail", SailState.FURLED, 0),
    ):
        orders.handle(ship, text)
        _run(runner, ship)
        assert (spritsail.state, spritsail.reefs) == (state, reefs), text


@pytest.mark.parametrize(
    "text, want_deg",
    [
        ("brace the spritsail yard sharp up on the starboard tack", LIMIT_DEG),
        ("brace the sprit topsail yard sharp up on the starboard tack", LIMIT_DEG),
        ("brace the spritsail yard square", 0.0),
        ("brace sharp up on the larboard tack", -LIMIT_DEG),
    ],
)
def test_the_brace_orders_brace_them_within_their_limit(text, want_deg):
    """Ext §4.2, left as it is: `working_yards` keeps them, braced by name and by the orders that
    brace every yard, within their own limit (their braces lead to the fore stay and the fore
    top, Lavery I30). An order naming a group of the file ("square the yards", "the head
    yards") braces the yards the file lists in it, and the fixture lists them in none."""
    ship = _under_plain_sail(frigate_with_mizen_yard())
    runner = _bare(ship, math.radians(-60.0))
    if want_deg == 0.0:
        for y in YARDS:
            ship.spars[y].brace_angle = math.radians(20.0)
    _kind, _words, data = orders.handle(ship, text)
    braced = {e["subject"] for e in data["evolutions"] if e["evolution"] == "brace"}
    assert braced & set(YARDS)
    _run(runner, ship)
    for y in braced & set(YARDS):
        assert _deg(ship.spars[y].brace_angle) == pytest.approx(want_deg, abs=0.01), y


def test_set_large_their_thrust_is_ahead_and_by_the_wind_it_holds_her_back():
    """Ext §10.2: set at 150 degrees off in fifteen knots, the yards trimmed square as the polar
    trims them, each sail under the bowsprit pulls her ahead (the *Bellerophon* at the Nile,
    "setting her spritsail, wore clear": James vol. 2 p. 180). By the wind, sixty degrees off and
    braced to its limit, each holds her back (observed), as the period topped the yard and
    reefed the sail or took it in (Lever 1808, l. 7271-7274) and `shorten sail` does."""
    plain = list(frigate_with_mizen_yard().groups["plain sail"])
    large = _by_the_wind(*plain, *SAILS, off_deg=150.0)
    for sid in SAILS:
        assert large.sails[sid].thrust_kn > 0.3, sid
    close = _by_the_wind(*plain, *SAILS, off_deg=60.0)
    for sid in SAILS:
        assert close.sails[sid].thrust_kn < 0.0, sid
    assert {y: _deg(close.spars[y].brace_angle) for y in YARDS} == dict.fromkeys(YARDS, LIMIT_DEG)


def test_the_polar_never_sets_them_and_is_the_frigates_less_their_windage(tmp_path):
    """Ext §10.2: out of "plain sail" the polar never sets them (`_rigged_for_plain_sail`); her
    closest angle and her beat are the fixture's without them, and every speed of the table is
    within a tenth of a knot and a half of it (their furled sails' and yards' windage; measured
    at most 0.11 knots, at 30 degrees in 25 knots)."""
    with_them = polar_of(str(write_ship(frigate_with_mizen_yard_doc(), tmp_path, "with")))
    doc = frigate_with_mizen_yard_doc()
    doc["spars"] = [s for s in doc["spars"] if s["id"] not in SPRIT]
    doc["sails"] = [s for s in doc["sails"] if s["id"] not in SPRIT]
    doc["lines"] = [ln for ln in doc["lines"] if ln["of"] not in SPRIT]
    doc["groups"] = {
        g: [m for m in members if m not in SPRIT]
        for g, members in doc["groups"].items()
        if g != "spritsails"
    }
    without = polar_of(str(write_ship(doc, tmp_path, "without")))
    assert with_them.closest_deg == without.closest_deg
    assert with_them.beat_deg(15.0) == without.beat_deg(15.0)
    for row, other in zip(with_them.speeds_kn, without.speeds_kn, strict=True):
        assert row == pytest.approx(other, abs=0.15)
    assert not set(SAILS) & set(frigate_with_mizen_yard().groups["plain sail"])


# ---------------------------------------------------------------------------
# Nothing of the eight files moves (Ext §11)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", EIGHT)
def test_the_eight_files_read_the_places_as_before(name):
    """No part of the eight is under the bowsprit (`tests/test_rig_classing.py`, the probe; their
    classing is the golden table's), so each place reads as before the rule: `shorten sail` adds
    no first line, under all sail; the light sails clewed up hove to are the topgallants and
    royals forward of the backed yards, and no other; every spar's windage at its own station if
    it stands on the hull, else at its root's."""
    ship = load_ship(f"data/ships/{name}.yaml")
    for sid in ship.groups.get("all sail", []):
        ship.sails[sid].state = SailState.SET
    assert not any(ship.under_bowsprit(pid) for pid in ship.parts)
    assert bowsprit_sail_lines(ship) == []
    backed = scripts.yards_to_back(ship)
    for sl in scripts.light_sails_forward_of(ship, backed):
        assert ship.parent_of(ship.yard_of(sl)).cls in ("topgallant_mast", "royal_mast"), sl.id
    clr = ship.hull.spec.clr_x_m
    for spar, _height, lever in _spar_places(ship):
        root = spar if spar.parent is None else ship.mast_of(spar)
        assert lever == pytest.approx(root.x_m - clr), spar.id
