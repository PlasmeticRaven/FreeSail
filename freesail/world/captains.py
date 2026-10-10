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
    "Leg",
    "Perception",
    "Planner",
    "actor_for",
    "load_doctrine",
    "load_tracks",
    "plain_position",
    "read_intent",
    "resolve_state",
    "role_for",
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
)

# The roles the doctrine files give (the fisherman is 43b's).
ROLES: tuple[str, ...] = ("kings-ship", "merchant", "packet", "commodore")

# The kinds of intent the captain reads.
INTENT_KINDS: tuple[str, ...] = ("trade", "station", "letter", "home", "passage")

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

# The states the far-detail body resolves in this package (spec M6 §4, "one brain, two
# bodies"; 43 fills the rest with the crewed promotion): on passage is her plan, hove to
# is no way.
FAR_DETAIL_STATES: tuple[str, ...] = ("on passage", "hove to for weather")

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
# The anchorage is taken at the first cast under this many fathoms within the book's
# reach of its mark, where the port's file gives its anchorage no depth (the merchant
# book's twelve for the Bay of Brest: Faden's eight, ten or sixteen on mud); with a
# depth given, two fathoms over it.
ANCHORAGE_FATHOMS = 12


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "words": self.words,
            "cargo": self.cargo,
            "tons": self.tons,
            "origin": self.origin,
            "destination": self.destination,
            "radius_nm": self.radius_nm,
            "done": self.done,
        }


_TRADE = re.compile(
    r"^trade\s+(?:(?P<tons>[\w-]+)\s+tons?\s+of\s+)?(?P<cargo>[\w' -]+?)\s+from\s+(?P<a>.+?)\s+"
    r"(?:to|for)\s+(?P<b>.+)$"
)
_STATION = re.compile(
    r"^(?:keep (?:the )?station|cruise|patrol)\s+off\s+(?P<place>.+?)"
    r"(?:\s+within\s+(?P<radius>[\d.]+)\s+miles?)?(?:\s+between\s+(?P<between>.+))?$"
)
_LETTER = re.compile(
    r"^carry\s+(?:this|a|the)\s+(?:letter|message|dispatch|despatch)\s+to\s+(?P<b>.+)$"
)
_HOME = re.compile(r"^run\s+home\s+(?:to|for)\s+(?P<b>.+)$")
_PASSAGE = re.compile(r"^(?:bound|passage|sail)\s+(?:from\s+(?P<a>.+?)\s+)?(?:for|to)\s+(?P<b>.+)$")


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

    m = _TRADE.match(text)
    if m:
        tons = None
        if m.group("tons"):
            tons = read_all(m.group("tons"))
            if tons is None:
                raise ValueError(f"'{m.group('tons')}' is no number of tons in '{words}'.")
        a = _place_id(world, group(m, "a"))
        b = _place_id(world, group(m, "b"))
        return Intent(
            "trade", said, cargo=m.group("cargo").strip(), tons=tons, origin=a, destination=b
        )
    m = _STATION.match(text)
    if m:
        place = _place_id(world, group(m, "place"))
        radius = float(m.group("radius") or 5.0)
        return Intent(
            "station", said, destination=place, radius_nm=radius, between=group(m, "between")
        )
    m = _LETTER.match(text)
    if m:
        return Intent("letter", said, destination=_place_id(world, group(m, "b")))
    m = _HOME.match(text)
    if m:
        return Intent("home", said, destination=_place_id(world, group(m, "b")))
    m = _PASSAGE.match(text)
    if m:
        a = _place_id(world, group(m, "a")) if m.group("a") else ""
        return Intent("passage", said, origin=a, destination=_place_id(world, group(m, "b")))
    raise ValueError(
        f"'{words}' is no intent a captain knows: say 'trade <cargo> from <A> to <B>', 'keep "
        "the station off <place> within <n> miles', 'carry this letter to <place>', 'run "
        "home to <place>' or 'bound for <place>'."
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
        return "kings-ship"
    if intent is not None and intent.kind == "letter":
        return "packet"
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

    def clear(self, a: Position, b: Position) -> bool:
        """Whether the straight line from a to b keeps the offing off the shore and the
        berth off the charted dangers, by the chart in the captain's hands."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return True
        shore = chart.line_shore(
            a,
            b,
            OFFING_NM * units.NAUTICAL_MILE,
            skip_start_m=OFFING_NM * units.NAUTICAL_MILE,
            skip_end_m=units.CABLE,
        )
        if shore is not None and (shore[2] or shore[0] < OFFING_NM * units.NAUTICAL_MILE):
            return False
        for _f, _off, crosses in chart.line_passes(a, b, DANGER_BERTH_NM * units.NAUTICAL_MILE):
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

    def _round_headland(self, start: Position, end: Position) -> list[tuple[str, Position]]:
        """A straight line that the shore or a danger stands across, with no track to
        take: the nearest headland (or island, or danger) to where the line meets the
        land is given an offing to seaward, and the two halves tried again, a few
        rounds at most; what cannot be cleared is left as it is, the master's warning
        on the course shaped saying what it crosses."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return []
        marks: list[tuple[str, Position]] = []
        a = start
        for _ in range(PLANNER_ROUNDS):
            if self.clear(a, end):
                break
            shore = chart.line_shore(
                a, end, OFFING_NM * units.NAUTICAL_MILE, skip_end_m=units.CABLE
            )
            where = shore[1] if shore is not None else None
            if where is None:
                for f, _off, crosses in chart.line_passes(
                    a, end, DANGER_BERTH_NM * units.NAUTICAL_MILE
                ):
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
            off = destination(head.position, away, OFFING_NM * units.NAUTICAL_MILE)
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
        if intent.kind == "station":
            place = self._place(intent.destination)
            if place is not None:
                mark = station_off(self.world, place[1], intent.radius_nm)
                legs += self._sea_legs(legs[-1].position if legs else start, mark)
                legs.append(Leg(plain_position(mark), mark, "station", intent.radius_nm))
            return legs
        port_to = self._port(intent.destination)
        if port_to is not None:
            approach = self._port_track(port_to, "from_sea")
            first = approach[0].position if approach else port_to.outer_road.position
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
            legs += self._sea_legs(legs[-1].position if legs else start, place[1])
            legs.append(
                Leg(place[0], place[1], "anchorage" if intent.kind == "home" else "to", 0.5)
            )
        return legs

    def _place(self, words: str) -> tuple[str, Position] | None:
        return _mark(self.world, words)

    def _sea_legs(self, a: Position, b: Position) -> list[Leg]:
        return [Leg(words, p, "to", 2.0) for words, p in self.sea_route(a, b)]


# ---------------------------------------------------------------------------
# Perception on the player's terms
# ---------------------------------------------------------------------------


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

    @classmethod
    def read(cls, world: Any) -> Perception:
        view = world.readings
        p = cls(tick=world.clock.tick, now=world.clock.ship_time)
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
        strangers = view.value("strangers")
        if isinstance(strangers, dict):
            p.strangers = list(strangers.get("items") or [])
        port = view.value("port")
        if isinstance(port, dict):
            p.port_distance_nm = port.get("distance_nm")
            # in port: at anchor within the port's reach by account (`ports.IN_PORT_NM`
            # is the port's own rule at the truth; the captain reads his account)
            dist = port.get("distance_nm")
            if (
                p.anchor_down
                and port.get("port")
                and dist is not None
                and float(dist) <= IN_PORT_NM
            ):
                p.in_port = str(port.get("port"))
        pilot = view.value("pilot")
        p.pilot_aboard = isinstance(pilot, dict) and bool(pilot.get("name"))
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
            p.glass_falling_fast = tendency.get("words") == "falling fast"
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
)


