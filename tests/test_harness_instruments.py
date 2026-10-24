"""The sample's deltas and the stand-by's instruments (package 58a; the cold review of
2026-10-22, R-26, R-31 and §7.2, the lugger officer's account of time): the deltas and the
line of what stands as before, a fold's first sample whole, the captain's word not said
twice; the tripwires of the ship's own state; the `ahead` reading, the director's by the
truth; the cost of thinking in the station's line. Truths 7b-124 to 7b-126 are in
`tests/test_known_truths.py`."""

from __future__ import annotations

from datetime import datetime

from freesail.agents import Harness, SamplingPolicy
from freesail.agents import harness as harness_mod
from freesail.agents.agent import captain, officer
from freesail.agents.fake import Fake, call
from freesail.agents.model import DATA
from freesail.agents.tripwires import TRIPWIRE_WORDS, tripwire_of
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.world import Scenario

FRIGATE = "data/ships/frigate-36.yaml"


def off_the_lizard(heading: float = 180.0, knots: float = 6.0):
    """The frigate under plain sail south-west of the Lizard in a steady westerly."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=knots,
        position={"lat_deg": 49.95, "lon_deg": -5.30},
        region="channel-west",
    )
    w = make_world(7, FRIGATE, sc)
    w.submit("set plain sail")
    w.run(600)
    return w


def seated(w, script, station=None):
    st = station or captain(SamplingPolicy.in_lockstep(None, "urgent"), 24 * 3600, world=w)
    h = Harness(w, st, Fake(script), save=lambda _w, _why: None)
    h.start()
    return h


def samples(h) -> list[dict]:
    return [t.content for t in h.turns if t.role == DATA and "tool_results" not in t.content]


def resumed(w) -> list[str]:
    return [e.text.removeprefix("[captain] ") for e in w.log if e.kind == "agent.resumed"]


# ---------------------------------------------------------------------------
# Item 1: the deltas
# ---------------------------------------------------------------------------


def test_the_first_sample_after_a_handover_fold_is_whole():
    """The lead's reading: the first sample of a seating, and the first after a handover
    fold, are whole; every later one carries the deltas and the line of what is as before."""
    w = off_the_lizard()
    h = seated(w, [call("stand_by", until="a glass")] * 12)
    w.run(5 * 1800 + 5)  # turns enough that a fold has older exchanges to fold
    later = samples(h)[-1]
    assert "readings_are" in later and "sails" not in later["readings"]
    assert later["as_before"].startswith("As before: the sails, no sail in sight, the book;")
    h._fold_handover("Handover: standing south under plain sail, all well.")
    w.run(1800)
    whole = samples(h)[-1]
    assert "readings_are" not in whole and "as_before" not in whole
    assert "sails" in whole["readings"] and "heading" in whole["readings"]


def test_the_captains_word_is_carried_once_and_the_officer_reading_not_again_for_it():
    """No repetition of what was said to the station: the captain's word rides the
    sample's `word` and its log line is not given again beside it; the officer of the
    watch's reading, which lists every word the captain told him, is not sent again for a
    new word alone."""
    w = off_the_lizard()
    st = officer(SamplingPolicy.in_lockstep(None, "notable", "urgent"), 24 * 3600, world=w)
    h = seated(w, [call("stand_by", until="a word on deck")] * 4, station=st)
    w.run(60)
    w.submit("tell the officer of the watch to keep a sharp lookout for the Lizard")
    w.run(60)
    told = samples(h)[-1]
    assert told["word"] == "keep a sharp lookout for the Lizard"
    assert not [ln for ln in told["log"] if ln["kind"] == "agent.told"]
    assert "officer_of_the_watch" not in told["readings"]
    assert [e for e in w.log if e.kind == "agent.told"]  # the log keeps it, for read_log


# ---------------------------------------------------------------------------
# Item 3: the tripwires
# ---------------------------------------------------------------------------


def test_the_tripwires_are_read_in_their_words_and_others_refused_with_them_named():
    assert [tripwire_of(w.replace("<n>", "8")).text for w in TRIPWIRE_WORDS] == [
        "her way settled",
        "depth under 8 fathoms",
        "speed under 8 knots",
        "speed over 8 knots",
        "the wind over 8 knots",
        "a point of interest within 8 miles",
        "a sail within 8 cables",  # package 70
    ]
    assert tripwire_of("the depth below ten fathoms").text == "depth under 10 fathoms"
    assert tripwire_of("she has settled").text == "her way settled"
    assert tripwire_of("the moon over the yardarm") is None
    w = off_the_lizard()
    h = seated(w, [call("stand_by", until="a glass")])
    said = h.stand_by("the tide under the keel")
    assert "'her way settled'" in said and "'depth under <n> fathoms'" in said


def test_her_way_settled_wakes_her_two_minutes_after_she_steadies_from_a_helm_order():
    """The lugger officer's own proposal ("making the right orders at the wrong time":
    trimming before she settled): after 'steer N' from a southerly course she turns and
    gathers way for minutes; the stand-by wakes when her speed has held within a quarter
    knot and her head within a quarter point for two minutes, and says her speed."""
    w = off_the_lizard()
    seated(w, [[call("submit_order", text="steer N"), call("stand_by", until="her way settled")]])
    start = w.clock.tick
    w.run(30 * 60)
    woke = [t for t in resumed(w) if t.startswith("Her way settled")]
    assert woke and woke[0].startswith("Her way settled, at ") and " knots;" in woke[0]
    at = next(e.tick for e in w.log if e.kind == "agent.resumed")
    assert at - start >= harness_mod.R.INTERVALS["a glass"] // 15  # minutes, not at once


def test_a_point_of_interest_and_the_depth_wake_a_stand_by_by_the_readings():
    """'a point of interest within 3 miles' wakes when a charted mark comes within three
    miles of her position by account that was not so when she stood by, and names it;
    'depth under 20 fathoms' when the chart's depth at her account, or the lead's, is
    under it; standing for the land on the Lizard's west side both come before the land."""
    w = off_the_lizard()
    script = [
        [
            call("submit_order", text="steer N"),
            call("stand_by", until="a point of interest within 3 miles"),
        ],
        call("stand_by", until="depth under 12 fathoms"),
        call("stand_by", until="a glass"),
    ]
    seated(w, script)
    w.run(90 * 60)
    woke = resumed(w)
    assert woke[0].startswith("A point of interest within 3 miles: ") and "by account" in woke[0]
    assert woke[1].startswith("Depth under 12 fathoms")
    assert R.REGISTRY.get("ahead") is not None


