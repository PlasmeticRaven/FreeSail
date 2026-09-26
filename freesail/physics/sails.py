"""Wind on the sails: what every set sail pushes with, and what it strains.

What this computes
------------------
Once per physics substep, `compute_sail_forces(ship, wind)` looks at every
sail aboard and works out the force the wind puts on it. The forces are added
up into what the hull physics (package 5) needs: a push along the keel
(thrust), a push sideways (which makes leeway), a heeling moment (which lays
the ship over) and a turning moment about the hull's centre of lateral
resistance (which is weather or lee helm). It also writes the result onto
each sail, and the resulting strain onto the sail's cloth, its spars and its
running rigging, for the strain system (package 9) to judge.

How a sail is worked out (spec §7.1 to §7.3)
--------------------------------------------
1. **The wind the sail feels.** The true wind is stronger aloft, so each sail
   is given the wind at its own height. The ship's own motion is subtracted
   to give the *apparent* wind: the wind a hand on that sail would feel.
2. **How much cloth is working.** The sail's area, less what is reefed, less
   what heel steals (a heeled sail presents less to the wind), less what is
   *blanketed* by another sail standing between it and the wind.
3. **Its angle to the wind.** A square sail lies along its yard, so its angle
   comes from the brace. A fore-and-aft sail lies along its sheet angle, on
   the lee side. The *angle of attack* is the angle between the apparent
   wind and the cloth: near zero the sail shakes (luffs), around 25° it pulls
   hardest, square-on it is a wall and only pushes.
4. **Lift and drag** from the class tables in `data/sail_classes.yaml`,
   times the wind pressure and the working area. Lift acts across the wind,
   drag along it. Both are resolved into the ship's own axes.
5. **Which face the wind is on.** A square sail with the wind on its fore
   face is *backed*: it pushes the ship astern, `sail.backed` is set and the
   transition is logged. A fore-and-aft sail with the wind on its lee face
   simply collapses and gives no lift (heaving to with a jib held to weather
   needs a sail state this package does not have; see the report).

Windage
-------
Furled sails, sails hanging in the gear, bare spars and wrecks all catch
wind. That is pure drag along the apparent wind. It is folded into the
thrust and side force and also reported separately in `windage_drag_n`.

Sign conventions (spec §4, docs/dev/M1-WorkPackages.md)
-----------------------------------------------------
Heading clockwise from north; thrust forward positive; side force to
starboard positive; heel and yaw moments positive to starboard; apparent
wind angle 0 dead ahead and positive when the wind is on the starboard bow.
`Spar.brace_angle` is positive for the trim used on the starboard tack (wind
from starboard): the starboard yardarm forward and the larboard yardarm aft,
so a positive brace goes with a positive apparent wind angle and the spec's
`alpha = AWA - theta` holds. (The contract's phrase "larboard yardarm
forward" for that same trim describes the other tack; see the report.)
`Sail.sheet_angle` is unsigned; the sail is always taken to lie on the lee
side.

Everything inside is SI: metres, seconds, newtons, radians. The `*_kn`
fields on parts are kilonewtons, as `parts.py` defines them.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from freesail import units
from freesail.physics.strain import baggy_luff  # package 22: the worn-canvas luff term
from freesail.ship.parts import Line, LineState, Sail, SailState, Spar

if TYPE_CHECKING:
    from freesail.physics.wind import Wind
    from freesail.ship.graph import Ship

# ---------------------------------------------------------------------------
# Constants (spec §7.3 and §7.5)
# ---------------------------------------------------------------------------

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "sail_classes.yaml"

# Fraction of a sail's force carried by each of its lines (§7.5).
SHEET_LOAD_FRACTION = 0.6
HALYARD_LOAD_FRACTION = 0.5
BRACE_LOAD_FRACTION = 0.3
STAY_LOAD_FRACTION = 1.0  # a staysail hangs its whole pull on its stay
HALYARD_CLASSES = frozenset({"halyard", "throat_halyard", "peak_halyard"})

# Blanketing (§7.3): a sail downwind of another loses this much area.
BLANKET_RUNNING = 0.30  # square sail behind square sail, running
BLANKET_OTHER = 0.15
BLANKET_RANGE_MAST_HEIGHTS = 3.0  # how far downwind the shadow reaches
RUNNING_AWA = units.deg_to_rad(150.0)  # "running": wind within 30° of dead astern

# The deck-level apparent wind is what a man on deck feels: deck plus head height.
WIND_EYE_HEIGHT_M = 1.5

# Which spar classes stack vertically (their height_m is their own length).
MAST_CLASSES = frozenset({"mast", "topmast", "topgallant_mast", "royal_mast"})
SQUARE_FAMILY = frozenset({"square", "studding"})

# A goose-winged course or topsail (package 19, spec M3 §6): the lee clew is
# hauled up and only the weather half of the sail draws (Luce 1884, ch. XXIV,
# 'Wearing in a Gale': "haul aboard the weather clew of the foresail ... A
# foresail in this state is 'goose-winged'"). Half the working area, its
# centre a quarter of the yard's length out toward the side still set.
GOOSE_WINGED_AREA_FRACTION = 0.5
GOOSE_WINGED_SHIFT = 0.25  # of the yard's length, toward the weather yardarm

# Bowlines (milestone 3b, spec 3b §4). A course or topsail whose weather bowline is
# hauled out, while its yard is braced up for that side, has its weather leech held taut
# forward: a flatter sail at the luff, which draws a few degrees nearer the wind before
# it lifts. Fincham 1843, art. 98: "the flatter the sails the sharper they may be
# braced"; Luce 1884, ch. XXIII, 'To Set a Close-Reefed Topsail': "haul taut the
# weather-brace and haul the bowline". The size of it is judgement (spec 3b §4): the
# class's lift curve is read BOWLINE_LUFF_GAIN_DEG further on at and below its luff
# angle, the shift tapering to nothing at the curve's peak, so the sail's luff angle is
# that much lower and a full sail draws as before.
BOWLINE_LUFF_GAIN_DEG = 4.0
# ... and its drag near the luff a little lower, the leech not shaking: a tenth at and
# below the luff angle, tapering likewise (judgement, spec 3b §4 "a little lower").
BOWLINE_DRAG_REDUCTION = 0.10
# A bowline cannot be kept hauled off the wind: with its yard braced in within this of
# square it is slacked (spec 3b §4, judgement; Luce 1884, ch. XXIV, 'Wearing': "Clear
# away the bo'lines! ... BRACE IN THE AFTER YARDS!").
BOWLINE_SLACK_ANGLE_DEG = 40.0
# The pull a hauled bowline takes, as a fraction of its sail's force: it holds the
# weather leech forward against a part of what the sheet and braces bear (judgement:
# well below a brace's 0.3, spec §7.5).
BOWLINE_LOAD_FRACTION = 0.1


# ---------------------------------------------------------------------------
# Sail classes: the tables
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SailClass:
    """One row of data/sail_classes.yaml, with angles in radians."""

    name: str
    alpha: tuple[float, ...]  # radians, ascending, 0..pi/2
    lift: tuple[float, ...]
    drag: tuple[float, ...]
    luff_angle: float  # radians
    reef_factor: float
    furled_windage: float
    notes: str = ""

    def coefficients(self, alpha: float, luff_gain: float = 0.0) -> tuple[float, float]:
        """(C_L, C_D) at an angle of attack in radians, folded to 0..pi/2.

        `luff_gain` (radians) is a flatter sail's: a bowline hauled (spec 3b §4). The
        lift is read that much further on at and below the luff angle, the shift
        tapering to nothing at the curve's peak, and the drag there is a little less.
        """
        a = min(max(abs(alpha), 0.0), math.pi / 2)
        c_l, c_d = _interp(self.alpha, self.lift, a), _interp(self.alpha, self.drag, a)
        peak = self.peak_alpha
        if luff_gain <= 0.0 or a >= peak:
            return c_l, c_d
        taper = 1.0 if a <= self.luff_angle else (peak - a) / (peak - self.luff_angle)
        c_l = _interp(self.alpha, self.lift, a + luff_gain * taper)
        return c_l, c_d * (1.0 - BOWLINE_DRAG_REDUCTION * taper)

    @property
    def peak_alpha(self) -> float:
        """The angle of attack at which the class's lift is greatest."""
        return self.alpha[max(range(len(self.lift)), key=lambda i: self.lift[i])]


