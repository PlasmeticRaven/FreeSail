# Code reader 08: the simulation's heart (core, ship, physics, settings, units, the ship generator)

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read under READERS.md and CODEREADERS.md. No file but
this one was written; the test suite was not run. Three short Python commands were run: one 600-tick
frigate run (timed), one timing of the rules fingerprint, one demonstration that the checkpoint
unpickler resolves `os.system` (resolved, never called). Scratch script for line counts:
`the session scratchpad, share.py` (outside the tree).

## 1. What it is

**Size.** 30 files, 17,970 lines: `freesail/core/` 9 files, 5,363 lines (`world.py` 2,911, `replay.py`
916, `acts.py` 503, `events.py` 499, `sun.py` 234, `moon.py` 219, `clock.py` 51, `rng.py` 29);
`freesail/ship/` 9 files, 6,764 lines (`schema.py` 2,953, `parts.py` 1,988, `form.py` 1,020, `graph.py`
459, `stub.py` 138, `profile.py` 91, `charges.py` 72, `loader.py` 42); `freesail/physics/` 9 files,
4,679 lines (`sails.py` 1,614, `strain.py` 757, `hull.py` 602, `integrate.py` 536, `anchor.py` 370,
`motion.py` 361, `wind.py` 308, `oars.py` 130); `settings.py` 566, `units.py` 461, `__main__.py` 137.
Comment and docstring lines are 27% of the whole (4,823 of 17,970; `hull.py` 58%, `charges.py` 65%).
Data: `data/ships/` 18 YAML files, 31,494 lines, 2,801 parts; `data/sail_classes.yaml` 165 lines. The
generator: `tools/gen_ships.py` 10,381 lines and `tools/ships/` 15 files, 18,429 lines, together 28,810,
about 1.6 times this whole part and 18% of `freesail/` (164,607 lines).

**What it does in the game.**
- `core/world.py` `World` owns the clock, the wind and weather, the hulls (the ship and every crewed
  ship), the log, the order journal and the save. `submit` (world.py:1969) gives an order to the
  current hull; `tick` (2333) advances one game second; `save` (2590) writes the journal.
- `core/replay.py` writes and reads saves (JSON) and checkpoints (gzipped pickle), and replays a
  journal. `core/acts.py` journals what an agent's station does as inputs. `core/events.py` is the
  `Event`, the `Log` and its digest, and the hourly roll-up. `core/rng.py` is the named seeded
  streams. `sun.py`, `moon.py`, `clock.py` are the sky and the bells.
- `ship/schema.py` parses and validates a ship file into `ShipSpec`; `ship/parts.py` holds the runtime
  state of every spar, sail, line, gun, anchor, the magazine, sail room, booms and cordage;
  `ship/graph.py` `Ship` answers role queries (yard of a sail, braces of a yard, dependents of a
  spar); `ship/form.py` draws the hull for the viewer only; `ship/stub.py` `PointShip` is the M0
  stand-in still used for the observer and the harbour's empty world.
- `physics/integrate.py` `step` (52) is the ship's stepper: four quarter-second substeps of sail
  forces (`sails.compute_sail_forces`), hull resistance, keel, rudder and helmsman (`hull.py`), the
  cable (`anchor.py`), oars, tow; then strain (`strain.apply_strain`) once a tick; then log notes.
  `wind.py` is the wind (an Ornstein-Uhlenbeck wander, gusts, squalls) and the ten-minute record;
  `motion.py` the reduced roll, pitch and heave.
- `settings.py` is the launcher's settings file; `__main__.py` starts the harbour server.

**What the player sees of it.** Every log line the ship writes (taken aback, sails lifting, strain
warnings, carried away, leeway, helm steady), the speed, heel and leeway in the readings, the bells,
sunrise and sunset, saving and loading.

**Tests that import it** (files under `tests/`, 174 test files): `core.world` 108, `core.replay` 61,
`ship.loader` 60, `ship.parts` 54, `core.events` 32, `physics.sails` 26, `ship.schema` 18,
`physics.wind` 18, `ship.profile` 17, `ship.graph` 14, `ship.form` 14, `ship.stub` 13, `physics.strain`
10, `core.rng` 9, `core.clock` 8, `physics.hull` 6, `physics.integrate` 4, `core.acts` 2,
`core.sun` 2, `physics.motion` 2, `physics.anchor` 2, `ship.charges` 2, `core.moon` 1, `physics.oars` 1,
`settings` 3, `units` 63. Named: `test_replay.py` 1,101, `test_checkpoint.py` 550, `test_determinism.py`
37, `test_sails.py` 480, `test_hull.py` 461, `test_hull_form.py` 1,427, `test_strain.py` 733,
`test_wind.py` 157, `test_ship_particulars.py` 604.

