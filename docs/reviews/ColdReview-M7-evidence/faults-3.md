# Faults planted: runner 3 (tests-06, tests-07, tests-08)

Scratch copy `scratchpad/m/3`, restored from `scratchpad/mut` after each fault and checked
with `diff -r -q` on `freesail/`, `data/` (less `charts`), `tools/` and `tests/`. Every run
was `python3 -m pytest -q -p no:cacheprovider -x <node id>` from the scratch copy, one
process. The scratch copy is not a git checkout, and the real tree is a shallow clone
without `f5be9110` (`git cat-file -t f5be9110`: "Not a valid object name"), so the
"against git" tests skip in both.

| No. | Test (file::name) | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 06-1 | test_hull.py::test_leeway_change_is_noted_at_most_once_a_minute | once-a-minute clause deleted | pass | SURVIVED (suite too) | 1 |
| 06-2 | test_hull.py::test_all_four_ships_run_under_bare_poles | sail and spar windage 0 | pass | SURVIVED (test_sea kills) | 2 |
| 06-3 | test_hull_cutter.py::test_the_drawn_hull_is_reported_beside_the_filed_figures | drawn displacement x 1.10 | pass | SURVIVED (lugger, brig pins kill) | 1 |
| 06-4 | test_hull_cutter.py::test_a_diff_of_her_physics_keys_against_git_shows_none; test_hull_brig.py::test_no_figure_the_physics_or_the_gunnery_reads_moved[data/ships/brig.yaml] | cutter mast rating +20 kN, brig GM +0.2 m, generator and files alike | **skip** | SURVIVED (skip; suite too) | 1 |
| 06-5 | test_indefatigable.py::test_her_drawn_hull_stands_within_its_bands_and_moves_nothing | 64's QD port half-breadths in 0.2 m | pass | KILLED | 2 |
| 06-A1 | (no test) leeway line flood | as 06-1; 5 tests run | - | SURVIVED | 1-11 |
| 06-A2 | (no test) no windage under bare poles | as 06-2; 3 tests run | - | KILLED | 1-3 |
| 06-A3 | (no test) rating changed in the generator | as 06-4 | - | SURVIVED | - |
| 07-1 | test_longitude.py::test_the_lookouts_estimate_is_drawn_once_and_held_while_she_makes_no_way | log line's estimate from the true distance | pass | SURVIVED (test_lookout kills) | 12 |
| 07-2 | test_mends_109.py::test_words_of_the_dialect_go_to_the_dialect (2 cases) | latitude-sight synonyms moved to "work up the reckoning" | pass | SURVIVED (truth 7-540 kills) | 7 |
| 07-3 | test_knowledge.py::test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks | "Not to be had in the cabin" kept for ever | pass | SURVIVED (suite too) | 13 |
| 07-4 | test_knowledge.py::test_the_boat_away_with_the_player_reads_the_ship_by_sight_and_hail_alone | word not written in other hulls' logs | pass | SURVIVED (say-is-heard test kills) | 22 |
| 07-5 | test_longitude.py::test_the_dialect_reads_the_new_rows_for_nothing_and_the_events_are_named | "east of" / "west of" swapped | pass | SURVIVED (test_reckoning kills) | 7 |
| 07-6 | test_mcp_server.py::test_the_chart_and_the_ships_view_come_as_images_drawn_by_the_open_page | `pic = None` in `Desk.picture` | pass | KILLED | 3 |
| 07-B1 | (no test) lugger forereaches hove to | helm untended, jib drawing, luggers only | - | SURVIVED | 8 |
| 07-B2 | (no test) `at a sounding` never fires | dispatch skips the event | - | KILLED (truth 66) | 33 |
| 07-B3 | (no test) word left standing behind shut ports | `self.word = None` removed | pass | KILLED (as predicted) | 2 |
| 08-1 | test_officer.py::test_the_handover_is_asked_for_at_a_reserve_in_tokens_and_of_an_officer_off_watch; ::test_the_handover_note_is_asked_for_at_the_budgets_fraction_and_folds_the_conversation | size threshold deleted | pass | SURVIVED, SURVIVED (2 others kill) | 4, 5 |
| 08-2 | test_orders.py::test_table[frigate: veer cable], [frigate: veer to ninety fathoms] | "veer cable" starts heave_in | pass | SURVIVED (test_anchor kills) | 2 |
| 08-3 | test_orders_m4a.py::test_trim_the_sail_and_tend_the_sheets (15 cases) | trimmed_sheets reversed | pass | SURVIVED | 8 |
| 08-4 | test_ordnance.py::test_the_kings_cutter_completes_her_magazine_of_the_ordnance_free_in_the_sound | reserve dropped from real `wanting` | pass | SURVIVED (2 others kill) | 4 |
| 08-5 | test_people.py::test_send_for_brings_a_man_to_where_the_captain_is_by_the_messenger | `PASS_THE_WORD_S = 3600` | pass | SURVIVED (suite too) | 14 |
| 08-6 | test_orders.py::test_take_a_fix_is_completed_from_the_marks_in_sight | "A and B and A" offered first | pass | SURVIVED | 8 |
| 08-A | (no test) messenger an hour | as 08-5; 5 tests run | - | SURVIVED | 14-22 |
| 08-B | (no test) real magazine without the reserve | as 08-4 | - | KILLED | 3, 1 |
| 08-C | claim, not a fault: handover at 16,384 | pristine code | - | CLAIM STANDS (worse) | - |

