"""The colours, the signal books, a signal hoisted and read, the private signal and the
hail (spec M7 §1 to §5; package 71; `docs/design/Design-Signals.md`)."""

from __future__ import annotations

import re

import pytest

from freesail import units
from freesail.world import hail as H
from freesail.world import signals as S
from freesail.world.nations import load_nations

# -- the books -----------------------------------------------------------------------------


def test_every_root_has_the_six_files_in_one_shape_and_the_nations_name_theirs():
    roots = S.roots()
    assert {"britain", "france", "basic"} <= set(roots)
    for root in roots:
        b = S.load_books(root)
        assert b.system in ("well-built", "basic")
        assert b.numerary and b.night and b.fog and b.convoy, root
        assert b.hoist_s == 60 and b.read_s == 60 and b.read_nm == 2.0
        for e in [*b.numerary, *b.convoy]:
            assert e.number is not None and e.meaning and e.source, (root, e.meaning)
            assert set(e.does) <= {"order", "state", "news", "answer", "closer", "release"}, e
        for e in [*b.night, *b.fog]:
            # 71's were all made; 76 read the British night book (1799) and fog book (1796)
            # and Audibert's French fog (1802) from the page: an entry is made, or its source
            # names the page's year
            assert e.show or e.fire, (root, e.meaning)
            assert e.made or re.search(r"\b1[78]\d\d\b", e.source), (root, e.meaning)
            if root == "britain" and not e.made:
                assert e.number is not None, e.meaning  # the British tables are numbered
    table = load_nations()
    for n in table.nations.values():
        assert S.books_for_nation(table, n.id).root == n.signals_root
    assert S.load_books("basic").telegraph is False
    assert S.load_books("france").telegraph is False


def test_the_british_book_keeps_the_numbers_remembered_and_marks_the_rest_made():
    b = S.load_books("britain")
    assert b.by_number(16).meaning == "Engage the enemy more closely" and not b.by_number(16).made
    assert b.by_number(72).meaning.startswith("Form the order of sailing in two columns")
    assert b.by_number(13).meaning == "Prepare for battle" and b.by_number(76).made is False
    made = [e for e in b.numerary if e.made]
    assert len(made) >= 100 and all("made" in e.source for e in made)
    e, q = b.find("tack in succession")
    assert e.number == 54 and e.in_succession and e.does == {"order": "put her about"}
    e, q = b.find("enemy in sight bearing NW")
    assert e.number == 1 and q["compass"] == "NW" and q["compass_deg"] == 315.0
    e, q = b.find("No. 16")
    assert e.number == 16 and e.does == {"closer": True}
    e, _ = b.find("to chase")
    assert e.does == {"state": "chasing"}
    assert b.find("the convoy to tack in succession", "convoy")[0].number == 5
    assert b.find("tack", "fog")[0].fire == "three guns, two quick and one slow"  # 1796, fog No. 8
    assert b.find("a sentence the book lacks") is None


def test_a_hoist_shows_its_books_form_and_the_british_numerary_is_unchanged_by_it():
    """Package 76: a book declares how its numbered signals are hoisted. The British numerary
    is a flag a figure (No. 186 three flags), as before the field, and its hoist's record
    carries no new key; du Pavillon's table (the French book) is two flags, the upper and the
    lower, whatever the cell's number (Audibert 1802, ch. IV § 71)."""
    gb = S.load_books("britain")
    assert gb.hoist_form == "numerary" and S.load_books("basic").hoist_form == "numerary"
    e, q = gb.find("No. 186")
    h = S.make_hoist(S.Locker(), gb, e, q, "harpy", 100)
    assert h.flags_words() == "three flags at the main" and "form" not in h.to_dict()
    e, q = gb.find("No. 16")
    assert S.make_hoist(S.Locker(), gb, e, q, "harpy", 100).flags_words() == "two flags at the main"
    fr = S.load_books("france")
    assert fr.hoist_form == "table"
    e, q = fr.find("general chase")
    h = S.make_hoist(S.Locker(), fr, e, q, "renard", 100)
    assert e.number < 10 and h.flags_words() == "two flags at the main"
    assert h.to_dict()["form"] == "table"


