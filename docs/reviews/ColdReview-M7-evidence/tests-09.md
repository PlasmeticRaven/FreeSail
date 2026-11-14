# Tests, reader 09: pictures to reckoning

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Every file below was read whole, with
`tests/conftest.py` first. Nothing was run but a few seconds of Python to count parametrised
cases and to evaluate one branch condition (stated where used). Code under test was read where a
judgement needed it (named in each finding). Not opened: anything under `docs/dev`,
`docs/design`, `docs/playtests`, `docs/gates`, the sealed notes; so the documents that
`test_practice.py` and `test_ports.py` read from those trees were not checked by me.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_pictures.py | 416 | 2 (2) | module: a scenario world run 600 s and served by uvicorn; module: headless Chromium | sound in intent; threshold lowered to pass; skips silently off the build machine |
| test_pivot_gun.py | 217 | 9 (9) | none (a ship loaded per test) | sound; drives the trainer by hand, never through the battery's tick |
| test_places.py | 292 | 6 (6) | none | sound; stale comments; some lines compared to the code's own output |
| test_ports.py | 2401 | 53 (57) | none module-scoped; many tests sail 1 to 8 hours | proves much; one vacuous `all()`; census pins; the pilot's passage sailed again and again |
| test_powder_orders.py | 504 | 10 (10) | none | words well proved; the quantities proved against a stale fake magazine |
| test_practice.py | 627 | 21 (25) | none | fakes stand in for a battery and a fit that now exist; one test of documents |
| test_practice_lookout.py | 209 | 7 (7) | none | sound |
| test_practice_orders.py | 908 | 29 (49) | none | sound in the main; one test of a monkeypatched `begin_exercise`; duplicates test_practice |
| test_primer.py | 603 | 11 (1095) | none (BLOCKS, FORMS built at import) | tests a document; two chapters' blocks never run; a swallowing `except` |
| test_prize_court.py | 400 | 8 (8) | none | sound; one `@pytest.mark.slow` against conftest's rule |
| test_prize_scenarios.py | 227 | 5 (5) | none | one `assert x or True`; two slow marks by hand |
| test_prizes.py | 470 | 8 (8) | none | sound; stale band in the rising; seed-picked outcomes |
| test_profile.py | 965 | 36 (103) | module `profile` (cheap), module `gen` (imports the generator) | tests the generator and stage-0 hooks; source-grep pin; duplicates test_profiles |
| test_profiles.py | 1099 | 24 (44) | module `gen` (again) | tests the generator and the drawn hulls; runs the whole generator a second time; reports where it should bound |
| test_python_api.py | 405 | 10 (10) | none | sound twins; one dead assertion |
| test_readings.py | 797 | 23 (26) | parametrised function fixture `world` (1200 s sailed per case) | sound; some tautology by design |
| test_reckoning.py | 2765 | 74 (74) | none | strong numerically; a dead branch, a one-case parametrise, one vacuous membership |

## conftest.py (read for the tiers; three things a reader of my files must know)

- The docstring (conftest.py:6) says the `slow` mark "is applied here and never in a test file".
  Six tests in my files carry `@pytest.mark.slow` by hand: test_prize_court.py:349,
  test_prize_scenarios.py:142 and 182, test_prizes.py:302, 336 and 368. The rule and the
  practice differ; the tier of those six is decided in two places. Weight low, sure.
- The slow tier is kept by node id (`SLOW_TESTS`, conftest.py:103-567). I checked every name it
  lists for test_ports, test_python_api, test_readings and test_reckoning: all exist today. But
  nothing checks this automatically; a rename silently moves a multi-minute test into the fast
  tier. Weight low, sure.
- conftest.py:715 rebuilds `set(others)` once per item (`i not in set(others)`): quadratic in
  the suite's size when sharded. Weight low, sure.

## test_pictures.py

