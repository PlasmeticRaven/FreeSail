"""The lee ports, built on the heel (package 75, L2) and the roll (L3; docs/design/Build-Ships.md
§7.1, §7.2, §14.1): a gun's port shut when the sea comes within a foot of its sill, opened again
six inches clear of that, the gun behind it run in and silent, its loading going on, the log told
once a change of state a deck and side.

The figures are the rule's arithmetic on each file's own triples, and the tables below are the
tuning notes' "The port triples before L2", typed from them, so that the files, the notes and
the rule are held to one another. Her heel is the test's hand wherever a heel is named, by
7-135's form (`Battery.tick` with a `Firer`) or by `heeled` below; one test heels her by her
own sails, and one rolls her by her own sea. Her roll is the test's hand likewise, on a `Firer`
or on the World's motion (truth 7-190's draft, at the end).
"""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path

import pytest

from freesail import units
from freesail.api import readings  # noqa: F401  (it loads its rows, in their order)
from freesail.api.action_readings import _guns as guns_reading
from freesail.api.action_readings import _ports_shut_words
from freesail.api.session import make_world, ship_factory
from freesail.combat import action, ports
from freesail.combat import shot as S
from freesail.combat.guns import Battery, FireMode, Firer, Target, _is_lee, battery_of, magazine
from freesail.core import replay
from freesail.core.clock import TICK_SECONDS
from freesail.core.events import Severity
from freesail.core.world import Scenario
from freesail.crew.quarters import quarters_of
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import Charge, Gun
from freesail.ship.profile import half_breadth_at_sill, ports_of

SEED = 7
FRIGATE = "data/ships/frigate-36.yaml"
BRIG = "data/ships/brig.yaml"
MERCHANT_BRIG = "data/ships/merchant-brig.yaml"
CUTTER = "data/ships/cutter.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"
TOPSAIL_SCHOONER = "data/ships/topsail-schooner.yaml"
LUGGER = "data/ships/lugger.yaml"
SMACK = "data/ships/smack.yaml"
SIXTY_FOUR = "data/ships/sixty-four.yaml"
RAZEE = "data/ships/razee-44.yaml"
LAUNCH = "data/ships/boat-launch-31.yaml"
# A real checkpoint of a cutter with her guns cast loose, written by the commit before package
# 75's stage 0 (c5140483): her guns hold no deck and her hull no profile, her sills 1.5 m. A
# kept save (§16.2): a change that breaks it is mended with a class default or a step in
# `core.replay._rebind`, never by changing it (`tests/test_checkpoint.py`).
PRE_75_CUTTER = "tests/fixtures/saves/pre-75-cutter-guns-cast-loose.checkpoint"

SHUT_M = S.PORT_SHUT_M
REOPEN_M = ports.PORT_REOPEN_M
# The hold (the lead's ruling of 2026-11-06): a shut port opens only once the sea has kept from
# its sill a minute. The rule's tests read it at ticks of their own; `HOLD` ticks after the sea
# was last at a sill is the first tick at which that port may open
HOLD = round(ports.PORT_HOLD_S / TICK_SECONDS)


def shut_heel(sill: float, half: float) -> float:
    """§7.1's arithmetic: the heel at which the sill lowered comes to a foot of the water."""
    return math.degrees(math.asin((sill - SHUT_M) / half))


def open_heel(sill: float, half: float) -> float:
    """And the heel at which it stands `PORT_REOPEN_M` clear of that again."""
    return math.degrees(math.asin((sill - SHUT_M - REOPEN_M) / half))


def firer_at(heel_deg: float, half_beam_m: float = 3.0, roll_deg: float = 0.0) -> Firer:
    return Firer(
        heel_deg=heel_deg,
        roll_deg=roll_deg,
        sea_height_m=0.0,
        weather_factor=1.0,
        half_beam_m=half_beam_m,
        heading_rad=0.0,
        position=None,
    )


def a_gun(
    x: float = 0.0,
    sill: float = 1.0,
    deck: str | None = "upper",
    side: str | None = "starboard",
    place: str = "broadside",
    gid: str = "gun.1.starboard",
) -> Gun:
    """A gun standing at a place of the test's choosing: on a triple the file has no gun at,
    or as a gun pickled before package 75 stands."""
    return Gun(
        id=gid,
        cls="long",
        rating_kn=0.0,
        kind="long",
        pounder=6.0,
        place=place,
        number=1,
        side=side,
        x_m=x,
        height_m=sill,
        deck=deck,
    )


def the_battery_of_one(path: str, gun: Gun) -> Battery:
    ship = load_ship(path)
    ship.guns = {gun.id: gun}
    return Battery(ship)


def _at_x(ship, x: float, side: str = "starboard") -> Gun:
    """The gun of that side at that place along her."""
    (gun,) = [g for g in ship.guns.values() if g.x_m == x and g.side == side]
    return gun


def cast_loose(ship) -> None:
    """Her guns cast loose by hand: the log's line is the guns' (the rule's own head)."""
    for gun in ship.guns.values():
        gun.cast_loose = True


def lines_of(ship, *kinds: str) -> list[tuple]:
    """The notes the battery has left for the log (`Ship.note`) since last asked."""
    notes = [n for n in ship.drain_notes() if len(n) == 5]
    return [n for n in notes if not kinds or n[1] in kinds]


# -- the tables: docs/dev/TuningNotes.md, "The port triples before L2" ------------------------

# (deck, x, sill, half-breadth, the "Shut at" column)
FRIGATE_TRIPLES = (
    ("upper", -16.50, 2.51, 4.84, 27.1),
    ("upper", -13.80, 2.42, 5.13, 24.4),
    ("upper", -11.00, 2.35, 5.30, 22.7),
    ("upper", -8.20, 2.28, 5.44, 21.3),
    ("upper", -5.50, 2.24, 5.52, 20.5),
    ("upper", -2.80, 2.21, 5.57, 20.0),
    ("upper", 0.00, 2.19, 5.60, 19.7),
    ("upper", 2.80, 2.20, 5.60, 19.8),
    ("upper", 5.50, 2.23, 5.60, 20.1),
    ("upper", 8.20, 2.28, 5.57, 20.8),
    ("upper", 11.00, 2.34, 5.48, 21.8),
    ("upper", 13.80, 2.42, 5.31, 23.5),
    ("upper", 16.50, 2.51, 4.83, 27.2),
    ("quarterdeck", -17.50, 4.28, 4.52, 61.6),
    ("quarterdeck", -14.00, 4.15, 4.95, 51.0),
    ("quarterdeck", -10.50, 4.05, 5.21, 46.0),
    ("quarterdeck", -7.00, 3.97, 5.37, 43.0),
    ("quarterdeck", -4.50, 4.11, 5.42, 44.6),
    ("forecastle", 14.00, 4.08, 5.08, 48.0),
    ("forecastle", 17.50, 4.25, 4.56, 59.9),
)
BRIG_TRIPLES = (
    ("upper", -11.55, 1.89, 3.40, 27.8),
    ("upper", -9.10, 1.77, 3.71, 23.3),
    ("upper", -6.50, 1.66, 3.96, 20.0),
    ("upper", -3.90, 1.60, 4.13, 18.3),
    ("upper", -1.30, 1.57, 4.21, 17.5),
    ("upper", 1.30, 1.58, 4.25, 17.5),
    ("upper", 3.90, 1.62, 4.21, 18.2),
    ("upper", 6.50, 1.70, 4.14, 19.7),
    ("upper", 9.10, 1.84, 3.80, 23.8),
    ("upper", 12.00, 2.02, 2.87, 36.7),
)
# the brig's but for her own guns' two, at x -4.0 and +4.0 (the notes, above the table)
MERCHANT_BRIG_TRIPLES = tuple(
    {
        -3.90: ("upper", -4.00, 1.60, 4.12, 18.3),
        3.90: ("upper", 4.00, 1.62, 4.21, 18.2),
    }.get(t[1], t)
    for t in BRIG_TRIPLES
)
CUTTER_TRIPLES = (
    ("upper", -4.75, 1.01, 2.56, 16.0),
    ("upper", -3.50, 1.00, 2.69, 15.0),
    ("upper", -2.35, 1.00, 2.77, 14.5),
    ("upper", -0.50, 1.03, 2.85, 14.7),
    ("upper", 0.02, 1.04, 2.86, 14.9),
    ("upper", 2.50, 1.15, 2.85, 17.3),
    ("upper", 3.58, 1.23, 2.79, 19.4),
)
SCHOONER_TRIPLES = (
    ("upper", -10.86, 1.19, 2.79, 18.5),
    ("upper", -8.40, 1.07, 3.06, 14.5),
    ("upper", -7.50, 1.04, 3.14, 13.5),
    ("upper", -2.08, 0.95, 3.51, 10.6),
    ("upper", 0.00, 0.96, 3.61, 10.5),
    ("upper", 4.81, 1.11, 3.56, 13.1),
    ("upper", 8.40, 1.30, 3.06, 19.0),
    ("upper", 10.50, 1.44, 2.29, 29.7),
)
TRIPLES = {
    FRIGATE: FRIGATE_TRIPLES,
    BRIG: BRIG_TRIPLES,
    MERCHANT_BRIG: MERCHANT_BRIG_TRIPLES,
    CUTTER: CUTTER_TRIPLES,
    PRIVATEER: SCHOONER_TRIPLES,
    TOPSAIL_SCHOONER: SCHOONER_TRIPLES,
}
# "The lowest shut heels": her lowest with a gun in it, deck by deck, fit by fit
LOWEST_WITH_A_GUN = (
    (FRIGATE, None, "upper", 19.7),
    (FRIGATE, None, "quarterdeck", 43.0),
    (BRIG, None, "upper", 17.5),
    (MERCHANT_BRIG, None, "upper", 18.2),
    (CUTTER, "carronades", "upper", 14.7),
    (CUTTER, "long guns", "upper", 14.7),
    (PRIVATEER, "long tom", "upper", 13.5),
    (PRIVATEER, "letter of marque", "upper", 10.5),
    (SIXTY_FOUR, "ardent class 1784", "lower", 10.55),
    (SIXTY_FOUR, "ardent class 1784", "upper", 34.69),
    (RAZEE, "as carried 1796", "upper", 14.5),
    (RAZEE, "as carried 1796", "quarterdeck", 42.02),
    (RAZEE, "as carried 1796", "forecastle", 43.84),
)


def _triples_of(path: str):
    """The file's own triples, read through the profile."""
    profile = load_spec(path).hull.profile
    return [(word, *t) for word, _ in profile.ports_m for t in ports_of(profile, word)]


@pytest.mark.parametrize("path", sorted(TRIPLES))
def test_each_file_holds_the_triples_the_notes_have(path):
    """Each triple of the file against the notes' row, and the notes' shut heel against the
    rule's arithmetic on it."""
    have = sorted(_triples_of(path), key=lambda t: (t[0], t[1]))
    want = sorted(TRIPLES[path], key=lambda t: (t[0], t[1]))
    assert len(have) == len(want)
    for (deck, x, sill, half), (w_deck, w_x, w_sill, w_half, w_shut) in zip(
        have, want, strict=True
    ):
        assert (deck, x, sill, half) == (w_deck, w_x, w_sill, w_half)
        assert shut_heel(sill, half) == pytest.approx(w_shut, abs=0.05), (deck, x)


@pytest.mark.parametrize("path", [LUGGER, SMACK])
def test_the_lugger_and_the_smack_have_no_port_and_no_gun_to_shut(path):
    spec = load_spec(path)
    assert not spec.hull.profile.ports_m and spec.armament is None
    assert battery_of(load_ship(path)) is None


