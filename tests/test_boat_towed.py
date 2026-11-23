"""Package 90, A4: the boat in tow.

A boat's `towed` (stage 0's key, which no committed file carries) is a boat towed astern on her
painter, not stowed on deck. She is not hoisted out: she is hauled up alongside by the painter
and manned at the gangway, with a little way on the ship (three knots, against a hoisting out's
two); manned, she lies astern on her painter, not off the lee quarter; and back alongside she
is veered astern on it again, not hoisted in. Her errands (`send the boat ashore`, the kedge),
her manning as a hull (`go to the boat`), the tow with her and her coming alongside say so, and
take a minute each way where the yard and stay tackles take five. While she is in tow her drag
is on the ship (`physics.integrate.step`, the trawl's road): her own resistance at the ship's
speed times `TOW_WAKE_FACTOR`; nothing while she is away, and nothing on a ship whose file tows
no boat. Every changed line stands behind `towed`; the figures are JUDGEMENT
(docs/dev/TuningNotes.md, "Package 90, A4"). Measured on the tartane probe (`cutter.yaml` rigged
as a tartane), her 15-ft boat on the 16-ft yawl's file.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from rig_fixtures import tartane_probe_doc, write_ship

from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions.registry import load_directory
from freesail.physics import hull as hp
from freesail.physics.integrate import TOW_WAKE_FACTOR
from freesail.ship.loader import load_ship
from freesail.world import boats as B
from freesail.world.geo import bearing_and_distance
from freesail.world.ports import BoatState
from tests.test_ports import CARRICK_ROAD, OFF_THE_LIZARD, at_anchor_in, world_at
from tests.test_reckoning import at_rest

SHIP_FILES = sorted(Path("data/ships").glob("*.yaml"))


def _probe(tmp_path, towed: bool = True) -> str:
    """The tartane probe, her boat towed astern (or, `towed` false, as filed: on deck)."""
    doc = tartane_probe_doc()
    if towed:
        doc["boats"][0]["towed"] = True
    return str(write_ship(doc, tmp_path, "tartane-towed" if towed else "tartane"))


def _phases(w, until_home: int = 7200) -> list[tuple[int, str]]:
    """The boat's phases as they change, by the seconds from now, until she is home."""
    t0, out = w.clock.tick, []
    for i in range(until_home):
        w.tick()
        phase = w.dealings.boat.phase
        if not out or out[-1][1] != phase:
            out.append((w.clock.tick - t0, phase))
        if i > 10 and not w.dealings.boat.away:
            break
    return out


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_no_committed_file_tows_a_boat_so_no_ship_is_given_her_drag(path):
    """The guard: a ship whose file tows no boat is never given `boat_in_tow`, at home or with
    her boat away or lost, so nothing of the eighteen files moves by the tow's drag."""
    ship = load_ship(path)
    ship.extra = {}
    for state in (BoatState(), BoatState(away=True, boat_id="boat"), BoatState(lost="stove")):
        B.keep_in_tow(ship, state)
        assert "boat_in_tow" not in ship.extra


def test_a_towed_boat_lies_astern_on_her_painter_and_her_drag_is_on_the_ship(tmp_path):
    """At anchor her boat is "towing astern on her painter", not "at the booms", and her hull
    (the yawl's file) is the ship's `boat_in_tow`; the probe as filed, her boat on deck, is as
    she was."""
    w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path))
    assert w.readings.words("boat") == "the boat towing astern on her painter"
    hull = load_ship("data/ships/boat-yawl-16.yaml").hull
    in_tow = w.ship.extra["boat_in_tow"]
    assert len(in_tow) == 1 and in_tow[0].wetted_area == hull.wetted_area
    filed = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path, towed=False))
    assert filed.readings.words("boat") == "the boat at the booms"
    assert "boat_in_tow" not in filed.ship.extra


