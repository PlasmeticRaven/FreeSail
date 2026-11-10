"""Package 75, the engine's settee step (B3.3; docs/design/Design-ShipsEngineExtensions.md §5,
§10.2): the bilander's main, a dipping lug with the key `settee`, set and clewed up as a square
sail and dipped round its mast as a lug (D1(a), D2(a); Lescallier 1791 p. 390).

The one key routes it (Ext §5.2): its own set, take in, furl and dip (`set_settee`,
`take_in_settee`, `furl_settee`, `dip_settee`), the lug's reef, trim, bend, unbend and shift.
Clewed up it hangs in its gear with its yard aloft (`Sail.yard_lowered` false); only a dip lowers
the yard. It is kept off every lugger's path (Ext §5.4): she gets under way as a ship and sets it
after the cast as her after sail, she has no storm lug, and the lugger's dip and lowering never
take it. In stays it is kept drawing as a ship's mizen and changed last, once the head yards are
swung (D3(b), Ext §5.5); in wearing it is lowered as she bears up and hoisted on the new lee once
the wind is past the stern (D46(d) rule 4 as reworded, Ext §5.6); hove to her main topsail goes to
the mast by her file's `heave_to_aback` (D4(a)), the settee kept with its sheet eased by the
engine's driver rule, which the lead's ruling on Ext §14 item 3 holds for it unless the figures
say otherwise (Ext §5.7; the figures both ways in docs/dev/TuningNotes.md, "The settee in the
engine"); forced round so through the wind and filled away, a settee left on her weather side is
dipped first, as she lies (B3.3b, the bilander's design §17 lead item 8), her tack read for it from
the wind at the first tick, and belayed meanwhile it is said to be left on deck (B3.3b's review). In
the gale it is one of her courses (E15): reefed with the topsails' second reef, taken in with their
third. Its sheet's block is a fathom abaft its clew by its own corners (Ext §5.9; the lead's ruling
on the bilander's §17 lead item 4).

None of the committed files carries a settee (`tests/test_rig_classing.py`, the probe), so the
tests run on the fixture `brig_with_settee()` (`tests/rig_fixtures.py`, stage 0E): `brig.yaml`
with her main course, spanker, gaff and boom replaced by a settee cut to D5(a)'s proportions, the
dry main yard and the main topsail above it, the main laid aback to heave to. The bilander's own
file is B4's; her measures there are hers (her design §12.2). Two truths are drafted here for
Phase 5, 7-198 and 7-199 (`docs/design/Build-Ships.md` §15), measured on the fixture and to be
measured again on her file.
"""

from __future__ import annotations

import math
import random
from datetime import datetime
from types import SimpleNamespace

import pytest
from rig_fixtures import brig_with_settee, brig_with_settee_doc, write_ship

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import hands
from freesail.crew.model import Crew, Rating, Sailor, Station, Watch
from freesail.evolutions import EVOLUTIONS, Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.storm import shorten_sail_lines
from freesail.orders.verbs import evolution_key
from freesail.orders.vocabulary import load_vocabulary
from freesail.physics import sails as P
from freesail.physics.wind import Wind, WindParams
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from freesail.ship.stub import OrderError
from freesail.world.captains import Captain

SETTEE = "main.settee"
YARD = "main.lug_yard"
LUGGER = "data/ships/lugger.yaml"
SETTEE_FILES = ("set_settee", "take_in_settee", "furl_settee", "dip_settee")
LUG_FLOOR_DEG = 8.0
# Thirty degrees of apparent wind on the larboard bow: the lee is starboard.
CLOSE = math.radians(-30.0)
LIGHT_AIRS = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))


def _bare(ship: Ship, awa: float = CLOSE) -> Runner:
    """A bare ship's runner, the deck reading `awa` of apparent wind, enough to trim to."""
    runner = Runner(ship)
    ship.dyn.apparent_wind_angle = awa
    ship.dyn.apparent_wind_speed = 6.0
    return runner


def _run(runner: Runner, ship: Ship, max_ticks: int = 3000, watch=None) -> tuple[int, list]:
    """Tick the runner (no physics) until nothing is in hand: the ticks and the notes; `watch`,
    a function of the ship called every tick."""
    ticks, notes = 0, []
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
        if watch is not None:
            watch(ship)
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return ticks, notes


def _under_plain_sail(ship: Ship) -> Ship:
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship


def _deg(angle: float) -> float:
    return round(math.degrees(abs(angle)), 3)


# ---------------------------------------------------------------------------
# One key, and how it routes (Ext §5.2)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "verb, evolution",
    [
        ("set", "set_settee"),
        ("take in", "take_in_settee"),
        ("furl", "furl_settee"),
        ("dip", "dip_settee"),
        ("reef", "reef_lug"),
        ("shake out", "shake_out_lug"),
        ("trim", "trim_lug_sheet"),
        ("bend", "bend_sail"),
        ("unbend", "unbend_sail"),
        ("shift", "shift_sail"),
    ],
)
def test_the_one_key_routes_the_settee_and_leaves_the_lugs_rows_to_the_lug(verb, evolution):
    """`evolution_key` (Ext §5.2): "settee" where the verb's mapping has a settee row (set, take
    in, furl, dip), else the class: so reef, shake out, trim, bend, unbend and shift are the lug's
    (D42(a), D45(a)). The lugger's main lug, a dipping lug with no key, keeps the lug's row of
    every verb, as before."""
    vocab = load_vocabulary()
    mapping = dict(vocab.evolutions[verb])
    if verb == "furl":
        # `furl` takes a lug in (`verbs.FURLED_AS_TAKEN_IN`): the settee's own row comes first
        mapping = {"lug": vocab.evolutions["take in"]["lug"], **mapping}
    settee = brig_with_settee().sails[SETTEE]
    assert mapping[evolution_key(settee, mapping)] == evolution
    lug = load_ship(LUGGER).sails["main.lug"]
    assert lug.dipping and not lug.settee
    if "lug" in mapping:
        assert evolution_key(lug, mapping) == "lug"


@pytest.mark.parametrize(
    "text, evolution",
    [
        ("set the mainsail", "set_settee"),
        ("take in the mainsail", "take_in_settee"),
        ("clew up the mainsail", "take_in_settee"),
        ("haul up the mainsail", "take_in_settee"),
        ("furl the mainsail", "furl_settee"),
        ("dip the mainsail", "dip_settee"),
        ("reef the mainsail", "reef_lug"),
        ("trim the mainsail", "trim_lug_sheet"),
        ("unbend the mainsail", "unbend_sail"),
    ],
)
def test_the_settees_orders_start_its_own_evolutions(text, evolution):
    """The orders as given, each started on the settee and run to its end; a take-in or a furl
    is handing it (`HANDING_EVOLUTIONS`), so a heave-to never lays it aback meanwhile. Set and
    unbent from furled, the rest from set."""
    ship = brig_with_settee()
    runner = _bare(ship)
    settee = ship.sails[SETTEE]
    if evolution not in ("set_settee", "unbend_sail"):
        settee.state = SailState.SET
        settee.lug_side = "larboard"  # the weather side: against its mast, to be dipped
        yard_trim.set_sheet_angle(ship, settee, math.radians(60.0))  # eased, to be trimmed
    _kind, _words, data = orders.handle(ship, text)
    assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [(evolution, SETTEE)]
    if evolution in ("take_in_settee", "furl_settee"):
        assert scripts.being_handed(ship, settee)
    _run(runner, ship)


@pytest.mark.parametrize("phrase", ["lower", "brail up", "haul down"])
def test_lower_the_mainsail_is_refused_in_the_settees_words(phrase):
    """Ext §5.2: a settee is clewed up aloft as a course is (Lescallier p. 390), never lowered as
    a lug is: "lower the mainsail" is refused, "clew up" named (`take_in_words`)."""
    ship = brig_with_settee()
    _bare(ship)
    ship.sails[SETTEE].state = SailState.SET
    with pytest.raises(OrderError) as e:
        orders.handle(ship, f"{phrase} the mainsail")
    past = {"lower": "lowered", "brail up": "brailed up", "haul down": "hauled down"}[phrase]
    assert str(e.value) == (
        f"A settee sail is clewed up, not {past}; say 'clew up the main settee' or 'take in the "
        "main settee'."
    )


def test_no_order_braces_the_settee_or_its_yard():
    """Its yard has vangs and ourses, worked by no order (D45(a)): the brace orders refuse the
    sail and its yard in a settee's words, as they refuse a lateen's (B3.1)."""
    ship = brig_with_settee()
    _bare(ship)
    ship.sails[SETTEE].state = SailState.SET
    for text, words in (
        (
            "brace the mainsail sharp up",
            "The main settee has no braces to its yard; a settee is trimmed with its sheet.",
        ),
        (
            "brace the main lug yard sharp up",
            "The main lug yard is a lug yard, not a yard; the settee on it is not braced; it is "
            "trimmed with its sheet and vangs.",
        ),
    ):
        with pytest.raises(OrderError) as e:
            orders.handle(ship, text)
        assert str(e.value) == words, text
    assert YARD not in {y.id for y in scripts.working_yards(ship)}


def test_the_settees_files_say_what_they_are():
    """Ext §5.3: four files, each `class: settee`, six hands (a company of eight meets each with
    a watch of four, D43), the loosing and the furl aloft, sources named; the times judgement."""
    aloft = {
        "set_settee": {"loose"},
        "take_in_settee": set(),
        "furl_settee": {"furl"},
        "dip_settee": set(),
    }
    for eid in SETTEE_FILES:
        evo = EVOLUTIONS[eid]
        assert evo.applies_to == {"class": "settee"} and evo.source, eid
        assert evo.crew["hands"] == 6, eid
        assert {s.do for s in evo.steps if s.aloft} == aloft[eid], eid
    assert EVOLUTIONS["dip_settee"].crew["rating"] == "able"
    assert [s.duration_s for s in EVOLUTIONS["dip_settee"].steps] == [30, 75, 75]  # 180 s
    assert "take_in_settee" in scripts.HANDING_EVOLUTIONS
    assert "furl_settee" in scripts.HANDING_EVOLUTIONS
    # the times stay out of the manoeuvres' files, whose timings are pinned whole (E16)
    for eid in ("tack", "wear", "heave_to", "boxhaul"):
        assert "settee_dip_s" not in EVOLUTIONS[eid].timing, eid
    assert scripts.SETTEE_DIP_S == 120.0


