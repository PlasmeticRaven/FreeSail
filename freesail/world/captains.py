"""The rules-based captain (spec M6 §4; decision 40; package 40): intent, plan and
behaviour, in three layers, as a goal, a book and a few judgements.

What the game does when nobody is seated, made explicit: the captain holds the player's
ship when the player and every model are absent and the scenario gives an **intent**
instead of a book (`intent: trade tin from Falmouth to Brest`); a scenario with a book is
sailed by its book as it always was, the captain named and his book's name read but no
judgement of his given, so that the recorded passages do not move (truth 77). He is the
stand-in a model captain's book falls back on when the model's door is silent (the
harness lends the deck to the book and his judgements stand in, `Captain.stand_in`), and
the brain the far-detail body of `freesail.world.ships` resolves (`resolve_state`; the
crewed promotion is 43's).

- **Intent** (`Intent`): the goal and its parameters, read from words: trade a cargo from
  A to B, keep the station off a place within so many miles, carry a letter to a place,
  run home to a place, a passage bound for a place. A port's part is its stance (a port
  hostile to her nation is refused in words) and its tracks; the nation's part is who is
  an enemy (the strangers a King's ship chases, a merchant hauls off from).
- **The plan** (`Planner`, `Leg`): legs derived at sea from the intent over the chart's
  own data, never written in advance: the port's pilot station (its outer road) and its
  tracks (`tracks:` in the port file: `to_sea`, `from_sea` and `in`), the common tracks
  the features file names (`tracks:` beside `features:`), the straight line between
  tried against the shore and the charted dangers, a headland that stands in the way
  given an offing. Each leg is shaped with the player's own `shape a course for`, worked
  again every hour by a standing order the captain writes for the leg, and a course the
  wind will not allow is beaten by the rule the course's own judgement makes (package
  37m: kept full and by on the tack that points nearer, put about when the other tack
  makes better at the hour's shaping) with the offing kept by the beating book.
- **Behaviour** (`Captain`): a state machine whose states are books in the dialect,
  loaded on entering a state and unloaded on leaving it (`Runtime.load_book`): on
  passage, beating, hove to for weather, running for shelter, at anchor, in port,
  investigating a stranger, chasing, evading, keeping station, in distress, and
  engaging (present and empty until M7). A transition is an event the ship perceives,
  judged by the doctrine's table (`Doctrine.transitions`), once a minute.
- **Doctrine as data** (`data/captains/<role>.yaml`, `Doctrine`): the thresholds with
  their sources, the books of each state as templates, and the transitions, role by
  role: the King's ship on station, the merchant, the packet, the convoy's commodore
  (the fisherman is 43b's). The owner tunes it with a text editor, as the books.
- **Perception on the player's terms** (`Perception`): everything the captain judges by
  is a reading of the registry (`World.readings`), the account (`distance_to` by
  account), the chart in his hands (the features and the lines tried on it from the
  account) and the log he keeps; nothing here reads the world's truth, and
  `tests/test_captains.py` proves it as 37j's proof does for the readings.
- **The rule of the road as 1805 had it** (`Captain._rule_of_the_road`): at a few cables
  the ship close-hauled on the starboard tack stands on, the larboard-tack ship gives
  way under her stern, and a ship running keeps clear of one by the wind; a reflex said
  in the log once an encounter.

Every doing of the captain's goes through an order: `World.submit` with the actor
`captain's rule '<state>'` (`ACTOR_PREFIX`), which the World logs as "By the captain, on
passage: shaping a course for the Lizard." and does not journal, since a judgement is a
deterministic function of the seed and the journal, as a standing order's firing is; so
the log reads as a captain's, and a replay makes every judgement again.
"""

from __future__ import annotations

import functools
import math
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.events import Severity
from freesail.world.geo import (
    Position,
    bearing_and_distance,
    destination,
    format_position,
    parse_position,
)

__all__ = [
    "ACTOR_PREFIX",
    "CAPTAINS_DIR",
    "FAR_DETAIL_STATES",
    "INTENT_KINDS",
    "JUDGE_EVERY_S",
    "ROLES",
    "STATES",
    "Captain",
    "Doctrine",
    "Intent",
    "Judgement",
    "Leg",
    "Perception",
    "split_via",
    "way_marks",
    "Planner",
    "actor_for",
    "load_doctrine",
    "load_tracks",
    "plain_position",
    "read_intent",
    "role_for",
    "size_of_words",
    "size_rank_of",
    "state_of_actor",
]

# The doctrine files, one a role.
CAPTAINS_DIR = Path(__file__).resolve().parents[2] / "data" / "captains"

# The states of the machine, from the start (decision 40), engaging empty until M7.
STATES: tuple[str, ...] = (
    "on passage",
    "beating",
    "hove to for weather",
    "running for shelter",
    "at anchor",
    "in port",
    "investigating a stranger",
    "chasing",
    "evading",
    "keeping station",
    "in distress",
    "engaging",
    "struck",  # package 70: the colours down, lying to for her captor (what follows is 74's)
    # package 72 (spec M7 §21): a member of a squadron or a convoy at her station in the
    # set; the rows out of it are each role file's (docs/design/Design-Squadrons.md)
    "in company",
)

# The roles the doctrine files give; the cruiser (package 43) is the small man-of-war on
# passage, a brig-sloop or a cutter of the Navy, who makes out a stranger, chases what she
# can fight and hauls off from what she cannot; the fisherman (package 43b) works a
# fishing ground for a trip and goes home, at far detail only.
ROLES: tuple[str, ...] = (
    "kings-ship",
    "merchant",
    "packet",
    "commodore",
    "cruiser",
    "fisherman",
    "privateer",  # package 70: a letter of marque cruising for prizes
)

# The kinds of intent the captain reads (package 43b: `fish`, a trip to a fishing ground
# and home again, the world's business).
INTENT_KINDS: tuple[str, ...] = ("trade", "station", "letter", "home", "passage", "fish")

# The actor a judgement's order carries; the World knows it as a rule's and does not
# journal it (`core.world.RULES_ACTOR_PREFIXES`).
ACTOR_PREFIX = "captain's rule "

# The captain judges once a minute of ship's time, at the roll-up's cadence (spec M6 §4:
# "at far detail that is pairwise distance and visibility at the roll-up's cadence"; the
# lookout looks once a minute, and nothing he judges by changes faster). His first
# judgement waits five minutes from the start, so that the scenario's first orders (an
# anchor let go at tick 0 is brought up in a minute or two) have taken effect before he
# reads where she is (judgement).
JUDGE_EVERY_S = 60
JUDGE_FIRST_S = 300

# The states in which the rules-based captain keeps the deck himself over a seated officer
# (package 41, spec M6 §11: he takes it back "for a judgement that needs the deck"): the
# gale and the shelter, a stranger investigated, chased or evaded, distress, and the
# engagement to come; in the rest (in port, at anchor, on passage, beating, keeping
# station) the officer holds the deck under his book, as the Regulations' lieutenant
# kept the watch under the captain's directions (judgement on the states' kinds).
CAPTAIN_ON_DECK_STATES: frozenset[str] = frozenset(
    {
        "hove to for weather",
        "running for shelter",
        "investigating a stranger",
        "chasing",
        "evading",
        "in distress",
        "engaging",
    }
)

# The states the far-detail body resolves without a brain (spec M6 §4, "one brain, two
# bodies"; package 40): on passage is her plan, hove to is no way. A vessel with a brain
# (`brains.FarCaptain`, package 43) resolves every state of the machine
# (`brains.resolve_state`); the brain lives in `freesail.world.brains`, apart from this
# module, which reads no truth (see `tests/test_captains.py`).
FAR_DETAIL_STATES: tuple[str, ...] = ("on passage", "hove to for weather", "in company")

# The class of a hull by what the tops make out of her, for the cruiser's judgement of a
# superior force (`overmatched`): a frigate over a brig over a schooner or a cutter
# (judgement on the catalogue's hierarchy of size, spec M5 §25; the guns are M7's).
# The lookout's words that mark a man of war (package 70: the privateer's fear of one, and
# the merchant's); judgement on the words `world/ships.py` gives a sail made out.
MAN_OF_WAR_WORDS: tuple[str, ...] = (
    "of war",
    "frigate",
    "sloop",
    "revenue",
    "king's",
    "man of war",
    "ship of the line",
)

# The nation's habit in action over the role's figures (spec M7 §9, §10: "the British
# close, the French at long shot"; the aim at the hull or the rigging; the roll fired on)
# is each nation's `habits:` entry in data/nations.yaml (package 71, the owner's word of
# 2026-10-24: 70's table in this module moved to the nations' data file, read through
# `world.nations.habits_of` by `Captain._habit`).

# The range a weaker mark is closed to in action (pistol shot, a third of a cable;
# judgement after the chases' record: the chaser ranges alongside).
CLOSE_RANGE_M = 60.0
# The engaging helm's margin off the close-hauled angle (package 71, item 8: the owner's
# first action, where 70's law steered by the mark's bearing alone and turned the King's
# cutter through the wind's eye, aback with her carronades silent for half an hour): no
# course in action is ordered nearer the wind than close-hauled and this, the same half
# point the course-shaping's own rule keeps (`navigation.COURSE_NOT_LAID_MARGIN_POINTS`).
ENGAGING_WIND_MARGIN_POINTS = 0.5
# The law's switch, for the bisection of what it moved (the tuning notes, package 71): off,
# 70's course by the mark's bearing alone is given again.
HELM_IN_ACTION = True


def helm_in_action(
    heading_deg: float,
    wind_from_deg: float,
    closest_deg: float,
    bearing_deg: float,
    side: str,
    ratio: float,
    gage: str = "weather",
) -> tuple[float, str]:
    """The engaging helm's course (package 71, item 8; spec M7 §10): the beam law of
    70 (the mark kept on the engaged beam, before it to close and abaft it to open, a
    straight law of the range over the wanted), **never within the ship's close-hauled
    angle and half a point of the wind's eye** (the course clamped to the close-hauled
    course on the tack her head is on, as `navigation._chase_course` clamps a chase), and
    the gage the doctrine names kept where the geometry allows: under `weather`, a mark to
    windward is worked up to by the wind on the tack that points nearer her rather than
    by the beam law that falls off to leeward; under `lee`, a mark to leeward the same
    the other way. Returns (the course true, degrees; the word for the log: '' for the
    beam law, 'as near the wind as she will lie' for the clamp, 'to keep the weather
    gage' or 'to take it'), and never a course across the eye: when the beam law wants
    the other tack the course is the close-hauled course on this one and the word says
    'the mark through the eye', for the doctrine's `through_the_eye` to answer."""
    sign = 1.0 if side == "starboard" else -1.0
    off = max(35.0, min(125.0, 90.0 + 55.0 * (1.0 - ratio)))
    course = (bearing_deg - sign * off) % 360.0
    word = ""
    point = units.rad_to_deg(units.POINT)
    edge = float(closest_deg) + ENGAGING_WIND_MARGIN_POINTS * point
    head_side = 1.0 if _signed_off(heading_deg, wind_from_deg) >= 0.0 else -1.0
    mark_off = _signed_off(bearing_deg, wind_from_deg)  # the mark's bearing from the eye
    windward = abs(mark_off) < 90.0
    if gage == "weather" and windward and ratio > 1.0:
        # she lies to windward of us and we have ground to make: by the wind on the tack
        # whose head points nearer her, which is the course that gains it
        toward = 1.0 if mark_off >= 0.0 else -1.0
        if toward == head_side:
            course = (wind_from_deg + toward * edge) % 360.0
            word = "by the wind, to take the weather gage"
    elif gage == "lee" and not windward and ratio > 1.0:
        toward = 1.0 if mark_off >= 0.0 else -1.0
        course = (bearing_deg - sign * min(off, 70.0)) % 360.0
        word = "to keep the lee gage"
    course_off = _signed_off(course, wind_from_deg)
    if abs(course_off) < edge:
        # within the close-hauled angle: the close-hauled course on her own tack
        course_side = 1.0 if course_off >= 0.0 else -1.0
        course = (wind_from_deg + head_side * edge) % 360.0
        word = (
            "as near the wind as she will lie; the mark through the eye"
            if course_side != head_side
            else "as near the wind as she will lie"
        )
    elif (1.0 if course_off >= 0.0 else -1.0) != head_side and abs(course_off) < 90.0:
        # the beam law wants the other tack by the wind's eye: never a course across it
        # from here; the close-hauled course on this tack, and the doctrine answers
        course = (wind_from_deg + head_side * edge) % 360.0
        word = "as near the wind as she will lie; the mark through the eye"
    return course, word


def _signed_off(course_deg: float, wind_from_deg: float) -> float:
    """The course's angle from the wind's eye, degrees, positive with the wind on her
    larboard side (her head to starboard of the eye)."""
    return units.rad_to_deg(units.wrap_pi(math.radians(course_deg - wind_from_deg)))


SIZE_RANK: dict[str, int] = {
    "frigate": 3,
    "brig-sloop": 2,
    "merchant brig": 2,
    "schooner": 1,
    "cutter": 1,
    "lugger": 1,  # package 43b: a chasse-marée of a hundred tons, the cutter's class
    "smack": 0,  # a fishing smack of thirty-five tons is nobody's match
}
_SIZE_WORDS: tuple[tuple[str, int], ...] = (
    ("frigate", 3),
    ("a ship", 3),
    ("brig", 2),
    ("schooner", 1),
    ("cutter", 1),
    ("lugger", 1),
    ("chasse-mar", 1),
    ("smack", 0),
)


def size_of_words(known: str) -> int:
    """The class of a sail from the lookout's words for her ('a brig-sloop of war,
    sixteen ports a side, standing ...'): nought while she is 'a sail'."""
    head = str(known or "").split(",")[0].split(";")[0].lower()
    for word, rank in _SIZE_WORDS:
        if word in head:
            return rank
    return 0


def size_rank_of(words: str) -> int | None:
    """The class of a hull by any words that name her ('brig', 'a French frigate', 'a
    brig-sloop of war'), ranked as the tops rank a sail (`_SIZE_WORDS`); None where the
    words name no class (package 68; the cold review's R-38: the brief's limit "brig" was
    looked up by the `SIZE_RANK` keys inside it, none of which "brig" holds, so a French
    frigate passed a brief of no enemy heavier than a brig)."""
    said = " ".join(str(words or "").lower().replace("\u2019", "'").split())
    if not said:
        return None
    padded = f"a {said.removeprefix('a ').removeprefix('an ').removeprefix('the ')}"
    for word, rank in _SIZE_WORDS:
        if word in padded:
            return rank
    return None


def size_of_file(ship_file: Any) -> int:
    """The class of the player's own ship by her file (`ships.DESCRIPTIONS`)."""
    from freesail.world.ships import DESCRIPTIONS

    name = Path(str(ship_file or "")).name
    for key, d in DESCRIPTIONS.items():
        if Path(d["file"]).name == name:
            return SIZE_RANK.get(key, 0)
    return 0


# The rule of the road's reach: a few cables (judgement; the hail is at four).
ROAD_CABLES = 3.0
# By the wind: within this of the wind's eye (six points, where every rig lies
# close-hauled in the judgement of package 37m, and a point of freedom); running: the
# wind abaft this.
BY_THE_WIND_DEG = 78.75
RUNNING_DEG = 135.0

# What a planner's straight line keeps off the shore and the dangers: a headland is
# given an offing of a league (judgement; the merchant book gives the open sea's marks a
# berth of two or three miles), a charted danger a mile (`chart.DANGER_PASS_NM`'s kin).
OFFING_NM = 3.0
DANGER_BERTH_NM = 1.0
# A planner's search stops after this many headlands have been cleared on one leg.
PLANNER_ROUNDS = 6
# In port, by the captain's account: at anchor within this of the port's roads (the
# port's own rule at the truth is `ports.IN_PORT_NM`, two miles; the same figure).
IN_PORT_NM = 2.0

# The entry (package 45, Part B item 3a; the owner's note 8: two entrances balked with the
# wind on the beam): a leg of a port's inner track is sailed when it lies no nearer the
# wind than this many points; the captain goes in as far as the legs serve and anchors
# at the last anchorage he can reach. Six points: a square-rigged merchantman's full and
# by with a little in hand for the stream (Fincham's "seldom within six points").
ENTRY_POINTS = 6.0

# Sail after the gale (Part B item 5; 37p's open point): the wind under `sail_again_kn`
# for `sail_again_minutes` and he makes sail again whatever his state; a head sail blown
# out of its bolt-ropes is replaced from the sail room when the wind is under
# `wear_wind_kn`. The glass (Part B item 6; the owner's note 4c): the wind's trend over
# the hour is kept here, since no reading gives it.
TREND_HOUR_S = 3600
# The land to leeward (Part B, the gale trial): the lee sector is six points either side
# of dead to leeward (as the doctrine's rows always had it), and the land within it is
# the nearest the chart's coast comes along rays of `LEE_RAY_NM` cast through the sector a
# point apart from the account. A first version read the nearest coast point and its
# bearing alone, and off Ushant two shores lie near-equidistant, one to leeward and one
# not: the nearest flipped between them minute by minute, and the captain hove to and
# filled away by turns (fifty state changes in the forenoon). Twelve miles is past every
# doctrine's sea room.
LEE_SECTOR_POINTS = 6
LEE_RAY_NM = 12.0
# The anchorage is taken at the first cast under this many fathoms within the book's
# reach of its mark, where the port's file gives its anchorage no depth (the merchant
# book's twelve for the Bay of Brest: Faden's eight, ten or sixteen on mud); with a
# depth given, two fathoms over it.
ANCHORAGE_FATHOMS = 12

# A leg re-laid as the stream changes (package 58b, item 1; the Éclair's first cruise: the
# leg laid on the flood was held through the ebb into the eastern narrows of the channel of
# Bas, and off Fréhel the way laid with the flood allowed at a knot and a half to the
# north-east was held while it eased to half a knot, which "would have closed Fréhel in the
# middle watch"). A course shaped allows the stream the master allows at that hour and no
# other (`Navigation.shape_for`: "worked once, when the course is shaped"), so the captain
# lays the leg again when the master's tide turns or she passes by his account into other
# waters (his `reckoning.tide` line), and when the stream he allows now would carry her off
# the line by more than `RELAY_OFF_LINE_NM` in the next glass beyond what the course laid
# allowed for; on passage and running for shelter (beating, his book shapes every glass),
# never twice within `RELAY_LEAST_S`. Judgement: a cable, the berth a pilot water's mark
# is passed within; a glass, his book's own interval.
RELAY_OFF_LINE_NM = 0.1
RELAY_GLASS_H = 0.5
RELAY_LEAST_S = 1800  # a glass between layings for the stream's change
RELAY_TURN_LEAST_S = 600  # ten minutes for the tide's turn (a course shaped at the turn holds)


def actor_for(state: str) -> str:
    return f"{ACTOR_PREFIX}'{state}'"


def state_of_actor(actor: str) -> str | None:
    """The state a judgement's actor names, or None for any other actor."""
    if not str(actor).startswith(ACTOR_PREFIX):
        return None
    return str(actor)[len(ACTOR_PREFIX) :].strip("'")


# ---------------------------------------------------------------------------
# Intent
# ---------------------------------------------------------------------------


@dataclass
class Intent:
    """The goal and its parameters, as read from words. `kind` is one of
    `INTENT_KINDS`; `origin` and `destination` are port ids where the chart has the port,
    else a feature's id or a pricked position's words; `cargo` and `tons` for a trade;
    `radius_nm` for a station; `between` the station's bounds in words, kept."""

    kind: str
    words: str
    cargo: str = ""
    tons: float | None = None
    origin: str = ""
    destination: str = ""
    radius_nm: float = 5.0
    between: str = ""
    done: bool = False
    via: tuple[str, ...] = ()  # the marks sailed by on the way, in order (package 45)
    # package 43b: a fishing trip's hours on the ground; `origin` is then her home port
    hours: float | None = None
    # package 70: a station cruised for prizes (a letter of marque's), the privateer's role
    prizes: bool = False
    # package 71: a passage made as a convoy's escort (`convoy the trade from A to B`), the
    # commodore's role; the merchantmen under his orders are the scenario's
    convoy: bool = False
    # package 72: a station that is a blockade of the port named (`blockade Brest`)
    blockade: str = ""

    def to_dict(self) -> dict[str, Any]:
        return (
            {
                "kind": self.kind,
                "words": self.words,
                "cargo": self.cargo,
                "tons": self.tons,
                "origin": self.origin,
                "destination": self.destination,
                "radius_nm": self.radius_nm,
                "done": self.done,
                "via": list(self.via),
            }
            | ({"hours": self.hours} if self.hours is not None else {})
            | ({"prizes": True} if self.prizes else {})
            | ({"blockade": self.blockade} if self.blockade else {})
        )


# `via` in an intent or a course (package 45): `trade tin from Falmouth to Lisbon via
# Ushant, Finisterre`, `shape a course for Lisbon via Ushant and Finisterre`; the marks
# are features by name or positions pricked on the chart, sailed in order.
_VIA = re.compile(r"\s+via\s+", re.IGNORECASE)
_VIA_SPLIT = re.compile(r"\s*,\s*|\s+and\s+then\s+|\s+then\s+|\s+and\s+", re.IGNORECASE)


def split_via(words: str, world: Any = None) -> tuple[str, list[str]]:
    """The destination's words and the marks after `via`, in order; no marks when the
    words have no `via`. The marks are parted at commas, `and` and `then`; where an
    order's grammar has dropped the commas ('via ushant finisterre'), the words are
    parted into the marks the chart knows, greedily from the left, when `world` is
    given."""
    parts = _VIA.split(str(words).strip(), maxsplit=1)
    if len(parts) == 1:
        return parts[0].strip(), []
    marks = [m.strip().rstrip(".") for m in _VIA_SPLIT.split(parts[1]) if m.strip(" .")]
    if world is not None:
        parted: list[str] = []
        for m in marks:
            parted += _part_marks(world, m) if _mark(world, m) is None else [m]
        marks = parted
    return parts[0].strip(), marks