@pytest.mark.parametrize(
    "path,triple",
    [(path, t) for path in sorted(TRIPLES) for t in TRIPLES[path]],
    ids=lambda v: v.split("/")[-1].removesuffix(".yaml") if isinstance(v, str) else f"{v[0]}{v[1]}",
)
def test_each_triple_shuts_and_reopens_at_the_rules_arithmetic(path, triple):
    """A gun stood on the triple, its half-breadth the profile's: open a hair below the heel
    that shuts it, shut a hair above, at once; shut still a hair above the heel that opens it,
    and a hair below it held a tick short of the minute and open at the minute (the lead's
    ruling of 2026-11-06; before it, open at once). Both heels are §7.1's, on the sill lowered
    by `half × sin(heel)`."""
    deck, x, sill, half, _ = triple
    battery = the_battery_of_one(path, a_gun(x, sill, deck))
    gid = "gun.1.starboard"
    shut, reopen = shut_heel(sill, half), open_heel(sill, half)
    assert reopen < shut
    assert ports.update(battery, firer_at(shut - 0.01), 0) == (frozenset(), frozenset())
    assert battery._shut == frozenset()
    assert ports.update(battery, firer_at(shut + 0.01), 1) == (frozenset({gid}), frozenset())
    assert battery._shut == {gid}
    assert ports.update(battery, firer_at(reopen - 0.01), HOLD) == (frozenset(), frozenset())
    assert ports.update(battery, firer_at(reopen + 0.01), 1 + HOLD) == (frozenset(), frozenset())
    assert battery._shut == {gid}
    opened = ports.update(battery, firer_at(reopen - 0.01), 1 + HOLD)
    assert opened == (frozenset(), frozenset({gid}))
    assert battery._shut == frozenset()


def test_the_reopening_is_six_inches_clear_in_the_sill_lowered():
    """The margin read off the sill itself: shut at a foot, opened at a foot and six inches,
    as `lee_port_shut` and `PORT_REOPEN_M` say it."""
    assert REOPEN_M == 0.15 and SHUT_M == 0.3048
    half = 2.85
    sill = 1.03

    def lowered(heel: float) -> float:
        return sill - half * math.sin(math.radians(heel))

    shuts, opens = shut_heel(sill, half), open_heel(sill, half)
    assert lowered(shuts) == pytest.approx(SHUT_M)
    assert lowered(opens) == pytest.approx(SHUT_M + REOPEN_M)
    assert S.lee_port_shut(sill, shuts + 0.01, half)
    assert not S.lee_port_shut(sill, shuts - 0.01, half)
    assert S.lee_port_shut(sill - REOPEN_M, opens + 0.01, half)
    assert not S.lee_port_shut(sill - REOPEN_M, opens - 0.01, half)


@pytest.mark.parametrize("path,fit,deck,lowest", LOWEST_WITH_A_GUN)
def test_every_gun_of_the_fit_shuts_at_the_heel_of_its_own_place(path, fit, deck, lowest):
    """Every port gun of the fit, on the heel its own sill and the side at it give, both
    sides of her; the lowest of the deck the notes' figure. A gun between two triples reads
    them straight between (`half_breadth_at_sill`). A sill higher than the side is broad (the
    64's quarterdeck and forecastle) never shuts on the heel, on her beam ends or short of it."""
    ship = load_ship(path, fit=fit)
    profile = ship.hull.spec.profile
    heels = []
    for gun in ship.guns.values():
        if gun.place not in ports.PORT_PLACES:
            continue
        half = half_breadth_at_sill(profile, gun.deck, gun.x_m)
        toward = 1.0 if gun.side == "starboard" else -1.0
        one = Battery(ship)
        if (gun.height_m - SHUT_M) / half >= 1.0:
            ports.update(one, firer_at(toward * 89.9), 0)
            assert gun.id not in one._shut, gun.id
            continue
        shut = shut_heel(gun.height_m, half)
        if gun.deck == deck:
            heels.append(shut)
        ports.update(one, firer_at(toward * (shut - 0.01)), 0)
        assert gun.id not in one._shut, gun.id
        ports.update(one, firer_at(toward * (shut + 0.01)), 1)
        assert gun.id in one._shut, gun.id
    assert min(heels) == pytest.approx(lowest, abs=0.05), (fit, deck)


# -- both sides -------------------------------------------------------------------------------


@pytest.mark.parametrize("heel,lee", [(25.0, "starboard"), (-25.0, "larboard")])
def test_she_shuts_the_side_she_heels_to_and_never_the_other(heel, lee):
    """Heel positive to starboard. The side follows `guns._is_lee`; the weather side's dip is
    the roll less the heel, below nought on the heel alone, so at any heel it stays open."""
    ship = load_ship(BRIG)
    battery = Battery(ship)
    shut, opened = ports.update(battery, firer_at(heel), 0)
    assert not opened
    assert shut == battery._shut
    assert shut, "at 25 degrees the brig's midships ports are under"
    for gun in ship.guns.values():
        if gun.id in shut:
            assert gun.side == lee and _is_lee(gun, heel)
    # the same ports of the other side at the other heel, number for number
    other = Battery(ship)
    ports.update(other, firer_at(-heel), 0)

    def numbers(ids):
        return sorted((ship.guns[g].place, ship.guns[g].x_m) for g in ids)

    assert numbers(other._shut) == numbers(shut)
    assert not (other._shut & shut)
    # she goes about: the new lee side shuts at once, and the old one is held until the sea
    # has kept from its sills a minute (the lead's ruling of 2026-11-06; before it, it opened
    # at once)
    ports.update(battery, firer_at(-heel), 1)
    assert battery._shut == shut | other._shut
    ports.update(battery, firer_at(-heel), HOLD)
    assert battery._shut == other._shut


@pytest.mark.parametrize("heel", [80.0, -80.0])
def test_the_weather_side_never_shuts_on_the_heel_alone(heel):
    ship = load_ship(FRIGATE)
    battery = Battery(ship)
    ports.update(battery, firer_at(heel), 0)
    weather = "larboard" if heel > 0.0 else "starboard"
    assert battery._shut, "she is on her beam ends, every lee port under"
    assert all(ship.guns[g].side != weather for g in battery._shut)


# -- a shut gun: run in, its loading going on, and silent --------------------------------------


def test_a_shut_gun_is_not_wanted_run_out_and_its_loading_goes_on():
    """§7.2's `wants_work`. Empty it wants loading; loaded and unprimed, priming; loaded and
    primed it has no work, where with the port open it wants running out."""
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    gun = ship.guns["gun.1.starboard"]
    battery._shut = frozenset({gun.id})
    assert battery.wants_work(gun)  # empty
    gun.loaded = Charge.ROUND
    assert battery.wants_work(gun)  # unprimed
    gun.primed = True
    assert not battery.wants_work(gun)
    battery._shut = frozenset()
    assert battery.wants_work(gun)  # the port open, it wants running out
    assert not gun.run_out


def test_a_gun_run_out_when_its_port_shuts_is_run_in_and_stays_loaded():
    """The lid lowered on a gun housed (judgement, §7.2). A running out or a pointing in hand
    is given over, and neither comes back while the port is shut."""
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    gun = ship.guns["gun.1.starboard"]
    gun.loaded, gun.primed, gun.run_out = Charge.ROUND, True, True
    service = battery.services[gun.id]
    service.phase = [n for n, _ in battery._phases(gun)].index("point")
    battery.tick(1.0, None, firer_at(30.0), None, None, 0, None)
    assert gun.id in battery._shut
    assert not gun.run_out and gun.loaded is Charge.ROUND and gun.primed
    assert service.idle
    # the far side's own gun, on the weather side, is left as it stood
    other = ship.guns["gun.1.larboard"]
    assert other.id not in battery._shut


def test_a_gun_named_to_fire_behind_a_shut_port_is_dropped_with_its_line():
    """§7.2's words, and the gun keeps its charge. A chaser's name reads as the deck says it."""
    ship = load_ship(BRIG)
    battery = Battery(ship)
    gun = next(g for g in ship.guns.values() if g.number == 3 and g.side == "larboard")
    chaser = next(g for g in ship.guns.values() if g.place == "bow")
    for g in (gun, chaser):
        g.loaded, g.primed, g.run_out = Charge.ROUND, True, True
    battery.single = [gun.id, chaser.id]
    battery._shut = frozenset({gun.id, chaser.id})
    battery._fire(None, firer_at(0.0), None, None, 0, None, None)
    assert battery.single == [] and gun.fired == 0 and chaser.fired == 0
    assert gun.loaded is Charge.ROUND
    notes = lines_of(ship, "guns.port_shut")
    assert [n[2] for n in notes] == [
        "The No. 3 larboard gun's port is shut; the sea is at its sill.",
        f"The {chaser.side} bow chaser's port is shut; the sea is at its sill.",
    ]
    assert notes[0][0] == "notable" and notes[0][3] == gun.id


def test_a_shot_across_her_bows_dropped_leaves_no_word_behind():
    """The chaser named for the shot across her bows is behind a shut port: the signal goes
    with it, and the next gun fired is not taken for it."""
    ship = load_ship(BRIG)
    battery = Battery(ship)
    chaser = next(g for g in ship.guns.values() if g.place == "bow")
    chaser.loaded, chaser.primed, chaser.run_out = Charge.ROUND, True, True
    battery.single, battery.across_bows = [chaser.id], True
    battery._shut = frozenset({chaser.id})
    battery._fire(None, firer_at(0.0), None, None, 0, None, None)
    assert battery.single == [] and not battery.across_bows


def test_a_named_gun_dropped_leaves_the_shot_across_her_bows_to_the_gun_still_named():
    """The signal goes when no named gun is left to carry it; while one is, it stays."""
    ship = load_ship(BRIG)
    battery = Battery(ship)
    shut, other = ship.guns["gun.1.starboard"], ship.guns["gun.2.starboard"]
    battery.single, battery.across_bows = [shut.id, other.id], True
    battery._shut = frozenset({shut.id})
    assert not battery.ready(other)
    battery._fire(None, firer_at(0.0), None, None, 0, None, None)
    assert battery.single == [other.id] and battery.across_bows


def test_a_shut_gun_stays_out_of_the_fire_as_they_bear_and_at_the_word():
    """Ready by every other measure (a gun that needs no running out, as a swivel at a port
    place would be, or one the test leaves run out), the shut port alone keeps it silent."""
    w = _at_quarters(CUTTER)
    serving = _Serving(w, "starboard")
    battery, gun = serving.battery, _at_x(w.ship, 2.5)
    assert battery.ready(gun)
    battery._shut = frozenset({gun.id})
    firer = replace(action._firer(w, w.ship), heel_deg=0.0)
    for word in (None, "starboard"):
        battery.word = word
        battery._fire(
            serving.quarters, firer, serving.mark, serving.rng, 1, lambda *a, **k: [], None
        )
        assert gun.fired == 0


def test_a_round_behind_a_shut_port_ends_primed_without_the_point():
    """§7.2: the loading goes on to primed, and neither the running out nor the pointing is
    worked behind the lid."""
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    gun = ship.guns["gun.1.starboard"]
    gun.loaded = Charge.ROUND
    battery._shut = frozenset({gun.id})
    prime = dict(battery._phases(gun))["prime"]
    battery._work(gun, prime + 0.01, magazine(ship), 0)
    assert gun.primed and battery.services[gun.id].idle and not gun.run_out


