"""Scripted manoeuvres: tack, wear, heave to and fill away (spec §8.5).

Without a crew model these are timelines. Each script sets the helm targets
in ``ship.dyn`` (``helm_mode``, ``target_heading``, ``target_rudder``) and
moves the yards' ``brace_angle`` over time, then watches what the physics
does with the ship (her heading relative to the true wind, and her speed)
to decide how the manoeuvre ended. The physics is not touched: a script
gives orders and reads the compass, like an officer on deck.

Conventions used here (spec §4 and the package 3 Dynamics):

- ``rel`` is the true wind's bearing relative to the bow, positive when the
  wind is on the starboard side. ``sign`` is +1 on the starboard tack and
  -1 on the larboard tack.
- A yard's ``brace_angle`` is positive when it is braced up for the
  starboard tack (wind from starboard: the starboard yardarm forward, the
  lee yardarm aft) and negative for the larboard tack. So a yard braced
  sharp up on tack ``sign`` sits at ``sign * brace_limit``; braced aback for
  that tack it sits at ``-sign * brace_limit``; square is 0. The limit is
  always read from the spar, never assumed.
- "Close-hauled" for the true wind is six points (67.5 degrees) unless the
  ship carries ``ship.extra["close_hauled_angle"]`` in radians.

The timings each script uses come from the ``timing:`` block of its
evolution file, so they can be tuned without touching this code:

- ``brace_s``: seconds to swing a set of yards round (45 s in the spec).
- ``brace_rate_deg_s``: how fast yards follow the wind when wearing.
- ``stays_timeout_s``: how long a tacking ship may hang in stays, from the
  moment her way is gone, before she has missed stays (package 32e).
- ``way_gone_fraction``, ``way_gone_lengths_per_min``: her way is gone when she
  makes less than this fraction of her speed at "helm's a-lee", or less than
  this many of her own lengths a minute, whichever is the more (package 32e).
- ``steady_deg``, ``steady_timeout_s``: when a manoeuvre counts as steady on
  its new course, and how long to wait for that before giving up waiting.
- ``wear_timeout_s``: how long a wear may take before it is abandoned.
- ``helm_deg``: the rudder angle for "helm a-lee" when heaving to.
- ``seconds_per_m2``, ``min_s``, ``max_s``: a sheet's trim, by the sail's size
  (`TrimSheetScript`, package 32e).

Every script keeps its own ``status`` ("running", "done" or "failed") and,
when failed, a ``reason`` in words that the evolution's ``on_fail`` line
shows.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.evolutions import trim as yard_trim
from freesail.ship import parts
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode, LineState, Sail, SailState, Spar, sync_catharpins
from freesail.ship.schema import YARD_LIKE_CLASSES

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

POINT = units.POINT


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def sharp_up_targets(ship: Ship, head: list[Spar], after: list[Spar]) -> dict[str, float]:
    """Each yard's unsigned angle braced sharp up on a wind, the after yards
    `trim.AFTER_YARDS_SHARPER_DEG` sharper than the head yards where the limits
    allow (spec 3b §2.2, Fincham art. 94; `trim.stagger`): the tack's final trim."""
    sync_catharpins(ship)
    targets, _ = yard_trim.stagger(ship, {y.id: y.brace_limit for y in head + after})
    return targets


def bowlines_hauled(ship: Ship) -> list[str]:
    """The sails whose bowline is hauled out now, in the ship's order (spec 3b §4)."""
    out: list[str] = []
    for line in ship.lines.values():
        if line.bowline_hauled and line.of not in out:
            out.append(line.of)
    return out


def let_go_bowlines(ship: Ship) -> bool:
    """Let go every bowline hauled out, as the yards are swung (Luce 1884, ch. XXIV,
    'Tacking': "The lee braces and the bowlines are let go"). True if any was."""
    any_hauled = False
    for line in ship.lines.values():
        if line.bowline_hauled:
            line.state = LineState.FREE
            line.hauled = 0.0
            any_hauled = True
    return any_hauled


def steady_out_bowlines(ship: Ship, sail_ids: list[str], sign: float) -> bool:
    """Haul out the weather bowline, for the tack `sign` gives (+1 starboard), of each
    sail named that is drawing: "Haul taut the lifts and weather braces! Steady out the
    bo'lines!" (Luce 1884, ch. XXIV, 'Tacking', 'Wearing'). True if any was hauled."""
    side = "starboard" if sign > 0 else "larboard"
    any_hauled = False
    for sid in sail_ids:
        sail = ship.sails.get(sid)
        if (
            sail is None
            or sail.wrecked
            or sail.state not in (SailState.SET, SailState.GOOSE_WINGED)
        ):
            continue
        line = ship.line_of(sail, "bowline", side)
        if line is None or line.state is LineState.PARTED:
            continue
        line.state = LineState.BELAYED
        line.hauled = 1.0
        any_hauled = True
    return any_hauled


# The studding sails in before going about (milestone 3b, spec 3b §7). Luce's tacking and
# wearing begin with them in (RigGeometryNotes §5), and his words for taking them in with
# all hands are "Stand by to take in the stun'sails ...! Haul taut! IN STUN'SAILS ... Rig in
# and get alongside the booms ... make up and stow away the studding-sails" (Luce 1884,
# ch. XXVII, 'Going large under all sail, to round to under single reefs'; ch. XXXIV,
# 'Having a leading wind, to run in and anchor': "Haul taut! IN STUDDING-SAILS"). The time:
# the watch's own evolutions', all at once with all hands: lowered away and hauled down (90
# s, data/evolutions/take_in_studding.yaml) and the booms rigged in (40 s,
# rig_in_studdingsail_boom.yaml); the sails are made up while she goes about.
STUDDING_IN_S = 90.0 + 40.0
BOOMS_IN_S = 40.0  # the booms alone, their sails already in (rig_in_studdingsail_boom.yaml)
_STUDDING_ALOFT = (
    SailState.SET,
    SailState.GOOSE_WINGED,
    SailState.SHEETED,
    SailState.LOOSED,
    SailState.IN_THE_GEAR,
)


def studding_work(ship: Ship) -> tuple[list[Sail], list[Spar]]:
    """The studding sails aloft (set, or on their way up or down) and the booms rigged
    out: what a tack or a wear takes in first. Both empty: nothing to do."""
    sails = [
        s
        for s in ship.sails.values()
        if s.cls == "studding" and not s.wrecked and s.state in _STUDDING_ALOFT
    ]
    booms = [
        b
        for b in ship.spars.values()
        if b.cls in parts.RIGGED_IN_CLASSES and b.rigged_out and not b.wrecked
    ]
    return sails, booms


class StuddingSailsIn:
    """The first all-hands work of a tack or a wear when studding sails are set or their
    booms out: in studding-sails and rig in the booms, then the manoeuvre proper."""

    def __init__(self, ship: Ship):
        self.ship = ship
        self.sails, self.booms = studding_work(ship)
        self.duration_s = STUDDING_IN_S if self.sails else BOOMS_IN_S
        self.progress = 0.0

    @property
    def needed(self) -> bool:
        return bool(self.sails or self.booms)

    def begin_words(self) -> str:
        if self.sails:
            return "Stand by to take in the studding-sails. Haul taut! In studding-sails!"
        return "Rig in and get alongside the studding-sail booms."

    def advance(self, dt: float, factor: float) -> bool:
        """Work on; True when the sails are in and made up and the booms rigged in."""
        self.progress = min(1.0, self.progress + dt / (self.duration_s * factor))
        if self.progress < 1.0 - 1e-9:
            return False
        for sail in self.sails:
            if not sail.wrecked and sail.state in _STUDDING_ALOFT:
                sail.state = SailState.FURLED  # made up and stowed as she goes about
        for boom in self.booms:
            if not boom.wrecked:
                boom.rigged_out = False
        return True

    def end_words(self) -> str:
        if self.sails:
            return "In studding-sails; rigged in and got alongside the booms."
        return "Rigged in the studding-sail booms."

    def remaining_s(self) -> float:
        return (1.0 - self.progress) * self.duration_s


def close_hauled_true_angle(ship: Ship) -> float:
    """The angle off the true wind at which this ship sails close-hauled."""
    return float(ship.extra.get("close_hauled_angle", 6 * POINT))


def head_sails(ship: Ship) -> list[Sail]:
    """The head sails set: jib-headed sails with sheets, forward of the foremost mast (the
    jibs and the fore staysails), in the ship file's order (package 32e)."""
    masts = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    fore_x = max((m.x_m for m in masts), default=0.0)
    return [
        sl
        for sl in ship.sails.values()
        if sl.is_set and sl.cls == "jibheaded" and sl.x_m > fore_x and ship.sheets_of(sl)
    ]


def boom_sails(ship: Ship) -> list[Sail]:
    """The gaff sails set on a boom (a ship's spanker, a fore-and-after's mainsail): the
    sails whose sheet a tack hauls aft and holds over (package 32e)."""
    return [
        sl
        for sl in ship.sails.values()
        if sl.is_set
        and sl.cls == "gaff"
        and ship.spar_of_role(sl, "boom") is not None
        and ship.sheets_of(sl)
    ]


def sheets_to(ship: Ship, sails: list[Sail], side: str | None, angle: float | None) -> None:
    """Work the sheets of these sails to `angle` (their floor when None) on `side`
    ('starboard', 'larboard', 'weather', 'lee' or None for the lee side), at once: the
    hands are at the sheets through a manoeuvre, and the time is the manoeuvre's."""
    for sl in sails:
        geo = yard_trim.sheet_geometry(ship, sl)
        yard_trim.set_sheet_angle(ship, sl, geo.floor if angle is None else angle, side)
        sl.shivering = False


def let_fly_sheets(ship: Ship, sails: list[Sail]) -> None:
    """Let the sheets of these sails run: the sails flog until they are drawn again."""
    for sl in sails:
        for ln in ship.sheets_of(sl):
            if ln.state is LineState.BELAYED:
                ln.state = LineState.FREE
                ln.hauled = 0.0
                ln.held_side = None
        sl.shivering = True


def ease_off_sheets(ship: Ship, sails: list[Sail]) -> None:
    """Ease the sheets of these sails right off, belayed on the lee side: the sails luff
    (a jib eased right off with the wind ahead lies over to leeward and lifts; let fly it
    flogs, with a loose sail's windage all the while, which in the model cost the frigate
    her way in stays and a hundred metres to leeward, package 32e)."""
    for sl in sails:
        geo = yard_trim.sheet_geometry(ship, sl)
        yard_trim.set_sheet_angle(ship, sl, geo.ceiling, None)
        sl.shivering = False


def draw_sheets(
    ship: Ship, sails: list[Sail], side: str | None = None, awa: float | None = None
) -> None:
    """Let these sails draw: each sheet trimmed to the apparent wind (`awa`, radians,
    else the deck's reading now) on `side` (the lee side as the deck reads it when None;
    a manoeuvre that knows the new tack names it, since the deck's reading lags as her
    head passes the wind)."""
    wind = ship.dyn.apparent_wind_angle if awa is None else awa
    for sl in sails:
        yard_trim.set_sheet_angle(ship, sl, yard_trim.wanted_sheet_angle(sl.cls, wind), side)
        sl.shivering = False


def full_and_by_apparent(ship: Ship, wind: Wind, way: float) -> float:
    """The apparent wind angle she will have on the close-hauled course she is coming to
    (`close_hauled_true_angle`) with `way` (m/s) on her: the wind a manoeuvre trims the
    sheets for before she has it (package 32e). The triangle of the true wind and the way
    she carried by the wind before the manoeuvre began (at "helm's a-lee", at "up helm"),
    since in stays she has next to none and the true wind's angle would have the sheets
    eased for a reach: the schooner and the brig were called tacked with their sails
    luffing and under a knot on them. Not the rig's luffing angle of the moment either,
    which reads the yards where they stand: squared, as the wind comes aft in a wear, it
    had the head sheets eased for a wind two points too broad, and the frigate griped up
    and lost her way coming to."""
    beta = close_hauled_true_angle(ship)
    w = max(wind.speed, 0.0)
    v = max(way, 0.0)
    return math.atan2(w * math.sin(beta), w * math.cos(beta) + v)


def shifted_sails(ship: Ship) -> list[Sail]:
    """The fore-and-aft sails set whose sheets are shifted over as she goes about and
    are neither head sails nor boom sails: the staysails abaft the fore mast and a
    schooner's loose-footed foresail, each with a sheet a side (package 32e; Lever
    1808, 'Tacking Expeditiously', p. 78: "all the Staysail Tacks and Sheets abaft the
    Fore Mast are let go, and the latter shifted over the Stays"; Luce 1884, ch. XXXIV,
    'To Wear': "when the wind is aft shift over the boom and head sheets")."""
    heads = {sl.id for sl in head_sails(ship)}
    booms = {sl.id for sl in boom_sails(ship)}
    return [
        sl
        for sl in ship.sails.values()
        if sl.is_set
        and sl.is_fore_and_aft
        and sl.id not in heads
        and sl.id not in booms
        and any(ln.side is not None for ln in ship.sheets_of(sl))
    ]


def shift_sheets_over(ship: Ship, new_lee: str, wind: Wind, way: float) -> None:
    """Shift every set fore-and-aft sail's sheet to the new tack's lee side, trimmed for
    the wind of the course she is coming to with the `way` (m/s) she had before: what a
    wear or a box-haul does as the wind comes aft, and a tack at "let go and haul"
    (package 32e)."""
    sails = head_sails(ship) + boom_sails(ship) + shifted_sails(ship)
    draw_sheets(ship, sails, new_lee, full_and_by_apparent(ship, wind, way))


def innermost_head_sail(ship: Ship, standing: bool = False) -> Sail | None:
    """The head sail nearest the mast (the fore staysail, or the jib if it is alone): the
    sheet a fore-and-after hauls to windward to heave to (Luce 1884, ch. XXXIV). With
    `standing`, of those that are set and not being handed (package 37k)."""
    heads = head_sails(ship)
    if standing:
        heads = [sl for sl in heads if not being_handed(ship, sl)]
    return min(heads, key=lambda sl: sl.x_m) if heads else None


# The evolutions that take a sail in, furl it or unbend it: a sail they are at, in hand
# or waiting for hands, is not one a heave-to lays aback (package 37k).
HANDING_EVOLUTIONS = frozenset(
    {
        "take_in_square",
        "take_in_gaff",
        "take_in_jibheaded",
        "take_in_studding",
        "furl_square",
        "furl_gaff",
        "furl_jibheaded",
        "unbend_sail",
        "shift_sail",
    }
)


def being_handed(ship: Ship, sail: Sail) -> bool:
    """Whether the hands are at taking this sail in, furling or unbending it, or have the
    order to (package 37k; the review's G7, game 10: the officer was hauling down the
    cutter's foresail at the pilot's hail while the captain hove her to; the heave-to
    backed that same foresail, said "Hove to", and she filled within a minute when it
    came down)."""
    runner = ship.extra.get("evolutions")
    for inst in getattr(runner, "instances", None) or ():
        if inst.evo.id in HANDING_EVOLUTIONS and sail.id in (
            inst.subject_id,
            inst.params.get("sail"),
        ):
            return True
    return False


def standing_sail_on(ship: Ship, yards: list[Spar]) -> Sail | None:
    """The first sail on these yards that a heave-to can lay to the mast: set, not being
    handed, and not a course (the heave-to hauls the courses up); or None."""
    courses = {sl.id for sl in lowest_square_sails(ship)}
    for y in yards:
        sail = ship.sail_of(y)
        if (
            sail is not None
            and sail.is_set
            and sail.id not in courses
            and not being_handed(ship, sail)
        ):
            return sail
    return None


def working_yards(ship: Ship) -> list[Spar]:
    """Every yard that can be braced: yard-like, not wrecked, not sent down."""
    return [
        s
        for s in ship.spars.values()
        if s.cls in YARD_LIKE_CLASSES and not s.wrecked and not s.sent_down
    ]


def _masts_with_yards(ship: Ship) -> list[Spar]:
    masts: list[Spar] = []
    for y in working_yards(ship):
        m = ship.mast_of(y)
        if m is not None and m not in masts:
            masts.append(m)
    return masts


def head_and_after_yards(ship: Ship) -> tuple[list[Spar], list[Spar]]:
    """Split the yards into the head yards (on the foremost mast that carries
    yards) and the after yards (all the rest). A ship whose yards are all on
    one mast, like a topsail schooner, has head yards only."""
    masts = _masts_with_yards(ship)
    if not masts:
        return [], []
    foremost = max(masts, key=lambda m: m.x_m)
    head = [y for y in working_yards(ship) if ship.mast_of(y) is foremost]
    after = [y for y in working_yards(ship) if ship.mast_of(y) is not foremost]
    return head, after


def after_square_yards(ship: Ship) -> list[Spar]:
    """The yards on the aftermost mast that carries yards (the mizzen on a
    frigate, the fore on a topsail schooner)."""
    masts = _masts_with_yards(ship)
    if not masts:
        return []
    aftermost = min(masts, key=lambda m: m.x_m)
    return [y for y in working_yards(ship) if ship.mast_of(y) is aftermost]


def yards_to_back(ship: Ship) -> list[Spar]:
    """The yards laid aback to heave to: those on the mast carrying the most
    square sail (Luce 1866 ch. XXVI: "the main topsail to the mast"). On a
    ship-rigged vessel that is the main; on a topsail schooner the fore, being
    the only mast with yards."""
    masts = _masts_with_yards(ship)
    if not masts:
        return []

    def square_area(mast: Spar) -> float:
        return sum(
            sl.area_m2
            for y in working_yards(ship)
            if ship.mast_of(y) is mast
            for sl in [ship.sail_of(y)]
            if sl is not None and sl.cls == "square"
        )

    chosen = max(masts, key=square_area)
    return [y for y in working_yards(ship) if ship.mast_of(y) is chosen]


def yards_to_back_set(ship: Ship) -> list[Spar]:
    """The yards a heave-to lays aback (package 37k): the main's as `yards_to_back` has
    them whenever a sail stands on them, set, not being handed and not a course (Luce's
    "main topsail to the mast"; with the topsail furled and the topgallant set, the
    topgallant); else those of the mast carrying the most square sail that so stands
    (Luce 1866, ch. XXVI, 'To heave to with the fore topsail to the mast'). With no such
    sail, `yards_to_back`'s, and the heave-to refuses in words."""
    masts = _masts_with_yards(ship)

    def standing_area(mast: Spar) -> float:
        yards = [y for y in working_yards(ship) if ship.mast_of(y) is mast]
        return sum(
            sl.area_m2
            for y in yards
            for sl in [ship.sail_of(y)]
            if sl is not None and sl.cls == "square" and sl is standing_sail_on(ship, [y])
        )

    best = max(masts, key=standing_area) if masts else None
    if best is None or standing_area(best) <= 0.0:
        return yards_to_back(ship)
    main = yards_to_back(ship)
    if main and standing_sail_on(ship, main) is not None:
        return main  # the main topsail to the mast, or what stands on the main (Luce)
    return [y for y in working_yards(ship) if ship.mast_of(y) is best]


def after_gaff_sails(ship: Ship) -> list:
    """The driver: gaff sails set on the aftermost lower mast (the spanker of a
    ship; a schooner's mainsail). Hove to with the main topsail aback it is
    brailed up, else it brings her head to wind and she gathers sternway
    (Luce 1866 ch. XXVI: 'regulate by easing off, or hauling aft, the spanker
    and jib sheets'; package 10 found the frigate with the spanker set lies 40
    degrees off with two knots of sternway, brailed up 55 to 60 degrees off
    with almost none). A schooner keeps her mainsail: it is her driving sail,
    not a driver, and without it she pays off broad and forereaches under her
    foresail and jibs (the period way for a fore-and-after is a jib sheet to
    windward, which the sail model cannot yet do)."""
    # Package 32b: the driver is found by place, not by counting masts. It is the gaff
    # sail on the aftermost lower mast when that mast carries square yards and another
    # mast forward of it does too (a ship's mizzen, a brig's main, whose spanker brought
    # the brig head to wind with sternway hove to, as the frigate's did before package
    # 10); a vessel whose yards are all on one mast, the schooner's fore or the cutter's
    # one mast, keeps her gaff sail, which is her driving sail.
    with_yards = _masts_with_yards(ship)
    if len(with_yards) < 2:
        return []
    aftermost = min(with_yards, key=lambda m: m.x_m)
    lower = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    if not lower or min(lower, key=lambda m: m.x_m) is not aftermost:
        return []
    return [
        sl
        for sl in ship.sails.values()
        if sl.cls == "gaff" and sl.is_set and ship.mast_of(sl) is aftermost
    ]


def light_sails_forward_of(ship: Ship, backed: list[Spar]) -> list:
    """The topgallants and royals set on the masts forward of the backed
    yards' mast: the light head sails. Hove to they are clewed up (Luce 1866
    ch. XXVI: 'settle down the top-gallant sails and royals, or clew them
    up'); left set, the fore topgallant drives her ahead at a knot and a half
    and lies her a point too broad (package 10, truth 12)."""
    masts = [ship.mast_of(y) for y in backed]
    if not masts or any(m is None for m in masts):
        return []
    x_backed = max(m.x_m for m in masts)
    out = []
    for sl in ship.sails.values():
        if not (sl.is_set and sl.cls == "square"):
            continue
        yard = ship.yard_of(sl)
        above = ship.parent_of(yard) if yard is not None else None
        mast = ship.mast_of(sl)
        if (
            above is not None
            and above.cls in ("topgallant_mast", "royal_mast")
            and mast is not None
            and mast.x_m > x_backed
        ):
            out.append(sl)
    return out


def names_of_sails(ship: Ship, sails: list) -> str:
    """'the spanker', or 'the foresail and the mainsail', for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    return " and ".join(f"the {part_name(ship, sl.id)}" for sl in sails) if sails else "the sail"


def lowest_square_sails(ship: Ship) -> list:
    """The courses: square sails on yards that hang directly on a lower mast."""
    out = []
    for y in working_yards(ship):
        parent = ship.parent_of(y)
        sl = ship.sail_of(y)
        if parent is not None and parent.cls == "mast" and sl is not None and sl.cls == "square":
            out.append(sl)
    return out


def wind_rel(ship: Ship, wind: Wind) -> float:
    """The true wind's bearing from the bow, positive on the starboard side."""
    return units.relative_bearing(ship.dyn.heading, wind.direction_from)


def estimated_wind_from(ship: Ship) -> float:
    """Where the wind comes from, as the deck reads it before any tick has told
    the script the true wind: heading plus the apparent wind angle."""
    return units.wrap_2pi(ship.dyn.heading + ship.dyn.apparent_wind_angle)


def trim_angle(rel: float, limit: float, close_hauled: float) -> float:
    """The brace angle a yard wants for a given true wind bearing: sharp up
    (the limit) when by the wind, easing to square as the wind comes aft."""
    a = abs(rel)
    if a <= close_hauled:
        fraction = 1.0
    else:
        fraction = (math.pi - a) / (math.pi - close_hauled)
    return math.copysign(limit * fraction, rel) if rel != 0 else 0.0


def sail_name_on(ship: Ship, yards: list[Spar]) -> str:
    """The name of the principal sail on a group of yards, for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    for y in yards:
        sail = ship.sail_of(y)
        if sail is not None and sail.is_set:
            return part_name(ship, sail.id)
    for y in yards:
        sail = ship.sail_of(y)
        if sail is not None:
            return part_name(ship, sail.id)
    return part_name(ship, yards[0].id) if yards else "the yards"


class YardSwing:
    """Moves a set of yards from where they are to their targets over a fixed
    time, scaled by the weather factor each tick."""

    def __init__(self, yards: list[Spar], targets: list[float], duration_s: float):
        self.yards = yards
        self.starts = [y.brace_angle for y in yards]
        self.targets = targets
        self.duration_s = max(duration_s, 0.0)
        self.progress = 1.0 if not yards or self.duration_s <= 0 else 0.0
        if self.progress >= 1.0:
            self._apply()

    def advance(self, dt: float, factor: float) -> bool:
        if self.progress < 1.0:
            self.progress = min(1.0, self.progress + dt / (self.duration_s * factor))
            if self.progress >= 1.0 - 1e-9:
                self.progress = 1.0
            self._apply()
        return self.progress >= 1.0

    def _apply(self) -> None:
        for y, s, t in zip(self.yards, self.starts, self.targets, strict=True):
            y.brace_angle = s + (t - s) * self.progress

    @property
    def done(self) -> bool:
        return self.progress >= 1.0

    def remaining_s(self) -> float:
        return (1.0 - self.progress) * self.duration_s


def move_toward(yards: list[Spar], targets: list[float], max_step: float) -> bool:
    """Brace each yard toward its target, moving at most ``max_step`` radians
    this tick. Returns True when every yard is at its target."""
    settled = True
    for y, target in zip(yards, targets, strict=True):
        delta = target - y.brace_angle
        if abs(delta) <= max_step:
            y.brace_angle = target
        else:
            y.brace_angle += math.copysign(max_step, delta)
            settled = False
    return settled


def follow_wind(yards: list[Spar], rel: float, close_hauled: float, max_step: float) -> bool:
    """Brace each yard toward its trim for the wind (see ``trim_angle``)."""
    targets = [trim_angle(rel, y.brace_limit, close_hauled) for y in yards]
    return move_toward(yards, targets, max_step)


# ---------------------------------------------------------------------------
# The base class
# ---------------------------------------------------------------------------


class Script:
    """One scripted manoeuvre in progress. The runner calls ``check`` before
    starting, ``begin`` when the manoeuvre starts, and ``tick`` every tick."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        self.ship = ship
        self.params = params
        self.timing = timing
        self.status = "running"
        self.reason: str | None = None
        self.phase = "ready"
        self.t = 0.0

    def timing_value(self, key: str, default: float) -> float:
        return float(self.timing.get(key, default))

    def holds(self) -> set[str]:
        return {self.ship.name}

    def clears(self) -> set[str]:
        """The parts whose work in hand this script belays when it begins, rather than
        waiting for it or leaving it to run on (a send-down's sails: see `_Rig.held`)."""
        return set()

    def check(self, words: dict[str, Any]) -> str | None:
        """An extra precondition in code. Returns the reason it fails, or None."""
        return None

    def begin(self, words: dict[str, Any]) -> None:
        raise NotImplementedError

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        raise NotImplementedError

    def remaining_s(self) -> float:
        return 0.0

    def words(self) -> dict[str, Any]:
        return {}

    def data(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_s": round(self.t, 1)}

    def left_words(self) -> str | None:
        """How the work is left when the captain belays it, in words for the log, when
        the script has more to say than the runner's "the helm and the yards left as
        they stand" (package 37k: a belay of getting under way says where it has left
        the anchor); None for the runner's words."""
        return None

    def belayed(self) -> None:
        """Called by the runner as the captain belays the work: whatever the script holds
        that would outlive it is let go (package 37k: the capstan's pawl, an anchor's
        cable `heaving`)."""

    def note(self, text: str, kind: str = "evolution.step") -> None:
        self.ship.note("routine", kind, text, self.ship.name)

    def fail(self, reason: str) -> None:
        self.status = "failed"
        self.reason = reason

    def finish(self) -> None:
        self.status = "done"


# ---------------------------------------------------------------------------
# Tack
# ---------------------------------------------------------------------------


class TackScript(Script):
    """Tack ship, after Luce 1866 ch. XXIV 'Tacking' (pp. 450-451) and 'Missing Stays',
    Luce 1884 ch. XXIV 'Missing Stays' ('In Irons') and ch. XXXIV 'Sloops', and Lever
    1808 'Tacking Expeditiously' (p. 78) and 'Missing Stays' (p. 94).

    Helm's a-lee: the helm is ordered to a heading twelve points round, through the
    wind, the head sheets let fly and the spanker (or a fore-and-after's main) sheet
    hauled aft, which brings her up. When her head is within a point of the wind,
    "mainsail haul": the after yards swing to the new tack. When her head has passed
    through the wind, "let go and haul": the head yards follow, the head sheets are
    drawn on the new tack and the helm is ordered to the new close-hauled course. She
    is tacked when steady on it.

    Package 32e (spec M5 open item 12): the miss-stays rule reads the vessel, and she
    is given Luce's recovery before she gives up. Her way is gone when she makes less
    than ``way_gone_fraction`` of her speed at "helm's a-lee" or less than
    ``way_gone_lengths_per_min`` of her own lengths a minute, whichever is the more.
    Way gone with her head more than a point off the wind, the after yards not yet
    swung, is a plain miss ("should she come to a stand, and fall off before the after
    yards are swung", Luce 1866). Way gone within a point of the wind, she hangs in
    stays: the helm is kept a-lee while she has way and shifted as she gathers
    sternway (the helmsman's rule, physics/hull.py: "if she gathers sternboard, Shift
    the helm!"), the head yards stay aback to box her head off on to the new tack, the
    head sheets are held to windward (the old lee side, aback once she is through: Luce
    1884, 'Sloops': "trim the jib sheet to windward again as she passes the direction
    of the wind"), and the spanker's or main's boom is hauled over to windward ("haul
    the spanker boom well over to the windward", Luce 1866). Only when she has plainly
    fallen back on the old tack (two points off the wind on the old side) or hung for
    ``stays_timeout_s`` from the moment her way went is it "missed stays": the yards
    are then squared as a brace with hands and time, the head sheets flattened in, the
    spanker sheet eased off (Luce 1866: "Flatten in the head sheets! ease off the
    spanker sheet") and the helm put up as an order the helmsman carries out.
    """

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.through = False
        self.swing: YardSwing | None = None
        self.old_heading = ship.dyn.heading
        self.new_course = ship.dyn.heading
        self.t_steady = 0.0
        self.bowlined: list[str] = []  # sails whose bowlines were hauled out before going about
        self.studding: StuddingSailsIn | None = None
        # package 32e: the recovery
        self.speed_at_helm = ship.dyn.speed
        self.way_gone_at: float | None = None
        self.way_gone_since: float | None = None
        self.hung = False
        self.heads: list[Sail] = []
        self.booms: list[Sail] = []
        self.shifted: list[Sail] = []  # the staysails abaft the fore mast, a foresail
        self.squaring: YardSwing | None = None
        self.miss_reason = ""

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.head + self.after}

    # -- the vessel's way ------------------------------------------------------------

    def way_gone_speed(self) -> float:
        """The speed below which her way is gone, m/s: the larger of a fraction of her
        speed at helm's a-lee and so many of her lengths a minute (the file's timing)."""
        fraction = self.timing_value("way_gone_fraction", 0.25)
        per_min = self.timing_value("way_gone_lengths_per_min", 1.0)
        return max(fraction * self.speed_at_helm, per_min * self.ship.hull.length / 60.0)

    def old_side(self, weather: bool) -> str:
        """The old tack's weather or lee side by name."""
        weather_side = "starboard" if self.sign > 0 else "larboard"
        lee_side = "larboard" if self.sign > 0 else "starboard"
        return weather_side if weather else lee_side

    def _boom_words(self) -> str:
        return names_of_sails(self.ship, self.booms) if self.booms else ""

    def begin(self, words: dict[str, Any]) -> None:
        # the studding sails first, if any are set or their booms out (spec 3b §7)
        studding = StuddingSailsIn(self.ship)
        if studding.needed:
            self.studding = studding
            self.phase = "in_studding_sails"
            self.note(studding.begin_words())
            return
        self._ready_about()

    def _ready_about(self) -> None:
        self.t = 0.0  # the stays are timed from "ready about"
        end_lying_to(self.ship)  # a ship going about is hove to no longer (package 37f)
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.bowlined = bowlines_hauled(self.ship)
        self.old_heading = dyn.heading
        self.speed_at_helm = dyn.speed
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(dyn.heading + self.sign * 12 * POINT)
        dyn.steady = False
        self.phase = "helm_down"
        # "Helm's a-lee!" and the head sheets eased off (Luce 1866, ch. XXIV, 'Tacking':
        # the head sheets let go as the helm goes down; eased right off here rather than
        # let fly, see `ease_off_sheets`); the spanker sheet hauled aft "as the sail
        # lifts"; a sloop's main sheet the same ("trim aft the main sheet", Luce 1884,
        # ch. XXXIV)
        self.heads = head_sails(self.ship)
        self.booms = boom_sails(self.ship)
        self.shifted = shifted_sails(self.ship)
        ease_off_sheets(self.ship, self.heads)
        sheets_to(self.ship, self.booms, None, None)
        words = "Ready about. Helm's a-lee"
        if self.heads:
            words += "; ease off the head sheets"
        if self.booms:
            words += f"; haul aft the {self._boom_words().replace('the ', '')} sheet"
        self.note(words + ".", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        if self.phase == "in_studding_sails":
            assert self.studding is not None
            if self.studding.advance(dt, factor):
                self.note(self.studding.end_words())
                self._ready_about()
            return
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "missed":
            # the yards squared as a brace, with hands and time; then she has missed stays
            assert self.squaring is not None
            if self.squaring.advance(dt, factor):
                self.fail(self.miss_reason)
            return
        if not self.through and self.sign * rel < 0 and abs(rel) < math.pi / 2:
            self.through = True
            if self.hung:
                self.note("Her head is through the wind; the head sails aback pay her off.")
                # the boom no longer held over: its sail draws on the new tack
                sheets_to(self.ship, self.booms, None, None)
        if not self.through:
            # her way is gone when she has made less than `way_gone_speed` for
            # `hang_after_s`: a dip as she comes head to wind is the ordinary tack
            if dyn.speed < self.way_gone_speed():
                self.way_gone_since = self.t if self.way_gone_since is None else self.way_gone_since
            else:
                self.way_gone_since = None
            way_gone = (
                self.way_gone_since is not None
                and self.t - self.way_gone_since >= self.timing_value("hang_after_s", 15.0)
            )
            if not self.hung and way_gone:
                if abs(rel) > POINT and self.phase == "helm_down":
                    # "should she come to a stand, and fall off before the after yards
                    # are swung" (Luce 1866): a plain miss
                    self._miss_stays("she lost her way before her head came up to the wind")
                    return
                self._hang()
            elif self.hung:
                assert self.way_gone_at is not None
                if self.t - self.way_gone_at > self.timing_value("stays_timeout_s", 180.0):
                    self._miss_stays("she hung in stays and would not come round")
                    return
                if self.sign * rel > 2 * POINT:
                    self._miss_stays("she fell off on the old tack")
                    return
            elif self.t > 3.0 * self.timing_value("stays_timeout_s", 180.0):
                self._miss_stays("she hung in stays and would not come round")
                return
        if self.phase == "helm_down":
            if abs(rel) <= POINT or self.through:
                self.phase = "mainsail_haul"
                # "The lee braces and the bowlines are let go, and the yards swung
                # around briskly by the weather braces" (Luce 1884, ch. XXIV, 'Tacking');
                # the staysails' sheets abaft the fore mast let go, to be shifted over
                # (Lever 1808, p. 78)
                bowlines = let_go_bowlines(self.ship)
                let_fly_sheets(self.ship, self.shifted)
                if self.after:
                    if bowlines:
                        self.note("Rise tacks and sheets. Mainsail haul; let go the bowlines.")
                    else:
                        self.note("Rise tacks and sheets. Mainsail haul.")
                elif bowlines:
                    self.note("Let go the bowlines.")
                self.swing = YardSwing(
                    self.after, [-self.sign * y.brace_limit for y in self.after], brace_s
                )
        if self.phase == "mainsail_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor) and self.through:
                self.phase = "let_go_and_haul"
                # the head yards to the final trim: the after yards stand sharper
                # (spec 3b §2.2, Fincham art. 94); the head sheets drawn on the new tack
                # ("Draw jib!", Luce 1884: "trim aft the head sheets"): the head sheets and
                # the boom's sheet trimmed on the new tack's lee side for the full-and-by
                # wind she is coming to (the deck's reading lags as her head passes the
                # wind). Flat aft they stall her: a spanker or a main kept flat holds her
                # head up while the head yards come round ("if she flies up into the wind,
                # let go the main sheet", Luce 1866, 'Tacking'), and the brig with her head
                # sheets flat made a knot and a half at four points off after seven minutes
                # (package 32e); trimmed for the wind, three and a half knots.
                new_lee = self.old_side(weather=True)
                self._draw_on_new_tack(new_lee, wind)
                draw = " Draw jib; trim aft the head sheets." if self.heads else ""
                if self.head:
                    self.note("Let go and haul." + draw)
                elif draw:
                    self.note(draw.strip())
                sharp = sharp_up_targets(self.ship, self.head, self.after)
                self.swing = YardSwing(
                    self.head, [-self.sign * sharp[y.id] for y in self.head], brace_s
                )
                self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
                dyn.target_heading = self.new_course
                dyn.steady = False
        elif self.phase == "let_go_and_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor):
                self.phase = "steady"
                self.t_steady = 0.0
                # the tack's final trim: the yards braced up, the sheets trimmed for the
                # full-and-by wind of the course she is ordered to, on the new tack's lee
                # side (to the wind of the moment they come flat while she is still coming
                # round, and she stalls); the trim order and the book's tending routine
                # take them from there
                self._draw_on_new_tack(self.old_side(weather=True), wind)
                if steady_out_bowlines(self.ship, self.bowlined, -self.sign):
                    self.note("Haul taut the lifts and weather braces. Steady out the bowlines.")
        elif self.phase == "steady":
            self.t_steady += dt
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.target_heading = self.new_course
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            if error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0)) or (
                self.t_steady >= self.timing_value("steady_timeout_s", 120.0)
            ):
                self.finish()

    def _draw_on_new_tack(self, new_lee: str, wind: Wind) -> None:
        """The sheets drawn on the new tack's lee side, for the full-and-by wind she is
        coming to with the way she carried to "helm's a-lee" (`full_and_by_apparent`).
        Eased a point fuller "until she has way" they were tried and found wrong in this
        model, whose head sails want their working angle of attack to draw at all: the
        frigate lost a hundred and fifty metres to leeward with them so (package 32e)."""
        full_and_by = full_and_by_apparent(self.ship, wind, self.speed_at_helm)
        draw_sheets(self.ship, self.heads + self.booms + self.shifted, new_lee, full_and_by)

    def _hang(self) -> None:
        """Her way is gone within a point of the wind: she hangs in stays, and the
        recovery begins (Luce 1866, 'Tacking' and 'Missing Stays'; Luce 1884, 'Sloops')."""
        self.hung = True
        self.way_gone_at = self.t
        # the head sheets held to windward: on the old lee side, so that they are aback
        # on the new weather bow as she passes the wind and pay her head off
        sheets_to(self.ship, self.heads, self.old_side(weather=False), None)
        # the spanker's (or the main's) boom hauled well over to windward: aback at the
        # stern, it pushes the stern to leeward and her head up to the wind
        sheets_to(self.ship, self.booms, self.old_side(weather=True), None)
        words = ["Her way is gone; she hangs in stays. Helm kept a-lee"]
        if self.head:
            words.append("the head yards aback to box her off")
        if self.heads:
            words.append("the head sheets held to windward")
        if self.booms:
            words.append(
                f"the {self._boom_words().replace('the ', '')} boom hauled over to windward"
            )
        self.note("; ".join(words) + ".", "helm.order")

    def _miss_stays(self, why: str) -> None:
        """Missed stays: the urgent line now; the yards squared as a brace with hands and
        time, the head sheets flattened in and the driver's sheet eased off (Luce 1866,
        'Missing Stays': "Flatten in the head sheets! ease off the spanker sheet"), the
        helm put up as an order; the evolution fails when the yards are square."""
        dyn = self.ship.dyn
        self.miss_reason = why
        self.phase = "missed"
        yards = self.head + self.after
        self.squaring = YardSwing(yards, [0.0] * len(yards), self.timing_value("brace_s", 45.0))
        # the head sheets flattened in on the old tack; the boom's sheet eased right off
        sheets_to(self.ship, self.heads, self.old_side(weather=False), None)
        for sl in self.booms:
            geo = yard_trim.sheet_geometry(self.ship, sl)
            yard_trim.set_sheet_angle(self.ship, sl, geo.ceiling, None)
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = self.old_heading
        dyn.steady = False
        orders = ["Up helm"]
        if yards:
            orders.append("square the yards")
        if self.heads:
            orders.append("flatten in the head sheets")
        if self.booms:
            orders.append(f"ease off the {self._boom_words().replace('the ', '')} sheet")
        self.ship.note(
            "urgent",
            "ship.missed_stays",
            f"Missed stays: {why}. {'; '.join(orders)}.",
            self.ship.name,
            {"reason": why, "old_tack": self.words()["old_tack"], **self.data()},
        )

    def remaining_s(self) -> float:
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "in_studding_sails" and self.studding is not None:
            return self.studding.remaining_s() + 60.0 + 2 * brace_s + 30.0
        if self.phase == "helm_down":
            return 60.0 + 2 * brace_s + 30.0
        if self.phase == "mainsail_haul" and self.swing is not None:
            return self.swing.remaining_s() + brace_s + 30.0
        if self.phase == "let_go_and_haul" and self.swing is not None:
            return self.swing.remaining_s() + 30.0
        if self.phase == "missed" and self.squaring is not None:
            return self.squaring.remaining_s()
        return 30.0

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d.update(
            {
                "through_the_wind": self.through,
                "new_course": self.new_course,
                "hung_in_stays": self.hung,
                "way_gone_at_s": self.way_gone_at,
            }
        )
        return d


