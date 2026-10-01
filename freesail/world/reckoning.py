"""The reckoning: the captain's account of where she is (spec M5 §13, §15; the study
`docs/design/Navigation1805.md` §1, §3, §4(a); package 33a).

**The world keeps the truth and the captain keeps his account.** The truth is the
physics' `Position` (`World.position`, package 32), which no reading, no snapshot and no
drawing gives. The reckoning is a second position, kept here with a two-by-two
covariance, advanced at each heave of the log by the logged run along the course
steered, corrected as the master corrected it (for his chart's variation, for the
leeway he allowed when close-hauled, for the set he allowed if any), and grown by the
error terms of N §3; and updated by each observation as a line or a point measurement
in the simplest Kalman form. The master's errors come from the model's seeded draws
(`rng` stream `reckoning`); the truth from the physics; the difference is what the
player discovers (N §3, the one rule that keeps it honest).

Two kinds of error, as N §3 has them:

- **What the master doubts** goes into the covariance and so into the ellipse the chart
  draws and the words he says: the log read to a quarter knot and the hour's run
  inferred from one heave (random, along the course); the helmsman's steering (random,
  across it; the traverse board's half-hourly pegs average it); his leeway estimate
  when close-hauled (a bias across the course); the set of the Channel's streams he did
  not allow for (a bias, east and west above all).
- **What he cannot know** moves the account and not the ellipse: the log-line marked
  short so that the ship overruns her reckoning (Luce); his chart's variation a decade
  old; the deviation of the ship's own iron, which nobody aboard in 1805 could name
  (N §1, the Apollo); and the leeway estimate's bias itself. That is the ellipse drawn
  too small, which is what wrecked *Apollo* (N §3), and it is why a landfall can be
  made wrong on the reckoning while the master still says he trusts it within ten
  miles.

The random terms grow the doubt as the square root of the steps; the biases grow it in
a straight line (N §3, "and they are the ones that kill"), which the bias accumulators
below keep as vectors whose outer products are added to the covariance and which a fix
resolves along its own line. The player never sees a matrix: `uncertainty_words` is the
master's sentence, and the viewer's chart draws the ellipse faintly about the reckoned
position and never the truth.

The observations (§13): a sounding is a line, the reckoning moved onto the nearest point
of the chart's depth contour consistent with the ground (`chart.Chart.contour_point`) and
the doubt across the contour shrunk to a few miles, along it left as it was; a bearing
of a mark is a line at the bearing's angle; two cross to a point; a transit is exact; the
noon latitude collapses north and south (`freesail.world.sights`). `Navigation` below is
the World's glue: the log hove hourly (two-hourly in a vessel that is not a ship of
war, Falconer), the noon sight and the day's work at the sun's noon, the master as the
first named person with a skill and a place (spec §22's minimum), the casts and the
bearings by order, and the lines the log says for each in the ship's-log voice.

Every constant names its source or says "judgement"; one from a figure the study marks
unverified says so here and in `docs/dev/TuningNotes.md`.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world.geo import Position, bearing_and_distance, estimate_words, format_position
from freesail.world.lookout import DISTANCE_BY_ESTIMATION_FRACTION as _LOOKOUT_ESTIMATE_FRACTION

__all__ = [
    "BEARING_SIGMA_DEG",
    "CHART_VARIATION_AGE_YEARS",
    "CONTOUR_SEARCH_MIN_NM",
    "CONTOUR_TOLERANCE_DEEP_FATHOMS",
    "CONTOUR_TOLERANCE_HAND_FATHOMS",
    "DAYS_WORK_MINUTES",
    "DEEP_SEA_LEAD_FATHOMS",
    "DEEP_SEA_LEAD_MAX_KN",
    "DEPARTURE_SIGMA_NM",
    "DEVIATION_MAX_DEG",
    "FIX_RUN_NM",
    "HAND_LEAD_FATHOMS",
    "HAND_LEAD_MARKS",
    "LEAD_DEEP_SIGMA_FATHOMS",
    "LEAD_HAND_SIGMA_FATHOMS",
    "LEEWAY_DOUBT_POINTS",
    "LEEWAY_ESTIMATE_ERROR_POINTS",
    "LEEWAY_ALLOWED_WITHIN_POINTS",
    "LUNAR_TAKEN_KIND",
    "LOG_INTERVAL_H_SHIP_OF_WAR",
    "LOG_INTERVAL_H_OTHER",
    "LOG_LINE_SHORT_MAX",
    "LOG_LINE_SHORT_MIN",
    "LOG_READ_KN",
    "LOG_READ_SIGMA_KN",
    "SET_DOUBT_EAST_KN",
    "SET_DOUBT_NORTH_KN",
    "SOUNDING_ACROSS_SIGMA_NM",
    "STEERING_SIGMA_POINTS_SEAWAY",
    "STEERING_SIGMA_POINTS_SMOOTH",
    "TRANSIT_SIGMA_NM",
    "TRACK_KEPT",
    "VARIATION_1805_DEG",
    "VARIATION_DRIFT_DEG_PER_YEAR",
    "Bearing",
    "CompassErrors",
    "Master",
    "Navigation",
    "Noon",
    "Reckoning",
    "Sounding",
    "age_words",
    "chant",
    "ground_words",
    "knots_words",
    "miles_words",
]

# ---------------------------------------------------------------------------
# The error terms (N §3), each with its source
# ---------------------------------------------------------------------------

# The log-line, marked short "by 3 or 4 feet" of a 47.6-foot knot so that "a ship will
# generally overrun her reckoning ... since it is best to err on the safe side" (Luce
# 1866, 'Log-line, Time-glasses'): 6 to 8 per cent by Luce's feet, 3 to 8 by N §3's
# table, which is the range taken. Drawn once per ship from the `reckoning` stream: the
# line's own marking, which the master does not correct (that is its purpose), so it is a
# bias on the account and not in the ellipse.
LOG_LINE_SHORT_MIN = 0.03
LOG_LINE_SHORT_MAX = 0.08
# The log read to a quarter knot (N §3; Falconer 1780, 'Log': the knots and their halves
# and quarters on the line); a quarter knot either way in the read itself, drawn each
# heave. In the covariance the hour's run inferred from one heave is a quarter of a mile
# an hour, one sigma (judgement on N §3's "read to a quarter knot ... the hour's run
# inferred from one heave").
LOG_READ_KN = 0.25
LOG_READ_SIGMA_KN = 0.25
# Before the first heave of a passage the master has no read and runs the account on
# her way as he judges it by eye, to the knot, with a knot of doubt one sigma
# (judgement: the departure taken with the sails still going up; the first heave comes
# at the hour, and a two-hourly log would otherwise leave the account standing).
SPEED_BY_EYE_SIGMA_KN = 1.0
# Hove to and making no way, the log-board notes the time and the master runs no
# distance for it; a ship hove to fore-reaches a knot or so, and one with more way on
# than this by eye is sailing whatever her yards say (judgement).
HOVE_TO_WAY_KN = 2.0
# "It is usual to heave the log once every hour in ships of war and East-Indiamen; and in
# all other vessels, once in two hours" (Falconer 1780, 'Log'; N §1). A ship of war is
# known by her marines (the frigate's and the brig's ship files muster them; the
# schooner and the cutter have none).
LOG_INTERVAL_H_SHIP_OF_WAR = 1
LOG_INTERVAL_H_OTHER = 2

# The compass. The true variation of the western Channel in 1805 is to be computed from
# the gufm1 field model at the chart's build (spec M5 §13; N §3): the study marks the
# figure UNVERIFIED (N, "Not verified": the Channel's variation in 1805; Falconer's "more
# than 20 degrees" at London in 1780 and 21° 09' W at Greenwich in 1773 are the anchors,
# "about two points west"). The value here is the model's as the package recalls it for
# the Lizard, about 24° W (London's series in Jackson, Jonkers and Walker 2000 runs 23
# to 24° W through the decade, and Cornwall lies a degree more westerly); the build tool
# does not yet compute it, so the constant is provisional and says so in TuningNotes.
VARIATION_1805_DEG = 24.0
# The captain's chart is the 1794 reissue of Mountaine and Dodson's variation chart
# (N §1), a decade old in 1805, and the variation was moving "a quarter of a degree a
# year" (N §3; the study's figure, not sourced further: unverified). The master allows
# his chart's variation, so the account's course is out by the drift of the decade, a
# bias he cannot know; an azimuth would correct it (N §3) and is not built (§32).
CHART_VARIATION_AGE_YEARS = 10
VARIATION_DRIFT_DEG_PER_YEAR = 0.25
# The deviation of the ship's own iron, by heading, "not corrected at all in 1805; a few
# degrees in a wooden ship with iron guns, more with iron stowed near the binnacle" (N
# §3; the size of a wooden frigate's deviation is on the study's unverified list). The
# semicircular form B sin H + C cos H with B and C drawn once per ship within this many
# degrees either way; a bias the player "cannot even ask for, only suffer".
DEVIATION_MAX_DEG = 3.0

# Steering: "half a point in a seaway, a quarter in smooth water; the traverse board's
# half-hourly peg averages it" (N §3, judgement there: no period source gives the
# helmsman's wander as a number). One sigma per hour of the course the master pegs,
# drawn each step; the seaway is a heavy sea or worse (spec M5 §4's words).
STEERING_SIGMA_POINTS_SMOOTH = 0.25
STEERING_SIGMA_POINTS_SEAWAY = 0.5

# Leeway, "estimated by eye from the angle of the wake to the keel and allowed in points
# on the course; very inconsiderable, except when the ship is close-hauled, and is
# accordingly disregarded whenever the wind is large" (Falconer 1780, 'Lee-way'; N §1).
# The master allows it within this many points of the true wind (the wind forward of
# the beam: judgement on Falconer's "large") and none beyond; his estimate is out by up
# to half a point either way (N §3), a bias drawn once per ship; his doubt of it, a
# quarter of a point one sigma across the course while it is allowed (judgement: half a
# point either way as a spread).
LEEWAY_ALLOWED_WITHIN_POINTS = 8.0
LEEWAY_ESTIMATE_ERROR_POINTS = 0.5
LEEWAY_DOUBT_POINTS = 0.25

# The set the master did not allow for (N §3: "Channel streams one to three knots turning
# with the tide, allowed for only if the master knows the establishment and his own
# longitude"; Rennell's current "a mile an hour to the northward for days in
# south-westerly gales", read in summary). Until package 34 the world's set is the
# scenario's stated current, none by default; the master's doubt of it is his whatever
# the world does, and grows in a straight line: the streams run east and west along the
# Channel, so the doubt lies east and west above all, and a little north and south for
# Rennell's current. The sizes are judgement, tuned so that four days of thick weather
# leave the ellipse N §3 describes (truth 58; TuningNotes, M5b).
SET_DOUBT_EAST_KN = 0.2
SET_DOUBT_NORTH_KN = 0.03

# A departure: the reckoning begins where the land was last seen, a mile in doubt
# (judgement: a bearing of a headland and its distance by estimation).
DEPARTURE_SIGMA_NM = 1.0
# A line of position taken within this run of the last is crossed with it (a fix of two
# bearings, a bearing and a sounding); one taken after a longer run replaces the account
# across it (judgement: two miles, a quarter of an hour's run, the time a master takes
# his two bearings in).
FIX_RUN_NM = 2.0

# The lead (Lever 1808, 'The Hand-Lead', 'The Deep-Sea Lead'; Luce 1884, ch. I 'The
# Lead'; Falconer 1780, 'Sounding'). The hand lead, 7 to 9 pounds on a line of about
# twenty fathoms marked at 2, 3, 5, 7, 10, 13, 15 and 17 (Lever; Luce marks 20 and on for
# the longer hand line), hove from the chains with way on; the deep-sea lead, 25 to 30
# pounds, "for which it is usual previously to bring-to the ship", or with a light breeze
# the line passed forward and hove from the spritsail yardarm (Lever, fig. 506). The
# deep-sea line here reaches 120 fathoms (Luce's coasting lead serves to 100 and the
# deep-sea beyond; one lead in the game, judgement); a ship with more than four knots
# of way does not get bottom with it (Lever's "going free with a light breeze":
# judgement on the words). The hand lead reads to the quarter fathom as the leadsman
# calls it, the deep-sea lead to the fathom (N §3, "depth to a fathom").
HAND_LEAD_FATHOMS = 20.0
HAND_LEAD_MARKS = (2, 3, 5, 7, 10, 13, 15, 17, 20)
DEEP_SEA_LEAD_FATHOMS = 120.0
DEEP_SEA_LEAD_MAX_KN = 4.0
LEAD_HAND_SIGMA_FATHOMS = 0.25
LEAD_DEEP_SIGMA_FATHOMS = 1.0
# Matched against the chart, a sounding "gives a band a few miles wide along the depth
# contour" (N §3): three miles one sigma across the contour, judgement on "a few". The
# contour the cast is matched to is the nearest point within the ellipse (at least this
# many miles about the reckoning) whose depth is within the tolerance of the cast and
# whose ground agrees; the tolerances are the lead's own error and the chart's
# (judgement).
SOUNDING_ACROSS_SIGMA_NM = 3.0
CONTOUR_SEARCH_MIN_NM = 5.0
CONTOUR_TOLERANCE_HAND_FATHOMS = 0.75
CONTOUR_TOLERANCE_DEEP_FATHOMS = 2.5

# A bearing of a landmark, "a degree or two by compass" (N §3): a degree and a half one
# sigma; a transit exact to a cable (spec §13: "a transit is exact"; judgement).
BEARING_SIGMA_DEG = 1.5
TRANSIT_SIGMA_NM = 0.1
# The distance off by estimation that goes with a bearing (spec §12's words, "twelve
# miles by estimation") is the lookout's own figure (package 33b: drawn once per sighting
# episode and held while she makes no way, `lookout.DISTANCE_BY_ESTIMATION_FRACTION`),
# the same in the list, the hail and the bearing taken. It is a second line, along the
# bearing, so a bearing with its distance lays the ship on the chart as the period's
# master did; a transit has none. The name is kept here for the tests.
DISTANCE_BY_ESTIMATION_FRACTION = _LOOKOUT_ESTIMATE_FRACTION

# The variation by observation (package 33b; decision 30; N §3: "an azimuth observation
# gets it to a degree"): once the master has observed an amplitude or an azimuth he
# allows his own figure in the traverse in place of the chart's decade-old one, and the
# account's course error is the deviation and the observation's error alone.
# `VARIATION_1805_DEG` above stays the world's truth (spec M5 §33 item 14, still
# UNVERIFIED: the gufm1 value not computed by the chart build).

# The lunar's evolution (`data/evolutions/take_lunar.yaml`) completes with this kind and
# the World hands it here as it hands the log's and the lead's.
LUNAR_TAKEN_KIND = "lunar.taken"

# The master's day's work at noon occupies him below this long (judgement: the traverse
# reduced from the log-board by the table and the sight worked, Falconer 1780,
# 'Log-board', 'Traverse'); the sight itself has him on deck for the last quarter of an
# hour before the sun's noon (`sights.SIGHT_ON_DECK_MINUTES`).
DAYS_WORK_MINUTES = 30

# The track by account kept for the chart: the last so many hourly positions (judgement:
# a week of hourly steps, so a long passage's snapshot stays small).
TRACK_KEPT = 168

_NM_PER_DEG = 60.0


# ---------------------------------------------------------------------------
# Words
# ---------------------------------------------------------------------------

_SMALL = (
    "no",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)
_TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")


def number_words(n: int) -> str:
    """'seven', 'forty-five', 'a hundred and twelve': a number as the log writes it."""
    n = int(n)
    if n < 20:
        return _SMALL[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (f"-{_SMALL[ones]}" if ones else "")
    if n < 200:
        rest = n - 100
        return "a hundred" + (f" and {number_words(rest)}" if rest else "")
    return str(n)


def knots_words(knots: float) -> str:
    """The log's read in words: 'six knots and a half', 'four knots and a quarter',
    'three knots and three quarters', 'seven knots', 'no way'."""
    quarters = round(knots * 4.0)
    whole, q = divmod(quarters, 4)
    if whole == 0 and q == 0:
        return "no way"
    words = f"{number_words(whole)} knot{'s' if whole != 1 else ''}" if whole else ""
    frac = {1: "a quarter", 2: "a half", 3: "three quarters"}.get(q, "")
    if whole and frac:
        return f"{words} and {frac}"
    if q == 2:
        return "half a knot"
    if frac:
        return f"{frac} of a knot"
    return words


def miles_words(nm: float) -> str:
    """'131 miles', 'a mile', 'half a mile': a distance in the log's whole miles."""
    n = round(nm)
    if n <= 0:
        return "half a mile" if nm >= 0.25 else "no distance"
    return "a mile" if n == 1 else f"{n} miles"


