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
from freesail.ship.schema import RudderSpec

# ---------------------------------------------------------------------------
# Tuning constants (package 10 adjusts these against the known truths, §7.6)
# ---------------------------------------------------------------------------

C_F = 0.008  # resistance coefficient on the wetted surface: friction, form and copper roughness
C_LAT = 1.0  # cross-flow drag of the lateral plane when the hull slides sideways (v |v|)
C_LAT_LIFT = 1.0  # keel lift per radian of leeway at speed (u v); the keel's "grip" when moving
# Yaw damping of the lateral plane (package 32e, spec M5 open item 12). The water's moment
# against the hull swinging is a cross-flow force on the lateral plane times a lever, and
# both grow with the length: at a point x along the hull the swing gives a cross flow r x,
# so the linear (lifting) term is rho A u (r L) acting at a lever of order L, a moment
# proportional to A L^2 u r, and the quadratic (cross-flow drag) term rho A (r L)^2 at the
# same lever, proportional to A L^3 r |r| (the standard slender-body form: Principles of
# Naval Architecture, the controllability chapter, whose yaw derivatives are made
# dimensionless by rho L^4 U for the linear and rho L^5 for the quadratic term). Package 10
# wrote the moment with one length only, rho A L (C u r + C' L r |r|), which is a force,
# not a moment, so the constants it tuned on the frigate hid her 41.8 m waterline: a
# fifty-foot cutter got the frigate's damping on a third of the lever and turned as the
# frigate turns, in metres (the lead's probe, 2026-09-30). The constants below are package
# 10's divided by the frigate's waterline (2.5 / 41.8, 2.0 / 41.8), so the frigate keeps
# the circle truth 16 measured (5.1 lengths at 8 knots) and every hull turns in a circle
# that scales with her length. Judgement: no period source gives a sailing ship's yaw
# damping; the form is the textbook's, the size fitted to the frigate's band.
C_YAW = 0.048  # quadratic yaw damping, per (A L^3 r |r|): the plane's cross-flow drag
C_YAW_LIN = 0.06  # linear yaw damping, per (A L^2 u r): a moving hull resists swinging
# The rudder's lift slope (per radian of helm) from the blade's aspect ratio, span^2 over
# area, by Helmbold's low-aspect-ratio formula 2 pi AR / (2 + sqrt(AR^2 + 4)) (Helmbold
# 1942, as Hoerner, Fluid-Dynamic Lift, ch. 3, gives it; quoted from memory, the page not
# verified), times RUDDER_EFFECTIVENESS for the wake of the deadwood and the sternpost the
# blade hangs behind and the flow's angle in a turn. Package 10 tuned one slope, C_R = 2.5,
# on the frigate (truths 10 and 16); her blade of 15 ft by 4 ft 3 in has an aspect ratio
# of 3.5 and a Helmbold slope of 3.65, so the effectiveness is 2.5 / 3.65 = 0.685 and the
# frigate's rudder pushes as it did. The schooner's, the cutter's and the brig's deeper,
# narrower blades (the ship files' span_m) bite a little harder per square metre (3.0,
# 3.1 and 2.8 per radian).
RUDDER_EFFECTIVENESS = 0.685  # judgement, fitted to keep package 10's rudder on the frigate
RUDDER_DEFAULT_ASPECT = 3.0  # a blade three times as deep as it is broad, when the file is silent
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
# Taken aback, the urgent line and its repeats (package 37c, the owner's ruling of
# 2026-10-03): a new episode is logged only after she has been clear of aback this long,
# so a thrust flickering about nought in a light air is one line and not one a minute;
# and the line is urgent only when there was something to lose, way on her as it began in
# an apparent wind of at least ABACK_URGENT_AWS_KN, free of the ground and the anchor.
# Otherwise it is notable (judgement: four knots, a light air to a light breeze, below
# which the sails aback cost her nothing she had).
ABACK_REARM_SECONDS = 60.0
ABACK_URGENT_AWS_KN = 4.0
# The lesser lines of it (package 37f; the review of gate 5c's playtests, 8.2 under "The
# log": "Her sails aback; she had no way on to lose" ten times in three hours of a calm).
# The clock arms the episode again, and the urgent line with it; the notable lines have a
# flag of their own (`HullState.aback_lesser`), armed again by her state and not by the
# clock: "no way on to lose", when she has way on again (`WAY_ON_KN`); "in the light
# air", when she has way on again or the wind is a working one again
# (`ABACK_URGENT_AWS_KN`); "as she lies at anchor" or "aground", when she does so no
# longer. So a calm is one line however long it lasts.
# Her sails lifting (package 37k; the review's G6: "Taken aback" was cried urgently eight
# times in game 10 "with no warning line before any of them"): the wind come forward of
# her luffing angle (`ship.extra["luff_angle"]`, the angle the helm's full-and-by keeps
# FULL_AND_BY_MARGIN outside) for LIFT_SAY_S together, with way on her in a working
# breeze, under sail that stands and no manoeuvre in hand, is a notable line, said before
# she can be aback (ABACK_SECONDS, after a sail's own ten seconds aback). Said once an
# episode, and armed again when she has stood full LIFT_REARM_S. Judgement: five seconds,
# longer than a sea's lift of the wind and short of the aback's; the rearm the aback's.
LIFT_SAY_S = 5.0
LIFT_REARM_S = ABACK_REARM_SECONDS
LEEWAY_NOTE_THRESHOLD = math.radians(1.0)  # leeway must change by this much to be noted
LEEWAY_NOTE_INTERVAL = 60.0  # seconds; at most one leeway note per minute
LEEWAY_MIN_SPEED = 0.25  # m/s; below this leeway is meaningless and read as zero
# Knots of headway under which the log writes no leeway line and the readings give no
# course or leeway (package 28c, playtests 1 and 3; judgement: half a knot, about the
# LEEWAY_MIN_SPEED above, as a sailor's "no way on"; `readings.READING_SPEED_FLOOR_KN`)
WAY_ON_KN = 0.5


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
    # time clear of aback since the last episode (starting armed), and whether she had
    # way on as this episode began (package 37c); class defaults, so older saves load
    seconds_clear_of_aback: float = ABACK_REARM_SECONDS
    aback_had_way: bool = False
    # which lesser line stands said ("anchor", "no_way", "light"; "" for none): package
    # 37f, with a default so that an older save loads
    aback_lesser: str = ""
    # her sails lifting (package 37k): how long, whether said this episode, how long she
    # has stood full since; defaults, so that an older save loads
    seconds_lifting: float = 0.0
    lifting_noted: bool = False
    seconds_full: float = 0.0
    beam_ends_noted: bool = False  # "on her beam ends" already logged for this episode
    last_noted_leeway: float = 0.0  # radians, leeway when last written in the log
    seconds_since_leeway_note: float = LEEWAY_NOTE_INTERVAL
    last_thrust_n: float = 0.0  # net thrust of the last substep, for the aback rule
    awa: float = 0.0  # deck-level apparent wind angle computed here, for the helm
    aws: float = 0.0  # deck-level apparent wind speed computed here
    sea_drag: float = 1.0  # the head sea's factor on the resistance this tick (spec M5 §4)
    # the tide's stream this tick, metres a second east and north (package 34), the
    # anchor down, and the ground holding her (`physics/integrate.py`)
    water: tuple[float, float] = (0.0, 0.0)
    at_anchor: bool = False
    aground: bool = False
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
    """The water's resistance to the hull swinging, in newton-metres, opposing `r`.

    Cross-flow force on the lateral plane times its lever, both growing with the length
    (see the constants above): the linear term is proportional to A L^2 u r, the
    quadratic to A L^3 r |r|. A short hull swings freely where a long one is held.
    """
    length2 = hull.length * hull.length
    q_area = 0.5 * units.RHO_WATER * hull.lateral_area * length2
    return -q_area * (C_YAW_LIN * abs(u) * r + C_YAW * hull.length * r * abs(r))


