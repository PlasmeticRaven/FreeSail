"""The captive's channel (spec M7 §19; package 74, step 3; the design in
`docs/design/Design-Prizes.md` §3): the player's ship struck and taken possession of by her
captor's rules captain (near, and the far body made a hull), the player's person aboard the
captor with his station stood down and his prompt following his body, a prisoner's reach at
her prompt and refusals in words; the parole asked by doctrine in the period's words,
answered in his own words or by rule, the places it gives, the sword returned; the
prisoners landed at the port's agent; the director's parole form and the cartel."""

from __future__ import annotations

import math
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import captive as C
from freesail.world import crews
from freesail.world import prizes as P
from freesail.world.geo import destination
from freesail.world.ships import vessel_from_spec
from freesail.world.things import things_of
from tests.test_brains import put, world_at
from tests.test_fight import FRIGATE

BREST_ROAD = {
    "lat_deg": 48.34181,
    "lon_deg": -4.69340,
}  # the road of Bertheaume, the port's outer road
OFF_BREST = "bound for Brest"  # from her road, the port's own track in


def _scenario(position: dict | None = None) -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=position or {"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
    )


def _struck_to_a_crewed_frigate(
    seed: int = 7,
    position: dict | None = None,
    her_goal: str = "bound for 48 20 N 4 50 W",
    fired_on_her: bool = False,
):
    """The player's frigate at quarters with a French frigate crewed ten metres off her beam,
    her captain engaging by his own machine; the player strikes his colours and her captain
    takes possession within the quarter hour (`taking possession`: closed, hove to, `take
    possession of her`). Returns (the player's World, her captor's hull) at the possession.
    With `fired_on_her` the player's ship stands among her captain's enemies by her shot
    before she strikes, as `combat.action._fired_on` writes it."""
    w = make_world(seed, FRIGATE, _scenario(position))
    w.submit("beat to quarters")
    w.run(5)
    heading = math.degrees(float(w.ship.heading))
    there = destination(w.position, heading + 90.0, 10.0)
    w.vessels.serial += 1
    v = vessel_from_spec(
        w,
        {
            "description": "frigate",
            "name": "Medusa",
            "nation": "france",
            "position": there,
            "goal": her_goal,
            "intent": her_goal,
        },
        w.vessels.serial,
    )
    v.plan = [("lie_to", math.inf)]
    v.sail_state = "lying to"
    w.vessels.add(v)
    enemy = crews.promote(w, v)
    # made from a far body lying to, she heaves to by the evolution (package 60, ruling A on
    # the fourth reading); the action begins once she lies so
    for _ in range(60):
        if enemy.ship.extra.get("hove_to"):
            break
        w.run(10)
    assert enemy.ship.extra.get("hove_to"), "the captor never came to lie to"
    enemy.ship.dyn.heading = float(w.ship.heading)
    enemy.captain.state = None
    enemy.submit("beat to quarters")
    w.submit("hold your fire")
    w.run(65)
    enemy.captain._enter("engaging")
    if fired_on_her:
        from freesail.combat.action import _own_id

        enemy.captain.fired_on.add(_own_id(w))
    w.run(60)
    assert w.submit("strike the colours").kind == "action.struck"
    for _ in range(12):
        w.run(60)
        if C.captive_of(w):
            break
    assert C.captive_of(w), "possession of the player's ship not taken within the quarter hour"
    return w, enemy


def _kinds(log, *kinds):
    return [e for e in log if e.kind in kinds]


# -- the player struck -----------------------------------------------------------------------------


