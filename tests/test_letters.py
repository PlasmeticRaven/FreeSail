"""Package 100: letters and things as one system (the owner's play of 2026-11-09, note 8).

Step 1, the thing with words: a letter is a thing with words, an author, an addressee and a
seal, written by the drafting's road and carried, handed, put down and hidden as any thing
is; sealed and opened (a broken seal shows); read where it is in reach by the one who reads
it, its words shown to him and to nobody else; destroyed by the player's act (burnt, torn up,
thrown overboard); made with its words and removed by the director's form; a thing looked
at shown with its description. One road for the player, a station and the director.
Truths 7-470 to 7-479 are in `tests/test_known_truths.py`.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import for_the_record
from freesail.core.world import Scenario
from freesail.world import knowledge
from freesail.world import things as TH

FRIGATE = "data/ships/frigate-36.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}
OFFICER = "officer of the watch"
WORDS = "I have the honour to report the Harpy in sight off the Lizard."


def world_for(**kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=OFF_THE_LIZARD,
        region="channel-west",
        **kw,
    )
    return make_world(7, FRIGATE, sc)


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


def _written(w, words=WORDS, to="the port admiral"):
    e = w.submit(f'write a letter to {to}: "{words}"')
    assert e.kind == "free.line" and e.data["moved"], e.text
    return TH.things_of(w)[-1]


def _senses_of(w, person):
    return knowledge.senses_of(w, person)


def test_a_letter_is_written_by_the_draftings_road_into_the_writers_keeping():
    """`write a letter to <whom>: "<words>"`: the captain on deck goes below to his table
    and is at his writing, as a book's drafting has him; the letter, a thing with its words,
    its writer, its addressee and the hour, is in his keeping; the order and the free line
    say it without its words, which are shown the writer alone."""
    from freesail.world.people import WRITING

    w = world_for()
    cap = w.people.captain
    letter = _written(w)
    assert (letter.name, letter.words, letter.author, letter.to) == (
        "a letter to the port admiral",
        WORDS,
        cap.name,
        "the port admiral",
    )
    assert letter.keeper == cap.id and letter.is_letter and letter.head == "letter"
    assert letter.written.startswith("10 June") and not letter.sealed
    assert cap.where == "cabin" and cap.occupied_with == WRITING
    below = events(w, "captain.below")[-1]
    line = events(w, "free.line")[-1]
    assert line.text == (
        "By the captain, in the cabin: wrote a letter to the port admiral; the letter is in "
        "the captain's keeping."
    )
    accepted = [e for e in events(w, "order.accepted") if "letter" in e.text][-1]
    assert accepted.text == "Order: write a letter to the port admiral."
    assert below.tick == line.tick
    # the words: in no line but the writer's own, and in no data of the free line
    with_words = [e for e in w.log.all() if WORDS in e.text]
    assert [e.kind for e in with_words] == ["free.written"]
    assert with_words[0].text == f'Your letter to the port admiral, as written: "{WORDS}"'
    assert WORDS not in str(line.data) and WORDS not in str(accepted.data)
    assert "author" in letter.to_dict() and "words" not in letter.to_dict()
    # the journal keeps the order whole, for the replay
    assert any(WORDS in t for _, _, t in w.journal)
    # the people's words list it as any thing kept
    assert "a letter to the port admiral in his keeping" in w.readings.words("people")
    # refused in words where it says no addressee or no words
    assert "Say the words after 'write a letter'" in w.submit("write a letter").text
    for bad in ("write a letter to the admiral", 'write: "nothing"'):
        e = w.submit(bad)
        assert e.kind == "order.rejected" and "write a letter to <whom>" in e.text, bad


def test_a_sealed_letter_is_read_only_by_breaking_its_seal_which_shows():
    """Sealed, a letter is not read but by breaking its seal (`open`, `break the seal of`),
    which shows ever after wherever it is listed; no new seal hides it."""
    w = world_for()
    letter = _written(w)
    e = w.submit("seal the letter")
    assert e.text.endswith("sealed the letter; the letter to the port admiral is sealed.")
    assert letter.sealed and TH.name_words(letter) == "a sealed letter to the port admiral"
    e = w.submit("read the letter")
    assert not e.data["moved"] and "is read only by breaking its seal" in e.text
    assert not events(w, "free.read")
    e = w.submit("seal the letter")
    assert "is sealed already" in e.text
    e = w.submit("break the seal of the letter")
    assert e.text.endswith("the seal of the letter to the port admiral is broken, and it shows.")
    assert letter.broken
    assert TH.name_words(letter) == "a letter to the port admiral with its seal broken"
    assert "with its seal broken in his keeping" in w.readings.words("people")
    e = w.submit("seal the letter")
    assert "no new seal hides it" in e.text and letter.broken
    e = w.submit("read the letter")
    assert e.data["moved"] and e.text.endswith(
        "read the letter; the letter to the port admiral read."
    )
    read = events(w, "free.read")[-1]
    assert read.text.startswith("The letter to the port admiral, in ")
    assert read.text.endswith(f'"{WORDS}"') and read.data["to"] == w.people.captain.name


def test_a_letters_words_reach_its_reader_and_nobody_else():
    """The free line of a reading is heard where it is said; the words are a line of the
    reach `reader`, the reader's and nobody else's, a station within earshot never shown them
    and the director, who has everything, shown them. A station's person who takes the
    letter and reads it is shown them, and the player is not."""
    from freesail.agents import tools
    from tests.test_orders_places import seat

    w = world_for()
    h = seat(w, OFFICER)
    officer = w.stations.holder(OFFICER)
    cap = w.people.captain
    letter = _written(w)
    w.submit("come on deck")
    e = w.submit("read the letter")
    assert e.data["heard_by"] == [OFFICER] and h.agent.heard[-1] == e.text
    assert WORDS not in " ".join(h.agent.heard)
    read = events(w, "free.read")[-1]
    assert not h._reaches(read)
    assert knowledge.hears(w, _senses_of(w, cap), read)  # the player's, at the prompt
    assert knowledge.reaches(w, knowledge.EVERYTHING, read)  # the director's
    for p in w.people.all:
        if p is not cap:
            assert not knowledge.reaches(w, _senses_of(w, p), read), p.name
    # handed to the held officer it lies before him; his own hand takes it and reads it
    e = w.submit(f"give the letter to {officer.name}")
    assert f"lies before {officer.name}" in e.text
    said = tools.call(w, OFFICER, "submit_order", {"text": "take the letter"})
    assert said.endswith(f"the letter to the port admiral is in {officer.name}'s keeping.")
    tools.call(w, OFFICER, "submit_order", {"text": "read the letter"})
    theirs = events(w, "free.read")[-1]
    assert theirs.data["to"] == officer.name and h._reaches(theirs)
    assert not knowledge.hears(w, _senses_of(w, cap), theirs)
    assert letter.keeper == officer.id


def test_a_paper_burnt_or_torn_up_is_gone_and_said_and_a_thing_that_is_no_paper_is_not():
    """Burnt or torn up a paper within reach is gone, and the line says so; the people's
    words and the places' have it no longer, and no verb finds it; a cask is no paper, and a
    thing out of reach is not destroyed. Thrown overboard a letter goes with the rest."""
    w = world_for()
    letter = _written(w)
    e = w.submit("burn the letter")
    assert e.text.endswith("burnt the letter; the letter to the port admiral is burnt, and gone.")
    assert (letter.place, letter.gone, letter.keeper) == (TH.GONE, "burnt", "")
    assert TH.find(w, "the letter") == []
    assert "letter" not in w.readings.words("people")
    assert w.readings.value("people")["things"] == ["a letter to the port admiral, burnt"]
    assert not w.submit("read the letter").data["moved"]
    second = _written(w, "A second word.", "Mr Veale")
    e = w.submit("tear up the letter")
    assert e.text.endswith("tore up the letter; the letter to Mr Veale is torn up, and gone.")
    assert second.gone == "torn up"
    third = _written(w, "A third.", "the agent")
    e = w.submit("throw the letter overboard")
    assert e.text.endswith("the letter to the agent went over the side.")
    assert third.place == TH.OVERBOARD
    w.world_order("aboard: a cask of brandy, in the cabin", "the test")
    e = w.submit("burn the cask")
    assert not e.data["moved"] and "is no paper to burn; throw it overboard" in e.text
    w.world_order("aboard: a sealed packet, in the hold", "the test")
    e = w.submit("burn the packet")
    assert not e.data["moved"] and "the sealed packet is in the hold" in e.text


def test_a_thing_looked_at_is_shown_with_its_description_and_a_letter_never_its_words():
    """`look at`, `examine`: a thing as anyone there sees it, its name, its description and
    where it lies; a letter its direction, its hand and its seal, never its words."""
    w = world_for()
    w.world_order("aboard: a sealed packet, on the quarterdeck, from the Custom House", "the test")
    e = w.submit("look at the packet")
    assert e.data["moved"] and e.text == (
        "By the captain, on the quarterdeck: looked at the packet; a sealed packet, from the "
        "Custom House; on the quarterdeck."
    )
    assert w.submit("examine the brandy").text.endswith("as said; nothing of the ship's changed.")
    letter = _written(w)
    w.submit("seal the letter")
    e = w.submit("inspect the letter")
    assert "a letter to the port admiral, in " in e.text and ", sealed;" in e.text
    assert WORDS not in e.text and letter.sealed
    # a thing that is no letter is opened and read as it always was: nothing moves
    for words in ("open the packet", "read the packet"):
        e = w.submit(words)
        assert e.text.endswith("as said; nothing of the ship's changed.")


def test_the_director_makes_a_letter_with_its_words_and_removes_a_thing_by_the_rule_of_reach():
    """`aboard: a letter from <whom> to <whom>, <where>[, sealed]: "<words>"` makes a letter
    with its words and none of them in the play log; `aboard: remove <a thing>` takes one out
    of the world, refused out of a held person's keeping and doubted before his eyes."""
    from freesail.world import orders as WO

    w = world_for()
    e = w.world_order(
        'aboard: a letter from the agent to the captain, on the cabin table, sealed: "Your cargo '
        'waits at the quay, sir."',
        "the test",
    )
    assert e.data["result"] == "done", e.text
    letter = TH.things_of(w)[-1]
    assert (letter.author, letter.to, letter.sealed, letter.place, letter.spot) == (
        "the agent",
        "the captain",
        True,
        "cabin",
        "on the table",
    )
    assert (
        letter.to_id == w.people.captain.id and letter.words == "Your cargo waits at the quay, sir."
    )
    assert not [e for e in w.log.all() if "cargo waits" in e.text and not for_the_record(e)]
    assert "In the cabin: a sealed letter from the agent to the captain on the table." in (
        w.readings.words("places")
    )
    w.submit("go below")
    w.submit("open the letter")
    w.submit("read the letter")
    read = events(w, "free.read")[-1]
    assert read.text == (
        'The letter from the agent to the captain: "Your cargo waits at the quay, sir."'
    )
    # removed: out of the held captain's keeping refused; lying before him, doubted
    w.submit("take the letter")
    e = w.world_order("aboard: remove the letter", "the test")
    assert e.data["result"] == "refused" and "held person's keeping" in e.text
    w.submit("put the letter on the table")
    o = WO.parse("aboard: remove the letter")
    assert "who would see it go by no hand" in WO.doubt(w, o)
    w.world_order("aboard: a cask of brandy, in the hold", "the test")
    assert WO.doubt(w, WO.parse("aboard: the cask removed")) is None
    e = w.world_order("aboard: the cask removed", "the test")
    assert e.data["result"] == "done" and TH.find(w, "the cask") == []
    assert all(t.name != "a cask of brandy" for t in TH.things_of(w))
    e = w.world_order("aboard: remove the chronometer", "the test")
    assert e.data["result"] == "refused" and "no thing answering to" in e.text


