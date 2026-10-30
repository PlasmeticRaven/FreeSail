"""Ports (spec M5 §23; package 35): Falmouth, Plymouth and Brest as places with a
pilot, roads and a mooring, a boat's landing, a market, a yard or the chandlers, a crew
pool and a stance toward each nation, each a file of `data/ports/` on one machinery.

**Arriving** is a sequence the log tells and the readings carry. When a ship is under
way in a port's pilot's cruising ground by day, the pilot cutter (32b's cutter at far
detail, `freesail.world.ships`) comes off from the port's quay and closes her; the
lookout sights her as he sights anything ("Sail ho!", a bearing first, her rig as she
nears); within hail she hails for a pilot, and within two cables, the ship under easy
sail, the pilot comes aboard as a person (`freesail.world.people`) with his skill, his
words (the channel, the marks, the anchorage, when the tide serves: his tide is the
port's own, which he knows as a man who lives by it, the one way the world's tide
reaches the captain, through a person; decision 30) and the port's news; the cutter
lies to under the lee and goes back. A port **closed** to the ship's nation refuses her
in the pilot's words from the cutter (truth 70); a **hostile** port sends no pilot. Then
the anchorage, the boat and the shore. **Leaving** is the reverse: `get under way` as
Luce has it (`freesail.evolutions.scripts.GetUnderWayScript`), the pilot's course out,
and the pilot off into his cutter beyond the outer road, his certificate signed and the
pilotage paid from the purse (the Regulations of 1806, the Pilot's articles).

**The pilot taken or declined** (package 37h; the owner's rulings of 5 and 7 October
2026, decisions 35 and 36; the review of gate 5c, G10). The boat's hail asks her to
shorten sail when she is too fast for him to board, and on its second hail to heave to,
and never asks a ship at anchor for either. `take the pilot` answers it (she shortens
sail or heaves to as the hail asked, and the boat keeps company, a cable and a half off
at the ship's own pace, until he can board); `decline the pilot` sends the boat back to
her station; `hail the pilot` hails a boat in sight and takes him. Unanswered, the boat
keeps company, hails once more after `PILOT_HAIL_AGAIN_S` and bears away for her
station, and the line says so: no pilot boards a ship that has not taken him. Aboard he
is a carrier of the truth of his own water: within his port's ground he warns of a
charted danger ahead on her true track, by name, and of the water where it shoals, on
which hand the deeper water lies (`Ports._warn`, from `chart.Chart.dangers_ahead` and
`shoal_ahead`, never a reading); in thick weather he says once that he cannot see his
marks and warns by the lead and the time run, nearer and without the bearing. He does not
con and does not converse beyond `ask the pilot` (the director's, milestone 6). He is
put off at the anchor in his port's anchorage or mooring, or outward a mile beyond the
outer road, and asks for his boat once; the pilotage is paid from the purse at his port's
rate as he goes, and the log says so.

**The boat** (`send the boat ashore`, `data/evolutions/send_boat.yaml`) is a passage by
distance at a boat's pace with hands and time, hoisted out and in, carrying a person, a
message or a purchase; what it brings back comes aboard at the gangway and reaches the
captain where he is through the messenger and the door (truth 68). **The market** is a
list of goods with a price each that moves by a small rules table (`Market.price`:
the season by the month, the war by the nations table, the supply by what has been sold
to the port and bought from it); `buy <n> tons of <good>` and `sell` go by the boat and
move the hold (from the ship file through the generator) and the purse; `the prices` are
known once the boat has been ashore and the purser has brought the list off (a paper,
`freesail.world.places.Papers`). **The dockyard** supplies a spar, a suit of sails,
cordage, water and provisions with a time and a cost against the ship's stores (the
frigate's from the King's yard by demand and survey, the schooner's from the chandlers
at a price). **The crew pool** gives hands by rating at a bounty and a delay, mustered
into the crew of milestone 3 with names from the muster's own lists.

**A port's state** (package 39d; spec M6 §26): a port is `open` or `blockaded`. A
blockaded port names its blockaders (`blockade: by:`), where their ships keep their
station and when the blockade began, from its file or from the scenario's `ports:` entry,
which may lay a blockade or lift one (`state: open`). What it means to a stance
(`Nations.stance`): the port is closed to the blockaders' enemies, its own nation's
ships among them, whose pilot will not take them in past the squadron, and whose trade,
yard and hands are shut to them as any closed port's; to the blockaders and the rest its
stance is the table's. It is watched by the blockaders' ships: `Ports.blockades()` lists
each blockaded port with its blockaders and their station, the one place 6c's world's
business reads to put the squadron on its station and to stop and search what comes
(nothing here moves a ship), and `the port` says it. The prize court, the neutral turned
away and the squadron itself are 6c's and milestone 7's.

Every constant below names its source or says judgement; the prices in the port files
are from memory and the files say so. Everything here is a function of the seed and
the journal: the pilot's name is drawn from the `people` stream, the recruits' from
`recruits`; a replay has them again, and a checkpoint holds the whole.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.world import ordnance
from freesail.world.geo import Position, bearing_and_distance
from freesail.world.people import Message

__all__ = [
    "BOAT_ASHORE_S",
    "BOAT_HOIST_IN_S",
    "BOAT_HOIST_OUT_S",
    "BOAT_PACE_KN",
    "IN_PORT_NM",
    "PILOT_AGAIN_H",
    "PILOT_BOARDS_UNDER_KN",
    "PILOT_BOARDS_WITHIN_M",
    "PILOT_COMPANY_M",
    "PILOT_HAIL_AGAIN_S",
    "PILOT_HAIL_WITHIN_M",
    "PILOT_LIES_TO_S",
    "PILOT_OFF_BEYOND_NM",
    "PILOT_STANDS_OUT_KN",
    "PILOT_THICK_AHEAD_S",
    "PILOT_THICK_NM",
    "PILOT_UNDER_KEEL_M",
    "PILOT_WAITS_SAY_S",
    "PILOT_WARN_ABEAM_M",
    "PILOT_WARN_AGAIN_S",
    "PILOT_WARN_AHEAD_S",
    "PILOT_WARN_MIN_M",
    "PORTS_DIR",
    "SUPPLY_CAP",
    "SUPPLY_FLOOR",
    "SUPPLY_PER_TON",
    "SUPPLY_RECOVERY_PER_DAY",
    "WAR_FACTOR",
    "BoatState",
    "Dockyard",
    "Good",
    "Job",
    "Market",
    "PilotSpec",
    "Port",
    "Ports",
    "Spot",
    "load_port",
    "port_files",
]

PORTS_DIR = Path(__file__).resolve().parents[2] / "data" / "ports"

# -- the pilot and his cutter (judgement throughout; no page times a pilot's boarding) --
# The cutter runs alongside within two cables and the pilot boards from her boat.
PILOT_BOARDS_WITHIN_M = 2.0 * units.CABLE
# He boards with the ship under easy sail: over this speed over the ground the cutter
# hails her to shorten sail and keeps company (judgement: a pilot's boat alongside a
# frigate at eight knots is a drowned pilot).
PILOT_BOARDS_UNDER_KN = 6.0
# Within four cables the cutter hails.
PILOT_HAIL_WITHIN_M = 4.0 * units.CABLE
# The cutter comes off to a ship with way on her, a knot through the water or more (a
# ship drifting under bare poles is not making for the port).
PILOT_COMES_OFF_OVER_KN = 1.0
# A port whose pilot refused her, or left her, is not tried again for six hours.
PILOT_AGAIN_H = 6.0
# The cutter lies to under the lee ten minutes after the boarding, then goes back.
PILOT_LIES_TO_S = 600
# Outward bound the pilot leaves her a mile beyond the outer road (the Regulations: the
# captain's certificate names the port or channel he conducted her out of).
PILOT_OFF_BEYOND_NM = 1.0
# -- the hail answered (package 37h; decisions 35 and 36): judgement throughout --
# Unanswered, the boat hails once more ten minutes after her first hail and bears away
# for her station ten minutes after that (judgement: time enough to answer a boat and
# shorten sail, and no longer than a pilot would hang on a ship that will not answer).
PILOT_HAIL_AGAIN_S = 600
# Hailed, the boat keeps company a cable and a half off, within the two cables he boards
# from (`ships.Vessel`'s `company` leg, at the ship's pace).
PILOT_COMPANY_M = 1.5 * units.CABLE
# A pilot who came aboard inward is put off at the anchor; he asks for his boat beyond the
# outer road only if she stands out to sea again with this much way on her, not as she
# drifts or forereaches hove to (judgement).
PILOT_STANDS_OUT_KN = 3.0
# Keeping company with a ship too fast for him to board, the boat says what she waits for,
# at most once in ten minutes (the review of gate 5c, G10: "a line from the pilot cutter
# saying what she waits for").
PILOT_WAITS_SAY_S = 600
# -- his warnings (package 37h; the owner's ruling of 7 October 2026: "He may warn of the
# shoal water or shore ahead with true knowledge in his water"); judgement throughout --
# He looks ten minutes' run ahead on her true track, and three cables at the least: a
# mile at six knots, time enough to stay or wear a ship or to anchor her.
PILOT_WARN_AHEAD_S = 600
PILOT_WARN_MIN_M = 3.0 * units.CABLE
# A danger her track passes within a cable of (beyond its own extent) is one he names.
PILOT_WARN_ABEAM_M = units.CABLE
# Shoal water is less than a fathom under her keel at the tide's height now.
PILOT_UNDER_KEEL_M = units.fathoms_to_m(1.0)
# He names each danger once while he is aboard, and the shoal water at most once in ten
# minutes.
PILOT_WARN_AGAIN_S = 600
# In thick weather, the visibility under a mile, he cannot see his marks (the owner's
# ruling: "Thick weather means he cannot see his marks"): he says so once, and warns by the
# lead and the time run, five minutes' run ahead and without the bearing.
PILOT_THICK_NM = 1.0
PILOT_THICK_AHEAD_S = 300
# At anchor within two miles of the port's roads or mooring she is in port: the boat
# goes ashore, the market and the yard serve her.
# A pilot's boat standing out for a ship she cannot catch gives her up beyond this many
# times the port's cruising ground from the station (package 45; judgement: a boat
# cruising six miles off follows a ship twelve, and no farther).
PILOT_LETS_GO_FACTOR = 2.0

# The pilot's fix (package 45, Part B item 2a; the owner's wardroom run: aground on the
# Fillettes with the account and its doubt nowhere near them after a cast of the lead
# moved the account, the pilot aboard). Aboard, within his port's ground and with his
# marks in sight (the visibility a mile or more), he has her by his marks: the account
# is brought to the truth every five minutes with a cable's doubt, said once; in thick
# weather he fixes nothing and warns by the lead and the time run as before (37h).
PILOT_FIX_EVERY_S = 300
PILOT_FIX_SIGMA_NM = 0.1

# The pilot's conn (package 45, Part B item 2c; `let the pilot take her in`): he conns
# her along his port's track by the conning words, the helm given a course by compass for
# each mark from where she truly is (he knows his water), the course corrected when the
# mark's bearing has drawn half a point from it, a mark passed within two cables; at the
# anchorage he says where to let go and his conn is done. His orders go under a rule's
# actor (not journaled, a deterministic function of the conn given).
PILOT_CONN_MARK_M = 2.0 * units.CABLE
# How far from the line to his mark the pilot lays her off to pass a danger on it (radians;
# package 45): two points, which at the warning distance of eight cables is three cables
# off the line, past a rock's warning berth (`PILOT_WARN_ABEAM_M`). Judgement.
PILOT_CONN_KEEP_OFF_RAD = 2.0 * units.POINT
PILOT_CONN_TURN_RAD = units.POINT / 2.0
# A danger is on his line when the line passes within its own extent and this much more
# (package 45c; judgement: none beyond the extent, a cable for a point rock).
PILOT_CONN_ON_THE_LINE_M = 0.0
# He cons her for a point on his leg this far ahead of where she is abreast of it (package
# 45c; judgement: a ship's turning circle and a half, a minute and a half at five knots).
PILOT_CONN_AHEAD_M = 2.0 * units.CABLE
# He cons her no nearer the wind than she lies close-hauled and this much more, full and by
# (package 45c; judgement: half a point, so that she is kept full with the yards braced up).
PILOT_LIE_MARGIN_RAD = 0.5 * units.POINT
# A course of his this many points from her head has the yards trimmed to it at his word
# (package 45c; judgement: a turn the old trim will not carry).
PILOT_TRIM_POINTS = 2.0
PILOT_TRIM_EVERY_S = 120  # once for a turn, not at each minute's order of it (judgement)
# He allows for the stream across his line, reckoning her way at no less than this and the
# allowance at no more than three points (package 45c; judgement: a vessel under sail in
# a tideway, and the most a pilot would lay her off his line).
PILOT_STREAM_WAY_KN = 3.0
PILOT_STREAM_MOST_RAD = 3.0 * units.POINT
PILOT_ACTOR = "standing order 'the pilot'"
# The set allowed for before his turn (package 43b; 45c's open item 1, the owner's wardroom
# save from 113000 and 114000: on a flood with the wind at NW the leg from the Goulet's
# second mark to its third, NE, could not be made good, the stream's allowance capped and
# she as near as she would lie, and the flood set her bodily across it onto the Mingan): a
# pilot who knows the next leg will not be made good under this wind with the stream on her
# bow takes his turning mark high, to the side the stream sets from, by as much as she will
# sag over the leg, so that her course made good from there runs down onto his next mark;
# no more than `PILOT_TURN_HIGH_MOST_M` off the mark (judgement: three cables, the width of
# the Goulet's pass between the north shore and the Mingan), and only into water she has
# under her with a fathom beneath her keel, on a clear line from the leg's start.
PILOT_TURN_HIGH_MOST_M = 3.0 * units.CABLE
PILOT_TURN_HIGH_LEAST_RAD = math.radians(3.0)
# He reckons the next leg a point closer to the wind than she lies now: the wind of the
# owner's save drew a point ahead (WNW to NW) in the quarter of an hour between his taking
# up the leg to his turning mark and her coming to it (judgement: a point, the wind's
# wander of a gusty day).
PILOT_SET_WIND_MARGIN_RAD = units.POINT
# The conn's design (package 45c; the owner's refinement of 2026-10-15): a pilot's conn is
# promised only along his track from the pilot station inward, leg by leg. Boarding
# elsewhere he first cons her to join it: at the nearest leg she is already inside of
# (within `PILOT_LEG_INSIDE_M` of it, between its marks), else at the station by a joining
# leg laid with the captain's planner (`captains.Planner.clear` and its rounds about a
# headland), with his own offing and berth in his own water where the planner's are the
# sea's (a league off the shore would never let him join a road under the land): two
# cables and a half off the shore and a cable off a charted danger (judgement: the
# warning's own berth, `PILOT_WARN_ABEAM_M`, and as far again off the shore for the set).
# Where no clear joining leg is found within the planner's rounds he says so, and takes
# her only from the station. At the station itself (within `PILOT_AT_STATION_M`) he takes
# her from there. Elsewhere he joins his track at the first mark of it ahead of her that a
# clear line reaches, the station or one beyond it, and not back at the station astern.
PILOT_LEG_INSIDE_M = 3.0 * units.CABLE
PILOT_AT_STATION_M = 4.0 * units.CABLE
PILOT_JOIN_OFFING_NM = 0.25
PILOT_JOIN_BERTH_NM = 0.1
# The pilot's conn in a stream (package 58b, item 6; package 68's debt, its item 19: with
# the wind over the water, his NE legs inside Bertheaume could not be laid on a four-knot
# flood under a north-westerly, and he had no answer but to pinch, onto the Mingan, or to
# go back for a mark astern). He judges each leg of his track ahead before he takes her
# into it, with the stream his water has on it and the wind over that water: a leg she
# lies is makable; one nearer the wind than she lies is makable while the course she makes
# good on it sags off it by less than `PILOT_SAG_LEAST_RAD`, or her sagging track runs
# clear (water a fathom beneath her keel all along it, and no danger within
# `PILOT_WARN_ABEAM_M` of it with less water than she draws). A leg that is not makable is
# not stood into: he brings her up where she is, in no more than `PILOT_WAIT_MOST_FATHOMS`
# by the chart, says why and the hour he looks for the stream to serve (the slack, found by
# looking ahead `PILOT_WAIT_AHEAD_S` at a time to `PILOT_WAIT_HORIZON_H` with the wind as it
# stands), or the wind, if no stream of the next tide serves; he looks again every
# `PILOT_WAIT_LOOK_S`, and when the legs serve he weighs and takes her in. In deeper water
# he cons her as before, as near as she will lie, and says that he cannot bring her up.
# And a turn of `PILOT_TRIM_POINTS` toward the wind has the yards trimmed for it first and
# the helm put over `PILOT_TRIM_FIRST_S` later (from 114000, his five-point turn to NNE
# with the yards for the wind on the quarter laid her aback in a minute). Judgement
# throughout: a point's sag is the most a turning mark taken high covers in his short legs;
# five and twenty fathoms, as the Éclair rode in two and twenty off Fréhel; five minutes, his
# look at the water; ten minutes, the steps of his reckoning of the tide; seven hours, past
# the next slack.
PILOT_SAG_LEAST_RAD = units.POINT
PILOT_WAIT_MOST_FATHOMS = 25.0
PILOT_WAIT_LOOK_S = 300
PILOT_WAIT_AHEAD_S = 600
PILOT_WAIT_HORIZON_H = 7.0
PILOT_TRIM_FIRST_S = 60
PILOT_JUDGE_WAY_KN = 4.0  # her way through the water as he reckons a leg (judgement)
PILOT_WEIGH_AHEAD_S = 1800  # he judges the stream for her under way in half an hour (judgement)
PILOT_COMMITTED_S = 2700  # weighed for the slack, he does not bring her up again so soon
PILOT_WAIT_WEIGH_S = 2700  # a weighing not come in three quarters of an hour is given up
PILOT_WAIT_REFUSED_S = 1800  # his weigh refused, he asks again in half an hour

IN_PORT_NM = 2.0
# -- the boat (judgement) --
# A boat's crew pull four knots on an errand (no page times a boat's crew; a man-of-war's
# cutter double-banked did better for a spurt and worse over an hour).
BOAT_PACE_KN = 4.0
# Hoisting a boat out with the yard and stay tackles, and in again (Luce 1866, 'Boats',
# 'Hoisting out boats' gives the sequence; the time is judgement).
BOAT_HOIST_OUT_S = 300
BOAT_HOIST_IN_S = 300
# The business ashore by errand, seconds: a letter left or fetched, the purser's turn
# round the market for the prices, a passenger landed, a purchase weighed and carted to
# the quay, a draft of recruits brought down (judgement).
BOAT_ASHORE_S = {
    "message": 1800,
    "prices": 1800,
    "person": 900,
    "purchase": 3600,
    "sale": 3600,
    "yard": 1800,
    "recruits": 1800,
    # package 53: a person landed to stay ashore, or taken off from the quay where he waits
    "landing": 300,
    "fetch": 300,
}
# Goods bought or sold go between the quay and the ship by the port's lighter, not by
# the boat's trips: three minutes a ton (twenty tons an hour, judgement; the boat itself
# carries under a ton), added to the boat's time ashore.
LIGHTER_S_PER_TON = 180
# -- the market's rules table (judgement; docs/dev/TuningNotes.md, package 35) --
# supply: each ton sold to the port lowers its price by this fraction, each ton bought
# from it raises it the same, between a floor and a cap; the glut or the want clears by
# a seventh a day (a week).
SUPPLY_PER_TON = 0.01
SUPPLY_RECOVERY_PER_DAY = 1.0 / 7.0
SUPPLY_FLOOR = 0.5
SUPPLY_CAP = 2.0
# war: a good whose origin is a nation the port's own is at war with is dearer by half
# (the smuggler's premium on French brandy in Cornwall; judgement in the figure).
WAR_FACTOR = 1.5
# Prices are given to the half pound, as a clerk's list.
PRICE_ROUND = 0.5
# The recruits come off by the boat in a draft once the delay is up.
RECRUIT_RATINGS = ("able", "ordinary", "landsman")


# ---------------------------------------------------------------------------
# The port as data
# ---------------------------------------------------------------------------


@dataclass
class Spot:
    """A place of the port on the chart: the roads, the mooring, the quay."""

    name: str
    position: Position
    depth_m: float | None = None
    bottom: str = ""
    feature_id: str = ""
    deep_draught_ft: float | None = None  # a ship drawing more goes to the anchorage instead

    @property
    def depth_words(self) -> str:
        from freesail.world.chart import fathoms_words

        return "no depth given" if self.depth_m is None else fathoms_words(self.depth_m)


@dataclass
class PilotSpec:
    station: str
    cruising_nm: float
    by_night: bool
    cutter_file: str
    names: tuple[str, ...]
    skill: float
    fee_pounds: float
    cast: str
    course_out_deg: float
    words: dict[str, str]
    # what comes off for the pilot when it is not the cutter (package 35b's files, read by
    # package 36): {kind: a gig, name: the St Mary's pilots' gig, under: oars and a lugsail}
    vessel: dict[str, Any] = field(default_factory=dict)

    @property
    def craft(self) -> str:
        """'cutter', 'gig', 'boat': the word the log uses for what comes off."""
        kind = str(self.vessel.get("kind") or "a cutter")
        return kind.removeprefix("a ").removeprefix("an ").removeprefix("the ") or "cutter"


@dataclass
class Good:
    good: str
    price: float
    origin: str | None
    season: dict[int, float]
    note: str = ""


@dataclass
class Market:
    """The port's goods and the rules that move their prices."""

    currency: str
    goods: dict[str, Good]
    net_sold: dict[str, float] = field(default_factory=dict)  # tons sold to the port, less bought
    settled_tick: int = 0  # when the supply last recovered a day's worth

    def recover(self, tick: int) -> None:
        """The glut or the want clears by `SUPPLY_RECOVERY_PER_DAY` each day."""
        days = (tick - self.settled_tick) / 86400.0
        if days < 1.0:
            return
        whole = int(days)
        self.settled_tick += whole * 86400
        keep = (1.0 - SUPPLY_RECOVERY_PER_DAY) ** whole
        self.net_sold = {g: t * keep for g, t in self.net_sold.items() if abs(t * keep) > 0.01}

    def factors(
        self, good: Good, when: datetime, nations: Any, port_nation: str
    ) -> dict[str, float]:
        season = float(good.season.get(when.month, 1.0))
        war = (
            WAR_FACTOR
            if good.origin and nations is not None and nations.at_war(good.origin, port_nation)
            else 1.0
        )
        supply = 1.0 - SUPPLY_PER_TON * self.net_sold.get(good.good, 0.0)
        supply = min(SUPPLY_CAP, max(SUPPLY_FLOOR, supply))
        return {"season": season, "war": war, "supply": supply}

    def price(self, name: str, when: datetime, nations: Any, port_nation: str) -> float:
        good = self.goods[name]
        f = self.factors(good, when, nations, port_nation)
        raw = good.price * f["season"] * f["war"] * f["supply"]
        return max(PRICE_ROUND, round(raw / PRICE_ROUND) * PRICE_ROUND)

    def listing(self, when: datetime, nations: Any, port_nation: str) -> list[tuple[str, float]]:
        return [(name, self.price(name, when, nations, port_nation)) for name in self.goods]

    def find(self, words: str) -> Good | None:
        key = " ".join(str(words).lower().replace("-", " ").split())
        for name, good in self.goods.items():
            if key in (name, name + "s", name.rstrip("s")):
                return good
        return None

    def sold_to_port(self, name: str, tons: float) -> None:
        self.net_sold[name] = self.net_sold.get(name, 0.0) + float(tons)

    def bought_from_port(self, name: str, tons: float) -> None:
        self.net_sold[name] = self.net_sold.get(name, 0.0) - float(tons)