def test_a_round_behind_a_shut_port_is_not_timed_for_the_drill():
    """The drill's mean and best are "from sponge to point" (`api/practice_readings.py`): a
    round from the sponge to primed behind the lid, with no running out and no point, is not
    one. Run out and pointed when the port opens, the next whole round is timed."""
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    mag = magazine(ship)

    def served(gun, seconds, at_phase=None):
        """As `Battery.tick` serves it: a second's work while it wants any. `at_phase` is the
        phase at which the port shuts on it."""
        for second in range(seconds):
            if not battery.wants_work(gun):
                return
            battery._work(gun, 1.0, mag, second)
            service = battery.services[gun.id]
            if at_phase and not service.idle and battery._phases(gun)[service.phase][0] == at_phase:
                battery._shut = battery._shut | {gun.id}
                battery._housed(gun)
                at_phase = None

    gun = ship.guns["gun.1.starboard"]
    battery._shut = frozenset({gun.id})
    served(gun, 300)
    assert gun.loaded and gun.primed and not gun.run_out and battery.services[gun.id].idle
    assert battery.drill_of(gun.id).cycles == 0 and battery.drill_of(gun.id).best_s is None
    # begun with the port open and shut on it at the priming, past the running out: nor this
    other = ship.guns["gun.2.starboard"]
    served(other, 300, at_phase="prime")
    assert other.id in battery._shut and other.loaded and other.primed and not other.run_out
    assert battery.services[other.id].idle
    assert battery.drill_of(other.id).cycles == 0 and battery.drill_of(other.id).best_s is None
    # opened, the gun's run out and it wants no timing either: its round was not from the sponge
    battery._shut = frozenset()
    served(other, 60)
    assert other.run_out and battery.drill_of(other.id).cycles == 0
    # a whole round from the sponge with the port open goes on the drill as it always did
    third = ship.guns["gun.3.starboard"]
    served(third, 300)
    assert third.run_out and third.primed
    assert battery.drill_of(third.id).cycles == 1 and battery.drill_of(third.id).best_s > 0.0


def test_a_gun_named_with_its_port_open_fires_as_it_did():
    ship = load_ship(BRIG)
    battery = Battery(ship)
    gun = next(g for g in ship.guns.values() if g.number == 3 and g.side == "larboard")
    gun.loaded, gun.primed, gun.run_out = Charge.ROUND, True, True
    battery.single = [gun.id]
    battery._fire(None, firer_at(0.0), None, None, 0, None, None)
    assert battery.single == [] and gun.fired == 1


def test_the_dumb_show_stands_idle_behind_a_shut_port_and_goes_on_when_it_opens():
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    gun = ship.guns["gun.1.starboard"]
    battery.begin_exercise("starboard")
    assert battery.wants_work(gun)
    battery._shut = frozenset({gun.id})
    assert not battery.wants_work(gun)
    battery._shut = frozenset()
    assert battery.wants_work(gun)


# -- a lee broadside heeled past her shut heel -------------------------------------------------


def _at_quarters(path: str, fit: str | None = None):
    """Her guns cast loose, loaded, primed and run out on both sides, in smooth water, with
    her heel nothing of her own: 7-135's form from here."""
    w = make_world(
        SEED,
        path,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=6.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=90.0,
            ship_speed_kn=0.0,
            fit=fit,
        ),
    )
    w.run(5)
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    battery = battery_of(w.ship)
    broadside = [g for g in w.ship.guns.values() if g.place == "broadside"]
    for _ in range(1500):  # one crew serves a pair of guns: the two sides' loading in turn
        w.tick()
        if all(battery.ready(g) for g in broadside):
            break
    return w


class _Serving:
    """A battery engaged on one side and firing as they bear, at a mark abeam a cable off,
    served by 7-135's form at a heel the test gives: every other thing of the tick as it is."""

    def __init__(self, world, side: str) -> None:
        self.world = world
        self.side = side
        self.ship = world.ship
        self.battery = battery_of(world.ship)
        self.quarters = quarters_of(world.ship)
        self.rng = world.rng.stream("lee-ports")
        self.clock = world.clock.tick
        self.battery.engaged = side
        self.battery.mode = FireMode.AS_THEY_BEAR
        self.battery.target = "mark"
        self.battery.target_words = "a brig"
        toward = math.pi / 2.0 if side == "starboard" else -math.pi / 2.0
        self.mark = Target(
            id="mark",
            words="a brig",
            bearing_rad=units.wrap_2pi(float(self.ship.heading) + toward),
            range_m=180.0,
            heading_rad=float(self.ship.heading),
            length_m=30.0,
            heel_deg=0.0,
            nation="france",
            body=None,
            world=None,
        )

    def serve(self, heel_abs: float, seconds: int) -> None:
        heel = heel_abs if self.side == "starboard" else -heel_abs
        firer = replace(action._firer(self.world, self.ship), heel_deg=heel)
        for _ in range(seconds):
            self.clock += 1
            self.battery.tick(
                1.0, self.quarters, firer, self.mark, self.rng, self.clock, lambda *a, **k: []
            )

    def lee_guns(self, deck: str | None = None) -> list[Gun]:
        return [
            g
            for g in self.ship.guns.values()
            if g.place == "broadside" and g.side == self.side and (deck is None or g.deck == deck)
        ]

    def fired(self) -> dict[str, int]:
        return {g.id: g.fired for g in self.ship.guns.values()}


def _shut_heels(ship, guns) -> dict[str, float]:
    profile = ship.hull.spec.profile
    return {g.id: shut_heel(g.height_m, half_breadth_at_sill(profile, g.deck, g.x_m)) for g in guns}


def _open_heels(ship, guns) -> dict[str, float]:
    profile = ship.hull.spec.profile
    return {g.id: open_heel(g.height_m, half_breadth_at_sill(profile, g.deck, g.x_m)) for g in guns}


@pytest.mark.parametrize(
    "path,fit,side,deck",
    [
        (CUTTER, "carronades", "starboard", "upper"),
        (CUTTER, "carronades", "larboard", "upper"),
        (CUTTER, "long guns", "starboard", "upper"),
        (PRIVATEER, "long tom", "starboard", "upper"),
        (PRIVATEER, "letter of marque", "larboard", "upper"),
        (BRIG, None, "starboard", "upper"),
        (FRIGATE, None, "starboard", "upper"),
    ],
)
def test_a_lee_broadside_past_the_shut_heel_is_run_in_and_silent(path, fit, side, deck):
    """§14.1. Half a degree under her lowest lee port's heel every lee gun fires. Past the
    highest of the deck none of it does: each is run in, each is served to loaded and primed
    behind its port (the loading goes on), and a loaded gun stays loaded; what fires over the
    rail or from a higher deck goes on firing. Back under the heel that opens the last port,
    held a tick short of the minute after the sea last stood at their sills, then at the minute
    they run out and fire again, unbidden (the hold, the lead's ruling of 2026-11-06; before
    it, at the first tick under)."""
    w = _at_quarters(path, fit)
    serving = _Serving(w, side)
    ship, battery = serving.ship, serving.battery
    lee = serving.lee_guns(deck)
    assert lee and all(battery.ready(g) for g in lee), "her guns made ready"
    shuts = _shut_heels(ship, lee)
    opens = _open_heels(ship, lee)

    # under: nothing shut, and the lee guns fire
    serving.serve(min(shuts.values()) - 0.5, 150)
    assert battery._shut == frozenset()
    fired = serving.fired()
    assert all(fired[g.id] >= 1 for g in lee), {g.id: fired[g.id] for g in lee}

    # past: run in and silent, the loading done behind the port
    serving.serve(max(shuts.values()) + 0.5, 1)
    assert {g.id for g in lee} <= battery._shut
    assert not any(g.run_out for g in lee)
    fired = serving.fired()
    serving.serve(max(shuts.values()) + 0.5, 240)
    after = serving.fired()
    assert all(after[g.id] == fired[g.id] for g in lee), "a shut gun fired"
    assert not any(g.run_out for g in lee)
    assert all(g.loaded and g.primed for g in lee), "the loading goes on behind the port"
    words = guns_reading(w, None)
    assert "ports shut" in words["words"] and set(words["ports_shut"]) == battery._shut

    # a gun with no port is not stopped: the privateer's pivot and her swivels over the rail,
    # and of the frigate's guns those of the decks above, whose sills stand clear yet
    if ship.fit == "long tom":
        over_the_rail = [g for g in ship.guns.values() if g.place in ("pivot", "rail")]
        fired_over = [g for g in over_the_rail if after[g.id] > fired[g.id]]
        assert any(g.place == "pivot" for g in fired_over) and all(
            g.id not in battery._shut for g in over_the_rail
        )
    if path == FRIGATE:
        above = [g for g in serving.lee_guns() if g.deck != deck]
        assert above and all(g.id not in battery._shut for g in above)
        assert any(after[g.id] > fired[g.id] for g in above), "the quarterdeck stands clear"

    # back: held a minute after the sea left the sills, then open, run out and firing again
    serving.serve(min(opens.values()) - 0.5, HOLD - 1)
    assert {g.id for g in lee} <= battery._shut
    serving.serve(min(opens.values()) - 0.5, 1)
    assert not (battery._shut & {g.id for g in lee})
    serving.serve(min(opens.values()) - 0.5, 150)
    again = serving.fired()
    assert all(again[g.id] > after[g.id] for g in lee), "the ports open and the guns silent"
    assert "ports shut" not in guns_reading(w, None)["words"]


@pytest.mark.parametrize("side", ["starboard", "larboard"])
def test_the_reading_says_the_side_it_counts(side):
    w = _at_quarters(CUTTER)
    serving = _Serving(w, side)
    serving.serve(20.0, 2)
    assert f"ports shut (three to {side})" in guns_reading(w, None)["words"]


def test_only_the_ports_under_are_shut_and_the_rest_of_the_broadside_fires():
    """The cutter between: at 16 degrees her two lower ports are under (x -3.5 at 15.0, x -0.5
    at 14.7) and her third, higher by the sheer forward (x +2.5 at 17.3), is not, and it fires
    alone."""
    w = _at_quarters(CUTTER)
    serving = _Serving(w, "starboard")
    ship, battery = serving.ship, serving.battery
    guns = sorted(serving.lee_guns(), key=lambda g: g.x_m)
    assert [g.x_m for g in guns] == [-3.5, -0.5, 2.5]
    serving.serve(16.0, 200)
    aft, mid, fore = guns
    assert battery._shut == {aft.id, mid.id}
    assert aft.fired == 0 and mid.fired == 0 and fore.fired >= 1
    assert not aft.run_out and not mid.run_out
    assert "ports shut (two to starboard)" in guns_reading(w, None)["words"]
    assert ship.guns[fore.id].id not in battery._shut


@pytest.mark.parametrize(
    "path,fit,heel,mark_m",
    [
        (CUTTER, "carronades", 16.0, 180.0),  # x -3.5 and -0.5 shut, the after division; +2.5 open
        (CUTTER, "long guns", 16.0, 370.0),
        (PRIVATEER, "long tom", 16.0, 370.0),  # x -7.5 shut, +10.5 and the pivot open
        (BRIG, None, 23.5, 180.0),
        (MERCHANT_BRIG, None, 18.25, 180.0),  # x +4.0 shut, the forward division; -4.0 open
    ],
)
def test_by_divisions_a_division_all_behind_shut_ports_holds_no_turn(path, fit, heel, mark_m):
    """A shut port silences its own gun and no other (§7.2): the turn passes a division with
    no gun open, and the other's guns fire by turns with no gun lost, as they do as they bear.
    Both ways round, for the merchant brig's forward gun shuts first and the cutter's after."""
    rounds = {}
    for mode in (FireMode.BY_DIVISIONS, FireMode.AS_THEY_BEAR):
        w = _at_quarters(path, fit)
        serving = _Serving(w, "starboard")
        serving.mark = replace(serving.mark, range_m=mark_m)
        battery = serving.battery
        battery.mode = mode
        serving.serve(heel, 900)
        assert battery._shut and all(
            g.fired == 0 for g in serving.lee_guns() if g.id in battery._shut
        )
        rounds[mode] = [g.fired for g in serving.lee_guns() if g.id not in battery._shut]
    assert all(n >= 5 for n in rounds[FireMode.BY_DIVISIONS]), rounds
    assert rounds[FireMode.BY_DIVISIONS] == rounds[FireMode.AS_THEY_BEAR], rounds