def test_each_settee_evolution_runs_to_its_end_and_only_a_dip_lowers_its_yard():
    """Ext §5.3, E11: set from furled (loosed aloft), clewed up, set from the gear, reefed and its
    reef shaken out as a lug's, dipped, furled on its yard: each to its end in its file's time.
    Clewed up or furled it keeps its yard aloft (`yard_lowered` false at every tick); the dip
    lowers it between its first step and its hoist, and passes it to the lee side."""
    ship = brig_with_settee()
    settee = ship.sails[SETTEE]
    runner = _bare(ship)
    lowered_at: list[bool] = []

    def watch(s):
        lowered_at.append(s.sails[SETTEE].yard_lowered)

    assert settee.state is SailState.FURLED and settee.lug_side is None
    runner.start(ship, "set_settee", SETTEE)
    ticks, notes = _run(runner, ship, watch=watch)
    assert settee.is_set and ticks == 135  # loosed aloft 90 s, tack and sheet 45 s
    assert settee.lug_side == "starboard"  # never hoisted on a side: to leeward
    assert _deg(settee.sheet_angle) == LUG_FLOOR_DEG  # the lug's trim: 30 less 25, its floor 8
    assert [n[2] for n in notes][-1] == "Set the mainsail."
    for evo, kind, ended, state in (
        (
            "take_in_settee",
            "sail.taken_in",
            "Took in the mainsail; hanging in the gear, its yard aloft.",
            SailState.IN_THE_GEAR,
        ),
        ("set_settee", "sail.set", "Set the mainsail.", SailState.SET),
        ("reef_lug", "sail.reefed", "Reefed the mainsail; now set, 1 reef.", SailState.SET),
        (
            "shake_out_lug",
            "sail.reef_shaken_out",
            "Shook the reef out of the mainsail; now set.",
            SailState.SET,
        ),
    ):
        runner.start(ship, evo, SETTEE)
        _ticks, notes = _run(runner, ship, watch=watch)
        assert [n[1] for n in notes][-1] == kind and [n[2] for n in notes][-1] == ended, evo
        assert settee.state is state, evo
    assert not any(lowered_at)
    settee.lug_side = "larboard"  # left on the weather side, as after a tack with no dip
    lowered_at.clear()
    runner.start(ship, "dip_settee", SETTEE)
    ticks, notes = _run(runner, ship, watch=watch)
    assert ticks == 180 and settee.is_set and settee.lug_side == "starboard"
    assert not settee.yard_lowered and lowered_at.count(True) == 150  # the shift and the hoist
    assert [n[2] for n in notes][-1] == "Dipped the mainsail; it stands to leeward of the mast."
    lowered_at.clear()
    runner.start(ship, "furl_settee", SETTEE)
    _ticks, notes = _run(runner, ship, watch=watch)
    assert settee.state is SailState.FURLED and not any(lowered_at)
    assert [n[2] for n in notes][-1] == "Furled the mainsail on its yard."


def test_a_settee_left_on_deck_is_set_by_hoisting_and_furled_there():
    """A manoeuvre belayed with the settee's yard on deck (`yard_lowered`, in the gear) leaves it
    there: setting it hoists the yard on the lee side; furling it furls it on deck and hoists the
    yard, the sail furled on it (Ext §5.3)."""
    ship = brig_with_settee()
    settee = ship.sails[SETTEE]
    runner = _bare(ship)
    settee.state, settee.yard_lowered, settee.lug_side = SailState.IN_THE_GEAR, True, "larboard"
    runner.start(ship, "set_settee", SETTEE)
    ticks, notes = _run(runner, ship)
    assert ticks == 105 and settee.is_set and not settee.yard_lowered  # hoist 60, tack 45
    assert settee.lug_side == "starboard"
    said = [n[2] for n in notes]
    # the opening line true of a yard on deck as of one aloft (B3.3's review: it said "let go the
    # clewlines and buntlines" of a sail lying on deck); the step's line says which
    assert "Man the mainsail tack and sheet." in said
    assert "Hoisted the mainsail's yard on the lee side of the mast." in said
    assert not any("clewlines" in t for t in said)
    settee.state, settee.yard_lowered = SailState.IN_THE_GEAR, True
    runner.start(ship, "furl_settee", SETTEE)
    ticks, notes = _run(runner, ship)
    assert ticks == 210 and settee.state is SailState.FURLED and not settee.yard_lowered
    said = [n[2] for n in notes]
    assert "Hands to furl the mainsail." in said and not any("aloft" in t for t in said)
    assert "Furled the mainsail on its yard on deck." in said
    # set, it is furled aloft: the topmen lay aloft
    settee.state = SailState.SET
    runner.start(ship, "furl_settee", SETTEE)
    _ticks, notes = _run(runner, ship)
    assert "Lay aloft and furl the mainsail." in [n[2] for n in notes]


# ---------------------------------------------------------------------------
# Every lug-keyed path (Ext §5.4): she is no lugger
# ---------------------------------------------------------------------------


def test_she_is_no_lugger_and_the_lugger_keeps_every_list_she_had():
    """Ext §5.4: the settee is among the dipping lugs (the stern watch reads it against its mast)
    but never the lugger's: `lugger_lugs`, `LugDip`, `_lugs_all` and getting under way leave it
    out, so her first words are a ship's and she has no storm lug (the captains'). The lugger's
    lists are what they were."""
    ship = _under_plain_sail(brig_with_settee())
    assert [s.id for s in scripts.dipping_lugs(ship)] == [SETTEE]
    assert [s.id for s in scripts.settees(ship)] == [SETTEE]
    assert scripts.lugger_lugs(ship) == [] and scripts.LugDip(ship).ids == []
    assert scripts._lugs_all(ship) == [] and scripts._standing_lugs_all(ship) == []
    assert scripts.under_way_start_words(ship) == scripts.UNDER_WAY_START_WORDS
    assert Captain._lugger_storm_lug(SimpleNamespace(world=SimpleNamespace(ship=ship))) is False
    assert scripts.boom_sails(ship) == [] and scripts.shifted_sails(ship) == []
    lugger = _under_plain_sail(load_ship(LUGGER))
    dipping = [s.id for s in scripts.dipping_lugs(lugger)]
    assert dipping == ["fore.lug", "main.lug"]
    assert [s.id for s in scripts.lugger_lugs(lugger)] == dipping
    assert scripts.LugDip(lugger).ids == dipping and scripts.settees(lugger) == []
    assert [s.id for s in scripts._lugs_all(lugger)] == dipping
    assert scripts.under_way_start_words(lugger) == scripts.UNDER_WAY_START_WORDS_LUGGER


def test_her_main_is_laid_aback_and_the_settee_is_no_driver():
    """Ext §5.7, D4(a): `heave_to_aback` on her main gives its yards to lay aback, the dry main
    yard and the main topsail's among them; without the key the fore carries the more square
    sail and is chosen, as in the trial (Eng §4.4). The settee is her after sail set after the
    cast (`after_gaff_sails_all`) and no driver in a manoeuvre (`after_gaff_sails`); the words
    name it."""
    ship = _under_plain_sail(brig_with_settee())
    backed = [y.id for y in scripts.yards_to_back(ship)]
    assert backed == ["main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"]
    assert scripts.yards_to_back_set(ship)[:2] == [
        ship.spars["main.yard"],
        ship.spars["main.topsail.yard"],
    ]
    assert P._square_rigged(ship) is True
    assert [m.id for m in scripts._masts_with_yards(ship)] == ["fore.mast", "main.mast"]
    assert scripts.after_gaff_sails(ship) == []
    assert [s.id for s in scripts.after_gaff_sails_all(ship)] == [SETTEE]
    assert scripts.driver_words(ship, []) == "the mainsail"
    ship.spars["main.mast"].heave_to_aback = False
    assert ship.mast_of(scripts.yards_to_back(ship)[0]).id == "fore.mast"


def test_its_sheet_leads_a_fathom_abaft_its_clew_by_its_own_corners():
    """Ext §5.9 and the lead's ruling on the bilander's §17 lead item 4: a settee's foot is its
    corners' tack to clew, in place of the loose-footed proxy (0.8 of the square root of the
    area), its block a fathom abaft the clew at the floor and abreast of it; the trim reads no part
    of the hull's profile. The lugger's lugs keep the proxy. On the fixture the foot is 12.24 m
    against the proxy's 7.42 m: the block 14.26 m abaft the tack's station, 2.21 m inside her
    taffrail (her rail's after end, x -16.47 m), where the proxy's lay 6.98 m inside it."""
    ship = brig_with_settee()
    settee = ship.sails[SETTEE]
    (tx, tz), _throat, _peak, (cx, cz) = settee.corners_m
    geo = yard_trim.sheet_geometry(ship, settee)
    assert not geo.boomed and geo.arm_m == pytest.approx(math.hypot(cx - tx, cz - tz))
    assert geo.arm_m == pytest.approx(12.24, abs=0.01)
    assert geo.offset_m == pytest.approx(geo.arm_m * math.sin(geo.floor))
    assert geo.lead_aft_m == yard_trim.FATHOM_M
    block_x = tx + geo._block(geo.floor)[0]
    assert block_x == pytest.approx(-14.26, abs=0.01)
    assert block_x - min(x for x, _z in ship.hull.spec.profile.rail_m) == pytest.approx(
        2.21, abs=0.01
    )
    lugger = load_ship(LUGGER)
    for sid in ("fore.lug", "main.lug"):
        lug = lugger.sails[sid]
        lug_geo = yard_trim.sheet_geometry(lugger, lug)
        assert lug_geo.arm_m == pytest.approx(0.8 * math.sqrt(lug.area_m2)), sid


