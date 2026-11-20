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
    shown him at the pages and at the console; the same word with him below in the cabin is
    not (so that a mend too loose fails here)."""
    w, d, con, out, sent = _played()
    assert K.players_senses(w).spot[2] == "quarterdeck" and K.players_station(w) == "captain"
    e = _say_as(w, "the master", LAUNCH)
    assert e.data["heard_by"] == [] and e.data["place"] == "quarterdeck"
    assert "person.spoke" in [m["event"]["kind"] for m in sent]
    assert _shown(sent, out, LAUNCH) == (True, True)
    assert d.hears(e) and con.hears(e)
    w.people.find("the master").where = "cabin"  # he goes below after: the line stands
    assert d.hears(e) and con.hears(e)
    w.people.find("the master").where = "quarterdeck"
    w.people.captain.where = "cabin"
    e = _say_as(w, "the master", "The cutter is alongside, sir.")
    assert e.data["heard_by"] == [] and e.data["place"] == "quarterdeck"
    assert _shown(sent, out, "The cutter is alongside") == (False, False)
    assert not d.hears(e) and not con.hears(e)


def test_truth_7_706_with_a_model_seated_the_word_and_the_models_own_say_are_shown_him():
    """With a model seated as officer of the watch, the word's hearers name the officer and
    not the player, and it is shown the player all the same; the officer's own `say` on the
    quarterdeck (`agent.spoke`, the same list of hearers held) is shown him too; with him
    below in the cabin, neither is."""
    w, d, con, out, sent = _played()
    h = _fake_officer(w)
    e = _say_as(w, "the master", LAUNCH)
    assert e.data["heard_by"] == ["officer of the watch"]
    assert _shown(sent, out, LAUNCH) == (True, True)
    spoke = w.submit("say the glass is falling", actor=h.actor)
    assert spoke.kind == "agent.spoke" and spoke.data["heard_by"] == []
    assert _shown(sent, out, "the glass is falling") == (True, True)
    w.people.captain.where = "cabin"
    e = _say_as(w, "the master", "The cutter is alongside, sir.")
    assert e.data["heard_by"] == ["officer of the watch"]
    assert _shown(sent, out, "The cutter is alongside") == (False, False)
    spoke = w.submit("say the glass is steady", actor=h.actor)
    assert spoke.kind == "agent.spoke" and spoke.data["place"] == "quarterdeck"
    assert _shown(sent, out, "the glass is steady") == (False, False)


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
    is not. The lookout's hail from the masthead (`say as the lookout`, a voice of the
    ship's own) is shown him on the quarterdeck, where `_say_as` takes it to be heard, and
    not below."""
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
    e = _say_as(w, "the lookout", "Sail ho! Broad on the lee bow.")
    assert e.data["place"] == "masthead" and e.data["heard_by"] == []
    assert _shown(sent, out, "Sail ho!") == (True, True)
    w.people.captain.where = "cabin"
    _say_as(w, "the lookout", "Deck there! She has hauled her wind.")
    assert _shown(sent, out, "She has hauled her wind") == (False, False)


