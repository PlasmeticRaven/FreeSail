"""The ration and the stores' fall (spec M7b §19; package 54): the Regulations' table as
data, the meals' fall of the provisions and the water by the ration for the company, the
purser's reading of what remains and for how long, short allowance with its line and its
cost to the hands, the water found foul, a store run out; nothing of it in the log but the
order and a store run out."""

from __future__ import annotations

import copy
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.crew import routine as routine_mod
from freesail.crew import victuals
from freesail.orders.errors import OrderError
from freesail.ship.loader import load_spec as load_ship_spec
from freesail.ship.schema import ShipFileError

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = str(ROOT / "data/ships/frigate-36.yaml")
CUTTER = str(ROOT / "data/ships/cutter.yaml")
SHIPS = sorted((ROOT / "data/ships").glob("*.yaml"))


def world_for(ship=FRIGATE, start=datetime(1805, 6, 11, 7, 58)):
    """A Tuesday at two minutes to breakfast."""
    sc = Scenario(start_time=start, gustiness=0.0, variability=0.0)
    return make_world(7, ship, sc)


def day_of_meals(world):
    for _, name in victuals.load_ration().meals:
        victuals.serve(world, name)


def test_the_ration_table_is_the_regulations_week_and_every_ship_names_it():
    """The Navy's table by the day (Sect. IX, Chap. I, Art. I): a pound of biscuit and a
    gallon of beer every day; the week's proportion as the printed table has it. Every
    ship file names the table and the water a man a day in its `crew.ration` block."""
    ration = victuals.load_ration()
    days = ration.tables["navy"]["days"]
    week = {}
    for issue in days.values():
        for k, v in issue.items():
            week[k] = week.get(k, 0) + v
    assert week == {
        "biscuit_lb": 7,
        "beer_gal": 7,
        "beef_lb": 4,
        "pork_lb": 2,
        "pease_pt": 2,
        "oatmeal_pt": 3,
        "butter_oz": 6,
        "cheese_oz": 12,
    }
    assert [h for h, _ in ration.meals] == [8, 12, 16]
    assert ration.gallons_a_ton == 252 and ration.short_allowance == 0.5
    for path in SHIPS:
        spec = load_ship_spec(path).crew
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))["crew"]["ration"]
        assert raw == {"table": "navy", "water_gallons": 1}, path.name
        assert spec.ration.table == "navy" and spec.ration.water_gallons == 1.0
    w = world_for()
    assert victuals.day_words(w) == (
        "Tuesday: a pound of biscuit, a gallon of beer and two pounds of beef a man"
    )


def test_a_ration_block_with_a_word_it_does_not_take_is_refused(tmp_path):
    doc = yaml.safe_load(Path(CUTTER).read_text(encoding="utf-8"))
    doc["crew"]["ration"]["grog"] = 1
    p = tmp_path / "cutter.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    with pytest.raises(ShipFileError, match="ration has 'grog'"):
        load_ship_spec(p)


def test_a_day_of_meals_draws_a_day_of_provisions_and_the_companys_gallons():
    """The frigate's 264: a day's three meals take a day of provisions at full allowance
    and 264 gallons of water, 264/252 of a ton; the purser's reading says what remains
    and for how long."""
    w = world_for()
    assert w.stores.provisions_days == 120 and w.stores.water_tons == 100
    day_of_meals(w)
    assert w.stores.provisions_days == pytest.approx(119.0)
    assert w.stores.water_tons == pytest.approx(100 - 264 / 252)
    r = w.readings["stores"]
    assert r["provisions_days_left"] == pytest.approx(119.0, abs=0.05)
    assert r["water_days"] == pytest.approx((100 - 264 / 252) * 252 / 264, abs=0.05)
    assert w.readings.words("stores") == "water 99 tons for 94.5 days, provisions for 119 days"
    page = w.papers.page("the purser's books").lines
    assert page[0] == "Water: 99 tons in the ground tier, for 94.5 days at full allowance."
    assert page[1] == "Provisions: 119 days at full allowance for 264 men."
    assert page[2] == "Expended since she was stored: 1 ton of water and 1 day of provisions."
    assert page[3].startswith("Tuesday: a pound of biscuit")


