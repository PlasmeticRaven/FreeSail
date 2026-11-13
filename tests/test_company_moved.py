"""Package 60, step 2 (`docs/design/Design-ShipBought.md` §6): the company moved between two
hulls by one order, `transfer ... to the "Fly"`: hands by count and by rating, persons by name
and rehomed, the boat's loads in their time, each muster made again; the refusals of §6.3.
Truth 7-484 is in tests/test_known_truths.py, calling here.

The ground: the merchant cutter at anchor in Carrick Road; a topsail schooner, the Fly, laid up
in ordinary at Falmouth by the director's word, a cable or so off, and given the player in play
(the `command:` form); he goes across in his boat, takes command of her and lays the cutter up,
and the boat is home again.
"""

from __future__ import annotations

import json

import pytest

from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.crew.model import Rating
from freesail.world import knowledge
from freesail.world import transfer as TR
from tests.test_boat_hull import CARRICK_ROAD
from tests.test_ordnance import at_anchor_in
from tests.test_ship_changed import _wo


def cutter_and_the_fly_taken_up():
    """(the world, the cutter, the Fly, his person): the Fly his, the cutter laid up, the boat
    that brought him home at the booms."""
    w = at_anchor_in(CARRICK_ROAD)
    _wo(
        w,
        'ship: a schooner "Fly" of Britain at 50 09.9 N 5 02.3 W, bound for Falmouth, '
        "intent: bound for Falmouth",
    )
    w.run(60)
    fly = w.sea_vessels.find("Fly")
    _wo(w, 'ship "Fly": in ordinary at Falmouth')
    w.run(1800)
    _wo(w, 'command: a new command for the master: the schooner "Fly" at Falmouth')
    me = knowledge.players_person(w)
    assert w.submit("go to the boat").kind == "person.aboard"
    assert w.submit("come alongside the Fly").kind == "boat.alongside"
    for _ in range(30):
        w.run(60)
        if str(me.hull) == str(fly.id):
            break
    e = w.submit("take command of her, and lay the Sherbourne up")
    assert e.kind == "ship.taken_up", e.text
    cutter, hull = w.first_hull, w.hulls[str(fly.id)]
    for _ in range(40):
        w.run(60)
        if not cutter.dealings.boat.away:
            break
    assert not cutter.dealings.boat.away
    return w, cutter, hull, me


def test_a_ship_taken_up_from_ordinary_wakes_at_her_anchor_and_is_workable():
    """Step 1, the lead's reading of ab0ade58 (item 1): the Fly laid in ordinary by the
    director's word sleeps in the far shape; taken up, she is his ship and is woken at once,
    riding at her anchor in Carrick Road as her far body lay, and forty minutes on she is
    awake, at her anchor where she was, and nothing failed in her (no box-off of a ship
    adrift)."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    v = fly.vessel
    assert v.crew.awake and v.crew.shape == "full"
    assert fly.at_anchor
    where = fly.position
    w.run(2400)
    assert v.crew.awake and v.crew.shape == "full" and w.players is fly
    assert fly.at_anchor
    assert TR._between_m(fly, type("P", (), {"position": where})()) < 100.0
    assert not [x for x in fly.log if x.kind == "evolution.failed"]
    assert fly.dealings.in_port() is not None


def _came_aboard(hull, since=0):
    return [x for x in hull.log if x.kind == "company.came_aboard" and x.tick >= since]


def test_fifteen_hands_go_across_in_two_loads_in_their_time_each_muster_made_again():
    """Two loads of the boat (twelve and three) a quarter of an hour each within two cables;
    the men in the boat in neither muster while she is away; each load said in her log as it
    comes aboard; both musters made again (the hands counted, their watches dealt)."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    before = len(TR._hands(cutter)), len(TR._hands(fly))
    given = w.clock.tick
    e = w.submit("transfer fifteen hands to the Fly")
    assert e.kind == "company.transfer", e.text
    assert "in two loads" in e.text
    w.run(60)
    in_boat = before[0] + before[1] - len(TR._hands(cutter)) - len(TR._hands(fly))
    assert in_boat == 12  # the first load in the boat, in neither muster
    assert "away" in cutter.dealings.boat.words()
    assert w.submit("transfer two hands to the Fly").kind == "order.rejected"  # the boat away
    w.run(TR.LOAD_NEAR_S)
    first = _came_aboard(fly, given)
    assert len(first) == 1 and "the first load of two" in first[0].text
    assert first[0].tick == given + TR.LOAD_NEAR_S
    w.run(TR.LOAD_NEAR_S)
    both = _came_aboard(fly, given)
    assert len(both) == 2 and "the second load of two" in both[1].text
    assert both[1].tick == given + 2 * TR.LOAD_NEAR_S
    assert (len(TR._hands(cutter)), len(TR._hands(fly))) == (before[0] - 15, before[1] + 15)
    crew = fly.ship.extra["crew"]
    assert len({s.id for s in crew.sailors}) == len(crew.sailors)  # told apart where they met
    assert all(s.at is None for s in crew.sailors if ":" in s.id)
    assert not cutter.dealings.boat.away and "the booms" in cutter.dealings.boat.words()


