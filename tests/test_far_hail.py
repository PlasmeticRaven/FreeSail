"""A far hull's hail goes to her captain's model (package 82b, item 3; `Design-DoorAndVisitor.md`
§4).

Two hulls at far detail, fifteen miles from the frigate and a cable apart, a model (a fake)
at each captain's station. The brig's captain hails the cutter: the cutter's hull hears it in
her log and her captain's sample carries it, nothing answers by table, and the brig's log
says she has not yet answered; the cutter's captain answers with his own hail and the brig's
log carries his words. A ship nobody holds is answered by table, far or full, as before. The
passage replays by both roads to the same logs.
"""

from __future__ import annotations

import json

from freesail.agents import Fake, Harness, SamplingPolicy, call
from freesail.agents.agent import captain as captain_station
from freesail.agents.model import Reply
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.world import crews as K
from freesail.world import hail as H
from tests.test_between_hulls import _run_until
from tests.test_crews import hove_to_world

ANSWER = "His Majesty's cutter Bess, from Falmouth"


def _hailer():
    """The brig's captain: he hails the cutter at his first sample, and notes after."""
    state = {"hailed": False}

    def act(last, turns):
        if not state["hailed"]:
            state["hailed"] = True
            return Reply(calls=(call("submit_order", text="hail the Bess: what ship is that?"),))
        return Reply(text="Aye.")

    return act


def _answerer(seen):
    """The cutter's captain: he answers a hail heard in his sample with his own, once."""
    state = {"answered": False}

    def act(last, turns):
        words = json.dumps(last)
        if "hails us" in words:
            seen.append(words)
            if not state["answered"]:
                state["answered"] = True
                return Reply(calls=(call("submit_order", text=f"hail the brig: {ANSWER}"),))
        return Reply(text="Aye.")

    return act


def _seat(crew, act):
    policy = SamplingPolicy.in_lockstep(600, "notable", "urgent")
    h = Harness(crew, captain_station(policy, 3600, world=crew), Fake([act], loop=True))
    h.model_name, h.door = "the fake", "runner"
    h.start()
    return h


def two_far_hulls(held: bool = True):
    """The brig Anna and the cutter Bess, a cable apart and fifteen miles off, hove to by
    the director's hand, each hull asleep with a fake at her captain's station (the cutter's
    only when `held`); the cutter's samples that heard a hail."""
    w = hove_to_world()
    for words in (
        'ship: a merchant brig "Anna" of Britain at 49 45 N 5 30 W, bound for Falmouth',
        'ship: a cutter "Bess" of Britain at 49 45.1 N 5 30 W, bound for Falmouth',
        'ship "Anna": intent bound for Falmouth',
        'ship "Bess": intent bound for Falmouth',
        'ship "Anna": order heave to for a watch',
        'ship "Bess": order heave to for a watch',
    ):
        e = w.world_order(words)
        assert e.data.get("result") == "done", e.text
    w.run(61)
    a, b = w.vessels.find("Anna"), w.vessels.find("Bess")
    seen: list[str] = []
    _, cb = K.station_world(w, "Bess")
    hb = _seat(cb, _answerer(seen)) if held else None
    # a minute before the brig's (who hails at once): the transcript road seats the hulls'
    # stations of one tick in the hulls' order, not the play's (found on the way, 82b)
    w.run(60)
    _, ca = K.station_world(w, "Anna")
    ha = _seat(ca, _hailer())
    return w, a, b, ha, hb, seen


def _kinds(log, kind):
    return [e for e in log if e.kind == kind]


def hail_and_answer():
    """The passage: the hail, unanswered by table, and the model's answer heard."""
    w, a, b, ha, hb, seen = two_far_hulls()
    _run_until(w, lambda: _kinds(a.crew.log, "hail.made"), 0.5)
    assert a.crew.shape == "far" and b.crew.shape == "far"
    assert H.model_holds_her(a.crew) and H.model_holds_her(b.crew)
    # heard in her log, urgent, and nothing answered by table on either side
    heard = _kinds(b.crew.log, "hail.heard")
    assert heard and "what ship is that?" in heard[0].text
    assert not _kinds(b.crew.log, "hail.answered") and not _kinds(a.crew.log, "hail.answered")
    # the hailer's log: she has not yet answered
    made = [e for e in a.crew.log if "Hailed" in e.text and "not yet answered" in e.text]
    assert made, [e.text for e in a.crew.log if "Hailed" in e.text]
    # her captain's sample carries it, and his answer reaches the hailer
    _run_until(w, lambda: _kinds(a.crew.log, "hail.heard"), 1.0)
    assert seen and "what ship is that?" in seen[0]
    back = _kinds(a.crew.log, "hail.heard")
    assert ANSWER in back[0].text and "hails us" in back[0].text
    assert a.crew.shape == "far" and b.crew.shape == "far"
    assert not _kinds(a.crew.log, "hail.answered") and not _kinds(b.crew.log, "hail.answered")
    return w, a, b


def test_a_far_hulls_hail_goes_to_her_captains_model_and_his_answer_to_the_hailer():
    hail_and_answer()


def test_a_ship_nobody_holds_is_answered_by_table_far_or_full():
    w, a, b, ha, hb, seen = two_far_hulls(held=False)
    assert b.crew.shape == "far" and not H.model_holds_her(b.crew)
    _run_until(w, lambda: _kinds(a.crew.log, "hail.made"), 0.5)
    answered = _kinds(a.crew.log, "hail.answered")
    assert answered and "Bess" in answered[0].text  # her table's words, as before


def test_the_hail_between_two_far_hulls_replays_by_both_roads_to_the_same_logs():
    w, a, b = hail_and_answer()
    data = json.loads(json.dumps(w.save()))
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == w.log.digest(), road
        for v in (a, b):
            assert copy.hulls[v.crew.id].log.digest() == v.crew.log.digest(), (road, v.name)
        back = _kinds(copy.hulls[a.crew.id].log, "hail.heard")
        assert back and ANSWER in back[0].text, road
