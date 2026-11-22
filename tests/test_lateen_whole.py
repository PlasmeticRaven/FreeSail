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
from rig_fixtures import (
    brig_with_settee_doc,
    polacre_probe_doc,
    tartane_probe_doc,
    write_ship,
    xebec_probe_doc,
)

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.physics.sails import against_the_mast, compute_sail_forces
from freesail.ship.loader import load_ship
from freesail.ship.parts import LineState, SailState
from freesail.standing.runtime import contrary

XEBEC_LATEENS = ("fore.lateen", "main.lateen", "mizzen.lateen")
# the trunk's answer to words that begin with no verb of hers (nudge 46, item 4)
NOT_HERS = (
    "is not an order this ship understands. An order begins with a verb such as set, take in, "
    "furl, reef, shake out, brace, trim or haul."
)


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


def test_a_rig_of_lateens_with_no_head_sail_nor_braced_yard_aboard_will_not_lie_to(xebec):
    """No head sail she can set and no braced yard aboard, her lateens set: refused in the
    xebec's words. A boat with no head sail is refused as before. (Nudge 46, item 3, the pin
    moved: with her jibs furled, as this test had it, she carries head sails and is told what is
    not set, `test_a_rig_of_lateens_with_a_head_sail_or_a_yard_not_set_is_told_what_is_not_set`;
    here they are blown out.)"""
    world = _from(xebec)
    for sail in world.ship.sails.values():
        if sail.cls == "jibheaded":
            sail.state = SailState.BLOWN_OUT
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
    words after it as it always did, the practice's verb is no order of hers (nudge 46, item 4,
    the two pins moved: "She carries no whole lateen; ..." and "but not 'stays'" before, the
    trunk's answer now), and the reading says she has no whole lateen."""
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
    for order in ("leave the mainsail", "leave the mainsail in stays"):
        reply = world.submit(order)
        assert reply.kind == "order.rejected"
        assert reply.text.endswith(f"'{order}' {NOT_HERS}"), reply.text
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
# The second pass (the lead's nudge 46): each mend at the door it was found at
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def tartane(tmp_path_factory) -> bytes:
    """The tartane probe settled: a whole lateen on her main under her square topsail, a small
    whole lateen on her mizen (a 7-m yard), her jibs."""
    return _settle(write_ship(_dipping(tartane_probe_doc()), tmp_path_factory.mktemp("t"), "tar"))


def _blow_out(ship, sail) -> None:
    sail.state = SailState.BLOWN_OUT


def _carry_away_the_yard(ship, sail) -> None:
    ship.yard_of(sail).wrecked = True


def _carry_away_the_mast(ship, sail) -> None:
    ship.mast_of(sail).wrecked = True


def _part_the_jeers(ship, sail) -> None:
    ship.halyard_of(sail).state = LineState.PARTED


def _part_its(cls: str):
    def part(ship, sail) -> None:
        (line,) = [ln for ln in ship.lines_of(sail) if ln.cls == cls]
        line.state = LineState.PARTED

    return part


# what befalls the main lateen while its yard is shifted; the line's reason; the sail as left
CASUALTIES = {
    "blown out": (
        _blow_out,
        "it blew out of the bolt-ropes while it was being shifted",
        SailState.BLOWN_OUT,
    ),
    "yard": (
        _carry_away_the_yard,
        "the main lateen yard was carried away while it was being shifted",
        SailState.IN_THE_GEAR,
    ),
    "mast": (
        _carry_away_the_mast,
        "the main mast was carried away while it was being shifted",
        SailState.IN_THE_GEAR,
    ),
    "jeers": (
        _part_the_jeers,
        "the main lateen yard jeers parted while it was being shifted; the yard came down and the "
        "sail hangs in its gear",
        SailState.IN_THE_GEAR,
    ),
    # nudge 48, item 2: before, each ended "Shifted the mainsail" set and drawing
    "sheet": (
        _part_its("sheet"),
        "the main lateen sheet parted while it was being shifted; the sail hangs in its gear, "
        "not set, till its sheet is rove afresh",
        SailState.IN_THE_GEAR,
    ),
    "tack": (
        _part_its("tack"),
        "the main lateen tack parted while it was being shifted; the sail hangs in its gear, not "
        "set, till its tack is rove afresh",
        SailState.IN_THE_GEAR,
    ),
}