def test_in_the_physics_it_is_the_lug_against_its_mast_on_the_weather_side():
    """Ext §5.9: nothing in the physics changes. Its curve is the lug's (D44(a)); with its yard on
    the side its sheet holds it to it draws whole, on the other side at two-thirds of its area
    (`LUG_AGAINST_MAST_AREA`), until it is dipped."""
    for side, share in (("starboard", 1.0), ("larboard", P.LUG_AGAINST_MAST_AREA)):
        ship = brig_with_settee()
        for s in ship.sails.values():
            s.state = SailState.FURLED
        settee = ship.sails[SETTEE]
        settee.state = SailState.SET
        settee.lug_side = side
        wind = Wind(WindParams.from_nautical(310.0, 15.0, 0.0, 0.0), random.Random(0))
        P.compute_sail_forces(ship, wind)  # the deck's reading: the lee is starboard
        yard_trim.set_sheet_angle(ship, settee, math.radians(25.0))
        P.compute_sail_forces(ship, wind)
        assert settee.curve_class == "lug"
        assert settee.area_effective_m2 == pytest.approx(settee.area_m2 * share, rel=1e-6), side


def test_the_gale_reefs_it_with_the_second_reef_and_takes_it_in_with_the_third():
    """E15, Ext §5.8: in "courses", the gale's reduction (`orders.storm`, Luce 1884 p. 476) reefs
    it with the fore course as the topsails take their second reef and takes it in, her aftermost
    course, with their third; she is square-rigged by her fore and main yards. "Take in the main
    settee" clews it up aloft."""
    ship = _under_plain_sail(brig_with_settee())
    topsails = [s for s in ship.sails.values() if s.id.endswith(".topsail") and s.is_set]
    for sl in topsails:
        sl.reefs = 1
    lines = shorten_sail_lines(ship, 30.0)
    assert "reef the main settee, one reef" in lines and "reef the fore course, one reef" in lines
    for sl in topsails:
        sl.reefs = 2
    lines = shorten_sail_lines(ship, 40.0)
    assert "take in the main settee" in lines and "reef the fore course, one reef" in lines
    _bare(ship)
    _kind, _words, data = orders.handle(ship, "take in the main settee")
    assert [e["evolution"] for e in data["evolutions"]] == ["take_in_settee"]


def test_every_settee_request_begins_with_her_company_of_eight():
    """D43, Ext §5.3: every settee evolution asks for six hands, which a company of eight with a
    main-top pair (Ext §5.1) meets from a watch of four on deck: short-handed, so begun with half
    and slower in proportion (`hands.SHORT_HANDED_SHARE`), never too few; aloft too, her topmen
    and the others able."""
    stations = (Station.MAIN_TOP, Station.FORE_TOP, Station.FORECASTLE, Station.AFTERGUARD)
    sailors = [
        Sailor(f"s{i:03d}", f"Hand {i}", Rating.ABLE, station, watch, 0.8, 0.8)
        for i, (watch, station) in enumerate(
            (w, s) for w in (Watch.STARBOARD, Watch.LARBOARD) for s in stations
        )
    ]
    crew = Crew("the bilander", sailors)
    for watch in (Watch.STARBOARD, Watch.LARBOARD):
        deck = [s for s in crew.sailors if s.watch is watch]
        for eid in SETTEE_FILES:
            evo = EVOLUTIONS[eid]
            want = hands.CrewRequest.from_mapping(evo.crew)
            aloft = any(step.aloft for step in evo.steps)
            for s in crew.sailors:
                s.at = None
            got = hands.request(crew, deck, eid, want, "main", aloft=aloft)
            assert got.outcome == hands.SHORT and got.got == 4, (watch, eid, got.outcome)


# ---------------------------------------------------------------------------
# The manoeuvres: the fixture sailing, seed 7 (B3.4's settle)
# ---------------------------------------------------------------------------


def _world(tmp_path, knots: float = 15.0, settle_s: int = 2400):
    """The fixture in a northerly on the starboard tack, 67.5 degrees off the wind at 5 kn, under
    plain sail braced sharp up and trimmed every two minutes, settled `settle_s` (B3.4's measure,
    docs/dev/TuningNotes.md, "The schooner's mast")."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, write_ship(brig_with_settee_doc(), tmp_path, "settee"), scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    for i in range(settle_s):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    assert world.ship.sails[SETTEE].is_set and world.ship.dyn.tack == "starboard"
    return world


def _rel_deg(world) -> float:
    return math.degrees(units.relative_bearing(world.ship.dyn.heading, world.wind.direction_from))


def _after(world, start: int) -> list:
    return [e for e in world.log if e.tick > start]


def _first_tick(world, start: int, words: str) -> int | None:
    hit = [e.tick for e in _after(world, start) if words in e.text]
    return hit[0] - start if hit else None


def test_hanging_in_stays_the_settee_is_held_over_to_windward_with_no_boom(tmp_path):
    """Ext §5.5 step 2: as a boom sail its sheet is held over to windward if she hangs in stays,
    and it pushes her stern away (Luce 1866, carried over by judgement); the words name the sail,
    not a boom it has not got. A miss before she is through eases its sheet off with the boom
    sails (`_miss_stays`), the settee's change never begun."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    world.submit("tack ship")
    world.tick()
    world.tick()
    runner = world.ship.extra["evolutions"]
    (tack,) = [i.script for i in runner.instances if isinstance(i.script, scripts.TackScript)]
    assert tack.booms == [settee] and tack.dip.ids == []
    tack._hang()
    (line,) = [n[2] for n in world.ship.drain_notes() if "hangs in stays" in n[2]]
    assert line.endswith("; the mainsail hauled over to windward."), line
    read = yard_trim.read_sheet(world.ship, settee)
    assert read.side == 1 and read.held_to_windward  # the old weather side: starboard
    tack._miss_stays("she fell off on the old tack")
    geo = yard_trim.sheet_geometry(world.ship, settee)
    assert settee.sheet_angle == pytest.approx(geo.ceiling, abs=1e-6)
    assert tack.settee_change is None and not settee.yard_lowered


@pytest.mark.parametrize("kept", [True, False])
def test_hove_to_her_main_topsail_goes_to_the_mast(tmp_path, monkeypatch, kept):
    """Ext §5.7, D4(a): the main topsail to the mast by her file's key, the fore topgallant clewed
    up, the fore course hauled up. The settee by the engine's driver rule, the lead's ruling on Ext
    §14 item 3: kept with its sheet eased, as the brig's spanker is, since her backed yards are on
    her aftermost mast; and (`SETTEE_KEPT_HOVE_TO` false, the way the figures were measured
    against) clewed up aloft, D4(a)'s words, its yard standing. Kept, she lies 63.5 degrees off at
    1.8 kn from +300 s to +900 s in 15 kn, inside the heave-to's four to seven points; clewed up,
    she lies 67.9 degrees off at +300 s and falls off past seven points by +600 s (80.6 degrees,
    93.3 at the most), as the brig falls off with her driver brailed (package 32e): so the driver
    rule stands, figures in docs/dev/TuningNotes.md, "The settee in the engine"."""
    monkeypatch.setattr(scripts, "SETTEE_KEPT_HOVE_TO", kept)
    world = _world(tmp_path)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("heave to")
    offs = []
    for i in range(1, 901):
        world.tick()
        if i > 300:
            offs.append(abs(_rel_deg(world)))
    texts = [e.text for e in _after(world, start)]
    words = "eased off the mainsail sheet" if kept else "clewed up the mainsail"
    assert f"Hauled up the courses; {words}." in texts, texts
    assert (
        "Braced the main topsail aback; braced up the other yards; hauled aft the head sheets; "
        "helm a-lee." in texts
    )
    assert any(
        t.startswith("Hove to on the starboard tack, main topsail to the mast") for t in texts
    )
    assert not settee.yard_lowered
    if kept:
        assert settee.is_set
        assert 45.0 <= min(offs) and max(offs) <= 78.75  # four to seven points
    else:
        assert settee.state is SailState.IN_THE_GEAR
        assert max(offs) > 78.75  # she falls off past seven points


