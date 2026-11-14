# Tests, reader 11: test_standing.py to test_world_orders.py, and the suite's machinery

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Every file below was read whole. The suite was
not run. Two short commands were run: `pytest --collect-only` on my 26 files (14 s, collection
only, no test body executed) to count the cases and check node ids, and a few seconds of Python
to import `tests/conftest.py` and `tests/test_standing.py` and count their lists. Nothing under
docs/dev, docs/design, docs/playtests or docs/gates was opened.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_standing.py | 2211 | 50 (249) | none module-scoped; many tests sail the frigate 15 to 60 min | sound in the main; one guarded assertion, one test of the test, stale "held" words |
| test_staying.py | 484 | 17 (20) | `frigate_by_the_wind` (module, mutated by 3 tests) | sound physics; wide bands; shared mutable fixture; duplicates truths 10/16 |
| test_stores.py | 184 | 9 (9) | none | sound |
| test_strain.py | 733 | 31 (36) | none | sound unit layer; World tests duplicate truth 9 |
| test_studding.py | 537 | 22 (37) | `brought_up` (module, 2 params, ~45 min sailed each) | sound for the frigate; schooner half parked as strict xfail |
| test_subtypes.py | 1211 | 33 (85) | `gen` (module, cheap) | pins much (exact ticks, data tables); truth 7-191 "draft" never moved |
| test_sun.py | 229 | 13 (13) | none | sound; almanac-checked |
| test_tackle_orders.py | 754 | 27 (43) | `moored_brig` (module, ~100 min sailed, checkpointed) | sound; good fixture practice |
| test_tell.py | 390 | 15 (16) | none | sound |
| test_the_ship_herself.py | 165 | 5 (14) | none | one test asserts what it passed in |
| test_tide.py | 1369 | 32 (32) | `tide` (module, cheap) | truths 62-64 sound; two thirds is a data audit pinning id lists |
| test_tow.py | 209 | 5 (5) | none | sound; one name promises "half a knot", body asserts about a knot |
| test_trim_order.py | 331 | 14 (16) | none | sound; half on a fake runner |
| test_units.py | 123 | 12 (29) | none | sound |
| test_via.py | 246 | 6 (6) | `off_falmouth` (module, mutated), `frigate_via` (module, up to 4 days) | sound; one `or`-shaped assertion |
| test_view_action.py | 570 | 17 (93) | none (Node per case) | sound; run twice over by truths 7-450..454 |
| test_viewer_action.py | 278 | 13 (49) | none | sound |
| test_visitor_name.py | 94 | 3 (3) | none | sound |
| test_wardroom.py | 147 | 4 (4) | none | covers 4 of 12 wardroom files |
| test_wardroom_doors.py | 879 | 22 (22) | none | sound; one test reads source text; a dead `assert allowed` |
| test_water.py | 317 | 11 (11) | none | sound; pumps checked on 7 of 18 ship files |
| test_weather.py | 1002 | 31 (35) | none | arithmetic sound; climatology tests parse prose notes; two stale names |
| test_weather_script.py | 403 | 21 (29) | none | sound |
| test_wind.py | 157 | 6 (10) | none | sound; long statistical runs |
| test_world.py | 82 | 9 (9) | none | milestone-1 point ship; one band wide enough for anything |
| test_world_orders.py | 1070 | 28 (28) | none | sound; long sails inside fast-tier tests |

Total for the 26 files: 903 cases collected from 522 test functions.

---

## The suite's machinery

### tests/conftest.py (737 lines, read whole)

**How the slow tier is decided** (`_is_slow`, conftest.py:589-592; `pytest_collection_modifyitems`,
:668-717). A test is marked `slow` if either:

1. its file is a key of `DAY_FIXTURES` (:42-99) and one of the fixture names listed for that file
   is among `item.fixturenames`: 11 files, 48 fixture names; or
2. its node id with `tests/` stripped is a member of the hand-written frozenset `SLOW_TESTS`
   (:103-568); or
3. it is a "pace" test (`_is_pace`, :648-657): marked `pace` by hand or whose name ends with
   `holds_truth_51s_floor` or `ticks_at_the_build_machines_floor`; these get both `pace` and `slow`.

The slow tests are then deselected unless `--slow` is given, or the `-m` expression contains the
substring "slow", or anything was "chosen on the command line" (:660-663).

**How many named by hand.** `SLOW_TESTS` holds **370** node ids (counted by importing the module).
133 of them are in test_known_truths.py. The list is the record of a measurement made on one
machine on dated runs ("2026-10-01", "2026-11-06" and so on); nothing re-measures it.

