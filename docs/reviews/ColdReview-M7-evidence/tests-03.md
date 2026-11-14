# Tests, reader 03: sixteen files from test_aboard_another.py to test_brains.py

Read whole, first line to last: `tests/conftest.py` and the sixteen files below. Code under test
was opened only where a test's claim needed checking (cited). Nothing was run but grep and a
few seconds of `python3 -c`/`ast` to count tests; the suite was not run. Commit 504a2506.

Counts are by `ast` over the file (top-level `def test_*`), parametrised cases expanded by hand
where the parameter list is a name or a comprehension.

| file | lines | tests (cases) | fixtures of weight | verdict |
|---|---|---|---|---|
| test_aboard_another.py | 277 | 9 (9) | none module-scoped; each test promotes a brig beside the frigate; two replays | sound in the main; two either-outcome asserts |
| test_aboard_found.py | 242 | 10 (10) | none; `world_at` a world per test | sound; one count pin, one vacuous-able `all` |
| test_agent_api.py | 995 | 22 (22) | a FastAPI `TestClient` per test; a 30 s long-poll thread | sound; pins constants in place of the cap it names; reads client JS |
| test_agents.py | 3168 | 105 (110) | none module-scoped; 15 of its tests named slow in conftest | proves much; one strict xfail of a dead rule, one tautology, many pins of constants and doc sizes |
| test_anchor.py | 707 | 22 (28) | module `brought_up` (40 min sailed, then mutated by the next test for up to 12 h) | sound core; three asserts that cannot fail, one dead block |
| test_api_door.py | 770 | 18 (19) | a local Messages-API HTTP server per test; door threads | sound; one repository-hygiene test that is not of the game |
| test_bellerophon.py | 2198 | 53 (93) | module `her` (a load); ~12 sailed tests of 10-30 s each | pins much from the data file; drafts of truths duplicating its own tests; one test pins a known gap |
| test_between_hulls.py | 367 | 8 (8) | none; `_round_trip` sailed twice | dead in part (test 1 is test 2's prefix) |
| test_bilander.py | 2119 | 48 (63) | module `her`, `spec`, `doc`, `settee`, `module` (a generator subprocess); `_her_settle` (2,400 ticks) sailed 13 times | pins much; one test touches no code at all; two cases test a flag the game never sets |
| test_bill_marines_and_flag.py | 174 | 7 (30) | none | sound; module docstring now false |
| test_boat_director.py | 140 | 5 (5) | none | one branch-either-way test |
| test_boat_drawing.py | 73 | 3 (7) | Node subprocess (skipped where Node is absent) | sound |
| test_boat_hull.py | 346 | 10 (10) | none | sound |
| test_boat_names.py | 90 | 2 (2) | none; three hulls, two asleep | sound |
| test_bowsprit_yards.py | 678 | 17 (34) | none; `_world` 1,200 ticks per sailed test | sound |
| test_brains.py | 416 | 10 (10) | none; but its `world_at` and `put` are a library for at least four other files | one vacuous assert; otherwise sound |

## conftest.py (read for the tiers)

- The slow tier is by fixture name (`DAY_FIXTURES`) and by node id (`SLOW_TESTS`, ~460 ids).
  A renamed test silently drops into the fast tier (conftest.py:25-27 says so). I checked every
  `SLOW_TESTS` id for my five files that appear there (test_agent_api, test_agents,
  test_bellerophon, test_bilander, test_boat_names): all exist today. No check in the suite
  enforces it; a ten-line test asserting each id resolves would.
- `test_anchor.py`'s module fixture `brought_up` (forty minutes sailed) is in no tier list, so
  it and its 12-hour follower run in the fast tier. Not measured; a suspicion of a slow fast test.
- conftest.py:715 rebuilds `set(others)` once per item (`i not in set(others)`): quadratic in
  the suite's size under `FREESAIL_SHARD`. Low weight, sure.
- The tier and pace marks are applied by name suffix (`_is_pace`, :648-657): a pace test whose
  name ends otherwise is a fast test unless marked by hand (test_bellerophon.py:2140 is).

## test_aboard_another.py

1. **Count and kind.** 9 tests, none parametrised, no module fixture. Each builds the frigate
   with the brig X promoted (`tests.test_crews._frigate_and_the_brig_x_on_the_sea`), two replay a
   save. Proves the player following another hull: her prompt, her captain standing aside, the
   director's door reading the followed hull, the player's seat on another ship and its replay.
2. **(a)** Nothing removed. The docstring's truths 7-322/323/326 "calling here" not checked in
   test_known_truths (not my file).
3. **(b)**
   - :84 `assert "commands again" in w.world_order("captain: carry on").text or hull.captain.commands`:
     either disjunct passes; if `carry on` silently does nothing but the captain already commands,
     it passes. Weight low, likely.
   - :175 `assert e.kind in ("order.accepted", "order.rejected")`: any answer passes.
   - :234 `assert e.kind in ("order.accepted", "agent.refused")` for the player's officer seat on
     another hull: the test named "the player's seat on another ship is hers" never shows the
     seat can give an order there. A fault that refuses every order of a seat on a hull not the
     player's own passes this file (see the last section). Weight medium, sure.
   - :73 `frigate.position != before` after 120 s: true of any moving ship. Low.
4. **(c)** `aboard_x` and `_frigate_and_the_brig_x_on_the_sea` are built afresh in all nine tests;
   tests 1, 2, 4, 8 each sail the same opening. Acceptable for isolation.
5. :188 `test_hail_holds_the_players_own_hull_with_no_rules_captain_...` sets
   `players.captain = None` by hand and restores it in `finally`: sound and the right way round.

## test_aboard_found.py

1. 10 tests, none parametrised. Each a frigate world at seed 7 off the Lizard. Proves the
   director's `aboard:` table: parsing, effects on parts, stores, cargo, chronometer, glass, the
   `plausible_when` conditions, watering, replay.
2. **(a)** None found.
3. **(b)**
   - :50 `assert len(table) == 34`: a count pin of `data/director/aboard.yaml`; the comment records
     three past edits of it. Breaks on every row added; proves nothing a reader can check.
   - :132 `assert all(s.condition <= 60.0 for s in sail_room(w.ship).sails)`: passes on an empty
     sail room. The frigate has spare sails today, so it bites; no `assert sail_room(...).sails`
     guards it. Low, likely.
   - :175-214 monkeypatches `WO.aboard_table` with a three-row table: steps round the data, but
     that is the point (testing the condition logic); sound.
   - Condition values 45, 35, 40, 50 (:91-101) are the data's; pinned to the table's numbers,
     acceptable as the table is the specification.
4. **(c)** None.
5. :70 the table's typo keys refused in words: a good test of a data loader.

## test_agent_api.py

1. 22 tests, none parametrised, `importorskip("fastapi")` and `("httpx")` at the head (:21-22):
   the whole file vanishes silently without them (CI installs both via `.[dev,server]`,
   `.github/workflows/ci.yml:66`). Each test a `TestClient` over the server's app. Proves the
   model door's routes: consent, key per seating, long poll, folds, lockstep, replay, the
   director's seat.
2. **(a)**
   - :466-470 the comment says "an empty answer after the wait, and the wait is capped"; the
     assertion is `TURNS_WAIT_MAX_S == 120 and POLL_RECHECK_S == 0.25`, constants imported from
     the code under test (`freesail/agents/remote.py:143`). No call asks for more than 120 s, so
     the cap at remote.py:886 (`min(float(wait or 0.0), TURNS_WAIT_MAX_S)`) is never exercised.
     Weight medium, sure.
3. **(b)**
   - :448-465 the long-poll bound: `POLL_S, BOUND_S = 30, 20`. The comment argues the band
     correctly (a lock-holding poll would hold the tick ~30 s). Sound, but the test costs up to
     30 s of wall clock when it fails and is slow-listed.
   - :886 `before >= 3`: loose, but the next line pins `samples_at == before` exactly. Sound.
   - :586 calls the private `driver._tick_owed`.
4. **(c)** The replay-to-digest test (:619) overlaps test_agents.py:1333
   (`test_a_live_game_with_late_replies_replays_to_the_same_digest`): one through HTTP, one
   through the harness. Both have value; noted.
5. :610-611 reads `client/instruments.js` and asserts three substrings: a test of the client's
   source text, not of behaviour. Low.

## test_agents.py

1. 105 tests, one parametrised into 6 (110 cases). No module fixture; the point ship for most,
   the frigate where sails matter. 15 of its tests are in `SLOW_TESTS`. Proves the harness: the
   brief's head, the tools, opt-out, the watcher's lack of authority, welfare (nudge, pause, ten
   real minutes), stand-by, determinism, the shelf, the REPL door, readings deltas.
2. **(a) Of what is no longer there.**
   - :2411-2429 `@pytest.mark.xfail(strict=True, reason="decision 60 ... it no longer ends the
     empty count")` on `test_an_empty_reply_at_an_urgent_event_counts_and_words_end_the_count`:
     "The rule before decision 60, kept as it was for the record". A test of a superseded rule,
     kept alive by a strict xfail: it must fail forever. Nobody can expect it mended; its
     successor is :2432. It is a document, not a test. Delete it. Weight low (costs a run and
     confusion), sure.
   - :679 `assert not hasattr(harness_mod, "WELFARE_UNATTENDED_BOUND_S")`: asserts a removed
     constant stays removed. A fossil guard. Low, sure.
   - :282 `test_the_tools_are_the_nine_of_the_spec_and_shelve_with_a_description_each` asserts a
     tuple of **eighteen** tools (:287-306). Name and body disagree. Low, sure.
3. **(b) Built not to fail.**
   - :1428 `assert first["readings"] == data_turns(fake)[0]["readings"] and ...`: `first` *is*
     `data_turns(fake)[0]` (:1420). A tautology. Low (the next lines do the work), sure.
   - :1861, :1870, :1934 pin `tools.CHARS_PER_TOKEN == 4` and the primer chapter 3's size
     "about 11,280 tokens"; the docstring (:1849-1858) records eight past values (7,650 to
     11,370). :1895 pins "108 evolutions" with a comment chronicling ten earlier counts; :1899
     "12 aboard"; :1876 "in 6 parts"; :1878 "in 5 parts"; :448 `len(lines) == 7` of
     `data/standing_orders/starter.orders`. Seven pins of the size of documents and data; each
     moves with every edit and proves nothing a reader can check. Weight medium (churn; teaches
     builders to re-pin without thinking), sure.
   - Constants pinned to themselves: :764-765 (`WELFARE_UNATTENDED_REAL_S == 600`,
     `WELFARE_REPEAT_N == 3`), :1386, :1445 (`SAMPLE_ROUTINE_LINES == 40`), :1485-1486, :2092
     (`SHELF_LIFE_TURNS == 3`), :2310 (`BUDGET_FREE_TOOLS == ...`), :2493
     (`ANSWER_UNASKED == result`, after the literal was already asserted). Eight such pins.
     They guard against an edit of the constant, not of behaviour. Low, sure.
   - :1448 `routine[-1]["text"].startswith("routine") or routine[-1]["kind"] == "clock.bell"`;
     :1254 `"the interval" in o.reason or "the glass" in o.reason`; :2672 `len(checked) >= 6`;
     :1247 `len(folded) >= 2`. Loose but each beside a sharper assertion. Low.
   - :2213-2220: the check that a letter is not seen before the boat brings it is
     `t.content.get("tick", received.tick) >= received.tick`: a data turn with no `tick` passes
     by default. Tool-result turns carry no tick, so a letter leaked through a tool result before
     the boat came would pass. Medium, likely.
   - :1571-1573 asserts `used == set(AGENT_LOG_KINDS)` then loops asserting each kind in `used`:
     the loop is redundant. Nil.
4. **(c)** Truth 43's six tests share one script `[REPEAT, ""]` (:642, :682, :755, :2993, :3036,
   :3051, :3086 all reach a pause by the same three repeats); a pause fixture would serve.
   `test_the_repl_turn_mode_*` (:1743, :1783, :3086, :3127) each drive `repl_mod.main` through a
   new save from scratch.
