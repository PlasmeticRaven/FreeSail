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

# package 37p: chasing at 9240 and keeping station again at 9840 (7260 and 7980 before),
# within hail at 9798 (7972 before): the stranger made out half an hour later, the
# frigate by the wind under the period's trim (TuningNotes, package 37p)
# package 45: chasing at 9180 and the station again at 24660 (9240 and 9840 at 37p): by the
# wind under the helm's new rules she meets the brig differently, the chase's lead puts her
# across the brig's bows and the brig draws forward 145 degrees and to windward in the first
# half hour; she is never within hail and the chase is given up at 10:51 (the chase rule's
# own, said for the lead in docs/dev/TuningNotes.md, package 45)
# package 45c: the chase rule mended (the chaser's own way across the line of sight from her
# run between the bearings, the lead to seventy degrees, a crossed chase laid for her
# bearing again): chasing at 9180, within hail at 10423 and keeping station at 10440
# (never within hail and the station at 24660 at package 45; docs/dev/TuningNotes.md, 45c)
# package 43 (merged after 45c): the Palinure has a captain of her own (the cruiser's
# doctrine, brains.py): she investigates the frigate at 06:00, makes her out overmatched and
# hauls off at 06:36 as the frigate makes her out and chases (9360; 9180 at 45c, when she
# held her leg); the frigate gives the chase up at 18960, 09:16, under the new rule of a
# chase that has not gained a mile in three hours (`chase stale`; 45c's mended chase had her
# within hail at 10423 and back on the station at 10440 with a brig that did not run), and
# the brig is bound on her way and gone before the end
TRIAL_STATION_STRANGER_STATES = [
    (300, "keeping station"),
    (7200, "investigating a stranger"),
    (9360, "chasing"),  # 9180 at package 45c
    (18960, "keeping station"),  # 10440 at package 45c (24660 at 45)
]
TRIAL_STATION_STRANGER_WITHIN_HAIL_TICKS: list[int] = []  # [10423] at 45c; never at 45
TRIAL_STATION_STRANGER_LINES = 714  # package 43 (889 at package 45c, 972 at 45, 961 at 37p)
TRIAL_STATION_STRANGER_DIGEST = "9e0bc47304373987"  # package 43 (3c2aba8b08fd1f63 at 45c)


@pytest.fixture(scope="module")
def station_stranger():
    return trial("trial-station-stranger")


def test_the_station_is_to_seaward_of_its_place_and_the_stranger_is_chased(station_stranger):
    """`keep the station off Ushant within 15 miles`: the station mark is the point the
    radius from the island with the most sea room, to the westward (`captains.station_off`),
    never the island itself, which the first trial ran her onto; the stranger put on the sea
    by the director (with a captain of her own since package 43, who investigates the frigate
    and runs from her) is investigated, made out and chased, the chase given up when it has
    not gained a mile in three hours, and the station kept again, the books loaded and
    unloaded by name."""
    w = station_stranger
    cap = w.captain
    assert cap.role == "kings-ship" and cap.intent is not None and cap.intent.kind == "station"
    mark = cap._station_mark()
    assert mark is not None and mark[0] == "48 33.3 N 5 26.6 W"
    assert states(w) == TRIAL_STATION_STRANGER_STATES
    assert books(w)[:3] == ["keeping station", "investigating a stranger", "chasing"]
    hail = [e.tick for e in w.log if e.kind == "sail.within_hail"]
    assert hail[:1] == TRIAL_STATION_STRANGER_WITHIN_HAIL_TICKS
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert cap.state == "keeping station"
    assert len(w.log) == TRIAL_STATION_STRANGER_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_STRANGER_DIGEST


# package 37p: lying a-try from 19440 to 37740 (before, the land under her lee by 25860
# as she drove up-Channel aback, and hove to again at 26520), on passage and keeping
# station again at 37740 and 37860, the gale's second hove-to at 43320
# package 45: the station kept by the wind from 06:30 to 09:33 with Ushant within ten miles
# to leeward (no sea room: the land read over the whole lee sector), hove to at 19980 (19440
# at 37p), on passage and the station again at 30780 and 30900 (37740, 37860), hove to again
# 41880 (43320), on passage and beating from 51480; sail made again at 20:30 after the gale,
# and she is aback by turns for the hour before it (docs/dev/TuningNotes.md, package 45)
TRIAL_STATION_GALE_FIRST_STATES = [
    (300, "keeping station"),
    (19980, "hove to for weather"),
    (30780, "on passage"),
    (30900, "keeping station"),
    (41880, "hove to for weather"),
]
# package 45c: the first states as they were; sail made again by steps after the gale
# (topsails 18:27, masts, reefs and jib 20:30, plain sail 21:19), keeping station at 63720
TRIAL_STATION_GALE_LINES = 1429  # package 45c (1399 at package 45, 1423 at package 37p)
TRIAL_STATION_GALE_DIGEST = "94d2943d029d197d"  # package 45c (3f0d36bbff4af262 at 45)