def test_the_spanish_book_is_added_by_data_alone_in_mazarredos_numbers():
    """Package 76: Spain's own root, the six files and the nations' line and nothing else.
    Mazarredo's plan (Cádiz 1781, the third edition): two flags read as a cell of four
    hundred, the cell's number the article (No. 247 the chase without keeping the order);
    the signals of one flag numbered above the table; by night the lanterns high and low of
    his nineteen, by fog the guns in two times a full minute apart."""
    from freesail.world.nations import load_nations

    assert load_nations().get("spain").signals_root == "spain"
    es = S.books_for_nation(load_nations(), "spain")
    assert es.nation == "spain" and es.hoist_form == "table" and not es.telegraph
    e, q = es.find("general chase")
    assert e.number == 247 and not e.made and e.original.startswith("Dar caza")
    h = S.make_hoist(S.Locker(), es, e, q, "santa-sabina", 100)
    assert h.flags_words() == "two flags at the main" and h.to_dict()["form"] == "table"
    assert es.find("man overboard")[0].number == 409
    assert es.find("engage the enemy more closely")[0].does == {"closer": True}
    night = {x.meaning: x for x in es.night}
    assert night["Wear together"].show == "two lanterns high and three lanterns low"
    third = "and then a rocket or the stern lanterns left lit"  # his chapter III, told after
    assert night["Tack in succession"].show.endswith(third)
    fog = {x.meaning: x for x in es.fog}
    assert fog["Shorten sail"].fire == "two guns"
    assert fog["Wear together"].fire == "two guns, and a full minute after three guns"
    assert all(not x.made for x in es.night + es.fog)
    # her private signal's draw is the one she drew on basic: the form kept word for word
    for month in (1, 6, 12):
        drawn = S.private_table(S.load_books("basic"), "spain", 1805, month, 7)
        assert S.private_table(es, "spain", 1805, month, 7) == drawn


def test_the_telegraphic_dictionary_spells_nelsons_sentence_in_twelve_hoists():
    b = S.load_books("britain")
    hoists = b.encode("England expects that every man will do his duty")
    assert [n for n, _ in hoists] == [253, 269, 863, 261, 471, 958, 220, 370, 4, 21, 19, 24]
    assert [w for _, w in hoists][-4:] == ["D", "U", "T", "Y"]
    with pytest.raises(S.BookFileError):
        S.load_books("france").encode("England expects")


def test_the_private_table_is_drawn_under_the_seed_by_nation_and_month():
    b = S.load_books("britain")
    t1 = S.private_table(b, "britain", 1805, 6, 7)
    assert t1 == S.private_table(b, "britain", 1805, 6, 7)
    assert t1.day_reply != S.private_table(b, "britain", 1805, 7, 7).day_reply
    assert t1.day_challenge != S.private_table(b, "britain", 1805, 6, 8).day_challenge
    spain = S.private_table(S.load_books("basic"), "spain", 1805, 6, 7)
    dutch = S.private_table(S.load_books("basic"), "batavian-republic", 1805, 6, 7)
    assert spain.day_challenge != dutch.day_challenge
    assert "one lights" not in t1.night_challenge + t1.night_reply
    assert t1.lines()[0].startswith("The private signals for June 1805")
    wrong = S.wrong_reply(b, "france", 1805, 6, 7, "day")
    assert wrong != t1.day_reply


# -- the colours -----------------------------------------------------------------------------


