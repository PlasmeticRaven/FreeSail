"""Package 109: the mends from the owner's play of 2026-11-12.

Step 1, the words that did nothing (notes 9, 4, 10 and the first half of 5): a free order is
accepted only where its words found a thing (or it writes one); where they matched nothing
it is refused in words that say what was not found and what the game does know by that
name. Words that are an order of the dialect go to the dialect ('take a sight for the
latitude', 'take possession', 'take command'), and one that names what happens of itself is
answered so ('open the gunports'). A thing is found by its listed name with or without its
state's words; two things of one name are named apart and taken by what tells them apart or
by 'the first', 'the second', 'the other'. The person's own keeping and the things lying
where he stands are a reading ('my keeping', 'what I have', 'inventory', 'the letters').

Each case is reproduced from a scenario on the trunk (the owner's saves are not here): the
Channel east in Brixham road, with the bilander given as the command line gives her.
Truths 7-540 onward are in `tests/test_known_truths.py`.
"""

from __future__ import annotations

import pytest

from freesail.world import things as TH
from freesail.world.scenarios import load_scenario, make_scenario_world

TORBAY = "data/scenarios/channel-east.yaml"
BILANDER = "data/ships/bilander.yaml"
WESTON = (
    'aboard: a letter from Mr Weston to the master, on the quarterdeck, sealed: "Proceed to '
    'Guernsey."'
)


def bilander():
    return make_scenario_world(load_scenario(TORBAY), ship=BILANDER)


def frigate():
    return make_scenario_world(load_scenario(TORBAY))


def refused(e) -> str:
    assert e.kind == "order.rejected", (e.kind, e.text)
    return e.data["reason"]


@pytest.mark.parametrize(
    "words",
    [
        "put Test Book on the table",
        "read the letter",
        "open the sea chest",
        "take the cutlass",
        "throw the empty bottle overboard",
        "give the chart to the mate",
        "examine the brandy",
    ],
)
def test_a_free_order_that_finds_nothing_is_refused_saying_what_was_not_found(words):
    """The owner: "it shouldn't accept an order that will do nothing at all." No free line
    that names nothing known is answered 'as said': it is refused, nothing journaled."""
    w = bilander()
    n = len(w.journal)
    why = refused(w.submit(words))
    assert "as said" not in why and "nothing of that name" in why.lower(), why
    assert "You keep nothing, and nothing lies here" in why, why
    assert len(w.journal) == n


def test_the_refusal_says_what_the_game_knows_by_that_name():
    """What is known: the things in his reach by their listed names, a thing gone over the
    side, a person not a thing, and an order of the dialect the words were near."""
    w = frigate()
    w.world_order("aboard: a sealed packet, on the quarterdeck, from the Custom House", "test")
    why = refused(w.submit("read the newspaper"))
    assert "lying here: a sealed packet" in why, why
    assert w.submit("take the packet").kind == "free.line"
    why = refused(w.submit("read the newspaper"))
    assert "in your keeping: a sealed packet" in why, why
    w.submit("throw the packet overboard")
    why = refused(w.submit("take the packet"))
    assert "the sealed packet went over the side" in why.lower(), why
    why = refused(w.submit("take posession of the renard"))
    assert "'take possession of'" in why, why


def test_an_order_with_a_thing_found_and_nothing_moved_is_said_as_before():
    """Where the words found a thing, the line is the world's as it was: shown, out of
    reach, or opened when it is no letter, 'as said' with its reason (the line stays)."""
    w = frigate()
    w.world_order("aboard: a sealed packet, in the hold, from the Custom House", "test")
    e = w.submit("take the packet")
    assert e.kind == "free.line" and "as said; nothing of the ship's changed" in e.text


@pytest.mark.parametrize(
    ("words", "kind"),
    [
        ("take a sight for the latitude", "navigation"),
        ("take a sight for latitude", "navigation"),
    ],
)
def test_words_of_the_dialect_go_to_the_dialect(words, kind):
    """'take a sight for the latitude' is the noon sight, the navigation's and not a free
    take of a thing called 'a sight'."""
    w = frigate()
    e = w.submit(words)
    assert e.kind != "free.line", e.text
    assert "nothing of that name" not in e.text


@pytest.mark.parametrize(
    ("words", "answer"),
    [
        ("open the gunports", "the ports open as the guns are run out"),
        ("open the ports", "the ports open as the guns are run out"),
        ("take a sight", "observe the sun"),
    ],
)
def test_words_naming_what_happens_of_itself_are_answered_so(words, answer):
    w = frigate()
    why = refused(w.submit(words))
    assert answer in why.lower() or answer in why, why


def test_take_command_of_the_prize_is_answered_by_its_road():
    """Package 109's case of 'take command' as it was (a refused phrase), kept beside package 60's
    order of those words: of a prize, the words are answered with possession's road."""
    w = frigate()
    why = refused(w.submit("take command of the prize"))
    assert "take possession of her" in why, why
    why = refused(w.submit("assume command of the prize"))
    assert "take possession of her" in why, why


def test_take_command_of_a_ship_his_to_take_is_package_60s_order():
    """Package 60 (the lead's reconciling of 2026-11-13): 'take command of her' aboard a ship
    given him is the order that changes his ship, not 109's refused phrase."""
    from tests.test_ship_changed import fly_taken_up

    w, fly, me, e = fly_taken_up()
    assert e.kind == "ship.taken_up" and w.players is w.hulls[str(fly.id)]


