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


def cutter_and_the_fly_taken_up(settle: str = ", and lay the Sherbourne up"):
    """(the world, the cutter, the Fly, his person): the Fly his, the cutter laid up (or as
    `settle` says), the boat that brought him home at the booms."""
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
    e = w.submit(f"take command of her{settle}")
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


def _until_home(w, hull, limit_s=7200):
    """Run until the hull's boat is back at the booms."""
    for _ in range(limit_s // 60):
        w.run(60)
        if not hull.dealings.boat.away:
            return
    raise AssertionError(f"the boat never came home: {hull.dealings.boat.words()}")


# -- the lead's reading of ab0ade58, items 2 to 7 ----------------------------------------------


def test_the_tail_lays_up_no_ship_he_commands():
    """Item 2: '..., and lay the Fly up' given aboard the Fly, his own ship, is refused in
    words and nothing changes: a ship is laid up when he has left her."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    hands = len(TR._hands(fly))
    e = w.submit("transfer two hands to the Sherbourne, and lay the Fly up")
    assert e.kind == "order.rejected", e.text
    assert "You command her" in e.text
    assert fly.vessel.regime != "in ordinary" and len(TR._hands(fly)) == hands


def test_hands_who_come_aboard_join_the_watches_as_they_stand():
    """Item 3: the hands who come are added to the watches as they stand, the smaller watch
    first; nobody already aboard either ship is moved, and the giver loses only those who
    go."""
    from freesail.crew.model import Watch

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    fly_watches = {s.id: s.watch for s in TR._hands(fly)}
    cutter_watches = {s.id: s.watch for s in TR._hands(cutter)}

    def count(hull, watch):
        return sum(1 for s in TR._hands(hull) if s.watch is watch)

    smaller = min((Watch.STARBOARD, Watch.LARBOARD), key=lambda x: (count(fly, x), x.value))
    e = w.submit("transfer one hand from the Sherbourne to the Fly")
    assert e.kind == "company.transfer", e.text
    _until_home(w, cutter)
    assert {s.id: s.watch for s in TR._hands(fly) if s.id in fly_watches} == fly_watches
    new = [s for s in TR._hands(fly) if s.id not in fly_watches]
    assert len(new) == 1 and new[0].watch is smaller
    left = {s.id: s.watch for s in TR._hands(cutter)}
    assert len(left) == len(cutter_watches) - 1
    assert all(cutter_watches[i] == wt for i, wt in left.items())


def test_a_lost_boat_carries_nobody():
    """Item 4: the giving ship's boat lost (swamped) is refused in words as the dealings
    refuse it, and stays lost."""
    from freesail.world.boats import lose_boat

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    lose_boat(w, cutter, "swamped")
    hands = len(TR._hands(cutter))
    e = w.submit("transfer two hands from the Sherbourne to the Fly")
    assert e.kind == "order.rejected", e.text
    assert "lost" in e.text
    assert cutter.dealings.boat.lost and len(TR._hands(cutter)) == hands


def test_men_told_off_for_the_loads_are_out_of_the_givers_count_at_the_order():
    """Item 5: every man told off for a load is out of the giving muster from the order (not
    only the first load's), so that no other order draws him again; at the end each is in one
    muster, and none is lost or doubled."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    giver, receiver = len(TR._hands(cutter)), len(TR._hands(fly))
    e = w.submit("transfer fifteen hands from the Sherbourne to the Fly")
    assert e.kind == "company.transfer", e.text
    assert len(TR._hands(cutter)) == giver - 15
    _until_home(w, cutter)
    # each man (a muster's ids are the ship's own, so the same id is two men in two ships)
    in_fly = {id(s) for s in TR._hands(fly)}
    in_cutter = {id(s) for s in TR._hands(cutter)}
    assert not in_fly & in_cutter
    assert (len(in_cutter), len(in_fly)) == (giver - 15, receiver + 15)


def test_a_person_is_rehomed_before_he_is_put_aboard(monkeypatch):
    """Item 6: as the prizes do it, a person moved is of the receiving ship's company before he
    is put aboard her (else a station held through him arrives as a visitor's)."""
    from freesail.world import movement

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    homes = []
    real = movement.put_aboard

    def watched(world, person, hull, *a, **k):
        homes.append((person.name, str(person.home), str(hull.id)))
        return real(world, person, hull, *a, **k)

    monkeypatch.setattr(movement, "put_aboard", watched)
    e = w.submit("transfer Mr Pearce from the Sherbourne to the Fly")
    assert e.kind == "company.transfer", e.text
    _until_home(w, cutter)
    mine = [h for h in homes if h[0] == "Mr Pearce"]
    assert mine and mine[0][1] == mine[0][2] == str(fly.id)


def test_the_officer_a_ship_is_left_to_stays_in_her():
    """Item 6: the officer the Sherbourne was left to (`command_passed_to`) is not moved out of
    her by a transfer; refused in words."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up(", and leave the Sherbourne to Mr Pearce")
    e = w.submit("transfer Mr Pearce from the Sherbourne to the Fly")
    assert e.kind == "order.rejected", e.text
    assert "left in his charge" in e.text


def test_a_receiver_gone_is_said_and_the_men_come_home():
    """Item 7: the receiving ship gone before the boat is alongside her: the boat finds no ship,
    says so in the giver's log, and brings her men home into her muster; and a ship he left
    that is gone is out of the list of the hulls he left."""
    from freesail.world.command import HULLS_LEFT

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    hands = len(TR._hands(fly))
    e = w.submit("transfer two hands to the Sherbourne")
    assert e.kind == "company.transfer", e.text
    cutter.vessel.done = True
    _until_home(w, fly)
    said = [x for x in fly.log if x.kind == "boat.returning"]
    assert said and "Sherbourne" in said[-1].text
    assert len(TR._hands(fly)) == hands
    assert str(cutter.id) not in (w.__dict__.get(HULLS_LEFT) or [])


def _came_aboard(hull, since=0):
    return [x for x in hull.log if x.kind == "company.came_aboard" and x.tick >= since]


def _due(hull, stage):
    """The tick of the boat's next job of this stage (her road's own pace)."""
    return min(j.due_tick for j in hull.dealings.jobs if j.payload.get("stage") == stage)


def test_fifteen_hands_go_across_in_two_loads_by_the_boats_road():
    """Two loads of the boat (twelve and three) by the dealings' road to another hull: every
    man told off out of her muster at the order, the first twelve in the boat; each load into
    the Fly's watches and said in her log as the boat comes alongside her, the second when she
    has been back for it; the boat home at the booms at the end."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    before = len(TR._hands(cutter)), len(TR._hands(fly))
    given = w.clock.tick
    e = w.submit("transfer fifteen hands from the Sherbourne to the Fly")
    assert e.kind == "company.transfer", e.text
    assert "in two loads" in e.text
    assert len(cutter.dealings.boat.hands) == 12 and "away" in cutter.dealings.boat.words()
    assert (len(TR._hands(cutter)), len(TR._hands(fly))) == (before[0] - 15, before[1])
    refused = w.submit("transfer two hands from the Sherbourne to the Fly")
    assert refused.kind == "order.rejected" and "is away already" in refused.text
    first_at = _due(cutter, "alongside")
    w.run(first_at - w.clock.tick + 1)
    first = _came_aboard(fly, given)
    assert len(first) == 1 and first[0].tick == first_at
    assert "Twelve hands came aboard from the Sherbourne (the first load of two)" in first[0].text
    assert len(TR._hands(fly)) == before[1] + 12
    second_at = None
    for _ in range(60):
        w.run(60)
        if cutter.dealings.boat.load_no == 2:
            second_at = _due(cutter, "alongside")
            break
    assert second_at is not None
    w.run(second_at - w.clock.tick + 1)
    both = _came_aboard(fly, given)
    assert len(both) == 2 and both[1].tick == second_at
    assert "the second load of two" in both[1].text
    _until_home(w, cutter)
    assert (len(TR._hands(cutter)), len(TR._hands(fly))) == (before[0] - 15, before[1] + 15)
    crew = fly.ship.extra["crew"]
    assert len({s.id for s in crew.sailors}) == len(crew.sailors)  # told apart where they met
    assert any(s.id.endswith(":the ship") for s in crew.sailors)
    assert "the booms" in cutter.dealings.boat.words()


def test_hands_by_their_rating():
    """`six able seamen and four ordinary`: so many of each rating, said as ten hands."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()

    def rated(hull, rating):
        return sum(1 for s in TR._hands(hull) if s.rating is rating)

    able, ordinary = rated(fly, Rating.ABLE), rated(fly, Rating.ORDINARY)
    e = w.submit("transfer six able seamen and four ordinary from the Sherbourne to the Fly")
    assert e.kind == "company.transfer" and e.text.startswith("Ten hands"), e.text
    _until_home(w, cutter)
    assert (rated(fly, Rating.ABLE), rated(fly, Rating.ORDINARY)) == (able + 6, ordinary + 4)
    assert "ten hands sign the Fly's articles" in _came_aboard(fly)[-1].text


def test_a_person_by_name_is_rehomed_to_the_ship_he_goes_to():
    """`transfer Mr Cannon and two hands to the Sherbourne`, given aboard the Fly: her mate goes
    across with the first load, is put aboard the cutter and is of her company there."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    mate = next(p for p in fly.people.people if p.name == "Mr Cannon")
    e = w.submit("transfer Mr Cannon and two hands to the Sherbourne")
    assert e.kind == "company.transfer", e.text
    _until_home(w, fly)
    assert str(mate.hull) == str(cutter.id) and str(mate.home) == str(cutter.id)
    assert mate in cutter.people.people and mate not in fly.people.people
    assert "Mr Cannon and two hands came aboard from the Fly" in _came_aboard(cutter)[-1].text


def test_the_people_and_the_hands_leave_a_laid_up_ship_her_keepers():
    """From the cutter laid up, 'the people and the hands' moves every seaman and every person
    but her keepers (§4.1, JUDGEMENT): her mate stays, and so do her idlers, her ship-keepers.
    Ten of her seamen are taken out of her muster by hand first, so that the Fly berths the
    rest and the keepers' path is the one that runs."""
    from freesail.crew.model import Station
    from freesail.world.musters import take_out

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    seamen = [s for s in TR._hands(cutter) if s.station is not Station.IDLERS]
    take_out(cutter, seamen[:10])
    idlers = [s for s in TR._hands(cutter) if s.station is Station.IDLERS]
    e = w.submit("transfer the people and the hands from the Sherbourne to the Fly")
    assert e.kind == "company.transfer", e.text
    _until_home(w, cutter)
    left = TR._hands(cutter)
    assert left == idlers and len(left) >= TR.MERCHANT_SHIP_KEEPER_HANDS
    names = {p.name: str(p.hull) for p in w.registry.persons()}
    assert names["Mr Pearce"] == str(cutter.id)  # her mate, a keeper
    assert names["Mr Pascoe"] == names["Richd. Oliver"] == str(fly.id)
    assert TR._souls(fly) <= TR.berths(fly)


def test_the_refusals_in_words():
    """§6.3: the ship giving them left unable to be worked; a name she has nobody to answer to;
    the receiver past her berths; each refusal leaves both musters as they were."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()

    def counts():
        return len(TR._hands(cutter)), len(TR._hands(fly))

    was = counts()
    hands = len(TR._hands(fly))
    e = w.submit(f"transfer {hands - TR.worked_by(fly) + 1} hands to the Sherbourne")
    assert e.kind == "order.rejected"
    assert f"she wants {TR._count_words(TR.worked_by(fly))} to be worked" in e.text
    assert "Transfer fewer, or lay her up first" in e.text
    e = w.submit("transfer Mr Nobody to the Sherbourne")
    assert e.kind == "order.rejected" and "answers to 'Mr Nobody'" in e.text
    e = w.submit("transfer twenty hands from the Sherbourne to the Fly")
    assert e.kind == "order.rejected"
    souls = TR._number(TR._souls(fly))
    assert f"The Fly berths sixty; she has {souls}, and would have" in e.text, e.text
    assert counts() == was and not cutter.dealings.boat.away and not fly.dealings.boat.away


def test_the_refusals_of_the_road_and_the_order():
    """Way on her, beyond a boat's pull, a prisoner giving it, nobody of his commanding a ship,
    and a ship not his, each refused in words with nothing changed."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    was = len(TR._hands(cutter)), len(TR._hands(fly))
    cutter.ship.dyn.u = 3.0
    e = w.submit("transfer two hands from the Sherbourne to the Fly")
    assert e.kind == "order.rejected" and "The Sherbourne has 5.8 knots of way on her" in e.text
    cutter.ship.dyn.u = 0.0
    real = TR._between_m
    TR._between_m = lambda a, b: 3000.0
    try:
        e = w.submit("transfer two hands from the Sherbourne to the Fly")
    finally:
        TR._between_m = real
    assert e.kind == "order.rejected" and "beyond a boat's pull (one mile)" in e.text
    me.confined_to = "the hold"
    with pytest.raises(TR.TransferError, match="is a prisoner"):
        TR.transfer(w, me, fly, "two hands", giver=cutter)
    me.confined_to = ""
    with pytest.raises(TR.TransferError, match="You command no ship here"):
        TR.transfer(w, None, fly, "two hands", giver=cutter)
    _wo(
        w,
        'ship: a brig "Hind" of Britain at 50 09.8 N 5 02.2 W, bound for Falmouth, '
        "intent: bound for Falmouth",
    )
    w.run(60)
    hind = w.hulls[str(w.sea_vessels.find("Hind").id)]
    with pytest.raises(TR.TransferError, match="The Hind is not yours to man"):
        TR.transfer(w, me, hind, "two hands")
    assert (len(TR._hands(cutter)), len(TR._hands(fly))) == was


def test_the_refusals_name_the_ships_that_are_here_in_the_worlds_words():
    """The lead's reading of ab0ade58: no refusal names the Amazon or the Fly whatever ships
    exist, and none is in the director's words (an observed world, a prompt, a world)."""
    import types

    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    e = w.submit("transfer some of the men")
    assert e.kind == "order.rejected" and "'transfer twenty hands to the Fly'" in e.text, e.text
    e = w.submit("take command of the Sherbourne, and leave her")
    assert e.kind == "order.rejected" and "Say how the Fly is left" in e.text, e.text
    for said in (e.text,):
        assert "Amazon" not in said and "prompt" not in said and "world" not in said
    with pytest.raises(TR.TransferError, match="^You command no ship here"):
        TR.transfer(types.SimpleNamespace(observed=True), me, fly, "two hands")


def test_alongside_the_men_cross_by_the_gangway_at_the_order():
    """Within `ALONGSIDE_M` of each other there is no boat: the men go across over the gangway
    at the order, into her watches, said in both logs."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    was = len(TR._hands(cutter)), len(TR._hands(fly))
    real = TR._between_m
    TR._between_m = lambda a, b: 20.0
    try:
        e = w.submit("transfer Mr Pascoe and three hands from the Sherbourne to the Fly")
    finally:
        TR._between_m = real
    assert e.kind == "company.transfer", e.text
    assert "lying alongside, over the gangway" in e.text
    assert (len(TR._hands(cutter)), len(TR._hands(fly))) == (was[0] - 3, was[1] + 3)
    assert not cutter.dealings.boat.away
    line = _came_aboard(fly)[-1].text
    assert line.startswith("Mr Pascoe and three hands came aboard from the Sherbourne over")
    assert [x for x in cutter.log if x.kind == "company.went_across"]


def test_the_tail_lays_up_the_ship_her_people_leave():
    """'..., and lay the Sherbourne up', given aboard the Fly of the Sherbourne he left to Mr
    Pearce: her hands go and she is laid in ordinary at Falmouth, her keepers alone wanted."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up(", and leave the Sherbourne to Mr Pearce")
    assert cutter.vessel.regime != "in ordinary"
    e = w.submit("transfer two hands from the Sherbourne to the Fly, and lay the Sherbourne up")
    assert e.kind == "company.transfer", e.text
    assert cutter.vessel.regime == "in ordinary"
    assert TR.worked_by(cutter) == TR.MERCHANT_SHIP_KEEPER_HANDS


def test_between_two_kings_ships_the_company_is_turned_over_by_the_admiraltys_order():
    """A King's ship's company to another King's ship is turned over by the Admiralty's order,
    not by her captain's (§6.3, FROM MEMORY): refused in words, nothing changed."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    real = TR._service
    TR._service = lambda hull: "kings"
    try:
        e = w.submit("transfer two hands from the Sherbourne to the Fly")
    finally:
        TR._service = real
    assert e.kind == "order.rejected"
    assert "turned over to the Fly by the Admiralty's order, not by her captain's" in e.text


def test_a_kings_ships_company_is_not_turned_over_to_a_merchantman():
    """The Amazon left to her first lieutenant: her people are borne on the King's books, and
    go to no merchantman (FROM MEMORY: turned over by the Admiralty's order)."""
    from tests.test_ship_changed import fly_taken_up

    w, fly, me, e = fly_taken_up()
    e = w.submit("transfer twenty hands from the Amazon to the Fly")
    assert e.kind == "order.rejected" and "borne on the King's books" in e.text, e.text


def test_a_checkpoint_with_a_load_in_the_boat_carries_on_to_the_same_end(tmp_path):
    """Fast: a checkpoint taken with the first load in the boat, loaded, carries on to the same
    musters and the same lines as the world it was taken from."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    assert w.submit("transfer fifteen hands from the Sherbourne to the Fly").kind == (
        "company.transfer"
    )
    w.run(120)
    assert cutter.dealings.boat.hands
    cp = replay.write_checkpoint(w, tmp_path / "load.checkpoint")
    _header, resumed = replay.read_checkpoint(cp)
    for world in (w, resumed):
        _until_home(world, world.first_hull)
    fid = str(fly.id)
    assert len(TR._hands(resumed.hulls[fid])) == len(TR._hands(fly))
    assert len(TR._hands(resumed.first_hull)) == len(TR._hands(cutter))
    lines = [x.text for x in _came_aboard(fly)]
    assert [x.text for x in _came_aboard(resumed.hulls[fid])] == lines and len(lines) == 2


@pytest.mark.slow
def test_a_save_with_a_transfer_replays_to_the_same_logs(tmp_path):
    """The order is journaled: the save replays to the same digests of both ships' logs, and a
    checkpoint taken with a load in the boat carries on to the same logs."""
    w, cutter, fly, me = cutter_and_the_fly_taken_up()
    order = "transfer fifteen hands from the Sherbourne to the Fly"
    assert w.submit(order).kind == "company.transfer"
    w.run(120)
    cp = replay.write_checkpoint(w, tmp_path / "transfer.checkpoint")
    _header, resumed = replay.read_checkpoint(cp)
    for world in (w, resumed):
        _until_home(world, world.first_hull)
    fid = str(fly.id)
    assert resumed.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert resumed.first_hull.log.digest() == w.first_hull.log.digest()
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.hulls[fid].log.digest() == w.hulls[fid].log.digest()
    assert copy.first_hull.log.digest() == w.first_hull.log.digest()
    assert len(TR._hands(copy.hulls[fid])) == len(TR._hands(fly))