**What happens to a slow test that is renamed.** Nothing says so. Its old id stays in the set and
matches nothing; the renamed test is no longer marked and runs in the fast tier whatever its time.
The file's own docstring admits it (:25-27). I checked every entry against the test functions now
defined:

- `test_standing.py::test_the_well_is_held_in_the_book_and_never_fires` (:418): gone; the test is
  now `test_the_well_is_sounded_every_glass_and_read_and_replays` (test_standing.py:1855), which
  sails an hour of the frigate and a replay, now in the fast tier.
- `test_orders_m4a.py::test_the_starter_file_loads_in_the_console_with_the_well_refused_and_the_rest_entered` (:318) and `..._with_the_well_held_...` (:415): both gone; the test is now
  `test_the_starter_file_loads_in_the_console_and_every_order_is_entered` (test_orders_m4a.py:318).
- `test_rollup.py::test_the_server_takes_speed_to_three_hundred_and_serves_the_store_by_ticks`
  (:351): gone; now `..._to_a_thousand_...` (test_rollup.py:239).

So 4 of 370 hand-named ids are dead (sure; parametrised ids outside my files were not checked
against collection, only their base names). Parametrised ids with positional suffixes are fragile
by construction: `test_staying.py::test_turning_truths_..._[brig-band2-fastest_band2]` (:375-376)
names the band by its index in the parametrise list, so reordering the table silently moves the
mark. Weight medium (the fast tier slowly fills with slow tests and nobody is told); confidence
sure.

A cheap mend the owner could ask for: a collection-time check that every `SLOW_TESTS` id and every
`DAY_FIXTURES` name matches something collected, failing loudly. Today a typo in either is silent.

**The shard rule does not keep a day whole (a real fault).** `FREESAIL_SHARD` (:692-716) shards by
`item.get_closest_marker("xdist_group")` "so a module-scoped day or passage stays whole on one
machine" (:695-696). But the `xdist_group` markers are added by `_group_by_shared_fixtures(items)`
at :717, *after* the sharding at :698-716, in the same hook. No test file sets `xdist_group` itself
(grep of tests/, pyproject.toml, .github/: only conftest). So when the shard key is read no item has
the marker, every item is sharded by its own node id, and the tests of one module-scoped day are
spread over the six machines of `.github/workflows/whole-suite.yml:63`, each machine sailing the day
again. The comment says the opposite of what the code does. Weight medium (the whole-suite workflow
pays for each day up to six times, and its timings mislead); confidence sure.

Also at :715, `items[:] = [i for i in items if i not in set(others)]` rebuilds the set for every
item: quadratic in the suite's size (about 3,800 test functions in 171 files). Low weight, sure.

**The command-line rule is wider than it says.** `_chosen_on_the_command_line` (:660-663) is true if
`-k` is given at all, or if *any* argument contains `::`. So `pytest tests/test_a.py
tests/test_b.py::one` runs all of test_a.py's slow tests too, and `pytest -k anything` over the
whole tree turns the slow tier on for every match. Low weight, sure.

**`"slow" in markexpr`** (:681) is a substring test: `-m "not slow"` turns `run_slow` on and then
`-m` deselects them; the effect is right by accident. Low.

**Sound:** the union-find grouping of module fixtures (:619-645) and the worker count hand-back
(:720-725) do what they say.

### tests/messages_api.py (474 lines)

A local HTTP server in the Messages API's streamed shape, a fake keyring and a fake page, used by 8
test files. Sound as a fake. Two notes: `fake_store` (:319-343) monkeypatches the private
`keyring.core._keyring_backend`, which a keyring release can rename (a test-infrastructure break,
not a game one); `wait_for` (:421-430) polls a real clock for up to 15 s, so slow machines make
these tests flaky rather than wrong. Low.

### tests/rig_fixtures.py (1089 lines)

Eight in-memory ship documents built from the committed ship files (the frigate with a mizen yard,
a settee brig, the driver, three schooner trials, tartane and polacre probes), used by nine test
files and named in a docstring of `freesail/evolutions/scripts.py:1298`. It reads the live
`data/ships/*.yaml` and looks lines up by id (`_like`, :1013-1022), so a renamed line in a ship file
fails loudly with a KeyError: good. Every figure in it is the module's own (judgement constants,
:73-262); tests that check "the fixture's area is the centroid's" check this file against itself.
`_scaled` (:747-753) silently gives a line with no rating 10 kN. Low.

### tests/fixtures/ and tests/browser_plans/

