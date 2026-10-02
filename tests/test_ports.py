"""The ports (spec M5 §23; package 35): Falmouth, Plymouth and Brest as files on one
machinery; the pilot coming off in his cutter, boarding and leaving; the anchorage, the
moor and the kedge; the boat's errands; the market and its rules table; the yard and the
crew pool; the stance of a port to a ship by the nations table. Everything inward is
reached by an order or a reading, everything outward comes through something the ship
models."""

from __future__ import annotations

import math
import shutil
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.ship.parts import booms
from freesail.world import ports as PT

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}
SOUTH_OF_FALMOUTH = {"lat_deg": 50.05, "lon_deg": -5.03}  # five miles south of the outer road
FALMOUTH_OUTER = {"lat_deg": 50.133, "lon_deg": -5.035}
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}
THE_RADE_INNER = {"lat_deg": 48.345, "lon_deg": -4.470}  # the Bay of Brest, within the Goulet
THE_SOUND = {"lat_deg": 50.345, "lon_deg": -4.150}  # Plymouth Sound, within the anchorage
START = datetime(1805, 6, 10, 10, 0)


def world_at(where, ship=FRIGATE, heading=20.0, speed=0.0, start=START, **kw):
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
        position=where,
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def at_anchor_in(where, ship=FRIGATE, heading=200.0, **kw):
    w = world_at(where, ship=ship, heading=heading, **kw)
    w.run(60)
    w.submit("let go the best bower")
    w.run(300)
    assert w.at_anchor
    return w


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


def run_until(world, kind, minutes=240):
    for _ in range(minutes):
        world.run(60)
        if events(world, kind):
            return events(world, kind)[-1]
    raise AssertionError(f"no {kind} in {minutes} minutes")


# ---------------------------------------------------------------------------
# The port as data
# ---------------------------------------------------------------------------


def test_the_three_ports_are_files_on_one_machinery_placed_from_the_chart():
    files = PT.port_files()
    assert list(files) == ["brest", "falmouth", "plymouth"]
    w = world_at(OFF_THE_LIZARD)
    assert list(w.ports.ports) == ["brest", "falmouth", "plymouth"]
    falmouth = w.ports.ports["falmouth"]
    assert falmouth.nation == "britain" and "White 1835" in falmouth.source
    # the roads and the anchorage are the chart's features, not figures of their own
    outer = w.chart.feature("falmouth-outer-road")
    assert falmouth.outer_road.feature_id == "falmouth-outer-road"
    assert falmouth.outer_road.position.lat_deg == pytest.approx(outer.position.lat_deg)
    assert falmouth.anchorage.feature_id == "carrick-road" and falmouth.anchorage.depth_m
    assert falmouth.anchorage.depth_words.endswith("fathoms")
    # the mooring is the port's own figure where the chart has no feature, with the
    # draught that sends a ship to the anchorage instead (White p. 26)
    assert falmouth.mooring.feature_id == "" and falmouth.mooring.deep_draught_ft == 15
    assert falmouth.mooring_for(units.feet_to_m(16.0)) is falmouth.anchorage
    assert falmouth.mooring_for(units.feet_to_m(9.0)) is falmouth.mooring
    assert falmouth.shore.name == "the quay at Falmouth"
    for port in w.ports.ports.values():
        assert port.pilot.names and 0.0 < port.pilot.skill <= 1.0 and port.pilot.fee_pounds > 0
        assert port.pilot.cast in ("starboard", "larboard")
        assert set(port.pilot.words) >= {"channel", "marks", "anchorage", "tide"}
        assert port.tide["enter_on"] == "flood" and port.tide["leave_on"] == "ebb"
        assert len(port.market.goods) >= 10 and port.market.currency == "pounds"
        assert port.dockyard.kind in ("yard", "chandlers") and "topmast" in port.dockyard.items
        assert set(port.crew_pool) == {"able", "ordinary", "landsman"}
        for good in port.market.goods.values():
            assert good.price > 0 and all(isinstance(m, int) for m in good.season)
    assert w.ports.ports["plymouth"].dockyard.kind == "yard"
    assert w.ports.ports["plymouth"].mooring.feature_id == "the-hamoaze"
    assert w.ports.ports["brest"].nation == "france"
    # the summary names the port she lies nearest
    assert any(ln.startswith("Port: ") for ln in w.summary_lines())


