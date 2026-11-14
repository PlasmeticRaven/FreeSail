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
| A-b6 | test_known_truths.py::test_truth_7_138_the_pace_with_two_crewed_cutters_in_action_holds_the_crewed_floor | 4 ms sleep after each crewed hull's tick (pace 425 to 148 ticks/s) | pass | SURVIVED | 37 |
| A-n1 | test_known_truths.py::test_truth_51_..._ticks_at_the_build_machines_floor, ::test_the_pace_on_the_day_under_systems_holds_truth_51s_floor, ::test_the_pace_on_the_gates_day_with_the_region_loaded_holds_truth_51s_floor, ::test_the_pace_at_the_merchant_passages_start_with_the_dozen_ships_holds_truth_51s_floor | 0.6 ms sleep at the head of `World.tick` | pass (558, 569, 528, 942 ticks/s) | KILLED (3 of 4; the merchant passage passed at 514) | 55 |
| A-n2 | test_known_truths.py::test_truth_11_the_frigate_wears_in_six_to_twelve_minutes, ::test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward (strict xfail); test_evolutions.py::test_wear_comes_round_the_other_way (2 cases), ::test_a_tack_and_a_wear_by_their_own_word_end_as_they_always_have; test_indefatigable.py::test_the_razee_stays_wears_and_lies_to_in_the_frigates_bands | wear holds the helm up 300 s after the wind is aft (loses 0.54 nm, not 0.13) | pass (wore in 513 s) | truth 11 pair SURVIVED; KILLED by test_evolutions frigate case (721 s against 720) | 31 |
| B-b2 | test_known_truths.py::test_truth_7_176_a_broadsides_casualties_are_men_of_the_muster_named_and_the_bill_counts | `_hull_hit` no longer calls `_casualties` (a shot through the hull hurts nobody) | pass | SURVIVED | 6 |
| B-n2 | test_known_truths.py::test_truth_7_183_the_first_action_replayed_with_the_arms_the_pumps_and_the_carpenter; test_health.py::test_the_butchers_bill_is_said_ten_minutes_after_the_last_shot; test_damage_control.py::test_the_carpenter_plugs_the_holes_worst_first_in_the_time_the_bill_says | the same plant | pass | KILLED by 7-183 (the privateer never strikes); the other two passed | 40 |
| B-b3 | test_known_truths.py::test_truth_7_179_a_volley_within_musket_shot_fells_the_near_decks_men_and_the_quarterdecks | `small_arms.QUARTERDECK_SHARE` 0.4 to 0.15 | pass | SURVIVED | 8 |
| B-b4 | test_known_truths.py::test_truth_7_147_a_signal_made_in_fog_is_a_gun_and_not_a_flag | `fog_signals_minute` never starts a ship's fog signals (`if False:`) | pass | SURVIVED | 12 |
| B-b5 | test_known_truths.py::test_truth_7_512_a_ship_sails_from_port_mahon_to_carloforte_and_from_algiers_to_tunis (and ::test_truth_7_545_..., the reader's control) | `ships.land_crossing` returns "" at once (the land guard off) | pass (both) | 7-512 SURVIVED; 7-545 KILLED, as predicted | 116 |
| B-n1 | test_known_truths.py::test_truth_7_150_a_light_is_seen_at_night_at_the_range_a_lantern_carries; test_lookout.py::test_at_night_a_light_is_a_light_and_the_lookout_does_not_name_it | a far ship's light order always sets `"none"` | pass | SURVIVED (both) | 9 |

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

## A-b6. Truth 7-138: the crewed pace cut to a third

```diff
--- mut/freesail/world/ships.py
+++ m/1/freesail/world/ships.py
@@ -1868,6 +1868,7 @@
             # her tick is the World's own with her current (package 84, step 6)
             with world.as_hull(crew):
                 world.tick()
+            import time; time.sleep(0.004)
             mirror(v, crew, minute)
```

Live: with a temporary print of `best` added to the test copy (then restored), the best of
three thousands was 148 ticks a second with the fault against 425 pristine (the machine
shared with other runners; the docstring's 538 was measured alone).

Output: `.  [100%]` (1 passed). SURVIVED. The floor is `crews.CREWED_FLOOR_TICKS_S = 60.0`
(freesail/world/crews.py:99), set for three crewed ships; with two, a loss of two thirds of
the pace passes. The pace would have to fall below a seventh of what was measured to fail.

## A-n1. The whole game slower by 0.6 ms a tick

```diff
--- mut/freesail/core/world.py
+++ m/1/freesail/core/world.py
@@ -2336,6 +2336,7 @@
         current, from `Vessels.tick_crews`, in the order a crewed World's ran)."""
+        import time; time.sleep(0.0006)
         followed = self.is_followed
```

A `print("BEST", best)` was put before each `assert best >= BUILD_MACHINE_FLOOR` of the test
copy for both runs (the assertion untouched; the file restored after). Pristine, on this
machine shared with three other runners: 558, 569, 528 and 942 ticks a second, against the
floor of 500 (tests/test_known_truths.py:2163), not the 843 to 1000 the reader quotes.
Faulted: 379, 379, 361 and 514.

Output, the first of three alike:
```
E       AssertionError: 379 ticks a second
E       assert 378.7558885490308 >= 500.0
tests/test_known_truths.py:2181: AssertionError
```
KILLED by truth 51, the day under systems and the gate's day with the region; the merchant
passage's start passed at 514 (from 942, a loss of 45 per cent). The kill is the load's as
much as the fault's: the pristine figures were within 6 to 14 per cent of the floor here, so
on the build machine alone at the figures the reader quotes (843 to 1000), the same 0.6 ms
gives about 560 to 625 and would pass, as the reader said. The fifth floor,
`test_the_pace_on_the_passage_holds_truth_51s_floor` (it needs the `gate_5b_passage` fixture),
was not run. By these figures the floors would pass a third of the pace lost on a quiet
machine, and an unchanged game came within 6 per cent of failing on a busy one: they measure
the machine more than the game.

## A-n2. A wear that runs off five minutes before coming to

```diff
--- mut/freesail/evolutions/scripts.py
+++ m/1/freesail/evolutions/scripts.py
@@ -1992,7 +1992,7 @@
                 follow_wind(self.head, rel, ch, max_step)
             wind_aft = abs(rel) >= units.deg_to_rad(165.0)
             crossed = self.sign * rel < 0 and abs(rel) > math.pi / 2
-            if wind_aft or crossed:
+            if (wind_aft or crossed) and self.t - self.__dict__.setdefault("_aft_at", self.t) >= 300.0:
                 self.phase = "come_to"
```

Live: the test's own `wear(close_hauled_on_starboard(FRIGATE))` gives "wore in 513 s; lost
0.127 nm" pristine and "wore in 640 s; lost 0.539 nm" with the fault. The loss is half a mile,
not the two miles the reader supposed.

Truth 11: the timed test passed (640 s is inside 360 to 720) and the strict xfail on the loss
stayed XFAIL (0.54 nm is outside a quarter to half a mile): both SURVIVED, as the reader said.

Beyond the half (grep for `wear ship`/`ship.wore` in tests; the likeliest by name):
`test_evolutions.py::test_wear_comes_round_the_other_way[data/ships/frigate-36.yaml]` failed:

```
>       assert 360 <= ticks <= 720  # six to twelve minutes
E       assert 721 <= 720
tests/test_evolutions.py:1059: AssertionError
```

Its schooner case, `test_a_tack_and_a_wear_by_their_own_word_end_as_they_always_have` and
`test_indefatigable.py::test_the_razee_stays_wears_and_lies_to_in_the_frigates_bands` passed.
So KILLED, but by one second over a time band, not by the ground lost; a hold of 240 s would
very likely pass it.

The 120 s variant the reader offered: wore in 501 s, lost 0.263 nm. Both truth-11 time tests
and `test_wear_comes_round_the_other_way` passed; the strict xfail failed as `[XPASS(strict)]`.
That is the xfail catching a wear that loses what Luce says it should (inside the band): with
120 s the plant is closer to a mend than a fault, and the strict xfail fails on the mend.

## B-b2 and B-n2. A shot through the hull hurts nobody

```diff
--- mut/freesail/combat/hits.py
+++ m/1/freesail/combat/hits.py
@@ -194,7 +194,6 @@
     keeper.minute.append(
         ("hole", f"a shot {'between wind and water' if below else 'through the side'} to {side}")
     )
-    _casualties(ship, keeper, MEN_HURT_HULL * scale * grape, x_m, "hull", rng, tick)
     return ["A shot struck her between wind and water."] if below else []
```

Live: forty calls of `HITS._hull_hit` on the frigate at quarters (seed 7, a stand-in gun of
18 pounds) make 40 holes and hurt 59 men pristine, 40 holes and 0 men with the fault.

B-b2, truth 7-176: PASSED. SURVIVED. The test calls `HITS._casualties(..., "hull", ...)`
itself six times (tests/test_known_truths.py, in its body), so the line removed from
`_hull_hit` is never on its road.

B-n2, "no truth in this half fires guns and counts hull casualties": refuted for 7-183, which
is in the same half. With the fault, the first action replayed fails at once:

```
>       assert first is not None and v.struck and not w.ship.extra.get("struck")
E       AssertionError: assert (781 is not None and False)
E        +  where False = Vessel(id='renard', ...).struck
```

(tests/test_known_truths.py:10571): with no splinter casualties the privateer's morale holds
and she never strikes. KILLED, though by the morale's consequence and not by a count of the
hurt. `test_health.py::test_the_butchers_bill_is_said_ten_minutes_after_the_last_shot` and
`test_damage_control.py::test_the_carpenter_plugs_the_holes_worst_first_in_the_time_the_bill_says`
passed.

## B-b3. Truth 7-179: the quarterdeck's share of the musketry cut from two in five to three in twenty

```diff
--- mut/freesail/combat/small_arms.py
+++ m/1/freesail/combat/small_arms.py
@@ -59,7 +59,7 @@
-QUARTERDECK_SHARE = 0.4
+QUARTERDECK_SHARE = 0.15
```

Live: `inspect.signature(SA.strike_a_man)` shows the default `quarterdeck_share` 0.15; the
choice is `quarterdeck if rng.random() < quarterdeck_share else deck`
(freesail/combat/small_arms.py:262).

Output: PASSED. SURVIVED. The test forces the draw to 0.1, under any share above a tenth, and
asserts only that some musketry fell and that this forced man is of the quarterdeck. Nothing
counts the share over many balls.

## B-b4. Truth 7-147: no rules ship ever keeps her fog signals

```diff
--- mut/freesail/world/signalling.py
+++ m/1/freesail/world/signalling.py
@@ -892,7 +892,7 @@
     if p.strangers:
         cap._business["sail_seen_tick"] = tick
     company = tick - int(cap._business.get("sail_seen_tick", -(10**9))) <= FOG_SIGNALS_COMPANY_S
-    if light == "fog" and company and not locker.fog_signals:
+    if False:
         if near:
```

Live: a script on the test's own fog sea (`_sea_at(49.5, -5.5, CUTTER, ...)`, visibility a
cable) with two far merchant brigs ninety metres apart nine miles off, run 20 minutes: pristine,
both brigs' lockers read `fog_signals True`; with the fault, both `False`. (Placed as in the
test, two miles off with nobody in sight, no ship starts them pristine either: her `p.strangers`
is empty in a cable's visibility, so the test's own Harpy is no witness.)