def test_sent_ashore_she_is_hauled_alongside_and_veered_astern_on_her_painter_again(tmp_path):
    """Measured, seed 7, Carrick Road: hauled up alongside and away in 56 s where the probe's
    boat on deck is hoisted out in 283 s, and veered astern again in 58 s where she is hoisted
    in in 290 s; the errand 4,581 s against 5,040. Away, her drag is off the ship."""
    w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path))
    n0 = len(w.log.all())
    assert w.submit("send the boat ashore").kind == "order.accepted"
    phases = _phases(w)
    assert phases == [
        (1, "hauling alongside"),
        (57, "pulling for the shore"),
        (1390, "at the quay"),
        (3190, "pulling back to the ship"),
        (4523, "alongside, veering astern"),
        (4581, ""),
    ]
    lines = [(e.kind, e.text) for e in w.log.all()[n0:] if e.kind.startswith("boat")]
    assert lines[-2:] == [
        (
            "boat.alongside",
            "The boat alongside from the shore and veered astern on her painter again.",
        ),
        ("boat.in", "The boat veered astern on her painter again."),
    ]
    started = [e.text for e in w.log.all()[n0:] if e.kind == "evolution.started"]
    assert started == ["Away the boat's crew! Haul the boat up alongside."]
    assert "boat_in_tow" in w.ship.extra
    filed = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path, towed=False))
    filed.submit("send the boat ashore")
    assert [t for t, _ in _phases(filed)] == [1, 284, 1617, 3417, 4750, 5040]


def test_away_on_her_errand_she_puts_no_drag_on_the_ship(tmp_path):
    """The key is gone from the moment she is hauled alongside till she is veered astern
    again (`keep_in_tow`, each tick)."""
    w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path))
    w.submit("send the boat ashore")
    w.run(2)
    assert w.dealings.boat.phase == "hauling alongside" and "boat_in_tow" not in w.ship.extra
    w.run(1800)
    assert w.dealings.boat.away and "boat_in_tow" not in w.ship.extra


def test_the_kedge_is_laid_out_by_a_towed_boat_hauled_alongside_for_it(tmp_path):
    """Measured, seed 7, Carrick Road: hauled alongside in 82 s where the boat on deck is
    hoisted out in 412 s (her hands short), the kedge slung in her as before, and veered astern
    again in 83 s against 413; the kedge laid out in 739 s against 1,399."""
    w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path))
    n0 = len(w.log.all())
    assert w.submit("lay out a kedge to the NE").kind == "order.accepted"
    assert _phases(w) == [
        (1, "hauling alongside"),
        (83, "the kedge slinging"),
        (496, "pulling out with the kedge"),
        (576, "pulling back"),
        (656, "alongside, veering astern"),
        (739, ""),
    ]
    started = [e.text for e in w.log.all()[n0:] if e.kind == "evolution.started"]
    assert started == ["Haul the boat up alongside; the kedge and a hawser into her."]
    assert any(e.kind == "ship.kedged" for e in w.log.all()[n0:])
    filed = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path, towed=False))
    filed.submit("lay out a kedge to the NE")
    assert [t for t, _ in _phases(filed)] == [1, 413, 826, 906, 986, 1399]


@pytest.mark.parametrize("knots", [2.5, 3.5])
def test_she_is_manned_from_alongside_with_a_little_way_on_her(tmp_path, knots):
    """With 2.5 knots of way a boat on deck is not hoisted out; a towed boat is hauled
    alongside and manned, and lies astern on her painter. With 3.5 knots neither is."""
    w = world_at(OFF_THE_LIZARD, ship=_probe(tmp_path), heading=0.0, speed=knots, wind_kn=0.0)
    w.run(2)
    e = w.submit("go to the boat")
    if knots < 3.0:
        assert e.kind == "person.aboard"
        assert e.text.startswith(
            "The boat hauled alongside and manned: her coxswain and 4 oarsmen in her, lying "
            "astern on her painter by "
        )
    else:
        assert e.kind == "order.rejected"
        assert e.text.endswith(
            "She has 3.4 knots of way on her; heave to or shorten sail before the boat is "
            "hauled alongside and manned."
        )
    filed = world_at(
        OFF_THE_LIZARD, ship=_probe(tmp_path, towed=False), heading=0.0, speed=knots, wind_kn=0.0
    )
    filed.run(2)
    e = filed.submit("go to the boat")
    assert e.kind == "order.rejected" and "before the boat is hoisted out." in e.text


