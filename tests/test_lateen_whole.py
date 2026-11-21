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
from rig_fixtures import polacre_probe_doc, write_ship, xebec_probe_doc

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.orders import navigation
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from freesail.world import captains as C

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


@pytest.fixture(scope="module")
def polacre(tmp_path_factory) -> bytes:
    """The polacre probe settled: a whole lateen on her fore and her mizen, a square main."""
    return _settle(write_ship(_dipping(polacre_probe_doc()), tmp_path_factory.mktemp("p"), "pol"))


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


def test_a_tack_that_leaves_the_lateens_leaves_the_yards_on_the_old_side_against_their_masts(xebec):
    """Said "and leave the lateens" (A1b's clause), the tack does nothing to a whole lateen's yard,
    so after it every lateen hangs on the new weather side, against its mast. (A1a's test of the
    tack before its change was built, the order given the clause at A1b.)"""
    world = _from(xebec)
    ship = world.ship
    world.submit("tack ship and leave the lateens")
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
    world.submit("tack ship and leave the lateens")
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
    world.submit("tack ship and leave the lateens")
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
    world.submit("tack ship and leave the lateens")
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


# ---------------------------------------------------------------------------
# Going about with the yard's change (A1b)
# ---------------------------------------------------------------------------

SHIFT_ALL = (
    "Shift the mainsail and the foresail and the mizen: ease the parrels, cast off the runners, "
    "peak up the yards and pass the cars round."
)


def _sides(world, ids=XEBEC_LATEENS) -> dict[str, str | None]:
    return {sid: world.ship.sails[sid].lug_side for sid in ids}


def _texts(world, n0: int, kinds=("helm.order", "evolution.step", "ship.tacked", "ship.wore")):
    return [
        (e.tick - world.log.all()[n0].tick, e.kind, e.text)
        for e in _after(world, n0)
        if e.kind in kinds
    ]


def test_a_tack_shifts_every_lateen_in_stays_by_default_and_is_tacked_when_they_are_over(xebec):
    """The ship's practice by default, "shift" in stays (the owner's "preferred"): the log says so
    at helm's a-lee; once her head is through the wind and her head sheets drawn the three yards
    are peaked up and their cars passed round together (her company serves all three parties), each
    yard its length at 8.7 s a metre (the ruling) by the crew's factor, the shortest over first; she
    is tacked once the last is, every lateen to leeward of its mast, and the end says nothing of a
    mast. Measured, seed 7: the change begun at +44 s, the mizen over at +151, the foresail at +227,
    the mainsail at +248, tacked at +344 (her steady time)."""
    world = _from(xebec)
    n0 = len(world.log.all())
    world.submit("tack ship")
    world.run(600)
    lines = _texts(world, n0)
    assert lines[0][2] == (
        "Ready about. Helm's a-lee; ease off the head sheets; haul aft the mizen sheet; the "
        "lateens to be shifted in stays."
    )
    begun = [t for t, _, x in lines if x == SHIFT_ALL]
    over = [(t, x.split(";")[0]) for t, k, x in lines if x.endswith("leeward of the mast.")]
    tacked = [(t, x) for t, k, x in lines if k == "ship.tacked"]
    assert begun and [x for _, x in over] == [
        "Shifted the mizen",
        "Shifted the foresail",
        "Shifted the mainsail",
    ]
    assert begun[0] < over[0][0] and len(tacked) == 1 and tacked[0][0] >= over[-1][0]
    assert tacked[0][1] == "Tacked; full and by on the larboard tack, heading E by N (77°)."
    assert world.ship.dyn.tack == "larboard"
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, "starboard")
    main = world.ship.sails["main.lateen"]
    seconds = scripts.lateen_yard_m(world.ship, main) * scripts.LATEEN_CHANGE_S_PER_M
    assert over[-1][0] - begun[0] >= seconds  # never quicker than the yard's own seconds


