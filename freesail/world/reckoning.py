"""The reckoning: the captain's account of where she is (spec M5 §13, §15; the study
`docs/design/Navigation1805.md` §1, §3, §4(a); package 33a).

**The world keeps the truth and the captain keeps his account.** The truth is the
physics' `Position` (`World.position`, package 32), which no reading, no snapshot and no
drawing gives. The reckoning is a second position, kept here with a two-by-two
covariance, advanced at each heave of the log by the logged run along the course
steered, corrected as the master corrected it (for his chart's variation, for the
leeway he allowed when close-hauled, for the set he allowed if any), and grown by the
error terms of N §3; and updated by each observation as a line or a point measurement
by one rule (below). The master's errors come from the model's seeded draws
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

**One rule for every observation** (package 37e). A cast, a bearing, a distance, a noon
latitude, a longitude by lunar or by chronometer, a transit and a fix by cross bearings
are each a line (or two) with the master's own doubt of it, and each is believed by the
same rule (`Reckoning.observe_line`, `observe_point`): **weighed** by the two doubts, the
account's and the observation's, in the simplest Kalman form; **taken** whole, the
account laid down on it, when the account is plainly out by it (further off than
`OBSERVATION_OUT_SIGMAS` of the two doubts together); and **kept** when the weighing
would move the account under half a cable. The same thing seen again tells him nothing
new: what a second look at one mark, a second cast on the same ground or a second sight
with the same instrument shares with the first (the compass, the chart, the tide he
allowed, the horizon) is not narrowed twice. Each line of the log says which of the
three was done and by how much (`verdict_words`). The lookout's distance by estimation
is weighed and never taken; a sail is no mark and moves nothing.

**The doubt** grows by the hour whatever she is doing but riding at anchor: under way by
the terms above; hove to by her drift as the eye judges it; becalmed by the stream
alone. The stream's part lies along its set and grows no further than the stream can
set her (`STREAM_DOUBT_FRACTION`, `STREAM_DOUBT_HOURS`). His words give it as it lies,
"within three miles NE and SW, nor a mile across", when it is long and thin
(`doubt_words`).

**The master's tide** (package 37e, the owner's ruling). He works the tide into the
traverse himself, as one more course: from the hour of high water at the nearest place
in his epitome, the moon's age by his almanac, and what his sailing directions say of
the waters his *account* puts her in (`tide.Directions`, `BookTide`, `Navigation.book_tide`),
summed by the quarter hour. No line of it reads the world's tide or the ship's true
place. The captain's own `allow <n> knots of set` replaces it until `allow the tide by
the book` hands it back. A course shaped (`Navigation.shape_course`) is the course to
steer so that, against that tide and with the leeway he allows, she makes good the line
from the account to the place; it is worked once, and the line is tried against the
shore as against the charted dangers.

`Navigation` below is the World's glue: the log hove hourly (two-hourly in a vessel
that is not a ship of war, Falconer), the noon sight and the day's work at the sun's
noon, the master as the first named person with a skill and a place (spec §22's
minimum), the casts, the bearings and the fix by order (the master chooses the marks
that leave him the least doubt, `_choose_marks`), and the lines the log says for each
in the ship's-log voice.

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
from freesail.world.geo import (
    Position,
    bearing_and_distance,
    estimate_words,
    format_position,
    name_words,
)
from freesail.world.lookout import DISTANCE_BY_ESTIMATION_FRACTION as _LOOKOUT_ESTIMATE_FRACTION

__all__ = [
    "BEARING_LINE_FORM_FRACTION",
    "BEARING_SIGMA_DEG",
    "CHART_VARIATION_AGE_YEARS",
    "COMPASS_ALLOWANCE_DEG",
    "COMPASS_ALLOWANCE_OBSERVED_DEG",
    "CONTOUR_GRAIN_M",
    "CONTOUR_SEARCH_MIN_NM",
    "CONTOUR_TOLERANCE_DEEP_FATHOMS",
    "CONTOUR_TOLERANCE_HAND_FATHOMS",
    "DAYS_WORK_MINUTES",
    "DEEP_SEA_LEAD_FATHOMS",
    "DEEP_SEA_LEAD_MAX_KN",
    "DEPARTURE_SIGMA_NM",
    "DEVIATION_MAX_DEG",
    "FIX_ACCOUNT_DIFFERS",
    "FIX_MARKS_CONSIDERED",
    "FIX_MARKS_IN_ALL",
    "FIX_MIN_CUT_DEG",
    "FIX_NOTABLE_NM",
    "HAND_LEAD_FATHOMS",
    "HOVE_TO_DRIFT_KN",
    "HOVE_TO_DRIFT_SIGMA_KN",
    "KEPT",
    "HAND_LEAD_MARKS",
    "LEAD_DEEP_SIGMA_FATHOMS",
    "LEAD_HAND_SIGMA_FATHOMS",
    "LEEWAY_DOUBT_POINTS",
    "LEEWAY_ESTIMATE_ERROR_POINTS",
    "LEEWAY_ALLOWED_WITHIN_POINTS",
    "LUNAR_TAKEN_KIND",
    "LOG_INTERVAL_H_SHIP_OF_WAR",
    "LOG_INTERVAL_H_OTHER",
    "LOG_LINE_DOUBT",
    "LOG_LINE_SHORT_MAX",
    "LOG_LINE_SHORT_MIN",
    "LOG_READ_KN",
    "LOG_READ_SIGMA_KN",
    "OBSERVATION_KEPT_NM",
    "OBSERVATION_OUT_SIGMAS",
    "SAME_GROUND_NM",
    "SAME_LINE_DEG",
    "SET_DOUBT_EAST_KN",
    "SET_DOUBT_NORTH_KN",
    "SHORE_PASS_NM",
    "SOUNDING_ACROSS_MAX_NM",
    "SOUNDING_ACROSS_MIN_NM",
    "STEERING_SIGMA_POINTS_SEAWAY",
    "STEERING_SIGMA_POINTS_SMOOTH",
    "STREAM_DOUBT_FRACTION",
    "STREAM_DOUBT_HOURS",
    "TAKEN",
    "TIDE_QUARTER_S",
    "TRANSIT_SIGMA_NM",
    "TRACK_KEPT",
    "VARIATION_1805_DEG",
    "VARIATION_DRIFT_DEG_PER_YEAR",
    "Bearing",
    "CompassErrors",
    "Master",
    "Navigation",
    "Noon",
    "Observation",
    "Reckoning",
    "Sounding",
    "WEIGHED",
    "age_words",
    "chant",
    "doubt_miles_words",
    "doubt_words",
    "doubted_words",
    "fathoms_said",
    "ground_words",
    "knots_words",
    "miles_words",
    "trust_words",
    "verdict_words",
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
# Hove to, a ship with more way on than this by eye is sailing whatever her yards say
# (judgement: a ship hove to fore-reaches a knot or so).
HOVE_TO_WAY_KN = 2.0
# Hove to or lying a-try she drives to leeward, and the master reckons it and does not
# stop the clock (package 37e; until then the hours hove to were struck from the
# interval and neither the account nor its doubt moved through them). Falconer 1780,
# 'Drift': "the angle which the line of a ship's motion makes with the nearest meridian,
# when she drives with her side to the wind and waves, and is not governed by the power
# of the helm: it also implies the distance which the ship drives on that line." No
# period figure for its rate was found, and it is by his eye: her drift through the
# water as it is, to this grain (a quarter of a knot, as the log is read; JUDGEMENT),
# its line by his compass, and his doubt of it half a knot one sigma (JUDGEMENT: half of
# the knot he doubts her way by eye, `SPEED_BY_EYE_SIGMA_KN`).
HOVE_TO_DRIFT_KN = 0.25
HOVE_TO_DRIFT_SIGMA_KN = 0.5
# Under this much way she has none worth the log (the hull's own floor, `WAY_ON_KN`):
# becalmed, the master runs nothing for her and the tide and his doubt go on.
NO_WAY_KN = 0.5
# Her way between the heaves (package 37e). The log gives her way at the moment it is
# hove, and "if at any time of the watch the wind has increased or abated in the
# intervals, so as to affect the ship's velocity, the officer generally makes a suitable
# allowance for it" (Falconer 1780, 'Log'). Until package 37e one read stood for the
# whole interval, the last for the account between heaves and the new one for the
# interval it closed: a schooner that filled away after her noon cast was reckoned at the
# three knots she was read at lying to for two hours of seven, and then at seven and
# three quarters for the same two hours. The mate's eye, which judges her way to this
# grain (half a knot, JUDGEMENT; to the knot when it must stand alone), now says how her
# way over the interval stood to her way when the log was hove, and the read is allowed
# by that part, within these bounds (JUDGEMENT: beyond them he would heave the log).
WAY_BY_EYE_GRAIN_KN = 0.5
WAY_ALLOWANCE_LEAST = 0.25
WAY_ALLOWANCE_MOST = 2.0
# The master's tide is summed across an interval by the quarter hour, since the tide may
# turn within it (the brief of 37e).
TIDE_QUARTER_S = 900
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
# south-westerly gales", read in summary). Since package 34 the world's set is the tide's
# stream (`world/tide.py`, the water's velocity in the physics) and the scenario's stated
# current if it gives one; the master's doubt of it is his whatever the world does, and
# grows in a straight line: the streams run east and west along the Channel, so the doubt
# lies east and west above all, and a little north and south for Rennell's current. The
# sizes are judgement, tuned so that four days of thick weather leave the ellipse N §3
# describes (truth 58; TuningNotes, M5b), and are not re-tuned to the tide: the stream
# turns, so a day's net set is a mile or two, within the doubt (TuningNotes, package 34).
SET_DOUBT_EAST_KN = 0.2
SET_DOUBT_NORTH_KN = 0.03
# What the master takes off a cast for the tide before he lays it on the chart's
# low-water contours (package 34): the height of his own tide above the datum, by the
# spring rise of the nearest place in his epitome, or this where the table gives no rise
# (judgement: the Channel's mean level over the datum, about three metres, T §1). Since
# package 37j every place of both tables has a rise (`data/tides/establishments.yaml`),
# and this serves only a table without one.
TIDE_ALLOWANCE_DEFAULT_M = 3.0
# The master's rise at the quarters as a part of the spring rise (Norie 1805, the tide
# table's note: the neap rise "about two-thirds" of the spring's; judgement in the figure,
# the Epitome's text not read, the rule a commonplace of the period's tables), and the
# tide's own day, twelve hours and twenty-five minutes (Moore 1799, 'Of the Tides').
NEAP_RISE_OF_SPRING = 2.0 / 3.0
TIDE_HOURS = 12.0 + 25.0 / 60.0
SYNODIC_MONTH_DAYS = 29.53

# A departure: the reckoning begins where the land was last seen, a mile in doubt
# (judgement: a bearing of a headland and its distance by estimation). The account is
# laid at the scenario's own position (package 37j); the mile is the doubt only.
DEPARTURE_SIGMA_NM = 1.0

# ---------------------------------------------------------------------------
# The one rule by which an observation is believed (package 37e; the review of gate 5c's
# playtests, section 10: the owner's game 9; amended by package 37j)
# ---------------------------------------------------------------------------
# Until package 37e there were three rules. A line taken after a run of two miles
# replaced the account across it and before that was weighed (`FIX_RUN_NM`): so in game 9
# a lunar good to 25 miles replaced an account good to two, and a noon latitude that was
# right was weighed against a doubt of a quarter of a mile and moved the account 150
# yards, the lead cast every glass having kept the run at nothing. A bearing's distance
# was laid down when the account's doubt along the sight was the greater (37d's second
# pass). A fix set the account outright. Now there is one (`Reckoning.observe_line`,
# `observe_point`):
#   - an observation is WEIGHED against the account by their two doubts, whatever the run
#     since the last one;
#   - when the two disagree by more than their doubts together allow, one of them is
#     plainly out, and THE BETTER FIGURE IS BELIEVED (package 37j, the lead's decision on
#     the fold-in's finding): the observation is TAKEN, the account laid on it and the
#     account's doubt in that direction become the observation's own, only when its doubt
#     is no greater than the account's across its line; else it is WEIGHED, as any
#     observation is, and the line says the master doubts it ("the sight stands five
#     miles to the N of the account, and the account, good to three cables, is the
#     better figure");
#   - an account that the weighing moved less than half a cable was KEPT.
# Package 37e took the observation whenever the two disagreed so: so an octant's sight
# good to two miles and a half laid down an account fixed to three cables a minute before
# (the merchant passage's second noon, on Linux; on Windows the same sight fell a hair
# under the line and was weighed), and a lunar of poor certainty overrode the better
# account (the owner's note 5 on game 9). The disagreement there was the sight's.
# "Their doubts together" is the sum of what he would trust each within, and he trusts a
# figure within `OBSERVATION_OUT_SIGMAS` of its doubt: two, the figure the lunar's and the
# chronometer's words have used since package 33b (`sights.LUNAR_TRUST_SIGMAS`), so that
# "plainly out" is "further apart than he would trust the one and the other within".
# JUDGEMENT, kept by package 37j for that reason and no other. (37e chose two over its
# brief's three so that game 9's noon of 16 June, 2.06 of the two doubts together from an
# account the lead had kept falsely small, was taken; under the amended rule that noon is
# taken only because the account's doubt is honest, `Navigation._cast`: a cast no longer
# narrows it beyond what the lead can say. docs/dev/TuningNotes.md, packages 37e and 37j.)
OBSERVATION_OUT_SIGMAS = 2.0
# An account the weighing moved less than this was kept: half a cable (judgement: the
# least the log's words say, `geo.distance_words`).
OBSERVATION_KEPT_NM = 0.05
TAKEN, WEIGHED, KEPT = "taken", "weighed", "kept"
# The same thing seen again tells him nothing new: a second line of the same thing (a
# mark's bearing, a mark's distance by the eye, the lead's cast) lying within this many
# degrees of the one remembered for it is the same line, and carries the same error (the
# compass's, the eye's, the chart's). Five degrees, JUDGEMENT: a mark a mile off has
# swung so far when she has run a cable across the sight. The last so many things are
# remembered (judgement: more marks than are ever in a fix or a watch's bearings).
SAME_LINE_DEG = 5.0
LINES_REMEMBERED = 24

# The doubt of the stream (package 37e). Where the master's directions give a stream he
# works it into the traverse himself (`Navigation`, below), and what he cannot know of
# it grows his doubt along its set: the hour (Bowditch 1802: the rule of the moon's age
# "will sometimes differ an hour from the truth", and the nearest place in his table may
# be twenty leagues off, with another hour of its own), the rate (the book's round
# figure, and springs and neaps by the moon's age alone) and the set (to a point).
# Together `STREAM_DOUBT_FRACTION` of the rate at its strength, one sigma, growing in a
# straight line by the clock, under way or not: three quarters, JUDGEMENT, sized by
# measurement on the recorded passages (docs/dev/TuningNotes.md, package 37e: in the
# open Channel at the springs of June 1805 his hour is an hour to an hour and a half
# early and his set two points off, and what he allows is as far from the stream as
# allowing nothing). It grows no further than the stream can set her before it turns:
# the unknown part runs one way for half a tide and back the next, which is its rate
# for `STREAM_DOUBT_HOURS`, a quarter of the tide's twelve hours (JUDGEMENT: a half-
# cosine of rate R sets her R times 12 h 25 m / 2 pi, two hours' worth, in a quarter of
# the tide; three, since his hour is out and the turn he reckons from is not the true).
STREAM_DOUBT_FRACTION = 0.75
STREAM_DOUBT_HOURS = 3.0
# What the master knows he cannot know of his own instruments, in the doubt of the run
# (package 37e; until then both moved the account and not the ellipse, "the ellipse drawn
# too small", and on the recorded passages the true error stood beyond twice the stated
# doubt in four to six samples of ten). The log-line is marked short on purpose, so that
# "a ship will generally overrun her reckoning" (Luce 1866), by three to eight per cent
# (N §3); he does not correct for it, that being its purpose, and so doubts his run along
# the course by `LOG_LINE_DOUBT` of it, one sigma: four per cent, twice which is the eight
# the line may be out (JUDGEMENT on N §3's range). And his compass: the chart's old
# variation and the deviation carry every course he lays down to one side, and he doubts
# the run across the course by the same allowance he makes in a bearing
# (`COMPASS_ALLOWANCE_DEG`, less once he has observed the variation). Both grow in a
# straight line with the run and are resolved by an observation, as the leeway's doubt
# is; `Navigation` passes them, and the traverse's own arithmetic (`Reckoning.advance`
# with neither, truth 58) is as it was.
LOG_LINE_DOUBT = 0.04
# The master's sentence gives the doubt's lie when it is long and thin: the greater axis
# this many times the lesser, and a mile or more (the brief's figure).
DOUBT_THIN_RATIO = 2.0

# The compass's own error in a bearing (package 37e). Every bearing carries the chart's
# old variation and the ship's deviation on her heading (in game 9 two and a half
# degrees), and the lines of a fix share it, so a tight cocked hat can sit well off the
# ship: four cables at ten miles. The master does not know that error; he knows its
# likely size, and counts it in a bearing's doubt and a fix's: the decade's drift of his
# chart's variation "a quarter of a degree a year" (N §3; the study marks the figure
# UNVERIFIED), two degrees and a half, the deviation "a few degrees" being of the same
# size and not to be had at all (N §3). Once he has the variation by an amplitude or an
# azimuth ("an azimuth observation gets it to a degree", N §3) there is left the
# observation's degree and the deviation on other headings than the one he observed on:
# a degree and a half, JUDGEMENT.
COMPASS_ALLOWANCE_DEG = 2.5
COMPASS_ALLOWANCE_OBSERVED_DEG = 1.5
# A bearing worked as an angle at the account (package 37d) is sound only while the
# account's doubt across the sight is small beside the distance to the mark: in game 9,
# with twelve miles of doubt and a light eleven miles off, it left 2.6 miles of error
# across the sight. Above this part of the distance the line itself is laid down
# (JUDGEMENT, the brief's tenth).
BEARING_LINE_FORM_FRACTION = 0.1
# A shaped course's line is tried against the land as it is against the charted dangers
# (package 37e): said when it crosses the land, or passes the shore within half a mile
# (JUDGEMENT: half the berth a charted danger is given, `chart.DANGER_PASS_NM`, since the
# shore is seen and a rock is not). When the place itself is on the land the last two
# miles of the line are not tried: a course for a town ends at the town (JUDGEMENT).
SHORE_PASS_NM = 0.5
SHORE_AT_PLACE_NM = 2.0
# Each board laid down by itself (package 37j; the review of game 10: standing off and on
# the account was run on along the mean of her headings since the last working, and the
# boards, which ought nearly to cancel, did not: the error grew from a quarter of a mile
# to two miles in an hour and three quarters). At a tack, a wear, heaving to and filling
# away, and an alteration of course of `BOARD_ALTERATION_POINTS` or more from the mean
# heading pegged since the last working, the account is worked up to that minute from the
# log-board and the hourly working goes on from there (Falconer 1780, 'Traverse': "an
# assemblage of various courses ... The true course and distance resulting from this
# diversity of courses is discovered by collecting the difference of latitude and
# departure of each course", each course by itself and never their mean). Two points,
# JUDGEMENT (the brief's); a board shorter than `BOARD_LEAST_S` under way is not cut again
# (JUDGEMENT: a minute, so that a ship in stays, her head swinging through eight points,
# is one board's end and the next's beginning and not a dozen).
BOARD_ALTERATION_POINTS = 2.0
BOARD_LEAST_S = 60
# Becalmed so long, the log's last read is no longer her way when she gathers it again,
# and it is judged by eye until the log is next hove (JUDGEMENT: ten minutes; a ship in
# stays has no way for a minute and is not becalmed).
CALM_MINUTES = 10

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
# contour" (N §3). The contour the cast is matched to is the nearest point within the
# ellipse (at least this many miles about the reckoning) whose depth is within the
# tolerance of the cast and whose ground agrees; the tolerances are the lead's own error
# and the chart's (judgement). How wide the band is depends on the bottom (package 37e;
# until then it was three miles everywhere, and in game 9 eight casts on a flat sand
# narrowed the doubt while the error grew from one mile to five): the tolerance in
# fathoms over the fathoms the charted depth changes in a mile across the contour there
# (`Navigation._sounding_sigma_nm`). Over a flat bottom that is leagues, and the cast no
# line at all; over a steep one it is a good line, and no better than
# `SOUNDING_ACROSS_MIN_NM` (a quarter of a mile, JUDGEMENT: the chart's soundings are
# not laid down closer). The slope is read over `SOUNDING_SLOPE_NM` either way.
SOUNDING_ACROSS_MIN_NM = 0.25
SOUNDING_ACROSS_MAX_NM = 60.0
SOUNDING_SLOPE_NM = 0.5
# "A second cast on the same ground ... narrows nothing further" (the brief of 37e): the
# chart's error there and the master's own allowance for the tide are in every cast
# alike. The same ground is within this of where the first cast of it was laid, or
# within his own doubt when that is more (JUDGEMENT: two miles; nearer than that he
# cannot tell the two places apart by the lead). Such a cast still moves the account by
# the weighing (the depth changing under her says she is moving), and leaves its doubt
# as it was.
SAME_GROUND_NM = 2.0
# A cast that does not agree with the chart within his doubt widens it so that the nearest
# water of that depth lies just beyond the edge of what he would trust the account within,
# by this part of it (package 37j; judgement: the same cast again then stays apart and is
# not weighed in, which only the doubt's own growth by the hours, or another ground, can
# change).
APART_EDGE = 0.001
CONTOUR_SEARCH_MIN_NM = 5.0
CONTOUR_GRAIN_M = 0.5 * units.NAUTICAL_MILE  # the contour search's own step (`chart.py`)
# Within a doubt smaller than that grain the search is made finer, to a quarter of what he
# would trust the account within and no finer than a cable (package 37j; JUDGEMENT: the
# least the log's words say of a distance, `geo.distance_words`).
CONTOUR_FINEST_M = units.CABLE
CONTOUR_TOLERANCE_HAND_FATHOMS = 0.75
CONTOUR_TOLERANCE_DEEP_FATHOMS = 2.5

# A bearing of a landmark, "a degree or two by compass" (N §3): a degree and a half one
# sigma; a transit exact to a cable (spec §13: "a transit is exact"; judgement).
BEARING_SIGMA_DEG = 1.5
TRANSIT_SIGMA_NM = 0.1
# The distance off by estimation that goes with a bearing (spec §12's words, "twelve
# miles by estimation") is the lookout's own figure (package 33b: the eye's error drawn
# once a sighting, `lookout.DISTANCE_BY_ESTIMATION_FRACTION`; package 37d: judged afresh
# as the distance changes), the same in the list, the hail and the bearing's words.
# Package 33a laid it down with every bearing as a second measurement good to fifteen per
# cent (the review of gate 5c's playtests, 5.1): every single bearing was then a fix of a
# good line and a poor distance, bearings of different marks disagreed by their separate
# errors and the account jerked from one to the other, and a standing order taking a
# bearing every few minutes made the master ever surer of the wrong place. Package 37d
# lays it down ONLY WHEN IT IS THE BETTER FIGURE: when the account's own doubt along the
# line of sight is greater than the estimate's, as at a departure or a landfall on one
# mark after a long run, where a bearing and distance of a headland is the period's
# ordinary way and all the master has along the line; it is then weighed in by the gain
# and the line says so. Once laid down the account is the better figure along that
# sight, so the next bearing applies nothing until the doubt has grown again with the
# run. Otherwise the distance is said and not applied, and the words add the account's
# own distance from the mark when that differs from the estimate by more than
# `FIX_ACCOUNT_DIFFERS` of it (a third, judgement: twice the eye's own error), so that a
# disagreement is in the log for whoever reads it. The name is kept here for the tests.
DISTANCE_BY_ESTIMATION_FRACTION = _LOOKOUT_ESTIMATE_FRACTION
FIX_ACCOUNT_DIFFERS = 1.0 / 3.0

# The fix by cross bearings (package 37d; N §3's table: "two bearings a fix"; N §1: "a
# fix, a transit of two marks gives an exact line"). `take a fix` takes the bearings of
# two or three charted marks in sight at one stroke and sets the account at the point
# that best fits their lines, a new departure. Two lines that cut by less than
# `FIX_MIN_CUT_DEG` are no fix: thirty degrees, JUDGEMENT (the study gives the bearing's
# error and that two bearings fix, and no least angle of cut; thirty degrees is the
# figure the later seamanship manuals teach, at which a degree and a half of bearing
# is already three degrees' worth of doubt along the finer line, 1 / sin 30°). Unnamed,
# the master chooses among the nearest `FIX_MARKS_CONSIDERED` marks (judgement: off
# Falmouth fifty are in sight, and he takes the near ones). The line is notable when the
# account moved more than `FIX_NOTABLE_NM` (the brief's mile).
FIX_MIN_CUT_DEG = 30.0
FIX_MARKS_CONSIDERED = 12
FIX_MARKS_IN_ALL = 36  # when the near marks all lie one way (a coast seen end on), any of these
FIX_NOTABLE_NM = 1.0

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


def fathoms_said(depth_m: float) -> str:
    """A depth in the master's words to the half fathom: 'two fathoms and a half', 'fifty
    fathoms', 'half a fathom' (package 37j: the tide he allows off a cast)."""
    halves = max(0, round(units.m_to_fathoms(depth_m) * 2.0))
    whole, half = divmod(halves, 2)
    if whole == 0:
        return "half a fathom" if half else "no water"
    words = f"{number_words(whole)} fathom{'s' if whole != 1 else ''}"
    return f"{words} and a half" if half else words


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


