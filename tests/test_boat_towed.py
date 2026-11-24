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


def _glossed(text: str) -> dict[bool, dict[str, str]]:
    """The served notes' gloss of the boat's marks: {towed: {mark: words}}, of a boat on deck
    (False) and of one towed astern (True), in the marks' order."""
    import re

    gloss = next(p for p in text.split("\n\n") if p.startswith("In its words the game fills"))
    on_deck, towed = re.fullmatch(
        r"In its words the game fills (.*); for a boat towed astern, with (.*)\.", gloss
    ).groups()
    marks = dict(re.findall(r'\{(boat_[a-z]+)\} with "([^"]*)"', on_deck))
    words = re.findall(r'"([^"]*)"', towed)
    assert len(words) == len(marks), gloss
    return {False: marks, True: dict(zip(marks, words, strict=True))}


@pytest.mark.parametrize(
    ("eid", "order"), [("send_boat", "send the boat ashore"), ("lay_out_kedge", "lay out a kedge")]
)
def test_the_boats_evolutions_marks_are_glossed_in_the_words_the_game_fills_them_with(
    tmp_path, eid, order
):
    """The lead's nudge 60: `send_boat` and `lay_out_kedge` serve {boat_out} (and `send_boat`
    {boat_back}) where they served the words, and their served notes gloss each mark in the
    words the game fills it with, of a boat on deck and of one towed astern. Every mark of the
    logged lines but the boat's name is glossed; on the probe with her boat on deck and towed,
    the running script's own words are the gloss's, and the line logged at the start is the
    entry's filled with them. A word changed in the one place and not the other fails here."""
    import re

    from freesail.agents import tools

    evo = load_directory()[eid]
    text = tools._evolution_text(evo)
    logged = next(p for p in text.split("\n\n") if p.startswith("Logged at the start"))
    # {boat} and {boat_cap}, the boat's name, were served before; every other mark is glossed
    marks = [m for m in dict.fromkeys(re.findall(r"\{(boat_[a-z]+)\}", logged)) if m != "boat_cap"]
    glossed = _glossed(text)
    assert marks and list(glossed[False]) == marks and list(glossed[True]) == marks, (eid, marks)
    for towed in (False, True):
        w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path, towed=towed))
        n0 = len(w.log.all())
        assert w.submit(order).kind == "order.accepted"
        w.run(2)
        (inst,) = [i for i in w.ship.extra["evolutions"].instances if i.evo.id == eid]
        words = inst.script.words()
        expected = {m: glossed[towed][m].replace("{boat}", words["boat"]) for m in marks}
        assert {m: words[m] for m in marks} == expected, (eid, towed)
        started = [e.text for e in w.log.all()[n0:] if e.kind == "evolution.started"]
        assert started == [evo.on_start.log.format_map({**words, **expected})], (eid, towed)


# ---------------------------------------------------------------------------
# The lateen hulls' list as it stands (the lead's nudge 60), item 8: the boat in tow
# ---------------------------------------------------------------------------


def test_a_boat_towed_faster_than_her_hull_speed_is_said_to_sheer_and_ship_water(tmp_path):
    """Nudge 60, item 8: an hour running at up to 11.75 kn, the yawl's hull speed 5.4, and no
    word; still "towing astern on her painter". Her drag past her hull speed is the wave term
    carried on beyond its ground (`physics.integrate.TOW_WAKE_FACTOR`'s note), not changed; the
    words say what a boat so towed does, once as she passes it (`boats.TOWED_TOO_FAST`), and the
    reading with them. Measured, seed 7, the probe running in 45 kn under her mainsail: said at
    6 s, once in the hour (her way at most 11.28 kn); the probe as filed, her boat on deck,
    never."""
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=45.0,
        gustiness=0.3,
        variability=0.3,
        ship_heading_deg=180.0,
        ship_speed_kn=5.0,
    )
    said = {}
    for towed in (True, False):
        w = make_world(7, _probe(tmp_path, towed=towed), sc)
        n0 = len(w.log.all())
        w.submit("set the mainsail")
        w.run(3600)
        said[towed] = [e for e in w.log.all()[n0:] if e.kind == "boat.towed_too_fast"]
        if towed:
            assert w.readings.words("boat") == (
                "the boat towing astern on her painter, sheering about and shipping water"
            )
    assert [e.text for e in said[True]] == [
        "The boat towing too fast for her, sheering about astern on her painter and shipping "
        "water; shorten sail to ease her."
    ]
    hull = load_ship("data/ships/boat-yawl-16.yaml").hull
    assert said[True][0].data["knots"] > said[True][0].data["hull_speed_kn"]
    assert said[True][0].data["hull_speed_kn"] == pytest.approx(
        hull.hull_speed / 0.514444, abs=0.01
    )
    assert said[False] == []


