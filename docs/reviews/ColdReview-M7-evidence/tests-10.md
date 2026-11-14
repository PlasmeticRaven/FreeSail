# Tests, reader 10: test_regatta.py to test_stand_by_words_and_action_flow.py

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. I read `tests/conftest.py` and all 25 files on my list, every line, plus the parts of the code named below where I needed them to judge a test. I ran no test. My only commands were greps, `wc` and one short Python script that checks the node ids in `conftest.py` against the files. Line numbers are the test file's unless I name another file.

## Summary table

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_regatta.py | 444 | 12 (12) | `first_course_runs` (module: two passages of the 5b course) | sound; one band built not to fail (441) |
| test_replay.py | 1101 | 22 (22) | none module-scoped; `three_stations()` built twice, `_watched_game()` four times | sound and hard; a few pins (`BUILD_NAME == "m6c"`), one timing band |
| test_rig_classing.py | 895 | 25 (71) | none | golden table pins by design; much of it tests the test fixtures' geometry, not the game |
| test_rig_geometry.py | 765 | 33 (51) | none | sound in the main; one parametrised test ignores its parameter and proves only a default argument |
| test_rollup.py | 486 | 19 (20) | none | sound; one stale node id in conftest moves a long test into the fast tier |
| test_routine.py | 560 | 24 (24) | `a_day` (module: 25 hours of the routine, no physics) | sound; one band built on a local copy of a code constant that leaves out part of the code's formula |
| test_sail_by_name.py | 459 | 14 (14) | none | one assertion built not to fail (164); two loose "either" asserts |
| test_sails.py | 480 | 23 (24) | none | sound force-level physics; one 25-fold band; one docstring that promises more than the body checks |
| test_scenario_nations.py | 235 | 4 (19) | none | tests a parsed block that no code reads |
| test_scenarios.py | 532 | 16 (16) | none | seven near-copies that want a table; one misplaced block of asserts |
| test_schooner_mast.py | 853 | 25 (74) | none | sound; pins the count of ship files; two long sailed tests in the fast tier |
| test_sea.py | 730 | 23 (27) | none | one tautology (636); one test of hooks that nothing reads, two milestones after "5b" |
| test_seat_hook.py | 175 | 3 (3) | none | sound; one long chain of refusals wants a table |
| test_server.py | 831 | 31 (61) | `world` param ×2 ships (function-scoped) | sound routes; one test reads the source text of `main`; ship-independent tests doubled |
| test_service.py | 159 | 6 (6) | none | sound |
| test_settee.py | 1566 | 37 (78) | none; about 26 fresh settles of 1,200 to 2,400 s | sound and hard; slow and repetitive; a stale docstring; two whole-trace pins; one monkeypatch that swaps like for like |
| test_settings.py | 214 | 9 (14) | none | tests the tooling, not the game; sound |
| test_ship_loader.py | 448 | 18 (48) | none | sound; holds a repository line-ending check that does not belong to the loader |
| test_ship_particulars.py | 604 | 19 (24) | six module-scoped `load_ship` (cheap) | data range checks; sound; stale docstring |
| test_ships.py | 889 | 29 (32) | none; `_under_way()` 1,500 ticks, built fresh about 15 times | asserts a stale docstring (251); one comparison of an object with itself (93); reads `client/map.js` text |
| test_ships_hierarchy.py | 235 | 10 (10) | 11 module sweeps and polars (slow tier) | sound bands; sails sweeps again that test_known_truths sails under the same names |
| test_sights.py | 182 | 7 (7) | none | one dead assertion (181 to 182); a comment and its band disagree |
| test_signals.py | 754 | 20 (32) | `_a_frigate` (module, cheap) | sound; strong data guard through `tools/check_signals.py` |
| test_squadrons.py | 829 | 21 (21) | none; several runs of 2 to 3.6 hours, not slow-marked | one tautology (530); one `A or B` assertion; one test step whose plant can never run |
| test_stand_by_words_and_action_flow.py | 157 | 5 (5) | none | three unrelated subjects under one name; one loop that does not require its other branch |

## The faults that matter most, across the files

1. **Assertions that cannot fail.**
   - test_sea.py:636 asserts `e.data["sea"] == e.data["sea"]`.
   - test_squadrons.py:530 asserts `hulk.position == hulk.position`.
   - test_sights.py:181-182 asserts `with pytest.raises(OrderError): raise OrderError("placeholder")`.
   - test_sail_by_name.py:164 asserts `world.ship.extra.get("chase", {}).get("id", "wasp") in ("wasp", "sail:wasp")`. No code writes `ship.extra["chase"]` (grep of `freesail/`), so the default `"wasp"` is always returned.
   - test_ships.py:93 compares the cached polar with itself after `cache_clear()`.

   Each of these is dressed as a check and checks nothing.
2. **Tests of things that no code uses, or of words in comments.**
   - test_sea.py:461 (`test_the_hooks_for_5b_are_numbers_that_nothing_reads_yet`): `Sea.horizon_nm` and `Motion.sight_error_factor` are still read by nothing at M7. The grep finds only their definitions.
   - test_scenario_nations.py as a whole tests a block that nothing reads (`Scenario.nations`, grep: no reader).
   - test_ships.py:251 asserts that `Vessel.promote.__doc__` contains "milestone 6". That docstring (freesail/world/ships.py:1095-1097) says the crewed promotion is still to come, and it has been built.
   - test_server.py:677-686 asserts a substring of `inspect.getsource(server.main)`.