@dataclass
class YardItem:
    item: str
    hours: float = 0.0
    pounds: float = 0.0
    pounds_per_100m2: float = 0.0
    pounds_per_fathom: float = 0.0
    hours_per_ton: float = 0.0
    pounds_per_ton: float = 0.0
    hours_per_day: float = 0.0
    pounds_per_man_day: float = 0.0
    note: str = ""


@dataclass
class Dockyard:
    kind: str  # "yard" (the King's, by demand) or "chandlers" (at a price)
    items: dict[str, YardItem]

    def find(self, words: str) -> YardItem | None:
        key = " ".join(str(words).lower().replace("-", " ").replace("_", " ").split())
        for name, item in self.items.items():
            if key in (name.replace("_", " "), name, "a " + name.replace("_", " ")):
                return item
        if key in ("spar", "a spar", "topmast", "a topmast"):
            return self.items.get("topmast")
        if key in ("sails", "sail", "a suit of sails", "suit of sails", "canvas"):
            return self.items.get("suit of sails")
        if key in ("rope", "cordage", "hemp"):
            return self.items.get("cordage")
        return None


@dataclass
class Port:
    id: str
    name: str
    nation: str
    source: str
    outer_road: Spot
    anchorage: Spot
    mooring: Spot
    shore: Spot
    pilot: PilotSpec
    tide: dict[str, Any]
    market: Market
    dockyard: Dockyard
    crew_pool: dict[str, dict[str, float]]
    closed_to: list[str] = field(default_factory=list)
    letters: list[Message] = field(default_factory=list)  # waiting at the port for the ship
    news: list[str] = field(default_factory=list)  # what the pilot tells, beside the wars
    path: str = ""
    # The port's tracks (spec M6 §4; package 40), for the rules-based captain's planner:
    # `to_sea`, the marks from the outer road to the open sea; `from_sea`, the marks from
    # the common track to the outer road; `in`, from the outer road to the anchorage.
    # Each mark a feature by its id or a position pricked on the chart, in the directions'
    # words; a port without them is approached by its outer road and anchorage alone.
    tracks: dict[str, list[str]] = field(default_factory=dict)
    # The port's reach (package 45, Part B item 3c): at anchor within this many miles of
    # its roads or mooring she is in port and does her business by the boat (`reach_nm`
    # in the file; `IN_PORT_NM` by default: Falmouth's outer road and Carrick Road are
    # both within two miles of the town, the road of Bertheaume eight miles from Brest).
    reach_nm: float = IN_PORT_NM
    # A port's state (package 39d; spec M6 §26): "open", or "blockaded" with `blockade`,
    # {"by": nation, "station": Position | None, "station_name", "since", "source"}. Plain
    # class defaults, so a checkpoint written before them loads (`core.replay`).
    state: str = "open"
    blockade: dict[str, Any] | None = None
    # The port's own places ashore beside every port's (package 53; spec M7b §14;
    # `places.port_places`): `places:` in the file, each {id, name, done, found, roles}. A
    # plain class default, so that a checkpoint from before loads.
    places: tuple[dict[str, Any], ...] = ()
    # The port's blockade station (package 72; spec M7 §22): `blockade_station:` in the file,
    # {feature, within_nm, source}, the inshore squadron's station off the port's approach
    # that the intent `blockade <port>` reads (the road itself lies behind the land from
    # seaward: Bertheaume behind Saint-Mathieu). None: the outer road. A plain class
    # default, so that a checkpoint from before loads.
    blockade_station: dict[str, Any] | None = None
    # The port's powder and shot (practice and resupply, between packages 72 and 73; the
    # build design's §1.3): `ordnance:` in the file as `world.ordnance.parse_block` reads it,
    # the storekeeper of the Ordnance or the merchants; None: none to be had. A plain class
    # default; a port pickled before it has none of its own, and `ordnance.block_of` reads
    # its file once.
    ordnance: dict[str, Any] | None = None
    # The port's nation by date (package 79d; 79a's dated form): the file's `nation:` as a
    # list of {nation, since, until}, Genoa the Ligurian Republic's until the annexation of
    # June 1805 and France's after; `nation` is the entry in force on the scenario's first
    # day, `nation_on` the entry for a day. Empty for a port of one nation. A plain class
    # default, so that a checkpoint from before loads.
    nations: tuple[dict[str, Any], ...] = ()

    def nation_on(self, when: datetime | date | None) -> str:
        """The port's nation on a day: its dated entry for the day, else `nation`."""
        return _dated_nation(self.nations, when) or self.nation

    @property
    def blockaded_by(self) -> str | None:
        """The blockaders' nation, or None when the port is open."""
        if self.state != "blockaded" or not self.blockade:
            return None
        return str(self.blockade.get("by") or "") or None

    def spots(self) -> list[Spot]:
        return [self.outer_road, self.anchorage, self.mooring]

    def mooring_for(self, draught_m: float) -> Spot:
        """Where she moors: the inner harbour, or the anchorage when she draws too much."""
        deep = self.mooring.deep_draught_ft
        if deep is not None and units.m_to_feet(draught_m) > deep:
            return self.anchorage
        return self.mooring

    def nearest_spot(self, pos: Position) -> tuple[Spot, float]:
        best = None
        for spot in self.spots():
            _, d = bearing_and_distance(pos, spot.position)
            if best is None or d < best[1]:
                best = (spot, d)
        assert best is not None
        return best[0], best[1] / units.NAUTICAL_MILE


