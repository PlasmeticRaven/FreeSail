# Tests, reader 05: test_door_follows.py to test_health.py

Reader 05 of the test-suite audit. Every file below was read whole, from its first line to its
last, after `tests/conftest.py`. Where I judged a test I also read the code it calls (named
where used). I ran nothing but `grep`, `wc`, `ls` and a `sed` of `pyproject.toml`: no test, no
world, no Python. So every "would pass" or "would fail" below is a reading, not a run.

## The table

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_door_follows.py | 126 | 3 (3) | none; each test builds the same two-hull scene again (`_two_captains_one_moved`), all three slow | sound; same scene built three times; duplicates truths 7-390/391 |
| test_driver.py | 1734 | 41 (80) | none module-scoped; `_world` and `_fair_wind_world` sail 1,200 ticks per call (about 20 calls) | proves hard things; pins much (phase seconds, golden refusals); one test enforces a known untruth |
| test_dumb_show.py | 506 | 10 (17) | none | sound in part; two tests compare the code with a pasted copy of itself |
| test_evolutions.py | 1937 | 64 (93) | none (stub physics) | mostly sound; time bands prove the stub, not the ship; one golden line pins a wrong heading |
| test_facade_readers.py | 262 | 5 (5) | `two_hulls` (module: a frigate and a promoted brig) | sound |
| test_far_action.py | 368 | 8 (8) | none; four tests sail 1 to 4 hours of far world each | marks `slow` by hand against conftest's rule; one assertion can never fail |
| test_far_hail.py | 142 | 3 (3) | none; `hail_and_answer` sailed twice | test 1 is a subset of test 3; "far or full" tests far only |
| test_fight.py | 505 | 12 (12) | none | mostly sound; escape-hatch `or`s; a vacuous `all()` |
| test_filling.py | 501 | 12 (12) | none | sound; arithmetic checked exactly |
| test_fishing.py | 323 | 15 (15) | none | dead in part: a loop over a possibly empty list; name promises "salt keeps", body does not test it |
| test_flag_drawings.py | 694 | 22 (27) | none; a JSON golden fixture; three tests need Node | pins much (golden file of every flag); a harbour test elsewhere |
| test_flags.py | 321 | 10 (15) | none | sound; one docstring says three minutes, the body asserts five |
| test_found_on_the_way_85.py | 124 | 4 (4) | none | sound |
| test_gale.py | 611 | 27 (30) | `frigate_by_the_wind` (module: 1,300 ticks) | one test cannot fail; one takes the module fixture and never uses it |
| test_geo.py | 298 | 13 (13) | none | sound; region list pinned |
| test_grammar_book.py | 186 | 9 (9) | `grammar` (a world made), `primer` | tests documents; one test checks one word anywhere in the primer |
| test_ground.py | 411 | 10 (10) | `standing_on_by_account` (module: up to 5 h sailed) | sound but for one assertion that can never fail |
| test_hands.py | 1060 | 32 (58) | none; the compatibility rule sails 40 worlds | the compatibility test is strong; stale module docstring; dead code in a fake |
| test_harbour.py | 702 | 16 (16) | none; a live uvicorn server; a browser | tests the launcher; the browser test skips on every CI job |
| test_harness_instruments.py | 205 | 8 (8) | none | one `or` swallows its own assertion |
| test_health.py | 373 | 12 (12) | none | one assertion can never fail; one `or` lets the wrong man take command |

Totals: 329 test functions, about 450 cases.

## What matters most, in short

1. **Assertions that cannot fail.** `kind != "order.refused"` in
   `test_ground.py:139` and `test_health.py:247`: no code in `freesail/` emits `order.refused`
   (grep: the string occurs only in these two lines); a refusal is `order.rejected`.
   `packet.damage["rounds_fired"] >= 0` in `test_far_action.py:361` (a count). `len(kept) <= 1`
   in `test_gale.py:334`, in a test named "the helm keeps her away and says so once".
2. **A golden line pinning a player-visible error.** `test_evolutions.py:890` pins
   "Tacked; braced up on the starboard tack, heading SSE (158°)." for a frigate the test itself
   holds at her old heading, 035° (`close_hauled_on_starboard`, wind from 090, 55° off;
   line 881 sets `s.dyn.heading = old_heading`). `TackScript.words()`
   (`freesail/evolutions/scripts.py:1829-1838`) reads the tack from the ship on a timeout but
   still formats `self.new_course`, the course she was put about for. The log tells the player
   she heads SSE while she heads NE. The test's docstring presents the line as correct.
3. **Comparisons with a copy of the code.** `test_dumb_show.py:359-379` `_old_hit_chance` is a
   line-for-line copy of `freesail/combat/shot.py:152-171`, compared over 840 cases (line 398);
   `_old_minute_line` (237-283) the same for `Battery.minute_line`. They detect any change and
   prove nothing about the gunnery. `test_flag_drawings.py:87-105` compare every flag drawing
   with a JSON recorded from the code.