@dataclass(frozen=True)
class Observation:
    """What the master did with one observation (package 37e, the one rule): `how` is
    'taken' (the account was plainly out and is laid on the observation), 'weighed' (the
    two were weighed by their doubts and the account moved) or 'kept' (weighed, and the
    account stayed within half a cable of where it was); how far and which way the
    account moved; how far the observation stood from the account, and the two doubts
    it was judged by; and whether it was the same thing seen again from the same place,
    which tells him nothing new."""

    how: str
    moved_nm: float = 0.0
    toward_deg: float = 0.0
    off_nm: float = 0.0
    account_sigma_nm: float = 0.0
    sigma_nm: float = 0.0
    repeat: bool = False
    # package 37j: the two stood further apart than their doubts together and the
    # observation was the poorer figure, so it was weighed and not taken, and the master
    # doubts it; and which way the observation stood from the account
    doubted: bool = False
    off_toward_deg: float = 0.0

    @property
    def moved(self) -> bool:
        return self.how != KEPT

    @property
    def poorer(self) -> bool:
        """Whether the observation was the poorer figure of the two."""
        return self.sigma_nm > self.account_sigma_nm

    def to_dict(self) -> dict[str, Any]:
        return {
            "how": self.how,
            "moved_nm": round(self.moved_nm, 2),
            "moved_toward": units.point_name(math.radians(self.toward_deg)),
            "off_nm": round(self.off_nm, 2),
            "account_sigma_nm": round(self.account_sigma_nm, 2),
            "sigma_nm": round(self.sigma_nm, 2),
            "repeat": self.repeat,
            "doubted": self.doubted,
        }


def _worst(a: Observation, b: Observation | None) -> str:
    """The word for two workings of one observation (a bearing's line and its distance):
    taken if either was, else weighed if either moved the account, else kept."""
    hows = {a.how} | ({b.how} if b is not None else set())
    for how in (TAKEN, WEIGHED):
        if how in hows:
            return how
    return KEPT