def _beyond_the_leg(a: Position, b: Position, p: Position) -> bool:
    """Whether `p` is beyond the leg's end `b` along the line from `a` (package 45c);
    False for a leg shorter than a cable."""
    if bearing_and_distance(a, b)[1] < units.CABLE:
        return False
    return _off_the_leg(a, b, p)[1] >= 1.0


def _wind_from_over_the_water(world: Any, wind: Any) -> float:
    """Where the wind comes from over the water at her (radians true): the true wind less
    the stream's set, the wind her sails feel and her close-hauled angle is counted from
    (package 68, item 19: in the Goulet's flood of four knots toward the east, the wind at
    NW over the ground is a point and more nearer north over the water, and the pilot's
    "as near as she will lie" laid by the wind over the ground had her sails lifting and
    the flood setting her onto the Mingan). The wind over the ground itself where there is
    no stream."""
    from freesail.physics.integrate import water_velocity

    ship = getattr(world, "ship", None)
    wx, wy = water_velocity(ship) if ship is not None else (0.0, 0.0)
    if wx == 0.0 and wy == 0.0:
        return float(wind.direction_from)
    vx, vy = wind.vector_at_height(10.0)
    ax, ay = vx - wx, vy - wy
    if math.hypot(ax, ay) < 1e-9:
        return float(wind.direction_from)
    return units.wind_direction_from(ax, ay)


