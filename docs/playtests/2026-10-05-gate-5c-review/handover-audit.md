# The audit of the build m5c-c

Written 2026-10-08 by a Claude Opus 5.5 session in Claude Code that had seen none of this
work, as the auditor's part of the handover. It is an account of what
`FreeSail-gate-m5c-c` holds today, set against the gate folder `FreeSail-gate-m5c`, and
checked in the code and the tests. The changes file (`CHANGES-m5c-c.md`), the four briefs
(`docs/dev/M5-WorkPackages.md`) and the review (`report.md` in this folder, its section 11
included) were read as claims to be checked, not as findings.

**What was done to make it.**

- Every file in the gate folder, in m5c-b, in the lead's four snapshots and in the build
  was hashed and the seven set side by side. The gate folder was also compared with the
  gate's zip, read without extracting it.
- The whole suite was run once, on four workers, and the linter once (Part 2, 2.5).
- The naval cruise was sailed under its own book, and four trials of what might bring its
  lost meeting back were made in memory.
- A few dozen orders were given to ships made in memory, to see what the build answers.
- The consent brief, the records and the stations' briefs were read by the game's own
  functions. The owner's four saves in this folder were loaded, with no tick run, and the
  last of them was replayed in memory.
- The code was read where a row of the ledger needed it.