class Reckoning:
    """The reckoned position with its covariance (square miles, east and north), the
    bias accumulators, and the records the chart draws. Pure arithmetic: nothing here
    reads the world; `Navigation` feeds it."""

    # Fields added since a checkpoint may have been written carry a plain class default
    # (package 37d's rule): the stream's doubt and the water it was grown in, and the
    # lines already had (package 37e).
    stream_doubt: list[float] | None = None
    stream_water: str | None = None
    run_doubt: list[float] | None = None
    course_doubt: list[float] | None = None
    _seen: dict[str, tuple[float, float]] | None = None
    # package 37j: the read's doubt along the boards since the log was hove, and the drift's
    read_doubt: list[float] | None = None
    drift_doubt: list[float] | None = None

    def __init__(self, start: Position, tick: int = 0, sigma_nm: float = DEPARTURE_SIGMA_NM):
        self.lat_deg = start.lat_deg
        self.lon_deg = start.lon_deg
        self.P: list[list[float]] = [[sigma_nm * sigma_nm, 0.0], [0.0, sigma_nm * sigma_nm]]
        # the biases: the set doubt east and north (independent, as standard deviations
        # that grow with the hours), the leeway doubt as a vector across the course, and
        # the doubt of the stream the master allows, a vector along its set
        self.set_doubt = [0.0, 0.0]
        self.leeway_doubt = [0.0, 0.0]
        self.stream_doubt = [0.0, 0.0]
        self.stream_water = None
        # and the doubt of the log-line, a vector along the courses run, and of the
        # compass, across them
        self.run_doubt = [0.0, 0.0]
        self.course_doubt = [0.0, 0.0]
        self.read_doubt = [0.0, 0.0]
        self.drift_doubt = [0.0, 0.0]
        # the lines already had, by the thing observed: the same thing seen again from
        # the same place tells him nothing new
        self._seen = {}
        # the run since the last observation: a record only since package 37e (the one
        # rule does not read it; the review's probe does)
        self.run_since_fix_nm = 0.0
        # the captain's own set, which replaces the master's tide while it stands
        # (knots, toward radians; no knots at all is his word that there is none); None:
        # the tide is the master's, by the book
        self.set_allowance: tuple[float, float] | None = None
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

    def _stream_doubt(self) -> list[float]:
        if self.stream_doubt is None:  # a checkpoint from before package 37e
            self.stream_doubt = [0.0, 0.0]
        return self.stream_doubt

    def _biases(self) -> list[list[float]]:
        """The bias vectors whose outer products are in the covariance: the leeway's,
        the stream's, the log-line's, the compass's and the log's read since it was last
        hove (package 37j)."""
        if self.run_doubt is None:  # a checkpoint from before package 37e
            self.run_doubt = [0.0, 0.0]
        if self.course_doubt is None:
            self.course_doubt = [0.0, 0.0]
        if self.read_doubt is None:  # a checkpoint from before package 37j
            self.read_doubt = [0.0, 0.0]
        return [
            self.leeway_doubt,
            self._stream_doubt(),
            self.run_doubt,
            self.course_doubt,
            self.read_doubt,
        ]

    def _drift_doubt(self) -> list[float]:
        if self.drift_doubt is None:  # a checkpoint from before package 37j
            self.drift_doubt = [0.0, 0.0]
        return self.drift_doubt

    def new_read(self) -> None:
        """The log hove again (package 37j): the last read's error is in the doubt as it
        stands, and the new read's begins from nothing."""
        self._biases()
        self.read_doubt = [0.0, 0.0]

    def lay_by_drift(self) -> None:
        """She has filled away (package 37j): the drift's error is in the doubt as it
        stands, and the next time she lies to his eye judges it afresh."""
        self.drift_doubt = [0.0, 0.0]

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
        *,
        clock_hours: float | None = None,
        also: tuple[float, float] | None = None,
        also_sigma_nm: float = 0.0,
        stream: tuple[str, float, float, float] | None = None,
        run_doubt: float = 0.0,
        course_doubt_rad: float = 0.0,
        held: bool = False,
    ) -> tuple[float, float]:
        """The traverse for one interval: the run `speed_kn` for `hours` along the course
        the master lays down (`course_rad`, already corrected as he corrects it), with
        the helmsman's error drawn for the interval; the doubt grown by the random terms
        (the read, `read_sigma_kn` an hour, and the steering) and the biases (the set,
        the leeway when close-hauled). Returns the miles east and north made by account.
        No hours at all (the whole interval hove to) still steps the board.

        Package 37e. `hours` are the hours she had way on; `clock_hours` (the same
        unless said) are the hours by the clock, under way, hove to or becalmed, which
        the doubt of the set grows by: she drifts whether she has way or not, and he
        doubts. `also` is what the master adds to the traverse besides the run, miles
        east and north: his tide as one more course and distance (Bowditch 1802,
        'Currents') and her drift hove to; `also_sigma_nm` his doubt of the drift.
        `stream` is the stream his directions give for the water (its name, its rate at
        strength in knots, its set in radians, the hours of it), for the part of it he
        cannot know. `run_doubt` is the part of the run he doubts along the course for
        his log-line's marking, and `course_doubt_rad` the angle he doubts the course by
        for his compass's own error. With none of these it is the traverse of package
        33a, and the captain's own set, if he has ordered one, is applied here for the
        clock's hours.

        `held` (package 37j; `Navigation` passes it): the log's read and her drift by eye
        are each one figure for the whole time it serves (the read until the log is next
        hove, the drift while she lies to), so their doubts are kept as biases that grow in
        a straight line across the boards (`read_doubt`, `drift_doubt`): an interval cut
        at every board (item 4 of the package) must not shrink them, as the sum of their
        squares by the interval would."""
        if hours < 0.0:
            return 0.0, 0.0
        clock = hours if clock_hours is None else max(hours, clock_hours)
        run = max(0.0, speed_kn) * hours
        course = course_rad + steer_error_rad
        de, dn = run * math.sin(course), run * math.cos(course)
        if also is not None:
            de += also[0]
            dn += also[1]
        elif self.set_allowance is not None:
            kn, toward = self.set_allowance
            de += kn * clock * math.sin(toward)
            dn += kn * clock * math.cos(toward)
        self._move(de, dn)
        self.run_since_noon_nm += math.hypot(de, dn) if also is not None else run
        self.run_since_fix_nm += run
        # the random terms, along and across the course
        steer_sigma = units.points_to_rad(
            STEERING_SIGMA_POINTS_SEAWAY if heavy_sea else STEERING_SIGMA_POINTS_SMOOTH
        )
        s_along = 0.0 if held else read_sigma_kn * hours
        s_across = run * steer_sigma
        c, s = math.cos(course), math.sin(course)
        # R diag(s_along², s_across²) Rᵀ with R the course's rotation (east, north)
        q_ee = s_along**2 * s * s + s_across**2 * c * c
        q_nn = s_along**2 * c * c + s_across**2 * s * s
        q_en = (s_along**2 - s_across**2) * s * c
        drift_var = 0.0 if held else also_sigma_nm**2
        self.P[0][0] += q_ee + drift_var
        self.P[1][1] += q_nn + drift_var
        self.P[0][1] += q_en
        self.P[1][0] += q_en
        if held:
            # the read's error along every board run on it, and the drift's either way
            self._biases()
            read = self.read_doubt
            assert read is not None
            old_r = list(read)
            read[0] += read_sigma_kn * hours * s
            read[1] += read_sigma_kn * hours * c
            self._add_outer(read, +1.0)
            self._add_outer(old_r, -1.0)
            drift = self._drift_doubt()
            for i in (0, 1):
                old = drift[i]
                drift[i] = old + also_sigma_nm
                self.P[i][i] += drift[i] * drift[i] - old * old
        # the biases grow in a straight line: the set doubt east and north, by the
        # clock's hours
        for i, kn in ((0, SET_DOUBT_EAST_KN), (1, SET_DOUBT_NORTH_KN)):
            old = self.set_doubt[i]
            new = old + kn * clock
            self.set_doubt[i] = new
            self.P[i][i] += new * new - old * old
        # and the leeway doubt across the course while close-hauled
        if close_hauled and leeway_doubt_rad > 0.0:
            old_l = list(self.leeway_doubt)
            self.leeway_doubt[0] += run * leeway_doubt_rad * c  # across: (cos, -sin)
            self.leeway_doubt[1] -= run * leeway_doubt_rad * s
            self._add_outer(self.leeway_doubt, +1.0)
            self._add_outer(old_l, -1.0)
        # the log-line's marking along the course and the compass's own error across it,
        # each a bias of the same sense on every course she runs
        if run_doubt > 0.0 or course_doubt_rad > 0.0:
            self._biases()
            assert self.run_doubt is not None and self.course_doubt is not None
            for vec, e, n in (
                (self.run_doubt, run * run_doubt * s, run * run_doubt * c),
                (self.course_doubt, run * course_doubt_rad * c, -run * course_doubt_rad * s),
            ):
                if e or n:
                    old_v = list(vec)
                    vec[0] += e
                    vec[1] += n
                    self._add_outer(vec, +1.0)
                    self._add_outer(old_v, -1.0)
        # and the part of the stream he cannot know, along its set: its hour and its
        # rate, growing in a straight line and no further than the stream can set her
        # before it turns (`STREAM_DOUBT_HOURS`); what was grown in other water stays
        if stream is not None:
            water, rate_kn, set_rad, stream_hours = stream
            doubt = self._stream_doubt()
            if water != self.stream_water:
                self.stream_water = water
                doubt[0] = doubt[1] = 0.0
            if rate_kn > 0.0 and stream_hours > 0.0:
                old_s = list(doubt)
                grow = STREAM_DOUBT_FRACTION * rate_kn * stream_hours
                e, n = doubt[0] + grow * math.sin(set_rad), doubt[1] + grow * math.cos(set_rad)
                size = math.hypot(e, n)
                limit = max(
                    STREAM_DOUBT_FRACTION * rate_kn * STREAM_DOUBT_HOURS, math.hypot(*old_s)
                )
                if size > limit > 0.0:
                    e, n = e * limit / size, n * limit / size
                doubt[0], doubt[1] = e, n
                self._add_outer(doubt, +1.0)
                self._add_outer(old_s, -1.0)
        self._clean()
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

    def _clean(self) -> None:
        """Keep the covariance a covariance: the bias vectors are taken out and put back
        as outer products, and after an observation has narrowed the doubt the two need
        not agree to the last figure."""
        p = self.P
        p[0][0] = max(p[0][0], 0.0)
        p[1][1] = max(p[1][1], 0.0)
        bound = math.sqrt(p[0][0] * p[1][1])
        cross = max(-bound, min(bound, 0.5 * (p[0][1] + p[1][0])))
        p[0][1] = p[1][0] = cross

    # -- the observations: one rule (package 37e) ---------------------------------------

    def _again(self, thing: str | None, n_e: float, n_n: float, however: bool = False) -> bool:
        """Whether this line is the same thing seen again from the same place: the same
        thing (a mark's bearing, a mark's distance, the lead's cast) whose line lies
        within `SAME_LINE_DEG` of the one remembered for it. A line that has swung by
        more is a new line, and is remembered in its place; `however` the line lies when
        the thing's error is the same wherever it is seen from (the eye's judging of one
        mark's distance)."""
        if thing is None:
            return False
        if self._seen is None:  # a checkpoint from before package 37e
            self._seen = {}
        found = self._seen.get(thing)
        if found is not None:
            if however:
                return True
            if abs(found[0] * n_e + found[1] * n_n) >= math.cos(math.radians(SAME_LINE_DEG)):
                return True
            del self._seen[thing]
        self._seen[thing] = (n_e, n_n)
        while len(self._seen) > LINES_REMEMBERED:
            del self._seen[next(iter(self._seen))]
        return False

    def _resolve(self, n_e: float, n_n: float, gain: float) -> None:
        """The biases resolved across a line by the part of the doubt the observation
        took: all of it for one taken, the gain for one weighed."""
        for vec in self._biases():
            along = n_e * vec[0] + n_n * vec[1]
            vec[0] -= gain * along * n_e
            vec[1] -= gain * along * n_n
        self.set_doubt[0] *= 1.0 - gain * abs(n_e)
        self.set_doubt[1] *= 1.0 - gain * abs(n_n)
        drift = self._drift_doubt()
        drift[0] *= 1.0 - gain * abs(n_e)
        drift[1] *= 1.0 - gain * abs(n_n)

    def _across(self, n_e: float, n_n: float) -> float:
        """The account's variance across a line whose unit normal is (n_e, n_n)."""
        p = self.P
        return max(
            0.0, n_e * (p[0][0] * n_e + p[0][1] * n_n) + n_n * (p[1][0] * n_e + p[1][1] * n_n)
        )

    def _floor(self, n_e: float, n_n: float, variance: float) -> None:
        """The doubt across a line kept no smaller than `variance`."""
        short = variance - self._across(n_e, n_n)
        if short > 0.0:
            self.P[0][0] += short * n_e * n_e
            self.P[1][1] += short * n_n * n_n
            self.P[0][1] += short * n_e * n_n
            self.P[1][0] += short * n_e * n_n

    def observe_line(
        self,
        de: float,
        dn: float,
        n_e: float,
        n_n: float,
        sigma_nm: float,
        thing: str | None = None,
        shared_sigma_nm: float | None = None,
        take: bool = True,
        however: bool = False,
        narrow: bool = True,
    ) -> Observation:
        """A line measurement, by the one rule for every observation (package 37e): the
        ship lies on the line through the point `de, dn` miles east and north of the
        reckoning whose unit normal is (`n_e`, `n_n`), within `sigma_nm` across it.

        - **Weighed.** The observation is weighed against the account by their two
          doubts, whatever the run since the last one (the Kalman update): the account
          moves toward the line by the part its own doubt is of the two, and its doubt
          across the line narrows; along the line nothing changes.
        - **Taken.** When the two disagree by more than their doubts together allow
          (`OBSERVATION_OUT_SIGMAS` of each, added), one of them is plainly out, and the
          better figure is believed (package 37j): when the observation's doubt is no
          greater than the account's across the line, the account is out, and it is
          laid on the line and its doubt across the line becomes the observation's own.
          This is Falconer 1780, 'Dead-reckoning' (the reckoning "is always to be
          corrected, as often as any good observation ... can be obtained"), kept for
          the case it was written for: a *good* observation.
        - **Doubted.** When they so disagree and the observation is the poorer figure,
          it is weighed as above, and the master doubts it (`Observation.doubted`, and
          the line says so, `verdict_words`): a sight of two miles and a half against an
          account fixed to three cables moves it a cable, and does not lay it down five
          miles off (package 37e did; the merchant passage's second noon).
        - **The same thing seen again tells him nothing new.** `thing` names what was
          observed (a mark's bearing, a mark's distance by the eye, the lead's cast); a
          second line of the same thing lying within `SAME_LINE_DEG` of the first
          carries the same error in the part `shared_sigma_nm` (all of it unless said:
          the compass's error in a bearing, the eye's in a distance, the chart's in a
          sounding), so it cannot bring the doubt across the line below that part, and
          where the account's doubt is no greater than it already, it is not applied.
          (`however` the line lies: the eye's judging of one mark's distance is the same
          error wherever she sees the mark from.)

        `take` False is for what is no observation in Falconer's sense and may only be
        weighed: the lookout's distance by estimation, the eye's guess, which package
        37d's second pass (approved by the owner) laid down "never in the replace form".
        `narrow` False is for a second cast of the lead on the same ground: weighed, it
        moves the account, and the doubt is left as it was.

        Returns what was done (`Observation`)."""
        p = self.P
        z = n_e * de + n_n * dn  # how far the line is, across it
        r = sigma_nm * sigma_nm
        prior = self._across(n_e, n_n)
        account_sigma = math.sqrt(prior)
        again = self._again(thing, n_e, n_n, however)
        shared = r if shared_sigma_nm is None else min(r, shared_sigma_nm * shared_sigma_nm)
        off_toward = math.degrees(math.atan2(n_e * z, n_n * z)) % 360.0
        if again and prior <= shared * (1.0 + 1e-9):
            return Observation(
                KEPT, 0.0, 0.0, abs(z), account_sigma, sigma_nm, True, off_toward_deg=off_toward
            )
        # package 37j: plainly out, the better figure is believed
        out = abs(z) > OBSERVATION_OUT_SIGMAS * (account_sigma + sigma_nm)
        better = sigma_nm <= account_sigma
        doubted = out and not better
        if take and out and better:
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
            self._resolve(n_e, n_n, 1.0)
            moved_e, moved_n = n_e * z, n_n * z
            how = TAKEN
        else:
            pn_e = p[0][0] * n_e + p[0][1] * n_n  # P n
            pn_n = p[1][0] * n_e + p[1][1] * n_n
            s = prior + r  # n P n + R
            if s <= 0.0:
                return Observation(
                    KEPT, 0.0, 0.0, abs(z), account_sigma, sigma_nm, again, doubted, off_toward
                )
            k_e, k_n = pn_e / s, pn_n / s  # the gain
            moved_e, moved_n = k_e * z, k_n * z
            self._move(moved_e, moved_n)
            if narrow:
                self.P = [  # (I - K nᵀ) P
                    [p[0][0] - k_e * pn_e, p[0][1] - k_e * pn_n],
                    [p[1][0] - k_n * pn_e, p[1][1] - k_n * pn_n],
                ]
                self._resolve(n_e, n_n, prior / s)
                if again:
                    self._floor(n_e, n_n, shared)
            how = WEIGHED if math.hypot(moved_e, moved_n) >= OBSERVATION_KEPT_NM else KEPT
        self._clean()
        self.run_since_fix_nm = 0.0
        return Observation(
            how,
            math.hypot(moved_e, moved_n),
            math.degrees(math.atan2(moved_e, moved_n)) % 360.0,
            abs(z),
            account_sigma,
            sigma_nm,
            again,
            doubted and how != TAKEN,
            off_toward,
        )

    def observe_point(
        self,
        de: float,
        dn: float,
        cov: list[list[float]],
        lines: list[tuple[str, float, float, float]] | None = None,
        common: tuple[float, float] | None = None,
    ) -> Observation:
        """A point measurement by the same rule: a fix `de, dn` miles east and north of
        the reckoning whose own doubt is `cov` (square miles, east and north). Taken
        when the two are farther apart than their doubts together allow, measured along
        the line between them, and the fix is the better figure there (package 37j):
        the account is laid on the fix and its doubt becomes the fix's own, a new
        departure. Weighed otherwise, so that a good fix still rules a doubtful account
        and a poor one cannot move a good account; when they so disagree and the fix is
        the poorer, it is doubted. `lines` are the fix's lines of bearing (the thing,
        the unit normal and the part of the line's doubt that is the same each time, as
        a variance): a fix by the same marks from the same place cannot narrow the doubt
        across a line below that part, and where every line is one already had and the
        account's doubt across each is no greater, it is not applied. `common` is how far
        the compass's own error (one sigma of what he allows for it) moves this fix,
        miles east and north (package 37j): the same in every fix by marks on that hand
        with that compass, so the account's doubt that way is never narrowed below it."""
        lines = lines or []
        again = [self._again(thing, n_e, n_n) for thing, n_e, n_n, _ in lines]
        apart = math.hypot(de, dn)
        if apart > 0.0:
            u_e, u_n = de / apart, dn / apart
        else:
            u_e, u_n = 1.0, 0.0
        off_toward = math.degrees(math.atan2(u_e, u_n)) % 360.0 if apart > 0.0 else 0.0
        account_sigma = math.sqrt(self._across(u_e, u_n))
        fix_sigma = math.sqrt(
            max(
                0.0,
                u_e * (cov[0][0] * u_e + cov[0][1] * u_n)
                + u_n * (cov[1][0] * u_e + cov[1][1] * u_n),
            )
        )
        if (
            lines
            and all(again)
            and all(
                self._across(n_e, n_n) <= shared * (1.0 + 1e-9) for _, n_e, n_n, shared in lines
            )
        ):
            return Observation(
                KEPT, 0.0, 0.0, apart, account_sigma, fix_sigma, True, off_toward_deg=off_toward
            )
        p = self.P
        common_prior = 0.0
        if common is not None and math.hypot(*common) > 0.0:
            size = math.hypot(*common)
            common_prior = self._across(common[0] / size, common[1] / size)
        out = apart > OBSERVATION_OUT_SIGMAS * (account_sigma + fix_sigma)
        better = fix_sigma <= account_sigma
        doubted = out and not better
        if out and better:
            self._move(de, dn)
            self.P = [[cov[0][0], cov[0][1]], [cov[1][0], cov[1][1]]]
            self.set_doubt = [0.0, 0.0]
            self.leeway_doubt = [0.0, 0.0]
            self.stream_doubt = [0.0, 0.0]
            self.run_doubt = [0.0, 0.0]
            self.course_doubt = [0.0, 0.0]
            self.read_doubt = [0.0, 0.0]
            self.drift_doubt = [0.0, 0.0]
            moved_e, moved_n = de, dn
            how = TAKEN
        else:
            s00, s01, s11 = p[0][0] + cov[0][0], p[0][1] + cov[0][1], p[1][1] + cov[1][1]
            det = s00 * s11 - s01 * s01
            if det <= 0.0:
                return Observation(
                    KEPT,
                    0.0,
                    0.0,
                    apart,
                    account_sigma,
                    fix_sigma,
                    all(again),
                    doubted,
                    off_toward,
                )
            i00, i01, i11 = s11 / det, -s01 / det, s00 / det  # S⁻¹
            k = [  # K = P S⁻¹
                [p[0][0] * i00 + p[0][1] * i01, p[0][0] * i01 + p[0][1] * i11],
                [p[1][0] * i00 + p[1][1] * i01, p[1][0] * i01 + p[1][1] * i11],
            ]
            moved_e = k[0][0] * de + k[0][1] * dn
            moved_n = k[1][0] * de + k[1][1] * dn
            self._move(moved_e, moved_n)
            self.P = [  # (I - K) P
                [
                    p[0][0] - k[0][0] * p[0][0] - k[0][1] * p[1][0],
                    p[0][1] - k[0][0] * p[0][1] - k[0][1] * p[1][1],
                ],
                [
                    p[1][0] - k[1][0] * p[0][0] - k[1][1] * p[1][0],
                    p[1][1] - k[1][0] * p[0][1] - k[1][1] * p[1][1],
                ],
            ]
            for vec in self._biases():
                e, n = vec
                vec[0] = e - k[0][0] * e - k[0][1] * n
                vec[1] = n - k[1][0] * e - k[1][1] * n
            self.set_doubt[0] *= max(0.0, 1.0 - k[0][0])
            self.set_doubt[1] *= max(0.0, 1.0 - k[1][1])
            drift = self._drift_doubt()
            drift[0] *= max(0.0, 1.0 - k[0][0])
            drift[1] *= max(0.0, 1.0 - k[1][1])
            self._clean()
            for (_thing, n_e, n_n, shared), seen in zip(lines, again, strict=True):
                if seen:
                    self._floor(n_e, n_n, shared)
            how = WEIGHED if math.hypot(moved_e, moved_n) >= OBSERVATION_KEPT_NM else KEPT
        # the compass's own error moves every fix by marks on one hand alike: a fix does
        # not make the account surer that way than the compass allows (package 37j), nor
        # less sure than it was
        if common is not None and how != TAKEN:
            size = math.hypot(*common)
            if size > 0.0:
                self._floor(common[0] / size, common[1] / size, min(size * size, common_prior))
        self._clean()
        self.run_since_fix_nm = 0.0
        return Observation(
            how,
            math.hypot(moved_e, moved_n),
            math.degrees(math.atan2(moved_e, moved_n)) % 360.0,
            apart,
            account_sigma,
            fix_sigma,
            bool(lines) and all(again),
            doubted and how != TAKEN,
            off_toward,
        )

    def within_doubt(self, sigmas: float) -> tuple[Any, float]:
        """What the master would trust the account within (package 37j): a test of a
        point, true when it lies within `sigmas` of the doubt as the ellipse lies (the
        Mahalanobis distance), and the reach of that region in miles (its greater
        semi-axis)."""
        p = self.P
        det = p[0][0] * p[1][1] - p[0][1] * p[1][0]
        reach = sigmas * self.ellipse()["semi_major_nm"]
        lat, lon = self.lat_deg, self.lon_deg
        if det <= 1e-12:

            def holds(point: Position) -> bool:
                de, dn = _offset_from(lat, lon, point)
                return math.hypot(de, dn) <= reach + 1e-9

            return holds, reach
        i00, i01, i11 = p[1][1] / det, -p[0][1] / det, p[0][0] / det
        limit = sigmas * sigmas * (1.0 + 1e-9)

        def holds(point: Position) -> bool:
            de, dn = _offset_from(lat, lon, point)
            return de * (i00 * de + i01 * dn) + dn * (i01 * de + i11 * dn) <= limit

        return holds, reach

    def widen_toward(self, de: float, dn: float, sigmas: float) -> float:
        """The doubt grown toward a point `de, dn` miles east and north so that the point
        lies `sigmas` of the doubt off (package 37j, a cast that does not agree within his
        doubt: the nearest water that answers it lies then at the edge of what he would
        trust the account within). The account does not move. Returns how far the doubt
        grew along that way, miles one sigma (nought when the point lay within already)."""
        d2 = de * de + dn * dn
        if d2 <= 0.0:
            return 0.0
        d = math.sqrt(d2)
        u_e, u_n = de / d, dn / d
        p = self.P
        det = p[0][0] * p[1][1] - p[0][1] * p[1][0]
        before = math.sqrt(self._across(u_e, u_n))
        if det <= 1e-12:
            a = 1.0 / max(self._across(u_e, u_n), 1e-12)
        else:
            a = (
                u_e * (p[1][1] * u_e - p[0][1] * u_n) + u_n * (-p[1][0] * u_e + p[0][0] * u_n)
            ) / det
        # with P' = P + k u uT, uT P'^-1 u = a / (1 + k a) (Sherman and Morrison), and the
        # point d u lies `sigmas` off when that is sigmas squared over d squared
        k = d2 / (sigmas * sigmas) - 1.0 / a
        if k <= 0.0:
            return 0.0
        p[0][0] += k * u_e * u_e
        p[1][1] += k * u_n * u_n
        p[0][1] += k * u_e * u_n
        p[1][0] += k * u_e * u_n
        self._clean()
        return math.sqrt(self._across(u_e, u_n)) - before

    def update_line(self, de: float, dn: float, n_e: float, n_n: float, sigma_nm: float) -> float:
        """`observe_line` for a caller that wants only the miles moved."""
        return self.observe_line(de, dn, n_e, n_n, sigma_nm).moved_nm

    def observe_latitude(self, lat_deg: float, sigma_nm: float) -> Observation:
        """The noon latitude: a line east and west through the observed latitude."""
        dn = (lat_deg - self.lat_deg) * _NM_PER_DEG
        return self.observe_line(0.0, dn, 0.0, 1.0, sigma_nm)

    def observe_longitude(self, lon_deg: float, sigma_nm: float) -> Observation:
        """A longitude by chronometer or by lunar (package 33b, spec §13): a line north
        and south through the observed longitude, weighed east and west by the
        observation's own doubt; north and south is left as it was."""
        de = (lon_deg - self.lon_deg) * _NM_PER_DEG * math.cos(math.radians(self.lat_deg))
        return self.observe_line(de, 0.0, 1.0, 0.0, sigma_nm)

    def observe_bearing(
        self,
        mark: Position,
        bearing_rad: float,
        sigma_nm: float,
        thing: str | None = None,
        shared_sigma_nm: float | None = None,
    ) -> Observation:
        """A bearing of a mark in the line's form: the line from the mark along the
        reciprocal of the bearing laid down; its normal is across the bearing."""
        de, dn = self.offset_nm(mark)
        n_e, n_n = math.cos(bearing_rad), -math.sin(bearing_rad)
        return self.observe_line(de, dn, n_e, n_n, sigma_nm, thing, shared_sigma_nm)

    def observe_distance(
        self,
        mark: Position,
        bearing_rad: float,
        distance_nm: float,
        sigma_nm: float,
        thing: str | None = None,
    ) -> Observation:
        """The distance off a mark by estimation, along the bearing: the line across the
        bearing at that distance from the mark, its normal along the bearing. The eye's
        guess: weighed against the account by their two doubts and never taken, and the
        same thing seen again however the mark bears."""
        de, dn = self.offset_nm(mark)
        n_e, n_n = math.sin(bearing_rad), math.cos(bearing_rad)
        return self.observe_line(
            de - distance_nm * n_e,
            dn - distance_nm * n_n,
            n_e,
            n_n,
            sigma_nm,
            thing,
            take=False,
            however=True,
        )

    def update_latitude(self, lat_deg: float, sigma_nm: float) -> float:
        return self.observe_latitude(lat_deg, sigma_nm).moved_nm

    def update_longitude(self, lon_deg: float, sigma_nm: float) -> float:
        return self.observe_longitude(lon_deg, sigma_nm).moved_nm

    def update_bearing(self, mark: Position, bearing_rad: float, sigma_nm: float) -> float:
        return self.observe_bearing(mark, bearing_rad, sigma_nm).moved_nm

    def update_distance(
        self, mark: Position, bearing_rad: float, distance_nm: float, sigma_nm: float
    ) -> float:
        return self.observe_distance(mark, bearing_rad, distance_nm, sigma_nm).moved_nm

    def set_position(self, pos: Position, tick: int, sigma_nm: float = DEPARTURE_SIGMA_NM) -> None:
        """The captain's override, or a departure: the account set to a point with a
        fresh doubt, the biases and the lines already had forgotten."""
        self.lat_deg, self.lon_deg = pos.lat_deg, pos.lon_deg
        self.P = [[sigma_nm * sigma_nm, 0.0], [0.0, sigma_nm * sigma_nm]]
        self.set_doubt = [0.0, 0.0]
        self.leeway_doubt = [0.0, 0.0]
        self.stream_doubt = [0.0, 0.0]
        self.run_doubt = [0.0, 0.0]
        self.course_doubt = [0.0, 0.0]
        self.read_doubt = [0.0, 0.0]
        self.drift_doubt = [0.0, 0.0]
        self._seen = {}
        self.run_since_fix_nm = 0.0
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
        return _ellipse_of(self.P)

    @property
    def words(self) -> str:
        """'49° 52' N, 6° 10' W by account'."""
        return f"{format_position(self.position)} by account"

    @property
    def uncertainty_words(self) -> str:
        """The master's sentence (`doubt_words`): "I would not trust the reckoning within
        twenty miles east or west, nor five north or south."."""
        return doubt_words(self.P)

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


def _ellipse_of(p: list[list[float]]) -> dict[str, float]:
    """The one-sigma ellipse of a covariance (square miles, east and north)."""
    a, b, c = p[0][0], p[0][1], p[1][1]
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
        "sigma_east_nm": round(math.sqrt(max(0.0, a)), 2),
        "sigma_north_nm": round(math.sqrt(max(0.0, c)), 2),
    }


def doubt_miles_words(nm: float) -> str:
    """A doubt in the master's words: in cables under a mile ('four cables', and never
    less than a cable), to the mile under ten, to five miles above (a master says
    'twenty miles', not 'nineteen')."""
    if nm < 0.95:
        cables = max(1, round(nm * 10.0))
        if cables < 10:
            return "a cable" if cables == 1 else f"{number_words(cables)} cables"
        return "a mile"
    miles = _round_miles(nm)
    return "a mile" if miles == 1 else f"{number_words(miles)} miles"


def doubt_words(p: list[list[float]]) -> str:
    """The master's sentence for a doubt (package 37e): "I would not trust the reckoning
    within twenty miles east or west, nor five north or south"; under a mile in cables
    ("within four cables east or west, nor two north or south"), never "a mile" for a
    cable; and when the doubt is long and thin (the greater axis twice the lesser, and
    a mile or more) and lies neither east and west nor north and south, with its lie:
    "I would not trust the reckoning within three miles NE and SW, nor a mile across."."""
    e = _ellipse_of(p)
    major = math.sqrt(max(0.0, 0.5 * (p[0][0] + p[1][1]) + _root_of(p)))
    minor = math.sqrt(max(0.0, 0.5 * (p[0][0] + p[1][1]) - _root_of(p)))
    lie = e["major_bearing_deg"] % 180.0
    oblique = min(lie, abs(lie - 90.0), 180.0 - lie) > 22.5
    if oblique and major >= 1.0 and major >= DOUBT_THIN_RATIO * minor:
        index = int(round(lie / 22.5)) % 8  # the sixteen points, a line and its reciprocal one
        one = units.point_name(math.radians(index * 22.5))
        other = units.point_name(math.radians(index * 22.5 + 180.0))
        return (
            f"I would not trust the reckoning within {doubt_miles_words(major)} {one} and "
            f"{other}, nor {doubt_miles_words(minor)} across."
        )
    east = math.sqrt(max(0.0, p[0][0]))
    north = math.sqrt(max(0.0, p[1][1]))
    return (
        f"I would not trust the reckoning within {doubt_miles_words(east)} east or west, "
        f"nor {doubt_miles_words(north)} north or south."
    )


def _root_of(p: list[list[float]]) -> float:
    diff = 0.5 * (p[0][0] - p[1][1])
    return math.sqrt(diff * diff + p[0][1] * p[0][1])


def trust_words(sigma_nm: float) -> str:
    """'within two miles', 'within four cables': how far the master would trust a figure,
    which is twice its doubt (`OBSERVATION_OUT_SIGMAS`, as the lunar's and the
    chronometer's words already say it)."""
    return f"within {doubt_miles_words(OBSERVATION_OUT_SIGMAS * sigma_nm)}"


def verdict_words(obs: Observation, by: str = "the observation", what: str | None = None) -> str:
    """What the master did, as the clause that ends an observation's line (package 37e:
    the words are a model's whole view of it). Taken: "the reckoning was out by it;
    laid down by the observation: moved six miles to the S". Weighed: "the account
    moved four cables to the N". Kept: "the account kept". Doubted (package 37j), the
    observation the poorer figure and further from the account than the two doubts
    together: "the sight stands five miles to the N of the account, and the account,
    good to three cables, is the better figure: the account kept" (`doubted_words`;
    `what` names the observation there, `by` unless said)."""
    from freesail.world.geo import distance_words

    if obs.how == KEPT:
        base = "the account kept"
    else:
        went = (
            f"moved {distance_words(obs.moved_nm * units.NAUTICAL_MILE)} to the "
            f"{units.point_name(math.radians(obs.toward_deg))}"
        )
        if obs.how == TAKEN:
            return f"the reckoning was out by it; laid down by {by}: {went}"
        base = f"the account {went}"
    if obs.doubted:
        return f"{doubted_words(obs, what or by)}: {base}"
    return base