@pytest.mark.parametrize(
    "order, left, end",
    [
        ("tack ship and leave the mizen", ["mizzen.lateen"], ", the mizen on the mast."),
        (
            "tack ship and leave the lateens on the mast",
            list(XEBEC_LATEENS),
            ", the lateens on their masts.",
        ),
        ("tack ship and change the lateens", [], "."),
        (
            "put her about and leave the lateens",
            list(XEBEC_LATEENS),
            ", the lateens on their masts.",
        ),
    ],
)
def test_the_orders_clause_says_which_lateens_are_left_and_the_end_says_where_they_lie(
    xebec, order, left, end
):
    """`tack ship`, `wear ship` and `put her about` take the clause after the order (Eng §2.3 item
    3): "and shift" ("and change") or "and leave", the lateens or one named, "on the mast" the
    words' own. A lateen left keeps its yard on the old side, against its mast on the new tack,
    and the tack's last line names it; the rest are shifted. `put her about` gives the clause to
    the tack it chooses."""
    world = _from(xebec)
    n0 = len(world.log.all())
    assert world.submit(order).kind == "order.accepted"
    world.run(600)
    sides = _sides(world)
    assert [sid for sid in XEBEC_LATEENS if sides[sid] == "larboard"] == left
    assert all(sides[sid] == "starboard" for sid in XEBEC_LATEENS if sid not in left)
    (tacked,) = [e.text for e in _after(world, n0) if e.kind == "ship.tacked"]
    assert tacked.endswith(f"heading E by N (77°){end}") or tacked.endswith(end), tacked
    if order.startswith("put her about"):
        assert [e.kind for e in _after(world, n0)].count("ship.put_about") == 1


def test_the_practice_is_ordered_answered_read_and_kept_with_her(xebec):
    """`leave the lateens in stays`, `shift the lateens in wearing`, "in going about" for both (the
    verb first and no comma: Eng §2.3 item 3), answered with the practice whole and read in the
    readings as a model at the conn reads them; kept on her as a plain dict of strings, which a
    checkpoint carries; the next tack reads it."""
    world = _from(xebec)
    reply = world.submit("leave the lateens in stays")
    assert reply.kind == "ship.lateen_practice"
    assert reply.text == "Her practice: the lateens left on the mast in stays, shifted in wearing."
    assert world.ship.extra[scripts.LATEEN_PRACTICE] == {"stays": "leave", "wearing": "shift"}
    assert world.readings.words("lateen_practice") == (
        "the lateens left on the mast in stays, shifted in wearing"
    )
    reply = world.submit("change the lateens in going about")
    assert reply.text == "Her practice: the lateens shifted in stays and in wearing."
    reply = world.submit("leave the lateens on the mast in going about")
    assert reply.text == "Her practice: the lateens left on the mast in stays and in wearing."
    reply = world.submit("shift the lateens in wearing")
    assert reply.text == "Her practice: the lateens left on the mast in stays, shifted in wearing."
    again = _from(replay.checkpoint_bytes(world))
    assert scripts.lateen_practice(again.ship) == {"stays": "leave", "wearing": "shift"}
    n0 = len(again.log.all())
    again.submit("tack ship")
    again.run(600)
    assert _sides(again) == dict.fromkeys(XEBEC_LATEENS, "larboard")
    (ready,) = [e.text for e in _after(again, n0) if e.kind == "helm.order"][:1]
    assert ready.endswith("; the lateens left on their masts.")


def test_a_standing_order_sets_the_practice_as_any_order(xebec):
    """The plan's A1b, "a standing order sets it as any order": entered, its order read whole as
    the book reads it (`orders.read_whole`: "the lateens" is a mark of the practice and no part
    sought by that name, which a hull's file without the group would refuse), and given at the
    glass. Built first with "the lateens" as the order's object, the book refused it ("There is
    no such part as the the lateens in this ship")."""
    world = _from(xebec)
    reply = world.submit('standing order "lateens": every glass then leave the lateens in wearing')
    assert reply.kind == "standing.given", reply.text
    n0 = len(world.log.all())
    world.run(1900)
    assert scripts.lateen_practice(world.ship) == {"stays": "shift", "wearing": "leave"}
    said = [
        e.text for e in _after(world, n0) if e.kind in ("order.accepted", "ship.lateen_practice")
    ]
    assert "By standing order 'lateens': leaving the lateens in wearing." in said
    assert "Her practice: the lateens shifted in stays, left on the mast in wearing." in said