# ---------------------------------------------------------------------------
# Wear
# ---------------------------------------------------------------------------


class WearScript(Script):
    """Wear ship, after Luce 1866 ch. XXIV 'Wearing'.

    Up helm: the helm is ordered dead before the wind and the after yards
    are braced in as she falls off, the head yards following once the wind
    is abaft the beam. When the wind is aft, the helm is ordered to the new
    close-hauled course and all yards are braced up as she comes to. She has
    worn when steady on it. Six to twelve minutes for a frigate is the truth
    to hit; the time is set by how fast the physics turns her, not by this
    script, which only sets the targets.
    """

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.way_before = ship.dyn.speed  # by the wind, before "up helm" (for the sheets)
        self.new_course = ship.dyn.heading
        self.bowlined: list[str] = []  # sails whose bowlines were hauled out before wearing
        self.studding: StuddingSailsIn | None = None
        self.brailed: list = []  # the driver brailed up at "up helm" (package 32b)

    def holds(self) -> set[str]:
        held = {self.ship.name} | {y.id for y in self.head + self.after}
        return held | {s.id for s in after_gaff_sails(self.ship)}

    def begin(self, words: dict[str, Any]) -> None:
        # the studding sails first, if any are set or their booms out (spec 3b §7)
        studding = StuddingSailsIn(self.ship)
        if studding.needed:
            self.studding = studding
            self.phase = "in_studding_sails"
            self.note(studding.begin_words())
            return
        self._up_helm()

    def _up_helm(self) -> None:
        self.t = 0.0  # the wear is timed from "up helm"
        end_lying_to(self.ship)  # a ship wearing is hove to no longer (package 37f)
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(estimated_wind_from(self.ship) + math.pi)
        dyn.steady = False
        self.phase = "bear_away"
        # "Put the helm up! Clear away the bo'lines! and as she falls off, BRACE IN THE
        # AFTER YARDS!" (Luce 1884, ch. XXIV, 'Wearing'), the spanker brailed up as the
        # helm goes up ("Brail up the spanker!", the same) and hauled out again as she comes
        # to. Package 32b: the brig, whose spanker is a fifth of her plain sail, would not
        # pay off with it set and came to on the new tack past close-hauled into the wind;
        # the driver is found by place (`after_gaff_sails`), so a fore-and-after keeps hers.
        self.brailed = after_gaff_sails(self.ship)
        for sl in self.brailed:
            sl.state = SailState.IN_THE_GEAR
        brail = f"; brail up {names_of_sails(self.ship, self.brailed)}" if self.brailed else ""
        self.bowlined = bowlines_hauled(self.ship)
        if let_go_bowlines(self.ship):
            self.note(
                f"Stand by to wear ship. Up helm; clear away the bowlines{brail}; brace in the "
                "after yards.",
                "helm.order",
            )
        else:
            self.note(
                f"Stand by to wear ship. Up helm{brail}; brace in the after yards.", "helm.order"
            )

    def _haul_out(self) -> str:
        """Haul out the driver brailed up at 'up helm', as she comes to; the words."""
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        words = []
        for sl in self.brailed:
            if sl.state is SailState.IN_THE_GEAR and _chain_standing(self.ship, sl):
                sl.state = SailState.SET
                words.append(f"Haul out the {part_name(self.ship, sl.id)}!")
        self.brailed = []
        return (" " + " ".join(words)) if words else ""

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        if self.phase == "in_studding_sails":
            assert self.studding is not None
            if self.studding.advance(dt, factor):
                self.note(self.studding.end_words())
                self._up_helm()
            return
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 1.0)) * dt / factor
        if self.t > self.timing_value("wear_timeout_s", 900.0):
            self.fail("she would not come round")
            return
        if self.phase == "bear_away":
            dyn.target_heading = units.wrap_2pi(wind.direction_from + math.pi)
            follow_wind(self.after, rel, ch, max_step)
            if abs(rel) > math.pi / 2:
                follow_wind(self.head, rel, ch, max_step)
            wind_aft = abs(rel) >= units.deg_to_rad(165.0)
            crossed = self.sign * rel < 0 and abs(rel) > math.pi / 2
            if wind_aft or crossed:
                self.phase = "come_to"
                # "when the wind is aft shift over the boom and head sheets" (Luce 1884,
                # ch. XXXIV, 'To Wear'; package 32e): every fore-and-aft sheet to the new
                # tack's lee side (the old weather side), trimmed for the wind she comes to
                shift_sheets_over(
                    self.ship, "starboard" if self.sign > 0 else "larboard", wind, self.way_before
                )
                self.note(
                    "Wind aft. Squared the head yards; shifted over the sheets; hauled out "
                    "and braced up."
                )
        if self.phase == "come_to":
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.target_heading = self.new_course
            dyn.steady = False
            sharp_up = -self.sign  # braced sharp up for the new tack
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
            # The driver brailed up at "up helm" is hauled out as she comes to, once she is
            # by the wind: hauled out with the wind aft, the brig's (a fifth of her plain
            # sail) rounded her up through the wind before the helm could meet her.
            if steady and self.brailed:
                self.note("By the wind." + self._haul_out())
            # The after yards go sharp up at once to bring her to; the head yards
            # follow the wind, keeping their sails full, until she is by the wind.
            # (All yards end at their limits, as at milestone 2: spec 3b §2.2 asks
            # the after yards' trim of the tack's final trim and the orders only.)
            after_done = move_toward(
                self.after, [sharp_up * y.brace_limit for y in self.after], max_step
            )
            if steady:
                head_done = move_toward(
                    self.head, [sharp_up * y.brace_limit for y in self.head], max_step
                )
            else:
                follow_wind(self.head, rel, ch, max_step)
                head_done = False
            if steady and after_done and head_done:
                # "When by the wind, right the helm, trim the yards, Haul taut the lifts
                # and weather braces! Steady out the bowlines!" (Luce 1884, 'Wearing')
                if steady_out_bowlines(self.ship, self.bowlined, sharp_up):
                    self.note("Haul taut the lifts and weather braces. Steady out the bowlines.")
                self.finish()

    def remaining_s(self) -> float:
        first = self.studding.remaining_s() if self.studding is not None else 0.0
        return first + max(0.0, self.timing_value("wear_estimate_s", 480.0) - self.t)

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }


# ---------------------------------------------------------------------------
# Heave to and fill away
# ---------------------------------------------------------------------------


# Hove to, a driver that is kept has its sheet eased to the trim of a wind six points on
# the bow (package 32e; judgement, measured on the brig: sheeted for five points she
# comes up head to wind and falls off, for eight she lies nearly abeam; for six she lies
# 69 degrees off, forereaching a knot and a half). Luce 1866, ch. XXVI: "regulate by
# easing off, or hauling aft, the spanker and jib sheets".
HOVE_TO_DRIVER_APPARENT = 6 * POINT

# Lying to, and the watch that keeps her so (package 37f; the review of gate 5c's
# playtests, 5.8 and 10.3 under the owner's note 6: "the helm and sails need to try to
# keep her hove to properly on the tack she hove to on"). Until this package the script
# braced the yards aback, put the helm a-lee and ended, and nobody tended her: from seven
# knots the fixed helm carried the brig's head through the wind inside a minute, and in a
# shifting light air she came round in six minutes and in twenty, to lie for hours with
# the wind abaft the other beam. Now the helm is eased as she comes up and her way is
# taken off before she is said to be hove to (`HeaveToScript`), and while the record
# stands the watch tends the helm and the sheets (`keep_lying_to`, once a tick from the
# runner), as Luce has it: "regulate by easing off, or hauling aft, the spanker and jib
# sheets" (Luce 1866, ch. XXVI, 'To heave to'). Every figure is the `timing:` block of
# data/evolutions/heave_to.yaml (`lying_to_timing`); the defaults written here are the
# file's.
LYING_TO_HANDS = "lying_to#watch"  # what the hands at the sheets carry in `Sailor.at`
# Sternway beyond which the helm is shifted lying to (m/s): the helmsman's own figure
# (`physics.hull.STERNWAY_SHIFT_SPEED`), written here so that the scripts do not import
# the physics.
LYING_TO_STERNWAY = 0.15
# Her way lying to is read smoothed over this long, seconds, for where the watch holds her.
LYING_TO_WAY_SMOOTH_S = 60.0
# The manoeuvres that have the helm and the yards while they are in hand: the watch's
# tending stands off for them (a ship being filled away is not held to her old tack).
HELM_MANOEUVRES = frozenset(
    {
        "heave_to",
        "fill_away",
        "tack",
        "wear",
        "boxhaul",
        "wear_short_round",
        "lie_a_try",
        "scud",
        "back_and_fill",
        "come_to_anchor",
        "get_under_way",
    }
)


def lying_to_timing() -> dict[str, float]:
    """The heave-to's own figures (data/evolutions/heave_to.yaml, `timing:`), for the
    tending that goes on after its script has ended."""
    from freesail.evolutions import registry  # local import: the registry reads the files

    evo = registry.get("heave_to")
    return evo.timing if evo is not None else {}


def lying_off(ship: Ship, wind: Wind, sign: float) -> float:
    """Her head's angle from the wind on the tack `sign` (+1 starboard), radians:
    positive while the wind is on that side, negative once it has come round her bow
    (or her stern) to the other."""
    return sign * wind_rel(ship, wind)


def _tack_name(sign: float) -> str:
    return "starboard" if sign > 0 else "larboard"


def _lee_name(sign: float) -> str:
    return "larboard" if sign > 0 else "starboard"


def _kept_after_sails(ship: Ship, info: dict[str, Any]) -> list[Sail]:
    """The after sails whose sheets the watch regulates lying to: the gaff sails set on
    a boom (a brig's or a ship's spanker when it is kept, a fore-and-after's mainsail)."""
    return boom_sails(ship)


def tend_lying_to(
    ship: Ship,
    info: dict[str, Any],
    dt: float,
    wind: Wind,
    timing: dict[str, float],
    sheets: bool = True,
    nearer: bool = True,
) -> float:
    """One tick of the tending: the helm, and with hands for them (`sheets`) the spanker
    and jib sheets, worked to hold her head between `near_points` and `far_points` from
    the wind on the tack `info["sign"]`. Returns her head's angle from the wind on that
    tack (`lying_off`).

    The helm. She lies with `helm_deg` of lee helm when her head is midway between the
    two; it is eased as she comes up, righted a quarter point outside `near_points` and
    put up (to leeward) nearer the wind than that; more of it as she falls off, to
    `helm_max_deg`. The helmsman meets her swing `helm_lead_s` ahead, so a ship rounding
    to with way on has the helm righted before her head is where it is to lie. With
    sternway the rudder works the other way and the helm is shifted (the helmsman's own
    rule, `physics/hull.py`).

    The sheets (Luce 1866, ch. XXVI: "regulate by easing off, or hauling aft, the spanker
    and jib sheets"). Within three quarters of a point of either bound nothing is touched.
    Falling off past that, the spanker (or a fore-and-after's main) sheet is hauled aft
    and the head sheets eased, in proportion, all of it a point further on; coming up,
    the spanker sheet is eased off and the head sheets kept flat; and nearer the wind than
    `aback_points` the innermost head sail's sheet is hauled to windward, to box her head
    off, until she is a half point inside her bounds again. The hands work a sheet from
    one end of that to the other in `sheet_s`.
    """
    dyn = ship.dyn
    sign = float(info.get("sign", 1.0))
    off = lying_off(ship, wind, sign)
    coming_up = sign * dyn.r  # rad/s: her head swinging toward the wind
    near = float(timing.get("near_points", 4.0)) * POINT
    far = float(timing.get("far_points", 7.0)) * POINT
    # -- where she is held ---------------------------------------------------------------
    # Midway between her bounds with `lie_kn` of headway; a point nearer the wind for each
    # knot she forereaches beyond that (her head yards lift and her way falls), a point
    # further off for each knot short of it or astern (they fill and she comes ahead). The
    # helm is given a mark no nearer either bound than a quarter of a point, the sheets
    # one no nearer than three quarters. Her way is read smoothed over a minute, so that
    # she is not hunted about by it.
    margin = 0.75 * POINT
    middle = 0.5 * (near + far)
    way_kn = units.ms_to_knots(dyn.u)
    smooth = float(info.get("way_kn", way_kn))
    smooth += (way_kn - smooth) * min(1.0, dt / LYING_TO_WAY_SMOOTH_S)
    info["way_kn"] = smooth
    lean = (float(timing.get("lie_kn", 0.5)) - smooth) * float(timing.get("lean_points_kn", 1.0))
    if not nearer:
        lean = max(lean, 0.0)  # bringing her to: not nearer the wind for the way she carries
    mark = max(near + 0.25 * POINT, min(far - 0.25 * POINT, middle + lean * POINT))
    aim = max(near + margin, min(far - margin, mark))
    # -- the helm -------------------------------------------------------------------
    helm = units.deg_to_rad(float(timing.get("helm_deg", 15.0)))
    hard = units.deg_to_rad(ship.hull.spec.rudder.max_angle_deg)
    most = min(hard, units.deg_to_rad(float(timing.get("helm_max_deg", 25.0))))
    ahead = off - coming_up * float(timing.get("helm_lead_s", 15.0))
    turn = helm * (ahead - mark) / (1.25 * POINT)  # + to bring her head up
    if dyn.u < -LYING_TO_STERNWAY:
        # sternway: the rudder works the other way, and the lee helm she carries with
        # headway is not wanted (a-lee, it throws her head off)
        wanted = max(-most, min(most, -turn))
    else:
        wanted = max(-hard, min(most, helm + turn))  # + is a-lee, toward the wind
    if not info.get("helm_by_order"):
        # a conning word given while she lies to (`helm a-weather`, `right the helm`) is
        # the captain's helm: the watch leaves it where he put it and tends the sheets
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = sign * wanted
    if not sheets:
        return off
    # -- the sheets ------------------------------------------------------------------
    looked = off - coming_up * float(timing.get("sheet_lead_s", 20.0))
    if looked > aim + margin:
        demand = min(1.0, (looked - (aim + margin)) / POINT)  # falling off: bring her up
    elif looked < aim - margin:
        demand = -min(1.0, ((aim - margin) - looked) / POINT)  # coming up: pay her off
    else:
        demand = 0.0
    now = float(info.get("sheets", 0.0))
    step = dt / max(float(timing.get("sheet_s", 30.0)), 1.0)
    new = now + max(-step, min(step, demand - now))
    boxed = bool(info.get("boxed"))
    box = looked < float(timing.get("aback_points", 2.5)) * POINT or (
        boxed and looked < near + 0.5 * POINT
    )
    if abs(new - now) < 1e-9 and box == boxed and info.get("sheets_set"):
        return off
    info["sheets"] = new
    info["boxed"] = box
    info["sheets_set"] = True
    _work_lying_to_sheets(ship, info, new, box)
    return off


def _work_lying_to_sheets(ship: Ship, info: dict[str, Any], demand: float, box: bool) -> None:
    """The sheets as the tending wants them: `demand` from -1 (pay her off) through 0 (as
    the heave-to left them) to +1 (bring her up); `box` the innermost head sail's sheet to
    windward. The sides are named by the tack she hove to on, not read from the wind of
    the moment, which is on either bow as she comes head to it."""
    sign = float(info.get("sign", 1.0))
    lee, weather = _lee_name(sign), _tack_name(sign)
    fore_and_aft = len(_masts_with_yards(ship)) < 2
    for sl in _kept_after_sails(ship, info):
        geo = yard_trim.sheet_geometry(ship, sl)
        # as the heave-to left it: a fore-and-after's main flat aft, a brig's spanker
        # eased for a wind six points on the bow
        rest = (
            geo.floor
            if fore_and_aft
            else yard_trim.wanted_sheet_angle(sl.cls, HOVE_TO_DRIVER_APPARENT)
        )
        to = geo.floor if demand > 0 else geo.ceiling
        yard_trim.set_sheet_angle(ship, sl, rest + (to - rest) * abs(demand), lee)
        sl.shivering = False
    heads = head_sails(ship)
    held = info.get("headsail")
    inner = min(heads, key=lambda sl: sl.x_m) if heads else None
    for sl in heads:
        geo = yard_trim.sheet_geometry(ship, sl)
        eased = geo.floor + (geo.ceiling - geo.floor) * max(demand, 0.0)
        if sl.id == held:
            # the fore-and-after's way: her staysail's sheet to windward, eased to let
            # her come up
            yard_trim.set_sheet_angle(ship, sl, eased, weather)
        elif fore_and_aft:
            continue  # her other head sails draw as they were trimmed
        elif box and sl is inner:
            yard_trim.set_sheet_angle(ship, sl, geo.floor, weather)
        else:
            yard_trim.set_sheet_angle(ship, sl, eased, lee)
        sl.shivering = False


def end_lying_to(ship: Ship) -> bool:
    """She is hove to no longer: the record cleared and the watch's hands let go. Called
    by whatever ends it without filling away (an anchor let go, the anchor aweigh, a tack
    or a wear begun, the ground: package 37f, the review's 5.8 and 10.3, where the record
    outlived a night at anchor and refused her a course four times with the anchor up).
    True if she was."""
    was = ship.extra.pop("hove_to", None) is not None
    lying_to_hands_off(ship)
    return was


def lying_to_hands_off(ship: Ship) -> None:
    from freesail.crew import hands  # local import: the crew is not the scripts' business
    from freesail.crew.model import Crew

    crew = ship.extra.get("crew")
    if isinstance(crew, Crew) and ship.extra.pop("lying_to.hands", None):
        hands.release(crew, LYING_TO_HANDS)


def _lying_to_hands_on(ship: Ship, info: dict[str, Any], clock: Any, timing: dict) -> bool:
    """The hands the tending costs the watch on deck (`keep_hands` of them, at the
    spanker and the head sheets): taken when she is hove to, given back and taken afresh
    from the relief when the watch changes, and asked for again every ten seconds while
    none are to be had. True when the sheets are manned. A ship without a crew has them
    (milestone 2's rule: every request met)."""
    from freesail.crew import bill, hands
    from freesail.crew.model import Crew
    from freesail.evolutions.runner import DEFAULT_WATCH_TIME

    crew = ship.extra.get("crew")
    if not isinstance(crew, Crew):
        return True
    when = clock if clock is not None else DEFAULT_WATCH_TIME
    watch = bill.watch_on_deck(crew, when).value
    held = int(ship.extra.get("lying_to.hands") or 0)
    if held and info.get("watch") == watch:
        return True
    kept = float(info.get("kept_s", 0.0))
    if not held and kept - float(info.get("hands_asked_s", -1e9)) < 10.0:
        return False
    info["hands_asked_s"] = kept
    if held:
        hands.release(crew, LYING_TO_HANDS)  # the watch relieved: the relief takes them
        ship.extra.pop("lying_to.hands", None)
    want = hands.CrewRequest(
        hands=max(1, int(timing.get("keep_hands", 4))),
        stations=("afterguard", "forecastle"),
    )
    got = hands.request(crew, bill.on_deck(crew, when), LYING_TO_HANDS, want, None)
    info["watch"] = watch
    if got.outcome == hands.TOO_FEW:
        return False
    ship.extra["lying_to.hands"] = got.got
    return True


def _aback_now(ship: Ship, info: dict[str, Any]) -> bool:
    """Whether anything of hers is aback as a ship hove to has it: a square sail set and
    pressed to its mast, or a head sail held aback by its sheet."""
    for sl in ship.sails.values():
        if not sl.is_set:
            continue
        if sl.cls == "square" and sl.backed:
            return True
        if sl.is_fore_and_aft and sl.backed:
            return True
    return False


def _yards_aback_for(ship: Ship, sign: float) -> list[Spar]:
    """The yards that are braced aback for the tack `sign` with a square sail set on
    them: braced up for the other tack."""
    out = []
    for y in working_yards(ship):
        sl = ship.sail_of(y)
        if sl is None or not sl.is_set or sl.cls != "square":
            continue
        if y.brace_angle * sign < -units.deg_to_rad(5.0):
            out.append(y)
    return out


def _judge_lying_to(
    ship: Ship, info: dict[str, Any], dt: float, wind: Wind, timing: dict[str, float]
) -> None:
    """If she is forced round all the same (a shift of many points, a squall), one urgent
    line says so and the record follows what she is doing (package 37f, item 1). Her
    head through the wind and `round_points` on the other bow for `round_s`: she has come
    round, and lies on the other tack with whatever of her yards is now aback (hove to
    on it, and kept on it), or with nothing aback is hove to no longer. And on either
    tack, with nothing of hers aback and more way on than `way_off_kn` for `fill_s`, she
    has filled and gathers way: hove to no longer, urgently (the review's 5.8: "she filled
    in a squall and sailed toward the land for an hour with no alert, the game still
    answering 'She is hove to'")."""
    dyn = ship.dyn
    sign = float(info.get("sign", 1.0))
    off = lying_off(ship, wind, sign)
    a_try = info.get("how") == "a-try"
    way_off = units.knots_to_ms(float(timing.get("way_off_kn", 1.5)))
    # -- through the wind -------------------------------------------------------------
    across = float(timing.get("round_points", 1.0)) * POINT
    if off < -across and off > -math.pi + across:
        info["round_s"] = float(info.get("round_s", 0.0)) + dt
    else:
        info["round_s"] = 0.0
    if info["round_s"] >= float(timing.get("round_s", 20.0)):
        new_sign = -sign
        aback = [] if a_try else _yards_aback_for(ship, new_sign)
        old, new = _tack_name(sign), _tack_name(new_sign)
        if aback:
            what = sail_name_on(ship, aback)
            info.update(
                {
                    "sign": new_sign,
                    "yards": [y.id for y in aback],
                    "round_s": 0.0,
                    "full_s": 0.0,
                    "sheets": 0.0,
                    "boxed": False,
                    "sheets_set": False,
                    "forced": True,
                }
            )
            info.pop("headsail", None)
            ship.note(
                "urgent",
                "ship.forced_round",
                f"She has been forced round through the wind and lies on the {new} tack, the "
                f"{what} to the mast: hove to on it. To stand on, fill away.",
                ship.name,
                {"old_tack": old, "tack": new, "yards": info["yards"], "hove_to": True},
            )
            return
        _hove_to_no_longer(
            ship,
            f"She has been forced round through the wind onto the {new} tack with nothing "
            f"aback: hove to no longer.",
            {"old_tack": old, "tack": new, "hove_to": False, "why": "forced round"},
        )
        return
    if a_try:
        return
    # -- fallen off, the wind abaft the beam -----------------------------------------------
    # more than `abaft_points` from the wind for `abaft_s`: the helm and the sheets have
    # not brought her to (a brig under her topsails alone has no sheet to regulate by),
    # and a ship lying with the wind abaft her beam is not hove to
    if off > float(timing.get("abaft_points", 9.0)) * POINT:
        info["abaft_s"] = float(info.get("abaft_s", 0.0)) + dt
    else:
        info["abaft_s"] = 0.0
    if info["abaft_s"] >= float(timing.get("abaft_s", 120.0)):
        rel = wind_rel(ship, wind)
        _hove_to_no_longer(
            ship,
            f"She has fallen off, the wind {units.wind_bearing_words(rel)}, and the helm and "
            f"the sheets will not bring her to: hove to no longer.",
            {
                "tack": _tack_name(1.0 if rel > 0 else -1.0),
                "hove_to": False,
                "why": "fallen off",
            },
        )
        return
    # -- filled, and gathering way ------------------------------------------------------
    # nothing of hers aback and more way on than she lies to with; or, forced round onto
    # the other tack, her after yards full there and the same way on her
    if dyn.u > way_off and (info.get("forced") or not _aback_now(ship, info)):
        info["full_s"] = float(info.get("full_s", 0.0)) + dt
    else:
        info["full_s"] = 0.0
    if info["full_s"] >= float(timing.get("fill_s", 60.0)):
        rel = wind_rel(ship, wind)
        where = units.wind_bearing_words(rel)
        how = "Her after yards full, she" if info.get("forced") else "She has filled and"
        _hove_to_no_longer(
            ship,
            f"{how} gathers way, the wind {where}: hove to no longer.",
            {"tack": _tack_name(1.0 if rel > 0 else -1.0), "hove_to": False, "why": "filled"},
        )


def _hove_to_no_longer(ship: Ship, text: str, data: dict[str, Any]) -> None:
    """The record cleared with an urgent line, and the helm told to keep her full and by
    on the tack she is on: a ship sailing off with her helm where the tending left it is
    nobody's, and a heading held might be the wind's eye."""
    dyn = ship.dyn
    end_lying_to(ship)
    dyn.helm_mode = HelmMode.FULL_AND_BY
    dyn.steady = False
    data = {**data, "speed_kn": round(units.ms_to_knots(dyn.u), 1), "heading": dyn.heading}
    ship.note(
        "urgent",
        "ship.filled",
        f"{text} The helm keeps her full and by.",
        ship.name,
        data,
    )