def doubted_words(obs: Observation, what: str = "the observation") -> str:
    """The master's doubt of an observation (package 37j): "the sight stands five miles
    to the N of the account, and the account, good to three cables, is the better
    figure"."""
    from freesail.world.geo import distance_words

    off = distance_words(max(units.CABLE, obs.off_nm * units.NAUTICAL_MILE))
    side = units.point_name(math.radians(obs.off_toward_deg))
    good = doubt_miles_words(obs.account_sigma_nm)
    return (
        f"{what} stands {off} to the {side} of the account, and the account, good to "
        f"{good}, is the better figure"
    )


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

    # the mark the last bearing was taken of (package 37d), for a second of the same mark
    # crossed with it; a class default, so that a checkpoint from before loads with it
    _last_bearing_mark: str | None = None
    # Package 37e, each with a plain class default for the same reason. The master's
    # sailing directions, looked up at their first use; the traverse board's four states
    # (`_peg`: `_run_n` None is a board from before, counted the old way once); her drift
    # hove to, summed; whether the log's last read is from before she lay to or lay
    # becalmed; the master's tide worked since the last step, by the quarter hour; the
    # book's stream for the doubt; what the log last said of his tide; whose tide the work
    # since noon carried; and the account and the doubt as last worked for a reading.
    directions: Any = None
    _run_n: int | None = None
    _hove_n: int = 0
    _riding_n: int = 0
    _calm_n: int = 0
    _dve: float = 0.0
    _dvn: float = 0.0
    _read_stale: bool = False
    _eye_sum: float = 0.0  # her way by eye summed over the ticks she had way on
    _eye_at_read: float | None = None  # her way by eye when the log was last hove
    _tide_e: float = 0.0
    _tide_n: float = 0.0
    _tide_from: int | None = None
    _tide_riding_n: int = 0
    _stream_rate_h: float = 0.0
    _stream_h: float = 0.0
    _stream_water: str | None = None
    _stream_set: float = 0.0
    _tide_said: tuple[str, bool] | None = None
    _tide_seen: tuple[str, bool] | None = None
    _tide_used: tuple[str, ...] = ()
    _now: Any = None
    _doubt: Any = None
    _cast_ground: tuple[float, float] | None = None  # where the ground's first cast was laid
    # package 37j: where the account stood at the last cast that did not agree with the chart
    _apart_ground: tuple[float, float] | None = None
    _ports: Any = None
    _highs: Any = None
    # package 37j: whether she lay to at the last tick pegged, for the board's end at
    # heaving to and filling away (None: not yet looked at)
    _board_lying: bool | None = None

    def __init__(self, world: Any, stream: random.Random):
        self.world = world
        self.stream = stream
        origin: Position = world.origin
        self.errors = CompassErrors.draw(stream)
        # the departure: where she is, a mile in doubt (package 37j: the position at the
        # start is the truth, as a departure taken from the land in sight is, and the
        # mile is the doubt and no error; until then every scenario opened with the
        # account drawn a mile out, which no departure is)
        self.reckoning = Reckoning(origin, world.clock.tick)
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
        # the captain's tide (package 34; spec M5 §16; T §2, §5): the epitome's table of
        # high water at full and change, the scenario's choice or the ship's (a ship of
        # war carries Norie's hours and minutes, the rest Moore's points), and Moore's
        # rule of 48 minutes; the world's tide is never read here
        from freesail.world.tide import Epitome

        table = getattr(world.scenario, "epitome", None)
        if not table:
            table = "norie" if _ship_of_war(world.ship) else "moore"
        self.epitome = Epitome.load(str(table))
        # the traverse board: the heading summed since the last step, and the leeway
        self._hx = 0.0
        self._hy = 0.0
        self._n = 0
        self._run_n = 0  # the ticks she had way on since the last step (package 37e)
        self._leeway_sum = 0.0
        self._close_hauled_n = 0
        self._hove_to_n = 0  # before package 37e: the ticks with no run on the board
        self._sea_heavy = False
        # the master's sailing directions for the streams (package 37e): his own book,
        # as the epitome is; the world's tide is never read here
        from freesail.world.tide import load_directions

        self.directions = load_directions()

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
        self._peg()
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
        if t.second == 0:
            self._say_tide()
        if t.minute == 0 and t.second == 0 and t.hour % self.log_interval_h == 0:
            if not self._riding():  # the log is not hove at anchor (package 34)
                self.heave_log(automatic=True)
        self._tick_noon()

    def _peg(self) -> None:
        """The traverse board pegged for this tick (package 37e). Four states of her, by
        the master's eye: riding at anchor or aground, when the account stays where it
        is and its doubt does not grow; hove to or lying a-try, driving to leeward, when
        he reckons her drift; with no way on (becalmed, in stays), when he runs nothing
        for her; and under way, when her head and her leeway are pegged for the run. In
        every state but the first the tide he allows and his doubt go on by the clock.
        And the master's tide is summed by the quarter hour as it passes."""
        world = self.world
        ship = world.ship
        if self._run_n is None:
            # a board from a checkpoint before package 37e: its no-run ticks (hove to, at
            # anchor) were one count, taken here as riding, and the rest as under way
            old = int(getattr(self, "_hove_to_n", 0))
            self._run_n = max(0, self._n - old)
            self._riding_n, self._hove_n = old, 0
        way_kn = units.ms_to_knots(_speed_through_water(ship))
        lying_to = "hove_to" in (getattr(ship, "extra", None) or {})
        was_lying = bool(self._board_lying)
        if self._board_ends(lying_to, way_kn):
            # each board laid down by itself (package 37j): the account worked up to this
            # minute before the new board is pegged
            self.bring_up()
            if was_lying and not lying_to:
                self.reckoning.lay_by_drift()
        self._n += 1
        if lying_to:
            # a read of the log taken while she lies to is no read of her way when she
            # has filled away: by eye then, until the log is next hove
            self._read_stale = True
        if self._riding():
            self._riding_n += 1
            self._tide_riding_n += 1
            self._read_stale = True
        elif lying_to and way_kn < HOVE_TO_WAY_KN:
            self._hove_n += 1
            east, north = _drift_through_water(ship)
            self._dve += east
            self._dvn += north
        elif way_kn < NO_WAY_KN:
            # no way on: nothing run; a calm of ten minutes and the log's last read is no
            # longer her way when she gathers it again
            self._calm_n += 1
            if self._calm_n >= CALM_MINUTES * 60:
                self._read_stale = True
        else:
            self._calm_n = 0
            self._run_n += 1
            self._eye_sum += round(way_kn / WAY_BY_EYE_GRAIN_KN) * WAY_BY_EYE_GRAIN_KN
            heading = float(ship.heading)
            self._hx += math.sin(heading)
            self._hy += math.cos(heading)
            dyn = getattr(ship, "dyn", None)
            if dyn is not None:
                self._leeway_sum += float(dyn.leeway)
            if self._close_hauled_now():
                self._close_hauled_n += 1
        tick = world.clock.tick
        begun = self.reckoning.last_step_tick if self._tide_from is None else self._tide_from
        if tick - begun >= TIDE_QUARTER_S:
            east, north, rate_h, hours, water, set_rad = self._tide_between(begun, tick)
            self._tide_e += east
            self._tide_n += north
            self._stream_rate_h += rate_h
            self._stream_h += hours
            if water is not None:
                self._stream_water, self._stream_set = water, set_rad
            self._tide_from = tick
            self._tide_riding_n = 0
            self._now = None

    def _board_ends(self, lying_to: bool, way_kn: float) -> bool:
        """Whether the board pegged so far ends at this tick (package 37j): she has hove
        to or filled away, or under way her head has gone `BOARD_ALTERATION_POINTS` or
        more from the mean heading of the board (a tack, a wear, an alteration of course),
        the board being `BOARD_LEAST_S` long at least."""
        was = self._board_lying
        self._board_lying = lying_to
        if self._n <= 0:
            return False
        if was is not None and was != lying_to:
            return True
        if lying_to or way_kn < NO_WAY_KN or self._riding():
            return False
        if (self._run_n or 0) < BOARD_LEAST_S:
            return False
        mean = math.atan2(self._hx, self._hy)
        turned = abs(units.wrap_pi(float(self.world.ship.heading) - mean))
        return turned >= units.points_to_rad(BOARD_ALTERATION_POINTS)

    def _riding(self) -> bool:
        """At anchor or aground (package 34): the ship goes nowhere by the master's
        account, whatever the stream does past her."""
        extra = getattr(self.world.ship, "extra", None) or {}
        if extra.get("aground"):
            return True
        tackle = extra.get("ground_tackle")
        return bool(tackle) and tackle.at_anchor()

    def _close_hauled_now(self) -> bool:
        world = self.world
        rel = abs(units.wrap_pi(float(world.ship.heading) - float(world.wind.direction_from)))
        return units.rad_to_points(rel) <= LEEWAY_ALLOWED_WITHIN_POINTS

    def _heavy_sea(self) -> bool:
        sea = getattr(self.world, "sea", None)
        if sea is None:
            return False
        return sea.reading().state in ("heavy", "very heavy")

    # -- the master's tide (package 37e) --------------------------------------------------
    #
    # "The master should work the tide into the reckoning himself ... as the books give
    # it" (the owner, 2026-10-07). Bowditch 1802, 'Currents': the ship is affected "as if
    # she had sailed in still water, with an additional course and distance exactly equal
    # to the course and set of the current", worked "in the traverse table as one more
    # course". At every step of the account, for the hours since the last, under way,
    # hove to or becalmed and never at anchor or aground, the master adds that course and
    # distance, from his own books and nothing else:
    #   - the water by where his ACCOUNT stands (`tide.Directions.area_at`: if the account
    #     is in the wrong water he works the wrong tide);
    #   - the hour of tide from high water at the nearest place in his epitome, by the
    #     moon's age and Moore's rule, as `tide_by_almanac` works it;
    #   - the rate between the book's neaps and springs by the moon's age, as
    #     `_tide_allowance_m` does for the rise, and through the tide by the half-cosine
    #     from the book's strongest hour;
    #   - summed across the interval by the quarter hour, since the tide may turn in it.
    # THE WORLD KEEPS THE TRUTH AND THE CAPTAIN KEEPS HIS ACCOUNT, FOR THE TIDE AS FOR THE
    # POSITION: no line here reads `Tide.at`, `Tide.stream_at`, `world.tide_state` or the
    # ship's true place (`tests/test_reckoning.py` proves it three ways). The captain's
    # own `allow <n> knots of set` replaces all of it until he hands it back.

    def _directions(self) -> Any:
        if self.directions is None:
            from freesail.world.tide import load_directions

            self.directions = load_directions()
        return self.directions

    def _tide_port(self, where: Position) -> Any:
        """The nearest place of his epitome to a position (his account's), by the
        hundredth of a degree: the place nearest that hundredth's own corner, so that
        what is remembered depends on the hundredth alone and never on who first asked
        from within it (a reading asked at one moment must not change what the working
        gets at another)."""
        key = (round(where.lat_deg, 2), round(where.lon_deg, 2))
        cache = _port_cache(self)
        found = cache.get(key)
        if found is None:
            if len(cache) > 512:
                cache.clear()
            found = cache[key] = self.epitome.nearest(Position(key[0], key[1]))[0]
        return found

    def _high_waters_about(self, port: Any, day: Any) -> list[datetime]:
        """His high waters at a place on a day, the day before and the day after, by
        Moore's rule and the moon's age at each day's noon."""
        cache = _high_water_cache(self)
        key = (port.name, day)
        found = cache.get(key)
        if found is None:
            if len(cache) > 256:
                cache.clear()
            found = []
            for offset in (-1, 0, 1):
                d = day + timedelta(days=offset)
                noon = datetime(d.year, d.month, d.day, 12, 0)
                found += self.epitome.high_waters(port, self.almanac_age_days(noon), d)
            cache[key] = found
        return found

    def book_tide(self, where: Position, when: datetime) -> BookTide | None:
        """The master's own tide at a place and a moment: the stream his directions give
        for that water, at the hour his epitome and almanac make it. `where` is his
        account's position and `when` his clock's time; None where the directions give
        no stream (beyond their limits)."""
        area = self._directions().area_at(where)
        if area is None:
            return None
        port = self._tide_port(where)
        age = self.almanac_age_days(when)
        springs = abs(math.cos(2.0 * math.pi * age / SYNODIC_MONTH_DAYS))
        rate = area.rate_kn(springs)
        highs = self._high_waters_about(port, when.date())
        if not highs:
            return BookTide(area, port, rate, 0.0, None)
        nearest = min(highs, key=lambda t: abs((t - when).total_seconds()))
        hours = (when - nearest).total_seconds() / 3600.0 - area.strongest_h
        along = rate * math.cos(2.0 * math.pi * hours / TIDE_HOURS)
        return BookTide(area, port, rate, along, nearest)

    def _tide_between(
        self, begun: int, tick: int, note: bool = True
    ) -> tuple[float, float, float, float, str | None, float]:
        """The tide the master allows between two ticks (a quarter of an hour, or the
        part of one in hand), as miles east and north: the captain's own set if he has
        ordered one, else the book's stream for the water the account stands in, at the
        hour of the middle of it; nothing for the part of it she rode at anchor. With it,
        for his doubt of the stream: the book's rate at strength times the hours, the
        hours, the water and its set. `note` False is for a reading, which must leave
        nothing behind it: whose tide the day's work carried (`_tide_used`, the noon's
        last sentence) is noted only when the board is pegged and the account worked."""
        ticks = tick - begun
        if ticks <= 0:
            return 0.0, 0.0, 0.0, 0.0, None, 0.0
        afloat = max(0, ticks - self._tide_riding_n)
        hours = afloat / 3600.0
        if hours <= 0.0:
            return 0.0, 0.0, 0.0, 0.0, None, 0.0
        world = self.world
        middle = world.clock.ship_time - timedelta(seconds=0.5 * ticks)
        where = self._account_with(self._tide_e, self._tide_n)
        book = self.book_tide(where, middle)
        rate_h = 0.0 if book is None else book.rate_kn * hours
        water = None if book is None else book.area.id
        set_rad = 0.0 if book is None else book.area.set_rad
        ordered = self.reckoning.set_allowance
        if ordered is not None:
            kn, toward = ordered
            east = kn * hours * math.sin(toward)
            north = kn * hours * math.cos(toward)
            whose = "captain"
        elif book is None:
            east = north = 0.0
            whose = "none"
        else:
            east = book.along_kn * hours * math.sin(book.area.set_rad)
            north = book.along_kn * hours * math.cos(book.area.set_rad)
            whose = "book"
        if note:
            self._tide_used = _with(self._tide_used, whose)
        return east, north, rate_h, hours, water, set_rad

    def tide_allowed(self) -> dict[str, Any]:
        """The tide the master allows in the reckoning at this moment, in words and
        figures, for the reading `the reckoning`, the noon and a shaped course: whose it
        is ('captain', 'book' or 'none'), the knots and where it sets, and for his own
        the water, the place of his high water and when it next turns."""
        r = self.reckoning
        if self._riding():
            return {"by": "none", "knots": 0.0, "words": "none while she rides at anchor"}
        if r.set_allowance is not None:
            kn, toward = r.set_allowance
            if kn <= 0.0:
                return {"by": "captain", "knots": 0.0, "words": "none, by the captain's order"}
            return {
                "by": "captain",
                "knots": kn,
                "toward_deg": round(math.degrees(toward) % 360.0, 1),
                "words": f"by the captain's order, {rate_words(kn)} {ward_words(toward)}",
            }
        now = self.world.clock.ship_time
        book = self.book_tide(self.account_now(), now)
        if book is None:
            return {"by": "none", "knots": 0.0, "words": "none, in open water"}
        toward = book.toward_rad
        turn = book.next_turn(now)
        out = {
            "by": "book",
            "knots": round(abs(book.along_kn), 2),
            "toward_deg": round(math.degrees(toward) % 360.0, 1),
            "flood": book.flood,
            "water": book.area.id,
            "port": book.port.name,
            "rate_kn": round(book.rate_kn, 2),
            "turn": None if turn is None else turn.isoformat(),
        }
        by = (
            f"by the directions for {book.area.name} and high water at {book.port.name} by "
            f"the epitome"
        )
        if abs(book.along_kn) < 0.5 * HOVE_TO_DRIFT_KN:
            making = "flood" if book.making_flood(now) else "ebb"
            out["words"] = f"slack water, the {making} to make, {by}"
        else:
            out["words"] = f"{book.words}, {by}"
        return out

    def _say_tide(self) -> None:
        """Once a minute, under way, hove to or becalmed: a routine line when the
        master's own tide turns and when she passes by his account into other waters
        (package 37e; the events of the tide's turn were the swing at anchor and never
        came under way). Said when the new state has stood two looks together, so an
        account on the edge of two waters does not say one a minute."""
        if self._riding() or self.reckoning.set_allowance is not None:
            self._tide_seen = None
            return
        now = self.world.clock.ship_time
        book = self.book_tide(self.account_now(), now)
        state = ("", True) if book is None else (book.area.id, book.making_flood(now))
        if self._tide_said is None:
            self._tide_said = state  # the tide as she begins: nothing to say of it yet
            return
        if state == self._tide_said:
            self._tide_seen = None
            return
        if state != self._tide_seen:
            self._tide_seen = state
            return
        was, self._tide_said, self._tide_seen = self._tide_said, state, None
        if book is None:
            text = "By the master's reckoning she is beyond his directions: no tide allowed."
            data: dict[str, Any] = {"water": None, "turn": False}
        else:
            what = "flood" if state[1] else "ebb"
            toward = book.area.set_rad if state[1] else book.area.set_rad + math.pi
            allowing = f"{rate_words(book.rate_kn)} to the {units.point_name(toward)}"
            turn = was[0] == state[0]
            if turn:
                text = f"By the master's tide the {what} makes: allowing {allowing}."
            else:
                text = (
                    f"By the master's reckoning she is in {_water_words(book.area.name)}: "
                    f"allowing the {what}, {allowing}."
                )
            data = {
                "water": book.area.id,
                "name": book.area.name,
                "flood": state[1],
                "rate_kn": round(book.rate_kn, 2),
                "toward_deg": round(math.degrees(toward) % 360.0, 1),
                "port": book.port.name,
                "turn": turn,
            }
        self.world.record(Severity.ROUTINE, "reckoning.tide", text, data=data)

    # -- the traverse ------------------------------------------------------------------

    def _working(self, speed_kn: float | None = None, working: bool = False) -> Working | None:
        """The traverse from the last step to this tick as the master would work it now,
        with no draw and nothing changed: the hours under way and the course and way for
        them, the hours hove to and her drift, the hours of the clock she was not riding,
        and the tide he allows. None when no time has passed. `working` is True only when
        the account is being worked (`bring_up`): a reading leaves nothing behind it."""
        r = self.reckoning
        tick = self.world.clock.tick
        hours = (tick - r.last_step_tick) / 3600.0
        n = self._n
        if hours <= 0.0 or n <= 0:
            return None
        run_n = self._run_n or 0
        run_h = hours * run_n / n
        hove_h = hours * self._hove_n / n
        clock_h = hours * max(0, n - self._riding_n) / n
        heading = math.atan2(self._hx, self._hy) % units.TWO_PI
        close_hauled = run_n > 0 and self._close_hauled_n * 2 > run_n
        leeway_allowed = 0.0
        if close_hauled:
            # the master's estimate by eye: the physics' leeway plus his bias
            leeway_allowed = self._leeway_sum / run_n + units.points_to_rad(
                self.errors.leeway_bias_points
            )
        course = heading + leeway_allowed + self.errors.course_error_rad(heading)
        # her way for the hours she had it: the log's read, allowed by the mate's eye for
        # what she has gained or lost of it over the interval (`WAY_BY_EYE_GRAIN_KN`)
        read_sigma = LOG_READ_SIGMA_KN
        eye_mean = self._eye_sum / run_n if run_n > 0 else 0.0
        eye_now = self._eye_now_kn()
        if speed_kn is not None and eye_now >= 1.0 and eye_mean > 0.0:
            # the log is hove now: her way now by the line, and over the interval so much
            # more or less of it as the eye made it
            read = speed_kn * _allowed(eye_mean / eye_now)
        elif self.last_log_read_kn is None or self._read_stale:
            # no read yet, or the last is from before she lay to or lay becalmed: her way
            # by eye until the log is next hove (to the knot, as the mate would say it)
            read, read_sigma = float(round(eye_mean)), SPEED_BY_EYE_SIGMA_KN
        else:
            read = float(self.last_log_read_kn)
            at = self._eye_at_read
            if at is not None and at >= 1.0 and eye_mean > 0.0:
                read *= _allowed(eye_mean / at)
        # her drift hove to, by his eye: the line she drives on by his compass and the
        # rate to the quarter knot
        drift_e = drift_n = 0.0
        if self._hove_n > 0 and hove_h > 0.0:
            east = units.ms_to_knots(self._dve / self._hove_n)
            north = units.ms_to_knots(self._dvn / self._hove_n)
            rate = round(math.hypot(east, north) / HOVE_TO_DRIFT_KN) * HOVE_TO_DRIFT_KN
            if rate > 0.0:
                line = math.atan2(east, north)
                line += self.errors.course_error_rad(line)
                drift_e = rate * hove_h * math.sin(line)
                drift_n = rate * hove_h * math.cos(line)
        # the tide: the quarters pegged and the part of one in hand
        begun = r.last_step_tick if self._tide_from is None else self._tide_from
        east, north, rate_h, stream_h, water, set_rad = self._tide_between(
            begun, tick, note=working
        )
        tide_e, tide_n = self._tide_e + east, self._tide_n + north
        rate_h += self._stream_rate_h
        stream_h += self._stream_h
        if water is None:
            water, set_rad = self._stream_water, self._stream_set
        stream = None
        if water is not None and stream_h > 0.0:
            stream = (water, rate_h / stream_h, set_rad, stream_h)
        return Working(
            run_h,
            course,
            read,
            read_sigma,
            close_hauled,
            clock_h,
            hove_h,
            (drift_e, drift_n),
            (tide_e, tide_n),
            stream,
        )

    def _account_with(self, tide_e: float, tide_n: float) -> Position:
        """The last worked position run on to now by the board, with so much tide: the
        account as the master has it in the middle of a working."""
        r = self.reckoning
        tick = self.world.clock.tick
        hours = (tick - r.last_step_tick) / 3600.0
        n = self._n
        if hours <= 0.0 or n <= 0:
            return r.position
        run_n = self._run_n or 0
        de, dn = tide_e, tide_n
        read = self.last_log_read_kn
        if read is None or self._read_stale:
            read = float(round(self._eye_sum / run_n)) if run_n > 0 else 0.0
        if run_n > 0 and read > 0.0:
            heading = math.atan2(self._hx, self._hy) % units.TWO_PI
            course = heading + self.errors.course_error_rad(heading)
            if self._close_hauled_n * 2 > run_n:
                course += self._leeway_sum / run_n + units.points_to_rad(
                    self.errors.leeway_bias_points
                )
            run = read * hours * run_n / n
            de += run * math.sin(course)
            dn += run * math.cos(course)
        return _displaced(r.position, de, dn)

    def _state_key(self) -> tuple:
        """Everything the account brought up to this moment is worked from: the tick,
        the account as last worked, the traverse board as pegged so far, the log's last
        read and whose tide is allowed. The remembered account and doubt are good only
        while this stands."""
        r = self.reckoning
        p = r.P
        return (
            self.world.clock.tick,
            r.lat_deg,
            r.lon_deg,
            r.last_step_tick,
            r.set_allowance,
            p[0][0],
            p[0][1],
            p[1][1],
            self._n,
            self._run_n,
            self._hove_n,
            self._riding_n,
            self.last_log_read_kn,
            self._read_stale,
            self._eye_at_read,
            self._tide_e,
            self._tide_n,
        )

    def account_now(self) -> Position:
        """The account as the mate brings it up from the log-board at this moment, for a
        reading or the chart: the last worked position run on at the log's last read
        along the traverse board's mean heading since, corrected as the master corrects
        it, with her drift hove to and the tide he allows (package 37e), with no draw
        and nothing changed (a reading never moves the account; the master works it at
        the heave, the noon and by order). Worked once and remembered while nothing it
        is worked from has changed (`_state_key`): a reading asked at one moment of a
        tick must not change what another gets later in it, or a game with a chart open
        would not be the game replayed."""
        r = self.reckoning
        key = self._state_key()
        if self._now is not None and self._now[0] == key:
            return self._now[1]
        w = self._working()
        if w is None:
            now = r.position
        else:
            run = max(0.0, w.read) * w.run_h
            de = run * math.sin(w.course) + w.drift[0] + w.tide[0]
            dn = run * math.cos(w.course) + w.drift[1] + w.tide[1]
            now = _displaced(r.position, de, dn)
        self._now = (key, now)
        self._doubt = None
        return now

    def doubt_now(self) -> dict[str, Any]:
        """The master's doubt at this moment (package 37e: it grows by the hour, so a
        reading two hours after the last working must not give the doubt as it stood
        then): the ellipse as the next working would leave it, with his sentence, and
        nothing changed."""
        r = self.reckoning
        key = self._state_key()
        if self._doubt is not None and self._doubt[0] == key:
            return self._doubt[1]
        w = self._working()
        if w is None:
            p = r.P
        else:
            ghost = Reckoning(r.position, r.last_step_tick)
            ghost.P = [row[:] for row in r.P]
            ghost.set_doubt = list(r.set_doubt)
            ghost.leeway_doubt = list(r.leeway_doubt)
            ghost.stream_doubt = list(r._stream_doubt())
            ghost.stream_water = r.stream_water
            r._biases()
            ghost.run_doubt = list(r.run_doubt or (0.0, 0.0))
            ghost.course_doubt = list(r.course_doubt or (0.0, 0.0))
            ghost.read_doubt = list(r.read_doubt or (0.0, 0.0))
            ghost.drift_doubt = list(r._drift_doubt())
            ghost.advance(
                w.run_h,
                w.course,
                w.read,
                self.world.clock.tick,
                close_hauled=w.close_hauled,
                heavy_sea=self._heavy_sea(),
                leeway_doubt_rad=units.points_to_rad(LEEWAY_DOUBT_POINTS),
                read_sigma_kn=w.read_sigma,
                clock_hours=w.clock_h,
                also=(w.drift[0] + w.tide[0], w.drift[1] + w.tide[1]),
                also_sigma_nm=HOVE_TO_DRIFT_SIGMA_KN * w.hove_h,
                stream=w.stream,
                run_doubt=LOG_LINE_DOUBT,
                course_doubt_rad=math.radians(self.compass_allowance_deg()),
                held=True,
            )
            p = ghost.P
        out = _ellipse_of(p) | {"words": doubt_words(p)}
        self._doubt = (key, out)
        return out

    def bring_up(self, speed_kn: float | None = None) -> tuple[float, float]:
        """Bring the account up to this tick from the last step: the course from the
        traverse board (the mean heading of the hours she had way on), corrected as the
        master corrects it, the run at the log's last read (or `speed_kn`), her drift
        for the hours hove to, the tide he allows for the hours of the clock (package
        37e), the doubt grown. Returns the miles east and north made."""
        world = self.world
        tick = world.clock.tick
        w = self._working(speed_kn, working=True)
        if w is None:
            return 0.0, 0.0
        heavy = self._heavy_sea()
        steer = self.stream.gauss(
            0.0,
            units.points_to_rad(
                STEERING_SIGMA_POINTS_SEAWAY if heavy else STEERING_SIGMA_POINTS_SMOOTH
            ),
        )
        made = self.reckoning.advance(
            w.run_h,
            w.course,
            w.read,
            tick,
            steer_error_rad=steer,
            close_hauled=w.close_hauled,
            heavy_sea=heavy,
            leeway_doubt_rad=units.points_to_rad(LEEWAY_DOUBT_POINTS),
            read_sigma_kn=w.read_sigma,
            clock_hours=w.clock_h,
            also=(w.drift[0] + w.tide[0], w.drift[1] + w.tide[1]),
            also_sigma_nm=HOVE_TO_DRIFT_SIGMA_KN * w.hove_h,
            stream=w.stream,
            run_doubt=LOG_LINE_DOUBT,
            course_doubt_rad=math.radians(self.compass_allowance_deg()),
            held=True,
        )
        self._hx = self._hy = 0.0
        self._n = 0
        self._run_n = 0
        self._eye_sum = 0.0
        self._hove_n = 0
        self._riding_n = 0
        self._dve = self._dvn = 0.0
        self._leeway_sum = 0.0
        self._close_hauled_n = 0
        self._hove_to_n = 0
        self._tide_e = self._tide_n = 0.0
        self._tide_from = None
        self._tide_riding_n = 0
        self._stream_rate_h = self._stream_h = 0.0
        self._stream_water = None
        self._now = None
        self._doubt = None
        return made

    def _speed_by_eye_kn(self) -> float:
        """Her way as the master judges it by eye before the log's first read: through
        the water, to the knot (`SPEED_BY_EYE_SIGMA_KN`)."""
        return float(round(units.ms_to_knots(_speed_through_water(self.world.ship))))

    def _eye_now_kn(self) -> float:
        """Her way at this moment as the mate's eye has it beside a read of the log, to
        the half knot (`WAY_BY_EYE_GRAIN_KN`)."""
        way = units.ms_to_knots(_speed_through_water(self.world.ship))
        return round(way / WAY_BY_EYE_GRAIN_KN) * WAY_BY_EYE_GRAIN_KN

    def _way_kn(self) -> float:
        """Her way as the master has it at this moment: the log's last read, or by eye
        when there is none yet or it is from before she lay to."""
        if self.last_log_read_kn is None or self._read_stale:
            return self._speed_by_eye_kn()
        return float(self.last_log_read_kn)

    def _way_to_shape_by_kn(self) -> float:
        """Her way for a course shaped now: the log's last read or by eye, as `_way_kn`;
        but a course is often shaped as she fills away or gets under way, with hardly any
        way on yet, and the allowance is for the leg to come, so when her way by eye is
        less than the log's last read before she lay to, that read is what she is
        reckoned to make again (a course shaped at one knot of way for a six-knot leg
        stood her thirty degrees off it)."""
        way = self._way_kn()
        if self._read_stale and self.last_log_read_kn is not None:
            way = max(way, float(self.last_log_read_kn))
        return way

    def compass_allowance_deg(self) -> float:
        """What the master allows for the compass's own error in a bearing: the chart's
        old variation and the deviation, of which he knows only the likely size
        (`COMPASS_ALLOWANCE_DEG`); less once he has the variation by an amplitude or an
        azimuth (`COMPASS_ALLOWANCE_OBSERVED_DEG`)."""
        by = str(getattr(self.variation, "by", ""))
        return (
            COMPASS_ALLOWANCE_DEG if by.startswith("the chart") else COMPASS_ALLOWANCE_OBSERVED_DEG
        )

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
        self.reckoning.new_read()
        self.last_log_read_kn = read
        self.last_log_tick = world.clock.tick
        self._eye_at_read = self._eye_now_kn()
        self._read_stale = False  # her way by the log again, and no longer by eye
        self._calm_n = 0
        self._moved()
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
        the arming's ground, matched to the chart's contour about the reckoning and
        worked as a line by the one rule (package 37e): as good a line as the bottom is
        steep there, and no line at all over a flat one; the line."""
        world = self.world
        chart = world.chart
        pos = world.position
        tick = world.clock.tick
        truth = chart.depth_at(pos) if chart is not None and pos is not None else None
        if truth is not None:
            # the lead reads the water there is (package 34, spec M5 §16): the chart's
            # depth at the datum and the tide's height over it
            truth += float(getattr(world, "tide_height_m", 0.0))
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
        tolerance = CONTOUR_TOLERANCE_DEEP_FATHOMS if deep else CONTOUR_TOLERANCE_HAND_FATHOMS
        give = units.fathoms_to_m(tolerance)
        # The tide's height by his own book (package 37j; package 34's flat three metres
        # where his table gave no rise, and in game 10 the cast at St Mary's read nearly a
        # fathom more than the chart where she truly was, and was laid down a mile off):
        # the cast reduced to the chart's datum by the rise and the hour his epitome gives
        # for the nearest place in it to his account, never the world's tide
        allowed_m = self._tide_allowance_m()
        on_chart_m = max(0.0, depth_m - allowed_m)

        def ground_of(p: Position, d: float) -> str:
            return ground_words(chart, p, d)

        # The cast not beyond doubt (package 37j). He looks for the cast's depth and
        # ground within his doubt (`OBSERVATION_OUT_SIGMAS` of it, the ellipse as it lies)
        # and no further: a cast says only that the bottom is not what was expected, and
        # never moves the account further than the account's own doubt.
        holds, reach_nm = r.within_doubt(OBSERVATION_OUT_SIGMAS)
        reach_nm = max(CONTOUR_GRAIN_M / units.NAUTICAL_MILE, reach_nm)
        step_m = min(CONTOUR_GRAIN_M, max(CONTOUR_FINEST_M, reach_nm * units.NAUTICAL_MILE / 4.0))
        found = chart.contour_point(
            r.position,
            on_chart_m,
            give,
            reach_nm * units.NAUTICAL_MILE,
            ground=ground,
            ground_of=ground_of,
            step_m=step_m,
            inside=holds,
        )
        # The chart's own grain. Where the chart about his account shows less water on one
        # hand and more on the other than the cast, the cast agrees with the account as
        # nearly as the chart can say, and he keeps it, narrowing nothing (package 37e: the
        # frigate a cable out by her fix off Black Head was "laid down by the cast" two
        # miles away)
        agrees = False
        if found is None or bearing_and_distance(r.position, found[0])[1] > CONTOUR_GRAIN_M:
            least, most = chart.depth_span(r.position, CONTOUR_GRAIN_M)
            if least - give <= on_chart_m <= most + give:
                found, agrees = (r.position, 0.0), True
        obs: Observation | None = None
        apart: dict[str, Any] | None = None
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
            # a second cast on the same ground narrows nothing further: the chart's
            # error there and his own allowance for the tide are in every cast alike
            reach = max(SOUNDING_SLOPE_NM, r.ellipse()["semi_major_nm"])
            across = self._sounding_sigma_nm(point, tolerance, reach)
            first = self._cast_ground
            same = (
                first is not None
                and bearing_and_distance(r.position, Position(*first))[1]
                <= max(SAME_GROUND_NM, reach) * units.NAUTICAL_MILE
            )
            obs = r.observe_line(de, dn, n_e, n_n, across, narrow=not (same or agrees))
            if not same or obs.how == TAKEN:
                self._cast_ground = (r.lat_deg, r.lon_deg)  # new ground, and its first cast
            self._moved()
        else:
            # Nothing within his doubt answers the cast: the cast does not agree with the
            # chart where he believes her. The account is kept; and his doubt is grown so
            # far, toward the nearest water of that depth and ground the chart shows
            # beyond it, that that water lies at the edge of what he would trust it
            # within: he no longer swears she is not there.
            beyond_nm = max(CONTOUR_SEARCH_MIN_NM, 2.0 * reach_nm)
            far = chart.contour_point(
                r.position,
                on_chart_m,
                give,
                beyond_nm * units.NAUTICAL_MILE,
                ground=ground,
                ground_of=ground_of,
            )
            apart = {"beyond_nm": beyond_nm}
            # a second cast on the ground of one that did not agree is the same thing seen
            # again (the chart's error there, or his tide's), and widens nothing further
            was = self._apart_ground
            again = (
                was is not None
                and bearing_and_distance(r.position, Position(*was))[1]
                <= SAME_GROUND_NM * units.NAUTICAL_MILE
            )
            if far is not None:
                de, dn = r.offset_nm(far[0])
                grown = 0.0
                if not again:
                    # just beyond the edge, so that the same cast again stays apart
                    grown = r.widen_toward(de, dn, OBSERVATION_OUT_SIGMAS * (1.0 + APART_EDGE))
                    self._apart_ground = (r.lat_deg, r.lon_deg)
                    self._moved()
                apart |= {
                    "nearest_nm": round(math.hypot(de, dn), 2),
                    "toward": units.point_name(math.atan2(de, dn)),
                    "grown_nm": round(grown, 2),
                    "again": again,
                }
        text = f"{chant(fathoms, not deep)}; {ground}."
        if allowed_m >= units.fathoms_to_m(1.0):
            # the reduction said when it is a fathom or more (package 37j)
            text += (
                f" {_head(fathoms_said(allowed_m))} of tide allowed by the epitome: "
                f"{fathoms_said(on_chart_m)} on the chart."
            )
        if obs is not None:
            text += f" {_head(verdict_words(obs, 'the cast'))}."
        elif apart is not None:
            if "nearest_nm" in apart:
                from freesail.world.geo import distance_words

                where = (
                    f"; the chart has that water nearest "
                    f"{distance_words(apart['nearest_nm'] * units.NAUTICAL_MILE)} to the "
                    f"{apart['toward']} of the account"
                )
                kept = (
                    "the account kept"
                    if apart["again"]
                    else "the account kept, and its doubt widened"
                )
            else:
                where = f", nor within {miles_words(apart['beyond_nm'])} of the account"
                kept = "the account kept"
            text += (
                f" The cast does not agree with the chart where {self.master.name} believes "
                f"her{where}: {kept}."
            )
        self._record_cast(tick, depth_m, ground, text, deep, obs, allowed_m=allowed_m, apart=apart)

    def _sounding_sigma_nm(
        self, point: Position, tolerance_fathoms: float, reach_nm: float = SOUNDING_SLOPE_NM
    ) -> float:
        """How good a line a cast is where it was matched (package 37e): the tolerance in
        fathoms over the fathoms the charted depth changes in a mile across the contour
        there. "A cast of the lead narrows the doubt only so far as the charted depth
        differs across his doubt" (the brief): the slope is read over `reach_nm` either
        way, his doubt's own reach and at least `SOUNDING_SLOPE_NM`. A quarter of a mile
        at the best, and leagues over a flat bottom, where a cast is no line at all."""
        chart = self.world.chart
        reach_nm = max(SOUNDING_SLOPE_NM, reach_nm)
        step = reach_nm * units.NAUTICAL_MILE
        here = chart.depth_at(point)
        if here is None:
            return SOUNDING_ACROSS_MAX_NM

        def depth(dx: float, dy: float) -> float:
            d = chart.depth_at(point.advanced(dx, dy))
            return here if d is None else d

        gx = (depth(step, 0.0) - depth(-step, 0.0)) / (2.0 * reach_nm)
        gy = (depth(0.0, step) - depth(0.0, -step)) / (2.0 * reach_nm)
        slope = units.m_to_fathoms(math.hypot(gx, gy))  # fathoms a mile
        if slope <= tolerance_fathoms / SOUNDING_ACROSS_MAX_NM:
            return SOUNDING_ACROSS_MAX_NM
        return max(SOUNDING_ACROSS_MIN_NM, tolerance_fathoms / slope)

    def _moved(self) -> None:
        """The account was worked by an observation: what was remembered of it for this
        tick is forgotten."""
        self._now = None
        self._doubt = None

    def tide_height_by_master_m(self) -> float:
        """The tide's height above low water now by the master's own reckoning (his
        epitome's rise and hour, `_masters_tide`): what the water where she lies will
        fall by to low water, as he would tell the captain letting go an anchor (package
        37f). Never the world's tide."""
        tide = self._masters_tide()
        if tide is None:
            return TIDE_ALLOWANCE_DEFAULT_M
        _spring_m, range_m, phase = tide
        return 0.5 * range_m * (1.0 + math.cos(phase))

    def _tide_allowance_m(self) -> float:
        """What the master takes off a cast for the tide before he lays it on the chart:
        his own tide, never the world's (decision 29), the height above his chart's
        datum, which is low water at springs (package 37j: until then the height above
        the day's low water, which at the neaps stands above the datum by half the
        difference of the two rises). Half the spring rise of the nearest place in his
        epitome to his account, and half the day's rise (the spring rise at full and
        change, two-thirds of it at the quarters: Norie's rule of thumb,
        `NEAP_RISE_OF_SPRING`) by the half-cosine of the time from his high water
        (`tide_by_almanac`) over the tide's twelve hours and twenty-five minutes, which
        is the rule of twelfths worked exactly; `TIDE_ALLOWANCE_DEFAULT_M` where the table
        gives no rise for the place."""
        tide = self._masters_tide()
        if tide is None:
            return TIDE_ALLOWANCE_DEFAULT_M
        spring_m, range_m, phase = tide
        return 0.5 * spring_m + 0.5 * range_m * math.cos(phase)

    def _masters_tide(self) -> tuple[float, float, float] | None:
        """The master's own tide at his account now: the spring rise of the nearest place
        in his epitome, the day's rise by the moon's age, and the phase from his nearest
        high water (radians, nought at high water); None where his table gives no rise
        there. His epitome, his almanac and his account, and nothing of the world's."""
        epitome = getattr(self, "epitome", None)
        if epitome is None:
            return None
        port, _ = epitome.nearest(self.reckoning.position)
        if port.spring_rise_ft is None:
            return None
        age = self.almanac_age_days()
        springs = abs(math.cos(2.0 * math.pi * age / SYNODIC_MONTH_DAYS))
        spring_m = units.feet_to_m(port.spring_rise_ft)
        range_m = spring_m * (NEAP_RISE_OF_SPRING + (1.0 - NEAP_RISE_OF_SPRING) * springs)
        now = self.world.clock.ship_time
        day = now.date()
        highs = epitome.high_waters(port, age, day) + epitome.high_waters(
            port, age + 1.0, day + timedelta(days=1)
        )
        if not highs:
            return spring_m, range_m, 0.5 * math.pi
        nearest = min(highs, key=lambda t: abs((t - now).total_seconds()))
        hours = (now - nearest).total_seconds() / 3600.0
        return spring_m, range_m, 2.0 * math.pi * hours / TIDE_HOURS

    def _record_cast(
        self,
        tick: int,
        depth_m: float | None,
        ground: str,
        text: str,
        deep: bool,
        obs: Observation | None = None,
        allowed_m: float | None = None,
        apart: dict[str, Any] | None = None,
    ) -> None:
        r = self.reckoning
        cast = Sounding(tick, depth_m, ground, text, r.lat_deg, r.lon_deg, deep)
        self.last_cast = cast
        r.soundings.append(cast)
        self.world.record(
            # a cast that finds no bottom is the watch's routine work, and tells her
            # nothing but that she is off soundings still (package 37f; the review of
            # gate 5c's playtests, 8.2: notable, each one woke a station standing by "at
            # a sounding" for the bottom, and the merchant passage logged them by the
            # score); bottom found is notable, as it was
            Severity.ROUTINE if depth_m is None else Severity.NOTABLE,
            "sounding",
            text,
            data={
                "depth_m": None if depth_m is None else round(depth_m, 2),
                "fathoms": None if depth_m is None else round(units.m_to_fathoms(depth_m), 2),
                "ground": ground,
                "deep": deep,
                "reckoning": r.words,
                "moved_nm": 0.0 if obs is None else round(obs.moved_nm, 2),
                "matched": obs is not None,
                "how": None if obs is None else obs.how,
                "line_sigma_nm": None if obs is None else round(obs.sigma_nm, 2),
                # package 37j: the master's own tide taken off before he laid it on the
                # chart, and a cast that did not agree with the chart within his doubt
                "tide_allowed_m": None if allowed_m is None else round(allowed_m, 2),
                "agrees": None if depth_m is None else apart is None,
                "apart": apart,
            },
        )

    # -- bearings -----------------------------------------------------------------------

    def take_bearing(self, name: str) -> tuple[str, dict[str, Any]]:
        """`take a bearing of <mark>`: the mark in sight by the lookout's name, or 'the
        land' or 'the light' for the nearest such; the bearing by compass with its error,
        worked as a line by the one rule (package 37e), and after it the lookout's
        distance by estimation as a second line along the sight, by the same rule: each
        is weighed against the account by their two doubts, taken when the account is
        plainly out, and tells him nothing new when it is the same thing seen again from
        the same place. The words say which. A sail's bearing is given and moves nothing
        (she is no mark: a line through her true position is a line through the ship's);
        a transit of the chart's when both its marks are in sight and in one. Refused in
        words when it is not in sight."""
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
        r = self.reckoning
        judged_m = max(0.1 * units.NAUTICAL_MILE, float(found.judged_m))
        estimate = estimate_words(judged_m)
        said = (
            f"{_head(found.feature.name)} bore {units.point_name(laid)}, {estimate} by estimation"
        )
        if found.seen_as == "sail":
            # a sail is no mark (package 37d): her bearing in words and data, the account
            # as it was (on the Harpy one bearing of a pilot's boat moved it ten miles);
            # her place is the truth's and is in no data
            return f"{said}.", {
                "tick": world.clock.tick,
                "id": found.feature.id,
                "name": found.feature.name,
                "bearing_deg": round(math.degrees(laid), 1),
                "sail": True,
                "estimate_m": round(judged_m),
                "estimate": estimate,
                "reckoning": r.words,
                "moved_nm": 0.0,
            }
        self.bring_up()
        before = r.position
        mark = found.feature.position
        fid = found.feature.id
        # the doubt across the line at the mark's distance by the account (the master's
        # own figure: the truth's distance is not read), with what he allows for the
        # compass's own error, which is the same in every bearing he takes
        de, dn = r.offset_nm(mark)
        away_nm = math.hypot(de, dn)
        allowance = self.compass_allowance_deg()
        sigma = _bearing_sigma_nm(away_nm * units.NAUTICAL_MILE, allowance)
        shared = away_nm * math.tan(math.radians(allowance))
        thing = f"{fid}:bearing"
        toward = math.atan2(de, dn)
        n_e, n_n = math.cos(toward), -math.sin(toward)  # square to the sight
        if away_nm < 1e-6 or math.sqrt(r._across(n_e, n_n)) > BEARING_LINE_FORM_FRACTION * away_nm:
            # the account's doubt is not small beside the distance to the mark: the line
            # itself is laid down, from the mark along the reciprocal of the bearing
            line = r.observe_bearing(mark, laid, sigma, thing, shared)
        else:
            # the bearing as an angle measured at the account, its line's normal square
            # to the mark as the account has it (package 37d): it moves the account
            # across the sight and no more, while a bearing of another mark still crosses
            # it and a second of the same mark after a run is a running fix
            z = -away_nm * math.sin(units.wrap_pi(laid - toward))
            line = r.observe_line(z * n_e, z * n_n, n_e, n_n, sigma, thing, shared)
            # A second bearing of the same mark: the doubt is turned with the account
            # about the mark, by the little the account's own bearing of it has just
            # changed. What one mark's bearings leave unknown is how far off she is, and
            # that doubt lies along the line of sight wherever on its arc the account
            # stands; left as it lay, the next bearing of the mark would find the doubt
            # a hair askew to its line and take that for a crossing.
            de2, dn2 = r.offset_nm(mark)
            turn = units.wrap_pi(math.atan2(de2, dn2) - toward)
            same = self._last_bearing_mark == fid
            if same and turn != 0.0 and math.hypot(de2, dn2) > 1e-6:
                c, s = math.cos(turn), math.sin(turn)
                (a, b), (_, d) = r.P
                # R P Rᵀ with R = [[c, s], [-s, c]]: a bearing turned clockwise by `turn`
                r.P = [
                    [c * c * a + 2 * c * s * b + s * s * d, c * s * (d - a) + (c * c - s * s) * b],
                    [c * s * (d - a) + (c * c - s * s) * b, s * s * a - 2 * c * s * b + c * c * d],
                ]
        self._last_bearing_mark = fid
        # The distance off by estimation, a second line along the sight (package 37e, in
        # place of 37d's guard): the eye's sixth of the distance is its doubt, and the
        # eye's error is the sighting's own, the same each time the mark is looked at, so
        # a second estimate of the same mark from the same place tells him nothing new.
        # It is weighed by the two doubts: where the account is the poorer figure along
        # the sight (a landfall on one mark after a long run, a departure) it moves most
        # of the way, and where the account is the better (after a fix) hardly at all. It
        # is never taken, being the eye's guess and no observation: so bearings of
        # different marks cannot jerk the account between their separate errors, and a
        # standing order that takes one every five minutes makes him no surer.
        de, dn = r.offset_nm(mark)
        away_nm = math.hypot(de, dn)
        judged_nm = judged_m / units.NAUTICAL_MILE
        distance: Observation | None = None
        if away_nm > 1e-6:
            sight = math.atan2(de, dn)
            distance = r.observe_distance(
                mark,
                sight,
                judged_nm,
                DISTANCE_BY_ESTIMATION_FRACTION * judged_nm,
                f"{fid}:distance",
            )
        self._moved()
        toward_deg, moved_m = bearing_and_distance(before, r.position)
        moved = moved_m / units.NAUTICAL_MILE
        _, account_m = bearing_and_distance(r.position, mark)
        by_account = estimate_words(account_m)
        differs = (
            abs(account_m - judged_m) > FIX_ACCOUNT_DIFFERS * judged_m and by_account != estimate
        )
        record = Bearing(
            world.clock.tick,
            fid,
            found.feature.name,
            math.degrees(laid),
            found.feature.lat_deg,
            found.feature.lon_deg,
            estimate,
        )
        r.bearings.append(record)
        how = _worst(line, distance)
        if how != KEPT and moved < OBSERVATION_KEPT_NM:
            how = KEPT
        applied = distance is not None and distance.how != KEPT
        if how == KEPT:
            verdict = "the account kept"
        else:
            from freesail.world.geo import distance_words

            went = (
                f"moved {distance_words(moved_m)} to the "
                f"{units.point_name(math.radians(toward_deg))}"
            )
            if how == TAKEN:
                by = "the bearing and its distance" if applied else "the bearing"
                verdict = f"the reckoning was out by it; laid down by {by}: {went}"
            else:
                verdict = f"the account {went}"
        if line.doubted and how != TAKEN:
            # package 37j: the bearing's line the poorer figure and plainly apart from the
            # account, weighed and doubted
            verdict = f"{doubted_words(line, 'the line of the bearing')}: {verdict}"
        aside = f"; {by_account} by the account" if differs else ""
        text = f"{said}{aside}: {verdict}."
        return text, record.to_dict() | {
            "reckoning": r.words,
            "how": how,
            "line": line.how,
            "doubted": line.doubted and how != TAKEN,
            "distance": None if distance is None else distance.how,
            "moved_nm": round(moved, 2),
            "moved_toward": units.point_name(math.radians(toward_deg)),
            "distance_applied": applied,
            "estimate_m": round(judged_m),
            "estimate": estimate,
            "account_m": round(account_m),
            "by_account": by_account,
            "differs": differs,
            "line_sigma_nm": round(sigma, 2),
        }

    # -- the fix by cross bearings (package 37d; its marks and its rule, package 37e) ------

    def _fix_marks(self) -> list[Any]:
        """The charted marks in sight that a fix may be taken by, nearest first: the
        land's headlands, lights, marks and a danger that shows; never the shore close
        aboard, a sail or a transit."""
        from freesail.world.lookout import SHORE_ID

        lookout = self.world.lookout
        marks = [
            s
            for s in lookout.sightings
            if s.seen_as in ("land", "light", "mark", "danger") and s.feature.id != SHORE_ID
        ]
        marks.sort(key=lambda s: s.judged_m)
        return marks

    def take_fix(self, names: list[str] | None = None) -> tuple[str, dict[str, Any]]:
        """`take a fix`, `take a fix by <mark> and <mark>` (or with a third): cross
        bearings of two or three charted marks in sight, and the point that best fits
        their lines (package 37d). Unnamed, the master takes the two or three whose fix
        has the least doubt (package 37e: each line's doubt across it at its mark's
        distance, with the compass's shared error counted, among sets of which some two
        lines cut by `FIX_MIN_CUT_DEG` or more; so a headland a mile off is preferred to
        a town six miles off). Each bearing is taken as `take_bearing` takes one: the
        compass's error for her heading common to the set, and each mark's own draw from
        the reckoning's stream, in the order the marks are said. The fix is the point
        that best fits the lines, each weighed by its own doubt across it at the mark's
        distance; its doubt counts what the master allows for the compass's own error,
        which the lines share (`COMPASS_ALLOWANCE_DEG`), and with three marks is no
        smaller than half the cocked hat. It is then worked by the one rule (package
        37e): taken when the account is plainly out, weighed otherwise, so that a good
        fix still rules a doubtful account and a poor one cannot move a good account.
        Refused in words that carry the cure: nothing in sight; one mark only; marks
        that cut too fine. Returns the line and its data (`notable` when the account
        moved over a mile)."""
        from freesail.evolutions.runner import OrderError
        from freesail.world.geo import distance_words

        world = self.world
        lookout = world.lookout
        if lookout is None:
            raise OrderError("No chart of these waters: there is no mark to take a fix by.")
        marks = self._fix_marks()
        allowance = self.compass_allowance_deg()
        if names:
            chosen = [self._fix_mark_named(name, marks) for name in names]
            if len({s.feature.id for s in chosen}) < len(chosen):
                raise OrderError("A fix wants two or three different marks; one was named twice.")
            if len(chosen) < 2:
                only = chosen[0].feature.name
                raise OrderError(
                    f"One mark gives a line and no fix: name a second with {only}, or take a "
                    f"bearing of {only}."
                )
            if len(chosen) > 3:
                raise OrderError("A fix is taken by two marks or three; name no more.")
            if _best_cut_deg(chosen) < FIX_MIN_CUT_DEG:
                raise OrderError(_too_fine_words(chosen))
        else:
            if not marks:
                if lookout.sightings:
                    raise OrderError(
                        "No charted mark is in sight to take a fix by: the land close aboard "
                        "and a sail are no marks; take a fix when a headland, a mark or a "
                        "light is made out."
                    )
                raise OrderError(
                    "Nothing is in sight to take a fix by; a fix wants two charted marks in sight."
                )
            if len(marks) == 1:
                only = marks[0].feature.name
                raise OrderError(
                    f"Only {only} is in sight, and one mark gives a line and no fix: take a "
                    f"bearing of {only}."
                )
            # the near marks first; when no two of them cut, any in sight
            chosen = _choose_marks(marks[:FIX_MARKS_CONSIDERED], allowance) or _choose_marks(
                marks[:FIX_MARKS_IN_ALL], allowance
            )
            if not chosen:
                raise OrderError(_too_fine_words(marks[:FIX_MARKS_IN_ALL]))
        # the bearings: the compass's error common to the set, each mark's own draw
        heading = float(world.ship.heading)
        common = self.errors.course_error_rad(heading)
        lines = []
        for s in chosen:
            laid = math.radians(s.bearing_deg) + common
            laid += self.stream.gauss(0.0, math.radians(BEARING_SIGMA_DEG))
            lines.append((s, laid % units.TWO_PI))
        self.bring_up()
        r = self.reckoning
        before = r.position
        fix, cov, hat_m = _fix_of(before, lines, allowance)
        # the doubt is the fix's own, and with three lines no smaller than half the hat
        if hat_m is not None:
            floor = (0.5 * hat_m / units.NAUTICAL_MILE) ** 2
            least = _least_eigen(cov)
            if least < floor:
                cov = [
                    [cov[0][0] + floor - least, cov[0][1]],
                    [cov[1][0], cov[1][1] + floor - least],
                ]
        # each line as the same thing seen again knows it: what of its doubt is the
        # compass's own error, the same in every fix by these marks from this place
        had = []
        for s, laid in lines:
            away_nm = bearing_and_distance(fix, s.feature.position)[1] / units.NAUTICAL_MILE
            shared = (away_nm * math.tan(math.radians(allowance))) ** 2
            had.append((f"{s.feature.id}:bearing", math.cos(laid), -math.sin(laid), shared))
        de, dn = r.offset_nm(fix)
        off_m = math.hypot(de, dn) * units.NAUTICAL_MILE
        # how far the compass's own error, one sigma of what he allows for it, moves this
        # fix: the same in every fix by marks on this hand, and never narrowed below
        # (package 37j)
        common = _compass_shift_nm(fix, lines, allowance)
        obs = r.observe_point(de, dn, cov, had, common)
        self._moved()
        self._last_bearing_mark = None
        toward, moved_m = bearing_and_distance(before, r.position)
        if obs.how != KEPT:
            r.track.append((world.clock.tick, r.lat_deg, r.lon_deg))
        for s, laid in lines:
            r.bearings.append(
                Bearing(
                    world.clock.tick,
                    s.feature.id,
                    s.feature.name,
                    math.degrees(laid),
                    s.feature.lat_deg,
                    s.feature.lon_deg,
                    estimate_words(s.judged_m),
                )
            )
        moved_nm = moved_m / units.NAUTICAL_MILE
        bore = ", ".join(f"{s.feature.name} {units.point_name(laid)}" for s, laid in lines)
        cut = _best_cut_deg(chosen) if len(chosen) == 2 else _least_cut_deg(chosen)
        if hat_m is not None:
            met = (
                "the lines met in a point"
                if hat_m < 0.5 * units.CABLE
                else f"the lines met within {distance_words(hat_m)}"
            )
        else:
            met = f"the lines cut at {5 * round(cut / 5.0):.0f} degrees"
        sigma_m = math.sqrt(max(0.0, _greatest_eigen(cov))) * units.NAUTICAL_MILE
        good = distance_words(max(units.CABLE, sigma_m))
        # package 37j: marks all on one hand fix her one way better than the other, and
        # the doubt is said as it lies, along the shore and off it
        hand = _one_hand(lines)
        if hand is not None:
            along_m, off_shore_m = _along_and_off_nm(cov, hand)
            along_m *= units.NAUTICAL_MILE
            off_shore_m *= units.NAUTICAL_MILE
            a_words = distance_words(max(units.CABLE, along_m))
            o_words = distance_words(max(units.CABLE, off_shore_m))
            if a_words != o_words:
                good = f"{a_words} along the shore and {o_words} off it"
        by_fix = f"{format_position(fix)} by the fix, good to {good}"
        went = f"moved {distance_words(moved_m)} to the {units.point_name(math.radians(toward))}"
        if obs.how == TAKEN:
            tail = f"The reckoning was out by it; laid down by the fix: {went}: {by_fix}."
        elif obs.how == WEIGHED and obs.doubted:
            tail = (
                f"{_head(by_fix)}, the fix the poorer figure: "
                f"{doubted_words(obs, 'it')}; the account {went}."
            )
        elif obs.how == WEIGHED:
            tail = f"The account {went}: {by_fix}."
        else:
            within = (
                "within half a cable of it"
                if off_m < 0.5 * units.CABLE
                else f"within {distance_words(max(units.CABLE, off_m))} of it"
            )
            poorer = ", the fix the poorer figure" if obs.poorer or obs.repeat else ""
            tail = f"{_head(by_fix)}{poorer}; the account kept, {within}."
        text = f"Fixed by cross bearings: {bore}; {met}. {tail}"
        data = {
            "marks": [
                {
                    "id": s.feature.id,
                    "name": s.feature.name,
                    "bearing_deg": round(math.degrees(laid), 1),
                    "bearing": units.point_name(laid),
                    "mark_lat_deg": s.feature.lat_deg,
                    "mark_lon_deg": s.feature.lon_deg,
                    "estimate": estimate_words(s.judged_m),
                }
                for s, laid in lines
            ],
            "cut_deg": round(cut, 1),
            "hat_m": None if hat_m is None else round(hat_m),
            "how": obs.how,
            "doubted": obs.doubted,
            "one_hand": hand is not None,
            "moved_nm": round(moved_nm, 2),
            "moved_toward": units.point_name(math.radians(toward)),
            "off_nm": round(off_m / units.NAUTICAL_MILE, 2),
            "lat_deg": round(fix.lat_deg, 5),
            "lon_deg": round(fix.lon_deg, 5),
            "sigma_nm": round(sigma_m / units.NAUTICAL_MILE, 2),
            "reckoning": r.words,
            "notable": moved_nm > FIX_NOTABLE_NM,
        }
        return text, data

    def _fix_mark_named(self, name: str, marks: list[Any]) -> Any:
        """A mark named for a fix: in sight by the lookout's name for it and one a fix
        may be taken by; refused in words for a sail, the shore, a transit, or one not
        in sight."""
        from freesail.evolutions.runner import OrderError

        lookout = self.world.lookout
        found = lookout.find(name)
        if found is None:
            if self._transit_named(name) is not None:
                raise OrderError(
                    f"{_head(name)} is a transit, a line of its own and no mark for a fix: "
                    f"take a bearing of it when its marks are in one."
                )
            in_sight = _and([s.feature.name for s in marks[:8]]) or "no charted mark"
            raise OrderError(
                f"{_head(name)} is not in sight to take a fix by; in sight: {in_sight}."
            )
        if found.seen_as == "sail":
            raise OrderError(
                "A sail is no mark for a fix: her place is not on the chart. Name two charted "
                "marks in sight."
            )
        if all(found.feature.id != s.feature.id for s in marks):
            raise OrderError(f"{_head(found.feature.name)} is no charted mark to take a fix by.")
        return found

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
        obs = r.observe_bearing(
            near.position, math.radians(b_line), TRANSIT_SIGMA_NM, f"{transit.id}:transit"
        )
        self._moved()
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
        text = (
            f"{_head(transit.name)}: on the transit, bearing {point}: "
            f"{verdict_words(obs, 'the transit')}."
        )
        data = record.to_dict() | {
            "reckoning": r.words,
            "moved_nm": round(obs.moved_nm, 2),
            "how": obs.how,
        }
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
        obs: Observation | None = None
        self.sight_day = t.date()
        if result.sight is not None:
            self.last_sight = result.sight
            self.sight_refused = None
            observed = result.sight.latitude_deg
            # by the one rule (package 37e): weighed against the account by their two
            # doubts, and taken when the account is plainly out
            obs = r.observe_latitude(observed, result.sight.sigma_nm)
            self._moved()
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
        if observed is not None and obs is not None:
            head = (
                f"Noon. Latitude by observation {_lat_words(observed)}; the reckoning was "
                f"{_lat_words(account_lat)}: {verdict_words(obs, what='the sight')}."
            )
        else:
            head = f"Noon. No sight; {result.refusal}. Latitude by account {lat_words}."
        since = "since the departure" if first else "since yesterday"
        made = (
            f" Course made good {since} {units.point_name(math.radians(cmg))}, {miles_words(run)}."
            if cmg is not None and run >= 0.5
            else ""
        )
        # whose tide the day's work carried (package 37e)
        carried = _carried_words(self._tide_used, self.reckoning.set_allowance)
        self._tide_used = ()
        text = f"{head}{made} Longitude by account {lon_words}.{carried}"
        data = {
            "noon": noon.to_dict(),
            "sight": None if result.sight is None else result.sight.to_dict(),
            "refusal": result.refusal,
            "reckoning": r.words,
            "uncertainty": r.uncertainty_words,
            "ellipse": r.ellipse(),
            "automatic": automatic,
            "how": None if obs is None else obs.how,
            "moved_nm": 0.0 if obs is None else round(obs.moved_nm, 2),
            "tide": self.tide_allowed(),
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
        tide = self.tide_allowed()
        text = (
            f"The reckoning worked up: {r.words}{made}. {r.uncertainty_words} The tide "
            f"allowed: {tide['words']}."
        )
        data = {
            "reckoning": r.words,
            "ellipse": r.ellipse(),
            "run_since_noon_nm": round(run, 1),
            "tide": tide,
        }
        return text, data

    def set_reckoning(self, pos: Position) -> tuple[str, dict[str, Any]]:
        """`set the reckoning to <lat> <long>`: the captain overrides the master."""
        world = self.world
        self.bring_up()
        self.reckoning.set_position(pos, world.clock.tick)
        self._moved()
        text = f"The reckoning set to {format_position(pos)} by the captain's order."
        data = {"reckoning": self.reckoning.words, "lat_deg": pos.lat_deg, "lon_deg": pos.lon_deg}
        return text, data

    def allow_set(self, knots: float, toward_rad: float | None) -> tuple[str, dict[str, Any]]:
        """`allow <n> knots of set to <direction>`: the captain's own set in the traverse,
        which replaces the master's own tide from this moment until the captain hands it
        back (package 37e; the owner's ruling of 2026-10-07: "replaces when used until
        handed back"); `allow no set` likewise, his word that there is none."""
        self.bring_up()
        r = self.reckoning
        if knots <= 0.0 or toward_rad is None:
            r.set_allowance = (0.0, 0.0)
            text = (
                "No set allowed for in the reckoning, by the captain's order; the master's "
                "own tide is laid by until it is handed back."
            )
        else:
            r.set_allowance = (knots, toward_rad % units.TWO_PI)
            text = (
                f"Allowing {knots_words(knots)} of set to the "
                f"{units.point_name(toward_rad, full=True)} in the reckoning, by the captain's "
                f"order, in place of the master's own tide."
            )
        self._moved()
        self._tide_seen = None
        return text, {"knots": knots, "by": "captain", "tide": self.tide_allowed()}

    def allow_tide_by_book(self) -> tuple[str, dict[str, Any]]:
        """`allow the tide by the book`: the captain hands the tide back to the master,
        who works it from his directions and his epitome again (package 37e)."""
        self.bring_up()
        r = self.reckoning
        was = r.set_allowance
        r.set_allowance = None
        self._moved()
        self._tide_said = self._tide_seen = None  # the log begins again from what he allows now
        tide = self.tide_allowed()
        head = (
            "The tide in the reckoning is the master's already, by the book"
            if was is None
            else "The tide in the reckoning handed back to the master, by the book"
        )
        return f"{head}: {tide['words']}.", {"by": "book", "tide": tide}

    def shape_course(self, place: str) -> tuple[float, str, dict[str, Any]]:
        """`shape a course for <place>`: the course from the reckoning to the chart's
        place (never from the truth), made good against the tide the master allows
        (`shape_for`); (the heading to steer in radians, the words, the data). Refused
        where the chart has no such place."""
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
        return self.shape_for(feature.position, feature.name, feature)

    def shape_for(
        self, target: Position, name: str, feature: Any = None
    ) -> tuple[float, str, dict[str, Any]]:
        """A course shaped for a place of the chart or a point pricked on it, from the
        account (never the truth), and since package 37e made good: by the owner's ruling
        the helm is ordered the course to steer so that, by the master's reckoning, she
        makes good the line from the account to the place, against the tide he allows at
        this hour (his own, or the captain's set), with the leeway he allows when she
        lies close-hauled, at her way by the log's last read or by eye. It is worked
        once, when the course is shaped; nothing alters the helm afterwards. The words
        give the line and the course to steer, and what the line passes: the charted
        dangers (package 33b) and, since 37e, the land (the chart's coast is the captain's
        own paper, so this gives nothing away). Returns (the heading to steer in radians,
        the words, the data)."""
        from freesail.world.chart import DANGER_PASS_NM

        world = self.world
        chart = world.chart
        self.bring_up()
        r = self.reckoning
        bearing, dist = bearing_and_distance(r.position, target)
        line = math.radians(bearing)
        words = (
            f"Shaped a course for {name}: {units.point_name(line)} by account, "
            f"{miles_words(dist / units.NAUTICAL_MILE)}"
        )
        data: dict[str, Any] = {
            "line_deg": round(bearing, 1),
            "distance_nm": round(dist / units.NAUTICAL_MILE, 2),
        }
        said = []
        if chart is not None:
            # the chart in the captain's hands (package 33b; decision 30): the straight
            # line from the account checked against the charted dangers, the master's
            # warning and no more (the helm rules of the book have no guard, which is the
            # captain's business)
            passes = chart.line_passes(r.position, target, DANGER_PASS_NM * units.NAUTICAL_MILE)
            if feature is not None:
                passes = [p for p in passes if p[0].id != feature.id]
            crossed = [f.name for f, _off, crosses in passes if crosses]
            # package 37j: how near, to the cable, from the account as it stands (it was
            # "within a mile" for all)
            from freesail.world.geo import distance_words

            near = [
                f"{f.name} within "
                f"{distance_words(max(units.CABLE, off - float(getattr(f, 'extent_m', 0.0))))}"
                for f, off, crosses in passes
                if not crosses
            ]
            if crossed:
                said.append(f"the line crosses {_and(crossed)}")
            if near:
                said.append(f"the line passes {_and(near)}")
            data["dangers"] = [
                {"id": f.id, "name": f.name, "off_m": round(off), "crosses": crosses}
                for f, off, crosses in passes
            ]
            shore = self._line_shore(r.position, target, feature)
            if shore is not None:
                said.append(shore["words"])
                data["shore"] = shore
        if said:
            words += "; " + " and ".join(said)
        steer, allowing = self._make_good(line)
        words += "."
        if allowing["words"]:
            words += " " + allowing["words"]
        data["allowing"] = allowing
        return steer, words, data

    def _line_shore(
        self, start: Position, target: Position, feature: Any = None
    ) -> dict[str, Any] | None:
        """What a shaped course's line does with the land (package 37e): "the line crosses
        the land about Léon", "the line passes the shore under Petit Minou within two
        cables"; None when it keeps `SHORE_PASS_NM` clear. The first of the line is not
        tried for a near pass (she lies where she lies), and when the place is one of the
        chart's own that lies on the land (a town, a headland) the last
        `SHORE_AT_PLACE_NM` of it is not tried at all: a course for Falmouth ends at
        Falmouth. A point pricked on the chart is tried to its end: in game 9 a waypoint
        chosen against the shore "came back clear"."""
        from freesail.world.geo import distance_words

        chart = self.world.chart
        within = SHORE_PASS_NM * units.NAUTICAL_MILE
        skip_end = 0.0
        if feature is not None and chart.nearest_shore(target, within_m=1.5 * units.CABLE):
            skip_end = SHORE_AT_PLACE_NM * units.NAUTICAL_MILE
        found = chart.line_shore(start, target, within, skip_start_m=within, skip_end_m=skip_end)
        if found is None:
            return None
        distance_m, where, crosses = found
        coast = chart.coast_at(where)
        name = coast.name if coast is not None and coast.name else None
        if name is None:
            # no headland within a mile of the point: the nearest land the chart names
            # within two leagues ("the land about Léon")
            from freesail.world.chart import LAND_KINDS

            named = chart.nearby(where, 6.0 * units.NAUTICAL_MILE, LAND_KINDS)
            if named:
                name = min(named, key=lambda f: bearing_and_distance(where, f.position)[1]).name
        if crosses:
            words = (
                f"the line crosses the land about {name}" if name else "the line crosses the land"
            )
        else:
            off = distance_words(max(units.CABLE, distance_m))
            under = f" under {name}" if name else ""
            words = f"the line passes the shore{under} within {off}"
        return {
            "words": words,
            "crosses": crosses,
            "distance_m": round(distance_m),
            "name": name,
        }

    def _make_good(self, line: float) -> tuple[float, dict[str, Any]]:
        """The course to steer so that she makes good a line, by the master's reckoning
        (package 37e): the triangle of her way through the water and the tide he allows.
        Returns (the heading in radians, what he allowed in words and figures). With
        nothing to allow the heading is the line and the words are empty; with no way on
        there is no triangle to work, and he says so; when no course makes it good at her
        present way he says so and gives the course whose course made good lies nearest
        the line."""
        from freesail.world.tide import time_words

        tide = self.tide_allowed()
        out: dict[str, Any] = {
            "by": tide["by"],
            "knots": float(tide.get("knots") or 0.0),
            "words": "",
            "steer_deg": round(math.degrees(line) % 360.0, 1),
            "made_good": True,
        }
        knots = out["knots"]
        if knots < 0.5 * HOVE_TO_DRIFT_KN or "toward_deg" not in tide:
            return line, out  # nothing to allow: the words as they were
        toward = math.radians(float(tide["toward_deg"]))
        out["toward_deg"] = tide["toward_deg"]
        if tide["by"] == "captain":
            what = f"{rate_words(knots)} of set {ward_words(toward)} by the captain's order"
        else:
            flood = "flood" if tide.get("flood") else "ebb"
            what = f"the {flood}, {rate_words(knots)} to the {units.point_name(toward)}"
        way = self._way_to_shape_by_kn()
        out["way_kn"] = way
        if way < NO_WAY_KN:
            out["made_good"] = False
            out["words"] = (
                f"She has no way on to work an allowance by: {what} is not allowed for in the "
                f"course; shape it again when she has gathered way."
            )
            return line, out
        t_e, t_n = knots * math.sin(toward), knots * math.cos(toward)
        along = t_e * math.sin(line) + t_n * math.cos(line)
        cross = t_e * math.cos(line) - t_n * math.sin(line)  # to the right of the line
        if abs(cross) < way and math.sqrt(way * way - cross * cross) + along > 0.0:
            steer = line + math.asin(-cross / way)
        else:
            # no course holds the line: the one whose course made good lies nearest it
            out["made_good"] = False
            best: tuple[float, float, float] | None = None
            for k in range(720):
                h = math.radians(0.5 * k)
                g_e, g_n = way * math.sin(h) + t_e, way * math.cos(h) + t_n
                off = abs(units.wrap_pi(math.atan2(g_e, g_n) - line))
                gain = g_e * math.sin(line) + g_n * math.cos(line)
                if best is None or (off, -gain) < (best[0], best[1]):
                    best = (off, -gain, h)
            assert best is not None
            steer = best[2]
        # the leeway he allows when she lies close-hauled: her head so much to windward
        lee = ""
        dyn = getattr(self.world.ship, "dyn", None)
        wind_from = float(self.world.wind.direction_from)
        forward = units.rad_to_points(abs(units.wrap_pi(steer - wind_from)))
        if dyn is not None and self._close_hauled_now() and forward <= LEEWAY_ALLOWED_WITHIN_POINTS:
            leeway = float(dyn.leeway) + units.points_to_rad(self.errors.leeway_bias_points)
            quarters = round(units.rad_to_points(abs(leeway)) * 4.0)
            if quarters >= 1:
                steer -= leeway
                out["leeway_deg"] = round(math.degrees(leeway), 1)
                lee = f", {_points_words(quarters)} of leeway allowed"
        steer %= units.TWO_PI
        out["steer_deg"] = round(math.degrees(steer), 1)
        point = units.point_name(steer)
        if not out["made_good"]:
            out["words"] = (
                f"Allowing {what}, no course makes it good at her present way of "
                f"{knots_words(way)}; {point} loses least{lee}."
            )
            return steer, out
        holds = ""
        if tide["by"] == "book" and tide.get("turn"):
            turn = datetime.fromisoformat(str(tide["turn"]))
            holds = (
                "; the allowance holds till the tide turns, about "
                f"{time_words(turn.hour + turn.minute / 60.0)}"
            )
        out["words"] = f"Allowing {what}, steer {point} to make it good{lee}{holds}."
        return steer, out

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
        from freesail.world.geo import distance_words

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
                    # to the cable, from the account as it stands (package 37j; whole
                    # miles before, so that a ledge four cables off was "no distance")
                    "words": f"{f.name} {units.point_name(laid)}, "
                    f"{distance_words(max(units.CABLE, dist))}",
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

    def chart_depths_within_doubt(self) -> tuple[float, float]:
        """The least and the greatest depth the chart shows within what the master would
        trust the account within (`OBSERVATION_OUT_SIGMAS` of the doubt as it stands, the
        ellipse as it lies), at the account and on sixteen bearings at the half and the
        edge of it; the land counted as no water (package 37j, `the depth of water`). The
        account and its doubt only."""
        chart = self.world.chart
        here = self.account_now()
        e = self.doubt_now()
        a = OBSERVATION_OUT_SIGMAS * float(e["semi_major_nm"])
        b = OBSERVATION_OUT_SIGMAS * float(e["semi_minor_nm"])
        lie = math.radians(float(e["major_bearing_deg"]))
        depths = []
        points = [here]
        for k in range(16):
            t = 2.0 * math.pi * k / 16.0
            # a point on the ellipse: along its greater axis by cos, its lesser by sin
            along, across = a * math.cos(t), b * math.sin(t)
            de = along * math.sin(lie) + across * math.cos(lie)
            dn = along * math.cos(lie) - across * math.sin(lie)
            for part in (0.5, 1.0):
                points.append(_displaced(here, part * de, part * dn))
        for p in points:
            d = chart.depth_at(p)
            depths.append(0.0 if d is None else float(d))
        return min(depths), max(depths)

    def no_dangers_words(self) -> str:
        from freesail.world.chart import DANGERS_WITHIN_NM

        if self.world.chart is None:
            return "no chart of these waters"
        return f"no charted danger within {miles_words(DANGERS_WITHIN_NM)} of the account"

    # -- the captain's tide (package 34; spec M5 §16; T §2, §5) ---------------------------

    def almanac_age_days(self, when: datetime | None = None) -> float:
        """The moon's age from the almanac at the day's noon, to the quarter of a day (the
        almanac gives the hour of the change; the master reckons from it): the mean
        elements' arithmetic (`tide.moon_age_days`), which is the almanac's."""
        from freesail.world.sights import greenwich_time
        from freesail.world.tide import moon_age_days

        t = self.world.clock.ship_time if when is None else when
        noon = greenwich_time(self.world, t.replace(hour=12, minute=0, second=0))
        return round(moon_age_days(noon) * 4.0) / 4.0

    def tide_by_almanac(self, port_words: str | None = None) -> dict[str, Any]:
        """`the tide by the almanac`: high water today at the port named, or the nearest
        place of the epitome's table to the account, by Moore's rule of 48 minutes and
        the table's establishment; in the master's words, with the next high water from
        now. Never the world's tide."""
        from freesail.world.tide import time_words

        world = self.world
        table = self.epitome
        port = table.by_name(port_words) if port_words else None
        asked_for = port_words
        if port is None:
            port, distance_nm = table.nearest(self.account_now())
        else:
            distance_nm = 0.0
        day = world.clock.ship_time.date()
        age = self.almanac_age_days()
        times = table.high_waters(port, age, day)
        now = world.clock.ship_time
        upcoming = [t for t in times if t >= now]
        if not upcoming:
            later = table.high_waters(port, age + 1.0, day + timedelta(days=1))
            upcoming = [t for t in later if t >= now]
        said = [time_words(t.hour + t.minute / 60.0) for t in times]
        if len(said) == 2:
            when = f"{said[0]} and {said[1]}"
        elif said:
            when = said[0]
        else:
            when = "no high water falls within the day"
        head = f"High water at {port.name} about {when} by the epitome"
        if asked_for and _key(asked_for) != _key(port.name):
            head = (
                f"The epitome has no {asked_for}; the nearest place in the master's table is "
                f"{port.name}, {miles_words(distance_nm)} off: high water there about {when}"
            )
        elif distance_nm > 5.0 and not asked_for:
            head = (
                f"High water at {port.name}, the nearest place in the master's table "
                f"({miles_words(distance_nm)} off), about {when} by the epitome"
            )
        age_words = f"the moon {_age_words(age)} old"
        table_words = f"{port.name} {port.establishment_words} at full and change"
        next_words = (
            time_words(upcoming[0].hour + upcoming[0].minute / 60.0)
            if upcoming
            else "the next tide"
        )
        if upcoming and upcoming[0].date() != day:
            next_words += " tomorrow"
        rise = ""
        if port.spring_rise_ft is not None:
            rise = f"; the rise {port.spring_rise_ft:g} feet at springs"
        words = f"{head} ({table_words}, {age_words}{rise})"
        return {
            "port": port.name,
            "words": words,
            "times": [t.isoformat() for t in times],
            "next": upcoming[0].isoformat() if upcoming else None,
            "next_words": next_words,
            "establishment_h": port.establishment_h,
            "age_days": age,
            "table": table.table,
            "spring_rise_ft": port.spring_rise_ft,
        }

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
        obs = r.observe_longitude(sight.longitude_deg, sight.sigma_nm)
        self._moved()
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
            f"trust it within {miles_words(trust)}{_beside_words(obs)}: "
            f"{verdict_words(obs, what='the sight')}."
        )
        data = {
            "sight": sight.to_dict(),
            "reckoning": r.words,
            "how": obs.how,
            "moved_nm": round(obs.moved_nm, 2),
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
        # by the one rule (package 37e): in game 9 a lunar "which he would trust within 25
        # miles" replaced an account he trusted within two; weighed, it moves such an
        # account a cable or two, and is taken only when the account is plainly out
        obs = r.observe_longitude(lunar.longitude_deg, lunar.sigma_nm)
        self._moved()
        of = lunar.body
        master = self.master.name
        text = (
            f"A set of distances of {of} and the moon taken by {master} and two of the young "
            f"gentlemen, and cleared: longitude by lunar {lunar.words}, which he would trust "
            f"{lunar.trust_words}{_beside_words(obs)}; the reckoning was "
            f"{_lon_words(account_lon)}: {verdict_words(obs, 'the lunar')}."
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
            "how": obs.how,
            "moved_nm": round(obs.moved_nm, 2),
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
        lat = self.reckoning.lat_deg  # his latitude by account (package 37j: no truth)
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
        # the doubt as it stands now, and the tide the master allows (package 37e)
        doubt = self.doubt_now()
        out["uncertainty"] = doubt["words"]
        out["ellipse"] = {k: v for k, v in doubt.items() if k != "words"}
        out["tide"] = self.tide_allowed()
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
        run = r.run_since_noon_nm + self._run_since_step_nm()
        return run, (None if dist < 0.1 * units.NAUTICAL_MILE else bearing)

    def _run_since_step_nm(self) -> float:
        """The distance made by account since the last working: the run, her drift hove
        to and the tide allowed, as the next working will enter them."""
        w = self._working()
        if w is None:
            return 0.0
        run = max(0.0, w.read) * w.run_h
        de = run * math.sin(w.course) + w.drift[0] + w.tide[0]
        dn = run * math.cos(w.course) + w.drift[1] + w.tide[1]
        return math.hypot(de, dn)

    def no_noon_words(self) -> str:
        if self.noon_had:
            return "no distance made good since noon"
        r = self.reckoning
        run = r.run_since_noon_nm + self._run_since_step_nm()
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
        """`the reckoning`: the account brought up to now, in degrees and in words, and
        the tide the master allows in it (package 37e: "he says what he allows", so that
        the captain can see it and overrule it)."""
        now = self.account_now()
        tide = self.tide_allowed()
        position = f"{format_position(now)} by account"
        return {
            "lat_deg": now.lat_deg,
            "lon_deg": now.lon_deg,
            "words": f"{position}; the tide allowed: {tide['words']}",
            "position": position,
            "tide": tide,
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


def _age_words(age_days: float) -> str:
    """'fifteen days', 'seven days and a half': the moon's age in the master's words."""
    whole = int(age_days)
    quarter = age_days - whole
    words = f"{number_words(whole)} day{'s' if whole != 1 else ''}" if whole else "under a day"
    if abs(quarter - 0.5) < 0.01:
        words += " and a half"
    elif abs(quarter - 0.25) < 0.01:
        words += " and a quarter"
    elif abs(quarter - 0.75) < 0.01:
        words += " and three quarters"
    return words


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


def _drift_through_water(ship: Any) -> tuple[float, float]:
    """Her motion through the water, metres a second east and north, as the master's eye
    has it hove to: her way ahead or astern and her drive to leeward together."""
    dyn = getattr(ship, "dyn", None)
    if dyn is None:
        return 0.0, 0.0
    heading = float(dyn.heading)
    u, v = float(dyn.u), float(dyn.v)
    return (
        u * math.sin(heading) + v * math.cos(heading),
        u * math.cos(heading) - v * math.sin(heading),
    )


def _allowed(part: float) -> float:
    """The mate's allowance for her way over an interval, as a part of the log's read."""
    return min(WAY_ALLOWANCE_MOST, max(WAY_ALLOWANCE_LEAST, part))


def _offset_from(lat_deg: float, lon_deg: float, other: Position) -> tuple[float, float]:
    """Miles east and north from a place to `other`, as `Reckoning.offset_nm` lays them."""
    de = (other.lon_deg - lon_deg) * _NM_PER_DEG * math.cos(math.radians(lat_deg))
    dn = (other.lat_deg - lat_deg) * _NM_PER_DEG
    return de, dn


def _displaced(pos: Position, de: float, dn: float) -> Position:
    """A position so many miles east and north of another, as the traverse lays it."""
    lat = pos.lat_deg + dn / _NM_PER_DEG
    scale = math.cos(math.radians(lat))
    lon = pos.lon_deg + (de / (_NM_PER_DEG * scale) if abs(scale) > 1e-9 else 0.0)
    return Position(lat, ((lon + 180.0) % 360.0) - 180.0)


def _with(used: tuple[str, ...], who: str) -> tuple[str, ...]:
    return used if who in used else used + (who,)


def _port_cache(nav: Any) -> dict[Any, Any]:
    if nav._ports is None:
        nav._ports = {}
    return nav._ports


def _high_water_cache(nav: Any) -> dict[Any, Any]:
    if nav._highs is None:
        nav._highs = {}
    return nav._highs


@dataclass(frozen=True)
class BookTide:
    """The master's own tide at a place and a moment (package 37e): the water his
    directions name, the place of his epitome whose high water he reckons from, the
    stream's rate at its strength this tide (between the book's neaps and springs by the
    moon's age), the rate now along the flood's set (negative on the ebb), and that high
    water by his clock."""

    area: Any  # tide.BookStream
    port: Any  # tide.EpitomePort
    rate_kn: float
    along_kn: float
    high_water: datetime | None

    @property
    def flood(self) -> bool:
        return self.along_kn >= 0.0

    @property
    def toward_rad(self) -> float:
        set_rad = float(self.area.set_rad)
        return set_rad % units.TWO_PI if self.flood else (set_rad + math.pi) % units.TWO_PI

    @property
    def words(self) -> str:
        """'the flood, a knot and a half to the E by N'."""
        tide = "flood" if self.flood else "ebb"
        return (
            f"the {tide}, {rate_words(abs(self.along_kn))} to the "
            f"{units.point_name(self.toward_rad)}"
        )

    def _hours(self, when: datetime) -> float | None:
        if self.high_water is None:
            return None
        hours = (when - self.high_water).total_seconds() / 3600.0
        return hours - float(self.area.strongest_h)

    def making_flood(self, when: datetime) -> bool:
        """Whether the flood is the tide that runs or, at slack water, is to make."""
        hours = self._hours(when)
        if hours is None or abs(self.along_kn) >= 0.5 * HOVE_TO_DRIFT_KN:
            return self.flood
        # at slack: the flood makes when the half-cosine is rising
        return math.sin(2.0 * math.pi * hours / TIDE_HOURS) < 0.0

    def next_turn(self, when: datetime) -> datetime | None:
        """When his tide next turns: the half-cosine's next nought after `when`."""
        hours = self._hours(when)
        if hours is None:
            return None
        quarter = TIDE_HOURS / 4.0
        k = math.floor((hours - quarter) / (TIDE_HOURS / 2.0)) + 1
        return when + timedelta(hours=quarter + k * TIDE_HOURS / 2.0 - hours)


@dataclass(frozen=True)
class Working:
    """One interval of the traverse as the master would work it (package 37e): the hours
    she had way on, the course and the way for them and the read's doubt, whether she
    lay close-hauled, the hours of the clock she was not riding, the hours hove to, her
    drift for them and the tide he allows (miles east and north each), and the stream
    his directions give, for his doubt of it."""

    run_h: float
    course: float
    read: float
    read_sigma: float
    close_hauled: bool
    clock_h: float
    hove_h: float
    drift: tuple[float, float]
    tide: tuple[float, float]
    stream: tuple[str, float, float, float] | None


def rate_words(knots: float) -> str:
    """A stream's rate in the master's words: 'a knot and a half', 'half a knot', 'two
    knots', 'a quarter of a knot'; 'nothing' for none."""
    words = knots_words(knots)
    if words == "no way":
        return "nothing"
    return "a knot" + words[len("one knot") :] if words.startswith("one knot") else words


_WARD = {
    0: "northward",
    4: "north-eastward",
    8: "eastward",
    12: "south-eastward",
    16: "southward",
    20: "south-westward",
    24: "westward",
    28: "north-westward",
}


def ward_words(toward_rad: float) -> str:
    """'to the westward', 'to the north-eastward' for the eight principal points; 'to the
    W by S' for the rest."""
    index = units.nearest_point_index(toward_rad)
    if index in _WARD:
        return f"to the {_WARD[index]}"
    return f"to the {units.point_name(toward_rad)}"


def _points_words(quarters: int) -> str:
    """'a quarter of a point', 'half a point', 'a point and a quarter'."""
    whole, q = divmod(int(quarters), 4)
    frac = {1: "a quarter", 2: "a half", 3: "three quarters"}.get(q, "")
    if whole == 0:
        return {1: "a quarter of a point", 2: "half a point", 3: "three quarters of a point"}[q]
    words = "a point" if whole == 1 else f"{number_words(whole)} points"
    return f"{words} and {frac}" if frac else words


def _water_words(name: str) -> str:
    """A water of the directions as the log says it after 'she is in': 'the Iroise',
    'the open Channel', 'the waters off the Lizard', 'Carrick Road'."""
    if name.startswith(("off ", "between ", "round ")):
        return f"the waters {name}"
    return name


def _carried_words(used: tuple[str, ...], ordered: tuple[float, float] | None) -> str:
    """Whose tide the day's work carried, as the noon line's last sentence (package 37e):
    the master's own by his directions and epitome, the captain's set, both, or none."""
    parts = []
    if "book" in used:
        parts.append("the master's tide by the directions and the epitome")
    if "captain" in used:
        if ordered is not None and ordered[0] > 0.0:
            parts.append(f"the captain's set of {rate_words(ordered[0])} {ward_words(ordered[1])}")
        else:
            parts.append("the captain's word for the set")
    if not parts:
        if "none" in used:
            return " No tide in the day's work: the directions give none for these waters."
        return ""
    return f" The day's work carried {_and(parts)}."


def _beside_words(obs: Observation) -> str:
    """', and the account within two miles': the account's own doubt set beside an
    observation's, when the observation is the poorer figure and the account was kept
    (the lunar of game 9: "which he would trust within 25 miles, and the account within
    two: the account kept")."""
    if obs.how == KEPT and obs.poorer and not obs.doubted:
        return f", and the account {trust_words(obs.account_sigma_nm)}"
    return ""


def _bearing_sigma_nm(distance_m: float, allowance_deg: float = 0.0) -> float:
    """The doubt across a bearing's line at the mark's distance: a degree and a half at
    ten miles is a quarter of a mile (N §3); with what the master allows for the compass's
    own error (package 37e, `COMPASS_ALLOWANCE_DEG`), the two together."""
    both = math.hypot(BEARING_SIGMA_DEG, allowance_deg)
    return max(0.05, distance_m / units.NAUTICAL_MILE * math.tan(math.radians(both)))


def _cut_deg(a: Any, b: Any) -> float:
    """The angle two marks' lines of bearing cut at, 0 to 90 degrees (a line and its
    reciprocal are one line)."""
    d = abs(a.bearing_deg - b.bearing_deg) % 180.0
    return min(d, 180.0 - d)


def _least_cut_deg(marks: list[Any]) -> float:
    return min(_cut_deg(a, b) for i, a in enumerate(marks) for b in marks[i + 1 :])


def _best_cut_deg(marks: list[Any]) -> float:
    return max(_cut_deg(a, b) for i, a in enumerate(marks) for b in marks[i + 1 :])


def _fix_doubt_nm(marks: tuple[Any, ...] | list[Any], allowance_deg: float) -> float:
    """How good a fix by these marks would be, before it is taken: the greater axis of
    its doubt in miles, from each line's doubt across it at its mark's distance by
    estimation (`BEARING_SIGMA_DEG`) and the compass's own error, which the lines share
    and which moves the whole fix (`allowance_deg`). With three marks it is no smaller
    than half the cocked hat he must expect, which is as large as the farthest line's
    own doubt (the lines of a fix swing about their marks by the compass's error and
    miss one another by the far mark's swing). The lookout's bearings and distances by
    estimation are all it reads."""
    a00 = a01 = a11 = g0 = g1 = 0.0
    farthest = 0.0
    for s in marks:
        away = max(0.1, float(s.judged_m) / units.NAUTICAL_MILE)
        farthest = max(farthest, away)
        sigma = max(0.05, away * math.tan(math.radians(BEARING_SIGMA_DEG)))
        w = 1.0 / (sigma * sigma)
        bearing = math.radians(s.bearing_deg)
        n_e, n_n = math.cos(bearing), -math.sin(bearing)
        a00 += w * n_e * n_e
        a01 += w * n_e * n_n
        a11 += w * n_n * n_n
        # a turn of the compass swings each line about its mark: her place on it moves
        # the mark's distance times the turn, across the line
        g0 += w * away * n_e
        g1 += w * away * n_n
    det = a00 * a11 - a01 * a01
    if det <= 1e-12:
        return math.inf
    c00, c01, c11 = a11 / det, -a01 / det, a00 / det
    turn = math.radians(allowance_deg)
    s_e, s_n = (c00 * g0 + c01 * g1) * turn, (c01 * g0 + c11 * g1) * turn
    cov = [[c00 + s_e * s_e, c01 + s_e * s_n], [c01 + s_e * s_n, c11 + s_n * s_n]]
    doubt = math.sqrt(max(0.0, _greatest_eigen(cov)))
    if len(marks) >= 3:
        hat = farthest * math.tan(math.radians(math.hypot(BEARING_SIGMA_DEG, allowance_deg)))
        doubt = max(doubt, 0.5 * hat)
    return doubt


def _choose_marks(marks: list[Any], allowance_deg: float = COMPASS_ALLOWANCE_DEG) -> list[Any]:
    """The two or three marks whose fix has the least doubt (package 37e; until then the
    three that cut at the widest angles, nearness only breaking ties, so that in game 9
    fixes were worked by towns three to seven miles off with a headland inside a mile):
    among the pairs and the threes of which some two lines cut by `FIX_MIN_CUT_DEG` or
    more, the set with the least `_fix_doubt_nm`; on a tie the nearer marks. None when
    no two cut by that much. The marks come nearest first and are returned so."""
    from itertools import combinations

    best: tuple[float, float, tuple[Any, ...]] | None = None
    for size in (3, 2):
        for group in combinations(marks, size):
            if _best_cut_deg(list(group)) < FIX_MIN_CUT_DEG:
                continue
            key = (round(_fix_doubt_nm(group, allowance_deg), 4), sum(s.judged_m for s in group))
            if best is None or key < best[:2]:
                best = (key[0], key[1], group)
    return list(best[2]) if best is not None else []


def _too_fine_words(marks: list[Any]) -> str:
    """The refusal for marks that cut too fine, naming them and how they bear from one
    another, with the cure."""
    a, b = max(
        ((x, y) for i, x in enumerate(marks) for y in marks[i + 1 :]),
        key=lambda pair: _cut_deg(*pair),
    )
    cut = max(1, int(_cut_deg(a, b)))
    apart = "a degree" if cut == 1 else f"{cut} degrees"
    return (
        f"{_head(a.feature.name)} and {b.feature.name} cut too fine for a fix: they bear "
        f"{units.point_name(math.radians(a.bearing_deg))} and "
        f"{units.point_name(math.radians(b.bearing_deg))}, their lines within "
        f"{apart} of one another, and a fix wants "
        f"{FIX_MIN_CUT_DEG:.0f}. Take a bearing of one for a line, or wait for a mark that "
        f"cuts better."
    )


def _least_eigen(cov: list[list[float]]) -> float:
    mean = 0.5 * (cov[0][0] + cov[1][1])
    diff = 0.5 * (cov[0][0] - cov[1][1])
    return mean - math.sqrt(diff * diff + cov[0][1] * cov[0][1])


def _greatest_eigen(cov: list[list[float]]) -> float:
    mean = 0.5 * (cov[0][0] + cov[1][1])
    diff = 0.5 * (cov[0][0] - cov[1][1])
    return mean + math.sqrt(diff * diff + cov[0][1] * cov[0][1])


def _fix_of(
    start: Position, lines: list[tuple[Any, float]], allowance_deg: float = 0.0
) -> tuple[Position, list[list[float]], float | None]:
    """The point that best fits the lines of bearing (each a sighting and the bearing
    laid down, radians), each weighed by its own doubt across it at the mark's distance
    (`_bearing_sigma_nm`): weighted least squares on the flat about the point, worked
    again from each answer until it stands (the flat is true only near the point, and an
    account ten miles out is not near). Returns the fix, its covariance in square miles
    (east, north), and with three lines the cocked hat's size in metres: the longest
    side of the triangle their crossings make, the crossings of lines that cut by less
    than a fix's cut left out.

    The covariance counts what the master allows for the compass's own error
    (`allowance_deg`, package 37e): every line of a fix carries it alike, so it does not
    show in the cocked hat and moves the whole fix, by each mark's distance times the
    turn; a tight hat by far marks is not a good fix, and "good to" must say so."""
    p = start
    cov = [[1.0, 0.0], [0.0, 1.0]]
    first = True
    for _ in range(8):
        a00 = a01 = a11 = b0 = b1 = g0 = g1 = 0.0
        for s, laid in lines:
            dx, dy = p.offset_to(s.feature.position)
            # the doubt across the line at the mark's distance: by the lookout's estimate
            # for the first working, then by the distance the fix itself gives
            away = s.judged_m if first else math.hypot(dx, dy)
            sigma = _bearing_sigma_nm(away) * units.NAUTICAL_MILE
            w = 1.0 / (sigma * sigma)
            n_e, n_n = math.cos(laid), -math.sin(laid)
            z = n_e * dx + n_n * dy  # how far the line lies from the point, across it
            a00 += w * n_e * n_e
            a01 += w * n_e * n_n
            a11 += w * n_n * n_n
            b0 += w * n_e * z
            b1 += w * n_n * z
            g0 += w * away * n_e
            g1 += w * away * n_n
        det = a00 * a11 - a01 * a01
        if abs(det) < 1e-18:
            break
        de = (a11 * b0 - a01 * b1) / det
        dn = (a00 * b1 - a01 * b0) / det
        p = p.advanced(de, dn)
        nm2 = units.NAUTICAL_MILE**2
        cov = [[a11 / det / nm2, -a01 / det / nm2], [-a01 / det / nm2, a00 / det / nm2]]
        if allowance_deg > 0.0:
            turn = math.radians(allowance_deg) / units.NAUTICAL_MILE
            s_e = (a11 * g0 - a01 * g1) / det * turn
            s_n = (a00 * g1 - a01 * g0) / det * turn
            cov = [
                [cov[0][0] + s_e * s_e, cov[0][1] + s_e * s_n],
                [cov[1][0] + s_e * s_n, cov[1][1] + s_n * s_n],
            ]
        if not first and math.hypot(de, dn) < 1.0:
            break
        first = False
    hat = None
    if len(lines) == 3:
        corners = []
        for i in range(3):
            for j in range(i + 1, 3):
                (sa, la), (sb, lb) = lines[i], lines[j]
                cut = abs(math.degrees(la - lb)) % 180.0
                if min(cut, 180.0 - cut) < FIX_MIN_CUT_DEG:
                    continue
                ax, ay = p.offset_to(sa.feature.position)
                bx, by = p.offset_to(sb.feature.position)
                # the crossing of the two lines, each through its mark along its bearing
                ta = (math.sin(la), math.cos(la))
                tb = (math.sin(lb), math.cos(lb))
                den = ta[0] * tb[1] - ta[1] * tb[0]
                if abs(den) < 1e-9:
                    continue
                k = ((bx - ax) * tb[1] - (by - ay) * tb[0]) / den
                corners.append((ax + k * ta[0], ay + k * ta[1]))
        if len(corners) >= 2:
            hat = max(
                math.hypot(c[0] - d[0], c[1] - d[1])
                for i, c in enumerate(corners)
                for d in corners[i + 1 :]
            )
        else:
            # two of the three lines all but one line: the hat is how far the third
            # crossing stands from the fix, twice over
            hat = 2.0 * max(math.hypot(c[0], c[1]) for c in corners) if corners else 0.0
    return p, cov, hat


# Marks all on one hand (package 37j): the bearings of a fix's marks lie within this arc
# of the compass, six points and a half (JUDGEMENT; in the Bay of Brest the three marks of 37e's
# finding bore from W by N to N by W, and off the Lizard in game 10 from NW to N by W).
ONE_HAND_DEG = 73.125


def _one_hand(lines: list[tuple[Any, float]]) -> float | None:
    """The mean bearing of a fix's marks (radians, toward them) when they lie all on one
    hand (`ONE_HAND_DEG`), else None."""
    bearings = sorted(laid % units.TWO_PI for _s, laid in lines)
    if len(bearings) < 2:
        return None
    gaps = [b - a for a, b in zip(bearings, bearings[1:], strict=False)]
    gaps.append(bearings[0] + units.TWO_PI - bearings[-1])
    span = units.TWO_PI - max(gaps)  # the least arc that holds them all
    if span > math.radians(ONE_HAND_DEG):
        return None
    e = sum(math.sin(b) for b in bearings)
    n = sum(math.cos(b) for b in bearings)
    return math.atan2(e, n)


def _along_and_off_nm(cov: list[list[float]], toward: float) -> tuple[float, float]:
    """A fix's doubt along the shore (square to the mean bearing of its marks) and off
    it (along that bearing), in miles."""
    r = (math.sin(toward), math.cos(toward))
    t = (r[1], -r[0])

    def sigma(v: tuple[float, float]) -> float:
        q = v[0] * (cov[0][0] * v[0] + cov[0][1] * v[1]) + v[1] * (
            cov[1][0] * v[0] + cov[1][1] * v[1]
        )
        return math.sqrt(max(0.0, q))

    return sigma(t), sigma(r)


def _compass_shift_nm(
    fix: Position, lines: list[tuple[Any, float]], allowance_deg: float
) -> tuple[float, float]:
    """How far a turn of the compass by `allowance_deg` moves a fix by these lines, miles
    east and north: each line swings about its mark by the mark's distance times the
    turn, and the fix by the weighted sum (the same arithmetic as `_fix_of`'s compass
    term). Large when the marks lie on one hand, nothing when they lie all round."""
    a00 = a01 = a11 = g0 = g1 = 0.0
    for s, laid in lines:
        away = bearing_and_distance(fix, s.feature.position)[1]
        sigma = _bearing_sigma_nm(away) * units.NAUTICAL_MILE
        w = 1.0 / (sigma * sigma)
        n_e, n_n = math.cos(laid), -math.sin(laid)
        a00 += w * n_e * n_e
        a01 += w * n_e * n_n
        a11 += w * n_n * n_n
        g0 += w * away * n_e
        g1 += w * away * n_n
    det = a00 * a11 - a01 * a01
    if abs(det) < 1e-18:
        return 0.0, 0.0
    turn = math.radians(allowance_deg) / units.NAUTICAL_MILE
    return (a11 * g0 - a01 * g1) / det * turn, (a00 * g1 - a01 * g0) / det * turn


def _tick_of(world: Any, when: datetime) -> int:
    return int((when - world.clock.start).total_seconds())


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


def _key(name: str) -> str:
    words = name_words(name)
    if words and words[0] == "the":
        words = words[1:]
    return " ".join(words)


def _lat_words(lat_deg: float) -> str:
    return format_position(Position(lat_deg, 0.0)).split(",")[0]


def _lon_words(lon_deg: float) -> str:
    return format_position(Position(0.0, lon_deg)).split(", ")[1]
