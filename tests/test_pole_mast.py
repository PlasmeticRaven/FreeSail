"""Package 90, A6: the pole mast's quick handing ("amener en paquet").

A pole mast is the mast and topmast in one stick: a braced yard above its lowest hangs on the
lower mast itself, and no topmast stands on it (`Ship.is_pole_mast`, read from the parts as filed
with no key; A5's levels, `Ship.yard_level`). Its upper square sails are taken in by letting their
halyards go, the yard lowered onto the yard below and the sail clewed up there (`take_in_pole`),
and furled from the yard below (`furl_pole`); the topmast evolutions are refused in words naming
the pole. Times JUDGEMENT (docs/dev/TuningNotes.md, "Package 90, A5 and A6"). No reef of a pole
sail is built: the smack's topsail has no reef bands and no committed file reaches one.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from rig_fixtures import polacre_probe_doc, write_ship

from freesail.agents import tools
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions.registry import load_directory
from freesail.orders import verbs
from freesail.orders.vocabulary import load_vocabulary
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState

SHIP_FILES = sorted(Path("data/ships").glob("*.yaml"))


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_the_smacks_main_is_the_one_committed_pole(path):
    """Of the committed files the smack's main alone carries a braced yard above its lowest on the
    lower mast with no topmast (`data/ships/smack.yaml`: "No topmast to strike: the topsail yard
    crosses the mast's own head"), and her topsail alone is on one."""
    ship = load_ship(path)
    poles = [sp.id for sp in ship.spars.values() if sp.cls == "mast" and ship.is_pole_mast(sp)]
    on = [sl.id for sl in ship.sails.values() if ship.on_pole(sl)]
    assert (poles, on) == ((["main.mast"], ["topsail"]) if path.stem == "smack" else ([], []))


def test_a_pole_takes_its_topsail_in_by_the_pole_and_its_course_as_a_course(tmp_path):
    """The smack's pole main: its topsail routed to `take_in_pole` and `furl_pole`, the square
    sail below it, its course, to the square sail's own. The polacre probe as filed, its topsail
    yard on a topmast, has no pole; with that yard crossing the lower mast's head under the
    topmast it is a topsail by its level (A5), and still no pole, the topmast standing."""
    ship = load_ship("data/ships/smack.yaml")
    vocab = load_vocabulary()
    take_in, furl = vocab.evolutions["take in"], vocab.evolutions["furl"]
    course = next(sl for sl in ship.sails.values() if sl.cls == "square" and not ship.on_pole(sl))
    topsail = ship.sails["topsail"]
    assert ship.yard_level(ship.yard_of(course)) == 0
    assert take_in[verbs.evolution_key(topsail, take_in, ship=ship)] == "take_in_pole"
    assert furl[verbs.evolution_key(topsail, furl, ship=ship)] == "furl_pole"
    assert take_in[verbs.evolution_key(course, take_in, ship=ship)] == "take_in_square"
    assert furl[verbs.evolution_key(course, furl, ship=ship)] == "furl_square"
    probe = load_ship(write_ship(polacre_probe_doc(), tmp_path, "polacre"))
    assert not any(probe.is_pole_mast(sp) for sp in probe.spars.values() if sp.cls == "mast")
    doc = polacre_probe_doc()
    for s in doc["spars"]:
        if s["id"] == "main.topsail.yard":
            s["on"], s["height_m"] = "main.mast", 15.6
    moved = load_ship(write_ship(doc, tmp_path, "topsail-on-the-mast"))
    assert moved.yard_level("main.topsail.yard") == 1 and not moved.is_pole_mast("main.mast")


def _smack(knots: float = 15.0, topsail: bool = True):
    world = make_world(
        7,
        "data/ships/smack.yaml",
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=knots,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=292.5,
            ship_speed_kn=5.0,
        ),
    )
    world.submit("set plain sail")
    world.run(120)
    if topsail:
        world.submit("set the topsail")
    for i in range(900):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    world.run(300)
    return world


def _lines(world, n0: int) -> list[tuple[int, str]]:
    kinds = ("evolution.started", "evolution.step", "sail.taken_in", "sail.furled")
    out = [e for e in world.log.all()[n0:] if e.kind in kinds]
    return [(e.tick, e.text) for e in out if "topsail" in e.text]


