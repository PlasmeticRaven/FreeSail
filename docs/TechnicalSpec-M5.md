# FreeSail: Technical Specification, Milestone 5 (A world)

Companion to `docs/TechnicalSpec-M0-M2.md`, `-M3.md`, `-M3b.md` and `-M4.md`, whose
conventions hold. Milestone 5 is three short gates:

- **5a. The sea and the sky:** weather that comes from somewhere (pressure systems with
  fronts, seeded from a monthly climatology), the glass and the sky as readings, gusts by
  air mass and squalls as events, a sea state and the ship's motion in it.
- **5b. The chart and the reckoning:** a real sea from open and period data, two positions
  kept apart (where she is, where she is reckoned to be), the period's navigation from the
  log-line to the lunar, the tide as the world has it and as the captain works it, the
  lookout, grounding and anchoring.
- **5c. Ports, nations and other sail:** two ports as places with a market, a dockyard and
  a crew pool; the nations table; a dozen ships at far detail with sightings; the
  world-order channel; named people with a position and a state.

*Proves: emergent play; a passage is a game.*

Owner's decisions that shape this chapter (2026-09-29, `§4` of the scoping draft, kept as
§34 here): a real sea, the western Channel and the Western Approaches, with older coast
and depth data wherever they can be had and a data model that grows toward the Atlantic;
both the schooner trading and the frigate cruising, from the same ports; navigation to the
lunar; the tide explored and now decided; other sail at far detail with sightings, to be
revisited as the milestone progresses; pressure systems; the seaway in 5a; three gates;
the heavy packages to Fable. The four studies are adopted as written and are this
chapter's sources for every number: `docs/design/WeatherSystems.md` (W),
`Navigation1805.md` (N), `Tides1805.md` (T), `ChartData.md` (C); with
`ThreeDimensions.md` (the seaway as reduced motions), `InwardAndOutward.md` (the
principle) and `Papers-and-Books.md` (the ship's papers). The commitments in
`docs/agents/README.md` and decisions 16 to 18, 23 and 25 of the proposal are requirements
here.

Two rules run through every section. **Everything inward is reachable by an order or a
reading; everything outward arrives through something the ship models** (the principle).
**The world keeps the truth and the captain keeps his account,** for position and for the
tide alike; no reading ever gives the truth where the period could not have it, and the
viewer never draws it.

---

## Part 5a: The sea and the sky

### 1. What 5a proves

The wind has a cause the captain can read from the glass and the sky before it arrives,
and a seaway that the hands aloft and the hull feel. The gate's day of 4c is sailed
again under a system instead of a script, the readings the watcher of playtest 7 asked
for are there, and nothing in it names a front or a centre.

### 2. Weather systems (`freesail/world/weather.py`, `data/weather/climatology.yaml`)

**The model** (W §2b, §5). A small number of pressure systems in and near the box: each a
centre (position, velocity), a central anomaly (a low negative, a high positive, hPa), a
radius, and for a low a life curve of deepening and filling. The pressure at a point is
the month's background (about 1015 hPa) plus the sum of the anomalies with a smooth
radial profile. The geostrophic wind is the gradient turned ninety degrees; the surface
wind is that turned inward by `SURFACE_TURN_DEG = 15` and scaled by `SURFACE_SCALE =
0.7`, with a cap in strong curvature. Two fronts hinge at each low, a warm front ahead
and a cold front behind, each a bearing, a length and a width, rotating and trailing as
the low moves until the cold front catches the warm and the low occludes. A ship's
**sector** (ahead of the warm front, the warm sector, behind the cold front, or under a
high) fixes the sky, the rain, the visibility and the air mass by a table written from
W §1.3, and crossing a front adds its veer. The sea breeze and coastal fog are hooks on a
distance-to-coast that 5b supplies; until then they are inert.

**Seeding** (W §5). `data/weather/climatology.yaml` holds, per month: the rate of lows
crossing the region, the distribution of their tracks (bearing and distance of closest
approach), their speeds (15 to 35 knots), their central pressures, the probability of a
high over the area and its orientation, and the direction shares of W §1.1 (the 1750 to
1854 row) as the check. The first-pass values are the study's, marked provisional; the
*Channel Pilot*'s climatic tables are read from a printed copy when the owner has one,
and the CLIWOC extraction (W §1.5) is a build-time study for when the first pass proves
wrong. A system's parameters are drawn from the month's table when the scenario starts
and whenever a system leaves the box or its life ends, from a named stream of the world's
seed (`rng` stream `weather`), separate from the wind's gusts; everything after the draw
is arithmetic, so a day replays tick for tick. A test runs a thousand simulated months
and requires the direction shares within `CLIMATOLOGY_TOLERANCE_PCT = 5` of the table and
the gale days within a stated band of Ushant's counts (W §1.2). **As built (package 30):**
the climatology carries, beside the study's table, a monthly background pressure and a
mean gradient (without them the sea between systems was calm) and a broadly placed high;
the file says `provisional: true`; the tool prints the thousand-month table beside the
study's. Two known weak spots, recorded in the tuning notes: the north quarter runs four
to eight points short (a north-westerly falls on the west quarter's edge), and
strong-breeze days are about half of Ushant's in winter, Ushant reading high on its cliff.
The glass does not check at the cold front, the pressure being a sum of bells; a frontal
trough would give it (open item).

**The scenario file** (W §5). `weather` grows a `systems` list: each a name, a kind, a
radius, waypoints of position, central pressure and time, and for a low its fronts'
initial bearings; the model follows the waypoints exactly as `WeatherScript.at` does
today and draws nothing while a scripted system is present. The old `wind` waypoints
remain as a second form that pins the base wind directly (steady wind, gustiness 0, as
every truth is measured; its gusts and wander by the air mass since package 31b, §3);
when both are given the pinned wind wins and the systems supply only the sky and the
glass. `data/scenarios/gate-4c-day.yaml` is re-expressed as a
low passing well north of Falmouth with the ship in its warm sector, the cold front
through at 22:00 and the ridge by dawn; the glass falls slowly all day, checks at the
front and rises fast in the gale. A world order (§27) appends a system or a waypoint,
journaled at its tick.

### 3. Gusts, squalls and wander (`freesail/physics/wind.py`)

The gust mechanism stays (start, hold, release). The factor is no longer drawn from
1.1 to 1.5 whatever the mean but by **air mass** from the sector (W §4): a warm sector
1.10 to 1.20, neutral air 1.15 to 1.30, unstable air behind a cold front 1.20 to 1.45,
with the top of the last range reserved for **squalls**, which are their own events of a
few minutes, drawn in unstable air, carrying a veer of a point or two and rain, logged
as "a squall" at notable severity and ended in the log. The 45-knot gale of the gate's day
then gusts to about 55, and to 65 only in a squall the log names. The direction's random
walk becomes mean-reverting about the systems' wind with a spread of 5 to 10 degrees in
unstable air and less in stable; its docstring's "a point an hour" is corrected. Speed
wander stays at about a tenth of the mean. The M4c tuning note on the gust factor is
closed by this section. **As built (package 30, revised by package 31b):** package 30
ran the air-mass rule, the squalls and the reverting wander only when the wind had a
cause (the systems) and kept the milestone 2 draws bit for bit under a fixed or a pinned
wind, so that truths 48 to 51 and the gate's day in its pinned form did not move (the
pinned gale still gusted to 67). The owner ruled at gate 5a (decision 28) that the pinned
form should take the rule too, and package 31b retired the milestone 2 draws: every wind
is in an air mass, the systems' sector when they drive it, else neutral unless the
scenario says (`wind: {air_mass: ...}` for a fixed wind; a pinned waypoint's `air_mass`,
which holds from its moment on, so a scripted cold front can say the air behind it is
unstable). Truths 48 to 51 and the day's digest were re-measured and re-pinned with the
reasons (`docs/dev/TuningNotes.md`, M5a, package 31b): the pinned gale gusts to about 55
outside a squall, and squalls come only where a waypoint says the air is unstable. A
gust's peak is the ten-minute mean times the factor, as the studies define it.

### 4. The sea state and the ship's motion (`freesail/world/sea.py`, `physics/motion.py`)

As `ThreeDimensions.md` §"Where a third dimension is genuinely needed", item 1, as
reduced models and never a physics engine. **The sea state** is a field at the ship: a
significant wave height and period from the wind's recent history (a first-order lag on
the Beaufort mean, `SEA_BUILD_HOURS` and `SEA_DECAY_HOURS` in the tuning notes), plus a
swell with its own direction and period that a low leaves behind; in words by the period's
scale (a smooth sea, a short chopping sea, a heavy sea, a long swell from the westward),
never Douglas numbers. **The motion** is three reduced quantities: roll amplitude and
period from the sea on the beam and the ship's stability, pitch from the sea ahead, and
heave; each a number with a time constant, no integration of a six-degree body.
**Consequences**, each one line of code where it lands: the crew factor aloft falls with
the roll (a reef in a heavy sea is slower); the strain model reads the motion as an extra
load on spars and gear; the hull loses speed in a head sea by a small factor; the glass
pumps by a hundredth or two; the noon sight's error and the lunar's grow with the motion
(§14); the lookout's horizon is what the height of eye and the swell allow. The sea's
words are a reading (§5) and the roll-up says the sea by the hour. The M4 open item 7
(windage under bare poles) is measured in this package while the hull is touched.
**As built (package 31):** the sea is kept only when the wind has a cause (the systems)
or the scenario says `sea: true`, so a fixed or pinned wind keeps none and every M4
constant stands; the wind sea is the vector's part along the present wind, the old sea
becoming the swell's when the wind shifts; a cross sea more than five points off the
wind is "confused". The motion is a driven oscillator at the ship's own roll period
(8.2 s for the frigate, 5.8 s for the schooner), capped at 35 degrees, with pitch and
heave from the wave's length against the ship's, all relaxed over ninety seconds. The
consequences landed as one factor each: the crew factor aloft by a table on the roll,
the strain's load on spars and lines (never canvas) by roll and pitch above a
two-degree dead band, the hull's resistance in a head sea, the glass's pumping capped at
two hundredths, and the sights' error inert for 5b. Windage under bare poles was
measured and not tuned: running dead before fifteen knots the frigate makes 2.9 knots,
lying a-hull she drifts half a knot, and Steel and Falconer both have a ship under bare
poles keeping her way before the wind; the "few tenths" of the M4 item is the a-hull
drift, and moving the run would move every truth under sail. The owner's ruling at gate 5a
(decision 28): it stands as measured. The two rulings beside it, the pinned form under the
air-mass rule and the sea's cost answered by the hands and not by easing the storm, were
built by package 31b, after which the day under systems loses nothing: the close reefs are
in twenty-six minutes before the first squall. The wave-growth constants derive from the
Pierson–Moskowitz form as WMO-702 gives it, worked but not read from the page, and say
so.

### 5. Readings and log lines for 5a (`freesail/api/readings.py`)

New rows in the registry, each with its words and its absent pattern:

- `the glass`: inches to the hundredth as the vernier reads ("29.72"), from the model's
  pressure at the ship (33.86 hPa an inch) with the ship's own reading noise; and `the
  tendency`: the change over the last three hours and the last hour in the period's
  words (steady, rising, falling, falling fast), kept by the ship's own record, so a ship
  with no glass has no tendency. "The glass has fallen a tenth since the forenoon watch."
  Whether the ship carries a glass is the scenario's (W §1.7: the captain's own, rare in a
  small vessel); the schooner's scenario says.
- `the sky`: Beaufort's letters as words (clear, detached clouds, overcast, dark and
  gloomy, threatening, hazy, thick) with Luce's signs for colour, from the sector and the
  distance to the front with a little seeded noise.
- `the weather`: rain, drizzle, passing showers, squally, thunder, fog.
- `the visibility`: how far a sail can be seen (the horizon, a few miles, a mile, a
  cable), the number §13's sighting reads.
- `the sea` and `the motion`: the words of §4.
- `the temperature` is deferred until something reads it (W §5).

The wind's readings stay as they are; the veer at a front and the back before it come
from the model and the existing lines say them. The standing dialect gains `the glass`
and `the tendency` for nothing, so `when the glass is falling fast then shorten sail` is
a book's line. The log says a front's passage only as the ship feels it: the veer, the
squall, the clearing. No reading names a front, a centre, an isobar or a track; the
director and the scenario author see them (§27), the captain never does (W §3).

**As built (package 37f, 2026-10-07; the review of gate 5c's playtests, 5.8 and 8.2 under
"The log"): the log's lines said once.**

- *The wind's shift* (`World._log_wind_shift`). No `wind.shift` line while the ten-minute
  mean is under a light breeze (`WIND_SHIFT_FLOOR_KN`, four knots, where Beaufort's scale
  and the log's own words pass from "light airs" to "a light breeze"): "Light and variable
  airs." is said once as it falls so (`wind.variable`), and "The wind has settled at NE, a
  light breeze." once when it has stood a light breeze five minutes, which is where the
  next shift is measured from. Nor of an unsteady wind, one whose mean swings back and
  forth: the wind's second turn within the hour (it has veered, backed, and veers again)
  is said as "The wind unsteady, backing and veering about NW, a gentle breeze." in place
  of the shift, and nothing more until the mean has stood within two points for half an
  hour. A wind that turns once, a front's backing and veer, is logged as before. The
  event `a wind shift` keeps the same floor (`EventSpec.ready`): it does not come while
  the wind is not settled, and what it is measured from stands meanwhile.
- *Aback* (`physics/integrate.py`, `physics/sails.py`). The urgent "Taken aback" keeps
  the episode's clock (a minute clear). The lesser lines have a flag of their own
  (`HullState.aback_lesser`), armed again by her state: "she had no way on to lose" when
  she has way on again; "in the light air" when she has way or a working wind again; "as
  she lies at anchor" when she does so no longer. A calm is one line. A sail's "taken
  aback" is said once an episode and "filled again" once after it, armed again when the
  sail has stood full a minute with way on her; and neither is said of a sail laid aback
  by order (hove to, a whole-ship manoeuvre in hand, or an evolution on that sail, its
  yard or its sheets).
- *A "could not" that is no failure* (`evolutions/runner.py`). A precondition marked
  `done: true` in an evolution's file is one whose failing means the thing ordered is
  done (the sail is set, the boom rigged in). Found so by work that waited its turn, it is
  a routine line in the precondition's own words (`evolution.done_already`) and not a
  failed evolution; refused at the order, it is refused as it always was.
- *The lead and the book.* A cast that finds no bottom is routine, and the event `a
  sounding` is bottom found. A standing order with nothing to do (a failing `if`, its
  order refused, its last work still queued) says so the first time and then once a watch
  for each reason, the reason being the clause or the refusal without its figures
  (`standing.Runtime.say_held`); open item 15 of §33 had it once a watch for the `if`
  alone.
- *A condition's place is checked at entry* (`standing/book.py`, `check_places`). A
  condition on `the distance to <place>` whose place is neither on the chart nor a
  position pricked on it is refused when the order is given, with the nearest forms the
  dialect takes: "the nearest land" for the shore in sight, or the chart's name nearest
  in spelling. (A reading the registry lists as not yet built is still entered and held,
  package 33c's rule.)

### 6. Truths for 5a (behavioural)

| # | Truth |
|---|---|
| 52 | A low passing north of the ship backs the wind and drops the glass ahead of it, veers the wind at the warm front, holds steady in the warm sector, veers it sharply with a squall at the cold front, and rises the glass fast behind, in that order, in one day of the gate's scenario re-expressed as a system |
| 53 | A thousand simulated months of the climatology give westerly days within five points of the 1750 to 1854 shares in every month, and easterly days between a tenth in summer and a quarter in late winter |
| 54 | Over the open sea a gust exceeds its ten-minute mean by no more than 1.3 outside a squall in any air mass, and a squall is logged by name when it does more |
| 55 | The same seed and scenario replay the weather tick for tick, systems, fronts and squalls included, and a scenario with a pinned `wind` gives the pinned wind whatever the systems do |
| 56 | A gale of a day raises a heavy sea that the frigate's reefing takes half as long again in as in a smooth one, and the sea outlasts the wind by hours in the log's words |
| 57 | No line in the log or any reading contains "front", "centre", "isobar" or "hPa"; the glass is in inches everywhere a player reads |

### 7. Gate 5a (outline)

The gate's day again with `systems` in place of `wind`, the glass read at every watch
change and the sky at every bell; the squall in the middle watch; the sea's words through
the gale and the next forenoon; the watcher through the local runner asked what the glass
says and what it makes of it; a second day from the climatology at seed 7 in January and
one in July, the direction shares of a month printed by a tool; the fake watcher's day
replayed to the same digest.

---

## Part 5b: The chart and the reckoning

### 8. What 5b proves

A passage is a game: the ship crosses a real sea by the period's means, the captain's
account of where she is diverges from where she is, and the lead, the land, the sun, the
moon and the chronometer each collapse the doubt by their own measure. A landfall is made
by the reckoning, and one is made wrong.

### 9. The geographic frame (`freesail/world/geo.py`, `core/world.py`)

The world frame becomes latitude and longitude (WGS 84 for the data; the game says
nothing of datums). The ship's motion each tick stays in metres in her own local frame
and is converted at the end of the tick (C §5.1); the map and the chart project for
drawing. `Scenario` gains `position` (a start latitude and longitude) in place of the bare
`latitude_deg` the sun used, which now reads the ship's; `ship_x`/`ship_y` remain for the
tests and truths that use a flat plane (a scenario without a chart is the plane it was).
Distances in the log stay in miles, leagues and cables.

### 10. Chart data (`data/charts/`, `tools/build_charts.py`)

As C §5, adopted whole. The files: `manifest.yaml` (regions, levels, every source with its
licence text, attribution line, URL, retrieval date and checksum); `tiles/<level>/` of
int16 decimetres relative to chart datum in 512-cell tiles at four levels (2.5′ world,
30″ Atlantic, 3″ region, 0.5″ harbour), with a distance-to-shore field and a per-tile
minimum depth at the two finer levels; `coast/<region>.geojson`; `features/<region>.yaml`
(hazards, marks, lights with their dates, places, anchorages, transits, bottom notes,
each with the period name, the modern name, a source citation and a line the log can
say); `overrides/<region>/` (period depth and shore patches with the sheet, its control
points and the datum correction). The build fetches into a cache outside the repository,
refuses any source whose licence is not in the allowed list (public domain, CC BY, Licence
Ouverte, OGL, LGPL, named per-source permissions; not ODbL), resamples, rasterises the
overrides and splices the period shore, derives the fields and indices, writes the tiles
and the manifest, and a test checks that every feature and override cites a source and
every source has an allowed licence. The runtime reads with `numpy` and `pyyaml` only.

**Sources for the M5 region** (C §6): EMODnet DTM 2024 for depth and coast, SHOM HOMONIM
as the French cross-check, GEBCO_2025 under everything and for the world and Atlantic
levels, Histolitt for the French shoreline where needed; no OpenStreetMap in the tiles
and no UKHO survey bathymetry until its licence is read. **Period patches**: Falmouth and
the Helford, Plymouth Sound and Cawsand without the breakwater, the Scillies with St Agnes
lit and the Bishop dark, Brest and the Iroise; from the Hurd engravings of Mackenzie and
Spence, Bellin, and the *Pilote français*, facts transcribed and images never shipped
(the image is licensed, the facts on it are not). **The feature list** from Faden 1793,
Stephenson 1795, Imray 1848 and White 1835 with Serres 1801 for the views, in the period's
words. The region's tiles are committed (under 25 MB compressed); the Atlantic and world
levels are fetched by the tool. The unverified items in C §7 are checked from a browser
when this package is built, each a morning's work, and recorded in the manifest.

### 11. Queries (`freesail/world/chart.py`)

Depth here (tile lookup, bilinear); aground (short-circuited by the per-tile minimum
depth against draught plus the highest tide plus a margin; otherwise the keel's cells at
bow and stern against draught, heel and the tide's height); nearest coast (the distance
field and its gradient, a name from the features index); in sight of what (once a game
minute: the features within the geographic horizon from the masthead, 2.08 (√h_eye +
√h_object) miles with heights in metres, filtered by the 0.25° index, then by 5a's
visibility and daylight and by the feature's own rules). The captain's chart is a separate
product built from the same features and coast, degraded as §17 says; the truth tiles are
never drawn (C §5.5).

**As built (package 37d, from the review of gate 5c's playtests, 5.1 and 5.6).** The
distance field is kept in whole cells, and its gradient over neighbouring cells is one of
a handful of directions, due north where the differences are nought. Two queries were
added beside it. `Chart.nearest_shore` gives the nearest dry ground itself, its distance
to a cell's width and its bearing well within half a point: the field says how far to
look, and the cells above the datum within that reach are searched; the lookout reads it
once a minute and `coast_at` chooses its name by it. `Chart.coast_trend` gives the bearing
toward the land as a whole and how steeply the shore's distance rises to seaward (0 to
1), from the field read as a continuous one and differenced over a baseline of three
kilometres; the sea breeze blows toward it and is scaled by it (W §1.4), so that the
breeze no longer turns from cell to cell as the ship moves and there is little or none in
a channel or a road ringed by land. **One frame for the plane's points**: the World
places a point of the ship's plane from the ship's own position and the point's offset
from her (`World.place_of_plane`, `plane_of`), for each anchor's depth, the weather's
coast and another vessel's wind; one jump from the scenario's origin drifted from her
place with the miles run.

### 12. The lookout (`freesail/world/lookout.py`)

The sighting model is the lookout's reading: what is in sight, its bearing by compass
and its distance by estimation, in the log's words ("The Lizard bearing N by E, distant
four leagues"; "A light on the larboard bow"; the coastal views of Serres for a headland's
look). A light is seen at night by its own range and date; a castle or a tower by day. In
5c the same model sights sail. The lookout is a station in the sense of decision 24's last
line (a small model could hold it later); in 5b it is the world's own voice at routine
severity, notable for a landfall or a danger.

**As built (package 37d, from the review of gate 5c's playtests, 5.1).** Three things
changed, each what a man on deck could see and nothing of the truth he could not have.
*The distance is judged afresh as it changes*: the eye's error is still drawn once a
sighting, and the estimate is made again with it whenever the true distance is a tenth
more or less than at the last judging, for the land and for a sail alike (package 33b held
it until the ship herself had run a mile, which told a brig "a mile" at under two
cables); a calm re-draws nothing. *The shore itself is a sighting at every look* within a
league, the visibility and the night's mile, whatever headlands are in sight beside it,
hailed once a sighting and never a mark to take a bearing of; `the nearest land` is that
sighting as a reading (§15). *Land ahead*: in the lookout's minute, with way on over the
ground and not at anchor or aground, the first dry ground at the tide's present height or
danger in sight along her course made good and a point on either side, within what he
can see of the shore; a notable line when she would be on it in under ten minutes at her
present speed over the ground and an urgent one under four, each once an approach, armed
again when five looks together find nothing ahead within a quarter of an hour. It is the
lookout's one urgent word, it reads her true motion as an eye does, and in fog it is
silent: the lead is the guard there.

### 13. Two positions (`freesail/world/reckoning.py`)

Kept apart from the first line. **The truth** is the physics' position in the frame of §9.
**The reckoning** is a position with a two-by-two covariance, advanced each hour by the
logged run along the compass course corrected for variation and the master's leeway
allowance and his tidal set, grown by the error terms of N §3, and updated by each
observation as a line or a point measurement, the simplest Kalman form, twenty lines of
arithmetic, deterministic under the seed. The player never sees a matrix: the master says
"I would not trust the reckoning within twenty miles east or west, nor five north or
south", and the viewer's chart draws the ellipse faintly about the reckoned position.

**The error terms**, each a named constant in the tuning notes with N §3's source: the
log-line's short-line bias (3 to 8 per cent) and a quarter-knot read; the chart's
variation a decade old (the 1805 Channel value computed from the gufm1 field model at
build, about two points west, the exact figure recorded); a deviation by heading the
navigator cannot know (a few degrees, seeded per ship); steering a quarter to half a
point; leeway's estimate half a point out when close-hauled; the tidal set the master did
not allow for (the world's tide of §16 against the captain's); the noon sight's two to
five miles with a good horizon and none in cloud; the chronometer's rate error one to
three seconds a day; the lunar's quarter to one degree by skill and sea. The whole is
tuned so that a day's run of 150 miles in thick weather leaves an ellipse of some 30 to
50 miles after four days without a sight (N §3), against Chan et al.'s figures as an
upper bound and not a target. **The rule that keeps it honest**: the player's errors come
from the model's seeded draws; the world's truth comes from the physics; the difference
is what the player discovers.

**Observations.** A sounding is a line: the reckoning moves onto the nearest point of the
chart's depth contour consistent with the ground and the across-contour uncertainty
shrinks. A bearing is a line; two cross to a point; a transit is exact. A noon latitude
collapses north and south. A time sight by chronometer and a lunar collapse east and
west, by their own errors. The day's work is automatic at noon and on demand.

**As built (package 37d, from the review of gate 5c's playtests, 5.1), reversing package
33a's "second line along the bearing".** Package 33a laid the lookout's distance by
estimation down with every bearing as a second measurement good to fifteen per cent, so
that each single bearing was a fix of a good line and a poor distance: bearings of
different marks disagreed by their separate errors and the account jerked from one to
the other, and a standing order taking a bearing every few minutes made the master ever
surer of the wrong place. **A bearing now gives a line, and the distance by estimation is
laid down with it only when it is the better figure** (the second pass of 37d; the first
laid it down never, and a landfall on one mark after a long run, where a bearing and
distance of a headland is the period's ordinary way, was left leagues along its line).
After the line is worked, for a charted mark, the account's variance along the line of
sight is set against the estimate's own (`DISTANCE_BY_ESTIMATION_FRACTION` of the judged
distance, squared): when the account's is the greater the estimate is weighed in along
the sight by the gain at that doubt (`Reckoning.weigh_line`; never the replace form, and
`update_line`'s rule is untouched), and the line says so: "The Lizard bore N by W, five
leagues by estimation; the account laid down at that distance, the estimate being the
better figure: moved three leagues to the SW." The data carries `distance_applied`,
`moved_nm` and `moved_toward`. Once laid down the account is the better figure along
that sight, so the next bearing applies nothing until the doubt has grown again with the
run; after a good fix none is applied. Otherwise the words keep the distance by
estimation and add the account's own distance from the mark when the two differ by more
than a third. The rule trusts the account's own doubt: where the account believes itself
better than it is, the estimate stays out and the two figures stand side by side in the
line (`docs/dev/TuningNotes.md`, package 37d, the second pass, has two such cases). A
second bearing of the same mark moves the account across
the line and not along it. **A sail is no mark**: her bearing is given and moves nothing.
**Two or three cross to a point by `take a fix`** (§15): the point that best fits the
lines, each weighed by its own doubt across it at the mark's distance; the account is
set there and its doubt becomes the fix's own, a new departure. Whether a sight replaces
the account or is weighed in (`FIX_RUN_NM`) is unchanged here and is package 37e's.

**As built (package 37e, from the review of game 9: the account).** Three rules became one,
the doubt was made honest about the hours she has no way, and the master works his own tide
(§16). What 37d's paragraph above says of the distance laid down "when it is the better
figure", of `Reckoning.weigh_line` and of a fix that sets the account outright is
superseded by this one.

*One rule for every observation* (`Reckoning.observe_line`, `observe_point`). A noon
latitude, a longitude by lunar or by chronometer, a cast of the lead, a transit, a
bearing's line, a bearing's distance by estimation and a fix by cross bearings are each
worked the same way against the account, whatever the run since the last. **Weighed**: by
the two doubts, the account's across the observation's line and the observation's own, in
the Kalman form. **Taken**: when the two stand further apart than
`OBSERVATION_OUT_SIGMAS` times the two doubts added, the account is plainly out; it is
laid on the observation and its doubt in that direction becomes the observation's own.
**Kept**: when the weighing would move the account under half a cable
(`OBSERVATION_KEPT_NM`). `FIX_RUN_NM` and `Reckoning.weigh_line` are gone;
`run_since_fix_nm` is still kept as a record and nothing in the rule reads it.
`OBSERVATION_OUT_SIGMAS` is **two, not the brief's three**: by game 9's own figures the
noon of 16 June stood 5.23 miles from the account with doubts of 0.26 and 2.28, which is
2.06 of the two together, and the brief's test requires that noon taken. The lookout's
distance by estimation is weighed and never taken (an eye a third out, allowed to lay the
account down, threw a fixed account three miles and a half). A sail is still no mark.

*The same thing seen again tells him nothing new.* Each observation carries the part of
its doubt that a second look would repeat (the compass's allowance in a bearing, the
chart and the tide's allowance in a cast, the instrument in a sight), and the account's
doubt across a line already had is not narrowed below that part (`_again`, `_floor`,
`LINES_REMEMBERED`). A second cast within two miles of the first of that ground
(`SAME_GROUND_NM`), or within the doubt, is weighed and narrows nothing.

*A bearing* is worked as the line through the mark when the account's doubt across the
sight is more than a tenth of the distance to the mark (`BEARING_LINE_FORM_FRACTION`), and
as an angle at the account otherwise; his doubt of it is the compass's allowance at the
mark's distance (`COMPASS_ALLOWANCE_DEG`, two and a half degrees; a degree and a half
once the variation has been observed).

*A cast* is as good a line as the bottom is steep where it is matched: the contour's
tolerance in fathoms over the fathoms the chart shelves in a mile there, read over the
reach of his own doubt (`_sounding_sigma_nm`; a quarter of a mile at the best, and no line
at all over a flat bottom). `SOUNDING_ACROSS_SIGMA_NM`, three miles whatever the ground,
is gone. Where the chart about the account shows less water on one hand and more on the
other than the cast (`Chart.depth_span`, at the contour search's own half-mile grain), the
cast agrees with the account and it is kept, whatever point the search finds further off.

*A fix* (`Navigation.take_fix`, `_choose_marks`, `_fix_of`). Unnamed, the master takes,
of all the sets of two or three marks in sight that cut by `FIX_MIN_CUT_DEG` or more, the
set that leaves the least doubt (`_fix_doubt_nm`: each line's doubt at its mark's
distance, the compass's allowance common to the set, and half the cocked hat to be
expected of three), so that a near mark is taken before a far one. The fix's point and
its covariance, the common compass term in it, are then worked against the account by the
one rule: a good fix rules a doubtful account, and a poor one no longer moves a good
account ("the fix the poorer figure; the account kept, within a cable of it").

*The words say what the master did*: each line carries one of "the account moved four
cables to the N", "the reckoning was out by it; laid down by the observation: moved five
miles to the S" and "the account kept" (with both doubts when a sight is kept), and its
data says `how` (`taken`, `weighed`, `kept`) with `moved_nm`.

*The doubt, honest* (`Reckoning.advance`, `Navigation._peg`, `_working`, `doubt_now`).
The traverse board is pegged in four states: riding at anchor, hove to, without way, and
under way. Only riding stops the account and its doubt. Hove to, the master reckons her
drift through the water by eye, to a quarter of a knot (`HOVE_TO_DRIFT_KN`), and doubts it
by half a knot (`HOVE_TO_DRIFT_SIGMA_KN`); without way he runs nothing for her; in both
the tide he allows carries the account and his doubt of the stream grows. Under way two
terms are added to N §3's: his log-line, four per cent of the run along the course
(`LOG_LINE_DOUBT`), and his compass, its allowance across the course; they are passed by
`Navigation` only, so truth 58's arithmetic on a bare `Reckoning` is unchanged. His doubt
of the stream lies along the stream's set, three quarters of its rate
(`STREAM_DOUBT_FRACTION`), and grows for three hours of a tide and no further
(`STREAM_DOUBT_HOURS`): a stream cannot set her further than it runs. A read of the log
taken while she lay to is not used after she fills away; her way is by eye until the log
is next hove, and between heaves the read is allowed by the mate's eye for the way she
has gained or lost (`WAY_BY_EYE_GRAIN_KN`; Falconer 1780, *Log*). The doubt is said as it
lies when it is long, thin and not along the compass's quarters ("within three miles NE
and SW, nor a mile across"; `doubt_words`), and in cables under a mile. `the reckoning's
uncertainty` and the chart's ellipse give the doubt as it stands at the moment asked
(`doubt_now`), not as it stood at the last working.

*Known shortfalls, measured* (`docs/dev/TuningNotes.md`, package 37e): at anchor in the
Bay of Brest, fixes every five minutes by three marks all in one quarter of the compass
leave the account believing itself good to a cable while it stands three cables out; and
the rule takes an observation whose own stated doubt is too small (the cruise's
chronometer, 7.6 miles out against a stated doubt of 2.3, laid a good account down off
Plymouth for half an hour until the next bearing took it back). *Both answered by package
37j, below.*

**As built (package 37j, the account amended; the review's part K and the fold-in's
finding, §33 item 24).** What 37e's paragraphs above say of "taken" and of a cast's search
is amended by this one.

*The better figure is believed* (`Reckoning.observe_line`, `observe_point`; the lead's
decision). When an observation and the account stand further apart than
`OBSERVATION_OUT_SIGMAS` times their two doubts added, one of them is plainly out, and the
observation is **taken** only when its doubt across its line is no greater than the
account's; otherwise it is **weighed** as any observation is, the account moving by the
part its own doubt is of the two, and the line says the master doubts it
(`Observation.doubted`, `doubted_words`): "the sight stands five miles and a half to the N
of the account, and the account, good to three cables, is the better figure: the account
moved a cable to the N". The number two is kept, and for its own reason now: it is what
he trusts a figure within (the lunar's and the chronometer's words), so that "plainly
out" is "further apart than he would trust the one and the other within"; 37e's reason
(game 9's noon taken at 2.06 of the doubts together) no longer bears, that noon being
believed or doubted by the better figure and not by the number. Held in tests with their
figures: the merchant passage's second noon (an octant's 2.5 miles against a fix's three
cables, a hair either side of the doubts together: weighed both ways, the account within
a cable of the fix); the cruise's chronometer (7.6 miles out against 2.28, the account a
cable in doubt: kept); game 9's lunar of note 5 (12.12 against 0.83: kept, and set
eighteen leagues off, still weighed and doubted); and game 9's noon of 16 June, doubted
against the account the lead had kept at a quarter of a mile, and weighed by the doubts
against an honest one. "Taken" outright that noon cannot be against any account no
better than the sight: their doubts together are then nine miles, and the two stood five
apart (docs/dev/TuningNotes.md, package 37j, has the forenoon sailed again).

*The cast not beyond doubt* (`Navigation._cast`, `Reckoning.within_doubt`,
`widen_toward`). The master looks for the cast's depth and ground within his doubt
(`OBSERVATION_OUT_SIGMAS` of it, the ellipse as it lies; `chart.contour_point`'s
`inside`, the search finer than half a mile within a small doubt, `CONTOUR_FINEST_M`) and
no further; a cast never moves the account further than its own doubt. The chart's grain
(37e's `depth_span`) stands. Where nothing within the doubt answers, "the cast does not
agree with the chart where Mr — believes her; the chart has that water nearest a mile
and a half to the SE of the account: the account kept, and its doubt widened": the account
stays, and its doubt is grown toward the nearest water that answers (searched as 37e
searched, five miles or twice the trust) until that water lies just beyond the edge of
what he would trust it within (`APART_EDGE`), so that the same cast again stays apart. A
second cast within `SAME_GROUND_NM` of one that did not agree is the same thing seen
again and widens nothing further. The data says `agrees` and `apart`.

*The tide's height under the lead by his book* (`_tide_allowance_m`, `_masters_tide`):
the cast is reduced to the chart's datum (low water at springs) by half the spring rise of
the nearest place in his epitome to his account and half the day's rise by the
half-cosine of the hours from his own high water; never the world's tide. Every place of
both tables has a rise (`data/tides/establishments.yaml`, `rise_judgement` where the
period's table gives none: the world's spring range rounded to the foot). The line says
the reduction when it is a fathom or more ("Two fathoms of tide allowed by the epitome:
nine fathoms on the chart."); the data carries `tide_allowed_m`. The fall to the day's
low water he gives at an anchor's letting go (`tide_height_by_master_m`, package 37f) is
counted from the day's own low water and is unchanged in meaning.

*Each board by itself* (`Navigation._board_ends`, `BOARD_ALTERATION_POINTS`,
`BOARD_LEAST_S`). At heaving to and filling away, and under way whenever her head goes two
points or more from the mean heading pegged since the last working (a tack, a wear, an
alteration of course), the account is worked up to that minute and the next board begun
there; a board shorter than a minute is not cut again. Because the account is now worked
more often, the log's read and her drift by eye, each one figure for the whole time it
serves, are kept as biases that grow in a straight line across the boards
(`Reckoning.read_doubt`, `drift_doubt`, `held`): the read's until the log is next hove
(`new_read`), the drift's until she fills away (`lay_by_drift`). `Reckoning.advance`
without `held` (truth 58) is as before.

*A fix's doubt on one hand* (`_compass_shift_nm`, `_one_hand`, `ONE_HAND_DEG`). How far
the compass's own error, one sigma of what he allows for it, moves a fix by its marks is
the same in every fix by marks on that hand with that compass; after a fix the account's
doubt that way is never narrowed below it (nor raised by it above what it was). With the
marks within six points and a half of one another, "good to" says the doubt as it lies
when the two differ: "good to a cable along the shore and four cables off it".

*The danger list from the best figure.* `the dangers` and the dangers a shaped course's
line passes are drawn from the account as it stands and said to the cable
(`geo.distance_words`): "the line passes the Penwin and the Vaze within a cable, the
Manacles within two cables and the Governor within a mile".

*The departure* is the scenario's own position (the truth at the start, as a departure
taken from the land in sight is) with a mile's doubt; until 37j the account opened a mile
out by a draw. At anchor the run since noon does not grow (tested).

### 14. Instruments, the sights and the lunar (`freesail/world/sights.py`, `core/moon.py`)

**The noon latitude** from the sun model already in `core/sun.py`, automatic at noon if
the sky allows, refused in cloud, with the octant's or the sextant's error and the
horizon's; double altitudes when noon is clouded is a later refinement. **The chronometer**
is a scenario item (`chronometer: {maker, rated, rate_s_per_day, drift: seeded}`): the
captain's own, rare in small vessels, absent from the schooner unless the scenario says;
wound daily (the log says the master did it; forgetting is a scenario event); a time
sight gives a longitude with the rate error times the days since rating plus the sight's
own two or three miles. **The lunar** (N §5, adopted): `take a lunar` (of the sun, or of a
named star) checks the conditions from `core/moon.py`, a low-precision moon good to a
degree (Meeus's short method; the same moon serves the tide's springs and neaps and the
night's light), refuses in the registry's words when the moon is too young, too low, out
of distance or the sky is thick, and otherwise occupies the master and two mates for a
quarter of an hour and returns an hour later a result *drawn, not computed*: the true
longitude plus an error from the seed scaled by the master's skill, the sea state and the
moon's rate (a quarter of a degree for a good master on a quiet day, a degree for a poor
one in a seaway; 10 to 39 miles at 50 N). The engine never clears a distance. If the
moon model runs past about a hundred lines, the lunar opens 5c and nothing else waits on
it; if the budget bites, the star lunar is cut first.

**The master** is the first named person (§22): a skill number for the sights, and a
position (on deck, below) that the lunar and the reckoning occupy. `set the reckoning to
<lat> <long>` lets the captain override him, as he could.

### 15. Orders and readings for 5b

Orders (the grammar's nouns from the chart's features, as the ship's from the ship file):
`heave the log` (also automatic every hour in the frigate and every two in the schooner);
`heave the lead`, `heave the deep-sea lead` (the latter brings her to, or runs the line
forward at a cost in hands and time); `take a bearing of <mark>` (refused if not in
sight); `work up the reckoning`; `observe the sun`; `take a sight for the longitude`;
`take a lunar [of <body>]`; `wind the chronometer`; `compare the watches`; `set the
reckoning to <lat> <long>`; `allow <n> knots of set to <direction>` for the traverse;
`come to an anchor`, `weigh` (§18); `shape a course for <place>`, which reads the
reckoning and not the truth and is refused where the chart has no such place.

Readings: `the reckoning` ("49° 52' N, 6° 10' W by account"); `the reckoning's
uncertainty` in the master's words; `the depth` and `the ground` from the last cast with
its age; `the bearing of <mark>` when in sight; `the distance run since noon`; `the
course made good`; `the latitude by observation`; `the longitude by chronometer` with the
days since rated; `the longitude by lunar` with the master's trust; `the chronometer's
error by lunar`; `the moon` (its age, up or not, in distance or not); `what is in sight`.
Each with its absent pattern ("No sight today; the sun was hid at noon"; "No lunar to be
had: the moon is two days old"). Log lines as N §4: "Hove the log: six knots and a half."
"By the mark seven; fine grey sand with black specks." "Noon. Latitude by observation 49°
48' N; the reckoning was 49° 56'. Course made good since yesterday ENE, 131 miles.
Longitude by account 5° 40' W." The roll-up keeps the noon line and the casts.

**As built (package 37d).** One order: `take a fix`, or `take a fix by <mark> and <mark>`
with a third if wanted (also `fix her position`, `take cross bearings`): cross bearings of
two or three charted marks in sight (a headland, a mark, a light, a danger that shows;
never the shore close aboard, a sail or a transit). Unnamed, the master takes the three
whose least angle of cut is greatest when that is thirty degrees or more, else the two
that cut best; two lines that cut by less than thirty degrees are no fix. It is refused in
words that carry the cure (nothing in sight; one mark only; marks that cut too fine). The
line is `reckoning.fix`, notable when the account moved more than a mile: "Fixed by cross
bearings: Black Head SW by W, St Anthony's Head NW by N, the Deadman NE by N; the lines
met within six cables. The account moved three leagues and a half to the NW: 50° 05' N,
4° 57' W by the fix, good to three cables." It is an order of the master's, where `take a
bearing of` is, and the officer of the watch has it by the captain's `you may take a fix`
until package 37g. A fix leaves its own doubt in the account, so a bearing taken after a
good one lays no distance down (§13), and one taken after a poor one, with a headland
close aboard, does. One reading: `the nearest land` (`the nearest shore`), the shore as
the lookout has it ("the land about Rame Head, on the larboard bow, bearing NW, nine
cables"; "no land within a league"; "not to be seen" by night or in thick weather),
compared in miles by what he said and never by the chart's own metres. Three events: `a
fix`, `land ahead`, `land close ahead`. Two severities: a dragging anchor is urgent and
the pilot's hails are notable.

**As built (package 37e).** `shape a course for <place>` orders the helm the course to
steer so that, by the master's reckoning, she makes good the line from the account to the
place (`Navigation.shape_course`, `shape_for`, `_make_good`): against the tide he allows
at that hour (his own, §16, or the captain's), with the leeway he allows when she must
lie close-hauled, at her way by the log's last read or by eye. The words give the line
and the course: "Shaped a course for the Goulet: NE by account, ten miles. Allowing the
flood, a knot and a half to the E by N, steer NE by N to make it good; the allowance
holds till the tide turns, about half past four." With nothing to allow they are as
before; with no way on her they say so and hold the line's own bearing; where no course
makes it good at her present way they say so and give the course that loses least. It is
worked once, when the course is shaped and at each firing of a standing rule that shapes
one; nothing alters the helm afterwards. The line is tried against the land as against
the charted dangers (`Chart.line_shore`): "the line crosses the land about Black Head",
"the line passes the shore under Petit Minou within two cables"; the course is ordered
all the same. The line's data carries `line_deg`, `distance_nm` and `allowing` (`by`,
`knots`, `toward_deg`, `steer_deg`, `way_kn`, `made_good`).

One order: `allow the tide by the book` (also `allow the tide`, `work the tide yourself`,
`hand the tide back` and the forms in the primer's table), which hands the tide in the
reckoning back to the master. `allow <n> knots of set to <direction>` now *replaces* the
master's own tide, in the traverse and in a course shaped, from the moment it is given
until it is handed back; `allow no set` tells him to allow nothing. The officer of the
watch has none of the three, as he has none of the master's orders. The reading `the
reckoning` gives the position by account and the tide allowed with whose it is
("... by account; the tide allowed: the flood, a knot and a half to the E by N, by the
directions for the Goulet and high water at Brest by the epitome"; "by the captain's
order, two knots to the westward"; "none, in open water"; "none while she rides at
anchor"), and its data carries `position` and `tide`. One event: `the turn of the tide by
the reckoning`, the master's own tide turning (the routine line `reckoning.tide`, which
is also said when by his account she passes into other waters), for a book that would
shape its course again; the swing at anchor's `the turn of the tide` is unchanged.

**As built (package 37j: `the port` and `the depth of water` by the captain's means, the
review's G4, the last step of its plan).** `the depth of water` (also `the water`, `the
depth of water by the chart`, `the depth by the chart`, `the charted depth`) is the
chart's depth at the position by account, at the chart's datum, said as the chart's and
never as a cast ("eleven fathoms at low water by the chart, at the position by account;
the chart has seven fathoms to fifteen within the account's doubt", the span read over
the doubt's ellipse at twice the doubt). In a standing order's condition the depth reads
the last cast of the lead (`the depth`), as the officer of the watch would read it, and
the chart's figure only when the book says `by the chart` (`standing.grammar`); the
merchant passage's two conditions read the lead since. `the port` gives the port's road
by its bearing and distance from the position by account with the account's doubt ("Falmouth,
the outer road bearing N by W by account, five miles, the account good to a mile"), as
`shape a course for` does, and beyond the pilot's cruising ground "no port within the
pilot's cruising ground by account; the nearest is Falmouth, NNE by account, seven
leagues, the account good to a mile"; at anchor in a port she is in it, as anyone aboard
can see. `the chronometer`'s miles of longitude are worked at the latitude by account. A
test asks every reading of two ships of one seed four miles apart with one account and
gets one answer, but the lookout's own rows (what the eye makes of the land and the
compass's bearing of a mark) and the moon's altitude in the data behind `the moon`
(`tests/test_readings.py`, `test_no_reading_gives_the_true_position_by_any_road`).

### 16. The tide (`freesail/world/tide.py`, `data/tides/constituents.yaml`, `streams.yaml`)

As T §5, adopted. **The world's tide**: M2, S2 and N2 at the eleven TICON gauges (St
Mary's, Newlyn, Devonport, Weymouth, Dover, Brest, Le Conquet, Roscoff, Saint-Malo, St
Helier, Cherbourg; CC BY 4.0, the licence text under `docs/references/`), interpolated
along the coast and across the Channel by the cotidal geometry; the astronomical
arguments set from `core/moon.py` so that high water at full and change falls at the
port's establishment. K1 and O1 are dropped (5 to 9 cm). Streams are tabulated by area
(`streams.yaml`: axis, spring rate, neap rate, phase against local high water) from the
published figures of T §1 and Bowditch 1802's headland table, with SHOM's open 2D atlas
for the Fromveur, the Four and the Goulet; the height gradient is not used for streams.
Evaluated once a simulated minute; five cosines. The stream sets the ship in the physics
as a water velocity; the height is under the lead and over the rocks that cover. **The
captain's tide**: the establishment of the port from his epitome (the ship's papers) and
the moon's age from his almanac, worked by Moore's rule of 48 minutes a day, wrong by up
to an hour as Bowditch admits, and by more when his book's establishment is an old one. The
difference between the two tides is the play, as the difference between the two positions
is. (Package 37j: the master's allowance under the lead is his own epitome's, by a rise
for every place of his table, §13.) **Exposure by the period's means only**: no tide readout, ever; the establishment table
by handle; the almanac's moon; the lead against the chart's depth; the landmark's state
(the Black Rock shows at half tide); the ship riding to the tide at anchor, the cable
slack at the turn; the set allowed for in the traverse. The primer carries the rule of 48
minutes and the headland table. The rule of twelfths is not put in an 1805 mouth (T §2).

**As built (package 37e, the owner's ruling of 2026-10-07: the master works the tide into
the reckoning himself).** The captain's tide of this section now has its place in the
traverse. **The world keeps the truth and the captain keeps his account, for the tide as
for the position**: the master's tide is worked from his epitome (the hour of high water
at the nearest place in his table, by Moore's rule), his almanac (the moon's age, for
springs and neaps) and the directions' statement for the waters his *account* puts her
in, and nothing else. No line of it reads `Tide.at`, `Tide.stream_at`, the tide's state
or the ship's true place (`Navigation.book_tide`, `_tide_between`; `tide.Directions`,
`BookStream`, `load_directions`); a test reads the source for the words and another sails
two ships ten miles apart in two waters with one account and gets one tide.

*What the directions say* is in `data/tides/streams.yaml` beside the world's own figures
for each area (`book:`): the point of the compass the flood sets toward, the rate at
springs to the half knot, the rate at neaps (half of the springs' where the period gives
none), and the hour, after high water at the nearest place in his epitome, at which the
flood runs strongest, to the half hour; with its source, and each figure that is
judgement named. By the owner's ruling, where the tide study found no period source for a
stream (the Fromveur, the Chenal du Four, the timing in the Goulet) the directions are
taken to give its set to the nearest point and its spring rate to the half knot, the
neaps at half of that, marked judgement: so the Fromveur's neaps are three knots and a
half by the book against the world's five. Period statements used: Bowditch 1802's
headland table for the hour off the Lizard and off the Start, and his "the Current in the
Mid. Channel is N.E." for the open Channel's set (which is twenty degrees from the
world's axis; the hour there is judgement, the sentence's "1 H. 30 M." being ambiguous).
Beyond the limits of the waters the directions cover (`book_limits`) he has no statement
and allows nothing.

*In the traverse* the stream is summed by the quarter hour (`TIDE_QUARTER_S`) as one more
course, under way, hove to and becalmed, and not while she rides. *His errors* are the
period's: his hour by Moore's rule (an hour to an hour and three quarters early against
the world in mid-Channel on 10 to 13 June 1805, about right on the 16th), his rate a
round figure, his set a point of the compass, and the wrong water allowed where his
account is in the wrong one. In the Iroise his tide follows the world's within a mile
over a tide; in the open Channel it is little nearer than allowing nothing, and his doubt
(§13) says so. The captain's `allow <n> knots of set` replaces it until `allow the tide
by the book` (§15). The lead's allowance for the height of tide is as before.

### 17. The captain's chart and the viewer (`client/map.js` becomes the chart)

The viewer's map becomes the captain's chart: the coast and the features as his chart of
1804 has them (a longitude error of the period's chart, a pilot's words where the chart
has no sounding), the reckoned position and its ellipse, the track by account, the noon
positions, the bearings taken, the soundings with their ground. The true position is not
in the snapshot the client receives (`api/queries.py` gives the reckoning; the truth is in
the save and the tests only). Since package 37j neither is the true distance of any
landmark in sight, and a mark's bearing in the snapshot is the point the lookout said it
by (`lookout.Lookout._data`); the log's own line of a sighting keeps them for the record
(`_line_data`), as it did. A `--casual` display of the truth is a later option and a
display choice, as the proposal says; nothing in the simulation changes for it.

### 18. Grounding and anchoring (`freesail/world/ground.py`, `evolutions/anchor_*.yaml`)

Touching is an event with speed, heel, tide and bottom type; the consequences are the
hull's (a stop, a strain on the masts, a leak by the bottom's kind and the speed) and the
log's, and getting off is the tide's business or the anchor's (a kedge is later).
`come to an anchor` and `weigh` are evolutions in the M3 form with hands and time (Steel
1794 vol. II: stemming the tide; Lever 1808); at anchor the ship rides to the tide and the
wind, the log says how, and the cable's scope against the depth is a check the evolution
makes. The port's mooring is 5c's.

**As built (package 37d, from the review of gate 5c's playtests, 5.8).** Each anchor's
depth is read where the anchor lies by the World's one frame (§11), not at a point found
by one jump from the scenario's origin: after a long run that point lay a mile and more
from the ship ("let go in twelve fathoms and a half" and then "Brought up ... in six
fathoms and a half"; a brig "Brought up ... in no water", the point having fallen on
the land), and the wrong depth fed the cable's holding. "... is dragging" is an urgent
line. The other anchoring faults of the review (the scope, the depth named in the order,
"Brought up" after `let go the anchor`) are package 37e's.

**As built (package 37f, 2026-10-07; the review's 5.8, 8.2 and 10.4, 10.5): the ground.**

- *An anchor's name is honoured* (`orders/ground_tackle.py`). `veer`, `heave short`,
  `heave in` and `weigh` work the anchor named, and the anchor she rides by when none is
  named; "to" is to a scope wherever the name stands, and a bare number so much more.
  An anchor that is not down is refused by name with the one she rides by; weighing an
  anchor she cannot come over while another holds her is refused with what would do it.
  `heave in to <n> fathoms` and `heave in <n> fathoms` are the capstan's orders for less
  cable (`heave_in.yaml`); `heave short` and `weigh` take no number. Moored, heaving in
  on one cable veers the other as she comes over.
- *`let go` says its scope and takes one* (the owner's ruling: the default stays five
  times the depth). Its first line is what it will do; `and veer to <n> fathoms`, `with
  <n> fathoms` (and `in <n> fathoms`, as before) veer to that and no further; `come to an
  anchor in <n> fathoms` is the depth to let go in, with `and veer to <n> fathoms` for the
  scope. Three notable warnings as the anchor goes: her swinging circle within
  `SWINGING_ROOM_M` (a cable) of the nearest land as the lookout judges it, the depth
  wanting more than the cable bent, and the water at low water by the master's own tide
  less than her draught. `World._say_brought_up` says "Brought up" for an anchor let go
  by itself.
- *The dragging* (`physics/anchor.py` `judge_cables`; `World._tick_anchors`). It begins
  only on a tick in which the anchor moves, having come home `DRAG_SAY_S` (seconds of
  creeping long past are forgiven as it holds); it is urgent once, with the advice that
  is left to take; while it goes on a notable `anchor.coming_home` line no oftener than
  `DRAG_REPORT_S`, with how far; "holds again", routine, after `DRAG_SETTLE_S` without
  moving, and the next drag is then a new one.
- *The ground's words* (`ground_factor`). A bottom note holds as the mean of the grounds
  it names (`GROUND_HOLDING` keeps its figures): "rock and mud" 0.55 where it was held as
  bare rock, 0.30. Every port's road and anchorage has its note; Brest road was given one
  (`brest-road`, mud, from the same words of Faden's as the Bay's).
- *At anchor she is still a ship* (`orders/verbs.py`, `UNDER_WAY_ONLY`). Of the whole-ship
  orders only the manoeuvres wait till she weighs or floats, with the helm's orders and
  `trim`; sail furled, handed or loosed to dry, yards squared or braced, the upper masts
  and yards sent down or swayed up are taken.

### 19. Truths for 5b (behavioural)

| # | Truth |
|---|---|
| 58 | Four days from Finisterre in thick weather without a sight, the reckoning's ellipse is 30 to 50 miles long east and west and under ten north and south, and a clear noon collapses the north-south axis to under five |
| 59 | A cast of the deep-sea lead in the Channel Soundings moves the reckoning onto the chart's contour consistent with the ground and narrows it across the contour to a few miles, leaving it along the contour as it was |
| 60 | The frigate with a chronometer rated at Plymouth forty days before has a longitude by chronometer within four miles of the truth when the rate is right, and a lunar on a quiet day shows the chronometer gaining when the scenario's rate is wrong by two seconds a day |
| 61 | `take a lunar` is refused within three days of new moon, with the moon under fifteen degrees, and in thick weather, in words that say which; allowed, it occupies the master and two mates for a quarter of an hour and answers within a degree an hour later |
| 62 | At Falmouth high water on the day of full moon falls at the establishment within twenty minutes; springs are twice neaps; the perigean spring exceeds the apogean by about a fifth |
| 63 | Off the Lizard the stream runs east from about three hours before to three hours after local high water at two knots at springs and one at neaps, and a ship hove to for six hours is set the log's miles by it |
| 64 | The captain's tide worked from Moore's rule and an 1805 establishment differs from the world's tide by less than an hour on the day of full moon and by up to an hour at the quarters |
| 65 | The Bishop is dark and St Agnes is lit in 1805; a night landfall on Scilly from the south-west sees St Agnes at its range and nothing else |
| 66 | Standing on by account across the reckoning's ellipse toward the Manacles in thick weather grounds the schooner on the ebb at the speed the log gives; the same passage with the lead going hourly does not |
| 73 | In fifteen knots under plain sail the cutter lies as close to the wind as the schooner or closer (package 32b; the hierarchy of the generator's rules across sizes; the first wording asked for half a point closer, which the owner amended on 2026-09-30: a cutter points much as a schooner does, and pointing by the file's own geometry is open item 12's, not a per-rig factor); measured 58° against 58° |
| 74 | The brig lies further off the wind than the schooner and within half a point of the frigate, or the ordering the sources support, said which (package 32b) |
| 75 | The cutter on a beam reach in fifteen knots under plain sail makes a speed within the band the package sets from the type's records, the source named (package 32b; provisional where a judgement) |
| 76 | The brig likewise (package 32b) |

### 20. Gate 5b (outline)

Revised 2026-09-30 (decision 29): the chronometer, the lunar, the tide, grounding and
anchoring moved to gate 5c's set, so that this gate proves the passage by the reckoning
and the noon sight alone. The passage Ushant to Falmouth in the frigate and in the
schooner, neither with a chronometer: a departure bearing off the Stiff, the log hove
hourly, a noon latitude, the Channel Soundings by the deep-sea lead, the Lizard sighted
and bearings taken, the Roads entered and the ship brought up (anchoring's evolution is
34's; the gate ends at the Roads). The same passage in thick weather with no sights, the
reckoning's ellipse read at each noon, and a landfall made wrong on purpose. The cutter
and the brig sailed through the same orders as the two reference ships. The chart in the
browser with the ellipse and the track by account. A tool that prints the chart data's
manifest and attribution. A saved day loaded from its checkpoint in seconds and carrying
on to the replay's digest. `--load` and the two climatology days carried from gate 5a.
Expected numbers from seed 7 and the day's weather pinned.

---

## Part 5c: Ports, nations and other sail

### 21. What 5c proves

There is somewhere to go and someone there: a passage between two ports with a cargo and
a sighting, and the log a captain could keep. The world-order channel exists, journaled,
for scenarios now and the director later. The inward minimum is in place: named people
with a position and a state, the cabin and the deck as places, the boat alongside, so a
message can come through the door.

### 22. Places and people (`freesail/world/places.py`, `people.py`)

The inward minimum of `InwardAndOutward.md`, and no more. A **place** is a name and a
description: the quarterdeck, the deck, the cabin, the gunroom, the tops, the boat, the
shore; a person is in one. A **person** is a name, a role (the captain, the master, the
first lieutenant, the mates, a messenger, a pilot), a skill where a system reads it (the
master's for the sights, §14), a position (a place) and a state (on deck, below, asleep,
ashore, sick, occupied by a task and until when). Orders move them where the period's
orders did (`send for the master`, `pass the word for`); the log says who came and went.
The crew of M3 stays counts and ratings; these are the few people the story names. The
sail room and the hold are the first places below, each with its keeper (the sailmaker,
the purser or the mate) and its paper (the sailmaker's account, the manifest), so that
what is in them is known by visiting or by reading, and the console's old `the sail room`
query becomes a paper the browser and the library serve alike
(`InwardAndOutward.md`, the worked example). The
harness's stations may later bind to a person (an officer at the master's place is M6);
in 5c a person is data and a line.

### 23. Ports (`data/ports/*.yaml`, `freesail/world/ports.py`)

Two ports, Falmouth and Brest, as places with: an anchorage and a mooring (the Roads and
the inner harbour; the Rade and the Penfeld), with the tide's window from §16; the boat
(sent ashore and back with hands and time, carrying a person, a message or a purchase);
the **market** (a list of goods with prices that move with supply, demand, war and season
by a small rules table, and a cargo the schooner's hold carries by tons; `buy`, `sell`,
`the prices`); the **dockyard** (repairs and stores by the part graph: a spar, a suit of
sails, cordage, water and provisions, with time and cost; the frigate's stores and
victualling from the yard, the schooner's from the market); the **crew pool** (hands to
recruit by rating, at a price and a delay); and a **stance** toward each nation (open,
neutral, closed, hostile), which decides whether the port is entered at all. Arriving is a
sequence the log tells: the pilot cutter, the pilot aboard as a person, the anchorage, the
boat, the shore. Leaving is the reverse with the tide.

**As built (package 37f, 2026-10-07; the review's 5.8, "Getting under way").** A vessel
whose yards are all on one mast is got under way as Luce's schooner is (1884, ch. XXXIV):
her mainsail hoisted with its boom steadied over to the side she is to cast toward, which
sheers her for the tack while the anchor still holds her; her topsail's yard laid abox
and her jib hoisted with its sheet to windward when the anchor is aweigh; her helm tended
from the first heave. In the playtests all three of a schooner's casts ran to the
timeout, and each was logged "She has paid off". For every rig, "paid off" is no longer
said at a timeout: at `cast_timeout_s` she is taken as she lies, on the tack wanted (the
line says how far she has paid off), on the other (the line says so, and she is got
under way on it), or hanging near the wind, when she is given till `cast_give_up_s` and
the evolution then fails in words with the anchor aweigh. On the merchant passage the
schooner casts in a minute and a half where she timed out at seven.

**The pilot cutter** is a vessel of her own (owner, 2026-09-29): a cutter as a ship file
(`data/ships/cutter.yaml`, generated by `tools/gen_ships.py` from Steel's tables with the
schooner's classes of parts; her base the armed cutter *Sherbourne* of 1763, 85 tons,
54 ft 6 in by 19 ft, six 3-pounders, from Slade's draught at Greenwich (`docs/design/VesselCandidates.md`); one
mast with a gaff mainsail, a square topsail, a running
bowsprit and jibs), the first of the vessel library's catalogue entries and the test the
proposal names for pillar 2: adding her changes nothing in the engine, and the one
generator addition expected, the running bowsprit, is recorded as such. She is sailable
enough to exist at near detail and honest at far; she carries the hierarchy truths of
§19 (73 and 75, from package 32b, owner 2026-09-30) and no verification of her own until
milestone 8 makes her a reference ship. The orders' grammar must read her file as
it reads the schooner's, with no rig assumed: that is the generalisability the vessel
library will stand on, and any order that fails on her is a fault in the grammar, not in
the file.

### 24. Nations (`data/nations.yaml`)

A small table: nations, who is at war with whom in 1805, letters of marque, what flags
mean, each port's nation. Enough for the stance in §23 and the sighting's "a stranger, her
colours not made out" in §25. Prizes, convoys and blockades are M7's play; the table is
theirs to read.

### 25. Other sail (`freesail/world/ships.py`)

A dozen ships at **far detail**, a mix of the frigate, the schooner, the cutter (§23) and
a **brig** (owner, 2026-09-29: `data/ships/brig.yaml`, two square-rigged masts with a gaff
spanker from the frigate's classes of parts; her base the brig-sloop *Harpy* of 1796, 316
tons, 95 ft by 28 ft, sixteen 32-pounder carronades, from Winfield's tables and the Greenwich draught
(`docs/design/VesselCandidates.md`); sized between the cutter and the frigate so
that the catalogue has a hierarchy of size to build on; the brig-sloop is the Navy's
brig and the merchant brig the trade's, one file with two descriptions; a full complement of head
sails, jib and flying jib and fore topmast staysail, and a main staysail and main topmast
staysail between the masts, since a brig without her staysails is not a starting point;
if the staysails prove troublesome that is a fault in the generator's rig rules to fix
there, a bad sign for the vessel library and treated as such; the same rule as the cutter,
no engine change, the hierarchy truths 74 and 76 of §19 and no verification until milestone 8): each a hull from the ship files, a nation, a captain with
a goal (trade this route, patrol this station, run home) and a plan (waypoints and a
speed from the wind by a polar drawn from her file), moved cheaply at the roll-up's cadence
by the same wind and tide as the player. The **lookout** (§12) sights them by the horizon
formula and 5a's visibility: "Sail ho!", the bearing, then what she looks like from the
tops as she nears (a rig, a size, her colours or none), at the period's distances. At
**near detail** (within a stated range of the player) a ship becomes an object with a
heading and a speed and a simple keep-course captain who obeys her plan and no more; her
sails are drawn by the viewer from her state, not simulated. The **level-of-detail
switch** is built with its promotion point; the crewed model and the rules-based captain
that would fill it are M6's, and the switch says so in one line of code. The owner's
ruling: far detail with sightings for this milestone, revisited as it progresses. A
sighting is a notable event, so a standing order can act on it and a watcher wakes.

### 26. The world-order channel (`freesail/world/orders.py`)

Orders to the world, not to the ship: append a weather system or a waypoint; put a ship
on the sea with a goal; deliver a message to a place; change a port's stance or a price;
name a person aboard or ashore. Given only by a scenario file (at a time) or, later, by
the director (§7.6 of the proposal); never by the captain's grammar, which refuses them in
words. Every world order is journaled at its tick with its source, visible after the fact
in the log at the driver's mark, saved and replayed. This is the seam the director needs
and the principle's carrier rule: a world order can send the cutter, it cannot put the
message on the table.

### 27. Scenarios (`freesail/world/scenarios.py`, `data/scenarios/`)

The scenario file grows to hold the position, the chart region, the systems, the tide's
date (the moon's age follows from the date), the ship's papers (the chart she carries and
its year, the epitome's establishment table, the almanac, the chronometer), her people,
her cargo, the ports' state, the other ships, and the world orders by time. Two starting
conditions ship with 5c: **the merchant passage**, the schooner from Falmouth for Brest
with a cargo, no chronometer, a master who can work a lunar; **the naval cruise**, the
frigate from Plymouth to the station off Ushant with a chronometer at the captain's
charge, stores from the yard, a lunarian master. Both from the same ports, both on the
gate's weather from the climatology or pinned.

### 28. Truths for 5c (behavioural)

| # | Truth |
|---|---|
| 67 | A ship at far detail moves by the same wind and tide as the player and is sighted at the horizon distance her rig's height and the visibility give, as "Sail ho!" with a bearing first and her rig only as she nears |
| 68 | A message from Brest reaches the captain in his cabin only by the boat, the door and a person, each a line in the log in order, and never by a line from nowhere |
| 69 | The schooner's cargo bought at Falmouth and sold at Brest makes or loses the sum the two markets' prices give, and a week's war news moves a price by the rules table |
| 70 | A port closed to the ship's nation refuses her entry in the pilot's words and the stance is the nations table's |
| 71 | A world order given by the scenario at a time is journaled at that tick with its source; the same order typed at the captain's prompt is refused |
| 72 | The merchant passage and the naval cruise replay to the same digest from their scenario files, ships, ports, people and weather included |

### 29. Gate 5c (outline)

The merchant passage: the schooner's cargo bought, the tide's window out of Falmouth, a
sail sighted off the Lizard and not made out, the Iroise in the schooner's chart's words,
the Goulet against the ebb refused by the master's tide and taken on the flood, Brest
entered by the pilot, the cargo sold. The naval cruise: the frigate from Plymouth, the
station off Ushant kept two days under standing orders, a stranger sighted and chased by
the plan's speed alone, a message by the cutter. A watcher through each door for a watch
of each. Both replayed.

**Joined to this gate** (decision 29, 2026-09-30): the chronometer, the moon and the
lunar (package 33b), the tide, grounding and anchoring (package 34), with their truths 60
to 64 and 66, since 5c's ports need the tide's window and the anchorage, and the passage
of 5b did not need the lunar to be a game.

**The lead's watch, as an officer's** (owner, 2026-09-29, revised 2026-09-30). The
officer of the watch is built after every other element of 5c is in place (package 37),
so that it is built with the world already there: per-order authority from the
vocabulary's verb levels, a domain (sail handling; no course changes, no all hands unless
the brief allows), the standing conflict rule reused as the welfare detector for a
station whose orders change the readings, `hand over the deck`, a station brief, the fake
proving each. Then the lead takes its first station in the game, the officer's watch on
one of the two passages, through Claude Code opened on the repository, on the same terms
as every other model: the consent question asked of these weights first and the record
kept under `docs/agents/consent/`, the brief read as any instance reads it, the log and
the journal the only record. The lead knows the game from the inside, which the record
will say; a fresh Fable session or an Opus 5.5 one is run beside it. **Gate 5c's verdict
waits on that watch**: it is given on the lead's officer's watch and the owner's own
playthrough together. A captain's station is milestone 6's.

**The station as it stands after the gate's first playtests** (package 37g, 2026-10-07;
the owner's rulings of 5 and 7 October). The deck goes to and fro without unseating the
officer: `you have the deck` and `I have the deck` move him between the watcher's standing
and the officer's, and his own `hand_over` gives the deck back and no more. Bearings and
fixes are within his domain; an order that changes her course is the course whatever its
words. The captain's word is a named thing, checked for what it names, or his general
authority to work the ship (`you may work the ship`), which keeps back the port's business,
his standing orders, a new destination and what cannot be undone; either stands through the
deck going to and fro, has force only with the deck, and ends when he takes it back or the
officer leaves the station. To avoid an immediate danger the officer's own word opens the
helm, heaving to and letting go an anchor. The detector counts orders that undo one
another, and never an alteration of the course. A paused or silent officer does not keep
the deck. A station that was stood down or left may be taken by the same model or another.
The contract is spec M4 §11's last bullet; primer 16 has it for the captain.

---

## 30. Performance

The budget is truth 51's floor (500 ticks a second for one frigate on the build machine,
1000 as built). 5a adds microseconds a tick (a few exponentials); 5b's queries are tile
lookups and a per-tile short-circuit, with sightings, the tide and the reckoning on a
minute's cadence; 5c's far-detail ships tick at the roll-up's cadence. A truth per gate
measures the whole at the gate's scenario, and the tuning notes carry the numbers.

## 31. Packages (outline; the heavy ones to Fable)

- **30. Weather systems** (5a §2, §3, §5 for the glass and sky; the scenario's `systems`;
  the gate's day re-expressed; truths 52 to 55, 57). Fable.
- **31. The sea and the motion** (5a §4, §5 for the sea's words; windage under bare
  poles; truth 56; gate 5a cut). Fable.
- **32. The chart data and the queries** (5b §9 to §12; the build tool; the four patches
  and the feature list, which is reading and tracing; truth 65). Fable, with the hand work
  reviewed by the lead against the sources.
- **32b. The cutter and the brig as ship files** (§23's cutter and §25's brig, pulled
  forward from 35 and 36 by the owner, 2026-09-30: the generator's cutter and brig rules,
  the two files, the running bowsprit, and the orders' grammar run across four ships; the
  hierarchy truths 73 to 76; no engine change, any found reported as a fault). Fable.
- **32c. The suite in two tiers, the days built once, a Windows job** and **32d. The
  `freesail` command, the settings file and the setup step** (the cold review's items 1
  and 9; spec M4 §24 item 6). Opus, in the owner's local sessions on the Windows machine.
- **33a. The reckoning, the noon sight, the captain's chart, the checkpoint save** (5b
  §13, §14's noon latitude, §15, §17; truths 58 and 59; gate 5b cut). Fable.
- **33b. The chronometer, the moon, the lunar and the azimuth; the captain's chart in
  his hands** (5b §14's rest; the variation by observation and the chart queries by
  account from decision 30; truths 60 and 61; in gate 5c's set by decision 29). Fable.
- **33c. The passage's words** and **33d. The browser's shelf** (the playtests' grammar
  and viewer follow-ups of decision 30: the readings at the prompt, the aliases, the
  starter book as a choice, open item 15; completion, the library pane, the clock on a
  station, zoom and pan). Opus, beside 33b.
- **34. The tide, grounding and anchoring** (5b §16, §18; truths 62 to 64, 66; in gate
  5c's set by decision 29). Fable.
- **35. Places, people, ports and nations** (5c §22 to §24; the pilot boarding from 32b's
  cutter; truths 68 to 70). Fable (the owner's ruling, 2026-09-30; the draft said Opus).
- **36. Other sail and the world-order channel** (5c §25 to §27; 32b's brig at far detail
  with her merchant description; the two scenarios; truths 67, 71, 72). Fable.
- **37. The officer of the watch** (§29; written when 36 lands; gate 5c is cut at its merge
  so that the gate covers the officer's watch (owner, 2026-10-02); the lead's watch follows
  it and gate 5c's verdict waits on that watch). Fable.

Each package's brief is written in `docs/dev/M5-WorkPackages.md` when its predecessor
has landed, in the form the M4 packages took.

What was built for gate 5c, and how it stands against this chapter whole, is
`docs/dev/M5-CloseOut-5c.md`; for gate 5b, `docs/dev/M5-CloseOut-5b.md` (the close-out form of milestone 4, adopted from the cold
review: the specification keeps the contract and points to the close-out rather than
growing "as built" paragraphs).

## 32. What this milestone does not do

Combat (M7), officers and captains as stations and the crewed promotion of other sail
(M6), the director (M7b), the tutorial and the deck view (M8), the Atlantic beyond the
tiles the tool can fetch, temperature, the sea breeze and coastal fog until the coast is
in (then 5b), double altitudes, the kedge, interiors beyond a name and a description.

## 33. Open items from this chapter

1. The *Channel Pilot*'s climatic tables and the pilot-chart percentages are to be read
   from printed copies (W §1.1); until then the climatology's first pass is marked
   provisional in the data file.
2. The 1806 Beaufort wording, the Admiralty's first issue of barometers and the WMO gust
   table (W) are quoted only once verified.
3. The chart study's unverified list (C §7): the Défense library's records, SHOM's two
   licence statements, the UKHO bathymetry licence, the datum offsets at the four ports,
   the lights' dates. Package 34 (2026-10-02) verified the tide's constituents against
   TICON's own file and the French ports' datum offsets from the RAM; Newlyn's and
   Devonport's are the study's UKHO figures, and Weymouth's, Dover's and St Helier's remain
   judgement (`data/tides/constituents.yaml` says which).
4. The lunar's day count per lunation and the 1805 clearing time (N) are the study's
   estimates; the game's constants say so.
5. Whether the schooner's file offers `shift the mainsail for the storm trysail`
   (playtest 8), for the M4 follow-ups list.
6. A station for the lookout (decision 24's last line), when a small model is tried at it;
   the fitness drill of package 37 is its first half.
7. The sail room in the browser (owner, playtest 8) waits for §22's places and papers;
   until then the console's query stands and the browser has none.
8. From package 31: the wave-growth sources (Pierson–Moskowitz, Bretschneider, JONSWAP,
   the Weiss and Rayleigh figures) to be read from a page; the head-sea resistance and the
   roll damping as judgements. (The day under systems lost the mizzen topsail to a
   65-knot squall until package 31b's parallel manning; it now loses nothing.)
9. From package 30: a frontal trough so the glass checks at the cold front; the north
   quarter's share. (The pinned form under the air-mass rule and the day under systems
   alone are built: packages 31b and 31.)
10. The lead at a station (§29): the consent question put to the lead's own weights inside
   the harness before the gate, the record kept as any other; and, for M6, the owner's
   wish that the lead take an officer's or a captain's station once they exist. **The
   officer's station is built (package 37, 2026-10-02); the consent question for the
   lead's weights and the lead's watch are gate 5c's verdict's.**
11. From package 31c: a door act recorded at the stationing tick, before any tick has run, is not made by a replay (`restore()` then `start()` does not play door acts); and `a wind shift` as a stand-by event reads the mean wind while the log's own `wind.shift` line reads the instant wind at two points, two definitions to unify when `core/world.py` is next open. *Unified in package 37c:* the log's line now reads the ten-minute mean as well, two points from where the log last put it and held a minute (`World.WIND_SHIFT_HOLD_S`). The event's reference is still the sample last read, and the log's is its own last line.
12. **The physics of staying** (from package 32b's finding and the owner's playtest of the frigate, 2026-09-30; the lead's probe the same day). Not the headsails: the schooner gets through in four and a half minutes by a sternboard and the cutter dies seven degrees short of the wind, because the turn is the frigate's (the rudder's force falls with the speed squared and the yaw damping constants were tuned on one hull, so a fifty-foot cutter turns at a degree and a third a second where she should spin), and the miss-stays rule is one number for every vessel (0.8 knots or 180 seconds before her head is through). When it fires, `TackScript._miss_stays` squares every yard in one tick with no hands and no time and orders the helm back to the old heading, which the owner saw as the yards jumping square and the ship hanging head to wind with no way for the rudder to bite. The package to write: yaw that scales with the vessel (rudder area and lever, damping from the lateral plane, the radius of gyration), checked by a turning truth per ship (Luce 1884 Appendix L for the frigate; the type's reputation for the cutter); a miss-stays rule that reads the vessel and allows Luce's recovery before it gives up (she hangs: the helm reversed as she gathers sternway, the head yards kept aback to box her head off, the after yards to the new tack once through, the headsail sheets held to windward as a state for the small vessels and for heaving to); squaring the yards on a true miss as a brace with hands and time, never a jump; and the schooner's, cutter's and brig's tacks as truths beside truth 10. Also from 32b: a per-sail pointing from the file's own geometry (aspect ratio, the sheeting floor from the gear, leeway from the lateral plane) in place of a per-rig factor, which the owner declined; truth 73 amended to "as close as the schooner or closer" (owner, 2026-09-30). The browser draws a running bowsprit at the length in the ship graph fetched once and does not redraw a reef until reload (the snapshot carries no spar length, `api/queries.py`).
13. **Sheets and trim are two records of one thing** (the owner's playtest, 2026-09-30). A fore-and-aft sail's trim is a number on the sail (`sheet_angle`), moved for free every tick by `evolutions/trim.py`'s `tend_sheets` (the cold review's finding 3) and by `trim the <sail>`; its sheet is a line with a state (belayed, free, parted). Let the main sheet fly and the line is free while the angle stays where it was; order `trim the mainsail` afterwards and the angle moves and the line stays free, so the order reports work and the sail does not draw. The fix is one truth: the sheet holds the trim. A sheet's length hauled sets the sail's angle by the boom's geometry (the generator knows the boom, the horse and the traveller); `haul`, `ease a fathom`, `let fly` and `belay` are level-0 orders on the line that move that length with hands; `trim the <sail>` (to the wind, or to a bearing) is an evolution that works the sheet to the length the wanted angle needs, hauling a sheet that was let fly as part of the trim, with hands and time as a brace has; the standing book's `trim` reaches the same evolution; and the free tending is retired, the afterguard tending sheets as routine work at a cadence the book or the watch orders. A sheet let fly then has no load and the sail flogs, as now; a sheet belayed carries the sail's load into the strain model by its length and angle. This moves the helmsman's `full and by`, which was tuned around free tending, and truths that read it; a physics and evolutions package with open item 12, before gate 5b.
14. From package 33a: `VARIATION_1805_DEG` (24° W) is the study's unverified figure, the gufm1
   field model not computed by the chart build; the azimuth and the amplitude are built by
   33b (the master's allowed variation comes from the observation, within a degree), so
   only the world's figure remains to verify; the landfall rule fires at the departure too
   (land in sight off Ushant), harmless.
15. **Built by package 33c (2026-10-01).** From the cut of gate 5b (`docs/dev/M5-CloseOut-5b.md`): the standing runtime's conflict
   rule treats every ship-subject evolution as one part, so `heave the lead` and `wear ship`
   are logged as contrary orders on the ship (routine lines; the lead still goes); and an
   `at <event>, if <condition>` rule logs a routine "not carried out" line at every event
   whose condition fails. Both for the standing runtime's next pass.

16. From package 35b (2026-10-02): where EMODnet has no land GEBCO's fill left a metre of
   water over some of the shore (Roscoff's town and the Isle Verte were water in the tiles
   until the patch made them land); the rest of the region's coast is to be swept for the
   same once, a build-tool check; and Roscoff's narrows were left to the modern grid where
   the sheet's georeference error was as wide as the channel.
17. From package 37d (2026-10-06). **The saves**: a save and its checkpoint carry the
   build's stamp (`"build": {"name", "rules"}`; `core.world.BUILD_NAME`, set by hand at
   each package or gate, and a fingerprint of the code and the data a replay reads), and
   `load` says which road it took and why and does not replay another build's game with a
   station's transcript in it unless asked (`--replay-anyway` at every door). A save is
   exact from its checkpoint, and a replay is promised only on the build that wrote it; a
   replay driven by the transcript alone is the harness's rework in milestone 6. Open: a
   station's *replies* are still placed in a replay by the count of journaled orders
   (`Playback._due`), as its seating was until this package; a reply given after a
   driver's line of the same tick may replay before it.
18. From package 37d: **the recorded passages and the bearing as a line.** The books of
   the gate's passages took a bearing every glass and at the landfall and relied on its
   distance by estimation to put the ship on the chart. Each book's bearing rule now
   takes a fix after the bearing (one line a book). After the first pass the schooner's
   run in to Carrick Road and the merchant passage's run through the Goulet did not come
   through. **After the second pass all six come through and are re-measured**: the
   schooner on the ticks recorded before 37d; the merchant with the bearing alone in
   pilot water and two of the Goulet's points moved for the flood's set, passing the
   Mingan 1.8 cables to the north (`docs/dev/TuningNotes.md`, package 37d). Left for a
   later package: the account runs wild for some minutes as a ship gets under way from
   an anchor and lags on a fair stream, believing itself good the while, so the Goulet's
   rules fire late; and `take a fix` puts a poor fix in the place of a better account.
19. From package 37d: the dialect compares `the nearest land` in miles and leagues and
   refuses cables (`standing/grammar.py`, `_DISTANCE_UNITS`); `under half a mile` is
   taken. The sun's local time still reads the ship's easting on the plane (`ship_x`),
   which is the same family as the anchor's point (§11) and is seconds of time on a long
   run; mending it moves every recorded sunrise and was left.
20. From package 37e, closed: item 18's "the account runs wild for some minutes as a ship
   gets under way from an anchor and lags on a fair stream" (a read taken before she lay
   to is no longer used, and the master's tide is in the account) and "`take a fix` puts a
   poor fix in the place of a better account" (the one rule, §13).
21. From package 37e, open, for the lead:
   - **Truth 59's words.** "A cast of the deep-sea lead ... moves the reckoning onto the
     chart's contour" held to the letter only while a cast after a long run replaced the
     account. By the one rule the cast is weighed (eight miles of doubt against a mile and
     a half: ninety-six parts in a hundred of the way), and the test allows the contour's
     tolerance and a fathom. The truth's sentence in §19 is not changed here.
   - **`OBSERVATION_OUT_SIGMAS` is two**, where the brief said three, for the reason in
     §13. With three, game 9's noon is weighed and moves the account 150 yards, as before.
   - **An observation whose stated doubt is too small** lays a good account down (§13,
     the cruise's chronometer). The master's doubt of his chronometer's rate is a second a
     day (`sights.RATE_DOUBT_S_PER_DAY`, "the low end of one to three"); this one was out
     by more than three. The remedy is in `sights.py`, which is not this package's.
   - **Repeated fixes by marks all on one hand** leave the account surer than the
     compass allows (§13). The fix's own "good to" is honest there; the account's is not.
   - **The open Channel's directions.** Set NE (Bowditch's) against the world's 065, and
     Moore's hour: the master's tide in mid-Channel is a rough allowance. One number in
     `streams.yaml` (the hour, marked judgement) can be flipped if the lead reads the
     "1 H. 30 M." sentence the other way.
   - **Three beats of the recorded passages did not come through** and are strict
     expected failures with their reasons in the tests: the naval cruise's stranger is
     chased and lost, not spoken; the schooner's pilot at Falmouth hails her and does not
     board. The merchant passage's pilot of Brest boards and asks for his boat again
     before the road of Bertheaume (the test is re-measured to it). *After package 37f:*
     the first two stand as they were (below); the pilot of Brest now stays aboard to the
     anchor.
   - **The entrance of the Chenal du Four.** The stream areas have hard edges, and the
     line from the Iroise to the road of Bertheaume crosses the corner of the Four's
     water, three knots and a half on one side of a line and a knot and a half on the
     other. The merchant's book works the course for the road again every five minutes
     there. A course shaped is worked for the water the account is in at that moment,
     by the owner's ruling; a line that crosses two waters is the book's to shape again.
22. From package 37f (2026-10-07), open, for the lead:
   - **A dragging that relapses.** By the brief, an anchor that has not moved for five
     minutes "holds again", and the next drag is a new one with its own urgent line. On
     bare rock in the Goulet's tide an anchor may hold six minutes and come home again,
     and each relapse is then urgent (eight urgent lines in eight hours when that state's
     ground is forced to rock, as many as before the package; on its own ground, rock and
     mud at 0.55, there is one). Treating a relapse within a quarter of an hour of "holds
     again" as the same dragging would end it; it is not what the brief says, and is not
     done.
   - **A course shaped with no way on her.** A course is worked once, for the way she has
     as it is shaped, and a ship filling away from lying to now has a knot and a half
     where she had four. The frigate's passage shapes its course as she fills and was
     set a point wrong by it for four hours; her book works the course again every glass
     (§20's passage; `gate-5b-passage.orders`). Whether `shape a course` should allow for
     the way she will have, or say that it could not, is the reckoning's question.
   - **The cruise's chase.** The stranger is still chased and lost. The frigate, close
     hauled on the starboard tack with the brig four miles on her quarter, is given "steer
     NE by E" by the book's `keep her bearing` half an hour into the chase, a course
     across the wind's eye from her head, and the helm takes her through the wind with
     every sail aback (91954, urgent); she has no way on at 93634 and the brig is out of
     sight. The first form of the chase order wears her for such a course ("she is worn
     round for it"); the form that follows the bearing does not. That, or the scenario's
     hours for the cutter and the brig, would bring the meeting back.
   - **Two chases, two wears.** On the same cruise two of the book's orders give chase to
     one sail at one tick, each queues a wear, and the second wear begins as the first
     ends and fails a quarter of an hour later ("she would not come round": "by the wind"
     has taken its helm). One wear and one failed evolution too many, harmless to her
     station; the book's, or the chase order's, to mend.
   - **The fore-and-afters hove to forereach.** Kept on their tack as the square-riggers
     are, the schooner makes up to two knots and a quarter and the cutter a knot and a
     half lying to in a twelve-knot breeze, and neither can be brought under a knot and
     a half as the brief's test for the brig requires of her; their tests allow them more.
   - **`weigh` moored.** `weigh` alone weighs the anchor she rides by and leaves her to
     the other, veering its cable; it is refused when that cable cannot reach. `unmoor`
     is still the order that picks up the lee anchor first by the book.

23. From package 37g (2026-10-07): the station's safety, and the deck, the leaving and
   the grant, as spec M4 §11's last bullet and §14 state them and primer 16 tells them.
   Open, for the lead:
   - **The consent brief was made leaner the same day** (the owner's word of 2026-10-07,
     before any model was asked again; the package's second pass). The first two points
     this item opened with are closed by it: the sentence about the handover note in a
     brief is no longer in the consent brief (a station's brief shows it), and the brief
     now says of the deck that "an officer that is paused, or that has been told it is
     silent past its time, gives the deck up to the captain until he gives it back". The
     consent brief keeps the kind of thing a model is asked to agree to; a station's
     particulars are in that station's brief, each said once
     (`tests/test_officer.py::test_what_moved_out_of_the_consent_brief_is_in_the_briefs_of_
     the_stations`), and the brief's *The record* says what brings the question again.
   - **What cannot be undone.** The vocabulary has one order that gives up something of the
     ship's for good, `cut away` (the wreck of a spar that has already carried away), and
     it has been within the officer's own domain since package 37, so that he can clear a
     wreck without waiting for the captain. The general grant therefore keeps back nothing
     in practice today under this head; the rule and the list (`irrevocable` in
     `data/vocabulary.yaml`) stand for the orders to slip or cut a cable when they are
     written. Whether clearing a wreck should want the captain's word is the owner's.
   - **What the general grant keeps back is named whole, in one text**
     (`agent.GENERAL_KEPT_BACK_WORDS`): the port's business, the captain's standing orders,
     a new destination, a chase (the review's list, under "when Milestone 7 comes"), the
     reckoning set by hand (the package's item 18) and the tide allowed in it, sending for
     a person, and anything that cannot be undone. The officer's brief, the grant's own
     line in the log and the sample that gives the grant or the deck say the same words,
     and each is refused in words that say it is kept back and may be allowed by name. The
     tide allowed and sending for a person are the package's reading; the consent brief no
     longer lists any of it.
   - **Reads are counted apart from orders, thirty-two a sampling point**, where the
     brief left "counted apart, or not at all" to the builder: a count keeps a bound on a
     reply that would read without end, and it is twice the orders'.
   - **A standing order the officer writes under the captain's word stays in the book**
     when that word ends, as it did before this package; its orders are checked when it
     is entered and not again when it fires.
   - **The REPL's turn mode does not put the question again after an opt-out**: it says
     in words that the interactive door does. A human at that door meets no consent step
     and is seated again at once.
   - **A station loaded from a save that records no model's name** (the game's own
     scripted station, or a save from before the names were kept) is taken by the first
     model that asks, after its own consent, as before this package.
   - **The way out of danger never brings the pause.** The brief said that used three
     times in a watch it brings the detector's word; it brings the word each third time
     and no pause, since a pause would take the deck from an officer at that moment.
   - Item 11 stands: an act from outside the loop at the stationing tick, before any tick
     has run, is not made by a replay.
24. From the fold-in of m5c-c (2026-10-08; decision 38; `docs/dev/TuningNotes.md`, its
   section). **A platform difference in the merchant passage.** Pinned by 37d to 37f on
   the owner's Windows machine, she comes out two lines longer and anchors in the Bay two
   ticks earlier on Linux (2994 lines against 2992; 115815 against 115817), her cast at
   the Iroise's mark a tick later (90241 against 90240), the mouth of the Goulet and the
   tin sold half a minute sooner (112078 against 112112; 123948 against 123951), and the
   5b schooner is brought up a tick earlier (58689 against 58690), with the schooner never worn and nothing of the
   fold-in's in her log; the frigate's passages agree, and the gate's own build agreed on
   both platforms. Something in those three packages reads a figure the two C
   libraries compute a last digit apart at a threshold the account's rules compare, or
   lists a folder in the file system's order. The pins stand as Linux measures them, where
   the releases run; `ci.yml`'s manual run of the whole suite on both platforms is the
   way to compare. Open: the cause, and whether the rules that compare near-equal figures
   should compare them at a coarser grain (a hundredth of a mile) so that both platforms
   agree by construction. The difference turned up a rule to amend (37e's one rule for
   an observation): at the merchant passage's second noon a sight of two miles and a
   half's doubt, five miles and a half from an account fixed to three cables, is taken
   outright on one platform and weighed on the other, the two being a hair either side
   of the doubts together; the owner's note 5 on game 9 (a poor lunar overriding the
   better account) is the same thing. For the 37e amendments: take an observation
   over the account only when it is the better figure. *Built by package 37j (§13): the
   better figure is believed, and on both platforms such a noon is now weighed, and
   doubted on the far side of the line, the account within a cable of the fix either
   way; the cause of the platform difference itself is still open.* **The helm through the wind.** A chase or a shaped course that
   would turn a square-rigged ship through the wind's wake is worn for
   (`orders.navigation._course_not_laid`); a plain `steer` through it is left as the helm
   has always had it, and a captain who types one from close-hauled will be taken aback.
   Open, for the owner: refused in words that name the wear, or worn without a word.
25. From package 37j (2026-10-09): the account amended (§13, §15 to §17;
   `docs/dev/TuningNotes.md`, its section). Open, for the lead:
   - **Game 9's noon of 16 June cannot be "taken" against an honest account** under the
     rule as amended: taken wants the sight no poorer than the account, and the two are
     then plainly apart only beyond twice their doubts added, at least nine miles; they
     stood five apart. It is doubted against the account the lead kept at a quarter of a
     mile, and weighed by the doubts against an honest one; the forenoon sailed again
     keeps the doubt honest (the truth within twice it at every glass). A lead-kept
     account already four miles out is helped and not cured: casts over the flat sand
     answer within the doubt in the wrong place and are weighed, as in 37e.
   - **The thick 5b passage takes the ground on Black Head** at 56081, after its landfall
     at 53820: the book's "the land" steers S into a south-easterly, "keep her full" bears
     her away and she is taken aback, and her leeway and the ebb set her onto the ledges.
     The track, not the rule (the departure at the truth, each board worked). The book's
     stand-off, or 37k's helm, to rule.
   - **The merchant passage makes no cast at the Iroise's mark**: the course for the
     Passage de l'Iroise is shaped once from nineteen miles off and not again within ten
     of Ushant, and she passes the mark wide by account (an expected failure).
   - **A fix by marks on one hand is as often poorer along the shore as off it**: the
     compass's shared error moves it along the shore, the narrow cut off it; "good to"
     says whichever the figures give.
   - **The log's line of a sighting keeps the mark's true distance and bearing** in its
     data, for the record; the snapshot's reading does not. If the log's data reaches the
     browser, it is a road the proof of §15 does not cover.

## 34. The scoping draft's rulings (record)

The questions put to the owner on 2026-09-29 and the rulings: 1, a real sea with older
data where it can be had, built to grow; 2, both the schooner trading and the frigate
cruising; 3, as recommended but lunars explored, then adopted; 4, the tide explored, then
the harmonic model with tabulated streams and two tides adopted; 5, far detail with
sightings, to be revisited; 6, pressure systems with fronts, seeded from a climatology;
7, the seaway in 5a; 8, three gates. The four studies were adopted as written the same
day and this chapter was written from them.

**The owner's rulings of October 2026 on the stations and the saves** (record; the
decisions log of `docs/DesignProposal.md`, decisions 34 to 36, has them with their
sources). *3 October*: a session may come back to its station unless it left saying it
does not want to; there is no count (package 37b). *5 October*, in answer to the review
of gate 5c's playtests (`docs/playtests/2026-10-05-gate-5c-review/report.md`, section 9):
a save lies in the folder of the build that played it; `you have the deck` and `I have
the deck` do not unseat the officer; a station that was stood down may be taken by the
same model or by another; a general grant keeps back the port's business and the
captain's standing orders, and what the standard of the era would make an unlikely
grant; `take a fix` is an order like any other; no opt-out so far was other than
amicable. *7 October*: a save is exact from its checkpoint, and a replay is promised only
on the build that made it (package 37d); the held-back list of the general grant is
approved for its first version, and it lapses when the officer is fully stood down or the
captain directly countermands it; three ways of leaving, with parity for the officer's
`hand_over` and the captain's `I have the deck` and `stand_down` for the amicable save
and exit; a final opt-out bars the model and not the station, with care for false
positives, and the relief may read the journal of the last holder; the way out of danger
on the officer's own word is kept as proposed (package 37g, which revised the consent
brief once for all of it). *The same day, on reading the revised brief*: it carried too
much of a station's particulars for a consent question, and a leaner brief was approved
as the lead drafted it, to go in before any model was asked again, with the officer's and
the watcher's briefs settled so that they hold what moved out of it (decision 37).