1. **Count and kind.** 2 tests, no parametrise. Module fixtures: `game` (a scenario world, 600 s
   run, uvicorn on a thread) and `page` (headless Chromium on the game's page; the page draws the
   pictures, `freesail/ui/server.py:950-985`). Proves that the chart and the ship's view reach a
   model through the API door and the MCP bridge as PNGs of the stated size, not blank, and that a
   shelved picture leaves a stub that says what it was.
2. **(a)** Nothing dead.
3. **(b)**
   - The blank threshold was lowered to pass (test_pictures.py:57-62): `BLANK_STD` was 8.0, the
     chart's own deviation measured 7.9 to 8.03, so it was cut to 4.0. The comment is honest, but
     it means the drawn chart is a picture of very low contrast that sits at the old floor; the
     test now proves "not a flat frame", little more. Weight low, sure.
   - The whole file skips when the vendor SDK, Playwright, its browser or Pillow is missing
     (lines 35-39, 154-162). The whole-suite workflow installs Chromium only for
     `test_browser_probe.py` and says "the pictures' test ... stay the build machines'"
     (`.github/workflows/whole-suite.yml:80-101`). So in CI these two tests skip and nothing fails
     on the skip. The owner's own complaint (a white image) is guarded only on the build machine.
     Weight medium, sure.
   - In the MCP test (line 409-411) the size is decoded from the PNG and compared with itself in
     `must_be_a_picture`; the only check of the tool's stated size is the words check at line 410.
     Not vacuous, but the size assertion in `must_be_a_picture` is a tautology there. Low, sure.
4. **(c)** None.
5. **Else.** The module-scoped `game` is not in `DAY_FIXTURES`; it costs a 600 s run plus a server
   start, and the browser fixture is a real browser: fine on the fast tier only because it skips
   on most machines.

## test_pivot_gun.py

1. 9 tests. No fixture of weight. Proves the privateer's pivot: no side, its arc from its file,
   training rate by hands, lee side when trained, the names it answers to, the load's refusals.
2. **(a)** None. The arc's history is kept as comments (lines 96-98, 180-183): old (60, 140) and
   new (62, 141).
3. **(b)** Every training test calls the private `Battery._train_pivots` directly (lines 112-132,
   139). The battery's own tick is the only caller (`freesail/combat/guns.py:504`); no test here
   proves that a pivot trains when the battery ticks. See Faults, "no test catches" 1. Weight
   medium, likely.
4. **(c)** The arc (62, 141) is asserted at lines 99-102 and 187, and again in
   test_profile.py:440 (and, by the comments, test_subtypes.py). The refusal of a pivot with a
   side is in test_pivot_gun.py:163-176 and test_profile.py:434-435. Fold into one place.
5. Good: the arc table at line 99 tests both edges on both sides.

## test_places.py

1. 6 tests. Proves the places as names, the hold, purse and stores as ledgers, the boats from the
   ship files, and the papers served by place to every station alike.
2. **(a)** Stale comments that contradict the assertion beside them: line 217-219 says "eleven
   since practice and resupply ... (10 before it)" and asserts 12; line 259 "10 before package 86"
   beside 12. Weight low, sure.
3. **(b)** Lines 167-170 compare each paper's lines to the very function that makes them
   (`sail_room(w.ship).inventory_lines()`, `booms(...)`, `cordage(...)`,
   `ground_tackle(...).describe()`): these prove wiring, never content; any content error in
   those functions passes. Weight low, sure. Line 58-66 pins the exact attribute set of a `Place`
   (`set(vars(p)) == {...}`): a structure pin, not a behaviour. Low, sure.
4. **(c)** None.
5. Good: test_the_papers_are_served_by_handle... (line 207) proves one refusal text at every
   station and at the pane: a real parity check.

## test_ports.py

1. 53 tests, 57 cases (`until` 2; dated-row refusals 4). No module fixtures; each test builds its
   own world. Seven are listed slow by node id. Many tests sail an hour or more (pilot passages,
   the Goulet from the wardroom save is eight hours, twice). Proves the ports as data, the market
   rules, the stance table, the pilot (hail, boarding, warnings, conn, fee), anchoring, mooring,
   kedging, the boat's errands, yard and crew pool, determinism and a checkpoint, the dated rows.
