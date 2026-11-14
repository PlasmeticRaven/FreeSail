# Faults planted: runner 3 (tests-06, tests-07, tests-08)

Scratch copy `scratchpad/m/3`, restored from `scratchpad/mut` after each fault and checked
with `diff -r -q` on `freesail/`, `data/` (less `charts`), `tools/` and `tests/`. Every run
was `python3 -m pytest -q -p no:cacheprovider -x <node id>` from the scratch copy, one
process. The scratch copy is not a git checkout, and the real tree is a shallow clone
without `f5be9110` (`git cat-file -t f5be9110`: "Not a valid object name"), so the
"against git" tests skip in both.

| No. | Test | Fault | Baseline | Result | s |
|---|---|---|---|---|---|
| 06-1 | test_hull.py::test_leeway_change_is_noted_at_most_once_a_minute | once-a-minute clause deleted | pass | SURVIVED | 1 |
| 06-2 | test_hull.py::test_all_four_ships_run_under_bare_poles | sail and spar windage return 0 | pass | SURVIVED | 2 |
| 06-3 | test_hull_cutter.py::test_the_drawn_hull_is_reported_beside_the_filed_figures | drawn displacement x 1.10 | pass | SURVIVED | 1 |
| 06-4 | test_hull_cutter.py::test_a_diff_of_her_physics_keys_against_git_shows_none, test_hull_brig.py::test_no_figure_..._moved[brig.yaml] | cutter main mast rating +20 kN, brig GM +0.2 m, generator and files alike | skip | SURVIVED (skip) | 1 |

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

| 06-5 | test_indefatigable.py::test_her_drawn_hull_stands_within_its_bands_and_moves_nothing | QD port half-breadths in 0.2 m | pass | KILLED | 2 |

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

| 07-1 | test_longitude.py::test_the_lookouts_estimate_is_drawn_once_and_held_while_she_makes_no_way | log line's estimate from true distance | pass | SURVIVED | 12 |

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

| 07-2 | test_mends_109.py::test_words_of_the_dialect_go_to_the_dialect (both cases) | two synonyms moved to the wrong order | pass | SURVIVED | 7 |

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

| 07-3 | test_knowledge.py::test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks | first non-None elsewhere line kept for ever | pass | SURVIVED | 13 |

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

| 07-4 | test_knowledge.py::test_the_boat_away_with_the_player_reads_the_ship_by_sight_and_hail_alone | loop recording the word on other hulls deleted | pass | SURVIVED | 22 |

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

| 07-5 | test_longitude.py::test_the_dialect_reads_the_new_rows_for_nothing_and_the_events_are_named | east_of and west_of swapped | pass | SURVIVED | 7 |

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

| 07-6 | test_mcp_server.py::test_the_chart_and_the_ships_view_come_as_images_drawn_by_the_open_page | `pic = None` in `Desk.picture` | pass | KILLED | 3 |

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
