"""The flags of command and identity (spec M7 §1; package 76, the owner's addition of
2026-11-07): each root's seventh file, `colours.yaml`, what flies where by the rules, the
lookout's words, the orders, and the private signal in another nation's form
(`freesail/world/flags.py`; docs/design/Design-Signals.md, "As built out")."""

from __future__ import annotations

import pytest

from freesail.world import flags as F
from freesail.world import signals as S
from freesail.world.nations import load_nations


def _places(listed):
    return [(x["place"], x["name"]) for x in listed]


# -- the files -----------------------------------------------------------------------------


@pytest.mark.parametrize("root", S.roots())
def test_every_root_has_its_colours_in_one_shape(root):
    """Every root has the seventh file; every flag a kind, a source and a drawing (basic's
    ensign drawn from the nation's word); every occasion's flags named in the file and at
    81's place words; the drawings within the flag's square."""
    f = F.load_colours(root)
    assert f.nation == S.load_books(root).nation and f.sources
    files = [f, *f.nations.values()]
    for g in files:
        assert g.flags and g.occasions, root
        for flag in g.flags.values():
            assert flag.kind in F.KINDS and flag.source, (root, flag.name)
            assert flag.drawing or (g is f and root == "basic" and flag.kind == "ensign")
            for p in flag.drawing:
                xs = p["rect"] if "rect" in p else [v for pt in p["line"] for v in pt]
                assert all(0.0 <= float(v) <= 1.0 for v in xs), (root, flag.name, p)
        assert any(o.occasion == "at sea" for o in g.occasions)
        for o in g.occasions:
            for name, where in o.flags:
                assert name in g.flags and F.place_ok(where), (root, o, name, where)


def test_the_file_refuses_a_place_not_81s_and_a_flag_it_has_not(tmp_path):
    base = tmp_path / "signals"
    (base / "x").mkdir(parents=True)
    good = (
        "nation: x\nsources: [made]\nflags:\n  - name: ensign\n    kind: ensign\n"
        "    proportion: [1, 2]\n    drawing:\n      - {rect: [0, 0, 1, 1], colour: red}\n"
        "    source: made\noccasions:\n"
    )
    (base / "x" / "colours.yaml").write_text(
        good + '  - {occasion: "at sea", role: "any", flags: [{name: ensign, where: "the poop"}]}\n'
    )
    with pytest.raises(S.BookFileError, match="place words"):
        F.load_colours("x", str(base))
    (base / "x" / "colours.yaml").write_text(
        good + '  - {occasion: "at sea", role: "any", flags: [{name: jack, where: "peak"}]}\n'
    )
    F.load_colours.cache_clear()
    with pytest.raises(S.BookFileError, match="names no flag"):
        F.load_colours("x", str(base))
    F.load_colours.cache_clear()


# -- what flies where ----------------------------------------------------------------------


def test_what_flies_where_by_role_occasion_and_state():
    n = load_nations()
    gb = S.Colours(state="shown", nation="britain")
    assert _places(F.flies(n, gb, "kings-ship")) == [
        ("peak", "red ensign"),
        ("main truck", "red pendant"),
    ]
    assert _places(F.flies(n, gb, "commodore")) == [
        ("peak", "red ensign"),
        ("main truck", "red broad pendant"),
    ]
    assert _places(F.flies(n, gb, "merchant")) == [("peak", "merchant red ensign")]
    assert _places(F.flies(n, gb, "kings-ship", in_action=True)) == [
        ("peak", "red ensign"),
        ("main topgallant masthead", "red ensign"),
        ("main truck", "red pendant"),
        ("fore truck", "union jack"),
    ]
    assert ("jackstaff", "union jack") in _places(F.flies(n, gb, "kings-ship", at_anchor=True))
    # the flags ordered beside: the broad pendant takes the pendant's place
    assert _places(F.flies(n, gb, "kings-ship", ordered=["broad pendant", "jack"])) == [
        ("peak", "red ensign"),
        ("main truck", "red broad pendant"),
        ("fore truck", "union jack"),
    ]
    # struck or hauled down: nothing; distress: the ensign turned over, said so
    for state in ("struck", "none"):
        assert F.flies(n, S.Colours(state=state, nation="britain"), "kings-ship") == []
    down = F.flies(n, S.Colours(state="distress", nation="britain"), "merchant")[0]
    assert down["drawing"]["inverted"] and down["words"].endswith("the ensign union down")
    # the hover's words as the lookout reads them; the lines kept apart from 81's parts
    ensign = F.flies(n, gb, "kings-ship")[0]
    assert ensign["words"] == "British colours, the red ensign"
    assert all("rect" in p for p in ensign["drawing"]["parts"]) and ensign["drawing"]["lines"]
    # false colours: the shown nation's file
    false = F.flies(n, S.Colours(state="false", nation="spain"), "kings-ship")
    assert _places(false) == [("peak", "Spanish ensign"), ("main truck", "Spanish pendant")]
    # a nation on basic: her plain ensign from her word; Portugal's own flags, dated
    moor = F.flies(n, S.Colours(state="shown", nation="morocco"), "merchant")[0]
    assert moor["drawing"]["parts"][0]["colour"] == "red"
    pt = F.file_for_nation(n, "portugal")
    assert pt.flags["Portuguese ensign"].dates == "-1816"