def keep_lying_to(ship: Ship, dt: float, wind: Wind, runner: Any = None) -> None:
    """Once a tick, from the runner: while she is hove to (`ship.extra["hove_to"]`) and no
    manoeuvre has the helm, the watch tends the helm and the sheets to hold her on her
    tack (`tend_lying_to`), which costs it `keep_hands` hands; she is judged
    (`_judge_lying_to`); and once a watch a routine line says how she lies. Lying a-try
    (`how: a-try`) keeps the helm its own script gave it and is judged only."""
    info = ship.extra.get("hove_to")
    if not isinstance(info, dict):
        if ship.extra.get("lying_to.hands"):
            lying_to_hands_off(ship)
        return
    for inst in getattr(runner, "instances", None) or ():
        if inst.evo.id in HELM_MANOEUVRES and not inst.waiting and inst.script is not None:
            return
    timing = lying_to_timing()
    kept = float(info.get("kept_s", 0.0)) + dt
    info["kept_s"] = kept
    clock = getattr(runner, "clock", None)
    a_try = info.get("how") == "a-try"
    if not a_try:
        manned = _lying_to_hands_on(ship, info, clock, timing)
        tend_lying_to(ship, info, dt, wind, timing, sheets=manned)
    _judge_lying_to(ship, info, dt, wind, timing)
    if ship.extra.get("hove_to") is not info:
        return
    # the routine line, one a watch: at the change of the watch by the ship's clock, or
    # every four hours of lying to where the runner has been given none
    if clock is not None:
        name = clock.watch()
        due = info.get("said_watch") not in (None, name)
        info["said_watch"] = name
    else:
        due = int(kept // 14400.0) > int((kept - dt) // 14400.0)
    if due:
        sign = float(info.get("sign", 1.0))
        off = lying_off(ship, wind, sign)
        ship.note(
            "routine",
            "ship.lying_to",
            f"Lying to on the {_tack_name(sign)} tack, her head {_points_off_words(off)} from "
            f"the wind; the watch tending the helm and the sheets.",
            ship.name,
            {
                "tack": _tack_name(sign),
                "off_points": round(units.rad_to_points(off), 1),
                "speed_kn": round(units.ms_to_knots(ship.dyn.u), 1),
            },
        )


def _points_off_words(off: float) -> str:
    """'six points', 'five points and a half', to the half point."""
    from freesail.crew.model import number_words  # local import: the words' one home

    halves = max(0, int(round(units.rad_to_points(abs(off)) * 2.0)))
    whole, half = divmod(halves, 2)
    if whole == 0:
        return "half a point" if half else "no points"
    noun = "point" if whole == 1 else "points"
    return f"{number_words(whole)} {noun}{' and a half' if half else ''}"


class HeaveToScript(Script):
    """Heave to (after Luce 1866 ch. XXVI 'To heave to'): haul up the courses, lay the
    yards of the mast carrying the most square sail aback (the main topsail to the mast),
    the rest full, and put the helm a-lee. Hauling up the courses is done directly here
    rather than through their own evolutions, which is milestone 2's simplification.

    Package 37f: her way is taken off first. The helm is not lashed a-lee: it is tended
    from the first tick as the watch tends it afterwards (`tend_lying_to`), eased and
    righted as she comes up, so that the way she carries does not take her head through
    the wind. "Hove to" is said when she lies on her tack between `near_points` and
    `far_points` from the wind with less than `way_off_kn` of way and her head quiet for
    `lie_s`; or at `way_off_timeout_s`, if she is on her tack with the wind before the
    beam, and otherwise the evolution fails in words. The backed yards and the tack are
    then written in ``ship.extra["hove_to"]``: the record that she is hove to, which the
    watch keeps her by (`keep_lying_to`) and which fill away, or whatever else ends it,
    clears (`end_lying_to`)."""

    # class defaults for the fields package 37f added, so that a heave-to caught mid-way
    # in a checkpoint from an earlier build loads and goes on
    headsail: Sail | None = None
    full: tuple | list = ()
    info: dict[str, Any] | None = None
    quiet_s = 0.0
    off = 0.0
    way_was = 0.0
    slowing = 1.0

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.swing: YardSwing | None = None
        self.headsail: Sail | None = None
        self.full: list[Spar] = []  # the yards that stay full, braced up for the tack
        self.info: dict[str, Any] = {}
        self.quiet_s = 0.0
        self.off = 0.0
        self.way_was = units.ms_to_knots(abs(ship.dyn.u))
        self.slowing = 1.0  # knots a second her way is falling by, smoothed

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in working_yards(self.ship)}

    def fore_and_after(self) -> bool:
        """A vessel whose yards are all on one mast (a topsail schooner, a cutter): hove to
        the fore-and-after's way (package 32e; Luce 1884, ch. XXXIV, 'To Heave to':
        "Haul flat aft the main sheet, putting the helm down, and haul the staysail sheet
        to windward"), with her topsail to the mast as well if it is set."""
        return len(_masts_with_yards(self.ship)) < 2

    def _backed_name(self) -> str:
        """The sail laid to the mast, for the log: the first on the backed yards that is
        set and not being handed (package 37k: says which), else as `sail_name_on`."""
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        sail = standing_sail_on(self.ship, self.yards)
        return (
            part_name(self.ship, sail.id)
            if sail is not None
            else sail_name_on(self.ship, self.yards)
        )

    def check(self, words: dict[str, Any]) -> str | None:
        # Package 37k: a sail that is set is laid aback, never one furled or in the gear,
        # nor one the hands are taking in (`being_handed`); the yards and the head sail
        # are chosen afresh when the work begins, since it may have waited its turn.
        self.yards = yards_to_back_set(self.ship)
        square_set = standing_sail_on(self.ship, self.yards) is not None
        if self.fore_and_after():
            if not square_set and innermost_head_sail(self.ship, standing=True) is None:
                return "No head sail is set to haul to windward, nor a topsail to lay aback."
            if not square_set:
                self.yards = []
        elif not self.yards:
            return "She has no square yards to lay aback."
        elif not square_set:
            return f"No sail is set on the {sail_name_on(self.ship, self.yards)} to lay aback."
        wanted = self.params.get("tack")
        if wanted in ("port",):
            wanted = "larboard"
        if wanted and wanted != self.ship.dyn.tack:
            return (
                f"She is on the {self.ship.dyn.tack} tack; "
                f"tack or wear first to heave to on the {wanted}."
            )
        if "hove_to" in self.ship.extra:
            return "She is hove to already."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        # The yards that stay full are braced up for the tack as she comes to (Luce 1884,
        # ch. XXVI, 'To heave to, having the wind aft, or on the quarter': "brace the
        # mizzen topsail sharp up ... meet her, as she comes to, with the helm, and by
        # bracing up the head yards, and hauling aft the head sheets"). Package 37f: left
        # as they were trimmed for a wind on the quarter they are all but square, and
        # with her head five points from the wind every sail she has is then aback: the
        # brig brought to from a run so went astern at a knot and a half for as long as
        # she lay. By the wind already they do not move.
        head, after = head_and_after_yards(self.ship)
        sharp = sharp_up_targets(self.ship, head, after)
        self.full = [y for y in working_yards(self.ship) if y not in self.yards]
        braced_up = any(
            abs(self.sign * sharp.get(y.id, y.brace_limit) - y.brace_angle) > units.deg_to_rad(3.0)
            and self.ship.sail_of(y) is not None
            and self.ship.sail_of(y).is_set
            for y in self.full
        )
        self.swing = YardSwing(
            self.yards + self.full,
            [-self.sign * y.brace_limit for y in self.yards]
            + [self.sign * sharp.get(y.id, y.brace_limit) for y in self.full],
            self.timing_value("brace_s", 45.0),
        )
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 15.0))
        dyn.steady = False
        self.phase = "back_after_yards"
        courses = [sl for sl in lowest_square_sails(self.ship) if sl.is_set]
        for sl in courses:
            sl.state = SailState.IN_THE_GEAR
        drivers = after_gaff_sails(self.ship)
        # The driver: brailed up on a ship whose backed yards are amidships and whose
        # mizzen topsail, full, balances her (package 10; the frigate with it set came head
        # to wind with sternway). Kept, with its sheet eased, on a vessel whose backed
        # yards are on her aftermost mast (a brig's main): no square sail is then full
        # abaft the backed one, and brailed up she falls off to a run (package 32e; Luce
        # 1866, ch. XXVI: "regulate by easing off ... the spanker ... sheets").
        eased: list[Sail] = []
        with_yards = _masts_with_yards(self.ship)
        backed_masts = {self.ship.mast_of(y).id for y in self.yards if self.ship.mast_of(y)}
        aftermost = min(with_yards, key=lambda m: m.x_m).id if with_yards else None
        if drivers and aftermost in backed_masts and len(with_yards) > 1:
            eased = drivers
            draw_sheets(self.ship, drivers, None, HOVE_TO_DRIVER_APPARENT)
            drivers = []
        for sl in drivers:
            sl.state = SailState.IN_THE_GEAR
        words = []
        if courses:
            words.append("hauled up the courses")
        if drivers:
            words.append(f"brailed up {names_of_sails(self.ship, drivers)}")
        if eased:
            sheet = names_of_sails(self.ship, eased).replace("the ", "")
            words.append(f"eased off the {sheet} sheet")
        if words:
            text = "; ".join(words) + "."
            self.note(text[0].upper() + text[1:])
        light = light_sails_forward_of(self.ship, self.yards)
        for sl in light:
            sl.state = SailState.IN_THE_GEAR
        if light:
            self.note(f"Clewed up {names_of_sails(self.ship, light)}.")
        self.headsail = None
        if self.fore_and_after():
            # the fore-and-after's way (Luce 1884, ch. XXXIV, 'To Heave to'): the main
            # sheet flat aft, the staysail sheet to windward, the helm down
            self.headsail = innermost_head_sail(self.ship, standing=True)
            booms = boom_sails(self.ship)
            sheets_to(self.ship, booms, None, None)
            if self.headsail is not None:
                sheets_to(self.ship, [self.headsail], "weather", None)
            words = []
            if booms:
                boom_names = names_of_sails(self.ship, booms).replace("the ", "")
                words.append(f"Hauled flat aft the {boom_names} sheet")
            if self.headsail is not None:
                words.append(f"{names_of_sails(self.ship, [self.headsail])} sheet to windward")
            if self.yards:
                words.append(f"braced the {self._backed_name()} aback")
            text = "; ".join(words) + "; helm a-lee."
            self.note(text[0].upper() + text[1:])
        else:
            # "regulate by easing off, or hauling aft, the spanker and jib sheets" (Luce
            # 1866, ch. XXVI): the head sheets hauled aft, so that the jibs draw as she
            # comes up and hold her head off (package 32e, measured on the frigate: with
            # them eased she came head to wind and gathered sternway; hauled aft she lies
            # five points off at a knot, truth 12)
            sheets_to(self.ship, head_sails(self.ship), None, None)
            up = "; braced up the other yards" if braced_up else ""
            self.note(
                f"Braced the {self._backed_name()} aback{up}; hauled aft the "
                "head sheets; helm a-lee."
            )
        # The other fore-and-aft sails that stay drawing (the staysails abaft the fore
        # mast, a schooner's foresail, a fore-and-after's jib): a sheet eased for a wind
        # free is hauled aft to the trim of a wind six points on the bow, where she is to
        # lie ("hauling aft the head sheets", Luce 1884, ch. XXVI, of heaving to with the
        # wind on the quarter). Left eased they shake when she has come to, and the
        # schooner brought to from a run went astern for it (package 37f). One held on
        # the weather side (a ship that has been taken aback and come round with her
        # sheets where they were) is shifted over to leeward the same way.
        others = shifted_sails(self.ship)
        if self.fore_and_after():
            others += [sl for sl in head_sails(self.ship) if sl is not self.headsail]
        lee = _lee_name(self.sign)
        for sl in others:
            wanted = yard_trim.wanted_sheet_angle(sl.cls, HOVE_TO_DRIVER_APPARENT)
            reading = yard_trim.read_sheet(self.ship, sl)
            eased = reading.angle > wanted + units.deg_to_rad(1.0)
            if reading.free or reading.held_to_windward or eased:
                yard_trim.set_sheet_angle(self.ship, sl, min(reading.angle, wanted), lee)
                sl.shivering = False
        self.info = {"yards": [y.id for y in self.yards], "sign": self.sign}
        if self.headsail is not None:
            self.info["headsail"] = self.headsail.id

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        assert self.swing is not None
        dyn = self.ship.dyn
        if self.info is None:  # begun under an earlier build: the record as it wrote it
            self.info = {"yards": [y.id for y in self.yards], "sign": self.sign}
            if self.headsail is not None:
                self.info["headsail"] = self.headsail.id
        swung = self.swing.advance(dt, factor)
        # the helm and the sheets tended from the first: eased as she comes up, so that
        # her way does not carry her head through the wind (the hands at the braces and
        # the sheets are the evolution's own)
        self.off = tend_lying_to(self.ship, self.info, dt, wind, self.timing, nearer=False)
        if not swung:
            return
        self.phase = "take_way_off"
        near = self.timing_value("near_points", 4.0) * POINT
        far = self.timing_value("far_points", 7.0) * POINT
        way = units.ms_to_knots(abs(dyn.u))
        quiet = abs(dyn.r) <= units.deg_to_rad(self.timing_value("quiet_deg_s", 0.25))
        # her way off: under `way_off_kn`, or no longer falling (a fore-and-after hove to
        # forereaches a knot or two in a breeze, and that is her way of lying to)
        self.slowing = 0.9 * self.slowing + 0.1 * (self.way_was - way) / max(dt, 1e-9)
        self.way_was = way
        off_kn = self.timing_value("way_off_kn", 1.5)
        most_kn = self.timing_value("way_most_kn", 4.5)
        ahead_kn = units.ms_to_knots(dyn.u)
        settled = (
            abs(self.slowing) <= self.timing_value("way_steady_kn_s", 0.004)
            and -off_kn < ahead_kn < most_kn
        )
        way_off = way < off_kn or settled
        if near <= self.off <= far and way_off and quiet:
            self.quiet_s += dt
        else:
            self.quiet_s = 0.0
        if self.quiet_s >= self.timing_value("lie_s", 20.0):
            self._hove_to()
        elif self.t >= self.timing_value("way_off_timeout_s", 600.0):
            if POINT < self.off < 8 * POINT and way < most_kn:
                self._hove_to()  # on her tack, the wind before the beam: she lies to
            else:
                dyn.target_rudder = 0.0
                self.fail(
                    f"she would not lie to on the {_tack_name(self.sign)} tack, the wind "
                    f"{units.wind_bearing_words(wind_rel(self.ship, wind))}; the "
                    f"{self._backed_name()} left aback and the helm amidships"
                    if self.yards
                    else f"she would not lie to on the {_tack_name(self.sign)} tack; the helm "
                    "amidships"
                )

    def _hove_to(self) -> None:
        self.ship.extra["hove_to"] = self.info
        self.finish()

    def remaining_s(self) -> float:
        brace = self.swing.remaining_s() if self.swing else self.timing_value("brace_s", 45.0)
        if self.phase == "take_way_off":
            return max(0.0, self.timing_value("lie_s", 20.0) - self.quiet_s)
        return brace + self.timing_value("lie_s", 20.0)

    def words(self) -> dict[str, Any]:
        tack = _tack_name(self.sign)
        if not self.yards and getattr(self, "headsail", None) is not None:
            from freesail.evolutions.runner import part_name  # local import to avoid a cycle

            backed = part_name(self.ship, self.headsail.id) + " sheet to windward,"
            return {"backed": backed, "hove_tack": tack}
        return {"backed": self._backed_name(), "hove_tack": tack}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d.update(
            {
                "tack": _tack_name(self.sign),
                "off_points": round(units.rad_to_points(self.off), 1),
                "speed_kn": round(units.ms_to_knots(self.ship.dyn.u), 1),
            }
        )
        return d


