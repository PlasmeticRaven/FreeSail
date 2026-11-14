# Faults planted, runner 1: known truths (a), known truths (b), view geometry

Faults taken from the `## Faults to plant` sections of `tests-01-known-truths-a.md`,
`tests-02-known-truths-b.md` and `tests-12-view-geometry.md`, in that order, planted one at
a time in the scratch copy `.../scratchpad/m/1` (commit 504a250) and restored from the
pristine copy `.../scratchpad/mut` after each; `diff -r -q` on `freesail/`, `data/` (less
`charts`), `client/` and `tests/` (less `__pycache__`) was clean before every next fault.
Every run was one pytest process, no `-n`. Seconds are wall-clock for the faulted run.

Numbering: A = file 01, B = file 02, G = file 12 (view geometry); "b" = the reader's claim
under (b), "n" = the reader's "no test would catch".

| No. | Test (file::name) | Fault | Baseline | Result | Secs |
|---|---|---|---|---|---|
| A-b1 | test_known_truths.py::test_truth_52_a_low_passing_north_backs_veers_holds_squalls_and_rises_in_that_order | squall never logged as passed (`weather.squall_over` branch deleted) | pass | SURVIVED | 27 |
| A-b3 | test_known_truths.py::test_truth_7_135_the_frigates_broadside_every_minute_and_three_quarters_and_slower_short | long gun's "run out" 18 s to 30 s (85 s nominal to 97) | pass | SURVIVED | 14 |
| A-b4 | test_known_truths.py::test_truth_7b_105_the_smacks_seine_fills_her_well_the_catch_sells_at_falmouth_and_spoils_kept | `price_of` swaps fresh and salted (fresh pilchards sell at the salted £10 not £6) | pass | SURVIVED | 65 |

## A-b1. Truth 52: the squall that never passes

```diff
--- mut/freesail/core/world.py
+++ m/1/freesail/core/world.py
@@ -1932,14 +1932,6 @@
                     "air_mass": wind.air_mass,
                 },
             )
-        else:
-            self.record(
-                Severity.NOTABLE,
-                "weather.squall_over",
-                f"The squall passed; the wind {units.point_name(wind.direction_from)}, "
-                f"{kn:.0f} knots.",
-                data={"knots": round(kn)},
-            )
```

Live: the same seed-7 system day sailed by a script (`World(seed=7,
scenario=the_gate_day_as_a_system())`, `sail_the_system`) logs `squall 2 squall_over 0`
with the fault and `squall 2 squall_over 2` pristine.

Output: `.  [100%]` (1 passed). SURVIVED. The line `assert all(events(world,
"weather.squall_over")), "each squall ends in the log"` (tests/test_known_truths.py:2303)
is `all()` of a list of events, true when the list is empty; it never compares the count
with the squalls.

## A-b3. Truth 7-135: a broadside of two minutes passes for one of a minute and three quarters

```diff
--- mut/freesail/combat/guns.py
+++ m/1/freesail/combat/guns.py
@@ -96,7 +96,7 @@
         ("cartridge", 9.0),
         ("shot", 13.0),
         ("ram", 9.0),
-        ("run out", 18.0),
+        ("run out", 30.0),
         ("prime", 9.0),
         ("point", 14.0),
     ),
```

Live: the test's own helper, `_frigate_interval`, gives full 122.1 s, short 183.2 s with the
fault; full 104.1 s, short 159.5 s pristine.

Output: `.  [100%]` (1 passed). SURVIVED. The bands `90.0 <= full <= 125.0` and
`140.0 <= short <= 210.0` hold a full-company broadside of 2 min 2 s, a sixth slower than
the minute and three quarters (105 s) the name promises. The reader's predicted figures
(119 s, 181 s) were close.

## A-b4. Truth 7b-105: fresh fish sold at the salted price

```diff
--- mut/freesail/world/fishing.py
+++ m/1/freesail/world/fishing.py
@@ -614,7 +614,7 @@
 
 def price_of(fish: str, salted: bool) -> float:
     price = fish_spec(fish).get("price") or {}
-    return float(price.get("salted" if salted else "fresh", 0.0))
+    return float(price.get("fresh" if salted else "salted", 0.0))
```

Live: `F.price_of('pilchards', False)` returns 10.0 with the fault (data/fishing/fish.yaml:38
has `price: {fresh: 6, salted: 10}`); mackerel 10.0 against its fresh 9.

Output: `.  [100%]` (1 passed). SURVIVED. The expectation is
`worth = sum(F.price_of(f, False) * t ...)` (tests/test_known_truths.py, in the test body),
the same function the sale calls, so the test checks the sale against itself; it does not
pin a figure from the data, and it applies no market factor of its own.