@pytest.mark.parametrize("what", sorted(CASUALTIES))
def test_a_casualty_while_the_shift_by_itself_is_in_hand_ends_it_in_true_words(xebec, what):
    """Nudge 46, item 1: the sail blown out, its yard or mast carried away, or its jeers parted
    while `shift the mainsail` is in hand ends the work in its own words, the sail left as the
    casualty left it, on its old side. Before, each ended "Shifted the mainsail; it stands to
    leeward of the mast." with the sail set and drawing (`ChangeLateenScript.tick`)."""
    world = _from(xebec)
    ship = world.ship
    world.submit("tack ship and leave the lateens")
    world.run(300)
    main = ship.sails["main.lateen"]
    side = main.lug_side
    n0 = len(world.log.all())
    assert world.submit("shift the mainsail").kind == "order.accepted"
    world.run(60)
    assert main.state is SailState.IN_THE_GEAR
    befall, said, state = CASUALTIES[what]
    befall(ship, main)
    world.run(400)
    lines = [(e.kind, e.text) for e in _after(world, n0)]
    assert ("evolution.failed", f"Could not shift the mainsail: {said}.") in lines, lines
    assert not [x for k, x in lines if k == "sail.dipped"]
    assert main.state is state and main.lug_side == side
    assert not [i for i in ship.extra["evolutions"].instances if i.evo.id == "change_lateen"]


@pytest.mark.parametrize("what", ["blown out", "jeers", "sheet", "tack"])
def test_a_casualty_in_stays_lets_the_yard_be_as_it_left_it_and_says_so(xebec, what):
    """Nudge 46, item 1, in stays: the main lateen blown out or its jeers parted while the tack
    shifts the lateens is let be as the casualty left it, on its old side, and said; the others are
    shifted and she is tacked. Before, a parted halyard ended "Shifted the mainsail" and set."""
    world = _from(xebec)
    ship = world.ship
    main = ship.sails["main.lateen"]
    n0 = len(world.log.all())
    world.submit("tack ship")
    for _ in range(600):
        world.tick()
        if main.state is SailState.IN_THE_GEAR:
            break
    assert main.state is SailState.IN_THE_GEAR
    side = main.lug_side
    befall, said, state = CASUALTIES[what]
    befall(ship, main)
    world.run(600)
    lines = [(e.kind, e.text) for e in _after(world, n0)]
    texts = [x for _, x in lines]
    assert ("evolution.step", f"Could not shift the mainsail: {said}.") in lines, texts
    assert "Shifted the mainsail; it stands to leeward of the mast." not in texts
    assert "Shifted the foresail; it stands to leeward of the mast." in texts
    assert main.state is state and main.lug_side == side
    assert any(k == "ship.tacked" for k, _ in lines)


def _in_their_gear(world, order: str, ids) -> object:
    """The order given and run until each of `ids` is in its gear, its change begun; the
    manoeuvre's script."""
    ship = world.ship
    assert world.submit(order).kind == "order.accepted"
    for _ in range(1500):
        world.tick()
        if all(ship.sails[i].state is SailState.IN_THE_GEAR for i in ids):
            break
    world.run(5)
    assert all(ship.sails[i].state is SailState.IN_THE_GEAR for i in ids)
    runner = ship.extra["evolutions"]
    (inst,) = [i for i in runner.instances if i.script is not None and hasattr(i.script, "phase")]
    return inst.script


def _in_hand(world) -> list:
    """The `change_lateen` works in hand."""
    runner = world.ship.extra["evolutions"]
    return [i for i in runner.instances if i.evo.id == "change_lateen"]


@pytest.mark.parametrize(
    "order, doing",
    [("tack ship", "tacking ship"), ("wear ship", "wearing ship")],
)
def test_a_going_about_belayed_mid_change_finishes_each_yard_begun_and_says_so(xebec, order, doing):
    """Nudges 46 and 48, item 2 and item 1: hands do not walk away from a yard peaked half round
    its mast, and a yard begun is finished in its time. Belayed while the lateens are shifted, the
    manoeuvre ends; each yard whose change is begun goes on as work in hand, named in the belay's
    line, and is said when it is set on the side it was going. Before nudge 46: "Belayed tacking
    ship; the helm and the yards left as they stand at steady.", and three dead lateens; before
    nudge 48, "... shifted round to the starboard side." and all three set in one tick."""
    world = _from(xebec)
    ship = world.ship
    script = _in_their_gear(world, order, XEBEC_LATEENS)
    side = script.lateen_change.side
    n0 = len(world.log.all())
    reply = world.submit("belay that")
    assert reply.kind == "work.belayed"
    assert reply.text.startswith(f"Belayed {doing}; the helm and the yards left as they stand")
    assert reply.text.endswith(
        "; the mainsail and the foresail and the mizen, their change begun, still being shifted "
        f"round to the {side} side."
    ), reply.text
    (work,) = _in_hand(world)
    assert work.subject_id == "main.lateen" and set(XEBEC_LATEENS) <= work.holds
    assert all(ship.sails[i].state is SailState.IN_THE_GEAR for i in XEBEC_LATEENS)
    world.run(600)
    shifted = [e.text for e in _after(world, n0) if e.kind == "sail.dipped"]
    assert sorted(shifted) == sorted(
        f"Shifted the {n}; it stands to leeward of the mast."
        for n in ("mainsail", "foresail", "mizen")
    ), shifted
    assert not [e for e in _after(world, n0) if e.text.startswith("Shift the mainsail: ease")]
    assert _sides(world) == dict.fromkeys(XEBEC_LATEENS, side)
    assert all(ship.sails[i].state is SailState.SET for i in XEBEC_LATEENS)
    assert not _in_hand(world)