@pytest.mark.parametrize("u", [-1.5, 1.5])
def test_making_sternway_her_boat_in_tow_drags_nothing(tmp_path, u):
    """Nudge 60, item 8: no case held that she drags nothing making sternway (her painter slack:
    `physics.integrate`, the way ahead alone). In a calm with no sail set and the same way put on
    her, astern her way falls off tick for tick as the probe's with her boat on deck; ahead it
    falls off faster, by the boat's drag."""
    ways = {}
    for towed in (True, False):
        w = at_rest(50.0, -4.0, ship=_probe(tmp_path, towed=towed))
        w.run(2)
        assert ("boat_in_tow" in w.ship.extra) is towed
        w.ship.dyn.u = u
        seen = []
        for _ in range(30):
            w.tick()
            seen.append(w.ship.dyn.u)
        ways[towed] = seen
    if u < 0:
        assert ways[True] == ways[False]
    else:
        assert all(a < b for a, b in zip(ways[True], ways[False], strict=True))


@pytest.mark.parametrize("eid", ["send_boat", "lay_out_kedge"])
def test_a_towed_boats_two_timings_are_the_ports_figures(eid):
    """Nudge 60, item 8: no case held `ports.BOAT_HAUL_ALONGSIDE_S` (nor its pair) against the
    evolutions' timing, which the scripts read first (`scripts._boat_out_s`, `_boat_in_s`)."""
    from freesail.world import ports

    timing = load_directory()[eid].timing
    assert timing["haul_alongside_s"] == ports.BOAT_HAUL_ALONGSIDE_S
    assert timing["veer_astern_s"] == ports.BOAT_VEER_ASTERN_S


def test_a_boat_towed_too_fast_is_said_at_her_hull_speed_and_again_only_under_nine_tenths():
    """Nudge 76, item 4: the towed boat's threshold and re-arming at their figures
    (`boats.TOWED_TOO_FAST_REARM`): said as the ship's way passes the boat's hull speed, not
    again while it stays over nine tenths of it, and again once it has fallen under that and
    risen past her hull speed once more; nothing at her hull speed itself."""
    from types import SimpleNamespace

    hull = load_ship("data/ships/boat-yawl-16.yaml").hull
    v = hull.hull_speed
    boat = SimpleNamespace(id="boat")
    notes = []
    ship = SimpleNamespace(dyn=SimpleNamespace(u=0.0), note=lambda *a: notes.append(a), extra={})
    state = SimpleNamespace(boat_name="the boat")
    said = []
    for u in (v, 1.01 * v, 1.2 * v, 0.95 * v, 1.05 * v, 0.89 * v, 0.95 * v, 1.01 * v):
        ship.dyn.u = u
        B._towed_too_fast(ship, ship.extra, [(boat, hull)], state)
        said.append(len(notes))
    assert B.TOWED_TOO_FAST_REARM == 0.9
    assert said == [0, 1, 1, 1, 1, 1, 1, 2]
    assert notes[0][1] == "boat.towed_too_fast"


def _stove(w) -> None:
    """A shot amidships on her deck, the boats' share drawn (`combat.hits._deck_hit`)."""
    from types import SimpleNamespace

    from freesail.combat import hits

    class _Draw:
        def random(self):
            return 0.0

    keeper = SimpleNamespace(minute=[])
    hits._deck_hit(
        w.ship, keeper, None, None, None, 0.0, "starboard", 1.0, False, _Draw(), w.clock.tick
    )


def test_a_boat_towed_astern_stove_by_a_shot_is_cut_adrift_not_on_the_booms(tmp_path):
    """Nudges 76 and 77, item 3 and item 1: a boat towed astern was "stove on the booms by a
    shot" and stayed in tow; then, cut adrift, she was still sent ashore, laid out the kedge and
    was gone to. Stove where she tows (`combat.hits._deck_hit`, its draw the boats' as before),
    she fills and her painter is cut, and she is lost by the road a boat swamped or cut adrift
    takes (`boats.stove_in_tow`, `lose_boat`): in tow no longer, used by nobody, and said so.
    The hit's data carries `towed`. The probe as filed, her boat on deck, is stove on the booms
    as before, and not lost."""
    said, data = {}, {}
    for towed in (True, False):
        w = at_anchor_in(CARRICK_ROAD, ship=_probe(tmp_path, towed=towed))
        assert ("boat_in_tow" in w.ship.extra) is towed
        n0 = len(w.log.all())
        _stove(w)
        w.run(2)
        stove = [e for e in w.log.all()[n0:] if e.kind == "boat.stove"]
        said[towed] = [e.text for e in stove]
        data[towed] = stove[0].data
        assert "boat_in_tow" not in w.ship.extra
        assert bool(w.dealings.boat.lost) is towed
        if towed:
            lost = [e.text for e in w.log.all()[n0:] if e.kind == "boat.lost"]
            assert lost == [
                "The boat stove by a shot as she towed astern, and cut adrift. A new one is the "
                "yard's."
            ]
            assert w.readings.words("boat").startswith("the boat lost: stove on the ")
            for order in ("send the boat ashore", "lay out a kedge", "go to the boat"):
                assert w.submit(order).kind == "order.rejected", order
    assert said == {
        True: [
            "The boat is stove by a shot as she tows astern; she fills, and her painter is cut."
        ],
        False: ["The boat is stove on the booms by a shot."],
    }
    assert data == {True: {"boat": "boat", "towed": True}, False: {"boat": "boat"}}