def age_words(seconds: float) -> str:
    """'just now', 'ten minutes ago', 'an hour ago', 'three hours ago', 'two days ago'."""
    minutes = int(seconds // 60)
    if minutes < 2:
        return "just now"
    if minutes < 60:
        return f"{number_words(minutes)} minutes ago"
    hours = minutes // 60
    if hours < 24:
        return "an hour ago" if hours == 1 else f"{number_words(hours)} hours ago"
    days = hours // 24
    return "a day ago" if days == 1 else f"{number_words(days)} days ago"


def chant(fathoms: float, hand: bool) -> str:
    """The leadsman's chant (Luce 1884, ch. I 'The Lead'): with the hand lead, 'By the
    mark seven' at a mark, 'By the deep nine' at a deep, 'And a half seven', 'And a
    quarter five', 'Quarter less five' between; with the deep-sea lead the fathoms as the
    song has them, 'forty-five fathoms'."""
    if not hand:
        n = max(1, round(fathoms))
        return f"{number_words(n).capitalize()} fathoms"
    quarters = round(fathoms * 4.0)
    whole, q = divmod(quarters, 4)
    if q == 0:
        if whole in HAND_LEAD_MARKS:
            return f"By the mark {number_words(whole)}"
        return f"By the deep {number_words(whole)}"
    if q == 1:
        return f"And a quarter {number_words(whole)}"
    if q == 2:
        return f"And a half {number_words(whole)}"
    return f"Quarter less {number_words(whole + 1)}"


# The ground the arming brings up where the chart's own bottom notes are silent, by the
# depth: the Western Approaches' floor is sand and shells inshore of the hundred-fathom
# line and grey sand and ooze beyond (Lever 1808, 'arming the Lead': "Sand, Coral,
# Shells, Oaze"; the song's "white sandy bottom" at forty-five fathoms; the spec's line
# "fine grey sand with black specks"). Judgement by band.
_GROUND_BY_DEPTH: tuple[tuple[float, str], ...] = (
    (10.0, "sand and broken shells"),
    (30.0, "fine sand"),
    (60.0, "fine grey sand with black specks"),
    (90.0, "grey sand and ooze"),
    (math.inf, "soft ooze"),
)


def ground_words(chart: Any, pos: Position, depth_m: float) -> str:
    """What the arming brings up at a point: the chart's nearest bottom note within three
    miles (package 32's notes, the pilot's words), else the ground by the depth."""
    if chart is not None:
        near = chart.bottom_near(pos, 3.0 * units.NAUTICAL_MILE)
        if near:
            return near
    fathoms = units.m_to_fathoms(depth_m)
    for limit, words in _GROUND_BY_DEPTH:
        if fathoms < limit:
            return words
    return _GROUND_BY_DEPTH[-1][1]


def _round_miles(nm: float) -> int:
    """The master's miles: to the mile under ten, to five above (a master says 'twenty
    miles', not 'nineteen')."""
    if nm < 10.0:
        return max(1, round(nm))
    return int(5 * round(nm / 5.0))


# ---------------------------------------------------------------------------
# The seeded errors of one ship
# ---------------------------------------------------------------------------


@dataclass
class CompassErrors:
    """What the master cannot know, drawn once per ship from the `reckoning` stream: the
    log-line's marking, the deviation's two coefficients, his leeway estimate's bias;
    and the chart's variation error, which is the decade's drift and no draw."""

    log_line_short: float  # the fraction the line reads over the truth
    deviation_b_deg: float
    deviation_c_deg: float
    leeway_bias_points: float
    variation_error_deg: float = CHART_VARIATION_AGE_YEARS * VARIATION_DRIFT_DEG_PER_YEAR

    @classmethod
    def draw(cls, stream: random.Random) -> CompassErrors:
        return cls(
            log_line_short=stream.uniform(LOG_LINE_SHORT_MIN, LOG_LINE_SHORT_MAX),
            deviation_b_deg=stream.uniform(-DEVIATION_MAX_DEG, DEVIATION_MAX_DEG),
            deviation_c_deg=stream.uniform(-DEVIATION_MAX_DEG, DEVIATION_MAX_DEG),
            leeway_bias_points=stream.uniform(
                -LEEWAY_ESTIMATE_ERROR_POINTS, LEEWAY_ESTIMATE_ERROR_POINTS
            ),
        )

    def deviation_deg(self, heading_rad: float) -> float:
        """The deviation on a heading, the semicircular form B sin H + C cos H."""
        return self.deviation_b_deg * math.sin(heading_rad) + self.deviation_c_deg * math.cos(
            heading_rad
        )

    def course_error_rad(self, heading_rad: float) -> float:
        """How far the course the master lays down lies from the course she steers: the
        chart's variation error and the deviation on her heading, in radians."""
        return math.radians(self.variation_error_deg + self.deviation_deg(heading_rad))

    @property
    def variation_allowed_deg(self) -> float:
        """The variation the master allows, west positive: the chart's, or his own by
        observation (package 33b)."""
        return VARIATION_1805_DEG - self.variation_error_deg

    def allow_variation(self, deg_west: float) -> None:
        """The master allows a variation he has observed (an amplitude or an azimuth,
        package 33b) in place of the chart's; the account's error in it is what the
        observation was out by."""
        self.variation_error_deg = VARIATION_1805_DEG - deg_west


# ---------------------------------------------------------------------------
# The records the chart draws
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Noon:
    tick: int
    lat_deg: float  # by account after the day's work
    lon_deg: float
    observed_lat_deg: float | None  # the latitude by observation, or None: no sight
    account_lat_deg: float  # the reckoning's latitude before the sight
    run_nm: float  # the run since the noon before, by account
    course_made_good_deg: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "lat_deg": round(self.lat_deg, 5),
            "lon_deg": round(self.lon_deg, 5),
            "observed_lat_deg": (
                None if self.observed_lat_deg is None else round(self.observed_lat_deg, 5)
            ),
            "run_nm": round(self.run_nm, 1),
        }


@dataclass(frozen=True)
class Bearing:
    tick: int
    feature_id: str
    name: str
    bearing_deg: float  # by compass, as the master laid it down
    mark_lat_deg: float
    mark_lon_deg: float
    distance_words: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "id": self.feature_id,
            "name": self.name,
            "bearing_deg": round(self.bearing_deg, 1),
            "mark_lat_deg": self.mark_lat_deg,
            "mark_lon_deg": self.mark_lon_deg,
        }


@dataclass(frozen=True)
class Sounding:
    tick: int
    depth_m: float | None  # None: no bottom
    ground: str
    words: str
    lat_deg: float  # the reckoning after the cast
    lon_deg: float
    deep: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "depth_m": None if self.depth_m is None else round(self.depth_m, 1),
            "ground": self.ground,
            "words": self.words,
            "lat_deg": round(self.lat_deg, 5),
            "lon_deg": round(self.lon_deg, 5),
        }


# ---------------------------------------------------------------------------
# The reckoning
# ---------------------------------------------------------------------------