3. **A stale node id in conftest.py:351.** `test_rollup.py::test_the_server_takes_speed_to_three_hundred_and_serves_the_store_by_ticks` names no test. The test was renamed `..._to_a_thousand_...` (test_rollup.py:239). That test runs 3,700 ticks of the frigate through the server and now sits in the fast tier. It is the only one of my 27 SLOW_TESTS entries that is missing.
4. **Unmarked heavy sailing in the fast tier.** test_settee.py settles a crewed brig fixture 1,200 or 2,400 s afresh about 26 times. test_ships.py builds `_under_way()` (1,500 ticks) about 15 times. test_squadrons.py runs convoys for 2 to 3.6 hours several times. test_schooner_mast.py has two settles of 2,400 s. None of them is in SLOW_TESTS or DAY_FIXTURES. I did not measure; this is a suspicion only, but a strong one by analogy with the listed tests.
5. **Docstrings the tree has outgrown.**
   - test_settee.py:23 says "None of the committed files carries a settee". `data/ships/bilander.yaml:318` has `settee: true` and line 193 has `heave_to_aback: true`.
   - test_ship_particulars.py:10-12 says "the source of all six files" and that "the last test regenerates them". There are 18 files, and the regeneration test is not the last.

---

## test_regatta.py

**Count and kind.** 12 tests, none parametrised. One module fixture, `first_course_runs` (line 418), sails the Ushant-to-Falmouth course twice, once under the rules captain and once under the fake (slow tier by DAY_FIXTURES). The fast tests sail a one-hour short course several times: `test_the_short_course...` sails it three times, and `test_a_model_is_named...`, `test_a_local_model...`, `test_a_hosted_model...` and `test_the_command_runs...` once or twice each. The file proves that the regatta tool loads a course, judges marks and the finish, scores a run, writes logs and the table without a model's name, enforces consent, and replays a run to its digest. It tests a tool (`tools/regatta.py`) laid over the game.

**(a)** Nothing dead found.

**(b)**
- Line 441: `fake["ran_s"] > 0 and (fake["finished"] or fake["miles_to_go"] > 0)`. For any run that started, either she finished or she has miles to go, so the disjunction cannot fail. The fake's run is checked for nothing but having started. Weight low, sure.
- Line 144: the time-limit check builds the judge at tick 10,000 and ticks it at 10,000. That is a fair check of the limit, but only at the boundary.

**(c)** The short course is sailed afresh in five tests, and the fake run in three of them. A module-scoped short-course run would serve test_a_model_is_named and the second run in test_the_short_course.

**Else.**
- `test_a_local_model...` (275) and `test_a_hosted_model...` (316) run the course at lockstep through mocked HTTP with `poll_wait=0.05`. The hosted one is in SLOW_TESTS; the local one is not, although it does the same work. Suspicion only.
- `test_the_judge_rounds_a_mark...` (107) is a good, cheap, exact test of the judge's geometry.

## test_replay.py

**Count and kind.** 22 tests, none parametrised, no module fixtures. Builders called repeatedly:
- `make_world()`, 2,300 ticks, in five tests;
- `_watched_game()`, 600 ticks with a station, in four;
- `three_stations()`, 3,600 ticks with three stations, in two;
- `five_stations()`, an hour with five stations, once;
- `crewed_voyage()` and `standing_voyage()`, once each.

The file proves that a game replays to the same digest by journal, by transcript and by acts, from checkpoint or from the journal. It also covers the build stamp and its refusal words, the station-ordering fixes, and the multi-hull save.

**(a)**
- Line 255 pins `BUILD_NAME == "m6c"`, and 258 pins `ENGINE_VERSION == "0.0.1"`. At milestone 7 the build name in every save still reads "m6c" (freesail/core/world.py:48). The pin keeps the name from moving and gives no reason. Either the name was never bumped, which is a code finding for the reviewer, or the test makes bumping it a test edit. Weight low, sure.
- Lines 582 and 657 assert that a save from before the count replays to a *different* digest (`old.log.digest() != world.log.digest()`). This pins the old fault as still present for old saves. That is intended, and the line is honest about it.

**(b)**
- Line 313: `time.perf_counter() - t0 < 0.5`. The docstring says the fingerprint takes "well under a tenth of a second (three hundredths)". The band is five times the claim and seventeen times the measure, and on a loaded machine it could still flake. The test also sets `world_mod._BUILD_RULES = None` (310) and leaves the recomputed value in place: harmless, but it changes module state. Weight low, sure.
- Lines 528-533: `repl_mod.main(...) in (0, 3)` accepts two exit codes and does not say which is right.
- Line 145 pins the count of journaled standing orders at `== 8`, and 135-142 pins the exact ticks of six firings. The comment gives the reasons (sunset 19:59 and so on), so these are pins a reader can check.

**(c)** `three_stations()` is built in both 713 and 752. One module fixture would save one 3,600-tick crewed build. Tests 16, 25 and 34 each build `make_world()` again for one assertion each.

**Else.**
- `test_a_stand_down_by_the_door_replays...` (624) and `test_five_stations...` (900) prove hard things exactly, by digest and by journals.
- `test_bad_format_is_rejected` (41) uses `try/else` rather than `pytest.raises`; it is correct but old-fashioned.

## test_rig_classing.py

**Count and kind.** 25 tests, 71 cases. The parametrised families: classing (8 files), the refusals (17 cases), the pickle (8), the probe (8), the fixtures (9) and `rigged_out` (2). There are no fixtures of weight; everything is loads and pure calls. The file proves how the manoeuvre gates class each of eight ship files, that the stage-0E keys load and refuse in words, and that pickles and checkpoints are unchanged.

