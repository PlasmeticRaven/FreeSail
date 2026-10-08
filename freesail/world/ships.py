"""Other sail at far detail (spec M5 §25; the proposal's §5.2; package 35 built the
smallest honest form for the pilot cutter, package 36 the dozen ships, their plans,
their descriptions and the level-of-detail switch).

A **vessel** is a hull from one of the four ship files (the frigate, the schooner, the
cutter, the brig in her two descriptions: the brig-sloop of the Navy and the merchant brig
of the trade, one file), a nation whose colours she wears, a captain with a **goal** (trade
this route, patrol this station, run home, carry the mail, carry a letter to the ship) and
a **plan**: the legs the goal makes, each a mark to steer for, and a speed from the wind by
a **polar drawn once from her file** (`polar_of`: the sails model of `physics/sails.py`
balanced against the hull's resistance at each angle off the wind, the yards and sheets
trimmed as `trim sails` trims them; a knot of the measured polars of
`docs/dev/TuningNotes.md`, "Where the four ships stand"), with the tide's stream of
package 34 added over the ground. She is moved **at the roll-up's cadence**, once a game
minute, and no oftener (truth 67: the same wind and tide as the player; §30: the pace),
and her sail state is a word from her plan and the wind (under plain sail, under reefed
topsails, lying to) for the lookout's description and nothing more. A ship whose course
lies closer to the wind than her polar allows beats for it, close-hauled on the tack
that points nearer the mark until she can lay it.

**The level-of-detail switch** (§25): within `NEAR_DETAIL_NM` of the player she is
promoted to a near-detail object, ticked every second with a heading that swings at a
rate instead of snapping and a keep-course captain who obeys her plan and no more; beyond
`NEAR_DEMOTE_NM` she goes back to far detail. The viewer draws her sails from her state
when it draws her at all (the captain's chart draws the lookout's sighting, never her).
The crewed promotion (the full part-and-crew model) and the rules-based captain who
fights or evades are milestone 6's; `Vessel.promote` is their seam.

What the ship models of her is what the lookout can see (`freesail.world.lookout`): a
sail at the horizon distance her rig's height and the eye give, hailed by a bearing first
("Sail ho!"), then as she nears what the tops make out at the period's distances: her
rig at `RIG_MADE_OUT_NM` (Luce 1866 ch. XXXIII, 'Chasing': "the angle subtended by the
masts"), her colours or none at `COLOURS_MADE_OUT_NM` (Falconer 1780, COLOURS: "the flags
or banners which distinguish the ships of different nations"), what she is at
`MADE_OUT_NM`; a glass sent aloft (`make her out`) reaches `GLASS_FACTOR` further. The
lookout's distance by estimation applies to her as to the land, drawn from a stream of
her own, `sail`; the ships' own draws (a dull sailer, a smart one) come from the `ships`
stream, so a sail on the sea never moves the land's draws and the pinned passages' ticks.

**The pilot cutter** (package 35; spec M5 §23) is the first vessel and is built on this
machinery: 32b's cutter, which comes off from the port when a ship is in the pilot's
cruising ground, closes her, lies to under her lee while the pilot boards, and goes back
(`freesail.world.ports.Ports`). Nothing here is special to any ship: every vessel is a
hull from a file, her polar drawn from it.
"""

from __future__ import annotations

import functools
import math
import random
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.world.chart import Feature, Sighting
from freesail.world.geo import Position, bearing_and_distance, horizon_nm

__all__ = [
    "COLOURS_MADE_OUT_NM",
    "DESCRIPTIONS",
    "GLASS_FACTOR",
    "HAIL_NM",
    "LYING_TO_KN",
    "MADE_OUT_NM",
    "NEAR_DEMOTE_NM",
    "NEAR_DETAIL_NM",
    "POLAR_ANGLES_DEG",
    "POLAR_WINDS_KN",
    "REEFED_FACTOR",
    "RIG_MADE_OUT_NM",
    "VESSEL_TICK_S",
    "Polar",
    "Vessel",
    "Vessels",
    "polar_of",
    "rig_height_m",
    "vessel_from_spec",
]

# A vessel at far detail is moved once a game minute, as the lookout looks (judgement:
# a brig at six knots moves a cable in a minute, which is the sighting's precision; spec
# M5 §30, the roll-up's cadence).
VESSEL_TICK_S = 60
# She has steerage way in the lightest air that moves her (judgement).
VESSEL_MIN_SPEED_KN = 1.0
# Within this a sail's rig is made out ("a brig"): the angle subtended by her masts is
# what the glass measures in a chase (Luce 1866 ch. XXXIII, 'Chasing'), and three masts
# or two are told from the tops at four miles by day (judgement on the eye's power from a
# frigate's masthead; the night's limit is the land's, `chart.NIGHT_LAND_NM`).
RIG_MADE_OUT_NM = 4.0
# Within this her colours are made out (Falconer 1780, COLOURS), or their want ("a
# stranger, her colours not made out"): a flag of a few yards read at two miles by a
# glass (judgement).
COLOURS_MADE_OUT_NM = 2.0
# Within this what she is and whose ("a merchant brig, deep laden"; "the Falmouth pilot's
# cutter, her number on her mainsail"): judgement.
MADE_OUT_NM = 1.5
# A glass sent aloft (`make her out`) makes out at half as far again what the naked eye
# makes out (judgement: the period's day glass against the eye).
GLASS_FACTOR = 1.5
# Within hail: four cables, the pilot cutter's hailing distance (`ports.PILOT_HAIL_WITHIN_M`).
HAIL_NM = 0.4
# A vessel making for the ship closes to this part of the distance asked (judgement: a
# cutter rounding to under a frigate's lee comes a cable and a half when two were named).
ARRIVE_FRACTION = 0.75
# Under reefed topsails with the courses in she makes this part of her plain-sail speed
# (judgement: the starter book's "shorten sail for weather" at thirty knots, the loss a
# reef and the courses cost); lying to she drifts to leeward at a knot (truth 28: lying a
# try under a knot and a half; judgement at a knot for a ship hove to under a topsail).
REEFED_FACTOR = 0.7
REEF_OVER_KN = 30.0
LYING_TO_KN = 1.0
LIE_TO_OVER_KN = 45.0
# The level-of-detail switch (spec M5 §25): promoted within two miles of the player, the
# range at which the sighting's words are hers and not "a sail" (`COLOURS_MADE_OUT_NM`),
# demoted beyond three (judgement; a stated range, hysteresis so she does not flicker).
NEAR_DETAIL_NM = 2.0
NEAR_DEMOTE_NM = 3.0
# A near-detail vessel swings her head at this rate instead of snapping to her course
# (judgement: the brig's 3 degrees a second hard over in the turning table, a plan's
# alteration gentler; docs/dev/TuningNotes.md, "Where the four ships stand").
NEAR_TURN_DEG_S = 1.0
# The polar's grid: the angles off the true wind and the wind speeds the file is balanced
# at; between them linear (judgement: the truths' polars are read every ten degrees).
POLAR_ANGLES_DEG = tuple(range(40, 181, 10))
POLAR_WINDS_KN = (8.0, 15.0, 25.0)
# Beating for a mark she holds her tack until she can lay the mark, and goes about when
# the mark has drawn to the other bow by this part of her beating angle (judgement: a
# pilot cutter beating up to a ship under way must go about as the ship crosses her,
# which truth 70's Brest cutter did not, and held her tack while the schooner passed to
# windward and away).
BEAT_TACK_FRACTION = 0.5
# Ships of one class sail differently by their trim and their age: a dull sailer makes
# this part of her file's polar at least, a smart one all of it, drawn once from the
# `ships` stream (judgement).
SAILING_FACTOR_MIN = 0.85