def test_by_divisions_a_division_with_a_gun_open_keeps_its_turn_while_that_gun_loads():
    """Only a division all shut is passed. At 14.85 degrees the cutter's midship port is shut
    (14.7) and her after one is not (15.0): the turn is the after division's, its open gun is
    loading, and the forward gun, ready, waits, as with no port shut at all."""
    w = _at_quarters(CUTTER)
    serving = _Serving(w, "starboard")
    battery = serving.battery
    battery.mode = FireMode.BY_DIVISIONS
    aft, mid, fore = sorted(serving.lee_guns(), key=lambda g: g.x_m)
    firer = replace(action._firer(w, w.ship), heel_deg=14.85)
    ports.update(battery, firer, 0)
    assert battery._shut == {mid.id}
    aft.loaded, aft.primed, aft.run_out = None, False, False
    battery.division_turn = "after"
    battery._fire(serving.quarters, firer, serving.mark, serving.rng, 1, lambda *a, **k: [], None)
    assert battery.division_turn == "after" and fore.fired == 0
    # and with no port shut the turn waits on the division's own loading, as it always has
    battery._shut = frozenset()
    mid.loaded, mid.primed, mid.run_out = None, False, False
    battery._fire(serving.quarters, firer, serving.mark, serving.rng, 2, lambda *a, **k: [], None)
    assert battery.division_turn == "after" and fore.fired == 0


def test_silent_by_their_ports_alone_counts_only_the_guns_that_would_fire():
    """What passes a division's turn and drops a word: some of the guns would fire at the mark
    when ready, and all those are shut. A gun open that could not fire anyway is no reason to
    wait on it: dismounted, not bearing, of a side not engaged, or short of the mark."""
    w = _at_quarters(CUTTER, "long guns")
    serving = _Serving(w, "starboard")
    battery, ship, mark = serving.battery, serving.ship, serving.mark
    relative = units.wrap_pi(mark.bearing_rad - float(ship.heading))
    lee = serving.lee_guns()
    ids = frozenset(g.id for g in lee)
    swivels = [g for g in ship.guns.values() if g.place == "rail" and g.side == "starboard"]
    assert swivels and all(battery.bears(g, relative) for g in lee + swivels)
    assert not battery._behind_ports(lee, relative, mark)  # none shut
    battery._shut = ids
    assert battery._behind_ports(lee, relative, mark)
    # one open: not silent by its ports
    battery._shut = ids - {lee[0].id}
    assert not battery._behind_ports(lee, relative, mark)
    # that one dismounted: silent by the ports of the rest
    lee[0].dismounted = True
    assert battery._behind_ports(lee, relative, mark)
    lee[0].dismounted = False
    # that one not bearing: the mark ahead of her, abeam no more, none of them would fire
    battery._shut = ids
    assert not battery._behind_ports(lee, 0.0, mark)
    # of a side not engaged: none of them would fire
    battery.engaged = "larboard"
    assert not battery._behind_ports(lee, relative, mark)
    battery.engaged = "starboard"
    # a swivel open over the rail at her lee: a gun of the word that can fire, within its reach
    assert not battery._behind_ports(lee + swivels, relative, mark)
    # and beyond its reach, not (a swivel's random shot is 366 m, her 3-pounders' 1,097 m)
    far = replace(mark, range_m=500.0)
    assert battery._behind_ports(lee + swivels, relative, far)
    assert not battery._behind_ports(lee, relative, replace(mark, range_m=2000.0))


def test_a_word_stands_with_no_gun_of_it_bearing_though_other_ports_are_shut():
    """Ports shut on the other side do not touch a word whose guns do not bear yet, whether
    that other side is engaged or not (the shut guns' side bears and fires for the mark to
    starboard, and they are no guns of the word for the larboard broadside)."""
    for engaged in ("larboard", "both"):
        w = _at_quarters(CUTTER)
        serving = _Serving(w, "starboard")
        battery, ship = serving.battery, serving.ship
        battery.mode = FireMode.HOLD
        battery.engaged = engaged
        serving.serve(20.0, 2)
        assert battery._shut, "the starboard side's ports"
        ship.drain_notes()
        battery.word = "larboard"
        serving.serve(20.0, 1)  # the mark to starboard: no larboard gun bears
        assert battery.word == "larboard" and not lines_of(ship, "guns.port_shut"), engaged


def test_the_word_for_a_broadside_all_behind_shut_ports_is_dropped_with_its_line():
    """As a gun named is (§7.2): the word does not stand for as long as she heels, to be
    answered unbidden by the first gun to run out when she comes upright. Nothing goes, then
    or after, and the guns keep their charges for the word given again."""
    w = _at_quarters(CUTTER)
    serving = _Serving(w, "starboard")
    battery, ship = serving.battery, serving.ship
    battery.mode = FireMode.HOLD
    lee = serving.lee_guns()
    serving.serve(20.0, 60)
    assert {g.id for g in lee} <= battery._shut
    ship.drain_notes()
    battery.word = "starboard"
    serving.serve(20.0, 1)
    assert battery.word is None and all(g.fired == 0 for g in lee)
    (line,) = lines_of(ship, "guns.port_shut")
    assert line[0] == "notable"
    assert line[2] == "The starboard broadside's ports are shut; the sea is at their sills."
    serving.serve(20.0, 60)
    assert not lines_of(ship, "guns.port_shut")
    serving.serve(5.0, 240)
    assert battery.word is None and all(g.fired == 0 for g in lee), "unbidden"
    assert all(battery.ready(g) for g in lee)
    battery.word = "starboard"
    serving.serve(5.0, 1)
    assert battery.word is None and [g.fired for g in lee] == [1, 1, 1]


def test_the_word_stands_on_any_gun_of_it_open_and_that_gun_answers_it():
    """At 16 degrees the cutter's forward gun stands open behind no lid: the word is not
    dropped, and it goes as it goes, by the guns ready. With that gun empty the word stands
    until it is ready, as with no port shut at all. The privateer's pivot fires over the rail
    and has no port, so her word stands with both her carronades shut."""
    w = _at_quarters(CUTTER)
    serving = _Serving(w, "starboard")
    battery, ship = serving.battery, serving.ship
    battery.mode = FireMode.HOLD
    aft, mid, fore = sorted(serving.lee_guns(), key=lambda g: g.x_m)
    serving.serve(16.0, 30)
    assert battery._shut == {aft.id, mid.id}
    ship.drain_notes()
    fore.loaded, fore.primed, fore.run_out = None, False, False
    battery.word = "starboard"
    serving.serve(16.0, 1)
    assert battery.word == "starboard" and not lines_of(ship, "guns.port_shut")
    for _ in range(600):
        serving.serve(16.0, 1)
        if battery.word is None:
            break
    assert battery.word is None and fore.fired == 1 and aft.fired == 0 and mid.fired == 0
    assert not lines_of(ship, "guns.port_shut")

    w = _at_quarters(PRIVATEER, "long tom")
    serving = _Serving(w, "starboard")
    battery, ship = serving.battery, serving.ship
    battery.mode = FireMode.HOLD
    serving.serve(35.0, 120)  # past 29.7, her higher carronade's; the pivot trained round
    assert {g.id for g in serving.lee_guns()} <= battery._shut
    ship.drain_notes()
    over_the_rail = [g for g in ship.guns.values() if g.place in ("pivot", "rail")]
    before = sum(g.fired for g in over_the_rail)
    battery.word = "starboard"
    serving.serve(35.0, 1)
    assert battery.word is None and not lines_of(ship, "guns.port_shut")
    assert sum(g.fired for g in over_the_rail) > before
    assert all(g.fired == 0 for g in serving.lee_guns())


def test_a_word_for_a_broadside_given_by_the_order_is_told_at_the_next_tick(heeled):
    """The orders' own road, every lee port shut: the order takes the word, and the deck's line
    follows on the next tick, the word gone and no gun fired when she comes upright. The
    order's own reply still says the word stands (`orders/gunnery.py`, outside this rule;
    named to the lead in the tuning notes)."""
    w = _at_quarters(CUTTER)
    battery = battery_of(w.ship)
    w.submit("engage a mark one cable off the larboard beam")
    w.submit("hold your fire")
    w.run(3)
    heeled["deg"] = -18.0
    w.run(3)
    lee = [g for g in w.ship.guns.values() if g.place == "broadside" and g.side == "larboard"]
    assert {g.id for g in lee} <= battery._shut
    w.submit("fire")
    w.run(2)
    assert battery.word is None
    said = [e.text for e in w.log if e.kind == "guns.port_shut"]
    assert said == ["The larboard broadside's ports are shut; the sea is at their sills."]
    heeled["deg"] = -1.0
    w.run(240)
    assert all(g.fired == 0 for g in lee) and all(battery.ready(g) for g in lee)


# -- the log, once a change of state a deck and side -------------------------------------------


@pytest.fixture
def heeled(monkeypatch):
    """Her heel as the battery reads it, by the test's hand, through the World's own tick:
    every other thing of the tick as it is."""
    real = action._firer
    heel = {"deg": 0.0}
    monkeypatch.setattr(
        action,
        "_firer",
        lambda world, ship: replace(real(world, ship), heel_deg=heel["deg"]),
    )
    return heel


def _quiet(path: str, fit: str | None = None):
    return make_world(
        SEED,
        path,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=6.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=90.0,
            ship_speed_kn=0.0,
            fit=fit,
        ),
    )


def _port_lines(w) -> list:
    return [e for e in w.log if e.kind in ("guns.ports_shut", "guns.ports_opened")]


def test_the_log_says_each_deck_and_side_once_a_change_of_state(heeled):
    """The frigate's three decks by their words: the upper deck's line at the first of its
    ports, none as the rest go under, the quarterdeck's and the forecastle's when theirs do,
    and each opened once, when the last of it has opened, a minute after the sea left it (the
    hold). A line is not said twice."""
    w = _quiet(FRIGATE)
    cast_loose(w.ship)
    w.run(5)
    assert not _port_lines(w)
    heeled["deg"] = 20.0  # the lowest of the upper deck under, at 19.7
    w.run(3)
    b = battery_of(w.ship)
    assert 0 < len(b._shut) < 13
    assert [(e.kind, e.text) for e in _port_lines(w)] == [
        ("guns.ports_shut", "The lee upper-deck ports are shut, the sea at their sills.")
    ]
    heeled["deg"] = 30.0  # all thirteen under, no second line
    w.run(3)
    assert len(b._shut) == 13 and len(_port_lines(w)) == 1
    heeled["deg"] = 50.0  # the quarterdeck's first and the forecastle's first go under
    w.run(3)
    assert [e.text for e in _port_lines(w)[1:]] == [
        "The lee forecastle ports are shut, the sea at their sills.",
        "The lee quarterdeck ports are shut, the sea at their sills.",
    ]
    heeled["deg"] = 25.0  # the two upper decks open; part of the upper deck stays shut
    w.run(HOLD + 3)
    assert [e.text for e in _port_lines(w)[3:]] == [
        "The lee forecastle ports are opened again, their sills clear of the sea.",
        "The lee quarterdeck ports are opened again, their sills clear of the sea.",
    ]
    assert b._shut and all(w.ship.guns[g].deck == "upper" for g in b._shut)
    heeled["deg"] = 5.0  # the last of the upper deck's opens
    w.run(HOLD + 3)
    assert [(e.kind, e.text) for e in _port_lines(w)[5:]] == [
        (
            "guns.ports_opened",
            "The lee upper-deck ports are opened again, their sills clear of the sea.",
        )
    ]
    assert b._shut == frozenset()
    heeled["deg"] = 2.0
    w.run(3)
    assert len(_port_lines(w)) == 6
    first = _port_lines(w)[0]
    assert first.data["deck"] == "upper" and first.data["side"] == "starboard"
    assert first.data["lee"] is True and first.data["heel_deg"] == 20.0


