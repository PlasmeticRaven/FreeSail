"""The gunner's filling of cartridges from the powder below (practice and resupply, between
packages 72 and 73; docs/design/Build-PracticeAndResupply.md §4).

The magazine keeps its filled cartridges by gun kind and calibre and its loose powder in
the barrels below (`ship.parts.Magazine`). While a kind is below its level the gunner fills,
once a minute from the action's tick (`combat.action.tick_action`): at quarters with the men
of the powder division who are not lent out (the Regulations 1806, 1808 printing, the
Gunner, Art. XVIII, OCR l.13065-13071: he is "to take all opportunities of filling powder"
during an action), out of quarters while the idlers are up with the gunner and his crew in
the filling room (Falconer 1780, QUARTER-GUNNER, l.14283-14289), never by night out of
quarters (Art. VII, l.12843-12850: the magazine is not opened until the proper officer is
in the light room; the night is judgement), never while the hoy is alongside and never
after the colours are struck. The men are read and never moved; the filling draws nothing
and says nothing at quarters but the powder's running out. That the fillers take no hands
from other work stands against the work in action's rule that every task competes for
hands (the build's decision 5): a stopgap, folded in by package 86 with the line in package
75's and 77's briefs that makes the gunner, his crew and the quarter gunners real posts
that compete for hands (77's, with the gunnery's evolutions, unless 75 takes it first).

The party is the quarter bill's `filling`, one man to every four cannon (Falconer's
quarter-gunner to every four cannon; the swivels are not cannon), reckoned so where the bill
does not say it (a bill pickled before it, or a hand-written file). Each man gives sixty
man-seconds a minute, and a cartridge takes `ship.parts.fill_seconds` of its charge. The
fillers' fatigue is left out (the build design's §10).

Its own lines, each once a change of state: `guns.powder_out` (NOTABLE) when the minute's
filling leaves the powder below under the charge of every kind still short, once until
powder comes aboard (a store that had nothing below to fill from, as one converted from
packages 70 to 72, never filled, so it never says it); `guns.filled` (ROUTINE), out of
quarters, when the last kind comes back to its level after a receipt or `fill cartridges`
asked for the report (`Magazine.report_filled`). A kind back at its level at quarters keeps
the report until she is out of them; a request when nothing was short is forgotten, for
nothing came back. The guns' own line, `guns.filling`, said while they wait at the
cartridge phase (`combat.guns`), may be said again once its kind is back at its level: this
discards it from the battery's once-set.
"""

from __future__ import annotations

from typing import Any

from freesail.core.events import Severity
from freesail.crew.bill import idlers_up
from freesail.crew.quarters import POWDER
from freesail.ship.parts import magazine, powder_words

__all__ = [
    "CANNON_A_FILLER",
    "MAN_SECONDS_A_MINUTE",
    "fill_tick",
    "fillers",
    "filling_of",
    "magazine_lines",
    "not_filling",
]

# One quarter gunner to every four cannon (Falconer 1780, QUARTER-GUNNER, l.14288-14289).
CANNON_A_FILLER = 4
MAN_SECONDS_A_MINUTE = 60.0


