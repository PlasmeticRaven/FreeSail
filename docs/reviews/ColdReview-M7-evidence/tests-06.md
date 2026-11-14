# Tests, reader 06: the hulls, the Hull, Indefatigable, the in-world rule, the islands

Tree at 504a250. Read whole: `tests/conftest.py` and the thirteen files below. Read in part, to judge
a test: `freesail/physics/integrate.py` 519-533, `freesail/physics/hull.py` 158-197, the names in
`freesail/physics/sails.py`, `tests/test_profiles.py` 750-809 and 1055-1095. Not opened: anything
under `docs/` (the six hull files read six notes under `docs/design/ships-design/`; I checked only
that they exist, with `test -e`). Nothing run but `pytest --collect-only` on these files and three
short Python calls (below). No test was run.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_held_hulls.py | 120 | 3 (3) | none; each test sails 4 to 50 minutes of a world with brigs | sound; one test likely slow and unmarked |
| test_hull.py | 461 | 27 (32) | none | sound; one name promises a check the body does not make |
| test_hull_brig.py | 595 | 22 (50) | `report` (the generator's module exec'd in process) | proves the file, the note and the generator agree; little of the game; its git test always skips |
| test_hull_cutter.py | 472 | 18 (28) | `module` (exec of tools/ships/hull_cutter.py) | the same, with a 15% band where 0.5% is the fact |
| test_hull_form.py | 1427 | 28 (101) | none | sound, the best file of the list; a few pins of recorded errors |
| test_hull_frigate.py | 639 | 19 (19) | `probe` (a subprocess of the generator's module) | as brig; pins much |
| test_hull_lugger.py | 614 | 25 (33) | none | as brig; one test asserts only a design note's wording; one holds of nothing |
| test_hull_schooner.py | 536 | 17 (27) | none (one test runs the generator twice in a subprocess) | as brig; reads Build-Ships.md |
| test_hull_smack.py | 626 | 20 (20) | `built` and a cache of three subprocess runs of her module | as brig; three tests for "she has no port" |
| test_hulls.py | 407 | 11 (11) | none; five tests each build the same hove-to world and a brig | sound; the old-shape writer is a forge to keep in step |
| test_in_world.py | 296 | 9 (95) | two scenario worlds, built once each | sound; tests served documents, by design |
| test_indefatigable.py | 2959 | 53 (68) | two ship loads | proves much, but none of its ~12 sailed tests is in the slow tier; truths re-assert the particulars |
| test_islands.py | 292 | 9 (10) | the atlantic-east chart, loaded once | sound in the main; tests tools and data more than play |

The six `test_hull_<ship>.py` files hold 121 test functions in 3,482 lines; the section after them
says how far they are one test written six times.

The tier rule (conftest.py): a test is slow only if it reads a fixture named in `DAY_FIXTURES` or
its node id is in `SLOW_TESTS`. None of my files has an entry in `DAY_FIXTURES`. From my files
`SLOW_TESTS` holds two of `test_held_hulls.py` (conftest.py:521-522) and nothing else. A collect of
`test_indefatigable.py`, the six hull files, `test_hulls.py` and `test_islands.py` without `--slow`
gives "367 tests collected", none deselected.

---

## test_held_hulls.py

**Count and kind.** 3 tests, none parametrised, no fixtures. Each builds `hove_to_world()` from
`tests/test_crews.py` and sails: test 1 61 s plus 3 × 60 s with six brigs; test 2 up to 40 × 60 s
plus 600 s; test 3 40 × 60 s. It proves that a hull a model holds through a door ranks over the crew
cap up to `HELD_OVER_CAP`, and that a held far hull standing for the Wolf is put about by its plan
with one urgent line its captain's sample carries.

**(a)** None found. `K.model_held`, `K.crewed`, `plan.danger` are all read live.

**(b)**
- `test_a_far_hull_held_through_no_door_keeps_the_far_plan_as_it_was` (116-120) asserts only that no
  `plan.danger` line is written in 40 minutes. It does not look at the plan, the heading or where
  she ends: a far plan broken in any other way passes. Weight low, sure.
- `test_a_hull_a_model_holds...` (55) hard-codes the cap as three (`names[:3]`) rather than reading
  it from `crews`; a changed cap fails the test with no word of why. Low, sure.

**(c)** Truth 7-400 in `test_known_truths.py` (named in conftest.py:523) is the same scenario again.
Not read by me.

**Else.** `test_a_far_held_hull_standing_for_a_rock...` (99) sails up to 50 minutes and is not in
`SLOW_TESTS`, while its two neighbours are (conftest.py:521-522, "4 to 14 s alone"). Likely slow and
in the fast tier. Medium, likely (not timed: I may not run it).

---

## test_hull.py

**Count and kind.** 27 tests, 32 cases (four parametrised: sign ×2 twice, three headings across
north, two winds). Function-scoped ship loads only. With `compute_sail_forces` stubbed to fixed
forces it proves the hull's surge, sway, heel, rudder, helmsman, full-and-by and the notes (aback,
beam ends, leeway, helm steady).

