# Faults planted, runner 2 (tests-03, tests-04, tests-05)

Scratch copy `.../scratchpad/m/2` of 504a250; each fault planted alone, the file restored
from `.../scratchpad/mut` after it and the copy checked pristine (`diff -r -q`, caches
excluded) before the next. Every test run by node id, `-x`, no `-n`. Seconds are wall time of
the pytest run with the fault planted.

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 03-1 | test_agent_api.py::test_the_long_poll_waits_without_holding_the_worlds_lock | long poll's 120 s cap removed | pass | SURVIVED | 7.3 |
| 03-2 | test_anchor.py::test_she_drags_in_a_gale_on_short_scope_and_a_standing_order_sees_it | "dragging;" dropped from the anchor reading's words | pass | KILLED | 8.6 |
| 03-3 | test_anchor.py::test_every_ship_carries_ground_tackle_by_her_size_from_the_generator[data/ships/brig.yaml] | brig's best bower 800 kg to 1 kg | pass | SURVIVED | 6.7 |
| 03-4 | test_bilander.py::test_her_burthen_by_the_old_measure_is_about_130_tons | bilander's beam 5.91 m to 6.5 m | pass | SURVIVED | 0.9 |
| 03-5 | test_boat_director.py::test_the_boat_lost_by_the_directors_word_and_doubted_on_a_smooth_sea | `plausible_when` of `boat_swamped` deleted | pass | SURVIVED | 9.7 |
| 03-6 | test_brains.py::test_the_perception_is_from_her_own_truth_and_sees_the_player_by_the_horizon | every sail in sight made out whole (`level = 3`) | pass | SURVIVED | 14.5 |

## 03-1: the long poll's cap

```diff
-        wait = max(0.0, min(float(wait or 0.0), TURNS_WAIT_MAX_S))
+        wait = max(0.0, float(wait or 0.0))
```
(`freesail/agents/remote.py:886`.) Live: with `remote.time` replaced by a clock that moves ten
seconds a call, `g.turns(wait=600)` on the test's own `Game` held the poll open 610 fake
seconds with the fault and 130 without it. Output: `.  [100%]`, 1 passed. The test asks only
that `TURNS_WAIT_MAX_S == 120` (the constant), never that a wait above it is cut down. SURVIVED.

## 03-2: "dragging" in the anchor's reading

```diff
         words = f"down, {how.rstrip('.')}, {riding.scope_fathoms:.0f} fathoms out"
-        if riding.dragging:
-            words = f"dragging; {words}"
```
(`freesail/api/readings.py:2215-2216`.) Output:
```
>       assert fired, "the standing order on the anchor's reading did not fire"
E       AssertionError: the standing order on the anchor's reading did not fire
tests/test_anchor.py:204: AssertionError
```
KILLED: the standing order `when the anchor is dragging` reads the words, so it no longer
fires. The reader's prediction ("likely passes") is refuted. (The line the reader pointed at,
:207, would indeed not have caught it: its `or anchor.scope_fathoms >= 20.0` is always true.)

## 03-3: the brig's anchor a kilogram

```diff
   - id: best_bower
     kind: bower
     name: the best bower
-    weight_kg: 800.0
+    weight_kg: 1.0
```
(`data/ships/brig.yaml:1892`.) Live: `ground_tackle(road_world(BRIG).ship).get("best_bower").weight_kg`
gives 1.0. Output: 1 passed. Only `weight_kg > 0` is asked of any ship but the frigate. SURVIVED.

## 03-4: the bilander's burthen

```diff
-  beam_m: 5.91
+  beam_m: 6.5
```
(`data/ships/bilander.yaml:43`.) Live: the neighbouring
`test_bilander.py::test_her_hull_holds_chapman_and_lloyds` fails at :150
(`Expected: 5.91 ± 0.1`). The named test: 1 passed in 0.9 s. It is arithmetic on literals
(b = 19.4 and two lengths written in the test) and calls no project code, so no fault in the
ship can reach it. SURVIVED (the fault itself is caught by another test).

## 03-5: the swamped boat on a smooth sea

```diff
     effect: {boat_lost: swamped}
-    plausible_when: {sea_above: ["smooth", "a smooth sea", "calm", "slight", "a slight sea"]}
     doubt: "the sea is too slight to swamp a boat alongside"
```
(`data/director/aboard.yaml:342`.) Live: `D.direct(w, "aboard: the boat swamped")` in the
test's Carrick Road world answers "Done: found aboard: The boat swamped alongside..." with the
fault and "Doubted, not performed: the sea is too slight..." without it. Output: 1 passed. The
test's `if said.startswith("Doubted"):` takes either answer. SURVIVED.

## 03-6: every sail made out whole at any range