def test_a_practice_set_in_stays_before_the_change_is_the_one_the_tack_reads(xebec):
    """Given while a tack is in hand and before its change has begun (Eng §2.3 item 3), the
    practice set is the one that tack reads: the plan is read again as the change would begin."""
    world = _from(xebec)
    world.submit("tack ship")
    world.run(5)
    assert world.submit("leave the lateens in stays").kind == "ship.lateen_practice"
    world.run(600)
    assert world.ship.dyn.tack == "larboard"
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, "larboard")


@pytest.mark.parametrize(
    "order, said",
    [
        (
            "leave the lateens",
            "Leave the lateens when? Say 'leave the lateens in stays', 'in "
            "wearing' or 'in going about'; or, for one going about, 'tack ship and leave the "
            "lateens'.",
        ),
        (
            "leave the mizen in stays",
            "The practice is the lateens' together, not the mizen's: "
            "'leave the lateens in stays', 'shift the lateens in wearing'. To leave one in a "
            "single going about, say it after the order: 'tack ship and leave the mizen'.",
        ),
        (
            "leave the lateens in stays in wearing",
            "Two occasions were given; say one, or 'in going about' for both.",
        ),
        (
            "tack ship and leave the jib",
            "The jib is no whole lateen: a going about shifts round "
            "their masts, or leaves on them, the lateens alone (the fore lateen, the mizzen lateen "
            "or the main lateen).",
        ),
        (
            "tack ship and leave",
            "'and leave' what? Name the lateens after it: 'and leave the "
            "lateens', 'and shift the mizen'.",
        ),
        (
            "tack ship and shift the mizen and leave the mizen",
            "The order says both to shift and to leave the mizen; say one.",
        ),
        (
            "put her about and leave the jib",
            "The jib is no whole lateen: a going about shifts "
            "round their masts, or leaves on them, the lateens alone (the fore lateen, the mizzen "
            "lateen or the main lateen).",
        ),
    ],
)
def test_the_practice_and_the_clause_are_refused_in_their_own_words(xebec, order, said):
    """Each refused at once, and a `put her about` whose clause is refused says nothing of its
    choice."""
    world = _from(xebec)
    n0 = len(world.log.all())
    reply = world.submit(order)
    assert reply.kind == "order.rejected" and reply.text.endswith(said), reply.text
    assert not [e for e in _after(world, n0) if e.kind == "ship.put_about"]
    assert scripts.LATEEN_PRACTICE not in world.ship.extra


def test_a_hull_with_no_whole_lateen_answers_every_word_as_before():
    """On a hull with no whole lateen (the cutter) the clause is answered as it was (measured at
    the base, 00382c4: the same sentence, its hints included), `put her about` passes over the
    words after it as it always did, the practice's verb has nothing to set, and the reading says
    she has no whole lateen."""
    world = make_world(
        7,
        "data/ships/cutter.yaml",
        Scenario(wind_from_deg=0.0, wind_speed_kn=15.0, ship_heading_deg=292.5, ship_speed_kn=5.0),
    )
    reply = world.submit("tack ship and leave the lateens")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(
        "'tack ship' was understood, but not 'and leave the lateens'; did you mean 'hand', 'leave "
        "the pumps', 'either' or 'the lanterns'? (Punctuation and 'the' are ignored; the rest must "
        "be a part, a side, a heading or a modifier such as 'sharp up', 'one reef' or 'a fathom'.)"
    )
    reply = world.submit("leave the mainsail")
    assert reply.kind == "order.rejected"
    assert reply.text.endswith(
        "She carries no whole lateen; 'leave' is said of a lateen's yard in going about, left on "
        "the mast."
    )
    reply = world.submit("leave the mainsail in stays")  # the occasion is no word of hers
    assert reply.kind == "order.rejected" and "but not 'stays'" in reply.text, reply.text
    assert world.readings.words("lateen_practice") == "no whole lateen aboard"
    assert world.readings.value("lateen_practice") is None
    assert scripts.LATEEN_PRACTICE not in world.ship.extra
    assert world.submit("put her about and leave the lateens").kind == "order.accepted"