def test_colours_are_a_state_and_the_lookout_reads_the_nation_shown():
    nations = load_nations()
    c = S.Colours()
    S.set_colours(c, nations, "shown", "france", 0)
    assert c.words(nations) == "French colours, the tricolour" and c.shows
    S.set_colours(c, nations, "false", "britain", 10)
    assert c.words(None) == "British colours, the red ensign" and c.shown_nation == "britain"
    S.set_colours(c, nations, "none", "", 20)
    assert not c.shows and c.words(nations) == "a stranger, her colours not made out"
    S.set_colours(c, nations, "distress", "france", 30)
    assert c.words(nations).endswith("the ensign union down")
    S.set_colours(c, nations, "struck", "", 40)
    assert c.words(nations) == "her colours struck"
    with pytest.raises(ValueError):
        S.set_colours(c, nations, "purple", "", 0)


def test_a_far_vessel_under_false_colours_is_made_out_as_the_nation_she_shows():
    from tests.test_brains import put, world_at

    w = world_at(49.5, -5.5)
    v = put(w, "cutter", "france", "49 29 N 5 30 W", "bound for Brest", colours="British")
    assert v.nation == "france" and v.nation_shown == "britain"
    assert v.colours_words() == "British colours, the red ensign"
    w.run(120)
    strangers = w.readings.value("strangers")
    item = next(i for i in strangers["items"] if i["id"] == v.id)
    assert item["nation"] == "britain"  # the ruse works on the reading, the truth is hers
    far = w.vessels.strangers_of(w, v, set())
    assert far  # she sees the frigate; the frigate's shadow shows her own
    with pytest.raises(ValueError):
        put(w, "cutter", "france", "49 20 N 5 30 W", "bound for Brest", colours="Ruritanian")


# -- a signal hoisted and read ---------------------------------------------------------------


def _reader() -> tuple[S.Locker, S.Books]:
    return S.Locker(), S.load_books("britain")


def test_a_hoist_is_seen_at_the_flags_range_and_read_a_minute_later_by_the_books_holder():
    sender = S.Locker()
    books = S.load_books("britain")
    entry, q = books.find("tack in succession")
    h = S.make_hoist(sender, books, entry, q, "harpy", 100)
    assert h.breaks_out == 160 and not h.flying(150) and h.flying(160)
    reader, rbooks = _reader()
    # beyond the flags' range: nothing; within it: seen, then read a minute later
    far = S.read_flying(
        reader,
        rbooks,
        "harpy",
        "the brig",
        [h],
        4.0 * units.NAUTICAL_MILE,
        "day",
        False,
        170,
        "nancy",
    )
    assert far == []
    seen = S.read_flying(
        reader,
        rbooks,
        "harpy",
        "the brig",
        [h],
        1.0 * units.NAUTICAL_MILE,
        "day",
        False,
        170,
        "nancy",
    )
    assert [x.kind for x in seen] == ["signal.seen"] and "two flags at the main" in seen[0].text
    nothing = S.read_flying(
        reader,
        rbooks,
        "harpy",
        "the brig",
        [h],
        1.0 * units.NAUTICAL_MILE,
        "day",
        False,
        200,
        "nancy",
    )
    assert nothing == []
    read = S.read_flying(
        reader,
        rbooks,
        "harpy",
        "the brig",
        [h],
        1.0 * units.NAUTICAL_MILE,
        "day",
        False,
        230,
        "nancy",
    )
    assert [x.kind for x in read] == ["signal.read"]
    assert read[0].text == "The brig's signal is No. 54, tack in succession."
    # a French reader has not the book
    french = S.Locker()
    seen = S.read_flying(
        french,
        S.load_books("france"),
        "harpy",
        "the brig",
        [h],
        1.0 * units.NAUTICAL_MILE,
        "day",
        False,
        170,
        "renard",
    )
    assert "a signal we cannot read: not of our book" in seen[0].text
    assert (
        S.read_flying(
            french,
            S.load_books("france"),
            "harpy",
            "the brig",
            [h],
            1.0 * units.NAUTICAL_MILE,
            "day",
            False,
            300,
            "renard",
        )
        == []
    )
    # the glass reaches further; the fog's gun is heard at three miles
    glass = S.read_flying(
        S.Locker(),
        rbooks,
        "harpy",
        "the brig",
        [h],
        2.8 * units.NAUTICAL_MILE,
        "day",
        True,
        170,
        "x",
    )
    assert glass and glass[0].kind == "signal.seen"
    gun_entry, _ = books.find("tack", "fog")
    gun = S.make_hoist(S.Locker(), books, gun_entry, {}, "harpy", 100, at_once=True)
    heard = S.read_flying(
        S.Locker(),
        rbooks,
        "harpy",
        "the brig",
        [gun],
        2.5 * units.NAUTICAL_MILE,
        "fog",
        False,
        100,
        "x",
    )
    assert (
        heard[0].kind == "signal.read"
        and heard[0].text == "The brig fires three guns, two quick and one slow: to tack."
    )
    sender.tidy(100 + 60 + 1800, books.flies_s)
    assert h.down is not None


