# Code reader 01: the sea, the sky and navigation

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read under READERS.md and CODEREADERS.md: nothing
under docs/dev, docs/design, docs/playtests or docs/gates opened; no test run; nothing changed
but this file. Commands run were greps, `wc`, an AST count of lines and functions, and three
short Python calls (named where used).

## 1. What it is

**Size.** Thirteen modules, 15,691 lines:

| module | lines | what it is |
|---|---|---|
| freesail/world/reckoning.py | 6,126 | the captain's dead reckoning and everything the master does |
| freesail/world/chart.py | 1,934 | the depth tiles, the coast, the features, sightings |
| freesail/world/weather.py | 1,674 | pressure systems, fronts, sky, glass, sea breeze, fog |
| freesail/world/movement.py | 1,276 | people moving about the ship, ashore, between hulls |
| freesail/world/tide.py | 1,152 | the world's harmonic tide, and the master's epitome and directions |
| freesail/world/water.py | 952 | water in the hull, pumps, foundering |
| freesail/world/sights.py | 801 | noon sight, chronometer, time sight, lunar, amplitude/azimuth |
| freesail/world/ground.py | 470 | grounding, kedging off, sounding the well |
| freesail/world/sea.py | 380 | wind sea and swell, its words |
| freesail/world/geo.py | 294 | Position, haversine, horizon, distance words |
| freesail/core/sun.py | 234 | NOAA/Spencer sun: daylight, transit |
| freesail/core/moon.py | 219 | Meeus low-precision moon (and a second sun) |
| freesail/world/weather_script.py | 179 | a scenario's pinned wind timeline |

Three of the eleven world modules named in my brief are not sea, sky or navigation:
`water.py` (hull flooding and pumps), `ground.py` (grounding consequences and the well) and
`movement.py` (people, places, visitors, captives, model and player seats). They are read and
reported, but they belong to the ship and the people.

**What it does in the game.** The world keeps a true position (`core/world.py:1548`
`_tick_geo`, the plane metres of the physics turned into latitude and longitude each tick). Beside
it `Navigation` (reckoning.py:2024) keeps the master's account: a position with a 2x2 covariance
(`Reckoning`, reckoning.py:952) advanced at each heave of the log from a "traverse board" pegged
every tick (`_peg`, :2233), with seeded biases the master cannot know (`CompassErrors`, :777:
log-line marked short, deviation, leeway bias, a decade-old variation) and doubts he does
(steering, the read, set, stream, compass). Each observation (cast, bearing, transit, fix by cross
bearings, noon latitude, time sight, lunar) is applied by one Kalman-style rule with three
outcomes, "taken", "weighed", "kept" (`observe_line` :1298, `observe_point` :1414). The master works
his own tide from an 1805 epitome and sailing directions (`book_tide` :2402) and never reads the
world's tide; he shapes courses against it (`shape_for` :4586, `_make_good` :4704), keeps a slate
for officers' own reckonings (:4135), and hands a "working" to whoever holds the master's station,
a model or the player (:3917 to :4069). The chart (`chart.py`) answers depth, grounding, nearest
shore, coast trend, what is in sight (with Allard's law for lights, :258) and dangers on a line.
The tide (`tide.py`) is M2, S2 and N2 at 100 gauges (11 global, 89 tied to chart blocks) blended by
inverse distance, with a seam taper, and stream areas; the World evaluates it once a minute. The
weather (`weather.py`) is Gaussian pressure systems on a flat km plane about the start, seeded from
13 climatology boxes, giving the wind each tick and sky/visibility once a minute. The sea
(`sea.py`) is a lagged Pierson-Moskowitz height plus a decayed swell, deterministic.

**What the player sees.** Log lines in period words: "Hove the log: six knots and a half.", the
leadsman's chant, "Noon. Latitude by observation ...", "the reckoning was out by it; laid down by
the fix", "I would not trust the reckoning within twenty miles east or west ...", tide-turn
lines, "Shaped a course for ...; the line passes the Manacles within two cables", lunar and
chronometer lines; readings such as `the reckoning`, `the dangers`, `the tide by the almanac`,
`the depth of water`; the browser chart's ellipse and track by account (`Navigation.to_dict`
:5418), never the truth.

