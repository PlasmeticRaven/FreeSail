"""Package 90, A1a and A1b: the whole lateen, its side and its going about.

A whole lateen (a sail of class `lateen` not cut at the mast, carrying `dipping`) keeps the side of
its mast its yard hangs on (`Sail.lug_side`), found once as it is first set; on the weather side it
lies against its mast and draws with the lug's two-thirds; its yard is shifted round the mast by
itself (`shift`, `change` or `dip`: `change_lateen`), peaked and never lowered; the watch says when
a gybe or a shift of wind through the bow has left it on its mast; and a rig of whole lateens with
no head sail and no braced yard will not lie to. No committed file carries one (the 64's and the
74's mizzen course are lateens cut at the mast and go about as a ship's mizen, every order of
theirs as before). docs/design/Design-Package90-Engine.md §2.3, §2.3a, §2.4.4; the lead's
rulings, docs/design/Plan-Package90.md §13.1; docs/dev/TuningNotes.md, "Package 90, A1a".

Each test enters by the door the behaviour is met at: a ship file loaded as the game loads it (the
probes of `tests/rig_fixtures.py`, written with `dipping` on each whole lateen) and an order given
as a player gives it, from a settle on the starboard tack (seed 7, 15 knots from the north, her head
292.5 degrees, plain sail trimmed).
"""

from __future__ import annotations

import io
import math
from pathlib import Path

import pytest
from rig_fixtures import write_ship, xebec_probe_doc

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState

XEBEC_LATEENS = ("fore.lateen", "main.lateen", "mizzen.lateen")


def _dipping(doc: dict) -> dict:
    """The document with `dipping: true` on each of its whole lateens (stage 0L's key)."""
    for s in doc["sails"]:
        if s.get("class") == "lateen" and not s.get("cut_at_mast"):
            s["dipping"] = True
    return doc


def _settle(path, heading: float = 292.5, seconds: int = 900) -> bytes:
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=5.0,
    )
    world = make_world(7, path, scenario)
    world.submit("set plain sail")
    for i in range(seconds):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    return replay.checkpoint_bytes(world)


def _from(settled: bytes):
    world = replay._Unpickler(io.BytesIO(settled)).load()
    replay._rebind(world)
    return world


def _after(world, n0: int) -> list:
    return [e for e in world.log.all()[n0:] if e.kind not in ("ship.leeway", "clock.bell")]


def _shift_the_wind(world, points: float) -> None:
    """The wind shifted `points` at a stroke (`tests/test_settee.py`'s, a squall's front)."""
    wind = world.wind
    wind.follow(units.wrap_2pi(wind.base_direction + points * units.POINT), wind.base_speed)
    world.scenario.wind_from_deg = math.degrees(wind.base_direction)


@pytest.fixture(scope="module")
def xebec_file(tmp_path_factory):
    return write_ship(_dipping(xebec_probe_doc()), tmp_path_factory.mktemp("xebec"), "xebec")


@pytest.fixture(scope="module")
def xebec(xebec_file) -> bytes:
    return _settle(xebec_file)


# ---------------------------------------------------------------------------
# The side (A1a)
# ---------------------------------------------------------------------------


def test_a_whole_lateen_is_set_on_the_lee_side_and_keeps_it_brailed_and_furled(xebec):
    """`set_lateen` finds a whole lateen's side once (its nought-second step), to leeward of the
    wind as she was settled on the starboard tack; brailed up and furled it keeps it, its yard
    aloft; set again after the wind has come to the other side, it is set where its yard hangs and
    the line says it lies on the mast."""
    world = _from(xebec)
    ship = world.ship
    assert {sid: ship.sails[sid].lug_side for sid in XEBEC_LATEENS} == dict.fromkeys(
        XEBEC_LATEENS, "larboard"
    )
    world.submit("take in the mainsail")
    world.run(120)
    main = ship.sails["main.lateen"]
    assert main.state is SailState.IN_THE_GEAR and main.lug_side == "larboard"
    world.submit("tack ship")
    world.run(300)
    assert ship.dyn.tack == "larboard"
    n0 = len(world.log.all())
    world.submit("set the mainsail")
    world.run(120)
    set_lines = [e.text for e in _after(world, n0) if e.kind == "sail.set"]
    assert set_lines == ["Set the mainsail; it lies on the mast."]
    assert main.lug_side == "larboard" and main.state is SailState.SET