def test_getting_under_way_she_casts_as_a_ship_and_sets_the_settee_after_the_cast(tmp_path):
    """Ext §5.8: with no lugger's lugs she is got under way as a ship (the trial's lugger's path
    failed at 1,842 s, Eng §4.4): her topsails loosed aloft and the settee, furled on its yard,
    loosed with them, cast with her head yards, and the settee set after the cast on the lee side,
    the words naming it. From Falmouth's outer road in 10 kn at seed 7 (B3.4's): under way in
    1,342 s, as the brig's 1,342-1,343 s."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=0.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
        position={"lat_deg": 50.133, "lon_deg": -5.035},
        region="channel-west",
    )
    world = make_world(7, write_ship(brig_with_settee_doc(), tmp_path, "settee"), scenario)
    world.run(60)
    assert world.submit("let go the best bower").kind == "order.accepted"
    world.run(900)
    settee = world.ship.sails[SETTEE]
    assert settee.state is SailState.FURLED
    start = world.clock.tick
    assert world.submit("get under way").kind == "order.accepted"
    states: list[tuple[SailState, int]] = []
    for _ in range(1800):
        world.tick()
        if not states or states[-1][0] is not settee.state:
            states.append((settee.state, world.clock.tick - start))
        if any(e.kind in ("ship.under_way", "evolution.failed") for e in _after(world, start)):
            break
    texts = [e.text for e in _after(world, start)]
    assert scripts.UNDER_WAY_START_WORDS in texts
    assert scripts.UNDER_WAY_START_WORDS_LUGGER not in texts
    loose = _first_tick(world, start, "Lay aloft, sail-loosers!")
    cast = [t for t in texts if "right the helm" in t]
    assert cast and cast[0].endswith(
        "right the helm, brace round the head yards, set the mainsail."
    )
    # furled on its yard aloft, it is loosed with the topsails and set at the cast (B3.3's
    # review: it went from furled to set in one tick, never loosed)
    assert [s for s, _t in states] == [SailState.FURLED, SailState.LOOSED, SailState.SET]
    assert states[1][1] == loose and states[2][1] == _first_tick(world, start, "right the helm")
    under = [e for e in _after(world, start) if e.kind == "ship.under_way"]
    assert under and 1300 <= under[0].tick - start <= 1400, texts[-3:]
    assert settee.is_set and settee.lug_side == "larboard"  # the starboard tack's lee


def test_rounding_to_the_settee_is_clewed_up_aloft_and_she_brings_up(tmp_path):
    """Ext §5.8: as she rounds to it is put in its gear with the square sails, which for a settee
    is clewed up with its yard aloft; she loses her way, lets go and brings up (Carrick Road in
    12 kn, plain sail set and trimmed, as `tests/test_anchor.py` brings the frigate up: let go at
    298 s, brought up at 1,246 s, the brig as filed 296 s and 1,244 s), and no driver she has not
    got is brailed up at "brought up". The trim is ordered after the first tick, the deck's first
    reading of the wind (before it, "There is no wind to trim to": B3.3's review)."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=335.0,
        ship_speed_kn=3.0,
        position={"lat_deg": 50.160, "lon_deg": -5.034},
        region="channel-west",
    )
    world = make_world(7, write_ship(brig_with_settee_doc(), tmp_path, "settee"), scenario)
    _under_plain_sail(world.ship)
    world.tick()  # the deck's first reading of the wind, which the trim needs
    assert world.submit("trim sails").kind == "sail.trimmed"
    world.run(120)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    assert world.submit("come to an anchor").kind == "order.accepted"
    states = set()
    for _ in range(1500):
        world.tick()
        if (
            _first_tick(world, start, "Helm down for") is not None
            and settee.state is not SailState.FURLED
        ):
            states.add((settee.state, settee.yard_lowered))
        if any(e.kind == "ship.brought_up" for e in _after(world, start)):
            break
    assert states == {(SailState.IN_THE_GEAR, False)}
    kinds = [e.kind for e in _after(world, start)]
    assert "ship.anchored" in kinds and "ship.brought_up" in kinds
    veered = [e.text for e in _after(world, start) if e.text.startswith("Veered to")]
    assert veered and "brail up" not in veered[0], veered


@pytest.mark.parametrize(
    "order, kind, settee_at_end",
    [
        ("box haul", "ship.box_hauled", "starboard"),
        ("wear short round", "ship.wore", "starboard"),
        ("box her off", "ship.boxed_off", "larboard"),
        ("lie a try", "ship.hove_to", None),
        ("scud", "ship.scudding", "larboard"),
        ("back and fill", "ship.hove_to", None),
        ("furl all", "sail.furled", None),
    ],
)
def test_the_untried_manoeuvres_each_run_to_an_end(tmp_path, order, kind, settee_at_end):
    """Ext §5.4's untried manoeuvres, each run once from the settle (seed 7, 15 kn): each ends in
    its own line. Box-hauling and wearing short round: the settee is lowered as the mainsail is
    hauled up ("Lower the mainsail! Square away the after yards!") and hoisted on the new lee once
    its time is done and she is coming to, as the mainsail is set again (the guard added, keyed on
    the settee: left set it was left against its mast with no word). Worn short round, the wind
    passes her stern, and the line says so, as in wearing; box-hauled in 15 kn her head goes
    through the wind by the bow on the sternboard (so too the brig's as filed), so the wind never
    passes her stern and the line does not say it did (B3.3's review). Boxed off from coming to she
    keeps her tack and it its side (boxed off from aback, below). Lying a-try it is clewed up
    aloft with her courses, her main course and her after sail, as the brig's mainsail and spanker
    are handed and as the gale has it in before (B3.3's review: left standing, the line named the
    main topsail and the staysails alone); scudding it stands; backing and filling clews it up
    aloft with her courses (the guard added: left drawing it took her head through the wind at the
    first board, and she was forced round); furling all furls it on its yard aloft.
    `settee_at_end`: the side its yard is on, set, at the end; None, not set."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    assert world.submit(order).kind == "order.accepted"
    for _ in range(1200):
        world.tick()
        if any(e.kind == kind for e in _after(world, start)):
            break
    assert any(e.kind == kind for e in _after(world, start)), [e.text for e in _after(world, start)]
    assert not settee.yard_lowered
    if settee_at_end is None:
        assert not settee.is_set
    else:
        assert settee.is_set and settee.lug_side == settee_at_end
    texts = [e.text for e in _after(world, start)]
    if order in ("box haul", "wear short round"):
        assert any(t.startswith("Lower the mainsail! Square away the after yards!") for t in texts)
        hoisted = {
            "wear short round": "Hoisted the mainsail on the starboard side, to leeward of the "
            "mast; the wind is past the stern.",
            "box haul": "Dipped the mainsail; hoisted on the starboard side, to leeward of the "
            "mast.",
        }[order]
        assert hoisted in texts, texts
        # hoisted as she comes to, never before the wind is aft
        assert _first_tick(world, start, hoisted) >= _first_tick(world, start, "Wind aft")
    if order == "lie a try":
        assert settee.state is SailState.IN_THE_GEAR
        took = next(t for t in texts if t.startswith("Took in "))
        assert "the mainsail" in took, took
        assert "Lying a-try under the main topsail and the staysails, helm a-lee." in texts
    if order == "back and fill":
        assert "Hauled up the foresail, the fore topgallant and the mainsail." in texts
        assert settee.state is SailState.IN_THE_GEAR
    if order == "furl all":
        assert settee.state is SailState.FURLED


def test_boxed_off_from_aback_the_settee_is_dipped_to_her_lee(tmp_path):
    """Taken aback, her head put across onto the larboard bow, the case `keep_full_and_by` and
    the captains box her off for: she is boxed off on the larboard tack, where the settee's yard,
    on the old lee, is on the weather side against its mast. It is lowered as the mainsail is
    hauled up, passed round and hoisted on her new lee once its time is done and the after sails
    take, and she is boxed off when it is up (B3.3's review, seed 7, 15 kn, from B3.4's settle of
    2,400 s: left set, it stayed against its mast to the end with no word said, 67.2 degrees off
    at 3.82 kn at +900 s; now hoisted and boxed off at 155 s, 69.9 degrees off at 4.37 kn at +900
    s). Here from a settle of 1,200 s."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    dyn = world.ship.dyn
    dyn.heading = units.wrap_2pi(world.wind.direction_from + math.radians(25.0))
    dyn.target_heading = dyn.heading
    world.tick()
    world.tick()
    assert dyn.tack == "larboard" and settee.lug_side == "larboard"
    start = world.clock.tick
    assert world.submit("box her off").kind == "order.accepted"
    for _ in range(600):
        world.tick()
        if any(e.kind == "ship.boxed_off" for e in _after(world, start)):
            break
    texts = [e.text for e in _after(world, start)]
    assert any(t.startswith("Lower the mainsail! Square away the after yards!") for t in texts)
    hoisted = "Dipped the mainsail; hoisted on the starboard side, to leeward of the mast."
    haul = _first_tick(world, start, "Her after sails take. Let go and haul!")
    boxed = [e.tick - start for e in _after(world, start) if e.kind == "ship.boxed_off"]
    assert haul is not None and boxed and haul <= _first_tick(world, start, hoisted) <= boxed[0]
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered
    assert dyn.tack == "larboard"
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert lies == 1 and not P.against_the_mast(settee, lies)


def test_gone_round_by_the_stern_from_a_box_off_the_settee_takes_the_other_tacks_lee():
    """Boxing off, she may go round by the stern instead and come to on the other tack (Luce's
    next case), whose lee is the old weather side: a settee lowered at the box is hoisted there,
    the wind past the stern; one still set on that tack's weather side is changed round to it,
    as in wearing (B3.3's review). The script's own turn, on the bare fixture on the starboard
    tack."""
    for side, lowered in (("larboard", False), ("starboard", True), ("starboard", False)):
        ship = _under_plain_sail(brig_with_settee())
        _bare(ship, -CLOSE)  # the wind on the starboard bow
        assert ship.dyn.tack == "starboard"
        settee = ship.sails[SETTEE]
        settee.lug_side = side
        box_off = scripts.BoxOffScript(ship, {}, EVOLUTIONS["box_off"].timing)
        if lowered:  # as the box lowers one on the weather side of the tack she is boxed off on
            change, lee, said = box_off._settee_at_box()
            assert change.ids == [SETTEE] and lee == "larboard"
            box_off.settee_change = change
            change.change(lee, 120.0, said)
        box_off._settee_at_come_to()
        change = box_off.settee_change
        if side == "starboard" and not lowered:  # on that tack's lee already: left as it is
            assert change is None and settee.is_set
            continue
        assert change is not None and change.side == "starboard" and not change.done
        assert change.hoisted_words == scripts.SETTEE_WORE_WORDS
        assert settee.yard_lowered and settee.state is SailState.IN_THE_GEAR


