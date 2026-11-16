"""The director's limits (package 115, part C; the cold review of 2026-11-14, decision 14
and 5.6; the owner's ruling of 2026-11-14): the director is free by default, the player's
own ship, person and prompt included; a brief's limits are real when a brief sets them, and
then they hold by every spelling, because they are judged on what the channel says an order
is (`freesail.world.orders.judged`, the one table of the forms) and never on its words; a
weight a limit cannot rank is refused; and the director's log holds every act that reached
the player's ship, his person or his prompt, in words that say whom it reached.

**Every test here comes in by the director's own door**: the `world_order` tool of a
director seated at the station (`freesail.agents.tools.world_order`), which is what a model
calls, or the player's line at the director's seat. The cold review's two probes
(`docs/reviews/ColdReview-M7-evidence/probes/director-*.py`) are among them. The director
is the scripted fake, and the identities are made up."""

from __future__ import annotations

from typing import Any

from freesail.agents import consent
from freesail.agents import director as D
from freesail.agents import tools as T
from freesail.agents.agent import DIRECTOR
from freesail.core.world import World
from freesail.world import orders as WO
from freesail.world import prizes as P
from tests.test_crews import hove_to_world
from tests.test_director import directed, log_kinds, log_texts, seat_director

# A brief that sets no limit at all (the owner's `director: brief <words>` is such a one).
FREE = {"name": "A free hand", "tone": "whatever the story needs"}
HANDS_OFF = {"name": "Hands off", "tone": "the sea alone", "limits": {D.HANDS_OFF: True}}
NOBODY_DIES = {"name": "Nobody dies", "tone": "a hard cruise", "limits": {"nobody_dies": True}}

LARK = 'ship: a cutter "Lark" of Britain at 49 31 N 5 31 W, bound for Plymouth'
ENDS = (
    "Done:",
    "Doubted, not performed:",
    "Refused",
    "The game has no way to do this as said:",
    "Logged as attempted, not performed:",
    "Following ",
    "Said to the player",
    "The day's budget",
)


def at_the_door(brief: Any, ticks: int = 120) -> tuple[World, Any]:
    """The frigate at seed 7 off the Lizard under `brief`, the player at her prompt having
    set plain sail and steered west, and a director seated at the station: (the world, the
    door: the director's own `world_order` tool, which answers in words)."""
    w = directed(brief)
    w.submit("steer west")
    for _ in range(ticks):
        w.tick()
    h = seat_director(w, [])

    def door(text: str, dry_run: Any = None) -> str:
        return T.world_order(h.world, DIRECTOR, text, dry_run=dry_run)

    return w, door


def entered(door: Any, text: str, reason: str = "the story wants it") -> str:
    """An order entered at the door, and entered again with a reason where it is doubted."""
    said = door(text)
    if said.startswith("Doubted"):
        said = door(f"{text} [reason: {reason}]")
    return said


def captain_of(w: World) -> Any:
    return w.people.captain


# The spellings by which the cold review walked round a limit (its decision 14, `spec-05`,
# `code-05b`, `refute-06`), each an act that reaches the player's own ship, his person or his
# prompt: (what it is, the order with `{cap}` for her captain's name).
REACHING = (
    ("her rules captain given an intent", "captain: intent bound for Plymouth"),
    ("the same without the word", "captain: bound for Plymouth"),
    ("her intent by her own name", 'ship "Amazon": intent bound for Plymouth'),
    ("her goal by her own name", 'ship "Amazon": bound for Plymouth'),
    ("a thing found aboard her", "aboard: a cask found stove"),
    ("the same with her name at the head", "aboard the Amazon: a cask found stove"),
    ("the same with her name quoted", 'aboard "Amazon": a cask found stove'),
    ("her captain hurt", "aboard: {cap} is hurt"),
    ("her captain hurt, her name at the head", "aboard the Amazon: {cap} is hurt"),
    ("a thing made on her cabin table", "aboard: a sealed packet, on the cabin table"),
    ("a sum paid into her purse", "aboard: twenty guineas paid into the purse by Mr Veale"),
    (
        "a person made aboard her",
        'person: make "Mr Gill", a merchant of forty, aboard in the cabin',
    ),
    ("words in the mouth of one of her people", 'say as the first lieutenant: "A sail, sir."'),
    ("the drivers moved", 'follow "the ship"'),
)

