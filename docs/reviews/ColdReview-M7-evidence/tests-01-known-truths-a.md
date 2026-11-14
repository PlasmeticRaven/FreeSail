# Tests, reader 01: tests/test_known_truths.py, lines 1 to 8700

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read whole, in chunks, lines 1 to 8700
(the first half of 17,391). The last test I read is truth 7-144 (line 8624 to 8699); truth
7-145 starts at line 8702 and is the other reader's. Read also: tests/conftest.py (its
DAY_FIXTURES, SLOW_TESTS and the pace rule, lines 1 to 110 and 648 to 657, and the SLOW_TESTS
entries for this file), and, to judge single tests, freesail/core/events.py 206-330,
freesail/core/world.py 1925-1941, freesail/combat/guns.py 85-120, freesail/world/fishing.py
597-617, freesail/evolutions/runner.py 1235-1280, data/evolutions/wear.yaml, and the test
lists of tests/test_staying.py, test_standing.py, test_fishing.py, test_ports.py,
test_canvas.py, test_studding.py, test_replay.py, test_sea.py, test_director.py,
test_signals.py, test_flags.py, test_captain_trials.py, test_lying_to.py,
test_ships_hierarchy.py. Nothing was run but grep, wc, an import check of four packages and
a few seconds of Python reading the file's syntax tree (to list tests and tiers).

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| tests/test_known_truths.py, first half | 1-8700 | 159 functions (162 cases: 3 parametrised x2); 8 strict xfail; 6 pace | 23 module-scoped: 4 polars/sweeps, 5 more sweeps/gales, 7 whole days or passages (29 to 48 game hours each), 6 harnessed days, 1 seine; plus `cutter_wardroom`, not in DAY_FIXTURES | Proves much through the game, but pins much more than it proves at the scenario level (75 tick constants, 8 digests, 8 line counts, 871 comment lines of re-pin history); a dozen weak or tautological asserts; heavy duplication with other files |

## 1. Count and kind

- **Tests.** 159 test functions in lines 1-8700 (the file has 446 in all). Parametrised: truth 9
  "nothing carries away" (line 377, frigate and schooner), truth 34 sunrise (line 1554, 15 and
  25 knots), the cutter and the brig (line 3597): 162 cases.
- **Tier.** By conftest's rules (DAY_FIXTURES at conftest.py:45-71, SLOW_TESTS, and the pace
  rule at conftest.py:648-657: a `pace` mark or a name ending `holds_truth_51s_floor` /
  `ticks_at_the_build_machines_floor`): **119 functions (122 cases) are slow-tier, 40 are
  fast**. The fast ones: truths 17, 21, 47, 65, 58, 59, 68, 69, 70, 67, 71, 81, 82, 83, 84, 85
  (both halves), 86, 7b-93, 107, 110, 113 to 123, 126, 131, 128, 7-134, 140, 139, 141, 142.
  Pace (slow and pace-marked): lines 2166, 2657, 2750, 3444, 4609, 8461.
- **Strict xfails (8):** truth 3 schooner (283), 11 wear loss (457), 18 spec times (719), 24
  (1054), 26 (1132), 28 (1251), 31 (1374), 7b-100-old (6036).
- **Module fixtures and cost.** `frigate_polar`, `schooner_polar` (14 headings each, ~20 game
  minutes each), `frigate_sweep`, `schooner_sweep` (steering up 2 deg at a time),
  `frigate_yards_alike_sweep`, `frigate_head_yards_sharper_sweep`, `frigate_bowlines_sweep`,
  `frigate_catharpins_sweep`, `frigate_plain_sail`, `frigate_lying_a_try` (hours of storm),
  `frigate_rising_gale` (1.5 h), `gate_day` (29 h), `gate_system_day` (45 h), `gate_5a_day`
  (29 h), `gate_5b_passage` (17 h), `gate_5b_schooner` (17 h), `gate_5c_merchant` (36 h),
  `gate_5c_cruise` (48 h), `gate_6a_intent` (36 h), `gate_6a_fake_captain` (the merchant
  passage again, 36 h, with a harness), `directed_day` (24 h, two harnesses), `voiced_watch`
  (2 h), `needs_days` (71 h), `gerrans_seine`, and `cutter_wardroom` (line 5145: the cutter
  with two harnesses and a seat, 2 h 40 min). Outside fixtures, single tests sail more whole
  days: truth 54 (45 h at line 2356), the thick passage (16 h, 3466), truth 112 (7 h, 6358),
  truth 129 (8 h 40 min, 8012), truth 7-133 (up to 3 h), and the five pace tests rebuild a day
  each.
