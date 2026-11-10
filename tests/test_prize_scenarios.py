"""The prize's scenarios, the truth's rows and the replay by both roads (package 74, step 7;
`docs/design/Design-Prizes.md` §8): `prize-home.yaml` and `captive.yaml` load and begin with
the prize in company and the player a prisoner aboard the captor; the director's truth shows
every prize with her crew and her prisoners, the paroles, the far actions and the courts; a
passage with the player taken, the parole exchanged and the captor under way, and a far fight's
passage, each replay by the transcript and by the acts to the same digests (84's acceptance
form)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from freesail import units
from freesail.api.readings import director_readings
from freesail.world import captive as C
from freesail.world import prizes as P
from freesail.world.geo import destination
from freesail.world.scenarios import begin, load_scenario, make_scenario_world
from tests.test_brains import world_at

ROOT = Path(__file__).resolve().parents[1]
PRIZE_HOME = ROOT / "data" / "scenarios" / "prize-home.yaml"
CAPTIVE = ROOT / "data" / "scenarios" / "captive.yaml"


def _begun(path: Path, minutes: int = 4):
    sf = load_scenario(path)
    w = make_scenario_world(sf)
    begin(w, sf)
    for _ in range(minutes):
        w.run(60)
    return sf, w


def test_the_prize_home_scenario_begins_with_the_brig_a_prize_in_company_and_the_truth_shows_her():
    """`prize-home.yaml`: the Amazon bound for Falmouth with the Deux Frères made her prize by
    the scenario's world order two minutes in (a full ship beside her by then): a prize master
    and a prize crew aboard her, her people prisoners, bound for Falmouth in company; the
    player's `the prize` reads her and the director's truth shows her with her crew and her
    prisoners (truth 7-367's rows)."""
    sf, w = _begun(PRIZE_HOME)
    assert sf.scenario.name.startswith("The prize's passage home")
    assert w.ship.name == "Amazon" and w.people.captain.name == "Captain Bowen"
    b = w.vessels.find("Deux Frères")
    assert b is not None and P.is_prize(b)
    rec = P.record_of(b)
    assert rec["captor"] == w.vessels.own.id and rec["goal"] == "falmouth" and rec["company"]
    assert rec["master"] and rec["crew"] >= P.PRIZE_CREW_LEAST and rec["prisoners"] > 0
    assert b.nation == "britain" and b.signals.colours.over == "france"  # his colours over hers
    said = w.readings.words("prize")
    assert "Deux Frères" in said and "in company" in said
    truth = director_readings(w)
    assert truth["prizes"] and "Deux Frères, a prize of the Amazon's" in truth["prizes"][0]
    assert f"{rec['crew']} hands" in truth["prizes"][0] and "in company" in truth["prizes"][0]
    assert any("Deux Frères" in row for row in truth.get("prisoners", [])) or rec["prisoners"]
    # the form in play, after the first minute, is doubted: a ship is taken by the guns
    from freesail.world import orders as WO

    doubt = WO.doubt(w, WO.parse('ship "Deux Frères": a prize of the Amazon'))
    assert doubt is not None and "scenario's start" in doubt
    e = w.world_order('ship "Deux Frères": a prize of the Amazon', "the test")
    assert e.data.get("result") != "done" and "a prize already" in e.text


def test_the_captive_scenario_begins_with_the_player_a_prisoner_aboard_the_captor():
    """`captive.yaml`: the Amazon struck to the Didon by the scenario's world order, the Didon
    made a full ship and the player her prisoner in the cabin, his parole asked in the captor's
    words a minute after; the prompt his (`where am I`, `say to the captain: I give my parole`
    answers the parole); the director on the captive's brief."""
    from freesail.agents import director as D

    sf, w = _begun(CAPTIVE)
    me = C.captive_person(w)
    assert me is not None and me.name == "Captain Bowen"
    didon = w.vessels.find("Didon")
    assert didon is not None and didon.crew is not None and me.hull == didon.id
    assert P.is_prize(w.vessels.own) and P.record_of(w.vessels.own)["captor"] == didon.id
    assert any(e.kind == "prize.parole_asked" for e in didon.crew.log)
    said = w.submit("where am i").text
    assert "aboard the Didon" in said and "a prisoner, his parole asked" in said
    out = w.submit("say to the captain: I give my parole")
    assert out.kind != "order.rejected", out.text
    w.run(60)
    assert any(e.kind == "prize.parole" for e in didon.crew.log)
    assert C.state_words(w, me) == "a prisoner on parole"
    brief = D.brief_of(w)
    assert brief is not None and brief.name == "The captive"
    assert brief.limits["enemy_heaviest"] == "frigate" and brief.limits["nobody_dies"]
    truth = director_readings(w)
    assert any("Amazon, a prize of the Didon's" in row for row in truth["prizes"])
    assert any("Captain Bowen (given)" in row for row in truth["prisoners"])


def _by_order(w, description: str, nation: str, position, goal: str, intent: str, name: str):
    """A ship put on the sea by the director's form, so that a replay makes her again (a
    vessel a test adds by hand is in no journal)."""
    from freesail.world.geo import format_position

    where = format_position(position).replace("°", "").replace("'", "").replace(",", "")
    order = f'ship: a {description} "{name}" of {nation} at {where}, {goal}, intent: {intent}'
    e = w.world_order(order, "the test")
    assert e.data.get("result") == "done", e.text
    v = w.vessels.find(name)
    assert v is not None
    return v


@pytest.mark.slow
def test_a_passage_with_the_player_taken_and_the_parole_exchanged_replays_by_both_roads():
    """84's acceptance form (truth 7-368): a French frigate put on the sea three cables off by
    the director's form and made a full ship at the first switch; the player's ship struck to
    her by the form (`ship "the ship": struck to the Renard`), the player taken aboard her,
    his parole asked by her captain's doctrine and given in his own words, the two under way
    for her port an hour; saved, the passage replays by its transcript and by its acts to the
    same digests of both hulls' logs."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    w = world_at(49.5, -5.5)
    w.submit("heave to")
    w.run(60)
    q = destination(w.position, 90.0, 3.0 * units.CABLE)
    renard = _by_order(w, "frigate", "France", q, "bound for Brest", "bound for Brest", "Renard")
    for _ in range(3):
        w.run(60)
        if renard.crew is not None and renard.crew.shape == "full":
            break
    assert renard.crew is not None and renard.crew.shape == "full"
    e = w.world_order('ship "the ship": struck to the Renard', "the test")
    assert e.data.get("result") == "done", e.text
    enemy = renard.crew
    me = C.captive_person(w)
    assert me is not None and me.hull == enemy.id
    for _ in range(3):
        w.run(60)
    out = w.submit("say to the captain: I give my parole")
    assert out.kind != "order.rejected", out.text
    w.run(3600)
    assert any(e.kind == "prize.parole" for e in enemy.log)
    data = json.loads(json.dumps(w.save()))
    want = (w.log.digest(), enemy.log.digest())
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        got = (copy.log.digest(), copy.hulls[enemy.id].log.digest())
        assert got == want, (road, got, want)


@pytest.mark.slow
def test_a_far_fights_passage_replays_by_both_roads_to_the_same_records():
    """Truth 7-368's second half: two far ships in anger twelve miles off, put on the sea by
    the director's forms (the French frigate on the King's cutter, the cap nought), the rounds
    fired until she strikes; saved, the passage replays by both roads to the same digest of the
    player's log and the same far records (the `far` stream opened at the first round and
    drawn again alike)."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    w = world_at(49.5, -5.5, crewed={"cap": 0})
    w.submit("heave to")
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    a = _by_order(
        w,
        "frigate",
        "France",
        far,
        "cruising off the Lizard within 20 miles",
        "cruise for prizes off the Lizard within 20 miles",
        "Renard",
    )
    q = destination(far, 90.0, 1.5 * units.NAUTICAL_MILE)
    b = _by_order(
        w,
        "cutter",
        "Britain",
        q,
        "cruising off the Lizard within 20 miles",
        "cruise off the Lizard within 20 miles",
        "Sprightly",
    )
    for _ in range(90):
        w.run(60)
        if b.struck:
            break
    assert b.struck and int(a.damage.get("rounds", 0) or 0) >= 1
    data = json.loads(json.dumps(w.save()))
    want = (w.log.digest(), dict(a.damage), dict(b.damage))
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        ca, cb = copy.vessels.get(a.id), copy.vessels.get(b.id)
        assert ca is not None and cb is not None, road
        got = (copy.log.digest(), dict(ca.damage), dict(cb.damage))
        assert got == want, (road, got[0] == want[0], got[1], want[1])