def test_the_lower_deck_is_said_in_the_designs_own_words(heeled):
    """§7.2's sentence, on the one ship with a lower deck."""
    w = _quiet(SIXTY_FOUR)
    cast_loose(w.ship)
    w.run(2)
    heeled["deg"] = 11.0
    w.run(3)
    assert [e.text for e in _port_lines(w)] == [
        "The lee lower-deck ports are shut, the sea at their sills."
    ]


def test_each_side_is_a_state_of_its_own(heeled):
    """She goes about at a heel past both sides' shut heels: the new lee side's line shut at
    once, and the old lee side's opened a minute after the sea left its sills, each with its
    side (the hold, the lead's ruling of 2026-11-06; before it, both on the same tick)."""
    w = _quiet(CUTTER)
    cast_loose(w.ship)
    w.run(2)
    heeled["deg"] = 20.0
    w.run(2)
    heeled["deg"] = -20.0
    w.run(2)
    assert [(e.kind, e.data["side"]) for e in _port_lines(w)] == [
        ("guns.ports_shut", "starboard"),
        ("guns.ports_shut", "larboard"),
    ]
    w.run(HOLD)
    assert [(e.kind, e.data["side"]) for e in _port_lines(w)] == [
        ("guns.ports_shut", "starboard"),
        ("guns.ports_shut", "larboard"),
        ("guns.ports_opened", "starboard"),
    ]


def test_the_line_is_the_guns_and_no_passage_hears_it(heeled):
    """With her guns secured the state is kept and the reading says it, and the log says
    nothing, shutting or opening: the captain's trials' passages are as they were. Cast loose
    with the port shut already, the line is said then, once; the opening is said in its turn.
    Secured again with the port still shut, the side is forgotten, and nothing is said when
    it opens."""
    w = _quiet(CUTTER)
    w.run(2)
    b = battery_of(w.ship)
    heeled["deg"] = 20.0
    w.run(2)
    assert len(b._shut) == 3 and "ports shut" in guns_reading(w, None)["words"]
    assert not _port_lines(w)
    heeled["deg"] = 2.0
    w.run(HOLD + 2)
    assert b._shut == frozenset() and not _port_lines(w)

    heeled["deg"] = 20.0
    w.run(2)
    cast_loose(w.ship)
    w.run(2)
    assert [(e.kind, e.severity) for e in _port_lines(w)] == [("guns.ports_shut", Severity.NOTABLE)]
    w.run(5)
    assert len(_port_lines(w)) == 1
    heeled["deg"] = 2.0
    w.run(HOLD + 2)
    assert [(e.kind, e.severity) for e in _port_lines(w)[1:]] == [
        ("guns.ports_opened", Severity.NOTABLE)
    ]

    heeled["deg"] = 20.0
    w.run(2)
    assert len(_port_lines(w)) == 3
    for gun in w.ship.guns.values():
        gun.cast_loose = False
    w.run(2)
    heeled["deg"] = 2.0
    w.run(HOLD + 2)
    assert b._shut == frozenset() and len(_port_lines(w)) == 3 and b._ports_told == frozenset()


def test_the_reading_says_ports_shut_while_any_are_and_only_then(heeled):
    w = _quiet(CUTTER)
    w.run(2)
    before = guns_reading(w, None)
    assert "ports shut" not in before["words"] and "ports_shut" not in before
    heeled["deg"] = 20.0
    w.run(2)
    reading = guns_reading(w, None)
    assert "ports shut (three to starboard)" in reading["words"]
    assert reading["ports_shut"] == sorted(battery_of(w.ship)._shut)
    assert w.readings.value("guns")["ports_shut"] == reading["ports_shut"]
    heeled["deg"] = 2.0
    w.run(HOLD + 2)
    assert guns_reading(w, None) == before


# -- no flicker in a gust ----------------------------------------------------------------------


def test_a_port_does_not_flicker_in_a_gust():
    """A gusty heel swinging over the shut heel and back above the reopening heel for an hour:
    shut once, at the first gust over, and never opened, and one line. Under the reopening
    heel it opens once, a minute after the last gust that brought the sea to its sill (the
    hold, the lead's ruling of 2026-11-06), and one line."""
    ship = load_ship(CUTTER)
    cast_loose(ship)
    profile = ship.hull.spec.profile
    battery = Battery(ship)
    gun = _at_x(ship, -0.5)  # the lowest of her guns
    half = half_breadth_at_sill(profile, gun.deck, gun.x_m)
    shut, reopen = shut_heel(gun.height_m, half), open_heel(gun.height_m, half)
    assert shut - reopen == pytest.approx(3.05, abs=0.1)  # the band a gust swings in
    changes = []
    for second in range(3600):
        # a ten seconds' swing, over the shut heel at each crest and down to the reopening
        # heel and no further at each trough
        swing = (shut - reopen) * 0.55 * math.sin(second * 0.628)
        heel = max(reopen + 0.01, (shut + reopen) / 2.0 + swing)
        changes.append(ports.update(battery, firer_at(heel), second))
    assert sum(gun.id in s for s, _ in changes) == 1
    assert sum(gun.id in o for _, o in changes) == 0
    assert gun.id in battery._shut
    last_sea = battery._sea_at_sill[gun.id]
    assert 3590 <= last_sea < 3600  # the last crest over the shut heel
    for second in range(3600, last_sea + HOLD):
        ports.update(battery, firer_at(reopen - 0.5), second)
    assert gun.id in battery._shut  # held a tick short of the minute
    ports.update(battery, firer_at(reopen - 0.5), last_sea + HOLD)
    assert gun.id not in battery._shut
    notes = lines_of(ship, "guns.ports_shut", "guns.ports_opened")
    assert [n[1] for n in notes] == ["guns.ports_shut", "guns.ports_opened"]


# -- the hold: a minute before a shut port opens (the lead's ruling of 2026-11-06) -----------------


def _cutters_lowest():
    """The cutter, a battery of her own, her lowest gun, and the heels a hair over the one that
    shuts it and a hair under the one that opens it."""
    ship = load_ship(CUTTER)
    gun = _at_x(ship, -0.5)
    half = half_breadth_at_sill(ship.hull.spec.profile, gun.deck, gun.x_m)
    shut, reopen = shut_heel(gun.height_m, half), open_heel(gun.height_m, half)
    return ship, Battery(ship), gun, firer_at(shut + 0.01), firer_at(reopen - 0.01)


def test_a_port_is_held_a_minute_through_the_gusts():
    """A gusty heel swinging over the shut heel at each crest and under the reopening heel at
    each trough, ten seconds a swing, for an hour: without the hold the port opened at every
    trough and shut at the next crest (the gun run in each time; the frigate's ports so changed
    46 times in an hour of gusts at 21 knots, Build-Ships.md §7.2's note since L3). With it, the
    port is shut once, at the first crest, and held while the gusts go on, and opens a minute
    after the last crest that brought the sea to its sill; one line each way."""
    ship = load_ship(CUTTER)
    cast_loose(ship)
    battery = Battery(ship)
    gun = _at_x(ship, -0.5)
    half = half_breadth_at_sill(ship.hull.spec.profile, gun.deck, gun.x_m)
    shut, reopen = shut_heel(gun.height_m, half), open_heel(gun.height_m, half)
    changes, clear = [], 0
    for second in range(3600):
        heel = (shut + reopen) / 2.0 + (shut - reopen) * 0.8 * math.sin(second * 0.628)
        clear += heel < reopen
        changes.append(ports.update(battery, firer_at(heel), second))
    assert clear > 900  # the sill stood clear of the reopening line at every trough
    assert sum(gun.id in s for s, _ in changes) == 1 and changes[0] == (frozenset(), frozenset())
    assert sum(gun.id in o for _, o in changes) == 0
    last_sea = battery._sea_at_sill[gun.id]
    assert 3590 <= last_sea < 3600
    for second in range(3600, last_sea + HOLD):
        ports.update(battery, firer_at(reopen - 0.5), second)
    assert gun.id in battery._shut
    ports.update(battery, firer_at(reopen - 0.5), last_sea + HOLD)
    assert gun.id not in battery._shut and battery._sea_at_sill == {}
    notes = lines_of(ship, "guns.ports_shut", "guns.ports_opened")
    assert [n[1] for n in notes] == ["guns.ports_shut", "guns.ports_opened"]


def test_the_sea_at_the_sill_again_starts_the_hold_afresh():
    """The hold counts from the last tick the sea was at the sill: a sea again within the minute
    starts it afresh, and a port opened and shut again by a later sea has a new minute. The
    shutting itself is at once, every time."""
    ship, battery, gun, over, clear = _cutters_lowest()
    assert ports.update(battery, over, 0) == (frozenset({gun.id}), frozenset())
    ports.update(battery, clear, 1)
    ports.update(battery, over, 30)  # a sea again within the minute
    assert battery._sea_at_sill == {gun.id: 30}
    ports.update(battery, clear, 31)
    ports.update(battery, clear, HOLD)  # a minute from the first sea: held still
    ports.update(battery, clear, 30 + HOLD - 1)
    assert gun.id in battery._shut
    assert ports.update(battery, clear, 30 + HOLD) == (frozenset(), frozenset({gun.id}))
    # opened, and the next sea shuts it at once, for a new minute
    assert ports.update(battery, over, 31 + HOLD) == (frozenset({gun.id}), frozenset())
    ports.update(battery, clear, 30 + 2 * HOLD)
    assert gun.id in battery._shut
    assert ports.update(battery, clear, 31 + 2 * HOLD) == (frozenset(), frozenset({gun.id}))


def test_a_port_shut_in_a_save_before_the_hold_is_held_from_its_first_reading():
    """A battery saved with a port shut before the hold has no tick for it (the class default,
    None): its minute counts from the first tick the rule reads it, and it opens then."""
    ship, battery, gun, _, clear = _cutters_lowest()
    battery._shut = frozenset({gun.id})  # as a save made at L3 left it
    assert "_sea_at_sill" not in battery.__dict__ and battery._sea_at_sill is None
    assert ports.update(battery, clear, 500) == (frozenset(), frozenset())
    assert battery._sea_at_sill == {gun.id: 500}
    ports.update(battery, clear, 500 + HOLD - 1)
    assert gun.id in battery._shut
    assert ports.update(battery, clear, 500 + HOLD) == (frozenset(), frozenset({gun.id}))


def test_a_checkpoint_taken_in_the_hold_keeps_it(heeled, tmp_path):
    """A save made while her ports are held keeps the tick the sea was last at each sill: read
    back, they open on the same tick as in the World that ran on, a minute after it."""
    w = _quiet(CUTTER)
    cast_loose(w.ship)
    w.run(2)
    heeled["deg"] = 20.0
    w.run(2)
    heeled["deg"] = 2.0
    w.run(20)
    held = dict(battery_of(w.ship)._sea_at_sill)
    assert len(held) == 3 and len(set(held.values())) == 1 and battery_of(w.ship)._shut
    path = replay.write_checkpoint(w, tmp_path / "held.checkpoint")
    _, loaded = replay.read_checkpoint(path)
    assert battery_of(loaded.ship)._sea_at_sill == held
    opened_at = []
    for world in (w, loaded):
        battery = battery_of(world.ship)
        for _ in range(2 * HOLD):
            if not battery._shut:
                break
            world.run(1)
        opened_at.append(world.clock.tick)
    assert opened_at[0] == opened_at[1]
    assert max(held.values()) + HOLD <= opened_at[0] <= max(held.values()) + HOLD + 1


