"""Found on the way (package 85's reading of the orders): four refusals mended.

- A standing order's name with an apostrophe ("the bay's mouth") was refused with "After
  the name say a colon": the closing quote now pairs with the opening one, so an
  apostrophe inside a name in double quotes is the name's.
- `hail the lugger` at three cables from a dismasted lugger in sight resolved to a far
  lugger on the world's sea: a rig word is matched among the sails in sight alone, a name
  alone reaches beyond them, and a mark in sight that answers to the words is said to be
  no sail.
- `captain: carry on`, the player's word that gives the ship back to her rules-based
  captain after the player's hand, was refused at the prompt as a world order (the
  director's channel's form): it is the player's own there.
- `gybe the mainsail` was answered "'wear ship' was understood, but not 'the mainsail'":
  the gybe is the wear whole and names no sail, and the answer says so with the sheet's
  order for a boom handled by hand.
"""

from __future__ import annotations

from pathlib import Path

from freesail import orders
from freesail.orders.errors import OrderError

ROOT = Path(__file__).resolve().parents[1]


def test_a_standing_orders_name_may_carry_an_apostrophe():
    from tests.test_primer import make_ship

    ship = make_ship("frigate", "plain-sail", "starboard")
    kind, log, _ = orders.handle(
        ship, 'standing order "the bay\'s mouth": every glass then trim sails'
    )
    assert kind == "standing.given" and log.startswith("Standing order 'the bay's mouth' entered")
    assert orders.handle(ship, 'show standing order "the bay\'s mouth"')[1].startswith(
        'Standing order "the bay\'s mouth"'
    )
    assert (
        orders.handle(ship, 'belay "the bay\'s mouth"')[1]
        == "Standing order 'the bay's mouth' belayed."
    )
    # curly quotes pair the same, and a single-quoted name still closes at a single quote
    assert orders.handle(ship, "standing order “Mr Pearce’s trim”: every glass then trim sails")[
        0
    ] == ("standing.given")
    assert orders.handle(ship, "standing order 'plain': every glass then heave the log")[0] == (
        "standing.given"
    )
    try:
        orders.handle(ship, 'standing order "unclosed: every glass then trim sails')
    except OrderError as e:
        assert "wants its closing quote" in str(e)
    else:
        raise AssertionError("an unclosed name was taken")


def test_the_hail_names_a_sail_in_sight_and_not_a_far_one_and_a_wreck_is_no_sail():
    from freesail.world import orders as WO
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    put(
        w,
        "lugger",
        "france",
        "49 00 N 6 00 W",
        "bound for Brest",
        intent="bound for Brest",
        name="Hirondelle",
    )
    w.run(1)
    WO.apply(w, WO.parse("mark: a dismasted lugger riding to a sea-anchor at 49 30.3 N 5 30 W"))
    w.run(120)
    assert "a dismasted lugger riding to a sea-anchor" in w.submit("what is in sight").text
    said = w.submit("hail the lugger: what ship is that?")
    assert said.kind == "order.rejected"
    assert "A dismasted lugger riding to a sea-anchor is in sight, but she is no sail" in said.text
    assert "cables off" not in said.text
    # a name alone reaches a sail beyond the lookout's sight, refused for the distance
    far = w.submit("hail the Hirondelle")
    assert far.kind == "order.rejected" and "beyond hail" in far.text
    # a rig word with nothing of it in sight
    none = w.submit("hail the brig")
    assert none.kind == "order.rejected" and "Nothing in sight answers to 'the brig'" in none.text


def test_captain_carry_on_at_the_prompt_is_the_players_own_hand_given_back():
    from freesail.world.scenarios import load_scenario, make_scenario_world

    w = make_scenario_world(load_scenario(ROOT / "data/scenarios/dispatches-falmouth.yaml"), seed=7)
    w.run(900)
    assert w.captain.commands and w.captain.state is not None
    w.submit("steer east")
    w.run(2)
    assert w.captain.aside
    aside = [e for e in w.log if e.kind == "captain.aside"]
    assert aside and "'captain: carry on' gives her back to him" in aside[-1].text
    said = w.submit("captain: carry on")
    assert said.kind == "captain.carry_on", said.text
    assert said.text.startswith("By the captain's word: Mr Bowen carries on: trade copper ore")
    assert not w.captain.aside
    again = w.submit("captain: carry on")
    assert again.kind == "order.rejected" and "is not standing aside; he commands her" in again.text
    # every other captain order is still the world's, refused at the prompt
    other = w.submit("captain: trade tin from Falmouth to Plymouth")
    assert other.kind == "order.rejected" and "an order to the world" in other.text


def test_gybe_the_mainsail_is_answered_that_the_gybe_names_no_sail():
    from tests.test_primer import make_ship

    ship = make_ship("schooner", "plain-sail", "starboard")
    for words in ("gybe the mainsail", "jibe her mainsail"):
        try:
            orders.handle(ship, words)
        except OrderError as e:
            assert "is wear ship whole, the period word, and takes no sail after it" in str(e)
            assert "'ease the main sheet'" in str(e)
        else:
            raise AssertionError(f"{words!r} was taken")
    kind, log, _ = orders.handle(ship, "gybe")
    assert log.startswith("Gybe, that is, wear ship")