"(suite too)" means that no other test run caught it either; "(X kills)" names the test
outside the named one that failed with the fault in.

## 06-1 Leeway noted more than once a minute

```
--- mut/freesail/physics/integrate.py
+++ freesail/physics/integrate.py
@@ -524,7 +524,6 @@
         not (st.at_anchor or st.aground)  # the stream past her at anchor is not leeway
         and d.u >= units.knots_to_ms(hp.WAY_ON_KN)
         and abs(d.leeway - st.last_noted_leeway) > hp.LEEWAY_NOTE_THRESHOLD
-        and st.seconds_since_leeway_note >= hp.LEEWAY_NOTE_INTERVAL
     ):
```

Live: the test's own set-up (frigate, thrust 30 kN, side 40 kN, 600 s) gives leeway notes at
seconds 5 and 65 pristine, and at 5 and 37 with the fault: two notes 32 s apart. The test
still passes (`.` in 1 s). It asserts only `len(leeway) <= 10` in ten minutes and that each
note changes by over a degree (`tests/test_hull.py:389-391`); nothing reads the interval
between notes. **SURVIVED**: the reader's claim stands.

## 06-2 No windage under bare poles

```
@@ -1551,6 +1551,7 @@
 def _sail_windage_area(ship: Ship, sail: Sail) -> float:
+    return 0.0  # FAULT
@@ -1575,6 +1576,7 @@
 def _spar_windage_area(spar: Spar) -> float:
+    return 0.0  # FAULT
```

Live: after the test's 60 s, pristine, the frigate, schooner, cutter and brig have drifted at
0.28, 0.48, 0.62 and 0.38 m/s (4 to 9 m east, 8 to 17 m north). With the fault all four are
at 0.0000 m/s, x = y = 0.000: they do not move at all. The test passes (2 s): it asserts
speed `< 2 kn`, finite position, and an apparent wind that is non-zero
(`tests/test_hull.py:457-461`), and a ship dead in the water with the true wind on her
satisfies all of them. **SURVIVED**.

## 06-3 The cutter's drawn displacement 10% heavy

```
@@ -181,7 +181,7 @@
-    return _displacement(_built(spec))
+    return _displacement(_built(spec)) * 1.10  # FAULT
```

The cutter's test passes (1 s): 105.5 t becomes 116 t, +9.5%, inside the 15% band
(`tests/test_hull_cutter.py:248`). Its printed line still says "drawn displacement 105 t
against the filed 106 t (-1%)", because `form.check` computes the figure with
`_displacement(built)` itself and not through `drawn_displacement_kg`
(`freesail/ship/form.py:195`): the line the test prints is not the figure the test
asserts. Live and caught elsewhere, as the reader said:
`test_hull_lugger.py::test_the_drawn_hull_is_reported_beside_the_filed_figures` fails
(`assert 111638.408343447 == 101500.0 ± 2.0e+03`, line 520) and
`test_hull_brig.py::test_the_drawn_displacement_and_depth_are_reported_beside_the_filed_ones`
fails (`assert 332959.3454923103 == 303000.0 ± 3.0e+03`, line 445). **SURVIVED** for the
named test; the fault is caught by the suite.

## 06-4 A physics figure moved in the cutter's and the brig's files

