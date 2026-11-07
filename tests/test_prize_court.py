"""The prize court and the money (spec M7 §18 and §20; package 74, step 5; the design in
`docs/design/Design-Prizes.md` §5): the valuation by the rows, the court sitting where the
prize is brought in, the sentence by the rules (condemned, restored with costs, salvage), the
money by the eighths of the scheme in force at the date (Lavery, Nelson's Navy, p. 116, for
the two British schemes), shared among the ships in sight at the strike, the purse's line, the
reading `the prize money`, the director's word to the court and its doubt."""

from __future__ import annotations

from datetime import date

import pytest

from freesail import units
from freesail.combat import action
from freesail.world import prize_court as PC
from freesail.world import prizes as P
from freesail.world.geo import destination
from tests.test_brains import put
from tests.test_prizes import _frigate

FALMOUTH_ROAD = {"lat_deg": 50.133, "lon_deg": -5.035}


# -- the rows --------------------------------------------------------------------------------------


def test_the_schemes_are_laverys_two_british_ones_by_date_and_the_rows_say_their_sources():
    """The eighths before 1808 (the captain three eighths, three classes an eighth each, the
    crew a quarter) and from 1808 (the captain two eighths, two classes an eighth, the petty
    officers and the crew a half), each citing Lavery p. 116; a privateer's by her articles
    (from memory, marked); France's and Spain's the British eighths, said so."""
    before = PC.scheme_for("britain", date(1805, 6, 12))
    after = PC.scheme_for("britain", date(1809, 1, 1))
    assert "Lavery" in before["source"] and "1708" in before["source"]
    assert "Lavery" in after["source"] and "1808" in after["source"]
    assert [c["share"] for c in before["classes"]] == [0.375, 0.125, 0.125, 0.125, 0.25]
    assert [c["share"] for c in after["classes"]] == [0.25, 0.125, 0.125, 0.5]
    assert abs(sum(c["share"] for c in before["classes"]) - 1.0) < 1e-9
    assert abs(sum(c["share"] for c in after["classes"]) - 1.0) < 1e-9
    assert (
        "flag officer" in before["classes"][0]["note"]
        and "not modelled" in before["classes"][0]["note"]
    )
    assert "FROM MEMORY" in after["classes"][3]["note"]
    privateer = PC.scheme_for("france", date(1805, 6, 12), service="privateer")
    assert [c["share"] for c in privateer["classes"]] == [0.5, 0.5] and "FROM MEMORY" in privateer[
        "source"
    ]
    spain = PC.scheme_for("spain", date(1805, 6, 12))
    assert spain.get("british_kept") and spain["classes"] == before["classes"]
    assert "decision 64" in spain["source"]
    rows = PC.money_rows()
    assert rows["head_money_pounds"] == 5.0 and rows["agent_share"] == 0.05
    assert rows["in_sight_shared"] and rows["in_sight_division"] == "complements"
    assert PC.court_days(_port_like("britain")) == 7 and PC.court_days(_port_like("spain")) == 10


def _port_like(nation: str):
    class _P:
        name = "X"

    p = _P()
    p.nation = nation
    return p


def test_the_valuation_is_the_rows_over_the_files_figures():
    """A merchant brig of 304 tons burthen (her displacement over 1.36) at £8 a ton worn ten
    years at two per cent: £1,944; her four long 6s at £4 the hundredweight, £320; a frigate
    at the man of war's £12."""
    w = _frigate()
    from freesail.world.geo import Position
    from freesail.world.ships import Vessel

    brig = Vessel("x", "X", "a brig", "data/ships/brig.yaml", "france", Position(49.4, -5.4))
    brig.description = "merchant brig"
    val = PC.valuation(w, brig)
    # her four long 6s of 20 cwt at £4 the hundredweight (the merchant brig's own file since
    # package 75's SW-4; the brig-sloop's eighteen gave £1,248 before the trunk's merge)
    assert val["tons"] == 304 and val["hull"] == 1944.0 and val["guns"] == 320.0
    frigate = Vessel(
        "y", "Y", "a ship", "data/ships/frigate-36.yaml", "france", Position(49.4, -5.4)
    )
    frigate.description = "frigate"
    fv = PC.valuation(w, frigate)
    assert fv["tons"] > 800 and abs(fv["hull"] - fv["tons"] * 12.0 * 0.8) <= 12.0


# -- the court at the port -------------------------------------------------------------------------


def _frigate_at(position: dict, seed: int = 7):
    from datetime import datetime

    from freesail.core.world import Scenario
    from tests.test_brains import FRIGATE, make_world

    return make_world(
        seed,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=270.0,
            wind_speed_kn=14.0,
            gustiness=0.0,
            variability=0.0,
            position=position,
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            nation="britain",
        ),
    )