@pytest.fixture(scope="module")
def station_gale():
    return trial("trial-station-gale")


def test_in_a_gale_with_sea_room_she_heaves_to_and_claws_off_a_lee_shore_by_turns(station_gale):
    """The doctrine's rows: a gale with sea room (the land to leeward beyond
    `sea_room_nm`) heaves her to; the land within `lee_shore_nm` to leeward while she lies
    to fills her away (on passage, then beating for the station to windward); the two
    thresholds apart (`no sea room` against `lee shore`) so that she does not heave to and
    fill away by turns at one line. She never takes the ground. The lead's finding on the
    way (docs/dev/TuningNotes.md, package 40c): between the turns she lay aback with no
    way for hours and was driven up-Channel at four knots. Since package 37p she lies
    a-try under the close-reefed main topsail and the storm staysails for five hours,
    drifting at a knot and a half over the ground, and is aback eleven minutes in the
    twenty hours, never three together."""
    w = station_gale
    st = states(w)
    assert st[:5] == TRIAL_STATION_GALE_FIRST_STATES
    assert "beating" in {s for _, s in st}
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert [e.tick for e in w.log if e.kind == "ship.hove_to"]
    assert len(w.log) == TRIAL_STATION_GALE_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_GALE_DIGEST


# package 37p: lying a-try from 19440 and on passage from 37740 to the end (before,
# beating at 37860, hove to again at 42900, on passage 45120 and beating 45180)
# package 45: hove to at 06:30 as the glass falls (the gale line a force sooner), and then
# by turns of the lee shore (Ushant within six miles over the lee sector) and the gale with
# sea room again, beating from 12:35 and sail made again after the gale (37p: hove to 19440,
# on passage 37740 to the end under the main topsail); never aground
# package 45c: lying a-try from 08:11 to 11:34 (the hove-to book's "under way again" no
# longer sets plain sail in thirty knots; at package 45 on passage at 23040, hove to again
# at 28500 and beating from 30900), then keeping station; sail made again by steps (topsails 14:45,
# reefs and jib 20:29 with the masts waiting for sea room, plain sail 20:44); never aground
TRIAL_STATION_LEE_SHORE_STATES = [
    (300, "keeping station"),
    (9000, "hove to for weather"),
    (11940, "on passage"),
    (12060, "keeping station"),
    (15060, "hove to for weather"),
    (27240, "on passage"),  # 23040 at package 45, then by turns to 30900
    (27300, "beating"),
    (27300, "keeping station"),
]
TRIAL_STATION_LEE_SHORE_LINES = 1665  # package 45c (2129 at package 45, 1668 at 37p)
TRIAL_STATION_LEE_SHORE_DIGEST = "fe10b699baf92229"  # package 45c (b7cbfbe33e2ed631 at 45)


@pytest.fixture(scope="module")
def station_lee_shore():
    return trial("trial-station-lee-shore")


def test_with_ushant_under_her_lee_she_is_not_left_hove_to_onto_it(station_lee_shore):
    """Started five miles west of Ushant with a westerly gale coming on: hove to once she
    has sea room, and never aground (the first trial grounded her in thirty-seven minutes
    on a course shaped for the island). Before package 37p she drove to leeward aback at
    four knots and was filled away for the land under her lee and beat off; since, she
    lies a-try at a knot and a third over the ground until the gale is done, the land
    never within the lee-shore line, and goes on passage after it."""
    w = station_lee_shore
    assert states(w) == TRIAL_STATION_LEE_SHORE_STATES
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert len(w.log) == TRIAL_STATION_LEE_SHORE_LINES
    assert w.log.digest()[:16] == TRIAL_STATION_LEE_SHORE_DIGEST


# -- the merchant on her passage ----------------------------------------------------------

