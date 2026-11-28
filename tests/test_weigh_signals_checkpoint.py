"""A far trader that never sailed, the harbour's King's ship, and a checkpoint refused: the
truths 7-790 to 7-793, 7-795 and 7-796 (7-794 and 7-798 in `test_harbour.py`, 7-797 and 7-799 in
`test_checkpoint.py`).

Three faults of the game as it was, two found by the owner in their own play (their notes 6
and 10 of 27 November), each reproduced first and pinned here as the game now has it; and the
lead's findings on the first build of the package (c22aa834).

- 7-790 (slow): a trader the business draws lying at the Havre's Little Road (three miles from
  the Great Road) is in port by the world's own rule (`Ports.in_port_at`: within the port's
  reach of its anchorage) and sails for Dover: her course out leaves out the anchorage she
  lies at, and ends at Dover's. OLD: she weighed every minute of the day, laid her whole
  passage afresh, found its first leg was to anchor in the Little Road, and lay there; the
  next minute the same. And a smack bound home to the port she weighed from comes to in it.
  OLD (c22aa834): every anchorage of that port was left out, and she ended her voyage off it.
- 7-791 (slow): a weigh that leaves her riding at her anchor still doubles the wait before
  the next, from an hour to a day. OLD: every minute of daylight; c22aa834, every hour.
- 7-792: a passage laid twice over the chart loads no tile the second time, and lays the
  same legs as before. OLD: the level kept sixteen tiles, the first in let go first, and every
  laying of the Havre's passage loaded all its tiles again.
- 7-793 (slow): a day of the owner's sea off Dover with the business on: no far vessel lays
  her passage more than three times in any hour, nor, lying in one place, in the day; and the
  Havre's trader comes to in Dover and sells her cargo.
- 7-795: the private table is a King's ship's by her papers as by her captain's place; a
  privateer's or a merchantman's papers give none; `private_signals` says last.
- 7-796: a game of the first action saved with the player a prisoner aboard the Renard loads
  by its checkpoint and goes on as the game that was saved. OLD: the checkpoint was headed
  with the Renard's hull's seed and journal, and was "not this save's".

7-794 is the harbour's King's ship in `tests/test_harbour.py`; 7-797 the sweep of the shipped
scenarios' checkpoints in `tests/test_checkpoint.py`; 7-798 the records' place kept as words, by
the harbour's road (`tests/test_harbour.py`) and the console's (`tests/test_console.py`).
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import brains as B
from freesail.world.geo import bearing_and_distance

ROOT = Path(__file__).resolve().parents[1]
HERMAPHRODITE = "data/ships/hermaphrodite-brig.yaml"
OFF_DOVER = {"lat_deg": 51.1145, "lon_deg": 1.32}  # where the owner's cruise began


def _channel_east(hour: int = 9, ship: str = HERMAPHRODITE):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, hour, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=OFF_DOVER,
        region="channel-east",
        ports=["le-havre", "dover"],
        nation="britain",
    )
    return make_world(1805, ship, sc)


def _lying_at_the_little_road(w, intent: str, vid: str = "trader", departing: bool = True):
    """A trader put at the Havre's Little Road as the business draws a ship lying at an
    anchorage (`Business._anchored_in`): her anchor down, her business in port part done;
    `departing`, the Havre the port she weighs from, as the business draws her."""
    from freesail.world.ships import vessel_from_spec

    port = w.dealings.ports["le-havre"]
    spec = {
        "id": vid,
        "description": "brig",
        "name": "Speedwell",
        "nation": "france",
        "position": port.anchorage.position.to_dict(),
        "goal": "bound for Falmouth",
        "intent": intent,
    }
    if departing:
        spec["departing"] = port.id
    v = vessel_from_spec(w, spec, w.vessels.serial + 1)
    w.vessels.serial += 1
    w.vessels.add(v)
    v.saved_plan = None
    v.plan = [("anchor", port.id)]
    brain = v.brain
    brain._departing = port.id if departing else ""
    brain.state = None
    brain.planned = True
    brain._business["drawn_in_port_s"] = 3 * 3600.0
    brain._state_entered = None
    return v, port


def _count_layings(monkeypatch) -> Counter:
    laid: Counter = Counter()
    plan = B.FarCaptain._plan

    def counted(self):
        laid[str(self.vessel.id)] += 1
        return plan(self)

    monkeypatch.setattr(B.FarCaptain, "_plan", counted)
    return laid


def test_truth_7_790_a_trader_lying_at_the_little_road_sails_for_dover(monkeypatch):
    laid = _count_layings(monkeypatch)
    w = _channel_east()
    v, port = _lying_at_the_little_road(w, "trade 33 tons of brandy from the Havre to Dover")
    w.run(12 * 3600)
    brain = v.brain
    off_nm = bearing_and_distance(port.anchorage.position, v.position)[1] / units.NAUTICAL_MILE
    states = [s for _t, s in brain.history]
    # in port by the world's own rule (`Ports.in_port_at`): within the port's reach of its
    # anchorage, three miles inside the Great Road
    assert states[0] == "in port", brain.history
    assert brain.state not in ("in port", "at anchor") and "on passage" in states, brain.history
    assert off_nm > 3.0, off_nm
    assert laid["trader"] <= 2, laid
    # her course out begins with the track's next mark, never the anchor she lay at; and it
    # ends at an anchor in Dover, the destination's anchorage laid where her track out had
    # held the only anchorage of the passage
    anchors = [leg for leg in v.plan if leg[0] == "anchor"]
    assert anchors == [("anchor", "dover")], v.plan


def test_truth_7_790_a_ship_bound_home_to_the_port_she_weighed_from_comes_to_in_it():
    """The lead's finding (1) of c22aa834: the anchorage left out is the one she lies at as
    she weighs, and only it. A smack twelve miles off Dover, the port she weighed from, runs
    home and comes to in it. OLD (c22aa834): every anchorage of that port was left out of
    every passage, and she ended her voyage off it, `done` at sea and "on passage"."""
    from freesail.world.geo import Position, destination
    from freesail.world.ships import vessel_from_spec

    road = {"lat_deg": 51.1145, "lon_deg": 1.32}  # Dover's road
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 6, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=destination(Position(**road), 150.0, 30 * units.NAUTICAL_MILE).to_dict(),
        region="channel-east",
        ports=["dover"],
    )
    w = make_world(1805, "data/ships/brig.yaml", sc)
    port = w.dealings.ports["dover"]
    off = destination(port.outer_road.position, 150.0, 12 * units.NAUTICAL_MILE)
    spec = {
        "id": "smack",
        "description": "smack",
        "name": "Brothers",
        "nation": "britain",
        "position": off.to_dict(),
        "goal": "run home to Dover",
        "intent": "run home to Dover",
        "departing": port.id,
    }
    v = vessel_from_spec(w, spec, w.vessels.serial + 1)
    w.vessels.serial += 1
    w.vessels.add(v)
    brain = v.brain
    brain._departing = port.id
    for _hour in range(8):
        w.run(3600)
        if v.done:
            break
    assert [s for _t, s in brain.history][-1] == "in port", brain.history
    assert v.done and brain.intent.done
    nm = bearing_and_distance(port.anchorage.position, v.position)[1] / units.NAUTICAL_MILE
    assert nm <= 0.5, nm


def test_truth_7_791_a_weigh_that_leaves_her_at_anchor_waits_longer_each_time(monkeypatch):
    """A ship at anchor at sea, out of any port's reach, whose every weigh lays a plan that
    anchors her where she lies: each weigh that leaves her riding there doubles the wait
    before the next, from an hour (`AT_ANCHOR_LEAST_S`) to a day (`AT_ANCHOR_MOST_S`), and
    is tried by day. OLD (the trunk): every minute of daylight; c22aa834: every hour."""
    from freesail.world.ships import vessel_from_spec

    weighs: list[int] = []
    plan = B.FarCaptain._plan

    def counted(self):
        if str(self.vessel.id) == "rider" and self.state is not None:  # not her making
            weighs.append(int(self.world.clock.tick))
        return plan(self)

    monkeypatch.setattr(B.FarCaptain, "_plan", counted)
    w = _channel_east(hour=6)
    here = {"lat_deg": 50.9, "lon_deg": 0.75}  # Rye Bay, some miles off: no port's reach
    spec = {
        "id": "rider",
        "description": "brig",
        "name": "Patience",
        "nation": "britain",
        "position": here,
        "goal": "run home to 50 54 N 0 45 E",
        "intent": "run home to 50 54 N 0 45 E",
    }
    v = vessel_from_spec(w, spec, w.vessels.serial + 1)
    w.vessels.serial += 1
    w.vessels.add(v)
    v.saved_plan = None
    v.plan = [("anchor", "")]
    brain = v.brain
    brain.state = None
    brain.planned = True
    w.run(24 * 3600)
    assert brain.state == "at anchor", brain.history
    assert [s for _t, s in brain.history] == ["at anchor"], brain.history
    gaps = [b - a for a, b in zip(weighs, weighs[1:], strict=False)]
    # an hour, two, four, then eight, the night waited through: four in the day
    assert 4 <= len(weighs) <= 6, weighs
    assert gaps[0] >= 2 * 3600 - 60, gaps
    assert all(b >= a for a, b in zip(gaps, gaps[1:], strict=False)), gaps
    assert all(g <= B.AT_ANCHOR_MOST_S + 12 * 3600 for g in gaps), gaps
    assert int(brain._business[B.WEIGH_TRIES]) == len(weighs), brain._business
    # the bound: after twenty weighs that left her riding, she is still asked within a day of
    # the last, by daylight, and once
    set_at = int(w.clock.tick)
    brain._business[B.WEIGH_TRIES] = 20
    brain._business[B.WEIGHED] = set_at
    del weighs[:]
    w.run(B.AT_ANCHOR_MOST_S + 12 * 3600)
    assert len(weighs) == 1, weighs
    assert B.AT_ANCHOR_MOST_S <= weighs[0] - set_at <= B.AT_ANCHOR_MOST_S + 12 * 3600, weighs
    # come to anew (her anchor let go again after a passage), the count begins afresh: the
    # hour, not the day, before she is asked
    brain._business[B.WEIGH_TRIES] = 20
    brain._business[B.WEIGHED] = int(w.clock.tick) - 60
    del weighs[:]
    brain._enter("at anchor")
    came_to = int(w.clock.tick)
    w.run(2 * 3600)
    assert len(weighs) == 1, (weighs, w.clock.ship_time)
    assert B.AT_ANCHOR_LEAST_S <= weighs[0] - came_to <= B.AT_ANCHOR_LEAST_S + 120, weighs


def test_truth_7_792_a_passage_laid_again_reads_its_tiles_from_the_cache_and_lays_the_same(
    monkeypatch,
):
    from freesail.world import chart as C
    from freesail.world.captains import Planner, read_intent

    w = _channel_east()
    intent = read_intent(w, "trade 33 tons of brandy from the Havre to Dover")
    port = w.dealings.ports["le-havre"]
    for level in w.chart.levels:
        level._cache.clear()
        level._order.clear()
    first = Planner(w).legs_for(intent, port.anchorage.position, port.id)
    loads: list[str] = []
    load = C.Tile.load.__func__

    def counted(cls, path):
        loads.append(str(path))
        return load(cls, path)

    monkeypatch.setattr(C.Tile, "load", classmethod(counted))
    again = Planner(w).legs_for(intent, port.anchorage.position, port.id)
    assert loads == []
    assert [(leg.kind, leg.words, leg.position) for leg in again] == [
        (leg.kind, leg.words, leg.position) for leg in first
    ]
    # and the same legs with a level of sixteen tiles, as the chart kept before
    for level in w.chart.levels:
        level.cache_size = 16
        level._cache.clear()
        level._order.clear()
    small = Planner(w).legs_for(intent, port.anchorage.position, port.id)
    assert [(leg.kind, leg.words, leg.position) for leg in small] == [
        (leg.kind, leg.words, leg.position) for leg in first
    ]
    assert len(loads) > 16  # the passage reads more tiles than sixteen
    # the least lately read is let go: of two kept, the one read again stays
    level = w.chart.levels[1]
    first_three = sorted(level.paths)[:3]
    keys = [tuple(int(x) for x in name.split("_")) for name in first_three]
    level.cache_size = 2
    level._cache.clear()
    level._order.clear()
    for key in (keys[0], keys[1], keys[0], keys[2]):
        level.tile(*key)
    del loads[:]
    level.tile(*keys[0])
    assert loads == []  # read again, kept
    level.tile(*keys[1])
    assert len(loads) == 1  # the least lately read, let go


def _owners_sea(tmp_path: Path):
    """The owner's cruise as he made it in the harbour (his notes, 27 November): the region
    channel-east from 05:00 of 12 June 1805, seed 1805, the hermaphrodite brig off Dover, a
    King's ship by her papers, climatology on, the business on; no orders given."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    path = tmp_path / "off-dover.yaml"
    path.write_text(
        "name: Off Dover\nseed: 1805\nstart: 1805-06-12T05:00\n"
        "position: {lat_deg: 51.1145, lon_deg: 1.32}\nregion: channel-east\n"
        "nation: britain\nship:\n  file: data/ships/hermaphrodite-brig.yaml\n"
        "  heading_deg: 200\npapers:\n  service: kings\nbusiness: on\n"
        "weather:\n  climatology: true\n",
        encoding="utf-8",
    )
    sf = load_scenario(path)
    w = make_scenario_world(sf)
    begin(w, sf)
    return w