def test_the_player_struck_is_a_person_aboard_the_captor_his_station_down_and_his_prompt_with_him():
    """The design's §3.1: the captor's rules captain takes possession of the player's ship
    (her record, her muster swapped, a prize master at her captain's station); the player's
    person is put aboard the captor in the cabin, a prisoner, his parole not asked, his sword
    in her captain's keeping, his own ship's station stood down; the drivers follow him (the
    prompt is the captor's), `where am I` says his state; her deck is refused him in words
    naming it, and his own ship's deck from her prompt and from his ship's prompt (a prize
    under a prize master); the captor's captain shapes his course for his port with the
    prisoners."""
    w, enemy = _struck_to_a_crewed_frigate()
    rec = C.captive_of(w)
    assert rec["person"] == "Captain Bowen" and rec["home"] == w.players.id
    assert rec["captor"] == enemy.id and rec["sword"]
    me = C.captive_person(w)
    assert me is not None and me.name == "Captain Bowen"
    assert me.hull == enemy.id and me.home == w.players.id and me.where == "cabin"
    assert me.confined_to == "cabin" and me.liberty == ()
    # his ship a prize: the prize master at her captain's station, her people prisoners
    prize = P.record_of(w.vessels.own)
    assert prize is not None and prize["how"] == "taken possession of"
    assert prize["captive"] == "Captain Bowen" and prize["captive_port"] == "brest"
    master = w.players.stations.holder("captain")
    assert master is not None and master.name == prize["master"] and master.home == w.players.id
    assert w.players.people.captain is master
    assert P.prisoners_of(w.players.ship).count == prize["prisoners"] > 200
    # the drivers follow him
    assert w.followed == enemy.id and w.own is enemy
    assert any(e.kind == "hull.followed" and "Captain Bowen" in e.text for e in enemy.log)
    taken = _kinds(enemy.log, "prize.captive")
    assert len(taken) == 1 and "lately commanding the Amazon" in taken[0].text
    assert "his sword is in Captain" in taken[0].text
    assert any(
        e.kind == "captain.intent" and "course for Brest with the prisoners" in e.text
        for e in enemy.log
    )
    assert enemy.captain.intent is not None and enemy.captain.intent.destination == "brest"
    # the sword
    swords = [t for t in things_of(w) if t.name == "Captain Bowen's sword"]
    assert len(swords) == 1 and swords[0].keeper == enemy.people.captain.id
    assert swords[0].keeper_home == enemy.id
    # his reach at her prompt
    said = w.submit("where am i").text
    assert (
        "aboard the Medusa, in the cabin, a prisoner, his parole not asked, of the Amazon" in said
    )
    out = w.submit("steer west")
    assert out.kind == "order.rejected"
    assert "You are a prisoner aboard the Medusa; her deck is not yours" in out.text
    assert "say to the captain" in out.text
    assert w.submit("the ship").text.startswith("The ship: The ship: Medusa")
    assert w.submit("go to the boat").kind == "order.rejected"
    assert enemy.readings.words("prisoners").startswith("one prisoner of rank: Captain Bowen")
    # his own ship's deck from her prompt and from his ship's: a prize's
    assert w.follow("the ship").kind != "order.rejected"
    out = w.submit("steer west")
    assert out.kind == "order.rejected" and "a prize under a prize master" in out.text
    assert "aboard the Medusa" in w.submit("where am i").text
    w.follow("Medusa")
    assert w.own is enemy


def test_the_parole_asked_by_doctrine_in_the_captors_words_and_given_in_the_captives_own():
    """The design's §3.2: the French captain asks a minute after the taking, in French and
    English from the hail table's parole rows, a line of her log where the captive stands;
    the captive's `say to the captain: I give you my parole` is read for it (and only while
    it is asked): given, the cabin and the gunroom are his and the quarterdeck by day, his
    sword is returned him, and the captain's acknowledgement is said; `where am I` says
    'on parole'; his moves within his liberty are his, beyond it refused."""
    w, enemy = _struck_to_a_crewed_frigate()
    w.run(120)
    asked = _kinds(enemy.log, "prize.parole_asked")
    assert len(asked) == 1 and asked[0].text.startswith("Captain Pope, in the cabin: Votre parole")
    assert "Captain Bowen, your sword is returned you" in asked[0].text
    pris = P.prisoners_of(enemy.ship)
    assert pris.parole["Captain Bowen"] == "asked"
    # words that read for nothing leave the question open
    out = w.submit("say to the captain: a hard thing, sir, to lose her so")
    assert out.kind == "person.spoke" and out.data["parole_read"] is False
    assert pris.parole["Captain Bowen"] == "asked"
    out = w.submit("say to the captain: I give you my parole, sir")
    assert out.kind == "person.spoke" and out.data["parole_read"] is True
    assert out.text.startswith("Captain Bowen, in the cabin, to the captain: I give you my parole")
    assert pris.parole["Captain Bowen"] == "given"
    given = _kinds(enemy.log, "prize.parole")
    assert len(given) == 1 and "gives his parole (in his own words)" in given[0].text
    assert "his sword is returned him" in given[0].text
    answered = _kinds(enemy.log, "prize.parole_answered")
    assert len(answered) == 1 and "Votre parole me suffit" in answered[0].text
    me = C.captive_person(w)
    assert me.liberty == C.PLACES_ON_PAROLE and me.confined_to == "cabin"
    sword = next(t for t in things_of(w) if t.name == "Captain Bowen's sword")
    assert sword.keeper == me.id and sword.keeper_home == w.players.id
    assert "a prisoner on parole, of the Amazon" in w.submit("where am i").text
    assert w.submit("come on deck").kind == "person.moved" and me.where == "quarterdeck"
    assert w.submit("go below").kind == "person.moved" and me.where == "gunroom"
    out = w.submit("go to the hold")
    assert out.kind == "order.rejected" and "Your parole gives you" in out.text
    # a second parole sentence reads for nothing: the question is answered
    out = w.submit("say to the captain: I give my parole again")
    assert out.data["parole_read"] is False
    assert enemy.readings.words("prisoners").endswith("Captain Bowen in the cabin (parole given)")