def _interp(xs: tuple[float, ...], ys: tuple[float, ...], x: float) -> float:
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    i = bisect.bisect_right(xs, x)
    x0, x1, y0, y1 = xs[i - 1], xs[i], ys[i - 1], ys[i]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _load_tables(path: Path = DATA_PATH) -> tuple[dict[str, SailClass], dict]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    classes: dict[str, SailClass] = {}
    for name, c in raw["classes"].items():
        alpha = tuple(units.deg_to_rad(float(a)) for a in c["alpha_deg"])
        lift, drag = tuple(map(float, c["lift"])), tuple(map(float, c["drag"]))
        if not (len(alpha) == len(lift) == len(drag)) or list(alpha) != sorted(alpha):
            raise ValueError(f"{path}: class '{name}' tables are ragged or not ascending.")
        classes[name] = SailClass(
            name=name,
            alpha=alpha,
            lift=lift,
            drag=drag,
            luff_angle=units.deg_to_rad(float(c["luff_angle_deg"])),
            reef_factor=float(c["reef_factor"]),
            furled_windage=float(c["furled_windage"]),
            notes=str(c.get("notes", "")).strip(),
        )
    return classes, raw["windage"]


SAIL_CLASSES, WINDAGE = _load_tables()
WINDAGE_BY_STATE: dict[SailState, float] = {
    SailState.IN_THE_GEAR: float(WINDAGE["states"]["in_the_gear"]),
    SailState.LOOSED: float(WINDAGE["states"]["loosed"]),
    SailState.SHEETED: float(WINDAGE["states"]["sheeted"]),
    SailState.BLOWN_OUT: float(WINDAGE["states"]["blown_out"]),
}
SPAR_AREA_FACTOR = float(WINDAGE["spar_area_factor"])
SPAR_DRAG_COEFFICIENT = float(WINDAGE["spar_drag_coefficient"])
WRECK_MULTIPLIER = float(WINDAGE["wreck_multiplier"])


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass
class SailForces:
    thrust_n: float  # along the keel, forward positive
    side_n: float  # to starboard positive
    heel_moment_nm: float  # positive heels to starboard
    yaw_moment_nm: float  # about hull.spec.clr_x_m, positive turns to starboard
    windage_drag_n: float  # drag of furled sails, spars and wrecks (already in thrust/side)