def test_box_hauled_in_a_light_air_the_settee_waits_for_her_to_come_to(tmp_path):
    """In 8 kn at seed 7 her head goes through the wind by the bow on the sternboard after the
    box (10.7 degrees on the bow at 117 s, through at 143 s) and stays on the new side: the wind
    on the new side is no gate for the hoist, which waits till she comes to as the mainsail is
    set again ("Wind aft", at 321 s), and the line does not say the wind passed her stern (B3.3's
    review: it was hoisted at 247 s with the wind 42.6 degrees on the bow, "the wind is past the
    stern", 91 s before "Wind aft")."""
    world = _world(tmp_path, knots=8.0)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("box haul")
    hoisted_at = None
    for i in range(1, 700):
        world.tick()
        if hoisted_at is None and settee.is_set and _first_tick(world, start, "Lower the mainsail"):
            hoisted_at = i
        if any(e.kind == "ship.box_hauled" for e in _after(world, start)):
            break
    texts = [e.text for e in _after(world, start)]
    wind_aft = _first_tick(world, start, "Wind aft")
    assert wind_aft is not None and hoisted_at is not None and hoisted_at >= wind_aft
    assert "Dipped the mainsail; hoisted on the starboard side, to leeward of the mast." in texts
    assert not any("the wind is past the stern" in t for t in texts)
    assert any(e.kind == "ship.box_hauled" for e in _after(world, start))
    assert settee.is_set and settee.lug_side == "starboard"