The cutter's main mast rating is not a literal in the generator but the result of its
rating pass, so the fault went into that pass, keyed to the cutter; the brig's GM is a
literal. The files were regenerated to a scratch directory and the changed ones copied in
(the brig's literal is shared, so `merchant-brig.yaml` moved too).

```
--- mut/tools/gen_ships.py
+++ tools/gen_ships.py
@@ (rate_spars, after the notes line, about 1481)
             self.notes[spar["id"]] = (self.notes.get(spar["id"], "").rstrip() + " " + how).strip()
+            if self.doc["ship"].get("name") == "Sherbourne" and spar["id"] == "main.mast":  # FAULT
+                spar["rating_kn"] = round(spar["rating_kn"] + 20.0, 1)  # FAULT
@@ -7008,7 +7008,7 @@
-            "gm_m": 0.95,
+            "gm_m": 1.15,
regenerated: cutter.yaml:175  rating_kn: 202.4 -> 222.4
             brig.yaml:53      gm_m: 0.95 -> 1.15
             merchant-brig.yaml:40 gm_m: 0.95 -> 1.15
```

Named tests: both skip ("the base commit f5be9110 cannot be read here", "f5be9110 is not in
this checkout"). The likeliest others (grep for `202.4`, `gm_m`, `rating_kn` in the tests),
all pass: `test_ship_particulars.py::test_generator_reproduces_the_committed_files` (the
generator and files agree, as a builder's change would leave them),
`::test_brig_hull_is_harpy_of_1796` (GM band 0.8 to 1.2, line 340),
`::test_cutter_sail_plan_follows_fincham_and_steel`,
`test_hull_cutter.py::test_the_hull_figures_stand_as_filed` (holds the hull only), and
`test_hull_brig.py::test_one_hull_in_two_roles_alike_but_her_own_two_guns_ports`.
**SURVIVED** (by skip): the tests that promise "no physics figure moved" cannot fail in a
shallow checkout, and nothing else pins those two figures.

## 06-5 The 64's quarterdeck ports moved in 0.2 m


```
--- mut/tools/ships/indefatigable.py
+++ tools/ships/indefatigable.py
@@ -929,7 +929,7 @@
     qd_ports = [
-        (x, wl1_above_k(x) + s, interp(TOP_TIMBER, x) + PLANK_FT) for x, s in QUARTERDECK_SILLS
+        (x, wl1_above_k(x) + s, interp(TOP_TIMBER, x) + PLANK_FT - 0.2 / 0.3048) for x, s in QUARTERDECK_SILLS
     ]
regenerated: sixty-four.yaml:81 quarterdeck half-breadths 4.01..5.18 -> 3.81..4.98 (only file changed)
```

Measured first: pristine, the 64's quarterdeck gaps were +0.173 to +0.269 m (upper deck to
+0.386); with the fault +0.373 to +0.469. The test fails:
`AssertionError: ('data/ships/sixty-four.yaml', -0.09654782195812839, 0.46868581842714274)`,
`assert 0.46868581842714274 <= 0.4` (`tests/test_indefatigable.py:718`). **KILLED**: the
reader's suspicion is refuted for 0.2 m. The headroom is thin all the same: the quarterdeck
stands 0.131 m inside the band, so a move of 0.1 m would pass (computed from the gaps, not
run).

## 06, faults "no test in my files would catch"

- **A1, the leeway line every few seconds** (fault 06-1 planted again). Grep of the tests for
  `ship.leeway`, `LEEWAY_NOTE_INTERVAL`, `seconds_since_leeway`, `Leeway [0-9]`; run with the
  fault: `test_readings.py::test_the_log_writes_no_leeway_line_without_way_on`,
  `::test_course_and_leeway_are_not_readings_with_no_way_on`,
  `test_rollup.py::test_the_words_come_from_the_kinds_and_counts`,
  `test_settee.py::test_the_luggers_tack_and_wear_are_as_they_were` (both cases; it filters
  `ship.leeway` out of the log it compares, line 1455), and the named test. All pass.
  **SURVIVED** in the suite as far as grep reaches.
- **A2, no windage under bare poles** (fault 06-2 planted again). Caught three times:
  `test_sea.py::test_windage_under_bare_poles_is_measured_and_recorded` fails
  (`assert 2.5 <= 0.0`, `tests/test_sea.py:503`: the frigate running under bare poles makes
  no way), `test_evolutions.py::test_cutting_away_a_boom_...` fails at line 1373
  (`_spar_windage_area(boom) > 0.0`), `test_lateen.py::test_the_course_draws_on_the_gaffs_curve_...`
  fails at line 182. **KILLED** by the suite; the reader's file alone would not.
- **A3, a spar's rating or a GM changed in the generator and the file regenerated**: that is
  fault 06-4, run above with five other tests. **SURVIVED**.

## 07-1 The lookout's log line carries the true distance


```
--- mut/freesail/world/lookout.py
+++ freesail/world/lookout.py
@@ -646,7 +646,7 @@
         return d | {
             "relative": relative_words(math.radians(s.bearing_deg) - heading_rad),
-            "estimate": estimate_words(s.judged_m),
+            "estimate": estimate_words(s.distance_m),
         }
```

Live, in the test's own world (ten miles south of the Lizard): the Lizard's
`lookout.sighting` line's data says "three leagues" (the truth, 18,520 m) while its text and
the reading say "four leagues" (the eye's, 23,924 m); pristine all three say four. The named
test passes (12 s). Its line 587 is worse than `or True` alone: it compares the reading's
first item (the Lizard) with `w.log[-1]`, which in that world is Mullion Island's line
("five leagues"), so pristine the assertion would be false even without the fault; the
`or True` hides a wrong comparison, not a flaky one. Caught elsewhere as the reader
predicted: `test_lookout.py::test_a_landfall_is_notable_the_reading_carries_it_and_the_land_lost_is_said_once`
fails, `AssertionError: assert ('three leagues' == 'four leagues'` (line 102).
**SURVIVED** for the named test; caught by the suite.

## 07-2 The latitude's sight sent to "work up the reckoning"


```
--- mut/data/vocabulary.yaml
+++ data/vocabulary.yaml
@@ -589,7 +589,8 @@
   work up the reckoning:
-    synonyms: [work the reckoning, work up the dead reckoning, bring up the reckoning, the day's work]
+    synonyms: [work the reckoning, work up the dead reckoning, bring up the reckoning, the day's work,
+               take a sight for the latitude, take a sight for latitude]
@@ -598,7 +599,7 @@
-               take a sight for the latitude, take a sight for latitude, take the latitude,
+               take the latitude,
```

Live: on the test's frigate, "take a sight for the latitude" answers `reckoning.worked`
("The reckoning worked up: 50° 25' N, 3° 30' W by account...") where pristine it is
`order.rejected` ("The sun is not yet on the meridian..."). Both cases pass: the test asserts
only that the kind is not `free.line` and the text lacks "nothing of that name"
(`tests/test_mends_109.py:107-108`); its `kind` parameter, "navigation", is never used.
Caught elsewhere: `test_known_truths.py::test_truth_7_540_a_free_order_that_finds_nothing_is_refused_and_one_that_did_is_said`
fails, `AssertionError: assert ('reckoning.worked' == 'order.rejected'` (line 16152).
**SURVIVED** for the named test; caught by the suite.

## 07-3 The "Not to be had in the cabin" line kept after he comes on deck


```
--- mut/freesail/agents/harness.py
+++ freesail/agents/harness.py
@@ -2033,14 +2033,15 @@
-    @staticmethod
-    def _readings_elsewhere(world: Any, senses: knowledge.Senses) -> str | None:
+    def _readings_elsewhere(self, world: Any, senses: knowledge.Senses) -> str | None:
         """..."""
+        stuck = getattr(self, "_elsewhere_fault", None)  # FAULT: the first answer kept
         if senses.everything:
-            return None
+            return stuck
         rows = knowledge.rows_elsewhere(senses)
-        return knowledge.elsewhere_words(rows, senses)
+        self._elsewhere_fault = stuck or knowledge.elsewhere_words(rows, senses)
+        return self._elsewhere_fault
```

Live: in the test's world, after the test's `w.run(3700)`, `w.submit("go on deck")`
(`captain.on_deck`) and another 3,700 s: pristine the two samples on the quarterdeck carry
`readings_elsewhere = None`; with the fault both still say "Not to be had in the cabin: the
true wind, ...". The named test passes (13 s): its "on deck again ... the line is gone"
check reads `samples(h)[0]`, the first sample, taken before he went below
(`tests/test_knowledge.py:249`), and the test never brings him on deck. Also run with the
fault, all pass: `::test_knowledge_all_turns_the_rule_off` (line 311),
`::test_the_lookouts_station_reads_the_horizon_and_no_instrument` (343),
`::test_the_masters_days_work_is_done_in_the_gunroom_by_the_rules_master_and_a_model_alike`
(1525: `"speed" in ... or "readings_elsewhere" not in ...`, carried by its first leg).
**SURVIVED**: the reader's claim stands, and no test in the file catches it.

## 07-4 A word said on deck no longer written in the other hulls' logs


```
--- mut/freesail/orders/stations.py
+++ freesail/orders/stations.py
@@ -637,15 +637,6 @@
         data["notable"] = True
-    for hull, names in elsewhere.items():
-        # the word as heard aboard another ship, in her log, for her people's samples
-        hull.record(
-            Severity.NOTABLE if data.get("notable") else Severity.ROUTINE,
-            kind,
-            line,
-            actor=str((getattr(ship, "extra", None) or {}).get("order_actor") or "the captain"),
-            data={**data, "heard_by": names, "said_from": here},
-        )
     return kind, line, data
```

The named test passes with the fault. Its hearing check is guarded by
`if bearing_cables(w, frigate, boat) <= 4` (`tests/test_knowledge.py:1821`), and the guard
cannot be true: the helper (`tests/test_knowledge.py:1828-1832`) takes the second value of
`geo.bearing_and_distance`, which is metres (`freesail/world/geo.py:148-150`), names it `nm`
and multiplies by ten. In the test the two hulls are at 49° 31' N and 49° 32' N, 5° 31' W,
about 1,063 m apart (5.7 cables), and the helper returns 10,633 "cables"; the branch would be
taken only within 0.4 m. Pristine, too, the boat's log holds no "launch ahoy" line at that
range. Caught elsewhere, as the reader said:
`::test_a_say_is_heard_on_every_hull_within_hearing_and_written_as_heard` fails,
`assert heard and heard[0].data["heard_by"] == ["captain"]` / `assert ([])`.
**SURVIVED** for the named test (by a unit error in its helper, which the reader did not
see); the fault is caught by the suite.

## 07-5 "is east of" and "is west of" swapped in the dialect


```
--- mut/freesail/standing/grammar.py
+++ freesail/standing/grammar.py
@@ -755,8 +755,8 @@
             ("is north of", "north_of"),
             ("is south of", "south_of"),
-            ("is east of", "east_of"),
-            ("is west of", "west_of"),
+            ("is east of", "west_of"),
+            ("is west of", "east_of"),
```

Live: in the test's world (49.75 N, 5.2 W), "the reckoning is west of 5 W" holds `True`
pristine and `False` with the fault. The named test passes (7 s): it asserts only
`holds(...) in (True, False)` (`tests/test_longitude.py:533`), and in its world "the
longitude by chronometer" has no value yet (`readings.value("longitude_by_chronometer")` is
None), so both of its east/west conditions are False pristine and faulty alike. Caught
elsewhere: `test_reckoning.py::test_the_dialect_reads_the_new_rows_for_nothing` fails,
`AssertionError: the reckoning is west of 5 W` / `assert False is True`.
**SURVIVED** for the named test; caught by the suite.

## 07-6 Every keyed fetch of a picture answers 404


```
--- mut/freesail/agents/remote.py
+++ freesail/agents/remote.py
@@ -1280,7 +1280,7 @@
             painter = pictures.painter_of(self.world())
-        pic = painter.get(str(picture_id)) if painter is not None else None
+        pic = None  # FAULT: painter.get(str(picture_id)) if painter is not None else None
         if pic is None:
```

The test fails: `assert len(images) == 1 and images[0].mime_type == "image/png"` /
`assert (0 == 1)` (`tests/test_mcp_server.py:1331`). The reader thought only the no-key 409
at the end touched this road; in fact the MCP bridge itself fetches the picture it returns
through that door (`freesail/agents/mcp_server.py:458` -> `game.picture` ->
`freesail/agents/remote.py:1733`, `GET /api/agents/{name}/picture/{id}` ->
`freesail/ui/server.py:1124` -> `desk.picture`), so the chart and the ship's view come back
with no image. (Pristine, a keyed fetch appended to the test answers 200 with the PNG; with
the fault the copy fails before reaching it, at the same assertion.) **KILLED**: the
reader's claim is refused.

## 07, faults "no test in my files would catch"

**B1, the lugger keeps her way hove to.** The reader's description (the mizen lug left
drawing, the helm amidships) could not be made live as written: the lugger has no square
yards to back (`HeaveToScript.yards` is `[]`, so `fore_and_after()`), and once she is hove
to `keep_lying_to` re-tends her helm and sheets every tick (`tend_lying_to`,
`freesail/evolutions/scripts.py:2669`), so a fault at the heave-to's start alone changed
nothing (two attempts, both identical to pristine to two decimals). The fault planted, for
luggers only (the files keyed on a `fore.lug`):

```
--- mut/freesail/evolutions/scripts.py
+++ freesail/evolutions/scripts.py
@@ -2666,7 +2666,8 @@
         manned = _lying_to_hands_on(ship, info, clock, timing)
-        tend_lying_to(ship, info, dt, wind, timing, sheets=manned)
+        if "fore.lug" not in ship.sails:  # FAULT: a lugger's helm and sheets left untended
+            tend_lying_to(ship, info, dt, wind, timing, sheets=manned)
@@ -2909,7 +2910,9 @@
             sheets_to(self.ship, booms, None, None)
-            if self.headsail is not None:
+            if "fore.lug" in self.ship.sails:  # FAULT: a lugger's helm amidships, jib drawing
+                dyn.target_rudder = 0.0
+            elif self.headsail is not None:
                 sheets_to(self.ship, [self.headsail], "weather", None)
```

Live: in `test_she_heaves_to_with_her_lugs_lowered`'s own world, ten minutes after "heave
to", pristine she has `u = -1.54 kn` (sternway) and holds it 20 minutes on; with the fault
`u = +1.92 kn` ahead and rising (1.95 kn 20 minutes on), the log saying "Hove to on the
starboard tack, under her fore-and-aft canvas, jib sheet to windward, helm a-lee." (the
words are not the deed). Not the three or four knots the reader guessed, but she
forereaches. `tests/test_lug.py` whole (5 tests, 8 s) passes; the named test's last line is
`assert math.degrees(abs(world.ship.dyn.u)) >= 0.0` (`tests/test_lug.py:130`), true of any
number. Grep for a lugger with "heave to" in the other tests finds only `test_lug.py` (the
truths' lugger test, `test_truth_7b_111`, tacks and wears). **SURVIVED.** Note also that
pristine she lies hove to with a knot and a half of sternway, which no test reads either.

**B2, `at a sounding` never fires.**

```
--- mut/freesail/standing/runtime.py
+++ freesail/standing/runtime.py
@@ -402,6 +402,7 @@
                         R.event_matches(spec, e.kind, e.data)
+                        and spec.words != "a sounding"  # FAULT: never dispatched
                         and e.actor != f"{ACTOR_PREFIX}'{rule.name}'"
```

Live: in Carrick Road, `standing order "b": at a sounding then steer 90` and "heave the lead":
pristine it fires ("By standing order 'b': steering 90."); with the fault it does not. Pass
with the fault: `test_log_lines.py::test_at_a_sounding_waits_for_the_bottom` (negative only,
as the reader said), `::test_a_cast_that_finds_no_bottom_is_routine_and_a_sounding_is_bottom_found`
(line 418 calls `event_matches` directly), `test_reckoning.py::test_the_dialect_reads_the_new_rows_for_nothing`
(parses `at a sounding` only). Fails: `test_ground.py::test_truth_66_the_same_passage_with_the_lead_going_hourly_does_not_ground`
(33 s), `AssertionError: assert (1 >= 5)` at `assert len(casts) >= 5` (its "fill away after
the cast" order never fills her away, so the hourly heave-to and cast chain stalls).
**KILLED** by the suite, outside the reader's files.

**B3, "fire" with every lee port shut.** The present behaviour first, pristine, in the
test's own set-up: the reply is `guns.fire`, "Fire the larboard broadside: no gun of it is
loaded and run out yet; the word stands until one bears.", the word `larboard` after the
reply and `None` two seconds on. The reader's account stands: the reply says the word
stands and the next tick drops it, and no test pins the reply's words. The worse fault:

```
--- mut/freesail/combat/guns.py
+++ freesail/combat/guns.py
@@ -924,7 +924,7 @@
         if not self._behind_ports(guns, relative, target):
             return
-        self.word = None
+        # FAULT: the word left standing
```

`test_lee_ports.py::test_a_word_for_a_broadside_given_by_the_order_is_told_at_the_next_tick`
fails, `AssertionError: assert 'larboard' is None` (line 940). **KILLED**, as the reader
predicted.

## 08-1 The handover note asked for whatever the conversation's size


```
--- mut/freesail/agents/harness.py
+++ freesail/agents/harness.py
@@ -3966,8 +3966,7 @@
         size = self._conversation_size()
-        if size < threshold:
-            return
+        # FAULT: the threshold no longer consulted
         if self._handover_asked_at and size - self._handover_asked_at < again:
```

Live: the frigate's officer seated as in the test at 902, with a budget of 200,000 (threshold
140,000): pristine no ask in six samples (the conversation 17,185 to 31,218 tokens); with the
fault the note is asked at 17,185 tokens, 8.6% of the context, and the conversation folded
(revision 1) at the second sample. Both named tests pass, as the reader predicted. Caught
elsewhere: `test_local_runner.py::test_the_handover_is_asked_for_by_the_servers_count` fails
(`assert not any("handover note" in n for n in plain.agent.notices)` / `assert not True`), and
`test_known_truths.py::test_truth_7b_132_a_seated_api_doors_fold_fires_at_the_default_budget_on_a_long_seat`
fails (the fold said at 75,000 tokens, not the 90,000 it pins). Pass:
`test_local_runner.py::test_the_handover_reserve_is_tokens_or_a_share_and_the_larger_when_both`,
`::test_the_two_stopgap_settings_on_the_fake_server` (both read `handover_threshold()` and
never the ask), `test_officer.py::test_what_moved_out_of_the_consent_brief_is_in_the_briefs_of_the_stations`.
**SURVIVED** for both named tests; caught by the suite.

## 08-C The claim as the code stands: the note asked at the first sample at 16,384

Not a fault: tried on the pristine code. The officer seated as in the test at 902 (the
frigate, "set plain sail", the fake model answering an ask with `handover_note`), and
`h.budget_tokens = 16384` (the figure the local runner advises,
`freesail/agents/local.py:604-606`, and the one `test_officer.py:999` shows reaching the
harness from it). Script: `scratchpad/r3/hand.py 16384`, run in the scratch copy.

```
budget 16384 threshold (9830, 1638) size at seat 13646
sample 1 size 17185 asks so far 0 revision 0
sample 2 size 14058 asks so far 1 revision 1
sample 3 size 19169 asks so far 1 revision 1
sample 4 size 13969 asks so far 2 revision 2
sample 5 size 19050 asks so far 2 revision 2
sample 6 size 14009 asks so far 3 revision 3
```

The reader's claim stands, and it is worse than he put it. The brief alone, at the seat, is
13,646 tokens: already past the threshold of 9,830 (six tenths of 16,384) before the officer
has said a word. The note is asked at the end of his first turn and rides the next sample;
the fold leaves the conversation at about 14,000, still over the threshold, so the ask comes
again as soon as it has grown by a tenth (1,638 tokens): three handover notes and three folds
in six samples, for as long as he is seated. At the context the runner itself advises, an
officer spends every other sample writing his handover note. (Whether the real local runner
gives exactly this budget was read from the test at 999, not run through a server.)

## 08-2 "veer cable" starts the heave-in


```
--- mut/freesail/orders/ground_tackle.py
+++ freesail/orders/ground_tackle.py
@@ -69,7 +69,7 @@
-    "veer cable": "veer_cable",
+    "veer cable": "heave_in",
```

Live: on the table's frigate, "veer cable" now answers "Started heave_in on ship." with
`runner.started == [('heave_in', 'ship', {})]`, and "veer to ninety fathoms" starts
`heave_in` with `{'fathoms': 90.0, 'to': True}`. Both rows pass: they give no `evo=`, so
`test_table` checks only the kind and the log's form (`tests/test_orders.py:831-835`).
Caught elsewhere: `test_anchor.py::test_veering_and_the_second_anchor_and_backing_with_the_stream`
fails, `assert abs(best.scope_fathoms - 60.0) < 0.5` / `AssertionError: assert (30.0 < 0.5)`.
**SURVIVED** for the named rows; caught by the suite.

## 08-3 The sheets trimmed reported in reverse


```
--- mut/freesail/orders/verbs.py
+++ freesail/orders/verbs.py
@@ -1315,7 +1315,7 @@
-        "trimmed_sheets": trimmed,
+        "trimmed_sheets": list(reversed(trimmed)),
```

Live: "tend the sheets" reports `['the jib', 'the fore topmast staysail', 'the mizzen
spanker']` for the evolutions started on `['mizzen.spanker', 'fore.topmast_staysail',
'jib']`; pristine the two agree, and the test's first leg (the names in order) holds pristine
for all four rows and fails for all four with the fault. The whole parametrised test passes
(15 cases, 8 s) on its second leg, `or len(data["trimmed_sheets"]) == len(expect.sheets)`
(`tests/test_orders_m4a.py:142-144`), which any list of the right length satisfies.
**SURVIVED**. Weight to a player is low (the order of a list in the order's data); the
weight to the suite is that the assertion on the sheets' names is void.

## 08-4 The real magazine never wants its barrels below made up


```
--- mut/freesail/ship/parts.py
+++ freesail/ship/parts.py
@@ -997,7 +997,7 @@
         established = sum(n * self.charge_of(*k) for k, n in level.items())
-        established += float(self.reserve_lb)
+        pass  # FAULT: established += float(self.reserve_lb)
```

The named test passes (4 s): it runs on `FakeMagazine`, whose own `wanting` adds the reserve
(`tests/test_ordnance.py:81`), so the real method is not under test there, as the reader said.
But the reader's further prediction is refuted: `::test_the_real_magazine_from_the_gunners_filling_to_the_shilling_and_the_page`
(825) fails, at line 847: the refusal reads "Her magazine is complete: ..." where it should
read "Her magazine wants no more shot: ...". And `test_magazine.py::test_receive_wanting_and_spoil_go_by_kind_and_the_wanting_is_to_the_nearest_barrel`
fails, `assert w.powder_lb == 40.0 and w.barrels == 0` / `assert (0.0 == 40.0)`. **SURVIVED**
for the named test; **KILLED** for the reader's fault B (the real `wanting`), twice.

## 08-5 The messenger takes an hour


```
--- mut/freesail/world/people.py
+++ freesail/world/people.py
@@ -91,7 +91,7 @@
-PASS_THE_WORD_S = 60
+PASS_THE_WORD_S = 3600
```

The test passes (14 s against 7 s pristine: it now runs an hour of ship's time and the man
comes at the end of it). It waits `PE.PASS_THE_WORD_S - 1` and then 1 (`tests/test_people.py:123-125`),
whatever the constant is. Fault A (the same fault, "no test pins 60"): every test that
reads the time names the constant (13 uses, in `test_people.py`, `test_letters.py`,
`test_known_truths.py:3692`); none names the figure. Run with it, all pass:
`test_people.py::test_a_watch_keeper_in_his_watch_below_at_night_is_asleep_by_the_bill`,
`::test_a_message_reaches_the_captain_where_he_is_through_the_messenger_and_the_door`,
`test_orders_places.py::test_the_captain_goes_where_he_will_aboard_and_the_deck_is_given_from_the_deck`,
`test_orders.py::test_send_for_the_master_where_the_master_is_the_captain_says_so`.
**SURVIVED** (both the named test and fault A).

## 08-6 A fix offered with the first mark again for its third


The reader gave no line; `_fix_offers` is at `freesail/orders/complete.py:373-395`. The
second of his two forms was planted (the first, the marks reversed, would be caught by the
test's line 2370, which compares the single offers with `_fix_marks` in order; not run).

```
--- mut/freesail/orders/complete.py
+++ freesail/orders/complete.py
@@ -390,7 +390,7 @@
             for c in names
-            if len({a, b, c}) == 3
+            if len({a, b, c}) == 3 or (a != b and c == a)  # FAULT: the first mark offered again
```

Live: after "take a fix by St Mawes castle and Manacle Point " the first offer is now "take a
fix by St Mawes castle and Manacle Point and St Mawes castle". The test passes (8 s): line
2373 asks only that the proper three be somewhere in the list, and line 2375 accepts
`reckoning.fix` or `order.rejected` of each of the first four. The reader expected the bad
offer to be rejected and passed by 2375's second leg; in fact the game takes it as a fix
(`reckoning.fix`, "Fixed by cross bearings: St Mawes castle NNW, Manacle Point WSW; the lines
cut at 80 degrees"): a two-mark fix under three-mark words, the repeated mark dropped without
a word. **SURVIVED**.

## Count

Faults planted against a named test: 17. **Survived 15, killed 2** (06-5, 07-6), not run 0.
Of the 15 that the named test let through, 9 were caught by some other test in the suite
when I looked for one (06-2, 06-3, 07-1, 07-2, 07-4, 07-5, 08-1, 08-2, 08-4), and 6 got past
every test I ran (06-1, 06-4, 07-3, 08-3, 08-5, 08-6). Of the readers' "no test would catch
it" faults: 6 tried as faults (06-A1, 06-A2, 07-B1, 07-B2, 07-B3, and 08-B as 08-4), 3 of
them SURVIVED (06-A1, 07-B1, 08-A; 06-A3 is 06-4) and 3 KILLED (06-A2, 07-B2, 08-B; 07-B3 was
predicted to be caught and was). The claim 08-C stands on the pristine code. One baseline
did not pass: the two "against git" tests of 06-4 skip in this checkout, as they will in any
shallow clone, and so cannot fail.

What the survivals have in common: the assertion that carries the test's name is made void by
a fallback (`or True`, `or len(...) == len(...)`, `>= 0.0`, `in (True, False)`), a guard
that is never true (`if bearing_cables(...) <= 4` on metres taken for miles, a skip when a
commit is absent), a figure read back from the constant under test (`PASS_THE_WORD_S`), or a
check on the first sample when the change comes later; and the things a player sees over
time (how often a line comes, which way she moves, how long a man takes) are where those
voids sit. The suite as a whole is better than the named tests: more than half of the
survivals are caught somewhere else, usually by an older truth or a pin in a neighbouring
file, so the cost is mostly that the named tests prove less than their names say, and
the six that nothing caught are the ones to mend.

Not done: the first form of 08-6 (marks reversed) was not run; the reader's "three or four
knots" for 07-B1 was not reached (the planted fault gives about two); no test file was run
whole except `tests/test_lug.py` (8 s) and the 15 cases of the 08-3 test.