@dataclass
class _Flow:
    """The apparent wind at one height, in the ship's axes (forward, starboard)."""

    speed: float  # m/s
    fwd: float  # unit vector of the air's motion relative to the ship
    stb: float
    awa: float  # radians, where the wind comes from, +ve on the starboard bow

    @property
    def q(self) -> float:
        """Dynamic pressure, N/m^2."""
        return 0.5 * units.RHO_AIR * self.speed * self.speed


# ---------------------------------------------------------------------------
# The entry point
# ---------------------------------------------------------------------------


def compute_sail_forces(ship: Ship, wind: Wind) -> SailForces:
    """Forces from every sail and everything else the wind pushes on.

    Writes each sail's `backed`, `force_kn`, `thrust_kn`, `side_force_kn`,
    `area_effective_m2`; the loads (`load_kn`) on sails, spars and lines;
    the deck-level `apparent_wind_angle` and `apparent_wind_speed` in
    `ship.dyn`; and `ship.extra["luff_angle"]`, the smallest apparent wind
    angle (radians) at which no set sail luffs.
    """
    _reset_loads(ship)
    dyn = ship.dyn
    hull = ship.hull.spec

    deck = _apparent(ship, wind, hull.deck_height_m + WIND_EYE_HEIGHT_M)
    dyn.apparent_wind_angle = deck.awa
    dyn.apparent_wind_speed = deck.speed

    heel_cos = max(math.cos(dyn.heel), 0.0)
    _tend_bowlines(ship)
    driving = [s for s in ship.sails.values() if _is_driving(ship, s)]
    flows = {s.id: _apparent(ship, wind, s.centre_height_m) for s in driving}
    blankets = _blanket_factors(ship, driving, flows)

    thrust = side = heel_m = yaw_m = windage = 0.0
    luff_angle: float | None = None
    luff_sum = 0.0
    luff_area = 0.0

    for sail in driving:
        cls = SAIL_CLASSES[sail.cls]
        flow = flows[sail.id]
        reefs = min(max(sail.reefs, 0), sail.reef_bands)
        area = sail.area_m2 * max(1.0 - cls.reef_factor * reefs, 0.0) * heel_cos * blankets[sail.id]
        if sail.state is SailState.GOOSE_WINGED:
            area *= GOOSE_WINGED_AREA_FRACTION
        chord, drive_normal = _chord(ship, sail, flow.awa)
        bowline = hauled_weather_bowline(ship, sail)
        gain = units.deg_to_rad(BOWLINE_LUFF_GAIN_DEG) if bowline is not None else 0.0
        f_fwd, f_stb, backed = _plate_force(flow, area, chord, drive_normal, cls, sail, gain)
        force = math.hypot(f_fwd, f_stb)

        _record_backed(ship, sail, backed)
        sail.area_effective_m2 = area
        sail.force_kn = force / 1000.0
        sail.thrust_kn = f_fwd / 1000.0
        sail.side_force_kn = f_stb / 1000.0
        _apply_loads(ship, sail, force / 1000.0)
        if bowline is not None:
            bowline.load_kn += BOWLINE_LOAD_FRACTION * force / 1000.0

        y = _lateral_offset(ship, sail, flow.awa)
        thrust += f_fwd
        side += f_stb
        heel_m += f_stb * sail.centre_height_m
        yaw_m += f_stb * (sail.x_m - hull.clr_x_m) - f_fwd * y

        # the ship's luff angle is the area-weighted mean of her driving sails':
        # a schooner sails by her fore-and-aft canvas with the square topsail
        # shaking, so the topsail must not set the rule for the whole rig
        sail_luff = _chord_angle(ship, sail) + cls.luff_angle - gain
        # -- package 22 (spec 3b §6.2): worn canvas is baggier and lies less close to the
        # wind; its luff angle rises by BAGGY_LUFF_DEG * (1 - condition / 100). The one
        # canvas term in this module; the constant and the rule are in physics/strain.py.
        sail_luff += baggy_luff(sail)
        # -- end package 22
        luff_weight = max(sail.area_effective_m2, 1e-6)
        luff_sum += sail_luff * luff_weight
        luff_area += luff_weight
        luff_angle = luff_sum / luff_area

    driving_ids = {s.id for s in driving}
    for sail in ship.sails.values():
        if sail.id in driving_ids:
            continue
        sail.backed = False  # a sail that is not drawing cannot be aback
        sail.area_effective_m2 = sail.force_kn = sail.thrust_kn = sail.side_force_kn = 0.0
        area = _sail_windage_area(ship, sail)
        if area > 0:
            flow = _apparent(ship, wind, sail.centre_height_m)
            d = flow.q * area
            windage += d
            thrust += d * flow.fwd
            side += d * flow.stb
            heel_m += d * flow.stb * sail.centre_height_m
            yaw_m += d * flow.stb * (sail.x_m - hull.clr_x_m)

    for spar in ship.spars.values():
        area = _spar_windage_area(spar)
        if area <= 0:
            continue
        height = _spar_centre_height(ship, spar)
        flow = _apparent(ship, wind, height)
        d = flow.q * area * SPAR_DRAG_COEFFICIENT
        windage += d
        thrust += d * flow.fwd
        side += d * flow.stb
        heel_m += d * flow.stb * height
        yaw_m += d * flow.stb * (_spar_x(ship, spar) - hull.clr_x_m)

    if luff_angle is None:
        ship.extra.pop("luff_angle", None)
    else:
        ship.extra["luff_angle"] = luff_angle

    return SailForces(
        thrust_n=thrust,
        side_n=side,
        heel_moment_nm=heel_m,
        yaw_moment_nm=yaw_m,
        windage_drag_n=windage,
    )