Output: PASSED. SURVIVED. The bell part of the test sets `vessel_locker(rider).fog_signals =
True` by hand (tests/test_known_truths.py:8852) and so never asks whether a ship would. `grep
-rn fog_signals tests` finds that line alone.

## B-b5. Truth 7-512: the land guard switched off

```diff
--- mut/freesail/world/ships.py
+++ m/1/freesail/world/ships.py
@@ -1684,6 +1684,7 @@
     and last cable are not tried (she lies where she lies; a place may be the shore)."""
+    return ""
     chart = getattr(world, "chart", None)
```

Output: 7-512 PASSED (2.6 s). SURVIVED: it draws the two passages' legs on the chart itself
(`chart.line_shore`, `chart.elevation_at`) and sails no ship, so the guard is never on its
road; its name ("a ship sails") promises more than a chart check.

The control, 7-545, FAILED (112 s), so the fault is live:

```
E                   assert (47.9946, -4.556) == (48.0387, -4.7439)
E                     At index 0 diff: 47.9946 != 48.0387
```

That is the pinned east corner of Diamond's patrol square in naval-cruise.yaml
(tests/test_known_truths.py:17323): `_goal_plan` places the corners with `land_crossing`
(freesail/world/ships.py:1301), and with the guard off the corner falls 0.19 degrees further east (whether on land was not checked).
The test's own `assert not land_crossing(...)` lines could not have caught it, the test
calling the faulted function as its oracle; it was the pinned figure that did.

## B-n1. A far ship told to show her lights stays dark

```diff
--- mut/freesail/world/signals.py
+++ m/1/freesail/world/signals.py
@@ -1413,9 +1413,7 @@
     if low in _LIGHT_ORDERS:
-        vessel_locker(vessel).lights = (
-            "none" if "no lights" in low else "top lights" if "top" in low else "stern lantern"
-        )
+        vessel_locker(vessel).lights = "none"
         return "her lights " + ("doused" if "no lights" in low else "hoisted")
```

Live: `far_perform(w, v, "hoist a stern lantern")` on a far brig at night returns `her lights
hoisted` and leaves her locker at `none` with the fault; pristine, `stern lantern` (and `top
lights` for "hoist the top lights"). With the fault the log says the lights are hoisted while
the ship shows none.

`grep` for the light orders in tests finds only 7-150, which sets `vessel_locker(v).lights =
"stern lantern"` by hand (tests/test_known_truths.py:8958) and orders the player's own lights;
no test calls `far_perform` with a light order. 7-150 and tests/test_lookout.py::
test_at_night_a_light_is_a_light_and_the_lookout_does_not_name_it both passed. SURVIVED.
