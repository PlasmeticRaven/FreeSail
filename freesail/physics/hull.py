"""Hull physics and the helmsman (spec §7.4).

What the water does to the ship, and what the man at the wheel does with the
rudder. The sails (package 4) push; this module answers with resistance
through the water, the sideways grip of the keel, the hull's reluctance to
turn, the heel that the wind's press and the ballast's righting settle on, and
the rudder. `integrate.py` adds the forces up and moves the ship; nothing here
changes `ship.dyn` except the helmsman's own bookkeeping.

Every number a tuner might want to touch is a named constant at the top of the
file. Units are SI throughout: metres, seconds, kilograms, newtons, radians.

Sign conventions (spec §4 and `Dynamics`): `u` is speed ahead, `v` speed to
starboard, `r` the rate of turning to starboard, `heel` positive when heeled
to starboard, `rudder` positive when put to starboard (the ship turns to
starboard), apparent wind angle positive when the wind is on the starboard
bow.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from freesail import units
from freesail.physics.wind import Wind
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode, Hull

# ---------------------------------------------------------------------------
# Tuning constants (package 10 adjusts these against the known truths, §7.6)
# ---------------------------------------------------------------------------

C_F = 0.008  # resistance coefficient on the wetted surface: friction, form and copper roughness
C_LAT = 1.0  # cross-flow drag of the lateral plane when the hull slides sideways (v |v|)
C_LAT_LIFT = 1.0  # keel lift per radian of leeway at speed (u v); the keel's "grip" when moving
C_YAW = 2.0  # quadratic yaw damping of the lateral plane when the ship swings fast (r |r|)
C_YAW_LIN = 2.5  # linear yaw damping when moving ahead (u r): a moving hull resists swinging
C_R = 2.5  # rudder lift per radian of helm; rudder side force = q * A_rudder * C_R * delta
RUDDER_X_FRACTION = 0.5  # the rudder hangs this fraction of the waterline length abaft amidships
RUDDER_SMALL_SPEED2 = 0.01  # m^2/s^2 added to u^2 so the rudder keeps a whisper of effect at rest
HEEL_DRAG_PER_RAD = 3.0  # extra resistance per radian of heel beyond HEEL_DRAG_ONSET (dragging)
HEEL_DRAG_ONSET = math.radians(20.0)  # heel at which the lee rail drags and speed falls
HEEL_KEEL_LEVER_FRACTION = 0.8  # the keel's reaction acts this fraction of the draught below water
HEEL_TIME_CONSTANT = 4.0  # seconds for the heel to settle to its balance (quasi-static heel)
BEAM_ENDS_HEEL = math.radians(40.0)  # heel at which the log cries "on her beam ends"
ADDED_MASS_SURGE = 0.05  # water carried along ahead, as a fraction of displacement
ADDED_MASS_SWAY = 0.8  # water carried along sideways, as a fraction of displacement
RADIUS_OF_GYRATION = 0.25  # yaw radius of gyration as a fraction of waterline length
ADDED_INERTIA_YAW = 0.5  # water swung with the hull, as a fraction of the dry yaw inertia
SWAY_CLAMP_SLOPE = 0.6  # |v| may not exceed SWAY_CLAMP_SLOPE * |u| + SWAY_CLAMP_OFFSET
SWAY_CLAMP_OFFSET = 0.5  # m/s; keeps sway sane at low speed (spec §7.4)
STERNWAY_SHIFT_SPEED = 0.15  # m/s of sternway beyond which the helmsman shifts the helm
HELM_KP = 1.0  # helmsman: radians of rudder per radian of heading error
HELM_KD = 8.0  # helmsman: seconds; rudder eased against the rate of swing to meet her
HELM_KI = 0.03  # helmsman: per second; how quickly he learns the helm she carries
HELM_KI_WINDOW = math.radians(10.0)  # he only learns the helm once within this much of the course
HELM_KI_LEAK_S = 60.0  # seconds; outside that window, or without way, what he learned fades
HELM_STEERAGE_SPEED = 0.75  # m/s (1.5 kn); under this the rudder bites too little to learn from
HELM_STUCK_RATE = math.radians(
    0.1
)  # rad/s; swinging slower than this, he learns the helm she carries
FULL_AND_BY_MARGIN = math.radians(8.0)  # sailed this much fuller than the sails' luffing angle
FULL_AND_BY_DEFAULT_LUFF = math.radians(45.0)  # luffing angle when package 4 has not said
WEATHER_HELM_TIME_CONSTANT = 30.0  # seconds; the weather-helm reading averages the rudder
STEADY_TOLERANCE = math.radians(2.0)  # within this of the ordered heading counts as on it
STEADY_SECONDS = 20.0  # for this long before the log says "steady"
ABACK_SECONDS = 10.0  # net thrust astern for this long with sail set is "taken aback"
LEEWAY_NOTE_THRESHOLD = math.radians(1.0)  # leeway must change by this much to be noted
LEEWAY_NOTE_INTERVAL = 60.0  # seconds; at most one leeway note per minute
LEEWAY_MIN_SPEED = 0.25  # m/s; below this leeway is meaningless and read as zero


# ---------------------------------------------------------------------------
# Bookkeeping the helmsman and the log keep between ticks
# ---------------------------------------------------------------------------


@dataclass
class HullState:
    """Memory that hull physics keeps in `ship.extra["hull"]` between ticks."""

    helm_integral: float = 0.0  # the helm the helmsman has learned to carry, radians
    last_target_heading: float | None = None  # to notice a new heading order
    last_helm_mode: HelmMode | None = None  # to notice a change of helm mode
    seconds_on_course: float = 0.0  # time spent within STEADY_TOLERANCE of the order
    steady_noted: bool = False  # helm.steady already logged for this order
    seconds_aback: float = 0.0  # time the net thrust has been astern with sail set
    aback_noted: bool = False  # ship.aback already logged for this episode
    beam_ends_noted: bool = False  # "on her beam ends" already logged for this episode
    last_noted_leeway: float = 0.0  # radians, leeway when last written in the log
    seconds_since_leeway_note: float = LEEWAY_NOTE_INTERVAL
    last_thrust_n: float = 0.0  # net thrust of the last substep, for the aback rule
    awa: float = 0.0  # deck-level apparent wind angle computed here, for the helm
    aws: float = 0.0  # deck-level apparent wind speed computed here
    extra: dict = field(default_factory=dict)


def hull_state(ship: Ship) -> HullState:
    """The hull's memory for this ship, created on first use."""
    st = ship.extra.get("hull")
    if not isinstance(st, HullState):
        st = HullState()
        ship.extra["hull"] = st
    return st


