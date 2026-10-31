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
(`freesail.world.dealings.Dealings`). Nothing here is special to any ship: every vessel is a
hull from a file, her polar drawn from it. Package 37h gives her a leg of her own,
`company`: hailed, the pilot's boat keeps company with the ship at the ship's pace, a
cable and a half off, until she is slow enough for him to board or her captain sends her
away, where before she was left astern by a ship standing in faster than she sailed.
"""

from __future__ import annotations

import functools
import math
import random
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.world.chart import Feature, Sighting
from freesail.world.geo import Position, bearing_and_distance, horizon_nm

# The followed hull's vessel's id (package 84, step 7): the player's ship as a vessel of
# the sea, the far brains' word for her since package 43 and the squadrons', the action's
# and the signals' since (`brains`, `squadrons` and `combat.action` import it from here).
PLAYER_ID = "the ship"

__all__ = [
    "COLOURS_MADE_OUT_NM",
    "COMPANY_CLOSING_KN",
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
# Keeping company (package 37h; the `company` leg): within the distance the leg names she
# goes with the ship at the ship's way over the ground, as a pilot's boat keeps company
# with a ship that has hailed her or that she has hailed; beyond it she closes at the
# ship's pace and this much more (judgement: a pilot cutter was built to be the fastest
# thing in her water, and a gig is towed or pulled alongside by the ship's line when she
# has come up; the far-detail boat is given the pace and not the means).
COMPANY_CLOSING_KN = 2.0

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
    # PROVISIONAL (the owner's ask of 2026-10-25, ahead of package 75): the letter of marque
    # of the schooner's draught, her guns her own file's; the tops make out a schooner
    "privateer schooner": {
        "file": "data/ships/privateer-schooner.yaml",
        "rig": "a schooner",
        "what": "a topsail schooner, pierced for guns",
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
    # package 43b (spec M6 §19): the chasse-marée on the Éclair of 1795 and the smack on the
    # Culloden of 1746, the coaster and the fisherman of the world's business
    "lugger": {
        "file": "data/ships/lugger.yaml",
        "rig": "a lugger",
        "what": "a chasse-marée, three-masted under lugs",
    },
    "smack": {
        "file": "data/ships/smack.yaml",
        "rig": "a smack",
        "what": "a fishing smack, her well amidships",
    },
    # package 75 (docs/design/Design-Ship-Indefatigable.md §8; D16 (a)): the Indefatigable as
    # built, an Ardent-class 64 of 1784, and as razeed in 1795, a 44 cut down from her; the
    # tops make out a ship
    "sixty-four": {
        "file": "data/ships/sixty-four.yaml",
        "rig": "a ship",
        "what": "a sixty-four, a ship of the line of two tiers of ports",
    },
    "razee": {
        "file": "data/ships/razee-44.yaml",
        "rig": "a ship",
        "what": "a razee, a heavy frigate cut down from a sixty-four, one tier of "
        "twenty-four-pounders",
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
    "a privateer schooner": "privateer schooner",
    "an armed schooner": "privateer schooner",
    "armed schooner": "privateer schooner",
    "a letter of marque": "privateer schooner",
    "letter of marque": "privateer schooner",
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
    "a lugger": "lugger",
    "lugger": "lugger",
    "a chasse-maree": "lugger",
    "chasse-maree": "lugger",
    "a chasse-marée": "lugger",
    "chasse-marée": "lugger",
    "a smack": "smack",
    "smack": "smack",
    "a fishing smack": "smack",
    "fishing smack": "smack",
    # package 75 (Design-Ship-Indefatigable.md §8): never "a ship of the line", the 74's words
    "a sixty-four": "sixty-four",
    "sixty-four": "sixty-four",
    "a 64": "sixty-four",
    "a sixty-four gun ship": "sixty-four",
    "a razee": "razee",
    "razee": "razee",
    "a razee frigate": "razee",
    "a cut-down sixty-four": "razee",
}


def description_key(words: str) -> str | None:
    """The description a scenario's words name ('a merchant brig', 'brig-sloop'); None
    for words that name none."""
    key = " ".join(str(words).lower().replace("_", " ").split())
    if key in DESCRIPTIONS:
        return key
    found = _DESCRIPTION_WORDS.get(key)
    if found is not None:
        return found
    # the description's own words after what qualifies them (package 68; the cold review
    # of 2026-10-22, R-43: "a French lugger" and "a small fishing lugger" were no
    # descriptions): the longest tail of the words that names one
    parts = key.removeprefix("a ").removeprefix("an ").removeprefix("the ").split()
    for n in range(len(parts) - 1, 0, -1):
        tail = " ".join(parts[-n:])
        if tail in DESCRIPTIONS:
            return tail
        if tail in _DESCRIPTION_WORDS:
            return _DESCRIPTION_WORDS[tail]
    return None


# The three caches by ship file (the descriptions, the masthead, the polar) hold 32: the
# eight files and the new ships' (package 75), each drawn once a run as before
# (docs/design/Design-Ship-Indefatigable.md §8: results unchanged, the pace kept).
@functools.lru_cache(maxsize=32)
def file_descriptions(ship_file: str) -> dict[str, dict[str, Any]]:
    """The descriptions a ship file carries of itself (`ship.descriptions`, written by
    `tools/gen_ships.py`: the brig's two), each {rig, what, note} and, where the file gives
    them (package 75; docs/design/Build-Ships.md §8.1), the `fit` a far ship of it carries
    when the scenario names none and the `roles` a scenario may give her, kept a list;
    empty for a file without them. The file is the source and `DESCRIPTIONS` the index."""
    import yaml

    try:
        doc = yaml.safe_load(open(ship_file, encoding="utf-8")) or {}
    except OSError:
        return {}
    found = (doc.get("ship") or {}).get("descriptions") or {}
    return {
        str(k): {kk: _description_value(kk, vv) for kk, vv in (v or {}).items()}
        for k, v in found.items()
    }


def _description_value(key: str, value: Any) -> Any:
    """A word of a file's description as kept: `roles` a list of words (one word read as a
    list of one), every other a string."""
    if key == "roles":
        return [str(r) for r in value] if isinstance(value, list | tuple) else [str(value)]
    return str(value)


# The player's ship files that no far description sails, by the description their words
# are taken from for her shadow in another ship's lookout (package 70).
SHADOW_FILES: dict[str, str] = {"merchant-brig.yaml": "merchant brig"}


def description(key: str) -> dict[str, Any]:
    """A description by its key: the index's entry with the ship file's own words for
    her rig and what she is where the file gives them, and her file's `fit` and `roles`
    for it where it gives them (package 75; absent otherwise)."""
    d: dict[str, Any] = dict(DESCRIPTIONS[key])
    own = file_descriptions(d["file"]).get(key)
    if own:
        d["rig"] = own.get("rig") or d["rig"]
        d["what"] = own.get("what") or d["what"]
        if own.get("fit"):
            d["fit"] = own["fit"]
        if own.get("roles"):
            d["roles"] = list(own["roles"])
    return d


@functools.lru_cache(maxsize=32)
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
    peak, within its limit; `evolutions.trim.wanted_sheet_angle` for the sheets, by the
    class whose curve drives the sail, `Sail.curve_class`, package 75)."""
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
            set_sheet_angle(ship, sail, wanted_sheet_angle(sail.curve_class, awa))


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


