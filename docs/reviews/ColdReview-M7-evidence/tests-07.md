# Tests, reader 07: test_knowledge to test_nations

Reader's evidence for the test-suite audit (TESTREADERS.md). Sixteen files under `tests/`, each
read whole from first line to last, with `tests/conftest.py` read first. Code under test was
opened where a judgement needed it (named in each finding). Nothing was run but `wc`, an AST
count of tests and parameters (a script in the scratchpad), a check that every `SLOW_TESTS`
entry for these files still names a function (all do), and `which py`. The suite was not run.
Counts of cases are by AST over the literal parameter lists, checked by hand where a list is
built.

## The files at a glance

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_knowledge.py | 2104 | 44 (44) | none declared; ~20 tests each sail 1 to 2 hours of the frigate with fakes seated; 18 in `SLOW_TESTS`; one `pace` | proves much that is hard; several conditional or mis-described assertions; one test of a feature switched off; every slow test run twice (truths re-call them) |
| test_lateen.py | 722 | 23 (40) | five tests each settle the mizen fixture 1200 ticks | sound; one family asserts the evolution id and nothing after |
| test_lee_ports.py | 1938 | 60 (179) | `heeled` (monkeypatches `action._firer`'s heel); `_at_quarters` builds a world up to 1500 ticks per test | sound and hard; pins a typed copy of the tuning notes' tables; truth 7-190 "drafts" never moved; one dead test |
| test_letters.py | 510 | 14 (18) | none | sound; two digest pins on a kept save |
| test_local_runner.py | 1407 | 30 (30) | `TestClient` game, runner in a thread, real-time waits | sound in substance; pins constants; timing-dependent threads |
| test_log_lines.py | 635 | 21 (21) | `synthetic` (swaps a registry row); monkeypatched sail forces | sound; one test can only fail one way |
| test_longitude.py | 712 | 14 (14) | worlds of up to three days sailed (forgotten chronometer) | contains `assert x or True`; one test asserts only that nothing raised; a stale docstring |
| test_lookout.py | 458 | 13 (13) | point ship teleported a look at a time | sound; two vacuous trailing asserts; overlaps test_longitude |
| test_lug.py | 131 | 5 (5) | module `by_the_wind` (settled lugger), used by one test only | contains an assertion that cannot fail; three tests re-settle the same lugger |
| test_lying_to.py | 950 | 26 (40) | `world_for` sails 1200 ticks per world, ~22 worlds; four six-hour runs | strong physics tests; the same hove-to brig built a dozen times |
| test_magazine.py | 609 | 16 (54) | none | sound; reference table typed from the source, not from the code |
| test_map_view.py | 313 | 9 (9) | Node subprocess | sound; one test not guarded by `needs_node`; a doubled decorator |
| test_mcp_server.py | 1346 | 35 (35) | `TestClient`, threads, one uvicorn server and a child process over stdio | substantial; real-time races; pins `.mcp.json`'s `py`, which does not exist on this machine |
| test_mends_109.py | 427 | 15 (39) | none heavy; one test builds a directed world per example of the director's table | one parametrised test ignores its own parameter and can pass on any refusal |
| test_moon.py | 104 | 5 (5) | none | sound: checked against Meeus and JPL Horizons |
| test_nations.py | 371 | 8 (8) | module `table`, `chart` (cheap loads) | pins the whole port index (140 rows) by hand; one test name stale |

Totals for the sixteen files: 338 test functions, 554 cases.

---

## tests/conftest.py (read for the tiers)

- The slow tier is by fixture name (`DAY_FIXTURES`, by file) and by node id (`SLOW_TESTS`, a
  hand list of some 440 ids). All ids for my sixteen files still name real functions (checked by
  AST). The docstring (lines 25 to 27) admits a renamed test silently leaves the slow list:
  nothing checks that an id in `SLOW_TESTS` exists, so a rename moves a slow test into the fast
  tier unannounced. Weight medium, sure.
- `test_lug.py`'s module fixture `by_the_wind` and `test_nations.py`'s are not in
  `DAY_FIXTURES`; correct, they are cheap (lug's is a settle of 600-odd ticks).
- Line 715: `items[:] = [i for i in items if i not in set(others)]` rebuilds the set for every
  item (quadratic in the run's size). Low, sure.

---

## test_knowledge.py (2104 lines)

**Count and kind.** 44 tests, none parametrised. No fixtures declared; the cost is in helpers:
`world_at` (frigate, 120 ticks of plain sail) and `seated` (a fake harness). About twenty tests
then sail 1,300 to 7,200 ticks with one to three fakes seated; 18 are named in `SLOW_TESTS`; one
is a `pace` measurement (line 473). The file proves the place-knowledge rule: what a person can
read and hear by where he stands (cabin, gunroom, hold, aloft, ashore, in a boat, aboard
another hull), reports and calls from the officer, the command devolving, the console's and the
browser's play log by the player's place, papers read where they are kept.

**(a) Tests of what is no longer there or no longer matters.**

- `test_the_drills_walk_teaches_the_places_before_the_game` (line 1637) tests a feature switched
  off on the trunk: it sets `consent.DRILL_WALK = True` by monkeypatch (line 1652). In the code
  `DRILL_WALK = False` (freesail/agents/consent.py:244) and the docstring says "off on the trunk
  by the lead's ruling, until package 55 re-briefs". The walk ships to nobody; truth 7-381 in
  test_known_truths.py (around line 13605) calls this test and so is a truth of a dormant path.
  Weight medium (costs a test and a truth that prove nothing a player meets), sure.
- `test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks`, line 248 to 249: the comment
  says "on deck again, every row comes back as the delta and the line is gone", and the assertion
  is `assert "readings_elsewhere" not in samples(h)[0]`. `samples(h)[0]` is the first sample of
  the conversation, taken before the fake's `go below`; the test never brings him on deck again.
  The comment promises a return to deck that the body does not test. Weight medium, sure.
- `test_the_boat_away_with_the_player_reads_the_ship_by_sight_and_hail_alone`, lines 1823 to
  1825: comment "home again, the deck is the ship's and the lines hers", then
  `w.submit("come alongside")` and `assert K.players_senses(w).spot[1] == boat.id`: it asserts
  he is still in the boat, the opposite of the comment, and does not run the world to bring him
  home. Weight low, sure.
- `test_the_filters_cost_measured_with_three_stations_seated` (line 473): docstring "asserted
  within a band: the rule costs under a fifth of the pace"; the assertion (line 499) is
  `ruled >= 0.7 * free`, under three tenths. Docstring and band differ. Weight low, sure.

**(b) Tests built not to fail.**

- Line 236: `if sail_lines:` guards the whole check that sail work below is heard only as a
  sound ("Sail handled overhead."). If no `sail.*` line reaches the cabin sample, nothing is
  asserted. The direct check of `K.as_heard` at line 158 covers the function; this guard leaves
  the end-to-end path unproved. Weight medium, sure.
- Line 1821: `if bearing_cables(w, frigate, boat) <= 4: assert heard`. The boat has pulled for
  40 minutes (`w.run(40 * 60)` at line 1807 after `give way`) at about three and a half knots,
  so it is likely two miles off and the hearing assertion never runs. The docstring promises "a
  word said on her deck within hearing is written in the boat's log as heard". Weight medium,
  likely (distance not measured; I did not run it).
- Line 222: `assert "heading" in below[0]["readings"] or "heading" in results(h, "readings")[0]`
  and line 1525 `assert "speed" in samples(h)[-1]["readings"] or "readings_elsewhere" not in
  samples(h)[-1]`: either leg passes; the second leg of 1525 holds on any on-deck sample even if
  the rows are wrong. Low, sure.
- Line 586 to 588: `all(... ) or len(noted) == 1`: when the director has had one sample with
  notes, the check of "I think not." is skipped. Low, sure.
- Line 409 `assert h.agent.state == h2.agent.state` compares two harnesses' states after
  different scripts; it says nothing the test's name promises. Line 470 `assert C is not None`
  asserts an import. Low, sure.
- Line 904 and 1060: refusals accepted in either of two wordings (`"may not" ... or "has no
  authority"`; `"may not wear ship" ... or "has not the deck"`). Line 1476 to 1480 accepts
  "are kept" or "is kept". Tolerant, not empty. Low.
- Line 499: the pace band, `ruled >= 0.7 * free`, is acknowledged wide for noise; as a `pace`
  test it runs only alone. Informative, not a guard. Low.

**(c) Tests that might be one.**

- The two-hour cabin passage (`the_captain_in_the_cabin()` then `w.run(7200)` or more) is sailed
  separately by `test_a_captain_in_the_cabin...` (3,700 s), `test_the_rules_officer_reports...`
  (7,200 s plus two more 7,200 s worlds, lines 792 and 796),
  `test_the_captain_is_called_for_a_danger...` (7,200 s), `test_the_console_shows_the_captain...`
  (7,200 s, through the console) and `test_the_browsers_log_and_snapshot...` (7,200 s, through
  the driver). Five sailings of one scenario at seed 7 for assertions on the same log; a module
  fixture could carry the first three. Weight medium (fast-tier and slow-tier time), sure.
- Every slow test here is run twice in a `--slow` run: test_known_truths.py imports and calls
  them (lines 13480 to 13757, 13972 to 13996, 15045 to 15247: about 25 calls), and both node ids
  sit in `SLOW_TESTS` (conftest lines 122 to 160). The pace test too (truth 7-386, line 13666).
  Weight medium, sure.
- `test_a_tripwire_judged_below_wakes_as_the_officers_call` (line 384) and
  `test_the_tripwires_call_is_a_line_in_the_log` (line 945) sail the same script (go below,
  stand by for speed under 20 knots) for 130 s each and check two faces of one event. Low.

**Anything else.**

- `test_every_kind_the_code_writes_is_placed_or_falls_to_the_deck_by_design` (line 101) is a
  good guard: it scans the source for dotted literals and fails on a new kind with no reach. Its
  regex (line 88) misses kinds built in f-strings or holding a digit; a kind so written escapes.
  Low, likely.
- `test_a_passage_with_a_captain_below_reported_to_called_and_writing_replays_by_both_roads`
  (line 1835) replays two hulls by both roads at two save points: a hard and useful test.

---

## test_lateen.py (722 lines)

**Count and kind.** 23 tests, 4 parametrised into 21 cases (5, 4, 2, 10): 40 cases. No
fixtures; `_world` (line 586) settles the mizen-yard fixture for 1200 ticks and is called by
four tests, and the getting-under-way test sails 4,500 ticks more. Proves the lateen mizen
course cut at the mast: it uses the gaff's curve and trim, its yard is no braced yard, its own
evolutions, its handling in stays, wearing, hove to and after the cast.

**(a)** None found. The class lookups the module docstring names (`curve_class`,
`YARD_LIKE_CLASSES`, `after_gaff_sails_all`) are all used in the code the tests call.

**(b)**

- `test_the_mizens_orders_start_its_own_evolutions` (line 425, 10 cases) asserts the evolution id
  started and then calls `_run(runner, ship)` (line 439) with nothing asserted after: the sail's
  state at the end (set, in the gear, furled, reefed) is not checked. `_run` asserts only that the
  runner finished. A take-in that left the sail set would pass. Weight medium, sure.
- `test_the_courses_sheet_keeps_the_gaffs_floor_by_every_route` (line 279): the docstring itself
  says each route clamps to the floor "so it cannot show which class's trim the route itself
  looks up". Honest, and the next test (line 330) supplies the discriminating case. Noted, not a
  fault.
- `test_hanging_in_stays...` (line 640) calls the private `tack._hang()` by hand to force the
  hang; it proves the words, not that she hangs. Acknowledged in its docstring. Low.
- Pins with reasons: `_spar_weight == 2.0` (line 156), `ticks == 2 * (60 + 120 + 90)` (line 168),
  `ticks == 90` (line 373). Three, each explained.

**(c)** The four manoeuvre tests (lines 624 to 698) each rebuild and settle the same world; one
module-scoped settled state copied per test would save three settles. Low.

---

## test_lee_ports.py (1938 lines)

**Count and kind.** 60 tests, 14 parametrised: 6, 2, 63 (every triple), 13, 2, 2, 7, 2, 5, 4,
7, 8, 9 and 3 cases, so 133 cases plus 46 plain: 179. One function fixture, `heeled`
(line 951), which monkeypatches `action._firer` to put the test's heel in through the World's own
tick. `_at_quarters` (line 562) runs a world up to 1,500 ticks to load both broadsides, called by
some 15 tests and cases. Proves the lee-port rule: shut a foot from the sill, open six inches
clear after a minute's hold, guns run in and loading on, the log once per deck and side, the roll,
old saves.

**(a)**

- `test_the_kept_saves_load_by_the_checkpoint_road_and_run_on` (line 1879): docstring speaks of
  "the kept saves" and "None of the three has a gun"; the body loads one save and asserts only
  that the clock advanced 120 ticks. Nothing of the ports is touched; loading kept saves is
  test_checkpoint.py's work. Dead in this file. Weight low, sure.
- Truth 7-190 (lines 1631 to 1809) is four tests headed "A draft, for Phase 5 to move into
  tests/test_known_truths.py". grep finds no `7_190` in test_known_truths.py; the drafts stay
  here. The truth list therefore does not hold the truth it numbers. Weight low, sure.

**(b)**

- `TRIPLES` and `LOWEST_WITH_A_GUN` (lines 141 to 225) are typed from docs/dev/TuningNotes.md and
  compared with the ship files (line 235, 6 cases; line 307, 13 cases): a pin of data against a
  document (about 63 triples and 13 heels), with the stated reason that "the files, the notes and
  the rule are held to one another". The rule's arithmetic is the test's own `shut_heel`
  (line 67) using the code's `S.PORT_SHUT_M`; the constant itself is pinned at line 291
  (`SHUT_M == 0.3048`, `REOPEN_M == 0.15`). Sound as a cross-check; any regeneration of a hull
  must re-type the table. Low.
- `LOWEST_LEE_PORT` (line 1640) pins nine shut heels and nine counts "measured". Nine pins with
  sources named. Low.
- The `heeled` fixture and `firer_at` step round the physics' heel by design (module docstring);
  two tests (lines 1269 and 1502) heel and roll her by her own sail and sea, so the road is also
  proved whole. Not a fault.
- Line 924 `test_a_word_for_a_broadside_given_by_the_order_is_told_at_the_next_tick`: the
  docstring records that "the order's own reply still says the word stands
  (`orders/gunnery.py`, outside this rule; named to the lead)". A known wrong answer to the player
  is described and no test pins it, nor is it `xfail`ed. Weight low (the next tick corrects it),
  sure that the test leaves it untested.

**(c)**

- `test_a_port_does_not_flicker_in_a_gust` (line 1129) and `test_a_port_is_held_a_minute_through_
  the_gusts` (line 1176) are the same hour of sinusoidal heel on the cutter's lowest gun with
  amplitude 0.55 and 0.8 and the same assertions; one with two amplitudes would do. Low.
- `test_the_one_compare_short_of_the_least_dip_changes_no_port` (line 1560, 7 cases) and
  `test_the_one_compare_takes_the_roll` (line 1616, 8 cases) are the same sweep with and without a
  roll; one table. Low.

**Anything else.** `test_each_triple_shuts_and_reopens_at_the_rules_arithmetic` (63 cases) and
`test_a_lee_broadside_past_the_shut_heel_is_run_in_and_silent` (7 cases) are good tests: they
would catch a builder's error in the sill, the half-breadth, the hold or the run-in.

---

## test_letters.py (510 lines)

**Count and kind.** 14 tests, one parametrised (5): 18 cases. No fixtures. Proves letters as
things: written, sealed and broken, read by the reader alone, destroyed, made by the director,
come aboard and handed, sent ashore, saved and replayed.

**(a)** None found.

**(b)**

- `OLD_LETTER_SAVE_DIGEST` and `OLD_LETTER_RUN_ON_DIGEST` (lines 473 to 474): two digests of a
  kept save, the second "the trunk's own world, run on 600 seconds". A reason is given (the old
  build's result); but any change to the wording of any line in those 600 s breaks it, and the
  failure says only "digest differs". Two pins. Weight low, sure.
- Line 437 to 455: the loop runs up to 240 minutes until two `message.door` lines, with no
  assertion that it got there; the later assertions on `held[...]` fail with a `KeyError`, not a
  word. Low.

**(c)** `test_an_old_message_in_the_messengers_hand_is_made_a_thing_at_the_load` (line 386,
synthetic old message) and `test_a_save_from_before_step_2...` (line 477, a real kept save)
prove the same conversion; the second is the stronger and the first could go. Low.

---

## test_local_runner.py (1407 lines)

**Count and kind.** 30 tests, none parametrised. `pytest.importorskip("httpx")` and
`("fastapi")` at module level (lines 25 to 26): the whole file is skipped if either is missing,
and `fastapi` is in the `server` extra, not `dev` (pyproject.toml lines 19 to 20). CI installs
`.[dev,server]` (ci.yml line 66), so CI runs it; a builder with `.[dev]` skips 30 tests with one
line of output. The fake model server is `httpx.MockTransport`; the game a `TestClient`; the
runner in a thread. Proves the local runner: identity from the server, request shape, tool round
trip, consent through the game, budget by the server's count, retries, the handover reserve.

**(a)** None found.

**(b)**

- Constants pinned with no other check: `L.REPLY_MAX_TOKENS == 4096 and L.REQUEST_TIMEOUT_S ==
  600` and `FAILURES_TO_STAND_DOWN == 3` (lines 647 to 648), `SITUATION_ALLOWANCE_TOKENS == 2500`
  (line 917), `HANDOVER_RESERVE_SHARE == 0.3`, `HANDOVER_RESERVE_TOKENS == 14000` (lines 1249 to
  1250), `TURN_ENDS_WORDS` text (line 848). Six tripwires on values read from the code. Low.
- `test_the_budget_counts_by_the_servers_figure_from_the_first_reply_on` line 1135:
  `1.1 < m.ratio < 1.2` where the fake server counts at 3.5 characters a token (line 972) and the
  runner at 4 (`tools.CHARS_PER_TOKEN`, freesail/agents/tools.py:137): the band is the test's own
  arithmetic (4/3.5 = 1.14). It proves the ratio is taken, not that it is right. Low, sure.
- Line 932: `if need_w <= need - 1:` before an assertion; given line 926 asserts `need > need_w`
  the guard is always true, so harmless, but it reads as conditional. Low.

**(c)** `Game`, `run_runner` and consent-record set-up recur in 12 tests; that is a helper, not
duplication. None.

**Anything else.** The threaded tests wait on real time (`wait_for` 10 s, `finished` 15 s,
`time.sleep(0.02)` polls). Under the four loaded cores the conftest describes, these can time out
and fail with "the runner did not get there in time", which tells a builder nothing of what
broke. Weight low to medium, a suspicion (not run).

---

## test_log_lines.py (635 lines)

**Count and kind.** 21 tests, none parametrised. Function fixture `synthetic` (line 469) swaps a
reading in the shared registry and restores it. Two tests monkeypatch
`integrate.compute_sail_forces` with fixed forces (lines 250, 277). Proves the log said once:
wind shifts with a floor and hysteresis, aback lines by state, a cast that finds no bottom, a
standing order held once a watch, conditions checked on entry.

**(a)** None found.

**(b)**

- `test_at_a_sounding_waits_for_the_bottom` (line 421) is negative only: three casts that find no
  bottom, and no firing of `at a sounding`. If `at a sounding` never fired at all, it would pass.
  The positive half (that it fires when bottom is found) is not sailed anywhere in the file; line
  418 checks only `R.event_matches` on the line. Weight medium, sure.
- `test_a_standing_order_with_nothing_to_do...` line 463: `fired <= firings` is an upper bound;
  nought firings passes. The held-line counts above it carry the test. Low.
- `test_the_event_a_wind_shift_keeps_the_same_floor` line 213: `len(shift_firings(steady)) >= 3`
  with no upper bound. Low.
- Constants pinned: `WIND_SHIFT_FLOOR_KN == 4.0` (line 64), `WIND_SWING_S == 3600 and
  WIND_STEADY_S == 1800` (line 142), `WIND_LIGHT_HOLD_S`, `WIND_SETTLE_S`, `WIND_SETTLE_BAND_KN`
  (lines 603 to 604). Five. Low.
- `test_the_shipped_books_enter_whole` (line 564) asserts only that no line is refused for "is not
  a place on the chart"; a book line refused for any other reason passes. Its name promises the
  books "enter whole". Weight low to medium, sure.

**(c)** The calm-boxes-the-compass and wind-falls-light tests (lines 69, 84, 197, 590) script
overlapping light-air winds; distinct assertions, acceptable. None.

---

## test_longitude.py (712 lines)

**Count and kind.** 14 tests, none parametrised. One sails nearly three days
(line 138, `3 * 24 * 3600 - 3600`); four are in `SLOW_TESTS`. Proves the chronometer, the time
sight, the lunar (drawn from truth plus seeded error), the amplitude and azimuth, chart queries
by account, and three lookout faults.

**(a)**

- `test_the_lookouts_estimate_is_drawn_once_and_held_while_she_makes_no_way` (line 575):
  docstring "held until she has moved a mile". The rule now is a tenth of the distance
  (`ESTIMATE_REFRESH_FRACTION = 0.1`, freesail/world/lookout.py:163 and 592), as
  test_lookout.py line 206 says. The test still passes because half a mile at ten miles is under a
  tenth and two miles over it, but the docstring describes a rule that is gone. Weight low, sure.

**(b)**

- Line 587: `assert look.reading(0.0)["items"][0]["estimate"] == w.log[-1].data["estimate"] or
  True`. It cannot fail. It was meant to tie the reading's estimate to the log's. Weight medium,
  sure.
- `test_the_dialect_reads_the_new_rows_for_nothing_and_the_events_are_named` (line 519): line 533
  `assert c.holds(w.readings, {}) in (True, False)` and line 547 `parse_standing(...)` with no
  assertion: both prove only that nothing raised. A condition that reads the wrong row, or
  `west of` read as `east of`, passes. Weight medium, sure.
- Line 642: `any(n.startswith("the Manacles") or n[:1].isupper() for n in named)` is implied by
  line 640, which already asserts every name starts upper case or with "the "/"a "; so it adds
  nothing. Low, sure.
- Line 494: `nav.dangers(2.0) is None or all(...)`; line 500 `" within " in e.text or "crosses"
  in e.text`; line 266 and 325 accept either of two words. Tolerant, not empty. Low.
- Lines 589 to 590, 601 to 602, 607 to 612 teleport the ship through private `w._position` and
  `w._geo_last`. By design; noted.

**(c)** The estimate-held behaviour is tested here (line 575) and in test_lookout.py
(`test_an_hour_of_calm_leaves_the_figure_as_it_was`, line 236, and
`test_the_lookout_judges_a_distance_afresh...`, line 206); the lookout file's are the sharper.
The lookout's section of this file (lines 570 to 711) belongs in test_lookout.py. Low.

**Anything else.** `test_the_lunars_spread_by_skill_sea_and_the_moons_rate` (line 355) measures
the draw over 400 seeds against the study's quarter degree and degree: a good statistical test.

---

## test_lookout.py (458 lines)

**Count and kind.** 13 tests, none parametrised. A point ship moved a minute at a time by
`look_from` (line 182), which advances the clock and teleports her. Proves the lookout's words,
height of eye, landfall, the land lost, lights at night, the distance judged afresh, the shore as
a sighting, land ahead notable and urgent.

**(a)** None found.

**(b)**

- `test_a_sail_whose_distance_halves...` line 281 `assert lines is not None` and line 280
  `... and s is not None`: `lines` is always a list from `look_from`; these assert nothing. Low,
  sure.
- Line 102 pins seed 7's "four leagues" for ten miles, with its reason (the eye's draw). One pin.
  Low.

**(c)** See test_longitude.py above.

**Anything else.** `test_land_ahead_is_notable_under_ten_minutes_and_urgent_under_four_each_once`
(line 345) and `test_land_ahead_comes_again_after_the_quiet...` (line 391) are good: they would
catch wrong thresholds, a repeated line, and silence at anchor or in fog.

---

## test_lug.py (131 lines)

**Count and kind.** 5 tests. Module fixture `by_the_wind` (line 28), a settled lugger, used by
one test (line 50). The other four call `make` and `settle` afresh (lines 41, 73, 99, 120), three
of them with the same orders and defaults. Proves the dipping lug: hoisted to leeward, against
the mast two thirds, dipped in a tack, `dip` by itself, lowered hove to.

**(a)** None found.

**(b)**

- `test_she_heaves_to_with_her_lugs_lowered` line 130: `assert math.degrees(abs(world.ship.dyn.u))
  >= 0.0`. An absolute value is never negative, and `degrees` of a speed is meaningless. It cannot
  fail, and nothing in the test checks that she has lost her way. Weight medium, sure.
- `test_the_lugs_are_hoisted_to_leeward_and_their_yards_are_not_braced` lines 46 to 47: "no brace
  order reaches a lug's yard" is proved by the absence of the words "lug yard" in any log line; a
  brace that logged in other words would pass. Line 40 (`not sp.is_yard`) carries the real check.
  Low.
- `test_a_dipping_lug_against_the_mast_draws_two_thirds` mutates the module fixture; the mizen's
  restore (line 69) is not in a `finally`. Low.

**(c)** The three re-settles want the module fixture they already have (copy it per test), or one
test. Low.

---

## test_lying_to.py (950 lines)

**Count and kind.** 26 tests, 5 parametrised (4, 6, 4, 2, 3 cases): 40 cases. No fixtures;
`world_for` (line 49) sails 1,200 ticks with a trim every 120, and is called about 22 times;
`test_held_six_hours...` sails 21,600 ticks for each of four ships. Proves heaving to that holds
its tack across ship types and winds, being forced round, `fill away` and `fill away and steer`,
the record cleared by anchor, tack, wear and ground, `trim sails` declined, the lifting warning.

**(a)** None found.

**(b)**

- `test_the_record_is_cleared_by_a_tack_and_by_a_wear` (line 516) begins the tack by hand,
  `scripts.TackScript(world.ship, {}, {}).begin({})` (lines 537 to 538), since the order is
  refused. Acknowledged; it proves the script's `begin`, not a tack the player can give. Low.
- `test_a_sail_still_being_set_or_trimmed_is_left_out_of_the_alarm` (line 851) drives the private
  `integrate._log_notes` with `last_thrust_n` and `backed` set by hand. A unit test of the alarm's
  filter; fine as such. Low.
- `test_no_lifting_line_under_full_and_by_in_a_steady_breeze` (line 942) is negative only; its
  positive twin is line 894. Acceptable.

**(c)** The hove-to brig, `world_for(BRIG, 292.0, 10.0)` then `heave to` and `run(600)`, is built
in tests at lines 286, 314, 381 (2 cases), 401, 429 (twice), 482 (twice, and a third whole
1,200-tick world at line 508 only to call `orders.handle` for a parse refusal), 662 and 686:
eleven sailings of one state. A module fixture copied by checkpoint, or one world per group of
assertions, would cut much of the file's time. Weight medium, sure.

**Anything else.** `test_the_brig_brought_to_from_each_of_the_games_states_holds_her_tack`
(line 120) and `test_held_six_hours_through_shifts...` (line 195) are strong: per-second bounds
on her head over ten minutes and six hours would catch a real regression in the heave-to helm.

---

## test_magazine.py (609 lines)

**Count and kind.** 16 tests, 5 parametrised (8, 20, 3, 7, 5): 54 cases. No fixtures. Proves the
magazine by kind: Table No. 29's charges, filling times, take and has by kind, the gunner's
filling, receipt and wanting, old magazines and fits converted, the schema's refusals, the
committed files' figures, the words.

**(a)** None found.

**(b)**

- `TABLE` (line 527, 7 rows) pins each committed file's cartridges, powder pounds, barrels and
  exercise charges, "the build design's table". Seven pins of generated data with a document as
  reason. Low.
- `TABLE_NO_29` (line 89) is typed from the Regulations as the design reads them and checked
  against `CHARGE_TABLE_LB`; a reference independent of the code. Good.

**(c)** `test_the_charges_and_the_filling_times_are_the_build_designs_table` (line 75, 8 cases)
overlaps `test_table_no_29_is_the_designs_reading_figure_by_figure` (line 128, 20 cases) for the
charge; the first adds the filling time. Low.

**Anything else.** `test_the_table_confirms_a_third_and_a_twelfth_rounded_down_to_the_ounce`
(line 145) derives every figure from the rule with `Fraction`: a test that proves something.

---

## test_map_view.py (313 lines)

**Count and kind.** 9 tests; eight marked `needs_node` (skip if `node` is absent). Each runs a
Node subprocess on `client/map.js`, `client/units.js` or `client/library.js`. Proves the chart
view's arithmetic, bearing-line fading, the chart tools' words, the units module, and the library
pane's Markdown renderer. A test of the client, not the game's model.

**(a)** None.

**(b)** None found; the expected values are computed by hand (e.g. line 236, cos 50°).

**Anything else.**

- `test_the_library_pane_renders_the_models_markdown` (line 283) has no `@needs_node`. Where Node
  is absent `run_js` calls `subprocess.run([None, ...])` and errors, where the module docstring
  (lines 8 to 9) says "where Node is not installed these tests are skipped". Weight low, sure.
- Lines 166 to 167: `@needs_node` written twice on one test. Harmless; a sign of a careless edit.
  Low, sure.
- No workflow installs Node; GitHub's hosted runners carry it, so CI likely runs these. A
  suspicion.

---

## test_mcp_server.py (1346 lines)

**Count and kind.** 35 tests, none parametrised. Module-level `importorskip` of anyio, mcp and
fastapi (lines 24 to 26). The game on a `TestClient`; the bridge through the MCP SDK's in-process
client; threads that turn the clock; one test starts uvicorn on a free port and the bridge as a
child process over stdio (line 997). Six in `SLOW_TESTS`. Proves the MCP door: tool listing,
consent first, the brief, the held call and its progress, cut-off calls never losing a turn,
stand-by digests, reconnects, keys, pictures.

**(a)** None found.

**(b)**

- `test_the_chart_and_the_ships_view_come_as_images_drawn_by_the_open_page` (line 1285): the
  comment at line 1342 says "the picture is held for the doors that fetch it, and asked for with
  the seating's key", but the test only fetches without a key and asserts 409 (line 1345). A
  keyed fetch that always returned 404 would pass. Line 1343, `pid = [ ... ] and asked[0]["id"]`,
  is an odd construct that yields a list if no image came. Weight medium, sure.
- Line 1277: `isinstance(second.call("readings", {}), str)`: `call` returns a string whatever
  happens. Vacuous; `second.phase == M.STATION` beside it does the work. Low, sure.
- the test at line 1122 of test_mcp_server.py (its name names a vendor's client; `..._mcp_json_points_..._at_the_bridge`) pins
  `.mcp.json`'s command as `"py"` (line 1129). `py` is the Windows launcher; `which py` on this
  machine finds nothing, so the configuration the test guards does not start on Linux or macOS.
  The test holds a value that is broken off Windows. Weight medium, sure.
- Constants pinned: `DEFAULT_WAIT_S == MCP_WAIT_S == 50`, `WAIT_CEILING_MAX_S == 14400`,
  `PROGRESS_EVERY_S == 15 and WAIT_SLICE_S == 2` (lines 317 to 322), `WAIT_FLOOR_S == 15.0`
  (line 1239). Four. Low.
- Line 662: `with pytest.raises(Exception)` (B017 suppressed) for the SDK's timeout; any error at
  all passes that step. Low.

**(c)** `test_a_game_with_an_mcp_watcher_replays...` (line 604), `test_a_continued_stand_by...`
(line 802) and `test_a_stand_by_asked_while_standing_by...` (line 854) each end with a replay to
the same digest; three replays of small sessions, cheap. None of weight.

**Anything else.** The file leans on real time: `ask_later` sleeps 0.8 s against a 0.3 s read
timeout (lines 661 to 663), `glass_later` 1.5 s (line 937), `anyio.sleep(0.6)` (line 908), 10 s
deadlines in polling threads. Under load these are races; a failure reads as an assertion on
text, not as "the thread was late". Weight medium, a suspicion (not run).

---

## test_mends_109.py (427 lines)

**Count and kind.** 15 tests, 5 parametrised (7, 2, 4, 9, 7): 39 cases. No fixtures; each case
loads the Channel-east scenario afresh; `test_every_form_of_the_directors_table_dry_runs...`
(line 374) builds a directed world and seats the director for every example of every form.
Proves package 109's mends: free orders that find nothing refused, things found by name, two
things named apart, the keeping as a reading, the short watch's boat, the director's dry run, the
view following the hull.

**(a)** None found.

**(b)**

- `test_words_of_the_dialect_go_to_the_dialect` (line 102, 2 cases): the parameter `kind`
  ("navigation") is never used in the body. The test asserts only `e.kind != "free.line"` and
  that "nothing of that name" is not in the text. A refusal of any other kind passes, as would the
  words routed to the wrong navigation order. The docstring says "is the noon sight"; nothing
  checks that. Weight medium, sure.
- Line 123: `answer in why.lower() or answer in why`: the second leg is redundant. Low.
- `test_a_dry_run_that_could_not_be_tried...` (line 289) monkeypatches `replay.checkpoint_bytes`
  to raise: steps round the copy to test the error words; by design. Not a fault.

**(c)** `test_a_free_order_that_finds_nothing...` (7 cases) and `test_his_keeping_and_what_lies_
here_is_a_reading` (7 cases) are already table-driven. None.

**Anything else.** `test_every_form_of_the_directors_table_dry_runs_as_it_is_performed`
(line 374) is a good sweeping test: it compares the dry run's verdict with the order's own for
every documented example.

---

## test_moon.py (104 lines)

**Count and kind.** 5 tests. No fixtures. Proves the moon's place, light, phase and the lunar
stars against Meeus's example 47.a and JPL Horizons for June 1805. Sound: external references
with tolerances stated. `LUNATION_DAYS` pinned (line 103) to the known constant. Nothing to
report.

---

## test_nations.py (371 lines)

**Count and kind.** 8 tests. Module fixtures `table` and `chart`, cheap loads. Proves the nations
table: wars of June 1805, stances, blockades, habits, signals roots, the news moving the market,
the naval blocks.

**(a)**

- `test_the_eight_nations_and_the_wars_of_june_1805` (line 27) lists sixteen nations (lines 28 to
  50). The name is stale since package 39f. Low, sure.

**(b)**

- `test_the_stance_of_a_port_toward_a_ship` (line 155) holds the whole port index typed by hand,
  140 entries (lines 165 to 309), each added package by package. The loop after it (line 310)
  checks the port files against the table, which is the useful check; the literal dict only pins
  the table to itself and grows with every port. Weight low (cost is edits, not false passes),
  sure.
- The nations list at lines 28 to 50 is another such pin (16 entries).
- Line 102 to 106: a relation's source passes if it contains "JUDGEMENT", "MEMORY", "1800",
  "1826" or "encyclopaedia"; loose. Low.
- Line 61 and 67: `wars_words()` checked by `startswith` then by `==` on the same string. Low.

**Anything else.** Line 98 opens the YAML without a `with` (file left open). Low.

---

## Across the files

- Truth wrappers: test_known_truths.py calls test functions of test_knowledge.py and
  test_letters.py by import (lines 13480 onward, 15280 onward). Each slow one runs twice in a
  `--slow` run and is listed twice in `SLOW_TESTS`. A truth that is only a call of another test
  is a second name for one test; marking the original with the truth's number would halve the
  time. Weight medium, sure.
- Module-level `importorskip` (test_local_runner.py, test_mcp_server.py) turns a missing extra
  into 65 silent skips. A builder who installs `.[dev]` as pyproject suggests loses both files.
  Putting `fastapi` in `dev`, or failing rather than skipping when `FREESAIL_REQUIRE_ALL` (or CI)
  is set, would close it. Weight medium, sure.
- Private reach: tests set `w._position`, `w._geo_last`, `battery._shut`, call `tack._hang()`,
  `integrate._log_notes`, `b._adapt`, `h._fold_handover`. Many are deliberate unit tests of one
  rule; they break on any refactor that renames internals. Low.

## What I did not do

- I ran no test, so every "would pass" below is a prediction, and the timing findings are
  suspicions.
- I did not read the code under test beyond the lines cited (consent.py:244, lookout.py:163 and
  592 and 615 to 669, harness.py:2037 to 2043, stations.py:610 to 649, remote.py:1271 to 1286,
  server.py:1121 to 1127, tools.py:137, local.py:173 and 227, vocabulary.yaml:591 to 604), nor the
  helper modules other tests import (`tests/test_crews.py`, `tests/test_ports.py`,
  `tests/test_director.py`, `tests/test_people.py`, `tests/test_between_hulls.py`,
  `tests/rig_fixtures.py`, `tests/messages_api.py`).
- I did not open anything under docs/dev, docs/design, docs/playtests, docs/gates or the sealed
  notes; the tuning notes the lee-ports tables are typed from were not checked against.

## Faults to plant

Claims under (b), each a fault a builder could make:

1. **test_longitude.py::test_the_lookouts_estimate_is_drawn_once_and_held_while_she_makes_no_way.**
   Fault: in freesail/world/lookout.py line 649 (`_line_data`), change
   `"estimate": estimate_words(s.judged_m)` to `"estimate": estimate_words(s.distance_m)` (the
   log's hail gives the true distance while the reading gives the eye's). The test's line 587 was
   meant to tie the two and ends `or True`. Prediction: this test passes although the log now
   leaks the truth. (test_lookout.py::test_a_landfall_is_notable... probably fails on its "four
   leagues" pin.)
2. **test_mends_109.py::test_words_of_the_dialect_go_to_the_dialect.** Fault: in
   data/vocabulary.yaml line 601, move `take a sight for the latitude, take a sight for latitude`
   out of `observe the sun`'s synonyms into `work up the reckoning`'s (line 592). The player's
   noon sight now works up the reckoning instead. Prediction: both cases pass although the words
   reach the wrong order.
3. **test_knowledge.py::test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks.** Fault:
   in freesail/agents/harness.py line 2040, make `_readings_elsewhere` remember its first non-None
   answer and return it ever after (e.g. `self._elsewhere = self._elsewhere or
   knowledge.elsewhere_words(...)`, as a static method made an instance one), so the "Not to be
   had in the cabin" line stays after he comes on deck. The test's "on deck again ... the line is
   gone" check reads the first sample, before he went below. Prediction: passes although broken;
   I believe no test in my files catches it (line 1525 of the master's test passes on its `speed`
   leg).
4. **test_knowledge.py::test_the_boat_away_with_the_player_reads_the_ship_by_sight_and_hail_alone.**
   Fault: in freesail/orders/stations.py lines 640 to 648, delete the loop that records a word in
   the other hearing hulls' logs. Prediction: this test passes (its hearing assertion is skipped by
   `if bearing_cables(...) <= 4` with the boat some two miles off);
   `test_a_say_is_heard_on_every_hull_within_hearing...` (line 703) should fail as it should.
5. **test_longitude.py::test_the_dialect_reads_the_new_rows_for_nothing_and_the_events_are_named.**
   Fault: in freesail/standing/grammar.py lines 758 to 759, swap the operators so that
   `("is east of", "west_of")` and `("is west of", "east_of")`. Prediction: passes (it asserts
   only `holds(...) in (True, False)`); a standing order "when the longitude by chronometer is
   west of 5 W" then fires on the wrong side.
6. **test_mcp_server.py::test_the_chart_and_the_ships_view_come_as_images_drawn_by_the_open_page.**
   Fault: in freesail/agents/remote.py line 1283, make `picture` ignore the painter (`pic =
   None`), so every keyed fetch of a picture is 404. Prediction: passes (it checks only the
   no-key 409); doors that fetch the picture lose it.

Faults I believe no test in my files would catch though a player would:

1. **The lugger keeps her way hove to.** In the lugger's heave-to (the code behind
   test_lug.py::test_she_heaves_to_with_her_lugs_lowered), leave the mizen lug drawing and the
   helm amidships so that she forereaches at three or four knots while the log says "hove to".
   test_lug.py checks the two lugs in the gear and then `degrees(abs(u)) >= 0`; test_lying_to.py
   sails no lugger. Prediction: no test in my files fails.
2. **`at a sounding` never fires.** In freesail/api/readings.py, make the `a sounding` event's
   match require a field no sounding line carries (keep `event_matches` true for the line so
   test_log_lines.py line 418 still passes, but break the standing book's dispatch of that event
   only). test_log_lines.py::test_at_a_sounding_waits_for_the_bottom is negative and passes; a
   player's "at a sounding then ..." never acts.
3. **The order "fire" with every lee port shut answers that the word stands.** Already so on the
   trunk by the docstring of test_lee_ports.py::test_a_word_for_a_broadside_given_by_the_order_is_
   told_at_the_next_tick (line 924): the reply says the word stands and the next tick drops it.
   No test pins the reply; a builder making it worse (the word left standing for ever in the reply
   and the state) would be caught only by that test's next-tick check.
