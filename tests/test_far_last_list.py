"""The lead's last list for package 75 (2026-11-14, 14:05 UTC, nudge 12), the far fight's items 1 to
7, each tried at the level of its cause and then on the case the readers found. The owner's word of
2026-11-14 on mends for the cause, not the symptom, governs them: each test names the cause and
the readers it serves, and each fails on 20a8e2e3 (its old figures in its docstring).

- **An order with no mark never falls back to "any sail"** (item 1): the order's "her" is the
  nearest sail her captain holds an enemy and may fight (`orders.gunnery._enemy_to_engage`), the
  player's order and the rules captain's alike; with none such the order is refused in words.
- **One record of who has fired on whom** (item 2): `relations.fired`, by the ids of the sea, read
  by every judge of the ship fired on (`Judgement.fired_on`) and so by `MARK`, far as near; the far
  rounds write it and read it for their strike.
- **A change of hands ends every relation held on her** (item 3): `relations.changed_hands`.
- **`still` answers the supporter's side and the holder's being** (item 4).
- **The near battery's mark judged anew when she changes hands** (item 5).

Measured on the owner's machine (Windows 11, 2026-11-14) at seed 7; old is 20a8e2e3."""

from __future__ import annotations

import math

import pytest

from freesail import units
from freesail.combat import far as F
from freesail.combat import far_action as FA
from freesail.combat.guns import FireMode, battery_of
from freesail.world import crews
from freesail.world import prizes as P
from freesail.world import relations as R
from freesail.world import signals as S
from freesail.world.geo import destination
from tests.test_brains import FRIGATE, put, world_at
from tests.test_relations import _sea


def _at(p):
    return {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg}


def _taken_by_the_french(w, brig, east_nm: float = 0.2):
    """The brig struck to a French frigate put `east_nm` east of her and taken possession of, the
    frigate then gone from the sea (a far prize under a French prize crew)."""
    q = destination(brig.position, 90.0, east_nm * units.NAUTICAL_MILE)
    fr = put(w, "frigate", "france", _at(q), "bound for Brest", "bound for Brest", name="Renard")
    brig.struck = True
    P.possess(w, fr, brig, by="a test", said=False)
    fr.done = True
    return fr


# -- item 1: the order's "her" -------------------------------------------------------------------


def _a_friend_and_an_enemys_prize():
    """The lead's case: the player's frigate hove to at seed 7, a British brig-sloop a third of a
    mile east of her, and a British merchant brig taken by the French 0.6 miles south; the cap
    nought; two minutes for the tops to make them out, and the hands beat to quarters."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    e = destination(w.position, 90.0, 0.3 * units.NAUTICAL_MILE)
    sloop = put(
        w,
        "brig-sloop",
        "britain",
        _at(e),
        "cruising off the Lizard within 20 miles",
        intent="cruise off the Lizard within 20 miles",
        name="Cruizer",
    )
    s = destination(w.position, 180.0, 0.6 * units.NAUTICAL_MILE)
    brig = put(w, "merchant brig", "britain", _at(s), "bound for Falmouth", "bound for Falmouth")
    _taken_by_the_french(w, brig)
    w.run(120)
    w.submit("beat to quarters")
    w.run(30)
    return w, sloop, brig


def test_her_is_the_nearest_enemy_her_captain_may_fight_and_with_none_the_order_is_refused():
    """The cause: an order with no mark fell back to "any sail": "her" was the nearest enemy by her
    colours or her shot, and with none (the only enemy in sight a prize, whom the one answer does
    not let be fought) the first sail in sight, whoever she was. Mended where "her" is read, for
    the player's order and the rules captain's alike (`orders.gunnery._enemy_to_engage`): the
    nearest sail his captain holds an enemy (`Captain._is_enemy`) and may fight (`relations.MARK`);
    with none, the order is refused in words and no mark is laid. A French frigate put in sight is
    "her", past the friend nearer and the prize. Old (20a8e2e3): "Engage a brig-sloop of war to
    starboard ... the guns to fire as they bear", the British brig-sloop the mark."""
    w, sloop, brig = _a_friend_and_an_enemys_prize()
    items = w.lookout.strangers(w, float(w.ship.heading))["items"]
    assert [i["id"] for i in items] == [sloop.id, brig.id]
    assert items[1]["nation"] == "france" and P.is_prize(brig)
    battery = battery_of(w.ship)
    for actor in ("the player", "the captain"):
        if actor == "the player":
            r = w.submit("engage her to starboard")
        else:
            r = w.captain.give("engage her to starboard", why="a test")
        assert r.kind == "order.rejected", (actor, r.text)
        assert "There is no enemy in sight to engage" in r.text and "in sight:" in r.text
        assert battery.target is None and battery.mode is FireMode.HOLD
    west = destination(w.position, 270.0, 0.8 * units.NAUTICAL_MILE)
    foe = put(w, "frigate", "france", _at(west), "bound for Brest", "bound for Brest", name="Foe")
    w.run(120)
    r = w.submit("engage her to starboard")
    assert r.kind == "guns.engage" and battery.target == foe.id, r.text
    from freesail.orders.gunnery import _enemy_to_engage

    assert _enemy_to_engage(w, items) is None  # the rule's own answer for the first two