# A pilot's boat under oars and a lugsail (the Scilly gig, the Roscoff pilots' boat:
# `pilot.vessel` in a port's file, package 35b's; read here at the lead's word, 2026-10-02):
# her masthead a few metres (a thirty-foot gig's lugsail yard: judgement), so that she is
# not seen at the horizon a cutter's rig gives but within `BOAT_SEEN_NM` by day (a boat's
# sail from a masthead, a mile or two: judgement), and her pace under oars and sail the
# boat's of `ports.BOAT_PACE_KN`, four knots, whatever the wind (judgement, as there).
BOAT_MASTHEAD_M = 5.0
BOAT_SEEN_NM = 2.0
BOAT_PACE_KN = 4.0

# The descriptions a scenario may give a far-detail ship: her file, her rig's word (what
# the tops make out at four miles), and what she is when made out (spec M5 §25: the
# brig-sloop of the Navy and the merchant brig of the trade, one file, two descriptions).
DESCRIPTIONS: dict[str, dict[str, str]] = {
    "frigate": {
        "file": "data/ships/frigate-36.yaml",
        "rig": "a ship",
        "what": "a frigate",
    },
    "schooner": {
        "file": "data/ships/topsail-schooner.yaml",
        "rig": "a schooner",
        "what": "a topsail schooner",
    },
    "cutter": {"file": "data/ships/cutter.yaml", "rig": "a cutter", "what": "a cutter"},
    "brig-sloop": {
        "file": "data/ships/brig.yaml",
        "rig": "a brig",
        "what": "a brig-sloop of war, sixteen ports a side",
    },
    "merchant brig": {
        "file": "data/ships/brig.yaml",
        "rig": "a brig",
        "what": "a merchant brig, deep laden",
    },
}
_DESCRIPTION_WORDS = {
    "a frigate": "frigate",
    "frigate": "frigate",
    "a ship": "frigate",
    "a schooner": "schooner",
    "schooner": "schooner",
    "a topsail schooner": "schooner",
    "topsail schooner": "schooner",
    "a cutter": "cutter",
    "cutter": "cutter",
    "a brig": "merchant brig",
    "brig": "merchant brig",
    "a merchant brig": "merchant brig",
    "merchant brig": "merchant brig",
    "a merchantman": "merchant brig",
    "a brig sloop": "brig-sloop",
    "brig sloop": "brig-sloop",
    "a brig-sloop": "brig-sloop",
    "brig-sloop": "brig-sloop",
    "a sloop of war": "brig-sloop",
    "the navy's brig": "brig-sloop",
}


def description_key(words: str) -> str | None:
    """The description a scenario's words name ('a merchant brig', 'brig-sloop'); None
    for words that name none."""
    key = " ".join(str(words).lower().replace("_", " ").split())
    if key in DESCRIPTIONS:
        return key
    return _DESCRIPTION_WORDS.get(key)


@functools.lru_cache(maxsize=8)
def file_descriptions(ship_file: str) -> dict[str, dict[str, str]]:
    """The descriptions a ship file carries of itself (`ship.descriptions`, written by
    `tools/gen_ships.py`: the brig's two), each {rig, what, note}; empty for a file
    without them. The file is the source and `DESCRIPTIONS` the index."""
    import yaml

    try:
        doc = yaml.safe_load(open(ship_file, encoding="utf-8")) or {}
    except OSError:
        return {}
    found = (doc.get("ship") or {}).get("descriptions") or {}
    return {str(k): {kk: str(vv) for kk, vv in (v or {}).items()} for k, v in found.items()}


def description(key: str) -> dict[str, str]:
    """A description by its key: the index's entry with the ship file's own words for
    her rig and what she is where the file gives them."""
    d = dict(DESCRIPTIONS[key])
    own = file_descriptions(d["file"]).get(key)
    if own:
        d["rig"] = own.get("rig") or d["rig"]
        d["what"] = own.get("what") or d["what"]
    return d


