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
                  32c the suite in two tiers, the days built once, a Windows job (beside 32; the owner's local session)
                  32d the freesail command, the settings file and the setup step (beside 32; the owner's local session)
          wave 4  33a the reckoning, the noon sight, the captain's chart, the checkpoint save, gate 5b
gate 5c:  wave 5  33b the chronometer, the moon and the lunar (beside 34)
                  34 the tide, grounding and anchoring
          wave 6  35 places, people, ports and nations
          wave 7  36 other sail, the world-order channel, the two scenarios, gate 5c cut
          wave 8  37 the officer of the watch; the lead's watch; the 5c verdict
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
day. Opus, **run by the owner in a local Claude Code session on the Windows machine** so
that the timings are the owner's machine's. No design change; no test moves between
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
§6 item 9, approved by the owner 2026-09-30. Opus, **run by the owner in a local Claude
Code session on the Windows machine**, since the whole package is about that machine's
paths, launcher and configuration files. No change to any door, the server, the console
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

## Packages 33a to 37 (outline; written in turn)

As spec M5 §31 after decision 29 (owner, 2026-09-30): 33a the reckoning with the log-line
and the lead, the noon sight, the captain's chart in the browser and a verified
checkpoint save (§13, §14's noon latitude, §15, §17; truths 58 and 59; gate 5b cut;
Fable); 33b the chronometer, the moon and the lunar (§14's rest; truths 60 and 61; Fable);
34 the tide, grounding and anchoring (§16, §18; truths 62 to 64 and 66; Fable); 35 places,
people, ports and nations, the pilot boarding from the cutter of 32b (§22 to §24, truths
68 to 70; Fable, the owner's ruling of 2026-09-30, the earlier outline's Opus struck); 36
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