def rudder_aspect_ratio(spec: RudderSpec) -> float:
    """The blade's span squared over its area, from the ship file's `span_m`; a blade
    RUDDER_DEFAULT_ASPECT times as deep as it is broad when the file gives no span."""
    if spec.span_m is None or spec.span_m <= 0.0 or spec.area_m2 <= 0.0:
        return RUDDER_DEFAULT_ASPECT
    return spec.span_m * spec.span_m / spec.area_m2


def rudder_lift_slope(spec: RudderSpec) -> float:
    """Side force per radian of helm on the blade, per unit of dynamic pressure and area:
    Helmbold's slope for the blade's aspect ratio times RUDDER_EFFECTIVENESS."""
    ar = rudder_aspect_ratio(spec)
    return RUDDER_EFFECTIVENESS * 2.0 * math.pi * ar / (2.0 + math.sqrt(ar * ar + 4.0))


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
    q = 0.5 * units.RHO_WATER * hull.spec.rudder.area_m2 * rudder_lift_slope(hull.spec.rudder)
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


def apparent_wind(
    ship: Ship, wind: Wind, water: tuple[float, float] = (0.0, 0.0)
) -> tuple[float, float]:
    """Apparent wind angle (radians, + on the starboard bow) and speed (m/s) on deck:
    the true wind less her motion over the ground, which is her way through the water
    and the water's own (`water`, the tide's stream, package 34)."""
    d = ship.dyn
    wx, wy = wind.vector_at_height(ship.hull.spec.deck_height_m)
    ex, ey = units.heading_vector(d.heading)
    sx = d.u * ex + d.v * ey
    sy = d.u * ey - d.v * ex
    if water != (0.0, 0.0):
        sx += water[0]
        sy += water[1]
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
