"""The trim of the sails: the yards' stagger, and the sheet that holds a sail's angle.

Milestone 3b's part (spec 3b §2.2): on a wind the after yards are braced sharper than
the head yards, so that all the sails touch together. `stagger` gives the angles; the
trim order, `brace sharp up` on the whole ship and the tack's final trim call it, and
read `AFTER_YARDS_SHARPER_DEG` and `EASE_HEAD_YARDS` from this module when they do, so a
test may change either for one scenario.

Package 32e's part (spec M5 open item 13): **the sheet holds the trim.** A fore-and-aft
sail's angle from the centreline is a reading of its sheet, never a number of its own:
the sheet's length hauled, through the boom's geometry (the boom's length, the breadth of
the horse its sheet travels on, the purchase's parts) or a loose-footed sail's clew's
travel, gives the angle (`SheetGeometry`); `read_sheet` reads a sail's sheets and says
where the sail lies (which side, at what angle, or flogging with its sheet let fly);
`set_sheet_angle` works the sheet to the length an angle needs, for the orders and the
evolutions that lay hands on it. The free tending that this module did until package
32e (`tend_sheets`, a degree a second every tick with no hands and no log line; the cold
review's finding 3) is retired: the sheets are worked by the level-0 line orders, by
`trim the <sail>` (an evolution with hands and time, `data/evolutions/trim_*_sheet.yaml`)
and by the starter book's tending routine at a cadence. `wanted_sheet_angle` is the
trim a sail wants for the apparent wind, which the trim evolution works the sheet to.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from freesail import units
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, LineState, Sail, Spar

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


# The trim a sail wants for the wind: chord angle = apparent wind angle minus this, per
# class, clamped to the range. The offsets are the sail classes' best angle of attack
# (package 10); the floors are what a boom on a horse and a jib's sheet lead allow (package
# 10's change 6: gaff 18 degrees, jib 15; the schooner held three knots at 40 degrees off
# the true wind with the mainsail sheeted to 8), the ceilings a sail squared off before the
# wind (truth 13). The sheet's geometry runs between the floor (flat aft) and the ceiling
# (eased right off).
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

# A loose-footed sail's clew swings about the tack on a foot of 0.8 of the square root
# of the area (the proxy the sail's lateral offset in physics/sails.py uses for a sail with
# no boom); its sheet leads from the clew to a block on the deck a fathom abaft where the
# clew stands with the sail at its floor angle, and abreast of it: the lead a rigger gives
# so that the sheet hauled aft flattens the sail to its floor and no further (judgement;
# the head sheets lead to the bows' and the gangways' cavils, the staysails' to the rail).
# A boom whose file gives no horse takes a horse a quarter of its own length (judgement).
LOOSE_FOOTED_FOOT_FACTOR = 0.8
LOOSE_FOOTED_LEAD_AFT_M = 1.8288
DEFAULT_HORSE_FRACTION_OF_BOOM = 0.25
FATHOM_M = 1.8288  # six feet: a fathom of the fall hauled or eased


def wanted_sheet_angle(cls: str, apparent_wind_angle: float) -> float:
    """The angle a sail of this class wants for the apparent wind, radians."""
    lo, hi = TRIM_RANGE[cls]
    return max(lo, min(hi, abs(apparent_wind_angle) - TRIM_OFFSET[cls]))


@dataclass(frozen=True)
class SheetGeometry:
    """How a sheet's length sets its sail's angle, and what lever it holds the sail by.

    A boomed sail (`boomed`): the boom of length `arm_m` swings about the mast; its end
    stands `height_m` above the horse, an iron rod of breadth `2 * offset_m` across the
    deck under the boom's end when the boom is amidships (Steel 1794 vol. I, p. 167,
    HORSE); the sheet's traveller runs to the lee end of the horse as the boom goes out,
    and the sheet's length from the traveller to the boom's end, times the purchase's
    `parts`, is the fall's scope. A loose-footed sail: the clew swings about the tack on
    the foot `arm_m`, and the sheet leads to a block on the deck `lead_aft_m` abaft the
    clew's place at the floor angle and `offset_m` off the centreline (abreast of that
    place). The sail's angle runs from `floor`
    (the sheet flat aft, `hauled` 1) to `ceiling` (eased right off, `hauled` 0), and the
    length between is the scope a fathom of fall is counted against.
    """

    floor: float
    ceiling: float
    arm_m: float
    offset_m: float
    height_m: float
    parts: int
    boomed: bool
    lead_aft_m: float = 0.0

    def _end(self, angle: float) -> tuple[float, float]:
        """The boom's end (or the clew), aft and to the side of the mast (or the tack)."""
        return -self.arm_m * math.cos(angle), self.arm_m * math.sin(angle)

    def _block(self, angle: float) -> tuple[float, float]:
        _ex, ey = self._end(angle)
        if self.boomed:
            return -self.arm_m, min(self.offset_m, ey)
        return -self.arm_m * math.cos(self.floor) - self.lead_aft_m, self.offset_m

    def sheet_length(self, angle: float) -> float:
        """Metres of fall out between the block and the boom's end or the clew."""
        ex, ey = self._end(angle)
        bx, by = self._block(angle)
        return self.parts * math.sqrt((ex - bx) ** 2 + (ey - by) ** 2 + self.height_m**2)

    @property
    def scope_m(self) -> float:
        """The fall between flat aft and eased right off, metres (never under a fathom)."""
        return max(self.sheet_length(self.ceiling) - self.sheet_length(self.floor), FATHOM_M)

    def hauled_from_angle(self, angle: float) -> float:
        angle = max(self.floor, min(self.ceiling, angle))
        out = self.sheet_length(angle) - self.sheet_length(self.floor)
        return max(0.0, min(1.0, 1.0 - out / self.scope_m))

    def angle_from_hauled(self, hauled: float) -> float:
        """The angle whose sheet length is `hauled` of the scope in, by bisection."""
        hauled = max(0.0, min(1.0, hauled))
        if hauled >= 1.0:
            return self.floor
        if hauled <= 0.0:
            return self.ceiling
        wanted = self.sheet_length(self.floor) + (1.0 - hauled) * self.scope_m
        lo, hi = self.floor, self.ceiling
        for _ in range(48):
            mid = 0.5 * (lo + hi)
            if self.sheet_length(mid) < wanted:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def lever_m(self, angle: float) -> float:
        """The sheet's lever about the mast, metres: the perpendicular from the mast to
        the sheet's line, as it holds the boom against the sail's pull."""
        ex, ey = self._end(angle)
        bx, by = self._block(angle)
        sx, sy, sz = bx - ex, by - ey, -self.height_m
        length = math.sqrt(sx * sx + sy * sy + sz * sz)
        if length < 1e-9:
            return 0.0
        return abs(ex * sy - ey * sx) / length