# JUDGEMENT: a far captain lays his passage when he weighs, when his business in port is done
# and when a chase or a gale is over; three in an hour is more than any of them asks. Measured
# over the day (package 129): at most two in any hour; OLD, the Havre's trader sixty.
LAYINGS_AN_HOUR_MOST = 3
# JUDGEMENT: lying in one place (her anchor down), a far captain lays his passage when his
# business in port is done, or when he weighs from an anchorage and the wait before the next
# weigh doubles (`brains.AT_ANCHOR_MOST_S`); three in a day is more than either asks. Measured
# over the owner's day: at most two; OLD (c22aa834), a ship who could not get away, one an
# hour of daylight for ever.
LAYINGS_LYING_A_DAY_MOST = 3
# JUDGEMENT, measured: the Havre's trader, the Little Road to Dover some 110 miles with the wind
# in the west, comes to in Dover at 37 hours (package 129); the bound allows the tide's turn.
DOVER_WITHIN_H = 42


def test_truth_7_793_a_day_of_the_owners_sea_lays_no_passage_again_and_again(monkeypatch, tmp_path):
    """The owner's sea a day (`_owners_sea`): no far vessel lays her passage more than three
    times in any hour, nor, lying in one place with her anchor down, more than three times
    in the day."""
    laid = _count_layings(monkeypatch)
    lying: Counter = Counter()
    plan = B.FarCaptain._plan

    def told(self):
        here = self.vessel.plan[:1]
        if here and here[0][0] == "anchor":
            lying[str(self.vessel.id)] += 1
        return plan(self)

    monkeypatch.setattr(B.FarCaptain, "_plan", told)
    w = _owners_sea(tmp_path)
    by_hour: Counter = Counter()
    for hour in range(24):
        before = Counter(laid)
        w.run(3600)
        for vid, n in laid.items():
            by_hour[(vid, hour)] = n - before.get(vid, 0)
    assert laid, "no far vessel laid a passage"
    worst = max(by_hour.values(), default=0)
    assert worst <= LAYINGS_AN_HOUR_MOST, sorted(by_hour.items(), key=lambda kv: -kv[1])[:5]
    assert max(lying.values(), default=0) <= LAYINGS_LYING_A_DAY_MOST, lying.most_common(5)