**(a)**
- The module docstring (1-5): "Every test replaces `compute_sail_forces` ... nothing here depends
  on package 4." False for five: 91, 98, 407, 422 call helpers directly, and
  `test_all_four_ships_run_under_bare_poles` (451) uses the real sail physics and says so. Low, sure.
- `test_leeway_change_is_noted_at_most_once_a_minute` (380-394): the name and the comment at 388
  ("no two notes within a minute of each other") promise a check of the interval. The body never
  reads a note's time. It asserts at most 10 notes in 600 s and that each note's leeway differs by
  more than a degree from the last. The interval is enforced at `freesail/physics/integrate.py:527`
  (`st.seconds_since_leeway_note >= hp.LEEWAY_NOTE_INTERVAL`). If that clause is removed, the notes
  still come one per degree of change, and leeway settles at a few degrees (the band at 132 is 0.5°
  to 15°), so both assertions very likely hold. Medium, likely. Planted below.

**(b)**
- `test_all_four_ships_run_under_bare_poles` (451-461) asserts speed under 2 kn, finite state,
  apparent wind non-zero and `"hull" in ship.extra`. A ship with no windage at all stays at 0 kn and
  passes every line. The docstring's "the real sail physics gives only windage" is not tested. Low
  to medium, likely. Planted below.
- `test_sway_is_clamped_at_low_speed` (160) and both full-and-by tests (278, 297) compare against
  the module's own constants (`SWAY_CLAMP_SLOPE`, `FULL_AND_BY_DEFAULT_LUFF + MARGIN`). Fair for an
  invariant, but a wrong constant cannot be caught here. Low.

**(c)** `run(ship, 60)` under bare poles for "the four ships"; data/ships now has 18 files (8 sailing
ships besides these four and the boats). Not a merge, but the "four" is stale. Low.

**Else.** The helm and aback tests (215, 260, 314, 357) are good tests of hard behaviour: overshoot,
short way across north, once per episode with the minute's re-arm.

---

## test_hull_brig.py

**Count and kind.** 22 tests, 50 cases (`path` ×2 on 7 tests; `key` ×11 × `path` ×2 at 261 gives
22). Module fixtures `note` and `lines` (the Markdown note parsed) and `report` (exec of
`tools/gen_ships.py` in process, then `gen.hull_form`). It proves that the brig's and the merchant
brig's YAML profile, the pages note `pages-zaz4491.md` and the generator's report agree, point for
point, and that the guns stand on the triples.

