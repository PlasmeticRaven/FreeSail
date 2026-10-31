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
# package 57: the chase given up at 18060, 09:01 (18960 before): her new rig aloft, and the
# brig's polar drawn from her file with Steel's staysails (docs/dev/TuningNotes.md, 57)
TRIAL_STATION_STRANGER_STATES = [
    (300, "keeping station"),
    (7200, "investigating a stranger"),
    (9360, "chasing"),  # 9180 at package 45c
    (18060, "keeping station"),  # package 57 (18960 at 43, 10440 at 45c, 24660 at 45)
]
TRIAL_STATION_STRANGER_WITHIN_HAIL_TICKS: list[int] = []  # [10423] at 45c; never at 45
# package 71: the King's brig makes the private signal to the Palinure once her colours are
# made out and reads no answer (a man of war's rig: the tell), thirty-one lines of the
# challenge and its reading; the states and the chase as before, proved by bisection
# (`signalling.CHALLENGES` off gives 756 and 9c24b2e01bb801e7 again)
# package 84, step 6 (the one clock): the Palinure's lookout reads the brig's hoists as flying by
# the game's tick, where her World's clock, counted from her promotion, stood behind the tick
# the private signal broke out at and never showed it her; she answers it now (a reply at
# 9840, one line more), the states, the books and the chase as before (TuningNotes, step 6)
TRIAL_STATION_STRANGER_LINES = 788  # package 84 step 6 (787 at 71; 756 at 56, the glass; 754 at 57)
TRIAL_STATION_STRANGER_DIGEST = "d56963daf49d566a"  # 84 step 6 (f8f4e544cc34b86e at 71)


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
# package 57: the course shaped at 300 allows the flood (she has way on by a hair, where
# before she had none to work the allowance by), and the day falls otherwise from there:
# hove to at 15060 (19980), on passage 30780, beating 31560 (the station 30900), hove to
# 32160 (41880); she lies to under the main staysail by the heavy-weather book short of the
# storm line both times (15944, 32161). Then beating from 37740 she is put about by 'the
# offing' among the islands of the Molène passage and twice will not wear under her
# close-reefed topsails and storm staysails in thirty knots ("Could not wear: she would
# not come round", 40681 and 42241), lies aback, is filled away full and by for her
# station by 'the leg', and takes the ground at 44332, La Helle two miles off, with land
# ahead called at six cables and two (43860, 44160), in distress at 44340. The xfail
# below; for the lead and package 58 (docs/dev/TuningNotes.md, package 57)
# package 58b (item 5, the gale book's mending; the judgement waits for the lead's
# playtest, so the pins below are left as they were and the trial an expected failure,
# the new figures beside the old): the fore topmast staysail is taken in at 8820 before it
# blows out (it blew out at 8983); lying a-try from 15060 she is never aback; filled away
# at 30780 she sets her close-reefed topsails and is not hove to again at 32160; beating
# for the station she is taken among the Molène islands by 'the offing' and takes the
# ground at 41415 (44332), in distress at 41460 (44340). The first states as they come now:
# 300 keeping station, 15060 hove to, 30780 on passage, 31560 beating, 41460 in distress
# (docs/dev/TuningNotes.md, package 58b)
# package 88 (item 2, the lead's ruling of 2026-10-30; the expected failure lifted by mending
# its cause): the room a wear takes read under her lee and the land ahead answered
# (`navigation.WEAR_ROOM`, `captains.DANGER_AHEAD`; with every package-88 switch off the trunk's
# figures come again: 1014 lines, aground 42394 among the Molène islands, in distress 42420).
# Keeping station in the forenoon she is tacked at 6721 and 7321 with Ushant two miles under
# her lee where she was worn, the day falls otherwise from there, and she never takes the
# ground: hove to 15060 as before, on passage 28560 and keeping station 28680 (on passage
# 30780 and beating 31560 before), hove to again 41880, on passage 49920 and beating from
# 50580 to the end. Filled away in 42 knots at 28560 she lies aback by turns for two hours
# (70 lines of it in the day, 23 before): 58b's gale book's ground, a finding in the notes.
TRIAL_STATION_GALE_FIRST_STATES = [
    (300, "keeping station"),
    (15060, "hove to for weather"),  # 19980 before package 57
    (28560, "on passage"),  # 30780 before package 88
    (28680, "keeping station"),  # beating 31560 before package 88
    (41880, "hove to for weather"),  # 32160 before 88 (41880 before package 57)
]
# package 45c: the first states as they were; sail made again by steps after the gale
# (topsails 18:27, masts, reefs and jib 20:30, plain sail 21:19), keeping station at 63720
# package 43b: the first states as they were; the beating book after the gale loaded at
# 52140, ten minutes later than at 51540 (the beating verdict's dwell), and the evening's
# tacks fall otherwise: she misses stays twice in plain sail after 18:00 and lies aback by
# turns for half an hour (36 lines of sails backed and filled, 4 before) before she wears
# package 58b: 864 lines and 4cb58e9ec1ab55c0, aground at 41415; the tree before it
# (872aa61) gives 857 and cefe2cf5136fb4d9, aground at 44332 (the pin was stale before 58b)
TRIAL_STATION_GALE_LINES = 1722  # package 88 (1014 on c168c51, aground 42394; 909 at 57)
TRIAL_STATION_GALE_DIGEST = "04f2fcd0fe9023a4"  # package 88 (93274bb5f658a34f on c168c51)


