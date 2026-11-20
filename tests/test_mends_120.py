"""Package 120: a word put in a mouth reaches the player (the owner's play of 2026-11-20).

The director's `say as <person>: "..."` (`world.orders._say_as`) wrote the line in the ship's
log and gave it to the stations held within earshot, and the player at the prompt was never
shown it, though his person stood on the same quarterdeck. A word's named hearers
(`heard_by`) are the stations held (a model's harness, the player's seat), which is what
every writer of the list walks; the play log's reading (`knowledge.hears`, decision 59) took
the list as the whole of who heard, and the player at the prompt is in no list. Now, where
his station is held by nobody, he hears such a word by the rule a held station is held to,
where his person stands: on deck within the place's earshot, not below, not asleep, not
ashore, not aboard another ship.

Each truth drives the browser's own `Driver` (a listener on it, the kinds shown) and the
console (the lines it prints), as the pages do.
"""

from __future__ import annotations

import dataclasses
import io

from freesail.ui.console import Console
from freesail.ui.server import Driver
from freesail.world import knowledge as K
from freesail.world.places import earshot
from tests.test_world_orders import OFF_FALMOUTH, _fake_officer, world_for

LAUNCH = "Launch is back, sir."


def _played():
    """A frigate off Falmouth with the pages' driver and the console both reading her log,
    the player at the prompt on the quarterdeck."""
    w = world_for(position=OFF_FALMOUTH, ports=["falmouth", "brest"])
    out = io.StringIO()
    con = Console(w, out=out)
    d = Driver(w)
    sent: list[dict] = []
    d.add_listener(lambda m: sent.append(m) if m.get("type") == "event" else None)
    d.tick(1)
    return w, d, con, out, sent


def _shown(sent: list[dict], out: io.StringIO, words: str) -> tuple[bool, bool]:
    """Whether the words were shown at the pages (the driver's events) and at the console
    (its printed lines)."""
    pages = any(words in str(m["event"].get("text", "")) for m in sent)
    return pages, words in out.getvalue()


def _say_as(w, who: str, words: str):
    w.world_order(f'say as {who}: "{words}"', "the director")
    return [e for e in w.log if e.kind == "person.spoke" and words in e.text][-1]


def test_truth_7_705_a_word_put_in_a_mouth_on_the_quarterdeck_is_shown_the_player_there():
    """The owner's fault: `say as the master` on the quarterdeck, no model seated, the
    player at the prompt there: the line is in the log, its hearers held are none, and it is
    shown him at the pages and at the console."""
    w, d, con, out, sent = _played()
    assert K.players_senses(w).spot[2] == "quarterdeck" and K.players_station(w) == "captain"
    e = _say_as(w, "the master", LAUNCH)
    assert e.data["heard_by"] == [] and e.data["place"] == "quarterdeck"
    assert "person.spoke" in [m["event"]["kind"] for m in sent]
    assert _shown(sent, out, LAUNCH) == (True, True)
    assert d.hears(e) and con.hears(e)


def test_truth_7_706_with_a_model_seated_the_word_and_the_models_own_say_are_shown_him():
    """With a model seated as officer of the watch, the word's hearers name the officer and
    not the player, and it is shown the player all the same; the officer's own `say` on the
    quarterdeck (`agent.spoke`, the same list of hearers held) is shown him too."""
    w, d, con, out, sent = _played()
    h = _fake_officer(w)
    e = _say_as(w, "the master", LAUNCH)
    assert e.data["heard_by"] == ["officer of the watch"]
    assert _shown(sent, out, LAUNCH) == (True, True)
    spoke = w.submit("say the glass is falling", actor=h.actor)
    assert spoke.kind == "agent.spoke" and spoke.data["heard_by"] == []
    assert _shown(sent, out, "the glass is falling") == (True, True)