# ---------------------------------------------------------------------------
# Mass and inertia
# ---------------------------------------------------------------------------


def surge_mass(hull: Hull) -> float:
    """Mass to be accelerated ahead: the ship plus a little water dragged with her."""
    return hull.spec.displacement_kg * (1.0 + ADDED_MASS_SURGE)


def sway_mass(hull: Hull) -> float:
    """Mass to be accelerated sideways: the ship plus a great deal of water."""
    return hull.spec.displacement_kg * (1.0 + ADDED_MASS_SWAY)


def yaw_inertia(hull: Hull) -> float:
    """Reluctance to swing: a long, heavy hull turns slowly (kg m^2)."""
    k = RADIUS_OF_GYRATION * hull.length
    return hull.spec.displacement_kg * k * k * (1.0 + ADDED_INERTIA_YAW)


# ---------------------------------------------------------------------------
# Forces from the water
# ---------------------------------------------------------------------------


def resistance(hull: Hull, u: float, heel: float = 0.0) -> float:
    """Resistance to motion ahead (or astern), in newtons, always opposing `u`.

    Skin friction over the wetted surface grows with the square of the speed;
    the quartic term stands in for wave-making and makes the last knots up to
    hull speed very dear. Beyond HEEL_DRAG_ONSET the lee side drags and the
    resistance rises again. The sign is opposite to `u`, so a ship making
    sternway is slowed just the same.
    """
    speed_ratio = abs(u) / hull.hull_speed if hull.hull_speed > 0 else 0.0
    wave = 1.0 + speed_ratio**4
    lean = 1.0 + HEEL_DRAG_PER_RAD * max(0.0, abs(heel) - HEEL_DRAG_ONSET)
    return -0.5 * units.RHO_WATER * hull.wetted_area * C_F * u * abs(u) * wave * lean