- **What it proves.** Points of sail, tacking, wearing, heaving to, sail handling and the
  crew (truths 1 to 33); standing orders (34 to 38); the gate days and their replay (48 to 57);
  navigation, ports, other ships (58 to 72); the rules captain and harness doors (77 to 86);
  the director, needs, places, fishing, the harbour (7b-90 to 7b-132); combat and signals
  (7-133 to 7-144).

### Truths as rows: how each proves

Kinds: **G** a ship sailed or an order given and the behaviour asserted by events, order
and bands; **R** the same game replayed or re-run to the same digest (self-consistency, no
pinned value); **P** dominated by pinned exact ticks, a digest, a line count or a golden
text; **U** a function or model driven in isolation, no ship sailed; **T** a tool, a
document, a launcher or a door rather than the game; **X** strict xfail; **pace**.

For the half: **G 112, R 9, P 13, U 4, T 7, X 8, pace 6** (159). Many G tests also pin exact
log texts (truths 21, 33, 34, 35, 37, 38, 68, 70, 7b-104, 7b-114, 7b-115, 7b-117, 7b-128 and
others compare whole sentences with `==`); the P count is only those where the pin is the
substance.

- G: truths 1, 2, 3 (frigate), 4, 5, 6, 7, 8, 9 (x2 tests), 10 (x2), 11 (time), 12 (x2), 13,
  14 (x2), 16, 17, 18 (ratio), 19, the shorten-sail test (760), 20, 21, 23, 24, 25, 26, 27,
  28, 29, 30, 31 (x2), 32, 33, 34 (x2), 35, 36 (x2), 37 (x2), 38, 47, 52, 54, 57, 56, 65, 59,
  60, 61, cutter-and-brig (3598), 68, 69, 70, 67, 71, 81, 79, 80, 82, 83, 84, 85a, 7b-90, 91,
  92, 93, 95, 96, 97, 103, 100, 101, 102, 111, 112, 105, 106, 107, 113, 114, 115, 116, 117,
  118, 119, 120, 121, 122, 123, 124, 126, 125, 131, 127, 128, 129, 7-134, 140, 133, 136, 137,
  141, 142, 143, 144.
- R: 15 (601), 22 (912), 49 (2091), 55 (2376), 5a replay (2639), 72 (4587), 6a replay
  (4816), 85b (5322), 7b-94 (5650).
- P: 48 (2015), 5a constants (2588), 5b passage (3326), thick passage (3460), schooner
  passage (3525), schooner's pilot (3573), merchant constants (4323), merchant Iroise cast
  (4479), cruise constants (4488), cruise speaks (4569), 77 (4734), 6a intent constants
  (4756), 78 (4945).
- U: 53 (2317, the tool's numbers), 58 (3107, `Reckoning` alone), 7-135 (8320, `battery.tick`
  driven by hand with a made `Target` and the private `_firer`), 7-139 (8424, `far.fight`).
