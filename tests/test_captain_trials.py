"""The captain's trials (spec M6 §9 item 1; decision 41; package 40c, the lead): the
rules-based captain of `freesail.world.captains` under weather scripts and world orders,
each trial a scenario of `data/scenarios/trials/` sailed by the intent alone, the states
he enters and the books he loads proved against the doctrine's table, and the whole run
pinned to its digest at seed 7 (measured on the build machine; docs/dev/TuningNotes.md,
package 40c). The gate's owner runs the same scenarios with no order of the ship's given.

The player's hand (decision 41) is tested here too, on the intent scenario: an order of
the ship's at the prompt makes the captain stand aside, `captain: carry on` gives her back.
"""

from __future__ import annotations

import pytest

from freesail.core.world import World
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

TRIALS = "data/scenarios/trials"
HOURS = 20


def trial(name: str, hours: int = HOURS) -> World:
    sf = load_scenario(f"{TRIALS}/{name}.yaml")
    world = make_scenario_world(sf)
    begin(world, sf)
    world.run(hours * 3600)
    return world


def states(world: World) -> list[tuple[int, str]]:
    return [(e.tick, e.data["state"]) for e in world.log if e.kind == "captain.state"]


def books(world: World) -> list[str]:
    return [
        e.data.get("state", "")
        for e in world.log
        if e.kind == "captain.state" and e.data.get("book")
    ]


# -- the King's ship on her station -----------------------------------------------------

TRIAL_STATION_STRANGER_STATES = [
    (300, "keeping station"),
    (7200, "investigating a stranger"),
    (7260, "chasing"),
    (7980, "keeping station"),
]
TRIAL_STATION_STRANGER_WITHIN_HAIL_TICK = 7972
TRIAL_STATION_STRANGER_LINES = 889
TRIAL_STATION_STRANGER_DIGEST = "01fb6bd6ab67f42c"


@pytest.fixture(scope="module")
def station_stranger():
    return trial("trial-station-stranger")


def test_the_station_is_to_seaward_of_its_place_and_the_stranger_is_chased(station_stranger):
    """`keep the station off Ushant within 15 miles`: the station mark is the point the
    radius from the island with the most sea room, to the westward (`captains.station_off`),
    never the island itself, which the first trial ran her onto; the stranger put on the sea
    by the director is investigated, made out, chased and spoken within the hour, and the
    station kept again, the books loaded and unloaded by name."""
    w = station_stranger
    cap = w.captain
    assert cap.role == "kings-ship" and cap.intent is not None and cap.intent.kind == "station"
    mark = cap._station_mark()
    assert mark is not None and mark[0] == "48 33.3 N 5 26.6 W"
    assert states(w) == TRIAL_STATION_STRANGER_STATES
    assert books(w)[:3] == ["keeping station", "investigating a stranger", "chasing"]
    hail = [e.tick for e in w.log if e.kind == "sail.within_hail"]
    assert hail[:1] == [TRIAL_STATION_STRANGER_WITHIN_HAIL_TICK]
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert cap.state == "keeping station"
    assert len(w.log) == TRIAL_STATION_STRANGER_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_STRANGER_DIGEST


TRIAL_STATION_GALE_FIRST_STATES = [
    (300, "keeping station"),
    (19440, "hove to for weather"),
    (25860, "on passage"),
    (25920, "keeping station"),
    (26520, "hove to for weather"),
]
TRIAL_STATION_GALE_LINES = 745
TRIAL_STATION_GALE_DIGEST = "4c544addc681f505"


@pytest.fixture(scope="module")
def station_gale():
    return trial("trial-station-gale")