def test_a_fourth_port_costs_a_file_and_nothing_else(tmp_path):
    """A port is a file of data/ports/ and the scenario's `ports:` list; a name without a
    file is refused naming the ones there are."""
    files = PT.port_files()
    fourth = tmp_path / "ports"
    fourth.mkdir()
    for p in files.values():
        shutil.copy(p, fourth / p.name)
    text = (fourth / "falmouth.yaml").read_text(encoding="utf-8")
    text = text.replace("id: falmouth\n", "id: penzance\n").replace(
        "name: Falmouth\n", "name: Penzance\n"
    )
    text = text.replace("  feature: falmouth-outer-road\n", "  feature: st-michaels-mount\n", 1)
    (fourth / "penzance.yaml").write_text(text, encoding="utf-8")
    assert list(PT.port_files(fourth)) == ["brest", "falmouth", "penzance", "plymouth"]
    w = world_at(OFF_THE_LIZARD)
    port = PT.load_port(fourth / "penzance.yaml", w.chart)
    assert port.id == "penzance" and port.name == "Penzance"
    assert port.outer_road.feature_id == "st-michaels-mount"
    assert port.outer_road.position.lon_deg == pytest.approx(
        w.chart.feature("st-michaels-mount").position.lon_deg
    )
    assert port.market.goods["tin"].price == 120 and port.pilot.cruising_nm == 6
    # the scenario picks the ports by name, and a name without a file is refused
    only = world_at(OFF_THE_LIZARD, ports=["falmouth"])
    assert list(only.ports.ports) == ["falmouth"]
    with pytest.raises(ValueError, match="no port file for 'penzance'"):
        world_at(OFF_THE_LIZARD, ports=["penzance"])
    # a world without a chart has no ports and the orders say so
    from freesail.core.world import World

    bare = World(seed=1)
    assert bare.ports.ports == {}
    assert bare.submit("send the boat ashore").kind == "order.rejected"
    assert bare.ports.port_words() is None and bare.ports.nearest() is None


# ---------------------------------------------------------------------------
# The market's rules table
# ---------------------------------------------------------------------------


class _Nations:
    def __init__(self, wars):
        self.wars = {frozenset(w) for w in wars}

    def at_war(self, a, b):
        return frozenset((a, b)) in self.wars


def test_the_market_moves_a_price_by_the_season_the_war_and_the_supply_and_no_more():
    good = PT.Good("pilchards", 14.0, "britain", {3: 1.3, 9: 0.8})
    market = PT.Market("pounds", {"pilchards": good, "hemp": PT.Good("hemp", 70.0, None, {})})
    peace, war = _Nations([]), _Nations([("britain", "france")])
    june, march = datetime(1805, 6, 1), datetime(1805, 3, 1)
    assert market.factors(good, june, peace, "britain") == {
        "season": 1.0,
        "war": 1.0,
        "supply": 1.0,
    }
    assert market.factors(good, march, peace, "britain")["season"] == 1.3
    assert market.price("pilchards", march, peace, "britain") == 18.0  # 18.2 to the half pound
    # the war rule: the good's origin at war with the port's nation, by the table given
    assert market.factors(good, june, war, "france")["war"] == PT.WAR_FACTOR
    assert market.factors(good, june, war, "britain")["war"] == 1.0  # her own goods at home
    assert market.factors(market.goods["hemp"], june, war, "france")["war"] == 1.0  # no origin
    assert market.price("pilchards", june, war, "france") == 21.0
    # the supply: a ton sold to the port takes a hundredth off, floored and capped
    market.sold_to_port("pilchards", 40.0)
    assert market.factors(good, june, peace, "britain")["supply"] == pytest.approx(0.6)
    market.sold_to_port("pilchards", 100.0)
    assert market.factors(good, june, peace, "britain")["supply"] == PT.SUPPLY_FLOOR
    market.net_sold["pilchards"] = -200.0  # bought from the port: scarce
    assert market.factors(good, june, peace, "britain")["supply"] == PT.SUPPLY_CAP
    # the glut clears by a seventh a day, whole days only, and the small rest is forgotten
    market.net_sold["pilchards"] = 70.0
    market.recover(86400 - 1)
    assert market.net_sold["pilchards"] == 70.0
    market.recover(86400)
    assert market.net_sold["pilchards"] == pytest.approx(60.0)
    market.recover(86400 * 8)
    assert market.net_sold["pilchards"] == pytest.approx(70.0 * (6.0 / 7.0) ** 8)
    market.net_sold["pilchards"] = 0.005
    market.recover(86400 * 9)
    assert "pilchards" not in market.net_sold
    # a price never rounds to nothing
    assert (
        PT.Market("pounds", {"dust": PT.Good("dust", 0.1, None, {})}).price(
            "dust", june, peace, "britain"
        )
        == PT.PRICE_ROUND
    )
    assert market.find("pilchard") is good and market.find("Hemp") is not None
    assert market.find("tea") is None