class Reckoning:
    """The reckoned position with its covariance (square miles, east and north), the
    bias accumulators, and the records the chart draws. Pure arithmetic: nothing here
    reads the world; `Navigation` feeds it."""

    def __init__(self, start: Position, tick: int = 0, sigma_nm: float = DEPARTURE_SIGMA_NM):
        self.lat_deg = start.lat_deg
        self.lon_deg = start.lon_deg
        self.P: list[list[float]] = [[sigma_nm * sigma_nm, 0.0], [0.0, sigma_nm * sigma_nm]]
        # the biases: the set doubt east and north (independent, as standard deviations
        # that grow with the hours) and the leeway doubt as a vector across the course
        self.set_doubt = [0.0, 0.0]
        self.leeway_doubt = [0.0, 0.0]
        # the run since the last observation: a line taken after a run replaces the
        # account across it; one taken before she has run on is crossed with the last
        self.run_since_fix_nm = 0.0
        self.set_allowance: tuple[float, float] | None = None  # (knots, toward radians)
        self.track: list[tuple[int, float, float]] = [(tick, self.lat_deg, self.lon_deg)]
        self.noons: list[Noon] = []
        self.bearings: list[Bearing] = []
        self.soundings: list[Sounding] = []
        self.last_step_tick = tick
        # the noon's account, for the run since noon and the course made good
        self.noon_mark: tuple[int, float, float] = (tick, self.lat_deg, self.lon_deg)
        self.run_since_noon_nm = 0.0

    # -- geometry ---------------------------------------------------------------------

    @property
    def position(self) -> Position:
        return Position(self.lat_deg, self.lon_deg)

    def offset_nm(self, other: Position) -> tuple[float, float]:
        """Miles east and north from the reckoning to `other`."""
        de = (other.lon_deg - self.lon_deg) * _NM_PER_DEG * math.cos(math.radians(self.lat_deg))
        dn = (other.lat_deg - self.lat_deg) * _NM_PER_DEG
        return de, dn

    def _move(self, de: float, dn: float) -> None:
        self.lat_deg += dn / _NM_PER_DEG
        scale = math.cos(math.radians(self.lat_deg))
        if abs(scale) > 1e-9:
            self.lon_deg += de / (_NM_PER_DEG * scale)
        self.lon_deg = ((self.lon_deg + 180.0) % 360.0) - 180.0

    # -- the advance --------------------------------------------------------------------

    def advance(
        self,
        hours: float,
        course_rad: float,
        speed_kn: float,
        tick: int,
        steer_error_rad: float = 0.0,
        close_hauled: bool = False,
        heavy_sea: bool = False,
        leeway_doubt_rad: float = 0.0,
        read_sigma_kn: float = LOG_READ_SIGMA_KN,
    ) -> tuple[float, float]:
        """The traverse for one interval: the run `speed_kn` for `hours` along the course
        the master lays down (`course_rad`, already corrected as he corrects it), with
        the helmsman's error drawn for the interval; the doubt grown by the random terms
        (the read, `read_sigma_kn` an hour, and the steering) and the biases (the set,
        the leeway when close-hauled). Returns the miles east and north made by account.
        No hours at all (the whole interval hove to) still steps the board."""
        if hours < 0.0:
            return 0.0, 0.0
        run = max(0.0, speed_kn) * hours
        course = course_rad + steer_error_rad
        de, dn = run * math.sin(course), run * math.cos(course)
        if self.set_allowance is not None:
            kn, toward = self.set_allowance
            de += kn * hours * math.sin(toward)
            dn += kn * hours * math.cos(toward)
        self._move(de, dn)
        self.run_since_noon_nm += run
        self.run_since_fix_nm += run
        # the random terms, along and across the course
        steer_sigma = units.points_to_rad(
            STEERING_SIGMA_POINTS_SEAWAY if heavy_sea else STEERING_SIGMA_POINTS_SMOOTH
        )
        s_along = read_sigma_kn * hours
        s_across = run * steer_sigma
        c, s = math.cos(course), math.sin(course)
        # R diag(s_along², s_across²) Rᵀ with R the course's rotation (east, north)
        q_ee = s_along**2 * s * s + s_across**2 * c * c
        q_nn = s_along**2 * c * c + s_across**2 * s * s
        q_en = (s_along**2 - s_across**2) * s * c
        self.P[0][0] += q_ee
        self.P[1][1] += q_nn
        self.P[0][1] += q_en
        self.P[1][0] += q_en
        # the biases grow in a straight line: the set doubt east and north
        for i, kn in ((0, SET_DOUBT_EAST_KN), (1, SET_DOUBT_NORTH_KN)):
            old = self.set_doubt[i]
            new = old + kn * hours
            self.set_doubt[i] = new
            self.P[i][i] += new * new - old * old
        # and the leeway doubt across the course while close-hauled
        if close_hauled and leeway_doubt_rad > 0.0:
            old_l = list(self.leeway_doubt)
            self.leeway_doubt[0] += run * leeway_doubt_rad * c  # across: (cos, -sin)
            self.leeway_doubt[1] -= run * leeway_doubt_rad * s
            self._add_outer(self.leeway_doubt, +1.0)
            self._add_outer(old_l, -1.0)
        self.last_step_tick = tick
        self.track.append((tick, self.lat_deg, self.lon_deg))
        if len(self.track) > TRACK_KEPT:
            del self.track[0 : len(self.track) - TRACK_KEPT]
        return de, dn

    def _add_outer(self, v: list[float], sign: float) -> None:
        self.P[0][0] += sign * v[0] * v[0]
        self.P[1][1] += sign * v[1] * v[1]
        self.P[0][1] += sign * v[0] * v[1]
        self.P[1][0] += sign * v[0] * v[1]

    # -- the observations (the simplest Kalman form) ------------------------------------

    def update_line(self, de: float, dn: float, n_e: float, n_n: float, sigma_nm: float) -> float:
        """A line measurement: the ship lies on the line through the point `de, dn` miles
        east and north of the reckoning whose unit normal is (`n_e`, `n_n`), within
        `sigma_nm` across it. The reckoning is moved onto the line and its doubt across
        the line becomes the measurement's own; along the line nothing changes. Returns
        the miles moved.

        Two cases, both the Kalman update. A line taken after the account has run on
        since the last observation (more than `FIX_RUN_NM`) *replaces* the account across
        it, the prior's doubt across the line taken as unbounded: this is how the period
        worked it (the observed latitude replaces the reckoned one, Falconer 1780,
        'Dead-reckoning': the reckoning "is always to be corrected, as often as any good
        observation of the sun can be obtained"; a bearing or a sounding puts the ship on
        its line), and it is what the ellipse drawn too small requires, since the biases
        the master cannot know are not in his doubt and a weighing by that doubt would
        let a bad account outvote a good sight (N §3, the Apollo). A line taken before
        she has run on, the second of a fix, is *crossed* with the first by the gain, so
        two bearings meet at their crossing and a bearing and a sounding likewise."""
        p = self.P
        z = n_e * de + n_n * dn  # how far the line is, across it
        r = sigma_nm * sigma_nm
        if self.run_since_fix_nm > FIX_RUN_NM:
            self._move(n_e * z, n_n * z)
            # P = (I - n nᵀ) P (I - n nᵀ) + R n nᵀ: the doubt along the line kept, across
            # it the measurement's own
            t_e, t_n = -n_n, n_e  # along the line
            along_var = t_e * (p[0][0] * t_e + p[0][1] * t_n) + t_n * (
                p[1][0] * t_e + p[1][1] * t_n
            )
            self.P = [
                [along_var * t_e * t_e + r * n_e * n_e, along_var * t_e * t_n + r * n_e * n_n],
                [along_var * t_n * t_e + r * n_n * n_e, along_var * t_n * t_n + r * n_n * n_n],
            ]
            moved = abs(z)
        else:
            pn_e = p[0][0] * n_e + p[0][1] * n_n  # P n
            pn_n = p[1][0] * n_e + p[1][1] * n_n
            s = n_e * pn_e + n_n * pn_n + r  # n P n + R
            k_e, k_n = pn_e / s, pn_n / s  # the gain
            self._move(k_e * z, k_n * z)
            self.P = [  # (I - K nᵀ) P
                [p[0][0] - k_e * pn_e, p[0][1] - k_e * pn_n],
                [p[1][0] - k_n * pn_e, p[1][1] - k_n * pn_n],
            ]
            moved = math.hypot(k_e * z, k_n * z)
        self.run_since_fix_nm = 0.0
        # the biases resolved across the line
        along = n_e * self.leeway_doubt[0] + n_n * self.leeway_doubt[1]
        self.leeway_doubt[0] -= along * n_e
        self.leeway_doubt[1] -= along * n_n
        self.set_doubt[0] *= 1.0 - abs(n_e)
        self.set_doubt[1] *= 1.0 - abs(n_n)
        return moved

    def update_latitude(self, lat_deg: float, sigma_nm: float) -> float:
        """The noon latitude: a line east and west through the observed latitude."""
        dn = (lat_deg - self.lat_deg) * _NM_PER_DEG
        return self.update_line(0.0, dn, 0.0, 1.0, sigma_nm)

    def update_longitude(self, lon_deg: float, sigma_nm: float) -> float:
        """A longitude by chronometer or by lunar (package 33b, spec §13): a line north
        and south through the observed longitude, which collapses east and west by the
        observation's own doubt and leaves north and south as it was."""
        de = (lon_deg - self.lon_deg) * _NM_PER_DEG * math.cos(math.radians(self.lat_deg))
        return self.update_line(de, 0.0, 1.0, 0.0, sigma_nm)

    def update_bearing(self, mark: Position, bearing_rad: float, sigma_nm: float) -> float:
        """A bearing of a mark: the line from the mark along the reciprocal of the bearing
        laid down; its normal is across the bearing."""
        de, dn = self.offset_nm(mark)
        n_e, n_n = math.cos(bearing_rad), -math.sin(bearing_rad)
        return self.update_line(de, dn, n_e, n_n, sigma_nm)

    def update_distance(
        self, mark: Position, bearing_rad: float, distance_nm: float, sigma_nm: float
    ) -> float:
        """The distance off a mark by estimation, along the bearing: the line across the
        bearing at that distance from the mark, its normal along the bearing."""
        de, dn = self.offset_nm(mark)
        n_e, n_n = math.sin(bearing_rad), math.cos(bearing_rad)
        return self.update_line(de - distance_nm * n_e, dn - distance_nm * n_n, n_e, n_n, sigma_nm)

    def set_position(self, pos: Position, tick: int, sigma_nm: float = DEPARTURE_SIGMA_NM) -> None:
        """The captain's override, or a departure: the account set to a point with a
        fresh doubt, the biases forgotten."""
        self.lat_deg, self.lon_deg = pos.lat_deg, pos.lon_deg
        self.P = [[sigma_nm * sigma_nm, 0.0], [0.0, sigma_nm * sigma_nm]]
        self.set_doubt = [0.0, 0.0]
        self.leeway_doubt = [0.0, 0.0]
        self.run_since_fix_nm = FIX_RUN_NM + 1.0  # the next line replaces, as after a run
        self.track.append((tick, self.lat_deg, self.lon_deg))

    # -- the ellipse and the words ------------------------------------------------------

    @property
    def sigma_east_nm(self) -> float:
        return math.sqrt(max(0.0, self.P[0][0]))

    @property
    def sigma_north_nm(self) -> float:
        return math.sqrt(max(0.0, self.P[1][1]))

    def ellipse(self) -> dict[str, float]:
        """The one-sigma ellipse: its semi-axes in miles and the bearing of the major
        axis from north, with the east and north standard deviations beside them."""
        a, b, c = self.P[0][0], self.P[0][1], self.P[1][1]
        mean = 0.5 * (a + c)
        diff = 0.5 * (a - c)
        root = math.sqrt(diff * diff + b * b)
        big, small = max(0.0, mean + root), max(0.0, mean - root)
        # the major axis's direction in the (east, north) plane
        if root < 1e-12:
            angle = 0.0
        else:
            angle = 0.5 * math.atan2(2.0 * b, a - c)  # from the east axis toward north
        bearing = (90.0 - math.degrees(angle)) % 180.0
        return {
            "semi_major_nm": round(math.sqrt(big), 2),
            "semi_minor_nm": round(math.sqrt(small), 2),
            "major_bearing_deg": round(bearing, 1),
            "sigma_east_nm": round(self.sigma_east_nm, 2),
            "sigma_north_nm": round(self.sigma_north_nm, 2),
        }

    @property
    def words(self) -> str:
        """'49° 52' N, 6° 10' W by account'."""
        return f"{format_position(self.position)} by account"

    @property
    def uncertainty_words(self) -> str:
        """The master's sentence: "I would not trust the reckoning within twenty miles
        east or west, nor five north or south." A doubt under a mile is 'a mile'."""
        east = _round_miles(self.sigma_east_nm)
        north = _round_miles(self.sigma_north_nm)
        return (
            f"I would not trust the reckoning within {miles_words(east)} east or west, "
            f"nor {miles_words(north)} north or south."
        )

    def since_noon(self) -> tuple[float, float | None]:
        """(the run since noon by account, the course made good since noon in degrees
        true, or None with no distance made)."""
        _, lat0, lon0 = self.noon_mark
        start = Position(lat0, lon0)
        bearing, dist = bearing_and_distance(start, self.position)
        if dist < 0.1 * units.NAUTICAL_MILE:
            return self.run_since_noon_nm, None
        return self.run_since_noon_nm, bearing

    def to_dict(self) -> dict[str, Any]:
        """For the captain's chart (`api.queries.snapshot`): the reckoned position, the
        ellipse, the track by account, the noons, the bearings and the soundings; never
        the truth."""
        run, cmg = self.since_noon()
        return {
            "lat_deg": round(self.lat_deg, 5),
            "lon_deg": round(self.lon_deg, 5),
            "words": self.words,
            "uncertainty": self.uncertainty_words,
            "ellipse": self.ellipse(),
            "track": [[t, round(la, 5), round(lo, 5)] for t, la, lo in self.track],
            "noons": [n.to_dict() for n in self.noons],
            "bearings": [b.to_dict() for b in self.bearings],
            "soundings": [s.to_dict() for s in self.soundings],
            "run_since_noon_nm": round(run, 1),
            "course_made_good_deg": None if cmg is None else round(cmg, 1),
        }


