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

## Table (tests-09; the tables of tests-10 and tests-11 head their own sections)

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

## tests-10

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 10-1 | test_sea.py::test_the_log_says_the_sea_when_its_words_change_and_the_rollup_says_it_by_the_hour | hourly line's `data["sea"]` is the motion's words | pass (5 s) | SURVIVED | 4 |
| 10-2 | test_sail_by_name.py::test_the_bearing_and_the_distance_pick_the_far_sail_on_the_same_bearing | `give chase` drops the `distant` clause | pass (7 s) | SURVIVED | 7 |
| 10-3 | test_rig_geometry.py::test_close_hauled_forces_are_unchanged_without_bowlines | lift x1.1 on the no-bowline path | pass (1 s) | SURVIVED | 1 |
| 10-4 | test_routine.py::test_three_calls_in_the_middle_watch_leave_the_morning_watch_tired | `FATIGUE_WEIGHT` 0.5 to 0.9 | pass (3 s) | SURVIVED | 2 |
| 10-5 | test_server.py::test_the_server_takes_the_ease_on_station_flag | `ease_on_station=args.ease_on_station and False` | pass (1 s) | SURVIVED | 1 |
| 10-6 | test_squadrons.py::test_the_business_draws_a_convoy_a_blockade_and_a_ship_in_ordinary_by_the_nations_knobs | a ship at anchor drifts 5 m east a step | pass (25 s) | SURVIVED | 24 |
| 10-A | (no test claimed) test_known_truths.py::test_truth_56_a_gale_of_a_day_raises_a_heavy_sea_the_reef_is_slower_in_and_that_outlasts_it | as 10-1 | not run (see section) | KILLED | 185 |
| 10-B | (no test claimed) 3 tests in test_ships.py, see section | as 10-2 | not run | SURVIVED | 43 |
| 10-C | (no test claimed) test_hands.py::test_crew_factor_for_the_rating_table | `- FATIGUE_FRESH` dropped at hands.py:426 | pass (1 s) | KILLED | 1 |

### 10-1 SURVIVED (named test); KILLED elsewhere (10-A)

```diff
--- mut/freesail/core/world.py
+++ freesail/core/world.py
@@ -1852,7 +1852,7 @@
         if self.sea is not None:
             # the sea by the hour (spec M5 §4), for the roll-up
-            data["sea"] = self.sea.words
+            data["sea"] = self.motion.words
```

Named test rc=0 (4 s). Its check is `assert all(e.data["sea"] == e.data["sea"] and "sea" in
e.text for e in hours)` (tests/test_sea.py:636): the field compared with itself. The reader's
claim stands for this test.

**10-A.** The reader's "no test in my files" holds, but the suite catches it in a slow truth
(grep of the tests for `data["sea"]` found tests/test_known_truths.py:2574):

```
>       assert nine.data["sea"] == "a heavy sea" and "a heavy sea" in nine.text
E       AssertionError: assert ('pitching hea...der her stern' == 'a heavy sea'
```

185 s. I did not run its baseline (another three minutes); the assertion that failed reads
exactly the field planted, so the failure is the fault's.

### 10-2 SURVIVED; 10-B SURVIVED

```diff
--- mut/freesail/orders/navigation.py
+++ freesail/orders/navigation.py
@@ -1654,7 +1654,7 @@
     if verb == "give chase":
         world = _world_with_lookout(ship)
-        which = _sail_and_rest(order.verb_phrase, rest)
+        which = _sail_and_rest(order.verb_phrase, rest.split(" distant")[0])
```

Named test rc=0 (7 s). Live, `give chase to the brig bearing NE distant two miles` on the
test's own `sails_about()`:

```
fault:    Gave chase to a brig-sloop of war on the starboard bow, bearing NE. Helm ordered: steer NE (48°).
pristine: Gave chase to a brig on the starboard bow, bearing NE. Helm ordered: steer NE (48°).
```

She chases the Raven, not the Wasp. In both runs `world.ship.extra.get("chase")` is `None`,
so line 164's `.get("id", "wasp")` is true whatever is chased: that check can never fail.
Line 163 asks only for "bearing NE". The reader's claim stands.