def _part_marks(world: Any, words: str) -> list[str]:
    """Words naming several marks run together, parted into the marks the chart knows,
    the longest first from the left ('ushant finisterre', 'the lizard 48 20 n 4 36 w');
    the words whole when no parting works (the caller refuses them)."""
    tokens = words.split()
    out: list[str] = []
    i = 0
    while i < len(tokens):
        taken = None
        for j in range(len(tokens), i, -1):
            cand = " ".join(tokens[i:j])
            if _mark(world, cand) is not None:
                taken = (cand, j)
                break
        if taken is None:
            return [words]
        out.append(taken[0])
        i = taken[1]
    return out


# A mark sailed by (`via`) that is land or a danger is given a berth to seaward: the
# point `VIA_BERTH_NM` from it on the bearing with the most sea room about the mark, among
# equals the one toward the hand the straight line from the mark before to the mark after
# puts it, and moved out until the shore is the planner's offing from the point; the mark
# is then left on the hand the point puts it. A mark that is water (a road, an anchorage,
# a sounding, a transit, a named stretch of sea or a pricked position) is sailed to itself.
WATER_KINDS = frozenset({"anchorage", "road", "bottom", "transit", "place"})
WAY_BEARINGS = 16
WAY_FAR_NM = 8.0  # the second read of the sea room about a mark (judgement: three leagues)
# The berth given a mark sailed by: five miles (Norie 1805 and the Channel pilots give
# Ushant "a berth of two or three leagues"; the planner's offing of a league is a headland's
# on a coast, where a cape is passed closer; judgement between them), moved out by miles
# until the shore is the planner's offing from the point itself.
VIA_BERTH_NM = 5.0
WAY_OUT_STEPS_NM = (0.0, 1.0, 2.0, 3.0, 4.0)


def way_marks(
    world: Any, start: Position, marks: list[str], end: Position | None
) -> list[tuple[str, Position, str]]:
    """The waypoints of a way by marks (package 45): for each mark in order, the words an
    order takes for the point to shape for, its position, and the hand it is left on
    ('leaving Ushant to larboard, a league to the westward of it'; '' for a mark sailed
    to). Refused in words (ValueError) for a mark the chart has not got. No routing
    between one point and the next: the straight line, as the plan's."""
    chart = getattr(world, "chart", None)
    found: list[tuple[str, Position, Any]] = []
    for words in marks:
        m = _mark(world, words)
        if m is None:
            raise ValueError(f"'{words}' names no mark of the chart to sail by.")
        f = chart.find_feature(" ".join(str(words).split())) if chart is not None else None
        if f is None and chart is not None:
            f = chart.feature(str(words).strip())
        found.append((m[0], m[1], f))
    out: list[tuple[str, Position, str]] = []
    before = start
    for i, (name, pos, f) in enumerate(found):
        after = found[i + 1][1] if i + 1 < len(found) else end
        if f is None or f.kind in WATER_KINDS or chart is None:
            out.append((name, pos, ""))
            before = pos
            continue
        if after is None:
            after = pos
        brg_line, _ = bearing_and_distance(before, after)
        brg_mark, d_mark = bearing_and_distance(before, pos)
        off_line = d_mark * math.sin(math.radians(brg_mark - brg_line))  # + to starboard
        # the perpendicular from the mark toward the line: the hand the line prefers
        prefer = (brg_line - 90.0) % 360.0 if off_line > 0 else (brg_line + 90.0) % 360.0
        toward = _seaward_bearing(chart, pos, prefer)
        point = units.point_name(math.radians(toward), full=True)
        toward = units.rad_to_deg(units.parse_course(point))
        miles = VIA_BERTH_NM
        for step in WAY_OUT_STEPS_NM:
            at = destination(pos, toward, (VIA_BERTH_NM + step) * units.NAUTICAL_MILE)
            miles = VIA_BERTH_NM + step
            if _sea_room_m(chart, at) >= OFFING_NM * units.NAUTICAL_MILE:
                break
        brg_w, _ = bearing_and_distance(before, at)
        side = math.sin(math.radians(brg_mark - brg_w))
        hand = "starboard" if side > 0 else "larboard"
        how_far = "a league" if miles == 3.0 else f"{int(miles)} miles"
        words = f"{how_far} {point} of {name}"
        said = f"leaving {name} to {hand}, {how_far} to the {_toward_words(toward)} of it"
        out.append((words, at, said))
        before = at
    return out


def _sea_room_m(chart: Any, at: Position) -> float:
    try:
        found = chart.coast_distance(at)
    except Exception:  # noqa: BLE001 - beyond the chart's field
        return math.inf
    return math.inf if found is None else float(found[0])


def _seaward_bearing(chart: Any, place: Position, prefer_deg: float) -> float:
    """The bearing from a mark toward the most sea room, over `WAY_BEARINGS` bearings: the
    room read `OFFING_NM` off the mark and again `WAY_FAR_NM` off it, summed to the nearest
    mile (a league off a cape every side but the land's reads much the same; three leagues
    off, the bay behind it is shore and the sea is open), and among equals the bearing
    nearest `prefer_deg` (as `station_off` finds a station, to the westward among equals)."""
    best: tuple[float, float, float] | None = None
    cap = 30.0 * units.NAUTICAL_MILE
    for i in range(WAY_BEARINGS):
        bearing = 360.0 * i / WAY_BEARINGS
        room = 0.0
        for radius_nm in (OFFING_NM, WAY_FAR_NM):
            there = destination(place, bearing, radius_nm * units.NAUTICAL_MILE)
            room += min(_sea_room_m(chart, there), cap)
        near = math.cos(math.radians(bearing - prefer_deg))
        key = (round(room / units.NAUTICAL_MILE), near)
        if best is None or key > (best[0], best[1]):
            best = (key[0], key[1], bearing)
    return best[2] if best is not None else prefer_deg


