"""Package 60, step 1 (`docs/design/Design-ShipBought.md` §2 to §4, §9.2; its gate §13): the
player's ship changed in play.

First the four floors of §4.2, each a fault waiting whether or not a ship is ever changed (the
gate's addition (a)): a crewed hull with no far brain is never put out of the world by an empty
plan; a far brain may be given to any ship but the player's; the game's first hull is never
released; the switch measures every crewed body by her own position. Then the followed ship's
far body at her truth (§9.2, the `--ship` road mended). Then the act: the director gives a
ship lying at Falmouth by the `command:` form, the player goes aboard her by his boat and takes
command of her by his order, the old ship left to her senior officer; the save replays across
the two ships; the refusals. Truths 7-480 to 7-483 are in tests/test_known_truths.py, calling
here.
"""

from __future__ import annotations

import json

import pytest

from freesail.agents.journal import journal_of, person_journal
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.ui.console import aboard_ship
from freesail.world import command, crews, knowledge
from freesail.world.geo import bearing_and_distance
from freesail.world.movement import put_aboard
from tests.test_boat_hull import CARRICK_ROAD, at_anchor_in
from tests.test_crews import _frigate_and_the_brig_x_on_the_sea


def _wo(w, text: str):
    e = w.world_order(f"{text} [reason: the test]", "the test")
    assert e.data["result"] == "done", e.text
    return e


def fly_given_at_falmouth():
    """The frigate at anchor in Carrick Road; a merchant brig, the Fly, put on the sea two
    cables off bound for Falmouth; the director's `command:` form gives her to Captain Bowen
    in play (she lies at Falmouth)."""
    w = at_anchor_in(CARRICK_ROAD)
    _wo(
        w,
        'ship: a merchant brig "Fly" of Britain at 50 09.9 N 5 02.3 W, bound for Falmouth, '
        "intent: bound for Falmouth",
    )
    w.run(120)
    fly = w.sea_vessels.find("Fly")
    e = _wo(w, 'command: a new command for Captain Bowen: the merchant brig "Fly" at Falmouth')
    assert "given him in play" in e.text
    return w, fly


def fly_taken_up():
    """`fly_given_at_falmouth`, then the player's own orders: to the boat, alongside the Fly,
    aboard her as a visitor, and `take command of her`."""
    w, fly = fly_given_at_falmouth()
    me = knowledge.players_person(w)
    assert w.submit("go to the boat").kind == "person.aboard"
    assert w.submit("come alongside the Fly").kind == "boat.alongside"
    for _ in range(60):
        w.run(60)
        if str(me.hull) == str(fly.id):
            break
    assert str(me.hull) == str(fly.id) and knowledge.players_visitor(w) is me
    e = w.submit("take command of her")
    assert e.kind == "ship.taken_up", e.text
    return w, fly, me, e


# ---------------------------------------------------------------------------
# the four floors (the design's §4.2; the gate's addition (a))
# ---------------------------------------------------------------------------


def test_a_crewed_hull_with_no_far_brain_lies_as_she_lay_and_is_never_put_out_of_the_world():
    """A hull with no far captain sleeps as she lay (package 60, ruling A on the fourth reading:
    at her anchor, lying to, or her course held; before, she was laid to wherever she was),
    and is kept: never done, her company still hers."""
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    b.brain = None
    b.plan = []
    lay = crews.how_she_lies(b)
    crews.demote(w, b)
    assert not hull.awake
    w.run(180)
    assert not b.done and b.plan and crews.how_she_lies(b) == lay, (lay, b.plan)
    assert w.hulls.get(b.id) is hull and len(w.registry.company(b.id)) > 0


def test_a_far_brain_may_be_given_to_any_ship_but_the_players():
    from freesail.world.prizes import _give_intent

    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    shadow = w.sea_vessels.player_shadow(w)
    _give_intent(w, shadow, "bound for Falmouth", "kings-ship")
    assert shadow.brain is None  # the player's ship is awake always
    me = knowledge.players_person(w)
    command.give(w, b, me, by="the test")
    put_aboard(w, me, hull, "quarterdeck", by="the boat")
    command.take_up(w, me, hull)
    _give_intent(w, shadow, "bound for Falmouth", "kings-ship")
    assert shadow.brain is not None  # the first hull is his no longer


