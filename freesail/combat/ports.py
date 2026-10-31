"""The lee ports (package 75; docs/design/Build-Ships.md §3.1 item 17, §7): a gun's port shut
when the sea comes to its sill, and opened again when the sill stands clear of it.

**The rule** (§7.1): for a gun placed broadside, bow or stern (`PORT_PLACES`; a pivot and a
rail gun fire over the rail and have no port), the dip is the heel toward the gun's side plus
the roll's amplitude, never below nought, the other side's the roll less the heel; the sill
lowered is the gun's `height_m` less the side's half-breadth at the sill
(`ship.profile.half_breadth_at_sill`, held once a gun; else half the beam, a gun with no deck
or a ship with no profile: an old save, a boat) times the sine of the dip; the port is shut
when the sill lowered is within `shot.PORT_SHUT_M` of the water (`shot.lee_port_shut`), and
opened again when it stands `PORT_REOPEN_M` clear of that, so that a port does not flicker in
a gust.

**The roll is held at nought (L2, §7.3): the heel alone.** `roll_in_the_dip` is the one place
the rule reads a roll, and L3 makes it `firer.roll_deg`, in its own commit, with nothing else
to change. What it will read: `Firer.roll_deg`, her World's motion, is the player's ship's
own where her World keeps a sea (`Scenario.sea`, or weather systems and no script), and
nought in a World that keeps none; a crewed ship's reads nought wherever she sails, for
`crews._crew_scenario` builds her with no sea and no motion though the World round her has
both.

**The wiring** (§7.2): `update` is called once a tick at the head of `guns.Battery.tick`, and
keeps every port gun's state in `Battery._shut`, secured or cast loose, for a port is shut by
the sea and not by the bill. The log says it once a change of state a deck and side: a deck's
side is shut when any port of it is, from the first to shut until the last has opened (the
`guns` reading counts them), so that its line is not said gun by gun as she heels. A gun
whose port shuts is run in, its loading goes on and it fires nothing; a gun named to fire
behind it, or the word for a broadside all behind them, is dropped with a line, and a division
all behind them holds no turn, so that a shut port silences its own gun and no other
(`Battery`). The far fight has no heel and no ports (`combat/far.py`).

**The line is the guns' (judgement, on §7.3's pins).** It is said only while a gun of that
deck's side is cast loose: at the port's shutting with her guns cast loose, or at the casting
loose with the port shut already. With the guns secured on passage the ports are shut by the
routine of the ship and there is nothing to tell, the state is kept and the reading says it,
and no sailing passage's log moves: said on passage as well, the line moved the captain's
trials' line counts (the station's lee shore 1,561 to 1,563, its gale 1,722 to 1,724), where
§7.3 and §16.1 expect only the actions to move.
"""

from __future__ import annotations

import math
from typing import Any

from freesail.combat import shot as S
from freesail.ship.profile import half_breadth_at_sill

__all__ = ["PORT_PLACES", "PORT_REOPEN_M", "roll_in_the_dip", "update"]

# The places of a gun that fires through a port in the side, the bow or the stern (a pivot
# and a rail gun fire over the rail: docs/design/Proposal-PivotGun.md §4.4); the schema's
# gun deck rule reads the same three (`schema._PORT_GUN_PLACES`).
PORT_PLACES: tuple[str, ...] = ("broadside", "bow", "stern")
# A shut port is opened again when its sill lowered stands this far clear of the shut
# line: six inches (judgement), so that a port does not open and shut with each gust.
PORT_REOPEN_M = 0.15
# The decks said with "-deck" in the log's line ("the lee upper-deck ports"); the others are
# their own word ("the lee quarterdeck ports"; `schema.DECK_WORDS`).
_DECKS_SAID_SO = ("lower", "middle", "upper")

_NONE: frozenset[str] = frozenset()


def roll_in_the_dip(firer: Any) -> float:
    """The roll's amplitude in the dip, in degrees. Held at nought: L2 is the heel alone
    (Build-Ships.md §7.3), and L3 makes this `float(firer.roll_deg)` and changes nothing
    else (`tests/test_lee_ports.py`'s `test_the_roll_is_held_at_nought` moves with it)."""
    return 0.0