# ---------------------------------------------------------------------------
# The stance
# ---------------------------------------------------------------------------


def test_the_ships_nation_is_her_companys_names_or_the_scenarios_word_and_the_stance_the_tables():
    frigate = world_at(OFF_THE_LIZARD)
    assert frigate.ports.ship_nation == "britain"
    assert {p.id: frigate.ports.stance(p) for p in frigate.ports.ports.values()} == {
        "falmouth": "open",
        "plymouth": "open",
        "brest": "hostile",
    }
    schooner = world_at(OFF_THE_LIZARD, ship=SCHOONER)
    assert schooner.ports.ship_nation == "united-states"
    assert {p.id: schooner.ports.stance(p) for p in schooner.ports.ports.values()} == {
        "falmouth": "neutral",
        "plymouth": "neutral",
        "brest": "neutral",
    }
    french = world_at(OFF_THE_LIZARD, ship=SCHOONER, nation="france")
    assert french.ports.ship_nation == "france"
    assert french.ports.stance(french.ports.ports["brest"]) == "open"
    assert french.ports.stance(french.ports.ports["falmouth"]) == "hostile"
    closed = world_at(
        OFF_THE_LIZARD, ship=SCHOONER, ports={"falmouth": {"closed_to": ["united-states"]}}
    )
    assert closed.ports.stance(closed.ports.ports["falmouth"]) == "closed"
    # the reading at sea: the nearest port and its stance, no pilot within reach
    said = frigate.readings.words("port")
    assert said.startswith("no port within the pilot's cruising ground; the nearest is Falmouth")
    assert frigate.readings["port"]["stance"] == "open"
    e = frigate.submit("the pilot")
    assert e.kind == "query.reading" and "no pilot aboard" in e.text


# ---------------------------------------------------------------------------
# The pilot
# ---------------------------------------------------------------------------


def test_the_pilot_comes_off_in_his_cutter_hails_boards_and_is_a_person_aboard():
    """The frigate standing in for Falmouth from five miles south under plain sail: the
    cutter is a sail the lookout hails, then the hail, then the pilot aboard from the
    cutter within two cables at six knots or under; he is a person with a name from the
    port's list, the readings have him, and he answers from his port's words."""
    w = world_at(SOUTH_OF_FALMOUTH, heading=0.0, speed=4.0)
    w.submit("set plain sail")
    aboard = run_until(w, "port.pilot_aboard", 150)
    sails = [e for e in events(w, "lookout.sighting") if e.data.get("seen_as") == "sail"]
    hail = events(w, "port.pilot_hail")[0]
    assert sails and sails[0].text.startswith("Sail ho!")
    assert sails[0].tick < hail.tick < aboard.tick
    assert (
        hail.text
        == "The cutter hailed: a pilot for Falmouth; shorten sail and he will come aboard."
    )
    assert hail.tick - sails[0].tick >= 60 and (aboard.tick - hail.tick) % 60 == 0
    pilot = w.ports.pilot
    assert pilot is not None and pilot.role == "pilot" and pilot.port == "falmouth"
    surname = pilot.name.removeprefix("Mr ")
    assert surname in w.ports.ports["falmouth"].pilot.names
    assert aboard.text.startswith(
        f"The pilot, {pilot.name} of Falmouth, came aboard from the cutter"
    )
    assert aboard.data["pilot"]["name"] == pilot.name
    # he is one of the people, and the readings have him
    assert w.people.find("the pilot") is pilot
    assert f"{pilot.name}: on the quarterdeck" in w.readings.words(
        "people"
    ) or "pilot" in w.readings.words("people")
    e = w.submit("where is the pilot")
    assert e.kind == "query.reading" and pilot.name in e.text
    said = w.readings.words("pilot")
    assert said.startswith(f"{pilot.name} of Falmouth aboard; ")
    assert "high water" in said.lower()
    assert (
        w.readings["pilot"]["cast"] == "starboard" and w.readings["pilot"]["course_out_deg"] == 169
    )
    assert w.readings["port"]["pilot"]["name"] == pilot.name
    # his words are the port file's, by the question
    e = w.submit("ask the pilot about the channel")
    assert e.kind == "pilot.answered" and "Keep the fair way and the lead going" in e.text
    assert "Killiganoon" in w.submit("ask the pilot for the marks").text
    assert "Carrick Road" in w.submit("ask the pilot about the anchorage").text
    tide = w.submit("ask the pilot when the tide serves").text
    assert "flood" in tide and "high water" in tide.lower()
    assert "at war with" in w.submit("ask the pilot for the news").text
    # the news came with him, once, as a line
    assert (
        len(events(w, "port.news")) == 1 and "Britain at war with" in events(w, "port.news")[0].text
    )
    assert len(events(w, "port.pilot_words")) == 1
    # the cutter lies to a while and goes home once he is aboard; nothing was refused
    cutter = w.ports._cutter()
    assert cutter is not None and not cutter.alongside and cutter.plan[0][0] == "lie_to"
    w.run(2 * 3600)
    assert w.ports._cutter() is None and not w.vessels.vessels
    assert not events(w, "port.pilot_refused")