2. **(a)**
   - `WARDROOM_SAVE` (line 1971) is a file under `docs/playtests/`: a test of the game whose input
     is a record in the project's account of itself. I did not open it (forbidden). A test datum
     belongs under `tests/` or `data/`. Weight medium, sure (that it lives there).
   - The long comment at 1977-1988 records an xfail lifted; nothing dead remains.
3. **(b)**
   - test_the_pilot_of_brest_takes_her_through_the_goulet... (line 1656-1657):
     `assert all("the Mingan" in t and "leave it to starboard" in t for t in warned)`. The
     docstring promises "the Mingan named, left to starboard", but an empty `warned` passes. If
     the pilot never warns at all the test passes. Weight medium, sure (that it is vacuous when
     empty); whether it is empty today I did not run.
   - Lines 495-497: `f"{pilot.name}: on the quarterdeck" in ... or "pilot" in ...words("people")`:
     the second clause makes the first moot (any line with "pilot" passes). Lines 576-578 likewise
     (`startswith("no pilot aboard") or "no pilot" in`). Weight low, sure.
   - Census pins: `ALL_PORTS` (lines 98-239) and the dated-files list (2196-2217) must be edited at
     each package; the stance test (384-437) rebuilds the expected table from the same lists. They
     catch an accidental file loss, nothing about behaviour. Low, sure.
   - test_a_crewed_stranger... (line 2156): `[j.hull for j in w.ports.jobs] == [b.id] *
     len(crew.dealings.jobs)` passes when both are empty. Low, likely.
   - test_the_pilot_reckons... (line 2053): band 335 to 350 degrees for a computed figure; wide but
     the code's function is small. Low, likely.
4. **(c)**
   - The frigate standing in from `SOUTH_OF_FALMOUTH` under plain sail with the pilot to be
     hailed is sailed in at least eight tests (465, 942 twice, 1250, 1316, 1354, 1377, 1414), each
     one to two and a half hours. test_the_pilots_hails_are_notable_lines (1250) sails the same
     150 minutes as the first test only to check the hails' severity: fold into line 465's test.
   - Four "ports stand on the block's marks and on their own positions" tests (1738, 1783, 1876,
     1924) are one shape: whole chart against Channel chart, positions within 1e-4, the datum
     string, the stance. One table-driven test.
5. Good: test_the_market_moves_a_price... (333) and test_dated_rows_* (2293-2401) are exact and
   cheap. Line 2105 imports `put` from `tests.test_brains`: tests import tests (also
   test_practice*, test_prize*, test_powder_orders), so a change in one file's helper moves
   others.

## test_powder_orders.py

1. 10 tests. Proves the supply's words (powder, shot, both; necessity; guns by calibre; numbers
   read whole), the cut to what the magazine wants, the routing of `buy`/`demand`, and the galley.
2. **(a)** The docstring (lines 11-14) says the magazine is "the fake of tests/test_ordnance.py
   ... written before Builder 1's was merged". It is merged: `Magazine.wanting`,
   `account_lines`, `return_barrels`, `describe` all exist (`freesail/ship/parts.py:993-1060`),
   and `FakeMagazine(Magazine)` (`tests/test_ordnance.py:71-104`) still overrides them with its
   own copies ("until it is merged"). The fake's `wanting` is a near copy of the real one with
   the barrel's 100 lb written as literals. Weight high, sure.
3. **(b)** Consequently test_each_quantity_is_cut_to_what_the_magazine_wants_and_says_so (275),
   test_demand_a_barrel_is_one_barrel... (242) and the Sound half of
   test_a_number_with_and_in_it... (219-239) prove the orders against the fake's arithmetic, not
   the game's. A rounding fault in the real `wanting` passes all three (Faults 1). Weight high,
   sure that the fake is used; likely that they would pass.