def test_she_shuts_her_own_lee_ports_by_the_press_of_her_own_sail():
    """No hand on her heel: the cutter under all her canvas in twenty-five knots, the wind on
    her starboard side. She heels to larboard past the heel of her lower ports, and the log
    and the state say so, and her weather ports stand open."""
    w = make_world(
        SEED,
        CUTTER,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=25.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=285.0,
            ship_speed_kn=4.0,
        ),
    )
    cast_loose(w.ship)
    w.submit("make all sail")
    w.submit("brace sharp up on the starboard tack")
    b = battery_of(w.ship)
    for i in range(1500):
        if i % 120 == 0:
            w.submit("trim sails")
        w.tick()
        if b._shut:
            break
    heel = math.degrees(float(w.ship.dyn.heel))
    assert heel < -14.0, f"{heel:.1f} degrees"
    w.run(2)
    assert b._shut and all(w.ship.guns[g].side == "larboard" for g in b._shut)
    (line,) = _port_lines(w)
    assert line.text == "The lee upper-deck ports are shut, the sea at their sills."
    assert line.data["side"] == "larboard" and line.data["lee"] is True


# -- the half-breadth, and a gun with no deck or no profile ------------------------------------


def test_the_half_breadth_is_read_once_a_gun(monkeypatch):
    """§7.1: held once a gun, the sine and the compare all a tick costs after."""
    calls = []
    real = ports.half_breadth_at_sill

    def counted(profile, deck, x):
        calls.append((deck, x))
        return real(profile, deck, x)

    monkeypatch.setattr(ports, "half_breadth_at_sill", counted)
    ship = load_ship(FRIGATE)
    battery = Battery(ship)
    for i, heel in enumerate((0.0, 5.0, 25.0, 50.0, 25.0, 0.0, -25.0)):
        ports.update(battery, firer_at(heel), i * HOLD)
    port_guns = [g for g in ship.guns.values() if g.place in ports.PORT_PLACES]
    assert len(calls) == len(port_guns) == len(battery._port_breadths)


def test_a_boat_with_a_gun_falls_back_to_half_the_beam():
    """A gun with no deck, in a boat: the gun's own height and half the beam the firer gives
    (`action._firer`: the beam over two). Her file's beam is 2.4 m. Package 82 drew each boat from
    a profile of her own, so the fallback here is the gun's want of a deck, not the hull's."""
    spec = load_spec(LAUNCH)
    assert spec.hull.profile is not None and spec.hull.beam_m == 2.4
    half = spec.hull.beam_m / 2.0
    sill = 0.60
    battery = the_battery_of_one(LAUNCH, a_gun(1.0, sill, deck=None, place="bow"))
    gid = "gun.1.starboard"
    shut, reopen = shut_heel(sill, half), open_heel(sill, half)
    ports.update(battery, firer_at(shut - 0.01, half), 0)
    assert battery._shut == frozenset()
    ports.update(battery, firer_at(shut + 0.01, half), 1)
    assert battery._shut == {gid}
    ports.update(battery, firer_at(reopen + 0.01, half), 1 + HOLD)
    assert battery._shut == {gid}
    ports.update(battery, firer_at(reopen - 0.01, half), 1 + HOLD)
    assert battery._shut == frozenset()
    assert battery._port_breadths == {gid: None}


def test_the_lines_say_no_deck_for_a_gun_with_none():
    battery = the_battery_of_one(LAUNCH, a_gun(1.0, 0.60, deck=None, place="bow"))
    cast_loose(battery.ship)
    ports.update(battery, firer_at(30.0, 1.2), 0)
    ports.update(battery, firer_at(0.0, 1.2), HOLD)
    notes = lines_of(battery.ship, "guns.ports_shut", "guns.ports_opened")
    assert [n[2] for n in notes] == [
        "The lee ports are shut, the sea at their sills.",
        "The lee ports are opened again, their sills clear of the sea.",
    ]
    assert notes[0][4]["deck"] is None


def test_a_chaser_of_no_side_is_said_on_the_centre_line_and_neither_lee_nor_weather():
    """A bow or stern gun may have no side (`Gun.name`: 'the stern chaser'). No file carries
    one today and the heel alone shuts none but a sill within a foot of the water upright;
    the roll does, by its amplitude alone, for no heel is toward the centre line (§7.1: the
    heel toward the gun's side plus the roll). The reading and the log must not guess a side
    for it. **Since L3's review** a sided port shut upright is said by its side's name, for
    upright she has no lee: old beside new, "The lee upper-deck ports are shut" for the
    larboard gun at no heel, now "The larboard upper-deck ports are shut"."""
    gun = a_gun(-12.0, 0.30, deck="upper", side=None, place="stern", gid="stern")
    assert gun.name == "the stern chaser"
    ship = load_ship(BRIG)
    other = a_gun(0.0, 0.30, deck="upper", side="larboard", gid="other")
    ship.guns = {gun.id: gun, other.id: other}
    cast_loose(ship)
    battery = Battery(ship)
    assert _ports_shut_words(ship, frozenset({gun.id})) == "ports shut (one on the centre line)"
    assert _ports_shut_words(ship, frozenset({gun.id, other.id})) == (
        "ports shut (one on the centre line and one to larboard)"
    )
    for heel in (0.0, 10.0, -10.0):
        one = a_gun(-12.0, 0.30, deck="upper", side=None, place="stern", gid="stern")
        solo = load_ship(BRIG)
        solo.guns = {one.id: one}
        cast_loose(solo)
        alone = Battery(solo)
        ports.update(alone, firer_at(heel), 0)
        one.height_m = 1.0
        ports.update(alone, firer_at(heel), HOLD)
        notes = lines_of(solo, "guns.ports_shut", "guns.ports_opened")
        assert [n[2] for n in notes] == [
            "The upper-deck ports are shut, the sea at their sills.",
            "The upper-deck ports are opened again, their sills clear of the sea.",
        ], heel
        assert notes[0][4]["lee"] is None and notes[0][4]["side"] is None
    # the roll shuts it by its amplitude, heeled or upright, and the heel alone never does
    one = a_gun(-12.0, 1.0, deck="upper", side=None, place="stern", gid="stern")
    solo = load_ship(BRIG)
    solo.guns = {one.id: one}
    cast_loose(solo)
    at = shut_heel(1.0, ports._half_breadth(Battery(solo), one, firer_at(0.0)))
    for heel in (0.0, 5.0, -5.0, 10.0, -10.0, 30.0, -30.0):
        alone = Battery(solo)
        ports.update(alone, firer_at(heel), 0)
        assert one.id not in alone._shut, heel
        ports.update(alone, firer_at(heel, roll_deg=at - 0.01), 1)
        assert one.id not in alone._shut, heel
        ports.update(alone, firer_at(heel, roll_deg=at + 0.01), 2)
        assert one.id in alone._shut, heel
    said = [(n[2], n[4]["lee"]) for n in lines_of(solo, "guns.ports_shut")]
    assert said == [("The upper-deck ports are shut, the sea at their sills.", None)] * 7
    # the side's own gun beside it keeps its side's word: upright, its name
    ports.update(battery, firer_at(0.0), 0)
    said = [(n[2], n[4]["lee"]) for n in lines_of(ship, "guns.ports_shut")]
    assert said == [
        ("The upper-deck ports are shut, the sea at their sills.", None),
        ("The larboard upper-deck ports are shut, the sea at their sills.", None),
    ]


def test_a_deck_with_no_ports_in_the_profile_and_no_profile_at_all_take_half_the_beam():
    """`half_breadth_at_sill` gives None for a deck the profile has no ports on."""
    half = 4.3
    sill = 2.10
    shut = shut_heel(sill, half)
    for deck, hull_profile in (("roundhouse", True), ("upper", False), (None, True)):
        ship = load_ship(BRIG)
        if not hull_profile:
            ship.hull.spec = replace(ship.hull.spec, profile=None)
        ship.guns = {"g": a_gun(0.0, sill, deck=deck, gid="g")}
        battery = Battery(ship)
        ports.update(battery, firer_at(shut - 0.01, half), 0)
        assert battery._shut == frozenset(), (deck, hull_profile)
        ports.update(battery, firer_at(shut + 0.01, half), 1)
        assert battery._shut == {"g"}, (deck, hull_profile)


def test_the_real_firer_gives_the_beam_over_two():
    w = _quiet(BRIG)
    assert action._firer(w, w.ship).half_beam_m == w.ship.hull.spec.beam_m / 2.0


# -- the pivot and the rail fire over the rail ---------------------------------------------------


@pytest.mark.parametrize("heel", [85.0, -85.0])
@pytest.mark.parametrize("path,fit", [(PRIVATEER, "long tom"), (CUTTER, "long guns")])
def test_a_pivot_and_a_rail_gun_never_shut(path, fit, heel):
    """§7.1, Proposal-PivotGun.md §4.4. On her beam ends every broadside port to leeward is
    shut and no pivot or swivel; a pivot has no deck, a swivel no port."""
    ship = load_ship(path, fit=fit)
    battery = Battery(ship)
    over_the_rail = [g for g in ship.guns.values() if g.place in ("pivot", "rail")]
    assert over_the_rail
    ports.update(battery, firer_at(heel), 0)
    lee = "starboard" if heel > 0.0 else "larboard"
    assert battery._shut == {
        g.id for g in ship.guns.values() if g.place == "broadside" and g.side == lee
    }
    assert not (battery._shut & {g.id for g in over_the_rail})


# -- the roll (L3) ------------------------------------------------------------------------------


def test_the_roll_is_read_and_shuts_both_sides_by_itself():
    """L3 (§7.3): `ports.roll_in_the_dip` reads `firer.roll_deg`. **Old beside new**, L2's
    `test_the_roll_is_held_at_nought`, which L3's one line moves: there the roll read 0.0, a
    roll of 40 degrees upright shut nothing, and her lowest gun stood open a hair short of its
    own heel under that roll. Now the roll reads 40.0; upright it shuts every broadside port of
    both sides; a hair short of the lowest gun's heel it shuts that gun; and a weather port
    shuts once the roll passes the heel by that port's own heel, and not a hair before (§7.1:
    the weather side's dip is the roll less the heel). Upright she has no lee, so with her guns
    cast loose each side's line is said by its name (since L3's review; before it, both lines
    said "lee")."""
    ship = load_ship(CUTTER)
    battery = Battery(ship)
    assert ports.roll_in_the_dip(firer_at(0.0, roll_deg=40.0)) == 40.0
    broadside = frozenset(g.id for g in ship.guns.values() if g.place == "broadside")
    assert ports.update(battery, firer_at(0.0, roll_deg=40.0), 0) == (broadside, frozenset())
    assert {ship.guns[g].side for g in battery._shut} == {"starboard", "larboard"}
    gun = _at_x(ship, -0.5)
    half = half_breadth_at_sill(ship.hull.spec.profile, gun.deck, gun.x_m)
    heel = shut_heel(gun.height_m, half)
    battery = Battery(ship)
    ports.update(battery, firer_at(heel - 0.01, roll_deg=40.0), 0)
    assert gun.id in battery._shut
    weather = _at_x(ship, -0.5, "larboard")
    battery = Battery(ship)
    ports.update(battery, firer_at(5.0, roll_deg=5.0 + heel - 0.01), 0)
    assert gun.id in battery._shut and weather.id not in battery._shut
    ports.update(battery, firer_at(5.0, roll_deg=5.0 + heel + 0.01), 1)
    assert weather.id in battery._shut
    cast_loose(ship)
    lines_of(ship)
    ports.update(Battery(ship), firer_at(0.0, roll_deg=40.0), 0)
    said = [(n[2], n[4]["side"], n[4]["lee"]) for n in lines_of(ship, "guns.ports_shut")]
    assert said == [
        ("The larboard upper-deck ports are shut, the sea at their sills.", "larboard", None),
        ("The starboard upper-deck ports are shut, the sea at their sills.", "starboard", None),
    ]