def test_truth_7_707_the_word_is_not_shown_him_below_asleep_or_ashore():
    """The same word with the player's person below in the cabin is not shown him; nor a
    word said in the cabin while he sleeps there; nor a word on the quarterdeck while he is
    ashore."""
    w, d, con, out, sent = _played()
    _say_as(w, "the master", LAUNCH)
    assert _shown(sent, out, LAUNCH) == (True, True)
    cap = w.people.captain
    cap.where = "cabin"
    assert K.players_senses(w).spot[2] == "cabin"
    _say_as(w, "the master", "The cutter is alongside, sir.")
    assert _shown(sent, out, "The cutter is alongside") == (False, False)
    cap.where = "quarterdeck"
    d.tick(3600)
    assert d.submit("sleep").kind == "needs.answer" and K.players_senses(w).asleep
    assert K.players_senses(w).spot[2] == "cabin"
    w.people.find("the master").where = "cabin"
    _say_as(w, "the master", "Are you awake, sir?")
    assert _shown(sent, out, "Are you awake") == (False, False)
    d.submit("the time")  # his order wakes him
    assert not K.players_senses(w).asleep
    cap.aboard, cap.where, cap.port, cap.ashore_at = False, "shore", "falmouth", "quay"
    w.people.find("the master").where = "quarterdeck"
    _say_as(w, "the master", "The tide is making, sir.")
    assert _shown(sent, out, "The tide is making") == (False, False)


def test_truth_7_708_a_word_below_or_in_the_galley_by_the_places_own_earshot():
    """A word in the galley is shown the player on the quarterdeck as the place's own
    earshot says (`places.earshot`: the galley is open to the deck); a word in the gunroom
    is not."""
    w, d, con, out, sent = _played()
    gardner = w.people.find("Mr Gardner")
    assert gardner.where == "gunroom"
    _say_as(w, "Mr Gardner", "The accounts are square.")
    assert _shown(sent, out, "The accounts are square") == (False, False)
    gardner.where = "galley"
    _say_as(w, "Mr Gardner", "The coppers are drawn.")
    by_earshot = "quarterdeck" in earshot("galley")
    assert _shown(sent, out, "The coppers are drawn") == (by_earshot, by_earshot)
    assert by_earshot  # as the places stand today


def test_truth_7_709_ashore_by_his_place_and_never_aboard_another_ship():
    """Ashore, a word put in a person's mouth is shown the player at the same place of the
    same port and not at another; a word aboard is not shown his person aboard another hull;
    and where his station is held (a model holds the captain), its hearers named are the
    whole of it, as before."""
    w, d, con, out, sent = _played()
    cap, master = w.people.captain, w.people.find("the master")
    for p in (cap, master):
        p.aboard, p.where, p.port, p.ashore_at = False, "shore", "falmouth", "counting_house"
    e = _say_as(w, "the master", "The agent is out, sir.")
    assert e.data["place"] == "shore"
    assert _shown(sent, out, "The agent is out") == (True, True)
    cap.ashore_at = "market"
    _say_as(w, "the master", "The agent is back, sir.")
    assert _shown(sent, out, "The agent is back") == (False, False)
    # aboard: his person on another hull's quarterdeck does not hear this one's
    for p in (cap, master):
        p.aboard, p.where, p.port, p.ashore_at = True, "quarterdeck", "", ""
    e = _say_as(w, "the master", LAUNCH)
    here = K.players_senses(w)
    assert K.hears(w, here, e, "captain")
    there = dataclasses.replace(here, spot=("aboard", "another hull", "quarterdeck"))
    assert not K.hears(w, there, e, "captain")
    # a model holding the captain's station: the list is his, and it names him or not
    held = dataclasses.replace(e, data={**e.data, "heard_by": []})
    assert not K._station_listed(w, "captain")
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import captain

    ch = Harness(
        w,
        captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=w),
        Fake(["Noted."], loop=True),
        save=lambda w, why: None,
    )
    ch.start()
    assert K._station_listed(w, "captain")
    assert not K.hears(w, here, held, "captain")
    assert K.hears(w, here, dataclasses.replace(e, data={**e.data, "heard_by": ["captain"]}))
