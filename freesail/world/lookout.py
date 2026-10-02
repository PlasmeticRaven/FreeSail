"""The lookout (spec M5 §12; package 32; package 33b's three faults): the sighting
model's reading in the log's words.

Once a game minute the World asks the lookout to look (`Lookout.look`): the chart says
what is within the horizon from the masthead and the weather's visibility, by each
feature's own rule (`freesail.world.chart.Chart.in_sight`), and the lookout says it as a
lookout did, by compass bearing and an estimated distance ("The Lizard bearing N by E,
distant four leagues"; "A light on the larboard bow, bearing NW by N"). The estimate is
the period's, to the nearest league or mile (`geo.estimate_words`), never the truth to a
cable; the bearing is true, the compass's variation being the reckoning's business
(package 33). A light at night is "a light": the lookout does not know whose it is, though
the reading's data names it for the master and the tests. In 5b the lookout is the
world's own voice at routine severity, notable for a landfall or a danger; in 5c the same
model sights sail, and later a small model may hold the station (decision 24).

The distance by estimation (package 33b; playtest 13: the Start at four miles, four
leagues and three leagues in an hour of calm) is the eye's judgement of a headland's
distance from its height and what shows of it, a fifth out either way as such estimates
are, drawn once per sighting episode from the `lookout` stream and held while she makes
no way: it is judged afresh only when she has moved a mile from where it was last judged,
so the figure in the list, the figure hailed and the figure a bearing is taken at are one
figure, and a calm does not re-draw it every hail. `what is in sight` names the dangers
first, then the lights, the land and the marks, nearest first within each, and the cap
of eight never cuts a danger off; a mark's name is whole mid-sentence ("Black Head", not
"black Head"). The lookout says when the chart ends ("the chart has nothing to the
northward of this"), hails a bearing steady and closing (the seaman's rule for a
collision course, here for a danger or the land: `lookout.closing`, the event `a bearing
steady and closing`), and on a moonlit night sees the land at a league
(`chart.MOONLIT_LAND_NM`; `sights.moonlit`).

The reading `what is in sight` (`freesail.api.readings`) is the last look's sightings,
and `the land` whether any land is among them, so a book may say `when the land is in
sight then ...`.

**Other sail** (spec M5 §25; package 35 began it with the pilot cutter, package 36 the
rest): a vessel of `freesail.world.ships` is sighted at the horizon her rig's height and
the eye give and hailed as "Sail ho!" with a bearing first (notable; the event `a sail
sighted`); then, as she nears, what the tops make out at the period's distances is a
routine line each time it changes (`lookout.made_out`: her rig and her course at
`ships.RIG_MADE_OUT_NM`, her colours or their want at `ships.COLOURS_MADE_OUT_NM`, the
event `a stranger's colours made out`; what she is at `ships.MADE_OUT_NM`), and a sail
gone from the horizon is "out of sight" (`lookout.sail_lost`, the event `a sail lost`).
`make her out` sends a glass aloft (`Lookout.make_out`) and answers with what the
distance allows, half as far again as the eye. `the strangers` (`Lookout.strangers`) is
every sail in sight with her bearing, her distance by estimation and what has been made
out of her, and never her position: the world keeps the truth and the captain keeps his
account, for other ships as for his own.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field, replace
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world.chart import CHART_EDGE_NM, NIGHT_LAND_NM, Chart, Feature, Sighting
from freesail.world.geo import Position, estimate_words

__all__ = [
    "CLOSING_FRACTION",
    "CLOSING_LAND_NM",
    "CLOSING_MINUTES",
    "CLOSING_STEADY_POINTS",
    "DEFAULT_HEIGHT_OF_EYE_M",
    "DISTANCE_BY_ESTIMATION_FRACTION",
    "ESTIMATE_HOLD_NM",
    "LOOKOUT_HAIL_MAX",
    "LOOKOUT_REPEAT_MIN",
    "READING_MAX",
    "SHORE_CLOSE_NM",
    "SHORE_ID",
    "Episode",
    "Lookout",
    "height_of_eye",
    "lead_words",
    "relative_words",
]

# A lookout with no masthead to climb (the point ship of the early milestones) looks
# from thirty metres, a frigate's topmast head; judgement.
DEFAULT_HEIGHT_OF_EYE_M = 30.0

# A feature lost and found again within this many minutes is not hailed again
# (judgement: a headland flickering at the edge of the haze is not a line a minute).
LOOKOUT_REPEAT_MIN = 30

# A look hails at most this many things newly in sight, dangers first, then lights, the
# land and the marks, nearest first; the rest are in the reading and not the log
# (judgement: off Falmouth's mouth fifty features are in sight, and a lookout hails the
# Black Rock, not every church behind the town).
LOOKOUT_HAIL_MAX = 6

# `what is in sight` names at most this many, dangers first and never cut off, then the
# rest nearest first, and counts the remainder.
READING_MAX = 8

# The shore itself is hailed, when no headland of the chart is in sight, within this
# many miles (package 33a; judgement: the cliffs seen close aboard in thick weather,
# the same three miles a danger is made out at, `chart.DANGER_SEEN_NM`), and within the
# visibility and the night's mile. Its sighting carries this id and is no mark.
SHORE_CLOSE_NM = 3.0
SHORE_ID = "the-shore"

# The distance off by estimation (spec §12's words, "twelve miles by estimation"; package
# 33a, moved here by 33b): the eye's judgement of a headland's distance from its height
# and what shows of it, a sixth of the distance one sigma either way, drawn once per
# sighting episode (judgement). It is held until she has moved a mile from where it was
# judged (judgement: an hour's run at a knot, the brief's "held while the ship makes
# under a knot"), then judged afresh with the same eye's error, so the estimate closes
# as she closes and does not wander in a calm.
DISTANCE_BY_ESTIMATION_FRACTION = 0.15
ESTIMATE_HOLD_NM = 1.0

# A bearing steady and closing (package 33b; the seaman's rule that a bearing which does
# not change while the range closes is a collision course): a danger at any distance it
# is seen at, or the land or a light within a league, seen ten minutes with its bearing
# within a point of where it first bore and its distance a fifth less, hailed once a
# sighting episode (judgement in the four numbers; a ship running in has every headland
# ahead steady and closing, and the hail is for what she may strike).
CLOSING_MINUTES = 10
CLOSING_STEADY_POINTS = 1.0
CLOSING_FRACTION = 0.8
CLOSING_LAND_NM = 3.0

MAST_CLASSES = frozenset({"mast", "topmast", "topgallant_mast", "royal_mast"})


def height_of_eye(ship: Any) -> float:
    """The lookout's eye at the topmast head: the deck's height above the water plus the
    lower mast and the topmast of the tallest chain standing (a topmast sent down or
    carried away brings him to the lower masthead); the default without a rig."""
    spars = getattr(ship, "spars", None)
    hull = getattr(ship, "hull", None)
    if not spars or hull is None:
        return DEFAULT_HEIGHT_OF_EYE_M
    deck = float(hull.spec.deck_height_m)
    best = 0.0
    for spar in spars.values():
        if spar.cls not in ("mast", "topmast") or spar.wrecked or spar.sent_down:
            continue
        chain = ship.spar_chain(spar)
        if any(p.wrecked or p.sent_down for p in chain):
            continue
        height = sum(float(p.height_m) for p in chain if p.cls in MAST_CLASSES)
        best = max(best, height)
    return deck + best if best > 0.0 else DEFAULT_HEIGHT_OF_EYE_M


def _key(name: str) -> str:
    """A name as it is matched: lower case, without its article or its punctuation."""
    words = "".join(c if c.isalnum() or c.isspace() else " " for c in name.lower()).split()
    if words and words[0] == "the":
        words = words[1:]
    return " ".join(words)


def relative_words(relative_rad: float) -> str:
    """Where a thing lies from the ship's head, in the lookout's words: right ahead, on
    the starboard bow, abeam to larboard, on the larboard quarter, right astern."""
    points = units.rad_to_points(abs(units.wrap_pi(relative_rad)))
    side = "starboard" if units.wrap_pi(relative_rad) >= 0 else "larboard"
    if points < 1.0:
        return "right ahead"
    if points < 6.0:
        return f"on the {side} bow"
    if points < 10.0:
        return f"abeam to {side}"
    if points < 15.0:
        return f"on the {side} quarter"
    return "right astern"


def lead_words(words: str) -> str:
    """A sentence's words mid-sentence: the first letter lowered when it is an article's
    ('A light ...', 'The land ...'), kept when it is a proper name's ('Black Head ...'):
    the reading's first-letter rule stops at a proper name (package 33b)."""
    first = words.split(" ", 1)[0]
    if first in ("A", "An", "The"):
        return words[:1].lower() + words[1:]
    return words


