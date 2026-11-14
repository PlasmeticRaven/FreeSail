# Faults planted, runner 1: known truths (a), known truths (b), view geometry

Faults taken from the `## Faults to plant` sections of `tests-01-known-truths-a.md`,
`tests-02-known-truths-b.md` and `tests-12-view-geometry.md`, in that order, planted one at
a time in the scratch copy `.../scratchpad/m/1` (commit 504a250) and restored from the
pristine copy `.../scratchpad/mut` after each; `diff -r -q` on `freesail/`, `data/` (less
`charts`), `client/` and `tests/` (less `__pycache__`) was clean before every next fault.
Every run was one pytest process, no `-n`. Seconds are wall-clock for the faulted run.

Numbering: A = file 01, B = file 02, G = file 12 (view geometry); "b" = the reader's claim
under (b), "n" = the reader's "no test would catch". The table is in the readers' order; the
sections below are in the order the faults were run (the cheap first).

| No. | Test (file::name) | Fault | Baseline | Result | Secs |
|---|---|---|---|---|---|
| A-b1 | test_known_truths.py::test_truth_52_a_low_passing_north_backs_veers_holds_squalls_and_rises_in_that_order | squall never logged as passed (`weather.squall_over` branch deleted) | pass | SURVIVED | 27 |
| A-b2 | test_known_truths.py::test_truth_50_at_three_hundred_times_the_log_shows_hourly_rollups_and_every_notable_line | `events.kept` keeps only urgent lines: notable lines rolled up at 300x | pass | SURVIVED | 223 |
| A-b3 | test_known_truths.py::test_truth_7_135_the_frigates_broadside_every_minute_and_three_quarters_and_slower_short | long gun's "run out" 18 s to 30 s (85 s nominal to 97) | pass | SURVIVED | 14 |
| A-b4 | test_known_truths.py::test_truth_7b_105_the_smacks_seine_fills_her_well_the_catch_sells_at_falmouth_and_spoils_kept | `price_of` swaps fresh and salted (fresh pilchards sell at the salted £10 not £6) | pass | SURVIVED | 65 |
| A-b5 | test_known_truths.py::test_truth_7_136_a_tack_with_the_guns_served_is_slower_by_exactly_the_hands_it_takes | `Quarters.lend` frees the hands to the tack but each still counts at his gun (guns stay 176 of 176 manned through the tack) | pass | SURVIVED | 14 |
| A-b6 | test_known_truths.py::test_truth_7_138_the_pace_with_two_crewed_cutters_in_action_holds_the_crewed_floor | 4 ms sleep after each crewed hull's tick (pace 425 to 148 ticks/s) | pass | SURVIVED | 37 |
| A-n1 | test_known_truths.py::test_truth_51_..._ticks_at_the_build_machines_floor, ::test_the_pace_on_the_day_under_systems_holds_truth_51s_floor, ::test_the_pace_on_the_gates_day_with_the_region_loaded_holds_truth_51s_floor, ::test_the_pace_at_the_merchant_passages_start_with_the_dozen_ships_holds_truth_51s_floor | 0.6 ms sleep at the head of `World.tick` | pass (558, 569, 528, 942 ticks/s) | KILLED (3 of 4; the merchant passage passed at 514) | 55 |
| A-n2 | test_known_truths.py::test_truth_11_the_frigate_wears_in_six_to_twelve_minutes, ::test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward (strict xfail); test_evolutions.py::test_wear_comes_round_the_other_way (2 cases), ::test_a_tack_and_a_wear_by_their_own_word_end_as_they_always_have; test_indefatigable.py::test_the_razee_stays_wears_and_lies_to_in_the_frigates_bands | wear holds the helm up 300 s after the wind is aft (loses 0.54 nm, not 0.13) | pass (wore in 513 s) | truth 11 pair SURVIVED; KILLED by test_evolutions frigate case (721 s against 720) | 31 |
| A-n3 | test_bellerophon.py::test_robbing_on_a_ship_with_no_lower_deck_is_as_it_was, ::test_robbing_by_deck_takes_the_shut_lower_deck_first_and_the_lower_deck_last (2 cases), ::test_robbing_past_every_gun_says_the_marines_last_with_one_and; test_hands.py::test_short_handed_arithmetic; (and 7-136 above) | guns at full crew while the tack takes their hands (the A-b5 plant) | pass | SURVIVED (all) | 20 |
| B-b1 | test_known_truths.py::test_truth_7_183_the_first_action_replayed_with_the_arms_the_pumps_and_the_carpenter | rules captain's hole filter `z_m < 0.3` to `< -99.0` (never sends the carpenter) | pass | SURVIVED | 220 |
| B-b2 | test_known_truths.py::test_truth_7_176_a_broadsides_casualties_are_men_of_the_muster_named_and_the_bill_counts | `_hull_hit` no longer calls `_casualties` (a shot through the hull hurts nobody) | pass | SURVIVED | 6 |
| B-b3 | test_known_truths.py::test_truth_7_179_a_volley_within_musket_shot_fells_the_near_decks_men_and_the_quarterdecks | `small_arms.QUARTERDECK_SHARE` 0.4 to 0.15 | pass | SURVIVED | 8 |
| B-b4 | test_known_truths.py::test_truth_7_147_a_signal_made_in_fog_is_a_gun_and_not_a_flag | `fog_signals_minute` never starts a ship's fog signals (`if False:`) | pass | SURVIVED | 12 |
| B-b5 | test_known_truths.py::test_truth_7_512_a_ship_sails_from_port_mahon_to_carloforte_and_from_algiers_to_tunis (and ::test_truth_7_545_..., the reader's control) | `ships.land_crossing` returns "" at once (the land guard off) | pass (both) | 7-512 SURVIVED; 7-545 KILLED, as predicted | 116 |
| B-b6 | test_known_truths.py::test_truth_7_284_the_blend_adds_a_membership_and_not_a_gauge, ::test_truth_7_441_the_frame_holds_every_state_and_the_view_writes_nothing | no code fault: the game unchanged, run repeatedly on the shared machine (the `-n 4` run itself NOT RUN: the runners' rule forbids `-n`) | pass | 7-284 failed 1 of 15 serial runs with the game unchanged (flaky: the reader's claim stands); 7-441 passed 5 of 5 | 167 |
| B-n1 | test_known_truths.py::test_truth_7_150_a_light_is_seen_at_night_at_the_range_a_lantern_carries; test_lookout.py::test_at_night_a_light_is_a_light_and_the_lookout_does_not_name_it | a far ship's light order always sets `"none"` | pass | SURVIVED (both) | 9 |
| B-n2 | test_known_truths.py::test_truth_7_183_the_first_action_replayed_with_the_arms_the_pumps_and_the_carpenter; test_health.py::test_the_butchers_bill_is_said_ten_minutes_after_the_last_shot; test_damage_control.py::test_the_carpenter_plugs_the_holes_worst_first_in_the_time_the_bill_says | the same plant | pass | KILLED by 7-183 (the privateer never strikes); the other two passed | 40 |
| B-n3 | test_known_truths.py::test_truth_7_173_...; test_damage_control.py::test_the_carpenter_plugs_the_holes_worst_first_in_the_time_the_bill_says, ::test_every_repair_is_an_evolution_with_hands_and_competes_for_them; test_fight.py::test_the_rules_captain_opens_musketry_within_a_cable_and_serves_out_the_arms_by_his_doctrine (and 7-183) | the same plant | pass | SURVIVED (all) | 16 |
| G-b1 | test_view_geometry.py::test_each_line_that_comes_down_ends_on_her_drawn_rail (36 cases) | every brace led to the mast abaft ends 6 m abaft and 4 m below that mast | pass (36) | SURVIVED (36 of 36; and 14 cases of four nearby brace and frame tests) | 11 |
| G-b2 | test_view_geometry.py::test_the_head_lies_on_head_m (10 cases) | `FIGURE_SHARE` 0.3 to 0.9 (the figurehead three times as tall) | pass (10) | SURVIVED (10 of 10; and 46 cases of five other head tests) | 5 |
| G-b3 | test_view_geometry.py::test_her_booms_and_her_courses_foot_stand_clear_of_her_drawn_decks[frigate-36], ::test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail[frigate-36] | a mend, not a fault: frigate's `mizzen.boom` `height_m` 2.4 to 4.5 (boom clears her taffrail) | pass (both, on the defect) | first PASSED on the mend (prediction refuted: it passes defect and mend alike); second FAILED on the mend (prediction stands: it pins the defect) | 2 |
| G-n1 | test_view_geometry.py::test_the_graph_and_snapshot_carry_what_the_view_reads, ::test_a_wreck_cleared_away_is_not_drawn, ::test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number, ::test_the_scale_is_the_full_rigs_whatever_is_sent_down_or_braced, ::test_only_a_drivers_boom_goes_from_the_drawing_when_it_is_rigged_in | a set studding sail's outer head corner drawn inboard (`-ss2 * Lb`) | pass | SURVIVED (44 of 44 cases) | 30 |
| G-n2 | test_view_geometry.py::test_the_frame_holds_her_boom_across_states_old_beside_new, ::test_every_sprit_sails_foot_stands_above_the_water_in_every_state, ::test_her_sprit_topsail_is_drawn_along_the_slant_to_its_files_area, ::test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number, ::test_the_scale_is_the_full_rigs_whatever_is_sent_down_or_braced | every sail bellies into the wind (`bellyDirection` sign flipped) | pass | SURVIVED (40 of 40 cases) | 67 |
| G-n3 | test_view_geometry.py::test_the_hovers_words_on_the_head_name_no_strip; test_server.py::test_index_serves_the_client (2 cases) | shipview.js drops the `backed` class: a sail aback drawn in the plain canvas colour | pass | SURVIVED (3 of 3) | 3 |

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

## B-b1 and B-n3. No rules captain ever plugs a shot hole

```diff
--- mut/freesail/world/captains.py
+++ m/1/freesail/world/captains.py
@@ -4441,7 +4441,7 @@
         holes = [
             h
             for h in (getattr(keeper, "holes", []) or [])
-            if not h.get("plugged") and float(h.get("z_m", 1.0)) < 0.3
+            if not h.get("plugged") and float(h.get("z_m", 1.0)) < -99.0
         ]
```

Live: the first-action scenario sailed 900 s (Renard engaging), eight `HITS._hull_hit` calls
on Renard aimed between wind and water (3 holes under water), then 700 s: pristine her log
has "By the captain, engaging: plugging the shot holes (the shot holes under water)." and
"Plug the shot holes! The carpenter and his crew to the side with the plugs."; with the fault,
no line with "plug" in it.

B-b1, 7-183: PASSED (220 s). SURVIVED. Its check is `under = [h ... if z_m < 0.0]; if under:
assert any("Plug the shot holes" ...)` (tests/test_known_truths.py, the test's body), and at
seed 7 Renard takes no hole under water, so the assertion is never reached, as its own comment
says ("at this seed her seven lie above it").

B-n3: grep for `plug the shot holes`, `plug_shot_hole` and `damage_priority` in tests gives
7-173 (the player's own order), two of tests/test_damage_control.py (the player's order) and
tests/test_fight.py:427 (reads the threshold's words). All four passed. SURVIVED: no test seen
has a rules captain plug a hole.

Side note from the liveness work, not a planted fault: with tests/test_fight.py's
`_alongside(30.0)`, the enemy's `Captain._damage_work` was called 0 times in 300 s of
`w.run` (a spy on the method), so a rules captain there never reaches his repairs; that
fixture cannot witness any captain's damage work. Not looked into further.

## B-b6. Truths 7-284 and 7-441: wall-clock ratios in the fast tier

No code was changed. The reader's run (`-n 4` beside the slow tier) was not made: the
runners' instruction forbids `-n` while three other runners share the four cores. Instead each
test was run alone, one process at a time, on the machine as it was (load average 1.9 to 5.2,
the other runners working).

7-284, fifteen runs: 14 passed, 1 failed (26 s in all), with the game pristine:

```
>       assert now < 1.25 * then, (now, then)
E       AssertionError: (0.024000508000426635, 0.011513147000187018)
E       assert 0.024000508000426635 < (1.25 * 0.011513147000187018)
```

A ratio of two timings of about a hundredth of a second each (each the best of five),
fails when the other cores are busy. FLAKY: the reader's claim stands for 7-284 even without
`-n`.

7-441 (its `part < 0.25 * whole`), five runs: all passed (141 s). Not shown flaky here; the
`-n 4` case was not tried.

## G-b1. Braces ending in the air between the masts

```diff
--- mut/client/projection.js
+++ m/1/client/projection.js
@@ -1786,7 +1786,7 @@
         var m = mastAftOf(Y.x);
-        var to = m ? v(m.x, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1)) : sideEnd(ss, Y.x - Y.half * 0.8);
+        var to = m ? v(m.x - 6, ss * 0.3, Math.min(Y.centre[2], m.head[2] - 1) - 4) : sideEnd(ss, Y.x - Y.half * 0.8);
```

Live: through the test file's own `fully_dressed` and `run_js(..., LINE_ENDS)` on the frigate,
the fore yard's starboard brace ends at `[-2, 0.3, 17]` pristine (the main mast) and at
`[-8, 0.3, 13]` with the fault, six metres abaft the main mast in the air; the test's own
`where_it_ends` calls both "mast".

Output: 36 PASSED. SURVIVED. `where_it_ends` (tests/test_view_geometry.py:6066) calls a brace's
end "mast" when `abs(end[1]) == 0.3` and reads neither its x nor its z, so any end 0.3 m off the
middle line passes as on a mast. Also run with the fault, all passed:
`test_the_scale_is_the_full_rigs_whatever_is_sent_down_or_braced` (3),
`test_the_braces_lead_up_to_the_fore_top_the_sheets_aft_and_the_lifts_to_the_spars_end` (6),
`test_the_frame_is_equal_across_the_shift_and_back` (2), `test_the_yards_brace_is_shown_from_the_beam` (3).

## G-b2. A figurehead three times its size

```diff
--- mut/client/projection.js
+++ m/1/client/projection.js
@@ -179,7 +179,7 @@
-  var FIGURE_SHARE = 0.3;
+  var FIGURE_SHARE = 0.9;
```

Output: 10 PASSED. SURVIVED. The test reads the share from the page
(`share: P.constants.FIGURE_SHARE`, tests/test_view_geometry.py:2128) and checks the figure
against `tall = got["share"] * top` (2145); it pins the siding (`assert s == 0.2`) but not the
share, so the figure, drawn at 0.9 of the head's height and checked against 0.9, passes. That
check passing is itself the proof the fault is live (the figure is drawn three times as tall).

Also run with the fault, all passed: `test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states`
(12), `test_no_sky_shows_between_the_head_and_the_stem_from_abaft_the_beam` (10),
`test_what_stands_on_the_head_paints_after_the_plate_it_stands_on` (5),
`test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number` (18),
`test_the_hovers_words_on_the_head_name_no_strip` (1). The whole file was not run.

## G-b3. The frigate's boom raised to clear her taffrail (a mend)

```diff
--- mut/data/ships/frigate-36.yaml
+++ m/1/data/ships/frigate-36.yaml
@@ -344,7 +344,7 @@
   class: boom
   'on': mizzen.mast
   length_m: 13.4
-  height_m: 2.4
+  height_m: 4.5
   horse_m: 5.8
```

The reader predicted both tests fail on the mend. One did:

```
>       assert a[2] - taffrail[2] == pytest.approx(old, abs=0.02)  # level, at its jaws' height
E       assert 0.2699999999999996 == -1.83 ± 0.02
FAILED tests/test_view_geometry.py::test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail[data/ships/frigate-36.yaml]
```

`test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail` pins the boom under the
taffrail by equality (`BOOM_OVER_TAFFRAIL_M[FRIGATE] = (-1.83, -1.33)`, with `UNDER_HER_TAFFRAIL`
naming it): it passes the defect and fails the mend. The reader's claim stands for it: a test
whose name says "clear her taffrail" that fails when she clears it.

`test_her_booms_and_her_courses_foot_stand_clear_of_her_drawn_decks` PASSED on the mend, as it
did on the defect: its checks are lower bounds (`>= over_deck - 1e-2`, `>= over_rail - 5e-3`)
against `BOOM_CLEAR_M[FRIGATE] = (0.26, -1.35)`, a negative floor over the rail, so it admits the
boom 1.35 m under her rail and admits it raised. The reader's prediction is refuted for this one:
it does not pin the defect, it tolerates it.

## G-n1. A studding sail drawn inboard across its topsail

```diff
--- mut/client/projection.js
+++ m/1/client/projection.js
@@ -1730,7 +1730,7 @@
         } else if (Yd && Yd.arm) {
           var ss2 = sideSign(spec.side);
           var headA = ss2 > 0 ? Yd.b : Yd.a;
-          cornersS = [headA, add(headA, mul(boom.arm || [0, 1, 0], ss2 * Lb)), boom.b, boom.a];
+          cornersS = [headA, add(headA, mul(boom.arm || [0, 1, 0], -ss2 * Lb)), boom.b, boom.a];
```

Live: the frigate fully dressed (the test file's `fully_dressed`, larboard tack) with
`fore.topmast.studdingsail.starboard` set, its corners by `P.buildSkeleton`: pristine
`[[6.49, 3.59, 29.6], [-0.88, 7.19, 29.6], [6.49, 3.59, 17], [13.86, 0, 17]]`; with the fault
the outer head corner is `[13.86, 0, 29.6]`, on the middle line instead of 7.19 m outboard.

`grep studding tests/test_view_geometry.py` finds no test that sets a studding sail other than
the ringtail (`fully_dressed` sets plain sail and head sails only; `extra` is used for the
cutter's and the smack's square sail). The five likeliest (above, 44 cases) all passed.
SURVIVED.

## G-n2. Every sail bellying into the wind

```diff
--- mut/client/projection.js
+++ m/1/client/projection.js
@@ -268,7 +268,7 @@
     var n = norm(normal);
     var s = dot(n, wind);
     if (Math.abs(s) < 1e-6) return [0, 0, 0];
-    return mul(n, s > 0 ? 1 : -1);
+    return mul(n, s > 0 ? -1 : 1);
```

Live: the frigate fully dressed on the larboard tack, the main topsail's mean path point less
the mean of its corners (the belly, metres): pristine `[0.58, 0.6, 0.15]`, faulted
`[-0.06, -0.84, 0.15]`; its path's y extent goes from -4.79..5.57 to -5.57..4.79. The belly is
thrown to the other side.

`grep belly tests` finds only docstrings and the frame figure `RINGTAIL_PAST_THE_FRAME_M`
(an upper bound, `view["over"] <= past`, tests/test_view_geometry.py:4588). The five likeliest
(the frame and sprit-sail tests above, 40 cases) all passed. SURVIVED: the reader's suspicion
that a frame test might move was not borne out.

## G-n3. A sail aback no longer coloured as aback

```diff
--- mut/client/shipview.js
+++ m/1/client/shipview.js
@@ -90,7 +90,7 @@
       } else if (f.kind === "sail") {
-        var scls = "sail " + f.cls + " " + f.state + (f.backed ? " backed" : "") + (f.reefs ? " reefed" : "") + (f.busy ? " busy" : "");
+        var scls = "sail " + f.cls + " " + f.state + (f.reefs ? " reefed" : "") + (f.busy ? " busy" : "");
```

Live: the brig under plain sail with her topsails marked backed in the snapshot, rendered by
`ShipView.render` in Node (the harness of test 5812, with `setAttribute` recording): pristine
`sail square set backed | fore topsail (set, aback)`; faulted `sail square set | fore topsail
(set, aback)`. The colour comes from `.ship-view .sail.backed` (client/style.css:259), so the
player loses the drawing's mark of a sail aback; the hover words still say "aback".

`grep -rln shipview.js tests` finds two tests: tests/test_view_geometry.py:5812 (reads hover
titles of the head) and tests/test_server.py::test_index_serves_the_client (the file is served).
Both passed. SURVIVED. The reader's "the hover titles of the head alone" is right; for the
whole suite, the grep is the evidence that no other test renders the file.

## Count

Twenty-four entries (the plants of B-b2 and B-n2, and of B-b1 and B-n3, are one each, run
against different tests):

- **SURVIVED: 19.** A-b1 to A-b6, A-n3; B-b1 to B-b5, B-n1, B-n3; G-b1, G-b2, G-n1, G-n2, G-n3.
- **KILLED: 3.** A-n1 (three of four pace floors, on a busy machine; a quiet one would very
  likely pass it); A-n2 (by `test_evolutions.py::test_wear_comes_round_the_other_way`, outside
  the half, by one second; the truth-11 pair in the half survived); B-n2 (by 7-183, in the
  half, through the privateer's morale).
- **Mixed: 1.** G-b3, a mend: the taffrail test fails on the mend (pins the defect, claim
  stands); the decks test passes defect and mend alike (claim refuted).
- **NOT RUN as described: 1.** B-b6 (`-n 4` is forbidden to runners). Run serially instead,
  7-284 failed once in fifteen with the game unchanged: flaky, claim stands; 7-441 held.

Readers' claims refuted: B-n2 ("no truth in this half fires guns and counts hull
casualties": 7-183 catches it); A-n1 only on this machine's load; A-n2 in part (a test
outside the half catches the 300 s hold by a second; with the reader's 120 s alternative the
strict xfail fails, on what is really a mend); G-b3's first test. Every reader's (b) claim
that was run as a fault survived.

**What the survivals have in common.** Most check the game against itself: the test computes
its expectation with the function under test (`kept` in truth 50, `price_of` in 7b-105,
`land_crossing` in 7-545, `P.constants.FIGURE_SHARE` in the head test), or calls the inner
function by hand and so steps round the faulted call (`_casualties` in 7-176, the locker's
`fog_signals` and `lights` set by hand in 7-147 and 7-150). The rest assert a band or a floor
wide enough to hold a broken game (the broadside, the crewed pace, the wear's time), a
vacuous form (`all()` of an empty list in truth 52; a check under `if under:` that the seed
never enters in 7-183; a brace counted "on a mast" by its y alone), or the log's words in
place of the state they report (7-136 reads the "robbed" line, never the guns' crews).