**(a)**
- `test_no_figure_the_physics_or_the_gunnery_reads_moved` (575-595), 2 cases: `git show
  f5be9110:...`. In this checkout `git cat-file -e f5be9110^{commit}` fails ("Not a valid object
  name") and `git rev-parse --is-shallow-repository` gives `true`. Every workflow uses
  `actions/checkout@v4` with no `fetch-depth` (ci.yml:62, whole-suite.yml:44/68/92/122,
  release.yml:31), which fetches one commit. So the test skips everywhere it runs. Unlike the
  cutter, lugger, schooner, smack and frigate files, the brig file has no pinned copy of her hull
  figures, so nothing in this file holds her physics keys at all. High for the claim it makes, sure.
  It is also a test of a step of the build: it proves the step that drew her lines moved no physics
  figure, against the file before that step. Its `_without_sw4_words` (557-572) shows that every
  later legitimate edit has to be cut out of the comparison by hand.
- `NOTE_LINES` (246-258) maps each key to itself: an indirection with no use. Low.

**(b)**
- Pins of what the drawing gives today, with the note as the only reason: the drawn displacement
  303 t ±3 t and its sentence "303 t against the filed 413 t (-27%)" (445-446), "2.87 m deep"
  (448), K at 11.25 ft (449), the drag 12.80/9.69/3.11 ft (462-464), the ten gaps with exactly
  `[6.5]` over `PORT_GAP_M` (477), the chase port 0.43 m off (241), the exact pair of differing
  ports (123-126). Eight pins of `freesail/ship/form.py`'s output or the file's present figures. A
  change to the drawing rule fails them all with no word of which is right. Medium, sure.
- `test_each_sill_in_its_sources_band` (216): `lowest - 1.52 == approx(0.05, abs=0.01)` pins the
  sill *outside* Steel's band by 5 cm, a record of a departure, not a band. Low.
- `test_the_drawn_displacement...` and `test_her_drag...` `print` their figures (442, 466). Nobody
  sees the output without `-s`. Low.

**(c)** See the six-file section. Every-file versions of "each port gun on a triple", "a mark on
every line" and "the gaps reported" are in `test_profiles.py` (764, 787, 1055).

**Else.** `test_the_load_line_is_wl1_and_the_faint_line_is_recorded` (219-229),
`test_the_form_and_the_marks_against_the_note` (404) and
`test_her_notes_carry_sources_and_no_figure_a_rule_computes` (482-510) test documents: the
note's prose and the YAML comments. They are not tests of the game. Medium, sure.

---

## test_hull_cutter.py

**Count and kind.** 18 tests, 28 cases (`key` ×11 at 257). Module fixtures `ship`, `spec`, `doc`,
`module` (exec of `tools/ships/hull_cutter.py`), `six` (the note's §6) and `section_cells`. Cheap.
It proves the same as the brig file for the cutter.

**(a)** `test_a_diff_of_her_physics_keys_against_git_shows_none` (423-472) skips (no f5be9110).
`HULL_AS_FILED` (399-418) stands in for the hull keys and the main mast's x and rake only. The
spars' ratings, the sails, the lines and the guns are not pinned anywhere in the file. High, sure.

**(b)**
- `test_the_drawn_hull_is_reported_beside_the_filed_figures` (236-249): the band is
  `drawn.DISPLACEMENT_RECORD_SHARE`, 15%, read from the code under test. The code gives 105.5 t
  drawn against 106 t filed (`python -c`, form.drawn_displacement_kg), within 0.5%. So the band is
  30 times the fact: the drawing could be 15% wrong and pass. Medium, sure. Planted below.
- `test_each_sill_in_its_sources_band` (209-210): `max(sills) <= 1.23` then `max(sills) < 1.52`.
  The second can never fail after the first. Low.
- `test_the_port_triples_gaps...` (218-233) asserts only the four measured ports, against
  `PORT_GAP_M` from the code. It prints seven lines to the terminal on every run
  (`capsys.disabled`), so CI logs carry them. Low.

**(c)** `test_the_module_gives_the_files_lines_and_the_guns_figures` (367): the generator's
regeneration of every file, byte for byte, is in `test_profiles.py:1072-1075`.

**Else.** `test_the_sections_meet_the_plans_waterlines` (339) checks the note against itself (47
gaps): the note's self-consistency, no figure of the game. Low.

---

## test_hull_form.py

**Count and kind.** 28 tests, 101 cases (54 refusals at 405, 18 ship files at 800). No module
fixtures. It proves the shape schema's refusals in words, the drawing rule of `freesail/ship/form.py`
(through every given point, ends closed, transom, round counter, fullness, rail and stem head),
the pickle's state before stage 0H, the server's stations, an AST guard that nothing outside the
schema, the form and the server reads the shape, and the rule against Steel's 36, the 64 and Lynx,
typed in from their sources.

**(a)** None found. `test_a_closure_takes_its_levels...` (742-756) names `OUTLINE_MET_TWICE_AT` as
gone; grep finds it nowhere in freesail/ or tools/, as the docstring says.

**(b)**
- `test_the_rule_against_steels_36...` (1406-1408) pins the rule's error at five after timbers to
  5 mm (`STEEL_36_AFTER_BODY_WIDEST`). The rule getting *better* there fails the test. The comment
  (1388-1395) says so: "Recorded, never moved". One pin. Low, sure.
- The guard (847-1019) reads names, not types. Its docstring says so (859-861).
  `test_the_guard_finds_a_shape_read` (947) proves its teeth on 23 forms. Sound for what it claims.

**(c)** The refusals are already one table (249-402). Good.

**Else.** This file builds its hulls in memory and never reads a note. Its checks against measured
lines (1398-1427) are the only tests in my list that check the drawing rule against hulls it was not
written from. It is the file the six hull files should lean on.

---

## test_hull_frigate.py

**Count and kind.** 19 tests, none parametrised. Module fixtures `ship`, `spec`, `profile`,
`written`, `note`, `probe` (a subprocess that imports `tools/gen_ships.py` and runs
`hull_frigate.add_her_lines`). It proves the frigate-36's profile against `pages-zaz2587.md`, her
guns on their triples, her sills in bands, and the generator's report.

**(a)**
- `test_no_figure_the_physics_or_the_gunnery_reads_moved` (499-528): the git half skips. The
  `FILED` pins and the rudder (503-505) run. The spars, sails and lines are unpinned. Medium, sure.
- `test_the_sheets_own_ports_are_kept_for_package_81` (419-426) keeps `SHEET_PORTS`, a constant of
  `tools/ships/hull_frigate.py:155` that no code in freesail/ or tools/ reads (grep). The test is
  its one reader. Low, likely.

**(b)**
- Pins: 1448 t ±5 (445), "drawn 5.05 m deep" (447), worst gap ≤0.025 (460), six stderr sentences of
  the generator (629-637), the transom's edge 0.0-0.25 m off at three heights (404). Nine pins of
  the drawing and of the report's wording. Medium, sure.
- 446: `drawn_t / filed_t - 1.0 <= DISPLACEMENT_RECORD_SHARE` is one-sided (no `abs`); it is saved
  only by the pin above it. Low.
- 405: `assert "The transom's edge:" in note`, a word in a design note. Low.

**(c)** `test_each_port_gun_stands_on_a_triple_of_its_deck` (180) and the mark test (159) are in
`test_profiles.py` for every file. `test_no_gun_moved_in_calibre_number_or_place` (531) is a pin of
the fit as filed, likely also held in `test_ship_particulars.py` (not read).

---

## test_hull_lugger.py

**Count and kind.** 25 tests, 33 cases (9 at 282). Module fixtures `doc`, `profile`, `spec`, `note`.
It proves her profile against `pages-zaz6306.md` and Le Coureur's table at the note's factors.

**(a)**
- `test_each_port_gun_stands_on_a_triple_of_its_deck` (218-230): she has no port gun (230 asserts
  `_port_guns(doc) == []`), so the loop at 225 runs over nothing. The name promises a check that
  holds of nothing. The docstring says so honestly. A test that proves "she has no port gun" should
  be named so. Low, sure.
- `test_a_diff_of_her_files_physics_keys_against_git_shows_none` (605) skips. `HULL_AS_FILED` (577)
  holds the hull keys, not the spars or sails. Medium, sure.

**(b)**
- `test_the_note_says_the_ruling_on_her_depth_and_her_length` (526-541) asserts seven phrases of a
  design note and nothing of the game or the file. It is a test that a document says a sentence.
  Medium, sure.
- `test_the_bowsprits_rating...` (583-588) holds 21.8 kN and a bold phrase of the note.
- Pins: 101.5 t rel 2% (520), -2.53 ±0.03 m (522), counts `== 44` (400), `== 22` (435), `== 13`
  (448), `== 9` (508), `== 12` (418), `feet == ["8","6","5","4","3"]` (374). Eight counts of the
  note's and file's present shape.

**(c)** `SHAPE_MARKS` (41) and `test_the_marks_are_the_notes` (199) prove the same marks three ways
(the file, a constant in the test, the note).

---

## test_hull_schooner.py

**Count and kind.** 17 tests, 27 cases (`path` ×2 on 2; `key` ×9). Module fixtures `spec`,
`profile`, `raw`. One test runs `gen_ships.schooner` twice in a subprocess. It proves the topsail
and privateer schooners' one hull against `pages-chapelle-fig17.md`, the factors from Lynx, the
guns' ports and the generator's output.

**(a)** `test_no_figure_the_physics_reads_moved` (458-492), 2 cases: the git half skips;
`HULL_FIGURES` and the rudder run. Medium, sure.

**(b)**
- `test_the_transom_rakes_about_38_degrees...` (332-333) opens `docs/design/Build-Ships.md` and
  asserts the phrase "raked about 38° from the upright". A game test that fails when a design
  document is reworded. Medium, sure.
- `test_the_drawn_hull_stands_beside...` (378) reads `drawn._station_at(drawn._built(spec), 1.515)`,
  two private names and a magic x; it pins 198 t ±2 and 3.10 m ±0.02. Low.
- `test_the_shut_heels_in_the_note...` (526-536) is a sound check of `lee_port_shut`'s arithmetic,
  with a note-table string appended (536).

**(c)** `test_the_two_files_carry_one_hull` (116) duplicates `SAME_HULL_BY_INTENT` in
`test_profiles.py`, as its docstring says. `made == text` (423) duplicates the regeneration check
of `test_profiles.py:1072-1075`.

**Else.** `test_her_sections_run_fair_along_the_ship` (264) is a good test: it would catch a misread
section without a note.

---

## test_hull_smack.py

**Count and kind.** 20 tests, none parametrised. Module fixtures `raw`, `ship`, `hull`, `built`; a
`functools.cache` of subprocess runs of `tools/ships/hull_smack.py` (three: "as built", "steel",
"plate"). It proves her profile against `pages-chapman-pl59.md`, the module's tables against the
note's §4, and the "plate"/"steel" choice of the lead's ruling.

**(a)**
- Three tests prove "she has no port": `test_she_has_no_port_gun_and_no_port_triple` (260),
  `test_no_source_gives_her_a_sill` (273), `test_her_port_triples_gaps_are_reported_as_none` (283).
  The module docstring (5-7) says they "hold them to nothing, and say so". They exist to keep the
  six files' list of sections the same. One would do. Low, sure.
- `test_her_file_but_for_her_lines_is_what_it_was_against_git` (586) skips; `PHYSICS_KEYS` (573)
  runs. Medium, sure.

**(b)**
- 539-542: the exact sentence `"drawn displacement 38 t against the filed 46 t (-18%), more than 15%
  off: recorded, not moved"`. A golden text pin. The "15%" line of principle 8 is *exceeded* here
  (the code gives 37.9 t against 46 t) and only reported: the 15% is not a check for her. Low.
- `test_the_lead_ruled_the_plates_frames...` (302-315) tests that the module's word "steel" still
  builds the other choice. It keeps a road the project ruled against alive under test. Low.

**(c)** `test_the_module_makes_what_the_file_holds` (318) duplicates the regeneration check in
`test_profiles.py`.

**Else.** `test_the_modules_feet_are_the_notes_tables` (325-361) and
`test_the_modules_other_lines_are_the_notes_too` (364-436) hold a tool's constants against a design
note's Markdown tables, 110 lines of parsing. Tests of a tool and a document, not of the game.

---

## The six test_hull_<ship>.py files: one test written six times

Each file follows the same eleven sections, under near-identical names:

| shape | brig | cutter | frigate | lugger | schooner | smack |
|---|---|---|---|---|---|---|
| 1 profile and form load, `form.check` passes | 96 | 100 | 120 | 163 | 100 | 186 |
| 2 a mark on every line, the judged set pinned | 144 | 113 | 159 | 190, 199 | 130 | 217 |
| 3 each port gun on a triple of its deck | 172 | 166, 180 | 180 | 218 (none) | 290 | 260 (none) |
| 4 each sill in its source's band | 194 | 189 | 196 | 233, 261 | 336 | 273 (none) |
| 5 each point of the file is the note's | 263, 278 | 273, 277, 289 | 264, 285 | 296, 301, 308, 315 | 160, 165 | 291 |
| 6 the note's tables are its own points | 290, 305, 321, 347 | 322, 339 | 293, 352 | 324-496 (8 tests) | 186, 264 | 325, 364 |
| 7 drawn displacement and depth beside the filed | 436 | 236 | 434 | 514 | 372 | 526 |
| 8 port triples' gaps reported | 469 | 218 | 450 | 261 | 387 | 283 |
| 9 her notes carry no figure a rule computes | 482 | 379 | 569 | 544 | 402 | 200 |
| 10 physics keys pinned by hand | none | 416 | 503 | 577 | 464 | 573 |
| 11 physics keys against git f5be9110 (skips) | 576 | 423 | 499 | 605 | 459 | 586 |

About 60 of the 121 functions are shapes 1-4 and 7-11. Each copy differs only in its constants (the
file, the note, the gun x, the sill band, the judged marks, the filed figures, the pinned displacement
and depth) and in its spelling. Each file has its own helpers for the same jobs (`_raw`, `doc`,
`raw`, `written`; `_git_show`, `_before`, inline `subprocess.run`; `same_points` twice with two
tolerances). The fifth and sixth shapes do not repeat: each file has its own Markdown parser for its
own note's layout (`_table`/`lines` in brig, `points_in`/`bullet`/`note_table` in cutter,
`between`/`points`/`table_of` in frigate, `_part`/`_bullet`/`_table`/`_coureur` in lugger,
`note_section`/`note_list` in schooner, `_note_blocks`/`_table_rows`/`_between`/`_pairs` in smack).
Those tests break when a note is reworded or re-laid, and they prove a document and a data file
agree, not that a ship sails.

What a table would save:
- One `SHIPS` table (file, sister file, gun x, judged marks, sill band, filed figures, expected
  displacement and depth with a stated tolerance) and one parametrised test for each of shapes 1, 2,
  4, 7, 9 and 10: six tests over eight files in place of about 45 functions, perhaps 1,000 of the
  3,482 lines.
- Shapes 2, 3 and 8 are already proved for every file in `test_profiles.py` (764, 787, 1055).
  Those copies can go, not be tabled. So can the byte-equality checks of the module against the
  file (cutter 367, schooner 423, smack 318), which `test_profiles.py:1072-1075` does for every file.
- Shape 11 always skips (see brig). Either fetch the history in CI and keep one tabled test, or
  delete the six and keep one hand pin per file in the table.
- Shapes 5 and 6 can be tabled only if the six notes' points are moved into one machine-read form (a
  data file beside each note). Until then they are six parsers to keep.