def test_a_wear_shifts_the_lateens_with_the_wind_aft_and_wears_when_they_are_over(xebec):
    """In the wear at its own point, "wind aft" (the settee's is lowered at "up helm"): the
    aftermost lateen eased at "up helm" and the log saying which are to be shifted; the three
    begun together as the wind comes aft; she is worn once the last is over. Measured: wind aft
    and the change begun at +55 s, the mainsail over at +258, worn at +309."""
    world = _from(xebec)
    n0 = len(world.log.all())
    world.submit("wear ship")
    world.run(600)
    lines = _texts(world, n0)
    assert lines[0][2] == (
        "Stand by to wear ship. Up helm; ease off the mizen sheet; the lateens to be shifted with "
        "the wind aft."
    )
    aft = [t for t, _, x in lines if x.startswith("Wind aft")]
    begun = [t for t, _, x in lines if x == SHIFT_ALL]
    over = [t for t, _, x in lines if x.endswith("leeward of the mast.")]
    worn = [(t, x) for t, k, x in lines if k == "ship.wore"]
    assert aft and begun == aft[:1] and len(over) == 3 and worn and worn[0][0] >= over[-1]
    assert worn[0][1] == "Wore ship; full and by on the larboard tack, heading ENE (68°)."
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, "starboard")


@pytest.mark.parametrize("have, together", [(None, True), (60, True), (12, False)])
def test_the_yards_are_shifted_together_where_the_hands_serve_all_else_the_main_first(
    xebec, monkeypatch, have, together
):
    """`LateenChange` (a plain class beside `SetteeChange`, built only when a lateen is to be
    changed): each yard's seconds its length at 8.7 a metre, its party one able hand for each 2½ m,
    at least four; together where the hands her company can give serve every party, the change
    done when the longest is; one after another, the main (the longest yard) first, each by its
    party's numbers term over the hands, where they do not."""
    world = _from(xebec)
    ship = world.ship
    monkeypatch.setattr(scripts, "hands_to_give", lambda _ship: have)
    for sid in XEBEC_LATEENS:
        ship.sails[sid].lug_side = "starboard"
    change = scripts.LateenChange(ship, list(XEBEC_LATEENS), "larboard")
    yard = {sid: scripts.lateen_yard_m(ship, ship.sails[sid]) for sid in XEBEC_LATEENS}
    assert change.ids == sorted(XEBEC_LATEENS, key=lambda sid: -yard[sid])
    assert change.ids[0] == "main.lateen"
    said = change.begin(scripts.LATEEN_CHANGE_S_PER_M)
    parties = {sid: scripts.lateen_party(ship, ship.sails[sid]) for sid in XEBEC_LATEENS}
    assert sum(parties.values()) <= 60 and sum(parties.values()) > 12
    if together:
        assert said == SHIFT_ALL and change.active == change.ids and change.queue == []
        assert change.left_s() == pytest.approx(yard["main.lateen"] * 8.7)
    else:
        assert said.startswith("Shift the mainsail: ease the parrel,") and change.queue
        assert change.active == ["main.lateen"]
        assert change.left["main.lateen"] == pytest.approx(
            yard["main.lateen"] * 8.7 * max(1.0, parties["main.lateen"] / 12)
        )
        assert change.left_s() == pytest.approx(sum(change.left.values()))
    ticks = 0
    while not change.advance(1.0, 1.0) and ticks < 2000:
        ticks += 1
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, "larboard")
    assert all(ship.sails[sid].state is SailState.SET for sid in XEBEC_LATEENS)
    assert ticks + 1 == pytest.approx(math.ceil(change_seconds(yard, parties, have)), abs=2)


def change_seconds(yard, parties, have) -> float:
    if have is None or sum(parties.values()) <= have:
        return max(yard.values()) * 8.7
    return sum(yard[sid] * 8.7 * max(1.0, parties[sid] / have) for sid in yard)


