# Tests reader 02b: tests/test_known_truths.py, line 8700 to the end

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Read whole from line 8600 (to pick up the
truth that straddles the boundary) to line 17391, with the file's head (lines 1 to 260:
imports, helpers and the module fixtures) and `tests/conftest.py` whole. The suite was not
run. Counts below were taken by parsing the file with `ast` (a few seconds of Python) and
by grep; everything else is from reading.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| tests/test_known_truths.py, 8700 to 17391 | 8,692 | 287 functions (292 cases: one parametrised into 6) | none module-scoped in this half; tests sail their own worlds, some for days of game time (see 1) | duplicates other files wholesale (102 bodies are calls of other files' tests); about half the rest pin data, text and tool output; the remainder prove real behaviour and some prove it well |

## 1. Count and kind

- **287 test functions** from `test_truth_7_145_...` (line 8702) to `test_truth_7_570_...`
  (line 17333). One is parametrised: `test_truth_7_501_...` (line 16068) into six roots.
  The truth that straddles the line, `test_truth_7_144_...` (8624 to 8699), is the other
  reader's; I note one fault in it under (b).
- **No module- or session-scoped fixture is defined in this half.** None of the
  `DAY_FIXTURES` names for this file is used after line 8700. Every test builds its own
  World, so the cost is per test: for example 7-154 sails 50,400 ticks (line 9118 and 9124),
  7-178 sails five days, 432,000 ticks (line 10373), 7-294 sails 98 hours (line 12025),
  7-519 61 hours, 7-539 96 hours, 7-200 a day of a fake captain's passage.
- **Slow tier.** By the conftest's three roads (the `SLOW_TESTS` ids, a hand mark, the pace
  rule) **88 of the 287 are slow-tier**: 60-odd by `SLOW_TESTS` id, **16 by a hand-written
  `@pytest.mark.slow` in this file** (7-200, 7-320, 7-352, 7-353, 7-357, 7-358, 7-360,
  7-364, 7-368, 7-369, 7-448, 7-519, 7-529, 7-539, 7-565, 7-570), and 6 pace tests (7-151,
  7-159, 7-160, 7-334, 7-361, 7-386; four of them hand-marked `@pytest.mark.pace`). No id in
  `SLOW_TESTS` for this file is stale (checked against every function name).
- **What the half proves.** Milestone 7's sea: signals and convoys, squadrons and blockade,
  practice at the guns and powder taken in, water, damage and wounds, the fight on deck,
  prizes and prisoners, the business and the regimes, and then a long run of chart blocks
  (Channel east, Mediterranean west, Gulf of Lion, Tyrrhenian, Catalan coast, Barbary, Sicily,
  Canaries) with their tides, lights and ports, plus the knowledge-by-place, boat, visitor,
  letter, flag-drawing and viewer packages.

### The truths taken as rows

| kind | count | which |
|---|---|---|
| body is nothing but calls of tests in other files | **102** | listed under (c) |
| calls other files' tests and adds a few asserts of its own | 3 | 7-333, 7-367, 7-436 |
| sails or orders the game itself (a World run, an order given) | 91 | of these 5 are pace measurements; perhaps 70 prove a behaviour through the game in a way a player would recognise (7-145 to 7-184, 7-200, 7-260, 7-271 to 7-274, 7-279, 7-286, 7-288, 7-290, 7-291, 7-294, 7-297, 7-302, 7-340 to 7-342, 7-426, 7-445, 7-491, 7-492, 7-494, 7-498, 7-499, 7-514, 7-519, 7-529, 7-539, 7-540 to 7-544, 7-580 to 7-582) |
| no World run and no order: data, chart cells, tide constants, yaml text, a tool's output | 94 | 7-158, 7-261 to 7-264, 7-266, 7-275 to 7-278, 7-280 to 7-285, 7-287, 7-289, 7-292, 7-293, 7-295, 7-298 to 7-301, 7-303 to 7-314, 7-427 to 7-432, 7-442 to 7-444, 7-350, 7-447, 7-490, 7-493, 7-495 to 7-497, 7-510 to 7-518, 7-520 to 7-528, 7-530 to 7-538, 7-545, 7-560 to 7-565, 7-570, 7-583, 7-584 and others |