`tests/fixtures/` (2.4 MB on disk):

| file | size | what it is |
|---|---|---|
| saves/m5c-b-harpy-tick602100.json + .checkpoint | 790 KB + 766 KB (gzip of 3.9 MB) | a playtest's saved game at tick 602,100 (556 inputs) and its pickled World |
| saves/m5c-cutter-tick34091.json + .checkpoint | 93 KB + 212 KB | a playtest's saved game at tick 34,091 and its checkpoint |
| saves/m5c-c-37d-officer-tick5400.json + .checkpoint | 21 KB + 203 KB | a package's own save with a fake officer, stamped build "m5c-c/37d" |
| saves/pre-100-step-2-letter-in-hand.json + .checkpoint | 2.4 KB + 196 KB | a save stamped build "m6c", tick 8,140 |
| saves/pre-75-cutter-guns-cast-loose.checkpoint | 33 KB | a bare checkpoint, no save beside it |
| flag_drawings_before_102.json | 128 KB | recorded drawing output (flag polygons) before package 102: a golden file |
| ConsentBrief-before-37g.md, -42a.md, -42b.md | 10.5, 10.6, 14.4 KB | old texts of the consent brief, compared against by test_officer.py |

The four saves are recorded runs (JSON: seed, scenario, `ship_ref` as a *path*, the journal of
inputs, standing orders, agents); the five checkpoints are gzip'd pickles of the program's own
object graph (`freesail/core/replay.py:20-40`). What makes them go stale:

- a checkpoint: any class renamed or moved, any new field without a class default, any change to
  the unpickler's allow-list; the replay module says these are mended by class defaults or
  `_rebind`, never by changing a fixture;
- a save's replay: any change to the physics, the RNG streams or the order grammar changes the
  digest; `ship_ref` is a path into data/ships, so a renamed ship file breaks every save naming it;
- the Harpy and cutter saves hold a model's transcript and the owner's typed lines; test_checkpoint
  skips its tests when they are absent (test_checkpoint.py:155-160), so deleting them turns failures
  into skips. They are present in this tree.
- `flag_drawings_before_102.json` is a golden pin of drawn output: any deliberate change to the flag
  drawing breaks it, and the reader cannot tell from the file why each polygon is right.

`tests/browser_plans/` (68 KB): 13 YAML plans (587 B to 2.4 KB) that `tools/browser_probe.py` types
into the real page in Chromium, two scenario YAMLs (583 and 593 B, one also loaded by
test_known_truths.py:16932) and `worlds.py` (670 B), which imports the private helper
`_struck_to_a_crewed_frigate` from `tests/test_captive.py`: a plan depends on a test module's
internals. The plans are run by `test_browser_probe.py` in the slow tier (`DAY_FIXTURES`). Not
recorded runs: scripts.

---

## Per file

### test_standing.py (2211 lines; 50 tests, 249 cases)

1. **Count and kind.** `test_table` is parametrised over `TABLE`'s 168 rows (116 accepted, 52
   refused) against four ships; three more parametrised tests (8, 11 and 16 cases). No module
   fixture; `synthetic` swaps a registry row per test (:912-926). Proves the standing-order
   dialect's grammar and refusals, the runtime's edge, duration, dwell and `every` timing, the
   conflict rule, the book's verbs, save and replay, the drivers, and the vocabulary's undo table.
2. **(a) Gone or stale.** The well: `WELL` is commented "held, not refused (package 33c)" at :115,
   :454, :532, and the section header :1757 says "the well held"; but
   `test_the_well_is_sounded_every_glass_and_read_and_replays` (:1855) proves the rule now fires
   (`rule.held is None`, :1871). The comments are stale and the slow list still names the old test
   (see conftest). Low, sure.
3. **(b) Built not to fail.**
   - `test_table_is_large_enough` (:882-884) asserts `len(TABLE) >= 100` and 30 refusals: a test of
     the test's own data, which no fault in the game can fail. Low, sure.
   - `test_the_dwell_waits_for_the_evolution_the_firing_started` (:1212-1232): the assertion the name
     promises ("not yet re-armed") sits under `if any(i in runner.instances for i in
     rule.started)` (:1229). The reef's steps in data/evolutions/reef_square.yaml are 60 + 150 + 90 s,
     about the dwell of 300 s (`STANDING_DWELL_S`, freesail/standing/rules.py:44) the test waits
     out (:1227, 301 s). If the reef is done by then, the test asserts only `rule.armed`, which is
     true with or without the rule under test. Medium, likely.
   - Pins of constants read from the code: `EVENT_SETTLE_S == 3600` (:1640), `GLASS_TURN_IN ==
     0.03` (:1686). Low.
   - The rest of the timing tests assert exact ticks of edge firings on synthetic readings: good,
     hard to pass by accident.