def filling_of(ship: Any) -> int:
    """The quarter bill's men filling cartridges: its `filling`, else one to every four
    cannon of her guns (the swivels not cannon), one at the least."""
    spec = getattr(getattr(ship, "spec", None), "crew", None)
    bill = getattr(spec, "quarter_bill", None)
    n = getattr(bill, "filling", None)
    if n is not None:
        return int(n)
    cannon = sum(1 for g in (getattr(ship, "guns", None) or {}).values() if g.kind != "swivel")
    return max(1, cannon // CANNON_A_FILLER)


def fillers(world: Any, ship: Any, quarters: Any) -> int:
    """The men at the filling this minute: at quarters the first of the bill's `filling`
    of the powder division, in id order, who are fit and not lent to other work (read, and
    never moved); out of quarters the bill's `filling` while the idlers are up (the gunner
    and his crew in the filling room, notionally: nobody's `at` moves), and nobody by
    night."""
    n = filling_of(ship)
    if quarters is not None and getattr(quarters, "at_quarters", False):
        powder = sorted(
            (s for s in (quarters.divisions.get(POWDER) or []) if s.fit and s.at is None),
            key=lambda s: s.id,
        )
        return len(powder[:n])
    if idlers_up(world.clock):
        return n
    return 0


# Why the gunner fills nothing this minute, as the magazine's reading says it after the
# kind he would fill for ("the gunner not filling for the 12-pounder carronades by night").
NIGHT_WORDS = " by night"
HOY_WORDS = " while the hoy is alongside"
STRUCK_WORDS = ", the colours struck"
NO_MAN_WORDS = ", no man of the powder to spare"


def _gate(world: Any, ship: Any, quarters: Any) -> tuple[str, int]:
    """The filling's gate beside the magazine's own (`short`, `filling_held`, the powder):
    why nothing is filled this minute, in `NIGHT_WORDS`' kind of words ("" when he fills),
    and the men at it."""
    extra = getattr(ship, "extra", None) or {}
    if extra.get("struck"):
        return STRUCK_WORDS, 0
    if getattr(getattr(world, "stores", None), "galley_fire_out", ""):
        return HOY_WORDS, 0  # the magazine open to the hoy: no light (the Gunner, Art. V)
    men = fillers(world, ship, quarters)
    if men <= 0:
        at_quarters = quarters is not None and getattr(quarters, "at_quarters", False)
        if not at_quarters and not idlers_up(world.clock):
            return NIGHT_WORDS, 0
        return NO_MAN_WORDS, 0
    return "", men


def not_filling(world: Any, ship: Any) -> str:
    """Why the gunner is not filling now though a kind is short and the powder below would
    fill it (the colours struck, the hoy alongside, by night out of quarters, or no man of
    the powder division to spare at quarters), for the magazine's reading
    (`Magazine.describe`); "" when nothing stops him. The gate `fill_tick` keeps; read,
    and nothing made (the ship's quarters as they stand)."""
    quarters = (getattr(ship, "extra", None) or {}).get("quarters")
    return _gate(world, ship, quarters)[0]


def magazine_lines(world: Any, ship: Any, mag: Any) -> list[str]:
    """The magazine's lines as the reading, the gunner's account and the supply's refusals
    say them (`Magazine.describe`), with why the gunner is not filling now while a kind is
    short and he is not (`not_filling`)."""
    stopped = not_filling(world, ship) if getattr(mag, "short", False) else ""
    return mag.describe(stopped) if stopped else mag.describe()


def fill_tick(world: Any, battery: Any, quarters: Any) -> None:
    """The gunner's minute at the filling (the module's head). It returns at once while the
    magazine is full (`not mag.short`; a report asked for is said or forgotten there), the
    filling is held, she is struck, the galley fire is out for the hoy, or no man is to be
    had; else the party's man-seconds go to `Magazine.fill`."""
    ship = battery.ship
    mag = magazine(ship)
    if battery._said_filling:
        _clear_said(battery, mag)
    if not mag.short:
        if mag.report_filled:
            _report_filled(world, mag, quarters)
        return
    if mag.filling_held:
        return
    why, men = _gate(world, ship, quarters)
    if why:
        return
    # whether some kind still short could be filled before this minute: the powder's running
    # out is told only when the filling itself brings the powder under the charges
    could = mag.neediest() is not None
    if mag.fill(MAN_SECONDS_A_MINUTE * men) and mag.report_filled:
        mag.report_due = True  # a cartridge filled since the report was asked for
    if battery._said_filling:
        _clear_said(battery, mag)
    if mag.short:
        if could and not mag.said_powder_out and mag.neediest() is None:
            _say_powder_out(world, mag)
        return
    if mag.report_filled:
        _report_filled(world, mag, quarters)


def _say_powder_out(world: Any, mag: Any) -> None:
    """The gunner's report that the powder below will fill no more of what is short: in the
    build design's words when none is left (§4), else with what is left and for which guns
    it is too little."""
    mag.said_powder_out = True
    n = mag.short_by()
    lb = float(mag.powder_lb)
    short = f"{n} cartridge{'s' if n != 1 else ''} short of the allowance."
    if lb <= 1e-9:
        text = f"The gunner reports all the powder filled: no loose powder below, and {short}"
    else:
        level = mag.level or {}
        kinds = " or ".join(
            f"the {mag.words_of(k)}" for k, lvl in level.items() if mag.filled_of(*k) < lvl
        )
        text = (
            "The gunner reports the powder below too little to fill another cartridge for "
            f"{kinds}: {powder_words(lb)} below, and {short}"
        )
    world.record(
        Severity.NOTABLE,
        "guns.powder_out",
        text,
        data={"short": n, "powder_lb": round(lb, 4)},
    )


def _report_filled(world: Any, mag: Any, quarters: Any) -> None:
    """The magazine complete with the report asked for (`report_filled`): said out of
    quarters when a cartridge was filled since it was asked (`report_due`), kept while she
    is at quarters (the filling says nothing there), and forgotten when nothing was filled,
    a receipt or `fill cartridges` into a complete magazine, whose own words say so."""
    if not mag.report_due:
        mag.report_filled = False
        return
    if quarters is not None and getattr(quarters, "at_quarters", False):
        return
    mag.report_filled = False
    mag.report_due = False
    level = mag.level or {}
    counts = ", ".join(f"{n} for the {mag.words_of(k)}" for k, n in level.items())
    world.record(
        Severity.ROUTINE,
        "guns.filled",
        f"The gunner has the cartridges filled to the allowance: {counts}; "
        f"{powder_words(mag.powder_lb)} below.",
        data={
            "powder_lb": round(float(mag.powder_lb), 4),
            "filled_by_gunner": int(mag.filled_by_gunner),
        },
    )


def _clear_said(battery: Any, mag: Any) -> None:
    """The waits told for kinds now back at their level forgotten, so that the next outage
    of each is told (a new set assigned, the old never mutated)."""
    level = mag.level or {}
    said = battery._said_filling
    back = {k for k in said if mag.filled_of(*k) >= level.get(k, 0)}
    if back:
        battery._said_filling = said - back