def _taken_in_falmouth_road(consort: bool = False):
    """The frigate hove to in Falmouth's road with the French brig struck and taken; with
    `consort`, a King's cutter a mile off in sight at the strike."""
    w = _frigate_at(FALMOUTH_ROAD)
    w.submit("set plain sail")
    w.submit("heave to")
    # the brig six cables off, as `_struck_brig` puts her, from a world at the road
    e = w.world_order('ship: a merchant brig "X" of France at 50 07.5 N 5 02 W, bound for Brest')
    assert e.data.get("result") == "done", e.text
    assert w.world_order('ship "X": intent bound for Brest').data.get("result") == "done"
    w.run(61)
    b = w.vessels.find("X")
    hull = b.crew
    assert hull is not None and hull.shape == "full"
    assert w.world_order('ship "X": order heave to for a watch').data.get("result") == "done"
    cutter = None
    if consort:
        q = destination(w.position, 90.0, 1.0 * units.NAUTICAL_MILE)
        cutter = put(
            w,
            "cutter",
            "britain",
            {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
            "cruising off the Lizard within 20 miles",
            intent="cruise off the Lizard within 20 miles",
            colours="shown",
            name="Sprightly",
        )
    w.run(120)
    action.strike(hull, False, "to the frigate")
    assert w.submit("take possession of her").kind == "prize.taken"
    return w, b, hull, cutter


def test_the_prize_is_condemned_and_the_money_paid_by_the_eighths_into_the_purse():
    """The design's §5.2 and §5.3 (truth 7-362): the French brig taken is condemned (France at
    war with Britain at the taking), valued by the rows (the hull £1,944, her guns £320,
    her powder and shot), nothing for the head money (a merchantman), the agent's five per
    cent and the court's fees deducted, the whole into the frigate's purse with the purse's
    line saying the eighths of 1805 (the captain three eighths), the account's lines as the
    prize account's, the reading `the prize money` the same; the ships in sight at the strike
    share by their complements."""
    w, b, hull, cutter = _taken_in_falmouth_road(consort=True)
    rec = P.record_of(b)
    assert rec["captor_nation"] == "britain" and rec["captor_complement"] == 264
    assert any(s["name"] == "Sprightly" for s in rec["in_sight"])
    assert not any(s["id"] == b.id for s in rec["in_sight"])
    port = w.ports.ports["falmouth"]
    assert PC.verdict(w, b, rec, port) == (
        "condemned",
        "a ship of France at war with the captors at the taking",
    )
    before = w.purse.pounds
    acc = PC.sentence(w, b, port)
    assert acc["sentence"] == "condemned" and acc["head_money"] == 0.0
    assert acc["valuation"]["hull"] == 1944.0 and acc["valuation"]["guns"] == 320.0
    assert acc["agent"] == round(acc["gross"] * 0.05) and acc["fees"] == 20.0
    assert acc["net"] == acc["gross"] - acc["agent"] - 20.0 and acc["reserved"] == 0.0
    ours, theirs = acc["shares"]
    assert ours["name"] == "Amazon" and theirs["name"] == "Sprightly"
    assert ours["pounds"] + theirs["pounds"] == acc["paid"]
    assert ours["pounds"] > theirs["pounds"] * 3  # by the complements, 264 to the cutter's
    assert ours["classes"][0] == ("the captain", round(ours["pounds"] * 0.375))
    assert w.purse.pounds == before + ours["pounds"]
    money = [e for e in w.log if e.kind == "prize.money"]
    assert len(money) == 1
    text = money[0].text
    assert text.startswith(
        "Prize money paid at Falmouth for the X, condemned by the High Court of Admiralty"
    )
    assert (
        "the head money £0 (a merchantman)" in text
        and "shared with Sprightly, in sight at the strike" in text
    )
    assert "the captain £" in text and text.endswith(f"The purse: {w.purse.words()}.")
    assert any(
        e.kind == "paper.written" and e.data.get("paper") == "the prize account" for e in w.log
    )
    assert w.readings.words("prize_money").startswith(
        "the X condemned by the High Court of Admiralty"
    )
    assert "the captain £" in w.readings.words("prize_money")
    assert b.prize["court"]["sentence"] == "condemned"
    assert any("condemned by the High Court" in words for _, words in b.story)
    # the court's sitting from the prize's own minute: lying in the port at anchor, the job is
    # queued due in the court's days
    assert (
        hull.captain.give("come to an anchor", why="the prize brought in").kind != "order.rejected"
    )
    for _ in range(10):
        w.run(60)
        if hull.dealings.in_port() is not None:
            break
    assert hull.dealings.in_port() is not None and hull.dealings.in_port().id == "falmouth"
    b.prize.pop("court")  # the sentence above was the rule's function; the minute queues the job
    w.run(60)
    jobs = [j for j in hull.dealings.jobs if j.kind == "prize_court"]
    assert len(jobs) == 1 and jobs[0].due_tick == b.prize["court_due"]
    assert jobs[0].due_tick - w.clock.tick <= 7 * 86400 and jobs[0].payload["prize"] == b.id
    assert any(e.kind == "prize.court_sits" and "in 7 days" in e.text for e in hull.log)


def test_a_neutral_wrongly_taken_is_restored_with_costs_against_the_captors():
    """The design's §5.2 (truth 7-363): a Danish brig at peace with Britain, struck and taken
    all the same, is restored to her owners by the court (her nation, colours, muster and
    people hers again by the swap, the prize master her prisoner), with costs and damages a
    tenth of her valuation paid from the captor's purse, the line saying why."""
    w = _frigate()
    w.submit("set plain sail")
    w.submit("heave to")
    e = w.world_order(
        'ship: a merchant brig "Anna Maria" of Denmark at 49 30 N 5 29 W, bound for Brest'
    )
    assert e.data.get("result") == "done", e.text
    w.world_order('ship "Anna Maria": intent bound for Brest')
    w.run(61)
    b = w.vessels.find("Anna Maria")
    hull = b.crew
    w.world_order('ship "Anna Maria": order heave to for a watch')
    w.run(120)
    action.strike(hull, False, "to the frigate")
    assert w.submit("take possession of her").kind == "prize.taken"
    port = w.ports.ports["falmouth"]
    rec = P.record_of(b)
    kind, why = PC.verdict(w, b, rec, port)
    assert kind == "restored" and "neutral" in why and "Denmark" in why
    w.purse.receive(1000.0, "the owner", "a sum for the voyage", w.clock.tick)
    before = w.purse.pounds
    acc = PC.sentence(w, b, port)
    assert acc["sentence"] == "restored" and acc["costs"] == round(1944.0 * 0.1)
    assert w.purse.pounds == before - acc["costs"]
    assert any(k == "paid" and p == acc["costs"] for _, k, p, _to, _l in w.purse.ledger)
    assert not P.is_prize(b) and b.nation == "denmark" and b.prize["retaken"][0] == "restored"
    assert hull.stations.holder("captain").name != rec["master"]
    said = [e for e in w.log if e.kind == "prize.sentenced"]
    assert said and "restored to her owners" in said[0].text and "costs and damages" in said[0].text
    assert w.readings.words("prize_money").startswith("the Anna Maria restored")


def test_the_directors_word_to_the_court_is_doubted_against_the_rule_and_performs_with_a_reason():
    from freesail.world import orders as WO

    w, b, hull, _ = _taken_in_falmouth_road()
    order = WO.parse("port falmouth: the court restores the X")
    doubt = WO.doubt(w, order)
    assert doubt is not None and "the court's rule gives condemned" in doubt
    assert WO.doubt(w, WO.parse("port falmouth: the court condemns the X")) is None
    e = w.world_order(
        "port falmouth: the court restores the X [reason: a flaw in the papers]", "the test"
    )
    assert e.data.get("result") == "done", e.text
    assert b.prize["court"]["sentence"] == "restored" and not P.is_prize(b)
    e = w.world_order("port falmouth: the court condemns the Nancy", "the test")
    assert e.data.get("result") != "done" and "No prize named" in e.text


def test_a_kings_ships_prize_of_war_pays_three_fourths_now_and_the_reserved_fourth_on_its_day():
    """The design's §5.3: a prize of war taken by a King's ship and purchased for the service
    pays head money (five pounds a head of the men aboard at the start) and three fourths of
    the net now, a fourth reserved for the later sentence in the court's days, paid from the
    prize's own minute when the day comes (the owner may turn the purchase off by the row)."""
    w, b, hull, _ = _taken_in_falmouth_road()
    port = w.ports.ports["falmouth"]
    rec = P.record_of(b)
    rec["role_was"], rec["men_at_start"] = "privateer", 80  # a privateer brig, as the record
    assert rec["service"] == "kings"  # of a King's frigate's taking
    before = w.purse.pounds
    acc = PC.sentence(w, b, port)
    assert acc["sentence"] == "condemned" and acc["head_money"] == 400.0
    assert (
        acc["reserved"] == round(acc["net"] * 0.25) and acc["paid"] == acc["net"] - acc["reserved"]
    )
    assert w.purse.pounds == before + acc["paid"]
    assert "reserved for the purchase for the service" in w.log[-1].text or any(
        "reserved for the purchase" in e.text for e in w.log if e.kind == "prize.money"
    )
    rec = P.record_of(b)
    assert rec["reserved_due"] - w.clock.tick == 7 * 86400
    w.run(60)
    assert w.purse.pounds == before + acc["paid"]  # not before its day
    b.prize["reserved_due"] = w.clock.tick  # the court's days run (the test's hand on the clock)
    w.run(60)
    assert w.purse.pounds == before + acc["paid"] + acc["reserved"]
    paid = [e for e in w.log if e.kind == "prize.money" and e.data.get("reserved")]
    assert len(paid) == 1 and "reserved fourth" in paid[0].text
    assert P.record_of(b).get("reserved_due") is None and acc.get("reserved_paid")
    w.run(60)
    assert w.purse.pounds == before + acc["paid"] + acc["reserved"]  # once


def test_a_ship_retaken_by_her_own_nations_cruiser_is_restored_with_salvage_to_the_recaptors():
    """The design's §5.2: the brig taken by the frigate and retaken by a French privateer
    coming up is, at a French port, her owners' again with salvage to the recaptors (an
    eighth of her value, the French rows' British eighths kept and said), the recaptors the
    sharers and not the frigate's consorts in sight at the first strike."""
    w, b, hull, cutter = _taken_in_falmouth_road(consort=True)
    far = destination(w.position, 180.0, 6.0 * units.NAUTICAL_MILE)
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Vengeur",
    )
    P.retake(w, b, by="the Vengeur coming up", how="retaken", captor=pv)
    rec = P.record_of(b)
    assert not P.is_prize(b) and rec["recaptor"] == pv.id and b.nation == "france"
    brest = w.ports.ports["brest"]
    assert PC.verdict(w, b, rec, brest) == (
        "salvage",
        "a ship of her own nation retaken from the enemy",
    )
    before = w.purse.pounds
    acc = PC.sentence(w, b, brest)
    assert acc["sentence"] == "salvage" and acc["head_money"] == 0.0
    val = acc["valuation"]
    whole = val["hull"] + val["guns"] + val["stores"] + acc["cargo"] + acc["goods"]
    assert acc["gross"] == round(whole * 0.125) and acc["goods"] > 0  # her powder and shot too
    assert [s["name"] for s in acc["shares"]] == ["Vengeur"]  # not the Amazon, not Sprightly
    assert acc["shares"][0]["pounds"] == acc["paid"] > 0
    assert "Conseil des prises" in acc["court"]
    assert w.purse.pounds == before  # the frigate's purse gets nothing of it
    assert any("salvage by le Conseil des prises" in words for _, words in b.story)


