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
data faults of 03-3 and 03-4 survive their named tests but not the suite. Then the generator
fault with the data regenerated by it (`python3 tools/gen_ships.py data/ships`, as a commit of
both would be): the regenerate test passes (3.2 s) and 03-3's brig case passes (6.9 s), but
the same test's frigate case fails at test_anchor.py:76 (`2200 < bower.weight_kg < 2600`) and
test_bilander.py::test_her_ground_tackle_is_the_house_rule_two_bowers_and_a_kedge fails at
:1187 (`weight_kg == approx(6.4 * CWT_KG)`). So the generator's rule is pinned at two sizes,
the frigate and the bilander; the brig's, schooner's and cutter's anchors are pinned by
nothing but the regenerate test's equality with themselves. KILLED (all data restored after).

## tests-04, the faults to plant

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 04-1 | test_catalogue.py::test_aloft_flags_are_on_the_steps_aloft | `aloft: true` deleted from the lateen's furl | pass | SURVIVED | 1.2 |
| 04-2 | test_date_and_war.py::test_the_pilots_news_enters_what_it_changed_in_the_papers | the pilot's news never entered in the papers | pass | SURVIVED | 8.8 |
| 04-3 | test_canvas.py::test_new_parts_do_not_change_the_ratings_of_the_old_spars | frigate's main topmast rated 26.2 kN, not 261.9 | pass | SURVIVED | 1.8 |
| 04-4 | test_captain.py::test_the_console_and_the_server_take_the_seat_flag | console's `seat_player` call deleted | pass | SURVIVED | 1.7 |
| 04-5 | test_consent.py::test_the_harness_and_the_consent_step_import_no_vendor | the vendor SDK imported at the head of the harness | pass | SURVIVED | 3.9 |
| 04-6 | test_director.py::test_the_aboard_orders_do_what_the_table_knows_and_reach_the_play_log_as_a_report | a seam found working reported and makes no water | pass | SURVIVED | 8.5 |

### 04-1

```diff
   - do: furl
     duration_s: 120
-    aloft: true
     sets: {sail.state: furled}
```
(`data/evolutions/furl_lateen.yaml:25`.) Live: `EVOLUTIONS['furl_lateen'].steps` gives
`[('brail_up', False), ('furl', False)]` with the fault, `('furl', True)` without. Output: 1
passed. `furl_lateen` is not in `ALOFT_STEPS`, so line 275 compares the file's set with itself.
SURVIVED.

### 04-2

```diff
             # what his news changed of the war the ship knows is entered in her papers, as
             # a price is (the owner's fifth note)
-            papers = getattr(world, "papers", None)
-            if papers is not None:
-                for line in papers.news_heard(f"the pilot off {port.name}"):
-                    self._record(
-                        Severity.NOTABLE, "paper.written", line, {"paper": "the news of the war"}
-                    )
```
(`freesail/world/dealings.py:863-868`.) Live: test_ports.py's frigate standing in for Falmouth
with peace made with France beforehand, run to `port.pilot_aboard`: `port.news` 1 line both
ways; `paper.written` by the pilot none with the fault, one ("The news of the war written up by
the captain: by the pilot off Falmouth, peace made between Britain and France...") without.
Output: 1 passed. The test writes the two lines itself with `w.record` and never runs the hook.
SURVIVED.

### 04-3

```diff
-  rating_kn: 261.9
+  rating_kn: 26.2
```
(`data/ships/frigate-36.yaml:233`.) Live: `load_spec(...)` gives the main topmast `rating_kn`
26.2. Output: 1 passed: the test asks only that there is one ringtail boom rated at 1 kN or
more. Caught elsewhere: test_ship_particulars.py::test_generator_reproduces_the_committed_files
fails (4.1 s). SURVIVED (the named test).

### 04-4

```diff
     seat = player_seat_for(world, args.seat, scenario_file)
-    if seat:
-        seat_player(world, seat, door="console")
```
(`freesail/ui/console.py:1211-1212`.) Live: `main(['--seat', 'officer'])` with `quit` on stdin
prints "The player takes the officer of the watch's station (the player, through the console,
...)" on the pristine code and not with the fault. Output: 1 passed: the test reads the source
for the strings `"--seat"` and `seat.route(`, both still there. SURVIVED.

