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

Canvas wears (milestone 3b, spec 3b §6.2)
-----------------------------------------
A sail's `condition` also falls with use, whatever the strain: by
`CLOTH_WEAR_PER_HOUR_SET` points an hour while it is set and drawing, three
times that while it flogs (sheet parted) or is aback, and not at all while
it is furled, hanging in its gear or in the sail room. A studding sail set
with the wind forward of Luce's angle (spec 3b §7) shivers in its gear and
counts as flogging: it wears at the flogging rate, and `physics/sails.py`
puts its snatching on its yard and boom with this module's flogging
constants, so its boom strains and, kept so, carries away. A sail is judged
against its *effective* cloth rating, `cloth * (0.4 + 0.6 * condition /
100)` (`Sail.effective_cloth_rating_kn`), so a worn sail strains, wears and
blows out (at `BLOW_OUT_RATIO` of what it bears now) before a new one would:
the same squall that a new sail rides out blows an old one out of the
bolt-ropes. A worn sail is also baggier and lies less close to the wind:
`baggy_luff(sail)` is added to its luff angle where the sail forces are
computed. Nothing mends canvas in milestone 3b.

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
from freesail.ship.parts import Line, LineState, Part, Sail, SailState, Spar, sync_catharpins

# ---------------------------------------------------------------------------
# The rule (spec §7.5)
# ---------------------------------------------------------------------------

DECAY_POINTS_PER_MINUTE = 2.0  # condition lost per minute per unit of ratio above 1.0
DECAY_RATIO = 1.0  # above this the part wears and the log is warned
CARRY_AWAY_RATIO = 1.5  # above this the part may carry away at any substep
CARRY_AWAY_COEFFICIENT = 0.002  # p per substep = this * (ratio - CARRY_AWAY_RATIO)^2
BLOW_OUT_RATIO = 1.8  # a set sail blows out for certain above this of its effective rating
WARNING_INTERVAL_S = 600.0  # one strain.warning per part per ten minutes
SUBSTEP_S = 0.25  # the physics substep (spec §3.1); the probability is per substep

# A flogging sail (sheet parted): a fifth of the cloth works, as a flat plate,
# and the snatching doubles the load it puts on its yard.
FLOGGING_AREA_FRACTION = 0.2
FLOGGING_DRAG_COEFFICIENT = 1.2
FLOGGING_LOAD_MULTIPLIER = 2.0

# A yard whose brace has parted swings to lie along the apparent wind, until
# it fouls the lee rigging at this angle from square. A lower yard whose mast has
# its catharpins swiftered in swings the catharpins' gain further before it fouls
# the shrouds drawn in (milestone 3b: every reader of the rigging's limit).
SWUNG_YARD_MAX = units.deg_to_rad(80.0)

# Canvas wear with use. Points of condition (0..100) an hour while a sail is set and
# drawing (spec 3b §6.2, a judgement there): 1.2 points a day set day and night, so a sail
# never taken in would be worn out in about twelve weeks; the sailmaker's mending that
# kept real canvas going longer is milestone 8.
CLOTH_WEAR_PER_HOUR_SET = 0.05
# A sail flogging (its sheet parted) or aback wears this many times faster (spec 3b §6.2).
CLOTH_WEAR_FLOGGING_FACTOR = 3.0
# A worn sail is baggier: its luff angle rises by this many degrees times (1 - condition /
# 100), six degrees for a sail worn out (spec 3b §6.2; Fincham 1843 art. 98, "the flatter
# the sails the sharper they may be braced").
BAGGY_LUFF_DEG = 6.0
# The catharpins swiftered in (milestone 3b, spec 3b §3): the lower shrouds drawn in
# below the top stay the mast less well athwartships, so its rating against the
# athwartships part of its load falls by this factor until they are eased. The
# direction is Lever's and Fincham's (the shrouds bowsed in toward the mast, art. 102
# note: "the shrouds ... will seldom allow the yards ... to be braced sufficiently
# sharp"); the figure is judgement, the gate's to judge. The fore-and-aft part of the
# load (stays and backstays) is judged against the rating as before, so a mast pressed
# on a wind, whose load is nearly all athwartships, is judged about a sixth harder,
# and one running before it hardly at all.
CATHARPIN_RATING_FACTOR = 0.85