5. Good and hard: :1086 (in-world text never becomes operator text, even when the fake obeys
   it), :2863 (a bell that falls while the call is in flight), :2993 (the ten real minutes on
   the server's monotonic clock, monkeypatched, then replayed). :1684-1688 reads `client/log.js`
   and `client/style.css` for substrings: a test of source text.

## test_anchor.py

1. 22 tests, 3 parametrised (4, 3, 2): 28 cases. Module fixture `brought_up`: the frigate under
   plain sail in Carrick Road, anchored, forty minutes sailed. Proves ground tackle from the
   file, bringing up, riding to the tide, dragging, parting, weighing, veering, refusals,
   the belays of getting under way, deep-water and short-water rules.
2. **(a)**
   - :59-79 `test_every_ship_carries_ground_tackle_by_her_size_from_the_generator`, whose
     docstring says "her anchors by her burthen (Luce: five hundredweight a hundred tons)":
     :73 reads `w.ship.spec.hull.burthen_tons if hasattr(...) else None` and :79 asserts
     `burthen is None or burthen > 0`. `burthen_tons` exists nowhere in `freesail/` (grep: no
     hit). So `burthen` is always None and :79 always passes; nothing in the test relates anchor
     weight to burthen except the frigate's 2,200-2,600 kg band. For the brig, cutter and
     schooner the weight is checked only `> 0`. Weight medium, sure.
   - :226-230 builds `parted` from `w.ship.log_lines()` `if hasattr(w.ship, "log_lines")`; the
     ship has no such method (only `freesail/agents/director.py:1590 log_lines(world)`), and the
     value is overwritten at :232. Dead code. Low, sure.
3. **(b)**
   - :206-207 `assert anchor.scope_fathoms > 20.0` then `assert "dragging" in
     w.readings["anchor"]["words"] or anchor.scope_fathoms >= 20.0`. The right disjunct is implied
     by the line before: :207 cannot fail, so the anchor reading's "dragging" word
     (`freesail/api/readings.py:2215-2216`) is untested here. Medium, sure.
   - :210 `anchor.cable_load_kn >= 0.0`: any load passes. Low.
   - :235 `w.readings["anchor"]["words"] == "lost" or "lost" in w.readings.words("ground_tackle")`.
     Low.
   - :396 `all(e.severity is Severity.ROUTINE for e in events(w, "anchor.holding"))`: passes on no
     holding line at all, which a 900 s drag in forty knots may well produce. Low, likely.
   - :222-224 sets `cable_condition = 0.5` and `cable_load_kn` by hand and calls
     `A.judge_cables` directly: a unit test of the judgement, not of a cable wearing out. Fine as
     a unit, but the name ("parts when worn out") overclaims.
4. **(c)** `test_she_drags_in_a_gale_...` (:188) and `test_a_dragging_anchor_is_an_urgent_line...`
   (:387) build the same world (OUTER_ROAD, 40 kn, 20 fathoms, 900 s) for one assertion more;
   one test would do.
5. The module fixture is mutated: `test_she_rides_to_the_tide_...` (:152) runs `brought_up` on
   for up to 9 h + 3 h. Any test placed after it in the file sees a world twelve hours older.
   Fragile by order. :399 (the anchor's depth after sixty miles) is a good regression test of a
   real frame bug.

## test_api_door.py

1. 18 tests, one parametrised into 2 (19). `importorskip` of the vendor SDK (pyproject.toml:29), keyring, fastapi, httpx
   (:22-25): silent skip of the whole file without them. A local `MessagesServer`
   (`tests/messages_api.py`) per test; the door runs in a thread against a `TestClient` game.
   Proves the key's road (store, env, file), refusal to start where a key would leak, the wire
   shape, cut-offs, refusals, another model's reply refused, the exchanges file scrubbed, the
   second vendor's dialect, pictures only to image-reading models.
2. **(a)** None.
3. **(b)**
   - :701 `got["thread"].join(timeout=120)` with no assert that the thread ended: a hung door
     passes. Low, likely.
   - :552-562 `test_no_file_of_the_repository_holds_the_shape_of_a_key` skips outside a git
     checkout and swallows `UnicodeDecodeError, OSError` per file (:568-571).
4. **(c)** None notable.
5. :548 is a repository-hygiene scan of every tracked file, not a test of the game; it belongs
   in CI as a linter step. Good: :121 (the door refuses to start where the key would be written)
   and :284 (the exchanges file holds no key).

## test_bellerophon.py

1. 53 tests, 8 parametrised: 93 cases (the two `[p for p in ARMED if p != SIXTY_FOUR]` are 7
   each). Module fixture `her` (`load_ship`), cheap. Eight tests are slow-listed (10-30 s
   each). Proves the 74's data file against its sources (hull, ports, spars, sails, guns, crew,
   anchors, boats), her handling as tuned, the bill by deck, lee ports shutting by heel.
2. **(a)**
   - :1384-1427 `test_a_cruiser_keeps_away_from_her_and_a_kings_frigate_does_not_today`: the
     docstring says the King's frigate closing her is "the engine's today, recorded, the rank-4
     rule ... being her road's step 7, not built here". The test pins a known gap as passing:
     when the rule is built, the test fails and must be re-pinned. Medium, sure.
   - :2140-2187 truth 7-196's draft: the docstring admits the 74s "do not keep their places but
     engage her" because the frigate carries no private signal: the pace measured is of a world
     other than the one the name describes. Low, sure.
3. **(b)**
   - The file is predominantly pins of `data/ships/seventy-four.yaml`'s numbers against its
     sources, with tight bands (±0.01 to ±0.05). Those are honest where the source is cited, but
     most bands are "measured" figures of the file itself (e.g. :93, :97, :99, :161, :190 `measured
     == 26`, :356, :436 `abs(p.speed_kn(90, 15) - 7.74) <= 0.5`). Many dozens of numeric pins in
     the first 1,000 lines (not counted exactly). Data written by `tools/ships/bellerophon.py` and then read back
     with its own figures is a regression lock, not a proof.
   - :941-979 runs the generator in a subprocess and asserts the committed file equals its output
     byte for byte, plus eleven golden lines of the report. A test of a tool.
   - `BEAT_LINE` (:1542-1557): eight golden beat-to-quarters lines, one per armed file, "measured
     before B7.b and after". Eight golden-text pins.
   - Redundant bands: :436-437 (±0.5 of 7.74 inside 7.0-8.5), :1312-1313 (2,490-2,900 t then
     2,560-2,660 t). Nil.
   - :544 `round(867.0 / frigate, 2) == 2.06` divides a literal, not her broadside: it checks
     only the frigate's 421 lb.
   - :1371-1376 `far_only` monkeypatches `crews.CREWED_CAP = 0`, stepping round promotion so the
     far brain decides alone; stated, fair.
4. **(c)** `test_truth_7_194_her_particulars_hold_their_sources` (:1281-1362), "a draft for
   Phase 5 to move", re-asserts beam, waterline, draught, displacement, GM, the lowest sill and
   its half-breadth, port counts and size, the 74/82/78 pieces and broadsides, crews, complement,
   lieutenants, marines, filling, exercise, anchors, boats and the description key: each already
   asserted in :82-102, :150-161, :528-544, :574-604, :607-629, :650-673, :776-795, :798-834,
   :842-878. A second copy of a third of the file. Truths 7-195 (:2036, :2105) are likewise
   drafts. `test_she_sails_under_her_rules_captain_with_no_fit_named_and_round_trips` (:1437) is
   the same scenario round-trip as test_bilander.py:2047 (and, by conftest, test_neufchatel.py):
   one parametrised test over files would serve.
5. :632 `test_the_viewer_draws_every_gun_of_her_three_fits` does `sys.path.insert(0, tools)` and
   imports a tool; the path is left changed for the rest of the process. :1709 (robbing by deck
   with shut ports) and :1938 (a deck fired to leeward leaves out shut ports) are good tests of
   hard behaviour.

## test_between_hulls.py

1. 8 tests, none parametrised. Proves a person sent aboard another hull by boat is a visitor
   there, his station going with him as a voice; both replay roads; boarders' officer on a deck
   won; a captive put aboard; the director's `person: goes aboard`.
2. **(a)** :138-139 `test_a_stationed_person_sent_aboard_another_hull_is_a_visitor_there_and_home_again`
   is the single line `_round_trip()`; :142 calls `_round_trip()` again and adds the replay. The
   first test is wholly contained in the second: the same hour and a half of two hulls sailed
   twice for nothing. Low (time), sure.
3. **(b)**
   - :183-189: "this seed is the first from 1 under which the first lieutenant ... stands at the
     deck won". A seed hunted to make the scenario come out; any change of the fight's draws
     breaks it for a reason unrelated to what it names. :258-260 pins the default seed's death
     `(530, "Mr Pearce is killed: a blow of a tomahawk.")`. Two RNG pins. Medium (brittle), sure.
4. **(c)** `_until_visiting` (:302) sails the first half of `_round_trip` again; three tests sail
   the same visit.
5. :353 (a boat refused beyond the pull leaves no hull made) is a good regression test.

## test_bilander.py

1. 48 tests, 6 parametrised: 63 cases. Module fixtures `her`, `spec`, `doc` (loads), `settee`
   (imports `tools/ships/settee.py` by path) and `module` (a subprocess running the generator to
   read its constants). `_her_settle` (2,400 ticks, all hands, trims) is sailed afresh in 13
   cases (:1433 ×5, :1508, :1576, :1658 ×2, :1917 ×2, :1995 ×2); only two of the file's tests
   are slow-listed. Proves the bilander's data file against Chapman, Gwyn, Steel, Lloyd's; her
   settee's cut; her handling hove to, tacking, wearing, dipping.
2. **(a)**
   - :1428-1466 `test_hove_to_her_main_topsail_goes_to_the_mast_and_she_lies_to_both_ways`
     monkeypatches `scripts.SETTEE_KEPT_HOVE_TO` to False for two of five cases. The game sets it
     True (`freesail/evolutions/scripts.py:2140`) and nothing changes it. Two cases (each a 2,400
     tick settle and 900 ticks hove to) prove an alternative the game never runs. Low, sure.
3. **(b)**
   - :160-166 `test_her_burthen_by_the_old_measure_is_about_130_tons`: `b = 19.4`; asserts
     `(length - 0.6*b)*b*b/2/94 == approx(tons)` for literal lengths. **It calls no code of the
     project.** It is arithmetic on its own constants and passes whatever the game does. The
     same arithmetic is repeated at :842-844 inside truth 7-197. Weight medium (a reader thinks
     her burthen is tested), sure.
   - :603-658 the generator's report: the committed file equal to its regeneration byte for byte,
     and thirteen golden lines of the report's text. A test of the tool.
   - `HOVE_TO` (:1414-1420) and `CLOSE_HAULED_HELM` (:1425): 30 measured figures pinned with
     ±1-3 degrees; `REQUESTS` (:1845-1855): sixteen tuples; the tick pins of :1560-1566,
     :1622, :1646, :1705, :1728, :1980-1984, :2034. The comments record repeated re-pinning
     ("old: -2.02, -2.02 and +0.25"). A regression lock on tuning, explained in prose, not a
     proof of sailing. Medium (cost of re-pinning), sure.
   - :1209-1211 `water_tons == 3.0` then a band `8*60/252 < 3.0 < 2*8*60/252`: the band is
     implied. Nil.
   - :697 `all(v >= 0.0 for row in polar.speeds_kn for v in row)`: any polar of zeros passes. Low.
4. **(c)** Truth 7-197 (:806-897) re-asserts :143-157, :374-401, :412-450, :1024, :911-962,
   :1230-1255: a second copy, "drafted here for Phase 5". :2047 is the scenario round trip of
   test_bellerophon.py:1437. The 13 settles could be one settled world checkpointed per wind and
   loaded per test.
5. :1809 (rule 5's measure of the settee held aback) and :1917 (truth 7-198, the dip in stays
   in one spell, six hands) are strong behavioural tests. :965 and :971 insert `tools` into
   `sys.path` for the process.

## test_bill_marines_and_flag.py

1. 7 tests, 3 parametrised (17 files, 5, 4): 30 cases. No fixture of weight. Proves the
   schema's `marines` and `flag` keys load, validate in words, and pickle as before.
2. **(a)** The module docstring (:8-11): "Both are inert: no file carries either, nothing reads
   them". False today: `data/ships/seventy-four.yaml` carries both (KEYLESS_FILES at :39 excludes
   it), and the beat to quarters reads `marines` (test_bellerophon.py:1596-1624). Stale
   docstring. Low, sure.
