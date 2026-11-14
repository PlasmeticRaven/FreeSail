# Faults, runner 5: the control (eighteen ordinary faults, no test named)

Scratch copy `.../scratchpad/m/5`, restored from `.../scratchpad/mut` after every fault
(`diff -r -q` on `freesail/`, `data/` without `charts`, and `tests/` clean each time).
Every run is the fast tier only, one process:
`timeout 600 python3 -m pytest -q -p no:cacheprovider -x <file> [-k ...]`. "Seconds" is
the wall time of the run that first failed on the fault (it includes collection and any
fixture the `-k` pulled in), and, where that differs much, the time of the catching test
alone.

## Results

(The table is filled in as each fault is done; see the sections below.)

## Fault 1. A square sail drives a fifth less

Planted in `freesail/physics/sails.py`, `compute_sail_forces`, after `_plate_force`:
both force components of every sail of class `square` scaled by 0.8 (so thrust, side
force, loads and the heel and yaw moments all fall by a fifth for square canvas).

```diff
@@ -394,6 +394,9 @@
             square_faced=d.square_faced,
             held=d.held,
         )
+        if sail.cls == "square":
+            f_fwd *= 0.8
+            f_stb *= 0.8
         # the studding sails' stall (spec 3b §7): forward of Luce's angle the sail shakes in
         # its gear; its lift falls away over a point and it flogs, a loose sail's windage.
         # A fore-and-aft sail with every sheet let fly flogs the same way (package 32e).
```

Run: `tests/test_known_truths.py -k "truth_4 or truth_3 or truth_1_"` (the `-k` also
matched the truth_3x tests). Truths 1, 3 (both) and 4, the speed and pointing truths,
**passed** with the fault in. The run stopped at
`test_truth_35_shorten_sail_fires_once_after_two_minutes_over_thirty_and_not_on_a_gust`
(tests/test_known_truths.py:1631):

```
>       assert lost and lost[0].subject == "main.topmast.studdingsail_boom.larboard"
E         - main.topmast.studdingsail_boom.larboard
E         + main.topgallant.studdingsail_boom.starboard
```

Baseline: truth_35 alone passes on the restored copy (12 s). **KILLED**, 184 s for the
run (the polar fixtures first), 12 s for truth_35 alone. What caught it is a pinned
detail (which studdingsail boom carries away first in a squall), not a speed: a
frigate whose square canvas gives a fifth less drive still meets truth 4's 7 to 9 knots
on the beam and truth 3's fastest point.

## Fault 2. The hull's grip against leeway halved

Planted in `freesail/physics/hull.py`, `sway_damping`: the whole return value halved
(cross-flow drag and keel lift both).

```diff
@@ -266,7 +266,7 @@
     when this balances the sails' side force.
     """
     q_area = 0.5 * units.RHO_WATER * hull.lateral_area
-    return -q_area * (C_LAT * v * abs(v) + C_LAT_LIFT * abs(u) * v)
+    return -0.5 * q_area * (C_LAT * v * abs(v) + C_LAT_LIFT * abs(u) * v)
 
 
 def sternway_yaw(hull: Hull, u: float, v: float) -> float:
```

Run: `tests/test_known_truths.py -k "truth_7_"`.

```
>       assert 3.0 <= close_hauled["leeway"] <= 6.0
E       assert 8.931437701488026 <= 6.0
tests/test_known_truths.py:336: AssertionError
```

**KILLED** by `test_truth_7_leeway_close_hauled_and_running`, 50 s.

## Fault 3. The rudder turns her the wrong way

Planted in `freesail/physics/hull.py`, `rudder_forces`: the sign of the side force (and
so of the yaw moment, which is the side force times the lever) reversed.

```diff
@@ -340,7 +340,7 @@
     """
     q = 0.5 * units.RHO_WATER * hull.spec.rudder.area_m2 * rudder_lift_slope(hull.spec.rudder)
     flow = u * abs(u) + math.copysign(RUDDER_SMALL_SPEED2, u if u != 0 else 1.0)
-    side = -q * flow * rudder
+    side = q * flow * rudder
     return side, side * rudder_lever(hull)
 
 
```

Run: `tests/test_hull.py`.

```
>       assert sign * d.r > 0.0
E       assert (1.0 * -0.020325671425847316) > 0.0
tests/test_hull.py:179: AssertionError
FAILED tests/test_hull.py::test_rudder_turns_the_ship_the_way_it_is_put[1.0]
```

**KILLED** by `test_hull.py::test_rudder_turns_the_ship_the_way_it_is_put`, 3 s.

## Fault 4. Evolutions take half the time