def test_the_orders_map_to_what_a_commanded_captain_does():
    books = S.load_books("britain")
    e, q = books.find("steer NW")
    h = S.make_hoist(S.Locker(), books, e, q, "x", 0)
    assert S.order_of(h) == "steer NW"
    e, q = books.find("steer")
    assert S.order_of(S.make_hoist(S.Locker(), books, e, q, "x", 0)) is None  # no compass given
    e, q = books.find("make all sail")
    assert S.order_of(S.make_hoist(S.Locker(), books, e, q, "x", 0)) == "make all sail"


# -- the hail's tables --------------------------------------------------------------------------


def test_the_hail_reads_its_questions_and_the_nation_in_an_answer():
    assert H.questions_in("What ship is that?") == ["what ship"]
    assert H.questions_in("Whence come you, and whither bound? What cargo?") == [
        "whence",
        "whither",
        "cargo",
    ]
    assert H.questions_in("Heave to, I am sending a boat") == ["heave to"]
    assert H.questions_in("Good morning") == ["what ship"]
    nations = load_nations()
    assert (
        H.nation_in_words(nations, "His Majesty's cutter Sherbourne. And what ship is that?")
        == "britain"
    )
    assert (
        H.nation_in_words(nations, "The Nancy of Guernsey, from Guernsey for Falmouth, in ballast.")
        == "britain"
    )
    assert H.nation_in_words(nations, "the French national brig Harpy") == "france"
    assert H.nation_in_words(nations, "The Vrouw Maria of Amsterdam") == "batavian-republic"
    assert H.nation_in_words(nations, "Good day to you") is None
    assert H.standard_hail("merchant") == "What ship is that, and whither bound?"


def test_a_privateer_under_false_colours_lies_by_the_table_and_a_kings_ship_names_herself():
    from tests.test_brains import put, world_at

    w = world_at(49.5, -5.5)
    renard = put(
        w,
        "cutter",
        "france",
        "49 29 N 5 30 W",
        "cruising off the Lizard within 10 miles",
        intent="cruise for prizes off the Lizard within 10 miles",
        colours="British",
        name="Renard",
    )
    lie = H.answer_by_table(w, renard, "What ship is that?")
    assert "Renard" not in lie and lie.startswith("The ") and " of " in lie
    assert H.nation_in_words(w.nations, lie) == "britain"
    S.set_colours(S.vessel_locker(renard).colours, w.nations, "shown", "france", 0)
    truth = H.answer_by_table(w, renard, "What ship is that?")
    assert truth.startswith("The privateer Renard of ")
    harpy = put(
        w,
        "brig-sloop",
        "britain",
        "49 20 N 5 30 W",
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Harpy",
    )
    assert H.answer_by_table(w, harpy, "what ship is that").startswith("His Majesty's sloop Harpy")
    assert H.answer_by_table(w, harpy, "heave to, I am sending a boat") == (
        "A King's ship heaves to for nobody: stand on."
    )
    nancy = put(
        w,
        "merchant brig",
        "britain",
        "49 25 N 5 25 W",
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Nancy",
    )
    answer = H.answer_by_table(w, nancy, "What ship, whence and whither?")
    assert answer.startswith("The Nancy of ") and "for Falmouth" in answer