class Captain:
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
        self._stranger: str | None = None
        self._departing = ""  # the port she sails from, for the plan's first legs
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
            self.active and (not self.seated or self.stand_in) and not getattr(self, "aside", False)
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
        }

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

    # -- the tick ---------------------------------------------------------------------

    def tick(self) -> None:
        """Once a minute, when his judgements are given: perceive, judge the doctrine's
        transitions, and work the state."""
        world = self.world
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
        if self.state is None:
            self._enter(self._first_state(p))
        self._transitions(p)
        self._work(p, events)
        self._rule_of_the_road(p)
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
        return "on passage"

    def _enter(self, state: str) -> None:
        world = self.world
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
        for line in self.doctrine.book(state):
            try:
                out.append(line.format_map(fills))
            except (KeyError, IndexError, ValueError):
                continue
        return out

    def _fills(self) -> dict[str, Any]:
        d = self.doctrine
        fills: dict[str, Any] = {k: v for k, v in (d.thresholds if d else {}).items()}
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
        if state == "hove to for weather":
            self.give("shorten sail")
            self.give("heave to")
            return
        lying_to = False
        if old == "at anchor" and state in ("on passage", "beating", "running for shelter"):
            # the at-anchor book's "at under way then set plain sail" is unloaded here,
            # before the anchor is catted and the ship says she is under way (package
            # 40c: the schooner left the road under her topsail alone): he gives it at
            # `ship.under_way` himself (`_work`)
            self._business["weighing"] = True
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
            self.give("give chase")
        elif state == "keeping station":
            station = self._station_mark()
            if station is not None:
                self.give(f"shape a course for {station[0]}")
        elif state == "evading":
            self._haul_off(Perception.read(world))

    # -- the doctrine's transitions ----------------------------------------------------

    def _transitions(self, p: Perception) -> None:
        if self.doctrine is None or self.state is None:
            return
        for t in self.doctrine.from_state(self.state):
            if self._stimulus(t.on, p) and not (t.unless and self._stimulus(t.unless, p)):
                self._enter(t.to)
                return

    def _stimulus(self, name: str, p: Perception) -> bool:
        d = self.doctrine
        th = d.threshold if d is not None else (lambda k, v=None: v)
        if name == "gale":
            return p.wind_kn >= float(th("gale_kn", 34)) and p.manoeuvre not in (
                "hove to",
                "heaving to",
            )
        if name == "gale over":
            return p.wind_kn < float(th("gale_over_kn", 28))
        if name == "lee shore":
            if p.wind_from_deg is None:
                return False
            # the land as the lookout sees it, else as the account lays it on the chart
            dist, land = p.nearest_land_nm, _point_deg(p.nearest_land_bearing or "")
            if dist is None or land is None:
                dist, land = p.coast_by_account_nm, p.coast_by_account_bearing_deg
            if dist is None or land is None or dist > float(th("lee_shore_nm", 6)):
                return False
            toward = (p.wind_from_deg + 180.0) % 360.0
            return abs(units.wrap_pi(math.radians(land - toward))) < math.radians(67.5)
        if name == "no sea room":
            # the land to leeward within the sea room a night's drift hove to wants
            # (package 40c): she heaves to only with sea room, and leaves it for a lee
            # shore within `lee_shore_nm`, the two thresholds apart so that she does not
            # heave to and fill away by turns at one line
            if p.wind_from_deg is None:
                return False
            dist, land = p.nearest_land_nm, _point_deg(p.nearest_land_bearing or "")
            if dist is None or land is None:
                dist, land = p.coast_by_account_nm, p.coast_by_account_bearing_deg
            if dist is None or land is None or dist > float(th("sea_room_nm", 10)):
                return False
            toward = (p.wind_from_deg + 180.0) % 360.0
            return abs(units.wrap_pi(math.radians(land - toward))) < math.radians(67.5)
        if name == "thick near the land":
            thick = p.visibility in ("a mile", "a cable")
            dist = p.nearest_land_nm if p.nearest_land_nm is not None else p.coast_by_account_nm
            near = dist is not None and dist < float(th("shelter_land_nm", 12))
            return thick and near and self._shelter_port(p) is not None
        if name == "weather clear":
            return p.visibility not in ("a mile", "a cable")
        if name == "hostile stranger":
            return self._nearest_enemy(p, float(th("stranger_hostile_nm", 6))) is not None
        if name == "stranger":
            return any(not s.get("spoken") for s in p.strangers)
        if name == "stranger lost":
            if self._stranger is None:
                return not p.strangers
            return not any(
                s.get("id") == self._stranger and not s.get("spoken") for s in p.strangers
            )
        if name == "stranger spoken":
            return any(s.get("id") == self._stranger and s.get("spoken") for s in p.strangers)
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
            return any(
                s.get("id") == self._stranger and s.get("nation") and not self._is_enemy(s)
                for s in p.strangers
            )
        if name == "course not laid":
            # in pilot water a foul wind is waited out at anchor, not beaten (`_passage`)
            return bool(self._business.get("course_not_laid")) and not self._inner_leg()
        if name == "course laid":
            return not self._business.get("course_not_laid")
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

    # -- the work of each state ---------------------------------------------------------

    def _work(self, p: Perception, events: list[Any]) -> None:
        state = self.state
        if state is None:
            return
        kinds = {e.kind for e in events}
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
        if state in ("on passage", "beating", "running for shelter"):
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
        elif state == "at anchor":
            if "ship.under_way" in kinds or "ship.weighed" in kinds:
                self._waiting_at_road = False
        if "ship.brought_up" in kinds:
            self._business["brought_up"] = True
        if "ship.under_way" in kinds or "ship.aweigh" in kinds:
            self._business.pop("brought_up", None)

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
            if e.kind == "helm.set" and state_of_actor(str(e.actor or "")) is not None:
                self._business["course_not_laid"] = bool((e.data or {}).get("course_not_laid"))
        if "ship.filled_away" in kinds and p.manoeuvre not in ("hove to", "heaving to"):
            if leg.kind != "out":
                self._shape_leg()
        if self._business.get("course_not_laid") and self._inner_leg():
            # a course not laid in pilot water (package 40c, the captain's trials: the
            # schooner beat up the Goulet and took the ground on the Fillettes). Most often
            # it is the allowance for the stream that brings the steered course up to the
            # wind, the stream running along the channel; then she is conned for the mark
            # by the rhumb line with the stream under her, as a pilot conns. A wind foul
            # for the line itself is waited out at anchor, the at-anchor book trying again
            # on the flood by day.
            self._business.pop("course_not_laid", None)
            if self._conn_for(leg, p):
                return
            port = self._port_of(leg.port)
            where = port.name if port is not None else leg.words
            self._waiting_at_road = True
            self.give("come to an anchor", why=f"the wind does not serve to enter {where}")
            self._enter("at anchor")
            return
        dist = self._distance_by_account(leg)
        if dist is not None and (dist <= leg.reached_nm or self._passed(leg)):
            self._leg_reached(leg, p)
            return
        if "lookout.land_ahead" in kinds and leg.kind != "out":
            self._shape_leg(why="land ahead")

    def _conn_for(self, leg: Leg, p: Perception) -> bool:
        """The helm given the rhumb line to the leg's mark by account, as a pilot conns
        her up a channel with the stream under her, when that line is laid; False when
        the wind is foul for the line itself."""
        from freesail.evolutions.scripts import close_hauled_true_angle

        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None or p.wind_from_deg is None:
            return False
        bearing, _ = bearing_and_distance(here, leg.position)
        off = abs(units.wrap_pi(math.radians(bearing - p.wind_from_deg)))
        closest = close_hauled_true_angle(self.world.ship)
        if off < closest + math.radians(5.0):
            return False
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
        if leg.kind not in ("to", "out") or self.leg_i == 0 or leg.reached_nm > 1.0:
            return False
        nav = getattr(self.world, "navigation", None)
        here = nav.account_now() if nav is not None else None
        if here is None:
            return False
        before = self.legs[self.leg_i - 1]
        along, _ = bearing_and_distance(before.position, leg.position)
        to_mark, _ = bearing_and_distance(here, leg.position)
        return abs(units.wrap_pi(math.radians(to_mark - along))) > math.pi / 2.0

    def _leg_reached(self, leg: Leg, p: Perception) -> None:
        world = self.world
        if leg.kind == "road":
            port = self._port_of(leg.port)
            if port is not None and not self._tide_serves(port, p, "enter"):
                self._waiting_at_road = True
                self.give("come to an anchor", why=f"the tide does not serve to enter {port.name}")
                self._enter("at anchor")
                return
        if leg.kind == "anchorage":
            self.give("come to an anchor", why=f"at {leg.words}")
            self._advance()
            if self.intent is not None and self.intent.kind in ("passage", "home", "letter"):
                # the voyage's end (package 40c): she is not sailed again on the tide
                self.intent.done = True
            return
        if leg.kind == "station":
            self._enter("keeping station")
            return
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
        self.legs = Planner(self.world).legs_for(self.intent, start, departing)
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
        self.give(f"shape a course for {leg.words}", why=why)

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
            self._departing = port.id
            self.legs, self.leg_i = [], 0

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
        return  # the book keeps the station; the transitions watch for a sail

    def _keep_stranger(self, p: Perception) -> None:
        if self._stranger is None:
            near = self._nearest_stranger(p)
            self._stranger = near.get("id") if near else None

    def _nearest_stranger(self, p: Perception) -> dict[str, Any] | None:
        items = [s for s in p.strangers if not s.get("spoken")]
        if not items:
            return None
        return min(items, key=lambda s: s.get("estimate_m") or math.inf)

    def _is_enemy(self, s: dict[str, Any]) -> bool:
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
            and not s.get("spoken")
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


# ---------------------------------------------------------------------------
# The far-detail body as an interface (spec M6 §4, §19; 43 fills it)
# ---------------------------------------------------------------------------


def resolve_state(vessel: Any, state: str) -> bool:
    """The state machine's state resolved into a far-detail plan on a vessel of
    `freesail.world.ships` (one brain, two bodies): `hove to for weather` is no way, she
    lies to until told otherwise; `on passage` is her goal's plan, kept. The other
    states are 43's with the crewed promotion, and are refused here (False) so that no
    body is moved by a state it cannot resolve. Returns whether the state was resolved."""
    if state not in STATES:
        raise ValueError(f"'{state}' is no state of the machine.")
    if state not in FAR_DETAIL_STATES:
        return False
    if state == "hove to for weather":
        if vessel.state != state:
            vessel.saved_plan = list(vessel.plan)
            vessel.plan = [("lie_to", math.inf)]
    elif state == "on passage":
        if (
            vessel.state == "hove to for weather"
            and getattr(vessel, "saved_plan", None) is not None
        ):
            vessel.plan = list(vessel.saved_plan)
            vessel.saved_plan = None
            vessel.lying_to_s = 0.0
    vessel.state = state
    return True