# -- the far court ---------------------------------------------------------------------------------


@pytest.mark.slow
def test_a_far_prize_in_her_goals_road_is_sentenced_on_her_record():
    """The cut-out prize bound for Brest with no hull: in the road the court's days run on her
    record and the sentence is written there (her captor at far detail has no purse: the
    account on the record alone)."""
    from tests.test_brains import world_at
    from tests.test_squadrons import STATION_INTENT

    w = world_at(49.5, -5.5, intent=STATION_INTENT)
    w.crewed_settings = {"cap": 0}
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    prey = put(
        w,
        "merchant brig",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for the Start",
        name="Nancy",
    )
    prey.sailing_factor = 0.85
    q = destination(far, 270.0, 1.2 * units.NAUTICAL_MILE)
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Vengeur",
    )
    pv.sailing_factor = 1.0  # as 72's scene has her: a fast schooner on a dull brig
    for _ in range(150):
        w.run(60)
        if P.is_prize(prey):
            break
    rec = P.record_of(prey)
    assert rec is not None and rec["goal"] == "brest"
    # in Brest's road (the test's hand on her position: the passage is a day's)
    port = w.ports.ports["brest"]
    prey.position = port.outer_road.position
    w.run(60)
    rec = P.record_of(prey)
    assert rec.get("court_due") and rec["court_port"] == "brest"
    prey.prize["court_due"] = w.clock.tick  # the court's days run (the test's hand on the clock)
    w.run(60)
    rec = P.record_of(prey)
    court = rec.get("court")
    assert court and court["sentence"] == "condemned" and "Conseil des prises" in court["court"]
    assert court["shares"][0]["name"] == "Vengeur" and court["paid"] > 0
    assert any("condemned by le Conseil des prises" in words for _, words in prey.story)