@pytest.mark.parametrize("side", ["larboard", "starboard"])
def test_in_stays_only_a_settee_off_the_new_lee_is_changed(tmp_path, side):
    """The tack's change (Ext §5.5 step 5) dips a settee whose yard hangs on the old lee, the new
    weather side; one already on the new lee side (left on the weather side before the tack, as
    a box-off from aback or a change cut short can leave it) is to leeward of its mast once she
    is through, and is left as it is, as the dip order leaves it (B3.3's review, 15 kn from B3.4's
    settle of 2,400 s: it was lowered and "passed round" to the side it was on, the yard on deck
    158-318 s while she fell off to 104 degrees, "Tacked" at 318 s; now 261 s). The served
    estimate counts the change to come until it is begun (B3.3's review: at "let go and haul" it
    said 75 s, with 221 s to go; now 195 s). Here from a settle of 1,200 s."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    settee.lug_side = side
    start = world.clock.tick
    world.submit("tack ship")
    runner = world.ship.extra["evolutions"]
    estimate, lowered = None, False
    for _ in range(600):
        world.tick()
        lowered = lowered or settee.yard_lowered
        tack = [i.script for i in runner.instances if isinstance(i.script, scripts.TackScript)]
        if tack and tack[0].phase == "let_go_and_haul" and estimate is None:
            estimate = tack[0].remaining_s()
        if any(e.kind == "ship.tacked" for e in _after(world, start)):
            break
    texts = [e.text for e in _after(world, start)]
    assert any(e.kind == "ship.tacked" for e in _after(world, start))
    dipped = any(t.startswith("Dip the mainsail") for t in texts)
    assert settee.is_set and settee.lug_side == "starboard"
    if side == "larboard":  # the old lee: changed, and the estimate counts it
        assert dipped and lowered and estimate >= scripts.SETTEE_DIP_S
    else:
        assert not dipped and not lowered and estimate < scripts.SETTEE_DIP_S


def test_filling_away_draws_the_settee_kept_hove_to_and_loosing_to_dry_hangs_it_aloft(tmp_path):
    """The other two untried: filled away from hove to (the settee kept, its sheet drawn with the
    boom sails', `_kept_after_sails`), and, furled all, loosed to dry in its gear aloft."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    world.submit("heave to")
    world.run(600)
    assert "hove_to" in world.ship.extra and settee.is_set
    start = world.clock.tick
    world.submit("fill away")
    world.run(300)
    assert any(e.kind == "ship.filled_away" for e in _after(world, start))
    assert settee.is_set and yard_trim.read_sheet(world.ship, settee).side == -1  # her lee
    world.submit("furl all")
    world.run(600)
    assert settee.state is SailState.FURLED and not settee.yard_lowered
    start = world.clock.tick
    world.submit("loose sails to dry")
    world.run(300)
    assert any(e.kind == "sail.loosed" for e in _after(world, start))
    assert settee.state is SailState.LOOSED and not settee.yard_lowered


DIP_AT_FILL_AWAY = (
    "Dip the mainsail: lower the yard, pass it round abaft the mast and shift the tack to the "
    "weather bow."
)
HAULED_AFT = "Hauled aft the head sheets; kept the helm a-lee to let her fall off."


def _shift_the_wind(world, points: float) -> None:
    """The wind shifted `points` at a stroke, as `tests/test_lying_to.py` forces a ship round
    hove to (a squall's front: the one way to do it in a test)."""
    wind = world.wind
    wind.follow(units.wrap_2pi(wind.base_direction + points * units.POINT), wind.base_speed)
    world.scenario.wind_from_deg = math.degrees(wind.base_direction)


FILL_CASES = {
    # case: the deck's reading of the wind, the settee's side, her head (degrees; the true wind
    # from the north), whether it is dipped, and to which side
    "on her lee": (-CLOSE, "larboard", 300.0, None),
    "on her weather side": (-CLOSE, "starboard", 300.0, "larboard"),
    "the deck's reading behind, on her lee": (CLOSE, "larboard", 300.0, None),
    "the deck's reading behind, on her weather side": (CLOSE, "starboard", 300.0, "larboard"),
    "head to the wind at the first tick": (CLOSE, "starboard", 2.0, "larboard"),
}


@pytest.mark.parametrize("case", list(FILL_CASES))
def test_at_fill_away_a_settee_on_her_weather_side_is_dipped_first_as_she_lies(case):
    """B3.3b (Ext §5.7; B4's review on her file), with its review's mend: the script's own turn on
    the bare fixture, the true wind (from the north) on her starboard bow, 60 degrees. At "fill
    away" with a settee set nothing is done till the first tick, which reads the tack she is on
    from the wind itself, as the fill away reads it, and not from the deck's reading, which lags
    a ship just come round (counted meanwhile by the deck's: the dip's 120 s if the deck has the
    settee on her weather side). A settee on her weather side by the wind (starboard, as a forced
    round leaves it) is then lowered, before she is let fall off: the fill away holds it and
    counts it in its estimate, and her hands tend her as she lies (`tend_lying_to`); when its
    time is done (120 ticks at a factor of one) it is hoisted on her lee with its sheet drawn for
    the wind she will have full and by, as the tack hoists it, and she is let fall off with the
    head sheets hauled aft once, its trim kept. One on her lee by the wind is left drawing and
    she is let fall off at once, braced full as she lies 60 degrees off; the script then carries
    no change, its fields as before the guard. Before the mend, read at the order from the deck's
    reading behind her, the one on her lee was lowered and hoisted again on the side it hung on,
    120 s lost, and the one on her weather side was found only at the first tick, after "Hauled
    aft the head sheets" had been said, and that line said again at the hoist (the review's
    finding). Within half a point of the wind at the first tick the deck's reading stands: with
    the settee on its lee she is let fall off, and once her head is off the wind on the other
    tack the settee is found on that tack's weather side and dipped, and she is let fall off
    again when it is up, each said. The fill away names the settee set in its holds from the
    order, whether it is dipped or not (the lead's ruling (3)(iii) of 2026-11-10): before, it named
    it only while it was being dipped, which the runner, reading the holds at the order, never
    saw; three of these pins moved with it, "not in its holds" at the order, left on her lee, and
    after the hoist, now "in its holds"."""
    awa, side, head, dipped_to = FILL_CASES[case]
    ship = _under_plain_sail(brig_with_settee())
    _bare(ship, awa)
    ship.dyn.heading = math.radians(head)
    settee = ship.sails[SETTEE]
    settee.lug_side = side
    ship.extra["hove_to"] = {"yards": [], "sign": 1.0}
    fill = scripts.FillAwayScript(ship, {}, EVOLUTIONS["fill_away"].timing)
    assert fill.check({}) is None
    fill.begin({})
    timing = EVOLUTIONS["fill_away"].timing
    after_s = timing["fall_off_timeout_s"] + timing["brace_s"]
    deck_lee = "larboard" if ship.dyn.tack == "starboard" else "starboard"
    by_the_deck = side != deck_lee  # on her weather side as the deck reads the wind
    assert ship.drain_notes() == [] and fill.phase == "ready" and fill.wind_to_read
    assert settee.is_set and not settee.yard_lowered and SETTEE in fill.holds()  # (3)(iii)
    assert fill.remaining_s() == pytest.approx(after_s + scripts.SETTEE_DIP_S * by_the_deck)
    fill.tick(1.0, LIGHT_AIRS, 1.0)
    texts = [n[2] for n in ship.drain_notes()]
    assert "wind_to_read" not in vars(fill)  # read: the field gone again
    if case == "head to the wind at the first tick":  # the deck's reading stands
        assert fill.phase == "fall_off" and texts == [HAULED_AFT] and fill.sign == -1.0
        assert "settee_change" not in vars(fill)
        ship.dyn.heading = math.radians(300.0)  # her head off the wind, the starboard tack's
        fill.tick(1.0, LIGHT_AIRS, 1.0)
        texts = [n[2] for n in ship.drain_notes()]
    if dipped_to is None:  # left as it is: she falls off at once
        assert fill.phase in ("fall_off", "brace_full") and texts[0] == HAULED_AFT
        assert DIP_AT_FILL_AWAY not in texts and fill.sign == 1.0
        assert "settee_change" not in vars(fill) and "lying" not in vars(fill)
        assert settee.is_set and not settee.yard_lowered and SETTEE in fill.holds()
        assert settee.lug_side == side
        return
    change = fill.settee_change
    assert change is not None and change.ids == [SETTEE] and not change.done
    assert change.side == dipped_to and fill.sign == 1.0  # the starboard tack, by the wind
    assert fill.phase == "dip_settee" and texts == [DIP_AT_FILL_AWAY]
    assert settee.yard_lowered and settee.state is SailState.IN_THE_GEAR
    assert SETTEE in fill.holds()
    begun = case != "head to the wind at the first tick"  # its first tick done with the order's
    assert fill.remaining_s() == pytest.approx(scripts.SETTEE_DIP_S - begun + after_s)
    ticks = int(begun)
    while fill.phase == "dip_settee" and ticks < 400:
        fill.tick(1.0, LIGHT_AIRS, 1.0)
        ticks += 1
    assert ticks == 120 and change.done and fill.sign == 1.0
    assert [n[2] for n in ship.drain_notes()] == [
        "Dipped the mainsail; hoisted on the larboard side, to leeward of the mast.",
        HAULED_AFT,
    ]
    assert fill.phase == "fall_off" and SETTEE in fill.holds()  # from the order, (3)(iii)
    assert settee.is_set and settee.lug_side == "larboard" and not settee.yard_lowered
    geo = yard_trim.sheet_geometry(ship, settee)
    full_and_by = scripts.full_and_by_apparent(ship, LIGHT_AIRS, 0.0)
    trimmed = max(geo.floor, min(geo.ceiling, yard_trim.wanted_sheet_angle("lug", full_and_by)))
    assert yard_trim.read_sheet(ship, settee).angle == pytest.approx(trimmed, abs=1e-6)


def test_forced_round_hove_to_the_kept_settee_is_dipped_first_and_she_fills_away(tmp_path):
    """B3.3b (Ext §5.7; the bilander's design §17 lead item 8, the lead's answer: a follow-up B3
    step keyed on `settee` alone, B4's review having found the need on her file). Hove to on the
    starboard tack with the settee kept by the driver rule, its yard on the larboard side, her
    lee; a shift of eight points forces her round onto the larboard tack, and `_judge_lying_to`
    changes her tack and her yards, not its side: its yard is on her weather side, against its
    mast. "Fill away" dips it first, as she lies: lowered at the order, hoisted on the starboard
    side when its time is done, and then she is let fall off and filled away, each said. Seed 7,
    15 kn, from a settle of 1,200 s: forced round 20 s after the shift, the order 40 s after that;
    the dip's words at +1 s, its yard on deck to +156 s, she lying 69-98 degrees off meanwhile
    (as she lies with it clewed up, D4(a)); hoisted and "Hauled aft the head sheets" at +157 s,
    "Filled away on the larboard tack" at +217 s; at +600 s it draws whole, as at the settle, at
    4.26 kn. Before the guard she was filled away at +59 s with it drawing against its mast to the
    end, two-thirds of it (57.2 of 86.0 m2), at 3.38 kn, and no line said so."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    whole = settee.area_effective_m2  # as it draws clear of its mast at the settle
    world.submit("heave to")
    world.run(600)
    assert world.ship.extra["hove_to"]["sign"] == 1.0
    assert settee.is_set and settee.lug_side == "larboard"
    start = world.clock.tick
    _shift_the_wind(world, -8.0)
    world.run(60)
    (forced,) = [e for e in _after(world, start) if e.kind == "ship.forced_round"]
    assert "lies on the larboard tack" in forced.text
    assert world.ship.extra["hove_to"]["sign"] == -1.0
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.lug_side == "larboard" and lies == 1 and P.against_the_mast(settee, lies)
    start = world.clock.tick
    assert world.submit("fill away").kind == "order.accepted"
    lowered = []
    for _ in range(600):
        world.tick()
        lowered.append(settee.yard_lowered)
    texts = [e.text for e in _after(world, start)]
    hoisted = "Dipped the mainsail; hoisted on the starboard side, to leeward of the mast."
    assert DIP_AT_FILL_AWAY in texts and hoisted in texts, texts
    assert _first_tick(world, start, DIP_AT_FILL_AWAY) == 1
    up = _first_tick(world, start, hoisted)
    assert abs(up - 157) <= 10 and _first_tick(world, start, HAULED_AFT) == up  # then falls off
    assert all(lowered[: up - 1]) and not any(lowered[up - 1 :])  # on deck till the hoist
    filled = [e for e in _after(world, start) if e.kind == "ship.filled_away"]
    assert len(filled) == 1 and filled[0].text.startswith("Filled away on the larboard tack")
    assert up < filled[0].tick - start <= up + 90
    assert not [e for e in _after(world, start) if e.kind in ("ship.aback", "ship.filled")]
    assert "hove_to" not in world.ship.extra and world.ship.dyn.tack == "larboard"
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered
    assert lies == 1 and not P.against_the_mast(settee, lies)
    assert settee.area_effective_m2 == pytest.approx(whole, rel=0.01)


def test_belayed_while_the_settee_is_dipped_the_words_say_it_is_left_on_deck(tmp_path):
    """B3.3b's review (should-fix): "fill away" belayed while the settee is being dipped. The
    runner's words named the script's phase, "... left as they stand at dip settee", and did not
    say the settee was left lowered on deck; the fill away's own words now do (`left_words`), the
    sail by its name, as the log names it. Seed 7, 15 kn, the fixture forced round as in the test
    above, "fill away", and "belay that" 30 s after: the settee left in its gear on deck on its old
    side, nothing of the fill away in hand; "set the mainsail" hoists it again, the captain's."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    world.submit("heave to")
    world.run(600)
    _shift_the_wind(world, -8.0)
    world.run(60)
    assert world.ship.extra["hove_to"]["sign"] == -1.0 and settee.lug_side == "larboard"
    start = world.clock.tick
    assert world.submit("fill away").kind == "order.accepted"
    world.run(30)
    assert _first_tick(world, start, DIP_AT_FILL_AWAY) == 1 and settee.yard_lowered
    reply = world.submit("belay that")
    assert reply.kind == "work.belayed"
    assert reply.text == (
        "Belayed filling away; the helm and the yards left as they stand; the mainsail lowered "
        "on deck, not yet dipped."
    )
    assert settee.state is SailState.IN_THE_GEAR and settee.yard_lowered
    assert settee.lug_side == "larboard"
    runner = world.ship.extra["evolutions"]
    assert not [i for i in runner.instances if i.evo.id == "fill_away"]
    assert world.submit("set the mainsail").kind == "order.accepted"
    world.run(300)
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.is_set and not settee.yard_lowered and world.ship.dyn.tack == "larboard"
    assert settee.lug_side == "starboard" and not P.against_the_mast(settee, lies)


# ---------------------------------------------------------------------------
# The lead's ruled builds of 2026-11-10, (3)(i) to (iii): the settee forced round and left to
# herself, paying off to a course, and held from the order
# ---------------------------------------------------------------------------

WATCH_DIPS = "The watch dips the mainsail, lying against its mast."
DIP_ORDERED = "Dip the mainsail! Hands to the jeers and the tack."
DIPPED_BY_ORDER = "Dipped the mainsail; it stands to leeward of the mast."


def test_forced_round_and_left_to_herself_the_watch_dips_the_kept_settee(tmp_path):
    """The lead's ruling (3)(i) of 2026-11-10 (B3.3b's "Found on the way" 1): forced round lying to
    and left to herself, no fill away ordered, the record's forced-round branch finds her hove to
    no longer, and the watch dips a settee lying against its mast and says so. The settee's own
    dip is ordered (`dip_settee`, its hands from the watch on deck, its times and words, its holds
    keeping the settee's other orders off it), as the helmsman's watch boxes her off by the order;
    hoisted to leeward its sheet stands as it lay. Seed 7, 15 kn, from a settle of 1,200 s, hove
    to 600 s, the shift of eight points: forced round at +20 s onto the larboard tack, the fore
    topsail to the mast; "Her after yards full, she gathers way ...: hove to no longer." at +118 s
    with the watch's words, the dip ordered in the same tick; the yard lowered right down at +158
    s and passed round at +257 s; "Dipped the mainsail; it stands to leeward of the mast." at +356
    s, then clear of its mast and drawing whole on the larboard tack. Before, the line ended at
    "The helm keeps her full and by." and she sailed on full and by with the settee against its
    mast to +1,800 s, 57.1 of its 85.8 m2, at 2.76 kn (3.14 dipped), no word said."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    whole = settee.area_effective_m2  # as it draws clear of its mast at the settle
    world.submit("heave to")
    world.run(600)
    assert world.ship.extra["hove_to"]["sign"] == 1.0 and settee.lug_side == "larboard"
    start = world.clock.tick
    _shift_the_wind(world, -8.0)
    for _ in range(600):
        world.tick()
        if "hove_to" not in world.ship.extra:
            break
    (forced,) = [e for e in _after(world, start) if e.kind == "ship.forced_round"]
    assert "lies on the larboard tack" in forced.text and forced.tick - start == 20
    (filled,) = [e for e in _after(world, start) if e.kind == "ship.filled"]
    assert filled.text.startswith("Her after yards full, she gathers way"), filled.text
    assert filled.text.endswith("hove to no longer. The helm keeps her full and by. " + WATCH_DIPS)
    assert filled.data["settees_dipped"] == [SETTEE] and filled.severity.value == "urgent"
    at = filled.tick - start
    assert abs(at - 118) <= 15 and _first_tick(world, start, DIP_ORDERED) == at
    runner = world.ship.extra["evolutions"]
    (dip,) = [i for i in runner.instances if i.evo.id == "dip_settee"]
    assert not dip.waiting and SETTEE in dip.holds and dip.given is None  # the watch's, no order
    lowered = []
    for _ in range(600):
        world.tick()
        lowered.append(settee.yard_lowered)
        if any(e.kind == "sail.dipped" for e in _after(world, start)):
            break
    up = _first_tick(world, start, DIPPED_BY_ORDER)
    assert up is not None and abs(up - at - 238) <= 20, [e.text for e in _after(world, start)]
    assert any(lowered) and not lowered[-1]
    world.run(300)
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered
    assert lies == 1 and not P.against_the_mast(settee, lies)
    assert settee.area_effective_m2 == pytest.approx(whole, rel=0.01)
    assert "hove_to" not in world.ship.extra and world.ship.dyn.tack == "larboard"
    assert not [e for e in _after(world, start) if e.kind == "evolution.failed"]


@pytest.mark.parametrize("side", ["larboard", "starboard"])
def test_forced_round_with_nothing_aback_the_watch_dips_only_a_settee_against_its_mast(side):
    """The ruling (3)(i)'s other forced-round branch, the record's own turn on the bare fixture:
    she comes round through the wind with nothing aback (her yards square), and is hove to no
    longer at once. Her yard on the old lee, the larboard side, now her weather side as the deck
    reads the wind: the line says the watch dips it and the settee's dip is begun at once, its
    hands met (no crew), the yard held. On her new lee already: the line as before, nothing
    begun. Before, the line was the same both ways and nothing was begun."""
    ship = _under_plain_sail(brig_with_settee())
    runner = _bare(ship, CLOSE)  # the deck reads the wind on her larboard bow: her lee starboard
    for y in scripts.working_yards(ship):
        y.brace_angle = 0.0  # square: nothing aback on either tack
    ship.dyn.heading = math.radians(30.0)  # the north wind 30 degrees on her larboard bow
    settee = ship.sails[SETTEE]
    settee.lug_side = side
    timing = scripts.lying_to_timing()
    ship.extra["hove_to"] = {"yards": [], "sign": 1.0, "round_s": timing["round_s"] - 1.0}
    scripts.keep_lying_to(ship, 1.0, LIGHT_AIRS, runner)
    notes = ship.drain_notes()
    (line,) = [n for n in notes if n[1] == "ship.filled"]
    assert line[2].startswith(
        "She has been forced round through the wind onto the larboard tack with nothing aback: "
        "hove to no longer. The helm keeps her full and by."
    )
    assert "hove_to" not in ship.extra
    dips = [i for i in runner.instances if i.evo.id == "dip_settee"]
    if side == "starboard":  # to leeward of its mast already: nothing said, nothing begun
        assert line[2].endswith("The helm keeps her full and by.")
        assert "settees_dipped" not in line[4]
        assert dips == [] and DIP_ORDERED not in [n[2] for n in notes]
        return
    assert line[2].endswith(WATCH_DIPS) and line[4]["settees_dipped"] == [SETTEE]
    assert [n[2] for n in notes].index(DIP_ORDERED) > notes.index(line)
    assert len(dips) == 1 and dips[0].subject_id == SETTEE and not dips[0].waiting
    _run(runner, ship)
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered


def test_filled_on_her_own_tack_no_settee_is_dipped_by_the_watch():
    """The ruling (3)(i) is the forced round's branch: hove to on the larboard tack and filled
    there of herself, not forced round ("She has filled and gathers way ..."), the watch dips no
    settee, though one lies on her weather side (its yard put there by hand), the line as it was."""
    ship = _under_plain_sail(brig_with_settee())
    runner = _bare(ship, CLOSE)
    ship.dyn.heading = math.radians(30.0)  # 30 degrees off on the larboard tack
    ship.dyn.u = units.knots_to_ms(3.0)
    ship.sails[SETTEE].lug_side = "larboard"
    timing = scripts.lying_to_timing()
    ship.extra["hove_to"] = {"yards": [], "sign": -1.0, "full_s": timing["fill_s"] - 1.0}
    scripts.keep_lying_to(ship, 1.0, LIGHT_AIRS, runner)
    (line,) = [n for n in ship.drain_notes() if n[1] == "ship.filled"]
    assert line[2].startswith("She has filled and gathers way")
    assert line[2].endswith("The helm keeps her full and by.") and "settees_dipped" not in line[4]
    assert not [i for i in runner.instances if i.evo.id == "dip_settee"]


def test_paying_off_to_a_course_a_kept_settee_is_trimmed_with_the_boom_sails():
    """The lead's ruling (3)(ii) of 2026-11-10 (B3.3b's "Found on the way" 2): filled away to a
    course, she pays off to it with her yards and sheets trimmed to the wind as it draws aft
    (`_pay_off`), and a settee kept set is trimmed with the boom sails (`_kept_after_sails`). The
    script's own turn on the bare fixture, the north wind 80 degrees on her starboard bow, the
    settee on her lee hauled flat aft, "fill away and steer SW": at the first trim of the pay-off
    its sheet is drawn for the wind she has, as the head sheets are. Before, it kept its trim."""
    ship = _under_plain_sail(brig_with_settee())
    _bare(ship, -CLOSE)  # the deck reads the wind on her starboard bow
    ship.dyn.heading = math.radians(280.0)
    settee = ship.sails[SETTEE]
    settee.lug_side = "larboard"
    geo = yard_trim.sheet_geometry(ship, settee)
    yard_trim.set_sheet_angle(ship, settee, geo.floor)
    ship.extra["hove_to"] = {"yards": [], "sign": 1.0}
    fill = scripts.FillAwayScript(ship, {"course_deg": 225.0}, EVOLUTIONS["fill_away"].timing)
    fill.signed = True
    fill.phase = "pay_off"
    fill.new_course = fill.course
    fill.tick(1.0, LIGHT_AIRS, 1.0)
    assert fill.phase == "pay_off" and fill.swing is not None and not fill.not_laid
    # the wind on her bow, 80 degrees, short of the course's 135 and past close-hauled
    aim = max(scripts.close_hauled_true_angle(ship), math.radians(80.0))
    assert aim == pytest.approx(math.radians(80.0))
    wanted = max(geo.floor, min(geo.ceiling, yard_trim.wanted_sheet_angle(settee.curve_class, aim)))
    assert wanted > geo.floor + math.radians(5.0)
    assert yard_trim.read_sheet(ship, settee).angle == pytest.approx(wanted, abs=1e-6)
    jib = ship.sails["jib"]
    jib_geo = yard_trim.sheet_geometry(ship, jib)
    jib_wanted = yard_trim.wanted_sheet_angle(jib.curve_class, aim)
    assert yard_trim.read_sheet(ship, jib).angle == pytest.approx(
        max(jib_geo.floor, min(jib_geo.ceiling, jib_wanted)), abs=1e-6
    )
    assert settee.lug_side == "larboard"  # trimmed on her lee, where it hangs


MANOEUVRES_THAT_CHANGE_IT = ("tack", "wear", "boxhaul", "box_off", "wear_short_round", "fill_away")


@pytest.mark.parametrize("evolution", MANOEUVRES_THAT_CHANGE_IT)
def test_each_manoeuvre_that_may_change_the_settee_holds_it_from_the_order(evolution, monkeypatch):
    """The lead's ruling (3)(iii) of 2026-11-10, the smaller way (B3.3b's review's finding): the
    runner reads an evolution's holds once, at the order, and the tack's, the wear's, the box-
    haul's and the fill away's named a settee only once its change had begun. Each manoeuvre
    that may change a settee now names the settees set from the order (`settees_held`), so that
    no order of the settee's is begun while it may be changed; one clewed up is not named. A ship
    with no settee holds what she held (the brig: her ship and her yards)."""
    evo = EVOLUTIONS[evolution]
    ship = _under_plain_sail(brig_with_settee())
    _bare(ship, -CLOSE)
    script = scripts.SCRIPTS[evo.script](ship, dict(evo.params), evo.timing)
    assert SETTEE in script.holds()
    ship.sails[SETTEE].state = SailState.IN_THE_GEAR
    again = scripts.SCRIPTS[evo.script](ship, dict(evo.params), evo.timing)
    assert SETTEE not in again.holds() and scripts.settees_held(ship) == set()
    brig = _under_plain_sail(load_ship("data/ships/brig.yaml"))
    _bare(brig, -CLOSE)
    held = scripts.SCRIPTS[evo.script](brig, dict(evo.params), evo.timing).holds()
    assert scripts.settees_held(brig) == set()
    monkeypatch.setattr(scripts, "settees_held", lambda ship: set())  # as before the ruling
    assert scripts.SCRIPTS[evo.script](brig, dict(evo.params), evo.timing).holds() == held


def test_an_order_of_the_settee_waits_for_the_fill_away_that_dips_it(tmp_path):
    """The ruling (3)(iii) on the case B3.3b's review measured: the fixture forced round hove to in
    15 kn, "fill away", and "furl the mainsail" 30 s after, while the settee lies on deck to be
    dipped. It now waits its turn behind the fill away, which holds the settee from the order,
    and is begun when she is filled away ("Lay aloft and furl the mainsail.", +217 s), furling the
    settee hoisted to leeward of its mast on its yard aloft.
    Before, it began at +31 s ("Hands to furl the mainsail.") while the yard was on deck, the dip
    hoisted it at +157 s, and "Furled the mainsail on its yard on deck." was said at +201 s of a
    yard hoisted."""
    world = _world(tmp_path, settle_s=1200)
    settee = world.ship.sails[SETTEE]
    world.submit("heave to")
    world.run(600)
    _shift_the_wind(world, -8.0)
    world.run(60)
    assert world.ship.extra["hove_to"]["sign"] == -1.0 and settee.lug_side == "larboard"
    start = world.clock.tick
    assert world.submit("fill away").kind == "order.accepted"
    world.run(30)
    assert settee.yard_lowered
    assert world.submit("furl the mainsail").kind == "order.accepted"
    runner = world.ship.extra["evolutions"]
    (filling,) = [i for i in runner.instances if i.evo.id == "fill_away"]
    (furling,) = [i for i in runner.instances if i.evo.id == "furl_settee"]
    assert furling.waiting and furling.waiting_for is None  # its turn, behind the fill away
    assert SETTEE in furling.holds and SETTEE in filling.holds
    for _ in range(900):
        world.tick()
        if settee.state is SailState.FURLED:
            break
    filled = [e.tick - start for e in _after(world, start) if e.kind == "ship.filled_away"]
    hoisted = _first_tick(world, start, "Dipped the mainsail; hoisted on the starboard side")
    furl = [e for e in _after(world, start) if e.kind == "sail.furled"]
    begun = [e for e in _after(world, start) if e.kind == "evolution.started" and "furl" in e.text]
    assert filled and hoisted is not None and furl and begun, [e.text for e in _after(world, start)]
    assert hoisted < filled[0] <= begun[0].tick - start < furl[0].tick - start
    assert "on deck" not in furl[0].text
    assert settee.state is SailState.FURLED and not settee.yard_lowered
    assert settee.lug_side == "starboard"


# The lugger's tack and wear at seed 7 from B3.4's settle (15 kn, 292.5 degrees): every line but
# the leeway's, with its tick after the order, the same on the tree before this step and after
# (the trace of Ext §10.1, measured both ways by B3.3 and found identical, the frigate's tack,
# wear and heave-to and the brig's with them). One line moved since, words only, every tick the
# same: the wear's at 36 s, "Wind aft. Squared the head yards; shifted over the sheets; ..."
# until B3.4b, where with no head yards (her lug yards are no braced yards) it says nothing of
# squaring them (the lead's ruling (3) of 2026-11-07; Luce 1884 p. 424, the head yards laid
# square with the wind aft).
LUGGER_TACK = [
    (0, "Order: tack ship."),
    (1, "All hands! (to tack ship)"),
    (
        1,
        "Ready about. Helm's a-lee; ease off the head sheets; haul aft the mizen sheet; lower the "
        "foresail and the mainsail.",
    ),
    (1, "All hands about ship."),
    (23, "Dip the foresail and the mainsail; shift the tacks to the weather bow."),
    (23, "Draw jib; trim aft the head sheets."),
    (90, "All hands on deck."),
    (
        137,
        "Dipped the foresail and the mainsail; hoisted on the starboard side, to leeward of the "
        "masts.",
    ),
    (180, "Tacked; braced up on the larboard tack, heading ENE (68°)."),
    (180, "Piped down; the starboard watch has the deck."),
]
LUGGER_WEAR = [
    (0, "Order: wear ship."),
    (1, "All hands! (to wear ship)"),
    (1, "Stand by to wear ship. Up helm; brace in the after yards."),
    (1, "Stations for wearing ship."),
    (
        36,
        "Wind aft. Shifted over the sheets; hauled out and braced up. Lowered the foresail and "
        "the mainsail to dip them.",
    ),
    (90, "All hands on deck."),
    (
        149,
        "Dipped the foresail and the mainsail; hoisted on the starboard side, to leeward of the "
        "masts.",
    ),
    (171, "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)."),
    (171, "Piped down; the starboard watch has the deck."),
]


@pytest.mark.parametrize("order, lines", [("tack ship", LUGGER_TACK), ("wear ship", LUGGER_WEAR)])
def test_the_luggers_tack_and_wear_are_as_they_were(order, lines):
    """Ext §10.1, the trace: the lugger's dip and lowering take her lugs alone (`lugger_lugs`),
    her lines and ticks as before the settee step (the wear's wind-aft line's words since moved
    by B3.4b, above)."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, LUGGER, scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    for i in range(2400):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    start, n0 = world.clock.tick, len(world.log.all())
    world.submit(order)
    for _ in range(200):
        world.tick()
    got = [
        (e.tick - start, e.text)
        for e in world.log.all()[n0:]
        if e.kind != "ship.leeway" and e.tick - start <= lines[-1][0]
    ]
    assert got == lines


