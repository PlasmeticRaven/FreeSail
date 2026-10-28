"""The world's business (spec M6 §19; package 43b): a scenario that says `business: on`
has its region peopled under the seed with traders carrying a cargo from a port where it
is cheap to one where it is dear, fishermen on the grounds the coast's features give and
the cruisers of the nations at war on their doctrine's stations, each with an intent and a
captain of her own; ships bound beyond the region leave it at the edge; the boat ashore
brings back the quay's rumours of prices. Off by default, and off for every recorded
passage, so that they are the ships they name and pin as before."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import business as B
from freesail.world import crews as CR
from freesail.world.brains import perceive_vessel
from freesail.world.geo import Position, bearing_and_distance
from freesail.world.scenarios import ScenarioError, load_scenario
from freesail.world.ships import vessel_from_spec

SCHOONER = "data/ships/topsail-schooner.yaml"
SCENARIOS = Path("data/scenarios")
# the free-play scenarios whose region the business peoples (package 43b): every other
# scenario, the recorded passages and the trials among them, says nothing and is off
# The free games with the business on: the four merchant ships', and the owner's two
# testing scenarios of 2026-10-17 (the smack out of Falmouth, the lugger out of Roscoff);
# never a recorded passage, whose pins stand on a sea with nobody else on it.
BUSY_SCENARIOS = {
    "merchant-brig.yaml",
    "merchant-cutter.yaml",
    "merchant-schooner-plymouth.yaml",
    "merchant-ship.yaml",
    "smack-falmouth.yaml",
    "lugger-roscoff.yaml",
    "dispatches-falmouth.yaml",  # the director's test of 2026-10-18, the business about her
}


def world_with(business=None, lat=50.0, lon=-5.0):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        business=business,
    )
    return make_world(7, SCHOONER, sc)


@pytest.fixture(scope="module")
def busy():
    return world_with("on")


def test_the_scenarios_word_is_on_off_or_a_density_and_anything_else_is_refused(tmp_path):
    assert B.business_density(None) == 0.0
    assert B.business_density("off") == 0.0
    assert B.business_density(False) == 0.0
    assert B.business_density("on") == 1.0
    assert B.business_density(True) == 1.0
    assert B.business_density("0.5") == 0.5
    with pytest.raises(ValueError, match="no density"):
        B.business_density("lots")
    with pytest.raises(ValueError, match="less than nothing"):
        B.business_density(-1)
    text = (SCENARIOS / "merchant-cutter.yaml").read_text(encoding="utf-8")
    text = re.sub(r"(?m)^business:.*\n", "", text)
    for said, kept in (("on", "on"), ("off", "off"), ("0.5", 0.5)):
        path = tmp_path / f"s-{said}.yaml"
        path.write_text(text + f"\nbusiness: {said}\n", encoding="utf-8")
        assert load_scenario(path).scenario.business == kept
    bad = tmp_path / "bad.yaml"
    bad.write_text(text + "\nbusiness: lots\n", encoding="utf-8")
    with pytest.raises(ScenarioError, match="no density"):
        load_scenario(bad)


def test_the_business_is_off_unless_said_and_every_recorded_passage_leaves_it_off():
    for path in sorted(SCENARIOS.glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        density = B.business_density(raw.get("business"))
        assert (density > 0.0) == (path.name in BUSY_SCENARIOS), path.name
    # a world told nothing has none, and its scenario's dict (its save) says nothing of it
    quiet = Scenario(start_time=datetime(1805, 6, 12, 10, 0))
    assert "business" not in quiet.to_dict()
    assert Scenario(start_time=datetime(1805, 6, 12, 10, 0), business="on").to_dict()[
        "business"
    ] == ("on")


def test_the_draw_peoples_the_region_with_trade_fishing_and_the_cruisers_at_war(busy):
    b = busy.business
    assert b is not None and b.region == "channel-west"
    kinds = {d.kind for d in b.drawn}
    # package 72: the convoys, the blockades and the ships in ordinary beside them
    assert kinds == {"trade", "fishing", "cruiser", "convoy", "escort", "blockade", "ordinary"}
    ids = {v.id for v in busy.vessels.vessels}
    for d in b.drawn:
        assert d.id in ids and d.intent and d.where
        v = busy.vessels.get(d.id)
        if d.kind in ("convoy", "ordinary"):
            # package 72: a convoy's merchantman keeps her station with no brain; a hull in
            # ordinary has none until commissioned
            assert v.brain is None
        else:
            assert v.brain is not None and v.brain.intent is not None
        assert b.inside(v.position)
    # nothing of the draw is a line of the player's log
    assert not [e for e in busy.log if "business" in e.kind]


def test_every_cargo_goes_from_where_it_is_cheap_to_where_it_is_dear_under_a_flag_both_take(busy):
    b = busy.business
    ports = {p.name: p for p in busy.ports.ports.values()}
    when = busy.clock.ship_time
    least = float(b.data["price_ratio_least"])
    traders = [d for d in b.drawn if d.kind == "trade"]
    assert traders
    for d in traders:
        assert re.match(r"\d+ tons of [a-z ]+", d.carries), d.carries
        m = re.match(r"trade (\d+) tons of (.+) from (.+) to (.+)$", d.intent)
        if m is None:
            continue  # bound in from the edge, or outward bound beyond the region
        good, a, z = m.group(2), ports[m.group(3)], ports[m.group(4)]
        pa = a.market.price(good, when, busy.nations, a.nation)
        pz = z.market.price(good, when, busy.nations, z.nation)
        assert pz / pa >= least, d.intent
        for port in (a, z):
            stance = busy.nations.stance(port.nation, d.nation, port.closed_to)
            assert stance in ("open", "neutral"), (d.intent, d.nation, port.id)


def test_the_cruisers_keep_the_stations_their_doctrine_names_for_nations_at_war(busy):
    raw = yaml.safe_load(Path("data/captains/cruiser.yaml").read_text(encoding="utf-8"))
    stations = raw["stations"]
    cruisers = [d for d in busy.business.drawn if d.kind == "cruiser"]
    assert {d.nation for d in cruisers} == {"britain", "france"}
    for d in cruisers:
        assert any(busy.nations.at_war(d.nation, o) for o in busy.nations.nations)
        m = re.match(r"keep the station off (.+) within ([\d.]+) miles", d.intent)
        assert m is not None
        named = [s for s in stations[d.nation] if busy.chart.find_feature(s["place"])]
        assert m.group(1) in {busy.chart.find_feature(s["place"]).name for s in named}
        v = busy.vessels.get(d.id)
        place = busy.chart.find_feature(m.group(1))
        apart = bearing_and_distance(v.position, place.position)[1] / units.NAUTICAL_MILE
        assert apart <= float(m.group(2)) + 1.0


def test_a_fisherman_works_her_ground_for_her_hours_and_runs_home_and_is_crewed_when_near(busy):
    fishermen = [d for d in busy.business.drawn if d.kind == "fishing"]
    assert fishermen
    grounds = {f.id for f, _home in busy.business.grounds()}
    for d in fishermen:
        v = busy.vessels.get(d.id)
        assert v.description in ("smack", "lugger")
        assert v.brain.role == "fisherman" and v.brain.intent.kind == "fish"
        assert v.brain.intent.destination in grounds
    # a trip of an hour on the Eddystone's ground from Plymouth, worked and done
    world = world_with(None, lat=50.17, lon=-4.40)
    world.vessels.serial += 1
    v = vessel_from_spec(
        world,
        {
            "description": "smack",
            "name": "Brothers",
            "nation": "britain",
            "position": {"lat_deg": 50.18, "lon_deg": -4.45},
            "goal": "bound for Plymouth",
            "intent": "fish on the oozy ground off the Eddystone for 1 hours from Plymouth",
        },
        world.vessels.serial,
    )
    world.vessels.add(v)
    brain = v.brain
    assert brain.role == "fisherman" and brain.intent.hours == 1.0
    # within the crewed range of the player, and promoted like any other ship since
    # package 56 (spec M7b §21a: 43b's "never crewed" lifted, the cap's order unchanged)
    world.run(120)
    assert brain.state == "keeping station"
    assert v.crew is not None and v.crew.shape == "full"
    assert v.crew.captain.role == "fisherman" and v.crew.captain.state == "keeping station"
    assert CR.FAR_ONLY_ROLES == frozenset()
    p = perceive_vessel(world, v, brain)
    brain._business["fishing_s"] = 3600.0 - 60.0
    brain._business["fishing_tick"] = p.tick - 60
    brain._fishing(p)
    assert brain.intent.kind == "home" and brain.intent.destination == "plymouth"
    assert brain.state == "on passage" and brain.role == "fisherman"


def test_the_draw_is_the_seeds_and_moves_no_other_draw(busy):
    again = world_with("on")
    assert [d.to_dict() for d in again.business.drawn] == [d.to_dict() for d in busy.business.drawn]
    # the world's other streams are as a world without the business draws them
    quiet = world_with(None)
    assert quiet.rng.stream("weather").random() == again.rng.stream("weather").random()


def test_a_ship_bound_beyond_the_region_leaves_it_at_the_edge_and_the_draw_is_hourly(
    busy, monkeypatch
):
    b = busy.business
    s, n, w, e = b.bounds
    d = next(d for d in b.drawn if d.kind == "trade" and not d.ended)
    v = busy.vessels.get(d.id)
    keep = (v.position, list(v.plan), v.done)
    beyond = Position(48.5, w - 0.2)
    try:
        v.position = Position(48.5, w - 0.05)
        v.plan = [("to", beyond, "beyond")]
        b.tick()
        assert v.done and d.ended == "left at the edge" and d.ended_tick == busy.clock.tick
    finally:
        v.position, v.plan, v.done = keep
        d.ended, d.ended_tick = "", None
    # the draw once an hour, up to the most the region holds
    data = dict(b.data)
    data["arrivals_per_hour"] = {"trader": 1.0, "fisherman": 1.0}
    monkeypatch.setattr(B.Business, "data", property(lambda self: data))
    before = len(b.drawn)
    b.last_draw = busy.clock.tick - B.DRAW_EVERY_S + 60
    b.tick()
    assert len(b.drawn) == before  # not yet the hour
    b.last_draw = busy.clock.tick - B.DRAW_EVERY_S
    b.tick()
    assert len(b.drawn) > before
    assert {x.kind for x in b.drawn[before:]} <= {"trade", "fishing"}
    data["most_ships"] = 0
    full = len(b.drawn)
    b.last_draw = busy.clock.tick - B.DRAW_EVERY_S
    b.tick()
    assert len(b.drawn) == full


def test_the_quays_rumours_are_true_as_of_the_day_and_said_as_rumour(busy):
    b = busy.business
    port = busy.ports.ports["falmouth"]
    said = b.rumour(port)
    assert said.startswith("The talk on the quay, as the boat's crew heard it: ")
    assert said.endswith(". Rumour, no more.")
    body = said.removeprefix("The talk on the quay, as the boat's crew heard it: ")
    body = body.removesuffix(". Rumour, no more.")
    items = re.split(r", | and (?=[a-z]+ (?:dear|cheap) at )", body)
    assert 2 <= len(items) <= 3
    names = {p.name: p for p in busy.ports.ports.values()}
    when = busy.clock.ship_time
    ratio = float(b.data["rumours"]["ratio"])
    for item in items:
        m = re.match(r"(.+) (dear|cheap) at (.+)$", item)
        assert m is not None, item
        good, how, there = m.group(1), m.group(2), names[m.group(3)]
        here_p = port.market.price(good, when, busy.nations, port.nation)
        there_p = there.market.price(good, when, busy.nations, there.nation)
        if how == "dear":
            assert there_p / here_p >= ratio
        else:
            assert here_p / there_p >= ratio


def test_the_boat_ashore_brings_the_rumours_off_only_where_the_business_is_on():
    """The owner's note 24: the boat sent for the prices brings back the quay's talk of
    prices high or low elsewhere, a routine line after the list; none without the
    business, so that the recorded passages' boats bring what they brought."""
    carrick = {"lat_deg": 50.160, "lon_deg": -5.034}
    seen = {}
    for business in (None, "on"):
        sc = Scenario(
            start_time=datetime(1805, 6, 10, 10, 0),
            wind_from_deg=225.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=250.0,
            position=carrick,
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            business=business,
        )
        w = make_world(7, SCHOONER, sc)
        w.run(60)
        w.submit("let go the best bower")
        w.run(300)
        assert w.at_anchor
        assert w.submit("send the boat ashore").kind == "order.accepted"
        for _ in range(180):
            w.run(60)
            if any(e.kind == "market.prices" for e in w.log):
                break
        assert [e for e in w.log if e.kind == "market.prices"]
        seen[business] = [e for e in w.log if e.kind == "port.rumour"]
    assert seen[None] == []
    (line,) = seen["on"]
    assert line.text.endswith("Rumour, no more.") and line.severity.name == "ROUTINE"