def test_a_rig_of_lateens_alone_waits_past_its_timeout_for_her_head_to_pay_off(xebec):
    """The ruling (§2.3 item 5): a tack's end waits for her to pay off on a rig with a whole
    lateen set and no square sail. The bare xebec (her head sails furled) is not within ten
    degrees of full and by at the tack's own timeout (300 s steady): she is tacked when she is,
    31 s after it, and the line says nothing of her not having paid off. Measured, seed 7."""
    world = _from(xebec)
    for sail in world.ship.sails.values():
        if sail.cls == "jibheaded" and sail.is_set:
            sail.state = SailState.FURLED
    world.run(300)
    n0 = len(world.log.all())
    world.submit("tack ship")
    (inst,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "tack"]
    tack = inst.script
    for _ in range(900):
        world.tick()
        if any(e.kind == "ship.tacked" for e in world.log.all()[n0:]):
            break
    (tacked,) = [e.text for e in _after(world, n0) if e.kind == "ship.tacked"]
    assert tack._lateen_rig() and tack.t_steady > tack.timing_value("steady_timeout_s", 120.0)
    assert "paid off" not in tacked and tack.not_paid_off == ""


def test_at_fill_away_a_lateen_on_her_weather_side_is_shifted_first_as_she_lies(polacre):
    """Hove to with a lateen on her weather side (as a forced round can leave one), "fill away"
    shifts it first as she lies, the fill away holding it and counting it, and lets her fall off
    when it is over; one on her lee is let be."""
    world = _from(polacre)
    world.submit("heave to")
    world.run(400)
    assert world.ship.extra.get("hove_to") and world.ship.dyn.tack == "starboard"
    world.ship.sails["fore.lateen"].lug_side = "starboard"  # her weather side
    n0 = len(world.log.all())
    assert world.submit("fill away").kind == "order.accepted"
    world.tick()
    (inst,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "fill_away"]
    assert inst.script.lateen_change.ids == ["fore.lateen"]
    assert "fore.lateen" in inst.script.holds()
    world.run(600)
    lines = _texts(world, n0, ("evolution.step", "helm.order", "ship.filled_away"))
    texts = [x for _, _, x in lines]
    assert texts[:3] == [
        "Shift the foresail: ease the parrel, cast off the runners, peak up the yard and pass "
        "the car round.",
        "Shifted the foresail; it stands to leeward of the mast.",
        "Hauled aft the head sheets; kept the helm a-lee to let her fall off.",
    ]
    assert texts[-1] == "Filled away on the starboard tack; braced full and steering WNW (292°)."
    assert _sides(world, ("fore.lateen", "mizzen.lateen")) == dict.fromkeys(
        ("fore.lateen", "mizzen.lateen"), "larboard"
    )


def test_forced_round_hove_to_with_nothing_aback_the_watch_shifts_the_lateens(xebec):
    """The hove-to watch's forced round (Eng §2.3a, row 7; without it B3.3b's silent bad hand
    comes back): forced through the wind with nothing aback, hove to no longer, the watch calls
    all hands to shift the lateens lying on their masts, the main first, and the line says so;
    each is shifted in its turn, and at the end every lateen stands to leeward of its mast."""
    world = _from(xebec)
    world.submit("heave to")
    world.run(400)
    n0 = len(world.log.all())
    _shift_the_wind(world, -8.0)
    world.run(900)
    (filled,) = [e for e in _after(world, n0) if e.kind == "ship.filled"]
    assert filled.text.endswith(
        "The watch calls all hands to shift the mainsail, lying on its mast. The foresail and the "
        "mizen, lying on their masts, are to be shifted."
    )
    assert filled.data["lateens_shifted"] and filled.data["lateens_to_be_shifted"]
    assert world.ship.dyn.tack == "larboard"
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, "starboard")