# -- item 2: one record of who has fired on whom --------------------------------------------------


def test_who_fired_on_whom_is_one_record_by_id_written_by_the_rounds_and_read_by_both_bodies():
    """The cause: who had fired on whom was kept in three places: each body's judge's own set (the
    far brain's, her hull's captain's), written by the near battery alone, and the far rounds' book
    of each pair by the ships' names, which no judge read; so that package 70's rule ("she fired on
    me: an enemy whatever her colours") was never true far off, and a ship's far brain and her
    hull's captain knew two things. Mended as one record (`relations.fired`, by the ids of the
    sea, on the sea's World): the far rounds write it each round a side fires, and read it for the
    strike "once fired on"; every judge of the ship fired on reads her row of it
    (`Judgement.fired_on`), so `MARK` holds the firer an enemy under any colours, far as near, and
    her hull's captain knows it at the promotion. Old (20a8e2e3): after the round neither brain
    knew the other had fired, the French 74 under British colours was no mark, and the hull's
    captain knew nothing."""
    w, us, foe, _mate = _sea()
    foe.position = destination(us.position, 90.0, 0.4 * units.NAUTICAL_MILE)
    foe.brain.state = "engaging"
    foe.brain._stranger = us.id
    FA.minute(w)
    assert us.damage.get("rounds") == 1 and foe.damage.get("rounds") == 1
    assert foe.id in us.brain.fired_on and us.id in foe.brain.fired_on
    assert R.has_fired(w, foe, us) and R.has_fired(w, us, foe)
    S.set_colours(S.vessel_locker(foe).colours, w.nations, "false", "britain", 0)
    assert R.still(w, us, foe, R.MARK)  # she fired on her: an enemy under any colours
    assert "fired_on" not in w.__dict__["_far_rounds"]["|".join(sorted((us.id, foe.id)))]
    hull = crews.promote(w, us)
    assert foe.id in hull.captain.fired_on and hull.captain._known_enemy({"id": foe.id})


def test_the_rounds_key_who_was_fired_on_by_the_side_never_by_a_shared_name():
    """The round's own record of who has been fired on (`far.round_once`'s `fired_on`) was keyed by
    the ships' names, which two ships may share (the far ship's name is her file's in the measure,
    her own on the sea): two frigates of one file, one with no guns, each under her line from the
    first round, and the one never fired on struck. Now each side is keyed by her id, or her place
    in the round where she has none: the one fired on strikes, and the other cannot. Old
    (20a8e2e3): the frigate never fired on struck at 180 seconds."""
    from freesail.core.rng import Rng

    a = F.far_ship(FRIGATE, "britain", strike_below=1.1)
    b = F.far_ship(FRIGATE, "france", strike_below=1.1)
    assert a.name == b.name
    b.guns = []
    fired_on: dict[str, bool] = {}
    r = F.round_once(a, b, 400.0, Rng(7).stream("far"), 180.0, fired_on)
    assert r.fired[0] > 0 and r.fired[1] == 0
    assert a.struck_at_s is None and b.struck_at_s == 180.0
    assert fired_on == {"a": False, "b": True}
    a.id, b.id = "ship-1", "ship-2"
    a.struck_at_s = b.struck_at_s = None
    fired_on = {}
    F.round_once(a, b, 400.0, Rng(7).stream("far"), 180.0, fired_on)
    assert fired_on == {"ship-1": False, "ship-2": True}


