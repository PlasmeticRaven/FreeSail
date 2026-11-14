# Faults, runner 5: the control (eighteen ordinary faults, no test named)

Scratch copy `.../scratchpad/m/5`, restored from `.../scratchpad/mut` after every fault
(`diff -r -q` on `freesail/`, `data/` without `charts`, and `tests/` clean each time).
Every run is the fast tier only, one process:
`timeout 600 python3 -m pytest -q -p no:cacheprovider -x <file> [-k ...]`. "Seconds" is
the wall time of the run that first failed on the fault (it includes collection and any
fixture the `-k` pulled in), and, where that differs much, the time of the catching test
alone.

## Results

| # | Fault | Where planted | Files run (fast tier) | Result | s to first failure |
|---|---|---|---|---|---|
| 1 | square sail drives 0.8 | physics/sails.py `compute_sail_forces` | test_known_truths.py `-k "truth_4 or truth_3 or truth_1_"` | KILLED by `test_known_truths.py::test_truth_35_shorten_sail_fires_once_after_two_minutes_over_thirty_and_not_on_a_gust` (which boom carries away first); truths 1, 3, 4 (speed, pointing) passed | 184 (12 alone) |
| 2 | hull's leeway grip halved | physics/hull.py `sway_damping` | test_known_truths.py `-k truth_7_` | KILLED by `test_truth_7_leeway_close_hauled_and_running` | 50 |
| 3 | rudder sign reversed | physics/hull.py `rudder_forces` | test_hull.py | KILLED by `test_hull.py::test_rudder_turns_the_ship_the_way_it_is_put` | 3 |
| 4 | evolution steps half time | evolutions/runner.py `_tick_steps` | test_evolutions.py | KILLED by `test_evolutions.py::test_every_sail_runs_its_evolutions_to_completion` | under 2 |
| 5 | `tack ship` preconditions dropped | data/evolutions/tack.yaml | test_evolutions.py | KILLED by `test_evolutions.py::test_tack_needs_way_and_a_close_hauled_course` | 6 |
| 6 | `for 2 minutes` ignored | standing/runtime.py `_tick_when` | test_standing.py | KILLED by `test_standing.py::test_when_fires_on_the_edge_after_its_duration_and_not_again_until_the_dwell` | 10 |
| 7 | reckoning set to the truth | world/reckoning.py `bring_up` | test_reckoning.py | KILLED by `test_reckoning.py::test_a_sounding_moves_the_account_onto_the_charts_contour_consistent_with_the_ground` | 9 |
| 8 | tidal stream reversed | world/tide.py `Tide.at` | test_tide.py | KILLED by `test_tide.py::test_truth_63_off_the_lizard_the_stream_runs_east_about_high_water_at_two_knots` | 2 |
| 9 | never takes the ground | world/ground.py `Ground.tick` | test_ground.py | KILLED by `test_ground.py::test_truth_66_standing_on_by_account_grounds_the_schooner_on_the_ebb_at_the_logs_speed` | 25 |
| 10 | unseeded nudge to the wind | physics/wind.py `Wind.step` | test_determinism.py | KILLED by `test_determinism.py::test_same_seed_same_log` | 2 |
| 11 | opt-out token not recognised | agents/harness.py `_take_reply` | test_agents.py | KILLED by `test_agents.py::test_truth_41_the_token_anywhere_in_the_output_ends_the_session_before_the_parser_sees_it` | 6 |
| 12 | domain check always allows | agents/tools.py `authority_check` | test_officer.py | KILLED by `test_officer.py::test_an_order_outside_the_domain_is_refused_in_words_and_logged` | 27 |
| 13 | buying takes no money | world/dealings.py (both buying paths) | test_ports.py | KILLED by `test_ports.py::test_the_boats_errand_ashore_brings_the_prices_off_and_the_orders_refuse_in_words_otherwise` | 98 |
| 14 | round shot never hits | combat/shot.py `hit_chance` | test_fight.py (passed whole), test_dumb_show.py | KILLED by `test_dumb_show.py::test_the_hit_chance_with_no_size_is_todays_and_a_size_replaces_the_hulls` (a copy of the formula) | 61 (18 alone) |
| 15 | world order in the play log | core/events.py `RECORD_ONLY_KINDS` | test_world_orders.py | KILLED by `test_world_orders.py::test_the_hand_gives_a_far_ship_her_captains_order_and_he_takes_up_his_plan_after_a_glass` | 66 |
| 16 | save leaves out the book | core/world.py `_save` | test_replay.py; test_standing.py `-k book_is_saved` | KILLED by `test_replay.py::test_a_stand_down_by_the_door_replays_with_every_line_in_its_place` (and `test_standing.py::test_the_book_is_saved_with_the_game_and_restored_by_replay`, 5 s) | 35 |
| 17 | lookout sees sail at twice the range | world/ships.py `Vessels.in_sight` | test_known_truths.py `-k truth_67` | KILLED by `test_truth_67_a_far_ship_moves_by_the_players_wind_and_tide_and_is_sighted_at_the_horizon` | 8 |
| 18 | wind capped at twenty knots | physics/wind.py `Wind.effective_speed` | test_wind.py | KILLED by `test_wind.py::test_gusts_by_air_mass_are_multiples_of_the_ten_minute_mean` | under 2 |

