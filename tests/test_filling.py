"""The gunner's filling of cartridges, and the guns waiting on him (practice and resupply,
between packages 72 and 73; docs/design/Build-PracticeAndResupply.md §4, §8.1).

The King's cutter of the action truths at seed 7: the party at quarters and out of them,
the men read and never moved, no filling with the hoy alongside or the colours struck, a
gun waiting at the cartridge phase told once an outage, the magazine out in today's words
and data and told again after powder comes aboard, the powder's running out told only when
the filling brings it under the charges and in words true to what is left, the report of
the cartridges filled only when it was asked for and something came back, a kind with no
level never waited on, no call of `fill` while the magazine is full, a battery, its
services and a magazine pickled before this build, and the magazine's reading saying the
gunner fills only while he does (the review's finding).
"""

from __future__ import annotations

import pickle
from datetime import datetime

from freesail.api.session import make_world
from freesail.combat.filling import fill_tick, fillers
from freesail.combat.guns import Battery, Service, battery_of
from freesail.core.events import Severity
from freesail.core.world import Scenario
from freesail.crew.quarters import POWDER, quarters_of
from freesail.ship.parts import Charge, Magazine, magazine

SEED = 7
CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
CARR_12 = ("carronade", 12.0)
WAIT_WORDS = (
    "No more filled cartridges for the 12-pounder carronades: the gunner is filling, and the "
    "guns wait on him."
)
OUT_WORDS = (
    "The gunner reports no more cartridges for the 12-pounder carronades: the magazine is out."
)


def _world(ship: str = CUTTER, hour: int = 10):
    """The action truths' scenario (tests/test_known_truths.py `_action_scenario`): off the
    Lizard on 12 June 1805, lying still, at the hour given."""
    return make_world(
        SEED,
        ship,
        Scenario(
            start_time=datetime(1805, 6, 12, hour, 0),
            wind_from_deg=270.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 49.8, "lon_deg": -5.3},
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            nation="britain",
            ship_heading_deg=180.0,
            ship_speed_kn=0.0,
        ),
    )


def _at_quarters(w) -> None:
    w.submit("beat to quarters")
    w.run(5)


def _guns_ready(w) -> None:
    _at_quarters(w)
    w.submit("cast loose the guns")
    w.run(200)


def _drawn(w) -> None:
    """Every gun drawn and its cycle cleared, so that each comes to its cartridge again."""
    battery = battery_of(w.ship)
    for g in w.ship.guns.values():
        g.loaded = None
        g.primed = False
        g.run_out = False
        battery.services[g.id] = Service()


def _lines(w, kind: str, words: str | None = None) -> list:
    return [e for e in w.log if e.kind == kind and (words is None or words in e.text)]


def test_the_party_at_quarters_by_day_out_of_quarters_and_none_at_night():
    """At quarters the bill's `filling` of the powder division who are fit and not lent;
    out of quarters the bill's figure while the idlers are up; nobody by night out of
    quarters. The frigate's is ten, the cutter's one."""
    w = _world()
    q = quarters_of(w.ship)
    assert not q.at_quarters and fillers(w, w.ship, q) == 1
    _at_quarters(w)
    assert q.at_quarters and q.divisions[POWDER]
    assert fillers(w, w.ship, q) == 1
    lent = {s.id: s.at for s in q.divisions[POWDER]}
    for s in q.divisions[POWDER]:
        s.at = "lent"
    assert fillers(w, w.ship, q) == 0
    for s in q.divisions[POWDER]:
        s.at = lent[s.id]
    night = _world(hour=23)
    nq = quarters_of(night.ship)
    assert fillers(night, night.ship, nq) == 0
    _at_quarters(night)
    assert fillers(night, night.ship, nq) == 1
    frigate = _world(FRIGATE)
    fq = quarters_of(frigate.ship)
    assert fillers(frigate, frigate.ship, fq) == 10
    _at_quarters(frigate)
    assert len([s for s in fq.divisions[POWDER] if s.fit and s.at is None]) > 10
    assert fillers(frigate, frigate.ship, fq) == 10