So of the 185 truths with a body of their own, about half prove a behaviour through the game
and half pin a number, a feature list, a stance table, a text or a tool's verdict. Many of
the second half are legitimate checks of data the game reads (a lighthouse's year, a port's
nation by date), but they are data audits and not "how the game behaves"; several test a
tool in `tools/` (see 5).

## 2. (a) Tests of what is no longer there or no longer matters

- **Old faults kept alive behind switches, and tested to still happen.**
  `test_truth_7_340_...` (13255) asserts the mend, then sets `captains.ABACK_RECOVER = False`
  and asserts the brig still lies aback with no way (13278 to 13282). `test_truth_7_341_...`
  (13285) does the same with `navigation.WEAR_ROOM` (13323 to 13325), `test_truth_7_342_...`
  (13328) with `signalling.TRUE_COLOURS_HELD` (13375 to 13376: the flicker at 5700 must still
  occur), `test_truth_7_350_...` (14567 to 14576) re-creates the zero-length far ship by hand,
  and 7-358 runs `test_the_toggle_off_leaves_the_world_as_it_was...`. Each keeps a known
  defect as a supported, tested path of the code. Weight medium (dead branches the suite
  forbids anyone to delete), confidence sure.
- **A name that promises a passage and a body that sails nothing.**
  `test_truth_7_512_a_ship_sails_from_port_mahon_to_carloforte_and_from_algiers_to_tunis`
  (15839): no ship is made; the body walks `chart.line_shore` and `elevation_at` along
  waypoints typed into the test (15850 to 15862). 7-536 (16734) and 7-537 (16794) are the
  same shape, named more honestly ("may sail"). These prove the chart has water along a line
  the author chose, not that a ship or the business's routing can make the passage. Weight
  medium, sure.
- **Docstring and body differ.** 7-146's docstring says the French book's refusal is "refused
  in words" (8749); the body only checks `S.load_books("france").encode(...)` raises
  (8778 to 8779), no order is given. 7-179's docstring promises the quarterdeck "two times in
  five" (10398); the body forces the draw with a fake RNG (10413 to 10430), so the share is
  never measured. 7-183's docstring says the privateer's carpenter plugs holes under water,
  and then says at this seed none lie under water (10580 to 10584), so that clause is never
  exercised. 7-334 computes the frigate-alone figure its docstring describes and only prints
  it (13126). Weight low to medium, sure.
- **A source "FROM MEMORY".** 7-496's docstring rests Barcelona's 1808 seizure on memory
  (15587), the file's own rule (7-261, line 10956) being that no source leans on memory alone.
  The test checks the data's date, not the source. Low, sure.

## 3. (b) Tests built not to fail

- **Or-shaped and conditional assertions in the first action replayed.**
  `test_truth_7_183_...` (10543): `any(... in w.log) or w.ship.extra["musketry"].served`
  (10575 to 10578); `if under:` (10583, which its own comment says is empty at seed 7);
  `events(enemy, "pumps.manned") or enemy.water.depth_m() < 0.3` (10585);
  `"killed" in bill or "wounded" in bill` (10587); `if killed:` (10592). Five of its
  behavioural claims can pass with the behaviour absent. High weight (this is the scenario the
  owner plays), sure.
- **The gunnery stepped round.** `test_truth_7_176_a_broadsides_casualties_...` (10278) and
  7-177 (10320) fire no broadside: they call the private `HITS._casualties` twelve times
  (10294 to 10296), and set `keeper.hits = 12` and `keeper.struck_by` by hand (10307 to 10308)
  to make the bill appear. The captain's hurt line is checked only `if cap.hurt:` (10305), the
  killed man's name only `if killed:` (10313). A broadside that hurt nobody would pass. High,
  sure.
