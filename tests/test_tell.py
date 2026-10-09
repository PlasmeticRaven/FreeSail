"""`tell the <station> ...` (package 29, the owner's tenth item, 2026-09-28): a way to
address a station that is not a question. Journaled as an order like `ask`, logged "The
captain to the watcher: <words>" (`agent.told`, notable), the words carried by the model's
next sample under `word` (reason "a word from the captain"), never under `question`, so
no answer is owed and nothing that waits on an answer is set. Every case against the
scripted fake, never a model.
"""

from __future__ import annotations

from typing import Any

import pytest

from freesail.agents import Fake, Harness, Reply, SamplingPolicy, Station, call, reply
from freesail.agents.agent import WATCHER_BRIEF, Authority
from freesail.agents.harness import A_WORD, ANSWER_UNASKED
from freesail.agents.model import DATA
from freesail.agents.repl import render_turn
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.core.events import Severity
from freesail.core.world import Scenario, World

EVERY = 600  # sampled every ten minutes (tests/test_agents.py's short station)
WORDS = "we make for Falmouth; keep an eye on the glass"


def point_world() -> World:
    """The frigate in a steady wind (the point ship has no order channel for stations)."""
    from freesail.api.session import make_world

    return make_world(
        7,
        "data/ships/frigate-36.yaml",
        Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0),
    )


def station() -> Station:
    return Station(
        "watcher",
        Authority.NONE,
        SamplingPolicy.in_lockstep(EVERY, "notable", "urgent"),
        1800,
        WATCHER_BRIEF,
    )


def stationed(world: World, script, **kw) -> tuple[Harness, Fake]:
    fake = Fake(script, **kw)
    h = Harness(world, station(), fake, save=lambda w, why: None)
    h.start()
    return h, fake


def samples(fake: Fake) -> list[dict[str, Any]]:
    """Every sample the fake was shown, in order, without repeats."""
    seen: list[dict[str, Any]] = []
    for turns in fake.seen:
        for t in turns:
            if t.role == DATA and "readings" in t.content and not any(t.content is s for s in seen):
                seen.append(t.content)
    return seen


def test_tell_is_an_order_journaled_and_logged_notable():
    world = point_world()
    h, _ = stationed(world, ["Aye."], loop=True)
    world.run(30)
    e = world.submit(f"tell the watcher {WORDS}")
    assert e.kind == "agent.told" and e.severity is Severity.NOTABLE
    assert e.text == f"The captain to the watcher: {WORDS}"
    assert world.journal[-1] == (30, "captain", f"tell the watcher {WORDS}")
    assert h.agent.word == WORDS and h.agent.question is None
    said = world.submit("say to the watcher all is well")
    assert said.kind == "agent.told" and said.text == "The captain to the watcher: all is well"


def test_a_tell_to_nobody_is_kept_and_passed_and_one_with_no_words_is_refused():
    """Package 37l (the review of gate 5c's playtests, G17: "a `tell` to an unmanned
    station is rejected and its words are lost"): the captain's word to a station nobody
    holds is kept in its journal and said so in the log, and passed to whoever takes the
    station in its first sample, once; a word with no words is refused as before."""
    world = point_world()
    e = world.submit("tell the watcher hello")
    assert e.kind == "agent.told", e.text
    assert e.text == (
        "The captain to the watcher: hello (nobody holds the station; the words are kept in "
        "its journal for whoever takes it)"
    )
    assert world.journal == [(0, "captain", "tell the watcher hello")]
    h, fake = stationed(world, ["Aye."])
    first = samples(fake)[0]
    assert first["word"] == "The captain's word, kept for whoever takes the station: hello"
    kinds = [x.kind for x in h.journal.entries]
    assert kinds[:2] == ["agent.word_kept", "agent.word_passed"]
    assert h.journal.kept_words() == []
    e = world.submit("tell the watcher")
    assert e.kind == "order.rejected" and "Tell the watcher what?" in e.text
    # a replay writes the same journal and gives the same log
    copy = replay.replay(world.save(), ship_factory)
    assert copy.log.digest() == world.log.digest()