def test_a_passage_with_letters_written_sealed_read_and_burnt_replays_to_the_same_log():
    """Every act of a letter is an order journaled, so a replay writes, seals, reads and
    burns it again at its tick: the same things and the same digest."""
    w = world_for()
    _written(w)
    w.run(600)
    w.submit("seal the letter")
    w.submit("give the letter to the master")
    w.world_order(
        'aboard: a letter from Mr Veale to the master, on the quarterdeck: "Ask at the Ship."',
        "the test",
    )
    w.run(300)
    w.submit("come on deck")
    w.submit("read the letter from Mr Veale")
    w.submit("burn the letter from Mr Veale")
    w.run(120)
    back = replay.replay_world(w, ship_factory)
    assert [t.to_dict() for t in TH.things_of(back)] == [t.to_dict() for t in TH.things_of(w)]
    assert [t.words for t in TH.things_of(back)] == [t.words for t in TH.things_of(w)]
    assert back.log.digest() == w.log.digest()


@pytest.mark.parametrize("verb", ["write", "seal", "examine", "burn", "tear up"])
def test_the_new_verbs_are_free_lines_and_the_director_has_no_hands(verb):
    """The verbs of a thing with words are free lines, every station's but the director's."""
    from freesail.orders.vocabulary import load_vocabulary
    from tests.test_director import directed

    vocab = load_vocabulary()
    assert verb in vocab.free_lines and vocab.verbs[verb].object == "free"
    d = directed()
    e = d.submit(f"{verb} the packet", actor="the director")
    assert e.kind == "order.rejected" and "no hands aboard" in e.text