### 04-5

```diff
 from __future__ import annotations
 
+import <the vendor SDK>  # noqa: F401
 import dataclasses
```
(`freesail/agents/harness.py:148`; the import name read from pyproject.toml:29.) Live:
importing `freesail.agents.harness` puts the vendor SDK in `sys.modules` with the fault, not
without. Output: 1 passed: the test bans only `mcp`, `mcp_types` and `httpx`. SURVIVED.

### 04-6

```diff
-    seam = world.water.start_seam(float(value), "a seam started below the wale")
+    seam = {"since": world.clock.tick}
```
(`freesail/world/orders.py:3569`.) Live: after `aboard: a seam found working [reason: t]` on
the test's `directed()` world, `w.water.state.seams` holds 0 seams with the fault, 1 without;
the director's answer still reads "Done: found aboard: a seam started, making 2 tons an hour".
Output: 1 passed (its check is `lambda: True`). The reader's second prediction holds:
test_damage_control.py::test_the_ground_leak_is_caulked_by_the_carpenter_in_his_hours passes
too (19.8 s). Caught elsewhere: test_water.py::test_the_directors_causes_act_through_the_keeper_and_the_pumped_out_form_is_doubted
fails at :253 (`where False = any(...)`, 5.9 s). SURVIVED (the named test).

## tests-04, the faults its reader said no test would catch

| # | Tests run | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 04-A | four (below) | back and fill `cycles: 2` to `cycles: 0` | pass (the xfail: xfail) | SURVIVED (all four) | 1.3 to 4.8 each |
| 04-B | test_scenarios.py::test_a_scenarios_seat_is_the_players_at_either_driver_unless_the_flag_says_otherwise; test_captain.py::test_the_console_and_the_server_take_the_seat_flag | the server's `seat_player` call dropped | pass | KILLED (the first) | 6.8; 1.1 |
| 04-C | four (below) | the pilot's news written to the papers under `port.id` | pass | SURVIVED (all four) | 8.3 to 22.5 each |

### 04-A: back and fill ends short

```diff
-  cycles: 2       # back and fill this many times, then lie to aback
+  cycles: 0       # back and fill this many times, then lie to aback
```
(`data/evolutions/back_and_fill.yaml:21`.) Live, on test_catalogue.py's own frigate world and
orders: "Backed the main topsail" 2 lines and "Filled" 1 with the fault, 3 and 2 without. (So
`cycles: 0` does not end the evolution at once, as the reader said: it ends a cycle short; the
script reads the figure loosely. Not chased further.) Tests chosen by
`grep "back and fill\|back_and_fill" tests/`, run: test_catalogue.py
`::test_backing_and_filling_keeps_her_place_and_leaves_her_lying_to` (strict xfail: `x` both
ways, so it stays an expected failure), `::test_whole_ship_orders_start_their_evolution[back and fill-back_and_fill]`,
test_settee.py `::test_the_untried_manoeuvres_each_run_to_an_end[back and fill-ship.hove_to-None]`,
test_bowsprit_yards.py `::test_backing_and_filling_their_sails_are_hauled_up`. All passed.
SURVIVED.

### 04-B: `--seat` at the browser

```diff
     if seat:
         from freesail.agents.seat import seat_player
-
-        seat_player(world, seat, door="browser")
```
(`freesail/ui/server.py:1834-1836`.) test_scenarios.py::test_a_scenarios_seat_is_the_players_at_either_driver_unless_the_flag_says_otherwise:
```
E       AttributeError: 'NoneType' object has no attribute 'station'
tests/test_scenarios.py:288: AttributeError
```
KILLED: the reader's claim is refuted (the test is outside his files; it seats the player
through the server's `prepare_game`). test_captain.py's flag test passes. But the same
test's name says "at either driver" and it drives only the server: with 04-4's console fault
planted again it passes (7.5 s), so 04-4 stands; no test runs the console's seating.

### 04-C: the pilot's news under the wrong port name