def test_belayed_with_yards_waiting_their_turn_those_are_left_on_their_masts_and_said(
    xebec, monkeypatch
):
    """Nudges 46 and 48: with too few hands for every yard at once (twelve, the main first), the
    main goes on in hand to the side it was going and the foresail and the mizen, not yet begun,
    are left set on their masts, each named."""
    world = _from(xebec)
    ship = world.ship
    monkeypatch.setattr(scripts, "hands_to_give", lambda _ship: 12)
    old = _sides(world)
    script = _in_their_gear(world, "tack ship", ("main.lateen",))
    change = script.lateen_change
    assert change.active == ["main.lateen"] and change.queue == ["fore.lateen", "mizzen.lateen"]
    reply = world.submit("belay that")
    assert reply.text.endswith(
        f"; the mainsail, its change begun, still being shifted round to the {change.side} side; "
        "the foresail and the mizen left on their masts, not yet shifted."
    ), reply.text
    assert _sides(world) == old
    assert ship.sails["main.lateen"].state is SailState.IN_THE_GEAR
    assert all(ship.sails[i].state is SailState.SET for i in ("fore.lateen", "mizzen.lateen"))
    world.run(600)
    assert _sides(world) == {**old, "main.lateen": change.side}
    assert all(ship.sails[i].state is SailState.SET for i in XEBEC_LATEENS)


@pytest.mark.parametrize("order", ["box haul", "fill away"])
def test_the_box_haul_and_the_fill_away_belayed_mid_change_finish_the_yards_alike(polacre, order):
    """Nudges 46 and 48, at the other manoeuvres the change is woven into: the box-haul (as the
    wear) and the fill away (a lateen on her weather side shifted as she lies; before nudge 46,
    "... the foresail in its gear, not yet shifted round the mast", and left so)."""
    world = _from(polacre)
    ship = world.ship
    ids = ("fore.lateen", "mizzen.lateen")
    if order == "fill away":
        world.submit("heave to")
        world.run(400)
        ship.sails["fore.lateen"].lug_side = "starboard"  # her weather side
        ids = ("fore.lateen",)
    script = _in_their_gear(world, order, ids)
    side = script.lateen_change.side
    reply = world.submit("belay that")
    names = "the foresail" if len(ids) == 1 else "the foresail and the mizen"
    its = "its" if len(ids) == 1 else "their"
    assert reply.text.endswith(
        f"; {names}, {its} change begun, still being shifted round to the {side} side."
    ), reply.text
    assert _in_hand(world)
    for _ in range(600):
        world.tick()
        if not _in_hand(world):
            break
    assert all(ship.sails[i].state is SailState.SET and ship.sails[i].lug_side == side for i in ids)


TIMED = {
    "xebec": XEBEC_LATEENS,
    "polacre": ("fore.lateen", "mizzen.lateen"),
    "tartane": ("main.lateen", "mizzen.lateen"),
}


def _drawing_on_the_new_hand(world, order: str, ids, belay: bool) -> int:
    """Seconds from the order until every one of `ids` is set and drawing on its new side; with
    `belay`, the order belayed as the change begins."""
    ship = world.ship
    old = {i: ship.sails[i].lug_side for i in ids}
    t0 = world.clock.tick
    assert world.submit(order).kind == "order.accepted"
    belayed = not belay
    for _ in range(2400):
        world.tick()
        if not belayed and any(ship.sails[i].state is SailState.IN_THE_GEAR for i in ids):
            assert world.submit("belay that").kind == "work.belayed"
            belayed = True
        sails = [ship.sails[i] for i in ids]
        if all(s.state is SailState.SET and s.lug_side != old[s.id] for s in sails):
            return world.clock.tick - t0
    raise AssertionError(f"{order}: not drawing on the new hand in 2,400 s")


@pytest.mark.parametrize(
    "probe, order",
    [
        ("xebec", "tack ship"),
        ("xebec", "wear ship"),
        ("tartane", "tack ship"),
        ("polacre", "tack ship"),
        ("polacre", "box haul"),
        ("polacre", "fill away"),
    ],
)
def test_a_belayed_going_about_is_never_sooner_on_the_new_hand_than_the_plain_one(
    xebec, polacre, tartane, probe, order
):
    """Nudge 48, item 1, the times pinned: a manoeuvre belayed as its change begins has its yards
    drawing on the new hand no sooner than the plain one, the yards begun finished in their time
    and at no lighter a rate than the manoeuvre's own (measured, seed 7: the xebec's tack 248 s
    beside 248; before, 44 s). Each probe settled as the rest; the fill away from hove to with a
    lateen on her weather side."""
    settled = {"xebec": xebec, "polacre": polacre, "tartane": tartane}[probe]
    ids = TIMED[probe]
    times = []
    for belay in (False, True):
        world = _from(settled)
        these = ids
        if order == "fill away":
            world.submit("heave to")
            world.run(400)
            world.ship.sails["fore.lateen"].lug_side = "starboard"
            these = ("fore.lateen",)
        times.append(_drawing_on_the_new_hand(world, order, these, belay))
    plain, belayed = times
    assert belayed >= plain, (plain, belayed)