Every script and its output is in my scratch folder, `handover-audit\` under the session's
scratchpad. Nothing was written in either folder but this file: a listing of every file's
size and time in both, taken before the suite and after it, is the same. No git command
was run. No model was seated, no consent question answered, no server started, and no
tool of the game's bridge called.

**How to read the marks** in the tables.

| Mark | Means |
|---|---|
| **P** | I ran it myself: a probe, a passage sailed, or the files read by the game's own functions |
| **T** | A test of that name is in the tree, its name says what the row says, and it passed in my run of the whole suite. I read the bodies of only a handful, marked "body read"; for the rest this is weaker evidence than a reading |
| **R** | I read the code or the document at the place named |
| **D** | From comparing the folders and the snapshots |
| "not checked" | I did not look. Where a row rests on the changes file or the review alone it says so |

## The short version

1. **The suite and the linter are as claimed.** `2981 passed, 9 xfailed in 1179.13s
   (0:19:39)`, and `All checks passed!`.
2. **The four packages are in the build as the changes file lists them, file for file**, and
   m5c-b came in byte for byte. I found no numbered item of the four briefs left unbuilt (the reports each
   brief asks for went to the lead and are not in the tree). Three of
   37e's are met only in part and the changes file says so (the fix's doubt when its marks
   lie on one hand; two beats of the recorded passages lost; three of four measured figures
   not reached).
3. **The naval cruise does not come through, and the reason on record is partly wrong.** The
   scenario puts the French brig at a fixed place that the frigate, since 37e, has already
   sailed past: the brig appears on her quarter, up wind and going away. The chase order
   then keeps the frigate on the tack that leads from the chase, and half an hour later
   turns her 175 degrees by the stern with her yards unbraced, which takes her aback. The
   record says she is taken through the wind, and that mending the chase order would bring
   the meeting back. On my trials it does not; moving the brig's place does, with no change
   to the code. The same handling fault takes her aback once more, earlier in the same
   passage, and nobody has noted it (Part 2, 2.4).
4. **The gate's document describes the gate as cut.** Its suite lines, both passages' times
   and words, and four of its items no longer match the build. Nine tests are expected
   failures: the owner's seven and two beats lost this week (Part 2).
5. **What the review recommended and the build does not hold**: the pilot (37h, not
   written); `the port` and `the depth of water` by the captain's means (kept for last, by
   the plan); every fault of the browser client; the boats; one reader for numbers; a tack
   that could not begin; a handful of words; and everything section 11 proposes after game
   10. Nothing in the code or the data has changed since game 10 was played.
6. **At the merge** (Part 3, 3.7 to 3.9): `.gitignore` will leave the kept saves out of a
   commit without a word; the build's own name is spelt in nine test lines; one consent
   record made in play is only in m5c-b; a test pins the bytes of a fixture file; and the
   consent brief must arrive unchanged.
7. **The gate folder is not the gate as cut.** It is the zip, unchanged, with the owner's
   saves, his notes, four scenario files, eight consent records and the review folder
   added. The review folder there was the same as the one here when I compared them,
   before this file and `report-2.md` were added here.
8. **Advice**: take all four packages, since none can be held without those after it, with
   the changes named in Part 4, 4.2, and seven things for the owner to decide first (4.3).

## Part 1. The ledger

One row for every recommendation of the review's sections 8, 10.6 and 11.6, every ruling
of its section 9, every numbered item of the four briefs, and every "left undone" in the
changes file. The rows are grouped by where they come from, in that order. Test names are
given without the leading `test_`; all are in `tests/` and all passed in my run.

### 1.1 The review, 8.1: three things to settle first

| Item | State | What I looked at |
|---|---|---|
| The replay of a saved game with a model in it: stamp every save, have `load` say which road it took, treat such saves as good from their checkpoints | **Built** (37d), as the owner ruled on 7 October | R: `core/world.py::build_stamp`, `core/replay.py::check_replay`, `load_report`. T: `another_builds_game_with_a_station_aboard_is_not_replayed_unless_asked`. P: the owner's four saves here load from their checkpoints |
| ... and a replay driven by the transcript | **Not built**; left for milestone 6 by the review's own advice and decision 36 | R: decision 36 |
| One revision of the consent brief, then one re-ask | **Built** (37g and its second pass, both before any model was asked) | D: `ConsentBrief.md` changed at m5c-b, 37g and the second pass and at no other stage. P: digest `288d0b18e34d76a8`; the one record made since is against it |
| One re-measuring of the recorded passages | **Overtaken** by the plan as ruled on 7 October (10.6): they were measured again three times, by 37d, 37e and 37f | R: the comments on `GATE_5C_*` in `tests/test_known_truths.py` |

### 1.2 The review, 8.2: build now. Near land

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A distance judged afresh when it has changed by a tenth | **Built** (37d) | R: `lookout.py`, `ESTIMATE_REFRESH_FRACTION = 0.1`; `ESTIMATE_HOLD_NM` is gone. T: `the_lookout_judges_a_distance_afresh_as_she_stands_in_from_a_league_to_two_cables`, `an_hour_of_calm_leaves_the_figure_as_it_was` |
| 2 | A single bearing gives a line; the distance by estimation not applied as a measurement | **Built** (37d), then changed twice: laid down when it is the better figure (37d's second pass), and weighed by the one rule (37e) | T: `a_landfall_on_one_mark_lays_the_account_down_by_the_bearing_and_its_distance`, `six_bearings_of_one_mark_lay_the_distance_down_once_and_the_account_does_not_creep` |
| 3 | `take a fix`, open to the officer | **Built** (37d); since 37e it is weighed and takes the near marks; the officer's own since 37g | T: `a_fix_by_two_marks_at_right_angles_brings_the_account_to_the_truth`, `a_fix_by_three_marks_says_the_cocked_hat_...`, `bearings_and_fixes_are_the_officers_own_and_a_sight_is_the_masters`. P: `every glass then take a fix` is entered in the book |
| 4 | No fix from a bearing of a sail | **Built** (37d) | T: `a_bearing_of_a_sail_moves_nothing` |
| 5 | The shore always a sighting; `the nearest land` a reading, in every sample | **Built** (37d). Whether every sample carries it: not checked | R: `chart.py::nearest_shore`. T: `the_shore_is_a_sighting_at_every_look_within_its_limits_and_hailed_once`, `the_nearest_land_is_a_reading_in_the_lookouts_words_and_never_the_charts_metres`. P: "The nearest land: the land about Trefusis Point, on the larboard quarter, bearing SE by E, a cable" |
| 6 | Land ahead: notable under ten minutes, urgent under four | **Built** (37d) | R: `lookout.py`, `LAND_AHEAD_NOTABLE_MIN = 10`, `LAND_AHEAD_URGENT_MIN = 4`. T: `land_ahead_is_notable_under_ten_minutes_and_urgent_under_four_each_once` |
| 7 | The sea breeze's direction from the coast's trend | **Built** (37d) | R: `weather.py`, `SEA_BREEZE_TREND_KM = 3.0`. T: `the_breeze_blows_toward_the_coasts_trend_and_is_scaled_by_its_steepness`, `from_the_harpys_own_weather_the_wind_no_longer_turns_as_the_ship_moves` |
| 8 | The anchor's place taken from the ship's own position | **Built** (37d) | R: `core/world.py::place_of_plane`. T: `an_anchor_let_go_after_a_run_of_sixty_miles_lies_in_the_depth_the_lead_found` |
| 9 | A sight blended unless it is the better figure, and the line says what the master did | **Built** (37e) | T: `the_lunar_of_game_9_moves_the_account_under_two_cables`, `the_words_of_a_cast_a_noon_and_a_bearing_say_which_of_the_three` |
| 10 | The pilot's boat closes with the ship, and keeps closing | **Not built.** It is 37h's, which is not written | T: `the_schooners_pilot_boards_before_she_runs_in` is an expected failure for want of it |
| 11 | The account at anchor, hove to and after a manoeuvre | **Built** (37e) | T: `hove_to_the_master_reckons_her_drift_and_the_run_since_noon_takes_it`, `after_she_fills_away_her_way_is_judged_by_eye_until_the_log_is_next_hove`, `the_doubt_grows_by_the_hour_hove_to_and_becalmed_and_not_at_anchor` |
| 12 | Bearings, the deep-sea lead and `heave the log` in the officer's domain | **Built** (37g for bearings and fixes; the lead and the log were there) | R: `agents/agent.py::OFFICER_DOMAIN` |
| 13 | "Dragging" urgent; a pilot's hail notable | **Built** (37d) | T: `a_dragging_anchor_is_an_urgent_line_and_holding_again_a_routine_one`, `the_pilots_hails_are_notable_lines` |
| 14 | `the port` and `the depth of water` by the captain's means | **Not built**, on purpose: the plan keeps it for last | R: `api/readings.py::_depth_of_water` ("by the chart at the ship's position"). P: both readings answer from her true place |

### 1.3 The review, 8.2: the station and the doors

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A key to each seating; a second door refused; a line when the door changes | **Built** (37g) | R: `agents/remote.py::_seat`, `held_words`. T (body read): `a_call_without_the_seatings_key_is_refused_in_words_and_nothing_is_run`; `a_call_whose_key_is_refused_stops_the_bridge_and_it_does_not_take_the_seat_back` |
| 2 | The turn budget: the ways out always run; reads apart; said and logged; sixteen | **Built** (37g): sixteen orders, thirty-two reads | R: `harness.py`, `ALWAYS_RUN_TOOLS`. T: `the_ways_out_and_the_stand_by_always_run_whatever_came_before`, `the_officers_orders_are_sixteen_a_turn_and_the_reads_are_counted_apart` |
| 3 | A captain's word in an open turn breaks the stand-by that follows | **Built** (37g) | T: `the_captains_word_in_an_open_turn_breaks_the_stand_by_that_closes_it` |
| 4 | A stand-by with the deck broken by danger, told when its event cannot come, with a bound | **Built** (37g) | T: `a_stand_by_with_the_deck_is_broken_by_danger_refused_what_cannot_end_and_bound` |
| 5 | A paused or silent station gives the deck back; urgent; the clock eases | **Built** (37g) | T: `a_paused_or_silent_officer_does_not_keep_the_deck_and_resume_gives_it_back` |
| 6 | The silence detector counts calls inside an open turn | **Built** (37g) | T: `the_silence_detector_hears_a_call_made_inside_an_open_turn` |
| 7 | The contrary detector: a stand-by clears the chain; the nudge with the order's result; drift counted only within two glasses | **Built** for the first two; the third **overtaken** by item 8: drift is never counted | T: `a_stand_by_that_answers_the_nudge_clears_the_chain_and_no_pause_comes_unread` |
| 8 | ... a link only when the later order undoes the earlier, from a table kept as data | **Built** (37g) | R: `data/vocabulary.yaml`, `undoes:`. T: `what_undoes_what_is_a_table_of_the_vocabulary_and_the_books_rule_is_unchanged`, `the_42_recorded_chains_are_silent_by_the_new_rule_and_set_take_in_set_still_speaks` |
| 9 | The journal read by a tool; the last note and the journal's size in every brief; `read_log` past 200 lines | **Built** (37g). `read_log`'s reach: not checked | T: `the_journal_is_read_back_by_its_writer_newest_first_by_count_tick_and_kind`; body read: `a_released_station_is_taken_by_another_model_with_its_own_consent` (the relief's brief carries the note) |
| 10 | The bridge asks for its station again on a 404; its wait adapts | **Built** (37g) | T: `the_bridge_asks_for_its_station_again_when_the_game_has_none`, `the_bridges_wait_adapts_when_the_client_cuts_a_waiting_call_short` |
| 11 | A sample's lines carry their actor; the captain's orders listed | **Built** (37g) | T: `a_sample_says_who_gave_each_order_and_lists_the_captains_and_the_work_in_hand` |
| 12 | A watcher can stand down with a save | **Built** (37g): `stand_down` for any station | T: `the_three_ways_of_leaving_cannot_be_taken_for_one_another`, `a_stand_down_is_taken_out_of_turn_and_while_paused_and_replays` |
| 13 | An allowance says what it granted; a prefix that allows nothing is refused | **Built** (37g) | T: `a_named_grant_means_what_it_says_and_several_of_one_order_stand_together` |
| 14 | The handover threshold as a reserve in tokens, with a flag; no officer without a context size; the guard on the officer's brief | **Built** as asked, and by the review's own section 11 the first part was wrong advice: it ended both seatings of game 10 | R: `harness.py::handover_threshold`, `HANDOVER_RESERVE_TOKENS = 14000`. T: `the_handover_reserve_is_a_flag_sent_with_the_station_request`, `no_officer_is_seated_without_a_context_size_and_the_guard_measures_his_own_brief` |
| 15 | The mending of 37b's opt-out path | **Built** (37g, item 13) | T: `final_is_read_from_the_tools_own_setting_and_from_nothing_else`, `opt_out_final_is_not_seated_again_and_replays`, `the_agent_api_seats_a_released_station_again_and_holds_an_opt_out_to_its_word` |

### 1.4 The review, 8.2: the log

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | "Aback": a flag for each severity, armed again by state; the per-sail lines once an episode, none for sails backed by order | **Built** (37f) | T: `in_a_calm_her_sails_aback_is_said_once_however_long_it_lasts`, `a_sail_taken_aback_is_said_once_an_episode`, `a_sail_laid_aback_by_order_says_nothing`, `the_urgent_line_has_its_own_flag_and_is_said_though_a_calms_line_stands` |
| 2 | Wind shift: no line in light airs or an unsteady wind; "light and variable" once; the event's floor | **Built** (37f) | T: `the_floor_is_a_light_breeze_by_the_logs_own_scale`, `the_wind_falling_light_is_said_once_and_the_next_settled_wind_once`, `the_event_a_wind_shift_keeps_the_same_floor` |
| 3 | A standing order with nothing to do: one routine line a watch | **Built** (37f) for a condition that does not hold. An action the ship refuses is another matter (the review counts 33 such refusals in game 10; not checked) | T: `a_standing_order_with_nothing_to_do_says_so_once_a_watch_for_each_reason`. P: in the cruise's log "keep her bearing ... not carried out" comes once a watch |
| 4 | A no-bottom cast routine; "a sounding" means bottom found | **Built** (37f) | T: `a_cast_that_finds_no_bottom_is_routine_and_a_sounding_is_bottom_found` |
| 5 | What the officer says with the deck is notable | **Built** (37g), with the deck or without | T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |

### 1.5 The review, 8.2: small faults

| Item | State | What I looked at |
|---|---|---|
| Client: `FATHOM` defined; the track's hourly points; bearing lines faded; the captain's markers named; the anchor in the snapshot | **Not built.** Nothing under `client/` has changed | D. R: `client/map.js` line 450 uses `U.FATHOM`, and no file under `client/` defines it |
| Boats: one state machine; a refused order not moving the person; the refusal saying the two-mile rule | **Not built**; put off by 37f's brief | D: no file of the boats changed. Not probed |
| Numbers: one reader for numbers in words | **Not built**; put off by 37f's brief | Not checked beyond the brief |
| Sails: `take in`, `furl`, `lower`, `clew up` reach the water sail and the jibs | **Could not tell.** No package claims it and I found no change for it; not probed | D: `orders/verbs.py` changed in 37f only |
| Hove to: the flag cleared by anchoring, weighing and tacking | **Built** (37f) | T: `the_record_is_cleared_when_an_anchor_is_let_go_and_when_she_takes_the_ground`, `the_record_is_cleared_by_a_tack_and_by_a_wear`, `lain_a_try_anchored_and_weighed_she_takes_a_course_at_the_first_order` |
| ... the starter book's trim rule guarded; `trim sails` declining hove to | **Built** (37f) | R: `data/standing_orders/starter.orders` lines 77 and 88. T: `every_shipped_trim_rule_carries_the_dialects_own_guard`, `trim_sails_is_declined_while_she_is_hove_to_in_words_that_carry_the_cure` |
| ... a hove-to ship that fills and gathers way says so, urgently | **Built** (37f) | T: `forced_round_by_a_shift_one_urgent_line_says_so_and_the_record_follows_her`, `a_brig_under_her_topsails_alone_that_falls_off_is_said_to_be_hove_to_no_longer` |
| Getting under way: the fore-and-aft cast; never "paid off" on a timeout | **Built** (37f) | T: `a_fore_and_after_casts_on_the_tack_ordered`, `paid_off_is_never_said_on_a_timeout` |
| Tacking: a tack that could not begin says why, not in the words of a missed stay | **Not built**; put off by 37f's brief | P: in my trial a tack ordered from off the wind was answered "Squared the yards; she fell off on the starboard tack, to try again or to wear" |
| The anchor: `heave in 70 fathoms`; `come to an anchor in twelve fathoms`; "Brought up" after `let go`; warnings for scope and draught | **Built** (37f) | P: `heave in 10 fathoms` taken; "Brought up by the best bower in 17 fathoms". T: `come_to_an_anchor_in_twelve_fathoms_stands_on_till_the_lead_calls_it`, `the_water_at_low_water_is_set_against_her_draught_as_the_anchor_goes` |
| At anchor and aground: the 26 refused verbs gone through; `furl all sail` at least | **Built** (37f). I did not count the verbs | P: at anchor `square the yards` is taken and `steer N` is refused. T: `a_ship_at_anchor_may_hand_her_sails_and_square_her_yards`, `a_ship_aground_may_do_the_same_and_no_manoeuvre` |
| The filter: `take in twenty tons of water` must not pass as the port's order | **Not built** | P: it is answered "She is not in port; there is no yard to demand it of" |
| Papers: her draught; `the prices` showing every list; port names without regard to case | **Not built** as far as I found; not probed | D: no change in the papers' or the ports' code but one severity |
| The carpenter reports the well | **Not built** as far as I found; not probed | D |
| Replay: an officer seated at tick 0 replays in his place | **Built** (37d) | R: `harness.py`, `stationed_after_inputs`. T: `an_officer_seated_at_tick_0_after_a_drivers_line_replays_in_his_place` |
| Words: 1805, not 1806, in the brief and primer 16 | **Not built** | P: the officer's brief as sent still says "as a lieutenant of 1806" |
| Words: "the breakwater" out of the Plymouth pilot's mouth | **Not built** | R: `data/ports/plymouth.yaml` line 52 |
| Words: the gate's "£6,000" | **Not built** | R: `docs/gates/gate-m5c.md`, item 1 |
| Words: hints that do not send `hail` to `haul` | **Not built** | P: `hail the pilot` is answered "did you mean 'haul'?" |

### 1.6 The review, 8.3: build after a ruling

| # | The matter | State | What I looked at |
|---|---|---|---|
| 1 | A general grant | **Built** (37g), on the rulings of 5 and 7 October. It keeps back more than the list on record (Part 4, C6) | R: `agent.py::_GENERAL`, `_KEPT_BACK`. T: `the_general_grant_opens_the_ships_working_and_keeps_back_what_it_keeps` |
| 2 | The emergency route | **Built** (37g, item 19), kept by the owner on 7 October | R: `agent.py::_DANGER`. T: `the_way_out_of_danger_is_the_officers_own_word_for_the_helm_a_heave_to_and_an_anchor` |
| 3 | Whether `say` ends a turn | **Not ruled, not built** | R: 37g's brief, "Not in 37g" |
| 4 | The pilot taken or declined; what he does aboard | **Ruled** (5 and 7 October); **not built**: 37h is not written | P: `hail the pilot` and `decline the pilot` are not orders; `take the pilot` is read as the reading `the pilot` |
| 5 | The master's own fixes in pilot waters | **Overtaken** by the ruling of 5 October: `take a fix` is an order, not a routine | section 9, answer 7 |
| 6 | Relief by another model | **Ruled**; **built** (37g) | T (body read): `a_released_station_is_taken_by_another_model_with_its_own_consent` |
| 7 | What a ship knows of another port's trade | **Not ruled, not built** | no brief holds it |
| 8 | The boat's errands | **Not ruled, not built** | no brief holds it |
| 9 | The well and the pumps | **Not ruled, not built** | no brief holds it |
| 10 | A late reply | **Not ruled, not built** | R: 37g's brief, "Not in 37g" |
| 11 | Who may ask a station back after a welfare stand-down | **Could not tell** whether it was ruled apart from relief. The build has one rule for every released station | R: `harness.py::seating` |

### 1.7 The review, 8.4: needs design work first

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A replay driven by the transcript | **Not built**; milestone 6 | decision 36 |
| 2 | The con | **Not built** as a thing apart. Taking the deck now leaves the officer seated, which the review offers as the captain's way to take the con | T: `you_have_the_deck_gives_it_and_i_have_the_deck_takes_it_and_no_more` |
| 3 | Stand by until x, or y, or z, with the dialect's conditions | **Not built** | no brief holds it; not probed |
| 4 | Features by their parts, and how marks stand to one another | **Not built** | 37d's brief, "Not in 37d" |
| 5 | The pilot as a voice | **Overtaken**: ruled later work, with the director (section 9, answer 6) | |
| 6 | What a sample carries | **Not built.** The review's section 11 says the samples have grown | not checked |
| 7 | Image tools | **Not built** | |
| 8 | The drill for a station with authority | **Not built**; "design first" in 37g's brief | the review says the drill miscounted in game 10; not checked |

### 1.8 The review, 8.5 to 8.8

| Item | State | What I looked at |
|---|---|---|
| 8.5, 1: no rule that shrinks the doubt because land is near | **Followed**, as far as I read: the doubt is moved by the run, the streams and observations | R: the constants and comments at the head of `world/reckoning.py`; not read through |
| 8.5, 3: the anchor inside a general grant | **Followed** | R: `agent.py::_GENERAL` holds `object:anchor` |
| 8.5, 4: no `keep` prefix; mend `trim` and ship `at steady on the course then trim sails` in the starter book | No `keep` prefix was built. `trim` hove to is mended (37f). The starter book has **no** `at steady on the course` rule | R: `data/standing_orders/starter.orders` |
| 8.5, 5: mend the sea breeze, not a minimum wind | **Both were done**: the sea breeze (37d) and a floor of four knots on the line (37f) | 1.2 item 7; 1.4 item 2 |
| 8.5, 6: the journal stays in the context; give the station its journal to read | **Followed** (37g) | 1.3 item 9 |
| 8.5, 7: the budget's counting before its size | **Both were done** (37g) | 1.3 item 2 |
| 8.5, 8: bind a door to its station before several stations through one door | **Followed** (37g) | 1.3 item 1 |
| 8.5, 9: no image tools now | **Followed** | |
| 8.5, 11: "taken aback" is not only noise | **Followed**: the urgent line keeps its own flag (37f) | 1.4 item 1 |
| 8.5, 2 and 10, and the points on the model's additions and on m5c-b | Judgements, not things to build | |
| 8.6: nothing of a later milestone pulled forward | **Followed**, as far as the briefs and the diff show | D |
| 8.7, 1: the officer's domain: bearings, the deep-sea lead and the log; a course change judged by its effect; the danger exception | **Built** (37g) | T: `an_order_that_changes_her_course_is_the_course_whatever_its_words`; 1.6 item 2 |
| ... `fill away` after a heave-to he did not order; heaving in with weighing and veering | **Not built** as the officer's own: both want the captain's word, by name or by the general authority | R: `agent.py::OFFICER_DOMAIN.refused` |
| 8.7, 2: no officer seated when the server reports no context size | **Built** (37g) | 1.3 item 14 |
| 8.7, 3: a far-detail vessel's leg across the coast refused at loading | **Not ruled, not built** | Part 2, item 14 |
| 8.7, 4: batch the brief's changes; a larger drill | The first **built**; the second **not built** | 1.1; 1.7 item 8 |
| 8.8, steps 1 and 2: the saves; near land, the sea breeze, the anchor's place, the schooner's cast | **Built** (37d; the cast in 37f) | above |
| 8.8, steps 3 and 4: the station's safety; the brief's one revision | **Built** (37g) | above |
| 8.8, step 5: the log's noise and the small faults | The noise **built** (37f); the small faults **partly**: see 1.5 | |
| 8.8, step 6: play what the gate still lacks | **Not done**, by the review's own account | cannot be checked from the tree |
### 1.9 The review, section 9: the owner's answers and rulings

| Ruling | State | What I looked at |
|---|---|---|
| 1. Replay: "save is exact from the checkpoint, replay is promised only on the build that made it" (7 October) | **Built** (37d). The promise itself is not quite kept for game 10's last save, which replays one line short on its own build (Part 4, C7) | 1.1. P: `saves_check.py` |
| ... stamp every save and checkpoint with its build | **Built** | P: the saves of games 9 and 10 carry `m5c-c/37d` and `m5c-c/37g` with their fingerprints |
| ... `load` refuses to replay another build's game with a model aboard unless told to | **Built** | T: `the_cutters_save_is_refused_a_replay_without_the_flag`, `every_door_that_loads_or_replays_says_the_same_words_and_takes_the_flag` |
| ... two or three of the playtest's checkpoints kept as tests | **Built** in this folder; at risk at the merge (Part 3, 3.9) | T: `a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_glass` (two saves), `the_packages_own_save_loads_from_its_checkpoint_and_runs_on_a_glass` |
| 2. The gate's verdict waits on the naval cruise and the lead's watch | **Stands.** Neither has been done, by the review's account, and the cruise does not come through (Part 2) | P |
| 3. A save lies in the folder of the build that played it | **Followed** | D: the saves of m5c and m5c-b were not brought over; this folder's eight are games 9 and 10 |
| 4. The grant: what stays out, and when it lapses (5 and 7 October) | **Built** (37g), with more kept back than the list on record | 1.6 item 1; Part 4, C6. T for its life: `the_general_grant_opens_the_ships_working_and_keeps_back_what_it_keeps` |
| 5. The deck: `you have the deck` and `I have the deck` do not unseat the officer | **Built** (37g) | T: `the_deck_is_taken_and_given_three_times_with_the_station_seated_throughout` |
| ... the officer's own `hand_over` gives the deck back and he stays | **Built** | T: `hand_over_gives_the_deck_back_with_the_note_and_the_officer_stays` |
| ... a `stand_down` tool for any station | **Built** | 1.3 item 12 |
| ... the readings say "off watch"; what he says is notable with the deck or without | **Built** | T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |
| 6. The pilot: taken or declined by an order; aboard he warns; unanswered he keeps company, hails once more and bears away (5 and 7 October) | **Not built.** 37h is not written | 1.6 item 4 |
| 7. `take a fix` is an order, not a routine | **Built** (37d) | 1.2 item 3 |
| 8. Relief: a station stood down may be taken by the same model or another | **Built** (37g) | 1.6 item 6. T: `a_station_left_in_a_playtest_save_is_taken_again_by_the_one_rule` |
| ... a final opt-out bars the model, not the station; the relief may read the journal (7 October) | **Built** | T: `opt_out_final_is_not_seated_again_and_replays`, `the_journal_is_read_back_by_its_writer_newest_first_by_count_tick_and_kind` |
| 9. The consent record of 3 October stands; every identity is asked again at the one revision | The re-ask is **built**. The record itself is not in this folder (Part 3, 3.7). Opus 5.5 was in fact asked again on 6 October, for game 9, because this folder did not hold that record, as the changes file said it would be | P: `consent_check.py`; the record of 6 October names the brief `f667a04e00b32e1f` |
| 10. The watcher's `opt_out` on the *Harpy* was not a withdrawal | **Recorded** in the review and in `Harness.md`; a save from before 37b reads such a leaving as a stand-down | R: `docs/agents/Harness.md` line 276; `harness.py::_leavings` |
| The way out of danger, kept as proposed (7 October) | **Built** (37g) | 1.6 item 2 |
| The approvals of 7 October: 37e, 37f, 37g | **All three built** | Part 3 |
| The work done locally, with no commits | **Followed**, as far as a folder can show: the build folder is not a repository | I ran no git command |

### 1.10 The review, 10.6: what game 9 changed in the plan

| Item | State | What I looked at |
|---|---|---|
| The rule, 1: an observation is weighed against the account by their two doubts | **Built** (37e) | T: `one_rule_an_observation_is_weighed_by_the_two_doubts_whatever_the_run` |
| The rule, 2: when they disagree by more than their doubts allow, the observation is taken | **Built**, with two for the brief's three (Part 4, C8) | R: `reckoning.py`, `OBSERVATION_OUT_SIGMAS = 2.0`. T: `one_rule_an_observation_is_taken_when_the_account_is_plainly_out` |
| The rule, 3: the doubt grows whether she has way or not, fits the streams, and is not narrowed by the same thing seen again | **Built** (37e) | T: `the_doubt_grows_by_the_hour_hove_to_and_becalmed_and_not_at_anchor`, `the_doubt_of_the_stream_grows_along_its_set_...`, `the_same_thing_seen_again_tells_him_nothing_new`, `eight_casts_in_a_calm_over_the_flat_sand_off_ar_men_narrow_nothing` |
| The rule, 4: a fix chooses the tightest marks, counts the compass's shared error, and at anchor a poorer fix does not move the account | **Partly built.** All three are in. Still missing, by the builder's own note and the review's 11.3: a fix whose marks lie on one hand claims too much | T: `in_the_goulet_the_master_takes_the_near_marks_before_camaret_brest_and_conquet`, `over_the_geometry_of_game_9s_fixes_good_to_is_honest`, `moored_in_brest_road_a_fix_by_far_marks_leaves_a_sound_account_where_it_was` |
| The owner's ruling: (b), the master works the tide himself, now | **Built** (37e) | T: `the_master_works_the_tide_into_the_traverse_as_one_more_course`, `no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place`, `the_masters_tide_is_his_own_two_ships_ten_miles_apart_work_the_same_tide`. P: the cruise's noon line, "The day's work carried the master's tide by the directions and the epitome" |
| Ruled: where the study has no period source, the set to the nearest point and the spring rate to the half knot, as judgement | **Built** (37e) | T: `the_directions_state_every_water_in_the_periods_form_beside_the_worlds_figures`. The figures themselves not read |
| Ruled: `shape a course` steers to make good by default | **Built** (37e) | T: `a_course_shaped_across_a_stream_lies_up_tide_by_the_triangle_and_makes_the_place`. P: "Allowing the ebb, a knot to the SW, steer S by W to make it good" in the cruise's log |
| Ruled: the captain's `allow ... knots of set` replaces the master's tide until handed back | **Built** (37e) | T: `the_captains_set_replaces_the_masters_tide_until_he_hands_it_back`. R: `data/vocabulary.yaml`, `allow the tide by the book` |
| A model working the reckoning: now, no prompt | **Followed**: nothing was built | |
| ... an officer's reckoning of his own beside the master's | **Not built**; "Not in 37e" | |
| The package built as two, the account and then lying to and the ground | **Done** as ruled | Part 3 |
| `shape a course` says when its line crosses or skirts the shore | **Built** (37e) | T: `a_course_shaped_across_a_headland_or_close_along_the_shore_says_so` |
| The land-ahead cry says how near she will pass | **Not built**: I found no such words | R: `world/lookout.py` (the cry says where it lies, its distance and the minutes) |
| The station-safety package: the detector first | **Built** (37g) | 1.3 items 7 and 8 |
| The chart in words | **Not built**; design first | |
| A fog signal | **Not built**; later | |
| For the gate's checklist: what game 9 added | A statement about play; not checked | |
| The plan as ruled: 37e, 37f, 37g, one at a time; the pilot is 37h | 37e, 37f and 37g **built** in that order; 37h **not written** | D: the snapshots |
| 37f's three rulings: `loose` stays; `trim sails` declines hove to; `let go` keeps its scope, says it and takes a number | **Built** (37f). `loose`: no change found, not probed | T: `trim_sails_is_declined_while_she_is_hove_to_...`, `let_go_says_what_it_will_do_as_the_order_is_given`, `let_go_takes_a_scope_and_veers_to_that_and_no_further` |
| Pushing back: build the ground tackle from the table in 10.4, not from the officer's list | **Followed**, by 37f's brief | R: the brief, items 5 to 9 |
| Pushing back: the land-ahead cry not made milder | **Followed**: ten minutes and four, unchanged | R: `lookout.py` |

### 1.11 The review, 11.6: what game 10 changed in the plan

Nothing in this list is built. Nothing at all in the code or the data has changed since
game 10 was played: its two saves carry the fingerprint the build has today (P).

| Item | State | What I looked at |
|---|---|---|
| The runner, 1: a reply cut off while the model was thinking is not passed on as its turn | **Not built** | R: `agents/local.py` nowhere reads why a reply ended |
| The runner, 2: tokens counted by the server's own figure | **Not built** | R: `local.py`, `CHARS_PER_TOKEN` throughout |
| The runner, 3: the reserve as a share of the context as well as a number | **Not built** | R: `harness.py::handover_threshold` |
| The runner, 4: on a refusal for size, leave out the oldest exchanges and ask again | **Not built**; not checked in the code | |
| The runner, 5: the line the replay drops at a stand-down by the door | **Not built**; the fault is real | P: my replay of the save, 4,239 lines for 4,240 |
| Until then: `--handover-reserve 30000` and a larger `--max-reply` | Both flags exist; neither tried, by the review or by me | R: `local.py` lines 812 and 830 |
| The account, 1: the master allows the tide's height for the lead by his book | **Not built**; the cause not checked in the code | |
| The account, 2: a cast never moves the account beyond its own doubt | **Not built** | |
| The account, 3: the account worked at every tack, wear, heave-to and large alteration | **Not built** | |
| The account, 4: a fix's doubt when its marks lie on one hand | **Not built** | 1.10 |
| The ground and the helm: an anchor at the bows can be let go; a belay says where it left the anchor | **Not built**; not reproduced by me (Part 4, C7) | P |
| ... an anchor the ship does not carry is refused at the order | **Partly so already**: refused at once when nothing is in hand, accepted when the hands are at other work | P |
| ... a heave-to backs a sail that is set; the alarm leaves sail still being made alone; a lifting sail said first; anchoring in forty fathoms looked at | **Not built**; not checked | |
| Words: a course with a half point | **Not built**; the fault is real | P: "steer west; W (270°)" |
| Words: the fog reading's sentence; "put the helm over"; the phrasings in 11.4; the drill's count | **Not built**; not checked | |
| Words: a standing order's action read when it is given | **Partly so already**: its first word is read, the rest is not | P |
| For 37h: the depths in St Mary's Sound; the dangers shown by name; a pilot aboard three times who takes her nowhere | 37h **not written** | |
| The consent brief stands as approved | **So**: unchanged since the model of game 10 answered against it | P: digest `288d0b18e34d76a8` in the brief and in the record of 7 October |
### 1.12 The brief of 37d, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | The build's stamp: a name and a fingerprint of the rules in every save and checkpoint | **Built** | R: `core/world.py::fingerprint_of`, `build_stamp`. T: `a_save_and_its_checkpoint_carry_the_builds_stamp`, `the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings`. The cost at start: the builder's figure, not timed by me |
| 2 | `load` says what it did, and does not replay another build's game with a model aboard unless told to; every door the same words and `--replay-anyway` | **Built** | R: `core/replay.py::load_report`, `check_replay`. T: `load_says_which_road_it_took_and_why_a_checkpoint_was_not_taken`, `every_door_that_loads_or_replays_says_the_same_words_and_takes_the_flag` |
| 3 | A station seated at tick 0 replays in its place | **Built** | 1.5 |
| 4 | Old checkpoints kept as tests: two of the playtest's and one of the package's own | **Built** | P: the two playtest saves are the owner's own, byte for byte. T: 1.9. R: the playtest saves' tests skip when the files are missing; the package's own fail |
| 5 | The lookout judges a distance afresh as it changes | **Built** | 1.2 item 1. T: `a_sail_whose_distance_halves_is_said_nearer_and_the_closing_hail_is_fresh` |
| 6 | A bearing gives a line; second pass, the distance laid down when it is the better figure | **Built**, then **overtaken** in its rule by 37e's item 1 | 1.2 item 2 |
| 7 | A sail is no mark | **Built** | 1.2 item 4 |
| 8 | `take a fix`: its forms, its marks, its refusals, its words | **Built**. Two of its particulars **overtaken**: the fix no longer sets the account outright (37e), and the officer no longer needs `you may take a fix` (37g) | T: `take_a_fix_is_a_navigation_order_with_the_words_a_seaman_would_type`, `take_a_fix_is_completed_from_the_marks_in_sight`, `a_fix_is_refused_in_words_that_carry_the_cure`, `two_worlds_of_one_seed_say_the_same_fix_and_another_seed_another`, `the_standing_dialect_has_take_a_fix_for_nothing` |
| 9 | The shore always a sighting; `the nearest land` a reading; `Chart.nearest_shore` | **Built** | 1.2 item 5. T: `the_nearest_shore_is_the_ground_itself_beside_a_plain_search`, `the_nearest_land_says_none_within_a_league_and_not_to_be_seen` |
| 10 | Land ahead | **Built** | 1.2 item 6. T: `land_ahead_comes_again_after_the_quiet_and_not_at_anchor_without_way_or_in_fog`, `a_danger_ahead_is_named_and_where_it_lies_is_said_from_her_head`. The counts by passage are in `TuningNotes.md`; not checked |
| 11 | Two severities: dragging urgent, the pilot's hails notable | **Built** | 1.2 item 13 |
| 12 | The sea breeze blows from the sea | **Built** | 1.2 item 7. T: `the_coasts_trend_never_turns_two_points_between_samples`, `off_an_open_coast_the_trend_is_square_on_to_the_land_and_flat_in_a_road`. The tick rate before and after: not checked |
| 13 | One frame for the plane's points | **Built** | 1.2 item 8. T: `the_coasts_distance_at_the_ship_is_the_charts_at_her_position_after_a_long_run` |
| 14 | The recorded passages re-measured once, with the reasons | **Built**; the constants were set again by 37e and 37f. The table of reasons is in `TuningNotes.md`; I did not check it line by line | T: the six recorded passages' tests pass on today's constants |
| 15 | The documents | **Built**, by the list of files; I did not read them against the code | D: every document the item names changed at 37d |
| 16 | The report | Made to the lead; not in the tree. Not checked | |
| | Rule: every new field on a checkpointed class has a plain default | **Holds**, by its proof | T: the fixture tests |
| | Rule: nothing in the consent brief or a station's brief changes | **Holds** for the consent brief. Not checked for the stations' briefs | D: `ConsentBrief.md` unchanged at 37d |

### 1.13 The brief of 37e, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | One rule for every observation: weighed, taken or kept, and the words say which | **Built**, with two where the brief said three; `FIX_RUN_NM` is gone | 1.10. T: `the_noon_of_game_9_is_taken_and_against_an_account_a_mile_out_it_is_weighed`, `a_bearing_of_a_light_eleven_miles_off_after_twelve_miles_of_doubt_lays_the_line_down`, `the_words_of_a_cast_a_noon_and_a_bearing_say_which_of_the_three`. P: in the cruise's log, "the reckoning was out by it; laid down by the observation" and "the account moved a mile to the NE by N" |
| 2 | The doubt, honest: by the hour with or without way; sized by the water; the same thing seen again; said in cables and with its lie | **Built** | 1.10. T: `the_doubt_is_said_in_cables_under_a_mile_and_with_its_lie_when_long_and_thin`, `the_master_doubts_his_log_line_and_his_compass_in_the_run` |
| 3 | `take a fix` by the marks that fix her best; an honest "good to"; weighed as any observation | **Partly built**: all in, but marks all on one hand still claim too much | 1.10. R: `COMPASS_ALLOWANCE_DEG = 2.5`, `..._OBSERVED_DEG = 1.5` |
| 4 | The account hove to, becalmed and after | **Built** | 1.2 item 11. R: `HOVE_TO_DRIFT_KN = 0.25` |
| 5 | What the directions say of each water | **Built** | D: `data/tides/streams.yaml`, 126 lines added. T: `the_directions_state_every_water_in_the_periods_form_beside_the_worlds_figures`, `the_directions_are_looked_up_by_a_position_and_say_nothing_beyond_their_limits` |
| 6 | The tide in the traverse | **Built** | T: `the_master_works_the_tide_into_the_traverse_as_one_more_course` |
| 7 | The proof that it is his own | **Built** | T: `the_masters_tide_is_his_own_two_ships_ten_miles_apart_work_the_same_tide`, `a_master_with_moores_table_works_another_hour_from_one_with_nories`, `no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place` |
| 8 | The captain's word and the master's: the three forms of `allow`; he says what he allows; the line and the event when his tide turns | **Built** | T: `the_three_forms_of_allow_are_offered_and_each_is_taken_and_logged_as_whose_it_is`, `the_log_says_when_the_masters_tide_turns_and_when_she_passes_into_other_waters`, `the_reckonings_reading_carries_the_tide_allowed_and_the_doubt_as_it_stands_now`. P: "the tide allowed: none while she rides at anchor" |
| 9 | A shaped course makes good; worked once; the line tried against the shore | **Built** | 1.10. T: `a_course_shaped_by_the_masters_own_tide_makes_the_place_where_the_tide_is_the_books`, `a_course_shaped_with_no_way_on_or_against_too_strong_a_stream_says_so` |
| 10 | The recorded passages re-measured once | **Built**; set again by 37f | as 37d's item 14 |
| 11 | The books tuned for a true account; a passage that will not come through marked a strict expected failure and reported | **Partly built.** The merchant's book is tuned and takes its fix again (the passage's test asks twelve fixes in pilot water). Two beats were lost and marked, as the item allows: the schooner's pilot, the cruise's brig | T: `the_merchant_passage_at_seed_7_has_its_own_constants`; the two expected failures. "The Mingan passed by not less than a cable and a half": the builder's figure is 1.9 cables; not measured by me |
| 12 | The proof by measurement | **Partly built**: measured and reported, with three of the four things asked not met, as the changes file says. Not measured again by me, and not measured by anyone since 37f moved the passages | T for the fourth: `the_brig_hove_to_six_hours_of_a_spring_ebb_in_the_iroise_keeps_an_honest_account` |
| 13 | The documents | **Built**, by the list of files; not read against the code. One sentence left: the spec's truth 59 still says a cast "moves the reckoning onto the chart's contour" | D. R: `docs/TechnicalSpec-M5.md` line 742 |
| 14 | The report | Made to the lead; not checked | |
| | Rule: no line of the master's tide reads the world's tide or the ship's true place | **Holds**, by its test | item 7 |
| | Rule: the mere asking of a reading changes nothing (found and mended on the way) | **Holds**, by its test | T: `a_reading_of_the_account_asked_mid_tick_changes_nothing_another_gets_after_it` |

### 1.14 The brief of 37f, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | Heaving to that holds its tack: the way taken off first; she is kept there; forced round, one urgent line; every rig | **Built.** The fore-and-afters forereach more than the knot and a half asked, by the builder's own note | T: `the_brig_brought_to_from_each_of_the_games_states_holds_her_tack`, `held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam`, `a_fore_and_after_brought_to_holds_her_tack_in_her_own_manner`, `the_tending_costs_the_watch_its_hands_and_the_relief_takes_them_over`. P: "Hove to on the starboard tack, main topsail to the mast, helm a-lee" in the cruise's log |
| 2 | `fill away` on the tack she is on; `fill away and steer <course>` | **Built** | T: `fill_away_fills_her_on_the_tack_she_is_on`, `a_ship_that_has_come_round_is_filled_on_her_new_tack_not_the_recorded_one`, `fill_away_and_steer_gives_the_helm_the_course_when_she_is_full` |
| 3 | The record that she is hove to, cleared | **Built** | 1.5. T: `the_reading_and_the_dialects_guard_read_the_one_record` |
| 4 | `trim sails` hove to; the shipped books' guard | **Built** | 1.5. T: `the_starter_books_trim_rules_sleep_through_a_heave_to_and_wake_after_it`. The review's 11.4 notes the guard does not cover lying at anchor |
| 5 | An anchor's name is honoured by `veer`, `heave short`, `heave in` and `weigh` | **Built** | T (body read): `the_cable_worked_is_the_named_anchors_and_to_is_kept`; `the_refusals_name_the_anchor_she_rides_by_and_what_would_do_it`, `weigh_weighs_the_anchor_named_and_says_what_she_rides_by` |
| 6 | "To" is kept when an anchor is named | **Built** | the same test, twelve forms |
| 7 | `let go` says its scope and takes one; the warning | **Built** | P: "Let go the best bower in 17 fathoms; veering to eighty-six fathoms, five times the depth". T: `the_scope_is_warned_of_when_she_will_swing_within_a_cable_of_the_land`, `the_scope_is_warned_of_when_it_is_more_than_the_cable_she_has` |
| 8 | `heave in`; `heave short` takes no number | **Built** | P: both, as the item says |
| 9 | The dragging line: urgent once, then notable with how far; "holds again"; a slack cable; the advice | **Built.** A drag that relapses on bare rock is still an urgent line each time, by the builder's note | R: `core/world.py::_dragging_advice`. T: `a_dragging_is_urgent_once_and_then_says_how_far_she_has_come`, `the_goulets_eight_hours_give_at_most_five_lines_the_first_urgent`, `the_advice_names_only_what_is_left_to_do` |
| 10 | The ground's words: two grounds as their mean; a note for every port's road | **Built** | T: `a_note_of_two_grounds_is_the_mean_of_them_and_not_the_worst`, `every_ports_road_and_anchorage_has_its_note_of_the_bottom` |
| 11 | Three small anchoring faults | **Built** | 1.5 |
| 12 | What a ship at anchor may do | **Built** | 1.5 |
| 13 | The fore-and-aft cast | **Built** | 1.5. T: `a_cast_the_wrong_way_is_said_and_she_is_got_under_way_on_that_tack`, `the_square_riggers_cast_as_they_did` |
| 14 | No wind-shift line in airs too light to have a direction | **Built** | 1.4 item 2. T: `a_calm_that_boxes_the_compass_logs_no_shift`, `a_wind_that_swings_back_and_forth_is_unsteady_and_is_said_so_once` |
| 15 | The aback lines, by state | **Built** | 1.4 item 1 |
| 16 | A "could not" that is no failure | **Built** | T: `queued_work_that_finds_it_done_already_is_a_routine_line_and_no_failure`, `queued_work_that_cannot_be_done_is_a_failed_evolution_still`. P: at anchor `furl all sail` is answered "Every sail is furled already" |
| 17 | A no-bottom cast routine; a standing order with nothing to do, once a watch | **Built** | 1.4 items 3 and 4 |
| 18 | A standing order's condition checked when it is entered | **Built** | P: "the distance to the land" is refused at entry with the forms that serve. T: `the_distance_to_the_land_is_refused_at_entry_with_the_forms_that_serve`, `a_name_the_chart_nearly_has_is_answered_with_that_name`, `the_shipped_books_enter_whole` |
| 19 | The recorded passages re-measured once | **Built**; these are the constants the suite pins today | T: the six passages' tests |
| 20 | The documents | **Built**, by the list of files; not read against the code | D |
| 21 | The report | Made to the lead; not checked | |
| | Ruling: `loose` stays as it is | **Followed**, as far as the diff shows; not probed | |

### 1.15 The brief of 37g, item by item

| # | Item | State | What I looked at |
|---|---|---|---|
| 1 | A key to each seating | **Built** | 1.3 item 1 |
| 2 | The turn's budget | **Built** | 1.3 item 2 |
| 3 | The captain's word in an open turn | **Built** | 1.3 item 3 |
| 4 | The stand-by with the deck | **Built** | 1.3 item 4 |
| 5 | The contrary-orders detector; the test on the record | **Built** | 1.3 items 7 and 8. T: `orders_that_undo_one_another_bring_the_nudge_then_the_pause`. The review says it spoke not once in game 10 |
| 6 | The silence detector | **Built** | 1.3 item 6 |
| 7 | A paused or silent officer does not keep the deck | **Built** | 1.3 item 5 |
| 8 | The doors: the bridge asks again; the handover's reserve; no officer without a context size; the guard on his own brief | **Built** as briefed; the reserve is the fault of game 10 | 1.3 items 10 and 14. T: `the_handover_is_asked_for_at_a_reserve_in_tokens_and_of_an_officer_off_watch` |
| 9 | What a sample tells; the reading `the work in hand` | **Built** | 1.3 item 11. P: "The work in hand: doing: heaving in" |
| 10 | Whose order, and where the officer is | **Built** | R: `orders/navigation.py::_whose`. T: `whose_order_it_was_where_the_officer_is_and_what_he_says` |
| 11 | The deck, given and taken | **Built** | 1.9 |
| 12 | Three ways of leaving | **Built** | T: `the_three_ways_of_leaving_cannot_be_taken_for_one_another`. P: the officer's brief as sent says them in three lines |
| 13 | The opt-out path, mended | **Built.** One door short: the REPL's turn mode does not put the question again; it says so and seats nobody | 1.3 item 15. R: `agents/repl.py`, the module's own account; `harness.py::seating`. T: `the_repl_seats_a_released_station_again_by_the_games_one_rule` |
| 14 | Relief | **Built** | 1.6 item 6 |
| 15 | The journal, read | **Built**; `read_log`'s reach not checked | 1.3 item 9 |
| 16 | The officer's domain, as drawn | **Built** | R: `agent.py::OFFICER_DOMAIN`. T: `bearings_and_fixes_are_the_officers_own_and_a_sight_is_the_masters`, `an_order_that_changes_her_course_is_the_course_whatever_its_words` |
| 17 | A named grant means what it says | **Built** | 1.3 item 13. T: `the_captains_word_allows_a_named_thing` |
| 18 | The general grant | **Built**, keeping back more than the brief's five (Part 4, C6). "What cannot be undone" is one order today, `cut away`, and it was the officer's already, by the builder's note | R: `agent.py::_GENERAL`, `_KEPT_BACK`; `data/vocabulary.yaml`, `you may work the ship`. T: 1.6 item 1 |
| 19 | The way out of danger | **Built** | 1.6 item 2 |
| 20 | The consent brief's one revision | **Overtaken** by the owner's word of 7 October (decision 37): the four sections' approved words went in, and were then replaced by the leaner brief before any model was asked | P: the brief's body is found whole in `drafts/consent-brief-lean-draft.md`; 1,371 words |
| 21 | The station's brief and the doors' words | **Built** (second pass). Left: the watcher's brief lists three tools a watcher is refused; the officer's brief still says "1806" | P: both briefs written out afresh; they are the review's evidence file to the byte. T: `what_moved_out_of_the_consent_brief_is_in_the_briefs_of_the_stations` |
| 22 | The re-ask, proven | **Built** | T: `a_yes_given_before_the_briefs_revision_is_asked_again_and_the_question_says_why`. P: by the rule, six identities are asked again and one is not |
| 23 | The documents; the decisions log; every document that still states the old re-seating rule found and mended | **Built** for the decisions log (34 to 37; decision 33 is marked superseded). Not mended: the gate's headline item 6 still says "a second seating once" beside the new parenthesis. The rest not read against the code | R: `docs/DesignProposal.md` lines 622 to 630; `docs/gates/gate-m5c.md` line 18 |
| 24 | The report | Made to the lead; not checked | |
| | Rule: no model is seated and no door opened to one | **Could not tell** from the tree. Consistent with it: no consent record was made or changed at the hours of the build; the two new ones are dated at the starts of games 9 and 10 | D: the records' times |
| | Rule: a save of an earlier build with a station held loads and plays on | **Holds**, by its tests | T: `an_older_save_with_a_station_held_plays_on_under_this_builds_rules`, `a_station_loaded_from_its_checkpoint_is_taken_over_by_the_same_model` |
### 1.16 The changes file: everything it says was left

"Still so" means the build as it stands is as the note describes.

| From | Left undone | State today | What I looked at |
|---|---|---|---|
| The base | The saves of m5c and m5c-b left behind | **Still so**, by the owner's rule | D |
| The base | The owner's notes of m5c left behind | **Still so** | D |
| The base | The one consent record made under m5c-b left behind | **Still so**; see Part 3, 3.7 | D |
| 37d | The account in the Goulet is not a true one | **Overtaken** by 37e: the reckoning's rule changed and the merchant's book was tuned for it. Whether it is now true there: the builder's figures, not measured by me | 1.13 item 11 |
| 37d | `take a fix` sets the account outright and picks its marks by how they cut | **Overtaken** by 37e: weighed, and by the near marks | 1.13 item 3 |
| 37d | The dialect does not take cables | **Still so** | P: "'the nearest land' is compared in miles, not cables" |
| 37d | `the port` and `the depth of water` give the true figures | **Still so**, by the plan | 1.2 item 14 |
| 37e | The three figures asked for and not met (the merchant's time more than three miles out; the frigate within a mile and a half inside half an hour of the land; the merchant's honesty) | **Not checked.** Nobody has measured them since 37f moved the passages | |
| 37e | The schooner's pilot hails and does not board | **Still so** | P: an expected failure in my run |
| 37e | The cruise's brig is chased and lost | **Still so**; the reason given is partly wrong (Part 2, 2.4) | P |
| 37e | At anchor in the Bay of Brest the master is surer than he should be | **Not checked**; nothing since claims to mend it | |
| 37e | A wrong chronometer can displace a good account | **Still so** | P: the cruise at 09:00 on the 12th, tick 10800, "the reckoning was out by it; laid down by the observation: moved two leagues and ..." |
| 37e | The number in the one rule is two where the brief said three | **Still so** | R: `OBSERVATION_OUT_SIGMAS = 2.0` |
| 37e | In the open Channel the master's tide is a rough allowance | **Not checked** | |
| 37e | Spec truth 59's sentence left for the lead | **Still so** | R: `docs/TechnicalSpec-M5.md` line 742 |
| 37f | The cruise's stranger is not spoken | **Still so** | P |
| 37f | The schooner's pilot does not board; left for 37h | **Still so**; 37h is not written | P |
| 37f | A dragging that relapses is more than one urgent line | **Not checked** | |
| 37f | The fore-and-afters hove to make more than a knot and a half | **Not checked.** The review says the cutter of game 10 lay hove to forereaching at about a knot | |
| 37f | A course shaped with next to no way on her is worked for that way | **Not checked** | |
| 37f | On the cruise two orders give chase to one sail at the same moment, and the second wear fails | **Still so** | P: ticks 79260 and 79261, and "Could not wear: she would not come round" at 80653. The same doubling shows at 07:00, where three orders give chase within a second |
| 37f | Under eight test workers the workers die at random | **Not checked.** Under four, in my run, none did | P |
| 37g | The silent officer's deck is not in the consent brief | **Overtaken**: it is in the brief as it stands ("or that has been told it is silent past its time") | R: `docs/agents/ConsentBrief.md`, *Being stopped* |
| 37g | What cannot be undone is one order, and it was the officer's already | **Still so**, by the builder's account; I did not go through the vocabulary | R: `agent.py::OFFICER_DOMAIN` holds the object `wreck` |
| 37g | Kept back from the general grant beyond the brief's list | **Still so**, and not ruled on the record (Part 4, C6) | R: `agent.py::_KEPT_BACK` |
| 37g | The REPL's turn mode does not put the consent question again after an opt-out | **Still so**; it seats nobody when the question is owed | R: `agents/repl.py`, the module's own account |
| 37g | A standing order the officer writes under the captain's word stays in the book when that word ends | **Not checked** | |
| 37g | An act at the very tick a station is seated is not replayed | **Not checked** | |
| After 37g's build | "One thing is still open with the owner": four heads in the brief, more in the build | The wording **closed** by the second pass; the ruling **not on record** | Part 4, C6 |
| 37g's second pass | The watcher's brief lists `hand_over` and `handover_note`, both refused to a watcher | **Still so**, and `submit_order` with them | P: the watcher's brief as sent |
| 37g's second pass | `stand_down` takes its note and does not insist on one | **Still so** | R: `agents/tools.py::stand_down`, the note defaults to nothing |
| Played, 7 and 8 October | Everything the paragraph lists from game 10; "nothing was changed in the build for this" | **So**: nothing was changed | P: the fingerprint in game 10's saves is today's. For the items themselves see 1.11 |

## Part 2. The gate

`docs/gates/gate-m5c.md`, item by item, as the build stands today.

### 2.1 The gate's document itself

- **Verdict: Pending.** Unchanged.
- **One change since the gate was cut**: a parenthesis in headline item 6, added by 37g, saying
  that a released station may be taken again as often as asked, that the deck goes to and
  fro, and that the detector counts orders that undo one another. (D: the file differs from
  m5c's only there; first changed in the snapshot after 37g.) The sentence it follows still
  says "a second seating once" and "contrary orders within a watch bring the nudge".
- **The rest of the document describes m5c as cut, and the build no longer matches it.**
  Nothing in it was re-measured after 37d to 37g. What is stale:

| Where | The gate's text | The build today | How I know |
|---|---|---|---|
| Setup, fast tier | "ends `2471 passed` and a line saying 244 slow tests were left out" | 2,731 passed by the changes file; 259 slow tests are left out (P: counted by collection; the fast tier was not run) | see 2.5 |
| Setup, whole suite | "`2708 passed, 7 xfailed`; the seven are your rulings" | **2,981 passed, 9 xfailed.** Two of the nine are not rulings (2.3) | P: my own run, 2.5 |
| The merchant passage | Falmouth pilot off 10:07; a sail off the Lizard at 12:49 "on the larboard bow, bearing SE by E, distant three leagues"; Brest pilot aboard 06:26; Bertheaume 07:47; the Bay 13:05; the tin sold 15:10 | pilot off 10:05; the sail at 13:05 "abeam to starboard, bearing W by S"; Brest pilot aboard 07:44; Bertheaume 08:46; the Bay 13:10; the tin sold 15:25 | R: the pinned ticks in `tests/test_known_truths.py`, `GATE_5C_MERCHANT_*`; the test passes in my run |
| The naval cruise | pilot aboard 08:12, off 09:07; the admiral's cutter within hail at 10:57 on the 12th; eight wears in the night; the *Palinure* at 07:16 "right ahead four leagues"; spoken at 11:42 | pilot aboard 08:13, off 09:03; the cutter within hail at 05:17 on the 13th, on the station; three wears and one that failed before 07:00; the *Palinure* at 07:00 "on the starboard quarter, bearing NNW, distant four miles"; **never spoken** | P: I sailed the cruise under its book (2.4) |
| The account against the truth | the figures at each noon and anchor | not re-measured by anyone since 37e; not checked by me | not checked |
| Item 1's expected lines | "at 12:49 'Sail ho! A sail on the larboard bow ...'"; "the purse moves by £6,000" | the 12:49 line is not said (above). The sale is for £10,800; £6,000 is the profit (the review's 8.2 asked for this to be mended; it was not) | R |
| Item 2's expected lines | "'Sail ho! A sail right ahead, bearing SW, distant four leagues' on the second morning"; "within hail: a stranger under no colours" | neither line is said | P |

### 2.2 The fourteen items

"Play" means the owner's own check in the browser or with a model. I started no server and
seated no model, so no item was checked in play; what is said of play comes from the review
(sections 4, 10.6 and 11) and is marked as its claim.

| # | Item | As the build stands | What I looked at |
|---|---|---|---|
| 1 | The merchant passage in the browser | The scripted passage comes through whole, Falmouth to the tin sold at Brest, with no grounding and no dragging. The expected lines in the gate's text are stale (2.1). Not checked in the browser | T: `test_the_merchant_passage_at_seed_7_has_its_own_constants` passes in my run; R: its constants |
| 2 | The naval cruise in the browser | **Does not come through.** The yard's provisions, the pilot, the admiral's letter and the station are there; the stranger is sighted, chased for half an hour, and lost. The review says the cruise has never been played by the owner at all | P: my own run of the scenario (2.4); T: `test_the_naval_cruise_speaks_the_stranger` is an expected failure |
| 3 | The longitude (on the cruise) | The orders are there and the scripted truths pass. On the cruise's own log the first time sight, at 09:00 off Plymouth with the land in sight, is "laid down by the observation" and moves the account more than two leagues: the fault 37e's own note admits (a chronometer trusted within five miles that is further out than that). The review says this item has not been played | P: my run, tick 10800; T: `test_truth_60_...`, `test_truth_61_...` pass |
| 4 | The tide at Falmouth | Unchanged in what the item asks. New since the gate: the master works the tide into the reckoning, and `the reckoning` says what tide is allowed | T: `test_truth_62_...`, `63`, `64` in `tests/test_tide.py` pass. Not checked in play |
| 5 | The anchor | Changed by 37f, and the item's lines still hold in form: "The best bower let go in 17 fathoms and a half; eighty-six fathoms of cable veered", "Brought up by the best bower ... Riding by the best bower to the flood". New: the first line says the scope ("veering to eighty-six fathoms, five times the depth"), an anchor's name is honoured, `heave in` exists, the dragging line is urgent once and names only what is left to do | P: my own probe at Carrick Road; T: `tests/test_tackle_orders.py` (26 tests) pass |
| 6 | The port | No change to the port's code but the severity of the pilot's hail (37d). Not checked | D: `freesail/world/ports.py` changed in 37d only |
| 7 | St Mary's and Roscoff | No change to the code. The review says British colours off Roscoff have not been played; St Mary's was entered in game 10 | D; the review's claim |
| 8 | The library's papers | No change found. Not checked | D: nothing under `client/` changed; the library's code unchanged |
| 9 | The lookout and the chart in the captain's hands | `shape a course` now steers to make good against the master's tide and says when its line crosses or skirts the shore; the nearest land is a reading; the client's chart is unchanged | T: `test_a_course_shaped_across_a_headland_or_close_along_the_shore_says_so`; P: probe of `the nearest land` |
| 10 | The officer's watch, Opus 5.5 through Claude Desktop | Played on m5c, m5c-b and on this folder at 37d (the review's games 2, 4, 8 and 9); **not played on the build as it stands**. Opus 5.5's last yes (6 October) was given against the brief as it stood before 37g, so the question is owed again, naming four sections, and the drill after it. The item's own words are stale: the deck given and taken no longer seats and unseats; `hand_over` gives the deck back and the officer stays | P: `consent_check` (my own read of the records by the game's rule); R: the item |
| 11 | The officer's watch, a local model on the cutter | Played on the build as it stands (game 10, 63 hours, by the review's account). The model's record of 7 October is against the brief as it stands and it is not asked again. Both seatings ended when the conversation outgrew the model's context; the cause is in the code (Part 4, C7) | P: the record's digest is the brief's (`288d0b18e34d76a8`); R: `harness.handover_threshold`, `local.py` |
| 12 | The truths of this gate | The gate's first command selects eleven tests (truths 6, 7, 60, 61, 65, 67 to 72); truths 62 to 64 and 66 are in `tests/test_tide.py` and `tests/test_ground.py` and are not selected by it. All of them pass in the whole suite. Neither of the two new expected failures is in the selection, so **this item passes as written while the cruise is broken** | P: `--collect-only` of the gate's own command; my suite run |
| 13 | A scenario saved and loaded | The cruise saved at 08:00 on the 13th replays to the same digest, and a save loads from its checkpoint. "The chase goes on to the same words" cannot be shown: at 08:00 the chase is already lost | T: `test_truth_72_the_two_scenarios_replay_to_the_same_digest` passes; R: `GATE_5C_CRUISE_SAVE_TICK` |
| 14 | Rulings wanted | *The officer's domain*: ruled (the review's section 9, questions 4 and 5, and the way out of danger kept on 7 October) and built by 37g. *The sample's size on a local model*: answered by play; the context is the live trouble (item 11). *A far-detail vessel's bound*: **not ruled and not built**; no guard refuses a leg that crosses the coast when a scenario loads. *The re-asks*: the rule watches six sections today (the opening, what an instance would see and do, leaving, being stopped, what is not done, the journal); the drill is unchanged and the review calls it too small | R: `agent.py::OFFICER_DOMAIN`, `consent.py::RE_ASK_SECTIONS`; no match for a coast guard in `world/scenarios.py` or `world/ships.py` |

### 2.3 Every test marked as an expected failure

Nine, all strict (a test that began to pass would fail the suite), all in
`tests/test_known_truths.py`. P: all nine were reported as expected failures in my run.

| Test | Since | Why it is marked |
|---|---|---|
| `test_truth_3_broad_reach_is_the_schooners_fastest_point` | milestone 3b | the schooner is fastest with the wind abeam, not on the quarter; the sail model has no cost for a fore-and-aft rig pressed on a reach |
| `test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward` | 3b | the wear comes to as soon as the wind is aft and loses about a tenth of a mile |
| `test_truth_18_the_watch_and_all_hands_take_the_spec_times` | 3b | plain sail is set in 16 minutes by the watch and under 6 by all hands, against the spec's 25 to 40 and 12 to 20 |
| `test_truth_24_a_quarter_point_closer_or_a_quarter_knot_more` | 3b, the owner's ruling | the after yards braced sharper gain 0.17 knot, under the quarter |
| `test_truth_26_about_half_a_point` | 3b, the owner's ruling | the bowlines gain a third of a point, not half |
| `test_truth_28_lying_a_try_under_a_knot_and_a_half` | 3b, the owner's ruling | a-try in 45 knots she goes astern at four to five knots |
| `test_truth_31_a_quarter_point_closer` | 3b, the owner's ruling | the catharpins gain under a degree |
| `test_the_schooners_pilot_boards_before_she_runs_in` | **37e** | the schooner of gate 5b now stands in at seven knots, and the Falmouth pilot, who boards a ship making under six, hails her and is left astern. Three mends of her book were tried and none kept. Left for 37h, the pilot's package, which is not written |
| `test_the_naval_cruise_speaks_the_stranger` | **37e**, restated by 37f | the cruise's French brig is chased and lost. The reason written on the mark is partly wrong (2.4) |

The first seven are the same seven the gate's document names (truths 3, 11, 18, 24, 26, 28
and 31; R: the same seven marks stand at the same lines of the gate's own file). The last two are beats of recorded passages
that the week's work lost. They are not rulings of the owner's, and the gate's sentence
"the seven are your rulings" is no longer the whole of it.

### 2.4 The naval cruise: exactly what stops it

I sailed `data/scenarios/naval-cruise.yaml` under its own book on the build as it stands,
to 08:40 on the second morning, and wrote out her log and her head, the wind and her way
every half minute about the chase (the scripts and their output are in my scratch folder,
`handover-audit\cruise_probe.py`, `cruise-log.txt`, `cruise-state.txt`). Every beat up to
there falls on the tick the passing test pins (the yard's stores, the pilot aboard and
off, the cutter's hail, the letter, the sighting, the chase lost), so this is the passage
the suite holds.

**What happens.**

1. *05:17 on the 13th* (tick 83838). The port admiral's cutter comes within hail on the
   station and the letter is read. Before 37e she caught the frigate off Plymouth at 10:57
   on the 12th; since 37e the frigate fills and sails as soon as the pilot is off, and the
   cutter has a stern chase of nineteen hours. The frigate chases the cutter (a stranger
   until her colours are made out) to the north-eastward for 76 minutes before she is
   within hail, then shapes for the station again.
2. *07:00* (tick 90000). The scenario's own order puts the *Palinure* on the sea at a
   position fixed in the file, 48° 50' N, 5° 16' W. The frigate is then at 48° 45.6' N,
   5° 12.9' W, standing SSW (206°) at five knots and a quarter: **the brig appears 4.8 miles
   on her starboard quarter, up wind of her and already standing away NE by N** at something
   under six knots (my reckoning from her bearing and distance at two moments). The scenario file's own comment says where she was meant
   to be: "five leagues on the frigate's bow at seven". At m5c, by the gate's own text, she was
   sighted right ahead at 07:16.
3. *07:00, the first chase order.* The brig bears NNW, 35 degrees from the wind's eye, so
   the course for her cannot be laid. `_chase_course` then puts the frigate close-hauled
   "on the tack she is on", which is the starboard tack, heading SW by W: **102 degrees away
   from the chase**, where the other tack would have pointed within 33 degrees of her. The
   line says "she is kept full and by on the starboard tack". For thirty minutes the two
   ships sail apart; the range opens from 4.9 miles to 8.5.
4. *07:30* (tick 91800). The book's "keep her bearing" gives chase again. The brig now
   bears N by E and the course ordered is NE by E (54°). The frigate's head is SW by W
   (229°): the new course is 175 degrees round, and the shorter way to it is **to larboard,
   by the stern**. The guard that wears her for a course "across the wind's eye from her
   head" looks only for the wind's eye inside the shorter turn; here the eye lies the other
   way, so no wear is ordered and the plain order `steer 54` is given. The helm takes her
   round by the stern (her head 229°, 206°, 169°, 135°, 104°, 78°, 63°, 54° at
   half-minute intervals) **with her yards still braced sharp up for the starboard tack.**
   Nobody braces them: the book's trim rules fire when she is "steady on the course" or the
   wind shifts, and neither happens. At 07:32:34 (tick 91954) every square sail is aback
   with the wind on her larboard quarter, the urgent line "Taken aback: the sails pressed
   against the masts and she lost her way" is logged, and she lies without way.
5. *07:57* (tick 93420). The brig is out of sight. The book shapes for the station again,
   which turns her back the same way; she has no way on at 08:00.

**The same handling fault bites earlier in the same log and is reported nowhere.** At
05:17, when the book shapes SW by S for the station from a head of NE by E, she is again
turned 150 degrees by the stern with her yards unbraced and is "Taken aback" at tick 83957,
an urgent line. That time she steadies on the course four and a half minutes later and the trim rule
braces her round. The changes file, the test's comments and the review mention one failed
wear (tick 80653) and one taking aback; there are two urgent lines in the cruise as pinned.

**Where it is in the code.** All of it is code the gate was cut with; none of it was
written this week (D: `_chase_course`, `_course_not_laid`, `_helm_for` and the `give chase`
order are the same to the character in the gate and the build, and so is
`naval-cruise.yaml`). The week's work changed where the frigate is at 07:00, and that exposed
it.

| What | Where |
|---|---|
| The brig's place and hour | `data/scenarios/naval-cruise.yaml`, `world_orders`, the third line: `ship: a brig-sloop "Palinure" of France at 48 50 N 5 16 W ...` at `1805-06-13T07:00` |
| The tack chosen for a chase too near the wind | `freesail/orders/navigation.py`, `_chase_course`, the last block ("on the tack she is on") |
| A large alteration by the stern given to the helm alone | `freesail/orders/navigation.py`, `_course_not_laid`, the branch that returns `"wear ship"` only when the wind's eye lies inside the shorter turn; and `give chase` and `shape a course for`, which then call `steer` |
| Nothing braces the yards while she turns | the cruise's book, `data/scenarios/naval-cruise.orders`: "trim to the course" waits for `steady on the course`; `steer` moves the helm and no more |

**What I tried, in memory only, with nothing in the tree changed** (`cruise_exp.py`,
`cruise_exp2.py` in my scratch folder):

| Trial | Result |
|---|---|
| The chase and the shaped course wear her whenever the new course puts the wind on her other side by the stern | no taking aback; she wears cleanly at 07:30; **the brig is still lost**, at 08:01 |
| The chase chooses the tack that points nearer the chase | the tack is ordered from a head too far off the wind and fails three times; taken aback at 07:32; the brig lost at 07:52. My change was crude; it shows only that this is not a one-line mend |
| Both together | the brig lost at 07:35 |
| **No change to the code. The brig put five leagues on the frigate's bow at 07:00** (48° 32' N, 5° 23' W in place of 48° 50' N, 5° 16' W) | **the meeting comes back.** Sighted at 07:17 "right ahead, bearing SSW, distant three leagues"; chased by her bearing; made out at 08:02 and 08:16; **within hail at 08:21** (tick 94899), "a stranger, her colours not made out"; "the chase up" shapes for the station at the same tick. Both things the expected-failure test asks are then true |

**So the changes file and the test's mark are right in one half and wrong in the other.**
They say that either the chase order wearing her, or the scenario's hours, would bring the
meeting back. On my trials the first does not and the second does. And the mark's account
of the moment itself ("a course across the wind's eye from her head, and the helm takes
her through the wind") is not what the ship does: she is not taken through the wind; she
is turned the other way, by the stern, and is caught aback because her yards were never
braced round. That matters to whoever mends it, because the mend the mark names (wearing
her "for a course across the wind, as its first form does") is already in the code and did
not fire, rightly by its own test.

**What the cruise needs to close.** One line of the scenario file set again for where the
frigate now is, the cruise's constants recorded again (its digest, its 1,988 lines, the
ticks of the sighting, the chase and the hail), the expected-failure mark taken off, and
the gate's text of the cruise written again. The brig's place is tuned to the frigate's
track, so any later change to the account, the tide or the pilot will move it again; a
world order that places a ship from the player's own position ("five leagues on her bow")
would not be so brittle, and does not exist. The handling fault (a large alteration given
to the helm with the yards left braced) is a separate matter that stays in the game
whatever is done to the scenario. (In the trial that brought the meeting back she was
taken aback once more, at tick 115716, half a minute after a wear at the hour. That is
another circumstance and I did not trace it. Of the pinned passage I read the first 26
hours and 40 minutes; the rest was run by the suite and not read by me.)

### 2.5 The suite and the linter, first hand

From the build folder, with `PYTHONPATH` set to it, `PYTHONUTF8=1` and
`PYTHONDONTWRITEBYTECODE=1`:

| Command | Its last line |
|---|---|
| `py -m pytest -n 4 --slow -p no:cacheprovider`, run once | `2981 passed, 9 xfailed in 1179.13s (0:19:39)` |
| `py -m ruff check . --no-cache` | `All checks passed!` |
| `py -m ruff format --check . --no-cache` | `171 files already formatted` |
| `py -m pytest --collect-only -q -p no:cacheprovider` (the fast tier counted, not run) | `fast tier: 259 slow tests left out` |

The suite's figures are the lead's: 2,981 and nine. It took nearly twenty minutes here
against his thirteen; other work was running on the machine. The nine expected failures
are the nine of 2.3, each named in the run's summary. With 2,990 tests in all and 259
left out, the fast tier is 2,731, which is the changes file's figure for it.

I gave the linter `--no-cache` so that it would write nothing in the folder; the brief's
command is the same without it. No `.pytest_cache` was made, and the listing of both
folders taken before the suite is the same after it.

### 2.6 What closing the gate needs

1. **The naval cruise brought through** (2.4): the scenario's line, the constants, the mark,
   the text.
2. **A decision on the schooner's pilot.** Her passage is gate 5b's, but its lost beat is one
   of the nine expected failures of this gate's suite. It waits on 37h, which is not written.
   Either 37h is built before the gate closes, or the gate closes with the mark standing
   and says so.
3. **The gate's document written again for the build**: the two suite lines, the passages'
   times and words, the account's figures, items 1, 2, 5, 6 (the headline), 10 and 13, and
   item 14 turned from "rulings wanted" into the rulings given. The folder's name comes
   out of headline item 6.
4. **The play the gate still lacks**, by the review's own count (its sections 4, 8.8 and
   10.6; I cannot check play): the naval cruise, the chronometer and the lunar on it,
   British colours off Roscoff, and the lead's own officer's watch, which the gate's
   opening lines make half of the verdict.
5. **The consent question, again, before any of that play with a model.** Six identities
   hold a yes that the rule will ask again at the next seating: Opus 5.5, Sonnet 5, Sonnet
   5.5, the llama3.1 8B, the qwen3.8 27B (by digest) and the Gemma4 26B Q4_K_M. Three of
   them (the September records) are asked with five sections named, the others with four.
   Only the Qwen3.8 27B 0814 file has answered against the brief as it stands. (P: my own
   read of the records by `consent.decide`.) Item 10 names Opus 5.5 through Claude Desktop,
   so that re-ask and its drill come first.
6. **The ruling the gate asked for and never had**: a far-detail vessel's leg across the
   coast (item 14).
7. **`BUILD_NAME` set for the gate**, with the nine test lines that spell it (Part 3).

## Part 3. What changed in the tree

### 3.1 How it was compared

I hashed every file in seven places and set them side by side: the gate folder, m5c-b, the
lead's four snapshots (after 37d, 37e, 37f and 37g's first pass) and the build as it stands.
Caches were left out. A file is put down to the package after which its content first
differs from the stage before. I also compared the gate folder with the gate's own zip,
`FreeSail-gate-m5c.zip`, reading the zip without extracting it. The scripts and their tables
are in my scratch folder (`treecmp.py`, `treesum.tsv`, `zipcmp.py`, `areas.py`).

Two things about the baseline first.

- **The gate folder is not the gate as cut; it is the gate as cut and then played in.** Every
  one of the zip's 589 files is in the folder unchanged. The folder holds 87 more: the
  owner's saves (14 under `saves\`, three more with their checkpoints at the root), his
  notes, four scenario files he wrote during the playtest (`data/scenarios/merchant-brig.yaml`,
  `merchant-cutter.yaml`, `merchant-schooner-plymouth.yaml`, `merchant-ship.yaml`), eight
  consent records made in play, and the review folder (54 files).
- **The review folder in the gate was the same, byte for byte, as the one in the build** when
  I compared them (before this file and `report-2.md` were added here), this morning's
  `report.md` included. The changes file calls the build's "a copy of the review
  as it stood on 2026-10-06" with the original in m5c; in fact both have been kept in step.
  A diff of the build against the gate folder therefore shows nothing of the review, and a
  diff against the zip shows all of it.

### 3.2 In numbers, the build against the gate folder

129 files changed, 23 added, 21 gone. The 21 are the owner's saves and notes of m5c, left
behind on purpose. The 23 are below.

| Area | Changed | New | Lines added / taken out | Which package |
|---|---|---|---|---|
| Code, `freesail/` | 44 | 0 | 10,408 / 1,188 | below |
| Tests, `tests/*.py` | 27 | 3 | 8,705 / 316 | below |
| Data, `data/` | 37 | 1 | 641 / 101 | below |
| Documents, `docs/` (the review folder aside) | 21 | 2 consent records | 3,224 / 114 | below |
| Test fixtures | 0 | 7 | | 37d (six), 37g's second pass (one) |
| The root | 0 | 2 | | `CHANGES-m5c-c.md`; `m5c-c Notes.txt` (the owner's) |
| The owner's saves | 0 | 8 | | games 9 and 10 |

Nothing changed under `client/`, `tools/` or `.github/`, nor `README.md`, `pyproject.toml`,
`.gitignore` or `.mcp.json`.

**The changes file's own lists of files are right.** For each of 37d, 37e, 37f, 37g and
37g's second pass I set its "Files changed" paragraph against what the snapshots show
changed at that stage, and found no file changed that it does not name and none named that
did not change. And m5c-b's claim holds: the 22 files m5c-b changed came into the build byte
for byte (15 of them were still m5c-b's own bytes after 37d; the other seven had by then
been changed again by 37d).

### 3.3 The code, by area

| Area | Files | Changed by |
|---|---|---|
| `freesail/agents/` (the harness, the doors, consent) | `agent.py`, `harness.py`, `tools.py`, `remote.py`, `consent.py` | m5c-b, then 37g; the first three again in 37g's second pass; `harness.py` also in 37d |
| | `mcp_server.py`, `local.py` | 37g and its second pass |
| | `journal.py`, `__init__.py` | 37g |
| | `repl.py` | 37d, 37g |
| `freesail/world/` | `reckoning.py` | 37d, 37e, 37f |
| | `chart.py` | 37d, 37e |
| | `lookout.py`, `weather.py`, `ports.py`, `ships.py` | 37d |
| | `tide.py` | 37e |
| | `ground.py` | 37f |
| | `people.py` | 37g |
| `freesail/core/` | `world.py` | m5c-b, 37d, 37e, 37f, 37g (the build's name each time) |
| | `replay.py` | m5c-b, 37d |
| `freesail/orders/` | `navigation.py` | 37d, 37e, 37g |
| | `complete.py` | 37d, 37e |
| | `verbs.py`, `ground_tackle.py` | 37f |
| | `stations.py`, `vocabulary.py`, `crew.py` | 37g |
| `freesail/evolutions/` | `scripts.py`, `runner.py`, `registry.py` | 37f |
| `freesail/physics/` | `hull.py`, `integrate.py` | m5c-b, 37f |
| | `anchor.py`, `sails.py` | 37f |
| `freesail/standing/` | `book.py`, `rules.py` | 37f |
| | `runtime.py` | 37f, 37g |
| `freesail/api/` | `readings.py` | 37d, 37e, 37f, 37g |
| | `queries.py` | 37g |
| `freesail/ui/` | `server.py` | 37d, 37g |
| | `console.py` | 37d |
| `freesail/ship/parts.py`, `freesail/crew/model.py` | | 37f; 37g |

### 3.4 Data and fixtures

| What | Changed by |
|---|---|
| `data/vocabulary.yaml` | every package: `take a fix` (37d); the three forms of `allow` (37e); `heave in`, `fill away and steer`, the anchors' names (37f); the general grant, `stand down`, `resume the officer`, and the table of what undoes what (37g) |
| `data/tides/streams.yaml` | 37e: what the master's directions say of each water |
| `data/evolutions/`: 27 changed, `heave_in.yaml` new | 37f: eight evolutions of lying to and the ground rewritten; nineteen marked so that "done already" is no failure |
| `data/scenarios/gate-5b-passage.orders` | 37d, 37e, 37f |
| `data/scenarios/merchant-passage.orders` | 37d, 37e, 37f |
| `data/scenarios/gate-5b-passage-schooner.orders` | 37d, 37e |
| `data/scenarios/naval-cruise.orders` | 37d, 37f. **`naval-cruise.yaml` itself is unchanged**, which is where the cruise's trouble lies (Part 2) |
| `data/standing_orders/starter.orders` | 37f: the guard on its trim rules |
| `data/charts/features/channel-west.yaml`, `.index.json`, `data/charts/manifest.yaml` | 37f: the note of the bottom in Brest road |
| `tests/fixtures/saves/m5c-cutter-tick34091` and `m5c-b-harpy-tick602100`, each a `.json` and a `.checkpoint` | 37d. **They are the owner's own saves, byte for byte** (P: compared with `FreeSail-gate-m5c\saves\freesail-seed7-tick34091` and `FreeSail-gate-m5c-b\saves\freesail-seed7-tick602100`). They hold a model's transcript and journal and the owner's typed lines |
| `tests/fixtures/saves/m5c-c-37d-officer-tick5400` (`.json`, `.checkpoint`) | 37d: a scripted game of the package's own making; nothing personal in it by its description (I did not read it through) |
| `tests/fixtures/ConsentBrief-before-37g.md` | 37g's second pass: the consent brief as it stood before 37g, for the test of the re-ask. Its digest is `f667a04e00b32e1f`, which is the digest Opus 5.5's record of 6 October was asked with (P) |

### 3.5 Tests

Three new files, all 37f's: `tests/test_lying_to.py` (20 tests), `test_tackle_orders.py`
(26) and `test_log_lines.py` (19). In all there are 191 test names the gate did not have
and seven it had that are gone, each of the seven replaced by a test of the new rule
(for example `test_you_have_the_deck_seats_the_officer_and_i_have_the_deck_stands_it_down`
by `..._gives_it_and_i_have_the_deck_takes_it_and_no_more`).

| Changed by | Test files |
|---|---|
| m5c-b only | `test_hull.py` |
| m5c-b, then later | `test_agent_api.py` (37g), `test_weather_script.py` (37f), `test_known_truths.py` (37d, 37e, 37f), `test_officer.py` (37d, 37g, second pass) |
| 37d | `test_anchor.py`, `test_lookout.py`, `test_weather.py`; with 37e `test_chart.py`, `test_orders.py`, `test_readings.py`; with 37f `test_ports.py`; with 37e and 37f `test_reckoning.py`, `conftest.py`; with all three after `test_checkpoint.py`, `test_replay.py` |
| 37e | `test_tide.py`, `test_longitude.py` |
| 37f | `test_catalogue.py`, `test_evolutions.py`, `test_ground.py`, `test_staying.py`; with 37g `test_agents.py` |
| 37g | `test_mcp_server.py`, `test_local_runner.py`, `test_standing.py` |
| 37g's second pass | `test_consent.py` |

### 3.6 Documents

| Document | Changed by |
|---|---|
| `docs/TechnicalSpec-M5.md` | m5c-b, 37d, 37e, 37f, 37g, second pass |
| `docs/TechnicalSpec-M0-M2.md` | m5c-b, 37f |
| `docs/TechnicalSpec-M3.md` | 37f |
| `docs/TechnicalSpec-M4.md` | 37g, second pass |
| `docs/DesignProposal.md` | 37g (decisions 34 to 36), second pass (decision 37) |
| `docs/agents/ConsentBrief.md` | m5c-b, 37g, second pass. **Unchanged through 37d, 37e and 37f**, as each of those packages claims |
| `docs/agents/README.md`, `ConsentAndPreferences.md` | m5c-b, 37g, second pass |
| `docs/agents/Harness.md` | m5c-b, 37d, 37g, second pass |
| `docs/dev/M5-WorkPackages.md` | 37d, 37e (the plan and the four briefs; the lead's) |
| `docs/dev/TuningNotes.md` | 37d, 37e, 37f, 37g |
| `docs/gates/gate-m5c.md` | 37g (one parenthesis) |
| Primer 3, 5, 7, 11 | 37f |
| Primer 6 | m5c-b |
| Primer 10 | 37d, 37e |
| Primer 12 | 37e |
| Primer 13 | 37d, 37e, 37f |
| Primer 16 | m5c-b, 37g, second pass |

### 3.7 The consent records made in play

The zip holds ten files under `docs/agents/consent/`. The build holds twenty. None of the
eighteen that are also in the gate folder differs from it by a byte (P), so nothing on
record was edited this week.

| Record | Made | In the zip | In the gate folder | In m5c-b | In the build |
|---|---|---|---|---|---|
| The ten of September (three early transcripts, seven harness records) | before the gate | yes | yes | yes | yes |
| `2026-10-02-opus-5.5.md` | play at m5c | no | yes | yes | yes |
| `2026-10-03-qwen3.8-27b-digest-...` (three files) | play at m5c | no | yes | yes | yes |
| `2026-10-04-gemma4-...` (two), `2026-10-04-qwen3.8-27b-0814-...`, `2026-10-04-qwen3.8-27b-digest-...` | play at m5c | no | yes | no | yes |
| **`2026-10-03-opus-5.5.md`** | play at m5c-b | no | **no** | yes | **no** |
| `2026-10-06-opus-5.5.md` | game 9, on this folder at 37d | no | no | no | yes |
| `2026-10-07-qwen3.8-27b-0814-q4_k_m.gguf.md` | game 10, on this folder as it stands | no | no | no | yes |

So eleven records were made in play since the gate was cut, and **the build folder holds
ten of them. The eleventh, Opus 5.5's of 3 October, is only in m5c-b.** The changes file
says it was left behind because it is not part of m5c-b's diff. But the consent brief
tells every model that "this conversation is kept verbatim ... in the game's repository
under `docs/agents/consent/`". If that sentence is to stay true, all eleven go into the
repository, the one in m5c-b among them. It is superseded as Opus 5.5's latest answer by
the record of 6 October, so carrying it changes nothing the game decides. Records are read
by the game and are not to be edited on the way.

### 3.8 What belongs to this folder alone

| Thing | Why it should not be carried as it is |
|---|---|
| `saves\` (four games' saves with checkpoints) | the owner's; by his rule a save lies in the folder of the build that played it. `.gitignore` leaves `saves/` out already |
| `m5c-c Notes.txt` | the owner's notes on game 9 |
| `.mcp.json` | identical to the gate's; nothing to carry |
| `CHANGES-m5c-c.md` | the folder's own account. Its substance belongs in the decisions log and the work-packages document, where most of it already is |
| **The build's name**, `BUILD_NAME = "m5c-c/37g"` in `freesail/core/world.py` | it names this folder. It is set by hand at each package or gate, so the repository sets its own. **Nine test lines spell it out** and must move with it: `tests/test_checkpoint.py` lines 218, 230 and 255, and `tests/test_replay.py` lines 251, 264, 334, 389, 406 and 433. (The lines there that say `m5c-c/37d` name the stamp inside 37d's fixture and stay.) Note that the second pass of 37g changed the code and did not change the name |
| The folder's name in the documents | `FreeSail-gate-m5c-c` or `m5c-c` is written in `docs/gates/gate-m5c.md`, `docs/DesignProposal.md`, `docs/dev/M5-WorkPackages.md` and `docs/dev/TuningNotes.md` |
| The review folder, `docs/playtests/2026-10-05-gate-5c-review/` | not in the zip. It is the same in both folders. Whether the repository takes it is the owner's to say: `report.md`, the readers' papers and the two chat transcripts under `evidence/` quote models' journals and the owner's typed lines at length; `drafts/` holds working papers |
| The two playtest saves under `tests/fixtures/saves/` | the changes file already leaves this to the owner. Two things it does not say are in 3.9 |
| The four free scenario files under `data/scenarios/` | the owner's, written at m5c and not in the zip. They are harmless, but see the fingerprint in 3.9 |
| Caches | `__pycache__` folders throughout and `.ruff_cache` at the root |

### 3.9 Four traps at the merge

1. **`.gitignore` will leave the fixture saves out without a word.** Its line `saves/` has no
   leading slash, so it matches a folder of that name at any depth, `tests/fixtures/saves/`
   included. A plain `git add` will not take the three kept saves, the package's own
   scripted one among them. The tests of the two playtest saves then skip, as written, and
   the tests of the package's own save fail, saying "restore it from the
   repository" (R: `tests/test_checkpoint.py::_the_37d_save`). So the promise in the
   changes file ("each must load from its checkpoint, run on and save again, on every
   build from now on") would lapse for the two playtest saves with nobody told. It needs an exception in `.gitignore` or the fixtures moved to a folder with
   another name. (R: `.gitignore`; I ran no git command, so this is from the rule as git
   documents it.)
2. **The fingerprint of the rules takes in every file under `data/` but the chart's tiles**
   (R: `core/world.py::fingerprint_of`), the owner's four free scenarios among them. Adding,
   leaving out or editing any scenario file makes a different build by that test. That is
   as the brief asked ("the data a replay reads"), and its consequence should be known: once
   the work is in the repository no save made in this folder is "this build's", so games 9
   and 10 load from their checkpoints and are refused a replay unless `--replay-anyway` is
   given. All four of the owner's saves here do load from their checkpoints on the build as
   it stands (P: `saves_check.py`; I ran no tick on them).
3. **A test pins the bytes of the fixture brief**: `tests/test_officer.py` line 1509 expects
   `tests/fixtures/ConsentBrief-before-37g.md` to have the digest `f667a04e00b32e1f`. The
   file has Unix line endings. A checkout that turns them into Windows ones would fail that
   test. The rules' fingerprint folds line endings; the consent digest does not.
4. **`docs/agents/ConsentBrief.md` must arrive unchanged in its watched sections.** One
   model has now answered against it (digest `288d0b18e34d76a8`, P). The rule compares the
   words of six sections and not the digest, so a re-wrapped line asks nobody again, but
   any change of a word in those sections asks every identity again, that one included.

## Part 4. Where the claims and the code part company

Most serious first. "The changes file" is `CHANGES-m5c-c.md`; "the review" is `report.md`.

### 4.1 The disagreements

**C1. The cruise's lost meeting is put down to the wrong cause, and the cure that is named
does not bring it back.** The changes file (37f, "The naval cruise"), the mark on
`test_the_naval_cruise_speaks_the_stranger` and the review's status block all say that the
book orders "a course that lies across the wind from her head; the helm takes her straight
through the wind, every sail aback", and that mending the chase order so that it wears her,
or the scenario's hours, would bring the meeting back. I sailed it (Part 2, 2.4). She is not
taken through the wind. She is turned 175 degrees the other way, by the stern, with her
yards left braced for the old tack, and is caught aback with the wind on her quarter. The
guard that wears her for a course across the wind's eye is in the code already and rightly
did not fire. A mend of the kind the mark names, tried in memory, did not bring the brig
back, nor did a second of my own, nor the two together; she was lost by 08:01 each time. Putting the brig where the scenario file's own comment
says she was meant to be, with no change to the code, did: within hail at 08:21. Half an
hour earlier still, the first chase order had put the frigate on the tack that led away
from the chase, and nobody has written that down either. *Why it is serious:* the cruise is
one of the two passages the gate is about, the owner is about to close the gate, and a
builder handed the mark's account would mend the wrong thing.

**C2. The cruise as pinned holds two urgent "Taken aback" lines and one failed wear in
its first 27 hours, which is as far as I read it; the record admits one of each.** Tick 83957, two minutes after the admiral's letter is read, is
the same handling fault as tick 91954. The cruise's test checks that she is never aground
and never drags; it does not look for a ship taken aback, so the suite is content. The
fault itself is not this week's (the chase code is the gate's own, D), but the week's work
is what brought the frigate to the places where it bites.

**C3. The gate's document describes the gate as cut, not the build.** Its two suite lines,
both passages' times and words, and items 1, 2, 10 and 13 are stale (Part 2, 2.1). Its item
12 passes as written, because the command it gives selects eleven tests and neither of the
two lost beats is among them. Its sentence "the seven are your rulings" now covers seven of
nine. None of this is hidden: nobody claimed the gate's text had been brought up to date.
It is here because the owner will read that text when he closes the gate.

**C4. "Each must load from its checkpoint, run on and save again, on every build from now
on."** True in this folder (T: the tests of the three kept saves pass). It will stop being
true in the repository unless something is done, for a reason the changes file does not
give: `.gitignore`'s `saves/` matches `tests/fixtures/saves/` (Part 3, 3.9). The changes
file does say that the two playtest saves wait on the owner's word and that their tests
skip without them. With the files missing those tests skip, and the tests of the package's
own save fail with the words "restore it from the repository" (R:
`tests/test_checkpoint.py::_the_37d_save`).

**C5. One consent record is in neither folder that will be diffed.** The changes file says
Opus 5.5's record of 3 October was left in m5c-b because it is not part of m5c-b's diff.
That is so (D). The consent brief promises each model that its record is kept in the
repository (Part 3, 3.7). The same paragraph of the changes file calls the review folder
here "a copy ... as it stood on 2026-10-06" with the original in m5c; the two are kept in
step and are identical today (D).

**C6. The general authority keeps back more than the list on record.** The owner approved
four heads on 7 October (the port's business, his standing orders, a new destination, what
cannot be undone) and the decisions log, decision 36, records those four. The brief of 37g
added a fifth (the reckoning set by hand). The code keeps back those five and four more: a
chase, the tide allowed in the reckoning, sending for a person, and the captain's own
going below and coming on deck (R: `freesail/agents/agent.py`, `_KEPT_BACK` and
`GENERAL_KEPT_BACK_WORDS`). The changes file says so plainly, twice, and says the second
pass "closes the point". What the second pass closed is the wording: the three places that
state the list now agree with one another and with the code. I found no ruling of the
owner's on the additions. A chase was on his own list under "when Milestone 7 comes".
It is a small thing, and it is the owner's.

**C7. The review's account of game 10, where I could check it.** Six of its statements about
the build were tried against the build:

| The review says (section 11) | What I found |
|---|---|
| A course with a half point is read as its last word | Borne out. `steer south by west half west` is answered "Helm ordered: steer west; W (270°)" (P) |
| The last save replays one line short, at a stand-down by the door | Borne out exactly. Replayed in memory on the build that wrote it: 4,239 lines against 4,240, the ship in the same place; the line missing is at tick 183600, "A notable event that speaks of danger: The Nut Rock ... the officer of the watch is sampled again" (P: `saves_check.py`). That line is one of 37g's own new ones |
| The handover note is asked for too late, and tokens are counted at four characters | Borne out in the code. The note is asked for at the context less 14,000 tokens when that is past six tenths: 88,400 of 102,400, where before 37g it was 61,440 (R: `harness.py::handover_threshold`). The runner counts four characters to a token and never reads why a reply ended (R: `local.py`; no use of the server's `finish_reason` or its token counts) |
| `Let go the sheet anchor` was accepted and failed four minutes later | True only when the hands are at other work. With nothing in hand the cutter refuses it at once: "no anchor aboard answers to 'sheet'". Given while she was getting under way it was accepted (P: `probe_orders.py`, `probe2.py`) |
| A standing order's action is not read when it is given | Half true. The action's first word is read: `then lett go the anker` is refused at entry. The rest is not: `then take a fix as soon as a bearing can be taken`, `then take a bearing of the moon made of cheese` and `then let go the sheet anchor` were all entered in the book (P) |
| An anchor left aweigh by a belay can be neither let go nor weighed | Not reproduced: my belay came before the anchor was aweigh, and she was then simply at anchor (P). Not checked further |

**C8. The number in the one rule is two where the brief said three.** Disclosed by the
builder, with the reason (R: `reckoning.py`, `OBSERVATION_OUT_SIGMAS = 2.0`). It is the rule
that took the cast a mile off in game 10, and that lays the cruise's account on a
chronometer more than five miles out at 09:00 with the land in sight (P: my run, tick
10800). With three, by the builder's note, game 9's noon sight would not be taken. So the
number is doing two jobs; the review's 11.6 proposes to take casts out from under it.

**C9. The watcher is told of three tools it is refused, not two.** The second pass's note
names `hand_over` and `handover_note`. The watcher's brief as sent also lists
`submit_order` among "the tools you have" (P: the briefs written out afresh, which are byte
for byte the review's `evidence/station-briefs-after-37g-second-pass.txt`).

**What I checked and found as claimed**, so that the list above is not read as the whole
picture:

- The suite's last line and the linter's (2.5).
- Every "Files changed" list in the changes file, against the snapshots (3.2).
- m5c-b applied byte for byte (3.2).
- The consent brief untouched by 37d, 37e and 37f; revised by 37g and its second pass;
  its digest `288d0b18e34d76a8`; its body 1,371 words; the body found whole in the approved
  draft (`drafts/consent-brief-lean-draft.md`).
- The eighteen consent records that were there before, unchanged by a byte.
- The re-ask: six identities owe the question, three with five sections named and three
  with four; the seventh has answered against the brief as it stands.
- The stations' briefs as a model is sent them are the review's evidence file to the byte.
- All four of the owner's saves here load from their checkpoints; game 10's two are this
  build's own (the same fingerprint of the rules), so nothing in the code or the data has
  changed since they were played.
- Game 9's and game 10's saves carry the stamps the review says.

### 4.2 Advice, package by package

It is advice. The owner and the repository's session decide.

The packages cannot be taken apart from one another. Each was built on the one before, and
the recorded passages' constants in `tests/test_known_truths.py` were set again by 37d, 37e
and 37f in turn. To hold one is to hold every one after it. So the advice below is to take
all of it, with the changes named, and none of them is a reason to hold.

| Package | Advice | The named change, and why |
|---|---|---|
| **m5c-b (37b, 37c)** | **Take as it is**, inside the whole. | It is in the build unchanged. What the review found wrong in it (the opt-out path, the floor on the log's lines) was mended by 37g and 37f; m5c-b by itself should not be taken without them |
| **37d**, the saves and the sight of land | **Take, with two named changes at the merge.** | (1) Set `BUILD_NAME` for the repository and move the nine test lines that spell it (3.8). (2) Settle the fixture saves before the first commit: the owner's word on the two playtest saves, and an exception to `.gitignore` for the folder (3.9). Left by the package and still so: the dialect will not take cables ("'the nearest land' is compared in miles, not cables", P); `the port` and `the depth of water` still give the true figures, by the plan |
| **37e**, the account | **Take, with one named change before the next game near land in thick weather, and one piece of data.** | (1) A cast of the lead should not move the account beyond the account's own doubt (the review's 11.6, the account, items 1 and 2). It is the one fault of the week that made a sound position unsound in the owner's hands, twice. I did not test the proposed mend. (2) The cruise's scenario line (2.4). Its two lost beats are 37e's doing in the plain sense that the ship now sails as she should; neither is a reason to hold it. Known and left: the three measured figures the brief asked for and did not get (not re-measured by me); the master surer than he should be at anchor in the Bay of Brest; a chronometer further out than its stated doubt displacing a good account |
| **37f**, lying to and the ground | **Take, with the cruise's mark written again.** | The text on `test_the_naval_cruise_speaks_the_stranger` and the paragraph in the changes file should say what the ship does (C1), so that the mend goes to the right place. And the handling fault deserves a line of its own in the work-packages document: a large alteration of course given to the helm alone, by `give chase` or `shape a course for`, leaves a square-rigged ship's yards braced for the old tack. Found in play and not mended, by the review's account: an anchor left aweigh, an anchor she does not carry accepted when the hands are busy, a heave-to that backs a sail being handed |
| **37g**, the station's safety, the deck, the leaving and the grant, with its second pass | **Take, with one named change before a local model is seated again**, and one ruling. | (1) The handover's reserve. As built it took away the margin that game 7 ran on, and both seatings of game 10 ended for it (C7). Until the runner counts tokens by the server's own figure, either put the default back to a share of the context or seat local models with a larger `--handover-reserve`; the review suggests 30,000 and says it is untried. (2) The owner's word on what the general authority keeps back beyond his list (C6). The consent brief should go in exactly as it is (3.9, the fourth trap). Small and left: the replay one line short at a stand-down by the door; the watcher's list of tools; "put the helm over" in the officer's brief, which by the review is not an order (not checked by me) |
| **37h**, the pilot | Not written. | The schooner's pilot waits on it, and so does one of the nine expected failures |
| **The review's section 11 proposals** | Not built; nothing in the build was changed after game 10 (P). | They are the owner's to rule on. Of them, the half-point course is the one I would not leave: the order is accepted and the ship steers six and a half points from what was said, in silence |

### 4.3 For the owner to decide before the work is folded in

1. Whether the two playtest saves under `tests/fixtures/saves/` go into the repository. They
   are his own games of 4 and 3 October, a model's transcript and his typed lines included.
2. Whether the review folder goes in, whole or in part.
3. Whether Opus 5.5's consent record of 3 October is fetched from m5c-b, so that all eleven
   records made in play are in the repository as the brief says.
4. The additions to what the general authority keeps back (C6).
5. Whether the gate closes with the schooner's pilot still an expected failure, or waits
   for 37h.
6. Where the *Palinure* is put, or whether the scenario should place her from the frigate's
   own position; and whether the handling fault behind C1 and C2 is mended before the cruise
   is played for the gate, since a captain who types `steer NE` from SW by W will meet it.
7. The name the repository's build is to carry in its saves.

## Part 5. What I did not check, and why

- **Anything in play.** No browser, no server, no model. Every statement here about what
  was played, by whom and what it showed is the review's.
- **The review's sections 1 to 7 and 10.1 to 10.5.** I read its status block, sections 8, 9,
  10.6 and 11. Its findings about the first nine games were not set against their logs.
- **The fast tier of the suite.** It was collected and counted, not run; the whole suite was
  run once.
- **The bodies of most tests.** See the mark **T** above.
- **The documents against the code.** For the spec, the primer, `Harness.md` and
  `TuningNotes.md` I checked which packages changed them and read a few places. I did not
  check that what they now say is what the code does, nor the tables of reasons for the
  recorded constants.
- **The measured figures**: 37e's tables of the account's error and the master's doubt, the
  merchant's distance off the Mingan, the gate's "account against the truth", the brig's
  head against the wind hove to, the cost of the fingerprint at start, the tick rate.
- **The two passes of 37d and of 37g's first build apart.** There is one snapshot after each
  package, so a file changed in a second pass cannot be told from the first by content.
  The second pass of 37g is the difference between the last snapshot and today.
- **The fixture saves by stage.** The snapshots leave out every folder named `saves`, so the
  three kept saves are dated by their files' times (3, 4 and 6 October) and not by a
  snapshot.
- **`m5c-b.diff` as a diff.** I compared the files it produced.
- **Whether any commit was made.** I ran no git command.
- **Eight test workers**, which the changes file says die at random.
- **Game 10's remaining claims**: the anchor left aweigh (tried, not reproduced), the fog
  reading's sentence, "put the helm over", the drill's count, the cause of the cast's
  mile in the tide's height, the runner sending one request three times.
- **`the nearest land` in every sample; `read_log` past two hundred lines; a standing order
  written under a grant that has ended; an act at the tick of a seating.**
