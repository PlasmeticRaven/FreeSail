SC = "freesail/evolutions/scripts.py"
ST = "freesail/orders/storm.py"
OI = "freesail/orders/__init__.py"
K = "tests/test_known_truths.py::"
T = ["tests/test_evolutions.py", "tests/test_ship_loader.py::test_slack_in_stays_is_a_habit_her_file_may_give_false_by_default_and_refused_else",
     "tests/test_captains.py::test_a_jib_kept_at_its_limit_is_taken_in_at_its_first_strain_whatever_the_wind",
     "tests/test_captains.py::test_a_jib_kept_at_its_limit_is_taken_in_by_the_captain_before_it_goes",
     "tests/test_diana.py::test_truth_7_664_shortened_in_25_knots_her_jib_is_left_on_her_and_she_stays",
     "tests/test_diana.py::test_truth_7_664_shortened_in_25_knots_she_gripes_without_her_jib",
     "tests/test_diana.py::test_truth_7_664_shortened_in_25_knots_with_her_jib_set_again_she_stays"] + [K + n for n in (
    "test_truth_7_760_no_ship_tacks_worse_than_she_did",
    "test_truth_7_763_a_ship_known_slack_in_stays_hauls_with_the_wind_ahead_any_other_at_the_point",
    "test_truth_7_763b_a_ship_known_slack_in_stays_is_said_so_in_the_ship",
    "test_truth_7_764_a_tack_that_falls_back_is_said_to_have_missed_stays",
    "test_truth_7_765_a_fore_and_afters_failed_tack_is_said_as_she_lies",
    "test_truth_7_766_the_jib_she_cannot_be_held_without_is_left_on_her_and_said",
    "test_truth_7_767_a_jib_over_its_rating_is_taken_in_and_the_players_order_obeyed",
    "test_truth_7_767b_a_kept_jib_is_kept_once_at_its_limit_and_its_strain_names_its_order",
    "test_truth_7_768_a_jib_the_storm_canvas_shifts_is_taken_in_as_before_and_never_said_kept",
    "test_truth_7_769_a_loaded_jib_her_helm_can_do_without_is_taken_in",
    "test_truth_7_761_the_fleet_goes_about_under_plain_sail")]
FB = '''                    if self.sign * rel > 2 * POINT:
                        self._miss_stays("she came through the wind and fell back on her old tack")
                        return
'''
IR = '''                    if abs(rel) <= 2 * POINT:
                        self._miss_stays("she lies in irons, her head in the wind")
                        return
'''
MUTANTS = [
    ("M01-haul-frac-0", SC, "HAUL_WAY_FRACTION = 0.4", "HAUL_WAY_FRACTION = 0.0", T),
    ("M02-haul-frac-1", SC, "HAUL_WAY_FRACTION = 0.4", "HAUL_WAY_FRACTION = 1.0", T),
    ("M03-wind-ahead-a-point", SC, "WIND_AHEAD_RAD = math.radians(0.5)", "WIND_AHEAD_RAD = math.radians(11.25)", T),
    ("M04-fell-back-branch-removed", SC, FB, "", T),
    ("M05-irons-branch-removed", SC, IR, "", T),
    ("M06-fell-back-bound-6-points", SC, FB, FB.replace("2 * POINT", "6 * POINT"), T),
    ("M07-irons-bound-1-point", SC, IR, IR.replace("2 * POINT", "1 * POINT"), T),
    ("M08-helm-share-0", ST, "HELM_IN_HAND_SHARE = 0.25", "HELM_IN_HAND_SHARE = 0.0", T),
    ("M09-helm-share-1", ST, "HELM_IN_HAND_SHARE = 0.25", "HELM_IN_HAND_SHARE = 1.0", T),
    ("M10-under-rating-dropped", ST, "if sail.load_kn / rating < 1.0 and wanted >", "if wanted >", T),
    ("M11-kept-counted-strained", ST, " not in before and sl not in kept", " not in before", T),
    ("M12-kept-words-dropped", OI, '            text += " " + storm.kept_jibs_words(ship, kept)', "            pass", T),
    ("M13-helm-without-sign", ST, "    to_windward = -1.0 if d.apparent_wind_angle >= 0 else 1.0",
     "    to_windward = 1.0 if d.apparent_wind_angle >= 0 else -1.0", T),
    ("M14-slack-in-stays-inverted", SC, '        if not getattr(spec, "slack_in_stays", False):',
     '        if getattr(spec, "slack_in_stays", False):', T),
]
