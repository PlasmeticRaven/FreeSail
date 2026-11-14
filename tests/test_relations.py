"""Whether she is still what I hold her to be (`freesail/world/relations.py`; package 75, the lead's
readings of cda12ec9, the far fight's (F2) to (F5) as one family): the one answer, tried at its
own level for every relation and every way each stops being so (a mark struck, taken, gone or of
her own side; a struck ship struck to another or taken; a prize retaken or gone; a supporter
struck, taken, gone or out of company, the player's ship among them), and `Judgement._alone`, its
reader for both bodies, on a set of prizes, a set whose members are gone, a commander far off and
a player struck. The far fight's cases (the second captor, the round at a prize, the captor alone
after her prize, the signal with nobody to engage) are in `tests/test_far_action.py`."""

from __future__ import annotations

import pytest

from freesail import units
from freesail.world import prizes as P
from freesail.world import relations as R
from freesail.world import signalling
from freesail.world import signals as S
from freesail.world import squadrons as Q
from freesail.world.geo import destination
from freesail.world.ships import PLAYER_ID
from tests.test_brains import put, world_at


def _sea(cap: int = 0):
    """tests/test_brains.py's world at seed 7, the cap nought: a British frigate twelve miles
    south of the player's, a French 74 a mile east of her and a British brig-sloop a mile west."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": cap}
    here = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    east = destination(here, 90.0, 1.0 * units.NAUTICAL_MILE)
    west = destination(here, 270.0, 1.0 * units.NAUTICAL_MILE)

    def at(p):
        return {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg}

    us = put(
        w, "frigate", "britain", at(here), "bound for Falmouth", "bound for Falmouth", name="A"
    )
    foe = put(w, "seventy-four", "france", at(east), "bound for Brest", "bound for Brest", name="F")
    mate = put(w, "brig-sloop", "britain", at(west), "bound for Falmouth", "bound for Falmouth")
    return w, us, foe, mate


def test_the_relations_are_four_and_a_word_no_relation_is_refused():
    w, us, foe, _mate = _sea()
    assert R.RELATIONS == ("mark", "struck", "prize", "support")
    with pytest.raises(ValueError, match="no relation"):
        R.still(w, us, foe, "friend")
    for what in R.RELATIONS:
        assert not R.still(w, us, us, what)  # nobody is anything to herself
        assert not R.still(w, us, "no-such-ship", what)  # nor a ship not on the sea


def test_a_mark_is_an_enemy_on_the_sea_unstruck_nobodys_prize_and_not_of_her_side():
    """`MARK`: the French 74 is the frigate's mark while she is on the sea, her colours up,
    nobody's prize and an enemy by what the frigate knows; struck, taken (by anybody), gone, a
    friend by the hail, or showing colours of a nation at peace with her, she is no mark. A ship
    showing none, and known nothing of, is held as she was; one who fired on her is a mark under
    any colours."""
    w, us, foe, mate = _sea()
    judge = us.brain
    assert R.still(w, us, foe, R.MARK) and R.still(w, us, foe.id, R.MARK, judge=judge)
    assert not R.still(w, us, mate, R.MARK)  # her own side, by her colours
    foe.struck = True
    assert not R.still(w, us, foe, R.MARK)
    foe.struck = False
    colours = S.vessel_locker(foe).colours
    S.set_colours(colours, w.nations, "false", "britain", 0)
    assert not R.still(w, us, foe, R.MARK)  # British colours: of her side by all she knows
    judge.fired_on.add(foe.id)
    assert R.still(w, us, foe, R.MARK)  # she fired on her: an enemy under any colours
    judge.fired_on.discard(foe.id)
    S.set_colours(colours, w.nations, "none", "", 0)
    assert R.still(w, us, foe, R.MARK)  # none shown, nothing known: as she was held
    signalling.recognise(judge, foe.id, "france", "the hail", False)
    assert not R.still(w, us, foe, R.MARK)  # a friend by the hail
    judge.recognised.clear()
    S.set_colours(colours, w.nations, "shown", "france", 0)
    P.possess(w, mate, foe, by="a test", said=False)
    assert P.is_prize(foe) and not R.still(w, us, foe, R.MARK)  # her own nation's prize
    assert not R.still(w, foe, mate, R.MARK)  # and the prize fights nobody's battles
    foe.done = True
    assert not R.still(w, us, foe, R.MARK)


def test_a_prize_of_the_enemy_is_no_mark_for_the_rounds_and_is_taken_back_by_coming_up():
    """A prize under the enemy's prize crew is no mark (`MARK`): the rounds never fight her, and
    she is taken back by a cruiser of her old nation coming alongside (`squadrons.far_captures`,
    her prize master's `yields_when_caught`)."""
    w, us, foe, mate = _sea()
    P.possess(w, foe, mate, by="a test", said=False)
    assert P.is_prize(mate) and mate.nation == "france"
    assert not R.still(w, us, mate, R.MARK)
    assert R.still(w, us, foe, R.MARK)


def test_a_struck_ship_is_hers_to_take_unless_another_has_her_or_struck_her_and_is_there():
    """`STRUCK`: the French 74 struck is the frigate's to take possession of while she is on the
    sea and nobody's prize, struck to her or to no one known; struck to the brig-sloop she is
    the brig-sloop's while the brig-sloop is there to take her (on the sea, not struck, nobody's
    prize), and the frigate's again when the brig-sloop is gone or struck; taken by either, or
    her colours up again, or gone, she is nobody's to take."""
    w, us, foe, mate = _sea()
    assert not R.still(w, us, foe, R.STRUCK)  # her colours up
    foe.struck = True
    assert R.still(w, us, foe, R.STRUCK) and R.still(w, mate, foe, R.STRUCK)
    foe.damage["struck_to"] = us.id
    assert R.still(w, us, foe, R.STRUCK) and not R.still(w, mate, foe, R.STRUCK)
    foe.damage["struck_to"] = mate.id
    assert R.still(w, mate, foe, R.STRUCK) and not R.still(w, us, foe, R.STRUCK)
    mate.struck = True
    assert R.still(w, us, foe, R.STRUCK)  # her taker struck herself
    mate.struck = False
    mate.done = True
    assert R.still(w, us, foe, R.STRUCK)  # her taker gone from the sea
    mate.done = False
    P.possess(w, mate, foe, by="a test", said=False)
    assert not R.still(w, us, foe, R.STRUCK) and not R.still(w, mate, foe, R.STRUCK)
    assert R.still(w, mate, foe, R.PRIZE) and not R.still(w, us, foe, R.PRIZE)


def test_a_prize_is_hers_while_on_the_sea_and_neither_retaken_nor_restored():
    """`PRIZE`: her own prize (`prizes.prizes_of`'s rule): hers by the record's captor, not
    another's, and none once retaken or gone from the sea."""
    w, us, foe, mate = _sea()
    foe.struck = True
    P.possess(w, us, foe, by="a test", said=False)
    assert R.still(w, us, foe, R.PRIZE) and not R.still(w, mate, foe, R.PRIZE)
    assert P.prizes_of(w, us.id) == [foe]
    P.retake(w, foe, by="a test", how="retaken")
    assert not R.still(w, us, foe, R.PRIZE) and P.prizes_of(w, us.id) == []


def test_a_supporter_is_on_the_sea_unstruck_nobodys_prize_and_within_the_sets_distance():
    """`SUPPORT`: one who could support her: on the sea, not struck, nobody's prize, and within
    the miles her set still holds a member of it (`in_company_nm`: the set's book's `lost_nm`,
    the squadron's eight miles, the convoy's six, the blockade's twelve; in no set, the squadron
    book's eight), or the miles given."""
    w, us, _foe, mate = _sea()
    assert R.in_company_nm(w, us.id) == 8.0  # in no set: the squadron book's
    assert R.still(w, us, mate, R.SUPPORT)  # a mile off
    assert not R.still(w, us, mate, R.SUPPORT, within_nm=0.5)
    far = destination(us.position, 270.0, 8.5 * units.NAUTICAL_MILE)
    mate.position = far
    assert not R.still(w, us, mate, R.SUPPORT)
    for kind, book, nm in (
        ("convoy", "", 6.0),
        ("squadron", "", 8.0),
        ("squadron", "blockade", 12.0),
    ):
        sq = Q.Squadron(id=f"s-{kind}-{book}", name="the set", kind=kind, book=book)
        sq.commander, sq.members = us.id, [us.id, mate.id]
        w.squadrons.add(sq, w)
        assert R.in_company_nm(w, us.id) == nm and R.in_company_nm(w, mate.id) == nm
        assert R.still(w, us, mate, R.SUPPORT) is (nm > 8.5), kind
        w.squadrons.remove(sq, w)
    mate.position = destination(us.position, 270.0, 1.0 * units.NAUTICAL_MILE)
    mate.struck = True
    assert not R.still(w, us, mate, R.SUPPORT)
    mate.struck = False
    P.possess(w, us, mate, by="a test", said=False)
    assert not R.still(w, us, mate, R.SUPPORT)  # a prize supports nobody


def test_the_players_ship_supports_while_she_has_a_place_and_has_not_struck():
    """`SUPPORT` and `MARK` of the player's ship (`PLAYER_ID`): her shadow on the sea where it is
    made, else her World's place and colours; struck (the World's `extra["struck"]`, a tick that
    may be nought), she supports nobody and is nobody's mark."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    near = destination(w.position, 180.0, 2.0 * units.NAUTICAL_MILE)
    at = {"lat_deg": near.lat_deg, "lon_deg": near.lon_deg}
    them = put(w, "frigate", "france", at, "bound for Brest", "bound for Brest", name="T")
    ours = put(w, "frigate", "britain", at, "bound for Falmouth", "bound for Falmouth", name="O")
    for made in (False, True):
        if made:
            w.vessels.player_shadow(w)
            assert w.vessels.get(PLAYER_ID) is not None
        assert R.still(w, ours, PLAYER_ID, R.SUPPORT) and R.still(w, them, PLAYER_ID, R.MARK)
        assert not R.still(w, them, PLAYER_ID, R.SUPPORT, within_nm=1.0)
        w.ship.extra["struck"] = 0  # struck at the first tick
        assert not R.still(w, ours, PLAYER_ID, R.SUPPORT), made
        assert not R.still(w, them, PLAYER_ID, R.MARK), made
        del w.ship.extra["struck"]


def _set(w, commander, members, kind="squadron"):
    sq = Q.Squadron(
        id="the-set",
        name="the set",
        kind=kind,
        nation="britain",
        commander=commander,
        members=list(members),
        goal="bound for Falmouth",
        formation="line ahead",
    )
    w.squadrons.add(sq, w)
    return sq


def test_a_set_of_her_prizes_or_of_members_gone_leaves_her_alone():
    """`Judgement._alone` (the lead's readings of cda12ec9, (F4)), the far body's: a ship in a
    set is left to its book only while a member but herself and its prizes could support her. The
    captor's company of her prize alone (`prizes.possess`'s "<id>-company") is nothing; nor a
    set whose other member is gone from the sea, struck, taken or out of company; a consort in
    company is. OLD BESIDE NEW: at 53c14457 each of these sets but the empty one made her never
    alone (`sets.of` alone was asked)."""
    w, us, foe, mate = _sea()
    assert us.brain._alone()
    foe.struck = True
    P.possess(w, us, foe, by="a test", said=False)
    company = w.squadrons.of(us.id)
    assert company is not None and company.id == f"{us.id}-company" and foe.id in company.prizes
    assert us.brain._alone()
    w.squadrons.remove(company, w)
    sq = _set(w, us.id, [us.id, mate.id])
    assert not us.brain._alone() and not mate.brain._alone()
    mate.struck = True
    assert us.brain._alone()
    mate.struck = False
    mate.position = destination(us.position, 270.0, 9.0 * units.NAUTICAL_MILE)
    assert us.brain._alone() and mate.brain._alone()
    mate.position = destination(us.position, 270.0, 1.0 * units.NAUTICAL_MILE)
    mate.done = True
    assert us.brain._alone() and mate.id in sq.members


def test_a_commander_far_off_struck_or_taken_leaves_her_alone_and_the_players_ship_too():
    """`Judgement._alone`'s commander (`under_orders_of`, no set; the lead's readings of cda12ec9,
    (F4): "`_commander_on_the_sea` has no distance (a commander two hundred miles off counts) and
    no test for a struck player"): her commander supports her within the squadron book's eight
    miles, on the sea, not struck and nobody's prize. The player's ship as her commander: within
    eight miles she is not alone, struck she is. OLD BESIDE NEW: at 53c14457 the commander two
    hundred miles off, and the player's ship struck, each left her never alone."""
    w, us, foe, mate = _sea()
    us.under_orders_of = mate.id
    assert not us.brain._alone()
    mate.position = destination(us.position, 180.0, 200.0 * units.NAUTICAL_MILE)
    assert us.brain._alone()
    mate.position = destination(us.position, 270.0, 1.0 * units.NAUTICAL_MILE)
    mate.struck = True
    P.possess(w, foe, mate, by="a test", said=False)
    assert P.is_prize(mate) and us.brain._alone()
    home = world_at(49.5, -5.5)
    home.crewed_settings = {"cap": 0}
    near = destination(home.position, 180.0, 3.0 * units.NAUTICAL_MILE)
    at = {"lat_deg": near.lat_deg, "lon_deg": near.lon_deg}
    v = put(home, "frigate", "britain", at, "bound for Falmouth", "bound for Falmouth", name="V")
    v.under_orders_of = PLAYER_ID
    assert not v.brain._alone()
    home.ship.extra["struck"] = 0
    assert v.brain._alone()
    del home.ship.extra["struck"]
    v.position = destination(home.position, 180.0, 9.0 * units.NAUTICAL_MILE)
    assert v.brain._alone()


def test_the_players_captain_in_a_set_is_alone_when_her_commander_is_far_off_or_struck():
    """`Judgement._alone` on the near body (the player's rules captain, `captains.Captain`): in a
    set commanded by a far brig-sloop five miles off she is left to its book; the brig-sloop nine
    miles off, struck or gone, she is alone (the one answer is the same for both bodies)."""
    home = world_at(49.5, -5.5)
    cap = home.captain
    near = destination(home.position, 180.0, 5.0 * units.NAUTICAL_MILE)
    mate = put(
        home,
        "brig-sloop",
        "britain",
        {"lat_deg": near.lat_deg, "lon_deg": near.lon_deg},
        "bound for Falmouth",
        name="Mate",
    )
    _set(home, mate.id, [mate.id, PLAYER_ID])
    assert not cap._alone()
    mate.position = destination(home.position, 180.0, 9.0 * units.NAUTICAL_MILE)
    assert cap._alone()
    mate.position = near
    assert not cap._alone()
    mate.struck = True
    assert cap._alone()
    mate.struck = False
    mate.done = True
    assert cap._alone()
