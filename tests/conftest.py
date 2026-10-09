"""The suite in two tiers, and the days built once a run (package 32c).

**Two tiers.** The slow tier is the tests that sail a day or replay one, and every other
test that took `SLOW_THRESHOLD_S` or more (setup, call and teardown) on the build machine
(`--durations=0`; docs/dev/TuningNotes.md, package 32c, has the measurements). The
`slow` mark is applied here and never in a test file, by two rules:

- the fixtures a test uses (`item.fixturenames`): a test that reads one of `DAY_FIXTURES`,
  the module-scoped fixtures that sail a day, a passage, a gale or a sweep of headings
  and took the threshold or more to build;
- its node id: the other tests over the threshold, named in `SLOW_TESTS`.

`pytest` alone runs the fast tier and ends with a line saying how many slow tests it left
out; `pytest --slow` runs everything; `pytest -m slow` the slow tier alone. Tests chosen
on the command line by node id (`file.py::test_name`) or by `-k` run whatever their tier.

**The days built once.** A module-scoped fixture is built once in each worker that runs a
test using it, and xdist's default distribution spreads a module's tests across the
workers, so `-n 4` could sail the same day four times. Every test that uses a
module-scoped fixture of its own module is put in an `xdist_group` named for the fixture
(tests sharing any such fixture share one group), and `--dist loadgroup` (in
`pyproject.toml`'s `addopts`) sends each group whole to one worker: each fixture is built
once a run and every other test still spreads, one at a time.

A test renamed or a new long test is not caught by the node ids: re-measure with
`python -m pytest -n 4 --slow --durations=0` and bring `SLOW_TESTS` up to date when the
fast tier grows slow.
"""

from __future__ import annotations

import pytest

SLOW_THRESHOLD_S = 5.0  # judgement: the fast tier in a few minutes on four loaded cores

# Module-scoped fixtures by the file that defines them: each took over the threshold to
# build, and is charged to whichever of its tests happens to run first, so every test
# that reads one is slow whatever its own time.
DAY_FIXTURES: dict[str, frozenset[str]] = {
    "test_known_truths.py": frozenset(
        {
            "frigate_polar",
            "schooner_polar",
            "frigate_sweep",
            "schooner_sweep",
            "frigate_plain_sail",
            "frigate_yards_alike_sweep",
            "frigate_head_yards_sharper_sweep",
            "frigate_bowlines_sweep",
            "frigate_catharpins_sweep",
            "frigate_lying_a_try",
            "frigate_rising_gale",
            "gate_day",
            "gate_system_day",
            "gate_5a_day",
            "gate_5b_passage",
            "gate_5b_schooner",  # package 37e: the schooner's passage, read by two tests
            "gate_5c_merchant",  # package 36: the merchant passage, 36 hours
            "gate_5c_cruise",  # package 36: the naval cruise, 48 hours
        }
    ),
    "test_ships_hierarchy.py": frozenset(
        {
            "frigate_sweep",
            "schooner_sweep",
            "cutter_sweep",
            "brig_sweep",
            "frigate_polar",
            "cutter_polar",
            "brig_polar",
        }
    ),
    "test_checkpoint.py": frozenset({"saved"}),
    "test_routine.py": frozenset({"a_day"}),
    "test_staying.py": frozenset({"frigate_by_the_wind"}),
    "test_studding.py": frozenset({"brought_up"}),
}