def test_the_mizzen_course_of_a_ship_is_set_as_before_with_no_side():
    """The 74's mizzen course, a lateen cut at the mast: no `dipping`, no side, its set's line as
    it was."""
    ship = load_ship("data/ships/seventy-four.yaml")
    course = ship.sails["mizzen.course"]
    assert course.cls == "lateen" and course.cut_at_mast and not course.dipping
    assert not scripts.is_whole_lateen(course)


def test_a_tack_leaves_the_yards_on_the_old_side_against_their_masts(xebec):
    """A1a alone: the tack does nothing to a whole lateen's yard (its change is A1b's), so after it
    every lateen hangs on the new weather side, against its mast."""
    world = _from(xebec)
    ship = world.ship
    world.submit("tack ship")
    world.run(300)
    assert ship.dyn.tack == "larboard"
    lee = "starboard"
    assert all(ship.sails[sid].lug_side not in (None, lee) for sid in XEBEC_LATEENS)


# ---------------------------------------------------------------------------
# The shift by itself, and its routing (A1a)
# ---------------------------------------------------------------------------


def test_shift_the_mainsail_shifts_its_yard_round_the_mast_by_the_yards_length(xebec):
    """`shift the mainsail`, its yard 19 m: all hands called, its party eight able hands (one for
    each 2½ m, the lead's ruling), its seconds 19 m at the lugger's 14.6 a metre, about 277 s by
    the weather and the hands (her company of 121 more than its party, so no longer for it); the
    sail in its gear meanwhile, then set on the new lee with the line."""
    world = _from(xebec)
    ship = world.ship
    world.submit("tack ship")
    world.run(300)
    n0 = len(world.log.all())
    reply = world.submit("shift the mainsail")
    assert reply.kind == "order.accepted", reply.text
    runner = ship.extra["evolutions"]
    (inst,) = [i for i in runner.instances if i.evo.id == "change_lateen"]
    assert inst.subject_id == "main.lateen" and runner._want(inst).all_hands
    assert scripts.lateen_party(ship, ship.sails["main.lateen"]) == 8
    world.run(2)
    main = ship.sails["main.lateen"]
    assert main.state is SailState.IN_THE_GEAR
    world.run(600)
    lines = [(e.tick - n0, e.kind, e.text) for e in _after(world, n0)]
    started = [t for t, k, x in lines if x.startswith("Shift the mainsail: ease the parrel")]
    shifted = [t for t, k, x in lines if k == "sail.dipped"]
    assert started and shifted, lines
    assert any(x == "Shifted the mainsail; it stands to leeward of the mast." for _, _, x in lines)
    assert 19 * scripts.LATEEN_SHIFT_ALONE_S_PER_M <= shifted[0] - started[0] <= 600
    assert main.state is SailState.SET and main.lug_side == "starboard"


@pytest.mark.parametrize("order", ["dip the mizen", "change the mizen", "shift the mizen"])
def test_dip_and_change_shift_a_whole_lateen_as_shift_does(xebec, order):
    world = _from(xebec)
    world.submit("tack ship")
    world.run(300)
    reply = world.submit(order)
    assert reply.kind == "order.accepted", reply.text
    runner = world.ship.extra["evolutions"]
    assert [(i.evo.id, i.subject_id) for i in runner.instances] == [
        ("change_lateen", "mizzen.lateen")
    ]
    mizen = world.ship.sails["mizzen.lateen"]
    assert scripts.lateen_party(world.ship, mizen) == 4  # its 10-m yard: the least party


def test_shift_for_a_new_one_goes_to_the_sail_room_and_the_good_hand_is_refused(xebec):
    """Said "for" a sail, the sail room's (`shift_sail`, as every lateen's before: the probe's sail
    room is empty); a whole lateen to leeward of its mast is not shifted."""
    world = _from(xebec)
    for text in ("shift the mainsail for a new one", "shift the mainsail for a spare"):
        reply = world.submit(text)
        assert reply.kind == "order.rejected" and "no spare sail left" in reply.text, reply.text
    reply = world.submit("shift the mainsail")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith("The mainsail lies to leeward of its mast already.")