@pytest.mark.parametrize(
    "order", ["take in the topsail", "lower the topsail", "clew up the topsail"]
)
def test_the_smacks_topsail_is_lowered_onto_the_yard_below_and_clewed_up_there(order):
    """Her halyards let go, the yard down on the yard below, the sail clewed up there in one step
    with no settling on a cap. Measured, seed 7, 15 kn: begun at +50 s (her watch at the sheets
    first) and in the gear at +138 s, 88 s, where the square sail's clew-up and settling took
    154 s. "lower" is a pole sail's word now; "haul up", a course's, is refused in her words."""
    world = _smack()
    n0 = len(world.log.all())
    assert world.submit(order).kind == "order.accepted"
    world.run(600)
    lines = _lines(world, n0)
    assert [x for _, x in lines] == [
        "Let go the topsail halyards; hands to the clewlines and buntlines.",
        "Lowered the topsail down onto the yard below and clewed it up there.",
        "Took in the topsail; lowered on the yard below, hanging in the gear.",
    ]
    assert lines[-1][0] - lines[0][0] == 88
    reply = _smack().submit("haul up the topsail")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(
        "A topsail or light sail on a pole mast is lowered, not hauled up; say 'lower the "
        "topsail' or 'take in the topsail'."
    )


def test_the_smacks_topsail_is_furled_from_the_yard_below():
    """Lowered and clewed up first, then the men lay out on the yard below and furl it: 300 s
    from its start, where the square sail's climb and furl aloft took 350 s (measured, seed 7)."""
    world = _smack()
    n0 = len(world.log.all())
    world.submit("furl the topsail")
    world.run(600)
    lines = _lines(world, n0)
    assert [x for _, x in lines] == [
        "Lay out on the yard below and furl the topsail.",
        "Lowered the topsail down onto the yard below and clewed it up there.",
        "Furled the topsail on the yard below.",
    ]
    assert lines[-1][0] - lines[0][0] == 300


@pytest.mark.parametrize(
    "order, what",
    [
        ("strike the topmasts", "topmasts to strike"),
        ("send down the topgallant masts", "topgallant masts to send down"),
        ("fid the topmast", "topmasts to fid"),
    ],
)
def test_the_topmast_evolutions_are_refused_in_words_naming_the_pole(order, what):
    world = make_world(7, "data/ships/smack.yaml", Scenario(wind_from_deg=0.0, wind_speed_kn=12.0))
    reply = world.submit(order)
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(
        f"She has no {what}; her masts are the main mast (a pole, the mast and topmast in one "
        "stick)."
    )


def test_the_two_evolutions_are_described_to_the_player_in_the_games_own_words():
    """The library serves an evolution's file notes (`tools._evolution_text`): the pole's two name
    no package, step or design document, only the ship's work and its sources."""
    evolutions = load_directory()
    for eid in ("take_in_pole", "furl_pole"):
        text = tools._evolution_text(evolutions[eid])
        assert "pole mast" in text
        for word in ("package", "Package", "A6", "Design", "docs/", "JUDGEMENT"):
            assert word not in text, (eid, word)
    assert "reef_pole" not in evolutions


def _brought_up_off_falmouth():
    """The harness's `shoal_anchor` start: off Falmouth in three fathoms and a half, 8 kn from
    225°, her head 335° at 2 kn, plain sail set, 60 s; then come to an anchor, 2,400 s."""
    world = make_world(
        7,
        "data/ships/smack.yaml",
        Scenario(
            wind_from_deg=225.0,
            wind_speed_kn=8.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=335.0,
            ship_speed_kn=2.0,
            start_time=datetime(1805, 6, 10, 10, 0),
            position={"lat_deg": 50.152, "lon_deg": -5.040},
            region="channel-west",
        ),
    )
    world.submit("set plain sail")
    world.run(60)
    world.submit("come to an anchor")
    world.run(2400)
    return world


def test_the_smack_gets_under_way_under_her_plain_sail_her_topsail_left_furled():
    """Nudge 39, ruling 3: getting under way makes her plain sail, so a topsail not of it is not
    loosed by the cast (`scripts._plain_sail_topsails`: by the plain sail, not by the vessel).
    The smack's topsail is set over her plain sail only at the player's word: through the cast it
    stays furled and she stands out under her mainsail and her jib, as at A1d. A5 and A6 as first
    built loosed it at +340 s of the order and set it at +600 s ("under the topsail and the
    mainsail and the jib"); every committed file's other topsails are of its plain sail."""
    world = _brought_up_off_falmouth()
    n0 = len(world.log.all())
    world.submit("get under way")
    seen = set()
    for _ in range(1500):
        world.tick()
        seen.add(world.ship.sails["topsail"].state)
    assert seen == {SailState.FURLED}
    under = [e.text for e in world.log.all()[n0:] if e.kind == "ship.under_way"]
    assert under == [
        "Under way on the starboard tack, under the mainsail and the jib; the best bower catted "
        "and fished; full and by."
    ]