# The other tests at or over the threshold: the mean of two whole-suite runs at `-n 4`
# on the build machine with three other suites running beside them (2026-10-01).
SLOW_TESTS: frozenset[str] = frozenset(
    {
        "test_agent_api.py::test_a_game_with_a_remote_agent_replays_to_the_same_digest",
        "test_agent_api.py::test_a_station_the_game_mans_itself_is_refused_and_a_loaded_games_is_taken_over",
        "test_agent_api.py::test_a_whole_session_through_the_routes",
        "test_agent_api.py::test_lockstep_holds_the_clock_while_the_door_has_the_floor",
        "test_agent_api.py::test_the_long_poll_waits_without_holding_the_worlds_lock",
        "test_agent_api.py::test_what_happens_while_the_model_holds_the_floor_is_folded_into_its_turn",
        "test_agents.py::test_a_door_that_leaves_out_old_turns_sends_the_first_kept_with_every_reading",
        "test_agents.py::test_a_game_with_an_agent_replays_to_the_same_digest_with_the_agent_stationed_late",
        "test_agents.py::test_a_live_game_with_late_replies_replays_to_the_same_digest",
        "test_agents.py::test_a_paused_watcher_is_stood_down_by_ten_real_minutes_only_on_the_servers_clock",
        "test_agents.py::test_a_sample_after_the_first_carries_only_what_changed_and_the_sails_in_one_line",
        "test_agents.py::test_live_sampling_folds_what_happens_while_the_model_has_the_floor",
        "test_agents.py::test_samples_bundled_into_an_open_turn_share_one_copy_of_what_is_common",
        "test_agents.py::test_the_agent_log_kinds_are_listed_in_one_place_and_used",
        "test_agents.py::test_the_console_stations_the_scripted_watcher_and_prints_its_lines",
        "test_agents.py::test_the_journal_is_saved_with_the_game_shown_on_request_and_present_in_a_replay",
        "test_agents.py::test_the_sail_line_names_the_ships_groups_and_says_every_sail",
        "test_agents.py::test_truth_43_repeating_after_the_nudge_pauses_with_the_human_asked_then_stands_down",
        "test_agents.py::test_truth_43_the_human_answers_a_pause_with_resume_or_stand_down",
        "test_agents.py::test_truth_45_two_lockstep_runs_with_the_same_fake_and_seed_give_the_same_digest",
        "test_agents.py::test_what_the_captain_has_the_model_can_get_from_its_samples",
        "test_canvas.py::test_the_same_seed_gives_the_same_log_with_canvas_work",
        "test_canvas.py::test_truth_27_with_the_ship_files_ratings",
        "test_canvas.py::test_worn_canvas_goes_before_its_spar_and_new_canvas_holds_until_the_spar_goes",
        "test_catalogue.py::test_backing_and_filling_keeps_her_place_and_leaves_her_lying_to",
        "test_catalogue.py::test_box_hauling_brings_her_round_on_her_heel",
        "test_catalogue.py::test_lying_a_try_in_a_gale_with_the_topgallant_masts_down",
        "test_catalogue.py::test_scudding_puts_the_wind_on_the_quarter",
        "test_catalogue.py::test_sending_down_the_topgallant_masts_at_once_loses_nothing_in_thirty_minutes",
        "test_catalogue.py::test_the_gale_carries_away_the_royals_without_sending_anything_down",
        "test_catalogue.py::test_the_other_three_box_haul_too[data/ships/brig.yaml]",
        "test_catalogue.py::test_the_other_three_wear_and_heave_to[data/ships/brig.yaml]",
        "test_catalogue.py::test_the_other_three_wear_and_heave_to[data/ships/cutter.yaml]",
        "test_catalogue.py::test_the_other_three_wear_and_heave_to[data/ships/topsail-schooner.yaml]",
        "test_chart.py::test_a_save_on_the_chart_replays_to_the_same_digest",
        "test_chart.py::test_she_takes_the_ground_and_the_log_says_so_once_and_comes_off_again",
        # package 37d: the kept saves run on a watch (a glass in the fast tier)
        "test_checkpoint.py::test_a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_watch[m5c-b-harpy-tick602100]",
        "test_checkpoint.py::test_a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_watch[m5c-cutter-tick34091]",
        "test_checkpoint.py::test_the_packages_own_save_loads_from_its_checkpoint_and_runs_on_a_watch",
        "test_crew_orders.py::test_close_reef_takes_every_reef_band",
        "test_crew_orders.py::test_pipe_down_is_refused_while_the_hands_are_about_ship",
        "test_evolutions.py::test_a_parted_sheet_is_rove_afresh_from_the_coil_and_the_sail_set_again",
        "test_evolutions.py::test_a_splice_costs_no_cordage_and_leaves_the_line_an_eighth_the_weaker",
        "test_evolutions.py::test_reeving_is_refused_in_words_for_a_sound_line_standing_rigging_and_an_empty_store",
        "test_hands.py::test_a_reef_short_of_its_party_begins_short_and_fills_as_hands_come_free",
        "test_hands.py::test_belaying_a_tack_is_not_the_tacks_belay_and_the_work_it_held_resumes",
        "test_hands.py::test_compatibility_one_evolution_with_the_watch_on_deck[fill_away]",
        "test_hands.py::test_compatibility_one_evolution_with_the_watch_on_deck[heave_to]",
        "test_hands.py::test_compatibility_one_evolution_with_the_watch_on_deck[tack]",
        "test_hands.py::test_compatibility_one_evolution_with_the_watch_on_deck[wear]",
        "test_hands.py::test_tack_ship_belays_the_topgallant_being_set_and_it_resumes_after",
        "test_hands.py::test_the_runner_does_not_pipe_down_when_the_captain_called_all_hands",
        "test_hands.py::test_three_topsails_are_reefed_together_each_up_to_its_party_and_the_surplus_goes_on",
        "test_known_truths.py::test_shorten_sail_takes_in_the_topgallants_while_the_reef_is_taken_and_the_reef_speeds_up",
        "test_known_truths.py::test_the_cutter_and_the_brig_sail_through_the_same_orders[data/ships/brig.yaml]",
        "test_known_truths.py::test_the_cutter_and_the_brig_sail_through_the_same_orders[data/ships/cutter.yaml]",
        "test_known_truths.py::test_the_pace_on_the_day_under_systems_holds_truth_51s_floor",
        "test_known_truths.py::test_the_pace_on_the_gates_day_with_the_region_loaded_holds_truth_51s_floor",
        "test_known_truths.py::test_the_passage_in_thick_weather_makes_its_landfall_wrong_on_the_reckoning",
        "test_known_truths.py::test_the_schooner_sails_the_passage_with_her_octant_and_the_log_every_two_hours",
        "test_known_truths.py::test_truth_10_she_misses_stays_when_put_about_under_three_knots",
        "test_known_truths.py::test_truth_10_the_frigate_tacks_in_five_to_ten_minutes_and_gains_to_windward",
        "test_known_truths.py::test_truth_11_the_frigate_wears_in_six_to_twelve_minutes",
        "test_known_truths.py::test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward",
        "test_known_truths.py::test_truth_12_backing_the_main_topsail_stops_the_ship",
        "test_known_truths.py::test_truth_12_she_fills_away_without_hanging_aback",
        "test_known_truths.py::test_truth_13_a_gaff_sail_wants_squaring_off_before_the_wind",
        "test_known_truths.py::test_truth_14_studding_sails_do_not_help_close_hauled",
        "test_known_truths.py::test_truth_14_studding_sails_help_on_a_broad_reach",
        "test_known_truths.py::test_truth_15_the_same_seed_gives_the_same_log",
        "test_known_truths.py::test_truth_16_tactical_diameter_at_eight_knots",
        "test_known_truths.py::test_truth_19_a_tack_belays_the_royals_being_set_and_they_resume_after",
        "test_known_truths.py::test_truth_20_a_night_of_all_hands_slows_the_morning_watch",
        "test_known_truths.py::test_truth_22_same_seed_same_muster_same_log_and_a_replay_reproduces_it",
        "test_known_truths.py::test_truth_23_sending_down_the_topgallant_masts_in_time_saves_the_royals",
        "test_known_truths.py::test_truth_25_pinched_to_five_points_she_makes_less_to_windward_than_kept_full",
        "test_known_truths.py::test_truth_27_a_worn_royal_blows_out_before_its_yard_goes_and_a_new_one_does_not",
        "test_known_truths.py::test_truth_29_studding_sails_flog_and_strain_at_six_points_and_draw_at_nine",
        "test_known_truths.py::test_truth_30_studding_sails_both_sides_running_gain_most_of_a_knot",
        "test_known_truths.py::test_truth_31_the_catharpins_brace_the_main_yard_four_degrees_sharper_and_rate_it_down",
        "test_known_truths.py::test_truth_33_one_yard_braced_away_from_its_neighbours_is_refused_and_the_mast_is_not",
        "test_known_truths.py::test_truth_34_at_sunrise_the_royals_are_set_again_only_under_twenty_knots[15.0-True]",
        "test_known_truths.py::test_truth_34_at_sunrise_the_royals_are_set_again_only_under_twenty_knots[25.0-False]",
        "test_known_truths.py::test_truth_34_at_sunset_the_night_routine_takes_in_the_light_sails_and_nothing_else",
        "test_known_truths.py::test_truth_35_shorten_sail_fires_once_after_two_minutes_over_thirty_and_not_on_a_gust",
        "test_known_truths.py::test_truth_36_keep_her_full_bears_away_a_point_forward_of_fifty_five_and_stops",
        "test_known_truths.py::test_truth_36_over_an_hour_of_a_wandering_wind_it_fires_no_more_than_four_times",
        "test_known_truths.py::test_truth_38_the_captains_standing_order_stands_and_the_masters_is_countermanded",
        "test_known_truths.py::test_truth_51_the_frigate_under_the_starter_routines_ticks_at_the_build_machines_floor",
        "test_known_truths.py::test_truth_53_a_thousand_months_of_the_climatology_give_the_studys_direction_shares",
        "test_known_truths.py::test_truth_54_a_gust_is_within_1_3_of_its_mean_in_any_air_mass_and_a_squall_is_named",
        "test_known_truths.py::test_truth_55_the_weather_replays_tick_for_tick_and_the_pinned_wind_wins",
        "test_known_truths.py::test_truth_5_dead_before_the_wind_is_slower_than_four_points_off",
        "test_known_truths.py::test_truth_6_headsails_and_spanker_set_the_helm",
        "test_known_truths.py::test_truth_9_nothing_carries_away_in_twenty_knots_under_plain_sail[data/ships/frigate-36.yaml]",
        "test_known_truths.py::test_truth_9_nothing_carries_away_in_twenty_knots_under_plain_sail[data/ships/topsail-schooner.yaml]",
        "test_known_truths.py::test_truth_9_royals_and_topgallants_carry_away_in_thirty_five_knots",
        "test_local_runner.py::test_the_runner_asks_consent_through_the_game_then_keeps_watch_for_a_few_glasses",
        "test_mcp_server.py::test_a_game_with_an_mcp_watcher_replays_from_its_save_to_the_same_log",
        "test_mcp_server.py::test_a_held_call_sends_progress_until_the_turn_opens",
        "test_mcp_server.py::test_a_read_beside_a_held_call_is_answered_at_once",
        "test_mcp_server.py::test_a_result_cut_off_after_it_was_made_goes_to_the_next_call",
        "test_mcp_server.py::test_a_scripted_passage_of_three_glasses_with_the_clock_turned_by_the_game",
        "test_mcp_server.py::test_the_bridge_runs_over_stdio_against_a_game_on_a_local_port",
        "test_orders_m4a.py::test_steady_out_the_bowlines_re_hauls_them_after_falling_off_and_coming_up",
        "test_orders_m4a.py::test_the_starter_file_loads_in_the_console_with_the_well_refused_and_the_rest_entered",
        "test_orders_m4a.py::test_the_starter_file_loads_on_the_server_driver",
        "test_python_api.py::test_a_python_rule_saves_as_its_name_and_source_and_loads_listed_but_belayed",
        "test_python_api.py::test_a_when_rule_with_a_duration_fires_as_its_twin_does",
        "test_python_api.py::test_an_at_rule_with_a_condition_is_held_as_its_twin_is",
        "test_python_api.py::test_the_body_runs_once_at_registration_and_is_handed_the_readings",
        "test_python_api.py::test_truth_40_the_night_routine_in_python_and_in_the_dialect_give_one_log",
        "test_readings.py::test_a_reading_replaced_in_the_registry_reaches_rule_and_snapshot_alike",
        "test_readings.py::test_a_sail_shaking_and_aback_read_from_the_physics[frigate-36]",
        "test_readings.py::test_a_sail_shaking_and_aback_read_from_the_physics[topsail-schooner]",
        "test_readings.py::test_course_and_leeway_are_not_readings_with_no_way_on",
        "test_readings.py::test_readings_are_the_physics_own_numbers[frigate-36]",
        "test_readings.py::test_snapshot_reads_its_instruments_from_the_registry[frigate-36]",
        "test_readings.py::test_the_view_is_cached_per_tick_and_per_order",
        "test_reckoning.py::test_the_brig_hove_to_six_hours_of_a_spring_ebb_in_the_iroise_keeps_an_honest_account",
        "test_reckoning.py::test_the_captains_chart_carries_the_account_and_never_the_truth",
        "test_reckoning.py::test_the_hand_lead_and_the_deep_sea_lead_cast_with_their_words_and_the_ground",
        "test_reckoning.py::test_the_log_is_hove_hourly_in_the_frigate_and_two_hourly_in_the_schooner",
        "test_reckoning.py::test_the_noon_the_days_work_and_the_readings_since_noon",
        "test_reckoning.py::test_the_same_seed_gives_the_same_account_and_a_replay_the_same_digest",
        "test_reckoning.py::test_work_up_set_and_allow_and_shape_a_course_read_the_account_not_the_truth",
        "test_replay.py::test_a_crewed_voyage_replays_to_the_same_log_and_the_same_muster",
        "test_replay.py::test_truth_39_a_passage_under_the_starter_routines_replays_with_the_same_firings",
        "test_rig_geometry.py::test_a_mast_swiftered_in_is_rated_down_athwartships[data/ships/brig.yaml]",
        "test_rig_geometry.py::test_a_mast_swiftered_in_is_rated_down_athwartships[data/ships/frigate-36.yaml]",
        "test_rig_geometry.py::test_the_same_orders_give_the_same_log",
        "test_rollup.py::test_at_sixty_and_above_the_samples_carry_the_same_rollup_the_captain_reads",
        "test_rollup.py::test_below_sixty_the_samples_are_as_they_were",
        "test_rollup.py::test_the_console_prints_the_rollup_at_sixty_and_every_line_below",
        "test_rollup.py::test_the_server_sends_rollups_at_sixty_and_events_below",
        "test_rollup.py::test_the_server_takes_speed_to_three_hundred_and_serves_the_store_by_ticks",
        "test_routine.py::test_a_crewed_world_through_a_day",
        "test_routine.py::test_same_crew_same_clock_same_calls_same_notes_and_fatigues",
        "test_sea.py::test_a_reef_takes_half_as_long_again_in_a_heavy_sea_as_in_a_smooth_one",
        "test_sea.py::test_a_standing_order_on_the_sea_fires_as_the_sea_gets_up",
        "test_sea.py::test_the_hull_loses_speed_in_a_head_sea_by_a_small_factor",
        "test_sea.py::test_the_log_says_the_sea_when_its_words_change_and_the_rollup_says_it_by_the_hour",
        "test_sea.py::test_the_sea_is_deterministic_and_a_replay_raises_it_again",
        "test_sea.py::test_the_strain_reads_the_motion_as_an_extra_load_and_is_unchanged_in_a_smooth_sea",
        "test_sea.py::test_windage_under_bare_poles_is_measured_and_recorded",
        "test_server.py::test_snapshot_reflects_state_changes[frigate-36]",
        "test_sights.py::test_observe_the_sun_by_order_at_noon_and_refused_before_and_after",
        "test_standing.py::test_every_never_queues_more_than_one",
        "test_standing.py::test_firing_is_deterministic",
        "test_standing.py::test_strike_takes_an_order_out_of_the_book_and_belay_keeps_it",
        "test_standing.py::test_the_book_is_saved_with_the_game_and_restored_by_replay",
        "test_standing.py::test_the_dwell_waits_for_the_evolution_the_firing_started",
        "test_staying.py::test_a_sails_aback_line_waits_out_a_seas_period",
        "test_staying.py::test_tack_truth_the_brig_goes_about_as_a_ship_does",
        "test_staying.py::test_tack_truth_the_cutter_is_quicker_than_the_schooner",
        "test_staying.py::test_the_cutter_swings_twice_as_fast_as_the_frigate",
        "test_staying.py::test_the_frigate_hung_in_stays_is_boxed_through_in_a_light_breeze",
        "test_staying.py::test_the_frigate_misses_stays_under_three_knots_and_squares_the_yards_as_a_brace",
        "test_staying.py::test_the_starter_book_tends_the_sheets_every_glass",
        "test_staying.py::test_turning_truths_the_small_vessels_turn_in_their_own_lengths[brig-band2-fastest_band2]",
        "test_staying.py::test_turning_truths_the_small_vessels_turn_in_their_own_lengths[schooner-band0-fastest_band0]",
        "test_strain.py::test_nothing_carries_away_in_twenty_knots_under_plain_sail[data/ships/frigate-36.yaml]",
        "test_strain.py::test_ratio_of_the_weakest_part_on_the_reference_ships",
        "test_strain.py::test_something_carries_away_in_thirty_five_knots_under_all_sail",
        "test_strain.py::test_the_log_is_deterministic_with_gear_carrying_away",
        "test_studding.py::test_booms_alone_are_rigged_in_first",
        "test_studding.py::test_studding_sails_brought_up_are_deterministic",
        "test_studding.py::test_the_tack_takes_the_studding_sails_in_first[data/ships/frigate-36.yaml]",
        "test_studding.py::test_the_tack_without_studding_sails_is_as_it_was[data/ships/frigate-36.yaml]",
        "test_studding.py::test_the_wear_takes_the_studding_sails_in_first",
        "test_sun.py::test_a_whole_day_raises_each_event_once_and_deterministically",
        "test_sun.py::test_the_frigate_carries_the_same_sun",
        "test_sun.py::test_the_midnight_sun_raises_nothing_and_does_not_crash",
        "test_tell.py::test_a_game_with_a_standing_orders_word_replays_to_the_same_digest",
        "test_tell.py::test_a_game_with_a_tell_replays_to_the_same_digest",
        "test_tell.py::test_a_stand_by_in_answer_to_a_word_ends_the_turn_at_once",
        "test_trim_order.py::test_a_trims_braces_log_one_line_when_the_last_is_done",
        "test_trim_order.py::test_the_trim_line_says_the_yards_on_deck_as_a_clause_and_not_as_a_refusal",
        "test_weather.py::test_a_standing_order_on_the_glass_fires_when_it_falls",
        # package 37d: eighty-three minutes of the Harpy's own weather, a sample a second
        "test_weather.py::test_from_the_harpys_own_weather_the_wind_no_longer_turns_as_the_ship_moves",
        "test_weather.py::test_the_gate_day_file_carries_both_forms_and_the_pinned_wind_wins",
        "test_weather.py::test_the_readings_on_a_ship_with_a_glass_and_on_one_without",
        "test_weather_script.py::test_a_scenario_world_replays_from_its_save",
        "test_weather_script.py::test_a_veering_script_is_logged_as_a_veer_and_a_standing_order_sees_it",
        "test_weather_script.py::test_trim_on_a_shift_fires_at_each_point_of_a_steady_veer_and_not_on_the_gusts",
        "test_weather_script.py::test_trim_on_a_shift_while_a_trim_is_in_hand_is_folded_not_stacked",
        # Packages 33b to 33d's tests, written beside this package and measured on the
        # lead's branch (ed865ca) on a quieter machine, where the bar above is about 2.3 s
        # (the whole suite ran 2.2 times faster than in the two runs above).
        "test_known_truths.py::test_truth_60_the_chronometer_within_four_miles_and_a_lunar_shows_it_gaining",
        "test_known_truths.py::test_truth_61_the_lunar_is_refused_in_words_that_say_which_and_answers_within_a_degree",
        "test_longitude.py::test_a_bearing_steady_and_closing_is_hailed_for_a_danger_and_the_chart_edge_said",
        "test_longitude.py::test_the_chronometer_is_the_scenarios_and_keeps_greenwich_time_with_its_error",
        "test_longitude.py::test_the_lunar_occupies_the_master_and_two_mates_and_answers_an_hour_later",
        "test_longitude.py::test_the_master_winds_it_at_eight_and_a_forgotten_one_runs_down",
        "test_orders_m4a.py::test_the_starter_file_loads_in_the_console_with_the_well_held_and_the_rest_entered",
        "test_server.py::test_ease_on_station_eases_the_clock_on_a_sample_and_says_so",
        "test_standing.py::test_she_is_hove_to_from_the_heave_to_until_she_fills_away",
        "test_standing.py::test_the_well_is_held_in_the_book_and_never_fires",
        # package 37f: six hours hove to for each ship, the watch's hands at the tending,
        # the starter book asleep through a heave-to, the Goulet's eight hours at anchor,
        # and a standing order held through two watches (measured at `-n 4`)
        "test_lying_to.py::test_held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam[data/ships/brig.yaml]",
        "test_lying_to.py::test_held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam[data/ships/cutter.yaml]",
        "test_lying_to.py::test_held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam[data/ships/frigate-36.yaml]",
        "test_lying_to.py::test_held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam[data/ships/topsail-schooner.yaml]",
        "test_lying_to.py::test_the_starter_books_trim_rules_sleep_through_a_heave_to_and_wake_after_it",
        "test_lying_to.py::test_the_tending_costs_the_watch_its_hands_and_the_relief_takes_them_over",
        "test_log_lines.py::test_a_standing_order_with_nothing_to_do_says_so_once_a_watch_for_each_reason",
        "test_tackle_orders.py::test_the_goulets_eight_hours_give_at_most_five_lines_the_first_urgent",
        # package 37h: the pilot's hail answered and unanswered, his boat in company with a
        # fast ship, and his leaving at the anchor, each an hour or more of sailing
        "test_ports.py::test_the_pilot_unanswered_keeps_company_hails_once_more_and_bears_away",
        "test_ports.py::test_the_pilot_declined_at_his_hail_is_sent_back_and_no_pilot_comes",
        "test_ports.py::test_a_fast_ship_is_hailed_to_shorten_sail_and_the_boat_keeps_company_until_she_does",
        "test_ports.py::test_hail_the_pilot_hails_his_boat_in_sight_and_takes_him",
        "test_ports.py::test_the_pilot_is_put_off_at_the_anchor_and_the_pilotage_paid_once",
    }
)