# ---------------------------------------------------------------------------
# The wind a sail feels
# ---------------------------------------------------------------------------


def _apparent(ship: Ship, wind: Wind, height: float) -> _Flow:
    """Apparent wind at a height above the water, in the ship's axes."""
    vx, vy = wind.vector_at_height(height)
    psi = ship.dyn.heading
    sin_h, cos_h = math.sin(psi), math.cos(psi)
    # world (x east, y north) to body (forward, starboard)
    a_fwd = vx * sin_h + vy * cos_h - ship.dyn.u
    a_stb = vx * cos_h - vy * sin_h - ship.dyn.v
    speed = math.hypot(a_fwd, a_stb)
    if speed < 1e-9:
        return _Flow(0.0, -1.0, 0.0, 0.0)
    return _Flow(speed, a_fwd / speed, a_stb / speed, math.atan2(-a_stb, -a_fwd))


# ---------------------------------------------------------------------------
# Which sails drive, and how they lie
# ---------------------------------------------------------------------------


def _chain_intact(ship: Ship, sail: Sail) -> bool:
    return not any(sp.wrecked or sp.sent_down for sp in ship.spar_chain(sail))


def _is_driving(ship: Ship, sail: Sail) -> bool:
    drawing = sail.is_set or (sail.state is SailState.GOOSE_WINGED and not sail.wrecked)
    return drawing and sail.cls in SAIL_CLASSES and _chain_intact(ship, sail)