# What comes to her from outside by what she models: never hers to refuse.
FROM_OUTSIDE = (
    'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth',
    'message: at Brest from the agent: "The tin will fetch its price."',
    "port brest: closed to Denmark",
    "mark: a wreck, her masts showing at 49 00 N 6 20 W",
    'person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Brest',
)


# ---------------------------------------------------------------------------
# Free by default
# ---------------------------------------------------------------------------


def test_under_a_brief_with_no_limits_every_act_that_reaches_the_players_ship_is_done():
    """The owner's ruling: the director is free by default, the player's own ship, person
    and prompt included. Under a brief that sets no limit each of the review's spellings is
    performed (a doubt answered with a reason), and nothing refuses the director for being
    the director."""
    for what, form in REACHING:
        w, door = at_the_door(FREE)
        said = entered(door, form.format(cap=captain_of(w).name))
        assert said.startswith(("Done:", "Following the Amazon")), (what, said)
        assert "director.refused" not in log_kinds(w), what


def test_with_no_limits_the_review_s_two_probes_do_what_they_did():
    """The cold review's probes, through the director's door under a brief with no limits:
    her captain is dangerously wounded, a cutter is put beside her, and she strikes to the
    cutter, her people prisoners and the player carried aboard his captor."""
    w, door = at_the_door(FREE)
    cap = captain_of(w).name
    assert entered(door, f"aboard: {cap} is badly hurt").startswith("Done:")
    assert "wounded" in log_texts(w)[-1] and "dangerously" in log_texts(w)[-1]
    assert entered(door, LARK).startswith("Done:")
    said = entered(door, 'ship "the ship": struck to the Lark')
    assert said.startswith("Done: Amazon struck to Lark") and "prisoners" in said
    assert P.is_prize(w.vessels.own)  # her people prisoners, a prize crew aboard her
    # and the captain's intent turns her from west under the player's hand
    w, door = at_the_door(FREE)
    assert door("captain: intent bound for Plymouth").startswith("Done: the captain's intent")
    assert w.captain.intent is not None and "Plymouth" in w.captain.intent.words


# ---------------------------------------------------------------------------
# Hands off the player's own ship
# ---------------------------------------------------------------------------


def test_hands_off_refuses_every_spelling_that_reaches_her_and_nothing_is_done():
    """A brief that sets `hands_off_the_players_ship`: each of the review's spellings is
    refused in words that name the limit and whom the order reaches, at the first entry and
    again with a reason; nothing of the ship is changed, no act is spent, and the log keeps
    the refusal."""
    for what, form in REACHING:
        w, door = at_the_door(HANDS_OFF)
        text = form.format(cap=captain_of(w).name)
        before = (w.captain.intent, len(w.people.all), w.vessels.own.goal, w.followed)
        for said in (door(text), door(f"{text} [reason: the story wants it]")):
            assert said.startswith("Refused, outside the brief:"), (what, said)
            assert "hands off the player's own ship" in said and "reaches the player's" in said
        assert before == (w.captain.intent, len(w.people.all), w.vessels.own.goal, w.followed)
        assert D.budget_of(w).acts == 0 and log_kinds(w)[-1] == "director.refused", what
        assert door(text, dry_run=True).startswith(
            "Dry run, nothing performed and no act spent: it would be refused, outside the brief"
        ), what


def test_hands_off_refuses_the_review_s_probes_the_wound_the_strike_and_the_prize():
    """The review's probes under hands-off: the wound (four words of it, three heads), the
    strike and the prize are refused; the cutter, which comes to her from outside, is put
    on the sea."""
    w, door = at_the_door(HANDS_OFF)
    cap = captain_of(w).name
    for head in ("aboard:", "aboard the Amazon:", 'aboard "Amazon":'):
        for words in ("is badly hurt", "badly hurt", "is dangerously hurt", "is badly wounded"):
            said = door(f"{head} {cap} {words} [reason: the story]")
            assert said.startswith("Refused, outside the brief:"), (head, words, said)
            assert "the player's own person" in said
    assert entered(door, LARK).startswith("Done:")
    for taken in (
        'ship "the ship": struck to the Lark',
        'ship "Amazon": struck to the Lark',
        'ship "the ship": a prize of the Lark',
        'ship "Amazon": a prize of Lark',
    ):
        said = door(f"{taken} [reason: the story wants a captivity]")
        assert said.startswith("Refused, outside the brief:") and "the player's prompt" in said
    assert not P.is_prize(w.vessels.own) and not getattr(captain_of(w), "confined_to", "")
    # her own ship the captor is done to her too: a prize crew is taken out of her people
    assert door('ship "Lark": struck to the Amazon [reason: x]').startswith("Refused, outside")