HALYARD_CLASSES = frozenset({"halyard", "throat_halyard", "peak_halyard"})
_DRAWING = frozenset({SailState.SET, SailState.GOOSE_WINGED})
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
    _tend_catharpins(ship)
    _tend_wrecks(ship, st)
    _wear_canvas(ship, st, dt)
    # the seaway (spec M5 §4, `physics.motion`): the ship's motion is an extra load on
    # spars and gear, a factor on the wind's load by the roll and the pitch; exactly 1.0
    # without a sea or in a smooth one, so the truths measured so do not move
    motion = ship.extra.get("motion")
    seaway = motion.load_factor if motion is not None else 1.0
    warnings: list[_Warning] = []
    for part, kind in _parts_by_kind(ship):  # insertion order: deterministic
        # `_out_of_action`, with each part's class looked up once per ship (package 29's
        # profile: three hundred parts a tick)
        if (
            part.wrecked
            or (kind is Spar and part.sent_down)
            or (kind is Line and part.state is LineState.PARTED)
            or (kind is Sail and part.state not in _DRAWING)
        ):
            part.load_kn = 0.0
            continue
        if part.load_kn <= 0.0:
            continue  # a ratio of nothing (every `strain_ratio` is load over a rating)
        if seaway != 1.0 and kind is not Sail:
            part.load_kn *= seaway  # the jerk of the masts on the spars and their gear
        ratio = part.strain_ratio
        if ratio <= DECAY_RATIO:
            continue
        part.condition = max(
            0.0, part.condition - DECAY_POINTS_PER_MINUTE * (ratio - DECAY_RATIO) * dt / 60.0
        )
        if _fails(part, ratio, dt, stream):
            _carry_away(ship, st, part, ratio)
        else:
            _warn(ship, st, part, ratio, warnings)
    _log_warnings(ship, warnings)


def cloth_wear_per_hour(ship: Ship, sail: Sail, st: StrainState | None = None) -> float:
    """Points of condition this sail loses an hour by use alone (spec 3b §6.2): three times
    CLOTH_WEAR_PER_HOUR_SET while it flogs or is aback, CLOTH_WEAR_PER_HOUR_SET while it is
    set and drawing, nothing while it is furled, in its gear, unbent or wrecked."""
    if sail.wrecked:
        return 0.0
    st = st if st is not None else strain_state(ship)
    if sail.id in st.flogging and sail.state is SailState.LOOSED:
        return CLOTH_WEAR_PER_HOUR_SET * CLOTH_WEAR_FLOGGING_FACTOR
    if sail.state not in _DRAWING:
        return 0.0
    if any(sp.wrecked or sp.sent_down for sp in ship.spar_chain(sail)):
        return 0.0  # set on a spar that is down: as good as furled
    if sail.backed or sail.shivering:
        # aback, or a studding sail shaking in its gear with the wind too far forward: it
        # flogs as a sail with its sheet parted does (spec 3b §7; physics/sails.py)
        return CLOTH_WEAR_PER_HOUR_SET * CLOTH_WEAR_FLOGGING_FACTOR
    return CLOTH_WEAR_PER_HOUR_SET


def baggy_luff(sail: Sail) -> float:
    """Radians a worn sail's luff angle rises by (spec 3b §6.2): BAGGY_LUFF_DEG times the
    share of its condition it has lost; nothing for a new sail."""
    lost = 1.0 - min(max(sail.condition, 0.0), 100.0) / 100.0
    return units.deg_to_rad(BAGGY_LUFF_DEG * lost)


def _wear_canvas(ship: Ship, st: StrainState, dt: float) -> None:
    """Wear every sail by its use this tick. Only use: the strain decay above the rating is
    applied with every other part's in `apply_strain`."""
    for sail in ship.sails.values():
        rate = cloth_wear_per_hour(ship, sail, st)
        if rate > 0.0:
            sail.condition = max(0.0, sail.condition - rate * dt / 3600.0)


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


def _parts_by_kind(ship: Ship) -> tuple[tuple[Part, type | None], ...]:
    """Every part in the ship's order with the class `_out_of_action` tests it as (Spar,
    Line, Sail, or None): the parts are fixed once the ship is loaded, so this is kept."""
    kinds = ship.extra.get("strain.parts_by_kind")
    if not isinstance(kinds, tuple):
        kinds = tuple(
            (part, next((k for k in (Spar, Line, Sail) if isinstance(part, k)), None))
            for part in ship.parts.values()
        )
        ship.extra["strain.parts_by_kind"] = kinds
    return kinds