def test_clearing_for_action_her_boat_lost_says_no_boat_out(tmp_path):
    """Nudge 77, item 1: `clear for action` said "The boats are out and towing astern" of a ship
    whose boat was stove and cut adrift. Her boat lost, the line says so (the tartane probe
    carries two, the other on the booms); with it, as before (that it says so of a boat left on
    the booms is the trunk's, older)."""
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=270.0,
        ship_speed_kn=5.0,
    )
    said = {}
    for stove in (True, False):
        w = make_world(7, _probe(tmp_path), sc)
        w.submit("set plain sail")
        w.run(600)
        if stove:
            _stove(w)
            w.run(2)
        n0 = len(w.log.all())
        assert w.submit("clear for action").kind == "order.accepted"
        w.run(900)
        said[stove] = [e.text for e in w.log.all()[n0:] if "the ship is clear" in e.text.lower()]
    assert said == {
        True: [
            "The rest of her boats are out and towing astern, the boat lost; the ship is clear."
        ],
        False: ["The boats are out and towing astern; the ship is clear."],
    }


def test_of_two_boats_towed_each_is_in_tow_and_one_stove_leaves_the_other(tmp_path):
    """Nudge 77, item 4: two boats towed astern, each her own hull's drag on the ship; the one
    that is not the errands' boat stove by a shot leaves the tow, and the other stays in it, the
    ship's boat not lost."""
    import copy

    doc = tartane_probe_doc()
    doc["boats"][0]["towed"] = True
    second = copy.deepcopy(doc["boats"][0])
    second["id"] = "boat2"
    second["name"] = "the jolly boat"
    doc["boats"].append(second)
    w = at_anchor_in(CARRICK_ROAD, ship=str(write_ship(doc, tmp_path, "tartane-two")))
    assert len(w.ship.extra["boat_in_tow"]) == 2
    w.ship.extra.setdefault("boats_stove", []).append("boat2")
    w.run(2)
    assert len(w.ship.extra["boat_in_tow"]) == 1
    assert not w.dealings.boat.lost
    assert w.readings.words("boat") == "the boat towing astern on her painter"


# ---------------------------------------------------------------------------
# The third pass's changes on ships in the game (the lead's nudge 79): declared and pinned
# ---------------------------------------------------------------------------


def test_on_a_committed_ship_a_lost_boat_lays_out_no_kedge(tmp_path):
    """Nudge 79, the declaration: on every committed ship with a boat, `lay out a kedge` with her
    boat lost was taken, and the boat cut adrift hoisted out and laid it out (the frigate's launch:
    "Hoist out the launch; the kedge and a hawser into her.", the kedge let go 775 s on). Now it
    is refused at the order, as a lost boat is sent on no errand."""
    w = at_anchor_in(CARRICK_ROAD)
    assert w.submit("cut the boat adrift").kind != "order.rejected"
    w.run(1)
    r = w.submit("lay out a kedge")
    assert r.kind == "order.rejected"
    assert r.text.startswith("Order not carried out ('lay out a kedge'): the launch is lost: ")


def test_on_a_committed_ship_clearing_for_action_with_her_boat_lost(tmp_path):
    """Nudge 79, the declaration: `clear for action` said "The boats are out and towing astern;
    the ship is clear." with her boat cut adrift. Now the boat lost is said, by her name."""
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=270.0,
        ship_speed_kn=5.0,
    )
    w = make_world(7, "data/ships/brig.yaml", sc)
    w.submit("set plain sail")
    w.run(600)
    w.submit("cut the boat adrift")
    w.run(1)
    n0 = len(w.log.all())
    w.submit("clear for action")
    w.run(1200)
    said = [e.text for e in w.log.all()[n0:] if "the ship is clear" in e.text.lower()]
    assert said == [
        "The rest of her boats are out and towing astern, the launch lost; the ship is clear."
    ]
