SC = "freesail/evolutions/scripts.py"
ST = "freesail/orders/storm.py"
OI = "freesail/orders/__init__.py"
K = "tests/test_known_truths.py::"
T = ["tests/test_evolutions.py"] + [K + n for n in (
    "test_truth_7_760_no_ship_tacks_worse_than_she_did",
    "test_truth_7_761_the_fleet_goes_about_under_plain_sail",
    "test_truth_7_762_the_fleet_goes_about_shortened",
    "test_truth_7_763_a_slack_ship_hauls_with_the_wind_ahead_a_smart_one_at_the_point",
    "test_truth_7_764_a_tack_that_falls_back_is_said_to_have_missed_stays",
    "test_truth_7_765_a_fore_and_afters_failed_tack_is_said_as_she_lies",
    "test_truth_7_766_the_jib_she_cannot_be_held_without_is_left_on_her_and_said",
    "test_truth_7_767_a_jib_over_its_rating_is_taken_in_and_the_players_order_obeyed")]
MUTANTS = [
    ("M01-haul-frac-0", SC, "HAUL_WAY_FRACTION = 0.4", "HAUL_WAY_FRACTION = 0.0", T),
    ("M02-haul-frac-1", SC, "HAUL_WAY_FRACTION = 0.4", "HAUL_WAY_FRACTION = 1.0", T),
    ("M03-wind-ahead-a-point", SC, "WIND_AHEAD_RAD = math.radians(0.5)", "WIND_AHEAD_RAD = math.radians(11.25)", T),
    ("M04-fell-back-branch-removed", SC,
     '''                    if self.sign * rel > 2 * POINT:
                        self._miss_stays("she came through the wind and fell back on her old tack")
                        return
''', "", T),
    ("M05-irons-branch-removed", SC,
     '''                    if abs(rel) <= 2 * POINT:
                        self._miss_stays("she lies in irons, her head in the wind")
                        return
''', "", T),
    ("M06-fell-back-bound-6-points", SC,
     '''                    if self.sign * rel > 2 * POINT:
                        self._miss_stays("she came through''',
     '''                    if self.sign * rel > 6 * POINT:
                        self._miss_stays("she came through''', T),
    ("M07-irons-bound-1-point", SC,
     "                    if abs(rel) <= 2 * POINT:\n                        self._miss_stays(\"she lies in irons",
     "                    if abs(rel) <= 1 * POINT:\n                        self._miss_stays(\"she lies in irons", T),
    ("M08-helm-share-0", ST, "HELM_IN_HAND_SHARE = 0.25", "HELM_IN_HAND_SHARE = 0.0", T),
    ("M09-helm-share-1", ST, "HELM_IN_HAND_SHARE = 0.25", "HELM_IN_HAND_SHARE = 1.0", T),
    ("M10-under-rating-dropped", ST, "if sail.load_kn / rating < 1.0 and wanted >", "if wanted >", T),
    ("M11-kept-counted-strained", ST, ' not in lines and sl not in kept', ' not in lines', T),
    ("M12-kept-words-dropped", OI, '        text += " " + kept_words', '        pass', T),
    ("M13-helm-without-sign", ST, "    to_windward = -1.0 if d.apparent_wind_angle >= 0 else 1.0",
     "    to_windward = 1.0 if d.apparent_wind_angle >= 0 else -1.0", T),
]

D = [K + "test_truth_7_766_the_jib_she_cannot_be_held_without_is_left_on_her_and_said",
     K + "test_truth_7_767_a_jib_over_its_rating_is_taken_in_and_the_players_order_obeyed"] + [
     K + f"test_truth_7_762_the_fleet_goes_about_shortened[{s}-25-{h}]" for s in ("frigate-36", "razee-44") for h in ("290.0", "292.5", "295.0")]
MUTANTS = [(m[0] + "-Dslow", m[1], m[2], m[3], D) for m in MUTANTS if m[0][:3] in ("M08", "M09", "M10", "M11", "M12", "M13")]