def sheet_geometry(ship: Ship, sail: Sail) -> SheetGeometry:
    """The sheet geometry of a fore-and-aft sail, from the ship file, kept per sail."""
    memo = ship.extra.setdefault("trim.sheet_geometry", {})
    geo = memo.get(sail.id)
    if geo is None:
        floor, ceiling = TRIM_RANGE.get(sail.cls, TRIM_RANGE["gaff"])
        boom = ship.spar_of_role(sail, "boom")
        sheets = ship.sheets_of(sail)
        parts = max((ln.parts for ln in sheets), default=1)
        if boom is not None and boom.length_m > 0.0:
            horse = boom.horse_m
            if horse <= 0.0:
                horse = DEFAULT_HORSE_FRACTION_OF_BOOM * boom.length_m
            geo = SheetGeometry(
                floor, ceiling, boom.length_m, 0.5 * horse, max(boom.height_m, 0.0), parts, True
            )
        else:
            foot = LOOSE_FOOTED_FOOT_FACTOR * math.sqrt(max(sail.area_m2, 1.0))
            offset = foot * math.sin(floor)
            geo = SheetGeometry(
                floor, ceiling, foot, offset, 0.0, parts, False, LOOSE_FOOTED_LEAD_AFT_M
            )
        memo[sail.id] = geo
    return geo


@dataclass(frozen=True)
class SheetReading:
    """Where a fore-and-aft sail lies, as its sheets hold it: its angle from the
    centreline; the side it lies on (+1 starboard, -1 larboard; None with no sheet
    belayed); whether it is held on the weather side (aback by the sheet); whether its
    sheets are all let fly (flogging); and the sheet doing the work, if one is."""

    angle: float
    side: float | None
    held_to_windward: bool
    free: bool
    working: Line | None


def lee_side_sign(ship: Ship) -> float:
    """The lee side as the deck reads the apparent wind: +1 starboard, -1 larboard."""
    return -1.0 if ship.dyn.apparent_wind_angle >= 0.0 else 1.0


def side_name(sign: float) -> str:
    return "starboard" if sign > 0 else "larboard"