@functools.lru_cache(maxsize=8)
def rig_height_m(ship_file: str) -> float:
    """The height of a vessel's masthead above the water from her ship file, which
    decides her horizon (truth 67): the deck's height plus the tallest chain of masts."""
    from freesail.ship.graph import Ship
    from freesail.ship.loader import load_spec
    from freesail.world.lookout import height_of_eye

    try:
        return float(height_of_eye(Ship(load_spec(ship_file))))
    except Exception:  # a file not found or not a rig: a small vessel's masthead (judgement)
        return 15.0


# ---------------------------------------------------------------------------
# The polar, drawn once from the file
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Polar:
    """A ship's speed through the water by the angle off the true wind and the wind's
    speed, under plain sail, as her file gives it: a table on `POLAR_ANGLES_DEG` by
    `POLAR_WINDS_KN`, knots; and the closest angle she holds way at."""

    angles_deg: tuple[int, ...]
    winds_kn: tuple[float, ...]
    speeds_kn: tuple[tuple[float, ...], ...]  # [wind][angle]
    closest_deg: float  # the least angle off the wind with a knot of way in 15 knots

    def speed_kn(self, off_wind_deg: float, wind_kn: float) -> float:
        off = min(180.0, abs(off_wind_deg))
        if off < self.angles_deg[0]:
            return 0.0
        rows = [self._at_angle(r, off) for r in self.speeds_kn]
        return _interp(self.winds_kn, rows, wind_kn)

    def _at_angle(self, row: tuple[float, ...], off: float) -> float:
        return _interp(self.angles_deg, row, off)

    def beat_deg(self, wind_kn: float) -> float:
        """The angle off the wind she beats at: the polar's best to windward, the speed
        times the cosine of the angle greatest (a cutter with a knot and a half of way
        at the closest angle makes more to windward a point and a half freer; truth 70's
        Brest pilot found it, beating out of the Goulet at a knot and a half)."""
        best, best_vmg = float(self.closest_deg), -1.0
        for a in self.angles_deg:
            if a >= 90:
                break
            vmg = self.speed_kn(float(a), wind_kn) * math.cos(math.radians(a))
            if vmg > best_vmg:
                best, best_vmg = float(a), vmg
        return best


def _interp(xs: Any, ys: Any, x: float) -> float:
    if x <= xs[0]:
        return float(ys[0])
    if x >= xs[-1]:
        return float(ys[-1])
    for i in range(1, len(xs)):
        if x <= xs[i]:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return float(ys[i - 1] + t * (ys[i] - ys[i - 1]))
    return float(ys[-1])


def _rigged_for_plain_sail(ship_file: str) -> Any:
    from freesail.ship.graph import Ship
    from freesail.ship.loader import load_spec
    from freesail.ship.parts import SailState

    ship = Ship(load_spec(ship_file))
    for sid in ship.groups.get("plain sail", []):
        ship.sails[sid].state = SailState.SET
    return ship


def _trim_for(ship: Any, awa: float) -> None:
    """The yards braced and the sheets tended to the apparent wind as `trim sails` does
    (`orders.verbs._trim`: the yard square less the wind's angle beyond the sail class's
    peak, within its limit; `evolutions.trim.wanted_sheet_angle` for the sheets)."""
    from freesail.evolutions.trim import set_sheet_angle, wanted_sheet_angle
    from freesail.physics.sails import SAIL_CLASSES

    for y in ship.spars.values():
        if not y.is_yard:
            continue
        sail = ship.sail_of(y)
        cls = SAIL_CLASSES.get(sail.cls if sail else "square") or SAIL_CLASSES["square"]
        chord = min(max(abs(awa) - cls.peak_alpha, 0.0), math.pi / 2)
        y.brace_angle = min(math.pi / 2 - chord, y.brace_limit)
    for sail in ship.sails.values():
        if sail.is_set and sail.is_fore_and_aft:
            set_sheet_angle(ship, sail, wanted_sheet_angle(sail.cls, awa))


def _balanced_speed_ms(ship: Any, off_wind_deg: float, wind_kn: float) -> float:
    """The speed at which the sails' thrust balances the hull's resistance on this
    heading in this wind, by bisection (no heel, no leeway: the far-detail simplification;
    a knot of the measured polars)."""
    from freesail.physics.hull import resistance
    from freesail.physics.sails import compute_sail_forces
    from freesail.physics.wind import Wind, WindParams

    wind = Wind(WindParams.from_nautical(off_wind_deg, wind_kn, 0.0, 0.0), random.Random(0))
    tw = units.knots_to_ms(wind_kn)
    theta = math.radians(off_wind_deg)
    ship.dyn.heading = 0.0
    lo, hi = 0.0, ship.hull.hull_speed * 1.3
    for _ in range(14):
        u = 0.5 * (lo + hi)
        ship.dyn.u = u
        ship.dyn.speed = u
        ship.dyn.v = 0.0
        awa = math.atan2(math.sin(theta) * tw, math.cos(theta) * tw + u)
        ship.dyn.apparent_wind_angle = awa
        _trim_for(ship, awa)
        forces = compute_sail_forces(ship, wind)
        if forces.thrust_n + resistance(ship.hull, u) > 0.0:
            lo = u
        else:
            hi = u
    return 0.5 * (lo + hi)


@functools.lru_cache(maxsize=8)
def polar_of(ship_file: str) -> Polar:
    """The polar drawn once from a ship file (spec M5 §25): plain sail, the yards and
    sheets trimmed to the wind, the sails' thrust against the hull's resistance at each
    angle and wind of the grid. Pure arithmetic on the file, the same on every machine."""
    ship = _rigged_for_plain_sail(ship_file)
    rows = []
    for wind_kn in POLAR_WINDS_KN:
        rows.append(
            tuple(
                round(units.ms_to_knots(_balanced_speed_ms(ship, a, wind_kn)), 2)
                for a in POLAR_ANGLES_DEG
            )
        )
    mid = rows[POLAR_WINDS_KN.index(15.0)] if 15.0 in POLAR_WINDS_KN else rows[0]
    closest = float(POLAR_ANGLES_DEG[-1])
    for a, kn in zip(POLAR_ANGLES_DEG, mid, strict=True):
        if kn >= 1.0:
            closest = float(a)
            break
    return Polar(tuple(POLAR_ANGLES_DEG), tuple(POLAR_WINDS_KN), tuple(rows), closest)