def _off_the_leg(a: Position, b: Position, p: Position) -> tuple[float, float]:
    """How far `p` lies off the leg from `a` to `b` (metres, on the flat at its latitude)
    and how far along it, as a share of the leg (0 at `a`, 1 at `b`)."""
    dx, dy = a.offset_to(b)
    px, py = a.offset_to(p)
    length2 = dx * dx + dy * dy
    if length2 < 1.0:
        return math.hypot(px, py), 0.0
    share = (px * dx + py * dy) / length2
    return abs(px * dy - py * dx) / math.sqrt(length2), share


def port_files(root: Path = PORTS_DIR) -> dict[str, Path]:
    return {p.stem: p for p in sorted(root.glob("*.yaml"))}


def load_port(
    path: str | Path,
    chart: Any = None,
    state: dict[str, Any] | None = None,
    when: datetime | date | None = None,
) -> Port:
    """A port from its file, its spots placed from the chart's features where the file
    names one (`feature:`), else from its own latitude and longitude; `state` is the
    scenario's for this port (closures, letters waiting, news)."""
    p = Path(path)
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    where = str(p)

    def spot(key: str) -> Spot:
        raw = doc.get(key) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"{where}: '{key}' is not a mapping")
        fid = str(raw.get("feature") or "")
        feature = chart.feature(fid) if chart is not None and fid else None
        if feature is not None:
            pos = feature.position
            depth = (
                units.fathoms_to_m(float(feature.depth_fathoms))
                if feature.depth_fathoms is not None
                else None
            )
            bottom = feature.bottom
        else:
            if raw.get("lat_deg") is None or raw.get("lon_deg") is None:
                if fid:
                    raise ValueError(
                        f"{where}: '{key}' names the feature '{fid}', which the chart has not, "
                        "and gives no lat_deg and lon_deg"
                    )
                raise ValueError(f"{where}: '{key}' gives no feature and no lat_deg and lon_deg")
            pos = Position(float(raw["lat_deg"]), float(raw["lon_deg"]))
            depth = None
            bottom = ""
        if raw.get("depth_fathoms") is not None:
            depth = units.fathoms_to_m(float(raw["depth_fathoms"]))
        if raw.get("bottom"):
            bottom = str(raw["bottom"])
        name = str(raw.get("name") or (feature.name if feature is not None else key))
        deep = raw.get("deep_draught_ft")
        return Spot(name, pos, depth, bottom, fid, None if deep is None else float(deep))

    pr = doc.get("pilot") or {}
    pilot = PilotSpec(
        station=str(pr.get("station") or ""),
        cruising_nm=float(pr.get("cruising_nm", 6.0)),
        by_night=bool(pr.get("comes_off_by_night", False)),
        cutter_file=str(pr.get("cutter") or "data/ships/cutter.yaml"),
        names=tuple(str(n) for n in (pr.get("names") or ["the pilot"])),
        skill=float(pr.get("skill", 0.9)),
        fee_pounds=float(pr.get("fee_pounds", 0.0)),
        cast=str(pr.get("cast") or "starboard"),
        course_out_deg=float(pr.get("course_out_deg", 180.0)),
        words={str(k): str(v) for k, v in (pr.get("words") or {}).items()},
        vessel={str(k): v for k, v in (pr.get("vessel") or {}).items()},
    )
    mk = doc.get("market") or {}
    goods: dict[str, Good] = {}
    for g in mk.get("goods") or []:
        season = {int(k): float(v) for k, v in (g.get("season") or {}).items()}
        goods[str(g["good"])] = Good(
            str(g["good"]), float(g["price"]), g.get("origin"), season, str(g.get("note", ""))
        )
    market = Market(str(mk.get("currency") or "pounds"), goods)
    dy = doc.get("dockyard") or {}
    items = {}
    for it in dy.get("items") or []:
        name = str(it["item"])
        items[name] = YardItem(
            item=name,
            hours=float(it.get("hours", 0.0)),
            pounds=float(it.get("pounds", 0.0)),
            pounds_per_100m2=float(it.get("pounds_per_100m2", 0.0)),
            pounds_per_fathom=float(it.get("pounds_per_fathom", 0.0)),
            hours_per_ton=float(it.get("hours_per_ton", 0.0)),
            pounds_per_ton=float(it.get("pounds_per_ton", 0.0)),
            hours_per_day=float(it.get("hours_per_day", 0.0)),
            pounds_per_man_day=float(it.get("pounds_per_man_day", 0.0)),
            note=str(it.get("note", "")),
        )
    dockyard = Dockyard(str(dy.get("kind") or "chandlers"), items)
    pool = {
        str(k): {kk: float(vv) for kk, vv in (v or {}).items()}
        for k, v in (doc.get("crew_pool") or {}).items()
    }
    state = state or {}
    closed = [str(x) for x in (doc.get("closed_to") or [])]
    closed += [str(x) for x in (state.get("closed_to") or []) if str(x) not in closed]
    port_state, blockade = _port_state(doc, state, where)
    letters = []
    for letter in state.get("letters") or []:
        if isinstance(letter, str):
            letters.append(Message(letter, str(doc.get("name") or p.stem)))
        else:
            letters.append(
                Message(
                    str(letter.get("text") or ""),
                    str(letter.get("origin") or doc.get("name") or p.stem),
                    str(letter.get("to") or "captain"),
                )
            )
    nations = _nations(doc.get("nation"), where)
    return Port(
        reach_nm=float(doc.get("reach_nm", IN_PORT_NM)),
        id=str(doc.get("id") or p.stem),
        name=str(doc.get("name") or p.stem),
        nation=(
            (_dated_nation(nations, when) or nations[0]["nation"])
            if nations
            else str(doc.get("nation") or "")
        ),
        nations=nations,
        source=str(doc.get("source") or ""),
        outer_road=spot("outer_road"),
        anchorage=spot("anchorage"),
        mooring=spot("mooring"),
        shore=spot("shore"),
        pilot=pilot,
        tide=dict(doc.get("tide") or {}),
        market=market,
        dockyard=dockyard,
        crew_pool=pool,
        closed_to=closed,
        letters=letters,
        news=[str(x) for x in (state.get("news") or [])],
        path=where,
        tracks={str(k): [str(m) for m in (v or [])] for k, v in (doc.get("tracks") or {}).items()},
        state=port_state,
        blockade=blockade,
        places=tuple(dict(x) for x in (doc.get("places") or []) if isinstance(x, dict)),
        blockade_station=(
            dict(doc["blockade_station"]) if isinstance(doc.get("blockade_station"), dict) else None
        ),
        ordnance=ordnance.parse_block(doc.get("ordnance"), where),
    )