**10-B.** Grep of the tests for `give chase` with a distance finds only this test. The other
submitters of `give chase` (tests/test_ships.py::test_make_her_out_sends_a_glass_aloft_and_give_chase_puts_the_helm_for_her_bearing,
::test_a_chase_through_the_winds_wake_wears_her_and_does_not_leave_the_yards_braced,
::test_a_chase_through_the_winds_eye_puts_her_about_and_a_small_alteration_is_steered)
pass under the fault (rc=0; 10, 17, 16 s); they give the bare order, so the fault cannot touch
them. No test catches the wrong ship chased.

### 10-3 SURVIVED (named test); caught next door

```diff
--- mut/freesail/physics/sails.py
+++ freesail/physics/sails.py
@@ -206,7 +206,7 @@
         if luff_gain <= 0.0 or a >= peak:
-            return c_l, c_d
+            return c_l * 1.1, c_d
```

Named test rc=0 (1 s): it compares two calls that take the same branch. As predicted,
tests/test_sails.py::test_curves_interpolate_and_fold fails (baseline pass, 1 s):

```
>       assert cl == pytest.approx(1.12) and 0.45 <= cd <= 0.55
E       assert (1.2320000000000002 == 1.12 ± 1.1e-06
tests/test_sails.py:93: AssertionError
```

### 10-4 SURVIVED (named test); caught next door

```diff
--- mut/freesail/crew/hands.py
+++ freesail/crew/hands.py
@@ -47,7 +47,7 @@
-FATIGUE_WEIGHT = 0.5
+FATIGUE_WEIGHT = 0.9
```

Named test rc=0 (2 s): it uses its own `FATIGUE_WEIGHT = 0.5` (tests/test_routine.py:36,
:486) and never calls the code's. Live: tests/test_hands.py::test_crew_factor_for_the_rating_table
fails (baseline pass, 1 s):

```
>       assert factor_for(ORD, ORD, fatigue=0.3) == pytest.approx(1.125)  # 0.05 of it is 'fresh'
E       assert 1.225 == 1.125 ± 1.1e-06
```

(Its next assertion, at :272-274, checks fatigue 1.0 against `hands.FATIGUE_WEIGHT` itself
and would pass under any weight.)

### 10-5 SURVIVED

```diff
--- mut/freesail/ui/server.py
+++ freesail/ui/server.py
@@ -1857,7 +1857,7 @@
-        ease_on_station=args.ease_on_station,
+        ease_on_station=args.ease_on_station and False,
```

Named test rc=0 (1 s): it asserts the substring `ease_on_station=args.ease_on_station` in
`inspect.getsource(server.main)` (tests/test_server.py:685-686), which the fault keeps.
Liveness is by reading only: `x and False` is always false, so the driver never eases; I did
not start `main()` (it serves). The flag is dead and the test is green.

### 10-6 SURVIVED

```diff
--- mut/freesail/world/ships.py
+++ freesail/world/ships.py
@@ -898,6 +898,8 @@
             self.speed_kn = 0.0
             self.tack = 0.0
+            from freesail.world.geo import destination
+            self.position = destination(self.position, 90.0, 5.0)
             return
```

Named test rc=0 (24 s). Live: the test's body run with the hulk's position taken before
`w.run(1800)` shows "hulk moved m: 150.0000000149308" (the far-detail step comes 30 times
in the half hour). The check `hulk.position == hulk.position` (tests/test_squadrons.py:530)
is true of any position. The reader's claim stands.

### 10-C KILLED (the reader's "test_routine's band would still pass" is right; the suite catches it)

```diff
--- mut/freesail/crew/hands.py
+++ freesail/crew/hands.py
@@ -423,7 +423,7 @@
-    fatigue = 1.0 + FATIGUE_WEIGHT * max(0.0, mean_fatigue - FATIGUE_FRESH)
+    fatigue = 1.0 + FATIGUE_WEIGHT * max(0.0, mean_fatigue)
```

