# Faults planted: runner 4 (tests-09, tests-10, tests-11)

Scratch copy `.../scratchpad/m/4`, pristine `.../scratchpad/mut`, both at 504a250. Every run
was `timeout 900 python3 -m pytest -q -p no:cacheprovider -x <node id>` from inside the
scratch copy, one process at a time. The project's `addopts` adds a second `-q`, so a pass
prints only its dots; the exit code (rc) and the wall-clock seconds are given for each run.
After each fault the file was copied back from the pristine copy and `diff -r -q` over
`freesail/`, `data/` (less `charts`) and `tests/` came back empty before the next.

Liveness checks (the "is the fault live" one-liners) were run as `PYTHONPATH=. python3
<script>` from the scratch copy: without `PYTHONPATH=.` a script outside the tree imports a
different `freesail` (an installed copy), which I found once (fault 9-1) and corrected.

## Table

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 9-1 | test_powder_orders.py::test_each_quantity_is_cut_to_what_the_magazine_wants_and_says_so | `Magazine.wanting` barrels rounded down | pass (5 s) | SURVIVED | 5 |
| 9-2 | test_practice_orders.py::test_the_loaded_guns_keep_their_charges_in_the_answer | `begin_exercise` never names a loaded gun | pass (7 s) | SURVIVED | 6 |
| 9-3 | test_primer.py::test_every_form_in_the_forms_tables_is_taken (the 5 chapter-13 `veer` ids) | every `veer` refused in words | pass (16 s) | SURVIVED | 27 |
| 9-4 | test_prize_scenarios.py::test_the_prize_home_scenario_begins_with_the_brig_a_prize_in_company_and_the_truth_shows_her | director's truth loses `prisoners` | pass (33 s) | SURVIVED | 36 |
| 9-5 | test_reckoning.py::test_the_cast_is_reduced_by_the_masters_own_tide_and_the_line_says_it | tide reduction said under a fathom too | pass (11 s) | SURVIVED | 15 |
| 9-6 | test_ports.py::test_the_pilot_of_brest_takes_her_through_the_goulet_on_the_truth_from_his_station | pilot's named-danger warning never logged | pass (14 s) | SURVIVED | 14 |
| 9-N1 | (no test claimed) test_known_truths.py::test_truth_7_169_the_long_tom_fires_on_when_the_carronades_filled_cartridges_are_spent | `Battery.tick` never trains the pivots | pass (8 s) | KILLED | 11 |
| 9-N2 | (no test claimed) test_magazine.py::test_receive_wanting_and_spoil_go_by_kind_and_the_wanting_is_to_the_nearest_barrel | as 9-1 | pass (1 s) | KILLED | 0 |
| 9-N3a | (no test claimed) test_known_truths.py::test_truth_7_155_the_squadron_keeps_its_line_at_far_detail_and_through_the_promotion | `keep your station` dropped from the vocabulary | pass (76 s, see note) | KILLED | 71 |
| 9-N3b | (no test claimed) 4 tests, see section | chapter 24's `the order of sailing` reading gives the order reversed | not run (see section) | SURVIVED | 64 |

## tests-09

### 9-1 SURVIVED

```diff
--- mut/freesail/ship/parts.py
+++ freesail/ship/parts.py
@@ -1009,7 +1009,7 @@
-        return Wanting(deficit, int((deficit + BARREL_LB / 2.0) // BARREL_LB), shot)
+        return Wanting(deficit, int(deficit // BARREL_LB), shot)
```

Live: a real `Magazine` short by 99 lb gives `Wanting(powder_lb=99.0, barrels=0, shot={})`
under the fault. The named test passed (rc=0, 5 s): its magazine is a `FakeMagazine`
(tests/test_ordnance.py:71) whose own `wanting` (:80-91) overrides the one planted in. The
reader's claim stands. See 9-N2: another file catches it.

### 9-2 SURVIVED

```diff
--- mut/freesail/combat/guns.py
+++ freesail/combat/guns.py
@@ -391,8 +391,6 @@
             self.services[g.id] = Service()
-            if g.loaded:
-                loaded.append(g.name)
         return loaded
```

Named test rc=0 (6 s): it monkeypatches `Battery.begin_exercise` with `_begin(names)`
(tests/test_practice_orders.py:467, :475, :481-486), so the real method is never called.
Live: tests/test_dumb_show.py::test_a_loaded_gun_is_exercised_from_the_run_out_to_the_point_and_keeps_its_charge
fails under the same fault:

```
>       assert sorted(named) == ["No. 1 starboard gun", "No. 2 starboard gun", "No. 3 starboard gun"]
E       AssertionError: assert [] == ['No. 1 starb...tarboard gun']
tests/test_dumb_show.py:160: AssertionError
```

So the claim about the named test stands, and the suite as a whole catches it.

### 9-3 SURVIVED

The unparametrised node id is 1,095 cases; the whole was still running at ten minutes, so I
stopped it and ran the five ids that the fault touches, `-k "forms_tables_is_taken and
veer and not wind"`: `13: veer cable`, `13: veer away`, `13: veer twenty fathoms`,
`13: veer to ninety fathoms`, `13: veer the small bower to ninety fathoms`. The `if` is at
line 248 of the commit, not 247 as the reader wrote.

```diff
--- mut/freesail/orders/ground_tackle.py
+++ freesail/orders/ground_tackle.py
@@ -245,7 +245,7 @@
         if verb == "veer cable":
             if fathoms is not None and said_to:
                 params["to"] = True
-            if left or (fathoms is None and said_to):
+            if True:
```

Live (frigate of test_primer's `make_ship`):

```
veer cable -> OrderError Veer how much? Say 'veer twenty fathoms', 'veer to ninety fathoms' or 'veer cable'.
veer twenty fathoms -> OrderError '' was not understood after 'veer'. Say 'veer twenty fathoms', ...
```

The five ids passed (rc=0, 27 s, `.....`): the test returns on any `OrderError` whose words
lack "was understood, but not" and "takes nothing after it" (tests/test_primer.py:598-602),
and neither refusal has them. Every `veer` order in the game refused, and the test of "every
form is taken" is green. The reader's claim stands. (Note for the reviewer: the full
1,095-case node id takes over ten minutes and is one test function.)

### 9-4 SURVIVED

```diff
--- mut/freesail/api/readings.py
+++ freesail/api/readings.py
@@ -4248,8 +4248,6 @@
     if prizes:
         out["prizes"] = prizes
-    if prisoners:
-        out["prisoners"] = prisoners
```

Named test rc=0 (36 s). Its check is
`assert any("Deux Frères" in row for row in truth.get("prisoners", [])) or rec["prisoners"]`
(tests/test_prize_scenarios.py:58): the `or rec["prisoners"]` makes it true whatever the
truth shows. Live, and as the reader predicted, the next test in the file fails:

```
>       assert any("Captain Bowen (given)" in row for row in truth["prisoners"])
E       KeyError: 'prisoners'
tests/test_prize_scenarios.py:94: KeyError
```

### 9-5 SURVIVED

```diff
--- mut/freesail/world/reckoning.py
+++ freesail/world/reckoning.py
@@ -3090,7 +3090,7 @@
         text = f"{chant(fathoms, not deep)}; {ground}."
-        if allowed_m >= units.fathoms_to_m(1.0):
+        if allowed_m >= 0.0:
```

Named test rc=0 (15 s). Its under-a-fathom check is under
`if low.navigation._tide_allowance_m() < units.fathoms_to_m(1.0):` (tests/test_reckoning.py:2618);
at the moment it picks (20 June 1805 13:00) the allowance is 2.43 m against a fathom of
1.83 m, so the branch is never entered and nothing is asserted. Live: at 20 June 14:00 the
allowance is 1.61 m and the cast under the fault reads "Quarter less ten; loose sand, not
very tenacious. One fathom of tide allowed by the epitome: nine fathoms on the chart." The
reader's claim stands; the test's guard has a date that never meets its condition.

### 9-6 SURVIVED

```diff
--- mut/freesail/world/dealings.py
+++ freesail/world/dealings.py
@@ -1037,12 +1037,6 @@
-            self._record(
-                Severity.URGENT,
-                "port.pilot_warns",
-                text,
-                {"port": port.id, "danger": f.id, "deeper": deeper, "thick": thick},
-            )
             return
```

Named test rc=0 (14 s): `assert all("the Mingan" in t ... for t in warned)` holds over an
empty list (tests/test_ports.py:1656-1657). Live: test_the_pilot_warns_of_a_danger_ahead_by_name_in_time_to_act fails:

```
>       assert len(rock) == 1 and rock[0].severity is Severity.URGENT
E       assert (0 == 1)
tests/test_ports.py:1469: AssertionError
```