3. **(b)** :83-84 `if crew is None: return` and :89 `if bill is not None:` make a case pass with
   nothing checked; every ship file carries `crew:` (grep), but five of the 17 (the boats) have no
   `quarter_bill`, so their bill half is skipped silently. Low, sure.
4. **(c)** :78 overlaps test_bellerophon.py:1651 (no one-gun-deck file has `marines`).
5. Sound.

## test_boat_director.py

1. 5 tests, none parametrised. Proves the `followed` reading, the boat's events, the director's
   `follow`, the boat lost by `aboard:`, the truth's view of a manned boat.
2. **(a)** None.
3. **(b)**
   - :116-120: "swamped: doubted on a smooth sea, performed with a reason" in the comment; the
     code is `if said.startswith("Doubted"): said = D.direct(... [reason: a squall])` then asserts
     the boat swamped. If the doubt never fires the test passes the same. The doubt of
     `boat_swamped` (`data/director/aboard.yaml:342`) is untested. Medium, sure.
   - :104 `"painter parted" in said or "gone adrift" in said`; :84
     `_events(frigate, "driver.follow") or _events(w, "driver.follow")`. Low.
4. **(c)** None.
5. Otherwise sound.

## test_boat_drawing.py

1. 3 tests, one parametrised over the 5 boat files: 7 cases. One test runs Node (skipped where
   Node is absent, `tests/test_view_geometry.py:173`). Proves the boats' generated profiles and the
   viewer's oars.