4. **Tests whose escape hatches let the fault through**: `test_health.py:372`,
   `test_fight.py:183`, `test_fight.py:452-453`, `test_harness_instruments.py:187-189`,
   `test_fishing.py:288-289` (a loop over a list never asserted non-empty).
5. **Skips nobody sees.** `test_harbour.py:504` (the harbour in the browser) skips wherever
   Chromium is not at `PLAYWRIGHT_BROWSERS_PATH`. `.github/workflows/whole-suite.yml:77-81`
   says the runners have no browser and that only `tests/test_browser_probe.py` is run with
   one (line 100). So this test runs only on the build machine.

---

## test_door_follows.py (126 lines)

**Count and kind.** 3 tests, none parametrised, no module fixture. Each calls
`_two_captains_one_moved` (lines 52-67): `_brig_alongside()` from `test_between_hulls`, a desk
with two API doors, the brig's captain sent aboard the frigate in his boat (up to 1.5 h run).
All three are in `SLOW_TESTS` (conftest 505-507). They prove that a seat follows its harness's
`ident` across a move, a save and replay by both roads, and a stand-down.

**(a)** None found. `visitor_name`, `home_harness`, `Desk._seat` exist as called.

**(b)**
- Line 95-98: the save's idents are put into a `set` before comparison, so a harness saved
  twice (a duplicate agent block) passes. Low, likely.
- Line 77 asserts `model_name == WEIGHTS`, which the test passed in at line 59; it shows the
  seat found is the right one only together with line 76. Low.

**(c)** The scene is built three times for three assertions groups; it is mutated by test 3
(the stand-down), so a module fixture would want tests 1 and 2 first. Truths 7-390 and 7-391
in `test_known_truths.py` (conftest 508-509) sail the same scene again: five builds of one
scene in the slow tier.

