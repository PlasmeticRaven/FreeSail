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


def test_a_crewed_hull_with_no_far_brain_lies_where_she_is_and_is_never_put_out_of_the_world():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    b.brain = None
    b.plan = []
    crews.demote(w, b)
    assert not hull.awake
    w.run(180)
    assert not b.done and b.plan and b.plan[0][0] in ("lie_to", "anchor")
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


def test_the_save_replays_across_the_two_ships_its_first_block_the_first_hulls():
    w, fly, me, _ = fly_taken_up()
    w.run(600)
    data = json.loads(json.dumps(w.save()))
    assert data["ship_ref"]["path"].endswith("frigate-36.yaml")
    assert data["player_ship"] == str(fly.id)
    copy = replay.replay(data, ship_factory)
    fid = str(fly.id)
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