def _trim_yard(ship: Ship, sail: Sail) -> Spar | None:
    """The yard whose brace sets this sail's angle: its own, or a stuns'l's parent yard."""
    yard = ship.yard_of(sail)
    if yard is None and sail.cls == "studding":
        boom = ship.spar_of_role(sail, "boom")
        yard = ship.parent_of(boom) if boom is not None else None
    return yard


def _chord_angle(ship: Ship, sail: Sail) -> float:
    """Unsigned angle of the sail's chord from the centreline, radians."""
    if sail.cls in SQUARE_FAMILY:
        yard = _trim_yard(ship, sail)
        brace = yard.brace_angle if yard is not None else 0.0
        return math.pi / 2 - min(abs(brace), math.pi / 2)
    return min(abs(sail.sheet_angle), math.pi / 2)


def _chord(ship: Ship, sail: Sail, awa: float) -> tuple[float, tuple[float, float]]:
    """The chord axis bearing (radians from the bow) and the 'drive normal'.

    The drive normal is the unit vector the air moves along when the sail is
    drawing as intended: forward through a square sail (wind on its after
    face), to leeward through a fore-and-aft sail (wind on its weather face).
    """
    if sail.cls in SQUARE_FAMILY:
        yard = _trim_yard(ship, sail)
        b = yard.brace_angle if yard is not None else 0.0
        # yard square: chord athwartships (pi/2); braced +b: starboard arm forward
        return math.pi / 2 - b, (math.cos(b), -math.sin(b))
    tack = 1.0 if awa >= 0 else -1.0  # sail lies on the lee side
    gamma = tack * min(abs(sail.sheet_angle), math.pi / 2)
    # normal pointing to leeward: the -tack side
    return gamma, (tack * math.sin(gamma), -tack * math.cos(gamma))


