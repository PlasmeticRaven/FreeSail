# Milestone 5 work packages: contracts between them

Milestone 5 is specified in `docs/TechnicalSpec-M5.md` in three parts with three gates.
Read it whole before your section, then the four studies it was written from
(`docs/design/WeatherSystems.md`, `Navigation1805.md`, `Tides1805.md`, `ChartData.md`;
with `ThreeDimensions.md` and `InwardAndOutward.md`), `docs/agents/README.md` (the
commitments to models, which are requirements), and the working rules of the earlier
milestones (`docs/dev/M3-WorkPackages.md`, `M3b-`, `M4-`), which hold: stay inside your
files, build what the specification says at the size it says, every number names its
source, physics before rules, deterministic, ship's-log voice, run the whole suite and
read the summary line yourself, report in the set order. Packages are scoped for a senior
engineer: leeway in how, and a little beyond the letter where the specification's intent
is served, said so in the report.

Three rules added for this milestone:

- **The world keeps the truth and the captain keeps his account.** No reading gives the
  truth where the period could not have it (position, the tide's hour, a front); the
  viewer never draws it; the tests read it from the world.
- **Every number from a study is checked against the study's own "unverified" list**
  before it becomes a constant; a constant from an unverified figure says so in its
  comment and in `docs/dev/TuningNotes.md`.
- **Parity is structural**, as in milestone 4: a reading in the registry or nowhere.

The owner's ruling (2026-09-29): the heavy packages go to Fable, the lead reviewing as
before; each package is written here when its predecessor has landed and is launched on
the owner's approval, not on the merge.

## Waves, gates and dependencies

```
gate 5a:  wave 1  30 weather systems, the glass and the sky, the scenario's systems, the gate's day as a system
                  30b clearing a wreck, spare spars, the storm mizzen in the viewer (beside 30; from playtest 10)
          wave 2  31 the sea and the ship's motion, windage under bare poles, gate 5a
gate 5b:  wave 3  32 the chart data and the queries, the lookout
          wave 4  33 the reckoning, the sights and the lunar, the captain's chart
          wave 5  34 the tide, grounding and anchoring, gate 5b
gate 5c:  wave 6  35 places, people, ports and nations
          wave 7  36 other sail, the world-order channel, the two scenarios, gate 5c
```

31 needs 30's wind (the sea reads its history). 32 needs nothing of 5a and may start
beside 31 once 30 has landed. 33 needs 32's chart and 30's sky; 34 needs 33's moon. 35
needs 32's places on the chart; 36 needs 35 and 30.

## Package 30: weather systems, the glass and the sky (`freesail/world/weather.py` new; `data/weather/climatology.yaml` new; `freesail/physics/wind.py` for the surface wind as the base, the gust factor by air mass, squalls and the mean-reverting wander; `freesail/core/world.py` and `core/rng.py` for the `weather` stream and the tick; `freesail/world/weather_script.py` and `scenarios.py` for the scenario's `systems` list beside `wind`; `freesail/api/readings.py` for the glass, the tendency, the sky, the weather and the visibility; `freesail/standing/` only if a reading's kind is new to the dialect; `freesail/ui/console.py` and `server.py` and `client/instruments.js` for the glass on the instruments; `data/scenarios/gate-4c-day.yaml` re-expressed; `tools/climatology_check.py` new; `docs/primer/` a section on the glass and the sky; `docs/dev/TuningNotes.md`; `tests/test_weather.py` new, `tests/test_wind.py`, `tests/test_readings.py`, `tests/test_known_truths.py` truths 52 to 55 and 57)

Spec M5 §2, §3, §5; `WeatherSystems.md` §1.3, §2(b), §3, §4, §5 for every number and
its source. Fable.

- **The systems** (§2). A `Weather` object owned by the World: a background pressure per
  month; systems as centres with a velocity, a central anomaly, a radius and, for a low, a
  life curve; a smooth radial profile; pressure at a point as the sum; the geostrophic
  wind from the gradient turned ninety degrees; the surface wind turned inward by
  `SURFACE_TURN_DEG = 15` and scaled by `SURFACE_SCALE = 0.7`, capped in strong
  curvature. Two fronts per low hinged at the centre (a bearing, a length, a width),
  rotating and trailing with the low's motion, occluding when the cold catches the
  warm. The sector of a point (ahead, warm, behind, under a high) and the sector table
  from the study's §1.3: sky, rain, visibility, air mass, and the veer at each front. The
  base wind the physics reads is the surface wind at the ship; `Wind` keeps its gusts and
  wander on top of it. Hooks, inert until 5b: a distance-to-coast the sea breeze and
  coastal fog will read.
- **Seeding** (§2). `climatology.yaml` per month: lows a month, track distribution
  (bearing and closest approach), speeds, central pressures, the high's probability and
  orientation, and the direction shares of the study's 1750 to 1854 row as the check;
  first-pass values from the study, each marked provisional where the study marks it
  unverified. Draws from the world's `weather` stream when a system leaves the box or
  its life ends; nothing else random. `tools/climatology_check.py` runs a thousand months
  and prints the direction shares and gale days by month beside the table; the test
  requires westerly and easterly days within `CLIMATOLOGY_TOLERANCE_PCT = 5` of the
  table in every month.
- **The scenario's `systems`** (§2). Waypoints of position, pressure and time, a radius,
  a low's fronts' initial bearings; followed exactly as `WeatherScript.at` interpolates;
  no draws while a scripted system is present. `wind` waypoints remain; with both, the
  pinned wind wins and the systems give only the sky and the glass. The gate's day
  re-expressed as a low passing well north of Falmouth, the ship in its warm sector, the
  cold front through at 22:00, the ridge by dawn; the glass falling slowly, checking at
  the front, rising fast in the gale. Truths 48 to 51 keep their pinned `wind` form and
  must not move.
- **Gusts, squalls and wander** (§3). The gust factor drawn by air mass from the sector
  (warm 1.10 to 1.20, neutral 1.15 to 1.30, unstable 1.20 to 1.45), the mechanism kept;
  squalls as events of a few minutes in unstable air with a veer of a point or two and
  rain, logged "A squall" notable at their start and their end; the direction's random
  walk made mean-reverting about the base with a spread of 5 to 10 degrees in unstable
  air and less in stable, the wrong docstring corrected; speed wander unchanged. The M4c
  tuning note on the gust factor closed with the reason.
- **Readings** (§5). `the glass` in inches to the hundredth with the ship's noise, absent
  when the scenario gives no glass; `the tendency` over three hours and one hour in the
  period's words, from the ship's own record; `the sky`; `the weather`; `the visibility`
  in the lookout's terms; each with its absent pattern; the dialect reading them for
  nothing (`when the glass is falling fast then shorten sail` is a book's line; a test).
  Log lines at the watch's changes and when the sky or the weather changes; the roll-up
  summing the glass's fall and the rain by the hour. The instruments panel shows the
  glass. No line anywhere names a front, a centre, an isobar or a hectopascal (truth 57
  is a grep over a day's log and every reading's words).
- **The primer** gains a section on the glass and the sky in the period's lore (FitzRoy's
  and Luce's rules as the study quotes them, with their dates), and what a captain of
  1805 did not know.
- **Tests**: the systems' arithmetic (a single low's wind field against the gradient rule;
  the fronts' geometry; the sector table); truth 52 on the gate's day as a system (the
  order of back, veer, steady, squall, rise); truth 53 by the climatology tool's numbers;
  truth 54 on gusts by air mass and squalls; truth 55 on replay and on the pinned wind
  winning; truth 57; the readings on both ships; a scenario file with both forms.
- **Report**: the final suite line; every constant with its source and whether the source
  was verified; the climatology tool's table for January, June and October; what moved
  in the tuning notes; anything from the study's unverified list that the build could
  check and did.

Not in 30: the sea state and the motion (31), temperature, the sea breeze and coastal fog
beyond their hooks, CLIWOC, replayed real tracks.

## Package 30b: clearing a wreck, spare spars, the storm mizzen in the viewer, two result strings (`data/evolutions/clear_wreck.yaml` new and `shift_spar.yaml` new; `freesail/evolutions/scripts.py` or the step list, `freesail/orders/verbs.py`, `data/vocabulary.yaml`, `freesail/orders/complete.py`; `freesail/ship/parts.py` and `loader.py` for spare spars, `data/ships/frigate-36.yaml` and `topsail-schooner.yaml` and `tools/gen_ships.py` for their spare spars; `client/projection.js` and `tests/test_view_geometry.py` for the storm mizzen; `freesail/agents/harness.py` for the two result strings; `docs/primer/03-making-and-shortening-sail.md`; `tests/test_evolutions.py` or the rig tests, `tests/test_orders.py`, `tests/test_agents.py`)

From playtest 10 (`docs/playtests/2026-09-29-post-4c-qwen-watcher/notes.md`, findings 1 to
4) and the owner's report of the storm mizzen. Opus. Runs beside package 30; it touches
nothing 30 touches (30 has the weather, the wind, the readings and the scenario file; 30b
has the rig, the viewer and two harness strings). Started 2026-09-29 on the owner's word.

1. **Clearing a wreck.** `cut away <the part>` (also `clear away the wreck of <the part>`,
   `clear away <the part>`, `clear the wreck`) for a carried-away spar or a wrecked sail:
   an evolution with hands and time in the M3 form and with a period source (Luce 1884
   on clearing wreck after a spar goes; Falconer 1780 "cut away"), which unbends and
   sends down what can be saved and cuts adrift what cannot, the sail to the sail room
   if it is whole and over the side if it is not, the spar's remains sent down or cut
   adrift, the standing and running rigging that went with it cleared; the log says what
   was saved and what went over the side. A wrecked sail may also be `unbend`-ed and a
   wrecked spar `send down`-ed directly where the existing evolutions can do it; today
   every verb refuses a wrecked part in words, so the refusals become the work. Aground
   or in a seaway the times are what the crew factor makes them. The part graph keeps the
   wreck's consequences (a boom gone means no studding sail on it) until a spar replaces
   it.
2. **Spare spars.** Ships carry spare spars as they carry spare sails (`parts.py`: a store
   by class, with counts, saved with the game): the frigate a spare topmast, spare
   topgallant masts, spare yards and studding-sail booms, the schooner a spare topmast and
   booms; the numbers from Steel 1794 or Luce 1884 on the boats and booms a ship carried,
   with the source in the file's comment, and generated by the ship tool so the cutter
   and the brig get theirs. `shift the <spar>` (also `shift ... for a spare`) replaces a
   carried-away spar with a spare of its class by an evolution with hands and time,
   after which the sail that belongs on it can be bent again; with no spare aboard it is
   refused in words ("No spare studding-sail boom aboard; the dockyard must supply one."),
   which milestone 5's port will answer. `the booms` (or `the spare spars`) as a console
   and browser query in the form of `the sail room`, and later a paper (spec M5 §22).
3. **The storm mizzen in the viewer.** A jib-headed sail on a stay that has no run to
   another spar (`storm_mizzen.stay`, `of: mizzen.mast`, the vertical stay under the
   mizzen trestle-trees) is not drawn. The projection places such a sail from its file's
   geometry (its luff along the stay from the mast head down to its tack at `x_m`, its
   foot toward the taffrail as the file's comment has it) and draws it as it draws the
   storm staysails. A geometry test in `test_view_geometry.py`.
4. **Two result strings.** `answer` with no question pending returns "Heard; your words
   are in the log, though no question was put." (finding 3). The sample that ends a
   stand-by says which calls before the stand-by in the same reply ran (a journal note,
   a library read), in one line (finding 4). Tests with the fake.

Out: the wreck's effect on the ship's motion and steering beyond what the part graph
already does; the dockyard (5c); the layering faults of the viewer (deferred).
Deliverables: the code and tests, the primer's note on clearing wreck and shifting a
spar, and a report for the lead naming the sources for the spare-spar counts.

## Package 31: the sea and the ship's motion (outline; written when 30 has landed)

Spec M5 §4, §5 (the sea's words), the M4 open item 7 (windage under bare poles), truth
56, the gate 5a cut. Fable.

## Packages 32 to 36 (outline; written in turn)

As spec M5 §31: 32 the chart data, the queries and the lookout (§9 to §12, truth 65;
Fable, the hand work reviewed by the lead against the sources); 33 the reckoning, the
sights and the lunar, the captain's chart (§13 to §15, §17, truths 58 to 61; Fable); 34
the tide, grounding and anchoring, gate 5b (§16, §18, truths 62 to 64 and 66; Fable);
35 places, people, ports and nations, with the cutter as a ship file for the pilot (§22 to
§24, truths 68 to 70; Opus); 36 other sail, the world-order channel, the brig as a ship
file, the two scenarios, gate 5c (§25 to §27, truths 67, 71, 72; Fable). The two new
vessels are the first catalogue entries and the test of pillar 2 (owner, 2026-09-29): no
engine change, the running bowsprit the one generator addition expected, every order that
fails on either a fault in the grammar to fix there.

## Integration (the lead)

The lead reviews each package against the studies and the spec, merges each wave, runs
the suite, cuts each gate, records the owner's verdicts, and writes the decisions log
entries. The lead takes a watch at gate 5c (spec §29).
