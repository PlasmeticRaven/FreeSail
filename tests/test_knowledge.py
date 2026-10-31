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


def seated(w, script, make=captain, every=600, **kw) -> Harness:
    st = make(SamplingPolicy.in_lockstep(every, "notable", "urgent"), world=w, **kw)
    stand = reply("", call("stand_by", until="a glass"))
    h = Harness(w, st, Fake(script, when_done=stand), save=lambda _w, _why: None)
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
    assert ruled >= 0.8 * free, (ruled, free)