def test_no_pilot_comes_off_by_night_to_a_ship_at_anchor_or_to_one_without_way():
    night = world_at(SOUTH_OF_FALMOUTH, heading=0.0, speed=4.0, start=datetime(1805, 6, 10, 1, 0))
    night.submit("set plain sail")
    night.run(1800)
    assert not night.vessels.vessels and not events(night, "port.pilot_hail")
    still = world_at(FALMOUTH_OUTER, heading=0.0, speed=0.0)
    still.run(1800)  # no way on her: nothing comes off
    assert not still.vessels.vessels
    riding = at_anchor_in(FALMOUTH_OUTER)
    riding.run(1800)
    assert not riding.vessels.vessels and riding.ports.pilot is None
    assert riding.ports.in_port() is riding.ports.ports["falmouth"]
    assert riding.readings.words("port").startswith("at anchor in Falmouth, the outer road")


def test_the_pilot_leaves_outward_bound_in_the_cutter_and_takes_his_fee_from_the_purse():
    """From the outer road with the pilot aboard, `get under way`: he gives her the cast
    and the course out; standing out beyond the road and a mile, the cutter comes off
    for him, he leaves her, and the pilotage is paid from the purse and written in it."""
    from freesail.world.people import Person

    w = at_anchor_in(FALMOUTH_OUTER, cargo={"purse_pounds": 100.0})
    pilot = w.people.add(Person("pilot-falmouth-1", "Mr Pascoe", "pilot", 0.9, port="falmouth"))
    w.ports.pilot, w.ports.pilot_port, w.ports.pilot_since = pilot, "falmouth", w.clock.tick
    e = w.submit("get under way")
    assert e.kind == "order.accepted"
    under_way = run_until(w, "ship.under_way", 90)
    assert under_way.data["tack"] == "starboard"  # the port's cast
    # the pilot's course out is S by E; with the wind at SW it lies too near the wind to
    # be laid, and she is kept full and by, the log saying why
    assert under_way.text.endswith(
        "full and by (S by E (169°) lying too near the wind to be laid)."
    )
    assert under_way.data["course_deg"] is None and not under_way.data["pilot_course"]
    left = run_until(w, "port.pilot_left", 150)
    hail = [e for e in events(w, "port.pilot_hail") if "come off for the pilot" in e.text]
    assert hail and hail[0].tick < left.tick
    assert left.text.startswith("Mr Pascoe left her in the cutter")
    assert "the pilotage, £5, paid and his certificate signed" in left.text
    assert w.purse.pounds == 95.0 and w.purse.entries[-1][1:] == (
        -5.0,
        "pilotage, Falmouth",
    )
    assert w.ports.pilot is None and w.people.find("the pilot") is None
    assert w.readings.words("pilot").startswith(
        "no pilot aboard"
    ) or "no pilot" in w.readings.words("pilot")


# ---------------------------------------------------------------------------
# Getting under way, mooring, the kedge
# ---------------------------------------------------------------------------