@pytest.fixture(scope="module")
def station_gale():
    return trial("trial-station-gale")


# package 57 to package 88 an expected failure: she took the ground among the islands of the
# Molène passage after the offing's and the leg's wears (44332 at 57, 41415 at 58b, 42394 on
# the merged tree of 58a, 67, 68 and 58b and on c168c51); lifted by package 88's mend of
# the cause, the wear with no room under her lee and the land ahead unanswered at night
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
    twenty hours, never three together. Since package 88 she is tacked and never worn with
    the land within the room a wear takes under her lee, puts about for the land on her bow
    or a danger ahead by the chart, and never takes the ground; filled away in the gale's
    tail she lies aback by turns for two hours (70 lines in the day), 58b's gale book's
    ground, said in the notes."""
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
    (9720, "hove to for weather"),  # 9000 before package 57
    (11940, "on passage"),
    (12060, "keeping station"),
    (15060, "hove to for weather"),
    # package 57: on passage and the station again at 30780 and 30840 (27240 and 27300),
    # hove to again at 41880, on passage and beating from 51480, and the station at 68940:
    # lying to longer under her new rig, never aground (docs/dev/TuningNotes.md, 57)
    (30780, "on passage"),  # 27240 at 43b, 23040 at package 45, then by turns to 30900
    # package 43b: beating and keeping station in the one minute at 27300 before, the
    # beating rule's two verdicts by turns; the verdict's dwell leaves the station alone
    (30840, "keeping station"),  # 27300 at 43b
    # the lead's judgement of 58b's gale book (2026-10-24), read from the trials' logs and not
    # played live (the owner's ruling): hove to again at 41940 (41880 at 57), the station at
    # 71340 (68940); the book lies her to never aback, and the expected failure is lifted
    # package 88 (items 1 and 2; every package-88 switch off gives the old list again): boxed
    # off at 12514 and 15157 by the recovery where she lay aback with sternway in the gale's
    # first hours (9 lines aback in the day, 29 before), hove to again at 32160, on passage,
    # beating and the station at 38340 and 38400, hove to at 41880 (41940 before), beating
    # from 51540 to the end (the station at 71340 before); put about for the land on her bow
    # by night, where under item 1 alone she stood on onto the Four at 61021; never aground
    (32160, "hove to for weather"),
    (38340, "on passage"),
    (38400, "beating"),
    (38400, "keeping station"),
    (41880, "hove to for weather"),  # 41940 before package 88
    (51480, "on passage"),
    (51540, "beating"),  # keeping station at 71340 before package 88
]
# the lead at the merge of 58a and 58b (2026-10-23): 58a's figure was 1669 "4720693ca65bc67b"
# package 58b (item 5, the gale book's mending; the judgement waits for the lead's
# playtest, so the pins are left as they were and the trial an expected failure, the new
# figures beside the old): filled away at 30780 with the gale's tail still blowing she sets
# her close-reefed topsails and has way, where she lay aback every three minutes under the
# storm canvas alone until 37800 (aback 19 minutes in the day, 41 before); hove to again at
# 41940 (41880), on passage and beating at 51480 and 51540 as before, keeping station at
# 71340 (68940); never aground; 1597 lines and ed48ca3d61e52f20
# package 88: 1561 lines and 6e88e97cbdffac7b; the trunk before it (c168c51) gives 1597 and
# 7fad0ce7e46ba366, its pinned ed48ca3d61e52f20 stale before this package (the lead to
# measure the trunk's figure in the cloud: a digest is the build machine's)
TRIAL_STATION_LEE_SHORE_LINES = 1561  # package 88 (1597 at 58b, judged 2026-10-24; 57: 1669)
TRIAL_STATION_LEE_SHORE_DIGEST = "6e88e97cbdffac7b"  # 88, the builder's container; the cloud
# 1ecbc08a61efb132 on the merged tree (ed48ca3d61e52f20 at 58b, stale); not asserted, see the test


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
    # the digest is not asserted (the lead at package 88's merge, 2026-10-31): a digest is
    # the machine's, and this trial's differs by machine with the states and the line count
    # the same (the cloud 1ecbc08a61efb132, the builder's container 6e88e97cbdffac7b);
    # the states, the grounding and the lines are the pins
    assert len(w.log.digest()) >= 16  # the digest is read, for the figure in a failure's log


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
# ebb at 19:23 and is in port at 19:24 (13:54 at 45c) -- and took the ground at 21:48 (the
# anchorage's let-go five minutes after its decision, with her way on into two fathoms of
# the chart; an xfail at package 43).
# package 43b: the beating rule one rule with a band and a dwell (`_course_verdict`): the
# four changes of state in six minutes at 08:58 are gone, and the beats fall otherwise
# (beating 31740 to 38340 and 44880 to 56340, against 18000 to 39060 and 44220 to 51720);
# she comes into Carrick Road later, at 19:41, and lets go in fifteen fathoms and a half
# (the let-go's cast, also 43b, is not wanted there), in port at 19:42; never aground, and
# the xfail lifted. The stand-back the cast brings is proved on this trial's old shoal in
# tests/test_anchor.py.
# package 57: the brig-sloop's polar drawn from her file with Steel's staysails stowed;
# the beats fall a minute or two otherwise (31680 to 38460 and 44940 on, against 31740 to
# 38340 and 44880 to 56340) and she comes to an anchor in Carrick Road at 57324, 19:55,
# at anchor at 57000 and in port at 57360 (in port at 56520 from her way into the road)
# package 58b (items 1 and 2, by bisection: the tree with both turned off gives every old
# figure): the brig's own captain lays his chasing leg again for the stream (her course in
# her own World's log), so the schooner's hauling-off marks fall a tenth of a minute
# otherwise from 15660; on passage she lays her leg again for the stream at 19680 and
# beats from 20400, on passage 22980, beating 31620, on passage 37560, is brought to for a
# cast of the deep-sea lead off the Lizard at 40740, beats from 46140, and comes to the
# outer road of Falmouth at 53040 with the wind foul to go in, lets go at 53669 in
# eighteen fathoms and a half and is in port from the road at 53700 (docs/dev/TuningNotes.md,
# package 58b). The old figures beside each.
# package 88 (items 1 and 2 with the lead's ruling of 2026-10-30; the switches
# `captains.ABACK_RECOVER`, `navigation.WEAR_ROOM`, `captains.DANGER_AHEAD` and
# `captains.ENGAGING_CHASE_STALE` all off give every old figure below again): taken aback at
# 368 (04:06), she lay with a knot or two of sternway for fifty-four minutes until she turned
# to evade at 3660; the captain's recovery boxes her off at 840 and she makes four knots by
# 04:16, so the French brig meets her at 14580 (08:03), not 05:01; her haul-off now keeps the
# sea (it steered the reciprocal across the land about Coverack and grounded her under item 1
# alone), and the brig, engaging her two to four miles astern and never in gunshot, gives the
# stale chase up after three hours (34200); she never fires. The recovery and the longer
# evasion cost her the port: at the twentieth hour she is on passage eleven miles from
# Falmouth by account, where before she anchored in the outer road at 51849 and was in port
# at 51900 (docs/dev/TuningNotes.md, package 88). The old figures beside each.
TRIAL_TRADE_STRANGER_STATES = [
    (300, "on passage"),
    (14580, "evading"),  # 3660 before package 88
    (34200, "on passage"),  # 18300 before 88 (17880 at 58b; 8100 at package 45c)
    (36720, "beating"),  # 19020 before 88 (20400 at 58b; 31680 at 57, 31740 at 43b)
    (66000, "on passage"),  # before 88: on passage 37380, beating 45600, at anchor 51240
    # and in port 51900 (53040 at anchor and 53700 in port at 58b; 57360 at 57)
]
# package 58b ([57324] at 57, [56498] at 43b, [55413] at 43)
TRIAL_TRADE_STRANGER_ANCHORED_TICKS: list[int] = []  # 88 ([51849] at 70; [53669] at 58b)
# package 71: the French brig's cruiser doctrine makes the private signal to the schooner
# (one line, her lookout's), and the brig's chase goes about for a chase on the other side
# of the wind's eye (`navigation.CHASE_TACKS_FOR_HER`, three lines fewer); every state and
# the anchor at 51849 as at 70, proved by bisection (the switches off give 1248 and
# 0a480f7a4b7f321a again)
# package 73: the butcher's bill said once after the brig's fire ("nobody hurt"), and the
# brig-sloop's captain serving out the small arms on entering the action, so that her fire on
# the schooner falls differently (the same lines, other texts); docs/dev/TuningNotes.md, 73
TRIAL_TRADE_STRANGER_LINES = 1594  # package 88 (1247 at 73; 1246 at 71; 1248 at 70; 1407 at 58b)
# decision 45, the pilot's news: 0efa38e1d5d2f172 before; package 37p (a04a80a960eabc53 before)
# package 43b on the merged tree with 44: every tick and line as on 43b's branch, a line's
# words 44's (acd7581476d8ee74 on 43b's branch)
# the lead at the merge of 58a and 58b (2026-10-23): 58a's figure was "9eb41044fc6e9907"
# package 56, the glass: 7b8012b076ebea42 (e73870448a788eac at 57)
# the merged tree of 58a and 58b (2026-10-23): 58b alone gave 5bbca78fdc6b5093; the digest reads
# severity, and 58a's recurring lines are routine in this passage too
# package 84, step 6 (the one clock): the butcher's bill at 20220, ten minutes after the brig's
# last shot by the game's tick; at 17520 before, the shot's tick written by the brig's World's
# clock, counted from her promotion and behind the game's (TuningNotes, step 6)
TRIAL_TRADE_STRANGER_DIGEST = (
    "bf059c3211b7cc9c"  # package 88 (02313d83240a11d5 at 84 step 6; 11b8a45bdc8c935a at 73)
)


@pytest.fixture(scope="module")
def trade_stranger():
    return trial("trial-trade-stranger")


def test_the_merchant_hauls_off_from_a_privateer_and_waits_in_the_road_for_a_wind(trade_stranger):
    """A British schooner bound for Falmouth (the merchant's doctrine by her wardroom
    file's binding, a master commanding, whatever the muster says), a French brig-sloop
    within two miles (and a captain of her own since package 43, who chases for three hours
    and gives it up): evading, hauling off every ten minutes until she is lost to sight,
    then on passage again; the pilot taken off Falmouth; and in pilot water a course the
    wind will not allow is not beaten (the first trial beat her onto the Black Rock): she
    comes to an anchor in the outer road and is in port from it at the end. Since package 88
    she is recovered from lying aback at the start, meets the brig three hours later, and at
    the twentieth hour is on passage for Falmouth, eleven miles off, never aground and never
    taken (the port's hour what the recovery and the longer evasion cost her; the lead's
    ruling of 2026-10-30)."""
    w = trade_stranger
    cap = w.captain
    assert cap.role == "merchant"
    assert states(w) == TRIAL_TRADE_STRANGER_STATES
    hauled = [e for e in w.log if "hauling off" in e.text and e.kind == "order.accepted"]
    assert len(hauled) >= 6
    anchored = [e.tick for e in w.log if e.kind == "ship.anchored"]
    assert anchored == TRIAL_TRADE_STRANGER_ANCHORED_TICKS
    waits = [e for e in w.log if "the wind does not serve to enter Falmouth" in e.text]
    # package 45: in port from the road, no wait to go in (2 before); package 58b: she comes
    # to the outer road beating with the wind foul to go in and anchors there for it (the
    # tide's words at 57000 before), in port from the road as at 45; package 70: fired into
    # and run clear, she comes to the road an hour earlier, the wind foul to go in, and waits
    # for it as at 58b; package 88: not at the road within the twenty hours (one wait before)
    assert len(waits) == 0
    # package 70: the brig's fire; package 88: met later and never in gunshot, she gives the
    # stale chase up unfired (fired into at 17362 before)
    assert not [e for e in w.log if e.kind == "action.fired_at"]
    assert not getattr(w.ship, "struck", False)
    # in port before package 88 (at anchor before package 45): on passage for Falmouth now
    assert cap.state == "on passage" and cap.intent is not None
    assert len(w.log) == TRIAL_TRADE_STRANGER_LINES
    assert w.log.digest()[:16] == TRIAL_TRADE_STRANGER_DIGEST
    assert not [e for e in w.log if e.kind == "ship.aground"]  # package 43b: no xfail


# package 37p: at anchor at 17280 (17220), the bower let go at 17688 (17669)
# package 45 (item 3): at anchor in the outer road, within Falmouth's reach, she is in port
# package 58b (items 1 and 2, by bisection: both turned off give every old figure, either
# alone does not): running for shelter in the fog she is brought to for a cast of the
# deep-sea lead inside the hundred-fathom line at 3900 and filled away at 4800, her leg laid
# again for the stream, and comes to the outer road earlier, at anchor at 12540 and the
# bower let go at 12850 in thirteen fathoms, in port at 12900 (docs/dev/TuningNotes.md,
# package 58b). The old figures beside each.
TRIAL_TRADE_THICK_STATES = [
    (300, "on passage"),
    (300, "running for shelter"),
    (12540, "at anchor"),  # 14400 at 45 (17280 at package 37p)
    (12900, "in port"),  # 14820 at 45
]
TRIAL_TRADE_THICK_ANCHORED_TICK = 12850  # package 58b (14775 at 45, 17688 at package 37p)
TRIAL_TRADE_THICK_LINES = 426  # package 58b (489 at 56, the glass; 482 at 45)
# decision 45, the pilot's news: 50901cf162ea95aa before; package 37p (10fee882c789666e before)
# package 45c: every tick and the lines as they were; a line's words moved (the pilot's
# conn and the weather's sky, both this package's)
# package 56, the glass: ce964d9f346034de (7915dc59337bd31d at 44); package 68 (item 1,
# riding): every tick and line the same, the account run while she came to her anchor at
# 14775 and was not yet brought up: the noon's longitude by account in its data moves in
# the fifth decimal (-5.03015 to -5.03016); the old rule restored gives the old digest
# package 68, riding: 3c2b220e06496db5 (ce964d9f346034de)
TRIAL_TRADE_THICK_DIGEST = "cfa538b19cb0d2fe"  # package 58b (3c2b220e06496db5 at 68)


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