def test_manned_she_lies_astern_and_comes_alongside_to_be_veered_astern_again(tmp_path):
    """Manned at rest she lies 12 m astern of the ship (the probe's head north: she bears
    south), where the boat on deck is put off the lee quarter; alongside again she is veered
    astern on her painter, her people aboard, and her drag on the ship once more."""
    w = at_rest(49.6, -5.2, ship=_probe(tmp_path))
    ship = w.players
    e = w.submit("go to the boat")
    assert "lying astern on her painter" in e.text
    brg, dist = bearing_and_distance(ship.position, w.own.position)
    assert round(dist, 1) == B.TOWED_ASTERN_M and round(brg) % 360 == 180
    w.run(60)
    assert "boat_in_tow" not in ship.ship.extra
    e = w.submit("come alongside")
    assert e.text == "The Sherbourne's boat veered astern on her painter again; her people aboard."
    lines = [x.text for x in ship.log.all() if x.kind == "boat.hoisted_in"]
    assert lines[-1].startswith(
        "The Sherbourne's boat alongside and veered astern on her painter again, "
    )
    w.run(1)
    assert "boat_in_tow" in ship.ship.extra


def test_the_tow_with_her_hauls_her_alongside_and_she_is_off_the_ship_ahead(tmp_path):
    """`tow her with the boat`: hauled alongside and manned for the tow, ahead on the line and
    no drag astern while she tows; `the boat alongside` veers her astern again."""
    w = at_rest(49.6, -5.2, ship=_probe(tmp_path))
    e = w.submit("tow her with the boat to the NE")
    assert e.kind == "boat.towing"
    assert e.text.startswith("The boat hauled alongside and manned for the tow, ")
    w.run(600)
    assert "boat_in_tow" not in w.ship.extra
    e = w.submit("the boat alongside")
    assert e.text == "The Sherbourne's boat veered astern on her painter again; her people aboard."
    w.run(60)
    assert "boat_in_tow" in w.ship.extra


def _reach(path: str, knots: float) -> tuple[float, object]:
    """The probe on a beam reach (the wind from 0, her head 270), plain sail trimmed every two
    minutes after five, seed 7: her mean way over the last 600 s of 2,400, in knots."""
    w = make_world(
        7,
        path,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=knots,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=270.0,
            ship_speed_kn=5.0,
        ),
    )
    w.submit("set plain sail")
    w.run(120)
    way = []
    for i in range(2400):
        if i % 120 == 0 and i > 300:
            w.submit("trim sails")
        w.tick()
        if i >= 1800:
            way.append(w.ship.dyn.u)
    return sum(way) / len(way) / 0.514444, w


def test_her_boat_in_tow_takes_its_own_resistance_in_the_wake_off_her_way(tmp_path):
    """Measured, seed 7, the probe on a beam reach in 15 kn: 7.23 kn with her boat on deck and
    7.00 with it in tow; the boat's drag there 905 N, the yawl's resistance at her speed times
    0.6, beside the probe's own 8,855 N (TuningNotes has 8 and 25 kn and the other points)."""
    filed, _ = _reach(_probe(tmp_path, towed=False), 15.0)
    towing, w = _reach(_probe(tmp_path), 15.0)
    assert (round(filed, 2), round(towing, 2)) == (7.23, 7.0)
    yawl = w.ship.extra["boat_in_tow"][0]
    u = towing * 0.514444
    assert round(-hp.resistance(yawl, u) * TOW_WAKE_FACTOR) == pytest.approx(905, abs=5)


def test_a_checkpoint_of_her_with_her_boat_in_tow_sails_on_the_same(tmp_path):
    """Her boat's hull is pickled with the ship's `extra` (a class the checkpoint admits
    already, `ship.parts.Hull`), and the copy sails on as she does."""
    _, w = _reach(_probe(tmp_path), 8.0)
    copy = replay.trial_copy(w, raising=True)
    assert "boat_in_tow" in copy.ship.extra
    w.run(120)
    copy.run(120)
    assert copy.ship.dyn.u == w.ship.dyn.u and copy.ship.dyn.heading == w.ship.dyn.heading


def test_the_boats_evolutions_tell_the_player_of_a_towed_boat_in_the_games_own_words():
    """The library serves the files' notes: the towed boat's paragraph names no package, step
    or design document."""
    from freesail.agents import tools

    evolutions = load_directory()
    for eid in ("send_boat", "lay_out_kedge"):
        text = tools._evolution_text(evolutions[eid])
        para = next(p for p in text.split("\n\n") if p.startswith("A boat towed astern"))
        assert "hauled up alongside" in para and "veered astern" in para
        for word in ("package", "Package", "A4", "Design", "docs/", "JUDGEMENT"):
            assert word not in para, (eid, word)