4. **(c) Might be one.** `test_a_rule_built_from_the_pieces_fires_like_its_dialect_twin` (:1543)
   and test_python_api.py's twins prove the same equivalence. The book's replay is proved in
   :1376, :1404 and :1855, each with its own sail.
5. **Else.** `test_firing_is_deterministic` (:1151) compares two worlds in one process: it cannot
   catch a dependence on hash seed or process. `test_the_starter_and_the_scenario_books_still_load_whole`
   (:2143) is a good regression net over four shipped books.

### test_staying.py (484 lines; 17 tests, 20 cases)

1. **Count and kind.** One module fixture `frigate_by_the_wind` (the frigate under plain sail 300 s
   on, in `DAY_FIXTURES`), used by three tests. Imports helpers from test_known_truths.py. Proves
   the yaw damping's scaling, the rudder slope, turning circles, tacks of four ships, Luce's
   recovery, a missed stays, the sheet's trim, heaving to fore-and-aft, the starter book's sheet
   tending.
2. **(a)** None found.
3. **(b)**
   - Bands: turning circle in lengths, schooner 4.0 to 7.0 (measured 5.4, :113), cutter 3.5 to 6.0
     (4.9), brig 4.0 to 6.0 (4.8); swing rate cutter 3.5 to 7.0 deg/s (5); brig's tack 285 to 600 s
     (measured 454, :195). Each band admits a change of a quarter or more either way. The docstring
     (:14-16) says the bands are judgement; still, a 25% slower cutter passes. Medium, sure.
   - `test_a_sails_aback_line_waits_out_a_seas_period` (:450): pins `BACKED_DWELL_S == 10.0` and calls
     the private `_record_backed` by hand after sailing 600 ticks it does not need; it is in
     `SLOW_TESTS` for a sail it does not use. Low.
4. **(c)** `test_the_cutter_swings_twice_as_fast_as_the_frigate` (:128) sails the cutter's circle
   again after the parametrised test sailed it; `test_tack_truth_the_cutter_is_quicker_than_the_schooner`
   (:175) sails the schooner's tack again after :161 did. Truths 10 and 16 in test_known_truths.py
   sail the frigate's.
5. **Else.** The module fixture is mutated by every test that reads it (:266, :300, :327: hauls, eases,
   lets fly the spanker sheet): the three tests depend on order. Run alone with `-k` each sees a
   different spanker. Medium, sure. `test_the_starter_book_tends_the_sheets_every_glass` (:377)
   checks the line is in the book's text and then submits its own copy, so the book as loaded is
   not what is tested.

### test_stores.py (184 lines; 9 tests)

Proves the ration table, a day's fall, short allowance, foul water, a store run out, replay. Sound.
`test_the_hands_tire...` (:137) pins `HARDSHIP_WORK == 0.5` (:151), a constant read from the code.
`test_the_ration_table...` (:42) checks every ship file's ration block: a good cross-file guard.

### test_strain.py (733 lines; 31 tests, 36 cases)

1. Unit tests of `apply_strain` on a minimal ship, consequences on the frigate and schooner, World
   runs of 20 minutes at 20 and 35 knots. No module fixture.
2. **(a)** `test_ratio_of_the_weakest_part_on_the_reference_ships` (:671) says it "documents where the
   draft ratings put the reference ships": a documentation test; its two `> 1.5` floors do assert.
3. **(b)** `test_probability_at_a_fixed_seed_gives_a_known_tick` (:252) builds its oracle by
   re-implementing the one-draw-a-tick rule; it pins the algorithm rather than the outcome (fair for
   determinism). :657 `any(p.wrecked ...) or snap["blown_out"]` is weak but follows :649. :668 pins
   the stream names. Low.
4. **(c)** `test_nothing_carries_away_in_twenty_knots_under_plain_sail` (:630) and
   `test_something_carries_away_in_thirty_five_knots_under_all_sail` (:644) are truth 9's two halves,
   which test_known_truths.py also sails (`test_truth_9_*`, both in `SLOW_TESTS`). Same scenario
   twice.
5. **Else.** The parted-line tests (:332-472) each pin the exact log sentence; a wording change breaks
   six tests, which is the project's choice.

### test_studding.py (537 lines; 22 tests, 37 cases)