def test_the_parole_refused_asked_again_after_a_glass_and_given_by_rule_after_a_watch():
    """§3.2's other roads: refused in his own words, the gunroom alone is his and a sentry at
    the door (said); nothing said, the captain asks once more after a glass and takes an
    officer's parole as given by the custom after a watch, each a line of the log."""
    w, enemy = _struck_to_a_crewed_frigate()
    w.run(120)
    out = w.submit("say to the captain: I will not give it, sir")
    assert out.data["parole_read"] is True
    me = C.captive_person(w)
    pris = P.prisoners_of(enemy.ship)
    assert pris.parole["Captain Bowen"] == "refused"
    assert me.confined_to == "gunroom" and me.where == "gunroom" and me.liberty == C.PLACES_REFUSED
    refused = _kinds(enemy.log, "prize.parole")
    assert len(refused) == 1 and "refuses his parole" in refused[0].text
    assert "a sentry at the door" in refused[0].text
    assert "Comme vous voulez" in _kinds(enemy.log, "prize.parole_answered")[0].text
    assert "a prisoner, his parole refused" in w.submit("where am i").text
    assert w.submit("come on deck").kind == "order.rejected"
    # by rule: nothing said for a watch
    w2, enemy2 = _struck_to_a_crewed_frigate()
    for _ in range(4 * 60 + 5):
        w2.run(60)
        if P.prisoners_of(enemy2.ship).parole.get("Captain Bowen") == "given":
            break
    asked = _kinds(enemy2.log, "prize.parole_asked")
    assert len(asked) == 2 and "il me faut votre réponse" in asked[1].text
    assert asked[1].tick - asked[0].tick >= C.PAROLE_ASK_AGAIN_S
    given = _kinds(enemy2.log, "prize.parole")
    assert (
        len(given) == 1 and "the captain's word: an officer's parole by the custom" in given[0].text
    )
    assert given[0].tick - asked[0].tick >= C.PAROLE_BY_RULE_S
    assert C.captive_person(w2).liberty == C.PLACES_ON_PAROLE


def test_the_director_sets_a_parole_for_a_captive_nobody_asks_and_is_doubted_while_one_waits():
    """§3.2: `aboard the Medusa: the parole of Captain Bowen given` performs for a captive
    aboard her, is doubted (not refused) while her captain has asked and waits his answer,
    and is refused for a person who is no prisoner of hers."""
    from freesail.world import orders as WO

    w, enemy = _struck_to_a_crewed_frigate()
    w.run(120)  # asked
    order = WO.parse("aboard the Medusa: the parole of Captain Bowen given")
    doubt = WO.doubt(w, order)
    assert doubt is not None and "waits his answer" in doubt
    e = w.world_order("aboard the Medusa: the parole of Captain Bowen refused", "the test")
    assert e.data.get("result") == "done", e.text
    pris = P.prisoners_of(enemy.ship)
    assert pris.parole["Captain Bowen"] == "refused"
    # the captor's log's line, which the captive aboard her hears, is the world's: it names
    # no director (old: "refuses his parole (the director's word): ...")
    line = _kinds(enemy.log, "prize.parole")[0]
    assert line.text == (
        "Captain Bowen refuses his parole: the gunroom alone is his, a sentry at the door."
    )
    assert "director" not in line.text and "director" not in str(line.data).lower()
    e = w.world_order("aboard the Medusa: the parole of Mr Veale given", "the test")
    assert e.data.get("result") != "done" and "no prisoner aboard the Medusa" in e.text


