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