- T: primer chapter 9 (2777, a document), 86 (5369), 7b-108 (6584, the launcher as a
  subprocess), 7b-109 (6674, the scenario maker), 7b-110 (6739, the settings file), 7b-130
  (7641), 7b-132 (7810, the API door's fold).
- X: 3 schooner, 11 loss, 18 times, 24, 26, 28, 31 (quarter point), 7b-100-old.
- pace: 51, the day under systems, the region loaded, the passage, the merchant start, 7-138.

## 2. (a) What is no longer there, or a name or docstring that promises another thing

- **Truth 7b-100-old (line 6036-6091), strict xfail of removed behaviour.** The reason
  (6038-6040) says the behaviour (an officer taking the deck into the gunroom) was ruled out
  by package 65; the test is kept "beside the new reading". It tests nothing that exists and
  is in SLOW_TESTS, so every slow run sails it. A strict xfail passes on any exception, so it
  cannot fail unless the removed behaviour comes back. Weight low; sure.
- **Truth 48's docstring against its body.** Docstring 2028-2029: "the heavy-weather routine
  ... its four orders on one tick and all carried out". Body 2060-2067: two orders carried out
  and the close reef refused. The comment at 2051-2059 explains the change; the docstring was
  not mended. Low; sure.
- **The intent schooner's docstring against its body (4756-4813).** Docstring: "is conned
  through the Goulet and anchors in the Bay of Brest in thirteen fathoms and a half ... and
  sells at £270". Body: anchored in the road of Bertheaume "in ten fathoms" (4796), the tin
  unsold (4775-4777, `GATE_6A_INTENT_SOLD_TICK is None`). Low; sure.
- **Truth 7-136's name and docstring against its body (8336-8370).** Name: "a tack with the
  guns served is slower by exactly the hands it takes". The docstring's own figures: cleared
  447 s, guns served under `sail before guns` 436 s (faster). The body asserts
  `sail_first <= cleared * 1.15` (8367), so the served tack is *not* required to be slower,
  and nothing is "exactly". The docstring's "with the guns gone short" is not asserted. Medium;
  sure.
- **Truth 7-140's docstring (8166-8167)** says the first action's privateer fights "an hour
  and fifty-three minutes (truth 7-133)"; truth 7-133's own docstring (8210-8222) says package
  71 moved it to fifty-nine minutes. Truth 7-139's docstring (8430-8431) repeats "near two
  hours". Stale. Low; sure.
- **The naval cruise's docstring (4489-4496)**: "wearing every second hour ... the frigate
  wears and runs her down in three hours"; the body asserts `len(wore) >= 8` (4530) and the
  constants say she is spoken after the bow placing of package 45c. Low; likely.
- **Comment against constant.** Line 1960-1965: "'trim on a shift' fires twelve times, not
  fourteen"; the list at 1966-1981 has fourteen entries, two annotated "two more after
  package 32e". Line 4213: "the cast at the Iroise's mark ... not made since package 37j";
  the test at 4479 and 4397-4398 asserts it is made at 90318 (package 45). Low; sure.
- **Truth 22's comment (922)**: "the journal holds accepted orders only" over an assertion on
  the *log's* kinds. Low; sure.
- **The pace test on the passage (3444-3457).** Docstring: "the queries and the reckoning per
  tick on the passage (the traverse board every tick, the grounding check, the lookout ...)".
  It measures the `gate_5b_passage` fixture's world *after* its 17 hours, when the frigate is
  brought up at anchor in the outer road (asserted at 3378-3383). It measures a ship at anchor,
  not the passage. Medium; sure.
- No assertion commented out, no `assert True`, found in the half.

## 3. (b) Built not to fail

Pins (the count asked for): **75** module constants of exact ticks or tick lists, **8**
digests, **8** line counts (lines 1944-1981, 2492-2525, 2925-3053, 4005-4262, 4642-4722,
4882-4907). Each digest carries a comment trail of earlier values ("1680cb1391720dd8 ...
bff57a00218b7ec5 at 57 (a235022bc8bf8bc7 at 45c)", 2525; the merchant digest's trail at
4255-4262; the schooner's at 3031-3041). The comments say each move was proved "by bisection"
or "the toggle gives the old digest" and point to docs/dev, which a reader of the test
cannot check. These are re-pinned to whatever the code does each package: they detect change,
never correctness. The half holds about 871 comment lines, most of them this history.

Specific findings:

1. **Truth 52, line 2303: `assert all(events(world, "weather.squall_over")), "each squall
   ends in the log"`.** `all()` over a list of Event objects is true for an empty list and for
   any non-empty one. It cannot fail. The record is at freesail/core/world.py:1935-1941. High
   for what it claims; sure.
2. **Truth 50, line 2131: `assert lines == [e for e in log if kept(e)]`.** The view and the
   expectation both use `kept()` from the code under test (freesail/core/events.py:206-209,
   used by `RollupView` at 299). The truth is "every notable and urgent line"; if `kept()`
   dropped notable lines both sides would agree and the counts at 2135-2139 would still sum.
   Medium; likely (by reading, not run).
3. **Truth 51, line 2182: `assert TICKS_PER_SECOND_HEADLESS / OWNER_TO_BUILD_RATIO >
   BUILD_MACHINE_MEASURED`.** Three constants of the test file (3000 / 2.0 > 1000). Asserts its
   own set-up. Low; sure. The floor itself (2163) is half the measured figure, so a pace
   regression of up to half passes all five floors in the half; the docstrings' own
   measurements (843, 862 at 2662) sit 70% above it.
4. **Truth 7-138, line 8484**: the floor is `crews.CREWED_FLOOR_TICKS_S`, read from the code
   under test, 60.0 (freesail/world/crews.py:99), against 538 measured (docstring 8466). A
   nine-fold slowdown passes. Medium; sure.
5. **Truth 7-144, lines 8658-8660**: `assert [s for _, s in states][:3] ==
   ["investigating a stranger", "chasing"][:2] or ("chasing" in [s for _, s in states])`. The
   second operand is already true whenever the loop broke on "chasing", and line 8661's
   `next(...)` would raise anyway; the first operand (a three-slice equal to a two-list) adds
   nothing. Whether the captain investigated first is not tested. Low; sure.
6. **The intent schooner, line 4777: `assert GATE_6A_INTENT_SOLD_TICK is None`**: a test
   constant asserted equal to itself. And 2622: `... == GATE_5A_LOST == []` (the constant is
   `[]` at 2500). Low; sure.
7. **Truth 53 (2317-2348)**: the band is `CLIMATOLOGY_TOLERANCE_PCT` from
   tools/climatology_check.py:43 (5), and the counts are the tool's own `run` and `table`. It
   tests a tool against its own tolerance; widen the tool and it passes. Low; sure.
8. **Truth 7b-105, line 6456-6460**: the sale is checked against `F.price_of(f, False)`, the
   same function the sale uses (freesail/world/fishing.py:597, 615-617). The truth is "at the
   market's price"; a wrong lookup in `price_of` would pass. Medium; likely.
9. **Truth 17, line 657: `settled_at <= 900`**: the loop runs 900 ticks and sets `settled_at =
   t - 60`, so the bound is vacuous; only `is not None` counts. Low; sure.
10. **Truth 7b-104, line 5953: `assert first is None or not first.by_hand`**; truth 7b-121,
   line 7370: `assert kept is None or not [...]`; truth 7b-125, line 7628: an assertion
   behind `if w.tide_state.flood is None:`, which may never run, and line 7626 an upper
   bound only (`len(swung) <= turns`) where the docstring promises "one now". Low; likely.
11. **Bands moved to the measured value, the truth's words softened.**
   - Truth 10 (403-424): "gains to windward" became the sum of three tacks with one allowed to
     lose ground; the docstring's own figures (51, -37, 27 m) show a knife's edge.
   - Truth 59 (3172-3198): the comment says the truth's "onto the contour" "held to the letter
     only while ..."; it is now "within seven fathoms of the cast's depth on the chart".
   - Truths 10 and 19's tack time widened since package 37p (19's comment 748: "465 s since
     package 37p's trim, 300 to 420 before"), now 285-600 and 300-600.
   - Truth 36 wandering wind (1689): `1 <= len(fired) <= 4`, measured 2.
   - Truth 7-133 (8244): 45 minutes to 3 hours, measured 59 minutes (justified in the file by
     "rule 7"). Truth 30 (1319): 0.6 to 1.2 kn for the spec's "about a knot".
   Medium; sure that the bands were moved, a judgement whether each is too wide.
12. **The xfail pairs: a passing test asserting the shortfall.** Truth 24's passing test
   asserts `0.05 <= as_built - alike < 0.25` (1048) and `closer < POINT / 4` (1051): it fails
   if the game ever reaches the spec, and its xfail twin (1065-1071) XPASSes then too. Truth 26
   likewise (`closer < POINT / 2`, 1126). The owner's rulings are pinned as passing tests of
   the deficiency. All eight strict xfails pass on *any* exception in their bodies (an
   AttributeError counts), so none can detect a break, only a spec met. Medium; sure.
13. **Unbounded loops**: `_one_shot_of_the_seine` (6404-6410, three `while` loops) and truth
   7b-106 (6495, `while v.brain.intent.kind == "fish"`). A fault hangs the suite rather than
   failing a test. Low; sure.
14. **Order dependence on a shared fixture.** The pace test on the passage (3444) runs 3,000
   more ticks on the shared `gate_5b_passage` world; the constants test (3326) passes only
   because it runs first in file order. Run alone or reordered (`-k`, a random-order plugin)
   the constants test would see a longer log. Truth 7b-105 likewise runs 25 hours on the
   shared `gerrans_seine` world (6462). Medium; likely.
15. **Skips.** Twelve `importorskip` (fastapi, the vendor SDK of pyproject.toml:29, keyring, httpx): truths 83, 86,
   7b-108, 109, 110, 130, 132. All four packages import on this machine, so they run here; on
   a machine without them seven truths skip without a word in the summary line. Low; sure.

## 4. (c) Tests that might be one

- **Exact duplicates in this file.** The merchant Iroise cast test (4479-4485) is lines
  4397-4398 of the merchant constants test, verbatim. Truth 77 (4743-4753) re-asserts the
  merchant and cruise digests the constants tests already assert (4471, 4566). Truth
  7b-100-old and 7b-100 sail the same scenario twice. Truths 7b-112 (7 h) and 7b-129 (8 h 40
  min) each sail `trial-station-gale` separately, and tests/test_captain_trials.py's
  `station_gale` fixture sails it again (16 h).
- **Duplicates in other files, by helper or scenario:**
  - truth 56's first half = tests/test_sea.py:342 (same `reef_ticks`,
    `frigate_under_plain_sail`, `heavy_sea_aboard`, the same 1.4-1.7 band);
  - truth 85b = tests/test_replay.py:752 (the same `three_stations`, `_restamp`, sampling
    monkeypatch);
  - truth 29 = tests/test_studding.py:225/234 (it imports `weather_studding_sails_at_nine_points`);
  - truth 27 = tests/test_canvas.py:319; truth 10 misses stays = tests/test_staying.py:221;
  - truth 35 = tests/test_standing.py:997 and 969; truth 38 = tests/test_standing.py:1252;
  - truths 7b-92, 93, 94, 123, 126 = tests/test_director.py:652, 483, 681, 459, 1551;
  - truths 7b-105, 106, 107 = tests/test_fishing.py:145/202, 223, 255;
  - truths 69, 70 = tests/test_ports.py:333/1155, 1116;
  - truth 7-143 = tests/test_signals.py:159, 348;
  - `frigate_sweep`, `schooner_sweep`, `frigate_polar` are built again by
    tests/test_ships_hierarchy.py:90-111 from this file's own helpers (both lists in
    DAY_FIXTURES): the same sweeps sailed twice a slow run.