def test_in_a_gale_with_sea_room_she_heaves_to_and_claws_off_a_lee_shore_by_turns(station_gale):
    """The doctrine's rows: a gale with sea room (the land to leeward beyond
    `sea_room_nm`) heaves her to; the land within `lee_shore_nm` to leeward while she lies
    to fills her away (on passage, then beating for the station to windward); the two
    thresholds apart (`no sea room` against `lee shore`) so that she does not heave to and
    fill away by turns at one line. She never takes the ground. The lead's finding on the
    way (docs/dev/TuningNotes.md, package 40c): between the turns she lies aback with no
    way for hours and is driven up-Channel at four knots, which is the ship's and the
    helm's to answer, not the captain's."""
    w = station_gale
    st = states(w)
    assert st[:5] == TRIAL_STATION_GALE_FIRST_STATES
    assert "beating" in {s for _, s in st}
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert [e.tick for e in w.log if e.kind == "ship.hove_to"]
    assert len(w.log) == TRIAL_STATION_GALE_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_GALE_DIGEST


TRIAL_STATION_LEE_SHORE_STATES = [
    (300, "keeping station"),
    (19440, "hove to for weather"),
    (37740, "on passage"),
    (37860, "beating"),
    (42900, "hove to for weather"),
    (45120, "on passage"),
    (45180, "beating"),
]
TRIAL_STATION_LEE_SHORE_LINES = 570
TRIAL_STATION_LEE_SHORE_DIGEST = "dca2273da941e096"


@pytest.fixture(scope="module")
def station_lee_shore():
    return trial("trial-station-lee-shore")


def test_with_ushant_under_her_lee_she_is_not_left_hove_to_onto_it(station_lee_shore):
    """Started five miles west of Ushant with a westerly gale coming on: hove to once she
    has sea room, filled away for the land under her lee, beating off, and never aground
    (the first trial grounded her in thirty-seven minutes on a course shaped for the
    island)."""
    w = station_lee_shore
    assert states(w) == TRIAL_STATION_LEE_SHORE_STATES
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert len(w.log) == TRIAL_STATION_LEE_SHORE_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_LEE_SHORE_DIGEST


# -- the merchant on her passage ----------------------------------------------------------

TRIAL_TRADE_STRANGER_STATES = [
    (300, "on passage"),
    (3660, "evading"),
    (8040, "on passage"),
    (34080, "at anchor"),
    (38160, "on passage"),
    (39720, "at anchor"),
]
TRIAL_TRADE_STRANGER_ANCHORED_TICKS = [34413, 40105]
TRIAL_TRADE_STRANGER_LINES = 1193
TRIAL_TRADE_STRANGER_DIGEST = "a04a80a960eabc53"


@pytest.fixture(scope="module")
def trade_stranger():
    return trial("trial-trade-stranger")


def test_the_merchant_hauls_off_from_a_privateer_and_waits_in_the_road_for_a_wind(trade_stranger):
    """A British schooner bound for Falmouth (the merchant's doctrine by her wardroom
    file's binding, a master commanding, whatever the muster says), a French brig-sloop
    within two miles: evading, hauling off every ten minutes until she is lost to sight,
    then on passage again; the pilot taken off Falmouth; and in pilot water a course the
    wind will not allow is not beaten (the first trial beat her onto the Black Rock): she
    comes to an anchor in the outer road and waits, the at-anchor book trying again on
    the flood by day; twice in this run, and at anchor at its end."""
    w = trade_stranger
    cap = w.captain
    assert cap.role == "merchant"
    assert states(w) == TRIAL_TRADE_STRANGER_STATES
    hauled = [e for e in w.log if "hauling off" in e.text and e.kind == "order.accepted"]
    assert len(hauled) >= 6
    anchored = [e.tick for e in w.log if e.kind == "ship.anchored"]
    assert anchored == TRIAL_TRADE_STRANGER_ANCHORED_TICKS
    waits = [e for e in w.log if "the wind does not serve to enter Falmouth" in e.text]
    assert len(waits) == 2
    assert cap.state == "at anchor" and cap.intent is not None and not cap.intent.done
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert len(w.log) == TRIAL_TRADE_STRANGER_LINES
    assert w.log.digest()[:16] == TRIAL_TRADE_STRANGER_DIGEST