def _toward_words(bearing_deg: float) -> str:
    names = ("northward", "eastward", "southward", "westward")
    return names[int(((bearing_deg + 45.0) % 360.0) // 90.0)]


_TRADE = re.compile(
    r"^trade\s+(?:(?P<tons>[\w-]+)\s+tons?\s+of\s+)?(?P<cargo>[\w' -]+?)\s+from\s+(?P<a>.+?)\s+"
    r"(?:to|for)\s+(?P<b>.+)$"
)
_STATION = re.compile(
    r"^(?:keep (?:the )?station|cruise|patrol)"
    r"(?P<prizes>\s+for\s+prizes|\s+against\s+(?:the\s+)?(?:enemy'?s?\s+)?trade)?"
    r"\s+off\s+(?P<place>.+?)"
    r"(?:\s+within\s+(?P<radius>[\d.]+)\s+miles?)?(?:\s+between\s+(?P<between>.+))?$"
)
_LETTER = re.compile(
    r"^carry\s+(?:this|a|the)\s+(?:letter|message|dispatch|despatch)\s+to\s+(?P<b>.+)$"
)
_HOME = re.compile(r"^run\s+home\s+(?:to|for)\s+(?P<b>.+)$")
# package 43b: `fish on the Eddystone ground for 20 hours from Plymouth`
_FISH = re.compile(
    r"^fish\s+(?:on|at|over)\s+(?P<ground>.+?)(?:\s+within\s+(?P<radius>[\d.]+)\s+miles?)?"
    r"\s+for\s+(?P<hours>[\d.]+)\s+hours?\s+(?:from|out\s+of)\s+(?P<home>.+)$"
)
_PASSAGE = re.compile(r"^(?:bound|passage|sail)\s+(?:from\s+(?P<a>.+?)\s+)?(?:for|to)\s+(?P<b>.+)$")
# package 71: the convoy's commodore ('convoy the trade from Falmouth to the Start', 'escort
# the convoy to Plymouth'): a passage with the commodore's doctrine
_CONVOY = re.compile(
    r"^(?:convoy|escort)\s+(?:the\s+)?(?:trade|convoy|merchantmen|ships|fleet)?\s*"
    r"(?:from\s+(?P<a>.+?)\s+)?(?:for|to)\s+(?P<b>.+)$"
)
# package 72 (spec M7 §22): the blockade's station, off the port's outer road ('blockade
# Brest', 'blockade Brest within 6 miles'): a station intent whose place is the road's feature
_BLOCKADE = re.compile(
    r"^blockade\s+(?:the\s+port\s+of\s+)?(?P<port>.+?)(?:\s+within\s+(?P<radius>[\d.]+)\s+miles?)?$"
)


def read_intent(world: Any, words: str) -> Intent:
    """An intent from its words, the places checked against the chart and the ports
    (raises ValueError in words): `trade tin from Falmouth to Brest`, `trade forty tons
    of tin from Falmouth to Brest`, `keep the station off Ushant within 15 miles`, `carry
    this letter to Brest`, `run home to Plymouth`, `bound for Brest`."""
    from freesail.orders.numbers import read_all

    said = " ".join(str(words).split()).rstrip(".")
    text = said.lower()

    def group(m: re.Match[str], name: str) -> str:
        return said[m.start(name) : m.end(name)] if m.group(name) else ""

    def to_and_via(words: str) -> tuple[str, tuple[str, ...]]:
        # the marks sailed by on the way (package 45), each checked against the chart
        dest, marks = split_via(words, world)
        for mark in marks:
            if _mark(world, mark) is None:
                raise ValueError(f"'{mark}' names no mark of the chart to sail by, in '{said}'.")
        return _place_id(world, dest), tuple(marks)

    m = _TRADE.match(text)
    if m:
        tons = None
        if m.group("tons"):
            tons = read_all(m.group("tons"))
            if tons is None:
                raise ValueError(f"'{m.group('tons')}' is no number of tons in '{words}'.")
        a = _place_id(world, group(m, "a"))
        b, via = to_and_via(group(m, "b"))
        return Intent(
            "trade",
            said,
            cargo=m.group("cargo").strip(),
            tons=tons,
            origin=a,
            destination=b,
            via=via,
        )
    m = _STATION.match(text)
    if m:
        place = _place_id(world, group(m, "place"))
        radius = float(m.group("radius") or 5.0)
        return Intent(
            "station",
            said,
            destination=place,
            radius_nm=radius,
            between=group(m, "between"),
            prizes=bool(m.group("prizes")),
        )
    m = _LETTER.match(text)
    if m:
        b, via = to_and_via(group(m, "b"))
        return Intent("letter", said, destination=b, via=via)
    m = _HOME.match(text)
    if m:
        b, via = to_and_via(group(m, "b"))
        return Intent("home", said, destination=b, via=via)
    m = _FISH.match(text)
    if m:
        # a fishing trip (package 43b): to the ground, worked as a station of a mile or two
        # for the hours, and home to the port she sailed from
        ground = _place_id(world, group(m, "ground"))
        home = _place_id(world, group(m, "home"))
        return Intent(
            "fish",
            said,
            origin=home,
            destination=ground,
            radius_nm=float(m.group("radius") or 1.5),
            hours=float(m.group("hours")),
        )
    m = _CONVOY.match(text)
    if m:
        a = _place_id(world, group(m, "a")) if m.group("a") else ""
        b, via = to_and_via(group(m, "b"))
        return Intent("passage", said, origin=a, destination=b, via=via, convoy=True)
    m = _BLOCKADE.match(text)
    if m:
        ports = getattr(world, "ports", None)
        port = ports.find(group(m, "port")) if ports is not None and ports.ports else None
        if port is None:
            raise ValueError(f"'{group(m, 'port')}' is no port of the chart to blockade.")
        # the port's own blockade station (data/ports/<port>.yaml `blockade_station`, off
        # the approach: Brest's off the Black Rocks), else its outer road
        station = dict(getattr(port, "blockade_station", None) or {})
        feature = str(station.get("feature") or getattr(port.outer_road, "feature_id", "") or "")
        chart = getattr(world, "chart", None)
        if not feature or chart is None or chart.feature(feature) is None:
            raise ValueError(
                f"the port of {port.name} has no blockade station or outer road on the chart."
            )
        from freesail.world.regimes import regime_knob

        radius = float(
            m.group("radius")
            or station.get("within_nm")
            or regime_knob("on blockade", "inshore_nm", 6.0)
        )
        intent = Intent("station", said, destination=feature, radius_nm=radius, between=port.id)
        intent.blockade = port.id
        return intent
    m = _PASSAGE.match(text)
    if m:
        a = _place_id(world, group(m, "a")) if m.group("a") else ""
        b, via = to_and_via(group(m, "b"))
        return Intent("passage", said, origin=a, destination=b, via=via)
    raise ValueError(
        f"'{words}' is no intent a captain knows: say 'trade <cargo> from <A> to <B>', 'keep "
        "the station off <place> within <n> miles', 'carry this letter to <place>', 'run "
        "home to <place>', 'bound for <place>' or 'convoy the trade from <A> to <B>'."
    )


def _place_id(world: Any, words: str) -> str:
    """A port's id, a feature's id or a pricked position's words, for a place named in an
    intent; refused in words when the chart knows no such place."""
    text = " ".join(str(words).split()).strip(" .")
    ports = getattr(world, "ports", None)
    port = ports.find(text) if ports is not None and getattr(ports, "ports", None) else None
    if port is not None:
        return port.id
    chart = getattr(world, "chart", None)
    if chart is not None:
        feature = chart.find_feature(text)
        if feature is not None:
            return feature.id
        # a fishing ground of the tables (package 56): its feature, or where it is pricked
        from freesail.world.fishing import find_ground

        ground = find_ground(world, text)
        if ground is not None:
            return ground.feature or plain_position(ground.position)
    try:
        return format_position(parse_position(text))
    except ValueError:
        raise ValueError(f"the chart knows no place named '{text}'") from None


# ---------------------------------------------------------------------------
# Doctrine as data
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Transition:
    """One row of a doctrine's table: from a state, on a stimulus, to a state, unless
    another stimulus holds."""

    frm: str
    on: str
    to: str
    unless: str = ""


@dataclass(frozen=True)
class Doctrine:
    """A role's doctrine as read: the thresholds (each with its source beside it), the
    books of each state as templates in the dialect, and the transitions in order."""

    role: str
    name: str
    path: str
    thresholds: dict[str, Any]
    sources: dict[str, str]
    books: dict[str, tuple[str, ...]]
    transitions: tuple[Transition, ...]

    def threshold(self, key: str, default: Any = None) -> Any:
        return self.thresholds.get(key, default)

    def book(self, state: str) -> tuple[str, ...]:
        return self.books.get(state, ())

    def from_state(self, state: str) -> list[Transition]:
        return [t for t in self.transitions if t.frm == state]


@functools.lru_cache(maxsize=8)
def _doctrine(path: str) -> Doctrine:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    role = str(raw.get("role") or Path(path).stem)
    thresholds: dict[str, Any] = {}
    sources: dict[str, str] = {}
    for key, entry in (raw.get("thresholds") or {}).items():
        if isinstance(entry, dict):
            thresholds[str(key)] = entry.get("value")
            sources[str(key)] = str(entry.get("source") or "")
        else:
            thresholds[str(key)] = entry
            sources[str(key)] = ""
    books: dict[str, tuple[str, ...]] = {}
    for state, lines in (raw.get("books") or {}).items():
        if state not in STATES:
            raise ValueError(f"{path}: '{state}' is no state of the machine ({', '.join(STATES)}).")
        books[str(state)] = tuple(" ".join(str(ln).split()) for ln in (lines or []))
    transitions = []
    for i, t in enumerate(raw.get("transitions") or []):
        if isinstance(t, dict):
            # YAML 1.1 reads a bare `on:` as the boolean key True
            t = {("on" if k is True else str(k)): v for k, v in t.items()}
        if not isinstance(t, dict) or not all(k in t for k in ("from", "on", "to")):
            raise ValueError(f"{path}, transitions {i + 1}: from, on and to.")
        for key in ("from", "to"):
            if t[key] not in STATES:
                raise ValueError(f"{path}, transitions {i + 1}: '{t[key]}' is no state.")
        transitions.append(
            Transition(str(t["from"]), str(t["on"]), str(t["to"]), str(t.get("unless") or ""))
        )
    return Doctrine(
        role, str(raw.get("name") or role), path, thresholds, sources, books, tuple(transitions)
    )


def load_doctrine(role: str) -> Doctrine:
    """The doctrine of a role (`data/captains/<role>.yaml`), read once."""
    path = CAPTAINS_DIR / f"{role}.yaml"
    if not path.is_file():
        raise ValueError(
            f"There is no doctrine for the role '{role}'; the roles: {', '.join(ROLES)}."
        )
    return _doctrine(str(path))


def role_for(world: Any, intent: Intent | None) -> str:
    """The role a ship's captain plays by her and her intent: a King's ship on station
    or bound for one is `kings-ship`; a letter carried is the packet's; a convoy's
    commodore is named by the intent; the rest trade."""
    if intent is not None and intent.kind == "station":
        return "privateer" if intent.prizes else "kings-ship"
    if intent is not None and intent.kind == "letter":
        return "packet"
    if intent is not None and intent.convoy:
        return "commodore"  # package 71: the convoy's escort, by the intent's words
    if intent is not None and intent.kind in ("home", "passage") and _is_kings_ship(world):
        return "kings-ship"
    return "merchant"


def _is_kings_ship(world: Any) -> bool:
    """A King's ship by her wardroom file's binding of the captain's station (package
    40c): a captain or a commander commands her; a master commands a merchantman or a
    hired cutter. Read from the file by the ship's own source, never by building the
    people: the captain is made with the World, before her company is mustered, and a
    muster built then would be a point ship's (a captain and the master alone)."""
    from freesail.world.people import load_wardroom

    spec = getattr(getattr(world, "ship", None), "spec", None)
    source = getattr(spec, "source", None)
    role = None
    if source:
        try:
            wardroom = load_wardroom(str(source))
        except ValueError:
            wardroom = None
        role = wardroom.role_of("captain") if wardroom is not None else None
    return role in ("captain", "commander")


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


@dataclass
class Leg:
    """One leg of the plan: a mark to shape a course for, in the words the order takes
    (a feature of the chart by its name, or a position pricked on it), its position, its
    kind (`to` a mark at sea, `road` a port's outer road where the tide is waited for,
    `anchorage` the port's anchorage where she comes to) and how near by account counts
    as reached."""

    words: str
    position: Position
    kind: str = "to"
    reached_nm: float = 2.0
    port: str = ""  # the port a road or an anchorage belongs to
    said: str = ""  # the leg in words for the log

    def to_dict(self) -> dict[str, Any]:
        return {
            "words": self.words,
            "kind": self.kind,
            "port": self.port,
            "reached_nm": self.reached_nm,
        }


@dataclass(frozen=True)
class Track:
    id: str
    name: str
    marks: tuple[tuple[str, Position], ...]  # (the words, the position) of each mark
    source: str = ""


def plain_position(p: Position) -> str:
    """A position in the plain form the dialect and the orders both read ('48 16.5 N 4
    48.0 W'), to a tenth of a minute: the books' own form for a point pricked on the
    chart (`format_position` writes the log's form, with the degree sign, which the
    dialect's `the distance to` does not read)."""

    def dm(value: float, pos: str, neg: str) -> str:
        hemi = pos if value >= 0 else neg
        value = abs(value)
        d = int(value)
        m = (value - d) * 60.0
        if m >= 59.95:
            d, m = d + 1, 0.0
        return f"{d} {m:04.1f} {hemi}"

    return f"{dm(p.lat_deg, 'N', 'S')} {dm(p.lon_deg, 'E', 'W')}"


# A station "off" a place (package 40c, the captain's trials): the place itself is the land
# (Ushant), and a course shaped for it runs her ashore. The station is the point the
# intent's radius from the place with the most sea room about it, read on the chart in
# his hands (the distance to the nearest shore at each of sixteen bearings, the farthest
# taken; ties to the westward, the open Atlantic's side), as the squadron's station lay
# to seaward of the Black Rocks.
STATION_BEARINGS = 16


def station_off(world: Any, place: Position, radius_nm: float) -> Position:
    chart = getattr(world, "chart", None)
    best: tuple[float, float, Position] | None = None
    for i in range(STATION_BEARINGS):
        bearing_deg = 360.0 * i / STATION_BEARINGS
        there = destination(place, bearing_deg, radius_nm * units.NAUTICAL_MILE)
        room = math.inf
        if chart is not None:
            try:
                found = chart.coast_distance(there)
            except Exception:  # noqa: BLE001 - beyond the chart's field
                found = None
            if found is not None:
                room = float(found[0])
        # the room to the nearest league, and among equals the westward bearing (the
        # open Atlantic's side, where the squadron's station lay)
        west = -math.sin(math.radians(bearing_deg))
        key = (round(room / (3.0 * units.NAUTICAL_MILE)), west)
        if best is None or key > (best[0], best[1]):
            best = (key[0], key[1], there)
    return best[2] if best is not None else place


def _mark(world: Any, words: str) -> tuple[str, Position] | None:
    """A track's mark: a feature by its id or name (its name is the order's words), or a
    pricked position (its words as the data gives them are the order's, in the plain
    form the dialect reads)."""
    chart = getattr(world, "chart", None)
    text = " ".join(str(words).split())
    if chart is not None:
        f = chart.feature(text) or chart.find_feature(text)
        if f is not None:
            return f.name, f.position
    try:
        p = parse_position(text)
    except ValueError:
        return None
    return (text if "°" not in text else plain_position(p)), p


def load_tracks(world: Any) -> list[Track]:
    """The common tracks the features files name (`tracks:` beside `features:` in each
    region's file: an id, a name, a source and the marks in order), read through the
    chart's manifest; none for a world without a chart."""
    chart = getattr(world, "chart", None)
    if chart is None:
        return []
    cache = getattr(chart, "_tracks", None)
    if cache is not None:
        return cache
    out: list[Track] = []
    for r in getattr(chart, "regions", ()):
        spec = chart.region_specs.get(r) or {}
        path = chart.root / str(spec.get("features") or "")
        if not spec.get("features") or not path.exists():
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for t in doc.get("tracks") or []:
            marks = []
            for words in t.get("marks") or []:
                m = _mark(world, str(words))
                if m is None:
                    raise ValueError(
                        f"{path}, track '{t.get('id')}': the chart has no mark '{words}'."
                    )
                marks.append(m)
            out.append(
                Track(
                    str(t.get("id")),
                    str(t.get("name") or t.get("id")),
                    tuple(marks),
                    str(t.get("source") or ""),
                )
            )
    chart._tracks = out
    return out


def _off_the_land(chart: Any, head: Position, where: Position, offing_nm: float) -> Position | None:
    """A point half as far again as `offing_nm` off the shore of the land the line meets,
    out from the land's charted point through `where` (package 45c, the pilot's joining
    leg); None when the land runs on beyond a league that way."""
    bearing, _ = bearing_and_distance(head, where)
    # half as far again, so that the line between two such marks keeps the offing
    want = 1.5 * offing_nm * units.NAUTICAL_MILE
    for k in range(1, 37):
        p = destination(where, bearing, k * units.CABLE / 2.0)
        # by the chart's shore and not its soundings (the captain's chart, never the
        # world's depth field): on the land the nearest dry ground is under her
        shore = chart.nearest_shore(p, within_m=want)
        if shore is None or shore.distance_m >= want:
            return p
    return None


class Planner:
    """The legs an intent makes over the chart, from the account (never the truth).

    `legs_for(intent, start, departing)` gives the plan: leaving a port, its `to_sea`
    track from the outer road; the sea route to the destination's `from_sea` track (the
    common tracks joined, or the straight line where it keeps clear of the shore and
    the dangers, a headland in the way given an offing); the destination's `from_sea`
    track to its outer road, where the tide is waited for, and its `in` track to the
    anchorage. A place that is no port is a mark shaped for and reached."""

    def __init__(self, world: Any) -> None:
        self.world = world

    # -- the ports' tracks -----------------------------------------------------------

    def _port(self, place: str) -> Any:
        ports = getattr(self.world, "ports", None)
        return (getattr(ports, "ports", None) or {}).get(place) if ports is not None else None

    def _port_track(self, port: Any, which: str) -> list[Leg]:
        """The legs of a port's track: leaving (`to_sea`), the outer road is a mark she
        is steered to on the pilot's course out and passes (`out`, reached within six
        cables, never shaped for from the anchorage: the merchant book's "clear of the
        road"); arriving (`from_sea`), the outer road is where the tide is waited for
        (`road`); the inner track (`in`) ends at the anchorage (`anchorage`), its marks
        reached within four cables or passed."""
        tracks = getattr(port, "tracks", None) or {}
        out: list[Leg] = []
        for words in tracks.get(which) or []:
            m = _mark(self.world, str(words))
            if m is None:
                continue
            kind = "to"
            reached = 2.0
            said = str(words)
            if m[0] == port.outer_road.name or said == port.outer_road.feature_id:
                kind, reached = ("out", 0.6) if which == "to_sea" else ("road", 1.5)
            elif m[0] == port.anchorage.name or said == port.anchorage.feature_id:
                kind, reached = "anchorage", 0.5
            elif which == "in":
                reached = 0.4
            out.append(Leg(m[0], m[1], kind, reached, port=port.id))
        return out

    # -- the sea route -----------------------------------------------------------------

    def clear(
        self,
        a: Position,
        b: Position,
        offing_nm: float = OFFING_NM,
        berth_nm: float = DANGER_BERTH_NM,
        end_skip_m: float = units.CABLE,
    ) -> bool:
        """Whether the straight line from a to b keeps the offing off the shore and the
        berth off the charted dangers, by the chart in the captain's hands. `offing_nm`
        and `berth_nm` are the captain's at sea; the pilot lays a joining leg in his own
        water with his own, the last of it, his station under the land, his own ground
        (`end_skip_m`; package 45c, `ports.PILOT_JOIN_OFFING_NM`)."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return True
        shore = chart.line_shore(
            a,
            b,
            offing_nm * units.NAUTICAL_MILE,
            skip_start_m=offing_nm * units.NAUTICAL_MILE,
            skip_end_m=end_skip_m,
        )
        if shore is not None and (shore[2] or shore[0] < offing_nm * units.NAUTICAL_MILE):
            return False
        for _f, _off, crosses in chart.line_passes(a, b, berth_nm * units.NAUTICAL_MILE):
            if crosses:
                return False
        return True

    def sea_route(self, start: Position, end: Position) -> list[tuple[str, Position]]:
        """The marks between two points at sea: none when the straight line keeps clear;
        else the shortest way along the common tracks whose ends the line reaches clear,
        and failing those a headland in the way given an offing."""
        if self.clear(start, end):
            return []
        tracks = load_tracks(self.world)
        nodes: list[tuple[str, Position]] = []
        edges: dict[int, list[tuple[int, float]]] = {}
        index: dict[str, int] = {}

        def node(mark: tuple[str, Position]) -> int:
            key = mark[0]
            if key not in index:
                index[key] = len(nodes)
                nodes.append(mark)
                edges.setdefault(index[key], [])
            return index[key]

        for t in tracks:
            ids = [node(m) for m in t.marks]
            for u, v in zip(ids, ids[1:], strict=False):
                d = bearing_and_distance(nodes[u][1], nodes[v][1])[1]
                edges[u].append((v, d))
                edges[v].append((u, d))
        if not nodes:
            return self._round_headland(start, end)
        s, e = node(("start", start)), node(("end", end))
        # the start and the end joined to every mark their straight lines reach clear
        for i, (_, p) in enumerate(nodes):
            if i in (s, e):
                continue
            if self.clear(start, p):
                d = bearing_and_distance(start, p)[1]
                edges[s].append((i, d))
            if self.clear(p, end):
                d = bearing_and_distance(p, end)[1]
                edges[i].append((e, d))
        best: dict[int, float] = {s: 0.0}
        prev: dict[int, int] = {}
        seen: set[int] = set()
        while True:
            frontier = [(d, i) for i, d in best.items() if i not in seen]
            if not frontier:
                break
            d, u = min(frontier)
            seen.add(u)
            if u == e:
                break
            for v, w in edges.get(u, []):
                if d + w < best.get(v, math.inf):
                    best[v] = d + w
                    prev[v] = u
        if e not in best:
            return self._round_headland(start, end)
        path = []
        at = e
        while at != s:
            path.append(at)
            at = prev[at]
        path.reverse()
        return [nodes[i] for i in path if i != e]

    def _round_headland(
        self,
        start: Position,
        end: Position,
        offing_nm: float = OFFING_NM,
        berth_nm: float = DANGER_BERTH_NM,
        end_skip_m: float = units.CABLE,
    ) -> list[tuple[str, Position]]:
        """A straight line that the shore or a danger stands across, with no track to
        take: the nearest headland (or island, or danger) to where the line meets the
        land is given an offing to seaward, and the two halves tried again, a few
        rounds at most; what cannot be cleared is left as it is, the master's warning
        on the course shaped saying what it crosses. The offing and the berth are the
        captain's at sea unless given (package 45c: the pilot's joining leg)."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return []
        marks: list[tuple[str, Position]] = []
        a = start
        for _ in range(PLANNER_ROUNDS):
            if self.clear(a, end, offing_nm, berth_nm, end_skip_m):
                break
            shore = chart.line_shore(a, end, offing_nm * units.NAUTICAL_MILE, skip_end_m=end_skip_m)
            where = shore[1] if shore is not None else None
            if where is None:
                for f, _off, crosses in chart.line_passes(a, end, berth_nm * units.NAUTICAL_MILE):
                    if crosses:
                        where = f.position
                        break
            if where is None:
                break
            heads = chart.nearby(
                where, 6.0 * units.NAUTICAL_MILE, ("headland", "island", "rock", "ledge")
            )
            if not heads:
                break
            head = min(heads, key=lambda f: bearing_and_distance(where, f.position)[1])
            # to seaward: away from the land as a whole (the coast's trend), else the
            # side the line comes from, a league off
            bearing, _ = bearing_and_distance(head.position, where)
            trend = chart.coast_trend(head.position, 3.0 * units.NAUTICAL_MILE)
            away = (trend[0] + 180.0) % 360.0 if trend is not None else bearing
            off = destination(head.position, away, offing_nm * units.NAUTICAL_MILE)
            if offing_nm < OFFING_NM:
                # a pilot's offing in his own water (package 45c): an island or a point
                # is longer than his two cables and a half, so the mark is laid that far
                # off its shore, out from it through where the line meets the land, and
                # not that far from its charted point (the Isle of Aix, a mile long)
                off = _off_the_land(chart, head.position, where, offing_nm) or off
            mark = (plain_position(off), off)
            if marks and marks[-1][0] == mark[0]:
                break  # the same headland again: no way round by this rule
            marks.append(mark)
            a = off
        return marks

    # -- the plan --------------------------------------------------------------------

    def legs_for(self, intent: Intent, start: Position, departing: str = "") -> list[Leg]:
        legs: list[Leg] = []
        port_from = self._port(departing) if departing else None
        if port_from is not None:
            legs += self._port_track(port_from, "to_sea")
        if intent.kind in ("station", "fish"):
            place = self._place(intent.destination)
            if place is not None:
                # a fishing trip's mark is the ground itself (package 56): a seine ground
                # lies in a bay, where a station kept a league off would be on the land
                mark = (
                    place[1]
                    if intent.kind == "fish"
                    else station_off(self.world, place[1], intent.radius_nm)
                )
                legs += self._sea_legs(legs[-1].position if legs else start, mark)
                legs.append(Leg(plain_position(mark), mark, "station", intent.radius_nm))
            return legs
        port_to = self._port(intent.destination)
        if port_to is not None:
            approach = self._port_track(port_to, "from_sea")
            first = approach[0].position if approach else port_to.outer_road.position
            legs += self._via_legs(legs[-1].position if legs else start, intent.via, first)
            legs += self._sea_legs(legs[-1].position if legs else start, first)
            legs += approach
            if not any(leg.kind == "road" for leg in legs):
                legs.append(
                    Leg(
                        port_to.outer_road.name,
                        port_to.outer_road.position,
                        "road",
                        1.5,
                        port_to.id,
                    )
                )
            inner = self._port_track(port_to, "in")
            legs += inner
            if not any(leg.kind == "anchorage" for leg in legs):
                legs.append(
                    Leg(
                        port_to.anchorage.name,
                        port_to.anchorage.position,
                        "anchorage",
                        0.5,
                        port_to.id,
                    )
                )
            return legs
        place = self._place(intent.destination)
        if place is not None:
            legs += self._via_legs(legs[-1].position if legs else start, intent.via, place[1])
            legs += self._sea_legs(legs[-1].position if legs else start, place[1])
            legs.append(
                Leg(place[0], place[1], "anchorage" if intent.kind == "home" else "to", 0.5)
            )
        return legs

    def _via_legs(self, a: Position, via: tuple[str, ...], end: Position) -> list[Leg]:
        """The legs by the intent's marks (package 45), each a `via` leg reached within two
        miles by account or passed abeam, with the sea route between one and the next
        where the straight line is not clear; no routing where none are named."""
        legs: list[Leg] = []
        if not via:
            return legs
        at = a
        for words, pos, hand in way_marks(self.world, a, list(via), end):
            legs += self._sea_legs(at, pos)
            legs.append(Leg(words, pos, "via", 2.0, said=hand))
            at = pos
        return legs

    def _place(self, words: str) -> tuple[str, Position] | None:
        return _mark(self.world, words)

    def _sea_legs(self, a: Position, b: Position) -> list[Leg]:
        return [Leg(words, p, "to", 2.0) for words, p in self.sea_route(a, b)]


# ---------------------------------------------------------------------------
# Perception on the player's terms
# ---------------------------------------------------------------------------


def _lee_land_nm(world: Any, p: Perception, here: Position | None = None) -> float | None:
    """The nearest land within the lee sector, in miles: the lookout's land when it bears
    within the sector, and the chart's coast along rays from the account a point apart
    through it (`LEE_SECTOR_POINTS` either side of dead to leeward, `LEE_RAY_NM` long);
    None with no wind, no account or nothing within the rays. `here` is the point the
    rays are cast from when it is not the player's account (a far-detail vessel's own
    truth, package 43)."""
    if p.wind_from_deg is None:
        return None
    toward = (p.wind_from_deg + 180.0) % 360.0
    half = math.radians(LEE_SECTOR_POINTS * 11.25)
    best: float | None = None
    land = _point_deg(p.nearest_land_bearing or "")
    if p.nearest_land_nm is not None and land is not None:
        if abs(units.wrap_pi(math.radians(land - toward))) < half:
            best = p.nearest_land_nm
    chart = getattr(world, "chart", None)
    if chart is None:
        return best
    if here is None:
        nav = getattr(world, "navigation", None)
        if nav is None:
            return best
        try:
            here = nav.account_now()
        except Exception:  # noqa: BLE001 - no account yet
            here = None
    if here is None:
        return best
    reach = LEE_RAY_NM * units.NAUTICAL_MILE
    for k in range(-LEE_SECTOR_POINTS, LEE_SECTOR_POINTS + 1):
        bearing = (toward + k * 11.25) % 360.0
        try:
            hit = chart.line_shore(here, destination(here, bearing, reach), 2.0 * units.CABLE)
        except Exception:  # noqa: BLE001 - a chart with no field here
            hit = None
        if hit is None:
            continue
        _, where, _ = hit
        d_nm = bearing_and_distance(here, where)[1] / units.NAUTICAL_MILE
        if best is None or d_nm < best:
            best = d_nm
    return best


@dataclass
class Perception:
    """What the captain judges by, read from the registry's readings and the account
    and nothing else (`Perception.read`): every field is what a reading gives him."""

    tick: int
    wind_kn: float = 0.0
    wind_from_deg: float | None = None
    heading_deg: float | None = None
    speed_kn: float = 0.0
    visibility: str = ""
    visibility_nm: float | None = None
    daylight: str = ""
    land_in_sight: bool = False
    nearest_land_nm: float | None = None
    nearest_land_bearing: str = ""
    anchor_down: bool = False
    aground: bool = False
    anchoring: bool = False
    coast_by_account_nm: float | None = None
    coast_by_account_bearing_deg: float | None = None
    lee_land_nm: float | None = None  # the nearest land within the lee sector (package 45)
    manoeuvre: str = ""
    strangers: list[dict[str, Any]] = field(default_factory=list)
    in_port: str = ""  # the port she lies in, by the port's reading
    port_distance_nm: float | None = None
    pilot_aboard: bool = False
    boat_away: bool = False
    hold: dict[str, float] = field(default_factory=dict)
    purse: float = 0.0
    prices: dict[str, float] = field(default_factory=dict)
    prices_port: str = ""
    high_waters: list[datetime] = field(default_factory=list)
    now: datetime | None = None
    glass_falling_fast: bool = False
    dangers_nm: float | None = None
    # package 45: the glass's tendency in words; the sails as the readings give them; the
    # pilot's conn; the port's reach
    glass_tendency: str = ""
    headsail_set: bool = False
    headsails_blown: list[str] = field(default_factory=list)
    headsails_bent: list[str] = field(default_factory=list)
    topsail_reefs: int = 0
    storm_staysails_set: bool = False
    # package 45c: every topsail set, and a course (or a schooner's gaff sail) set, for
    # the steps of sail after the gale
    topsails_all_set: bool = True
    courses_set: bool = True
    pilot_conn: bool = False
    reach_nm: float = IN_PORT_NM
    # package 43: her own class and each stranger's (`SIZE_RANK`), for a cruiser's judgement
    # of a superior force; the port she lies off, for a far-detail body
    own_size: int = 0
    # package 58b: the tide the master allows in the reckoning now (`the reckoning`'s own
    # words and figures: whose, the knots, where it sets, the flood or the ebb, the water)
    tide_allowed: dict[str, Any] = field(default_factory=dict)
    # package 58b: the depth of water by the chart at the account, in fathoms (None off the
    # chart or on the land)
    chart_fathoms: float | None = None

    @classmethod
    def read(cls, world: Any) -> Perception:
        view = world.readings
        p = cls(tick=world.clock.tick, now=world.clock.ship_time)
        p.own_size = size_of_file(getattr(getattr(world.ship, "spec", None), "source", ""))
        wind = view.value("mean_true_wind_speed")
        if wind is None:
            wind = view.value("true_wind_speed")
        p.wind_kn = units.ms_to_knots(float(wind)) if wind is not None else 0.0
        frm = view.value("mean_true_wind_from")
        if frm is None:
            frm = view.value("true_wind_from")
        p.wind_from_deg = units.rad_to_deg(float(frm)) % 360.0 if frm is not None else None
        heading = view.value("heading")
        p.heading_deg = units.rad_to_deg(float(heading)) % 360.0 if heading is not None else None
        speed = view.value("speed")
        p.speed_kn = units.ms_to_knots(float(speed)) if speed is not None else 0.0
        vis = view.value("visibility")
        if isinstance(vis, dict):
            p.visibility = str(vis.get("words") or "")
            p.visibility_nm = vis.get("miles")
        p.daylight = str(view.value("daylight") or "")
        land = view.value("land")
        p.land_in_sight = bool(isinstance(land, dict) and land.get("in_sight"))
        near = view.value("nearest_land")
        if isinstance(near, dict) and near.get("metres") is not None:
            p.nearest_land_nm = float(near["metres"]) / units.NAUTICAL_MILE
            p.nearest_land_bearing = str(near.get("bearing") or "")
        anchor = view.value("anchor")
        if isinstance(anchor, dict):
            p.anchor_down = anchor.get("state") == "down"
            p.aground = anchor.get("state") == "aground"
        p.manoeuvre = str(view.value("manoeuvre_in_hand") or "")
        work = view.value("work_in_hand")
        if isinstance(work, dict):
            # an anchor being brought to (package 40c): the evolution is work, not a
            # manoeuvre, and she is not under way again while it is in hand
            doing = list(work.get("doing") or []) + list(work.get("waiting") or [])
            p.anchoring = any("anchor" in str(w) for w in doing)
        # the nearest shore by his account on the chart in his hands (package 40c, the
        # captain's trials): in thick weather or by night the lookout sees no land, and
        # the captain judges a lee shore or the land's nearness by his reckoning
        nav = getattr(world, "navigation", None)
        chart = getattr(world, "chart", None)
        if nav is not None and chart is not None:
            try:
                here = nav.account_now()
                found = chart.coast_distance(here) if here is not None else None
            except Exception:  # noqa: BLE001 - a chart with no field here
                found = None
            if found is not None:
                metres, toward = found
                p.coast_by_account_nm = float(metres) / units.NAUTICAL_MILE
                p.coast_by_account_bearing_deg = float(toward)
            p.lee_land_nm = _lee_land_nm(world, p)
        strangers = view.value("strangers")
        if isinstance(strangers, dict):
            # each with her class by the lookout's words (package 43), on a copy: the
            # reading's own items are the registry's
            p.strangers = [
                dict(s, size=size_of_words(str(s.get("known") or "")))
                for s in (strangers.get("items") or [])
            ]
        port = view.value("port")
        if isinstance(port, dict):
            p.port_distance_nm = port.get("distance_nm")
            # in port: at anchor within the port's reach by account (`ports.IN_PORT_NM`
            # is the port's own rule at the truth; the captain reads his account)
            dist = port.get("distance_nm")
            # the port's reach (package 45): the reading carries it
            p.reach_nm = float(port.get("reach_nm") or IN_PORT_NM)
            if (
                p.anchor_down
                and port.get("port")
                and dist is not None
                and float(dist) <= p.reach_nm
            ):
                p.in_port = str(port.get("port"))
        pilot = view.value("pilot")
        p.pilot_aboard = isinstance(pilot, dict) and bool(pilot.get("name"))
        p.pilot_conn = isinstance(pilot, dict) and bool(pilot.get("conn"))
        reckoning = view.value("reckoning")
        if isinstance(reckoning, dict) and isinstance(reckoning.get("tide"), dict):
            p.tide_allowed = dict(reckoning["tide"])
        charted = view.value("depth_of_water")
        if charted is not None:
            p.chart_fathoms = units.m_to_fathoms(float(charted))
        # the sails by the readings (package 45): the head sails set, blown out or bent
        # and furled, the topsails' reefs, the storm staysails
        ship = world.ship
        groups = getattr(ship, "groups", {}) or {}
        sails = getattr(ship, "sails", {}) or {}
        head_ids = [sid for g in ("jibs", "staysails") for sid in groups.get(g, []) if sid in sails]
        for sid in head_ids:
            r = view.value("sail", sid)
            if not isinstance(r, dict):
                continue
            state = str(r.get("state") or "")
            if state == "set":
                p.headsail_set = True
            elif state == "blown_out":
                p.headsails_blown.append(sid)
            elif state in ("furled", "bent", "in_the_gear", "loosed"):
                p.headsails_bent.append(sid)
        for sid in groups.get("topsails", []):
            r = view.value("sail", sid)
            if isinstance(r, dict) and str(r.get("state") or "") == "set":
                p.topsail_reefs = max(p.topsail_reefs, int(r.get("reefs") or 0))
            elif isinstance(r, dict):
                p.topsails_all_set = False
        lower = [sid for sid in groups.get("courses", []) if sid in groups.get("plain sail", [])]
        lower = lower or [
            sid for sid in groups.get("gaff sails", []) if sid in groups.get("plain sail", [])
        ]
        if lower:
            p.courses_set = any(
                isinstance(r, dict) and str(r.get("state") or "") == "set"
                for r in (view.value("sail", sid) for sid in lower)
            )
        for sid in groups.get("storm staysails", []) or groups.get("storm canvas", []):
            r = view.value("sail", sid)
            if isinstance(r, dict) and str(r.get("state") or "") == "set":
                p.storm_staysails_set = True
        boat = view.value("boat")
        p.boat_away = bool(isinstance(boat, dict) and boat.get("away"))
        manifest = view.value("manifest")
        if isinstance(manifest, dict):
            p.hold = {str(k): float(v) for k, v in (manifest.get("goods") or {}).items()}
        purse = view.value("purse")
        if isinstance(purse, dict):
            p.purse = float(purse.get("pounds") or 0.0)
        prices = view.value("prices")
        if isinstance(prices, dict):
            p.prices_port = str(prices.get("port") or "")
            p.prices = {str(k): float(v) for k, v in (prices.get("prices") or {}).items()}
        tide = view.value("tide_by_almanac")
        if isinstance(tide, dict):
            p.high_waters = [datetime.fromisoformat(t) for t in (tide.get("times") or [])]
            if tide.get("next"):
                nxt = datetime.fromisoformat(str(tide["next"]))
                if nxt not in p.high_waters:
                    p.high_waters.append(nxt)
        tendency = view.value("tendency")
        if isinstance(tendency, dict):
            p.glass_tendency = str(tendency.get("words") or "")
            p.glass_falling_fast = p.glass_tendency == "falling fast"
        dangers = view.value("dangers")
        if isinstance(dangers, dict) and dangers.get("metres") is not None:
            p.dangers_nm = float(dangers["metres"]) / units.NAUTICAL_MILE
        return p

    def tide_is(self, which: str) -> bool | None:
        """Whether it is the flood or the ebb now by the master's almanac: the ebb for
        six hours after high water, the flood for the six before the next; None with no
        table."""
        if not self.high_waters or self.now is None:
            return None
        before = [t for t in self.high_waters if t <= self.now]
        after = [t for t in self.high_waters if t > self.now]
        since = (self.now - max(before)).total_seconds() / 3600.0 if before else None
        until = (min(after) - self.now).total_seconds() / 3600.0 if after else None
        ebb = since is not None and since < 6.0 + 0.2
        flood = until is not None and until < 6.0 + 0.2 and not ebb
        if since is None and until is not None:
            ebb = until > 6.2
            flood = not ebb
        return ebb if which == "ebb" else flood


# ---------------------------------------------------------------------------
# The captain
# ---------------------------------------------------------------------------


# The stimuli a doctrine's transition may name, each judged from the perception alone.
STIMULI: tuple[str, ...] = (
    "ready for sea",
    "gale",
    "gale over",
    "lee shore",
    "no sea room",
    "thick near the land",
    "weather clear",
    "hostile stranger",
    "stranger",
    "stranger lost",
    "stranger spoken",
    "enemy made out",
    "friend made out",
    "course not laid",
    "course laid",
    "at the road",
    "under way",
    "anchored",
    "anchored in port",
    "sheltered",
    "aground",
    "afloat",
    "cargo done",
    # package 43 (the cruiser's doctrine): an enemy of a bigger class within the hostile
    # distance; a stranger within `investigate_nm` of a ship on passage; a chase that has
    # not closed in `chase_stale_hours`
    "overmatched",
    "stranger near",
    "chase stale",
    # package 70 (the engaging doctrine): an enemy within the doctrine's engaging distance;
    # none within its breaking-off distance for its minutes; the mark engaged has struck;
    # a man of war of the enemy's within the hostile distance (the privateer's fear)
    "enemy in range",
    "enemy out of range",
    "enemy struck",
    "man of war near",
)


class Judgement:
    """The brain's judgement, shared by the two bodies (spec M6 §4, "one brain, two
    bodies"; package 43): the weather's trend and the doctrine's transitions on a
    `Perception`, whoever built it. `Captain` (the near body: the player's ship or a
    promoted vessel, whose doings are orders) and `FarCaptain` (the far body, whose
    doings are a plan) both carry a `doctrine`, a `state`, a `trend`, the wind's log, the
    stranger in hand and a `_business` dict, and each gives the few hooks the stimuli
    ask of its body (`_inner_leg`, `_waiting_at_road`, `_shelter_port`, `_nearest_enemy`,
    `_is_enemy`, `_ready_for_sea`, `_enter`)."""

    doctrine: Doctrine | None
    state: str | None
    trend: str
    intent: Intent | None
    _stranger: str | None
    _gale_over_since: int | None
    _wind_log: list[tuple[int, float]]
    _business: dict[str, Any]
    _waiting_at_road: bool
    # the strangers this captain has done with (package 43): a chase given up as stale is
    # not taken up again while she is in sight, as a sail spoken is a stranger no more
    given_up: set[str] = frozenset()  # type: ignore[assignment]
    # the ships that have fired on her (package 70, rule 3): an enemy from then on whatever
    # her colours (a checkpoint from before loads with none)
    fired_on: set[str] = frozenset()  # type: ignore[assignment]

    def _inner_leg(self) -> bool:
        return False

    def _spoken(self, s: dict[str, Any]) -> bool:
        """Whether a sail is a stranger no more to this captain: spoken within hail (the
        lookout's flag), or her chase given up (`given_up`)."""
        sid = str(s.get("id") or "")
        return (
            bool(s.get("spoken"))
            or sid in (self.given_up or ())
            or sid in (getattr(self, "spoken_ids", None) or ())
        )

    def _unspoken(self, p: Perception) -> list[dict[str, Any]]:
        return [s for s in p.strangers if not self._spoken(s)]

    def _read_trend(self, p: Perception) -> str:
        """The weather's trend (package 45, Part B item 6): "worsening" when the glass is
        falling fast or the wind has risen by a force (`worsening_wind_kn`) within the
        hour; "mending" when the glass is rising or the wind has eased by as much; else
        "". Luce 1884 ch. XXVIII on the barometer as the instrument of warning, and
        FitzRoy's rules of the glass (a rapid fall, a blow soon; "long foretold, long
        last"); the force's knots and the hour judgement."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        self._wind_log.append((p.tick, p.wind_kn))
        self._wind_log = [x for x in self._wind_log if p.tick - x[0] <= TREND_HOUR_S]
        risen = p.wind_kn - self._wind_log[0][1]
        worsening = p.glass_falling_fast or risen >= float(th("worsening_wind_kn", 6))
        mending = p.glass_tendency in ("rising", "rising fast") or risen <= -float(
            th("mending_wind_kn", 6)
        )
        self.trend = "worsening" if worsening else "mending" if mending else ""
        # the gale-over line as the trend moves it, and how long the wind has stood under
        # it: sooner by `mending_sooner_kn` with the glass rising, lower by
        # `worsening_sooner_kn` with the glass falling (as the gale line is), so that the
        # two lines keep their band apart
        line = float(th("gale_over_kn", 28))
        if self.trend == "mending":
            line += float(th("mending_sooner_kn", 4))
        elif self.trend == "worsening":
            line -= float(th("worsening_sooner_kn", 6))
        if p.wind_kn < line:
            if self._gale_over_since is None:
                self._gale_over_since = p.tick
        else:
            self._gale_over_since = None
        self._read_chase(p)
        return self.trend

    def _read_chase(self, p: Perception) -> None:
        """The chase's log (package 43): the stranger in hand's distance at each
        judgement while she is chased or closed, for the `chase stale` stimulus (a chase
        that has not closed in `chase_stale_hours` is given up: the trials' two captains
        chased and ran for fifteen hours without a cable gained)."""
        log = getattr(self, "_chase_log", None)
        if log is None:
            log = self._chase_log = []
        if self.state not in ("investigating a stranger", "chasing") or self._stranger is None:
            log.clear()
            return
        for s in p.strangers:
            if s.get("id") == self._stranger and s.get("estimate_m") is not None:
                if log and log[-1][2] != self._stranger:
                    log.clear()
                log.append((p.tick, float(s["estimate_m"]), self._stranger))
                return

    def _chase_stale(self, hours: float) -> bool:
        log = getattr(self, "_chase_log", None) or []
        if len(log) < 2:
            return False
        span = hours * 3600.0
        if log[-1][0] - log[0][0] < span:
            return False
        then = next(d for t, d, _ in log if log[-1][0] - t <= span)
        return log[-1][1] >= then - units.NAUTICAL_MILE

    def _transitions(self, p: Perception) -> None:
        if self.doctrine is None or self.state is None:
            return
        for t in self.doctrine.from_state(self.state):
            if self._stimulus(t.on, p) and not (t.unless and self._stimulus(t.unless, p)):
                if t.on == "chase stale" and self._stranger is not None:
                    # the chase given up: she is done with, and not closed again in sight
                    if not isinstance(self.given_up, set):
                        self.given_up = set()
                    self.given_up.add(str(self._stranger))
                if t.on == "friend made out" and self._stranger is not None:
                    # a friend made out is a stranger no more (package 43b: the business's
                    # cruiser off the Isle of Bas made out a neutral lying in Roscoff every
                    # minute, and took her for a stranger again the minute after)
                    if not isinstance(self.given_up, set):
                        self.given_up = set()
                    self.given_up.add(str(self._stranger))
                self._enter(t.to)
                return

    def _overmatched(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        """An enemy of a bigger class than her own within `within_nm` (package 43, the
        cruiser's judgement of a superior force), by what the tops have made out."""
        enemies = [
            s
            for s in p.strangers
            if self._is_enemy(s)
            and not self._spoken(s)
            and s.get("estimate_m") is not None
            and float(s["estimate_m"]) / units.NAUTICAL_MILE <= within_nm
            and int(s.get("size") or 0) > int(p.own_size or 0)
            # package 70: a merchantman of a bigger hull is a prize, not a superior force
            and "merchant" not in str(s.get("known") or "").lower()
        ]
        if not enemies:
            return None
        return min(enemies, key=lambda s: float(s["estimate_m"]))

    def _stimulus(self, name: str, p: Perception) -> bool:
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        # the glass as a stimulus (package 45, Part B item 6): worsening brings the
        # heavy-weather rows a step sooner, mending the fair-weather rows
        # (a first version widened the sea room and the lee shore by half as well when the
        # glass fell: on the station fifteen miles off Ushant that put the station itself
        # inside the no-sea-room line, and she hove to and filled away by turns all the
        # forenoon of the gale trial; the two lines stand as the doctrine gives them)
        sooner = float(th("worsening_sooner_kn", 6)) if self.trend == "worsening" else 0.0
        if name == "weather worsening":
            return self.trend == "worsening"
        if name == "weather mending":
            return self.trend == "mending"
        if name == "gale":
            return p.wind_kn >= float(th("gale_kn", 34)) - sooner and p.manoeuvre not in (
                "hove to",
                "heaving to",
            )
        if name == "gale over":
            # under the line for `gale_over_minutes` together, not on a lull (the first
            # version filled her away ten minutes after she hove to, on a lull of the
            # gusty wind, and she thrashed between the two books all the forenoon of the
            # station trial); and while the glass falls the line comes down with the gale
            # line, so that the band between them is never narrowed to a gust's width
            since = self._gale_over_since
            minutes = float(th("gale_over_minutes", 10))
            return since is not None and p.tick - since >= minutes * 60.0
        if name == "lee shore":
            # the land within the lee sector (`_lee_land_nm`: the lookout's land when it
            # bears so, and the chart's coast along the account's rays through the sector)
            return p.lee_land_nm is not None and p.lee_land_nm <= float(th("lee_shore_nm", 6))
        if name == "no sea room":
            # the land to leeward within the sea room a night's drift hove to wants
            # (package 40c): she heaves to only with sea room, and leaves it for a lee
            # shore within `lee_shore_nm`, the two thresholds apart so that she does not
            # heave to and fill away by turns at one line
            return p.lee_land_nm is not None and p.lee_land_nm <= float(th("sea_room_nm", 10))
        if name == "thick near the land":
            thick = p.visibility in ("a mile", "a cable")
            dist = p.nearest_land_nm if p.nearest_land_nm is not None else p.coast_by_account_nm
            near = dist is not None and dist < float(th("shelter_land_nm", 12))
            return thick and near and self._shelter_port(p) is not None
        if name == "weather clear":
            return p.visibility not in ("a mile", "a cable")
        if name == "hostile stranger":
            return self._nearest_enemy(p, float(th("stranger_hostile_nm", 6))) is not None
        if name == "overmatched":
            return self._overmatched(p, float(th("stranger_hostile_nm", 6))) is not None
        if name == "stranger":
            return any(not self._spoken(s) for s in p.strangers)
        if name == "stranger near":
            within = float(th("investigate_nm", 10))
            return any(
                not self._spoken(s)
                and s.get("estimate_m") is not None
                and float(s["estimate_m"]) / units.NAUTICAL_MILE <= within
                for s in p.strangers
            )
        if name == "chase stale":
            return self._chase_stale(float(th("chase_stale_hours", 3)))
        # package 70: the engaging doctrine's stimuli
        if name == "enemy in range":
            within = float(th("engage_nm", 0.0))
            return within > 0.0 and self._enemy_within(p, within) is not None
        if name == "enemy out of range":
            within = float(th("break_off_nm", 2.0))
            if self._enemy_within(p, within) is not None:
                self._business.pop("out_of_range_since", None)
                return False
            since = self._business.setdefault("out_of_range_since", p.tick)
            return p.tick - since >= float(th("break_off_minutes", 10)) * 60.0
        if name == "enemy struck":
            return self._enemy_struck(p)
        if name == "man of war near":
            # package 72: a privateer's own distance for a man of war (`man_of_war_nm`),
            # apart from the two leagues a superior force is hauled off from, so that she
            # hovers on a convoy and runs when the escort bears down
            within = float(th("man_of_war_nm", th("stranger_hostile_nm", 6)))
            return self._man_of_war_within(p, within) is not None
        if name == "stranger lost":
            if self._stranger is None:
                return not p.strangers
            return not any(
                s.get("id") == self._stranger and not self._spoken(s) for s in p.strangers
            )
        if name == "stranger spoken":
            return any(s.get("id") == self._stranger and self._spoken(s) for s in p.strangers)
        if name == "enemy made out":
            return any(
                s.get("id") == self._stranger and self._is_enemy(s) for s in p.strangers
            ) or any(
                s.get("id") == self._stranger
                and s.get("made_out", 0) >= 2
                and s.get("nation") is None
                for s in p.strangers
            )
        if name == "friend made out":
            # package 71: a King's captain with the private signal aboard takes a stranger
            # under his own colours for a friend only when she has answered it (or the
            # hail) rightly; a neutral's colours are a friend's by themselves
            return any(
                s.get("id") == self._stranger
                and s.get("nation")
                and not self._is_enemy(s)
                and self._friend_sure(s)
                for s in p.strangers
            )
        if name == "course not laid":
            # in pilot water a foul wind is waited out at anchor, not beaten (`_passage`)
            return self._course_dwelt(p, "not laid") and not self._inner_leg()
        if name == "course laid":
            return self._course_dwelt(p, "laid")
        if name == "at the road":
            return bool(self._waiting_at_road)
        if name == "under way":
            return not p.anchor_down and not p.aground and not p.anchoring
        if name == "anchored":
            return p.anchor_down
        if name == "anchored in port":
            return p.anchor_down and bool(p.in_port)
        if name == "sheltered":
            return p.anchor_down
        if name == "aground":
            return p.aground
        if name == "afloat":
            return not p.aground
        if name == "ready for sea":
            return self._ready_for_sea(p)
        if name == "cargo done":
            return bool(self.intent and self.intent.done)
        return False

    def _course_verdict(self, p: Perception) -> str:
        """Whether the course shaped for the leg is laid, by one rule (package 43b; the
        trade trial's beating rule and passage rule traded the deck every two minutes as
        an evasion ended, each state's first course, shaped on the edge of the wind, giving
        the other verdict): the course last shaped by his rule (`course_heading_deg`)
        against the wind of the minute, not laid nearer the wind than her close-hauled
        angle and the shaping's margin (`COURSE_NOT_LAID_MARGIN_POINTS`), laid only
        `beating_band_points` freer than that, and between the two as it was. With no
        course shaped yet, the helm's own word on the last (`course_not_laid`)."""
        from freesail.orders.navigation import COURSE_NOT_LAID_MARGIN_POINTS

        b = self._business
        heading = b.get("course_heading_deg")
        closest = b.get("course_closest_deg")
        before = b.get("course_verdict")
        if heading is None or closest is None or p.wind_from_deg is None:
            verdict = "not laid" if b.get("course_not_laid") else "laid"
        else:
            th = self.doctrine.threshold if self.doctrine else (lambda _k, d=None: d)
            point = units.rad_to_deg(units.POINT)
            off = abs((float(heading) - float(p.wind_from_deg) + 180.0) % 360.0 - 180.0)
            edge = float(closest) + COURSE_NOT_LAID_MARGIN_POINTS * point
            band = float(th("beating_band_points", 0.5)) * point
            if off < edge:
                verdict = "not laid"
            elif off >= edge + band:
                verdict = "laid"
            else:
                verdict = before or ("not laid" if b.get("course_not_laid") else "laid")
        if verdict != before:
            b["course_verdict"] = verdict
            b["course_verdict_since"] = p.tick
        return verdict

    def _course_dwelt(self, p: Perception, wanted: str) -> bool:
        """The verdict `wanted` held for the doctrine's `beating_dwell_minutes` (package
        43b): the beating book is taken up, and given up, on a verdict that has stood a
        while, never on one course's word."""
        if self._course_verdict(p) != wanted:
            return False
        th = self.doctrine.threshold if self.doctrine else (lambda _k, d=None: d)
        since = int(self._business.get("course_verdict_since", p.tick))
        return p.tick - since >= float(th("beating_dwell_minutes", 10)) * 60.0

    # the hooks each body gives (the near body's are `Captain`'s own methods)

    def _enter(self, state: str) -> None:  # pragma: no cover - the bodies' own
        raise NotImplementedError

    def _shelter_port(self, p: Perception) -> Any:
        return None

    def _is_enemy(self, s: dict[str, Any]) -> bool:
        return False

    def _known_enemy(self, s: dict[str, Any]) -> bool | None:
        """What he knows of her beyond her colours (package 71, rule 3): True when she
        fired on him or he saw her fire under false colours, or the private signal or the
        hail made her an enemy; False when they made her a friend; None when neither."""
        sid = str(s.get("id") or "")
        if sid in (self.fired_on or ()) or sid in (getattr(self, "pirates", None) or ()):
            return True
        known = (getattr(self, "recognised", None) or {}).get(sid)
        if known is not None and known.get("enemy") is not None:
            return bool(known["enemy"])
        return None

    def _friend_sure(self, s: dict[str, Any]) -> bool:
        from freesail.world import signalling

        known = self._known_enemy(s)
        if known is not None:
            return not known
        if str(s.get("nation") or "") != signalling._own_nation(self):
            return True
        return signalling._table(self) is None

    def _nearest_enemy(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        return None

    def _ready_for_sea(self, p: Perception) -> bool:
        return False

    # -- the action's (package 70) ----------------------------------------------------

    def _enemy_within(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        """The nearest enemy within the miles, spoken or not (a ship that has fired on
        her is an enemy whatever was said): the engaging doctrine's mark."""
        enemies = [
            s
            for s in p.strangers
            if self._is_enemy(s)
            and s.get("estimate_m") is not None
            and float(s["estimate_m"]) / units.NAUTICAL_MILE <= within_nm
            and not self._stranger_struck(s)
        ]
        if not enemies:
            return None
        return min(enemies, key=lambda s: float(s["estimate_m"]))

    def _man_of_war_within(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        """An enemy's man of war within the miles, by the lookout's words of her ('a
        brig-sloop of war', 'a frigate', 'a cutter of the revenue'); a stranger under no
        colours of a man of war's rig counts, a privateer taking no chances."""
        for s in p.strangers:
            if s.get("estimate_m") is None:
                continue
            if float(s["estimate_m"]) / units.NAUTICAL_MILE > within_nm:
                continue
            words = str(s.get("known") or "").lower()
            if not any(w in words for w in MAN_OF_WAR_WORDS):
                continue
            if self._is_enemy(s) or s.get("nation") is None:
                return s
        return None

    def _stranger_struck(self, s: dict[str, Any]) -> bool:
        return False

    def _enemy_struck(self, p: Perception) -> bool:
        return False


class Captain(Judgement):
    """The rules-based captain of the player's ship: named after the person who commands
    her, with the scenario's book or his intent; the state machine, the plan and the
    doctrine; and the stand-in for a model at the captain's station."""

    def __init__(self, world: Any, intent: str | None = None, books: tuple[str, ...] = ()):
        self.world = world
        self.intent_words = intent or ""
        self.intent: Intent | None = None
        self.books = tuple(books)  # the scenario's standing-orders files, by name
        self.state: str | None = None
        self.doctrine: Doctrine | None = None
        self.role = ""
        self.legs: list[Leg] = []
        self.leg_i = 0
        self.leg_shaped_tick: int | None = None
        self.stand_in = False  # a model's door silent: the judgements stand in
        self.seated = False  # a model holds the captain's station
        # the player's hand (decision 41; package 40c): a direct order of the ship's given
        # at the prompt on an intent scenario makes him stand aside, his book struck,
        # until `captain: carry on` gives her back to him
        self.aside = False
        self.last_judged = -1
        self._seen_log = 0
        self._road_said: dict[str, int] = {}
        self._state_entered: int | None = None
        self._waiting_at_road = False
        self._business: dict[str, Any] = {}
        self._plan_from: Position | None = None  # where the plan was laid (package 45)
        # the weather's trend (package 45): the wind each judgement for an hour, and the
        # trend read from it and the glass ("worsening", "mending" or "")
        self._wind_log: list[tuple[int, float]] = []
        self.trend = ""
        self._calm_since: int | None = None  # the wind under the sail-again line since
        self._gale_over_since: int | None = None  # the wind under the gale-over line since
        self._entry_stop: int | None = None  # the inner leg he anchors at, the wind foul beyond
        self._stranger: str | None = None
        self._departing = ""  # the port she sails from, for the plan's first legs
        self.given_up: set[str] = set()  # the chases given up (package 43)
        self.fired_on: set[str] = set()  # the ships that fired on her (package 70)
        # package 71 (rule 3): what he knows of each sail by the private signal or the hail
        # (`signalling.recognise`), the pirates he saw fire under false colours, the sail
        # spoken (the far brain's set, folded in and back)
        self.recognised: dict[str, dict[str, Any]] = {}
        self.pirates: set[str] = set()
        self.spoken_ids: set[str] = set()
        self.error = ""
        if self.intent_words:
            try:
                self.intent = read_intent(world, self.intent_words)
            except ValueError as e:
                self.error = str(e)
                self.intent = None
            self.role = role_for(world, self.intent)
            self.doctrine = load_doctrine(self.role)

    # -- who and what ------------------------------------------------------------------

    @property
    def name(self) -> str:
        people = getattr(self.world, "people", None)
        try:
            return people.captain.name if people is not None else "the captain"
        except (IndexError, AttributeError):
            return "the captain"

    @property
    def active(self) -> bool:
        """Whether the captain has an intent to sail by (a scenario with a book has
        none: the book sails her, as it always did)."""
        return self.intent is not None

    @property
    def commands(self) -> bool:
        """Whether his judgements are given now: an intent, and no model at the
        captain's station with the deck (or that model's door silent, the stand-in)."""
        return (
            self.active
            and (not self.seated or self.stand_in)
            and not getattr(self, "aside", False)
            and getattr(self, "over_head_until", None) is None
        )

    def book_words(self) -> str:
        if self.state is not None:
            return f"his book '{self.state}'"
        if self.books:
            names = ", ".join(Path(b).name for b in self.books)
            return f"the scenario's book ({names})"
        return "no book"

    def words(self) -> str:
        """For `the captain` reading: who commands and by what."""
        head = f"{self.name}, {self.role or 'by the book'}" if self.active else self.name
        if self.active:
            what = f"{head}; the intent: {self.intent.words}" if self.intent else head
            if self.intent is not None and self.intent.done:
                what += " (done)"
            if self.state:
                what += f"; {self.state}"
            if self.legs and self.leg_i < len(self.legs):
                what += f"; the leg for {self.legs[self.leg_i].words}"
            if self.error:
                what += f"; the intent refused: {self.error}"
            if getattr(self, "aside", False):
                what += (
                    "; standing aside at the player's order ('captain: carry on' gives her back)"
                )
            return what
        return f"{head}, by {self.book_words()}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "intent": self.intent.to_dict() if self.intent else None,
            "state": self.state,
            "aside": bool(getattr(self, "aside", False)),
            "books": list(self.books),
            "legs": [leg.to_dict() for leg in self.legs],
            "leg": self.leg_i,
            "stand_in": self.stand_in,
            "seated": self.seated,
            "commands": self.commands,
        } | (
            # an order over his head (package 62), only while there is one
            {"over_head": self.over_head_order}
            if getattr(self, "over_head_until", None) is not None
            else {}
        )

    # -- the intent changed (a world order) ----------------------------------------------

    def set_intent(self, words: str) -> str:
        """`captain: intent <words>` (the director's seam): the intent read anew, the
        plan dropped and worked again at the next judgement; the words for the journal."""
        self.intent = read_intent(self.world, words)
        self.intent_words = " ".join(words.split())
        self.role = role_for(self.world, self.intent)
        self.doctrine = load_doctrine(self.role)
        self.legs, self.leg_i, self.leg_shaped_tick = [], 0, None
        self._business = {}
        self.error = ""
        if self.state is not None:
            self._leave(self.state)
            self.state = None
        return f"the captain's intent: {self.intent.words}"

    def player_hand(self, text: str) -> None:
        """The player's hand on an intent scenario (decision 41): an order of the ship's
        given at the prompt while the captain commands makes him stand aside, said once
        in the log; his state's book is struck so that no rule of his fights the player's
        helm, his intent and his plan kept for `captain: carry on`."""
        if not self.commands or self.state is None:
            # not yet in command (the scenario's opening orders come before his first
            # judgement, and a replay gives them again as the captain's): no hand
            return
        self.aside = True
        state = self.state
        self._leave(state)
        self.state = None
        words = f" and his book '{state}' struck"
        self.world.record(
            Severity.NOTABLE,
            "captain.aside",
            f"{self.name} stands aside at your order ({text!r}){words}; "
            "'captain: carry on' gives her back to him.",
            actor=actor_for(state),
            data={"order": text, "state": state, "intent": self.intent_words},
        )

    def carry_on(self) -> str:
        """`captain: carry on`: the captain commands again from where she is, his plan
        worked afresh at his next judgement; the words for the journal."""
        if not self.active:
            raise ValueError("The captain has no intent to carry on with; give him one first.")
        if not getattr(self, "aside", False):
            raise ValueError(f"{self.name} is not standing aside; he commands her.")
        self.aside = False
        self.legs, self.leg_i, self.leg_shaped_tick = [], 0, None
        self._business = {}
        self.last_judged = -1
        return f"{self.name} carries on: {self.intent.words if self.intent else ''}"

    def strike_state(self) -> None:
        """The colours struck (package 70; `combat.action.strike`): the machine enters
        `struck`, whose book is empty and whose work is to lie to for her captor."""
        if self.state == "struck":
            return
        if not isinstance(self.fired_on, set):
            self.fired_on = set()
        if self.active and self.commands:
            self._enter("struck")
        else:
            self.state = "struck"

    # -- an order over his head (spec M7b §3; package 62) ------------------------------

    # the director's hand: the tick until which he holds by an order given over his head as
    # his own, and its words; None when he sails by his own judgement (class defaults, so
    # that a checkpoint from before loads with none)
    over_head_until: int | None = None
    over_head_order: str = ""
    over_head_event: str = ""  # the event the hold was named until (package 66)

    def over_his_head(self, text: str, until: int, event: str = "") -> None:
        """An order of her own grammar given to her as his by the director's hand: he is
        told it came over his head, so that his book is struck as at the player's hand (no
        rule of his fights it) and his judgements are held until `until`, the director's
        next order to her setting it again; his intent and plan are kept, and taken up from
        where she is when the glass is out (`take_up_again`). Nothing of it is said: the
        order is in her log as his."""
        if self.over_head_until is None and self.state is not None:
            self._leave(self.state)
            self.state = None
        self.over_head_until = int(until)
        self.over_head_order = " ".join(str(text).split())
        self.over_head_event = str(event or "")

    def take_up_again(self) -> None:
        """The glass out (or the director's `carry on`): he commands again from where she
        is, his plan worked afresh at his next judgement, as at `captain: carry on`."""
        if self.over_head_until is None:
            return
        self.over_head_until = None
        self.over_head_order = ""
        self.over_head_event = ""
        self.legs, self.leg_i, self.leg_shaped_tick = [], 0, None
        self._business = {}
        self.last_judged = -1

    def _hold_event_came(self) -> bool:
        """The event the hold was named until come to her (package 66), read once a minute
        from her truth: a crewed World's own vessel in her parent's sea."""
        event = str(getattr(self, "over_head_event", "") or "")
        world = self.world
        if not event or world.clock.tick % 60:
            return False
        parent, vessel = getattr(world, "parent", None), getattr(world, "vessel", None)
        if parent is None or vessel is None:
            return False
        from freesail.world.crews import hold_event_came

        return hold_event_came(parent, vessel, event)

    # -- the tick ---------------------------------------------------------------------

    def tick(self) -> None:
        """Once a minute, when his judgements are given: perceive, judge the doctrine's
        transitions, and work the state."""
        world = self.world
        until = getattr(self, "over_head_until", None)
        if until is not None and (world.clock.tick >= until or self._hold_event_came()):
            self.take_up_again()
        if not self.commands:
            self._seen_log = len(world.log)
            return
        tick = world.clock.tick
        if tick - self.last_judged < JUDGE_EVERY_S and self.last_judged >= 0:
            return
        if self.last_judged < 0 and tick < JUDGE_FIRST_S:
            return
        self.last_judged = tick
        events = [world.log[i] for i in range(self._seen_log, len(world.log))]
        self._seen_log = len(world.log)
        p = Perception.read(world)
        self._read_trend(p)
        if self.state is None:
            self._enter(self._first_state(p))
        self._transitions(p)
        self._work(p, events)
        if self.state not in ("engaging", "struck"):
            self._rule_of_the_road(p)  # no giving way to an enemy in action (package 70)
        # the signals (package 71): what his people read this minute answered and obeyed,
        # the private signal made and judged, the colours by his doctrine
        from freesail.world import signalling

        signalling.near_minute(self, p)
        self._deck_by_rule()

    # -- the deck to a seated officer (package 41; spec M6 §11) --------------------------

    def _officer_held(self) -> Any:
        """A model or the player at the officer of the watch's station, seated and able
        to hold the deck (not released, not paused); None otherwise."""
        from freesail.agents.harness import holder_of

        held = holder_of(self.world, "officer of the watch")
        if held is None or not getattr(held, "started", True):
            return None
        a = held.agent
        if a.released or a.paused:
            return None
        return held

    def _deck_by_rule(self) -> None:
        """The rules-based captain over a seated officer (package 41, item 5): on an
        intent scenario with nobody at the captain's station, a model or the player at
        the officer's is given the deck by the captain's own words, his standing orders
        (the state's book) in force over it, and he takes it back for a judgement that
        needs the deck (`CAPTAIN_ON_DECK_STATES`: the gale, the shelter, a stranger, the
        chase, distress), saying so, and gives it again when the state is a quiet one.
        A deck the harness took from a silent or paused officer is not given again by
        rule: that is the owner's `resume` or his word."""
        if self.seated or self.state is None:
            return
        held = self._officer_held()
        if held is None:
            return
        a = held.agent
        world = self.world
        wants = self.state not in CAPTAIN_ON_DECK_STATES
        actor = actor_for(self.state)
        if wants and not a.deck and not a.deck_lost:
            try:
                words = held.give_deck(by=self.name)
            except Exception:  # refused in words (no authority, paused): no deck by rule
                return
            world.record(
                Severity.NOTABLE,
                "agent.deck",
                f"{words} ({self.name}, by his rule, {self.state}; his standing orders "
                "stand over it.)",
                actor=actor,
                data={
                    "station": "officer of the watch",
                    "deck": "given",
                    "by": "rule",
                    "state": self.state,
                },
            )
        elif not wants and a.deck:
            try:
                words = held.take_deck(by=self.name)
            except Exception:
                return
            world.record(
                Severity.NOTABLE,
                "agent.deck",
                f"{words} ({self.name} takes the deck for a judgement that needs it: "
                f"{self.state}.)",
                actor=actor,
                data={
                    "station": "officer of the watch",
                    "deck": "taken",
                    "by": "rule",
                    "state": self.state,
                },
            )

    # -- states ------------------------------------------------------------------------

    def _first_state(self, p: Perception) -> str:
        if p.aground:
            return "in distress"
        if p.anchor_down and p.in_port:
            self._departing = p.in_port
            return "in port"
        if p.anchor_down:
            return "at anchor"
        if self.intent is not None and self.intent.kind == "station" and self._on_station(p):
            return "keeping station"
        return "on passage"  # a member of a set: `_enter` makes it `in company` (package 72)

    def _enter(self, state: str) -> None:
        world = self.world
        # package 72 (spec M7 §21): a member of a set enters `in company` where her
        # doctrine would enter a plan state; the set is the parent World's, and the
        # player's own ship may be a member of one
        from freesail.world.squadrons import plan_state_of

        root = getattr(world, "parent", None) or world
        own = str(getattr(getattr(world, "vessel", None), "id", "") or "the ship")
        state = plan_state_of(root, own, state)
        old = self.state
        if old is not None:
            self._leave(old)
        self.state = state
        self._state_entered = world.clock.tick
        lines = self._book_lines(state)
        runtime = getattr(world, "standing", None)
        loaded = []
        if runtime is not None and lines:
            loaded = runtime.load_book(state, lines, actor_for(state))
        said = f"{self.name}: {state}"
        if self.intent is not None:
            said += f" ({self.intent.words})"
        if loaded:
            said += f"; his book '{state}' loaded: {', '.join(loaded)}"
        world.record(
            Severity.NOTABLE,
            "captain.state",
            said + ".",
            actor=actor_for(state),
            data={"state": state, "from": old, "book": loaded, "intent": self.intent_words},
        )
        self._on_enter(state, old)

    def _leave(self, state: str) -> None:
        runtime = getattr(self.world, "standing", None)
        if runtime is not None:
            runtime.unload_book(state, actor_for(state))

    def _book_lines(self, state: str) -> list[str]:
        """The state's book from the doctrine's template, the placeholders filled with
        the plan's words; a line whose placeholder has no value is left out."""
        if self.doctrine is None:
            return []
        fills = self._fills()
        out = []
        # while the pilot has the conn (package 45) the book's course lines are left out,
        # or the hourly "the leg" would take her back from him at the hour; and so when the
        # conn was the officer's to give (package 58b: the pilot brought her up to wait for
        # the flood to slacken, and the book written again at the weigh carried "the leg",
        # which shaped her back out of the Goulet for the outer mark under the pilot's feet)
        conn = bool(self._business.get("conn_given")) or self._pilot_has_conn()
        for line in self.doctrine.book(state):
            if conn and 'standing order "the leg"' in line:
                continue
            try:
                out.append(line.format_map(fills))
            except (KeyError, IndexError, ValueError):
                continue
        return out

    def _pilot_has_conn(self) -> bool:
        view = getattr(self.world, "readings", None)
        pilot = view.value("pilot") if view is not None else None
        return isinstance(pilot, dict) and bool(pilot.get("conn"))

    def _fills(self) -> dict[str, Any]:
        d = self.doctrine
        fills: dict[str, Any] = {k: v for k, v in (d.thresholds if d else {}).items()}
        # package 70: the fighting book's words from the doctrine and the nation's habit
        habit = self._habit()
        fills["aim"] = {"hull": "her hull", "rigging": "her rigging"}.get(
            str(habit["aim"]), "between wind and water"
        )
        fills["charge"] = {
            "round": "round shot",
            "chain": "chain shot",
            "grape": "grape",
            "double": "double shot",
        }.get(str(habit["charge"]), "round shot")
        fills["engage_range_cables"] = f"{habit['engage_range_cables']:g}"
        fills["break_off_cables"] = f"{habit['break_off_cables']:g}"
        leg = self.legs[self.leg_i] if self.legs and self.leg_i < len(self.legs) else None
        if leg is not None:
            fills["mark"] = leg.words
            fills["reached"] = f"{leg.reached_nm:g}"
        if self.intent is not None:
            station = self._station_mark()
            if self.intent.kind == "station" and station is not None:
                fills["station"] = station[0]
                fills["radius"] = f"{self.intent.radius_nm:g}"
                fills["radius_out"] = f"{self.intent.radius_nm * 2:g}"
                fills["radius_in"] = f"{max(1.0, self.intent.radius_nm * 0.6):g}"
            port = self._port_of(self.intent.destination)
            if port is not None:
                fills["port"] = port.name
                # the spot by its chart name where it has a feature (Falmouth's outer road
                # is 'the outer road' in the port file, which no 'distance to' reads;
                # package 40c), else the port file's name
                fills["road"] = self._spot_words(port.outer_road)
                fills["anchorage"] = self._spot_words(port.anchorage)
                depth_m = getattr(port.anchorage, "depth_m", None)
                fills["anchorage_fathoms"] = (
                    f"{units.m_to_fathoms(float(depth_m)) + 2.0:.0f}"
                    if depth_m
                    else str(ANCHORAGE_FATHOMS)
                )
                fills["cast_in"] = getattr(port.pilot, "cast", "starboard")
                course_in = self._course_in(port)
                fills["course_in"] = course_in
            origin = self._port_of(self.intent.origin)
            if origin is not None:
                fills["cast_out"] = getattr(origin.pilot, "cast", "starboard")
                fills["course_out"] = units.point_name(
                    math.radians(float(getattr(origin.pilot, "course_out_deg", 180.0)))
                )
        fills["light_sail"] = self._light_sail()
        fills["storm_topsail"] = self._storm_topsail()
        return fills

    def _spot_words(self, spot: Any) -> str:
        feature = getattr(spot, "feature_id", None) or getattr(spot, "feature", None)
        chart = getattr(self.world, "chart", None)
        if feature and chart is not None:
            f = chart.feature(str(feature))
            if f is not None:
                return str(f.name)
        return str(getattr(spot, "name", "") or "")

    def _light_sail(self) -> str:
        """The sail taken in at the pilot's hail, by the ship's own names: the fore
        topsail where she has one, else the topsail (a cutter)."""
        sails = getattr(self.world.ship, "sails", {}) or {}
        if "fore.topsail" in sails:
            return "fore topsail"
        if "topsail" in sails:
            return "topsail"
        return "topsails"

    def _storm_topsail(self) -> str:
        """The topsail she lies to under in a gale, by the ship's own names (package 37p):
        the one `lie a-try` keeps, on the mast with the most square sail (the main topsail
        of a ship or a brig, the fore topsail of a topsail schooner), else as
        `_light_sail`."""
        ship = self.world.ship
        try:
            from freesail.evolutions.runner import part_name
            from freesail.evolutions.scripts import _topsails_on, yards_to_back

            kept = _topsails_on(ship, yards_to_back(ship))
        except (AttributeError, KeyError, TypeError, ValueError):
            kept = []
        return part_name(ship, kept[0].id) if kept else self._light_sail()

    def _course_in(self, port: Any) -> str:
        """The course from the outer road to the first inner mark, for the book that
        gets her under way for the port; east by default."""
        inner = Planner(self.world)._port_track(port, "in")
        if inner:
            bearing, _ = bearing_and_distance(port.outer_road.position, inner[0].position)
            return units.point_name(math.radians(bearing))
        return "E"

    def _port_of(self, place: str) -> Any:
        ports = getattr(self.world, "ports", None)
        return (
            (getattr(ports, "ports", None) or {}).get(place)
            if ports is not None and place
            else None
        )

    def _fill_away_first(self) -> None:
        """A state that sails her, entered hove to (the gale over, or the land under her
        lee while she lies to): filled away first, or every course is refused (package
        40c, the captain's trials: the frigate drifted onto Ushant hove to, her courses
        refused)."""
        manoeuvre = str(self.world.readings.value("manoeuvre_in_hand") or "")
        if manoeuvre in ("hove to", "heaving to"):
            # his own heave-to (the weather's) to undo: a heave-to the book orders for a
            # pilot's boat is the book's, and is not touched
            self._business["filling"] = True
        if manoeuvre == "hove to":
            self.give("fill away", why="to make sail")

    def _on_enter(self, state: str, old: str | None = None) -> None:
        """What is ordered on entering a state, beyond the book."""
        world = self.world
        if old == "engaging" and state != "struck":
            # the action over (the mark struck, lost or out of range): the guns silent and
            # secured, the hands back under the watch bill (package 70)
            self.give("cease firing", why="the action over")
            self.give("secure the guns", why="the action over")
            self._business.pop("engaged_side", None)
            self._business.pop("steered_for", None)
        if state == "hove to for weather":
            # package 37p: shortened, the jibs in by their ratings and the storm staysails
            # over the storm line (`orders.storm`), and lying to under the close-reefed
            # main topsail and the staysails as Luce has a ship lie to in a gale (1884,
            # ch. XXIX: "The ship is now 'lying to' under close-reefed main topsail, fore
            # storm staysail"), where heaving to with the main topsail aback took the
            # frigate astern at five knots and failed in the trials
            self.give("shorten sail")
            if self._lugger_storm_lug():
                # package 58b (item 5): a lugger has no topsail to lie a-try under; she lies
                # to under her own storm canvas, the taille-vent in the main lug's place
                # (Forfait 1788 p. 52: tacked at the foot of the mast, "safe aback") and the
                # storm jib in the jib's, hove to when it is set (the heave-to lowers the fore
                # lug, hauls the mizen flat aft and the storm jib to windward)
                self.give("shift the mainsail for the storm lug", why="to lie to in a gale")
                self.give("shift the jib for the storm jib", why="to lie to in a gale")
                self._business["lie_to_storm_lug"] = True  # hove to when the storm jib is set
                return
            self.give("lie a-try")
            return
        sailing_states = ("on passage", "beating", "running for shelter")
        if old == "hove to for weather" and state in sailing_states:
            # package 58b (item 5; 57's gale trial): filled away from lying to with the wind
            # still over his shorten-sail line (the gale over by the glass, or the land under
            # her lee) she was left under the storm canvas alone, had no way, lay aback every
            # three minutes and drove onto the islands; she makes sail to go through the
            # water, the topsails set as they stand close-reefed ("Keep her a good full!",
            # Luce 1884, ch. XXIV, p. 414; ch. XXIX), before the sail after the gale by steps
            why = self._sail_to_fill_away()
            if why:
                self.give("set the topsails", why=why)
        lying_to = False
        if old == "at anchor" and state in ("on passage", "beating", "running for shelter"):
            # the at-anchor book's "at under way then set plain sail" is unloaded here,
            # before the anchor is catted and the ship says she is under way (package
            # 40c: the schooner left the road under her topsail alone): he gives it at
            # `ship.under_way` himself (`_work`)
            self._business["weighing"] = True
        elif state in ("on passage", "beating", "running for shelter") and old != "at anchor":
            # under way with no sail set (package 43b, from package 44's regatta: a captain
            # started so made none for a day): sail made as after weighing, the topsails
            # alone in a wind over the doctrine's shortening line
            self._sail_if_none()
        if state != "at anchor":
            self._fill_away_first()
            manoeuvre = str(world.readings.value("manoeuvre_in_hand") or "")
            lying_to = manoeuvre in ("hove to", "heaving to")
        if state in ("on passage", "beating", "running for shelter"):
            self._business.pop("sailing", None)
            # a course while she lies to is refused; it is shaped when she has filled
            # away (`_work`, at `ship.filled_away`)
            if lying_to:
                return
            if self.legs and self.leg_i < len(self.legs) and self.legs[self.leg_i].kind != "out":
                self._shape_leg()
        elif state == "investigating a stranger":
            self.give("make her out")
        elif state == "chasing":
            self.give(self._chase_order(Perception.read(world)))
        elif state == "keeping station":
            station = self._station_mark()
            if station is not None:
                self.give(f"shape a course for {station[0]}")
        elif state == "in company":
            # package 72: her station in her set taken up at once; the book keeps it
            try:
                self.give("keep your station", why="her station in the set")
            except Exception:  # noqa: BLE001 - the flag not in sight: the book tries again
                pass
        elif state == "evading":
            self._haul_off(Perception.read(world))
        elif state == "engaging":
            self._engage_now(Perception.read(world))
        elif state == "struck":
            # the colours down: she lies to for her captor (package 70; what follows is 74's)
            manoeuvre = str(world.readings.value("manoeuvre_in_hand") or "")
            lying = manoeuvre in ("hove to", "heaving to") or bool(
                (getattr(world.ship, "extra", None) or {}).get("hove_to")
            )
            if not lying and not self._business.get("struck_lying_to"):
                self._business["struck_lying_to"] = True
                self.give("heave to", why="the colours struck")

    # -- the doctrine's transitions: `Judgement` (the mixin shared with the far body) --

    # -- the work of each state ---------------------------------------------------------

    def _work(self, p: Perception, events: list[Any]) -> None:
        state = self.state
        if state is None:
            return
        kinds = {e.kind for e in events}
        self._damage_work(p)
        if self._business.get("filling") and p.manoeuvre == "hove to":
            # a sailing state entered while she was still heaving to for the weather
            # (package 40c): the fill away waits for the heave-to to finish, and is given
            # here once a minute until she fills, every course being refused while she
            # lies to; a heave-to of the book's (the pilot's boat) is not his to undo
            self.give("fill away", why="to make sail")
            return
        sailing = ("on passage", "beating", "running for shelter")
        if "ship.under_way" in kinds and self._business.pop("weighing", False):
            self.give("set plain sail", why="under way from the anchor")
        filled = "ship.filled_away" in kinds and state in sailing
        if filled and self._business.pop("filling", False):
            # his own fill away done (not the book's after a pilot): the leg shaped now
            if self.legs and self.leg_i < len(self.legs) and self.legs[self.leg_i].kind != "out":
                self._shape_leg(why="filled away")
        self._weather_work(p, kinds)
        if state not in ("at anchor", "in port", "in distress"):
            self._head_sails_straining(p, events)
        if state == "hove to for weather" and self._business.get("lie_to_storm_lug"):
            # the lugger's storm jib set: she is hove to under it and the taille-vent
            from freesail.ship.parts import SailState

            ship_sails = getattr(self.world.ship, "sails", {}) or {}
            jib = ship_sails.get("storm_jib")
            if jib is not None and jib.is_set and p.manoeuvre not in ("hove to", "heaving to"):
                self._business.pop("lie_to_storm_lug", None)
                self.give("heave to", why="under the taille-vent and the storm jib")
            elif (
                jib is not None
                and jib.state is SailState.FURLED
                and not self._business.get("storm_jib_set")
            ):
                # shifted for the jib already hauled down, it is bent and furled: set it
                self._business["storm_jib_set"] = True
                self.give("set the storm jib", why="to lie to under it")
        if state in ("on passage", "beating", "running for shelter"):
            if self._casts(p, kinds):
                return  # brought to for the deep-sea lead: the leg waits for the cast
            self._passage(p, events, kinds)
        elif state == "in port":
            self._in_port(p)
        elif state == "keeping station":
            self._station(p)
        elif state in ("investigating a stranger", "chasing"):
            self._keep_stranger(p)
        elif state == "evading":
            if p.tick - (self._business.get("hauled_off", -(10**9))) >= 600:
                self._haul_off(p)
        elif state == "engaging":
            self._engaging(p)
        elif state == "at anchor":
            if "ship.under_way" in kinds or "ship.weighed" in kinds:
                self._waiting_at_road = False
        if "sail.across_the_stern" in kinds and state not in ("hove to for weather", "in distress"):
            self._across_the_stern(events)
        if "ship.brought_up" in kinds:
            self._business["brought_up"] = True
        if "ship.under_way" in kinds or "ship.aweigh" in kinds:
            self._business.pop("brought_up", None)

    def _lugger_storm_lug(self) -> bool:
        """A lugger with her storm lug in the sail room or bent (package 58b, item 5): no
        topsail to lie a-try under, and the taille-vent for a blow."""
        ship = self.world.ship
        sails = getattr(ship, "sails", {}) or {}
        try:
            from freesail.evolutions.scripts import _lugs_all
        except ImportError:  # pragma: no cover
            return False
        return bool(_lugs_all(ship)) and "taille_vent" in sails

    def _sail_to_fill_away(self) -> str:
        """Why she makes sail as she fills away from lying to (package 58b, item 5), or "":
        the wind still over `shorten_sail_kn` and a topsail not set, she would have no way
        under the storm canvas alone; the land under her lee says it is to claw off."""
        p = Perception.read(self.world)
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        if p.wind_kn < float(th("shorten_sail_kn", 30)) or p.topsails_all_set:
            return ""
        if self._stimulus("lee shore", p):
            return "to claw off the land under her lee"
        return "to give her way, the wind still strong"

    def _head_sails_straining(self, p: Perception, events: list[Any]) -> None:
        """A head sail straining at its bolt-ropes in a wind over `shorten_sail_kn` is taken
        in before it blows out (package 58b, item 5; 57's gale trial: the fore topmast
        staysail strained at 08:16 and at 08:26 and split at 08:29, the jib hauled down and
        it left standing). The storm staysails are the book's storm canvas, and stand."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        if p.wind_kn < float(th("shorten_sail_kn", 30)):
            return
        ship = self.world.ship
        try:
            from freesail.evolutions.scripts import head_sails
        except ImportError:  # pragma: no cover
            return
        groups = getattr(ship, "groups", {}) or {}
        storm = set(groups.get("storm staysails", [])) | set(groups.get("storm canvas", []))
        heads = {sl.id for sl in head_sails(ship)} - storm
        done = self._business.setdefault("head_sails_in", {})
        for e in events:
            sid = getattr(e, "subject", None)
            if e.kind != "strain.warning" or sid not in heads or "bolt-ropes" not in e.text:
                continue
            if p.tick - int(done.get(sid, -(10**9))) < 600:
                continue
            done[sid] = p.tick
            self.give(f"take in the {self._sail_name(sid)}", why="straining at the bolt-ropes")

    def _casts(self, p: Perception, kinds: set[str]) -> bool:
        """The lead on a long leg (package 58b, item 2): the hand lead every glass where the
        chart has under `cast_glass_fathoms` at the account, the deep-sea lead every hour in
        deeper water within `cast_hour_fathoms`; for the deep-sea lead she is brought to
        when her way is over the four knots it wants (Falconer 1780, 'Sounding': "it is
        usual previously to bring-to the ship"), only in a wind under `shorten_sail_kn`, and
        filled away when the cast is had. Not in pilot water (its own lead goes), with the
        pilot aboard, at anchor or lying to. True while she is brought to for a cast, so
        that the leg is not shaped against the heave-to."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        b = self._business
        brought = b.get("cast_brought_to")
        if brought is not None:
            if "sounding" in kinds or p.tick - int(brought) >= 900:
                # the cast had (or a quarter of an hour gone without one): filled away
                b.pop("cast_brought_to", None)
                b.pop("cast_given", None)
                if p.manoeuvre in ("hove to", "heaving to"):
                    self.give("fill away", why="the cast had")
                return False
            if p.manoeuvre == "hove to" and p.speed_kn < 3.0 and not b.get("cast_given"):
                b["cast_given"] = True
                self.give("heave the deep-sea lead", why="brought to for a cast")
            return True
        if p.chart_fathoms is None or self._inner_leg() or p.pilot_aboard:
            return False
        if p.anchor_down or p.aground or p.manoeuvre in ("hove to", "heaving to"):
            return False
        if "cast_tick" not in b:
            # the first cast a glass or an hour into the leg, not at its laying: cast at
            # once, the deep-sea lead held the hands from a cruiser's heave-to for her
            # station (truth 7b-113) and the book's own lead goes in pilot water
            b["cast_tick"] = p.tick
            return False
        last = int(b["cast_tick"])
        if p.chart_fathoms < float(th("cast_glass_fathoms", 20)):
            if p.tick - last >= 1800:
                b["cast_tick"] = p.tick
                self.give("heave the lead", why="in soundings on the leg")
            return False
        if p.chart_fathoms >= float(th("cast_hour_fathoms", 100)) or p.tick - last < 3600:
            return False
        # inshore: the land in sight, or the coast by his account within `cast_inshore_nm`
        # (taken another way: brought to every hour across the open Channel, the schooner
        # on her intent lost a quarter of her time to it and never made Brest in 36 hours)
        coast = p.coast_by_account_nm
        if p.land_in_sight and p.nearest_land_nm is not None:
            coast = p.nearest_land_nm
        if coast is None or coast > float(th("cast_inshore_nm", 15)):
            return False
        b["cast_tick"] = p.tick
        if p.speed_kn <= 4.0:
            self.give("heave the deep-sea lead", why="inside the hundred-fathom line")
            return False
        # brought to for it only once a watch (`cast_bring_to_hours`), and not in a blow:
        # brought to every hour, the schooner on her intent lost an hour in four along the
        # coast of Léon (taken another way, package 58b)
        # (nor beating, nor with the land under her lee within her sea room: hove to for a cast
        # off the Léon coast after the gale, the frigate drove toward it and took the ground)
        last_brought = int(b.get("cast_brought_tick", -(10**9)))
        if (
            self.state == "beating"
            or p.wind_kn >= float(th("shorten_sail_kn", 30))
            or (p.lee_land_nm is not None and p.lee_land_nm <= float(th("sea_room_nm", 10)))
            or p.tick - last_brought < 3600.0 * float(th("cast_bring_to_hours", 4))
        ):
            return False
        e = self.give("heave to", why="to bring her to for a cast of the deep-sea lead")
        if e.kind != "order.rejected":
            b["cast_brought_to"] = p.tick
            b["cast_brought_tick"] = p.tick
            return True
        return False

    def _across_the_stern(self, events: list[Any]) -> None:
        """The sail work after the wind has come across the stern (package 58b, item 3; the
        owner's ruling of 2026-10-23: nothing is ordered by the helm, and the sail work is
        the captain's judgement): his next orders are the lugs left against their masts
        dipped, the yards left by the lee braced round, and a boom that came over by itself
        sheeted for its new side, each by its own order. The deck's line said what was
        left (`navigation.watch_the_stern`); a lug since dipped is refused as done."""
        crossed = [e for e in events if e.kind == "sail.across_the_stern"]
        if not crossed:
            return
        data = crossed[-1].data or {}
        sails = getattr(self.world.ship, "sails", {}) or {}
        why = "the wind across the stern"
        for sid in data.get("lugs") or []:
            sl = sails.get(sid)
            if sl is not None and sl.is_set:
                self.give(f"dip the {self._sail_name(sid)}", why=why)
        if data.get("yards"):
            self.give("trim sails", why=why)
        elif data.get("booms"):
            self.give("trim the sheets", why=why)

    def _sail_if_none(self) -> None:
        """Plain sail made when she is under way with none set (package 43b), the topsails
        alone over `shorten_sail_kn`; nothing when a sail is set or the anchor is down."""
        world = self.world
        ship = getattr(world, "ship", None)
        if ship is None or any(s.is_set for s in ship.sails.values()):
            return
        p = Perception.read(world)
        if p.anchor_down or p.anchoring or p.aground:
            return
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        if p.wind_kn > float(th("shorten_sail_kn", 30)):
            self.give("set the topsails", why="under way with no sail set, the wind strong")
        else:
            self.give("set plain sail", why="under way with no sail set")

    def _weather_work(self, p: Perception, kinds: set[str]) -> None:
        """Sail after the gale, whatever his state (package 45, Part B item 5; 37p's open
        point: the station trial beat for the station under the main topsail and two
        staysails to the end, the hove-to book's line having unloaded with the book); a
        head sail blown out replaced from the sail room; and the glass (item 6): sail
        shortened by the book's next line a step before the gale line when the weather
        is worsening."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        shorten_kn = float(th("shorten_sail_kn", 30))
        again_kn = float(th("sail_again_kn", 25))
        minutes = float(th("sail_again_minutes", 30))
        if self.trend == "mending":
            minutes = minutes / 2.0
        if p.wind_kn >= shorten_kn:
            self._business["gale_met"] = True
            self._business.pop("made_sail_after", None)
            self._business.pop("sail_step", None)
        if p.wind_kn < again_kn:
            if self._calm_since is None:
                self._calm_since = p.tick
        else:
            self._calm_since = None
        lying = p.manoeuvre in ("hove to", "heaving to") or p.anchor_down or p.aground
        sailing = self.state not in ("hove to for weather", "at anchor", "in port", "in distress")
        # worsening: the book's next line a step sooner than its own threshold
        if (
            self.trend == "worsening"
            and sailing
            and not lying
            and p.topsail_reefs == 0
            and p.wind_kn >= shorten_kn - float(th("worsening_sooner_kn", 6))
            and not self._business.get("shortened_sooner")
        ):
            self._business["shortened_sooner"] = True
            self.give("shorten sail", why="the glass falling and the wind rising")
        if p.wind_kn < shorten_kn - float(th("worsening_sooner_kn", 6)):
            self._business.pop("shortened_sooner", None)
        # sail again after the gale, by steps (package 45c; Luce 1884 ch. XXIX p. 479:
        # "After the gale abates, sail should not be made upon the vessel too rapidly"):
        # the topsails as they stand reefed when the wind has been under the shorten-sail
        # line for `topsails_again_minutes`; the topgallant masts swayed up, the reefs out
        # and the jib when it has been under `sail_again_kn` for `sail_again_minutes`; the
        # rest of the plain sail, the courses last, when it has stayed under that line
        # `courses_again_minutes` more and the reefs are out (a first version set the
        # courses while the watch was still shaking out the reefs: the yards went untrimmed
        # after a tack for want of hands, and off the Léon coast she lay aback by turns,
        # went astern and took the ground in the lee-shore trial). Package 45's one step
        # (plain sail at once, and the books' "under way again" at the fill away in thirty
        # knots) had the frigate in the station trial aback by turns for the hour after it.
        steps = self._business
        if p.wind_kn < shorten_kn:
            steps.setdefault("easing_since", p.tick)
        else:
            steps.pop("easing_since", None)
        gale = bool(steps.get("gale_met")) and sailing and not lying
        easing = steps.get("easing_since")
        if (
            gale
            and not steps.get("sail_step")
            and easing is not None
            and p.tick - int(easing) >= float(th("topsails_again_minutes", 10)) * 60.0
            and not p.topsails_all_set
        ):
            steps["sail_step"] = 1
            self.give("set the topsails", why="the gale easing")
        calm = self._calm_since is not None and p.tick - self._calm_since >= minutes * 60.0
        # the topgallant masts are all hands at the mast-ropes for half an hour and more,
        # which holds a tack the offing asks for: not with the land under her lee within
        # `lee_shore_nm`, where they wait for the sea room (the lee-shore trial off the Léon
        # coast, a first version: the offing's tack waited twenty minutes behind them, she
        # missed stays, fell off along the shore and took the ground at the hour's wear); the
        # reefs, the jib and the courses do not wait, since she claws off under them
        sea_room = p.lee_land_nm is None or p.lee_land_nm > float(th("lee_shore_nm", 6))
        if (
            gale
            and calm
            and sea_room
            and int(steps.get("sail_step") or 0) >= 2
            and steps.get("masts_wait")
        ):
            steps.pop("masts_wait", None)
            self.give("sway up the topgallant masts", why="the land no longer under her lee")
        if (
            gale
            and calm
            and int(steps.get("sail_step") or 0) < 2
            and (
                p.topsail_reefs > 0
                or p.storm_staysails_set
                or p.headsails_blown
                or not p.topsails_all_set
                or not p.courses_set
            )
        ):
            steps["sail_step"] = 2
            steps["sail_step_tick"] = p.tick
            why = "the gale over" + (", the weather mending" if self.trend == "mending" else "")
            if p.topsail_reefs > 0 or p.storm_staysails_set:
                if sea_room:
                    self.give("sway up the topgallant masts", why=why)
                else:
                    steps["masts_wait"] = True
                self.give("shake out the reefs in the topsails", why=why)
            for sid in p.headsails_blown:
                if p.wind_kn < float(th("wear_wind_kn", 30)):
                    self.give(f"bend a new {self._sail_name(sid)}", why="blown out in the gale")
            if not p.topsails_all_set:
                self.give("set the topsails", why=why)
            self.give("set the jib", why=why)
        if (
            gale
            and calm
            and int(steps.get("sail_step") or 0) == 2
            and p.topsail_reefs == 0
            and p.tick - int(steps.get("sail_step_tick") or p.tick)
            >= float(th("courses_again_minutes", 15)) * 60.0
        ):
            steps["sail_step"] = 3
            steps["made_sail_after"] = True
            steps.pop("gale_met", None)
            self.give("set plain sail", why="the courses last, the gale over")
        # a head sail bent again after the gale, and not yet set
        if (
            self._business.get("made_sail_after")
            and sailing
            and not lying
            and p.headsails_bent
            and not p.headsail_set
            and p.wind_kn < float(th("wear_wind_kn", 30))
            and p.tick - self._business.get("headsail_set_tick", -(10**9)) >= 600
        ):
            self._business["headsail_set_tick"] = p.tick
            self.give(f"set the {self._sail_name(p.headsails_bent[0])}", why="bent anew")

    def _sail_name(self, sid: str) -> str:
        try:
            from freesail.evolutions.runner import part_name

            return part_name(self.world.ship, sid)
        except (AttributeError, KeyError, TypeError, ValueError, ImportError):
            return sid.replace(".", " ").replace("_", " ")

    def _passage(self, p: Perception, events: list[Any], kinds: set[str]) -> None:
        if not self.legs:
            self._plan(p)
            if not self.legs:
                return
            if self.legs[0].kind != "out":
                self._shape_leg()
            return
        if self.leg_i >= len(self.legs):
            return
        leg = self.legs[self.leg_i]
        for e in events:
            if e.kind == "helm.set" and (e.data or {}).get("verb") == "shape a course for":
                # the leg as laid, the stream allowed then (package 58b, item 1), by his
                # rule or his book's hourly "the leg"
                shaped = e.data or {}
                self._business["laid"] = {
                    "tick": e.tick,
                    "line_deg": shaped.get("line_deg"),
                    "allowing": dict(shaped.get("allowing") or {}),
                }
            if e.kind == "helm.set" and state_of_actor(str(e.actor or "")) is not None:
                data = e.data or {}
                self._business["course_not_laid"] = bool(data.get("course_not_laid"))
                # the course shaped and her close-hauled angle, for the one rule's verdict
                # (package 43b, `_course_verdict`)
                if data.get("heading") is not None:
                    from freesail.evolutions.scripts import close_hauled_true_angle

                    self._business["course_heading_deg"] = (
                        units.rad_to_deg(float(data["heading"])) % 360.0
                    )
                    self._business["course_closest_deg"] = units.rad_to_deg(
                        close_hauled_true_angle(self.world.ship)
                    )
                if (data.get("helm") or {}).get("held_for") == "way":
                    # shaped before she had way (package 58b, item 4): held by the helm, and
                    # shaped again when she has it, the stream then allowed for
                    self._business["held_for_way"] = True
        gathered = any(
            e.kind == "helm.course_given" and (e.data or {}).get("held_for") == "way"
            for e in events
        )
        if gathered and self._business.pop("held_for_way", False) and leg.kind != "out":
            self._shape_leg(why="she has gathered way")
            return
        if "ship.filled_away" in kinds and p.manoeuvre not in ("hove to", "heaving to"):
            if leg.kind != "out":
                self._shape_leg()
        if self._business.get("course_not_laid") and self._inner_leg():
            # a course not laid in pilot water (package 40c, the captain's trials: the
            # schooner beat up the Goulet and took the ground on the Fillettes). Most often
            # it is the allowance for the stream that brings the steered course up to the
            # wind, the stream running along the channel; then she is conned for the mark
            # with the stream under her: by the pilot, who has the conn (package 45), or
            # by the rhumb line. A wind foul for the leg itself (`ENTRY_POINTS`) is waited
            # out at anchor, the at-anchor book trying again on the flood by day.
            self._business.pop("course_not_laid", None)
            if self._leg_serves(leg, p) and self._conn_for(leg, p):
                return
            port = self._port_of(leg.port)
            where = port.name if port is not None else leg.words
            self._waiting_at_road = True
            self.give("come to an anchor", why=f"the wind does not serve to enter {where}")
            self._enter("at anchor")
            return
        if p.pilot_conn and self._inner_leg():
            # the pilot conns her (package 45): no course of the captain's fights his, the
            # legs advance by account for the anchor
            dist = self._distance_by_account(leg)
            if dist is not None and (dist <= leg.reached_nm or self._passed(leg)):
                self._leg_reached(leg, p)
            return
        if self._business.get("conn_given") and not p.pilot_conn and not p.pilot_aboard:
            # the pilot gone (put off, or he gave her up): the captain has her again, his
            # book whole
            self._business.pop("conn_given", None)
            self._reload_leg_book()
        elif self._business.get("conn_given") and not p.pilot_conn:
            # the pilot aboard but the conn given up (a helm order of the book's or the
            # officer's): the captain conns the leg himself, his book whole
            self._business.pop("conn_given", None)
            self._business["conn_refused"] = True
            self._reload_leg_book()
            self._shape_leg(why="the pilot gave her up")
            return
        dist = self._distance_by_account(leg)
        if dist is not None and (dist <= leg.reached_nm or self._passed(leg)):
            self._leg_reached(leg, p)
            return
        if "lookout.land_ahead" in kinds and leg.kind != "out":
            self._shape_leg(why="land ahead")
            return
        relay = self._stream_changed(p, events, leg)
        if relay:
            self._shape_leg(why=relay)

    def _stream_changed(self, p: Perception, events: list[Any], leg: Leg) -> str:
        """Why the leg is to be laid again for the stream (package 58b, item 1), or "": the
        master's tide turned since it was laid (his `reckoning.tide` line), or the stream he
        allows now differs from the one the course was laid for by enough across the line to
        carry her `RELAY_OFF_LINE_NM` off it in the next glass. On passage or running for
        shelter, on a leg he shapes (not the pilot's water nor the road's way out), not lying
        to, and not within `RELAY_LEAST_S` of the last laying; never for the captain's own
        set ordered, which the master holds whatever the tide."""
        if self.state not in ("on passage", "running for shelter") or leg.kind == "out":
            return ""
        if self._inner_leg() or p.pilot_conn or p.manoeuvre in ("hove to", "heaving to"):
            return ""
        laid = self._business.get("laid")
        if not isinstance(laid, dict) or laid.get("line_deg") is None:
            return ""
        since = p.tick - int(laid.get("tick", p.tick))
        now = p.tide_allowed or {}
        turned = [e for e in events if e.kind == "reckoning.tide" and (e.data or {}).get("turn")]
        if turned:
            # the master's turn, kept until the leg is laid again (it may come within
            # minutes of a laying, and is answered when the ten minutes are out)
            flood = bool((turned[-1].data or {}).get("flood"))
            self._business["tide_turned"] = ("flood" if flood else "ebb", turned[-1].tick)
        pending = self._business.get("tide_turned")
        if pending and int(laid.get("tick") or 0) > int(pending[1]):
            self._business.pop("tide_turned", None)  # laid again since the turn
            pending = None
        if now.get("by") == "captain" or since < RELAY_TURN_LEAST_S:
            return ""
        from freesail.world.reckoning import rate_words, ward_words

        if pending:
            self._business.pop("tide_turned", None)
            return f"the tide has turned, the {pending[0]} making"
        if since < RELAY_LEAST_S:
            return ""

        def vector(tide: dict[str, Any]) -> tuple[float, float]:
            if "toward_deg" not in tide:
                return 0.0, 0.0
            knots = float(tide.get("knots") or 0.0)
            toward = math.radians(float(tide["toward_deg"]))
            return knots * math.sin(toward), knots * math.cos(toward)

        allowed = dict(laid.get("allowing") or {})
        line = math.radians(float(laid["line_deg"]))
        steer = math.radians(float(allowed.get("steer_deg", laid["line_deg"])))
        if not allowed.get("made_good", True) and abs(units.wrap_pi(steer - line)) < 0.01:
            allowed = {}  # no way on to work an allowance by: nothing was allowed
        e0, n0 = vector(allowed)
        e1, n1 = vector(now if now.get("by") == "book" else {})
        de, dn = e1 - e0, n1 - n0
        across = de * math.cos(line) - dn * math.sin(line)
        if abs(across) * RELAY_GLASS_H <= RELAY_OFF_LINE_NM:
            return ""
        if "toward_deg" in now and float(now.get("knots") or 0.0) > 0.0:
            toward = math.radians(float(now["toward_deg"]))
            stream = f"{rate_words(float(now['knots']))} {ward_words(toward)}"
        else:
            stream = "none"
        return f"the stream changed since the leg was laid: {stream} now"

    def _leg_serves(self, leg: Leg, p: Perception) -> bool:
        """Whether a leg of the inner track lies no nearer the wind than `ENTRY_POINTS`
        (package 45, Part B item 3a), from the account to its mark."""
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None or p.wind_from_deg is None:
            return True
        bearing, _ = bearing_and_distance(here, leg.position)
        off = abs(units.wrap_pi(math.radians(bearing - p.wind_from_deg)))
        return off >= ENTRY_POINTS * units.POINT

    def _entry_stop_for(self, p: Perception) -> int | None:
        """The inner track judged leg by leg from the one in hand (package 45, item 3a):
        the index of the last leg before the first that the wind will not serve, where
        she anchors if it is a port's road or anchorage; None when every leg serves."""
        if p.wind_from_deg is None or not self.legs:
            return None
        nav = getattr(self.world, "navigation", None)
        at = nav.account_now() if nav is not None else None
        if at is None:
            return None
        last_ok: int | None = None
        for i in range(self.leg_i, len(self.legs)):
            leg = self.legs[i]
            if not leg.port or leg.kind not in ("to", "anchorage", "road"):
                at = leg.position
                continue
            bearing, _ = bearing_and_distance(at, leg.position)
            off = abs(units.wrap_pi(math.radians(bearing - p.wind_from_deg)))
            if off < ENTRY_POINTS * units.POINT:
                return last_ok
            if leg.kind in ("road", "anchorage"):
                last_ok = i
            at = leg.position
        return None

    def _conn_for(self, leg: Leg, p: Perception) -> bool:
        """The helm given the rhumb line to the leg's mark by account, as a pilot conns
        her up a channel with the stream under her, when that line is laid; the pilot
        himself given the conn when he is aboard (package 45); False when the wind is
        foul for the line itself (`_leg_serves`)."""
        if not self._leg_serves(leg, p):
            return False
        if (
            p.pilot_aboard
            and not p.pilot_conn
            and not self._business.get("conn_given")
            and not self._business.get("conn_refused")
        ):
            self._business["conn_given"] = True
            e = self.give("let the pilot take her in", why="his water")
            if e.kind != "order.rejected":
                self._reload_leg_book()
                return True
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None:
            return False
        bearing, _ = bearing_and_distance(here, leg.position)
        point = units.point_name(math.radians(bearing))
        e = self.give(f"steer {point}", why=f"conning her for {leg.words}, the stream under her")
        return e.kind != "order.rejected"

    def _inner_leg(self) -> bool:
        """Whether the leg in hand is a port's inner track (its `in` marks or its
        anchorage): pilot water, where a course the wind will not allow is not beaten."""
        if not self.legs or self.leg_i >= len(self.legs):
            return False
        leg = self.legs[self.leg_i]
        return bool(leg.port) and (
            leg.kind == "anchorage" or (leg.kind == "to" and leg.reached_nm <= 0.5)
        )

    def _passed(self, leg: Leg) -> bool:
        """Whether the account has run past a mark of an inner track without reaching
        it within its distance (the account between the log's heaves swings, and the
        merchant book turned at a meridian for that): the mark bears abaft the beam of
        the leg's own direction, from the mark before it."""
        if leg.kind == "via":
            pass  # a mark sailed by (package 45) is left on its hand, however far off
        elif leg.kind not in ("to", "out") or self.leg_i == 0 or leg.reached_nm > 1.0:
            return False
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None:
            return False
        # the line to the mark: from the mark before it, or for the plan's first leg from
        # where the plan was laid (package 45; before, the first leg read the last)
        if self.leg_i > 0:
            start = self.legs[self.leg_i - 1].position
        elif self._plan_from is not None:
            start = self._plan_from
        else:
            return False
        along, _ = bearing_and_distance(start, leg.position)
        to_mark, dist = bearing_and_distance(here, leg.position)
        if abs(units.wrap_pi(math.radians(to_mark - along))) <= math.pi / 2.0:
            return False
        # abeam only within two miles of the mark or of the line to it (package 43b, the
        # master's way's rule, `WAY_PASSED_WITHIN_NM`: the regatta's mark far to windward)
        from freesail.world.geo import off_the_line_m
        from freesail.world.reckoning import WAY_PASSED_WITHIN_NM

        near = WAY_PASSED_WITHIN_NM * units.NAUTICAL_MILE
        return dist <= near or off_the_line_m(start, leg.position, here) <= near

    def _leg_reached(self, leg: Leg, p: Perception) -> None:
        world = self.world
        if leg.kind == "road":
            port = self._port_of(leg.port)
            if port is not None and not self._tide_serves(port, p, "enter"):
                self._waiting_at_road = True
                self.give("come to an anchor", why=f"the tide does not serve to enter {port.name}")
                self._enter("at anchor")
                return
        stop_here = self._entry_stop is not None and self.leg_i == self._entry_stop
        if stop_here and leg.kind != "anchorage":
            # as far in as the wind serves (package 45, item 3a): the next leg lies too
            # near the wind, and this is the last anchorage he can reach
            self._entry_stop = None
            self._waiting_at_road = True
            why = f"at {leg.words}; the wind does not serve farther in"
            self.give("come to an anchor", why=why)
            self._enter("at anchor")
            return
        if leg.kind == "anchorage":
            self._entry_stop = None
            self.give("come to an anchor", why=f"at {leg.words}")
            self._advance()
            if self.intent is not None and self.intent.kind in ("passage", "home", "letter"):
                # the voyage's end (package 40c): she is not sailed again on the tide
                self.intent.done = True
            return
        if leg.kind == "station":
            self._enter("keeping station")
            return
        if leg.kind == "via" and leg.said:
            world.record(
                Severity.NOTABLE,
                "captain.plan",
                f"{self.name}: {leg.words} passed, {leg.said}.",
                actor=actor_for(self.state or "on passage"),
                data={"leg": leg.to_dict()},
            )
        self._advance()
        if self.leg_i < len(self.legs):
            self._shape_leg()
        else:
            what = self.intent.words if self.intent else "nothing more"
            world.record(
                Severity.NOTABLE,
                "captain.plan",
                f"{self.name}: the plan's last leg is run; {what}.",
                actor=actor_for(self.state or "on passage"),
                data={"legs": [lg.to_dict() for lg in self.legs]},
            )

    def _advance(self) -> None:
        self.leg_i += 1
        self._reload_leg_book()

    def _reload_leg_book(self) -> None:
        """The state's book carries the leg's mark: on a new leg it is written again."""
        if self.state in ("on passage", "beating", "running for shelter"):
            runtime = getattr(self.world, "standing", None)
            if runtime is not None:
                runtime.unload_book(self.state, actor_for(self.state), quiet=True)
                lines = self._book_lines(self.state)
                if lines:
                    runtime.load_book(self.state, lines, actor_for(self.state), quiet=True)

    def _plan(self, p: Perception) -> None:
        if self.intent is None:
            return
        nav = getattr(self.world, "navigation", None)
        start = nav.account_now() if nav is not None else None
        if start is None:
            return
        departing = p.in_port or self._departing
        self._plan_from = start
        try:
            self.legs = Planner(self.world).legs_for(self.intent, start, departing)
        except ValueError as e:
            # a mark of the way the chart has not got (package 45): said once, no plan
            self.world.record(
                Severity.URGENT,
                "captain.plan",
                f"{self.name} cannot lay the plan for {self.intent.words}: {e}",
                actor=actor_for(self.state or "on passage"),
            )
            self.legs = []
        self.leg_i = 0
        said = "; ".join(lg.words for lg in self.legs) or "no legs"
        self.world.record(
            Severity.NOTABLE,
            "captain.plan",
            f"{self.name}'s plan for {self.intent.words}: {said}.",
            actor=actor_for(self.state or "on passage"),
            data={"legs": [lg.to_dict() for lg in self.legs]},
        )
        self._reload_leg_book()

    def _shape_leg(self, why: str = "") -> None:
        if not self.legs or self.leg_i >= len(self.legs):
            return
        leg = self.legs[self.leg_i]
        self.leg_shaped_tick = self.world.clock.tick
        p = Perception.read(self.world)
        if p.pilot_conn:
            # the pilot has her (package 45), on any leg (45c: the owner's merchantman,
            # given to the pilot in the Goulet, was taken back from him by the captain's
            # course for the anchorage at his state's change, and stood out for the Iroise)
            return
        if self._inner_leg():
            # the entry judged leg by leg (package 45, item 3a): the legs he can reach
            self._entry_stop = self._entry_stop_for(p)
            if (
                p.pilot_aboard
                and not self._business.get("conn_given")
                and not self._business.get("conn_refused")
                and self._leg_serves(leg, p)
            ):
                self._business["conn_given"] = True
                e = self.give("let the pilot take her in", why="his water")
                if e.kind != "order.rejected":
                    self._reload_leg_book()
                    return
        e = self.give(f"shape a course for {leg.words}", why=why)
        shaped = getattr(e, "data", None) or {}
        if shaped.get("line_deg") is not None:
            # the leg as laid now (package 58b, item 1), so that a second laying in the
            # same minute is not asked for against the one before it
            self._business["laid"] = {
                "tick": self.world.clock.tick,
                "line_deg": shaped.get("line_deg"),
                "allowing": dict(shaped.get("allowing") or {}),
            }

    def _distance_by_account(self, leg: Leg) -> float | None:
        found = self.world.readings.value("distance_to", leg.words)
        if not isinstance(found, dict) or found.get("metres") is None:
            return None
        return float(found["metres"]) / units.NAUTICAL_MILE

    def _tide_serves(self, port: Any, p: Perception, which: str) -> bool:
        wanted = str((getattr(port, "tide", None) or {}).get(f"{which}_on") or "")
        if wanted not in ("flood", "ebb"):
            return True
        serves = p.tide_is(wanted)
        if serves is None:
            return True
        return bool(serves) and p.daylight == "day"

    # -- in port: the business --------------------------------------------------------

    def _ready_for_sea(self, p: Perception) -> bool:
        if self.intent is None or not p.anchor_down:
            return False
        port = self._port_of(p.in_port)
        if port is None:
            return False
        if self.intent.kind == "trade" and port.id == self.intent.origin:
            if not p.hold.get(self.intent.cargo):
                return False
        if p.boat_away:
            return False
        return self._tide_serves(port, p, "leave")

    def _in_port(self, p: Perception) -> None:
        if self.intent is None:
            return
        port = self._port_of(p.in_port)
        if port is None:
            return
        if self.intent.kind in ("passage", "home", "letter") and port.id == self.intent.destination:
            # the voyage's end (package 40c): she is not sailed again on the tide
            self.intent.done = True
        if self.intent.kind == "trade":
            if port.id == self.intent.origin and not p.hold.get(self.intent.cargo):
                self._buy(port, p)
            elif port.id == self.intent.destination and p.hold.get(self.intent.cargo):
                self._sell(port, p)
            elif port.id == self.intent.destination and not self.intent.done:
                if self._business.get("sold"):
                    self.intent.done = True
        if self._ready_for_sea(p) and not self.intent.done and not self._business.get("sailing"):
            self._sail(port, p)

    def _buy(self, port: Any, p: Perception) -> None:
        if p.boat_away or self._business.get("bought"):
            return
        if p.prices_port != port.id or self.intent is None:
            if self._business.get("brought_up") and not self._business.get("sent_for_prices"):
                e = self.give("send the boat ashore with the mate", why="for the prices")
                if e.kind != "order.rejected":
                    self._business["sent_for_prices"] = True
            return
        price = p.prices.get(self.intent.cargo)
        if not price:
            return
        room = float(self.world.readings.value("manifest").get("room_tons") or 0.0)
        tons = self.intent.tons or math.floor(min(room, p.purse * 0.95 / price))
        if tons <= 0:
            return
        self._business["bought"] = True
        self.give(f"buy {tons:g} tons of {self.intent.cargo}")

    def _sell(self, port: Any, p: Perception) -> None:
        if p.boat_away or self._business.get("sold") or self.intent is None:
            return
        if p.prices_port != port.id:
            # the boat goes for the prices once she is brought up (the merchant book's
            # "the agent": at brought up), when the hands are free of the anchor
            if self._business.get("brought_up") and not self._business.get(
                "sent_for_prices_at_" + port.id
            ):
                e = self.give("send the boat ashore with the mate", why="for the prices")
                if e.kind != "order.rejected":
                    self._business["sent_for_prices_at_" + port.id] = True
            return
        tons = p.hold.get(self.intent.cargo, 0.0)
        if tons <= 0:
            return
        self._business["sold"] = True
        self.give(f"sell {tons:g} tons of {self.intent.cargo}")

    def _sail(self, port: Any, p: Perception) -> None:
        """Under way for sea on the pilot's cast and course out of the port's file; the
        doctrine's table takes her on passage when the anchor is aweigh."""
        cast = getattr(port.pilot, "cast", "starboard")
        course = units.point_name(math.radians(float(getattr(port.pilot, "course_out_deg", 180.0))))
        e = self.give(f"get under way on the {cast} tack and steer {course}", why="the tide serves")
        if e.kind != "order.rejected":
            self._business["sailing"] = True
            self._business.pop("course_not_laid", None)
            self._business.pop("conn_given", None)
            self._business.pop("conn_refused", None)
            self._departing = port.id
            self.legs, self.leg_i = [], 0
            self._entry_stop = None

    # -- the station, the strangers ----------------------------------------------------

    def _station_mark(self) -> tuple[str, Position] | None:
        """The station's mark: the point off the place (`station_off`), as words the
        dialect reads and as a position."""
        if self.intent is None:
            return None
        place = _mark(self.world, self.intent.destination)
        if place is None:
            return None
        if self.intent.kind != "station":
            return place
        mark = station_off(self.world, place[1], self.intent.radius_nm)
        return plain_position(mark), mark

    def _on_station(self, p: Perception) -> bool:
        if self.intent is None:
            return False
        station = self._station_mark()
        if station is None:
            return False
        found = self.world.readings.value("distance_to", station[0])
        if not isinstance(found, dict) or found.get("metres") is None:
            return False
        return float(found["metres"]) / units.NAUTICAL_MILE <= self.intent.radius_nm * 2.0

    def _station(self, p: Perception) -> None:
        # the book keeps the station; the transitions watch for a sail. A fisherman on her
        # ground works her gear (package 56; the fishermen promoted, spec M7b §21a)
        if self.role == "fisherman" and self.intent is not None and self.intent.kind == "fish":
            from freesail.world import fishing

            fishing.captain_work(self, p)

    def _keep_stranger(self, p: Perception) -> None:
        if self._stranger is None:
            near = self._nearest_stranger(p)
            self._stranger = near.get("id") if near else None

    # -- the action (package 70; spec M7 §10) ------------------------------------------

    def _habit(self) -> dict[str, Any]:
        """The figures he fights by: the role's file's, the nation's habit over them
        (data/nations.yaml `habits:`, package 71) where the file names none."""
        from freesail.world.nations import DEFAULT_HABITS

        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        ports = getattr(self.world, "ports", None)
        nation = str(getattr(ports, "ship_nation", "") or "")
        nations = getattr(self.world, "nations", None)
        habit = nations.habits_of(nation) if nations is not None else dict(DEFAULT_HABITS)
        factor = float(habit.get("range_factor", 1.0))
        aim = th("aim", "") or habit["aim"]
        roll = th("roll", "") or habit["roll"]
        closer = 0.5 if self._business.get("closer") else 1.0  # 'engage more closely' (71)
        return {
            "aim": aim,
            "roll": roll,
            "charge": th("charge", "round") or "round",
            "side": th("engage_side", "weather") or "weather",
            "engage_range_cables": float(th("engage_range_cables", 2.0)) * factor * closer,
            "break_off_cables": float(th("break_off_nm", 2.0)) * 10.0,
            "fire_mode": th("fire_mode", "as they bear") or "as they bear",
        }

    def _mark(self, p: Perception) -> dict[str, Any] | None:
        """The enemy engaged: the battery's mark if she is in sight, else the nearest
        enemy within the breaking-off distance."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        battery = (getattr(self.world.ship, "extra", None) or {}).get("battery")
        target = getattr(battery, "target", None) if battery is not None else None
        if target is not None:
            for s in p.strangers:
                if s.get("id") == target and s.get("estimate_m") is not None:
                    return s
        return self._enemy_within(p, float(th("break_off_nm", 2.0)))

    def _side_of_mark(self, p: Perception, s: dict[str, Any]) -> str:
        """The side she bears on now: the battery engaged."""
        bearing = float(s.get("bearing_deg") or 0.0)
        heading = float(p.heading_deg or 0.0)
        rel = (bearing - heading + 180.0) % 360.0 - 180.0
        return "starboard" if rel >= 0.0 else "larboard"

    def _engage_now(self, p: Perception) -> None:
        """Entering `engaging`: the drum, the guns cast loose, loaded and laid by the
        doctrine, the mark engaged on the side she bears, the fire held until the book's
        range (the book opens it)."""
        habit = self._habit()
        mark = self._mark(p)
        # rule 3 (package 71): her true colours before the first shot; the ruse was the
        # law's until then and no further
        from freesail.world.signals import player_locker

        colours = player_locker(self.world).colours
        if colours.state in ("false", "none"):
            self.give("hoist the colours", why="her true colours before the first shot")
        self._business["engaged_at"] = p.tick
        quarters = (getattr(self.world.ship, "extra", None) or {}).get("quarters")
        if quarters is None or not getattr(quarters, "at_quarters", False):
            self.give("beat to quarters", why="an enemy in range")
        self.give("cast loose the guns", why="an enemy in range")
        self.give(f"load with {self._fills()['charge']}")
        self.give(f"aim at {self._fills()['aim']}")
        if habit["roll"] in ("up", "down"):
            self.give(f"fire on the {habit['roll']} roll")
        if mark is not None:
            side = self._side_of_mark(p, mark)
            self._business["engaged_side"] = side
            self.give(f"engage her to {side}", why="the enemy in range")
            self.give("hold your fire", why="until she is within the book's range")
        self._fight_ready(p)
        self._engaging(p)

    def _engaging(self, p: Perception) -> None:
        """Each minute of the action: the mark kept on the engaged beam at the doctrine's
        range (closed when beyond it, opened when under half of it), the battery shifted
        when she crosses the bow or the stern; the fire the book's."""
        mark = self._mark(p)
        if mark is None or p.heading_deg is None:
            return
        side = self._side_of_mark(p, mark)
        if side != self._business.get("engaged_side"):
            self._business["engaged_side"] = side
            self.give(f"engage her to {side}", why="she bears on the other side")
        habit = self._habit()
        wanted = habit["engage_range_cables"] * units.NAUTICAL_MILE / 10.0
        rng = float(mark.get("estimate_m") or wanted)
        last_tick = int(self._business.get("steered_tick", -(10**9)))
        self._musketry(p, rng)
        if self._boarding(p, mark, rng):
            return
        if self._weaker(p, mark):
            # a weaker mark (a smaller class, or a merchantman) is chased and closed to
            # pistol shot: the chaser runs alongside, and the range-keeping law is for an
            # equal (the trade-stranger trial: the beam law steered the brig across the
            # chase and the schooner ran clear)
            wanted = CLOSE_RANGE_M
            if rng > CLOSE_RANGE_M * 3.0:
                # the chase renewed every three minutes (the chasing book's 'keep her
                # bearing' is not loaded in this state; a chase given once is one course)
                if self._business.get("steered_for") != "chase" or p.tick - last_tick >= 180:
                    self._business["steered_for"] = "chase"
                    self._business["steered_tick"] = p.tick
                    self.give(self._chase_order(p), why="to close her")
                return
        bearing = float(mark.get("bearing_deg") or 0.0)
        # the angle she is kept on, before the beam to close and abaft it to open, a
        # straight law of the range over the wanted (at the range abeam; at twice it four
        # points before the beam; at half, three points abaft), so the course does not
        # jump at a band's edge; never within the close-hauled angle, the gage kept
        # (`helm_in_action`, package 71's item 8)
        ratio = rng / max(wanted, 1.0)
        if p.wind_from_deg is None:
            return
        from freesail.evolutions.scripts import close_hauled_true_angle

        closest = units.rad_to_deg(close_hauled_true_angle(self.world.ship))
        if HELM_IN_ACTION:
            course, word = helm_in_action(
                p.heading_deg, p.wind_from_deg, closest, bearing, side, ratio, habit["side"]
            )
        else:  # 70's law, for the bisection alone
            sign = 1.0 if side == "starboard" else -1.0
            off = max(35.0, min(125.0, 90.0 + 55.0 * (1.0 - ratio)))
            course, word = (bearing - sign * off) % 360.0, ""
        if "through the eye" in word:
            self._through_the_eye(p, mark, side)
        last = self._business.get("steered_for")
        if last == "chase":
            last = None
        turn = abs((course - float(last) + 180.0) % 360.0 - 180.0) if last is not None else 999.0
        if turn >= 10.0 and p.tick - last_tick >= 120:
            self._business["steered_for"] = course
            self._business["steered_tick"] = p.tick
            why = "to keep the enemy on the engaged beam" + (f", {word}" if word else "")
            self.give(f"steer {course:.0f}", why=why)

    # -- package 73 (spec M7 §11, §11a, §13, §14): the fight on deck and the damage ----------

    def _th(self, key: str, default: Any = None) -> Any:
        d = self.doctrine
        return d.threshold(key, default) if d is not None else default

    def _fight_ready(self, p: Perception) -> None:
        """Entering the action: the marines into the tops where the kit's habit is the
        tops (`marines_tops`: `kit` reads the nation's share aloft, true or false says it
        outright), the small arms served out where he may board (`board_odds` above
        nought)."""
        from freesail.combat.small_arms import kit_of, marines_of

        ship = self.world.ship
        if marines_of(ship):
            tops = self._th("marines_tops", "kit")
            kit = kit_of(self.world)
            aloft = tops is True or (tops == "kit" and float(kit.get("tops_share", 0.0)) >= 0.3)
            if aloft:
                self.give("marines to the tops", why="the marksmen aloft, the nation's habit")
        if float(self._th("board_odds", 0.0) or 0.0) > 0.0:
            self.give("serve out the small arms", why="to be ready to board or be boarded")

    def _musketry(self, p: Perception, range_m: float) -> None:
        """The marines open by volley within the doctrine's cables of a near deck and hold
        their fire beyond twice it; the small arms at will with them."""
        from freesail.combat.small_arms import musketry_of

        ship = self.world.ship
        quarters = ship.extra.get("quarters")
        if quarters is None or not getattr(quarters, "at_quarters", False):
            return
        m = musketry_of(ship)
        cables = float(self._th("musketry_cables", 1.0) or 1.0)
        within = cables * units.NAUTICAL_MILE / 10.0
        crew = ship.extra.get("crew")
        from freesail.crew.model import Station

        borne = crew is not None and any(s.fit for s in crew.by_station.get(Station.MARINES, []))
        if borne:  # at their carronades until the order takes them to their muskets
            if range_m <= within and m.mode == "hold":
                self.give("marines, fire by volley", why=f"within {cables:g} cables")
            elif range_m > 2.0 * within and m.mode != "hold":
                self.give("marines, hold your fire", why="she is beyond musket shot")
        if m.served:
            if range_m <= within and m.small_arms_mode == "hold":
                self.give("small arms, fire at will", why=f"within {cables:g} cables")
            elif range_m > 2.0 * within and m.small_arms_mode != "hold":
                self.give("small arms, hold your fire", why="she is beyond musket shot")

    def _boarding(self, p: Perception, mark: dict[str, Any], range_m: float) -> bool:
        """Whether he is laying her aboard this minute (the helm law stands aside): by
        `board_odds` (his boarders so many times her fit company) and `board_when` (`her
        guns silent`: no shot of hers has struck for five minutes; `at any time`); the
        chase's helm to close, the grapnels within their throw, the boarders away once
        grappled; a fight in hand holds the course."""
        from freesail.combat.boarding import GRAPPLE_RANGE_M, boarders_of, fight_of, grappled_to
        from freesail.combat.hits import damage_of
        from freesail.world.brains import PLAYER_ID

        ship = self.world.ship
        odds = float(self._th("board_odds", 0.0) or 0.0)
        if odds <= 0.0:
            return False
        f = fight_of(ship)
        if f is not None and not f.over:
            return True
        if self._stranger_struck(mark):
            return False
        mid = str(mark.get("id") or "")
        v = self._vessel_of(mid)
        crew_world = getattr(v, "crew", None) if v is not None else None
        body = (
            crew_world.ship
            if crew_world is not None and getattr(crew_world, "shape", "full") == "full"
            else None
        )
        if body is None and mid == PLAYER_ID:
            parent = getattr(self.world, "parent", None)
            body = parent.ship if parent is not None else None
        if body is None or body.extra.get("crew") is None:
            return False
        theirs = sum(1 for s in body.extra["crew"].sailors if s.fit)
        ours = len(boarders_of(ship, self.world))
        if ours < odds * max(theirs, 1):
            return False
        when = str(self._th("board_when", "her guns silent") or "her guns silent")
        if when != "at any time":
            keeper = damage_of(ship)
            last = int(keeper.struck_by.get(mid, -(10**9))) if keeper is not None else -(10**9)
            if p.tick - last < 300 and last > -(10**8):
                return False
            if last <= -(10**8) and p.tick - int(self._business.get("engaged_at", p.tick)) < 300:
                return False
        tick = p.tick
        if grappled_to(ship) == mid:
            if tick - int(self._business.get("boarders_tick", -(10**9))) >= 120:
                self._business["boarders_tick"] = tick
                self.give("boarders away", why="grappled, the odds his")
            return True
        if range_m <= GRAPPLE_RANGE_M:
            if tick - int(self._business.get("grapple_tick", -(10**9))) >= 180:
                self._business["grapple_tick"] = tick
                self.give("grapple her", why="within a grapnel's throw")
            return True
        if tick - int(self._business.get("board_tick", -(10**9))) >= 180:
            self._business["board_tick"] = tick
            self.give("lay her aboard", why=f"to board her: {ours} boarders to her {theirs}")
        return True

    def _damage_work(self, p: Perception) -> None:
        """Each minute in any state: her boarders on his deck repelled; the pumps manned at
        the doctrine's depth; the colours struck when the water gains past the share with
        an enemy at hand; the repairs by the doctrine's priority (in action the leak first,
        then the rigging that keeps him sailing; after it the rigging whole)."""
        from freesail.combat.boarding import fight_of
        from freesail.combat.small_arms import musketry_of

        world = self.world
        ship = world.ship
        tick = p.tick
        f = fight_of(ship)
        if f is not None and not f.over and f.defender is ship and not musketry_of(ship).repelling:
            self.give("repel boarders", why="her boarders on our deck")
        water = getattr(world, "water", None)
        st = water.state if water is not None else None
        if water is None or st is None:
            return
        depth = float(water.depth_m())
        pumps = water.pumps
        at = float(self._th("pumps_at_m", 0.3) or 0.3)
        if (
            depth >= at
            and not pumps.manned
            and tick - int(self._business.get("pumps_tick", -(10**9))) >= 600
        ):
            self._business["pumps_tick"] = tick
            self.give("man the pumps", why=f"the well at {depth:.2f} m")
        share = float(self._th("give_up_at_share", 0.4) or 0.4)
        founder = float(water.founder_t())
        losing = pumps.manned and float(water.gain_t_per_h()) > float(
            pumps.rate_t_per_h(pumps.hands())
        )
        if (
            share > 0.0
            and founder > 0.0
            and float(st.tons) >= share * founder
            and losing
            and self.state == "engaging"
            and not ship.extra.get("struck")
            and not self._business.get("gave_up")
        ):
            self._business["gave_up"] = True
            self.give(
                "strike the colours", why="the water gaining on the pumps with an enemy at hand"
            )
        self._repairs(p)

    def _repairs(self, p: Perception) -> None:
        from freesail.evolutions.repair_scripts import (
            parted_running_lines,
            parted_standing_lines,
            sprung_spars,
        )

        world = self.world
        ship = world.ship
        tick = p.tick
        if tick - int(self._business.get("repairs_tick", -(10**9))) < 600:
            return
        runner = ship.extra.get("evolutions")
        in_hand = (
            {inst.evo.id for inst in getattr(runner, "instances", [])}
            if runner is not None
            else set()
        )
        keeper = ship.extra.get("damage")
        holes = [
            h
            for h in (getattr(keeper, "holes", []) or [])
            if not h.get("plugged") and float(h.get("z_m", 1.0)) < 0.3
        ]
        order = list(self._th("damage_priority", ["the leak", "the rigging", "the guns"]) or [])
        in_action = self.state == "engaging"
        wanted: list[tuple[str, str]] = []
        for what in order:
            if what == "the leak" and holes and "plug_shot_hole" not in in_hand:
                wanted.append(("plug the shot holes", "the shot holes under water"))
            if what == "the rigging":
                if parted_standing_lines(ship) and "set_up_rigging" not in in_hand:
                    wanted.append(("set up the rigging", "the standing rigging parted"))
                if not in_action:
                    if parted_running_lines(ship) and "reeve_line" not in in_hand:
                        wanted.append(("reeve new lines", "the running rigging shot away"))
                    for spar in sprung_spars(ship):
                        if "fish_spar" not in in_hand:
                            from freesail.evolutions.repair_scripts import _name

                            wanted.append((f"fish the {_name(ship, spar.id)}", "a sprung spar"))
                            break
        if not wanted:
            return
        self._business["repairs_tick"] = tick
        text, why = wanted[0]
        self.give(text, why=why)

    def _chase_order(self, p: Perception) -> str:
        """'chase the cutter': the chase named by HIS stranger's rig when the lookout has
        it, so the helm goes after the sail he judged and not the order's own choice (the
        nearest stranger of the lookout's, who counts a sail under our own colours no
        stranger: the encounter's frigate, package 71, gave chase to the merchant brig two
        miles off while the privateer under British colours ran); 'give chase' when her
        rig is not yet made out or the lookout has no word for it."""
        sid = self._stranger
        lookout = getattr(self.world, "lookout", None)
        if sid is None or lookout is None:
            return "give chase"
        for s in p.strangers:
            if str(s.get("id") or "") != str(sid):
                continue
            words = str(s.get("known") or "").split(",")[0].split(";")[0].strip()
            rig = words.removeprefix("a ").removeprefix("an ").strip()
            if rig and rig != "sail" and lookout.find(f"the {rig}") is not None:
                return f"chase the {rig}"
        return "give chase"

    def _through_the_eye(self, p: Perception, mark: dict[str, Any], side: str) -> None:
        """The mark passes through the wind's eye (package 71, item 8): by the doctrine's
        `through_the_eye` he shifts the engaged battery and stays on his tack (the default:
        his guns go on, the beam law finding her on the other side next minute), or puts
        about or wears for her (a handy cutter may tack, a frigate wears), once a crossing
        and not again within five minutes."""
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        what = str(th("through_the_eye", "shift") or "shift")
        last = int(self._business.get("through_the_eye_tick", -(10**9)))
        if what not in ("tack", "wear") or p.tick - last < 300:
            return
        self._business["through_the_eye_tick"] = p.tick
        self._business["steered_tick"] = p.tick
        self._business["steered_for"] = None
        order = "put her about" if what == "tack" else "wear ship"
        self.give(order, why="the enemy passes through the wind's eye")

    def _enemy_within(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        if not getattr(self.world.ship, "guns", None):
            return None  # no guns: she never engages; she runs by the merchant's rows
        return super()._enemy_within(p, within_nm)

    def _weaker(self, p: Perception, mark: dict[str, Any]) -> bool:
        """A mark of a smaller class than her own, or a merchantman of any class."""
        if "merchant" in str(mark.get("known") or "").lower():
            return True
        return int(mark.get("size") or 0) < int(p.own_size or 0)

    def _stranger_struck(self, s: dict[str, Any]) -> bool:
        v = self._vessel_of(str(s.get("id") or ""))
        return bool(v is not None and getattr(v, "struck", False))

    def _enemy_struck(self, p: Perception) -> bool:
        battery = (getattr(self.world.ship, "extra", None) or {}).get("battery")
        target = getattr(battery, "target", None) if battery is not None else None
        if target is None:
            return False
        v = self._vessel_of(str(target))
        return bool(v is not None and getattr(v, "struck", False))

    def _vessel_of(self, vid: str) -> Any:
        world = self.world
        sea = getattr(world, "vessels", None)
        v = sea.get(vid) if sea is not None else None
        if v is None and vid == "the ship":
            parent = getattr(world, "parent", None)
            v = parent.vessels.player_shadow(parent) if parent is not None else None
        return v

    def _nearest_stranger(self, p: Perception) -> dict[str, Any] | None:
        items = self._unspoken(p)
        if not items:
            return None
        return min(items, key=lambda s: s.get("estimate_m") or math.inf)

    def _is_enemy(self, s: dict[str, Any]) -> bool:
        known = self._known_enemy(s)  # package 71: the shot, the private signal, the hail
        if known is not None:
            return known
        nation = s.get("nation")
        if not nation:
            return False
        nations = getattr(self.world, "nations", None)
        ports = getattr(self.world, "ports", None)
        own = ports.ship_nation if ports is not None else None
        return bool(nations is not None and own and nations.at_war(str(nation), own))

    def _nearest_enemy(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        enemies = [
            s
            for s in p.strangers
            if self._is_enemy(s)
            and not self._spoken(s)
            and s.get("estimate_m") is not None
            and float(s["estimate_m"]) / units.NAUTICAL_MILE <= within_nm
        ]
        if not enemies:
            return None
        return min(enemies, key=lambda s: float(s["estimate_m"]))

    def _haul_off(self, p: Perception) -> None:
        """Evading: a course shaped for a point away from the nearest enemy, the
        reciprocal of her bearing, by account."""
        d = self.doctrine
        enemy = self._nearest_enemy(
            p, float(d.threshold("stranger_hostile_nm", 6)) * 3 if d else 18
        )
        if enemy is None:
            return
        self._stranger = enemy.get("id")
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None:
            return
        away = (float(enemy.get("bearing_deg") or 0.0) + 180.0) % 360.0
        point = destination(here, away, 20.0 * units.NAUTICAL_MILE)
        self._business["hauled_off"] = p.tick
        self.give(
            f"shape a course for {plain_position(point)}",
            why=f"hauling off from {enemy.get('known', 'a stranger')}",
        )

    def _shelter_port(self, p: Perception) -> Any:
        """The nearest port open to her within the doctrine's reach, by the port's
        reading (by account)."""
        ports = getattr(self.world, "ports", None)
        if ports is None or not getattr(ports, "ports", None):
            return None
        d = self.doctrine
        reach = float(d.threshold("shelter_within_nm", 20)) if d else 20.0
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None:
            return None
        best = None
        for port in ports.ports.values():
            if ports.stance(port) in ("hostile", "closed"):
                continue
            _, dist = bearing_and_distance(here, port.outer_road.position)
            nm = dist / units.NAUTICAL_MILE
            if nm <= reach and (best is None or nm < best[1]):
                best = (port, nm)
        return best[0] if best else None

    # -- the rule of the road ----------------------------------------------------------

    def _rule_of_the_road(self, p: Perception) -> None:
        """At a few cables, the custom of 1805 as a reflex (spec M6 §4): the ship
        close-hauled on the starboard tack stands on, the larboard-tack ship gives way
        under her stern, a ship running keeps clear of one by the wind. Judged from the
        strangers' reading (her course as made out) and the wind; said once an
        encounter, notable."""
        if p.wind_from_deg is None or p.heading_deg is None or p.anchor_down:
            return
        reach = ROAD_CABLES * units.CABLE
        for s in p.strangers:
            est = s.get("estimate_m")
            sid = str(s.get("id") or "")
            if est is None or float(est) > reach or (s.get("made_out") or 0) < 1:
                if sid in self._road_said and (est is None or float(est) > reach * 2):
                    del self._road_said[sid]
                continue
            if sid in self._road_said:
                continue
            if "pilot" in str(s.get("known") or "") or s.get("spoken"):
                continue  # a pilot's boat keeping company, or a sail spoken: no crossing
            her = _course_in_words(str(s.get("known") or ""))
            if her is None:
                continue
            ours = _tack_and_point(p.heading_deg, p.wind_from_deg)
            hers = _tack_and_point(her, p.wind_from_deg)
            order, words = _road_rule(ours, hers)
            self._road_said[sid] = p.tick
            who = str(s.get("known") or "a sail").split(",")[0]
            self.world.record(
                Severity.NOTABLE,
                "captain.road",
                f"{self.name}, by the rule of the road: {who} {s.get('relative', '')}, {words}.",
                actor=actor_for(self.state or "on passage"),
                data={"id": sid, "ours": ours, "hers": hers, "order": order},
            )
            if order:
                self.give(order, why="the rule of the road")

    # -- orders ------------------------------------------------------------------------

    def give(self, text: str, why: str = "") -> Any:
        """An order of the captain's judgement, through `World.submit` under the rules
        actor: logged as a captain's, never journaled."""
        from freesail.standing.runtime import said_as_done

        world = self.world
        state = self.state or "on passage"
        ship = world.ship
        done = said_as_done(ship, text) if hasattr(ship, "parts") else text
        said = f"By the captain, {state}: {done}" + (f" ({why})" if why else "")
        return world.submit(text, actor=actor_for(state), said=said)


# ---------------------------------------------------------------------------
# The rule of the road's arithmetic
# ---------------------------------------------------------------------------

_COURSE_WORDS = re.compile(r"\(([NESWbyh ]+(?:\s*\d*)?)\)")


def _point_deg(words: str) -> float | None:
    """A compass point's words to degrees, through the units' own reader."""
    try:
        rad = units.parse_course(str(words).strip())
    except (ValueError, KeyError, AttributeError, units.CourseError):
        return None
    return units.rad_to_deg(rad) % 360.0 if rad is not None else None


def _course_in_words(known: str) -> float | None:
    """The stranger's course from the lookout's words ('standing to the eastward (E)')."""
    m = _COURSE_WORDS.search(known)
    if m is None:
        return None
    return _point_deg(m.group(1))


def _tack_and_point(course_deg: float, wind_from_deg: float) -> dict[str, Any]:
    rel = units.rad_to_deg(units.wrap_pi(math.radians(wind_from_deg - course_deg)))
    tack = "starboard" if rel >= 0 else "larboard"
    off = abs(rel)
    point = (
        "by the wind" if off <= BY_THE_WIND_DEG else "running" if off >= RUNNING_DEG else "reaching"
    )
    return {"tack": tack, "point": point, "course_deg": round(course_deg, 1)}


def _road_rule(ours: dict[str, Any], hers: dict[str, Any]) -> tuple[str, str]:
    """(the order, the words): the custom of 1805 (Luce 1884 ch. XXXII on the older
    rule, Falconer's 'the ship on the starboard tack keeps her wind'): both by the wind
    on opposite tacks, the starboard-tack ship stands on and the larboard-tack ship bears
    up under her stern; a ship running or reaching keeps clear of one by the wind; the
    rest stand on."""
    if ours["point"] == "by the wind" and hers["point"] == "by the wind":
        if ours["tack"] == hers["tack"]:
            return "", "both by the wind on the same tack; we stand on"
        if ours["tack"] == "starboard":
            return "", "she is by the wind on the larboard tack and gives way; we stand on"
        return (
            "bear away two points",
            "she is by the wind on the starboard tack and stands on; we give way under her stern",
        )
    if hers["point"] == "by the wind":
        return "bear away two points", "she is by the wind and stands on; we keep clear of her"
    if ours["point"] == "by the wind":
        return "", "we are by the wind and stand on; she keeps clear"
    return "", "neither by the wind; we stand on"


# The far-detail brain's names, reached here for the callers that know the brain by this
# module (package 43): `freesail.world.brains` imports this module, so it is loaded late.
_BRAINS = ("FarCaptain", "PLAYER_ID", "perceive_vessel", "resolve_state", "role_of_vessel")


def __getattr__(name: str) -> Any:
    if name in _BRAINS:
        from freesail.world import brains

        return getattr(brains, name)
    raise AttributeError(name)