---

## test_hulls.py

**Count and kind.** 11 tests, none parametrised, no fixtures. Five tests each build `hove_to_world()`
with a merchant brig put 3 miles off and sail 61 s or more. It proves package 84's `Hull` behind the
World's names, a crewed ship's own Hull, the player's vessel as the sea's own, and that a checkpoint
in the shape of before the Hull converts on load and ticks on to the same digest.

**(a)** `_old_shape_checkpoint` (108-219) forges a save "in the shape a build before package 84
wrote", 110 lines that pop and rename fields of the present classes. It has to be kept in step with
every new field. If the forge drifts from what an old build wrote, the test proves that the
converter reads the forge. The docstring (9-10) points to the kept real saves in `test_checkpoint.py`
as "the same proof on real files". Those are the proof; this is a second, synthetic one. Low,
likely.

**(b)**
- `test_the_players_vessel_is_left_out...` (359-363): a negative assertion on log text (no
  sighting with "a cable" and "frigate" in it). It passes under any rewording of the lookout's line.
  The `in_sight` check before it (355-358) is the real one. Low, sure.
- `test_the_worlds_per_ship_names...` (35) skips names the Hull lacks with `if hasattr`. Checked:
  1 of 63 (`_last_sea_height`) is skipped. Not empty. Sound.