# ---------------------------------------------------------------------------
# The master (spec §14's last paragraph; §22's minimum)
# ---------------------------------------------------------------------------


@dataclass
class Master:
    """The first named person: a name from the ship's list, a skill for the sights, a
    place (on deck, below) that the sight and the day's work occupy until a tick."""

    name: str  # "Mr Ellis"; "the master" when the ship's list names none
    skill: float  # 0 to 1, for the sights
    place: str = "on deck"
    occupied_until: int | None = None
    occupied_with: str = ""

    def occupy(self, place: str, until: int, with_what: str) -> None:
        self.place = place
        self.occupied_until = until
        self.occupied_with = with_what

    def tick(self, now: int) -> str | None:
        """Free him when his work is done; the line to say, if any."""
        if self.occupied_until is not None and now >= self.occupied_until:
            self.occupied_until = None
            was = self.occupied_with
            self.occupied_with = ""
            if self.place == "below":
                self.place = "on deck"
                return f"{self.name} came on deck, the {was} done."
        return None

    @property
    def occupied(self) -> bool:
        return self.occupied_until is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "skill": round(self.skill, 2),
            "place": self.place,
            "occupied_with": self.occupied_with,
        }


def master_of(ship: Any) -> Master:
    """The master from the ship's list: the sailor at the post 'master' (every ship file
    musters one; the frigate's, the schooner's, the cutter's and the brig's), addressed
    by his surname as the log addresses a warrant officer; his skill the muster's for
    deck work, which is the navigator's."""
    crew = (getattr(ship, "extra", None) or {}).get("crew")
    sailor = getattr(crew, "posts", {}).get("master") if crew is not None else None
    if sailor is None:
        return Master("the master", 0.7)
    surname = str(sailor.name).split()[-1]
    return Master(f"Mr {surname}", float(getattr(sailor, "skill_deck", 0.7)))


# ---------------------------------------------------------------------------
# Navigation: the World's glue
# ---------------------------------------------------------------------------

# The log kinds the runner's two evolutions complete with (`data/evolutions/heave_log.yaml`,
# `heave_lead.yaml`, `heave_deep_sea_lead.yaml`): the World hands them here and does not
# record the runner's own line, since the read is not known until the log is in.
LOG_HOVE_KIND = "log.hove"
LEAD_HOVE_KIND = "lead.hove"
NAVIGATION_KINDS = frozenset({LOG_HOVE_KIND, LEAD_HOVE_KIND, LUNAR_TAKEN_KIND})

# The subject the two evolutions hold: the runner's alias for the ship that is not the
# manoeuvres' `ship`, so the mate at the log and the leadsman in the chains do not hold
# her against a tack or a wear (`runner.Runner.SHIP_SUBJECTS`).
LOG_SUBJECT = "her"


