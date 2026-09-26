"""Strain, wear and carrying away: what the press of sail does to the gear.

Package 4 (`sails.py`) writes `load_kn` on every sail, spar and line each
physics substep. This module, called once per tick after the substeps
(`apply_strain`, from `integrate.step`), judges those loads against each
part's `rating_kn` and applies spec §7.5:

- `ratio = load / rating`. At or below 1.0 nothing happens. Nothing ever
  recovers: repair is milestone 8.
- Above 1.0 the part's `condition` (0..100) decays at `2 * (ratio - 1)`
  points per minute, and the log gets a notable `strain.warning` for the
  part once every ten minutes while it stays strained.
- Above 1.5 the part may carry away at any substep with probability
  `0.002 * (ratio - 1.5)^2`, drawn from the named random stream `strain`.
  It carries away for certain when its condition reaches 0. A set sail
  blows out for certain above 1.8 of its cloth rating.

Randomness comes only from `ship.extra["rng"].stream("strain")` (the
session composer sets `ship.extra["rng"]`) or, failing that, from a stream
passed in. With neither, the probability is zero: a bare ship stepped in a
unit test is deterministic and only the certain failures happen.

What carrying away does
-----------------------
- A **halyard** parts: its yard (or gaff) comes down and the sail hangs in
  the gear (`SailState.IN_THE_GEAR`), giving no drive. It cannot be set
  again until the halyard is repaired (milestone 8): `set` hoists via the
  halyard and the runner fails the hoist on a parted line.
- A **sheet** parts: the sail is freed and flogs. Its state becomes
  `LOOSED` (package 4 then gives it no drive and a fifth or so of its area
  in windage), and each tick this module puts the flogging load on its
  yard and the spars beneath: twice the drag of a fifth of the cloth. The
  sail is re-sheeted by `set`, whose sheet-home step runs from `loosed`.
- A **brace** parts: the yard swings until it lies along the apparent
  wind. Each tick the yard's `brace_angle` is set so its chord follows the
  apparent wind angle (capped at `SWUNG_YARD_MAX`, where the yard fouls the
  rigging), so the sail luffs and gives no thrust. A brace evolution can
  ramp the angle but the yard swings back the same tick.
- A **stay** with a sail hanked to it parts: the sail comes down with it
  and hangs in the gear.
- A **spar** carries away: it and everything that `Ship.dependents()`
  returns for it (spars above it, their sails, their lines) are marked
  `wrecked`. Package 4 gives a wrecked sail no force and multiplies the
  windage of wrecked sails and spars by `WRECK_MULTIPLIER` (3.0 in
  `data/sail_classes.yaml`), so the wreck hangs to leeward and drags.
- A **sail** blows out: `SailState.BLOWN_OUT`, no force, a little windage
  from the tatters. A new sail must be bent (milestone 8).

Spars that are `sent_down` carry no load and are never judged; nor are
wrecked parts and parted lines. Their `load_kn` is held at zero.

State this module keeps between ticks lives in `ship.extra["strain"]`
(`StrainState`): elapsed time, when each part was last warned about, which
sails are flogging and which yards have swung, and a record of everything
that has parted, blown out or carried away, for the log, the snapshot and
a later `cut away` order.

Log lines are in the ship's-log voice: short, past tense, concrete.
Everything carried away is `urgent`; a warning is `notable`.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, LineState, Part, Sail, SailState, Spar

# ---------------------------------------------------------------------------
# The rule (spec §7.5)
# ---------------------------------------------------------------------------

DECAY_POINTS_PER_MINUTE = 2.0  # condition lost per minute per unit of ratio above 1.0
DECAY_RATIO = 1.0  # above this the part wears and the log is warned
CARRY_AWAY_RATIO = 1.5  # above this the part may carry away at any substep
CARRY_AWAY_COEFFICIENT = 0.002  # p per substep = this * (ratio - CARRY_AWAY_RATIO)^2
BLOW_OUT_RATIO = 1.8  # a set sail blows out for certain above this of its cloth rating
WARNING_INTERVAL_S = 600.0  # one strain.warning per part per ten minutes
SUBSTEP_S = 0.25  # the physics substep (spec §3.1); the probability is per substep

# A flogging sail (sheet parted): a fifth of the cloth works, as a flat plate,
# and the snatching doubles the load it puts on its yard.
FLOGGING_AREA_FRACTION = 0.2
FLOGGING_DRAG_COEFFICIENT = 1.2
FLOGGING_LOAD_MULTIPLIER = 2.0

# A yard whose brace has parted swings to lie along the apparent wind, until
# it fouls the lee rigging at this angle from square.
SWUNG_YARD_MAX = units.deg_to_rad(80.0)

HALYARD_CLASSES = frozenset({"halyard", "throat_halyard", "peak_halyard"})
ALOFT_STATES = frozenset(
    {SailState.SET, SailState.GOOSE_WINGED, SailState.SHEETED, SailState.LOOSED}
)
_SIDES = ("starboard", "larboard")


# ---------------------------------------------------------------------------
# State kept between ticks
# ---------------------------------------------------------------------------


@dataclass
class StrainState:
    """What the strain system remembers, in `ship.extra["strain"]`."""

    elapsed_s: float = 0.0
    last_warning_s: dict[str, float] = field(default_factory=dict)
    flogging: set[str] = field(default_factory=set)  # sails whose sheet has parted
    swung: set[str] = field(default_factory=set)  # yards whose brace has parted
    parted: list[str] = field(default_factory=list)  # line ids, in order
    blown_out: list[str] = field(default_factory=list)  # sail ids, in order
    carried_away: list[str] = field(default_factory=list)  # spar ids, in order (roots only)

    def snapshot(self) -> dict[str, Any]:
        return {
            "flogging": sorted(self.flogging),
            "swung": sorted(self.swung),
            "parted": list(self.parted),
            "blown_out": list(self.blown_out),
            "carried_away": list(self.carried_away),
        }


def strain_state(ship: Ship) -> StrainState:
    """The strain memory for this ship, created on first use."""
    st = ship.extra.get("strain")
    if not isinstance(st, StrainState):
        st = StrainState()
        ship.extra["strain"] = st
    return st


# ---------------------------------------------------------------------------
# The entry point
# ---------------------------------------------------------------------------


def apply_strain(ship: Ship, dt: float, rng_stream: random.Random | None = None) -> None:
    """Judge every loaded part against its rating and carry away what fails.

    Call once per tick after the physics substeps have written `load_kn`.
    `rng_stream` is used only when `ship.extra["rng"]` is absent; with
    neither, nothing fails by chance.
    """
    st = strain_state(ship)
    st.elapsed_s += dt
    stream = _stream(ship, rng_stream)
    _tend_wrecks(ship, st)
    for part in list(ship.parts.values()):  # insertion order: deterministic
        if _out_of_action(part):
            part.load_kn = 0.0
            continue
        ratio = part.strain_ratio
        if ratio <= DECAY_RATIO:
            continue
        part.condition = max(
            0.0, part.condition - DECAY_POINTS_PER_MINUTE * (ratio - DECAY_RATIO) * dt / 60.0
        )
        if _fails(part, ratio, dt, stream):
            _carry_away(ship, st, part, ratio)
        else:
            _warn(ship, st, part, ratio)


def failure_probability(ratio: float, dt: float = 1.0) -> float:
    """The chance a part at this ratio carries away within `dt` seconds by the
    substep rule of §7.5 (zero at or below CARRY_AWAY_RATIO)."""
    if ratio <= CARRY_AWAY_RATIO:
        return 0.0
    p_substep = CARRY_AWAY_COEFFICIENT * (ratio - CARRY_AWAY_RATIO) ** 2
    trials = max(1, round(dt / SUBSTEP_S))
    return 1.0 - (1.0 - min(p_substep, 1.0)) ** trials


# ---------------------------------------------------------------------------
# Judgement
# ---------------------------------------------------------------------------


def _stream(ship: Ship, given: random.Random | None) -> random.Random | None:
    rng = ship.extra.get("rng")
    if rng is not None:
        if hasattr(rng, "stream"):
            return rng.stream("strain")
        if hasattr(rng, "random"):
            return rng
    return given


def _out_of_action(part: Part) -> bool:
    """Wrecked parts, parted lines, sent-down spars and sails not set carry no load."""
    if part.wrecked:
        return True
    if isinstance(part, Spar):
        return part.sent_down
    if isinstance(part, Line):
        return part.state is LineState.PARTED
    if isinstance(part, Sail):
        return part.state not in (SailState.SET, SailState.GOOSE_WINGED)
    return False


def _fails(part: Part, ratio: float, dt: float, stream: random.Random | None) -> bool:
    if part.condition <= 0.0:
        return True
    if isinstance(part, Sail) and ratio > BLOW_OUT_RATIO:
        return True
    if stream is None or ratio <= CARRY_AWAY_RATIO:
        return False
    return stream.random() < failure_probability(ratio, dt)


def _warn(ship: Ship, st: StrainState, part: Part, ratio: float) -> None:
    last = st.last_warning_s.get(part.id)
    if last is not None and st.elapsed_s - last < WARNING_INTERVAL_S:
        return
    st.last_warning_s[part.id] = st.elapsed_s
    name = _name(ship, part.id)
    dire = ratio > CARRY_AWAY_RATIO
    if isinstance(part, Spar):
        text = (
            f"{name} bending like a whip; she will carry it away if sail is not shortened."
            if dire
            else f"{name} working under the press of sail."
        )
    elif isinstance(part, Line):
        text = (
            f"{name} stranding; it will not hold much longer."
            if dire
            else f"{name} bar-taut and surging on the pin."
        )
    else:
        text = (
            f"{name} stretched drum-tight; it will not stand much more."
            if dire
            else f"{name} straining at the bolt-ropes."
        )
    ship.note("notable", "strain.warning", text, subject=part.id, data=_data(part, ratio))


def _data(part: Part, ratio: float) -> dict[str, Any]:
    return {
        "ratio": ratio,
        "load_kn": part.load_kn,
        "rating_kn": part.rating_kn,
        "condition": part.condition,
    }


# ---------------------------------------------------------------------------
# Carrying away
# ---------------------------------------------------------------------------


def _carry_away(ship: Ship, st: StrainState, part: Part, ratio: float) -> None:
    if isinstance(part, Line):
        _part_line(ship, st, part, ratio)
    elif isinstance(part, Spar):
        _wreck_spar(ship, st, part, ratio)
    else:
        _blow_out(ship, st, part, ratio)


def _part_line(ship: Ship, st: StrainState, line: Line, ratio: float) -> None:
    line.state = LineState.PARTED
    line.load_kn = 0.0
    st.parted.append(line.id)
    name = _name(ship, line.id)
    target = ship.parts.get(line.of)
    data = _data(line, ratio)
    data["of"] = line.of
    affected: list[str] = []

    if line.cls in HALYARD_CLASSES:
        sails = _sails_hoisted_by(ship, line)
        for sail in sails:
            if sail.state in ALOFT_STATES:
                sail.state = SailState.IN_THE_GEAR
                st.flogging.discard(sail.id)
                affected.append(sail.id)
        sail_names = _names(ship, affected)
        if isinstance(target, Spar) and target.cls == "gaff":
            what = f"the gaff came down and the {sail_names} hangs in the brails"
        elif isinstance(target, Spar):
            what = f"the yard came down on the cap and the {sail_names} hangs in the gear"
        else:
            what = f"the {sail_names} came down in a heap"
        text = f"{name} parted; {what}." if affected else f"{name} parted."
    elif line.cls == "sheet" and isinstance(target, Sail):
        if target.state is SailState.SET:
            target.state = SailState.LOOSED
            st.flogging.add(target.id)
            affected.append(target.id)
            text = f"{name} parted; the {_name(ship, target.id, False)} flogging itself to ribbons."
        else:
            text = f"{name} parted."
    elif line.cls == "brace" and isinstance(target, Spar):
        st.swung.add(target.id)
        affected.append(target.id)
        _swing_yard(ship, target)
        text = f"{name} parted; the {_name(ship, target.id, False)} swung round to the wind."
    elif line.cls == "stay":
        sails = [s for s in ship.sails.values() if s.roles.get("stay") == line.id]
        for sail in sails:
            if sail.state in ALOFT_STATES:
                sail.state = SailState.IN_THE_GEAR
                st.flogging.discard(sail.id)
                affected.append(sail.id)
        text = (
            f"{name} parted; the {_names(ship, affected)} came down with it."
            if affected
            else f"{name} parted."
        )
    else:
        text = f"{name} parted."
    data["affected"] = affected
    ship.note("urgent", "line.parted", text, subject=line.id, data=data)


def _sails_hoisted_by(ship: Ship, halyard: Line) -> list[Sail]:
    target = ship.parts.get(halyard.of)
    if isinstance(target, Sail):
        return [target]
    if isinstance(target, Spar):
        sail = ship.sail_of(target)
        return [sail] if sail is not None else []
    return []


def _wreck_spar(ship: Ship, st: StrainState, spar: Spar, ratio: float) -> None:
    dependents = ship.dependents(spar)
    spar.wrecked = True
    spar.load_kn = 0.0
    for dep in dependents:
        dep.wrecked = True
        dep.load_kn = 0.0
        st.flogging.discard(dep.id)
        st.swung.discard(dep.id)
    st.swung.discard(spar.id)
    st.carried_away.append(spar.id)
    sails = [d.id for d in dependents if isinstance(d, Sail) and d.state in ALOFT_STATES]
    spars = [d.id for d in dependents if isinstance(d, Spar)]
    name = _name(ship, spar.id)
    where = " in the slings" if spar.is_yard else ""
    if sails and spars:
        what = f"the {_names(ship, sails)}, with the {_names(ship, spars)},"
    elif sails or spars:
        what = f"the {_names(ship, sails or spars)}"
    else:
        what = ""
    text = f"{name} carried away{where}{'; ' + what + ' hanging to leeward' if what else ''}."
    data = _data(spar, ratio)
    data["wrecked"] = [d.id for d in dependents]
    ship.note("urgent", "spar.carried_away", text, subject=spar.id, data=data)


def _blow_out(ship: Ship, st: StrainState, sail: Sail, ratio: float) -> None:
    sail.state = SailState.BLOWN_OUT
    sail.load_kn = 0.0
    st.flogging.discard(sail.id)
    st.blown_out.append(sail.id)
    text = f"{_name(ship, sail.id)} split and blew out of the bolt-ropes."
    ship.note("urgent", "sail.blown_out", text, subject=sail.id, data=_data(sail, ratio))


# ---------------------------------------------------------------------------
# Wrecks between ticks: flogging sails load their yards, swung yards follow the wind
# ---------------------------------------------------------------------------


def _tend_wrecks(ship: Ship, st: StrainState) -> None:
    for spar in ship.spars.values():
        if spar.sent_down or spar.wrecked:
            spar.load_kn = 0.0
    for sid in sorted(st.flogging):
        sail = ship.sails.get(sid)
        if sail is None or sail.wrecked or sail.state is not SailState.LOOSED:
            st.flogging.discard(sid)  # re-sheeted, taken in, or gone with its spar
            continue
        _load_flogging(ship, sail)
    for yid in sorted(st.swung):
        yard = ship.spars.get(yid)
        if yard is None or yard.wrecked or yard.sent_down:
            st.swung.discard(yid)
            continue
        _swing_yard(ship, yard)


def _load_flogging(ship: Ship, sail: Sail) -> None:
    """A sail whose sheet has parted snatches at its yard with a fifth of its
    cloth, and the load on the yard and the spars beneath is doubled."""
    aws = ship.dyn.apparent_wind_speed
    q = 0.5 * units.RHO_AIR * aws * aws
    area = FLOGGING_AREA_FRACTION * sail.area_m2
    force_kn = q * area * FLOGGING_DRAG_COEFFICIENT / 1000.0
    sail.area_effective_m2 = area
    sail.force_kn = force_kn
    for spar in ship.spar_chain(sail):
        if not (spar.wrecked or spar.sent_down):
            spar.load_kn += FLOGGING_LOAD_MULTIPLIER * force_kn


def _swing_yard(ship: Ship, yard: Spar) -> None:
    """Lay the yard along the apparent wind: its chord follows the AWA, so the
    sail on it luffs and gives no thrust."""
    awa = ship.dyn.apparent_wind_angle
    chord = min(abs(awa), math.pi - abs(awa))  # the chord's angle from the keel
    angle = min(math.pi / 2 - chord, SWUNG_YARD_MAX)
    yard.brace_angle = math.copysign(angle, awa) if awa != 0.0 else angle


# ---------------------------------------------------------------------------
# Names for the log
# ---------------------------------------------------------------------------


def _name(ship: Ship, part_id: str, capital: bool = True) -> str:
    """A sailor's name for a part: the ship file's first plain alias, else the
    id in words with the side first ('larboard main topsail brace')."""
    name = None
    for alias, target in ship.aliases.items():
        if target == part_id and not alias.startswith("the "):
            name = alias
            break
    if name is None:
        words = part_id.replace("_", " ").split(".")
        if len(words) > 1 and words[-1] in _SIDES:
            words = [words[-1], *words[:-1]]
        name = " ".join(words)
    return name[:1].upper() + name[1:] if capital else name


def _names(ship: Ship, ids: list[str]) -> str:
    names = [_name(ship, i, False) for i in ids]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