def test_weigh_alone_is_the_anchor_up_and_no_sail_and_get_under_way_is_luces_whole_sequence():
    """The owner's ruling (2026-10-02): `weigh` is heave short, break out, cat and fish and
    nothing more; `get under way` is Luce's ch. XXI whole: heave short, loose the
    topsails, weigh, cast on the tack wanted, fill and set the jib and the spanker."""
    plain = at_anchor_in(FALMOUTH_OUTER)
    plain.submit("weigh")
    run_until(plain, "ship.aweigh", 40)
    plain.run(600)
    assert not plain.at_anchor and not [s.id for s in plain.ship.sails.values() if s.is_set]
    assert not events(plain, "ship.under_way")
    luce = at_anchor_in(FALMOUTH_OUTER)
    e = luce.submit("get under way on the larboard tack and steer SW by S")
    assert e.kind == "order.accepted"
    luce.run(1)
    started = events(luce, "evolution.started")[-1]
    assert started.text.startswith("All hands up anchor! Pass the messenger, ship the bars")
    assert events(luce, "crew.all_hands")[-1].text == "All hands! (to get under way)"
    done = run_until(luce, "ship.under_way", 90)
    steps = [x.text for x in luce.log if x.kind == "evolution.step"]
    assert any("Heave round" in s or "heave" in s.lower() for s in steps)
    assert any("Let fall" in s or "sheet home" in s.lower() for s in steps)
    assert events(luce, "ship.aweigh") and events(luce, "ship.aweigh")[0].tick < done.tick
    assert done.text.startswith("Under way on the larboard tack, under topsails and the jib")
    assert "catted and fished" in done.text
    assert done.data["tack"] == "larboard"
    set_now = {s.id for s in luce.ship.sails.values() if s.is_set}
    assert {"fore.topsail", "main.topsail", "mizzen.topsail", "jib"} <= set_now
    assert "fore.course" not in set_now
    luce.run(600)
    assert units.ms_to_knots(luce.ship.dyn.speed) > 2.0
    assert luce.readings.value("anchor")["state"] in ("catted", "at the bows", "stowed", "ready")
    # the refusals in words
    e = luce.submit("get under way")
    assert e.kind == "order.rejected" and "no anchor is down" in e.text
    e = at_anchor_in(FALMOUTH_OUTER).submit("get under way on the moon")
    assert e.kind == "order.rejected" and "was not understood after 'get under way'" in e.text
    # the aliases: 'weigh and make sail' is the whole, 'up anchor' the anchor alone
    whole = at_anchor_in(FALMOUTH_OUTER)
    assert whole.submit("weigh and make sail").kind == "order.accepted"
    whole.run(1)
    assert events(whole, "evolution.started")[-1].text.startswith(
        "All hands up anchor! Pass the messenger"
    )
    alone = at_anchor_in(FALMOUTH_OUTER)
    assert alone.submit("up anchor").kind == "order.accepted"
    alone.run(1)
    assert not events(alone, "evolution.started")[-1].text.startswith(
        "All hands up anchor! Pass the messenger"
    )


def test_moor_lays_a_second_anchor_with_the_hawse_open_and_unmoor_brings_her_to_single_anchor():
    w = at_anchor_in(THE_RADE_INNER, heading=250.0)
    first = w.readings.value("anchor")
    assert first["name"] == "the best bower"
    e = w.submit("moor")
    assert e.kind == "order.accepted"
    w.run(1)
    assert events(w, "evolution.started")[-1].text.startswith(
        "Moor ship! Veer away on the best bower cable; clear away the small bower."
    )
    moored = run_until(w, "ship.moored", 60)
    assert moored.text.startswith("Moored with the best bower to the ")
    assert "the small bower to the" in moored.text and "the hawse open to the" in moored.text
    tackle = w.readings.value("ground_tackle")
    down = [a for a in tackle["anchors"] if a["state"] == "down"]
    assert {a["name"] for a in down} == {"the best bower", "the small bower"}
    for a in down:
        assert a["scope_fathoms"] == pytest.approx(down[0]["scope_fathoms"], rel=0.2)
    assert len(events(w, "ship.anchored")) == 2  # the second let go is a line of its own
    assert w.readings.words("anchor").startswith("moored with two anchors; down, riding by")
    assert w.readings["anchor"]["moored"] is True
    # moored, she will not get under way nor moor again
    e = w.submit("get under way")
    assert e.kind == "order.rejected" and "unmoor first" in e.text
    e = w.submit("moor")
    assert e.kind == "order.rejected" and "moored already" in e.text
    w.run(3600)
    assert w.at_anchor and not events(w, "anchor.dragging")
    e = w.submit("unmoor")
    assert e.kind == "order.accepted"
    w.run(1)
    assert events(w, "evolution.started")[-1].text.startswith("Unmoor ship! Bring to on the ")
    unmoored = run_until(w, "ship.unmoored", 60)
    assert (
        unmoored.text.startswith("Unmoored: the ") and "riding at single anchor by" in unmoored.text
    )
    down = [a for a in w.readings.value("ground_tackle")["anchors"] if a["state"] == "down"]
    assert len(down) == 1 and w.at_anchor and w.readings["anchor"]["moored"] is False
    e = w.submit("unmoor")
    assert e.kind == "order.rejected"
    # at sea, in words
    e = world_at(OFF_THE_LIZARD).submit("moor")
    assert e.kind == "order.rejected" and "come to an anchor first" in e.text