**(c)** The hove-to world with a brig put at "49 33 N 5 30 W" is built in 79, 264, 313, 341, 373, 394:
the same setup six times. A module fixture cannot be shared where the tests run it on, but a
checkpoint copy could. Low.

**Else.** The digest comparisons after load (104-105, 247, 307, 407) are good tests of a hard thing.

---

## test_in_world.py

**Count and kind.** 9 tests, 95 cases (primer chapters, brief constants, tools, ten library topics
on a King's ship, three on a cutter, seven stations). Module fixtures `kings_ship` and `cutter`, two
scenario worlds, built not sailed. It proves that the primer, the briefs, the tools' words and the
library carry no word of the build (package, gate, milestone, the owner's rulings, a vendor's name).

**(a)** None. Its sources are read from the live code (`dir(agent)`, `TOOLS`, `tools.library`).

**(b)** `test_the_rule_has_teeth` (289-295) proves the patterns catch and the allow-list spares.
Sound. The allow-list is literal phrases (107-115), narrow.

**(c)** None.

**Else.** A file that tests documents. Here that is the purpose: these texts are served in the game
to a player or a model. Sound.

---

## test_indefatigable.py

**Count and kind.** 53 tests, 68 cases (`path` ×2 on 11 tests, three flips, one ×2 with ids).
Module fixtures `sixty_four` and `razee` (two ship loads). It proves the 64 and the razee: hulls,
profiles and sills against the measured lines, spars against Steel's table, sails, guns, crews,
ground tackle, names, polars, helm (truths 6 and 17), stays, wear and lying to, a scenario round
trip with a checkpoint, the driver and the mizen course, and the drafts of truths 7-186 to 7-189 and
7-230.

**(a)**
- Truths 7-186 to 7-189 (1620, 1693, 1806, 2725, 2777) are "drafted here ... to be moved into
  tests/test_known_truths.py in Phase 5" (15-19). `test_truth_7_186...` re-asserts what the tests
  above it assert: beam and draught (109, 133), 26 long 24s (1057), complements 491 and 330 and
  marines 84 and 50 (1144), four bowers of 57 cwt (1223). Low, sure.
- `test_her_notes_carry_sources...` (759-799) asserts that the ship file cites
  `"docs/dev/TuningNotes.md"` (774), with about 20 phrases of the YAML comments. It tests the
  comments of a data file. Medium, sure.

**(b)**
- `test_the_generators_report_prints_what_her_notes_no_longer_carry` (812-853) runs the generator
  in a subprocess and pins 15 sentences of its stderr ("spanker 200 m2 (was 218)", "its end 29.4 ft
  beyond it", and others): golden text of a tool's report. The file byte equality (834) duplicates
  `test_profiles.py`. Medium, sure.
- `test_her_drawn_hull_stands_within_its_bands_and_moves_nothing` (700-718): the name says "moves
  nothing" but the body checks only the displacement within 2% and the port gaps within 0.40 m, eight
  times `PORT_GAP_M`. Nothing of "moves nothing" is checked. Low, sure.
- 2173: `driver.area_m2 == round(area, 0) or abs(driver.area_m2 - area) <= 1.0`; the second arm
  makes the first redundant. Low.
- Docstrings carry dozens of "measured at seed 7" figures (1386-1396, 1426-1443, 1498-1502,
  2603-2621, 2780-2799) that no assertion holds. They will go stale silently. Low.

**(c)**
- `_world(tmp_path)` sails the same 1200 ticks of settling for
  `test_truth_7_230...[course]` (2527) and `test_truth_7_189_the_64_handles...` (2725), and with the
  driver bent for `[driver]` and `test_the_64s_driver_is_brailed...` (2558): one scenario sailed four
  times.
- `test_truth_7_189_she_stays_quickly...` (2777) tacks the frigate-36 three times (2802-2808) as a
  reference, which the truths of `test_known_truths.py` already sail.
- `test_the_razee_stays_wears_and_lies_to...` (1497) and 7-189 (2777) are the same tack-wear-heave
  routine for the two hulls, wanting one table by path.

**Else.**
- **The slow tier.** None of the 68 cases is in `SLOW_TESTS` or reads a `DAY_FIXTURES` fixture
  (collect: none deselected). About twelve sail: the helm tests (1422, 2 × at least 3,600 ticks
  plus three `under_plain_sail` settles), the stays (1497, three tacks, a wear, 900 ticks), the
  round trip (1545, 2 × 5,400 ticks plus 600), truth 7-188 (four `_interval`s, each 100 ticks plus
  1,200 battery ticks), 7-230 ×2, the driver brailed (up to 7,000 ticks), the shift (1,200 plus up to
  3,000), 7-189 ×2, truth 9 ×2 (four `sail_in_a_wind`). The 74's twins in `test_bellerophon.py` are
  in `SLOW_TESTS` at 5.2 to 28.8 s each (conftest.py:557-566). So the fast tier almost certainly runs
  minutes of sailing it says it leaves out. Conftest.py:25-27 admits a new long test is not caught.
  Medium, likely (not timed).
- `test_the_64s_driver_is_brailed...` (2585) reuses the file `_world(..., bent=True)` wrote at the
  same `tmp_path` 22 lines earlier: an unstated coupling inside the test. Low.
- `test_her_helpers_refuse_a_cut_that_breaks_its_contract` (2878) and `test_her_flips_stand_each_by_
  itself` (2939) test the generator's helpers and flips: tools, not the game. They are cheap and
  sound.

---

## test_islands.py

**Count and kind.** 9 tests, 10 cases (2 scenarios). Module fixtures `manifest` and `whole` (the
atlantic-east chart loaded). It proves Madeira and the Azores in the chart, their unlit 1805 lights,
Pico's peak to its geographic horizon, the roads' depths, the Portuguese neutral ports, the tide
gauges and Norie's hours, Fayal's channel stream, the tile tool's same bytes, and the two scenarios'
loading.

**(a)**
- `test_the_islands_ports_are_portuguese_neutral_and_stand_on_their_own_positions_too` (173): the
  docstring promises "on the Channel's chart alone their own positions"; no Channel chart is loaded.
  The position check (186) compares latitude only. Checked: all 15 spots have a `feature_id`, so the
  loop is not empty. Low, sure.
- `test_the_islands_gauges_are_read...` (194) takes a parameter `tide=None` that nothing uses. Low.

**(b)** `len(lights) == 10` (112), tile counts `== 25` and `== 153` (95-96): pinned counts of data.
Low.

**(c)** None.

**Else.** `test_the_islands_stand_alone...` (74) and `test_a_tile_is_written...` (254) test
`tools/build_charts.py` and the manifest, not play. The Pico test (123) is a good test of a hard
behaviour: the tall-feature search beyond the index's reach.

---

## What I did not look at

The six pages notes under `docs/design/ships-design/` and `docs/design/Build-Ships.md` (forbidden);
so I cannot say whether a hull file's figures are right against its sources, only what the tests
compare. `tests/test_profiles.py` beyond the lines named. `tests/test_ship_particulars.py`,
`tests/test_known_truths.py`, `tests/test_bellerophon.py`, `tests/test_crews.py` and
`tests/test_brains.py`, which these files import or lean on. No timing of any test.

## Faults to plant

1. **tests/test_hull.py::test_leeway_change_is_noted_at_most_once_a_minute.** In
   `freesail/physics/integrate.py` line 527, delete the clause
   `and st.seconds_since_leeway_note >= hp.LEEWAY_NOTE_INTERVAL` (or set `LEEWAY_NOTE_INTERVAL =
   0.0` at `freesail/physics/hull.py:159`). The name says it catches more than one leeway note a
   minute. Prediction: passes although the game is broken (likely).
2. **tests/test_hull.py::test_all_four_ships_run_under_bare_poles.** In `freesail/physics/sails.py`,
   make `_sail_windage_area` (1553) and `_spar_windage_area` (1577) return `0.0`. The docstring says
   it proves the ships drift under windage alone. Prediction: passes although they do not drift
   (likely).
3. **tests/test_hull_cutter.py::test_the_drawn_hull_is_reported_beside_the_filed_figures.** In
   `freesail/ship/form.py`, multiply what `drawn_displacement_kg` returns by `1.10`. The test says it
   holds the drawn displacement beside the filed. Prediction: passes (105.5 t becomes 116 t, +9.5%,
   inside the 15% band); the lugger's and the brig's pins in their own files fail.
4. **tests/test_hull_cutter.py::test_a_diff_of_her_physics_keys_against_git_shows_none** (and the
   brig's `test_no_figure_the_physics_or_the_gunnery_reads_moved[data/ships/brig.yaml]`). In
   `data/ships/cutter.yaml` change the `rating_kn` of `main.mast` (and in `brig.yaml` the hull's
   `gm_m` by +0.2), and make the same change in `tools/gen_ships.py` so the regenerated file matches.
   The name says no physics figure moved. Prediction: skips (f5be9110 absent), so passes, and no
   other test in my files catches it.
5. **tests/test_indefatigable.py::test_her_drawn_hull_stands_within_its_bands_and_moves_nothing.**
   In `tools/ships/indefatigable.py` (and regenerated `sixty-four.yaml`), move every quarterdeck
   port triple's half-breadth in by 0.2 m. The name says "moves nothing". Prediction: passes if the
   quarterdeck's gaps were within ±0.2 m (I have not measured them); the 0.40 m band is wide enough
   (suspicion).

Faults no test in my files would catch, though a player would:

1. The leeway line every few seconds while it changes (fault 1): a log flooded on a beam reach.
2. No windage under bare poles (fault 2): a ship hove to or lying a-hull does not drift to leeward.
3. A spar's rating or a sail's area changed for the brig, cutter, lugger, schooner, smack or frigate
   in `tools/gen_ships.py` and the file regenerated: gear carries away earlier or later. The six
   "nothing the physics reads moved" tests skip in every shallow checkout, and the hand pins hold
   only the hull's keys (the brig's none).
