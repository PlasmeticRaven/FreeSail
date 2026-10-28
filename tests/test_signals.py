"""The colours, the signal books, a signal hoisted and read, the private signal and the
hail (spec M7 §1 to §5; package 71; `docs/design/Design-Signals.md`)."""

from __future__ import annotations

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
            assert e.made and (e.show or e.fire), (root, e.meaning)
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
    assert b.find("tack", "fog")[0].fire == "two guns"
    assert b.find("a sentence the book lacks") is None


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
        and heard[0].text == "The brig fires two guns: tack together."
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