def test_the_word_rides_the_next_sample_under_its_own_key_and_a_text_reply_ends_the_turn():
    """Case 1: text only. The sample is taken at the next tick, reason "a word from the
    captain", the words under `word` and no `question`; a reply of text lands as the
    watcher's line and ends the turn; the word is not put again."""
    world = point_world()
    h, fake = stationed(world, ["Aye.", "Noted, Falmouth it is.", "All quiet."])
    world.run(60)
    calls = fake.calls
    world.submit(f"tell the watcher {WORDS}")
    assert fake.calls == calls, "not sampled on the order itself: at the next tick"
    world.tick()
    assert fake.calls == calls + 1
    s = samples(fake)[-1]
    assert s["reason"] == A_WORD and s["word"] == WORDS
    assert s["question"] is None
    assert "[watcher] Noted, Falmouth it is." in [e.text for e in world.log]
    assert h.open_sample is None and h.agent.word is None and h.agent.question is None
    world.run(EVERY)  # the next sample is the policy's, with no word in it
    later = samples(fake)[-1]
    assert later["reason"] != A_WORD and "word" not in later


def test_a_stand_by_in_answer_to_a_word_ends_the_turn_at_once():
    """Case 2: the model stands by. The turn ends, the stand-by is logged, and the word is
    not put again when it ends."""
    world = point_world()
    h, fake = stationed(world, ["Aye.", call("stand_by", until="eight bells"), "Up."])
    world.run(60)
    world.submit(f"tell the watcher {WORDS}")
    world.tick()
    assert h.agent.standing_by and h.open_sample is None
    assert [e.text for e in world.log if e.kind == "agent.stood_by"] == [
        "[watcher] Standing by until eight bells."
    ]
    world.run(4 * 3600)
    assert not any(s.get("word") for s in samples(fake)[2:])


def test_an_answer_given_anyway_is_logged_as_said():
    """Case 3: the model answers though nothing was asked: its words are heard in the log as
    `agent.said`, and the tool says the words are in the log though no question was put."""
    world = point_world()
    h, fake = stationed(world, ["Aye.", reply("", call("answer", text="Falmouth, aye.")), ""])
    world.run(60)
    world.submit(f"tell the watcher {WORDS}")
    world.tick()
    said = [e for e in world.log if e.kind == "agent.said"]
    assert [e.text for e in said] == ["[watcher] Falmouth, aye."]
    assert said[0].data["question"] is None
    results = [t.content for t in h.turns if t.role == DATA and "tool_results" in t.content]
    assert results[-1]["tool_results"][0]["result"] == ANSWER_UNASKED


def test_a_tell_and_an_ask_at_once_ride_one_sample():
    """Case 4: `tell` and then `ask` on the same tick: the ask's sample, taken on its order,
    carries both, the word under `word` and the question under `question`."""
    world = point_world()

    def answer_it(last, turns):
        if last.get("question"):
            return reply("", call("answer", text=f"Aye; {last['question']}: nothing yet."))
        return Reply()

    h, fake = stationed(world, [answer_it], loop=True)
    world.run(60)
    world.submit(f"tell the watcher {WORDS}")
    world.submit("ask the watcher whether the glass is falling")
    both = [s for s in samples(fake) if s.get("word") and s.get("question")]
    assert len(both) == 1
    assert both[0]["word"] == WORDS
    assert both[0]["question"] == "whether the glass is falling"
    assert both[0]["reason"] == "a question"
    world.run(5)
    assert sum(1 for s in samples(fake) if s.get("word")) == 1, "the word is carried once"
    assert [e.text for e in world.log if e.kind == "agent.said"] == [
        "[watcher] Aye; whether the glass is falling: nothing yet."
    ]