def sway_damping(hull: Hull, u: float, v: float) -> float:
    """The keel's grip against sliding sideways, in newtons, opposing `v`.

    Two parts: cross-flow drag of the whole lateral plane (grows with v^2, the
    only grip when she is stopped) and the keel's lift when she has way on
    (grows with u v: a moving keel bites like a wing). Leeway is what is left
    when this balances the sails' side force.
    """
    q_area = 0.5 * units.RHO_WATER * hull.lateral_area
    return -q_area * (C_LAT * v * abs(v) + C_LAT_LIFT * abs(u) * v)


def yaw_damping(hull: Hull, u: float, r: float) -> float:
    """The water's resistance to the hull swinging, in newton-metres, opposing `r`."""
    q_area = 0.5 * units.RHO_WATER * hull.lateral_area * hull.length
    return -q_area * (C_YAW_LIN * abs(u) * r + C_YAW * hull.length * r * abs(r))


def rudder_lever(hull: Hull) -> float:
    """Distance of the rudder abaft the centre of lateral resistance (negative x)."""
    return -RUDDER_X_FRACTION * hull.length - hull.spec.clr_x_m


def rudder_forces(hull: Hull, u: float, rudder: float) -> tuple[float, float]:
    """Side force (N, to starboard positive) and yaw moment (N m) from the rudder.

    A rudder put to starboard is pushed to larboard by the water streaming past
    it; acting at the stern, that swings the bow to starboard. The push grows
    with the square of the speed through the water, so a ship without way does
    not answer her helm. With sternway the rudder works the other way, as it
    should.
    """
    q = 0.5 * units.RHO_WATER * hull.spec.rudder.area_m2 * C_R
    flow = u * abs(u) + math.copysign(RUDDER_SMALL_SPEED2, u if u != 0 else 1.0)
    side = -q * flow * rudder
    return side, side * rudder_lever(hull)


# ---------------------------------------------------------------------------
# Heel
# ---------------------------------------------------------------------------


def equilibrium_heel(hull: Hull, heel_moment_nm: float, side_force_n: float) -> float:
    """The heel at which the wind's press and the ballast's righting balance.

    The sails push above the water and the keel pushes back below it; the
    couple is the sails' heeling moment plus the side force times the keel's
    depth. The righting moment is displacement times g times GM times sin(heel).
    If the press exceeds what the ship can right at all she is held at 90
    degrees (M2 does not capsize; the log will say she would).
    """
    keel = HEEL_KEEL_LEVER_FRACTION * hull.spec.draught_m
    moment = heel_moment_nm + side_force_n * keel
    righting = hull.spec.displacement_kg * units.G * hull.spec.gm_m
    if righting <= 0:
        return 0.0
    ratio = max(-1.0, min(1.0, moment / righting))
    return math.asin(ratio)


def relax_heel(heel: float, target: float, dt: float) -> float:
    """Move the heel toward its balance over HEEL_TIME_CONSTANT seconds."""
    return target + (heel - target) * math.exp(-dt / HEEL_TIME_CONSTANT)


# ---------------------------------------------------------------------------
# Apparent wind at deck level (also computed by package 4; kept here so the
# helmsman never depends on it)
# ---------------------------------------------------------------------------


def apparent_wind(ship: Ship, wind: Wind) -> tuple[float, float]:
    """Apparent wind angle (radians, + on the starboard bow) and speed (m/s) on deck."""
    d = ship.dyn
    wx, wy = wind.vector_at_height(ship.hull.spec.deck_height_m)
    ex, ey = units.heading_vector(d.heading)
    sx = d.u * ex + d.v * ey
    sy = d.u * ey - d.v * ex
    ax, ay = wx - sx, wy - sy
    speed = math.hypot(ax, ay)
    if speed < 1e-9:
        return 0.0, 0.0
    return units.relative_bearing(d.heading, units.wind_direction_from(ax, ay)), speed


