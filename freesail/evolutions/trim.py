"""Tending the sheets of fore-and-aft sails between orders.

A watch on deck does not leave a jib or a spanker sheeted as it was when
set; as the ship's heading or the wind changes they ease or haul the sheet
to keep the sail drawing. Until the crew system (milestone 3) does this as
work, this module does it as a slow automatic adjustment: each set
fore-and-aft sail's sheet angle drifts toward the trim for the present
apparent wind at a modest rate. Square sails are not touched; bracing yards
is always an explicit order.

Milestone 3b adds the trim of the yards between the masts (spec 3b §2.2):
on a wind the after yards are braced sharper than the head yards, so that
all the sails touch together. `stagger` gives the angles; the trim order,
`brace sharp up` on the whole ship and the tack's final trim call it, and
read `AFTER_YARDS_SHARPER_DEG` and `EASE_HEAD_YARDS` from this module when
they do, so a test may change either for one scenario.
"""

from __future__ import annotations

import math

from freesail import units
from freesail.ship.graph import Ship
from freesail.ship.parts import Spar

# Head and after yards on a wind. Fincham 1843, art. 94: "it will be found commonly the
# case, that the after-yards are braced sharper up than the fore-yards; which, by the
# stream of the wind being brought more a-head before it strikes the after-sails,
# produces an effect nearly the same as if the sails were in planes parallel to each
# other, when the whole of them are so trimmed as just to touch at the same time".
# Art. 96 gives the reverse: with increased way, little sea and a ship griping, "brace
# the head-yards sharper than the after-yards" (the `head yards sharper` modifier).
# Fincham gives no figure in art. 94; three degrees is spec 3b §2.2's, and it is the
# difference at the sharp end of Hardy's long ships' ranges in art. 102 (main yards
# braced 23 to 29 degrees from the keel, fore yards 26 to 30).
AFTER_YARDS_SHARPER_DEG = 3.0

# Whether the head yards are eased to make the difference when the after yards can
# come no sharper. Off, judgement from measurement (package 21): Fincham's reason for
# the practice is that the head sails bend the stream so that the after sails meet the
# wind more ahead (art. 94), and the sail model has no such headed stream: every sail
# meets the same apparent wind. So easing the head yards only loses way: the frigate
# made 4.72 knots at 66 degrees off the wind against 4.88 with every yard at its
# limit, and milestone 2's truths 8, 10, 12 and 19 failed. With it off, on a wind the
# after yards stand as much sharper as their rigging allows beyond the head yards (the
# re-sourced limits of Fincham art. 102 put the main yard two degrees beyond the fore;
# the catharpins more), and the log names the difference. Turn it on when the sail
# model heads the after sails' wind.
EASE_HEAD_YARDS = False

# The spar a yard is slung on, as its level for pairing yards across masts: the
# course yards and the crossjack on the lower masts, the topsail yards on the
# topmasts, and so on.
_LEVELS = ("mast", "topmast", "topgallant_mast", "royal_mast")


def _level(ship: Ship, yard: Spar) -> str:
    parent = ship.parent_of(yard)
    return parent.cls if parent is not None else ""


