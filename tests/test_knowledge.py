"""The place's knowledge (package 65, step 1; `docs/design/Design-PlaceKnowledge.md` §2 to
§5; decision 59): a sample carries what the person's place allows. The lines by where they
are heard, every kind the code writes placed or at the deck by design; the readings by
place, with where each is to be had; the harness's sample, the brief head and the handover
fold by the person's senses; a reading asked where it is not to be had answered with where;
the lookout's masthead; a man with the deck kept from going below; a tripwire judged below
fired as the officer's call; `knowledge: all`. Truths 7-370 (in part), 7-373, 7-376, 7-380,
7-383 and 7-386 are in `tests/test_known_truths.py` and call these."""

from __future__ import annotations

import pathlib
import re
from datetime import datetime
from typing import Any

import pytest

from freesail.agents import Fake, Harness, SamplingPolicy, call, reply, tools
from freesail.agents.agent import PLACE_KNOWLEDGE_WORDS, captain, lookout, officer
from freesail.agents.model import DATA, OPERATOR
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.events import Event, Severity
from freesail.core.world import Scenario
from freesail.world import knowledge as K

FRIGATE = "data/ships/frigate-36.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}
ROOT = pathlib.Path(__file__).resolve().parents[1]


def world_at(where=OFF_THE_LIZARD, start=datetime(1805, 6, 10, 10, 0), **kw):
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=250.0,
        position=where,
        chart="channel-west",
        glass=True,
        **kw,
    )
    w = make_world(7, FRIGATE, sc)
    w.submit("set plain sail")
    w.run(120)
    return w


def seated(w, script, make=captain, every=600, loop=False, **kw) -> Harness:
    st = make(SamplingPolicy.in_lockstep(every, "notable", "urgent"), world=w, **kw)
    stand = reply("", call("stand_by", until="a glass"))
    fake = Fake(script, loop=True) if loop else Fake(script, when_done=stand)
    h = Harness(w, st, fake, save=lambda _w, _why: None)
    h.model_name, h.door = "the fake", "runner"
    h.start()
    return h


def samples(h: Harness) -> list[dict[str, Any]]:
    return [t.content for t in h.turns if t.role == DATA and "tool_results" not in t.content]


def results(h: Harness, name: str) -> list[Any]:
    out = []
    for t in h.turns:
        if t.role == DATA and "tool_results" in t.content:
            out += [r["result"] for r in t.content["tool_results"] if r.get("name") == name]
    return out


def event(kind: str, text: str = "", **data: Any) -> Event:
    return Event(0, datetime(1805, 6, 10, 10, 0), Severity.ROUTINE, kind, text or kind, data=data)


# ---------------------------------------------------------------------------
# The lines by where they are heard (§4)
# ---------------------------------------------------------------------------


def code_kinds() -> set[str]:
    """Every dotted string literal in the code that is a kind of log line (the families
    that are no kind, a file's or a part's name, left out: `knowledge.NOT_KINDS`)."""
    pat = re.compile(r'"([a-z_]+\.[a-z_]+)"')
    kinds: set[str] = set()
    for p in (ROOT / "freesail").rglob("*.py"):
        for m in pat.finditer(p.read_text(encoding="utf-8")):
            k = m.group(1)
            if k.endswith((".yaml", ".html", ".json", ".py", ".md")):
                continue
            if k.split(".", 1)[0] in K.NOT_KINDS:
                continue
            kinds.add(k)
    return kinds


def test_every_kind_the_code_writes_is_placed_or_falls_to_the_deck_by_design():
    """The lead's guard (the design's §4): every kind of line the code writes is in the
    reach table by its kind or by its family, so that a new family appears placed or the
    suite fails; the default for a kind nobody placed is the deck, never everywhere."""
    kinds = code_kinds()
    assert len(kinds) > 150
    unplaced = sorted(k for k in kinds if k not in K.REACH and k.split(".", 1)[0] not in K.FAMILIES)
    assert unplaced == [], f"kinds with no reach, to be placed in knowledge.REACH: {unplaced}"
    assert K.DEFAULT_REACH == "deck"
    assert K.reach_of("newfamily.line") == "deck"
    # the classes are the design's and no other
    assert set(K.REACH.values()) | set(K.FAMILIES.values()) <= {
        "aboard",
        "wakes",
        "deck",
        "aft",
        "said",
        "person",
        "place",
        "port",
        "record",
    }


def test_the_reach_of_the_hulls_sounds_the_deck_and_the_record():
    """The bell, a gun and all hands reach the hold; the deck's work does not; the sail
    work reaches the cabin and not the gunroom; the record's lines reach everyone; a
    sleeper is woken by a gun and not by the bell."""
    deck = K.Senses(K.senses_of_place("quarterdeck"), ("aboard", "h", "quarterdeck"), "quarterdeck")
    hold = K.Senses(K.senses_of_place("hold"), ("aboard", "h", "hold"), "hold")
    cabin = K.Senses(K.senses_of_place("cabin"), ("aboard", "h", "cabin"), "cabin")
    gunroom = K.Senses(K.senses_of_place("gunroom"), ("aboard", "h", "gunroom"), "gunroom")
    asleep = K.Senses(frozenset({K.ASLEEP}), ("aboard", "h", "gunroom"), "gunroom", asleep=True)
    bell, gun, hands = event("clock.bell"), event("guns.fire"), event("crew.all_hands")
    trim, brace = event("sail.trimmed"), event("yard.braced_round")
    saved = event("driver.saved")
    hail = event("lookout.sighting", seen_as="sail")
    for e in (bell, gun, hands, trim, brace, saved, hail):
        assert K.reaches(None, deck, e)
    assert all(K.reaches(None, hold, e) for e in (bell, gun, hands, saved))
    assert not any(K.reaches(None, hold, e) for e in (trim, brace, hail))
    assert all(K.reaches(None, cabin, e) for e in (bell, gun, trim, brace))
    assert not K.reaches(None, cabin, hail)
    assert not any(K.reaches(None, gunroom, e) for e in (trim, brace, hail))
    assert K.reaches(None, asleep, gun) and K.reaches(None, asleep, hands)
    assert not any(K.reaches(None, asleep, e) for e in (bell, trim, saved, hail))
    # the sounds of sail work in the cabin (the lead's ruling): the sound, not the figure
    set_ = Event(
        0,
        datetime(1805, 6, 10),
        Severity.ROUTINE,
        "sail.set",
        "Fore topsail set.",
        subject="fore.topsail",
        data={"sail": "fore.topsail"},
    )
    assert K.as_heard(set_, cabin) == "Sail handled overhead."
    assert K.as_heard(brace, cabin) == "The hands at the braces."
    assert K.as_heard(set_, deck) is None and K.as_heard(set_, gunroom) is None
    assert K.as_heard(event("evolution.started", "Tacking."), cabin) is None


def test_the_senses_of_each_place_and_the_readings_places():
    """The table of §3 and §5: the open deck's three places share the deck's senses, aloft
    is its own, the cabin's and the gunroom's theirs, a room below its own; every reading
    row carries its places, the deck's by default, and the cabin's are the design's."""
    assert K.senses_of_place("quarterdeck") == K.senses_of_place("galley") == {K.ABOARD, K.DECK}
    assert K.senses_of_place("tops") == {K.ABOARD, K.ALOFT}
    assert K.senses_of_place("cabin") == {K.ABOARD, K.CABIN}
    assert K.senses_of_place("hold") == {K.ABOARD, "hold"}
    assert K.senses_of_place("shore") == {K.ASHORE}
    assert K.senses_of_place("boat") == {K.DECK, "boat"}  # within a pull of her, her deck's
    rows = [r for r in R.REGISTRY if not r.is_absent and r.kind not in R.DRIVER_KINDS]
    assert all("deck" in r.where or K.ABOARD in r.where or r.per_asker for r in rows)
    cabin = K.Senses(K.senses_of_place("cabin"), ("aboard", "h", "cabin"), "cabin")
    had = {r.id for r in rows if K.reading_here(r, cabin) and r.parametric is None}
    for must in ("heading", "glass", "tendency", "depth_of_water", "reckoning", "heel", "time"):
        assert must in had, must
    for not_here in ("speed", "true_wind_speed", "depth", "in_sight", "sail_in_sight", "helm"):
        assert not_here not in had, not_here
    gunroom = K.Senses(K.senses_of_place("gunroom"), ("aboard", "h", "gunroom"), "gunroom")
    assert not K.reading_here(R.REGISTRY.get("heading"), gunroom)  # the tell-tale is the cabin's
    assert K.reading_here(R.REGISTRY.get("reckoning"), gunroom)
    assert K.where_words(R.REGISTRY.get("depth")) == "the lead is cast on deck"
    assert K.where_words(R.REGISTRY.get("helm")) == "to be had on deck"
    assert K.where_words(R.REGISTRY.get("in_sight")) == "to be had on deck or aloft"