**(a)**
- The golden `TABLE` (98-134) and the probe (460-476) cover the eight files of stage 0 only. The tree has 18. `bilander.yaml` now carries `settee: true` and `heave_to_aback: true`, and `seventy-four.yaml` and `sixty-four.yaml` also match the grep for the new keys. The probe's purpose (docstring 462-464: "what keeps every extension inert ... until a ship's builder writes it") is now a statement about a subset. It is still true of the eight, but no longer the guard the docstring describes. test_schooner_mast.py's header says the razee's and the 64's rows are in `test_indefatigable.py`, which I did not read. Weight low, likely.

**(b)**
- `test_the_table_holds_the_eight_files` (146) asserts `len(TABLE) == 8`, the size of the test's own dict. Only the `is_file()` half tests anything.
- The TABLE is a pin of eight rows. The file's docstring gives the rule ("a row that moves is a fault of the step, not a figure to repin"), so the pins have a stated reason, though the figures' source is a design document I was not to open.

**(c)**
- `_under_bowsprit` over the eight files (405-407) and the probe (473) check the same thing.
- The graph test (699-701) reloads all eight files again, as do 389-391, 405-407 and 416. Up to five loads of each file per run, cheap but repeated.

**Else.**
- Large parts test `tests/rig_fixtures.py` (1,089 lines of test-only rig generator), not the game:
  - `test_the_frigates_fixture_is_cut_to_the_contracts` (553);
  - `test_the_brigs_settee_is_cut_to_d5a...` (617);
  - `test_the_driver_fixture_is_cut_to_its_contract` (828);
  - `test_each_fixture_loads_and_validates...` (496).

  These prove that the test fixtures were drawn right. They are worth having only because other tests stand on those fixtures.
- The refusal family (324-362) is a good table-driven test.

## test_rig_geometry.py

**Count and kind.** 33 tests, 51 cases. There are no module fixtures. Most tests run a bare runner; four sail a World (`test_a_mast_swiftered_in...` ×4: 900 + 500 ticks, two of them slow-listed; `test_the_same_orders...`: two voyages of 2,700 ticks). The file proves the brace limits and stagger, the catharpins, the bowlines, adjacent-yard clearance, and determinism.

**(a)/(b)**
- `test_close_hauled_forces_are_unchanged_without_bowlines` (161-168) is parametrised over four ship paths and never uses `path`: four identical runs. Its body asserts `cls.coefficients(a) == cls.coefficients(a, 0.0)`. That proves only that the default argument is 0.0 and that the two calls take the same branch (freesail/physics/sails.py:208-209). The docstring promises "milestone 2's to the last newton ... the class tables' values", and no recorded value is compared. Any change to the no-bowline curve passes. Weight medium, sure. Fault 3 below.
- Line 371 recomputes the code's own formula, `1 / sqrt(1 - s^2 + (s/f)^2)`, from freesail/physics/strain.py:702-704 with `s` read the same way the code reads it. That half mirrors the code. The bounds beside it (`s > 0.8`, `f <= rf < 0.9`, `> 0.97` running) carry the weight.
- Line 489: `assert "fore.course.bowline.starboard" in want if which == "frigate" else want`. For the schooner it asserts only that `want` is not empty. Correct, but obscure.
- Lines 209-212 test the `EASE_HEAD_YARDS` switch, which is off in the code (freesail/evolutions/trim.py:56). The test keeps an unused branch alive. Low.

**(c)** `test_a_ship_starts_as_milestone_3_left_her` and `test_close_hauled...` share the same four-ship parametrisation for nothing. Lines 519-520 loop `for side in ("starboard",)` over one item.

**Else.** The adjacent-yard tests (623-707) check the refusal words exactly; they are good.

## test_rollup.py

**Count and kind.** 19 tests, 20 cases. No module fixtures. Five tests sail the frigate for 20 to 120 minutes. The file proves the roll-up view, its parity across console, server and samples, and auto-slow.