# -- the far body ----------------------------------------------------------------------------------


# -- step 3's mends from the owner's play (2026-11-09) ---------------------------------------------


def _metres_between(a, b) -> float:
    from freesail.world.geo import bearing_and_distance

    return float(bearing_and_distance(a, b)[1])


def test_a_captives_words_and_readings_never_stand_his_captors_captain_aside():
    """The owner's play, the worst of five: a prisoner's 'say to Captain Penrose Yes.' was
    taken for the player's hand on the captor's captain (`Captain.player_hand`, decision
    41), who stood aside with his book struck; nobody commanded her, she lay aback and took
    the ground. A captive's words, readings and moves aboard his captor are a person's own:
    her captain commands throughout, no `captain.aside` is written, and she sails for her
    port. The rule is the giver's (`movement.hand_on_her`): one of her own company and a
    free man; a visitor of another ship's is no hand on her either."""
    from freesail.world import movement as M

    w, enemy = _struck_to_a_crewed_frigate()
    cap = enemy.captain
    w.run(120)  # he fills and shapes his course; the parole is asked
    assert cap.state == "on passage" and not cap.aside and cap.intent_words == "bound for Brest"
    before = enemy.position
    for words in (
        "say to the captain: Yes.",
        "where am I",
        "say to the captain: I thank you, sir.",
        "go to the deck",
        "go below",
        "hail her",
        "take a fix",
    ):
        w.submit(words)
        assert not cap.aside and cap.state == "on passage", words
    w.run(600)
    assert not cap.aside and cap.state == "on passage" and cap.commands
    assert not _kinds(w.log, "captain.aside") and not _kinds(enemy.log, "captain.aside")
    assert _metres_between(before, enemy.position) > 300.0, "she does not sail for her port"
    # the rule by its giver: the captive, a visitor of another hull's, one of her own
    assert M.hand_on_her(w, "captain") is False
    visitor = type("P", (), {"name": "Mr Veale", "home": "another"})
    visitor.confined_to, visitor.liberty = "", ()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(M, "person_of_actor", lambda world, actor: visitor())
        assert M.hand_on_her(enemy, "captain") is False
        visitor.home = enemy.own.id
        assert M.hand_on_her(enemy, "captain") is True
        mp.setattr(M, "person_of_actor", lambda world, actor: None)
        assert M.hand_on_her(enemy, "captain") is True


def test_a_captor_she_fired_on_before_she_struck_does_not_engage_his_own_prize():
    """The owner's play, the second: the player had fired on her before he struck, so he
    stood in her captain's `fired_on`; a minute after the possession Captain Penrose went
    `engaging` again and fired into his own prize, his prize master and twenty hands aboard
    her. His own prize, and any prize of his nation in her captor's hands, is no enemy
    (`Judgement._prize_of_ours`), and the taking clears her from what he knew her an enemy
    by. (Without the mend, in this scene: `engaging` at the first judgement after the
    possession and 38 shot at her in the quarter hour, measured.)"""
    w, enemy = _struck_to_a_crewed_frigate(fired_on_her=True)
    cap = enemy.captain
    me = str(w.players.id)  # the player's ship, by her id on the one sea
    assert me not in cap.fired_on, "the taking did not clear her from his enemies"
    taken = w.clock.tick
    w.run(900)
    assert cap.state == "on passage" and not cap.aside
    states = [e for e in _kinds(enemy.log, "captain.state") if e.tick > taken]
    assert states and not any("engaging" in e.text for e in states), [e.text for e in states]
    assert not [e for e in _kinds(enemy.log, "action.fired") if e.tick > taken]
    assert not [e for e in _kinds(w.players.log, "action.fired_at") if e.tick > taken]
    # the judgement itself: she is his prize, whatever she did; given back, judged as any sail
    assert cap._prize_of_ours(me) and cap._known_enemy({"id": me}) is False
    cap.fired_on.add(me)
    assert cap._known_enemy({"id": me}) is False
    rec = P.record_of(enemy.vessels.get(me))
    rec["retaken"] = ("retaken", "a test", w.clock.tick)
    assert cap._known_enemy({"id": me}) is True
    del rec["retaken"]


