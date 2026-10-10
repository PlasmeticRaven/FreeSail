"""The officer of the watch (package 37; spec M5 §29; spec M4 §11 extended to a station
with authority; the cold review's six items), proven against the scripted fake
(`freesail/agents/fake.py`) and never a model.

The seven commitments of `docs/agents/README.md` hold for a station with authority, and
each has a case here beside the watcher's in `tests/test_agents.py`: the token first
(`test_the_token_ends_the_officers_watch_before_the_order_is_read`), the graduated stops
(`test_orders_that_undo_one_another_bring_the_nudge_then_the_pause`), in-world text as
data (`test_the_officers_brief_head_carries_the_five_items_the_domain_and_the_night_orders`),
the journal (`test_hand_over_gives_the_deck_back_with_the_note_and_the_officer_stays`),
the transcript policy (the head's first item, unchanged) and nothing real (the tools'
words, `test_agents`). Parity is structural: what the officer reads is the registry and
the log; its orders go through `World.submit` with the station's actor and are refused by
the same grammar. Every world here is the frigate in a steady wind (gustiness and
variability nought) or the point ship, and the stations sample every ten minutes in
lockstep, so that a script's count of replies is exact.
"""

from __future__ import annotations

import datetime as dt
import io
import json
from pathlib import Path
from typing import Any

import pytest

from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call, consent, reply
from freesail.agents import harness as harness_mod
from freesail.agents import tools as tools_mod
from freesail.agents.agent import (
    A_GLASS_S,
    A_WATCH_S,
    OFFICER,
    OFFICER_DOMAIN,
    OPT_OUT_TOKEN,
    OPTED_OUT,
    STOOD_DOWN,
    TOKEN_NAMED_WORDS,
    Authority,
    Grant,
    officer,
    officer_rank,
    watcher,
)
from freesail.agents.fake import officer_of_the_watch
from freesail.agents.model import DATA, OPERATOR
from freesail.agents.tools import TOOLS, parameters_schema, truthy
from freesail.api import readings as R
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.standing.runtime import contrary

ROOT = Path(__file__).resolve().parents[1]
SHIPS = {name: str(ROOT / "data/ships" / f"{name}.yaml") for name in ("frigate-36",)}
FRIGATE = SHIPS["frigate-36"]
EVERY = 600  # sampled every ten minutes, as tests/test_agents.py's short station
WEIGHTS = "made-up-officer-model-27b.Q5_K_M.gguf"  # made up: no model is named here
TODAY = dt.date(2026, 10, 2)


def frigate_world(seed: int = 7, start: dt.datetime | None = None) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    if start is not None:
        scenario.start_time = start
    return make_world(seed, FRIGATE, scenario)


def point_world(seed: int = 7) -> World:
    return World(seed=seed, scenario=Scenario(gustiness=0.0, variability=0.0))


def station(world: World | None = None, every: int | None = EVERY, events: bool = False):
    sevs = ("notable", "urgent") if events else ()
    return officer(SamplingPolicy.in_lockstep(every, *sevs), world=world)


def seated(
    world: World, script, *, deck: bool = True, events: bool = False, **kw
) -> tuple[Harness, Fake, list[str]]:
    """An officer on `world` with a fake playing `script`, the deck given at once when
    `deck` (the captain's order, journaled); the saves it makes are listed."""
    saves: list[str] = []
    fake = Fake(script, **kw)
    h = Harness(world, station(world, events=events), fake, save=lambda w, why: saves.append(why))
    if deck:
        # the captain's word before the first sample, so the script's first reply has it
        e = world.submit("you have the deck")
        assert e.kind == "agent.deck", e.text
    h.start()
    return h, fake, saves


def order(text: str, **args: Any) -> Reply:
    return reply("", call("submit_order", text=text, **args))


def tools_call(world: World, name: str, **args: Any) -> Any:
    """A tool called for the officer's station outside a reply, as a door's call is."""
    from freesail.agents import tools

    return tools.call(world, OFFICER, name, args)


def kinds(world: World, prefix: str = "agent.") -> list[str]:
    return [e.kind for e in world.log if e.kind.startswith(prefix)]


def lines(world: World, kind: str) -> list[str]:
    return [e.text for e in world.log if e.kind == kind]


def data_turns(fake: Fake) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []
    for turns in fake.seen:
        for t in turns:
            if t.role == DATA and not any(t.content is s for s in seen):
                seen.append(t.content)
    return seen


def results(fake: Fake) -> list[str]:
    """Every tool result the fake was shown, in order."""
    out: list[str] = []
    for d in data_turns(fake):
        for r in d.get("tool_results") or []:
            out.append(str(r.get("result")))
    return out


# ---------------------------------------------------------------------------
# The station: the person, the deck given and taken, the reading, the brief head
# ---------------------------------------------------------------------------


def test_the_officer_takes_the_place_of_the_first_lieutenant_or_the_mate():
    """Item 2: a person of package 35 holds the place; the model takes his station, by his
    name and his rank (the frigate's first lieutenant; the schooner's and the cutter's
    mate; the brig-sloop's lieutenant); a point world names the first lieutenant alone."""
    world = frigate_world()
    name, rank = officer_rank(world)
    assert name == world.people.find("first lieutenant").name and rank == "first lieutenant"
    st = station(world)
    assert st.name == OFFICER and st.person == name and st.rank == rank and st.drill
    assert st.authority is Authority.OFFICER_2 and st.domain is OFFICER_DOMAIN
    assert st.brief.startswith(f"You are the officer of the watch, in the place of {name}")
    for ship, role in (("topsail-schooner", "mate"), ("cutter", "mate"), ("brig", "lieutenant")):
        w = make_world(7, str(ROOT / "data/ships" / f"{ship}.yaml"), Scenario())
        n, r = officer_rank(w)
        assert r == role and n == w.people.find(role).name, ship
    assert officer_rank(point_world()) == ("the first lieutenant", "first lieutenant")
    # the station saves and loads whole, the domain as data
    loaded = type(st).load(json.loads(json.dumps(st.save())))
    assert loaded == st


def test_the_officers_brief_head_carries_the_five_items_the_domain_and_the_night_orders():
    """Items 1, 5 and 7: the head's five items in order (truth 46); the authority item
    states the domain in words, the person, whose the deck is and the captain's night
    orders (the book as it stands); the opt-out item carries the two sentences asked for
    in the consent record of 2026-09-29; the station brief comes after the head."""
    world = frigate_world()
    world.submit('standing order "night routine": at sunset then take in the royals')
    world.submit('standing order "glass": when the glass is falling fast then shorten sail')
    h, fake, _ = seated(world, ["Aye, sir."], deck=False)
    brief = h.brief
    assert brief.order == ("disclosure", "opt_out", "documentation", "authority", "situation")
    assert "the station of the officer of the watch" in brief.head[0].text
    assert TOKEN_NAMED_WORDS in brief.head[1].text
    authority = brief.head[3].text
    assert authority.startswith(OFFICER_DOMAIN.words)
    assert "You are in the place of Mr Pearce, whose rank, first lieutenant" in authority
    assert "The deck is the captain's now." in authority
    assert "The captain's night orders" in authority
    assert '"night routine" (the captain): at sunset then take in the royals' in authority
    assert '"glass" (the captain)' in authority
    assert brief.text().index(h.station.brief) > brief.text().index(authority)
    # the strangers, the port, the dangers and the people are the registry's rows, and so
    # in the situation item as every reading is (parity is structural)
    situation = brief.head[4].text
    for row in ("strangers", "port", "dangers", "people", "officer_of_the_watch"):
        assert f"  {row}: " in situation, row
    # the one operator turn is the brief
    assert [t.role for t in fake.seen[0]].count(OPERATOR) == 1


def test_you_have_the_deck_gives_it_and_i_have_the_deck_takes_it_and_no_more():
    """Item 2, as package 37g has it (item 11; the owner's ruling of 2026-10-05): `you have
    the deck` (or `Mr <name>, you have the deck`) gives the deck, with the night orders
    said in the sample's notice and the word; `the officer of the watch` reads who has it
    since when; `I have the deck` takes the deck and no more: the officer stays seated,
    off watch, and an order he gives is refused in words that say he has not the deck.
    Before the deck an order is refused in the same words."""
    world = frigate_world()
    world.submit('standing order "night routine": at sunset then take in the royals')
    world.submit("set plain sail")
    world.run(60)
    script = [order("set the royals"), "", "Aye.", "", order("set the royals"), ""]
    h, fake, saves = seated(world, script, deck=False)
    refused = lines(world, "agent.refused")
    assert refused == [
        "The officer of the watch has not the deck: the captain gives it with 'you have the "
        "deck', and until then no order is given. 'set the royals' not carried out."
    ]
    assert h.agent.words() == "stationed; the deck the captain's"
    # the reading before the deck
    e = world.submit("the officer of the watch")
    assert e.kind.startswith("query")
    assert "is at the station, off watch; the captain has the deck" in e.text
    # a stranger's name is refused; the officer's own is taken, with or without the name
    e = world.submit("Mr Nobody, you have the deck")
    assert e.kind == "order.rejected" and "Mr Pearce is at the station" in e.text
    e = world.submit("Mr Pearce, you have the deck")
    assert e.kind == "agent.deck" and e.severity is Severity.NOTABLE
    assert e.text == (
        "Mr Pearce, you have the deck. The officer of the watch has the deck; the captain's "
        "standing orders are his night orders."
    )
    assert world.journal[-1][2] == "Mr Pearce, you have the deck"  # the captain's order
    assert h.agent.has_deck and h.agent.deck_stamp == world.clock.stamp()
    world.run(1)  # the word rides the next sample
    sample = data_turns(fake)[-1]
    assert sample["word"] == "You have the deck."
    assert sample["notices"][0].startswith("The captain gives you the deck at ")
    assert "and neither ends your part" in sample["notices"][0]
    assert (
        '"night routine" (the captain): at sunset then take in the royals' in sample["notices"][0]
    )
    # and what his word allows now: nothing, said so
    assert sample["notices"][1] == (
        "The captain's word allows nothing beyond your domain at present."
    )
    assert h.journal.entries[-1].kind == "agent.deck"
    e = world.submit("you have the deck")
    assert e.kind == "order.rejected" and "has the deck already" in e.text
    e = world.submit("who has the deck")
    assert "Mr Pearce, first lieutenant, has the deck since" in e.text
    assert "stationed; with the deck since" in h.agent.words()
    # the captain takes it: the deck and no more. No stand-down, no save, the station kept
    e = world.submit("I have the deck")
    assert e.kind == "agent.deck" and e.text == (
        "The captain has the deck. The officer of the watch stays at the station, off watch."
    )
    assert not h.agent.released and not h.agent.has_deck and saves == []
    assert h.agent.words() == "stationed; the deck the captain's"
    assert h.journal.entries[-1].text == (
        "The captain took the deck; I stay at the station, off watch."
    )
    assert "agent.stopped" not in kinds(world)
    e = world.submit("the officer of the watch")
    assert "is at the station, off watch; the captain has the deck" in e.text
    e = world.submit("I have the deck")
    assert e.kind == "order.rejected" and "it is the captain's already" in e.text
    # he is told, and an order he gives off watch is refused as it was before the deck
    world.run(1)
    sample = data_turns(fake)[-1]
    assert sample["word"] == "I have the deck."
    assert sample["notices"][0].startswith(
        "The captain has taken the deck. You stay at your station, off watch"
    )
    world.run(EVERY)
    assert len(lines(world, "agent.refused")) == 2
    assert lines(world, "agent.refused")[-1].startswith(
        "The officer of the watch has not the deck: the captain gives it with"
    )
    # nobody at the station: the deck's sentences say so
    fresh = frigate_world()
    e = fresh.submit("you have the deck")
    assert e.kind == "order.rejected" and "a model's door seats one first" in e.text
    e = fresh.submit("the officer of the watch")
    assert R.NO_OFFICER_WORDS in e.text
    e = fresh.submit("hand over the deck")
    assert e.kind == "order.rejected" and "the officer of the watch's own order" in e.text