def _fails(part: Part, ratio: float, dt: float, stream: random.Random | None) -> bool:
    if part.condition <= 0.0:
        return True
    if isinstance(part, Sail) and ratio > BLOW_OUT_RATIO:
        return True
    if stream is None or ratio <= CARRY_AWAY_RATIO:
        return False
    return stream.random() < failure_probability(ratio, dt)


@dataclass
class _Warning:
    """One part's warning this tick: its words for one part and for several, so that the
    parts that strain the same way on the same tick are logged as one line."""

    part: Part
    ratio: float
    one: str  # the words after the part's name, for it alone
    many: str | None  # the same for several; None: this warning is never grouped


def _warn(
    ship: Ship, st: StrainState, part: Part, ratio: float, out: list[_Warning] | None = None
) -> None:
    last = st.last_warning_s.get(part.id)
    if last is not None and st.elapsed_s - last < WARNING_INTERVAL_S:
        return
    st.last_warning_s[part.id] = st.elapsed_s
    dire = ratio > CARRY_AWAY_RATIO
    many: str | None
    if isinstance(part, Spar):
        if dire:
            one = "bending like a whip; she will carry it away if sail is not shortened."
            many = "bending like whips; she will carry them away if sail is not shortened."
        else:
            one = many = "working under the press of sail."
        if part.swiftered_in:
            one, many = (
                one[:-1] + ", the catharpins swiftered in.",
                many[:-1] + (", the catharpins swiftered in."),
            )
        shaking = [
            s
            for s in ship.sails.values()
            if s.shivering and s.roles.get("boom") == part.id and part.cls == "studdingsail_boom"
        ]
        if shaking:  # the log says why (spec 3b §7)
            one = f"whipping as the {_name(ship, shaking[0].id, False)} flogs; " + (
                "she will carry it away." if dire else "she is too near the wind for it."
            )
            many = None
    elif isinstance(part, Line):
        if dire:
            one = "stranding; it will not hold much longer."
            many = "stranding; they will not hold much longer."
        else:
            one = many = "bar-taut and surging on the pin."
    else:
        if dire:
            one = "stretched drum-tight; it will not stand much more."
            many = "stretched drum-tight; they will not stand much more."
        else:
            one = many = "straining at the bolt-ropes."
    warning = _Warning(part, ratio, one, many)
    if out is None:
        _log_warnings(ship, [warning])
    else:
        out.append(warning)


def _log_warnings(ship: Ship, warnings: list[_Warning]) -> None:
    """The tick's warnings in the log: the parts that strain the same way on the same tick
    in one line ("The fore, main and mizzen royal masts and yards bending like whips; ..."),
    each alone as ever (package 29b, playtest 7's finding 6: a gust logged six identical
    lines, one for each royal mast and yard). A grouped line's subject is its first part and
    its data the worst part's, with every part and its ratio under `parts` and `ratios`."""
    groups: dict[tuple[str, str], list[_Warning]] = {}
    order: list[tuple[str, str]] = []
    for w in warnings:
        key = (type(w.part).__name__, w.many if w.many is not None else f"#{w.part.id}")
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(w)
    for key in order:
        group = groups[key]
        if len(group) == 1:
            w = group[0]
            text = f"{_name(ship, w.part.id)} {w.one}"
            ship.note(
                "notable", "strain.warning", text, subject=w.part.id, data=_data(w.part, w.ratio)
            )
            continue
        worst = max(group, key=lambda w: w.ratio)
        names = _group_names(ship, [w.part.id for w in group])
        text = f"{names[:1].upper()}{names[1:]} {group[0].many}"
        data = _data(worst.part, worst.ratio)
        data["parts"] = [w.part.id for w in group]
        data["ratios"] = {w.part.id: w.ratio for w in group}
        ship.note("notable", "strain.warning", text, subject=group[0].part.id, data=data)


_MAST_WORDS = ("fore", "main", "mizzen")