### What one tick does, in order (world.py:2333-2510)

1. For the followed hull only: `clock.advance`, then the scenario's world orders due (2341-2344).
2. `_follow_weather`: weather systems advanced, base wind followed (2345, 2282-2321).
3. `wind.step` and `wind_record.add` (2348-2349); squall and gust lines (2350-2364); `_log_wind_shift`
   (2365).
4. On the minute: the sky and glass (2366); the sea on the minute and the motion every tick
   (2368-2372); the tide on the minute (2373-2375).
5. `ship.step(1.0, wind)`: the physics above and the evolutions (stepper), its notes recorded, the
   log-line and lead casts deferred to the reckoning (2376-2386).
6. `_tick_geo`: the run in metres to latitude and longitude (2389).
7. For the followed hull: `_tick_vessels`, the business on the minute and every other hull's whole
   `tick` run inside it (`Vessels.tick_crews`) (2392-2393, 1652-1673).
8. The guns, `combat.action.tick_action` (2396-2399); the chart: grounding, anchors, lookout on the
   minute (2400-2401); the water in the ship (2405-2411); the reckoning (2412-2416).
9. Ports' dealings and the world's ports (2420-2422); the people's tasks (2423); the watch routine
   (2426-2433); the officer's reports (2440).
10. On the minute: victuals, needs, health, the prize, the court martial, the fishery, the director's
    seat budgets (2441-2470).
11. Bells (2471-2480); sunrise and sunset (2483); the standing orders (2485); the rules-based
    captain (2488-2490); a boat's coxswain (2491-2496); the hourly change of the deck (2499-2507);
    every agent's `on_tick` (2509-2510).

Every other hull ticks in step 7, after the player's physics and before the player's guns and chart:
the order is a rule of the game held only by this listing.

**Cost.** One run, frigate (`data/ships/frigate-36.yaml`, 386 parts), default open-water scenario (no
chart, no weather systems, no other ships), orders `make plain sail` and `steer west`:

```
import 0.26s, world 0.85s, orders 0.33s, 600 ticks 0.91s = 1.5 ms/tick
log lines 60 speed kn 1.6 set sails 10 parts 386
```

About 650 game seconds a real second for one ship alone; a scenario with a chart, systems, a sea and
crewed ships costs more and was not timed. Making the World costs 0.85 s; the rules fingerprint alone
is 0.114 s over 179 Python files and 500 data files (12 MB), where world.py:76-77 says "some thirty
milliseconds for two hundred files and four megabytes".

## 2. Is it reached?

The game reaches: `World.tick`, `submit`, `save`, `replay.load_report` and `save_to_file` (from
`ui/server.py:757`, `ui/console.py:196,722`, `agents/repl.py`, `agents/remote.py`), all of physics through
`api/session.py` `make_world` and `attach_systems`, `ship.form.stations` (through `api/queries.py:28`
for the viewer), `moon_at` (through `world/sights`), `settings` (through `__main__.py`).

Not reached by the game (grep of `freesail/` and `client/` for callers):
- `world.py:2858-2877` `_ship_length_m`, `_ship_draught_m`, `_ship_heel`, `_ship_speed`: no caller
  anywhere.
- `sails.py:1388` `_blanket_factors` and `sails.py:1084` `_chord`: named only in docstrings
  (696, 706, 1412); replaced by `_blanket_factors_and_offsets` and `_chord_on_lee`.
- `events.py:333` `shown_dict`: no caller in the tree.
- `clock.py:61` `Clock.bells`: tests only (`tests/test_core.py:13`); the game uses `bells_struck` and
  `World._bells_struck` (world.py:1744).
- `charges.py` `CHARGE_TABLE_LB` and `parts.charge_lb` (674): reached only by the generator and
  tests; the game reads `filed_charge_lb` (`api/viewer_guns.py:465`, `parts.Magazine.charge_of`). The
  Regulations' table is in the game package and the game never reads it.