@pytest.mark.slow
def test_an_enemy_under_false_colours_in_a_far_fight_is_still_fought_by_the_ship_she_fires_into():
    """The case caught: truth 7-231's pair (`tests/test_far_action.py`, `_two_on_passage`), the
    Foudroyant hoisting British colours at 600 mid-engagement: the Hero, fired into every round,
    held her no mark by her colours, gave up the action at 1260 and struck at 1380 "on passage",
    fought still. Now the Hero engages her to the end, as truth 7-231's pair does under their own
    colours: struck at 1200 while `engaging`, the Foudroyant on passage at 1320. Old (20a8e2e3):
    the Hero `on passage` at 1260 and struck at 1380."""
    from tests.test_far_action import _two_on_passage

    w, a, b = _two_on_passage()
    w.run(540)
    assert w.clock.tick == 600 and a.brain.state == b.brain.state == "engaging"
    S.set_colours(S.vessel_locker(a).colours, w.nations, "false", "britain", 600)
    for _ in range(15):
        w.run(60)
    states = [s for t, s in b.brain.history if t > 600]
    assert "on passage" not in states[: states.index("struck")], b.brain.history
    assert (1200, "struck") in b.brain.history
    assert (1320, "on passage") in a.brain.history


# -- item 3: a change of hands ends every relation held on her -----------------------------------


def test_a_change_of_hands_ends_every_relation_held_on_her():
    """The cause: a relation held after what it stood on is gone. Of the relations held on a ship
    that changes hands, `relations.changed_hands` forgot what was known of her shot, the signal and
    the hail, and kept the rest: the sails spoken and the chases given up (`spoken_ids`,
    `given_up`, read raw by `Judgement._spoken`), the player's having spoken her (`Vessel.spoken`),
    the orders she sailed under and the orders of the ships under hers (`under_orders_of`), the far
    rounds' book of her pairs. Mended there, the one road of every change of hands: every judge on
    the sea forgets that he spoke her or gave her up, her own judges every ship they spoke or gave
    up; her orders and her inferiors' end (she is under her captor's, by his company's book); the
    book of her pairs goes, another pair's stays. Old (20a8e2e3): every one of them held but her
    own orders, which her captor's company rewrote."""
    w, us, foe, mate = _sea()
    us.brain.spoken_ids.add(mate.id)
    us.brain.given_up.add(mate.id)
    foe.brain.given_up.add(mate.id)
    mate.brain.spoken_ids.add(us.id)
    mate.brain.given_up.add(foe.id)
    mate.spoken = True
    mate.under_orders_of = us.id
    west = destination(mate.position, 270.0, 0.5 * units.NAUTICAL_MILE)
    cutter = put(w, "cutter", "britain", _at(west), "bound for Falmouth", "bound for Falmouth")
    cutter.under_orders_of = mate.id
    book = w.__dict__.setdefault("_far_rounds", {})
    book["|".join(sorted((foe.id, mate.id)))] = {"last": 0, "since": 0}
    book["|".join(sorted((foe.id, us.id)))] = {"last": 0, "since": 0}
    mate.struck = True
    P.possess(w, foe, mate, by="a test", said=False)
    assert mate.id not in us.brain.spoken_ids and mate.id not in us.brain.given_up
    assert mate.id not in foe.brain.given_up
    assert mate.brain.spoken_ids == set() and mate.brain.given_up == set()
    assert not mate.spoken
    assert mate.under_orders_of == foe.id  # her captor's company's, by the taking
    assert cutter.under_orders_of == ""
    assert not S.commanded_by(mate, us.id) and not S.commanded_by(cutter, mate.id)
    assert list(book) == ["|".join(sorted((foe.id, us.id)))]