4. **(c)** None in the file.
5. The galley tests (416-504) are good and exact.

## test_practice.py

1. 21 tests, 25 cases (notional mark at 5 bearings). Proves the cask and notional mark as
   targets, a hit on the cask, no recognition/outlaw/morale for a mark, the cask's drift and
   loss, the practice reading, the idle rows, the allowance for exercise.
2. **(a)**
   - The docstring (lines 10-13) says Builder 1's battery "was not merged" and fakes stand in.
     It is merged: `Battery.last_practice_tick` (`freesail/combat/guns.py:281`, set at 988),
     `Drill` (guns.py:256), `FitSpec.exercise_charges` (`freesail/ship/schema.py:858`). Yet
     `_with_allowance` (499-502) still writes the field onto a copied fit "stood in", and
     `ShortMagazine` (473-477) stands in for `wanting`. Weight medium, sure.
   - test_the_documents_say_what_practice_and_resupply_built (578-614) tests documents, not the
     game: it reads `docs/dev/TuningNotes.md`, `docs/TechnicalSpec-M7.md`,
     `docs/dev/M7-WorkPackages.md`, `docs/agents/Harness.md`, `docs/design/Design-Squadrons.md`,
     asserts sentences in them, asserts a sentence is absent from one, and pins the count of
     event words at 13 (line 610). A doc edit fails the game's suite. Weight medium, sure.
3. **(b)** test_a_mark_fired_on_is_no_sail... (177-217) replaces `Battery.tick` with a fake
   (line 206) that sets `last_practice_tick` itself and calls `resolve` itself. The claim
   "no recognition, no outlaw, no morale" is proved for the fake's firing, not the battery's
   (whose own path at guns.py:984-990 decides practice against firing). The notional-mark test
   that follows (220) uses the real battery but never strikes anything. Weight medium, sure.
4. **(c)** test_a_fresh_cask_gives_up_the_one_in_the_water_once (289) and
   test_practice_orders.py::test_a_fresh_heave_gives_up_the_cask_in_the_water (122) prove the
   same abandonment. The cask's sight is proved here (cask_in_sight) and in
   test_practice_lookout.py.
5. Good: test_the_cask_drifts... (244) recomputes the drift from stream and leeway and checks no
   stream is drawn.

## test_practice_lookout.py

1. 7 tests. Proves the cask as a sighting of its own kind: ranges by light and haze, never
   hailed, lost and regained once, its own stream, not a fix mark, found as "the mark", named
   first in `what is in sight`, a bearing of it moves no account.