def test_the_fillers_are_read_and_never_moved_and_the_filling_draws_and_says_nothing():
    w = _world()
    _at_quarters(w)
    q = quarters_of(w.ship)
    mag = magazine(w.ship)
    mag.set_filled("carronade", 12, 320)
    crew = w.ship.extra["crew"]
    before = [(s.id, s.at, s.quarters, s.turned_up) for s in crew.sailors]
    streams, lines = w.rng.stream_names(), len(w.log)
    battery = battery_of(w.ship)
    for _ in range(10):
        fill_tick(w, battery, q)
    assert [(s.id, s.at, s.quarters, s.turned_up) for s in crew.sailors] == before
    # ten minutes of one man: 600 man-seconds, four cartridges of 135, the rest in hand
    assert mag.filled_by_gunner == 4 and mag.filled_of("carronade", 12) == 324
    assert mag.powder_lb == 196.0 and mag.fill_s == 60.0
    assert w.rng.stream_names() == streams and len(w.log) == lines


def test_no_filling_while_the_hoy_is_alongside_when_struck_or_when_held():
    w = _world()
    q = quarters_of(w.ship)
    mag = magazine(w.ship)
    battery = battery_of(w.ship)
    mag.set_filled("carronade", 12, 320)
    w.stores.galley_fire_out = "powder"  # the hoy alongside (the supply's state)
    fill_tick(w, battery, q)
    assert mag.fill_s == 0.0
    w.stores.galley_fire_out = ""
    fill_tick(w, battery, q)
    assert mag.fill_s == 60.0
    w.ship.extra["struck"] = 600  # the tick she struck (`action.strike`)
    fill_tick(w, battery, q)
    assert mag.fill_s == 60.0
    del w.ship.extra["struck"]
    mag.filling_held = True
    fill_tick(w, battery, q)
    assert mag.fill_s == 60.0 and mag.filled_by_gunner == 0
    mag.filling_held = False
    fill_tick(w, battery, q)
    assert mag.fill_s == 120.0 and mag.filled_by_gunner == 0  # a carronade's is 135
    fill_tick(w, battery, q)
    assert mag.fill_s == 45.0 and mag.filled_by_gunner == 1


def test_the_magazine_reading_says_the_gunner_fills_only_while_he_does_and_why_not():
    """The `magazine` reading and the gunner's account's page name the kind he fills for
    while he fills; by night out of quarters, with the hoy alongside, with the colours
    struck and at quarters with no man of the powder to spare, the filling's own gate
    (`filling.not_filling`), they say he is not filling for it and why (the review's
    finding: "the gunner filling for the 12-pounder carronades" in each, and nothing
    filled)."""

    from freesail.api.action_readings import _magazine

    def head(w):  # the row's getter: `w.readings` keeps one view a tick
        return _magazine(w, None)["lines"][0]

    filling = (
        "Filled cartridges: 300 of 330 for the 12-pounder carronades; the gunner filling for "
        "the 12-pounder carronades."
    )
    stopped = (
        "Filled cartridges: 300 of 330 for the 12-pounder carronades; the gunner not filling "
        "for the 12-pounder carronades"
    )
    w = _world()
    mag = magazine(w.ship)
    mag.set_filled("carronade", 12, 300)
    assert head(w) == filling
    assert w.papers.page("the gunner's account").lines[0] == filling
    w.stores.galley_fire_out = "powder"  # the hoy alongside (the supply's state)
    assert head(w) == stopped + " while the hoy is alongside."
    page = w.papers.page("the gunner's account")
    assert page.lines[0] == stopped + " while the hoy is alongside."
    w.run(600)
    assert mag.filled_by_gunner == 0
    w.stores.galley_fire_out = ""
    w.ship.extra["struck"] = 600  # the tick she struck (`action.strike`)
    assert head(w) == stopped + ", the colours struck."
    w.run(600)
    assert mag.filled_by_gunner == 0
    del w.ship.extra["struck"]
    assert head(w) == filling
    w.run(600)
    assert mag.filled_by_gunner > 0  # by day out of quarters he fills, as it said
    _at_quarters(w)
    q = quarters_of(w.ship)
    assert head(w).endswith("; the gunner filling for the 12-pounder carronades.")
    for s in q.divisions[POWDER]:
        s.at = "lent"
    assert head(w).endswith(
        "; the gunner not filling for the 12-pounder carronades, no man of the powder to spare."
    )
    mag.filling_held = True
    assert head(w).endswith("; the filling stopped by order.")
    night = _world(hour=23)
    nmag = magazine(night.ship)
    nmag.set_filled("carronade", 12, 300)
    assert head(night) == stopped + " by night."
    night.run(3600)
    assert nmag.filled_by_gunner == 0
    _at_quarters(night)
    assert head(night) == filling  # at quarters by night he fills