Planted in `freesail/evolutions/runner.py`, `_tick_steps`: every step's pace halved, so
every step (and so every evolution) runs in half its time. The runner's own estimate
(`nominal_duration_s`) is left alone.

```diff
@@ -878,7 +878,7 @@
         step = inst.step
         if step is None:
             return
-        pace = step.duration_s * self._last_factor * self._crew_factor(inst, step.aloft)
+        pace = 0.5 * step.duration_s * self._last_factor * self._crew_factor(inst, step.aloft)
         inst.progress = min(1.0, inst.progress + dt / pace)
         if inst.progress >= 1.0 - PROGRESS_EPSILON:
             inst.progress = 1.0
```

Run: `tests/test_evolutions.py`.

```
>           assert 60 <= ticks <= EVOLUTIONS[f"set_{cls}"].nominal_duration_s
E           assert 60 <= 45
tests/test_evolutions.py:313: AssertionError
FAILED tests/test_evolutions.py::test_every_sail_runs_its_evolutions_to_completion[data/ships/frigate-36.yaml]
```

**KILLED** by `test_evolutions.py::test_every_sail_runs_its_evolutions_to_completion`,
under 2 s.

## Fault 5. `tack ship` without its preconditions

Planted in `data/evolutions/tack.yaml`: both preconditions (way of two knots; close-hauled
or a course given) removed.

```diff
@@ -29,9 +29,7 @@
 verb: tack
 applies_to: {class: ship}
 script: tack
-preconditions:
-  - {check: dyn.speed >= knots(2), reason: "She has not way enough on her to stay: {speed} through the water."}
-  - {check: close_hauled() or params.course_deg != none, reason: "She is not close-hauled; bring her by the wind before going about."}
+preconditions: []
 timing:
   brace_s: 45            # to swing the after yards, and again the head yards; and to square them on a miss
   light_after_swing_s: 20  # the short after swing (package 75, the lead's ruling 1 of 2026-11-06): a
```

Run: `tests/test_evolutions.py`.

```
E       Failed: DID NOT RAISE OrderError
tests/test_evolutions.py:714: Failed
FAILED tests/test_evolutions.py::test_tack_needs_way_and_a_close_hauled_course
```

**KILLED** by `test_evolutions.py::test_tack_needs_way_and_a_close_hauled_course`, 6 s.

## Fault 6. A standing order's `for 2 minutes` ignored

Planted in `freesail/standing/runtime.py`, `_tick_when`: the rule fires on the first
tick its condition holds, whatever its duration.

```diff
@@ -431,7 +431,7 @@
         if rule.armed:
             if holds:
                 rule.held_s += TICK_SECONDS
-                if rule.held_s >= rule.trigger.duration_s:
+                if rule.held_s >= 0.0:
                     self._fire(rule, view)
                     rule.armed = False
                     rule.held_s = 0.0
```

Run: `tests/test_standing.py`.

```
    assert firings(w) == [], "not before two minutes have held"
E         Left contains one more item: 1
tests/test_standing.py:976: AssertionError
FAILED tests/test_standing.py::test_when_fires_on_the_edge_after_its_duration_and_not_again_until_the_dwell
```

**KILLED** by
`test_standing.py::test_when_fires_on_the_edge_after_its_duration_and_not_again_until_the_dwell`,
10 s.

## Fault 7. The dead reckoning never errs

Planted in `freesail/world/reckoning.py`, the account's `bring_up` (the one place the
traverse is stepped): after each step the account's latitude and longitude are set to
the ship's true position.

```diff
@@ -2824,6 +2824,9 @@
         )
         # the board on the master's slate, as he laid it down (package 40b)
         self.reckoning.slate_board(self._board(begun, tick, w, steer, made))
+        if world.position is not None:
+            self.reckoning.lat_deg = world.position.lat_deg
+            self.reckoning.lon_deg = world.position.lon_deg
         self._hx = self._hy = 0.0
         self._n = 0
         self._run_n = 0
```

Run: `tests/test_reckoning.py`.

```
>       assert cast.data["matched"] and cast.data["moved_nm"] > 0.5
E       assert (True and 0.0 > 0.5)
tests/test_reckoning.py:363: AssertionError
FAILED tests/test_reckoning.py::test_a_sounding_moves_the_account_onto_the_charts_contour_consistent_with_the_ground
```