2. None. 3. None beyond the 0.06-0.07 h band at test_boat_hull (not here). 4. None. 5. Sound; the
   Node test is the only test in my list of the browser's drawing code.

## test_boat_hull.py

1. 10 tests, none parametrised. Proves the boat manned as a hull, pulling at 3-4 kn and tiring,
   stepping the mast, coming alongside with her log folded, errands without a hull, the hoy as a
   vessel, the boat lost and replaced, swamping.
2. None.
3. **(b)** :291-293 `test_a_sea_above_her_weather_swamps_her_by_the_sea_states` asserts four
   memberships of two constant sets: it never puts a boat in a sea. The name promises a
   behaviour the body does not exercise. Low, sure. :27-32 `_run_until` returns `minutes` on
   timeout rather than failing; callers mostly assert `< minutes`, but :76, :186, :208 do not
   check it (the next assertion does the work).
4. **(c)** :345-346 is a wrapper of a helper, so the helper can be called from truths; fine.
5. :84 (the men tire) is a good behavioural test.

## test_boat_names.py

1. 2 tests. Three hulls, two asleep. Proves the boat's people are the giver's hull's and a
   person of another ship is refused in words. 2-4: none. :64 `e.kind in ("evolution.started",
   "order.accepted")`, guarded by :65. 5. A good regression test of a real id-collision bug.