2. **(a)** None.
3. **(b)** Line 157: `land["nearest"] is None or ...` passes when no land is near; low. Line 93:
   the regex band allows any of five cable words; deliberate (the eye's error). Low, sure.
4. **(c)** Overlaps test_practice.py on sight; small.
5. Sound. test_the_practice_stream_opens_only_with_a_cask_and_moves_no_other_draw (130) is a good
   determinism test.

## test_practice_orders.py

1. 29 tests, 49 cases (notional bearings 8, read-whole forms 11, standing refusals 4). Proves the
   practice orders' forms and refusals in words, the dumb show, the filling, the files, the
   scenario's round trip, a rules captain half an hour with a cask engaged.
2. **(a)** The docstring (12-15) again says "written before Builder 1's battery was merged";
   it is merged (`Battery.begin_exercise`, `freesail/combat/guns.py:371-396`).
3. **(b)** test_the_loaded_guns_keep_their_charges_in_the_answer (464-486) monkeypatches
   `Battery.begin_exercise` with a fake returning a given list of names, then asserts the order's
   text names that many loaded guns. The real `begin_exercise`'s list of loaded guns is never
   exercised here; if it returned `[]` always the test passes (Faults 2). Weight medium, sure.
   test_a_rules_captain_with_a_cask_engaged... (870-908) records in its docstring that at seed 7
   "no shot is fired at it": it asserts that practice under the rules captain does nothing, a
   finding pinned as a pass. Weight low, sure.
4. **(c)** Duplicates test_practice.py on the fresh cask (122) and the notional mark's bearing.
5. Good: test_in_dumb_show_from_empty_a_gun_fired_by_name_takes_a_cartridge_and_fires (624) runs
   the real battery and counts rounds and drills exactly.

## test_primer.py

1. 11 tests, 1095 cases at import (156 order blocks, 37 world-order forms, 894 table forms;
   counted by importing the module). Tests a document, `docs/primer/`, against the order parser.
   The evolution runner is replaced by `InstantRunner` (declared, 129-193).
2. **(a)**
   - The docstring says "Every fenced code block in the primer whose info string begins with
     `orders`". `CHAPTERS` (84-110) omits 13, 19 and 24, which hold 7, 3 and 4 `orders` blocks
     (`grep -c '^```orders'`). Only 13 is excused (lines 101-104). The 7 blocks of chapter 19
     and 24 are never run. Weight medium, sure.
   - The `orders-pending` machinery (35-38, 403-404) has no block to act on: 0 of 156 blocks are
     pending. Dead path. Low, sure.
3. **(b)**
   - test_every_form_in_the_forms_tables_is_taken (578-603): any `OrderError` that is not
     `UnknownVerbError`/`UnknownNounError` is swallowed unless its text contains "was understood,
     but not" or "takes nothing after it" (598-602). The parser also refuses wording in other
     words, as a plain `OrderError`: e.g. `"'{left}' was not understood after 'veer'"`
     (`freesail/orders/ground_tackle.py:254-258`, and 271, 277, 292, 349). A table form refused
     for its words with such a message passes. Docstring: "refused for the ship's state ... never
     for its words". Weight high, sure (Faults 3).
   - test_the_primer_shows_enough_orders (376-382) and test_the_forms_tables_are_there_and_large_enough
     (538-547) are count floors (`>= 25`, `>= 100`, `>= 90`, `>= 240`, `>= 260`). Low, sure.
4. **(c)** None.
5. This file tests a tool and a document, which is a fair thing to own, but the owner should know
   1095 of the suite's cases are documentation checks.

## test_prize_court.py

1. 8 tests (one marked slow by hand). Proves the eighths by date, the valuation, condemnation,
   restoration with costs, salvage, the reserved fourth, the director's doubted word, the far
   court.
2. **(a)** None.
3. **(b)** Line 89: `abs(fv["hull"] - fv["tons"] * 12.0 * 0.8) <= 12.0` re-derives the formula;
   `round(1944.0 * 0.1)` (247) pins the valuation. Low, sure. Lines 291-293:
   `"reserved..." in w.log[-1].text or any(...)`: fine. Line 212: the record's `court` popped by
   hand after `PC.sentence` was called directly, so the queue is tested on a record the court
   never wrote. Low, likely.
4. **(c)** `_taken_in_falmouth_road` (118-149) is a near copy of `tests/test_prizes.py::_struck_brig`.
5. Sound.

## test_prize_scenarios.py

1. 5 tests (two marked slow by hand, each a passage replayed by two roads). Proves the two
   scenarios begin as they say, no served line names the director, and two replays by both roads.
2. **(a)** None.
3. **(b)** Line 58: `assert any("Deux Frères" in row for row in truth.get("prisoners", [])) or
   rec["prisoners"]`. Line 51 has already asserted `rec["prisoners"] > 0`, so this is
   `assert x or True`. The director's truth's prisoners row is not tested here (Faults 4).
   Weight medium, sure.
4. **(c)** None.
5. The two replay tests (143, 183) are strong.

## test_prizes.py

1. 8 tests (three slow by hand). Proves possession, refusals, prisoners by the boat, burning, the
   rising (won and put down), the far cut-out and retaking, the checkpoint.
2. **(a)** Line 24: `ships = pytest.importorskip("freesail.world.ships")`. The module exists and
   is imported unguarded elsewhere; the guard can only hide an ImportError raised inside it by
   skipping the whole file. Low, sure.
3. **(b)**
   - test_the_prisoners_rise... (303-333): docstring "sixteen prisoners over a prize crew of
     eight", but line 324 asserts `pris.count <= 21`, the old figure from before the merchant
     brig's own file. Stale band. Low, sure.
   - The risings are seed-picked: `PUT_DOWN_SEED = 2` "the first seed from 1 whose rising is put
     down" (362); seed 1 "rise in the first hour". The tests pin the stream's draws; any change
     to stream use moves them, and the "odds rule holds" half (355-359) asserts only that the
     hour was judged and nothing rose, not that no draw was made. Low, likely.
4. **(c)** See prize_court.
5. Sound otherwise; the checkpoint test (450) compares the copy to the original, as it should.

## test_profile.py

1. 36 tests, 103 cases (35 schema refusals, 34 generator refusals). Module fixtures `profile`
   (cheap) and `gen` (the generator imported). Proves the profile's schema and helpers, the gun
   deck keys, `unarmed`, the pivot's arc, the generator's helpers, and "stage 0" hooks.
2. **(a)** Many tests are named for package 75's stage-0 hooks ("items 17 to 25") and say "as
   before" for pickles and forms. test_the_lee_ports_update_shuts_nothing_upright... (679)
   docstring: "where stage 0 had it wait behind its port", the body now asserts the opposite
   (dropped). Name and body still agree on "shuts nothing upright"; the history is in the
   docstring. Low, sure.
3. **(b)** test_the_lee_ports_events_are_registered_and_said_by_the_rule (733-737) greps the whole
   `freesail/` source for the text `"guns.ports_` and pins the two file names it appears in. A
   move of the string to a constant fails it; a third emitter in a file named `ports.py` elsewhere
   passes. A test of code layout. Low, sure.
4. **(c)** test_the_hook_runs_the_four_ships_modules_after_the_eight_each_writing_its_own (510)
   runs `tools/gen_ships.py` in a subprocess and compares every committed ship file byte for
   byte; test_profiles.py::test_truth_7_185 (1055) runs the generator again and does the same
   comparison; and test_profiles.py's docstring names a third, `tests/test_ship_particulars.py`.
   The `gen` fixture is defined identically in both files (test_profile.py:555, test_profiles.py:55).
   Weight medium, sure.
5. This file tests a tool (the generator) more than the game.

## test_profiles.py

1. 24 tests, 44 cases. Module `gen`. Proves the generator's form helpers, Steel's table reader,
   the dump format, and over the 13 hull files: rails above decks, marks, port gaps, displacement
   report, the pair check, truth 7-185.
2. **(a)** `FT` defined twice (52, 1026). Low.
3. **(b)**
   - test_the_drawn_displacement_and_depth_stand_beside_the_filed_ones (811-826): it prints the
     drawn displacements and asserts only the set of ships more than 15% off,
     `{"brig", "merchant-brig", "smack"}` (docstring: brigs at -27%, smack -18%). There is no
     bound on how far off those three may be: a brig drawn at -80% passes. Weight medium, sure.
   - test_each_port_triples_gap... (787-808) prints every gap and asserts only the measured
     triples; the rest are "reported" to stdout under `capsys.disabled()`. The reports are
     invisible in a normal run. Low, sure.
4. **(c)** See test_profile.py: the second whole-generator run (1065-1075).
5. Good: test_the_pair_check_fails_one_drawing_under_two_files_figures (993) is a test written
   from a found mutation. The pair check (1002) runs 78 pairs x 3 views of numpy Hausdorff; not
   in the slow list; I did not time it.

## test_python_api.py

1. 10 tests (five in the slow list). Proves the decorators enter rules identical to the dialect's,
   twin logs, the body runs once, refusals, the save and the absent Python rule.
2. **(a)** test_truth_40... lines 117-120:
   `assert [t for t, *_ in standing_lines(python)] and all((python.clock.start.replace(...)).__class__
   for _ in [0])`. The `all(...)` is over one element whose value is a class object, always true;
   the comment says "a tick each". The second half asserts nothing. Weight low, sure.
3. **(b)** test_a_python_rule_saves... line 375-376: `copy.run(600)` then `placeholders[0].fired
   == 1, "it did not run"`. The save is at 20:05 after the sunset it fired on; no sunset falls in
   the next 600 s, so a live placeholder would not have fired either. The check proves nothing
   about the placeholder being inert. Weight low, sure.
4. **(c)** The three twin tests (85, 126, 151) are one shape; a table would do.
5. Sound otherwise.

## test_readings.py

1. 23 tests, 26 cases (`world` fixture over 2 ships for 3 tests). Proves the registry's rows,
   absent sentences, readings equal the physics' numbers, the cache, snapshot parity, words, the
   mean wind, the nearest land, the reckoning reading, and that no reading leaks the true
   position.
2. **(a)** None.
3. **(b)** test_readings_are_the_physics_own_numbers (148-189) compares each reading with the
   attribute it reads (`r["speed"] == d.speed`): wiring by design, would pass with wrong physics.
   Line 575: `value["metres"] != shore.distance_m`, true for nearly any float. Line 481-482: the
   gust assertion runs only inside a condition; the later `seen` set saves it. Low, sure.
4. **(c)** None.
5. Good: test_no_reading_gives_the_true_position_by_any_road (724) is a strong, general proof
   across every registered row.

## test_reckoning.py

1. 74 tests, 74 cases (one parametrise of one case). Nine in the slow list. Proves the
   arithmetic of the reckoning, the doubts, the observation rule, the lead, bearings, fixes, the
   noon, the master's tide, shaped courses, the slate, and determinism.
2. **(a)**
   - `@pytest.mark.parametrize("casts", [True])` (2624): one case; the `if casts:` at 2641 is
     always taken. Vestige of a dropped `False` case. Low, sure.
   - test_the_cast_is_reduced_by_the_masters_own_tide_and_the_line_says_it, lines 2616-2621:
     "under a fathom the line says nothing of it" sits under `if low.navigation._tide_allowance_m()
     < units.fathoms_to_m(1.0)`. I evaluated it: the allowance there is 2.43 m against 1.83 m, so
     the branch is never taken and the claim is never checked (Faults 5). Weight medium, sure.
3. **(b)**
   - Line 401: `e.data["how"] in (K.TAKEN, K.WEIGHED, K.KEPT)`: those are the only three values
     (`freesail/world/reckoning.py:389`). Vacuous. Low, sure.
   - Line 283: `read > stw * 1.0`; line 326 an `or`; line 575 `account != truth`; line 651
     `assert lines is not None`. Weak. Low.
   - test_no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place (1799-1842)
     greps function sources for eight strings. It catches the obvious leak and nothing aliased
     (a local `t = self.world.tide` written as `world.tide` with no dot before it passes). The
     behavioural twin, test_the_masters_tide_is_his_own... (1751), is the real proof. Low, sure.
   - test_the_slate... (2312) and test_my_reckoning... (2387) assert under `if "Latitude by
     observation" in noon.text`; I did not check whether the branch is taken. Low, a suspicion.
4. **(c)** Many pins are by seed and say so ("2.7 miles against 5.4 at this seed", 2682; "1.2
   degrees at this seed since 37j", 698). Not duplicates, but each fails on any change of a
   stream's use.
5. The arithmetic tests (65-260, 1008-1198) are exact and cheap and prove hard things.
   test_over_the_geometry_of_game_9s_fixes_good_to_is_honest (1603) is a good statistical test.

## Faults to plant

Under (b): my strongest claims.

1. **tests/test_powder_orders.py::test_each_quantity_is_cut_to_what_the_magazine_wants_and_says_so.**
   In `freesail/ship/parts.py`, `Magazine.wanting`, line 1012, change
   `int((deficit + BARREL_LB / 2.0) // BARREL_LB)` to `int(deficit // BARREL_LB)` (barrels
   wanted rounded down: a magazine short by 99 lb asks for none). The name says each quantity is
   cut to what the magazine wants. Prediction: passes although the game is broken
   (`FakeMagazine.wanting` overrides the real one).
2. **tests/test_practice_orders.py::test_the_loaded_guns_keep_their_charges_in_the_answer.** In
   `freesail/combat/guns.py`, `Battery.begin_exercise`, lines 394-395, delete
   `if g.loaded: loaded.append(g.name)` (always return `[]`). The name says the loaded guns keep
   their charges in the answer. Prediction: passes although broken (the test monkeypatches
   `begin_exercise`).
3. **tests/test_primer.py::test_every_form_in_the_forms_tables_is_taken.** In
   `freesail/orders/ground_tackle.py` line 247, change `if left or (fathoms is None and said_to):`
   to `if True:` (every `veer` refused in words). Chapter 13's table lists `veer cable`,
   `veer away`, `veer twenty fathoms`, `veer to ninety fathoms`. The name says every form in the
   tables is taken. Prediction: passes although broken (the refusals are plain `OrderError`s whose
   text is neither phrase the test looks for; chapter 13's blocks are not run at all).
4. **tests/test_prize_scenarios.py::test_the_prize_home_scenario_begins_with_the_brig_a_prize_in_company_and_the_truth_shows_her.**
   In `freesail/api/readings.py` lines 4251-4252, delete `if prisoners: out["prisoners"] =
   prisoners`. The docstring says the director's truth shows her prisoners. Prediction: this test
   passes although broken; test_the_captive_scenario... in the same file fails (KeyError at line
   94), so the file as a whole catches it.
5. **tests/test_reckoning.py::test_the_cast_is_reduced_by_the_masters_own_tide_and_the_line_says_it.**
   In `freesail/world/reckoning.py` line 3093, change `if allowed_m >= units.fathoms_to_m(1.0):`
   to `if allowed_m >= 0.0:` (the reduction said on every cast). The docstring says it is said
   only when a fathom or more. Prediction: passes although broken (the under-a-fathom branch is
   never entered; other casts in the file only assert the words present).
6. **tests/test_ports.py::test_the_pilot_of_brest_takes_her_through_the_goulet_on_the_truth_from_his_station.**
   In `freesail/world/dealings.py` lines 1040-1045, delete the `self._record(Severity.URGENT,
   "port.pilot_warns", text, {...})` call for a named danger (keep the `return` after it). The
   docstring says the Mingan is named and left to starboard. Prediction: this test passes
   (`all()` over an empty list), unless a shoal warning (line 1058) happens to fire on the way in;
   test_the_pilot_warns_of_a_danger_ahead_by_name... fails, so the file catches it.

Faults I believe no test in my files would catch, though a player would:

1. `freesail/combat/guns.py` line 504: delete `self._train_pivots(dt, quarters, firer, target)` in
   `Battery.tick`. The privateer's long Tom never trains round in play and so never bears;
   test_pivot_gun.py drives `_train_pivots` by hand. (Likely.)
2. The rounding fault of Faults 1 in `Magazine.wanting`: in my files every magazine that wants
   anything is a fake (`FakeMagazine`, `ShortMagazine`); a player in port asking "take in powder"
   short by under a barrel would be told she wants none. (Likely; test_ordnance.py, not mine, may
   catch it.)
3. A wording fault in a primer chapter-19 or chapter-24 `orders` block, or in the parser for an
   order shown only there: those 7 blocks are never run (`CHAPTERS`, test_primer.py:84-110), so a
   player following the wardroom or squadron chapter would meet refusals no test sees. (Sure that
   the blocks are not run.)