# ---------------------------------------------------------------------------
# Package 53b: transactions, not variables (spec M7b §17a)
# ---------------------------------------------------------------------------


def test_a_sum_paid_in_or_out_is_a_transaction_with_its_cause_and_never_below_nothing():
    """`aboard: twenty guineas paid into the purse by Mr Veale` credits the purse with the
    ledger's line and its cause, a notable line of the purser's books in the play log; a
    sum paid out is the same, refused below nothing; a debt is entered and moves no money.
    Nothing of the channel sets the purse: each line is a sum with its payer or payee."""
    from freesail.core.events import for_the_record
    from freesail.world.orders import read_sum
    from tests.test_orders_places import in_falmouth

    assert [read_sum(x) for x in ("twenty guineas", "£30", "£6 10s", "a guinea")] == [
        21.0,
        30.0,
        6.5,
        1.05,
    ]
    assert read_sum("thirty pounds ten shillings") == 30.5 and read_sum("a packet") is None
    w = in_falmouth()
    w.world_order('person: make "Mr Veale", a clerk, ashore at Falmouth', "the test")
    was = w.purse.pounds
    assert "ledger" not in w.readings.value("purse")
    e = w.world_order("aboard: twenty guineas paid into the purse by Mr Veale", "the test")
    assert e.data["result"] == "done" and w.purse.pounds == pytest.approx(was + 21.0)
    paid = [x for x in w.log.all() if x.kind == "purse.received"]
    assert len(paid) == 1 and not for_the_record(paid[0]) and paid[0].severity.value == "notable"
    assert paid[0].text == (
        f"Paid into the purse by Mr Veale, twenty guineas (£21); the purse {w.purse.words()}."
    )
    assert w.purse.entries[-1] == (w.clock.tick, 21.0, "paid by Mr Veale, twenty guineas (£21)")
    assert w.readings.value("purse")["ledger"] == [
        f"Paid by Mr Veale, twenty guineas (£21); the purse {w.purse.words()}."
    ]
    e = w.world_order("aboard: £6 paid from the purse to Mr Veale for his trouble", "the test")
    assert e.data["result"] == "done" and w.purse.pounds == pytest.approx(was + 15.0)
    left = w.purse.pounds
    e = w.world_order(f"aboard: £{left + 1:.0f} paid from the purse to Mr Veale", "the test")
    assert e.data["result"] == "refused" and "nothing is paid below nothing" in e.text
    assert w.purse.pounds == left
    e = w.world_order("aboard: a debt of £30 owed to the chandler at Plymouth", "the test")
    assert e.data["result"] == "done" and w.purse.pounds == left
    assert w.readings.value("purse")["debts"] == "owed to the chandler at Plymouth, £30"
    e = w.world_order("aboard: a sum paid into the purse by Mr Veale", "the test")
    assert e.data["result"] == "refused" and "no sum the purse reads" in e.text


