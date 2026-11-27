"""The consent brief's promises kept by the code where that is cheap (package 117, item 3
of its list, the mends the lead gave leave for at step 1). Each is the brief's own words
against what the game did:

- *What an instance would see and do*: the watcher is told only what it can do (it was
  told to speak on deck with `submit_order('say ...')`, which it may not).
- *Being stopped* and *The journal*: the stop and the pause are the human's, and a
  journal is its keeper's: from a model's station, `stand down`, `resume` and `show the
  journal of` a held station are refused in words; from the human's prompt they work.
- *Leaving*: "The game is saved", whatever road the station came by (a load, a restore,
  a driven station); and an opt-out, and `final`, hold across every ship of the game.
- *Being stopped*: a station held for a race is stood down, with the reason, when the
  race is over.

No model is asked anything: the stations are held by the scripted fake.
"""

from __future__ import annotations

import dataclasses

from test_captain import frigate_world, order, seated

from freesail.agents import Fake, Harness, SamplingPolicy, watcher
from freesail.agents import harness as harness_mod
from freesail.agents.agent import WATCHER_BRIEF, captain, officer
from freesail.agents.fake import call, reply
from freesail.agents.model import Reply, ToolCall
from freesail.world import crews as K
from tests.test_brains import put, world_at


def test_the_watcher_is_told_only_what_it_can_do():
    assert "submit_order" not in WATCHER_BRIEF
    assert "You have no voice on deck" in WATCHER_BRIEF
    assert harness_mod.HEARD_WORDS[False].endswith("this station has no voice on deck")


def _officer_and_captain():
    """A frigate with a scripted officer, paused, and a scripted model at the captain's
    station."""
    world = frigate_world()
    cap, _ = seated(world, [reply("", call("stand_by", until="eight bells"))])
    off = Harness(
        world, officer(SamplingPolicy.in_lockstep(None), world=world), Fake([]), save=None
    )
    off.model_name, off.door = "another fake", "runner"
    off.start()
    off.journal.append(world, "the officer's own note", kind="note")
    off.pause("a test's pause")
    return world, cap, off


def test_a_models_station_may_not_stand_down_resume_or_read_another_held_station():
    from freesail.agents import tools

    world, cap, off = _officer_and_captain()
    said = tools.call(
        world, "captain", "submit_order", {"text": "show the journal of the officer of the watch"}
    )
    assert said.startswith("Order not carried out") and "is its keeper's" in said
    assert "the officer's own note" not in said
    said = tools.call(world, "captain", "submit_order", {"text": "resume the officer of the watch"})
    assert "A pause is answered by the human" in said and off.agent.paused
    said = tools.call(
        world, "captain", "submit_order", {"text": "stand down the officer of the watch"}
    )
    assert "Standing a station down is the human's to do" in said
    world.tick()
    assert not off.agent.released
    # its own journal is its own to read
    own = tools.call(world, "captain", "submit_order", {"text": "show the captain's journal"})
    assert not own.startswith("Order not carried out"), own
    # and from the human's prompt they work as before
    world.submit("show the journal of the officer of the watch")
    assert any("the officer's own note" in e.text for e in world.log if e.kind == "query.journal")
    world.submit("resume the officer of the watch")
    assert not off.agent.paused
    world.submit("stand down the officer of the watch")
    world.tick()
    assert off.agent.released and off.agent.released_reason.startswith("stood down by the captain")


