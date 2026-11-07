"""The prize (spec M7 §18; package 74, step 2; the design in `docs/design/Design-Prizes.md`
§2): possession taken of a struck ship within a boat's pull by the order and at once by the
officer on a deck carried; the prize as a hull of the one world under a new nation, goal
and role, her muster swapped for the prize crew's and her people her prisoners; the prize
master at her captain's station; the prisoners taken aboard by the boat; the rising; the
far cut-out's possession on the records, the privateer parting from her prize and a cruiser
retaking her; the prize burnt; the readings and the events; the save."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail import units
from freesail.combat import action
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.world import prizes as P
from freesail.world.geo import destination
from tests.test_brains import FRIGATE, make_world, put, world_at
from tests.test_squadrons import STATION_INTENT

ships = pytest.importorskip("freesail.world.ships")


def _frigate(seed: int = 7):
    return make_world(
        seed,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=270.0,
            wind_speed_kn=14.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 49.5, "lon_deg": -5.5},
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            nation="britain",
        ),
    )


def _struck_brig(seed: int = 7):
    """The frigate hove to with a French brig put on the sea six cables off and promoted at
    the first switch, held hove to by the director's hand within a boat's pull, and struck
    to the frigate by her colours (`action.strike` with the words, as her captain would)."""
    w = _frigate(seed)
    w.submit("set plain sail")
    w.submit("heave to")
    e = w.world_order('ship: a merchant brig "X" of France at 49 30 N 5 29 W, bound for Brest')
    assert e.data.get("result") == "done", e.text
    assert w.world_order('ship "X": intent bound for Brest').data.get("result") == "done"
    w.run(61)
    b = w.vessels.find("X")
    hull = b.crew
    assert hull is not None and hull.shape == "full"
    assert w.world_order('ship "X": order heave to for a watch').data.get("result") == "done"
    w.run(120)
    action.strike(hull, False, "to the frigate")
    assert b.struck and hull.ship.extra.get("struck")
    return w, b, hull


def _nm(a, b) -> float:
    return P._bearing_distance(a.position, b.position)[1] / units.NAUTICAL_MILE


def _events(log, kind: str) -> list:
    return [e for e in log if e.kind == kind]


# -- possession taken near ---------------------------------------------------------------------


def test_take_possession_of_a_struck_brig_within_a_boats_pull_makes_her_a_prize_of_ours():
    """The design's §2.1 to §2.5: `take possession of her` on the struck brig six cables off
    writes her record (how, when, her nation and intent before), draws the prize crew out of
    our muster (our bill short by them, hers theirs), puts the prize master (the ladder's
    man: a master's mate, the first lieutenant kept) at her captain's station with his home
    the prize, confines her people below (her officers in the cabin, her men in the hold),
    hoists our colours over hers, and gives her our nation, the prize master's role and the
    intent of our doctrine's port; she keeps our company by the set."""
    w, b, hull = _struck_brig()
    ours = len(w.ship.extra["crew"].sailors)
    hers = len(hull.ship.extra["crew"].sailors)
    her_captain = hull.people.captain
    out = w.submit("take possession of her")
    assert out.kind == "prize.taken", out.text
    rec = P.record_of(b)
    assert rec is not None and P.is_prize(b)
    assert rec["how"] == "taken possession of" and rec["captor"] == w.own.id
    assert rec["nation_was"] == "france" and rec["intent_was"] == "bound for Brest"
    assert rec["men_at_start"] == hers and rec["prisoners"] == hers
    crew = rec["crew"]
    assert P.PRIZE_CREW_LEAST <= crew <= ours // 3
    # the muster swap: our bill short by the prize crew, hers the prize crew's, her people
    # the prisoners' record
    assert len(w.ship.extra["crew"].sailors) == ours - crew
    assert len(hull.ship.extra["crew"].sailors) == crew
    pris = P.prisoners_of(hull.ship)
    assert pris is not None and pris.count == hers and pris.nation == "france"
    assert hull.ship.extra["routine"].crew is hull.ship.extra["crew"]  # the keeper re-pointed
    # the prize master: the ladder's man, at her captain's station, at home in her
    master = hull.stations.holder("captain")
    assert master is not None and master.name == rec["master"]
    assert master.role in ("lieutenant", "master's mate", "midshipman", "mate")
    assert master.role != "first lieutenant"
    assert master.hull == b.id and master.home == b.id
    assert hull.people.captain is master and master.id == rec["master_id"]
    assert rec["master_home"] == w.own.id
    # her people confined by their rank
    assert her_captain.confined_to == "cabin" and her_captain.where == "cabin"
    places = {p.confined_to for p in hull.people.people if p.confined_to}
    assert places == {"cabin", "hold"}
    # her colours, nation, role and intent
    colours = b.signals.colours
    assert b.nation == "britain" and colours.state == "shown" and colours.over == "france"
    assert "over French" in colours.words(w.nations)
    assert b.role == P.PRIZE_MASTER_ROLE and b.intent_words == "carry the prize to Falmouth"
    assert rec["goal"] == "falmouth" and rec["service"] == "kings"
    assert hull.captain.doctrine.role == P.PRIZE_MASTER_ROLE
    assert hull.captain.intent is not None and hull.captain.intent.destination == "falmouth"
    assert not b.struck and not hull.ship.extra.get("struck")
    # her company
    company = w.squadrons.commanded_by(w.own.id)
    assert company is not None and b.id in company.prizes and rec["company"] == company.id
    # the lines: ours urgent on our log, hers on hers, the stories
    taken = _events(w.log, "prize.taken")
    assert len(taken) == 1 and "Possession taken of the X" in taken[0].text
    assert _events(hull.log, "prize.possessed") and any(
        e.kind == "person.aboard" and "as prize master" in e.text for e in hull.log
    )
    assert any("possession taken of the X" in words for _, words in w.vessels.own.story)
    assert any("taken by the Amazon" in words for _, words in b.story)
    # the readings
    words = w.readings.words("prize")
    assert "the X, taken possession of, under" in words and "for Falmouth, in company" in words
    assert "prize crew of" in hull.readings.words("prize_crew")
    assert "prisoners, confined below" in hull.readings.words("prisoners")
    assert "in the cabin (parole not asked)" in hull.readings.words("prisoners")
    assert w.readings.words("prisoners") == "no prisoners"
    assert w.readings.words("prize_crew") == "she is no prize"


def test_take_possession_is_refused_in_its_five_ways():
    """Not struck; beyond a boat's pull; a prize already; our own colours struck; the boat
    away: each refused in words, nothing done."""
    from freesail.orders.errors import OrderError

    w = _frigate()
    w.submit("set plain sail")
    w.submit("heave to")
    w.world_order('ship: a merchant brig "X" of France at 49 30 N 5 29 W, bound for Brest')
    w.world_order('ship "X": intent bound for Brest')
    w.run(61)
    b = w.vessels.find("X")
    hull = b.crew
    w.world_order('ship "X": order heave to for a watch')
    w.run(60)
    # 1. she has not struck
    out = w.submit("take possession of her")
    assert out.kind == "order.rejected" and "No ship has struck to us" in out.text
    out = w.submit("take possession of the X")
    assert out.kind == "order.rejected" and "has not struck; her colours are flying" in out.text
    # 2. beyond a boat's pull: a struck ship four miles off
    far = destination(w.position, 90.0, 4.0 * units.NAUTICAL_MILE)
    v = put(
        w,
        "merchant brig",
        "france",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for Brest",
        name="Far",
    )
    v.struck = True
    out = w.submit("take possession of the X")  # the brig near has not struck
    assert out.kind == "order.rejected"
    out = w.submit(f"take possession of the {v.name}")
    assert out.kind == "order.rejected" and "beyond a boat's pull" in out.text
    assert not P.is_prize(v)
    # 3. a prize already
    action.strike(hull, False, "to the frigate")
    assert w.submit("take possession of her").kind == "prize.taken"
    out = w.submit("take possession of the X")
    assert out.kind == "order.rejected" and "is a prize already" in out.text
    # 4. our own colours struck
    action.strike(w, False, "the test")
    out = w.submit("take possession of the X")
    assert out.kind == "order.rejected" and "Our own colours are struck" in out.text
    w.ship.extra.pop("struck")
    # 5. the boat away
    boat = w.dealings.boat
    boat.away = True
    with pytest.raises(OrderError):
        from freesail.orders.prize import _boat_ready

        _boat_ready(w)
    out = w.submit("take four of the prisoners aboard")
    assert out.kind == "order.rejected" and "is away" in out.text
    boat.away = False


def test_the_prisoners_are_taken_aboard_by_the_boat_so_many_at_a_time_and_counted():
    """`take six of the prisoners aboard`: six of hers into our hold, prisoners of ours
    (`the prisoners` on our ship counts them), six fewer in her; `take the prisoners aboard`
    the rest; refused when she has none left."""
    w, b, hull = _struck_brig()
    assert w.submit("take possession of her").kind == "prize.taken"
    hers = P.prisoners_of(hull.ship).count
    out = w.submit("take six of the prisoners aboard")
    assert out.kind == "prize.prisoners_aboard" and out.data["taken"] == 6, out.text
    assert P.prisoners_of(hull.ship).count == hers - 6
    ours = P.prisoners_of(w.ship)
    assert ours is not None and ours.count == 6 and ours.nation == "france"
    assert all(s.id.startswith(f"{b.id}:") for s in ours.crew.sailors)
    assert w.readings.words("prisoners").startswith("six prisoners, confined below")
    assert "(six more taken out of her)" in hull.readings.words("prisoners")
    out = w.submit("take 20 of the prisoners aboard from the X")
    assert out.kind == "prize.prisoners_aboard" and out.data["taken"] == 20
    out = w.submit("take the prisoners aboard")
    assert out.kind == "prize.prisoners_aboard" and out.data["taken"] == hers - 26
    assert P.prisoners_of(hull.ship).count == 0 and P.prisoners_of(w.ship).count == hers
    w.run(60)  # the readings are the minute's
    # her people's count is nought; her officers of rank are persons confined in her still
    # (the named few are not moved by the boat's loads: the design's §2.2 and §3.5)
    words = hull.readings.words("prisoners")
    assert words.startswith(
        "eleven prisoners of rank: Captain Pope in the cabin (parole not asked)"
    )
    out = w.submit("take the prisoners aboard")
    assert out.kind == "order.rejected" and "has no prisoners left" in out.text


def test_a_prize_is_burnt_by_the_order_her_people_prisoners_and_the_prize_crew_home():
    """`burn the prize`: her people into our hold as prisoners, the prize crew home again
    (our bill whole), the prize master with them at home, the vessel gone from the sea with
    the word, the line saying nothing is to be had for her but the head money; `scuttle the
    prize` the same, sunk; refused for a ship that is no prize of ours."""
    w, b, hull = _struck_brig()
    ours = len(w.ship.extra["crew"].sailors)
    assert w.submit("take possession of her").kind == "prize.taken"
    rec = dict(P.record_of(b))
    master = hull.stations.holder("captain")
    out = w.submit("burn the prize")
    assert out.kind == "prize.burnt" and out.data["how"] == "burnt", out.text
    assert "The X is burnt: her people" in out.text and "head money" in out.text
    assert b.done and P.record_of(b)["fate"][0] == "burnt"
    assert len(w.ship.extra["crew"].sailors) == ours
    assert P.prisoners_of(w.ship).count == rec["prisoners"]
    assert master.hull == w.own.id and master.home == w.own.id and not master.confined_to
    assert len(_events(w.log, "prize.burnt")) == 1
    assert w.readings.words("prize") == "no prize"
    assert any("the X burnt" in words for _, words in w.vessels.own.story)
    # a stranger is no prize of ours
    far = destination(w.position, 90.0, 0.5 * units.NAUTICAL_MILE)
    v = put(
        w,
        "merchant brig",
        "france",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for Brest",
    )
    out = w.submit(f"scuttle the {v.name}")
    assert out.kind == "order.rejected" and "is no prize of ours" in out.text


# -- the rising ---------------------------------------------------------------------------------


def _stood_off(seed: int, taken: int = 0):
    """The prize taken, so many of her prisoners taken aboard, the frigate filled away and
    stood off beyond the cover distance; the hours since the taking set back nineteen on
    the record (the test's hand on the clock: a prize crew tired by the hours) so that the
    rule is judged at its next hour."""
    w, b, hull = _struck_brig(seed)
    assert w.submit("take possession of her").kind == "prize.taken"
    if taken:
        assert w.submit(f"take {taken} of the prisoners aboard").kind == "prize.prisoners_aboard"
    w.submit("fill away")
    w.submit("steer west")
    for _ in range(45):
        w.run(60)
    assert _nm(w.vessels.own, b) > P.COVER_NM
    rec = P.record_of(b)
    rec["taken_at"] -= 19 * 3600
    rec["rising_judged"] = rec["taken_at"]
    return w, b, hull


def _risings(hull) -> list[str]:
    return [e.kind for e in hull.log if e.kind.startswith("prize.rising")]


@pytest.mark.slow
def test_the_prisoners_rise_on_a_thin_tired_prize_crew_with_no_captor_near_and_retake_her():
    """The design's §2.8: a hundred and twenty-one prisoners over a prize crew of
    twenty-one (the King's ship's share of our two hundred and sixty-four), nineteen hours in
    her, the frigate two miles off: the rule draws once an
    hour (a quarter's chance) and at seed 1 they rise in the first hour and have the deck by
    73's tables; she is retaken by her own people (her nation, colours, role and intent
    hers again, the prize crew her prisoners, the prize master a captive in her cabin), the
    frigate's log says so with the prize lost. At seed 7 the two draws of the first two
    hours fail and nothing is said."""
    w, b, hull = _stood_off(1)
    for _ in range(61):
        w.run(60)
        if _risings(hull):
            break
    assert _risings(hull) == ["prize.rising", "prize.rising_won"]
    rec = P.record_of(b)
    assert rec["retaken"][0] == "retaken" and rec["retaken"][1] == "the prisoners rising"
    assert b.nation == "france" and b.role == "merchant" and b.intent_words == "bound for Brest"
    assert b.signals.colours.state == "shown" and b.signals.colours.over == ""
    assert not P.is_prize(b)
    pris = P.prisoners_of(hull.ship)
    assert pris is not None and pris.nation == "britain" and pris.count <= 21
    master = w.people.find(rec["master"]) or hull.people.find(rec["master"])
    assert master is not None and master.confined_to == "cabin"
    assert hull.stations.holder("captain") is not master
    assert _events(hull.log, "prize.retaken") and _events(w.log, "prize.lost")
    assert "retaken (the prisoners rising)" in _events(w.log, "prize.lost")[0].text
    w2, b2, hull2 = _stood_off(7)
    for _ in range(125):
        w2.run(60)
    assert _risings(hull2) == [] and P.is_prize(b2)


@pytest.mark.slow
def test_a_rising_put_down_puts_the_prisoners_in_irons_for_a_day_and_the_odds_rule_holds():
    """With seventy of her people taken into the frigate first (fifty-one over the prize
    crew of twenty-one, the odds over two to one), the rising at the seed found is put down
    in the third hour: the prisoners in irons for a day (the reading says so), the prize ours
    still. With a hundred taken (twenty-one over twenty-one) the rule never draws: the odds
    are under two to one."""
    w, b, hull = _stood_off(PUT_DOWN_SEED, taken=70)
    for _ in range(250):
        w.run(60)
        if _risings(hull):
            break
    assert _risings(hull) == ["prize.rising", "prize.rising_down"], _risings(hull)
    pris = P.prisoners_of(hull.ship)
    assert pris.in_irons(w.clock.tick) and P.is_prize(b)
    assert ", in irons" in hull.readings.words("prisoners")
    assert pris.irons_until - w.clock.tick <= P.IRONS_HOURS * 3600
    w2, b2, hull2 = _stood_off(1, taken=100)
    rec = P.record_of(b2)
    for _ in range(125):
        w2.run(60)
    assert _risings(hull2) == [] and rec.get("rising_judged", 0) > rec["taken_at"]


PUT_DOWN_SEED = 2  # the first seed from 1 whose rising is put down (seed 1's wins the deck)


# -- the far cut-out and the retaking ----------------------------------------------------------


@pytest.mark.slow
def test_the_cut_out_prize_parts_for_brest_under_her_prize_crew_and_a_cruiser_retakes_her():
    """The design's §2.9 and §2.8 (the brief's §20 first truth, amended): the merchant brig
    cut out by the privateer schooner at far detail is possessed on the records (a prize crew
    of six, her people the prisoners' count, bound for Brest under the prize master's role
    with the privateer's colours over hers) and, the privateer's doctrine parting from her,
    sails for Brest alone; a King's cutter cruising a mile from her comes up and she yields
    to him as the prize master's doctrine has her: retaken, her nation, colours, goal and
    role her own again, the privateer's story and the retaking's line saying so."""
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
    p = destination(far, 270.0, 1.2 * units.NAUTICAL_MILE)
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Vengeur",
    )
    pv.sailing_factor = 1.0
    for _ in range(150):
        w.run(60)
        if P.is_prize(prey):
            break
    rec = P.record_of(prey)
    assert rec and rec["how"] == "cut out" and rec["captor"] == pv.id
    assert rec["crew"] == P.PRIZE_CREW_LEAST and rec["prisoners"] == rec["men_at_start"] > 0
    assert rec["goal"] == "brest" and not rec.get("company") and rec["master"] == ""
    assert prey.nation == "france" and prey.role == P.PRIZE_MASTER_ROLE
    assert prey.intent_words == "carry the prize to Brest"
    assert prey.brain.doctrine.role == "prize-master"
    assert prey.signals.colours.over == "britain"
    cut = _events(w.log, "squadron.cut_out")
    assert len(cut) == 1 and "sent in under a prize crew" in cut[0].text
    for _ in range(60):
        w.run(60)
    assert _nm(pv, prey) > P.COVER_NM and prey.speed_kn > 3.0  # parted, under way for Brest
    q = destination(prey.position, 90.0, 1.0 * units.NAUTICAL_MILE)
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
    for _ in range(240):
        w.run(60)
        if P.record_of(prey).get("retaken"):
            break
    rec = P.record_of(prey)
    assert rec["retaken"][:2] == ("retaken", "Sprightly coming up")
    assert not P.is_prize(prey) and prey.nation == "britain" and prey.role == "merchant"
    assert prey.intent_words == "bound for the Start" and prey.brain.doctrine.role == "merchant"
    assert prey.signals.colours.state == "shown" and prey.signals.colours.over == ""
    assert not prey.struck and prey.brain.state != "struck"
    retaken = _events(w.log, "prize.retaken")
    assert len(retaken) == 1 and "retaken by Sprightly coming up" in retaken[0].text
    assert any("retaken (Sprightly coming up)" in words for _, words in prey.story)
    assert any("the Nancy retaken" in words for _, words in pv.story)
    assert cutter.brain.state in ("chasing", "cruising", "on passage", None)