## test_bowsprit_yards.py

1. 17 tests, 6 parametrised (3, 2, 3, 3, 4, 8): 34 cases. Fixture ships from
   `tests/rig_fixtures.py` and three files with the yards added in memory. Proves the
   spritsail yards are head yards and no mast's, in classing, trim, the helm's mark, windage,
   tacking, wearing, heaving to, shorten sail, the polar.
2. None.
3. **(b)** `ROWS` and `FIXTURE_ROW` (:81-115) are golden rows copied from
   `tests/test_rig_classing.py`; a change there will not be seen here. :575 pins evolution
   timings (`90 + 60 + 30`) from data. Low.
4. **(c)** Shares `_run`, `LIGHT_AIRS`, `_until`, `_after` verbatim with test_bellerophon.py
   (:455-463, :1076-1084) and test_bilander.py (:1398-1404): helpers duplicated across three
   files.
5. Sound. The "measured on the rule's absence" notes say the tests were seen to fail without
   the rule; good practice.

## test_brains.py

1. 10 tests, none parametrised. Proves the far brain: role by description and intent,
   perception from her own truth, states resolved into plans, cruiser doctrine (evade,
   chase, speak), the land guard, the world order's intent, station-keeping, the beating
   verdict's dwell.
2. **(a)** :377 `_ = destination`: a dead line keeping an import alive.
3. **(b)**
   - :122 `assert "Y" not in ids or all(s["made_out"] == 0 ...)`: `ids` holds vessel ids, which
     are `f"ship-{serial}"` (`freesail/world/ships.py:1561`), never the name "Y". The left
     disjunct is always true; the line cannot fail. The comment says "the brig twenty miles from
     the frigate is a sail and no more", but `far` is at 48 40 N, about fifty miles off and
     beyond any horizon, so it is not in sight at all. The "made out by eye at the lookout's
     distances" clause is untested. Medium, sure.
   - :299-301 `[sail.spoke lines] or not any(f"sail:{x}" in getattr(w.lookout, "_sails_seen", {})
     ...)`: the `getattr` default makes the right side true if the attribute is renamed. Low,
     likely.
   - :114 `"frigate" in ship["known"] or "ship" in ship["known"]`. Low.