def test_hands_off_does_not_refuse_what_comes_to_her_from_outside():
    """The weather, a sail, a letter left at a port, a port's stance, a mark and a person
    made ashore are the world's, not hers: done under hands-off as under any brief."""
    w, door = at_the_door(HANDS_OFF)
    for form in FROM_OUTSIDE:
        assert entered(door, form).startswith("Done:"), form
    # and another ship's own affairs are hers, not the player's
    assert entered(door, 'ship "Nancy": intent bound for Plymouth').startswith("Done:")
    assert entered(door, 'ship "Nancy": running home to Falmouth').startswith("Done:")
    assert "director.refused" not in log_kinds(w)


def test_hands_off_refuses_the_drivers_moved_to_another_ship_and_back():
    """`follow` is the player's prompt: under hands-off it is refused like the rest (and
    still costs no act where it is allowed)."""
    w, door = at_the_door(HANDS_OFF)
    assert entered(door, LARK).startswith("Done:")
    assert entered(door, 'ship "Lark": intent bound for Plymouth').startswith("Done:")
    acts = D.budget_of(w).acts
    said = door('follow "Lark"')
    assert said.startswith("Refused, outside the brief:") and "the player's prompt" in said
    assert w.ship.name == "Amazon" and D.budget_of(w).acts == acts
    w, door = at_the_door(FREE)
    entered(door, LARK)
    entered(door, 'ship "Lark": intent bound for Plymouth')
    acts = D.budget_of(w).acts
    assert door('follow "Lark"') == "Following the Lark."
    assert w.ship.name == "Lark" and D.budget_of(w).acts == acts  # a driver's line, no act
    # the ship his prompt is aboard is his while he is aboard her
    w.director_brief = D.resolve_brief(HANDS_OFF)
    said = door('ship "Lark": intent bound for Falmouth')
    assert (
        said.startswith("Refused, outside the brief:") and "the ship the player is aboard" in said
    )


# ---------------------------------------------------------------------------
# Nobody dies
# ---------------------------------------------------------------------------


def test_nobody_dies_refuses_the_grave_wound_by_every_word_and_every_head():
    """`nobody_dies` has something to refuse: a person badly hurt (three in ten die of a
    grave wound treated, six in ten not), by each of the table's words for it and with or
    without her name at the order's head, her captain or another of her people; a light
    hurt, which kills nobody, is done."""
    w, door = at_the_door(NOBODY_DIES)
    cap = captain_of(w).name
    for who in (cap, "the first lieutenant"):
        for head in ("aboard:", "aboard the Amazon:", 'aboard "Amazon":'):
            for words in ("is badly hurt", "badly hurt", "is dangerously hurt", "is badly wounded"):
                for tail in ("", " [reason: the story]"):
                    said = door(f"{head} {who} {words}{tail}")
                    assert said.startswith("Refused, outside the brief:"), (head, who, words)
                    assert "nobody dies" in said and "a thing that kills" in said
    crew = w.ship.extra["crew"]
    assert not [s for s in crew.sailors if s.hurt]
    assert entered(door, "aboard the Amazon: the first lieutenant is hurt").startswith("Done:")
    assert [s.wound for s in crew.sailors if s.hurt] == ["light"]


def test_every_shipped_brief_now_refuses_the_grave_wound():
    """Each starter brief sets `nobody_dies`, and each now refuses what it let through: the
    review's wound of the player's own captain, under the gentlest brief and the hardest."""
    for name in D.starter_briefs():
        w, door = at_the_door(name)
        said = door(f"aboard the Amazon: {captain_of(w).name} is badly hurt [reason: the story]")
        assert said.startswith("Refused, outside the brief:") and "nobody dies" in said, name
        assert "nobody dies by your hand" in D.brief_of(w).limits_words()