def test_a_whole_lateen_blown_out_has_no_yard_to_shift_round(xebec):
    world = _from(xebec)
    world.ship.sails["main.lateen"].state = SailState.BLOWN_OUT
    reply = world.submit("shift the mainsail")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(
        "The mainsail is blown out; there is no yard to shift round. Shift it for a new one."
    )


def test_the_mizzen_course_of_the_74_is_shifted_for_a_spare_and_not_dipped_as_before():
    """Every order of the committed ships as it was: `shift the mizen` on the 74 is the sail
    room's, and `dip the mizen` is refused in its old words."""
    world = make_world(7, "data/ships/seventy-four.yaml", Scenario())
    reply = world.submit("dip the mizen")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith("'dip' has no meaning for a lateen sail.")
    reply = world.submit("shift the mizen")
    assert reply.kind == "order.accepted", reply.text
    runner = world.ship.extra["evolutions"]
    assert [i.evo.id for i in runner.instances] == ["shift_sail"]


def test_the_shift_waits_for_a_manoeuvre_in_hand(xebec):
    """A manoeuvre holds the whole lateens from the order (`lateens_held`, as a settee is held),
    so the shift ordered meanwhile follows it."""
    world = _from(xebec)
    world.submit("tack ship")
    world.run(2)
    n0 = len(world.log.all())
    assert world.submit("shift the mainsail").kind == "order.accepted"
    runner = world.ship.extra["evolutions"]
    assert [(i.evo.id, i.waiting) for i in runner.instances] == [
        ("tack", False),
        ("change_lateen", True),
    ]
    world.run(600)
    lines = _after(world, n0)
    tacked = [e.tick for e in lines if e.kind == "ship.tacked"]
    begun = [e.tick for e in lines if e.text.startswith("Shift the mainsail: ease the parrel")]
    assert tacked and begun and tacked[0] <= begun[0], [e.text for e in lines]


# ---------------------------------------------------------------------------
# The watch: the stern and the bow (A1a)
# ---------------------------------------------------------------------------


def test_the_stern_watch_says_a_lateen_left_on_its_mast_by_a_gybe(xebec):
    world = _from(xebec)
    n0 = len(world.log.all())
    world.submit("steer 135")  # across the wind by the stern: she gybes by the helm
    world.run(240)
    said = [e for e in _after(world, n0) if e.kind == "sail.across_the_stern"]
    assert [e.text for e in said] == [
        "The wind has come across the stern to the larboard quarter: the foresail and the mizen "
        "and the mainsail lie on their masts; shift them when you will."
    ]
    assert said[0].data["lateens"] == ["fore.lateen", "mizzen.lateen", "main.lateen"]


def test_the_bow_watch_says_a_lateen_left_on_its_mast_by_a_shift_of_wind_through_the_bow(xebec):
    """A shift of wind through her bow outside a manoeuvre: one line, once, a point past dead
    ahead (the stern watch heard only a gybe)."""
    world = _from(xebec)
    n0 = len(world.log.all())
    _shift_the_wind(world, -8.0)
    world.run(240)
    said = [e for e in _after(world, n0) if e.kind == "sail.across_the_bow"]
    assert [e.text for e in said] == [
        "The wind has come round ahead to the larboard bow: the foresail and the mizen and the "
        "mainsail lie on their masts; shift them when you will."
    ]


def test_the_bow_watch_says_a_luggers_lugs_left_on_their_masts_at_the_same_cause():
    """Mended at its cause (the card names it): the lugger's dipping lugs, left on their masts by a
    shift of wind through her bow, are said as the stern watch says them after a gybe. The
    bilander's settee, which the box-off changes, is not said by the bow."""
    lugger = _from(_settle("data/ships/lugger.yaml"))
    n0 = len(lugger.log.all())
    _shift_the_wind(lugger, -8.0)
    lugger.run(240)
    assert [e.text for e in _after(lugger, n0) if e.kind == "sail.across_the_bow"] == [
        "The wind has come round ahead to the larboard bow: the foresail and the mainsail are "
        "against their masts; dip them when you will."
    ]
    bilander = _from(_settle("data/ships/bilander.yaml"))
    _shift_the_wind(bilander, -8.0)
    bilander.run(240)
    assert not [e for e in bilander.log.all() if e.kind == "sail.across_the_bow"]