def test_a_bare_yes_gives_the_parole_and_a_bare_no_refuses_it_read_as_whole_words():
    """The owner's play, the third: 'say to Captain Penrose Yes.' left the parole asked.
    While the question is open a bare yes, oui, sí, aye, 'I do', 'you have it' gives it and
    a bare no, non, 'never', 'I will not' refuses it, as whole words ('not' is no 'no',
    'yesterday' no 'yes'); both in one answer read as neither and the question stays open;
    nothing is read once it is answered."""
    assert all(C._whole_words(t, C.PAROLE_YES_WORDS) for t in ("yes.", "oui, monsieur", "i do"))
    assert all(C._whole_words(t, C.PAROLE_NO_WORDS) for t in ("no.", "non", "i will not, sir"))
    assert not C._whole_words("yesterday i did not know", C.PAROLE_YES_WORDS)
    assert not C._whole_words("i do not know what to say, nothing", C.PAROLE_NO_WORDS)
    w, enemy = _struck_to_a_crewed_frigate()
    me = C.captive_person(w)
    w.run(120)
    pris = enemy.ship.extra["prisoners"]
    assert pris.parole.get(me.name) == "asked"
    for words in ("I cannot say yet.", "Yes and no.", "Yesterday I should have known."):
        w.submit(f"say to the captain: {words}")
        assert pris.parole.get(me.name) == "asked", words
    w.submit("say to the captain: Yes.")
    assert pris.parole.get(me.name) == "given"
    assert me.liberty == C.PLACES_ON_PAROLE and not enemy.captain.aside
    w.submit("say to the captain: No.")  # answered: nothing more is read
    assert pris.parole.get(me.name) == "given"
    # and the bare no, in another taking
    w2, enemy2 = _struck_to_a_crewed_frigate()
    me2 = C.captive_person(w2)
    w2.run(120)
    w2.submit("say to the captain: Non.")
    assert enemy2.ship.extra["prisoners"].parole.get(me2.name) == "refused"
    assert me2.liberty == C.PLACES_REFUSED


def test_an_answer_that_holds_a_negation_is_never_read_as_the_parole_given():
    """The lead's ruling of 2026-11-10: "I do not." and "you have it not" were read as given
    (the plain yes's "i do" and "you have it" with a negation after them), and "you shall not
    have my parole" by the form "my parole". An answer that holds a negation is never given,
    by the forms or the plain words; it is refused by the refused forms and the plain no
    alone, and otherwise the question stays open."""
    for words in (
        "I do not.",
        "I do not know",
        "I do not see why I should",
        "you have it not",
        "I don't give you my parole yet",
        "I can't say",
        "Je ne donne pas ma parole",
        "Yes and no.",
    ):
        assert C.read_parole(words) is None, words
    for words in (
        "you shall not have my parole",
        "No, I do not",
        "No.",
        "Never, sir",
        "I refuse",
        "I do not give it",
    ):
        assert C.read_parole(words) is False, words
    for words in (
        "I do.",
        "You have it, sir",
        "I give you my parole",
        "You have my word, lieutenant",
        "Oui",
    ):
        assert C.read_parole(words) is True, words
    # at the prompt: the question stays open through the negated yes, and the refusal is read
    w, enemy = _struck_to_a_crewed_frigate()
    me = C.captive_person(w)
    w.run(120)
    pris = enemy.ship.extra["prisoners"]
    assert pris.parole.get(me.name) == "asked"
    for words in ("I do not.", "You have it not.", "I do not know."):
        w.submit(f"say to the captain: {words}")
        assert pris.parole.get(me.name) == "asked", words
    w.submit("say to the captain: You shall not have my parole.")
    assert pris.parole.get(me.name) == "refused"
    assert me.liberty == C.PLACES_REFUSED