def read_sheet(ship: Ship, sail: Sail) -> SheetReading:
    """Read a fore-and-aft sail's sheets: the one truth of its trim (spec M5 open item 13).

    A sail with a sheet each side lies on the side whose sheet is hauled and belayed (the
    tighter of two), at that sheet's angle; a boomed sail with one sheet lies to leeward,
    or on the side its sheet is held over to; with no sheet belayed it flogs. A sail with
    no sheet at all in the file keeps the angle it has.
    """
    all_sheets = ship.sheets_of(sail)
    if not all_sheets:
        return SheetReading(sail.sheet_angle, None, False, False, None)
    lee = lee_side_sign(ship)
    geo = sheet_geometry(ship, sail)
    belayed = [ln for ln in all_sheets if ln.state is LineState.BELAYED]
    if not belayed:
        return SheetReading(sail.sheet_angle, None, False, True, None)
    sided = [ln for ln in belayed if ln.side is not None]
    if sided:
        lee_name = side_name(lee)
        working = max(sided, key=lambda ln: (ln.hauled, ln.side == lee_name))
        side = 1.0 if working.side == "starboard" else -1.0
        angle = geo.angle_from_hauled(working.hauled)
        return SheetReading(angle, side, side != lee, False, working)
    working = belayed[0]
    if working.held_side is not None:
        side = 1.0 if working.held_side == "starboard" else -1.0
    else:
        side = lee
    angle = geo.angle_from_hauled(working.hauled)
    return SheetReading(angle, side, side != lee, False, working)


def refresh_reading(ship: Ship, sail: Sail) -> SheetReading:
    """Read the sheets and write the sail's `sheet_angle` reading from them."""
    reading = read_sheet(ship, sail)
    if not reading.free:
        sail.sheet_angle = reading.angle
    return reading


def working_sheet(ship: Ship, sail: Sail, side: str | None = None) -> Line | None:
    """The sheet that holds this sail on `side` ('starboard', 'larboard', 'weather',
    'lee' or None for the lee side): of a pair, that side's; a single sheet, itself."""
    sheets = [ln for ln in ship.sheets_of(sail) if ln.state is not LineState.PARTED]
    if not sheets:
        return None
    if sheets[0].side is None:
        return sheets[0]
    lee = side_name(lee_side_sign(ship))
    weather = "larboard" if lee == "starboard" else "starboard"
    wanted = {None: lee, "lee": lee, "weather": weather}.get(side, side)
    for ln in sheets:
        if ln.side == wanted:
            return ln
    return None


def set_sheet_angle(ship: Ship, sail: Sail, angle: float, side: str | None = None) -> float:
    """Work the sheet to the length this angle needs and belay it: the sail lies on
    `side` (the lee side unless said; 'weather' holds it to windward). Of a pair the
    other sheet is let go; a single sheet is held over when the side is not the lee.
    With `side` 'either', or with no side said before the deck has read a wind, both
    sheets of a pair are belayed alike and the sail lies to leeward of whatever wind
    comes (`read_sheet`'s tie goes to the lee sheet): the state a sail is set in before
    the first tick. Returns the angle the sheet gives (the class's floor at least, its
    ceiling at most)."""
    geo = sheet_geometry(ship, sail)
    angle = max(geo.floor, min(geo.ceiling, angle))
    no_reading = ship.dyn.apparent_wind_angle == 0.0 and ship.dyn.apparent_wind_speed == 0.0
    if side == "either" or (side is None and no_reading):
        hauled = geo.hauled_from_angle(angle)
        for ln in ship.sheets_of(sail):
            if ln.state is not LineState.PARTED:
                ln.hauled = hauled
                ln.state = LineState.BELAYED
                ln.held_side = None
        refresh_reading(ship, sail)
        return angle
    line = working_sheet(ship, sail, side)
    if line is None:
        sail.sheet_angle = angle
        return angle
    line.hauled = geo.hauled_from_angle(angle)
    line.state = LineState.BELAYED
    if line.side is None:
        lee = side_name(lee_side_sign(ship))
        weather = "larboard" if lee == "starboard" else "starboard"
        line.held_side = {None: None, "lee": None, "weather": weather, lee: None}.get(side, side)
    else:
        for other in ship.sheets_of(sail):
            if other is not line and other.state is LineState.BELAYED:
                other.state = LineState.FREE
                other.hauled = 0.0
    refresh_reading(ship, sail)
    return angle


def angle_words(angle: float) -> str:
    """'24° off the centreline', for the log."""
    deg = units.rad_to_deg(abs(angle))
    return "amidships" if deg < 0.5 else f"{deg:.0f}° off the centreline"
