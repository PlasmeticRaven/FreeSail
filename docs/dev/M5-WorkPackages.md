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
                  31b all hands in parallel, the rig's repairs, the pinned form under the air-mass rule (after gate 5a; playtest 11)
                  31c the watcher's watch: the sample's delta, the door's wait, weather events, tell/ask in the book (beside 31b)
gate 5b:  wave 3  32 the chart data and the queries, the lookout
                  32b the cutter and the brig as ship files, the orders' grammar across four ships (beside 32; pulled forward from 35 and 36, owner 2026-09-30)
                  32c the suite in two tiers, the days built once, a Windows job (Opus; landed 2026-10-01; the Windows job proven on GitHub's runner at the push)
                  32d the freesail command, the settings file and the setup step, written for any machine (Opus; after 33c and 33d; one test cycle on the owner's machine)
          wave 4  33a the reckoning, the noon sight, the captain's chart, the checkpoint save, gate 5b
                  32e staying and sheets: the fore-and-aft rig at the small vessels' scale (spec open items 12 and 13; before gate 5b; launched 2026-09-30)
                  (landed 2026-09-30: 31b, 31c, 32, 32b)
gate 5c:  wave 5  33b the chronometer, the moon, the lunar and the azimuth; the captain's chart in his hands (Fable; landed 2026-10-01)
                  33c the passage's words: readings at the prompt, the aliases, the starter book as a choice (Opus; landed 2026-10-01)
                  33d the browser's shelf: completion, the library pane, the clock on a station, zoom and pan (Opus; landed 2026-10-01)
                  34 the tide, grounding and anchoring, as Luce has it (Fable; landed 2026-10-02)
                  32f the launcher page: the browser's front door with the game's options (Opus; after 33d and 32d; owner, 2026-10-01)
          wave 6  35 places, people, ports and nations; the pilot boarding from the cutter (Fable; written 2026-10-02 for the owner's review)
          wave 7  36 other sail, the world-order channel, the two scenarios, gate 5c cut
          wave 8  37 the officer of the watch; the lead's watch beside other models' (an Opus 5.5 watch, and a local model on the cutter: owner, 2026-10-01); the 5c verdict
```

31 needs 30's wind (the sea reads its history). 32 needs nothing of 5a and may start
beside 31 once 30 has landed. 33a needs 32's chart and 30's sky; 33b needs 33a's
reckoning; 34 needs 33b's moon. 35 needs 32's places on the chart; 36 needs 35 and 30; 37
needs 36, since the officer is built with the world in place (owner, 2026-09-30). **Gates
lag the work** (owner, 2026-09-30, decision 29): a package is written as its predecessor
lands and launched on the owner's word whether or not the previous gate has been run; a
gate is cut when its last package lands, for the owner to run when they can, and its
rulings feed a follow-up package as 5a's fed 31b. 32b needs nothing of 5a or 5b: it is
data work on the generator and the ship files, and any engine change it finds is a fault
reported, not a feature built.

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

## Package 31: the sea and the ship's motion, windage under bare poles, gate 5a (`freesail/world/sea.py` new; `freesail/physics/motion.py` new; `freesail/physics/integrate.py` and the hull's resistance and windage wherever they live, for the speed lost in a head sea and the windage under bare poles; `freesail/physics/strain.py` for the motion's load; `freesail/crew/hands.py` for the crew factor aloft in a seaway; `freesail/api/readings.py` for `the sea` and `the motion`; `freesail/core/world.py` for the sea's tick and the glass's pumping; `freesail/core/events.py` for the sea in the roll-up; `client/instruments.js`; `data/scenarios/gate-5a-day.yaml` new (the day under systems alone); `docs/primer/09-the-glass-and-the-sky.md` for the sea's words; `docs/gates/gate-m5a.md`; `docs/dev/TuningNotes.md`; `tests/test_sea.py` new, `tests/test_known_truths.py` truth 56 and the pace truth, `tests/test_strain.py`, `tests/test_hands.py`)

Spec M5 §4, §5 (the sea's words), §6 truth 56, §7 gate 5a; `ThreeDimensions.md` (the
seaway as reduced motions, never a physics engine); spec M4 §24 item 7 (windage under
bare poles: the frigate makes three knots under bare poles in fifteen knots dead astern
where a few tenths would be expected; to be measured against Luce on drift under bare
poles and tuned). Fable. Written 2026-09-29 when package 30 landed; launched on the
owner's approval.

- **The sea state** (§4). A field at the ship (`Sea`): a significant wave height and a
  period from the wind's recent history, a first-order lag on the ten-minute mean
  (`SEA_BUILD_HOURS`, `SEA_DECAY_HOURS`, the period from the height by the open-sea
  relation, each with a source in the tuning notes: the WMO or Bretschneider relations
  for a fetch-unlimited sea at the wind's speed and duration, cited and marked where a
  figure is a judgement); a swell with its own direction, height and period that a low
  leaves behind (from the systems' history: the strongest wind of the last day and its
  direction, decaying over a day); the combined sea in the period's words ("a smooth
  sea", "a short chopping sea", "a heavy sea", "a long swell from the westward", "a
  confused sea" when wind and swell cross), never the Douglas numbers. Ticked once a
  simulated minute. Deterministic; saved and replayed.
- **The motion** (§4). Three reduced quantities (`Motion`): the roll amplitude and
  period from the sea on the beam against the ship's stability (the righting the hull
  already has, or a stated proxy), pitch from the sea ahead, heave; each a number with a
  time constant, no integration of a six-degree body. In words in `the motion` ("rolling
  heavily", "pitching into it", "easy"). Nothing here moves the ship on the plane; it is
  what the hands and the gear feel.
- **The consequences** (§4), each one line where it lands: the crew factor aloft falls
  with the roll (`hands.crew_factor`, a table by roll amplitude with a source; a reef in a
  heavy sea takes half as long again, truth 56); the strain model reads the motion as an
  extra load on spars and gear (a factor on the wind's load by the roll and pitch; the
  strain truths' numbers must not move in a smooth sea); the hull loses speed in a head
  sea by a small factor (added resistance, a judgement bounded by the sources and
  recorded); the glass pumps by a hundredth or two in a seaway (`GLASS_NOISE_IN` scaled by
  the motion); the lookout's horizon is what the height of eye and the swell allow (a
  number 5b's sighting reads; inert until then); the noon sight's and the lunar's error
  hooks (numbers 5b's sights read; inert until then).
- **Windage under bare poles** (M4 open item 7). Measure the frigate under bare poles in
  fifteen knots dead astern; compare with Luce on drift under bare poles and with the
  hull and rig windage the sail model already carries; tune the hull's and the rig's
  windage so the drift is a few tenths of a knot, with the reason in the tuning notes;
  every truth that depends on speed under sail must not move (if one does, the windage
  is in the wrong term).
- **Readings and lines** (§5): `the sea` and `the motion` in the registry with their
  words and absent patterns; the dialect reads them (`when the sea is heavy then ...`);
  a log line when the sea's words change; the roll-up says the sea by the hour; the
  instruments panel shows the sea; the console's `state` has it. The primer's chapter 9
  gains the sea's words with their sources (Luce 1884 and the period logs' phrases).
- **The gate's day under systems alone**: `data/scenarios/gate-5a-day.yaml`, the
  re-expressed day of package 30 without the pinned `wind`, sailed by the starter
  routines; its ticks and digest recorded as truth constants of their own (the M4
  constants untouched); the pace truth for gate 5a measured on it (truth 51's floor).
- **Gate 5a** (§7): `docs/gates/gate-m5a.md` in the form of the M4 gates, for the owner
  to run on the console or the browser: the day under a system with the glass read at
  every watch change and the sky at every bell; the squall in the middle watch; the sea's
  words through the gale and the next forenoon; the watcher through the local runner
  asked what the glass says; a January day and a July day from the climatology at seed 7
  with the tool's table; the fake watcher's day replayed to the same digest; `--load` of
  a save with a station, carried from gate 4c; the ruling asked of the owner on the
  pinned form and the air-mass rule (spec §3 as built). Expected numbers from seed 7.
- **Tests**: the sea's build and decay against the relations; the swell left by a
  passing low; the words at each height; the motion's three numbers on the beam, ahead
  and astern; each consequence in isolation (a reef in a smooth and a heavy sea; the
  strain in a smooth sea unchanged; the head-sea loss); windage under bare poles before
  and after; truth 56; the day under systems replayed; the pace.
- **Report**: the final suite line; every constant with its source and whether it was
  verified; the windage before and after with Luce's figure; what moved in the tuning
  notes; the day-under-systems constants; anything you could not do and why.

Not in 31: pitch and roll moving the ship on the plane, a six-degree body, wave-by-wave
motion, the sea breeze and coastal fog, anything of the chart.

## Package 31b: all hands manned in parallel, the ship's cost, the rig's repairs, the pinned form under the air-mass rule (`freesail/crew/hands.py` and `evolutions/runner.py` for the party bound and the parallel manning of a group; `data/evolutions/*.yaml` for each all-hands sail evolution's party (`reef_square`, `furl_all`, `loose_sails_to_dry`; the masts' and the manoeuvres' `hands: all` unchanged); `data/standing_orders/starter.orders` and `data/scenarios/gate-4c-day.orders` if the heavy-weather routine's order of work changes; `data/evolutions/reeve_line.yaml` new and `freesail/orders/verbs.py`, `data/vocabulary.yaml` for `reeve`/`splice`; `freesail/orders/verbs.py` for the brace line with yards sent down; `freesail/physics/wind.py`, `core/world.py`, `world/weather_script.py` for the pinned form under the air-mass rule; `docs/primer/03-making-and-shortening-sail.md`, `07-a-first-passage.md` and `09-the-glass-and-the-sky.md`; `docs/TechnicalSpec-M3.md` §3.2 and spec M5 §3; `docs/dev/TuningNotes.md`; `tests/test_hands.py`, `tests/test_known_truths.py` (truths 18, 19, 20, 48 to 51, 56 and the day-under-systems constants as they move), `tests/test_weather.py`, `tests/test_evolutions.py`)

From gate 5a's rulings (decision 28) and playtest 11's findings 7 to 11 and 14
(`docs/playtests/2026-09-29-gate-5a-opus-5.5-watcher/notes.md`). Fable. Written 2026-09-30;
launched on the owner's approval. Runs beside 31c (the harness), which touches none of
these files; before 32 if the owner prefers, since 32 does not depend on it.

1. **All hands manned in parallel, with a bound on any one job** (finding 14; ruling 3).
   Today an all-hands sail evolution takes every idle hand (package 29b's pool rule), so
   "reef the topsails" put a hundred and fifty hands on the fore topsail while the main and
   the mizzen waited in turn, and the crew factor's numbers term never rewards hands beyond
   the party. The change: each all-hands *sail* evolution names its useful party per sail
   (`crew: {hands: all, party: N}`; the reef of a frigate's topsail some forty aloft and on
   the yard and the rest at the halyards and reef tackles on deck, from Luce 1884 ch. XXIII
   'Reefing Topsails' and the watch bill's stations, the number with its source); a call
   for all hands still turns the watch below up, and a group order's jobs are manned
   together, each up to its party, in book order, the surplus to the next job and then to
   whatever else waits for hands; more hands up to the party are faster (the numbers term
   as it is), beyond it no faster. The manoeuvres and the masts (`hands: all` scripts)
   keep taking everyone. Truth 18 (plain sail with all hands) and truth 19 do not move;
   the gate's day under systems is re-measured (three topsails reefed together, the
   close reefs likely in before the squall) and its constants re-pinned with the reasons;
   truth 56's ratio holds by construction. Spec M3 §3.2 gains the rule in a paragraph.
2. **The heavy-weather routine's order of work** (finding 10). With item 1 the close reef
   and the send-down share the hands; measure whether the book's order (send down, take in,
   bend, close reef) still leaves the topsails unreefed at the squall on the gate's day,
   and if it does, put the close reef first in the starter book and say why in the primer
   ("the order of an order's clauses is the order of the work" as a sentence in chapter 7).
   The primer also gains one line on sails taken in staying in the gear (finding 11).
3. **Parted running rigging is reeved afresh** (finding 7). `reeve a new <line>` (also
   `reeve the <line> afresh`, `splice the <line>`) as an evolution with hands and time and a
   source (Lever 1808 on reeving running rigging; Luce on splicing), the sail it serves
   refused for setting or sheeting home while the line is parted (the inconsistency the
   model saw, a sail sheeted with a parted sheet, closed), the spare cordage from stores
   counted as the spare sails are. Refusals in words.
4. **The brace line with yards sent down** (finding 8): "Braced six yards to the wind; the
   topgallant and royal yards are on deck." and no "Not ..." list.
5. **The primer must not narrate the gate's day** (finding 9): chapter 9's "Where the
   weather comes from" rewritten around a typical passing low in general terms, with no
   hour-by-hour of any scenario; the scenario's name in the log's first line stays.
6. **The pinned form under the air-mass rule** (ruling 1). A fixed or pinned wind takes
   the air-mass gust rule, the squalls and the reverting wander as the systems do, with a
   neutral air mass unless the scenario says; the milestone 2 draws retire. Truths 48 to
   51's constants and the day digest are re-measured and re-pinned with the reasons
   (`GATE_DAY_*`, truth 50's counts), and every other truth's numbers checked: a truth that
   moves by more than its own tolerance says why in the tuning notes. If it cannot be done
   cleanly (a truth that depends on the old draws' shape), stop, say which, and leave both
   forms with a note, as the owner allowed.
7. **Tests**: the party bound and the parallel manning (three topsails together, the
   surplus to a fourth job, no job over its party); the day under systems and the pinned
   day re-measured; `reeve`; the brace line; the primer's chapter 9 free of the day's
   hours (a test that greps for its times); the pinned form's gusts within 1.3 outside a
   squall.
8. **Report**: the suite's last line; every constant that moved, old and new, with its
   reason; the day under systems' new cost in canvas and whether the close reefs were in
   before the squall; the parties per evolution with their sources; anything not done.

## Package 31c: the watcher's watch (`freesail/agents/harness.py` for the sample's delta, the weather events, `read_log`'s default, the journal while standing by, a bell during a call, the release line; `freesail/agents/tools.py` and `agent.py` for the events' words and the brief; `freesail/agents/mcp_server.py` for the wait under the client's limit; `freesail/api/readings.py` `EVENTS`; `freesail/standing/grammar.py`, `rules.py` and `freesail/orders/*` for `tell`/`ask the <station>` inside a standing order; `docs/agents/Harness.md`, `ConsentBrief.md` only if a sentence bears on it; `tests/test_agents.py`, `tests/test_mcp_server.py`, `tests/test_standing.py`, `tests/test_tell.py`)

From playtest 11's findings 1 to 6 and 12 to 13 (`docs/playtests/2026-09-29-gate-5a-opus-5.5-watcher/notes.md`)
and the owner's ruling of 2026-09-30. Opus. Written 2026-09-30; launched on the owner's
approval; runs beside 31b and touches none of its files.

1. **A sample carries only what changed** (finding 1; spec M4 §24 item 9). The first
   sample of a station carries the full readings; every later one the readings that
   changed since the model's last sample, in the same words, plus a compact sail line
   ("plain sail and the royals set; all studdingsails furled; storm canvas unbent") in
   place of the thirty sail rows, the full rows on request through the readings tool;
   samples bundled into one open turn share one copy of what is common. The parity rule
   holds: nothing is withheld that the captain has, only not repeated. Measured in the
   report: the tokens of the gate's day's samples before and after.
2. **The MCP door's wait fits under the client's limit** (finding 2). The bridge's held
   call defaults to `MCP_WAIT_S = 200` (under the Claude Desktop client's four minutes, the
   study of the owner's sessions), re-issued cleanly by the model with an honest interim
   digest as 28c built it; `--wait` still overrides; `Harness.md` says why.
3. **Weather events to stand by for** (finding 3): `a wind shift` (a point or more), `the
   glass falling fast`, `the glass turning`, `the sea getting up` (its words changing
   upward), `a change in the sky`, `a squall` (already there), in `EVENTS` with the log
   kinds they match, in the tool's description and the brief's list; parity: the dialect
   gets the same events for nothing where it lacks them.
4. **Standing orders can `tell` and `ask` a station** (finding 13; the owner's first
   note): the station verbs allowed after `then`, resolved at give time to a station that
   exists or refused in words ("there is no lookout aboard yet"), delivered as a word or a
   question as the captain's own would be, with the standing order named as the speaker
   in the log line ("By standing order 'sea': the captain to the watcher: ...").
5. **Three small gaps** (findings 4, 5, 6): `read_log` with no `since_tick` defaults to
   the model's last sample; the journal is allowed while standing by (it changes nothing
   in the game; the stand-by continues); a bell or event that falls while a call is in
   flight is delivered when the call returns, not skipped.
6. **The release line's full stop** (finding 12): no second stop after a reason ending in
   one.
7. **The unattended wait is counted in real minutes only** (the cold review's one bug,
   `docs/design/ColdReview-2026-09-30.md` §2.4 item 1; the owner's ruling, 2026-09-30,
   folded in here). Today a paused model is stood down when a watch of *ship's* time has
   passed unanswered (`harness.py`, the tick path under `WELFARE_UNATTENDED_BOUND_S`),
   which at 300x is under a minute of real time, and the browser server never calls the
   driver's real-minutes check (`check_unattended` runs from the console's loop only).
   The change: the ship's-time stand-down goes; the only bound is `WELFARE_UNATTENDED_REAL_S`
   (ten real minutes) on the driver's monotonic clock, and every driver calls
   `check_unattended` (the server's tick loop, the console as now, the REPL as fits its
   lockstep); the stand-down stays an act from outside the loop (`door_act`) recorded at
   its tick, so a replay makes it at the same moment as every other outside stop. The
   pause itself is unchanged (a nudge, then the pause with the human asked). Words:
   `ConsentBrief.md`'s "within a watch of ship's time or ten real minutes, whichever
   comes first" becomes ten real minutes however fast the ship's clock runs (this changes
   the brief's hash; say so in the report), `Harness.md` §11 likewise, the harness's
   docstrings, and the REPL's `--max-ticks` default named from `R.INTERVALS` rather than
   the retired constant. Tests: with the fake, a paused watcher through a day at 300x
   with no answer is not stood down; the injected clock crossing ten minutes stands it
   down; the server's loop calls the check (the app fixture, a fake monotonic clock);
   the stand-down replays at its tick.
8. **Tests** with the fake for each; `test_mcp_server.py` for the wait; `test_standing.py`
   for the station verbs; the parity test extended to the delta (what the captain has, the
   model can get).
9. **Report**: the suite's last line; the sample sizes before and after on the gate's day;
   the events' words as built; the unattended bound's tests; anything not done.

## Package 32: the geographic frame, the chart data, the queries and the lookout (`freesail/world/geo.py` new; `freesail/world/chart.py` new; `freesail/world/lookout.py` new; `tools/build_charts.py` new; `data/charts/` new (`manifest.yaml`, `tiles/`, `coast/`, `features/`, `overrides/`); `freesail/core/world.py` and `freesail/world/scenarios.py` for the position and the chart region; `freesail/world/weather.py` for the coast-distance hook (the sea breeze and coastal fog it enables); `freesail/api/readings.py` for `what is in sight`, `the depth of water` (the chart's, distinct from the lead's cast which is 33's), `the land`; `freesail/api/queries.py` and `client/map.js` for the chart drawn under the track (the coast and the features, never the truth's soundings as a grid); `docs/references/` for the chart sources' licence texts and a `Charts.md`; `docs/dev/TuningNotes.md`; `tests/test_geo.py`, `tests/test_chart.py`, `tests/test_lookout.py` new, `tests/test_known_truths.py` truth 65)

Spec M5 §9 to §12, §30; `ChartData.md` whole (§2 the sources and their licences, §3 the
period surveys and how to read a sounding, §4 the pilots, §5 the data model, the levels,
the disk, the build and the queries, §6 the recommendation, §7 the unverified list, which
is binding: each item is checked from a browser when this package is built and the result
recorded in the manifest or the study). Fable, with the hand work (the four period patches
and the feature list) reviewed by the lead against the sources. Written 2026-09-30 when
package 31 landed; launched on the owner's approval. Package 33 needs this package's
chart; package 35's places sit on it.

- **The geographic frame** (§9). Latitude and longitude as the world frame; the ship's
  motion in metres in her local frame converted at the end of each tick; `Scenario.position`
  in place of the bare latitude the sun used, which now reads the ship's; `ship_x`/`ship_y`
  kept for the flat-plane tests and truths, a scenario with no chart region being the
  plane it was (every M4 and 5a constant unchanged; a test). Distances in the log in
  miles, leagues and cables; positions in degrees and minutes when the game says them at
  all (the truth is never said to the captain; 33 gives him his reckoning).
- **The chart data** (§10, C §5). The files as C §5.2: `manifest.yaml` (regions, levels,
  every source with its licence text, attribution line, URL, retrieval date and checksum;
  the build's version hash), `tiles/<level>/<lat>_<lon>.npz` (int16 decimetres relative to
  chart datum, 512-cell tiles at the four levels 2.5′, 30″, 3″, 0.5″; a distance-to-shore
  field and a per-tile minimum depth at the two finer levels), `coast/<region>.geojson`,
  `features/<region>.yaml` (hazards, marks, lights with their dates, places, anchorages,
  transits, bottom notes; each with the period name, the modern name, an extent or height,
  a source citation in the references' form and a line the log can say),
  `overrides/<region>/*.yaml` (period depth and shore patches: polygons with a depth or a
  drying height in the sheet's own units and datum, the sheet, the control points and the
  datum correction). The M5 region is 48 to 51 N, 7 to 3 W. The region's tiles and the
  world level are committed (the region under 25 MB compressed, the world about 25 MB);
  the Atlantic level is fetched by the tool and not committed. Runtime reads with `numpy`
  and `pyyaml` only.
- **The build** (`tools/build_charts.py`, C §5.4): fetch into a cache outside the
  repository with URL, date and checksum, refusing any source whose licence is not in the
  allowed list (public domain, CC BY, Licence Ouverte, OGL, LGPL, named per-source
  permissions; never ODbL); resample (GDAL or rasterio may be used by the tool if
  installed, never by the game); rasterise the overrides and splice the period shore;
  derive the distance field, the per-tile minimum and a 0.25° feature index; write the
  tiles, the coast, the manifest with the attribution block the game shows in its about
  text, and a report. A test that every feature and override cites a source and every
  source in the manifest has an allowed licence. The sources: EMODnet DTM 2024 (CC BY 4.0)
  for the region's depth and coast; SHOM HOMONIM (Licence Ouverte) as the French
  cross-check with its datum; GEBCO_2025 (public domain) for the world and Atlantic levels
  and under everything; Histolitt (SHOM–IGN credit) for the French shoreline where needed;
  no OpenStreetMap in the tiles; no UKHO survey bathymetry until its licence is read and
  recorded. The licence texts under `docs/references/` with a `Charts.md` naming every
  source and what was taken from it.
- **The period patches and the feature list** (C §3, §4, §6), the hand work: four
  overrides (Falmouth and the Helford; Plymouth Sound and Cawsand without the breakwater;
  the Scillies; Brest, the Goulet and the Iroise) from the Hurd engravings of Mackenzie and
  Spence, Bellin, and the *Pilote français*, the facts transcribed with the sheet cited and
  the scans never committed; the feature list for the whole coast from Faden 1793,
  Stephenson 1795, Imray 1848 and White 1835, with Serres 1801 for the views, in the
  period's words, the lights dated so that 1805 sees St Agnes and not the Bishop. Each
  entry a source. Where a scan cannot be read at the resolution a sounding needs, the
  entry says what it rests on. The lead reviews this list against the sources before the
  merge; write it so that review is possible (the citation on every line).
- **The queries** (§11, C §5.5, `chart.py`): depth here (tile lookup, bilinear, the current
  tile and its neighbours cached); aground (short-circuited by the per-tile minimum against
  draught plus the highest tide plus a margin, otherwise the keel's cells at bow and stern
  against draught and heel and a tide height the tide of package 34 will supply, 0 until
  then: this package raises the `ship.aground` event and 34 gives it the tide and the
  consequences); nearest coast (the distance field and its gradient, a name from the
  index); in sight of what (once a game minute: the features within the horizon from the
  masthead, 2.08 (√h_eye + √h_object) miles with heights in metres, by the index, then by
  5a's visibility and daylight, then by the feature's own rules: a light at night by its
  range and date, a mark by day). The coast-distance hook of package 30 wired, so the sea
  breeze and coastal fog it left inert come alive by the study's rules (W §1.4), tested on
  a summer afternoon off Falmouth.
- **The lookout** (§12, `lookout.py`): the world's own voice at routine severity, notable
  for a landfall or a danger: "The Lizard bearing N by E, distant four leagues." "A light
  on the larboard bow." The lookout's words are what the sighting model gives, by compass
  bearing and estimated distance (the estimate the period's, to the nearest league or
  mile, not the truth); the reading `what is in sight` in the registry, the dialect reading
  it (`when the land is in sight then ...`). In 5c the same model sights sail.
- **The chart in the browser** (§17's first half; the reckoning half is 33's): `map.js`
  draws the region's coast and the features under the track as the captain's chart will
  (the truth's position still drawn for now, since the reckoning does not exist yet; 33
  removes it). The truth tiles are never drawn as a depth grid.
- **Truth 65** (the Bishop dark and St Agnes lit in 1805; a night landfall on Scilly from
  the south-west sees St Agnes at its range and nothing else) and the pace truth for this
  package (the queries per tick on the gate's day with the region loaded, floor 500).
- **Report**: the final suite line; the manifest's sources with licences and what each
  item of C §7 was found to be; the four patches' sheets and control points; the feature
  list's count by kind and its sources; the disk of what is committed; the pace; anything
  you could not do and why.

Not in 32: the reckoning and its instruments (33), the tide (34), anchoring's evolution
(34), ports and people (35), sail in sight (36), the Atlantic committed.

## Package 32b: the cutter and the brig as ship files, the orders' grammar across four ships (`tools/gen_ships.py` for a `cutter()` and a `brig()` builder with their crews, sail rooms and booms, and the running bowsprit as the one addition to the generator's rules; `data/ships/cutter.yaml` new and `data/ships/brig.yaml` new, generated and never hand-edited; `freesail/ship/schema.py` and `parts.py` only for the running bowsprit's flag if the file needs one; `data/evolutions/` for the bowsprit's two evolutions and `freesail/orders/verbs.py`, `data/vocabulary.yaml` for their verbs; `freesail/orders/*`, `freesail/evolutions/scripts.py`, `freesail/standing/*` and `client/projection.js` only where an order, a script, a standing order or the drawing fails on one of the new ships, each such fix a fault listed in the report; `tests/test_orders.py`, `test_standing.py`, `test_primer.py`, `test_catalogue.py`, `test_ship_loader.py`, `test_rig_geometry.py`, `test_view_geometry.py`, `test_canvas.py`, `test_hull.py` widened from two ships to four; `docs/primer/01-the-ship.md` a section for each vessel and `03-making-and-shortening-sail.md` for the running bowsprit; `docs/design/VesselCandidates.md` for the figures as read from a source; `README.md` run lines; `docs/dev/TuningNotes.md`)

Spec M5 §23 (the cutter) and §25 (the brig), `docs/design/VesselCandidates.md` (the owner's
choice and the figures as noted, every one to be read again from a source before it is a
number in a file), the design proposal's pillar 2 (the vessel library: a new ship is a
file, not an engine change). Pulled forward from packages 35 and 36 by the owner
(2026-09-30) so that the catalogue's hierarchy of size, cutter 85 tons, schooner 224,
brig 316, frigate 933, exists before the ports and the other sail need it. Fable.

The rule that governs the package, from §23: **no engine change.** The two files are built
by `tools/gen_ships.py` from documented particulars and period rules exactly as the
frigate's and the schooner's are, with the citation beside every number and "judgement"
beside every number that is one; the loader, the physics, the evolutions, the orders, the
standing orders and the viewer read them as they read the two existing files. Any order,
script or drawing that fails on either new ship is a fault in the grammar or in the
generator's rig rules, fixed there (in the grammar so that it reads the file with no rig
assumed; in the generator so that the file says what the grammar needs), never by a
special case for the ship, and every such fix is listed in the report. The one generator
addition the spec expects is the running bowsprit. If anything at all in `freesail/`
outside `orders/`, `evolutions/scripts.py` and `standing/` must change to seat either ship,
stop, and say what and why in the report before changing it: that is the finding pillar 2
exists to make, and the lead decides.

- **The sources.** The lead's figures in `VesselCandidates.md` are from memory and from
  the owner's notes of the kits' manuals; read each again before it is a number. For
  *Harpy*, Winfield's *British Warships in the Age of Sail 1793 to 1817* (the Diligence
  class) if it can be reached, else the manual's figures marked as such: 316 tons burthen,
  95 ft 0 in on the gun deck, 75 ft 1 5/8 in on the keel, 28 ft 1 1/2 in extreme breadth,
  12 ft 0 1/2 in depth in hold, complement 121, sixteen 32-pounder carronades and two
  6-pounder chase guns. For *Sherbourne*, Winfield's *1714 to 1792* volume or the RMG
  draught's record if reachable, else the manual's: 85 tons burthen, 54 ft 6 in (say
  whether on deck or on the keel, which the source will settle; the two differ by a
  fifth), 19 ft breadth, complement 30, six 3-pounders and eight swivels. The spars from
  the references already in the repository, which have what the two existing ships did
  not need: **Fincham 1843** (`docs/references/fincham/`), "On Masting Cutters and
  Schooners" with the table of proportions for masts, booms and bowsprits of cutters and
  the tables of lengths of lower masts and topmasts for cutters of different lengths (the
  OCR's pp. 66 to 71), and "On Masting Brigs" with the tables of masts, bowsprits,
  jib-booms and flying jib-booms and of yards and booms for brigs of different lengths
  (pp. 82 to 88), with the tables of diameters for both; and **Steel 1794** vol. I, the
  rigging tables for "a cutter of 200 tons" and "brigs of 200 tons" and "brigs of 150
  tons" for the rope sizes, scaled by the rule the frigate's rope follows, and his
  sail-making chapter for the cutter's mainsail and trysail and the brig's sails
  ("the sails of a brig with two masts are also similar to those on the main and fore
  masts of a ship"). Luce's proportions are the check for the brig, as the frigate's
  rules; Fincham's cutter tables are the primary source for the cutter, since neither
  Luce nor Falconer masts a cutter. Every table read is cited by the OCR's page as the
  schooner's builder cites Chapelle's.
- **The cutter** (§23): one file, `data/ships/cutter.yaml`, her name *Sherbourne*, her
  type `cutter`, described as the Channel's revenue cutter of 1763 whose type the pilot
  cutters and the hired armed cutters of the war shared. The hull as the schooner's is
  derived: a load waterline between the keel and the deck length, the breadth as given, a
  draught from the type (a cutter drew deep aft, on the order of half her breadth; say
  the rule), a displacement from a block coefficient the type's fullness justifies
  (fuller than the schooner's 0.33; say which and why), a stiff `gm_m` (a cutter was
  stiff and carried a great press of sail: the type's reputation is the judgement's
  ground), a hull speed from `1.34 sqrt(LWL ft)` bounded by the type's records, a low
  deck. One mast, lower mast and topmast (Steel: the cutter's topmast fidded above a
  lower mast left eight-square at the deck), with the head of the lower mast, the hounds
  and the cap as parts so that the topmast can be struck as the frigate's are; the gaff
  mainsail on a long boom over the counter and its gaff, the boom's length by Fincham's
  table; the square sail on its yard (Steel's "cross-jack" of the one-masted vessel, set
  flying from the deck and not a standing yard: model it as the schooner's fore yard is,
  or as a yard that is crossed and sent down, whichever the file can say without an
  engine change, and say which; spec M0 to M2 §12 item 7 records that the schooner's own
  bare fore yard was left out of her file for a milestone 1 test that counts her yards,
  which is the same question, and may be closed the same way); the square topsail on the topsail yard and the
  topgallant above it, as the kit's model shows three yards; the fore staysail on the
  forestay; the jib on its traveller on the running bowsprit; the gaff topsail if Fincham
  or Steel gives the type one at her date, else not; the storm trysail and the storm jib;
  reef bands on the mainsail (three, as the type's), the topsail (two) and the jib. Guns
  in the description and the `era_notes`, as the frigate's are (they are not parts until
  milestone 7). The sail room and the booms
  (package 30b's `spare_spars`) scaled to her: a spare topmast, a spare topsail yard, a
  spare jib and mainsail, judgement said so. A crew of thirty by the schooner's stations
  with no tops (forecastle, afterguard, waisters, idlers), `posts` master and mate and
  boatswain, names english; ratings a revenue crew's, mostly able.
- **The running bowsprit** (§23's one generator addition): a cutter's bowsprit ran in and
  out on the deck through a gammoning iron and a fid, reefed in heavy weather to bring
  the jib's tack inboard and rigged out for the full jib. In the file: the bowsprit spar
  with a `running` flag and its housed and full outboard lengths; the jib's tack at the
  full length. Two evolutions in `data/evolutions/`, `reef_bowsprit` (the verbs `reef the
  bowsprit`, `run in the bowsprit`) and `rig_out_bowsprit` (`rig out the bowsprit`), that
  set the outboard length and move the jib's tack, with the jib taken in first as a
  precondition (a reefed bowsprit sets the smaller jib or the storm jib; the full jib
  needs the full length), their crew and duration from Steel's or Lever's account of
  the work if either gives one, judgement otherwise. If a step kind the runner does not
  have is needed to move a spar's geometry, that is an engine change: stop and report it,
  and leave the flag in the file with its meaning in the comment, so that the file is
  right even if the evolution waits. The viewer draws the bowsprit at its current length
  from the state, or at the full length with a note in the report if the state is not
  in the drawing's data.
- **The brig** (§25): one file, `data/ships/brig.yaml`, her name *Harpy*, her type `brig`,
  described as the Diligence-class brig-sloop of 1796 (the merchant brig is her second
  description at far detail, which is package 36's to write: this file is the sloop's).
  The hull as the frigate's is derived (gun deck and keel to a waterline, burthen to a
  displacement with a sloop's block, the hold to a draught, a frigate's `gm_m` scaled, a
  hull speed from the waterline). Two masts, fore and main, each with a lower mast, a
  topmast and a topgallant mast, and royal masts only if Fincham's or Steel's brig of her
  size carries them by her date (say which; the kit's model shows three yards a mast);
  courses, topsails and topgallants on both with the frigate's reef bands; the spanker on
  its boom and gaff on the main; the head sails complete, fore topmast staysail on its
  stay, jib on the jib-boom, flying jib on the flying jib-boom; the staysails between the
  masts, the main staysail and the main topmast staysail, and the main topgallant
  staysail if the sources give it; studding sails on the fore and main by the frigate's
  rule (the lower, topmast and topgallant studding sails, the booms on the yards); the
  storm canvas of a brig (a main storm staysail, a storm trysail on the main, a storm
  fore staysail). Her guns as the frigate's are. The booms scaled from the frigate's list
  (Luce's frigate carries two of each; a brig-sloop one topmast that answers either mast,
  as Chapelle says of the brig, one topgallant mast, one topsail yard, a pair of booms),
  and the sail room by the schooner's rule (a second of each sail she could least do
  without, one of each storm sail). A crew of 121 by the frigate's stations in small
  (forecastle, fore top, main top, afterguard, waisters, marines, idlers), `posts` the
  sloop's (commander, lieutenant, master, boatswain, gunner, carpenter, purser, surgeon;
  what the loader has of these), names english. If the staysails prove troublesome that
  is a fault in the generator's rig rules to fix there, as §25 says, "a bad sign for the
  vessel library and treated as such": fix it in the rule and say so.
- **Balance and ratings.** Both ships are measured, not tuned: `tools/measure_loads.py`
  run on each for the spar ratings under the generator's design winds (the cutter's
  topgallant and square sail at the gaff topsail's 22 knots, since both come in early;
  say the rule); `clr_x_m` set as the schooner's was, close-hauled in 15 knots with a
  few degrees of weather helm on a beam reach, the numbers in the comment; each ship's
  polar drawn by the same means the frigate's and the schooner's were (close-hauled
  angle and speed in 15 knots, the beam reach, the run) and written in the report and in
  `TuningNotes.md` in the form of its "Where the ships stand" tables (speed by apparent
  angle, plain sail, 15 knots), so that the hierarchy can be seen: the cutter weatherly
  and quick for her size, closer to the wind than the schooner's five points as spec M0
  to M2 §12 item 11 expects of a cutter, the brig between the schooner and the frigate.
  Four **hierarchy truths** go with the files (owner, 2026-09-30, from the cold review:
  a ship with no truth is a ship whose pointing and speed are whatever the rules made of
  a new size, and these are the only check that the generator's rules hold at eighty-five
  tons): truth 73, the cutter lies closer to the wind than the schooner in fifteen knots
  under plain sail, by at least half a point; truth 74, the brig lies further off than the
  schooner and within half a point of the frigate (or the ordering the sources support,
  the choice explained); truths 75 and 76, the cutter's and the brig's speed on a beam
  reach in fifteen knots under plain sail each within a band the package sets from the
  type's records, the source named and the band marked provisional where it is a
  judgement. In `tests/test_known_truths.py` after 31b has merged (the lead says when),
  else in `tests/test_ships_hierarchy.py` for the lead to fold in; spec M5 §19. Milestone
  8's verification of each as a reference ship is a separate matter (§23, §25).
- **The grammar across four ships** (the test §23 names). Every test module that loads
  the two ship files loads four; every test that runs an order on "both ships" runs it on
  all four where the ship has the part, and asserts the refusal's words where she has
  not; the catalogue test's "the orders reach the right evolution on both ships" becomes
  four. Then the sweep: on each new ship, every verb of `data/vocabulary.yaml` with every
  noun her file gives, and the primer's and the catalogue's sequences (`make sail`,
  `shorten sail`, `plain sail`, `all plain sail`, `reef`, `shake out`, `furl`, `loose`,
  `set`, `take in`, `clew up`, `haul up`, `brace`, `trim`, `tack`, `wear`, `boxhaul`, `wear
  short round`, `heave to`, `lie a-try`, `scud`, `send down`, `sway up`, `cut away`, `clear
  the wreck`, `shift the spar`, `reeve`, `all hands`, `pipe down`, `belay`, the sail-room
  orders, every reading and every standing-order form of the starter file and the gate
  days' orders). The known places to look, from the grammar as it stands: `the topsail`
  on a one-masted ship (unambiguous with one; the grammar must not require a mast's
  name it has no need of); the mast names `verbs.py` knows (`fore`, `main`, `mizzen`),
  which the cutter's single mast must not need to give (Steel calls it the mast, or the
  main mast; accept both); the plain-sail set and the heavy-weather routine built from
  the file (a cutter's plain sail is mainsail, foresail, jib and topsail; a brig's the
  frigate's less a mast); the manoeuvre scripts that back a head sail or a mizzen
  (boxhauling and wearing short round on a ship with no mizzen the schooner already
  exercises; on the cutter the head sail is the staysail and the after sail the
  mainsail, which the scripts must find by class and place, not by name); lying a-try
  under the storm canvas each ship has; the topmen's mast (`runner.py`'s "the mast the
  subject stands on") on a ship with no tops; `client/projection.js`, which draws the
  hull as a lens from the file's dimensions and the rig from its parts and so needs no
  art for a new ship, drawing a gaff mainsail whose boom overhangs the counter, a running
  bowsprit, and the brig's staysails between two masts; the primer test's fences
  (```` ```orders cutter ````, ```` ```orders brig ````) once its ship table knows the
  names; the sail room's and the booms' queries; `tools/day_log.py`
  and the day's scenarios run under each ship (`--ship` if the tool lacks it). Every
  failure fixed in the grammar or the generator, and every fix listed: that list is
  the package's finding about pillar 2.
- **The primer.** `01-the-ship.md` gains a section for each new vessel in the form of the
  schooner's, forward to aft and deck upward, with her plain-sail set and her storm
  canvas named, and an orders block the primer test runs on her; `03-making-and-
  shortening-sail.md` a paragraph on reefing and rigging out a running bowsprit; the
  `README.md` run lines name all four ships. `VesselCandidates.md` gets the figures as
  read, beside the lead's, with the source and page.
- **Report**: the final suite line; the sources read with pages, and every number that
  is a judgement; the two ships' particulars as built (waterline, displacement, draught,
  sail area by sail, complement); the polar figures for both beside the schooner's and
  the frigate's; the list of orders, scripts, standing forms and drawings that failed on
  each ship and where each was fixed; the four hierarchy truths' measured values and
  their bands with the sources; what the running bowsprit needed and whether its
  evolutions run; anything that wanted an engine change and what you did instead;
  anything you could not do and why.

Not in 32b: the pilot's boarding and the port's cutter as a person's vessel (35), the brig
at far detail and her merchant description (36), truths for either ship (milestone 8),
*Alert*, *Speedy* and the wishlist (milestone 8), the tartane and the bilander of decision
11 (milestone 8, unchanged by this package), the lateen mizzen and the yacht.

## Package 32c: the suite in two tiers, the days built once, a Windows job (`tests/conftest.py` new; `pyproject.toml` for the markers and the options; `.github/workflows/ci.yml` and `release.yml`; `docs/gates/README.md` and `README.md` for the two ways to run the tests; `docs/dev/TuningNotes.md` for the timings)

From the cold review of 2026-09-30 (`docs/design/ColdReview-2026-09-30.md` §2.1 "The test
suite has become an integration suite" and §6 item 1), approved by the owner the same
day. Opus. First written for the owner's local session; built by the lead's cloud session
instead (owner, 2026-10-01: the repository is public, so the Windows job on GitHub's runner
costs nothing and is the Windows test; the owner runs the fast tier once afterwards for
the tuning notes' timing on their machine). No design change; no test moves between
files and no test's body changes (package 31b is editing `tests/test_known_truths.py`
at the same time, so that file is not to be touched at all).

1. **Two tiers.** A `slow` marker for the tests that sail a day or replay one (the
   pinned days in `test_known_truths.py`, the replay days in `test_replay.py` and
   `test_sea.py`, and any test over a threshold the builder sets from `--durations` and
   names in the report), applied from `tests/conftest.py` by node id or by the fixtures a
   test uses (`item.fixturenames`), never by editing the test files. `pytest` alone runs
   the fast tier and ends with one line saying how many slow tests it left out and how to
   run them; `pytest --slow` runs everything. The fast tier's target is under three
   minutes on the owner's machine on all its cores.
2. **The days built once.** With xdist's default distribution a module-scoped day fixture
   is built on every worker that draws one of its tests, so `-n 4` can sail the same day
   four times. Group the tests that share a module-scoped day fixture on to one worker
   (`xdist_group` marks applied in the same hook, with `--dist loadgroup`), so each day is
   built once a run and the rest of the suite still spreads. Measure the whole suite's
   wall clock at `-n auto` before and after on the owner's machine and on the build
   machine's figures in the review (eleven minutes alone, seventeen on four workers) and
   choose the distribution that is faster; say which and why.
3. **A Windows job.** `ci.yml` runs the fast tier on `ubuntu-latest` and on
   `windows-latest` (Python 3.11, `PYTHONUTF8=1`), on every code push as now, both under
   the same concurrency group; `release.yml` runs the whole suite (`--slow`) on Linux as it
   does, with the grouping. The Actions minutes are the owner's: keep the Windows job to
   the fast tier and say in the report what a push now costs in minutes.
4. **Docs.** `README.md`'s test line and `docs/gates/README.md` say the two tiers; the
   timings before and after go in `docs/dev/TuningNotes.md` under a heading for this
   package.
5. **Report**: the fast tier's and the slow tier's counts and wall clocks on the owner's
   machine (`-n auto`), before and after the grouping; the tests marked slow and the rule
   that marked them; the CI cost per push; anything not done.

## Package 32d: the `freesail` command, the settings file and the setup step (`freesail/cli.py` new, `freesail/__main__.py` new; `pyproject.toml` for `[project.scripts]`; `docs/Setup.md` new; `README.md`'s "Running it"; `tests/test_cli.py` new)

Spec M4 §24 open item 6 (the owner's note at gate 4b, 2026-09-27) and the cold review's
§6 item 9, approved by the owner 2026-09-30. Opus. **Deferred to after 33c and 33d land
and to be rewritten before launch** (owner, 2026-10-01, decision 31): built by the lead's
session and written for any machine, not the owner's, with one test cycle on the owner's
machine (the only Windows machine with Claude Desktop on it). The rewrite: the three
platforms' locations discovered by the command (`%APPDATA%`, `~/Library/Application
Support`, `~/.config`), the records and saves in the user's own data folder since the
consent records belong to whoever runs the game, its own entry merged beside any other
server in the Desktop config with a backup taken first, nothing of the owner's machine
hardcoded; the doors left open for others to come (an OpenRouter API door is wanted,
with a security pass of its own before it is built: a key kept outside the repository
and never in a settings file that is shared, never logged, never passed to the game);
and `freesail play` opening the browser on the launcher page of 32f once that exists. No change to any door, the server, the console
or the harness: the command wraps their `main(argv)` functions and passes arguments
through. `docs/agents/Harness.md` is not edited here (package 31c holds it); the report
gives the lead the lines that point from it to `docs/Setup.md`.

1. **The command.** `freesail` (installed by `pip install -e` as a console script) and
   `py -m freesail` (the same `main`) with subcommands: `play` (the browser game,
   `freesail.ui.server`), `console` (`freesail.ui.console`), `local` and `repl` (the two
   doors), `bridge` (`freesail.agents.mcp_server`, for the configuration files to name),
   `setup`, `install` and `check`. Each pass-through subcommand takes the defaults it
   lacks from the settings (the ship, the seed, the records directory) and passes
   everything else to the module's `main` unchanged, so `freesail play --wind 0,15` is
   `py -m freesail.ui.server <the settings' ship> --wind 0,15`.
2. **The settings file.** The things the owner sets once: the default ship file, the seed,
   the ports (the game's and the agents'), the model names for each door, the records
   directory, the installed game folder. TOML, read with the standard library's `tomllib`
   and written by a small writer of flat tables (no new dependency), kept outside the game
   folder so a gate does not lose it: `%APPDATA%\FreeSail\settings.toml` on Windows,
   `$XDG_CONFIG_HOME/freesail/settings.toml` or `~/.config/freesail/settings.toml`
   elsewhere; overridable by `FREESAIL_SETTINGS` for the tests. `freesail setup` with no
   argument asks for each value with the current one as the default and writes the file.
3. **The setup step.** `freesail setup desktop` writes or merges the `freesail` entry into
   Claude Desktop's `claude_desktop_config.json` (`%APPDATA%\Claude\` on Windows; the
   macOS and Linux paths for completeness; overridable by `FREESAIL_DESKTOP_CONFIG`),
   naming the Python that is running, the bridge module, the game's address and the model
   name from the settings, and leaving every other server in the file alone; it prints
   what it wrote and reminds the owner to restart Claude Desktop. `freesail setup
   claude-code` writes `.mcp.json` in the game folder the same way. Both refuse in words
   if the model name is not set, since consent is kept under it (`Harness.md` §3, §4).
4. **Install and update in place.** `freesail install <zip or folder>` puts a gate into
   the one installed location (from the settings, default `%LOCALAPPDATA%\FreeSail\game`
   on Windows, `~/.local/share/freesail/game` elsewhere), keeping `saves/` and
   `docs/agents/consent/` from the previous install (the consent records the owner's
   sessions wrote there are not in the zip), runs `pip install -e ".[dev,server,agents]"`
   in it, and then re-runs both setup steps so that the configuration files name the same
   path they always did. The zip is the release's (`FreeSail-gate-<name>/` at its top).
   The first install may be run from inside an extracted gate folder to adopt it.
5. **`freesail check`** prints the state a support question needs: the Python and its
   path, the package's version and location, the settings file and its values, whether
   each configuration file exists and names this install, whether the game answers at its
   port, and the records directory. No network beyond localhost.
6. **Docs.** `docs/Setup.md` for the owner: install once, `freesail setup`, `freesail
   setup desktop`, `freesail setup claude-code`, `freesail play`, updating to the next
   gate with `freesail install`, and what to do if `freesail` is not on the path (`py -m
   freesail`). `README.md`'s "Running it" gains the command beside the module lines, which
   stay.
7. **Tests** (`tests/test_cli.py`, no network, temporary directories throughout, the
   environment overrides above): the parser and the pass-through arguments; the settings
   round trip; `setup desktop` creating a file and merging into one with another server;
   `setup claude-code`; `install` from a small zip into a temporary location preserving
   `saves/` and the consent records; `check`'s output with nothing running.
8. **Report**: the suite's last line; the commands as they ran on the owner's machine
   (`freesail check`'s output pasted); the configuration files as written, with the model
   name blanked; what could not be done on the machine and why.

## Package 32e: staying and sheets, the fore-and-aft rig at the small vessels' scale (`freesail/physics/hull.py` for the yaw that scales with the vessel and the rudder's lever; `freesail/evolutions/scripts.py` for `TackScript`'s recovery, its miss-stays rule and the squaring as a brace, and `heave_to`'s headsail; `freesail/evolutions/trim.py` retired into `data/evolutions/trim_fore_and_aft.yaml` new and `scripts.TrimScript`, or kept only as the geometry (angle from the sheet's length); `freesail/ship/parts.py` and `schema.py` for the sheet's length as the sail's trim and the headsail sheet held to windward; `freesail/physics/sails.py` for the sail's angle read from its sheet and the load carried back; `freesail/physics/strain.py` for the sheet's load; `freesail/orders/verbs.py` and `data/vocabulary.yaml` for `haul`, `ease a fathom`, `let fly`, `flat aft`, `to windward`; `data/evolutions/tack.yaml`, `heave_to.yaml`, `wear.yaml` for the timings by vessel; `tools/gen_ships.py` for the boom's horse or traveller and the sheet's scope on all four ships; `data/standing_orders/starter.orders` for the sheet-tending routine; `docs/primer/04-trimming.md` and `05-going-about.md`; `docs/TechnicalSpec-M0-M2.md` §7.4 and spec M5 open items 12 and 13; `docs/dev/TuningNotes.md`; `tests/test_hull.py`, `test_evolutions.py`, `test_catalogue.py`, `test_trim_order.py`, `test_known_truths.py` (truth 10's three siblings, a turning truth per ship, the pointing truths re-measured))

Spec M5 open items 12 (the physics of staying) and 13 (sheets and trim), from the owner's
playtest of 2026-09-30, package 32b's finding and the lead's probe the same day; the cold
review's finding 3 (`tend_sheets`); spec M0 to M2 §12 item 2 (a turning truth from Luce
1884 Appendix L). Fable. Before gate 5b, whose passage tacks the schooner up the Channel.
Physics before rules; every constant its source or its confession; the pinned days
re-measured with the reasons.

- **Yaw that scales with the vessel** (item 12; `hull.py`). Today the rudder's force is
  `q · A_rudder · C_R · δ` with `q` from the speed squared, the damping `C_YAW_LIN` and
  `C_YAW` on the lateral plane, and the radius of gyration a quarter of the length, all
  tuned on the frigate; the probe shows the cutter turning at a degree and a third a
  second with the helm hard over at six knots, the schooner the same, both dying before
  the wind. Derive the turn from the hull as the file gives it: the rudder's area and its
  lever (already there), the lateral plane's damping scaled by its area and length as a
  short deep hull differs from a long one (the standard form: linear damping ∝ area ×
  length, quadratic ∝ area × length²), the yaw inertia from the displacement and a radius
  of gyration by hull type if one source gives it, and the rudder's lift slope with the
  aspect ratio of the blade the file describes. A **turning truth per ship** measured
  against a source: the frigate's tactical diameter from Luce 1884 Appendix L (the
  turning experiments; spec M0 to M2 §12 item 2, owed since milestone 2), the small
  vessels' from the type's record (a cutter "spins on her heel"; a figure with a page, or
  a judgement band said so). Truths 1 to 47 re-measured; a truth that moves says why.
- **Staying, with Luce's recovery** (item 12; `TackScript`, `tack.yaml`). The miss-stays
  rule reads the vessel: the way she must keep is a fraction of her close-hauled speed
  and her length, not 0.8 knots for every hull, and "hung in stays" is measured from the
  moment her way is gone, not from "helm's a-lee". When she hangs head to wind the script
  does what the seamanship texts say before it gives up (Luce 1866 ch. XXIV 'Missing
  Stays' and 'Boxing off'; Lever 1808): the helm kept over while she has way, reversed as
  she gathers sternway, the head yards kept aback to box her head off on to the new tack
  (a square-rigger) or the headsail sheets held to windward (a fore-and-aft vessel, and
  the frigate's jibs too), the after yards to the new tack once she is through; only when
  she has plainly fallen back on the old tack is it "missed stays", and then the yards
  are squared **as a brace with hands and time** (`YardSwing`, as "mainsail haul" is),
  never in a tick, and the helm put up as an order the helmsman carries out. The log says
  each stage in the period's words. Truth 10 keeps the frigate's five to ten minutes; the
  schooner's, the cutter's and the brig's tacks become truths beside it (a schooner about
  in under two minutes in a working breeze, the cutter quicker, the brig as a ship in
  little; each with its source or its band said), and the frigate's miss under three
  knots stays a miss.
- **The headsail sheet held to windward** (items 12 and 13; `parts.py`, `sails.py`,
  `heave_to.yaml`). A jib-headed sail's sheet may be held to windward as a state of the
  line (`to windward`), the sail then aback by the physics (its force reversed, its
  centre forward giving the bow off), which is what a small vessel uses to tack in light
  air and what heaving to properly needs ("the jib sheet to windward, the helm a-lee");
  `heave_to` on the cutter and the schooner uses it instead of the topsail to the mast
  where the file has no square sail to back, and the frigate's heave-to may add it. An
  order `haul the jib sheet to windward` and its release.
- **The sheet holds the trim** (item 13). One truth for a fore-and-aft sail's angle: the
  sheet's length hauled, through the boom's geometry (the boom's length and the horse's
  or traveller's breadth, which the generator writes for all four ships from the file's
  spars; a loose-footed sail by its clew's travel), gives the sail's angle to the
  centreline; `sheet_angle` becomes a reading of the line, never set on its own. Level 0
  works the line with hands: `haul the main sheet`, `haul it flat aft`, `ease the main
  sheet a fathom`, `let fly the main sheet`, `belay`; a sheet let fly has no load and the
  sail flogs (as now), a sheet belayed carries the sail's load into the strain model by
  its angle and length so that a main sheet can part in a gybe. `trim the <sail>` (to the
  wind, or to a bearing) is an **evolution on the sheet**: the afterguard works the sheet
  to the length the wanted angle needs, hauling a sheet that was let fly as part of it,
  with hands and a duration from the sail's size (a sheet of the frigate's spanker is a
  purchase and a party; the cutter's main sheet three men); the standing book's `trim`
  and the manoeuvres' sheet work reach the same evolution. **The free tending is
  retired**: `tend_sheets` goes, and the starter book gains a sheet-tending routine at a
  cadence (each glass, or on a shift of a point, the afterguard's routine work) so that a
  ship whose hands are all aloft has sheets that are not tended, which is true. The
  helmsman's `full and by` was tuned on free tending (tuning notes, package 10, changes 4
  and 6); re-measure the pointing truths and re-tune the helmsman's margin if they move,
  saying which.
- **The square rig's sheets** are not changed (tacks and sheets remain states, the yards'
  braces the trim), except that a course's sheet let fly flogs the sail as now.
- **Measured, not tuned**: the four ships' polars again after the change (the tuning
  notes' tables), the turning circles, the tacks' times; the pinned days re-measured and
  re-pinned with the reasons (the days hold no tack; the trim routine may move a line or
  two).
- **Tests**: the turning truths; the three new tack truths and the recovery's stages on
  the frigate (hung, boxed off, through) and on the cutter (the jib to windward); the
  miss under three knots still a miss, and the squaring a brace with a duration; the
  sheet as the trim (haul, ease, let fly, trim after a let-fly hauls it back); the sheet's
  load and parting; heaving to on the cutter and the schooner; the starter's tending
  routine; the primer's samples.
- **Report**: the suite's last line; every constant that moved with its source; the
  turning circles and the tacks' times of the four ships beside their sources; the
  pointing truths before and after; the recovery as the log says it, one transcript of
  the frigate hung and boxed off; what could not be sourced and is a judgement; anything
  not done.

Not in 32e: a per-sail pointing from the sail's own geometry (item 12's last paragraph;
after this lands, if the re-measured pointing wants it), the gybe as a manoeuvre with the
boom coming over on a timeline (`Presentation.md`'s rig-motion item), the kedge, the
sweeps.

## Package 33a (launched 2026-09-30): the reckoning, the noon sight, the captain's chart, the checkpoint save, gate 5b (`freesail/world/reckoning.py` new; `freesail/world/sights.py` new for the noon latitude only (the chronometer and the lunar are 33b's); `freesail/core/sun.py` for the altitude at noon if it lacks one; `freesail/core/world.py` for the reckoning's hourly step, the automatic log and noon, the master as the first named person's skill and place (spec §22's minimum, no more), and the checkpoint; `freesail/core/replay.py` for the checkpoint's load and its proof; `freesail/ship/parts.py` and the systems' `to_dict`/`from_dict` where a checkpoint needs them; `freesail/world/lookout.py` for the bearing taken; `freesail/world/chart.py` for the depth contour a cast is matched to; `freesail/api/readings.py` for the 5b readings; `freesail/api/queries.py` and `client/map.js` for the captain's chart (the reckoned position and its ellipse, the track by account, the noon positions, the bearings, the soundings; the truth removed from the snapshot); `freesail/orders/verbs.py`, `data/vocabulary.yaml`, `data/evolutions/heave_log.yaml`, `heave_lead.yaml`, `heave_deep_sea_lead.yaml` new; `freesail/standing/*` only for a new reading kind; `data/scenarios/gate-5b-passage.yaml` new (Ushant to Falmouth); `data/ships/*.yaml` through `tools/gen_ships.py` for the log-line and the lead as fittings if the file wants them; `tools/day_log.py` for the passage; `docs/primer/` a chapter on the reckoning; `docs/gates/gate-m5b.md` (the lead writes it at the cut; the package supplies the expected numbers); `docs/dev/TuningNotes.md`; `tests/test_reckoning.py`, `test_sights.py`, `test_checkpoint.py` new, `tests/test_known_truths.py` truths 58 and 59 and the pace truth for the passage)

Spec M5 §13, §14's noon latitude, §15, §17, §20 as revised by decision 29; `Navigation1805.md`
§1, §3 (every error term and its source), §4(a) and §5; `InwardAndOutward.md` (the master
as a person with a place and a skill is the inward minimum this package needs); the cold
review's §6 item 6 (the checkpoint save). Fable. The gate 5b package: the passage by the
reckoning and the noon sight alone, no chronometer, no lunar, no tide (33b and 34, in
gate 5c's set). The two rules of the chapter govern it: **the world keeps the truth and
the captain keeps his account**, no reading and no drawing ever gives the truth; and every
number from the study is checked against its own unverified list before it is a constant.

- **Two positions** (§13; `reckoning.py`). The truth is the physics' `Position` (package
  32). The reckoning is a position with a two-by-two covariance, advanced each hour by the
  logged run along the compass course corrected for the chart's variation and the
  master's leeway allowance and set, grown by the error terms of N §3 as named constants
  with their sources (the log-line's short-line bias 3 to 8 per cent and the quarter-knot
  read; the chart's variation a decade old, the 1805 Channel value from the gufm1 field
  model computed at build and recorded, about two points west; a deviation by heading
  the navigator cannot know, a few degrees seeded per ship; steering a quarter to half a
  point; leeway's estimate half a point out close-hauled; the tidal set not allowed for,
  which until package 34 is the scenario's stated current, none by default), and updated
  by each observation as a line or a point measurement in the simplest Kalman form,
  twenty lines of arithmetic, deterministic under the seed (`rng` stream `reckoning`).
  Tuned so that a day's run of 150 miles in thick weather leaves an ellipse of some 30 to
  50 miles after four days without a sight, Chan et al.'s figures an upper bound and not
  a target. The player never sees a matrix: `the reckoning's uncertainty` is the master's
  words ("I would not trust the reckoning within twenty miles east or west, nor five
  north or south"). The one rule: the player's errors come from the model's seeded draws;
  the world's truth from the physics.
- **Observations as lines and points** (§13). A sounding (`heave the lead` to twenty
  fathoms with the hand lead, `heave the deep-sea lead` beyond it, which brings her to
  or runs the line forward at a cost in hands and time, Luce and Lever for the work): the
  reckoning moves onto the nearest point of the chart's depth contour consistent with the
  ground (the chart's bottom notes, package 32) and the across-contour uncertainty
  shrinks, along it stays. A bearing (`take a bearing of <mark>`, refused in words if it
  is not in sight, the lookout's mark; a degree or two of error) is a line; two cross to
  a point; a transit (the chart's) is exact. The noon latitude collapses north and south.
  `work up the reckoning` on demand and automatic at noon (the day's work). `set the
  reckoning to <lat> <long>` lets the captain override the master, as he could. `heave
  the log` by order and automatic every hour in the frigate and every two in the
  schooner (and the cutter and the brig by their type; say which), the reading to a
  quarter knot with the line's bias. `shape a course for <place>` reads the reckoning
  and the chart's places, refused where the chart has no such place.
- **The noon sight** (§14's first sentence; `sights.py`, `sun.py`). Automatic at noon if
  the sky allows (5a's sky and visibility), refused in cloud in the registry's words ("No
  sight today; the sun was hid at noon"), with the octant's or the sextant's error (the
  scenario says which instrument, the frigate a sextant, the schooner an octant) and the
  horizon's (two to five miles with a good horizon, the sea's motion of 5a widening it,
  the hook 31 left inert now read). `observe the sun` by order at noon. Double altitudes
  are not built (§32).
- **The master** (§14's last paragraph; §22's minimum). The first named person: a name
  from the ship's list, a skill for the sights, a place (on deck, below) that the day's
  work occupies. No more of §22 than that; package 35 builds people and places whole.
- **Readings and log lines** (§15). `the reckoning` ("49° 52' N, 6° 10' W by account");
  `the reckoning's uncertainty`; `the depth` and `the ground` from the last cast with its
  age (the absent row of package 32 filled); `the bearing of <mark>` when in sight; `the
  distance run since noon`; `the course made good`; `the latitude by observation`;
  `what is in sight` as 32 built it. Each with its absent pattern. Log lines as N §4:
  "Hove the log: six knots and a half." "By the mark seven; fine grey sand with black
  specks." "Noon. Latitude by observation 49° 48' N; the reckoning was 49° 56'. Course
  made good since yesterday ENE, 131 miles. Longitude by account 5° 40' W." The roll-up
  keeps the noon line and the casts. The standing dialect reads the new rows for nothing
  (`when the depth is under 40 fathoms then heave the lead every glass`).
- **The captain's chart** (§17; `queries.py`, `map.js`). The snapshot carries the
  reckoned position and its ellipse, the track by account, the noon positions, the
  bearings taken and the soundings with their ground, and **no longer the truth**: package
  32's `position` leaves the snapshot (the truth is in the save and the tests only). The
  browser draws the ellipse faintly about the reckoned position, the track by account,
  the marks of the noon and the casts; the coast and the features as 32 drew them. A
  `--casual` display of the truth is a later display choice and is not built.
- **The checkpoint save** (the cold review's item 6; `world.py`, `replay.py`). A save
  stays a journal by definition; a checkpoint is a snapshot of the world's whole state
  written beside the journal (the ship's parts and dynamics, the crew, the routine, the
  runner's instances, the standing book, the weather and the sea, the reckoning, the
  agents' journals and turns, the rng streams' states), loaded directly by `--load` in
  seconds, and **proven by a test** that a world loaded from the checkpoint and a world
  replayed to the same tick carry on to the same digest for a watch. The old save loads
  as before. The day-long scenarios' `--load` at gate 5b uses it.
- **The passage** (§20; `gate-5b-passage.yaml`): Ushant to Falmouth in the frigate and
  in the schooner, neither with a chronometer, on the climatology's weather at seed 7 or
  a pinned day (say which and why): a departure bearing off the Stiff, the log hove
  hourly, a noon latitude, the Channel Soundings by the deep-sea lead, the Lizard sighted
  and bearings taken, the Roads entered; the same passage in thick weather with no sights
  and a landfall made wrong on purpose (the scenario's sky pinned thick). The cutter and
  the brig sailed through the same orders (a short leg each). `tools/day_log.py` runs it.
  The expected numbers for the gate report: the reckoning against the truth at each noon
  and at the landfall, the ellipse's axes, the casts, the ticks of the notable moments,
  the digests.
- **Truths 58 and 59** (§19) and the pace truth for the passage (the queries and the
  reckoning per tick on the passage, floor 500). Truths 60 to 64 and 66 are 33b's and
  34's.
- **The primer**: a chapter on the reckoning (the log-line, the lead and its arming,
  the traverse, the noon sight, the day's work, what the master's words mean), with
  orders blocks the primer test runs.
- **Report**: the suite's last line; every constant with its source and whether the
  study marked it unverified; the passage's expected numbers as above; the checkpoint's
  proof and its load time against the replay's; the reckoning's ellipse after one, two
  and four days of thick weather beside N §3's 30 to 50 miles; anything you could not do
  and why.

Not in 33a: the chronometer, the moon and the lunar (33b), the tide and the set it gives
(34), grounding's consequences and anchoring (34), the port and the pilot (35), double
altitudes, the kedge, the `--casual` display.

## Follow-ups from gate 5b's playtests (12 and 13), sorted

From the owner's notes and the watcher's post-session notes and journals of playtests 12
(the frigate's passage) and 13 (the cutter's and the brig's free passages),
`docs/playtests/2026-10-01-gate-5b-opus-5.5-*/`, read by the lead on 2026-10-01. Each
finding is placed where it is cheapest to build well; the packages named below are
written for the owner's word as their predecessors land. The owner's rulings on the gate
(the four of `gate-m5b.md` item 11) and the verdict are decision 30 when given.

**Into 33b (the chronometer, the moon and the lunar), as the captain's chart's second
half**, since every one is the chart in the captain's hands rather than the world's:

- A charted mark by account: `the bearing of <mark> by the chart` and `the distance to
  <mark>` from the reckoned position (the watcher advised from memory of the real chart);
  `the dangers` within some miles of the account, the nearest first; both readings for
  the dialect and the stand-by for nothing.
- `shape a course for <place>` says when the straight line crosses or passes close to a
  charted danger ("N by E by account, 17 miles; the line passes the Manacles within a
  mile"), and the pilot's answer (35) is the better course; "keep her full" and the other
  helm rules have no guard against bearing away toward a danger, which is the same
  reading's to give (playtest 12's course ran straight on to the Manacles twice).
- The lookout's distance by estimation drawn once per feature per sighting and held
  while the ship makes no way, not re-drawn at every hail (the Start at four miles, four
  leagues, three leagues in an hour of calm); a mark's distance the same in the list and
  in a bearing taken.
- `what is in sight` names dangers first, then lights, the land, the marks, and the cap
  of eight does not cut a danger off; a wake event `a danger sighted` (and `a bearing
  steady and closing` if it can be read cheaply) in `EVENTS` for the watcher and the book.
- The light at night against the weather's visibility: the rule bounds a light by the
  visibility as it bounds a mark, and the squalls' rain had the cutter blind to the Lizard
  lights ten miles off after dark while it had seen the towers by day at four leagues;
  check the period's practice (a light's loom carries in rain where a headland does not)
  and the visibility's words in passing showers, which may sit too low for too long.
- The features' names: "the Nare Head" of the Manacles' transit is Nare Point by the
  Helford (Nare Head is on the Roseland), to be read again from White 1835; the chart's
  edge north of the Start (Berry Head, Torbay) said in words by the lookout.
- Mark names are lower-cased mid-sentence by the reading ("black Head", "manacle Point":
  `lookout.py`'s first-letter rule on a proper name).

**Into 34 (the tide, grounding and anchoring)**, since the anchor is what every passage
wanted at its end and the set is what every reckoning lacked:

- The anchor: both free passages and the gate's own ended hove to for want of it; the
  owner's "shoal water" rule hove the cutter to in seven fathoms in an entrance where she
  drifted back toward the Head; the book's "lie off" answer is a stopgap the gate asks
  the owner to rule on.
- The log over-reads and the reckoning runs east of the truth on every passage (the
  noon fix two to three miles short; the watcher says fifteen per cent): with the tide's
  stream in, the set becomes the world's and the captain's allowance the dialect's, and
  the log-line's bias is to be re-measured against the study's three to eight per cent.
- A hove-to ship's reckoning (the board's "hours hove to making no way") against her
  true drift and forereach, which disagreed in the brig's night.

**A package of its own, "the fore-and-aft rig's second pass", after 34 and before 35,
physics and evolutions (Fable)**, since these are the same subject as 32e:

- Heaving to that holds: the frigate at noon came up, every sail aback for four minutes,
  then paid off and gathered four knots before the cast; the brig came through the wind
  and back before settling; the cutter's heave-to "a bit uncertain" (the owner). The
  balance when lying to against the spanker's or the mainsail's trim, the yards' aback
  through a wear (every square sail aback mid-wear at 18:43), and the lead able to go
  while hove to without the conflict rule breaking the heave-to.
- Filling away sets again the sail the heave-to took in (the courses, the topgallant and
  the spanker stayed in the gear until the captain set them by hand).
- Way coming off in a calm: the brig held three knots for forty minutes in two knots of
  wind (the hull's resistance at low speed; `taken aback` fired every few minutes as an
  urgent line and eased the clock each time: urgent only above a wind floor, notable in
  a calm).
- `trim sails` braces the furled square yards first and starves the mainsail's trim and
  once the lead; furled yards last or not at all. `trim sails` on the instant wind
  chases flaws in light shifting airs; the mean wind.
- Manoeuvres pre-empt routine work for hands: the cutter's tack queued behind the lead;
  `tack ship` from a reach brings her by the wind first instead of refusing; `avast that`
  belayed the tack (the last order) when the lead was meant, which the words allow.
- Reefs: `reef the mainsail, two reefs` takes two more; a `to N reefs` form and a ceiling
  for a reef rule that fires at every squall (the main reached four reefs).
- The helm reading gives its side (weather or lee); "making sternway" shown at four
  knots; the sea's words chattering through squalls (a dwell on "getting up / going
  down"); `state`'s apparent wind at 0 knots while the readings had 13; the hands on deck
  changing at four bells in the morning watch (`NIGHT_ENDS_HOUR`, the tuning notes'
  structural item since 29b).
- The viewer: the cutter's storm trysail and storm jib drawn as the mainsail and the
  jib, and the brig's storm trysail likewise (their own spars and positions from the
  generator); the running bowsprit redrawn at its length (the snapshot carries the spar's
  length; 32b's note).

**A small grammar package, "the passage's words" (Opus)**, which can run beside anything:

- A reading asked at the prompt: the owner typed `the reckoning`, `the master`, `the
  bearing of the Lizard` and `the reckoning's uncertainty` as the gate report's item 2
  told them to (the lead's error in the report), and the grammar refused each, since a
  reading is a row the instruments show, a rule tests and a model asks for, with no form
  at the prompt. Every reading's words typed alone (or after `what is`) are answered in
  the log as a query, as `the booms` and `the sail room` are; parity with the model's
  `readings` tool for nothing.
- A bearing taken by any of a feature's words when one in sight matches (`manacle` for
  Manacle Point; `the manacles` is the danger, a different feature, and says so);
  `belay`/`avast` by the order's words as package 29c meant (`belay heave the lead` was
  refused for the work's log name "heaving lead"); "(1 reefs in)"; `set the mainsail,
  one reef` as set then reef; the starter's `sound the well` held, not refused at every
  start, until the well is a reading (spec M4 §24 item 4).
- Aliases the owner and the watcher reached for: `steer for <place>` (the course shaped),
  `take a sounding` and `sound` (the lead), `trim the <sail> sheet` and `tend the <sail>
  sheet` (the sheet's trim), `the reckoning's doubt`; the owner found "the take / work up
  / reckoning's uncertainty terms" unclear with the primer and the gate guide beside
  him and many orders refused (`refused.md` in each playtest folder lists them with the
  reasons): the primer's reckoning chapter to carry every form the grammar takes, in a
  table, and a test that every form in the chapter parses.
- From the brig's refusals: a standing order named case-blind and loosely in `belay`
  and `resume` (`belay "blind lead"` was read as a part); whole-ship groups the brig lacks
  (`the topmast studdingsails` of both masts, `the sails`, `the square sails` as the
  cutter's file has it); `trice` as the period's word that earns the scandalise refusal.
- The dialect: "the daylight is night" refused where "daylight is night" was taken;
  `if she is hove to` / `if she is not hove to` as a condition (the brig's trim rules
  belayed by hand through a heave-to); a reading for the manoeuvre in hand.
- The standing runtime (spec open item 15): the conflict rule's grain (`heave the lead`
  against `heave to` and `wear ship` logged as contrary orders on the ship, and at noon
  it cost the heave-to); the held lines of an `at ... if ...` rule.

**The browser (a viewer package, the first of `Presentation.md`'s, when the owner says)**:

- The console's completion in the browser (`Presentation.md`); the reference library and
  the ship's papers readable in the browser in a pane of their own, which the owner puts
  first and allows to wait for the places and papers of 35 (the sail room's worked
  example in `InwardAndOutward.md`); an option to ease the clock to 1x when the watcher
  is sampled or speaks; zoom and pan on the chart.

**Harness, for 33c or the officer's package (37)**: the Desktop door's 200-second
re-poll at 1x (the client's limit; a longer hold is not ours to give, but a stand-by that
needs no re-call could be); the `in_sight` cap and the chart query above are the
watcher's first wants for the officer's station.

**Still open after 33b and 33c** (2026-10-01): the roll-up's and the library's own `_lower_first` (`core/events.py`, `agents/tools.py`, the cold review's duplicated helper) still lower a proper name's first letter when a line opens with one; the lookout's lines are right since 33b. A small item for the next pass on the log's words, with the helper made one.

**Noted, not acted on**: "morning sail" never fires on the gate's passage because the
clock starts two minutes after sunrise (the scenario's; a line in the gate report); the
watcher's own two mistakes, corrected by itself in the log (the spanker's trim, the helm's
side), which are the candour the brief asked for.

## Package 33b: the chronometer, the moon, the lunar and the azimuth; the captain's chart in his hands (`freesail/core/moon.py` new; `freesail/world/sights.py` for the time sight, the lunar, the amplitude; `freesail/world/reckoning.py` for the chronometer's and the lunar's updates and the variation by observation; `freesail/world/chart.py` and `lookout.py` for the chart queries by account, the dangers, the distance held, the names; `freesail/api/readings.py` for the new rows and events; `freesail/orders/navigation.py`, `data/vocabulary.yaml`, `data/evolutions/` for the sights' evolutions; `freesail/world/scenarios.py` for `chronometer:`; `data/charts/features/channel-west.yaml` for the two names; `data/scenarios/gate-5b-passage*.yaml` only if the frigate gains a chronometer for 5c's cruise (she does not here); `docs/primer/10-the-reckoning.md` and a chapter on the longitude; `docs/dev/TuningNotes.md`; `tests/test_sights.py`, `test_moon.py` new, `test_reckoning.py`, `test_chart.py`, `test_lookout.py`, `tests/test_known_truths.py` truths 60 and 61)

Spec M5 §14 (the chronometer, the lunar), §15's readings and orders they carry, §13's
updates; `Navigation1805.md` §2 (chronometers and lunars, every figure with its
unverified mark), §4(b) and (c), §5; decision 29 (in gate 5c's set); decision 30 (the
azimuth comes here; the captain's chart items from playtests 12 and 13). Fable. Written
2026-10-01 for the owner's final review.

- **The moon** (`core/moon.py`, §14): a low-precision moon good to a degree (Meeus's
  short method, the chapter and the terms cited), giving its age, phase, altitude, azimuth
  and the distance to the sun and to a short list of the lunar stars; the night's light
  for the lookout's words ("a moonlit night", which the land rule of §12 may read) and the
  age for the tide of 34 and for the almanac in the ship's papers. If the model runs past
  about a hundred lines, say so and keep it to what the lunar needs.
- **The chronometer** (§14; N §2): a scenario item, `chronometer: {maker, rated, rate_s_per_day,
  drift: seeded}`, the captain's own, absent unless the scenario says; wound daily by the
  master, the log saying so; `wind the chronometer` by order, and a chronometer not wound
  is a dead one, a scenario event; `compare the watches`. **The time sight** (`take a sight
  for the longitude`): a morning or afternoon sun altitude with the latitude and the
  declination giving the local hour angle, the longitude against the chronometer's time
  with the rate error times the days since rating plus the sight's own two or three miles;
  refused in cloud or with the sun too low; the reckoning's east-west axis updated by it.
  Readings `the chronometer` (its time, the days since rated) and `the longitude by
  chronometer` with the master's trust in words.
- **The lunar** (§14; N §2, §4(c), §5): `take a lunar [of the sun | of <star>]`, the
  conditions from the moon (up and above fifteen degrees, a body in distance, the sky
  clear enough, a horizon by day or by moonlight), refused in the registry's words
  otherwise ("No lunar to be had: the moon is two days old"); allowed, it occupies the
  master and two mates for a quarter of an hour (a crew cost, the master's place taken),
  and an hour of ship's time later the log gets the result, *drawn and not computed*: the
  true longitude plus an error from the seed scaled by the master's skill, the sea state
  of 5a and the moon's rate, a quarter of a degree for a good master on a quiet day, a
  degree for a poor one in a seaway (10 to 39 miles at 50° N). The reckoning updated by
  it; `the longitude by lunar`, `the chronometer's error by lunar`, `the moon`. The star
  lunar is cut first if the budget bites.
- **The azimuth** (decision 30): `observe an amplitude` at sunrise or sunset (the sun's
  bearing by compass against its true amplitude from the declination and the latitude:
  N §3's "an azimuth observation gets it to a degree"), refused in cloud or with the sun
  not on the horizon; `observe an azimuth` by day with the sun's altitude; the result the
  variation by observation, `the variation` as a reading with its date, and the reckoning
  thereafter corrected by it rather than the chart's decade-old figure, the master's
  words saying what he found. `VARIATION_1805_DEG` stays the world's truth (open item 14,
  still unverified; say so).
- **The captain's chart in his hands** (playtests 12 and 13; decision 30): `the bearing of
  <mark> by the chart` and `the distance to <mark>` from the reckoned position for any
  charted feature, in sight or not, with "by account" in the words; `the dangers` within
  a stated distance of the account, the nearest first, by name and bearing; `shape a
  course for <place>` says when the straight line passes a charted danger within a
  mile or crosses it ("N by E by account, 17 miles; the line passes the Manacles within a
  mile"), the pilot of 35 being the better answer and this the warning the master could
  give; the helm rules of the book have no guard, and that is the captain's business, so
  no rule is added; the events `a danger sighted` and, if it reads cheaply, `a bearing
  steady and closing` in `EVENTS` for the book and the stand-by.
- **The lookout, three faults** (playtest 13): a feature's distance by estimation drawn
  once per sighting episode and held while the ship makes under a knot, not re-drawn at
  every hail (the Start at four miles, four leagues and three leagues in an hour of calm),
  the same figure in the list and in a bearing taken; `what is in sight` names dangers
  first, then lights, the land, the marks, the cap of eight never cutting a danger off;
  a mark's name whole mid-sentence ("Black Head", not "black Head": the reading's
  first-letter rule stops at a proper name). The light at night against the visibility:
  read the period's practice on a light's loom in rain against a headland's (White 1835,
  Imray 1874 on the Lizard lights' range in thick weather) and either keep the rule with
  the words in the tuning notes or give a light a floor the weather does not cut below;
  and the visibility's words in passing showers between squalls checked against §5's
  table. The chart's edge: the lookout says in words that the chart ends ("the chart has
  nothing north of the Start").
- **Two names** (playtest 12): the Manacles' transit mark is Nare Point by the Helford
  (White 1835; Nare Head is on the Roseland), the feature and the transit corrected from
  the page; "the Beast" and "the Gray" checked against White's words.
- **Truths 60 and 61** (§19) as written, measured at seed 7 on the frigate given a
  chronometer by a test scenario (the gate's passage files stay without one); the
  azimuth's truth as a line in the reckoning tests (a sunrise amplitude on a clear
  morning finds the variation within a degree and the account thereafter runs truer).
- **The primer**: chapter 10 gains the chronometer, the time sight, the lunar and the
  amplitude in the master's words and an orders block for each; every form the grammar
  takes in a table (the owner's note 2, playtest 12), with the test that each parses.
- **Report**: the suite's last line; every constant with its source and the study's mark;
  the moon's accuracy against a known date (the Almanac's figure for one night, cited);
  the chronometer's and the lunar's errors on the frigate's test passage; the amplitude's
  result; the chart queries' words; the lookout's distances before and after; anything
  not done and why.

Not in 33b: the tide (34), the anchor (34), the pilot (35), double altitudes, the
star catalogue beyond the lunar's short list, the `--casual` display.

## Package 33c: the passage's words (`freesail/orders/*` for the readings at the prompt, the aliases, the bearing by any word, belay by the order's words, the groups; `freesail/standing/grammar.py` and `rules.py` for the article, the hove-to condition, a named rule case-blind; `freesail/standing/runtime.py` for the conflict rule's grain and the held lines (spec open item 15) and the starter's `sound the well` held; `data/vocabulary.yaml`; `data/standing_orders/starter.orders` split; `docs/primer/06-the-watch-and-the-log.md` or a chapter of its own for the starter book; `docs/primer/10-the-reckoning.md` for the forms table; `tests/test_orders.py`, `test_standing.py`, `test_primer.py`, `test_complete.py`, `test_tell.py`)

From playtests 12 and 13's refused orders (`refused*.md` in their folders, each with the
lead's reading) and the owner's notes and rulings of 2026-10-01 (decision 30). Opus.
Written 2026-10-01 for the owner's final review; runs beside 33b and 33d, touching none
of their files (33b owns `navigation.py`'s new orders; this package touches only the
aliases of the existing ones).

1. **A reading asked at the prompt.** Every reading's words typed alone, or after `what
   is`, are answered in the log as a query line (kind `query.reading`, routine), as `the
   booms` and `the sail room` are: `the reckoning`, `the reckoning's uncertainty`, `the
   bearing of the Lizard`, `the master`, `the glass`, `the sea`, a sail by name; the
   registry's absent words where a reading is not to be had. The console and the browser
   alike (one path through `World.submit`); the completer offers them. Parity: the same
   words the model's `readings` tool gives, nothing more.
2. **Aliases**: `steer for <place>` and `make for <place>` (the course shaped); `take a
   sounding`, `sound` and `cast the lead` (the lead); `trim the <sail> sheet` and `tend
   the <sail> sheet` (the sheet's trim evolution of 32e); `work up a reckoning`; `the
   reckoning's doubt`; `trice up the driver` answered with the scandalise refusal's words
   (no state for a dropped peak yet); `set the <sail>, one reef` as set then reef.
3. **Bearings and belays.** `take a bearing of <words>` takes a feature by any of its
   words when one feature in sight matches (`manacle` for Manacle Point), says which two
   when two do, and says in words that the Manacles proper are a different feature and
   not in sight; `belay`/`avast <the order's words>` matches the work by the order that
   started it as package 29c meant (`belay heave the lead` against "heaving lead");
   "(1 reefs in)" and every count's plural.
4. **The groups the brig and the cutter lack**: `the square sails`, `the sails` (every
   sail set), `the topmast studdingsails` of both masts, `the stuns'ls`, by the ship's
   file through the generator's groups where the ship has the parts, refused in words
   where she has not; `the lee stuns'ls` names the lee side's.
5. **The dialect**: "the daylight is night" taken as "daylight is night" is (the article
   before a reading's name everywhere); `if she is hove to` / `if she is not hove to`,
   and `the manoeuvre in hand` as a reading (hove to, tacking, wearing, none), so a trim
   rule can sleep through a heave-to; a standing order named in `belay`, `resume` and
   `show` case-blind and by any distinct part of its name.
6. **The standing runtime** (spec open item 15): the conflict rule's grain, so that
   `heave the lead` and `heave to` or `wear ship` are not contrary orders on "the ship"
   (the lead is the lead's; a manoeuvre is the helm's and the yards'); an `at <event>, if
   <condition>` rule whose condition fails does not log a held line at every event, only
   the first and then once a watch; the starter's `sound the well` held until the well is
   a reading (spec M4 §24 item 4), not refused at every start.
7. **The starter book is a choice** (the owner's ruling, decision 30). The starter file
   is split: `starter.orders` keeps the general and instructive routines (the night and
   morning sail, shortening for weather, keeping her full, trim on a shift, tending the
   sheets, heavy weather and the storm staysail, the well), and a passage's own orders
   stay in the scenario's file; no game loads the starter book unless the scenario says
   or the player asks (`--standing-orders data/standing_orders/starter.orders` on the
   console and the server, and a line in the browser's and the console's opening words
   saying how to load it or to begin with none); a primer chapter, "the starting book",
   prints each routine with the reason it exists and shows how to write one's own, with
   the dialect's forms; the gate's and the climatology day scenarios keep the book by
   name as they do. The owner's words: never a hard requirement for beginning.
8. **The forms table**: the primer's chapter 10 (and chapter 6 for the standing forms)
   carries every form the grammar takes for the reckoning's orders and readings in a
   table, and a test parses every row.
9. **Tests** for each; the refused orders of playtests 12 and 13 that should now be taken
   are a table in `tests/test_orders.py` (each with its new answer), and those that should
   still be refused keep their words.
10. **Report**: the suite's last line; the table of the forty-nine refusals of the three
    sessions with what each now does; the starter book's split; anything not done.

## Package 33d: the browser's shelf (`client/app.js`, `log.js`, `map.js`, `index.html`, `style.css`; `freesail/ui/server.py` for the completion route, the library routes and the driver's option; `freesail/orders/complete.py` as the completer behind the route; `freesail/agents/tools.py`'s `library` reused, not changed; `docs/agents/Harness.md` untouched; `README.md`'s run lines; `tests/test_server.py`)

From `docs/design/Presentation.md` (completion in the browser), the owner's notes of
playtest 12 (items 1, 3 and 4) and decision 30. Opus. Written 2026-10-01 for the owner's
final review; runs beside 33b and 33c and touches none of their files. Text and data
remain the baseline: nothing here is the only way to know something.

1. **Completion in the browser.** A route on the console's completer (`/api/complete?line=`),
   and a hint under the order line as the line is typed, the same words the console
   offers; Tab takes the first, the arrows move through them; the readings at the prompt
   of 33c appear among them once that lands (the route reads the completer, so nothing
   here changes for it).
2. **The library in a pane.** A pane of its own beside the log (or a pop-out window, the
   owner's word: "to avoid cluttering the log"), opened by a button and by a `library`
   line at the prompt: the reference library's topics as the model's `library` tool serves
   them (the primer by chapter and section, the catalogue of evolutions, the grammar's
   page, the tools' page), and the ship's papers the game holds by handle (`the booms`,
   `the sail room`, `the boatswain's store` as 31b and 30b answer them; the establishment
   table when 34 brings it), rendered from the same Markdown the model reads, with
   `find` across it. Nothing is served the model cannot ask for, and nothing the model
   can ask for is withheld. The sail room's pane is the one `InwardAndOutward.md` holds
   for 35's places: until then the console's query stands, and the pane shows the papers
   that exist and says which wait.
3. **The clock and the stations.** An option in the instruments (and a flag,
   `--ease-on-station`) to ease the clock to 1x whenever a station is sampled or speaks,
   as an urgent line eases it, and to speed up again by hand; off by default; a driver's
   line in the log says it happened, so a replay makes it.
4. **The chart's zoom and pan.** The wheel and a drag on the chart; the scale bar and the
   names follow (names when a mile is thirty pixels, as now); a button to centre on the
   ship again; the plane's map the same.
5. **Tests**: the completion route; the library routes serving each topic and `find`; the
   option easing the clock on a sample with the fake watcher and the log's line; the chart
   block unchanged (zoom is the client's; a Node test of the projection if one fits the
   existing view tests).
6. **Report**: the suite's last line; the routes and their words; what the pane shows and
   what it says waits; anything not done.

## Package 34: the tide, grounding and anchoring (`freesail/world/tide.py` new; `data/tides/constituents.yaml` and `streams.yaml` new; `freesail/core/world.py` for the tide's minute and the water's velocity in the physics; `freesail/physics/integrate.py` for the stream as a water velocity; `freesail/world/chart.py` for the tide's height under the lead and over the rocks that cover (`tide_m`); `freesail/world/reckoning.py` for the set the master allows against the world's; `freesail/world/ground.py` new; `data/evolutions/anchor_*.yaml` new (let go, veer, ride, heave short, weigh, cat and fish, a kedge laid by the boat as a later note) and `freesail/evolutions/scripts.py` for their scripts; `freesail/ship/parts.py` and `tools/gen_ships.py` for the anchors and the cable as parts of the four ships (bowers, a stream and a kedge; hemp cable by the fathom); `freesail/orders/*` and `data/vocabulary.yaml` for the ground tackle's words; `freesail/api/readings.py` for the tide's exposures and the ship's riding; `data/scenarios/gate-5b-passage*.yaml` gaining the anchor at the end; `docs/primer/` a chapter on the tide and the anchor; `docs/references/` the licence texts; `docs/dev/TuningNotes.md`; `tests/test_tide.py`, `test_ground.py`, `test_anchor.py` new, `tests/test_known_truths.py` truths 62 to 64 and 66)

Spec M5 §16, §18; `Tides1805.md` whole (§1's figures, §5 the recommendation adopted,
§6's unverified list); Luce 1866 ch. XIV and XV (ground tackle), ch. XXXIV (anchoring and
tending ship) and 1884 Appendix I and K (in a tideway, tending at single anchor); Lever
1808 on the anchor; Steel 1794 vol. II on stemming the tide; decision 29 (gate 5c's set)
and decision 30 (the owner: "full Luce/reference based anchor handling is well desired").
Fable. Written 2026-10-01 for the owner's final review; after 33b has landed (the moon's
age sets the tide's springs and neaps).

- **The world's tide** (§16; T §5). M2, S2 and N2 at the eleven TICON gauges (St Mary's,
  Newlyn, Devonport, Weymouth, Dover, Brest, Le Conquet, Roscoff, Saint-Malo, St Helier,
  Cherbourg; CC BY 4.0, the licence text under `docs/references/`), interpolated along
  the coast and across the Channel by the cotidal geometry; the astronomical arguments
  from the moon of 33b so that high water at full and change falls at the port's
  establishment; K1 and O1 dropped. Streams tabulated by area (`streams.yaml`: axis,
  spring rate, neap rate, phase against local high water) from T §1 and Bowditch 1802's
  headland table, with SHOM's open atlas for the Fromveur, the Four and the Goulet;
  evaluated once a simulated minute, five cosines. The stream sets the ship in the
  physics as a water velocity (the reckoning does not see it); the height is under the
  lead (`heave the lead` reads the chart's depth plus the tide) and over the rocks that
  cover (the aground test of §11 reads it).
- **The captain's tide** (§16). The establishment of the port from his epitome (the ship's
  papers, by handle: the table of high water at full and change by port, in hours and
  minutes or in points of the moon's bearing, with the spring rise, a poorer ship a poorer
  table) and the moon's age from his almanac, worked by Moore's rule of 48 minutes a day,
  wrong by up to an hour as Bowditch admits and by more with an old establishment; `the
  tide by the almanac` as a reading in the master's words ("high water at Falmouth about
  half past four this afternoon by the epitome"); the set he allows in the traverse
  (`allow <n> knots of set to <direction>`, 33a's) against the world's stream, the
  difference the play; the log-line's bias and the reckoning's eastward run of playtests
  12 and 13 re-measured once the stream is in (N §3's three to eight per cent), the
  tuning notes saying what the set explains and what the bias must. No tide readout, ever
  (T §5): the exposures are the table, the moon, the lead against the chart, the shore's
  marks that cover and dry (the Black Rock at half tide: the lookout's line), the ship
  riding to the tide, the reckoning's set.
- **Grounding** (§18; `ground.py`). Touching is an event with speed, heel, tide and bottom
  (32's urgent line becomes the beginning): the consequences are the hull's (a stop, the
  strain on the masts by the speed, a leak by the bottom's kind and the speed, the well
  rising, the pumps) and the log's; getting off is the tide's business (she floats on the
  flood if she took the ground on the ebb, the log saying when) or the anchor's (a kedge
  laid by the boat, noted as 35's boat work or later). The rule of truth 66 as written.
- **Anchoring, as Luce has it** (§18; decision 30). The anchors and the cable as parts of
  each ship from the generator (a 36's bowers and sheet anchor, a stream and a kedge; the
  schooner's, the cutter's and the brig's by their size; hemp cable by the fathom with its
  rating, Steel's tables; chain allowed by the file where the era says): `come to an
  anchor` as the evolution Luce ch. XXXIV gives (the sails taken in as she comes head to
  wind or tide, the anchor let go with way off her, the cable veered to a scope the depth
  wants, the yards squared, "riding to the flood"); `let go the best bower`, `veer cable`,
  `heave short`, `weigh` (the capstan, the hands, the time by the scope), `cat and fish the
  anchor`; at anchor she rides to the wind and the tide by the physics (the cable's pull
  on the bow, the stream and the windage, the ship swinging at slack water, "the cable
  slack at the turn"), the log saying how and the readings `the cable` (the scope, the
  strain) and `the anchor` (down, aweigh, catted); the cable's strain in the strain model
  (it parts, she drags); an anchor dragging a notable line, with Luce's answers (veer
  more cable, let go the second anchor, back an anchor) as orders. Mooring with two
  anchors is 5c's port (35). The gate 5b passages end with the anchor let go in the
  outer road or Carrick Road instead of lying to (the scenario's book amended; decision
  30: lying to was fine for the testing and no more), and the schooner's with hers off
  the town.
- **Truths 62, 63, 64 and 66** (§19) as written, measured at seed 7; a truth for the
  anchor (she brings up in the depth the scope allows and rides to the tide, and drags in
  a gale on short scope), its band from Luce.
- **The primer**: a chapter on the tide (the rule of 48 minutes, the headland table, the
  lead against the chart) and the anchor (Luce's sequence in the captain's words), with
  orders blocks.
- **Report**: the suite's last line; the constituents' sources and the datum offsets (open
  item 3's unverified four) as found or still not; the stream table with its sources; the
  two tides at Falmouth on the day of full moon; the log bias and the set re-measured on
  the three passages; the anchor's evolutions with their sources and times; anything not
  done and why.

Not in 34: the pilot and the port (35), mooring (35), the kedge laid by the boat (35's
boat), the Fromveur's eddies beyond the atlas, warping and towing (M7, M8).

## Package 32f: the launcher page (outline; written after 33d and 32d land)

Owner, 2026-10-01 (decision 31): the launcher with options is a page in the browser,
not a separate program, since the game is already a browser client of a server. The
first page the server shows: the ship, the scenario or a free passage, the seed, the
month's weather or a pinned day, the starter book or none (33c's choice, given a place),
the compression, which door a model comes through and under what name, the records
folder; then start. The console and the command-line arguments stay for preference and
for scripts. Packaging for a machine without Python (a start that carries its own
Python) is milestone 8's, and runs the `freesail` command, which opens this page.

## Package 35: places, people, ports and nations; the pilot boarding from the cutter (`freesail/world/places.py` new, `people.py` new, `ports.py` new, `nations.py` new; `data/ports/falmouth.yaml` and `brest.yaml` new, `data/nations.yaml` new, `data/papers/` new for the epitome's establishment table and the port's price list; `freesail/world/scenarios.py` for `people:`, `papers:`, `cargo:`, `ports:`; `freesail/core/world.py` for the places' and people's tick (a person occupied until when; the boat's passage); `freesail/world/ships.py` only for the pilot cutter as a vessel that comes off and goes back (the far-detail ships are 36's; the cutter's file is 32b's); `freesail/evolutions/scripts.py` and `data/evolutions/` for `send the boat`, `get under way` (Luce's order: heave short, loose and sheet home the topsails, weigh, cast her), `moor`/`unmoor` (two anchors and the hawse, 34's note), `lay out a kedge` by the boat; `freesail/orders/*` and `data/vocabulary.yaml` for the people's and the port's words; `freesail/api/readings.py` for the new rows and events; `freesail/agents/tools.py` for the ship's papers served by `library` to every station (the one change to the agents' code, as a `papers` topic beside the primer, read-only); `freesail/ui/server.py` only so that the library pane's papers come from the same source; `tools/gen_ships.py` for each ship's hold and her complement of boats; `docs/primer/14-the-port.md` new; `docs/dev/TuningNotes.md`; `tests/test_places.py`, `test_people.py`, `test_ports.py`, `test_nations.py` new, `tests/test_known_truths.py` truths 68, 69 and 70)

Spec M5 §22, §23, §24 (with §16's tide window and §18's anchorage from 34); `InwardAndOutward.md`
whole (the inward minimum and the sail room's worked example); `Papers-and-Books.md` (the
reference is a promise, the papers are things); `VesselCandidates.md` (the cutter as the
pilot's); `Tides1805.md` §2 (the port's establishment; "when the tide serves, get under
way"); the Regulations of 1806 in `docs/references/admiralty/` for who comes aboard and
what the captain signs; Luce 1866 ch. XXXIV and XXXV (getting under way, mooring and
unmooring), Lever 1808 (the boats, the kedge); Steel 1794 on the boats a ship carried; the
pilots White 1835 and Imray 1874 for the Roads and the Rade. Decision 30 (the owner's wish
for the full anchor handling; the pilot's answer as the better course than the master's
warning). Fable. Written 2026-10-02 for the owner's final review; after 34 (the anchorage
and the tide's window are its).

- **Places** (§22). A place is a name and a description, no more: the quarterdeck, the
  deck, the cabin, the gunroom, the tops, the sail room, the hold, the boat, the shore (the
  port's quay). A person is in one. `where is <person>` and `the people` read them;
  `go below`/`come on deck` move the captain between the cabin and the quarterdeck (the
  log says so, and the first consequence: a message reaches him where he is). No layout,
  no movement simulated; a person's place changes at the moments the period's orders
  changed it (`send for the master`, `pass the word for the carpenter`, the boat's going
  and coming). Text and data are the baseline; the viewer draws nothing new.
- **People** (§22). The named few: the captain, the master (33a's, now a person whole),
  the first lieutenant, two mates, the surgeon, the purser, the boatswain, the carpenter,
  the sailmaker, a midshipman as messenger; for the schooner the master and a mate; for
  each a name from the crew's names file, a role, a skill where a system reads it (the
  master's for the sights as now; the pilot's for the channel), a place and a state (on
  deck, below, asleep by the watch bill, ashore, sick, occupied by a task until a tick).
  A task that occupies a person (the lunar, the reckoning, the boat) says so in the log
  and refuses a second call on him in words. The people are saved and replayed, and
  `the people` lists them as the muster lists the hands. The crew of M3 stays counts.
- **The papers** (§22; `Papers-and-Books.md`). Each paper is a thing aboard with a keeper
  and a place: the sailmaker's account (the sail room; what `the sail room` answers,
  dated by its last entry, written when the sailmaker is sent to look or at the muster),
  the manifest (the hold; the cargo by tons), the purser's books (the stores), the
  boatswain's store book (the cordage), the booms' list, the epitome's establishment
  table (34's `tide_by_almanac` reads it; the table itself as a page: port, high water at
  full and change, spring rise), the port's price list once bought ashore. **Served by
  handle through `library`** as a `papers` topic, listed with their sizes and shelved as
  the primer is, to every station the same (the watcher included: the parity gap 33d
  found, a paper reachable only through `submit_order`, closes here); the browser's pane
  reads the same topic and the two "waiting" entries go. A paper is only as current as
  its last entry, and the log says when one is written or read.
- **Ports** (§23). `data/ports/falmouth.yaml` and `brest.yaml`: the anchorage and the
  mooring (Carrick Road and the inner harbour off the town; the Rade and the Penfeld) as
  positions on 32's chart with 34's tide window (the depth at low water, the flood to
  carry her in); the boat (sent ashore and back, a passage by distance at the boat's pace
  with hands and time, carrying a person, a message or a purchase; the kedge laid from it);
  the **market** (a list of goods with a price each that moves by a small rules table:
  supply by what has been sold, demand by season, war by the nations table; `buy <n> tons
  of <good>`, `sell`, `the prices` after the boat has been ashore; the schooner's hold by
  tons from the generator); the **dockyard** (a spar, a suit of sails, cordage, water and
  provisions, each with a time and a cost against the part graph, the frigate's from the
  yard by the Regulations' forms, the schooner's from the market); the **crew pool** (hands
  by rating at a price and a delay, mustered into the crew of M3); the **stance** toward
  each nation (open, neutral, closed, hostile) from `data/nations.yaml`. **Arriving** is a
  sequence the log tells and the readings carry: the pilot cutter sighted by the lookout
  (32b's cutter as a vessel that comes off from the port at the right tide and lies to
  under the ship's lee), the pilot aboard as a person with his skill, `the pilot` as a
  reading (his words: the channel, the marks, when the tide serves) and `ask the pilot`
  as a question; the anchorage; the boat; the shore. **Leaving** is the reverse: `get
  under way` as Luce has it, with the tide, the pilot off at the outer road. `moor` and
  `unmoor` with two anchors and the hawse in the inner harbour.
- **Nations** (§24). `data/nations.yaml`: Britain, France, Spain, the Batavian Republic,
  the United States, Portugal, Denmark; who is at war with whom in June 1805, letters of
  marque, the flags' words for 36's "a stranger, her colours not made out"; each port's
  nation. The stance is read from it; prizes and convoys are M7's.
- **Truths 68, 69 and 70** (§28) as written, measured at seed 7: a message from Brest
  reaches the captain in his cabin by the boat, the door and a person, each a line in
  order, never from nowhere; the schooner's cargo bought at Falmouth and sold at Brest
  makes or loses the sum the two price lists give, and a week's war news moves a price by
  the rules table; a port closed to the ship's nation refuses her entry in the pilot's
  words and the stance is the table's.
- **The primer**: chapter 14, "The port": the pilot, the anchorage and the mooring, the
  boat, the market and the yard, getting under way with the tide, in the captain's words
  with orders blocks and a forms table with its parse test.
- **Report**: the suite's last line; the people, places and papers as built with their
  words; the pilot's boarding on the frigate's passage (the ticks, the lines); the two
  ports' files with their sources; the market's rules table and the sums of truth 69; the
  nations table with its source for each war; every pinned constant that moved and why;
  anything not done and why.

Not in 35: the far-detail ships and the sighting of sail (36), the two scenarios whole
(36), the world-order channel (36), a person as a station a model may hold (M6; a
person is data and a line here), interiors beyond a name and a description (the bound of
`InwardAndOutward.md`), prizes and convoys (M7), warping and towing (M8).

## Packages 36 and 37 (outline; written in turn)

As spec M5 §31 after decisions 29 and 30: 33a, 33b, 33c, 33d, 34 and 35 above; 36
other sail, the world-order channel, the brig of 32b at far detail with her merchant
description, the two scenarios, gate 5c cut (§25 to §27, truths 67, 71, 72; Fable); 37 the
officer of the watch (per-order authority from the vocabulary's verb levels, a domain, the
standing conflict rule as the welfare detector for a station with authority, `hand over
the deck`, the station brief, the fake proving each; written when 36 lands so that it is
built with the world in place; Fable), after which the lead takes the officer's watch on
one of the two passages and gate 5c's verdict is given on that watch and the owner's
together (§29). The two new vessels' files are 32b's, pulled forward (owner, 2026-09-30)
so that the catalogue's hierarchy exists before the ports and the other sail need it.

## Integration (the lead)

The lead reviews each package against the studies and the spec, merges each wave, runs
the suite, cuts each gate, records the owner's verdicts, and writes the decisions log
entries. The lead takes a watch at gate 5c (spec §29).