# ---------------------------------------------------------------------------
# The harness's sample by place (truths 7-370 in part, 7-373, 7-376, 7-380)
# ---------------------------------------------------------------------------


def the_captain_in_the_cabin() -> tuple[Any, Harness]:
    w = world_at()
    script = [
        reply("", call("submit_order", text="go below")),
        reply("", call("readings")),
        reply("", call("stand_by", until="a glass")),
    ]
    h = seated(w, script)
    w.run(60)
    assert w.people.captain.where == "cabin"
    return w, h


def test_a_captain_in_the_cabin_reads_the_cabins_and_not_the_decks():
    """Truth 7-370 in part: his sample carries no deck reading and says in one line where
    they are to be had; the glass, the tell-tale's heading and the chart's rows are his;
    the `readings` tool lists the rest under `not_here`; the deck's work reaches him as a
    sound and the lookout's sighting not at all, while the bell does."""
    w, h = the_captain_in_the_cabin()
    w.run(3700)  # past the bells of 10:30 and 11:00, which reach him below
    below = [s for s in samples(h) if "in the cabin" in str(s.get("you"))]
    assert below, [s.get("you") for s in samples(h)]
    s = below[-1]
    keys = set(s["readings"])
    assert not keys & {"speed", "true_wind_speed", "sail_in_sight", "depth", "helm", "sails"}
    # the deltas (58a): the cabin's rows that did not change are not said again; the tool
    # gives every row he has there
    assert "heading" in below[0]["readings"] or "heading" in results(h, "readings")[0]
    line = s["readings_elsewhere"]
    assert line.startswith("Not to be had in the cabin:")
    assert "the lead is cast on deck" in line and "the log is hove on deck" in line
    tool = results(h, "readings")[0]
    assert "speed" not in tool and "heading" in tool and "glass" in tool
    assert tool["where_you_are"] == "in the cabin"
    assert tool["not_here"]["speed"] == "the log is hove on deck"
    assert tool["not_here"]["depth"] == "the lead is cast on deck"
    # the lines: the bell reaches, the sighting does not, the sail work is a sound
    kinds = {ln["kind"] for s_ in below for ln in s_["log"]}
    assert "clock.bell" in kinds
    assert not kinds & {"lookout.sighting", "lookout.made_out", "helm.order"}
    sail_lines = [ln for s_ in below for ln in s_["log"] if ln["kind"].startswith("sail.")]
    if sail_lines:
        assert all(
            ln["text"]
            in (
                "Sail handled overhead.",
                "Sail filled again.",
                "Sail drawing again.",
                "Sail aback overhead.",
                "Sail shaking overhead.",
            )
            for ln in sail_lines
        ), sail_lines
    # on deck again, every row comes back as the delta and the line is gone
    assert "readings_elsewhere" not in samples(h)[0]


def test_a_reading_asked_where_it_is_not_to_be_had_is_answered_with_where():
    """Truth 7-373: at the prompt (`what is the depth` from the cabin) the answer says where
    the lead is cast and where the asker is, not the figure; the same reading from the deck
    gives the figure; a reading the cabin has (the glass) answers there; a standing order's
    condition and the rules read the ship as before."""
    w = world_at()
    before = w.submit("what is the depth").text
    assert "you are" not in before and before.startswith("The depth:"), before
    assert w.submit("go below").kind == "captain.below"
    e = w.submit("what is the depth")
    assert e.kind == "query.reading" and e.data.get("elsewhere") is True
    assert e.text == "The depth: the lead is cast on deck; you are in the cabin."
    assert w.submit("the speed").text == "The speed: the log is hove on deck; you are in the cabin."
    glass = w.submit("the glass").text
    assert glass.startswith("The glass:") and "you are in the cabin" not in glass
    heading = w.submit("the heading").text
    assert "you are in the cabin" not in heading  # the tell-tale compass (the lead's ruling)
    assert w.submit("come on deck").kind == "captain.on_deck"
    assert "you are" not in w.submit("what is the depth").text
    # the book reads the ship, not a person
    w.submit("go below")
    w.submit('standing order "deep": when the depth is under 200 fathoms then heave the lead')
    assert "deep" in str(w.standing.book.lines())


def test_the_handover_fold_keeps_the_place():
    """Truth 7-376: a handover note written in the cabin folds the conversation into a brief
    head whose readings are the cabin's and whose lines are those that reached him there."""
    w = world_at()
    script = [
        reply("", call("submit_order", text="go below")),
        reply("", call("stand_by", until="a glass")),
        reply("", call("handover_note", note="Below, writing; the deck the officer's.")),
        reply("", call("stand_by", until="a glass")),
    ]
    h = seated(w, script)
    w.run(2 * 1800 + 120)
    assert w.people.captain.where == "cabin"
    # the brief says the rule once, in its head
    head = [t.content for t in h.turns if t.role == OPERATOR][0]
    assert PLACE_KNOWLEDGE_WORDS in head
    # the fold's turn carries the readings whole as they stood, the cabin's (58a: the first
    # sample after a fold is whole)
    folded = [t.content for t in h.turns if t.role == DATA and "folded" in t.content]
    assert folded, "nothing was folded"
    rows = folded[-1]["readings"]
    assert "heading" in rows and "glass" in rows and "depth_of_water" in rows
    assert not set(rows) & {"speed", "true_wind_speed", "sails", "sail_in_sight", "helm"}
    assert "in the cabin" in str(h.line())


def test_knowledge_all_turns_the_rule_off():
    """Decision 59's key: under `knowledge: all` a captain in the cabin reads every row and
    every line, and a reading asked there gives the figure."""
    w = world_at(knowledge="all")
    assert K.all_known(w)
    h = seated(w, [reply("", call("submit_order", text="go below"))])
    w.run(1300)
    below = [s for s in samples(h) if "in the cabin" in str(s.get("you"))]
    assert below and "speed" in below[-1]["readings"] and "readings_elsewhere" not in below[-1]
    assert "you are in the cabin" not in w.submit("what is the depth").text
    assert w.scenario.to_dict()["knowledge"] == "all"
    assert "knowledge" not in world_at().scenario.to_dict()


def test_the_scenario_key_is_read_and_refused_in_words(tmp_path):
    from freesail.world.scenarios import ScenarioError, load_scenario

    p = tmp_path / "k.yaml"
    p.write_text("name: k\nknowledge: all\nship:\n  file: data/ships/frigate-36.yaml\n")
    assert load_scenario(p).scenario.knowledge == "all"
    p.write_text("name: k\nknowledge: some\nship:\n  file: data/ships/frigate-36.yaml\n")
    with pytest.raises(ScenarioError, match="'place'.*'all'"):
        load_scenario(p)


# ---------------------------------------------------------------------------
# The masthead (truth 7-383)
# ---------------------------------------------------------------------------


def test_the_lookouts_station_reads_the_horizon_and_no_instrument():
    """Truth 7-383: the lookout's sample carries the horizon's rows and the heading, no log,
    no lead, no glass; a `say` on the quarterdeck does not reach it, `say to the lookout`
    does, and the sail work does."""
    w = world_at()
    h = seated(w, [reply("", call("stand_by", until="a glass"))], make=lookout)
    first = samples(h)[0]
    keys = set(first["readings"])
    assert {"in_sight", "nearest_land", "heading", "sail_in_sight", "lookout"} <= keys
    assert not keys & {"speed", "depth", "glass", "helm", "reckoning", "leeway"}
    assert "the log is hove on deck" in first["readings_elsewhere"]
    w.submit("say the glass is falling")
    w.submit("say to the lookout keep a sharp eye to leeward")
    w.submit("set the main royal")
    w.run(1900)
    later = samples(h)[1:]
    kinds = {ln["kind"] for s in later for ln in s["log"]}
    assert "agent.spoke" not in kinds  # the quarterdeck's conversation does not carry aloft
    assert any("sharp eye" in str(s.get("word")) for s in later)  # a word to him does
    assert any(k.startswith(("sail.", "evolution.")) for k in kinds)


# ---------------------------------------------------------------------------
# The deck not left (the lead's ruling 6); a tripwire below as the officer's call (7-387)
# ---------------------------------------------------------------------------