@pytest.mark.parametrize(
    "words",
    [
        "open the sealed letter from Mr Weston to the master",
        "open a sealed letter from Mr Weston to the master",
        "open the letter from Mr Weston to the master",
        "open the letter from Mr Weston",
        "open the letter from Weston",
        "open the letter to the master",
        "open Mr Weston's letter",
        "open the sealed letter",
        "break the seal of the letter from Mr Weston to the master",
    ],
)
def test_a_thing_is_found_by_its_listed_name_with_or_without_its_state(words):
    """The director's letter listed as 'a sealed letter from Mr Weston to the master' is
    taken by those words and by the words of it without its seal."""
    w = bilander()
    e = w.world_order(WESTON, "the director")
    assert e.data.get("result") != "refused", e.text
    (letter,) = TH.things_of(w)
    assert "a sealed letter from Mr Weston to the master" in w.submit("my keeping").text
    e = w.submit(words)
    assert e.kind == "free.line" and e.data["moved"], e.text
    assert letter.broken


def _two_letters(w):
    w.world_order(
        'aboard: a letter from the Admiralty to the captain, on the quarterdeck, sealed: "Cruise."',
        "test",
    )
    w.run(600)
    w.world_order(
        'aboard: a letter from Mr Gill to the captain, on the quarterdeck: "The stores are short."',
        "test",
    )
    return TH.things_of(w)


def test_two_things_of_one_name_are_named_apart_and_taken_by_what_tells_them_apart():
    """Two letters to the captain: 'open the letter to the captain' names both by their
    writers, their keeping and the first words of one not sealed, and nothing moves; the
    writer's name, 'the first', 'the second' and 'the other' each take one."""
    w = frigate()
    admiralty, gill = _two_letters(w)
    why = refused(w.submit("read the letter to the captain"))
    assert "two letters" in why and "the Admiralty" in why and "Mr Gill" in why, why
    assert "The stores are short" in why and "Cruise" not in why, why  # sealed words unseen
    assert "'the first'" in why, why
    e = w.submit("read the letter from Mr Gill")
    assert e.kind == "free.line" and e.data["thing"] == gill.id, e.text
    e = w.submit("open the first letter")
    assert e.kind == "free.line" and e.data["thing"] == admiralty.id, e.text
    e = w.submit("read the other letter")
    assert e.kind == "free.line" and e.data["thing"] == gill.id, e.text
    e = w.submit("read the second")
    assert e.kind == "free.line" and e.data["thing"] == gill.id, e.text
    e = w.submit("give the first letter to Mr Pearce")
    assert e.kind == "free.line" and e.data["thing"] == admiralty.id, e.text


@pytest.mark.parametrize(
    "words",
    [
        "the things",
        "what I have",
        "inventory",
        "my keeping",
        "what is in my keeping",
        "the letters",
        "what have I got",
    ],
)
def test_his_keeping_and_what_lies_here_is_a_reading(words):
    w = frigate()
    w.world_order("aboard: a sealed packet, on the quarterdeck, from the Custom House", "test")
    w.world_order("aboard: a snuffbox, on the quarterdeck", "test")
    w.submit("take the snuffbox")
    e = w.submit(words)
    assert e.kind.startswith("query."), (e.kind, e.text)
    assert "In your keeping: a snuffbox." in e.text, e.text
    assert "Lying here: a sealed packet." in e.text, e.text


# -- Step 2: the boat and the short watch (note 1) ------------------------------------------


def _anchored_bilander(watch_of_two: bool = True):
    """The bilander at anchor in Brixham road; with `watch_of_two`, run on into the morning
    watch, when her larboard watch of two has the deck (the owner's case)."""
    w = bilander()
    w.submit("let go the anchor")
    w.run(7800 if watch_of_two else 600)
    return w


def _since(w, n):
    return [e for e in list(w.log)[n:]]


def test_the_watch_too_few_to_send_the_boat_calls_all_hands_and_pipes_down():
    """On the trunk 'go ashore' in the morning watch waited two hours ("Not hands enough on
    deck to send boat; there are but two to spare") and he sat in the boat. Now all hands
    are called for her, she is manned and hoisted out, and the hands are piped down."""
    w = _anchored_bilander()
    n = len(w.log)
    assert w.submit("go ashore").kind == "order.accepted"
    w.run(1200)
    kinds = [e.kind for e in _since(w, n)]
    assert "evolution.waiting" not in kinds
    called = next(e for e in _since(w, n) if e.kind == "crew.all_hands")
    assert called.text == "All hands! (to send boat)"
    assert kinds.index("crew.all_hands") < kinds.index("crew.piped_down")
    assert kinds.index("crew.piped_down") <= kinds.index("evolution.started")
    assert "boat.away" in kinds
    crew = w.ship.extra["crew"]
    assert not crew.all_hands_called


def test_the_boat_at_the_side_is_belayed_from_her_and_he_is_on_deck_again():
    """A person in the boat that has not left the ship's side may belay her ('belay that',
    'belay the boat'), and is on deck again; once she has left the side, he may not."""
    for words in ("belay that", "belay the boat"):
        w = _anchored_bilander(watch_of_two=False)
        w.submit("go ashore")
        cap = w.people.captain
        assert cap.where == "boat"
        e = w.submit(words)
        assert e.kind == "work.belayed", (words, e.text)
        w.run(120)
        assert cap.aboard and cap.where in ("deck", "quarterdeck"), cap.where
        stood = [e for e in w.log if e.kind == "boat.stood_down"]
        assert stood and "Mr Bowen on deck again" in stood[-1].text
    w = _anchored_bilander(watch_of_two=False)
    w.submit("go ashore")
    w.run(900)
    assert w.dealings.boat.phase != "hoisting out"
    assert w.submit("belay that").kind == "order.rejected"