def _plate_force(
    flow: _Flow,
    area: float,
    chord: float,
    drive_normal: tuple[float, float],
    cls: SailClass,
    sail: Sail,
    luff_gain: float = 0.0,
) -> tuple[float, float, bool]:
    """Lift and drag on one sail, resolved into (forward, starboard) newtons.

    The sail is a plate along `chord`. Drag acts along the apparent wind;
    lift across it, toward the sail's lee side. Returns the force and whether
    a square sail is backed. `luff_gain` is a hauled bowline's (see
    `SailClass.coefficients`); it helps only a sail drawing on its after face.
    """
    d = (flow.fwd, flow.stb)
    c = (math.cos(chord), math.sin(chord))
    n = (-c[1], c[0])
    if n[0] * d[0] + n[1] * d[1] < 0:
        n = (-n[0], -n[1])  # the normal on the sail's lee (downstream) side
    sin_i = min(max(n[0] * d[0] + n[1] * d[1], 0.0), 1.0)
    alpha = math.asin(sin_i)
    on_drive_face = drive_normal[0] * d[0] + drive_normal[1] * d[1] >= 0.0
    c_l, c_d = cls.coefficients(alpha, luff_gain if on_drive_face else 0.0)
    backed = False
    if not on_drive_face:
        if sail.cls in SQUARE_FAMILY:
            backed = alpha > cls.luff_angle  # wind on the fore face and filling it
        else:
            c_l, c_d = 0.0, cls.coefficients(0.0)[1]  # cloth collapses and flogs
    q_a = flow.q * area
    # lift direction: perpendicular to the flow, on the lee side of the sail
    l_fwd, l_stb = n[0] - sin_i * d[0], n[1] - sin_i * d[1]
    l_len = math.hypot(l_fwd, l_stb)
    if l_len > 1e-9:
        l_fwd, l_stb = l_fwd / l_len, l_stb / l_len
    else:
        l_fwd = l_stb = 0.0
    f_fwd = q_a * (c_d * d[0] + c_l * l_fwd)
    f_stb = q_a * (c_d * d[1] + c_l * l_stb)
    return f_fwd, f_stb, backed


# ---------------------------------------------------------------------------
# Bowlines (spec 3b §4)
# ---------------------------------------------------------------------------


def _bowlines(ship: Ship) -> tuple[Line, ...]:
    """Every bowline aboard, in the ship file's order (kept, since lines are fixed)."""
    cached = ship.extra.get("sails.bowlines")
    if not isinstance(cached, tuple):
        cached = tuple(ln for ln in ship.lines.values() if ln.cls == "bowline")
        ship.extra["sails.bowlines"] = cached
    return cached


def hauled_weather_bowline(ship: Ship, sail: Sail) -> Line | None:
    """The bowline doing its work on this sail, or None: hauled out, on the side the
    sail's yard is braced up for, with the yard braced up at least
    BOWLINE_SLACK_ANGLE_DEG from square. A hauled lee bowline holds nothing."""
    if not ship.lines_of(sail, "bowline"):
        return None
    yard = ship.yard_of(sail)
    if yard is None or abs(yard.brace_angle) < units.deg_to_rad(BOWLINE_SLACK_ANGLE_DEG):
        return None
    side = "starboard" if yard.brace_angle > 0 else "larboard"
    line = ship.line_of(sail, "bowline", side)
    return line if line is not None and line.bowline_hauled else None


def _tend_bowlines(ship: Ship) -> None:
    """Slack a hauled bowline whose sail is no longer drawing, or whose yard has been
    braced in within BOWLINE_SLACK_ANGLE_DEG of square: it will not stand off the
    wind. The second is logged; a sail taken in overhauls its bowline with the rest
    of its gear."""
    slack_at = units.deg_to_rad(BOWLINE_SLACK_ANGLE_DEG)
    for line in _bowlines(ship):
        if not line.bowline_hauled:
            continue
        sail = ship.parts.get(line.of)
        if not isinstance(sail, Sail):
            continue
        yard = ship.yard_of(sail)
        drawing = _is_driving(ship, sail)
        braced_in = yard is not None and abs(yard.brace_angle) < slack_at
        if drawing and not braced_in:
            continue
        line.state = LineState.FREE
        line.hauled = 0.0
        if drawing and yard is not None:
            from freesail.evolutions.runner import part_name  # local import, as scripts.py does

            ship.note(
                "routine",
                "line.slacked",
                f"Let go the {part_name(ship, line.id)} as the {part_name(ship, yard.id)} "
                "came in; a bowline will not stand off the wind.",
                subject=line.id,
            )


