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
| A-b5 | test_known_truths.py::test_truth_7_136_a_tack_with_the_guns_served_is_slower_by_exactly_the_hands_it_takes | `Quarters.lend` frees the hands to the tack but each still counts at his gun (guns stay 176 of 176 manned through the tack) | pass | SURVIVED | 14 |
| A-n3 | test_bellerophon.py::test_robbing_on_a_ship_with_no_lower_deck_is_as_it_was, ::test_robbing_by_deck_takes_the_shut_lower_deck_first_and_the_lower_deck_last (2 cases), ::test_robbing_past_every_gun_says_the_marines_last_with_one_and; test_hands.py::test_short_handed_arithmetic; (and 7-136 above) | guns at full crew while the tack takes their hands (the A-b5 plant) | pass | SURVIVED (all) | 20 |
| A-b2 | test_known_truths.py::test_truth_50_at_three_hundred_times_the_log_shows_hourly_rollups_and_every_notable_line | `events.kept` keeps only urgent lines: notable lines rolled up at 300x | pass | SURVIVED | 223 |

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

## A-b5. Truth 7-136: the tack takes the hands and the guns lose none

The reader's fault ("return the lent sailors as freed but leave each at his gun crew") cannot
be planted by leaving `s.at` alone, because the tack's second `hands.request`
(freesail/evolutions/runner.py:1262) takes only men whose `at` is clear. So the men are
cleared for the tack as before and also kept on a list the gun crew counts as its own:

```diff
--- mut/freesail/crew/quarters.py
+++ m/1/freesail/crew/quarters.py
@@ -131,7 +131,7 @@
     @property
     def hands(self) -> list[Sailor]:
         """The men at the gun now: assigned, fit, and not lent to other work."""
-        return [s for s in self.members if s.fit and s.at == self.key]
+        return [s for s in self.members if s.fit and (s.at == self.key or s in self.__dict__.get("_lent", []))]
@@ -363,6 +363,7 @@
                 for s in at[:n]:
                     s.at = None
+                    gc.__dict__.setdefault("_lent", []).append(s)
                     freed.append(s)
@@ -378,6 +379,7 @@
             for s in at:
                 s.at = None
+                gc.__dict__.setdefault("_lent", []).append(s)
                 freed.append(s)
```

Live: a script replaying the test's `tack(True)` (frigate close hauled, guns run out, `sail
before guns`, `tack ship`) counts the hands at the guns 60 s into the tack: pristine 176
before and 92 during, robbed 84, tacked in 376 s; with the fault 176 before and 176 during,
robbed 84, tacked in 376 s. The tack is manned and the battery serves at full rate.

Output: `.  [100%]` (1 passed). SURVIVED. The test asserts the `quarters.robbed` line, its
count (>= 40) and its words, and that the tack is no slower than 1.15 of cleared; nothing
reads the guns' crews or rate during the tack. The name's "slower by exactly the hands it
takes" is not measured: the faulted tack takes exactly as long as the pristine one.

The same fault stands for file 01's "no test would catch" item 3 (A-n3 below).

## A-n3. "The guns firing at full rate while the tack takes their crews"

The A-b5 plant, unchanged. `grep -rn "quarters.robbed\|\.lend(\|hands_at(" tests` finds,
besides 7-136, only the three robbing tests of tests/test_bellerophon.py (1683, 1709, 1745),
which call `q.lend` and read the words of the line; tests/test_hands.py::
test_short_handed_arithmetic was the likeliest by name. All five (with the parametrised pair)
ran: `...........  [100%]`, every one passed. SURVIVED: the claim stands for these; the whole
suite was not run.

## A-b2. Truth 50: notable lines swallowed by the roll-up

```diff
--- mut/freesail/core/events.py
+++ m/1/freesail/core/events.py
@@ -206,7 +206,7 @@
 def kept(e: Event) -> bool:
     """A line the roll-up shows as it is: notable and urgent lines, the captain's and the
     driver's own, and every station's (`STATION_ACTORS`)."""
-    return e.severity is not Severity.ROUTINE or e.actor in KEPT_ACTORS or e.actor in STATION_ACTORS
+    return e.severity is Severity.URGENT or e.actor in KEPT_ACTORS or e.actor in STATION_ACTORS
```

Live: `rollup([notable squall at 10:05, routine line at 10:06], 300, so_far=True)` gives
`['Rollup:2 other entries; 2 routine entries so far.']` with the fault (the squall gone, and
called routine) against `['Event:A squall: the wind veers.', 'Rollup:1 other entry; 1 routine
entry so far.']` pristine.

Output: `.  [100%]` (1 passed, 223 s, nearly all the gate day's fixture). SURVIVED. The test's
oracle is the function under test: `assert lines == [e for e in log if kept(e)]`, and every
other assertion (hours, counts, `sum(r.count) + len(lines) == len(log)`) holds whatever
`kept` lets through. Its second assertion would reject a routine line shown, never a notable
line hidden.
