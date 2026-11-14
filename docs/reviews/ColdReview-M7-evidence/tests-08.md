# tests-08: the audit of nine test files

Reader's list: `tests/test_neufchatel.py`, `test_observer.py`, `test_officer.py`, `test_orders.py`,
`test_orders_m4a.py`, `test_orders_places.py`, `test_ordnance.py`, `test_parity.py`,
`test_people.py`, with `tests/conftest.py` read first for the tiers. Tree at 504a250. No test was
run; nothing but this file was written. Counts are of `def test_` lines and of the
`parametrize` tables as read.

| File | Lines | Tests (cases) | Fixtures of weight | Verdict |
|---|---|---|---|---|
| test_neufchatel.py | 1,759 | 51 (61) | module `her` (one YAML loaded, cheap); one test slow by name | a data file's audit in the main; helm bands drawn round the code; truth 7-192 repeats the file |
| test_observer.py | 316 | 10 (17) | none; one 24-hour day, marked `slow` in the file | sound in the main; the day proves little; four tests run twice through test_known_truths |
| test_officer.py | 3,917 | 64 (74) | none; every test makes and sails its own frigate world; four start a TestClient | proves much, pins much; a third is the consent brief; the handover test moved to fit the brief |
| test_orders.py | 2,877 | 85 (726; `TABLE` alone 470) | none; `FakeRunner` for the table; 49 chart worlds for the playtest table | sound grammar table; proves parsing, not the evolutions; some rows check only the kind |
| test_orders_m4a.py | 351 | 10 (35) | `close_hauled_frigate` (1,200 s sailed) built three times | sound in part; an `or` empties one table check; two dead slow ids in conftest |
| test_orders_places.py | 482 | 17 (18) | none; the deck-bill test sails 7 h with three fake stations | sound; a few `!=` and negative checks |
| test_ordnance.py | 966 | 24 (24) | none; a world at anchor per test | 17 of 24 stand on a fake magazine the real one has replaced; refusals well pinned |
| test_parity.py | 390 | 6 (6) | module `seated_world` (scenario, fake captain, 20 min) | truth 91 a good test; the enumerations prove a reason is written, not that a road works |
| test_people.py | 971 | 27 (27) | none; the crewed-brig world built three times | sound; leans on helpers imported from four other test files |

**Spot-checks of the earlier reader's claims.** Four were checked against the files and hold:
`test_winfields_tonnage_holds_by_the_navys_rule` is arithmetic on literals (test_neufchatel.py
114-118); `@pytest.mark.slow` stands in the file at test_observer.py:303 against conftest.py:6;
the `or len(h.agent.grants) == 2` at test_officer.py:3284-3286; `"in the gear"` against
`SailState.IN_THE_GEAR = "in_the_gear"` (freesail/ship/parts.py:136) at test_officer.py:437.
Two corrections are made in section 3 below: four tests start a TestClient, not five; and the
budget comment lists nine raises, not eleven.

---

## 1. tests/test_neufchatel.py (1,759 lines)

### Count and kind