def test_a_cargo_freighted_comes_off_by_the_lighter_at_no_price_with_its_cause_in_the_manifest():
    """`aboard: ten tons of wool freighted by Mr Veale at the quay for Plymouth`: the
    market's own form at no price, the freight in the hold's ledger and the manifest with
    its cause, the goods off by the port's lighter; refused in words where the hold has no
    room, the hold's tons being the game's."""
    from tests.test_orders_places import in_falmouth

    w = in_falmouth()
    w.world_order('person: make "Mr Veale", a clerk, ashore at Falmouth', "the test")
    purse = w.purse.pounds
    e = w.world_order(
        "aboard: ten tons of wool freighted by Mr Veale at the quay for Plymouth", "the test"
    )
    assert e.data["result"] == "done" and w.purse.pounds == purse
    assert w.hold.goods.get("wool") is None  # not yet: the lighter brings it off
    assert w.hold.lines()[-1] == "10 tons of wool freighted by Mr Veale at Falmouth for Plymouth."
    for _ in range(180):
        if w.hold.goods.get("wool"):
            break
        w.run(60)
    assert w.hold.goods["wool"] == 10.0
    came = [x for x in w.log.all() if x.kind == "market.bought" and x.data.get("good") == "wool"]
    assert came and came[0].text.startswith("10 tons of wool came off by the lighter from Falmouth")
    room = w.hold.room_tons
    e = w.world_order(
        f"aboard: {room + 5:.0f} tons of tin freighted by Mr Veale at the quay", "the test"
    )
    assert e.data["result"] == "refused" and "will not stow" in e.text
    # the room is the room left after what is bought and coming off (found on the way in
    # the dispatches: the master's cargo in the boat, the freight engaged beside it)
    w.submit("send the boat ashore")
    for _ in range(120):
        if not w.dealings.boat.away:
            break
        w.run(60)
    w.submit(f"buy {w.hold.room_tons - 2:.0f} tons of copper ore")
    assert w.dealings.boat.away
    e = w.world_order("aboard: five tons of wool freighted by Mr Veale at the quay", "the test")
    assert e.data["result"] == "refused" and "tons bought are coming off" in e.text