# ---------------------------------------------------------------------------
# The truths, drafted for Phase 5 (docs/design/Build-Ships.md §15): 7-198 and 7-199
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "knots, lowered_s, haul_s, factor",
    [(15.0, 155, 97, 1.33), (20.0, 161, 96, 1.51)],
)
def test_truth_7_198_the_settee_in_stays_is_kept_drawing_its_ourse_to_leeward_and_dipped_last(
    tmp_path, knots, lowered_s, haul_s, factor
):
    """Truth 7-198 (drafted; Ext §10.3 item 1; D46 rules 2 and 3, D3(b)): in stays the settee is
    kept drawing as a ship's mizen is, its ourse braced to leeward as the helm goes down, and its
    yard is changed last, after the head yards are swung. Each rule is carried over by judgement
    from a ship's mizen (Bourdé 1765 p. 87; Steel 1794 vol. II p. 316; Boteler p. 163) to the
    bilander's settee, which Röding (1794 vol. II col. 581) has lowered and shifted round in going
    about (D1(a)); rule 2 is pinned on her own dip, the yard lowered and passed round, not against
    a brig (D46(d)).

    The fixture `brig_with_settee()` at seed 7, from close-hauled on the starboard tack in 15 and
    20 kn (B3.4's settle: 2,400 s at 292.5 degrees, 67.5 degrees off). Measured on the owner's
    machine (2026-11-07), B3.3: at helm's a-lee + 1 tick the settee set at its floor, 8 degrees,
    the words "haul aft the mainsail sheet and brace the ourse to leeward"; "Let go and haul" at
    97 s and 96 s; the head yards' swing ended and the yard lowered at 155 s and 161 s ("Dip the
    mainsail: lower the yard, pass it round abaft the mast ..."); down 159 and 181 ticks
    (`SETTEE_DIP_S` 120 by her factor of 1.33 and 1.51), its side larboard to starboard; hoisted at
    314 s and 342 s, "Tacked" at 318 s and 342 s; at +400 s on the larboard tack 67.7 and 66.8
    degrees off. Judged by her heading and tack at a set time, never by the "Tacked" line
    (D13(a)). Rule 5's clause is not pinned here: in her own tack at seed 7 the settee is never
    aback (its single sheet lies it to leeward of the wind; Ext §5.10's measure, the tuning notes),
    so that half goes to the lead. To be measured again on the bilander's file (B4) in Phase 5.
    The words since, every tick the same (B3.4b, the lead's ruling (2) of 2026-11-07; Luce 1884
    pp. 421, 428, 446): her after yards hauled by "Main-topsail haul." with her fore tack kept
    fast, and that line "Rise fore tack and sheet. Let go and haul. ..." (at 97 s in 15 kn), where
    they were "Rise tacks and sheets. Main-topsail haul." and "Let go and haul. ..."."""
    world = _world(tmp_path, knots=knots)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("tack ship")
    world.tick()
    assert settee.is_set and _deg(settee.sheet_angle) == pytest.approx(LUG_FLOOR_DEG, abs=1.0)
    line = next(e.text for e in _after(world, start) if "Helm's a-lee" in e.text)
    assert "haul aft the mainsail sheet and brace the ourse to leeward" in line, line
    sides, lowered = [], []
    for i in range(2, 601):
        world.tick()
        if settee.yard_lowered:
            lowered.append(i)
        sides.append(settee.lug_side)
        if i == 400:
            at_400 = (world.ship.dyn.tack, abs(_rel_deg(world)))
    haul = _first_tick(world, start, "Let go and haul")
    swung = _first_tick(world, start, "Dip the mainsail: lower the yard")
    tacked = _first_tick(world, start, "Tacked")
    hoisted = _first_tick(world, start, "Dipped the mainsail; hoisted on the starboard side")
    assert abs(haul - haul_s) <= 5 and haul < swung
    assert lowered[0] >= swung and abs(lowered[0] - lowered_s) <= 10
    down = len(lowered)
    assert lowered == list(range(lowered[0], lowered[0] + down))  # one spell, not two
    assert abs(down - scripts.SETTEE_DIP_S * factor) <= 10
    assert sides[0] == "larboard" and sides[-1] == "starboard"
    assert hoisted is not None and tacked is not None and tacked >= hoisted
    assert at_400[0] == "larboard" and abs(at_400[1] - 67.5) <= 5.0