- **Families for one table-driven test.** The five pace tests (2166, 2657, 2750, 3444, 4609)
  repeat one best-of-three loop over different worlds. The "saved and replayed to the same
  digest" check appears in about twenty tests in the half (15, 22, 49, 55, the 5a replay, 72,
  the 6a replay, 85a, 85b, 7b-94, 95, 100, 101, 102, 114, 118, 121, 131 and the old 100). The
  "has its own constants" tests (2588, 3326, 3460, 3525, 4323, 4488, 4756) are one shape: ticks,
  lines, digest per scenario.
- **Helper library.** 32 other test files import from tests/test_known_truths.py (grep
  `from tests.test_known_truths` / `from test_known_truths`): a change to `make`,
  `under_plain_sail`, `pointing_sweep` here moves them all.
- **Shadowed helper.** `_until` is defined twice at module level (6170 with `minutes=300`,
  "not done in time"; 7124 with `step=60, most=240`, "never came"). Python keeps the second, so
  truths 7b-101 and 7b-102 run under a 240-minute limit and the other message, not the one
  written beside them. Low; sure. (`CUTTER` is also assigned twice, 5080 and 8043, same value.)

## 5. Anything else

- **Good, hard tests (one line each).** The shorten-sail test (760-830) proves the reef's
  hands arriving tick by tick and the topgallants in during the reef. Truth 37 (1722-1765)
  derives its tick from the wind ramp's arithmetic (1732), not a pin. Truth 65 (2690-2747)
  proves the light by date and range. Truth 7b-115 (6986-7042) proves ten free lines refused
  with state unchanged. Truth 78 (4961) asserts the harnessed log equals the unharnessed log
  line for line, a strong equivalence. Truth 7b-125 proves a real defect's cure against the
  test's own count of tide turns.