```diff
-            level, _ = o.made_out(distance, glass=(o.id == glass_for))
+            level = 3
```
(`freesail/world/ships.py:1983`, in `Vessels.strangers_of`, which `brains.perceive_vessel`
calls at `freesail/world/brains.py:143`.) Live: a second French brig put 15.2 km from the
test's near brig is perceived as `made_out 3`, "a merchant brig, deep laden ... French colours"
with the fault, and `made_out 0`, "a sail", without it. Output: 1 passed. The test's far brig is
fifty miles off and never in sight, so the closing assertion (`"Y" not in ids or ...`) cannot
fail. SURVIVED.

## tests-03, the faults its reader said no test would catch

| # | Tests run | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 03-A | five of test_aboard_another.py (below) | a player's seat on a hull not his own refused every line | pass | SURVIVED (all five) | 12.5 to 47.1 each |
| 03-B | four (below) | `boat_swamped` without `plausible_when` (fault 03-5 again) | pass | SURVIVED (all four) | 1.2 to 8.8 each |
| 03-C | test_ship_particulars.py::test_generator_reproduces_the_committed_files; test_bilander.py::test_the_generator_writes_her_file_as_committed_and_reports_its_checks | the generator's bowers at a tenth (then at half) of the rule | pass | KILLED | 1.5 / 0.8; 4.7 |

### 03-A: the seat aboard another hull can never order

`freesail/agents/seat.py`, `PlayerSeat.route`:
```diff
         line = " ".join(str(text).split())
         low = line.lower()
+        _w = getattr(self.world, "world", None)
+        if _w is not None and getattr(_w, "players", None) is not None and self.world is not _w.players:
+            return self._refused(line, f"The {self.station.name} has not the authority. {line!r} not carried out.")
```
Live: on the test's `aboard_x()` world, `seat_player(w, "officer").route("set the royals")` gives
`agent.refused ... has not the authority`. Run, all passed: test_aboard_another.py
`::test_the_players_seat_on_another_ship_is_hers_and_stays_when_the_drivers_move_on` (12.5 s),
`::test_the_seat_goes_with_its_person_by_the_boat_and_replays` (47.1 s),
`::test_the_player_aboard_another_ship_has_her_prompt_and_his_own_is_left_as_she_lies` (14.8 s),
`::test_the_station_kept_on_the_players_ship_by_her_name_reads_the_players_vessel` (12.6 s),
`::test_the_player_aboard_another_ship_replays_by_his_acts_to_the_same_digests` (19.5 s).
(`grep '\.route(' tests/` finds no other test that seats the player on a hull not his own.)
Worse than the reader said: on the pristine code the same call is refused too (`agent.refused:
The officer of the watch has not the deck (the captain has it)`), so the one `route` call on
another hull, :233-234, cannot tell a working seat from a dead one: no test in the suite shows
a seated player on another hull ever carrying out an order. SURVIVED.

### 03-B: the swamped boat on a smooth sea

The fault of 03-5, planted again. Tests chosen by `grep -n "boat_swamped\|plausible_when" tests/`:
test_boat_hull.py::test_the_boat_swamped_loses_her_people_and_the_ship_says_so,
test_aboard_found.py::test_every_thing_of_the_table_is_read_and_each_form_finds_its_own_thing,
`::test_every_condition_must_hold_and_the_new_ones_read_the_ship`,
`::test_a_key_the_game_does_not_know_is_the_tables_mistake_said_at_the_load`. All passed. No
test asks that a thing with a `doubt` has a `plausible_when` for it to be doubted by. SURVIVED.

### 03-C: the generator's anchors out of proportion

`tools/gen_ships.py:501`, first `/ 100.0` to `/ 1000.0` (the bowers a tenth):
```diff
-    bower_cwt = round(BOWER_CWT_PER_100_TONS * burthen / 100.0, 1)
+    bower_cwt = round(BOWER_CWT_PER_100_TONS * burthen / 1000.0, 1)
```
The generator then stops: `ShipFileError: rating pass: anchor 'kedge' has weight_kg of nothing.`
(both tests fail on it). Planted milder, `/ 200.0` (the bowers at half), so that the files are
written: test_ship_particulars.py::test_generator_reproduces_the_committed_files fails at :590
(`assert '# The biland...' == '# The biland...'`, the bowers' note differs). KILLED: the reader
did not have the regenerate-and-compare test in his files; it holds every committed ship file
to the generator byte for byte. Tried also against the hand edits of 03-3 (the brig's bower at
1 kg) and 03-4 (the bilander's beam at 6.5 m): it fails on each at :590 (4.2 s, 3.4 s). So the
data faults of 03-3 and 03-4 survive their named tests but not the suite; a change made in the
generator and the data together (regenerated and committed) would pass this test and 03-3's.