@pytest.mark.parametrize(
    "order, end", [("box haul", "ship.box_hauled"), ("wear short round", "ship.wore")]
)
def test_box_hauled_or_worn_short_round_the_lateens_are_shifted_with_the_wind_aft(
    polacre, order, end
):
    """The box-haul and the wear short round shift the lateens as the wear does, with the wind aft
    (the practice in wearing), and end once they are over."""
    world = _from(polacre)
    n0 = len(world.log.all())
    assert world.submit(order).kind == "order.accepted"
    world.run(900)
    lines = _texts(world, n0, ("evolution.step", end))
    aft = [t for t, _, x in lines if x.startswith("Wind aft")]
    begun = [t for t, _, x in lines if x.startswith("Shift the foresail and the mizen:")]
    over = [t for t, _, x in lines if x.endswith("leeward of the mast.")]
    ended = [t for t, k, _ in lines if k == end]
    assert aft and begun == aft[:1] and len(over) == 2 and ended and ended[0] >= over[-1]
    assert world.ship.dyn.tack == "larboard"
    assert _sides(world, ("fore.lateen", "mizzen.lateen")) == dict.fromkeys(
        ("fore.lateen", "mizzen.lateen"), "starboard"
    )


def test_the_change_is_built_only_when_a_lateen_is_to_be_shifted(xebec):
    """`LateenChange` is a plain class built only when a lateen is to be shifted (Eng §2.3 item
    2), so that no checkpoint of the game's own holds one (truth 7-606's census, which admits
    neither it nor `SetteeChange`: a checkpoint taken while either is in hand is refused, as the
    settee's always was). A tack that leaves the lateens builds none, nor one of a ship with no
    whole lateen; its field the class's own default."""
    world = _from(xebec)
    world.submit("tack ship and leave the lateens")
    (inst,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "tack"]
    world.run(600)
    assert "lateen_change" not in vars(inst.script) and inst.script.lateen_change is None
    cutter = _from(_settle("data/ships/cutter.yaml"))
    assert cutter.submit("tack ship").kind == "order.accepted"
    (inst,) = [i for i in cutter.ship.extra["evolutions"].instances if i.evo.id == "tack"]
    cutter.run(300)
    assert not {"lateen_change", "lateen_plan", "mizen_eased", "not_paid_off"} & set(
        vars(inst.script)
    )
    with pytest.raises(replay.CheckpointRefused, match="LateenChange"):
        busy = _from(xebec)
        busy.submit("tack ship")
        busy.run(100)
        _from(replay.checkpoint_bytes(busy))  # refused as it is loaded


def test_the_reading_and_the_verb_are_named_in_the_going_about_chapter():
    """The practice's verb and its reading named in the primer's going-about chapter, for
    `tests/test_grammar_book.py`'s two primer tests (Eng §2.3 item 3)."""
    chapter = Path("docs/primer/05-going-about.md").read_text(encoding="utf-8")
    assert "`leave the lateens in stays`" in chapter and "`the lateen practice`" in chapter


# ---------------------------------------------------------------------------
# The rules captain and `put her about` (A1c)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def xebec_in_a_breeze(xebec_file) -> bytes:
    """The xebec probe settled as the rest, in a strong breeze of 25 kn."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=25.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, xebec_file, scenario)
    world.submit("set plain sail")
    for i in range(900):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    return replay.checkpoint_bytes(world)


def test_over_22_knots_put_her_about_wears_a_lateen_and_says_why(xebec_in_a_breeze, xebec):
    """Package 45's choice gains one reason to wear (Eng §2.3 item 6; the lead's ruling): a whole
    lateen set and the mean true wind over `LATEEN_TACK_KN`, a module constant beside
    `WEAR_WIND_KN`, read for every voice; said in Forfait's reason. In 15 kn she tacks."""
    assert navigation.LATEEN_TACK_KN == 22.0 < navigation.WEAR_WIND_KN
    world = _from(xebec_in_a_breeze)
    assert navigation.put_about_choice(world.ship) == (
        "wear ship",
        "the wind 25 knots: a lateen is not put in stays in a strong wind",
    )
    n0 = len(world.log.all())
    assert world.submit("put her about").kind == "order.accepted"
    world.run(2)
    (said,) = [e.text for e in _after(world, n0) if e.kind == "ship.put_about"]
    assert (
        said
        == "Put about: wearing, the wind 25 knots: a lateen is not put in stays in a strong wind."
    )
    assert [i.evo.id for i in world.ship.extra["evolutions"].instances] == ["wear"]
    assert navigation.put_about_choice(_from(xebec).ship)[0] == "tack ship"