# ---------------------------------------------------------------------------
# The vessel
# ---------------------------------------------------------------------------


@dataclass
class Vessel:
    """A vessel at far detail: who she is, where she is, and her plan."""

    id: str
    name: str  # as the lookout names her when made out: "the Falmouth pilot's cutter"
    kind: str  # her rig's word when made out at a distance: "a cutter"
    ship_file: str
    nation: str
    position: Position
    heading_deg: float = 0.0
    speed_kn: float = 0.0  # her speed over the water now, knots
    colours: str = ""  # the words of her colours when made out
    flag: str = ""  # the short word of her flag ("the red ensign")
    nation_adjective: str = ""  # "British", for "British colours"
    shows_colours: bool = True  # a King's ship wears them; a merchantman shows them near
    purpose: str = ""  # "standing out from the land", for the hail when her rig is made out
    description: str = ""  # a description's key (DESCRIPTIONS); "" for the pilot's cutter
    what: str = ""  # what she is when made out ("a merchant brig, deep laden")
    goal: str = ""  # the goal in words, for the author and the tests
    # the plan: a list of legs, each ("to", Position, name), ("to_ship", metres),
    # ("lie_to", seconds) or ("home", Position, name); the first is the one in hand, and
    # the vessel is done when the list is empty unless she cycles her route
    plan: list[tuple[Any, ...]] = field(default_factory=list)
    cycle: bool = False
    done: bool = False
    distance_run_m: float = 0.0
    lying_to_s: float = 0.0
    alongside: bool = False  # within hail of the ship, lying under her lee
    sailing_factor: float = 1.0  # a dull sailer or a smart one, drawn once
    sail_state: str = "under plain sail"
    tack: float = 0.0  # the tack she is beating on: +1 starboard, -1 larboard, 0 none
    detail: str = "far"
    letter: Any = None  # a Message she carries for the ship (`carry a letter`)
    hailed: bool = False  # within hail once: the line said
    spoken: bool = False  # within hail at any time: a stranger no more (the book's)
    # a boat under oars and sail (a port's `pilot.vessel`): her own height, the distance
    # she is seen within, and her pace, in place of a ship file's
    boat: bool = False
    height_override_m: float | None = None
    seen_within_nm: float | None = None
    pace_override_kn: float | None = None

    @property
    def height_m(self) -> float:
        if self.height_override_m is not None:
            return self.height_override_m
        return rig_height_m(self.ship_file)

    @classmethod
    def boat_of(cls, port_id: str, spec: dict[str, Any], **kw: Any) -> Vessel:
        """A pilot's boat from a port file's `pilot.vessel` ({kind: a gig, name: the St
        Mary's pilots' gig, under: oars and a lugsail}): sighted within `BOAT_SEEN_NM`,
        pulling at `BOAT_PACE_KN` whatever the wind, "pulling off from the land"."""
        return cls(
            kind=str(spec.get("kind") or "a boat"),
            name=str(spec.get("name") or f"the {port_id} pilots' boat"),
            purpose="pulling off from the land",
            boat=True,
            height_override_m=float(spec.get("height_m", BOAT_MASTHEAD_M)),
            seen_within_nm=float(spec.get("seen_nm", BOAT_SEEN_NM)),
            pace_override_kn=float(spec.get("pace_kn", BOAT_PACE_KN)),
            **kw,
        )

    @property
    def polar(self) -> Polar:
        return polar_of(self.ship_file)

    # -- the plan ------------------------------------------------------------------------

    def _wind_at(self, world: Any) -> tuple[float, float]:
        """(direction from, degrees; speed, m/s): the same wind as the player's (truth
        67): the systems' surface wind at her own place when the systems drive the wind,
        else the world's base wind (the mean, not the gust)."""
        systems = getattr(world, "systems", None)
        if systems is not None and getattr(world, "weather", None) is None and world.origin:
            # her place on the systems' plane by the world's one frame (package 37d: from
            # the player's own position and her offset from it, not by one jump from the
            # scenario's origin, which drifts from the ship's plane with the miles run)
            plane = world.plane_of(self.position) if hasattr(world, "plane_of") else None
            if plane is not None:
                x_km, y_km = plane[0] / 1000.0, plane[1] / 1000.0
            else:
                bearing, dist = bearing_and_distance(world.origin, self.position)
                rad = math.radians(bearing)
                x_km = dist * math.sin(rad) / 1000.0
                y_km = dist * math.cos(rad) / 1000.0
            direction, speed = systems.surface_wind_at(x_km, y_km)
            return math.degrees(direction) % 360.0, float(speed)
        wind = world.wind
        return math.degrees(wind.base_direction) % 360.0, float(wind.base_speed)

    def _state_for(self, wind_kn: float, lying_to: bool) -> str:
        if lying_to or wind_kn > LIE_TO_OVER_KN:
            return "lying to"
        if wind_kn > REEF_OVER_KN:
            return "under reefed topsails"
        return "under plain sail"

    def pace_kn(self, course_deg: float, wind_from_deg: float, wind_kn: float) -> float:
        """Her speed through the water on a course in a wind, by her polar and her
        sail state; nothing closer to the wind than her polar allows."""
        if self.pace_override_kn is not None:
            return self.pace_override_kn  # a boat under oars: her pull, whatever the wind
        off = abs(units.rad_to_deg(units.wrap_pi(math.radians(course_deg - wind_from_deg))))
        kn = self.polar.speed_kn(off, wind_kn) * self.sailing_factor
        if self.sail_state == "under reefed topsails":
            kn *= REEFED_FACTOR
        return max(VESSEL_MIN_SPEED_KN, kn) if off >= self.polar.closest_deg else kn

    def _intercept(self, world: Any, target: Position) -> Position:
        """Where to steer for a ship under way: her position run on at her way over the
        ground for the time it takes to get there at this vessel's own pace (the world's
        own boat knows the world's truth; two passes of the sum are enough). Found on the
        way: a pilot cutter steering for where the ship was, beating, fell astern of a
        schooner crossing her at four knots and never came up with her (truth 70)."""
        east, north = _ship_velocity(world)
        if abs(east) + abs(north) < 0.05:
            return target
        own = max(units.knots_to_ms(max(self.speed_kn, VESSEL_MIN_SPEED_KN)), 0.25)
        # the time to the meeting: |r + v t| = own t, r the ship's offset from here and v
        # her way; the least positive root, else (she cannot be caught) the ship herself
        bearing, distance = bearing_and_distance(self.position, target)
        rx = distance * math.sin(math.radians(bearing))
        ry = distance * math.cos(math.radians(bearing))
        a = east * east + north * north - own * own
        b = 2.0 * (rx * east + ry * north)
        c = rx * rx + ry * ry
        roots = []
        if abs(a) < 1e-9:
            if abs(b) > 1e-9:
                roots.append(-c / b)
        else:
            disc = b * b - 4.0 * a * c
            if disc >= 0.0:
                sq = math.sqrt(disc)
                roots.extend(((-b - sq) / (2.0 * a), (-b + sq) / (2.0 * a)))
        times = [t for t in roots if t > 0.0]
        if not times:
            return target
        t = min(min(times), 3 * 3600.0)  # three hours at most
        return target.advanced(east * t, north * t)

    def _course_for(self, bearing_deg: float, wind_from_deg: float, wind_kn: float) -> float:
        """The course she steers for a mark: the bearing when she can lay it at her
        beating angle or freer, else by the wind at that angle on the tack that points
        nearer, held until she can lay it."""
        if self.pace_override_kn is not None:
            return bearing_deg  # a boat pulls straight for her mark
        beat = self.polar.beat_deg(wind_kn)
        theta = units.rad_to_deg(units.wrap_pi(math.radians(bearing_deg - wind_from_deg)))
        if abs(theta) >= beat:
            self.tack = 0.0
            return bearing_deg
        if self.tack == 0.0:
            self.tack = 1.0 if theta >= 0.0 else -1.0
        elif theta * self.tack < 0.0 and abs(theta) > beat * BEAT_TACK_FRACTION:
            # the mark has drawn to the other bow (a ship under way passing her): about
            self.tack = -self.tack
        return (wind_from_deg + self.tack * beat) % 360.0

    def tick(self, world: Any, dt: float) -> None:
        """Move along the plan for `dt` seconds, by the wind at her and the tide."""
        if self.done or not self.plan:
            self.done = True
            return
        leg = self.plan[0]
        kind = leg[0]
        wind_from, wind_ms = self._wind_at(world)
        wind_kn = units.ms_to_knots(wind_ms)
        self.sail_state = self._state_for(wind_kn, kind == "lie_to")
        if kind == "lie_to":
            self.lying_to_s += dt
            # hove to she drifts to leeward at a knot, as the player does (truth 28)
            self.heading_deg = (wind_from + 90.0) % 360.0
            self.speed_kn = 0.0
            self._drift(world, (wind_from + 180.0) % 360.0, units.knots_to_ms(LYING_TO_KN), dt)
            if self.lying_to_s >= float(leg[1]):
                self.lying_to_s = 0.0
                self.plan.pop(0)
            return
        if kind == "to_ship":
            target = world.position
            if target is None:
                self.plan.pop(0)
                return
            target = self._intercept(world, target)
            # she runs in to a little under the hailing distance asked, so that a ship
            # under way is caught and not followed for ever at exactly that distance
            arrive_m = (float(leg[1]) if len(leg) > 1 else units.CABLE * 2.0) * ARRIVE_FRACTION
        else:
            target = leg[1]
            arrive_m = units.CABLE
        bearing, distance = bearing_and_distance(self.position, target)
        if distance <= arrive_m + 1.0:  # a metre: she stops at the mark
            self._arrived(world, leg)
            return
        if self.sail_state == "lying to":
            self.heading_deg = (wind_from + 90.0) % 360.0
            self.speed_kn = 0.0
            self._drift(world, (wind_from + 180.0) % 360.0, units.knots_to_ms(LYING_TO_KN), dt)
            return
        course = self._course_for(bearing, wind_from, wind_kn)
        if self.detail == "near":
            # the keep-course captain at near detail: her head swings at a rate
            swing = units.rad_to_deg(units.wrap_pi(math.radians(course - self.heading_deg)))
            limit = NEAR_TURN_DEG_S * dt
            course = (self.heading_deg + max(-limit, min(limit, swing))) % 360.0
        self.heading_deg = course
        self.speed_kn = self.pace_kn(course, wind_from, wind_kn)
        step = units.knots_to_ms(self.speed_kn) * dt
        if course == bearing and step >= distance - arrive_m:
            step = max(0.0, distance - arrive_m)
        rad = math.radians(course)
        self.position = self.position.advanced(step * math.sin(rad), step * math.cos(rad))
        self.distance_run_m += step
        self._stream(world, dt)
        if course == bearing and step >= distance - arrive_m:
            self._arrived(world, leg)

    def _drift(self, world: Any, toward_deg: float, ms: float, dt: float) -> None:
        rad = math.radians(toward_deg)
        self.position = self.position.advanced(ms * dt * math.sin(rad), ms * dt * math.cos(rad))
        self._stream(world, dt)

    def _stream(self, world: Any, dt: float) -> None:
        """The tide's stream over the ground (package 34), the same the player feels."""
        tide = getattr(world, "tide", None)
        if tide is None:
            return
        from freesail.world.sights import greenwich_time

        east, north = tide.stream_at(self.position, greenwich_time(world))
        if east or north:
            self.position = self.position.advanced(east * dt, north * dt)

    def _arrived(self, world: Any, leg: tuple[Any, ...]) -> None:
        kind = leg[0]
        self.tack = 0.0
        if self.cycle and kind == "to":
            self.plan.append(self.plan.pop(0))
            return
        self.plan.pop(0)
        if kind == "to_ship" and not self.plan:
            # come up with the ship and nothing after: she lies to under the ship's lee
            # until whoever sent her gives her a plan (the pilot's cutter, `ports.py`)
            self.plan = [("lie_to", math.inf)]
            return
        if kind == "home" or (kind == "to" and not self.plan):
            self.done = True

    # -- the level of detail -------------------------------------------------------------

    def promote(self, near: bool) -> None:
        """Far to near detail and back (spec M5 §25). The crewed promotion (the full
        part-and-crew model) and the rules-based captain who fights or evades are
        milestone 6's; this switch is their seam and does nothing more than the cadence."""
        self.detail = "near" if near else "far"

    # -- what the lookout makes out ------------------------------------------------------

    def made_out(self, distance_m: float, glass: bool = False) -> tuple[int, str]:
        """(the level made out, the words) at this distance: 0 'a sail'; 1 her rig and
        her course; 2 her colours or their want; 3 what she is. A glass aloft reaches
        `GLASS_FACTOR` further at each level."""
        nm = distance_m / units.NAUTICAL_MILE
        reach = GLASS_FACTOR if glass else 1.0
        if nm <= MADE_OUT_NM * reach:
            return 3, self._words(3)
        if nm <= COLOURS_MADE_OUT_NM * reach:
            return 2, self._words(2)
        if nm <= RIG_MADE_OUT_NM * reach:
            return 1, self._words(1)
        return 0, "a sail"

    def course_words(self) -> str:
        if self.sail_state == "lying to":
            return "lying to"
        point = units.point_name(math.radians(self.heading_deg))
        return f"standing to the {_ward(self.heading_deg)} ({point}), {self.sail_state}"

    def colours_words(self) -> str:
        if not self.shows_colours or not self.nation_adjective:
            return "a stranger, her colours not made out"
        flag = f", {self.flag}" if self.flag else ""
        return f"{self.nation_adjective} colours{flag}"

    def words_at(self, level: int) -> str:
        """What is known of her at a level made out (the reading `the strangers`)."""
        return "a sail" if level <= 0 else self._words(min(level, 3))

    def _words(self, level: int) -> str:
        rig = f"{self.kind} {self.purpose}".strip() if self.purpose else self.kind
        if level == 1:
            return f"{rig}, {self.course_words()}"
        if level == 2:
            return f"{rig}, {self.course_words()}; {self.colours_words()}"
        what = self.what or self.name
        return f"{what}, {self.course_words()}; {self.colours_words()}"

    def seen_as_feature(self, distance_m: float) -> Feature:
        """The feature the lookout sees at this distance: 'a sail' beyond
        `RIG_MADE_OUT_NM`, her rig within it, and what she is within `MADE_OUT_NM`."""
        nm = distance_m / units.NAUTICAL_MILE
        if nm <= MADE_OUT_NM:
            name = self.what or self.name
        elif nm <= RIG_MADE_OUT_NM:
            name = f"{self.kind} {self.purpose}".strip() if self.purpose else self.kind
        else:
            name = "a sail"
        return Feature(
            f"sail:{self.id}",
            "sail",
            name,
            self.position.lat_deg,
            self.position.lon_deg,
            modern=self.id,
            height_m=self.height_m,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "description": self.description,
            "nation": self.nation,
            "position": self.position.to_dict(),
            "heading_deg": round(self.heading_deg, 1),
            "speed_kn": round(self.speed_kn, 2),
            "sail_state": self.sail_state,
            "goal": self.goal,
            "plan": [str(leg[0]) for leg in self.plan],
            "detail": self.detail,
            "done": self.done,
            "alongside": self.alongside,
            "hailed": self.hailed,
            "spoken": self.spoken,  # the book's: a sail spoken is a stranger no more
        }