test_routine's named test passes (rc=0, 2 s). tests/test_hands.py::test_crew_factor_for_the_rating_table fails:

```
>       assert factor_for(ORD, ORD, fatigue=0.3) == pytest.approx(1.125)  # 0.05 of it is 'fresh'
E       assert 1.15 == 1.125 ± 1.1e-06
```

## tests-11

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 11-1 | test_the_ship_herself.py::test_every_stations_brief_opens_its_situation_with_the_ship | the watcher's brief not told his ship | pass (23 s) | SURVIVED | 24 |
| 11-2 | test_via.py::test_an_intent_by_way_of_marks_gives_the_captain_the_legs | `legs_for` returns `[]` with no via | pass (8 s) | SURVIVED | 8 |
| 11-3 | test_standing.py::test_the_dwell_waits_for_the_evolution_the_firing_started | `_still_working` returns False | pass (7 s) | KILLED | 4 |
| 11-4 | test_world.py::test_wind_does_not_die_and_stays_near_base | the scenario's wind halved at set-up | pass (2 s) | SURVIVED | 3 |
| 11-5 | test_staying.py::test_turning_truths_the_small_vessels_turn_in_their_own_lengths[cutter-band1-fastest_band1] | cutter's rudder 1.2 to 0.96 m², and to 0.85 m² | pass (3 s) | SURVIVED (both) | 3 + 3 |
| 11-6 | test_studding.py::test_studding_sails_draw_at_nine_points[schooner] | the schooner's studding sails always stalled | **xfailed** (5 s) | SURVIVED (xfailed again) | 5 |
| 11-N1a | (no test claimed) test_indefatigable.py::test_her_ship_files_posts_and_people_agree_with_her_wardroom_files[data/ships/sixty-four.yaml] | the 64's first two posts swapped in data/people | pass (1 s) | KILLED | 1 |
| 11-N1b | (no test claimed) test_ship_particulars.py::test_generator_reproduces_the_committed_files | the smack's two posts swapped in data/people | pass (2 s) | KILLED | 3 |
| 11-N2 | (no test claimed) test_bellerophon.py::test_her_boats_pumps_hold_and_stores | the 74's four chain pumps removed | pass (1 s) | KILLED | 2 |
| 11-N3 | (no test claimed) a slow test renamed into the fast tier | not a fault in the game | n/a | NOT RUN | - |

### 11-1 SURVIVED

```diff
--- mut/freesail/agents/harness.py
+++ freesail/agents/harness.py
@@ -1153,7 +1153,7 @@
-            ship="" if self._is_directors else R.ship_words(world),
+            ship="" if (self._is_directors or self.station.name == "watcher") else R.ship_words(world),
```

Named test rc=0 (24 s): it builds the brief itself with `ship=R.ship_words(w)`
(tests/test_the_ship_herself.py:124-132), so the harness's choice is never exercised. Live,
the watcher seated by the harness (`stationed(w, ..., st=agent.watcher(world=w))`, the helper
of :150):

```
fault:    watcher situation starts: The last 8 lines of the log:   Morning watch, 4 bells (06:00) ...
pristine: watcher situation starts: The ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class, ship-rigged; ...
```

The reader's claim stands.

### 11-2 SURVIVED

```diff
--- mut/freesail/world/captains.py
+++ freesail/world/captains.py
@@ -1429,6 +1429,8 @@
     def legs_for(self, intent: Intent, start: Position, departing: str = "") -> list[Leg]:
+        if not intent.via:
+            return []
```

Named test rc=0 (8 s): `assert [lg.kind for lg in plain] == ["to"] or all(lg.kind != "via"
for lg in plain)` (tests/test_via.py:132) is true of `[]`. Live: tests/test_captains.py::test_the_planner_joins_the_ports_tracks_and_the_common_track_by_the_iroise
fails (baseline pass, 8 s):

```
>       assert words[:3] == ["Falmouth outer road", "50 00 N 4 57 W", "49 52 N 5 06 W"]
E       AssertionError: assert [] == ['Falmouth ou... 52 N 5 06 W']
```

