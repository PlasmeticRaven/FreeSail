"""The things found aboard, widened (the director's `aboard:` table,
`data/director/aboard.yaml`; spec M7b §3): slots for a sail, a line, an anchor and a good
beside the spar; effects on the sails, the rigging, the cable, the water and the
provisions by share, the cargo struck off with its cause, the spare canvas and cordage, the
chronometer and the glass; every condition of a thing's `plausible_when` held together,
with the days since she watered, the mean wind and the anchor among them; a thing whose
effect wants what she lacks answered "no way as said"; the water found foul made sweet
again by watering. Proven on the frigate at seed 7 off the Lizard (`tests.test_brains.
world_at`), never a model."""

from __future__ import annotations

import pytest

from freesail.agents import director as D
from freesail.api import readings as R
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.ship.parts import cordage, ground_tackle, sail_room
from freesail.world import orders as WO
from tests.test_brains import world_at

CHRONOMETER = {
    "maker": "Earnshaw",
    "where": "Plymouth",
    "rated": "1805-04-26",
    "rate_s_per_day": 1.8,
    "drift": 0.0,
}


def found(w, text: str, done: bool = True):
    """The order given with a reason (past the doubt), as the director's door would; done,
    unless the test says it is to be refused."""
    e = w.world_order(f"aboard: {text} [reason: the test]", "the test")
    assert (e.data["result"] == "done") is done, (text, e.text)
    return e


def reports(w):
    return [e for e in w.log.all() if e.kind == "aboard.found"]


def test_every_thing_of_the_table_is_read_and_each_form_finds_its_own_thing():
    """The table loads with known keys only; each form, its slot filled by a name the
    frigate has, finds its own thing and no other."""
    table = WO.aboard_table()
    # package 70: the guns' two; package 73: the people's health, five; package 82: the boat's
    # three (stove, swamped, gone adrift)
    assert len(table) == 34
    assert set(WO._PLAUSIBLE) == WO.ABOARD_PLAUSIBLE_KEYS
    w = world_at(49.5, -5.5)
    w.hold.stow("tin", 10.0)
    fill = {
        "spar": "the fore topmast",
        "sail": "the fore topsail",
        "line": "the starboard main brace",
        "anchor": "the best bower",
        "good": "tin",
        "gun": "No. 3 starboard gun",  # package 70: a gun by the gun deck's words
        "person": "the first lieutenant",  # package 73: a person by his role or his name
    }
    for thing in table:
        for form in thing["words"]:
            said = WO._SLOT.sub(lambda m: fill[m.group(1)], form)
            got = WO._aboard_match(w, f"aboard: {said}")
            assert got is not None and got[0]["id"] == thing["id"], (form, got)


def test_a_key_the_game_does_not_know_is_the_tables_mistake_said_at_the_load(tmp_path):
    for body, said in (
        ("effect: {sail_condtion: 40}", "effect has no key sail_condtion"),
        ("plausible_when: {at_ancor: true}", "plausible_when has no key at_ancor"),
        ("effect: {sail_condition: 40}", "wants every form to name the {sail}"),
    ):
        path = tmp_path / f"t{abs(hash(body))}.yaml"
        path.write_text(
            f'things:\n  - id: x\n    words: ["a thing found"]\n    {body}\n', encoding="utf-8"
        )
        with pytest.raises(ValueError, match=said.replace("{", r"\{").replace("}", r"\}")):
            WO.aboard_table(str(path))