# ---------------------------------------------------------------------------
# The helmsman
# ---------------------------------------------------------------------------


def heading_error(ship: Ship, st: HullState) -> float | None:
    """How far the ship must still turn (radians, + to starboard), or None in RUDDER mode.

    HEADING mode: the short way round from the present heading to the ordered
    one, so an order across north is nothing special. FULL_AND_BY: the sails'
    luffing angle plus a margin is the apparent wind angle wanted, on whichever
    bow the wind is now; the error is how far she must come up or bear away.
    """
    d = ship.dyn
    if d.helm_mode is HelmMode.HEADING:
        return units.wrap_pi(d.target_heading - d.heading)
    if d.helm_mode is HelmMode.FULL_AND_BY:
        luff = ship.extra.get("luff_angle")
        wanted = luff if isinstance(luff, int | float) else FULL_AND_BY_DEFAULT_LUFF
        wanted += FULL_AND_BY_MARGIN
        return st.awa - math.copysign(wanted, st.awa if st.awa != 0 else 1.0)
    return None


def steer(ship: Ship, dt: float) -> float:
    """The helmsman's hand: returns the rudder angle after `dt` seconds.

    In RUDDER mode he puts the wheel where ordered and holds it. Otherwise he
    meets her: helm in proportion to how far she is off her course, eased as
    she swings so as not to overshoot, plus whatever standing helm he has
    learned she needs to hold a straight course (the weather or lee helm). He
    learns that helm only near the course and with steerage way on; off the
    course or without way it fades over HELM_KI_LEAK_S, so a helm learned while
    she was rounding up with no way does not hold her off her course later. The
    wheel moves no faster than the rudder's rate and no further than its stop.
    """
    d = ship.dyn
    st = hull_state(ship)
    spec = ship.hull.spec.rudder
    max_angle = units.deg_to_rad(spec.max_angle_deg)
    if d.helm_mode is HelmMode.RUDDER:
        wanted = max(-max_angle, min(max_angle, d.target_rudder))
    else:
        err = heading_error(ship, st)
        assert err is not None
        # he learns the standing helm only when she is not swinging (on her
        # course, or held off it) and has steerage way; while she turns, what
        # the wheel is doing is not the helm she carries
        if abs(d.r) < HELM_STUCK_RATE and d.u > HELM_STEERAGE_SPEED:
            learn = max(-HELM_KI_WINDOW, min(HELM_KI_WINDOW, err))
            st.helm_integral += HELM_KI * learn * dt
            st.helm_integral = max(-max_angle, min(max_angle, st.helm_integral))
        else:
            # off her course, or without steerage way, the standing helm he
            # learned means nothing: let it fade rather than hold her off
            st.helm_integral *= math.exp(-dt / HELM_KI_LEAK_S)
        wanted = HELM_KP * err - HELM_KD * d.r + st.helm_integral
        if d.u < -STERNWAY_SHIFT_SPEED:
            # she is making sternway: the rudder acts the other way, so the
            # helmsman shifts the helm (and forgets the standing helm meanwhile)
            st.helm_integral = 0.0
            wanted = -(HELM_KP * err - HELM_KD * d.r)
        wanted = max(-max_angle, min(max_angle, wanted))
    rate = units.deg_to_rad(spec.rate_deg_s) * dt
    move = max(-rate, min(rate, wanted - d.rudder))
    return d.rudder + move


def weather_helm_reading(previous: float, rudder: float, awa: float, dt: float) -> float:
    """Update the weather-helm reading: the standing rudder she needs, averaged.

    Positive when she wants to round up into the wind (weather helm: the
    rudder must be held to leeward to stop her), negative for lee helm. The
    rudder is averaged over WEATHER_HELM_TIME_CONSTANT so the helmsman's
    working of the wheel does not show.
    """
    to_windward = -1.0 if awa >= 0 else 1.0  # rudder held to leeward reads positive
    sample = to_windward * rudder
    f = math.exp(-dt / WEATHER_HELM_TIME_CONSTANT)
    return sample + (previous - sample) * f