def test_a_prisoner_hails_nobody_and_his_prompt_performs_his_own_words_moves_and_needs_alone():
    """The owner's play, the fourth and fifth: the prisoner's 'hail her' was made by the
    trumpet from his captor's deck, and his 'go ashore' was refused in the free man's words
    ("bring her to an anchor"). A captive's prompt performs exactly: a word said, asked or
    told (`movement.CAPTIVE_STATION_VERBS`), a reading or a question his place allows, his
    body's moves within his parole (`CAPTIVE_VERBS`), his needs and a free line; every other
    order, the ones read before the vocabulary's among them (a hail, the colours, a signal,
    a standing order, a book, a station stood down, `captain: carry on`), is refused in the
    words that name his state, and nothing of it is done."""
    from freesail.world import movement as M

    assert M.CAPTIVE_VERBS == {"go to", "go below", "come on deck", "go aloft"}
    assert M.CAPTIVE_STATION_VERBS == {"say", "ask", "tell"}
    w, enemy = _struck_to_a_crewed_frigate()
    w.run(120)
    hails = len(_kinds(enemy.log, "hail.made")) + len(_kinds(w.players.log, "hail.answered"))
    for words in (
        "hail her",
        "hail the frigate: what ship is that?",
        "say to the Amazon: heave to",
        "strike the colours",
        "hoist the colours",
        "make the private signal",
        # package 98's step 7, met at the trunk: the flags of command are the deck's orders
        # by the place's check, so a prisoner is refused them by the same road as the colours
        "haul down the broad pendant",
        "haul down the second ensign",
        "haul down the jack",
        'standing order "mine": when the wind shifts then trim sails',
        "captain: carry on",
        "take a fix",
        "come to anchor",
        "beat to quarters",
        "set the courses",
        "heave to",
    ):
        out = w.submit(words)
        assert out.kind == "order.rejected", (words, out.kind, out.text)
        assert "You are a prisoner aboard the Medusa" in out.text, (words, out.text)
    for words in ("go ashore", "come aboard the Amazon"):
        out = w.submit(words)
        assert out.kind == "order.rejected" and "you leave her where her captain lands you" in (
            out.text
        ), (words, out.text)
        assert "anchor" not in out.text
    assert (
        len(_kinds(enemy.log, "hail.made")) + len(_kinds(w.players.log, "hail.answered")) == hails
    )
    assert not enemy.captain.aside
    # what he may: his words, a reading, his needs, and (his parole given) his moves
    assert w.submit("say to the captain: I give my parole").kind == "person.spoke"
    assert w.submit("where am I").kind == "query.reading"
    assert w.submit("how am i").kind != "order.rejected"
    assert w.submit("go to the deck").kind == "person.moved"
    assert w.submit("go below").kind == "person.moved"


def test_a_prizes_answer_to_a_hail_names_her_captors_ship_and_her_prize_master():
    """The owner's play, the fourth's other half: the prize answered "prize to Mr Ray's
    ship", naming whoever stood at the hailing prompt. A prize under her prize crew answers
    whose prize she is by her captor's ship ("prize to the Medusa") and her prize master by
    his own name, both from her record."""
    from freesail.world import hail as H

    w, enemy = _struck_to_a_crewed_frigate()
    prize = enemy.vessels.get(str(w.players.id))
    rec = P.record_of(prize)
    assert rec["captor_name"] == "Medusa" and rec["master"]
    said = H.answer_by_table(enemy, prize, "What ship is that?", w.players)
    assert said.startswith("The Amazon, prize to the Medusa, "), said
    assert "'s ship" not in said
    who = H.answer_by_table(enemy, prize, "Who commands her?", w.players)
    assert rec["master"] in who and "prize master" in who, who