def test_the_sails_the_rigging_and_the_cable_are_cut_by_name_and_said_by_their_people():
    w = world_at(49.5, -5.5)
    sid = WO._part_by_name(w.ship, "the fore topsail", "sails")
    lid = WO._part_by_name(w.ship, "the main brace", "lines")  # the first of the pair
    assert sid is not None and lid is not None
    e = found(w, "the fore topsail found mildewed")
    assert e.data["result"] == "done" and "the fore topsail mildewed (its condition 45)" in e.text
    assert w.ship.parts[sid].condition == 45.0
    found(w, "the main brace found stranded")
    assert w.ship.parts[lid].condition == 35.0
    found(w, "the best bower cable found chafed in the hawse")
    best = next(a for a in ground_tackle(w.ship).anchors if a.id == "best_bower")
    assert best.cable_condition == 40.0
    found(w, "the sheet anchor cable found chafed")
    sheet = next(a for a in ground_tackle(w.ship).anchors if a.id == "sheet")
    assert sheet.cable_condition == 40.0
    found(w, "the main topmast found rotten")
    assert w.ship.parts[WO._spar_by_name(w.ship, "the main topmast")].condition == 50.0
    texts = [e.text for e in reports(w)]
    assert texts[0].startswith("The sailmaker reports the fore topsail mildewed")
    assert texts[2].startswith("The boatswain reports the best bower's cable chafed")
    assert all(e.severity.value == "notable" for e in reports(w))
    # a condition is only ever cut: a second finding above it changes nothing
    w.ship.parts[sid].condition = 20.0
    found(w, "the fore topsail found chafed")
    assert w.ship.parts[sid].condition == 20.0


def test_the_stores_the_cargo_and_the_spare_gear_fall_by_their_share_with_the_cause():
    w = world_at(49.5, -5.5)
    w.hold.stow("tin", 20.0)
    water, days = w.stores.water_tons, w.stores.provisions_days
    found(w, "the leaguers found leaking")
    assert w.stores.water_tons == pytest.approx(water * 0.85)
    found(w, "the biscuit found mouldy")
    assert w.stores.provisions_days == pytest.approx(days * 0.92)
    found(w, "rats found in the bread room")
    assert w.stores.provisions_days == pytest.approx(days * 0.92 * 0.97)
    e = found(w, "the tin found damaged by the bilge water")
    assert e.data["result"] == "done" and "2 tons of tin struck off" in e.text
    assert w.hold.goods["tin"] == pytest.approx(18.0)
    assert "2 tons of tin struck off the manifest, found damaged by the bilge water." in (
        w.hold.lines()
    )
    fathoms = cordage(w.ship).fathoms
    found(w, "rats found at the cordage")
    assert cordage(w.ship).fathoms == pytest.approx(fathoms * 0.75)
    found(w, "the spare canvas found mildewed")
    assert all(s.condition <= 60.0 for s in sail_room(w.ship).sails)
    # a good she has none of is no form: the words are answered as the channel's own
    e = found(w, "the brandy found wet", done=False)
    assert e.data["result"] == "refused"


def test_a_report_only_thing_says_its_own_words_of_what_is_not_modelled():
    w = world_at(49.5, -5.5)
    # package 73: a seam found working is a leak the keeper runs; the bilge is the report-only
    assert "nothing of the bilge" in found(w, "the bilge found foul").text
    e = found(w, "the compass found sticking")
    assert "nothing of the compass's error is modelled yet" in e.text
    assert reports(w)[-1].data["report_only"]


def test_the_chronometer_found_stopped_is_dead_by_its_cause_and_set_going_by_the_account():
    w = world_at(49.5, -5.5, chronometer=CHRONOMETER, instrument="sextant")
    c = w.navigation.chronometer
    e = found(w, "the chronometer found stopped")
    assert e.data["result"] == "done" and not c.going
    assert "is dead, stopped by a jar in a heavy sea" in c.words(w)
    assert "already" in found(w, "the chronometer found stopped", False).text
    w.navigation.wind_chronometer()
    assert c.going and not c.stopped
    # a ship with none: the game has no way to do it as said, and the director is told so
    bare = world_at(49.5, -5.5)
    D.direct(bare, "aboard: the chronometer found stopped", by="t")  # the doubt seen (68)
    said = D.direct(bare, "aboard: the chronometer found stopped [reason: the test]", by="t")
    assert said.startswith("Logged as attempted") and "she carries no chronometer" in said