_ORDER = {"danger": 0, "sail": 1, "light": 2, "land": 3, "mark": 4}

# The words the lookout's sail is asked for by (`find`), for a bearing of her (package 35).
_SAIL_WORDS = frozenset(
    {
        "sail",
        "a sail",
        "the sail",
        "the stranger",
        "stranger",
        "cutter",
        "the cutter",
        "pilot cutter",
        "the pilot cutter",
    }
)
# A sail by her rig as the tops made it out (package 36): the word in the lookout's name
# for her ("a brig, standing to the eastward").
_RIG_WORDS = {
    "brig": "brig",
    "ship": "ship",
    "frigate": "frigate",
    "schooner": "schooner",
    "merchantman": "merchant",
}


@dataclass
class Episode:
    """One sighting episode of a feature: the eye's error drawn for it, the estimate held,
    where it was last judged, where the feature first bore for the closing rule."""

    factor: float
    estimate_m: float
    judged_at: tuple[float, float]
    first_bearing_deg: float
    first_distance_m: float
    since_minute: int
    last_minute: int
    closing_said: bool = False


@dataclass
class Lookout:
    chart: Chart
    sightings: list[Sighting] = field(default_factory=list)
    height_of_eye_m: float = DEFAULT_HEIGHT_OF_EYE_M
    _announced: dict[str, int] = field(default_factory=dict)  # feature id -> the minute hailed
    _had_land: bool = False
    _looked: bool = False
    _episodes: dict[str, Episode] = field(default_factory=dict)
    _stream: random.Random | None = None
    # the other sail's estimates are drawn from a stream of their own (package 35), so
    # that a sail in sight never moves the land's draws and the pinned passages' ticks
    _sail_stream: random.Random | None = None
    _edge_said: bool = False
    _moonlit_said: bool = False
    moonlit: bool = False
    # other sail (package 36): the level made out of each sail so far (0 a sail, 1 her
    # rig, 2 her colours, 3 what she is) and the words of her last bearing, for the line
    # when she is lost
    _sail_said: dict[str, int] = field(default_factory=dict)
    _sails_seen: dict[str, str] = field(default_factory=dict)

    def look(self, world: Any) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """Look from the masthead now: the sightings kept for the reading, and the log's
        lines for what is newly in sight, a landfall or a danger notable, for a bearing
        steady and closing, for the chart's edge and for the land lost. Nothing on the
        plane."""
        pos = world.position
        if pos is None:
            return []
        if self._stream is None:
            rng = getattr(world, "rng", None)
            self._stream = rng.stream("lookout") if rng is not None else random.Random(0)
            self._sail_stream = rng.stream("sail") if rng is not None else random.Random(1)
        conditions = getattr(world, "conditions", None)
        visibility_nm = conditions.visibility_nm if conditions is not None else None
        self.height_of_eye_m = height_of_eye(world.ship)
        daylight = world.daylight
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        self.moonlit = False
        if daylight != "day":
            from freesail.world.sights import moon_now, moonlit

            self.moonlit = moonlit(moon_now(world))
            if self.moonlit and not self._moonlit_said:
                self._moonlit_said = True
                lines.append(
                    (
                        Severity.ROUTINE,
                        "lookout.moonlight",
                        "A moonlit night; the land may be made out at a league.",
                        {"moonlit": True},
                    )
                )
        else:
            self._moonlit_said = False
        found = self.chart.in_sight(
            pos,
            self.height_of_eye_m,
            visibility_nm,
            daylight,
            world.clock.ship_time,
            self.moonlit,
            tide_m=float(getattr(world, "tide_height_m", 0.0)),  # a rock covered (34)
        )
        if not any(s.seen_as == "land" for s in found):
            shore = self._shore_close_aboard(pos, visibility_nm, daylight)
            if shore is not None:
                found.append(shore)
                found.sort(key=lambda s: s.distance_m)
        vessels = getattr(world, "vessels", None)
        if vessels is not None and vessels.vessels:
            # the other sail (spec M5 §25; package 35's pilot cutter): at the horizon her
            # rig's height and the eye give, within the weather's visibility
            found.extend(vessels.in_sight(pos, self.height_of_eye_m, visibility_nm, daylight))
            found.sort(key=lambda s: s.distance_m)
        minute = world.clock.tick // 60
        heading = float(world.ship.heading)
        land_now = any(s.seen_as in ("land", "light") for s in found)
        first_land = land_now and not self._had_land
        # what is newly in sight, dangers first, then lights, the land, the marks, nearest
        # first within each; a lookout hails the few that matter (LOOKOUT_HAIL_MAX) and the
        # rest are in the reading, not the log
        fresh = []
        judged: list[Sighting] = []
        for s in found:
            last = self._announced.get(s.feature.id)
            self._announced[s.feature.id] = minute
            new_episode = last is None or minute - last >= LOOKOUT_REPEAT_MIN
            if new_episode:
                fresh.append(s)
            judged.append(self._judge(s, pos, minute, new_episode))
        found = judged
        fresh_ids = {s.feature.id for s in fresh}
        fresh = [s for s in found if s.feature.id in fresh_ids]
        fresh.sort(key=lambda s: (_ORDER.get(s.seen_as, 9), s.distance_m))
        for s in fresh[:LOOKOUT_HAIL_MAX]:
            text = self.words(s, heading)
            # a danger is notable; so is everything seen in the look that makes the
            # landfall, and a sail ("Sail ho!", package 35)
            notable = s.seen_as in ("danger", "sail") or first_land
            data = self._data(s, heading) | {
                "height_of_eye_m": round(self.height_of_eye_m, 1),
                "landfall": bool(first_land),
            }
            lines.append(
                (Severity.NOTABLE if notable else Severity.ROUTINE, "lookout.sighting", text, data)
            )
        lines.extend(self._closing(found, heading, minute))
        lines.extend(self._sails(world, found, fresh_ids, heading))
        if self._had_land and not land_now and self._looked:
            lines.append(
                (Severity.ROUTINE, "lookout.lost", "The land is out of sight.", {"count": 0})
            )
        edges = self.chart.edge_near(pos, CHART_EDGE_NM * units.NAUTICAL_MILE)
        if edges and not self._edge_said:
            self._edge_said = True
            lines.append(
                (
                    Severity.ROUTINE,
                    "lookout.chart_edge",
                    f"The chart has nothing to the {_ward(edges)} of this; the coast beyond is "
                    f"uncharted.",
                    {"edges": edges},
                )
            )
        elif not edges:
            self._edge_said = False
        self.sightings = found
        self._had_land = land_now
        self._looked = True
        return lines

    def _judge(self, s: Sighting, pos: Position, minute: int, new_episode: bool) -> Sighting:
        """The distance by estimation for a sighting: drawn once an episode and held
        while she has not moved a mile from where it was judged; the shore close aboard
        is judged true (the cliffs are at the distance they are)."""
        if s.feature.id == SHORE_ID:
            return replace(s, estimate_m=s.distance_m)
        ep = self._episodes.get(s.feature.id)
        here = (pos.lat_deg, pos.lon_deg)
        if ep is None or new_episode:
            assert self._stream is not None
            stream = (
                self._sail_stream if s.seen_as == "sail" and self._sail_stream else self._stream
            )
            factor = max(0.3, 1.0 + stream.gauss(0.0, DISTANCE_BY_ESTIMATION_FRACTION))
            ep = Episode(
                factor, s.distance_m * factor, here, s.bearing_deg, s.distance_m, minute, minute
            )
            self._episodes[s.feature.id] = ep
        else:
            moved = _miles_between(ep.judged_at, here)
            if moved >= ESTIMATE_HOLD_NM:
                ep.estimate_m = s.distance_m * ep.factor
                ep.judged_at = here
            ep.last_minute = minute
        return replace(s, estimate_m=ep.estimate_m)

    def _closing(
        self, found: list[Sighting], heading: float, minute: int
    ) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """A danger or the land whose bearing has held within a point for ten minutes
        while the distance closed by a fifth: hailed once an episode."""
        out = []
        for s in found:
            if s.seen_as not in ("danger", "land", "light") or s.feature.id == SHORE_ID:
                continue
            if s.seen_as != "danger" and s.distance_m > CLOSING_LAND_NM * units.NAUTICAL_MILE:
                continue
            ep = self._episodes.get(s.feature.id)
            if ep is None or ep.closing_said or minute - ep.since_minute < CLOSING_MINUTES:
                continue
            swung = abs(units.wrap_pi(math.radians(s.bearing_deg - ep.first_bearing_deg)))
            if swung > units.points_to_rad(CLOSING_STEADY_POINTS):
                continue
            if s.distance_m > CLOSING_FRACTION * ep.first_distance_m:
                continue
            ep.closing_said = True
            point = units.point_name(math.radians(s.bearing_deg))
            name = "A light" if s.seen_as == "light" else _head(s.feature.name)
            text = (
                f"{name} bearing {point}, steady and closing: distant {estimate_words(s.judged_m)}."
            )
            data = s.to_dict() | {
                "relative": relative_words(math.radians(s.bearing_deg) - heading),
                "estimate": estimate_words(s.judged_m),
                "closing": True,
            }
            out.append((Severity.NOTABLE, "lookout.closing", text, data))
        return out

    # -- other sail (spec M5 §25; package 36) -------------------------------------------

    @staticmethod
    def _data(s: Sighting, heading_rad: float) -> dict[str, Any]:
        """A sighting's data for a line or a reading: a sail's without the truth's
        distance (the captain has her bearing and his estimate, never her position)."""
        d = s.to_dict()
        if s.seen_as == "sail":
            d.pop("distance_m", None)
        return d | {
            "relative": relative_words(math.radians(s.bearing_deg) - heading_rad),
            "estimate": estimate_words(s.judged_m),
        }

    def _vessel(self, world: Any, s: Sighting) -> Any:
        vessels = getattr(world, "vessels", None)
        return vessels.get(s.feature.modern) if vessels is not None else None

    def _sails(
        self, world: Any, found: list[Sighting], fresh_ids: set[str], heading: float
    ) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """What the tops make out of each sail as she nears, a routine line as it
        changes; and a sail lost from the horizon."""
        out: list[tuple[Severity, str, str, dict[str, Any]]] = []
        seen: dict[str, str] = {}
        for s in found:
            if s.seen_as != "sail":
                continue
            v = self._vessel(world, s)
            if v is None:
                continue
            fid = s.feature.id
            relative = relative_words(math.radians(s.bearing_deg) - heading)
            level, words = v.made_out(s.distance_m)
            said = self._sail_said.get(fid)
            if said is None:
                # hailed this look: the hail says what the distance allows
                self._sail_said[fid] = level
            elif level > said:
                self._sail_said[fid] = level
                out.append(self._made_out_line(v, s, level, words, relative, glass=False))
            seen[fid] = f"{_head(self._sail_word(v, level))} {relative}"
        for fid, where in list(self._sails_seen.items()):
            if fid not in seen:
                self._sail_said.pop(fid, None)
                out.append(
                    (
                        Severity.ROUTINE,
                        "lookout.sail_lost",
                        f"{where} is out of sight.",
                        {"id": fid.removeprefix("sail:"), "words": where},
                    )
                )
        self._sails_seen = seen
        return out

    @staticmethod
    def _sail_word(v: Any, level: int) -> str:
        """'the sail', 'the brig', 'the merchant brig': how the lookout names her now."""
        if level >= 3:
            return "the " + (v.what or v.name).split(",")[0].removeprefix("a ").removeprefix("the ")
        if level >= 1:
            return "the " + v.kind.removeprefix("a ")
        return "the sail"

    def _made_out_line(
        self, v: Any, s: Sighting, level: int, words: str, relative: str, glass: bool
    ) -> tuple[Severity, str, str, dict[str, Any]]:
        who = self._sail_word(v, level - 1 if level > 1 else 0)
        colours = level >= 2 and v.shows_colours and bool(v.nation_adjective)
        if glass:
            text = f"The glass aloft makes out {who} {relative}: {words}."
        elif level == 1:
            text = f"{_head(who)} {relative} is {words}."
        elif level == 2:
            text = (
                f"{_head(who)} {relative} shows {v.colours_words()}."
                if colours
                else (f"{_head(who)} {relative} is {v.colours_words()}.")
            )
        else:
            text = f"{_head(who)} {relative} is {words}."
        data = {
            "id": v.id,
            "level": level,
            "colours": bool(colours),
            "nation": v.nation if colours else None,
            "words": words,
            "relative": relative,
            "bearing_deg": round(s.bearing_deg, 1),
            "estimate_m": None if s.estimate_m is None else round(s.estimate_m),
            "glass": glass,
        }
        return Severity.ROUTINE, "lookout.made_out", text, data

    def make_out(self, world: Any, which: str | None = None) -> tuple[str, dict[str, Any]]:
        """`make her out`: a glass sent aloft, and the answer at once with what the
        distance allows (`ships.GLASS_FACTOR` further than the eye); refused in words
        with no sail in sight. Returns (the line, its data)."""
        from freesail.orders.errors import OrderError

        sails = [s for s in self.sightings if s.seen_as == "sail"]
        if not sails:
            raise OrderError("No sail in sight to make out.")
        s = self.find(which) if which else None
        if which and s is None:
            raise OrderError(f"Nothing in sight answers to {which!r}; the strangers are listed.")
        if s is None:
            s = min(sails, key=lambda x: x.distance_m)
        v = self._vessel(world, s)
        heading = float(world.ship.heading)
        relative = relative_words(math.radians(s.bearing_deg) - heading)
        if v is None:
            return f"The glass aloft makes out nothing more of the sail {relative}.", {
                "id": s.feature.id,
                "glass": True,
            }
        level, words = v.made_out(s.distance_m, glass=True)
        self._sail_said[s.feature.id] = max(level, self._sail_said.get(s.feature.id, 0))
        if level == 0:
            text = (
                f"The glass aloft makes out nothing more of the sail {relative}: her hull is "
                f"below the horizon, distant {estimate_words(s.judged_m)}."
            )
            return text, {"id": v.id, "level": 0, "colours": False, "glass": True}
        _, _, text, data = self._made_out_line(v, s, level, words, relative, glass=True)
        return text, data

    def strangers(self, world: Any, heading_rad: float) -> dict[str, Any]:
        """`the strangers`: every sail in sight, nearest first, with her bearing, her
        distance by estimation and what has been made out of her; never her position."""
        sails = sorted(
            (s for s in self.sightings if s.seen_as == "sail"), key=lambda s: s.distance_m
        )
        items = []
        for s in sails:
            v = self._vessel(world, s)
            level = self._sail_said.get(s.feature.id, 0)
            point = units.point_name(math.radians(s.bearing_deg))
            relative = relative_words(math.radians(s.bearing_deg) - heading_rad)
            head = self._sail_word(v, level).removeprefix("the ") if v is not None else "sail"
            head = "a sail" if head == "sail" else f"a {head}"
            known = v.words_at(level) if v is not None and level > 0 else ""
            detail = ""
            if known:
                # the course and the colours after the bearing: what has been made out
                detail = ": " + known.split(", ", 1)[1] if ", " in known else ""
            items.append(
                {
                    "id": s.feature.modern,
                    "bearing_deg": round(s.bearing_deg, 1),
                    "bearing": point,
                    "relative": relative,
                    "estimate_m": None if s.estimate_m is None else round(s.estimate_m),
                    "estimate": estimate_words(s.judged_m),
                    "made_out": level,
                    "known": known or "a sail",
                    "words": f"{head} {relative}, bearing {point}, distant "
                    f"{estimate_words(s.judged_m)}{detail}",
                }
            )
        if not items:
            return {"in_sight": False, "count": 0, "words": "no sail in sight", "items": []}
        words = "; ".join(lead_words(i["words"]) for i in items)
        return {"in_sight": True, "count": len(items), "words": words, "items": items}

    def _shore_close_aboard(
        self, pos: Any, visibility_nm: float | None, daylight: str
    ) -> Sighting | None:
        """The shore itself, close aboard, when no headland of the chart is in sight
        (package 33a: in thick weather a ship standing in sees the cliffs before any
        named mark, and a landfall in fog is made on them). From the chart's distance
        field: within `SHORE_CLOSE_NM`, the visibility, and at night `NIGHT_LAND_NM`. A
        sighting of the shore is land for the reading `the land`, and no mark to take a
        bearing of."""
        found = self.chart.coast_distance(pos)
        if found is None:
            return None
        distance_m, bearing_deg = found
        limit = SHORE_CLOSE_NM
        if visibility_nm is not None:
            limit = min(limit, float(visibility_nm))
        if daylight == "night":
            limit = min(limit, SHORE_CLOSE_NM if self.moonlit else NIGHT_LAND_NM)
        if distance_m > limit * units.NAUTICAL_MILE:
            return None
        coast = self.chart.coast_at(pos)
        name = f"the land about {coast.name}" if coast is not None and coast.name else "the land"
        shore = Feature(SHORE_ID, "headland", name, pos.lat_deg, pos.lon_deg, height_m=0.0)
        return Sighting(shore, bearing_deg, distance_m, "land", distance_m)

    @staticmethod
    def words(s: Sighting, heading_rad: float) -> str:
        """The sighting in the lookout's words."""
        point = units.point_name(math.radians(s.bearing_deg))
        relative = relative_words(math.radians(s.bearing_deg) - heading_rad)
        distance = estimate_words(s.judged_m)
        if s.seen_as == "light":
            return f"A light {relative}, bearing {point}."
        head = _head(s.feature.name)
        if s.seen_as == "sail":
            # the hail for other sail (spec M5 §25, truth 67's form; package 35): a bearing
            # first, her rig only as she nears (`ships.Vessel.seen_as_feature`)
            return f"Sail ho! {head} {relative}, bearing {point}, distant {distance}."
        if s.feature.id == SHORE_ID:
            return f"{head} close aboard {relative}, bearing {point}, distant {distance}."
        if s.seen_as == "danger":
            # a rock that covers and dries is "showing" when it is seen (package 34)
            showing = " showing" if s.feature.kind == "drying" else ""
            return f"{head}{showing} bearing {point}, distant {distance}: a danger."
        return f"{head} bearing {point}, distant {distance}."

    # -- for the bearing taken (package 33a, spec M5 §13, §15) ---------------------------

    def find(self, name: str) -> Sighting | None:
        """The sighting a name means, for `take a bearing of <mark>` and `the bearing of
        <mark>`: a feature in sight by its period name or its modern one ('the Lizard',
        'Lizard Point'), 'the land' for the nearest land in sight, 'the light' for the
        nearest light; None when nothing in sight answers to it."""
        key = _key(name)
        if not key:
            return None
        if key in ("land", "shore", "coast", "headland", "nearest land"):
            # the nearest land; at night, when the land itself is not to be seen, the
            # nearest light or mark that is (the reading `the land` counts them so); the
            # shore close aboard is no mark to take a bearing of
            for kinds in (("land",), ("light", "mark")):
                land = [
                    s for s in self.sightings if s.seen_as in kinds and s.feature.id != SHORE_ID
                ]
                if land:
                    return min(land, key=lambda s: s.distance_m)
            return None
        if key in ("light", "nearest light", "the light"):
            lights = [s for s in self.sightings if s.seen_as == "light"]
            return min(lights, key=lambda s: s.distance_m) if lights else None
        if key in _SAIL_WORDS or f"the {key}" in _SAIL_WORDS or key in _RIG_WORDS:
            # a sail in sight, by the lookout's words for her (package 35), or by her rig
            # as made out ('the brig': the nearest brig among the sails; package 36)
            sails = [s for s in self.sightings if s.seen_as == "sail"]
            if key in _RIG_WORDS:
                rig = _RIG_WORDS[key]
                named = [s for s in sails if rig in _key(s.feature.name)]
                return min(named, key=lambda s: s.distance_m) if named else None
            return min(sails, key=lambda s: s.distance_m) if sails else None
        for s in self.sightings:
            f = s.feature
            if f.id == SHORE_ID:
                continue  # the shore close aboard is no mark of the chart
            if key in (_key(f.name), _key(f.modern), _key(f.id.replace("-", " "))):
                return s
        return None

    # -- the readings -------------------------------------------------------------------

    def reading(self, heading_rad: float) -> dict[str, Any]:
        """`what is in sight`: the last look's sightings with the lookout's words, the
        dangers first and never cut off, then the lights, the land and the marks nearest
        first; or nothing in sight. Near the chart's edge the words say the chart ends."""
        ordered = sorted(self.sightings, key=lambda s: (_ORDER.get(s.seen_as, 9), s.distance_m))
        items = []
        for s in ordered:
            items.append(
                self._data(s, heading_rad) | {"words": self.words(s, heading_rad).rstrip(".")}
            )
        dangers = [i for i in items if i["seen_as"] == "danger"]
        rest = [i for i in items if i["seen_as"] != "danger"]
        shown = dangers + rest[: max(0, READING_MAX - len(dangers))]
        named = [lead_words(i["words"]) for i in shown]
        more = len(items) - len(named)
        if more > 0:
            named.append(f"and {more} more in sight")
        words = "; ".join(named) or "nothing in sight"
        if self._edge_said:
            words += "; the chart ends here"
        return {"count": len(items), "words": words, "items": items}

    def sail(self, heading_rad: float) -> dict[str, Any]:
        """`a sail in sight` (package 35; the row the registry held absent since M4): in
        sight or not, with the nearest sail and the lookout's words for each."""
        sails = sorted(
            (s for s in self.sightings if s.seen_as == "sail"), key=lambda s: s.distance_m
        )
        items = [
            self._data(s, heading_rad)
            | {"words": self.words(s, heading_rad).removeprefix("Sail ho! ").rstrip(".")}
            for s in sails
        ]
        if not items:
            return {"in_sight": False, "words": "not in sight", "count": 0, "items": []}
        words = "in sight: " + items[0]["words"]
        if len(items) > 1:
            words += f", and {len(items) - 1} more"
        return {
            "in_sight": True,
            "words": words,
            "count": len(items),
            "items": items,
            "nearest": items[0],
        }

    def land(self, heading_rad: float) -> dict[str, Any]:
        """`the land`: in sight or not, with the nearest land or light sighted."""
        # the land: the shore, its marks and its lights; a rock in sight is a danger, not land
        land = [s for s in self.sightings if s.seen_as in ("land", "light", "mark")]
        if not land:
            return {"in_sight": False, "words": "not in sight", "nearest": None}
        nearest = min(land, key=lambda s: s.distance_m)
        return {
            "in_sight": True,
            "words": "in sight",
            "nearest": nearest.to_dict() | {"words": self.words(nearest, heading_rad).rstrip(".")},
        }


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


def _ward(edges: list[str]) -> str:
    return " and the ".join(f"{e}ward" for e in edges)


def _miles_between(a: tuple[float, float], b: tuple[float, float]) -> float:
    dn = (b[0] - a[0]) * 60.0
    de = (b[1] - a[1]) * 60.0 * math.cos(math.radians(0.5 * (a[0] + b[0])))
    return math.hypot(de, dn)
