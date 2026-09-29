"""One tick of ship motion: sails push, the water answers, the ship moves.

`step(ship, dt, wind)` is the hook the World calls once per game second. It
runs four substeps of a quarter second each. In every substep the sails are
asked what they are doing (`compute_sail_forces`, package 4), the hull adds
its resistance, keel grip, rudder and turning damping (`hull.py`), the
helmsman moves the wheel, and the ship's speeds are advanced first and then
her position and heading from the new speeds (semi-implicit Euler, which is
what keeps the arithmetic from running away). Heel relaxes toward its balance.

After the four substeps the readings a sailor sees are refreshed (speed
through the water, leeway, weather helm) and the log is told of anything
worth a line: settled on the ordered heading, taken aback, leeway changed.
"""

from __future__ import annotations

import math

from freesail import units
from freesail.physics import hull as hp
from freesail.physics.sails import compute_sail_forces, hold_rig, release_rig
from freesail.physics.strain import apply_strain
from freesail.physics.wind import Wind
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode

SUBSTEPS = 4  # per tick (spec §3.1)


def step(ship: Ship, dt: float, wind: Wind) -> None:
    """Advance the ship's motion by one tick of `dt` seconds (normally 1.0)."""
    st = hp.hull_state(ship)
    _notice_helm_orders(ship, st)
    h = dt / SUBSTEPS
    # the seaway (spec M5 §4, `physics.motion`): the hull's added resistance in a head
    # sea, a factor read once a tick; 1.0 without a sea
    motion = ship.extra.get("motion")
    st.sea_drag = motion.resistance_factor if motion is not None else 1.0
    # the rig is read once for the four substeps (package 29's profile; `sails._Rig` says
    # why nothing it holds can change between them)
    hold_rig(ship)
    try:
        for _ in range(SUBSTEPS):
            forces = compute_sail_forces(ship, wind)
            st.awa, st.aws = hp.apparent_wind(ship, wind)
            _substep(
                ship,
                st,
                h,
                forces.thrust_n,
                forces.side_n,
                forces.heel_moment_nm,
                forces.yaw_moment_nm,
            )
            st.last_thrust_n = forces.thrust_n
    finally:
        release_rig(ship)
    apply_strain(ship, dt)  # package 9: wear and carrying away, once per tick (spec §7.5)
    _update_readings(ship)
    _log_notes(ship, st, dt)


def _substep(
    ship: Ship,
    st: hp.HullState,
    h: float,
    thrust_n: float,
    side_n: float,
    heel_moment_nm: float,
    yaw_moment_nm: float,
) -> None:
    """One quarter-second of motion under the given sail forces."""
    d = ship.dyn
    hull = ship.hull

    # -- the helmsman moves the wheel -----------------------------------------
    d.rudder = hp.steer(ship, h)
    rudder_side, rudder_yaw = hp.rudder_forces(hull, d.u, d.rudder)

    # -- speeds: driving forces explicitly, the water's damping implicitly -------
    # Each damping is written as a rate D so that force = -D * speed and the
    # update is speed / (1 + D h / m): this cannot overshoot or reverse the
    # motion however hard the water pushes, which a plain explicit step would.
    m_u, m_v, i_z = hp.surge_mass(hull), hp.sway_mass(hull), hp.yaw_inertia(hull)

    drag_u = _rate(hp.resistance(hull, d.u, d.heel) * st.sea_drag, d.u)
    drag_v = _rate(hp.sway_damping(hull, d.u, d.v), d.v)
    drag_r = _rate(hp.yaw_damping(hull, d.u, d.r), d.r)

    # Body-axis kinematics: as the bow swings, the water the ship is moving
    # through does not swing with it (the m v r and -m u r terms, with the
    # ship's own mass m, not the water she carries along).
    m = hull.spec.displacement_kg
    u_new = (d.u + (thrust_n + m * d.v * d.r) / m_u * h) / (1.0 + drag_u * h / m_u)
    v_new = (d.v + (side_n + rudder_side - m * d.u * d.r) / m_v * h) / (1.0 + drag_v * h / m_v)
    r_new = (d.r + (yaw_moment_nm + rudder_yaw) / i_z * h) / (1.0 + drag_r * h / i_z)

    # Clamp sway so a becalmed ship cannot skate sideways (spec §7.4).
    v_limit = hp.SWAY_CLAMP_SLOPE * abs(u_new) + hp.SWAY_CLAMP_OFFSET
    v_new = max(-v_limit, min(v_limit, v_new))

    d.u, d.v, d.r = u_new, v_new, r_new

    # -- position and heading from the new speeds ------------------------------
    ex, ey = units.heading_vector(d.heading)
    d.x += (d.u * ex + d.v * ey) * h
    d.y += (d.u * ey - d.v * ex) * h
    d.heading = units.wrap_2pi(d.heading + d.r * h)

    # -- heel settles toward its balance -------------------------------------------
    target = hp.equilibrium_heel(hull, heel_moment_nm, side_n)
    d.heel = hp.relax_heel(d.heel, target, h)

    # -- weather helm reading (averaged rudder, signed by the tack) -------------
    d.weather_helm = hp.weather_helm_reading(d.weather_helm, d.rudder, st.awa, h)