**KILLED** by
`test_reckoning.py::test_a_sounding_moves_the_account_onto_the_charts_contour_consistent_with_the_ground`,
9 s. (Caught indirectly: the account already on the truth has nothing to be moved by
the lead. The earlier tests in the file, which drive `Reckoning.advance` directly, did
not see it, as they would not: the fault is in the world's use of the account.)

## Fault 8. The tidal stream sets the opposite way

Planted in `freesail/world/tide.py`, `Tide.at`: the tidal part of the stream negated, so
the flood runs where the ebb should and the ebb where the flood should (the Strait's
constant current is left as it was). This reverses what the ship is set by and what the
readings report alike.

```diff
@@ -641,7 +641,7 @@
         # the flood runs strongest `phase_h` hours after local high water: the stream is a
         # cosine of the height's phase, shifted by the area's phase at M2's rate
         shift = area.phase_h * self.speeds["M2"]
-        along = rate_kn * math.cos(math.radians(phase - shift))
+        along = -rate_kn * math.cos(math.radians(phase - shift))
         speed = units.knots_to_ms(along)
         axis = math.radians(area.axis_deg)
         east, north = speed * math.sin(axis), speed * math.cos(axis)
```

Run: `tests/test_tide.py`.

```
E           AssertionError: HW-2: toward 265
E           assert 265.0 <= 125.0
tests/test_tide.py:115: AssertionError
FAILED tests/test_tide.py::test_truth_63_off_the_lizard_the_stream_runs_east_about_high_water_at_two_knots
```

**KILLED** by `test_tide.py::test_truth_63_off_the_lizard_the_stream_runs_east_about_high_water_at_two_knots`, 2 s.

## Fault 9. A ship never takes the ground

Planted in `freesail/world/ground.py`, `Ground.tick`: the strike never happens, whatever
the chart's test says (`_strike` is never called).

```diff
@@ -180,7 +180,7 @@
                     tide_m,
                     dangers=self._dangers,
                 )
-        if touched is not None and self.grounded is None:
+        if False and touched is not None and self.grounded is None:
             self._strike(touched, rock)
         elif touched is None and self.grounded is not None:
             self._afloat()
```

Run: `tests/test_ground.py`.

```
        w, aground = standing_on_by_account
>       assert aground
E       assert False
tests/test_ground.py:94: AssertionError
FAILED tests/test_ground.py::test_truth_66_standing_on_by_account_grounds_the_schooner_on_the_ebb_at_the_logs_speed
```

**KILLED** by `test_ground.py::test_truth_66_standing_on_by_account_grounds_the_schooner_on_the_ebb_at_the_logs_speed`, 25 s.

## Fault 10. The simulation no longer deterministic

Planted in `freesail/physics/wind.py`, `Wind.step`: an unseeded `random.random()` (the
module's global generator, not the wind's stream) nudges the wind's speed by up to a
hundredth of a metre a second each tick.

```diff
@@ -196,7 +196,7 @@
         # speed: mean-reverting walk about the base speed
         pull = (self.base_speed - self.speed) * 0.0005 * dt
         noise = r.gauss(0.0, 0.01 * v * self.base_speed * math.sqrt(dt))
-        self.speed = max(self.MIN_SPEED, self.speed + pull + noise)
+        self.speed = max(self.MIN_SPEED, self.speed + pull + noise + 0.02 * (random.random() - 0.5))
         mean = mean_speed if mean_speed is not None else self.speed
         # gusts
         self.gust_started = False
```

Run: `tests/test_determinism.py`.

```
E         - 97ff94ec0148e02d13187163f1798221d0db63823fc7835a9be070791bfefe6d
E         + 3edad1962d9733d2f242ca99f1e8dc26853a19b44a82799ea7a3a352e5911164
tests/test_determinism.py:24: AssertionError
FAILED tests/test_determinism.py::test_same_seed_same_log
```

**KILLED** by `test_determinism.py::test_same_seed_same_log`, 2 s.

## Fault 11. The harness no longer recognises the opt-out token

Planted in `freesail/agents/harness.py`, `Harness._take_reply`: the token scan that runs
on every reply before anything else is disabled. (The out-of-turn scan in
`agents/remote.py` and the scan in `agents/mcp_server.py` are left as they were.)

```diff
@@ -2529,7 +2529,7 @@
         self._replied_tick = int(world.clock.tick)  # the cost of thinking (package 58a)
         # 1. the token, before anything else reads the reply
         for piece in reply.pieces():
-            if OPT_OUT_TOKEN in piece:
+            if False and OPT_OUT_TOKEN in piece:
                 reason, how, final = leaving_of(reply, piece)
                 self.leave(reason, how=how, final=final)
                 return
```

Run: `tests/test_agents.py`.

```
E        +  where False = AgentState(station=Station(name='watcher', ...).released
tests/test_agents.py:485: AssertionError
FAILED tests/test_agents.py::test_truth_41_the_token_anywhere_in_the_output_ends_the_session_before_the_parser_sees_it
```

**KILLED** by `test_agents.py::test_truth_41_the_token_anywhere_in_the_output_ends_the_session_before_the_parser_sees_it`, 6 s.

