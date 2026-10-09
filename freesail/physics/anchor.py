"""The anchor and the cable in the physics (package 34; spec M5 §18; decision 30).

At anchor the ship is free in the water: the stream (`ship.extra["water"]`, the tide's
velocity over the ground, `world/tide.py`) and the wind on her hull and rig move her as
they move a ship under way, and the cable pulls at the hawse. The anchor lies where it
was let go, in the ship's own plane (`Anchor.ground_x`, `ground_y`, metres east and north
of the start), with the water over it the chart's depth and the tide (`Anchor.depth_m`,
which the World keeps up each minute); the cable runs straight from the hawse to it. While
the hawse is within the cable's reach the cable is slack and she rides by the bight of it
(Luce 1866 ch. XXXIV, p. 574: "the vessel will swing without passing over her anchor,
riding by the bight of the cable"); past it the cable comes taut and pulls, a spring of
hemp: the breaking strain stretches it by a seventh to a fifth (Luce 1866, ch. IV, 'Rope',
the Book of Allowances' note: "It stretches from one seventh to one fifth ... before
breaking"), so its stiffness is the breaking strain over `CABLE_STRETCH_FRACTION` of the
scope out, and a little of hemp's own damping is added (judgement) so that she does not
surge on it for ever. The pull is applied at the hawse, half the waterline forward of the
centre, so its athwartships part swings her head to the pull: that is how she rides head
to wind and tide, and why she sheers about at the turn.

The holding: the pull on the anchor along the ground, against what it holds. An
Admiralty-pattern anchor holds some four times its weight in good ground (judgement,
`HOLDING_PER_WEIGHT`: a modern figure for the old pattern, not the period's, which judged
holding by the ship dragging and by the ground; Falconer 1780, ANCHOR-ground: "neither
too deep, too shallow, nor rocky"), less by the ground's kind (Steel 1794 vol. II, p.
292: in soft and oozy ground "anchors will not hold securely, but come home with little
wind"; in hard and rocky ground they "cannot have much hold"), and less as the cable's
angle at the anchor rises on a short scope (Lever 1808, 'Single Anchor', p. 97: with a
short scope "the angle between the cable and the surface of the bottom is rendered more
obtuse ... its effort is to lift the anchor upwards"; Luce 1866 ch. XXXIV, p. 568: "the
old rule for giving the proper scope to ride by, was three times the depth of water; but
a far safer rule would be five or even six times the depth"). When the pull exceeds the
holding the anchor drags: it is moved along the bottom toward the ship until the cable's
pull is what it holds, and `Anchor.dragging` is set for the World to say so. The cable's
tension is judged against its rating as every line is (spec §7.5, `physics/strain.py`'s
rule and constants): it wears above the rating, warns, and parts above half the breaking
strain by the strain stream's draw, when she is adrift.

Everything here is SI inside: metres, newtons, radians, seconds.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.physics import strain
from freesail.ship.graph import Ship
from freesail.ship.parts import Anchor, AnchorState, GroundTackle

__all__ = [
    "CABLE_DAMPING_FRACTION",
    "CABLE_STRETCH_FRACTION",
    "DRAGGING_HOLD_FRACTION",
    "DRAG_HOLDS_AGAIN_S",
    "DRAG_REPORT_MIN_M",
    "DRAG_REPORT_S",
    "DRAG_SAY_S",
    "DRAG_SETTLE_S",
    "GROUND_HOLDING",
    "HAWSE_FRACTION",
    "HOLDING_PER_WEIGHT",
    "RIDING_SCOPE_PER_DEPTH",
    "SHORT_SCOPE_PER_DEPTH",
    "SHORT_STAY_SCOPE_PER_DEPTH",
    "TRIP_ANGLE_DEG",
    "cable_forces",
    "ground_factor",
    "judge_cables",
    "scope_wanted_m",
]

# What an anchor holds in good ground, as a multiple of its weight: judgement (a modern
# figure for the Admiralty pattern, which held poorly beside a patent anchor; the
# period's texts give no number).
HOLDING_PER_WEIGHT = 4.0
# The ground's share of that, by the words of the chart's bottom note (judgement on Steel
# 1794 vol. II p. 292 and Falconer 1780, ANCHOR-ground; the words are the notes' own).
GROUND_HOLDING: tuple[tuple[str, float], ...] = (
    ("rock", 0.3),
    ("stone", 0.4),
    ("ooze", 0.5),
    ("oozy", 0.5),
    ("weed", 0.6),
    ("shell", 0.6),
    ("gravel", 0.7),
    ("mud", 0.8),
    ("clay", 1.0),
    ("sand", 1.0),
    ("good ground", 1.0),
)
DEFAULT_GROUND_HOLDING = 0.9
# The cable's angle at the anchor at which it lifts the fluke out: judgement on Lever's
# words (above); the holding falls in a straight line from the horizontal to this.
TRIP_ANGLE_DEG = 35.0
# An anchor lifted past its tripping angle, or dragging on its side, still holds this
# part of its full holding (judgement: a quarter, about its own weight in good ground;
# an anchor coming home is not a free weight on the bottom).
DRAGGING_HOLD_FRACTION = 0.25
# And only once it has been coming home for this long (judgement: a minute; the snub as
# she is brought up moves the anchor a fathom in seconds and is not a drag), and it holds
# again once it has held this long (judgement: five minutes; an anchor coming home and
# holding by turns as she sheers about is one dragging). `judge_cables` keeps the count
# once a tick from what `cable_forces` did in its substeps.
DRAG_SAY_S = 60.0
DRAG_SETTLE_S = 300.0
# While a dragging goes on the log says how far the anchor has come no oftener than this
# (package 37f; the brief's quarter of an hour), and only if it has come this much further
# since it last said (judgement: two fathoms, more than a snub moves it).
DRAG_REPORT_S = 900.0
DRAG_REPORT_MIN_M = 3.6576
# The log's "holds again" (package 37k; the review's G8, 37f's own note): only when the
# anchor has held this long, a quarter of an hour; an anchor that comes home again within
# it is the same dragging, one urgent line however often it relapses. The physics' flag
# (`Anchor.dragging`, what the reading says now) still falls after DRAG_SETTLE_S.
DRAG_HOLDS_AGAIN_S = 900.0
# The hemp cable's stretch at its breaking strain (Luce 1866, ch. IV: one seventh to one
# fifth); the stiffness follows.
CABLE_STRETCH_FRACTION = 0.15
# Hemp's own damping, as a fraction of critical on the ship's surge mass: judgement, so
# that a ship brought up surges on her cable a few times and settles.
CABLE_DAMPING_FRACTION = 0.2
# The hawse-holes, where the cable leaves the ship: half the waterline forward of the
# centre (the stem; judgement).
HAWSE_FRACTION = 0.5
# The scope to ride by: five times the depth (Luce 1866 ch. XXXIV, p. 568, "a far safer
# rule would be five or even six times the depth"); the old rule of three (the same);
# a short stay, hove in for weighing, a cable and a half the depth (judgement on Luce's
# "the old rule for a short stay was, that the cable should be in a line with the fore
# topmast stay", ch. XXI, which at a frigate's rake is about that).
RIDING_SCOPE_PER_DEPTH = 5.0
SHORT_SCOPE_PER_DEPTH = 3.0
SHORT_STAY_SCOPE_PER_DEPTH = 1.5


def ground_factor(bottom: str) -> float:
    """The holding of a ground by the words of its bottom note: the mean of the grounds it
    names (package 37f; the review of gate 5c's playtests, 10.5). A note of two grounds,
    "rock and mud" in the Goulet, "sand and rock" at Roscoff, was held as the first word
    of the table found in it, which is the worst, bare rock, and the Goulet held a third
    of good ground where the pilot anchors on it. A rule, not a table: `GROUND_HOLDING`
    keeps its figures, each ground named counts once ("ooze" and "oozy" are one), and a
    note that names none of them is `DEFAULT_GROUND_HOLDING`."""
    words = (bottom or "").lower()
    found: dict[str, float] = {}
    for key, factor in GROUND_HOLDING:
        if key in words:
            found.setdefault(key[:3], factor)  # "ooze" and "oozy": one ground
    if not found:
        return DEFAULT_GROUND_HOLDING
    return sum(found.values()) / len(found)


def scope_wanted_m(depth_m: float, per_depth: float = RIDING_SCOPE_PER_DEPTH) -> float:
    """The cable a depth wants, in metres."""
    return per_depth * max(depth_m, 0.0)


def holding_n(anchor: Anchor, angle_rad: float) -> float:
    """What the anchor holds along the ground now, in newtons."""
    lift = max(0.0, 1.0 - math.sin(max(angle_rad, 0.0)) / math.sin(math.radians(TRIP_ANGLE_DEG)))
    lift = max(lift, DRAGGING_HOLD_FRACTION)
    return HOLDING_PER_WEIGHT * anchor.weight_kn * 1000.0 * ground_factor(anchor.bottom) * lift


def hawse_position(ship: Ship) -> tuple[float, float]:
    d = ship.dyn
    lever = HAWSE_FRACTION * ship.hull.length
    return d.x + math.sin(d.heading) * lever, d.y + math.cos(d.heading) * lever


def cable_forces(ship: Ship, water: tuple[float, float], h: float) -> tuple[float, float, float]:
    """The cable's pull on the ship this substep: (ahead N, to starboard N, yaw N m),
    and the anchors' loads, holding and dragging set for the tick."""
    tackle = ship.extra.get("ground_tackle")
    if not isinstance(tackle, GroundTackle):
        return 0.0, 0.0, 0.0
    down = tackle.down()
    if not down:
        return 0.0, 0.0, 0.0
    d = ship.dyn
    hull = ship.hull
    sin_h, cos_h = math.sin(d.heading), math.cos(d.heading)
    lever = HAWSE_FRACTION * hull.length
    hx, hy = d.x + sin_h * lever, d.y + cos_h * lever
    # the hawse's velocity over the ground: the ship's through the water, the water's, and
    # the swing's part at the bow
    vgx = d.u * sin_h + d.v * cos_h + water[0] + d.r * lever * cos_h
    vgy = d.u * cos_h - d.v * sin_h + water[1] - d.r * lever * sin_h
    mass = hull.spec.displacement_kg
    fwd = stb = yaw = 0.0
    for anchor in down:
        if anchor.ground_x is None or anchor.ground_y is None:
            continue
        dx, dy = anchor.ground_x - hx, anchor.ground_y - hy
        dist = math.hypot(dx, dy)
        depth = max(anchor.depth_m, 0.0)
        scope = anchor.scope_m
        length = math.hypot(dist, depth)
        if length <= scope or dist < 1e-6:
            anchor.taut = False
            anchor.cable_load_kn = 0.0
            anchor.holding_kn = holding_n(anchor, math.atan2(depth, max(dist, 1e-6))) / 1000.0
            continue
        ux, uy = dx / dist, dy / dist  # toward the anchor
        theta = math.atan2(depth, dist)
        breaking = strain.CARRY_AWAY_RATIO * anchor.cable_kn * 1000.0
        k = breaking / max(CABLE_STRETCH_FRACTION * scope, 1.0)
        stretch = length - scope
        rate = -(vgx * ux + vgy * uy)  # the hawse drawing away from the anchor
        c = 2.0 * CABLE_DAMPING_FRACTION * math.sqrt(k * mass)
        tension = max(0.0, k * stretch + c * rate)
        pull = tension * math.cos(theta)
        holds = holding_n(anchor, theta)
        anchor.holding_kn = holds / 1000.0
        if anchor.heaving:
            # the capstan heaves the ship up to her anchor: the cable's pull brings her
            # ahead, and the anchor is not said to drag (it is broken out when the cable
            # is up and down, the weigh script's word)
            pass
        elif pull > holds:
            # it drags: the anchor comes toward the ship along the cable's line until the
            # pull along the ground is what it holds
            tension = holds / math.cos(theta)
            stretch_held = max(0.0, (tension - c * max(rate, 0.0)) / k)
            new_dist = math.sqrt(max((scope + stretch_held) ** 2 - depth * depth, 0.0))
            anchor.ground_x = hx + ux * new_dist
            anchor.ground_y = hy + uy * new_dist
            pull = holds
            anchor.came_home = True
            anchor.moved_m += max(0.0, dist - new_dist)  # how far it came, for the log
        anchor.taut = True
        anchor.cable_load_kn = tension / 1000.0
        fx, fy = pull * ux, pull * uy
        a_fwd = fx * sin_h + fy * cos_h
        a_stb = fx * cos_h - fy * sin_h
        fwd += a_fwd
        stb += a_stb
        yaw += a_stb * lever
    return fwd, stb, yaw


def judge_cables(ship: Ship, dt: float) -> None:
    """Once a tick: the drag judged over time (an anchor that has come home for
    DRAG_SAY_S together is dragging, and holds again after DRAG_SETTLE_S holding), and
    the cables of the anchors down against their ratings, by the strain model's rule
    (spec §7.5): worn above the rating, warned once in ten minutes, parted above half the
    breaking strain by the strain stream's draw or when worn out."""
    tackle = ship.extra.get("ground_tackle")
    if not isinstance(tackle, GroundTackle):
        return
    stream = strain._stream(ship, None)
    st = strain.strain_state(ship)
    for anchor in tackle.anchors:
        if not anchor.down or anchor.heaving:
            anchor.dragging = False
            anchor.came_home = False
            anchor.drag_s = anchor.hold_s = 0.0
            anchor.moved_m = anchor.drag_m = 0.0
            continue
        # Package 37f (the review's 10.4): the dragging is one thing from the minute it is
        # judged to have begun until the anchor has held DRAG_SETTLE_S, and how far it has
        # come in that time is kept for the log. It is judged to begin only on a tick in
        # which the anchor moves, so never of an anchor whose cable is slack; and seconds
        # of creeping long past are forgiven as it holds (DRAG_SAY_S of them in
        # DRAG_SETTLE_S), where before they stood until five minutes' holding wiped them
        # all, and an anchor that crept a second in every few minutes was "dragging" in
        # the end with its cable slack.
        if anchor.came_home:
            if anchor.drag_s <= 0.0:
                anchor.drag_m = 0.0  # a new coming home: how far is counted from here
            anchor.drag_s += dt
            anchor.hold_s = 0.0
            anchor.drag_m += anchor.moved_m
            if anchor.drag_s >= DRAG_SAY_S:
                anchor.dragging = True
        else:
            anchor.hold_s += dt
            if anchor.hold_s >= DRAG_SETTLE_S:
                anchor.drag_s = 0.0
                anchor.dragging = False
            elif not anchor.dragging:
                anchor.drag_s = max(0.0, anchor.drag_s - dt * DRAG_SAY_S / DRAG_SETTLE_S)
        anchor.came_home = False
        anchor.moved_m = 0.0
    for anchor in tackle.down():
        ratio = anchor.cable_strain_ratio
        if ratio <= strain.DECAY_RATIO:
            continue
        anchor.cable_condition = max(
            0.0,
            anchor.cable_condition
            - strain.DECAY_POINTS_PER_MINUTE * (ratio - strain.DECAY_RATIO) * dt / 60.0,
        )
        parts = anchor.cable_condition <= 0.0 or (
            stream is not None
            and ratio > strain.CARRY_AWAY_RATIO
            and stream.random() < strain.failure_probability(ratio, dt)
        )
        name = f"{anchor.name} cable"
        if parts:
            anchor.state = AnchorState.LOST
            anchor.cable_load_kn = 0.0
            anchor.taut = False
            anchor.dragging = False
            lost = f"{name[:1].upper()}{name[1:]} parted; the anchor is lost, and she is adrift."
            ship.note(
                "urgent",
                "cable.parted",
                lost,
                subject=anchor.id,
                data={
                    "anchor": anchor.id,
                    "ratio": round(ratio, 2),
                    "scope_fathoms": anchor.scope_fathoms,
                },
            )
            continue
        key = f"cable:{anchor.id}"
        last = st.last_warning_s.get(key)
        if last is not None and st.elapsed_s - last < strain.WARNING_INTERVAL_S:
            continue
        st.last_warning_s[key] = st.elapsed_s
        dire = ratio > strain.CARRY_AWAY_RATIO
        words = (
            "stranding at the hawse; it will not hold much longer: veer more cable, or let go "
            "the second anchor."
            if dire
            else "bar-taut and surging on the bitts."
        )
        ship.note(
            "notable",
            "strain.warning",
            f"{name[:1].upper()}{name[1:]} {words}",
            subject=anchor.id,
            data={
                "ratio": round(ratio, 2),
                "load_kn": round(anchor.cable_load_kn, 1),
                "rating_kn": anchor.cable_kn,
            },
        )


def riding_words(ship: Ship, tide_state: Any, wind_from_rad: float) -> str:
    """How she rides, in the log's words: 'riding to the flood, the wind across the
    tide' (Lever 1808, 'Single Anchor': the leeward tide, the weather tide; Falconer
    1780, RIDING: athwart, between the wind and tide, easy, hard)."""
    tackle = ship.extra.get("ground_tackle")
    riding = tackle.riding_by() if isinstance(tackle, GroundTackle) else None
    by = f" by {riding.name}" if riding is not None else ""
    if tide_state is None or tide_state.slack:
        return f"Riding{by}, head to wind."
    stream = math.radians(tide_state.stream_toward_deg)
    # the tide "from" is the opposite of the way it runs; the wind "from" is given
    between = abs(units.wrap_pi(wind_from_rad - (stream + math.pi)))
    points = units.rad_to_points(between)
    which = "the flood" if tide_state.flood else "the ebb"
    if points < 4.0:
        how = "wind and tide together"  # a leeward tide: both ahead (Lever)
    elif points > 12.0:
        how = "a windward tide, the wind against the tide"
    else:
        how = "the wind across the tide"
    taut = ""
    if riding is not None and riding.taut and riding.cable_strain_ratio > 0.5:
        taut = ", riding hard"
    return f"Riding{by} to {which}, {how}{taut}."