def test_a_kedge_is_laid_out_by_the_boat_to_the_bearing_given():
    w = at_anchor_in(CARRICK_ROAD)
    e = w.submit("lay out a kedge to the NE")
    assert e.kind == "order.accepted"
    w.run(1)
    assert events(w, "evolution.started")[-1].text == (
        "Hoist out the launch; the kedge and a hawser into her."
    )
    assert w.readings["boat"]["away"] and "kedge" in w.readings.words("boat")
    e2 = w.submit("send the boat ashore")
    assert e2.kind == "order.rejected" and "away" in e2.text
    kedged = run_until(w, "ship.kedged", 60)
    assert (
        kedged.text.startswith("The kedge laid out ") and "to the NE by the launch" in kedged.text
    )
    kedge = next(
        a for a in w.readings.value("ground_tackle")["anchors"] if a["name"] == "the kedge"
    )
    assert kedge["state"] == "down"
    assert not w.readings["boat"]["away"]
    # the kedge lies to the north-east of her
    tackle = w.ship.extra["ground_tackle"]
    anchor = next(a for a in tackle.anchors if a.kind == "kedge")
    dx, dy = anchor.ground_x - w.ship.dyn.x, anchor.ground_y - w.ship.dyn.y
    bearing = math.degrees(math.atan2(dx, dy)) % 360.0
    assert 20.0 < bearing < 70.0, bearing
    assert "fathoms" in kedged.text
    # the time is the boat's: hoist out, sling, pull out at four knots, back, hoist in
    assert kedged.tick - e.tick >= 900
    e = w.submit("lay out a kedge")
    assert e.kind == "order.rejected" and "the kedge is down" in e.text


# ---------------------------------------------------------------------------
# The boat, the market, the yard and the crew pool
# ---------------------------------------------------------------------------


def test_the_boats_errand_ashore_brings_the_prices_off_and_the_orders_refuse_in_words_otherwise():
    at_sea = world_at(OFF_THE_LIZARD)
    for order in (
        "send the boat ashore",
        "buy ten tons of tin",
        "sell ten tons of tin",
        "take in water",
    ):
        e = at_sea.submit(order)
        assert e.kind == "order.rejected" and "not in port" in e.text, order
    assert "The prices: no prices are known" in at_sea.submit("the prices").text
    under_way = world_at(FALMOUTH_OUTER, heading=0.0, speed=3.0)
    e = under_way.submit("send the boat ashore")
    assert e.kind == "order.rejected" and "bring her to an anchor in Falmouth's roads" in e.text
    w = at_anchor_in(CARRICK_ROAD, ship=SCHOONER, heading=250.0, cargo={"purse_pounds": 500.0})
    assert w.readings.words("boat") == "the long-boat at the booms"
    e = w.submit("buy ten tons of tin")
    assert e.kind == "order.rejected" and "send the boat ashore first" in e.text
    e = w.submit("send the boat ashore with the mate")
    assert e.kind == "order.accepted" and w.ports.boat.errand == "person"
    w.run(1)
    assert events(w, "evolution.started")[-1].text == (
        "Away the long-boat's crew! Hoist out the long-boat."
    )
    mate = w.people.find("the mate")
    assert mate is not None and not mate.aboard and mate.where == "boat"
    assert w.people.state_words(mate) == "in the boat"
    e = w.submit("send for the mate")
    assert e.kind == "order.rejected"
    away = run_until(w, "boat.away", 10)
    assert (
        away.text
        == f"The long-boat away for the quay at Falmouth with {mate.name}, for the prices and "
        "what news there is."
    )
    assert w.readings["boat"]["away"]
    assert (
        w.readings.words("boat")
        == "the long-boat away for the prices and what news there is, pulling for the shore"
    )
    run_until(w, "boat.ashore", 60)
    assert mate.where == "shore" and w.people.state_words(mate) == "ashore"
    back = run_until(w, "boat.alongside", 120)
    pull_m = w.ports.to_shore_m(w.ports.ports["falmouth"])
    pull_s = pull_m / units.knots_to_ms(PT.BOAT_PACE_KN)
    assert back.tick - away.tick == pytest.approx(
        2 * pull_s + PT.BOAT_ASHORE_S["person"] + PT.BOAT_HOIST_IN_S, abs=120
    )
    assert mate.aboard and mate.where == "deck"
    assert events(w, "person.came")[-1].text == f"{mate.name} came aboard from the boat."
    prices = events(w, "market.prices")[0]
    assert prices.text.startswith("The mate's list of the prices at Falmouth is aboard: tin £")
    assert prices.tick == back.tick
    listed = w.readings["prices"]
    assert listed["port"] == "falmouth" and listed["prices"]["tin"] == 120.0
    assert listed["prices"]["brandy"] == 300.0  # French brandy at war, 200 by the half
    assert w.submit("the prices").text.startswith("The prices: at Falmouth (10 June")
    assert w.papers.page("the price list").lines[0].startswith("Prices at Falmouth, 10 June")
    assert not w.readings["boat"]["away"] and not w.people.find("the pilot")
    # the hold and the purse bound the bargain
    e = w.submit("buy two hundred tons of tin")
    assert e.kind == "order.rejected" and "room in the hold for 112 tons" in e.text
    e = w.submit("buy ten tons of tin")
    assert e.kind == "order.rejected" and "the purse holds £500" in e.text
    e = w.submit("buy ten tons of tea")
    assert e.kind == "order.rejected" and "market has no tea" in e.text
    e = w.submit("sell ten tons of tin")
    assert e.kind == "order.rejected" and "The hold has 0 tons of tin" in e.text
    e = w.submit("buy three tons of coal")
    assert e.kind == "market.bargain" and e.data["sum_pounds"] == 6.0
    assert w.purse.pounds == 494.0
    e = w.submit("sell ten tons of tin")
    assert e.kind == "order.rejected" and "is away" in e.text
    assert w.readings.words("boat").startswith("the long-boat away for the goods bought")
    bought = run_until(w, "market.bought", 180)
    assert bought.text.startswith("3 tons of coal hoisted in and struck down into the hold")
    assert w.hold.goods == {"coal": 3.0}
    assert w.readings.words("manifest").startswith("3 tons of coal; room for 109 tons")
    assert w.readings.words("purse").startswith("£494")
    e = w.submit("sell three tons of coal")
    assert e.kind == "market.bargain" and w.hold.goods == {} and w.purse.pounds == 500.0


