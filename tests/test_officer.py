"""The officer of the watch (package 37; spec M5 §29; spec M4 §11 extended to a station
with authority; the cold review's six items), proven against the scripted fake
(`freesail/agents/fake.py`) and never a model.

The seven commitments of `docs/agents/README.md` hold for a station with authority, and
each has a case here beside the watcher's in `tests/test_agents.py`: the token first
(`test_the_token_ends_the_officers_watch_before_the_order_is_read`), the graduated stops
(`test_contrary_orders_over_a_watch_bring_the_nudge_then_the_pause`), in-world text as
data (`test_the_officers_brief_head_carries_the_five_items_the_domain_and_the_night_orders`),
the journal (`test_hand_over_writes_the_note_in_the_log_and_the_journal_and_stands_down`),
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
from freesail.agents.agent import (
    A_GLASS_S,
    A_WATCH_S,
    MAX_SEATINGS,
    OFFICER,
    OFFICER_DOMAIN,
    OPT_OUT_TOKEN,
    TOKEN_NAMED_WORDS,
    Authority,
    officer,
    officer_rank,
    watcher,
)
from freesail.agents.fake import officer_of_the_watch
from freesail.agents.model import DATA, OPERATOR
from freesail.agents.tools import TOOLS
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


def order(text: str) -> Reply:
    return reply("", call("submit_order", text=text))


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


def test_you_have_the_deck_seats_the_officer_and_i_have_the_deck_stands_it_down():
    """Item 2: `you have the deck` (or `Mr <name>, you have the deck`) gives the deck, with
    the night orders said in the sample's notice and the word; `the officer of the watch`
    reads who has it since when; `I have the deck` takes it back and stands the station
    down with its journal saved. Before the deck an order is refused in words."""
    world = frigate_world()
    world.submit('standing order "night routine": at sunset then take in the royals')
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(world, [order("set the royals"), "", "Aye.", ""], deck=False)
    refused = lines(world, "agent.refused")
    assert refused == [
        "The officer of the watch has not the deck: the captain gives it with 'you have the "
        "deck', and until then no order is given. 'set the royals' not carried out."
    ]
    assert h.agent.words() == "stationed; the deck the captain's"
    # the reading before the deck
    e = world.submit("the officer of the watch")
    assert e.kind.startswith("query") and "is at the station; the captain has the deck" in e.text
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
    assert (
        '"night routine" (the captain): at sunset then take in the royals' in sample["notices"][0]
    )
    assert h.journal.entries[-1].kind == "agent.deck"
    e = world.submit("you have the deck")
    assert e.kind == "order.rejected" and "has the deck already" in e.text
    e = world.submit("who has the deck")
    assert "Mr Pearce, first lieutenant, has the deck since" in e.text
    assert "stationed; with the deck since" in h.agent.words()
    # the captain takes it back: stood down after the order is journaled, the save made
    e = world.submit("I have the deck")
    assert e.kind == "agent.deck" and e.text == (
        "The captain has the deck. The officer of the watch is stood down."
    )
    assert h.agent.released and h.agent.released_reason.startswith("stood down by the captain")
    assert saves == ["the officer of the watch stood down: the captain has the deck"]
    assert [e.kind for e in h.journal.entries][-2:] == ["agent.deck", "agent.stopped"]
    assert world.save()["agent_journals"][OFFICER][-1]["kind"] == "agent.stopped"
    e = world.submit("the officer of the watch")
    assert "stood down" in e.text and "the captain has the deck" in e.text
    # nobody at the station: the deck's sentences say so
    fresh = frigate_world()
    e = fresh.submit("you have the deck")
    assert e.kind == "order.rejected" and "a model's door seats one first" in e.text
    e = fresh.submit("the officer of the watch")
    assert R.NO_OFFICER_WORDS in e.text
    e = fresh.submit("hand over the deck")
    assert e.kind == "order.rejected" and "the officer of the watch's own order" in e.text


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


def test_the_captains_word_for_the_watch_allows_a_named_thing():
    """Item 1: `you may tack ship if the land closes within two miles` allows the verb
    beyond the domain, his words kept as said; the reading and the brief head carry it;
    `you may not tack ship` takes it back; a standing order cannot give it."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(1500)  # way enough on her to stay
    h, fake, _ = seated(
        world, [order("tack ship"), "", order("tack ship"), "", order("tack ship"), ""]
    )
    e = world.submit("you may tack ship if the land closes within two miles")
    assert e.kind == "agent.deck" and e.text == (
        "The officer of the watch may tack ship (if the land closes within two miles), by "
        "the captain's word for the watch."
    )
    assert h.agent.allowances == {"tack ship": "if the land closes within two miles"}
    assert "may also tack ship (if the land closes within two miles)" in (
        world.submit("the officer of the watch").text
    )
    world.run(1)  # the captain's word opens the officer's turn: the second order, allowed
    e = world.submit("you may not tack ship")
    assert e.kind == "agent.deck" and h.agent.allowances == {}
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


