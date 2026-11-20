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


def _before_the_speakers_side(e):
    """The line as a save written before the speaker's side was held it (no `said_at`)."""
    gone = (K.SAID_AT, K.SAID_PORT, K.SPEAKER_ID)
    return dataclasses.replace(e, data={k: v for k, v in e.data.items() if k not in gone})


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
    old = _before_the_speakers_side(e)  # a save's line: read by what it says of him
    assert not d.hears(old) and not con.hears(old)
    assert d.hears(e) and con.hears(e)  # the line says he spoke beside the player
    # ...and the master back beside the player at the market, the namesake of his trade in
    # the boat with no port: the boat is no port's, and the master's word is the player's
    master.where, master.ashore_at = "shore", "market"
    pearce.where, pearce.port, pearce.ashore_at = "boat", "", ""
    assert d.hears(old) and con.hears(old)
    assert d.hears(e) and con.hears(e)
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


# -- the speaker's side read from the line (the lead's list of 2026-11-20 15:54) ----------


def _read_back(d, w, words: str) -> tuple[bool, bool, bool]:
    """Whether the words are shown when the log is read back later: the pages' log as the
    driver serves it (`Driver.shown_log`), the console's `log N`, and the page's
    `/api/log`."""
    from own_page import DoorClient

    from freesail.ui.server import create_app

    shown = any(words in str(m.get("text", "")) for m in d.shown_log())
    out = io.StringIO()
    Console(w, out=out).handle_line("log 500")
    with DoorClient(create_app(d)) as http:
        api = any(words in str(m.get("text", "")) for m in http.get("/api/log?limit=5000").json())
    return shown, words in out.getvalue(), api


NOWHERE = (False, False, False)
EVERYWHERE = (True, True, True)


def test_truth_7_709_read_back_ashore_then_aboard_by_where_he_spoke():
    """The lead's reproduction: the master speaks ashore at Falmouth, the player on the
    quarterdeck; it is not shown him. The master comes back aboard to the quarterdeck, the
    player never moving: read back, at the pages, the console and the page's log, the word
    is still not shown. The converse: a word on the quarterdeck, shown, and the master then
    goes ashore: still shown. The line holds where he stood as he spoke."""
    w, d, con, out, sent = _played()
    master = w.people.find("the master")
    master.aboard, master.where, master.port, master.ashore_at = (
        False,
        "shore",
        "falmouth",
        "market",
    )
    e = _say_as(w, "the master", "Fish is dear today.")
    assert e.data[K.SAID_AT] == ["ashore", "falmouth", "market"]
    assert _shown(sent, out, "Fish is dear") == (False, False)
    master.aboard, master.where, master.port, master.ashore_at = True, "quarterdeck", "", ""
    assert _read_back(d, w, "Fish is dear") == NOWHERE
    e = _say_as(w, "the master", "The glass is rising, sir.")
    assert _shown(sent, out, "The glass is rising") == (True, True)
    master.aboard, master.where, master.port, master.ashore_at = (
        False,
        "shore",
        "falmouth",
        "market",
    )
    assert _read_back(d, w, "The glass is rising") == EVERYWHERE


def test_truth_7_709_read_back_ashore_at_another_place_then_at_his():
    """Ashore, the master at the counting house and the player at the market: his word is
    not shown; he walks to the market, the player standing: read back, still not. The
    converse: a word beside the player at the market, shown; he walks back to the counting
    house: still shown."""
    w, d, con, out, sent = _played()
    cap, master = w.people.captain, w.people.find("the master")
    for p in (cap, master):
        p.aboard, p.where, p.port = False, "shore", "falmouth"
    cap.ashore_at, master.ashore_at = "market", "counting_house"
    _say_as(w, "the master", "The agent is out, sir.")
    assert _shown(sent, out, "The agent is out") == (False, False)
    master.ashore_at = "market"
    assert _read_back(d, w, "The agent is out") == NOWHERE
    _say_as(w, "the master", "The agent is back, sir.")
    assert _shown(sent, out, "The agent is back") == (True, True)
    master.ashore_at = "counting_house"
    assert _read_back(d, w, "The agent is back") == EVERYWHERE


def test_truth_7_709_read_back_aboard_another_hull_then_brought_aboard_hers():
    """The brig X's mate speaks on her quarterdeck, the player on the frigate's: not shown.
    He is brought to the frigate's quarterdeck (`movement.put_aboard`), the player standing:
    read back, still not (the hull is the line's, not where he stands now). The converse:
    his word on the frigate's quarterdeck beside the player, shown; he goes back to the
    brig: still shown."""
    from freesail.world import movement
    from tests.test_knowledge import _with_the_brig_x

    w, _b, brig = _with_the_brig_x()
    d = Driver(w)
    cannon = brig.people.find("Mr Cannon")
    assert K.players_senses(w).spot[1:] == (str(w.own.id), "quarterdeck")
    e = _say_as(w, "Mr Cannon", "Fair wind for Falmouth.")
    assert e.data[K.SAID_AT] == ["aboard", str(brig.own.id), "quarterdeck"]
    assert not d.hears(e)
    movement.put_aboard(w, cannon, w.players, place="quarterdeck")
    assert _read_back(d, w, "Fair wind for Falmouth") == NOWHERE
    _say_as(w, "Mr Cannon", "Your servant, sir.")
    assert _read_back(d, w, "Your servant") == EVERYWHERE
    movement.put_aboard(w, cannon, brig, place="quarterdeck")
    assert _read_back(d, w, "Your servant") == EVERYWHERE