**(a)** conftest.py:351 lists `test_rollup.py::test_the_server_takes_speed_to_three_hundred_and_serves_the_store_by_ticks`. No such test exists. The test at 239 is `..._to_a_thousand_...`. The slow mark is therefore lost, and a 3,700-tick frigate run through the TestClient sits in the fast tier. I found this with the script described at the head of this file: of the 27 SLOW_TESTS entries naming my files, this is the only one that names no test. Weight medium (the fast tier's time), sure.

**(b)**
- Lines 191-193 loop over the non-routine events after tick 600 and check each was printed. If there are none, the loop passes empty; there is no assertion that `notable` is non-empty. Low, a suspicion.
- Lines 78-79 pin the constants `ROLLUP_FROM == 60`, `ROLLUP_PERIOD_S == 3600` and `KEPT_ACTORS`, a reading of the code against literals. The spec is cited.
- Lines 485-486 construct a `Station("second lieutenant", ...)` only to see that a module-level `STATION_ACTORS` grows. The constructor mutates a global, and the test leaves it mutated for every later test in the worker. Low, sure.

**(c)** Lines 432-443 re-import `summarise`, which is already imported at 31.

**Else.** `test_auto_slow_changes_the_drivers_speed_and_a_replay...` (379) is a good determinism test of a driver line.

## test_routine.py

**Count and kind.** 24 tests, none parametrised. One module fixture, `a_day` (68), runs 25 hours of the routine alone (90,000 ticks without physics; it is in DAY_FIXTURES). `_night()` runs 8 hours of the routine and is called five times. `test_a_crewed_world_through_a_day` runs a schooner World 86,400 ticks with `ship.stepper = None`. The file proves the watch bill, all hands, pipe-down and fatigue rates.

**(b)**
- Line 36 copies `FATIGUE_WEIGHT = 0.5` from freesail/crew/hands.py:50, and line 486 asserts `1.10 <= 1 + FATIGUE_WEIGHT * morning <= 1.25`. The code's term is `1 + FATIGUE_WEIGHT * max(0, mean - FATIGUE_FRESH)` with `FATIGUE_FRESH = 0.05` (hands.py:54, 426). The test's formula leaves out the subtraction, uses its own copy of the weight, and never calls the code. It gives 1.170 where the code gives 1.145; both are in the band. The docstring calls it "truth 20's mechanism", but the morning's slowness is never read from the code. Weight medium, sure. Fault 4 below.
- Lines 346-351 pin five fatigue constants to their literal values. Lines 483 and 485 pin `0.0109` and `0.3405` to ±5e-4, with the reason left in docs/dev, which I may not open. That is three exact pins.

**(c)** `test_a_crewed_world_through_a_day` (530) repeats `test_a_days_watch_changes...` (95) through the World on another ship: a fair end-to-end check, but the same seven reliefs. `test_same_crew_same_clock...` sails `_night(CALLS)` twice more, after `test_three_calls...` has sailed it once.

**Else.** Line 532 sets `world.ship.stepper = None`. The attribute exists (freesail/ship/graph.py:60), so the comment is true. Tests 167-213 pin the arrival curve (47, 31 a 30 s, and so on) as exact counts. They are exact, but derived from the rule as stated.

## test_sail_by_name.py

**Count and kind.** 14 tests, plus one non-test function, `recorded_passages_name_their_sails_as_before`, which test_known_truths calls. No fixtures. `sails_about()` builds a frigate world with four sails and is called seven times. The file proves the sail resolver by kind, quarter, bearing, distance and name, the boat to a sail, the identified name in the rows, and the toggle proof.

**(b)**
- Line 164: `world.ship.extra.get("chase", {}).get("id", "wasp") in ("wasp", "sail:wasp")`. No code writes `ship.extra["chase"]`, so the expression is always `"wasp"`. The chase's target is therefore never checked. The only check left is `"bearing NE" in chase.text` (163), and both the Raven and the Wasp bear NE (157). The docstring claims "the glass, the bearing and the chase take the same words". The chase half is unproven. Weight medium, sure. Fault 2 below.
- Line 122: `_id_of(...) == "nancy" or _id_of(...) == "swift"`. The docstring says "'make out the brig' gives the nearer", and the nearer is the Nancy (0.25 miles against 0.30). Either answer passes. Low.
- Lines 141-149: the bearing of the sail is accepted within 15 degrees, more than a point. Low.
- Line 414: `own = world.vessel.id if getattr(world, "vessel", None) is not None else "the ship"` hedges on the world's shape, and the reader cannot tell which branch runs.

**(c)** `sails_about()` with its 120-second settle is built in seven tests; a module fixture with copies would do, if the World copies cheaply.

**Else.** The toggle proof `_passage()` (296-316) sets the module global `SAIL_BY_NAME` in a `try/finally`, which is correct. But the code keeps a toggle (freesail/world/lookout.py:1643 and seven readers) whose only use is this proof.

## test_sails.py

**Count and kind.** 23 tests, 24 cases. No fixtures. All tests are pure force computations. The file proves the sail-force model: apparent wind, symmetry, backing, blanketing, reefs, loads, strain and truths 2, 5 and 13 at force level.

**(b)**
- Line 262: `4_000 < f.thrust_n < 100_000`, a 25-fold band. The comment says the drive is "about six" kilonewtons, so the band would pass a model off by more than an order of magnitude upward. Weight low, sure.
- `test_deterministic` (476) calls a pure function twice on the same ship with a wind that is never stepped (line 30 says so). It cannot fail unless the function mutates state. Low.
- `test_schooner_points_higher_than_the_frigate` (460): the docstring says "the schooner drives, the frigate cannot". The body checks only that the schooner's thrust per square metre is greater; the frigate's thrust is never asserted to be at most zero. Low, sure.

**Else.**
- Lines 90-101 and 356-358 pin table values and load fractions (1.12, 1.25, 0.12/0.42, 0.6/0.5/0.3), in effect mirrors of the code's constants. There are six such pins.
- `test_loads_go_on_cloth_spars_and_lines` (344) is a good exact accounting test.

## test_scenario_nations.py

**Count and kind.** 4 tests, 19 cases (16 refusals). No fixtures. The file proves the parsing, validation and round-trip of the scenario `nations:` block.

**(a)** The docstring says plainly that "nothing reads it". The grep confirms that `Scenario.nations` is written by freesail/world/scenarios.py:619 and read by no code. The file is a full test of a dormant field, kept for a later scenario (B6). It is not wrong, but it costs upkeep for no behaviour. Weight low, sure.

**(b)** Line 227: `len(files) > 25`, a loose count. Fine.

**Else.** The refusal table is good.

## test_scenarios.py

**Count and kind.** 16 tests, none parametrised. Each passage test loads the whole chart (cost not measured). The file proves that each block's scenario loads with its ports, marks, tide and book, and that the scenario writer round-trips.

**(c)** Seven tests have one shape: `test_the_channel_east...`, `_strait...`, `portugal...`, `spithead...`, `mahon...`, `tarragona...`, `bona...` and `the_faro...` (lines 21-532). Each one:

1. loads;
2. checks the chart name, seed and orders file;
3. checks the level and depth at the start;
4. checks the list of ports;
5. checks the feature by name;
6. checks the distance band;
7. checks the tide area;
8. asserts `begin(...) >= 10` and that no order was rejected.

One table-driven test would hold them.

**Else.**
- Lines 52-57 of the Channel-east test assert facts about the Strait's weather box (`box_at(36.2, -5.5)`), which has nothing to do with Channel east. The orphaned comment at 51 ("the book is read whole") sits above them. They are misplaced from the Strait test. Low, sure.
- Line 303 uses relative paths (`"data/scenarios/merchant-brig.yaml"`) where the rest use ROOT, so it depends on the working directory.
- Line 309 asserts that the merchant brig's `ration.table == "navy"`, though the docstring says "a merchant's stores". It may be a ration pattern; a suspicion.
- Line 166: `len(kept) > len(old) - 40`, a loose band.

## test_schooner_mast.py

**Count and kind.** 25 tests, 74 cases. Two families run over all 18 ship files (`SHIP_FILES`), 36 cases between them. No fixtures. Two tests sail the trial-B fixture for 2,400 s and then tack it (492, 617); neither is slow-marked. The file proves the "schooner's mast" rule at its three places, the short after-swing, the haul's words, and the gale's after-sail lines.

**(b)**
- Line 201 pins `len(SHIP_FILES) == 18`. The count is repinned with every new ship ("Old: seventeen files"). It guards that the guard is not empty, which `>=` would do as well.
- Line 537: `15 <= ... <= 35` against a measured 24. Line 538: `90 <= ... <= 240` against a measured 164, which barely excludes the old 289. Line 665: `90 <= ... <= 180` against 151, the old value being 219. These bands are fair.

**(c)**
- `test_trial_a_classes_as_it_did_before_the_rule` (246) asserts the same row as the parametrised `test_each_rig_is_classed...[fore course (trial A)]` (221).
- `test_only_the_neufchatel_swings_her_after_yards_short` (580) loads all 18 files again, after the guard (178).

**Else.** `test_the_polacre...` (270) says of itself that it is "a record of the reading ... more than a test of the rule". The two tack tests are good, measured end-to-end tests.

## test_sea.py

**Count and kind.** 23 tests, 27 cases. No fixtures. Sailed tests: three frigates of 2,100 ticks (398), two days of 6 hours (691), 7 hours (615), 4 hours (603), and reefs (342). Six are slow-listed. The file proves the sea's build, decay and swell, the motion, the consequences (reef, strain, head-sea, glass), readings, dialect, lines and determinism.

**(a)** `test_the_hooks_for_5b_are_numbers_that_nothing_reads_yet` (461): `Sea.horizon_nm` (freesail/world/sea.py:374) and `Motion.sight_error_factor` (freesail/physics/motion.py:343) are read by no code at M7. Every other `horizon_nm(` call is geo's function. The test keeps numbers alive that 5b was to wire and never did. Either the hooks are dead or a promised effect (a seaway shortening the horizon and spoiling sights) is missing. Weight low as a test, medium as a gap a player would notice; sure.

**(b)**
- Line 636: `assert all(e.data["sea"] == e.data["sea"] and "sea" in e.text for e in hours)`. The first clause is a tautology. Nothing checks that `hours` is non-empty, or that the data's sea is the sea's words. Weight medium, sure. Fault 1 below.
- Line 679: `ln.startswith("A ") and " sea" in ln or "swell" in ln`. By precedence this takes any line containing "swell". Low.
- Line 518: `0.2 <= leeward <= 1.5`, and 520: a bearing between 135 and 270 degrees. Loose, but argued.

**Else.** `test_the_strain_reads_the_motion...` (357) and `test_a_reef_takes_half_as_long_again...` (342) isolate a consequence cleanly; they are good.

## test_seat_hook.py

**Count and kind.** 3 tests, none parametrised. The file proves the director's seat and unseat world orders, the budget stand-down through the server, and the live `world:` prefix with its replay.

**(b)** Line 68: the "for no samples" refusal checks only `result == "refused"`, not its words.

**(c)** Lines 48-92 are a chain of fifteen refusals and grants in one test. A failure at refusal 3 hides refusals 4 to 15. They want a table.

**Else.** Sound.

## test_server.py

**Count and kind.** 31 tests, 61 cases. The function-scoped `world` fixture is parametrised over two ships, and every test using `world` or `client` runs twice. Each `client` starts a TestClient. The file proves the routes, the websocket, the snapshot and graph shapes, saving, loading, completion, the library, the papers, ease-on-station and the chart marks.

**(b)**
- `test_the_server_takes_the_ease_on_station_flag` (677-686) asserts that `"ease_on_station=args.ease_on_station" in inspect.getsource(server.main)`. It tests the source text, not the behaviour. Weight medium, sure. Fault 5 below.
- `test_the_client_has_the_charts_tools` (800-816) and `test_the_client_has_the_shelf` (702) grep the client's HTML and JS for identifiers (`drawRose`, `BEARING_FULL_S`). That proves the names are present, not that the code works.
- Line 587: `keeper = "purser" if world.people.find("the purser") is not None else "mate"` derives the expectation from the world under test.

**(c)** Ship-independent tests run twice through the `client` fixture: `test_index_serves_the_client`, `test_client_has_no_network...` (no fixture, once), `test_the_client_has_the_shelf`, `test_the_client_has_the_charts_tools`, and `test_a_mark_that_does_not_read...` (8 × 2 = 16 cases). `test_the_library_routes...` (485) walks the whole library twice, once per ship. About 25 cases are duplicates.

**Else.** `test_the_marks_are_laid_listed_and_rubbed_out` (721) proves that the marks touch neither digest nor journal; it is good.

## test_service.py

**Count and kind.** 6 tests, none parametrised. The file proves `service_of` and `under_the_regulations` by their four sources. Sound. Line 73 checks the role table against the doctrine's roles, which is a good drift guard.

## test_settee.py

**Count and kind.** 37 tests, 78 cases. No module fixtures. `_world()` builds the brig-with-settee fixture from a file and sails it 1,200 or 2,400 s, and it is called in about 26 cases:

- `test_hove_to...` ×2 (2,400 s each);
- `test_the_untried_manoeuvres...` ×7 (1,200 s);
- `test_in_stays...` ×2 (1,200 s);
- truth 7-198 ×2 and 7-199 ×2 (2,400 s each);
- `test_box_hauled_in_a_light_air` (2,400 s);
- about eight single tests at 1,200 s each;
- `test_the_luggers_tack_and_wear` ×2 (2,400 s, the lugger).

That is roughly 45,000 crewed ticks in the fast tier. No test here is in SLOW_TESTS or DAY_FIXTURES. The file proves the settee's own evolutions, its exclusion from the lugger's paths, its handling in stays, wearing, heave-to, fill away, box-off and forced round, and drafts truths 7-198 and 7-199.

**(a)** The docstring at 23 says "None of the committed files carries a settee ... so the tests run on the fixture". `data/ships/bilander.yaml:313-318` is a settee (`settee: true`), and lines 1188-1189 and 1314 point to `tests/test_bilander.py` for "her file's case". The premise is stale; truths 7-198 and 7-199 are still pinned on the fixture "to be measured again on the bilander's file". Weight low, sure.

**(b)**
- Lines 1306-1308: `scripts.settees_held(brig) == set()` is asserted, and then `settees_held` is monkeypatched to `lambda ship: set()` and the holds compared. The patch swaps a function that returns `set()` for one that returns `set()`, so the comparison cannot differ. The case is meant to show "a ship with no settee holds what she held". It shows nothing beyond line 1306. Low, sure.
- `LUGGER_TACK` and `LUGGER_WEAR` (1387-1425) are two whole-trace pins (lines and ticks) of the lugger's tack and wear. They are justified as a no-change trace of the settee step, but they break on any wording change to the lugger's manoeuvres. Two pins.
- Pins of geometry: 383 (12.24), 387 (-14.26), 388 (2.21). Pins of time: 226 ([30, 75, 75]), 232 (`SETTEE_DIP_S == 120.0`), and 251/280/300/311 (tick counts 135, 180, 105 and 210, derived in comments from the files' steps).
- `test_hove_to...` parametrises `SETTEE_KEPT_HOVE_TO` both ways (538). The False branch is the road not shipped, kept alive by the test.

**(c)** Twenty-odd fresh settles from the same scenario and seed. A module-scoped settled World, copied per test (the checkpoint pickle exists), would save most of the cost if it is shown to be equivalent.

**Else.** The fill-away cases (888-980) and the forced-round tests (983-1131) prove hard sequencing exactly; they are good. Their docstrings are long histories of reviews, which a builder must read to see what is asserted.

## test_settings.py

**Count and kind.** 9 tests, 14 cases. The file proves the settings file's paths by platform, the refusal of keys, the desktop client's entries and the config merge. It tests the tooling, not the game.

**Else.** `test_the_settings_and_the_players_places_are_never_inside_the_repository` (144) calls `save_settings(S.DEFAULTS, ROOT / "settings.yaml")`. If the refusal ever broke, the test would write into the repository. Low. Otherwise sound.

## test_ship_loader.py

**Count and kind.** 18 tests, 48 cases. The file proves the loader's indexing, defaults, refusals in words, the running bowsprit, rake, and the four reference ships' shape.

**(b)** Lines 135-136: one warning per class. If there were no warnings it would pass on empty lists, but 137 requires a brace warning. Fine.

**(c)** `test_frigate_particulars_stay_in_period` (380) repeats three checks of test_ship_particulars.py, and says so.

**Else.**
- `test_every_text_file_is_kept_with_lf_endings_by_the_attributes` (433) checks the repository's `.gitattributes` and walks the whole tree for CR bytes. It tests the repository, not the loader, and belongs in a hygiene file.
- `SHIPS` (216) checks only four of the 18 files' structure.

## test_ship_particulars.py

**Count and kind.** 19 tests, 24 cases. Six module fixtures, each a cheap `load_ship`. `test_generator_reproduces_the_committed_files` runs `tools/gen_ships.py` in a subprocess and compares every file. The file proves the ship files' figures against period ranges, and that the generator is the source.

**(a)** The docstring at 10-12 is stale: "the source of all six files ... the last test regenerates them". There are 18 files, and the last test is the forward-slash one. Lines 374-377 are an empty section header left behind. Low.

**Else.** The generator test (555) is a strong guard, both ways. The range tests are argued from sources line by line.

## test_ships.py

**Count and kind.** 29 tests, 32 cases. No fixtures. `_under_way()` sails 1,500 ticks and is called in about 15 tests (three of them parametrised ×2). `test_two_worlds...` sails 90 minutes twice; `test_the_lookout_hails...` up to 600 minutes. None is slow-listed. The file proves the far-detail vessel (polar, goals, cadence, level of detail), the lookout's words, the chart's privacy and the helm's judgement of courses across the wind.

**(a)/(b)**
- Line 251: `assert "milestone 6" in (S.Vessel.promote.__doc__ or "")`. It asserts text in a docstring. The docstring (freesail/world/ships.py:1095-1097) says the crewed promotion "and the rules-based captain who fights or evades are milestone 6's; this switch ... does nothing more than the cadence". That was true before M6 and is stale now; the test keeps it from being corrected. Weight low, sure.
- Lines 91-93: `S.polar_of.cache_clear(); again = S.polar_of(FRIGATE); assert again.speeds_kn == S.polar_of(FRIGATE).speeds_kn`. The second call returns the cached `again`, so the test compares an object with itself. "Drawn once and the same again" is not tested. Low, sure.
- Line 413: `abs(estimate / truth - 1.0) < 0.6` accepts 0.4 to 1.6 times the truth. That proves only "an estimate, not the truth" in the weakest sense. Line 287 hedges `eye ... else 30.0`.
- Lines 420-421 read `client/map.js` for `"ESTIMATE_DOUBT = 0.15"`, the text of the client.
- Lines 386-391 give three standing orders and assert only that they were accepted, not that they fire.

**(c)** `_under_way(25.0)` (frigate) is sailed afresh in about ten tests for one order each. A module-scoped settled World, copied, would do.

**Else.** The helm-judgement tests (547-783) are exact about words and outcomes; they are good.

## test_ships_hierarchy.py

**Count and kind.** 10 tests, none parametrised. Eleven module fixtures, sweeps and polars of six ships (slow tier). The file proves the ships' relative pointing and beam-reach speed (truths 73 to 76, extended).

**(c)** The fixtures `frigate_sweep`, `schooner_sweep` and `frigate_polar` here sail the same thing as the same-named fixtures in test_known_truths.py (conftest.py:47-49), a second time in another module. Sharing them through a conftest-level session fixture would save three slow sweeps.

**(b)/Else.**
- Line 124 allows the cutter to be a degree *worse* than the schooner under a truth worded "as close or closer". That is a tolerance, and it is stated.
- `test_the_four_ships_stand_in_order...` (154): the docstring says "every one under her hull speed". The body asserts only `brig < 9.5` (the cutter's hull speed) and never checks each ship against her own. It also repeats truths 75 and 76.

## test_sights.py

**Count and kind.** 7 tests. The noon sight's time, the sky's refusal, the error by instrument, skill and sea, and the order.

**(b)**
- Lines 181-182: `with pytest.raises(OrderError): raise OrderError("placeholder")  # the orders' refusal path is tested above`. The test raises its own exception and catches it. It is a dead line that reads as a check. Weight low, sure.
- Line 105: the comment says "'2 to 5 miles with a good horizon', the sextant's end", while the band is `1.5 < sextant < 2.5`. The comment and the band disagree about what the source allows.
- `test_the_sky_pinned_thick...` (169) never orders a sight in the fog; it checks only `sky_allows` directly.

**Else.** `spread()` over 400 seeds per case is a fair statistical test.

## test_signals.py

**Count and kind.** 20 tests, 32 cases. The checker runs over 6 roots, the read-by-own-book test over 5, and the convoy over 4 roots (half an hour each, slow-listed). One module fixture, `_a_frigate`, from `tools/check_signals.py`. The file proves the books' shape, numbers and finding, the telegraph, the private tables, colours, hoists seen and read by range and time, the hail's tables, and the hail's grammar.

**(b)** Line 25 pins `hoist_s == 60`, `read_s == 60` and `read_nm == 2.0` for every root, constants alike across nations. Line 171 asserts only `far` (non-empty). Low.

**Else.** `test_the_checker_passes_every_root` (686) is a strong data guard that needs no edit for a new nation. The hail grammar tests (492-611) list exact phrasings; they are good. The parametrised slow ids in conftest match the five roots present.

## test_squadrons.py

**Count and kind.** 21 tests, none parametrised. No fixtures. Several long runs, none slow-marked:

- 10,800 + 1,800 s (109);
- 12,900 s (263);
- 7,200 + 2,400 s (452);
- 3,600 + 600 + 3,600 × 2 s (805);
- 4,200 s plus up to 4,800 s (533);
- two `world_with("on")` business worlds from test_business, whose own fixture conftest calls "8 to 11 s loaded".

These are far-detail runs, so perhaps cheaper; I did not measure. The file proves the squadron set, formations, pace cap, stragglers, divisions, the commodore's book, the cut-out, succession by the wake, the regimes and the business.

**(b)**
- Line 530: `assert all(v.brain is None for v in ordinary) and hulk.position == hulk.position`. The second clause is a tautology; the hulk's staying at anchor is not tested. Weight medium, sure. Fault 6 below.
- Lines 179-181: `sq.under(harpy.id) == [...] or (lead in sq.under(harpy.id) and other not in sq.under(harpy.id))`. The looser second branch makes the first moot.
- Lines 798-800: `old = getattr(Q, "_LAST_COURSE", None); if isinstance(old, dict): old.update(...)`. The table is gone (freesail/world/squadrons.py:1431 now keeps the courses on the World), so the "stale course planted" step never runs. The test's docstring claims it. Only line 802's check that no module table is left carries weight. Low, sure.
- Line 345: `len(read) >= 2` of four merchantmen. Line 256: `pytest.raises(Exception, match="no kind")`, which is broad.

**Else.** `test_a_merchantman_brought_to_by_a_privateer...` (351) proves the full prize record exactly; it is good.

## test_stand_by_words_and_action_flow.py

**Count and kind.** 5 tests. The stand-by's answers at two doors, the fire's severity, the yards' severity at quarters, and the signal book's page.

**(b)**
- Lines 106-108 check that every fired minute's severity matches the rule. Nothing requires that a routine minute (a miss) occurs, so the routine branch may never be exercised. A suspicion.
- Line 88: `"true_wind" in first_text or "heading" in first_text`. Loose.
- Line 147 pins the words "The Britain signal books", a slip of the adjective that the test now holds in place.

**Else.** The file's name joins three unrelated subjects (doors, gunfire, signal book). A builder looking for the fire's severity would not look here.

---

## Faults to plant

Under (b), each nominated test is followed by the fault to plant, what the test says it guards, and my prediction.

1. **tests/test_sea.py::test_the_log_says_the_sea_when_its_words_change_and_the_rollup_says_it_by_the_hour**
   - Fault: in freesail/core/world.py line 1855, change `data["sea"] = self.sea.words` to `data["sea"] = self.motion.words`.
   - What the test names: the hourly line carries the sea for the roll-up (line 636).
   - Prediction: **passes although the game is broken.** Line 636 compares the field with itself; the text at 1857 still says "sea"; the roll-up check at 669 needs only " sea" anywhere in a roll-up.
2. **tests/test_sail_by_name.py::test_the_bearing_and_the_distance_pick_the_far_sail_on_the_same_bearing**
   - Fault: in freesail/orders/navigation.py line 1657, change `which = _sail_and_rest(order.verb_phrase, rest)` to `which = _sail_and_rest(order.verb_phrase, rest.split(" distant")[0])`, so that `give chase` drops the distance clause.
   - What the test names: "the glass, the bearing and the chase take the same words". The chase should take the Wasp at two miles.
   - Prediction: **passes although the game is broken.** The chase takes the nearer Raven, also bearing NE, so line 163's "bearing NE" holds, and line 164 defaults to "wasp".
3. **tests/test_rig_geometry.py::test_close_hauled_forces_are_unchanged_without_bowlines**
   - Fault: in freesail/physics/sails.py line 209, change `return c_l, c_d` to `return c_l * 1.1, c_d`.
   - What the test names: the forces with no bowline are milestone 2's "to the last newton".
   - Prediction: **passes** (both calls take the same branch). test_sails.py::test_curves_interpolate_and_fold should fail at line 93.
4. **tests/test_routine.py::test_three_calls_in_the_middle_watch_leave_the_morning_watch_tired**
   - Fault: in freesail/crew/hands.py line 50, change `FATIGUE_WEIGHT = 0.5` to `FATIGUE_WEIGHT = 0.9`.
   - What the test names: a night of three calls costs "about a sixth of the morning's pace", band 1.10 to 1.25.
   - Prediction: **passes** (the test uses its own copy, 0.5). The code's term becomes 1 + 0.9 × 0.29 = 1.26, outside the truth's band. Other files may catch it.
5. **tests/test_server.py::test_the_server_takes_the_ease_on_station_flag**
   - Fault: in freesail/ui/server.py line 1860, change `ease_on_station=args.ease_on_station,` to `ease_on_station=args.ease_on_station and False,`.
   - What the test names: `--ease-on-station` on the command line reaches the driver.
   - Prediction: **passes although the flag is dead.** The source still contains the substring.
6. **tests/test_squadrons.py::test_the_business_draws_a_convoy_a_blockade_and_a_ship_in_ordinary_by_the_nations_knobs**
   - Fault: in freesail/world/ships.py, make a ship at anchor drift. Between line 900 and the `return` at 901, insert `self.position = destination(self.position, 90.0, 5.0)`, with `destination` imported from `freesail.world.geo`.
   - What the test names: the hulk in ordinary stays at anchor through 1,800 s (line 530).
   - Prediction: **passes.** `hulk.position == hulk.position` holds whatever the position.

**Faults in behaviour that I believe no test in my files would catch, though a player would:**

- **A.** The hourly weather line's data sea swapped for the motion's words (Fault 1). The roll-up a player reads at speed would carry "rolling heavily" where the sea's words belong.
- **B.** `give chase to the brig bearing NE distant two miles` chasing the nearer brig on the same bearing (Fault 2). The player chases the wrong ship.
- **C.** The fatigue weight or the fresh threshold in freesail/crew/hands.py:426 (for example `- FATIGUE_FRESH` dropped). Every tired crew works slower, and test_routine's band would still pass because it never calls the code.

## What I did not read

- `tests/rig_fixtures.py`: I read only its list of definitions, not its body.
- `tests/test_bilander.py` and `tests/test_indefatigable.py`, which my files point to.
- The helper builders imported from other test files: `test_known_truths` (`_gerrans_world`, `pointing_sweep`, `polar`, `_two_cutters_at_pistol_shot`, `_captain_standing_by_a_glass`), `test_crews.hove_to_world`, `test_brains.put/world_at`, `test_business.world_with`, `test_wardroom_doors`, `test_agents`, `test_local_runner`, `test_weather.gate_systems`, `test_observer`, `test_hands.sailor`, `test_grammar_book`, and `messages_api`.
- `tools/regatta.py` and `tools/check_signals.py` beyond the names the tests call.

I measured no durations. Every claim above about the fast tier's cost is a suspicion from tick counts, except the stale node id, which is sure.