# package 37p: on passage again at 8100 (8040), at anchor 33960 (34080) and 40980
# (39720), the bower let go at 34292 and 41307 (34413 and 40105)
# package 45 (item 3): at anchor within the port's reach she is in port and does her
# business from the road by the boat; the second anchorage of 37p (at anchor 33960, under
# way 38160 for the wind, at anchor again 40980) is not sought
# package 43 (merged after 45c): the Renard has a captain of her own (the cruiser's
# doctrine): she chases the schooner from 05:05 and gives the chase up at 08:05 (`chase
# stale`); the schooner hauls off until the brig is lost to sight at 08:58 (8100 at 45c,
# when the brig held a fixed course), is set back forty miles to the south-westward by it,
# beats up to Falmouth by turns from the forenoon, anchors in Carrick Road on the evening
# ebb at 19:23 and is in port at 19:24 (13:54 at 45c) -- and takes the ground at 21:48 (see
# the xfail below: the anchorage's let-go five minutes after its decision, with her way on
# into two fathoms of the chart). The states between 17880 and 18240 are 45c's beating rule
# and the passage rule trading the deck every two minutes as the evasion ends, for the lead.
TRIAL_TRADE_STRANGER_STATES = [
    (300, "on passage"),
    (3660, "evading"),
    (17880, "on passage"),  # 8100 at package 45c
    (18000, "beating"),
    (18120, "on passage"),
    (18240, "beating"),
    (39060, "on passage"),
    (44220, "beating"),
    (51720, "on passage"),
    (55440, "in port"),  # 35640 at package 45c (35340 at 45)
]
TRIAL_TRADE_STRANGER_ANCHORED_TICKS = [55413]  # [35630] at 45c ([35292] at 45)
TRIAL_TRADE_STRANGER_LINES = 1556  # package 43 (1176 at package 45c, 1170 at 45, 1252 at 37p)
# decision 45, the pilot's news: 0efa38e1d5d2f172 before; package 37p (a04a80a960eabc53 before)
TRIAL_TRADE_STRANGER_DIGEST = "f7ad5b1e06dd737e"  # package 43 (db253be58da059ca at 45c)


@pytest.fixture(scope="module")
def trade_stranger():
    return trial("trial-trade-stranger")


@pytest.mark.xfail(
    strict=True,
    reason="package 43: with a captain in the Renard the schooner is chased three hours, set "
    "forty miles to the south-westward, and comes into Carrick Road on the evening ebb; the "
    "anchorage's standing order decides to anchor at 19:18 over five fathoms of the chart and "
    "the bower is let go at 19:23 with her way on, over two, and she takes the ground aft on "
    "the ebb at 21:48 (ship.aground 64080); the states and the digest are pinned as the run "
    "gave them; for the lead (the anchoring's domain; docs/dev/TuningNotes.md, package 43)",
)
def test_the_merchant_hauls_off_from_a_privateer_and_waits_in_the_road_for_a_wind(trade_stranger):
    """A British schooner bound for Falmouth (the merchant's doctrine by her wardroom
    file's binding, a master commanding, whatever the muster says), a French brig-sloop
    within two miles (and a captain of her own since package 43, who chases for three hours
    and gives it up): evading, hauling off every ten minutes until she is lost to sight,
    then on passage again; the pilot taken off Falmouth; and in pilot water a course the
    wind will not allow is not beaten (the first trial beat her onto the Black Rock): she
    comes to an anchor in the outer road and is in port from it at the end."""
    w = trade_stranger
    cap = w.captain
    assert cap.role == "merchant"
    assert states(w) == TRIAL_TRADE_STRANGER_STATES
    hauled = [e for e in w.log if "hauling off" in e.text and e.kind == "order.accepted"]
    assert len(hauled) >= 6
    anchored = [e.tick for e in w.log if e.kind == "ship.anchored"]
    assert anchored == TRIAL_TRADE_STRANGER_ANCHORED_TICKS
    waits = [e for e in w.log if "the wind does not serve to enter Falmouth" in e.text]
    assert len(waits) == 0  # package 45: in port from the road, no wait to go in (2 before)
    assert cap.state == "in port" and cap.intent is not None  # at anchor before package 45
    assert len(w.log) == TRIAL_TRADE_STRANGER_LINES
    assert w.log.digest()[:16] == TRIAL_TRADE_STRANGER_DIGEST
    # last, so that the pins above are proved before the expected failure (package 43)
    assert not [e for e in w.log if e.kind == "ship.aground"]


# package 37p: at anchor at 17280 (17220), the bower let go at 17688 (17669)
# package 45 (item 3): at anchor in the outer road, within Falmouth's reach, she is in port
TRIAL_TRADE_THICK_STATES = [
    (300, "on passage"),
    (300, "running for shelter"),
    (14400, "at anchor"),  # 17280 at package 37p
    (14820, "in port"),
]
TRIAL_TRADE_THICK_ANCHORED_TICK = 14775  # package 45 (17688 at package 37p)
TRIAL_TRADE_THICK_LINES = 482  # package 45 (553 at package 37p)
# decision 45, the pilot's news: 50901cf162ea95aa before; package 37p (10fee882c789666e before)
# package 45c: every tick and the lines as they were; a line's words moved (the pilot's
# conn and the weather's sky, both this package's)
TRIAL_TRADE_THICK_DIGEST = "f39f5c6f393dd75d"  # package 45c (590cfb8f12834ac7 at 45)


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
    assert w.captain.state == "in port"  # package 45: the outer road is within Falmouth's reach
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