def test_truth_7_709_ashore_by_his_place_aboard_another_ship_by_his_hull_and_no_namesake():
    """Ashore, a word put in a person's mouth is shown the player at the same place of the
    same port and not at another, and a namesake standing at the player's place does not
    show him the word of a man at another place. The player a visitor aboard the brig X: her
    mate's word on her quarterdeck is shown him, and still with a man of the same name in
    the frigate; a word of the brig's said while he is aboard the frigate is not. Where his
    station is held (a model holds the captain), its hearers named are the whole of it."""
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
    # a namesake at the player's place: the master's word at the counting house is not
    # shown him at the market for the namesake standing beside him there
    pearce = w.people.find("Mr Pearce")
    pearce.name = master.name  # the first of that name in the registry
    pearce.aboard, pearce.where, pearce.port = False, "shore", "falmouth"
    pearce.ashore_at = "market"
    e = _say_as(w, "the master", "The agent is gone again, sir.")
    assert e.text.startswith(master.name)
    assert _shown(sent, out, "The agent is gone again") == (False, False)
    # ...and the master beside the player at the market, the namesake at the counting
    # house: his word is shown (the line's trade tells the two apart)
    master.ashore_at, pearce.ashore_at = "market", "counting_house"
    e = _say_as(w, "the master", "The boat waits at the steps, sir.")
    assert _shown(sent, out, "The boat waits at the steps") == (True, True)
    # a man in the boat off Falmouth is said 'ashore at Falmouth': with a namesake of his
    # trade at the market beside the player, the boat's word is not the player's to hear
    assert e.data["place"] == "shore" and e.data["where"].startswith("ashore at Falmouth")
    master.where, master.ashore_at = "boat", ""
    pearce.role, pearce.ashore_at = master.role, "market"
    assert not d.hears(e) and not con.hears(e)
    pearce.role = "first lieutenant"
    # a model holding the captain's station: the list is his, and it names him or not
    for p in (cap, master):
        p.aboard, p.where, p.port, p.ashore_at = True, "quarterdeck", "", ""
    e = _say_as(w, "the master", LAUNCH)
    here = K.players_senses(w)
    assert K.hears(w, here, e, "captain") and not K._station_listed(w, "captain")
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import captain

    Harness(
        w,
        captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=w),
        Fake(["Noted."], loop=True),
        save=lambda w, why: None,
    ).start()
    assert K._station_listed(w, "captain")
    assert not K.hears(w, here, dataclasses.replace(e, data={**e.data, "heard_by": []}))
    assert K.hears(w, here, dataclasses.replace(e, data={**e.data, "heard_by": ["captain"]}))


def test_truth_7_709_aboard_another_ship_by_her_hull_whatever_his_name():
    """The second half of 7-709, aboard: the brig X's mate speaks on her quarterdeck. The
    player on the frigate is not shown it; a visitor on the brig's quarterdeck is, at the
    pages and at the console, and still when a man of the frigate's bears the same name."""
    from freesail.world import movement
    from tests.test_knowledge import _with_the_brig_x

    w, _b, brig = _with_the_brig_x()

    def views():
        out = io.StringIO()
        Console(w, out=out)
        d = Driver(w)
        sent: list[dict] = []
        d.add_listener(lambda m: sent.append(m) if m.get("type") == "event" else None)
        return sent, out

    sent, out = views()
    cannon = brig.people.find("Mr Cannon")
    assert cannon is not None and cannon.where == "quarterdeck"
    assert K.players_senses(w).spot[2] == "quarterdeck"  # on the frigate's quarterdeck
    _say_as(w, "Mr Cannon", "Fair wind for Falmouth.")
    assert _shown(sent, out, "Fair wind for Falmouth") == (False, False)
    bowen = w.people.captain
    movement.put_aboard(w, bowen, brig, place="quarterdeck")
    assert K.players_visitor(w) is bowen
    sent, out = views()  # the pages and the console as opened with him aboard her
    w.world_order('say as Mr Cannon: "The tide serves, sir."', "the director")
    assert _shown(sent, out, "The tide serves") == (True, True)
    purser = next(p for p in w.people.everyone if p.role == "purser" and p.hull != brig.own.id)
    purser.name = "Mr Cannon"  # a namesake of the frigate's, in her gunroom
    assert purser.where == "gunroom"
    w.world_order('say as Mr Cannon: "The pilot is aboard, sir."', "the director")
    assert _shown(sent, out, "The pilot is aboard") == (True, True)
    purser.where = "quarterdeck"  # the namesake on the frigate's quarterdeck: his trade
    w.world_order('say as Mr Cannon: "The anchor is a-peak, sir."', "the director")
    assert _shown(sent, out, "The anchor is a-peak") == (True, True)