@pytest.mark.parametrize("held", ["spoken", "given up"])
def test_a_cruiser_who_spoke_a_ship_or_gave_her_up_retakes_her_from_the_enemy(held):
    """The case caught: the British Amethyst cruising 0.6 miles north of a British merchant brig
    she has spoken (or whose chase she has given up), the brig then taken by a French frigate
    that leaves the sea: the Amethyst never looked at her again, and never retook her. Now the
    taking makes her a stranger to the Amethyst, who retakes her by coming up at 180, as a
    cruiser that knew nothing of her does. Old (20a8e2e3): never retaken in half an hour."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    here = destination(w.position, 180.0, 2.0 * units.NAUTICAL_MILE)
    brig = put(w, "merchant brig", "britain", _at(here), "bound for Falmouth", "bound for Falmouth")
    north = destination(here, 0.0, 0.6 * units.NAUTICAL_MILE)
    am = put(
        w,
        "frigate",
        "britain",
        _at(north),
        "cruising off the Lizard within 20 miles",
        intent="cruise off the Lizard within 20 miles",
        name="Amethyst",
    )
    (am.brain.spoken_ids if held == "spoken" else am.brain.given_up).add(brig.id)
    _taken_by_the_french(w, brig)
    for _ in range(20):
        w.run(60)
        if (P.record_of(brig) or {}).get("retaken"):
            break
    rec = P.record_of(brig) or {}
    assert rec.get("retaken") and rec.get("recaptor") == am.id, w.clock.tick
    assert brig.nation == "britain" and not P.is_prize(brig)


# -- item 4: the side of a supporter, the being of the holder -------------------------------------


def test_support_is_of_her_side_and_a_holder_off_the_sea_or_struck_holds_nobody():
    """The cause: `still` asked of the other ship and not of the holder, and `SUPPORT` never asked
    whose side the supporter was on, so each caller asked it or did not (`_captor_near` and
    `_covered` asked "of her nation", `_alone` nothing). Mended in `still`: a supporter is of her
    side (her nation or an ally's), and a holder not on the sea holds nobody, a holder struck nobody
    but her prizes. Old (20a8e2e3): the French 74 a mile off supported the British frigate, who
    under his orders was never alone; a holder of no id, gone or struck held his mark, his struck
    enemy and his supporter."""
    w, us, foe, mate = _sea()
    assert R.still(w, us, mate, R.SUPPORT) and not R.still(w, us, foe, R.SUPPORT)
    assert not R.still(w, foe, us, R.SUPPORT)
    spain = destination(foe.position, 0.0, 0.5 * units.NAUTICAL_MILE)
    don = put(w, "frigate", "spain", _at(spain), "bound for Brest", "bound for Brest", name="D")
    assert w.nations.allied("france", "spain") and R.still(w, foe, don, R.SUPPORT)
    us.under_orders_of = foe.id
    assert us.brain._alone()
    us.under_orders_of = ""
    for holder in ("", "no-such-ship"):
        assert not R.still(w, holder, foe, R.MARK)
        assert not R.still(w, holder, mate, R.SUPPORT)
    foe.struck = True
    assert R.still(w, us, foe, R.STRUCK)
    for gone in ("done", "struck"):
        setattr(us, gone, True)
        assert not R.still(w, us, foe, R.STRUCK), gone
        assert not R.still(w, us, mate, R.SUPPORT), gone
        setattr(us, gone, False)
    foe.struck = False
    for gone in ("done", "struck"):
        setattr(us, gone, True)
        assert not R.still(w, us, foe, R.MARK), gone
        setattr(us, gone, False)
    foe.struck = True
    P.possess(w, us, foe, by="a test", said=False)
    us.struck = True
    assert R.still(w, us, foe, R.PRIZE)  # her prize crew hold her until she is retaken
    us.done = True
    assert not R.still(w, us, foe, R.PRIZE)


# -- item 5: the near battery's mark --------------------------------------------------------------


def _firing_into_an_enemys_prize():
    """The player's frigate at quarters at seed 7, her guns cast loose and run out, the cap nought;
    a British merchant brig taken by the French lying to a quarter of a mile on her starboard
    beam (no brain of her own: her plan is to lie to), engaged by name to starboard, the guns
    firing as they bear for five minutes; a British frigate, the Amethyst, three miles north."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    beam = (math.degrees(float(w.ship.heading)) + 90.0) % 360.0
    s = destination(w.position, beam, 0.25 * units.NAUTICAL_MILE)
    brig = put(w, "merchant brig", "britain", _at(s), "bound for Falmouth", "bound for Falmouth")
    _taken_by_the_french(w, brig)
    brig.plan = [("lie_to", math.inf)]
    brig.brain = None
    north = destination(w.position, 0.0, 3.0 * units.NAUTICAL_MILE)
    am = put(
        w,
        "frigate",
        "britain",
        _at(north),
        "cruising off the Lizard within 20 miles",
        intent="cruise off the Lizard within 20 miles",
        name="Amethyst",
    )
    w.submit("beat to quarters")
    w.run(120)
    w.submit("cast loose the guns")
    w.run(200)
    w.submit("load with round shot")
    w.submit("run out the guns")
    w.run(200)
    assert w.submit("engage the merchant brig to starboard").kind == "guns.engage"
    w.run(300)
    return w, brig, am


@pytest.mark.parametrize("how", ["retaken", "restored"])
def test_a_mark_that_changes_hands_under_fire_is_judged_anew_and_the_fire_held(how):
    """The cause, the same as item 3's: the battery's mark is a relation laid on her people, and
    nothing ended it when she changed hands, so the guns fired as they bore at whatever she had
    become (only a strike held the fire, `action._watch_struck`). Mended where the change of hands
    ends every relation (`relations.changed_hands` tells each World whose battery is laid on her)
    and in the battery's tick, which asks the one answer (`MARK`, her captain's judgement) of her
    as she now is: no mark, the fire held and the deck told why. Run as the lead asked: the French
    prize retaken by the Amethyst, or restored, while the guns fire as they bear. Old (20a8e2e3):
    45 shot more at her in the five minutes after (108 fired at the end, for 63 at the change)."""
    w, brig, am = _firing_into_an_enemys_prize()
    battery = battery_of(w.ship)
    assert battery.target == brig.id and battery.mode is FireMode.AS_THEY_BEAR
    before = battery.rounds_fired
    assert before > 0
    if how == "retaken":
        P.retake(w, brig, by="the Amethyst coming up", how="retaken", captor=am)
    else:
        P.retake(w, brig, by="the court", how="restored")
    at = w.clock.tick
    w.run(300)
    assert battery.rounds_fired == before and battery.mode is FireMode.HOLD
    said = [e for e in w.log if e.kind == "action.mark_changed_hands"]
    assert len(said) == 1 and said[0].tick == at + 1, [e.text for e in said]
    assert said[0].text == f"A merchant brig is {how}: the guns hold their fire."
    # the minute's line after the change says the shot of that minute before it, and none after
    assert not [e for e in w.log if e.kind == "action.fired" and e.tick > at + 60]


# -- the review of 0dcdb8cf: the player's ship's own names, and the hail ---------------------------


def test_a_change_of_hands_under_another_hull_reads_the_players_ship_as_hers():
    """The review of 0dcdb8cf, F1. The cause: `relations` reads the player's ship's own names (her
    captain, her ship and its battery, her place, her colours, the orders she sails under) on the
    sea's World, whose per-ship names read whichever hull is current; since `_root` gives the World
    (item 2's one record), a change of hands run under another hull read that hull's as hers. In
    ordinary play the current hull is the captor's: a crewed French frigate's own `take possession
    of the ship` cleared all her captain knew of every ship as one of the player's ship's own
    judges. Mended in the one place, `relations._players` (the player's own hull, `World.players`),
    read wherever the module means her. The captor's captain keeps what he knew of a British
    brig-sloop; the player's own captain forgets every ship, as her own judge (gundeck-1's
    JUDGEMENT, the one list's 53); and her own state read under the captor's hull is hers. Old
    (0dcdb8cf): the captor's pirates, chases given up and recognised all emptied, and the player's
    ship read as the captor (not struck, French); 20a8e2e3 kept them (its `_root` gave the followed
    hull)."""
    from freesail.world.ships import PLAYER_ID

    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 2}
    w.submit("heave to")
    w.run(60)
    east = destination(w.position, 90.0, 0.15 * units.NAUTICAL_MILE)
    fr = put(w, "frigate", "france", _at(east), "bound for Brest", "bound for Brest", name="Renard")
    west = destination(w.position, 270.0, 3.0 * units.NAUTICAL_MILE)
    other = put(w, "brig-sloop", "britain", _at(west), "bound for Falmouth", "bound for Falmouth")
    hx = fr.crew if fr.crew is not None else crews.promote(w, fr)
    cap, mine = hx.captain, w.captain
    cap.pirates.add(other.id)
    cap.given_up.add(other.id)
    cap.recognised[other.id] = {"enemy": True, "nation": "britain", "by": "the hail"}
    mine.given_up.add(other.id)
    mine.recognised[other.id] = {"enemy": False, "nation": "britain", "by": "the hail"}
    shadow = w.vessels.get(PLAYER_ID)
    with w.as_hull(hx):
        judges = R._own_judges(R._root(w), shadow)
        assert mine in judges and cap not in judges
        assert mine in R.judges(w)
    w.submit("strike the colours")
    w.run(5)
    with w.as_hull(hx):
        hers = R._PlayersShip(w)  # her place, colours and nation where her shadow is not made
        assert hers.struck and hers.nation == "britain"
    r = hx.submit("take possession of the ship")
    assert r.kind == "prize.taken" and P.is_prize(shadow), r.text
    assert cap.pirates == {other.id} and cap.given_up == {other.id}
    assert set(cap.recognised) == {other.id}
    assert mine.given_up == set() and mine.recognised == {}