4. **(c)** :217 overlaps test_bellerophon.py:1384 (cruiser evades a bigger enemy).
5. `world_at` and `put` here are imported by test_aboard_found, test_bellerophon, test_bilander
   and (via `put`) test_bellerophon's truth 7-196: a test file used as a library. Move them to a
   helper module; a change to this file's world silently moves four others'.

## General, across the sixteen

- **Drafts in the wrong place.** test_bellerophon.py and test_bilander.py hold five "drafts for
  Phase 5 to move into test_known_truths.py" (7-194, 7-195 ×2, 7-196, 7-197, and 7-198/199),
  each re-asserting the file's own earlier tests. Either move them or drop the duplicates.
- **Pins in place of proofs.** The two ship files are mostly locks on a generated data file's
  numbers and on tuning figures, with long prose histories of re-pinning in docstrings. They will
  catch any change, wanted or not, and so will be re-pinned without thought.
- **Sizes of documents.** test_agents pins the token size of a primer chapter and the counts of
  evolutions and papers; every content edit breaks the agent tests.
- **Tool and source-text tests in the game's suite:** generator byte-equality (bellerophon :941,
  bilander :603), `check_viewer_guns` (bellerophon :632, bilander :965), the repository key scan
  (api_door :548), and substring checks of `client/*.js` and `style.css` (agent_api :610,
  agents :1684).