No fault needed the widening step: each was caught by the first file chosen, except
fault 14, which the first file (test_fight.py) let through and the second caught.

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

## Fault 12. A station below the captain may give any order

Planted in `freesail/agents/tools.py`, `authority_check`: the domain's answer
(`domain.why_not`) replaced by "allowed", so every station's order passes as within its
domain (the officer of the watch, the master, the lookout, a passenger alike).

```diff
@@ -1004,7 +1004,7 @@
         # duty allows, whatever his domain (his duty is the movement's own check), and asks
         # what is ashore
         return text, "", DOMAIN
-    why = domain.why_not(order.verb, spec.object, spec.level)
+    why = None
     if why is None:
         return text, "", DOMAIN
     agent = harness.agent
```

Run: `tests/test_officer.py`.

```
E         At index 0 diff: "Order not carried out ('tack ship'): She has not way enough on her to stay: 0.7 kn through the water." != "The officer of the watch may not tack ship without the captain: a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's."
tests/test_officer.py:486: AssertionError
FAILED tests/test_officer.py::test_an_order_outside_the_domain_is_refused_in_words_and_logged[tack ship-...]
```

**KILLED** by `test_officer.py::test_an_order_outside_the_domain_is_refused_in_words_and_logged`, 27 s.

## Fault 13. Buying at a market takes no money

Planted in `freesail/world/dealings.py`: the purse's `pay` struck out of both buying
paths (the single bargain and the bargains struck together). The goods still come, the
market still moves, and the line still says the money was paid.

```diff
@@ -2324,7 +2324,7 @@
                     f"{tons:g} tons of {good.good} at {pounds_words(price)} a ton is "
                     f"{pounds_words(sum_pounds)}, and the purse holds {purse.words()}."
                 )
-            purse.pay(sum_pounds, f"{tons:g} tons of {good.good} at {port.name}", now)
+            pass  # purse.pay(sum_pounds, f"{tons:g} tons of {good.good} at {port.name}", now)
             port.market.bought_from_port(good.good, tons)
             self._send_boat(
                 port,
@@ -2443,7 +2443,7 @@
         said: list[str] = []
         for good_name, tons, price, sum_pounds in struck:
             if verb == "buy":
-                purse.pay(sum_pounds, f"{tons:g} tons of {good_name} at {port.name}", now)
+                pass  # purse.pay(sum_pounds, f"{tons:g} tons of {good_name} at {port.name}", now)
                 port.market.bought_from_port(good_name, tons)
                 items.append(
                     {"kind": "purchase", "good": good_name, "tons": tons, "pounds": sum_pounds}
```

Run: `tests/test_ports.py`.

```
E        +  where 500.0 = Purse(pounds=500.0, entries=[], ledger=[]).pounds
tests/test_ports.py:839: AssertionError
FAILED tests/test_ports.py::test_the_boats_errand_ashore_brings_the_prices_off_and_the_orders_refuse_in_words_otherwise
```

(the assertion is `assert w.purse.pounds == 494.0`, tests/test_ports.py:839.)
**KILLED**, 98 s for the file to that point.

## Fault 14. Round shot never hits