def _group_names(ship: Ship, ids: list[str]) -> str:
    """'the fore, main and mizzen royal masts and yards', from the parts' own names: the
    parts that differ only by their mast are named once with the masts before them, and
    those that share the masts and all but their last word are joined on it."""
    by_rest: dict[str, list[str]] = {}
    alone: list[str] = []
    for pid in ids:
        name = _name(ship, pid, False)
        first, _, rest = name.partition(" ")
        if first in _MAST_WORDS and rest:
            by_rest.setdefault(rest, []).append(first)
        else:
            alone.append(name)
    # the rests that share the same masts, together
    by_masts: dict[tuple[str, ...], list[str]] = {}
    for rest, masts in by_rest.items():
        by_masts.setdefault(tuple(masts), []).append(rest)
    phrases: list[str] = []
    for masts, rests in by_masts.items():
        plural = len(masts) > 1
        heads = {r.rsplit(" ", 1)[0] if " " in r else "" for r in rests}
        if len(rests) > 1 and len(heads) == 1 and "" not in heads:
            head = heads.pop()
            lasts = [r.rsplit(" ", 1)[1] + ("s" if plural else "") for r in rests]
            what = f"{head} {_and(lasts)}"
        else:
            what = _and([r + ("s" if plural else "") for r in rests])
        phrases.append(f"the {_and(list(masts))} {what}")
    phrases += [f"the {n}" for n in alone]
    return _and(phrases)


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _data(part: Part, ratio: float) -> dict[str, Any]:
    data = {
        "ratio": ratio,
        "load_kn": part.load_kn,
        "rating_kn": part.rating_kn,
        "condition": part.condition,
    }
    if isinstance(part, Sail):  # what the cloth bears at its condition (spec 3b §6.2)
        data["effective_rating_kn"] = part.effective_cloth_rating_kn
    factor = getattr(part, "rating_factor", 1.0)
    if factor != 1.0:
        data["rating_factor"] = factor  # the catharpins swiftered in (spec 3b §3)
    return data


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
    elif line.cls == "bowline" and isinstance(target, Sail):
        # it holds nothing now (parts.Line.bowline_hauled): the leech lifts (spec 3b §4)
        text = f"{name} parted; the {_name(ship, target.id, False)} lifting at the weather leech."
    else:
        text = f"{name} parted."
    data["affected"] = affected
    ship.note("urgent", "line.parted", text, subject=line.id, data=data)


def _sails_hoisted_by(ship: Ship, halyard: Line) -> list[Sail]:
    target = ship.parts.get(halyard.of)
    if isinstance(target, Sail):
        return [target]
    if isinstance(target, Spar):
        # every sail bent to the yard or gaff, not only the first the graph lists: a storm
        # trysail shares the main gaff with the mainsail it is bent in place of (spec 3b
        # §6.4). The studding sails that name the yard hang from their own halyards.
        return [
            s
            for s in ship.sails.values()
            if s.cls != "studding"
            and target.id in (s.roles.get(r) for r in ("yard", "gaff", "sprit", "boom"))
        ]
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


def _tend_catharpins(ship: Ship) -> None:
    """Keep the lower yards' limits with their masts' catharpins, and rate each lower
    mast for them: `rating_factor` is 1.0 as rigged; swiftered in, the athwartships
    part of the mast's load is judged against CATHARPIN_RATING_FACTOR of its rating."""
    for yard, was in sync_catharpins(ship):
        ship.note(
            "routine",
            "yard.braced",
            f"{_name(ship, yard.id)} came in to {abs(units.rad_to_deg(yard.brace_angle)):.0f}° "
            f"from {abs(units.rad_to_deg(was)):.0f}° as the lower shrouds went out.",
            subject=yard.id,
        )
    for mast in ship.spars.values():
        if mast.cls != "mast":
            continue
        if not mast.swiftered_in:
            mast.rating_factor = 1.0
            continue
        athwart = total = 0.0
        for sail in ship.sails.values():
            if sail.force_kn > 0.0 and ship.mast_of(sail) is mast:
                athwart += abs(sail.side_force_kn)
                total += sail.force_kn
        s = min(athwart / total, 1.0) if total > 0.0 else 1.0
        c2 = 1.0 - s * s
        mast.rating_factor = 1.0 / math.sqrt(c2 + (s / CATHARPIN_RATING_FACTOR) ** 2)


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
    # the catharpins' gain on a lower yard, if its mast has them swiftered in
    gain = max(yard.brace_limit - yard.rigged_brace_limit, 0.0)
    angle = min(math.pi / 2 - chord, SWUNG_YARD_MAX + gain)
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