def _record_backed(ship: Ship, sail: Sail, backed: bool) -> None:
    if backed == sail.backed:
        return
    sail.backed = backed
    name = _name(sail.id)
    if backed:
        ship.note("notable", "sail.backed", f"{name} taken aback.", subject=sail.id)
    else:
        ship.note("routine", "sail.filled", f"{name} filled again.", subject=sail.id)


def _name(part_id: str) -> str:
    text = part_id.replace(".", " ").replace("_", " ")
    return text[:1].upper() + text[1:]


# ---------------------------------------------------------------------------
# Where a sail is, for blanketing and for the yaw of one-sided sails
# ---------------------------------------------------------------------------


def _lateral_offset(ship: Ship, sail: Sail, awa: float) -> float:
    """Metres to starboard of the centreline of the sail's centre of effort."""
    if sail.state is SailState.GOOSE_WINGED:
        # the weather clew is the one left set: the centre moves out to windward
        yard = _trim_yard(ship, sail)
        reach = GOOSE_WINGED_SHIFT * (yard.length_m if yard is not None else 0.0)
        return reach if awa >= 0 else -reach
    if sail.cls == "studding":
        boom = ship.spar_of_role(sail, "boom")
        yard = _trim_yard(ship, sail)
        reach = (yard.length_m / 2 if yard else 0.0) + (boom.length_m / 2 if boom else 0.0)
        return reach if sail.side == "starboard" else -reach
    if sail.is_fore_and_aft:
        spar = ship.spar_of_role(sail, "boom") or ship.spar_of_role(sail, "gaff")
        foot = (
            spar.length_m
            if spar is not None and spar.length_m > 0
            else 0.8 * math.sqrt(sail.area_m2)
        )
        lee = -1.0 if awa >= 0 else 1.0
        return lee * 0.5 * foot * math.sin(min(abs(sail.sheet_angle), math.pi / 2))
    return 0.0


def _sail_height(ship: Ship, sail: Sail) -> float:
    """A rough height of the cloth, metres, for the blanketing shadow."""
    if sail.cls in SQUARE_FAMILY:
        yard = _trim_yard(ship, sail)
        if yard is not None and yard.length_m > 0:
            return max(sail.area_m2 / yard.length_m, 3.0)
    return 1.2 * math.sqrt(sail.area_m2)


def _blanket_factors(ship: Ship, driving: list[Sail], flows: dict[str, _Flow]) -> dict[str, float]:
    """Area factor per sail after blanketing by sails to windward of it (§7.3).

    A sail is blanketed when another set sail lies upwind of it along the
    apparent wind, within three mast-heights, within half that sail's height
    across the wind, and overlapping it in height. The largest single
    shadow applies; shadows do not stack.
    """
    mast_height = max((s.height_m for s in ship.spars.values() if s.cls == "mast"), default=20.0)
    reach = BLANKET_RANGE_MAST_HEIGHTS * mast_height
    pos = {
        s.id: (s.x_m, _lateral_offset(ship, s, flows[s.id].awa), s.centre_height_m) for s in driving
    }
    height = {s.id: _sail_height(ship, s) for s in driving}
    out: dict[str, float] = {}
    for b in driving:
        flow = flows[b.id]
        xb, yb, zb = pos[b.id]
        shadow = 0.0
        for a in driving:
            if a is b:
                continue
            xa, ya, za = pos[a.id]
            dx, dy = xb - xa, yb - ya
            along = dx * flow.fwd + dy * flow.stb  # positive: b is downwind of a
            across = abs(-dx * flow.stb + dy * flow.fwd)
            if not (0.0 < along <= reach):
                continue
            if across > 0.5 * height[a.id]:
                continue
            if abs(za - zb) > 0.5 * (height[a.id] + height[b.id]):
                continue
            running = (
                a.cls in SQUARE_FAMILY and b.cls in SQUARE_FAMILY and abs(flow.awa) >= RUNNING_AWA
            )
            shadow = max(shadow, BLANKET_RUNNING if running else BLANKET_OTHER)
        out[b.id] = 1.0 - shadow
    return out