class Navigation:
    """The reckoning kept aboard one World: the master, the log-line and the lead, the
    noon and the day's work, the casts and the bearings by order, and the lines."""

    def __init__(self, world: Any, stream: random.Random):
        self.world = world
        self.stream = stream
        origin: Position = world.origin
        self.errors = CompassErrors.draw(stream)
        # the departure: where the land was last seen, drawn a mile in doubt
        de = stream.gauss(0.0, DEPARTURE_SIGMA_NM)
        dn = stream.gauss(0.0, DEPARTURE_SIGMA_NM)
        self.reckoning = Reckoning(origin, world.clock.tick)
        self.reckoning._move(de, dn)
        # the master is named from the ship's list, which the composer musters after the
        # World is made (`api.session.attach_crew`), so he is looked up at his first call
        self._master: Master | None = None
        self._log_interval_h: int | None = None
        self._automatic_heaves: list[bool] = []  # the heaves begun and not yet in
        self.noon_had = False  # a first noon worked: the run since noon has a meaning
        self.last_log_read_kn: float | None = None
        self.last_log_tick: int | None = None
        self.last_cast: Sounding | None = None
        self.last_sight: Any = None  # sights.Sight
        self.sight_day: Any = None  # the date of the last sight or refusal
        self.sight_refused: str | None = None  # today's refusal, in words
        self._noon_done_day: Any = None
        self._transit: datetime | None = None  # today's noon by the sun
        # the longitude (package 33b; spec §14): the chronometer when the scenario gives
        # one, its drift and its rating's offset drawn from the `chronometer` stream; the
        # last time sight and the last lunar; a lunar in hand (the body, while the master
        # and the mates are at the distances) and one cleared below, due at a tick; and
        # the variation the master allows, the chart's until he observes his own
        from freesail.world.sights import Chronometer, Variation

        spec = getattr(world.scenario, "chronometer", None)
        self.chronometer: Chronometer | None = (
            Chronometer.from_scenario(spec, world.clock.ship_time, world.rng.stream("chronometer"))
            if spec
            else None
        )
        self.last_time_sight: Any = None  # sights.TimeSight
        self.last_lunar: Any = None  # sights.Lunar
        self._lunar_in_hand: str | None = None
        self._lunar_pending: tuple[int, Any] | None = None
        self.variation = Variation(self.errors.variation_allowed_deg, "the chart of 1794")
        # the traverse board: the heading summed since the last step, and the leeway
        self._hx = 0.0
        self._hy = 0.0
        self._n = 0
        self._leeway_sum = 0.0
        self._close_hauled_n = 0
        self._hove_to_n = 0  # the ticks hove to since the last step: no run on the board
        self._sea_heavy = False

    @property
    def master(self) -> Master:
        if self._master is None:
            self._master = master_of(self.world.ship)
        return self._master

    @property
    def log_interval_h(self) -> int:
        if self._log_interval_h is None:
            self._log_interval_h = (
                LOG_INTERVAL_H_SHIP_OF_WAR
                if _ship_of_war(self.world.ship)
                else LOG_INTERVAL_H_OTHER
            )
        return self._log_interval_h

    # -- the tick ---------------------------------------------------------------------

    def tick(self, pending: list[tuple[str, dict[str, Any]]]) -> None:
        """Every tick: the traverse board pegged, the pending heaves and casts finished,
        the log hove at the hour, the noon. `pending` is the runner's completions this
        tick (`NAVIGATION_KINDS`), in order."""
        world = self.world
        ship = world.ship
        heading = float(ship.heading)
        self._hx += math.sin(heading)
        self._hy += math.cos(heading)
        self._n += 1
        dyn = getattr(ship, "dyn", None)
        if dyn is not None:
            self._leeway_sum += float(dyn.leeway)
        if self._close_hauled_now():
            self._close_hauled_n += 1
        if "hove_to" in (getattr(ship, "extra", None) or {}) and (
            units.ms_to_knots(_speed_through_water(ship)) < HOVE_TO_WAY_KN
        ):
            self._hove_to_n += 1
        if self._lunar_pending is not None and world.clock.tick >= self._lunar_pending[0]:
            self._lunar_cleared()
        line = self.master.tick(world.clock.tick)
        if line:
            world.record(Severity.ROUTINE, "master.place", line, data=self.master.to_dict())
        for kind, data in pending:
            if kind == LOG_HOVE_KIND:
                # the hourly heaves and the ordered ones finish in the order they began,
                # both holding the same subject, so the flags are a queue
                automatic = self._automatic_heaves.pop(0) if self._automatic_heaves else False
                self._log_hove(automatic=automatic)
            elif kind == LEAD_HOVE_KIND:
                self._cast(deep=data.get("evolution") == "heave_deep_sea_lead")
            elif kind == LUNAR_TAKEN_KIND:
                self._lunar_taken()
        t = world.clock.ship_time
        if self.chronometer is not None:
            said = self.chronometer.tick(t)
            if said:
                dead = not self.chronometer.going
                world.record(
                    Severity.NOTABLE if dead else Severity.ROUTINE,
                    "chronometer.dead" if dead else "chronometer.wound",
                    said,
                    data=self.chronometer.to_dict(),
                )
        if t.minute == 0 and t.second == 0 and t.hour % self.log_interval_h == 0:
            self.heave_log(automatic=True)
        self._tick_noon()

    def _close_hauled_now(self) -> bool:
        world = self.world
        rel = abs(units.wrap_pi(float(world.ship.heading) - float(world.wind.direction_from)))
        return units.rad_to_points(rel) <= LEEWAY_ALLOWED_WITHIN_POINTS

    def _heavy_sea(self) -> bool:
        sea = getattr(self.world, "sea", None)
        if sea is None:
            return False
        return sea.reading().state in ("heavy", "very heavy")

    # -- the traverse ------------------------------------------------------------------

    def account_now(self) -> Position:
        """The account as the mate brings it up from the log-board at this moment, for a
        reading or the chart: the last worked position run on at the log's last read
        along the traverse board's mean heading since, corrected as the master corrects
        it, with no draw and nothing changed (a reading never moves the account; the
        master works it at the heave, the noon and by order)."""
        r = self.reckoning
        tick = self.world.clock.tick
        hours = (tick - r.last_step_tick) / 3600.0
        read = self.last_log_read_kn
        if read is None:
            read = self._speed_by_eye_kn()
        if hours <= 0.0 or self._n == 0 or read <= 0.0:
            return r.position
        hours = self._hours_under_way(hours)
        heading = math.atan2(self._hx, self._hy) % units.TWO_PI
        course = heading + self.errors.course_error_rad(heading)
        if self._close_hauled_n * 2 > self._n:
            course += self._leeway_sum / self._n + units.points_to_rad(
                self.errors.leeway_bias_points
            )
        run = read * hours
        de, dn = run * math.sin(course), run * math.cos(course)
        if r.set_allowance is not None:
            kn, toward = r.set_allowance
            de += kn * hours * math.sin(toward)
            dn += kn * hours * math.cos(toward)
        lat = r.lat_deg + dn / _NM_PER_DEG
        scale = math.cos(math.radians(lat))
        lon = r.lon_deg + (de / (_NM_PER_DEG * scale) if abs(scale) > 1e-9 else 0.0)
        return Position(lat, ((lon + 180.0) % 360.0) - 180.0)

    def bring_up(self, speed_kn: float | None = None) -> tuple[float, float]:
        """Bring the account up to this tick from the last step: the course from the
        traverse board (the mean heading since), corrected as the master corrects it,
        the run at the log's last read (or `speed_kn`), the doubt grown. Returns the
        miles east and north made."""
        world = self.world
        tick = world.clock.tick
        hours = (tick - self.reckoning.last_step_tick) / 3600.0
        if hours <= 0.0 or self._n == 0:
            return 0.0, 0.0
        hours = self._hours_under_way(hours)
        heading = math.atan2(self._hx, self._hy) % units.TWO_PI
        close_hauled = self._close_hauled_n * 2 > self._n
        leeway_allowed = 0.0
        if close_hauled:
            # the master's estimate by eye: the physics' leeway plus his bias
            leeway_allowed = self._leeway_sum / self._n + units.points_to_rad(
                self.errors.leeway_bias_points
            )
        course = heading + leeway_allowed + self.errors.course_error_rad(heading)
        read = self.last_log_read_kn if speed_kn is None else speed_kn
        read_sigma = LOG_READ_SIGMA_KN
        if read is None:
            read, read_sigma = self._speed_by_eye_kn(), SPEED_BY_EYE_SIGMA_KN
        heavy = self._heavy_sea()
        steer = self.stream.gauss(
            0.0,
            units.points_to_rad(
                STEERING_SIGMA_POINTS_SEAWAY if heavy else STEERING_SIGMA_POINTS_SMOOTH
            ),
        )
        made = self.reckoning.advance(
            hours,
            course,
            read,
            tick,
            steer_error_rad=steer,
            close_hauled=close_hauled,
            heavy_sea=heavy,
            leeway_doubt_rad=units.points_to_rad(LEEWAY_DOUBT_POINTS),
            read_sigma_kn=read_sigma,
        )
        self._hx = self._hy = 0.0
        self._n = 0
        self._leeway_sum = 0.0
        self._close_hauled_n = 0
        self._hove_to_n = 0
        return made

    def _hours_under_way(self, hours: float) -> float:
        """The interval's hours less those hove to and making no way, which the
        log-board notes and the master runs no distance for (her drift hove to is the
        set he does not know)."""
        if self._n <= 0 or self._hove_to_n <= 0:
            return hours
        return hours * max(0.0, 1.0 - self._hove_to_n / self._n)

    def _speed_by_eye_kn(self) -> float:
        """Her way as the master judges it by eye before the log's first read: through
        the water, to the knot (`SPEED_BY_EYE_SIGMA_KN`)."""
        return float(round(units.ms_to_knots(_speed_through_water(self.world.ship))))

    # -- the log-line -------------------------------------------------------------------

    def heave_log(self, automatic: bool = False) -> str | None:
        """Start the heave: the evolution when the ship has a runner (the mate of the
        watch, a hand at the reel and one at the glass, half a minute), else the read at
        once. Returns the runner's line for an order, None for the hourly heave."""
        from freesail.evolutions.runner import OrderError

        runner = (getattr(self.world.ship, "extra", None) or {}).get("evolutions")
        if runner is None or not hasattr(runner, "instances"):
            self._log_hove(automatic)
            return None
        params: dict[str, Any] = {"automatic": automatic}
        if automatic:
            params["log_group"] = "the log"  # the hourly heave says its one line only
        try:
            line = runner.start(self.world.ship, "heave_log", LOG_SUBJECT, params)
        except OrderError:
            return None  # the hands are about ship, or the log is out already
        self._automatic_heaves.append(automatic)
        return line

    def _log_hove(self, automatic: bool) -> None:
        """The log is in: the read, to a quarter knot, with the line's marking and the
        heave's own error; the account brought up with it; the line."""
        world = self.world
        stw = units.ms_to_knots(_speed_through_water(world.ship))
        read = stw * (1.0 + self.errors.log_line_short) + self.stream.uniform(
            -LOG_READ_KN, LOG_READ_KN
        )
        read = max(0.0, round(read * 4.0) / 4.0)
        self.bring_up(read)
        self.last_log_read_kn = read
        self.last_log_tick = world.clock.tick
        world.record(
            Severity.ROUTINE,
            "log.read",
            f"Hove the log: {knots_words(read)}.",
            data={"knots": read, "automatic": automatic, "reckoning": self.reckoning.words},
        )

    # -- the lead ---------------------------------------------------------------------

    def heave_lead(self, deep: bool) -> str:
        """Start the cast (an order): the hand lead from the chains, or the deep-sea lead
        with the line passed forward; the evolution's line."""
        from freesail.evolutions.runner import OrderError

        world = self.world
        if world.chart is None:
            raise OrderError("No chart of these waters: there is no bottom to sound yet.")
        runner = (getattr(world.ship, "extra", None) or {}).get("evolutions")
        if runner is None or not hasattr(runner, "instances"):
            self._cast(deep)
            return "The lead hove."
        evo = "heave_deep_sea_lead" if deep else "heave_lead"
        return runner.start(world.ship, evo, LOG_SUBJECT, {"deep": deep})

    def _cast(self, deep: bool) -> None:
        """The lead is up: the depth by the chart at the truth with the lead's error and
        the arming's ground, matched to the chart's contour about the reckoning, the
        account moved onto it and its doubt across shrunk; the line."""
        world = self.world
        chart = world.chart
        pos = world.position
        tick = world.clock.tick
        truth = chart.depth_at(pos) if chart is not None and pos is not None else None
        limit = DEEP_SEA_LEAD_FATHOMS if deep else HAND_LEAD_FATHOMS
        speed_kn = units.ms_to_knots(_speed_through_water(world.ship))
        if deep and speed_kn > DEEP_SEA_LEAD_MAX_KN:
            text = (
                "The deep-sea lead would not get bottom with the way she has on; bring her "
                "to, or shorten sail, and try again."
            )
            self._record_cast(tick, None, "", text, deep)
            return
        if truth is None or units.m_to_fathoms(truth) > limit:
            what = "a hundred and twenty" if deep else "twenty"
            self._record_cast(tick, None, "", f"No bottom at {what} fathoms.", deep)
            return
        sigma = LEAD_DEEP_SIGMA_FATHOMS if deep else LEAD_HAND_SIGMA_FATHOMS
        fathoms = units.m_to_fathoms(truth) + self.stream.gauss(0.0, sigma)
        fathoms = max(0.25, round(fathoms * 4.0) / 4.0 if not deep else round(fathoms))
        ground = ground_words(chart, pos, truth)
        depth_m = units.fathoms_to_m(fathoms)
        self.bring_up()
        r = self.reckoning
        radius = max(CONTOUR_SEARCH_MIN_NM, 2.0 * r.ellipse()["semi_major_nm"])
        tolerance = CONTOUR_TOLERANCE_DEEP_FATHOMS if deep else CONTOUR_TOLERANCE_HAND_FATHOMS
        found = chart.contour_point(
            r.position,
            depth_m,
            units.fathoms_to_m(tolerance),
            radius * units.NAUTICAL_MILE,
            ground=ground,
            ground_of=lambda p, d: ground_words(chart, p, d),
        )
        moved = 0.0
        if found is not None:
            point, normal_deg = found
            de, dn = r.offset_nm(point)
            # the line across the contour: toward the nearest point of it, which is the
            # contour's normal where the account is off it, the depth's gradient where
            # the account is on it already
            off = math.hypot(de, dn)
            if off > 0.1:
                n_e, n_n = de / off, dn / off
            else:
                n = math.radians(normal_deg)
                n_e, n_n = math.sin(n), math.cos(n)
            moved = r.update_line(de, dn, n_e, n_n, SOUNDING_ACROSS_SIGMA_NM)
        text = f"{chant(fathoms, not deep)}; {ground}."
        self._record_cast(tick, depth_m, ground, text, deep, moved, found is not None)

    def _record_cast(
        self,
        tick: int,
        depth_m: float | None,
        ground: str,
        text: str,
        deep: bool,
        moved: float = 0.0,
        matched: bool = False,
    ) -> None:
        r = self.reckoning
        cast = Sounding(tick, depth_m, ground, text, r.lat_deg, r.lon_deg, deep)
        self.last_cast = cast
        r.soundings.append(cast)
        self.world.record(
            Severity.NOTABLE,
            "sounding",
            text,
            data={
                "depth_m": None if depth_m is None else round(depth_m, 2),
                "fathoms": None if depth_m is None else round(units.m_to_fathoms(depth_m), 2),
                "ground": ground,
                "deep": deep,
                "reckoning": r.words,
                "moved_nm": round(moved, 2),
                "matched": matched,
            },
        )

    # -- bearings -----------------------------------------------------------------------

    def take_bearing(self, name: str) -> tuple[str, dict[str, Any]]:
        """`take a bearing of <mark>`: the mark in sight by the lookout's name, or 'the
        land' or 'the light' for the nearest such; the bearing by compass with its error,
        the reckoning drawn onto its line; a transit of the chart's when both its marks
        are in sight and in one. Refused in words when it is not in sight."""
        from freesail.evolutions.runner import OrderError

        world = self.world
        lookout = world.lookout
        if lookout is None:
            raise OrderError("No chart of these waters: there is no mark to take a bearing of.")
        found = lookout.find(name)
        if found is None:
            transit = self._transit_named(name)
            if transit is not None:
                return self._transit_bearing(transit)
            if not lookout.sightings:
                raise OrderError("Nothing is in sight to take a bearing of.")
            from freesail.world.lookout import SHORE_ID

            if all(s.feature.id == SHORE_ID for s in lookout.sightings):
                raise OrderError(
                    "The land close aboard is no mark of the chart to take a bearing of; "
                    "name a headland when one is made out."
                )
            raise OrderError(
                f"{_head(name)} is not in sight; in sight: "
                f"{lookout.reading(float(world.ship.heading))['words']}."
            )
        heading = float(world.ship.heading)
        error = self.errors.course_error_rad(heading) + self.stream.gauss(
            0.0, math.radians(BEARING_SIGMA_DEG)
        )
        laid = (math.radians(found.bearing_deg) + error) % units.TWO_PI
        self.bring_up()
        r = self.reckoning
        moved = r.update_bearing(found.feature.position, laid, _bearing_sigma_nm(found.distance_m))
        # the distance off by estimation, the lookout's held figure (package 33b), a
        # second line along the bearing
        judged_nm = max(0.1, found.judged_m / units.NAUTICAL_MILE)
        moved += r.update_distance(
            found.feature.position, laid, judged_nm, DISTANCE_BY_ESTIMATION_FRACTION * judged_nm
        )
        estimate = estimate_words(judged_nm * units.NAUTICAL_MILE)
        record = Bearing(
            world.clock.tick,
            found.feature.id,
            found.feature.name,
            math.degrees(laid),
            found.feature.lat_deg,
            found.feature.lon_deg,
            estimate,
        )
        r.bearings.append(record)
        text = (
            f"{_head(found.feature.name)} bore {units.point_name(laid)}, {estimate} by estimation."
        )
        return text, record.to_dict() | {"reckoning": r.words, "moved_nm": round(moved, 2)}

    def _transit_named(self, name: str) -> Any:
        chart = self.world.chart
        if chart is None:
            return None
        key = _key(name)
        for f in chart.features.values():
            if f.kind == "transit" and _key(f.name) == key:
                return f
        return None

    def _transit_bearing(self, transit: Any) -> tuple[str, dict[str, Any]]:
        from freesail.evolutions.runner import OrderError

        world = self.world
        chart = world.chart
        marks = [chart.feature(m) for m in transit.marks]
        seen = {s.feature.id for s in world.lookout.sightings}
        if any(m is None for m in marks) or not all(m.id in seen for m in marks):
            raise OrderError(f"The marks of {transit.name} are not both in sight.")
        near, far = marks[0], marks[1]
        b_line, _ = bearing_and_distance(far.position, near.position)
        b_ship, dist = bearing_and_distance(world.position, near.position)
        if abs(units.wrap_pi(math.radians(b_ship - b_line))) > math.radians(2.0):
            raise OrderError(
                f"{_head(near.name)} is not yet on with {far.name}; she is not on the transit."
            )
        self.bring_up()
        r = self.reckoning
        moved = r.update_bearing(near.position, math.radians(b_line), TRANSIT_SIGMA_NM)
        record = Bearing(
            world.clock.tick,
            transit.id,
            transit.name,
            b_line,
            near.lat_deg,
            near.lon_deg,
            estimate_words(dist),
        )
        r.bearings.append(record)
        point = units.point_name(math.radians(b_line))
        text = f"{_head(transit.name)}: on the transit, bearing {point}."
        data = record.to_dict() | {"reckoning": r.words, "moved_nm": round(moved, 2)}
        return text, data | {"transit": True}

    # -- the noon and the day's work ------------------------------------------------------

    def noon_by_the_sun(self) -> datetime:
        """Today's noon by the sun on the ship's clock: the sun's meridian passage at her
        easting (`core.sun.Sun.transit`)."""
        world = self.world
        return world._sun_now().transit(world.clock.ship_time, world.ship_x)

    def _tick_noon(self) -> None:
        world = self.world
        t = world.clock.ship_time
        if t.second != 0:
            return
        from freesail.world.sights import SIGHT_ON_DECK_MINUTES

        if self._transit is None or self._transit.date() != t.date():
            self._transit = self.noon_by_the_sun()
            if t > self._transit + timedelta(hours=1):
                # noon passed before the book was opened (a scenario begun in the
                # afternoon): no day's work today, as a sunrise before tick 0 is no event
                self._noon_done_day = t.date()
        if self._noon_done_day == t.date():
            return
        if t < self._transit - timedelta(minutes=SIGHT_ON_DECK_MINUTES):
            return
        if t >= self._transit and self._noon_done_day != t.date():
            self.days_work(automatic=True)
            return
        # the master on deck with his instrument for the last quarter of an hour
        if not self.master.occupied and world.clock.tick < _tick_of(world, self._transit):
            self.master.occupy("on deck", _tick_of(world, self._transit), "sight")

    def observe_sun(self) -> tuple[str, dict[str, Any]]:
        """`observe the sun` by order: the noon sight now if the sun is near the meridian
        and the sky allows; refused in words otherwise."""
        from freesail.evolutions.runner import OrderError
        from freesail.world.sights import SIGHT_ON_DECK_MINUTES

        world = self.world
        t = world.clock.ship_time
        if self._transit is None or self._transit.date() != t.date():
            self._transit = self.noon_by_the_sun()
        if self.last_sight is not None and self.sight_day == t.date():
            s = self.last_sight
            return f"The sun was observed at noon: latitude {s.words}.", {"sight": s.to_dict()}
        if t < self._transit - timedelta(minutes=SIGHT_ON_DECK_MINUTES):
            raise OrderError(
                f"The sun is not yet on the meridian; noon by the sun is at "
                f"{self._transit:%H:%M} by the clock."
            )
        if t > self._transit + timedelta(hours=1):
            why = self.sight_refused or "the sun is well past the meridian"
            raise OrderError(f"Noon is past; {why}.")
        return self.days_work(automatic=False)

    def days_work(self, automatic: bool) -> tuple[str, dict[str, Any]]:
        """The day's work at noon (Falconer 1780, 'Dead-reckoning', 'Log-board'): the
        reckoning brought up from the log-board, the noon latitude taken if the sky
        allows and put in place of the reckoned one, the longitude carried by account;
        the noon line; the master below to work it."""
        from freesail.world import sights

        world = self.world
        t = world.clock.ship_time
        tick = world.clock.tick
        self.bring_up()
        r = self.reckoning
        run, cmg = r.since_noon()
        account_lat = r.lat_deg
        result = sights.noon_sight(world, self.master, self.stream)
        observed: float | None = None
        self.sight_day = t.date()
        if result.sight is not None:
            self.last_sight = result.sight
            self.sight_refused = None
            observed = result.sight.latitude_deg
            r.update_latitude(observed, result.sight.sigma_nm)
        else:
            self.last_sight = None
            self.sight_refused = result.refusal
        self._noon_done_day = t.date()
        first = not self.noon_had
        self.noon_had = True
        noon = Noon(tick, r.lat_deg, r.lon_deg, observed, account_lat, run, cmg)
        r.noons.append(noon)
        r.noon_mark = (tick, r.lat_deg, r.lon_deg)
        r.run_since_noon_nm = 0.0
        lat_words = _lat_words(r.lat_deg)
        lon_words = _lon_words(r.lon_deg)
        if observed is not None:
            head = (
                f"Noon. Latitude by observation {_lat_words(observed)}; the reckoning was "
                f"{_lat_words(account_lat)}."
            )
        else:
            head = f"Noon. No sight; {result.refusal}. Latitude by account {lat_words}."
        since = "since the departure" if first else "since yesterday"
        made = (
            f" Course made good {since} {units.point_name(math.radians(cmg))}, {miles_words(run)}."
            if cmg is not None and run >= 0.5
            else ""
        )
        text = f"{head}{made} Longitude by account {lon_words}."
        data = {
            "noon": noon.to_dict(),
            "sight": None if result.sight is None else result.sight.to_dict(),
            "refusal": result.refusal,
            "reckoning": r.words,
            "uncertainty": r.uncertainty_words,
            "ellipse": r.ellipse(),
            "automatic": automatic,
        }
        self.master.occupy("below", tick + DAYS_WORK_MINUTES * 60, "day's work")
        if automatic:
            world.record(Severity.NOTABLE, "reckoning.noon", text, data=data)
        return text, data

    def work_up(self) -> tuple[str, dict[str, Any]]:
        """`work up the reckoning` on demand: the account brought up to now and said."""
        self.bring_up()
        r = self.reckoning
        run, cmg = r.since_noon()
        made = (
            f"; run since noon {miles_words(run)}, course made good "
            f"{units.point_name(math.radians(cmg))}"
            if cmg is not None and run >= 0.5 and self.noon_had
            else ""
        )
        text = f"The reckoning worked up: {r.words}{made}. {r.uncertainty_words}"
        data = {"reckoning": r.words, "ellipse": r.ellipse(), "run_since_noon_nm": round(run, 1)}
        return text, data

    def set_reckoning(self, pos: Position) -> tuple[str, dict[str, Any]]:
        """`set the reckoning to <lat> <long>`: the captain overrides the master."""
        world = self.world
        self.bring_up()
        self.reckoning.set_position(pos, world.clock.tick)
        text = f"The reckoning set to {format_position(pos)} by the captain's order."
        data = {"reckoning": self.reckoning.words, "lat_deg": pos.lat_deg, "lon_deg": pos.lon_deg}
        return text, data

    def allow_set(self, knots: float, toward_rad: float | None) -> tuple[str, dict[str, Any]]:
        """`allow <n> knots of set to <direction>`: the master's allowance in the
        traverse; none clears it."""
        self.bring_up()
        if knots <= 0.0 or toward_rad is None:
            self.reckoning.set_allowance = None
            text = "No set allowed for in the reckoning."
        else:
            self.reckoning.set_allowance = (knots, toward_rad)
            text = (
                f"Allowing {knots_words(knots)} of set to the "
                f"{units.point_name(toward_rad, full=True)} in the reckoning."
            )
        return text, {"knots": knots}

    def shape_course(self, place: str) -> tuple[float, str]:
        """`shape a course for <place>`: the course from the reckoning to the chart's
        place (never from the truth); (the heading in radians, the words). Refused where
        the chart has no such place."""
        from freesail.evolutions.runner import OrderError

        world = self.world
        chart = world.chart
        if chart is None:
            raise OrderError("No chart of these waters: there is no place to shape a course for.")
        key = _key(place)
        feature = None
        for f in chart.features.values():
            if _key(f.name) == key or _key(f.modern) == key:
                feature = f
                break
        if feature is None:
            kinds = ("town", "place", "anchorage", "road", "headland", "island")
            known = sorted({f.name for f in chart.features.values() if f.kind in kinds})
            names = ", ".join(known[:12])
            more = f", and {len(known) - 12} more" if len(known) > 12 else ""
            raise OrderError(f"The chart has no place named {place!r}; it names {names}{more}.")
        self.bring_up()
        r = self.reckoning
        bearing, dist = bearing_and_distance(r.position, feature.position)
        heading = math.radians(bearing)
        words = (
            f"Shaped a course for {feature.name}: {units.point_name(heading)} by account, "
            f"{miles_words(dist / units.NAUTICAL_MILE)}"
        )
        # the chart in the captain's hands (package 33b; decision 30): the straight line
        # from the account checked against the charted dangers, the master's warning and
        # no more (the pilot of package 35 is the better answer; the helm rules of the
        # book have no guard, which is the captain's business)
        from freesail.world.chart import DANGER_PASS_NM

        within = DANGER_PASS_NM * units.NAUTICAL_MILE
        passes = chart.line_passes(r.position, feature.position, within)
        passes = [p for p in passes if p[0].id != feature.id]
        if passes:
            crossed = [f.name for f, _off, crosses in passes if crosses]
            near = [f.name for f, _off, crosses in passes if not crosses]
            said = []
            if crossed:
                said.append(f"the line crosses {_and(crossed)}")
            if near:
                said.append(f"the line passes {_and(near)} within a mile")
            words += "; " + " and ".join(said)
        return heading, words + "."

    # -- the chart in the captain's hands (package 33b; decision 30) ---------------------

    def _charted(self, name: str) -> Any:
        """A feature of the chart by name, for the queries by account; refused in words
        when the chart has no such name."""
        from freesail.evolutions.runner import OrderError

        chart = self.world.chart
        if chart is None:
            raise OrderError("No chart of these waters: there is nothing charted to ask of.")
        feature = chart.find_feature(name)
        if feature is None:
            raise OrderError(f"The chart has nothing named {name!r}.")
        return feature

    def by_chart(self, name: str) -> dict[str, Any] | None:
        """`the bearing of <mark> by the chart` and `the distance to <mark>`: from the
        account brought up to now to the charted feature, in sight or not, "by account"
        in the words; None where the chart has no such name."""
        chart = self.world.chart
        if chart is None or not name:
            return None
        feature = chart.find_feature(name)
        if feature is None:
            return None
        now = self.account_now()
        bearing, dist = bearing_and_distance(now, feature.position)
        heading = math.radians(bearing)
        laid = (heading + self.errors.course_error_rad(heading)) % units.TWO_PI  # by compass
        nm = dist / units.NAUTICAL_MILE
        return {
            "id": feature.id,
            "name": feature.name,
            "bearing": laid,
            "bearing_true_deg": round(bearing, 1),
            "metres": dist,
            "words": f"{units.point_name(laid)} by account, {miles_words(nm)}",
            "distance_words": f"{miles_words(nm)} by account",
        }

    def dangers(self, within_nm: float | None = None) -> dict[str, Any] | None:
        """`the dangers`: the charted dangers within so many miles of the account (ten
        unless said), the nearest first, by name, bearing by compass and distance; None
        where there is no chart, or none within reach (`no_dangers_words`)."""
        from freesail.world.chart import DANGERS_WITHIN_NM

        chart = self.world.chart
        if chart is None:
            return None
        radius = float(within_nm) if within_nm else DANGERS_WITHIN_NM
        now = self.account_now()
        found = chart.dangers_near(now, radius * units.NAUTICAL_MILE)
        if not found:
            return None
        items = []
        for f, bearing, dist in found:
            heading = math.radians(bearing)
            laid = (heading + self.errors.course_error_rad(heading)) % units.TWO_PI
            items.append(
                {
                    "id": f.id,
                    "name": f.name,
                    "kind": f.kind,
                    "bearing": laid,
                    "metres": dist,
                    "words": f"{f.name} {units.point_name(laid)}, "
                    f"{miles_words(dist / units.NAUTICAL_MILE)}",
                }
            )
        words = "; ".join(i["words"] for i in items[:8])
        if len(items) > 8:
            words += f"; and {len(items) - 8} more"
        return {
            "metres": items[0]["metres"],
            "words": f"{words}: by account, within {miles_words(radius)}",
            "items": items,
            "within_nm": radius,
        }

    def no_dangers_words(self) -> str:
        from freesail.world.chart import DANGERS_WITHIN_NM

        if self.world.chart is None:
            return "no chart of these waters"
        return f"no charted danger within {miles_words(DANGERS_WITHIN_NM)} of the account"

    # -- the chronometer (package 33b; spec §14; N §4(b)) ---------------------------------

    def _no_chronometer(self) -> None:
        from freesail.evolutions.runner import OrderError

        if self.chronometer is None:
            raise OrderError(
                "There is no chronometer aboard: the longitude is by account, and by lunar "
                "when the moon serves."
            )

    def wind_chronometer(self) -> tuple[str, dict[str, Any]]:
        """`wind the chronometer`: wound by order; one that had run down is set going
        again by the deck watch, which is the ship's time by the account, so it keeps the
        account's longitude error in its time until a lunar corrects it."""
        self._no_chronometer()
        c = self.chronometer
        world = self.world
        t = world.clock.ship_time
        if c.going:
            text = c.wind(t)
            return text, {"chronometer": c.to_dict(), "set": False}
        from freesail.world.sights import _SECONDS_PER_DEG

        self.bring_up()
        c.going = True
        c.wind(t)
        # the master sets it from the local time by the sun and his longitude by account
        c.set_error_s = (world.position.lon_deg - self.reckoning.lon_deg) * _SECONDS_PER_DEG
        c.set_error_s -= c.offset_s + c.drift_s_per_day * c.days_since_rated(t)
        text = (
            f"Wound {c.name} and set it going by the deck watch and the account; it keeps "
            f"no Greenwich time now but {self.master.name}'s, until a lunar corrects it."
        )
        return text, {"chronometer": c.to_dict(), "set": True}

    def compare_watches(self) -> tuple[str, dict[str, Any]]:
        """`compare the watches`: the chronometer against the deck watch, which keeps the
        ship's time."""
        from freesail.world.sights import greenwich_time

        self._no_chronometer()
        c = self.chronometer
        world = self.world
        t = world.clock.ship_time
        if not c.going:
            text = f"Compared the watches: {c.name} is dead, not having been wound."
            return text, {"chronometer": c.to_dict()}
        gmt = c.masters_gmt(greenwich_time(world), t)
        between = (gmt - t).total_seconds()
        sign = "" if between >= 0 else "-"
        m, s = divmod(int(round(abs(between))), 60)
        h, m = divmod(m, 60)
        text = (
            f"Compared the watches: {c.name} {gmt:%Hh %Mm %Ss} at Greenwich, the deck watch "
            f"{t:%Hh %Mm %Ss}; {sign}{h}h {m:02d}m {s:02d}s between them."
        )
        return text, {"chronometer": c.to_dict(), "between_s": round(between)}

    def take_time_sight(self) -> tuple[str, dict[str, Any]]:
        """`take a sight for the longitude` (N §4(b)): the longitude by chronometer, the
        reckoning's east-west axis updated by it; refused in words."""
        from freesail.evolutions.runner import OrderError
        from freesail.world import sights

        world = self.world
        if self.master.occupied and self.master.place == "below":
            raise OrderError(
                f"{self.master.name} is below at the {self.master.occupied_with}; wait for him."
            )
        sight, refusal = sights.time_sight(world, self.master, self.chronometer, self.stream)
        if sight is None:
            raise OrderError(f"No sight for the longitude: {refusal}.")
        self.bring_up()
        r = self.reckoning
        account_lon = r.lon_deg
        moved = r.update_longitude(sight.longitude_deg, sight.sigma_nm)
        self.last_time_sight = sight
        tick = world.clock.tick
        self.master.occupy("below", tick + sights.TIME_SIGHT_WORK_MINUTES * 60, "time sight")
        c = self.chronometer
        where = f" from {c.where}" if c.where else " from its rating"
        trust = _round_miles(2.0 * sight.sigma_nm)
        text = (
            f"{'Forenoon' if sight.forenoon else 'Afternoon'}. The sun's altitude for the time: "
            f"longitude by chronometer {sight.words}, {c.name} {sight.days_since_rated} days"
            f"{where}; the reckoning was {_lon_words(account_lon)}. {self.master.name} would "
            f"trust it within {miles_words(trust)}."
        )
        data = {
            "sight": sight.to_dict(),
            "reckoning": r.words,
            "moved_nm": round(moved, 2),
            "ellipse": r.ellipse(),
        }
        return text, data

    # -- the lunar (package 33b; spec §14; N §4(c), §5) --------------------------------

    def take_lunar(self, asked: str | None) -> str:
        """`take a lunar [of the sun | of <star>]`: the conditions checked from the
        moon, refused in the registry's words; allowed, the master and two mates to the
        quarterdeck with the sextants for a quarter of an hour (the evolution), the
        result an hour of ship's time later."""
        from freesail.evolutions.runner import OrderError
        from freesail.world import sights

        world = self.world
        if world.position is None:
            raise OrderError("No lunar to be had: there is no sea here.")
        body, refusal = sights.lunar_body(world, sights.moon_now(world), asked)
        if body is None:
            raise OrderError(refusal + ".")
        if self.master.occupied:
            raise OrderError(
                f"{self.master.name} is {self.master.place} at the {self.master.occupied_with}; "
                f"wait for him."
            )
        if self._lunar_pending is not None:
            raise OrderError("A lunar is being cleared below already.")
        runner = (getattr(world.ship, "extra", None) or {}).get("evolutions")
        tick = world.clock.tick
        self._lunar_in_hand = body
        of = "the sun" if body == "the sun" else body
        if runner is None or not hasattr(runner, "instances"):
            self._lunar_taken()
            return f"A set of distances of {of} and the moon taken."
        line = runner.start(world.ship, "take_lunar", LOG_SUBJECT, {"body": of})
        self.master.occupy("on deck", tick + sights.LUNAR_ON_DECK_MINUTES * 60, "lunar")
        return line

    def _lunar_taken(self) -> None:
        """The distances are taken: the result drawn now from the truth and the seed
        (the moment of the observation is the moment that matters) and given when the
        master has cleared it below, an hour of ship's time later."""
        from freesail.world import sights

        world = self.world
        body = self._lunar_in_hand or "the sun"
        self._lunar_in_hand = None
        chron_lon = None
        if self.chronometer is not None and self.chronometer.going:
            # what the chronometer gives at this moment, for the error by lunar
            chron_lon = sights.chronometer_longitude(
                world, self.master, self.chronometer, self.stream
            )
        result = sights.lunar_result(world, self.master, self.stream, body, chron_lon)
        due = world.clock.tick + sights.LUNAR_CLEARING_MINUTES * 60
        self._lunar_pending = (due, result)
        self.master.occupy("below", due, "lunar")
        world.record(
            Severity.ROUTINE,
            LUNAR_TAKEN_KIND,
            f"The distances taken; {self.master.name} below to clear them.",
            data={"body": body, "due_tick": due},
        )

    def _lunar_cleared(self) -> None:
        """The lunar cleared: the log's line, the reckoning updated by it."""
        from freesail.world import sights

        world = self.world
        assert self._lunar_pending is not None
        _due, lunar = self._lunar_pending
        self._lunar_pending = None
        self.last_lunar = lunar
        self.bring_up()
        r = self.reckoning
        account_lon = r.lon_deg
        moved = r.update_longitude(lunar.longitude_deg, lunar.sigma_nm)
        of = lunar.body
        master = self.master.name
        text = (
            f"A set of distances of {of} and the moon taken by {master} and two of the young "
            f"gentlemen, and cleared: longitude by lunar {lunar.words}, which he would trust "
            f"{lunar.trust_words}; the reckoning was {_lon_words(account_lon)}."
        )
        fast = lunar.chronometer_fast_s
        if fast is not None and self.chronometer is not None:
            c = self.chronometer
            if abs(fast) < sights.CHRONOMETER_FAULT_S:
                verdict = f"and he finds no fault in {c.name}"
            else:
                sense = "gaining" if fast > 0 else "losing"
                verdict = f"and he thinks it {sense} on its rate, by {_seconds_words(abs(fast))}"
            gave = _lon_words(lunar.chronometer_longitude_deg)
            text += f" {_head(c.name)} gave {gave}, {verdict}."
        data = {
            "lunar": lunar.to_dict(),
            "reckoning": r.words,
            "moved_nm": round(moved, 2),
            "ellipse": r.ellipse(),
            "chronometer_fast_s": None if fast is None else round(fast, 1),
        }
        world.record(Severity.NOTABLE, "reckoning.lunar", text, data=data)

    # -- the variation by observation (package 33b; decision 30) -------------------------

    def observe_variation(self, amplitude: bool) -> tuple[str, dict[str, Any]]:
        """`observe an amplitude` at sunrise or sunset, `observe an azimuth` by day: the
        variation by observation, which the master allows from now in place of the
        chart's; refused in words in cloud or with the sun not where the sight wants it."""
        from freesail.evolutions.runner import OrderError
        from freesail.world import sights

        world = self.world
        if world.position is None:
            raise OrderError("No sun to observe: there is no sea here.")
        var, refusal, figures = sights.amplitude_or_azimuth(
            world, self.errors, self.stream, amplitude, VARIATION_1805_DEG
        )
        if var is None:
            what = "amplitude" if amplitude else "azimuth"
            raise OrderError(f"No {what} to be had: {refusal}.")
        self.bring_up()
        before = self.variation
        was = (
            f"where the chart gave {before.words}"
            if before.by.startswith("the chart")
            else f"where he allowed {before.words} before"
        )
        self.errors.allow_variation(var.deg_west)
        self.variation = var
        compass = units.point_name(math.radians(figures["compass_bearing_deg"]))
        if amplitude:
            when = "rising" if figures["rising"] else "setting"
            head = f"Observed the sun's amplitude at its {when}, bearing {compass} by compass"
        else:
            head = f"Observed the sun's azimuth, bearing {compass} by compass"
        text = (
            f"{head}: variation of the compass {var.words}, {was}; {self.master.name} allows it "
            f"in the reckoning from now."
        )
        return text, {"variation": var.to_dict(), "figures": figures}

    # -- the readings -----------------------------------------------------------------

    def chronometer_reading(self) -> dict[str, Any] | None:
        """`the chronometer`: its time, the days since rated, and the master's trust in
        miles of longitude (the number the dialect compares); None without one."""
        c = self.chronometer
        if c is None:
            return None
        world = self.world
        t = world.clock.ship_time
        lat = world.position.lat_deg if world.position is not None else 50.0
        doubt = c.doubt_nm(t, lat)
        trust = _round_miles(2.0 * doubt) if c.going else 0
        words = c.words(world)
        if c.going:
            words += f"; {self.master.name} would trust it within {miles_words(trust)}"
        return {"metres": units.nm_to_m(doubt), "words": words, "going": c.going} | c.to_dict()

    def no_chronometer_words(self) -> str:
        return "the ship carries no chronometer"

    def longitude_by_chronometer_reading(self) -> dict[str, Any] | None:
        """`the longitude by chronometer`: today's time sight, with the days since rated
        and the master's trust; None without one today."""
        s = self.last_time_sight
        if s is None or s.tick // 86400 != self.world.clock.tick // 86400:
            return None
        c = self.chronometer
        where = f" from {c.where}" if c is not None and c.where else " from its rating"
        trust = _round_miles(2.0 * s.sigma_nm)
        return {
            "lat_deg": self.reckoning.lat_deg,
            "lon_deg": s.longitude_deg,
            "words": f"{s.words} by chronometer, {s.days_since_rated} days{where}, which "
            f"{self.master.name} would trust within {miles_words(trust)}",
            "sigma_nm": s.sigma_nm,
        }

    def no_time_sight_words(self) -> str:
        if self.chronometer is None:
            return "no longitude by chronometer: the ship carries none"
        if not self.chronometer.going:
            return f"no longitude by chronometer: {self.chronometer.name} is dead"
        return "no sight for the longitude today"

    def longitude_by_lunar_reading(self) -> dict[str, Any] | None:
        """`the longitude by lunar`: the last lunar, with its date and the master's trust."""
        lunar = self.last_lunar
        if lunar is None:
            return None
        age = age_words(self.world.clock.tick - lunar.tick)
        return {
            "lat_deg": self.reckoning.lat_deg,
            "lon_deg": lunar.longitude_deg,
            "words": f"{lunar.words} by lunar of {lunar.body}, {age}, which {self.master.name} "
            f"would trust {lunar.trust_words}",
            "sigma_nm": lunar.sigma_nm,
        }

    def no_lunar_words(self) -> str:
        from freesail.world import sights

        if self._lunar_pending is not None:
            return "a lunar is being cleared below"
        _body, refusal = sights.lunar_body(self.world, sights.moon_now(self.world), None)
        if refusal:
            return refusal[:1].lower() + refusal[1:]
        return "no lunar taken yet; the moon serves"

    def chronometer_error_reading(self) -> dict[str, Any] | None:
        """`the chronometer's error by lunar`: the last lunar against the chronometer,
        in seconds of time and in miles of longitude (the number the dialect compares)."""
        lunar = self.last_lunar
        if lunar is None or lunar.chronometer_fast_s is None:
            return None
        from freesail.world import sights

        fast = lunar.chronometer_fast_s
        lat = self.reckoning.lat_deg
        miles = abs(fast) / 240.0 * 60.0 * math.cos(math.radians(lat))
        c = self.chronometer
        name = c.name if c is not None else "the chronometer"
        if abs(fast) < sights.CHRONOMETER_FAULT_S:
            words = f"{name} shows no fault by the lunar of {lunar.body}"
        else:
            sense = "gaining" if fast > 0 else "losing"
            words = (
                f"{name} {sense} on its rate by {_seconds_words(abs(fast))}, "
                f"{miles_words(miles)} of longitude, by the lunar of {lunar.body}"
            )
        return {"metres": units.nm_to_m(miles), "words": words, "fast_s": round(fast, 1)}

    def no_chronometer_error_words(self) -> str:
        if self.chronometer is None:
            return "the ship carries no chronometer"
        if self.last_lunar is None:
            return "no lunar taken yet to check the chronometer by"
        return "the last lunar had no chronometer to check"

    def moon_reading(self) -> dict[str, Any] | None:
        """`the moon`: its age, its phase, whether it is up and in distance of a body."""
        from freesail.world import sights

        world = self.world
        moon = sights.moon_now(world)
        if moon is None:
            return None
        allowed, _ = sights.sky_allows(getattr(world, "conditions", None))
        age = int(round(moon.age_days))
        age_said = "new" if age == 0 else f"{number_words(age)} day{'s' if age != 1 else ''} old"
        if moon.up:
            alt = int(round(moon.altitude_deg))
            where = f"up, {number_words(alt)} degrees high"
            if not allowed:
                where += " behind the cloud"
        else:
            where = "not up"
        body, refusal = sights.lunar_body(world, moon, None)
        if body is not None:
            distance = f"in distance of {body}"
        else:
            distance = refusal.replace("No lunar to be had: ", "no lunar: ")
        return {
            "in_sight": bool(moon.up and allowed),
            "words": f"{age_said}, {moon.phase}; {where}; {distance}",
            "age_days": round(moon.age_days, 2),
            "phase": moon.phase,
            "fraction": round(moon.fraction, 3),
            "altitude_deg": round(moon.altitude_deg, 1),
            "azimuth_deg": round(moon.azimuth_deg, 1),
            "up": moon.up,
            "body": body,
        }

    def variation_reading(self) -> float:
        """`the variation` the master allows, west positive, in radians; the words carry
        its source and its date (`api.readings.Angle`)."""
        return math.radians(self.variation.deg_west)

    def to_dict(self) -> dict[str, Any]:
        """The captain's chart's block (`api.queries.snapshot`): the reckoning brought up
        to now, its ellipse, the track by account, the noons, the bearings, the
        soundings, the master, the chronometer, the longitude sights and the variation;
        the truth nowhere in it."""
        out = self.reckoning.to_dict()
        now = self.account_now()
        out["lat_deg"], out["lon_deg"] = round(now.lat_deg, 5), round(now.lon_deg, 5)
        out["words"] = f"{format_position(now)} by account"
        out["master"] = self.master.to_dict()
        out["log_interval_h"] = self.log_interval_h
        out["last_log_kn"] = self.last_log_read_kn
        out["chronometer"] = None if self.chronometer is None else self.chronometer.to_dict()
        out["time_sight"] = None if self.last_time_sight is None else self.last_time_sight.to_dict()
        out["lunar"] = None if self.last_lunar is None else self.last_lunar.to_dict()
        out["variation"] = self.variation.to_dict()
        return out

    # -- the readings of package 33a ------------------------------------------------------

    def depth_reading(self) -> float | None:
        """`the depth`: the last cast's depth in metres, None before a cast or without bottom."""
        return self.last_cast.depth_m if self.last_cast is not None else None

    def ground_reading(self) -> dict[str, Any] | None:
        """`the ground`: the last cast's ground with its age."""
        cast = self.last_cast
        if cast is None or cast.depth_m is None:
            return None
        age = self.world.clock.tick - cast.tick
        return {
            "words": cast.ground,
            "age_s": age,
            "cast": cast.words,
            "said": f"{cast.ground}, by the cast {age_words(age)}",
        }

    def since_noon_reading(self) -> tuple[float, float | None] | None:
        """`the distance run since noon` and `the course made good`: by account, from the
        account brought up to now; None before the first noon, when 'since noon' has no
        meaning (the run is since the departure, which `no_noon_words` says)."""
        if not self.noon_had:
            return None
        r = self.reckoning
        now = self.account_now()
        _, lat0, lon0 = r.noon_mark
        bearing, dist = bearing_and_distance(Position(lat0, lon0), now)
        run = r.run_since_noon_nm + (self.last_log_read_kn or 0.0) * (
            (self.world.clock.tick - r.last_step_tick) / 3600.0
        )
        return run, (None if dist < 0.1 * units.NAUTICAL_MILE else bearing)

    def no_noon_words(self) -> str:
        if self.noon_had:
            return "no distance made good since noon"
        r = self.reckoning
        run = r.run_since_noon_nm + (self.last_log_read_kn or 0.0) * (
            (self.world.clock.tick - r.last_step_tick) / 3600.0
        )
        return f"no noon yet; the run since the departure is {miles_words(run)} by account"

    def no_cast_words(self) -> str:
        if self.last_cast is None:
            return "no cast yet; the lead has not been hove"
        if self.last_cast.depth_m is None:
            age = age_words(self.world.clock.tick - self.last_cast.tick)
            return f"no bottom by the last cast, {age}"
        return "not to be had"

    def latitude_reading(self) -> float | None:
        """`the latitude by observation`: today's, in degrees; None without a sight."""
        t = self.world.clock.ship_time
        if self.last_sight is not None and self.sight_day == t.date():
            return float(self.last_sight.latitude_deg)
        return None

    def no_sight_words(self) -> str:
        t = self.world.clock.ship_time
        if self.sight_day == t.date() and self.sight_refused:
            return f"No sight today; {self.sight_refused}."
        transit = self._transit
        if transit is None or transit.date() != t.date():
            transit = self.noon_by_the_sun()
        if t < transit:
            return f"No sight yet today; noon by the sun is at {transit:%H:%M}."
        return "No sight today."

    def bearing_reading(self, name: str | None) -> dict[str, Any] | None:
        """`the bearing of <mark>`: the mark in sight by name, its bearing by compass
        (the master's, with the compass's errors and none of the sight's) and the
        lookout's estimate of the distance; None when not in sight."""
        lookout = self.world.lookout
        if lookout is None or not name:
            return None
        found = lookout.find(name)
        if found is None:
            return None
        heading = float(self.world.ship.heading)
        laid = math.radians(found.bearing_deg) + self.errors.course_error_rad(heading)
        laid %= units.TWO_PI
        return {
            "id": found.feature.id,
            "name": found.feature.name,
            "bearing": laid,
            "words": f"{units.point_name(laid)}, {estimate_words(found.judged_m)}",
            "estimate": estimate_words(found.judged_m),
        }

    def reckoning_reading(self) -> dict[str, Any]:
        """`the reckoning`: the account brought up to now, in degrees and in words."""
        now = self.account_now()
        return {
            "lat_deg": now.lat_deg,
            "lon_deg": now.lon_deg,
            "words": f"{format_position(now)} by account",
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + f" and {names[-1]}"


def _seconds_words(seconds: float) -> str:
    """'a minute and twenty seconds', 'forty seconds', 'two minutes'."""
    n = int(round(seconds))
    m, s = divmod(n, 60)
    minutes = "" if m == 0 else ("a minute" if m == 1 else f"{number_words(m)} minutes")
    secs = "" if s == 0 else f"{number_words(s)} second{'s' if s != 1 else ''}"
    if minutes and secs:
        return f"{minutes} and {secs}"
    return minutes or secs or "no time"


def _variation_words(deg_west: float, by: str) -> str:
    from freesail.world.sights import Variation

    return Variation(deg_west, by).words


def _ship_of_war(ship: Any) -> bool:
    """A ship of war musters marines (Falconer's "ships of war" heave the log hourly)."""
    from freesail.crew.model import Station

    crew = (getattr(ship, "extra", None) or {}).get("crew")
    if crew is None:
        spec = getattr(ship, "spec", None)
        stations = getattr(getattr(spec, "crew", None), "stations", None) or {}
        return bool(stations.get("marines"))
    return bool(crew.by_station.get(Station.MARINES))


def _speed_through_water(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    if dyn is not None:
        return max(0.0, float(dyn.u))
    return float(getattr(ship, "speed", 0.0))


def _bearing_sigma_nm(distance_m: float) -> float:
    """The doubt across a bearing's line at the mark's distance: a degree and a half at
    ten miles is a quarter of a mile (N §3)."""
    return max(0.05, distance_m / units.NAUTICAL_MILE * math.tan(math.radians(BEARING_SIGMA_DEG)))


def _tick_of(world: Any, when: datetime) -> int:
    return int((when - world.clock.start).total_seconds())


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


def _key(name: str) -> str:
    words = "".join(c if c.isalnum() or c.isspace() else " " for c in name.lower()).split()
    if words and words[0] == "the":
        words = words[1:]
    return " ".join(words)


def _lat_words(lat_deg: float) -> str:
    return format_position(Position(lat_deg, 0.0)).split(",")[0]


def _lon_words(lon_deg: float) -> str:
    return format_position(Position(0.0, lon_deg)).split(", ")[1]