PORT_STATES = ("open", "blockaded")


def _nations(raw: Any, where: str) -> tuple[dict[str, Any], ...]:
    """A port's dated nations (package 79d): `nation:` as a list of {nation, since, until}
    (ISO dates, either open), in the order given; () for the one word."""
    if not isinstance(raw, list):
        return ()
    out = []
    for entry in raw:
        if not isinstance(entry, dict) or not entry.get("nation"):
            raise ValueError(f"{where}: each entry of a dated nation gives its nation")
        dates = {
            k: (v if isinstance(v, date) or v is None else date.fromisoformat(str(v)))
            for k in ("since", "until")
            for v in [entry.get(k)]
        }
        out.append({**entry, "nation": str(entry["nation"]), **dates})
    return tuple(out)


def _dated_nation(nations: tuple[dict[str, Any], ...], when: datetime | date | None) -> str:
    """The dated entry in force on a day ('' for none, or no day): `since` and `until`
    both counted in, as the business's dated blockades are (`business._within`)."""
    if when is None:
        return ""
    day = when.date() if isinstance(when, datetime) else when
    for entry in nations:
        if entry["since"] and day < entry["since"]:
            continue
        if entry["until"] and day > entry["until"]:
            continue
        return str(entry["nation"])
    return ""


def _port_state(
    doc: dict[str, Any], state: dict[str, Any], where: str
) -> tuple[str, dict[str, Any] | None]:
    """A port's state from its file, the scenario's entry for the port over it (package
    39d): `state:` open or blockaded, and for a blockade `blockade:` with `by` (the
    blockaders' nation, required), `station` (where their ships keep it: lat_deg, lon_deg
    and a name), `since` and `source`. A scenario's `state: open` lifts the file's
    blockade; its `blockade:` keys go over the file's."""
    word = str(state.get("state") or doc.get("state") or "open")
    if word not in PORT_STATES:
        raise ValueError(f"{where}: state '{word}' is not one of {', '.join(PORT_STATES)}")
    if word != "blockaded":
        return word, None
    raw = {**dict(doc.get("blockade") or {}), **dict(state.get("blockade") or {})}
    if not raw.get("by"):
        raise ValueError(f"{where}: a blockaded port names its blockaders (blockade: by:)")
    station = raw.get("station") or {}
    pos = (
        Position(float(station["lat_deg"]), float(station["lon_deg"]))
        if station.get("lat_deg") is not None and station.get("lon_deg") is not None
        else None
    )
    return word, {
        "by": str(raw["by"]),
        "station": pos,
        "station_name": str(station.get("name") or ""),
        "since": str(raw.get("since") or ""),
        "source": str(raw.get("source") or ""),
    }