def test_the_glass_found_broken_is_gone_from_the_readings_and_stays_gone_in_a_replay():
    w = world_at(49.5, -5.5, systems=[], climatology=True, glass=True)
    assert w.glass is not None
    e = found(w, "the glass found broken")
    assert e.data["result"] == "done" and w.glass is None
    assert R._no_glass_words(w) == R.GLASS_BROKEN_WORDS
    assert "broken already" in found(w, "the glass found broken", False).text
    w.run(600)
    back = replay.replay_world(w, ship_factory)
    assert back.glass is None and back.log.digest() == w.log.digest()


def test_every_condition_must_hold_and_the_new_ones_read_the_ship(monkeypatch):
    """`plausible_when` is read whole: a thing whose conditions all hold is not doubted,
    and one failing among them doubts it; `at_anchor`, `wind_above` and
    `days_since_watered` read the ship."""
    w = world_at(49.5, -5.5)  # at sea, under way, fourteen knots of wind
    cable = WO.parse("aboard: the best bower cable found chafed")
    assert "rides at no anchor" in WO.doubt(w, cable)
    # the water foul by the days since she watered, not since the voyage began
    foul = WO.parse("aboard: the water found foul")
    assert "casks do not foul" in WO.doubt(w, foul)
    w.stores.watered_tick = w.clock.tick - 6 * 86400
    assert WO.doubt(w, foul) is None
    w.run(600)
    table = [
        {
            "id": "both",
            "words": ["a thing of two conditions found"],
            "effect": {"report_only": True},
            "plausible_when": {"wind_above": 10, "at_anchor": False},
            "doubt": "no cause",
        },
        {
            "id": "either",
            "words": ["a thing of a fresh wind found"],
            "effect": {"report_only": True},
            "plausible_when": {"wind_above": 10, "at_anchor": True},
            "doubt": "not at anchor",
        },
        {
            "id": "gale",
            "words": ["a thing of a gale found"],
            "effect": {"report_only": True},
            "plausible_when": {"wind_above": 30},
            "doubt": "no gale",
        },
    ]
    monkeypatch.setattr(WO, "aboard_table", lambda path=None: table)
    assert WO.doubt(w, WO.parse("aboard: a thing of two conditions found")) is None
    assert WO.doubt(w, WO.parse("aboard: a thing of a fresh wind found")) == "not at anchor"
    assert WO.doubt(w, WO.parse("aboard: a thing of a gale found")) == "no gale"


def test_watering_makes_the_foul_water_sweet_and_counts_the_days_afresh():
    from tests.test_ports import CARRICK_ROAD, at_anchor_in, run_until

    w = at_anchor_in(CARRICK_ROAD, cargo={"purse_pounds": 500.0})
    found(w, "the water found foul")
    w.stores.water_tons -= 10.0
    assert w.stores.foul and w.stores.watered_tick == 0
    assert w.submit("take in water").kind == "yard.demanded"
    done = run_until(w, "yard.done", 120)
    assert "the foul water started overboard and the casks filled sweet" in done.text
    assert not w.stores.foul and w.stores.watered_tick == done.tick
    assert "found foul" not in w.stores.words()
    assert "casks do not foul" in WO.doubt(w, WO.parse("aboard: the water found foul"))


def test_a_found_thing_is_the_same_after_a_replay():
    w = world_at(49.5, -5.5, cargo={"goods": {"tin": 10.0}})  # the scenario's, so replayed
    for text in ("the fore topsail found mildewed", "the bread found damp", "the tin found wet"):
        assert found(w, text).data["result"] == "done"
    w.run(300)
    back = replay.replay_world(w, ship_factory)
    assert back.log.digest() == w.log.digest()
    sid = WO._part_by_name(w.ship, "the fore topsail", "sails")
    assert back.ship.parts[sid].condition == w.ship.parts[sid].condition == 45.0
    assert back.stores.provisions_days == pytest.approx(w.stores.provisions_days)
    assert back.hold.goods == w.hold.goods