@pytest.mark.parametrize("knots, crossed_s, hoisted_s", [(15.0, 66, 152), (20.0, 55, 168)])
def test_truth_7_199_in_wearing_the_settee_is_lowered_as_she_bears_up_and_hoisted_past_the_wind(
    tmp_path, knots, crossed_s, hoisted_s
):
    """Truth 7-199 (drafted; Ext §10.3 item 2; D46(d) rule 4 as reworded): in wearing the settee is
    lowered as she bears up and hoisted again on the new lee once the stern is past the wind.
    Steel's order for a ship's mizen (1794 vol. II pp. 321-322: hauled up as she bears up, hauled
    out "as soon as the stern has passed the wind"), carried over by judgement to the dip D1(a)
    gives the settee; the truth pins the order of events, not a clewing up.

    The fixture at seed 7, from close-hauled on the starboard tack in 15 and 20 kn (B3.4's settle).
    Measured on the owner's machine (2026-11-07), B3.3: lowered at "up helm" + 1 tick ("Up helm;
    lower the mainsail; brace in the after yards"); the wind across the stern to the larboard
    quarter at 66 s and 55 s; hoisted at 152 s and 168 s, the wind then 99.6 and 133.6 degrees on
    the larboard side ("Hoisted the mainsail on the starboard side, to leeward of the mast; the
    wind is past the stern."); "Wore" at 478 s and 520 s; at +600 s on the larboard tack 67.3
    degrees off, both. Judged by her heading and tack at a set time (D13(a)). To be measured again
    on the bilander's file (B4) in Phase 5."""
    world = _world(tmp_path, knots=knots)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("wear ship")
    lowered, crossed, hoist = [], None, None
    for i in range(1, 601):
        world.tick()
        rel = _rel_deg(world)
        if settee.yard_lowered:
            lowered.append(i)
        if crossed is None and rel < 0 and abs(rel) > 90:
            crossed = i
        if hoist is None and lowered and not settee.yard_lowered:
            hoist = (i, rel)
        if i == 600:
            at_600 = (world.ship.dyn.tack, abs(rel))
    up = next(e.text for e in _after(world, start) if "Up helm" in e.text)
    assert "Up helm; lower the mainsail; brace in the after yards" in up, up
    assert lowered and lowered[0] <= 5
    assert abs(crossed - crossed_s) <= 10 and abs(hoist[0] - hoisted_s) <= 10
    assert hoist[0] > crossed and hoist[1] < 0.0  # the wind on the new side of the stern
    assert settee.is_set and settee.lug_side == "starboard"
    assert at_600[0] == "larboard" and abs(at_600[1] - 67.5) <= 5.0