def test_nobody_dies_refuses_the_boat_lost_only_while_anyone_is_in_her():
    """The boat stove, swamped or gone adrift kills whoever is in her (`boats.lose_boat`):
    refused under `nobody_dies` while she is manned, by any head; with nobody in her she is
    a boat lost and no more, and it is done."""
    from freesail.world.boats import manned_hull

    w, door = at_the_door(NOBODY_DIES)
    assert manned_hull(w, w.own) is None
    assert entered(door, "aboard the Amazon: the boat gone adrift").startswith("Done:")
    w = hove_to_world()
    D.set_brief(w, NOBODY_DIES, source="the test")
    h = seat_director(w, [])

    def door(text: str) -> str:
        return T.world_order(h.world, DIRECTOR, text)

    frigate = w.players
    e = w.submit("go to the launch")  # the player's own person down into her boat
    assert e.kind == "person.aboard", e.text
    assert manned_hull(w, frigate) is not None and captain_of(frigate).hull == w.own.id
    for lost in ("the boat swamped", "the boat stove", "the boat gone adrift"):
        said = door(f"aboard the Amazon: {lost} [reason: a squall]")
        assert said.startswith("Refused, outside the brief:") and "nobody dies" in said, lost
    assert not captain_of(frigate).dead and manned_hull(w, frigate) is not None


def test_nobody_dies_does_not_refuse_a_hazard_the_ship_can_answer():
    """The lead's ruling of 2026-11-16: deadly is an act that kills of itself. A seam
    working, the water foul and a man taken ill are hazards the ship answers; they are not
    refused by `nobody_dies`, and the brief's own words say so."""
    w, door = at_the_door(NOBODY_DIES)
    for form in ("aboard: a seam found working", "aboard: the water found foul"):
        assert entered(door, form).startswith("Done:"), form
    words = D.brief_of(w).limits_words()
    assert "no act that kills of itself" in words and "is not refused by it" in words


# ---------------------------------------------------------------------------
# The weight of an enemy
# ---------------------------------------------------------------------------


def test_an_enemy_by_a_word_the_ranking_did_not_know_is_refused_as_heavier():
    """The review's `a line-of-battle ship` and `a 74` under "no enemy heavier than a
    cutter": weighed as the ship's maker reads them (a seventy-four) and refused."""
    w, door = at_the_door("quiet-passage")
    for desc in ("a line-of-battle ship", "a 74", "a seventy-four", "a ship of the line"):
        said = door(f'ship: {desc} "Brave" of France at 48 30 N 6 30 W, bound for Brest')
        assert said.startswith("Refused, outside the brief:"), (desc, said)
        assert "no enemy heavier than a cutter" in said and "is heavier" in said
        assert w.vessels.find("Brave") is None
    assert entered(
        door, 'ship: a cutter "Furet" of France at 48 30 N 6 30 W, bound for Brest'
    ).startswith("Done:")


def test_a_weight_the_limit_cannot_rank_is_refused_not_passed(monkeypatch):
    """A limit whose own word the ranking does not know weighs nothing, and so no enemy
    passes it; and an enemy of no class the ranking knows is refused under a limit that is
    set, in words that say what could not be ranked. A friend is not weighed at all."""
    brief = {"name": "Odd", "tone": "x", "limits": {"enemy_heaviest": "galleon"}}
    w, door = at_the_door(brief)
    said = door('ship: a cutter "Furet" of France at 48 30 N 6 30 W, bound for Brest')
    assert said.startswith("Refused, outside the brief:") and "'galleon' is no class" in said
    assert "refused, not passed" in said and w.vessels.find("Furet") is None
    assert entered(
        door, 'ship: a frigate "Medusa" of Britain at 48 30 N 6 30 W, bound for Plymouth'
    ).startswith("Done:")
    # an enemy the ranking cannot weigh, under a limit it can
    from freesail.world import captains

    real = captains.size_rank_of
    monkeypatch.setattr(
        captains, "size_rank_of", lambda words: None if "lugger" in str(words) else real(words)
    )
    w, door = at_the_door("quiet-passage")
    said = door('ship: a lugger "Furet" of France at 48 30 N 6 30 W, bound for Brest')
    assert said.startswith("Refused, outside the brief:"), said
    assert "of no class the ranking of a sail knows" in said and "refused, not passed" in said


def test_the_weight_is_judged_wherever_an_enemy_is_put_on_the_sea():
    """The lead's ruling: the weight is asked of a ship in ordinary commissioned as of a new
    ship. A French frigate laid up by the owner's order (the owner's are outside the brief)
    is not commissioned by a director whose brief allows nothing heavier than a cutter."""
    w, door = at_the_door("quiet-passage")
    w.world_order(
        'ship: a frigate "Vengeance" of France at 48 10 N 5 00 W, bound for Brest',
        source="the owner",
    )
    assert w.vessels.find("Vengeance") is not None  # the owner's order met no brief
    w.world_order('ship "Vengeance": in ordinary at Brest', source="the owner")
    assert w.vessels.find("Vengeance").regime == "in ordinary"
    said = door('ship "Vengeance": commissioned for cruise off the Lizard within 10 miles at once')
    assert said.startswith("Refused, outside the brief:"), said
    assert "no enemy heavier than a cutter" in said and "frigate of France is heavier" in said
    assert w.vessels.find("Vengeance").regime == "in ordinary"


