"""A far trader that never sailed, the harbour's King's ship, and a checkpoint refused: the
truths 7-790 to 7-793, 7-795 and 7-796 (7-794 and 7-798 in `test_harbour.py`, 7-797 and 7-799 in
`test_checkpoint.py`).

Three faults of the game as it was, two found by the owner in his own play (his notes 6 and
10 of 27 November), each reproduced first and pinned here as the game now has it.

- 7-790: a trader the business draws lying at the Havre's Little Road (three miles from the
  Great Road, beyond the port's reach of it, so `at anchor` and not `in port`) sails for Dover:
  her course out by the port's track to sea no longer begins with an anchor where she lies.
  OLD: she weighed every minute of the day, laid her whole passage afresh, found its first
  leg was to anchor in the Little Road, and lay there; the next minute the same.
- 7-791: a weigh that leaves her riding at her anchor still is not tried again until the hour
  at anchor has passed once more. OLD: every minute of the day.
- 7-792: a passage laid twice over the chart loads no tile the second time, and lays the
  same legs as before. OLD: the level kept sixteen tiles, the first in let go first, and every
  laying of the Havre's passage loaded all its tiles again.
- 7-793 (slow): a day of the owner's sea off Dover with the business on: no far vessel lays
  her passage more than three times in any hour.
- 7-795: the private table is a King's ship's by her papers as by her captain's place; a
  privateer's or a merchantman's papers give none; `private_signals` says last.
- 7-796: a game of the first action saved with the player a prisoner aboard the Renard loads
  by its checkpoint and goes on as the game that was saved. OLD: the checkpoint was headed
  with the Renard's hull's seed and journal, and was "not this save's".

7-794 is the harbour's King's ship in `tests/test_harbour.py`; 7-797 the sweep of the shipped
scenarios' checkpoints in `tests/test_checkpoint.py`.
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
    w.run(4 * 3600)
    brain = v.brain
    off_nm = bearing_and_distance(port.anchorage.position, v.position)[1] / units.NAUTICAL_MILE
    states = [s for _t, s in brain.history]
    assert states[0] == "at anchor", brain.history  # beyond the reach of the Great Road
    assert brain.state != "at anchor" and "on passage" in states, brain.history
    assert off_nm > 3.0, off_nm
    assert laid["trader"] <= 2, laid
    # her course out begins with the track's next mark, never the anchor she lay at
    assert not any(leg[0] == "anchor" and leg[1] == port.id for leg in v.plan), v.plan


def test_truth_7_791_a_weigh_that_leaves_her_at_anchor_is_not_tried_every_minute(monkeypatch):
    laid = _count_layings(monkeypatch)
    w = _channel_east(hour=8)
    # her voyage's end is where she lies: every plan laid anchors her there again
    v, port = _lying_at_the_little_road(
        w, "run home to the Little Road of Havre", "homeward", departing=False
    )
    w.run(5 * 3600)
    brain = v.brain
    assert brain.state == "at anchor", brain.history
    # an hour at anchor, then a weigh an hour: four or five in five hours, never one a minute
    assert 1 <= laid["homeward"] <= 5, laid
    assert int(brain._business[B.WEIGHED]) > 3 * 3600, brain._business


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


def test_truth_7_793_a_day_of_the_owners_sea_lays_no_passage_again_and_again(monkeypatch, tmp_path):
    laid = _count_layings(monkeypatch)
    w = _owners_sea(tmp_path)
    by_hour: Counter = Counter()
    for hour in range(24):
        before = Counter(laid)
        w.run(3600)
        for vid, n in laid.items():
            by_hour[(vid, hour)] = n - before.get(vid, 0)
    worst = max(by_hour.values(), default=0)
    assert worst <= LAYINGS_AN_HOUR_MOST, sorted(by_hour.items(), key=lambda kv: -kv[1])[:5]
    # the Havre's brandy trader of his sea sails, and is not lying in the Little Road
    havre = [
        v
        for v in w.vessels.vessels
        if v.brain is not None
        and v.brain.intent is not None
        and v.brain.intent.kind == "trade"
        and v.brain.intent.origin == "le-havre"
    ]
    assert havre, [getattr(v.brain, "intent", None) for v in w.vessels.vessels]
    for v in havre:
        assert "on passage" in [s for _t, s in v.brain.history], (v.id, v.brain.history)


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
