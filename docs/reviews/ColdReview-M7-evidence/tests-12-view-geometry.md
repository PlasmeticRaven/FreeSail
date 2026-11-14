# Tests reader 12: tests/test_view_geometry.py

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Read whole, lines 1 to 7056. Code consulted
where a test needed judging: `client/projection.js` (in part: constants 44-203, sheet and belly
helpers 253-300, yard hoist 855-880, studding sail booms 940-975, `quadSail` 1231-1245, braces
1757-1800, studding sails 1712-1745, `taffrail` 2150-2160, `sortFigures` 3754-3810, exports
4710-4764), `client/shipview.js` (line 93), `freesail/api/queries.py` 560-582,
`freesail/ship/form.py` 870-900, `freesail/agents/pictures.py` 1-40, `freesail/api/viewer_guns.py`
1-40, `tools/ships/spritsail_yards.py` 25-185, `tools/python_twin.py` (whole),
`.github/workflows/*.yml` (grep), `tests/conftest.py` 1-30, `tests/test_indefatigable.py`
2850-2866. Commands run: `pytest --collect-only` on this file (collection only, no test run),
a Node start-up timing, a few seconds of Python to list which files serve a profile.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| tests/test_view_geometry.py | 7,056 | 139 (1,045): 108 parametrised into 1,014 cases, 31 single | none module- or session-scoped; 153 `run_js` calls, each a fresh Node process (about 65 ms to start, measured) on a ship built from YAML; 7 `make_world`, 6 of them a FastAPI `TestClient` | proves a great deal of real geometry, but out of proportion: about 175 numbers pinned to what the code gave, a block of tests that demand recorded defects persist, roughly 120 cases on branches no served graph reaches, and five copy-pasted "frame holds" tests |

## 1. Count and kind

- 139 test functions, 1,045 collected cases. The largest families: the boom sail's sheet (54
  cases, line 4626), lines on the rail (36, line 6118), the closed hull (31, line 1687), and about
  forty tests parametrised over the thirteen profiled files (`PROFILED`, line 171) or over
  `DRAWN_BY` (15 cases, line 1085).
- No module or session fixture. Every case builds its ship from the YAML afresh
  (`make_ship`), turns it into graph and snapshot (`ship_state`, line 197) and runs a JavaScript
  body in Node against `client/projection.js` (`run_js`, line 176). Six tests start the game's
  HTTP server in-process (`TestClient`, lines 3213, 3867, 5404, 5462, 6531, 6998) and two of
  them sail the engine through an evolution (`shifted_for_the_driver_and_back`, line 5243, up
  to 3,000 steps twice; the settee's tack, line 7013, up to 1,800 ticks). Run time not measured
  (the suite was not to be run); at least 1,045 Node start-ups.
- 137 of the 139 tests carry `@needs_node`; without Node they skip silently. Node is on this
  machine (v22) and on GitHub's runners, so in CI they run.
- What it proves: that the browser's ship view (`client/projection.js`, 4,764 lines, pure
  functions) draws each committed ship's hull from the stations the server serves, places every
  spar, sail and line where its file and the snapshot put them (set, furled, reefed, braced,
  sheeted, goose-winged, struck, sent down, on either tack, heeled), keeps a fixed scale across
  states, and paints in a sane far-to-near order.

## What the file is for in the game, and whether 7,000 lines are in proportion

