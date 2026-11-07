"""The boat's names are the giver's hull's (package 82b, item 5; `Design-DoorAndVisitor.md` §6).

The owner's order of the testing week, `send the boat to Lynx with the captain and Mr Pearce
and ...` (sixteen names), landed the far brigs' people aboard the Lynx: the names were read
among the frigate's company, but the boat kept them by their ids, which are their posts' ("the
master", "the boatswain") and so shared by every hull's company, and her landing looked them
up by an id map over every hull, the last hull's man of each post standing for the frigate's.
Three hulls beside the frigate, two of them asleep, reproduce it by that mechanism: the
frigate's master, boatswain and carpenter go to the Lynx and the Lynx's master comes back in
the same boat, and the sleeping brigs' men of the same posts stay in their own ships. A
person of another ship named in the order is refused in words, and the boat is not sent.

Package 75 (SW-4, Build-Ships.md §8.4): the merchant brigs sail their own file, whose company
of sixteen has a master, a mate and a second mate, a boatswain, a carpenter and a boy and no
gunner, where the brig-sloop's file gave them the frigate's posts all through; the third post
shared by every hull is the carpenter's (old: the gunner's).
"""

from __future__ import annotations

from freesail.world import crews as K
from tests.test_between_hulls import _run_until
from tests.test_crews import hove_to_world

POSTS = ("master", "boatswain", "carpenter")  # SW-4: was the gunner, no merchant brig's post


def three_hulls():
    """The frigate; the brig Lynx a cable or so off, hove to and awake; the French brigs
    Chevalier and Renard sixteen miles off, asleep, their companies with men of the
    frigate's posts."""
    w = hove_to_world()
    for words in (
        'ship: a merchant brig "Chevalier" of France at 49 45 N 5 17 W, bound for Brest',
        'ship "Chevalier": intent bound for Brest',
        'ship: a merchant brig "Renard" of France at 49 45.2 N 5 17 W, bound for Brest',
        'ship "Renard": intent bound for Brest',
        'ship: a merchant brig "Lynx" of Britain at 49 30 N 5 29.5 W, bound for Falmouth',
        'ship "Lynx": intent bound for Falmouth',
        'ship "Lynx": order heave to for a watch',
    ):
        e = w.world_order(words)
        assert e.data.get("result") == "done", e.text
    w.run(61)
    for name in ("Chevalier", "Renard"):
        K.station_world(w, name)
    lynx, chev, ren = (w.vessels.find(n).crew for n in ("Lynx", "Chevalier", "Renard"))
    assert lynx.shape == "full" and chev.shape == "far" and ren.shape == "far"
    return w, lynx, chev, ren


def _of(hull, post):
    return next(p for p in hull.people.people if p.id == post)


def test_the_boats_people_are_the_givers_and_the_far_brigs_men_of_the_same_posts_stay():
    w, lynx, chev, ren = three_hulls()
    w.people.find("the captain")  # the company mustered
    mine = [_of(w.own, post) for post in POSTS]
    theirs = [_of(hull, post) for hull in (chev, ren) for post in POSTS]
    hers = _of(lynx, "master")  # the Lynx's master, fetched by the same boat: the post again
    names = " and ".join(p.name for p in mine)
    e = w.submit(f"send the boat to the Lynx with {names} for {hers.name}")
    assert e.kind in ("evolution.started", "order.accepted"), e.text
    assert w.dealings.boat.away, e.text
    # alongside her: the frigate's three aboard the Lynx, the brigs' men of their posts at home
    _run_until(w, lambda: all(p.hull == lynx.id for p in mine), 1.0)
    assert all(p.home == w.own.id for p in mine)
    for p in theirs:
        assert p.hull == p.home and p.where != "boat", p.name
    # back: the Lynx's master aboard the frigate, the frigate's three still in the Lynx
    _run_until(w, lambda: not w.dealings.boat.away, 1.0)
    assert hers.hull == w.own.id and hers.home == lynx.id
    assert all(p.hull == lynx.id for p in mine)
    for p in theirs:
        assert p.hull == p.home and p.where != "boat", p.name


def test_a_person_of_another_ship_named_in_the_order_is_refused_in_words():
    w, lynx, chev, ren = three_hulls()
    # the Chevalier's mate, a post the frigate has not (package 75, SW-4: the merchant brig's own
    # company; old: her lieutenant, Mr Newton, of the brig-sloop's file)
    other = _of(chev, "mate")
    e = w.submit(f"send the boat to the Lynx with the captain and {other.name}")
    assert e.kind == "order.rejected"
    assert f"{other.name} is of the Chevalier, not of this ship; the boat is not sent" in e.text
    assert not w.dealings.boat.away and w.people.captain.hull == w.own.id
    # a name nobody of the game answers to is refused as before
    e = w.submit("send the boat to the Lynx with the captain and Mr Nobody")
    assert e.kind == "order.rejected" and "Nobody aboard answers to 'mr nobody'" in e.text