Planted in `freesail/combat/shot.py`, `hit_chance`: the chance multiplied by nought
(every great gun's shot, near and far, at the mark or at a ship, misses).

```diff
@@ -168,7 +168,7 @@
     aspect = 0.6 + 0.4 * abs(math.sin(aspect_rad))
     quality = min(1.2, max(0.6, aim))
     steady = 1.0 / (1.0 + 0.05 * max(0.0, scatter_deg) * max(r, 0.5))
-    return min(0.98, base * size * aspect * quality * steady)
+    return 0.0 * min(0.98, base * size * aspect * quality * steady)
 
 
 # The bands in the period's words, for the log (judgement on the usage).
```

Runs: `tests/test_fight.py` **passed whole** (12 fast tests, 43 s) with no shot able to
hit. Then `tests/test_dumb_show.py`:

```
E                           AssertionError: assert 0.0 == 0.21600000000000003
tests/test_dumb_show.py:398: AssertionError
FAILED tests/test_dumb_show.py::test_the_hit_chance_with_no_size_is_todays_and_a_size_replaces_the_hulls
```

**KILLED** by `test_dumb_show.py::test_the_hit_chance_with_no_size_is_todays_and_a_size_replaces_the_hulls`,
18 s (61 s with the first file). What caught it is a test that keeps a copy of the
formula (`_old_hit_chance`, tests/test_dumb_show.py:359) and compares the two: a
regression lock on the arithmetic, not a test that a broadside does anything. The file
named for the fight let a gunnery in which nothing ever hits pass.

## Fault 15. A world order written to the play log as it is given

Planted in `freesail/core/events.py`: `world.order` taken out of `RECORD_ONLY_KINDS`, so
`for_the_record` no longer keeps the order's own line from the play log (the console's
and the server's filters both read it).

```diff
@@ -187,7 +187,7 @@
 # the full record (the log's store, the save, the replay, the director's view) and never
 # in a station's sample, its `read_log` or the browser's play log, which carry only its
 # effects as they are met. Marked by kind, so that no line's words or digest move.
-RECORD_ONLY_KINDS = frozenset({"world.order", "director.revealed"})
+RECORD_ONLY_KINDS = frozenset({"director.revealed"})
 # ...and the actors whose every line is for the record (spec M7b §6; package 50): the
 # director's station, whose seating, stand-bys and leaving no station and no play log
 # sees (a director you can see coming is not a director); added as its station is made
```

Run: `tests/test_world_orders.py`.

```
>       assert not [x for x in w.log if "By the captain" in x.text and not for_the_record(x)]
E       assert not [Event(tick=60, ..., kind='world.o... "X": order heave to', 'source': 'the test', ...})]
tests/test_world_orders.py:504: AssertionError
FAILED tests/test_world_orders.py::test_the_hand_gives_a_far_ship_her_captains_order_and_he_takes_up_his_plan_after_a_glass
```

**KILLED** by `test_world_orders.py::test_the_hand_gives_a_far_ship_her_captains_order_and_he_takes_up_his_plan_after_a_glass`,
66 s.

## Fault 16. A save leaves out the standing orders' book

The book is not restored from the save's `standing_orders` key in this build: that key is
"for the reader" (freesail/core/world.py:2617, comment), and a replay re-enters the book
from the orders in `inputs` and `journal` (`replay._give`); only Python rules are read
from the key (`ui/console.py:444`, `restore_python_rules`). So to make a replayed game
come back with an empty book, the plant leaves the book out in all three places a save
carries it: the key written empty, and the `standing order ...` orders dropped from the
journal and the inputs. (With the journal changed, a checkpoint no longer belongs to its
save and the load replays, so a reload comes back empty too.)

```diff
@@ -2609,13 +2609,13 @@
             "scenario": self.scenario.to_dict(),
             "ship_ref": self.ship.save_ref(),
             "end_tick": self.clock.tick,
-            "journal": [list(entry) for entry in self.journal],
+            "journal": [list(entry) for entry in self.journal if not str(list(entry)[2]).lower().startswith("standing order")],
             # every order and driver's line in the order they came, which a replay gives
             # again (package 29); a save without it replays its journal
-            "inputs": [dict(entry) for entry in self.inputs],
+            "inputs": [dict(entry) for entry in self.inputs if not str(entry.get("order", "")).lower().startswith("standing order")],
             # the book of standing orders (spec M4 §3): the orders' text and state, for the
             # reader; a replay re-enters them from the journal
-            "standing_orders": self.standing.book.save(),
+            "standing_orders": [],
             # the agents (spec M4 §11): each station, its policy, its transcript (the
             # model's replies, which a replay plays back) and its journal; since package
             # 82 a harness may be in another hull than the one it was seated on (its person
```

Run: `tests/test_replay.py`.

```
E        +  and   9 = len(<freesail.core.events.Log object ...>)
tests/test_replay.py:641: AssertionError
FAILED tests/test_replay.py::test_a_stand_down_by_the_door_replays_with_every_line_in_its_place
```

(the assertion is `assert len(copy.log) == len(world.log)`.) Baseline: that test alone
passes on the restored copy (12 s). **KILLED**, 35 s. Also confirmed by
`tests/test_standing.py -k book_is_saved` (5 s):
`test_the_book_is_saved_with_the_game_and_restored_by_replay` fails at
tests/test_standing.py:1386 (`Right contains 3 more items, first extra item: 'bells'`).
`test_replay.py::test_truth_39_a_passage_under_the_starter_routines_replays_with_the_same_firings`,
earlier in the file, passed: the starter book comes from the scenario, not the journal.

## Fault 17. The lookout sights a sail at twice the distance

Planted in `freesail/world/ships.py`, `Vessels.in_sight`: the horizon limit for a sail
doubled (the weather's visibility and the night's limit still cap it).

```diff
@@ -2174,7 +2174,7 @@
                 continue  # her own body is no sail of hers (package 84, step 7)
             bearing, distance = bearing_and_distance(pos, v.position)
             nm = distance / units.NAUTICAL_MILE
-            limit = min(vis_nm, horizon_nm(height_of_eye_m, v.height_m))
+            limit = min(vis_nm, 2.0 * horizon_nm(height_of_eye_m, v.height_m))
             if v.seen_within_nm is not None:
                 limit = min(limit, v.seen_within_nm)  # a boat: the eye's limit, not the horizon's
             if daylight != "day":
```

Run: `tests/test_known_truths.py -k truth_67`.

```
E       assert (55153.17872604997 / 1852.0) <= (22.67373878646558 + 0.15)
tests/test_known_truths.py:3931: AssertionError
FAILED tests/test_known_truths.py::test_truth_67_a_far_ship_moves_by_the_players_wind_and_tide_and_is_sighted_at_the_horizon
```

**KILLED** by `test_truth_67_a_far_ship_moves_by_the_players_wind_and_tide_and_is_sighted_at_the_horizon`, 8 s.

## Fault 18. The wind never exceeds twenty knots

Planted in `freesail/physics/wind.py`, `Wind.effective_speed` (which the sails, the
evolutions' weather factor, the wind record and every reading of the wind read): capped
at twenty knots.

```diff
@@ -239,7 +239,7 @@
             peak = self._gust_peak
         if self.squall_remaining > 0.0:
             peak = max(peak, self._squall_peak)
-        return max(self.speed, peak)
+        return min(units.knots_to_ms(20.0), max(self.speed, peak))
 
     def speed_at_height(self, height: float) -> float:
         h = max(height, 1.0)
```

Run: `tests/test_wind.py`.

```
E                     Obtained: 10.28888
E                     Expected: 12.230851837726812 ± 1.2e-05
tests/test_wind.py:68: AssertionError
FAILED tests/test_wind.py::test_gusts_by_air_mass_are_multiples_of_the_ten_minute_mean[warm]
```

**KILLED** by `test_wind.py::test_gusts_by_air_mass_are_multiples_of_the_ten_minute_mean`, under 2 s.

## Count

Eighteen planted, eighteen KILLED in the fast tier, none survived, none not run. Twelve
were caught within thirty seconds of starting the first file chosen, and all within about
a hundred seconds of the catching file's start (fault 1's 184 s is the polar fixtures of
other truths run first; the catching test takes 12 s alone).

Two kills are softer than the count makes them look. Fault 1 (a fifth less drive from
square canvas) passed every speed and pointing truth it touched (truths 1, 3 and 4) and
was caught only by truth 35's pinned detail of which studdingsail boom carries away
first; a fault that lowered the drive and left that detail alone would have got past
those truths. Fault 14 (no great gun ever hits) passed test_fight.py whole and was
caught by a test that holds a copy of the hit-chance formula and compares the two, a
lock on the arithmetic rather than a test that a broadside does anything; a fault
further down (in `hits.resolve_shot`, or where `guns.py` reads the chance) would not
meet that copy.

What the fast tier catches quickly: a fault that reverses a sign, removes a guard or a
check, or breaks a rule with an exact, named answer (the rudder, the tide's direction,
the preconditions, the duration of a rule, the opt-out token, the domain, the purse,
the record-only line, determinism, the wind's gust multiple) is caught in seconds by a
test whose name says the behaviour. What it lets through more easily is a fault of
degree in the physics: a change of a fifth in a force sits inside the wide bands the
speed truths allow, and is caught, when it is, by a pinned incidental figure, not by the
truth the behaviour belongs to.