def test_an_officer_with_the_deck_does_not_go_below_and_may_go_aloft():
    """The lead's ruling on §12: `go below` and `go to <a place below>` are refused to a
    station with the deck below the captain's, in words naming hand_over; `go aloft` is
    allowed; without the deck he goes below as 53 let him; the captain goes below as he
    always did."""
    w = world_at()
    h = seated(w, [reply("", call("stand_by", until="a glass"))], make=officer)
    assert w.submit("you have the deck").kind == "agent.deck"
    said = tools.call(w, "officer of the watch", "submit_order", {"text": "go below"})
    assert "You have the deck: it is not left for the gunroom" in said and "hand_over" in said
    said = tools.call(w, "officer of the watch", "submit_order", {"text": "go to the hold"})
    assert "it is not left for the hold" in said
    pearce = w.stations.holder("officer of the watch")
    assert pearce.where == "quarterdeck"
    said = tools.call(w, "officer of the watch", "submit_order", {"text": "go aloft"})
    assert said == f"{pearce.name} went aloft into the tops."
    tools.call(w, "officer of the watch", "submit_order", {"text": "come on deck"})
    assert w.submit("I have the deck").kind == "agent.deck"
    said = tools.call(w, "officer of the watch", "submit_order", {"text": "go below"})
    assert said == f"{pearce.name} went below to the gunroom."
    assert h.agent.deck is False
    assert w.submit("go below").kind == "captain.below"  # the captain's deck is by right


def test_a_tripwire_judged_below_wakes_as_the_officers_call():
    """Truth 7-387: a captain in the cabin standing by for `speed under 20 knots` (which holds
    at once) is woken with 'the officer of the watch sends down to you' before the words, the
    log being hove on deck; the same stand-by on deck wakes as 58a's. A tripwire the cabin
    can judge (the depth by the chart) wakes as 58a's there too."""
    w = world_at()
    script = [
        reply("", call("submit_order", text="go below")),
        reply("", call("stand_by", until="speed under 20 knots")),
        reply("", call("stand_by", until="depth under 200 fathoms")),
        reply("", call("stand_by", until="a glass")),
    ]
    h = seated(w, script)
    w.run(130)
    woke = [e.text for e in w.log if e.kind == "agent.resumed"]
    assert len(woke) >= 2, woke
    assert "sends down to you: speed under 20 knots" in woke[0], woke
    assert "sends down" not in woke[1] and "depth under 200 fathoms" in woke[1].lower(), woke
    pearce = w.stations.holder("officer of the watch")
    assert pearce.name.split()[-1] in woke[0]
    w2 = world_at()
    h2 = seated(w2, [reply("", call("stand_by", until="speed under 20 knots"))])
    w2.run(130)
    woke2 = [e.text for e in w2.log if e.kind == "agent.resumed"]
    assert woke2 and "sends down" not in woke2[-1] and "speed under 20 knots" in woke2[-1].lower()
    assert h.agent.state == h2.agent.state


# ---------------------------------------------------------------------------
# A station reseated after a checkpoint, and on a hull that sleeps (truth 7-385); the pace
# (truth 7-386)
# ---------------------------------------------------------------------------