def test_a_tell_wakes_a_stand_by():
    world = point_world()
    h, fake = stationed(world, [call("stand_by", until="eight bells"), "Aye, Falmouth."])
    world.run(120)
    assert h.agent.standing_by
    world.submit(f"tell the watcher {WORDS}")
    world.tick()
    assert not h.agent.standing_by
    assert [e.text for e in world.log if e.kind == "agent.resumed"] == [
        "[watcher] A word from the captain; the watcher is sampled again."
    ]
    s = samples(fake)[-1]
    assert s["reason"] == A_WORD and s["word"] == WORDS
    assert s["stood_by"]["until"] == "eight bells"


def test_a_word_to_a_turn_already_open_is_folded_in():
    """A door that answers late (the floor the model's): the word is folded into the open
    sample at the next tick, never as a question."""
    world = point_world()
    replies: list[Reply | None] = [None, None, None]
    fake = Fake([lambda last, turns: replies.pop(0) if replies else Reply()], loop=True)
    h = Harness(world, station(), fake, save=lambda w, why: None)
    h.start()
    assert h.open_sample is not None
    world.submit(f"tell the watcher {WORDS}")
    world.tick()
    assert h.open_sample.word == WORDS and h.open_sample.question is None
    folded = [t.content for t in h.turns if t.role == DATA and t.content.get("folded")]
    assert folded and folded[-1]["word"] == WORDS


def test_the_bridge_and_the_repl_show_the_word():
    """The MCP bridge renders a sample with the REPL's `render_turn`; the runner sends the
    sample as JSON, `word` and all."""
    world = point_world()
    h, fake = stationed(world, ["Aye.", "Aye."])
    world.run(60)
    world.submit(f"tell the watcher {WORDS}")
    world.tick()
    turn = next(t for t in reversed(h.turns) if t.role == DATA and t.content.get("word"))
    assert f"The captain tells you: {WORDS}" in render_turn(turn)
    assert "The captain asks" not in render_turn(turn)


def test_a_game_with_a_tell_replays_to_the_same_digest(tmp_path):
    from freesail.api.session import make_world

    world = make_world(
        7,
        "data/ships/frigate-36.yaml",
        Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0),
    )
    stationed(world, ["Aye.", "Noted.", "Quiet."], loop=True)
    world.submit("set plain sail")
    world.run(300)
    world.submit(f"tell the watcher {WORDS}")
    world.run(EVERY)
    world.submit("tell the watcher all is well")
    world.submit("ask the watcher how she goes")
    world.run(120)
    data = replay.load_file(replay.save_to_file(world, tmp_path / "told.json"))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert [e.text for e in copy.log if e.kind == "agent.told"] == [
        f"The captain to the watcher: {WORDS}",
        "The captain to the watcher: all is well",
    ]


@pytest.mark.parametrize("words", ["tell the watcher", "say to the watcher"])
def test_the_vocabulary_knows_tell(words):
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    verb = vocab.phrase_to_verb[words]
    assert vocab.verbs[verb].object == "station"


# ---------------------------------------------------------------------------
# A standing order tells and asks (package 31c; the owner's finding at gate 5a)
# ---------------------------------------------------------------------------

SEA = 'standing order "sea": every 10 minutes then tell the watcher the sea is getting up'