# ---------------------------------------------------------------------------
# Item 4: `ahead`, and the cost of thinking
# ---------------------------------------------------------------------------


def test_ahead_says_what_lies_on_her_course_within_the_next_glass_by_account():
    """`ahead`: one line of what lies on her course within the next glass at her speed,
    from her position by account (the land, a danger near her track, the depth by the
    chart where it shoals or changes, a sail on her head); at anchor nothing."""
    w = off_the_lizard()
    first = w.readings.words("ahead")
    assert first.startswith("on her course S at ") and "the next glass" in first
    assert "by account" in first
    w.submit("steer N")
    seen = []
    for _ in range(8):
        w.run(600)
        seen.append(w.readings.words("ahead"))
    assert any("shoaling under 10 fathoms by the chart" in s for s in seen), seen
    assert any("the land in " in s for s in seen), seen
    assert seen.index(next(s for s in seen if "the land in " in s)) > 0  # the land comes last


def test_the_directors_ahead_is_the_truths():
    """The owner's ruling: the `ahead` reading is every station's that has the deck's
    readings, the director's by the truth (her true place, head and speed)."""
    w = off_the_lizard()
    truth = R.director_readings(w)
    assert truth["ships"][0]["ahead"].endswith(
        ("by the truth: open water, 29 fathoms by the chart",)
    ) or ("by the truth" in truth["ships"][0]["ahead"])
    assert "ahead: on her course" in truth["words"]


def test_the_line_says_the_ships_time_since_the_models_last_reply():
    """The cost of thinking: every sample's first line (66's) closes with the ship's time
    since the model's last reply; nothing before its first."""
    assert harness_mod.cost_words(0) == "under a minute of the ship's time since your last reply"
    assert harness_mod.cost_words(12 * 60 + 5).startswith("12 minutes of")
    assert harness_mod.cost_words(3900).startswith("an hour and 5 minutes of")
    assert harness_mod.cost_words(2 * 3600).startswith("2 hours of")
    w = off_the_lizard()
    h = seated(w, [call("stand_by", until="a glass")] * 3)
    w.run(1805)
    first, second = samples(h)[:2]
    assert "since your last reply" not in first["you"]
    assert second["you"].endswith("; 30 minutes of the ship's time since your last reply.")