1. `brought_up` (module, parametrised frigate and schooner): set studding sails at nine points, then
   thirty trims at six points; each is about 45 minutes of ship time. In `DAY_FIXTURES`.
2. **(a)** None.
3. **(b)** **The schooner's half is a strict xfail** (:203-212): `pytest.param(SHIPS[1],
   marks=_SCHOONER_IN_IRONS)`. Both tests using `brought_up` (:225, :234) are expected to fail on the
   schooner, because she lies in irons going astern during set-up (comment :196-202). An xfail
   swallows *any* failure: a schooner whose studding sails never set, an exception in the set-up, a
   broken stall curve, all pass as "xfailed". `strict=True` only makes a mend fail loudly. So truths
   29 and 30 are not proven on the schooner at all, and the module fixture still sails her day to get
   there. Medium, sure. Nobody could expect it mended without a change to the set-up script, which is
   the test's own.
4. **(c)** The tack tests (:376, :401) sail `close_hauled` again per ship per test.
5. **Else.** `test_the_water_sail_needs_no_boom_rigged_out` (:279) asserts only that the main boom is
   rigged out at load: data, not behaviour. `test_setting_studding_sails_on_a_wind_is_not_refused`
   (:245) has no assertion beyond "does not raise", which is what it means.

### test_subtypes.py (1211 lines; 33 tests, 85 cases)

1. The sub-types as fits and roles, index rows, role refusals at load, the Indiaman's and revenue
   cutter's books, far and crewed behaviour, the pivot's arc from the generator, quarters in unarmed
   files, truth 7-191. `gen` (module) loads tools/gen_ships.py.
2. **(a)** `test_truth_7_191_...` (:1024) is "**A draft, for Phase 5 to move into
   tests/test_known_truths.py**"; grep finds no `7_191` in test_known_truths.py. The move never
   happened; the truth lives as a draft. Low, sure.
3. **(b)** Pins with "measured on the owner's machine" and nothing a reader can check:
   `states == [(60, ...), (120, "on passage")]` and `(1920, ...)` (:574, :577), `(540, "evading")`
   (:604), `[(120, ...), (360, "chasing"), (420, "evading")]` (:677-681), morale `0.123` and `0.273`
   (:1055-1063), the quarters' divisions (:912-916), the pivot's arc `(62.0, 141.0)` (:869). About a
   dozen exact pins; any change to the brains' timing breaks several at once and the mender will be
   tempted to re-pin. Medium, sure. `TABLE` (:59-72) and `INDIAMAN_FIGURES` (:444-452) restate data
   files.
4. **(c)** `_at_sea`, `_sail` and `_states` are re-sailed per test; the revenue-cutter scenarios
   (:557, :581, :1088, :1119, :1164) could share one world.
5. **Else.** Many tests (:455-510, :608-629) check the shape of doctrine YAML files, not play.

### test_sun.py (229 lines; 13 tests)

Sound: an almanac's times with a stated tolerance (:28-35), events once a day, longitude, high
latitudes, replay. `test_a_whole_day_raises_each_event_once_and_deterministically` (:161) runs a
whole day twice in one process for two events. Low.

### test_tackle_orders.py (754 lines; 27 tests, 43 cases)

Sound and well made. `moored_brig` (:92-104) sails once, writes a checkpoint, and each test reads a
fresh copy (`moored`, :107): the right way to share a long set-up. It is **not** in `DAY_FIXTURES`
and costs about 100 minutes of ship time; if it is over the threshold the tests reading it are in the
fast tier unmarked (not measured). `test_the_goulets_eight_hours_give_at_most_five_lines` (:440)
asserts `1 <= len(said) <= 5` and urgent `<= 2`: a band, stated. `test_every_ports_road...`
(:492-513) pins the list of ports without a bottom note.

### test_tell.py (390 lines; 15 tests, 16 cases)

Sound; every case on the scripted fake. `test_the_vocabulary_knows_tell` (:265) tests the data file.

### test_the_ship_herself.py (165 lines; 5 tests, 14 cases)

**(b)** `test_every_stations_brief_opens_its_situation_with_the_ship` (:120-144), six stations: it
builds the brief itself with `ship=R.ship_words(w)` (:131) and asserts the situation starts with the
ship's words. It proves `Brief.build` puts what it is given first; it does not prove any station's
real seating gives it the ship. The seating's own call (freesail/agents/harness.py:1156) is tested
only for the officer (:147). Medium, sure. Imports helpers from test_brains, test_crews and
test_agents.

### test_tide.py (1369 lines; 32 tests)

1. `tide` (module) loads the tables. Truths 62, 63, 64 (:67-249) are good: the establishment within
   20 minutes, springs to neaps, the stream off the Lizard by the hour, Moore's rule against the
   world's tide, each a physical claim with its source.
2. **(a)/(e)** About twenty of the 32 tests audit data/tide files: lists of gauge ids in order
   (:672-682, :750-762, :826, :992, :1055-1062), counts (`len(channel) == 15`, :513;
   `len(blocks) == 89`, :1134), the set of block names (:1140-1172), the seam catches (:1333-1337).
   Each new block has meant editing several of them ("old: 76", :1132; "was 14", :511). They test a
   document, and they pin it. Medium (cost of upkeep, and they invite re-pinning), sure.
   `test_the_constituents_...` (:62-64) asserts the words "TICON", "CC BY 4.0" and "UNVERIFIED" are in
   the YAML file's text.
3. **(b)** `test_truth_63_a_ship_hove_to...` band 3 to 14 miles in six hours (:153) is wide; the
   tighter claim (:180) carries it. Low.
4. **(c)** The "blended everywhere would move Falmouth" trial is written five times
   (:700-712, :842-851, :1008-1017, :1066-1077, :1350-1369): one helper and a table of blocks.
5. **Else.** `test_the_fill_is_raised_by_the_level...` (:1194) loads tools/build_charts.py and tests
   the tool, not the game.

### test_tow.py (209 lines; 5 tests)

**(a)** `test_the_lugger_is_towed_clear_of_the_lavandiere_at_half_a_knot` (:204) runs a helper that
asserts `0.8 <= speed <= 1.3` (:179); the comment (:176-178) says half a knot is the four-hour figure
in the known truth. The name promises what the body does not check. Low, sure. Otherwise sound; the
cutter test (:46) checks the head, the speed, the station, the tiring and the end in one sail.

### test_trim_order.py (331 lines; 14 tests, 16 cases)

Sound. Eight tests use `FakeRunner` (:14-27) and assert what was *started*, which is the order's
job. `from freesail.evolutions import trim` twice (:78, :84). `test_trimmed_for_the_point...` (:305)
compares two half-hour sails: a real behavioural test.

### test_units.py (123 lines; 12 tests, 29 cases)

Sound.

### test_via.py (246 lines; 6 tests)

1. `off_falmouth` (module, 120 s) and `frigate_via` (module, up to four days, `DAY_FIXTURES`).
2. **(b)** `test_an_intent_by_way_of_marks_gives_the_captain_the_legs` (:131-132):
   `assert [lg.kind for lg in plain] == ["to"] or all(lg.kind != "via" for lg in plain)`. The second
   clause is true of an empty list, so a planner that returns no legs at all for a plain passage
   passes. Medium, sure.
3. **Else.** `off_falmouth` is mutated by `test_the_order_shapes_the_first_mark...` (:76-111: orders
   given, the way target set by hand, two minutes run); the next test reads its account. Order
   dependence. Low.

### test_view_action.py (570 lines; 17 tests, 93 cases)

1. Node-driven tests of client/projection.js (skipped when Node is absent; Node is present here and
   on the CI images). Parametrised over every armed profiled ship file, found by glob at import.
2. **(c)/(e)** Truths 7-450 to 7-454 in test_known_truths.py (:15125-15190) import and call these very
   test functions in loops. The same work runs twice, once fast here and once in the slow tier there
   (7-450, 7-451 are in `SLOW_TESTS`). Worse, calling a decorated test function directly bypasses its
   `needs_node` skip: only 7-450 checks for Node itself; 7-451, 7-452 and 7-454 would error, not skip,
   on a machine without Node. Low, sure.
3. Sound otherwise; the paint-order tests over 48 views each (:378, :439) are strong.

### test_viewer_action.py (278 lines; 13 tests, 49 cases)

Sound. `test_a_gun_a_tenth_off...` (:133) inserts tools/ into `sys.path` at run time and tests
tools/check_viewer_guns.py. `test_the_graph_serves_the_guns_and_the_ports` (:158) pins 40 guns and 18
ports for the frigate. Imports private helpers from test_known_truths and test_lee_ports.

### test_visitor_name.py (94 lines; 3 tests)

Sound. Depends on private helpers of test_between_hulls and test_door_follows. In `SLOW_TESTS`.

### test_wardroom.py (147 lines; 4 tests)

**(e)** `test_the_ship_files_posts_and_people_agree_with_the_wardroom_files` (:42) checks 4 ships
(`SHIPS`, :19-24); data/people has 12 wardroom files. The same check is copied into
test_bellerophon.py:687, test_bilander.py:1061, test_indefatigable.py:1213 and test_neufchatel.py:788.
One test over `data/people/*.yaml` would cover all and replace five; as it stands the lugger, the
smack, the merchant brig and the 64 have, as far as I found, no agreement check. Medium, likely.

### test_wardroom_doors.py (879 lines; 22 tests)

1. The lesser stations, binding, stand-by on several conditions, the deck's conversation, the
   player's seat, the doors and the pace rule; all on fakes.
2. **(b)** :244 builds `allowed`, never uses it, then asserts `allowed and ...` (:272): the first
   half is a non-empty literal. Low, sure. :866 `note in h.brief.text() or "The station's journal"
   in h.brief.text()`: weak. :490-493 accepts either of two wordings.
3. **(e)** `test_the_cadence_policies_and_the_doors_flags` (:832-834) reads the source text of
   freesail/agents/mcp_server.py and local.py and asserts the strings `"--cadence"` are present: it
   tests the code's text, not behaviour. Low.
4. **Else.** `test_the_rules_based_captain_gives_a_seated_officer_the_deck...` (:642) sails about four
   hours then up to sixteen more, and pins the meeting tick 14,700 by a comment about package 88; it is
   not in `SLOW_TESTS` (time not measured; a suspicion it is over 5 s).

### test_water.py (317 lines; 11 tests)

Sound behavioural tests of leaks, pumps, foundering and hatches. **(e)**
`test_the_ship_files_carry_their_pumps_and_plugs_through_the_generator` (:293) says "every ship file"
and checks 7 of the 18 in data/ships. `test_the_hatches_battened...` (:219) monkeypatches the sea
height, which is the input, not the thing tested: fair.

### test_weather.py (1002 lines; 31 tests, 35 cases)

1. Systems arithmetic against the gradient rule, fronts, sectors, seeding, scenario forms, readings,
   log, roll-up, sea breeze, climatology boxes.
2. **(a)** `test_the_hooks_for_the_coast_are_inert_until_5b` (:249): the hooks have been built
   (freesail/world/weather.py:1546-1640, used at :1379, :1505); the test now only checks the no-coast
   default. Stale name. Low, sure. `test_the_climatology_has_four_boxes_the_channels_as_it_was_and_three_provisional`
   (:710) asserts **thirteen** boxes (:717-734). Stale name. Low, sure.
3. **(e)** The climatology tests (:765-1002) parse the *prose notes* of data/weather's climatology
   YAML (`row["note"].split(": N ", 1)[1].split(", the calm")...`, :813, :851, :993) and sum days per
   point against pinned totals: tests of a document's wording, which break if a note is rephrased.
   Medium, sure.
4. **Good.** `test_a_single_lows_wind_follows_the_gradient_rule` (:91) computes the expected wind from
   the stated rule independently: a real check.
5. `test_from_the_harpys_own_weather...` (:665) depends on the playtest fixture and skips without it.

### test_weather_script.py (403 lines; 21 tests, 29 cases)

Sound. `test_trim_on_a_shift_fires...` (:355) bands the firing minutes 5 to 45 and +5 to 75, stated
as the wander's; the count of two is the claim and holds. `test_the_gate_day_world...` (:252) pins the
book's ten names and `n == 12`.

### test_wind.py (157 lines; 6 tests, 10 cases)

Sound statistical tests; each steps a day or eight hours of a Wind object a second at a time (the
first: 86,400 steps), which costs time in the fast tier (not measured).

### test_world.py (82 lines; 9 tests)

The milestone-1 point ship. **(b)** `test_wind_does_not_die_and_stays_near_base` (:63): `5 < kn <
30` for a 15-knot wind after six hours, and `0 <= direction < 2*pi`, which the wrap makes true of any
value. A wind at a third or twice its base passes. Low, sure.

### test_world_orders.py (1070 lines; 28 tests)

Sound: each world-order channel carried out and refused in words, journaled, replayed; the carrier
chain of a letter in order (:204-249); the hand's hold across promotion. Several tests sail long
inside the fast tier: :218 up to four hours, :995 up to twelve hours, until an event. None is in
`SLOW_TESTS` (not measured).

---

## Cross-file findings

1. **Tests import other tests' private helpers**: test_staying (from test_known_truths), test_tow
   (test_reckoning, test_ground, test_ports), test_the_ship_herself (test_brains, test_crews,
   test_agents), test_visitor_name, test_viewer_action, test_world_orders, and
   tests/browser_plans/worlds.py (test_captive). A rename in one test file breaks others and the
   browser probe. Low.
2. **Module fixtures mutated by their readers** (test_staying, test_via): order dependence that
   `-k` or a reorder exposes. test_tackle_orders shows the safe pattern (a checkpoint, a fresh copy).
3. **Determinism tests compare two runs in one process** (test_standing :1151, test_sun :161,
   test_studding :500, test_strain :660). They cannot catch a dependence on process state.
4. **Data audits that pin lists** (test_tide, test_weather, test_subtypes): high upkeep, and every
   edit is an invitation to re-pin to whatever the data now says.

---

## Faults to plant

1. **test_the_ship_herself.py::test_every_stations_brief_opens_its_situation_with_the_ship.**
   In freesail/agents/harness.py line 1156 change
   `ship="" if self._is_directors else R.ship_words(world),` to
   `ship="" if (self._is_directors or self.station.name == "watcher") else R.ship_words(world),`.
   The name says every station's brief opens with the ship. Prediction: **passes** although the
   watcher is no longer told his ship (the test passes the ship words itself; the harness test
   :147 seats only the officer).
2. **test_via.py::test_an_intent_by_way_of_marks_gives_the_captain_the_legs.** In
   freesail/world/captains.py, `Planner.legs_for` (line 1431): return `[]` at the top when `intent.via` is empty.
   The name and line 131's comment say a plain passage sails the straight line. Prediction:
   **passes** (the `or all(...)` clause is true of an empty list) though a captain with no via has no
   plan.
3. **test_standing.py::test_the_dwell_waits_for_the_evolution_the_firing_started.** In
   freesail/standing/runtime.py, make `_still_working` (line 502) `return False`. The name says the
   dwell waits for the evolution. Prediction: a suspicion it **passes**, if the reef is done within
   301 s, because the only assertion of the waiting is under the `if` at :1229; fails as it should if
   the reef outlasts the dwell.
4. **test_world.py::test_wind_does_not_die_and_stays_near_base.** In the point World's wind set-up
   (freesail/core/world.py line 812, where the Scenario's `wind_speed_kn` is read for the wind), multiply it
   by 0.5. The name says the wind stays near its base. Prediction: **passes** (7.5 knots is inside
   5 to 30); other tests elsewhere may catch it.
5. **test_staying.py::test_turning_truths_the_small_vessels_turn_in_their_own_lengths[cutter-...].**
   Raise the cutter's turning circle by about 20% (in data/ships/cutter.yaml reduce the rudder's
   `area_m2` by a fifth, or in freesail/physics/hull.py scale `rudder_lift_slope` by 0.8 for spans
   under 2 m). The name says the cutter turns in her own lengths as measured (4.9). Prediction:
   **passes** while the circle stays under 6.0 lengths and the swing over 3.5 deg/s.
6. **test_studding.py::test_studding_sails_draw_at_nine_points[schooner].** Make the schooner's
   studding sails never set (in freesail/physics/sails.py `studding_stall`, return 1.0 when the ship's
   rig is a schooner, or remove `studdingsail` sails from topsail-schooner.yaml's "all sail" group).
   Prediction: **reported xfailed, counted as expected**: the strict xfail swallows any failure.

**Faults I believe no test in my files would catch, though a player would:**

1. Reorder the `posts` in data/people/smack.yaml (or lugger.yaml, merchant-brig.yaml,
   sixty-four.yaml) without regenerating the ship file: the ship's posts and the wardroom disagree.
   test_wardroom checks four other ships; the copies of its check that I found cover the bilander,
   the 74, the razee and the Neufchatel's file. Likely uncaught.
2. Give data/ships/seventy-four.yaml (or sixty-four.yaml, razee-44.yaml) no chain pumps: a holed 74
   founders where she should not. test_water checks pumps on seven files only. Likely uncaught by my
   files.
3. A slow test renamed: it moves into the fast tier unmarked and the fast tier slows; nothing fails.
   (Already happened four times; conftest.py:318, :351, :415, :418.)

## What I did not do

- Did not run any test; the predictions above are from reading.
- Did not measure any test's time, so the remarks that long sails sit in the fast tier
  (test_wardroom_doors :642, test_world_orders :218 and :995, test_tackle_orders' `moored_brig`,
  test_wind's day of steps) are suspicions.
- Did not check the parametrised `SLOW_TESTS` ids outside my 26 files against collection (only their
  function names).
- Read the code under test only where named above (the dwell, the reef's durations, the coast hooks,
  the harness's brief call, replay.py's header); did not open test_known_truths.py beyond the lines
  cited.