- `form.half_breadth_at`, `form.drawn_displacement_kg`, `form.check`: tools and tests only.
- Fields the code says nothing reads: `Scenario.nations` ("READ BY NOTHING YET", world.py:284),
  `QuarterBillSpec.marines` ("Read by nothing until her bill by deck", schema.py:756),
  `CrewSpec.flag` (schema.py:788), `Motion.sight_error_factor` ("Inert until then", motion.py:344;
  game reference count 1, its own definition aside).
- `replay.replay_world` (391): tests only, as its docstring says.

## 3. Built more than once

- **A sailor's name for a part, five times.** `evolutions/runner.py` `part_name`, `ship/parts.py:1424`
  `_sailor_name` (its docstring: "as evolutions.runner.part_name, which this module cannot import"),
  `physics/strain.py:737` `_name`, `physics/integrate.py:351` `_sail_words` (alias, but no side-first),
  `physics/sails.py:1335` `_name` (no alias, no side-first). So the same sail is "Mainsail ..." in a
  strain line and "Main course taken aback." in `sails._record_backed` (1325). Joining: one function
  in `ship/graph.py`.
- **Gravity, twice.** `units.G = 9.80665` (units.py:32); `world/ground.py:95 GRAVITY_M_S2 = 9.81`,
  `world/water.py:83 G = 9.81`. Units copied by hand outside `units.py` despite its docstring ("the only
  module that converts"): `parts.py:1862` 50.802 kg a cwt (the generator's `CWT_KG = 50.8023`,
  gen_ships.py:458), feet and fathoms in `combat/shot.py:65`, `evolutions/trim.py:289,291`,
  `world/water.py:76`, `world/ground.py:77`, `world/boats.py:73`, `api/viewer_guns.py:32`.
- **The sail-force law, twice.** The engine (`sails.py`, `wind.py` with `SHEAR_EXPONENT = 0.11`) and the
  generator's `static_kn` (gen_ships.py:440-446), which hard-codes the shear 0.11, its own `RHO_AIR`
  and `KNOT` (396-397), and `PEAK_COEFF` (136-140) copied from the class tables "if the curves change,
  change these and rerun". Today they differ: recomputed from `data/sail_classes.yaml` the studding
  class peaks at |(1.35, 0.50)| = 1.44, the generator uses 1.25; square 1.227/1.23, gaff 1.29/1.29,
  jib-headed 1.322/1.32, lug 1.285/1.29, lateen 1.246/1.25 agree; `sprit` (1.104) has no entry, so a
  sprit sail would fail the rating pass, as the lateen's own comment (137-139) says the lateen did.
  Studding sails and booms are rated against a force about 13% below what the engine puts on them.
- **A sail's cloth rating, twice.** `parts.py:76` `CLOTH_KN_PER_M2_NO2 = 0.32`, whose comment calls
  "the first draft's 0.9 ... an untuned default"; `Sail.from_spec` (parts.py:351) still falls back to
  `0.9 * area` when a file omits `cloth_rating_kn`. No shipped file omits it (304 sails checked by
  loading), so only a hand-written ship meets it, at nearly three times the cloth strength.
- **Charges, twice.** `charges.py` `CHARGE_TABLE_LB` (the table) and `parts.py:661` `CHARGE_SHARE` (the
  shares "from memory"), with eight ship files kept on the shares by rule (charges.py:294-303). Known
  and documented; still two tables of one fact.
- **Interpolation along a line, four times in the game and three in the tools.** `ship/profile.py:22`
  `interp`, `physics/sails.py:221` `_interp`, `world/ships.py:499` `_interp`; `tools/ships/bellerophon.py:96`,
  `indefatigable.py:844`, `neufchatel.py:120` each `interp` (same body).