def test_hands_by_their_rating():
    """`six able seamen and four ordinary`: so many of each rating, said as ten hands."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()

    def rated(hull, rating):
        return sum(1 for s in TR._hands(hull) if s.rating is rating)

    able, ordinary = rated(fly, Rating.ABLE), rated(fly, Rating.ORDINARY)
    e = w.submit("transfer six able seamen and four ordinary to the Fly")
    assert e.kind == "company.transfer" and e.text.startswith("Ten hands"), e.text
    w.run(TR.LOAD_NEAR_S + 60)
    assert (rated(fly, Rating.ABLE), rated(fly, Rating.ORDINARY)) == (able + 6, ordinary + 4)
    assert "ten hands sign the Fly's articles" in _came_aboard(fly)[-1].text


def test_a_person_by_name_is_rehomed_to_the_ship_he_goes_to():
    """`transfer Mr Cannon and two hands to the Sherbourne`, given aboard the Fly: her mate goes
    across with the first load, is put aboard the cutter and is of her company there."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    mate = next(p for p in fly.people.people if p.name == "Mr Cannon")
    e = w.submit("transfer Mr Cannon and two hands to the Sherbourne")
    assert e.kind == "company.transfer", e.text
    w.run(TR.LOAD_NEAR_S + 60)
    assert str(mate.hull) == str(cutter.id) and str(mate.home) == str(cutter.id)
    assert mate in cutter.people.people and mate not in fly.people.people
    assert "Mr Cannon and two hands came aboard from the Fly" in _came_aboard(cutter)[-1].text


def test_the_people_and_the_hands_leave_a_laid_up_ship_her_keepers():
    """From the cutter laid up, 'the people and the hands' moves every hand but her ship-keeper
    (§4.1, JUDGEMENT), where the Fly berths them; refused in words where she would not."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    room = TR.berths(fly) - TR._souls(fly)
    hands = len(TR._hands(cutter))
    e = w.submit("transfer the people and the hands to the Fly")
    if hands - TR.MERCHANT_SHIP_KEEPER_HANDS > room:
        assert e.kind == "order.rejected" and f"berths {TR._number(TR.berths(fly))}" in e.text
        assert len(TR._hands(cutter)) == hands  # nothing changed
        e = w.submit(f"transfer {room} hands to the Fly")
    assert e.kind == "company.transfer", e.text
    w.run(3 * TR.LOAD_NEAR_S + 60)
    assert TR._souls(fly) <= TR.berths(fly)


def test_the_refusals_in_words():
    """§6.3: the ship giving them left unable to be worked; the receiver past her berths; a
    name she has nobody to answer to; no ship of his named; nothing to transfer."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    hands = len(TR._hands(fly))
    e = w.submit(f"transfer {hands - TR.worked_by(fly) + 1} hands to the Sherbourne")
    assert e.kind == "order.rejected"
    assert f"she wants {TR._count_words(TR.worked_by(fly))} to be worked" in e.text
    assert "Transfer fewer, or lay her up first" in e.text
    e = w.submit("transfer Mr Nobody to the Sherbourne")
    assert e.kind == "order.rejected" and "answers to 'Mr Nobody'" in e.text
    e = w.submit("transfer twenty hands to the Fly")
    assert e.kind == "order.rejected"
    assert len(TR._hands(fly)) == hands  # nothing changed by a refusal


def test_a_kings_ships_company_is_not_turned_over_to_a_merchantman():
    """The Amazon left to her first lieutenant: her people are borne on the King's books, and
    go to no merchantman (FROM MEMORY: turned over by the Admiralty's order)."""
    from tests.test_ship_changed import fly_taken_up

    w, fly, me, e = fly_taken_up()
    e = w.submit("transfer twenty hands from the Amazon to the Fly")
    assert e.kind == "order.rejected" and "borne on the King's books" in e.text, e.text


@pytest.mark.slow
def test_a_save_with_a_transfer_replays_to_the_same_logs(tmp_path):
    """The order is journaled: the save replays to the same digests of both ships' logs, and a
    checkpoint taken with a load in the boat carries on to the same logs."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    assert w.submit("transfer fifteen hands to the Fly").kind == "company.transfer"
    w.run(120)
    cp = replay.write_checkpoint(w, tmp_path / "transfer.checkpoint")
    _header, resumed = replay.read_checkpoint(cp)
    for world in (w, resumed):
        world.run(2 * TR.LOAD_NEAR_S)
    fid = str(fly.id)
    assert resumed.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert resumed.first_hull.log.digest() == w.first_hull.log.digest()
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert copy.first_hull.log.digest() == w.first_hull.log.digest()
    assert len(TR._hands(copy.hulls[fid])) == len(TR._hands(fly))