# ---------------------------------------------------------------------------
# The ports of one World
# ---------------------------------------------------------------------------


@dataclass
class BoatState:
    """The ship's boat on an errand, as data (a checkpoint holds it)."""

    away: bool = False
    boat_id: str = ""
    boat_name: str = "the boat"
    errand: str = ""
    port_id: str = ""
    carrying: list[dict[str, Any]] = field(default_factory=list)  # what goes ashore
    bringing: list[dict[str, Any]] = field(default_factory=list)  # what comes back
    phase: str = ""
    since_tick: int = 0
    people: list[str] = field(default_factory=list)  # person ids in the boat
    # package 53 (spec M7b §14): the people she lands to stay ashore, and the people she
    # takes off from the quay, by id; plain class defaults, so a checkpoint from before loads
    landing: tuple[str, ...] = ()
    fetching: tuple[str, ...] = ()

    def words(self) -> str:
        if not self.away:
            return f"{self.boat_name} at the booms"
        return f"{self.boat_name} away {_errand_words(self.errand)}, {self.phase}"


@dataclass
class Job:
    """Something the port does for the ship in its own time: the yard's spar, the
    recruits' draft. Data only, applied by kind when due (`Ports._apply_job`)."""

    due_tick: int
    kind: str
    port_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    words: str = ""
    # the hull the job is for (package 84, step 3): set by her `Dealings` when she makes it;
    # "" in a checkpoint from before, hers by the list it is in
    hull: str = ""