- **Generator helpers re-written per ship.** `between_the_masts` four times (gen_ships.py:1816,
  `tools/ships/bellerophon.py:2044`, `indefatigable.py:2550` "modelled on the generator's
  `between_the_masts`", `neufchatel.py:1928`); `write`, `quarter_bill`, `ground_tackle`, `company`,
  `armament`, `at_the_guns`, `her_report` four times each; `head_geometry`, `staysail`,
  `studding_sails`, `storm_canvas`, `x_m`, `profile_into`, `hull_block` three times.
- **A ship file read twice.** `ship/loader.py:27` through the schema, and `world/ships.py:404`
  `yaml.safe_load(open(ship_file))` for `ship.descriptions`, which the schema does not parse
  (`parse_ship` reads `name`, `rig`, `era_notes` only, schema.py:1053-1058).
- **An order parser, twice.** `ship/stub.py:67` `PointShip.handle_order` (steer, speed, stop, by hand)
  beside the orders grammar; reachable in the harbour's empty World (`__main__.py:176`) and an
  observed world.
- **Caches in two styles.** `graph.py:35` keeps the schooner memo outside the Ship "so a memo kept in
  her ... would put a key in every save"; `sails.py` keeps `sails.load_paths`, `sails.spar_places`,
  `sails.yard_level`, `sails.bowlines`, `sails.square_rigged` and `strain.parts_by_kind` in
  `ship.extra`, which is pickled into every checkpoint, and `graph._chain_memo` is pickled with the
  Ship.

## 4. Size and shape as a hazard

Longest functions (lines): `World.__init__` 436 (world.py:713), `schema.validate` 238 (2383),
`schema._parse_crew` 178 (2729), `World.tick` 178 (2333), `sails.compute_sail_forces` 168 (335),
`integrate._log_notes` 139 (398), `World._submit_awake` 136 (1988), `replay.replay` 129 (149),
`schema._parse_stern` 107 (1849), `integrate._substep` 104 (100, seven parameters). In the generator:
`frigate` 1,022 lines (gen_ships.py:2135), `brig` 868, `schooner` 819, `cutter` 776, `lugger` 623,
`smack` 600; `between_the_masts` takes nine keyword parameters.

`world.py` holds 74 function-level imports, 59 of them from `freesail.world`, `crew`, `combat`,
`standing`, `evolutions`; `replay.py` 16; the rest of this part a handful. The per-ship names of the
World are installed as properties after the class (world.py:2698-2773: `PER_SHIP_FIELDS`, `vessels`,
`vessel`, `parent`), and `own` reads a thread-local stack keyed by `id(world)` (world.py:527-558,
2704-2712), so `world.ship` means whichever hull a block has made current on this thread. A reader of
`World` cannot see its fields in the class.

Global mutable state: `world._BUILD_RULES` (52), `world._TIDE` (2846), `world._CURRENT` (2704),
`sails._SHEAR_FACTORS` (813), `graph._SCHOONER_YARDS` (35), and `events.STATION_ACTORS` (170), a
process-wide set that grows as stations are defined and that `World._submit_awake` reads to decide
whether an order is journaled (2004, 2014): journaling depends on what else the process made.

Checkpoint compatibility shapes the code: 13 `__getstate__` hooks in `schema.py` and `parts.py` that
drop a field "so that a ... is pickled as before"; `World.__setstate__` and three `_adopt_old_*`
converters (world.py:1152-1258); `replay._rebind` (547-628) patches five generations of old state;
`parts._convert_70` (1135). In these three directories 54 comments speak of "from before", "pickled
as before" or "older saves load".

History in place of explanation: 542 "package NN" references in the three directories (core 261,
ship 158, physics 123) and about 70 mentions of a ruling, "the owner" or "the lead". `graph.py:207-243`
spends 37 lines of docstring on a 5-line method; `hull.py` is 58% comment. Much of it is useful cause
(why a constant has its value); much of it is ledger. A newcomer is helped by the sources and judged
figures, and drowned by the package numbers, which point into `docs/dev/` that a reader of the code
cannot use.

## 5. Correctness and honesty

**Determinism (the proposal's hard requirement).** Inside this part every random draw goes through
`core/rng.py` (sha256 of seed and name; grep finds no `random.random`, `time.time`, `datetime.now`,
`uuid` or `hash(` in core, ship, physics, nor in the simulation's other packages). Sets are iterated
only sorted (`strain.py:665,671`, `StrainState.snapshot`) or used for membership; dicts are insertion
ordered from file order. `id()` is used only for the hull stack and `_rebind`'s seen set, not for
order. That much is sound. Floating point across platforms is not solved: `events._canonical`
(events.py:123-136) rounds every float to nine significant digits for the digest, which (a) leaves two
floats that differ in the last bit unequal whenever they straddle a rounding boundary (rare per value,
but a day's log holds a great many floats), and (b) does nothing about a last-bit difference that grows
through the helmsman's integral, the thresholds (`STEADY_TOLERANCE`, `BACKED_DWELL_S`, the strain
draws) and the wind's feedback into a different log. The comment records one such difference found
between two machines. `tests/test_determinism.py` (37 lines) drives a `PointShip` World only; the
ship's determinism rests on same-machine replay tests.

**Save and replay ("a saved log is a saved game").** A save (world.py:2590-2646) is JSON: seed,
scenario, `ship_ref` (the ship file's path only, graph.py:421), the `inputs` journal, the stations'
acts, and blocks for agents and hulls; the log itself is not in it. Beside it, a checkpoint
(replay.py:504-529) is a gzipped pickle of the whole object graph. The load (815-905) takes the
checkpoint when it matches seed, end tick and input counts and its log's digest; else it replays the
journal. Across a change of build:
- The build is `rules_fingerprint` (world.py:55-83), a hash of every `freesail/**/*.py` (the UI, the
  agents, every comment) and every file under `data/` but the tiles, read from the working tree, so an
  untracked file dropped under `data/` changes it too. Any edit makes every earlier save "another
  build's".
- Then a JSON replay is promised nothing: `check_replay` (739-812) says "the log may differ", replays a
  station's game by its acts if they are whole, and refuses one with a transcript unless
  `--replay-anyway`.
- The checkpoint road is accepted from another build with one line of words (871-877): the pickle is
  loaded into this build's classes and leans on class defaults and the converters above.
- `save_to_file` (68-81) drops the checkpoint silently on `PicklingError`, `TypeError` or
  `AttributeError`; no driver says whether it was written (`ui/server.py:757-773`,
  `ui/console.py:722-723`). A save can lose its only exact road without a word.
- `BUILD_NAME = "m6c"` (world.py:48) at the milestone-7 commit; its comment names "m5c-c" (36, 92).

**The checkpoint's safety claim is false.** replay.py:27-28 and 448-450: "a checkpoint from elsewhere
cannot run code here". `_Unpickler.find_class` (491-501) admits any name in any module whose name
starts `freesail.`, and pickle resolves dotted names through that module's namespace. Run:

```
freesail.settings os.system -> <built-in function system>
freesail.core.replay pickle.loads -> <built-in function loads>
builtins eval -> refused: UnpicklingError the checkpoint names builtins.eval, which a checkpoint may not hold
```

A REDUCE opcode after the first would call it. `tests/test_checkpoint.py:125-130` tests only the
direct `posix.system` reference. A save shared with its checkpoint is a program.

**The boundary (core, ship, physics, crew import nothing from client, agents, api, ui).** Broken in
core, all inside functions:
- `core/world.py`: `agents.director` (1124, 1296, 2686), `api.readings` (1955), `agents.watches`
  (2505), `api.queries` (2555), `agents.harness` (2653).
- `core/replay.py`: `agents.harness` (143, 283, 291, 624), `agents.director` (319, 333, 349, 902),
  `agents.seat` (383), `api.session` (611).
- `core/acts.py`: `agents.journal` (410), `agents.director` (446).

Nineteen in all. `ship/`, `physics/` and `freesail/crew/` import nothing from client, agents, api or ui
(grep). Layering inversions beyond the stated rule: `physics/sails.py:96` imports `evolutions.trim` at
module level and `evolutions.runner` at 1040 and 1203; `physics/motion.py:38` imports `world.sea`;
`world.py` calls private helpers of `evolutions.scripts` (`_ground_speed`, `_depth_words`,
`_fathoms_words`, `_riding`, 1506, 1517); `api/readings.py:447,994` calls the private
`sails._apparent` and `strain._out_of_action`.

**Rig-agnosticism ("nothing in code assumes a number of masts or a kind of sail").** Physics and ship
code name no part ids: the only string literals with mast names are `strain.py:449`
`_MAST_WORDS = ("fore", "main", "mizzen")` (for grouping warning words) and `schema.py:394-403`
`CREW_STATIONS` with `fore_top`, `main_top`, `mizzen_top`, which caps a ship's tops at three named
masts, against schema.py:9 ("Nothing here knows about any particular rig"). The lugger files its mast
`mizen` (9 ids in `data/ships/lugger.yaml`) where every other file says `mizzen` (342), so its warnings
never group. Structural assumptions: four levels of mast (`mast`, `topmast`, `topgallant_mast`,
`royal_mast`; schema.py:112-128, `sails.YARD_LEVELS` 860), no skysail. "Frigate" appears in code only
as tuning: `hull.py` divides package 10's yaw damping by "the frigate's waterline" (74-75) and fits
`RUDDER_EFFECTIVENESS` to her (86); `motion.Particulars` defaults to her figures (146-148). The rule
holds for part names and fails, mildly, for crew stations and mast levels.

**Ships as data files.** Every file in `data/ships/` opens "Generated by tools/gen_ships.py; edit that
script and rerun, do not edit this file." (`frigate-36.yaml:2`, `boat-cutter-23.yaml:2`), and
`tests/test_ship_particulars.py:555-592` fails the suite if any committed file differs from a fresh
generator run. The YAML is output; the source is 28,810 lines of Python. A person can edit a file and
the game will load it, but the suite will fail and the next regeneration will undo it. The schema is
loose where a hand would slip: spars, sails, lines, the hull and the top level drop unknown keys
silently (`_parse_spar` 2070, `_parse_sail` 2181, `_parse_line` 2356, `_parse_hull` 1593; schema.py:71
"Unknown keys are dropped silently"), while guns, crew, pumps, anchors and the profile are strict. A
misspelt `rating_kn` on a spar becomes the class default with only a warning in `spec.warnings`; a
misspelt `x_m` or `height_m` becomes 0.0 (`Spar.from_spec`, parts.py:242-243). `_parse_hull` uses `or`
for defaults (1599-1601), so a rudder `max_angle_deg: 0` reads 35.

Why the tool is so large: it is where the ships are designed. Each ship is a long function (`frigate`
1,022 lines) of period rules applied to published dimensions, a rating pass that re-runs a static copy
of the sail-force law, and prose: a quarter of its lines open with a string literal (gen_ships.py
2,654 of 10,381; indefatigable.py 1,461 of 5,085), the notes and comments written into the YAML. The
docstring (gen_ships.py:1-11) still says it generates "the four reference ship files"; it writes 18.

**Other honesty points.** Sources are mostly cited and judgement is mostly marked; unverified figures
say so (hull.py:79 Helmbold "quoted from memory, the page not verified"; moon.py:255-256 the stars'
places "from memory ... unverified"; motion.py:62-63, 73-75). `world.readings` (1946-1965) caches by
(tick, log length) on the stated premise "every order writes a log line", which the same file breaks:
`UNLOGGED_KINDS` answers (2066-2077) and repeated standing-order refusals (2044-2056) return without
a line, and `needs.heard_order` (2031) changes state without one, so a view read on that tick may be
stale (a suspicion; not demonstrated). `strain.py:10` "Nothing ever recovers: repair is milestone 8"
sits beside jury masts and preventers of package 73 (parts.py:209-213, strain.py:519-535).

## 6. Thin or overgrown

Overgrown at the edges, sound at the centre. The integrator, the hull, the wind and the sail plate
(`integrate._substep`, `hull.py`, `wind.Wind.step`, `sails._plate_force`) are compact, signed
carefully, damped implicitly and honest about their tuning. Around them the part has grown far past
what the physics uses:
- `ship/form.py` (1,020 lines) and the hull profile in `schema.py` (18 keys, with a form of 3 and a stern of 7) draw a sourced hull section
  by section, while the physics reads only length, beam, draught, displacement and GM, and wets the
  hull as `L * (1.7 T + 0.7 B)` (`parts.Hull.wetted_area`, parts.py:1930-1934). The schema itself
  says the shape is "drawn only" (schema.py:80-87).
- `ship/parts.py` carries the gunner's whole magazine economy (`Magazine`, 1,000 lines with the sail
  room, booms and cordage) in the ship module.
- `ship/schema.py` (2,953 lines) validates gallery tiers and stern lights (1849-1955) for the viewer.
- `world.py` carries every system's wiring and every generation's converters in one class.
The generator, at 1.6 times the simulation's heart, is the largest single overgrowth in this part.

## 7. What is not tested

- The unpickler against a name reached through a `freesail.` module's namespace (section 5).
- A save whose checkpoint failed to pickle: nothing reports it, and grep finds no test of the silent
  drop.
- Cross-platform determinism of a ship (not a `PointShip`): no test can see it; the digest rounding is
  the only guard.
- The fallback cloth rating 0.9 kN/m2 for a sail without `cloth_rating_kn`: no shipped file uses it.
- Unknown keys in spars, sails, lines and the hull: dropped silently, by design; no test refuses them.
- The generator's `PEAK_COEFF` against `data/sail_classes.yaml`: no test compares them (the studding
  class differs today).
- `settings.py` is imported by 3 test files; `units.py` by 63.
- What the player meets that tests cannot see: the order of hulls within a tick (other ships tick
  between the player's physics and her guns), and the replay refusal words after any edit to any file.

## The ten findings that matter

1. **A checkpoint can run code.** `replay._Unpickler` admits every attribute of every `freesail.`
   module, so `freesail.settings` gives `os.system` and `freesail.core.replay` gives `pickle.loads`
   (shown above); replay.py:27-28 says the opposite and the one test checks only a direct reference.
   High, sure.
2. **The simulation does not keep the boundary.** Nineteen imports from `freesail.agents` and
   `freesail.api` inside `core/world.py`, `core/replay.py` and `core/acts.py`, all hidden in functions;
   physics imports `evolutions` and `world`. Ship, physics and crew are clean of agents, api and ui.
   High, sure.
3. **A save survives no change of build.** The fingerprint hashes every Python file of the game and
   every data file in the working tree, so any edit makes every save another build's: the JSON
   journal then "may differ" or is refused, and only a pickle held together by about fifty
   compatibility shims is exact; `save_to_file` drops that pickle silently when it fails. High, sure.
4. **Ships are not data a person edits.** All 18 YAML files are generator output and a test fails on
   any hand edit; the real source is 28,810 lines of Python with each ship's design re-written per
   module. Medium-high, sure.
5. **The generator re-implements the sail-force law, and its copy has drifted.** `PEAK_COEFF` (gen_ships.py:136)
   gives studding sails 1.25 where the engine's table gives 1.44, so studding gear is rated against
   13% less force than it meets; shear, air density and knot are copied by hand. Medium, sure.
6. **Cross-platform determinism is assumed, not secured.** Rounding the digest to nine significant
   digits (events.py:123-136) neither equalises boundary-straddling floats nor prevents divergence;
   the only determinism test drives a point ship. Medium, likely.
7. **`world.py` is a god object.** A 436-line constructor, a 178-line tick whose order is the game's
   rule, 74 function-level imports, per-ship fields bolted on as properties after the class and read
   through a thread-local stack. Changing it is dangerous. Medium, sure.
8. **The same fact in several places.** Five part-name functions that disagree (sails.py:1335 ignores
   aliases), gravity 9.80665 and 9.81, the cwt as 50.802 and 50.8023, interpolation seven times, the
   cloth rating's discarded 0.9 kept as `Sail.from_spec`'s fallback (parts.py:351). Medium, sure.
9. **Rig-agnosticism holds for part names, not for the crew or the mast levels.** `CREW_STATIONS`
   fixes three tops named fore, main and mizzen; four mast levels are the only ones; the lugger's
   `mizen` defeats `strain._MAST_WORDS`. Low-medium, sure.
10. **Dead and stale.** Unreached: `world._ship_*` helpers (2858-2877), `sails._blanket_factors`,
    `sails._chord`, `events.shown_dict`, `Clock.bells`, the Regulations' charge table in the game;
    stale words: "four reference ship files", `BUILD_NAME` m6c against comments of m5c-c, the
    fingerprint's "thirty milliseconds" (measured 114 ms); 542 package numbers in comments. Low, sure.

## What I did not read

- `freesail/units.py` lines 140-461: read as a list of definitions and constants only.
- `freesail/ship/form.py` lines 520-1020: read as a list of definitions only.
- `tools/gen_ships.py` and `tools/ships/*.py`: skimmed for shape as instructed (header, `__main__`,
  the design-load law, the coefficient table, function sizes, duplicated names), not read line by
  line.
- `data/ships/*.yaml`: all 18 loaded and validated through the schema; only the heads of the frigate
  and a boat and a slice of the frigate's spars read by eye. `data/sail_classes.yaml` read but for the
  lift and drag lists of the lug, lateen and sprit rows.
- Code outside my part that it calls (`world/hulls.py`, `world/crews.py`, `api/readings.py`,
  `evolutions/`, `agents/harness.py`) was grepped for callers only. The concurrency of a server thread
  reading the World while the driver ticks was not examined.
- No test was run; tick cost was measured on one open-water scenario only.