def test_the_channel_doubts_money_from_nobody_a_far_payer_and_a_sum_beyond_the_ports_means():
    """The doubt of a transaction (decision 50): money from nobody, from a person the world
    does not know, from a payer neither aboard nor at a port she lies within a boat's reach
    of, a sum beyond a port's means by the business's figures (a full lading of its dearest
    good), a freight to a ship at sea; a debt is never doubted. A held person's money is
    his holder's own word, refused by the rule of reach."""
    from freesail.world import orders as WO
    from tests.test_orders_places import in_falmouth

    w = in_falmouth()
    w.world_order('person: make "Mr Veale", a clerk, ashore at Falmouth', "the test")
    w.world_order('person: make "Mr Gill", a merchant, ashore at Brest', "the test")
    falmouth = w.dealings.ports["falmouth"]
    means = B.port_means_pounds(w, falmouth)
    assert means == pytest.approx(
        max(
            falmouth.market.price(g, w.clock.ship_time, w.nations, falmouth.nation)
            for g in falmouth.market.goods
        )
        * B.load_business()["cargo_tons"][-1]
    )

    def doubt(text):
        return WO.doubt(w, WO.parse(text))

    assert doubt("aboard: twenty guineas paid into the purse by Mr Veale") is None
    assert "from nobody" in doubt("aboard: twenty guineas paid into the purse")
    assert "nobody answering to 'the owners'" in doubt(
        "aboard: £100 paid into the purse by the owners"
    )
    assert "neither aboard nor at a port" in doubt("aboard: £5 paid into the purse by Mr Gill")
    assert "beyond Falmouth's means" in doubt(
        f"aboard: £{means + 100:.0f} paid into the purse by Mr Veale"
    )
    assert doubt("aboard: a debt of £30 owed to the chandler at Plymouth") is None
    assert "neither aboard nor at a port" in doubt("aboard: ten tons of wool freighted by Mr Gill")
    at_sea = world_with()
    at_sea.world_order('person: make "Mr Veale", a clerk, aboard in the cabin', "the test")
    assert WO.doubt(at_sea, WO.parse("aboard: £5 paid into the purse by Mr Veale")) is None
    # a freighter aboard a ship at sea: no lighter, his goods struck down at once
    assert WO.doubt(at_sea, WO.parse("aboard: ten tons of wool freighted by Mr Veale")) is None
    at_sea.world_order("aboard: ten tons of wool freighted by Mr Veale", "the test")
    assert at_sea.hold.goods["wool"] == 10.0
    # the captain is held by the player at the prompt: his money is his own word
    e = w.world_order(f"aboard: £5 paid into the purse by {w.people.captain.name}", "the test")
    assert e.data["result"] == "refused" and "nobody gives it for him" in e.text