def test_a_hail_of_the_players_ship_waits_for_the_player_and_moves_no_sail():
    """The playtest of 2026-10-27: the frigate with her armed tender, a model at the
    cutter's captain's station. Every hail the cutter made was answered for the player's
    ship by table, and her rules-based captain made all sail, "hailed to heave to; she will
    not", whatever the words: `model_holds_her` called `Captain.commands` (a property) as a
    method, and the heave-to was worked on every hail, not only on the demand. The player's
    ship with no rules captain commanding hears the hail and keeps it for his `say to her`;
    a ship answering by table moves her sail only when she is asked to heave to."""
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    assert not w.captain.commands  # the player commands her: no intent, no rules captain
    raven = put(
        w,
        "cutter",
        "britain",
        "49 30.2 N 5 30 W",
        "in company with the ship",
        intent="patrol off the Lizard within 5 miles",
        name="Raven",
    )
    w.run(61)
    crew = raven.crew
    assert crew is not None and crew.shape == "full"
    assert H.model_holds_her(w)
    shadow = w.vessels.player_shadow(w)
    n = len(w.log)
    assert H.deliver(crew, shadow, "We are well, how are you?", int(crew.clock.tick)) is None
    new = list(w.log)[n:]
    assert [e.kind for e in new] == ["hail.heard"]
    assert w.ship.extra["hail_pending"]["words"] == "We are well, how are you?"
    # a ship her rules captain commands answers by table: an enemy merchantman hailed with
    # a question that is no demand moves no sail; the demand itself she runs from
    w2 = hove_to_world()
    nancy = put(
        w2,
        "merchant brig",
        "france",
        "49 30.2 N 5 30 W",
        "bound for Brest",
        intent="bound for Brest",
        name="Nancy",
    )
    w2.run(61)
    assert nancy.crew is not None and nancy.crew.shape == "full"
    assert nancy.crew.captain.commands and not H.model_holds_her(nancy.crew)

    def hailed(words: str) -> list[str]:
        n2 = len(nancy.crew.log)
        assert H.deliver(w2, nancy, words, int(w2.clock.tick))
        return [e.text for e in list(nancy.crew.log)[n2:] if "making all sail" in e.text]

    assert hailed("What news?") == []
    assert hailed("Heave to, I am sending a boat") != []


def test_a_crewed_ship_under_the_directors_hand_or_standing_aside_is_still_answered_by_table():
    """Package 86's fold-in (the review of the owner's local work, section 3): the hail
    fix's `commands` branch is the player's ship's alone. A crewed ship whose rules captain
    holds by the director's hand (`over_his_head`) or stands aside commands nothing, and no
    model holds her: the table answers her hail as it did, where the owner's fix had left it
    pending with nobody to answer. The player's ship with her captain aside still waits for
    the player."""
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    nancy = put(
        w,
        "merchant brig",
        "britain",
        "49 30.2 N 5 30 W",
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Nancy",
    )
    w.run(61)
    crew = nancy.crew
    assert crew is not None and crew.shape == "full"
    cap = crew.captain
    cap.over_his_head("heave to", until=int(w.clock.tick) + 3600)
    assert not cap.commands and not H.model_holds_her(crew)
    answer = H.deliver(w, nancy, "What ship is that?", int(w.clock.tick))
    assert answer and answer.startswith("The Nancy of ")
    assert "hail_pending" not in crew.ship.extra
    cap.take_up_again()
    cap.aside = True
    assert not cap.commands and not H.model_holds_her(crew)
    assert H.deliver(w, nancy, "What ship is that?", int(w.clock.tick)).startswith("The Nancy")
    # the player's own ship, her rules captain standing aside: the hail waits for him
    w.captain.aside = True
    assert H.model_holds_her(w)