- **The state under test set by the test.** 7-147's bell at anchor: the test sets the rider's
  `sail_state = "at anchor"` and `vessel_locker(rider).fog_signals = True` (10850 to 10852),
  though the code sets fog signals itself (`freesail/world/signalling.py` 895 to 902), so the
  automatic road is never exercised. 7-150 sets the far ship's lantern by hand (8958) and then
  checks only that the player's `hoist a stern lantern` changes his own reading (8962 to 8965).
  7-167 and 7-169 set powder and cartridges by hand (stated in their docstrings). 7-179 forces
  the RNG (10426). 7-341 sets `dyn.u` (13320). 7-584 jumps `w.clock.tick` and calls the private
  `w.business._blockades()` (16557 to 16558). 7-260 jumps the clock over 55 hours (10906).
- **Bands widened to the measurement.** 7-271: "re-measured to 0.8" after measuring 0.648
  against a bound of 0.6 (11285 to 11290). 7-280: "within a foot" became 1.25 after measuring
  1.01 (11555 to 11557). 7-290 and 7-291 allow a 6.0 m depth step at a seam (11924, 11960)
  where 7-274 allows 1.0 (11390). 7-161 and 7-183 accept a strike anywhere from 45 minutes to
  three hours after the first shot (9439, 10572) against docstrings that say 59 or 90 minutes.
- **Pins with no reason a reader can check.** Exact tick pins of the seed's run: 7-145
  `ticks == [900, 1080, 1260, 1440]` (8742), 7-152 `(2040, 2182, 2340, 6060)` (9066), 7-154
  ticks 11400, 37920, 43200 (9119, 9125, 9128), 7-260 `197345` and `197400` (10898, 10911),
  7-340 `[1800]`, `[1980]`, `[2110]`, 2160 (13273 to 13276), 7-342 the first three
  colour states with ticks (13367 to 13371), 7-350 `(0, 4, 3)` and `(1, 5, 3)` (14575 to 14576).
  Counts pinned to whatever the data now holds: `len(nations) == 16` (10949, its comment a
  history of bumps), `len(knobs) == 6` (10931), 109 and 158 tiles (16640, 16882), `== 4593`
  tiles (17391), `== 3 * 149504` cells (17080), `squares == 33` (17329), `len(land) >= 210`
  (12548), 24 ways in and 24 out (16297). I count about 30 such pins in the half. Exact text
  pins of refusals and lines run to several dozen (7-165, 7-167, 7-168, 7-240, 7-244, 7-426
  ...). Medium, sure: each breaks on any honest change and tells nobody whether the game is
  right.
- **Code compared with itself.** 7-172 checks the leak against `W.orifice_t_per_h` of the
  same module (10166; the 75 to 95 band beside it is independent). 7-570 builds its expected
  tile with `Tile.filled_from`, the method under test (17377). 7-295 re-implements the weather
  stream's seeding, `hashlib.sha256(f"7:weather:{serial}")` (12089), so it would not notice
  the game seeding differently.
- **Assertions satisfied by construction or vacuous.** 7-309: `block in tide.blocks_at(p) or
  block in ("madeira", "azores")` (12640) is vacuous for two of its three cases. 7-270:
  `"nab-light" not in in_sight or not ...lit_in(1805)` (11234). 7-172: `"pumps" in words or
  "lifting" in words` (10181). 7-441: `out["smoke"] >= len(fires) or not fires` (14377).
  7-174's last check `speed <= max(speed, 0.1)` (10239) is near-tautological. 7-156
  `all(g != 180 ...)` (9194) is implied by the line before. 7-155 asserts the constant
  `K.CREWED_CAP >= 3` (9160).