# ---------------------------------------------------------------------------
# A vessel from a scenario's or a world order's words
# ---------------------------------------------------------------------------


def _ward(heading_deg: float) -> str:
    quarter = int(((heading_deg % 360.0) + 22.5) // 45.0) % 8
    return (
        "northward",
        "north-eastward",
        "eastward",
        "south-eastward",
        "southward",
        "south-westward",
        "westward",
        "north-westward",
    )[quarter]


def place_position(world: Any, words: str) -> tuple[Position, str] | None:
    """A place named in a goal: a port by its name (its outer road, where a ship bound
    for it brings up), a feature of the chart by its name, or a position in the log's
    form; None where the chart knows no such place."""
    from freesail.world.geo import parse_position

    text = " ".join(str(words).split())
    ports = getattr(world, "ports", None)
    port = ports.find(text) if ports is not None and ports.ports else None
    if port is not None:
        return port.outer_road.position, port.name
    chart = getattr(world, "chart", None)
    if chart is not None:
        feature = chart.find_feature(text)
        if feature is not None:
            return feature.position, feature.name
    try:
        return parse_position(text), text
    except ValueError:
        return None


def _goal_plan(world: Any, goal: str, start: Position) -> tuple[list[tuple[Any, ...]], bool, str]:
    """The legs a goal's words make: (plan, cycles, the goal's words as kept).

    trading <A> to <B>              to B, to A, and again (trade this route)
    bound from <A> for <B>          to B, and gone in
    patrolling off <place> within <n> miles    a square of four marks about the station
    running home to <place>         to the place, and in
    carrying the mail to <place>    to the place, and in
    carrying a letter to the ship   to the ship, then home where she came from
    """
    import re

    text = " ".join(goal.lower().split())
    m = re.match(r"^(?:trading|trade)\s+(.+?)\s+(?:to|and)\s+(.+)$", text)
    if m:
        a, b = place_position(world, m.group(1)), place_position(world, m.group(2))
        if a is None or b is None:
            raise ValueError(f"the chart knows no such place in '{goal}'")
        return [("to", b[0], b[1]), ("to", a[0], a[1])], True, f"trading {a[1]} to {b[1]}"
    m = re.match(r"^bound\s+(?:from\s+(.+?)\s+)?for\s+(.+)$", text)
    if m:
        b = place_position(world, m.group(2))
        if b is None:
            raise ValueError(f"the chart knows no such place in '{goal}'")
        origin = f"from {m.group(1)} " if m.group(1) else ""
        return [("to", b[0], b[1])], False, f"bound {origin}for {b[1]}"
    m = re.match(
        r"^(?:patrolling|patrol|cruising|cruise)\s+(?:off|on the station off)\s+(.+?)"
        r"(?:\s+within\s+([\d.]+)\s+miles?)?$",
        text,
    )
    if m:
        p = place_position(world, m.group(1))
        if p is None:
            raise ValueError(f"the chart knows no such place in '{goal}'")
        radius_nm = float(m.group(2) or 5.0)
        marks = []
        for bearing in (270.0, 0.0, 90.0, 180.0):  # west, north, east, south of the station
            from freesail.world.geo import destination

            marks.append(("to", destination(p[0], bearing, radius_nm * units.NAUTICAL_MILE), p[1]))
        return marks, True, f"patrolling off {p[1]} within {radius_nm:g} miles"
    m = re.match(r"^(?:running|run)\s+home\s+(?:to|for)\s+(.+)$", text)
    if m:
        p = place_position(world, m.group(1))
        if p is None:
            raise ValueError(f"the chart knows no such place in '{goal}'")
        return [("home", p[0], p[1])], False, f"running home to {p[1]}"
    m = re.match(r"^(?:carrying|carry)\s+the\s+mail\s+(?:to|for)\s+(.+)$", text)
    if m:
        p = place_position(world, m.group(1))
        if p is None:
            raise ValueError(f"the chart knows no such place in '{goal}'")
        return [("home", p[0], p[1])], False, f"carrying the mail to {p[1]}"
    if re.match(r"^(?:carrying|carry)\s+a\s+(?:letter|message|dispatch|despatch)", text):
        return [("to_ship", 2.0 * units.CABLE), ("home", start, "home")], False, goal
    raise ValueError(
        f"'{goal}' is no goal a captain at far detail knows: say trading <A> to <B>, bound "
        f"from <A> for <B>, patrolling off <place> within <n> miles, running home to <place>, "
        f"carrying the mail to <place>, or carrying a letter to the ship."
    )


def vessel_from_spec(world: Any, spec: dict[str, Any], serial: int) -> Vessel:
    """A vessel from a scenario's `ships:` entry or a world order's words: her
    description (one of `DESCRIPTIONS`), her name, her nation, her position and her goal;
    `colours: shown | none` whether she wears them. Her sailing factor is drawn from the
    `ships` stream, so that two brigs of one file are not one brig."""
    key = description_key(str(spec.get("description") or spec.get("kind") or ""))
    if key is None:
        raise ValueError(
            f"'{spec.get('description')}' is no description a far-detail ship takes; say one "
            f"of {', '.join(DESCRIPTIONS)}."
        )
    d = description(key)
    nation_id = str(spec.get("nation") or "britain")
    nation = world.nations.get(nation_id)
    raw = spec.get("position")
    if isinstance(raw, dict):
        position = Position.from_dict(raw)
    elif isinstance(raw, Position):
        position = raw
    else:
        found = place_position(world, str(raw or ""))
        if found is None:
            raise ValueError(f"'{raw}' is no position and no place of the chart")
        position = found[0]
    name = str(spec.get("name") or f"{key} {serial}")
    plan, cycle, goal = _goal_plan(world, str(spec.get("goal") or "bound for Falmouth"), position)
    stream = world.rng.stream("ships")
    factor = SAILING_FACTOR_MIN + (1.0 - SAILING_FACTOR_MIN) * stream.random()
    shows = str(spec.get("colours", "shown")).lower() not in ("none", "no", "false", "hidden")
    vessel = Vessel(
        id=str(spec.get("id") or f"ship-{serial}"),
        name=name,
        kind=d["rig"],
        ship_file=d["file"],
        nation=nation.id,
        position=position,
        colours=nation.colours,
        flag=getattr(nation, "flag", ""),
        nation_adjective=nation.adjective,
        shows_colours=shows,
        description=key,
        what=d["what"],
        goal=goal,
        plan=plan,
        cycle=cycle,
        sailing_factor=round(factor, 3),
    )
    if spec.get("letter") is not None:
        from freesail.world.people import Message

        letter = spec["letter"]
        if isinstance(letter, dict):
            vessel.letter = Message(
                str(letter.get("text") or ""),
                str(letter.get("origin") or name),
                str(letter.get("to") or "captain"),
                carried_by=f"the {d['rig'].removeprefix('a ')} {name}",
            )
        else:
            vessel.letter = Message(
                str(letter), name, carried_by=f"the {d['rig'].removeprefix('a ')} {name}"
            )
    vessel.heading_deg = (
        bearing_and_distance(position, plan[0][1])[0]
        if plan and len(plan[0]) > 1 and isinstance(plan[0][1], Position)
        else 0.0
    )
    return vessel


# ---------------------------------------------------------------------------
# The vessels of one World
# ---------------------------------------------------------------------------


class Vessels:
    """The vessels of one World, ticked once a game minute (`World.tick`; a near-detail
    vessel every second), and what the lookout can see of them."""

    def __init__(self, world: Any = None) -> None:
        self.world = world
        self.vessels: list[Vessel] = []
        self.serial = 0

    def add(self, vessel: Vessel) -> Vessel:
        """A vessel put on the sea; her nation's colours' words from the table when
        whoever made her gave none (the pilot cutter of `ports.py`)."""
        nations = getattr(self.world, "nations", None)
        if nations is not None and not vessel.nation_adjective:
            try:
                nation = nations.get(vessel.nation)
            except KeyError:
                nation = None
            if nation is not None:
                vessel.nation_adjective = nation.adjective
                vessel.flag = getattr(nation, "flag", "")
                vessel.colours = vessel.colours or nation.colours
        self.vessels.append(vessel)
        return vessel

    def get(self, vessel_id: str) -> Vessel | None:
        for v in self.vessels:
            if v.id == vessel_id:
                return v
        return None

    def find(self, words: str) -> Vessel | None:
        """A vessel by her id or her name, the article and the case disregarded."""
        key = " ".join(str(words).lower().split()).removeprefix("the ")
        for v in self.vessels:
            if key in (v.id.lower(), v.name.lower(), v.name.lower().removeprefix("the ")):
                return v
        return None

    def active(self) -> list[Vessel]:
        return [v for v in self.vessels if not v.done]

    def tick(self, world: Any, dt: float = float(VESSEL_TICK_S)) -> list[tuple[Any, ...]]:
        """The minute's move of every far-detail vessel; the second's of a near one
        (`tick_near`). Returns the lines the vessels' own events make (a letter brought
        alongside, a vessel within hail), for the World to record."""
        lines: list[tuple[Any, ...]] = []
        for v in self.vessels:
            if v.done or v.detail == "near":
                continue
            v.tick(world, dt)
        lines.extend(self._promote_and_hail(world))
        self.vessels = [v for v in self.vessels if not v.done]
        return lines

    def tick_near(self, world: Any, dt: float = 1.0) -> list[tuple[Any, ...]]:
        """Every second: the near-detail vessels only."""
        if not any(v.detail == "near" and not v.done for v in self.vessels):
            return []
        for v in self.vessels:
            if v.detail == "near" and not v.done:
                v.tick(world, dt)
        lines = self._promote_and_hail(world)
        self.vessels = [v for v in self.vessels if not v.done]
        return lines

    def _promote_and_hail(self, world: Any) -> list[tuple[Any, ...]]:
        """The level of detail by the distance from the player, and a vessel come within
        hail (a letter she carries comes aboard: the carrier of truth 68)."""
        from freesail.core.events import Severity

        pos = world.position
        if pos is None:
            return []
        lines: list[tuple[Any, ...]] = []
        for v in self.vessels:
            if v.done:
                continue
            _, distance = bearing_and_distance(pos, v.position)
            nm = distance / units.NAUTICAL_MILE
            if v.detail == "far" and nm <= NEAR_DETAIL_NM:
                v.promote(True)
            elif v.detail == "near" and nm > NEAR_DEMOTE_NM:
                v.promote(False)
            if nm <= HAIL_NM and not v.hailed:
                v.hailed = True
                v.spoken = True
                words = v.what or v.name
                if v.letter is not None:
                    v.alongside = True
                    lines.append(
                        (
                            Severity.NOTABLE,
                            "sail.within_hail",
                            f"{_head(words)} is within hail, {v.course_words()}; she has a "
                            f"letter for the ship.",
                            {"id": v.id, "letter": True},
                        )
                    )
                    letter, v.letter = v.letter, None
                    lines.extend(world.people.message_aboard(letter))
                    v.alongside = False
                elif v.description:
                    lines.append(
                        (
                            Severity.NOTABLE,
                            "sail.within_hail",
                            f"{_head(words)} is within hail, {v.course_words()}; "
                            f"{v.colours_words()}.",
                            {"id": v.id, "letter": False},
                        )
                    )
            elif nm > HAIL_NM * 2.0:
                v.hailed = False
        return lines

    def in_sight(
        self, pos: Position, height_of_eye_m: float, visibility_nm: float | None, daylight: str
    ) -> list[Sighting]:
        """The vessels in sight from the masthead: within the horizon her rig's height
        and the eye give (truth 67), within the weather's visibility, by day; at night a
        sail is seen only close aboard, as the land is (`chart.NIGHT_LAND_NM`)."""
        from freesail.world.chart import NIGHT_LAND_NM

        vis_nm = math.inf if visibility_nm is None else float(visibility_nm)
        out: list[Sighting] = []
        for v in self.vessels:
            if v.done:
                continue
            bearing, distance = bearing_and_distance(pos, v.position)
            nm = distance / units.NAUTICAL_MILE
            limit = min(vis_nm, horizon_nm(height_of_eye_m, v.height_m))
            if v.seen_within_nm is not None:
                limit = min(limit, v.seen_within_nm)  # a boat: the eye's limit, not the horizon's
            if daylight != "day":
                limit = min(limit, NIGHT_LAND_NM)
            if nm <= limit:
                out.append(Sighting(v.seen_as_feature(distance), bearing, distance, "sail"))
        out.sort(key=lambda s: s.distance_m)
        return out

    def to_dict(self) -> list[dict[str, Any]]:
        return [v.to_dict() for v in self.vessels]


def _ship_velocity(world: Any) -> tuple[float, float]:
    """The player's ship's way over the ground, metres a second east and north (the
    truth, for the world's own vessels); nothing for a point ship or at anchor."""
    ship = world.ship
    dyn = getattr(ship, "dyn", None)
    if dyn is None or getattr(world, "at_anchor", False):
        return 0.0, 0.0
    try:
        from freesail.physics.integrate import water_velocity

        wx, wy = water_velocity(ship)
    except Exception:  # a ship without the physics' water: her way alone
        wx, wy = 0.0, 0.0
    ex, ey = units.heading_vector(float(dyn.heading))
    u, v = float(getattr(dyn, "u", 0.0)), float(getattr(dyn, "v", 0.0))
    return u * ex + v * ey + wx, u * ey - v * ex + wy


def _head(words: str) -> str:
    return words[:1].upper() + words[1:]