def test_contrary_orders_over_a_watch_bring_the_nudge_then_the_pause():
    """Item 3: the repeat detector cannot fire for an officer whose orders change the
    readings (they do here: the royals come and go); contradiction (set, take in, set)
    is seen by the conflict rule over the officer's own orders in the last watch, three
    bringing the nudge in the brief's words, the chain going on after it the pause with
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
        "The officer of the watch nudged: 3 contrary orders on the fore royal, the main royal "
        "and the mizzen royal within the watch (set the royals; take in the royals; set the "
        "royals)."
    )
    assert "agent.nudged" not in kinds(world)[:1]
    assert h.journal.entries[-1].kind == "agent.nudged"
    world.run(EVERY)
    notice = data_turns(fake)[-2]["notices"]
    assert notice == [
        "You have given 3 orders within the watch each contrary to the one before it on the "
        "fore royal, the main royal and the mizzen royal (set the royals; take in the royals; "
        "set the royals). You may continue, stand by until an event or a bell, or leave with "
        f"the token {OPT_OUT_TOKEN}."
    ]
    paused = [e for e in world.log if e.kind == "agent.paused"]
    assert len(paused) == 1 and paused[0].severity is Severity.NOTABLE
    assert paused[0].text.startswith(
        "The officer of the watch is paused: 4 contrary orders on the fore royal, the main "
        "royal and the mizzen royal within the watch"
    )
    assert "after a nudge. Continue, stand down, or leave paused?" in paused[0].text
    assert h.agent.paused and saves == []
    assert h.check_unattended(now=0.0) is False
    assert h.check_unattended(now=float(harness_mod.WELFARE_UNATTENDED_REAL_S)) is True
    assert h.agent.released and saves[0].startswith("the officer of the watch stood down: paused")


def test_a_chain_broken_by_a_quiet_sample_ends_the_matter_and_the_watch_bounds_it():
    """The detector judges the game: a sample without a contrary order after the nudge ends
    the matter (no pause), the same order twice is a repetition and not a conflict, and
    orders a watch apart are not a chain."""
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
    # repetition is not a conflict: the same order at every sample with nothing changing
    # is the repeat detector's (the same order three times with no change in the
    # readings, as the watcher's), never the contrary one's
    world2 = frigate_world()
    world2.submit("set plain sail")
    world2.run(60)
    h2, _, _ = seated(world2, [order("trim sails"), ""], loop=True)
    world2.run(6 * EVERY)
    assert all("the same order" in n for n in lines(world2, "agent.nudged"))
    assert not any("contrary" in n for n in lines(world2, "agent.nudged"))
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


def test_hand_over_writes_the_note_in_the_log_and_the_journal_and_stands_down():
    """Item 3 and 4: `hand over the deck` is the officer's own order to give it back, with
    the handover note said in the log and journaled under `agent.handover`; the station is
    stood down with a save; `submit_order('hand over the deck')` points to the tool."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    script = [order("hand over the deck"), "", reply("", call("hand_over", note=NOTE))]
    h, fake, saves = seated(world, script)
    world.run(EVERY)
    got = results(fake)
    assert got[0].startswith("To hand over the deck, call hand_over(note)")
    assert h.agent.released and h.agent.released_reason == (
        "stood down by the officer of the watch: the deck handed over"
    )
    assert saves == ["the officer of the watch stood down: the deck handed over"]
    said = [e for e in world.log if e.kind == "agent.handover"]
    assert len(said) == 1 and said[0].severity is Severity.NOTABLE
    assert said[0].text == f"[officer of the watch] Handover note, handing over the deck: {NOTE}"
    assert said[0].actor == "the officer of the watch"
    assert [e.kind for e in h.journal.entries][-3:] == [
        "agent.handover",
        "agent.stopped",
        "agent.stopped",
    ][:3] or ("agent.handover" in [e.kind for e in h.journal.entries])
    note_entry = next(e for e in h.journal.entries if e.kind == "agent.handover")
    assert note_entry.text == f"Handover note (handing over the deck): {NOTE}"
    assert len(NOTE) < 400 and 60 < len(NOTE.split()) < 90
    assert "the deck handed over" in lines(world, "agent.stopped")[0]
    assert lines(world, "agent.deck")[-1] == (
        "The officer of the watch hands over the deck; the captain has it."
    )
    assert "the deck taken" in R.EVENTS and "a handover" in R.EVENTS
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