def test_the_work_handed_on_is_no_sooner_where_its_own_hands_would_work_lighter(
    tartane, monkeypatch
):
    """Nudge 48, item 1, the rate pinned: the work a belay hands on is worked at no lighter a rate
    than the manoeuvre's own at the belay, so that a lighter factor of its own (made so here, the
    shift by itself's hands at half the tack's) never makes the yards draw sooner than the plain
    tack has them."""
    from freesail.evolutions.runner import Runner

    crew_factor = Runner._crew_factor

    def lighter(self, inst, aloft):
        factor = crew_factor(self, inst, aloft)
        return factor * 0.5 if inst.evo.id == "change_lateen" else factor

    monkeypatch.setattr(Runner, "_crew_factor", lighter)
    ids = TIMED["tartane"]
    plain = _drawing_on_the_new_hand(_from(tartane), "tack ship", ids, False)
    belayed = _drawing_on_the_new_hand(_from(tartane), "tack ship", ids, True)
    assert belayed >= plain, (plain, belayed)


def test_a_save_taken_while_the_work_handed_on_is_in_hand_loads_and_sails_on_the_same(xebec):
    """Nudge 48, item 1: the work a belay hands on is a `change_lateen` with plain fields, so a
    save taken while it is in hand loads (a save while the manoeuvre's change is in hand is refused,
    as the second pass had it), and sails on as the world it was taken from."""
    world = _from(xebec)
    _in_their_gear(world, "tack ship", XEBEC_LATEENS)
    world.submit("belay that")
    world.run(20)
    again = _from(replay.checkpoint_bytes(world))
    (work,) = _in_hand(again)
    assert sorted(work.script.handed) == sorted(XEBEC_LATEENS)
    world.run(300)
    again.run(300)
    assert _sides(world) == _sides(again)
    assert [world.ship.sails[i].state for i in XEBEC_LATEENS] == [
        again.ship.sails[i].state for i in XEBEC_LATEENS
    ]


def test_the_work_handed_on_is_a_shift_by_itself_and_is_belayed_as_one(xebec):
    """Nudge 48, item 1: the work a belay hands on is a shift by itself, and belayed in its turn
    it is left in its gear and said (the second pass's unsure 2, allowed as built)."""
    world = _from(xebec)
    _in_their_gear(world, "tack ship", XEBEC_LATEENS)
    world.submit("belay that")
    assert _in_hand(world)
    reply = world.submit("belay that")
    assert reply.kind == "work.belayed"
    assert reply.text.endswith(
        "the mainsail and the foresail and the mizen in their gear, their yards not yet shifted "
        "round their masts."
    ), reply.text
    assert not _in_hand(world)