def test_she_rolls_her_own_ports_under_in_a_seaway_lee_first_then_weather():
    """No hand on her heel or her roll: the cutter in a World that keeps a sea, 17.5 knots of
    wind and its sea on her starboard beam, plain sail set, her guns cast loose. Her roll builds
    over her first minutes (the motion's 90 s) while she is still all but upright, and by the
    World's own tick her lee ports shut when the heel and the roll first reach her lowest gun's
    heel, 14.74 degrees, and her weather ports when the roll less the heel does, each said once
    in its own words. At L2 (the roll held at nought) neither came: she settles at about 7.9
    degrees of heel, short of her ports by the heel alone (measured on the owner's machine,
    2026-11-05: the lee at tick 74, heel 1.81 and roll 12.97, the log's line at 75; the weather
    at 116, 1.96 and 16.72, its line at 117; settled, heel 7.87 and roll 23.35)."""
    w = make_world(
        SEED,
        CUTTER,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=17.5,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=270.0,
            ship_speed_kn=4.0,
            sea=True,
        ),
    )
    cast_loose(w.ship)
    w.submit("set plain sail")
    battery = battery_of(w.ship)
    lowest = ports._least_dip(battery, action._firer(w, w.ship))
    assert lowest == pytest.approx(14.74, abs=0.01)
    first: dict[str, tuple[int, float, float]] = {}
    for i in range(1800):
        if i % 120 == 0:
            w.submit("trim sails")
        w.tick()
        heel = abs(math.degrees(float(w.ship.dyn.heel)))
        for gid in battery._shut:
            first.setdefault(w.ship.guns[gid].side, (w.clock.tick, heel, w.motion.roll_deg))
    lee, weather = first["larboard"], first["starboard"]
    assert lee[0] < weather[0] < 300
    assert lee[1] < 2.5 and weather[1] < 2.5
    assert lowest <= lee[1] + lee[2] < lowest + 0.2
    assert lowest <= weather[2] - weather[1] < lowest + 0.2
    heel = abs(math.degrees(float(w.ship.dyn.heel)))
    assert 7.5 < heel < lowest - 6.0 and w.motion.roll_deg > 22.0
    assert {w.ship.guns[g].side for g in battery._shut} == {"larboard", "starboard"}
    assert [(e.text, e.data["side"], e.data["lee"]) for e in _port_lines(w)] == [
        ("The lee upper-deck ports are shut, the sea at their sills.", "larboard", True),
        ("The weather upper-deck ports are shut, the sea at their sills.", "starboard", False),
    ]
    # the lee's words answer the lee's line and never the weather's, which the roll brings
    # (`api/practice_readings.py`; a book `at the lee ports shut` acts on the lee side alone)
    lee_words = readings.EVENTS["the lee ports shut"]
    said = [readings.event_matches(lee_words, e.kind, e.data) for e in _port_lines(w)]
    assert said == [True, False]


@pytest.mark.parametrize(
    "path", [CUTTER, PRIVATEER, BRIG, FRIGATE, SIXTY_FOUR, RAZEE, MERCHANT_BRIG]
)
def test_the_one_compare_short_of_the_least_dip_changes_no_port(path):
    """A tick short of the battery's least dip reads no gun (`ports._least_dip`), for the pace.
    It stands a hair under the lowest port the rule shuts, and a battery with the compare
    shuts and opens the same ports as one without it, both ways and on either side."""
    ship = load_ship(path)
    battery = Battery(ship)
    whole = Battery(ship)
    whole._least_shut_dip = -1.0  # never short of it
    profile = ship.hull.spec.profile
    heels = [
        shut_heel(g.height_m, half_breadth_at_sill(profile, g.deck, g.x_m))
        for g in ship.guns.values()
        if g.place in ports.PORT_PLACES
        and g.height_m - SHUT_M < half_breadth_at_sill(profile, g.deck, g.x_m)
    ]
    least = ports._least_dip(battery, firer_at(0.0))
    assert least < min(heels) < least + 1e-5
    ports.update(battery, firer_at(least - 0.01), 0)
    assert not battery._shut
    ports.update(battery, firer_at(min(heels) + 0.01), 1)
    assert battery._shut
    battery._shut = frozenset()
    battery._ports_told = frozenset()
    sweep = [h / 4.0 for h in range(0, 161)]
    heels_swept = sweep + sweep[::-1] + [-h for h in sweep] + [-h for h in sweep[::-1]]
    for tick, heel in enumerate(heels_swept, start=2):
        firer = firer_at(heel)
        assert ports.update(battery, firer, tick) == ports.update(whole, firer, tick), heel
        assert battery._shut == whole._shut, heel


def test_no_sea_no_roll():
    """A World that keeps no sea reads no roll for the rule to take (§7.1, map-engine §10
    item 4); one that keeps a sea, her own motion."""
    w = _quiet(CUTTER)
    assert w.sea is None and w.motion is None
    assert action._firer(w, w.ship).roll_deg == 0.0
    sea = make_world(
        SEED,
        CUTTER,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=20.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=90.0,
            sea=True,
        ),
    )
    sea.run(120)
    assert sea.motion is not None and sea.ship.extra["motion"] is sea.motion
    assert action._firer(sea, sea.ship).roll_deg == sea.motion.roll_deg > 0.0


@pytest.mark.parametrize("roll", [3.0, 12.0])
@pytest.mark.parametrize("path", [CUTTER, PRIVATEER, FRIGATE, SIXTY_FOUR])
def test_the_one_compare_takes_the_roll(path, roll):
    """`ports._least_dip`'s compare is the roll plus the heel: with a roll on, a battery with the
    compare shuts and opens the same ports as one without it, both ways and on either side."""
    ship = load_ship(path)
    battery = Battery(ship)
    whole = Battery(ship)
    whole._least_shut_dip = -1.0  # never short of it
    sweep = [h / 4.0 for h in range(0, 161)]
    heels_swept = sweep + sweep[::-1] + [-h for h in sweep] + [-h for h in sweep[::-1]]
    for tick, heel in enumerate(heels_swept):
        firer = firer_at(heel, roll_deg=roll)
        assert ports.update(battery, firer, tick) == ports.update(whole, firer, tick), heel
        assert battery._shut == whole._shut, heel


# -- truth 7-190 (§15), drafted here for Phase 5 to move into tests/test_known_truths.py --------

# Each armed file and her default fit: the deck and shut heel of her lowest port with a gun in it
# by §7.1's arithmetic on her drawn hull, degrees (L2's `LOWEST_WITH_A_GUN`, read again at L3),
# and the count of that deck's lee ports shut a degree above it (measured). Every file of
# `data/ships` whose default fit has a port gun is a row (the truth's last line below).
LOWEST_LEE_PORT = (
    (BRIG, "diligence class 1796", "upper", 17.5, 4),
    (CUTTER, "carronades", "upper", 14.7, 2),
    (FRIGATE, "amazon class 1795", "upper", 19.7, 5),
    (MERCHANT_BRIG, "merchant", "upper", 18.2, 2),
    (PRIVATEER, "long tom", "upper", 13.5, 1),
    (RAZEE, "as carried 1796", "upper", 14.5, 6),
    (SIXTY_FOUR, "ardent class 1784", "lower", 10.55, 6),
)
# The razee's three decks with guns in them, as lines of the truth (§15, "Not truths, said";
# Indf §3.4): her main battery the 64's lower deck raised by her rise, and the two above it.
RAZEE_DECKS = (("upper", 14.5, 6), ("quarterdeck", 42.02, 1), ("forecastle", 43.84, 1))
# The 74's lowest lee port shuts at 10.6 degrees of heel alone: the *Bellona*'s 5 ft 2 in at
# Channel draught on 22.7 ft (Research-74-2026-10.md §13.1 answer 5, revised by the owner
# 2026-10-28; §15's row 7-195). Her file is not built yet, so the figure is §15's and Bel's.
SEVENTY_FOURS_SHUT_DEG = 10.6
# The roll set on the World's motion for the truth's second half (judgement: a ship "rolling"
# in the motion's words, `physics.motion.ROLL_ROLLING_DEG` 6, short of heavily).
ROLL_SET_DEG = 4.0


def _in_a_sea(path: str, fit: str | None = None):
    """A World that keeps a sea (`sea: true` under a fixed wind), so that she has her motion;
    her default fit unless one is named."""
    w = make_world(
        SEED,
        path,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=6.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=90.0,
            ship_speed_kn=0.0,
            sea=True,
            fit=fit,
        ),
    )
    assert w.motion is not None and w.ship.extra["motion"] is w.motion
    return w


def _ports_at(w, heel_deg: float, roll_deg: float, tick: int) -> frozenset[str]:
    """Her ports as the rule reads them at this heel (to starboard) and this roll, both set on
    the World's own names (`ship.dyn.heel`, `world.motion`) and read through `action._firer`,
    at a tick of the test's own (the hold counts in ticks)."""
    w.ship.dyn.heel = math.radians(heel_deg)
    w.motion.roll_deg = roll_deg
    battery = battery_of(w.ship)
    ports.update(battery, action._firer(w, w.ship), tick)
    return battery._shut


def _lowest_lee(w, deck: str):
    """Her lowest starboard port gun of the deck, and its shut heel by §7.1's arithmetic (a sill
    higher above the shut line than the side is broad never shuts on the heel, and is passed)."""
    profile = w.ship.hull.spec.profile
    heels = {}
    for g in w.ship.guns.values():
        if g.place in ports.PORT_PLACES and g.side == "starboard" and g.deck == deck:
            half = half_breadth_at_sill(profile, g.deck, g.x_m)
            if g.height_m - SHUT_M < half:
                heels[g.id] = shut_heel(g.height_m, half)
    gid = min(heels, key=heels.get)
    return gid, heels[gid]


def _open_then_shut(w, deck: str, figure: float, roll: float, at: int) -> tuple[int, int]:
    """Her lowest lee port of the deck open half a degree below its shut heel less the roll, and
    shut a degree above it; the counts shut at each, the weather side open at both; upright
    with no roll every port open again once the minute's hold has run, from tick `at`."""
    gid, heel = _lowest_lee(w, deck)
    assert heel == pytest.approx(figure, abs=0.05), (w.ship.name, deck)
    assert not _ports_at(w, 0.0, 0.0, at)
    below = _ports_at(w, heel - roll - 0.5, roll, at + 1)
    assert gid not in below
    above = _ports_at(w, heel - roll + 1.0, roll, at + 2)
    assert gid in above
    assert all(w.ship.guns[g].side == "starboard" for g in below | above)
    counts = (
        sum(1 for g in below if w.ship.guns[g].deck == deck),
        sum(1 for g in above if w.ship.guns[g].deck == deck),
    )
    assert _ports_at(w, 0.0, 0.0, at + 1 + HOLD)  # held a tick short of the minute
    assert not _ports_at(w, 0.0, 0.0, at + 2 + HOLD)
    return counts