def test_a_gun_waits_at_the_cartridge_phase_while_the_gunner_fills_told_once_an_outage():
    """No filled cartridge and powder below: each gun waits at its cartridge with its phase
    and seconds kept, `guns.filling` said once for the kind; the gunner's cartridges are
    taken as they come. Once the kind is back at its level the next outage is told."""
    w = _world()
    _guns_ready(w)
    _drawn(w)
    mag = magazine(w.ship)
    battery = battery_of(w.ship)
    mag.set_filled("carronade", 12, 0)
    w.run(110)
    waiting = []
    for g in w.ship.guns.values():
        svc = battery.services[g.id]
        if not svc.idle and battery._phases(g)[svc.phase][0] == "cartridge":
            assert svc.stalled == "no cartridge" and not g.loaded
            assert svc.left_s == battery._phases(g)[svc.phase][1]  # not begun
            waiting.append(g.id)
    assert len(waiting) >= 5, waiting
    told = _lines(w, "guns.filling")
    assert [e.text for e in told] == [WAIT_WORDS]
    assert told[0].severity is Severity.NOTABLE
    assert told[0].data["kind"] == "carronade" and told[0].data["pounder"] == 12.0
    assert not _lines(w, "guns.magazine_empty")
    w.run(15 * 60)
    loaded = [g for g in w.ship.guns.values() if g.loaded]
    assert len(loaded) == 6 and mag.filled_by_gunner >= 6
    assert len(_lines(w, "guns.filling")) == 1  # never back at its level: one outage
    # a level of one: each cartridge filled ends the outage, and the next is told
    w2 = _world()
    _guns_ready(w2)
    _drawn(w2)
    mag2 = magazine(w2.ship)
    mag2.level = {CARR_12: 1}
    mag2.set_filled("carronade", 12, 0)
    w2.run(10 * 60)
    assert len(_lines(w2, "guns.filling")) >= 2
    # held by order: the words say so, and nothing is filled
    w3 = _world()
    _guns_ready(w3)
    _drawn(w3)
    mag3 = magazine(w3.ship)
    mag3.set_filled("carronade", 12, 0)
    mag3.filling_held = True
    w3.run(5 * 60)
    held = _lines(w3, "guns.filling")
    assert len(held) == 1 and held[0].text == (
        "No more filled cartridges for the 12-pounder carronades, and the guns wait: the "
        "filling stopped by order; say 'fill cartridges'."
    )
    assert held[0].data["held"] is True and mag3.filled_by_gunner == 0


def test_the_magazine_out_keeps_todays_words_and_data_and_is_told_again_after_a_receipt():
    """No filled cartridge and no powder: today's path and words, once, and nothing from
    the gunner, whose powder never fell under a charge (there was none to fill from);
    powder taken in, the gunner fills, the guns load, and when it is spent he says so in
    the build design's words, and the magazine is out again and told again (the
    self-clearing sets)."""
    w = _world()
    _guns_ready(w)
    _drawn(w)
    mag = magazine(w.ship)
    mag.set_filled("carronade", 12, 0)
    mag.powder_lb = 0.0
    w.run(120)
    out = _lines(w, "guns.magazine_empty")
    assert [e.text for e in out] == [OUT_WORDS]
    assert out[0].data == {"pounder": 12.0, "charge": "round"}
    assert out[0].severity is Severity.NOTABLE
    assert not _lines(w, "guns.powder_out")
    assert not _lines(w, "guns.filling") and not any(g.loaded for g in w.ship.guns.values())
    mag.receive(3.0, when="12 June 1805", words="Three pounds of powder.")
    w.run(12 * 60)
    assert sum(1 for g in w.ship.guns.values() if g.loaded) == 3
    assert mag.powder_lb == 0.0 and mag.filled_by_gunner == 3
    assert [e.text for e in _lines(w, "guns.magazine_empty")] == [OUT_WORDS, OUT_WORDS]
    spent = _lines(w, "guns.powder_out")  # the last filled not yet taken by its gun
    assert [e.text for e in spent] == [
        "The gunner reports all the powder filled: no loose powder below, and 329 "
        "cartridges short of the allowance."
    ]
    assert spent[0].data == {"short": 329, "powder_lb": 0.0}
    assert spent[0].severity is Severity.NOTABLE
    assert len(_lines(w, "guns.filling")) == 1