- **Failure messages.** Most pin asserts are bare `==` on long lists or tick integers; a failed
  digest says only that two hex strings differ, and the reason lives in comments pointing to
  docs/dev. Truth 7-144's `next(...)` (8661) and truth 7b-120's `[...][-1]` (7322) raise
  StopIteration/IndexError rather than saying what is missing.
- **Tests of a tool or a document, not the game:** the primer chapter 9 test (2777-2802,
  docs/primer/09-the-glass-and-the-sky.md), truth 53 (tools/climatology_check.py), the
  launcher, harbour and settings truths 7b-108 to 110, the API door truths 86, 7b-130, 7b-132.
- **`cutter_wardroom` (5145)** sails two hours forty minutes with three stations and is neither
  in DAY_FIXTURES nor are its two tests in SLOW_TESTS: they run in the fast tier. Whether it
  crosses the 5 s threshold I did not measure (forbidden to run). Low; a suspicion.
- **Private API in tests:** `driver._tick_owed` (5209), `Desk._own_act` (7206),
  `director_mod._peak_wind_kn` (5538), `combat.action._firer` (8268),
  `world.navigation._tide_allowance_m` (3197). A refactor breaks them without a behaviour
  change.
- **The file's header docstring (1-72)** covers truths 1 to 51 only; truths 52 to 7-144 are
  introduced by section comments.