# -- the hail's colon optional ---------------------------------------------------------------


def test_the_hail_names_the_sail_with_or_without_the_colon():
    """The voice in one grammar: `hail the brig what ship is that?` and `say to the Nancy
    heave to, I am sending a boat` are the hail of chapter 23 with the colon left out,
    the sail told from the words by her rig, her name or 'her'; with the colon the sail
    is what stands before it as before. The lookout's hail of the deck ('hail sail ho',
    'hail the deck sail ho') and a word to a station ('say to the watcher all is well')
    are not hails of a sail, a capitalised 'Sail ho' included."""
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    put(
        w,
        "merchant brig",
        "france",
        "49 30.2 N 5 30 W",
        "bound for Brest",
        intent="bound for Brest",
        name="Nancy",
    )
    w.run(61)
    for words, said in (
        ("hail the brig: what ship is that?", "what ship is that?"),
        ("hail the brig what ship is that?", "what ship is that?"),
        ("hail the merchant brig whence come you", "whence come you"),
        ("hail her what ship is that", "what ship is that"),
        ("say to her, heave to", "heave to"),
        ("say to the brig heave to", "heave to"),
        ("say to the Nancy heave to, I am sending a boat", "heave to, I am sending a boat"),
        ("hail Nancy what ship is that", "what ship is that"),
    ):
        e = w.submit(words)
        assert e.kind == "hail.answered", (words, e.text)
        assert f"by the trumpet: '{said}'" in e.text, (words, e.text)
    assert w.submit("hail the brig").text.startswith(
        "Hailed a merchant brig by the trumpet: 'What ship is that?'"
    )
    for words in ("hail the deck sail ho", "hail Sail ho, two points on the bow"):
        e = w.submit(words)
        assert e.kind == "order.rejected" and "A hail is the lookout's" in e.text, words
    assert w.submit("say to the watcher all is well").kind == "agent.told"
    e = w.submit("hail the cutter what ship")
    assert e.kind == "order.rejected" and "Nothing in sight answers to 'the cutter'" in e.text
    # the head never crosses a colon or a comma (the lead's finding at the review of
    # items 1 and 2): a word to a station that names a sail after the colon is the
    # station's, and the lookout's hail of the deck that names one is his
    for words in ("say to the master: the brig has tacked", "say to the lookout: watch the brig"):
        assert w.submit(words).kind == "agent.told", words
    for words in (
        "hail the deck: a sail two points on the bow",
        "hail the deck: the brig is bearing away",
    ):
        e = w.submit(words)
        assert e.kind == "order.rejected" and "A hail is the lookout's" in e.text, words


# -- the hail as it is typed, and answered (the owner's second test, 2026-10-31) ----------------