- **Wall-clock timing in the fast tier.** 7-284 asserts the tide's fresh cells within 1.25 of
  the old and a lookup under 20 microseconds (11712, 11716); 7-441 asserts a part of the
  snapshot under a quarter of the whole (14388). Neither is named or marked as pace, so both
  run in the fast tier under `-n 4` beside other workers, which the conftest's own note
  (`_is_pace`, conftest 648 to 657) says reads the load, not the code. Flaky by design.
  Medium, sure.
- **Hedged calls.** `enemy.run(60) if hasattr(enemy, "run") else w.run(60)` (10433);
  `h.release("the test is done") if hasattr(h, "release") else None` (10821); `if named:`
  guarding 7-179's last asserts (10436).
- **Half a test dropped silently.** 7-500 and 7-502 run the drawing half only
  `if shutil.which("node")` (15733, 16368), with no skip reported; on a machine without Node
  they pass having tested half.
- **Boundary note (other reader's truth).** 7-144 line 8658:
  `[s ...][:3] == [...][:2] or ("chasing" in [...])` compares a three-slice with two items, so
  only the `or` can hold; the `next(...)` on 8661 would raise anyway.
- No `xfail`, no `skip` in this half except the honest importorskips (Playwright, fastapi,
  the vendor SDK of pyproject.toml:29) and 7-450's Node skip; one broad `except Exception` (15093) turns a browser
  failure into a skip, which is reasonable for 7-448.

## 4. (c) Tests that might be one

- **102 truths are bodies of calls to tests in other files, 197 distinct twin functions in
  31 files**, each twin also collected in its own file, so each runs at least twice a full
  run. By file: test_knowledge 40, test_sail_by_name 14, test_flag_drawings 14, test_captive
  11, test_letters 11, test_boat_hull 10, test_view_action 8, test_far_action 8,
  test_prize_court 8, test_flags 7, test_prizes 7, test_aboard_another 6, test_between_hulls
  5, test_boat_director 5, test_viewer_action 5, and 16 more files with 1 to 4. The wrappers
  are 7-320 to 7-332 (less 7-333), 7b-113 and 7b-114 in part, 7-351 to 7-369 (less 7-350,
  7-361 and the part-wrapper 7-367), 7-370 to 7-401, 7-420, 7-421, 7-433 to 7-439 (7-436 a
  part-wrapper), 7-443, 7-446, 7-449 to 7-461,
  7-470 to 7-479, 7-501 to 7-506. **The twin and the truth do not differ at all**: the truth's
  body is the twin's call, its only difference the docstring. Some twins run three times:
  `test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks` is called by 7-370 (13485)
  and by 7-373 (13524). 7-433 (14160) loops test_signals' twin over spain, united-states and
  naples, cases the twin already runs by its own parametrise. 7-501 repeats
  test_flag_drawings' parametrise over the same roots. 7-565 (16339) is
  `test_chart_audit.py::test_the_full_sweep_is_the_known_list_exactly` (92) again, both slow.
  `SLOW_TESTS` lists both halves of several pairs (conftest 122 and 129, 141 and 142, 145 and
  146, 147 and 148, 159 and 160, 505 to 509, 511 and 512, 515 to 518): the slow tier pays twice.
- **Four slow twins run in the fast tier through their truths**: 7-355 runs
  `test_captive::test_a_far_body_that_takes_the_players_ship_is_made_a_hull_and_holds_him`,
  7-362 runs `test_prize_court::test_a_far_prize_in_her_goals_road_is_sentenced_on_her_record`,
  7-366 runs `test_court::test_the_captor_holding_the_players_person_is_refused_for_both_reasons`,
  7-367 runs `test_director::test_every_world_order_form_has_examples_that_parse_and_that_the_game_performs`
  (in `SLOW_TESTS`, conftest 462). The tier the twins were put in is defeated.
- **Marks bypassed.** Calling a twin by name drops its decorators. The view twins are
  `@needs_node` (test_view_action.py 77 onward); 7-437, 7-439, 7-451 to 7-454 call them
  without the skip, and 7-440 to 7-444 call `run_js` directly, whose `NODE` is `None` without
  Node (test_view_geometry.py 172): on such a machine these truths error where their twins skip.
  Only 7-450 guards itself (15138).
- **Families that want one table-driven test** (the same 10 to 20 lines with other numbers):
  the anchorage holds six hours, 7-273, 7-288, 7-297, 7-494, 7-514; the seam crossed with the
  business carried, 7-157, 7-274, 7-290, 7-291, 7-302, 7-491, 7-492; the frigate sails a block
  by her short book, 7-279, 7-294, 7-499, 7-519, 7-529, 7-539; the lights by year,
  7-276, 7-285, 7-292, 7-296, 7-298, 7-300, 7-497, 7-517; ports' stance tables, 7-275, 7-289,
  7-299, 7-301, 7-496, 7-518; the master's tide-hour by place, 7-278, 7-293, 7-304; the pace
  of a convoy, 7-151, 7-159, 7-160; each road "as its pilot has it", 7-524, 7-535, 7-538.
- Scenario twins outside the file: test_scenarios.py loads each block's scenario
  (spithead.yaml at 333, mahon.yaml 376, tarragona.yaml 420, bona.yaml 459, the-faro.yaml 497)
  without sailing it; the truths sail them, so they do differ. test_signals.py 115 to 121 is
  7-146's encoding half verbatim (the same twelve numbers and the same French refusal). The
  practice truths overlap test_practice_orders.py (engage the cask, exercise the battery,
  heave a cask), the powder truths test_ordnance.py and test_powder_orders.py, the water
  truths test_water.py and test_damage_control.py, the fight truths test_fight.py (7-179 to
  7-181 use its `_alongside`), 7-182 test_health.py's helpers; I did not read those files and
  cannot say how far they repeat.

## 5. Anything else

- **Good tests that prove something hard** (one line each): 7-166 (the cask lost, seen and
  lost again in haze, no round fired while unseen); 7-170 and 7-171 (checkpoint, resume and
  replay compared in the same run, digest for digest); 7-169 (powder conserved to the pound);
  7-164 (`vars(mag) == start` after twenty minutes of dumb show); 7-200 (a fake captain's whole
  day ashore and back, both logs checked for what each must and must not hold); 7-282, 7-283,
  7-312, 7-314 (old tide bit-for-bit outside the new blocks); 7-530 (every older port the same
  on every day); 7-545 (every scenario's patrol square in water and clear of land).
- **Tests of tools and documents, not the game.** 7-261 (every yaml knob's source matches a
  citation regex), 7-262 (the knobs equal themselves read from data), 7-295 and 7-304
  (`"NW 10" in note`, `"gales 7" in note`: strings in a yaml comment field, 12083 and 12405),
  7-277 (`datum == "unverified"`), 7-305 to 7-309 (`tools/build_charts.py`), 7-432
  (`tools/check_signals.py`), 7-436 (`tools/check_viewer_guns.py`), 7-560 to 7-565
  (`tools/audit_chart.py`), 7-448 (`tools/browser_probe.py` in Chromium).
- **Global side effects.** `sys.path.insert(0, tools)` with no removal (14228, 15088);
  `sys.modules["build_charts"] = tool` (12422) and `sys.modules.setdefault("audit_chart", ...)`
  (16210); `tempfile.mkdtemp()` never cleaned in 7-390, 7-391, 7-392 (13707 to 13709, 13727,
  13789 to 13793) where `tmp_path` is used elsewhere; mid-file imports `import yaml` (10828),
  `from freesail.api import queries` (14208), and `import yaml` again inside a loop (11478).
- **The conftest's rule is false.** Its docstring says the slow mark "is applied here and never
  in a test file" (conftest line 6); this half carries 16 hand marks, and the twin files more.
- **Failure messages.** Most pins carry the measured value (`, when`, `, gaps`), which helps.
  The wrappers fail inside another file's test with that test's message, so a red truth names
  a truth number whose own text gives no clue which of up to seven calls broke (7-395 calls
  seven).
- **Docstrings are histories.** Many carry the numbers of earlier packages ("2760, 2866, 3000
  and 6420 before", 9035; "5280 before package 84's step 6", 9036), digests "recorded, not
  pinned" (9409 to 9418 and five more). A reader cannot tell the truth from its record.
- **Not looked at.** The twins' own bodies (I read the conftest's lists and grepped their
  marks, not the 31 files), and the code under test beyond the lines cited.

## Faults to plant

Claims under (b):

1. `tests/test_known_truths.py::test_truth_7_183_the_first_action_replayed_with_the_arms_the_pumps_and_the_carpenter`.
   Fault: in `freesail/world/captains.py` line 4444 change `float(h.get("z_m", 1.0)) < 0.3` to
   `float(h.get("z_m", 1.0)) < -99.0` (the rules captain never sends the carpenter to a hole).
   The name says the privateer's carpenter plugs her holes. Prediction: passes although the
   game is broken (the check is under `if under:`, line 10583).
2. `tests/test_known_truths.py::test_truth_7_176_a_broadsides_casualties_are_men_of_the_muster_named_and_the_bill_counts`.
   Fault: in `freesail/combat/hits.py` delete the call on line 197
   (`_casualties(ship, keeper, MEN_HURT_HULL * scale * grape, x_m, "hull", rng, tick)`): a shot
   through the hull hurts nobody. The name says a broadside's casualties are men of the muster.
   Prediction: passes although broken (the test calls `_casualties` itself).
3. `tests/test_known_truths.py::test_truth_7_179_a_volley_within_musket_shot_fells_the_near_decks_men_and_the_quarterdecks`.
   Fault: in `freesail/combat/small_arms.py` line 62 change `QUARTERDECK_SHARE = 0.4` to `0.15`.
   The docstring says the quarterdeck takes two balls in five. Prediction: passes although
   broken (the forced draw 0.1 is still under 0.15).
4. `tests/test_known_truths.py::test_truth_7_147_a_signal_made_in_fog_is_a_gun_and_not_a_flag`.
   Fault: in `freesail/world/signalling.py` line 895 change the condition to `if False:` (a ship
   in fog never keeps her fog signals of herself). The name and docstring say a bell at anchor
   is heard within the mile. Prediction: passes although broken (the test sets
   `fog_signals = True` itself, line 10852).
5. `tests/test_known_truths.py::test_truth_7_512_a_ship_sails_from_port_mahon_to_carloforte_and_from_algiers_to_tunis`.
   Fault: in `freesail/world/ships.py` make `land_crossing` (line 1682) return `""` at its first
   line. The name says a ship sails these passages. Prediction: 7-512 passes although far ships
   may now route across land (it sails no ship); 7-545 in the same file should fail.
6. `tests/test_known_truths.py::test_truth_7_284_the_blend_adds_a_membership_and_not_a_gauge`
   and `::test_truth_7_441_the_frame_holds_every_state_and_the_view_writes_nothing`. No code
   fault: run them under `-n 4` beside the slow tier. Prediction: fail intermittently with the
   game unchanged (wall-clock ratios in the fast tier).

Faults I believe no test in this half would catch, though a player would:

1. `freesail/world/signals.py` lines 1416 to 1418: make a far ship's light order always set
   `"none"`. A convoy told to show its lights stays dark; 7-150 sets the lantern by hand and
   never orders it. (Confidence: sure for this half, a suspicion for the whole suite.)
2. `freesail/combat/hits.py` line 197 as in fault 2 above: hull hits hurt nobody in every
   action. No truth in this half fires guns and counts hull casualties (7-176 bypasses; 7-183
   accepts "killed" or "wounded" from deck hits). (Sure for this half; test_fight.py unread.)
3. `freesail/world/captains.py` line 4444 as in fault 1: no rules captain ever plugs a shot hole
   under water; only the player's order is tested (7-173). (Sure for this half.)