## Not looked at

Lines 8700 to 17,391 (the other reader's). The code a test calls, beyond the lines named at the
head. docs/dev, docs/design, docs/playtests, docs/gates and the sealed notes, which the
comments cite for every re-pin, were not opened, so no "by bisection" claim was checked.
Nothing was run: the tier counts come from conftest's lists read against the file, not from a
collection.

## Faults to plant

1. **tests/test_known_truths.py::test_truth_52_a_low_passing_north_backs_veers_holds_squalls_and_rises_in_that_order.**
   Fault: in freesail/core/world.py delete the `else:` branch at lines 1935-1941 (the squall
   is never said to pass). The test's line 2303 claims "each squall ends in the log".
   Prediction: passes although the game is broken.
2. **tests/test_known_truths.py::test_truth_50_at_three_hundred_times_the_log_shows_hourly_rollups_and_every_notable_line.**
   Fault: in freesail/core/events.py line 209 change `e.severity is not Severity.ROUTINE` to
   `e.severity is Severity.URGENT` (notable lines rolled up at 300x). The name says every
   notable line is shown. Prediction: passes although the game is broken.
3. **tests/test_known_truths.py::test_truth_7_135_the_frigates_broadside_every_minute_and_three_quarters_and_slower_short.**
   Fault: in freesail/combat/guns.py line 98 change `("run out", 18.0)` to `("run out", 30.0)`
   (85 s nominal to 97: by the docstring's scaling about 119 s full, 181 s short). The name says
   a minute and three quarters. Prediction: passes (bands 90-125 and 140-210) although the
   broadside is two minutes.
4. **tests/test_known_truths.py::test_truth_7b_105_the_smacks_seine_fills_her_well_the_catch_sells_at_falmouth_and_spoils_kept.**
   Fault: in freesail/world/fishing.py line 617 change `"salted" if salted else "fresh"` to
   `"fresh" if salted else "salted"` (fresh fish sold at the salted price). The name says sold
   at the market's price. Prediction: passes (it computes the expectation with the same
   `price_of`).
5. **tests/test_known_truths.py::test_truth_7_136_a_tack_with_the_guns_served_is_slower_by_exactly_the_hands_it_takes.**
   Fault: in freesail/crew/quarters.py, `Quarters.lend` (line 343), return the lent sailors as
   freed but leave each at his gun crew (do not take him off the gun), so the tack is manned
   and the guns stay fully crewed. The name says the guns lose what the tack takes. Prediction:
   passes (it asserts only that hands were "robbed" in the log and that the tack is no slower
   than 1.15 of cleared).
6. **tests/test_known_truths.py::test_truth_7_138_the_pace_with_two_crewed_cutters_in_action_holds_the_crewed_floor.**
   Fault: in freesail/world/crews.py line 99 the floor is 60.0; plant instead a slowdown in
   the crewed ship's step (for example `time.sleep(0.004)` once per crewed world tick, about a
   five-fold slowdown from 538 ticks a second). Prediction: passes.

Faults I believe no test in this half would catch, though a player would:

1. **The whole game at about two thirds of its speed.** In freesail/core/world.py add
   `time.sleep(0.0006)` at the head of `World.tick`. The five floors are 500 ticks a second
   against 843 to 1000 measured; run alone they pass. A player at high compression sees the
   ship sail a third slower.
2. **A wear that loses two miles to leeward.** In freesail/evolutions/scripts.py `WearScript`
   (line 1860), hold the helm up for 300 s more once the wind is aft before the new course is
   ordered. Truth 11's passing test asserts only 360 to 720 s and the tack (and might catch the
   time if the delay pushes it over 720; then use 120 s); its strict xfail on the loss passes
   whatever the loss is outside a quarter to half a mile. A player sees the wear throw away
   ground.
3. **The guns firing at full rate while the tack takes their crews** (fault 5 above, from the
   player's side): no test in the half asserts the guns' rate during a manned tack.