# ---------------------------------------------------------------------------
# Strain (§7.5): who carries the sail's pull
# ---------------------------------------------------------------------------


def _reset_loads(ship: Ship) -> None:
    for part in ship.parts.values():
        part.load_kn = 0.0


def _apply_loads(ship: Ship, sail: Sail, force_kn: float) -> None:
    """Put a sail's pull on its cloth, its spars and its running rigging."""
    sail.load_kn = force_kn
    chain = ship.spar_chain(sail)
    for spar in chain:  # each spar carries everything above it
        spar.load_kn += force_kn
    if (
        sail.cls == "studding"
    ):  # the graph's chain starts at the parent yard; the boom carries it too
        boom = ship.spar_of_role(sail, "boom")
        if boom is not None and boom not in chain:
            boom.load_kn += force_kn
    for ln in ship.sheets_of(sail):
        ln.load_kn += SHEET_LOAD_FRACTION * force_kn
    halyards = [ln for ln in ship.lines_of(sail) if ln.cls in HALYARD_CLASSES]
    if chain:
        halyards += [ln for ln in ship.lines_of(chain[0]) if ln.cls in HALYARD_CLASSES]
    for ln in halyards:
        ln.load_kn += HALYARD_LOAD_FRACTION * force_kn
    yard = ship.yard_of(sail)
    if yard is not None:
        for ln in ship.braces_of(yard):
            ln.load_kn += BRACE_LOAD_FRACTION * force_kn
    stay = sail.roles.get("stay")
    if stay in ship.lines:
        ship.lines[stay].load_kn += STAY_LOAD_FRACTION * force_kn


# ---------------------------------------------------------------------------
# Windage: what the wind pushes on that is not drawing
# ---------------------------------------------------------------------------


def _sail_windage_area(ship: Ship, sail: Sail) -> float:
    cls = SAIL_CLASSES.get(sail.cls)
    if cls is None:
        return 0.0
    wrecked = sail.wrecked or any(sp.wrecked for sp in ship.spar_chain(sail))
    if wrecked:
        return sail.area_m2 * cls.furled_windage * WRECK_MULTIPLIER
    if sail.state is SailState.FURLED:
        return sail.area_m2 * cls.furled_windage
    if sail.state in (SailState.SET, SailState.GOOSE_WINGED):
        # set on a spar that is sent down: as good as furled
        return sail.area_m2 * cls.furled_windage
    return sail.area_m2 * WINDAGE_BY_STATE.get(sail.state, 0.0)


def _spar_windage_area(spar: Spar) -> float:
    if spar.sent_down:
        return 0.0
    length = spar.length_m if spar.length_m > 0 else spar.height_m
    area = SPAR_AREA_FACTOR * length * length
    return area * WRECK_MULTIPLIER if spar.wrecked else area


def _spar_centre_height(ship: Ship, spar: Spar) -> float:
    """Height above the water of the middle of a spar."""
    deck = ship.hull.spec.deck_height_m
    if spar.cls in MAST_CLASSES:
        base = sum(p.height_m for p in ship.spar_chain(spar)[1:] if p.cls in MAST_CLASSES)
        return deck + base + spar.height_m / 2
    return deck + spar.height_m


def _spar_x(ship: Ship, spar: Spar) -> float:
    if spar.parent is None:
        return spar.x_m
    root = ship.mast_of(spar)
    return root.x_m if root is not None else spar.x_m