TRIAL_TRADE_THICK_STATES = [
    (300, "on passage"),
    (300, "running for shelter"),
    (17220, "at anchor"),
]
TRIAL_TRADE_THICK_ANCHORED_TICK = 17669
TRIAL_TRADE_THICK_LINES = 539
TRIAL_TRADE_THICK_DIGEST = "10fee882c789666e"


@pytest.fixture(scope="module")
def trade_thick():
    return trial("trial-trade-thick")


def test_in_thick_weather_near_the_land_the_merchant_runs_for_the_road_and_waits(trade_thick):
    """Fog with the Lizard two leagues off by account (the land judged by the account on
    the chart in his hands, since the lookout sees none): running for shelter at his first
    judgement, the pilot taken, the anchor let go in the outer road, and there she stays
    while it is thick (the at-anchor book goes in only when the visibility is better than
    a mile; the first trial took her in through the fog and onto the Black Rock)."""
    w = trade_thick
    assert w.captain.role == "merchant"
    assert states(w) == TRIAL_TRADE_THICK_STATES
    assert [e.tick for e in w.log if e.kind == "ship.anchored"] == [TRIAL_TRADE_THICK_ANCHORED_TICK]
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert w.captain.state == "at anchor"
    assert len(w.log) == TRIAL_TRADE_THICK_LINES
    assert w.log.digest()[:16] == TRIAL_TRADE_THICK_DIGEST


# -- the player's hand (decision 41) ------------------------------------------------------


def intent_world(ticks: int = 21600) -> World:
    """The intent scenario with the schooner at sea: the tin bought, the Falmouth pilot
    taken out and put off (she heaves to for his boat at 10:21), the first leg shaped."""
    sf = load_scenario("data/scenarios/merchant-intent.yaml")
    world = make_scenario_world(sf)
    begin(world, sf)
    world.run(ticks)
    return world


def test_an_order_at_the_prompt_makes_the_captain_stand_aside_and_carry_on_gives_her_back():
    """On an intent scenario the player at the prompt is the captain: his first order of
    the ship's strikes the rules-based captain's book and he stands aside, said once; a
    reading or a station's sentence is not a hand; `captain: carry on` gives her back, his
    plan worked afresh; the scenario's opening orders before his first judgement are not
    a hand either (the intent scenario's digest stands)."""
    w = intent_world()
    cap = w.captain
    assert cap.commands and cap.state == "on passage"
    w.submit("the reckoning")
    assert cap.commands and not cap.aside
    e = w.submit("steer S")
    assert e.kind != "order.rejected"
    assert cap.aside and not cap.commands and cap.state is None
    aside = [x for x in w.log if x.kind == "captain.aside"]
    assert len(aside) == 1 and "stands aside at your order" in aside[0].text
    assert "'on passage' struck" in aside[0].text
    assert w.standing.books_loaded() == []
    w.run(1800)
    assert cap.aside and cap.state is None  # no judgement while he stands aside
    assert "standing aside" in w.readings["captain"]["words"]
    w.submit("steer SW")
    assert len([x for x in w.log if x.kind == "captain.aside"]) == 1  # said once
    from freesail.world.orders import apply, parse

    words, _ = apply(w, parse("captain: carry on"))
    assert "carries on" in words
    assert not cap.aside and cap.commands
    w.run(120)
    assert cap.state is not None
    # carry on when he is not aside, or with no intent, is refused in words
    with pytest.raises(Exception, match="not standing aside"):
        apply(w, parse("captain: carry on"))


def test_the_players_hand_replays_with_him_aside():
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    w = intent_world()
    w.submit("steer S")
    w.run(600)
    copy = replay_mod.replay(w.save(), ship_factory)
    assert copy.captain.aside and copy.log.digest() == w.log.digest()
