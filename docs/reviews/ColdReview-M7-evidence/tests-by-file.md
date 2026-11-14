# The test suite by file

One row for each test file: the reader's count of lines and of tests (cases), the weight of
its fixtures and the reader's verdict in a few words (from the heads of `tests-01` to
`tests-12`, where each verdict is argued with its lines), joined to the seconds of the
timed run of the fast tier at the commit under review (`timings/fast-tier-per-test.csv`:
four workers, 78.7 minutes by the clock, 18,743 seconds of work; a file's seconds are the
sum over its cases, setup and teardown included, whichever worker ran them). The slow tier
was not run by the review. `tests/test_known_truths.py` was read in two halves and has two
rows; its seconds are on the first.

| test file | lines | tests (cases) | fast tier: cases run, seconds | the reader's verdict | read in |
|---|---:|---|---:|---|---|
| test_aboard_another.py | 277 | 9 (9) | 9, 122 s | sound in the main; two either-outcome asserts | tests-03.md |
| test_aboard_found.py | 242 | 10 (10) | 10, 26 s | sound; one count pin, one vacuous-able `all` | tests-03.md |
| test_agent_api.py | 995 | 22 (22) | 16, 17 s | sound; pins constants in place of the cap it names; reads client JS | tests-03.md |
| test_agents.py | 3168 | 105 (110) | 95, 74 s | proves much; one strict xfail of a dead rule, one tautology, many pins of constants and doc sizes | tests-03.md |
| test_anchor.py | 707 | 22 (28) | 28, 192 s | sound core; three asserts that cannot fail, one dead block | tests-03.md |
| test_api_door.py | 770 | 18 (19) | 19, 23 s | sound; one repository-hygiene test that is not of the game | tests-03.md |
| test_bellerophon.py | 2198 | 53 (93) | 84, 108 s | pins much from the data file; drafts of truths duplicating its own tests; one test pins a known gap | tests-03.md |
| test_between_hulls.py | 367 | 8 (8) | 8, 189 s | dead in part (test 1 is test 2's prefix) | tests-03.md |
| test_bilander.py | 2119 | 48 (63) | 61, 97 s | pins much; one test touches no code at all; two cases test a flag the game never sets | tests-03.md |
| test_bill_marines_and_flag.py | 174 | 7 (30) | 30, 10 s | sound; module docstring now false | tests-03.md |
| test_boat_director.py | 140 | 5 (5) | 5, 38 s | one branch-either-way test | tests-03.md |
| test_boat_drawing.py | 73 | 3 (7) | 7, 4 s | sound | tests-03.md |
| test_boat_hull.py | 346 | 10 (10) | 10, 192 s | sound | tests-03.md |
| test_boat_names.py | 90 | 2 (2) |  | sound | tests-03.md |
| test_bowsprit_yards.py | 678 | 17 (34) | 34, 22 s | sound | tests-03.md |
| test_brains.py | 416 | 10 (10) | 10, 48 s | one vacuous assert; otherwise sound | tests-03.md |
| test_browser_probe.py | 68 | 2 (13) | 1, 0 s | sound; tests the probe tool and its plans | tests-04.md |
| test_business.py | 547 | 15 | 6, 18 s | sound in the main; one fixture mutated across tests; an `if ...: continue` escape | tests-04.md |
| test_canvas.py | 668 | 27 (36) | 33, 12 s | two tests are one test twice; one test asserts nothing its name says | tests-04.md |
| test_captain.py | 690 | 18 | 18, 120 s | sound behaviour; two source-text tests prove nothing of behaviour | tests-04.md |
| test_captain_rules.py | 309 | 9 | 9, 49 s | sound; unit tests of private methods with `give` faked | tests-04.md |
| test_captain_trials.py | 552 | 8 | 3, 145 s | pins much, proves little; one name says the opposite of its body; one digest dropped | tests-04.md |
| test_captains.py | 624 | 16 | 16, 118 s | sound mostly; a source grep; a tautology | tests-04.md |
| test_captive.py | 629 | 12 | 10, 154 s | sound behaviour; duplicates its own scene; `slow` marked in the file | tests-04.md |
| test_catalogue.py | 1013 | 33 (57) | 47, 17 s | an aloft check that checks five files; a strict xfail of a broken evolution since 37p | tests-04.md |
| test_chart.py | 2421 | 60 (74) | 70, 86 s | tests data and the build tool; wall-clock asserts in the fast tier; block families want a table | tests-04.md |
| test_chart_audit.py | 294 | 14 | 13, 95 s | tests a tool; one test pins a known data fault as expected | tests-04.md |
| test_check_viewer_guns.py | 70 | 4 (21) | 21, 7 s | sound; tests a tool over the data | tests-04.md |
| test_checkpoint.py | 550 | 16 (22) | 12, 95 s | sound; one test depends on a file under docs/playtests | tests-04.md |
| test_complete.py | 164 | 11 | 11, 6 s | sound; runs on the M1 point ship and a fake runner | tests-04.md |
| test_consent.py | 519 | 22 (31) | 31, 2 s | sound; the vendor-free test's list is stale | tests-04.md |
| test_console.py | 83 | 6 | 6, 19 s | sound; on the point ship | tests-04.md |
| test_context_budget.py | 158 | 6 | 6, 1 s | tests a tool and a document | tests-04.md |
| test_core.py | 71 | 5 | 5, 0 s | sound | tests-04.md |
| test_court.py | 510 | 7 | 3, 17 s | one 170-line story test; `slow` marked in the file | tests-04.md |
| test_crew_model.py | 502 | 27 (28) | 28, 4 s | sound; one golden muster text | tests-04.md |
| test_crew_orders.py | 392 | 21 (32) | 30, 19 s | sound; one assertion reads the fake runner's own effect | tests-04.md |
| test_crews.py | 1079 | 24 | 20, 340 s | sound behaviour; or-escapes; a band looser than its docstring | tests-04.md |
| test_damage_control.py | 328 | 10 | 10, 122 s | sound | tests-04.md |
| test_date_and_war.py | 125 | 3 | 3, 268 s | one test performs the hook itself and asserts what it wrote | tests-04.md |
| test_determinism.py | 37 | 3 | 3, 2 s | runs the point ship only; little left of the game in it | tests-04.md |
| test_director.py | 1823 | 53 (57) | 55, 310 s | sound in the main; a vacuous check; 25 excused examples | tests-04.md |
| test_door_follows.py | 126 | 3 (3) |  | sound; same scene built three times; duplicates truths 7-390/391 | tests-05.md |
| test_driver.py | 1734 | 41 (80) | 80, 98 s | proves hard things; pins much (phase seconds, golden refusals); one test enforces a known untruth | tests-05.md |
| test_dumb_show.py | 506 | 10 (17) | 17, 13 s | sound in part; two tests compare the code with a pasted copy of itself | tests-05.md |
| test_evolutions.py | 1937 | 64 (93) | 90, 23 s | mostly sound; time bands prove the stub, not the ship; one golden line pins a wrong heading | tests-05.md |
| test_facade_readers.py | 262 | 5 (5) | 5, 14 s | sound | tests-05.md |
| test_far_action.py | 368 | 8 (8) | 4, 15 s | marks `slow` by hand against conftest's rule; one assertion can never fail | tests-05.md |
| test_far_hail.py | 142 | 3 (3) | 1, 5 s | test 1 is a subset of test 3; "far or full" tests far only | tests-05.md |
| test_fight.py | 505 | 12 (12) | 12, 41 s | mostly sound; escape-hatch `or`s; a vacuous `all()` | tests-05.md |
| test_filling.py | 501 | 12 (12) | 12, 32 s | sound; arithmetic checked exactly | tests-05.md |
| test_fishing.py | 323 | 15 (15) | 13, 20 s | dead in part: a loop over a possibly empty list; name promises "salt keeps", body does not test it | tests-05.md |
| test_flag_drawings.py | 694 | 22 (27) | 27, 173 s | pins much (golden file of every flag); a harbour test elsewhere | tests-05.md |
| test_flags.py | 321 | 10 (15) | 11, 6 s | sound; one docstring says three minutes, the body asserts five | tests-05.md |
| test_found_on_the_way_85.py | 124 | 4 (4) | 4, 23 s | sound | tests-05.md |
| test_gale.py | 611 | 27 (30) | 30, 63 s | one test cannot fail; one takes the module fixture and never uses it | tests-05.md |
| test_geo.py | 298 | 13 (13) | 13, 14 s | sound; region list pinned | tests-05.md |
| test_grammar_book.py | 186 | 9 (9) | 9, 14 s | tests documents; one test checks one word anywhere in the primer | tests-05.md |
| test_ground.py | 411 | 10 (10) | 10, 255 s | sound but for one assertion that can never fail | tests-05.md |
| test_hands.py | 1060 | 32 (58) | 49, 48 s | the compatibility test is strong; stale module docstring; dead code in a fake | tests-05.md |
| test_harbour.py | 702 | 16 (16) | 13, 29 s | tests the launcher; the browser test skips on every CI job | tests-05.md |
| test_harness_instruments.py | 205 | 8 (8) | 8, 93 s | one `or` swallows its own assertion | tests-05.md |
| test_health.py | 373 | 12 (12) | 12, 718 s | one assertion can never fail; one `or` lets the wrong man take command | tests-05.md |
| test_held_hulls.py | 120 | 3 (3) | 1, 6 s | sound; one test likely slow and unmarked | tests-06.md |
| test_hull.py | 461 | 27 (32) | 32, 10 s | sound; one name promises a check the body does not make | tests-06.md |
| test_hull_brig.py | 595 | 22 (50) | 50, 9 s | proves the file, the note and the generator agree; little of the game; its git test always skips | tests-06.md |
| test_hull_cutter.py | 472 | 18 (28) | 28, 0 s | the same, with a 15% band where 0.5% is the fact | tests-06.md |
| test_hull_form.py | 1427 | 28 (101) | 101, 7 s | sound, the best file of the list; a few pins of recorded errors | tests-06.md |
| test_hull_frigate.py | 639 | 19 (19) | 19, 1 s | as brig; pins much | tests-06.md |
| test_hull_lugger.py | 614 | 25 (33) | 33, 0 s | as brig; one test asserts only a design note's wording; one holds of nothing | tests-06.md |
| test_hull_schooner.py | 536 | 17 (27) | 27, 1 s | as brig; reads Build-Ships.md | tests-06.md |
| test_hull_smack.py | 626 | 20 (20) | 20, 1 s | as brig; three tests for "she has no port" | tests-06.md |
| test_hulls.py | 407 | 11 (11) | 11, 32 s | sound; the old-shape writer is a forge to keep in step | tests-06.md |
| test_in_world.py | 296 | 9 (95) | 95, 9 s | sound; tests served documents, by design | tests-06.md |
| test_indefatigable.py | 2959 | 53 (68) | 68, 320 s | proves much, but none of its ~12 sailed tests is in the slow tier; truths re-assert the particulars | tests-06.md |
| test_islands.py | 292 | 9 (10) | 10, 7 s | sound in the main; tests tools and data more than play | tests-06.md |
| test_knowledge.py | 2104 | 44 (44) | 25, 110 s | proves much that is hard; several conditional or mis-described assertions; one test of a feature switched off; every slow test run twice (truths re-call them) | tests-07.md |
| test_known_truths.py (lines 1 to 8700) | 1-8700 | 159 functions (162 cases: 3 parametrised x2); 8 strict xfail; 6 pace | 244, 4358 s | Proves much through the game, but pins much more than it proves at the scenario level (75 tick constants, 8 digests, 8 line counts, 871 comment lines of re-pin history); a dozen weak or tautological asserts; heavy duplication with other files | tests-01-known-truths-a.md |
| test_known_truths.py (lines 8700 to end) | 8,692 | 287 functions (292 cases: one parametrised into 6) | (with the first half) | duplicates other files wholesale (102 bodies are calls of other files' tests); about half the rest pin data, text and tool output; the remainder prove real behaviour and some prove it well | tests-02-known-truths-b.md |
| test_lateen.py | 722 | 23 (40) | 40, 25 s | sound; one family asserts the evolution id and nothing after | tests-07.md |
| test_lee_ports.py | 1938 | 60 (179) | 179, 54 s | sound and hard; pins a typed copy of the tuning notes' tables; truth 7-190 "drafts" never moved; one dead test | tests-07.md |
| test_letters.py | 510 | 14 (18) | 18, 77 s | sound; two digest pins on a kept save | tests-07.md |
| test_local_runner.py | 1407 | 30 (30) | 29, 19 s | sound in substance; pins constants; timing-dependent threads | tests-07.md |
| test_log_lines.py | 635 | 21 (21) | 20, 39 s | sound; one test can only fail one way | tests-07.md |
| test_longitude.py | 712 | 14 (14) | 10, 56 s | contains `assert x or True`; one test asserts only that nothing raised; a stale docstring | tests-07.md |
| test_lookout.py | 458 | 13 (13) | 13, 44 s | sound; two vacuous trailing asserts; overlaps test_longitude | tests-07.md |
| test_lug.py | 131 | 5 (5) | 5, 7 s | contains an assertion that cannot fail; three tests re-settle the same lugger | tests-07.md |
| test_lying_to.py | 950 | 26 (40) | 34, 126 s | strong physics tests; the same hove-to brig built a dozen times | tests-07.md |
| test_magazine.py | 609 | 16 (54) | 54, 9 s | sound; reference table typed from the source, not from the code | tests-07.md |
| test_map_view.py | 313 | 9 (9) | 9, 1 s | sound; one test not guarded by `needs_node`; a doubled decorator | tests-07.md |
| test_mcp_server.py | 1346 | 35 (35) | 29, 83 s | substantial; real-time races; pins `.mcp.json`'s `py`, which does not exist on this machine | tests-07.md |
| test_mends_109.py | 427 | 15 (39) | 39, 393 s | one parametrised test ignores its own parameter and can pass on any refusal | tests-07.md |
| test_moon.py | 104 | 5 (5) | 5, 0 s | sound: checked against Meeus and JPL Horizons | tests-07.md |
| test_nations.py | 371 | 8 (8) | 8, 2 s | pins the whole port index (140 rows) by hand; one test name stale | tests-07.md |
| test_neufchatel.py | 1,759 | 51 (61) | 60, 68 s | a data file's audit in the main; helm bands drawn round the code; truth 7-192 repeats the file | tests-08.md |
| test_observer.py | 316 | 10 (17) | 16, 130 s | sound in the main; the day proves little; four tests run twice through test_known_truths | tests-08.md |
| test_officer.py | 3,917 | 64 (74) | 74, 291 s | proves much, pins much; a third is the consent brief; the handover test moved to fit the brief | tests-08.md |
| test_orders.py | 2,877 | 85 (726; `TABLE` alone 470) | 726, 200 s | sound grammar table; proves parsing, not the evolutions; some rows check only the kind | tests-08.md |
| test_orders_m4a.py | 351 | 10 (35) | 33, 15 s | sound in part; an `or` empties one table check; two dead slow ids in conftest | tests-08.md |
| test_orders_places.py | 482 | 17 (18) | 16, 37 s | sound; a few `!=` and negative checks | tests-08.md |
| test_ordnance.py | 966 | 24 (24) | 24, 22 s | 17 of 24 stand on a fake magazine the real one has replaced; refusals well pinned | tests-08.md |
| test_parity.py | 390 | 6 (6) | 5, 19 s | truth 91 a good test; the enumerations prove a reason is written, not that a road works | tests-08.md |
| test_people.py | 971 | 27 (27) | 27, 167 s | sound; leans on helpers imported from four other test files | tests-08.md |
| test_pictures.py | 416 | 2 (2) | 2, 18 s | sound in intent; threshold lowered to pass; skips silently off the build machine | tests-09.md |
| test_pivot_gun.py | 217 | 9 (9) | 9, 1 s | sound; drives the trainer by hand, never through the battery's tick | tests-09.md |
| test_places.py | 292 | 6 (6) | 6, 24 s | sound; stale comments; some lines compared to the code's own output | tests-09.md |
| test_ports.py | 2401 | 53 (57) | 50, 479 s | proves much; one vacuous `all()`; census pins; the pilot's passage sailed again and again | tests-09.md |
| test_powder_orders.py | 504 | 10 (10) | 10, 8 s | words well proved; the quantities proved against a stale fake magazine | tests-09.md |
| test_practice.py | 627 | 21 (25) | 25, 34 s | fakes stand in for a battery and a fit that now exist; one test of documents | tests-09.md |
| test_practice_lookout.py | 209 | 7 (7) | 7, 13 s | sound | tests-09.md |
| test_practice_orders.py | 908 | 29 (49) | 49, 93 s | sound in the main; one test of a monkeypatched `begin_exercise`; duplicates test_practice | tests-09.md |
| test_primer.py | 603 | 11 (1095) | 1095, 2575 s | tests a document; two chapters' blocks never run; a swallowing `except` | tests-09.md |
| test_prize_court.py | 400 | 8 (8) | 7, 42 s | sound; one `@pytest.mark.slow` against conftest's rule | tests-09.md |
| test_prize_scenarios.py | 227 | 5 (5) | 3, 42 s | one `assert x or True`; two slow marks by hand | tests-09.md |
| test_prizes.py | 470 | 8 (8) | 5, 24 s | sound; stale band in the rising; seed-picked outcomes | tests-09.md |
| test_profile.py | 965 | 36 (103) | 103, 12 s | tests the generator and stage-0 hooks; source-grep pin; duplicates test_profiles | tests-09.md |
| test_profiles.py | 1099 | 24 (44) | 44, 18 s | tests the generator and the drawn hulls; runs the whole generator a second time; reports where it should bound | tests-09.md |
| test_python_api.py | 405 | 10 (10) | 5, 4 s | sound twins; one dead assertion | tests-09.md |
| test_readings.py | 797 | 23 (26) | 19, 36 s | sound; some tautology by design | tests-09.md |
| test_reckoning.py | 2765 | 74 (74) | 65, 476 s | strong numerically; a dead branch, a one-case parametrise, one vacuous membership | tests-09.md |
| test_regatta.py | 444 | 12 (12) | 8, 21 s | sound; one band built not to fail (441) | tests-10.md |
| test_replay.py | 1101 | 22 (22) | 20, 204 s | sound and hard; a few pins (`BUILD_NAME == "m6c"`), one timing band | tests-10.md |
| test_rig_classing.py | 895 | 25 (71) | 71, 11 s | golden table pins by design; much of it tests the test fixtures' geometry, not the game | tests-10.md |
| test_rig_geometry.py | 765 | 33 (51) | 48, 16 s | sound in the main; one parametrised test ignores its parameter and proves only a default argument | tests-10.md |
| test_rollup.py | 486 | 19 (20) | 16, 11 s | sound; one stale node id in conftest moves a long test into the fast tier | tests-10.md |
| test_routine.py | 560 | 24 (24) | 18, 13 s | sound; one band built on a local copy of a code constant that leaves out part of the code's formula | tests-10.md |
| test_sail_by_name.py | 459 | 14 (14) | 13, 48 s | one assertion built not to fail (164); two loose "either" asserts | tests-10.md |
| test_sails.py | 480 | 23 (24) | 24, 3 s | sound force-level physics; one 25-fold band; one docstring that promises more than the body checks | tests-10.md |
| test_scenario_nations.py | 235 | 4 (19) | 19, 8 s | tests a parsed block that no code reads | tests-10.md |
| test_scenarios.py | 532 | 16 (16) | 16, 24 s | seven near-copies that want a table; one misplaced block of asserts | tests-10.md |
| test_schooner_mast.py | 853 | 25 (74) | 74, 17 s | sound; pins the count of ship files; two long sailed tests in the fast tier | tests-10.md |
| test_sea.py | 730 | 23 (27) | 20, 6 s | one tautology (636); one test of hooks that nothing reads, two milestones after "5b" | tests-10.md |
| test_seat_hook.py | 175 | 3 (3) | 3, 24 s | sound; one long chain of refusals wants a table | tests-10.md |
| test_server.py | 831 | 31 (61) | 59, 52 s | sound routes; one test reads the source text of `main`; ship-independent tests doubled | tests-10.md |
| test_service.py | 159 | 6 (6) | 6, 32 s | sound | tests-10.md |
| test_settee.py | 1566 | 37 (78) | 78, 103 s | sound and hard; slow and repetitive; a stale docstring; two whole-trace pins; one monkeypatch that swaps like for like | tests-10.md |
| test_settings.py | 214 | 9 (14) | 14, 0 s | tests the tooling, not the game; sound | tests-10.md |
| test_ship_loader.py | 448 | 18 (48) | 48, 2 s | sound; holds a repository line-ending check that does not belong to the loader | tests-10.md |
| test_ship_particulars.py | 604 | 19 (24) | 24, 4 s | data range checks; sound; stale docstring | tests-10.md |
| test_ships.py | 889 | 29 (32) | 32, 230 s | asserts a stale docstring (251); one comparison of an object with itself (93); reads `client/map.js` text | tests-10.md |
| test_ships_hierarchy.py | 235 | 10 (10) |  | sound bands; sails sweeps again that test_known_truths sails under the same names | tests-10.md |
| test_sights.py | 182 | 7 (7) | 6, 7 s | one dead assertion (181 to 182); a comment and its band disagree | tests-10.md |
| test_signals.py | 754 | 20 (32) | 28, 32 s | sound; strong data guard through `tools/check_signals.py` | tests-10.md |
| test_squadrons.py | 829 | 21 (21) | 21, 307 s | one tautology (530); one `A or B` assertion; one test step whose plant can never run | tests-10.md |
| test_stand_by_words_and_action_flow.py | 157 | 5 (5) | 5, 10 s | three unrelated subjects under one name; one loop that does not require its other branch | tests-10.md |
| test_standing.py | 2211 | 50 (249) | 243, 113 s | sound in the main; one guarded assertion, one test of the test, stale "held" words | tests-11.md |
| test_staying.py | 484 | 17 (20) | 8, 14 s | sound physics; wide bands; shared mutable fixture; duplicates truths 10/16 | tests-11.md |
| test_stores.py | 184 | 9 (9) | 9, 24 s | sound | tests-11.md |
| test_strain.py | 733 | 31 (36) | 32, 6 s | sound unit layer; World tests duplicate truth 9 | tests-11.md |
| test_studding.py | 537 | 22 (37) | 28, 10 s | sound for the frigate; schooner half parked as strict xfail | tests-11.md |
| test_subtypes.py | 1211 | 33 (85) | 82, 99 s | pins much (exact ticks, data tables); truth 7-191 "draft" never moved | tests-11.md |
| test_sun.py | 229 | 13 (13) | 10, 6 s | sound; almanac-checked | tests-11.md |
| test_tackle_orders.py | 754 | 27 (43) | 42, 184 s | sound; good fixture practice | tests-11.md |
| test_tell.py | 390 | 15 (16) | 13, 9 s | sound | tests-11.md |
| test_the_ship_herself.py | 165 | 5 (14) | 14, 56 s | one test asserts what it passed in | tests-11.md |
| test_tide.py | 1369 | 32 (32) | 32, 88 s | truths 62-64 sound; two thirds is a data audit pinning id lists | tests-11.md |
| test_tow.py | 209 | 5 (5) | 5, 44 s | sound; one name promises "half a knot", body asserts about a knot | tests-11.md |
| test_trim_order.py | 331 | 14 (16) | 13, 8 s | sound; half on a fake runner | tests-11.md |
| test_units.py | 123 | 12 (29) | 29, 0 s | sound | tests-11.md |
| test_via.py | 246 | 6 (6) | 5, 7 s | sound; one `or`-shaped assertion | tests-11.md |
| test_view_action.py | 570 | 17 (93) | 93, 60 s | sound; run twice over by truths 7-450..454 | tests-11.md |
| test_view_geometry.py | 7,056 | 139 (1,045): 108 parametrised into 1,014 cases, 31 single | 1045, 782 s | proves a great deal of real geometry, but out of proportion: about 175 numbers pinned to what the code gave, a block of tests that demand recorded defects persist, roughly 120 cases on branches no served graph reaches, and five copy-pasted "frame holds" tests | tests-12-view-geometry.md |
| test_viewer_action.py | 278 | 13 (49) | 49, 20 s | sound | tests-11.md |
| test_visitor_name.py | 94 | 3 (3) | 2, 7 s | sound | tests-11.md |
| test_wardroom.py | 147 | 4 (4) | 4, 22 s | covers 4 of 12 wardroom files | tests-11.md |
| test_wardroom_doors.py | 879 | 22 (22) | 22, 207 s | sound; one test reads source text; a dead `assert allowed` | tests-11.md |
| test_water.py | 317 | 11 (11) | 11, 44 s | sound; pumps checked on 7 of 18 ship files | tests-11.md |
| test_weather.py | 1002 | 31 (35) | 31, 19 s | arithmetic sound; climatology tests parse prose notes; two stale names | tests-11.md |
| test_weather_script.py | 403 | 21 (29) | 25, 4 s | sound | tests-11.md |
| test_wind.py | 157 | 6 (10) | 10, 1 s | sound; long statistical runs | tests-11.md |
| test_world.py | 82 | 9 (9) | 9, 2 s | milestone-1 point ship; one band wide enough for anything | tests-11.md |
| test_world_orders.py | 1070 | 28 (28) | 28, 179 s | sound; long sails inside fast-tier tests | tests-11.md |

Sum of the seconds over all files (the work of all workers, not the wall clock): fast tier 18743 s.

Test files with no row from a reader: none