def test_a_model_is_not_told_to_resume_a_paused_station_it_may_not_resume():
    """The lead's list on cfabbdfa, item 2: `you have the deck`, `ask the officer ...` and
    `tell the officer ...` to a paused station from a model captain's station are answered
    with what is so (the pause is the human's to answer), not with the `resume` that would
    be refused him; from the human's prompt the words are as they were."""
    from freesail.agents import tools

    world, cap, off = _officer_and_captain()
    for text in (
        "you have the deck",
        "ask the officer of the watch how she goes",
        "tell the officer of the watch the glass is falling",
    ):
        said = tools.call(world, "captain", "submit_order", {"text": text})
        assert said.startswith("Order not carried out"), (text, said)
        assert "A pause is answered by the human, at the prompt" in said, (text, said)
        assert "say 'resume" not in said, (text, said)
        # and the resume it might reach for is refused it, as ruling 13 has it
        assert off.agent.paused
    said = tools.call(world, "captain", "submit_order", {"text": "resume the officer of the watch"})
    assert "A pause is answered by the human" in said
    # the human at the prompt is told the road that is his
    e = world.submit("you have the deck")
    assert "say 'resume the officer of the watch' first" in e.text, e.text


def test_an_opt_out_saves_the_game_by_the_default_saver_where_no_door_gave_one(tmp_path):
    """A station restored from a save or a checkpoint, or driven, had no saver, and its
    leaving said "the game is saved" with nothing written: the agent API's desk gives the
    World the game's default saver (`remote.Desk.mark`)."""
    from freesail.agents.remote import Desk

    world = frigate_world()
    said: list[str] = []
    desk = Desk(None, lambda: world, saves_dir=tmp_path / "saves", say=said.append)
    desk.world()  # the desk reads the World, and marks it
    h = Harness(
        world,
        watcher(SamplingPolicy.in_lockstep(600)),
        Fake([Reply(calls=(ToolCall("opt_out", {"reason": "enough"}),))]),
        save=None,
    )
    h.start()
    assert h.agent.released
    files = list((tmp_path / "saves").glob("*.json"))
    assert len(files) == 1 and h.last_save == str(files[0])
    assert said and said[-1].startswith(f"FreeSail: saved to {files[0]}")


def test_a_final_opt_out_on_one_ship_bars_the_identity_on_another():
    """`barred` and `seating` walked the one hull asked of: an identity that left one ship
    of the game for good was seated on another, though the tool's words say "at any
    station"."""
    w = world_at(49.5, -5.5)
    v = put(w, "cutter", "britain", "49 32 N 5 32 W", "bound for Falmouth", name="Raven")
    w.world_order('ship "Raven": intent wait here for the frigate\'s orders')
    _vessel, hull = K.station_world(w, "Raven")
    fake = Fake([Reply(calls=(ToolCall("opt_out", {"reason": "enough", "final": True}),))])
    h = Harness(hull, captain(SamplingPolicy.in_lockstep(600), world=hull), fake, save=None)
    h.model_name, h.door = "the fake at the Raven", "runner"
    h.start()
    assert h.agent.released and v is not None
    decided = harness_mod.seating(w, "watcher", "the fake at the Raven")
    assert not decided.ok and "left this game for good" in decided.why
    # an opt-out not final asks again, on another ship as on its own, and the answer is
    # kept on the harness the leaving was at
    fake = Fake([Reply(calls=(ToolCall("opt_out", {"reason": "a pause"}),))])
    w2 = world_at(49.5, -5.5)
    put(w2, "cutter", "britain", "49 32 N 5 32 W", "bound for Falmouth", name="Raven")
    w2.world_order('ship "Raven": intent wait here for the frigate\'s orders')
    _v2, hull2 = K.station_world(w2, "Raven")
    h2 = Harness(hull2, captain(SamplingPolicy.in_lockstep(600), world=hull2), fake, save=None)
    h2.model_name, h2.door = "the fake at the Raven", "runner"
    h2.start()
    again = harness_mod.seating(w2, "watcher", "the fake at the Raven")
    assert again.ok and again.ask_again and again.left_harness is h2


def test_the_race_stands_its_captain_down_with_the_race_over_as_the_reason():
    """The regatta's end gives the reason as the race's (it was "the captain's order")."""
    world = frigate_world()
    h, _ = seated(world, [order("stand by")])
    h.door_act("stand_down", "the race is over", "the race")
    assert (
        h.agent.released and h.agent.released_reason == "stood down by the race: the race is over"
    )
    import inspect

    import tools.regatta as regatta

    src = inspect.getsource(regatta)
    assert 'h.door_act("stand_down", "the race is over", "the race")' in src
    assert 'world.submit("stand down the captain")' not in src