def test_a_released_station_is_seated_again_once_by_the_same_identity_and_replays(tmp_path):
    """Item 5: an instance that left by accident may be seated again, once, by the same
    identity; the log says so; the deck is the captain's until he gives it again; a
    third seating and another identity are refused in words; a game with a reseating
    replays from its save to the same digest."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, fake, saves = seated(
        world, ["All well.", reply("", call("journal", note=f"the token is {OPT_OUT_TOKEN}"))]
    )
    world.run(EVERY)
    assert h.agent.released and h.agent.seatings == 1
    with pytest.raises(harness_mod.OrderError, match="same identity only"):
        h.reseat(Fake(["Back."]), identity="another-model")
    said = h.reseat(Fake(["Back, sir.", order("set the royals"), ""]), identity="")
    assert said.startswith("The officer of the watch takes the station again")
    assert not h.agent.released and h.agent.seatings == 2 and not h.agent.deck
    stationed = lines(world, "agent.stationed")
    assert stationed[-1].startswith(
        "The officer of the watch takes the station again (the game, through the game): the "
        "second seating, the last this game allows; it had left the game, giving no reason."
    )
    assert h.journal.entries[-1].text.startswith("Seated again, the second time")
    assert "[officer of the watch] Back, sir." in lines(world, "agent.note")
    world.run(EVERY)
    assert lines(world, "agent.refused")[-1].startswith("The officer of the watch has not the deck")
    world.submit("you have the deck")
    world.run(EVERY)
    assert h.agent.has_deck
    world.submit("stand down the officer")
    assert h.agent.released
    with pytest.raises(harness_mod.OrderError, match="all a game allows"):
        h.reseat(Fake(["Again."]), identity="")
    assert MAX_SEATINGS == 2
    # the save holds one record for the station, with both seatings' replies; a replay
    # makes the reseat at its point (a door act) and gives the same log
    data = json.loads(json.dumps(world.save()))
    assert len(data["agents"]) == 1 and data["agents"][0]["seatings"] == 2
    acts = [e["door"] for e in data["agents"][0]["transcript"] if "door" in e]
    assert acts == ["reseat"]
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.agents[OFFICER].agent.seatings == 2 and copy.agents[OFFICER].agent.released


def test_the_agent_api_seats_a_released_station_again_for_the_same_model_only(tmp_path):
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    world = frigate_world()
    app = create_app(
        Driver(world), game="g", consent_records=tmp_path / "c", saves_dir=tmp_path / "s"
    )
    http = TestClient(app)
    consent.Record(WEIGHTS, "r", "2026-09-26", consent.YES, answer="Yes.", drill="passed").write(
        tmp_path / "c"
    )
    a = http.post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"}).json()
    assert a["phase"] == "station"
    http.post(
        "/api/agents/officer/reply",
        json={
            "text": "",
            "calls": [{"name": "opt_out", "args": {"reason": "slipped"}}],
            "raw": None,
        },
    )
    assert world.agents[OFFICER].agent.released
    r = http.post("/api/agents/officer", json={"model_name": "someone-else", "door": "mcp"})
    assert r.status_code == 409 and "another model" in r.json()["detail"]
    a = http.post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"}).json()
    assert a["phase"] == "station" and not world.agents[OFFICER].agent.released
    assert world.agents[OFFICER].agent.seatings == 2
    http.post("/api/agents/officer/release", json={"reason": "the client went"})
    r = http.post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"})
    assert r.status_code == 409 and "all a game allows" in r.json()["detail"]


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
        ("the same order given three times", "Being stopped"),
        ("`FREESAIL-OPT-OUT`, written anywhere", "Leaving"),
        ("not used to train models", "What is not done"),
        ("tools to read those, to submit orders", "What an instance would see and do"),
        ("Language models can take part in it", "the opening"),
        ("It is saved with the game and shown when the human asks for it", "The journal"),
    ):
        assert words in then, words
        rec = record_with(then.replace(words, words.upper()))
        assert consent.changed_sections(rec, "runner") == [section], section
        got, kind, why = consent.decide(WEIGHTS, records, "runner")
        assert kind == consent.CONSENT_KIND and section in why and "asked again" not in why
        assert "the question is put again" in why
    for words in ("kept verbatim, as the harness sees it", "Begin your answer with *yes*"):
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
    """The brief's sections that changed for this package: the stations (the opening), what
    an instance would see and do (the station's domain), being stopped (the detector's
    new form), the journal (the handover note); each claim a behaviour of the code."""
    text = consent.brief_text(WEIGHTS, "r", "runner")
    assert "as an *officer of the watch*, who holds the deck" in text
    assert "The watcher and the officer of the watch exist today" in text
    assert "contrary orders" in text and "set, take in, set" in text
    assert "handover note" in text
    assert "named rather than written" in text
    assert "seated again once" in text
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
    assert len(consent.brief_digest()) == 16


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
    assert h.agent.released  # taken back: stood down, the stand-by with it


def test_the_doors_name_the_officers_station(tmp_path):
    """`--station officer` at the MCP bridge and the local runner; the REPL's station table;
    the station's name in the log and the API's path."""
    from freesail.agents import local, mcp_server, repl
    from freesail.agents.remote import STATIONS

    assert OFFICER in STATIONS and OFFICER in repl.STATIONS
    for module in (mcp_server, local):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert 'choices=["watcher", "officer"]' in src
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