def test_truth_7_793_the_havres_trader_comes_to_in_dover_and_sells_her_cargo():
    """What the owner would see of his sea's trader: drawn lying at the Havre's Little Road
    with a cargo for Dover, she sails, comes to in Dover within `DOVER_WITHIN_H` hours,
    sells her cargo there, buys a return cargo and sails again. The player's ship is in mid
    Channel, out of the near detail's reach of her (the game's own captain sails a ship
    within two miles of the player's, `ships.NEAR_DETAIL_NM`). OLD: the trunk, she lay at
    the Little Road; c22aa834, she reached Dover and ended her voyage off it, `done` at sea,
    nothing sold."""
    from freesail.world.ships import vessel_from_spec

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 6, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 50.25, "lon_deg": -0.6},
        region="channel-east",
        ports=["le-havre", "dover"],
    )
    w = make_world(1805, "data/ships/brig.yaml", sc)
    port, dover = w.dealings.ports["le-havre"], w.dealings.ports["dover"]
    spec = {
        "id": "trader",
        "description": "brig",
        "name": "Speedwell",
        "nation": "britain",
        "position": port.anchorage.position.to_dict(),
        "goal": "trading the Havre to Dover",
        "intent": "trade 20 tons of wine from the Havre to Dover",
        "departing": port.id,
    }
    v = vessel_from_spec(w, spec, w.vessels.serial + 1)
    w.vessels.serial += 1
    w.vessels.add(v)
    v.saved_plan = None
    v.plan = [("anchor", port.id)]
    brain = v.brain
    brain._departing = port.id
    brain.state = None
    brain.planned = True
    brain._business["drawn_in_port_s"] = 3 * 3600.0
    brain._state_entered = None
    in_dover = None
    for hour in range(1, DOVER_WITHIN_H + 13):
        w.run(3600)
        here = bearing_and_distance(dover.anchorage.position, v.position)[1]
        if in_dover is None and brain.state == "in port" and here < 2 * units.NAUTICAL_MILE:
            in_dover = hour
        if any("sold at" in words for _t, words in getattr(v, "story", ()) or ()):
            break
    assert in_dover is not None and in_dover <= DOVER_WITHIN_H, (in_dover, brain.history)
    assert v.detail == "far"
    sold = [words for _t, words in v.story if "sold at" in words]
    assert sold[0].startswith("20 tons of wine sold at Dover"), v.story
    # her return cargo is for the Havre, the port she sailed from, and she sails with it
    assert brain.intent.kind == "trade", brain.intent
    assert (brain.intent.origin, brain.intent.destination) == ("dover", "le-havre"), brain.intent
    assert not v.done


