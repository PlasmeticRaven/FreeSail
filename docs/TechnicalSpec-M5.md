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
drift, and moving the run would move every truth under sail. It is the owner's ruling at
gate 5a with two others (the pinned form and the air-mass rule; the squalls' cost in
canvas on the day under systems). The wave-growth constants derive from the
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

### 12. The lookout (`freesail/world/lookout.py`)

The sighting model is the lookout's reading: what is in sight, its bearing by compass
and its distance by estimation, in the log's words ("The Lizard bearing N by E, distant
four leagues"; "A light on the larboard bow"; the coastal views of Serres for a headland's
look). A light is seen at night by its own range and date; a castle or a tower by day. In
5c the same model sights sail. The lookout is a station in the sense of decision 24's last
line (a small model could hold it later); in 5b it is the world's own voice at routine
severity, notable for a landfall or a danger.

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
is. **Exposure by the period's means only**: no tide readout, ever; the establishment table
by handle; the almanac's moon; the lead against the chart's depth; the landmark's state
(the Black Rock shows at half tide); the ship riding to the tide at anchor, the cable
slack at the turn; the set allowed for in the traverse. The primer carries the rule of 48
minutes and the headland table. The rule of twelfths is not put in an 1805 mouth (T §2).

### 17. The captain's chart and the viewer (`client/map.js` becomes the chart)

The viewer's map becomes the captain's chart: the coast and the features as his chart of
1804 has them (a longitude error of the period's chart, a pilot's words where the chart
has no sounding), the reckoned position and its ellipse, the track by account, the noon
positions, the bearings taken, the soundings with their ground. The true position is not
in the snapshot the client receives (`api/queries.py` gives the reckoning; the truth is in
the save and the tests only). A `--casual` display of the truth is a later option and a
display choice, as the proposal says; nothing in the simulation changes for it.

### 18. Grounding and anchoring (`freesail/world/ground.py`, `evolutions/anchor_*.yaml`)