def test_a_going_about_belayed_while_the_settee_is_lowered_says_it_is_on_deck(tmp_path):
    """Nudge 46, item 2's question of the settee: on the trunk, a tack belayed while the settee
    lies lowered on deck said "the helm and the yards left as they stand at steady" and nothing
    of it (the bilander's the same: docs/dev/TuningNotes.md, "Package 90, A1a and A1b's second
    pass"). The one cause mended: the belay names it, in the fill away's words, and leaves it
    lowered on deck, as before."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, write_ship(brig_with_settee_doc(), tmp_path, "settee"), scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    for i in range(2400):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    settee = next(sl for sl in world.ship.sails.values() if sl.settee)
    assert world.submit("tack ship").kind == "order.accepted"
    for _ in range(1500):
        world.tick()
        if settee.yard_lowered:
            break
    world.run(5)
    assert settee.yard_lowered and settee.state is SailState.IN_THE_GEAR
    reply = world.submit("belay that")
    assert reply.text.endswith("; the mainsail lowered on deck, not yet dipped."), reply.text
    assert settee.yard_lowered and settee.state is SailState.IN_THE_GEAR


def test_a_rig_of_lateens_with_a_head_sail_or_a_yard_not_set_is_told_what_is_not_set(
    xebec, tartane
):
    """Nudge 46, item 3: what she carries, the yards and the head sails alike (the lead's nudge
    43). With a head sail or a braced yard aboard and none set she is told what is not set, in the
    trunk's words; the lateens' words only where she carries neither. Pinned both ways on the
    probes: the xebec with her jibs furled, and with them blown out; the tartane with her jibs
    blown out and her topsail furled (a yard aboard, not set), and with its yard sent down. With
    the yards' check read of what is set, or dropped, the tartane's first case fails; with the
    head sails' read of what is set, the xebec's."""
    told = "No head sail is set to haul to windward, nor a topsail to lay aback."
    for probe, head, yard, said in (
        (xebec, SailState.FURLED, None, told),
        (xebec, SailState.BLOWN_OUT, None, scripts.LATEENS_WILL_NOT_LIE_TO),
        (tartane, SailState.BLOWN_OUT, "furled", told),
        (tartane, SailState.BLOWN_OUT, "sent down", scripts.LATEENS_WILL_NOT_LIE_TO),
    ):
        world = _from(probe)
        ship = world.ship
        for sail in ship.sails.values():
            if sail.cls == "jibheaded":
                sail.state = head
        if yard is not None:
            topsail = ship.sails["topsail"]
            topsail.state = SailState.FURLED
            if yard == "sent down":
                ship.yard_of(topsail).sent_down = True
        reply = world.submit("heave to")
        assert reply.kind == "order.rejected" and reply.text.endswith(said), (head, yard, reply)


@pytest.mark.parametrize("path", sorted(str(p) for p in Path("data/ships").glob("*.yaml")))
def test_leave_is_no_order_of_a_ship_with_no_whole_lateen_and_answers_as_before(path):
    """Nudge 46, item 4: `leave` is an order only in the practice's forms, and only on a hull with
    a whole lateen. On every committed ship "leave port", "leave the ship" and a bare "leave" are
    answered as at the trunk; before, "There is no such part as the  in this ship." (an empty
    name), "... as the ship in this ship." and "Leave what?"."""
    world = make_world(7, path, Scenario())
    for order in ("leave port", "leave the ship", "leave", "leave the lateens in stays"):
        reply = world.submit(order)
        assert reply.kind == "order.rejected"
        assert reply.text.endswith(f"'{order}' {NOT_HERS}"), reply.text
        assert "the  " not in reply.text
    # nor is it hinted: at 0d5d2c56 "leav port" was answered "did you mean 'leave'?"
    for order in ("leav port", "leaves"):
        assert world.submit(order).text.endswith(f"'{order}' {NOT_HERS}")
    reply = world.submit("leeve the mizen")
    assert "understands; did you mean 'reeve'? An order" in reply.text, reply.text


def test_leave_on_a_hull_with_a_whole_lateen_is_the_practices_alone(xebec):
    """Nudge 46, item 4, on the xebec probe: the practice's forms are hers, each answered in its
    own words; any other form of `leave` is answered as at the trunk, and none with an empty
    name."""
    world = _from(xebec)
    for order in ("leave port", "leave the ship", "leave", "leave the jib", "leave her"):
        reply = world.submit(order)
        assert reply.text.endswith(f"'{order}' {NOT_HERS}"), reply.text
    for order, said in (
        ("leave the lateens", "Leave the lateens when?"),
        ("leave the mizen in stays", "The practice is the lateens' together, not the mizen's"),
        ("leave the jib in stays", "The practice is the lateens' together, not the jib's"),
    ):
        reply = world.submit(order)
        assert reply.kind == "order.rejected" and said in reply.text, reply.text
        assert "the  " not in reply.text
    reply = world.submit("leave the lateens in stays")
    assert reply.kind == "ship.lateen_practice", reply.text


def test_the_standing_orders_contraries_move_on_no_ship_with_no_whole_lateen():
    """Nudge 46, item 5: the sail room's mark ("for" said after a canvas verb) tells a shift round
    the mast from a shift for a new sail, and only of a whole lateen. On the cutter, old beside
    new: "shift the jib" beside "shift the jib for a new one" (and "bend the jib" beside "bend the
    jib for a new one") is a repetition, as at the trunk; at 0d5d2c56 the mark had entered the
    manner and each was a contrary on the jib."""
    ship = make_world(7, "data/ships/cutter.yaml", Scenario()).ship
    for verb in ("shift", "bend"):
        for words in ("for a new one", "for a spare"):
            assert contrary(ship, f"{verb} the jib", f"{verb} the jib {words}") == ""
    assert contrary(ship, "shift the jib", "shift the jib for the heavy one") == "the jib"


def test_a_whole_lateens_shift_and_its_shift_for_a_new_one_stay_contrary(xebec):
    """Nudge 46, item 5, the other way: on the xebec probe "shift the mainsail" (round its mast)
    and "shift the mainsail for a new one" (the sail room's) are two works on one sail; the jib's
    two shifts are one, as on every ship."""
    ship = _from(xebec).ship
    assert contrary(ship, "shift the mainsail", "shift the mainsail for a new one") != ""
    assert contrary(ship, "shift the jib", "shift the jib for a new one") == ""


@pytest.mark.parametrize("path", sorted(str(p) for p in Path("data/ships").glob("*.yaml")))
def test_the_practices_row_is_in_no_sample_of_a_ship_with_no_whole_lateen(path):
    """Nudge 46, item 6: "no whole lateen aboard" was in every station's sample on all eighteen
    ships. The row is left out of the sample where she carries no whole lateen
    (`readings.idle_lateen_rows`, read by `action_readings.idle_rows`, the sample's own road); the
    readings tool keeps it on every ship, as every reading is named in the primer."""
    from freesail.agents import tools
    from freesail.agents.harness import Harness

    world = make_world(7, path, Scenario())
    assert "lateen_practice" not in Harness._sample_readings(world)
    assert tools.readings_words(world)["lateen_practice"] == "no whole lateen aboard"


def test_the_practices_row_is_in_the_sample_of_a_hull_with_a_whole_lateen(xebec):
    """Nudge 46, item 6, the other way: on the xebec probe the row rides in the sample."""
    from freesail.agents.harness import Harness

    world = _from(xebec)
    assert Harness._sample_readings(world)["lateen_practice"] == (
        "the lateens shifted in stays and in wearing"
    )


def test_a_tack_ended_before_she_paid_off_says_her_sternway_and_not_full_and_by(tartane):
    """Nudge 46, item 7: the bare tartane probe (her topsail and head sails furled at once, plain
    sail settled) tacked: the end, before she has paid off, says she is through the wind and how
    she lies, her sternway named. Measured, seed 7: "Tacked; through the wind on the larboard
    tack, heading NE by N (38°), but she has not paid off: she lies 38° off the wind with a knot
    of sternway." Before: "Tacked; full and by ... with no way of way.", going astern at more
    than a knot."""
    world = _from(tartane)
    for sail in world.ship.sails.values():
        if sail.cls != "lateen":
            sail.state = SailState.FURLED
    n0 = len(world.log.all())
    world.submit("tack ship")
    world.run(900)
    (tacked,) = [e.text for e in _after(world, n0) if e.kind == "ship.tacked"]
    assert tacked.startswith("Tacked; through the wind on the larboard tack, heading "), tacked
    assert "but she has not paid off: she lies " in tacked and "full and by" not in tacked
    assert tacked.endswith(" of sternway.") and "of way of way" not in tacked


def test_the_clause_names_a_lateen_not_set_and_the_lateens_are_all_she_carries(xebec):
    """Nudge 46, item 7: `tack ship and leave the mizen` with the mizen taken in says so, where
    the clause was dropped without a word; and the two shifted are named, "the lateens" being all
    she carries."""
    world = _from(xebec)
    world.submit("take in the mizen")
    world.run(400)
    assert world.ship.sails["mizzen.lateen"].state is SailState.IN_THE_GEAR
    n0 = len(world.log.all())
    assert world.submit("tack ship and leave the mizen").kind == "order.accepted"
    world.run(60)
    (alee,) = [e.text for e in _after(world, n0) if e.kind == "helm.order"][:1]
    assert alee.endswith(
        "; the foresail and the mainsail to be shifted in stays; the mizen is not set and is let "
        "be."
    ), alee


def test_a_whole_lateen_on_the_bad_hand_draws_two_thirds_of_its_cloth(xebec):
    """Nudge 46, item 8, the two-thirds pinned at the door it is met at: tacked with the lateens
    left, each lies on its mast to windward and draws with two-thirds of its cloth
    (`LUG_AGAINST_MAST_AREA`), against what the same sail draws with its yard to leeward."""
    world = _from(xebec)
    world.submit("tack ship and leave the lateens")
    world.run(600)
    ship = world.ship
    assert ship.dyn.tack == "larboard"
    for sid in XEBEC_LATEENS:
        sail = ship.sails[sid]
        lies = 1.0  # her lee is the starboard side on the larboard tack
        assert sail.lug_side == "larboard" and against_the_mast(sail, lies)
        compute_sail_forces(ship, world.wind)
        against = sail.area_effective_m2
        sail.lug_side = "starboard"
        try:
            compute_sail_forces(ship, world.wind)
            clear = sail.area_effective_m2
        finally:
            sail.lug_side = "larboard"
        assert clear > 0.0
        # the figure itself, two-thirds, and not the constant (nudge 48, item 6: made 0.9, the
        # constant's own pin passed)
        assert against == pytest.approx(2.0 / 3.0 * clear, rel=0.02), sid


def test_the_least_party_of_four_is_met_at_the_tartanes_mizen(tartane, monkeypatch):
    """Nudge 46, item 8, the least party pinned: the tartane's mizen yard is 7 m, so its party by
    the yard is three (2½ m a hand) and the least party, four, stands. Shifted by itself with two
    hands to give, it takes four over two of its 7 m at 14.6 s a metre: 204 s, by the weather."""
    world = _from(tartane)
    ship = world.ship
    mizen = ship.sails["mizzen.lateen"]
    assert scripts.lateen_yard_m(ship, mizen) == pytest.approx(7.0)
    assert scripts.lateen_party(ship, mizen) == scripts.LATEEN_LEAST_PARTY == 4
    monkeypatch.setattr(scripts, "hands_to_give", lambda _ship: 2)
    world.submit("tack ship and leave the lateens")
    world.run(400)
    assert world.submit("shift the mizen").kind == "order.accepted"
    (inst,) = [i for i in ship.extra["evolutions"].instances if i.evo.id == "change_lateen"]
    assert inst.script.left_s == pytest.approx(7.0 * scripts.LATEEN_SHIFT_ALONE_S_PER_M * 4 / 2)


# ---------------------------------------------------------------------------
# The third pass (the lead's nudge 48)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("how", ["carried away", "shot away"])
def test_a_mast_gone_while_the_yard_is_shifted_is_named_as_it_went(xebec, how):
    """Nudge 48, item 5: the mast carried away (by the strain's own road, which wrecks its yard
    with it) is said as the mast, and "shot away" where a shot did it; before, "the main lateen
    yard was carried away" whatever went. The yard alone, as the yard."""
    from freesail.physics import strain as ST

    for spar_id, said in (("main.mast", "the main mast"), ("main.lateen_yard", None)):
        world = _from(xebec)
        ship = world.ship
        world.submit("tack ship and leave the lateens")
        world.run(300)
        n0 = len(world.log.all())
        assert world.submit("shift the mainsail").kind == "order.accepted"
        world.run(60)
        ST._wreck_spar(ship, ST.strain_state(ship), ship.spars[spar_id], 0.0, how=how)
        world.run(60)
        name = said or "the main lateen yard"
        fails = [e.text for e in _after(world, n0) if e.kind == "evolution.failed"]
        assert fails == [
            f"Could not shift the mainsail: {name} was {how} while it was being shifted."
        ]


PLACES_BELOW = ("cabin", "gunroom", "hold", "masthead", "shore", "boat")


def _senses_at(world, place: str):
    from freesail.world import knowledge as K

    spot = ("ashore", "", "") if place == "shore" else ("aboard", world.ship.name, place)
    return K.Senses(K.senses_of_place(place), spot, "" if place == "shore" else place)


def _both_doors(world, senses, monkeypatch) -> tuple[str | None, str]:
    """The line of the rows not to be had, at the stations' door and the player's."""
    from freesail.agents.harness import Harness
    from freesail.api import queries
    from freesail.world import knowledge as K

    monkeypatch.setattr(K, "players_senses", lambda _world: senses)
    return Harness._readings_elsewhere(world, senses), queries.knowledge_block(world)["words"]


@pytest.mark.parametrize("path", sorted(str(p) for p in Path("data/ships").glob("*.yaml")))
def test_the_rows_not_to_be_had_are_counted_as_at_the_trunk_on_a_ship_with_no_lateen(
    path, monkeypatch
):
    """Nudge 48, item 3: "Not to be had ...: ... and 18 more" had become "19 more" on every ship,
    the practice's row counted though it is no row of hers. At both doors, the stations' and the
    player's, the line is the one drawn from the rows less hers (`knowledge.rows_elsewhere` given
    the world): the trunk's to the byte, measured old beside new on the eighteen (the session's
    scratch, `n46/r3.py`)."""
    from freesail.world import knowledge as K

    world = make_world(7, path, Scenario())
    for place in PLACES_BELOW:
        senses = _senses_at(world, place)
        rows = [r for r in K.rows_elsewhere(senses) if r.id != "lateen_practice"]
        want = K.elsewhere_words(rows, senses)
        assert K.rows_elsewhere(senses, world) == rows
        station, player = _both_doors(world, senses, monkeypatch)
        assert station == want and player == (want or ""), (place, station)


def test_the_rows_not_to_be_had_still_count_the_practice_where_she_carries_a_lateen(
    xebec, monkeypatch
):
    """Nudge 48, item 3, the other way: on the xebec probe the practice's row is hers, and is
    counted at both doors where it is not to be had (in the cabin, on deck's rows)."""
    from freesail.world import knowledge as K

    world = _from(xebec)
    senses = _senses_at(world, "cabin")
    rows = K.rows_elsewhere(senses, world)
    assert "lateen_practice" in {r.id for r in rows}
    station, player = _both_doors(world, senses, monkeypatch)
    assert station == player == K.elsewhere_words(rows, senses)


@pytest.mark.parametrize(
    "order, said",
    [
        (
            "leave in stays",
            "Leave what in stays? Her practice is said of the lateens together: "
            "'leave the lateens in stays'.",
        ),
        (
            "leave port in stays",
            "Leave what in stays? Her practice is said of the lateens "
            "together: 'leave the lateens in stays'.",
        ),
        (
            "shift in wearing",
            "Shift what in wearing? Her practice is said of the lateens "
            "together: 'shift the lateens in wearing'.",
        ),
    ],
)
def test_an_occasion_with_no_sail_named_is_asked_of_in_the_practices_words(xebec, order, said):
    """Nudge 48, item 4: on a hull with a whole lateen, an occasion said with no sail of hers
    before it is asked of, and nothing is named that is not there; before, "There is no such
    part as the in stays in this ship; did you mean the main staysail ..."."""
    reply = _from(xebec).submit(order)
    assert reply.kind == "order.rejected" and reply.text.endswith(said), reply.text
    assert "no such part" not in reply.text


@pytest.mark.parametrize(
    "order, clause, said",
    [
        ("tack ship and leave the mizen", "Ready about.", "; the mizen is not set and is let be."),
        (
            "tack ship and leave the lateens",
            "Ready about.",
            "; the lateens are not set and are let be.",
        ),
        (
            "wear ship and leave the mizen",
            "Stand by to wear ship.",
            "; the mizen is not set and is let be.",
        ),
    ],
)
def test_the_clause_is_said_with_every_lateen_taken_in(xebec, order, clause, said):
    """Nudge 48, item 5: with every whole lateen taken in, the clause's lateens are said, not set
    and let be; before, nothing was said of the clause."""
    world = _from(xebec)
    for sid in XEBEC_LATEENS:
        world.ship.sails[sid].state = SailState.FURLED
    n0 = len(world.log.all())
    assert world.submit(order).kind == "order.accepted"
    world.run(5)
    (first,) = [e.text for e in _after(world, n0) if e.kind == "helm.order"][:1]
    assert first.startswith(clause) and first.endswith(said), first


def _tacked(world, n0: int) -> str:
    (line,) = [e.text for e in _after(world, n0) if e.kind == "ship.tacked"]
    return line


def test_the_tacks_end_says_she_has_not_paid_off_on_any_hull_with_a_lateen(polacre):
    """Nudge 48, item 5: the end's line says what she is on any hull that carries a whole lateen.
    The polacre probe with her jibs furled ended "Tacked; braced up on the larboard tack, heading
    NE (40°)." forty-odd degrees off with sternway; now, measured, seed 7: "..., heading NE (46°),
    but she has not paid off: she lies 46° off the wind with a knot of sternway." Her fore lateen,
    eased and drawn with the head sheets, is named for them, and no jib is drawn that is furled."""
    world = _from(polacre)
    for sail in world.ship.sails.values():
        if sail.cls == "jibheaded":
            sail.state = SailState.FURLED
    n0 = len(world.log.all())
    world.submit("tack ship")
    world.run(900)
    tacked = _tacked(world, n0)
    assert tacked.startswith("Tacked; braced up on the larboard tack, heading ")
    assert ", but she has not paid off: she lies " in tacked and tacked.endswith(" of sternway.")
    texts = [e.text for e in _after(world, n0)]
    assert not [x for x in texts if "Draw jib" in x or "head sheets" in x], texts
    assert any("; ease off the foresail sheet;" in x for x in texts)
    assert any("Draw the foresail; trim aft its sheet." in x for x in texts)


def test_the_tacks_end_says_she_has_fallen_off_past_full_and_by(xebec):
    """Nudge 48, item 5: the xebec probe with her mizen furled ended "Tacked; full and by on the
    larboard tack, heading E (95°)." ninety-five degrees off; now, measured, seed 7: "Tacked;
    through the wind on the larboard tack, heading E (95°), but she has fallen off: she lies 95°
    off the wind with three knots of way."."""
    world = _from(xebec)
    world.ship.sails["mizzen.lateen"].state = SailState.FURLED
    n0 = len(world.log.all())
    world.submit("tack ship")
    world.run(900)
    tacked = _tacked(world, n0)
    assert tacked.startswith("Tacked; through the wind on the larboard tack, heading "), tacked
    assert ", but she has fallen off: she lies " in tacked and "full and by" not in tacked


def test_under_half_a_knot_either_way_she_has_no_way_on_her(xebec):
    """Nudge 48, item 6, pinned: the end's words with under half a knot of way or sternway say "no
    way on her" (turned back to "no way of way", every file passed before)."""
    world = _from(xebec)
    world.submit("tack ship")
    (inst,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "tack"]
    for u_kn, said in (
        (0.3, "with no way on her"),
        (-0.4, "with no way on her"),
        (1.2, "with a knot of way"),
        (-1.4, "with a knot of sternway"),
    ):
        world.ship.dyn.u = units.knots_to_ms(u_kn)
        words = inst.script._not_paid_off_words(world.wind)
        assert words.endswith(said) and "of way of way" not in words, (u_kn, words)


def test_the_luggers_lugs_at_a_belay_are_named_and_left_as_they_were():
    """Nudge 48, ruled on the second pass's unsure 4: the lugger's dipping lugs lowered when her
    tack or wear is belayed are named, words alone, and left in their gear as before (a third move
    on a committed ship, declared: "Belayed tacking ship; the helm and the yards left as they
    stand at helm down." before)."""
    settled = _settle("data/ships/lugger.yaml", seconds=2400)
    for order, doing in (("tack ship", "tacking ship"), ("wear ship", "wearing ship")):
        world = _from(settled)
        ship = world.ship
        lugs = [i for i, sl in ship.sails.items() if sl.cls == "lug" and sl.dipping]
        assert world.submit(order).kind == "order.accepted"
        for _ in range(1500):
            world.tick()
            if any(ship.sails[i].state is SailState.IN_THE_GEAR for i in lugs):
                break
        world.run(3)
        reply = world.submit("belay that")
        assert reply.text.startswith(f"Belayed {doing}; the helm and the yards left as they stand")
        assert reply.text.endswith("; the foresail and the mainsail lowered, not yet dipped."), (
            reply
        )
        world.run(120)
        assert all(ship.sails[i].state is SailState.IN_THE_GEAR for i in lugs)