def test_a_standing_order_tells_the_watcher_as_the_captain_would_and_the_log_names_it():
    """The word is delivered as the captain's own is, under `word`, no answer owed; the
    log line names the standing order as the speaker, in the name of the officer who gave
    it; the firing's own line is as every firing's."""
    world = point_world()
    world.submit(SEA)
    world.submit(
        'standing order "glass" by the master: every 10 minutes then say to the watcher mind '
        "the glass"
    )
    h, fake = stationed(world, ["Aye.", "Noted.", "Noted."], loop=True)
    world.run(EVERY)
    told = [e for e in world.log if e.kind == "agent.told"]
    assert [(e.actor, e.text, e.severity) for e in told] == [
        (
            "standing order 'sea'",
            "By standing order 'sea': the captain to the watcher: the sea is getting up",
            Severity.NOTABLE,
        ),
        (
            "standing order 'glass'",
            "By standing order 'glass': the master to the watcher: mind the glass",
            Severity.NOTABLE,
        ),
    ]
    assert told[0].data == {
        "station": "watcher",
        "words": "the sea is getting up",
        "by": "standing order 'sea'",
    }
    fired = [e.text for e in world.log if e.kind == "order.accepted"]
    assert "By standing order 'sea': telling the watcher the sea is getting up." in fired
    s = samples(fake)[-1]
    assert s["reason"] == A_WORD and s["word"] == "the sea is getting up\nmind the glass"
    assert s["question"] is None
    assert world.journal[-2:] == [
        (0, "captain", SEA),
        (
            0,
            "captain",
            'standing order "glass" by the master: every 10 minutes then say to the watcher '
            "mind the glass",
        ),
    ], "the firings are not journaled; the orders that gave them are"
    # the captain's own word is logged as it always was, in the same tick as a firing
    world.run(EVERY - 1)
    e = world.submit("tell the watcher all is well")
    assert e.text == "The captain to the watcher: all is well" and "by" not in e.data


def test_a_standing_order_asks_and_the_question_is_sampled_once():
    """A standing order's `ask` is put as the captain's own is, answered at once; the
    firing's line is notable, and the sample that carried the question has carried it, so
    no second sample is taken for it (package 31c)."""
    world = point_world()
    world.submit('standing order "q": every 5 minutes then ask the watcher how the glass stands')

    def answer_it(last, turns):
        if last.get("question"):
            return reply("", call("answer", text="Steady at thirty."))
        return Reply()

    h, fake = stationed(world, [answer_it], loop=True)
    before = len(samples(fake))
    world.run(EVERY - 1)  # the question at 300; the station's own interval at 600
    asked = [e for e in world.log if e.kind == "agent.asked"]
    assert [e.text for e in asked] == [
        "By standing order 'q': the captain asks the watcher: how the glass stands?"
    ]
    new = samples(fake)[before:]
    assert [s["reason"] for s in new] == ["a question"], [s["reason"] for s in new]
    assert new[0]["question"] == "how the glass stands"
    assert [e.text for e in world.log if e.kind == "agent.said"] == ["[watcher] Steady at thirty."]


def test_a_standing_orders_word_to_a_station_nobody_mans_is_refused_when_it_fires():
    """Given before the watcher takes the station (a book read at the start), the order
    stands; a firing while nobody mans it is refused in words, as the captain's would be."""
    world = point_world()
    e = world.submit(SEA)
    assert e.kind == "standing.given", e.text
    world.run(EVERY)
    (refused,) = [e for e in world.log if e.kind == "order.rejected"]
    assert refused.actor == "standing order 'sea'"
    assert "There is no watcher at the station; nobody has been stationed there." in refused.text
    stationed(world, ["Aye.", "Noted."], loop=True)
    world.run(EVERY)
    assert [e.text for e in world.log if e.kind == "agent.told"] == [
        "By standing order 'sea': the captain to the watcher: the sea is getting up"
    ]


def test_a_game_with_a_standing_orders_word_replays_to_the_same_digest(tmp_path):
    world = point_world()
    world.submit(SEA)
    world.submit('standing order "q": every 20 minutes then ask the watcher how she goes')
    stationed(world, ["Aye.", reply("", call("answer", text="Well.")), "Noted."], loop=True)
    world.run(3 * EVERY)
    data = replay.load_file(replay.save_to_file(world, tmp_path / "book.json"))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert [e.text for e in copy.log if e.kind == "agent.told"] == [
        e.text for e in world.log if e.kind == "agent.told"
    ]
    assert len([e for e in copy.log if e.kind == "agent.told"]) == 3