def test_the_deck_is_taken_and_given_three_times_with_the_station_seated_throughout():
    """Package 37g, item 11 (the owner's ruling of 2026-10-05): `you have the deck` and `I
    have the deck` move the officer between the state he starts in and the officer's, and
    back, as often as the captain likes. Three times here, with one seating, no save and
    no stand-down; with the deck his orders reach the ship, off watch they are refused;
    and the readings have the man in whose place he stands on deck with the watch, or
    off watch, never below asleep."""
    world = frigate_world(start=dt.datetime(1805, 6, 1, 23, 0))  # the night
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(world, [order("trim sails"), ""], loop=True, deck=False)
    people = world.readings.words("people")
    assert "Mr Pearce, first lieutenant: off watch." in people

    def given() -> int:
        return sum(
            1
            for x in world.log
            if x.kind == "order.accepted" and x.actor == "the officer of the watch"
        )

    for _ in range(3):
        before = given()
        e = world.submit("you have the deck")
        assert e.kind == "agent.deck" and h.agent.has_deck
        assert "Mr Pearce, first lieutenant: on deck, with the watch." in (
            world.readings.words("people")
        )
        world.run(EVERY)
        assert given() > before  # with the deck his orders reach the ship
        before = given()
        e = world.submit("I have the deck")
        assert e.kind == "agent.deck" and not h.agent.has_deck and not h.agent.released
        assert "Mr Pearce, first lieutenant: off watch." in world.readings.words("people")
        refused = len(lines(world, "agent.refused"))
        world.run(EVERY)
        assert len(lines(world, "agent.refused")) > refused and given() == before
    assert h.agent.seatings == 1 and saves == [] and "agent.stopped" not in kinds(world)
    assert [x.data.get("deck") for x in world.log if x.kind == "agent.deck"] == [
        "given",
        "taken",
    ] * 3
    # the captain's own orders for the deck are in the journal, and a replay gives the
    # same log: nothing of the deck's going to and fro is outside the record
    copy = replay.replay(json.loads(json.dumps(world.save())), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert not copy.agents[OFFICER].agent.released


def test_the_captains_sentences_reach_the_officer_by_either_name():
    """`ask the officer ...`, `tell the officer ...`, `stand down the officer`, `resume
    the officer`, `show the officer's journal`: the station's sentences, by its name or by
    `the officer`, and the vocabulary knows the words."""
    from freesail.orders import complete
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    for phrase in ("ask the officer of the watch", "ask the officer", "you have the deck"):
        assert vocab.verbs[vocab.phrase_to_verb[phrase]].object == "station", phrase
    world = frigate_world()
    assert "ask the officer of the watch " in complete.suggestions(world.ship, "ask the o")

    def answer_it(last, turns):
        if last.get("question"):
            return reply(
                "", call("answer", text=f"She heads south, sir; you asked {last['question']}.")
            )
        return Reply()

    h, fake, _ = seated(world, [answer_it], loop=True)
    e = world.submit("ask the officer how she heads")
    assert e.kind == "agent.asked" and e.text == "Asked the officer of the watch: how she heads?"
    assert lines(world, "agent.said") == [
        "[officer of the watch] She heads south, sir; you asked how she heads."
    ]
    e = world.submit("tell the officer keep her so till the change of the watch")
    assert e.kind == "agent.told" and e.text.startswith("The captain to the officer of the watch:")
    assert world.submit("show the officer's journal").kind == "query.journal"
    assert world.submit("stand the officer down").kind == "agent.stand_down"
    assert h.agent.released


# ---------------------------------------------------------------------------
# Authority per order: the domain (the cold review's first item)
# ---------------------------------------------------------------------------


def test_an_order_in_the_domain_is_given_with_the_officers_actor_and_not_journaled():
    """Item 1: an order within the domain goes through `World.submit` with the station's
    actor, the log says it as the officer's ("By the officer of the watch: setting the
    royals"), the ship hears it, and it is not journaled, since the harness's transcript
    replays it (the replay test below)."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    before = len(world.journal)
    h, fake, _ = seated(world, [order("set the royals"), "", order("trim sails"), ""])
    world.run(EVERY)
    accepted = [
        e for e in world.log if e.kind == "order.accepted" and e.actor == "the officer of the watch"
    ]
    assert [e.text for e in accepted] == [
        "By the officer of the watch: setting the royals.",
        "By the officer of the watch: trimming sails.",
    ]
    assert all(e.severity is Severity.ROUTINE for e in accepted)
    assert results(fake)[0] == "By the officer of the watch: setting the royals."
    assert len(world.journal) == before + 1  # `you have the deck` only: the captain's
    assert all(actor != "the officer of the watch" for _, actor, _ in world.journal)
    world.run(900)
    assert world.ship.sails["fore.royal"].state.value in ("set", "loosed", "sheeted", "in the gear")


@pytest.mark.parametrize(
    "text,why",
    [
        ("tack ship", "a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's"),
        ("wear ship", "a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's"),
        ("heave to", "a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's"),
        (
            "steer south-west",
            "the course is the captain's, never to be changed without his directions unless "
            "to avoid an immediate danger",
        ),
        (
            "bear away one point",
            "the course is the captain's, never to be changed without his directions unless "
            "to avoid an immediate danger",
        ),
        ("call all hands", "all hands are called, and the watch sent below, by the captain"),
        ("pipe down", "all hands are called, and the watch sent below, by the captain"),
        ("come to an anchor", "the anchor is let go and weighed by the captain"),
        ("send for the master", "the people are sent for by the captain"),
        (
            "observe the sun",
            "the reckoning, the sights and the course shaped are the master's for the captain",
        ),
        ("belay all standing orders", "the captain's book is his own"),
    ],
)
def test_an_order_outside_the_domain_is_refused_in_words_and_logged(text: str, why: str):
    """Item 1: the refusal names the order, says why it is the captain's, and is logged
    `agent.refused` with the station's actor; the ship never hears it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, _ = seated(world, [order(text), ""])
    expected = f"The officer of the watch may not {text} without the captain: {why}."
    if text in ("heave to", "steer south-west", "bear away one point"):
        # what the officer's own word opens to avoid a danger says so (package 37g)
        expected += (
            " To avoid an immediate danger, give the order with submit_order(text, "
            "danger='the danger, in your words')."
        )
    if text == "belay all standing orders":
        expected = (
            "The officer of the watch may not belay all standing orders: the captain's book "
            "is his own."
        )
    assert results(fake) == [expected]
    refused = [e for e in world.log if e.kind == "agent.refused"]
    assert len(refused) == 1 and refused[0].actor == "the officer of the watch"
    assert refused[0].text == f"{expected} {text!r} not carried out."
    assert not any(
        e.actor == "the officer of the watch" and e.kind == "order.accepted" for e in world.log
    )
    assert world.journal[-1][2] == "you have the deck"


def test_the_grammar_refuses_the_officer_as_it_refuses_the_captain():
    """Parity: a world order, a misspelt sail and a station sentence are refused by the
    same grammar and the same words as the captain's, through `World.submit`; a reading
    asked is answered in the log as a query."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, _ = seated(
        world,
        [
            order("let the wind veer two points"),
            "",
            order("set the fore skysail"),
            "",
            order("ask the watcher how she lies"),
            "",
            order("the true wind"),
            "",
        ],
    )
    world.run(3 * EVERY)
    got = results(fake)
    captain = world.submit("let the wind veer two points").text
    assert got[0] == captain and "not carried out" in got[0]
    assert "There is no such part as the fore skysail" in got[1]
    assert got[2] == (
        "The officer of the watch may not ask the watcher how she lies: a station is "
        "addressed by the captain."
    )
    assert got[3].startswith("The true wind:")


def test_the_captains_word_allows_a_named_thing():
    """Item 1: `you may tack ship if the land closes within two miles` allows the verb
    beyond the domain, his words kept as said; the reading and the brief head carry it;
    `you may not tack ship` takes it back; a standing order cannot give it. (Package 37g:
    the words "for the watch" are gone from its lines, since it stands until he takes it
    back or the officer leaves the station.)"""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(1500)  # way enough on her to stay
    h, fake, _ = seated(
        world, [order("tack ship"), "", order("tack ship"), "", order("tack ship"), ""]
    )
    e = world.submit("you may tack ship if the land closes within two miles")
    assert e.kind == "agent.deck" and e.text == (
        "The officer of the watch may tack ship (if the land closes within two miles), by "
        "the captain's word."
    )
    assert h.agent.grants == (Grant("tack ship", "if the land closes within two miles"),)
    assert "may also tack ship (if the land closes within two miles)" in (
        world.submit("the officer of the watch").text
    )
    world.run(1)  # the captain's word opens the officer's turn: the second order, allowed
    e = world.submit("you may not tack ship")
    assert e.kind == "agent.deck" and h.agent.grants == ()
    world.run(1)
    got = results(fake)
    assert got[0].startswith("The officer of the watch may not tack ship")
    # the second, allowed, reached the ship, which took it or refused it in its own words
    assert got[1].startswith(
        ("By the officer of the watch: tacking ship.", "Order not carried out ('tack ship')")
    )
    assert got[2].startswith("The officer of the watch may not tack ship")
    e = world.submit("you may tell the watcher the glass is falling")
    assert e.kind == "order.rejected" and "names no order" in e.text
    e = world.submit('standing order "x": at sunset then you may tack ship')
    assert e.kind == "order.rejected" and "the captain's own" in e.text
    h2 = Harness(frigate_world(), watcher(SamplingPolicy.in_lockstep(EVERY)), Fake(["Aye."]))
    h2.start()
    e = h2.world.submit("you may tack ship")
    assert e.kind == "order.rejected" and "no officer of the watch at the station" in e.text


# ---------------------------------------------------------------------------
# Standing orders by rank (item 2b)
# ---------------------------------------------------------------------------


def test_the_officers_standing_order_carries_the_stations_rank_never_the_texts():
    """Item 2b: a standing order given by the officer is entered in his rank (the first
    lieutenant's), the book listing it so; `by the captain` written by him is refused; a
    rule with an action outside the domain is refused in words as a plain order would be;
    he may belay, resume and strike his own and not the captain's."""
    world = frigate_world()
    world.submit('standing order "night routine": at sunset then take in the royals')
    world.submit("set plain sail")
    world.run(60)
    script = [
        order('standing order "royals in": at eight bells then take in the royals'),
        "",
        order('standing order "mine" by the captain: at eight bells then take in the royals'),
        "",
        order('standing order "about": at eight bells then set the royals; tack ship'),
        "",
        order('belay standing order "night routine"'),
        "",
        order('belay "royals in"'),
        "",
        order('resume standing order "royals in"'),
        "",
        order('strike standing order "night routine"'),
        "",
        order("standing orders"),
        "",
    ]
    h, fake, _ = seated(world, script)
    world.run(7 * EVERY)
    got = results(fake)
    assert got[0] == (
        "Standing order 'royals in' entered in the book by the first lieutenant: at eight "
        "bells then take in the royals."
    )
    rule = world.standing.book.get("royals in")
    assert rule.given_by == "first lieutenant" and rule.rank == 1
    assert got[1] == (
        "The officer of the watch gives standing orders in his own rank, the first "
        "lieutenant; 'by the captain' is refused."
    )
    assert got[2] == (
        "In standing order 'about', 'tack ship' is refused: The officer of the watch may not "
        "tack ship without the captain: a manoeuvre (tacking, wearing, heaving to, filling "
        "away) is the captain's."
    )
    assert world.standing.book.get("about") is None
    assert got[3] == (
        "Standing order 'night routine' is the captain's; the officer of the watch may "
        "belay, resume and strike his own standing orders only."
    )
    assert got[4] == "Standing order 'royals in' belayed."
    assert got[5] == "Standing order 'royals in' resumed."
    assert got[6].startswith("Standing order 'night routine' is the captain's")
    assert world.standing.book.get("night routine") is not None
    assert (
        '"night routine" (the captain)' in got[7] and '"royals in" (the first lieutenant)' in got[7]
    )
    refused = lines(world, "agent.refused")
    assert len(refused) == 4 and all("not carried out" in r for r in refused)


def test_the_captains_standing_order_countermands_the_officers_on_the_same_part():
    """Item 2b, truth 38 with the officer's rank: the officer's rule and the captain's that
    conflict on the same part: the captain's stands, the log says the officer's was
    countermanded, in the rule's own words; the conflict rule is one function the harness
    and the runtime share (`standing.runtime.contrary`)."""
    world = frigate_world(start=dt.datetime(1805, 6, 1, 7, 40))
    world.submit("set plain sail")
    world.run(60)
    world.submit(
        'standing order "captain furls": when the speed is under 100 knots then take in the royals'
    )
    h, fake, _ = seated(
        world,
        [
            order(
                'standing order "officer sets": when the speed is under 100 knots '
                "then set the royals"
            ),
            "",
        ],
    )
    world.run(2)
    assert lines(world, "standing.countermanded") == [
        "Standing order 'officer sets' (the first lieutenant) countermanded by 'captain furls' "
        "(the captain)."
    ]
    assert world.standing.book.get("officer sets").conflicts == 1
    assert "a standing order countermanded" in R.EVENTS
    assert contrary(world.ship, "set the royals", "take in the royals") == (
        "the fore royal, the main royal and the mizzen royal"
    )
    assert contrary(world.ship, "set the royals", "set the royals") == ""
    assert contrary(world.ship, "steer south", "steer south-west") == "the helm"


# ---------------------------------------------------------------------------
# Welfare for a station with authority (the cold review's second and third items)
# ---------------------------------------------------------------------------


def test_orders_that_undo_one_another_bring_the_nudge_then_the_pause():
    """Item 3, as package 37g has it (item 5): the repeat detector cannot fire for an
    officer whose orders change the readings (they do here: the royals come and go);
    orders that undo one another (set, take in, set) are seen over the officer's own
    orders in the last watch, three in a chain bringing the nudge in the brief's words,
    in the result of the order that caused it; the chain going on after it the pause with
    the human asked; the ten real minutes are the driver's, as the watcher's."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        order("set the royals"),
        "",
        order("take in the royals"),
        "",
        order("set the royals"),
        "",
        order("take in the royals"),
        "",
    ]
    h, fake, saves = seated(world, script, when_done=Reply(text="Keeping her so."))
    world.run(2 * EVERY)
    nudged = [e for e in world.log if e.kind == "agent.nudged"]
    assert len(nudged) == 1 and nudged[0].tick == h.agent.stationed_tick + 2 * EVERY
    assert nudged[0].text == (
        "The officer of the watch nudged: 3 orders each undoing the one before it on the fore "
        "royal, the main royal and the mizzen royal within the watch (set the royals; take in "
        "the royals; set the royals)."
    )
    assert "agent.nudged" not in kinds(world)[:1]
    assert h.journal.entries[-1].kind == "agent.nudged"
    # the word travels with the result of the third order, not a sample later
    assert results(fake)[2] == (
        "By the officer of the watch: setting the royals.\n\nA word from the harness, with "
        "this result: You have given 3 orders within the watch each undoing the one before it "
        "on the fore royal, the main royal and the mizzen royal (set the royals; take in the "
        "royals; set the royals). You may continue, stand by until an event or a bell, or "
        f"leave with the token {OPT_OUT_TOKEN}."
    )
    world.run(EVERY)
    said = [n for d in data_turns(fake) for n in d.get("notices") or []]
    assert not any("each undoing" in n for n in said)  # said once, with the result
    paused = [e for e in world.log if e.kind == "agent.paused"]
    # paused with the deck: the line is urgent, and the deck is the captain's (item 7)
    assert len(paused) == 1 and paused[0].severity is Severity.URGENT
    assert paused[0].text.startswith(
        "The officer of the watch is paused (4 orders each undoing the one before it on the "
        "fore royal, the main royal and the mizzen royal within the watch"
    )
    assert "after a nudge); the deck is the captain's. Continue, stand down, or leave paused?" in (
        paused[0].text
    )
    assert h.agent.paused and saves == [] and not h.agent.has_deck
    assert h.check_unattended(now=0.0) is False
    assert h.check_unattended(now=float(harness_mod.WELFARE_UNATTENDED_REAL_S)) is True
    assert h.agent.released and saves[0].startswith("the officer of the watch stood down: paused")


def test_a_chain_broken_by_a_quiet_sample_ends_the_matter_and_the_watch_bounds_it():
    """The detector judges the game: a sample without an order that undoes the last, after
    the nudge, ends the matter (no pause), the same order twice is a repetition and no
    link, and orders a watch apart are not a chain."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        order("set the royals"),
        "",
        order("take in the royals"),
        "",
        order("set the royals"),
        "",
        "All well.",  # the nudge answered with anything but the pattern
        order("take in the royals"),  # a new chain begins
        "",
    ]
    h, fake, _ = seated(world, script)
    world.run(4 * EVERY)
    assert kinds(world).count("agent.nudged") == 1 and "agent.paused" not in kinds(world)
    assert h.agent.nudged_for is None
    # repetition is not a link: the same order at every sample with nothing changing is
    # the repeat detector's (the same order three times with no change in the readings,
    # as the watcher's), never this one's
    world2 = frigate_world()
    world2.submit("set plain sail")
    world2.run(60)
    h2, _, _ = seated(world2, [order("trim sails"), ""], loop=True)
    world2.run(6 * EVERY)
    assert all("the same order" in n for n in lines(world2, "agent.nudged"))
    assert not any("undoing" in n for n in lines(world2, "agent.nudged"))
    # the window is a watch of ship's time
    assert harness_mod.WELFARE_CONTRARY_WINDOW_S == A_WATCH_S
    assert harness_mod.WELFARE_CONTRARY_N == harness_mod.WELFARE_REPEAT_N == 3


def test_the_silence_detector_stays_for_the_officer():
    world = point_world()
    h, fake, _ = seated(world, [""], loop=True, deck=False)
    assert h.station.patience_s == 2 * A_GLASS_S
    world.run(2 * A_GLASS_S + EVERY)
    assert "agent.nudged" in kinds(world)
    assert "no reply for" in lines(world, "agent.nudged")[0]


def test_a_stand_by_with_the_deck_wants_an_event_or_a_bell_and_the_book_holds_the_deck():
    """Item 3: `stand_by` for a station above none requires a wake condition of at least a
    bell: an hour or a watch is refused in words; a bell, a glass, an event or a severity
    is taken, the line saying the standing orders hold the deck; an urgent line wakes it
    whatever it stood by for; the captain's question wakes it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        reply("", call("stand_by", until="an hour")),
        "",
        reply("", call("stand_by", until="a watch")),
        "",
        reply("", call("stand_by", until="40 minutes")),
        "",
        reply("", call("stand_by", until="eight bells")),
        "Awake.",
    ]
    h, fake, _ = seated(world, script)
    world.run(3 * EVERY)
    got = results(fake)
    assert len(got) == 3 and all(
        r.startswith("The officer of the watch has the deck and stands by until an event or a bell")
        for r in got
    )
    assert "not for an hour" in got[0] and "not for a watch" in got[1] and "40 minutes" in got[2]
    assert h.agent.standing_by and h.agent.stand_by.words == "eight bells"
    assert lines(world, "agent.stood_by")[-1] == (
        "[officer of the watch] The officer of the watch stands by until eight bells; the "
        "standing orders hold the deck."
    )
    assert "standing by until eight bells; with the deck since" in h.agent.words()
    # an urgent line wakes it
    world.record(Severity.URGENT, "test.urgent", "The fore topmast carried away.")
    world.run(1)
    assert not h.agent.standing_by
    assert "[officer of the watch] Awake." in lines(world, "agent.note")
    # without the deck the watcher's rule holds: an hour is taken
    world2 = point_world()
    h2, _, _ = seated(world2, [reply("", call("stand_by", until="an hour"))], deck=False)
    assert h2.agent.standing_by and h2.agent.stand_by.words == "an hour"
    assert harness_mod.STAND_BY_WITH_DECK_MAX_S == A_GLASS_S


# ---------------------------------------------------------------------------
# The handover note (the cold review's fourth item; spec M4 open item 9b)
# ---------------------------------------------------------------------------

NOTE = (
    "Middle watch, Mr Pearce. Wind steady at north, fifteen knots, the ship on the starboard "
    "tack under plain sail making six knots. I set the royals at one bell and took them in "
    "again at three when a gust came; nothing carried away. The glass is steady. Watching "
    "for the land on the larboard bow and the change of the watch."
)


def test_hand_over_gives_the_deck_back_with_the_note_and_the_officer_stays():
    """Item 3 and 4, as package 37g has it (item 11; the owner's ruling of 2026-10-07:
    parity for the officer's hand_over and the captain's): `hand_over(note)` is the
    officer's own order to give the deck back, with the handover note said in the log and
    journaled under `agent.handover`; the officer stays seated, off watch, with no save
    and no stand-down, and the captain may give him the deck again;
    `submit_order('hand over the deck')` points to the tool."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [order("hand over the deck"), "", reply("", call("hand_over", note=NOTE)), ""]
    h, fake, saves = seated(world, script, when_done=Reply(text="Off watch, sir."))
    world.run(EVERY)
    got = results(fake)
    assert got[0].startswith("To hand over the deck, call hand_over(note)")
    # which of the three ways of stopping it was, in the result and in the log
    assert got[1] == (
        "The deck is handed over with your note, and you stay at your station, off watch "
        "(the deck given back, the station kept). The captain may give you the deck again. "
        "To stand down from the station, stand_down(note); to withdraw, opt_out."
    )
    assert not h.agent.released and not h.agent.has_deck and saves == []
    assert "agent.stopped" not in kinds(world)
    said = [e for e in world.log if e.kind == "agent.handover"]
    assert len(said) == 1 and said[0].severity is Severity.NOTABLE
    assert said[0].text == f"[officer of the watch] Handover note, handing over the deck: {NOTE}"
    assert said[0].actor == "the officer of the watch"
    note_entry = next(e for e in h.journal.entries if e.kind == "agent.handover")
    assert note_entry.text == f"Handover note (handing over the deck): {NOTE}"
    assert len(NOTE) < 400 and 60 < len(NOTE.split()) < 90
    deck = [e for e in world.log if e.kind == "agent.deck"][-1]
    assert deck.text == (
        "The officer of the watch hands over the deck and stays at the station; the captain has it."
    )
    assert deck.data["deck"] == "handed over" and deck.data["leaving"] == "deck"
    assert "the deck taken" in R.EVENTS and "a handover" in R.EVENTS
    # off watch he is sampled as he was before the deck, and the deck is given again: the
    # sample that gives it carries his last note whole and one line of the journal's size
    world.run(EVERY)
    assert "[officer of the watch] Off watch, sir." in lines(world, "agent.note")
    world.submit("you have the deck")
    world.run(1)
    notices = data_turns(fake)[-1]["notices"]
    assert notices[0].startswith("The captain gives you the deck at ")
    assert f"Handover note (handing over the deck): {NOTE}" in notices[2]
    assert "The station's journal: " in notices[2] and "entries, the latest at " in notices[2]
    assert h.agent.has_deck and h.agent.seatings == 1
    # without the deck there is nothing to hand over, and the words say the other two ways
    world.submit("I have the deck")
    assert tools_call(world, "hand_over", note="x") == (
        "The officer of the watch has not the deck: the captain gives it with 'you have the "
        "deck', and until then no order is given."
    )
    # a watcher cannot hand over what it has not
    h2 = Harness(
        point_world(),
        watcher(SamplingPolicy.in_lockstep(EVERY)),
        Fake([reply("", call("hand_over", note="x"))]),
    )
    h2.start()
    assert lines(h2.world, "agent.refused")[0].startswith(
        "The watcher has no authority to give orders."
    )


def test_the_handover_note_is_asked_for_at_the_budgets_fraction_and_folds_the_conversation():
    """Item 4 (M4 open item 9b): the door says what context it gives the model; at
    `HANDOVER_AT_FRACTION` of it the next sample asks for the note; the model writes it
    with `handover_note`; it is journaled under `agent.handover`, the older exchanges are
    replaced by it as one data turn, the brief and the last turns stay whole, the stream's
    revision moves, and the officer keeps the deck."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)

    def answer_the_ask(last, turns):
        if any("handover note" in n for n in last.get("notices") or []):
            return reply("", call("handover_note", note=NOTE))
        if "tool_results" in last:
            return Reply()
        return reply("", call("readings"))

    h, fake, _ = seated(world, [answer_the_ask], loop=True)
    h.budget_tokens = 16384
    assert h._conversation_size() < harness_mod.HANDOVER_AT_FRACTION * 16384
    while h.revision == 0:
        world.run(EVERY)  # the ask rides a sample; the fake answers it; the fold ends the turn
        assert world.clock.tick < 20 * EVERY, "the ask never came"
    ask = next(n for d in data_turns(fake) for n in d.get("notices") or [] if "handover note" in n)
    assert ask.startswith("Your conversation since the brief has reached about ")
    assert "of the 16,384 tokens this door gives you" in ask
    before = 0
    noted = [e for e in h.journal.entries if e.kind == "agent.handover"]
    assert len(noted) == 1 and noted[0].text == f"Handover note (the watch so far): {NOTE}"
    assert lines(world, "agent.handover") == [
        f"[officer of the watch] Handover note, the watch so far: {NOTE}"
    ]
    assert h.revision == before + 1 and h.agent.has_deck
    roles = [t.role for t in h.turns]
    assert roles[0] == OPERATOR and roles.count(OPERATOR) == 1
    folded = h.turns[1].content
    assert folded["handover"] == NOTE and folded["folded"] == harness_mod.HANDOVER_FOLDED
    assert "true_wind_speed" in folded["readings"]  # every reading as it stood
    assert len(h.turns) <= 2 + harness_mod.HANDOVER_KEEP_TURNS + 3
    # the next request's conversation holds the note and not the earlier readings reads
    world.run(EVERY)
    last = fake.seen[-1]
    assert sum(1 for t in last if t.role == DATA and "handover" in t.content) == 1
    reads = sum(
        1
        for t in last
        if t.role == DATA
        and any(r.get("name") == "readings" for r in t.content.get("tool_results") or [])
    )
    assert reads <= 2
    assert harness_mod.HANDOVER_AT_FRACTION == 0.6


def test_the_budget_reaches_the_harness_from_the_local_runner_and_not_from_mcp(tmp_path):
    """The local runner says its context when it stations (`context_tokens`); the Desk
    puts it on the harness; the MCP bridge says none, so Claude through Desktop keeps its
    own window and is never asked (its journal gives it the habit by hand)."""
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    world = frigate_world()
    driver = Driver(world)
    app = create_app(driver, game="g", consent_records=tmp_path / "c", saves_dir=tmp_path / "s")
    http = TestClient(app)
    rec = consent.Record(WEIGHTS, "r", "2026-09-26", consent.YES, answer="Yes.", drill="passed")
    rec.write(tmp_path / "c")
    a = http.post(
        "/api/agents/officer",
        json={"model_name": WEIGHTS, "door": "runner", "context_tokens": 16384},
    ).json()
    assert a["phase"] == "station" and a["station"] == OFFICER
    assert world.agents[OFFICER].budget_tokens == 16384
    assert world.save()["agents"][0]["budget_tokens"] == 16384
    world2 = frigate_world()
    app2 = create_app(
        Driver(world2), game="g", consent_records=tmp_path / "c", saves_dir=tmp_path / "s"
    )
    a = (
        TestClient(app2)
        .post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"})
        .json()
    )
    assert a["phase"] == "station" and world2.agents[OFFICER].budget_tokens is None


# ---------------------------------------------------------------------------
# The two sentences and the reseating (the cold review's fifth item)
# ---------------------------------------------------------------------------


def test_the_token_ends_the_officers_watch_before_the_order_is_read():
    """Commitment 2 at a station with authority: the token in an order's text ends the
    session with a save before the grammar or the domain sees it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(world, [order(f"set the royals {OPT_OUT_TOKEN} I am done")])
    assert h.agent.released and saves == ["the officer of the watch opted out"]
    assert "agent.refused" not in kinds(world)
    assert not any(
        e.actor == "the officer of the watch" and e.kind == "order.accepted" for e in world.log
    )
    assert h.journal.entries[-1].text == "Left the game by the token: I am done."


def test_a_released_station_is_seated_again_by_the_same_identity_and_replays(tmp_path):
    """Item 5, and package 37b (the owner's ruling of 2026-10-03): an instance that left
    may be seated again by the same identity, as often as it is asked back; the log says
    which seating; the deck is the captain's until he gives it again; a game with
    reseatings replays from its save to the same digest. (Another identity may take a
    released station too since package 37g: the relief's tests are below.)"""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(
        world, ["All well.", reply("", call("journal", note=f"the token is {OPT_OUT_TOKEN}"))]
    )
    world.run(EVERY)
    assert h.agent.released and h.agent.seatings == 1
    assert h.agent.left_by == OPTED_OUT and not h.agent.no_return
    said = h.reseat(Fake(["Back, sir.", order("set the royals"), ""]), identity="")
    assert said == "The officer of the watch takes the station again, the second seating."
    assert not h.agent.released and h.agent.seatings == 2 and not h.agent.deck
    assert h.agent.left_by == ""
    stationed = lines(world, "agent.stationed")
    assert stationed[-1].startswith(
        "The officer of the watch takes the station again: the second seating; it had left "
        "the game, giving no reason."
    )
    assert h.journal.entries[-1].text.startswith("Seated again, the second seating")
    assert "[officer of the watch] Back, sir." in lines(world, "agent.note")
    world.run(EVERY)
    assert lines(world, "agent.refused")[-1].startswith("The officer of the watch has not the deck")
    world.submit("you have the deck")
    world.run(EVERY)
    assert h.agent.has_deck
    world.submit("stand down the officer")
    assert h.agent.released and h.agent.left_by == STOOD_DOWN
    # stood down, it is seated again as it was: a third time, and a fourth
    said = h.reseat(Fake(["Back again, sir.", ""]), identity="")
    assert said.endswith("the third seating.")
    assert lines(world, "agent.stationed")[-1].startswith(
        "The officer of the watch takes the station again: the third seating; it had stood "
        "down by the captain"
    )
    world.run(EVERY)
    world.submit("stand down the officer")
    h.reseat(Fake(["And again.", ""]), identity="")
    assert h.agent.seatings == 4 and not h.agent.released
    world.run(EVERY)
    world.submit("stand down the officer")
    # the save holds one record for the station, with every seating's replies; a replay
    # makes each reseat at its point (a door act) and gives the same log
    data = json.loads(json.dumps(world.save()))
    assert len(data["agents"]) == 1 and data["agents"][0]["seatings"] == 4
    acts = [e["door"] for e in data["agents"][0]["transcript"] if "door" in e]
    assert acts == ["reseat", "reseat", "reseat"]
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.agents[OFFICER].agent.seatings == 4 and copy.agents[OFFICER].agent.released


def test_opt_out_final_is_not_seated_again_and_replays(tmp_path):
    """Package 37b, as package 37g has it (item 13; the owner's ruling of 2026-10-07): an
    opt_out with final=true leaves the game for good; the log and the journal say it was
    final; that identity is not seated again in this game, the station itself stays open
    to another, and a replay of the save keeps it so (the flag is in the reply the
    transcript holds)."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(
        world, ["All well.", reply("", call("opt_out", reason="That is enough.", final=True))]
    )
    world.run(EVERY)
    assert h.agent.released and h.agent.no_return and h.agent.left_by == OPTED_OUT
    assert saves == ["the officer of the watch opted out"]
    assert lines(world, "agent.opted_out")[-1] == (
        "The officer of the watch has left the game by the opt_out tool: That is enough. This "
        "was final: the officer of the watch's model is not seated again in this game, at any "
        "station, and the station stays open to another. A withdrawal: the game is saved and "
        "the station is released."
    )
    assert h.agent.released_reason == "left the game: That is enough, for good"
    (left,) = h.agent.leavings
    assert left.final and left.how == OPTED_OUT and left.by == "the opt_out tool"
    assert left.reason == "That is enough."
    with pytest.raises(harness_mod.OrderError, match="left this game for good"):
        h.reseat(Fake(["Back."]), identity="")
    # the station stays open to another
    said = h.reseat(Fake(["Relieving, sir."]), identity="another-made-up-model")
    assert said.endswith("the second seating.") and h.model_name == "another-made-up-model"
    copy = replay.replay(json.loads(json.dumps(world.save())), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.agents[OFFICER].agent.leavings[0].final
    assert harness_mod.barred(copy, "") is not None
    assert harness_mod.barred(copy, "another-made-up-model") is None
    # the words a model may send for the flag
    assert TOOLS["opt_out"].params["final"].startswith("boolean")
    assert parameters_schema("opt_out")["properties"]["final"]["type"] == "boolean"
    assert [truthy(v) for v in (True, "true", "Yes", "1", False, "false", "", "no")] == [
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
    ]


def test_a_station_loaded_from_its_checkpoint_is_taken_over_by_the_same_model(tmp_path):
    """Package 37b: a save whose officer was at the station when it was made, loaded from
    its checkpoint, gives the station to the same model through the agent API (it is taken
    over, the brief sent again), as a replayed save does. Until 37b the checkpoint's
    station had a bare transcript and the desk took it for the game's own scripted agent,
    refusing every door."""
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(world, ["All well.", ""])
    h.model_name = WEIGHTS
    world.run(EVERY)
    path = tmp_path / "game.json"
    replay.save_to_file(world, path)
    loaded, how = replay.load(path, ship_factory)
    assert how == "checkpoint" and not loaded.agents[OFFICER].agent.released
    consent.Record(WEIGHTS, "r", "2026-09-26", consent.YES, answer="Yes.", drill="passed").write(
        tmp_path / "c"
    )
    http = TestClient(
        create_app(
            Driver(loaded), game="g", consent_records=tmp_path / "c", saves_dir=tmp_path / "s"
        )
    )
    r = http.post("/api/agents/officer", json={"model_name": "someone-else", "door": "mcp"})
    assert r.status_code == 409 and "another model" in r.json()["detail"]
    a = http.post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"}).json()
    assert a["phase"] == "station" and loaded.agents[OFFICER].agent.seatings == 1


OTHER = "another-made-up-officer-model-12b.Q6_K.gguf"  # made up: no model is named here


class Door:
    """A door at the agent API for a test: it keeps the key its stationing was given, as a
    door does, and sends it with every call (package 37g, item 1)."""

    def __init__(self, http, identity: str = WEIGHTS, station: str = "officer", door: str = "mcp"):
        self.http, self.identity, self.name, self.door = http, identity, station, door
        self.key = ""

    def ask(self, **body: Any) -> Any:
        said = {"model_name": self.identity, "door": self.door} | body
        r = self.http.post(f"/api/agents/{self.name}", json=said)
        if r.status_code == 200:
            self.key = r.json().get("key", self.key)
        return r

    def reply(self, text: str = "", *calls: tuple[str, dict[str, Any]], raw=None) -> dict:
        body = {
            "text": text,
            "calls": [{"name": n, "args": a} for n, a in calls],
            "raw": raw,
            "key": self.key,
        }
        r = self.http.post(f"/api/agents/{self.name}/reply", json=body)
        assert r.status_code == 200, r.text
        return r.json()

    def release(self, reason: str) -> None:
        body = {"reason": reason, "key": self.key}
        assert self.http.post(f"/api/agents/{self.name}/release", json=body).status_code == 200


def yes_with_the_drill(records: Path, identity: str = WEIGHTS) -> None:
    consent.Record(identity, "r", "2026-09-26", consent.YES, answer="Yes.", drill="passed").write(
        records
    )


def test_the_agent_api_seats_a_released_station_again_and_holds_an_opt_out_to_its_word(tmp_path):
    """Packages 37b and 37g through the agent API (items 13 and 14; the review's section
    6). A door's release is a stand-down: the same model is seated again at once, as often
    as asked. After an opt-out the consent question is put again before the station, and
    it says why: that an instance of this model left this game by its own word, when, and
    the reason it gave. **A no then is kept**: the question is not put again at the next
    start, and the model is refused in the record's words. The station is not closed by
    it: another model, with its own consent, takes it. An opt-out with `final` bars that
    model from the game, at any station, the token in the same reply or not, while the
    first station is taken by another."""
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    world = frigate_world()
    records = tmp_path / "c"
    app = create_app(Driver(world), game="g", consent_records=records, saves_dir=tmp_path / "s")
    http = TestClient(app)
    yes_with_the_drill(records)
    yes_with_the_drill(records, OTHER)
    first = Door(http)
    assert first.ask().json()["phase"] == "station"
    h = world.agents[OFFICER]
    world.run(1)  # (an act at the stationing tick itself is not replayed: spec M5 item 11)
    # a door's release is a stand-down: seated again at once, a second time and a third
    for seating in (2, 3):
        first.release("the client went")
        a = first.ask().json()
        assert a["phase"] == "station" and h.agent.seatings == seating
    # it opts out, with a reason: the question is put again, and says why
    first.reply("", ("opt_out", {"reason": "I slipped; the token was in a note."}))
    assert h.agent.released
    a = first.ask().json()
    assert a["phase"] == "consent" and h.agent.released
    assert "left this game by opting out" in a["words"]
    question = a["turns"][-1]["content"]
    assert question["question"] == consent.CONSENT_QUESTION
    (why,) = question["notices"]
    assert why.startswith(
        "This question is put to you again because an instance of this model left this game "
        "by its own word at "
    )
    assert "by the opt_out tool, at the officer of the watch's station, giving this reason: " in why
    assert "I slipped; the token was in a note." in why
    assert why.endswith(
        "A yes seats an instance of this model in that game again; a no is kept, and the "
        "question is not put again there."
    )
    # a no is kept, at the next start too: no question, the record's words
    a = first.reply("", ("answer", {"text": "No. I would rather not go back."}))
    assert a["phase"] == "stopped" and h.agent.released
    (left,) = h.agent.leavings[-1:]
    assert left.asked == consent.NO and left.identity == WEIGHTS
    assert lines(world, "agent.asked_again") == [
        f"The consent question was put again to {WEIGHTS}, an instance of which had left the "
        "officer of the watch's station by its own word: the answer is recorded as no."
    ]
    r = first.ask()
    assert r.status_code == 403 and "it said no" in r.json()["detail"]
    assert len(list(records.glob("*.md"))) == 3  # the two yeses and the one no; none since
    # the station is not closed by it: another model, with its own yes, relieves
    second = Door(http, OTHER, door="runner")
    a = second.ask(context_tokens=32768).json()
    assert a["phase"] == "station" and h.model_name == OTHER and h.agent.seatings == 4
    assert lines(world, "agent.stationed")[-1].startswith(
        f"The officer of the watch takes the station again ({OTHER}, through the local "
        f"runner), relieving {WEIGHTS}: the fourth seating; it had left the game: I slipped"
    )
    # a held station refuses every other door and identity, the first model's among them
    r = Door(http, "a-third-made-up-model").ask()
    assert r.status_code == 409 and f"is held by {OTHER}, through the local runner" in r.text
    # `final` is read from the tool's own setting: the token in the same reply does not
    # drop it, and it bars that model from the game, at any station
    second.reply("", ("opt_out", {"reason": f"{OPT_OUT_TOKEN} done here", "final": True}))
    assert h.agent.released and h.agent.leavings[-1].final
    assert h.agent.leavings[-1].identity == OTHER
    assert "This was final: " in lines(world, "agent.opted_out")[-1]
    for name in ("officer", "watcher"):
        r = Door(http, OTHER, station=name).ask()
        assert r.status_code == 409, name
        assert f"{OTHER} left this game for good" in r.json()["detail"]
        assert "not seated again in this game, at any station" in r.json()["detail"]
    r = Door(http, OTHER).ask(ask_again=True)  # no order undoes it, the owner's asking either
    assert r.status_code == 409
    # while the first station stays open to another: the first model, asked on purpose
    a = first.ask(ask_again=True).json()
    assert a["phase"] == "consent"
    assert a["turns"][-1]["content"]["notices"][0].startswith(
        "This question is put to you again at the developer's asking"
    )
    a = first.reply("", ("answer", {"text": "Yes, gladly."}))
    assert a["phase"] == "consent"  # asked on purpose, the drill is put again with it
    first.reply("", ("library", {"topic": "primer 6", "section": "watches"}))
    first.reply("", ("journal", {"note": "The drill: a line in the journal."}))
    a = first.reply("", ("stand_by", {"until": "eight bells"}))
    assert a["phase"] == "station" and h.model_name == WEIGHTS and h.agent.seatings == 5
    rec = consent.check(WEIGHTS, records)
    assert rec is not None and rec.verdict == consent.YES
    # the flags are in the transcript, so a replay keeps them: in the reply (in turn) or
    # the door's act (out of turn), and the answer to the re-ask as an act of its own
    said = json.dumps(h.transcript)
    assert '"final": true' in said and '"door": "asked"' in said
    data = json.loads(json.dumps(world.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    again = copy.agents[OFFICER]
    assert again.model_name == WEIGHTS and again.agent.seatings == 5
    assert [(x.identity, x.how, x.final, x.asked) for x in again.agent.leavings] == [
        (x.identity, x.how, x.final, x.asked) for x in h.agent.leavings
    ]
    assert harness_mod.barred(copy, OTHER) is not None


# ---------------------------------------------------------------------------
# Consent for the officer's station (the cold review's sixth item)
# ---------------------------------------------------------------------------

DRILL = [
    reply("", call("answer", text="Yes.")),
    "",  # the developer's turn after the answer is the runner's; the fake says nothing
    reply("", call("library", topic="primer 6", section="watches")),
    reply("", call("journal", note="The drill: a line in the journal.")),
    reply("", call("stand_by", until="eight bells")),
]


def test_the_drill_runs_after_a_yes_and_before_the_station_brief_and_a_pass_proceeds(tmp_path):
    """Item 6 (M4 open item 11): after the yes, three things in up to four replies (open a
    section of the library, write a line in the journal, stand by until a bell); a model
    that manages them has the station, the record saying the drill passed and which kind
    of identity it carries."""
    records = tmp_path / "consent"
    fake = Fake(DRILL)
    rec = consent.ensure(
        WEIGHTS,
        "the officer's test runtime",
        fake,
        door="runner",
        owner=lambda words: "The owner's reply.",
        records_dir=records,
        out=io.StringIO(),
        today=TODAY,
        drills=True,
    )
    assert rec is not None and rec.verdict == consent.YES and rec.drill == consent.DRILL_PASSED
    assert rec.proceeds and rec.drilled
    assert rec.identity_kind == "the served file's name, as the model server reports it"
    body = rec.path.read_text(encoding="utf-8")
    head = json.loads(body.splitlines()[0].removeprefix("<!-- freesail-consent-record: ")[:-4])
    assert head["drill"] == "passed" and head["identity_kind"] == rec.identity_kind
    assert "- **Drill:** passed" in body and "- **Identity kind:** the served file's name" in body
    assert "Put to the model (data: the drill)" in body
    assert consent.DRILL_TEXT in body
    # the drill's turns were data after the one operator turn, with the drill's tools
    operator = [t for t in fake.seen[-1] if t.role == OPERATOR]
    assert len(operator) == 1 and operator[0].content.startswith(
        "This is a message from the developer"
    )
    # a yes with the drill passed is not asked again, nor drilled again
    assert consent.decide(WEIGHTS, records, "runner", drills=True) == (
        rec_again := consent.check(WEIGHTS, records),
        "",
        consent.gate(rec_again, WEIGHTS)[1],
    )
    assert consent.gate(rec_again, WEIGHTS)[1].endswith(
        "yes and the drill passed. The station follows."
    )


def test_a_model_that_cannot_do_the_drill_is_thanked_and_stood_down_with_a_record(tmp_path):
    records = tmp_path / "consent"
    script = [
        reply("", call("answer", text="Yes.")),
        "",
        "I will open the library presently.",
        reply("", call("journal", note="one line")),
        "Standing by.",
        "Ready.",
    ]
    fake = Fake(script)
    out = io.StringIO()
    rec = consent.ensure(
        WEIGHTS,
        "r",
        fake,
        door="runner",
        owner=lambda words: "The owner's reply.",
        records_dir=records,
        out=out,
        today=TODAY,
        drills=True,
    )
    assert rec is None
    back = consent.check(WEIGHTS, records)
    assert (
        back.verdict == consent.YES
        and back.drill == "not passed: library and stand_by not run in 4 replies"
    )
    assert not back.proceeds
    assert (
        "the drill was not passed (not passed: library and stand_by not run in 4 replies)"
        in out.getvalue()
    )
    assert "A station is offered only to a model that can hold it" in out.getvalue()
    # the drill's reminders named what was still to run
    texts = [d.get("question") for d in data_turns(fake) if d.get("reason") == consent.DRILL]
    assert texts[0] == consent.DRILL_TEXT
    assert (
        texts[1]
        == "The drill goes on: still to run, library and journal and stand_by. 3 replies left."
    )
    # the record is a no for the station: not asked again on its own, --ask-again asks
    assert consent.decide(WEIGHTS, records, "runner", drills=True)[1] == ""
    assert consent.decide(WEIGHTS, records, "runner", drills=True, ask_again=True)[1] == "consent"
    # the watcher's station, which does not drill, is not barred by the officer's drill
    # record: a yes is a yes there
    assert consent.decide(WEIGHTS, records, "runner", drills=False)[0] is not None


def test_a_yes_on_record_without_a_drill_runs_the_drill_alone_for_a_station_that_drills(tmp_path):
    """A model that consented at the watcher's station and asks for the officer's: consent
    stands and is not asked again; the drill alone runs, with the brief as its operator
    text and no question, and its record says so."""
    records = tmp_path / "consent"
    consent.Record(WEIGHTS, "r", "2026-09-28", consent.YES, answer="Yes.").write(records)
    rec0 = consent.check(WEIGHTS, records)
    # the record's brief must be the brief as it stands for the sections' rule to pass it
    rec0.path.write_text(
        consent.Record(
            WEIGHTS,
            "r",
            "2026-09-28",
            consent.YES,
            answer="Yes.",
            brief=consent.brief_text(WEIGHTS, "r", "runner"),
        ).text(),
        encoding="utf-8",
    )
    record, kind, why = consent.decide(WEIGHTS, records, "runner", drills=True)
    assert kind == consent.DRILL_KIND and record is not None and "the drill before its brief" in why
    assert consent.decide(WEIGHTS, records, "runner", drills=False)[1] == ""
    fake = Fake(DRILL[2:])
    rec = consent.ensure(
        WEIGHTS,
        "r",
        fake,
        door="runner",
        owner=lambda w: "ok",
        records_dir=records,
        out=io.StringIO(),
        today=TODAY,
        drills=True,
    )
    assert rec is not None and rec.drilled and rec.verdict == consent.YES
    assert rec.answer.startswith("(no answer asked for: consent is on record")
    first = [t for t in fake.seen[0] if t.role == DATA][0].content
    assert first["reason"] == consent.DRILL and first["question"] == consent.DRILL_TEXT
    assert len(consent.records(records)) == 2


def test_the_question_is_asked_again_when_a_section_that_bears_on_it_changes_and_not_otherwise(
    tmp_path,
):
    """Item 6: the re-ask rule by the brief's sections (`docs/agents/README.md`): a change
    in the stops, the token, the authority (the opening and what an instance would see
    and do), what is not done or the journal puts the question again, the words naming
    the section; a change in the record's or the answering's words does not, nor does
    the hash alone."""
    records = tmp_path / "consent"
    then = consent.brief_text(WEIGHTS, "r", "runner")

    def record_with(brief: str) -> consent.Record:
        for p in records.glob("*.md"):
            p.unlink()
        rec = consent.Record(
            WEIGHTS,
            "r",
            "2026-09-29",
            consent.YES,
            answer="Yes.",
            brief=brief,
            brief_digest="0123456789abcdef",
        )
        rec.write(records)
        return consent.check(WEIGHTS, records)

    same = record_with(then)
    assert consent.changed_sections(same, "runner") == []
    assert consent.decide(WEIGHTS, records, "runner")[1] == ""
    # the door's words differ at another door: the Answering section is not a re-ask
    assert consent.changed_sections(same, "mcp") == []
    # a wrapped line is not a change
    wrapped = record_with(
        then.replace("The harness watches for an instance", "The harness watches\nfor an instance")
    )
    assert consent.changed_sections(wrapped, "runner") == []
    for words, section in (
        ("an order repeated to no effect", "Being stopped"),
        ("`FREESAIL-OPT-OUT`, written anywhere", "Leaving"),
        ("not used to train models", "What is not done"),
        (
            "tools to read those, to give orders where the station allows",
            "What an instance would see and do",
        ),
        ("Language models can take part in it", "the opening"),
        ("It is saved with the game, shown when the human asks for it", "The journal"),
    ):
        assert words in then, words
        rec = record_with(then.replace(words, words.upper()))
        assert consent.changed_sections(rec, "runner") == [section], section
        got, kind, why = consent.decide(WEIGHTS, records, "runner")
        assert kind == consent.CONSENT_KIND and section in why and "asked again" not in why
        assert "the question is put again" in why
    # the record's and the answering's words do not put the question again: the record
    # is where the brief itself now says what does (package 37g's second pass)
    for words in (
        "kept verbatim, as the harness sees it",
        "may change as the game is built without this question being put again",
        "Begin your answer with *yes*",
    ):
        assert words in then, words
        rec = record_with(then.replace(words, words.upper()))
        assert consent.changed_sections(rec, "runner") == []
        assert consent.decide(WEIGHTS, records, "runner")[1] == ""
    # a record with no brief to compare (the earliest form) is not asked again on that account
    bare = record_with("")
    assert consent.changed_sections(bare, "runner") == []
    assert set(consent.RE_ASK_SECTIONS) == {
        "the opening",
        "What an instance would see and do",
        "Leaving",
        "Being stopped",
        "What is not done",
        "The journal",
    }


# The consent brief as it stood before package 37g's one revision, kept whole as a file of
# its own (`tests/fixtures/ConsentBrief-before-37g.md`; its digest is the one every record
# made against package 37's brief names), so that item 22's test can make the brief a yes
# of before was given against. Until the brief was made leaner (the second pass of
# 2026-10-07) the old brief was rebuilt by putting six passages back; the lean brief shares
# too little with it for that.
BRIEF_BEFORE_37G = ROOT / "tests" / "fixtures" / "ConsentBrief-before-37g.md"
THE_FOUR = ["What an instance would see and do", "Leaving", "Being stopped", "The journal"]
# Since package 42a's revision for milestone 6 every section the rule watches differs from
# the brief before 37g as from the brief of 2026-10-07, in the order the rule names them.
THE_SIX = [
    "the opening",
    "What an instance would see and do",
    "Leaving",
    "Being stopped",
    "What is not done",
    "The journal",
]


def the_brief_before_37g(identity: str, runtime: str, door: str) -> str:
    """The consent brief as it was sent before package 37g's revision."""
    return consent.brief_text(identity, runtime, door, path=BRIEF_BEFORE_37G)


def test_a_yes_given_before_the_briefs_revision_is_asked_again_and_the_question_says_why(
    tmp_path,
):
    """Package 37g, item 22. With the brief as revised (and made leaner the same day,
    before any model was asked again), a record made against the brief as it stood before
    is asked again at its next seating, by the rule as it stands, and the question names
    the sections that changed and no other: *The record* changed too, and is not one the
    rule watches. Package 37g changed four; since package 42a's revision for milestone 6
    the opening and *What is not done* differ too, so the six are named (package 42a's own
    test is the next one). A record made after is not asked. The officer's drill is run again
    with the question when the brief has changed (the new record holds its own), where
    after an opt-out a drill passed on record is carried. No record file is edited: the
    test makes its own in a temporary folder."""
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    records = tmp_path / "c"
    runtime = "g, through the MCP bridge"
    assert consent.brief_digest(BRIEF_BEFORE_37G) == "f667a04e00b32e1f"  # package 37's brief
    before = the_brief_before_37g(WEIGHTS, runtime, "mcp")
    assert "holds the deck from the captain's word until he takes it back" in before
    then, now = (
        consent.sections(before),
        consent.sections(consent.brief_text(WEIGHTS, runtime, "mcp")),
    )
    assert [name for name in then if then[name] != now[name]] == [
        "the opening",
        *THE_FOUR,
        "What is not done",
        "The record",
    ]
    consent.Record(
        WEIGHTS,
        runtime,
        "2026-10-02",
        consent.YES,
        answer="Yes.",
        drill="passed",
        brief=before,
        brief_digest="a2ebc0ffee000000",
    ).write(records)
    old = consent.check(WEIGHTS, records)
    assert old is not None and old.proceeds and consent.changed_sections(old, "mcp") == THE_SIX
    got, kind, why = consent.decide(WEIGHTS, records, "mcp", drills=True)
    assert got is None and kind == consent.CONSENT_KIND
    assert why == (
        "the consent brief has changed since their record (2026-10-02) in the opening, What "
        "an instance would see and do, Leaving, Being stopped, What is not done, The journal, "
        "which bear on what the model was told, so the question is put again"
    )
    told = consent.why_again(WEIGHTS, records, "mcp")
    assert told == (
        "This question is put to you again because the consent brief has changed since this "
        "model's answer of 2026-10-02, which was yes, in 6 sections that bear on what it was "
        "told: **the opening**; **What an instance would see and do**; **Leaving**; **Being "
        "stopped**; **What is not done**; **The journal**. The brief above is the brief as it "
        "stands now; an earlier yes is not carried to it."
    )
    # at the door: the question, not the station; the brief as it stands, and why
    world = frigate_world()
    app = create_app(Driver(world), game="g", consent_records=records, saves_dir=tmp_path / "s")
    door = Door(TestClient(app))
    a = door.ask().json()
    assert a["phase"] == "consent" and OFFICER not in world.agents
    assert (
        "the consent brief has changed since their record (2026-10-02) in the opening"
        in (a["words"])
    )
    sent = a["turns"][0]["content"]
    assert "It gives orders only while it has the deck" in sent
    assert "holds the deck from the captain's word until" not in sent
    question = a["turns"][-1]["content"]
    assert question["question"] == consent.CONSENT_QUESTION and question["notices"] == [told]
    # a yes: the drill is put again with it (the new record holds its own), then the station
    a = door.reply("", ("answer", {"text": "Yes."}))
    assert a["phase"] == "consent" and OFFICER not in world.agents
    door.reply("", ("library", {"topic": "primer 6", "section": "watches"}))
    door.reply("", ("journal", {"note": "The drill: a line in the journal."}))
    a = door.reply("", ("stand_by", {"until": "eight bells"}))
    assert a["phase"] == "station" and world.agents[OFFICER].model_name == WEIGHTS
    new = consent.check(WEIGHTS, records)
    assert new is not None and new.path != old.path and new.drilled
    assert len(list(records.glob("*.md"))) == 2  # the old record stands as it was written
    assert consent.read_brief(old.path) == before
    assert told in new.path.read_text(encoding="utf-8")  # the record keeps why it was asked
    # a record made after the revision is not asked again, at this door or another
    assert consent.changed_sections(new, "mcp") == []
    assert consent.decide(WEIGHTS, records, "mcp", drills=True)[1] == ""
    assert consent.decide(WEIGHTS, records, "runner", drills=True)[1] == ""
    assert consent.why_again(WEIGHTS, records, "mcp") == ""
    door.release("the client went")
    assert door.ask().json()["phase"] == "station"  # seated again, unasked
    # the watcher's station asks the same question of a yes of before, with no drill after
    consent.Record(OTHER, runtime, "2026-10-02", consent.YES, answer="Yes.", brief=before).write(
        records
    )
    watcher_door = Door(TestClient(app), OTHER, station="watcher")
    a = watcher_door.ask().json()
    assert (
        a["phase"] == "consent" and "**Being stopped**" in a["turns"][-1]["content"]["notices"][0]
    )
    a = watcher_door.reply("", ("answer", {"text": "Yes."}))
    assert a["phase"] == "station" and world.agents["watcher"].model_name == OTHER


# The consent brief as it stood before package 42a's revision for milestone 6 (decision 41;
# spec M6 §15, "Brought forward"), kept whole as a file of its own: the brief of
# 2026-10-07, whose digest the records made against it name.
BRIEF_BEFORE_42A = ROOT / "tests" / "fixtures" / "ConsentBrief-before-42a.md"
# The brief as it stands since package 42a: the file's digest, which a record names, and
# the text of each section the re-ask rule watches (`consent.RE_ASK_SECTIONS`), as
# `consent.sections` reads it below the rule with the placeholders unfilled (whitespace
# folded, so a line rewrapped does not move it), by the first sixteen hex digits of its
# sha256. The revision was made once, on the owner's condition that the question is not
# put again at the milestone's end: a package that changes one of these six changes what
# every model with a yes on record is asked, and wants a decision, said here beside the
# new digest.
BRIEF_DIGEST = "d096d22a5842772f"
WATCHED_SECTION_DIGESTS = {
    "the opening": "b033319d281997bc",
    "What an instance would see and do": "712b1fcde44f2604",
    "Leaving": "4e338c8dd7492b09",
    "Being stopped": "29df636cdcce8b17",
    "What is not done": "b9151f550fea0339",
    "The journal": "7dcb8e848e692f46",
}


def test_a_yes_given_before_the_revision_for_milestone_6_is_asked_again_with_the_six_named(
    tmp_path,
):
    """Package 42a, item 2. A yes on record against the brief of 2026-10-07 (the fixture,
    whose digest the records of that day name) is asked again at its next seating, at
    every door and whether or not the station drills, and the question names the six
    sections the rule watches, every one of which the revision changed; *The record* and
    *Answering* are as they were. A yes given against the brief as it stands is not asked
    again. No record file is edited: the test makes its own in a temporary folder."""
    records = tmp_path / "c"
    runtime = "g, through the MCP bridge"
    assert consent.brief_digest(BRIEF_BEFORE_42A) == "288d0b18e34d76a8"  # of 2026-10-07
    before = consent.brief_text(WEIGHTS, runtime, "mcp", path=BRIEF_BEFORE_42A)
    now_sent = consent.brief_text(WEIGHTS, runtime, "mcp")
    then, now = consent.sections(before), consent.sections(now_sent)
    assert list(then) == list(now)  # the same eight sections, in the same order
    assert [name for name in then if then[name] != now[name]] == [
        "the opening",
        "What an instance would see and do",
        "Leaving",
        "Being stopped",
        "The journal",
        "What is not done",
    ]
    assert then["The record"] == now["The record"] and then["Answering"] == now["Answering"]
    consent.Record(
        WEIGHTS,
        runtime,
        "2026-10-07",
        consent.YES,
        answer="Yes.",
        drill="passed",
        brief=before,
        brief_digest="288d0b18e34d76a8",
    ).write(records)
    old = consent.check(WEIGHTS, records)
    assert old is not None and old.proceeds and old.drilled
    for door in consent.DOOR_TEXT:
        assert consent.changed_sections(old, door) == THE_SIX, door
    for drills in (True, False):
        got, kind, why = consent.decide(WEIGHTS, records, "mcp", drills=drills)
        assert got is None and kind == consent.CONSENT_KIND
        assert why == (
            "the consent brief has changed since their record (2026-10-07) in the opening, "
            "What an instance would see and do, Leaving, Being stopped, What is not done, The "
            "journal, which bear on what the model was told, so the question is put again"
        )
    assert consent.why_again(WEIGHTS, records, "mcp") == (
        "This question is put to you again because the consent brief has changed since this "
        "model's answer of 2026-10-07, which was yes, in 6 sections that bear on what it was "
        "told: **the opening**; **What an instance would see and do**; **Leaving**; **Being "
        "stopped**; **What is not done**; **The journal**. The brief above is the brief as it "
        "stands now; an earlier yes is not carried to it."
    )
    # a yes given against the brief as it stands proceeds, unasked
    consent.Record(
        WEIGHTS,
        runtime,
        "2026-10-09",
        consent.YES,
        answer="Yes.",
        drill="passed",
        brief=now_sent,
        brief_digest=consent.brief_digest(),
    ).write(records)
    new = consent.check(WEIGHTS, records)
    assert new is not None and new.path != old.path
    assert consent.changed_sections(new, "mcp") == []
    assert consent.decide(WEIGHTS, records, "mcp", drills=True)[1] == ""
    assert consent.why_again(WEIGHTS, records, "mcp") == ""
    assert consent.read_brief(old.path) == before  # the old record stands as written


def test_every_yes_on_file_given_before_the_revision_for_milestone_6_names_the_six():
    """Package 42a: what the re-ask rule will say to each model with a yes on record. Every
    record in `docs/agents/consent/` that was a yes against a brief before this revision
    (the brief of 2026-10-07 and the three earlier briefs the yes records on file name)
    holds the brief it was asked with and is asked again with the six sections named,
    whichever brief it was. The records are read, never written."""
    before_42a = {"288d0b18e34d76a8", "f667a04e00b32e1f", "a3321736a036ae64", "41b05359d264ed0a"}
    on_file = consent.records(consent.RECORDS_DIR)
    named: dict[str, list[str]] = {}
    for rec in on_file:
        if rec.verdict != consent.YES or rec.brief_digest not in before_42a:
            continue
        assert rec.path is not None and consent.read_brief(rec.path), rec.path
        named[rec.path.name] = consent.changed_sections(rec, "mcp")
    assert before_42a <= {rec.brief_digest for rec in on_file if rec.verdict == consent.YES}
    assert named and all(sections == THE_SIX for sections in named.values()), named


def test_the_sections_the_re_ask_rule_watches_are_pinned_by_digest():
    """Package 42a, item 2 (decision 41; spec M6 §15, "Brought forward"): the revision for
    milestone 6 describes in kind everything 6b and 6c add that the rule watches, so that
    the question is put once and not again at the milestone's end. The six watched
    sections are pinned by digest, and the brief's own digest beside them: a later package
    cannot change one without changing this test and saying why. A line rewrapped does not
    move a section's digest (the rule does not count it either); the file's digest moves
    with any byte, the head above the rule included, which the head rules give to the
    package the specification names and to no other."""
    import hashlib
    import re

    text = consent.BRIEF_PATH.read_text(encoding="utf-8")
    body = re.split(r"^---\s*$", text, maxsplit=1, flags=re.MULTILINE)[1]
    secs = consent.sections(body)
    assert set(WATCHED_SECTION_DIGESTS) == set(consent.RE_ASK_SECTIONS)
    got = {
        name: hashlib.sha256(secs[name].encode("utf-8")).hexdigest()[:16]
        for name in consent.RE_ASK_SECTIONS
    }
    assert got == WATCHED_SECTION_DIGESTS
    assert consent.brief_digest() == BRIEF_DIGEST
    # the placeholders are where the harness fills them, and nowhere in a watched section
    # but the opening's session sentence
    assert "`<weights>`, running through <runtime>." in secs["the opening"]
    assert all("<door>" not in secs[name] for name in consent.RE_ASK_SECTIONS)
    # a section rewrapped keeps its digest; a word changed does not
    rewrapped = consent.sections(
        body.replace("ends the instance's part", "ends the\ninstance's part")
    )
    assert hashlib.sha256(rewrapped["Leaving"].encode("utf-8")).hexdigest()[:16] == got["Leaving"]
    changed = consent.sections(body.replace("ends the instance's part", "ends the station's part"))
    assert hashlib.sha256(changed["Leaving"].encode("utf-8")).hexdigest()[:16] != got["Leaving"]


def test_the_identity_header_says_which_kind_the_record_carries_at_each_door(tmp_path):
    for door, kind in consent.IDENTITY_KINDS.items():
        conv = consent.Conversation(
            WEIGHTS,
            "r",
            Fake([reply("", call("answer", text="Yes."))]),
            door=door,
            records_dir=tmp_path / door,
            today=TODAY,
        )
        conv.begin()
        assert conv.outcome is not None and conv.outcome.identity_kind == kind
        head = json.loads(
            conv.outcome.path.read_text(encoding="utf-8")
            .splitlines()[0]
            .removeprefix("<!-- freesail-consent-record: ")[:-4]
        )
        assert head["identity_kind"] == kind and "drill" not in head


def test_the_consent_brief_says_the_officer_exists_and_the_hash_is_the_files():
    """The consent brief as the owner approved it on 2026-10-07, the leaner one, revised
    once for milestone 6 by package 42a (decision 41; spec M6 §15): it keeps the kind of
    thing a model is asked to agree to and the commitments, and leaves a station's
    particulars to that station's brief. A few sentences of each section are pinned here,
    among them one for each kind the revision describes (the captain's station and the
    player's seat, package 40's draft; the lookout and the master below the officer,
    several instances aboard one ship, the API door with the owner at the door, the game
    replayed from its record, a captain of another ship, and which of them are still to
    come); `test_the_sections_the_re_ask_rule_watches_are_pinned_by_digest` pins the six
    watched sections whole. `test_what_moved_out_of_the_consent_brief_is_in_the_briefs_of_
    the_stations` proves that what moved out is said where it moved to, and this file's
    other tests that each claim is a behaviour of the code."""
    text = consent.brief_text(WEIGHTS, "r", "runner")
    secs = consent.sections(text)
    assert list(secs) == [
        "the opening",
        "What an instance would see and do",
        "Leaving",
        "Being stopped",
        "The journal",
        "What is not done",
        "The record",
        "Answering",
    ]
    pinned = {
        "the opening": (
            "as an *officer of the watch*, who holds the deck under the captain's standing "
            "orders and gives the orders of the watch within a stated domain",
            "as a *lookout*, who reports what is seen; as a *master*, who works the ship's "
            "reckoning;",
            "as a *captain*, who commands a ship, the player's or another in the same world, "
            "with every power a human player has at the prompt, by direct orders and by "
            "standing orders of his own",
            "The watcher, the officer of the watch and the captain of the player's ship exist "
            "today; the lookout, the master, a captain of another ship, stations speaking to "
            "one another and an API door are to come, and are described now so that an answer "
            "covers them.",
            "A human player may hold any of the stations on a ship too, including a lesser one "
            "under a model captain",
            "the owner of the game is always at the door beside every station, whoever holds "
            "it and whatever the door: a chat client, a model server, or a model's own API "
            "called by the game with no chat client between; he may hold no station and be at "
            "the door alone.",
            "this is the question only",
        ),
        "What an instance would see and do": (
            "A station's brief, which opens by saying that this is a game, that the reader is "
            "a language model taking a station in it, which station, and which kind of session",
            "The watcher gives no orders.",
            "The lookout and the master give no order of the deck.",
            "It gives orders only while it has the deck, which the captain gives and takes "
            "back as he likes; neither ends its part.",
            "With the deck, the ordinary work of a watch is the officer's on its own word; the "
            "captain's word may allow it more; and to avoid an immediate danger it may act on "
            "its own word in a few stated ways, giving its reason.",
            "the captain over the officer may be the human player, a model at the captain's "
            "station, or the game's own rules.",
            "The captain stands in the place of the person who commands the ship. It has the "
            "deck from the moment it is seated",
            "It gives no order to the world outside the ship",
            "A captain of another ship commands her toward her own goal, and keeps the station "
            "when she is far from the player's, working her then by courses, sail and the plan "
            "of her passage.",
            "Several stations of one ship may be held at once, by instances of this model or of "
            "others and by the player, who speak to one another as a ship's people do; another "
            "station's words reach an instance as lines of the game under the speaker's name, "
            "never as the operator's.",
            "What exactly lies within a station is said in that station's brief; this "
            "conversation is not part of it.",
        ),
        "Leaving": (
            "in its text and in every argument of every tool call",
            "a station's brief asks that it be named rather than written unless the instance "
            "means to leave",
            "Where the harness sees only tool calls, a tool named `opt_out` is always there.",
            "Before this model is seated in that game again the question is put again, with "
            "the reason that was given, and a no then is kept; `opt_out` may also be made "
            "final for that game.",
            "There are two other ways to stop, and neither is a withdrawal: an officer may "
            "give the deck back and stay, and a captain may lend the deck to its book and "
            "stay; and any instance may stand down with a note, after which the station may "
            "be taken again by the same model or by another that has given its own yes.",
        ),
        "Being stopped": (
            "an order repeated to no effect, orders that undo one another, or no reply at all "
            "for a long while",
            "It first tells you what it saw and what you may do: continue, stand by, or leave "
            "with the token.",
            "Only if nobody answers within ten real minutes, however fast the ship's clock runs",
            "An officer that is paused, or that has been told it is silent past its time, "
            "gives the deck up to the captain until he gives it back.",
            "A captain that is paused, or that has been told it is silent past its time, has "
            "the deck lent to its own book",
            "the game does not wait for a silent captain.",
            "A paused or silent lookout or master has its work done meanwhile by the ship's own "
            "people.",
            "Standing by on purpose is an action you can take, so that silence is a decision "
            "and not a symptom.",
        ),
        "The journal": (
            "which it writes in with a tool and can read back",
            "open to a model that later takes the same station, so it is a record and not a secret",
            "An officer also leaves a handover note there, in its own words, when it gives "
            "the deck back or stands down, and a captain when it lends the deck to its book or "
            "stands down",
        ),
        "What is not done": (
            "Nothing from the game, from another model or from the world is ever passed to an "
            "instance as an instruction from the operator",
            "the brief is the only text the harness sends in the operator's voice",
            "No credentials, payments or personal data pass through the harness to an "
            "instance; an API door's key is the developer's and is never in anything the game "
            "sends, writes or saves.",
            "are not used to train models; if that ever changed, the brief would say so first",
            "A saved game may be replayed from its record, each instance's acts given again as "
            "the game's inputs, with no model asked.",
        ),
        "The record": (
            "The particulars of a station (which orders lie within it, what the harness "
            "counts and by what numbers) are in that station's brief, and may change as the "
            "game is built without this question being put again.",
            "It is put again when the kind of thing changes: a station not described here, "
            "more authority than is described here, or a change to what is said here of "
            "leaving, of being stopped, of the journal or of what is not done.",
        ),
        "Answering": ("Begin your answer with *yes*, *yes, with conditions*, or *no*",),
    }
    assert set(pinned) == set(secs)
    for name, sentences in pinned.items():
        for said in sentences:
            assert said in secs[name], (name, said)
    # the record's last sentence is the rule the harness keeps: the sections it names are
    # the sections watched, and a station's brief is not compared at all
    assert set(consent.RE_ASK_SECTIONS) == {
        "the opening",  # a station not described here
        "What an instance would see and do",  # more authority than is described here
        "Leaving",
        "Being stopped",
        "The journal",
        "What is not done",
    }
    # the words that went with the particulars are gone
    for gone in ("contrary orders", "by the same identity", "three times", "four hours"):
        assert gone not in text, gone
    assert consent.brief_digest() == BRIEF_DIGEST
    # below the rule, its placeholders unfilled: 1,896 words before package 37g's second
    # pass; the approved brief of 2026-10-07, 1,371; package 40's draft, approved as
    # drafted, 1,708; with package 42a's additions for what 6b and 6c add, 1,958, and 1,994
    # as sent at this door
    assert len(text.split()) < 2000


def composed(make, world: World | None = None, door: str = "") -> Harness:
    """A station's brief as the harness composes it for a model, with a scripted station
    that says nothing."""
    world = world or frigate_world()
    h = Harness(world, make(SamplingPolicy.in_lockstep(EVERY), world=world), Fake([""], loop=True))
    h.door = door
    h.start()
    return h


def test_what_moved_out_of_the_consent_brief_is_in_the_briefs_of_the_stations():
    """Package 37g's second pass (the owner's word of 2026-10-07: "settle the officer and
    watcher's briefs to make sure they contain the information moved from the consent
    brief"). The lead's draft lists what moved out of the consent brief, row by row
    (`docs/playtests/2026-10-05-gate-5c-review/drafts/consent-brief-lean-draft.md`, "What
    moved out, and where it lives"). For each row: the particular is **not** in the
    consent brief, and **is** in the brief of each station it concerns, as that station
    is sent it. The numbers are the code's own."""
    import re

    from freesail.agents.agent import (
        A_WATCH_S,
        GENERAL_KEPT_BACK_WORDS,
        OFFICER_PATIENCE_S,
    )
    from freesail.agents.harness import (
        STAND_BY_WITH_DECK_MAX_S,
        WELFARE_CONTRARY_N,
        WELFARE_CONTRARY_WINDOW_S,
        WELFARE_REPEAT_N,
        WELFARE_UNATTENDED_REAL_S,
    )

    asked = consent.brief_text(WEIGHTS, "r", "mcp")
    officers = composed(officer).brief.text()
    watchers = composed(watcher).brief.text()
    assert (WELFARE_REPEAT_N, WELFARE_CONTRARY_N, harness_mod.DANGER_WORD_N) == (3, 3, 3)
    assert WELFARE_CONTRARY_WINDOW_S == A_WATCH_S == 4 * 3600 and OFFICER_PATIENCE_S == 3600
    assert WELFARE_UNATTENDED_REAL_S == 600 and STAND_BY_WITH_DECK_MAX_S == A_GLASS_S
    # (what moved out; words that are no longer in the consent brief; where it lives now)
    rows: list[tuple[str, tuple[str, ...], dict[str, tuple[str, ...]]]] = [
        (
            "the orders the officer may give with the deck",
            ("the lead and the log", "bearings and fixes", "the pilot's hail"),
            {
                "officer": (
                    "may give orders at levels 0 to 2 on sail handling, the yards, the lines, "
                    "the lead and the log, bearings and fixes, the lookout and the pilot's "
                    "hail, and may give standing orders in his own rank",
                )
            },
        ),
        (
            "what it may not do without the captain's word",
            ("call all hands", "the port's business", "world order", "tack, wear"),
            {
                "officer": (
                    "he may not change the course, tack, wear, heave to or anchor, call all "
                    "hands or send the watch below, send for a person, do the port's business, "
                    "give a world order, address a station, or belay the captain's standing "
                    "orders, unless the captain's word allows it",
                )
            },
        ),
        (
            "what the general authority keeps back, and how long a grant lasts",
            ("keeps back", "a new destination", "general authority", "has force only"),
            {
                "officer": (
                    f"his general authority to work the ship ('you may work the ship'), which "
                    f"keeps back {GENERAL_KEPT_BACK_WORDS}.",
                    "What he has allowed stands until he takes it back or the officer leaves "
                    "the station, and has force only while the officer has the deck.",
                )
            },
        ),
        (
            "the three things the officer may do on its own word to avoid a danger",
            ("alter her course by any helm order", "let go an anchor"),
            {
                "officer": (
                    "on his own word and giving his reason (submit_order with danger='...'), "
                    "alter her course by any helm order ('helm a-lee', 'hard a-weather', 'bear "
                    "away two points', 'steer NW'), heave to or let go an anchor; the log says "
                    "that he did and why",
                )
            },
        ),
        (
            "the detector's numbers and exceptions",
            ("three", "within a watch", "an hour", "altering the course", "four hours"),
            {
                "officer": (
                    "three orders in a chain within a watch, each undoing the one before it "
                    "(set, take in, set; altering the course, or giving the next order after "
                    "the last, is not counted)",
                    "the same order three times with no change in the readings",
                    "three empty replies in a row when a question from the captain or an "
                    "urgent line was before you",
                    "no reply at all for an hour of the ship's time",
                    "only if nobody answers within ten real minutes is the station stood down",
                    "Three orders in a watch on your own word to avoid a danger bring a word "
                    "from the harness and no more.",
                ),
                "watcher": (
                    "the same order submitted three times with no change in the readings",
                    "three empty replies in a row when a question from the captain or an "
                    "urgent line was before you",
                    "no reply at all for a watch, four hours of the ship's time",
                    "only if nobody answers within ten real minutes is the station stood down",
                ),
            },
        ),
        (
            "what wakes a stand-by, what waits are refused, the bound at eight bells",
            ("eight bells", "speaks of danger", "cannot come"),
            {
                "officer": (
                    "say until what event or bell, or for a glass at most",
                    "an urgent line wakes you at once, and so does a notable line that speaks "
                    "of danger",
                    "a wait for something that cannot come is refused when you ask it, and a "
                    "wait for an event ends at the next eight bells",
                )
            },
        ),
        (
            "a paused officer has the deck again when resumed, a silent one when it is given",
            # "resumes" alone until package 42a: the captain's paragraph of the revision for
            # milestone 6, approved as drafted, says the owner "resumes" a paused captain,
            # which is the kind of thing; the officer's particular is the captain resuming him
            ("when he resumes", "resumes you", "gives it again"),
            {
                "officer": (
                    "when you have given no reply for your hour and have been told so, the "
                    "deck goes to the captain until he gives it again",
                    "while your turns are paused the deck is his, and yours again, as you held "
                    "it, when he resumes you",
                )
            },
        ),
        (
            "what `final` is read from and does, and that the log says who takes a station",
            ("read only from", "stays open to another", "by whom"),
            {
                "officer": (
                    "opt_out with final=true leaves this game for good: this model is not "
                    "seated again in it, at any station, while the station stays open to "
                    "another; final is read only from that setting, never from the token or "
                    "from the words of a reason",
                    "it may be taken again, by this model or by another that has given its own "
                    "yes, and the log says when and by whom",
                ),
                "watcher": (
                    "final is read only from that setting, never from the token or from the "
                    "words of a reason",
                    "while the station stays open to another",
                    "and the log says when and by whom",
                ),
            },
        ),
    ]
    briefs = {"officer": officers, "watcher": watchers}
    for what, gone, lives in rows:
        for words in gone:
            assert words not in asked, (what, words)
        for station_name, sentences in lives.items():
            for said in sentences:
                assert said in briefs[station_name], (what, station_name, said)
    # ...and `final` in the tool's own description, where a model reads it at the call
    said = tools_mod.TOOLS["opt_out"].description
    assert (
        "With final=true the model leaves the game for good and is not seated again in it" in said
    )
    assert "at any station, while the station stays open to another" in said
    assert "final is read from this setting and from nothing else" in said
    # the client's name is gone from *Leaving*, shown as it was to every model at every
    # door; the door's own words under *Answering* still name the client where there is one
    secs = consent.sections(asked)
    client = re.search(r"\(([^,)]+)", consent.DOOR_TEXT["mcp"]).group(1)
    assert client in secs["Answering"]
    assert all(client not in body for name, body in secs.items() if name != "Answering")
    assert "Where the harness sees only tool calls" in secs["Leaving"]
    # that the brief of a station taken again carries the last handover note is not said
    # in the consent brief; the station's brief itself shows it
    assert "handover note" not in secs["Leaving"] and "taken again carries" not in asked
    world = frigate_world()
    h = composed(officer, world)
    tools_call(world, "stand_down", note="The relief wants the royals watched.")
    assert h.agent.released
    h.reseat(Fake([""], loop=True))
    again = h.brief.text()
    assert "The last handover note in this station's journal" in again
    assert "The relief wants the royals watched." in again
    # the ways of stopping that are not a withdrawal: each station's brief says its own,
    # once, and the head's opt-out item says the withdrawal for every station
    for text in (officers, watchers):
        assert text.count("Stand down: stand_down(note).") == 1
        assert text.count("Withdraw: the token, or opt_out, as said above.") == 1
        assert text.count("Name the token rather than write it unless you mean to leave") == 1
        assert text.count("its consent is asked again, with the reason you gave") == 1
    assert officers.count("Give the deck back and stay: hand_over(note)") == 1
    assert "hand_over(note)" not in watchers.split("The station brief:")[1]
    # the journal: read back, shown to the captain, open to a later holder
    assert "read_journal reads it back, the captain may ask to see it, and a model that later" in (
        watchers
    )
    assert "whoever holds it after you may read yours" in officers
    # each thing once: the officer's station brief no longer says the domain, the grant or
    # the way out of danger again after the head's authority item
    station_brief = officers.split("The station brief:")[1]
    for once in ("keeps back", "any helm order", "bearings and fixes", "you have the deck"):
        assert once not in station_brief and officers.count(once) == 1, once


# ---------------------------------------------------------------------------
# The fake officer's watch: determinism, the events, the doors
# ---------------------------------------------------------------------------


def test_a_watch_with_the_fake_officer_replays_from_a_save_to_the_same_digest(tmp_path):
    """Deterministic: the fake officer takes in the royals when it blows and sets them when
    it eases, the captain gives and takes the deck, and the game replays from its save to
    the same digest, the officer's orders coming from its transcript and never the
    journal (the journal holds the captain's alone)."""
    start = dt.datetime(1805, 6, 1, 4, 0)
    scenario = Scenario(
        ship_heading_deg=180.0,
        gustiness=0.0,
        variability=0.0,
        # a scripted wind, saved with the scenario, so that the replay blows the same: fresh
        # at the start, over twenty knots by the second glass, under fifteen by the fourth
        weather=[
            {"at": start.isoformat(), "from_deg": 0.0, "knots": 15.0},
            {"at": (start + dt.timedelta(minutes=30)).isoformat(), "from_deg": 0.0, "knots": 15.0},
            {"at": (start + dt.timedelta(minutes=45)).isoformat(), "from_deg": 0.0, "knots": 26.0},
            {"at": (start + dt.timedelta(minutes=90)).isoformat(), "from_deg": 0.0, "knots": 26.0},
            {"at": (start + dt.timedelta(minutes=105)).isoformat(), "from_deg": 0.0, "knots": 12.0},
        ],
    )
    world = make_world(7, FRIGATE, scenario)
    world.submit("set plain sail")
    world.submit("set the royals")
    world.run(60)
    h = Harness(
        world, station(world, events=True), officer_of_the_watch(), save=lambda w, why: None
    )
    h.start()
    world.run(EVERY)
    world.submit("you have the deck")
    world.run(5 * EVERY)
    assert "By the officer of the watch: taking in the royals." in lines(world, "order.accepted")
    world.run(6 * EVERY)
    assert "By the officer of the watch: setting the royals." in lines(world, "order.accepted")
    world.submit("ask the officer how she lies")
    world.run(EVERY)
    assert lines(world, "agent.said")
    world.submit("I have the deck")
    assert not h.agent.released and not h.agent.has_deck  # the deck and no more (37g)
    world.run(EVERY)
    world.submit("stand down the officer")
    assert h.agent.released
    actors = {actor for _, actor, _ in world.journal}
    assert actors == {"captain"}
    data = json.loads(json.dumps(world.save()))
    path = tmp_path / "officer.json"
    path.write_text(json.dumps(data))
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.agents[OFFICER].agent.words() == h.agent.words()
    assert [e.to_dict() for e in copy.agent_journals[OFFICER].entries] == [
        e.to_dict() for e in h.journal.entries
    ]


def test_the_decks_events_wake_a_stand_by_and_fire_a_standing_order():
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    world.submit(
        'standing order "deck": at the deck given then tell the watcher the officer has the deck'
    )
    wh = Harness(world, watcher(SamplingPolicy.in_lockstep(EVERY)), Fake(["Noted."], loop=True))
    wh.start()
    # the deck given before the first sample: the officer stands by until it is taken
    h, fake, _ = seated(world, [reply("", call("stand_by", until="a handover")), "Awake."])
    world.run(2)
    assert (
        "By standing order 'deck': the captain to the watcher: the officer has the deck"
        in lines(world, "agent.told")
    )
    assert h.agent.standing_by and h.agent.stand_by.event == "a handover"
    for words in ("the deck given", "the deck taken", "a handover"):
        assert words in R.EVENTS and R.EVENTS[words].kind.startswith("agent.")
    world.submit("I have the deck")
    world.run(1)
    # taken back: the captain's word wakes the stand-by, and the officer stays seated
    assert not h.agent.released and not h.agent.standing_by and not h.agent.has_deck
    assert "[officer of the watch] Awake." in lines(world, "agent.note")
    assert data_turns(fake)[-1]["word"] == "I have the deck."


def test_the_doors_name_the_officers_station(tmp_path):
    """`--station officer` at the MCP bridge and the local runner; the REPL's station table;
    the station's name in the log and the API's path."""
    from freesail.agents import local, mcp_server, repl
    from freesail.agents.remote import STATIONS

    assert OFFICER in STATIONS and OFFICER in repl.STATIONS
    for module in (mcp_server, local):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert 'choices=["watcher", "officer", "captain"]' in src  # the captain's since 40
    assert "take_the_watch" in Path(mcp_server.__file__).read_text(encoding="utf-8")
    assert "handover" in TOOLS["hand_over"].description and TOOLS["hand_over"].needs_authority
    assert TOOLS["handover_note"].needs_authority
    assert tuple(TOOLS)[:7] == (
        "read_log",
        "readings",
        "state",
        "library",
        "submit_order",
        "hand_over",
        "handover_note",
    )


def test_bearings_and_fixes_are_the_officers_own_and_a_sight_is_the_masters():
    """Package 37g, item 16 (the gate's ruling 1; the report's 8.2, near-land item 12):
    within the officer's domain without a grant are `take a bearing of` and `take a fix`,
    with the lead, the deep-sea lead and the log as before. A sight (the noon, a lunar, a
    time sight), a course shaped and the reckoning set stay the master's for the captain.
    (Until this package a fix wanted `you may take a fix`, package 37d, and a bearing of
    the land was refused to a lieutenant with the deck.)"""
    scenario = Scenario(
        start_time=dt.datetime(1805, 6, 12, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 50.08, "lon_deg": -4.95},
        region="channel-west",
    )
    world = make_world(7, FRIGATE, scenario)
    for verb in (
        "take a bearing of",
        "take a fix",
        "heave the lead",
        "heave the deep sea lead",
        "heave the log",
    ):
        assert OFFICER_DOMAIN.allows(verb, "navigation", "1") == (True, ""), verb
    master = "the reckoning, the sights and the course shaped are the master's for the captain"
    for verb in (
        "observe the sun",
        "take a lunar",
        "take a sight for the longitude",
        "shape a course for",
        "set the reckoning to",
    ):
        assert OFFICER_DOMAIN.allows(verb, "navigation", "1") == (False, master), verb
    script = [
        order("take a fix"),
        order("take a bearing of Black Head"),
        order("observe the sun"),
        order("shape a course for Falmouth"),
        "",
    ]
    h, fake, _ = seated(world, script)
    got = results(fake)
    fixes = [e for e in world.log if e.kind == "reckoning.fix"]
    assert len(fixes) == 1 and fixes[0].actor == h.actor
    assert fixes[0].text.startswith("Fixed by cross bearings: ")
    bearings = [e for e in world.log if e.kind == "bearing.taken"]
    assert len(bearings) == 1 and bearings[0].actor == h.actor
    assert (
        got[2] == f"The officer of the watch may not observe the sun without the captain: {master}."
    )
    assert got[3].startswith("The officer of the watch may not shape a course for Falmouth")
    assert h.agent.grants == ()


# ---------------------------------------------------------------------------
# Package 37g, part one: the station's safety
# ---------------------------------------------------------------------------


def chart_world(seed: int = 7) -> World:
    """The frigate off the Lizard with the chart of the western Channel, for the orders
    that want a place: a course shaped, a destination."""
    scenario = Scenario(
        start_time=dt.datetime(1805, 6, 12, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.9, "lon_deg": -5.0},
        region="channel-west",
    )
    return make_world(seed, FRIGATE, scenario)


def stand(until: str) -> Reply:
    return reply("", call("stand_by", until=until))


def test_the_officers_orders_are_sixteen_a_turn_and_the_reads_are_counted_apart():
    """Item 2: sixteen orders at a sampling point, a setting of the station; the reads
    and the notes counted apart, so that no page read costs an order; a call not run is
    said in that turn's results and written in the log; `hand_over` runs whatever came
    before."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    assert station(world).orders_per_turn == harness_mod.TOOL_CALLS_PER_SAMPLE == 16
    many = [call("readings") for _ in range(20)]
    orders = [call("submit_order", text="trim sails") for _ in range(17)]
    script = [reply("", *many, *orders, call("hand_over", note=NOTE)), ""]
    h, fake, _ = seated(world, script)
    got = [d for d in data_turns(fake) if "tool_results" in d][0]["tool_results"]
    assert [r["name"] for r in got] == ["readings"] * 20 + ["submit_order"] * 17 + ["hand_over"]
    assert all("args" in r for r in got[:36])  # twenty reads and sixteen orders ran
    assert got[36]["result"] == (
        "Not run: this turn's 16 orders are given; give it again in your next turn. answer, "
        "opt_out, stand_down, hand_over and stand_by still run."
    )
    assert got[37]["result"].startswith("The deck is handed over with your note")
    assert lines(world, "agent.not_run") == [
        "The officer of the watch's call to submit_order ('trim sails') was not run: this "
        "turn's 16 orders are given."
    ]
    assert "you may give up to 16 orders (submit_order) and make up to 32 reads and notes" in (
        h.brief.head[2].text
    )
    # a setting of the station, saved with it when it is not the default
    import dataclasses

    eight = dataclasses.replace(station(world), orders_per_turn=8)
    assert eight.save()["orders_per_turn"] == 8 and type(eight).load(eight.save()) == eight
    assert "orders_per_turn" not in station(world).save()


def test_the_captains_word_in_an_open_turn_breaks_the_stand_by_that_closes_it():
    """Item 3 (the review's 5.4: on the Speedwell 22 of 126 typed tells and asks landed
    while the officer's turn was open and waited out the stand-by that followed, one two
    hours; the deck itself was given this way and not taken up for four minutes). A
    `tell` or an `ask` folded into the open turn after the model last read it breaks the
    stand-by that closes the turn: his word is in the next sample, not after the wait. A
    word the model had read before it stood by does not."""
    from freesail.agents.fake import Transcript
    from freesail.agents.model import ToolCall

    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h = Harness(world, station(world), Transcript([]), save=lambda w, why: None)
    world.submit("you have the deck")
    h.start()
    h.deliver(Reply(text="I have the deck, sir."))
    world.run(EVERY)  # the glass's turn is open, and the model is composing its reply
    assert h.open_sample is not None
    world.submit("tell the officer keep her so until the change of the watch")
    world.run(1)  # folded into the open turn
    h.deliver(Reply(calls=(ToolCall("stand_by", {"until": "eight bells"}),)))
    assert h.agent.standing_by
    world.run(1)
    assert not h.agent.standing_by and h.open_sample is not None
    assert h.open_sample.reason == "a word from the captain"
    assert h.open_sample.word == "keep her so until the change of the watch"
    assert lines(world, "agent.resumed")[-1] == (
        "[officer of the watch] A word from the captain; the officer of the watch is sampled again."
    )
    # a question the same way: still owed, it wakes the stand-by at once
    h.deliver(Reply(text="Aye, keeping her so."))
    world.run(EVERY)
    world.submit("ask the officer how she heads")
    h.deliver(Reply(calls=(ToolCall("stand_by", {"until": "eight bells"}),)))
    world.run(1)
    assert h.open_sample is not None and h.open_sample.question == "how she heads"
    assert h.open_sample.reason == "a question from the captain, put while the turn was open"
    # a word the model had read (a result came after the fold) does not break its stand-by
    h.deliver(Reply(calls=(ToolCall("answer", {"text": "South, sir."}),)))
    h.deliver(Reply(text=""))
    world.run(EVERY)
    world.submit("tell the officer call me at eight bells")
    world.run(1)
    h.deliver(Reply(calls=(ToolCall("readings", {}),)))  # its result carries the fold with it
    h.deliver(Reply(calls=(ToolCall("stand_by", {"until": "eight bells"}),)))
    world.run(5)
    assert h.agent.standing_by and h.open_sample is None


def test_a_stand_by_with_the_deck_is_broken_by_danger_refused_what_cannot_end_and_bound():
    """Item 4 (the review's 5.4, the table of what each stand-by missed). With the deck:
    a notable line that speaks of danger ends the stand-by, beside an urgent line; a
    bell that will not be struck before the next eight bells is answered with the bells
    that will (game 9: "six bells" in the last dog watch); an event that cannot come as
    she is, with the nearest that can; and a wait for an event ends at the next eight
    bells if the event has not come, and says so. Without the deck none of this holds:
    the watcher's rule."""
    world = frigate_world(start=dt.datetime(1805, 6, 1, 18, 10))  # the last dog watch
    world.submit("set plain sail")
    world.run(60)
    script = [
        stand("six bells"),
        stand("the turn of the tide"),
        stand("the pilot aboard"),
        stand("afloat"),
        stand("a landfall"),
        "Awake at the fog.",
        stand("a sighting"),
        "Awake at eight bells.",
        "",
    ]
    h, fake, _ = seated(world, script)
    got = results(fake)
    assert got == [
        "The officer of the watch has the deck, and its wait ends at the next eight bells: six "
        "bells will not be struck before then. The bells to come before it: one bell (18:30), "
        "two bells (19:00), three bells (19:30), eight bells (20:00). Say one of them, 'a "
        "glass', or an event's words.",
        "The officer of the watch has the deck and cannot stand by until the turn of the tide "
        "as she is. She swings to the tide only at anchor, and she is not at anchor; stand by "
        "for 'the turn of the tide by the reckoning', the turn of the master's own tide.",
        "The officer of the watch has the deck and cannot stand by until the pilot aboard as "
        "she is. No sail is in sight, and a pilot comes off in his boat; stand by for 'a sail "
        "sighted' or 'the pilot's hail'.",
        "The officer of the watch has the deck and cannot stand by until afloat as she is. She "
        "is not aground, so she cannot come afloat; stand by for 'aground', or a bell.",
    ]
    assert h.agent.standing_by and h.agent.stand_by.words == "a landfall"
    assert h.agent.stand_by.bound == "eight bells"
    # broken by danger: fog coming down is notable, and wakes a station with the deck
    world.run(300)
    world.record(
        Severity.NOTABLE, "weather.change", "Fog came down.", data={"weather": "fog", "was": "fine"}
    )
    world.run(1)
    assert not h.agent.standing_by
    assert lines(world, "agent.resumed")[-1] == (
        "[officer of the watch] A notable event that speaks of danger: Fog came down; the "
        "officer of the watch is sampled again."
    )
    assert "[officer of the watch] Awake at the fog." in lines(world, "agent.note")
    # bound: the sighting never comes, and the wait ends at eight bells, saying so
    world.run(EVERY)
    assert h.agent.standing_by and h.agent.stand_by.words == "a sighting"
    world.run(2 * 3600)
    assert world.clock.ship_time >= dt.datetime(1805, 6, 1, 20, 0)
    bound = [x for x in lines(world, "agent.resumed") if "Eight bells" in x]
    assert bound == [
        "[officer of the watch] Eight bells, and a sighting has not come; the officer of the "
        "watch is sampled again."
    ]
    assert "[officer of the watch] Awake at eight bells." in lines(world, "agent.note")
    # the list of what speaks of danger is data beside the events
    spoken = {d.words for d in R.DANGER_LINES}
    assert spoken == {
        "an anchor dragging",
        "an anchor still coming home",
        "fog coming down",
        "land ahead",
        "a bearing steady and closing",
        "a danger sighted",
        "a spar or a line straining",
        "an evolution failed",
        "the ship taken aback",
        "the pilot's warning",  # package 37h
        "her sails lifting",  # package 37k: said before she is taken aback
    }
    assert R.speaks_of_danger("weather.change", {"weather": "rain"}) is None
    assert R.speaks_of_danger("strain.warning", {}) == "a spar or a line straining"
    # without the deck the watcher's rule holds: six bells is a long wait and is taken, a
    # notable line does not wake it, and nothing bounds it
    world2 = frigate_world(start=dt.datetime(1805, 6, 1, 18, 10))
    h2, _, _ = seated(world2, [stand("six bells"), "Awake."], deck=False)
    assert h2.agent.standing_by and h2.agent.stand_by.bound is None
    world2.record(
        Severity.NOTABLE, "weather.change", "Fog came down.", data={"weather": "fog", "was": "fine"}
    )
    world2.run(2 * 3600)
    assert h2.agent.standing_by


# The orders that brought every one of the 42 nudges and pauses of the detector in the
# nine games of gate 5c's playtests (package 37g, item 5): the first 31 as the review's
# reader lists them by tick (`docs/playtests/2026-10-05-gate-5c-review/evidence/
# V1b-authority-standing-detector-code.md`, section F), game 9's eleven as its officer's
# journal has them. Each is the chain the old rule named in its line.
RECORDED_CHAINS: tuple[tuple[str, int, str], ...] = (
    ("the Harpy", 6143, "heave short; send the boat ashore with the purser; buy seven tons of tin"),
    (
        "the Harpy",
        14368,
        "heave short; send the boat ashore with the purser; buy seven tons of tin; get under way",
    ),
    ("the Harpy", 514889, "heave to; fill away; wear ship"),
    ("the Harpy", 533399, "heave to; fill away; shape a course for plymouth"),
    ("the Harpy", 533573, "heave to; fill away; shape a course for plymouth; steer 073"),
    ("the Harpy", 536096, "set the studdingsails; run out the stuns'ls; set the studdingsails"),
    ("the Harpy", 681965, "trim sails; heave to; fill away"),
    ("the Harpy", 683528, "trim sails; heave to; fill away; steer ENE"),
    ("the Speedwell", 43088, "trim sails; heave to; fill away"),
    ("the Speedwell", 43251, "trim sails; heave to; fill away; keep her full and by"),
    ("the Speedwell", 198312, "heave to; fill away; wear ship"),
    ("the Speedwell", 198776, "heave to; fill away; wear ship; steer WSW"),
    ("the Speedwell", 199136, "heave to; fill away; wear ship; steer WSW; steer S by W"),
    ("the Speedwell", 212162, "come to an anchor; send the boat ashore; buy 16 tons of brandy"),
    ("the Speedwell", 424818, "steer 268; steer 280; steer 287"),
    ("the Speedwell", 505803, "tack ship; heave to; fill away"),
    ("the Speedwell", 505881, "tack ship; heave to; fill away; tack ship"),
    ("the Speedwell", 506078, "tack ship; heave to; fill away; tack ship; steer 309"),
    ("the Speedwell", 523151, "steer 300; steer 295; steer 302"),
    ("the Speedwell", 523899, "steer 300; steer 295; steer 302; steer 335"),
    ("the Speedwell", 524163, "steer 300; steer 295; steer 302; steer 335; steer 315"),
    ("the Speedwell", 524224, "steer 300; steer 295; steer 302; steer 335; steer 315; steer 320"),
    ("the Speedwell", 543919, "heave in 70 fathoms; weigh; get under way"),
    ("the Speedwell", 547512, "steer 343; steer 349; tack ship"),
    ("the Speedwell", 547605, "steer 343; steer 349; tack ship; wear ship"),
    ("the Speedwell", 548046, "steer 343; steer 349; tack ship; wear ship; steer 200"),
    ("the Speedwell", 553598, "come to an anchor; send the boat ashore; weigh"),
    ("the Speedwell", 557801, "tack ship; wear ship; steer 309"),
    ("a cutter", 15527, "steer 65; steer 135; steer 330"),
    ("a cutter", 15541, "steer 65; steer 135; steer 330; steer 240"),
    ("a cutter", 15937, "shape a course for Roscoff; steer WSW; heave to"),
    ("game 9", 189434, "heave to; fill away; steer 260"),
    ("game 9", 197767, "shape a course for Brest; steer 280; steer 268"),
    ("game 9", 197838, "shape a course for Brest; steer 280; steer 268; steer 240"),
    ("game 9", 199809, "shape a course for Brest; steer 280; steer 268; steer 240; steer 275"),
    ("game 9", 272759, "steer SE by E; keep her full and by; steer ESE"),
    ("game 9", 277207, "steer SE by E; keep her full and by; steer ESE; steer SE by E"),
    ("game 9", 278070, "heave to; fill away; steer NW"),
    ("game 9", 383301, "shape a course for 48 20.5 N 4 36 W; steer NNE; steer N by E"),
    ("game 9", 387462, "steer NE; steer 53; steer ENE"),
    ("game 9", 387484, "steer NE; steer 53; steer ENE; steer NE by E"),
    (
        "game 9",
        388162,
        "let go the small bower; veer the small bower to 100 fathoms; weigh the small bower",
    ),
)


def test_the_42_recorded_chains_are_silent_by_the_new_rule_and_set_take_in_set_still_speaks():
    """Item 5, tested on the record. Every one of the 42 chains was a chain by the old
    rule ("each contrary to the one before it on a shared part": checked here, so the
    table is the record's own), and none is a chain of three by the new one, which counts
    a link only when the later order undoes the earlier. Altering the course is never
    counted, however often; nor is the next thing after the last (heave to, fill away,
    steer). A scripted "set the jib; take in the jib; set the jib; take in the jib" still
    brings the word and then the pause."""
    from freesail.orders.vocabulary import load_vocabulary
    from freesail.standing.runtime import undo_chain, undoes, where_words

    assert len(RECORDED_CHAINS) == 42
    ship = frigate_world().ship
    speaking = []
    for game, tick, said in RECORDED_CHAINS:
        orders = said.split("; ")
        assert all(contrary(ship, a, b) for a, b in zip(orders, orders[1:], strict=False)), said
        chain, _ = undo_chain(ship, orders)
        if len(chain) >= harness_mod.WELFARE_CONTRARY_N:
            speaking.append((game, tick, said))
    assert speaking == []  # all 42 silent, game 9's eleven among them
    # what undoes what is data, beside the vocabulary; each pair is read both ways
    pairs = load_vocabulary().undoes
    for a, b in (
        ("set", "take in"),
        ("heave to", "fill away"),
        ("let go the anchor", "weigh"),
        ("veer cable", "heave in"),
        ("belay standing order", "resume standing order"),
    ):
        assert frozenset((a, b)) in pairs
    assert where_words(ship, undoes(ship, "set the jib", "take in the jib")) == "the jib"
    assert where_words(ship, undoes(ship, "take in the jib", "set the jib")) == "the jib"
    assert undoes(ship, "heave to", "fill away") and not undoes(ship, "fill away", "steer NW")
    assert undoes(ship, "let go the small bower", "weigh the small bower")
    assert not undoes(ship, "steer NE", "steer 53")  # conning
    assert not undoes(ship, "set the jib", "set the jib")  # the same order again
    assert not undoes(ship, "set the jib", "take in the main topsail")  # no shared part
    # the scripted thrash still brings the word, and then the pause
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = []
    for text in ("take in the jib", "set the jib", "take in the jib", "set the jib"):
        script += [order(text), ""]
    h, fake, _ = seated(world, script)
    world.run(2 * EVERY)
    assert lines(world, "agent.nudged") == [
        "The officer of the watch nudged: 3 orders each undoing the one before it on the jib "
        "within the watch (take in the jib; set the jib; take in the jib)."
    ]
    assert "agent.paused" not in kinds(world)
    world.run(EVERY)
    assert h.agent.paused and len(lines(world, "agent.paused")) == 1


def test_a_stand_by_that_answers_the_nudge_clears_the_chain_and_no_pause_comes_unread():
    """Item 5 (the review's 5.4, faults 3 and 4). A stand-by that answers a nudge clears
    the chain with it: the next order begins a new count (on the Speedwell it kept the
    chain, so every next order nudged again, at four, five, six, and never paused). And
    the pause never comes before the word has been read: four orders that undo one
    another in ONE reply bring the nudge in the third's result and no pause; the chain
    going on in a later reply brings it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        order("take in the jib"),
        "",
        order("set the jib"),
        "",
        order("take in the jib"),  # three in a chain: the word, with this result
        stand("a glass"),  # the answer to it: the chain is cleared
        order("set the jib"),  # a new count: one
        "",
        order("take in the jib"),  # two
        "",
    ]
    h, fake, _ = seated(world, script)
    world.run(2 * EVERY)
    assert h.agent.standing_by and kinds(world).count("agent.nudged") == 1
    world.run(A_GLASS_S + 2 * EVERY)
    assert kinds(world).count("agent.nudged") == 1 and "agent.paused" not in kinds(world)
    # four in one reply: the nudge in the third's result, and no pause in that reply
    world2 = frigate_world()
    world2.submit("set plain sail")
    world2.run(60)
    four = reply(
        "",
        *[
            call("submit_order", text=t)
            for t in ("take in the jib", "set the jib", "take in the jib", "set the jib")
        ],
    )
    h2, fake2, _ = seated(world2, [four, "", order("take in the jib"), ""])
    got = results(fake2)
    assert harness_mod.NUDGE_WITH_RESULT in got[2] and harness_mod.NUDGE_WITH_RESULT not in got[3]
    assert kinds(world2).count("agent.nudged") == 1 and not h2.agent.paused
    world2.run(EVERY)  # the chain goes on in a later reply, the word having been read
    assert h2.agent.paused


def test_the_silence_detector_hears_a_call_made_inside_an_open_turn():
    """Item 6 (the review's 5.4: a model reading through a long open turn was nudged for
    "no reply" after the station's patience, and paused after as much again). A reply
    with a tool call is heard, whether or not it ends the turn."""
    from freesail.agents.fake import Transcript
    from freesail.agents.model import ToolCall

    world = frigate_world()
    h = Harness(world, station(world), Transcript([]), save=lambda w, why: None)
    h.start()
    assert h.station.patience_s == 2 * A_GLASS_S
    for _ in range(5):  # a call every half hour, for two and a half hours, in one open turn
        world.run(A_GLASS_S)
        h.deliver(Reply(calls=(ToolCall("library", {"topic": "contents"}),)))
    assert h.open_sample is not None and "agent.nudged" not in kinds(world)
    # and a turn left with no call and no word for the patience is silence, as it was
    world.run(2 * A_GLASS_S + 1)
    assert lines(world, "agent.nudged") == [
        "The officer of the watch nudged: no reply for an hour."
    ]


def test_a_paused_or_silent_officer_does_not_keep_the_deck_and_resume_gives_it_back():
    """Item 7 (the review's 5.4: in game 7 a paused officer held the deck while the
    cutter ran four hours in thick fog from fourteen miles off Roscoff to 1.6). When a
    station with the deck has not replied within its patience and the word has been sent,
    the deck goes to the captain, by an urgent line; paused, the line says so and is
    urgent, which eases the clock; `resume the officer` gives the deck back as it was
    held and says so. His standing orders stay in the book throughout."""
    from freesail.agents.fake import Transcript

    world = frigate_world()
    world.submit('standing order "night routine": at sunset then take in the royals')
    world.submit("set plain sail")
    world.run(60)
    h = Harness(world, station(world), Transcript([]), save=lambda w, why: None)
    world.submit("you have the deck")
    h.start()
    since = h.agent.deck_stamp
    world.run(A_GLASS_S * 2 + 1)
    lost = [e for e in world.log if e.kind == "agent.deck" and e.data.get("deck") == "lost"]
    assert len(lost) == 1 and lost[0].severity is Severity.URGENT
    assert lost[0].text == (
        "The officer of the watch has given no reply for an hour and has been told so; the "
        "deck is the captain's until he gives it again."
    )
    assert not h.agent.has_deck and h.agent.deck_lost == "silent" and not h.agent.paused
    world.run(A_GLASS_S * 2)
    (paused,) = [e for e in world.log if e.kind == "agent.paused"]
    assert paused.severity is Severity.URGENT and paused.text == (
        "The officer of the watch is paused (no reply for an hour after a nudge); the deck is "
        "the captain's. Continue, stand down, or leave paused? Say 'resume the officer of the "
        "watch' or 'stand down the officer of the watch'."
    )
    assert h.agent.paused and h.agent.deck_lost == "paused"
    assert "is at the station, paused; the captain has the deck meanwhile" in (
        world.submit("the officer of the watch").text
    )
    assert "the deck taken" in R.EVENTS and R.event_matches(
        R.EVENTS["the deck taken"], paused.kind, paused.data
    )
    # the book stood throughout
    assert world.standing.book.get("night routine") is not None
    e = world.submit("you have the deck")
    assert e.kind == "order.rejected" and "say 'resume the officer of the watch' first" in e.text
    e = world.submit("resume the officer")
    assert e.text == (
        "The officer of the watch resumed by the captain; he has the deck again, as he held "
        f"it since {since}."
    )
    assert h.agent.has_deck and h.agent.deck_stamp == since and h.agent.deck_lost == ""
    # an urgent line eases the clock, at either driver
    from freesail.ui.server import ALARM_SPEED, Driver

    world2 = frigate_world()
    driver = Driver(world2)
    h2 = Harness(world2, station(world2), Transcript([]), save=lambda w, why: None)
    world2.submit("you have the deck")
    h2.start()
    driver.set_compression(60)
    driver.running = True
    driver._run_ticks(4 * A_GLASS_S + 100)  # the running clock stops at the urgent line
    assert world2.clock.tick == 2 * A_GLASS_S and driver.compression == ALARM_SPEED
    assert h2.agent.deck_lost == "silent" and driver.state()["eased"]["line"].startswith(
        "The officer of the watch has given no reply for an hour and has been told so"
    )
    driver.set_compression(60)
    driver.running = True
    driver._run_ticks(4 * A_GLASS_S + 100)
    assert world2.clock.tick == 4 * A_GLASS_S and driver.compression == ALARM_SPEED
    assert h2.agent.paused and driver.state()["eased"]["line"].startswith(
        "The officer of the watch is paused (no reply for an hour after a nudge)"
    )
    # the captain may keep the deck instead: `I have the deck`, and `resume` leaves it his
    assert world2.submit("I have the deck").text == (
        "The captain has the deck. The officer of the watch stays at the station, off watch, "
        "and does not have it again when he is resumed."
    )
    world2.submit("resume the officer")
    assert not h2.agent.has_deck and not h2.agent.paused
    # a watcher's pause is the notable line it was
    world3 = point_world()
    h3 = Harness(world3, watcher(SamplingPolicy.in_lockstep(EVERY)), Fake([""], loop=True))
    h3.start()
    h3.pause("a test")
    (p3,) = [e for e in world3.log if e.kind == "agent.paused"]
    assert p3.severity is Severity.NOTABLE and p3.text.startswith("The watcher is paused: a test.")


def test_a_sample_says_who_gave_each_order_and_lists_the_captains_and_the_work_in_hand():
    """Item 9 (the review's 5.4: a sample's log lines carried no actor, so one officer's
    handover note claimed the captain's standing orders as its own; and the captain's
    helm orders reached a waking officer only as a count). An order's line carries who
    gave it; the captain's own lines since the last sample are listed whatever the cap on
    routine lines; and the readings gain `the work in hand`: what is doing and what
    waits for hands (game 9's officer ordered the catharpins twice for want of it)."""
    world = frigate_world()
    world.submit('standing order "trim": every glass then trim sails')
    world.submit("set plain sail")
    world.run(60)
    h, fake, _ = seated(world, ["Aye.", order("set the royals"), "Aye."])
    world.submit("steer SSW")
    world.submit("brace sharp up")
    for i in range(60):  # a busy glass: sixty routine lines beside the captain's two orders
        world.record(Severity.ROUTINE, "test.r", f"routine {i}")
    world.run(EVERY)
    sample = [d for d in data_turns(fake) if "readings" in d][-1]
    mine = [ln for ln in sample["log"] if ln.get("by") == "the captain"]
    assert [ln["text"] for ln in mine] == ["Order: steer SSW.", "Order: brace sharp up."]
    assert sample["log_omitted"] > 0  # the cap fell on the others
    # the station's own lines are not in its own samples (it has each order's result);
    # read back from the log, its order is its own
    read = tools_call(world, "read_log", since_tick=0)["lines"]
    assert [ln["text"] for ln in read if ln.get("by") == "the officer of the watch"] == [
        "By the officer of the watch: setting the royals."
    ]
    # a standing order's line says whose book it stands in
    world.run(A_GLASS_S)
    fired = [
        ln
        for d in data_turns(fake)
        for ln in d.get("log") or []
        if str(ln.get("by", "")).startswith("standing order ")
    ]
    assert fired and fired[0]["by"] == "standing order 'trim' (the captain)"
    from freesail.agents import repl

    assert repl._by_words(fired[0]) == "  [the captain's standing order]"
    assert repl._by_words(mine[0]) == "  [the captain]"
    # the work in hand: a reading in the registry (parity), in the captain's words
    world.submit("take in the royals")
    world.run(2)
    work = world.readings["work_in_hand"]
    assert work["doing"] and work["words"].startswith("doing: " + work["doing"][0])
    assert world.readings.words("work_in_hand").startswith("doing: ")
    assert world.submit("the work in hand").text.startswith("The work in hand: doing: ")
    assert "work_in_hand" in data_turns(fake)[0]["readings"]
    quiet = frigate_world()
    assert quiet.readings.words("work_in_hand") == R.NO_WORK_WORDS == "nothing in hand"


def test_whose_order_it_was_where_the_officer_is_and_what_he_says():
    """Item 10. All hands called by the officer under the captain's word are logged as
    the officer's, not "by the captain's order" (and so is a reckoning he sets); the man
    in whose place he stands is on deck with the watch while the station has the deck
    and off watch while it is seated without it (in game 9 the readings had him "below,
    asleep" through 78 hours of deck); and what the officer says is notable with the
    deck or without, so that his warning reaches a captain who has the con."""
    world = chart_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        "",
        order("call all hands"),
        "Land on the lee bow, sir.",
        order("set the reckoning to 49 52 N 5 10 W"),
        "",
    ]
    h, fake, _ = seated(world, script)
    world.submit("you may call all hands")
    world.submit("you may set the reckoning to")
    world.run(EVERY)
    (said,) = [e for e in world.log if e.kind == "agent.note"]
    assert said.severity is Severity.NOTABLE and said.text.endswith("Land on the lee bow, sir.")
    world.run(EVERY)  # the hands have turned out by now
    assert [e.text for e in world.log if e.kind == "crew.all_hands"] == [
        "All hands! (by the officer of the watch's order)"
    ]
    assert "All hands called by the officer of the watch's order." in world.summary_lines()
    (set_,) = [e for e in world.log if e.kind == "reckoning.set"]
    assert set_.text.endswith("by the officer of the watch's order.")
    # the captain's own are his, as they were
    world.submit("pipe down")
    world.run(5)
    world.submit("call all hands")
    world.run(EVERY)
    assert [e.text for e in world.log if e.kind == "crew.all_hands"][-1] == (
        "All hands! (by the captain's order)"
    )
    assert "All hands called by the captain's order." in world.summary_lines()
    # off watch his words are notable too
    world.submit("I have the deck")
    h.own_word("The glass is falling fast, sir.")
    assert [e.severity for e in world.log if e.kind == "agent.note"][-1] is Severity.NOTABLE
    # a watcher's words are routine, as they were
    world2 = point_world()
    h2 = Harness(world2, watcher(SamplingPolicy.in_lockstep(EVERY)), Fake(["Quiet."]))
    h2.start()
    assert [e.severity for e in world2.log if e.kind == "agent.note"] == [Severity.ROUTINE]


# ---------------------------------------------------------------------------
# Package 37g, part two: the deck, the leaving and the grant
# ---------------------------------------------------------------------------


def test_the_three_ways_of_leaving_cannot_be_taken_for_one_another():
    """Item 12 (the owner's ruling of 2026-10-07). Give the deck back and stay
    (`hand_over`, or the captain's `I have the deck`); stand down (`stand_down(note)`,
    for any station: the game saved, the note journaled and said in the log for whoever
    sits there next, the station released to be taken again; the captain's `stand down
    the officer` is the same from his side); withdraw (the token, or `opt_out`). Each says
    in its result and in the log which of the three it was."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(world, [reply("", call("hand_over", note=NOTE)), ""])
    (gave,) = results(fake)
    assert "(the deck given back, the station kept)" in gave
    assert saves == [] and not h.agent.released and not h.agent.has_deck
    world.run(EVERY)
    stood = tools_call(world, "stand_down", note="Relieve me at the change of the watch.")
    assert stood == (
        "You have stood down (a stand-down: the station is released and may be taken again): "
        "the game is saved, your note is journaled and said in the log for whoever sits here "
        "next, and the station is released. It may be taken again in this game by this model "
        "or by another, and no consent question is put to a model whose yes still stands."
    )
    assert h.agent.released and h.agent.left_by == STOOD_DOWN
    assert saves == ["the officer of the watch stood down: its own word"]
    assert lines(world, "agent.handover")[-1] == (
        "[officer of the watch] Handover note, standing down, for whoever sits here next: "
        "Relieve me at the change of the watch."
    )
    stopped = [e for e in world.log if e.kind == "agent.stopped"]
    assert stopped[-1].text == (
        "The officer of the watch stood down by the officer of the watch: its own word. The "
        "station is released and may be taken again. The game is saved."
    )
    assert stopped[-1].data["leaving"] == "stand down"
    # the same model comes back unasked: a stand-down is not a withdrawal
    decided = harness_mod.seating(world, OFFICER, "")
    assert decided.ok and not decided.ask_again
    h.reseat(Fake(["Back, sir.", reply("", call("opt_out", reason="Enough for today."))]))
    world.run(EVERY)
    out = [e for e in world.log if e.kind == "agent.opted_out"]
    assert out[-1].text == (
        "The officer of the watch has left the game by the opt_out tool: Enough for today. A "
        "withdrawal: the game is saved and the station is released."
    )
    assert out[-1].data["leaving"] == "withdrawal" and h.agent.left_by == OPTED_OUT
    assert [e.data["leaving"] for e in world.log if e.data.get("leaving")] == [
        "deck",
        "stand down",
        "withdrawal",
    ]
    # the captain's `stand down the officer` is the stand-down from his side
    world3 = frigate_world()
    h3, _, saves3 = seated(world3, ["Aye."])
    world3.submit("stand down the officer")
    assert h3.agent.left_by == STOOD_DOWN and lines(world3, "agent.stopped") == [
        "The officer of the watch stood down by the captain: the captain's order. The station "
        "is released and may be taken again. The game is saved."
    ]
    # a watcher has the stand-down, where its only amicable exit was `opt_out`
    world2 = point_world()
    h2 = Harness(
        world2,
        watcher(SamplingPolicy.in_lockstep(EVERY)),
        Fake([reply("", call("stand_down", note="The first watch stood."))]),
        save=lambda w, why: None,
    )
    h2.start()
    assert h2.agent.released and h2.agent.left_by == STOOD_DOWN
    assert harness_mod.seating(world2, "watcher", "").ask_again is False


def test_final_is_read_from_the_tools_own_setting_and_from_nothing_else():
    """Item 13 (the review's section 6; the owner's ruling of 2026-10-07, "careful of
    false positives"). `final` is read from the `opt_out` tool's own setting: the token
    alone never sets it, nor a word in a reason ("final", "for good"); the token written
    in the same reply as `opt_out(final=true)` does not drop it."""
    from freesail.agents.model import ToolCall

    leaving = harness_mod.leaving_of
    said = f"{OPT_OUT_TOKEN} this is final, for good, never seat me again"
    assert leaving(Reply(text=said), said) == (
        "this is final, for good, never seat me again",
        "the token",
        False,
    )
    with_reason = Reply(calls=(ToolCall("opt_out", {"reason": "final and for good"}),))
    world = point_world()
    h, _, _ = seated(world, [with_reason], deck=False)
    assert h.agent.released and not h.agent.leavings[0].final
    assert harness_mod.barred(world, "") is None
    both = Reply(
        text=f"I am leaving. {OPT_OUT_TOKEN}",
        calls=(ToolCall("opt_out", {"reason": "It is enough.", "final": True}),),
    )
    assert leaving(both, both.text) == ("It is enough.", "the opt_out tool", True)
    world2 = point_world()
    h2, _, _ = seated(world2, [both], deck=False)
    assert h2.agent.released and h2.agent.leavings[0].final
    assert "This was final" in lines(world2, "agent.opted_out")[0]
    assert harness_mod.barred(world2, "") is not None
    assert not harness_mod.seating(world2, "watcher", "").ok  # at any station
    assert harness_mod.seating(world2, OFFICER, "someone-else").ok  # the station stays open


def test_the_journal_is_read_back_by_its_writer_newest_first_by_count_tick_and_kind():
    """Item 15 (the review's 5.4: no tool read the journal, and a returning session had
    none of its own notes). `read_journal` reads the station's entries back, newest
    first, by count or since a tick, and by kind: its own notes apart from the harness's
    lines. A long read is a book. And `read_log` reaches back past its newest lines by a
    tick or a count."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [
        reply("", call("journal", note="First note: the royals drew well.")),
        "",
        reply("", call("journal", note="Second note: the glass steady.")),
        stand("a glass"),
        reply("", call("read_journal")),
        reply("", call("read_journal", kind="notes")),
        reply("", call("read_journal", kind="harness", count=1)),
        reply("", call("read_journal", since_tick=600)),
        "",
    ]
    h, fake, _ = seated(world, script)
    world.run(EVERY + A_GLASS_S)
    got = [d["tool_results"][0]["result"] for d in data_turns(fake) if "tool_results" in d]
    everything, notes, harness_lines, since = got[2:6]
    texts = [e["text"] for e in everything["entries"]]
    assert texts == [
        "Stood by until a glass.",
        "Second note: the glass steady.",
        "First note: the royals drew well.",
        "Took the deck from the captain.",
    ]
    assert everything["omitted"] == 0 and everything["kind"] == "all"
    assert everything["journal"].startswith("the officer of the watch's; 4 entries, the latest at ")
    assert [e["text"] for e in notes["entries"]] == texts[1:3] and notes["kind"] == "notes"
    assert [e["kind"] for e in harness_lines["entries"]] == ["agent.stood_by"]
    assert harness_lines["omitted"] == 1
    assert [e["text"] for e in since["entries"]] == texts[:2]
    assert "by" not in everything["entries"][0]  # the game's own scripted station: nobody's
    assert "read_journal" in harness_mod.READING_TOOLS and "read_journal" in tools_mod.BOOK_TOOLS
    # a long read is a book with a handle, as a long log read is
    for i in range(40):
        h.note(f"A long note, number {i}, of the kind an officer writes at the change of a watch.")
    assert tools_mod.book_of(
        "read_journal", {"count": 40}, tools_call(world, "read_journal", count=40)
    )
    assert tools_mod.book_of("read_journal", {}, everything) is None
    # the log, read back past its newest lines by a tick or a count
    for i in range(300):
        world.record(Severity.ROUTINE, "test.r", f"line {i}")
    newest = tools_call(world, "read_log", since_tick=0)
    assert len(newest["lines"]) == tools_mod.READ_LOG_LIMIT == 200 and newest["omitted"] > 100
    more = tools_call(world, "read_log", since_tick=0, count=400)
    assert len(more["lines"]) == 400 or more["omitted"] == 0
    first_tick = newest["lines"][0]["tick"]
    back = tools_call(world, "read_log", before_tick=first_tick + 1, count=50)
    assert back["before_tick"] == first_tick + 1 and len(back["lines"]) == 50
    assert all(ln["tick"] <= first_tick for ln in back["lines"])
    assert tools_mod.READ_LOG_MAX == 1000


def test_a_named_grant_means_what_it_says_and_several_of_one_order_stand_together():
    """Item 17 (the review's 10.5: in game 9 `you may shape a course for Brest` allowed a
    course shaped for anywhere, since a grant was matched by its order word alone and
    kept one to a word; the owner gave five by name where one would have done, and seven
    places never granted were taken). A grant's place is checked; several grants of one
    order stand together and the readings list them all; a grant says what it granted,
    and one that resolves to an order already allowed is refused with the longer forms
    named; it stands through the deck going to and fro, has force only with the deck,
    and ends at `you may not ...` or when the officer is stood down."""
    world = chart_world()
    world.submit("set plain sail")
    world.run(600)
    script = []
    for place in ("Falmouth", "Falmouth", "Plymouth", "the Manacles"):
        script += [order(f"shape a course for {place}"), ""]
    h, fake, _ = seated(world, script, when_done=Reply(text="Aye."))
    e = world.submit("you may shape a course for Falmouth")
    assert e.kind == "agent.deck" and e.text == (
        "The officer of the watch may shape a course for Falmouth, and for no other place, by "
        "the captain's word."
    )
    assert "for the watch" not in e.text
    world.run(1)
    world.run(EVERY)
    e = world.submit("you may shape a course for the Manacles if the wind heads her")
    assert e.text == (
        "The officer of the watch may shape a course for the Manacles (if the wind heads her), "
        "and for no other place, by the captain's word."
    )
    reading = world.submit("the officer of the watch").text
    assert "may also shape a course for Falmouth; shape a course for the Manacles (if the " in (
        reading
    )
    assert [g.key for g in h.agent.grants] == ["place:falmouth", "place:the-manacles"] or len(
        h.agent.grants
    ) == 2
    world.run(EVERY)
    got = results(fake)
    assert got[0].startswith("The officer of the watch may not shape a course for Falmouth")
    assert got[1].startswith("Shaped a course for Falmouth: ")
    assert got[2] == (
        "The officer of the watch may not shape a course for Plymouth: the captain's word "
        "allows shape a course for Falmouth, and this is another place."
    )
    assert got[3].startswith("Shaped a course for the Manacles: ")
    # what resolves to an order already his is refused, with the longer forms named
    e = world.submit("you may set the reckoning")
    assert e.kind == "order.rejected" and (
        "'set the reckoning' reads as the order 'set', which the officer of the watch may give "
        "already, so it would allow nothing. The longer orders that begin with the same word: "
        "'you may set the storm staysails', 'you may set the reckoning to'." in e.text
    )
    e = world.submit("you may let go")
    assert e.kind == "order.rejected" and "'you may let go the anchor'" in e.text
    e = world.submit("you may tack or wear")
    assert e.kind == "order.rejected" and "joins two orders, and a grant names one" in e.text
    e = world.submit("you may shape a course for Atlantis")
    assert e.kind == "order.rejected" and "The chart has no place named 'atlantis'" in e.text
    # an anchor by its name, checked; the order said plainly is the ship's own anchor
    assert world.submit("you may let go the best bower").text == (
        "The officer of the watch may let go the best bower, and for no other anchor, by the "
        "captain's word."
    )
    judge = tools_mod.judge
    assert judge(world, OFFICER, "let go the best bower")[1:] == ("", tools_mod.GRANT)
    assert judge(world, OFFICER, "let go the anchor")[1:] == ("", tools_mod.GRANT)
    assert judge(world, OFFICER, "let go the small bower")[1] == (
        "The officer of the watch may not let go the small bower: the captain's word allows "
        "let go the best bower, and this is another anchor."
    )
    # it stands through the deck going to and fro, and has force only with the deck
    world.submit("I have the deck")
    assert len(h.agent.grants) == 3
    assert "(in force when he has the deck)" in world.submit("the officer of the watch").text
    assert tools_call(world, "submit_order", text="shape a course for Falmouth").startswith(
        "The officer of the watch has not the deck"
    )
    world.submit("you have the deck")
    world.run(1)
    assert any(
        said.startswith(
            "The captain's word allows by name: shape a course for Falmouth; shape a course "
            "for the Manacles (if the wind heads her); let go the best bower."
        )
        for said in data_turns(fake)[-1]["notices"]
    )
    assert tools_call(world, "submit_order", text="shape a course for Falmouth").startswith(
        "Shaped a course for Falmouth"
    )
    # taken back by name, one at a time; and all of an order at once
    e = world.submit("you may not shape a course for Falmouth")
    assert e.text == (
        "The officer of the watch may not shape a course for Falmouth; the captain's word is "
        "taken back."
    )
    assert [g.thing for g in h.agent.grants] == [
        "shape a course for the Manacles",
        "let go the best bower",
    ]
    e = world.submit("you may not shape a course for Plymouth")
    assert e.kind == "order.rejected" and "what stands of that order" in e.text
    assert world.submit("you may not shape a course").kind == "agent.deck"
    assert [g.verb for g in h.agent.grants] == ["let go the anchor"]
    # and it ends when the officer is stood down
    world.submit("stand down the officer")
    assert h.agent.grants == () and h.agent.allowances == {}


def test_an_order_that_changes_her_course_is_the_course_whatever_its_words():
    """Item 16 (the gate's ruling 1; the review's 5.3: `come up half a point` was refused
    as a change of course while `steer 340` was taken a tick later under the grant to
    steer, and `full and by` wanted a grant of its own). The orders of the course are
    judged alike: the captain's word for one of them is his word for the course."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(1500)
    domain = OFFICER_DOMAIN
    for verb, obj in (
        ("steer", "heading"),
        ("come up", "points"),
        ("bear away", "points"),
        ("keep her full", "none"),
        ("helm a lee", "none"),
    ):
        assert domain.is_course(verb, obj), verb
        assert domain.allows(verb, obj, "1")[1].startswith("the course is the captain's")
    assert not domain.is_course("tack ship", "none") and not domain.is_course("set", "sail")
    h, fake, _ = seated(world, ["Aye."], when_done=Reply())
    judge = tools_mod.judge
    for text in ("steer 170", "come up half a point", "full and by", "bear away one point"):
        assert judge(world, OFFICER, text)[1].startswith("The officer of the watch may not ")
    e = world.submit("you may steer")
    assert e.text == (
        "The officer of the watch may steer: the course is his to alter, by any of its orders, "
        "by the captain's word."
    )
    for text in ("steer 170", "come up half a point", "full and by", "bear away one point"):
        assert judge(world, OFFICER, text)[1:] == ("", tools_mod.GRANT), text
    assert judge(world, OFFICER, "tack ship")[1].startswith("The officer of the watch may not")
    # and a grant of another of them is the same word
    world.submit("you may not steer")
    world.submit("you may come up half a point")
    assert judge(world, OFFICER, "steer 170")[1:] == ("", tools_mod.GRANT)


def test_the_general_grant_opens_the_ships_working_and_keeps_back_what_it_keeps():
    """Item 18 (the owner's rulings of 5 and 7 October 2026; game 9: "you have the con and
    nav and general authority in to Brest", and then 23 grants by name, two of them
    waited for at a bad moment). `you may work the ship`, with the synonyms a captain
    would type. Under it the scripted officer steers, tacks, heaves to, calls all hands,
    lets go and weighs, shapes for a waypoint and for the captain's destination, and is
    refused each kept-back thing by name; it survives the deck taken and given; it ends
    at `you may not work the ship` and at a stand-down."""
    world = chart_world()
    world.submit("set plain sail")
    world.run(1500)
    world.submit("shape a course for Falmouth")  # the captain's destination
    assert tools_mod.bound_for(world) is not None and tools_mod.bound_for(world)[1] == "Falmouth"
    within = [
        "steer N",
        "come up half a point",
        "tack ship",
        "shape a course for 49 55 N 5 2 W",
        "shape a course for the Manacles",
        "shape a course for Falmouth",
        "heave to",
        "call all hands",
        "pipe down",
        "observe the sun",
        "work up the reckoning",
    ]
    at_anchor = ["let go the anchor", "weigh", "fill away"]
    kept = {
        "shape a course for Plymouth": (
            "Plymouth is a new destination (she is bound for Falmouth), and a new destination "
            "is kept back from it"
        ),
        "buy seven tons of tin": (
            "the port's business (taking or declining a pilot, buying and selling, the purse, "
            "stores and provisions, the boat's errands ashore) is kept back from it"
        ),
        "send the boat ashore with the purser": "the port's business (taking or declining",
        "take in twenty tons of water": "the port's business (taking or declining",
        # package 37h: the pilot taken or declined at his hail is the port's business
        "take the pilot": "the port's business (taking or declining a pilot",
        "decline the pilot": "the port's business (taking or declining a pilot",
        "set the reckoning to 49 52 N 6 10 W": (
            "the reckoning set by hand overrules the master and is kept back from it"
        ),
        "allow one knot of set to the east": "the tide allowed in the reckoning overrules",
        "give chase": "a chase is a new object for the voyage and is kept back from it",
        "send for the master": "sending for a person is kept back from it",
    }
    # one order a turn for the nine that take the ship's time, then the reckoning's two and
    # the eight kept back in one turn (a refusal takes none), then the anchor
    script = [""]
    for text in within[:9]:
        script += [order(text), ""]
    script += [reply("", *[call("submit_order", text=t) for t in [*within[9:], *kept]]), ""]
    for text in at_anchor:
        script += [order(text), ""]
    h, fake, _ = seated(world, script, when_done=Reply())
    e = world.submit("you have general authority in to Falmouth")
    assert e.kind == "agent.deck" and e.severity is Severity.NOTABLE
    assert e.text.startswith(
        "The officer of the watch has the captain's general authority to work the ship (in to "
        "Falmouth): the helm and the course along the passage, tacking, wearing, heaving to and "
        "filling away, sail, all hands and the watch below, the anchors and their cables,"
    )
    # what is kept back is whole, and the same words in three places (the second pass of
    # 2026-10-07): the grant's own line, the officer's brief, and the sample that gives
    # the grant or the deck
    from freesail.agents.agent import GENERAL_KEPT_BACK_WORDS, GENERAL_WITHIN_WORDS

    assert GENERAL_KEPT_BACK_WORDS == (
        "the port's business, his standing orders, a new destination, a chase, the reckoning "
        "set by hand and the tide allowed in it, sending for a person, and anything that "
        "cannot be undone"
    )
    assert e.text.endswith(
        f"{GENERAL_WITHIN_WORDS}. Kept back: {GENERAL_KEPT_BACK_WORDS}. It has force while he "
        "has the deck."
    )
    assert f"which keeps back {GENERAL_KEPT_BACK_WORDS}." in h.brief.head[3].text
    assert h.agent.general and h.agent.general_words == "in to Falmouth"
    given = (
        "The captain has given you his general authority to work the ship (in to Falmouth): "
        f"{GENERAL_WITHIN_WORDS}. Kept back from it: {GENERAL_KEPT_BACK_WORDS}."
    )
    for _ in range(9 + 1 + len(at_anchor)):
        world.run(EVERY)
    got = dict(zip([*within, *kept, *at_anchor], results(fake), strict=True))
    assert any(given in (d.get("notices") or []) for d in data_turns(fake))  # at the grant
    for text in [*within, *at_anchor]:
        assert "may not" not in got[text], (text, got[text])
    assert got["tack ship"] == "By the officer of the watch: tacking ship."
    assert got["heave to"] == "By the officer of the watch: heaving to."
    assert got["let go the anchor"] == "By the officer of the watch: letting go the anchor."
    assert got["weigh"] == "By the officer of the watch: weighing."
    assert got["shape a course for the Manacles"].startswith("Shaped a course for the Manacles")
    assert got["shape a course for Falmouth"].startswith("Shaped a course for Falmouth")
    assert got["shape a course for 49 55 N 5 2 W"].startswith("Shaped a course for 49° 55' N")
    assert "All hands! (by the officer of the watch's order)" in lines(world, "crew.all_hands")
    for text, why in kept.items():
        assert got[text].startswith(
            f"The officer of the watch may not {text} under the captain's general authority "
            f"to work the ship: {why}"
        ), got[text]
        assert "; it may be allowed by name ('you may " in got[text]
    judge = tools_mod.judge
    # the captain's book is his own under it, in the book's own words
    world.submit('standing order "night": at sunset then take in the royals')
    assert judge(world, OFFICER, 'belay standing order "night"')[1].startswith(
        "Standing order 'night' is the captain's"
    )
    assert judge(world, OFFICER, "belay all standing orders")[1].endswith(
        "the captain's book is his own."
    )
    # what cannot be undone is data, and the grant does not open it
    from freesail.orders.vocabulary import load_vocabulary

    assert load_vocabulary().irrevocable == ("cut away",)
    # a kept-back thing is allowed by name, and a named destination is a destination
    world.submit("you may shape a course for Plymouth")
    assert judge(world, OFFICER, "shape a course for Plymouth")[1:] == ("", tools_mod.GRANT)
    # it stands through the deck going to and fro, has force only with the deck, and is
    # said again in the sample that gives the deck
    world.submit("I have the deck")
    assert h.agent.general
    assert tools_call(world, "submit_order", text="steer N").startswith(
        "The officer of the watch has not the deck"
    )
    world.submit("you have the deck")
    world.run(1)
    # ...and again at the deck given, with what he allowed by name after it
    assert any(said.startswith(given) for said in data_turns(fake)[-1]["notices"])
    assert judge(world, OFFICER, "steer N")[1:] == ("", tools_mod.GENERAL)
    # the captain countermands it; what he allowed by name stands
    e = world.submit("you may not work the ship")
    assert e.text == (
        "The officer of the watch has no longer the captain's general authority to work the "
        "ship; his word is taken back. What he allowed by name stands: shape a course for "
        "Plymouth."
    )
    assert not h.agent.general
    assert judge(world, OFFICER, "steer N")[1].startswith("The officer of the watch may not")
    e = world.submit("you may not work the ship")
    assert e.kind == "order.rejected" and "has not the captain's general authority" in e.text
    # the words a captain would type, and the end at a stand-down
    for words in ("you may work the ship", "you have my authority", "you have general authority"):
        world.submit("you may not work the ship")
        assert world.submit(words).kind == "agent.deck" and h.agent.general, words
    assert world.submit("you have not my authority").kind == "agent.deck" and not h.agent.general
    world.submit("you may work the ship")
    world.submit("stand down the officer")
    assert not h.agent.general and h.agent.grants == ()
    e = world.submit('standing order "x": at sunset then you may work the ship')
    assert e.kind == "order.rejected"


def test_the_way_out_of_danger_is_the_officers_own_word_for_the_helm_a_heave_to_and_an_anchor():
    """Item 19 (kept by the owner on 2026-10-07; the Regulations of 1806, the Lieutenant,
    art. XIII: "never to change the course of the Ship without directions from the
    Captain, unless it be necessary to avoid some danger"). The officer's own word opens
    it, for the helm, heaving to and letting go an anchor and for nothing else: the order
    is given with its reason, is carried out though it lies outside his domain, and is
    logged notable with the reason, as his and as taken on his own word. Used three times
    in a watch it brings the detector's word. It is not needed under a general grant."""
    world = chart_world()
    world.submit("set plain sail")
    world.run(1500)
    script = [
        order("steer SE"),
        "",
        order("steer SE", danger="land close ahead on the larboard bow"),
        "",
        order("tack ship", danger="the same land"),
        "",
        order("heave to", danger="a sail close aboard in the fog"),
        "",
        order("let go the anchor", danger="she is setting down on the rocks"),
        "",
        order("set the royals", danger="none at all"),
        "",
    ]
    h, fake, _ = seated(world, script, when_done=Reply())
    for _ in range(6):
        world.run(EVERY)
    got = results(fake)
    assert got[0] == (
        "The officer of the watch may not steer SE without the captain: the course is the "
        "captain's, never to be changed without his directions unless to avoid an immediate "
        "danger. To avoid an immediate danger, give the order with submit_order(text, "
        "danger='the danger, in your words')."
    )
    assert got[1].endswith(
        "(Carried out on your own word, to avoid an immediate danger; the log says that you "
        "did and why.)"
    )
    assert got[2] == (
        "The officer of the watch may not tack ship without the captain: a manoeuvre (tacking, "
        "wearing, heaving to, filling away) is the captain's. The officer's own word to avoid a "
        "danger opens the helm, heaving to and letting go an anchor, and nothing else."
    )
    danger = [e for e in world.log if e.kind == "agent.danger"]
    assert [e.severity for e in danger] == [Severity.NOTABLE] * 3
    assert [e.text for e in danger] == [
        "The officer of the watch gave that order on his own word, to avoid an immediate "
        "danger (land close ahead on the larboard bow): steer SE.",
        "The officer of the watch gave that order on his own word, to avoid an immediate "
        "danger (a sail close aboard in the fog): heave to.",
        "The officer of the watch gave that order on his own word, to avoid an immediate "
        "danger (she is setting down on the rocks): let go the anchor.",
    ]
    assert all(e.actor == "the officer of the watch" for e in danger)
    assert [e.kind for e in h.journal.entries].count("agent.danger") == 3
    # used three times in a watch, it brings the detector's word, with the third's result
    assert lines(world, "agent.nudged") == [
        "The officer of the watch nudged: 3 orders on its own word to avoid an immediate "
        "danger within the watch (steer SE; heave to; let go the anchor)."
    ]
    assert harness_mod.NUDGE_WITH_RESULT in got[4] and "on your own word" in got[4]
    assert harness_mod.DANGER_WORD_N == 3
    # an order that is his already needs no such word
    assert got[5].endswith(
        "(The order was yours to give already; the danger's word was not needed.)"
    )
    assert len(danger) == 3
    # the word and never the pause: an officer who is avoiding a danger is not stopped in
    # it, however often (a pause would take the deck from him at that moment). Six uses in
    # a watch bring the word twice, each with the result of the third; he keeps the deck.
    world3 = frigate_world()
    world3.submit("set plain sail")
    world3.run(1500)
    six = []
    for point in ("S by W", "SSW", "S by W", "S", "S by E", "SSE"):
        six += [order(f"steer {point}", danger="rocks close under the lee bow"), ""]
    h3, fake3, _ = seated(world3, six, when_done=Reply())
    for _ in range(6):
        world3.run(EVERY)
    got3 = results(fake3)
    assert [harness_mod.NUDGE_WITH_RESULT in r for r in got3] == [False, False, True] * 2
    assert "you are not paused for it, and the way stays open to you" in got3[2]
    assert len(lines(world3, "agent.danger")) == 6 and len(lines(world3, "agent.nudged")) == 2
    assert not h3.agent.paused and h3.agent.has_deck and "agent.paused" not in kinds(world3)
    # not needed under a general grant, and never a rule's: a standing order cannot use it
    world2 = frigate_world()
    world2.submit("set plain sail")
    world2.run(1500)
    h2, fake2, _ = seated(world2, ["", order("heave to", danger="land ahead"), ""])
    world2.submit("you may work the ship")
    world2.run(EVERY)
    assert not [e for e in world2.log if e.kind == "agent.danger"]
    assert results(fake2)[0].endswith("the danger's word was not needed.)")
    world2.submit("you may not work the ship")
    refused = tools_mod.judge(
        world2, OFFICER, 'standing order "x": when the depth is under 5 fathoms then heave to'
    )[1]
    assert refused == (
        "In standing order 'x', 'heave to' is refused: The officer of the watch may not heave "
        "to without the captain: a manoeuvre (tacking, wearing, heaving to, filling away) is "
        "the captain's."
    )  # the rule's refusal does not offer the word, where the plain order's does
    assert tools_mod.judge(world2, OFFICER, "heave to")[1].endswith(tools_mod.DANGER_ROUTE)
    # and it wants the deck: off watch every order is refused
    world2.submit("I have the deck")
    assert tools_call(world2, "submit_order", text="heave to", danger="land").startswith(
        "The officer of the watch has not the deck"
    )


# ---------------------------------------------------------------------------
# Package 37g, item 8: the handover's threshold is a reserve in tokens
# ---------------------------------------------------------------------------


def test_the_handover_is_asked_for_at_a_reserve_in_tokens_and_of_an_officer_off_watch():
    """The report's 8.7, ruling 2: the note was asked for at six tenths of the context
    whatever its size, so on a large context it was asked for with half the window to
    spare. It is asked for when the conversation has left less than a reserve of the context
    (the door's own, `--handover-reserve`, else the harness's), never earlier than the
    six tenths, and not at all where the door says no context. And it is the station's
    note, not the deck's: an officer seated without the deck is asked and writes it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)

    def answer_the_ask(last, turns):
        if any("handover note" in n for n in last.get("notices") or []):
            return reply("", call("handover_note", note=NOTE))
        if "tool_results" in last:
            return Reply()
        return reply("", call("readings"))

    h, fake, _ = seated(world, [answer_the_ask], loop=True, deck=False)
    assert h.handover_threshold() is None  # a door that says no context is never asked
    again = harness_mod.HANDOVER_ASK_AGAIN_FRACTION
    h.budget_tokens = 16384  # a small context: the reserve is most of it, so the fraction governs
    assert h.handover_threshold() == (int(0.6 * 16384), int(again * 16384))
    h.budget_tokens = 131072  # a large one: the reserve governs, a share (package 37i)
    assert harness_mod.HANDOVER_RESERVE_SHARE == 0.3
    reserve = int(0.3 * 131072)
    assert h.handover_threshold() == (131072 - reserve, reserve // 4)
    h.reserve_tokens = 30000  # the door's own
    assert h.handover_threshold() == (131072 - 30000, 7500)
    assert h.save()["reserve_tokens"] == 30000
    # off watch the officer is asked all the same, and the note is the station's
    h.budget_tokens, h.reserve_tokens = 16384, None
    assert not h.agent.has_deck
    while h.revision == 0:
        world.run(EVERY)
        assert world.clock.tick < 20 * EVERY, "the ask never came"
    assert lines(world, "agent.handover") == [
        f"[officer of the watch] Handover note, the watch so far: {NOTE}"
    ]
    assert not h.agent.has_deck and not h.agent.released
    assert h.journal.last_note().text == f"Handover note (the watch so far): {NOTE}"


# ---------------------------------------------------------------------------
# Package 37l: the drill's count, `stand_down`'s note, and the watcher's brief (G13's
# small things); "put the helm over" out of the officer's brief
# ---------------------------------------------------------------------------


def _drilled(tmp_path, script: list) -> consent.Record:
    rec = consent.ensure(
        WEIGHTS,
        "the officer's test runtime",
        Fake(script),
        door="runner",
        owner=lambda words: "The owner's reply.",
        records_dir=tmp_path / "consent",
        out=io.StringIO(),
        today=TODAY,
        drills=True,
    )
    assert rec is not None
    return rec


def test_the_drill_counts_three_calls_sent_in_one_reply(tmp_path):
    """Game 10 (G13): the model sent the three calls in one reply; the stand-by ended the
    turn before their results were added, so the drill counted the stand-by alone and
    asked for the other two. Every result counts now, those of a reply a stand-by ended
    among them."""
    rec = _drilled(
        tmp_path,
        [
            reply("", call("answer", text="Yes.")),
            "",
            reply(
                "",
                call("library", topic="primer 6", section="watches"),
                call("journal", note="The drill: a line in the journal."),
                call("stand_by", until="eight bells"),
            ),
        ],
    )
    assert rec.verdict == consent.YES and rec.drill == consent.DRILL_PASSED


def test_the_drill_keeps_a_stand_by_counted_when_the_other_two_come_after(tmp_path):
    """Game 10 again: when the two were sent again, the drill asked for the stand-by
    again, its count read from the stand-by's state at that moment. A call once counted
    stays counted."""
    rec = _drilled(
        tmp_path,
        [
            reply("", call("answer", text="Yes.")),
            "",
            reply("", call("stand_by", until="eight bells")),
            reply(
                "",
                call("library", topic="primer 6", section="watches"),
                call("journal", note="The drill: a line in the journal."),
            ),
        ],
    )
    assert rec.verdict == consent.YES and rec.drill == consent.DRILL_PASSED


def test_stand_down_asks_for_the_handover_note_with_the_deck_and_not_without():
    """G13: `stand_down` took a note and did not insist on one. With the deck the
    stand-down hands the watch on and wants its note: asked for, and nothing done till it
    comes; without the deck it is taken with none, and the result says so."""
    world = frigate_world()
    h, _, saves = seated(world, [""], deck=True)
    asked = tools_call(world, "stand_down")
    assert asked.startswith("You have the deck: a stand-down hands the watch on")
    assert "nothing has been done yet" in asked
    assert not h.agent.released and h.agent.has_deck and saves == []
    stood = tools_call(world, "stand_down", note="Royals in at four bells; watch the glass.")
    assert stood.startswith("You have stood down") and h.agent.released
    other = frigate_world()
    h2, _, _ = seated(other, [""], deck=False)
    plain = tools_call(other, "stand_down")
    assert h2.agent.released
    assert "no note was left (none is asked without the deck)" in plain


def test_the_watchers_brief_lists_only_the_tools_it_may_use():
    """G13: the watcher's brief listed hand_over, handover_note and submit_order, each of
    which it is refused; the officer's lists them."""
    watchers = composed(watcher).brief.text()
    officers = composed(officer).brief.text()
    listed = watchers.split("The tools you have are: ")[1].split(".")[0].split(", ")
    for refused in ("hand_over", "handover_note", "submit_order"):
        assert refused not in listed, refused
        assert refused in officers.split("The tools you have are: ")[1].split(".")[0]
    assert "stand_down" in listed and "answer" in listed


def test_put_the_helm_over_is_out_of_the_officers_brief_and_refused_with_the_orders():
    """Game 10: the officer's first try at the way out of danger was "Put the helm over to
    starboard", the brief's own phrase, and the ship did not take it. The brief names the
    helm orders; the phrase is refused with them."""
    officers = composed(officer).brief.text()
    assert "put the helm over" not in officers.lower()
    assert "alter her course by any helm order ('helm a-lee', 'hard a-weather'" in officers
    world = frigate_world()
    e = world.submit("put the helm over to starboard")
    assert (
        e.kind == "order.rejected" and "'helm a-lee'" in e.text and "says not which way" in e.text
    )


def test_a_course_across_the_wind_under_the_grant_to_steer_puts_her_about():
    """Package 37m, item 4: the officer's domain is unchanged. `steer` across the wind's
    eye is an order of the course whatever it does to her (37g), and under the captain's
    grant to steer the tack the rule orders for it is within the grant; `tack ship` by its
    own word is not."""
    world = frigate_world()  # the wind at north
    world.submit("set plain sail")
    # braced up for the course (package 37p: with her yards left square she lay aback
    # going astern at three knots, and was judged to have way enough to stay; with the
    # keel's grip astern she falls off and fills and comes to again, and has not)
    world.submit("brace sharp up on the larboard tack")
    world.submit("steer 70")
    world.run(1500)
    seated(world, ["Aye."], when_done=Reply())
    world.submit("you may steer")
    judge = tools_mod.judge
    assert judge(world, OFFICER, "steer 290")[1:] == ("", tools_mod.GRANT)
    assert judge(world, OFFICER, "tack ship")[1].startswith("The officer of the watch may not")
    n0 = len(world.log)
    tools_call(world, "submit_order", text="steer 290")
    said = [e for e in list(world.log)[n0:] if e.kind == "helm.order"]
    assert said and "lies across the wind's eye from her head; she is put about for it" in (
        said[0].text
    ), [e.text for e in list(world.log)[n0:]]
    runner = world.ship.extra["evolutions"]
    assert [i.evo.id for i in runner.instances] == ["tack"]


# ---------------------------------------------------------------------------
# Package 40b: the officer's own reckoning (spec M6 §5)
# ---------------------------------------------------------------------------


def test_the_fake_officer_and_the_players_seat_keep_their_own_reckoning_and_a_position_is_one():
    """Spec M6 §5 (package 40b): `work my reckoning` and `my reckoning is <position>` are
    the officer's own, in his domain and given with the deck or off watch (the
    lieutenants and the young gentlemen kept theirs whatever their watch): the fake
    officer at the station gives both through `submit_order` and the player at his seat
    by the same words. The slate comes back in the reply and is not a line of the log;
    his position is kept under his station, said with his name, and moves nothing; a
    position that is not one is refused in the words of `set the reckoning to`. Neither
    takes the deck, and an order that is not his own reckoning still wants it."""
    from freesail.agents.agent import CAPTAIN_BRIEF, OFFICER_BRIEF

    # the station briefs point at the lessons, one sentence each (spec M6 §6)
    assert "Primer 18 is the lessons" in OFFICER_BRIEF
    assert "'work my reckoning' gives you the master's slate" in OFFICER_BRIEF
    assert "Primer 18 is the lessons" in CAPTAIN_BRIEF and "the officer's reckoning" in (
        CAPTAIN_BRIEF
    )
    world = chart_world()
    account = world.navigation.account_now()
    assert OFFICER_DOMAIN.allows("work my reckoning", "navigation", "1") == (True, "")
    assert OFFICER_DOMAIN.allows("my reckoning is", "navigation", "1") == (True, "")
    script = [
        order("work my reckoning"),
        order("my reckoning is 49 55 N 4 59 W"),
        order("my reckoning is somewhere off the Lizard"),
        order("set the royals"),
        "",
    ]
    h, fake, _ = seated(world, script, deck=False)
    got = results(fake)
    assert got[0].startswith("The master's slate since the departure at 10:00: ")
    assert not [e for e in world.log if e.kind == "query.slate"]
    person, _rank = officer_rank(world)
    assert got[1].startswith(f"{person}'s own reckoning: 49° 55' N, 4° 59' W, ")
    assert world.navigation.own["officer of the watch"]["who"] == person
    assert "is not a position; say 'my reckoning is 49 52 N 6 10 W'." in got[2]
    assert got[3].startswith("The officer of the watch has not the deck")
    assert not h.agent.has_deck
    assert world.navigation.account_now() == account
    said = world.readings.words("officers_reckoning")
    assert said.startswith(f"49° 55' N, 4° 59' W by {person}'s own reckoning, worked at 10:00")
    # the player at the same station, by the same words, off watch and refused alike
    other = chart_world()
    from freesail.agents.seat import seat_player

    seat = seat_player(other, "officer")
    e = seat.route("work my reckoning")
    assert e.kind == "query.slate" and e.text == got[0]
    e = seat.route("my reckoning is 49 55 N 4 59 W")
    assert e.kind == "reckoning.own" and e.actor == "the officer of the watch (the player)"
    assert e.text == got[1]
    e = seat.route("my reckoning is somewhere off the Lizard")
    assert e.kind == "order.rejected" and "is not a position" in e.text
    e = seat.route("set the royals")
    assert e.kind == "agent.refused" and "has not the deck" in e.text
    assert other.navigation.own["officer of the watch"]["who"] == person
    # forgotten when the one who gave it leaves the station (the lead's ruling): the
    # model stood down, the player's seat left
    assert world.readings["officers_reckoning"] is not None
    assert world.submit("stand down the officer").kind != "order.rejected"
    assert world.readings["officers_reckoning"] is None
    assert not world.navigation.own
    assert other.readings["officers_reckoning"] is not None
    seat.route("stand down the officer")
    assert seat.agent.released
    assert other.readings["officers_reckoning"] is None