@functools.lru_cache(maxsize=32)
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
    # ("company", metres), ("lie_to", seconds) or ("home", Position, name); the first is
    # the one in hand, and the vessel is done when the list is empty unless she cycles
    # her route
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
    # the state machine's state her far-detail body resolves (spec M6 §4, "one brain,
    # two bodies"; package 40, `captains.resolve_state`): on passage is her plan, hove
    # to for weather is no way with the plan kept to resume; the rest are 43's with the
    # crewed promotion. A vessel in a checkpoint from before loads on passage.
    state: str = "on passage"
    saved_plan: list[tuple[Any, ...]] | None = None
    # the plan's last mark reached under a held station (package 84, step 4): she lies to
    # there, and her World says so once (`CrewedWorld.far_tick`)
    mark_reached: str = ""
    # the brain on the far body (package 43; spec M6 §4, §19): a vessel given an `intent:`
    # carries a `captains.FarCaptain`, who judges once a minute from her truth and lays
    # her plan state by state; a vessel without one sails her goal's plan as before. Her
    # crewed body while she is promoted (`crews.CrewedWorld`), the tick of her last
    # dealing with the player (a chase, a hail: the cap's order), and a warning the guard
    # gives at her making (a leg across the land, a plan that cannot be laid).
    intent_words: str = ""
    brain: Any = None
    # her hull (package 84, step 6): the `Hull` of the one World that keeps her whole,
    # awake or asleep, None for a ship with none; `crew` is the field's old name
    crew: Any = None
    dealing_tick: int = -1
    warning: str = ""
    sail_order: str = ""  # a station's sail as a state in the far shape (`crews.far_order`)
    # a fishing vessel's fishery (package 56; `world.fishing.Fishery`): her gear, the gear
    # in the water and her catch, one object for her far body and her crewed World; None
    # until she fishes (and in a checkpoint from before)
    fishing: Any = None
    # the far body's short story of her own (package 62; spec M7b §12b's ground): the lines
    # her captain's orders given by the director's hand say in her log while she has no
    # World of her own, as (tick, words); empty in a checkpoint from before
    story: tuple[tuple[int, str], ...] = ()
    # the fit of guns she carries (spec M7 §7; package 70): a name of her file's fits, ""
    # for the file's default; her crewed World's ship is made with it, and the far fight
    # reads it. Her colours as a state the lookout reads (rule 3, 71's hook): "shown" or
    # "struck"; and the far body's damage summed (74's ground, package 70's measure).
    fit: str = ""
    struck: bool = False
    damage: dict[str, Any] = field(default_factory=dict)
    # package 71 (spec M7 §1 to §4): her signal locker (`signals.Locker`: her colours as a
    # state, the hoists flying, her lights; one object with her crewed World's), and whose
    # signals command her (`under the orders of`: a ship's id, 'the ship' for the player's;
    # the least relation under 72's squadron); None and '' in a checkpoint from before
    signals: Any = None
    under_orders_of: str = ""
    # package 72 (spec M7 §21): the set she is a member of (`squadrons.Squadron.id`, written
    # by the set alone; "" for a ship in none), and, on a set's commander, the set's pace as
    # a cap on his far body (the slowest member's best: the convoy at the slowest ship's
    # pace); None in a checkpoint from before and on every ship that commands no set
    squadron: str = ""
    pace_cap_kn: float | None = None
    # package 72 (spec M7 §22): her regime where it is more than her state ("in ordinary":
    # a hull at a port's anchorage with no company and no intent), the sortie she sails
    # for when commissioned, and the tick a commission falls due (-1 for none)
    regime: str = ""
    sortie: str = ""
    commission_tick: int = -1
    # package 75 (docs/design/Build-Ships.md §8.1): the role a scenario gives her (`role:`),
    # one of her description's `roles` and of `captains.ROLES`, which her captain sails by
    # before the one her description and intent give (`brains.role_of_vessel`,
    # `captains.role_for`); "" for none, and in a checkpoint from before. Left out of her
    # saved forms while empty (`to_dict`, `__getstate__`), so that none of them moves
    role: str = ""

    def __getstate__(self) -> dict[str, Any]:
        """Her state for the checkpoint, her role only where a scenario gave her one
        (package 75), so that a vessel without one is pickled as before it."""
        state = dict(self.__dict__)
        if not state.get("role"):
            state.pop("role", None)
        return state

    @property
    def hull(self) -> Any:
        """Her `Hull` (the design's name; `crew` the field's)."""
        return self.crew

    @hull.setter
    def hull(self, value: Any) -> None:
        self.crew = value

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

    def _state_for(self, wind_kn: float, lying_to: bool, at_anchor: bool = False) -> str:
        if at_anchor:
            return "at anchor"
        if lying_to or wind_kn > LIE_TO_OVER_KN:
            return "lying to"
        if self.sail_order == "under reefed topsails" or wind_kn > REEF_OVER_KN:
            return "under reefed topsails"
        return "under plain sail"

    def _target_of(self, world: Any, target_id: Any) -> tuple[Position, float, float] | None:
        """Where a chase's or an evasion's target is now and her way over the ground
        (metres a second east and north): the player's ship (`captains.PLAYER_ID`), or
        another vessel; None when she is gone."""
        from freesail.world.brains import PLAYER_ID

        if target_id == PLAYER_ID:
            pos = world.position
            if pos is None:
                return None
            east, north = _ship_velocity(world)
            return pos, east, north
        other = world.vessels.get(str(target_id)) if target_id else None
        if other is None or other.done:
            return None
        ms = units.knots_to_ms(other.speed_kn)
        rad = math.radians(other.heading_deg)
        return other.position, ms * math.sin(rad), ms * math.cos(rad)

    def pace_kn(self, course_deg: float, wind_from_deg: float, wind_kn: float) -> float:
        """Her speed through the water on a course in a wind, by her polar and her
        sail state; nothing closer to the wind than her polar allows."""
        if self.pace_override_kn is not None:
            return self.pace_override_kn  # a boat under oars: her pull, whatever the wind
        off = abs(units.rad_to_deg(units.wrap_pi(math.radians(course_deg - wind_from_deg))))
        kn = self.polar.speed_kn(off, wind_kn) * self.sailing_factor
        if self.sail_state == "under reefed topsails":
            kn *= REEFED_FACTOR
        cap = getattr(self, "pace_cap_kn", None)
        if cap is not None:
            kn = min(kn, float(cap))  # package 72: the set's pace, the slowest member's
        return max(VESSEL_MIN_SPEED_KN, kn) if off >= self.polar.closest_deg else kn

    def _intercept(self, world: Any, target: Position) -> Position:
        """Where to steer for a ship under way: her position run on at her way over the
        ground for the time it takes to get there at this vessel's own pace (the world's
        own boat knows the world's truth; two passes of the sum are enough). Found on the
        way: a pilot cutter steering for where the ship was, beating, fell astern of a
        schooner crossing her at four knots and never came up with her (truth 70)."""
        east, north = _ship_velocity(world)
        return self._intercept_moving(target, east, north)

    def _intercept_moving(self, target: Position, east: float, north: float) -> Position:
        """`_intercept` for any target with a way over the ground (package 43: a chase
        between vessels)."""
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
        if self.done:
            return
        if not self.plan:
            if self.station_held():
                self.plan = [("lie_to", math.inf)]
            else:
                self.done = True
                return
        leg = self.plan[0]
        kind = leg[0]
        wind_from, wind_ms = self._wind_at(world)
        wind_kn = units.ms_to_knots(wind_ms)
        self.sail_state = self._state_for(wind_kn, kind == "lie_to", kind == "anchor")
        if kind == "anchor":
            # at anchor (package 43, the brain's states): she rides head to wind, no way,
            # no drift, until her captain weighs
            self.heading_deg = wind_from % 360.0
            self.speed_kn = 0.0
            self.tack = 0.0
            return
        if kind in ("chase", "away"):
            # the brain's chase of a stranger, or her flight from one (package 43): the
            # target's place now, the course for it or away from it by the polar's rule
            found = self._target_of(world, leg[1])
            if found is None:
                self.plan.pop(0)
                return
            pos, east, north = found
            if kind == "chase":
                target = self._intercept_moving(pos, east, north)
                arrive_m = float(leg[2]) * ARRIVE_FRACTION if len(leg) > 2 else units.CABLE
                bearing, distance = bearing_and_distance(self.position, target)
                if distance <= arrive_m + 1.0:
                    return  # within hail: she keeps her distance, and her captain speaks her
            else:
                bearing, distance = bearing_and_distance(self.position, pos)
                bearing = (bearing + 180.0) % 360.0
                arrive_m = -1.0
            if self.sail_state == "lying to":
                self.heading_deg = (wind_from + 90.0) % 360.0
                self.speed_kn = 0.0
                self._drift(world, (wind_from + 180.0) % 360.0, units.knots_to_ms(LYING_TO_KN), dt)
                return
            course = self._course_for(bearing, wind_from, wind_kn)
            if self.detail == "near":
                swing = units.rad_to_deg(units.wrap_pi(math.radians(course - self.heading_deg)))
                limit = NEAR_TURN_DEG_S * dt
                course = (self.heading_deg + max(-limit, min(limit, swing))) % 360.0
            self.heading_deg = course
            self.speed_kn = self.pace_kn(course, wind_from, wind_kn)
            step = units.knots_to_ms(self.speed_kn) * dt
            if kind == "chase" and course == bearing and step >= distance - arrive_m:
                step = max(0.0, distance - arrive_m)
            rad = math.radians(course)
            self.position = self.position.advanced(step * math.sin(rad), step * math.cos(rad))
            self.distance_run_m += step
            self._stream(world, dt)
            return
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
        if kind == "company":
            self._keep_company(world, float(leg[1]), dt, wind_from, wind_kn)
            return
        if kind == "station":
            # package 72 (spec M7 §21): her station in her set's formation, by the set
            from freesail.world.squadrons import keep_station

            keep_station(self, world, dt, wind_from, wind_kn)
            return
        if kind == "to_ship":
            target = self._ship_target(world)
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

    def _keep_company(
        self, world: Any, within_m: float, dt: float, wind_from: float, wind_kn: float
    ) -> None:
        """The `company` leg (package 37h): within `within_m` of the ship she goes with
        her at her way over the ground, on her course; beyond it she closes straight for
        her at her own pace or the ship's and `COMPANY_CLOSING_KN` more, whichever is the
        greater. She keeps company until whoever gave her the leg gives her another (the
        pilot's boat, `ports.py`)."""
        target = world.position
        if target is None:
            self.plan.pop(0)
            return
        east, north = _ship_velocity(world)
        ship_ms = math.hypot(east, north)
        bearing, distance = bearing_and_distance(self.position, target)
        if distance <= within_m:
            self.position = self.position.advanced(east * dt, north * dt)
            self.speed_kn = units.ms_to_knots(ship_ms)
            if ship_ms > 0.05:
                self.heading_deg = math.degrees(math.atan2(east, north)) % 360.0
            self.distance_run_m += ship_ms * dt
            return
        own = units.knots_to_ms(self.pace_kn(bearing, wind_from, wind_kn))
        speed = max(own, ship_ms + units.knots_to_ms(COMPANY_CLOSING_KN))
        step = min(speed * dt, max(0.0, distance - 0.9 * within_m))
        rad = math.radians(bearing)
        self.position = self.position.advanced(step * math.sin(rad), step * math.cos(rad))
        self.heading_deg = bearing
        self.speed_kn = units.ms_to_knots(speed)
        self.distance_run_m += step

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

    def _ship_target(self, world: Any) -> Any:
        """Where 'the ship' of a `to_ship` leg is: the player's own hull (whichever is
        followed; package 84, step 10), or the hull a letter she carries is for
        (`Message.to_hull`; package 84, step 9)."""
        to_hull = str(getattr(self.letter, "to_hull", "") or "") if self.letter is not None else ""
        hull = (getattr(world, "hulls", None) or {}).get(to_hull) if to_hull else None
        if hull is not None:
            return hull.position
        players = getattr(world, "players", None)
        return players.position if players is not None else world.position

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
            if self.station_held():
                # a crewed hull whose captain's station is held (package 84, step 4; the
                # design's §2.5): her voyage is that station's to end, not the sea's, so
                # at the plan's last mark she lies to until a course is shaped or she is
                # brought to an anchor; her World says so (`CrewedWorld.far_tick`)
                self.plan = [("lie_to", math.inf)]
                self.mark_reached = (
                    str(leg[2]) if len(leg) > 2 and leg[2] else "the plan's last mark"
                )
                return
            self.done = True

    def station_held(self) -> bool:
        """Whether a station is seated at this hull's captain's station and holds her
        deck (package 84, step 4): the same test the far brain stands aside by."""
        crew = getattr(self, "crew", None)
        near = getattr(crew, "captain", None) if crew is not None else None
        return (
            near is not None
            and bool(getattr(near, "seated", False))
            and not getattr(near, "stand_in", False)
        )

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
        if self.sail_state in ("lying to", "at anchor"):
            return self.sail_state
        point = units.point_name(math.radians(self.heading_deg))
        return f"standing to the {_ward(self.heading_deg)} ({point}), {self.sail_state}"

    def colours_words(self) -> str:
        """Her colours as a lookout reads them (package 71): the nation SHOWN, which under
        false colours is not her own; 'a stranger, her colours not made out' when none."""
        from freesail.world.signals import vessel_locker

        return vessel_locker(self).colours.words(None)

    @property
    def nation_shown(self) -> str | None:
        """The nation a lookout makes out from her colours, None when none show."""
        from freesail.world.signals import colours_seen

        shows, nation, _adj, _flag = colours_seen(self)
        return nation if shows else None

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
        d: dict[str, Any] = {
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
        if self.brain is not None:
            # the brain's record (package 43), on a vessel with an intent only: nothing new
            # in the pinned form of a vessel without one
            d["intent"] = self.intent_words
            d["brain"] = self.brain.to_dict()
            # crewed is awake at full detail; a World kept asleep (package 84, step 5) says
            # so apart, so that the glass's pinned data reads as before the step
            awake = self.crew is not None and getattr(self.crew, "shape", "full") == "full"
            d["crewed"] = awake
            if self.crew is not None and not awake:
                d["asleep"] = True
        if self.warning:
            d["warning"] = self.warning
        if getattr(self, "fit", ""):
            d["fit"] = self.fit  # package 70
        if getattr(self, "role", ""):
            d["role"] = self.role  # package 75: only where a scenario gave her one
        if getattr(self, "struck", False):
            d["struck"] = True
        locker = getattr(self, "signals", None)
        if locker is not None and locker.colours.state != "shown":
            d["colours"] = locker.colours.to_dict()  # package 71: only off the plain state
        if getattr(self, "under_orders_of", ""):
            d["under_orders_of"] = self.under_orders_of
        if getattr(self, "squadron", ""):
            d["squadron"] = self.squadron  # package 72: only on a member
        story = getattr(self, "story", ()) or ()
        if story:
            # her captain's orders by the director's hand (package 62): only where there
            # are some, so that every pinned form stands
            d["story"] = [list(line) for line in story]
        return d


# ---------------------------------------------------------------------------
# A vessel from a scenario's or a world order's words
# ---------------------------------------------------------------------------


@contextmanager
def players_current(world: Any) -> Iterator[Any]:
    """The block reads the player's ship: given a World or a hull, the player's own hull
    (`World.players`, whichever hull is followed or current since step 10) is made current
    for it and the World yielded, so that her per-ship names (`ship`, `position`,
    `dealings`, `readings`) and the properties of her per-ship objects are hers (package
    84, step 6); what was given is yielded as it is when she is current already, on the
    endless plane and in an old shape."""
    base = world.__dict__.get("world", world) if hasattr(world, "__dict__") else world
    players = base.__dict__.get("_own") if hasattr(base, "__dict__") else None
    if players is None or getattr(base, "own", None) is players:
        yield base if players is not None else world
        return
    with base.as_hull(players):
        yield base


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
    ports = getattr(world, "dealings", None)
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
    in company with the ship [within <n> cables]   keeping company with the player's ship (71)
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
    m = re.match(
        r"^(?:in|keeping|keep)\s+company\s+with\s+(?:the\s+)?(?:ship|commodore|convoy|flag)"
        r"(?:\s+within\s+([\d.]+)\s+cables?)?$",
        text,
    )
    if m:
        # package 71 (spec M7 §3, the least relation): a merchantman of a convoy keeps
        # company with the player's ship (the pilot's boat's `company` leg, 37h) within so
        # many cables, two by default; her signals are read by `under_the_orders_of`
        cables = float(m.group(1) or 2.0)
        return (
            [("company", cables * units.CABLE)],
            False,
            f"in company with the ship within {cables:g} cables",
        )
    raise ValueError(
        f"'{goal}' is no goal a captain at far detail knows: say trading <A> to <B>, bound "
        f"from <A> for <B>, patrolling off <place> within <n> miles, running home to <place>, "
        f"carrying the mail to <place>, carrying a letter to the ship, or in company with "
        f"the ship."
    )


def approach_plan(world: Any, port: Any) -> list[tuple[Any, ...]]:
    """A port's way in from the sea as a far body's plan (package 43b's business, and since
    package 84 step 4 the far shape's `shape a course for <port>`): its track from the sea,
    its road, its inner track to the anchorage (`Planner.legs_for`'s, without the sea
    route to its first mark)."""
    from freesail.world.brains import _plan_of_legs
    from freesail.world.captains import Planner

    planner = Planner(world)
    plan = _plan_of_legs(planner._port_track(port, "from_sea"))
    road = ("to", port.outer_road.position, port.outer_road.name)
    if not any(len(leg) > 1 and leg[1] == road[1] for leg in plan):
        plan.append(road)
    plan += _plan_of_legs(planner._port_track(port, "in"))
    anchorage = ("to", port.anchorage.position, port.anchorage.name)
    if not any(len(leg) > 1 and leg[1] == anchorage[1] for leg in plan):
        plan.append(anchorage)
    return plan


def port_course(world: Any, vessel: Any, port: Any, via: str = "") -> list[tuple[Any, ...]]:
    """A far body's course for a port by the tracks (package 84, step 4; the design's §2.5
    and its finding 4): the planner's passage for it (`Planner.legs_for`) as the far brain
    lays one, out of the port she lies in by its track to sea, along the common tracks
    where the straight line is not clear of the shore, by the marks her captain names
    (`via`, package 45's words: 'the Start, the Bolt Tail', each given its offing) where the
    chart has no track, in by the port's track from the sea to its road and its anchorage,
    the whole under the land guard (`land_crossing`); raises ValueError in words when a leg
    crosses the land, naming the way by marks."""
    from freesail.world.brains import _plan_of_legs
    from freesail.world.captains import Planner, read_intent

    here = vessel.position
    ports = getattr(world, "ports", None)
    lying = ports.in_port_at(here) if ports is not None else None
    departing = lying.id if lying is not None and lying.id != port.id else ""
    words = f"bound for {port.name}" + (f" via {via}" if via else "")
    intent = read_intent(world, words)
    legs = Planner(world).legs_for(intent, here, departing)
    # the port she weighs from: its anchorage is where she lies, not a mark to anchor at
    # (Torbay's track to sea begins at Brixham road); and the plan ends at the first anchor
    # in the port she is bound for (a track whose road follows its anchorage)
    legs = [leg for leg in legs if not (leg.kind == "anchorage" and leg.port == departing)]
    plan = _plan_of_legs(legs)
    for i, leg in enumerate(plan):
        if leg[0] == "anchor":
            plan = plan[: i + 1]
            break
    crossing = land_crossing(world, here, plan)
    if crossing:
        way = f" via {via}" if via else ""
        raise ValueError(
            f"the course for {port.name}{way} by the tracks {crossing}; give the way by marks "
            f"('shape a course for {port.name} via <a headland or a position>')"
        )
    return plan


def _out_of_port(world: Any, port_id: str) -> list[tuple[Any, ...]]:
    """The marks of a port's track to sea (`Planner._port_track`), as a far body's plan."""
    ports = getattr(world, "ports", None)
    port = (getattr(ports, "ports", None) or {}).get(port_id) if ports is not None else None
    if port is None:
        return []
    from freesail.world.brains import _plan_of_legs
    from freesail.world.captains import Planner

    return _plan_of_legs(Planner(world)._port_track(port, "to_sea"))


def _role_of_spec(spec: dict[str, Any], key: str, d: dict[str, Any]) -> str:
    """A far ship's `role:` (package 75; Build-Ships.md §8.1): a captain's role
    (`captains.ROLES`) that her description's file gives her among its `roles`, "in their
    reasonable degrees"; "" where the scenario names none. Anything else is refused in
    words, at her making."""
    role = " ".join(str(spec.get("role") or "").lower().split())
    if not role:
        return ""
    from freesail.world.captains import ROLES

    if role not in ROLES:
        raise ValueError(f"'{role}' is no captain's role; the roles: {', '.join(ROLES)}.")
    roles = list(d.get("roles") or [])
    if role not in roles:
        given = f"the roles {', '.join(roles)}" if roles else "no role"
        raise ValueError(f"'{role}' is no role a {key} takes; her file gives a {key} {given}.")
    return role


def _default_fit(ship_file: str) -> str:
    """Her file's default fit (package 75): its armament's `default`, or `unarmed` for a
    file with no armament, whose ship carries no guns already."""
    from freesail.ship.loader import load_spec
    from freesail.ship.schema import UNARMED

    armament = load_spec(ship_file).armament
    return armament.default if armament is not None else UNARMED


def vessel_from_spec(world: Any, spec: dict[str, Any], serial: int) -> Vessel:
    """A vessel from a scenario's `ships:` entry or a world order's words: her
    description (one of `DESCRIPTIONS`), her name, her nation, her position and her goal;
    `colours: shown | none` whether she wears them. Her sailing factor is drawn from the
    `ships` stream, so that two brigs of one file are not one brig. Package 75
    (docs/design/Build-Ships.md §8.1): `role:` the role her captain sails by, one of her
    description's `roles` and of `captains.ROLES`, else refused in words; with no `fit:`
    she carries her description's fit where her file gives one that is not its default."""
    key = description_key(str(spec.get("description") or spec.get("kind") or ""))
    if key is None:
        raise ValueError(
            f"'{spec.get('description')}' is no description a far-detail ship takes; say one "
            f"of {', '.join(DESCRIPTIONS)}."
        )
    d = description(key)
    role = _role_of_spec(spec, key, d)
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
    departing = str(spec.get("departing") or "")
    if departing and not cycle and not (spec.get("intent") or spec.get("free_intent")):
        # made in a port's harbour (package 68, spec M7b §21i's simple half): out by the
        # port's track to sea, the pilot's way, before her goal's legs, and not across the
        # land (an intent's captain lays it so himself, `brains.FarCaptain`)
        plan = _out_of_port(world, departing) + plan
    if spec.get("sailing_factor") is not None:
        # drawn by the caller from its own stream (the world's business, package 43b, so
        # that its ships move no draw of the scenario's)
        factor = float(spec["sailing_factor"])
    else:
        stream = world.rng.stream("ships")
        factor = SAILING_FACTOR_MIN + (1.0 - SAILING_FACTOR_MIN) * stream.random()
    colours_word = str(spec.get("colours", "shown")).lower().strip()
    shows = colours_word not in ("none", "no", "false", "hidden")
    fit = " ".join(str(spec.get("fit") or "").split())
    if not fit and d.get("fit") and d["fit"] != _default_fit(d["file"]):
        # package 75 (§8.1): the sub-type's fit where the scenario names none, and only
        # where it is not her file's default, so that a far ship of the default keeps the
        # pinned form she had (`to_dict` writes a fit only where she has one)
        fit = str(d["fit"])
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
        fit=fit,
        role=role,
    )
    # package 71: `colours: <another nation>` is false colours of that nation ('colours:
    # British' on a French privateer); `under_the_orders_of:` whose signals command her;
    # `lights:` what she shows by night
    from freesail.world.signals import set_colours, vessel_locker

    locker = vessel_locker(vessel)
    if shows and colours_word not in ("shown", "yes", "true", ""):
        other = world.nations.find(colours_word)
        if other is None:
            raise ValueError(
                f"'{spec.get('colours')}' is no colours a ship shows: 'shown', 'none', or a "
                "nation of the table for false colours"
            )
        if other.id != nation.id:
            set_colours(locker.colours, world.nations, "false", other.id, 0)
    boss = spec.get("under_the_orders_of", spec.get("under_orders_of"))
    if boss:
        vessel.under_orders_of = " ".join(str(boss).split())
    if spec.get("lights"):
        locker.lights = str(spec["lights"])
    if str(spec.get("regime") or "").lower().strip() == "in ordinary":
        # package 72 (spec M7 §22): a hull laid up at a port's anchorage, commissioned later
        from freesail.world.regimes import put_in_ordinary

        ports = getattr(world, "dealings", None)
        port = None
        best = None
        for p in (getattr(ports, "ports", None) or {}).values():
            _, d = bearing_and_distance(position, p.anchorage.position)
            if best is None or d < best:
                port, best = p, d
        if port is None or best is None or best > 3.0 * units.NAUTICAL_MILE:
            raise ValueError(f"'{name}' in ordinary lies at no port's anchorage")
        vessel.position = port.anchorage.position
        put_in_ordinary(world, vessel, port, str(spec.get("sortie") or ""))
        return vessel
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
    intent = " ".join(str(spec.get("intent") or "").split())
    free = " ".join(str(spec.get("free_intent") or "").split())
    if intent and free:
        raise ValueError(
            f"{name} is given both an intent and a free intent; give her one or the other."
        )
    if intent or free:
        # the brain on the far body (package 43): her captain, who lays her plan from the
        # intent over the chart at his first judgement; refused in words when the intent
        # is none a captain knows. A free intent (`free_intent:`, 2026-10-27) is taken as
        # it is said, the goal for a model at her captain's station: he does not sail by it
        from freesail.world.brains import FarCaptain
        from freesail.world.captains import free_intent

        words = intent or free
        vessel.intent_words = words
        given = free_intent(words) if free else None
        vessel.brain = FarCaptain(world, vessel, words, given=given)
        if spec.get("departing"):
            # lying in a port (the world's business, package 43b): her plan goes out by
            # the port's track, as a ship's that sails from it does
            vessel.brain._departing = str(spec["departing"])
        vessel.brain._plan()
        if vessel.warning:
            raise ValueError(vessel.warning)
        crossing = land_crossing(world, vessel.position, vessel.plan)
        if crossing:
            # the far-detail guard (spec M6 §19): a captain's plan across the land is
            # refused at her making, not sailed
            raise ValueError(f"{name}'s plan {crossing}; give her a way by marks (via)")
        vessel.heading_deg = (
            bearing_and_distance(position, vessel.plan[0][1])[0]
            if vessel.plan and len(vessel.plan[0]) > 1 and isinstance(vessel.plan[0][1], Position)
            else vessel.heading_deg
        )
    else:
        # the guard's word on a ship without a brain, whose plan is the goal's straight
        # legs (the recorded passages' dozen are such, and six of them sail across a cape
        # at far detail: the measurement in docs/dev/TuningNotes.md, package 43); the
        # driver prints it with the scenario's lines, and nothing of it is in the log
        crossing = land_crossing(world, vessel.position, vessel.plan)
        if crossing:
            vessel.warning = f"her plan {crossing}"
    return vessel