**Else.** Test 2 (replay by both roads with the visitor's identity) proves something hard.

## test_driver.py (1734 lines)

**Count and kind.** 41 tests; 13 parametrised into 52 cases (the one-place rule over all 18
ship files, line 298; the belay table of 12, line 785; others 2 each), 80 cases in all. No
module fixture: `_world` (1203-1230) and `_fair_wind_world` (1589-1609) each sail 1,200 ticks
under physics, and about 20 calls are made (8 cases of the four manoeuvre tests, 4 of the
toggle under way, 2 checkpoint tests, the toggle shift's two, the truth's one). None of the file
is in `SLOW_TESTS` or `DAY_FIXTURES`; I did not time it. It proves the 64's driver on a
fixture frigate: the shift and its phases, the one-place rule, the boom rigged out only with
the driver, belays and wrecks, the toggle key's inertness, and truth 7-230.

**(a)**
- `test_nothing_in_the_physics_or_the_gunnery_reads_the_boom_rigged_in` (909-919) greps the
  source of `freesail/physics` and `freesail/combat` for the text `rigged_out` and asserts none.
  Its docstring calls the stowed boom's windage "a small untruth, accepted". The test makes
  the known defect permanent: whoever mends it (reads `rigged_out` in the physics) fails it. It
  also tests the source text, not behaviour. Medium, sure.
- The constants `SHIFT_S`, `SHIFT_OUT_S`, `SHIFT_BACK_S` (98-114) are the data file's times
  copied by hand (`data/evolutions/shift_sail.yaml`, all marked judgement in the comment);
  tests 192, 414, 465, 494, 686 assert the runner's phase seconds equal them. A retune of the
  file fails nine tests, none of which says the shift is wrong. Low, sure.

**(b)**
- Golden pins: I count 27 exact refusal or log strings (for example 251-254, 272-279, 571-591,
  665-673, 1428-1430, 1441-1443, 1464-1472) and 5 exact polar figures (1483, 1563). The refusal
  strings are the player's words and their pin is useful; the polar row
  (`test_the_frigates_polar_row_is_the_spankers_row_of_ext_3_2`, 1559) is computed by
  `polar_of` (`freesail/world/ships.py:571`) and pinned to two places, with no reason a reader
  can check other than "the design's §3.2". Low.
- `test_truth_7_230` line 1733: the driver's sheet within 5 degrees of the wanted angle, and
  1734 between the gaff's floor and ceiling (18 to 85 degrees); the docstring measured 59.6.
  The 5-degree band is fair; the floor-to-ceiling band admits any trim. Low.
- `test_the_toggle_on_the_shift_under_way_moves_its_time_by_the_booms_phase` (1656):
  `120 <= took["rig_out_boom"] <= 150` and every other phase within 2 s of the keyless world:
  a real comparison. Sound.

**(c)**
- Row 3' (the spanker re-filed as a lateen) is asserted twice in the same terms:
  `test_the_driver_filed_as_the_spanker_is_the_spanker_to_the_physics` (1566-1581) and
  `test_truth_7_230` (1706-1709). The truth repeats the shift under way of `_shifted_under_way`
  that test 1643 also sails. One of each pair could go.
- `test_the_mizen_is_shifted_for_the_driver_and_back_each_to_its_end` (192),
  `test_bend_the_driver_and_unbend_it_take_the_boom_and_the_course_leaves_it` (465) and
  `test_the_boom_goes_out_before_the_bend_and_comes_in_after_the_unbend` (414) each prove the
  same phase lists from different ends.

**Else.** The toggle proof (`test_the_toggle_on_the_bare_ship_moves_the_booms_state...`,
1087-1109) compares every part's whole state with the key present and absent across 20 orders:
a strong test of inertness. The docstrings carry long design history ("Old beside new",
"Measured without the line ... ") that a builder cannot check from the test.

## test_dumb_show.py (506 lines)

**Count and kind.** 10 tests; one parametrised into 8 cases (305); 17 cases. No fixture;
each world test runs the cutter 5 to 15 minutes. It proves dumb-show exercise (no powder, no
stream, drill counted), the side dropped, a loaded gun exercised, the minute's words, the hit
chance's size term and a shot at a mark.

**(a)**
- `test_a_fall_at_the_cask_within_half_a_cable_is_at_a_cable` (478-506): the docstring says the
  fall is "at a cable" in the struck line and in the drill alike; the body checks only the
  drill's keys (505-506). The struck line is not read. Low, sure.

**(b)**
- `_old_hit_chance` (359-379) is the current `shot.hit_chance` (`freesail/combat/shot.py:152-171`)
  copied, and `test_the_hit_chance_with_no_size_is_todays_and_a_size_replaces_the_hulls`
  (382-406) compares the two over 840 cases. It catches any edit, wanted or not, and the
  builder who retunes the gunnery must edit the copy too. It proves nothing about hits.
  Likewise `_old_minute_line` (237-283) against `Battery.minute_line` (305-312). Medium, sure.
- `test_a_shot_at_a_mark_is_practice_and_never_firing_on_a_sail` (438-475): `resolve` is a
  fake returning `[]` (449-451); line 466 `if struck:` makes the "on the mark" check
  conditional; line 465 `set(resolved) <= {...}` holds for an empty list. If no shot struck in
  six minutes, half the test is skipped silently. Low, likely.
- `test_the_drill_keeps_its_best_and_its_mean` (219-231): `best_s <= total_s / cycles` is true
  of any minimum and also of `best_s` set to the mean; it would pass if "best" were never
  computed apart. Low, sure.
- `test_dumb_show_serves_the_guns_at_the_actions_pace...` (216): band 30 to 300 s per cycle;
  the real assertion is `live == dumb` (214). Sound.

**(c)** `_world`, beat to quarters, cast loose is repeated in 7 tests; fine as setup.

## test_evolutions.py (1937 lines)

**Count and kind.** 64 tests; 13 parametrised (42 cases); 93 cases. No module fixture; most
run the runner on stub physics (`still`, `turner`, `staller`, `hangs_in_stays`, 63-117). Three
(`_frigate_under_plain_sail`, 1602) sail 1,200 ticks under physics and are in `SLOW_TESTS`.
It proves the registry, the expression language, preconditions, serialisation, tack/wear/heave
to on stubs, the haul words, wrecks and spare spars, reeving and splicing, tacks for a course.

**(a)**
- The `run` helper (120-129) stops at `max_ticks` without asserting the work finished (unlike
  `test_driver._run`, which does). A hung evolution returns 3000 ticks quietly; most tests then
  catch it by state, but `test_same_orders_give_the_same_log` (1263-1276) would compare two
  identical hangs and pass. Low, likely.

**(b)**
- Time bands that measure the stub: `test_tack_succeeds_when_the_ship_turns` (746) "a frigate
  should take five to ten minutes", 240 to 600 ticks, with the turn rate fixed at 0.4 deg/s by
  `turner(0.4)`; `test_wear_comes_round_the_other_way` (1059) 360 to 720; the bilander (986).
  The comment at 745 admits "The stub's turn rate sets the time". These bands prove the stub,
  not the ship; the names say "succeeds", which is fair, but the band reads as truth 10/11.
  Low, sure.
- `test_a_tack_ended_by_the_steady_timeout_names_the_tack_she_lies_on` (851-892) pins at 890
  the line "Tacked; braced up on the starboard tack, heading SSE (158°)." while the stub holds
  her at `old_heading` (881), 035°. `scripts.py:1829-1838`: on a timeout `new_tack` is read from
  the ship and `new_course` is still the course ordered. The test pins a log line that
  contradicts the ship. Also the same string's heading appears in
  `test_a_tack_and_a_wear_by_their_own_word_end_as_they_always_have` (1931) for the larboard
  tack, where it is right. High (the player is told a wrong heading), sure.
- `test_wear_gives_up_when_she_will_not_pay_off` (1080) `ticks == 901`: the file's timeout plus
  one, pinned. Low.
- `test_the_bilanders_settee_is_no_course_hauled_at_the_word` (912-945): four cases, every
  `said` the same string; a table whose expected column is constant. Low.
- `test_the_booms_hold_each_ship_files_spare_spars_by_class` (1336-1340) asserts the text of a
  YAML comment in the data files ("Luce 1866 ch. XVII", "'Stowing Booms'"): it tests a document.
  Low.

**(c)** `close_hauled_on_starboard` plus "brace every yard to its limit" is written out 8
times (726-729, 838-840, 868-870, 969-971, 995-997, 1045-1048) before `_braced_up_on_starboard`
(1824) was written for it; the earlier tests could use the helper. The haul word cases
(790, 821, 896, 922) want one table.

**Else.** `test_expressions_refuse_unsafe_things` (261-277) and
`test_registry_rejects_bad_files` (169-192) are good guards.

## test_facade_readers.py (262 lines)

**Count and kind.** 5 tests; `two_hulls` module fixture (the frigate and the brig X promoted;
`test_crews._frigate_and_the_brig_x_on_the_sea`), used by three. Proves truths 7-422 to 7-425
and a guard walking every hull's object graph for a stray World reference.

**(a)** None.

**(b)**
- `test_truth_7_424` (129-158) monkeypatches `World.submit` by assignment (150-154), restored in
  `finally`; fine, but it patches the class for every thread of the process. Low.
- The guard (`world_handles`, 191-236) skips a list of shared objects (194-212) and allows two
  kept references (188). A new system that holds the World through one of the skipped objects
  passes; that is by design and said. Low, suspicion.

**(c)** None.

**Else.** The guard is a good structural test. The truth tests depend on test order only
through the module fixture's `follow` state; 7-423 builds its own world because it follows the
brig, which is right.

## test_far_action.py (368 lines)

**Count and kind.** 8 tests, no parametrisation, no fixture. Four are marked
`@pytest.mark.slow` in the file (92, 223, 280, 313), each sailing up to two or four hours of
far world. It proves the far fight by rounds, the toggle, the chase leg, near and far agreement,
the far record carried into a hull and back, the far reply under the cap, the packet taken.

**(a)**
- The name of `test_the_near_fight_of_two_cutters_at_a_cable_and_the_far_rounds_agree_within_a_round`
  (176) promises one round; its docstring and body say two (182, 217). Low, sure.
- The conftest's own rule (conftest 6-7: "The `slow` mark is applied here and never in a test
  file") is broken by the four hand marks. Low, sure.

**(b)**
- `test_a_packet_that_fights_is_brought_to_by_the_privateers_rounds_and_taken` line 361:
  `packet.damage["rounds_fired"] >= 0`. A count is never negative; the docstring's "fires her
  guns within her four cables" is not tested. Line 360 checks rounds of the pair, not shots by
  the packet. Medium, sure.
- Line 216 pins `near_s == 35 and far_s == 360.0` "as found", which makes line 217's band
  redundant: the test is a change detector for both fights at seed 7. Low.
- Line 132 `len(heard) >= rounds // 2`: half the rounds may go unheard. Low.
- `test_the_toggle_off_...` (142-154) sets the module global `FA.ENABLED` and restores it in
  `finally`: sound, and the toggle test is useful.
- `test_a_far_ship_replies...` (287) resets the module global `FA.FALLBACK_COUNT` and never
  restores it; harmless under xdist groups. Low.

**(c)** `_two_in_anger` plus `_run_until_struck` is sailed in full by tests 93 and 224; the
first could hand its world to the second. `test_a_hull_fought_awake...` (255) and test 176
build the same near action of truth 7-140, which `test_known_truths.py` also sails.

## test_far_hail.py (142 lines)

**Count and kind.** 3 tests; no fixture; `two_far_hulls` sets up two far hulls with fakes,
`hail_and_answer` sails until the answer. Two tests are slow (conftest 515-516). Proves a far
hull's hail goes to her captain's model and back, the table answer for an unheld ship, replay.

**(a)**
- `test_a_ship_nobody_holds_is_answered_by_table_far_or_full` (125-130): "far or full" in the
  name; the body sets up the far case only (`b.crew.shape == "far"`, 127). The full case is not
  in this file. Low, sure.

**(b)** None strong.

**(c)** `test_a_far_hulls_hail_goes_to_her_captains_model...` (121-122) is `hail_and_answer()`
and nothing else; `test_the_hail_between_two_far_hulls_replays...` (133) calls the same and adds
the replay. The first is a strict subset of the third, two slow passages for one. Truths 7-393
and 7-394 sail it twice more (conftest 517-518).

## test_fight.py (505 lines)

**Count and kind.** 12 tests, no fixture; `_alongside` makes a frigate at quarters and a crewed
French frigate beside her (65 s run). Proves the quarter bill's figures, the musket's chance,
the marines, the small arms, grapple, boarding repulsed and carried, repel boarders, the rules
captain's musketry, and (oddly) the director's `aboard:` forms.

**(a)**
- `test_the_director_puts_men_on_the_sick_list_and_hurts_an_officer...` (467-505) tests the
  director's sickness forms; it belongs with `test_health.py`. Low.

**(b)**
- Line 183: `any(s.station is Station.QUARTERDECK for s in hurt) or len(hurt) < 6`. The docstring
  promises "the quarterdeck's share"; under six hurt the share is not checked. Low, sure.
- Line 411: `enemy.run(5) if hasattr(enemy, "run") else w.run(5)`: the test does not know what
  its own object is. Low.
- Lines 445-451: three alternatives `or`-ed for "the arms served"; line 435 already checks the
  words. Low.
- Lines 452-453: `ours = [...hurt]; assert all("musket ball" in s.hurt_how for s in ours)`. The
  docstring says "our people fall to his musketry"; with nobody hurt `all([])` is true. The test
  passes if the French musketry hits nobody. Medium, sure.
- Line 360 `2 <= f.round <= 12`: the docstring says "a few rounds". Low.

**(c)** None beyond `_alongside`.

## test_filling.py (501 lines)

**Count and kind.** 12 tests, no fixture; the cutter (one man filling) and the frigate (ten).
Proves who fills, when not, the waits and outages, powder running out, the report, old
pickles.

**(a)** None.

**(b)** `fill_tick` is called directly on a hand-set magazine (127-133, 143-159, 369-386):
precise man-second arithmetic (600 / 135 = 4 cartridges, 131), checkable by a reader. The hoy
alongside is stood in for by `w.stores.galley_fire_out = "powder"` (142, 188); I checked that
`freesail/world/ordnance.py:570` and `:668` are the only writers, so the stand-in is faithful.
Line 501 `all(g.loaded in (None, Charge.ROUND) ...)` admits nearly any state. Low.

**(c)** None.

**Else.** A sound file.

## test_fishing.py (323 lines)

**Count and kind.** 15 tests, no fixture; two slow (conftest 458-459). Proves the fishing data,
grounds, gear, the catch function, the well and the hold, spoilage, orders, the quay, far
fishermen, the glass by tiers, a made-out line, a checkpoint.

**(a)**
- `test_the_spoilage_is_said_when_a_lot_turns_and_once_a_day_and_salt_keeps` (145-155): the
  catch is stowed with `salt=None` (148), so nothing is salted and "salt keeps" is not tested;
  "once a day" is checked after one hour only (150-151), not over a second day. Two of the
  name's three clauses are not in the body. Medium, sure.
- `test_the_business_fishermen_are_crewed_like_any_other_ship_near_the_player` (219-220)
  asserts a constant, `CR.FAR_ONLY_ROLES == frozenset()`; the same assertion is in
  `test_business.py:197`. No ship is crewed. Low, sure.

**(b)**
- `test_a_made_out_line_gives_her_bearing_and_the_course_she_stands` (267-294): `made` is never
  asserted non-empty; the loop at 288-289 is the only check of the name's "made out line gives
  her bearing". If no `lookout.made_out` line is logged in the 180 s, the test passes on the
  reading and the glass alone. Medium, sure.
- `test_every_ground_fish_and_yield_carries_its_source...` (67-71) checks that each source string
  contains "judgement", "Holdsworth" or "EB 1810": a test of the data's wording. Low.

**(c)** None.

## test_flag_drawings.py (694 lines)

**Count and kind.** 22 tests; one parametrised over 6 signal roots (198); 27 cases. Three need
Node (`skipif`, 97, 152, 358) and run the client's `projection.js`. Proves the widened drawing
form, every signal flag drawn, numerals by the year, hoists in order and at their place,
dressing ship, the nations' days, an old save.

**(a)**
- `record()` (79-84) is the writer of the golden fixture, kept in the test module and never
  called by a test. Low.

**(b)**
- Golden pins: `test_every_colours_drawing_is_served_as_before_the_package` (87-94) and
  `..._drawn_as_before_the_package` (97-105) compare every flag of every root with
  `tests/fixtures/flag_drawings_before_102.json`, recorded from the code at package 102's head.
  Two golden pins over every flag. Their purpose ("as before the package") is spent once the
  package is merged; now they make any mended flag drawing fail with no sign of whether the old
  or the new is right. Medium, sure.
- `test_dress_ship_is_refused_below_as_the_colours_are` (502-514) asserts only that the two
  refusals end in the same words after the last colon (514); two refusals of any kind with the
  same tail pass. It never checks the words say "go on deck". Low, likely.
- `test_a_fleet_in_harbour_dresses_on_its_nations_day_and_not_on_another` (580-597): the
  docstring has the French ship "at anchor beside her"; `_harbour` puts her at 49 20 N 7 30 W
  (573), about a hundred miles off, "for the test". Whether she stays undressed by her nation or
  by her distance (far detail) the test cannot tell. Line 588 `getattr(..., "dressed", False)`.
  Low, suspicion.
- The Node tests skip where Node is absent; Node is on this machine (`/opt/node22/bin/node`) and
  the CI workflows do not set it up (no `setup-node`), relying on the runner image. Low,
  suspicion.

**(c)** `_harbour` days (580, 600, 631, 654) each sail the morning again; fine.

**Else.** This file tests the viewer's geometry as well as the game: the JS runs from a Python
test (`tests/test_view_geometry.run_js`).

## test_flags.py (321 lines)

**Count and kind.** 10 tests; one parametrised over 6 roots; 15 cases. Four are slow
(conftest 107-110), each a quarter of an hour sailed. Proves the colours files, what flies
where, the lookout's words, flag orders, the private signals in succession, truth 7-457.

**(a)**
- `test_the_private_signals_in_succession_unanswered_make_her_an_enemy` (208-237): the
  docstring says "three minutes a hoist"; line 231 asserts 300 s between hoists. One of the two
  is wrong. Low, sure.

**(b)**
- `test_the_lookout_reads_the_pendant_and_the_broad_pendant...` (113-132): the broad pendant is
  tested by setting `brig.role = "commodore"` by hand (131) on a merchant brig, not a
  commodore escorting a convoy as the docstring says. The words function is tested; the role's
  flight is the test's own setting. Low.

**(c)** None.

## test_found_on_the_way_85.py (124 lines)

**Count and kind.** 4 tests, no fixture. Proves four mended refusals: an apostrophe in a
standing order's name, a rig word matched in sight only, `captain: carry on` at the prompt,
`gybe the mainsail`.

**(a)** None. **(b)** The `try/except/else: raise AssertionError` forms (50-55, 116-122) are
correct (a passing call fails the test). **(c)** None. Sound.

## test_gale.py (611 lines)

**Count and kind.** 27 tests; two parametrised (3 and 2 cases); 30 cases. Module fixture
`frigate_by_the_wind` (222-224; `full_and_by`, 400 + 900 ticks). Proves the trim by levels,
yards by hand in points, the helmsman's mark, storm canvas, aback and recovery, heave to with
sternway.

**(b)**
- `test_headed_full_and_by_the_helm_keeps_her_away_and_says_so_once` (327-335): asserts
  `len(kept) <= 1` (334), true with nothing said, and `not events("ship.lifting")` (335), true if
  nothing happened. Nothing checks that her head came off. A helm that does nothing passes.
  High for what the name claims, sure. It also takes `frigate_by_the_wind` as a parameter and
  never uses it (327-328 builds its own `full_and_by`), so the module fixture is built and the
  test is joined to its xdist group for nothing.
- `test_heave_to_with_sternway_lies_to_drifting_and_says_so` (596-611): sets `u = -3 kn` (608)
  and reads `inst.script.words()`; the evolution is never run to "Hove to", so "lies to
  drifting" is the test's own setting read back. Low, sure.
- `test_a_schooner_keeps_the_mean_of_her_sails` (321-324): asserts a key is absent; passes if
  the helm logic never ran. Low.
- `test_full_and_by_with_the_yards_braced_sharp_up...` (314): `78 < off < 92` for "the old rule".
  Fair.
- `test_full_and_by_two_minutes_in_irons...` (593) `"boxed_off" not in ...extra` is weak; the
  rest of the test (587-590) is exact. Low.

**(c)** `full_and_by` is sailed afresh by 246, 254 (twice), 321, 327 for one assertion each;
the yards-by-hand tests (159, 184, 198) each sail 300 to 400 ticks of the same setup.

## test_geo.py (298 lines)

**Count and kind.** 13 tests, no fixture. Proves the sphere's arithmetic, positions in words,
the plane without a position, the position kept from her run, the scenario's position, region
and chart fields, saves.

**(b)** Line 260-281 pins the chart's list of 20 regions: every new region edits this test, a
change detector of the data. Low. Everything else is arithmetic a reader can check (40, 51, 92).

Sound.

## test_grammar_book.py (186 lines)

**Count and kind.** 9 tests; fixtures `grammar` (module: a naval-cruise world made and the
library's grammar page rendered) and `primer` (module: every `docs/primer/*.md` read). This
file tests documents: the generated grammar page against the vocabulary, and the hand-written
primer against the vocabulary and the registry.

**(b)**
- `test_every_world_order_form_is_named_in_the_primer` (170-174): the docstring says "in the
  director's chapter"; the body takes the first word of each form (`f.words.split(":")[0].split(" ")[0]`,
  173), words such as "ship" or "aboard", and looks for it anywhere in the whole primer flattened
  to one string. It cannot fail while the primer uses those common words. Medium, sure.
- `_named` (142-143) is a substring test of the whole primer: a verb such as `set` is found
  inside any word containing it. `test_every_verb_of_the_vocabulary_is_named_in_the_primer`
  (146-156) is weak for short verbs. Low, likely.

**Else.** The first three tests guard a page "complete by construction" (docstring 4-7): they
test the generator against its inputs, which is fair.

## test_ground.py (411 lines)

**Count and kind.** 10 tests; module fixture `standing_on_by_account` (76-84: the schooner
sailed up to five hours to the Manacles). Proves truth 66 (grounding by account, and not with
the lead), the strike's consequences, the director's leak orders, the shock to the masts,
kedging, soft ground, drying rocks, an old pickle.

**(b)**
- `test_truth_66_the_same_passage_with_the_lead_going_hourly_does_not_ground` line 139:
  `assert w.submit(line).kind != "order.refused"`. No code emits `order.refused` (grep over
  `freesail tests tools client`: only this line and `test_health.py:247`). A standing order
  refused (`order.rejected`) passes the assertion; the test would then fail later only if the
  ship grounds. Medium, sure.
- Line 103: "five knots or six knots" in the strike line; 102, within 1.5 kn of the log. Fair.
- Line 164: `"(rock)" in where or strike.data["rock"]`. Low.

**(c)** `on_the_falmouth_bank` is sailed by 271 (twice), 362, 389, and the soft-ground test
(306-339) builds the same scenario again inline (309-323) instead of calling it.

**Else.** Truth 66's two clauses are a strong pair.

## test_hands.py (1060 lines)

**Count and kind.** 32 tests; three parametrised (20 compatibility cases, 3 from-the-gear, 6
belay forms); 58 cases. No fixture; the compatibility rule sails 40 worlds, 1,200-tick setups
for the manoeuvres; eleven entries in `SLOW_TESTS`. Proves the hands pool, the crew factor,
short-handed running, pre-emption by all hands, belaying work, parties.

**(a)**
- The module docstring (9-11) says "The composer does not yet give the runner the World's clock
  ... these tests set `runner.clock = world.clock` themselves, as that line will";
  `freesail/api/session.py:82` has done it for some time. The line at 115 is now redundant and
  the docstring stale. Low, sure.
- `FakeRoutine.tick` (426-428): a statement after `return`, never run. Low, sure.

**(b)**
- `test_tack_ship_belays_the_topgallant...` line 487: `300 <= t + 31 <= 600`. Fair.
- The comment at 821 says the forms "are all taken"; the body asserts each is rejected (824):
  parsed, then refused for nothing to belay. Misleading, not wrong. Low.

**(c)** `close_hauled_frigate` (431-445) sails 1,200 ticks for each of three tests.

**Else.** `test_compatibility_one_evolution_with_the_watch_on_deck` (620-629) proves the crewed
ship finishes each of the twenty milestone-2 evolutions on the same tick as the uncrewed: a
strong regression guard. `test_three_topsails_are_reefed_together...` (974-1018) checks the
party bound on every tick.

## test_harbour.py (702 lines)

**Count and kind.** 16 tests; fixtures `port` and `client` (function scope, a FastAPI
`TestClient`), `browser_page` (a live uvicorn server and Chromium through Playwright). Two
tests start a live server; one starts the API door as a subprocess against a fake Messages
server. It tests the launcher, the scenario maker, the settings and the desktop config writer,
not the game's sailing.

**(a)** None found. `station_watcher` is imported and unused (227).

**(b)**
- `test_in_the_browser_a_game_is_started_and_the_four_scenarios_round_trip` (504-553): the
  fixture skips if Playwright cannot find a browser (484-492). `whole-suite.yml:77-81` says the
  CI runners "have Playwright the package and no browser, so every test that wants one skipped";
  the browser job runs only `tests/test_browser_probe.py` (line 100). This test therefore runs
  on the build machine alone and can break unseen. Medium, sure.
- `test_the_api_door_started_from_the_harbour...` line 448-450:
  `any("credential store" not in ln and "environment" in ln ...)`: any output line with the word
  "environment" passes. Low.
- `test_the_harbour_starts_a_seats_door_as_the_directors...` (594-683) monkeypatches
  `start_door` and `_stop_seat_door` (638-639), so the door's start and stop are fakes; the
  docstring says so ("without a subprocess"). It tests the argv and the tending, fairly.
- Line 702 starts a subprocess (`Door("d10", ...)`) that is never waited for. Low.

**(c)** None.

## test_harness_instruments.py (205 lines)

**Count and kind.** 8 tests, no fixture; each world sails 600 ticks before the test and up to
90 minutes after. Proves the sample's deltas, the captain's word once, tripwires, `ahead`,
the cost-of-thinking line.

**(b)**
- `test_the_directors_ahead_is_the_truths` (182-190): line 187-189 is
  `endswith(("by the truth: open water, 29 fathoms by the chart",)) or ("by the truth" in ...)`.
  The second operand makes the first moot: any line containing "by the truth" passes. Nothing
  checks the director's line reads her true place rather than her account. Medium, sure.
- `test_her_way_settled_wakes_her_two_minutes...` (134): `at` is the first `agent.resumed` of
  any kind (133), and the bound is `a glass // 15` = 120 s; the docstring's "two minutes" is
  right. Fair.

**(c)** None.

## test_health.py (373 lines)

**Count and kind.** 12 tests, no fixture. Two run long: `test_the_water_expended...` runs the
cutter five days (195), `test_the_dead_are_buried...` the frigate 46 hours (224, 228). Neither
is in `SLOW_TESTS`; I did not time them and do not know whether `run` is fast enough to keep
them under the threshold. Proves wounds, the surgeon, healing, the sick list, thirst, burial,
the butcher's bill, a station holder hurt or killed.

**(a)** None.

**(b)**
- `test_bury_the_dead_by_order_reads_the_service_at_once` line 247: `kind != "order.refused"`
  can never fail (no such kind exists). Lines 248-250 do the work. Low, sure.
- `test_a_holder_killed_ends_his_station_and_the_captain_killed_passes_the_command` line 372:
  `w.people.captain.role != "first lieutenant" or w.people.captain.name in passes[0].text`. The
  docstring says "the first lieutenant takes the command"; the assertion passes whoever takes it
  so long as it is not the first lieutenant, and checks the name only if it is. The succession
  order (`freesail/crew/health.py:434-441`) is not proved. Medium, sure.
- Line 203-206: `"Mr Bowen is dead of thirst" in e.text or captain.name in e.text`. Low.
- `_hit` (43-51) forces the wound's gravity after the draw: fair, and said.

**(c)** `test_fight.py:467-505` tests health's director forms; it belongs here.

## Faults to plant

1. **test_gale.py::test_headed_full_and_by_the_helm_keeps_her_away_and_says_so_once.** In
   `freesail/physics/integrate.py` lines 253-258 delete the `ship.note("routine",
   "helm.kept_away", ...)` call (keep the `return` at 259). The name says the helm keeps her
   away and says so once. Prediction: passes (`len(kept) <= 1` holds with none, and no
   `ship.lifting` is emitted because the `return` stays).
2. **test_far_action.py::test_a_packet_that_fights_is_brought_to_by_the_privateers_rounds_and_taken.**
   In `freesail/combat/far.py` line 187 change `shots = whole + (1 if rng.random() < frac else 0)`
   to `shots = 0 if firer.nation == "britain" else whole + (1 if rng.random() < frac else 0)`
   (the packet never fires). The docstring says she fires her guns within four cables.
   Prediction: passes (line 361 is `>= 0`; the packet still strikes by morale under fire).
3. **test_fight.py::test_the_rules_captain_opens_musketry_within_a_cable_and_serves_out_the_arms_by_his_doctrine.**
   In `freesail/combat/small_arms.py` line 183 change `if range_m >= MUSKET_SHOT_M:` to
   `if range_m >= MUSKET_SHOT_M or kit.get("volley_s") == 30:` (the French kit's figure,
   `data/marines.yaml:54`: the enemy's musketry never hits). The docstring says our people fall
   to his musketry. Prediction: passes (`all()` over an empty list, 452-453). (Seen in passing,
   not a test finding: line 185 `float(kit.get("hit_at_50_yd", 0.04) or 0.04)` turns a kit
   filed with 0.0 into 0.04, so the data cannot say "never hits".)
4. **test_health.py::test_a_holder_killed_ends_his_station_and_the_captain_killed_passes_the_command.**
   In `freesail/crew/health.py` line 435 delete `"first lieutenant",` from the succession. The
   docstring says the first lieutenant takes the command. Prediction: passes (line 372 accepts
   any other role), likely; unless the first lieutenant was the officer already killed, in which
   case the fault is invisible here anyway.
5. **test_fishing.py::test_a_made_out_line_gives_her_bearing_and_the_course_she_stands.** In the
   lookout's made-out line (`freesail/world/lookout.py`, the `lookout.made_out` text) drop the
   `", bearing ..."` clause. Prediction: passes if no `lookout.made_out` line is logged in the
   180 s (the list is never asserted non-empty); fails otherwise. I could not tell which without
   running it.
6. **test_ground.py::test_truth_66_the_same_passage_with_the_lead_going_hourly_does_not_ground.**
   Make the standing-order parser refuse the `if the depth is under 41 fathoms` condition (so
   the "haul off" order is `order.rejected`). The name says the lead's passage does not ground.
   Prediction: the assertion at 139 passes regardless; the test fails only if she then grounds
   within six hours, which depends on the stand-on order; suspicion.

**Faults no test in my files would catch, though a player would:**

1. (Present now, not planted.) `freesail/evolutions/scripts.py:1831-1837`: a tack ended by the
   steady timeout names the tack she lies on but the heading she was meant to take; the log says
   "starboard tack, heading SSE (158°)" while she heads 035°. `test_evolutions.py:890` pins it.
2. In `freesail/world/fishing.py` line 548 change the salted lot's `None` to `tick + 12 * 3600`
   (salted fish spoil like green). No test in my files checks a salted lot's spoilage
   (`test_fishing.py:139` checks the green lot only; 148 stows with no salt).
3. In `freesail/physics/integrate.py` line 247 swap the words:
   `side = "larboard" if st.awa >= 0 else "starboard"`. "Kept her away, the wind 50° on the
   larboard bow" with the wind on the starboard bow. `test_gale.py:327-335` counts the lines and
   never reads them.

## What I did not do

I ran no test and no world, so the timing of `test_driver.py` (about twenty 1,200-tick
settlings, none in the slow tier) and of `test_health.py`'s five-day and two-day runs is
unknown to me; nor do I know whether `test_fishing.py:288`'s list is empty in practice. I did
not read `tests/rig_fixtures.py`, `tests/test_between_hulls.py`, `tests/test_crews.py`,
`tests/test_brains.py`, `tests/test_view_geometry.py` or `tests/messages_api.py`, which these
files import, beyond the names they call; nor the JSON fixture's contents; nor the code under
test beyond the functions cited.