```diff
-                for line in papers.news_heard(f"the pilot off {port.name}"):
+                for line in papers.news_heard(f"the pilot off {port.id}"):
```
(`freesail/world/dealings.py:865`.) Live (the 04-2 boarding): the paper reads "by the pilot off
falmouth" (the id) for "by the pilot off Falmouth". Tests chosen by grep for `pilot off`,
`news_heard`, `port.news` and run: test_date_and_war.py
`::test_the_war_is_what_the_ship_knows_never_the_worlds_table` (9.0 s),
`::test_the_pilots_news_enters_what_it_changed_in_the_papers` (8.3 s),
test_known_truths.py `::test_truth_7_241_the_war_is_what_the_ship_knows_and_the_news_is_entered_in_her_papers`
(11.2 s), test_ports.py `::test_the_pilot_comes_off_in_his_cutter_hails_boards_and_is_a_person_aboard`
(22.5 s). All passed: each that reads the papers calls `news_heard` with the literal "the pilot
off Falmouth" itself, and the one that boards the pilot never changes the war first, so the hook's
loop has nothing to write. Taken with 04-2: the hook that puts the pilot's news in the papers is
run by no test with anything to write. SURVIVED.

## tests-05, the faults to plant

| # | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 05-1 | test_gale.py::test_headed_full_and_by_the_helm_keeps_her_away_and_says_so_once | the `helm.kept_away` line deleted | pass | SURVIVED | 5.7 |
| 05-2 | test_far_action.py::test_a_packet_that_fights_is_brought_to_by_the_privateers_rounds_and_taken | a British far ship fires no shot | pass | SURVIVED (fault inert here: see below) | 15.9 |
| 05-3 | test_fight.py::test_the_rules_captain_opens_musketry_within_a_cable_and_serves_out_the_arms_by_his_doctrine | the French kit's musketry never hits | pass | SURVIVED (fault inert here; survives three more) | 9.7 |

### 05-1

```diff
     if d.helm_mode is HelmMode.FULL_AND_BY:
         what = f", the {_sail_words(ship, sail)} lifting" if isinstance(sail, str) else ""
-        ship.note(
-            "routine",
-            "helm.kept_away",
-            f"Kept her away{what}, the wind {deg}° on the {side} bow.",
-            data={**data, "sail": sail},
-        )
         return
```
(`freesail/physics/integrate.py:253-258`.) Live, the test's own world and wind shift: the
`helm.kept_away` lines are `[]` with the fault and `['Kept her away, the fore topsail lifting,
the wind 39° on the starboard bow.']` without. Output: 1 passed (`len(kept) <= 1`). SURVIVED.

### 05-2

```diff
-        shots = whole + (1 if rng.random() < frac else 0)
+        shots = 0 if firer.nation == "britain" else whole + (1 if rng.random() < frac else 0)
```
(`freesail/combat/far.py:187`.) Output: 1 passed. But the fault is inert in this test: the
test's own body run to the packet's striking gives, with the fault and on the pristine code
alike, `packet rounds_fired 0`, `privateer rounds_fired 87`, six rounds each. The packet
(three 12-pdr carronades, `random_m` 731.5 m) never fires one shot before she strikes: the
docstring's "fires her guns within her four cables" is false of the test's own run, and the
assertion at :361 (`rounds_fired >= 0`) hides it. The reader's claim stands and is worse than
he said: the test cannot see the packet's fire because there is none to see. SURVIVED.

### 05-3

```diff
-    if range_m >= MUSKET_SHOT_M:
+    if range_m >= MUSKET_SHOT_M or kit.get("volley_s") == 30:
```
(`freesail/combat/small_arms.py:183`.) Live: `hit_chance({'volley_s': 30, 'hit_at_50_yd':
0.05}, 20.0)` gives 0.0. The named test: 1 passed. Inert here: on the pristine code the test's
own world after 540 s has 0 of our people hurt, so the closing `all("musket ball" in ...)`
runs over an empty list and the docstring's "our people fall to his musketry" is false of its
own run. Three more musketry tests run with the fault, all passed:
test_fight.py `::test_the_hit_chance_falls_with_the_square_of_the_range_to_nought_at_musket_shot` (0.6 s),
`::test_the_marines_fire_by_volley_within_musket_shot_and_her_people_fall` (15.0 s),
test_known_truths.py `::test_truth_7_179_a_volley_within_musket_shot_fells_the_near_decks_men_and_the_quarterdecks`
(11.5 s). The French marines can be made harmless at any range and no test of the four sees it.
SURVIVED.