The claim about the named test stands; the suite catches the fault elsewhere.

### 11-3 KILLED (the reader's suspicion refuted)

```diff
--- mut/freesail/standing/runtime.py
+++ freesail/standing/runtime.py
@@ -500,6 +500,7 @@
     def _still_working(self, rule: Rule) -> bool:
+        return False
```

The reef outlasts the dwell at seed 7, so the guarded assertion is reached:

```
>           assert not rule.armed, "the reef still in hand: not yet re-armed"
E           AssertionError: the reef still in hand: not yet re-armed
```

The test is conditional (tests/test_standing.py:1229) and would go blind if the reef were
ever made quicker than 301 s, but as it stands it catches the fault.

### 11-4 SURVIVED

```diff
--- mut/freesail/core/world.py
+++ freesail/core/world.py
@@ -809,7 +809,7 @@
         wind_params = WindParams.from_nautical(
             self.scenario.wind_from_deg,
-            self.scenario.wind_speed_kn,
+            self.scenario.wind_speed_kn * 0.5,
```

Named test rc=0 (3 s). Live: the test's own world after six hours, 8.48 kn under the fault
against 16.97 kn pristine. Its band `5 < kn < 30` (tests/test_world.py:67) for a 15-knot base
holds both. I did not look for other tests that would catch it.

### 11-5 SURVIVED

```diff
--- mut/data/ships/cutter.yaml
+++ data/ships/cutter.yaml
@@ -79,7 +79,7 @@
   rudder:
-    area_m2: 1.2
+    area_m2: 0.96
```

and a second run at `area_m2: 0.85`. Measured with the test's own `turning_circle`:

| rudder m² | circle (lengths) | swing (deg/s) | circle change |
|---|---|---|---|
| 1.2 (pristine) | 4.93 | 4.97 | |
| 0.96 (a fifth less, as the reader said) | 5.59 | 4.33 | +13% |
| 0.85 | 5.99 | 3.99 | +21% |

Both runs rc=0 (3 s each): the band is 3.5 to 6.0 lengths and 3.5 to 7.0 deg/s
(tests/test_staying.py:116). At 0.96 m² test_the_cutter_swings_twice_as_fast_as_the_frigate
also passed (5 s). A circle grown by a fifth passes; the band is about 20% wide above the
measured figure. Not run: tests/test_ship_particulars.py::test_generator_reproduces_the_committed_files,
which would fail on any hand edit of a ship file (see 11-N1b and 11-N2) but says nothing of
turning; the same fault made in the generator's source would pass it.

### 11-6 SURVIVED (and the baseline does not pass)

Baseline: the test is **xfailed** before any fault (`XFAIL ... the schooner's setup in irons
(package 37p ...)`, `-rxX`, 5 s), by the strict mark at tests/test_studding.py:203-212. The
schooner's case of "studding sails draw at nine points" is already broken in the game and
recorded as expected.

```diff
--- mut/freesail/physics/sails.py
+++ freesail/physics/sails.py
@@ -1014,6 +1014,8 @@
     cls = SAIL_CLASSES["studding"]
+    if "schooner" in str(getattr(getattr(ship, "spec", None), "rig", "")):
+        return 1.0
```

Live: `studding_stall` gives 1.0 for the schooner's four studding sails at 3 rad off the bow,
0.0 for the frigate's. Run with `-rxX` (no `-x`): `XFAIL ... 1 xfailed in 5.35s`. The strict
xfail would turn red only if the schooner's studding sails began to draw; any further break
of them is reported as expected. The reader's prediction stands exactly.

### 11-N1 KILLED (refuted, both ways)