**Callers.** The World makes one `Navigation` per world with a position (core/world.py:950-959)
and ticks it every tick (core/world.py:2416). Orders reach it through `freesail/orders/navigation.py`
(47 references), readings through `freesail/api/readings.py` (39), and the rules captain
(`world/captains.py`, 21), dealings (9), crews (6) and others.

**Tests.** Dedicated files: tests/test_reckoning.py 2,765 lines (74 tests), test_chart.py 2,421
(60), test_tide.py 1,369 (32), test_weather.py 1,002 (31), test_sea.py 730 (23),
test_weather_script.py 403, test_ground.py 411 (10), test_water.py 317 (11), test_geo.py 298,
test_chart_audit.py 294, test_sun.py 229, test_sights.py 182 (7), test_moon.py 103. The reckoning
is also imported by test_longitude.py (711), test_wardroom_doors.py (879) and
test_known_truths.py (17,391 lines, one file).

**The data.**
- data/tides: constituents.yaml 1,326 lines (100 gauges, only M2/S2/N2; 31 with no mean level),
  establishments.yaml 321 (Norie 111 ports, Moore 23; 55 rises marked judgement), streams.yaml
  1,659 (82 areas, each with a world statement and a `book:` statement; all 82 book statements
  carry a `judgement` list).
- data/weather/climatology.yaml: 3,637 lines, 13 boxes, every one `provisional: true`.
- data/charts, 359 MB, 2,398 files: `tiles/1` 54 files 11 MB (the level-1 30" GEBCO corridor and
  `atlantic-south`), `tiles/2` 1,587 files 288 MB (3" regional, EMODnet), `tiles/3` 684 files
  53 MB (0.5" harbour patches); `coast/` 20 GeoJSON 5.7 MB; `features/` 20 YAML plus 20 index JSON
  1.6 MB; `overrides/` 10 period-polygon YAMLs; `manifest.yaml` 398 KB, 14,520 lines;
  `audit-known.yaml`, `unverified-checks.yaml`. Levels 0 (world) and the "atlantic" level 1 are
  named in the manifest but not committed (their tile lists are empty).

## 2. The charts: how made, how loaded, what the repository carries

**Made** by tools/build_charts.py (3,099 lines; read the docstring and skimmed its structure):
fetches GEBCO 2025 (extract API and CEDA GeoTIFFs), EMODnet DTM 2024 (ERDDAP netCDF) and French
sources into `.cache/charts`, resamples with numpy only (own readers for ESRI ASCII, netCDF
classic and TIFF, :1172-:1407), rasterises period overrides, derives a chamfer distance field
(:1521), per-tile and per-block minimum depth, a 0.25-degree feature index, coast polylines, and
writes `tiles/<level>/<south_sec>_<west_sec>.npz` with int16 elevation (decimetres at levels 2
and 3), optionally horizontally differenced (`predictor` 2, :1501-:1507), uint16 `dist`. The
manifest records every source, licence, checksum and the tile lists. tools/chart_manifest.py
(99 lines) only prints the manifest.

**Loaded** by `chart.load_chart` (chart.py:893) into a module-level cache `_CHARTS` (:890),
shared by every World in the process. `Chart.__init__` (:945, 168 lines, the longest function
of the module) parses the manifest with the pure-Python `yaml.safe_load` (:884), builds `Level`
objects whose tiles are `np.load`ed on demand into a 16-tile cache per level (:693-:711), undoes
the differencing with a uint16 cumsum (:560-:564), and fills NODATA from "beside" layers
(`Tile.filled_from` :593). `tide.region_bounds` and `tide.charted_bounds` (tide.py:806, :828)
each parse the same 398 KB manifest again with the C loader. Measured: `yaml.safe_load` of the
manifest 0.76 s, `CSafeLoader` 0.10 s, so about a second of start-up goes on reading one file
three times (low; sure).

**What the repository carries.** The tiles are committed as plain git blobs; .gitattributes has
no LFS, only `text=auto` and a note that git detects the tiles as binary. This checkout is
shallow (430 commits), and its pack is already 427 MiB; within those 430 commits the tiles were
rewritten in 9 commits and the manifest in 18. Every rebuild of a region adds its megabytes to
history for good, and every clone takes all of it (medium; sure on the facts, the growth rate
is an inference from the 9 commits).

## 3. Why is reckoning.py six thousand lines, and is all of it navigation?

It is three things in one file: a 870-line estimator (`Reckoning`, :952-:1820, 41 methods), a
3,528-line `Navigation` class (:2024-:5551, 115 methods) and 570 lines of helpers. By AST count
the file is 4,267 code lines, 729 docstring lines and 664 comment lines (23 per cent), and the
text names "package NN", "game N", "the owner" or "gate" 197 times. Laid out by what each stretch
does:

| lines | what | navigation? |
|---|---|---|
| 1-180 | module essay and `__all__` | |
| 182-617 | 60-odd constants, most with a paragraph of provenance and history | yes |
| 620-770 | `number_words`, `knots_words`, `miles_words`, `age_words`, `chant`, ground words | partly: `number_words` is the game's general number speller (imported by evolutions/scripts.py five times, world/ordnance.py, world/sights.py, core/world.py:2797, api/readings.py); `rate_words`/`ward_words` are imported by dealings.py and captains.py |
| 952-1937 | the estimator, the slate, doubt words | yes |
| 1945-1995 | `Master` | yes |
| 2024-2580 | state, tick, traverse board, the master's tide | yes |
| 2580-2885 | the traverse worked (four near copies, see 4.2) | yes |
| 2886-3253 | log and lead | yes |
| 3254-3744 | bearings, transits, fix by cross bearings | yes |
| 3745-3914 | noon and day's work | yes |
| 3915-4080 | the master's station's "working" for a model or the player's seat | no: agent hand-off |
| 4081-4427 | slate, officers' own reckonings keyed by harness seatings and seats | half: the arithmetic is navigation, the holder bookkeeping (`_holder_of` :4372, `_owns` :4387) is agent/seat management |
| 4469-4557 | "the way by marks": a waypoint autopilot that calls `world.submit(...)` (:4542) | no: an order-issuing behaviour living in the estimator's module |
| 4558-4946 | shape a course, chart queries | yes |
| 4947-5278 | almanac tide, chronometer, lunar, variation | yes |
| 5279-5552 | about 25 `*_reading` and `no_*_words` methods | no: reading formatting for api/readings.py |
| 5554-6126 | helpers: fix least squares, BookTide, words | mostly |

So roughly 800 to 1,000 lines are not navigation (agent and seat hand-off, an autopilot, the
game's English number words, reading formatting), and the navigation that remains is long
because every behaviour is written as long prose-commented methods with backward-compatibility
shims (class-level defaults "for a checkpoint from before package 37e/37j/40b/41/45", ten such
mentions, and `_run_n is None` migration code in `_peg`, :2243-:2248). It imports 57 modules
inside functions, 13 of them `OrderError` from `freesail.evolutions.runner`, which is the same
class as `freesail.ship.stub.OrderError` and `freesail.orders.errors.OrderError` (three import
routes to one class).

## 4. Built more than once

**4.1 Number and word spellers.** `reckoning.number_words` (:649, to 199, then digits) beside
`crew/model.py:177` (a table), `agents/agent.py:2236` (a dict), `world/people.py:1757` (to 99),
`combat/guns.py:1184` `count_words` (to 60), `geo._count_words` (:239, to 12, then digits),
`chart.fathoms_words`'s own table (:235, to 12), `ground._SMALL` (:412, to 11, with "an").
They disagree today: `chart.fathoms_words` says "13 fathoms" and "dry at the datum" where
`reckoning.fathoms_said` (:703) says "thirteen fathoms" and "no water", and both reach the
player (the grounding line, chart.py:512; the cast line, reckoning.py:3096). `miles_words` exists
twice with different rules (reckoning.py:681 whole miles; agents/tripwires.py:342 cables and
half miles). `_seconds_words` (reckoning.py:5565) beside `combat/guns.seconds_words` and
`agents/mcp_server._seconds_words`. `_head`/`_cap`/`_and` are defined in about 25 modules
(grep `def _head|def _cap|def _and`). Joining: one `words` module; the cost is the pinned log
lines in the tests. (medium; sure)

**4.2 The account run on from the last working, four times.** `account_now` (:2716),
`_account_with` (:2663), `_in_hand` (:4111) and `_run_since_step_nm` (:5473) each recompute the
run since the last step. Three go through `_working`; `_account_with` re-derives course and run
itself and differs: it applies no allowance of the read by the mate's eye (`_allowed`, used at
:2615/:2624) and no drift hove to. It is the position the master's tide is looked up at
(`_tide_between` :2442), so the water and tide he works can be chosen from a slightly different
place than the account the player is shown. (low; sure that they differ, a suspicion that it
shows)

**4.3 The ghost reckoning.** `doubt_now` (:2742) copies a `Reckoning` field by field (:2755-:2765)
and replays `advance`. Any field added to `Reckoning` and not to this copy silently misstates
the doubt the player reads; `bring_up` (:2807) passes the same 16 arguments to `advance` by hand.
(medium hazard; sure)

**4.4 The fix's normal equations three times.** `_fix_doubt_nm` (:5849), `_fix_of` (:5939) and
`_compass_shift_nm` (:6064) each build the same weighted normal matrix and the compass-swing
vector; the 2x2 eigenvalues are computed in `_ellipse_of` (:1823), `_root_of` (:1886, which
`doubt_words` uses beside a call to `_ellipse_of`), `_least_eigen`/`_greatest_eigen` (:5927).
Two Mahalanobis tests: `Reckoning.within_doubt` (:1551, from P) and `_sigmas_off` (:6095, from the
ellipse dict, whose axes `_ellipse_of` has rounded to 0.01 mile). (low; sure)

**4.5 Flat-earth offsets, four ways.** `Reckoning.offset_nm`/`_offset_from` (:1021, :5634: cos of
the start latitude, 60 miles a degree), `_displaced`/`_move` (:5641, :1027: cos of the end
latitude), `geo.Position.offset_to` and `advanced` (geo.py:76, :90: mean latitude, metres on a
sphere), and haversine `bearing_and_distance` (geo.py:148). `_offset_from` and `_displaced` are
not inverses (at 50 N over 50 miles of northing the east component differs by about 1.7 per cent),
and `_own_now` (:4224) chains them. (low; sure)

**4.6 Name keys three times.** `reckoning._key` (:6114), `chart._name_key` (:282), `tide._key`
(:1148): the same five lines. Features are found by name in `Chart.find_feature` (:1660, an
index of id, modern and period names), but `shape_course` (:4569-:4574) loops over every feature
with its own key, and `_transit_named` (:3689) loops again. (low; sure)

**4.7 Two suns, two moons' ages, and a third mean sun.** `core/sun.py` (NOAA/Spencer series,
longitude from plane easting) gives daylight, noon and the altitude; `core/moon.py` computes the
sun's place again by Meeus (`_sun_longitude` :95) and `sights.amplitude_or_azimuth` takes the
sun's altitude from the first and its azimuth from the second in consecutive lines
(sights.py:772-:773). `tide._mean_longitudes` (:155) is a third set of solar/lunar elements. Ran
both suns for 15 June 1805 at 49.9 N 5.2 W: altitudes agree within 0.05 degrees, so it is
duplication, not error. The moon's age is computed by true elongation (`moon_at`) and by mean
longitudes (`tide.moon_age_days`, which the master uses and the docstring calls "the almanac's
arithmetic", reckoning.py:4952). (low; sure)

**4.8 Copies of constants.** `TIDE_HOURS` (reckoning.py:340) and `timedelta(hours=12, minutes=25)`
(tide.py:938); `SYNODIC_MONTH_DAYS = 29.53` (reckoning.py:341) and `LUNATION_DAYS = 29.530588861`
(moon.py:35); `CONTOUR_GRAIN_M` (reckoning.py:529, commented as chart.py's) and `CONTOUR_STEP_M`
(chart.py:150); `2.08` hard-coded in `Sea.horizon_nm` (sea.py:380) beside
`geo.HORIZON_NM_PER_ROOT_METRE`; `FOOT_M` in ground.py:77 and water.py:76; two eight-quarter tables
(`sea._QUARTERS` :155, `reckoning._WARD` :5759); `_lon_words` identical in reckoning.py:6125 and
sights.py:503; point-in-polygon in tide.py:254 and tools/build_charts.py:1858. (low; sure)

**4.9 The ship's position in two frames.** The sun's longitude is `ship_x` (the physics' plane
easting, core/world.py:1304) divided by the cosine of the current latitude (sun.py:132-:138).
The World's true longitude is integrated separately on the sphere and also receives the
scenario's stated current, which `ship_x` never sees (core/world.py:1558-:1567). So noon,
daylight and the time-sight guards drift from the true longitude with the meridians'
convergence and with any stated current. Arithmetic, not run: Channel to Madeira (50 N 5 W to
32.6 N 16.9 W) puts the sun's longitude about a degree out, some five minutes of noon. The
weather is likewise on a flat km plane about the start with Coriolis fixed at 50 N
(weather.py:125, used :1360-:1362) though its boxes run to the Canaries, where the true
Coriolis parameter is about 0.6 of it. (medium; likely)

**4.10 movement.put_aboard** (:1062, 121 lines) runs the same 25-line block twice, once for a
harness (:1102-:1132) and once for the player's seat (:1133-:1161). (low; sure)

## 5. Size and shape as a hazard

Longest functions in the part: `take_bearing` 194 lines (reckoning.py:3256), `take_fix` 193
(:3468), `_cast` 174 (:2949), `Chart.__init__` 168 (chart.py:945), `advance` 151 (:1075, 16
parameters), `observe_point` 136 (:1414), `movement.put_aboard` 121, `observe_line` 115 (:1298, 10
parameters), `movement.go` 88, `water.leaks` 83.

`Navigation` holds about 70 state fields, 38 of them declared at class level as defaults for
old pickles (:2028-:2085). Its caches (`_now`, `_doubt`, keyed by a 17-element state tuple,
:2689) are correct only if every input is in the key; `_moved()` must be remembered at every
observation (it is called 13 times). Module-level mutable state: `_CHARTS` (chart.py:890),
`_REGION_BOUNDS`, `_CHARTED_BOUNDS`, `_DIRECTIONS` (tide.py:803, :825, :1038), `geo._name_words`
lru_cache (:138), `Tide._about_cache` shared between Worlds. Class-level mutable lists on `Tide`
(:356-:359, with `noqa`) exist only for unpickling.

Function-level imports: reckoning 57, movement 29, water 7, ground 3, tide 1, sights 1. Many dodge
cycles (world to evolutions, orders, agents).

The comments are history first: "Until package 37e there were three rules ... Package 37e took the
observation whenever ... (the merchant passage's second noon, on Linux; on Windows the same sight
fell a hair under the line)" (reckoning.py:352-:384) explains a constant of 2.0. A newcomer is
drowned rather than helped: the current rule is there, but must be dug out of the record of every
earlier rule. Comments and code disagree in places: chart.py:1323 says the reckoning uses
`Reckoning.update_line`, which nothing in the game calls (it uses `observe_line`); `sea.py:30` and
:378 call `horizon_nm` "the hook 5b's sighting reads", but nothing reads it (geo.horizon_nm is used);
tide.py:6 still opens on "the eleven TICON gauges" with 100 in the file.

## 6. Correctness and honesty

**6.1 The simulation's boundary is not kept.** `freesail/world` imports `freesail.agents` 62 times
and `freesail.orders` 76 times (grep); core imports agents 16 times. In my part:
reckoning.py:4037 imports `agents.agent.door_words` and writes the holder's `model_name` and the
"door" into the ship's log ("worked at the master's station by ... (<model name>, through <door>)",
:4039, :4053); reckoning.py:4834 imports the private `_off_a_place` from `orders.navigation`;
movement.py:937/:962/:1007 import `agents.harness` and `agents.agent`, and movement.py:1028-1043
holds `VISITOR_BRIEF`, a prompt for a model ("stand_down(note)", "opt_out", "the token") inside the
world. `reckoning._master_station` (:3917) reads `world.agents` and `world.player_seat`. (high;
sure)

**6.2 The day's work gives a course made good with the distance sailed.** `Reckoning.advance`
adds each board's length to `run_since_noon_nm` (:1136) and `since_noon` returns that sum beside
the bearing from noon to now (:1793-:1801); the noon line prints "Course made good since yesterday
<point>, <run> miles" (:3851-:3855). After a day of tacking the distance is the sum of the boards,
not the distance made good the course belongs with. (medium; sure from the code; not run)

**6.3 `time_words` says "at noon" for any time in the twelve o'clock hour.** Ran it:
`time_words(12.5)` gives "half past twelve at noon", 12.75 gives "a quarter to one at noon"
(tide.py:1124-:1125). It speaks high water in `the tide by the almanac` and the tide's turn in a
shaped course (reckoning.py:4794). 00:15 gives "a quarter past twelve in the middle watch". (low;
sure)

**6.4 "Today" two ways.** `longitude_by_chronometer_reading` takes today as `tick // 86400`
(reckoning.py:5304), seconds since the scenario's start; every other reading uses the calendar
date (`sight_day == t.date()`, :5502). A scenario begun at 06:00 has its "day" end at 06:00.
Throughout, ticks are taken to be seconds (3600 and 86400 hard-coded) while core/clock.py:10 keeps
`TICK_SECONDS = 1.0` as a named constant. (low; sure)

**6.5 Faked by design, and said so.** The noon latitude is the truth plus a Gaussian error
(sights.py:212-:213); the time sight and the lunar are the true longitude plus drawn error
(:549-:560, :693-:724), "drawn and not computed" in their own docstrings. Honest, but it means
the elaborate moon (`moon_at`, nine lunar stars) decides only whether a lunar is allowed and how
wide the error is; no distance is ever cleared. (low; sure)

**6.6 Readings that change state.** `Water.leaks` (water.py:251), called by `describe` for the
readings, writes `st.ground_rate_m_per_h` and `st.ground_rock` (:286-:291). Reckoning was careful
to make readings pure (`note=False`, :2423); water is not. (low; sure)

**6.7 Thin science behind the numbers.** Every constant in reckoning.py names a source or says
judgement; `VARIATION_1805_DEG = 24.0` is "the model's as the package recalls it" (:265-:273),
and the build tool "does not yet compute it". The tide has three constituents only (M2, S2, N2,
constituents.yaml), with no diurnal ones, yet serves the Mediterranean blocks, where the tide is
small and mixed (a suspicion on the physics; low). Every climatology box is provisional; every one
of the 82 book streams carries a judgement list.

**6.8 Swallowed exceptions.** water.py:352 and :596, movement.py:226, :664, :921, :951, :1205,
:1253 catch bare `Exception` and carry on. (low; sure)

**6.9 Nondeterminism.** None found in my part: the weather's noise is a BLAKE2 hash of seed and
key (weather.py:354), the reckoning draws only from its seeded stream, `_seen` is an ordered dict,
the tide cache is keyed on cell centres precisely to avoid order dependence (tide.py:472-:476).
Sound.

## 7. Thin or overgrown

Overgrown. The reckoning models a 1805 master's error budget in more detail than anything it
feeds: biases as vectors resolved along observation lines, doubts that never narrow below a
shared compass term, a second reckoning for each officer, a timed hand-off to a model, a tide
worked from a period epitome by the quarter hour, a fix that chooses the best two or three of 36
marks by expected doubt (`_choose_marks`, :5888, up to C(12,3)+C(12,2) and then C(36,3) sets).
Against it the sights it is corrected by are the truth plus a draw. The chart is the heaviest
asset in the repository (359 MB) for a text game; its finest level (3", 288 MB) serves the lead,
grounding, the pilot and the coast trend, which a coarser grid with the hand-made dangers (already
read by name, chart.py:1253) would largely serve. Weather and sea are proportionate. The tide is
proportionate in the Channel and stretched thin beyond it. Water, ground and movement are not
navigation and should leave this part.

## 8. What is not tested

By grep of tests/ for the function or its order's words: `Navigation.chart_depths_within_doubt`
(reached by the reading `the depth of water`, api/readings.py:687; the phrase is in 9 test files
but the function name nowhere), `Reckoning.widen_toward` (:1576, the "cast does not agree" path),
`working_notice` (:3988), `_adopt_master_figure` (:4010, only indirectly through "my reckoning is"),
`set_way`/`_tend_way` (the way by marks; "by way of" appears in one test file), `Chart.shoal_ahead`
and `_deeper_side` (chart.py:1765, :1795; used by dealings.py:1049, :1894 and readings.py:2099),
`Weather.append_waypoint` (weather.py:1057), `Tide.open_edge_nm`, `Navigation.lay_by_drift`. Test
only, not reached by the game: `Reckoning.update_latitude/update_bearing` (and `update_longitude`,
`update_distance`, reached by nothing), `Tide.establishment_at`, `tide.local_mean_time`,
`Chart.level_at`. Dead: `reckoning._variation_words` (:5576), `water.well_feet_words` (:944),
`Sea.horizon_nm` (sea.py:374), `chart._ = field` (:1934, an import kept alive by assignment).
`weather.quarter_of`/`prevailing` are reached only by tools/climatology_check.py.

Behaviour a player meets that tests cannot see well: the log's English (4.1 and 6.3 are visible
defects that pinned-line tests did not catch), and long-passage drift between the plane and the
sphere (4.9).

## The ten findings that matter

1. **The world layer is not a simulation boundary.** reckoning.py writes a model's name and door
   into the ship's log (:4037-:4053) and imports a private order parser (:4834); movement.py imports
   agent harnesses and holds a model prompt (`VISITOR_BRIEF`, :1028); world/ imports agents 62 times
   and orders 76 times. High; sure.
2. **reckoning.py is one 3,528-line class plus an estimator.** Some 800-1,000 of its 6,126 lines
   are agent hand-off, an order-issuing autopilot (`world.submit`, :4542), reading formatting and
   the game's general number words; 57 function-level imports; 197 history references. Medium-high;
   sure.
3. **The chart tiles are 359 MB of plain git blobs**, rewritten in 9 of the 430 visible commits;
   the shallow pack is already 427 MiB, no LFS. Medium; sure.
4. **Two frames for one position.** The sun's longitude comes from plane easting that ignores
   meridian convergence and the scenario's current (sun.py:132, core/world.py:1558); the weather
   uses Coriolis at 50 N down to the Canaries (weather.py:125). Medium; likely (arithmetic, not
   run).
5. **The noon line pairs course made good with distance sailed** (reckoning.py:1136, :3851). Medium;
   sure from code.
6. **Number and distance words built eight or more times and already disagreeing** in what the
   player reads ("13 fathoms" against "thirteen fathoms", "dry at the datum" against "no water";
   two `miles_words`). Medium; sure.
7. **The account run on from the last working is computed four ways**, one of which
   (`_account_with`, :2663) differs and is the one the master's tide is looked up at; and
   `doubt_now`'s hand-copied ghost `Reckoning` (:2755) will go wrong silently when a field is
   added. Medium; sure.
8. **Pickle-compatibility shims are part of the design**: class-level defaults "for a checkpoint
   from before package X" across Reckoning, Navigation, Tide, Weather, Ground, Chronometer, with
   migration code in the per-tick `_peg` (:2243). Every new field costs a shim. Medium; sure.
9. **Visible small defects**: `time_words` "half past twelve at noon" (ran it); "today" by
   `tick // 86400` in one reading (:5304); stale docstrings naming `update_line` and an "inert hook"
   that is dead. Low; sure.
10. **Detail beyond what feeds it**: the estimator's bias algebra and the 36-mark fix search sit on
   sights that are the truth plus a draw; three tide constituents and provisional climatology carry
   the whole expanded map. Low-medium; sure on the facts, the judgement is mine.

## What I did not read

- tools/build_charts.py: docstring, function list and the fetch/format parts only, not its 3,099
  lines whole. tools/chart_manifest.py: first 80 of 99 lines.
- No chart tile opened (as instructed); data/charts/manifest.yaml only its head and a parse; the
  coast, features, overrides, audit-known.yaml and unverified-checks.yaml not read.
- data/tides and data/weather: counted by a parse (gauges, ports, areas, boxes), not read line by
  line.
- The tests: counted and grepped, not read; the suite not run.
- Callers outside my part (orders/navigation.py, api/readings.py, world/captains.py, lookout.py,
  dealings.py, core/world.py beyond the cited lines) were grepped, not read.
- Every file of my part was read whole: reckoning.py, chart.py, tide.py, geo.py, sea.py, weather.py,
  weather_script.py, sights.py, water.py, ground.py, movement.py, core/moon.py, core/sun.py.