### 9-N1 KILLED (the reader's "no test would catch" refuted)

```diff
--- mut/freesail/combat/guns.py
+++ freesail/combat/guns.py
@@ -501,7 +501,6 @@
             for g in active:
                 self._work(g, dt / factor, mag, tick)
-        self._train_pivots(dt, quarters, firer, target)
         self._fire(quarters, firer, target, rng, tick, resolve, mag)
```

Grep of the tests for `_train_pivots`, pivot and long Tom: test_pivot_gun.py drives
`_train_pivots` by hand, as the reader said; but truth 7-169 sails the privateer at
quarters through `Battery.tick` and catches it (baseline pass, 8 s):

```
>       assert pivot.fired >= 10  # 25 at seed 7
E       AssertionError: assert 0 >= 10
tests/test_known_truths.py:9982: AssertionError
```

### 9-N2 KILLED (refuted, in a file the reader did not hold)

Same diff as 9-1. tests/test_magazine.py builds a real `Magazine` (grep for `.wanting()`
and `.barrels`); baseline pass (1 s); under the fault:

```
>       assert w.powder_lb == 60.0 and w.barrels == 1  # sixty pounds: the nearest barrel
E       AssertionError: assert (60.0 == 60.0 and 0 == 1)
tests/test_magazine.py:336: AssertionError
```

### 9-N3: the chapter 19 and 24 `orders` blocks

The blocks are not run: tests/test_primer.py:84-110 `CHAPTERS` lists neither
`19-the-wardroom.md` nor `24-the-squadron.md` (nor 13, 21, 22, 25, 27). That part of the
claim is sure. A wording fault in a block would mean editing `docs/primer`, which is the
shared copy and never edited, so I planted faults in the code behind two orders that
chapter 24's block shows.

**First attempt, dead and discarded.** I removed `"your station"` from the tuple at
freesail/orders/station.py:102. It changes nothing: `keep your station` is a synonym in
data/vocabulary.yaml:901 and reaches `_parse` with no object. Truth 7-155 passed (76 s)
under that dead edit, which serves as its baseline.

**9-N3a KILLED.**

```diff
--- mut/data/vocabulary.yaml
+++ data/vocabulary.yaml
@@ -898,7 +898,7 @@
   keep station:
-    synonyms: [keep your station, keep her station, take station, take your station,
+    synonyms: [keep her station, take station, take your station,
```

Live: `keep your station` raises `UnknownVerbError: 'keep your station' is not an order this
ship understands; did you mean 'take your station', ...`. Caught, not by any primer test,
but because the `in company` captain's book gives exactly those words
(freesail/world/captains.py:2963):

```
>       assert max(_off_station_m(w, sq).values()) <= 1.5 * units.CABLE, _off_station_m(w, sq)
E       AssertionError: {'nimble': 6526.381687905378, 'sparrow': 5448.528765564996}
tests/test_known_truths.py:9165: AssertionError
```

A finding on the way: captains.py:2962-2965 wraps that `give` in `except Exception: pass`,
so the captain's refused order is silent; only the distance off station shows it.

**9-N3b SURVIVED.**

```diff
--- mut/freesail/api/squadron_readings.py
+++ freesail/api/squadron_readings.py
@@ -149,7 +149,7 @@
     root = _root(world)
-    order = [_name_of(root, m) for m in sq.members]
+    order = [_name_of(root, m) for m in reversed(sq.members)]
```

Live (test_squadrons' `convoy_world` with the player's ship put in the set): "order of
sailing, two cables apart: M4, M3, M2, M1, M0, Harpy, Amazon", where the members run
Amazon, Harpy, M0 ... M4. No test reads any of the four squadron readings (`the squadron`,
`the convoy`, `the order of sailing`, `the station`): grep of tests/ for their ids and
words finds none. Run under the fault, all rc=0: test_agents.py::test_readings_tool_reads_the_registry_and_nothing_else
(4 s), test_squadrons.py::test_the_set_writes_the_relation_on_every_member_and_clears_it_when_she_leaves
(12 s), ::test_the_line_ahead_and_the_line_abreast_lay_the_members_by_the_interval (10 s),
::test_the_convoy_forms_in_the_order_of_sailing_and_keeps_it_at_the_slowest_ships_pace
(38 s). I did not run their baselines (each passed with the fault in, so a baseline adds
nothing).