def test_truth_7_709_read_back_a_namesake_of_his_trade_decides_nothing():
    """The brig's Mr Cannon speaks on her quarterdeck and then goes below in her; a man of
    the frigate's is named Mr Cannon, of the same trade, on the frigate's quarterdeck beside
    the player: the brig's word is not shown him, read back. The converse: the frigate's Mr
    Cannon speaks beside the player, shown; he goes below and the brig's Mr Cannon stands on
    her quarterdeck: still shown."""
    from tests.test_knowledge import _with_the_brig_x

    w, _b, brig = _with_the_brig_x()
    d = Driver(w)
    cannon = brig.people.find("Mr Cannon")
    _say_as(w, "Mr Cannon", "The brig is snug, sir.")
    cannon.where = "cabin"
    purser = next(p for p in w.people.everyone if p.role == "purser" and p.hull != brig.own.id)
    purser.name, purser.role, purser.where = "Mr Cannon", cannon.role, "quarterdeck"
    assert _read_back(d, w, "The brig is snug") == NOWHERE
    cannon.where = "quarterdeck"
    e = _say_as(w, "Mr Cannon", "The frigate is snug, sir.")
    assert e.data[K.SAID_AT] == ["aboard", str(w.own.id), "quarterdeck"]
    assert _read_back(d, w, "The frigate is snug") == EVERYWHERE
    purser.where = "gunroom"
    assert _read_back(d, w, "The frigate is snug") == EVERYWHERE


def test_truth_7_708_the_mastheads_hail_is_her_hulls_and_no_others():
    """The frigate's lookout hails from her masthead, the brig X hove to beside her: the
    line says the hail was her hull's (`said_at`), and it is shown the player on her
    quarterdeck, read back as live; a person standing on the brig's quarterdeck at the
    same moment would not hear it, nor one in the frigate's gunroom, and one at her
    masthead would."""
    from tests.test_knowledge import _with_the_brig_x

    w, _b, brig = _with_the_brig_x()
    d = Driver(w)
    e = _say_as(w, "the lookout", "Sail ho! Fine on the weather bow.")
    frigate = str(w.own.id)
    assert frigate != str(brig.own.id)
    assert e.data[K.SAID_AT] == ["aboard", frigate, "masthead"]
    assert d.hears(e)
    assert _read_back(d, w, "Fine on the weather bow") == EVERYWHERE
    here = K.players_senses(w)
    for spot, heard in (
        (("aboard", str(brig.own.id), "quarterdeck"), False),  # another hull's deck
        (("aboard", frigate, "gunroom"), False),
        (("aboard", frigate, "masthead"), True),
        (("aboard", frigate, "quarterdeck"), True),
    ):
        assert K.hears(w, dataclasses.replace(here, spot=spot), e) is heard, spot
    # ...and still so with the brig followed (the player gone aboard her): the hull is the
    # line's, not the hull the world now follows
    from freesail.world import movement
    from freesail.world.hearing import own_hull

    movement.put_aboard(w, w.people.captain, brig, place="quarterdeck")
    assert own_hull(w) == str(brig.own.id)
    assert not K.hears(w, dataclasses.replace(here, spot=("aboard", own_hull(w), "quarterdeck")), e)
    assert K.hears(w, dataclasses.replace(here, spot=("aboard", frigate, "quarterdeck")), e)


def test_truth_7_709_a_line_without_the_speakers_side_is_read_as_before_hidden_on_doubt():
    """A line of a save written before the speaker's side was (no `said_at`) is read by
    what it says of him, his name, trade and place, as before: the master's word at the
    market beside the player is shown; with a namesake of his trade at the counting house
    of the same port (the line holds no place ashore), it is hidden on doubt. The line that
    says where he stood is not in doubt: shown. The fall-back, pinned."""
    w, d, con, out, sent = _played()
    cap, master = w.people.captain, w.people.find("the master")
    for p in (cap, master):
        p.aboard, p.where, p.port, p.ashore_at = False, "shore", "falmouth", "market"
    e = _say_as(w, "the master", "The agent is out, sir.")
    assert _shown(sent, out, "The agent is out") == (True, True)
    old = _before_the_speakers_side(e)
    assert d.hears(old) and con.hears(old)  # read by his name: he is beside the player
    pearce = w.people.find("Mr Pearce")
    pearce.name, pearce.role = master.name, master.role
    pearce.aboard, pearce.where, pearce.port = False, "shore", "falmouth"
    pearce.ashore_at = "counting_house"
    assert not d.hears(old) and not con.hears(old)  # two answer to it, one out of hearing
    assert d.hears(e) and con.hears(e)