@pytest.mark.slow
def test_a_far_body_that_takes_the_players_ship_is_made_a_hull_and_holds_him():
    """§3.1 and §4.3: a French frigate cruising for prizes at far detail (the cap nought)
    chases the player, who strikes; her brain enters `taking possession` (a struck mark is
    no superior force and no man of war to fear) and at hailing distance the far minute takes
    possession on the records: she is made a hull and woken as a dealing of the first rank,
    the player's person aboard her, the prompt hers."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    q = destination(w.position, 90.0, 0.5 * units.NAUTICAL_MILE)
    f = put(
        w,
        "frigate",
        "france",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Renard",
    )
    for _ in range(10):
        w.run(60)
        if f.brain.state in ("engaging", "chasing"):
            break
    assert f.brain.state in ("engaging", "chasing")
    assert w.submit("strike the colours").kind == "action.struck"
    for _ in range(15):
        w.run(60)
        if C.captive_of(w):
            break
    rec = C.captive_of(w)
    assert rec is not None and rec["captor"] == f.id
    assert any(state == "taking possession" for _, state in f.brain.history)
    hull = f.crew
    assert hull is not None and hull.awake and hull.shape == "full"
    assert w.hulls[f.id] is hull and f.dealing_tick >= 0  # a dealing of the first rank
    assert w.followed == f.id and w.own is hull
    assert "aboard the Renard, in the cabin, a prisoner" in w.submit("where am i").text
    assert P.record_of(w.vessels.own)["how"] == "struck at far detail"
    assert enemy_log_has(hull, "prize.captive")
    w.run(120)
    assert _kinds(hull.log, "prize.parole_asked")


def enemy_log_has(hull, kind: str) -> bool:
    return any(e.kind == kind for e in hull.log)


# -- the prisoners landed and the cartel -----------------------------------------------------------


@pytest.mark.slow
def test_the_prisoners_are_landed_to_the_agent_at_brest_and_a_cartel_brings_the_captive_home():
    """§3.3 and §3.4: the captor lying in Brest's road with the player taken comes to an
    anchor in port; the next minute her prisoners are landed to le commissaire des
    prisonniers with the list of their names, the captive ashore there, a prisoner of war,
    the prompt's orders refused as such; `cartel: a cartel from Brest for Captain Bowen`
    puts a cartel under a flag of truce on the sea at the road, who takes him off within hail
    (he is held nowhere now: refused for a person nobody holds) ... the form's doubt beyond
    a day's sail."""
    from freesail.world import orders as WO

    w, enemy = _struck_to_a_crewed_frigate(position=BREST_ROAD, her_goal=OFF_BREST)
    # her captain's own hand (the rule's actor): the followed prompt's "captain" is the
    # captive's from the taking
    out = enemy.captain.give("come to an anchor", why="the prisoners landed")
    assert out.kind != "order.rejected", out.text
    for _ in range(10):
        w.run(60)
        if enemy.dealings.in_port() is not None:
            break
    assert enemy.dealings.in_port() is not None and enemy.dealings.in_port().id == "brest"
    for _ in range(3):
        w.run(60)
        if _kinds(enemy.log, "prize.prisoners_landed"):
            break
    landed = _kinds(enemy.log, "prize.prisoners_landed")
    assert len(landed) == 1 and "le commissaire des prisonniers at Brest" in landed[0].text
    assert "Captain Bowen ashore there, prisoners of war" in landed[0].text
    me = C.captive_person(w)
    assert me is not None and not me.aboard and me.where == "shore" and me.port == "brest"
    assert me.ashore_at == "agent_for_prisoners" and not me.confined_to
    assert C.captive_of(w)["ashore"] == "brest"
    said = w.submit("where am i").text
    assert "ashore at Brest, at the agent for prisoners" in said
    out = w.submit("steer west")
    assert out.kind == "order.rejected" and "a prisoner of war ashore at Brest" in out.text
    assert P.prisoners_of(enemy.ship).count == 0
    # a cartel for a person nobody holds is refused; one from a port beyond a day's sail
    # is doubted
    e = w.world_order("cartel: a cartel from Brest for Captain Bowen", "the test")
    assert e.data.get("result") != "done" and "Nobody holds" in e.text
    # the cartel's road: a second scene with the captive aboard her still
    w2, enemy2 = _struck_to_a_crewed_frigate(position=BREST_ROAD, her_goal=OFF_BREST)
    doubt = WO.doubt(w2, WO.parse("cartel: a cartel from Falmouth for Captain Bowen"))
    assert doubt is not None and "beyond a day's sail" in doubt
    e = w2.world_order("cartel: a cartel from Brest for Captain Bowen", "the test")
    assert e.data.get("result") == "done", e.text
    cartel = w2.vessels.get(e.data["cartel"])
    assert cartel is not None and cartel.role == C.CARTEL_ROLE
    assert cartel.signals.colours.state == "truce"
    assert cartel.signals.colours.words(w2.nations) == "a flag of truce"
    assert cartel.signals.colours.shown_nation == "" and cartel.nation == "france"
    for _ in range(90):
        w2.run(60)
        if cartel.done:
            break
    taken = _kinds(enemy2.log, "prize.cartel")
    assert len(taken) == 1 and "takes off Captain Bowen by the boat" in taken[0].text
    assert cartel.done and _kinds(enemy2.log, "prize.cartel_landed")
    me2 = w2.players.people.find("Captain Bowen")
    assert me2 is not None and me2.where == "shore" and me2.port == "brest" and not me2.cartel
    assert C.captive_of(w2) is None