def test_the_games_first_hull_is_never_released_whatever_her_far_body_does():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    first = w.first_hull
    shadow = w.sea_vessels.player_shadow(w)
    company = len(w.registry.company(first.id))
    shadow.done = True
    crews.release_done(w)
    assert w.hulls.get(first.id) is first and shadow.crew is first
    assert len(w.registry.company(first.id)) == company


def test_the_switch_measures_every_crewed_body_by_her_own_position():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    b.brain = None  # a hull with no far brain beside the player's ship
    nm = bearing_and_distance(w.position, b.position)[1] / 1852.0
    assert nm < crews.settings(w)[2]
    crews.switch(w)
    assert hull.awake, "a hull alongside was measured as beyond the range"


# ---------------------------------------------------------------------------
# the followed ship's far body at her truth (the design's §9.2; truth 7-481)
# ---------------------------------------------------------------------------


def followed_body_off_m(minutes: int = 20) -> list[float]:
    """The brig X followed under `--ship` with the royals set: her far body's distance from
    her truth every five minutes (it stood 934 m off after five, 3,803 m after twenty, on the
    trunk before this step)."""
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    aboard_ship(w, "X", lambda s: None)
    w.submit("set the royals")
    out = []
    for _ in range(minutes // 5):
        w.run(300)
        out.append(bearing_and_distance(hull.position, b.position)[1])
    return out


def test_the_followed_ships_far_body_stands_at_her_truth():
    off = followed_body_off_m(20)
    assert max(off) < 50.0, off


# ---------------------------------------------------------------------------
# the act (the design's §2.3; truths 7-480, 7-482, 7-483)
# ---------------------------------------------------------------------------


def test_the_player_takes_command_of_a_ship_given_him_and_his_person_seat_and_journal_go_with_him():
    w, fly = fly_given_at_falmouth()
    amazon = w.players
    me = knowledge.players_person(w)
    mine = person_journal(w, me)
    mine.append(w, "The Fly is to be mine.", by="the test")
    assert w.submit("go to the boat").kind == "person.aboard"
    assert w.submit("come alongside the Fly").kind == "boat.alongside"
    for _ in range(60):
        w.run(60)
        if str(me.hull) == str(fly.id):
            break
    e = w.submit("take command of her")
    assert e.kind == "ship.taken_up"
    hull = w.hulls[str(fly.id)]
    assert w.players is hull and w.first_hull is amazon and w.followed == str(fly.id)
    assert knowledge.players_person(w) is me and knowledge.player_hull(w) is hull
    assert me.home == str(fly.id) and hull.people.captain is me
    assert knowledge.players_visitor(w) is None  # she is his home, not a visit
    assert fly.brain is None
    assert person_journal(w, me) is mine and journal_of(hull, "captain") is mine
    assert "Captain Bowen takes command of the Fly" in e.text
    assert any(x.kind == command.TAKEN_UP for x in hull.log)
    left = [x for x in amazon.log if x.kind == command.TAKEN_UP]
    assert len(left) == 1 and "leaves the Amazon for the Fly; she is left to" in left[0].text
    assert amazon.people.captain is not me  # her senior officer commands her
    # his orders are the Fly's now
    assert w.submit("where am i").text.endswith("aboard the Fly, on the quarterdeck.")


def test_the_save_replays_across_the_two_ships_its_first_block_the_first_hulls(tmp_path):
    """The save replays across the change with his orders after it (the lead's review of
    step 1, item 7), and a checkpoint taken after the change carries on to the same logs."""
    w, fly, me, _ = fly_taken_up()
    fid = str(fly.id)
    assert w.submit("weigh anchor").kind == "order.accepted"
    w.run(600)
    cp = replay.write_checkpoint(w, tmp_path / "changed.checkpoint")
    _header, resumed = replay.read_checkpoint(cp)
    for world in (w, resumed):
        assert world.submit("where am i").kind
        world.run(600)
    assert resumed.players is resumed.hulls[fid]
    assert resumed.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert resumed.first_hull.log.digest() == w.first_hull.log.digest()
    data = json.loads(json.dumps(w.save()))
    assert data["ship_ref"]["path"].endswith("frigate-36.yaml")
    assert data["player_ship"] == fid
    copy = replay.replay(data, ship_factory)
    assert copy.players is copy.hulls[fid]
    assert copy.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert copy.first_hull.log.digest() == w.first_hull.log.digest()
    assert knowledge.players_person(copy).name == me.name


def test_a_save_with_no_change_carries_no_player_ship_and_the_split_reads_as_before():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    w.run(120)
    data = w.save()
    assert "player_ship" not in data and w.players is w.first_hull
    assert w.__dict__.get("_players") is None


def test_the_old_ship_is_kept_in_the_world_with_her_company():
    w, fly, me, _ = fly_taken_up()
    amazon = w.first_hull
    company = len(w.registry.company(amazon.id))
    w.run(1800)
    assert w.hulls.get(amazon.id) is amazon
    assert len(w.registry.company(amazon.id)) == company
    body = amazon.vessel
    assert body is not None and not body.done


def test_the_old_ship_laid_up_at_falmouth():
    w, fly = fly_given_at_falmouth()
    me = knowledge.players_person(w)
    hull = w.hulls.get(str(fly.id)) or crews.station_world(w, str(fly.id))[1]
    put_aboard(w, me, hull, "quarterdeck", by="the boat")
    text, data = command.take_up(w, me, hull, how=command.LAID_UP)
    assert "the Amazon is laid in ordinary at Falmouth" in text
    shadow = w.first_hull.vessel
    assert shadow.regime == "in ordinary" and shadow.plan[0][0] == "anchor"


# ---------------------------------------------------------------------------
# the refusals (the design's §2.5)
# ---------------------------------------------------------------------------


def test_the_refusals_in_words():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    me = knowledge.players_person(w)
    put_aboard(w, me, hull, "quarterdeck", by="the boat")
    with pytest.raises(command.CommandError, match="is not yours: she is her owners'"):
        command.take_up(w, me, hull)
    e = w.submit("take command of her")
    assert e.kind == "order.rejected" and "is not yours" in e.text
    command.give(w, b, me, by="the test")
    with pytest.raises(command.CommandError, match="lies at no anchor in a port"):
        command.take_up(w, me, hull, how=command.LAID_UP)
    with pytest.raises(command.CommandError, match="Nobody of the Amazon answers to"):
        command.take_up(w, me, hull, officer="Mr Nobody")
    assert w.players is w.first_hull and me.home == "the ship"  # nothing changed
    # from the boat, before going aboard
    w2, fly = fly_given_at_falmouth()
    assert w2.submit("go to the boat").kind == "person.aboard"
    e = w2.submit("take command of her")
    assert e.kind == "order.rejected" and "is a boat" in e.text
    e = w2.submit('take command of the "Fly"')
    assert e.kind == "order.rejected" and "You are not aboard the Fly" in e.text


# ---------------------------------------------------------------------------
# the lead's review of step 1 (2026-11-12), items 1 to 6 and 8, each failing before its mend
# ---------------------------------------------------------------------------


def test_a_direct_take_up_writes_her_line_in_the_new_ships_log():
    """Item 1: the act called directly (as step 3's purchase will) says itself in the new
    ship's log; the set's check overwrote `said` and wrote nothing."""
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    me = knowledge.players_person(w)
    command.give(w, b, me, by="the test")
    put_aboard(w, me, hull, "quarterdeck", by="the boat")
    command.take_up(w, me, hull)
    assert sum(1 for x in hull.log if x.kind == command.TAKEN_UP) == 1


def test_the_boat_that_brought_him_across_goes_home_and_is_hoisted_in():
    """Item 2: the launch lying alongside the Fly for his coming back pulls home to the Amazon
    when he has taken command, and is hoisted in there; she lay alongside for ever."""
    w, fly, me, e = fly_taken_up()
    act = w.clock.tick
    launch = next(h for h in w.hulls.values() if movement_boat(h))
    for _ in range(60):
        w.run(60)
        if launch.vessel is None or launch.vessel.done:
            break
    assert launch.vessel.done and str(launch.id) not in w.hulls
    assert any(x.kind == "boat.hoisted_in" and x.tick > act for x in w.first_hull.log)


def movement_boat(hull) -> bool:
    from freesail.world.movement import is_boat_hull

    return is_boat_hull(hull)


def test_a_third_ships_boat_alongside_her_waits_on_when_he_takes_command():
    """The lead's review of 1eb18434 (B): a boat of a third ship's lying fast alongside the Fly,
    which did not bring him, is not sent home by his taking command (`_boats_home` sent every
    other ship's boat alongside her home); the launch that brought him is."""
    from freesail.world import boats

    w, fly = fly_given_at_falmouth()
    me = knowledge.players_person(w)
    assert w.submit("go to the boat").kind == "person.aboard"
    assert w.submit("come alongside the Fly").kind == "boat.alongside"
    for _ in range(60):
        w.run(60)
        if str(me.hull) == str(fly.id):
            break
    _wo(
        w,
        'ship: a merchant brig "Hind" of Britain at 50 09.8 N 5 02.2 W, bound for Falmouth, '
        "intent: bound for Falmouth",
    )
    w.run(60)
    hind = w.hulls[str(w.sea_vessels.find("Hind").id)]
    hind.ship.dyn.u = 0.0  # her way off her, by hand, for the boat to be hoisted out
    jolly, _said = boats.man_boat(w, hind, "")
    boats.board_from_boat(w, jolly, w.hulls[str(fly.id)])
    assert w.submit("take command of her").kind == "ship.taken_up"
    w.run(600)
    mark = dict(boats._oars(jolly).pulling_for or {})
    assert str(jolly.id) in w.hulls and mark.get("fast") and mark.get("hull") == str(fly.id)
    launch = next(h for h in w.hulls.values() if movement_boat(h) and h is not jolly)
    assert any(x.kind == "boat.mark" and "nobody to wait for" in x.text for x in launch.log)


def test_the_man_who_gives_her_up_is_her_late_master_never_the_player():
    """Item 3: her rules captain stands down in his own name, before the command passes; the
    line named the player standing aside at his own order."""
    w, fly, me, e = fly_taken_up()
    hull = w.players
    line = [x for x in hull.log if x.kind == "captain.aside"][-1]
    assert not line.text.startswith(me.name) and f"gives up her command to {me.name}" in line.text
    assert "stands aside at your order" not in line.text


def test_the_director_doubts_a_ship_not_his_services_to_give():
    """Item 4: a ship of another nation, an enemy's, or a prize not condemned is doubted in
    words; a British merchantman lying at Falmouth is not."""
    from freesail.world import orders as WO

    order = WO.parse(
        'command: a new command for Captain Bowen: the merchant brig "Fly" at Falmouth'
    )
    for nation, words in (
        ("France", "is an enemy's ship (France's)"),
        ("Portugal", "is a ship of Portugal"),
        ("Britain", None),
    ):
        w = at_anchor_in(CARRICK_ROAD)
        _wo(w, f'ship: a merchant brig "Fly" of {nation} at 50 09.9 N 5 02.3 W, bound for Falmouth')
        w.run(120)
        said = WO.doubt(w, order)
        assert (said is None) if words is None else (words in str(said)), (nation, said)
    w.sea_vessels.find("Fly").prize = {"captor": "the ship", "manned": True}
    assert "a prize the court has not condemned" in str(WO.doubt(w, order))


def test_the_hull_he_left_asleep_wakes_when_she_is_near_again_and_no_other_hull_does():
    """Item 6, as the lead's review of 1eb18434 narrowed it: the hull he left, kept with no far
    brain and put to sleep, is woken within the range (built from the ships with a brain
    alone, she slept for good); a hull he never commanded with no far brain (the Hind's, put
    to sleep by hand) is not woken by it: the switch woke any such hull."""
    w, fly, me, e = fly_taken_up()
    old = w.first_hull
    crews.demote(w, old.vessel)
    assert not old.awake
    crews.switch(w)
    assert old.awake
    _wo(
        w,
        'ship: a merchant brig "Hind" of Britain at 50 09.8 N 5 02.2 W, bound for Falmouth, '
        "intent: bound for Falmouth",
    )
    w.run(60)
    hind = w.sea_vessels.find("Hind")
    hind.brain = None
    crews.demote(w, hind)
    crews.switch(w)
    assert not w.hulls[str(hind.id)].awake


def test_his_weigh_anchor_waits_for_the_furling_and_is_not_belayed():
    """Item 6: the Fly finishing her coming to under her late master as he takes command; his
    'weigh anchor' waits for the furling and is then begun (it was belayed with no word)."""
    w, fly, me, e = fly_taken_up()
    act = w.clock.tick
    hull = w.players
    assert w.submit("weigh anchor").kind == "order.accepted"
    w.run(1200)
    assert any(
        x.kind == "evolution.started" and x.tick > act and "up anchor" in x.text for x in hull.log
    )


def test_a_weigh_given_as_she_comes_to_an_anchor_says_at_the_order_that_it_waits():
    """The lead's review of 1eb18434 (A), every ship's: the frigate coming to an anchor under
    plain sail is ordered to weigh at tick 300; the weigh waits for the anchor, and the log
    says so at the order (it ran at 1482, as she was brought up, with no word)."""
    from tests.test_anchor import road_world

    w = road_world(speed_kn=3.0)
    w.submit("set plain sail")
    w.run(240)
    assert w.submit("come to an anchor").kind == "order.accepted"
    w.run(60)
    given = w.clock.tick
    assert w.submit("weigh anchor").kind == "order.accepted"
    w.run(2)
    said = [x for x in w.log if x.kind == "evolution.waiting" and x.tick >= given]
    assert said and "The weigh waits for the anchor" in said[0].text
    assert said[0].tick <= given + 1


def test_a_chase_of_the_first_hull_steers_for_her_body_after_the_change():
    """Item 5: `PLAYER_ID` is the game's first hull; after he takes command of another, a
    chase of hers steers for her own body, not for his new ship."""
    from freesail.world.ships import PLAYER_ID

    w, fly, me, e = fly_taken_up()
    w.run(60)
    first = w.first_hull.vessel
    pos, _east, _north = fly._target_of(w, PLAYER_ID)
    assert bearing_and_distance(pos, first.position)[1] < 1.0
    assert bearing_and_distance(pos, w.players.position)[1] > 100.0


def test_his_new_ship_firing_is_no_pirate_in_her_own_captains_eyes():
    """Item 5: a witness of the fire; the root's own captain was the new ship's, and the
    firer's id hers, so she marked herself a pirate."""
    from freesail.combat import action

    w, fly, me, e = fly_taken_up()
    hull = w.players
    with w.as_hull(hull):
        action._witnessed(w, w.clock.tick)
    cap = hull.captain
    assert str(fly.id) not in getattr(cap, "pirates", set())


def test_under_the_orders_of_the_ship_after_the_change_is_his_new_ship():
    """Item 5: 'under the orders of the ship' names the player's ship by her id."""
    w, fly, me, e = fly_taken_up()
    _wo(w, 'ship: a merchant brig "Hind" of Britain at 50 09.5 N 5 02.0 W, bound for Falmouth')
    _wo(w, 'ship "Hind": under the orders of the ship')
    assert w.sea_vessels.find("Hind").under_orders_of == str(fly.id)


def test_a_set_of_his_is_refused_after_the_change_in_words():
    """Item 5: every reader of a set takes `PLAYER_ID` for the player's ship; a set under his
    command is refused in words after he has changed ships, until a set's command is carried."""
    w, fly, me, e = fly_taken_up()
    _wo(w, 'ship: a merchant brig "Hind" of Britain at 50 09.5 N 5 02.0 W, bound for Falmouth')
    r = w.world_order(
        'squadron: "the Inshore squadron" of Britain under the ship with Hind, bound for '
        "Falmouth [reason: the test]",
        "the test",
    )
    assert r.data["result"] != "done" and "taken command of another ship" in r.text, r.text


def test_the_loader_says_a_save_from_before_played_aboard_another_ship_parts_from_its_game():
    """Item 8: no legacy mode; a save from before the followed body's mend that was played
    aboard another ship is said, by the loader, to part from its game; one of this build is
    marked and says nothing."""
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    aboard_ship(w, "X", lambda s: None)
    w.run(60)
    data = json.loads(json.dumps(w.save()))
    assert data["followed_body"] and replay.followed_body_words(data, "replay") == []
    del data["followed_body"]
    said = replay.followed_body_words(data, "replay")
    assert len(said) == 1 and "parts from it after" in said[0]
    assert "goes on from where it was saved" in replay.followed_body_words(data, "checkpoint")[0]
    w2, _b, _h = _frigate_and_the_brig_x_on_the_sea()
    plain = json.loads(json.dumps(w2.save()))
    del plain["followed_body"]
    assert replay.followed_body_words(plain, "replay") == []