# The names of a hull's dealings (`freesail.world.dealings.Dealings`), refused on the
# world's `Ports` in words that say where they live (package 84, step 3).
DEALINGS_NAMES: frozenset[str] = frozenset(
    (
        "_aground",
        "_along_the_leg",
        "_anchoring",
        "_apply_job",
        "_as_she_will_lie",
        "_bear_away",
        "_boat_back",
        "_boat_in_sight",
        "_boat_kept",
        "_bring_up_to_wait",
        "_clear_line",
        "_conn",
        "_conn_keep_off",
        "_conn_off",
        "_conn_order",
        "_cutter",
        "_fix",
        "_for_the_stream",
        "_foul_leg",
        "_ground_speed_kn",
        "_ground_velocity",
        "_hail",
        "_hail_reset",
        "_in_hand",
        "_joined_track",
        "_land_and_take_off",
        "_launch_cutter",
        "_leg_made",
        "_legs_judged",
        "_made_good_on",
        "_muster_recruits",
        "_note_lay_in",
        "_passengers",
        "_people_back",
        "_pilot_boards",
        "_pilot_leaves",
        "_put_off_at_anchor",
        "_record",
        "_send_boat",
        "_stream_at",
        "_stream_turn",
        "_tick_pilot",
        "_tide_words",
        "_track_marks",
        "_turn_high",
        "_under_sail",
        "_wait_at_anchor",
        "_waiting_words",
        "_waits",
        "_warn",
        "_water_for",
        "_way_kn",
        "_write_price_list",
        "answer",
        "answer_pilot",
        "boat",
        "boat_phase",
        "boat_reading",
        "boat_spec",
        "boats_words",
        "conn",
        "conn_bearing",
        "conn_heading",
        "conn_i",
        "conn_inward",
        "conn_order_tick",
        "conn_track",
        "cutter_errand",
        "cutter_hailed",
        "cutter_id",
        "cutter_port",
        "declined_until",
        "demand",
        "enter_hands",
        "fetch_person",
        "fix_said",
        "fix_tick",
        "give_conn",
        "hail_answer",
        "hail_count",
        "hail_tick",
        "hail_wants",
        "in_port",
        "inward_track",
        "land_person",
        "lay_in",
        "nearest",
        "nearest_by_account",
        "no_prices_words",
        "pilot",
        "pilot_boat_asked",
        "pilot_inward",
        "pilot_port",
        "pilot_reading",
        "pilot_since",
        "pilot_words",
        "port_words",
        "price_lists",
        "prices_reading",
        "send_boat",
        "ship_nation",
        "shoal_warned_tick",
        "stance_of_hers",
        "take_conn_back",
        "thick_said",
        "tick",
        "to_shore_m",
        "trade",
        "trade_list",
        "trade_together",
        "waiting_words",
        "warned",
        "waterman",
    )
)