def _rate(opposing_force: float, speed: float) -> float:
    """The damping rate D >= 0 such that `opposing_force == -D * speed`."""
    if abs(speed) < 1e-9:
        return 0.0
    return max(0.0, -opposing_force / speed)


def _notice_helm_orders(ship: Ship, st: hp.HullState) -> None:
    """Start counting afresh when a new helm order arrives."""
    d = ship.dyn
    if st.last_helm_mode is None:
        # first tick: a ship that starts steady has nothing to report
        st.steady_noted = d.steady
        st.last_helm_mode = d.helm_mode
        st.last_target_heading = d.target_heading
        return
    new_order = (
        d.helm_mode is not st.last_helm_mode
        or (d.helm_mode is HelmMode.HEADING and d.target_heading != st.last_target_heading)
        or (not d.steady and st.steady_noted)
    )
    if new_order:
        st.seconds_on_course = 0.0
        st.steady_noted = False
        if d.helm_mode is not st.last_helm_mode:
            st.helm_integral = 0.0
    st.last_helm_mode = d.helm_mode
    st.last_target_heading = d.target_heading


def _update_readings(ship: Ship) -> None:
    d = ship.dyn
    d.speed = math.hypot(d.u, d.v)
    # leeway means something only when she has way on: a ship drifting broadside
    # under bare poles has no course to make leeway from
    d.leeway = math.atan2(d.v, d.u) if abs(d.u) >= hp.LEEWAY_MIN_SPEED else 0.0


def _log_notes(ship: Ship, st: hp.HullState, dt: float) -> None:
    d = ship.dyn

    # helm.steady: settled within 2 degrees of the ordered heading for 20 s, once per order
    err = hp.heading_error(ship, st)
    if err is not None and not st.steady_noted:
        if abs(err) <= hp.STEADY_TOLERANCE:
            st.seconds_on_course += dt
        else:
            st.seconds_on_course = 0.0
        if st.seconds_on_course >= hp.STEADY_SECONDS:
            st.steady_noted = True
            d.steady = True
            if d.helm_mode is HelmMode.HEADING:
                text = f"Steady on {units.format_heading(d.target_heading)}."
            else:
                text = (
                    f"Steady, full and by, the wind {units.rad_to_deg(abs(st.awa)):.0f}° "
                    f"on the {'starboard' if st.awa >= 0 else 'larboard'} bow."
                )
            ship.note(
                "routine",
                "helm.steady",
                text,
                data={"heading": d.heading, "rudder": d.rudder, "weather_helm": d.weather_helm},
            )

    # ship.aback: thrust astern for 10 s with sail set, unless she is deliberately
    # in stays (a whole-ship evolution such as a tack or a heave-to is in progress).
    # Sails pressed against the masts means a square sail backed, or nothing set
    # drawing at all; the windage of canvas still being set while the jibs draw
    # is not being taken aback (truth 17: getting under way).
    set_sails = [s for s in ship.sails.values() if s.is_set]
    sail_set = bool(set_sails)
    pressed = any(s.backed for s in set_sails) or not any(s.thrust_kn > 0 for s in set_sails)
    runner = ship.extra.get("evolutions")
    in_stays = "hove_to" in ship.extra or (
        bool(runner) and any(e.get("subject") in ("ship", ship.name) for e in runner.in_progress())
    )
    if sail_set and pressed and st.last_thrust_n < 0 and not in_stays:
        st.seconds_aback += dt
    else:
        st.seconds_aback = 0.0
        st.aback_noted = False
    if st.seconds_aback >= hp.ABACK_SECONDS and not st.aback_noted:
        st.aback_noted = True
        ship.note(
            "urgent",
            "ship.aback",
            "Taken aback: the sails pressed against the masts and she lost her way.",
            data={"thrust_n": st.last_thrust_n, "speed": d.speed},
        )

    # on her beam ends: heel beyond 40 degrees, once per episode
    if abs(d.heel) >= hp.BEAM_ENDS_HEEL:
        if not st.beam_ends_noted:
            st.beam_ends_noted = True
            side = "starboard" if d.heel > 0 else "larboard"
            ship.note(
                "urgent",
                "ship.beam_ends",
                f"On her beam ends, {units.rad_to_deg(abs(d.heel)):.0f}° to {side}; "
                "she would not have come up again.",
                data={"heel": d.heel},
            )
    else:
        st.beam_ends_noted = False

    # leeway: a routine line when it changes by more than a degree, at most once a minute,
    # and only with way on (hull.WAY_ON_KN of headway): gathering way from rest or making
    # sternway, leeway is not a reading (playtest 1: "Leeway 145°" from a standing start)
    st.seconds_since_leeway_note += dt
    if (
        d.u >= units.knots_to_ms(hp.WAY_ON_KN)
        and abs(d.leeway - st.last_noted_leeway) > hp.LEEWAY_NOTE_THRESHOLD
        and st.seconds_since_leeway_note >= hp.LEEWAY_NOTE_INTERVAL
    ):
        st.last_noted_leeway = d.leeway
        st.seconds_since_leeway_note = 0.0
        deg = abs(units.rad_to_deg(d.leeway))
        if deg < 0.5:
            text = "Leeway nil."
        else:
            text = f"Leeway {deg:.0f}° to {'starboard' if d.leeway > 0 else 'larboard'}."
        ship.note("routine", "ship.leeway", text, data={"leeway": d.leeway, "speed": d.speed})