SLOW_HINT = "run them with: python -m pytest --slow (the slow tier alone: -m slow)"

_LEFT_OUT = pytest.StashKey[int]()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run the slow tier too: the days sailed and replayed and the long tests "
        "(tests/conftest.py)",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.stash[_LEFT_OUT] = 0


def _is_slow(item: pytest.Item) -> bool:
    if DAY_FIXTURES.get(item.path.name, frozenset()).intersection(item.fixturenames):
        return True
    return item.nodeid.removeprefix("tests/") in SLOW_TESTS


def _module_fixture_keys(item: pytest.Item) -> list[str]:
    """The module-scoped fixtures defined in the test's own module that it uses, each
    with its parameter's index when the fixture is parametrised (each parameter is a
    fixture built of its own)."""
    info = getattr(item, "_fixtureinfo", None)
    if info is None:
        return []
    module_id = item.nodeid.split("::", 1)[0]
    callspec = getattr(item, "callspec", None)
    keys = []
    for name in item.fixturenames:
        defs = info.name2fixturedefs.get(name)
        if not defs:
            continue
        fixturedef = defs[-1]
        if fixturedef.scope != "module" or fixturedef.baseid != module_id:
            continue
        key = f"{item.path.name}::{name}"
        if callspec is not None and name in callspec.indices:
            key += f"[{callspec.indices[name]}]"
        keys.append(key)
    return keys