class Ports:
    """**The ports of the world** (package 84, step 3; the design's §2.4): the port files
    and their state, loaded by the scenario's `ports:` (every file of `data/ports/` when
    the world has a chart and the scenario says nothing), their markets, yards, pools,
    places and blockades, a port's stance toward a nation, the nearest port to a place, and
    the jobs of every hull. One for the game, on `world.ports`, shared by every World of it
    (a crewed ship's World is given its parent's). What a ship does with a port, her pilot
    and his conn, the cutter sent for her, her boat and its errands, her price lists, her
    bargains and the hands she enters, is her `Dealings` (`freesail.world.dealings`, on
    `world.dealings`), which read these. A name of the dealings read here is refused in
    words naming where it lives."""

    def __init__(self, world: Any) -> None:
        self.world = world
        self.ports: dict[str, Port] = {}
        self._load()

    # -- loading -----------------------------------------------------------------------

    # -- loading -----------------------------------------------------------------------

    def _load(self) -> None:
        world = self.world
        wanted = getattr(world.scenario, "ports", None)
        files = port_files()
        states: dict[str, dict[str, Any]] = {}
        if wanted is None:
            ids = list(files) if world.chart is not None else []
        elif isinstance(wanted, dict):
            ids = list(wanted)
            states = {str(k): dict(v or {}) for k, v in wanted.items()}
        else:
            ids = [str(x) for x in wanted]
        for pid in ids:
            path = files.get(pid)
            if path is None:
                raise ValueError(
                    f"no port file for '{pid}' in {PORTS_DIR} (the ports are {', '.join(files)})"
                )
            self.ports[pid] = load_port(
                path, world.chart, states.get(pid), getattr(world.scenario, "start_time", None)
            )

    # -- the ports against a place and a nation ---------------------------------------------

    def stance(self, port: Port, nation: str) -> str:
        """The port's stance toward a ship of the nation: the nations' table over the
        port's closures and its blockade (`Nations.stance`)."""
        # package 79d: a port of dated nations by the world's day (Genoa's annexation)
        port_nation = port.nation_on(self.world.clock.ship_time) if port.nations else port.nation
        return self.world.nations.stance(
            port_nation, str(nation), port.closed_to, blockaded_by=port.blockaded_by
        )

    def nearest_to(
        self, pos: Position | None, within_nm: float | None = None
    ) -> tuple[Port, float] | None:
        """The nearest port by its roads to a place, and the miles to them; None beyond
        `within_nm` or with no place."""
        if pos is None or not self.ports:
            return None
        best = None
        for port in self.ports.values():
            _, d = port.nearest_spot(pos)
            if best is None or d < best[1]:
                best = (port, d)
        if best is None or (within_nm is not None and best[1] > within_nm):
            return None
        return best

    def in_port_at(self, pos: Position | None) -> Port | None:
        """The port a ship lying at a place is in: within the port's reach (`Port.reach_nm`,
        `IN_PORT_NM` by default) of its roads or mooring; the caller says whether she is at
        anchor."""
        found = self.nearest_to(pos)
        if found is None:
            return None
        port, d_nm = found
        return port if d_nm <= port.reach_nm else None

    def to_shore_from(self, pos: Position | None, port: Port) -> float:
        return bearing_and_distance(pos, port.shore.position)[1] if pos is not None else 0.0

    def blockades(self) -> list[dict[str, Any]]:
        """The blockaded ports of this World and who watches each (package 39d): the
        port, the blockaders' nation, their station and its name, as data for 6c's
        world's business to read; nothing here moves a ship."""
        out = []
        for port in self.ports.values():
            by = port.blockaded_by
            if by is None or port.blockade is None:
                continue
            out.append(
                {
                    "port": port.id,
                    "by": by,
                    "station": port.blockade.get("station"),
                    "station_name": port.blockade.get("station_name", ""),
                    "since": port.blockade.get("since", ""),
                }
            )
        return out

    def watched_by(self, port: Port) -> str | None:
        """The nation whose ships watch the port: its blockaders, or None."""
        return port.blockaded_by

    def find(self, words: str) -> Port | None:
        key = " ".join(str(words).lower().split()).removeprefix("the ")
        for port in self.ports.values():
            if key in (port.id, port.name.lower()):
                return port
        return None

    def news_words(self, port: Port) -> str:
        parts = list(port.news)
        wars = self.world.nations.wars_words()
        parts.append(wars[:1].upper() + wars[1:] + ".")
        return " ".join(parts)

    def places_lines(self, port: Port) -> list[str]:
        """The port's places in words, with the people of the world ashore at each."""
        from freesail.world.movement import ashore_at
        from freesail.world.places import port_place_lines

        there: dict[str, list[str]] = {}
        # the persons of the world as they stand, every hull's, without mustering anyone
        # for a reading (a world in which nobody has moved is as it was; package 84, step 2
        # and 3: the registry's persons, a company not yet built adding none)
        registry = getattr(self.world, "registry", None)
        if registry is not None:
            everyone = registry.persons()
        else:
            people = self.world.people
            everyone = people.people if getattr(people, "_built", True) else []
        for p in everyone:
            if not p.aboard and p.where == "shore" and p.port == port.id:
                there.setdefault(ashore_at(self.world, p), []).append(p.name)
        # the things lying there (package 53b), in nobody's keeping
        from freesail.world.things import lying_ashore, lying_words

        lying = {
            k: [lying_words(t) for t in v] for k, v in lying_ashore(self.world, port.id).items()
        }
        return port_place_lines(port, there, lying)

    def price_of(self, port: Port, good: str) -> float:
        world = self.world
        port.market.recover(world.clock.tick)
        return port.market.price(good, world.clock.ship_time, world.nations, port.nation)

    # -- the hulls' dealings, and their jobs ------------------------------------------------

    def dealings_all(self) -> list[Any]:
        """Every hull's dealings in this world: the World's own and each crewed ship's."""
        world = self.world
        out = []
        own = getattr(getattr(world, "own", None), "dealings", None)
        if own is not None:
            out.append(own)
        for v in getattr(getattr(world, "vessels", None), "vessels", None) or []:
            crew = getattr(v, "crew", None)
            d = getattr(getattr(crew, "own", None), "dealings", None)
            if d is not None and d not in out:
                out.append(d)
        return out

    @property
    def jobs(self) -> list[Job]:
        """The jobs of every hull (the yard's, the pool's, the lighter's, the hoy's, the
        waterman's), each with the hull it is for (`Job.hull`): a view in the hulls'
        order; a job is added through its hull's dealings."""
        out: list[Job] = []
        for d in self.dealings_all():
            out.extend(d.jobs)
        return out

    def tick(self) -> None:
        """The world's ports' tick, once a tick of the World that owns them: nothing yet
        (the markets recover as they are read; each hull's dealings tick in her World's
        tick, her jobs with them). The place for the sleeping hulls' jobs (step 5)."""
        return None

    def __getattr__(self, name: str) -> Any:
        if name in DEALINGS_NAMES:
            raise AttributeError(
                f"`Ports` is the world's; `{name}` is a hull's dealing: read it on "
                f"`world.dealings` (`freesail.world.dealings.Dealings`)"
            )
        raise AttributeError(name)


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def _possessive(name: str) -> str:
    """'Falmouth's', and 'St Mary's' as it stands (package 35b: a port named for a saint
    is a possessive already, and 'St Mary's's market' is no clerk's English)."""
    return name if name.endswith(("'s", "’s")) else f"{name}'s"


# The words of a boat's errand after 'with', which name no passenger (package 68).
_ERRAND_WORDS = (
    "letter",
    "message",
    "dispatch",
    "despatch",
    "water",
    "provisions",
    "cask",
    "prices",
    "news",
    "yard",
    "recruits",
    "hands",
    "goods",
    "money",
    "purse",
    "list",
)

# A waterman's boat from the quay (package 68; the cold review of 2026-10-22, R-62: one
# boat for all the port's business, and the captain waited an hour and forty minutes for
# her): his pull is reckoned at this speed between the ship and the quay, and five minutes
# to shove off and to come alongside (judgement), and his fare is a shilling a head
# (judgement on the period's watermen's fares; no port's data gives its own yet).
WATERMAN_KN = 2.5
WATERMAN_TURN_S = 300
WATERMAN_FARE_POUNDS = 0.05


def _after(text: str, leads: tuple[str, ...]) -> str:
    for lead in leads:
        i = text.find(lead)
        if i >= 0:
            rest = text[i + len(lead) :].strip()
            for stop in (" for ", " to ", " with "):
                j = rest.find(stop)
                if j > 0:
                    rest = rest[:j]
            return rest.strip(" .")
    return ""


def _errand_words(errand: str) -> str:
    return {
        "prices": "for the prices and what news there is",
        "message": "with a letter",
        "person": "for the prices and what news there is",
        "purchase": "for the goods bought",
        "sale": "with the goods sold",
        "yard": "to the yard",
        "recruits": "for the hands entered",
        "landing": "to land a person who stays ashore",
        "fetch": "to bring a person off from the quay",
    }.get(errand, errand)


def _hours_words(hours: float) -> str:
    if hours < 1.0:
        return f"{max(1, round(hours * 60))} minutes"
    if abs(hours - round(hours)) < 0.05:
        n = round(hours)
        return f"{n} hour{'s' if n != 1 else ''}"
    return f"{hours:.1f} hours"


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