# ---------------------------------------------------------------------------
# The owner's and the scenario's orders are outside the brief
# ---------------------------------------------------------------------------


def test_the_owners_world_order_meets_no_brief_and_no_doubt():
    """`world: <order>` is the owner's, and a scenario's are the scenario's: judged by the
    table for what they are, never by a brief's limits and never doubted."""
    w, door = at_the_door(HANDS_OFF)
    cap = captain_of(w).name
    e = w.world_order(f"aboard the Amazon: {cap} is hurt", source="the owner")
    assert e.data["result"] == "done" and "wounded" in e.text
    j = WO.judged(w, WO.parse("captain: intent bound for Plymouth"))
    assert j.form.key == "captain" and j.the_players
    e = w.world_order("captain: intent bound for Plymouth", source="the owner")
    assert e.data["result"] == "done" and "director.refused" not in log_kinds(w)


# ---------------------------------------------------------------------------
# The director's log
# ---------------------------------------------------------------------------


def test_the_directors_log_holds_every_act_that_reached_her_in_words_that_say_whom():
    """No line is said to the player; the director's log is where its acts are read. Each
    act given through the door that reached the player's ship, his person or his prompt is
    in the log as the player reads it (`the director's log`), saying whom it reached; an
    act that reached nobody of his says nothing of the kind."""
    w, door = at_the_door(FREE)
    cap = captain_of(w).name
    assert door("captain: intent bound for Plymouth").startswith("Done:")
    assert entered(door, f"aboard the Amazon: {cap} is hurt").startswith("Done:")
    assert entered(
        door, 'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth'
    )
    assert entered(door, LARK).startswith("Done:")
    assert entered(door, 'ship "Lark": intent bound for Plymouth').startswith("Done:")
    assert door('follow "Lark"') == "Following the Lark."
    assert door('follow "the ship"') == "Following the Amazon."
    assert entered(door, 'ship "the ship": struck to the Lark').startswith("Done:")
    lines = D.reveal(w, "the player")
    text = "\n".join(lines)

    def line(of: str) -> str:
        return next(x for x in lines if of in x)

    assert "it reached the player's own ship (the Amazon)" in line("Given: captain: intent")
    hurt = line(f"aboard the Amazon: {cap} is hurt;")
    assert f"it reached the player's own person ({cap}) and the player's own ship" in hurt
    assert "it reached" not in line('"Nancy"') and "it reached" not in line('ship "Lark": intent')
    assert "(follow)" in line("Following the Lark") and "it reached the player's prompt" in line(
        "Following the Lark"
    )
    assert "it reached the player's prompt" in line("Following the Amazon")
    struck = line('ship "the ship": struck to the Lark; the doubt')
    for whom in ("the player's own person", "the player's own ship", "the player's prompt"):
        assert whom in struck, whom
    assert text.count("it reached") == 5
    assert "director.follow" in D.KINDS


# ---------------------------------------------------------------------------
# Every form, given to the player's own ship, ends in words
# ---------------------------------------------------------------------------


def _hers(example: str) -> str:
    """A form's example turned on the player's own ship: her name for the other ship's."""
    for name in ("Harpy", "Medusa", "Nancy", "Lark"):
        example = example.replace(f'"{name}"', '"Amazon"').replace(f"the {name}", "the Amazon")
    return example


def test_every_form_given_to_the_players_own_ship_ends_done_doubted_or_refused(tmp_path):
    """An order that reaches the door ends in words, never in an error: every example of
    every form of the one table, turned on the player's own ship, under a brief with no
    limits, a starter and hands-off, entered and entered again with a reason. Among them the
    fault met on the way (`ship "<her>": in ordinary at ...`, which raised)."""
    for brief in (FREE, "quiet-passage", HANDS_OFF):
        w, door = at_the_door(brief, ticks=30)
        w.__dict__["saves_dir"] = str(tmp_path)
        for f in WO.WORLD_ORDER_FORMS:
            for x in f.examples:
                for text in (_hers(x), f"{_hers(x)} [reason: the story]"):
                    said = door(text)
                    assert said.startswith(ENDS), (brief, text, said)