def land_crossing(world: Any, start: Position, plan: list[tuple[Any, ...]]) -> str:
    """The far-detail guard (package 43; spec M6 §19): the first leg of a plan whose
    straight line crosses dry ground on the chart in words ('crosses the land on the leg
    to Brest'), or "" when every leg keeps clear or the world has no chart. A leg's first
    and last cable are not tried (she lies where she lies; a place may be the shore)."""
    chart = getattr(world, "chart", None)
    if chart is None:
        return ""
    a = start
    for leg in plan:
        if len(leg) < 2 or not isinstance(leg[1], Position):
            continue
        b = leg[1]
        try:
            hit = chart.line_shore(
                a, b, units.CABLE, skip_start_m=units.CABLE, skip_end_m=units.CABLE
            )
        except Exception:  # noqa: BLE001 - beyond the chart's field
            hit = None
        if hit is not None and hit[2]:
            name = str(leg[2]) if len(leg) > 2 and leg[2] else "her mark"
            return f"crosses the land on the leg to {name}"
        a = b
    return ""


# ---------------------------------------------------------------------------
# The vessels of one World
# ---------------------------------------------------------------------------


class Vessels:
    """The vessels of one World, ticked once a game minute (`World.tick`; a near-detail
    vessel every second), and what the lookout can see of them."""

    # Package 43: the player's ship as the far-detail brains see her (`player_shadow`), the
    # lines the brains' meetings make before the tick records them, and the crewed
    # promotion's bookkeeping (`crews.promote_and_demote`). Class defaults, so that a
    # checkpoint from before loads with them.
    _shadow: Vessel | None = None
    _spoke_lines: list[tuple[Any, ...]] | None = None
    crewed_ids: tuple[str, ...] = ()

    def __init__(self, world: Any = None) -> None:
        self.world = world
        self.vessels: list[Vessel] = []
        self.serial = 0
        # the followed hull's own vessel (package 84, step 7; the shadow before it): the
        # player's ship as a vessel of the sea, last in `vessels`, never moved by the sea
        self.own: Vessel | None = None
        self._spoke_lines = []
        self.crewed_ids = ()

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
        own = self.__dict__.get("own")
        if own is not None and self.vessels and self.vessels[-1] is own:
            # the followed hull's vessel stays last (the design's rule 3: the brains'
            # nearest-first orders and the lookouts' lists as the shadow gave them)
            self.vessels.insert(len(self.vessels) - 1, vessel)
        else:
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
        """The other sail on the sea: every vessel not done but the player's own (package 84,
        step 7: she is on the sea, last, and no sail of her own lookout's)."""
        own = self.__dict__.get("own")
        return [v for v in self.vessels if not v.done and v is not own]

    def tick(self, world: Any, dt: float = float(VESSEL_TICK_S)) -> list[tuple[Any, ...]]:
        """The minute's move of every far-detail vessel; the second's of a near one
        (`tick_near`). Returns the lines the vessels' own events make (a letter brought
        alongside, a vessel within hail), for the World to record."""
        lines: list[tuple[Any, ...]] = []
        # the brains judge first, once a minute, from their own truth (package 43): what
        # each sees of the others is as they stood at the minute's start, as the player's
        # lookout sees them
        if self._spoke_lines is None:
            self._spoke_lines = []
        for v in self.vessels:
            if v.done or v.brain is None or (v.crew is not None and v.crew.shape == "full"):
                continue
            v.brain.tick()
        sets = getattr(world, "squadrons", None)
        if sets is not None:
            # the squadrons' minute (package 72; spec M7 §21): the stations computed from
            # the commanders' frames, the stragglers counted, the commanders' books read;
            # and the far captures, a rule of the sea whether a set is on it or not
            lines.extend(sets.tick(world))
        if any(getattr(v, "regime", "") == "in ordinary" for v in self.vessels):
            # the regimes' minute (package 72; spec M7 §22): the commissions due, the sorties
            from freesail.world.regimes import minute as regimes_minute

            lines.extend(regimes_minute(world))
        if any(v.under_orders_of and v.brain is None and not v.done for v in self.vessels):
            # a vessel under another's orders with no brain (a convoy's merchantman given
            # only her company to keep) reads and obeys the signals by the least captain
            # (package 71; `signalling.brainless_minute`)
            from freesail.world.signalling import brainless_minute

            brainless_minute(world)
        for v in self.vessels:
            if v.done or v.detail == "near" or (v.crew is not None and v.crew.shape == "full"):
                continue
            v.tick(world, dt)
            if v.crew is not None:
                from freesail.world.crews import mirror_far

                mirror_far(v.crew)  # a sleeping hull follows her far body's move
        lines.extend(self._spoke_lines)
        self._spoke_lines = []
        self._deliver_to_hulls(world)
        lines.extend(self._promote_and_hail(world))
        if any(v.brain is not None for v in self.vessels) or self.crewed_ids:
            # the crewed promotion by the range and the cap (package 43; `world.crews`),
            # and the director's seats' budgets (spec M6 §23)
            from freesail.world.crews import enforce_budgets, switch

            switch(world)
            enforce_budgets(world)
        self.vessels = [v for v in self.vessels if not v.done]
        return lines

    def tick_crews(self, world: Any) -> None:
        """Every second: each crewed vessel's own World ticked (her physics, her book,
        her captain, her stations), and her truth mirrored into the far body's record
        (package 43; `world.crews`); a World kept in the far shape for a seated station
        mirrors the far body instead."""
        if not self.crewed_ids:
            return
        from freesail.world.crews import far_tick, mirror

        minute = world.clock.ship_time.second == 0
        for v in self.vessels:
            crew = v.crew
            if crew is None or v.done or crew.is_followed:
                continue  # the followed hull's tick is the World's own
            if not crew.awake:
                far_tick(crew)
                continue
            # her tick is the World's own with her current (package 84, step 6)
            with world.as_hull(crew):
                world.tick()
            mirror(v, crew, minute)

    # -- the followed hull's own vessel (package 84, step 7; the shadow of package 43) -----

    def player_shadow(self, world: Any) -> Vessel | None:
        """The player's ship as a vessel of the sea (package 84, step 7; `Vessels.own`): a
        vessel of her file's description under `PLAYER_ID`, at her truth, her colours
        taken as shown, her sail state by her manoeuvre, her hull the followed hull and the
        followed hull's `vessel` her; made at the first asking and kept last in `vessels`,
        brought up to her truth every tick of the followed hull's (`World._tick_vessels`)
        and at every asking; None on the endless plane. The name is the shadow's, which
        every reader of hers asked by it; she is the one vessel the sea never moves."""
        from freesail.world.captains import _is_kings_ship

        with players_current(world) as world:
            pos = getattr(world, "position", None)
            if pos is None or getattr(world, "is_observer", False):
                # none on the plane; none in an observed world (package 82, item 1): the
                # observer's hull is no ship on the sea, and no brain sees her
                return None
            ship = world.ship
            s = self.__dict__.get("own")
            if s is None:
                source = str(getattr(getattr(ship, "spec", None), "source", "") or "")
                key = ""
                for k, d in DESCRIPTIONS.items():
                    if (
                        source
                        and d["file"].split("/")[-1] == source.replace("\\", "/").split("/")[-1]
                    ):
                        key = k
                        if k != "merchant brig":
                            break
                if key in ("merchant brig", "brig-sloop"):
                    key = "brig-sloop" if _is_kings_ship(world) else "merchant brig"
                if not key:
                    # a player's file no far description sails (the merchant brig's own, package
                    # 70): her words by the file's name, so that another ship's lookout does not
                    # read a trader as 'a ship' of the line's class
                    key = SHADOW_FILES.get(source.replace("\\", "/").split("/")[-1], "")
                d = description(key) if key else {"file": source, "rig": "a ship", "what": "a ship"}
                ports = getattr(world, "dealings", None)
                nation_id = str(getattr(ports, "ship_nation", "") or "britain")
                try:
                    nation = world.nations.get(nation_id)
                except KeyError:
                    nation = None
                s = Vessel(
                    id=PLAYER_ID,
                    name=str(getattr(ship, "name", "") or "the ship"),
                    kind=d["rig"],
                    ship_file=d["file"] or source,
                    nation=nation_id,
                    position=pos,
                    colours=getattr(nation, "colours", ""),
                    flag=getattr(nation, "flag", ""),
                    nation_adjective=getattr(nation, "adjective", ""),
                    description=key,
                    what=d["what"],
                    detail="crewed",
                )
                self.own = s
                self.vessels.append(s)  # last, and kept last by `add`
            hull = world.own
            if s.crew is not hull:
                # her hull the followed hull, and she its vessel (a load re-links them)
                s.crew = hull
                hull.vessel = s
            # package 71: the player's locker is her vessel's (her colours as she shows them,
            # her signals flying), one object
            from freesail.world.signals import player_locker

            s.signals = player_locker(world)
            s.position = pos
            s.struck = bool((getattr(ship, "extra", None) or {}).get("struck"))  # package 70
            s.heading_deg = units.rad_to_deg(float(ship.heading)) % 360.0
            s.speed_kn = units.ms_to_knots(_ship_speed_ms(ship))
            # her sail state by her manoeuvre, read from the ship as the reading
            # `manoeuvre_in_hand` reads it (`api.readings._manoeuvre`), every tick
            if getattr(world, "at_anchor", False):
                s.sail_state = "at anchor"
            elif _lying_to(world):
                s.sail_state = "lying to"
            else:
                s.sail_state = "under plain sail"
            return s

    def strangers_of(
        self, world: Any, vessel: Vessel, spoken: set[str], glass_for: str | None = None
    ) -> list[dict[str, Any]]:
        """The sail in sight from a vessel's masthead, in the form the captain's
        `strangers` reading gives (package 43, `captains.Perception.of_vessel`): every
        other vessel and the player's ship within the horizon her rig's height and the
        other's give, within the player's visibility, by day (at night close aboard, as
        the land is), each made out at the lookout's distances by eye (the glass aloft for
        the one her captain has in hand), her nation when her colours are shown and made
        out, `spoken` for a sail spoken; the distance is her truth, nearest first."""
        from freesail.world.chart import NIGHT_LAND_NM
        from freesail.world.lookout import relative_words

        conditions = getattr(world, "conditions", None)
        vis_nm = float(conditions.visibility_nm) if conditions is not None else math.inf
        daylight = str(world.daylight)
        pos, eye = vessel.position, vessel.height_m
        heading = math.radians(vessel.heading_deg)
        items: list[dict[str, Any]] = []
        self.player_shadow(world)  # the followed hull's vessel brought up to her truth
        others: list[Vessel] = [o for o in self.vessels if o is not vessel and not o.done]
        for o in others:
            bearing, distance = bearing_and_distance(pos, o.position)
            nm = distance / units.NAUTICAL_MILE
            limit = min(vis_nm, horizon_nm(eye, o.height_m))
            if o.seen_within_nm is not None:
                limit = min(limit, o.seen_within_nm)
            if daylight != "day":
                limit = min(limit, NIGHT_LAND_NM)
            if nm > limit:
                continue
            level, _ = o.made_out(distance, glass=(o.id == glass_for))
            shown = o.nation_shown  # package 71: the colours SHOWN, false or true
            colours = level >= 2 and shown is not None
            items.append(
                {
                    "id": o.id,
                    "bearing_deg": round(bearing, 1),
                    "bearing": units.point_name(math.radians(bearing)),
                    "relative": relative_words(math.radians(bearing) - heading),
                    "estimate_m": round(distance),
                    "made_out": level,
                    "known": o.words_at(level),
                    "nation": shown if colours else None,
                    "spoken": o.id in spoken,
                    "size": _size_of(o),
                }
            )
        items.sort(key=lambda s: s["estimate_m"])
        return items

    def spoke(self, a: Vessel, b_id: str) -> None:
        """Two sail within hail of one another, one of them speaking the other (package
        43; the owner's note 19: a word in the log at hailing distance): a routine line
        when the player's lookout has both in sight, in the words he has for them; nothing
        otherwise, since a meeting beyond his horizon is no line of his log."""
        from freesail.core.events import Severity

        world = self.world
        lookout = getattr(world, "lookout", None)
        if lookout is None or self._spoke_lines is None:
            return
        seen = getattr(lookout, "_sails_seen", {}) or {}
        wa, wb = seen.get(f"sail:{a.id}"), seen.get(f"sail:{b_id}")
        if not wa or not wb:
            return
        brain = a.brain
        exchange = str(getattr(brain, "_exchange", "") or "") if brain is not None else ""
        hail = brain.doctrine.threshold("hail", "") if brain is not None and brain.doctrine else ""
        if exchange:
            # package 71: the standard exchange written once, in the lookout's hearing
            said = f" {wa} hails her, and the words carry across the water: {exchange}"
        else:
            said = f" {wa} hails her" + (f": {hail!r}" if hail else "") + "."
        self._spoke_lines.append(
            (
                Severity.ROUTINE,
                "sail.spoke",
                f"{wa} and {wb[:1].lower() + wb[1:]} are within hail of one another.{said}",
                {"id": a.id, "other": b_id},
            )
        )

    def tick_near(self, world: Any, dt: float = 1.0) -> list[tuple[Any, ...]]:
        """Every second: the near-detail vessels only."""
        if not any(v.detail == "near" and not v.done for v in self.vessels):
            return []
        for v in self.vessels:
            if v.detail == "near" and not v.done:
                v.tick(world, dt)
                if v.crew is not None:
                    from freesail.world.crews import mirror_far

                    mirror_far(v.crew)  # a sleeping hull within the near range (step 6)
        lines = self._promote_and_hail(world)
        self.vessels = [v for v in self.vessels if not v.done]
        return lines

    def _deliver_to_hulls(self, world: Any) -> None:
        """A letter carried for another hull comes aboard her within hail (package 84,
        step 9), the lines hers; the carrier goes home after."""
        from freesail.core.events import Severity

        hulls = getattr(world, "hulls", None) or {}
        players = getattr(world, "players", None)
        for v in self.vessels:
            letter = v.letter
            if v.done or letter is None:
                continue
            to_hull = str(getattr(letter, "to_hull", "") or "")
            hull = hulls.get(to_hull) if to_hull else None
            if hull is None and players is not None and players is not getattr(world, "own", None):
                hull = players  # the player's letter while another hull is followed (step 10)
            if hull is None or hull is getattr(world, "own", None) or hull.position is None:
                continue
            _, distance = bearing_and_distance(hull.position, v.position)
            if distance / units.NAUTICAL_MILE > HAIL_NM:
                continue
            words = v.what or v.name
            hull.record(
                Severity.NOTABLE,
                "sail.within_hail",
                f"{_head(words)} is within hail, {v.course_words()}; she has a letter for "
                "the ship.",
                data={"id": v.id, "letter": True},
            )
            v.letter, v.alongside = None, True
            for severity, kind, text, data in hull.people.message_aboard(letter):
                hull.record(severity, kind, text, data=data)
            v.alongside = False

    def _promote_and_hail(self, world: Any) -> list[tuple[Any, ...]]:
        """The level of detail by the distance from the player, and a vessel come within
        hail (a letter she carries comes aboard: the carrier of truth 68)."""
        from freesail.core.events import Severity

        pos = world.position
        if pos is None:
            return []
        lines: list[tuple[Any, ...]] = []
        own = self.__dict__.get("own")
        for v in self.vessels:
            if v.done or v is own:
                continue
            _, distance = bearing_and_distance(pos, v.position)
            nm = distance / units.NAUTICAL_MILE
            if v.detail == "far" and nm <= NEAR_DETAIL_NM:
                v.promote(True)
            elif v.detail == "near" and nm > NEAR_DEMOTE_NM:
                v.promote(False)
            brain = v.brain
            if brain is not None and (
                nm <= HAIL_NM
                or (
                    brain._stranger == _player_id()
                    and brain.state in ("investigating a stranger", "chasing", "evading")
                )
            ):
                # in dealings with the player (package 43): a chase, a hail; the cap's order
                v.dealing_tick = world.clock.tick
            if nm <= HAIL_NM and not v.hailed:
                v.hailed = True
                v.spoken = True
                words = v.what or v.name
                hail = ""
                if brain is not None:
                    # her captain speaks the ship (package 43; the owner's note 19)
                    brain.speak(_player_id())
                    said = brain.doctrine.threshold("hail", "") if brain.doctrine else ""
                    hail = f" She hails: {said!r}." if said else ""
                    if said:
                        # package 71: the hail heard on deck, for the stations and for the
                        # player's answer (`say to her: ...`), which her captain reads
                        from freesail.world.hail import player_hailed

                        player_hailed(world, v, said)
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
                            f"{v.colours_words()}.{hail}",
                            {"id": v.id, "letter": False},
                        )
                    )
            elif nm > HAIL_NM * 2.0:
                v.hailed = False
        return lines

    def in_sight(
        self,
        pos: Position,
        height_of_eye_m: float,
        visibility_nm: float | None,
        daylight: str,
        viewer: Vessel | None = None,
    ) -> list[Sighting]:
        """The vessels in sight from the masthead: within the horizon her rig's height
        and the eye give (truth 67), within the weather's visibility, by day; at night a
        sail is seen only close aboard, as the land is (`chart.NIGHT_LAND_NM`)."""
        from freesail.world.chart import NIGHT_LAND_NM
        from freesail.world.signals import LIGHT_SEEN_NM

        vis_nm = math.inf if visibility_nm is None else float(visibility_nm)
        out: list[Sighting] = []
        for v in self.vessels:
            if v.done or v is viewer:
                continue  # her own body is no sail of hers (package 84, step 7)
            bearing, distance = bearing_and_distance(pos, v.position)
            nm = distance / units.NAUTICAL_MILE
            limit = min(vis_nm, horizon_nm(height_of_eye_m, v.height_m))
            if v.seen_within_nm is not None:
                limit = min(limit, v.seen_within_nm)  # a boat: the eye's limit, not the horizon's
            if daylight != "day":
                limit = min(limit, NIGHT_LAND_NM)
            if nm <= limit:
                out.append(Sighting(v.seen_as_feature(distance), bearing, distance, "sail"))
            elif vis_nm < 1.0 and _sound_of(v, nm):
                # package 71 (spec M7 §5): in fog her bell at anchor, her gun or her drum under
                # way, heard beyond the visibility at the range a sound carries
                out.append(
                    Sighting(
                        Feature(
                            f"sound:{v.id}",
                            "sound",
                            _sound_of(v, nm),
                            v.position.lat_deg,
                            v.position.lon_deg,
                            modern=v.id,
                            height_m=v.height_m,
                        ),
                        bearing,
                        distance,
                        "sound",
                    )
                )
            elif daylight == "night" and nm <= min(vis_nm, LIGHT_SEEN_NM) and _lights_of(v):
                # package 71 (spec M7 §5): her light seen at night beyond the hull's loom, at
                # the range a lantern carries, as a sighting of its own
                out.append(
                    Sighting(
                        Feature(
                            f"light:{v.id}",
                            "light",
                            "a light",
                            v.position.lat_deg,
                            v.position.lon_deg,
                            modern=v.id,
                            height_m=v.height_m,
                        ),
                        bearing,
                        distance,
                        "light",
                    )
                )
        out.sort(key=lambda s: s.distance_m)
        return out

    def to_dict(self) -> list[dict[str, Any]]:
        return [v.to_dict() for v in self.vessels]


