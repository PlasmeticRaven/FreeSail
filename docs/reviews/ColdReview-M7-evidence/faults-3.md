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