Touching is an event with speed, heel, tide and bottom type; the consequences are the
hull's (a stop, a strain on the masts, a leak by the bottom's kind and the speed) and the
log's, and getting off is the tide's business or the anchor's (a kedge is later).
`come to an anchor` and `weigh` are evolutions in the M3 form with hands and time (Steel
1794 vol. II: stemming the tide; Lever 1808); at anchor the ship rides to the tide and the
wind, the log says how, and the cable's scope against the depth is a check the evolution
makes. The port's mooring is 5c's.

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
- **33b. The chronometer, the moon and the lunar** (5b §14's rest; truths 60 and 61; in
  gate 5c's set by decision 29). Fable.
- **34. The tide, grounding and anchoring** (5b §16, §18; truths 62 to 64, 66; in gate
  5c's set by decision 29). Fable.
- **35. Places, people, ports and nations** (5c §22 to §24; the pilot boarding from 32b's
  cutter; truths 68 to 70). Fable (the owner's ruling, 2026-09-30; the draft said Opus).
- **36. Other sail and the world-order channel** (5c §25 to §27; 32b's brig at far detail
  with her merchant description; the two scenarios; truths 67, 71, 72; gate 5c cut). Fable.
- **37. The officer of the watch** (§29; written when 36 lands; the lead's watch follows
  it and gate 5c's verdict waits on that watch). Fable.

Each package's brief is written in `docs/dev/M5-WorkPackages.md` when its predecessor
has landed, in the form the M4 packages took.

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
   the lights' dates.
4. The lunar's day count per lunation and the 1805 clearing time (N) are the study's
   estimates; the game's constants say so.
5. Whether the schooner's file offers `shift the mainsail for the storm trysail`
   (playtest 8), for the M4 follow-ups list.
6. A station for the lookout (decision 24's last line), when a small model is tried at it.
7. The sail room in the browser (owner, playtest 8) waits for §22's places and papers;
   until then the console's query stands and the browser has none.
8. From package 31: the wave-growth sources (Pierson–Moskowitz, Bretschneider, JONSWAP,
   the Weiss and Rayleigh figures) to be read from a page; the head-sea resistance and the
   roll damping as judgements; the day under systems loses the mizzen topsail to a
   65-knot squall (the third gate 5a ruling).
9. From package 30: a frontal trough so the glass checks at the cold front; the north
   quarter's share; the pinned form and the air-mass rule (the gate 5a ruling); a
   `gate-5a-day.yaml` with the day under systems alone, for the gate cut (package 31).
12. **The physics of staying** (from package 32b's finding and the owner's playtest of the frigate, 2026-09-30; the lead's probe the same day). Not the headsails: the schooner gets through in four and a half minutes by a sternboard and the cutter dies seven degrees short of the wind, because the turn is the frigate's (the rudder's force falls with the speed squared and the yaw damping constants were tuned on one hull, so a fifty-foot cutter turns at a degree and a third a second where she should spin), and the miss-stays rule is one number for every vessel (0.8 knots or 180 seconds before her head is through). When it fires, `TackScript._miss_stays` squares every yard in one tick with no hands and no time and orders the helm back to the old heading, which the owner saw as the yards jumping square and the ship hanging head to wind with no way for the rudder to bite. The package to write: yaw that scales with the vessel (rudder area and lever, damping from the lateral plane, the radius of gyration), checked by a turning truth per ship (Luce 1884 Appendix L for the frigate; the type's reputation for the cutter); a miss-stays rule that reads the vessel and allows Luce's recovery before it gives up (she hangs: the helm reversed as she gathers sternway, the head yards kept aback to box her head off, the after yards to the new tack once through, the headsail sheets held to windward as a state for the small vessels and for heaving to); squaring the yards on a true miss as a brace with hands and time, never a jump; and the schooner's, cutter's and brig's tacks as truths beside truth 10. Also from 32b: a per-sail pointing from the file's own geometry (aspect ratio, the sheeting floor from the gear, leeway from the lateral plane) in place of a per-rig factor, which the owner declined; truth 73 amended to "as close as the schooner or closer" (owner, 2026-09-30). The browser draws a running bowsprit at the length in the ship graph fetched once and does not redraw a reef until reload (the snapshot carries no spar length, `api/queries.py`). *Landed in package 32e (2026-09-30):* the yaw damping in the standard form (∝ A L² and A L³), the rudder's lift slope from the blade's aspect ratio, the miss-stays rule read from the vessel (her way gone under a quarter of her speed at "helm's a-lee" or a length a minute, for five seconds), Luce's recovery when she hangs within a point of the wind (the helm shifted with sternway by the helmsman, the head yards aback, the head sheets held to windward, the boom hauled over to windward), the squaring on a true miss as a brace with hands and time, and a turning truth and a tack truth for each of the four ships (`docs/dev/TuningNotes.md`, package 32e). Appendix L proved to be steamship trials only; the frigate's circle stays a judgement band. The per-sail pointing and the browser's bowsprit remain open.
13. **Sheets and trim are two records of one thing** (the owner's playtest, 2026-09-30). A fore-and-aft sail's trim is a number on the sail (`sheet_angle`), moved for free every tick by `evolutions/trim.py`'s `tend_sheets` (the cold review's finding 3) and by `trim the <sail>`; its sheet is a line with a state (belayed, free, parted). Let the main sheet fly and the line is free while the angle stays where it was; order `trim the mainsail` afterwards and the angle moves and the line stays free, so the order reports work and the sail does not draw. The fix is one truth: the sheet holds the trim. A sheet's length hauled sets the sail's angle by the boom's geometry (the generator knows the boom, the horse and the traveller); `haul`, `ease a fathom`, `let fly` and `belay` are level-0 orders on the line that move that length with hands; `trim the <sail>` (to the wind, or to a bearing) is an evolution that works the sheet to the length the wanted angle needs, hauling a sheet that was let fly as part of the trim, with hands and time as a brace has; the standing book's `trim` reaches the same evolution; and the free tending is retired, the afterguard tending sheets as routine work at a cadence the book or the watch orders. A sheet let fly then has no load and the sail flogs, as now; a sheet belayed carries the sail's load into the strain model by its length and angle. This moves the helmsman's `full and by`, which was tuned around free tending, and truths that read it; a physics and evolutions package with open item 12, before gate 5b. *Landed in package 32e (2026-09-30):* the sheet holds the trim (`evolutions/trim.py`'s geometry from the boom, the horse and the purchase the generator writes, or a loose-footed sail's clew); `haul`, `ease a fathom`, `let fly`, `belay`, `to windward` and `draw` on the line; `trim the <sail>` as `trim_gaff_sheet` and `trim_jib_sheet` with hands and time, reached by `trim sails`, the book and the manoeuvres; a sheet let fly flogs and carries no load, a belayed boom sheet carries the sail's moment by its lever; the free tending retired and the starter book tending the sheets every glass. The pointing truths did not move, so the helmsman's margin stands. Not done: a sheet parting in a gybe wants the boom's swing on a timeline, which the quasi-static load does not give.
11. From package 31c: a door act recorded at the stationing tick, before any tick has run, is not made by a replay (`restore()` then `start()` does not play door acts); and `a wind shift` as a stand-by event reads the mean wind while the log's own `wind.shift` line reads the instant wind at two points, two definitions to unify when `core/world.py` is next open.
10. The lead at a station (§29): the consent question put to the lead's own weights inside
   the harness before the gate, the record kept as any other; and, for M6, the owner's
   wish that the lead take an officer's or a captain's station once they exist.

## 34. The scoping draft's rulings (record)

The questions put to the owner on 2026-09-29 and the rulings: 1, a real sea with older
data where it can be had, built to grow; 2, both the schooner trading and the frigate
cruising; 3, as recommended but lunars explored, then adopted; 4, the tide explored, then
the harmonic model with tabulated streams and two tides adopted; 5, far detail with
sightings, to be revisited; 6, pressure systems with fronts, seeded from a climatology;
7, the seaway in 5a; 8, three gates. The four studies were adopted as written the same
day and this chapter was written from them.
