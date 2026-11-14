# Tests, reader 04: test_browser_probe to test_director (26 files)

Read whole, first line to last, at commit 504a250: `tests/conftest.py` and the 26 files below.
Nothing was run but short reads (a grep, `ast` counts of `def test_`, a few seconds of python
to count the director's forms and the browser plans, `ls` of `tests/fixtures/saves/`). The
suite was not run. No file under docs/dev, docs/design, docs/playtests or docs/gates was
opened; one test reads a file under docs/playtests and I say so without opening it.

Code read to judge a test: `tests/test_primer.py` 125-170 (the InstantRunner),
`freesail/orders/verbs.py` 376-441, `freesail/world/dealings.py` 860-868, `freesail/world/
orders.py` 3565-3571, `freesail/ui/console.py` 1205-1213, `freesail/world/crews.py` 118-126 and
892, `data/charts/audit-known.yaml` 15-19, `data/evolutions/*.yaml` (grep for `aloft: true`).

## The table

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_browser_probe.py | 68 | 2 (13) | `probe_browser`: Chromium, a game served per plan | sound; tests the probe tool and its plans |
| test_business.py | 547 | 15 | `busy`: a region peopled (8-11 s) | sound in the main; one fixture mutated across tests; an `if ...: continue` escape |
| test_canvas.py | 668 | 27 (36) | none module-scoped; four 40-minute gales | two tests are one test twice; one test asserts nothing its name says |
| test_captain.py | 690 | 18 | none; 90-minute and 2-hour passages, sailed twice each | sound behaviour; two source-text tests prove nothing of behaviour |
| test_captain_rules.py | 309 | 9 | none | sound; unit tests of private methods with `give` faked |
| test_captain_trials.py | 552 | 8 | five trials, 20 h of game each | pins much, proves little; one name says the opposite of its body; one digest dropped |
| test_captains.py | 624 | 16 | `under_way`: 19,600 s sailed, fast tier | sound mostly; a source grep; a tautology |
| test_captive.py | 629 | 12 | none; the same struck-ship scene built 14 times | sound behaviour; duplicates its own scene; `slow` marked in the file |
| test_catalogue.py | 1013 | 33 (57) | none; several 30-minute gales | an aloft check that checks five files; a strict xfail of a broken evolution since 37p |
| test_chart.py | 2421 | 60 (74) | `chart`, `manifest`, `whole` | tests data and the build tool; wall-clock asserts in the fast tier; block families want a table |
| test_chart_audit.py | 294 | 14 | `sampled`: the audit on its grid | tests a tool; one test pins a known data fault as expected |
| test_check_viewer_guns.py | 70 | 4 (21) | none | sound; tests a tool over the data |
| test_checkpoint.py | 550 | 16 (22) | `saved`: 4 h of the gate-5b passage | sound; one test depends on a file under docs/playtests |
| test_complete.py | 164 | 11 | none | sound; runs on the M1 point ship and a fake runner |
| test_consent.py | 519 | 22 (31) | none | sound; the vendor-free test's list is stale |
| test_console.py | 83 | 6 | none | sound; on the point ship |
| test_context_budget.py | 158 | 6 | none | tests a tool and a document |
| test_core.py | 71 | 5 | none | sound |
| test_court.py | 510 | 7 | none; the captive scene again | one 170-line story test; `slow` marked in the file |
| test_crew_model.py | 502 | 27 (28) | `frigate_crew`, `schooner_crew` (cheap) | sound; one golden muster text |
| test_crew_orders.py | 392 | 21 (32) | none | sound; one assertion reads the fake runner's own effect |
| test_crews.py | 1079 | 24 | none; many 400-minute loops | sound behaviour; or-escapes; a band looser than its docstring |
| test_damage_control.py | 328 | 10 | none | sound |
| test_date_and_war.py | 125 | 3 | none | one test performs the hook itself and asserts what it wrote |
| test_determinism.py | 37 | 3 | none | runs the point ship only; little left of the game in it |
| test_director.py | 1823 | 53 (57) | none | sound in the main; a vacuous check; 25 excused examples |

## tests/conftest.py (the tiers)

- The docstring (line 6) says "The `slow` mark is applied here and never in a test file".
  It is applied in test files: `test_captive.py:515, 568`, `test_chart_audit.py:91`,
  `test_court.py:43, 264, 355, 450`. Weight low (the rule is the project's own and is broken
  silently); sure.
- `DAY_FIXTURES` says the captain's trials are "16 hours each" (line 73); the file sails
  `HOURS = 20` (`test_captain_trials.py:20`). Low; sure.
- `test_captains.py`'s `under_way` (19,600 s of the intent scenario with the rules captain)
  is in no `DAY_FIXTURES` entry, so its two tests run in the fast tier. Whether it is over
  the 5 s threshold I did not measure. Low; a suspicion.
- Line 715 builds `set(others)` for every item (quadratic over the collection). Low; sure.
- `SLOW_TESTS` names for my files all still exist (checked by `ast`).

## test_browser_probe.py (68 lines)

1. 2 tests; one parametrised over the 12 plan files in `tests/browser_plans/` (13 cases).
   `probe_browser` launches Chromium once for the module. Proves the probe's plans play
   at the real page.
2. (a) None.
3. (b) `probe_browser` skips on any launch exception (line 33). With Playwright installed
   on this machine it will run; a broken browser install shows as a skip, not a failure.
   Low; sure.
4. (c) None.
5. A file that tests a tool (`tools/browser_probe.py`) and its plans. The real assertion is
   inside `run_plan`; the failure message prints the plan's lines, which is good.

## test_business.py (547 lines)

1. 15 tests. `busy` (module): a region peopled at seed 7. Proves the business draw, its
   cargoes, cruisers, fishermen, rumours, transactions and far traders.
2. (a) `test_a_fisherman_works_her_ground...` line 197 asserts `CR.FAR_ONLY_ROLES ==
   frozenset()`. The constant (`freesail/world/crews.py:126`) is an empty frozenset kept
   and read at line 892 to exclude nothing. A removed feature's shell pinned empty by a
   test. Low; sure.
3. (b)
   - `test_every_cargo_goes_from_where_it_is_cheap...` line 136: `if m is None: continue`.
     Any trader whose intent is not "trade N tons of X from A to Z" is skipped; if every
     trader were drawn in another form the price check runs on nothing and the test passes
     on `assert traders` alone. Medium; likely.
   - `test_the_draw_is_the_seeds_and_moves_no_other_draw` line 211 compares one number of
     one stream ("weather"). A business that drew from "lookout" or "muster" passes. Low;
     sure.
   - `test_a_ship_bound_beyond_the_region...` lines 232-247 monkeypatch `Business.data` and
     tick the module's shared `busy`, adding drawn ships that are never removed; later tests
     on `busy` (`test_the_quays_rumours...`, `test_a_dated_entry...`) see a world other
     than the one their docstrings describe. Order-dependent. Low; sure.
   - `test_a_far_trader_at_her_port...` lines 488-493: the cargo check runs only `if
     brain.intent.kind == "trade"`; a "passage" home skips it. Low; sure.
   - Same test, lines 512-523: `B.load_business` is replaced on the module by assignment
     (not monkeypatch) and its cache cleared; restored in `finally`. Works, but a failure
     before `try` would leak. Low.
4. (c) `test_the_boat_ashore_brings_the_rumours_off...` sails two worlds to anchor in
   Carrick Road (36 s, in `SLOW_TESTS`); `test_captain_rules.py` and `test_crews.py` build
   the same anchorage. Low.
5. `test_the_draw_peoples_the_region...` (105) and `test_the_cruisers_keep_the_stations...`
   (147) are good checks of data against doctrine.

## test_canvas.py (668 lines)

1. 27 tests (36 cases, three parametrised over the four ships). No module fixtures; the
   gale helper sails 2,400 ticks of the frigate in 35 knots, four times across two tests.
   Proves canvas numbers, wear, the sail room, storm canvas and truth 27's mechanism.
2. (a)
   - `test_new_parts_do_not_change_the_ratings_of_the_old_spars` (583): the name and the
     docstring say every spar keeps its rating; the body asserts there is one ringtail boom
     and its rating is at least 1.0. No old spar's rating is compared with anything.
     Medium; sure.
   - `test_no_2_canvas_is_the_anchor_of_the_derivation` (135) is parametrised over four
     ships but `M2_NO2_RATINGS` holds only two; for the cutter and the brig the body asserts
     the constant `== 0.32` and nothing else. Low; sure.
   - `test_the_muster_and_the_sail_room_query_lines` line 458 comment "the lead wires this
     into the session (package 22 report)": stale, it is wired (line 460 passes on it). Low.
   - `test_orders_still_reach_the_square_sail_scripts` line 662 loads a ship and discards it
     at 665. Dead line. Low.
3. (b)
   - `test_every_sail_has_a_canvas_number...` (153) recomputes the rating with the code's
     own formula and the code's own `storm_cloth_rating_for` (163); it checks the loader
     applies the formula, not that the formula is right. Low; sure.
   - `test_no_2_canvas...` line 149 compares to milestone 2's values times 0.32/0.9 within
     0.15 kN: a band derived from the current code's anchor. Low.
4. (c) `test_worn_canvas_goes_before_its_spar...` (319) calls `gale_royals(100.0,
   TRUTH_27_NO2_KN_PER_M2)` with `TRUTH_27_NO2_KN_PER_M2 = 0.32` (278), and the scale
   factor is `0.32 / CLOTH_KN_PER_M2_NO2` = `0.32 / 0.32` = 1.0 (line 143 asserts the
   constant is 0.32). So it is exactly `test_truth_27_with_the_ship_files_ratings` (328):
   the same four gales, the same assertions. Both are in `SLOW_TESTS`, and truth 27 has its
   own test in `test_known_truths.py` (named in `SLOW_TESTS` line 289). Three runs of one
   scenario. Medium (slow-tier time); sure.
   `test_a_ship_file_with_only_a_count_has_made_up_sails` (390) and
   `test_catalogue.py::test_spare_sails_come_from_the_crew_section...` (535) test the
   count-only stores form with a `SimpleNamespace`; the loader refuses a count beside the
   list (`test_canvas.py:615`). Whether any ship file still uses the count alone I did not
   check. Low; a suspicion.
5. `test_the_effective_rating_and_blowing_out_of_a_worn_sail` (234) is a good unit test of
   the mechanism.

## test_captain.py (690 lines)

1. 18 tests, no module fixtures. Two tests sail the merchant passage 90 minutes twice and
   one two hours twice (base and seated). Proves the captain's station, the deck by right,
   hand-over, stand-down, the player's seat and replay with both seated.
2. (a) None found.
3. (b)
   - `test_the_doors_name_the_captains_station` (408) and
     `test_the_console_and_the_server_take_the_seat_flag` (631) read the source text of
     `mcp_server.py`, `local.py`, `console.py`, `server.py` and assert strings
     (`'"--seat"' in src and "seat.route(" in src`). The flag could be parsed and ignored,
     and they pass. Medium; sure (fault 4 below).
   - `test_a_silent_captains_door...` line 209: `all(a.startswith("captain") for _, a, _
     in world.journal)` is meant to say "nothing of his journaled", but the rules' actor is
     `"captain's rule ..."` (line 207), which also starts with "captain". A rules judgement
     journaled by mistake passes. Line 156's `<= {"captain"}` is the strict form and passes
     on an empty journal. Medium; sure.
   - `test_the_captains_brief_head...` line 186 pins `"primer 17"` and `"primer 16"` in the
     brief: document numbering, not behaviour. Low.
4. (c) The player's seat is proved in four tests here (514, 563, 596, 642) and again in
   `test_checkpoint.py:385`. Not excessive.
5. `test_a_silent_captain_on_a_book_scenario...` (219) and `test_the_fake_captain_gives_six
   _orders...` (235) compare the whole log line for line with an unseated run: strong.

## test_captain_rules.py (309 lines)

1. 9 tests, none heavy (a quarter hour of sailing per world). Proves put-about choice, the
   trend, the gale lines, sail after the gale, the port's reach.
2. (a) None.
3. (b) Lines 143 and 191 pin the doctrine's thresholds `(40.0, 32.0, 6.0, 4.0, 10.0)` and
   `(25.0, 30.0, 10.0, 15.0)`, read from the data under test. The pin is harmless (the
   later lines use the read values) but a doctrine change fails the test for no fault.
   Low; sure. `cap.give` is replaced by a recorder (187, 236, 272): the rule's choice is
   tested, not that the order is given. Acceptable for a unit test.
4. (c) None.
5. Sound. The tests call private methods (`_read_trend`, `_weather_work`, `_stimulus`) and
   set private state (line 117); a refactor breaks them without a fault.

## test_captain_trials.py (552 lines)

1. 8 tests. Five module fixtures, each 20 hours of a trial scenario (`station_stranger`,
   `station_gale`, `station_lee_shore`, `trade_stranger`, `trade_thick`), all slow. Proves
   the rules captain under weather and strangers, and the player's hand (three fast tests).
2. (a)
   - `test_the_merchant_hauls_off_from_a_privateer_and_waits_in_the_road_for_a_wind` (381):
     the name says she waits in the road; the docstring (387-388) says "she comes to an
     anchor in the outer road and is in port from it at the end". The body asserts the
     opposite: `anchored == []` (400, `TRIAL_TRADE_STRANGER_ANCHORED_TICKS: list[int] = []`),
     `len(waits) == 0` (407), `cap.state == "on passage"` (413). The trial now never reaches
     the road; the test was re-pinned to that and kept its name. Medium; sure.
   - `TRIAL_STATION_STRANGER_WITHIN_HAIL_TICKS: list[int] = []` (72) makes line 109 assert
     that she is never within hail of the stranger she chases. Low; sure.
3. (b) Pins: 4 digests asserted (113, 204, 415, 464), 5 line counts (112, 203, 278, 414,
   463), 5 exact state-and-tick lists. The comments (45-85, 116-170, 207-260, 288-373,
   419-443) record each re-pin by package: the figures are whatever the code last gave,
   with the reason in a note a reader cannot check here. The properties a player would
   care about (never aground, the chase, in port) are a few lines among the pins.
   - `test_with_ushant_under_her_lee...` line 283: `assert len(w.log.digest()) >= 16`. The
     digest is read and nothing asserted of it; the comment (279-282) says the digest
     "differs by machine with the states and the line count the same". That is the code's
     own admission that a log digest is not the same across machines, which bears on every
     replay-by-digest claim in the project. Weight high for the determinism claim,
     low for this test; the machine dependence is likely (from the comment, not measured).
4. (c) Each trial is one fixture for one test: no waste. The three fast tests each sail
   `intent_world()` six hours (470-477) separately; one module fixture would serve two of
   them (they mutate it, so not trivially). Low.
5. Failure messages: `states(w) == TRIAL_...` prints two long lists; a reader cannot tell a
   real fault from a harmless change of one tick. This file is the clearest case in my list
   of "pins much, proves little".

## test_captains.py (624 lines)

1. 16 tests. `under_way` (module): the intent scenario to 19,600 s, fast tier. Proves the
   intent reader, the doctrine files, the planner, the state machine's books, perception,
   the rule of the road, the far-detail interface, 58b's sea sense.
2. (a) Line 435 `_ = destination`: an import kept alive by a dead line. Low.
3. (b)
   - `test_nothing_in_captains_reads_the_worlds_truth_by_any_road` (276): the first half
     greps `captains.py`'s source for eleven strings; `world.own.position`, a helper in
     another module, or `getattr` passes it. The second half (two ships, one account, equal
     perceptions) is a real test. Low; sure.
   - Line 311: `assert pa.tide_is("ebb") in (True, False)` holds for any boolean. Built not
     to fail. Low; sure.
   - Line 363: `bad.kind == "world.order_refused" or "no intent" in bad.text`. Low.
4. (c) `test_the_planner_joins_the_ports_tracks...` (148) and `test_the_captain_buys_the
   _cargo...` (213) both check the plan's marks; fine.
5. `test_every_book_line_of_every_doctrine_parses...` (112) is a good data test.

## test_captive.py (629 lines)

1. 12 tests; `_struck_to_a_crewed_frigate` (51) builds the scene (a French frigate crewed
   beside the player, the strike, the possession, up to 14 minutes) and is called 14 times
   in this file (lines 121, 180, 219, 234, 256, 298, 339, 370, 384, 427, 453, 504, 579, 610)
   and three more times by `test_court.py`. Proves the captive's channel.
2. (a) A section heading "the far body" (276) with nothing under it; its test is at 515.
   Low.
3. (b) Lines 451-452 pin `CAPTIVE_VERBS` and `CAPTIVE_STATION_VERBS` to literal sets. Low.
   Line 322-328 monkeypatches `person_of_actor` to test `hand_on_her` alone: fine.
4. (c) The scene is deterministic; seven tests that only read it (112, 173, 288's opening,
   360, 392, 440, 497) could share a module fixture of the scene after `w.run(120)` if they
   did not mutate it; most do, so the cost stands. Medium (time); sure.
5. `@pytest.mark.slow` at 515 and 568, against conftest's rule. The tests named after the
   owner's play (288, 331, 360, 392, 440) each state the defect they guard: good.

## test_catalogue.py (1013 lines)

1. 33 tests (57 cases). No module fixtures; the gale (`the_gale`, 1,800 ticks at 35 knots)
   twice, the handling scripts through the real world. Proves the evolution catalogue.
2. (a)
   - An empty section "The routine's two" (317-320): the tests it held are gone. Low; sure.
   - `test_milestone_2_timings_are_unchanged` (261): `M2_TIMINGS` has been amended at
     packages 32e, 37f, 37m, 75 (comments 75-142) with keys milestone 2 never had; the test
     compares the files with a copy of the files, edited whenever they change. The name
     promises milestone 2's figures frozen. Medium; sure.
   - `test_the_catalogue_reaches_forty...` line 238 `len(EVOLUTIONS) >= 39`. Low.
3. (b)
   - `test_aloft_flags_are_on_the_steps_aloft` line 275:
     `assert aloft == ALOFT_STEPS.get(data["id"], aloft)`. For every file not among the five
     in `ALOFT_STEPS`, the default is `aloft` itself, so the assertion is `aloft == aloft`.
     Of the twelve files with `aloft: true` (`ease_catharpins`, `furl_lateen`, `furl_settee`,
     `set_settee`, `rig_in/out_studdingsail_boom`, `swifter_in_catharpins`, ...) seven are
     checked by nothing. Lines 278-279 assert the test's own constant is non-empty. Medium;
     sure (fault 1).
   - `test_the_new_crew_lines_fit...` line 311: for the cutter `outcome in (ENOUGH, SHORT)`.
     Low.
   - `test_backing_and_filling_keeps_her_place...` (940-967): `xfail(strict=True)` since
     package 37p, "for the lead"; now package 100-plus. Strict xfail means any further
     break in `back and fill` is also an expected failure: the evolution is in the
     catalogue, the order starts it (`test_whole_ship_orders_start_their_evolution` case
     "back and fill"), and nothing proves it does what it says. Nobody could expect it
     mended from this file. Medium; sure.
4. (c) `test_sending_down_the_topgallant_masts_at_once...` (997) is truth 23's mechanism;
   `test_known_truths.py::test_truth_23...` sails the same gale (in `SLOW_TESTS`). The
   handling tests (816-938) overlap `test_staying.py`, `test_lying_to.py` (by their names
   in `SLOW_TESTS`; not read). Low; likely.
5. `test_whole_ship_orders_start_their_evolution` (726) is 16 cases of one parse each; fine
   as a table.

## test_chart.py (2421 lines)

1. 60 tests (74 cases: 12 shore places, 3 tracks). Module fixtures `chart`
   (channel-west), `manifest`, `whole` (atlantic-east, every region). Proves the chart
   data, the manifest's licences, the build tool's arithmetic and checks, the queries, the
   sea breeze and fog hooks, and each block's lights, depths and seams.
2. (a) None found; every block named is in the manifest list the test pins.
3. (b)
   - Wall-clock assertions in the fast tier: line 300 (`< 100e-6` a grounding check), 336
     (`< 150e-6`), 340 (`< 2e-3`). Under `-n 4` on loaded cores these are flaky, and the
     project's own conftest (`_is_pace`) says such figures read the load. Medium; sure.
   - Line 308-311: `aground(...) is not None or chart.depth_at(shoal) > 3.3`. Low.
   - Line 1056: `widened` lets either of two corridors pass, with two budgets. Low.
   - Count and value pins that grow with each block: the region list (929), the bounds
     (944-945), `222 of 222` (1301-1303), `len(lacking) == 27` (2287), tile counts (1510,
     1636, 1790-1791, 1913), exact light lists per block. About 25 such pins. They are
     data tests: each fails on a data change, not on a fault. Low.
   - Line 798 asserts the replaced code's defect is still present (`old_changes >= 20`).
     A mend of `coast_distance` fails this test. Low; sure.
4. (c) Each block (Channel east, Biscay north, Biscay south, Portugal, Strait, Channel's
   east block, Mediterranean west) has the same three tests: checks pass and tiles, lights
   of 1805, depths in its roads (1365-2248). One table-driven test per kind would hold all.
   And 20 tests call `load_chart(WHOLE)` afresh (1088, 1389, 1431, 1442, 1467, 1555, 1585,
   1637, 1684, 1729, 1817, 1830, 1865, 1953, 1988, 2073, 2116, 2204, 2227, 2269) though the
   module has the `whole` fixture (901). Medium (time); sure (whether the loader caches I did not check).
5. Several tests are of a tool (`tools/build_charts.py`, `tools/chart_manifest.py`) and one
   of a document: `test_the_manifest_lists_the_c7_checks...` (640) reads
   `docs/references/Charts.md`. `test_the_regions_tiles_are_present...` (177) runs
   `git ls-files`. `test_the_coasts_distance_at_the_ship...` (824) is a good regression
   test of a real fault (the plane's drift).

## test_chart_audit.py (294 lines)

1. 14 tests; `sampled` runs the audit on its grid once; `chart` loads atlantic-east.
   Proves the audit tool's checks by planting and its ratchet against the known list.
2. (a) None.
3. (b) `test_two_regions_claiming_the_same_water_are_found` (187) asserts the live data's
   finding `{"a-overlap:ligurian-sea+tyrrhenian"}`. That is a real fault in the chart
   (`data/charts/audit-known.yaml:15-19`: the Tyrrhenian's box drawn over the Ligurian
   sea's south, "the tide blends both blocks' gauges"), pinned as the expected answer.
   Mending the overlap fails this test. The ratchet itself (`test_the_sampled_audit_finds
   _nothing_the_known_list_lacks`) passes the 142 known findings by design. Medium; sure.
4. (c) None.
5. A file that tests a tool. `@pytest.mark.slow` at 91 against conftest's rule. The
   planting tests (121-268) are good: each plants a fault and asserts its key.

## test_check_viewer_guns.py (70 lines)

1. 4 tests (21 cases: 18 ship files). Proves the viewer's gun checker on every ship file.
2. (a) None. 3. (b) None. 4. (c) `test_the_checker_runs_clean_over_the_tree` (33) repeats
   the parametrised test in one call. Low.
5. A file that tests a tool. Sound.

## test_checkpoint.py (550 lines)

1. 16 tests (22 cases). `saved` (module): 3 h of the gate-5b passage with a fake watcher,
   saved, then a watch more. Proves the checkpoint, its refusal when foreign or tampered,
   the unpickler's allow-list, old saves read under this build.
2. (a) `make_the_37d_save` (282) is code no test runs, kept by design. The skip in
   `_playtest_save` (175-183) cannot fire: the saves are committed (`tests/fixtures/saves/`
   holds both). Low.
3. (b) Lines 346-352 and 370-377 branch on `same_build(...)`; under any later build the
   first branch never runs. Low; sure. Line 92 `load_s < replay_s / 5` is wall-clock, but
   in the slow tier.
4. (c) None of note.
5. `test_the_owners_tender_save_loads_and_replays_its_first_minutes_when_asked` (478) reads
   `docs/playtests/2026-10-25-to-27-owner-playtests-70-72/saves/m7-cutter-tender-test.json`
   (path at 489-491; I did not open it). A test that fails if a record directory is moved
   or pruned, and is not under `tests/fixtures/`. Medium; sure. The other old-save tests are
   good: they would catch a build that cannot read an old checkpoint.

## test_complete.py (164 lines)

1. 11 tests. Proves completion offers and that each offer parses.
2. (a) None.
3. (b) Lines 57-61: three `or`s where the third (`any("one reef" in x ...)`) holds whenever
   either of the first two does. Line 32 `"hold" in s or "go" in s`. Low. The `FakeRunner`
   (7-18) makes `handle` succeed whatever the runner would say; the test is of the parser,
   as its docstring says.
4. (c) None. 5. Sound.

## test_consent.py (519 lines)

1. 22 tests (31 cases). Proves the consent conversation, the record, the gate, the REPL door.
2. (a) `test_the_harness_and_the_consent_step_import_no_vendor` (500): the free list (506)
   names eight modules; `freesail/agents/` now also has `director`, `seat`, `remote`,
   `watches`, `tripwires`, `pictures`, unchecked. The banned list (518) is `mcp`,
   `mcp_types`, `httpx`; the vendor SDK named in `pyproject.toml:29` (
   imported in `freesail/agents/api.py:513, 937`) is not banned, so an import of that SDK in `harness.py`
   passes. The name promises "no vendor". Medium; sure (fault 5).
3. (b) None beyond that.
4. (c) None.
5. `test_the_brief_says_what_the_harness_does_in_its_own_numbers` (70) ties the brief's
   words to the code's constants: a good pattern.

## test_console.py (83 lines)

1. 6 tests. Proves the console's driver lines, save and replay, the roll-up, follow.
2. (a) `make_console` uses `World(seed=3)`, the milestone 1 point ship; the game is now
   played on ship files. Four of six tests test the console on a stand-in. Low; sure.
3. (b) None. 4. (c) None. 5. Sound as far as it goes.

## test_context_budget.py (158 lines)

1. 6 tests on a GGUF header the test writes byte by byte. Proves the context budget tool.
2. (a) None. 3. (b) `pytest.importorskip("gguf")` (17): installed here. None else.
4. (c) None.
5. A file that tests a tool; `test_harness_md_has_the_command...` (154) tests a document
   (`docs/agents/Harness.md`) for a date and a phrase. Low.

## test_core.py (71 lines)

1. 5 tests. Clock bells, rng streams, the log's queries and digest, the line format. Sound.

## test_court.py (510 lines)

1. 7 tests, four marked `slow` in the file (43, 264, 355, 450). The captive scene from
   `test_captive.py` again, landed at Brest.
2. (a) None.
3. (b) Line 85: `"lost no ship" in e.text or "No person" in e.text`. The docstring (49) says
   "refused for a man who lost no ship"; a refusal because the person is not found at all
   passes too. Low; likely.
4. (c) `test_the_court_martial_sits_by_the_form...` (44) is one 170-line story: the
   exchange, the court, the questions, the log read, the verdict, the new command, the
   scenario written, loaded and begun, the dismissal rules. A failure at line 190 tells a
   builder only that something between landing and the new ship's record differs.
   `test_a_new_command_names_its_file...` (279) re-proves the new command on a lighter
   scene. Medium; sure.
5. The file imports helpers from three other test modules (`tests.test_captive`,
   `tests.test_director`, `tests.test_brains`): the test files are a library to each other.

## test_crew_model.py (502 lines)

1. 27 tests (28 cases). `frigate_crew`, `schooner_crew` (module, cheap). Proves the crew
   section, the muster, the watch bill.
2. (a) None.
3. (b) `FRIGATE_MUSTER_SEED_7_FORENOON` (453-478): one golden text, names drawn at seed 7.
   A change of the names list fails it for no fault. Low. Line 258's counts are reasoned
   (largest remainder) in the comment: good.
4. (c) None. 5. Sound.

## test_crew_orders.py (392 lines)

1. 21 tests (32 cases). Proves the hands selector, a watch sent, all hands, pipe down,
   close reef, the state line, the snapshot's crew.
2. (a) None.
3. (b) `test_close_reef_after_one_reef_takes_the_rest` (279): `sail.reefs == sail.reef_bands`
   (289) is the InstantRunner's own `min(sail.reefs + n, sail.reef_bands)`
   (`tests/test_primer.py:165`), not the game's. The useful assertion is `params["reefs"]`
   (290), which reads `freesail/orders/verbs.py:385`. Low; sure.
   The test imports `from test_primer import make_ship` (280), a bare module name that
   works only with `tests/` on the path. Low.
4. (c) None. 5. Sound.

## test_crews.py (1079 lines)

1. 24 tests, no module fixtures; most sail `hove_to_world()` and then loop up to 400
   minutes for a demotion. Proves the crewed promotion, sleep and wake, the cap, the far
   shape, the follow.
2. (a) None.
3. (b)
   - `test_truth_87_the_brig_promoted_sails_near_the_track...` (154): the docstring says
     "within ... a mile over an hour"; the assertion (187) is `<= 1.5`. The two brigs sail
     different latitudes (49 10 N and 49 33 N) and the miles use one cosine (0.65). A band
     looser than the truth it names. Low; sure.
   - Line 273: `"X at full detail" in brief or "at full detail" in brief`: the first term is
     redundant, the test is the second. Lines 277-279 likewise. Line 343 `assert r`. Low.
   - Line 729: `names[0] == falmouth.tracks["to_sea"][0] or len(names) > 3`. Low.
   - Line 854: `len(hers) >= 6`, the comment says six exactly. Low.
   - `MagicMock` harnesses at 952 and 1073 stand for a seated station; the cap's rule is
     what is tested. Acceptable.
4. (c) The demotion loop (`_asleep`, and inline at 75-79, 310-314) runs in five tests.
   Low.
5. `test_a_ship_demoted_sleeps_with_her_damage_and_wakes_the_same_ship` (828) is a strong
   test of a hard thing (state kept across sleep and checkpoint).

## test_damage_control.py (328 lines)

1. 10 tests, no fixtures; worlds sailed 15 minutes then up to seven hours of repair.
2. (a) None.
3. (b) Line 302: `gain == 0.0 or all(lk.kind == "the seams" ...)`. Low. Line 88's band
   1,200 to 1,500 s is stated against the bill's twenty minutes: fair.
4. (c) None. 5. Sound; each repair is driven by its order and checked in the state.

## test_date_and_war.py (125 lines)

1. 3 tests on the dispatches scenario (function-scoped fixture).
2. (a) Line 90 calls `news_heard("the boat from the quay at Falmouth")` directly. In the
   code only the pilot's hook calls `news_heard` (`freesail/world/dealings.py:865`); the
   module docstring speaks of "every change the news brought her". No boat brings news of
   the war. Low; sure.
3. (b) `test_the_pilots_news_enters_what_it_changed_in_the_papers` (111): the docstring
   says "The pilot's hook"; the body (118-121) writes the `port.news` and `paper.written`
   lines itself, with the hook's own code copied, and then asserts those two lines are in
   the log. The real hook (`dealings.py:862-868`) is never run. Delete it and the test
   passes. High for this behaviour; sure (fault 2).
4. (c) None. 5. The other two tests are sound.

## test_determinism.py (37 lines)

1. 3 tests on `World(seed=...)` with the point ship.
2. (a) The game's determinism is now proven on ship files elsewhere (replay tests in nearly
   every file of my list). These three test the milestone 1 stand-in; `test_log_is_not_
   trivially_short` asserts three kinds exist. They could go, or move onto a ship file.
   Low; sure.

## test_director.py (1823 lines)

1. 53 tests (57 cases). No module fixtures; `_forms_worlds` builds three seas lazily inside
   one test. Proves the director's station, the doubt, the brief's limits, the budget, the
   hidden log, the two replay roads, the voice, the hand, the forms and dry run, seats.
2. (a) Line 1053 asserts `w.people.find("the cook") is None` after the loop, so only the
   second world (`briefed`) is checked. Line 1565 an unused import kept by `noqa`. Low.
3. (b)
   - `test_the_aboard_orders_do_what_the_table_knows...` line 351: the check for "a seam
     found working" is `lambda: True`. The effect (`freesail/world/orders.py:3569`,
     `world.water.start_seam`) is not tested here. Medium; sure (fault 6).
   - Line 373 pins `len(WO.aboard_table()) == 34`. Low.
   - Line 418: `w.systems is None or w.systems.find("the gale") is None`. Low.
   - Line 554: `< 20` lines of `person.spoke` in half an hour. A band. Low.
   - `test_every_world_order_form_has_examples_that_parse_and_that_the_game_performs`
     (1505): of 96 examples in 41 forms, 25 are excused by `UNPERFORMED_HERE` (1417-1451)
     with a phrase the refusal must hold, and "it would be doubted" with "it would do this"
     counts as performed (1525-1527). The name says the game performs them. The excuses are
     honest in words but the claim is "verified examples". Low; sure.
4. (c) `seat_director` plus `directed()` is rebuilt in nearly every test; acceptable. The
   two replay-by-both-roads tests (681, 1153) are distinct scenes.
5. `test_how_the_world_behaves_is_written_from_the_code...` (1599) checks the page's
   figures against the code's constants: a good pattern. `A_GLASS` is defined at 1041 after
   its first use at 1033 (module-level, works, reads badly).

## Across the files

- Helpers are imported across test modules (`tests.test_brains`, `tests.test_captive`,
  `tests.test_director`, `tests.test_orders_places`, `tests.test_ground`,
  `tests.test_observer`, bare `test_primer`). A change in one test file's helper moves
  tests in others. A `tests/helpers/` or conftest fixtures would make the dependency plain.
- Wall-clock assertions in the fast tier (test_chart 300, 336, 340) against the project's
  own rule for pace figures.
- Exact digests and line counts are the main pins of the trials; the comment beside the
  lee-shore trial says a digest differs by machine.
- Source-text tests (test_captain 408, 631; test_captains 276; test_consent 500) prove the
  text, not the behaviour.

## Faults to plant

Each to be planted alone in a scratch copy.

1. `test_catalogue.py::test_aloft_flags_are_on_the_steps_aloft`. Fault: in
   `data/evolutions/furl_lateen.yaml` delete line 25 (`    aloft: true`), so the lateen's
   furl on its yard aloft is counted as deck work (the crew factor and the aloft skill
   wrong). The name says the aloft flags are on the steps aloft. Prediction: passes
   although the game is broken (only five files are checked; line 275 compares `aloft`
   with itself for the rest).
2. `test_date_and_war.py::test_the_pilots_news_enters_what_it_changed_in_the_papers`.
   Fault: in `freesail/world/dealings.py` delete lines 863-868 (the `papers = getattr(...)`
   and the `for line in papers.news_heard(...)` loop), so the pilot's news is never entered
   in the papers. Prediction: passes although broken (the test writes the lines itself).
3. `test_canvas.py::test_new_parts_do_not_change_the_ratings_of_the_old_spars`. Fault: in
   `data/ships/frigate-36.yaml` line 233 change `rating_kn: 261.9` to `rating_kn: 26.2` (a
   slipped digit on the main topmast). The name says every old spar keeps its rating.
   Prediction: passes although broken (other files' strain tests may fail; this one will
   not).
4. `test_captain.py::test_the_console_and_the_server_take_the_seat_flag`. Fault: in
   `freesail/ui/console.py` delete lines 1211-1212 (`if seat:` /
   `seat_player(world, seat, door="console")`), so `--seat officer` is parsed and ignored.
   The name says the console takes the seat flag. Prediction: passes although broken.
5. `test_consent.py::test_the_harness_and_the_consent_step_import_no_vendor`. Fault: add
   an import of the vendor SDK (the package of `pyproject.toml:29`) at the top of `freesail/agents/harness.py`. The name says the harness
   imports no vendor. Prediction: passes (only `mcp`, `mcp_types`, `httpx` are banned).
6. `test_director.py::test_the_aboard_orders_do_what_the_table_knows_and_reach_the_play_log
   _as_a_report`. Fault: in `freesail/world/orders.py` line 3569 replace
   `seam = world.water.start_seam(float(value), "a seam started below the wale")` with
   `seam = {"since": world.clock.tick}`, so the seam is reported and makes no water. The
   name says the aboard orders do what the table knows. Prediction: passes (its check is
   `lambda: True`); `test_damage_control.py::test_the_ground_leak...` starts its seam
   directly and will not catch it either.

Faults I believe no test in my files would catch, though a player would:

A. `data/evolutions/back_and_fill.yaml` line 21: `cycles: 2` to `cycles: 0` (back and fill
   ends at once). The one test of the behaviour is a strict xfail and stays an expected
   failure; `test_whole_ship_orders_start_their_evolution` checks only that it starts.
B. `freesail/ui/server.py` lines 1834-1836: drop the `seat_player(world, seat,
   door="browser")` call; `--seat` at the browser does nothing. The flag test reads only
   the source's strings, which remain (`"--seat"` at 1767, `seat.route(` at 612).
C. In `freesail/world/dealings.py` 865, the pilot's news written to the papers under the
   wrong port name (`f"the pilot off {port.id}"`): test_date_and_war never runs the hook,
   and no other file in my list reads `paper.written` from a pilot.

## What I did not do

Ran nothing of the suite; did not measure any fixture's time (the `under_way` tier
question stays a suspicion). Did not read the other test files that the duplicates point
to (test_known_truths, test_staying, test_lying_to, test_brains, test_primer beyond lines
125-170). Did not check whether `load_chart` caches, nor whether any ship file uses the
count-only spare sails form. Did not open the playtest save `test_checkpoint.py:489` reads.
