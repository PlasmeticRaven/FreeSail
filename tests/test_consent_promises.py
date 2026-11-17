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
