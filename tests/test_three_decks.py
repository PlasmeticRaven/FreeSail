"""Package 90, A9: three gun decks (`docs/design/Plan-Package90.md` §6; the *Concepción*'s design,
`docs/design/Design-Ship-PurisimaConcepcion.md` §5.5 and §6.3; the engine note,
`docs/design/Design-Package90-Engine.md` §6).

The quarter bill's two readers of a deck (`crew/quarters.py`): the middle deck's crews behind ports
the sea has shut robbed first with the lower deck's, and of the crews left open the upper deck's and
the upper works' first, the middle deck's after them and the lower deck's last. The gun deck's
words (`orders/gunnery.py`): "the second deck" and "the third deck" for the middle and the upper
deck of a ship of three gun decks, and "the main deck" refused there in words naming her three
(the lead's ruling 7 of 2026-11-18). Each is keyed on broadside guns on a `middle` deck, which no
committed file carries; so they are proved on the engine note's three-decker probe
(`tests/rig_fixtures.py`, the 74 with a middle deck where her upper deck was and an upper deck
raised over it, her company 839: scratch figures, not the *Concepción*'s), written as a ship file
and loaded as the game loads one, and every two-decker is held to its order and words as before.

The probe's figures were measured at seed 7 in tests/test_brains.py's world off the Lizard (the
cloud's build machine, 2026-11-28).
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from rig_fixtures import three_decker_probe_doc, write_ship

from freesail.ship.loader import load_ship, load_spec

ROOT = Path(__file__).resolve().parents[1]
SEVENTY_FOUR = "data/ships/seventy-four.yaml"
SIXTY_FOUR = "data/ships/sixty-four.yaml"
TWO_DECKERS = (SEVENTY_FOUR, SIXTY_FOUR)
# the files that may carry a middle deck: hers alone, when it lands (Con-D decision 1)
HERS = "data/ships/three-decker.yaml"


@pytest.fixture(scope="module")
def probe_path(tmp_path_factory) -> str:
    """The three-decker probe written as a ship file, for what reads a path."""
    folder = tmp_path_factory.mktemp("three-decks")
    return str(write_ship(three_decker_probe_doc(), folder, "three-decker-probe"))


def _beaten(path, heel_deg=None, engaged=None):
    """Her quarters at muster, seed 7, tests/test_brains.py's world (tests/test_bellerophon.py's
    `_beaten`); heeled by hand to shut the lee ports by the rule, the battery engaged to a side,
    where asked."""
    from freesail.combat import action, ports
    from freesail.combat.guns import battery_of
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, path)
    w.run(10)
    said = w.submit("beat to quarters")
    w.run(30)
    if heel_deg is not None:
        b = battery_of(w.ship)
        b.engaged = engaged
        w.ship.dyn.heel = math.radians(heel_deg)
        ports.update(b, action._firer(w, w.ship), w.clock.tick)
    return w, said, quarters_of(w.ship)


def _committed() -> list[str]:
    return sorted(f"data/ships/{p.name}" for p in (ROOT / "data" / "ships").glob("*.yaml"))


# ---------------------------------------------------------------------------
# Keyed on a middle deck
# ---------------------------------------------------------------------------


def test_no_committed_file_but_hers_carries_a_middle_deck():
    """A9 is keyed on broadside guns on a `middle` deck (Plan §6, row A9): no committed file
    carries one in any fit, so nothing committed robs, says or names a deck otherwise (her file,
    when it lands, the only one that may)."""
    with_middle = set()
    for path in _committed():
        spec = load_spec(path)
        for fit in (spec.armament.fits or {}).values() if spec.armament else ():
            if any(g.deck == "middle" for g in fit.guns):
                with_middle.add(path)
    assert with_middle <= {HERS}, with_middle


# ---------------------------------------------------------------------------
# The beat and the robbing by deck (crew/quarters.py)
# ---------------------------------------------------------------------------


def test_the_beat_says_three_gun_decks_from_below(probe_path):
    """B7.b's line a deck (`_deck_lines`) takes the middle deck between the lower and the upper, as
    the engine note measured it (Eng §6.1), every crew manned: lower, middle, upper, then the
    quarterdeck, the forecastle and the poop."""
    _w, said, q = _beaten(probe_path)
    lines = q.describe()
    assert lines[1:7] == [
        "The lower deck: 14 gun crews, 182 men.",
        "The middle deck: 14 gun crews, 126 men.",
        "The upper deck: 14 gun crews, 126 men.",
        "The quarterdeck: seven gun crews, 42 men.",
        "The forecastle: three gun crews, 16 men.",
        "The poop: three gun crews, 12 men.",
    ]
    assert " ".join(lines[1:7]) in said.text
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())


def test_a_middle_deck_behind_shut_ports_is_robbed_with_the_lower_deck(probe_path):
    """Con-D §6.3 (A9): heeled 35 deg to starboard by hand, engaged to starboard, the sea shuts her
    whole lee lower tier and the middle tier amidships (the probe's sills, the 74's upper deck's:
    measured, the middle deck's Nos. 4 to 10); the middle deck's crews whose starboard gun is shut
    are counted shut with the lower deck's (before A9, the lower deck's alone)."""
    from freesail.crew.quarters import LOWER, MIDDLE

    _w, _said, q = _beaten(probe_path, heel_deg=35.0, engaged="starboard")
    shut = q._shut_crews()
    by_deck = {}
    for k in shut:
        by_deck.setdefault(q.crews[k].deck, set()).add(int(k.rsplit(":", 1)[1]))
    assert set(by_deck) == {LOWER, MIDDLE}
    assert by_deck[LOWER] == set(range(1, 15))
    assert by_deck[MIDDLE] == set(range(4, 11))


@pytest.mark.parametrize(
    "heel, ranks_seen, words",
    [
        (
            12.5,
            {0, 1, 2, 3},
            "from the lower deck, Nos. 4 to 11, their ports shut, the poop, Nos. 1 to 3, the "
            "upper deck, Nos. 1 to 14, the quarterdeck, Nos. 1 to 7, the forecastle, Nos. 1 to 3, "
            "and the middle deck, Nos. 3 to 14",
        ),
        (
            35.0,
            {0, 1, 2},
            "from the lower deck, Nos. 1 to 14, their ports shut, the middle deck, Nos. 4 to 10, "
            "their ports shut, the poop, Nos. 1 to 3, the upper deck, Nos. 3 to 14, and the "
            "quarterdeck, Nos. 1 to 7",
        ),
    ],
)
def test_robbing_on_three_decks_takes_the_shut_then_the_upper_then_the_middle_the_lower_last(
    probe_path, heel, ranks_seen, words
):
    """Con-D §6.3 (A9): the crews behind shut ports first, the lower deck's and the middle deck's
    together from the end that bears least; then the upper deck's and the upper works' (the 74's
    "other decks"); then the middle deck's open crews; the lower deck's open crews last, the
    lighter metal before the heavier. Sail work wanting 400 hands, the enemy forward, the line
    names each deck, the shut crews apart (measured): at 12.5 deg her lower tier shut amidships
    and the middle deck's open crews taken before any open lower-deck crew; at 35 deg her whole
    lower tier shut and her middle tier amidships (before A9 the middle deck's shut crews ranked
    with the upper works', and its open crews with them before the lower deck's)."""
    from freesail.crew.quarters import LOWER, MIDDLE, _rob_order

    _w, _said, q = _beaten(probe_path, heel_deg=heel, engaged="starboard")
    shut = q._shut_crews()
    order = sorted(q.crews.values(), key=lambda gc: _rob_order(gc, True, shut))
    numbered = [gc for gc in order if gc.deck]

    def rank(gc):
        if gc.key in shut:
            return 0
        return {MIDDLE: 2, LOWER: 3}.get(gc.deck, 1)

    ranks = [rank(gc) for gc in numbered]
    assert ranks == sorted(ranks), ranks
    assert set(ranks) == ranks_seen
    assert {numbered[i].deck for i, r in enumerate(ranks) if r == 1} == {
        "upper",
        "quarterdeck",
        "forecastle",
        "roundhouse",
    }
    freed, said = q.lend(400, False, True)
    assert len(freed) >= 400
    assert said == words


def _rob_order_before_a9(gc, bearing_fwd, shut):
    """The robbing order as it stood before A9 (crew/quarters.py `_rob_order` at 93cf624c), the
    reference against which every two-decker is held."""
    from freesail.crew.quarters import GUN_PREFIX, LOWER, _crew_number

    key = gc.key[len(GUN_PREFIX) :]
    if "swivel" in key:
        return (0, 0, 0.0, key)
    if _crew_number(gc.key) is None:
        return (1, 0, 0.0, key)
    deck = (0 if gc.key in shut else 2) if gc.deck == LOWER else 1
    x = gc.x_m if bearing_fwd in (True, None) else -gc.x_m
    return (2, deck, x, key)


@pytest.mark.parametrize("path", TWO_DECKERS)
@pytest.mark.parametrize("heel", [8.0, 12.5, 30.0, 40.0])
def test_a_two_deckers_robbing_is_as_it_was_at_every_heel(path, heel):
    """A9 is keyed on a middle deck: on the 74 and the 64, heeled by hand and engaged to the lee
    side, the crews counted shut are the lower deck's alone, as before (their upper ports shut
    too at 40 deg, and are not counted), and the order from either end is the order before A9,
    crew for crew (the ranks 0, 1 and 2 become 0, 1 and 3)."""
    from freesail.crew.quarters import LOWER, _rob_order

    _w, _said, q = _beaten(path, heel_deg=heel, engaged="starboard")
    shut = q._shut_crews()
    assert all(q.crews[k].deck == LOWER for k in shut)
    for fwd in (True, False, None):
        new = sorted(q.crews.values(), key=lambda gc: _rob_order(gc, fwd, shut))
        old = sorted(q.crews.values(), key=lambda gc: _rob_order_before_a9(gc, fwd, shut))
        assert [gc.key for gc in new] == [gc.key for gc in old], (heel, fwd)


# ---------------------------------------------------------------------------
# The deck's words (orders/gunnery.py)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "words, deck, side, n",
    [
        ("the middle deck", "middle", None, 28),
        ("the second deck", "middle", None, 28),
        ("the starboard second deck", "middle", "starboard", 14),
        ("the second-deck guns", "middle", None, 28),
        ("the third deck", "upper", None, 28),
        ("the third deck to larboard", "upper", "larboard", 14),
        ("the upper deck", "upper", None, 28),
        ("the lower deck", "lower", None, 28),
        ("the gun deck", "lower", None, 28),
        ("No. 3 gun of the second deck", "middle", None, 2),
        ("No. 3 starboard gun of the third deck", "upper", "starboard", 1),
        ("the second deck's No. 3", "middle", None, 2),
        ("the main deck", None, None, 0),
        ("the starboard main deck", None, None, 0),
        ("the main deck's No. 3", None, None, 0),
    ],
)
def test_her_gun_decks_by_their_words_on_three_decks(probe_path, words, deck, side, n):
    """Con-D §5.5 (A9): on a ship of three gun decks "the second deck" names the middle deck and
    "the third deck" the upper (James vol. 2 p. 51; Falconer's "the second or middle deck"), in
    every form a deck is named by, with a number or without; "the main deck" names none."""
    from freesail.orders.gunnery import guns_named

    ship = load_ship(probe_path)
    ids = guns_named(ship, words)
    assert len(ids) == n, (words, len(ids))
    if deck:
        assert {ship.guns[g].deck for g in ids} == {deck}
    if side:
        assert {ship.guns[g].side for g in ids} == {side}


@pytest.mark.parametrize("path", TWO_DECKERS)
def test_on_a_two_decker_the_second_and_third_deck_name_none_and_the_main_deck_her_upper(path):
    """A9's words are keyed on a middle deck: on the 74 and the 64 "the second deck" and "the third
    deck" name no gun of hers, as before (judgement: left unbuilt there, Con-D §5.5), and "the
    main deck" her upper deck, as before (Cumby's word)."""
    from freesail.orders.gunnery import guns_named

    ship = load_ship(path)
    for words in ("the second deck", "the third deck", "No. 3 gun of the second deck"):
        assert guns_named(ship, words) == [], words
    upper = sorted(g.id for g in ship.guns.values() if g.deck == "upper" and g.place == "broadside")
    assert sorted(guns_named(ship, "the main deck")) == upper


def _engaged_at_quarters(path):
    """At quarters, her guns cast loose, a mark engaged to starboard (tests/test_bellerophon.py's
    world for "fire the starboard lower deck")."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, path)
    w.run(10)
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    w.submit("engage a mark four cables on the starboard beam")
    return w


def test_fire_the_second_deck_fires_her_middle_deck_and_the_main_deck_is_refused_naming_three(
    probe_path,
):
    """Through the order (A9; the lead's ruling 7): "fire the second deck" puts her fourteen
    starboard middle-deck guns (the side engaged) to fire each as soon as it is ready, the reply
    in the words said;
    "fire the main deck" is refused in words naming her three gun decks, as a bare number is
    refused naming her decks."""
    from freesail.combat.guns import battery_of

    w = _engaged_at_quarters(probe_path)
    said = w.submit("fire the second deck")
    assert said.kind == "guns.fire", said.text
    assert (
        said.text == "The starboard second-deck guns to fire each as soon as it is ready, 14 guns."
    )
    single = battery_of(w.ship).single
    assert {(w.ship.guns[g].deck, w.ship.guns[g].side) for g in single} == {("middle", "starboard")}
    said = w.submit("fire the starboard main deck")
    assert said.kind == "order.rejected", said.text
    assert said.text == (
        "Order not carried out ('fire the starboard main deck'): She has three gun decks, the "
        "lower deck, the middle deck and the upper deck, and 'the main deck' names none of them: "
        "name the deck, as 'fire the middle deck' (or 'the second deck'; 'the third deck' is the "
        "upper)."
    )


def test_on_the_74_fire_the_second_deck_is_refused_as_before_and_the_main_deck_fires():
    """On the 74 the words are as before A9 (measured at 93cf624c): "fire the second deck" names
    no gun of hers, in the refusal's old words; "fire the starboard main deck" fires her upper
    deck's fourteen."""
    w = _engaged_at_quarters(SEVENTY_FOUR)
    said = w.submit("fire the second deck")
    assert said.kind == "order.rejected"
    assert said.text == (
        "Order not carried out ('fire the second deck'): Fire what? Say 'fire' for the broadside "
        "at the word, 'fire the starboard broadside', 'fire No. 3 gun of the lower deck', 'fire "
        "the bow chaser', 'fire the pivot gun', 'fire a shot across her bows' or 'fire a gun to "
        "leeward'; 'the second deck' names no gun of hers."
    )
    said = w.submit("fire the starboard main deck")
    assert said.text == "The starboard main-deck guns to fire each as soon as it is ready, 14 guns."