def test_the_cartridges_filled_are_reported_only_when_it_was_asked_and_out_of_quarters():
    """`guns.filled` when a receipt or `fill cartridges` asked for it and the last kind
    comes back to its level: out of quarters at once; at quarters the report waits, and is
    said once she is out of them. Asked when nothing was short (a receipt into a complete
    magazine), it is forgotten, and a later refill nobody asked about says nothing."""
    w = _world()
    mag = magazine(w.ship)
    mag.set_filled("carronade", 12, 320)
    w.run(30 * 60)  # by day out of quarters: the bill's one man, ten cartridges
    assert mag.filled_of("carronade", 12) == 330 and not mag.short
    assert mag.powder_lb == 190.0 and not _lines(w, "guns.filled")
    mag.set_filled("carronade", 12, 320)
    mag.report_filled = True  # a receipt or `fill cartridges` asks for the report
    w.run(30 * 60)
    filled = _lines(w, "guns.filled")
    assert [e.text for e in filled] == [
        "The gunner has the cartridges filled to the allowance: 330 for the 12-pounder "
        "carronades; 1 barrel and 80 pounds below."
    ]
    assert filled[0].severity is Severity.ROUTINE
    assert not mag.report_filled and not mag.report_due
    # a receipt into a complete magazine: nothing comes back, so the request is forgotten
    mag.receive(100.0, when="12 June 1805", words="A barrel of powder.")
    assert mag.report_filled and not mag.short
    w.run(2 * 60)
    assert not mag.report_filled and len(_lines(w, "guns.filled")) == 1
    # a cartridge spent and filled again later: nobody asked, and nothing is said
    mag.take("carronade", 12, Charge.BLANK)
    w.run(10 * 60)
    assert mag.filled_of("carronade", 12) == 330 and mag.powder_lb == 279.0
    assert len(_lines(w, "guns.filled")) == 1
    # at quarters the filling says nothing, and the report waits until she is out of them
    _at_quarters(w)
    mag.set_filled("carronade", 12, 325)
    mag.report_filled = True
    w.run(15 * 60)
    assert mag.filled_of("carronade", 12) == 330 and mag.report_filled and mag.report_due
    assert len(_lines(w, "guns.filled")) == 1
    quarters_of(w.ship).stand_down()
    w.run(2 * 60)
    filled = _lines(w, "guns.filled")
    assert [e.text for e in filled[1:]] == [
        "The gunner has the cartridges filled to the allowance: 330 for the 12-pounder "
        "carronades; 2 barrels and 74 pounds below."
    ]
    assert not mag.report_filled and not mag.report_due


def test_the_powder_out_is_said_when_the_filling_brings_it_under_the_charges_in_true_words():
    """`guns.powder_out` comes when the minute's filling leaves the powder below under the
    charge of every kind still short, once until powder comes aboard. Powder left over,
    under a long 18's six pounds, is said with the guns it is too little for, and the
    reading agrees; powder put under the charges by hand never fell, and nothing is said."""
    w = _world(FRIGATE)
    q = quarters_of(w.ship)
    mag = magazine(w.ship)
    battery = battery_of(w.ship)
    mag.set_filled("long", 18, 2000)
    mag.powder_lb = 5.0  # under the 18-pounders' charge, as found
    for _ in range(3):
        fill_tick(w, battery, q)
    assert not _lines(w, "guns.powder_out") and mag.filled_by_gunner == 0
    mag.powder_lb = 11.0  # one cartridge of six pounds, and five over
    fill_tick(w, battery, q)  # ten men by day: 600 man-seconds, an 18's cartridge is 210
    assert mag.filled_by_gunner == 1 and mag.powder_lb == 5.0
    spent = _lines(w, "guns.powder_out")
    assert [e.text for e in spent] == [
        "The gunner reports the powder below too little to fill another cartridge for the "
        "long 18-pounders: 5 pounds below, and 53 cartridges short of the allowance."
    ]
    assert spent[0].data == {"short": 53, "powder_lb": 5.0}
    assert spent[0].severity is Severity.NOTABLE
    assert mag.describe()[0].endswith("; too little powder below to fill more.")
    assert mag.describe()[1] == "Powder below: 5 pounds, of 77 barrels established."
    for _ in range(3):
        fill_tick(w, battery, q)
    assert len(_lines(w, "guns.powder_out")) == 1  # once until powder comes aboard


