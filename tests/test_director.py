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
        'ship: a cutter "Ashore" of Britain at 50 05 N 5 15 W, bound for Falmouth': "on the land",
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
        'say as the carpenter: "She is making a little water, sir."',
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
    assert len(WO.aboard_table()) == 4
    assert "aboard" in WO.CHANNELS and WO.recognises("aboard: a cask found stove")


# ---------------------------------------------------------------------------
# §4: the brief and its limits, enforced by the channel
# ---------------------------------------------------------------------------


def test_the_starter_briefs_load_and_the_console_brief_is_words_alone():
    names = D.starter_briefs()
    assert names == ["chase", "hard-cruise", "interesting-passage", "quiet-passage"]
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