# -- the save -------------------------------------------------------------------------------------


def test_a_checkpoint_taken_with_a_prize_in_company_comes_back_whole(tmp_path):
    """The prize's record, her prisoners, the prize crew and the prize master's seat in the
    checkpoint (the object graph pickled, `replay.write_checkpoint`), read back whole. The
    replay by the transcript and by the acts is the fight's passage (step 4: she strikes by
    the fight, a recorded road; the strike by the test's hand here is none)."""
    w, b, hull = _struck_brig()
    assert w.submit("take possession of her").kind == "prize.taken"
    assert w.submit("take six of the prisoners aboard").kind == "prize.prisoners_aboard"
    w.run(300)
    path = replay.write_checkpoint(w, tmp_path / "prize.ckpt")
    _, copy = replay.read_checkpoint(path)
    cb = copy.vessels.find("X")
    assert P.is_prize(cb) and P.record_of(cb) == P.record_of(b)
    ch = copy.hulls[b.id]
    assert P.prisoners_of(ch.ship).count == P.prisoners_of(hull.ship).count
    assert P.prisoners_of(copy.ship).count == 6
    assert len(ch.ship.extra["crew"].sailors) == P.record_of(b)["crew"]
    master = ch.stations.holder("captain")
    assert master is not None and master.name == P.record_of(b)["master"] and master.home == b.id
    assert copy.readings.words("prize") == w.readings.words("prize")
    assert cb.signals.colours.over == "france" and cb.nation == "britain"