@pytest.mark.parametrize("path,fit,deck,figure,count", LOWEST_LEE_PORT)
def test_truth_7_190_every_armed_files_lowest_lee_port_shuts_at_its_heel_and_a_roll_sooner(
    path, fit, deck, figure, count
):
    """**A draft, for Phase 5 to move into `tests/test_known_truths.py` and measure again on the
    merged tree** (Build-Ships.md §15, row 7-190; the lead's ruling; the owner's rule, Bel §13.1
    answer 7: the dip is the heel toward the gun's side plus the roll's amplitude). Each armed
    file's default fit in a World that keeps a sea (`sea: true`, six knots, seed 7), her heel
    to starboard and her roll set by hand on the World's own names (`ship.dyn.heel`,
    `world.motion`) and read through `action._firer`, the rule run on her battery: no tick, no
    digest. Her lowest port with a gun in it, on her drawn hull: the brig's 17.5, the cutter's
    14.7, the frigate's 19.7, the merchant brig's 18.2, the long tom's 13.5, the razee's 14.5
    and the 64's lower deck's 10.55 degrees (±0.05). With no roll, no port of that deck shut
    half a degree below that heel, and that port shut a degree above it, with 4, 2, 5, 2, 1, 6
    and 6 of the deck's lee ports; with a roll of 4 degrees on the World's motion, the same
    four degrees of heel sooner, a roll's amplitude, by the same counts. Her weather side open
    throughout; upright with no roll, every port open again once the minute's hold has run (the
    lead's ruling of 2026-11-06; at once before it). Measured on the owner's machine,
    2026-11-05, at L3. She is built with no fit named, so that the row's fit is her file's
    default (since L3's review: the fit was named, and the line could not fail)."""
    w = _in_a_sea(path)
    assert w.ship.fit == fit
    assert _open_then_shut(w, deck, figure, 0.0, 0) == (0, count)
    assert _open_then_shut(w, deck, figure, ROLL_SET_DEG, 4 * HOLD) == (0, count)


def test_truth_7_190_the_frigates_lee_ports_stand_open_at_the_seventy_fours_shut_heel():
    """7-190's clause (Bel §6.1, P5, "the frigate unmoved"; `Design-Ship-Bellerophon.md` §14.3
    leaves it to this truth). A draft for Phase 5, as above. At the 74's 10.6 degrees of heel
    alone (`SEVENTY_FOURS_SHUT_DEG`: §15's and Bel's figure, her file not yet built) every port
    of the frigate-36 stands open, heeled to either side, her lowest shutting at 19.7 on her
    drawn hull (Bel's 21.0 was her first written sill); and with a roll of 4 degrees on her
    motion as well."""
    w = _in_a_sea(FRIGATE, None)
    assert _lowest_lee(w, "upper")[1] == pytest.approx(19.7, abs=0.05)
    for tick, roll in enumerate((0.0, ROLL_SET_DEG)):
        assert _ports_at(w, SEVENTY_FOURS_SHUT_DEG, roll, 2 * tick) == frozenset()
        assert _ports_at(w, -SEVENTY_FOURS_SHUT_DEG, roll, 2 * tick + 1) == frozenset()


@pytest.mark.parametrize("deck,figure,count", RAZEE_DECKS)
def test_truth_7_190_the_razees_lee_ports_deck_by_deck(deck, figure, count):
    """The razee's lee ports, lines of 7-190 (§15; Indf §3.4, 10.6 and 14.5 heel alone): her
    main battery is the 64's lower deck raised by her rise, and shuts at 14.5 for the 64's
    10.55 on the drawn hulls (3.95 degrees later, ±0.1); her quarterdeck at 42.02 and her
    forecastle at 43.84. Each open half a degree below and shut a degree above, and a roll's
    amplitude sooner, as the truth's row, with 6, 1 and 1 of the deck's lee ports. A draft for
    Phase 5, as above. Each of her default fit and the 64's."""
    w = _in_a_sea(RAZEE)
    assert w.ship.fit == "as carried 1796"
    assert _open_then_shut(w, deck, figure, 0.0, 0) == (0, count)
    assert _open_then_shut(w, deck, figure, ROLL_SET_DEG, 4 * HOLD) == (0, count)
    if deck == "upper":
        her = _lowest_lee(w, "upper")[1]
        sixty_four = _in_a_sea(SIXTY_FOUR)
        assert sixty_four.ship.fit == "ardent class 1784"
        was = _lowest_lee(sixty_four, "lower")[1]
        assert her - was == pytest.approx(3.95, abs=0.1)


def test_truth_7_190_covers_every_armed_file():
    """7-190 is of every armed file: each file of `data/ships` whose default fit carries a gun
    in a port (`ports.PORT_PLACES`) is a row of `LOWEST_LEE_PORT`, and no row is of a file that
    carries none, so that a ship file added or rearmed is not passed by in silence. Today the
    seven: the brig, the cutter, the frigate-36, the merchant brig, the privateer schooner, the
    razee and the 64 (since L3's review). A draft for Phase 5, as above."""
    armed = {
        path.as_posix()
        for path in sorted(Path("data/ships").glob("*.yaml"))
        if any(g.place in ports.PORT_PLACES for g in load_ship(path.as_posix()).guns.values())
    }
    assert armed == {row[0] for row in LOWEST_LEE_PORT}
    assert len(armed) == 7


# -- the old saves -----------------------------------------------------------------------------


def _an_old_ship(w) -> None:
    """Her guns and her hull as a checkpoint from before package 75 has them: no deck on a gun
    and no profile on the hull, the guns at their pickled heights."""
    w.ship.hull.spec = replace(w.ship.hull.spec, profile=None)
    for gun in w.ship.guns.values():
        gun.deck = None
    battery = battery_of(w.ship)
    for name in ("_shut", "_port_breadths", "_least_shut_dip", "_sea_at_sill"):
        battery.__dict__.pop(name, None)


def test_an_old_battery_with_no_shut_reads_the_class_defaults():
    """A `Battery` pickled before the ports: no `_shut` and no held half-breadths of its own."""
    ship = load_ship(CUTTER)
    made = Battery(ship)
    old = Battery.__new__(Battery)
    old.__dict__.update(made.__dict__)
    assert "_shut" not in old.__dict__ and "_port_breadths" not in old.__dict__
    assert old._shut == frozenset() and old._port_breadths is None
    assert ports.update(old, firer_at(0.0), 0) == (frozenset(), frozenset())
    assert "_shut" not in old.__dict__  # nothing to hold, nothing written
    assert "_sea_at_sill" not in old.__dict__ and old._sea_at_sill is None


def test_an_old_checkpoint_of_a_ship_with_guns_loads_and_fights_at_its_old_heights(tmp_path):
    """§16.2: an old ship with no profile and no gun decks reads her pickled heights on half
    the beam, through the checkpoint's own road. The old heel is the old height's."""
    w = _quiet(CUTTER)
    w.run(2)
    _an_old_ship(w)
    old_heights = {g.id: g.height_m for g in w.ship.guns.values()}
    path = replay.write_checkpoint(w, tmp_path / "old.checkpoint")
    _, loaded = replay.read_checkpoint(path)
    battery = battery_of(loaded.ship)
    assert "_shut" not in battery.__dict__
    assert all(g.deck is None and "deck" not in g.__dict__ for g in loaded.ship.guns.values())
    assert loaded.ship.hull.spec.profile is None
    loaded.run(5)
    gun = _at_x(loaded.ship, -0.5)
    half = loaded.ship.hull.spec.beam_m / 2.0
    shut = shut_heel(old_heights[gun.id], half)
    firer = firer_at(shut - 0.01, half)
    ports.update(battery, firer, loaded.clock.tick)
    assert gun.id not in battery._shut
    firer = firer_at(shut + 0.01, half)
    ports.update(battery, firer, loaded.clock.tick + 1)
    assert gun.id in battery._shut


def test_a_checkpoint_with_ports_shut_comes_back_shut_and_says_nothing_again(heeled, tmp_path):
    w = _quiet(CUTTER)
    cast_loose(w.ship)
    w.run(2)
    heeled["deg"] = 20.0
    w.run(3)
    shut = battery_of(w.ship)._shut
    assert shut and len(_port_lines(w)) == 1
    path = replay.write_checkpoint(w, tmp_path / "shut.checkpoint")
    _, loaded = replay.read_checkpoint(path)
    assert battery_of(loaded.ship)._shut == shut
    loaded.run(3)
    assert battery_of(loaded.ship)._shut == shut and len(_port_lines(loaded)) == 1


def test_the_kept_saves_load_by_the_checkpoint_road_and_run_on():
    """§16.2's kept saves, read under this build (the fast tier reads them whole in
    `tests/test_checkpoint.py`). None of the three has a gun: the rule on a real old ship with
    guns is the next test's."""
    save = "tests/fixtures/saves/m5c-c-37d-officer-tick5400.json"
    world, report = replay.load_report(save, ship_factory)
    assert report.how == "checkpoint"
    before = world.clock.tick
    world.run(120)
    assert world.clock.tick == before + 120


def test_a_real_checkpoint_from_before_the_package_fights_at_its_old_heights(heeled):
    """§16.2, on a checkpoint the commit before stage 0 wrote: no profile on her hull and no
    deck on a gun, not even as an attribute of the pickled gun, and her guns at their pickled
    1.5 m on half her beam of 5.8 m, shut at 24.34 degrees. The ports shut by the rule, the
    guns run in, the lines say no deck, and they open again; what it holds goes back to disk."""
    _, w = replay.read_checkpoint(PRE_75_CUTTER)
    ship = w.ship
    battery = battery_of(ship)
    assert ship.hull.spec.profile is None
    assert all("deck" not in g.__dict__ and g.deck is None for g in ship.guns.values())
    assert "_shut" not in battery.__dict__ and "_port_breadths" not in battery.__dict__
    assert any(g.cast_loose for g in ship.guns.values())
    lee = [g for g in ship.guns.values() if g.place == "broadside" and g.side == "starboard"]
    assert {g.height_m for g in lee} == {1.5} and ship.hull.spec.beam_m / 2.0 == 2.9
    shut = shut_heel(1.5, 2.9)
    assert shut == pytest.approx(24.34, abs=0.01)
    w.run(30)
    heeled["deg"] = shut - 0.05
    w.run(3)
    assert battery._shut == frozenset() and not _port_lines(w)
    heeled["deg"] = shut + 0.05
    w.run(3)
    assert {g.id for g in lee} == battery._shut
    assert not any(g.run_out for g in lee)
    assert [e.text for e in _port_lines(w)] == ["The lee ports are shut, the sea at their sills."]
    assert set(battery._port_breadths.values()) == {None}
    heeled["deg"] = 0.0
    w.run(HOLD + 3)
    assert battery._shut == frozenset()
    assert [e.text for e in _port_lines(w)[1:]] == [
        "The lee ports are opened again, their sills clear of the sea."
    ]


def test_a_real_checkpoint_from_before_the_package_comes_round_the_disk(heeled, tmp_path):
    _, w = replay.read_checkpoint(PRE_75_CUTTER)
    w.run(3)
    heeled["deg"] = 30.0
    w.run(3)
    shut = battery_of(w.ship)._shut
    assert shut
    path = replay.write_checkpoint(w, tmp_path / "again.checkpoint")
    _, again = replay.read_checkpoint(path)
    assert battery_of(again.ship)._shut == shut
    assert battery_of(again.ship)._ports_told == battery_of(w.ship)._ports_told
    again.run(3)
    assert len(_port_lines(again)) == len(_port_lines(w)) == 1