def test_the_yard_supplies_by_demand_at_plymouth_and_the_chandlers_at_a_price_at_falmouth():
    plymouth = at_anchor_in(THE_SOUND, heading=180.0, cargo={"purse_pounds": 100.0})
    assert plymouth.ports.in_port() is plymouth.ports.ports["plymouth"]
    before = booms(plymouth.ship).counts.get("topmast", 0)
    e = plymouth.submit("demand a topmast from the yard")
    assert e.kind == "yard.demanded" and e.data["cost_pounds"] == 0 and e.data["hours"] == 8
    assert e.text.startswith(
        "Demanded a spare topmast by demand on the King's yard, surveyed and vouched at Plymouth"
    )
    assert plymouth.purse.pounds == 100.0
    plymouth.run(8 * 3600 - 60)
    assert not events(plymouth, "yard.done")
    plymouth.run(60)
    done = events(plymouth, "yard.done")
    assert (
        len(done) == 1 and done[0].text == "A spare topmast came off and was got in on the booms."
    )
    assert booms(plymouth.ship).counts["topmast"] == before + 1
    written = events(plymouth, "paper.written")[-1]
    assert written.text.startswith("The booms' list written up by the boatswain")
    # water and provisions by the quantity, into the purser's books
    water0 = plymouth.stores.water_tons
    e = plymouth.submit("take in twenty tons of water")
    assert e.kind == "yard.demanded" and e.data["quantity"] == 20 and e.data["hours"] == 2.0
    plymouth.run(2 * 3600)
    assert plymouth.stores.water_tons == water0 + 20
    assert "20 tons of water came off" in events(plymouth, "yard.done")[-1].text
    assert "the purser's books" in events(plymouth, "paper.written")[-1].data["paper"]
    e = plymouth.submit("take in provisions for ten days")
    assert e.kind == "yard.demanded" and e.data["cost_pounds"] == 0
    e = plymouth.submit("demand a mainmast from the yard")
    assert e.kind == "order.rejected" and "has no mainmast; it supplies" in e.text
    falmouth = at_anchor_in(CARRICK_ROAD, cargo={"purse_pounds": 100.0})
    e = falmouth.submit("demand a topmast from the yard")
    assert e.kind == "yard.demanded" and e.data["cost_pounds"] == 40.0
    assert "from the chandlers for £40 at Falmouth" in e.text and falmouth.purse.pounds == 60.0
    e = falmouth.submit("buy a suit of sails from the chandlers")
    assert e.kind == "order.rejected" and "the purse holds £60" in e.text
    poor = at_anchor_in(CARRICK_ROAD, cargo={"purse_pounds": 10.0})
    e = poor.submit("demand a topmast from the yard")
    assert e.kind == "order.rejected" and "costs £40 and the purse holds £10" in e.text
    # at Brest, hostile to the English, the yard will not serve her
    brest = at_anchor_in(THE_RADE_INNER, heading=250.0)
    e = brest.submit("demand a topmast from the yard")
    assert e.kind == "order.rejected" and "Brest is hostile to her" in e.text