def test_the_lookout_reads_the_pendant_and_the_broad_pendant_at_the_colours_range():
    """A King's frigate made out with her colours: 'she wears a pendant at the main: a
    man-of-war'; a merchant brig her ensign alone, nothing more said; a commodore escorting a
    convoy his broad pendant."""
    from tests.test_brains import put, world_at

    w = world_at(49.5, -5.5)
    frigate = put(w, "frigate", "britain", "49 29 N 5 32 W", "bound for Plymouth", name="Amazon")
    brig = put(w, "brig", "britain", "49 31 N 5 32 W", "bound for Plymouth", name="Nancy")
    w.run(240)
    made = [e.text for e in w.log if e.kind == "lookout.made_out"]
    assert any(
        "British colours, the red ensign; she wears a pendant at the main: a man-of-war." in t
        for t in made
    ), made
    items = {i["id"]: i for i in w.readings.value("strangers")["items"]}
    assert items[frigate.id]["words"].endswith("she wears a pendant at the main: a man-of-war")
    assert items[brig.id]["words"].endswith("British colours, the red ensign")
    brig.role = "commodore"
    assert F.vessel_flies_words(w, brig) == "she wears a broad pendant at the main: a commodore"


def test_beating_to_quarters_doubles_the_ensigns_with_the_jack_at_the_fore():
    """The player's frigate, a King's ship by her papers: at sea her ensign at the peak and her
    pendant at the main; at quarters the second ensign at the main topgallant masthead and the
    jack at the fore, as the viewer reads the locker's list."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, papers={"private_signals": True})
    S.locker_of(w.ship)
    w.run(60)
    assert _places(S.locker_of(w.ship).flies) == [
        ("peak", "red ensign"),
        ("main truck", "red pendant"),
    ]
    w.submit("beat to quarters")
    w.run(240)
    assert w.ship.extra["quarters"].at_quarters
    assert _places(S.locker_of(w.ship).flies) == [
        ("peak", "red ensign"),
        ("main topgallant masthead", "red ensign"),
        ("main truck", "red pendant"),
        ("fore truck", "union jack"),
    ]
    from freesail.api import viewer_flags

    assert viewer_flags.flags(w, w.ship) == S.locker_of(w.ship).flies


def test_the_flag_orders_and_their_refusal():
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, papers={"private_signals": True})
    w.submit("hoist the broad pendant")
    w.submit("hoist the jack")
    said = [e.text for e in w.log if e.kind == "flags.changed"]
    assert said == [
        "A commodore's broad pendant hoisted at the main.",
        "The union jack hoisted at the fore.",
    ]
    assert ("main truck", "red broad pendant") in _places(S.locker_of(w.ship).flies)
    w.submit("haul down the colours")
    assert S.locker_of(w.ship).flies == [] and S.locker_of(w.ship).ordered_flags == []
    w.submit("hoist a second ensign at the main")
    refused = [e.text for e in w.log if e.kind == "order.rejected"]
    assert refused and "Her colours are down" in refused[-1]


# -- the private signal in another nation's form -------------------------------------------


def _succession_world():
    from tests.test_brains import world_at

    return world_at(
        49.5,
        -5.5,
        papers={"private_signals": True, "signal_books": ["spain", "portugal"]},
        intent="keep the station off the Lizard within 20 miles",
    )


def test_a_table_not_held_is_refused_in_words_and_the_tables_held_are_named():
    from tests.test_brains import world_at

    w = _succession_world()
    assert list(S.held_tables(w)) == ["britain", "spain", "portugal"]
    w.submit("make the Danish private signal")
    refused = [e.text for e in w.log if e.kind == "order.rejected"]
    assert refused and "There is no Danish table aboard" in refused[-1]
    assert "British, Spanish, Portuguese" in refused[-1]
    bare = world_at(49.5, -5.5)
    assert S.held_tables(bare) == {}


def test_the_private_signals_in_succession_unanswered_make_her_an_enemy():
    """The Java's move: the British, Spanish and Portuguese challenges in succession to a
    frigate under British colours, each a hoist in its nation's form, three minutes a hoist;
    none answered, and the captain holds her an enemy by the tell (71's: our colours, a man of
    war's rig, no answer)."""
    from tests.test_brains import put

    w = _succession_world()
    put(
        w,
        "frigate",
        "france",
        "49 29 N 5 31 W",
        "bound for Brest",
        name="Hortense",
        colours="British",
    )
    w.run(180)
    w.submit("make the private signals in succession to Hortense")
    w.run(900)
    locker = S.locker_of(w.ship)
    made = [h for h in locker.made if h.book == "private"]
    assert [h.form_nation for h in made] == ["britain", "spain", "portugal"]
    assert [b.breaks_out - a.breaks_out for a, b in zip(made, made[1:], strict=False)] == [300, 300]
    judged = [e for e in w.log if e.kind == "signal.private_judged"]
    assert [e.text for e in judged] == [
        "The frigate makes no answer to the private signals, British, Spanish and Portuguese in "
        "succession: a man of war under false colours, an enemy."
    ]
    assert w.captain.recognised["ship-1"]["enemy"] is True


def test_a_stranger_answers_the_challenge_made_in_her_own_form_and_no_other():
    """A Danish frigate holds the Danish table and no other: she makes no answer to the
    British challenge and answers the Danish rightly, so the succession stops at the Danish and
    she is known a Danish ship (Denmark at peace; Denmark stands on basic for her signals, her
    table the same draw her own ships hold)."""
    from tests.test_brains import put, world_at

    w = world_at(
        49.5,
        -5.5,
        papers={"private_signals": True, "signal_books": ["denmark"]},
        intent="keep the station off the Lizard within 20 miles",
    )
    put(
        w,
        "frigate",
        "denmark",
        "49 29 N 5 31 W",
        "bound for Plymouth",
        name="Najaden",
        intent="bound for Plymouth",
    )
    w.run(180)
    assert list(S.held_tables(w)) == ["britain", "denmark"]
    w.submit("make the private signals in succession to Najaden")
    w.run(900)
    judged = [e.text for e in w.log if e.kind == "signal.private_judged"]
    assert judged == ["The frigate answers the Danish private signal rightly: a Danish ship."]
    made = [h.form_nation for h in S.locker_of(w.ship).made if h.book == "private"]
    assert made == ["britain", "denmark"]
    assert w.captain.recognised["ship-1"]["enemy"] is False


def test_the_flags_of_command_come_down_by_their_names_and_the_flags_read_what_flies():
    """Truth 7-457 (package 98, step 7; the owner's further note of 2026-11-09): the broad
    pendant, the jack and a second ensign, hoisted, are read by `the flags` at their places
    beside the ensign (it said none with all three flying); each comes down by its name
    (haul down, strike, lower), the colours left flying, and is refused in words when it is
    not flying; the signal hoist is read after them; `the colours` reads the ensign as
    before; from the cabin each is refused as the deck's, the reading answered where it is
    had."""
    from freesail.api.session import make_world

    w = make_world(7, "data/ships/hermaphrodite-brig.yaml")
    colours = w.submit("the colours").text
    ensign = "American colours, the stars and stripes at the peak"
    assert w.submit("the flags").text == f"The flags: {ensign}."
    for line in ("hoist the broad pendant", "hoist the jack", "hoist a second ensign at the main"):
        assert w.submit(line).kind == "flags.changed", line
    said = w.submit("the flags").text
    assert "broad pendant at the main truck" in said
    assert "jack, the union of stars at the fore truck" in said
    assert said.count("stars and stripes at the") == 2  # the ensign doubled
    assert w.submit("the colours").text == colours
    # the signal hoist read after them
    assert w.submit("make the signal to chase").kind == "signal.ordered"
    for _ in range(10):
        w.run(30)
        if "signal flying" in w.submit("the flags").text:
            break
    said = w.submit("the flags").text
    assert "; the signal flying: " in said and said.index("signal flying") > said.index("jack")
    # each by its name, the colours left flying
    for line, gone in (
        ("haul down the jack", "jack"),
        ("strike the broad pendant", "broad pendant"),
        ("lower the second ensign", "main topgallant masthead"),
    ):
        e = w.submit(line)
        assert e.kind == "flags.changed" and "hauled down" in e.text, (line, e.text)
        assert gone not in w.submit("the flags").text, line
    assert w.submit("the flags").text.startswith(f"The flags: {ensign}; the signal flying")
    assert w.submit("the colours").text == colours
    for line in ("haul down the jack", "lower the broad pendant", "haul down the second ensign"):
        e = w.submit(line)
        assert e.kind == "order.rejected" and "is flying: there is none to haul down" in e.text
    # by the deck's rule (step 6): from the cabin refused, the reading where it is had
    w.submit("hoist the jack")
    w.submit("go below")
    e = w.submit("haul down the jack")
    assert e.kind == "order.rejected" and "go on deck to give an order of the deck" in e.text
    assert w.submit("the flags").text.endswith("you are in the cabin.")