def test_a_sail_that_changes_hands_within_hail_is_hailed_and_spoken_anew():
    """The review of 0dcdb8cf, F2. The cause: the player's having spoken a sail is one fact kept in
    two flags, `Vessel.spoken` and `Vessel.hailed`, set together by both roads of the hail
    (`Vessels._promote_and_hail`, `hail._spoken`); `relations.changed_hands` ended `spoken` alone,
    and the hail is made only where she is not `hailed`, so that a ship changing hands within hail
    was never spoken again, and no hail said for her new people, until she lay beyond twice hail's
    distance (the rules captain, cruising, investigated her for forty minutes and never spoke her).
    Mended in `changed_hands`: both end. A British merchant brig lying to 0.2 miles off the
    player's ship, spoken, is taken by the French: within the minute she is hailed, the line with
    her French colours, and spoken. Old (0dcdb8cf): spoken False and hailed True at 0.22, 0.26 and
    0.33 miles, no hail; 20a8e2e3: spoken True throughout, never hailed again."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    east = destination(w.position, 90.0, 0.2 * units.NAUTICAL_MILE)
    brig = put(w, "merchant brig", "britain", _at(east), "bound for Falmouth", "bound for Falmouth")
    brig.plan = [("lie_to", float("inf"))]
    w.run(120)
    assert brig.spoken and brig.hailed
    n = len(w.log)
    _taken_by_the_french(w, brig)
    brig.plan = [("lie_to", float("inf"))]
    brig.brain = None
    w.run(60)
    said = [e for e in list(w.log)[n:] if e.kind == "sail.within_hail"]
    assert len(said) == 1 and "French colours" in said[0].text, [e.text for e in said]
    assert brig.spoken and brig.hailed
    (item,) = [
        i for i in w.lookout.strangers(w, float(w.ship.heading))["items"] if i["id"] == brig.id
    ]
    assert item["spoken"]


def test_a_ship_that_has_struck_is_refused_the_engage_in_her_own_state():
    """The review of 0dcdb8cf, F6. The cause: the order to engage asked the marks and never her own
    state. Since item 4 a holder struck fights nobody (`relations.still`), so that after the
    player's ship struck, "her" was refused as "no enemy in sight to engage ... in sight: a
    frigate" with a French frigate in sight, and a mark named was taken "to fire as they bear" for
    guns the strike keeps silent. Mended in the order, before any mark (`gunnery._engage`): a ship
    whose colours are struck is refused the engage in the words of her own state, by either road.
    Old (0dcdb8cf): "There is no enemy in sight to engage ..." and "Engage a frigate to starboard:
    ... the guns to fire as they bear."; 20a8e2e3: both taken ("guns.engage")."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    east = destination(w.position, 90.0, 0.5 * units.NAUTICAL_MILE)
    put(w, "frigate", "france", _at(east), "bound for Brest", "bound for Brest", name="Foe")
    w.run(150)
    w.submit("beat to quarters")
    w.run(30)
    assert w.submit("strike the colours").kind == "action.struck"
    w.run(5)
    battery = battery_of(w.ship)
    for order in ("engage her to starboard", "engage the frigate to starboard"):
        r = w.submit(order)
        assert r.kind == "order.rejected", (order, r.text)
        assert r.text.endswith(
            "Our own colours are struck: the guns are silent; she lies to for her captor."
        ), r.text
        assert battery.target is None and battery.mode is FireMode.HOLD