def update(battery: Any, firer: Any) -> tuple[frozenset[str], frozenset[str]]:
    """The battery's ports this tick against the rule (the module's head): the ids of the
    guns whose ports were shut this tick and of those opened, each set once a change of
    state, the battery's `_shut` set to the guns now shut and the log told of a deck's side
    that has changed. `_shut` is not written while nothing changes. With no port shut and
    none told, a tick whose dip is short of the battery's least (`_least_dip`) costs one
    compare; else a sine and a compare a port gun."""
    from freesail.combat.guns import _is_lee  # guns imports this module

    was = battery._shut
    heel_deg = firer.heel_deg
    heel = abs(heel_deg)
    roll = roll_in_the_dip(firer)
    if not was and not battery._ports_told and roll + heel < _least_dip(battery, firer):
        return _NONE, _NONE
    shut: list[str] = []
    opened: list[str] = []
    for gun in battery.ship.guns.values():
        if gun.place not in PORT_PLACES:
            continue
        half_breadth = _half_breadth(battery, gun, firer)
        dip = max(0.0, roll + heel if _is_lee(gun, heel_deg) else roll - heel)
        if gun.id in was:
            if not S.lee_port_shut(gun.height_m - PORT_REOPEN_M, dip, half_breadth):
                opened.append(gun.id)
        elif S.lee_port_shut(gun.height_m, dip, half_breadth):
            shut.append(gun.id)
    now, newly, reopened = was, _NONE, _NONE
    if shut or opened:
        newly, reopened = frozenset(shut), frozenset(opened)
        now = (was | newly) - reopened
        battery._shut = now
    if now or battery._ports_told:
        _tell(battery, now, reopened, heel_deg, _is_lee)
    return newly, reopened


def _least_dip(battery: Any, firer: Any) -> float:
    """The least dip that shuts a port of this battery, in degrees, read once and held: no
    side's dip is above the roll plus the heel, so below this no port can shut and a tick need
    read no gun. A hair under the rule's own figure, so that it never stands in the rule's way;
    a class default on the battery, as `_port_breadths` is."""
    least = battery._least_shut_dip
    if least is None:
        least = 90.0
        for gun in battery.ship.guns.values():
            if gun.place in PORT_PLACES:
                above = gun.height_m - S.PORT_SHUT_M
                half_breadth = _half_breadth(battery, gun, firer)
                if above <= 0.0:
                    least = 0.0
                elif above < half_breadth:
                    least = min(least, math.degrees(math.asin(above / half_breadth)) - 1e-6)
        battery._least_shut_dip = least
    return least


def _half_breadth(battery: Any, gun: Any, firer: Any) -> float:
    """The side's half-breadth at the gun's sill, read from the profile once a gun and held;
    half the beam for a gun with no deck, a ship with no profile, or a deck with no ports in
    it (§7.1). A class default on the battery, so that one pickled before it makes its own."""
    held = battery._port_breadths
    if held is None:
        held = battery._port_breadths = {}
    if gun.id in held:
        breadth = held[gun.id]
    else:
        profile = getattr(getattr(battery.ship.hull, "spec", None), "profile", None)
        deck = getattr(gun, "deck", None)
        breadth = None
        if profile is not None and deck is not None:
            breadth = half_breadth_at_sill(profile, deck, gun.x_m)
        held[gun.id] = breadth
    return firer.half_beam_m if breadth is None else breadth


def _by_deck(guns: dict[str, Any], ids: frozenset[str]) -> dict[tuple[str, str], list[str]]:
    """The guns of these ids by their deck and side, in order, for the log (a set's order is
    the process's own, and the log's must not be)."""
    out: dict[tuple[str, str], list[str]] = {}
    for gid in sorted(ids):
        gun = guns.get(gid)
        if gun is not None:
            out.setdefault((gun.deck or "", gun.side or ""), []).append(gid)
    return out


def _tell(
    battery: Any, now: frozenset[str], reopened: frozenset[str], heel_deg: float, is_lee: Any
) -> None:
    """The log's lines for the deck's sides that have changed state (the module's head): shut,
    with a port of it shut and a gun of it cast loose, told once; opened, when the last port of
    a side so told has opened. Guns secured with their port still shut say nothing, then or
    when it opens."""
    ship = battery.ship
    guns = ship.guns
    shut = _by_deck(guns, now)
    fighting = {key: ids for key, ids in shut.items() if any(guns[g].cast_loose for g in ids)}
    told = battery._ports_told
    if told == frozenset(fighting):
        return
    battery._ports_told = frozenset(fighting)
    lines = [(key, ids, True) for key, ids in fighting.items() if key not in told]
    gone = _by_deck(guns, reopened)
    lines += [(key, gone[key], False) for key in told if key not in shut and key in gone]
    for (deck, side), ids, closing in sorted(lines):
        # upright she has no lee, and a port opening as she comes upright was the lee's; a
        # chaser on the centre line has neither side's word
        lee = None if not side else heel_deg == 0.0 or is_lee(guns[ids[0]], heel_deg)
        which = "" if lee is None else "lee " if lee else "weather "
        said = f"{deck}-deck " if deck in _DECKS_SAID_SO else f"{deck} " if deck else ""
        if closing:
            kind = "guns.ports_shut"
            text = f"The {which}{said}ports are shut, the sea at their sills."
        else:
            kind = "guns.ports_opened"
            text = f"The {which}{said}ports are opened again, their sills clear of the sea."
        ship.note(
            "notable",
            kind,
            text,
            ids[0],
            {
                "deck": deck or None,
                "side": side or None,
                "lee": lee,
                "guns": ids,
                "heel_deg": round(abs(heel_deg), 1),
            },
        )