def test_an_ordered_tack_over_22_knots_is_obeyed_and_warned_once(xebec_in_a_breeze, xebec):
    """`tack ship` is never turned into a wear: obeyed, and warned once in words, a note of the
    ship's (the lead's ruling). In 15 kn, or with no whole lateen set, no warning."""
    world = _from(xebec_in_a_breeze)
    n0 = len(world.log.all())
    assert world.submit("tack ship").kind == "order.accepted"
    world.run(120)
    assert [i.evo.id for i in world.ship.extra["evolutions"].instances] == ["tack"]
    warned = [e for e in _after(world, n0) if e.kind == "ship.tack_warned"]
    assert [e.text for e in warned] == [
        "The wind 25 knots: a lateen is not put in stays in a strong wind; she is put in stays as "
        "ordered."
    ]
    calm = _from(xebec)
    n1 = len(calm.log.all())
    calm.submit("tack ship")
    calm.run(2)
    assert not [e for e in _after(calm, n1) if e.kind == "ship.tack_warned"]


@pytest.mark.parametrize("order", ["steer 45", "steer north-east"])
def test_the_courses_judgement_wears_a_lateen_over_22_knots_across_the_eye(
    xebec_in_a_breeze, order
):
    """A course across the wind's eye comes to `judge_course`'s eye branch (the road of `steer`,
    `shape a course` and the captains' hourly leg): over 22 kn with a whole lateen set she is worn
    for it, in the choice's words (ruled)."""
    world = _from(xebec_in_a_breeze)
    reply = world.submit(order)
    assert "the wind 25 knots: a lateen is not put in stays in a strong wind, and she is worn " in (
        reply.text
    ), reply.text
    world.run(2)
    assert [i.evo.id for i in world.ship.extra["evolutions"].instances] == ["wear"]


def test_with_no_room_to_wear_the_courses_judgement_tacks_a_lateen_regardless(
    xebec_in_a_breeze, monkeypatch
):
    """Where there is no room to wear (`no_room_to_wear`), the course's judgement tacks her
    regardless, as `put_about_choice` does with the land to leeward (ruled), and says why."""
    world = _from(xebec_in_a_breeze)
    monkeypatch.setattr(navigation, "no_room_to_wear", lambda _s: "the land a mile under her lee")
    course = math.radians(45.0)
    judged = navigation.judge_course(world.ship, course, helm_order=False)
    assert judged.branch == "tack"
    assert judged.words.endswith(
        "lies too near the wind to be laid; the wind 25 knots, but there is no room to wear with "
        "the land a mile under her lee: she is put about and kept full and by on the larboard tack"
    ), judged.words


def _recording(world):
    """The rules captain of `world`, his orders recorded and not given."""
    cap = world.captain
    given: list[tuple[str, str]] = []

    def give(text: str, why: str = ""):
        given.append((text, why))
        return type("E", (), {"kind": "order.accepted", "data": {}})()

    cap.give = give
    return cap, given


def test_the_rules_captain_sets_the_practice_by_the_wind_once_at_each_crossing(xebec):
    """From his book with its defaults (`lateen_leave_kn`, 12 kn): `leave the lateens in stays` as
    the mean true wind falls under it and `shift the lateens in stays` as it rises over it, each
    once at the crossing and only where the practice differs, so that every tack by any road reads
    it; nothing on a hull with no whole lateen, and nothing kept there."""
    world = _from(xebec)
    cap, given = _recording(world)
    p = C.Perception.read(world)
    p.wind_kn = 15.0
    cap._lateen_work(p)
    assert given == []  # the practice "shift" already: nothing at the first reading
    p.wind_kn = 9.0
    cap._lateen_work(p)
    assert given == [("leave the lateens in stays", "the wind under 12 knots")]
    cap._lateen_work(p)
    assert len(given) == 1  # once, at the crossing
    scripts.set_lateen_practice(world.ship, "leave", ("stays",))
    p.wind_kn = 16.0
    cap._lateen_work(p)
    assert given[1] == ("shift the lateens in stays", "the wind over 12 knots")
    cutter = _from(_settle("data/ships/cutter.yaml"))
    other, said = _recording(cutter)
    q = C.Perception.read(cutter)
    q.wind_kn = 9.0
    other._lateen_work(q)
    assert said == [] and not {"lateen_light", "bad_hand_since"} & set(other._business)


