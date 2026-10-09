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
   simply collapses and gives no lift, unless its sheet holds it there.

The sheet holds the trim (package 32e, spec M5 open item 13)
------------------------------------------------------------
A fore-and-aft sail lies where its sheets hold it (`evolutions.trim.read_sheet`): on
the side whose sheet is hauled and belayed, at the angle the sheet's length gives
through the boom's or the clew's geometry. Held on the weather side (the jib sheet to
windward, the spanker boom hauled over to windward) it stands aback by its sheet: a
plate with the wind on its outer face, its force to leeward, which is what boxes a bow
off and what a fore-and-after heaves to by (Luce 1884, ch. XXXIV, 'Sloops', 'To Heave
to'). With every sheet let fly it flogs: no lift, a loose sail's windage, and the
snatching that the studding sails' stall puts on its spars. The working sheet carries
the sail's pull: a boomed sail's by the lever the sheet holds the boom by, a
loose-footed sail's a fraction of the pull. `Sail.sheet_angle` is refreshed here from
the sheet each time the rig is read; nothing sets it on its own.

Studding sails and the wind (milestone 3b, spec 3b §7)
------------------------------------------------------
A studding sail draws on its yard's brace like the sail beside it, but only with
the wind free: forward of Luce's angle for its level (the studding class's stall
in `data/sail_classes.yaml`, counted off the bow as the known truths count points
of sail) its lift falls away over a point, it shakes in its gear with a loose
sail's windage, and it flogs as the strain model counts flogging: worn at the
flogging rate, its snatching doubled on its yard and its boom (`_apply_shaking`),
so the boom strains and, kept so, carries away. Nothing refuses it. A studding
sail with no side (the ringtail, the water sail) lies in its gaff sail's plane on
the lee side, at that sail's sheet angle.

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
import functools
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from freesail import units
from freesail.evolutions import trim as yard_trim
from freesail.physics.strain import (  # package 22: the worn-canvas luff term
    FLOGGING_DRAG_COEFFICIENT,
    FLOGGING_LOAD_MULTIPLIER,
    baggy_luff,
)
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
    # The stall (milestone 3b, the studding class only): the wind's angle off the bow
    # (radians, by level: "lower", "upper") forward of which the sail shivers, and the band
    # over which its lift falls to nothing. Empty for a class that has none.
    stall_wind: dict[str, float] = field(default_factory=dict)
    stall_band: float = 0.0

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

    @functools.cached_property
    def peak_alpha(self) -> float:
        """The angle of attack at which the class's lift is greatest (kept: the tables
        are fixed once loaded, and it is read for every drawing sail every substep)."""
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
        stall = c.get("stall") or {}
        classes[name] = SailClass(
            name=name,
            alpha=alpha,
            lift=lift,
            drag=drag,
            luff_angle=units.deg_to_rad(float(c["luff_angle_deg"])),
            reef_factor=float(c["reef_factor"]),
            furled_windage=float(c["furled_windage"]),
            notes=str(c.get("notes", "")).strip(),
            stall_wind={
                level: units.deg_to_rad(float(deg))
                for level, deg in (stall.get("wind_deg") or {}).items()
            },
            stall_band=units.deg_to_rad(float(stall.get("band_deg", 0.0))),
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

# Studding sails and the wind (milestone 3b, spec 3b §7): the studding class's stall, as
# data/sail_classes.yaml gives it, with Luce's angles cited there. Degrees off the bow of
# the true wind, by level: "lower" for the lower studding sails and the sails that take
# their figure (the ringtail, the water sail, the save-alls), "upper" for the topmast and
# topgallant studding sails.
STUDDING_MIN_WIND_DEG = {
    level: units.rad_to_deg(a) for level, a in SAIL_CLASSES["studding"].stall_wind.items()
}
STUDDING_STALL_BAND_DEG = units.rad_to_deg(SAIL_CLASSES["studding"].stall_band)
# A shivering studding sail flogs as the strain model's parted-sheet sail does (strain.py,
# FLOGGING_DRAG_COEFFICIENT and FLOGGING_LOAD_MULTIPLIER: the cloth's drag, doubled by the
# snatching, on its yard and the spars beneath), but with all its cloth: held at its head,
# tack and sheet, the whole sail shakes in its gear, where a sail whose sheet has parted
# streams from its yard with a fifth of its cloth working (FLOGGING_AREA_FRACTION). Every
# snatch comes on the boom end through the tack. Judgement: the figure that makes a boom
# rated for its drawing sail in 18 knots (tools/gen_ships.py) strain when its sail shakes
# in a moderate breeze, as studding sail booms were sprung when a ship came up with them
# set (spec 3b §7).
SHIVERING_AREA_FRACTION = 1.0
# The flag and the log line do not flicker at the limit: a shivering sail is logged drawing
# again only when the wind is this far abaft its limit (judgement: the helmsman's yaw).
SHIVERING_HYSTERESIS_DEG = 1.0


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


# A sail's "taken aback" and "filled again" are recorded when the physics has read it
# so for this long: in a seaway the wind on a sail set near the eye, hove to, crosses its
# face with every pitch, and the lines came at every roll (package 33a's finding, package
# 32e). Ten seconds, longer than a hull's pitching period (the frigate's about eight,
# spec M5 §4): judgement. Read without a `dt` (the tests' direct calls) it records at once.
BACKED_DWELL_S = 10.0


def compute_sail_forces(ship: Ship, wind: Wind, dt: float = 0.0) -> SailForces:
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
    field = _FlowField(ship, wind)

    deck = field.at(hull.deck_height_m + WIND_EYE_HEIGHT_M)
    dyn.apparent_wind_angle = deck.awa
    dyn.apparent_wind_speed = deck.speed

    heel_cos = max(math.cos(dyn.heel), 0.0)
    _tend_bowlines(ship)
    true_off = true_wind_off_bow(ship, wind)
    rig = _rig(ship)
    driving = rig.driving
    flows = {s.id: field.at(s.centre_height_m) for s in driving}
    blankets, offsets = _blanket_factors_and_offsets(ship, rig, flows)

    thrust = side = heel_m = yaw_m = windage = 0.0
    luff_angle: float | None = None
    luff_sum = 0.0
    luff_area = 0.0

    for d in rig.drawing:
        sail = d.sail
        cls = d.cls
        flow = flows[sail.id]
        area = d.area * heel_cos * blankets[sail.id]
        if d.goose_winged:
            area *= GOOSE_WINGED_AREA_FRACTION
        if d.square_chord is not None:
            chord, drive_normal = d.square_chord
        elif d.side_sign != 0.0:
            # a fore-and-aft sail lies on the side its sheet holds it (package 32e)
            chord, drive_normal = _chord_on_lee(d.chord_angle, -d.side_sign)
        else:
            chord, drive_normal = _chord_on_lee(d.chord_angle, flow.awa)
        bowline = hauled_weather_bowline(ship, sail) if d.has_bowlines else None
        gain = units.deg_to_rad(BOWLINE_LUFF_GAIN_DEG) if bowline is not None else 0.0
        f_fwd, f_stb, backed = _plate_force(
            flow,
            area,
            chord,
            drive_normal,
            cls,
            sail,
            gain,
            square_faced=d.square_faced,
            held=d.held,
        )
        # the studding sails' stall (spec 3b §7): forward of Luce's angle the sail shakes in
        # its gear; its lift falls away over a point and it flogs, a loose sail's windage.
        # A fore-and-aft sail with every sheet let fly flogs the same way (package 32e).
        stall = studding_stall(ship, sail, true_off) if d.studding else 0.0
        if d.flogging:
            stall = 1.0
        if stall > 0.0:
            shake = WINDAGE_BY_STATE[SailState.LOOSED] * area * flow.q
            f_fwd = (1.0 - stall) * f_fwd + stall * shake * flow.fwd
            f_stb = (1.0 - stall) * f_stb + stall * shake * flow.stb
            backed = False  # shaking, not aback
        force = math.hypot(f_fwd, f_stb)

        _record_backed(ship, sail, backed, dt)
        if d.studding:
            _record_shivering(ship, sail, stall, true_off)
        elif d.side_sign != 0.0:
            sail.shivering = d.flogging  # its sheet let fly: it flogs (the order said so)
        sail.area_effective_m2 = area
        sail.force_kn = force / 1000.0
        sail.thrust_kn = f_fwd / 1000.0
        sail.side_force_kn = f_stb / 1000.0
        _apply_loads(ship, sail, force / 1000.0, d)
        if stall > 0.0:
            _apply_shaking(ship, sail, stall * flow.q * area * SHIVERING_AREA_FRACTION)
        if bowline is not None:
            bowline.load_kn += BOWLINE_LOAD_FRACTION * force / 1000.0

        y = offsets[sail.id]
        thrust += f_fwd
        side += f_stb
        heel_m += f_stb * sail.centre_height_m
        yaw_m += f_stb * (sail.x_m - hull.clr_x_m) - f_fwd * y

        # the ship's luff angle is the area-weighted mean of her driving sails':
        # a schooner sails by her fore-and-aft canvas with the square topsail
        # shaking, so the topsail must not set the rule for the whole rig
        sail_luff = d.chord_angle + cls.luff_angle - gain
        # -- package 22 (spec 3b §6.2): worn canvas is baggier and lies less close to the
        # wind; its luff angle rises by BAGGY_LUFF_DEG * (1 - condition / 100). The one
        # canvas term in this module; the constant and the rule are in physics/strain.py.
        sail_luff += d.baggy_luff
        # -- end package 22
        luff_weight = max(sail.area_effective_m2, 1e-6)
        luff_sum += sail_luff * luff_weight
        luff_area += luff_weight
        luff_angle = luff_sum / luff_area

    for sail in rig.idle:
        sail.backed = False  # a sail that is not drawing cannot be aback
        sail.shivering = False  # nor shake in its gear
        sail.area_effective_m2 = sail.force_kn = sail.thrust_kn = sail.side_force_kn = 0.0
    terms = field.drag_terms(rig.windage_heights)
    for area, height, lever, i in rig.idle_windage:
        q, fwd, stb = terms[i]
        d = q * area
        windage += d
        thrust += d * fwd
        side += d * stb
        heel_m += d * stb * height
        yaw_m += d * stb * lever

    for area, height, lever, i in rig.spar_windage:
        q, fwd, stb = terms[i]
        d = q * area * SPAR_DRAG_COEFFICIENT
        windage += d
        thrust += d * fwd
        side += d * stb
        heel_m += d * stb * height
        yaw_m += d * stb * lever

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
# The rig as the wind meets it this tick (package 29: the performance budget)
# ---------------------------------------------------------------------------

# The key under which `integrate.step` keeps one tick's `_Rig` in `ship.extra` for its four
# substeps (`hold_rig`, `release_rig`).
RIG_KEY = "sails.rig"


@dataclass
class _Drawing:
    """One driving sail's figures that hold for the whole tick: its class, its area after
    reefing (before heel and blanketing), its chord's angle to the centreline, a square
    sail's chord and drive normal (on its yard's brace), and its worn canvas's luff; a
    fore-and-aft sail's side as its sheet holds it (package 32e)."""

    sail: Sail
    cls: SailClass
    area: float
    goose_winged: bool
    square_faced: bool
    studding: bool
    chord_angle: float
    square_chord: tuple[float, tuple[float, float]] | None
    baggy_luff: float
    height: float  # the cloth's height, for the blanketing shadow
    has_bowlines: bool  # any bowline at all (`hauled_weather_bowline` is None without one)
    side_sign: float = 0.0  # a fore-and-aft sail: +1 lying to starboard, -1 to larboard
    held: bool = False  # held on the weather side by its sheet: aback by the sheet
    flogging: bool = False  # every sheet let fly: it flogs
    working_sheet: str | None = None  # the sheet that carries its pull


@dataclass
class _Rig:
    """What the wind meets this tick: the sails drawing (`driving`, with their `drawing`
    figures), the sails not drawing (`idle`) and those of them that catch wind with their
    windage areas, the spars that catch wind with their areas, heights and levers, and the
    blanketing shadow's reach.

    Package 29's profile (spec M4 §20): nothing in these changes between the four substeps
    of a tick. Sails are set and furled, braces and sheets moved, spars sent down by the
    evolutions and the sheet tending before the substeps, and worn, blown out and carried
    away by the strain model after them; the substeps move only the hull and the helm, and
    slack a bowline (`_tend_bowlines`, which the forces read afresh each substep). So
    `integrate.step` holds one `_Rig` for its four substeps, and every number is the one
    the per-substep reading gave (the replay digests say so). A caller outside the
    integrator gets a fresh one each call."""

    driving: list[Sail]
    drawing: list[_Drawing]
    idle: list[Sail]
    idle_windage: list[tuple[float, float, float, int]]  # area, height, lever, height's slot
    spar_windage: list[tuple[float, float, float, int]]  # the same, for the spars
    windage_heights: list[float]  # the heights the windage reads, each once
    reach: float


def hold_rig(ship: Ship) -> None:
    """From now until `release_rig`, the rig is read once and kept (`integrate.step`)."""
    ship.extra[RIG_KEY] = None


def release_rig(ship: Ship) -> None:
    ship.extra.pop(RIG_KEY, None)


def _rig(ship: Ship) -> _Rig:
    if RIG_KEY not in ship.extra:
        return _read_rig(ship)
    rig = ship.extra[RIG_KEY]
    if rig is None:
        rig = _read_rig(ship)
        ship.extra[RIG_KEY] = rig
    return rig


def _read_rig(ship: Ship) -> _Rig:
    driving = [s for s in ship.sails.values() if _is_driving(ship, s)]
    drawing = []
    lee = yard_trim.lee_side_sign(ship)
    for sail in driving:
        cls = SAIL_CLASSES[sail.cls]
        reefs = min(max(sail.reefs, 0), sail.reef_bands)
        square_faced = not _in_gaff_plane(sail)
        square_chord = None
        side_sign, held, flogging, working = 0.0, False, False, None
        if sail.cls in SQUARE_FAMILY and square_faced:
            yard = _trim_yard(ship, sail)
            b = yard.brace_angle if yard is not None else 0.0
            # yard square: chord athwartships (pi/2); braced +b: starboard arm forward
            square_chord = (math.pi / 2 - b, (math.cos(b), -math.sin(b)))
        elif sail.is_fore_and_aft:
            # the sheet holds the trim (package 32e): the sail lies where its sheets hold
            # it, and its angle reading is refreshed from them
            reading = yard_trim.refresh_reading(ship, sail)
            side_sign = reading.side if reading.side is not None else lee
            held, flogging = reading.held_to_windward, reading.free
            working = reading.working.id if reading.working is not None else None
        drawing.append(
            _Drawing(
                sail=sail,
                cls=cls,
                area=sail.area_m2 * max(1.0 - cls.reef_factor * reefs, 0.0),
                goose_winged=sail.state is SailState.GOOSE_WINGED,
                square_faced=square_faced,
                studding=sail.cls == "studding",
                chord_angle=_chord_angle(ship, sail),
                square_chord=square_chord,
                baggy_luff=baggy_luff(sail),
                height=_sail_height(ship, sail),
                has_bowlines=bool(ship.lines_of(sail, "bowline")),
                side_sign=side_sign,
                held=held,
                flogging=flogging,
                working_sheet=working,
            )
        )
    driving_ids = {s.id for s in driving}
    idle = [s for s in ship.sails.values() if s.id not in driving_ids]
    heights: list[float] = []
    slots: dict[float, int] = {}

    def slot(height: float) -> int:
        i = slots.get(height)
        if i is None:
            i = slots[height] = len(heights)
            heights.append(height)
        return i

    clr_x = ship.hull.spec.clr_x_m
    idle_windage = []
    for sail in idle:
        area = _sail_windage_area(ship, sail)
        if area > 0:
            h = sail.centre_height_m
            idle_windage.append((area, h, sail.x_m - clr_x, slot(h)))
    spar_windage = []
    for spar, height, lever in _spar_places(ship):
        area = _spar_windage_area(spar)
        if area > 0:
            spar_windage.append((area, height, lever, slot(height)))
    return _Rig(
        driving=driving,
        drawing=drawing,
        idle=idle,
        idle_windage=idle_windage,
        spar_windage=spar_windage,
        windage_heights=heights,
        reach=_blanket_reach(ship),
    )


def _blanket_reach(ship: Ship) -> float:
    """How far downwind a sail's shadow reaches: BLANKET_RANGE_MAST_HEIGHTS of the tallest
    lower mast (fixed by the ship file, so kept per ship)."""
    reach = ship.extra.get("sails.blanket_reach")
    if not isinstance(reach, float):
        mast_height = max(
            (s.height_m for s in ship.spars.values() if s.cls == "mast"), default=20.0
        )
        reach = BLANKET_RANGE_MAST_HEIGHTS * mast_height
        ship.extra["sails.blanket_reach"] = reach
    return reach


def _chord_on_lee(chord_angle: float, awa: float) -> tuple[float, tuple[float, float]]:
    """`_chord` for a sail that lies on the lee side, from its chord's unsigned angle."""
    tack = 1.0 if awa >= 0 else -1.0  # sail lies on the lee side
    gamma = tack * chord_angle
    # normal pointing to leeward: the -tack side
    return gamma, (tack * math.sin(gamma), -tack * math.cos(gamma))


def _blanket_factors_and_offsets(
    ship: Ship, rig: _Rig, flows: dict[str, _Flow]
) -> tuple[dict[str, float], dict[str, float]]:
    """`_blanket_factors` over the rig's figures, and each driving sail's lateral offset
    (`_lateral_offset`), which the yaw moment reads again."""
    reach = rig.reach
    pos = {}
    height = {}
    offsets = {}
    for d in rig.drawing:
        s = d.sail
        y = _lateral_offset(ship, s, flows[s.id].awa, d.side_sign)
        offsets[s.id] = y
        pos[s.id] = (s.x_m, y, s.centre_height_m)
        height[s.id] = d.height
    return _shadows(rig.driving, flows, pos, height, reach), offsets


# ---------------------------------------------------------------------------
# The wind a sail feels
# ---------------------------------------------------------------------------


class _FlowField:
    """The apparent wind at any height for one substep, each height worked out once.

    Package 29's profile (the performance budget, spec M4 §20): the sails, the furled
    canvas and the bare spars ask for the wind at some sixty heights a substep, many of
    them the same, and each asked the wind for its speed, its vector and the heading's
    sines afresh. Here the wind's direction and gust, the heading's sine and cosine and
    the ship's motion are read once, and each height's flow is kept for the substep. The
    arithmetic is `Wind.vector_at_height` and `_apparent` step for step, in the same order,
    so every number is the same to the last bit (the replay digests say so). A wind that
    is not the plain `Wind` (a test's own) is asked through its methods as before.
    """

    __slots__ = ("wind", "plain", "eff", "sin_t", "cos_t", "sin_h", "cos_h", "u", "v", "memo")

    def __init__(self, ship: Ship, wind: Wind) -> None:
        from freesail.physics.wind import Wind as PlainWind

        self.wind = wind
        self.plain = type(wind) is PlainWind
        psi = ship.dyn.heading
        self.sin_h, self.cos_h = math.sin(psi), math.cos(psi)
        self.u, self.v = ship.dyn.u, ship.dyn.v
        water = ship.extra.get("water")
        if water and (water[0] != 0.0 or water[1] != 0.0):
            # the tide's stream (package 34): the rig feels her motion over the ground
            self.u += water[0] * self.sin_h + water[1] * self.cos_h
            self.v += water[0] * self.cos_h - water[1] * self.sin_h
        self.eff = self.sin_t = self.cos_t = 0.0
        if self.plain:
            self.eff = wind.effective_speed
            toward = wind.direction_from + math.pi  # units.wind_vector
            self.sin_t, self.cos_t = math.sin(toward), math.cos(toward)
        self.memo: dict[float, _Flow] = {}

    def air(self, height: float) -> tuple[float, float, float]:
        """(speed, forward, starboard) of the air past the ship at a height, m/s."""
        if self.plain:
            speed = self.eff * _shear(self.wind, height)
            vx, vy = speed * self.sin_t, speed * self.cos_t
        else:
            vx, vy = self.wind.vector_at_height(height)
        sin_h, cos_h = self.sin_h, self.cos_h
        a_fwd = vx * sin_h + vy * cos_h - self.u
        a_stb = vx * cos_h - vy * sin_h - self.v
        return math.hypot(a_fwd, a_stb), a_fwd, a_stb

    def at(self, height: float) -> _Flow:
        flow = self.memo.get(height)
        if flow is not None:
            return flow
        speed, a_fwd, a_stb = self.air(height)
        if speed < 1e-9:
            flow = _Flow(0.0, -1.0, 0.0, 0.0)
        else:
            flow = _Flow(speed, a_fwd / speed, a_stb / speed, math.atan2(-a_stb, -a_fwd))
        self.memo[height] = flow
        return flow

    def drag_terms(self, heights: list[float]) -> list[tuple[float, float, float]]:
        """(q, fwd, stb) at each height: what windage reads, which needs no angle. The
        same numbers as `at(height)`'s `q`, `fwd` and `stb`, worked in one loop."""
        out = []
        half_rho = 0.5 * units.RHO_AIR  # _Flow.q, left to right
        if not self.plain:
            airs = [self.air(height) for height in heights]
        else:
            eff, sin_t, cos_t = self.eff, self.sin_t, self.cos_t
            sin_h, cos_h, u, v = self.sin_h, self.cos_h, self.u, self.v
            airs = []
            for height in heights:
                wind_speed = eff * _shear(self.wind, height)
                vx, vy = wind_speed * sin_t, wind_speed * cos_t
                a_fwd = vx * sin_h + vy * cos_h - u
                a_stb = vx * cos_h - vy * sin_h - v
                airs.append((math.hypot(a_fwd, a_stb), a_fwd, a_stb))
        for speed, a_fwd, a_stb in airs:
            if speed < 1e-9:
                out.append((half_rho * 0.0 * 0.0, -1.0, 0.0))
            else:
                out.append((half_rho * speed * speed, a_fwd / speed, a_stb / speed))
        return out


# `Wind.speed_at_height`'s shear factor, (h / REFERENCE_HEIGHT) ** SHEAR_EXPONENT, kept by
# height: the same power of the same numbers is the same number, and a ship's parts stand
# at a few dozen heights (package 29's profile).
_SHEAR_FACTORS: dict[tuple[float, float, float], float] = {}


def _shear(wind: Wind, height: float) -> float:
    h = max(height, 1.0)
    key = (h, wind.REFERENCE_HEIGHT, wind.SHEAR_EXPONENT)
    k = _SHEAR_FACTORS.get(key)
    if k is None:
        k = (h / wind.REFERENCE_HEIGHT) ** wind.SHEAR_EXPONENT
        _SHEAR_FACTORS[key] = k
    return k


def _apparent(ship: Ship, wind: Wind, height: float) -> _Flow:
    """Apparent wind at a height above the water, in the ship's axes."""
    vx, vy = wind.vector_at_height(height)
    psi = ship.dyn.heading
    sin_h, cos_h = math.sin(psi), math.cos(psi)
    u, v = ship.dyn.u, ship.dyn.v
    water = ship.extra.get("water")
    if water and (water[0] != 0.0 or water[1] != 0.0):
        u += water[0] * sin_h + water[1] * cos_h  # over the ground (package 34)
        v += water[0] * cos_h - water[1] * sin_h
    # world (x east, y north) to body (forward, starboard)
    a_fwd = vx * sin_h + vy * cos_h - u
    a_stb = vx * cos_h - vy * sin_h - v
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
    """The yard whose brace sets this sail's angle: its own, or a stuns'l's parent yard.
    A studding sail with no side (the ringtail, the water sail) has none: it lies in its
    gaff sail's plane (`_gaff_host`)."""
    yard = ship.yard_of(sail)
    if yard is None and sail.cls == "studding" and not _in_gaff_plane(sail):
        boom = ship.spar_of_role(sail, "boom")
        yard = ship.parent_of(boom) if boom is not None else None
    return yard


# ---------------------------------------------------------------------------
# Studding sails and the wind (spec 3b §7)
# ---------------------------------------------------------------------------


def _in_gaff_plane(sail: Sail) -> bool:
    """A studding-class sail with no side: the ringtail abaft a gaff sail's leech, the
    water sail under its boom (spec 3b §6.4). It extends the gaff sail, not a yard."""
    return sail.cls == "studding" and sail.side is None


def _gaff_host(ship: Ship, sail: Sail) -> Sail | None:
    """The gaff sail whose plane a sideless studding sail lies in: the one on the boom its
    own boom rigs out on (the ringtail's), or the boom it is spread under (the water
    sail's). The one set, if any is (a storm trysail may be bent in the mainsail's place)."""
    boom = ship.spar_of_role(sail, "boom")
    if boom is not None and boom.cls == "studdingsail_boom":
        boom = ship.parent_of(boom)
    if boom is None:
        return None
    hosts = [
        s
        for s in ship.sails.values()
        if s is not sail and s.is_fore_and_aft and s.roles.get("boom") == boom.id
    ]
    return next((s for s in hosts if s.is_set), hosts[0] if hosts else None)


def true_wind_off_bow(ship: Ship, wind: Wind) -> float:
    """The true wind's angle off the bow, radians 0..pi, unsigned: the angle Luce and the
    known truths count points of sail by ("six points", "one point free")."""
    vx, vy = wind.vector_at_height(10.0)
    psi = ship.dyn.heading
    t_fwd = vx * math.sin(psi) + vy * math.cos(psi)
    t_stb = vx * math.cos(psi) - vy * math.sin(psi)
    if math.hypot(t_fwd, t_stb) < 1e-9:
        return math.pi  # no wind: nothing forward of any limit
    return abs(math.atan2(-t_stb, -t_fwd))


def studding_level(ship: Ship, sail: Sail) -> str:
    """'lower' or 'upper' for the stall's angle (spec 3b §7): a studding sail beside a lower
    yard's sail is a lower one, beside a topsail or topgallant an upper one; a sail with no
    yard (the ringtail, the water sail) takes the lower's figure, as do the save-alls."""
    yard = ship.yard_of(sail)
    parent = ship.parent_of(yard) if yard is not None else None
    return "upper" if parent is not None and parent.cls != "mast" else "lower"


def studding_stall(ship: Ship, sail: Sail, off_bow: float) -> float:
    """How far a studding sail is stalled, 0 (drawing) to 1 (all shaking), with the true
    wind `off_bow` radians off the bow: nothing abaft its level's angle, all of it a point
    (the band) forward of it, in a straight line between. Any other class: 0."""
    if sail.cls != "studding":
        return 0.0
    cls = SAIL_CLASSES["studding"]
    limit = cls.stall_wind.get(studding_level(ship, sail))
    if limit is None or off_bow >= limit:
        return 0.0
    if cls.stall_band <= 0.0:
        return 1.0
    return min((limit - off_bow) / cls.stall_band, 1.0)


def _record_shivering(ship: Ship, sail: Sail, stall: float, off_bow: float) -> None:
    """Keep `sail.shivering` and log it as it starts and stops. It starts the moment the
    wind is forward of the sail's angle and stops SHIVERING_HYSTERESIS_DEG abaft it."""
    if sail.cls != "studding":
        return
    if stall > 0.0:
        shivering = True
    elif sail.shivering:
        limit = SAIL_CLASSES["studding"].stall_wind.get(studding_level(ship, sail), 0.0)
        shivering = off_bow < limit + units.deg_to_rad(SHIVERING_HYSTERESIS_DEG)
    else:
        shivering = False
    if shivering == sail.shivering:
        return
    sail.shivering = shivering
    from freesail.evolutions.runner import part_name  # local import, as scripts.py does

    name = part_name(ship, sail.id)
    name = name[:1].upper() + name[1:]
    if shivering:
        ship.note(
            "notable",
            "sail.shivering",
            f"{name} shaking in its gear; she is too near the wind to carry it.",
            subject=sail.id,
        )
    else:
        ship.note("routine", "sail.drawing", f"{name} drawing again.", subject=sail.id)


def _apply_shaking(ship: Ship, sail: Sail, drag_area_q: float) -> None:
    """The snatching of a shivering studding sail (spec 3b §7), as the strain model loads a
    sail whose sheet has parted (strain.py, `_load_flogging`): the cloth's flogging drag,
    `drag_area_q` (newtons per unit drag coefficient) times FLOGGING_DRAG_COEFFICIENT, on
    the cloth, and doubled by FLOGGING_LOAD_MULTIPLIER on the yard, the spars beneath it
    and the boom whose end the tack is hauled out to."""
    flog_kn = drag_area_q * FLOGGING_DRAG_COEFFICIENT / 1000.0
    sail.load_kn += flog_kn
    spars = list(ship.spar_chain(sail))
    boom = ship.spar_of_role(sail, "boom")
    if boom is not None and boom not in spars:
        spars.append(boom)
    for spar in spars:
        if not (spar.wrecked or spar.sent_down):
            spar.load_kn += FLOGGING_LOAD_MULTIPLIER * flog_kn


def _chord_angle(ship: Ship, sail: Sail) -> float:
    """Unsigned angle of the sail's chord from the centreline, radians."""
    if _in_gaff_plane(sail):
        host = _gaff_host(ship, sail)
        return min(abs(host.sheet_angle), math.pi / 2) if host is not None else 0.0
    if sail.cls in SQUARE_FAMILY:
        yard = _trim_yard(ship, sail)
        brace = yard.brace_angle if yard is not None else 0.0
        return math.pi / 2 - min(abs(brace), math.pi / 2)
    return min(abs(sail.sheet_angle), math.pi / 2)


def _chord(ship: Ship, sail: Sail, awa: float) -> tuple[float, tuple[float, float]]:
    """The chord axis bearing (radians from the bow) and the 'drive normal'.

    The drive normal is the unit vector the air moves along when the sail is
    drawing as intended: forward through a square sail (wind on its after
    face), to leeward through a fore-and-aft sail (wind on its weather face). A
    studding sail with no side lies in its gaff sail's plane on the lee side, at that
    sail's sheet angle.
    """
    if sail.cls in SQUARE_FAMILY and not _in_gaff_plane(sail):
        yard = _trim_yard(ship, sail)
        b = yard.brace_angle if yard is not None else 0.0
        # yard square: chord athwartships (pi/2); braced +b: starboard arm forward
        return math.pi / 2 - b, (math.cos(b), -math.sin(b))
    tack = 1.0 if awa >= 0 else -1.0  # sail lies on the lee side
    gamma = tack * _chord_angle(ship, sail)
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
    square_faced: bool = True,
    held: bool = False,
) -> tuple[float, float, bool]:
    """Lift and drag on one sail, resolved into (forward, starboard) newtons.

    The sail is a plate along `chord`. Drag acts along the apparent wind;
    lift across it, toward the sail's lee side. Returns the force and whether
    a square sail is backed. `luff_gain` is a hauled bowline's (see
    `SailClass.coefficients`); it helps only a sail drawing on its after face.
    `square_faced` false takes a studding-class sail lying in a gaff sail's plane
    (the ringtail, the water sail) as fore-and-aft: wind on its lee face, it collapses.
    `held` is a fore-and-aft sail whose sheet holds it on the weather side (package
    32e): it stands as a plate with the wind on its outer face, aback, and does not
    collapse.
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
        if (sail.cls in SQUARE_FAMILY and square_faced) or held:
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


# A sail's "taken aback" is said once an episode, and "filled again" once after it
# (package 37f; the review of gate 5c's playtests, 8.2 under "The log"): the lines are
# armed again when the sail has stood full this long together with way on her, so a sail
# that lifts and fills by turns in a calm, or with her in irons, is one line and its
# answer. The hull's own figures (`hull.ABACK_REARM_SECONDS`, `hull.WAY_ON_KN`), kept
# here since the hull's module is not this one's to import.
BACKED_REARM_S = 60.0
BACKED_REARM_WAY_KN = 0.5


def _laid_aback_by_order(ship: Ship, sail: Sail) -> bool:
    """Whether a sail going aback now is aback by order (package 37f: none of the
    per-sail lines for those): she is hove to, when the yards to the mast and the head
    sheet to windward are the watch's own work; or a whole-ship evolution is in hand (a
    tack, a wear, heaving to, filling away, getting under way, coming to anchor), which
    lays yards aback as it goes; or an evolution is working this sail, its yard or its
    sheets (`back the main topsail`, a sheet hauled to windward)."""
    if "hove_to" in ship.extra:
        return True
    runner = ship.extra.get("evolutions")
    instances = getattr(runner, "instances", None)
    if not instances:
        return False
    yard = ship.yard_of(sail)
    mine = {sail.id, *(ln.id for ln in ship.sheets_of(sail))}
    if yard is not None:
        mine.add(yard.id)
    for inst in instances:
        subject = getattr(inst, "subject_id", None)
        if subject in ("ship", ship.name) or subject in mine:
            return True
    return False


def sails_in_hand(ship: Ship) -> set[str]:
    """The sails the hands are at now (package 37k): every sail that a running evolution
    works, itself, its yard or its sheets (`set the jib`, `trim the fore topsail`, a sheet
    hauled), as `_laid_aback_by_order` reads a sail's own work; work waiting for hands is
    not yet at it. The alarm for being taken aback leaves these alone: in game 10 two of
    its eight urgent cries came as sail was made after weighing, the sails not yet
    sheeted home and trimmed."""
    runner = ship.extra.get("evolutions")
    instances = getattr(runner, "instances", None)
    if not instances:
        return set()
    out: set[str] = set()
    for inst in instances:
        if getattr(inst, "waiting", False) or getattr(inst, "paused", False):
            continue
        subject = getattr(inst, "subject", None)
        if isinstance(subject, Sail):
            out.add(subject.id)
        elif isinstance(subject, Spar):
            sail = ship.sail_of(subject)
            if sail is not None:
                out.add(sail.id)
        elif isinstance(subject, Line):
            for sl in ship.sails.values():
                if subject in ship.sheets_of(sl):
                    out.add(sl.id)
                    break
        named = (getattr(inst, "params", None) or {}).get("sail")
        if isinstance(named, str):
            out.add(named)
    return out


def _record_backed(ship: Ship, sail: Sail, backed: bool, dt: float = 0.0) -> None:
    timers = ship.extra.get("sails.backed_for")
    if not isinstance(timers, dict):
        timers = ship.extra["sails.backed_for"] = {}
    said = ship.extra.get("sails.backed_said")
    if not isinstance(said, dict):
        said = ship.extra["sails.backed_said"] = {}
    if backed == sail.backed:
        timers.pop(sail.id, None)
        entry = said.get(sail.id)
        if entry is not None and not backed and dt > 0.0:
            # full, and with way on her: the lines are armed again after a minute of it
            if ship.dyn.u >= units.knots_to_ms(BACKED_REARM_WAY_KN):
                entry["clear_s"] = entry.get("clear_s", 0.0) + dt
                if entry["clear_s"] >= BACKED_REARM_S:
                    del said[sail.id]
            else:
                entry["clear_s"] = 0.0
        return
    by_order = ship.extra.get("sails.backed_by_order")
    if not isinstance(by_order, dict):
        by_order = ship.extra["sails.backed_by_order"] = {}
    if dt > 0.0:
        held = timers.get(sail.id, 0.0) + dt
        if held < BACKED_DWELL_S:
            if sail.id not in timers:
                # as it begins to go: an order's work may be done before the dwell is
                by_order[sail.id] = _laid_aback_by_order(ship, sail)
            timers[sail.id] = held
            return
    timers.pop(sail.id, None)
    ordered = bool(by_order.pop(sail.id, False)) or _laid_aback_by_order(ship, sail)
    sail.backed = backed
    name = _name(sail.id)
    entry = said.get(sail.id)
    if backed:
        if ordered:
            # laid aback by order: no line for it, nor for its filling when the order ends
            said[sail.id] = {"silent": True, "filled": True, "clear_s": 0.0}
            return
        if entry is not None:
            entry["clear_s"] = 0.0
            return  # once an episode
        said[sail.id] = {"filled": False, "clear_s": 0.0}
        ship.note("notable", "sail.backed", f"{name} taken aback.", subject=sail.id)
    else:
        if entry is None or entry.get("filled"):
            if entry is not None and entry.get("silent"):
                del said[sail.id]  # the order's own sail, full again: nothing stands
            return
        entry["filled"] = True
        ship.note("routine", "sail.filled", f"{name} filled again.", subject=sail.id)


def _name(part_id: str) -> str:
    text = part_id.replace(".", " ").replace("_", " ")
    return text[:1].upper() + text[1:]


# ---------------------------------------------------------------------------
# Where a sail is, for blanketing and for the yaw of one-sided sails
# ---------------------------------------------------------------------------


def _lateral_offset(ship: Ship, sail: Sail, awa: float, side_sign: float = 0.0) -> float:
    """Metres to starboard of the centreline of the sail's centre of effort. A
    fore-and-aft sail lies on `side_sign`'s side (+1 starboard) when given (the side its
    sheet holds it, package 32e), else to leeward of the apparent wind."""
    if sail.state is SailState.GOOSE_WINGED:
        # the weather clew is the one left set: the centre moves out to windward
        yard = _trim_yard(ship, sail)
        reach = GOOSE_WINGED_SHIFT * (yard.length_m if yard is not None else 0.0)
        return reach if awa >= 0 else -reach
    if _in_gaff_plane(sail):
        # in the gaff sail's plane on the lee side (spec 3b §6.4): as far out as its centre
        # lies abaft the mast along the boom, swung out by the sheet
        host = _gaff_host(ship, sail)
        mast = ship.mast_of(ship.spar_of_role(sail, "boom")) if host is not None else None
        along = max(mast.x_m - sail.x_m, 0.0) if mast is not None else 0.0
        lee = -1.0 if awa >= 0 else 1.0
        return lee * along * math.sin(_chord_angle(ship, sail))
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
        lee = side_sign if side_sign != 0.0 else (-1.0 if awa >= 0 else 1.0)
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
    return _shadows(driving, flows, pos, height, reach)


def _shadows(
    driving: list[Sail],
    flows: dict[str, _Flow],
    pos: dict[str, tuple[float, float, float]],
    height: dict[str, float],
    reach: float,
) -> dict[str, float]:
    """The blanketing rule of `_blanket_factors`, given each sail's place and height.

    Every pair of driving sails is looked at each substep, so the loop reads plain local
    values (package 29's profile); the arithmetic and the tests are the rule's, in order."""
    out: dict[str, float] = {}
    places = [(a, *pos[a.id], height[a.id], a.cls in SQUARE_FAMILY) for a in driving]
    for b, xb, yb, zb, hb, b_square in places:
        flow = flows[b.id]
        fwd, stb = flow.fwd, flow.stb
        b_running = b_square and abs(flow.awa) >= RUNNING_AWA
        shadow = 0.0
        for a, xa, ya, za, ha, a_square in places:
            if a is b:
                continue
            dx, dy = xb - xa, yb - ya
            along = dx * fwd + dy * stb  # positive: b is downwind of a
            if not (0.0 < along <= reach):
                continue
            across = abs(-dx * stb + dy * fwd)
            if across > 0.5 * ha:
                continue
            if abs(za - zb) > 0.5 * (ha + hb):
                continue
            running = a_square and b_running
            shadow = max(shadow, BLANKET_RUNNING if running else BLANKET_OTHER)
        out[b.id] = 1.0 - shadow
    return out


# ---------------------------------------------------------------------------
# Strain (§7.5): who carries the sail's pull
# ---------------------------------------------------------------------------


def _reset_loads(ship: Ship) -> None:
    for part in ship.parts.values():
        part.load_kn = 0.0


@dataclass(frozen=True)
class _LoadPath:
    """Who carries a sail's pull, from the graph (fixed once the ship is loaded): its spars
    nearest first and a studding sail's boom, its sheets, halyards and braces, its stay."""

    spars: tuple[Spar, ...]
    sheets: tuple[Line, ...]
    halyards: tuple[Line, ...]
    braces: tuple[Line, ...]
    stay: Line | None


def _load_path(ship: Ship, sail: Sail) -> _LoadPath:
    """The sail's load path, worked out once per ship and kept (package 29's profile)."""
    paths = ship.extra.get("sails.load_paths")
    if not isinstance(paths, dict):
        paths = {}
        ship.extra["sails.load_paths"] = paths
    path = paths.get(sail.id)
    if path is None:
        chain = ship.spar_chain(sail)
        spars = list(chain)  # each spar carries everything above it
        if sail.cls == "studding":
            # the graph's chain starts at the parent yard; the boom carries it too
            boom = ship.spar_of_role(sail, "boom")
            if boom is not None and boom not in chain:
                spars.append(boom)
        halyards = [ln for ln in ship.lines_of(sail) if ln.cls in HALYARD_CLASSES]
        if chain:
            halyards += [ln for ln in ship.lines_of(chain[0]) if ln.cls in HALYARD_CLASSES]
        yard = ship.yard_of(sail)
        stay = sail.roles.get("stay")
        path = _LoadPath(
            spars=tuple(spars),
            sheets=tuple(ship.sheets_of(sail)),
            halyards=tuple(halyards),
            braces=tuple(ship.braces_of(yard)) if yard is not None else (),
            stay=ship.lines[stay] if stay in ship.lines else None,
        )
        paths[sail.id] = path
    return path


def _sheet_load_kn(ship: Ship, sail: Sail, force_kn: float, d: _Drawing | None) -> float:
    """What the working sheet carries of the sail's pull (package 32e). A boomed sail's
    sheet holds the boom against the sail's moment about the mast: the pull times the
    sail's centre's distance abaft the mast, over the sheet's lever (the perpendicular
    from the mast to the sheet's line, `SheetGeometry.lever_m`), so a sheet eased far
    off or hauled nearly amidships bears more than one at a working angle. A
    loose-footed sail's sheet takes SHEET_LOAD_FRACTION of the pull, its tack and
    halyard the rest."""
    if d is None or d.side_sign == 0.0:
        return SHEET_LOAD_FRACTION * force_kn
    geo = yard_trim.sheet_geometry(ship, sail)
    if not geo.boomed:
        return SHEET_LOAD_FRACTION * force_kn
    mast = ship.mast_of(sail)
    arm = abs(mast.x_m - sail.x_m) if mast is not None else 0.4 * geo.arm_m
    lever = geo.lever_m(d.chord_angle)
    if lever <= 0.1:
        lever = 0.1
    return force_kn * arm / lever


def _apply_loads(ship: Ship, sail: Sail, force_kn: float, d: _Drawing | None = None) -> None:
    """Put a sail's pull on its cloth, its spars and its running rigging."""
    sail.load_kn = force_kn
    path = _load_path(ship, sail)
    for spar in path.spars:
        spar.load_kn += force_kn
    if d is not None and d.side_sign != 0.0:
        # a fore-and-aft sail: its working sheet carries the pull, a sheet let fly nothing
        if d.working_sheet is not None:
            for ln in path.sheets:
                if ln.id == d.working_sheet:
                    ln.load_kn += _sheet_load_kn(ship, sail, force_kn, d)
    else:
        for ln in path.sheets:
            ln.load_kn += SHEET_LOAD_FRACTION * force_kn
    for ln in path.halyards:
        ln.load_kn += HALYARD_LOAD_FRACTION * force_kn
    for ln in path.braces:
        ln.load_kn += BRACE_LOAD_FRACTION * force_kn
    if path.stay is not None:
        path.stay.load_kn += STAY_LOAD_FRACTION * force_kn


# ---------------------------------------------------------------------------
# Windage: what the wind pushes on that is not drawing
# ---------------------------------------------------------------------------


def _sail_windage_area(ship: Ship, sail: Sail) -> float:
    cls = SAIL_CLASSES.get(sail.cls)
    if cls is None or sail.state is SailState.UNBENT:
        # unbent: in the sail room, or gone over the side with a wreck cleared away
        # (package 30b), whatever became of the spars it was bent to
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


def _spar_places(ship: Ship) -> tuple[tuple[Spar, float, float], ...]:
    """Each spar with the height of its middle and its lever about the centre of lateral
    resistance (`_spar_x` less `clr_x_m`), in the ship file's order: fixed by the graph
    and the ship file, so worked out once per ship and kept (package 29's profile)."""
    places = ship.extra.get("sails.spar_places")
    if not isinstance(places, tuple):
        clr = ship.hull.spec.clr_x_m
        places = tuple(
            (spar, _spar_centre_height(ship, spar), _spar_x(ship, spar) - clr)
            for spar in ship.spars.values()
        )
        ship.extra["sails.spar_places"] = places
    return places