def test_a_magazine_of_packages_70_to_72_resumed_short_says_nothing_of_powder_it_never_had():
    """A store pickled by packages 70 to 72 (three fields, by calibre) after rounds were
    fired is converted with no powder below and is short: the gunner has nothing to fill
    from, so nothing is said, out of quarters or at them. Powder taken in, he fills, and
    its running out is told as for any ship."""
    w = _world()
    old = Magazine.__new__(Magazine)
    old.__dict__.update(
        {
            "cartridges": {12.0: 258},
            "shot": {float(k): dict(v) for k, v in w.ship.fit_spec.shot.items()},
            "fired": {12.0: 72},
        }
    )
    old = pickle.loads(pickle.dumps(old))
    w.ship.extra["magazine"] = old
    lines = len(w.log)
    w.run(5 * 60)  # by day out of quarters
    _at_quarters(w)
    w.run(5 * 60)
    mag = magazine(w.ship)
    assert mag is old and mag.layout == 2 and mag.short and mag.powder_lb == 0.0
    assert mag.filled_of("carronade", 12) == 258 and mag.filled_by_gunner == 0
    assert not _lines(w, "guns.powder_out") and not _lines(w, "guns.filled")
    assert not [e for e in list(w.log)[lines:] if e.kind.startswith("guns.")]
    mag.receive(2.0, when="12 June 1805", words="Two pounds of powder.")
    w.run(6 * 60)
    assert mag.filled_by_gunner == 2 and mag.powder_lb == 0.0
    spent = _lines(w, "guns.powder_out")
    assert [e.text for e in spent] == [
        "The gunner reports all the powder filled: no loose powder below, and 70 cartridges "
        "short of the allowance."
    ]


def test_a_kind_with_no_level_is_never_waited_on_and_its_magazine_is_out_as_today():
    """A gun whose kind has no level in the magazine (a hand-written fit that leaves its
    cartridges out) is one the gunner never fills: it does not wait on him and nothing
    says he is filling, though powder is below; it takes today's path, the magazine out
    in today's words, once."""
    w = _world()
    _guns_ready(w)
    _drawn(w)
    mag = magazine(w.ship)
    mag.level = {}
    mag.set_filled("carronade", 12, 0)
    powder, filled = mag.powder_lb, mag.filled_by_gunner
    assert powder >= 1.0 and not mag.short
    w.run(5 * 60)
    assert not _lines(w, "guns.filling")
    assert [e.text for e in _lines(w, "guns.magazine_empty")] == [OUT_WORDS]
    assert not any(g.loaded for g in w.ship.guns.values())
    assert mag.powder_lb == powder and mag.filled_by_gunner == filled


def test_fill_is_never_called_while_the_magazine_is_full():
    w = _world()
    mag = magazine(w.ship)
    calls: list[float] = []
    real = mag.fill

    def spy(man_seconds: float):
        calls.append(man_seconds)
        return real(man_seconds)

    mag.fill = spy
    w.run(60 * 60)
    _at_quarters(w)
    w.run(10 * 60)
    assert calls == []
    mag.set_filled("carronade", 12, 329)
    w.run(2 * 60)
    assert calls and set(calls) == {60.0}
    del mag.fill


def test_a_battery_and_services_pickled_before_this_build_wait_fill_and_say_the_lines():
    """Built by `__new__` with the attributes of packages 70 to 72 only: every attribute
    of this build is a plain class default, and the battery serves, waits, fills and says
    its lines with them."""
    w = _world()
    _guns_ready(w)
    battery = battery_of(w.ship)
    old = Battery.__new__(Battery)
    state = dict(vars(battery))
    for name in ("exercise", "drill", "last_practice_tick", "_dumb", "_said_filling", "_said_out"):
        state.pop(name, None)
    old.__dict__.update(state)
    services = {}
    for gid, svc in battery.services.items():
        s = Service.__new__(Service)
        s.__dict__.update(
            {"phase": -1, "left_s": 0.0, "stalled": svc.stalled, "said_stalled": False}
        )
        assert s.began_tick is None
        services[gid] = s
    old.services = services
    assert old.exercise is None and old.drill is None and old._said_out is None
    w.ship.extra["battery"] = old
    for g in w.ship.guns.values():
        g.loaded = None
        g.primed = False
        g.run_out = False
    mag = magazine(w.ship)
    mag.set_filled("carronade", 12, 0)
    w.run(10 * 60)
    assert [e.text for e in _lines(w, "guns.filling")] == [WAIT_WORDS]
    assert mag.filled_by_gunner > 0 and any(g.loaded for g in w.ship.guns.values())
    assert old.drill and old._said_filling == {CARR_12}
    assert old.begin_exercise("both") == [g.name for g in w.ship.guns.values() if g.loaded]
    old.end_exercise()
    assert old.exercise is None and old.last_practice_tick is None
    assert all(g.loaded in (None, Charge.ROUND) for g in w.ship.guns.values())