def test_the_bow_watch_says_nothing_in_a_tack_nor_of_a_ship_with_no_lateen_or_lug(xebec):
    world = _from(xebec)
    n0 = len(world.log.all())
    world.submit("tack ship")
    world.run(300)
    assert not [e for e in _after(world, n0) if e.kind == "sail.across_the_bow"]
    brig = make_world(
        7,
        "data/ships/brig.yaml",
        Scenario(wind_from_deg=0.0, wind_speed_kn=15.0, ship_heading_deg=292.5),
    )
    brig.submit("set plain sail")
    brig.run(300)
    _shift_the_wind(brig, -8.0)
    brig.run(120)
    assert not [e for e in brig.log.all() if e.kind == "sail.across_the_bow"]


# ---------------------------------------------------------------------------
# Hove to (A1a)
# ---------------------------------------------------------------------------


def test_a_rig_of_lateens_with_no_head_sail_set_will_not_lie_to(xebec):
    """No head sail set and no braced yard, her lateens set: refused in the xebec's words. A boat
    with no head sail is refused as before."""
    world = _from(xebec)
    for sail in world.ship.sails.values():
        if sail.cls == "jibheaded":
            sail.state = SailState.FURLED
    reply = world.submit("heave to")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(scripts.LATEENS_WILL_NOT_LIE_TO)
    boat = make_world(7, "data/ships/boat-launch-31.yaml", Scenario())
    reply = boat.submit("heave to")
    assert reply.text.endswith(
        "No head sail is set to haul to windward, nor a topsail to lay aback."
    )


@pytest.mark.parametrize("path", sorted(str(p) for p in Path("data/ships").glob("*.yaml")))
def test_no_whole_lateen_is_ever_a_driver_hove_to(path):
    """The driver rule (`after_gaff_sails`) never takes a whole lateen, every sail set: a lateen
    mizen is kept set hove to (Design-Package90-Engine.md §2.3 item 5). Over every committed file
    as filed (none carries one) and as each would be with every lateen not cut at the mast whole."""
    for ship in (load_ship(path), _keyed(path)):
        for sail in ship.sails.values():
            sail.state = SailState.SET
        assert not [s.id for s in scripts.after_gaff_sails(ship) if scripts.is_whole_lateen(s)]


def test_the_xebec_probes_lateen_mizen_is_no_driver(xebec_file):
    ship = load_ship(xebec_file)
    for sail in ship.sails.values():
        sail.state = SailState.SET
    assert [s.id for s in ship.sails.values() if scripts.is_whole_lateen(s)] == list(
        (*XEBEC_LATEENS[:1], "mizzen.lateen", "main.lateen")
    )
    assert scripts.after_gaff_sails(ship) == []


def _keyed(path: str):
    """The committed file loaded, every lateen of it not cut at the mast given `dipping` in the
    loaded parts (none is: the 64's and the 74's are cut at the mast)."""
    ship = load_ship(path)
    for sail in ship.sails.values():
        if sail.cls == "lateen" and not sail.cut_at_mast:
            sail.dipping = True
    return ship


def test_a_small_company_takes_the_longer_for_a_party_she_cannot_give():
    """The party's numbers term (`scripts.party_term`): the party over the hands her company can
    give (the posts at the conn never counted), never less than 1, as the crew's own rule has it.
    The bilander's company (nine aboard, her master and mate at the conn) against the tartane's
    ten for a 24-m main yard, and against the least party, four."""
    world = make_world(7, "data/ships/bilander.yaml", Scenario())
    have = scripts.hands_to_give(world.ship)
    assert have is not None and 0 < have < 10
    assert scripts.party_term(world.ship, 10) == pytest.approx(10 / have)
    assert scripts.party_term(world.ship, 4) == 1.0
    assert scripts.party_term(load_ship("data/ships/bilander.yaml"), 10) == 1.0  # no company