def _player_id() -> str:
    return PLAYER_ID


# The evolutions whose work in hand is a heaving to (the reading `the manoeuvre in hand`
# says "heaving to" for them, `api.readings.MANOEUVRE_WORDS`; package 84, step 11: read
# here from the ship, the world no reader of the api).
_HEAVING_TO_EVOLUTIONS = ("heave_to", "lie_a_try")


def _lying_to(world: Any) -> bool:
    """Whether the ship lies to or is heaving to, by the same rule as the reading `the
    manoeuvre in hand`: the evolution runner's work in hand first (the first instance not
    waiting names the manoeuvre), else the heave-to's record on the ship
    (`ship.extra["hove_to"]`, which filling away clears)."""
    extra = getattr(getattr(world, "ship", None), "extra", None) or {}
    runner = extra.get("evolutions")
    for inst in getattr(runner, "instances", None) or ():
        evo_id = str(getattr(getattr(inst, "evo", None), "id", "") or "")
        if evo_id and not getattr(inst, "waiting", False):
            return evo_id in _HEAVING_TO_EVOLUTIONS
    return "hove_to" in extra


def _sound_of(v: Vessel, nm: float) -> str:
    """What is heard of a far vessel in fog at this distance (package 71): 'a bell' at
    anchor within the mile, 'a gun' under way in company within three, 'a drum' alone
    within the mile, while she keeps the fog signals; '' otherwise."""
    from freesail.world.signals import BELL_HEARD_NM, GUN_HEARD_NM

    locker = getattr(v, "signals", None)
    if locker is None:
        return ""
    fog_gun = any(h.book == "fog" and h.down is None for h in locker.flying)
    if fog_gun and nm <= GUN_HEARD_NM:
        return "a gun"
    if not locker.fog_signals:
        return ""
    plan = getattr(v, "plan", None) or []
    at_anchor = bool(plan) and plan[0][0] == "anchor" or v.sail_state == "at anchor"
    if at_anchor:
        return "a bell" if nm <= BELL_HEARD_NM else ""
    if getattr(v, "under_orders_of", ""):
        return "a gun" if nm <= GUN_HEARD_NM else ""
    return "a drum" if nm <= BELL_HEARD_NM else ""


def _lights_of(v: Vessel) -> str:
    """The lights a far vessel shows by night (package 71): her locker's, or a fishing
    vessel's lantern at her gear (56's)."""
    locker = getattr(v, "signals", None)
    lights = str(getattr(locker, "lights", "") or "none") if locker is not None else "none"
    if lights != "none":
        return lights
    fishing = getattr(v, "fishing", None)
    out = getattr(fishing, "out", None) if fishing is not None else None
    return "a lantern at her nets" if out is not None and out.state == "fishing" else ""


def _size_of(v: Vessel) -> int:
    """A vessel's class for a cruiser's judgement of a superior force (package 43;
    `captains.SIZE_RANK`): by her description, or her file's where she has none (the
    pilot's cutter)."""
    from freesail.world.captains import SIZE_RANK, size_of_file

    if v.description:
        return SIZE_RANK.get(v.description, 0)
    return size_of_file(v.ship_file)


def _ship_speed_ms(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    if dyn is not None:
        return float(getattr(dyn, "speed", 0.0) or 0.0)
    return float(getattr(ship, "speed", 0.0) or 0.0)


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
