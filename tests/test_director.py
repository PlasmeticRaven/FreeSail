"""The director's station (spec M7b §2 to §6; decisions 46 and 50; package 50): a station
above the game bound to no person of any ship; the world orders doubted, not refused, and
entered again with a reason; an order the game has no way to perform answered honestly and
logged as attempted (the owner's refinement of 2026-10-17); the brief's limits enforced by
the channel; the budget in samples and acts a day; the log hidden from every station and
the player and revealed on request, inline in the replay view; the save and both roads of
the replay; the console's seat, the browser's queries and the doors. Proven against the
scripted fake (`freesail/agents/fake.py`, `director_above_the_game`) and never a model;
the identities are made up."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pytest

from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call, consent, reply
from freesail.agents import director as D
from freesail.agents import tools as T
from freesail.agents.agent import (
    CAPTAIN,
    DIRECTOR,
    SESSION_DIRECTOR,
    STATION_FACTORIES,
    captain,
    session_kind_of,
)
from freesail.agents.fake import captain_of_the_ship, director_above_the_game
from freesail.agents.seat import seat_player
from freesail.api import readings as R
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import for_the_record
from freesail.core.world import Scenario, World
from freesail.world import orders as WO
from tests.test_brains import put, world_at

ROOT = Path(__file__).resolve().parents[1]
EVERY = 600
WEIGHTS = "made-up-director-model-9b.Q4_K_M.gguf"  # made up: no model is named here

# A sail well outside the horizon (some thirty miles south-west) and one inside it (seven
# miles west-south-west) of the frigate at 49.5 N 5.5 W, for the doubt.
FAR_BRIG = 'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth'
NEAR_CUTTER = 'ship: a cutter "Lark" of Britain at 49 28 N 5 40 W, bound for Falmouth'


def world_at_time(hour: int, minute: int) -> World:
    """The frigate off the Lizard at another hour of 12 June 1805 (`world_at`'s water)."""
    sc = Scenario(
        start_time=dt.datetime(1805, 6, 12, hour, minute),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
    )
    return make_world(7, "data/ships/frigate-36.yaml", sc)


def directed(brief: Any = "quiet-passage", **kw) -> World:
    """The frigate at seed 7 off the Lizard with a brief given by the test (an input)."""
    w = world_at(49.5, -5.5, **kw)
    w.submit("set plain sail")
    if brief is not None:
        D.set_brief(w, brief, source="the test")
    return w


def seat_director(w: World, script: Any, every: int = EVERY) -> Harness:
    fake = script if hasattr(script, "reply") else Fake(script, loop=True)
    st = STATION_FACTORIES[DIRECTOR](
        SamplingPolicy.in_lockstep(every, "notable", "urgent"), world=w
    )
    h = Harness(w, st, fake, session_kind=SESSION_DIRECTOR, save=lambda w, why: None)
    h.model_name, h.door = "the fake director", "runner"
    h.start()
    return h


def seat_captain(w: World, orders=()) -> Harness:
    h = Harness(
        w,
        captain(SamplingPolicy.in_lockstep(EVERY, "notable", "urgent"), world=w),
        captain_of_the_ship(list(orders)),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake captain", "mcp"
    h.start()
    return h


def log_kinds(w: World) -> list[str]:
    return [e.kind for e in D.log_of(w).entries]


def log_texts(w: World) -> list[str]:
    return [e.text for e in D.log_of(w).entries]


# ---------------------------------------------------------------------------
# §2: the station
# ---------------------------------------------------------------------------


def test_the_director_is_aboard_only_when_a_brief_is_given_and_a_world_without_one_is_as_it_was():
    w = world_at(49.5, -5.5)
    assert DIRECTOR not in w.stations.names() and w.stations.binding(DIRECTOR) is None
    assert w.stations.holder(DIRECTOR) is None
    assert not [e for e in w.log.all() if for_the_record(e)]
    assert D.brief_of(w) is None and w.save()["director"] == {}
    D.set_brief(w, "quiet-passage", source="the test")
    assert DIRECTOR in w.stations.names()
    b = w.stations.binding(DIRECTOR)
    assert b is not None and b.kind == DIRECTOR and b.person == ""
    bound = [e for e in w.log.all() if e.kind == "station.bound"]
    assert bound and all(for_the_record(e) and e.actor == "the director" for e in bound)
    assert w.inputs[-1]["director_brief"]["name"] == "A quiet passage"
    assert log_kinds(w) == ["director.brief"]
    assert w.save()["director"]["brief"]["limits"]["wind_max_kn"] == 27


def test_the_station_is_made_with_the_players_brief_after_the_fixed_part_and_the_truth_tools():
    w = directed()
    st = STATION_FACTORIES[DIRECTOR](world=w)
    assert st.name == DIRECTOR and st.authority.value == "director" and st.person == ""
    assert st.domain is not None and not st.domain.deck
    assert st.brief.startswith(D.DIRECTOR_BRIEF) and "The player's brief:" in st.brief
    assert "A quiet passage" in st.brief and "no wind above 27 knots" in st.brief
    # the owner's refinement (2026-10-17): the forms are examples, not a rule
    assert "examples of reasonable orders, not as the whole of what you may try" in st.brief
    assert "attempted when you think it reasonable" in st.brief
    assert session_kind_of("play", DIRECTOR) == SESSION_DIRECTOR
    h = seat_director(w, [Reply()])
    assert "world_order" in h.tool_names and "truth" in h.tool_names
    assert "hand_over" not in h.tool_names and "handover_note" not in h.tool_names
    # the pictures at this station (the lead's note): the chart for planning, said to be the
    # player's and not the truth; no ship's view above the game
    at_door = T.tool_names(pictures=True, director=True)
    assert "chart" in at_door and "ship_view" not in at_door
    assert "ship_view" in T.tool_names(pictures=True)
    assert "no other ship is on it" in T.description_of("chart", director=True)
    assert T.description_of("chart", director=True) != T.description_of("chart")
    assert T.description_of("truth", director=True) == T.TOOLS["truth"].description
    assert "stands on no deck" in T.call(w, DIRECTOR, "ship_view", {})
    assert "the chart tool is not the truth" in st.brief
    head = h.brief.text()
    assert "taking the station of the director" in head and SESSION_DIRECTOR in head
    assert "The voyage:" in head  # the voyage's words, as the captain's brief has them
    assert "no order of any ship" in head
    assert "his standing orders as the book holds" not in head  # no captain over the director
    # the fixed brief head's order holds (truth 46), whatever the station brief says
    assert h.brief.order == ("disclosure", "opt_out", "documentation", "authority", "situation")


def test_every_order_of_the_ship_is_refused_at_the_director_and_the_readings_are_read():
    w = directed()
    h = seat_director(w, [Reply()])
    n = len(w.journal)
    for text in ("set the royals", "steer N", "heave to", "say good morning"):
        said = T.call(w, DIRECTOR, "submit_order", {"text": text})
        assert "no order of any ship" in said, (text, said)
    assert "not carried out" in T.call(w, DIRECTOR, "submit_order", {"text": "ask the master why"})
    assert len(w.journal) == n
    refused = [e for e in w.log.all() if e.kind == "agent.refused"]
    assert refused and all(for_the_record(e) for e in refused)
    # a reading is read (the player's ship's, beside the truth), and a world order through
    # submit_order is sent to its own tool
    assert "knots" in T.call(w, DIRECTOR, "submit_order", {"text": "the true wind"})
    said = T.call(w, DIRECTOR, "submit_order", {"text": FAR_BRIG})
    assert "world_order tool" in said
    assert h.agent.samples >= 1


def test_the_truth_is_the_directors_alone_and_the_other_stations_do_not_see_it_or_the_director():
    w = directed()
    put(w, "merchant brig", "britain", "49 00 N 6 20 W", "bound for Falmouth", "bound for Falmouth")
    seat_director(w, [Reply()])
    seat_captain(w)
    truth = T.call(w, DIRECTOR, "truth", {})
    assert isinstance(truth, dict) and "refused" not in truth
    names = [s["name"] for s in truth["ships"]]
    assert names[0] == w.ship.name and "X" in names
    assert "intent" in truth["ships"][1] and "from_the_ship" in truth["ships"][1]
    assert "wind_now" in truth["weather"] and "systems" in truth["weather"]
    assert w.ship.name in truth["people"] and "markets" in truth and "words" in truth
    assert "Amazon" in truth["words"] or w.ship.name in truth["words"]
    # the captain's station: refused in words, and no director in its state or stations
    assert "refused" in T.call(w, CAPTAIN, "truth", {})
    assert "director" not in T.call(w, CAPTAIN, "state", {}).lower()
    assert "director" in T.call(w, DIRECTOR, "state", {}).lower()
    assert "director" not in w.readings.words("stations")
    assert "world_order" not in w.agents[CAPTAIN].tool_names
    assert "gives no world order" in T.call(w, CAPTAIN, "world_order", {"text": FAR_BRIG})


def test_the_truth_says_her_state_shows_the_intent_not_the_placeholder_and_reads_within():
    """Package 68 (the cold review of 2026-10-22, R-35): the director read "she is NOT
    aground" from her speed alone, every business ship's goal read "bound for Falmouth",
    and a read cost seven to twelve thousand tokens, most of them far ships. The player's
    ship says her state; a ship by her intent shows the intent and no goal; `within` keeps
    the near ships and their people, and counts the rest."""
    from tests.test_ground import on_the_falmouth_bank

    w = on_the_falmouth_bank()
    D.set_brief(w, "quiet-passage", source="the test")
    put(w, "merchant brig", "britain", "50 05 N 5 00 W", "bound for Falmouth", "", name="Near")
    put(
        w,
        "brig-sloop",
        "france",
        "48 00 N 6 00 W",
        "bound for Falmouth",
        "keep the station off Ushant within 15 miles",
        name="Far",
    )
    seat_director(w, [Reply()])
    truth = T.call(w, DIRECTOR, "truth", {})
    own = truth["ships"][0]
    assert own["state"].startswith("aground, ") and "; the tide " in own["state"], own["state"]
    by = {s["name"]: s for s in truth["ships"][1:]}
    assert "goal" not in by["Far"] and by["Far"]["intent"].startswith("keep the station off")
    near = T.call(w, DIRECTOR, "truth", {"within": 20})
    names = [s["name"] for s in near["ships"]]
    assert names[0] == own["name"] and "Near" in names and "Far" not in names
    assert near["within"].endswith("; 1 more beyond, not shown")
    assert "refused" in T.call(w, DIRECTOR, "truth", {"within": "far"})
    w2 = directed()
    seat_director(w2, [Reply()])
    assert T.call(w2, DIRECTOR, "truth", {})["ships"][0]["state"] == "under way"


# ---------------------------------------------------------------------------
# §3: the world orders, doubted not refused; the forms as examples
# ---------------------------------------------------------------------------


def test_a_doubted_order_is_not_performed_and_entered_again_with_its_reason_it_is():
    """Decision 50: the channel states the reason and the owner's words; entered again
    with a `[reason: ...]` the order is performed, and the log keeps the act, the doubt
    and the reason together."""
    w = directed()
    said = D.direct(w, NEAR_CUTTER, by="the test")
    assert said.startswith("Doubted, not performed:") and "inside the lookout's horizon" in said
    assert WO.REENTER_WORDS in said and "[reason: ...]" in said
    assert w.vessels.find("Lark") is None and log_kinds(w)[-1] == "director.doubted"
    assert D.budget_of(w).acts == 0
    said = D.direct(w, f"{NEAR_CUTTER} [reason: the story wants her near]", by="the test")
    assert said.startswith("Done:") and w.vessels.find("Lark") is not None
    entry = D.log_of(w).entries[-1]
    assert entry.kind == "director.reentered" and entry.by == "the test"
    assert "the doubt: a sail put on the sea" in entry.text
    assert "the reason: the story wants her near" in entry.text
    assert D.budget_of(w).acts == 1
    # the order itself is the channel's record, never the play log's
    orders = [e for e in w.log.all() if e.kind == "world.order"]
    assert orders[-1].data["source"] == "the director" and for_the_record(orders[-1])
    assert "[reason" not in orders[-1].data["order"]


def test_what_the_channel_doubts_and_what_it_lets_be():
    w = directed(systems=[], climatology=True, glass=True)
    w.run(60)
    cases = {
        FAR_BRIG: None,  # thirty miles off: over the horizon
        NEAR_CUTTER: "inside the lookout's horizon",
        # on the land: the form's refusal since package 68, never a doubt a reason answers
        'ship: a cutter "Ashore" of Britain at 50 05 N 5 15 W, bound for Falmouth': None,
        "mark: a cask adrift at 49 28 N 5 40 W": "inside the lookout's horizon",
        "mark: a wreck, her masts showing at 49 00 N 6 20 W": None,
        'weather: low "the deep" radius 450 km at 1805-06-12T10:00 -600 600 940': "season's floor",
        'weather: low "the near" radius 400 km at 1805-06-12T10:00 50 50 998': (
            "out of a steady glass"
        ),
        'weather: low "the far" radius 450 km at 1805-06-12T10:00 -900 700 996': None,
        'message: by a cutter from Brest from the Prefect: "Come."': "could not know where",
        'message: by a cutter from Falmouth from the collector: "The packet is in."': None,
        'message: at Brest from the Prefect: "Come."': None,
        "port falmouth: price of tin 300": "moved by",
        "port falmouth: price of tin 120": None,
        "port brest: closed to Denmark": None,
        "aboard: the fore topmast is found sprung": "nothing has strained",
        "aboard: the water found foul": "casks do not foul",
    }
    for text, expected in cases.items():
        found = WO.doubt(w, WO.parse(text))
        if expected is None:
            assert found is None, (text, found)
        else:
            assert found is not None and expected in found, (text, found)
    ashore = 'ship: a cutter "Ashore" of Britain at 50 05 N 5 15 W, bound for Falmouth'
    said = D.direct(w, f"{ashore} [reason: the story wants her there]", by="the test")
    assert said.startswith("Logged as attempted") and "is on the land by the chart" in said
    assert "the nearest water she floats in is" in said and w.vessels.find("Ashore") is None
    # a mind changed wants no cause
    put(w, "merchant brig", "britain", "49 00 N 6 20 W", "bound for Falmouth", "bound for Falmouth")
    assert WO.doubt(w, WO.parse('ship "X": intent run home to Brest')) is None
    # a far-off deep low is doubted by the floor only; a waypoint faster than the season's
    e = w.world_order('weather: low "the far" radius 450 km at 1805-06-12T10:00 -900 700 996', "t")
    assert e.data["result"] == "done"
    fast = 'weather: waypoint for "the far" at 1805-06-12T12:00 900 700 996'
    assert "faster than the season's lows" in WO.doubt(w, WO.parse(fast))


def test_an_order_the_game_has_no_way_to_perform_is_answered_honestly_and_logged_as_attempted():
    """The owner's refinement (2026-10-17): the forms are examples; an order beyond them,
    or free words within a domain the table does not know, is not refused as 'not allowed'
    but answered honestly, and entered again with a reason it is logged as attempted, the
    words kept for whoever builds the next forms."""
    w = directed()
    for text in (
        "news: war declared between Britain and Denmark",
        "aboard: the cook reports the beef cask found rotten",
        "weather: a squall line from the north-west in forty minutes",
        'say as the harbourmaster of Falmouth: "The packet is in."',
    ):
        said = D.direct(w, text, by="the test")
        assert said.startswith("The game has no way to do this as said"), (text, said)
        assert "not allowed" not in said and "[reason: ...]" in said
        assert log_kinds(w)[-1] == "director.unperformed" and text in log_texts(w)[-1]
        said = D.direct(w, f"{text} [reason: to see what the game makes of it]", by="the test")
        assert said.startswith("Logged as attempted, not performed"), (text, said)
        entry = D.log_of(w).entries[-1]
        assert entry.kind == "director.attempted"
        assert text in entry.text and "to see what the game makes of it" in entry.text
    assert D.budget_of(w).acts == 0  # nothing performed, nothing counted
    assert "director.refused" not in log_kinds(w)  # the brief's limits alone refuse


def test_the_aboard_orders_do_what_the_table_knows_and_reach_the_play_log_as_a_report():
    w = directed(brief=None)
    spar = w.ship.parts["fore.topmast"]
    water = w.stores.water_tons
    for text, _kind, check in (
        (
            "aboard: the fore topmast is found sprung [reason: the test]",
            "spar_sprung",
            lambda: spar.condition == 30.0,
        ),
        (
            "aboard: a cask found stove [reason: the test]",
            "cask_stove",
            lambda: w.stores.water_tons == water - 1.0,
        ),
        ("aboard: a seam found working [reason: the test]", "seam_working", lambda: True),
        ("aboard: the water found foul [reason: the test]", "water_foul", lambda: w.stores.foul),
    ):
        # the doubt seen first, then entered again with the reason (package 68: a reason on
        # the first entry answers no doubt the director has seen)
        D.direct(w, text.split(" [reason")[0], by="the test")
        said = D.direct(w, text, by="the test")
        assert said.startswith("Done: found aboard"), (text, said)
        assert check(), text
    reports = [e for e in w.log.all() if e.kind == "aboard.found"]
    assert [e.data["thing"] for e in reports] == [
        "spar_sprung",
        "cask_stove",
        "seam_working",
        "water_foul",
    ]
    assert reports[0].text.startswith("The carpenter reports the fore topmast sprung")
    assert all(e.severity.value == "notable" and not for_the_record(e) for e in reports)
    assert "found foul" in "\n".join(w.stores.lines(100))
    # the table is what the game can do, not what the director may say
    assert len(WO.aboard_table()) == 26  # package 70: the guns' two things
    assert "aboard" in WO.CHANNELS and WO.recognises("aboard: a cask found stove")


# ---------------------------------------------------------------------------
# §4: the brief and its limits, enforced by the channel
# ---------------------------------------------------------------------------


def test_the_starter_briefs_load_and_the_console_brief_is_words_alone():
    names = D.starter_briefs()
    # the starters the code and the primer name are there; the owner's own briefs beside
    # them (interesting-passage-nobudget, 2026-10-19) are welcome and checked the same
    assert {
        "chase",
        "dispatches",  # the owner's story brief for the director's test (2026-10-18)
        "hard-cruise",
        "interesting-passage",
        "quiet-passage",
    } <= set(names)
    for name in names:
        b = D.resolve_brief(name)
        assert b.tone and b.challenge and b.limits.get("nobody_dies") and b.acts_a_day > 0
        assert b.cadence in ("glass", "watch")
    quiet = D.resolve_brief("a quiet passage")
    assert quiet.name == "A quiet passage" and quiet.limits["enemy_heaviest"] == "cutter"
    assert D.resolve_brief(str(ROOT / "data/director/briefs/chase.yaml")).name == "A chase"
    words = D.resolve_brief("a quiet passage with a chase on the second day", source="the console")
    assert words.tone.startswith("a quiet passage with a chase") and words.limits == {}
    assert words.limits_words() == "none beyond the channel's doubt"
    assert D.DirectorBrief.from_dict({"limits": {"gale_max_force": 8}}).limits["wind_max_kn"] == 40
    with pytest.raises(ValueError):
        D.DirectorBrief.from_dict({"cadence": "minute"})
    with pytest.raises(ValueError):
        D.resolve_brief("")


def test_the_briefs_limits_refuse_outright_with_the_reason_and_the_refusal_is_logged():
    """Spec M7b §4: a world order outside the brief's limits is refused as outside the
    brief, enforced by the channel and never trusted to the model; the chase's brief lets
    a brig through where the quiet passage refuses it."""
    w = directed("quiet-passage", systems=[], climatology=True)
    gale = 'weather: low "the gale" radius 450 km at 1805-06-12T10:00 -800 800 965'
    said = D.direct(w, gale, by="the test")
    assert said.startswith("Refused, outside the brief") and "no wind above 27 knots" in said
    assert w.systems is None or w.systems.find("the gale") is None
    assert log_kinds(w)[-1] == "director.refused"
    brig = (
        'ship: a brig-sloop "Harpy" of France at 49 00 N 6 20 W, running home to Brest, no colours'
    )
    said = D.direct(w, brig, by="the test")
    assert "no enemy heavier than a cutter" in said and w.vessels.find("Harpy") is None
    said = D.direct(w, "port brest: closed to Britain [reason: the war]", by="the test")
    assert "keeps the war as it is" in said and "britain" not in w.ports.ports["brest"].closed_to
    assert D.direct(w, "port brest: closed to Denmark", by="the test").startswith("Done")
    friend = 'ship: a brig-sloop "Harpy" of Britain at 49 00 N 6 20 W, bound for Plymouth'
    assert D.direct(w, friend, by="the test").startswith("Done")  # not an enemy
    assert D.budget_of(w).acts == 2
    # the chase's brief allows a brig and a fresher wind
    w2 = directed("chase", systems=[], climatology=True)
    assert D.direct(w2, brig, by="the test").startswith("Done")
    fresh = 'weather: low "a blow" radius 450 km at 1805-06-12T10:00 -800 800 1000'
    assert D._peak_wind_kn(w2, fresh) < 33 and D.direct(w2, fresh, by="the test").startswith("Done")
    assert D._peak_wind_kn(w2, gale) > 33 and "Refused" in D.direct(w2, gale, by="the test")
    # the brief with no limits doubts and never refuses
    w3 = directed("a voyage in the player's own words", systems=[], climatology=True)
    assert D.direct(w3, gale, by="the test").startswith("Doubted")  # the season's floor
    assert D.direct(w3, f"{gale} [reason: the test]", by="the test").startswith("Done")


# Each starter brief's enemy limit against an enemy of each class (package 68; the cold
# review of 2026-10-22, R-38: "brig" held none of the ranking's keys, and a French frigate
# passed four briefs of no enemy heavier than a brig; only "cutter" was tested).
_CLASSES = {"cutter": 1, "lugger": 1, "brig-sloop": 2, "merchant brig": 2, "frigate": 3}


@pytest.mark.parametrize(
    "brief,heaviest",
    [
        ("quiet-passage", 1),
        ("chase", 2),
        ("interesting-passage", 2),
        ("dispatches", 2),
        ("hard-cruise", 3),
    ],
)
def test_each_starter_briefs_enemy_limit_refuses_a_heavier_enemy_and_passes_its_own(
    brief: str, heaviest: int
):
    from freesail.world.captains import size_rank_of

    limit = D.resolve_brief(brief).limits["enemy_heaviest"]
    assert size_rank_of(limit) == heaviest
    for desc, rank in _CLASSES.items():
        w = directed(brief, systems=[], climatology=True)
        order = f'ship: a {desc} "Harpy" of France at 49 00 N 6 20 W, running home to Brest'
        said = D.direct(w, order, by="the test")
        if rank > heaviest:
            assert said.startswith("Refused, outside the brief"), (desc, said)
            assert f"no enemy heavier than a {limit}" in said
            assert w.vessels.find("Harpy") is None
        else:
            assert not said.startswith("Refused"), (desc, said)


# ---------------------------------------------------------------------------
# §5: sampling, the budget and the clock
# ---------------------------------------------------------------------------


def test_the_budget_of_acts_is_spent_and_renewed_with_the_ships_day():
    """Spec M7b §5 and truth 93: a director on a budget of three acts a day gives no
    fourth; the result and the log say the budget is spent; it stands by until the next
    day and the next day's sample says the budget is renewed."""
    w = world_at_time(23, 20)
    w.submit("set plain sail")
    D.set_brief(
        w,
        {"name": "three a day", "budget": {"samples_a_day": 48, "acts_a_day": 3}},
        source="the test",
    )
    orders = [
        "port falmouth: price of tin 120",
        "port falmouth: price of tin 125",
        "port falmouth: price of tin 130",
        "port falmouth: price of tin 135",
        "port falmouth: price of tin 140",
    ]
    h = seat_director(w, director_above_the_game(orders))
    w.run(3 * EVERY + 1)
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 130.0
    b = D.budget_of(w)
    assert b.acts == 3 and b.held_until is not None and b.day == "1805-06-12"
    spent = [t for t in log_texts(w) if "budget of 3 acts is spent" in t]
    assert spent and "stands by until the next day (1805-06-13 00:00)" in spent[0]
    samples = h.agent.samples
    w.run(9 * 60)  # held: no sample opens before midnight, whatever the policy
    assert h.agent.samples == samples
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 130.0
    w.run(41 * 60)  # past midnight: the budget renewed, the fourth order given
    assert h.agent.samples > samples
    assert any("budget is renewed (1805-06-13)" in t for t in log_texts(w))
    assert w.ports.ports["falmouth"].market.goods["tin"].price >= 135.0
    assert D.budget_of(w).day == "1805-06-13" and D.budget_of(w).acts >= 1
    # the notices say the budget as it stands, every sample
    told = [t for t in h.turns if t.role == "data" and "notices" in (t.content or {})]
    assert any("The day's budget" in n for t in told for n in t.content["notices"])


def test_the_budget_of_samples_holds_the_director_and_the_cadence_is_the_briefs():
    w = directed({"name": "few samples", "budget": {"samples_a_day": 2, "acts_a_day": 9}})
    h = seat_director(w, [Reply()])
    w.run(4 * EVERY)
    assert h.agent.samples == 2 and D.budget_of(w).held_until is not None
    assert any("budget of 2 samples is spent" in t for t in log_texts(w))
    # the cadence: every watch by the brief
    w2 = directed({"name": "slow", "cadence": "watch"})
    st = STATION_FACTORIES[DIRECTOR](world=w2)
    assert st.policy.every_s == 4 * 3600 and "every watch" in st.policy.describe()
    from freesail.agents.agent import cadence_policy

    assert cadence_policy("glass", DIRECTOR, world=w2).every_s == 4 * 3600
    assert cadence_policy("glass", DIRECTOR, world=w).every_s == 1800


def test_the_directors_own_lines_wake_it_not_and_every_other_station_meets_them():
    """Package 68 (the cold review of 2026-10-22, R-61: 42% of a day's samples were the
    director's own `say as` and `aboard` lines echoing back): the lines its own world order
    writes open no sample of the director's, nor are they folded into its turn; the
    captain meets them as before."""
    w = directed()
    ch = seat_captain(w)
    script = [
        reply("", call("world_order", text='say as the boatswain: "A cask stove, sir."')),
        Reply(),
        reply("", call("world_order", text='say as the cook: "The cask is stove, sir."')),
        Reply(),
    ]
    dh = seat_director(w, Fake(script, loop=True))
    w.run(3 * EVERY)
    # each sample's say as echoed back and opened the next, every tick, before
    assert len([e for e in w.log if e.kind == "person.spoke"]) < 20
    reasons = json.dumps([t.content.get("reason") for t in dh.turns if t.role == "data"])
    folds = json.dumps(
        [t.content for t in dh.turns if t.role == "data" and t.content.get("folded")]
    )
    assert "cask" not in reasons and "cask" not in folds, reasons
    seen = json.dumps([t.content for t in ch.turns if t.role == "data"])
    assert "cask" in seen  # the captain met the effects


def test_the_budget_is_set_in_play_a_new_brief_lifts_the_hold_and_words_keep_the_limits():
    """Package 68 (R-61): `director: budget <n> samples, <m> acts` sets the day's budget in
    play, an input replayed; a brief whose budget the day's counts are within lifts a hold
    the old one made; `director: brief <words>` changes the tone and keeps the limits, the
    cadence and the budget it does not name; a starter's name is a brief whole."""
    from freesail.ui.console import director_brief_words, give_director_brief

    w = directed({"name": "few samples", "budget": {"samples_a_day": 2, "acts_a_day": 9}})
    h = seat_director(w, [Reply()])
    w.run(4 * EVERY)
    assert h.agent.samples == 2 and D.budget_of(w).held_until is not None
    said = give_director_brief(w, director_brief_words("director: budget 60 samples, 10 acts"), "p")
    assert said[0].startswith("The director's budget is set (p): 60 samples and 10 acts a day")
    assert D.brief_of(w).name == "few samples" and D.budget_of(w).held_until is None
    assert any("The hold is lifted by the new brief: 2 of 60 samples" in t for t in log_texts(w))
    w.run(EVERY)
    assert h.agent.samples == 3  # sampled again the same day
    bad = give_director_brief(w, director_brief_words("director: budget plenty"), "p")
    assert bad[0].startswith("The budget was not taken: A budget says its samples or its acts")
    # words keep the limits; a starter is whole
    w2 = directed("quiet-passage", systems=[], climatology=True)
    give_director_brief(w2, "a quieter passage still, the fog the only foe", "p")
    b = D.brief_of(w2)
    assert b.tone.startswith("a quieter passage still") and b.limits["enemy_heaviest"] == "cutter"
    assert (
        b.limits.get("nobody_dies")
        and b.samples_a_day == D.resolve_brief("quiet-passage").samples_a_day
    )
    give_director_brief(w2, "chase", "p")
    assert D.brief_of(w2).limits["enemy_heaviest"] == "brig"
    copy = replay.replay(json.loads(json.dumps(w2.save())), ship_factory)
    assert D.brief_of(copy).to_dict() == D.brief_of(w2).to_dict()


# ---------------------------------------------------------------------------
# §6: the log, hidden and revealed; the replay view; the save
# ---------------------------------------------------------------------------


def _no_director_in(lines: list[Any]) -> bool:
    text = json.dumps(lines).lower()
    return "director" not in text and "world order" not in text


def test_the_directors_words_and_acts_reach_no_station_and_no_play_log_and_the_effects_do():
    """Truths 91 and 92: a world order given by the director appears in no station's
    sample and no play log; its effect does, when met; the log is empty to every station
    and the player until asked for."""
    w = directed()
    ch = seat_captain(w)
    dh = seat_director(w, director_above_the_game([FAR_BRIG, "aboard: a cask found stove"]))
    w.run(6 * EVERY)
    # the director spoke and acted
    assert "director.order" in log_kinds(w) and any(e.kind == "note" for e in D.log_of(w).entries)
    assert w.vessels.find("Nancy") is not None
    # the play log as every view has it
    play = [e for e in w.log.all() if not for_the_record(e)]
    assert _no_director_in([e.text for e in play])
    assert not [e for e in play if e.actor == "the director"]
    hidden = [e for e in w.log.all() if for_the_record(e)]
    assert any(e.kind == "agent.stationed" and e.actor == "the director" for e in hidden)
    assert any(e.kind == "world.order" and e.data["source"] == "the director" for e in hidden)
    # the captain's samples and its reads
    samples = [t.content for t in ch.turns if t.role == "data"]
    assert _no_director_in(samples)
    assert _no_director_in(T.read_log(w, CAPTAIN, since_tick=0)["lines"])
    assert "director" not in T.call(w, CAPTAIN, "read_journal", {}).__repr__().lower()
    # the effect is met: the cooper's report in the captain's sample
    assert any("cooper reports a water cask stove" in json.dumps(s) for s in samples)
    # the player's views
    from freesail.ui.server import Driver

    driver = Driver(w, compression=60.0)
    assert _no_director_in(driver.shown_log(1000))
    # the director's own journal is the log, read back by it alone
    read = T.call(w, DIRECTOR, "read_journal", {"kind": "notes"})
    assert any("Arranging" in e["text"] for e in read["entries"])
    assert dh.journal is D.log_of(w)
    # the journal and the seat of other stations show nothing of it
    for text in (
        "show the director's journal",
        "tell the director to send a gale",
        "ask the director why",
    ):
        e = w.submit(text)
        assert e.kind == "order.rejected" and "above the game" in e.text, text


def test_the_log_is_revealed_on_request_the_director_told_and_shown_inline_in_the_replay_view():
    w = directed()
    dh = seat_director(w, [Reply()])
    D.direct(w, FAR_BRIG, by="the test")
    w.run(2 * EVERY)
    n = len(w.inputs)
    lines = D.reveal(w, "the player")
    assert lines[0].startswith("The director's log (") and any("(order)" in ln for ln in lines)
    assert any("(brief)" in ln for ln in lines) and lines[-1].endswith("asked for by the player.")
    revealed = w.log.all()[-1]
    assert revealed.kind == "director.revealed" and revealed.actor == "driver"
    assert for_the_record(revealed) and len(w.inputs) == n + 1
    assert any("asked for by the player" in x for x in dh.agent.notices)
    w.run(EVERY)
    told = [t.content for t in dh.turns if t.role == "data" and t.content.get("notices")]
    assert any("asked for by the player" in n for t in told for n in t["notices"])
    stories = D.two_stories(w)
    marked = [ln for ln in stories if ln.startswith("D ")]
    assert (
        marked
        and any("(order)" in ln for ln in marked)
        and any("(revealed)" in ln for ln in marked)
    )
    assert not any("World order" in ln for ln in stories if not ln.startswith("D "))
    first_d = next(i for i, ln in enumerate(stories) if ln.startswith("D "))
    assert first_d > 0 and stories[first_d - 1].startswith(("*", " ", "!", "="))
    assert D.two_stories(w, 3) == stories[-3:]


def test_a_directed_voyage_saved_replays_by_both_roads_to_the_same_log_and_the_same_directors_log(
    tmp_path,
):
    """Truth 94: a directed voyage saved and replayed gives the same log, the director's
    acts among the inputs; by the transcript (this build's own game) and by the stations'
    acts (another build's road), the director's log entry for entry; and from its
    checkpoint with the director seated and the budget as it stood."""
    w = directed()
    seat_captain(w, ["heave the log"])
    seat_director(
        w,
        director_above_the_game(
            [
                NEAR_CUTTER,
                FAR_BRIG,
                "aboard: the water found foul",
                "port falmouth: price of tin 125",
            ]
        ),
    )
    w.run(5 * EVERY)
    D.reveal(w, "the player")
    w.run(2 * EVERY)
    path = tmp_path / "directed.json"
    replay.save_to_file(w, path)
    data = replay.load_file(path)
    assert data["director"]["budget"]["acts"] == 4 and data["director"]["brief"]["name"]
    assert "director" in data["agent_journals"]
    acts = [a for a in data["station_acts"] if "world_order" in a]
    assert len(acts) == 4 and all(a["station"] == DIRECTOR for a in acts)
    assert not [i for i in data["inputs"] if i.get("source") == "the director"]
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == w.log.digest(), road
        assert log_texts(copy) == log_texts(w), road
        assert copy.vessels.find("Lark") is not None and copy.stores.foul
        assert D.budget_of(copy).acts == 4
    back, report = replay.load_report(path, ship_factory)
    assert report.how == "checkpoint" and DIRECTOR in back.agents
    assert D.brief_of(back).name == "A quiet passage" and D.budget_of(back).acts == 4
    assert back.stations.aboard(DIRECTOR)


# ---------------------------------------------------------------------------
# The console, the browser and the doors
# ---------------------------------------------------------------------------


def test_the_console_reveals_the_log_gives_the_brief_and_seats_the_player_as_director():
    import io

    from freesail.ui.console import Console

    w = world_at(49.5, -5.5)
    out = io.StringIO()
    console = Console(w, out=out)
    console.handle_line("director: brief")
    assert "No brief is given yet" in out.getvalue()
    console.handle_line("director: brief quiet-passage")
    assert "The director's brief is given" in out.getvalue() and D.brief_of(w) is not None
    assert w.stations.aboard(DIRECTOR)
    console.handle_line("the director's log")
    assert "The director's log (" in out.getvalue() and "(brief)" in out.getvalue()
    assert w.log.all()[-1].kind == "director.revealed"
    # the player at the director's seat: a bare world order is the director's
    seat = seat_player(w, "director", door="console")
    assert w.player_seat is seat and seat.station.name == DIRECTOR
    out.truncate(0)
    out.seek(0)
    console.handle_line(NEAR_CUTTER)
    assert "Doubted, not performed" in out.getvalue()
    console.handle_line(f"{NEAR_CUTTER} [reason: the player's own story]")
    assert "Done:" in out.getvalue() and w.vessels.find("Lark") is not None
    assert log_kinds(w)[-1] == "director.reentered" and D.log_of(w).entries[-1].by == "the player"
    out.truncate(0)
    out.seek(0)
    console.handle_line("set the royals")
    assert "no order of any ship" in out.getvalue() or "not carried out" in out.getvalue()
    assert not [j for j in w.journal if j[2] == "set the royals"]
    console.handle_line("the truth")
    assert "heading" in out.getvalue() and "Lark" in out.getvalue()
    console.handle_line("two stories 5")
    assert "D " in out.getvalue()
    # the owner's own live order is still his, through the prefix, undoubted
    console.handle_line("world: port falmouth: price of tin 300")
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 300.0
    # the play log at the console carries no record-only line
    out.truncate(0)
    out.seek(0)
    console.handle_line("log 200")
    printed = out.getvalue()
    assert "World order" not in printed and "director's station is bound" not in printed
    # the seat replays: the binding and the seat are inputs
    copy = replay.replay(w.save(), ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.player_seat is not None and copy.player_seat.station.name == DIRECTOR
    assert log_texts(copy) == log_texts(w)


def test_the_browser_answers_the_same_requests_and_its_log_carries_nothing_of_the_director():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    w = directed()
    seat_director(w, director_above_the_game([FAR_BRIG]))
    w.run(2 * EVERY)
    driver = Driver(w, compression=60.0)
    e = driver.submit("the director's log")
    assert e.kind == "query.director_log" and "(order)" in e.text
    assert w.log.all()[-1].kind == "director.revealed"
    e = driver.submit("two stories 4")
    assert e.kind == "query.two_stories" and "D " in e.text
    e = driver.submit("director: brief")
    assert e.kind == "query.director_brief" and "A quiet passage" in e.text
    with TestClient(create_app(driver)) as http:
        got = http.get("/api/director/log").json()
        assert got["lines"][0].startswith("The director's log") and got["entries"]
        shown = http.get("/api/log?limit=2000").json()
        assert _no_director_in(shown)
        page = http.get("/").text
        assert 'id="director-panel"' in page and "director's log" in page
        js = http.get("/client/app.js").text
        assert "query.director_log" in js and "openDirectorLog" in js


def test_ease_on_station_never_eases_for_the_director_and_no_refusal_names_it():
    """Package 68 (the cold review of 2026-10-22, R-20; spec M7b §6): with
    `--ease-on-station`, "Compression eased to 1x: the director is sampled" reached the
    officer's samples six times, and the standing order's refusal listed the director among
    the stations a standing order may tell. The director's samples ease nothing and write
    no line; the refusal names the stations aboard and never the director."""
    pytest.importorskip("fastapi")
    from freesail.ui.server import Driver

    w = directed()
    h = seat_director(w, ["Nothing yet."])
    driver = Driver(w, compression=60.0, ease_on_station=True)
    driver.running = True
    driver._run_ticks(2 * EVERY + 10)
    assert h.agent.samples >= 2
    assert driver.compression == 60.0
    assert not [e for e in w.log.all() if e.kind == "driver.eased"]
    assert not [e for e in w.log.all() if "director" in e.text and not for_the_record(e)]
    e = w.submit("standing order 'sea': when the glass is falling fast then tell the director so")
    assert e.kind == "order.rejected" and "the director is above the game" in e.text, e.text
    assert "the director" not in e.text.split("; a standing order may tell or ask ", 1)[1]


def test_a_door_seats_a_model_as_the_director_with_the_directors_brief_and_tools(tmp_path):
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    records = tmp_path / "consent"
    records.mkdir()
    consent.Record(
        WEIGHTS, "a test runtime", "2026-10-17", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    w = directed()
    driver = Driver(w, compression=60.0)
    app = create_app(driver, game="a test", consent_records=records, saves_dir=tmp_path / "s")
    with TestClient(app) as http:
        bare = world_at(49.5, -5.5)
        assert "director" not in bare.stations.names()
        a = http.post("/api/agents/director", json={"model_name": WEIGHTS, "door": "runner"}).json()
        assert a.get("key") and "taking the station of the director" in json.dumps(a)
        assert SESSION_DIRECTOR in json.dumps(a)
        h = w.agents[DIRECTOR]
        assert h.model_name == WEIGHTS and "world_order" in h.tool_names
        assert "world_order" in json.dumps(a) and "truth" in json.dumps(a)
        r = http.post(
            "/api/agents/director/reply",
            json={
                "text": "A sail for the morning.",
                "calls": [{"name": "world_order", "args": {"text": FAR_BRIG}}],
                "key": a["key"],
            },
        ).json()
        assert "Done:" in json.dumps(r)
        assert w.vessels.find("Nancy") is not None
        assert "A sail for the morning." in log_texts(w)  # the free text, a thought
        assert not [e for e in w.log.all() if "A sail for the morning" in e.text]
        agents = http.get("/api/agents").json()
        assert DIRECTOR in json.dumps(agents)
        # a second door for another station is refused the director's tools
        assert "truth" not in T.tool_names()


def test_a_scenario_file_gives_the_brief_and_a_bad_one_is_refused_at_the_load(tmp_path):
    from freesail.world.scenarios import ScenarioError, load_scenario, make_scenario_world

    base = (
        "name: x\nseed: 7\nstart: 1805-06-12T05:00\nposition: {lat_deg: 49.6, lon_deg: -5.4}\n"
        "region: channel-west\nship: {file: data/ships/topsail-schooner.yaml}\n"
    )
    good = tmp_path / "a.yaml"
    good.write_text(base + "director: {brief: quiet-passage, models: [], seats: 1}\n")
    sf = load_scenario(good)
    assert sf.scenario.director["brief"]["name"] == "A quiet passage"
    w = make_scenario_world(sf)
    assert D.brief_of(w).name == "A quiet passage" and w.stations.aboard(DIRECTOR)
    assert not [i for i in w.inputs if "director_brief" in i]  # the scenario's, not an input
    saved = w.save()
    assert saved["scenario"]["director"]["brief"]["name"] == "A quiet passage"
    copy = replay.replay(saved, ship_factory)
    assert D.brief_of(copy).name == "A quiet passage" and copy.stations.aboard(DIRECTOR)
    bad = tmp_path / "b.yaml"
    bad.write_text(base + "director: {brief: {cadence: minute}}\n")
    with pytest.raises(ScenarioError, match="director.brief"):
        load_scenario(bad)


def test_the_fake_director_at_the_console_seat_and_the_owner_at_the_door_are_told_apart():
    """The owner's `world:` order is never doubted and never the director's; the
    director's log keeps the director's acts only."""
    w = directed()
    D.direct(w, FAR_BRIG, by="the test")
    e = w.world_order(NEAR_CUTTER, source="the owner")
    assert e.data["result"] == "done" and w.vessels.find("Lark") is not None
    assert not any("Lark" in t for t in log_texts(w))
    assert [i for i in w.inputs if i.get("source") == "the owner"]


def test_stand_down_leaves_the_note_in_the_directors_log_and_the_play_log_says_only_that_it_left():
    w = directed()
    h = seat_director(w, [reply("", call("stand_down", note="Enough arranged for one day."))])
    w.run(1)
    assert h.agent.released
    assert any("Enough arranged" in t for t in log_texts(w))
    assert not [e for e in w.log.all() if "Enough arranged" in e.text]  # the log's alone
    left = [e for e in w.log.all() if e.kind in ("agent.handover", "agent.stopped")]
    assert left and all(e.actor == "the director" and for_the_record(e) for e in left)
    assert any("leaves a note in its log" in e.text for e in left)
    assert not any("Enough arranged" in e.text for e in left if e.kind == "agent.handover")


def test_the_time_and_the_dates_of_the_budget_are_the_ships():
    w = directed()
    assert D.day_of(w) == "1805-06-12"
    assert D.next_day_tick(w) == 14 * 3600  # from ten in the morning to midnight
    late = world_at_time(23, 59)
    late.run(30)
    assert D.next_day_tick(late) - late.clock.tick == 30
    assert R.director_readings(w)["stamp"]


# ---------------------------------------------------------------------------
# Package 52 (spec M7b §8, §9, §15): the director's voice
# ---------------------------------------------------------------------------


def seat_officer(w: World, script: Any) -> Harness:
    from freesail.agents.agent import officer

    fake = script if hasattr(script, "reply") else Fake(script, loop=False, when_done=reply("Aye."))
    h = Harness(
        w,
        officer(SamplingPolicy.in_lockstep(EVERY, "notable", "urgent"), world=w),
        fake,
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake officer", "mcp"
    h.start()
    return h


def sample_words(h: Harness) -> str:
    return json.dumps([t.content for t in h.turns if t.role == "data"])


def test_the_rule_of_reach_is_a_refusal_in_the_directors_log_naming_the_stations_held():
    """Spec M7b §9: the director speaks as anyone no model or player holds, never as a held
    station: refused outright in words that name the stations held, in its log, counted
    against nothing; and the same person unheld is spoken for."""
    w = directed()
    said = D.direct(w, 'say as the captain: "Make it so."', by="the test")
    assert said.startswith("Refused, by the rule of reach: Captain Bowen is the captain's")
    assert "the stations held now: the captain (Captain Bowen, the player at the prompt)" in said
    assert log_kinds(w)[-1] == "director.refused" and "rule of reach" in log_texts(w)[-1]
    assert D.budget_of(w).acts == 0 and not [e for e in w.log.all() if e.kind == "person.spoke"]
    said = D.direct(w, 'say as the carpenter: "She is making a little water, sir."', by="t")
    assert said.startswith("Done: Mr Chambers spoke on the deck") and D.budget_of(w).acts == 1


def test_a_person_made_by_the_director_is_its_act_doubted_by_the_boats_reach_and_logged():
    w = directed()
    said = D.direct(w, 'person: make "Mr Fox", a pilot, ashore at Brest', by="the test")
    assert said.startswith("Done: Mr Fox, pilot; made from words, ashore at Brest")
    said = D.direct(w, 'person: "Mr Fox" comes aboard as master', by="the test")
    assert said.startswith("Doubted, not performed: Mr Fox is ashore at Brest")
    said = D.direct(
        w, 'person: "Mr Fox" comes aboard as master [reason: a fishing boat brought him]', "t"
    )
    assert said.startswith("Done: Mr Fox came aboard from Brest")
    assert w.stations.holder("master").name == "Mr Fox"
    assert log_kinds(w)[-3:] == ["director.order", "director.doubted", "director.reentered"]


def test_a_question_to_a_person_nobody_holds_waits_for_the_director_and_is_answered_as_him():
    """Spec M7b §9: `ask the cook ...` from a station, with a director seated, goes to the
    director's next sample (and its log); the director answers as him with `say as`, which
    costs no act; the answer is the cook's words in the galley, heard within earshot, and
    goes back to the asker as a word, which wakes its stand-by."""
    w = directed()
    dh = seat_director(w, director_above_the_game([], answers={}))
    oh = seat_officer(
        w,
        [
            reply(
                "",
                call("submit_order", text="ask the cook what is for dinner"),
                call("stand_by", until="a watch"),
            ),
            "Thank you, cook.",
        ],
    )
    w.run(2 * EVERY)
    cook = w.people.find("the cook")
    assert cook is not None and cook.where == "galley"
    asked = [e for e in w.log.all() if e.kind == "agent.asked"]
    assert asked and asked[0].text == (
        f"The officer of the watch (Mr Pearce), on the quarterdeck, asks {cook.name}, the "
        "cook (in the galley): what is for dinner?"
    )
    spoke = [e for e in w.log.all() if e.kind == "person.spoke"]
    assert spoke and spoke[0].text == f"{cook.name}, the cook, in the galley: Aye, sir."
    assert "officer of the watch" in spoke[0].data["heard_by"]
    assert "whom nobody holds: what is for dinner?" in sample_words(dh)
    assert f"{cook.name}, the cook, in the galley, answers your question" in sample_words(oh)
    # the stand-by was for a watch, and the run is less: the answer woke it
    assert D.budget_of(w).acts == 0  # an answer is counted against nothing
    assert "director.asked" in log_kinds(w) and not D.questions_of(w)
    assert not oh.agent.asked  # the wait ended


def test_unanswered_the_askers_stand_by_wakes_after_a_glass():
    w = directed()
    seat_director(w, director_above_the_game([]))  # a director that never answers
    oh = seat_officer(
        w,
        [
            reply(
                "",
                call("submit_order", text="ask the cook what is for dinner"),
                call("stand_by", until="a watch"),
            ),
            "Very well.",
        ],
    )
    w.run(EVERY + A_GLASS)
    assert "No answer came from" in sample_words(oh) and "what is for dinner?) within a glass" in (
        sample_words(oh)
    )
    assert not oh.agent.asked
    assert not [e for e in w.log.all() if e.kind == "person.spoke"]


A_GLASS = 1800


def test_with_no_director_seated_the_rules_answer_as_they_did():
    """The question to the cook with no director: refused as before, in the same words
    (a world with a brief and none seated, and a world with neither); the masthead
    answers from what is in sight whoever is seated above."""
    plain = world_at(49.5, -5.5)
    briefed = directed()
    for w in (plain, briefed):
        e = w.submit("ask the cook what is for dinner")
        assert e.kind == "order.rejected" and "not an order this ship understands" in e.text
    assert w.people.find("the cook") is None
    seat_director(briefed, director_above_the_game([]))
    e = briefed.submit("ask the lookout what is in sight")
    assert e.kind == "agent.asked" and "The masthead answers" in e.text


def test_an_answer_costs_no_act_and_an_unasked_word_does():
    w = directed({"name": "one act", "budget": {"samples_a_day": 48, "acts_a_day": 1}})
    seat_director(w, director_above_the_game([]))
    w.submit("ask the cook what is for dinner")
    said = D.direct(w, 'say as the cook: "Pease and pork, sir."', by="the test")
    assert "an answer, counted against nothing; 1 act of the day's 1 left" in said
    said = D.direct(w, 'say as the cook: "And duff on Sunday."', by="the test")
    assert said.startswith("Done:") and D.budget_of(w).acts == 1


def test_a_word_said_between_people_and_heard_is_a_word_on_deck_for_the_stand_bys():
    """Spec M7b §15 (the owner's note 15 of gate m6a-2): a word said between people and
    heard by another counts as "a word on deck" for the stand-bys: the captain's word to
    the master on the quarterdeck wakes the officer standing by there; the same word from
    the cabin does not; a person's words heard in the galley do."""
    from freesail.agents.agent import master

    def stood(w: World) -> Harness:
        oh = seat_officer(w, [call("stand_by", until="a word on deck"), "Heard."])
        mh = Harness(
            w,
            master(SamplingPolicy.in_lockstep(EVERY, "notable", "urgent"), world=w),
            Fake([call("stand_by", until="a watch")], loop=True),
            save=lambda w, why: None,
        )
        mh.model_name, mh.door = "the fake master", "mcp"
        mh.start()
        w.run(60)
        assert oh.agent.standing_by
        return oh

    w = world_at(49.5, -5.5)
    oh = stood(w)
    w.submit("tell the master we make for Falmouth")
    w.run(2)
    assert not oh.agent.standing_by
    w = world_at(49.5, -5.5)
    oh = stood(w)
    w.submit("go below")
    w.submit("tell the master we make for Falmouth")
    w.run(2)
    assert oh.agent.standing_by  # said in the cabin: not heard on deck
    w.world_order('say as the cook: "Dinner, sir."', "the test")
    w.run(2)
    assert not oh.agent.standing_by


# ---------------------------------------------------------------------------
# The director's hand (spec M7b §3; package 62)
# ---------------------------------------------------------------------------

NANCY = (
    'ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth, '
    "intent: bound for Falmouth"
)


def test_the_hand_is_among_the_examples_with_its_refusal_and_the_starters_offer_it():
    """The director's station brief names the hand among the examples of reasonable orders
    (the orders are examples, not a rule), with its refusal where a captain is held; each
    starter brief offers an order by the hand as the player's own example, read to the
    director after the tone."""
    brief = D.DIRECTOR_BRIEF
    assert "'ship \"Harpy\": order heave to'" in brief and "'ship \"Harpy\": crewed'" in brief
    assert "no order goes through a captain a model or the player holds" in brief
    assert "in her own log as her captain's, never yours" in brief
    for name in D.starter_briefs():
        b = D.resolve_brief(name)
        assert any(": order " in x for x in b.examples), name
        assert "examples, not a rule" in b.body() and b.to_dict()["examples"] == list(b.examples)
    chase = D.resolve_brief("chase")
    assert chase.examples == ('ship "Harpy": order give chase',)
    assert "examples" not in D.DirectorBrief.from_dict({"name": "x"}).to_dict()
    one = D.DirectorBrief.from_dict({"examples": 'ship "A": order heave to'})
    assert one.examples == ('ship "A": order heave to',)


def test_the_dispatches_scenario_loads_with_its_brief_and_a_captain_who_reads_his_intent():
    """The owner's scenario for the director's test (package 62 found it unable to load:
    Fowey has no port file, and its intent was no intent a captain knows): the World is
    made, the director bound on the dispatches brief with the hand in its examples, and the
    rules captain reads his intent."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(ROOT / "data/scenarios/dispatches-falmouth.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    b = D.brief_of(w)
    assert b is not None and b.name == "The dispatches" and DIRECTOR in w.stations.names()
    assert 'ship "Medusa": order give chase' in b.examples
    assert w.captain.intent is not None and not w.captain.error
    assert w.business is not None and set(w.ports.ports) == {"falmouth", "plymouth"}


def test_the_fake_director_uses_the_hand_doubted_reentered_attempted_and_replayed(tmp_path):
    """A fake director puts a trader on the sea, brings her to by her captain's order,
    lets go her anchor where the chart doubts it and enters it again with its reason, and asks
    what the far shape cannot carry, logged as attempted: the director's log keeps every
    act as the director's, her story says the orders as her captain's, the play log and the
    captain's samples carry nothing of them; saved, the voyage replays by both roads to the
    same log and the same story."""
    w = directed("chase")
    ch = seat_captain(w)
    seat_director(
        w,
        director_above_the_game(
            [
                NANCY,
                'ship "Nancy": order heave to',
                'ship "Nancy": order come to an anchor',
                'ship "Nancy": order set the fore royal',
            ]
        ),
    )
    w.run(2 * EVERY)
    kinds = log_kinds(w)
    for kind in (
        "director.order",
        "director.doubted",
        "director.reentered",
        "director.unperformed",
        "director.attempted",
    ):
        assert kind in kinds, kind
    texts = log_texts(w)
    assert any(t.startswith('Given: ship "Nancy": order heave to;') for t in texts)
    assert any("fathoms by the chart" in t and t.startswith("Entered again") for t in texts)
    assert any("the orders the far shape carries are" in t for t in texts)
    v = w.vessels.find("Nancy")
    said = [s for _t, s in v.story]
    assert said[:2] == ["By the captain: heaving to.", "By the captain: coming to an anchor."]
    assert D.budget_of(w).acts == 3
    play = [e for e in w.log.all() if not for_the_record(e)]
    assert _no_director_in([e.text for e in play])
    assert not [e for e in play if "By the captain" in e.text or "Nancy" in e.text]
    samples = [t.content for t in ch.turns if t.role == "data"]
    assert not [s for s in samples if "By the captain" in json.dumps(s)]
    path = tmp_path / "hand.json"
    replay.save_to_file(w, path)
    data = replay.load_file(path)
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == w.log.digest(), road
        assert log_texts(copy) == texts, road
        assert copy.vessels.find("Nancy").story == v.story, road


# ---------------------------------------------------------------------------
# Things and transactions (spec M7b §17a; package 53b)
# ---------------------------------------------------------------------------


def test_the_brief_says_his_words_move_no_money_and_gives_things_and_sums_as_examples():
    """The station brief names a thing made or moved and the transactions among the
    examples, says that the director's words move no money and no thing and that nothing
    is set, keeps the rule of reach for a held person's keeping, and leaves the free lines
    to the people; the dispatches brief offers the sum paid and the freight."""
    brief = D.DIRECTOR_BRIEF
    for said in (
        "'aboard: a sealed packet, on the cabin table, from the Custom House'",
        "'aboard: twenty guineas paid into the purse by Mr Veale'",
        "'aboard: £6 paid from the purse to the pilot'",
        "'aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth'",
        "'aboard: a debt of £30 owed to the chandler at Plymouth'",
        "Your words move no money and no thing",
        "there is no setting of the purse or of anything else",
        "leave it where he can take it",
        "you give none, and you read them in your sample",
    ):
        assert said in brief, said
    b = D.resolve_brief("dispatches")
    assert "aboard: twenty guineas paid into the purse by Mr Veale" in b.examples
    assert "aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth" in b.examples


def test_the_director_pays_by_a_transaction_doubted_far_off_and_makes_a_thing_by_the_reach():
    """The director's door keeps the channel's doubt for a sum (a payer forty miles off is
    doubted, performed when entered again with a reason, the act and the doubt and the
    reason in his log), the purse's own line in the play log and never the order; a payment
    below nothing is answered honestly and performs nothing; a thing is made where the
    holder can take it, and refused into the keeping of a held person by the rule of
    reach."""
    from freesail.world import things as TH

    w = directed()
    assert D.direct(w, 'person: make "Mr Veale", a clerk, ashore at Plymouth', by="t").startswith(
        "Done:"
    )
    purse = w.purse.pounds
    sum_order = "aboard: twenty guineas paid into the purse by Mr Veale"
    said = D.direct(w, sum_order, by="the test")
    assert said.startswith("Doubted, not performed: Mr Veale is ashore at Plymouth")
    assert "neither aboard nor at a port" in said and w.purse.pounds == purse
    said = D.direct(w, f"{sum_order} [reason: he sent it by the pilot cutter]", by="the test")
    assert said.startswith("Done: twenty guineas (£21) paid into the purse by Mr Veale")
    assert w.purse.pounds == pytest.approx(purse + 21.0)
    assert log_kinds(w)[-1] == "director.reentered"
    assert "he sent it by the pilot cutter" in log_texts(w)[-1]
    play = [e for e in w.log.all() if not for_the_record(e)]
    assert [e.kind for e in play if "Veale" in e.text] == ["purse.received"]
    assert not [e for e in play if "aboard:" in e.text]
    D.direct(w, "aboard: £99999 paid from the purse to Mr Veale", by="t")  # the doubt seen
    said = D.direct(w, "aboard: £99999 paid from the purse to Mr Veale [reason: x]", by="t")
    assert said.startswith("Logged as attempted, not performed") and "below nothing" in said
    assert w.purse.pounds == pytest.approx(purse + 21.0)
    said = D.direct(w, "aboard: a letter for the port admiral, in the captain's keeping", by="t")
    assert said.startswith("Refused, by the rule of reach:") and "leave it where he" in said
    said = D.direct(w, "aboard: a letter for the port admiral, on the cabin table", by="t")
    assert said.startswith("Done: a letter for the port admiral made, on the table in the cabin")
    assert [t.name for t in TH.things_of(w)] == ["a letter for the port admiral"]
    # the director has no hands: a free line at his station is refused
    e = w.submit("take the letter", actor="the director")
    assert e.kind == "order.rejected" and "no hands aboard" in e.text


def test_the_dispatches_scenario_carries_the_packet_in_the_captains_keeping():
    """The owner's scenario gains the packet as a thing (package 53b, item 4): in the
    cutter's captain's keeping from the start, from the Custom House, and in the people's
    words and the truth."""
    from freesail.world import things as TH
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(ROOT / "data/scenarios/dispatches-falmouth.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    (packet,) = TH.things_of(w)
    cap = w.people.captain
    assert (packet.name, packet.keeper, packet.description) == (
        "a sealed packet",
        cap.id,
        "from the Custom House",
    )
    assert f"{cap.name}, master: " in w.readings.words("people")
    assert "a sealed packet in his keeping" in w.readings.words("people")
    assert R.director_readings(w)["things"][0].startswith(
        f"a sealed packet, in {cap.name}'s keeping"
    )
    # the cutter's company mustered (found on the way: the brief bound in the World's making
    # had built the people before the muster, the captain and the master alone)
    assert w.stations.holder("officer of the watch").role == "mate"
    # a free line at the prompt is no order of the ship's: the rules captain sails on
    w.run(60)
    commands = w.captain.commands
    e = w.submit("give the packet to Mr Veale")
    assert e.kind == "free.line" and w.captain.commands == commands
    assert not [x for x in w.log.all() if x.kind == "captain.aside"]


# Package 66: the station's line and the stand-by (the dispatches test's findings 9, 17,
# 18, 19 and 25)
# ---------------------------------------------------------------------------


def test_the_line_opens_every_sample_with_the_place_the_deck_and_the_state():
    """Every sample of a seated person opens with one line of his own, before the log: who
    he is, where he is and since when, whose the deck is, his state; it changes when he
    moves. The director's says the day's budget and whose turn the clock waits on. The
    console's `how am I` answers with the same line."""
    w = world_at(49.5, -5.5)
    h = seat_captain(w, ["go below"])
    w.run(1)
    first = next(t.content for t in h.turns if t.role == "data")
    assert list(first)[0] == "you"
    assert first["you"].startswith("You: the captain, on the quarterdeck, since 10:00; the deck ")
    assert first["you"].endswith("on your feet since 10:00.")
    w.run(2 * EVERY)
    lines = [t.content["you"] for t in h.turns if t.role == "data" and "you" in t.content]
    assert any(ln.startswith("You: the captain, in the cabin, since 10:") for ln in lines), lines
    d = directed()
    dh = seat_director(d, director_above_the_game([]))
    d.run(1)
    said = next(t.content["you"] for t in dh.turns if t.role == "data" and "you" in t.content)
    assert said.startswith("You: the director, above the game; the day's budget 1 of ")
    assert said.endswith("acts used; the clock waits on you.")
    o = world_at(49.5, -5.5)
    oh = seat_officer(o, [call("stand_by", until="a glass")])
    o.run(1)
    assert oh.line().startswith("You: Mr Pearce, the officer of the watch, on the quarterdeck")
    assert "; the deck the captain's; " in oh.line()
    o.submit("Mr Pearce, you have the deck")
    assert "; the deck yours; " in oh.line()
    said = o.submit("how am i").text
    assert said.startswith(
        "You: the captain, on the quarterdeck, since 10:00; the deck Mr Pearce's"
    )


def test_the_truth_and_the_chart_are_the_directors_meanwhile_reads():
    """The director standing by reads the truth (and the chart, a picture tool) out of turn,
    and the stand-by goes on (the dispatches test's finding 9)."""
    from freesail.agents.remote import ASIDE_TOOLS, READ_ONLY_TOOLS

    assert "truth" in READ_ONLY_TOOLS and "chart" in READ_ONLY_TOOLS
    assert "read_journal" in ASIDE_TOOLS
    w = directed()
    h = seat_director(w, [call("stand_by", until="a watch")])
    w.run(60)
    assert h.agent.standing_by
    told = h.aside(call("truth"))
    assert isinstance(told, dict) and "ships" in told and h.agent.standing_by


def test_an_officer_bound_to_nobody_on_a_merchantman_is_the_mate():
    """Where the ship is no King's ship, the officer of the watch bound to nobody is the mate
    in the harness's default words, never the first lieutenant (the dispatches scenario's
    people held a master only); a King's ship keeps the lieutenant."""
    from freesail.agents.agent import merchant_ship, officer, officer_rank
    from freesail.world.scenarios import load_scenario, make_scenario_world

    sc = load_scenario(str(ROOT / "data" / "scenarios" / "dispatches-falmouth.yaml"))
    cutter = make_scenario_world(sc, seed=7)
    # since 53b the cutter has her company and the mate holds the officer's station; sent
    # ashore, he leaves it bound to nobody, which is the case this test is about
    mate = cutter.stations.holder("officer of the watch")
    assert mate is not None and mate.role == "mate"
    e = cutter.world_order(f'person: "{mate.name}" leaves the ship at Falmouth', "the test")
    assert e.data["result"] == "done", e.text
    assert cutter.stations.holder("officer of the watch") is None
    assert merchant_ship(cutter) and officer_rank(cutter) == ("the mate", "mate")
    st = officer(world=cutter)
    assert st.person == "the mate" and st.rank == "mate"
    assert "first lieutenant" not in st.brief and "in the place of the mate" in st.brief
    frigate = world_at(49.5, -5.5)
    assert not merchant_ship(frigate) and officer_rank(frigate)[1] == "first lieutenant"


def test_the_form_is_checked_before_the_doubt_and_a_first_reason_answers_no_doubt_unseen():
    """Package 68 (the cold review of 2026-10-22, R-41): the doubt was judged before the
    form, so a malformed order came back only "doubted" and a small model took it for a
    working template; and a reason given on the first entry overrode a doubt the director
    never saw (a man carried nine miles ashore in a minute). The form is checked first and
    answered in words; a reason on the first entry is held to the doubt, which is shown,
    and the order entered again with its reason is performed."""
    w = directed(systems=[], climatology=True)
    w.run(60)
    bad = (
        'ship: a cutter "Lark" of Brixham-on-Sea at 49 32 N 5 32 W, bound from Torbay for '
        "Falmouth, British colours"
    )
    said = D.direct(w, bad, by="the test")
    assert said.startswith("The game has no way to do this as said: the nation"), said
    assert "Doubted" not in said
    said = D.direct(w, f"{NEAR_CUTTER} [reason: the story wants her near]", by="the test")
    assert said.startswith("Doubted, not performed: a sail put on the sea"), said
    assert w.vessels.find("Lark") is None and log_kinds(w)[-1] == "director.doubted"
    said = D.direct(w, f"{NEAR_CUTTER} [reason: the story wants her near]", by="the test")
    assert said.startswith("Done:") and log_kinds(w)[-1] == "director.reentered"


# ---------------------------------------------------------------------------
# Package 58a: the forms reference, the dry run, the lookups and how the world behaves
# (the cold review of 2026-10-22, R-42 and §7.1: the lugger director's four asks)
# ---------------------------------------------------------------------------

# the examples the test's seas cannot perform as they stand, and the game's honest words
# for why: the seat wants the owner's grant and a consent record; the starter briefs' own
# ships are not on the test's sea; an order that answers another (carry on, fill away) or
# wants a sail in sight of her or money in the purse
UNPERFORMED_HERE = {
    "seat: <the model's exact name> as captain of <ship> for 20 samples": "No consent",
    "unseat: <ship>": "No ship named",
    'ship "Lark": order shape a course for Falmouth': "No ship named 'Lark'",
    'ship "Nancy": order heave to': "No ship named 'Nancy'",
    'ship "Harpy": order carry on': "under no order of yours",
    'ship "Harpy": order haul off': "No sail in sight to haul off from",
    'ship "Medusa": order fill away': "She is not hove to",
    "aboard: £6 paid from the purse to the pilot": "the purse holds nothing",
    'ship "Harpy": crewed': "at full detail already",  # near: crewed by the promotion itself
}


def _forms_worlds() -> list[Any]:
    """The test's three seas for the forms, each made when first wanted: a fresh one; one
    with the brig-sloop Harpy at far detail, 46 miles off with her captain's intent; and one
    with Harpy and the frigate Medusa three miles off and crewed, in sight of the frigate,
    Mr Fox and Mr Veale aboard, a low on the systems and a packet on the cabin table. No
    brief (no limit), the weather by systems."""

    def fresh() -> World:
        w = directed(None, systems=[], climatology=True)
        w.run(60)
        return w

    def far() -> World:
        w = fresh()
        order = D.form_of("ship.new").examples[0]
        assert w.world_order(order, "the test").data["result"] == "done"
        w.run(60)
        return w

    def near() -> World:
        w = fresh()
        for order in (
            'ship: a brig-sloop "Harpy" of France at 49 32 N 5 31 W, running home to Brest, '
            "intent: run home to Brest",
            'ship: a frigate "Medusa" of Britain at 49 32 N 5 29 W, bound for Plymouth, intent: '
            "keep the station off the Deadman within 8 miles",
            'person: make "Mr Fox", a Guernsey pilot of sixty, aboard in the cabin',
            'person: make "Mr Veale", a clerk of the Custom House, aboard in the cabin',
            'weather: low "the low" radius 450 km at 1805-06-13T04:00 -300 500 1000',
            "aboard: a sealed packet, on the cabin table, from the Custom House",
        ):
            assert w.world_order(order, "the test").data["result"] == "done", order
        w.run(120)
        return w

    made: dict[str, World] = {}

    def world(name: str, make: Any) -> World:
        if name not in made:
            made[name] = make()
        return made[name]

    return [lambda: world("fresh", fresh), lambda: world("far", far), lambda: world("near", near)]


def test_every_world_order_form_has_examples_that_parse_and_that_the_game_performs():
    """The library's grammar gains 'the world orders', every form with examples a test
    performs (the lugger director's first ask: "a complete director grammar with verified
    examples"; 37% of its orders failed, learning the forms by refusal): each example
    parses to its form's channel, and its dry run on the sea it is meant for (a fresh one,
    one with her ship far off, one with her ships and people near) says it would be
    performed, or doubted with what it would then do; the few the test's seas cannot
    perform are answered in the game's honest words about the situation, never the form."""
    worlds = _forms_worlds()
    keys = [f.key for f in D.WORLD_ORDER_FORMS]
    assert len(keys) == len(set(keys)) and all(f.examples for f in D.WORLD_ORDER_FORMS)
    channels = set(WO.CHANNELS)
    for f in D.WORLD_ORDER_FORMS:
        assert f.channel in channels, f.key
        for x in f.examples:
            assert WO.parse(x).channel == f.channel, x
            said = []
            for world in worlds:
                s = D.dry_run(world(), x)
                said.append(s)
                if "it would be performed" in s or (
                    "it would be doubted" in s and "it would do this: " in s
                ):
                    break
            else:
                assert x in UNPERFORMED_HERE, (x, said)
                assert any(UNPERFORMED_HERE[x] in s for s in said), (x, said)


def test_the_briefs_examples_are_drawn_from_the_forms_never_written_apart():
    """The station brief's examples are the forms' own, and so are the starter briefs'."""
    every = set(D.every_example())
    in_brief = [x for x in every if f"'{x}'" in D.DIRECTOR_BRIEF]
    assert len(in_brief) >= 30
    assert '\'weather: low "the low" radius 450 km fronts 140 300 at 1805-06-13T04' in (
        D.DIRECTOR_BRIEF
    )
    for name in D.starter_briefs():
        for x in D.resolve_brief(name).examples:
            assert x in every, (name, x)
    grammar = T.library(world_at(49.5, -5.5), "captain", "grammar", section="the world orders")
    page = str(grammar)
    for f in D.WORLD_ORDER_FORMS:
        assert f.words in page and all(f"e.g. {x}" in page for x in f.examples), f.key


def test_a_dry_run_says_a_refusal_and_a_form_at_fault_and_is_a_read_at_the_desk():
    """The dry run answers in the channel's order: the brief's limit, the form at fault,
    the rule of reach; and at the door it is a read (it ends no stand-by, and counts
    among the reads, not the orders)."""
    w = directed("quiet-passage")
    w.run(60)
    frigate = 'ship: a frigate "Vengeance" of France at 49 00 N 6 20 W, running home to Brest'
    said = D.dry_run(w, frigate)
    assert said.startswith("Dry run, nothing performed and no act spent: it would be refused")
    assert "outside the brief" in said and w.vessels.find("Vengeance") is None
    said = D.dry_run(w, "weather: a gale from the west")
    assert "the game has no way to do this as said" in said
    assert T.is_dry_run("world_order", {"text": "x", "dry_run": "true"})
    assert not T.is_dry_run("world_order", {"text": "x"})
    from freesail.agents.remote import Desk  # noqa: F401  (the desk's aside, below)

    h = seat_director(w, [call("stand_by", until="a watch")])
    w.run(60)
    assert h.agent.standing_by
    result = h.aside(call("world_order", text=frigate, dry_run=True))
    assert str(result).startswith("Dry run") and h.agent.standing_by


def test_the_truths_lookups_a_port_the_grounds_the_systems_and_a_point():
    """The lugger director's second ask, read-only lookups: a port's places and prices, the
    fishing grounds, the systems seeded and appended with their tracks (and that they add),
    and whether a point is at sea and its depth by the chart; each a small read."""
    w = directed(None, systems=[], climatology=True)
    seat_director(w, [call("stand_by", until="a watch")])
    w.run(60)
    port = T.call(w, "director", "truth", {"ports": "Falmouth"})["ports"]
    assert port["ports"][0]["port"] == "Falmouth" and "The quay" in port["words"]
    assert port["ports"][0]["prices"]
    grounds = T.call(w, "director", "truth", {"grounds": "all"})["grounds"]
    assert grounds["grounds"] and "pilchards" in grounds["words"]
    w.world_order('weather: high "the ridge" radius 900 km at 1805-06-13T04:00 300 -500 1024', "t")
    systems = T.call(w, "director", "truth", {"systems": True})["systems"]
    ridge = [s for s in systems["systems"] if s["name"] == "the ridge"]
    assert ridge and ridge[0]["appended"] and ridge[0]["track"]
    assert "systems add" in systems["words"]
    sea = T.call(w, "director", "truth", {"at": "49 55 N 4 35 W"})
    assert sea["at"]["at_sea"] and "fathoms" in sea["at"]["words"]
    land = T.call(w, "director", "truth", {"at": "the Lizard"})
    assert not land["at"]["at_sea"] and "on the land" in land["at"]["words"]
    refused = T.call(w, "captain", "truth", {"ports": "Falmouth"})
    assert "ports" not in refused  # the lookups are the truth's, the director's alone


def test_how_the_world_behaves_is_written_from_the_code_and_says_its_figures():
    """The lugger director's fourth ask: a short page of how the world behaves, every
    figure in it the code's own constant."""
    from freesail.world import crews
    from freesail.world import orders as wo
    from freesail.world import weather as wx

    page = T._world_topic().whole
    for said in (
        f"{wx.SYSTEM_REACH_KM:g} km",
        f"{wx.APPEND_RAMP_S // 60} minutes",
        f"{wx.GEOSTROPHIC_MS_PER_HPA_PER_100KM:g} m/s",
        f"{crews.CREWED_NM:g} miles",
        f"{crews.CREWED_CAP} at once",
        f"{crews.HAND_HOLD_S // 60} minutes",
        f"{wo.LETTER_REACH_NM:g} miles",
        f"{wo.PRICE_SWING:.0%}",
        f"{wo.BOAT_REACH_NM:g} miles",
        f"{wo.LOW_DEEP_HPA:g} hPa",
        f"{wo.HIGH_CEILING_MARGIN_HPA:g} hPa",
        "Systems add",
    ):
        assert said in page, said
    assert "the world: how the world behaves" in str(T.library(world_at(49.5, -5.5), "captain"))


def test_an_appended_system_grows_in_and_a_waypoint_after_an_ended_track_runs_from_now():
    """R-39's small part: a system appended in play grows in from the order's tick (an
    hour at the least, else until its first point's time), the glass never stepping; a
    waypoint appended to a track that had ended runs from where the system stands, reached
    an hour on at the soonest; a high is doubted like a low."""
    from freesail.world import weather as wx

    w = directed(None, systems=[], climatology=True)
    w.run(60)

    def glass() -> float:
        return float(w.systems.pressure_at(w.ship_x_km, w.ship_y_km))

    before = glass()
    w.world_order('weather: low "the low" radius 450 km at 1805-06-12T13:00 0 0 990', "t")
    readings = [glass()]
    for _ in range(12):
        w.run(900)
        readings.append(glass())
    steps = [a - b for a, b in zip(readings, readings[1:], strict=False)]
    assert abs(readings[0] - before) < 0.05  # nothing at the order's tick
    assert max(steps) < 3.0 and readings[-1] < before - 20.0  # down by degrees, all of it
    # the track ended at 13:00: a waypoint for twenty minutes on is reached an hour on
    w.run(1800)
    e = w.world_order('weather: waypoint for "the low" at 1805-06-12T13:50 100 100 1000', "t")
    assert "reached at" in e.text and "from where it stands now" in e.text
    low = w.systems.find("the low")
    assert low.track[-1].at - low.track[-2].at == dt.timedelta(seconds=wx.APPEND_RAMP_S)
    # a high above the season's ceiling is doubted, as a deep low is
    w2 = directed(None, systems=[], climatology=True)
    high = WO.parse('weather: high "the dome" radius 900 km at 1805-06-13T04:00 300 -500 1060')
    assert "above the season's ceiling" in str(WO.doubt(w2, high))
    fair = WO.parse('weather: high "the ridge" radius 900 km at 1805-06-13T04:00 900 -900 1022')
    assert WO.doubt(w2, fair) is None


# Package 67: the seat's form widened, its cost said, and the channel with the player
# ---------------------------------------------------------------------------

SEATED = "made-up-seated-model-3"


def granted(w: World, tmp_path: Path, **grant: Any) -> World:
    records = tmp_path / "consent"
    records.mkdir(exist_ok=True)
    consent.Record(
        SEATED, "a test runtime", "2026-10-23", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    w.consent_records_dir = records
    w.scenario.director = {"models": [SEATED], "seats": 4, "seats_in_voyage": 8} | grant
    return w


def test_the_seat_is_held_at_every_station_of_a_ship_and_for_a_persons_voice(tmp_path):
    """Package 67, item 4: `seat: <model> as <station> [of <ship>]` for every station a ship
    has, the player's own ship allowed by default; a person bound to a station is seated
    at it, one nobody holds as his voice; the rule of reach refuses a held station; the
    grant may keep the seats off the player's ship; a time for the door to come lapses the
    seat and the director's log says so; and `unseat:` takes the same words."""
    w = granted(directed(), tmp_path)
    put(w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth")
    own = w.ship.name
    cases = [
        (f"seat: {SEATED} as officer for 3 samples", "own/officer of the watch"),
        (
            f"seat: {SEATED} as officer of the watch of X for 3 samples",
            "ship-1/officer of the watch",
        ),
        (f"seat: {SEATED} as lookout of {own} for 1 hours, within 20 minutes", "own/lookout"),
    ]
    for text, key in cases:
        e = w.world_order(text)
        assert e.data["result"] == "done", e.text
        assert key in WO.director_seats(w)
    held = WO.director_seats(w)["own/officer of the watch"]
    assert held["what"] == f"the officer of the watch of {own}" and held["ship"] == ""
    e = w.world_order(f"seat: {SEATED} as captain for 3 samples")
    assert e.data["result"] == "refused" and "held by the player at the prompt" in e.text
    e = w.world_order(f"seat: {SEATED} as officer of the watch of Nowhere for 3 samples")
    assert e.data["result"] == "refused" and "No ship named 'Nowhere'" in e.text
    e = w.world_order(f"seat: {SEATED} as officer for 3 samples")
    assert e.data["result"] == "refused" and "already" in e.text
    # the master by his name: the station he holds
    e = w.world_order(f"seat: {SEATED} as {w.stations.holder('master').name} for 2 samples")
    assert e.data["result"] == "done" and "the master of" in e.text
    # the seat's result says its cost's shape and how its door comes
    assert "a model run on the owner's key" in e.text and "counted from its door's" in e.text
    assert "where the game has a harbour (py -m freesail)" in e.text and "--station" in e.text
    # the lookout's door never came within twenty minutes: the seat lapses
    w.run(21 * 60)
    assert "own/lookout" not in WO.director_seats(w)
    assert any(t.startswith("The seat lapsed") for t in log_texts(w))
    # the grant keeps the seats off her: refused on her, another ship's as before
    for key in list(WO.director_seats(w)):
        WO.director_seats(w).pop(key)
    w.scenario.director["seats_on_the_players_ship"] = False
    e = w.world_order(f"seat: {SEATED} as lookout for 2 samples")
    assert e.data["result"] == "refused" and "seats_on_the_players_ship: false" in e.text
    e = w.world_order(f"seat: {SEATED} as captain of X for 2 samples")
    assert e.data["result"] == "done", e.text
    assert w.world_order("unseat: X, the brig is home").data["result"] == "done"
    # a person nobody holds: his voice, ashore where he is
    w.scenario.director["seats_on_the_players_ship"] = True
    made = w.world_order('person: make "Mr Veale", a merchant of fifty, ashore at Falmouth')
    assert made.data["result"] == "done", made.text
    e = w.world_order(f"seat: {SEATED} as Mr Veale for 5 samples")
    assert e.data["result"] == "done" and "as the voice of Mr Veale" in e.text
    assert w.stations.kind_of("mr veale") == "passenger"
    assert w.stations.holder("mr veale").name == "Mr Veale"
    e = w.world_order(f"seat: {SEATED} as Mr Nobody for 5 samples")
    assert e.data["result"] == "refused" and "Nobody answers to 'Mr Nobody'" in e.text
    e = w.world_order("unseat: Mr Veale, enough of him")
    assert e.data["result"] == "done" and "mr veale" not in w.stations.names()
    # nothing of the seats in the play log: the orders are for the record
    assert not [x for x in w.log if not for_the_record(x) and "seat" in x.text.lower()]


def test_the_seats_spending_is_in_the_directors_budget_line_and_its_brief_says_the_cost(
    tmp_path,
):
    """Package 67, item 3: the director's brief says what a seat costs and the channel with
    the player; the day's budget line names the seats held and their spending."""
    w = granted(directed(), tmp_path)
    brief = D.station_brief_text(w)
    assert "A seat costs the owner money." in brief and "paid for by the owner" in brief
    assert "answer the player:" in brief and "phrased without world detail" in brief
    assert brief.index("A seat costs") < brief.index("The player's brief:")
    assert "The seats held" not in D.budget_words(w)
    w.world_order(f"seat: {SEATED} as officer for 20 samples")
    assert D.budget_words(w).endswith(
        f"The seats held, on the owner's key: {SEATED} as the officer of the watch of "
        f"{w.ship.name}, held for 20 samples, no door yet."
    )


def test_the_players_word_and_the_directors_answer_by_every_road_and_none_in_the_play_log():
    """Package 67, item 5: `director: <words>` at the browser's order box goes to the
    director's log, its next sample (a word, which wakes a stand-by) and the pane, with no
    director seated said so; the brief's words are still the brief's; the director answers
    by a world order, by a reply that opens with 'answer the player:' or by the answer
    tool, each to the driver's listeners and its log and none to the play log, no act
    counted; the save replays."""
    from freesail.ui.console import director_brief_words, director_word
    from freesail.ui.server import Driver

    assert director_word("director: is the wind to stay west?") == "is the wind to stay west?"
    assert director_word("director: brief a quiet passage") is None
    assert director_word("director: budget 60 samples") is None
    assert director_word("director:") is None
    assert director_brief_words("director: is the wind to stay west?") is None
    assert director_brief_words("director: brief quiet-passage") == "quiet-passage"
    w = directed()
    driver = Driver(w, compression=1.0)
    sent: list[dict[str, Any]] = []
    driver.add_listener(sent.append)
    e = driver.submit("director: is the wind to stay west?")
    assert e.kind == "query.director_word" and "no director is seated now" in e.text
    assert [m["line"]["text"] for m in sent if m["type"] == "channel"] == [
        "is the wind to stay west?"
    ]
    script = [
        reply("", call("stand_by", until="a watch")),
        reply("answer the player: It may back south by night.", call("stand_by", until="a watch")),
        reply(
            "",
            call("answer", text="answer the player: The glass will tell you first."),
            call("stand_by", until="a watch"),
        ),
        reply("", call("stand_by", until="a watch")),
    ]
    h = seat_director(w, Fake(script))
    w.run(60)
    acts = D.budget_of(w).acts
    driver.submit("director: and the fog?")
    w.run(60)
    assert h.agent.standing_by
    driver.submit("director: thank you")
    w.run(60)
    answers = [m["line"]["text"] for m in sent if m["type"] == "channel"]
    assert answers == [
        "is the wind to stay west?",
        "and the fog?",
        "It may back south by night.",
        "thank you",
        "The glass will tell you first.",
    ]
    assert D.budget_of(w).acts == acts  # an answer is no act
    assert [x["from"] for x in D.channel_lines(w)] == [
        "the player",
        "the player",
        "the director",
        "the player",
        "the director",
    ]
    for line in answers:
        assert not [x for x in w.log if line in x.text]
    copy = replay.replay(json.loads(json.dumps(w.save())), ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert [x["text"] for x in D.channel_lines(copy)][:2] == answers[:2]