def _group_by_shared_fixtures(items: list[pytest.Item]) -> None:
    """Join the module-scoped fixtures that any one test uses together, so that one group
    holds every test touching any of them, and mark each such test with its group."""
    parent: dict[str, str] = {}

    def find(k: str) -> str:
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    keyed = []
    for item in items:
        keys = _module_fixture_keys(item)
        if not keys:
            continue
        keyed.append((item, keys))
        for k in keys:
            parent.setdefault(k, k)
        root = find(keys[0])
        for k in keys[1:]:
            other = find(k)
            if other != root:
                root, other = sorted((root, other))
                parent[other] = root
    for item, keys in keyed:
        item.add_marker(pytest.mark.xdist_group(find(keys[0])))


def _chosen_on_the_command_line(config: pytest.Config) -> bool:
    """Tests picked by node id or by `-k` run whatever their tier: whoever names a test
    wants it run (the gate reports name truths so)."""
    return bool(config.getoption("keyword")) or any("::" in str(a) for a in config.args)


# First, so that the marks are in place before `-m` selects and before xdist's worker
# writes the groups into the node ids.
@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        if _is_slow(item):
            item.add_marker(pytest.mark.slow)
    run_slow = (
        config.getoption("--slow")
        or "slow" in (config.getoption("markexpr") or "")
        or _chosen_on_the_command_line(config)
    )
    if not run_slow:
        left_out = [i for i in items if i.get_closest_marker("slow") is not None]
        if left_out:
            items[:] = [i for i in items if i.get_closest_marker("slow") is None]
            config.hook.pytest_deselected(items=left_out)
            config.stash[_LEFT_OUT] = len(left_out)
            if hasattr(config, "workerinput"):  # an xdist worker: the controller says it
                config.workeroutput["freesail_slow_left_out"] = len(left_out)
    _group_by_shared_fixtures(items)


# Under xdist the controller collects nothing: the workers' count comes back with them.
@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(node, error) -> None:
    left_out = (getattr(node, "workeroutput", None) or {}).get("freesail_slow_left_out", 0)
    stash = node.config.stash
    stash[_LEFT_OUT] = max(stash.get(_LEFT_OUT, 0), left_out)


def pytest_unconfigure(config: pytest.Config) -> None:
    """The fast tier's last line, after pytest's own summary (on the controller only)."""
    left_out = config.stash.get(_LEFT_OUT, 0)
    if not left_out or hasattr(config, "workerinput"):
        return
    reporter = config.pluginmanager.get_plugin("terminalreporter")
    if reporter is None:
        return
    tests = "test" if left_out == 1 else "tests"
    reporter.write_line(f"fast tier: {left_out} slow {tests} left out; {SLOW_HINT}")