- **Silent skips by import:** test_agent_api, test_api_door (`importorskip`); test_agents :1667
  imports fastapi without a skip, so the same missing package skips one file and errors another.

Not looked at: the other test files' own truths that these docstrings say call here
(test_known_truths.py), `tests/messages_api.py`, `tests/rig_fixtures.py`, `tests/test_crews.py`
helpers beyond names; no test was run, so no timing claim above is measured.

## Faults to plant

1. **test_agent_api.py::test_the_long_poll_waits_without_holding_the_worlds_lock.** In
   `freesail/agents/remote.py` line 886 change `wait = max(0.0, min(float(wait or 0.0),
   TURNS_WAIT_MAX_S))` to `wait = max(0.0, float(wait or 0.0))`. The comment says "the wait is
   capped". Prediction: passes although a door can hold a poll open without limit.
2. **test_anchor.py::test_she_drags_in_a_gale_on_short_scope_and_a_standing_order_sees_it.** In
   `freesail/api/readings.py` delete lines 2215-2216 (`if riding.dragging: words = f"dragging;
   {words}"`). The test's :207 claims to read "dragging" in the anchor reading. Prediction:
   passes (likely; the standing order may read the event or `to_dict()`'s flag, not the words).
3. **test_anchor.py::test_every_ship_carries_ground_tackle_by_her_size_from_the_generator[data/ships/brig.yaml].**
   In `data/ships/brig.yaml` set the best bower's `weight_kg` to `1.0`. The docstring says the
   anchors are by her burthen. Prediction: passes (only `> 0` is asked of any ship but the
   frigate).
4. **test_bilander.py::test_her_burthen_by_the_old_measure_is_about_130_tons.** In
   `freesail/ship/loader.py` make `load_spec` raise `ValueError` for any path ending
   `bilander.yaml` (or change her beam in `data/ships/bilander.yaml` to 6.5 m). The name says her
   burthen is about 130 tons. Prediction: passes; it calls no project code.
5. **test_boat_director.py::test_the_boat_lost_by_the_directors_word_and_doubted_on_a_smooth_sea.**
   In `data/director/aboard.yaml` delete line 342 (`plausible_when` of `boat_swamped`).
   The comment says swamped is "doubted on a smooth sea". Prediction: passes.
6. **test_brains.py::test_the_perception_is_from_her_own_truth_and_sees_the_player_by_the_horizon.**
   In `freesail/world/ships.py` line 1983 replace `level, _ = o.made_out(distance,
   glass=(o.id == glass_for))` with `level = 3` (every sail in sight made out whole at any
   range). The docstring says a sail is made out "at the lookout's distances by eye". Prediction:
   passes (likely; :113 asks `>= 2` of a ship a mile off, :122 cannot fail).

Faults I believe no test in my files would catch, though a player would:

- **A player's seat on a hull not his own can never order.** In `freesail/agents/seat.py`, make
  `PlayerSeat.route` return the authority refusal whenever the seat's hull is not the player's
  own ship's hull. test_aboard_another.py
  :234 accepts `agent.refused`. A player seated as officer aboard the followed brig could give
  no order. (Location by name, not line: not read.)
- **The swamped boat on a smooth sea.** Fault 5 above: a director's model could swamp the boat in
  a flat calm with no doubt raised; nothing in my files sees it.
- **Ground tackle out of proportion.** Fault 3 above, applied by the generator rather than by
  hand (`tools/gen_ships.py` `ground_tackle_for`, e.g. hundredweights per ton divided by ten):
  every small vessel's anchors a tenth of their weight, dragging in any breeze; only the
  frigate's weight is banded.