def test_the_rules_captain_shifts_a_yard_after_a_board_on_the_bad_hand(xebec):
    """A board of `bad_hand_s` (1,800 s, his book's default) with yards left on the bad hand and
    no manoeuvre in hand: each shifted by its own order, its why the board's minutes; and at once
    as the wind rises over `lateen_leave_kn`."""
    world = _from(xebec)
    world.submit("tack ship and leave the lateens")
    world.run(600)
    assert scripts.lateens_on_their_masts(world.ship)
    saved = replay.checkpoint_bytes(world)
    cap, given = _recording(world)
    p = C.Perception.read(world)
    assert p.manoeuvre == "none"
    p.wind_kn = 15.0
    cap._lateen_work(p)
    p.tick += 1799
    cap._lateen_work(p)
    assert given == []
    p.tick += 1
    cap._lateen_work(p)
    assert sorted(given) == sorted(
        (f"shift the {name}", "30 minutes on the bad hand")
        for name in ("mainsail", "foresail", "mizen")
    )
    risen, said = _recording(_from(saved))
    q = C.Perception.read(risen.world)
    q.wind_kn = 9.0
    risen._lateen_work(q)
    q.wind_kn = 14.0
    risen._lateen_work(q)
    assert ("shift the mainsail", "the wind risen over 12 knots") in said


def test_the_rules_captain_shifts_a_lateen_the_bow_or_the_stern_left_on_its_mast(xebec):
    """After the wind has crossed the stern, or come round ahead through the bow (A1a's lines),
    he shifts each lateen the line named, as he dips a lug; the lugger's lugs the bow names are
    not his to dip here."""
    world = _from(xebec)
    n0 = len(world.log.all())
    _shift_the_wind(world, -8.0)
    world.run(240)
    events = _after(world, n0)
    assert [e.kind for e in events].count("sail.across_the_bow") == 1
    cap, given = _recording(world)
    cap._across_the_bow(events)
    assert given == [
        (f"shift the {name}", "the wind round ahead through the bow")
        for name in ("foresail", "mizen", "mainsail")
    ]
    stern = _from(xebec)
    n1 = len(stern.log.all())
    stern.submit("steer 135")
    stern.run(240)
    crossed = _after(stern, n1)
    cap, given = _recording(stern)
    cap._across_the_stern(crossed)
    assert [t for t, _ in given][:3] == [
        f"shift the {n}" for n in ("foresail", "mizen", "mainsail")
    ]
    lugger = _from(_settle("data/ships/lugger.yaml"))
    n2 = len(lugger.log.all())
    _shift_the_wind(lugger, -8.0)
    lugger.run(240)
    cap, given = _recording(lugger)
    cap._across_the_bow(_after(lugger, n2))
    assert given == []


@pytest.mark.parametrize("path", sorted(str(p) for p in Path("data/captains").glob("*.yaml")))
def test_the_rules_captains_lateen_keys_are_in_no_committed_book(path):
    """`lateen_leave_kn` and `bad_hand_s` are read with their defaults and written in no committed
    book (ruled): a key in one would move `tests/test_subtypes.py`'s pairs of books."""
    text = Path(path).read_text(encoding="utf-8")
    assert "lateen_leave_kn" not in text and "bad_hand_s" not in text
    assert (C.LATEEN_LEAVE_KN, C.BAD_HAND_S) == (12.0, 1800)