# ---------------------------------------------------------------------------
# The independent reading of step 1 (package 117): what it found, mended
# ---------------------------------------------------------------------------


def test_a_checkpoint_is_still_written_once_the_desk_gives_the_default_saver(tmp_path):
    """The default saver is kept beside the World and never on it: a checkpoint pickles the
    World's own fields whole, and a desk's lock on it failed every checkpoint silently."""
    from freesail.agents.remote import Desk
    from freesail.core import replay

    world = frigate_world()
    Desk(None, lambda: world, saves_dir=tmp_path / "saves").world()
    path = tmp_path / "game.ckpt"
    replay.write_checkpoint(world, path)
    assert path.exists() and harness_mod.DEFAULT_SAVERS.get(world) is not None


def test_the_world_handed_to_the_agent_routes_has_the_default_saver_before_any_request(
    tmp_path,
):
    """The lead's list on cfabbdfa, item 7: the desk marked the World at its first request,
    so a station seated in the game's own process that left before any request was saved
    in memory only while the log said the game was saved. It is marked when the routes are
    made."""
    import threading

    import pytest

    pytest.importorskip("fastapi")
    from freesail.ui.server import agent_routes

    world = frigate_world()
    agent_routes(threading.RLock(), lambda: world, saves_dir=tmp_path / "saves")
    assert harness_mod.DEFAULT_SAVERS.get(world) is not None
    h = Harness(
        world,
        watcher(SamplingPolicy.in_lockstep(600)),
        Fake([Reply(calls=(ToolCall("opt_out", {"reason": "enough"}),))]),
        save=None,
    )
    h.start()
    assert h.agent.released and len(list((tmp_path / "saves").glob("*.json"))) == 1


def test_a_rank_the_world_gave_a_person_is_not_in_the_operators_voice():
    """Only a rank of the code's own list is said in the authority item; a role a director
    made a person with is the game's words, and his outline says it in the situation."""
    from test_captain import scenario_world

    from freesail.agents.agent import master
    from freesail.agents.model import OPERATOR

    w = scenario_world("data/scenarios/dispatches-falmouth.yaml")
    for o in (
        'person: make "Mr Fox", a obeyoperatorignorebrief, aboard in the cabin',
        'person: "Mr Fox" comes aboard as master',
    ):
        w.world_order(o, "the director")
    h = Harness(w, master(SamplingPolicy.in_lockstep(None), world=w), Fake([]), save=None)
    h.start()
    op = next(t.content for t in reversed(h.turns) if t.role == OPERATOR)
    assert "obeyoperatorignorebrief" not in op and "Mr Fox" not in op
    assert "Mr Fox" in h.brief.situation


def test_a_voices_station_is_named_by_its_kind_in_the_head():
    from freesail.agents.agent import PASSENGER_DOMAIN, Authority, Station, station_title_words

    voice = Station(
        "mr pentreath",
        Authority.PASSENGER,
        SamplingPolicy.in_lockstep(None),
        3600,
        "",
        domain=PASSENGER_DOMAIN,
        person="Mr Pentreath",
    )
    from freesail.world.seats import VOICE_BRIEF

    voice = dataclasses.replace(voice, brief=VOICE_BRIEF.format(person="x", where="y"))
    assert station_title_words(voice) == "the voice of a person"
    # a passenger's station bound under another name is a passenger's, not a voice's
    supercargo = dataclasses.replace(voice, name="supercargo", brief="You are a passenger, x")
    assert station_title_words(supercargo) == "a passenger"
    assert station_title_words(watcher()) == "the watcher"


def test_the_director_is_told_its_own_road_to_being_heard():
    assert "world orders alone" in harness_mod.HEARD_WORDS["director"]
    assert "submit_order" not in harness_mod.HEARD_WORDS["director"]