def test_the_hail_is_read_in_any_capitals_by_her_rate_and_with_her_article():
    """`Hail the schooner` was refused as the lookout's eleven times while `hail the schooner`
    was taken, `hail a topsail schooner` was refused though the log calls her so, and the line
    in quotes too. The verb in any capitals, the sail by her rate as well as her rig, and by
    'a'; the lookout's own words stay his, whatever is in sight."""
    from freesail.agents.seat import seat_player
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    put(
        w,
        "merchant brig",
        "france",
        "49 30.2 N 5 30 W",
        "bound for Brest",
        intent="bound for Brest",
        name="Nancy",
    )
    w.run(61)
    for words in (
        "Hail the brig: whence come you",
        "Hail the brig whence come you",
        "HAIL HER whence come you",
        "Say to her, whence come you",
        "Say to the Nancy whence come you",
        "hail a merchant brig: whence come you",
        "hail a merchant brig whence come you",
        '"hail the brig: whence come you"',
    ):
        e = w.submit(words)
        assert e.kind == "hail.answered", (words, e.text)
        assert "by the trumpet: 'whence come you'" in e.text, (words, e.text)
    # no sail named: the lookout's, as before, and the refusal says how a sail is hailed
    for words in ("Hail Sail ho, two points on the bow", "hail a sail two points on the bow"):
        e = w.submit(words)
        assert e.kind == "order.rejected" and "A hail is the lookout's" in e.text, words
        assert "'hail the <sail>: <words>'" in e.text, words
    e = w.submit("hail a cutter what ship")
    assert e.kind == "order.rejected" and "Nothing in sight answers to 'a cutter'" in e.text
    # a brig in sight, and the lookout's report of one is his report
    seat = seat_player(w, "lookout", door="browser")
    e = seat.route("hail a brig two points on the lee bow")
    assert e.kind == "agent.hail", e.text
    w.submit("stand down the lookout")
    # by her rate: the words the other deck hears her called
    w2 = hove_to_world()
    put(
        w2,
        "sixty-four",
        "britain",
        "49 30.2 N 5 30 W",
        "bound for Falmouth",
        intent="bound for Falmouth",
        name="Ardent",
    )
    w2.run(61)
    e = w2.submit("hail the sixty-four: what ship is that?")
    assert e.kind == "hail.answered", e.text
    e = w2.submit("hail the seventy-four: what ship is that?")
    assert e.kind == "order.rejected" and "Nothing in sight answers to" in e.text


def test_a_captains_answer_to_a_hail_reaches_the_ship_that_hailed_her():
    """The Raven's captain answered `hail the sixty-four: ...` three times; each was a remark
    on her own quarterdeck, 'heard by' her own people, and none reached the player's log. His
    first try, `hail the ship: ...`, was refused because her masthead had not yet reported the
    ship that had just hailed her. A sail that has hailed this deck is hailed back whether the
    masthead has her or not, and a station's hail that names no sail is refused, not said."""
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import captain as captain_station
    from freesail.agents.model import Reply
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    raven = put(
        w,
        "cutter",
        "britain",
        "49 30.2 N 5 30 W",
        "in company with the ship",
        intent="patrol off the Lizard within 5 miles",
        name="Raven",
    )
    w.run(61)
    crew = raven.crew
    assert crew is not None and crew.shape == "full"
    policy = SamplingPolicy.in_lockstep(3600)
    Harness(crew, captain_station(policy, 3600, world=crew), Fake([Reply()], loop=True)).start()

    def said_from_her(words: str):
        before, hers = len(w.log), len(crew.log)
        with w.as_hull(crew):
            e = crew.submit(words, actor="the captain")
        return e, list(w.log)[before:], list(crew.log)[hers:]

    assert w.submit("hail the cutter: what ship is that?").kind == "hail.made"
    assert crew.ship.extra["hail_pending"]["from"] == str(w.own.id)
    # her masthead has not reported us: the hail is answered all the same
    crew.lookout._sails_seen.clear()
    for words, said in (
        ("hail the ship: Aye aye, sir", "Aye aye, sir"),
        ("hail her: We follow directly", "We follow directly"),
        ("hail the frigate: At your service", "At your service"),
    ):
        e, mine, hers = said_from_her(words)
        assert e.kind == "hail.made", (words, e.text)
        assert [x.kind for x in mine] == ["hail.heard"], (words, [x.text for x in mine])
        assert f"hails us: '{said}'" in mine[0].text
        assert "agent.spoke" not in {x.kind for x in hers}, words
    # a hail that names no sail is told so, and nothing is said on her deck or heard on ours
    e, mine, hers = said_from_her("hail the moon: Aye aye, sir")
    assert e.kind == "order.rejected" and "'hail the <sail>: <words>'" in e.text, e.text
    assert mine == [] and "agent.spoke" not in {x.kind for x in hers}
    # beyond hail, the hailer is not to be answered by a shout
    far = w.vessels.player_shadow(w)
    assert crew.ship.extra["hail_pending"]["from"] == str(far.id)
    assert H._has_hailed_us(crew, far, 1.0) and not H._has_hailed_us(crew, far, 2000.0)