class FillAwayScript(Script):
    """Fill away after lying to (Luce 1866 ch. XXVI 'To fill away, after lying
    to with the main topsail to the mast': 'Right the helm, haul aft the head
    sheets ... As she falls off, brace up the after yards ... and trim to the
    course'). Hove to she lies close to the wind with little way or some
    sternway; braced full from there she is only taken aback. So first she is
    let fall off: the helm is kept a-lee while she has sternway (the rudder
    then throws her head off) and put up once she gathers headway, until her
    head is ``fill_off_deg`` off the true wind (far enough for the backed
    sails to fill when braced) or ``fall_off_timeout_s`` has passed. Lying
    hove to as heave_to leaves her, five points off, she needs no falling
    off and is braced at once. Then every yard that is aback is braced round
    full over ``brace_s`` and the helm given its course. The courses and driver
    that heaving to hauled up stay as they are: setting them again is the
    captain's order.

    Package 37f (the review's 5.8 and 10.3: "fill away picks the old course or the wrong
    tack"): she is filled on the tack she is on, the side the wind is on now, and not on
    the tack the record says she hove to on; a ship that had put herself about was taken
    back through the wind by it with every sail aback, three times in game 9. The yards
    braced round are those that are aback for that tack, whichever mast they are on.
    `fill away and steer <course>` (`params["course_deg"]`): when she is full the helm
    has that course, if it can be laid on the tack she is on (more than half a point
    outside close-hauled, the wind on the same side). She is braced full by the wind
    first, as with no course, and then pays off to it, her yards and sheets trimmed to
    the wind she has every `retrim_s` as it draws aft (Luce: "As she falls off ... trim to
    the course"), and to the course's own wind when her head is within half a point of
    it or `pay_off_timeout_s` has passed; braced at once for a course with the wind
    abaft the beam, as this first did, the frigate's topsails lifted with her head
    still five points from the wind and the log said "Her sails aback". A course that
    cannot be laid so is said, and she is kept full and by on her tack. With no course
    she is steered close-hauled on her tack, as before."""

    # class defaults for the fields package 37f added (a checkpoint from an earlier build)
    course: float | None = None
    not_laid = ""
    signed = False
    phase_t = 0.0
    retrim_in = 0.0
    last_trim = False

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.yards: list[Spar] = working_yards(ship)
        self.swing: YardSwing | None = None
        self.new_course = ship.dyn.heading
        course = params.get("course_deg")
        self.course: float | None = (
            None if course is None else units.wrap_2pi(units.deg_to_rad(float(course)))
        )
        self.not_laid = ""  # why the course said could not be given her, in words
        self.signed = False  # the tack read from the true wind, at the first tick

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards}

    def check(self, words: dict[str, Any]) -> str | None:
        if "hove_to" not in self.ship.extra:
            return "She is not hove to."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        ch = close_hauled_true_angle(self.ship)
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.new_course = units.wrap_2pi(estimated_wind_from(self.ship) - self.sign * ch)
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 20.0))
        dyn.steady = False
        self.phase = "fall_off"
        # the watch's tending ends here: the hands at the sheets are the evolution's
        lying_to_hands_off(self.ship)
        # the head sheets hauled aft (Luce 1866, ch. XXVI): a head sail held to windward
        # to heave to (package 32e) is let draw, and the boom sails trimmed to the wind,
        # on the lee side of the tack she is on
        drawn = head_sails(self.ship)
        draw_sheets(self.ship, drawn + boom_sails(self.ship), _lee_name(self.sign))
        self.note(
            "Hauled aft the head sheets; kept the helm a-lee to let her fall off.", "helm.order"
        )

    def _course_for(self, wind: Wind) -> float:
        """The course she is given when full: the one said, if it can be laid on the tack
        she is on; else close-hauled on it, and `not_laid` says why."""
        ch = close_hauled_true_angle(self.ship)
        by_the_wind = units.wrap_2pi(wind.direction_from - self.sign * ch)
        if self.course is None:
            return by_the_wind
        # the wind's bearing on her bow when she is on the course, on this tack's side
        off = self.sign * units.wrap_pi(wind.direction_from - self.course)
        said = units.format_heading(self.course)
        tack = _tack_name(self.sign)
        if off < 0.0:
            self.not_laid = (
                f"{said} lies on the other tack; she is kept full and by on the {tack} "
                f"tack: tack or wear for it"
            )
            return by_the_wind
        if off < ch + 0.5 * POINT:
            self.not_laid = (
                f"{said} lies too near the wind to be laid; she is kept full and by on "
                f"the {tack} tack"
            )
            return by_the_wind
        self.not_laid = ""
        return self.course

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        if not self.signed and abs(rel) > 0.5 * POINT:
            # the tack she is on, by the wind itself (the deck's reading lags a ship that
            # has just come round)
            self.signed = True
            sign = 1.0 if rel > 0 else -1.0
            if sign != self.sign:
                self.sign = sign
                draw_sheets(
                    self.ship,
                    head_sails(self.ship) + boom_sails(self.ship),
                    _lee_name(self.sign),
                )
        self.new_course = self._course_for(wind)
        if self.phase == "fall_off":
            helm = units.deg_to_rad(self.timing_value("helm_deg", 20.0))
            # with sternway the rudder works the other way: the helm a-lee throws
            # her head off; with headway it is the helm up that does it
            dyn.target_rudder = self.sign * helm if dyn.u < 0.0 else -self.sign * helm
            wanted = units.deg_to_rad(self.timing_value("fill_off_deg", 55.0))
            fallen_off = self.sign * rel >= wanted
            if fallen_off or self.t >= self.timing_value("fall_off_timeout_s", 180.0):
                self.phase = "brace_full"
                aback = _yards_aback_for(self.ship, self.sign)
                what = sail_name_on(self.ship, aback) if aback else "yards"
                if self.t > 1.0:
                    self.note(f"Fallen off; braced the {what} full.")
                else:
                    self.note(f"Braced the {what} full.")
                head, after = head_and_after_yards(self.ship)
                sharp = sharp_up_targets(self.ship, head, after)
                # every yard that is aback, or braced up for the other tack with nothing
                # set, is braced round for this tack, sharp up by the wind (the after
                # yards the sharper, spec 3b §2.2): full for where her head is now,
                # whatever course she is to have
                swung: list[Spar] = []
                targets: list[float] = []
                for y in self.yards:
                    if y.brace_angle * self.sign >= 0.0 and y not in aback:
                        continue  # full on this tack already: left as it is
                    swung.append(y)
                    targets.append(self.sign * sharp.get(y.id, y.brace_limit))
                self.swing = YardSwing(swung, targets, self.timing_value("brace_s", 45.0))
                dyn.helm_mode = HelmMode.HEADING
                dyn.target_heading = self.new_course
                dyn.target_rudder = 0.0
                dyn.steady = False
            return
        if self.course is None or self.not_laid:
            dyn.target_heading = self.new_course  # by the wind: the wind's own point
        if self.phase == "pay_off":
            self._pay_off(dt, wind, factor, rel)
            return
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            ch = close_hauled_true_angle(self.ship)
            on_course = self.sign * units.wrap_pi(wind.direction_from - self.new_course)
            if self.course is not None and not self.not_laid and on_course > ch + 0.5 * POINT:
                # full: now she pays off to the course ordered, trimmed as she goes
                dyn.target_heading = self.new_course
                self.phase = "pay_off"
                self.phase_t = 0.0
                self.retrim_in = 0.0
                self.swing = None
                return
            end_lying_to(self.ship)
            self.finish()

    def _pay_off(self, dt: float, wind: Wind, factor: float, rel: float) -> None:
        """Full and gathering way, she pays off to the course ordered: her yards and
        sheets trimmed to the wind on her bow as it draws aft, and to the course's own
        wind at the last."""
        ship = self.ship
        dyn = ship.dyn
        dyn.target_heading = self.new_course
        self.phase_t += dt
        self.retrim_in -= dt
        if self.swing is not None and self.swing.advance(dt, factor):
            self.swing = None
        if self.last_trim:
            if self.swing is None:
                end_lying_to(ship)
                self.finish()
            return
        ch = close_hauled_true_angle(ship)
        on_course = self.sign * units.wrap_pi(wind.direction_from - self.new_course)
        now = self.sign * rel
        there = now >= on_course - 0.5 * POINT
        late = self.phase_t >= self.timing_value("pay_off_timeout_s", 240.0)
        if there or late:
            aim = on_course if there else max(ch, min(now, on_course))
            self.last_trim = True  # done when this swing is
        elif self.retrim_in > 0.0:
            return
        else:
            aim = max(ch, min(now, on_course))
            self.retrim_in = self.timing_value("retrim_s", 20.0)
        every = self.timing_value("retrim_s", 20.0)
        targets = [trim_angle(self.sign * aim, y.brace_limit, ch) for y in self.yards]
        self.swing = YardSwing(list(self.yards), targets, every)
        draw_sheets(ship, head_sails(ship) + boom_sails(ship), _lee_name(self.sign), aim)

    def remaining_s(self) -> float:
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "fall_off":
            return max(0.0, self.timing_value("fall_off_timeout_s", 180.0) - self.t) + brace_s
        if self.phase == "pay_off":
            return max(0.0, self.timing_value("pay_off_timeout_s", 240.0) - self.phase_t)
        return self.swing.remaining_s() if self.swing else brace_s

    def words(self) -> dict[str, Any]:
        course = units.format_heading(self.new_course)
        if self.not_laid:
            course_words = f"steering {course}, full and by ({self.not_laid})"
        elif self.course is not None:
            course_words = f"steering {course}, the course ordered"
        else:
            course_words = f"steering {course}"
        return {
            "new_course": course,
            "filled_tack": _tack_name(self.sign),
            "course_words": course_words,
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d.update(
            {
                "tack": _tack_name(self.sign),
                "course_deg": round(units.rad_to_deg(self.new_course), 1),
                "course_ordered": self.course is not None and not self.not_laid,
                "not_laid": self.not_laid,
            }
        )
        return d


# ---------------------------------------------------------------------------
# Milestone 3, package 19: the catalogue to forty
# ---------------------------------------------------------------------------
#
# The scripts below do crew work that one step list cannot express, because it
# changes several parts at once (every topgallant mast and the yards on it),
# keeps a count (the spare sails in the sail room) or steers the ship. Each
# follows the contract above: its timings come from the file's `timing:`
# block (`<phase>_s`), it keeps `status` and `reason`, it says which parts it
# `holds()`, and it reports its `data()`. It gives orders (helm targets, brace
# angles, sail states) and reads the compass; it never touches the physics.
#
# Work aloft: a phase named in the file's `params.aloft` list is work on the
# yards or in the tops, and `script.aloft` is true while it runs, so that the
# crew factor (spec M3 §3.3) can use the hands' skill aloft for it.

MAST_CLASSES = frozenset({"mast", "topmast", "topgallant_mast", "royal_mast"})
DRAWING = frozenset({SailState.SET, SailState.SHEETED, SailState.GOOSE_WINGED})
HANGING = frozenset({SailState.LOOSED, SailState.IN_THE_GEAR})
DEFAULT_SPARE_SAILS = parts.DEFAULT_SPARE_SAILS  # made-up sails when the file gives no stores


def _names(ship: Ship, parts: list) -> str:
    """'the fore royal', 'the fore royal and the main royal', for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    names = [f"the {part_name(ship, p.id)}" for p in parts]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _in_ship_order(ship: Ship, parts: list) -> list:
    order = {pid: i for i, pid in enumerate(ship.parts)}
    seen: dict[str, Any] = {}
    for p in parts:
        seen.setdefault(p.id, p)
    return sorted(seen.values(), key=lambda p: order.get(p.id, 0))


def _nearest_mast(ship: Ship, part: Any) -> Spar | None:
    """The mast, topmast, topgallant mast or royal mast a part is carried on."""
    for sp in ship.spar_chain(part):
        if sp.cls in MAST_CLASSES:
            return sp
    return None


def _chain_standing(ship: Ship, part: Any) -> bool:
    """True when nothing the part stands on is wrecked or sent down."""
    return not any(sp.wrecked or sp.sent_down for sp in ship.spar_chain(part))


def _spar_words(ship: Ship, spars: list[Spar], mast_cls: str) -> str:
    """The spars for the log, without the poles and booms that go with them:
    'the fore topgallant yard and the fore royal yard, with their studding sail
    booms', 'the fore topgallant mast and the main topgallant mast'."""
    heads = [s for s in spars if s.cls == mast_cls]
    if heads:
        return _names(ship, heads)
    yards = [s for s in spars if s.is_yard]
    booms = [s for s in spars if s.cls == "studdingsail_boom"]
    text = _names(ship, yards or spars)
    if yards and booms:
        text += ", with their studding sail booms"
    return text


def mast_inventory(ship: Ship) -> str:
    """What masts she has, for a refusal: 'the fore mast and fore topmast, and the
    main mast and main topmast'."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    groups: list[str] = []
    for lower in ship.spars.values():
        if lower.cls != "mast":
            continue
        chain = [lower] + [
            d for d in ship.dependents(lower) if isinstance(d, Spar) and d.cls in MAST_CLASSES
        ]
        names = [part_name(ship, m.id) for m in _in_ship_order(ship, chain)]
        groups.append(
            "the " + (names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1])
        )
    if not groups:
        return "she has no masts"
    return "her masts are " + (
        groups[0] if len(groups) == 1 else ", ".join(groups[:-1]) + ", and " + groups[-1]
    )


def spare_sails(ship: Ship) -> int:
    """The sails in the sail room, counted (spec M3 §6; spec 3b §6.3 keeps the count).

    The room itself is `parts.sail_room(ship)`: the ship file's list of sails
    (`crew.stores.sails`), or for a file that gives only `spare_sails` that many
    made-up sails that fit any yard, else DEFAULT_SPARE_SAILS of them. The count
    is also kept in ``ship.extra["spare_sails"]`` for anything that reads it."""
    return len(parts.sail_room(ship))


def _subject_sail(ship: Ship, params: dict[str, Any], words: dict[str, Any] | None):
    """The sail a sail script works on: `params["sail"]` (the verbs pass it), or
    the subject the runner names in its words."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    sid = params.get("sail")
    if isinstance(sid, str) and sid in ship.sails:
        return ship.sails[sid]
    name = (words or {}).get("subject")
    for sail in ship.sails.values():
        if part_name(ship, sail.id) == name:
            params["sail"] = sail.id
            return sail
    return None


class PhasedScript(Script):
    """Work done in named phases, one after another. Each phase takes
    ``timing[<phase>_s]`` seconds (else the class default) stretched by the
    factor the runner passes. A subclass lists its phases in ``begin`` with
    ``start_phases`` and says in ``end_phase`` what each one changes; a phase
    that has nothing to do is simply left out of the list."""

    DEFAULTS: dict[str, float] = {}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.plan: list[str] = []
        self.index = -1
        self.progress = 0.0
        self.aloft_phases = frozenset(str(p) for p in (params.get("aloft") or ()))

    @property
    def aloft(self) -> bool:
        """True while the phase under way is work aloft (the file's `params.aloft`)."""
        return self.phase in self.aloft_phases

    def phase_s(self, name: str) -> float:
        return self.timing_value(f"{name}_s", self.DEFAULTS.get(name, 60.0))

    def start_phases(self, phases: list[str]) -> None:
        self.plan = list(phases)
        self.index = -1
        self._next_phase()

    def _next_phase(self) -> None:
        self.index += 1
        self.progress = 0.0
        if self.index >= len(self.plan):
            self.phase = "done"
            self.finish()
            return
        self.phase = self.plan[self.index]
        self.start_phase(self.phase)

    def start_phase(self, name: str) -> None:
        """Called as a phase begins; nothing by default."""

    def end_phase(self, name: str) -> None:
        """Called as a phase ends: apply what it did."""

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        if self.status != "running" or not (0 <= self.index < len(self.plan)):
            return
        duration = self.phase_s(self.phase)
        if duration <= 0:
            self.progress = 1.0
        else:
            self.progress = min(1.0, self.progress + dt / (duration * factor))
        if self.progress >= 1.0 - 1e-9:
            self.end_phase(self.phase)
            if self.status == "running":
                self._next_phase()

    def remaining_s(self) -> float:
        if not (0 <= self.index < len(self.plan)):
            return 0.0
        this = (1.0 - self.progress) * self.phase_s(self.phase)
        return this + sum(self.phase_s(p) for p in self.plan[self.index + 1 :])

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["aloft"] = self.aloft
        return d


# ---------------------------------------------------------------------------
# Sending spars down and up: topgallant masts, their yards, topmasts
# ---------------------------------------------------------------------------


class _Rig:
    """The upper spars of one class across the ship: for each mast of the class
    (the *head*), the masts that go with it (a royal pole on a topgallant mast),
    the yards and booms they carry, and the sails bent or hanked to them."""

    def __init__(self, ship: Ship, mast_cls: str, poles: tuple[str, ...]):
        self.heads: list[Spar] = [
            s for s in ship.spars.values() if s.cls == mast_cls and not s.wrecked
        ]
        self.group: dict[str, list[Spar]] = {}
        self.yards: dict[str, list[Spar]] = {}
        self.sails: dict[str, list] = {}
        self.above: dict[str, list[Spar]] = {}
        for head in self.heads:
            deps = ship.dependents(head)
            group = [head] + [
                d for d in deps if isinstance(d, Spar) and d.cls in poles and not d.wrecked
            ]
            ids = {m.id for m in group}
            carried = [d for d in deps if isinstance(d, Sail) and not d.wrecked]
            yards = [
                d
                for d in deps
                if isinstance(d, Spar)
                and d.cls not in MAST_CLASSES
                and not d.wrecked
                and (_nearest_mast(ship, d) or head).id in ids
            ]
            sails = [
                s for s in carried if (m := _nearest_mast(ship, s)) is not None and m.id in ids
            ]
            self.group[head.id] = _in_ship_order(ship, group)
            self.yards[head.id] = _in_ship_order(ship, yards)
            self.sails[head.id] = _in_ship_order(ship, sails)
            self.above[head.id] = _in_ship_order(
                ship,
                [
                    d
                    for d in deps
                    if isinstance(d, Spar)
                    and d.cls in MAST_CLASSES
                    and d.id not in ids
                    and not d.wrecked
                ],
            )

    def held(self, sails: bool = True) -> set[str]:
        """What a send-down or sway-up holds against other evolutions: the masts,
        and the sails on them unless ``sails`` is false. Held, a sail being set
        is finished first and one ordered meanwhile waits. Sending down the
        topgallant masts holds the masts alone and belays the sail work in hand on
        those masts' sails instead of waiting for it (`Script.clears`): the masts
        come down, and a royal cannot be set on a mast being struck; what was
        belayed is refused when it takes up again on a spar sent down. The rest of
        the sail work in hand runs on: all hands is a pool action (the owner's
        ruling of 2026-09-29 at gate 4c, spec M3 §3.4). Not the yards: a brace on
        one is harmless, and one ordered after it is down is refused."""
        out: set[str] = set()
        for head in self.heads:
            out |= {p.id for p in self.group[head.id]}
            if sails:
                out |= {p.id for p in self.sails[head.id]}
        return out


class SendDownScript(PhasedScript):
    """Send down upper spars: the topgallant and royal yards, the topgallant
    masts with them, or the topmasts (Luce 1884, ch. XX 'To send down topgallant
    and royal yards and topgallant masts'; ch. XXIX 'Preparations for a Gale':
    "send down top-gallant masts ... as it eases her considerably").

    The file's params say which: ``mast`` (the class of mast, e.g.
    ``topgallant_mast``), ``poles`` (classes that go down with it, e.g. the
    royal mast), ``with_masts`` (false to send down only the yards on them),
    ``clear_away`` (true to clew up anything still set first; false to refuse
    instead) and the words for the log (``what``, ``doing``, ``first``).

    Phases: ``clear_away`` (clew up what is drawing on those spars),
    ``yards`` (the yards and booms sent down, their sails furled on them),
    ``mast`` (unfid and lower the masts). Everything sent down is marked
    ``sent_down``; the strain model then puts no load on it, the physics no
    windage, and nothing on it can be set until it is swayed up again."""

    DEFAULTS = {"clear_away": 60.0, "yards": 300.0, "mast": 420.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.mast_cls = str(params.get("mast") or "topgallant_mast")
        self.poles = tuple(str(p) for p in (params.get("poles") or ()))
        self.with_masts = bool(params.get("with_masts", True))
        self.clear_away = bool(params.get("clear_away", True))
        self.rig = _Rig(ship, self.mast_cls, self.poles)
        self.masts: list[Spar] = []
        self.yards: list[Spar] = []
        self.sails: list = []
        self.clew: list = []
        self.sent: list[Spar] = []

    def holds(self) -> set[str]:
        return {self.ship.name} | self.rig.held(bool(self.params.get("hold_sails", True)))

    def clears(self) -> set[str]:
        if bool(self.params.get("hold_sails", True)):
            return set()
        return self.rig.held(sails=True) - self.rig.held(sails=False)

    def _what(self) -> str:
        return str(self.params.get("what") or self.mast_cls.replace("_", " ") + "s")

    def _survey(self) -> None:
        """What is still aloft to be sent down, now."""
        self.rig = _Rig(self.ship, self.mast_cls, self.poles)
        heads = [h for h in self.rig.heads if not h.sent_down]
        self.masts, self.yards, self.sails = [], [], []
        for h in heads:
            if self.with_masts:
                self.masts += [m for m in self.rig.group[h.id] if not m.sent_down]
                self.sails += self.rig.sails[h.id]
                self.yards += [y for y in self.rig.yards[h.id] if not y.sent_down]
            else:
                self.yards += [y for y in self.rig.yards[h.id] if not y.sent_down]
                yard_ids = {y.id for y in self.yards}
                self.sails += [
                    s
                    for s in self.rig.sails[h.id]
                    if (chain := self.ship.spar_chain(s)) and chain[0].id in yard_ids
                ]
        self.clew = [s for s in self.sails if s.state in DRAWING]

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        what = self._what()
        verb = str(self.params.get("verb_words") or "send down")
        if not self.rig.heads:
            return f"She has no {what} to {verb}; {mast_inventory(ship)}."
        self._survey()
        if self.with_masts and not self.masts:
            return f"The {what} are sent down already."
        if not self.with_masts:
            if all(h.sent_down for h in self.rig.heads):
                masts = self.mast_cls.replace("_", " ") + "s"
                return f"The {masts} are on deck; there are no yards aloft on them to {verb}."
            if not self.yards:
                return f"The {what} are on deck already."
        standing = [
            m
            for h in self.rig.heads
            if not h.sent_down
            for m in self.rig.above[h.id]
            if not m.sent_down and m.parent == h.id  # the mast stepped on it, not its pole
        ]
        if standing:
            first = str(self.params.get("first") or "send down the masts above")
            return (
                f"{first[:1].upper()}{first[1:]} first: {_names(ship, standing)} "
                f"{'is' if len(standing) == 1 else 'are'} still aloft."
            )
        if not self.clear_away and self.clew:
            doing = str(self.params.get("doing") or f"{verb}ing the {what}")
            return (
                f"{_names(ship, self.clew)[:1].upper()}{_names(ship, self.clew)[1:]} "
                f"{'is' if len(self.clew) == 1 else 'are'} set; take "
                f"{'it' if len(self.clew) == 1 else 'them'} in before {doing}."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self._survey()
        phases = []
        if self.clew:
            phases.append("clear_away")
            self.note(f"Clew up {_names(self.ship, self.clew)}; stand by to send down.")
        if self.yards:
            phases.append("yards")
        if self.masts:
            phases.append("mast")
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "clear_away":
            for s in self.clew:
                if s.state in DRAWING:
                    s.state = SailState.IN_THE_GEAR
            self.note(f"Clewed up {_names(ship, self.clew)}; hands aloft to send down.")
        elif name == "yards":
            for y in self.yards:
                y.sent_down = True
                y.brace_angle = 0.0
            yard_ids = {y.id for y in self.yards}
            for s in self.sails:
                chain = ship.spar_chain(s)
                if chain and chain[0].id in yard_ids:
                    self._stow(s)
            self.sent += self.yards
            self.note(f"Sent down on deck {_spar_words(ship, self.yards, self.mast_cls)}.")
        elif name == "mast":
            for s in self.sails:
                self._stow(s)
            for m in self.masts:
                m.sent_down = True
            self.sent += self.masts
            self.note(f"Unfidded and lowered away {_spar_words(ship, self.masts, self.mast_cls)}.")

    @staticmethod
    def _stow(sail) -> None:
        if sail.state not in (SailState.UNBENT, SailState.BLOWN_OUT):
            sail.state = SailState.FURLED

    def words(self) -> dict[str, Any]:
        return {"sent": _spar_words(self.ship, self.sent, self.mast_cls)}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["sent_down"] = [p.id for p in self.sent]
        return d


class SwayUpScript(PhasedScript):
    """Sway up and fid what SendDownScript sent down: the topgallant masts and
    their yards, the yards alone, or the topmasts (Luce 1884, ch. XX 'To send up
    topgallant masts and topgallant and royal yards': "Sway aloft and fid ...
    Sway across! Bend the gear!"). Params as for SendDownScript; ``below``
    names the order that must come first when the mast below is struck.

    Phases: ``mast`` (sway aloft and fid) and ``yards`` (cross the yards,
    square). The sails come up furled on their yards, to be set by order."""

    DEFAULTS = {"mast": 480.0, "yards": 360.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.mast_cls = str(params.get("mast") or "topgallant_mast")
        self.poles = tuple(str(p) for p in (params.get("poles") or ()))
        self.with_masts = bool(params.get("with_masts", True))
        self.rig = _Rig(ship, self.mast_cls, self.poles)
        self.masts: list[Spar] = []
        self.yards: list[Spar] = []
        self.crossed: list[Spar] = []

    def holds(self) -> set[str]:
        return {self.ship.name} | self.rig.held(bool(self.params.get("hold_sails", True)))

    def clears(self) -> set[str]:
        if bool(self.params.get("hold_sails", True)):
            return set()
        return self.rig.held(sails=True) - self.rig.held(sails=False)

    def _what(self) -> str:
        return str(self.params.get("what") or self.mast_cls.replace("_", " ") + "s")

    def _survey(self) -> None:
        self.rig = _Rig(self.ship, self.mast_cls, self.poles)
        self.masts, self.yards = [], []
        for h in self.rig.heads:
            if self.with_masts:
                if not h.sent_down:
                    continue
                self.masts += [m for m in self.rig.group[h.id] if m.sent_down]
                self.yards += [y for y in self.rig.yards[h.id] if y.sent_down]
            elif not h.sent_down:
                self.yards += [y for y in self.rig.yards[h.id] if y.sent_down]

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        what = self._what()
        verb = str(self.params.get("verb_words") or "sway up")
        if not self.rig.heads:
            return f"She has no {what} to {verb}; {mast_inventory(ship)}."
        self._survey()
        if not self.with_masts and all(h.sent_down for h in self.rig.heads):
            masts = self.mast_cls.replace("_", " ") + "s"
            return f"The {masts} are on deck; sway them up before crossing the yards."
        if not self.masts and not self.yards:
            return f"The {what} are aloft already."
        struck = []
        for m in self.masts:
            below = ship.parent_of(m)
            if below is not None and below.id not in {x.id for x in self.masts}:
                if below.sent_down or below.wrecked:
                    struck.append(below)
        if struck:
            first = str(self.params.get("below") or "sway up the masts below")
            return (
                f"{first[:1].upper()}{first[1:]} first: {_names(ship, struck)} "
                f"{'is' if len(struck) == 1 else 'are'} struck."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self._survey()
        phases = []
        if self.masts:
            phases.append("mast")
            what = _spar_words(self.ship, self.masts, self.mast_cls)
            self.note(f"Man the mast-ropes; sway aloft {what}.")
        if self.yards:
            phases.append("yards")
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "mast":
            for m in self.masts:
                m.sent_down = False
            self.crossed += self.masts
            what = _spar_words(ship, self.masts, self.mast_cls)
            self.note(f"Swayed aloft and fidded {what}; set up the rigging.")
        elif name == "yards":
            for y in self.yards:
                y.sent_down = False
                y.brace_angle = 0.0
            self.crossed += self.yards
            self.note(f"Crossed {_spar_words(ship, self.yards, self.mast_cls)}; bent the gear.")

    def words(self) -> dict[str, Any]:
        return {"swayed": _spar_words(self.ship, self.crossed, self.mast_cls)}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["swayed_up"] = [p.id for p in self.crossed]
        return d


# ---------------------------------------------------------------------------
# Bending, unbending and shifting a sail
# ---------------------------------------------------------------------------
#
# Milestone 3b (package 22, spec 3b §6.3): the sail room holds sails, not a count. A sail
# unbent goes down to it with its canvas number and condition; bending draws the best
# spare of the kind (`parts.SailRoom.choose`), or the one the order names:
#   params["canvas_no"]  a number: "bend the No. 1 fore topsail"
#   params["heavy"]      true: "shift the fore topsail for the heavy one"
#   params["for"]        another sail's id (or name) bent in the subject's place:
#                        "shift the spanker for the storm mizzen"
# A sail bent in place of another (`Sail.in_place_of`: the storm mizzen for the spanker, a
# schooner's storm trysail for her mainsail, her storm jib for the jib) is bent only when
# the other is unbent: the one refusal spec 3b §6.4 names.


def _sail_named(ship: Ship, value: Any) -> Sail | None:
    """A sail by id, alias or a sailor's name for it."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    if not isinstance(value, str) or not value:
        return None
    if value in ship.sails:
        return ship.sails[value]
    target = ship.aliases.get(value)
    if target in ship.sails:
        return ship.sails[target]
    for sail in ship.sails.values():
        if part_name(ship, sail.id) == value:
            return sail
    return None


def _in_each_others_place(a: Sail, b: Sail) -> bool:
    return a.in_place_of == b.id or b.in_place_of == a.id


class _SailWork(PhasedScript):
    """A script on one sail, the evolution's subject. The verbs pass the sail's
    id as `params["sail"]`; without it the sail is found from the runner's
    words. Holds nothing beyond the sail, which the runner holds for it.

    `target` is the sail that is bent (the subject, or the one a shift names
    with `params["for"]`) and `spare` the sail chosen for it from the sail
    room, chosen at the check so that a refusal comes at once."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sail = _subject_sail(ship, params, None)
        self.target: Sail | None = None
        self.spare: parts.SpareSail | None = None

    def holds(self) -> set[str]:
        return set()

    # Unbending takes a sail out of a wreck (package 30b); bending and shifting want its
    # spars standing
    WORKS_IN_A_WRECK = False

    def _find(self, words: dict[str, Any]) -> str | None:
        if self.sail is None:
            self.sail = _subject_sail(self.ship, self.params, words)
        if self.sail is None:
            return "Name the sail to work on."
        ship, sail = self.ship, self.sail
        root = wreck_root(ship, sail)
        if root is not None and (sail.wrecked or not self.WORKS_IN_A_WRECK):
            # the part graph keeps a wreck's consequences until a spare replaces the spar
            # (package 30b): the refusal names the spar and the order that clears it
            return self._wreck_refusal(root)
        if not _chain_standing(ship, sail):
            return f"The {self._name()}'s yard or mast is wrecked or sent down."
        return None

    def _wreck_refusal(self, root: Spar) -> str | None:
        """Why this sail cannot be worked while a spar it needs is carried away, or None
        when it can (a wrecked sail unbent where it hangs: package 30b)."""
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        ship, sail = self.ship, self.sail
        spar = part_name(ship, root.id)
        if not root.sent_down:  # the wreck still hangs
            if root.cls in OVER_THE_SIDE_CLASSES:
                return f"The {self._name()} went over the side with the {spar}; cut away the wreck."
            if self.WORKS_IN_A_WRECK:
                return None  # cut out of the wreck where it hangs and sent down
            if sail.wrecked:
                return (
                    f"The {self._name()} hangs in the wreck of the {spar}; cut away the wreck, "
                    f"then shift the {spar} for a spare."
                )
            return (
                f"The wreck of the {spar} still hangs aloft; cut it away and shift the {spar} "
                f"for a spare before the {self._name()} can be bent."
            )
        gone = gone_spar(ship, sail)
        what = part_name(ship, gone.id) if gone is not None else spar
        return f"The {what} is carried away; shift it for a spare first."

    def _name(self, sail: Sail | None = None) -> str:
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        sail = sail if sail is not None else self.sail
        return part_name(self.ship, sail.id) if sail is not None else "sail"

    def room(self) -> parts.SailRoom:
        return parts.sail_room(self.ship)

    def _rival(self, sail: Sail, but: Sail | None = None) -> Sail | None:
        """A bent sail that holds this one's place (spec 3b §6.4), other than `but`."""
        for other in self.ship.sails.values():
            if other is sail or other is but or other.state is SailState.UNBENT:
                continue
            if _in_each_others_place(sail, other):
                return other
        return None

    def _choose(self, target: Sail) -> str | None:
        """Choose the sail to bend to `target` from the room, or say why there is none."""
        room = self.room()
        name = self._name(target)
        raw_no = self.params.get("canvas_no")
        canvas_no = int(raw_no) if isinstance(raw_no, int | float) and raw_no else None
        heavy = bool(self.params.get("heavy"))
        self.spare = room.choose(target.id, canvas_no=canvas_no, heavy=heavy)
        if self.spare is not None:
            return None
        fits = room.fitting(target.id)
        if not fits:
            return (
                f"There is no spare sail left in the sail room to bend in place of the "
                f"{name}; the sailmaker must make one first."
            )
        there = "; ".join(room.describe(s, target.id)[4:] for s in fits)
        if canvas_no is not None:
            return (
                f"There is no {name} of No. {canvas_no} canvas in the sail room; it holds {there}."
            )
        return f"There is no heavy-weather {name} in the sail room; it holds {there}."

    def _draw(self) -> bool:
        """Take the chosen sail out of the room (choosing again if another evolution has
        taken it meanwhile). False, with the evolution failed, when there is none left."""
        room = self.room()
        if self.spare is None or not any(s is self.spare for s in room.sails):
            reason = self._choose(self.target)
            if reason:
                self.fail(reason)
                return False
        room.take(self.spare)
        self.ship.extra["spare_sails"] = len(room)
        return True

    def _stow(self, sail: Sail) -> None:
        """The unbent sail goes down to the sail room with its canvas and condition."""
        room = self.room()
        room.stow(parts.SpareSail(kind=sail.id, canvas_no=sail.canvas_no, condition=sail.condition))
        self.ship.extra["spare_sails"] = len(room)

    def _bend_spare(self) -> None:
        target = self.target
        target.state = SailState.FURLED
        target.reefs = 0
        spare = self.spare
        target.bend_canvas(
            spare.canvas_no if spare is not None else None,
            spare.condition if spare is not None else 100.0,
        )

    def _spare_words(self) -> str:
        """'No. 1 canvas, new' for the sail chosen."""
        if self.spare is None or self.target is None:
            return "new"
        room = self.room()
        no = room.number_of(self.spare, self.target.id)
        cond = parts.condition_words(self.spare.condition)
        return f"No. {no} canvas, {cond}" if no is not None else cond

    def words(self) -> dict[str, Any]:
        n = spare_sails(self.ship)
        return {
            "spare_sails": f"{n} spare sail{'s' if n != 1 else ''}",
            "bent": self._name(self.target or self.sail),
            "canvas": self._spare_words(),
            # how a shift leaves the new sail: set in a drawing sail's place, else furled
            "left": "set" if getattr(self, "was_drawing", False) else "furled",
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["spare_sails"] = spare_sails(self.ship)
        if self.target is not None:
            d["bent"] = self.target.id
        if self.spare is not None:
            d["canvas_no"] = self.spare.canvas_no
            d["condition"] = self.spare.condition
        return d


class UnbendScript(_SailWork):
    """Unbend a sail from its yard, gaff or stay and send it down (Luce 1884, ch. XX 'To
    unbend sail': "Trice up! Lay out and unbend! ... Ease away! Lower
    together!"). Phases ``unbend`` (aloft: cast off the robands and head
    earings) and ``lower`` (on deck: lower it down by the buntlines and stow
    it). A sound sail goes back to the sail room with its canvas number and
    condition; a blown-out one is condemned and does not."""

    DEFAULTS = {"unbend": 180.0, "lower": 90.0}
    WORKS_IN_A_WRECK = True
    from_wreck = False  # set as the work begins: the sail hung in a wreck

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        sail = self.sail
        if sail.state is SailState.UNBENT:
            return f"The {self._name()} is unbent already; there is no sail on the yard."
        if sail.state in DRAWING and not sail.wrecked:
            # a sail in a wreck hangs to leeward whatever it was doing: its robands and
            # earings are cut where it hangs (Luce 1884, ch. XXXI, 'Topgallant Yard Carried
            # Away': "Cut adrift the clewlines from the clews, cut robands and head earings")
            return f"The {self._name()} is set; take it in before unbending it."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.from_wreck = self.sail.wrecked
        self.start_phases(["unbend", "lower"])

    def end_phase(self, name: str) -> None:
        if name == "lower":
            sound = self.sail.state is not SailState.BLOWN_OUT
            self.sail.state = SailState.UNBENT
            self.sail.reefs = 0
            self.sail.wrecked = False  # out of the wreck: on deck, in the sail room or gone
            self.sail.load_kn = 0.0
            cut = (
                "Cut the {} clear of the wreck, lowered it" if self.from_wreck else "Lowered the {}"
            )
            head = cut.format(self._name())
            if sound:
                self._stow(self.sail)
                self.note(f"{head} on deck and stowed it in the sail room.")
            else:
                self.note(f"{head} down on deck; the rags are condemned.")


class BendScript(_SailWork):
    """Bend a sail from the sail room to a bare yard, gaff or stay (Luce 1884, ch.
    XX 'Bending sail': "Sway aloft! ... Haul out! Lay out! And bring to!").
    Phases ``send_up`` (on deck: rouse the sail up from the sail room and sway
    it aloft) and ``bend`` (aloft: haul out the head, pass the robands and head
    earings, bend the gear). The sail bent is the best of its kind in the room
    or the one the order names, and brings its canvas number and condition to
    the part. It is left furled, to be set by order."""

    DEFAULTS = {"send_up": 120.0, "bend": 240.0}

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        if self.sail.state is not SailState.UNBENT:
            return (
                f"The {self._name()} is bent already ({self.sail.describe_state()}); "
                f"to change it for another, shift it."
            )
        rival = self._rival(self.sail)
        if rival is not None:
            return (
                f"The {self._name(rival)} is bent in the {self._name()}'s place; unbend it first, "
                f"or shift the {self._name(rival)} for the {self._name()}."
            )
        self.target = self.sail
        return self._choose(self.sail)

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["send_up", "bend"])

    def end_phase(self, name: str) -> None:
        if name == "send_up":
            if self._draw():
                self.note(
                    f"Roused up the {self._name()} from the sail room ({self._spare_words()}) "
                    f"and swayed it aloft."
                )
        elif name == "bend":
            self._bend_spare()


class ShiftScript(_SailWork):
    """Shift a sail: take it in if it is drawing, unbend it and bend another in
    its place, and set the new one if the old was drawing. Luce's shift begins
    with the sail set: 'To shift a topsail (by the wind, under all plain sail)'
    opens "Clew up! ... Settle away the topsail halliards ... Lay out! Furl
    and unbend! ... Lower the sail down to leeward by the buntlines. Send up
    the new sail ... Bring to and bend the sail ... Let fall! Sheet home!"
    (Luce 1866, ch. XXXII Shifting Sails and Spars), and 'To shift a jib'
    opens "Haul the sail down". So the phases are ``take_in`` (on deck, only
    for a drawing sail), ``unbend`` (aloft), ``send_up`` (on deck: the old sail
    down to the sail room, unless it is in rags, and the new one up), ``bend``
    (aloft) and ``set`` (only when the old sail was drawing; a furled or
    hauled-up sail is shifted where it hangs and the new one left furled, as
    the port drill has it). The new sail is the best of the kind in the room,
    or the one the order names: a number, the heavy one, or another sail bent
    in this one's place ("shift the spanker for the storm mizzen", Luce 1884
    ch. XXVII: "the storm mizzen is a substitute for the spanker"). Gate 4a's
    ruling (2026-09-27): shifting a sail is the whole of taking in and
    replacing it, so a set sail is not refused."""

    # take_in: the take-in evolutions' steps run 45 s (a head sail's downhaul) to
    # 105 s (a course clewed up and hauled up); 90 s is the gaff sail's, taken as the
    # middle. set: the set evolutions' hoist or sheet-home-and-hoist steps, 75 s to
    # 150 s; 120 s. Both judgement from data/evolutions/take_in_*.yaml, set_*.yaml.
    DEFAULTS = {"take_in": 90.0, "unbend": 180.0, "send_up": 150.0, "bend": 240.0, "set": 120.0}

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        sail = self.sail
        if sail.state is SailState.UNBENT:
            return f"The {self._name()} is unbent; there is nothing to shift. Bend a new one."
        self.was_drawing = sail.state in DRAWING
        target = sail
        wanted = self.params.get("for")
        if wanted:
            target = _sail_named(self.ship, wanted)
            if target is None:
                return f"There is no sail called the {wanted} to shift the {self._name()} for."
            if not _in_each_others_place(sail, target):
                return (
                    f"The {self._name(target)} is not bent in the {self._name()}'s place; "
                    f"shift the {self._name()} for another of its kind."
                )
            if target.state is not SailState.UNBENT:
                return f"The {self._name(target)} is bent already."
            rival = self._rival(target, but=sail)
            if rival is not None:
                return (
                    f"The {self._name(rival)} is bent in the {self._name(target)}'s place; "
                    f"unbend it first."
                )
        self.target = target
        return self._choose(target)

    def begin(self, words: dict[str, Any]) -> None:
        drawing = getattr(self, "was_drawing", False)
        phases = ["unbend", "send_up", "bend"]
        if drawing:
            phases = ["take_in", *phases, "set"]
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        if name == "take_in":
            # the sail hauled up in its gear or hauled down its stay, the hands standing
            # by to unbend it; the same state the take-in evolutions leave
            self.old_state = self.sail.state
            self.sail.state = SailState.IN_THE_GEAR
            verb = "Hauled down" if self.sail.cls == "jibheaded" else "Clewed up"
            self.note(f"{verb} the {self._name()} to shift it.")
        elif name == "unbend":
            if getattr(self, "old_state", None) is None:
                self.old_state = self.sail.state
            self.sail.state = SailState.UNBENT
            self.sail.reefs = 0
            self.note(f"Unbent the {self._name()} and lowered it down on deck.")
        elif name == "set":
            # the new sail let fall and set in the old one's place (Luce: "Let fall!
            # Sheet home!"); its sheet and yard stand as the old sail's did
            self.target.state = SailState.SET
            self.ship.note(
                "notable",
                "sail.set",
                f"Set the {self._name(self.target)} in the {self._name()}'s place.",
                self.target.id,
            )
        elif name == "send_up":
            # draw the new sail first, so the old one going down is not sent straight back up
            if not self._draw():
                return
            if getattr(self, "old_state", None) is not SailState.BLOWN_OUT:
                # the old sail is sound: it goes down to the sail room for the sailmaker
                self._stow(self.sail)
            self.note(f"Swayed aloft the {self._name(self.target)} ({self._spare_words()}).")
        elif name == "bend":
            self._bend_spare()


# ---------------------------------------------------------------------------
# Wrecks: clearing away a spar carried away, and shifting it for a spare (package 30b)
# ---------------------------------------------------------------------------
#
# A spar that carries away takes with it everything that stands on it, hangs from it or is
# of it (`physics/strain.py`, `_wreck_spar`: all of it marked `wrecked`, hanging to leeward
# and dragging). Clearing the wreck (`clear_wreck.yaml`) saves what can be saved and cuts
# adrift what cannot: a sail that is whole goes down to the sail room, the rags of one
# blown out go over the side, the spars' remains are sent down on deck, and a lower mast
# or the bowsprit, which goes over the side, is cut adrift with all it carries (Luce 1884,
# ch. XXXI Carrying Away Masts and Spars: "When a mast goes over the side, first, get clear
# of the wreck"). The spars stay `wrecked`, now `sent_down` as well: on deck or gone, they
# catch no wind and bear no load, and the part graph keeps the wreck's consequences (a boom
# gone means no studding sail on it) until `shift the <spar>` (`shift_spar.yaml`) puts a
# spare of its class in its place from the booms (`parts.booms`).

# The spars whose wreck goes over the side and is cut adrift rather than sent down: a lower
# mast or the bowsprit carries away at the deck or the knightheads, and the wreck lies in
# the water (Luce 1884, ch. XXXI, 'Bowsprit Carried Away or Sprung': "Should the wreck be in
# the water under the bows ... Clear away the wreck"; 'Lower Mast Carried Away or Sprung':
# "Clear away the wreck ... Cut the rigging clear"). Every other spar's wreck hangs aloft
# and is sent down ('Main Topmast Carried Away': "Send the wreck down ... Send the stump
# down next"; 'Topgallant Mast Carried Away': "send down the wreck as convenient").
OVER_THE_SIDE_CLASSES = frozenset({"mast", "bowsprit"})

# The work in a spar, sending its wreck down or a spare aloft, relative to a studding-sail
# boom's (judgement, from how much of Luce 1884 ch. XXXII each shift takes: 'To Shift a
# Topmast Studding-sail Boom' a whip and a guy; 'To Shift a Topgallant Mast' the mast-rope
# and the light yards; 'To Shift a Topsail Yard' the yard purchase, burtons and every piece
# of its gear; 'To Shift a Topmast' the top pendants, the topgallant mast and the topsail
# yard out of the way). A class not listed counts as a yard.
SPAR_WORK: dict[str, float] = {
    "studdingsail_boom": 1.0,
    "flying_jib_boom": 1.5,
    "royal_mast": 1.5,
    "yard": 2.0,
    "lug_yard": 2.0,
    "lateen_yard": 2.0,
    "gaff": 2.0,
    "boom": 2.0,
    "sprit": 2.0,
    "jib_boom": 2.5,
    "topgallant_mast": 2.5,
    "topmast": 6.0,
    "bowsprit": 8.0,
    "mast": 10.0,
}


def spar_work(spar: Spar) -> float:
    return SPAR_WORK.get(spar.cls, SPAR_WORK["yard"])


def sail_spars(ship: Ship, sail: Sail) -> list[Spar]:
    """Every spar a sail needs standing: the chain of its principal spar, and each spar it
    names in a role (a studding sail's boom beside its yard, a gaff sail's boom) or whose
    stay it is hanked to, with the chains of those."""
    out = list(ship.spar_chain(sail))
    for target in sail.roles.values():
        if target in ship.spars:
            chain = ship.spar_chain(target)
        elif target in ship.lines:
            chain = ship.spar_chain(ship.lines[target])
        else:
            continue
        out.extend(sp for sp in chain if sp not in out)
    return out


def gone_spar(ship: Ship, sail: Sail) -> Spar | None:
    """The first spar the sail needs that is carried away, or None."""
    return next((sp for sp in sail_spars(ship, sail) if sp.wrecked), None)


def wreck_root(ship: Ship, part: Any) -> Spar | None:
    """The spar that carried away and took this part with it: for a spar carried away, the
    lowest spar of its chain carried away with it; for a sail, that of the first spar it
    needs that is carried away. None when nothing the part needs is carried away."""
    if isinstance(part, Sail):
        part = gone_spar(ship, part)
    if not isinstance(part, Spar) or not part.wrecked:
        return None
    root = part
    parent = ship.parent_of(root)
    while parent is not None and parent.wrecked:
        root, parent = parent, ship.parent_of(parent)
    return root


def wrecks(ship: Ship) -> list[Any]:
    """Every wreck still to be cleared, in the ship file's order: each spar carried away
    whose wreck still hangs (not yet sent down or cut adrift) and that stands on nothing
    carried away, and each sail blown out on spars that stand (its rags)."""
    out: list[Any] = [
        sp
        for sp in ship.spars.values()
        if sp.wrecked and not sp.sent_down and wreck_root(ship, sp) is sp
    ]
    out += [
        s
        for s in ship.sails.values()
        if s.state is SailState.BLOWN_OUT and not s.wrecked and gone_spar(ship, s) is None
    ]
    return out


def regear(ship: Ship) -> list:
    """Reeve afresh the gear of the parts that stand again (a spare shifted in a spar's
    place): every line the wreck took whose part stands whole now is no longer wrecked.
    The gear of a sail waits for every spar the sail needs."""
    back = []
    for ln in ship.lines.values():
        if not ln.wrecked:
            continue
        target = ship.parts.get(ln.of)
        if isinstance(target, Sail):
            standing = not target.wrecked and gone_spar(ship, target) is None
        elif isinstance(target, Spar):
            standing = not any(sp.wrecked for sp in ship.spar_chain(target))
        else:
            standing = False
        if standing:
            ln.wrecked = False
            ln.load_kn = 0.0
            back.append(ln)
    return back


def _subject_part(ship: Ship, params: dict[str, Any], words: dict[str, Any] | None):
    """The part a wreck script works on: `params["part"]` (the verbs pass it), or the
    subject the runner names in its words."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    pid = params.get("part")
    if isinstance(pid, str) and pid in ship.parts:
        return ship.parts[pid]
    name = (words or {}).get("subject")
    for p in list(ship.spars.values()) + list(ship.sails.values()):
        if part_name(ship, p.id) == name:
            params["part"] = p.id
            return p
    return None


def _joined(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


class ClearWreckScript(PhasedScript):
    """Clear away the wreck of a spar carried away, or the rags of a sail blown out
    (Luce 1884, ch. XXXI Carrying Away Masts and Spars: "No explicit rule can be given for
    sending down broken spars. The first thing to be attended to is their being steadied
    and prevented from falling on deck or tearing the sails"; Falconer 1780, *Veering*:
    "the mizen-mast must instantly be cut away"). The part named may be the spar carried
    away, any spar or sail that went with it (the whole wreck is cleared), or a blown-out
    sail on standing spars.

    Phases, each left out when it has nothing to do:
      secure      aloft: the wreck steadied with burtons and tripping-lines
      sails       aloft: robands and earings cut, each sail that is whole lowered on deck
                  for the sail room, the rags of one blown out cut adrift over the side
                  ('Topgallant Yard Carried Away': "Cut adrift the clewlines from the
                  clews, cut robands and head earings, and lower")
      send_down   on deck: the spars' remains sent down ('Main Topmast Carried Away':
                  "Send the wreck down ... Send the stump down next")
      cut_adrift  on deck: the lanyards and lashings cut and the wreck of a lower mast or
                  the bowsprit let go over the side with everything on it ('Lower Mast
                  Carried Away': "Cut the rigging clear")
    `params["send_down"]` (the order `send down <the spar>`) refuses a wreck that must be
    cut adrift. The sails phase takes its time for the first sail and half as much again for
    each other (the hands at several at once), the others by the work in the spars
    (`SPAR_WORK`); all judgement."""

    DEFAULTS = {"secure": 60.0, "sails": 120.0, "send_down": 90.0, "cut_adrift": 60.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.part = _subject_part(ship, params, None)
        self.root: Spar | None = None
        self.rags: Sail | None = None  # a blown-out sail on standing spars: its rags alone
        self.spars: list[Spar] = []
        self.sails: list[Sail] = []  # aloft in the wreck
        self.stowed: list[Sail] = []  # in the sail room, wrecked with the spars they need
        self.saved: list[Sail] = []
        self.lost: list[Sail] = []
        self.over_side = False
        if self.part is not None:
            self._survey()

    def _name(self, part: Any) -> str:
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        return part_name(self.ship, part.id)

    def _survey(self) -> None:
        ship, part = self.ship, self.part
        self.root = wreck_root(ship, part)
        self.rags = None
        if self.root is None:
            if isinstance(part, Sail) and part.state is SailState.BLOWN_OUT:
                self.rags = part
                self.sails = [part]
            return
        deps = ship.dependents(self.root)
        self.spars = [self.root] + [d for d in deps if isinstance(d, Spar)]
        wrecked = [d for d in deps if isinstance(d, Sail) and d.wrecked]
        self.sails = [s for s in wrecked if s.state is not SailState.UNBENT]
        self.stowed = [s for s in wrecked if s.state is SailState.UNBENT]
        self.over_side = self.root.cls in OVER_THE_SIDE_CLASSES

    def holds(self) -> set[str]:
        return {p.id for p in self.spars + self.sails}

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        if self.part is None:
            self.part = _subject_part(ship, self.params, words)
        part = self.part
        if part is None:
            return "Name the spar or the sail whose wreck is to be cleared."
        self._survey()
        name = self._name(part)
        if self.root is None and self.rags is None:
            if isinstance(part, Sail):
                if part.state is SailState.UNBENT:
                    return f"The {name} is unbent; there is nothing aloft to cut away."
                return (
                    f"The {name} is sound and {part.describe_state()}; there is no wreck to cut "
                    f"away. To send it down, unbend it."
                )
            if isinstance(part, Spar) and part.sent_down:
                return f"The {name} is sent down on deck, not carried away; there is no wreck."
            return f"The {name} stands sound; there is no wreck to cut away."
        if self.rags is not None:
            if self.params.get("send_down"):
                return f"The {name} is blown out; unbend it to send it down, or cut it away."
            return None
        root = self._name(self.root)
        if self.root.sent_down:
            return f"The wreck of the {root} is cleared already; shift the {root} for a spare."
        if self.over_side and self.params.get("send_down"):
            return (
                f"The {root} went over the side; its wreck cannot be sent down. Cut away the wreck."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self._survey()
        phases = ["secure"]
        if self.sails and not self.over_side:
            phases.append("sails")
        if self.spars:
            phases.append("cut_adrift" if self.over_side else "send_down")
        self.start_phases(phases)

    def phase_s(self, name: str) -> float:
        base = super().phase_s(name)
        if name == "sails":
            return base * (1.0 + 0.5 * max(0, len(self.sails) - 1))
        if name == "send_down":
            return base * max(1.0, sum(spar_work(s) for s in self.spars))
        return base

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "secure":
            if self.rags is not None:
                self.note(f"Hands aloft to cut the rags of the {self._name(self.rags)} adrift.")
            else:
                self.note(
                    f"Steadied the wreck of the {self._name(self.root)} with burtons and "
                    f"tripping-lines."
                )
        elif name == "sails":
            for s in self.sails:
                whole = s.state is not SailState.BLOWN_OUT
                s.state = SailState.UNBENT
                s.reefs = 0
                s.wrecked = False
                s.load_kn = 0.0
                if whole:
                    room = parts.sail_room(ship)
                    spare = parts.SpareSail(kind=s.id, canvas_no=s.canvas_no, condition=s.condition)
                    room.stow(spare)
                    ship.extra["spare_sails"] = len(room)
                    self.saved.append(s)
                else:
                    self.lost.append(s)
            for s in self.stowed:
                s.wrecked = False  # in the sail room all along
            said = []
            if self.saved:
                said.append(f"lowered {self._the(self.saved)} on deck for the sail room")
            if self.lost:
                said.append(f"cut the rags of {self._the(self.lost)} adrift over the side")
            self.note("Cut the robands and earings; " + "; ".join(said) + ".")
        elif name in ("send_down", "cut_adrift"):
            for sp in self.spars:
                sp.sent_down = True  # on deck, or gone: no wind on it, no load
                sp.brace_angle = 0.0
                sp.load_kn = 0.0
                if sp.cls in parts.RIGGED_IN_CLASSES:
                    sp.rigged_out = False
            if name == "cut_adrift":
                for s in self.sails:
                    s.state = SailState.UNBENT
                    s.reefs = 0
                    s.wrecked = False
                    s.load_kn = 0.0
                    self.lost.append(s)
                for s in self.stowed:
                    s.wrecked = False
                self.note(
                    f"Cut the lanyards and lashings; the wreck of the {self._name(self.root)} "
                    f"went over the side{self._with()}."
                )
            else:
                self.note(
                    f"Sent down on deck the remains of the {self._name(self.root)}"
                    f"{self._with()}; the gear that went with it unrove and cleared."
                )

    def _the(self, items: list) -> str:
        """'the fore royal and the fore royal yard', for the log."""
        return _joined([f"the {self._name(p)}" for p in items])

    def _with(self) -> str:
        return f", with {self._the(self.spars[1:])}" if len(self.spars) > 1 else ""

    def _account(self) -> str:
        """What was saved and what went over the side, for the log."""
        if self.rags is not None:
            return "its rags cut adrift and over the side"
        if self.over_side:
            gone = self.spars[1:] + self.lost
            return "cut adrift and over the side" + (f" with {self._the(gone)}" if gone else "")
        pieces = ["its remains sent down on deck" + self._with()]
        if self.saved:
            pieces.append(f"{self._the(self.saved)} saved to the sail room")
        if self.lost:
            pieces.append(f"the rags of {self._the(self.lost)} over the side")
        else:
            pieces.append("nothing went over the side")
        return "; ".join(pieces)

    def _spares(self) -> str:
        """What the booms hold for the spar carried away, for the log."""
        if self.root is None:
            return ""
        n = parts.booms(self.ship).have(self.root.cls)
        words = parts.spar_class_words(self.root.cls, n if n else 1)
        if n:
            return f" The booms hold {n} spare {words}."
        return f" There is no spare {words} aboard."

    def words(self) -> dict[str, Any]:
        part = self.root if self.root is not None else self.rags or self.part
        return {
            "wreck": self._name(part) if part is not None else "wreck",
            "account": self._account() if (self.root or self.rags) else "",
            "spares": self._spares(),
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["wreck"] = self.root.id if self.root is not None else None
        d["spars"] = [s.id for s in self.spars]
        d["saved"] = [s.id for s in self.saved]
        d["over_the_side"] = [s.id for s in self.lost] + (
            [s.id for s in self.spars] if self.over_side else []
        )
        return d


class ShiftSparScript(PhasedScript):
    """Shift a spar carried away for a spare of its class from the booms (Luce 1884, ch.
    XXXII Shifting Sails and Spars, 'To Shift a Topmast Studding-sail Boom', 'To Shift a
    Topgallant Mast', 'To Shift a Topsail Yard', 'To Shift a Topmast': "Send the stump
    down next, and proceed to send aloft a new topmast", ch. XXXI). The wreck must be
    cleared first, and the spar it stands on must stand. Phases:
      get_up  on deck: the spare got out of the booms and its gear put on it
      sway    aloft: swayed aloft and fidded, crossed, or landed in its irons
      rig     aloft: the gear rove and the rigging set up
    each taking its time by the work in the spar (`SPAR_WORK`). The spar stands again,
    whole; the gear the wreck took is rove afresh where its parts stand (`regear`); a sail
    that belongs on it is left in the sail room, to be bent by order."""

    DEFAULTS = {"get_up": 60.0, "sway": 120.0, "rig": 90.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.spar = _subject_part(ship, params, None)

    def _name(self, part: Any) -> str:
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        return part_name(self.ship, part.id)

    def holds(self) -> set[str]:
        if not isinstance(self.spar, Spar):
            return set()
        return {self.spar.id} | {s.id for s in self.ship.sails_using(self.spar)}

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        if self.spar is None:
            self.spar = _subject_part(ship, self.params, words)
        spar = self.spar
        if not isinstance(spar, Spar):
            return "Name the spar to shift for a spare."
        name = self._name(spar)
        if not spar.wrecked:
            if spar.sent_down:
                return (
                    f"The {name} is sent down on deck, not carried away; there is nothing to shift."
                )
            return f"The {name} is sound; only a spar carried away is shifted for a spare."
        root = wreck_root(ship, spar) or spar
        if not root.sent_down:
            return f"The wreck of the {self._name(root)} still hangs aloft; cut it away first."
        if root is not spar:
            first = self._name(root)
            return f"The {name} went with the {first}; shift the {first} first."
        parent = ship.parent_of(spar)
        if parent is not None and parent.sent_down:
            return f"The {self._name(parent)} is sent down; sway it up before shifting the {name}."
        if parts.booms(ship).have(spar.cls) == 0:
            return (
                f"No spare {parts.spar_class_words(spar.cls)} aboard; the dockyard must supply one."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["get_up", "sway", "rig"])

    def phase_s(self, name: str) -> float:
        base = super().phase_s(name)
        return base * spar_work(self.spar) if isinstance(self.spar, Spar) else base

    def end_phase(self, name: str) -> None:
        ship, spar = self.ship, self.spar
        name_ = self._name(spar)
        what = parts.spar_class_words(spar.cls)
        if name == "get_up":
            store = parts.booms(ship)
            if store.have(spar.cls) == 0:  # taken by another shift meanwhile
                self.fail(f"No spare {what} aboard; the dockyard must supply one")
                return
            store.take(spar.cls)
            ship.extra["spare_spars"] = len(store)
            self.note(f"Got the spare {what} out of the booms and put its gear on it.")
        elif name == "sway":
            spar.wrecked = False
            spar.sent_down = False
            spar.condition = 100.0
            spar.load_kn = 0.0
            spar.brace_angle = 0.0
            if spar.cls in parts.RIGGED_IN_CLASSES:
                spar.rigged_out = False  # landed in its irons, rigged in, ready to rig out
            if spar.cls in MAST_CLASSES:
                done = f"Swayed aloft and fidded the new {name_}"
            elif spar.cls in YARD_LIKE_CLASSES:
                done = f"Swayed aloft and crossed the new {name_}"
            elif spar.cls in parts.RIGGED_IN_CLASSES:
                done = f"Landed the new {name_} in its irons and clamped it"
            elif spar.cls in ("jib_boom", "flying_jib_boom"):
                done = f"Rigged out and pointed the new {name_}"
            else:
                done = f"Swayed up and shipped the new {name_}"
            self.note(f"{done}.")
        elif name == "rig":
            regear(ship)
            self.note(f"Rove the {name_}'s gear and set up the rigging.")

    def words(self) -> dict[str, Any]:
        ship, spar = self.ship, self.spar
        if not isinstance(spar, Spar):
            return {}
        n = parts.booms(ship).have(spar.cls)
        left = (
            f"{n} spare {parts.spar_class_words(spar.cls, n)} left on the booms"
            if n
            else f"no spare {parts.spar_class_words(spar.cls)} left aboard"
        )
        after = []
        unbent = [
            s
            for s in ship.sails_using(spar)
            if s.state is SailState.UNBENT and gone_spar(ship, s) is None
        ]
        if unbent:
            names = _joined([f"the {self._name(s)}" for s in unbent])
            after.append(f"{names} may be bent to it again")
        wanting = [d for d in ship.dependents(spar) if isinstance(d, Spar) and d.wrecked]
        if wanting:
            names = _joined([f"the {self._name(d)}" for d in wanting])
            verb = "is" if len(wanting) == 1 else "are"
            after.append(f"{names}, carried away with it, {verb} still to be shifted")
        return {"left": left, "after": "; " + "; ".join(after) if after else ""}

    def data(self) -> dict[str, Any]:
        d = super().data()
        if isinstance(self.spar, Spar):
            d["spar"] = self.spar.id
            d["spare_spars"] = len(parts.booms(self.ship))
        return d


# ---------------------------------------------------------------------------
# Routine sail work for the whole ship: loosing to dry, furling everything
# ---------------------------------------------------------------------------


class LooseToDryScript(PhasedScript):
    """Loose sails to dry (Luce 1884, ch. XX 'To loose sail to the buntlines'
    (port routine): "Loose sail! ... Let fall! ... Topgallant-sails and royals
    hang down, their clews hauled up snug. The head sails are spread on the
    booms, heads of fore and aft sails hauled about half-way out"). Every
    furled sail on a standing spar, except the studding sails, which are
    stowed below, is loosed to hang in its gear. One phase, ``loose``
    (aloft). Refused when it blows more than ``max_wind_kn`` across the deck."""

    DEFAULTS = {"loose": 180.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sails = self._furled()

    def _furled(self) -> list:
        return [
            s
            for s in self.ship.sails.values()
            if s.state is SailState.FURLED
            and s.cls != "studding"
            and not s.wrecked
            and _chain_standing(self.ship, s)
        ]

    def holds(self) -> set[str]:
        return {self.ship.name} | {s.id for s in self.sails}

    def check(self, words: dict[str, Any]) -> str | None:
        limit = self.timing_value("max_wind_kn", 20.0)
        across = units.ms_to_knots(self.ship.dyn.apparent_wind_speed)
        if across > limit:
            return (
                f"It blows too hard to loose sails to dry: {across:.0f} knots across the deck; "
                f"wait for it to fall below {limit:.0f}."
            )
        self.sails = self._furled()
        if not self.sails:
            return "There is no furled sail to loose; they are all set, in the gear or below."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sails = self._furled()
        self.start_phases(["loose"])

    def end_phase(self, name: str) -> None:
        for s in self.sails:
            if s.state is SailState.FURLED:
                s.state = SailState.LOOSED
        self.note("Let fall; the sails hang in their gear to dry.")

    def words(self) -> dict[str, Any]:
        return {"count": len(self.sails)}


class FurlAllScript(PhasedScript):
    """Furl every sail (Luce 1884, ch. XX 'To furl sail': "Furl sail! ... Lay
    out! ... Furl away! ... Lay in! Down booms! Lay down from aloft!"). What is
    drawing is clewed up, hauled down or brailed first (phase ``clew_up``, on
    deck), then everything that hangs loose is furled or stowed (phase
    ``furl``, aloft). Studding sails are made up and sent below."""

    DEFAULTS = {"clew_up": 90.0, "furl": 240.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sails = self._loose()

    def _loose(self) -> list:
        return [
            s
            for s in self.ship.sails.values()
            if (s.state in DRAWING or s.state in HANGING)
            and not s.wrecked
            and _chain_standing(self.ship, s)
        ]

    def holds(self) -> set[str]:
        return {self.ship.name} | {s.id for s in self.sails}

    def check(self, words: dict[str, Any]) -> str | None:
        self.sails = self._loose()
        if not self.sails:
            return "Every sail is furled already."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sails = self._loose()
        drawing = [s for s in self.sails if s.state in DRAWING]
        self.start_phases((["clew_up"] if drawing else []) + ["furl"])

    def end_phase(self, name: str) -> None:
        if name == "clew_up":
            drawing = [s for s in self.sails if s.state in DRAWING]
            for s in drawing:
                s.state = SailState.IN_THE_GEAR
            self.note(f"Clewed up, hauled down and brailed up {_names(self.ship, drawing)}.")
        elif name == "furl":
            for s in self.sails:
                if s.state in DRAWING or s.state in HANGING:
                    s.state = SailState.FURLED

    def words(self) -> dict[str, Any]:
        return {"count": len(self.sails)}


# ---------------------------------------------------------------------------
# Ship handling: box-hauling, lying a-try, scudding, backing and filling
# ---------------------------------------------------------------------------


def _after_courses(ship: Ship) -> list:
    """The courses abaft the foremost mast that carries yards: the mainsail of a
    ship (Luce: "Up mainsail and spanker!")."""
    head, _after = head_and_after_yards(ship)
    head_ids = {y.id for y in head}
    return [
        sl
        for sl in lowest_square_sails(ship)
        if sl.is_set and ship.yard_of(sl) is not None and ship.yard_of(sl).id not in head_ids
    ]


def _after_sail(ship: Ship) -> list:
    """What is hauled up to box-haul: the courses abaft the head yards and the
    gaff sails set on the aftermost mast (Luce: "Up mainsail and spanker!"; on a
    schooner, whose after sail is her main gaff sail, that is lowered)."""
    masts = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    drivers: list = []
    if masts:
        aftermost = min(masts, key=lambda m: m.x_m)
        drivers = [
            sl
            for sl in ship.sails.values()
            if sl.cls == "gaff" and sl.is_set and ship.mast_of(sl) is aftermost
        ]
    return _after_courses(ship) + drivers


class BoxHaulScript(Script):
    """Box-haul her: wear short round by bracing the head yards abox (Luce 1884,
    ch. XXIV 'Box-hauling'; Luce 1866 ch. XXIV 'Box Hauling').

    ``luff``: "Put the helm down! ... Up mainsail and spanker!" The helm is put
    a-lee and the mainsail and spanker hauled up; she flies up toward the wind
    and loses her way. (``luff_first`` 0 skips this for wearing short round:
    the helm is put hard up at once.)
    ``box``: "Square away the after yards! Brace abox the head yards!" The
    after yards are squared and the head yards laid aback over ``brace_s``;
    the helm is left a-lee, which is right for the sternboard.
    ``fall_off``: she gathers sternway and her head falls off; "as the after
    sails lift, brace them in to keep them lifting", and the head yards are
    squared once the wind is abaft the beam. "As soon as the sails on the
    foremast give her headway, shift the helm."
    ``come_to``: with the wind across the stern, the mainsail and spanker are
    set again and she comes to on the new tack, the after yards sharp up and
    the head yards braced up as she comes, as at the end of a wear.

    She has box-hauled when steady on the new close-hauled course; she fails
    if it takes longer than ``box_timeout_s``."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.way_before = ship.dyn.speed  # by the wind, before the helm (for the sheets)
        self.hauled_up: list = []
        self.swing: YardSwing | None = None
        self.new_course = ship.dyn.heading
        self.sternway = False
        self.helm_shifted = False

    def holds(self) -> set[str]:
        held = {self.ship.name} | {y.id for y in self.head + self.after}
        held |= {s.id for s in _after_sail(self.ship)}
        return held

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.head:
            return "She has no head yards to brace abox."
        if "hove_to" in self.ship.extra:
            return "She is hove to; fill away first, or wear."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        helm = units.deg_to_rad(self.timing_value("helm_deg", 25.0))
        dyn.helm_mode = HelmMode.RUDDER
        dyn.steady = False
        if self.timing_value("luff_first", 1.0) > 0:
            dyn.target_rudder = self.sign * helm
            self.phase = "luff"
            self.note("Ready about. Helm's a-lee; checked the lee head braces.", "helm.order")
        else:
            dyn.target_rudder = -self.sign * helm
            self._box()

    def _box(self) -> None:
        """Up mainsail and spanker (as the sails lift, in box-hauling; at once, in
        wearing short round), square the after yards and brace the head yards abox."""
        self.phase = "box"
        self.hauled_up = _after_sail(self.ship)
        for sl in self.hauled_up:
            sl.state = SailState.IN_THE_GEAR
        up = ""
        if self.hauled_up:
            from freesail.evolutions.runner import part_name  # local import to avoid a cycle

            up = "Up " + " and ".join(part_name(self.ship, sl.id) for sl in self.hauled_up) + "! "
        targets = [-self.sign * y.brace_limit for y in self.head] + [0.0 for _ in self.after]
        self.swing = YardSwing(self.head + self.after, targets, self.timing_value("brace_s", 45.0))
        if self.after:
            text = "Square away the after yards! Brace abox the head yards!"
        else:
            text = "Brace abox the head yards!"
        self.note(up + text)

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        helm = units.deg_to_rad(self.timing_value("helm_deg", 25.0))
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 1.0)) * dt / factor
        if self.t > self.timing_value("box_timeout_s", 900.0):
            self._restore()
            self.fail("she would not come round")
            return
        if self.phase == "luff":
            stopped = dyn.u <= units.knots_to_ms(self.timing_value("stop_kn", 1.0))
            head_to_wind = abs(rel) <= POINT or self.sign * rel < 0
            if stopped or head_to_wind or self.t >= self.timing_value("luff_timeout_s", 120.0):
                self._box()
        if self.phase in ("box", "fall_off"):
            # sternway throws her head off with the helm a-lee; headway needs it up
            dyn.target_rudder = self.sign * helm if dyn.u < 0.0 else -self.sign * helm
            if dyn.u < 0.0:
                self.sternway = True
            elif self.sternway and not self.helm_shifted:
                self.helm_shifted = True
                self.note("She gathers headway. Shift the helm!", "helm.order")
        if self.phase == "box":
            assert self.swing is not None
            if self.swing.advance(dt, factor):
                self.phase = "fall_off"
                self.note("Her head falls off.")
        elif self.phase == "fall_off":
            follow_wind(self.after, rel, ch, max_step)
            if abs(rel) > math.pi / 2:
                follow_wind(self.head, rel, ch, max_step)
            crossed = self.sign * rel < 0 and abs(rel) > math.pi / 2
            if crossed or abs(rel) >= units.deg_to_rad(165.0):
                self.phase = "come_to"
                words = self._restore()
                # the sheets shifted over to the new tack's lee side, the old weather side
                # (package 32e), the mainsail and spanker set again among them
                shift_sheets_over(
                    self.ship, "starboard" if self.sign > 0 else "larboard", wind, self.way_before
                )
                self.note(f"Wind aft; braced up the after yards; shifted over the sheets.{words}")
        if self.phase == "come_to":
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.helm_mode = HelmMode.HEADING
            dyn.target_heading = self.new_course
            dyn.steady = False
            sharp_up = -self.sign
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
            after_done = move_toward(
                self.after, [sharp_up * y.brace_limit for y in self.after], max_step
            )
            if steady:
                head_done = move_toward(
                    self.head, [sharp_up * y.brace_limit for y in self.head], max_step
                )
            else:
                follow_wind(self.head, rel, ch, max_step)
                head_done = False
            if steady and after_done and head_done:
                self.finish()

    def _restore(self) -> str:
        """Set again the mainsail and spanker that were hauled up for the evolution;
        the words for the log ("Main tack and sheet! Haul out the spanker!")."""
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        words = []
        for sl in self.hauled_up:
            if sl.state is SailState.IN_THE_GEAR and _chain_standing(self.ship, sl):
                sl.state = SailState.SET
                name = part_name(self.ship, sl.id)
                if sl.cls == "square":
                    tack = name.replace("sail", "").replace("course", "").strip()
                    words.append(f"Board the {tack} tack and haul aft the sheet!")
                else:
                    words.append(f"Haul out the {name}!")
        self.hauled_up = []
        return (" " + " ".join(words)) if words else ""

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("box_estimate_s", 360.0) - self.t)

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }


def _topsails_on(ship: Ship, yards: list[Spar]) -> list:
    """The topsails among a mast's yards: square sails on yards that hang on a topmast."""
    out = []
    for y in yards:
        sl = ship.sail_of(y)
        parent = ship.parent_of(y)
        if sl is not None and sl.cls == "square" and parent is not None and parent.cls == "topmast":
            out.append(sl)
    return out


class LieATryScript(Script):
    """Lie a-try (lie to in a gale) under the close-reefed topsail of the mast
    that carries the most square sail and the staysails (Luce 1884, ch. XXIX
    'In a Gale': "The ship is now 'lying to' under close-reefed main topsail,
    fore storm staysail, and probably single reefed trysail").

    Phase ``hand_sails`` (``hand_s``): every other square sail is clewed up
    or hauled up, the studding sails taken in, the jibs hauled down (the ship
    file's ``jibs`` group) and the driver brailed up (``after_gaff_sails``: the
    spanker of a ship, which is far bigger than Luce's trysail and brings her
    head to the wind with sternway, as package 10 found for heaving to; a
    schooner keeps her gaff sails). The staysails stand. Phase ``brace``: the
    topsail yards braced sharp up for the tack she is on and the helm put a
    little a-lee (``helm_deg``); she comes up to about five points off and
    lies there, drifting to leeward. How much reef is in the topsail is the
    captain's order before this one. She is left lying to as ``heave_to``
    leaves her (``ship.extra["hove_to"]``, the topsail yards already full),
    so ``fill away`` ends it."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.topsails = _topsails_on(ship, self.yards)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.handed: list = []
        self.swing: YardSwing | None = None
        self.progress = 0.0

    def _to_hand(self) -> list:
        ship = self.ship
        keep = {s.id for s in self.topsails}
        jibs = set(ship.groups.get("jibs", []))
        out = []
        for sl in ship.sails.values():
            if sl.id in keep or not (sl.state in DRAWING or sl.state is SailState.LOOSED):
                continue
            if sl.cls in ("square", "studding") or sl.id in jibs:
                out.append(sl)
        drivers = {sl.id for sl in after_gaff_sails(ship)}
        out += [sl for sl in ship.sails.values() if sl.id in drivers and sl not in out]
        return out

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards} | {s.id for s in self._to_hand()}

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.topsails:
            return "She has no topsail to lie a-try under."
        if "hove_to" in self.ship.extra:
            return "She is lying to already."
        if not any(s.is_set for s in self.topsails):
            return (
                f"The {names_of_sails(self.ship, self.topsails)[4:]} is not set; set it, "
                f"close-reefed, to lie a-try under it."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sign = 1.0 if self.ship.dyn.tack == "starboard" else -1.0
        self.handed = self._to_hand()
        if self.handed:
            self.phase = "hand_sails"
            self.note(f"Hands to shorten sail: {_names(self.ship, self.handed)}.")
        else:
            self._brace()

    def _brace(self) -> None:
        self.phase = "brace"
        self.swing = YardSwing(
            self.yards,
            [self.sign * y.brace_limit for y in self.yards],
            self.timing_value("brace_s", 45.0),
        )
        dyn = self.ship.dyn
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 5.0))
        dyn.steady = False
        # the staysails' sheets hauled aft (package 32e: the sheet holds the trim, and a
        # staysail left at a reaching trim lets her come up inside five points)
        sheets_to(self.ship, head_sails(self.ship), None, None)
        self.note(
            f"Braced the {sail_name_on(self.ship, self.yards)} sharp up; hauled aft the head "
            "sheets; helm a-lee.",
            "helm.order",
        )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        if self.phase == "hand_sails":
            self.progress = min(
                1.0, self.progress + dt / (self.timing_value("hand_s", 120.0) * factor)
            )
            if self.progress >= 1.0 - 1e-9:
                for sl in self.handed:
                    if sl.state in DRAWING or sl.state is SailState.LOOSED:
                        sl.state = (
                            SailState.FURLED if sl.cls == "studding" else SailState.IN_THE_GEAR
                        )
                self.note(f"Took in {_names(self.ship, self.handed)}.")
                self._brace()
            return
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            # the topsail yard is already full: fill away braces it where it is
            yards = [y.id for y in self.yards]
            self.ship.extra["hove_to"] = {"yards": yards, "sign": self.sign, "how": "a-try"}
            self.finish()

    def remaining_s(self) -> float:
        brace = self.timing_value("brace_s", 45.0)
        if self.phase == "hand_sails":
            return (1.0 - self.progress) * self.timing_value("hand_s", 120.0) + brace
        return self.swing.remaining_s() if self.swing else brace

    def words(self) -> dict[str, Any]:
        return {"topsail": names_of_sails(self.ship, self.topsails)[4:]}


class ScudScript(Script):
    """Scud before a gale (Luce 1884, ch. XXIX 'To scud': "a vessel may scud
    before it, under such sail as the force of the wind will allow ... The best
    sails for scudding are a close-reefed main topsail and single or
    double-reefed foresail ... The fore topmast staysail should always be
    set"). The helm is put up and she is steered with the wind ``quarter_deg``
    on the weather quarter (not dead aft, where she would be brought by the
    lee); the driver is brailed up so that she will bear up; every yard is
    braced in to the wind as she goes off (``brace_rate_deg_s``). She is
    scudding when steady on that course with the yards trimmed, or after
    ``scud_timeout_s``. What sail she carries is the captain's order before
    this one; the helmsman keeps the course afterwards."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.course = ship.dyn.heading
        self.drivers: list = []

    def holds(self) -> set[str]:
        return (
            {self.ship.name}
            | {y.id for y in working_yards(self.ship)}
            | {s.id for s in after_gaff_sails(self.ship)}
        )

    def check(self, words: dict[str, Any]) -> str | None:
        if "hove_to" in self.ship.extra:
            return "She is lying to; fill away first, then bear up to scud."
        return None

    def _course_for(self, wind_from: float) -> float:
        q = units.deg_to_rad(self.timing_value("quarter_deg", 15.0))
        return units.wrap_2pi(wind_from - self.sign * (math.pi - q))

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.course = self._course_for(estimated_wind_from(self.ship))
        self.drivers = after_gaff_sails(self.ship)
        for sl in self.drivers:
            sl.state = SailState.IN_THE_GEAR
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = self.course
        dyn.steady = False
        self.phase = "bear_up"
        brailed = f"; brailed up {names_of_sails(self.ship, self.drivers)}" if self.drivers else ""
        self.note(f"Up helm{brailed}; brace in the yards as she goes off.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 0.5)) * dt / factor
        self.course = self._course_for(wind.direction_from)
        dyn.target_heading = self.course
        yards = working_yards(self.ship)
        settled = follow_wind(yards, rel, ch, max_step)
        error = abs(units.wrap_pi(dyn.heading - self.course))
        steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
        if (steady and settled) or self.t >= self.timing_value("scud_timeout_s", 600.0):
            self.finish()

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("scud_estimate_s", 180.0) - self.t)

    def words(self) -> dict[str, Any]:
        side = "starboard" if self.sign > 0 else "larboard"
        return {"course": units.format_heading(self.course), "quarter": side}


class BackAndFillScript(Script):
    """Back and fill (Luce 1884, Appendix I 'In a Tideway', 'Backing and
    Filling': "by backing, filling, or shivering the main yard, either to keep
    in the best of the tide, or to make way for other vessels"; Luce 1866 ch.
    XXII). The yards of the mast that carries the most square sail are laid
    aback and she drops astern, then braced full and she forereaches, ``cycles``
    times, each board held for ``hold_s`` after a brace of ``brace_s``. As in
    heaving to, the courses are hauled up, the driver brailed up and the light
    sails forward clewed up first; the helm is a-lee (``helm_deg``) while she
    is aback and amidships while she forereaches. She ends with the yards
    aback, lying to as ``heave_to`` leaves her, so ``fill away`` stands her on.
    There are no tides yet (milestone 5), so what she keeps is her place, not a
    channel."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.boards: list[str] = []
        self.board = -1
        self.swing: YardSwing | None = None
        self.hold = 0.0

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards}

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.yards:
            return "She has no square yards to back and fill."
        if not any(s.is_set for y in self.yards for s in [self.ship.sail_of(y)] if s):
            return f"No sail is set on the {sail_name_on(self.ship, self.yards)} to back and fill."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        info = self.ship.extra.get("hove_to")
        if info:
            self.sign = float(info.get("sign", self.sign))
        else:
            self.sign = 1.0 if self.ship.dyn.tack == "starboard" else -1.0
        cycles = max(1, int(round(self.timing_value("cycles", 2.0))))
        boards = ["back", "fill"] * cycles + ["back"]
        if info and info.get("yards"):
            boards = boards[1:]  # already aback: begin by filling
        self.boards = boards
        dyn = self.ship.dyn
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = 0.0
        dyn.steady = False
        self.ship.extra.pop("hove_to", None)
        # as for heaving to: the courses hauled up, the driver brailed up and the
        # light sails forward clewed up, or she flies up into the wind when backed
        handed = [sl for sl in lowest_square_sails(self.ship) if sl.is_set]
        handed += after_gaff_sails(self.ship) + light_sails_forward_of(self.ship, self.yards)
        for sl in handed:
            sl.state = SailState.IN_THE_GEAR
        if handed:
            self.note(f"Hauled up {_names(self.ship, handed)}.")
        self._next_board()

    def _next_board(self) -> None:
        self.board += 1
        if self.board >= len(self.boards):
            self.ship.extra["hove_to"] = {"yards": [y.id for y in self.yards], "sign": self.sign}
            self.finish()
            return
        self.phase = self.boards[self.board]
        aback = self.phase == "back"
        target = [(-self.sign if aback else self.sign) * y.brace_limit for y in self.yards]
        self.swing = YardSwing(self.yards, target, self.timing_value("brace_s", 45.0))
        self.hold = 0.0
        # the helm a-lee while she drops astern keeps her head from falling off
        # (sternway reverses the rudder); amidships while she forereaches
        helm = units.deg_to_rad(self.timing_value("helm_deg", 15.0))
        self.ship.dyn.target_rudder = self.sign * helm if aback else 0.0
        what = sail_name_on(self.ship, self.yards)
        if aback:
            self.note(f"Backed the {what}; her way checked.")
        else:
            self.note(f"Filled the {what}; she forereaches.")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        assert self.swing is not None
        if not self.swing.advance(dt, factor):
            return
        self.hold += dt
        last = self.board == len(self.boards) - 1
        if last or self.hold >= self.timing_value("hold_s", 90.0):
            self._next_board()

    def remaining_s(self) -> float:
        left = len(self.boards) - self.board - 1
        each = self.timing_value("brace_s", 45.0) + self.timing_value("hold_s", 90.0)
        now = self.swing.remaining_s() if self.swing else 0.0
        return now + max(0, left) * each

    def words(self) -> dict[str, Any]:
        return {"backed": sail_name_on(self.ship, self.yards)}


# ---------------------------------------------------------------------------
# A parted line rove afresh, or spliced (package 31b; playtest 11's finding 7)
# ---------------------------------------------------------------------------

# Fathoms of rope a new line of each class takes from the coil, for a frigate's rig:
# judgement from each line's lead (a topsail sheet from the clew through the yardarm
# sheave and the quarter block to the deck, both parts of a double sheet; a halyard's tye
# and fall; a brace's pendant and its fall led aft to the deck; a course's tack short and
# doubled, "twice the length of the single tacks", Steel 1794, vol. I, the note to the
# tables). Steel's tables of the lengths of running rigging by rate are at the end of his
# second volume and their figures did not survive the OCR, so these are not read from
# them (docs/dev/TuningNotes.md, M5a, package 31b). Scaled by the ship's length on the
# waterline against the frigate's (`REEVE_REFERENCE_LENGTH_M`), so the schooner's lines
# take about three fifths.
LINE_FATHOMS: dict[str, float] = {
    "sheet": 30.0,
    "tack": 15.0,
    "halyard": 40.0,
    "throat_halyard": 30.0,
    "peak_halyard": 40.0,
    "brace": 35.0,
    "lift": 20.0,
    "clewline": 30.0,
    "buntline": 30.0,
    "bowline": 25.0,
    "downhaul": 25.0,
    "reef_tackle": 20.0,
    "vang": 15.0,
    "outhaul": 15.0,
}
DEFAULT_LINE_FATHOMS = 25.0
REEVE_REFERENCE_LENGTH_M = 41.8  # the frigate's length on the waterline (her ship file)
# A spliced rope is "weaker than the main part of the rope by about one-eighth" (Luce
# 1884, ch. II Knotting and Splicing, 'Splicing'): a spliced line's rating, of its own.
SPLICED_STRENGTH = 7.0 / 8.0
# The lines whose hauled part is slack when new-rove: the next set hauls them home.
_ROVE_SLACK_CLASSES = frozenset(
    {"sheet", "tack", "halyard", "throat_halyard", "peak_halyard", "clewline", "buntline"}
    | {"downhaul", "reef_tackle", "outhaul", "bowline", "vang"}
)


def line_fathoms(ship: Ship, line: Any) -> float:
    """The fathoms a new line of this class takes from the coil, for this ship's size."""
    base = LINE_FATHOMS.get(getattr(line, "cls", ""), DEFAULT_LINE_FATHOMS)
    hull = getattr(getattr(ship, "hull", None), "spec", None)
    length = getattr(hull, "length_waterline_m", None)
    scale = float(length) / REEVE_REFERENCE_LENGTH_M if length else 1.0
    return float(round(base * max(0.3, min(scale, 2.0))))


def reeve_refusal(ship: Ship, line: Any, splice: bool = False) -> str | None:
    """Why this line cannot be rove afresh (or spliced) now, in a sentence, or None: it
    is standing rigging, it went with a spar that carried away (its gear is rove again
    when the spar is shifted for a spare, `regear`), it is sound, or the boatswain's
    store has not the rope for it."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    if not isinstance(line, parts.Line):
        return "Name the line to reeve."
    name = part_name(ship, line.id)
    if line.is_standing:
        return (
            f"The {name} is standing rigging, set up with deadeyes and lanyards; it is not "
            f"rove, and nothing here sets it up afresh yet."
        )
    if line.wrecked:
        return (
            f"The {name} went with its spar when it carried away; clear the wreck and shift "
            f"the spar for a spare, and its gear is rove again with the rest."
        )
    if line.state is not LineState.PARTED:
        done = "spliced" if splice else "rove afresh"
        return f"The {name} is sound and rove; only a parted line is {done}."
    if not splice:
        store = parts.cordage(ship)
        wants = line_fathoms(ship, line)
        if store.fathoms + 1e-9 < wants:
            have = round(store.fathoms)
            if have <= 0:
                return (
                    f"There is no spare cordage in the boatswain's store to reeve a new "
                    f"{name}; splice it instead, or wait for the dockyard."
                )
            return (
                f"There {'is' if have == 1 else 'are'} but {have} fathom{'s' if have != 1 else ''} "
                f"of spare cordage in the boatswain's store; a new {name} wants {wants:g}. "
                f"Splice it instead."
            )
    return None


def _line_part(ship: Ship, params: dict[str, Any], words: dict[str, Any] | None) -> Any:
    """The line a reeve works on: `params["line"]` (the verbs pass it), or the subject the
    runner names in its words."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    lid = params.get("line")
    if isinstance(lid, str) and lid in ship.lines:
        return ship.lines[lid]
    name = (words or {}).get("subject")
    for ln in ship.lines.values():
        if part_name(ship, ln.id) == name:
            params["line"] = ln.id
            return ln
    return None


class ReeveScript(PhasedScript):
    """Reeve a new line in the place of one that has parted, from the coil in the
    boatswain's store, or splice the parted ends (`params.splice`): package 31b, from
    playtest 11's finding 7. Running rigging is what "reeves through blocks, or sheave
    holes" (Lever 1808, 'Rigging'), "got out in the coil, and cut to proper lengths when
    reeved on board" (Steel 1794, vol. I); "ropes reeving through blocks are joined by a
    long splice ... the splice is weaker than the main part of the rope by about
    one-eighth" (Luce 1884, ch. II). Phases:
      cut     on deck: the coil roused up, the length measured off and cut
      reeve   aloft: the new line rove through its blocks and belayed slack
      splice  aloft: the two ends brought together and spliced (a splice alone)
    A new line is whole at the ship file's rating; a spliced one at seven eighths. A
    yard that swung when its brace parted is a yard again (to be braced by order); a
    sail that came down or flogged is set again by order, its gear being whole."""

    DEFAULTS = {"cut": 60.0, "reeve": 240.0, "splice": 300.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.line = _line_part(ship, params, None)
        self.splice = bool(params.get("splice"))
        self.fathoms = 0.0

    def _name(self, part: Any) -> str:
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        return part_name(self.ship, part.id)

    def holds(self) -> set[str]:
        """The line, and the sail or the yard it serves, so that a set or a brace given
        behind the reeve waits its turn."""
        if not isinstance(self.line, parts.Line):
            return set()
        held = {self.line.id}
        if self.line.of in self.ship.parts:
            held.add(self.line.of)
        return held

    def check(self, words: dict[str, Any]) -> str | None:
        if self.line is None:
            self.line = _line_part(self.ship, self.params, words)
        return reeve_refusal(self.ship, self.line, self.splice)

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["splice"] if self.splice else ["cut", "reeve"])

    def end_phase(self, name: str) -> None:
        ship, line = self.ship, self.line
        if name == "cut":
            store = parts.cordage(ship)
            wants = line_fathoms(ship, line)
            if store.fathoms + 1e-9 < wants:  # taken by another reeve meanwhile
                self.fail(
                    f"there {'is' if round(store.fathoms) == 1 else 'are'} but "
                    f"{round(store.fathoms)} fathoms of spare cordage left in the boatswain's "
                    f"store, and a new {self._name(line)} wants {wants:g}"
                )
                return
            store.take(wants)
            ship.extra["spare_cordage_fathoms"] = store.fathoms
            self.fathoms = wants
            self.note(
                f"Roused up the coil and measured off {wants:g} fathoms for the new "
                f"{self._name(line)}."
            )
        elif name in ("reeve", "splice"):
            self._make_whole(new=name == "reeve")

    def _make_whole(self, new: bool) -> None:
        ship, line = self.ship, self.line
        line.state = LineState.FREE if line.cls == "bowline" else LineState.BELAYED
        line.hauled = 0.0 if line.cls in _ROVE_SLACK_CLASSES else 1.0
        line.load_kn = 0.0
        if new:
            spec = next((ln for ln in ship.spec.lines if ln.id == line.id), None)
            if spec is not None and spec.rating_kn:
                line.rating_kn = float(spec.rating_kn)
            line.condition = 100.0
        else:
            line.rating_kn = line.rating_kn * SPLICED_STRENGTH
        target = ship.parts.get(line.of)
        if line.cls == "brace" and isinstance(target, Spar):
            from freesail.physics.strain import strain_state  # local import to avoid a cycle

            strain_state(ship).swung.discard(target.id)

    def _ready_words(self) -> str:
        """What the whole line lets the captain do: 'the fore topsail may be sheeted home
        and set', 'the main topsail yard may be braced again'."""
        ship, line = self.ship, self.line
        target = ship.parts.get(line.of)
        if isinstance(target, Sail):
            if line.cls == "sheet":
                return f"the {self._name(target)} may be sheeted home and set"
            if line.cls in ("halyard", "throat_halyard", "peak_halyard"):
                return f"the {self._name(target)} may be hoisted again"
            return f"the {self._name(target)} may be worked again"
        if isinstance(target, Spar):
            if line.cls == "brace":
                return f"the {self._name(target)} may be braced again"
            if line.cls in ("halyard", "throat_halyard", "peak_halyard"):
                sails = ship.sails_using(target)
                if sails:
                    return f"the {self._name(sails[0])} may be hoisted again"
            return f"the {self._name(target)} may be worked again"
        return "it may be worked again"

    def words(self) -> dict[str, Any]:
        ship, line = self.ship, self.line
        if not isinstance(line, parts.Line):
            return {}
        name = self._name(line)
        store = parts.cordage(ship)
        if self.splice:
            begin = f"Splice the {name}! A marline-spike and a fid aloft."
            done = f"Spliced the {name}, an eighth the weaker for it; {self._ready_words()}."
        else:
            begin = f"Reeve a new {name}! Rouse up the coil from the boatswain's store."
            done = (
                f"Rove a new {name}; {self._ready_words()}. {store.describe().capitalize()} "
                f"left in the boatswain's store."
            )
        return {
            "begin": begin,
            "done": done,
            "verb_word": "splice" if self.splice else "reeve",
            "fathoms": self.fathoms,
            "cordage_left": store.describe(),
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        if isinstance(self.line, parts.Line):
            d["line"] = self.line.id
        d["splice"] = self.splice
        d["fathoms"] = self.fathoms
        d["cordage_left_fathoms"] = round(parts.cordage(self.ship).fathoms, 1)
        return d


# ---------------------------------------------------------------------------
# Package 32e: the sheet holds the trim (spec M5 open item 13)
# ---------------------------------------------------------------------------


class TrimSheetScript(Script):
    """Trim a fore-and-aft sail's sheet: hands work the sheet to the length the wanted
    angle needs, over a time set by the sail's size, and belay it (`trim_gaff_sheet.yaml`,
    `trim_jib_sheet.yaml`). The angle wanted is `params["angle_deg"]`, or the trim for
    the apparent wind as the script begins (`trim.wanted_sheet_angle`); the side is
    `params["side"]` (weather, lee or none: the lee side). A sheet let fly is taken up and
    hauled as part of it; of a pair the other sheet is let go, as "Draw jib!" has it.
    The sail's angle reading follows the sheet as it is worked, so the physics feels the
    change progressively, as a brace's ramp is felt."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sail: Sail | None = None
        self.line: Any = None
        self.start_hauled = 1.0
        self.target_hauled = 1.0
        self.target_angle = 0.0
        self.duration_s = 30.0
        self.progress = 0.0
        self.last_set = 1.0

    def holds(self) -> set[str]:
        held: set[str] = set()
        sail = _subject_sail(self.ship, self.params, None)
        if sail is not None:
            held.add(sail.id)
            held |= {ln.id for ln in self.ship.sheets_of(sail)}
        return held

    def check(self, words: dict[str, Any]) -> str | None:
        sail = _subject_sail(self.ship, self.params, words)
        if sail is None:
            return "no such sail"
        if not sail.is_fore_and_aft:
            return f"the {words.get('subject', 'sail')} is trimmed by its yard, not a sheet"
        if not self.ship.sheets_of(sail):
            return f"the {words.get('subject', 'sail')} has no sheet"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        sail = _subject_sail(self.ship, self.params, words)
        assert sail is not None
        self.sail = sail
        geo = yard_trim.sheet_geometry(self.ship, sail)
        self._aim(geo)
        side = self.params.get("side")
        side = side if side in ("weather", "lee", "starboard", "larboard") else None
        self.line = yard_trim.working_sheet(self.ship, sail, side)
        if self.line is not None:
            if self.line.state is LineState.FREE:
                # a sheet let fly is taken up first: its scope is what it ran out to
                self.line.hauled = min(self.line.hauled, 0.0)
            self.line.state = LineState.BELAYED
            self.start_hauled = self.line.hauled
            if self.line.side is None:
                lee = yard_trim.side_name(yard_trim.lee_side_sign(self.ship))
                weather = "larboard" if lee == "starboard" else "starboard"
                self.line.held_side = weather if side == "weather" else None
            else:
                for other in self.ship.sheets_of(sail):
                    if other is not self.line and other.state is LineState.BELAYED:
                        other.state = LineState.FREE
                        other.hauled = 0.0
        else:
            self.start_hauled = self.target_hauled
        yard_trim.refresh_reading(self.ship, sail)
        self.last_set = self.line.hauled if self.line is not None else self.start_hauled
        per_m2 = self.timing_value("seconds_per_m2", 0.3)
        lo, hi = self.timing_value("min_s", 15.0), self.timing_value("max_s", 120.0)
        self.duration_s = max(lo, min(hi, per_m2 * sail.area_m2))
        self.progress = 0.0
        self.phase = "hauling" if self.target_hauled >= self.start_hauled else "easing"

    def _aim(self, geo: yard_trim.SheetGeometry) -> None:
        """The trim wanted: the angle ordered, or the trim for the apparent wind as it
        stands now (the hands trim to the wind they feel, not the one at the order)."""
        assert self.sail is not None
        angle = self.params.get("angle_deg")
        if isinstance(angle, int | float):
            wanted = units.deg_to_rad(float(angle))
        else:
            wanted = yard_trim.wanted_sheet_angle(self.sail.cls, self.ship.dyn.apparent_wind_angle)
        self.target_angle = max(geo.floor, min(geo.ceiling, wanted))
        self.target_hauled = geo.hauled_from_angle(self.target_angle)

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        if self.sail is None:
            self.fail("no sail to trim")
            return
        if self.line is not None and (
            self.line.state is not LineState.BELAYED or abs(self.line.hauled - self.last_set) > 1e-9
        ):
            # other hands have the sheet (a manoeuvre's, or an order at the pin): the
            # party gives way, and the sheet stands where they put it
            self.line = None
            self.finish()
            return
        self._aim(yard_trim.sheet_geometry(self.ship, self.sail))
        self.progress = min(1.0, self.progress + dt / (self.duration_s * factor))
        if self.line is not None:
            self.line.hauled = self.start_hauled + (self.target_hauled - self.start_hauled) * (
                self.progress
            )
            self.line.state = LineState.BELAYED
            self.last_set = self.line.hauled
        yard_trim.refresh_reading(self.ship, self.sail)
        if self.progress >= 1.0 - 1e-9:
            if self.line is not None:
                self.line.hauled = self.target_hauled
            yard_trim.refresh_reading(self.ship, self.sail)
            self.finish()

    def remaining_s(self) -> float:
        return (1.0 - self.progress) * self.duration_s

    def words(self) -> dict[str, Any]:
        angle = self.sail.sheet_angle if self.sail is not None else self.target_angle
        held = ""
        if self.line is not None and self.params.get("side") == "weather":
            held = " to windward"
        return {"angle_words": yard_trim.angle_words(angle) + held}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["sheet_deg"] = round(units.rad_to_deg(self.target_angle), 1)
        return d


# ---------------------------------------------------------------------------
# Package 34: the ground tackle (spec M5 §18; decision 30)
# ---------------------------------------------------------------------------
#
# The anchor's evolutions, as Luce 1866 ch. XXI and XXXIV, Lever 1808 and Steel 1794 vol.
# II have them (the files under data/evolutions/ cite the pages). Each script works the
# ship's `GroundTackle` (`ship.parts.ground_tackle`): the anchors' states, the cable
# veered or hove in by the fathom at the file's rates; the physics of the cable's pull,
# the holding and the dragging is `physics/anchor.py`, and the World says the riding, the
# turn of the tide and an anchor dragging. The depth the anchor goes down in is the
# truth's (the World keeps `ship.extra["water_depth_m"]` up each minute: the chart's depth
# and the tide), which is what the lead in the chains calls as the cable runs.


def _tackle(ship: Ship) -> Any:
    from freesail.ship.parts import ground_tackle

    return ground_tackle(ship)


def _water_depth(ship: Ship) -> float | None:
    depth = ship.extra.get("water_depth_m")
    return None if depth is None else float(depth)


def _hawse(ship: Ship) -> tuple[float, float]:
    from freesail.physics.anchor import hawse_position

    return hawse_position(ship)


def _ground_speed(ship: Ship) -> float:
    """Her speed over the ground, metres a second."""
    from freesail.physics.integrate import water_velocity

    d = ship.dyn
    wx, wy = water_velocity(ship)
    ex, ey = units.heading_vector(d.heading)
    return math.hypot(d.u * ex + d.v * ey + wx, d.u * ey - d.v * ex + wy)


def _headway_over_ground(ship: Ship) -> float:
    """Her way along her head over the ground, metres a second (negative astern)."""
    from freesail.physics.integrate import water_velocity

    d = ship.dyn
    wx, wy = water_velocity(ship)
    ex, ey = units.heading_vector(d.heading)
    return d.u + wx * ex + wy * ey


def _fathoms_words(fathoms: float) -> str:
    from freesail.world.reckoning import number_words

    n = int(round(fathoms))
    return f"{number_words(n)} fathom{'s' if n != 1 else ''}"


def _depth_words(depth_m: float | None) -> str:
    from freesail.world.chart import fathoms_words

    return "no bottom" if depth_m is None else fathoms_words(depth_m)


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]


def _riding(ship: Ship, wind: Wind | None) -> str:
    from freesail.physics.anchor import riding_words

    state = ship.extra.get("tide_state")
    wind_from = wind.direction_from if wind is not None else float(ship.dyn.heading)
    return riding_words(ship, state, wind_from)


class _AnchorScript(Script):
    """What the anchor scripts share: the tackle found, the anchor named, the cable
    veered or hove by the fathom at a rate."""

    # the scope each other anchor had before its cable was veered to follow this one's
    # coming in (package 37f); a class default for a checkpoint from an earlier build
    followed: dict[str, float] | None = None

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.tackle = _tackle(ship)
        self.anchor: Any = None
        self.wind: Wind | None = None
        self.followed = None

    def holds(self) -> set[str]:
        return {self.ship.name}

    def _no_tackle(self) -> str | None:
        if self.tackle is None or not self.tackle.anchors:
            return "she carries no ground tackle"
        return None

    def _named(self, words: Any) -> Any:
        anchor = self.tackle.by_words(words if isinstance(words, str) else None)
        return anchor

    def _worked(self) -> str | None:
        """The anchor an order to veer or heave in works: the one it names
        (`params["anchor"]`), which must be down, or the one she rides by. Sets
        `self.anchor`; returns the refusal in words, which name the anchor she rides by
        (package 37f: `veer the small bower to 80 fathoms` veered the best bower, and
        `weigh the small bower` weighed it, without a word)."""
        riding = self.tackle.riding_by()
        if riding is None:
            hanging = hanging_anchor(self.tackle, self.params.get("anchor"))
            if hanging is not None:
                # package 37k (game 10: `weigh the best bower` was answered "no anchor is
                # down" with the best bower hanging at the bows after a belay)
                return f"no anchor is down: {anchor_left_words(hanging)}"
            return "no anchor is down"
        named = self.params.get("anchor")
        if not named:
            self.anchor = riding
            return None
        anchor = self._named(named)
        if anchor is None:
            return f"no anchor aboard answers to '{named}'; she rides by {riding.name}"
        if not anchor.down:
            return f"{anchor.name} is {anchor.state.value}, not down; she rides by {riding.name}"
        self.anchor = anchor
        return None

    def _veer(self, dt: float, factor: float, target_m: float, rate_key: str) -> bool:
        """The cable veered toward `target_m` at the file's rate; True when there."""
        rate = units.fathoms_to_m(self.timing_value(rate_key, 1.0)) / max(factor, 1e-9)
        limit = min(target_m, units.fathoms_to_m(self.anchor.cable_fathoms))
        self.anchor.scope_m = min(limit, self.anchor.scope_m + rate * dt)
        return self.anchor.scope_m >= limit - 1e-6

    def _heave(self, dt: float, factor: float, target_m: float, rate_key: str) -> bool:
        """The cable hove in toward `target_m` at the capstan's rate; True when there."""
        rate = units.fathoms_to_m(self.timing_value(rate_key, 0.1)) / max(factor, 1e-9)
        self.anchor.scope_m = max(target_m, self.anchor.scope_m - rate * dt)
        return self.anchor.scope_m <= target_m + 1e-6

    def _follow(self, dt: float, factor: float) -> None:
        """Another anchor down while this one's cable comes in: its cable veered to
        follow (`_veer_to_follow`), and what it had out before remembered for the words.
        Without it a moored ship hove toward one anchor drags the other home (package
        37f: the review's table of the ground-tackle orders, run moored)."""
        others = [a for a in self.tackle.down() if a is not self.anchor]
        if not others:
            return
        if self.followed is None:
            self.followed = {a.id: a.scope_m for a in others}
        _veer_to_follow(
            self.ship, self.anchor, others, dt, factor, self.timing_value("veer_fathoms_per_s", 1.0)
        )

    def _followed_words(self) -> str:
        """'; the small bower's cable veered to ninety fathoms as it came in', or nothing."""
        said = []
        for a in self.tackle.down() if self.tackle is not None else []:
            before = (self.followed or {}).get(a.id)
            if before is not None and a.scope_m > before + units.fathoms_to_m(1.0):
                said.append(
                    f"{a.name}'s cable veered to {_fathoms_words(a.scope_fathoms)} as it came in"
                )
        return ("; " + "; ".join(said)) if said else ""

    def left_words(self) -> str | None:
        """'the best bower aweigh and hanging at the bows, to be let go again or catted
        and fished': where the work leaves the anchor (package 37k)."""
        if self.anchor is None:
            return None
        return anchor_left_words(self.anchor)

    def belayed(self) -> None:
        if self.anchor is not None:
            self.anchor.heaving = False  # the bars unshipped: she rides by it again

    def words(self) -> dict[str, Any]:
        anchor = self.anchor.name if self.anchor is not None else "the anchor"
        fathoms = self.anchor.scope_fathoms if self.anchor is not None else 0.0
        depth = self.anchor.depth_m if self.anchor is not None else _water_depth(self.ship)
        return {
            "anchor": anchor,
            "anchor_cap": _cap(anchor),
            "fathoms": _fathoms_words(fathoms),
            "depth": _depth_words(depth),
            "riding": _riding(self.ship, self.wind),
            "followed": self._followed_words(),
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        if self.anchor is not None:
            d["anchor"] = self.anchor.to_dict()
        return d


def _belay_held_work(ship: Ship) -> None:
    """The sail work the manoeuvre belayed, or that waited its turn for hands while all
    hands were at the anchor, is not taken up at anchor (the runner resumes a manoeuvre's
    belayed work when all hands are done, decision 25; a sail half set when she came to
    anchor is furled with the rest and its order is done with, and a trim that waited
    finds no sail to trim)."""
    runner = ship.extra.get("evolutions")
    if runner is None or not hasattr(runner, "belay"):
        return
    held = [
        i for i in runner.instances if getattr(i, "paused", False) or getattr(i, "waiting", False)
    ]
    if held:
        runner.belay(ship, held)


# The states of an anchor that can be let go (package 37k): at the bows, catted and
# fished; a-cockbill; hanging at the cat-head, catted and not fished ("suspended at the
# cat-head by its stopper, ready to be sunk from the bow at a moment's warning", Falconer
# 1780, ANCHOR a cock-bill); and aweigh, broken out and hanging by its cable under the
# hawse, which is let go by letting the cable run. In game 10 the best bower was left
# aweigh by a belay of getting under way and every order to let it go was refused ("the
# best bower is aweigh") until it had been catted and fished, fourteen minutes; an
# anchor hanging at the bows is the one that can be let go soonest.
LET_GO_STATES = ("at the bows", "a-cockbill", "aweigh", "catted")


def can_let_go(anchor: Any) -> bool:
    return anchor.state.value in LET_GO_STATES


def hanging_anchor(tackle: Any, named: Any = None) -> Any:
    """The anchor the words name if it hangs at the bows (aweigh or catted), else the
    first that does when none is named; None when none does."""
    from freesail.ship.parts import AnchorState

    hanging = (AnchorState.AWEIGH, AnchorState.CATTED)
    if named:
        anchor = tackle.by_words(named if isinstance(named, str) else None)
        return anchor if anchor is not None and anchor.state in hanging else None
    return next((a for a in tackle.anchors if a.state in hanging), None)


def anchor_left_words(anchor: Any) -> str:
    """Where an anchor is, in the forecastle's words, for a belay's line and a refusal
    (package 37k): 'the best bower on the bottom with forty fathoms of cable out'; 'the
    best bower aweigh and hanging at the bows, to be let go again or catted and fished';
    'the best bower at the cat-head, not yet fished, ready to let go'; 'the best bower
    catted and fished'."""
    from freesail.ship.parts import AnchorState

    name = anchor.name
    state = anchor.state
    if state is AnchorState.DOWN:
        return f"{name} on the bottom with {_fathoms_words(anchor.scope_fathoms)} of cable out"
    if state is AnchorState.AWEIGH:
        where = "off the ground under the bows" if anchor.ground_x is not None else "at the bows"
        return f"{name} aweigh and hanging {where}, to be let go again or catted and fished"
    if state is AnchorState.CATTED:
        return f"{name} at the cat-head, not yet fished, ready to let go"
    if state is AnchorState.STOWED:
        return f"{name} catted and fished"
    if state is AnchorState.READY:
        return f"{name} a-cockbill, ready to let go"
    return f"{name} {state.value}"


def _let_go(ship: Ship, anchor: Any, depth_m: float) -> None:
    """The anchor let go where the hawse is: on the bottom, the cable out to the depth,
    the ground the chart's bottom note."""
    from freesail.ship.parts import AnchorState

    hx, hy = _hawse(ship)
    anchor.state = AnchorState.DOWN
    anchor.ground_x, anchor.ground_y = hx, hy
    anchor.depth_m = depth_m
    anchor.scope_m = depth_m
    if end_lying_to(ship):
        # brought to her anchor she is hove to no longer (package 37f): the record
        # cleared and the helm righted
        ship.dyn.helm_mode = HelmMode.RUDDER
        ship.dyn.target_rudder = 0.0
    anchor.bottom = str(ship.extra.get("bottom", "") or "")
    anchor.taut = False
    anchor.dragging = False
    anchor.cable_load_kn = 0.0
    anchor.drag_s = anchor.hold_s = anchor.drag_m = anchor.moved_m = 0.0
    # she is not yet brought up by it: the evolution says when she is, or the World
    # (`World._say_brought_up`, for an anchor let go by itself)
    anchor.brought_up = False


def _scope_wanted(ship: Ship, anchor: Any, depth_m: float, fathoms: Any) -> float:
    from freesail.physics.anchor import scope_wanted_m

    if fathoms:
        return units.fathoms_to_m(float(fathoms))
    return scope_wanted_m(depth_m)


def _scope_plan(anchor: Any, depth_m: float, fathoms: Any) -> tuple[float, str]:
    """The cable an anchor let go in this depth will be given, metres, and the words for
    it as the anchor goes (package 37f; the owner's ruling of 2026-10-07: `let go` keeps
    veering the scope the depth wants, says the figure as it lets go, and takes a number
    when one is given): 'veering to a hundred and thirty fathoms, five times the depth';
    'veering to forty-five fathoms and no further'; or all the cable she has to it, when
    the depth wants more."""
    from freesail.physics.anchor import RIDING_SCOPE_PER_DEPTH, scope_wanted_m
    from freesail.world.reckoning import number_words

    whole_m = units.fathoms_to_m(anchor.cable_fathoms)
    if fathoms:
        target = min(units.fathoms_to_m(float(fathoms)), whole_m)
        return target, f"veering to {_fathoms_words(units.m_to_fathoms(target))} and no further"
    wanted = scope_wanted_m(depth_m)
    times = number_words(int(round(RIDING_SCOPE_PER_DEPTH)))
    if wanted > whole_m + 1e-6:
        return whole_m, (
            f"veering all the cable bent to it, {_fathoms_words(anchor.cable_fathoms)}, "
            f"where {times} times the depth wants {_fathoms_words(units.m_to_fathoms(wanted))}"
        )
    return wanted, (
        f"veering to {_fathoms_words(units.m_to_fathoms(wanted))}, {times} times the depth"
    )


def _low_water_warning(ship: Ship, depth_m: float) -> str | None:
    """'By the master's tide there will be two fathoms here at low water, and she draws
    eleven feet.': the warning as an anchor goes, when the water the lead finds less the
    fall the master reckons to low water (his own tide by the epitome, never the
    world's) is less than her draught; else None (package 37f; the review's 5.8:
    "Nothing checks depth against draught")."""
    world = _world_of(ship)
    nav = getattr(world, "navigation", None)
    fall = getattr(nav, "tide_height_by_master_m", None)
    if fall is None:
        return None
    at_low = depth_m - float(fall())
    draught = float(ship.hull.spec.draught_m)
    if at_low >= draught:
        return None
    feet = int(round(units.m_to_feet(draught)))
    there = "no water" if at_low <= 0.0 else _depth_words(at_low)
    return (
        f"By the master's tide there will be {there} here at low water, and she draws {feet} feet."
    )


def _anchoring_warnings(
    ship: Ship, anchor: Any, depth_m: float, scope_m: float, fathoms: Any = None
) -> None:
    """The notable lines as an anchor goes: the scope when it is more than the cable she
    has, the swinging room on the scope to be veered, and the water at low water against
    her draught."""
    for kind, text in (
        ("anchor.depth_warning", _deep_road_warning(depth_m)),
        ("anchor.scope_warning", _cable_warning(anchor, depth_m, fathoms)),
        ("anchor.scope_warning", _scope_warning(ship, anchor, depth_m, scope_m)),
        ("anchor.depth_warning", _low_water_warning(ship, depth_m)),
    ):
        if text:
            ship.note("notable", kind, text, ship.name, {})


# The deep road (package 37k; the review's G8, game 10: the cutter anchored twice in 45
# to 48 fathoms with nearly the whole of her best bower's cable out, and the officer's
# `let go the small bower` in the same water was refused). What the period did:
# Falconer 1780, ANCHOR-ground, "a bottom which is neither too deep, too shallow, nor
# rocky; as in the first the cable bears too nearly perpendicular, and is thereby apt to
# jerk the anchor out of the ground"; Luce 1866, ch. XXXIV, p. 568, three times the depth
# the old rule of scope and five or six the safer; Luce 1884, ch. XXXIV, "Always
# double-bitt before anchoring in deep water, as at Madeira, and similar anchorages",
# deep water being the exception he names; and the directions this game's charts are
# drawn from put the roads of these waters in three to seventeen fathoms (Carrick Road
# seven to seventeen, St Just Pool fourteen or fifteen, Bertheaume eight to twelve, the
# Bay of Brest eight to sixteen, St Mary's Road four and five). The rule: an anchor is
# not let go where its whole cable gives under three times the depth (`_too_deep`, the
# old rule's scope, the least a ship rides by; the refusal names an anchor whose cable
# would reach), and past `DEEP_ROAD_FATHOMS` the anchor goes with a notable warning that
# this is no road (`_deep_road_warning`). Twenty fathoms: deeper than any road of the
# directions, by three; judgement.
DEEP_ROAD_FATHOMS = 20.0


def _too_deep(tackle: Any, anchor: Any, depth_m: float, where: str) -> str | None:
    """'no anchoring ground here: forty-four fathoms and a half, and the small bower's
    hundred and twenty fathoms of cable give less than three times the depth, the least
    she will ride by; the best bower has two hundred and forty': the refusal when the
    anchor's whole cable is under three times the depth (Luce's old rule of scope;
    Falconer's ground too deep), naming an anchor whose cable would reach; else None."""
    from freesail.physics.anchor import SHORT_SCOPE_PER_DEPTH
    from freesail.world.reckoning import number_words

    def reaches(a: Any) -> bool:
        return depth_m <= units.fathoms_to_m(a.cable_fathoms) / SHORT_SCOPE_PER_DEPTH

    if reaches(anchor):
        return None
    times = number_words(int(round(SHORT_SCOPE_PER_DEPTH)))
    cable = _fathoms_words(anchor.cable_fathoms)
    why = (
        f"no anchoring ground {where}: {_depth_words(depth_m)}, and {anchor.name}'s {cable} "
        f"of cable give less than {times} times the depth, the least she will ride by"
    )
    other = next(
        (
            a
            for a in (tackle.anchors if tackle is not None else ())
            if a is not anchor and can_let_go(a) and reaches(a)
        ),
        None,
    )
    if other is not None:
        why += f"; {other.name} has {_fathoms_words(other.cable_fathoms)}"
    return why


def _deep_road_warning(depth_m: float) -> str | None:
    """'Forty-five fathoms is deep water to anchor in: the roads lie in seventeen fathoms
    and less, and here she rides on a steep cable and will be long heaving it in.': the
    warning as an anchor goes in more than `DEEP_ROAD_FATHOMS`; else None."""
    if units.m_to_fathoms(depth_m) <= DEEP_ROAD_FATHOMS:
        return None
    return (
        f"{_cap(_depth_words(depth_m))} is deep water to anchor in: the roads lie in "
        "seventeen fathoms and less, and here she rides on a steep cable and will be long "
        "heaving it in."
    )


def _cable_warning(anchor: Any, depth_m: float, fathoms: Any) -> str | None:
    """'The best bower has a hundred and twenty fathoms of cable bent to it, and five
    times the depth wants a hundred and thirty: she will have all of it and no more.':
    the warning when the scope ordered, or the scope the depth wants, is more than the
    cable she has; else None (package 37f, item 7)."""
    from freesail.physics.anchor import RIDING_SCOPE_PER_DEPTH, scope_wanted_m
    from freesail.world.reckoning import number_words

    whole = float(anchor.cable_fathoms)
    if fathoms:
        asked = float(fathoms)
        why = f"{_fathoms_words(asked)} were ordered"
    else:
        asked = units.m_to_fathoms(scope_wanted_m(depth_m))
        times = number_words(int(round(RIDING_SCOPE_PER_DEPTH)))
        why = f"{times} times the depth wants {_fathoms_words(asked)}"
    if asked <= whole + 0.5:
        return None
    return (
        f"{_cap(anchor.name)} has {_fathoms_words(whole)} of cable bent to it, and {why}: "
        "she will have all of it and no more."
    )


# A ship at anchor swings about it with the wind and the tide: the circle's radius is the
# cable along the ground and her own length. The scope is warned of when the circle comes
# within this of the nearest land, as the lookout judges it (package 37f; a cable: the
# brief's figure, the least a prudent officer leaves under his stern).
SWINGING_ROOM_M = units.CABLE


def _scope_warning(ship: Ship, anchor: Any, depth_m: float, scope_m: float) -> str | None:
    """'With a hundred and thirty fathoms out she will swing within a cable of the land to
    the northward.': the warning as the scope is said, when her swinging circle on that
    scope comes within `SWINGING_ROOM_M` of the nearest land by the lookout's judgement
    (his distance by estimation, never the chart's), else None. In game 9 the officer
    veered a hundred and twenty-eight fathoms in a berth two cables from the shore."""
    from freesail.world.reckoning import ward_words

    world = _world_of(ship)
    lookout = getattr(world, "lookout", None)
    if lookout is None:
        return None
    land = lookout.nearest_land(float(ship.dyn.heading))
    if not land:
        return None
    along = math.sqrt(max(scope_m * scope_m - depth_m * depth_m, 0.0))
    room = float(land["metres"]) - (along + ship.hull.length)
    if room >= SWINGING_ROOM_M:
        return None
    toward = units.parse_compass_point(str(land.get("bearing") or ""))
    where = f" {ward_words(toward)}" if toward is not None else ""
    out = _fathoms_words(units.m_to_fathoms(scope_m))
    how = "onto" if room <= 0.0 else "within a cable of"
    return f"With {out} out she will swing {how} the land{where}."


class ComeToAnchorScript(_AnchorScript):
    """Come to an anchor as Luce has it (data/evolutions/come_to_anchor.yaml)."""

    let_go_depth: float | None = None  # "in twelve fathoms": the depth to let go in, metres

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.target: float = 0.0
        self.heading_target: float | None = None
        self.swing: YardSwing | None = None
        self.phase_t = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if self.tackle.at_anchor():
            riding = self.tackle.riding_by()
            return f"she is at anchor already, riding by {riding.name}"
        if self.ship.extra.get("aground"):
            return "she is aground"
        self.anchor = self._named(self.params.get("anchor"))
        if self.anchor is None:
            return f"no anchor aboard answers to '{self.params.get('anchor')}'"
        if not can_let_go(self.anchor):
            return f"{self.anchor.name} is {self.anchor.state.value}"
        depth = _water_depth(self.ship)
        if depth is None:
            return "no bottom here to anchor in"
        whole = units.fathoms_to_m(self.anchor.cable_fathoms)
        wanted = self.params.get("depth_fathoms")
        if wanted:
            # "come to an anchor in twelve fathoms": the depth to let go in, as the primer
            # has it; she stands on until the lead calls it (package 37f)
            self.let_go_depth = units.fathoms_to_m(float(wanted))
            depth = self.let_go_depth
        if why := _too_deep(self.tackle, self.anchor, depth, "there" if wanted else "here"):
            return why
        scope = self.params.get("fathoms")
        if scope and units.fathoms_to_m(float(scope)) < depth:
            return (
                f"{_fathoms_words(float(scope))} of cable will not reach the bottom in "
                f"{_depth_words(depth)}"
            )
        if scope and units.fathoms_to_m(float(scope)) > whole + 1e-6:
            return (
                f"{self.anchor.name} has but {_fathoms_words(self.anchor.cable_fathoms)} of "
                f"cable bent to it"
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        ship = self.ship
        depth = _water_depth(ship)
        if self.let_go_depth is not None and (depth is None or depth > self.let_go_depth):
            self.phase = "stand_on"
            self.phase_t = 0.0
            self.note(
                f"Stand on until the lead calls {_depth_words(self.let_go_depth)}; the anchor "
                "clear for letting go."
            )
            return
        self._shorten_sail()

    def _shorten_sail(self) -> None:
        ship = self.ship
        self.phase = "shorten_sail"
        self.phase_t = 0.0
        light = [
            sl
            for sl in ship.sails.values()
            if sl.is_set and (sl.cls == "studding" or _is_upper_square(ship, sl))
        ]
        for sl in light:
            sl.state = SailState.IN_THE_GEAR
        for sl in lowest_square_sails(ship):
            if sl.is_set:
                sl.state = SailState.IN_THE_GEAR
        if light or any(True for _ in lowest_square_sails(ship)):
            self.note("Haul taut! In studding sails, royals and topgallants; up courses.")

    def _stronger(self, wind: Wind) -> float:
        """The heading to come to: the stream's if it runs stronger than
        `stem_tide_kn`, else the wind's (Luce 1866 ch. XXXIV, p. 573)."""
        from freesail.physics.integrate import water_velocity

        wx, wy = water_velocity(self.ship)
        stream_kn = units.ms_to_knots(math.hypot(wx, wy))
        if stream_kn >= self.timing_value("stem_tide_kn", 1.5):
            # head to the stream: the way it comes from
            return units.wrap_2pi(math.atan2(-wx, -wy))
        return units.wrap_2pi(wind.direction_from)

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        dyn = ship.dyn
        if self.phase == "stand_on":
            depth = _water_depth(ship)
            assert self.let_go_depth is not None
            if depth is not None and depth <= self.let_go_depth:
                self.note(f"The lead calls {_depth_words(depth)}.")
                self._shorten_sail()
            elif self.phase_t >= self.timing_value("stand_on_timeout_s", 3600.0):
                self.fail(
                    f"the lead has not called {_depth_words(self.let_go_depth)} in an hour's "
                    f"standing on; {_depth_words(depth)} here"
                )
            return
        if self.phase == "shorten_sail":
            if self.phase_t >= self.timing_value("clew_up_s", 150.0) * factor:
                self.phase = "round_to"
                self.phase_t = 0.0
                self.heading_target = self._stronger(wind)
                dyn.helm_mode = HelmMode.HEADING
                dyn.target_heading = self.heading_target
                dyn.steady = False
                # the topsails clewed up and the jib hauled down as she comes to; the
                # spanker kept to bring her up (Luce p. 569)
                for sl in ship.sails.values():
                    if sl.is_set and (sl.cls == "square" or sl.cls == "jibheaded"):
                        sl.state = SailState.IN_THE_GEAR
                _belay_held_work(ship)  # the sail work waiting for hands finds no sail now
                self.note(
                    f"Let go the topsail sheets; clew up; haul down the jib. Helm down for "
                    f"{units.point_name(self.heading_target)}."
                )
            return
        if self.phase == "round_to":
            depth = _water_depth(ship)
            way = _headway_over_ground(ship)
            timeout = self.timing_value("lose_way_timeout_s", 420.0)
            if way <= 0.3 or self.phase_t >= timeout:
                if depth is None:
                    self.fail("no bottom here to anchor in")
                    return
                self.phase = "veer"
                self.phase_t = 0.0
                _let_go(ship, self.anchor, depth)
                self.target, plan = _scope_plan(self.anchor, depth, self.params.get("fathoms"))
                self.note(
                    f"Stand clear of the cable; stream the buoy; let go {self.anchor.name}! "
                    f"Let go in {_depth_words(depth)}."
                )
                ship.note(
                    "notable",
                    "ship.anchored",
                    f"{_cap(self.anchor.name)} let go in {_depth_words(depth)}; {plan}.",
                    ship.name,
                    {
                        "anchor": self.anchor.to_dict(),
                        "scope_fathoms": round(units.m_to_fathoms(self.target), 1),
                    },
                )
                _anchoring_warnings(
                    ship, self.anchor, depth, self.target, self.params.get("fathoms")
                )
            return
        if self.phase == "veer":
            if self._veer(dt, factor, self.target, "veer_fathoms_per_s"):
                self.phase = "brought_up"
                self.phase_t = 0.0
                for sl in after_gaff_sails(ship):
                    if sl.is_set:
                        sl.state = SailState.IN_THE_GEAR
                self.note(
                    f"Veered to {_fathoms_words(self.anchor.scope_fathoms)}; brail up the spanker."
                )
            return
        if self.phase == "brought_up":
            settled = self.anchor.taut and _ground_speed(ship) < 0.3
            if settled or self.phase_t >= self.timing_value("settle_s", 240.0):
                self.phase = "furl"
                self.phase_t = 0.0
                dyn.helm_mode = HelmMode.RUDDER
                dyn.target_rudder = 0.0
                yards = working_yards(ship)
                self.swing = YardSwing(
                    yards, [0.0 for _ in yards], self.timing_value("furl_s", 600.0)
                )
                self.anchor.brought_up = True  # the evolution's own line says so
                self.note("Brought up. Stations for furling sail; square the yards.")
            return
        if self.phase == "furl":
            if self.swing is not None:
                self.swing.advance(dt, factor)
            if self.phase_t >= self.timing_value("furl_s", 600.0) * factor:
                for sl in ship.sails.values():
                    if (
                        sl.state
                        in (
                            SailState.SET,
                            SailState.IN_THE_GEAR,
                            SailState.LOOSED,
                            SailState.SHEETED,
                            SailState.GOOSE_WINGED,
                        )
                        and not sl.wrecked
                    ):
                        sl.state = SailState.FURLED
                _belay_held_work(ship)
                self.finish()

    def remaining_s(self) -> float:
        return (
            max(0.0, self.timing_value("furl_s", 600.0) - self.phase_t)
            if self.phase == "furl"
            else 600.0
        )


def _is_upper_square(ship: Ship, sail: Any) -> bool:
    """A square sail above the topsails: on a topgallant or royal yard."""
    if sail.cls != "square":
        return False
    yard = ship.yard_of(sail)
    parent = ship.parent_of(yard) if yard is not None else None
    return parent is not None and parent.cls in ("topgallant_mast", "royal_mast")


class LetGoAnchorScript(_AnchorScript):
    """Let go an anchor where she is (data/evolutions/let_go_anchor.yaml). It veers the
    scope the depth wants, five times the depth, and its first line says the figure; with
    a number (`let go the best bower and veer to 45 fathoms`) it veers to that and no
    further (package 37f; the owner's ruling of 2026-10-07: the officer of game 9 met the
    scope as a veer that "ran past its number")."""

    # class defaults for the fields package 37f added (a checkpoint from an earlier build)
    plan = ""
    depth0: float | None = None
    warned = True

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.target = 0.0
        self.plan = ""
        self.depth0: float | None = None
        self.warned = False

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if self.ship.extra.get("aground"):
            return "she is aground"
        self.anchor = self._named(self.params.get("anchor"))
        if self.anchor is None:
            return f"no anchor aboard answers to '{self.params.get('anchor')}'"
        from freesail.ship.parts import AnchorState

        if self.anchor.state is AnchorState.DOWN:
            return f"{self.anchor.name} is down already"
        if self.anchor.state is AnchorState.LOST:
            return f"{self.anchor.name} is lost"
        if not can_let_go(self.anchor):
            return f"{self.anchor.name} is {self.anchor.state.value}"
        depth = _water_depth(self.ship)
        if depth is None:
            return "no bottom here to anchor in"
        whole = units.fathoms_to_m(self.anchor.cable_fathoms)
        if (why := _too_deep(self.tackle, self.anchor, depth, "here")) is not None:
            return why
        scope = self.params.get("fathoms")
        if scope and units.fathoms_to_m(float(scope)) < depth:
            return (
                f"{_fathoms_words(float(scope))} of cable will not reach the bottom in "
                f"{_depth_words(depth)}"
            )
        if scope and units.fathoms_to_m(float(scope)) > whole + 1e-6:
            return (
                f"{self.anchor.name} has but {_fathoms_words(self.anchor.cable_fathoms)} of "
                f"cable bent to it"
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "stand_clear"
        # what it will do, said as the order is given: the depth here and the scope
        self.depth0 = _water_depth(self.ship)
        if self.depth0 is not None:
            self.target, self.plan = _scope_plan(
                self.anchor, self.depth0, self.params.get("fathoms")
            )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.wind = wind
        if self.phase == "stand_clear":
            if not self.warned and self.depth0 is not None:
                self.warned = True
                _anchoring_warnings(
                    self.ship, self.anchor, self.depth0, self.target, self.params.get("fathoms")
                )
            if self.t >= self.timing_value("stand_clear_s", 15.0) * factor:
                depth = _water_depth(self.ship)
                if depth is None:
                    self.fail("no bottom here to anchor in")
                    return
                _let_go(self.ship, self.anchor, depth)
                self.target, self.plan = _scope_plan(self.anchor, depth, self.params.get("fathoms"))
                self.phase = "veer"
            return
        if self._veer(dt, factor, self.target, "veer_fathoms_per_s"):
            self.finish()

    def words(self) -> dict[str, Any]:
        d = super().words()
        depth = self.depth0 if self.depth0 is not None else _water_depth(self.ship)
        d["let_go_depth"] = _depth_words(depth)
        d["plan"] = self.plan or "veering to the scope the depth wants"
        return d

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["scope_fathoms"] = round(units.m_to_fathoms(self.target), 1)
        return d

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 60.0
        left = max(0.0, self.target - self.anchor.scope_m)
        return units.m_to_fathoms(left) / max(self.timing_value("veer_fathoms_per_s", 1.0), 0.01)


class VeerCableScript(_AnchorScript):
    """Veer cable on the anchor she rides by, or on the one named
    (data/evolutions/veer_cable.yaml)."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.target = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if (why := self._worked()) is not None:
            return f"{why} to veer on" if why == "no anchor is down" else why
        whole = units.fathoms_to_m(self.anchor.cable_fathoms)
        fathoms = self.params.get("fathoms")
        if fathoms:
            wanted = units.fathoms_to_m(float(fathoms))
            self.target = wanted if self.params.get("to") else self.anchor.scope_m + wanted
        else:
            self.target = self.anchor.scope_m * 4.0 / 3.0
        if self.target <= self.anchor.scope_m + 1e-6:
            out = _fathoms_words(self.anchor.scope_fathoms)
            return (
                f"{self.anchor.name} has {out} out already; to have less out, heave in to "
                f"{float(fathoms):g} fathoms"
                if fathoms
                else f"{self.anchor.name} has {out} out already"
            )
        if self.anchor.scope_m >= whole - 1e-6:
            whole_words = _fathoms_words(self.anchor.cable_fathoms)
            return f"the whole cable is out on {self.anchor.name}, {whole_words}"
        self.target = min(self.target, whole)
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "veer"

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.wind = wind
        if self._veer(dt, factor, self.target, "veer_fathoms_per_s"):
            self.finish()

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 60.0
        left = max(0.0, self.target - self.anchor.scope_m)
        return units.m_to_fathoms(left) / max(self.timing_value("veer_fathoms_per_s", 0.5), 0.01)


class HeaveShortScript(_AnchorScript):
    """Heave in to a short stay (data/evolutions/heave_short.yaml)."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.target = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if (why := self._worked()) is not None:
            return why
        per = self.timing_value("short_stay_per_depth", 1.5)
        self.target = max(self.anchor.depth_m * per, self.anchor.depth_m)
        if self.anchor.scope_m <= self.target + 1e-6:
            out = _fathoms_words(self.anchor.scope_fathoms)
            if self.params.get("anchor"):
                return f"{self.anchor.name} is hove short already, {out} out"
            return f"she is hove short already, {out} out"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "rig_capstan"
        self.anchor.heaving = True

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.wind = wind
        if self.phase == "rig_capstan":
            if self.t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "heave"
                self.note("The messenger passed, the bars shipped and swiftered; heave round!")
            return
        self._follow(dt, factor)
        if self._heave(dt, factor, self.target, "heave_fathoms_per_s"):
            self.anchor.heaving = False
            self.finish()

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 60.0
        left = max(0.0, self.anchor.scope_m - self.target)
        return units.m_to_fathoms(left) / max(self.timing_value("heave_fathoms_per_s", 0.1), 0.01)


class HeaveInScript(_AnchorScript):
    """Heave in so much cable, or to a scope, at the capstan (data/evolutions/heave_in.yaml;
    package 37f: `heave in 70 fathoms` ran as `heave short`, and 163 fathoms came in). On
    the anchor named, or the one she rides by; never to less than the depth, which is the
    cable up and down and the anchor breaking out: that is `weigh`."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.target = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if (why := self._worked()) is not None:
            return why
        fathoms = self.params.get("fathoms")
        if not fathoms or float(fathoms) <= 0.0:
            return "heave in how much? Say 'heave in twenty fathoms' or 'heave in to eighty'"
        wanted = units.fathoms_to_m(float(fathoms))
        out = _fathoms_words(self.anchor.scope_fathoms)
        if self.params.get("to"):
            self.target = wanted
            if self.target >= self.anchor.scope_m - 1e-6:
                return (
                    f"{self.anchor.name} has but {out} out; to have more out, veer to "
                    f"{float(fathoms):g} fathoms"
                )
        else:
            self.target = self.anchor.scope_m - wanted
        if self.target < self.anchor.depth_m - 1e-6:
            per = self.timing_value("short_stay_per_depth", 1.5)
            short = _fathoms_words(units.m_to_fathoms(self.anchor.depth_m * per))
            left = _fathoms_words(units.m_to_fathoms(max(self.target, 0.0)))
            return (
                f"{left} of cable in {_depth_words(self.anchor.depth_m)} of water would have "
                f"{self.anchor.name} off the ground ({out} are out): to heave it up say "
                f"'weigh', and for a short stay, {short}, 'heave short'"
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "rig_capstan"
        self.anchor.heaving = True

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.wind = wind
        if self.phase == "rig_capstan":
            if self.t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "heave"
                self.note("The messenger passed, the bars shipped and swiftered; heave round!")
            return
        self._follow(dt, factor)
        if self._heave(dt, factor, self.target, "heave_fathoms_per_s"):
            self.anchor.heaving = False
            self.finish()

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 60.0
        left = max(0.0, self.anchor.scope_m - self.target)
        return units.m_to_fathoms(left) / max(self.timing_value("heave_fathoms_per_s", 0.1), 0.01)


class WeighAnchorScript(_AnchorScript):
    """Weigh: heave in, break the anchor out, hove up to the bows, cat and fish
    (data/evolutions/weigh_anchor.yaml).

    Package 37f: the anchor named is the one weighed (`weigh the small bower`); with none
    named, the one she rides by. While another anchor holds her, she is hove up to this one
    by the unmoor's method, the other cable veered as this one comes in (Luce 1866, ch.
    XXXIV, 'Unmooring'); where the other cable has not the length to let her come over
    this anchor, the order is refused in words that name the anchor she rides by and what
    would do it. Never another anchor in silence."""

    others: tuple | list = ()  # a class default: a weigh in a checkpoint from an earlier build

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.phase_t = 0.0
        self.hoist_s = 0.0
        self.others: list[Any] = []  # the anchors that still hold her, their cables veered

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        if (why := self._worked()) is not None:
            return why
        if self.ship.extra.get("aground"):
            return "she is aground"
        riding = self.tackle.riding_by()
        self.others = [a for a in self.tackle.down() if a is not self.anchor]
        for other in self.others:
            need = _reach_m(self.ship, self.anchor, other)
            if need is None:
                continue
            whole = units.fathoms_to_m(other.cable_fathoms)
            if need > whole + 1e-6:
                apart = _fathoms_words(units.m_to_fathoms(need))
                return (
                    f"{self.anchor.name} cannot be hove up while {other.name} holds her: to "
                    f"come over it she must have {apart} of {other.name}'s cable, which is "
                    f"{_fathoms_words(other.cable_fathoms)} in all. Weigh {other.name} first"
                    f"{', or unmoor' if len(self.tackle.down()) == 2 else ''}; she rides by "
                    f"{riding.name}"
                )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        per = self.timing_value("short_stay_per_depth", 1.5)
        short = max(self.anchor.depth_m * per, self.anchor.depth_m)
        self.phase = "rig_capstan" if self.anchor.scope_m > short + 1e-6 else "heave"
        self.phase_t = 0.0
        self.anchor.heaving = True

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        if self.phase == "rig_capstan":
            if self.phase_t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "heave"
                self.phase_t = 0.0
                self.note("The messenger passed, the bars shipped and swiftered; heave round!")
            return
        if self.phase == "heave":
            up_and_down = max(self.anchor.depth_m, 1.0)
            # the cables of the anchors that still hold her veered as this one comes in,
            # so that she is hove up to it and not held between the two
            _veer_to_follow(
                ship,
                self.anchor,
                list(self.others),
                dt,
                factor,
                self.timing_value("veer_fathoms_per_s", 1.0),
            )
            if self._heave(dt, factor, up_and_down, "heave_fathoms_per_s"):
                self.phase = "break_out"
                self.phase_t = 0.0
                self.note(
                    f"{_cap(self.anchor.name)}'s cable is up and down."
                    if self.others
                    else "The cable is up and down."
                )
            return
        if self.phase == "break_out":
            if self.phase_t >= self.timing_value("break_out_s", 60.0) * factor:
                self.anchor.state = AnchorState.AWEIGH
                end_lying_to(ship)  # weighing, she is hove to no longer (package 37f)
                self.anchor.heaving = False
                self.anchor.taut = False
                self.anchor.dragging = False
                self.anchor.cable_load_kn = 0.0
                self.anchor.holding_kn = 0.0
                self.phase = "hoist"
                self.phase_t = 0.0
                self.hoist_s = units.m_to_fathoms(self.anchor.depth_m) / max(
                    self.timing_value("hoist_fathoms_per_s", 0.2), 0.01
                )
                ship.note(
                    "notable",
                    "ship.aweigh",
                    f"{_cap(self.anchor.name)} is aweigh.",
                    ship.name,
                    {"anchor": self.anchor.to_dict()},
                )
            return
        if self.phase == "hoist":
            if self.phase_t >= self.hoist_s * factor:
                self.anchor.scope_m = 0.0
                self.anchor.ground_x = self.anchor.ground_y = None
                self.phase = "cat_and_fish"
                self.phase_t = 0.0
                self.note(
                    f"{_cap(self.anchor.name)} up to the bows; avast heaving, pawl the capstan. "
                    f"Hook the cat."
                )
            return
        if self.phase == "cat_and_fish":
            if self.phase_t >= self.timing_value("cat_and_fish_s", 300.0) * factor:
                self.anchor.state = AnchorState.STOWED
                self.finish()

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 60.0
        heave = units.m_to_fathoms(max(0.0, self.anchor.scope_m - self.anchor.depth_m)) / max(
            self.timing_value("heave_fathoms_per_s", 0.1), 0.01
        )
        return (
            heave
            + self.timing_value("break_out_s", 60.0)
            + self.timing_value("cat_and_fish_s", 300.0)
        )

    def words(self) -> dict[str, Any]:
        d = super().words()
        riding = self.tackle.riding_by() if self.tackle is not None else None
        if riding is not None and riding is not self.anchor:
            d["after"] = f"she rides by {riding.name}, {_fathoms_words(riding.scope_fathoms)} out"
        else:
            d["after"] = "she is under way"
        return d


def _reach_m(ship: Ship, anchor: Any, other: Any) -> float | None:
    """The cable `other` must have out for the ship to lie over `anchor`: from her hawse
    there to where `other` lies, with the water over it; None if either is not placed."""
    if None in (anchor.ground_x, anchor.ground_y, other.ground_x, other.ground_y):
        return None
    apart = math.hypot(other.ground_x - anchor.ground_x, other.ground_y - anchor.ground_y)
    return math.hypot(apart, max(other.depth_m, 0.0))


def _veer_to_follow(
    ship: Ship, anchor: Any, others: list[Any], dt: float, factor: float, rate_fm_s: float
) -> None:
    """The cables of the anchors that still hold her veered as `anchor`'s comes in (the
    unmoor's method, for any anchor weighed while another is down: Luce 1866, ch. XXXIV,
    'Unmooring', "veer away on the weather cable as the lee one comes in"). Each is given
    what lets her lie between the two anchors at the scope now out on the one being hove:
    their distance apart less that scope along the ground, with the water over it and a
    fiftieth to spare, as far as it has cable; never taken in. She is so kept riding by the
    other anchor till she is over this one, and the other cable is not run out to let her
    swing round it."""
    rate = units.fathoms_to_m(rate_fm_s) / max(factor, 1e-9)
    if anchor.ground_x is None or anchor.ground_y is None:
        return
    along = math.sqrt(max(anchor.scope_m**2 - max(anchor.depth_m, 0.0) ** 2, 0.0))
    for other in others:
        if not other.down or other.ground_x is None or other.ground_y is None:
            continue
        apart = math.hypot(other.ground_x - anchor.ground_x, other.ground_y - anchor.ground_y)
        line = math.hypot(max(apart - along, 0.0), max(other.depth_m, 0.0))
        wanted = min(1.02 * line, units.fathoms_to_m(other.cable_fathoms))
        if other.scope_m < wanted:
            other.scope_m = min(wanted, other.scope_m + rate * dt)


class CatAndFishScript(_AnchorScript):
    """Cat and fish an anchor left aweigh (data/evolutions/cat_and_fish_anchor.yaml)."""

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.ship.parts import AnchorState

        if (why := self._no_tackle()) is not None:
            return why
        named = self.params.get("anchor")
        hanging = [
            a for a in self.tackle.anchors if a.state in (AnchorState.AWEIGH, AnchorState.CATTED)
        ]
        self.anchor = self._named(named) if named else (hanging[0] if hanging else None)
        if self.anchor is None:
            return "no anchor is aweigh to cat and fish"
        if self.anchor.state is AnchorState.STOWED:
            return f"{self.anchor.name} is catted and fished already"
        if self.anchor.state not in (AnchorState.AWEIGH, AnchorState.CATTED):
            return f"{self.anchor.name} is {self.anchor.state.value}"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        from freesail.ship.parts import AnchorState

        self.phase = "fish" if self.anchor.state is AnchorState.CATTED else "cat"

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.wind = wind
        if self.phase == "cat":
            if self.t >= self.timing_value("cat_s", 150.0) * factor:
                self.anchor.state = AnchorState.CATTED
                self.phase = "fish"
                self.note(f"Hooked the cat; {self.anchor.name} up to the cat-head.")
            return
        total = self.timing_value("cat_s", 150.0) + self.timing_value("fish_s", 150.0)
        if self.t >= total * factor:
            self.anchor.state = AnchorState.STOWED
            self.finish()

    def remaining_s(self) -> float:
        return max(
            0.0, self.timing_value("cat_s", 150.0) + self.timing_value("fish_s", 150.0) - self.t
        )


class BackAnchorScript(_AnchorScript):
    """Back the riding anchor with the stream (data/evolutions/back_anchor.yaml)."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.stream: Any = None

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.ship.parts import AnchorState

        if (why := self._no_tackle()) is not None:
            return why
        self.anchor = self.tackle.riding_by()
        if self.anchor is None:
            return "no anchor is down to back"
        self.stream = next((a for a in self.tackle.anchors if a.kind == "stream"), None)
        if self.stream is None:
            return "she carries no stream anchor"
        if self.stream.state is not AnchorState.STOWED:
            return f"the stream anchor is {self.stream.state.value}"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "shackle"

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.wind = wind
        if self.t >= self.timing_value("shackle_s", 240.0) * factor:
            # the stream goes down on the riding cable's line and holds with the bower
            self.stream.state = AnchorState.DOWN
            self.stream.ground_x, self.stream.ground_y = self.anchor.ground_x, self.anchor.ground_y
            self.stream.depth_m = self.anchor.depth_m
            self.stream.scope_m = self.anchor.scope_m
            self.stream.bottom = self.anchor.bottom
            self.finish()

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("shackle_s", 240.0) - self.t)


# ---------------------------------------------------------------------------
# The port (package 35; spec M5 §23): getting under way as Luce has it, mooring and
# unmooring, a kedge laid out by the boat, and the boat sent ashore
# ---------------------------------------------------------------------------


def _world_of(ship: Ship) -> Any:
    """The World the ship sails in, through the standing runtime the World attaches to
    every ship it makes (`orders.prompt.world_of`); None for a ship alone."""
    runtime = ship.extra.get("standing")
    return getattr(runtime, "world", None)


def _topsails(ship: Ship) -> list[Sail]:
    """The topsails: the square sails whose yard crosses a topmast."""
    out = []
    for sl in ship.sails.values():
        if sl.cls != "square" or sl.wrecked:
            continue
        yard = ship.yard_of(sl)
        parent = ship.parent_of(yard) if yard is not None else None
        if parent is not None and parent.cls == "topmast":
            out.append(sl)
    return out


def _boom_mainsails(ship: Ship) -> list[Sail]:
    """A fore-and-after's gaff sails on a boom (the mainsail she gets under way under),
    set or not; nothing on a ship with yards on two masts (her spanker is set last)."""
    if len(_masts_with_yards(ship)) >= 2:
        return []
    return [
        sl
        for sl in ship.sails.values()
        if sl.cls == "gaff" and not sl.wrecked and ship.spar_of_role(sl, "boom") is not None
    ]


def _head_sails_all(ship: Ship) -> list[Sail]:
    """The jibs and fore staysails that are bent, set or not: the jib-headed sails
    forward of the foremost mast with sheets, inboard first."""
    masts = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    fore_x = max((m.x_m for m in masts), default=0.0)
    out = [
        sl
        for sl in ship.sails.values()
        if sl.cls == "jibheaded"
        and not sl.wrecked
        and sl.state is not SailState.UNBENT
        and sl.x_m > fore_x
        and ship.sheets_of(sl)
    ]
    return sorted(out, key=lambda sl: sl.x_m)


def _jib(ship: Ship) -> list[Sail]:
    """The jib she casts under: the sail named so among the head sails bent, else the
    outermost of them (a cutter's single jib, a schooner's)."""
    heads = _head_sails_all(ship)
    named = [sl for sl in heads if sl.id.split(".")[-1] == "jib"]
    if named:
        return named[:1]
    return heads[-1:]


def _set_fore_and_aft(ship: Ship, sails: list[Sail], tack: str) -> None:
    """Set these fore-and-aft sails and draw their sheets on the lee side of `tack`."""
    lee = "larboard" if tack == "starboard" else "starboard"
    for sl in sails:
        if sl.state in (SailState.FURLED, SailState.LOOSED, SailState.IN_THE_GEAR):
            sl.state = SailState.SET
            sl.reefs = 0
    drawing = [sl for sl in sails if sl.is_set]
    if drawing:
        draw_sheets(ship, drawing, lee)


class GetUnderWayScript(_AnchorScript):
    """Get under way as Luce has it (data/evolutions/get_under_way.yaml): heave short,
    loose and sheet home the topsails, weigh, cast her on the tack wanted; the anchor
    catted and fished as she pays off.

    Package 37f (the review of gate 5c's playtests, 5.8, "Getting under way"): a vessel
    whose yards are all on one mast casts as a fore-and-after does, her jib's sheet held
    to windward, her mainsail's eased till she has cast, and her helm tended (a-lee
    while she drops astern, up when she has headway); and "paid off" is never said on a
    timeout: at cast_timeout_s she is taken as she lies, on the tack wanted, on the
    other (which the line says, and she is got under way on it), or hanging head to
    wind, when she is given till cast_give_up_s and the evolution then fails in words."""

    fore_and_aft = False  # a class default, for a checkpoint from an earlier build
    main_eased = False  # the same: her main sheet eased off as she pays off

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.phase_t = 0.0
        self.tack = "starboard"
        self.course: float | None = None
        self.sign = 1.0
        self.swing: YardSwing | None = None
        self.short_m = 0.0
        self.hoist_s = 0.0
        self.anchor_t = 0.0  # the anchor's own clock from the break-out: hoisting, catting
        self.anchor_phase = ""
        self.cast_done = False
        self.fore_and_aft = False
        self.sails_words = "under topsails and jib"
        self.pilot_course = False
        self.course_not_laid: float | None = None

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        down = self.tackle.down()
        if not down:
            return "no anchor is down: she is under way already, or adrift"
        if len([a for a in down if a.kind == "bower"]) >= 2:
            return "she is moored; unmoor first, to single anchor"
        if self.ship.extra.get("aground"):
            return "she is aground"
        world = _world_of(self.ship)
        ports = getattr(world, "ports", None)
        if ports is not None and ports.boat.away:
            return f"{ports.boat.boat_name} is away; she cannot leave without her boat"
        self.anchor = self.tackle.riding_by()
        tack = self.params.get("tack")
        if tack in ("port",):
            tack = "larboard"
        pilot = ports.pilot_reading() if ports is not None else None
        if tack in ("starboard", "larboard"):
            self.tack = tack
        elif pilot is not None:
            self.tack = str(pilot.get("cast") or "starboard")
        course = self.params.get("course_deg")
        if course is not None:
            self.course = units.deg_to_rad(float(course))
        elif pilot is not None and pilot.get("course_out_deg") is not None:
            self.course = units.deg_to_rad(float(pilot["course_out_deg"]))
            self.pilot_course = True
        self.sign = 1.0 if self.tack == "starboard" else -1.0
        return None

    def begin(self, words: dict[str, Any]) -> None:
        per = self.timing_value("short_stay_per_depth", 1.5)
        self.short_m = max(self.anchor.depth_m * per, self.anchor.depth_m)
        self.phase = "rig_capstan" if self.anchor.scope_m > self.short_m + 1e-6 else "loose"
        self.phase_t = 0.0
        self.anchor.heaving = True
        self.fore_and_aft = len(_masts_with_yards(self.ship)) < 2
        if self.phase == "loose":
            self._begin_loose()

    def _sheer_helm(self) -> None:
        """A fore-and-after's helm, tended from the first heave till she has cast
        (package 37f): put over to sheer her head across the wind for the tack wanted
        while she has way through the water (heaving up to her anchor she has, and in a
        stream), a-lee for the stern-board when she has none or drops astern. Left where
        the last course had it, as it was, the helmsman steered for that course as the
        capstan drew her ahead, and sheered her as often the wrong way as the right: the
        wind was then three and four points on the wrong bow when the anchor broke out,
        and no jib will throw her head across the wind from there."""
        dyn = self.ship.dyn
        helm = units.deg_to_rad(15.0)
        dyn.helm_mode = HelmMode.RUDDER
        dyn.steady = False
        dyn.target_rudder = -self.sign * helm if dyn.u > 0.15 else self.sign * helm

    def _steady_boom_over(self) -> None:
        """Her main boom steadied over to the side she is to cast toward (see the tick)."""
        mains = [sl for sl in _boom_mainsails(self.ship) if sl.is_set]
        angle = units.deg_to_rad(self.timing_value("cast_boom_deg", 30.0))
        sheets_to(self.ship, mains, _lee_name(self.sign), angle)
        for sl in mains:
            for ln in self.ship.sheets_of(sl):
                if ln.side is None and ln.state is LineState.BELAYED:
                    # held there whichever bow the wind is on (a sheet worked to the lee
                    # side of the moment is not held, and the boom would swing across)
                    ln.held_side = _lee_name(self.sign)
            yard_trim.refresh_reading(self.ship, sl)

    def _begin_loose(self) -> None:
        ship = self.ship
        self.phase = "loose"
        self.phase_t = 0.0
        tops = _topsails(ship)
        mains = _boom_mainsails(ship)
        for sl in tops:
            if sl.state is SailState.FURLED:
                sl.state = SailState.LOOSED
        names = []
        if tops:
            names.append("topsails" if len(tops) > 1 else "the topsail")
        if mains:
            names.append("the mainsail")
        self.sails_words = (
            "under " + " and ".join(names + ["the jib"]) if names else "under the jib"
        )
        self.note(
            "Pawl the capstan; stopper the cable. Stations for loosing sail! Lay aloft, "
            "sail-loosers! Man the topsail sheets and halliards."
        )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        dyn = ship.dyn
        if self.swing is not None:
            self.swing.advance(dt, factor)
        if self.fore_and_aft and self.phase in (
            "rig_capstan",
            "heave_short",
            "loose",
            "heave",
            "break_out",
        ):
            self._sheer_helm()
        if self.phase == "rig_capstan":
            if self.phase_t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "heave_short"
                self.phase_t = 0.0
                self.note("The messenger passed, the bars shipped and swiftered; heave round!")
            return
        if self.phase == "heave_short":
            if self._heave(dt, factor, self.short_m, "heave_fathoms_per_s"):
                self._begin_loose()
            return
        if self.phase == "loose":
            if self.phase_t >= self.timing_value("loose_s", 240.0) * factor:
                tops = _topsails(ship)
                for sl in tops:
                    if sl.state in (SailState.LOOSED, SailState.FURLED, SailState.IN_THE_GEAR):
                        sl.state = SailState.SET
                        sl.reefs = 0
                mains = _boom_mainsails(ship)
                _set_fore_and_aft(ship, mains, self.tack)
                # A fore-and-after's mainsail is hoisted with its boom steadied over to
                # the side she is to cast toward, the lee side of the tack wanted (package
                # 37f; Luce 1884, ch. XXXIV, 'Getting under way.--Schooners': "To cast to
                # starboard, heave up the anchor, putting the helm a starboard, main boom
                # steadied over to starboard ... hoist the staysail, or staysail and jib,
                # with the port sheets aft"). So held, the wind ahead or on either bow
                # takes it on its fore side and drives her stern the other way: she is
                # sheered for the tack while the anchor still holds her, and cast when it
                # is aweigh. Set flat aft for the tack, as it was, it held her head to the
                # wind, and all three of a schooner's casts in the playtests timed out
                # (the review's 5.8).
                self._steady_boom_over()
                self.fore_and_aft = len(_masts_with_yards(ship)) < 2
                head, after = head_and_after_yards(ship)
                yards = head + after
                targets = [-self.sign * y.brace_limit for y in head] + [
                    self.sign * y.brace_limit for y in after
                ]
                _belay_held_work(ship)
                self.phase = "heave"
                self.phase_t = 0.0
                if self.fore_and_aft:
                    # Her topsail is hoisted with its yard square and laid abox only when
                    # the anchor is aweigh (package 37f). Abox while the anchor still holds
                    # her by the bow, it swings her stern and not her head: the schooner
                    # and the cutter were so sheered the wrong way at the breakout, and
                    # cast on the wrong tack or hung till the timeout.
                    self.note(
                        "Let fall! Sheet home! Hoist away the topsail and the mainsail, the "
                        f"main boom steadied over to {_lee_name(self.sign)}. Man the bars; "
                        "heave round!"
                    )
                else:
                    self.swing = YardSwing(yards, targets, self.timing_value("brace_s", 60.0))
                    self.note(
                        f"Let fall! Sheet home! Hoist away the topsails! Brace up the after "
                        f"yards for the {self.tack} tack, the head yards abox. Man the bars; "
                        "heave round!"
                    )
            return
        if self.phase == "heave":
            up_and_down = max(self.anchor.depth_m, 1.0)
            if self._heave(dt, factor, up_and_down, "heave_fathoms_per_s"):
                self.phase = "break_out"
                self.phase_t = 0.0
                self.note("The cable is up and down. Man the jib halliards!")
            return
        if self.phase == "break_out":
            if self.phase_t >= self.timing_value("break_out_s", 60.0) * factor:
                self.anchor.state = AnchorState.AWEIGH
                end_lying_to(ship)  # weighing, she is hove to no longer (package 37f)
                self.anchor.heaving = False
                self.anchor.taut = False
                self.anchor.dragging = False
                self.anchor.cable_load_kn = 0.0
                self.anchor.holding_kn = 0.0
                self.hoist_s = units.m_to_fathoms(self.anchor.depth_m) / max(
                    self.timing_value("hoist_fathoms_per_s", 0.2), 0.01
                )
                self.anchor_t = 0.0
                self.anchor_phase = "hoist"
                ship.note(
                    "notable",
                    "ship.aweigh",
                    f"{_cap(self.anchor.name)} is aweigh.",
                    ship.name,
                    {"anchor": self.anchor.to_dict()},
                )
                # the jib hoisted and the helm a-lee for the stern-board (Luce)
                _set_fore_and_aft(ship, _jib(ship), self.tack)
                self.fore_and_aft = len(_masts_with_yards(ship)) < 2
                if self.fore_and_aft:
                    # a fore-and-after casts by her jib: its sheet held to windward of the
                    # tack she is to cast on, aback, which pays her head off (Luce 1884,
                    # ch. XXXIV, 'Sloops': "trim the jib sheet to windward"); sheeted to
                    # leeward, as it was, it did nothing for her head to wind. And her
                    # topsail yard abox now that she is free to turn.
                    sheets_to(ship, [sl for sl in _jib(ship) if sl.is_set], self.tack, None)
                    head, _after = head_and_after_yards(ship)
                    self.swing = YardSwing(
                        head,
                        [-self.sign * y.brace_limit for y in head],
                        self.timing_value("abox_s", 20.0),
                    )
                dyn.helm_mode = HelmMode.RUDDER
                dyn.target_rudder = self.sign * units.deg_to_rad(15.0)
                dyn.steady = False
                self.phase = "cast"
                self.phase_t = 0.0
                self.note(
                    "Let go the downhauls, hoist away the jib, its sheet to windward! The "
                    "topsail yard abox. Helm a-lee for the stern-board."
                    if self.fore_and_aft
                    else "Let go the downhauls, hoist away the jib! Helm a-lee for the stern-board."
                )
            return
        if self.phase in ("cast", "under_way"):
            # the anchor hove up, catted and fished meanwhile
            self.anchor_t += dt
            if self.anchor_phase == "hoist" and self.anchor_t >= self.hoist_s * factor:
                self.anchor.scope_m = 0.0
                self.anchor.ground_x = self.anchor.ground_y = None
                self.anchor_phase = "cat_and_fish"
                self.anchor_t = 0.0
                self.note(
                    f"{_cap(self.anchor.name)} up to the bows; avast heaving, pawl the capstan. "
                    f"Hook the cat."
                )
            elif (
                self.anchor_phase == "cat_and_fish"
                and self.anchor_t >= self.timing_value("cat_and_fish_s", 300.0) * factor
            ):
                self.anchor.state = AnchorState.STOWED
                self.anchor_phase = "done"
            if self.phase == "cast":
                rel = units.wrap_pi(float(wind.direction_from) - float(dyn.heading))
                side = "starboard" if rel > 0 else "larboard"
                off = units.rad_to_points(abs(rel))
                if self.fore_and_aft:
                    # her helm tended as she casts: a-lee while she drops astern, which
                    # throws her head off, and put up as soon as she gathers headway
                    self._sheer_helm()
                    boom = units.deg_to_rad(self.timing_value("cast_boom_deg", 30.0))
                    if not self.main_eased and side == self.tack and abs(rel) > boom:
                        # the wind now abaft the boom's own angle on the bow she is cast
                        # on, the mainsail would fill and hold her head up: its sheet is
                        # eased right off till she has paid off
                        self.main_eased = True
                        ease_off_sheets(ship, [sl for sl in _boom_mainsails(ship) if sl.is_set])
                cast = off >= self.timing_value("cast_points", 7.0) and side == self.tack
                how = "She has paid off"
                if not cast and off >= self.timing_value("cast_points", 7.0):
                    # cast the other way, plainly: she is got under way on the tack she
                    # has taken, and the line says so (never the tack wanted, in silence)
                    cast = True
                    how = (
                        f"She would not cast on the {self.tack} tack: she has paid off on "
                        f"the {side}"
                    )
                    self.tack = side
                    self.sign = 1.0 if side == "starboard" else -1.0
                if not cast and self.phase_t >= self.timing_value("cast_timeout_s", 420.0):
                    # Package 37f: "paid off" is never said on a timeout. At cast_timeout_s
                    # she is taken as she lies: paid off four points or more on the tack
                    # wanted, she has cast; as far on the other, she has cast the wrong
                    # way and is got under way on that tack, and the line says so; hanging
                    # nearer the wind than that she is given till cast_give_up_s, and then
                    # the evolution fails in words, the anchor aweigh.
                    enough = self.timing_value("cast_enough_points", 4.0)
                    if off >= enough and side == self.tack:
                        cast = True
                        how = f"She has paid off {_points_off_words(abs(rel))} and no further"
                    elif off >= enough:
                        cast = True
                        how = (
                            f"She would not cast on the {self.tack} tack: she has paid off on "
                            f"the {side}"
                        )
                        self.tack = side
                        self.sign = 1.0 if side == "starboard" else -1.0
                    elif self.phase_t >= self.timing_value("cast_give_up_s", 900.0):
                        dyn.target_rudder = 0.0
                        self.fail(
                            f"she hangs {_points_off_words(abs(rel))} from the wind and will "
                            f"not cast, {self.anchor.name} aweigh; let go again, or cast her "
                            "by hand with the jib sheet to windward and the helm"
                        )
                        return
                if cast:
                    self.cast_done = True
                    head, after = head_and_after_yards(ship)
                    if self.fore_and_aft:
                        # let draw: the jib's sheet shifted to leeward and the main sheet
                        # hauled aft, both for the wind she now has
                        fore_aft = [sl for sl in _jib(ship) + _boom_mainsails(ship) if sl.is_set]
                        draw_sheets(ship, fore_aft, _lee_name(self.sign), abs(rel))
                    # the head yards braced round for the tack (and the after yards with
                    # them, if she has cast the other way from the one they were braced for)
                    self.swing = YardSwing(
                        head + after,
                        [self.sign * y.brace_limit for y in head + after],
                        self.timing_value("brace_s", 60.0),
                    )
                    _set_fore_and_aft(ship, after_gaff_sails_all(ship), self.tack)
                    # the course steered once she has cast: the pilot's, unless it lies
                    # closer to the wind than she will sail, when she is kept full and by
                    # (a helm held to a course she cannot lie pinches her into irons)
                    closest = close_hauled_true_angle(ship) + 0.5 * POINT
                    if self.course is not None and (
                        abs(units.wrap_pi(self.course - float(wind.direction_from))) >= closest
                    ):
                        dyn.helm_mode = HelmMode.HEADING
                        dyn.target_heading = units.wrap_2pi(self.course)
                    else:
                        dyn.helm_mode = HelmMode.FULL_AND_BY
                        if self.course is not None:
                            self.course_not_laid = self.course
                            self.pilot_course = False
                            self.course = None
                    dyn.steady = False
                    self.phase = "under_way"
                    self.phase_t = 0.0
                    self.note(
                        f"{how}; right the helm, draw the jib, haul aft the main sheet, brace "
                        "round the topsail yard."
                        if self.fore_and_aft
                        else f"{how}; right the helm, brace round the head yards, set the spanker."
                    )
                return
            if self.anchor_phase == "done" and (self.swing is None or self.swing.done):
                self.finish()

    # what the work was at, for a belay's line (package 37k)
    _DOING = {
        "rig_capstan": "the capstan rigging",
        "heave_short": "heaving short",
        "loose": "loosing sail",
        "heave": "heaving in",
        "break_out": "breaking the anchor out",
        "cast": "casting",
        "under_way": "under way",
    }

    def left_words(self) -> str | None:
        """'the helm and the yards left as they stand, casting; the best bower aweigh and
        hanging at the bows, to be let go again or catted and fished' (package 37k: in
        game 10 a belay of getting under way left the anchor aweigh and said nothing of
        it, and every order to let it go was refused)."""
        doing = self._DOING.get(self.phase)
        head = "the helm and the yards left as they stand" + (f", {doing}" if doing else "")
        if self.anchor is None:
            return head
        return f"{head}; {anchor_left_words(self.anchor)}"

    def words(self) -> dict[str, Any]:
        d = super().words()
        if self.course is not None:
            how = f"steering {units.format_heading(self.course)}"
            how += ", the pilot's course" if self.pilot_course else ""
        else:
            how = "full and by"
            if self.course_not_laid is not None:
                how += (
                    f" ({units.format_heading(self.course_not_laid)} lying too near the wind "
                    "to be laid)"
                )
        d.update({"tack": self.tack, "sail_words": self.sails_words, "course_words": how})
        return d

    def data(self) -> dict[str, Any]:
        d = super().data()
        d.update(
            {
                "tack": self.tack,
                "course_deg": None
                if self.course is None
                else round(units.rad_to_deg(self.course), 1),
                "pilot_course": self.pilot_course,
                "sails": self.sails_words,
            }
        )
        if self.anchor is not None:
            d["anchor"] = self.anchor.to_dict()
        return d

    def remaining_s(self) -> float:
        if self.anchor is None:
            return 600.0
        heave = units.m_to_fathoms(max(0.0, self.anchor.scope_m - self.anchor.depth_m)) / max(
            self.timing_value("heave_fathoms_per_s", 0.1), 0.01
        )
        return (
            heave + self.timing_value("loose_s", 240.0) + self.timing_value("cat_and_fish_s", 300.0)
        )


def after_gaff_sails_all(ship: Ship) -> list[Sail]:
    """The driver, set or not: the gaff sail on the aftermost of two or more masts with
    yards (a ship's spanker, a brig's main); nothing on a fore-and-after."""
    with_yards = _masts_with_yards(ship)
    if len(with_yards) < 2:
        return []
    aftermost = min(with_yards, key=lambda m: m.x_m)
    return [
        sl
        for sl in ship.sails.values()
        if sl.cls == "gaff" and not sl.wrecked and ship.mast_of(sl) is aftermost
    ]


def _anchor_bearing(ship: Ship, anchor: Any) -> float | None:
    """The bearing from the ship to an anchor on the ground, radians true."""
    if anchor.ground_x is None or anchor.ground_y is None:
        return None
    d = ship.dyn
    return units.wrap_2pi(math.atan2(anchor.ground_x - d.x, anchor.ground_y - d.y))


class MoorScript(_AnchorScript):
    """Moor with two anchors and the hawse open (data/evolutions/moor.yaml)."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.second: Any = None
        self.phase_t = 0.0
        self.riding_m = 0.0
        self.far_m = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.ship.parts import AnchorState

        if (why := self._no_tackle()) is not None:
            return why
        down = self.tackle.down()
        if not down:
            return "no anchor is down to moor from; come to an anchor first"
        if len([a for a in down if a.kind == "bower"]) >= 2:
            return "she is moored already"
        if self.ship.extra.get("aground"):
            return "she is aground"
        self.anchor = self.tackle.riding_by()
        named = self.params.get("anchor")
        self.second = self.tackle.by_words(named) if named else self.tackle.by_words("second")
        if self.second is None or self.second is self.anchor:
            return "no second anchor is to be had"
        if self.second.state not in (AnchorState.STOWED, AnchorState.READY):
            return f"{self.second.name} is {self.second.state.value}"
        depth = max(self.anchor.depth_m, 1.0)
        self.riding_m = _scope_wanted(self.ship, self.anchor, depth, None)
        whole = units.fathoms_to_m(self.anchor.cable_fathoms)
        self.far_m = min(2.0 * self.riding_m, whole - units.fathoms_to_m(5.0))
        if self.far_m <= self.anchor.scope_m + 1e-6:
            out = _fathoms_words(self.anchor.scope_fathoms)
            return f"{self.anchor.name} has {out} out already; there is no cable to moor with"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "veer"
        self.phase_t = 0.0

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        if self.phase == "veer":
            if self._veer(dt, factor, self.far_m, "veer_fathoms_per_s"):
                self.phase = "let_go"
                self.phase_t = 0.0
                self.note(
                    f"Veered to {_fathoms_words(self.anchor.scope_fathoms)}; stand clear of "
                    f"{self.second.name}'s cable!"
                )
            return
        if self.phase == "let_go":
            if self.phase_t >= self.timing_value("stand_clear_s", 15.0) * factor:
                depth = _water_depth(ship)
                if depth is None:
                    self.fail("no bottom here to let go the second anchor in")
                    return
                _let_go(ship, self.second, depth)
                ship.note(
                    "notable",
                    "ship.anchored",
                    f"{_cap(self.second.name)} let go in {_depth_words(depth)}, the second "
                    f"anchor of the moor.",
                    ship.name,
                    {"anchor": self.second.to_dict()},
                )
                self.phase = "rig_capstan"
                self.phase_t = 0.0
                self.anchor.heaving = True
            return
        if self.phase == "rig_capstan":
            if self.phase_t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "middle"
                self.phase_t = 0.0
                self.note(
                    f"Bring to on {self.anchor.name}'s cable and heave in; veer away on "
                    f"{self.second.name}'s."
                )
            return
        if self.phase == "middle":
            first_done = self._heave(dt, factor, self.riding_m, "heave_fathoms_per_s")
            rate = units.fathoms_to_m(self.timing_value("veer_fathoms_per_s", 1.0)) / max(
                factor, 1e-9
            )
            limit = min(self.riding_m, units.fathoms_to_m(self.second.cable_fathoms))
            self.second.scope_m = min(limit, self.second.scope_m + rate * dt)
            if first_done and self.second.scope_m >= limit - 1e-6:
                self.anchor.heaving = False
                self.second.brought_up = True  # moored: the moor's own line says how she lies
                self.finish()

    def words(self) -> dict[str, Any]:
        d = super().words()
        ship = self.ship
        b1 = _anchor_bearing(ship, self.anchor) if self.anchor is not None else None
        b2 = _anchor_bearing(ship, self.second) if self.second is not None else None
        wind_from = self.wind.direction_from if self.wind is not None else float(ship.dyn.heading)
        d.update(
            {
                "second": self.second.name if self.second is not None else "the second anchor",
                "first_point": units.point_name(b1) if b1 is not None else "one hand",
                "second_point": units.point_name(b2) if b2 is not None else "the other",
                "open_point": units.point_name(wind_from),
                "fathoms": _fathoms_words(units.m_to_fathoms(self.riding_m)),
            }
        )
        return d

    def remaining_s(self) -> float:
        return 1200.0 if self.phase != "middle" else 600.0


class UnmoorScript(_AnchorScript):
    """Unmoor: the lee anchor hove up first, to single anchor (data/evolutions/unmoor.yaml)."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.second: Any = None  # the anchor she rides by when it is done
        self.phase_t = 0.0
        self.hoist_s = 0.0
        self.riding_m = 0.0

    def check(self, words: dict[str, Any]) -> str | None:
        if (why := self._no_tackle()) is not None:
            return why
        down = [a for a in self.tackle.down() if a.kind == "bower"]
        if len(down) < 2:
            return (
                "she is not moored; she rides at single anchor"
                if self.tackle.down()
                else "no anchor is down"
            )
        if self.ship.extra.get("aground"):
            return "she is aground"
        world = _world_of(self.ship)
        wind_from = (
            float(world.wind.direction_from) if world is not None else float(self.ship.dyn.heading)
        )
        downwind = units.wrap_2pi(wind_from + math.pi)

        def lee_ness(a: Any) -> float:
            b = _anchor_bearing(self.ship, a)
            return abs(units.wrap_pi(b - downwind)) if b is not None else math.pi

        down.sort(key=lee_ness)
        self.anchor, self.second = down[0], down[1]
        self.riding_m = _scope_wanted(self.ship, self.second, max(self.second.depth_m, 1.0), None)
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "rig_capstan"
        self.phase_t = 0.0
        self.anchor.heaving = True

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        if self.phase == "rig_capstan":
            if self.phase_t >= self.timing_value("rig_capstan_s", 180.0) * factor:
                self.phase = "heave"
                self.phase_t = 0.0
                self.note("The messenger passed on the lee cable; heave round!")
            return
        if self.phase == "heave":
            # the weather cable veered to the riding scope as the lee one comes in
            rate = units.fathoms_to_m(self.timing_value("veer_fathoms_per_s", 1.0)) / max(
                factor, 1e-9
            )
            limit = min(self.riding_m, units.fathoms_to_m(self.second.cable_fathoms))
            if self.second.scope_m < limit:
                self.second.scope_m = min(limit, self.second.scope_m + rate * dt)
            if self._heave(dt, factor, max(self.anchor.depth_m, 1.0), "heave_fathoms_per_s"):
                self.phase = "break_out"
                self.phase_t = 0.0
                self.note(f"{_cap(self.anchor.name)}'s cable is up and down.")
            return
        if self.phase == "break_out":
            if self.phase_t >= self.timing_value("break_out_s", 60.0) * factor:
                self.anchor.state = AnchorState.AWEIGH
                end_lying_to(ship)  # weighing, she is hove to no longer (package 37f)
                self.anchor.heaving = False
                self.anchor.taut = False
                self.anchor.dragging = False
                self.anchor.cable_load_kn = 0.0
                self.anchor.holding_kn = 0.0
                self.hoist_s = units.m_to_fathoms(self.anchor.depth_m) / max(
                    self.timing_value("hoist_fathoms_per_s", 0.2), 0.01
                )
                ship.note(
                    "notable",
                    "ship.aweigh",
                    f"{_cap(self.anchor.name)} is aweigh.",
                    ship.name,
                    {"anchor": self.anchor.to_dict()},
                )
                self.phase = "hoist"
                self.phase_t = 0.0
            return
        if self.phase == "hoist":
            if self.phase_t >= self.hoist_s * factor:
                self.anchor.scope_m = 0.0
                self.anchor.ground_x = self.anchor.ground_y = None
                self.phase = "cat_and_fish"
                self.phase_t = 0.0
                self.note(f"{_cap(self.anchor.name)} up to the bows; hook the cat.")
            return
        if self.phase == "cat_and_fish":
            if self.phase_t >= self.timing_value("cat_and_fish_s", 300.0) * factor:
                self.anchor.state = AnchorState.STOWED
                self.finish()

    def words(self) -> dict[str, Any]:
        d = super().words()
        d["second"] = self.second.name if self.second is not None else "the other anchor"
        d["fathoms"] = _fathoms_words(self.second.scope_fathoms) if self.second is not None else ""
        return d

    def remaining_s(self) -> float:
        return 1500.0 if self.phase in ("rig_capstan", "heave") else 400.0


class LayOutKedgeScript(_AnchorScript):
    """A kedge carried out by the boat and let go (data/evolutions/lay_out_kedge.yaml)."""

    holds_subject = True

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.phase_t = 0.0
        self.out_m = 0.0
        self.pull_s = 0.0
        self.toward = 0.0
        self.boat_name = "the boat"
        self.ports: Any = None

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.ship.parts import AnchorState

        if (why := self._no_tackle()) is not None:
            return why
        self.anchor = next((a for a in self.tackle.anchors if a.kind == "kedge"), None)
        if self.anchor is None:
            return "she carries no kedge"
        if self.anchor.state not in (AnchorState.STOWED, AnchorState.READY):
            return f"the kedge is {self.anchor.state.value}"
        if self.ship.extra.get("aground"):
            return "she is aground"
        world = _world_of(self.ship)
        self.ports = getattr(world, "ports", None)
        boat = self.ports.boat_spec() if self.ports is not None else None
        if boat is None:
            return "she carries no boat to lay it out with"
        if self.ports.boat.away:
            return f"{boat.name} is away"
        self.boat_name = boat.name
        if _water_depth(self.ship) is None:
            return "no bottom here to lay a kedge in"
        toward = self.params.get("toward_deg")
        if toward is not None:
            self.toward = units.wrap_2pi(units.deg_to_rad(float(toward)))
        else:
            self.toward = float(self.ship.dyn.heading)
        fathoms = self.params.get("fathoms")
        whole = units.fathoms_to_m(self.anchor.cable_fathoms)
        self.out_m = (
            min(whole, units.fathoms_to_m(float(fathoms)))
            if fathoms
            else whole * self.timing_value("hawser_fraction", 0.75)
        )
        pace = units.knots_to_ms(self.timing_value("boat_pace_kn", 4.0))
        self.pull_s = self.out_m / max(pace, 0.1)
        return None

    def begin(self, words: dict[str, Any]) -> None:
        from freesail.world.ports import BoatState

        self.phase = "hoist_out"
        self.phase_t = 0.0
        if self.ports is not None:
            boat = self.ports.boat_spec()
            self.ports.boat = BoatState(
                away=True,
                boat_id=boat.id,
                boat_name=boat.name,
                errand="laying out the kedge",
                phase="hoisting out",
                since_tick=0,
            )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        from freesail.ship.parts import AnchorState

        self.t += dt
        self.phase_t += dt
        self.wind = wind
        ship = self.ship
        if self.phase == "hoist_out":
            if self.phase_t >= self.timing_value("hoist_out_s", 300.0) * factor:
                self.phase = "sling"
                self.phase_t = 0.0
                if self.ports is not None:
                    self.ports.boat.phase = "the kedge slinging"
            return
        if self.phase == "sling":
            if self.phase_t >= self.timing_value("sling_s", 300.0) * factor:
                self.phase = "pull_out"
                self.phase_t = 0.0
                if self.ports is not None:
                    self.ports.boat.phase = "pulling out with the kedge"
                self.note(
                    f"{_cap(self.boat_name)} away with the kedge over her stern, paying out the "
                    f"hawser toward {units.point_name(self.toward)}."
                )
            return
        if self.phase == "pull_out":
            if self.phase_t >= self.pull_s:
                depth = _water_depth(ship)
                if depth is None:
                    self.fail("no bottom to let the kedge go in")
                    return
                hx, hy = _hawse(ship)
                ex, ey = units.heading_vector(self.toward)
                self.anchor.state = AnchorState.DOWN
                self.anchor.ground_x, self.anchor.ground_y = (
                    hx + ex * self.out_m,
                    hy + ey * self.out_m,
                )
                self.anchor.depth_m = depth
                self.anchor.scope_m = self.out_m
                self.anchor.bottom = str(ship.extra.get("bottom", "") or "")
                self.anchor.taut = False
                self.anchor.dragging = False
                self.anchor.cable_load_kn = 0.0
                ship.note(
                    "notable",
                    "ship.anchored",
                    f"The kedge let go from {self.boat_name} "
                    f"{_fathoms_words(units.m_to_fathoms(self.out_m))} to the "
                    f"{units.point_name(self.toward)}.",
                    ship.name,
                    {"anchor": self.anchor.to_dict()},
                )
                self.phase = "pull_back"
                self.phase_t = 0.0
                if self.ports is not None:
                    self.ports.boat.phase = "pulling back"
            return
        if self.phase == "pull_back":
            if self.phase_t >= self.pull_s:
                self.phase = "hoist_in"
                self.phase_t = 0.0
                if self.ports is not None:
                    self.ports.boat.phase = "alongside, hoisting in"
            return
        if self.phase == "hoist_in":
            if self.phase_t >= self.timing_value("hoist_in_s", 300.0) * factor:
                if self.ports is not None:
                    from freesail.world.ports import BoatState

                    self.ports.boat = BoatState(
                        boat_id=self.ports.boat.boat_id, boat_name=self.boat_name
                    )
                self.finish()

    def words(self) -> dict[str, Any]:
        d = super().words()
        d.update(
            {
                "boat": self.boat_name,
                "fathoms": _fathoms_words(units.m_to_fathoms(self.out_m)),
                "point": units.point_name(self.toward),
            }
        )
        return d

    def remaining_s(self) -> float:
        return max(60.0, 2.0 * self.pull_s)


class SendBoatScript(Script):
    """The boat sent ashore and back (data/evolutions/send_boat.yaml): a passage by
    distance at a boat's pace; what she does ashore and brings back is the port's
    (`freesail.world.ports.Ports.boat_phase`). Holds the boat and not the ship."""

    holds_subject = False

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.phase_t = 0.0
        self.pull_s = 0.0
        self.ashore_s = 0.0
        self.boat_name = "the boat"
        self.ports: Any = None

    def holds(self) -> set[str]:
        return {"the boat"}

    def check(self, words: dict[str, Any]) -> str | None:
        world = _world_of(self.ship)
        self.ports = getattr(world, "ports", None)
        if self.ports is None:
            return "there is no port here to send her to"
        port = self.ports.ports.get(str(self.params.get("port") or ""))
        if port is None:
            return "no port is named for the boat to go to"
        boat = self.ports.boat_spec()
        if boat is None:
            return "she carries no boat"
        self.boat_name = boat.name
        from freesail.world.ports import BOAT_ASHORE_S, LIGHTER_S_PER_TON

        distance = self.ports.to_shore_m(port)
        pace = units.knots_to_ms(self.timing_value("boat_pace_kn", 4.0))
        self.pull_s = distance / max(pace, 0.1)
        errand = str(self.params.get("errand") or "prices")
        # goods go by the port's lighter while the boat is at the quay: so many tons
        tons = sum(
            float(item.get("tons", 0.0))
            for item in self.ports.boat.carrying
            if item.get("kind") in ("purchase", "sale")
        )
        self.ashore_s = float(BOAT_ASHORE_S.get(errand, 1800)) + tons * LIGHTER_S_PER_TON
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.phase = "hoist_out"
        self.phase_t = 0.0

    def _say(self, phase: str) -> None:
        if self.ports is None:
            return
        for severity, kind, text, data in self.ports.boat_phase(phase):
            self.ship.note(severity.value, kind, text, self.ship.name, data)

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        self.phase_t += dt
        if self.phase == "hoist_out":
            if self.phase_t >= self.timing_value("hoist_out_s", 300.0) * factor:
                self.phase = "pull_out"
                self.phase_t = 0.0
                self._say("away")
            return
        if self.phase == "pull_out":
            if self.phase_t >= self.pull_s:
                self.phase = "ashore"
                self.phase_t = 0.0
                self._say("ashore")
            return
        if self.phase == "ashore":
            if self.phase_t >= self.ashore_s:
                self.phase = "pull_back"
                self.phase_t = 0.0
                self._say("returning")
            return
        if self.phase == "pull_back":
            if self.phase_t >= self.pull_s:
                self.phase = "hoist_in"
                self.phase_t = 0.0
                if self.ports is not None:
                    self.ports.boat.phase = "alongside, hoisting in"
            return
        if self.phase == "hoist_in":
            if self.phase_t >= self.timing_value("hoist_in_s", 300.0) * factor:
                self._say("alongside")
                self.finish()

    def words(self) -> dict[str, Any]:
        return {"boat": self.boat_name, "boat_cap": _cap(self.boat_name)}

    def remaining_s(self) -> float:
        left = {
            "hoist_out": 2 * self.pull_s + self.ashore_s + 600.0,
            "pull_out": self.pull_s + self.ashore_s + 300.0 + self.pull_s,
            "ashore": self.ashore_s + self.pull_s + 300.0,
            "pull_back": self.pull_s + 300.0,
            "hoist_in": 300.0,
        }
        return max(0.0, left.get(self.phase, 600.0) - self.phase_t)


SCRIPTS: dict[str, type[Script]] = {
    "tack": TackScript,
    "trim_sheet": TrimSheetScript,
    "wear": WearScript,
    "heave_to": HeaveToScript,
    "fill_away": FillAwayScript,
    "send_down": SendDownScript,
    "sway_up": SwayUpScript,
    "unbend": UnbendScript,
    "bend": BendScript,
    "shift": ShiftScript,
    "clear_wreck": ClearWreckScript,
    "shift_spar": ShiftSparScript,
    "reeve": ReeveScript,
    "loose_to_dry": LooseToDryScript,
    "furl_all": FurlAllScript,
    "boxhaul": BoxHaulScript,
    "lie_a_try": LieATryScript,
    "scud": ScudScript,
    "back_and_fill": BackAndFillScript,
    # the ground tackle (package 34)
    "come_to_anchor": ComeToAnchorScript,
    "let_go_anchor": LetGoAnchorScript,
    "veer_cable": VeerCableScript,
    "heave_short": HeaveShortScript,
    "heave_in": HeaveInScript,
    "weigh_anchor": WeighAnchorScript,
    "cat_and_fish": CatAndFishScript,
    "back_anchor": BackAnchorScript,
    # the port (package 35)
    "get_under_way": GetUnderWayScript,
    "moor": MoorScript,
    "unmoor": UnmoorScript,
    "lay_out_kedge": LayOutKedgeScript,
    "send_boat": SendBoatScript,
}