def test_a_station_restored_from_a_checkpoint_keeps_its_place_and_its_senses(tmp_path):
    """Truth 7-385 in part: a captain's station in the cabin, saved and read back, samples the
    cabin's (the person's place persists with the save; the filter keeps nothing of its own)."""
    from freesail.core import replay as replay_mod

    w, h = the_captain_in_the_cabin()
    w.run(60)
    assert "cabin" in h.senses().place
    path = replay_mod.write_checkpoint(w, tmp_path / "below.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    assert c.people.captain.where == "cabin"
    h2 = c.agents["captain"]
    assert h2.senses().place == "cabin" and not h2.senses().everything
    readings = h2._sample_readings(c, h2.senses())
    assert "heading" in readings and "speed" not in readings


def test_a_station_on_a_hull_that_sleeps_and_wakes_reads_by_its_place():
    """Truth 7-385: a fake at the captain's station of a brig beside the frigate goes below;
    sailed beyond the range she sleeps in the far shape (84), and his senses are the
    cabin's still; brought near she wakes, and the same. The place rule reads the person's
    place in her, whatever her shape."""
    from freesail.agents.agent import captain as captain_station
    from freesail.world import crews as C
    from tests.test_crews import _asleep, hove_to_world, put

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    hull = b.crew
    assert hull is not None and hull.shape == "full"
    policy = SamplingPolicy.in_lockstep(600, "notable", "urgent")
    script = [reply("", call("submit_order", text="go below"))]
    h = Harness(
        hull,
        captain_station(policy, 3600, world=hull),
        Fake(script, when_done=reply("", call("stand_by", until="a glass"))),
    )
    h.model_name, h.door = "the fake", "runner"
    h.start()
    w.run(60)
    assert hull.people.captain.where == "cabin" and h.senses().place == "cabin"
    _asleep(w, b)
    assert hull.shape == "far"
    assert hull.people.captain.where == "cabin" and h.senses().place == "cabin"
    assert not any("speed" in s["readings"] for s in samples(h)[1:])
    b.position = w.position.advanced(0.0, 3.0 * 1852.0)
    w.run(61)
    assert hull.shape == "full"
    assert h.senses().place == "cabin"
    assert C is not None


@pytest.mark.pace
def test_the_filters_cost_measured_with_three_stations_seated():
    """Truth 7-386 (informative, `pace`): the frigate under plain sail with three fakes
    seated (the captain's, the officer's and the lookout's stations, each standing by a
    glass) in truth 51's form (a thousand ticks to settle, the best of three thousands),
    `knowledge: place` against `knowledge: all` on the same tree. The filter is a lookup a
    line and a set test a row at a sampling point, and the per-tick scan of a stand-by's new
    lines; asserted within a band: the rule costs under a fifth of the pace."""
    import time

    def measure(knowledge: str) -> float:
        w = world_at(knowledge=knowledge)
        for make in (captain, officer, lookout):
            seated(w, [reply("", call("stand_by", until="a glass"))], make=make, every=1800)
        w.run(1000)
        best = 0.0
        for _ in range(3):
            t0 = time.perf_counter()
            w.run(1000)
            best = max(best, 1000 / (time.perf_counter() - t0))
        return best

    ruled, free = measure("place"), measure("all")
    print(f"three stations seated: knowledge place {ruled:.0f} ticks a second; all {free:.0f}")
    # the band is wide for the machine's noise (the two measures a minute apart differ by a
    # tenth either way on four cores); the figures are the record
    assert ruled >= 0.7 * free, (ruled, free)


# ---------------------------------------------------------------------------
# A reply's prose is the person's own note (§6, decision 60; step 2)
# ---------------------------------------------------------------------------


def _prose_notes(h: Harness) -> list[Any]:
    return [e for e in h.journal.entries if e.kind == "agent.note"]


def test_a_replys_prose_is_a_note_heard_by_nobody_and_a_say_is_heard():
    """Decision 60 (truth 7-379): a reply's prose is written in the station's journal under
    the model's mark and in the director's log by the station, in no log of the play, and
    no station hears it; a `say` is heard (66); prose alone where an answer was owed is
    counted as words written into the journal and nothing said, and the next sample carries
    the notice naming the tools; the director's sample carries the stations' notes."""
    from freesail.agents import director as D
    from freesail.agents import harness as harness_mod
    from tests.test_director import seat_director

    w = world_at()
    stand = reply("", call("stand_by", until="a glass"))
    director = seat_director(w, [stand])
    cap_script = {"n": 0}

    def captains_part(last, turns):
        # his first reply prose; a question answered in prose once, then with the tool
        cap_script["n"] += 1
        if cap_script["n"] == 1:
            return reply("The glass is steady; I shall keep her so.")
        if last.get("question") and cap_script["n"] == 2:
            return reply("I think not.")
        if last.get("question"):
            return reply("", call("answer", text="Shorten sail, Mr Pearce."))
        return stand

    cap = seated(w, [captains_part], loop=True)
    off_script = {"n": 0}

    def officers_part(last, turns):
        off_script["n"] += 1
        if off_script["n"] == 1:
            return reply("", call("submit_order", text="say the wind is backing, sir"))
        if off_script["n"] == 2:
            return reply("", call("submit_order", text="ask the captain whether to shorten sail"))
        return stand

    off = seated(w, [officers_part], make=officer, loop=True)
    w.run(1)
    # the captain's prose: his note, under his mark, and the director's log's, by him
    note = _prose_notes(cap)[0]
    assert note.text == "The glass is steady; I shall keep her so." and note.by == "the fake"
    assert note.line().endswith("(note) The glass is steady; I shall keep her so.")
    logged = [e for e in D.log_of(w).entries if e.kind == "agent.note"]
    assert logged[0].by == "captain"
    assert logged[0].text == "The glass is steady; I shall keep her so."
    assert not any(e.kind == "agent.note" for e in w.log)
    # the officer on the same quarterdeck heard nothing of it; the captain hears the say
    assert not [s for s in samples(off) if s.get("heard")]
    spoke = [e for e in w.log if e.kind == "agent.spoke"]
    assert spoke and "the wind is backing, sir" in spoke[0].text
    assert spoke[0].data["heard_by"] == ["captain"]
    w.run(600)
    heard = [s["heard"] for s in samples(cap) if s.get("heard")]
    assert heard and "on the quarterdeck: the wind is backing, sir" in heard[0][0]
    # the officer's question: the captain's reply of prose alone leaves it owed, counted in
    # its own words and never as "an empty reply"; the next sample names the tools; the
    # question stands until answered (29c), and the answer with the tool ends the count
    w.run(600)
    asked = [s for s in samples(cap) if s.get("question")]
    assert asked and asked[0]["question"].endswith("asks: whether to shorten sail")
    (counted,) = [e for e in cap.journal.entries if e.kind == "agent.empty_reply"]
    assert counted.text == (
        "Words written into the journal and nothing said in the world, where an answer was "
        "owed (a question); one in a row."
    )
    assert "I think not." in [e.text for e in _prose_notes(cap)]
    notices = [n for s in samples(cap) if s.get("notices") for n in s["notices"]]
    assert harness_mod.NOTE_NOT_HEARD.format(owed="a question") in notices
    said = [e for e in w.log if e.kind == "agent.said"]
    assert said and said[0].text.endswith("Shorten sail, Mr Pearce.")
    assert cap.agent.empty_count == 0 and cap.agent.empty_noted == 0
    # the director's sample carries the stations' notes since its last, and no one else's
    noted = [s["notes"] for s in samples(director) if s.get("notes")]
    assert noted and noted[0][0].endswith("the captain: The glass is steady; I shall keep her so.")
    assert (
        all("I think not." in n for s in noted[1:] for n in s if "captain" in n) or len(noted) == 1
    )
    assert not [s for s in samples(cap) if s.get("notes")]
    # the words the harness says of it
    assert "Your reply's prose is your own note" in PLACE_KNOWLEDGE_WORDS
    assert "A word to a person is no order of the ship" in PLACE_KNOWLEDGE_WORDS


def test_the_wakes_reason_names_the_speaker_and_the_kind():
    """The owner's point of 2026-11-05 (the fully crewed brig): a station woken by a word
    was told "a word from the captain" whoever spoke. The reason names the speaker and the
    kind: a word, a question or an answer from whom; the prompt's own tell is the captain's
    (`A_WORD`); a word kept for a station nobody held names itself; the log's line says the
    same."""
    from freesail.agents.agent import master
    from freesail.agents.harness import A_WORD

    w = world_at()
    stand = reply("", call("stand_by", until="a glass"))

    def captains_part(last, turns):
        if last.get("question"):
            return reply("", call("answer", text="Shorten sail, Mr Pearce."))
        return stand

    cap = seated(w, [captains_part], loop=True)
    stage = {"n": 0}
    orders = [
        "tell the captain the wind is backing",
        "ask the captain whether to shorten sail",
        "tell the master mind the glass",
    ]

    def officers_part(last, turns):
        # one order a sample, a stand-by between: the word, the question, the word kept
        stage["n"] += 1
        if stage["n"] % 2 == 1 and stage["n"] // 2 < len(orders):
            return reply("", call("submit_order", text=orders[stage["n"] // 2]))
        return stand

    off = seated(w, [officers_part], make=officer, loop=True)
    who = off.who_words  # 'the officer of the watch (Mr ...)'
    w.run(1200)
    told = [s for s in samples(cap) if s.get("word")]
    assert told and told[0]["reason"] == f"a word from {who}"
    assert told[0]["word"].endswith("to you: the wind is backing")
    resumed = [e.text for e in w.log if e.kind == "agent.resumed"]
    assert f"[captain] A word from {who}; the captain is sampled again." in resumed
    asked = [s for s in samples(cap) if s.get("question")]
    assert asked and asked[0]["reason"] == f"a question from {who}"
    assert asked[0]["question"].endswith("to shorten sail")
    answered = [s for s in samples(off) if s.get("word")]
    assert answered and answered[0]["reason"] == f"an answer from {cap.who_words}"
    assert answered[0]["word"].endswith("Shorten sail, Mr Pearce.")
    # the prompt's own word is the captain's, as it always was
    w.submit("tell the officer of the watch keep her so")
    w.run(2)
    s = samples(off)[-1]
    assert s["reason"] == A_WORD == "a word from the captain" and s["word"] == "keep her so"
    # the officer's word to the master, whom nobody held, waits in the master's journal and
    # is passed to whoever takes the station, the reason naming its keeping
    kept = [e for e in w.log if e.kind == "agent.told" and e.data.get("kept")]
    assert kept and kept[0].data["speaker"] == "officer of the watch"
    m = seated(w, [stand], make=master)
    s = samples(m)[0]
    assert s["reason"] == "the start"
    assert s["word"].endswith("kept for whoever takes the station: mind the glass")
    assert m.agent.word is None and m.agent.word_reason == ""


def test_a_station_is_never_woken_by_its_own_word():
    """The owner's observation of 2026-11-05: seven of the brig's captain's sixty wakes
    followed his own last word. A station's word to itself (`tell`, `say to`) is refused in
    words; its word to a station nobody holds is kept there and wakes the speaker not at
    all; a question put to a person nobody holds while a director sits comes back, when no
    answer came in a glass, as "no answer from <him>" and never as the speaker's own word."""
    from freesail.agents import harness as harness_mod
    from tests.test_director import seat_director

    w = world_at()
    seat_director(w, [reply("", call("stand_by", until="a glass"))])
    stand = reply("", call("stand_by", until="a glass"))
    off = seated(
        w,
        [
            reply(
                "",
                call("submit_order", text="tell the officer of the watch keep her so"),
                call("submit_order", text="say to the officer of the watch all well"),
                call("submit_order", text="tell the master mind the glass"),
                call("submit_order", text="ask the gunner whether the guns are secured"),
            ),
            stand,
            stand,
            stand,
        ],
        make=officer,
    )
    w.run(1)
    refused = [r for r in results(off, "submit_order") if "tells itself nothing" in str(r)]
    assert len(refused) == 2, results(off, "submit_order")
    assert off.agent.word is None and off.agent.word_reason == ""
    kept = [e for e in w.log if e.kind == "agent.told" and e.data.get("kept")]
    assert kept and kept[0].data["station"] == "master"
    # nothing of his own wakes him: his stand-by holds through the glass but for the answer
    # that did not come, which names the gunner
    asked = [e for e in w.log if e.kind == "agent.asked"]
    assert asked and "gunner" in asked[-1].text
    w.run(harness_mod.PERSON_ANSWER_BOUND_S + 5)
    reasons = [s["reason"] for s in samples(off)[1:]]
    assert not any("officer of the watch" in r for r in reasons), reasons
    woke = [s for s in samples(off) if s.get("word") and "No answer came from" in s["word"]]
    assert woke and woke[0]["reason"].startswith("no answer from ")
    assert "officer" not in woke[0]["reason"]


def test_a_say_is_heard_on_every_hull_within_hearing_and_written_as_heard():
    """Truth 7-389 (the lead's word of 2026-11-05): a station's `say` reaches every hull's
    stations within hearing: ashore at the same place of the same port, whichever ship
    brought each; the line is written as heard into each hearing hull's log with that
    hull's hearers named, and nothing reaches a quarterdeck three miles off."""
    from freesail.agents.agent import master
    from tests.test_people import _world_with_a_crewed_brig

    w, b = _world_with_a_crewed_brig()
    crew = b.crew
    # the player's captain and the brig's master both ashore at Falmouth, at the counting
    # house, their whereabouts written as the boat would write them (package 84, step 2)
    for person in (w.people.captain, crew.people.find("the master")):
        person.aboard, person.where, person.port, person.ashore_at = (
            False,
            "shore",
            "falmouth",
            "counting_house",
        )
    stand = reply("", call("stand_by", until="a glass"))
    cap = seated(w, [stand])
    greet = reply("", call("submit_order", text="say good day to you all"))
    seated(crew, [greet, stand], make=master)
    w.run(2)
    said = [e for e in crew.log if e.kind == "agent.spoke"]
    assert said and "ashore at Falmouth, at the counting house: good day to you all" in said[0].text
    assert said[0].data["heard_by"] == []  # nobody of the brig's was there
    heard = [e for e in w.log if e.kind == "agent.spoke" and "good day to you all" in e.text]
    assert heard and heard[0].data["heard_by"] == ["captain"]
    assert heard[0].data["said_from"] == b.id and heard[0].text == said[0].text
    w.run(1800)  # overheard, not addressed: the words ride his next sample (41's rule)
    s = samples(cap)[-1]
    assert s.get("heard") and s["heard"][0].endswith("at the counting house: good day to you all")
    # aboard, three miles apart, a word on one quarterdeck reaches no station of the other
    for person in (w.people.captain, crew.people.find("the master")):
        person.aboard, person.where, person.port, person.ashore_at = True, "quarterdeck", "", ""
    n = len(w.log)
    e = crew.submit("say the glass is falling", actor="the master")
    assert e.kind == "agent.spoke" and e.data["heard_by"] == []
    assert not [e for e in list(w.log)[n:] if e.kind == "agent.spoke"]
    assert [e for e in crew.log if e.kind == "agent.spoke" and "glass is falling" in e.text]


# ---------------------------------------------------------------------------
# Step 3: report, the messenger and the call; the sleeper's wake; the command devolved
# (the design's §7; decision 63; truths 7-370 whole, 7-371, 7-372, 7-387 whole)
# ---------------------------------------------------------------------------


def _officer_seated(w, script=None, loop=True) -> Harness:
    stand = reply("", call("stand_by", until="a glass"))
    fake = Fake(script or [stand], loop=True) if loop else Fake(script, when_done=stand)
    h = Harness(w, officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=w), fake)
    h.model_name, h.door = "the fake officer", "runner"
    h.start()
    return h


def test_the_rules_officer_reports_to_the_captain_below_a_minute_later_and_not_on_deck():
    """Truth 7-370 whole: the rules' officer of the watch sends down to the captain in the
    cabin each reportable line of the deck a minute after it (the messenger's minute), the
    report a notable line for him (`report.made`, reach `person`) in his sample there, the
    deck's line itself not; a captain on deck gets no report; a model at the officer's
    station makes the rules' officer silent (the duty is the model's, the brief says it)."""
    from freesail.world import reports

    w, h = the_captain_in_the_cabin()
    w.run(7200)
    made = [e for e in w.log if e.kind == reports.REPORT_MADE]
    assert made, [e.kind for e in w.log if e.kind.startswith("report.")]
    pearce = w.stations.holder("officer of the watch")
    for e in made:
        assert e.text.startswith(f"{pearce.name} sent down to the captain, in the cabin: "), e.text
        assert e.data["to"] == w.people.captain.name and e.data["of"] in reports.REPORTABLE
        # the line it reports fell a minute before, of the kind the report names
        sources = [
            x for x in w.log if x.tick == e.tick - reports.MESSENGER_S and x.kind == e.data["of"]
        ]
        assert sources, (e.text, e.data)
    below = [s for s in samples(h) if "in the cabin" in str(s.get("you"))]
    kinds = {ln["kind"] for s in below for ln in s["log"]}
    assert reports.REPORT_MADE in kinds
    assert not kinds & {"lookout.sighting", "lookout.made_out", "agent.hail"}
    # on deck no report is made: he sees it
    w2 = world_at()
    w2.run(7200)
    assert not [e for e in w2.log if e.kind.startswith("report.")]
    # a model at the officer's station: the rules' officer reports nothing
    w3 = world_at()
    _officer_seated(w3)
    w3.submit("you have the deck")
    w3.submit("go below")
    w3.run(7200)
    assert not [e for e in w3.log if e.kind == reports.REPORT_MADE]


def test_the_captain_is_called_for_a_danger_once_for_a_thing_and_for_everything_by_night():
    """The design's §7: a danger line (her sails lifting, taken aback) with the captain
    below makes a call, not a report, said once for a thing until he comes on deck; by
    night every reportable line is a call; the words are the officer's."""
    from freesail.world import reports

    w, h = the_captain_in_the_cabin()
    w.run(7200)
    called = [e for e in w.log if e.kind == reports.REPORT_CALLED]
    assert called, [e.kind for e in w.log if e.kind.startswith("report.")]
    pearce = w.stations.holder("officer of the watch")
    for e in called:
        assert e.text.startswith(f"{pearce.name} sends for the captain: "), e.text
        assert e.data["to"] == w.people.captain.name
        assert e.text.count("lifting") <= 1 and e.text.count("aback") <= 1, e.text
    # once for a thing: no second call of one kind within the hour while he is below
    kinds = [e.data["of"] for e in called]
    for kind in set(kinds):
        ticks = [e.tick for e in called if e.data["of"] == kind]
        assert all(b - a >= 3600 for a, b in zip(ticks, ticks[1:], strict=False)), (kind, ticks)
    # the call ends his stand-by: he is sent for
    woke = [e.text for e in w.log if e.kind == "agent.resumed" and "sent for:" in e.text.lower()]
    assert woke, [e.text for e in w.log if e.kind == "agent.resumed"][:3]
    # the words by day and by night, judged on the lines themselves
    ev = Event(
        tick=1,
        ship_time=datetime(1805, 6, 10, 10, 0),
        severity=Severity.NOTABLE,
        kind="lookout.sighting",
        text="Sail ho! A sail two points on the larboard bow.",
        actor="sim",
        data={"seen_as": "sail", "relative": "two points on the larboard bow"},
    )

    class Day:
        daylight = "day"

    class Night:
        daylight = "night"

    what = reports._what(ev)
    assert what == "a sail sighted, two points on the larboard bow"
    assert reports._why_called(Day(), ev, what) is None
    assert reports._why_called(Night(), ev, what) == what
    aback = Event(
        tick=1,
        ship_time=datetime(1805, 6, 10, 10, 0),
        severity=Severity.NOTABLE,
        kind="ship.aback",
        text="Taken aback: the sails pressed against the masts.",
        actor="sim",
        data={},
    )
    assert (
        reports._why_called(Day(), aback, None)
        == "taken aback: the sails pressed against the masts"
    )
    hail = Event(
        tick=1,
        ship_time=datetime(1805, 6, 10, 10, 0),
        severity=Severity.NOTABLE,
        kind="agent.hail",
        text="[lookout] Sail ho!",
        actor="the lookout",
        data={},
    )
    assert reports._why_called(Night(), hail, None) is None  # the sighting's own report


def test_call_the_captain_is_the_officers_order_and_the_call_wakes_the_sleeper_as_all_hands_do():
    """Truth 7-372 and the design's §7: `call the captain [: <why>]` is the officer of the
    watch's order (his domain names it; the master's does not), refused from the captain
    himself and when the captain is on deck; its line (`report.called`) wakes a captain
    asleep below, whom the bell and a notable line of the deck did not; an officer asleep
    below is woken by all hands and not by the bell."""
    from tests.test_people import _behind

    w = world_at()
    _officer_seated(w)
    w.submit("you have the deck")
    # the captain's station: a fake that turns in below (tired by hand)
    sleep = reply("", call("stand_by", until="asleep below until called"))
    ch = seated(w, [reply("", call("stand_by", until="a glass")), sleep])
    cap = w.people.captain
    w.run(60)
    assert cap.needs.by_hand  # a station's person: his needs his own, not the company's
    _behind(w, cap.needs, awake=30)
    w.run(1800)  # the glass, or the first wake before it: his second reply turns him in
    assert cap.needs.asleep == "below" and cap.where == "cabin", (cap.needs.asleep, cap.where)
    assert ch.agent.standing_by
    e = w.submit("call the captain")
    assert e.kind == "order.rejected" and "there is no sending for yourself" in e.text
    # a notable line of the deck and the bell do not wake him
    before = len(w.log)
    w.submit("set the royals", actor="the officer of the watch")
    w.run(1800)
    assert any(x.kind == "clock.bell" for x in list(w.log)[before:])
    assert ch.agent.standing_by and cap.needs.asleep == "below"
    # the master may not call him; the officer may, and the call wakes him
    master_result = tools.call(w, "master", "submit_order", {"text": "call the captain"})
    assert "may not" in str(master_result) or "has no authority" in str(master_result), (
        master_result
    )
    result = tools.call(
        w, "officer of the watch", "submit_order", {"text": "call the captain: a sail to windward"}
    )
    assert "sends for the captain: a sail to windward" in str(result), result
    called = [x for x in w.log if x.kind == "report.called"]
    assert (
        called
        and called[-1].data["why"] == "a sail to windward"
        and called[-1].actor == "the officer of the watch"
    )
    w.run(2)
    assert not cap.needs.asleep and cap.where == "quarterdeck"  # back where he turned in from
    woke = [x.text for x in w.log if x.kind == "agent.resumed"][-1]
    assert "sent for:" in woke.lower() and "a sail to windward" in woke, woke
    # on deck again he sees it: the call is refused in words
    w.submit("come on deck")
    result = tools.call(w, "officer of the watch", "submit_order", {"text": "call the captain"})
    assert "he sees it" in str(result), result
    # an officer asleep below: the bell does not wake him, all hands does
    w2 = world_at()
    oh2 = _officer_seated(w2, [reply("", call("stand_by", until="a glass")), sleep], loop=False)
    w2.run(60)
    pearce = w2.stations.holder("officer of the watch")
    assert pearce.needs.by_hand
    _behind(w2, pearce.needs, awake=30)
    w2.run(1800)  # the glass: his second reply turns him in
    assert pearce.needs.asleep == "below" and oh2.agent.standing_by, pearce.needs.asleep
    before = len(w2.log)
    w2.run(1800)
    assert any(x.kind == "clock.bell" for x in list(w2.log)[before:]) and oh2.agent.standing_by
    e = w2.submit("call all hands")
    assert e.kind != "order.rejected", e.text
    w2.run(2)
    assert not pearce.needs.asleep
    woke2 = [x.text for x in w2.log if x.kind == "agent.resumed"][-1]
    assert "woken:" in woke2.lower() and "hands" in woke2.lower(), woke2


def test_the_tripwires_call_is_a_line_in_the_log():
    """Truth 7-387 whole: the tripwire judged for a captain below fires as the officer's call
    and the log says so (`report.called`, 'Mr Pearce sends down to the captain: speed under
    20 knots'), before the station's wake line; on deck no such line."""
    w = world_at()
    script = [
        reply("", call("submit_order", text="go below")),
        reply("", call("stand_by", until="speed under 20 knots")),
        reply("", call("stand_by", until="a glass")),
    ]
    seated(w, script)
    w.run(130)
    called = [e for e in w.log if e.kind == "report.called"]
    assert called, [e.kind for e in w.log][-10:]
    pearce = w.stations.holder("officer of the watch")
    head = f"{pearce.name} sends down to the captain: speed under 20 knots"
    assert called[0].text.startswith(head), called[0].text
    assert called[0].data["why"].startswith("speed under 20 knots")
    resumed = [e for e in w.log if e.kind == "agent.resumed"]
    assert resumed and resumed[0].tick >= called[0].tick
    assert list(w.log).index(called[0]) < list(w.log).index(resumed[0])
    w2 = world_at()
    seated(w2, [reply("", call("stand_by", until="speed under 20 knots"))])
    w2.run(130)
    assert not [e for e in w2.log if e.kind == "report.called"]


def test_the_command_devolves_on_the_held_officer_while_the_captain_is_away():
    """Decision 63: `you have the deck` with the captain aboard is the watch; the captain in
    the boat for the shore, the command devolves on the officer who holds the station (his
    deck, a notice, the log's line), who holds the captain's authority whole (a manoeuvre
    is his to order, logged as given in command); landed and brought back, the captain has
    the command again when he gives an order, and the officer's authority is his own."""
    from tests.test_ports import CARRICK_ROAD, at_anchor_in

    w = at_anchor_in(CARRICK_ROAD)
    oh = _officer_seated(w)
    w.run(60)
    assert tools.judge(w, "officer of the watch", "tack ship")[1]  # his own authority refuses
    e = w.submit("go ashore")
    assert e.kind != "order.rejected", e.text
    w.run(2)
    dev = [x for x in w.log if x.kind == "ship.command_devolved"]
    assert (
        len(dev) == 1
        and dev[0].text == "The command devolves on Mr Pearce, the captain in the boat."
    )
    assert dev[0].data["station"] == "officer of the watch"
    assert oh.agent.deck
    w.run(600)
    notice = [
        n for s in samples(oh) for n in s.get("notices", []) if "command has devolved on you" in n
    ]
    assert notice, [s.get("notices") for s in samples(oh)][-2:]
    assert tools.judge(w, "officer of the watch", "tack ship") == (
        "tack ship",
        "",
        "the command devolved",
    )
    result = tools.call(w, "officer of the watch", "submit_order", {"text": "call all hands"})
    assert "may not" not in str(result), result
    mine = [x for x in w.log if x.actor == "the officer of the watch"]
    his = [x.text for x in mine if "in command" in x.text]
    assert his and his[-1].startswith("By the officer of the watch, in command:"), his
    # the player's own typed order from the shore does not take it back: he is away
    cap = w.people.captain
    for _ in range(60):
        w.run(60)
        if cap.where == "shore":
            break
    assert not cap.aboard and cap.where == "shore"
    assert [x for x in w.log if x.kind == "ship.command_resumed"] == []
    for _ in range(90):  # the boat back at the ship before she fetches him
        if not w.dealings.boat.away:
            break
        w.run(60)
    e = w.submit("come aboard")
    assert e.kind != "order.rejected", e.text
    for _ in range(90):
        w.run(60)
        if cap.aboard:
            break
    assert cap.aboard
    w.run(2)
    resumed = [x for x in w.log if x.kind == "ship.command_resumed"]
    assert len(resumed) == 1 and resumed[0].text.startswith("The captain has the command again")
    assert tools.judge(w, "officer of the watch", "tack ship")[2] != "the command devolved"
    assert len([x for x in w.log if x.kind == "ship.command_devolved"]) == 1


def test_a_told_order_is_the_captains_word_and_never_refused():
    """Decision 63: an order the captain tells a station to carry out is his word for that
    thing: the officer told to tack ship tacks her, the log saying it was given at the
    captain's word, without the deck too; a manoeuvre he was not told stays refused."""
    w = world_at()
    oh = _officer_seated(w)
    w.run(60)
    assert tools.judge(w, "officer of the watch", "tack ship")[1]
    e = w.submit("tell the officer to tack ship")
    assert e.kind == "agent.told"
    assert oh.agent.told[-1] == "tack ship"  # the grammar drops the 'to'
    assert tools.judge(w, "officer of the watch", "tack ship") == (
        "tack ship",
        "",
        "the captain's word, told",
    )
    assert tools.judge(w, "officer of the watch", "wear ship")[1]
    assert tools.told_order(w, "officer of the watch", "tack ship")
    result = tools.call(w, "officer of the watch", "submit_order", {"text": "tack ship"})
    assert "has not the deck" not in str(result), result
    mine = [x for x in w.log if x.actor == "the officer of the watch" and "tack" in x.text.lower()]
    assert mine and "By the officer of the watch, at the captain's word:" in mine[-1].text, [
        x.text for x in mine
    ]
    result = tools.call(w, "officer of the watch", "submit_order", {"text": "wear ship"})
    assert "may not wear ship" in str(result) or "has not the deck" in str(result), result
    w.submit("you have the deck")
    result = tools.call(w, "officer of the watch", "submit_order", {"text": "wear ship"})
    assert "may not wear ship" in str(result), result


def test_the_boats_report_at_the_quay_reaches_the_captain_ashore_and_nothing_else_of_the_ship():
    """Truth 7-371: a captain ashore at the port has nothing of the ship in his sample (the
    readings answer that nothing of the ship is to be read ashore, the deck's lines none)
    but the boat's report when her manned boat comes to the quay (`report.boat`, reach
    `port`): her state, whose the deck is, all well."""
    from freesail.world import boats as B
    from tests.test_ports import CARRICK_ROAD, at_anchor_in

    w = at_anchor_in(CARRICK_ROAD)
    frigate = w.players
    cap = seated(w, [reply("", call("readings")), reply("", call("stand_by", until="a glass"))])
    w.run(60)
    person = w.people.captain
    person.aboard, person.where, person.port, person.ashore_at = False, "shore", "falmouth", "quay"
    w.run(1801)
    ashore = [s for s in samples(cap) if "ashore" in str(s.get("you"))]
    assert ashore, [s.get("you") for s in samples(cap)]
    assert not {ln["kind"] for s in ashore for ln in s["log"]} & {
        "sail.set",
        "clock.bell",
        "helm.order",
    }
    pearce = w.stations.holder("officer of the watch")
    e = w.submit("go to the launch", actor="the officer of the watch")
    assert e.kind == "person.aboard", e.text
    boat = w.hulls[f"{frigate.id}:launch"]
    assert B.is_boat(boat) and pearce.hull == boat.id
    e = boat.submit("pull for the quay", actor="the officer of the watch")
    assert e.kind != "order.rejected", e.text
    for _ in range(60):
        w.run(60)
        if any(x.kind == "boat.at_quay" for x in boat.log):
            break
    assert any(x.kind == "boat.at_quay" for x in boat.log)
    w.run(2)
    report = [x for x in frigate.log if x.kind == "report.boat"]
    assert len(report) == 1, [x.kind for x in list(frigate.log)[-5:]]
    assert report[0].text.startswith(
        "The boat came in to the quay at Falmouth; the coxswain reports: the ship at anchor"
    )
    assert report[0].data["port"] == "falmouth" and person.name in report[0].data["to"]
    w.run(1801)
    kinds = [ln["kind"] for s in samples(cap) for ln in s["log"]]
    assert "report.boat" in kinds


def test_the_officers_brief_says_the_duty_and_the_kinds_are_placed():
    from freesail.agents.agent import OFFICER_BRIEF

    assert (
        "Report to the captain what the Regulations gave the lieutenant to report" in OFFICER_BRIEF
    )
    assert "'call the captain: <why>'" in OFFICER_BRIEF
    assert "the command devolves on the senior officer" in OFFICER_BRIEF
    assert K.REACH["report.made"] == "person" and K.REACH["report.called"] == "wakes"
    assert K.REACH["report.boat"] == "port" and K.REACH["ship.command_devolved"] == "aboard"
    assert (
        R.EVENTS["a report"].kind == "report.made"
        and R.EVENTS["the captain called"].kind == "report.called"
    )


# ---------------------------------------------------------------------------
# Step 4: the player at the prompt reads by his place (decision 59), one person (decision 62)
# ---------------------------------------------------------------------------


def _console(w):
    import io

    from freesail.ui.console import Console

    out = io.StringIO()
    return Console(w, out=out), out


def test_the_console_shows_the_captain_what_reaches_him_where_he_is():
    """Truth 7-382, the console: the play log is the player's person's, what reaches him
    where he is (decision 59; the design's §11). The captain in the cabin is shown no deck
    line (the lookout's sightings, the sail work) and is shown the officer's report; `log N`
    reads back by the same rule; on deck again the deck's lines are his."""
    from freesail.world import reports

    w = world_at()
    con, out = _console(w)
    assert con.handle_line("set the royals")
    assert "set the royals" in out.getvalue()
    assert con.handle_line("go below")
    assert "went below" in out.getvalue()
    mark = out.tell()
    assert con.handle_line("tick 7200")
    below = out.getvalue()[mark:]
    made = [e for e in w.log if e.kind == reports.REPORT_MADE]
    assert made, [e.kind for e in w.log if e.kind.startswith("report.")]
    assert "sent down to the captain, in the cabin" in below
    deck = [e for e in w.log if e.kind in ("lookout.sighting", "lookout.made_out", "agent.hail")]
    assert deck
    for e in deck:
        assert e.text not in below, e.text
    mark = out.tell()
    assert con.handle_line("log 400")
    read_back = out.getvalue()[mark:]
    assert "sent down to the captain" in read_back
    for e in deck:
        assert e.text not in read_back, e.text
    assert con.handle_line("come on deck")
    mark = out.tell()
    con.handle_line("heave the log")  # the deck's business, his again on deck
    assert "Order: heave the log." in out.getvalue()[mark:]
    assert K.players_senses(w).spot == ("aboard", w.players.id, "quarterdeck")


def test_knowledge_all_the_directors_seat_and_follow_of_another_hull_are_the_owners_eye():
    """Truth 7-382, the owner's eye: under `knowledge: all` the captain in the cabin is shown
    everything; in an observed world the director's seat and `follow` of a hull he holds no
    person in show everything of her (the design's §11)."""
    from tests.test_observer import observed_world

    w = world_at(knowledge="all")
    con, out = _console(w)
    con.handle_line("go below")
    mark, since = out.tell(), w.clock.tick
    con.handle_line("tick 3600")
    shown = out.getvalue()[mark:]
    deck = [
        e
        for e in w.log
        if e.tick > since and e.kind in ("lookout.sighting", "sail.set", "agent.hail")
    ]
    assert deck and all(e.text in shown for e in deck)
    assert K.players_senses(w).everything
    w2, _ = observed_world()
    assert K.players_person(w2) is None and K.players_senses(w2).everything
    con2, out2 = _console(w2)
    assert con2.handle_line('follow "Medusa"')
    assert K.players_senses(w2).everything
    mark = out2.tell()
    con2.handle_line("set the royals")
    assert "set the royals" in out2.getvalue()[mark:]


def test_the_browsers_log_and_snapshot_are_the_players_persons():
    """Truth 7-382, the browser: the pages' play log and the log's reach-back are filtered
    as the console's; the snapshot's `knowledge` says where the player is, the rows not to
    be had there with where each is, and whether the deck's are his; `follow` and `look at`
    typed at the order line are the driver's, a refusal sent to the pages alone."""
    from freesail.ui.server import Driver
    from freesail.world import reports

    w = world_at()
    d = Driver(w)
    k = d.snapshot()["knowledge"]
    assert k["place"] == "on the quarterdeck" and not k["everything"] and k["deck"]
    assert k["hidden"] == [] and k["words"] == ""
    d.submit("go below")
    d.tick(7200)
    k = d.snapshot()["knowledge"]
    assert k["place"] == "in the cabin" and not k["deck"]
    hidden = {h["id"]: h["where"] for h in k["hidden"]}
    assert hidden["speed"] == "the log is hove on deck" and "in_sight" in hidden
    assert "heading" not in hidden and "glass" not in hidden
    assert k["words"].startswith("Not to be had in the cabin: ")
    shown = d.shown_log(2000)
    kinds = {x.get("kind") for x in shown}
    assert reports.REPORT_MADE in kinds
    assert not kinds & {"lookout.sighting", "lookout.made_out", "agent.hail"}
    sent: list[dict] = []
    d.add_listener(sent.append)
    e = d.submit('follow "the ship"')
    assert e.kind == "driver.follow" and sent[0]["event"]["kind"] == "driver.follow"
    e = d.submit('follow "Nobody Afloat"')
    assert e.kind == "driver.refused" and "Nobody Afloat" in e.text
    assert not [x for x in w.log if x.kind == "driver.refused"]


def test_the_player_goes_aboard_another_ship_in_his_own_boat_and_the_prompt_follows_him():
    """Decision 62: the player is one person and the prompt follows his body. From his own
    manned boat `come alongside the X` pulls for her and, alongside, puts him aboard her as
    a visitor, the drivers following him (a `hull.followed` line, no driver's input); his
    log there is hers by his place; `go to the boat` from her deck puts him back in his own
    boat lying alongside, and `come alongside` brings him home, the drivers with him."""
    from tests.test_between_hulls import _brig_alongside, _run_until

    w, b, hull = _brig_alongside()
    captain = w.people.captain
    assert K.players_person(w) is captain
    e = w.submit("go to the boat")
    assert e.kind == "person.aboard", e.text
    boat = w.hulls[w.followed]
    assert boat is not w.players and captain.hull == boat.id
    e = w.submit("come alongside the X")
    assert "Pulling for the X" in e.text and "goes aboard her" in e.text, e.text
    _run_until(w, lambda: captain.hull == hull.id, 1.0)  # raises when not reached
    assert w.followed == hull.id  # the prompt followed his body
    followed = [x for x in hull.log if x.kind == "hull.followed"]
    assert followed and captain.name in followed[-1].text
    assert not [x for x in w.players.log if x.kind == "driver.follow"]
    assert "aboard the X, on the quarterdeck, a visitor, of the" in w.submit("where am i").text
    # the prompt is his there (decision 62): a passenger's reach, as a seated visitor's
    e = w.submit("steer west")
    assert e.kind == "order.rejected" and "as a visitor" in e.text, e.text
    assert "gives no order of her deck" in e.text and "'go to the boat' takes you off" in e.text
    assert hull.people.captain is not K.players_visitor(hull) is captain
    senses = K.players_senses(w)
    assert senses.spot == ("aboard", hull.id, "quarterdeck") and not senses.everything
    alongside = [x for x in boat.log if x.kind == "boat.alongside"]
    assert alongside and "went aboard her" in alongside[-1].text
    # back into his own boat, made fast alongside her, and home
    w.run(600)  # she keeps her station alongside while the X lies to
    e = w.submit("go to the boat")
    assert e.kind == "person.aboard" and captain.hull == boat.id, e.text
    assert w.followed == boat.id
    assert "made fast alongside the X" in w.submit("where am i").text
    e = w.submit("come alongside")
    assert "hoisted in" in e.text
    # the frigate hove to still makes near three knots and the launch three and a half:
    # two hours and a half of pulling, the men tiring (package 82's figures)
    _run_until(w, lambda: captain.hull == w.players.id, 3.0)
    assert w.followed == w.players.id and not w.players.dealings.boat.away


def test_a_drivers_word_never_shadows_an_order_of_the_game():
    """Decision 62 (the owner's clarification): a driver's word never shadows an order of
    the game, and an order of the game is never read as the driver's. `hold` alone holds
    the clock and `hold water` is the boat's order; every verb and synonym of the vocabulary
    whose first word is a driver's reaches the ship from the console."""
    from freesail.orders.vocabulary import load_vocabulary
    from freesail.ui.console import HELP

    heads = {"hold", "go", "speed", "time", "tick", "state", "follow", "look", "log", "save"}
    for word in heads:
        assert re.search(rf"^\s+{word}\b", HELP, re.M), word  # each a driver's command
    vocab = load_vocabulary()
    phrases = sorted(
        p
        for p, verb in vocab.phrase_to_verb.items()
        if p.split()[0] in heads and vocab.verbs[verb].object != "driver"
    )
    assert {"hold water", "hold your fire", "go below", "go ashore", "go aloft"} <= set(phrases)
    w = world_at()
    con, out = _console(w)
    con.handle_line("go")
    con.handle_line("time 30")
    for phrase in phrases:
        before = (con.running, con.compression, w.clock.tick, len(w.log), len(w.journal))
        mark = out.tell()
        con.handle_line(phrase)
        after = (con.running, con.compression, w.clock.tick, len(w.log), len(w.journal))
        assert after[:3] == before[:3], phrase  # nothing of the driver's moved
        assert after[3] > before[3] or after[4] > before[4], phrase  # the ship answered
        assert "Clock held" not in out.getvalue()[mark:], phrase
    con.handle_line("hold")
    assert not con.running and "Clock held." in out.getvalue()


# ---------------------------------------------------------------------------
# Step 5: books, papers and pictures in their places (the design's §8; truth 7-374)
# ---------------------------------------------------------------------------


def test_the_ships_own_are_read_where_they_are_kept_and_the_reference_anywhere():
    """Truth 7-374: the library refuses the manifest from the quarterdeck with "in the hold"
    and the walk, serves it after `go to the hold`, and serves the primer anywhere; the log
    book, the chart, the book of standing orders and a book drafted are read where they are
    kept and refused elsewhere with where they are; the ship is seen from the deck and not
    from the cabin; `find` across the library says what it left out; the director and
    `knowledge: all` read everything from anywhere."""
    w = world_at()
    lib = lambda *a, **k: str(tools.library(w, "captain", *a, **k))  # noqa: E731
    assert lib("papers", "manifest") == (
        "The manifest is kept in the hold, with the purser; go to the hold to read it (or ask "
        "the purser)."
    )
    assert lib("papers", "the news of the war").startswith(
        "The news of the war is kept in the cabin, with the captain; go to the cabin to read it"
    )
    assert "To be had on the quarterdeck: the boatswain's store book" in lib("papers")
    e = w.submit(
        'draft a book "night orders": standing order "lead": every glass then heave the lead'
    )
    assert e.kind == "book.drafted"
    assert "heave the lead" in lib("books", "night orders")
    assert w.submit("go to the hold").kind == "person.moved"
    # in the hold: the manifest and the purser's books his, the primer his, the rest not
    page = lib("papers", "manifest")
    assert page.startswith("The manifest: the hold's capacity and the cargo in it by tons")
    assert page.splitlines()[1:] == w.papers.page("manifest").lines
    assert "The purser's books:" in lib("papers", "all")
    assert "Not in the hold: the sailmaker's account (in the sail room" in lib("papers", "all")
    assert lib("primer 2").startswith("primer 2: The wind and the points of sail.")
    assert "fore mast" in lib("the ship") and "submit_order:" in lib("tools")
    assert lib("papers", "booms") == (
        "The booms' list is kept on the deck, with the boatswain; come on deck to read it (or "
        "ask the boatswain)."
    )
    assert lib("standing orders") == (
        "The book of standing orders is on the quarterdeck and in the cabin; you are in the "
        "hold: come on deck to read it."
    )
    assert lib("books", "night orders") == (
        "The book 'night orders' is on the quarterdeck and in the cabin, with the book of "
        "standing orders; you are in the hold: come on deck to read it."
    )
    assert lib("books") == (
        "The books drafted are on the quarterdeck and in the cabin, with the book of standing "
        "orders; you are in the hold: come on deck to read it."
    )
    got = tools.read_log(w, "captain", since_tick=0)
    assert got == {
        "error": "The log book is in the cabin and the gunroom, the log board on the "
        "quarterdeck; you are in the hold: come on deck to read it."
    }
    assert tools.chart(w, "captain") == (
        "The chart is in the cabin and the gunroom, and at the binnacle on deck; you are in the "
        "hold: come on deck to read it."
    )
    assert tools.ship_view(w, "captain") == (
        "She is seen from the deck or the boat; you are in the hold: come on deck to see her."
    )
    found = lib(find="heave the lead")
    assert "Not searched, being elsewhere:" in found
    assert "the book of standing orders (on the quarterdeck and in the cabin)" in found
    assert "the books drafted (on the quarterdeck and in the cabin)" in found
    assert "the ship's papers elsewhere (the sailmaker's account (in the sail room" in found
    contents = lib("contents")
    assert (
        "the ship's own are read where they are kept. In the hold, the papers to be had are "
        "the manifest, the purser's books"
    ) in contents
    assert (
        "The book of standing orders and the books drafted are on the quarterdeck and in the cabin."
    ) in contents
    # on deck: the log, the chart, the ship and the books his; the primer still his
    assert w.submit("come on deck").kind == "captain.on_deck"
    assert "lines" in tools.read_log(w, "captain", since_tick=0)
    assert isinstance(tools.chart(w, "captain"), dict)  # no page open: the words and the rows
    assert isinstance(tools.ship_view(w, "captain"), dict)
    assert "heave the lead" in lib("books", "night orders")
    assert lib("standing orders").startswith("There are no standing orders in the book.")
    assert "The book of standing orders and the books drafted are here." in lib("contents")
    # in the cabin: the chart and the log his, the ship not seen
    assert w.submit("go below").kind == "captain.below"
    assert isinstance(tools.chart(w, "captain"), dict)
    assert "lines" in tools.read_log(w, "captain", since_tick=0)
    assert tools.ship_view(w, "captain") == (
        "She is seen from the deck or the boat; you are in the cabin: come on deck to see her."
    )
    assert lib("papers", "the news of the war").startswith("The news of the war: the nations'")
    # a seated model reads the same through its harness
    script = [
        reply("", call("submit_order", text="go to the hold")),
        reply("", call("library", topic="papers", section="manifest")),
        reply("", call("library", topic="papers", section="the price list")),
        reply("", call("read_log")),
        reply("", call("stand_by", until="a glass")),
    ]
    h = seated(world_at(), script)
    h.world.run(60)
    pages = results(h, "library")  # each a book, stubbed with its handle and number
    assert pages[0].startswith("the ship's papers, the manifest, opened")
    assert "The manifest: the hold's capacity" in pages[0]
    assert "The price list is kept in the cabin, with the purser; go to the cabin" in pages[1]
    assert "error" in results(h, "read_log")[0]
    # the director everything, from anywhere; `knowledge: all` the same for everyone
    assert str(tools.library(w, "director", "papers", "manifest")).startswith("The manifest:")
    assert "lines" in tools.read_log(w, "director", since_tick=0)
    every = world_at(knowledge="all")
    assert str(tools.library(every, "captain", "papers", "manifest")).startswith("The manifest:")
    assert "To be had" not in str(tools.library(every, "captain", "papers"))
    # ashore and asleep, the words (the design's §8; the port's tests have the walk)
    ashore = K.Senses(frozenset({K.ASHORE}), ("ashore", "falmouth", "quay"), "")
    assert K.thing_elsewhere("log", ashore) == "The ship's log is aboard her."
    assert K.thing_elsewhere("chart", ashore) == "The chart is aboard her."
    assert K.thing_elsewhere("standing orders", ashore) == (
        "The book of standing orders is aboard her."
    )
    assert K.thing_elsewhere("ship_view", ashore) == (
        "She is seen from the deck or the boat; you are ashore."
    )
    page = w.papers.page("manifest")
    assert K.paper_elsewhere(w, page, ashore) == "The manifest is aboard her, in the hold."
    asleep = K.Senses(frozenset({K.ASLEEP}), ("aboard", "x", "gunroom"), "gunroom", asleep=True)
    assert K.thing_elsewhere("log", asleep) == K.ASLEEP_WORDS
    assert K.paper_elsewhere(w, page, asleep) == K.ASLEEP_WORDS


def test_the_keeper_carries_his_paper_while_he_is_at_it():
    """The keeper's rule (the design's §8): a paper is in its place until its keeper is
    occupied with it, and then it is with him where he is; the listing says so; freed, it
    lies in its place again. A task of his that does not name the paper leaves it."""
    w = world_at()
    purser = w.people.find("the purser")
    assert purser is not None and purser.where == "gunroom"
    books = w.papers.page("the purser's books")
    assert K.paper_place(w, books) == ("hold", "with the purser")
    assert w.people.occupy(purser, "cabin", w.clock.tick + 600, "the purser's books") is None
    assert K.paper_place(w, books) == ("cabin", "with the purser at his the purser's books")
    assert K.paper_place(w, w.papers.page("manifest")) == ("hold", "with the purser")
    assert w.submit("go below").kind == "captain.below"
    page = str(tools.library(w, "captain", "papers", "purser's books"))
    assert page.startswith("The purser's books: the stores of water and provisions")
    assert str(tools.library(w, "captain", "papers", "manifest")).startswith(
        "The manifest is kept in the hold, with the purser; go to the hold"
    )
    listing = str(tools.library(w, "captain", "papers"))
    here = listing.split("To be had in the cabin: ")[1].split("\n")[0]
    assert here.startswith("the purser's books, the epitome's table of the establishments")
    assert "the manifest (in the hold, with the purser)" in listing
    w.people.free(purser)
    assert K.paper_place(w, books) == ("hold", "with the purser")
    assert str(tools.library(w, "captain", "papers", "purser's books")).startswith(
        "The purser's books are kept in the hold"
    ) or str(tools.library(w, "captain", "papers", "purser's books")).startswith(
        "The purser's books is kept in the hold"
    )
    # a task that does not name the paper: the slops are not the books
    assert w.people.occupy(purser, "deck", w.clock.tick + 600, "the slops issued") is None
    assert K.paper_place(w, books) == ("hold", "with the purser")
    w.people.free(purser)