def test_hands_enter_from_the_pool_at_a_bounty_and_muster_into_the_crew_by_the_boat():
    w = at_anchor_in(CARRICK_ROAD, cargo={"purse_pounds": 100.0})
    crew = w.ship.extra["crew"]
    n0 = crew.complement
    e = w.submit("enter four able seamen")
    assert e.kind == "crew.entering"
    assert e.data["n"] == 4 and e.data["bounty_pounds"] == 12.0
    assert e.text == "Entered 4 able at Falmouth at £3 bounty each; they come off in 12 hours."
    assert w.purse.pounds == 88.0 and w.ports.ports["falmouth"].crew_pool["able"]["hands"] == 0
    e = w.submit("enter two able seamen")
    assert e.kind == "order.rejected" and "No able hands are to be had at Falmouth" in e.text
    e = w.submit("enter ten landsmen")
    assert e.data["n"] == 10 and e.data["bounty_pounds"] == 10.0
    e = w.submit("enter six landsmen")
    assert e.data["n"] == 2 and "(6 asked; Falmouth has no more)" in e.text
    e = w.submit("enter three midshipmen")
    assert e.kind == "order.rejected" and "not a rating hands enter at" in e.text
    w.run(6 * 3600)
    entered = events(w, "crew.entered")
    assert len(entered) == 2 and all(
        "landsmen from Falmouth, come off in the boat" in x.text for x in entered
    )
    assert crew.complement == n0 + 12
    w.run(6 * 3600)
    entered = events(w, "crew.entered")
    assert len(entered) == 3 and entered[-1].text.startswith("Entered 4 able seamen from Falmouth")
    assert crew.complement == n0 + 16 and entered[-1].data["names"]
    names = entered[-1].data["names"]
    assert len(set(s.name for s in crew.sailors)) == len(crew.sailors)
    assert all(crew.by_id[s.id].rating.value == "able" for s in crew.sailors[-4:])
    # the same seed and the same orders, the same names: the recruits' stream is its own
    again = at_anchor_in(CARRICK_ROAD, cargo={"purse_pounds": 100.0})
    for order in ("enter four able seamen", "enter ten landsmen", "enter six landsmen"):
        again.submit(order)
    again.run(12 * 3600)
    assert events(again, "crew.entered")[-1].data["names"] == names


# ---------------------------------------------------------------------------
# Determinism and the checkpoint
# ---------------------------------------------------------------------------


def test_the_port_is_a_function_of_the_seed_and_a_checkpoint_mid_errand_resumes_it(tmp_path):
    from freesail.core import replay

    def voyage():
        w = at_anchor_in(CARRICK_ROAD, ship=SCHOONER, heading=250.0, cargo={"purse_pounds": 500.0})
        w.submit("send the boat ashore")
        w.run(600)
        return w

    a, b = voyage(), voyage()
    assert a.log.digest() == b.log.digest()
    assert a.readings["boat"] == b.readings["boat"]
    path = replay.write_checkpoint(a, tmp_path / "port.ckpt")
    _, c = replay.read_checkpoint(path)
    assert c.readings["boat"] == a.readings["boat"] and c.ports.boat.away
    for w in (a, c):
        run_until(w, "boat.alongside", 120)
        w.submit("buy three tons of coal")
        run_until(w, "market.bought", 180)
    assert a.log.digest() == c.log.digest()
    assert a.readings["prices"] == c.readings["prices"] and c.hold.goods == {"coal": 3.0}
    # the pilot's name is the people's stream: the same at the same seed, and the
    # lookout's stream untouched by the cutter (the pinned passages' ticks stand)
    p1 = world_at(SOUTH_OF_FALMOUTH, heading=0.0, speed=4.0)
    p2 = world_at(SOUTH_OF_FALMOUTH, heading=0.0, speed=4.0)
    for w in (p1, p2):
        w.submit("set plain sail")
        run_until(w, "port.pilot_aboard", 150)
    assert p1.ports.pilot.name == p2.ports.pilot.name
    assert p1.log.digest() == p2.log.digest()