def _papers(**papers):
    w = _channel_east(ship="data/ships/brig.yaml")  # her captain given no place
    w.scenario.papers = dict(papers)
    return w


def test_truth_7_795_the_private_table_by_her_papers_service():
    from freesail.world.signals import table_of

    for papers, carries in (
        ({}, False),
        ({"service": "kings"}, True),
        ({"service": "King's ship"}, True),
        ({"service": "kings", "private_signals": False}, False),
        ({"service": "privateer"}, False),
        ({"service": "merchant"}, False),
        ({"service": "merchant", "private_signals": True}, True),
        ({"private_signals": True}, True),
    ):
        w = _papers(**papers)
        assert w.captain.role == "", papers
        table = table_of(w)
        assert (table is not None) == carries, (papers, table)
        if table is not None:
            assert table.nation == "britain" and table.adjective == "British"
            said = w.submit("the private signal").text
            assert said.startswith("The private signal: by day,"), said
        else:
            said = w.submit("show the private signal").text
            assert "this ship carries none" in said, said


def _first_action_taken(tmp_path: Path):
    """The first action begun as the harbour begins it, the guns fired, then the colours struck
    and the player taken aboard the Renard, his parole asked and given."""
    from freesail.ui.server import prepare_game, server_parser

    args = server_parser().parse_args(
        ["--scenario", str(ROOT / "data/scenarios/first-action.yaml")]
    )
    w = prepare_game(args, say=lambda _line: None)
    for order in ("beat to quarters", "cast loose the guns", "fire as they bear"):
        w.submit(order)
    w.run(900)
    w.submit("strike the colours")
    w.run(1500)
    w.submit("I give my parole")
    w.run(600)
    return w


def test_truth_7_796_the_first_action_saved_a_prisoner_loads_by_its_checkpoint(tmp_path):
    from freesail.core import replay as R
    from freesail.ui.server import prepare_game, server_parser

    w = _first_action_taken(tmp_path)
    # the player is held aboard her captor: the world's per-ship names read the Renard's hull
    assert w.own is not w.__dict__["_own"]
    save = tmp_path / "taken.json"
    R.save_to_file(w, save)
    loaded = prepare_game(server_parser().parse_args(["--load", str(save)]), say=lambda _l: None)
    report = loaded.load_report
    assert report.how == "checkpoint", report.words
    assert loaded.log.digest() == w.log.digest()
    w.run(600)
    loaded.run(600)
    assert loaded.clock.tick == w.clock.tick
    assert loaded.log.digest() == w.log.digest()