The reader named smack, lugger and merchant-brig among the files whose posts no test checks.
Their people files do carry posts (`post: true`; the smack's are master and mate).

**11-N1a**, the 64: the captain's and first lieutenant's entries swapped in
data/people/sixty-four.yaml (lines 34-56, 22 lines moved). tests/test_indefatigable.py:1203
runs test_wardroom's check on the 64 and the razee:

```
>       assert [p.post for p in spec.crew.posts] == wardroom.posts, stem
E       AssertionError: sixty-four
E       assert ['captain', '...utenant', ...] == ['first lieut...utenant', ...]
```

**11-N1b**, the smack: master's and mate's entries swapped in data/people/smack.yaml (lines
19-38); live, `PE.load_wardroom("data/ships/smack.yaml").posts == ['mate', 'master']`.
test_wardroom.py::test_the_ship_files_posts_and_people_agree_with_the_wardroom_files passes
(rc=0, 2 s: its four ships omit the smack), as the reader said; but the generator test
regenerates the ship files from the people files and fails:

```
E           AssertionError: smack.yaml differs from what tools/gen_ships.py writes; edit the generator and rerun it
```

"Without regenerating the ship file" is exactly what test_generator_reproduces_the_committed_files
catches, for every ship.

### 11-N2 KILLED (refuted)

The four `pump.chain.*` entries deleted from data/ships/seventy-four.yaml (lines 5640-5660;
two hand pumps left).

```
>       assert [p.kind for p in spec.pumps] == ["chain"] * 4 + ["hand"] * 2
E       AssertionError: assert ['hand', 'hand'] == ['chain', 'ch...hand', 'hand']
```

(tests/test_bellerophon.py::test_her_boats_pumps_hold_and_stores, baseline pass, 1 s). The
generator test also fails on the edit. I did not try the 64 or the razee.

### 11-N3 NOT RUN

A slow test renamed into the fast tier is a fault in the test list, not in the game. Nothing
to plant and run.

## Count

29 faults or variants tried: 18 against named tests (9-1 to 9-6, 10-1 to 10-6, 11-1 to
11-6) and 11 of the readers' "no test would catch it" (9-N1, 9-N2, 9-N3a, 9-N3b, 10-A, 10-B,
10-C, 11-N1a, 11-N1b, 11-N2, 11-N3). 11-5's two rudder sizes count as one.

- **SURVIVED: 19.** Named: 9-1, 9-2, 9-3, 9-4, 9-5, 9-6, 10-1, 10-2, 10-3, 10-4, 10-5,
  10-6, 11-1, 11-2, 11-4, 11-5, 11-6 (17 of 18). Uncaught: 9-N3b, 10-B.
- **KILLED: 9.** Named: 11-3. Uncaught claims refuted: 9-N1, 9-N2, 9-N3a, 10-A, 10-C,
  11-N1a, 11-N1b, 11-N2 (8 of 11).
- **NOT RUN: 1.** 11-N3 (not a fault in the game).

What the survivals have in common: the named test never reaches the code its name promises,
because it supplies the answer itself (a `FakeMagazine`, a monkeypatched `begin_exercise`, a
test-local `FATIGUE_WEIGHT`, the ship words passed into `Brief.build`, the source text
grepped), or its assertion is a tautology or vacuous (`x == x`, `all()` of an empty list,
`.get(..., "wasp")` on a key never set, `... or rec["prisoners"]`, `or all(...)` of `[]`, a
guard whose date never meets its condition, a strict xfail). In eight of the seventeen another
test elsewhere in the suite does catch the same fault (9-1, 9-2, 9-4, 9-6, 10-1, 10-3, 10-4,
11-2); in the rest (9-3, 9-5, 10-2, 10-5, 10-6, 11-1, 11-4, 11-5, 11-6) I found none, though
I looked only as far as each section says.

## What I did not do

- I did not run the whole 1,095-case `test_every_form_in_the_forms_tables_is_taken`; only the
  five chapter-13 `veer` ids the fault touches.
- I did not run truth 56's baseline (10-A) or the baselines of the four tests in 9-N3b and
  the three in 10-B, all of which passed with the fault in.
- I did not start the server for 10-5; the fault's liveness there is by reading.
- I did not look for other tests that catch 11-4 or 11-1.
- Running a check script once from the pristine copy (to compare a reading, 9-N3b) left
  Python bytecode caches under `.../scratchpad/mut/tests/__pycache__` and `.../mut/freesail`;
  no source file there was changed.