51 test functions; two are parametrised (`test_her_words_name_her_through_the_index`, 8 cases,
line 930; `test_she_is_a_privateer_wherever_no_scenario_or_intent_names_a_role`, 4 cases, line
1090): 61 cases. One module fixture, `her` (line 72), a `load_ship` of one YAML file: cheap. No
day fixture. One test is named in conftest's `SLOW_TESTS` (the round trip, conftest line 546); the
tack, the wear and two heave-tos, the getting under way (about 2,400 s of ship's time), the lie
a-try and truth 9's two twenty-minute runs are sailed in the fast tier.

What it proves: that one ship's data file (`data/ships/hermaphrodite-brig.yaml`) holds the figures
transcribed from her design, that the generator tool writes that file, and that she tacks, wears,
heaves to, gets under way, lies a-try and reads as a privateer. About 30 of the 51 tests are
checks of a data file or of a tool, not of the game's behaviour.

### (a) No longer there, or no longer what the name says

- `test_her_gale_reefs_her_fore_course_twice_and_keeps_her_mainsail` (1569-1612). The docstring
  (27 lines) describes a gale sailed for 8,400 s with times and speeds. The body sails nothing: it
  loads the ship, sets the plain sail by hand (1599-1600), sets `topsail.reefs` and `course.reefs`
  by hand and calls the private `orders.storm._after_sail_lines` four times. The name and the
  docstring promise a gale; the body tests one helper's return value. Weight medium, sure.
- `test_truth_7_192_...` (1688) and `test_truth_7_193_...` (1296) call themselves "a draft for
  Phase 5 to move into tests/test_known_truths.py". `grep -n "7_192\|7_193"
  tests/test_known_truths.py` gives nothing: the move was not made, and the two "truths" live only
  here. Weight low, sure.
- `test_her_file_loads_rates_and_polars` (619) says of itself that the polar's "figures are pinned
  at step 5 ... below"; what is left in it of the polar is `all(v >= 0.0 ...)` and
  `closest_deg <= 90.0` (627-628), which every polar passes. A stepping stone kept after the
  later tests replaced it.

### (b) Built not to fail

- `test_winfields_tonnage_holds_by_the_navys_rule` (114-118) calls no code of the project at all:
  it is arithmetic on four literals written in the test. It cannot fail. Sure.
- `test_her_gale_reefs_...` 1611-1612: `ship.sails["fore.sail"].is_set`,
  `ship.sails["main.sail"].is_set and ... reefs == 0` assert the state the test set at 1599-1600;
  `_after_sail_lines` only returns a list of words (it is asserted on by its return value) and
  nothing the test calls could have changed a sail. Sure.
- `test_her_file_loads_rates_and_polars` 627-628: a polar of all zeros passes. Sure.
- The helm bands are fitted to the measurement after each tune. `test_her_helm_as_tuned_is_
  balanced_close_hauled` (1335): band -1.0 to +1.7, the code gives +1.65; the docstring says the
  band was "widened by 0.2 degrees" after the fore staysail's correction moved her, and that for a
  time "its band moved to her measure, +2.5 to +5.0". `test_her_helm_as_tuned_abeam_and_at_ten_
  points` (1360): band +0.3 to +4.0, the code gives +0.39, the lower bound moved from 0.5 to
  admit it. These are not wide bands (0.05 and 0.09 degree of headroom) but they are bands drawn
  round what the code gives, by the file's own account. Weight medium (the test records the
  tune; it does not judge it), sure.
- `test_she_wears_and_lies_to_...` (1461): hove to she must make less than 3.5 kn (1505); the
  code gives 3.12 kn. The docstring says this is "above" truth 12's 1.6 kn. A ship "hove to" at
  three knots is passed by a bound set above what she does. Weight medium, sure of the bound; I
  did not read truth 12.
- `test_her_scenario_round_trips_...` (1156): speed 6.22 +-0.5 kn (1221), a band that holds every
  figure the docstring lists from five successive tunings (5.95 to 6.22). And the docstring states
  that sailed eleven minutes longer she "takes the ground at 4,266 s in a fathom and a half ...
  the lookout's warning ... not acted on", "not mended": the test stops at 3,600 s, short of a
  defect the file knows of. A player's privateer under the rules captain runs aground while
  "investigating a stranger"; no test in this file fails for it. Weight high (as a known defect
  with a test cut short of it), sure of the text; the grounding itself I did not reproduce.
- `test_her_polar_is_drawn_...` (1261): +-0.5 kn about 4.85, 8.53, 12.07; again every older tune
  in the docstring (4.95/8.68/12.22, 4.99/8.73/12.27) is inside. Likely sound enough as a guard
  against gross change; it would not catch a 5% loss of speed.
- Golden text and pins, counted: 9 exact sentences of the generator's stderr (576-596), one
  byte-for-byte comparison of the generated file (575), 15 rail points and 33 port figures
  compared for equality with the YAML (162-170), the class words (614), the description words
  (906), the 17-row `ROLE_BY_INTENT` table "measured before the step" (1014-1034), the quarters'
  counts (826-836), three notes lines from the gun checker (709-715). Most have a source named
  in a comment; `ROLE_BY_INTENT` and the quarters' counts are what the code gave.
- `test_her_quarters_at_the_beat_...` (805): the docstring says the design has the marines "stand
  apart from the guns" and that the engine instead puts all sixteen at the carronades, "and is
  reported". The test then pins the engine's behaviour (829-834). A departure from the design is
  held in place by its test. Weight medium, sure.
- No `xfail`, `skip`, `try/except` or empty loop found.

### (c) Might be one

- `test_truth_7_192_...` (1688-1759) repeats, figure for figure, assertions made earlier in the
  same file: the hull's five (1711-1715 against 95-103), the masts (1718-1719 against 279-282),
  the boom and fore yard (1726-1727 against 311-313), the ports (1729, 1735 against 164, 174), the
  guns (1737 against 660), the broadside (1741 against 722), the company (1743-1745 against
  740-756), the classing (1746-1748 against 455, 463, 439), the description (1753-1759 against
  922-926, 949, 959). It adds nothing. One of the two should go.
- The hull, spar, sail, gun, company, tackle and stores tests (91-900, about 20 tests) are one
  table of "key, figure, tolerance, source" against one loaded spec; they are written out as
  twenty functions of hand-built asserts. The docstring says they are "in the band form of
  tests/test_ship_particulars.py": the other ships have the same family again in their own
  files (`test_bilander.py`, `test_bellerophon.py` are named in conftest). One table-driven test
  over all ships would serve.
- `ROLE_BY_INTENT` and `test_her_row_sails_by_her_first_role_and_no_other_row_moves` (1037) cover
  every description in the game and must be edited for every new ship
  (`set(ROLE_BY_INTENT) == set(S.DESCRIPTIONS)`, 1054); they belong with the brains' tests, not in
  one ship's file. `test_only_she_has_a_boomless_gaff_sail_beside_a_course` (1615) likewise loads
  every ship.
- `under_plain_sail(HER, ...)` is built afresh in six tests (1292, 1356, 1373 twice, 1387, 1556,
  1645) and `close_hauled_on_starboard(HER)` in three (1442, 1485, 1491): one settled world per
  point of sailing, shared by a module fixture, would do.
- `test_her_broadside_by_70s_rule_...` (718) also asserts the brig's 268 lb and the frigate's
  421 lb, which are other ships' figures.

### Anything else

- Tests of tools, not the game: `test_the_generator_writes_her_file_as_committed_...` (559,
  runs `tools/ships/neufchatel.py` in a subprocess), `test_the_builders_checklist_...` (693,
  `tools/check_viewer_guns.py`; it also does `sys.path.insert(0, .../tools)` at 699 and never
  removes it, so later tests in the same worker import with `tools/` first on the path).
- Tests of a document: `test_her_notes_carry_no_figure_a_rule_computes` (599) greps the YAML's
  comments; `test_every_line_of_her_shape_carries_its_rung` (226) checks the "marks" words.
- Private functions are called directly in eight tests (`scripts._masts_with_yards`,
  `_boom_mainsails`, `_square_rigged`, `_after_sail_lines`, `TackScript._after_swing_s`,
  `_haul_words`, `_courses_drawing`, `S._default_fit`): a rename breaks the test with the
  behaviour intact.
- The docstrings carry the project's tuning history ("old beside new", five generations deep in
  places: 1156-1175, 1335-1353, 1423-1439, 1569-1595). A builder reading a failure has to find
  the current figure among four old ones.
- A good one: `test_she_stays_quickly_her_light_main_yards_hauled_short` (1423) sails a real tack
  and checks the words said, their order and spacing, and that she ends on the other tack to
  windward.

---

## 2. tests/test_observer.py (316 lines)

### Count and kind

10 test functions; one parametrised into 8 (`test_what_an_observed_scenario_cannot_carry_is_
refused_in_words`, line 82): 17 cases. No fixtures; nine tests each load the scenario
`the-channel-observed.yaml` and make its world (business on, a region loaded). One test carries
`@pytest.mark.slow` in the file (303) and sails 24 hours.

Proves: a world with no player's ship loads, refuses the ship's orders in words, answers "no ship
followed", follows a named hull and gives the view back, moves the view, and replays.

### (a)

Nothing dead found. One contradiction with conftest: its docstring says the `slow` mark "is
applied here and never in a test file" (conftest 6); this file applies it at line 303. Low.

### (b)

- `test_a_day_observed_...` (304-316): `w.clock.tick == 24 * 3600` (311) is what the helper ran;
  `any(e.kind == "driver.follow" ...)` (310) is the line written by the helper's own
  `w.follow("Medusa")` at 297; `any(e.kind.startswith("lookout") or "Sail ho" in e.text ...)` (308)
  is satisfied by any one lookout line in 24 hours of the Channel. What is left that could fail
  for a broken day: the business made at least one ship (307), the Medusa is awake and within 20
  miles of the Deadman (306, 316). Weight low to medium, sure.
- `pytest.importorskip("fastapi")` (258): the server is an optional extra (pyproject line 20), so
  on a machine without it the browser's test is skipped silently. `test_officer.py` imports
  fastapi with no guard (984, 1147), so the two files disagree about whether it may be absent.
  Low.
- `"observed" in json.dumps(w.save()["scenario"])` (117): a substring of a JSON dump; the key
  with value `false` would pass. Low.

### (c)

- `tests/test_known_truths.py` 13058-13083: truth 7-320 imports and calls this file's
  `test_a_day_observed_...`, and truth 7-321 imports and calls three more of its tests. In a whole
  run each of the four is run twice under two names, the 24-hour day among them. The "truth" tests
  add no assertion. This is the pattern conftest's `SLOW_TESTS` shows across the suite (a
  `test_x.py::...` line followed by a `test_known_truths.py::test_truth_...` line for the same
  thing, e.g. conftest 122-156). Weight medium (time, and a false count of what is proved), sure.
- Nine worlds made from the same scenario for nine tests; the five that only read
  (`test_the_observers_world_...`, `..._readings_...`, the loader's first) could share one.

### Anything else

Sound in the main: the refusals are exact words checked against the same order given to a world
with a ship (207-217), the replay is by digest mid-follow (194-204).

---

## 3. tests/test_officer.py (3,917 lines)

### Count and kind

64 test functions; one parametrised into 11 (`test_an_order_outside_the_domain_is_refused_in_
words_and_logged`, line 440): 74 cases. No module fixtures: every test builds its own frigate
world (`frigate_world`, 65) and most sail it 60 to 1,500 s before seating a scripted fake; a few
run two to four hours of ship's time (2616, 2892). Four tests start a FastAPI `TestClient`
(980, 1141, 1215, 1577; corrected from "five"), each importing fastapi with no guard; 2942
imports `freesail.ui.server` too. None of this file's tests is in conftest's `SLOW_TESTS`.

Proves: the officer of the watch's station under a scripted fake: the deck given and taken, which
orders lie in his domain, the captain's grants, the welfare detectors (nudge, pause), the three
ways of leaving, reseating and replay, the handover note; and, for about a third of its length
(1328-2336), the consent brief's text and the re-ask rule.

### (a)

- `test_the_doors_name_the_officers_station` (2425-2448): the docstring promises "`--station
  officer` at the MCP bridge and the local runner". The body reads the two modules' source text
  and asserts the string `"--station"` is in it, that `choices=` is not within the next 200
  characters, and that `take_the_watch` occurs somewhere in `mcp_server.py` (2432-2437). No flag
  is parsed, no door opened. Weight medium, sure.
- `test_a_released_station_is_seated_again_...` and `test_opt_out_final_...` take `tmp_path`
  (1033, 1091) and never use it. Trivial.

### (b)

- `test_the_handover_note_is_asked_for_at_the_budgets_fraction_...` (902-977). The door's budget
  is set by the test, and the comment at 920-944 records it being raised nine times
  (16,000 → 18,000 → 18,500 → 20,000 → 20,500 → 21,000 → 21,500 → 22,000 → 22,500 → 23,000;
  corrected from "eleven"; the comment itself says "five hundred more, 22,500" twice, at 937
  and 939), each time because the officer's brief had grown past six tenths of the last figure ("13,516 with
  both, over the fraction of 22,500 (13,500): five hundred more, 23,000"). The test's own
  precondition (946) is kept true by moving the test. What the history says about the game: the
  frigate officer's conversation is about 13,500 tokens at the moment he is seated, and the local
  runner's context in the same file is 16,384 (996, and the advice in `freesail/agents/local.py`
  604-606), whose six tenths is 9,830. At that door the handover note is asked for before the
  officer has done anything. No test fails for it; this one is stepped round it each time.
  Weight high, likely (I did not run a seat at 16,384 to see the ask; the arithmetic is the
  file's own and `harness.handover_threshold`, harness.py 3940-3957).
  Read further in the harness by this reader: `_conversation_size` counts from the operator
  turn inclusive (harness.py:3928), so the brief itself is in the size; at 16,384 the reserve
  is `max(0.3 * 16384, HANDOVER_RESERVE_TOKENS = 14000)` (harness.py:365, 3951-3953), so the
  six tenths governs (3955-3957): threshold 9,830, asked again every 1,638 tokens of growth
  (`HANDOVER_ASK_AGAIN_FRACTION = 0.1`, harness.py:342). The fold (3976-3993) keeps the brief
  whole, so it cannot bring the size under the threshold: at that door the officer is asked for
  a note at his first sample and again each time the talk grows by a tenth of the context.
  Sure of the code; likely of the effect.
- `test_the_handover_is_asked_for_at_a_reserve_in_tokens_...` (3668): the thresholds are checked
  by restating the code's formula (`int(0.6 * 16384)`, `131072 - int(0.3 * 131072)`, `reserve //
  4`: 3690-3696). Then the budget is set to 16,384 and the loop waits for the ask (3699-3703):
  by the figures above the ask comes on the first sample whatever the reserve logic does. Likely.
- `test_a_chain_broken_by_a_quiet_sample_...` 765-766:
  `all("the same order" in n for n in lines(world2, "agent.nudged"))` and
  `not any("undoing" in n ...)`: both pass if no nudge was logged at all, and the comment claims
  the repeat detector does speak there. Whether the list is empty I did not run. A suspicion.
- `test_a_named_grant_means_what_it_says_...` 3284-3286:
  `[g.key for g in h.agent.grants] == ["place:falmouth", "place:the-manacles"] or len(h.agent.grants) == 2`.
  The `or` leaves only the length. Sure.
- `test_the_journal_is_read_back_...` 3243: `len(more["lines"]) == 400 or more["omitted"] == 0`:
  either arm alone passes. Low, sure.
- `test_an_order_in_the_domain_...` 437: after "set the royals" and fifteen minutes the fore
  royal's state must be one of `("set", "loosed", "sheeted", "in the gear")`. `SailState.IN_THE_GEAR`
  has the value `"in_the_gear"` (freesail/ship/parts.py 136), so the fourth can never match, and
  it is the state of a sail hauled up, not set. As written the test passes for a royal merely
  loosed. Low, sure.
- `test_hand_over_gives_the_deck_back_...` 866: `len(NOTE) < 400 and 60 < len(NOTE.split()) < 90`
  asserts the size of the test's own constant.
- `before = 0` then `h.revision == before + 1` (953, 959): arithmetic on a literal.
- Pins with no reason a reader can check: 14 digests of the consent brief and its sections
  (`BRIEF_DIGEST`, six `WATCHED_SECTION_DIGESTS`, 1702-1710; the three fixtures' own digests at
  1596, 1732, 1823, which test that a file in `tests/fixtures/` hashes to itself; four digests at
  1800). These are meant as change-detectors and say so (1880-1889); they prove the document did
  not move, not that the game does anything.
- Golden text: about 60 sentences of the consent brief (1966-2093), about 25 of the station
  briefs (2163-2284), and upward of 150 exact log lines and tool results through the file. Any
  rewording of a line breaks tests whose behaviour is intact; none of it is unfalsifiable.
- Word-count ratchet: `len(text.split()) < 2300` with 2,295 as sent (2112-2120); "the bound moves
  with each revision".
- Constants compared with literals: `(WELFARE_REPEAT_N, WELFARE_CONTRARY_N, DANGER_WORD_N) ==
  (3, 3, 3)` and four more (2159-2161), `HANDOVER_AT_FRACTION == 0.6` (977), `READ_LOG_MAX ==
  1000` (3248), `HANDOVER_RESERVE_SHARE == 0.3` (3692), `TOOL_CALLS_PER_SAMPLE == 16` (2538).
  A constant restated is a pin, not a test.
- No `xfail`, `skip` or swallowing `try/except`.

### (c)

- The same opening ("frigate_world(); set plain sail; run 60; seated(...)") is written out in
  about 35 tests. A function-scoped fixture would shorten the file; a module-scoped settled world
  copied per test would save the sail-setting each time.
- The three re-ask tests (1577, 1721, 1812) are one test with a table of (fixture, date, digest,
  door, sections changed); their bodies differ in six literals.
- `test_the_consent_brief_says_the_officer_exists_and_the_hash_is_the_files` (1936) and
  `test_the_sections_the_re_ask_rule_watches_are_pinned_by_digest` (1880) both assert
  `consent.brief_digest() == BRIEF_DIGEST` (1902, 2111) and both assert the set of
  `RE_ASK_SECTIONS` (1896, 2100; and a third time at 1542). With the six sections pinned whole by
  digest, the sixty pinned sentences of 1966-2093 can never fail first: they are redundant.
- The deck given and taken is proved at 199, 289, 837, 2343, 2398, 3087 with overlapping
  assertions of the same log lines ("The captain has the deck. The officer of the watch stays at
  the station, off watch.": 255, 2965). The docstring names `tests/test_agents.py` as holding the
  watcher's twin of each commitment; I did not read it.
- The undo-chain nudge is sailed three times with near-identical scripts (677, 2806-2821, 2824).

### Anything else

- A third of this file (1328-2336, about 1,000 lines) is the consent brief: a document under
  `docs/agents/`, its fixtures, and `test_every_yes_on_file_...` (1794), which reads the records
  committed under `docs/agents/consent/`. They are tests of documents and of the consent rule, in
  a file named for the officer; they would be found sooner in a `test_consent_brief.py`.
- A good one: `test_the_42_recorded_chains_are_silent_by_the_new_rule_...` (2768) replays 42
  chains recorded from real play against the old rule (checked to have fired, 2784) and the new.
- Good: the replay-by-digest tests (333, 1086, 1121, 1318, 2391) make the station's behaviour
  part of the determinism proof.
- Many tests are 80 to 150 lines with 30 to 60 assertions in sequence on one world (199-286,
  3251-3357, 3397-3549, 3552-3660). The first failure hides the rest, and a failure's message is
  a long string diff with nothing to say which step of the story broke.
- Private members used: `h._conversation_size()` (946), `driver._run_ticks` (2951, 2958),
  `repl._by_words` (3017).

### Finished by this reader (the file read whole, 1-3917)

Further (b) findings:

- `test_the_captains_word_allows_a_named_thing` 557-559: the second, allowed `tack ship` must
  start with `"By the officer of the watch: tacking ship."` or `"Order not carried out ('tack
  ship')"`. Either the ship tacks or refuses: the test proves the grant passed the domain, not
  that it did anything. Low, sure.
- `test_a_watch_with_the_fake_officer_replays_...` 2379: `assert lines(world, "agent.said")`,
  any line said at all. Low.
- `test_the_fake_officer_and_the_players_seat_keep_their_own_reckoning_...` 3911:
  `kind != "order.rejected"` for a stand-down. Low.
- More pins of what the code now holds: the first seven tool names in order (2440-2448), the
  twelve `DANGER_LINES` words (2680-2694), `load_vocabulary().irrevocable == ("cut away",)`
  (3513), `len(list(records.glob("*.md"))) == 3` (1274). A change of data breaks them with the
  behaviour intact; none states why the figure is right.
- `test_every_yes_on_file_given_before_the_revision_...` (1794-1809) reads the consent records
  committed under `docs/agents/consent/`: a test of files in the repository, not of the game. It
  cannot pass empty (`named and ...`, 1809), which is to its credit.

Further (c):

- "put the helm over" is refused in `test_put_the_helm_over_is_out_of_the_officers_brief_...`
  (3805-3816) and again in test_orders.py's G17 table (2711-2715).
- The three consent drill tests (1341, 1384, 3733, 3754) and `_drilled` (3717) could share one
  helper; `consent.ensure(...)` with seven keyword arguments is written out five times.

Anything else:

- The module docstring (982) names a vendor's chat client; harmless in a test, noted only.
- Good: `test_the_42_recorded_chains_...` (2768) first checks that each recorded chain *was* a
  chain under the old rule (2784), so the table cannot silently be wrong.
- Good: `test_the_three_ways_of_leaving_cannot_be_taken_for_one_another` (3087) checks the
  `leaving` data on the log lines in order (3132-3136), which a reworded sentence would not hide.

---

## 4. tests/test_orders.py (2,877 lines)

### Count and kind

85 test functions; twelve parametrised: `test_table` over `TABLE` (470 rows, line 86-816),
`test_the_playtests_refusals_now` over `PLAYTEST_REFUSALS` (49, 1972-2286), and ten smaller
tables (6, 24, 15, 9, 12, 7, 27, 7, 22, 5): 726 cases by a parse of the file (`ast`, not run).
No fixtures. `TABLE` runs on a bare `Ship` with `FakeRunner` (39-50), which records starts and
refuses only what it is told; the 49 playtest cases and some later tests each make a world on
the western Channel chart (`voyage`, 1889). Nothing in conftest's `SLOW_TESTS`.

Proves: the imperative grammar for the frigate, schooner, cutter and brig: the words a sailor
types, what each resolves to (evolution, subjects, parameters, sides by the tack), the refusals
and their words, level-0 line effects, the helm's targets, the card to the quarter point, the
number reader, and 49 orders the playtests had refused, given through `World.submit`.

### (a)

- Nothing removed whose test remains, as far as grep shows. Two comments record retired
  behaviour honestly: "splice the main brace" (207-209) and the colours and pumps (2701-2708).
- The row `(B, "reef the bowsprit", ok(evo="reef_bowsprit", ...))  # the runner refuses` (801):
  the table records as accepted an order the real game refuses, because the fake runner refuses
  nothing. The row proves the parse and states the opposite of the game's answer. Low, sure of the
  row; the real refusal I take from the row's own comment and test_catalogue, which I did not read.

### (b)

- The whole `TABLE` stands on `FakeRunner`: a row with `ok(evo=...)` proves which evolution the
  grammar asks for, never that it can be started or does anything. That is the design (the
  docstring, 1-9) and sound for a grammar test; the owner should know the 470 cases say nothing of
  the ship.
- Ten rows check only the returned kind: `let go the best bower`, `let go the anchor`, `come to an
  anchor with the small bower`, `veer to ninety fathoms`, `veer cable`, `heave short`, `weigh`,
  `weigh anchor`, `up anchor` (177-186), all `ok(kind="evolution.started")` with no `evo`,
  `subjects` or `count`. `test_table` (820-852) then checks nothing but the kind and that the log
  line is a capitalised sentence: a `veer cable` that starts `heave_in`, or a start of nothing at
  all with that kind returned, passes. Medium, sure.
- `test_table_is_large_enough` (855-859) asserts the size of the test's own table;
  `test_the_playtests_refusals_are_forty_nine` (2289-2294) counts its own table (49; 15, 16, 18;
  26 taken). Assertions of what the test set up. Low, sure.
- `test_the_playtests_refusals_now` (2302-2321): a `took` row passes on any of its kinds, and
  `TRIM_FAIR` is three (`evolution.started`, `order.accepted`, `sail.trimmed`, 1959). Low.
- `test_take_a_fix_is_completed_from_the_marks_in_sight` 2374-2375: every completion offered is
  submitted and must give `reckoning.fix` **or `order.rejected`**. A completion that is always
  refused passes. The name promises completions from marks in sight; the loop cannot fail on what
  the completions do. Medium, sure.
- `test_the_three_forms_of_allow_...` 2409: `2.0 < (steer - line) % 360 < 40.0`, a 38-degree band
  for the allowance of two knots of set. Low; I did not compute the figure.
- `test_the_phrasings_of_g17_on_a_ship` 2727-2732: the `no` branch, unlike `test_table`'s
  (828), does not check that the runner started nothing.
- No `xfail`, `skip`, swallowing `try`, or empty loop.

### (c)

- The helm words are proved three times in this suite: `TABLE` rows 317-338 and 562-601;
  `test_come_up_and_bear_away_...` (1032), `test_half_points_are_kept` (1362),
  `test_conning_words_set_the_helm_modes` (1376); and test_orders_m4a.py's `HELM_TABLE` (195-220)
  with the same words (`luff`, `bear away`, `come up a point`).
- `FakeRunner` is defined here (39), again in test_orders_m4a.py (32) and, by that file's
  docstring, in test_trim_order.py: one in a shared helper.
- `test_the_phrasings_of_g17_on_a_ship` (2720) re-implements `test_table`'s body in short; its rows
  belong in `TABLE`.

### Anything else

- Good: `test_the_whole_card_in_words_is_read_to_the_quarter_point` (2472) reads every quarter
  point in every form (over 512 forms) and checks the degrees to 1e-9; `test_every_number_to_a_
  hundred_...` (2589). Hard things, proved whole.
- Good: `test_an_unreadable_course_is_refused_and_never_steered_to_its_last_word` (2525) checks the
  helm is untouched after a refusal (2534).
- `test_table`'s failure message names the order and the expected words (827, 831): a builder can
  read it.

---

## 5. tests/test_orders_m4a.py (351 lines)

### Count and kind

10 test functions; two parametrised (`TRIM_TABLE` 15, `HELM_TABLE` 12): 35 cases. No fixtures;
`close_hauled_frigate` (234-252) sails 1,200 s and is built afresh in three tests (259, 318, 336).
Two of its tests are in `SLOW_TESTS` by name (conftest.py:317, 319).

Proves: `trim the <sail>`, `tend the sheets`, the owner's words for bearing away, `steady out the
bowlines` after falling off and coming up, and the starter standing-orders file loading on the
console and on the server driver.

### (a)

- conftest.py:318 and 415 name `test_the_starter_file_loads_in_the_console_with_the_well_refused_
  and_the_rest_entered` and `..._with_the_well_held_and_the_rest_entered`. Neither exists: the test
  is now `test_the_starter_file_loads_in_the_console_and_every_order_is_entered` (318). The rename
  (the well's order left the book, 328) left two dead ids; the test, which sails the same 1,200 s as
  its slow sibling at 336, now runs in the fast tier. Low, sure (checked by a parse of the names).
- `test_the_starter_file_names_a_source_for_every_order` (343-351) checks words in the data file's
  comments: a test of a document.

### (b)

- `test_trim_the_sail_and_tend_the_sheets` 142-144: `data["trimmed_sheets"] == [...] or
  len(data["trimmed_sheets"]) == len(expect.sheets)`. The `or` leaves only the length: the names
  and their order are never checked for the 2- and 3-sheet rows. The same shape as
  test_officer.py:3284. Sure.
- `test_steady_out_the_bowlines_...` 300: `>= 10` lines that start "Steadied out" for five
  bowlines; a band with no upper bound. Low.
- The 1,200 s sailed in `close_hauled_frigate` is the price of a test whose two real assertions are
  the book's names and the count 7 (318-333).

### (c)

- `HELM_TABLE` repeats test_orders.py's helm rows (see section 4).
- The two starter-file tests (318, 336) build the same world to load the same file: one world,
  copied, would do; or one test with the two drivers as parameters.

### Anything else

- The module imports `freesail.ui.server.Driver` at its head (25), and server.py imports fastapi at
  its head (116): without the `server` extra the whole file fails to collect, where
  test_observer.py `importorskip`s the same dependency. CI installs it (`.github/workflows/ci.yml:66`,
  `.[dev,server]`); `dev` alone does not (pyproject.toml:19-20). Low.
- Good: `test_steady_out_the_bowlines_...` (259) sails the real ship through four points and eight
  and back, and checks the bowlines stand, are let go with their words, and are steadied out.

---

## 6. tests/test_orders_places.py (482 lines)

### Count and kind

17 test functions; one parametrised into 2: 18 cases. No fixtures. `in_falmouth` (47-53) brings
the schooner to anchor in Carrick Road (360 s) in seven tests; `test_the_deck_passes_among_the_
officers_...` (339) sails seven hours with three fake officers seated (slow by conftest.py:455).

Proves: a person's place and what it allows (below, aloft, ashore, the cabin the captain's), the
port's places ashore, books drafted, posted and given to the boat, several officer's stations and
the deck passing by the watch bill, the boat's passengers, the waterman, the deck's orders refused
below and ashore.

### (a)

Nothing dead found. The docstring says truths 7b-100 to 7b-102 are in test_known_truths.py
(4-5); conftest.py:451-454 lists them beside two tests of this file, the same pattern as
test_observer's.

### (b)

- `!=` and negative checks that pass on almost anything: `set the main topsail` `.kind !=
  "order.rejected"` (142), `go ashore` likewise (482), `"ashore" not in w.submit("the port").text`
  (107), `the signals` `.kind.startswith("query.")` (461). Low, sure.
- `test_a_place_ashore_named_aboard_says_go_ashore_first_and_go_alone_runs_the_clock` (158-169):
  the second half tests the console's `go` command on another world, a subject apart from the first
  half and from the file. Low.
- No `xfail`, `skip`, `try/except`, or empty loop; `until` (60-65) raises on time out rather than
  passing.

### (c)

- `world_at` (32-44) here, `world_at` in test_ordnance.py (139-156) and `world_for` in
  test_people.py (24-35) build the same Scenario with the same wind and seed; `in_falmouth` here
  and `at_anchor_in` in test_ordnance.py (159-165) are the same anchoring. One shared helper.
- `seat` (68-74) is imported by test_people.py (723): a helper that lives in a test file.

### Anything else

- Good: `test_the_deck_passes_among_the_officers_at_the_change_of_the_watch_by_the_bill` (339)
  checks the exact line at noon, the deck back at the first dog watch, the captain's `I have the
  deck` and that the first lieutenant keeps it through a change.
- Good: `test_the_boats_passengers_are_carried_or_refused_in_words_never_dropped` (382) is a
  regression test for a named defect (R-62) with the boat checked not sent on each refusal.

---

## 7. tests/test_ordnance.py (966 lines)

### Count and kind

24 test functions, none parametrised. No fixtures; each test makes one to three worlds at anchor
(`at_anchor_in`, 360 s). `hurry` (184-190) brings the hoy's job due at the next tick, so that no
test sails the hoy's hours; each test that uses it asserts the due tick first (316, 347).

Proves: the ports' `ordnance:` blocks; the refusals of a demand for powder and shot in order and
words; the King's cutter's issue at Plymouth; the hoy's two stages; the purse paid at alongside; a
short purse; a ship weighing with the hoy alongside; the gunner's account and its keeper.

### (a)

- `FakeMagazine` (71-104) and its docstring: "Builder 1's magazine as §1.1 gives it, until it is
  merged (§7.3)"; the module docstring (10-19): "Written before Builder 1's magazine was merged".
  It is merged: `freesail/ship/parts.py:818` `class Magazine` with `wanting` (993-1012),
  `account_lines` (1018-1023), `return_barrels` (1025), `describe` (1042), and test 825 asserts
  `type(mag) is Magazine` on a world made the ordinary way. Yet 17 of the 24 tests still replace
  the real magazine with the fake (`kings_cutter`, `after_the_action`, `fake_magazine`, used at
  296-823). Every figure they pin of what she wants ("1 barrel of powder and 149 round shot",
  "3 barrels ... £16 12s") is the fake's arithmetic, not the game's. The fake's `wanting` is a
  near copy of the real one (90 against 1012) and its `account_lines` differs from the real
  (`f"{when}: {words}."` with a full stop, 100, against parts.py:1023 without). A fault in the real
  `wanting` reaches none of those 17. Medium, sure.

### (b)

- `test_the_kings_cutter_completes_her_magazine_...` 373: `page.lines == [*mag.describe(),
  *mag.account_lines()]`, the paper compared with the fake's own output. On the fake this proves
  the paper copies the magazine, not what the magazine says. 869 does the same on the real one,
  which is the test that counts.
- Pins: the count of ports without a block, `27 + 8 + 8 + 4 + 7 + 5 + 7 + 13 + 11 + 13 + 7`
  (215), with a comment history of five packages each editing it (206-214); a commented line in
  `data/ports/lisbon.yaml` (228), a test of a comment in a data file. Low.
- `test_the_hoy_goes_back_when_she_is_gone_from_the_road_...` (397-427) and `test_a_hoy_of_shot_
  alone_goes_back_with_the_shot` (787-822) inject a Plymouth job, at stage "stowed", into a ship
  lying at Falmouth, and assert the line "She weighed before the powder was struck down". She has
  not weighed. The code's "weighed" branch is reached by any ship not in the job's port at that
  stage; the test pins a sentence false of its own scenario. The real weighing is tested properly
  at 430. Low, sure of the test.
- No `xfail`, `skip`, `try/except`, or empty loop.

### (c)

- conftest.py:473-475 names truths 7-167 ("the King's cutter completes her magazine from the
  Ordnance free") and 7-168 ("powder is taken in at the road not the harbour"), which by their
  names are this file's 296 and 381 again. I did not open test_known_truths.py to see whether they
  call these functions.
- `world_at`, `at_anchor_in`: see section 6.
- The four refusal tests (507, 530, 546, 568) are one table of (world, order, words); the file
  says so of itself ("every refusal of the demand in its order and words", 4).

### Anything else

- Good: `test_the_kings_cutter_completes_her_magazine_...` checks the purse untouched and no random
  stream drawn through the whole issue (305-306, 376-377): a determinism guard most tests omit.
- Good: `test_a_port_pickled_before_the_block_reads_it_once_from_its_file` (256) covers a real
  migration hazard (a checkpoint from an older checkout) with real pickles.

---

## 8. tests/test_parity.py (390 lines)

### Count and kind

6 test functions, none parametrised. One module fixture, `seated_world` (175-189): the gate 5b
passage scenario with a fake captain seated and 1,200 s sailed; shared by four tests and mutated
by them in turn (orders submitted, 206, 242-243, 286). `test_truth_91_...` (355) builds two more
worlds and sails each about two hours (slow by conftest.py:447).

Proves: that the captain's station and the console read and order through the same functions, and
(truth 91) that a fake captain and the console giving the same ten orders at the same ticks make
the same log.

### (a)

Nothing dead found.

### (b)

- The enumeration tests prove that a reason is written, not that a road works.
  `CONSOLE_COMMANDS` (63-100), `SNAPSHOT_BLOCKS` (104-138) and `TOOL_COUNTERPARTS` (142-168) map
  each command, block and tool to a sentence; `test_every_console_command_has_its_road_...` (264)
  and `test_the_snapshot_and_the_tools_...` (289) pass as soon as a key with any sentence is added.
  Only backticked ids in `SNAPSHOT_BLOCKS` are checked to exist (296-303); of the commands' roads,
  four are exercised (`muster`, `state`, `the sail room`, `the booms`, 272-283). Of the 25 roads
  marked "by design" (15 commands, 10 tools), none is checked. Medium, sure.
- `_console_commands` (246-261): a command not in `CONSOLE_COMMANDS` is added (to make the test
  fail) only when it is the first of a comma-separated line (`elif i == 0`, 259); a new alias
  written after a comma is dropped silently. Low, sure.
- 222: `set(tool["sails"])` non-empty and all values strings: passes for any sail line.
- 390: `>= len(SAME_ORDERS) - 1` lines by the captain; loose, but 389 is the real check.

### (c)

Nothing to merge; `_the_passage` and `seated_world` build the same scenario two ways for good
reason (the fixture seats a captain, the truth test does not share state).

### Anything else

- Good: `test_truth_91_a_fake_captain_and_the_console_give_the_same_orders_to_the_same_log` (355)
  is the strongest test in this list: two games, line for line, order lines compared by kind and
  everything else by words (340-352), with a check that the fake did give its orders on time (378).
- The shared module world means an order accepted by one test changes what the next reads; today
  every order submitted is refused or a query, so it holds. Low.

---

## 9. tests/test_people.py (971 lines)

### Count and kind

27 test functions, none parametrised. No fixtures; a frigate world per test (`world_for`), and
`_world_with_a_crewed_brig` (811, from test_crews) built in three tests (825, 874, 952), one of
which (825) sails up to 400 minutes waiting for her demotion (862-866).

Proves: the named few drawn from the muster by post, their places and states, `send for` by the
messenger, a task that occupies a person, the watch bill's sleepers, messages to the cabin door,
people made from words, the needs (hunger, thirst, sleep) told only to the person, things and free
lines, one registry of persons across hulls and hearing by spot.

### (a)

Nothing dead found. The comments at 669-673, 701-702, 710-713 record package 109's change in place
of the old expectation and the assertions follow the new code.

### (b)

- `test_send_for_brings_a_man_to_where_the_captain_is_by_the_messenger` 123-125, 135, 201: the
  wait is `PE.PASS_THE_WORD_S`, read from the code (freesail/world/people.py:94, 60). Whatever the
  constant, the test passes; a grep of tests/ finds no test that pins 60 (test_known_truths.py:3692
  and test_letters.py compare with the constant too). Medium, sure.
- `test_the_people_and_where_is_...` 96: `e.text.endswith(", carpenter, on the deck.") is False`,
  then 98 pins the whole text: the first is a negative check that adds nothing. Low.
- 149 `"already" in e.text`; 709 `.kind != "free.line"`. Low.
- `test_a_word_ashore_is_heard_by_whoever_is_at_that_place_...` 899-904 writes the brig's mate
  ashore by hand ("as the boat would write them", 881): hearing is tested on a state no act of the
  game made. Documented; low.
- No `xfail`, `skip`, `try/except`, or empty loop; the demotion loop (863-866) is followed by an
  assertion that it happened (867).

### (c)

- Helpers imported from other test files: `tests.test_brains.put` (341), `tests.test_orders_places.
  seat` (723), `tests.test_director.directed` (798), `tests.test_crews.hove_to_world, put` (814).
  A change to a helper in one file breaks tests in another; they belong in a shared module.
- The five needs tests at the prompt (433, 455, 468, 498, 515) share `_at_the_prompt`, which is
  right; nothing to merge.

### Anything else

- Good: `test_the_people_are_a_function_of_the_seed_...` (238) checks two worlds by digest, a
  checkpoint's people, and the run after the checkpoint by digest.
- Good: `test_the_persons_of_every_hull_are_one_registry_...` (825) follows the registry through
  the brig's demotion to her removal.

---

## A note on tests/conftest.py (read for the tiers)

- conftest.py:6 says the `slow` mark is "applied here and never in a test file"; test_observer.py
  applies it (see section 2).
- conftest.py:318 and 415 are dead node ids (section 5); a parse of every id that names a file of
  this list found no other.
- conftest.py:715: `items[:] = [i for i in items if i not in set(others)]` builds the set afresh
  for every item, quadratic in the suite's size when sharding. Low, sure.

---

## Faults to plant

Under (b), each in a scratch copy:

1. **test_officer.py::test_the_handover_is_asked_for_at_a_reserve_in_tokens_and_of_an_officer_off_watch**
   and **::test_the_handover_note_is_asked_for_at_the_budgets_fraction_and_folds_the_conversation**.
   Fault: in `freesail/agents/harness.py` delete lines 3969-3970 (`if size < threshold:` /
   `return`), so the note is asked for at every turn's end whatever the size. The names say the ask
   comes at the reserve and at the fraction. Prediction: both pass although the threshold is gone
   (3668 waits for the first ask, which comes at once at 16,384 anyway; 902's precondition at 946
   still holds and its loop ends at the first ask).
2. **test_orders.py::test_table[frigate: veer cable]** and **[frigate: veer to ninety fathoms]**.
   Fault: in `freesail/orders/ground_tackle.py` line 72 change `"veer cable": "veer_cable"` to
   `"veer cable": "heave_in"`. The rows say veering starts. Prediction: both pass (the rows check
   only the kind; `FakeRunner` records any start). Other files may catch it; none of mine does.
3. **test_orders_m4a.py::test_trim_the_sail_and_tend_the_sheets[tend the sheets]** (and `[trim the
   headsails]`, `[tend sheets]`, `[trim the sheets]`). Fault: in `freesail/orders/verbs.py` line
   1318 change `"trimmed_sheets": trimmed,` to `"trimmed_sheets": list(reversed(trimmed)),`. The
   test says it checks the sheets trimmed. Prediction: passes (the `or len(...)` at 142-144); the
   one-sheet schooner test at 185 is not touched by a reversal.
4. **test_ordnance.py::test_the_kings_cutter_completes_her_magazine_of_the_ordnance_free_in_the_sound**
   (and the 16 other tests on the fake). Fault: in `freesail/ship/parts.py` delete line 1000
   (`established += float(self.reserve_lb)`), so the real magazine never wants its barrels below
   made up. The name says she completes her magazine. Prediction: passes (the test uses
   `FakeMagazine.wanting`); `test_the_real_magazine_...` (825) passes too, its demand being carried
   by the ten round shot and its last check by powder set to the reserve by hand.
5. **test_people.py::test_send_for_brings_a_man_to_where_the_captain_is_by_the_messenger**.
   Fault: in `freesail/world/people.py` line 94 change `PASS_THE_WORD_S = 60` to
   `PASS_THE_WORD_S = 3600`. The test says the man comes by the messenger. Prediction: passes (it
   waits the constant, whatever it is).
6. **test_orders.py::test_take_a_fix_is_completed_from_the_marks_in_sight**. Fault: make
   `freesail/orders/complete.py`'s fix offers name the marks in reverse of `_fix_marks` order beyond
   the first two, or offer a third mark that is the first again (`... and A and B and A`). The name
   says the completions are from the marks in sight and usable. Prediction for the second form:
   passes (2375 accepts `order.rejected`). A suspicion: I did not read complete.py to give the line.

Faults a player would meet that I believe no test in these nine files catches:

- A. `PASS_THE_WORD_S = 3600` (freesail/world/people.py:94): every man sent for takes an hour to
  come aft. No test in the suite pins 60, by grep.
- B. The real `Magazine.wanting` without the reserve (parts.py:1000): a ship takes in powder for
  her cartridges and never for her barrels below. Only `test_the_real_magazine_...` uses the real
  `wanting`, and its checks miss it (fault 4).
- C. Not planted but present: an officer seated through the local runner at the 16,384 context the
  runner itself advises (freesail/agents/local.py:604-606) is asked for his handover note at his
  first sample and again at every tenth of growth (section 3). No test fails for it; the one test
  at that budget (3668) waits for exactly that ask and passes.

Not read: test_known_truths.py, test_trim_order.py, test_catalogue.py, test_crews.py,
test_brains.py, test_director.py, test_letters.py (named above only from grep or from conftest);
`freesail/orders/complete.py` (fault 6 is given without its line). No test was run.