def test_a_ship_in_commission_is_not_laid_up_in_ordinary_whoever_asks():
    """The fault met through the director's door: the player's own ship laid up in ordinary
    raised an error. It is refused by the game's own rule, in the game's words, to the
    director and to the owner alike: she is in commission, her people aboard."""
    w, door = at_the_door(FREE)
    said = door('ship "Amazon": in ordinary at Falmouth')
    assert said.startswith("The game has no way to do this as said: Amazon is in commission")
    assert "paid off" in said and log_kinds(w)[-1] == "director.unperformed"
    e = w.world_order('ship "Amazon": in ordinary at Falmouth', source="the owner")
    assert e.data["result"] == "refused" and "is in commission" in e.text
    assert w.vessels.own.regime != "in ordinary"


# ---------------------------------------------------------------------------
# The one table
# ---------------------------------------------------------------------------


def test_every_order_performed_names_its_form_of_the_one_table():
    """The channel reads what an order is where it performs it: every example of every form
    that this sea can perform is judged to be its own form, with a reach the form declares;
    and the table is the channel's, read by the director's module."""
    assert D.WORLD_ORDER_FORMS is WO.WORLD_ORDER_FORMS
    w, door = at_the_door(FREE, ticks=30)
    entered(door, 'ship: a brig-sloop "Harpy" of Britain at 49 00 N 6 20 W, bound for Falmouth')
    entered(door, 'ship: a frigate "Medusa" of Britain at 49 05 N 6 25 W, bound for Plymouth')
    judged = 0
    for f in WO.WORLD_ORDER_FORMS:
        assert set(f.reach) <= set(WO.REACHES) and f.harm in (
            WO.HARM_NONE,
            WO.HARM_HURT,
            WO.HARM_DEADLY,
            WO.HARM_BY_THE_THING,
        ), f.key
        for x in f.examples:
            j = WO.judged(w, WO.parse(x))
            if j is None:
                continue  # this sea cannot perform it as said: the channel's own refusal
            judged += 1
            assert j.form.key == f.key, (x, j.form.key)
            assert j.reaches <= set(f.reach), (x, sorted(j.reaches), f.reach)
    assert judged >= 60
    # judging performs nothing
    before = (w.clock.tick, len(w.log.all()), len(w.vessels.active()), len(w.people.all))
    WO.judged(w, WO.parse('ship: a cutter "Wasp" of Britain at 49 00 N 6 20 W, bound for Falmouth'))
    WO.judged(w, WO.parse("aboard: a cask found stove"))
    assert before == (w.clock.tick, len(w.log.all()), len(w.vessels.active()), len(w.people.all))


def test_the_dry_run_judges_on_a_copy_and_makes_no_hull_on_the_world():
    """The dry run reads the door's own sequence, and what it must make to judge (the hull
    of a far ship named at an order's head) it makes on its copy: the world is not touched."""
    w, door = at_the_door(FREE)
    entered(door, 'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth')
    assert w.vessels.find("Nancy").crew is None
    said = door("aboard the Nancy: a cask found stove", dry_run=True)
    assert said.startswith("Dry run, nothing performed and no act spent:")
    assert w.vessels.find("Nancy").crew is None and "nancy" not in " ".join(w.hulls).lower()


# ---------------------------------------------------------------------------
# The consent question is not put again by a station's brief
# ---------------------------------------------------------------------------


def test_a_change_to_the_directors_station_brief_puts_no_consent_question_again(monkeypatch):
    """The re-ask rule compares the consent brief's own sections and nothing else
    (`consent.changed_sections`): the director's station brief, changed by this package,
    is no part of what a consent record is compared with."""
    text = consent.brief_text("made-up-weights-7b", "a made-up runtime", "runner")
    record = consent.Record(
        date="2026-11-16",
        identity="made-up-weights-7b",
        runtime="a made-up runtime",
        verdict=consent.YES,
        brief=text,
    )
    record.path = consent.BRIEF_PATH  # a record on file, its brief kept as it was sent
    assert consent.changed_sections(record, "runner") == []
    monkeypatch.setattr(D, "DIRECTOR_BRIEF", D.DIRECTOR_BRIEF + " A sentence more.")
    monkeypatch.setattr(D, "SEAT_AND_CHANNEL_BRIEF", "Other words.")
    assert consent.changed_sections(record, "runner") == []
    assert "director" not in " ".join(consent.RE_ASK_SECTIONS).lower()
    assert D.DIRECTOR_BRIEF not in text and "You are the director" not in text