def stagger(
    ship: Ship, targets: dict[str, float], head_sharper: bool = False
) -> tuple[dict[str, float], float | None]:
    """Stagger the sharp-up angles of yards braced together on a wind.

    `targets` maps yard ids to unsigned angles from square (radians), each already
    within its yard's limit: what each yard would be braced to alone. The head yards
    are the yards on the foremost mast among them, the after yards those on the others.
    Each after yard is braced up to `AFTER_YARDS_SHARPER_DEG` beyond the head yard of
    its level, as far as its own limit allows; it is never braced less sharp than its
    target for this. Only with `EASE_HEAD_YARDS` is a head yard eased to make up what
    the after yards' rigging will not give, against the main yard of its level (the
    after mast nearest the head). With `head_sharper` it is the after yards that are
    eased, to that much less than the head yard of their level (art. 96). A mizzen yard
    whose own limit is below the head yards' is left at it.

    Returns the new targets and the difference the log names: the main yard's angle
    less the head yard's at the lowest level both have, in degrees (negative with the
    head yards sharper), or None when the yards are all on one mast.
    """
    step = units.deg_to_rad(AFTER_YARDS_SHARPER_DEG)
    out = dict(targets)
    limits = {yid: ship.spars[yid].brace_limit for yid in targets}
    masts: dict[str, Spar] = {}
    by_level: dict[tuple[str, str], str] = {}
    for yid in targets:
        yard = ship.spars[yid]
        mast = ship.mast_of(yard)
        if mast is None:
            continue
        masts[mast.id] = mast
        by_level.setdefault((mast.id, _level(ship, yard)), yid)
    if len(masts) < 2:
        return out, None
    head = max(masts.values(), key=lambda m: m.x_m)
    main = max((m for m in masts.values() if m is not head), key=lambda m: m.x_m)
    for (mast_id, level), yid in by_level.items():
        if mast_id == head.id:
            continue
        ref = by_level.get((head.id, level))
        if ref is None:
            continue
        if head_sharper:
            out[yid] = max(0.0, min(out[yid], out[ref] - step))
        elif out[yid] < out[ref] + step:
            out[yid] = max(out[yid], min(limits[yid], out[ref] + step))
    if EASE_HEAD_YARDS and not head_sharper:
        for (mast_id, level), yid in by_level.items():
            ref = by_level.get((main.id, level))
            if mast_id == head.id and ref is not None:
                out[yid] = max(0.0, min(out[yid], out[ref] - step))
    for level in _LEVELS:
        h, m = by_level.get((head.id, level)), by_level.get((main.id, level))
        if h is not None and m is not None:
            return out, units.rad_to_deg(out[m] - out[h])
    return out, None


def difference_words(diff_deg: float | None) -> str:
    """'the after yards three degrees sharper', for the log; '' for yards on one mast."""
    if diff_deg is None:
        return ""
    n = int(round(abs(diff_deg)))
    if n == 0:
        return "the head and after yards alike"
    words = ("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    count = words[n] if n < len(words) else str(n)
    degrees = "degree" if n == 1 else "degrees"
    which = "after" if diff_deg > 0 else "head"
    return f"the {which} yards {count} {degrees} sharper"


def signed(targets: dict[str, float], sign: float) -> dict[str, float]:
    """The unsigned targets with the tack's sign: + braced up for the starboard tack."""
    return {k: math.copysign(v, sign) if v else 0.0 for k, v in targets.items()}


SHEET_RATE = units.deg_to_rad(1.0)  # radians per second the hands can work a sheet
# chord angle = apparent wind angle minus this, per class, clamped to the range
TRIM_OFFSET = {
    "gaff": units.deg_to_rad(25.0),
    "jibheaded": units.deg_to_rad(28.0),
    "lug": units.deg_to_rad(25.0),
    "lateen": units.deg_to_rad(25.0),
    "sprit": units.deg_to_rad(25.0),
}
TRIM_RANGE = {
    "gaff": (units.deg_to_rad(18.0), units.deg_to_rad(85.0)),
    "jibheaded": (units.deg_to_rad(15.0), units.deg_to_rad(60.0)),
    "lug": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
    "lateen": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
    "sprit": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
}


def wanted_sheet_angle(cls: str, apparent_wind_angle: float) -> float:
    lo, hi = TRIM_RANGE[cls]
    return max(lo, min(hi, abs(apparent_wind_angle) - TRIM_OFFSET[cls]))


def tend_sheets(ship: Ship, dt: float) -> None:
    """Move every set fore-and-aft sail's sheet toward its trim, a little per tick."""
    awa = ship.dyn.apparent_wind_angle
    if ship.dyn.apparent_wind_speed < 0.5:
        return
    step = SHEET_RATE * dt
    for sail in ship.sails.values():
        if not sail.is_set or not sail.is_fore_and_aft:
            continue
        wanted = wanted_sheet_angle(sail.cls, awa)
        delta = wanted - sail.sheet_angle
        if abs(delta) <= step:
            sail.sheet_angle = wanted
        else:
            sail.sheet_angle += step if delta > 0 else -step