def test_the_world_serves_at_the_meal_hours_and_writes_nothing_of_it():
    """The meals at eight, noon and four: the fall is a reading and not a line."""
    w = world_for()
    lines = len(w.log)
    w.run(3 * 60)  # through eight o'clock
    assert w.stores.provisions_days == pytest.approx(120 - 1 / 3)
    assert not [e for e in w.log.all()[lines:] if e.kind.startswith(("stores.", "needs."))]


def test_short_allowance_halves_the_fall_says_the_temper_and_tires_the_hands():
    w = world_for()
    e = w.submit("short allowance")
    assert e.kind == "stores.allowance" and e.severity.value == "notable"
    assert "short allowance, half the whole" in e.text and "take it sullenly" in e.text
    assert "the provisions for 240 days" in e.text
    assert ("captain", "short allowance") in [(a, t) for _, a, t in w.journal]
    day_of_meals(w)
    assert w.stores.provisions_days == pytest.approx(119.5)
    assert w.stores.water_tons == pytest.approx(100 - 132 / 252)
    assert "(239 at short allowance)" in w.readings.words("stores")
    routine = w.ship.extra["routine"]
    assert routine.hardship == pytest.approx(0.5)
    with pytest.raises(OrderError, match="short allowance already"):
        w.ship.handle_order("short allowance")
    back = w.submit("whole allowance")
    assert "back to whole allowance" in back.text and routine.hardship == 0.0
    # the officer may not: the allowance is the captain's
    from freesail.agents.agent import OFFICER_DOMAIN

    assert OFFICER_DOMAIN.why_not("short allowance", "allowance", "1") is not None
    assert OFFICER_DOMAIN.why_not("eat", "needs", "1") is None


def test_the_hands_tire_the_faster_on_short_allowance_and_not_at_all_otherwise():
    """The routine's rates scaled by the hardship; at nought the rates are as they were,
    to the bit."""
    a, b = world_for(), world_for()
    b.submit("short allowance")
    c = world_for()
    c.ship.extra["routine"].hardship = 0.0
    for w in (a, b, c):
        w.run(600)
    fa = [s.fatigue for s in a.ship.extra["crew"].sailors]
    fb = [s.fatigue for s in b.ship.extra["crew"].sailors]
    fc = [s.fatigue for s in c.ship.extra["crew"].sailors]
    assert fa == fc
    assert sum(fb) > sum(fa)
    assert routine_mod.HARDSHIP_WORK == 0.5 and routine_mod.HARDSHIP_REST == 0.5


def test_the_water_found_foul_costs_the_hands_and_a_store_run_out_is_said_once():
    w = world_for(CUTTER)
    w.stores.foul = True
    victuals.tick(w)
    assert w.ship.extra["routine"].hardship == pytest.approx(victuals.FOUL_WATER_HARDSHIP)
    w.stores.provisions_days = 0.2
    lines = victuals.serve(w, "dinner")
    assert [(k, d["store"]) for _, k, _, d in lines] == [("stores.out", "provisions")]
    assert "The last of the provisions served out at dinner" in lines[0][2]
    assert victuals.serve(w, "supper") == []
    assert w.stores.provisions_days == 0.0 and w.ship.extra["routine"].hardship == 1.0


def test_a_ship_with_no_stores_in_her_file_is_not_victualled():
    w = world_for()
    w.ship.spec = copy.deepcopy(w.ship.spec)
    w.ship.spec.crew.stores.provisions_days = 0
    w.ship.spec.crew.stores.water_tons = 0
    assert not victuals.victualled(w) and victuals.tick(w) == []
    with pytest.raises(OrderError, match="keeps no stores"):
        w.ship.handle_order("short allowance")


def test_a_save_with_short_allowance_replays_to_the_same_digest_and_stores():
    w = world_for(CUTTER)
    w.submit("short allowance")
    w.run(5 * 3600)
    again = replay.replay_world(w, ship_factory)
    assert again.log.digest() == w.log.digest()
    assert again.stores.provisions_days == pytest.approx(w.stores.provisions_days)
    assert again.stores.allowance == 0.5