The thing tested is the picture of the ship: the view a player watches to see what sail is set,
how the yards are braced, which side a sail lies on, whether a topmast is struck. A player who
lost it would lose the one visual confirmation of orders in a text-first game; the same picture is
posted to the language-model officers on request (`freesail/agents/pictures.py:1-12`). Nothing
in the simulation reads it: the code says so of its own rules (`BOOM_STEEVE`,
`test_view_geometry.py:3919-3921`: "a drawing rule: no file moves and the physics reads none of
it"). So a fault here misleads the eye; it cannot change a result, a log line or a save.

Proportion: the test file is one and a half times the code it tests (7,056 against 4,764 lines)
and is probably the largest single test file of a presentation layer in the suite. Of its 7,056
lines about 915 are docstrings, 349 comment lines, 1,045 embedded JavaScript, 581 blank, leaving
roughly 4,150 of Python (counted with `ast`/`tokenize`). The docstrings are largely history: 28
"old beside new" passages and 40 "measured" notes that record what an earlier drawing did (for
example lines 2197-2201, 5599-5601, 5624-5628, 5777-5781). That history is not asserted and is
the project's diary kept in the test file. My judgement: the geometry is fiddly enough to need
tests, and many here are good (below), but the bulk comes from running each of about forty hull
checks over thirteen files, pinning per-file measurements, and keeping branches alive for graphs
the game never serves. A third to a half could go without losing a real guard. Weight medium,
confidence likely.

## Python geometry that the browser repeats

The file tests JavaScript, not Python: every drawing assertion is on what `projection.js`
returns in Node. But the picture is computed partly in each language, and the file is the only
place where they meet.

1. **The hull's stations: Python computes, JavaScript draws, and also recomputes.**
   `freesail/ship/form.py` builds the drawn stations, served in every graph with a profile
   (`freesail/api/queries.py:577-580`). The JavaScript has its own second derivation of the hull
   from the profile alone, `profileHull` (`projection.js:2206`), used when no stations are served,
   and its own `formHull` with an `hbAt` for heights between stations. `form.py` in turn copies the
   viewer's rule for a round counter (`form.py:880-883`, `_counter_side`: "as the viewer draws it
   (client/projection.js, `formHull`'s `hbAt`)"). Agreement is checked in places: deck strips
   against `form.half_breadth_at` within 5 mm, but only on the regular stations
   (`test_view_geometry.py:1239-1245`; at the ends only "within the beam"); lights and galleries
   within 1 cm (1990-1991, 2067-2077); strip corners on served points within 1 mm (1828-1871);
   mast feet against `profile.deck_at` within 1 mm (1279); `profileHull` against the served
   stations for a stem tack within 1 mm on three files (6445-6455). The band tests check the bands
   against the JavaScript's own `H.hbAt` (2604, 2659), so JavaScript against itself. Confidence
   sure.
2. **The sprit topsail's cut** is computed in JavaScript (`squareCut`) and copied in Python
   (`tools/ships/spritsail_yards.py:162-171`, `drawn_by_slant`, used by the 64's and the 74's
   generators). The only check that they agree is that both are pinned to 9.30 m in two files
   (`test_view_geometry.py:3558`, `tests/test_indefatigable.py:2859`). One point, by coincidence
   of pins. Weight low, confidence sure.
3. **The settee's sheet block** is computed by the trim (Python, `sheet_geometry`) and by the
   drawing, and they are known to differ by 0.33 m; the test allows 0.5 m
   (`BLOCK_FROM_THE_TRIMS_M`, 6562-6565, asserted at 6863). Weight low, confidence sure.
4. **The guns and ports** are placed in Python (`freesail/api/viewer_guns.py`) and drawn in
   JavaScript, which repeats a deck-slope rule (`viewer_guns.py:349`). This file does not test
   them at all (`portFigures`, `gunFigures`, `flagFigures`, `effects` are not called here).
5. **Inside the test** about a dozen JavaScript rules are transcribed into Python and the
   JavaScript is then compared with the transcription: `todays_lens` (1108, compared at 1e-9 at
   1417), `head_chain` (3360, compared at 1e-12 at 3856 and 1e-9 at 3795), `rail_tops` and
   `rail_end` (2865-2880), `taffrail_of` (2852), `boom_end` (3930), `settee_block` (6649),
   `_mast_line` (2927), `_main_mast_x` (6620), `served_deck_at` (6640), `drawn_floor` (1807),
   `lead_x` (6074). Such a comparison proves the JavaScript equals what its author wrote twice; a
   wrong rule passes. Weight medium, confidence sure.
6. Several JavaScript constants are copied into the test by hand although `P.constants`
   exports them: `CLEW_SPREAD`, `HEAD_SPREAD` (3274-3276), `LUG_LEE_OF_BEAM`,
   `YARD_BEFORE_OF_BEAM` (6559-6560), `UNDERWATER_HEEL` (1804); others are copied because they
   are not exported (`FOOT_SAG`, `GEAR_DEPTH`, `BOOM_STEEVE_DEG`, `DERRICK_ALONG`,
   `JIB_TACK_FRACTION`). Low.
7. `tools/python_twin.py` does not bear on this: it is a demonstration that a standing order in
   the dialect and its twin in the Python API give one log (its docstring and body, lines 1-78).
   Nothing in it is geometry. `freesail/agents/pictures.py:4-8` records the decision not to have a
   second renderer in Python, which is sound.

## 2. (a) Tests of what is no longer there or no longer matters

- **The boats are left out of the hull tests though they now carry profiles.** Every boat file
  serves `profile` and `stations` (checked: `queries.ship_graph` on all 18 files). But
  `PROFILED` excludes them (line 171, "every ship carries a profile since the hull step"), so
  the five boats miss about forty `PROFILED`/`DRAWN_BY` hull tests (strips on stations, decks,
  below the drawn depth, mast feet, bowsprit, bands). The comment at 167-169 ("her drawing is
  that package's last step") is stale, and the branch at 1701-1703 (`if "profile" not in hull:
  assert path in BOATS ... return`) can no longer be reached. Weight medium, confidence sure.
- **Branches no served graph reaches, kept under test on in-test documents.** The lens for a hull
  with no profile (`WITHOUT_PROFILE`, line 1383: every profiled file with its profile popped)
  feeds `test_a_graph_with_no_profile_is_drawn_as_before_point_for_point` (13 cases),
  `..._draws_its_lens_with_no_nan` (13), `test_without_a_profile_the_bowsprit...` (13),
  `test_with_no_profile_the_lines_come_down_as_before` (26), `..._keeps_its_middles_depth` (13 of
  18), plus inline "old" runs (4594-4619, 4651-4658). The schema still allows a hull without a
  profile, so the branch is reachable by a new file, but each of the thirteen cases tests the same
  lens worked from three numbers (length, beam, deck height); one or two would do. The
  "profile without stations" builder (`DRAWN_BY`'s `"profile"` rows, line 1085; 1688's
  `"profile"` cases; 6419, 6445) runs `profileHull`, which the server never takes, since every
  graph with a profile carries stations (`queries.py:579-580`). About 40 cases. Weight medium,
  confidence sure.
- **History asserted as if it were behaviour.** Several "old" figures compute what a superseded
  rule would have given and pin it: `BOWSPRIT_DRAWN`'s first column, the distance of the drawn
  bowsprit's end from the B5.1 rule (1304-1318, asserted 1364-1368); `BOOM_CLEAR_LEVEL_M`, the
  clearance of a level line that is no longer drawn on any profiled hull (4674-4685, asserted
  4749-4754); `BOOM_OVER_TAFFRAIL_M`'s first column (4947-4959, 5028), which is the file's jaws
  height less the taffrail, a file number, not the drawing; `LEVEL_ROOT_M`'s middle column
  (1327-1331, 6281). These do not test the game. Weight low, confidence sure.
- `test_the_sets_of_files_with_no_part_name_files_that_exist` (1717) tests the test's own
  tables. `test_the_cutters_square_sail_is_its_files_twenty_seven_feet_deep` (780) asserts that
  the string "27 ft deep" is in the YAML (791): a test of a comment. Low.
- `test_a_wreck_cleared_away_is_not_drawn` (655) calls `run_js` but has no `@needs_node`;
  without Node it fails with a `None` executable rather than skipping. Two lines up,
  `test_the_cutter_is_drawn_from_her_file` carries `@needs_node` twice (585-586). Low, sure.

## 3. (b) Tests built not to fail

**Pinned numbers.** About 156 numbers in tables plus about 20 inline, nearly all marked
"measured at her landing" or "measured at her step 4", with tolerances of 1 mm to 2 cm:
`BOWSPRIT_DRAWN` 26 (1304), `LEVEL_ROOT_M` 9 (1327), `CHORD_OFF_THE_SIDE_M` 13 (2577),
`LIGHTS_SEEN_ABEAM` 1 (2460), `FRAME_STILL_MOVES_M` 1, `RINGTAIL_PAST_THE_FRAME_M` 2,
`FRAME_MOVED_OLD_M` 9 (4472-4489), `SHEET_END_X_M` 18 (4493), `BOOM_CLEAR_LEVEL_M` and
`BOOM_CLEAR_M` 40 (4674-4697), `BOOM_OVER_TAFFRAIL_M` 22 (4947), `STORM_MIZZEN_CLEAR_M` 3 (5038),
`STEM_TACK_Z_M` 10 (5866), `TACK_OFF_HER_SIDE_M` 1 (5993), `DRIVER_CLEW_RISE_M` (3927); inline
5.27/5.26 (1283-1284), 3.97 and 9.30 (3553, 3558), -28.35/8.53/-2.97/5.25 (4442-4445), 1.14
(4757), 7.16 (4803), 0.94/0.02 (4919-4920), 195.6 m2 (4929), 40 degrees (4932), 0.02 (4124).
Some have a checkable source (the 27 ft at 789, the lug's two-thirds at 914, Steel's 9 yards at
3553); most do not, and say only that this is what the code drew on the day. They are change
detectors: any rule change fails them, and the builder re-measures and re-pins. Set-valued tables
of the same kind: `LINES_ON_THE_RAIL` (5887-5967), `STEM_TACKED` (5970), `TIERS_IN_THE_SIDE`
(2532), `RIGHTLY_WITHOUT` (1639, at least read from sources and cross-checked against the file's
keys at 1711, which is good). Weight medium, confidence sure.

**Tests that demand a recorded defect stay.** These turn a known fault into an assertion, so
mending it fails the test:
- `test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail[frigate-36]` asserts
  `over < 0.0` (5030-5031): the frigate's boom must pass under her taffrail. The same defect is
  pinned in `BOOM_CLEAR_M[FRIGATE] = (0.26, -1.35)` (4689) and
  `BOOM_CLEAR_LEVEL_M[FRIGATE] = (-0.10, -1.83)`, so
  `test_her_booms_and_her_courses_foot_stand_clear_of_her_drawn_decks[frigate]` passes a boom
  1.35 m through her stern under a name that says "stand clear". Weight medium, sure.
- `test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number` asserts for the lugger
  and the five boats that figures DO stand over the frame (`OVER_THE_FRAME`, 6494; `assert
  got["over"]`, 6520-6521), by up to 2.11 m. Weight low, sure.
- `TACK_OFF_HER_SIDE_M` (5993, asserted 6244-6245): the *Neufchatel*'s head sail's tack must stand
  0.202 m off her side, in the air. Low, sure.
- Tolerances widened to fit one file: `FRAME_STILL_MOVES_M` (4472, used 4583),
  `RINGTAIL_PAST_THE_FRAME_M` (4475), the lugger's mizen foot exempted (2340-2345),
  `STORM_MIZZEN_CLEAR_M[FRIGATE] = 0.04` against a measured 0.041 (5038).

**An expectation built from the code under test.** `test_the_head_lies_on_head_m` (2097) reads
`P.constants.FIGURE_SHARE` from the module (2128) and builds the figure's expected size from it
(2145-2149). Only `HEAD_SIDING_M` is pinned (2135); nothing in the suite pins `FIGURE_SHARE`
(grep). A figurehead three times the size passes. Weight low, confidence sure.

**A loose classification.** `where_it_ends` (6049) counts any brace whose end has |y| = 0.3 as
"on a mast" (6066-6067), with no check of x or height, and any end equal to any yard's arm as "up
in the rig" (6068-6070). So `test_each_line_that_comes_down_ends_on_her_drawn_rail` (6118),
whose docstring says "none ends in the air", would pass a brace led to the wrong place on the
centreline. The only exact check of a brace's end is for the yards under the bowsprit (3669).
Weight medium, confidence likely.

**Weak or one-sided bands.**
- `test_steels_staysails_are_drawn_from_their_cut` (1045): for the four-sided mizzen staysail it
  asserts only that something is drawn (1068); the four-sidedness is asserted of the graph
  (1050-1052), not of the drawing.
- `test_a_yard_is_drawn_at_its_hoist` (796): the reefed yard need only lie between the cap and
  half a metre under its height (827); the reef's depth is not checked.
- `test_every_other_gaff_sail_keeps_the_foot_and_the_bundle_it_was_drawn_with` (4824): bands 0.4
  to 1.0 m and 0.2 to 0.4 m (4839) against measured 0.50-0.87 and 0.26-0.33.
- `test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states` (2357): its
  "outside" test checks minX, maxX and minY, not maxY (2383-2384).
- `test_the_lines_come_down_on_the_rail_as_the_game_serves_her` (6528): only a non-empty subset
  (6546-6547).

No `xfail`, no `skip` other than `needs_node` and `importorskip("fastapi")`, no swallowing
`try/except` (the one at the `UNDER_THE_WATER` body, 2413-2418, is the test of a refusal and
asserts its message at 2434). Empty loops are guarded (`assert got`, `assert seen > 0`, `assert
longer > 0`) throughout; that is done well.

## 4. (c) Tests that might be one

- Five "the frame holds X across states" tests share one JavaScript body of about 25 lines,
  copy-pasted: the mizen yard (3048), the yards under the bowsprit (3728), her boom (4529), the
  driver's boom (5174), the settee (6919). With `test_the_scale_is_the_full_rigs...` (320),
  `test_a_yard_is_drawn_at_its_hoist`'s bounds (830), the head and galleries' frame (2357), the
  bands' extent (2740), the shift and back (5382) and the frame unmoved (6499), eleven tests prove
  "the view does not rescale". One table-driven test over (rig, states, ids) would do.
- The polygon `winding` function is written twice in JavaScript strings (1428, 2215).
- Each "through the game's own doors" test (3207, 3861, 5396, 5454, 6528, 6990) repeats in
  substance a direct test beside it; they are worth keeping as integration checks, but they are
  the slowest cases and six of them is many.
- `WITHOUT_PROFILE`'s thirteen copies of one lens (above): one case per distinct hull shape at
  most.
- The two driver-shift tests (5292, 5382) run the same engine shift twice
  (`shifted_for_the_driver_and_back`), once each; one call could feed both.

## 5. Anything else

- Good tests that prove something hard: `test_ahead_and_astern_no_station_is_hollow...` (1522)
  samples over a thousand points of each section against the drawn polygons; `test_the_rig_keeps_
  its_order_but_against_a_face_seen_from_inside` (5657) sweeps 24 facings by 5 heels and checks
  the painter's order exactly; `test_every_file_draws_a_closed_hull_with_no_nan` (1687) checks the
  outline is one closed loop with every vertex met twice; `test_the_yard_stays_on_the_courses_line_
  as_the_mizen_is_shifted...` (5292) drives the engine's own evolution and draws every state.
- Failure messages are mostly a tuple of ids and coordinates; a builder can find the figure but
  not the rule. The frame tests' message is `(name, k)` with no numbers (3091-3092).
- The docstrings carry the project's argument (rulings, owners' words, measurements of past
  drawings). A reader cannot tell from them which sentence is asserted. Low.

## Faults to plant

Claims under (b):

1. `tests/test_view_geometry.py::test_each_line_that_comes_down_ends_on_her_drawn_rail`. In
   `client/projection.js` line 1789 change
   `var to = m ? v(m.x, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1)) : ...` to
   `var to = m ? v(m.x - 6, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1) - 4) : ...` (every
   brace led to the mast abaft ends 6 m abaft and 4 m below that mast, in the air). The name and
   docstring say no line ends in the air. Prediction: passes although the braces are broken
   (likely; the frame test might catch it on a short ship if the end leaves the frame).
2. `tests/test_view_geometry.py::test_the_head_lies_on_head_m`. In `client/projection.js` line
   182 change `var FIGURE_SHARE = 0.3;` to `var FIGURE_SHARE = 0.9;`. It should catch a figure on
   the head of the wrong size. Prediction: passes (sure for this test; likely for the whole file).
3. `tests/test_view_geometry.py::test_her_booms_and_her_courses_foot_stand_clear_of_her_drawn_decks[data/ships/frigate-36.yaml]`
   and `::test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail[data/ships/frigate-36.yaml]`.
   Not a fault but a mend: in `data/ships/frigate-36.yaml` raise `mizzen.boom`'s `height_m` from
   2.4 to 4.5 so that her boom clears her taffrail. The names say the boom stands clear.
   Prediction: both fail on the mend (they pin the defect), and the first passed the defect.

Faults I believe no test in this file would catch, though a player would see them:

1. A set studding sail drawn inboard across its topsail: `client/projection.js` line 1733
   (`cornersS = [headA, add(headA, mul(boom.arm || [0, 1, 0], ss2 * Lb)), boom.b, boom.a];`),
   change `ss2 * Lb` to `-ss2 * Lb`. No test here sets a studding sail other than the ringtail.
   Confidence likely.
2. Every sail bellying into the wind: `client/projection.js` line 271, change
   `return mul(n, s > 0 ? 1 : -1);` to `return mul(n, s > 0 ? -1 : 1);`. No test here checks the
   direction of a belly. Confidence a suspicion (a frame or depth-order test might move).
3. A sail taken aback no longer shown as aback: `client/shipview.js` line 93, delete
   `(f.backed ? " backed" : "")`. Only one test here renders `shipview.js` (5812), and it reads
   the hover titles of the head alone. Confidence likely for this file; other files not read.

## What I did not read

The rest of `client/projection.js` (I read the parts named at the head, perhaps a fifth of it),
`client/shipview.js` beyond line 93, `tests/rig_fixtures.py` (imported constants taken as named),
`freesail/ship/form.py` beyond 870-900, and the other test files that touch the viewer
(`tests/test_server.py`, `tests/test_flag_drawings.py`, `tests/test_map_view.py`). I did not run
any test, so run time and the predictions above are unmeasured.
