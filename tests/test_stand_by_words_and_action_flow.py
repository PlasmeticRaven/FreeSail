"""The stand-by's words, and the action's severities (the model officer's first, fourth
and fifth friction points of the playtests of packages 70 to 72).

A reply that batches calls before a `stand_by` had every call of the reply answered "Not
run: a stand-by earlier in the reply ended your turn" at the doors, the orders that ran
before the stand-by among them; now the harness keeps those calls' results on the turn
(`Reply.ran`), the doors answer them with what they returned, and "not run" is said only
of the calls after the stand-by. In action at 1x every minute's fire woke a stand-by on 'a
notable event': the discharges' minute line is routine unless a shot struck her or the fire
opened, and at quarters the trimmers' yard-by-yard lines are routine, a trim's one line for
all of them and the sails' lines notable as before. The signal book in the papers says
whose it is (this ship's own by her service), and the common book of no nation says it is
no other ship's.
"""

from __future__ import annotations

import json

from freesail.agents.model import MODEL, Reply
from freesail.core.events import Severity
from tests.test_agents import call, frigate_world, point_world, reply, stationed
from tests.test_local_runner import A_GLASS_S, llama, model_for


def test_the_calls_before_a_stand_by_are_answered_with_their_results_at_the_doors():
    """A journal note and a readings read before the stand-by ran; the harness keeps their
    results on the turn, and the local runner's messages answer each with its result, the
    stand-by with its words, and only a call after the stand-by with 'not run'."""
    world = point_world()
    h, fake, _ = stationed(
        world,
        [
            reply(
                "",
                call("journal", note="the wind is steady"),
                call("stand_by", until="a glass"),
                call("journal", note="never run"),
            ),
            "Awake.",
        ],
    )
    assert h.agent.standing_by
    turn = next(t for t in reversed(h.turns) if t.role == MODEL)
    r: Reply = turn.content
    assert [c.name for c in r.calls] == ["journal", "stand_by", "journal"]
    assert len(r.ran) == 1 and r.ran[0]["name"] == "journal"
    assert str(r.ran[0]["result"]) == "Noted in the journal."
    # the transcript carries it, and a reply read back from it has it
    assert Reply.from_dict(r.to_dict()).ran == r.ran
    assert Reply.from_dict(Reply("x").to_dict()).ran == ()
    # the local runner's messages: the first call its result, the stand-by its words, the
    # third 'not run'
    world.run(A_GLASS_S)  # the stand-by ends: the next sample's turn is there to answer before
    assert not h.agent.standing_by
    msgs = model_for(llama([])).messages(h.turns)
    answers = [x["content"] for x in msgs if x["role"] == "tool"]
    assert len(answers) == 3, msgs
    assert answers[0] == "Noted in the journal."
    assert answers[1].startswith("Standing by: this ended your turn")
    assert answers[2] == "Not run: a stand-by earlier in the reply ended your turn."


def test_the_api_door_answers_the_ran_calls_the_same_way():
    from freesail.agents import api as A

    world = point_world()
    h, fake, _ = stationed(
        world,
        [
            reply("", call("readings"), call("stand_by", until="a glass"), call("readings")),
            "Awake.",
        ],
    )
    assert h.agent.standing_by
    door = A.ApiModel("a-model", "a-key")
    _, out = door.messages(h.turns)
    results = [
        b
        for msg in out
        if msg["role"] == "user"
        for b in msg["content"]
        if b.get("type") == "tool_result"
    ]
    assert len(results) == 3
    first = results[0]["content"]
    first_text = first if isinstance(first, str) else json.dumps(first)
    assert "true_wind" in first_text or "heading" in first_text, first
    assert not first_text.startswith("Not run")
    assert str(results[1]["content"]).startswith("Standing by: this ended your turn")
    assert results[2]["content"] == "Not run: a stand-by earlier in the reply ended your turn."


def test_a_minute_of_fire_that_struck_nothing_is_routine_and_a_hit_or_the_opening_notable():
    """Two cutters at pistol shot: the first minute's line (the fire opened) is notable; a
    minute whose shot all fell short, over or wide is routine; a minute with a shot that
    struck her notable."""
    from tests.test_known_truths import _two_cutters_at_pistol_shot

    w, v, enemy, battery = _two_cutters_at_pistol_shot()
    w.submit("fire as they bear")
    w.run(600)
    fired = [e for e in w.log if e.kind == "action.fired"]
    assert fired, "nothing fired"
    assert fired[0].severity is Severity.NOTABLE  # the fire opened
    for e in fired:
        expect = Severity.NOTABLE if (e.data.get("struck") or e is fired[0]) else Severity.ROUTINE
        assert e.severity is expect, (e.text, e.data)


def test_at_quarters_the_yards_braced_one_by_one_are_routine_and_a_trim_is_one_notable_line():
    world = frigate_world()
    world.submit("set plain sail")
    world.run(600)
    n = len(world.log)
    world.submit("brace sharp up on the starboard tack")
    world.run(300)
    before = [e for e in list(world.log)[n:] if e.kind == "yard.braced"]
    assert before and all(e.severity is Severity.NOTABLE for e in before)
    world.submit("beat to quarters")
    world.run(120)
    n = len(world.log)
    world.submit("square the yards")
    world.run(300)
    at_quarters = [e for e in list(world.log)[n:] if e.kind == "yard.braced"]
    assert at_quarters and all(e.severity is Severity.ROUTINE for e in at_quarters)
    n = len(world.log)
    world.submit("trim sails")
    world.run(300)
    trimmed = [e for e in list(world.log)[n:] if e.kind == "yard.braced"]
    assert (
        trimmed
        and trimmed[-1].text.startswith("Braced ")
        and "yards to the wind" in trimmed[-1].text
    )
    assert trimmed[-1].severity is Severity.NOTABLE


def test_the_signal_book_says_whose_it_is_and_the_common_book_whose_it_is_not():
    from freesail.world import signals as S
    from freesail.world.scenarios import load_scenario, make_scenario_world
    from tests.test_grammar_book import ROOT

    w = make_scenario_world(load_scenario(ROOT / "data/scenarios/naval-cruise.yaml"), seed=7)
    page = w.papers.page("the signal book")
    assert page.lines[0].startswith(
        "The Britain signal books, this ship's own by her service (well-built): "
    )
    # a nation that names no book reads the common one, which says it is no other ship's
    w.scenario.nation = "denmark"
    assert S.books_for(w).root == "basic"
    page = w.papers.page("the signal book")
    assert page.lines[0].startswith(
        "The common signal book, in the period's general form and no nation's own: this "
        "ship's nation keeps no book of her own in the game, so hers is this one, and no "
        "other ship's numbers are to be read from it; "
    )