# -- every root (package 76, step 6): the checker, and each root's hoist read and obeyed ----

NATION_OF_ROOT = {r: S.load_books(r).nation for r in S.roots()}
NATIONS_ROOTS = [r for r in S.roots() if r != "basic"]


@pytest.fixture(scope="module")
def _a_frigate():
    from tools.check_signals import _a_ship

    return _a_ship()


@pytest.mark.parametrize("root", S.roots())
def test_the_checker_passes_every_root(root, _a_frigate):
    """`tools/check_signals.py` over every root under data/signals/, so that a nation added
    later is checked by a test that does not know her name: her files load, every `does` an
    order a ship takes or a form 71's design names, every qualifier one the engine fills,
    every source named, every made entry marked, every nation reading her under her name."""
    from tools.check_signals import check_root

    assert check_root(root, _a_frigate) == []


@pytest.mark.parametrize("root", NATIONS_ROOTS)
def test_a_hoist_is_read_by_her_own_book_and_not_by_anothers(root):
    """A signal made under a nation's book is read by a ship holding that book ('No. N, the
    meaning') and is 'a signal we cannot read' to a ship holding another's."""
    books = S.load_books(root)
    entry, q = books.find("tack in succession")
    h = S.make_hoist(S.Locker(), books, entry, q, "sender", 100)
    near = 1.0 * units.NAUTICAL_MILE

    stranger = S.Locker()

    def read(reader_books, tick):
        return S.read_flying(
            stranger, reader_books, "sender", "the brig", [h], near, "day", False, tick, "x"
        )

    own = S.Locker()
    S.read_flying(own, books, "sender", "the brig", [h], near, "day", False, 170, "x")
    got = S.read_flying(own, books, "sender", "the brig", [h], near, "day", False, 230, "x")
    assert [x.kind for x in got] == ["signal.read"]
    assert f"No. {entry.number}, " in got[0].text
    other = "britain" if root != "britain" else "france"
    seen = read(S.load_books(other), 170)
    assert seen and "a signal we cannot read: not of our book" in seen[0].text
    assert read(S.load_books(other), 300) == []


@pytest.mark.parametrize("root", [r for r in NATIONS_ROOTS if r != "britain"])
def test_the_convoy_tacks_in_succession_on_one_hoist_of_her_own_book(root):
    """The convoy of four (data/scenarios/convoy.yaml) under each nation's colours and books:
    the player's one hoist of her convoy book's 'tack in succession' is read by every master,
    each a commanded captain under her orders, and performed in succession (Britain's is truth
    7-145)."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    nation = NATION_OF_ROOT[root]
    sf = load_scenario("data/scenarios/convoy.yaml")
    sf.scenario.nation = nation
    for spec in sf.scenario.ships:
        spec["nation"] = nation
    w = make_scenario_world(sf)
    begin(w, sf)
    names = ["Nancy", "Two Brothers", "Providence", "Friendship"]
    assert S.books_for(w).root == root
    w.run(600)
    said = w.submit("make the signal to tack in succession")
    assert said.kind == "signal.ordered", said.text
    entry = S.load_books(root).find("tack in succession", "convoy")[0]
    assert f"No. {entry.number}, " in said.text
    about: dict[str, int] = {}
    for _ in range(30):
        w.run(60)
        for n in names:
            v = w.vessels.find(n)
            if n not in about and any("went about" in words for _, words in (v.story or ())):
                about[n] = next(t for t, words in v.story if "went about" in words)
    assert set(about) == set(names), about
    ticks = [about[n] for n in names]
    assert ticks == sorted(ticks) and len(set(ticks)) == 4, ticks
