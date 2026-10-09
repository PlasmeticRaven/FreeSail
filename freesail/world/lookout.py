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
are, drawn once per sighting episode from the `lookout` stream. It is judged afresh, with
the same eye's error, whenever the true distance is a tenth more or less than it was at
the last judging (package 37d: `ESTIMATE_REFRESH_FRACTION`), for the land and for a sail
alike, so the figure in the list, the figure hailed and the figure a bearing's words
give are one figure, it follows her in as she closes, and a calm still re-draws nothing,
since nothing has changed and the error is the sighting's. `what is in sight` names the dangers
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

**The shore itself** (package 37d; the review of gate 5c's playtests, 5.1) is a sighting
at every look within a league, the visibility and the night's mile, whatever headlands
are in sight beside it: the nearest dry ground by the chart's own search
(`chart.Chart.nearest_shore`), hailed once a sighting, and never a mark to take a
bearing of. `the nearest land` (`Lookout.nearest_land`) is that sighting as a reading:
where it lies from her head, its bearing to the point, its distance by estimation and
the coast's name. **Land ahead** (`Lookout._land_ahead`) is the lookout's one urgent
word: along her course made good and a point on either side, the first dry ground at the
tide's present height or danger in sight, within what he can see of the shore; a notable
line when she would be on it in under ten minutes at her present speed over the ground
and an urgent one under four, each once an approach. It is the eye's judgement of a
bearing that does not change and a distance that does, so it reads her true motion, and
only toward what can be seen: in fog it is silent and the lead is the guard.

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
from freesail.world.geo import Position, estimate_words, name_words

__all__ = [
    "CLOSING_FRACTION",
    "CLOSING_LAND_NM",
    "CLOSING_MINUTES",
    "CLOSING_STEADY_POINTS",
    "DEFAULT_HEIGHT_OF_EYE_M",
    "DISTANCE_BY_ESTIMATION_FRACTION",
    "ESTIMATE_REFRESH_FRACTION",
    "LAND_AHEAD_CLEAR_LOOKS",
    "LAND_AHEAD_CLEAR_MIN",
    "LAND_AHEAD_NOTABLE_MIN",
    "LAND_AHEAD_POINTS",
    "LAND_AHEAD_URGENT_MIN",
    "LAND_AHEAD_WAY_KN",
    "LOOKOUT_HAIL_MAX",
    "LOOKOUT_REPEAT_MIN",
    "READING_MAX",
    "SHORE_CLOSE_ABOARD_NM",
    "SHORE_CLOSE_NM",
    "SHORE_ID",
    "Episode",
    "Lookout",
    "ahead_words",
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

# The shore itself is a sighting within this many miles (package 33a; judgement: the
# cliffs seen close aboard in thick weather, the same three miles a danger is made out
# at, `chart.DANGER_SEEN_NM`), and within the visibility and the night's mile (a league
# on a moonlit night). Package 33a hailed it only when no headland of the chart was in
# sight, so off any named coast the nearest land was never spoken of; since package 37d
# it is a sighting at every look. Its sighting carries this id and is no mark. It is said
# "close aboard" within a mile (judgement on the words).
SHORE_CLOSE_NM = 3.0
SHORE_CLOSE_ABOARD_NM = 1.0
SHORE_ID = "the-shore"

# The distance off by estimation (spec §12's words, "twelve miles by estimation"; package
# 33a, moved here by 33b): the eye's judgement of a headland's distance from its height
# and what shows of it, a sixth of the distance one sigma either way, drawn once per
# sighting episode (judgement). Package 33b held it until the ship herself had moved a
# mile, so that a calm should not re-draw it; that rule told the Harpy "Penlee Point ...
# a mile" at under two cables, and kept a cutter at "two miles" for 37 minutes while her
# bearing swung from S to NW by N (the review of gate 5c's playtests, 5.1). Since package
# 37d it is judged afresh, with the same eye's error for the sighting, whenever the true
# distance is this fraction more or less than it was at the last judging (judgement: a
# tenth, the least change an eye that is a sixth out could be said to see), for the land
# and for a sail alike; a calm re-draws nothing, since nothing has changed.
DISTANCE_BY_ESTIMATION_FRACTION = 0.15
ESTIMATE_REFRESH_FRACTION = 0.1

# Land ahead (package 37d; the review of gate 5c's playtests, 5.1 and C.3 of its reader's
# report: nothing the lookout said was urgent, and the Harpy's three "steady and closing"
# hails came 46 to 59 minutes before she struck). In the lookout's minute, with way on
# over the ground (half a knot, `physics.hull.WAY_ON_KN`'s figure) and not at anchor or
# aground: along her course made good since the last look and a point on either side
# (the seaman's "bearing steady" is within a point, `CLOSING_STEADY_POINTS`), the first
# dry ground at the tide's present height or danger in sight, within what he can see of
# the shore. The time to it at her present speed over the ground: under ten minutes a
# notable line, under four an urgent one (the owner's figures from the review's 8.2,
# judgement: ten minutes is time to wear a frigate or let go an anchor, four to put the
# helm down), each once an approach; the approach is over, and both armed again, when
# five looks together (judgement) find nothing ahead within a quarter of an hour.
LAND_AHEAD_NOTABLE_MIN = 10
LAND_AHEAD_URGENT_MIN = 4
LAND_AHEAD_CLEAR_MIN = 15
LAND_AHEAD_CLEAR_LOOKS = 5
LAND_AHEAD_POINTS = 1.0
LAND_AHEAD_WAY_KN = 0.5
# The cast along each line steps by the shore's own distance while that is more than this
# margin off (the field is in whole cells and within two per cent), and by this step when
# nearer, reading the depth for dry ground (judgement: a harbour cell and a little).
LAND_AHEAD_MARGIN_M = 100.0
LAND_AHEAD_STEP_M = 20.0
# two looks are a minute apart; a longer gap (a load, the first look) casts nothing
LAND_AHEAD_LOOK_GAP_S = 120

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
    words = name_words(name)
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


def ahead_words(relative_rad: float) -> str:
    """Where a thing she is standing into lies from her head, finer than
    `relative_words` forward: right ahead within half a point, fine on the bow within
    two, then as the lookout says anything."""
    points = units.rad_to_points(abs(units.wrap_pi(relative_rad)))
    if points < 0.5:
        return "right ahead"
    if points < 2.0:
        side = "starboard" if units.wrap_pi(relative_rad) >= 0 else "larboard"
        return f"fine on the {side} bow"
    return relative_words(relative_rad)


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
    """One sighting episode of a feature: the eye's error drawn for it, the estimate as
    last judged, where the feature first bore for the closing rule, and the true distance
    at the last judging (package 37d: judged afresh when it has changed by a tenth; nought
    in an episode from a checkpoint of before, which is judged afresh at its next
    look)."""

    factor: float
    estimate_m: float
    first_bearing_deg: float
    first_distance_m: float
    since_minute: int
    last_minute: int
    closing_said: bool = False
    judged_m: float = 0.0


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
    _sail_known: dict[str, str] = field(default_factory=dict)  # the words made out so far
    # package 37d, each with a plain default so that a checkpoint from before loads with
    # it: the shore's estimates from a stream of their own (so that the shore, now always
    # a sighting, moves no headland's draw); how far the last look could see the shore,
    # and what bounded it ("" a league, "night", "weather"); where and when the last look
    # was made, for her course made good; and the land-ahead lines said this approach
    # with the looks together that found nothing ahead
    _shore_stream: random.Random | None = None
    _shore_limit_nm: float = SHORE_CLOSE_NM
    _shore_bound: str = ""
    _looked_from: tuple[int, float, float] | None = None
    _ahead_notable: bool = False
    _ahead_urgent: bool = False
    _ahead_clear: int = 0

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
        if self._shore_stream is None:
            # its own check: a lookout from a checkpoint of before has the other two
            rng = getattr(world, "rng", None)
            self._shore_stream = rng.stream("shore") if rng is not None else random.Random(2)
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
        # the shore itself, at every look (package 37d: it was looked for only when no
        # headland of the chart was in sight, so off any named coast the nearest land
        # was never spoken of)
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
        lines.extend(self._land_ahead(world, pos, found, heading))
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
        """The distance by estimation for a sighting: the eye's error drawn once an
        episode, and the distance judged afresh with it whenever the true distance is a
        tenth more or less than it was at the last judging (package 37d), for the land,
        the shore and a sail alike. A calm re-draws nothing: nothing has changed, and
        the error is the sighting's."""
        ep = self._episodes.get(s.feature.id)
        if ep is None or new_episode:
            assert self._stream is not None
            stream = self._stream
            if s.seen_as == "sail" and self._sail_stream:
                stream = self._sail_stream
            elif s.feature.id == SHORE_ID and self._shore_stream:
                stream = self._shore_stream
            factor = max(0.3, 1.0 + stream.gauss(0.0, DISTANCE_BY_ESTIMATION_FRACTION))
            ep = Episode(
                factor,
                s.distance_m * factor,
                s.bearing_deg,
                s.distance_m,
                minute,
                minute,
                judged_m=s.distance_m,
            )
            self._episodes[s.feature.id] = ep
        else:
            was = ep.judged_m
            if was <= 0.0 or abs(s.distance_m - was) >= ESTIMATE_REFRESH_FRACTION * was:
                ep.estimate_m = s.distance_m * ep.factor
                ep.judged_m = s.distance_m
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
                self._sail_known[fid] = v.words_at(level)
            elif level > said:
                self._sail_said[fid] = level
                self._sail_known[fid] = v.words_at(level)
                out.append(self._made_out_line(v, s, level, words, relative, glass=False))
            seen[fid] = f"{_head(self._sail_word(v, level))} {relative}"
        for fid, where in list(self._sails_seen.items()):
            if fid not in seen:
                self._sail_said.pop(fid, None)
                self._sail_known.pop(fid, None)
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

    def sail_name(self, fid: str, default: str = "a sail") -> str:
        """How a sail is named in an order's words from what has been made out of her so
        far, eye or glass: 'a sail', 'a brig', 'a brig-sloop of war' (the first words of
        `the strangers`)."""
        return (self._sail_known.get(fid) or default).split(",")[0].split(";")[0]

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
        if level >= self._sail_said[s.feature.id]:
            self._sail_known[s.feature.id] = v.words_at(level)
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
            if v is not None and level >= 1:
                # the course and the colours after the bearing: what has been made out
                detail = ": " + v.course_words()
                if level >= 2:
                    detail += "; " + v.colours_words()
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
                    # her nation once her colours are made out and she shows them; None
                    # while she is a stranger (too far, or no colours)
                    "nation": v.nation
                    if v is not None and level >= 2 and v.shows_colours and v.nation_adjective
                    else None,
                    "spoken": bool(v is not None and v.spoken),  # within hail at any time
                    "words": f"{head} {relative}, bearing {point}, distant "
                    f"{estimate_words(s.judged_m)}{detail}",
                }
            )
        if not items:
            return {"in_sight": False, "count": 0, "words": "no sail in sight", "items": []}
        words = "; ".join(lead_words(i["words"]) for i in items)
        return {"in_sight": True, "count": len(items), "words": words, "items": items}

    def stranger(self, world: Any, heading_rad: float, own_nation: str | None) -> dict[str, Any]:
        """`a stranger in sight`: the sail in sight that is not known for one of the ship's
        own nation, the nearest first: every sail is a stranger until her colours are made
        out (Falconer 1780, COLOURS), and one that shows none or another nation's stays
        one until she is spoken within hail (what follows is milestone 7's). For the
        book: a cruiser chases strangers, and not the port's own cutter nor a sail she has
        spoken."""
        every = self.strangers(world, heading_rad)
        items = [
            i
            for i in every["items"]
            if (i["nation"] is None or i["nation"] != own_nation) and not i["spoken"]
        ]
        if not items:
            return {"in_sight": False, "count": 0, "words": "no stranger in sight", "items": []}
        words = "; ".join(lead_words(i["words"]) for i in items)
        return {"in_sight": True, "count": len(items), "words": words, "items": items}

    def _shore_limit(self, visibility_nm: float | None, daylight: str) -> tuple[float, str]:
        """How far the lookout can see the shore itself, in miles, and what bounds it:
        `SHORE_CLOSE_NM` by day, the visibility, and at night `NIGHT_LAND_NM` (a league
        on a moonlit night); "" when nothing bounds it short of the league."""
        limit, bound = SHORE_CLOSE_NM, ""
        if visibility_nm is not None and float(visibility_nm) < limit:
            limit, bound = float(visibility_nm), "weather"
        if daylight == "night" and not self.moonlit and NIGHT_LAND_NM < limit:
            limit, bound = NIGHT_LAND_NM, "night"
        return limit, bound

    def _shore_close_aboard(
        self, pos: Any, visibility_nm: float | None, daylight: str
    ) -> Sighting | None:
        """The shore itself (package 33a: in thick weather a ship standing in sees the
        cliffs before any named mark, and a landfall in fog is made on them; package 37d:
        at every look, whatever headlands are in sight beside it). The nearest dry ground
        by the chart's own search (`Chart.nearest_shore`: its bearing true to the ground
        and not to the field's handful of directions), within `SHORE_CLOSE_NM`, the
        visibility, and at night `NIGHT_LAND_NM`. A sighting of the shore is land for
        the reading `the land`, and no mark to take a bearing of."""
        limit, bound = self._shore_limit(visibility_nm, daylight)
        self._shore_limit_nm, self._shore_bound = limit, bound
        shore = self.chart.nearest_shore(pos, within_m=limit * units.NAUTICAL_MILE)
        if shore is None:
            return None
        coast = self.chart.coast_at(pos, shore)
        name = f"the land about {coast.name}" if coast is not None and coast.name else "the land"
        land = Feature(SHORE_ID, "headland", name, pos.lat_deg, pos.lon_deg, height_m=0.0)
        return Sighting(land, shore.bearing_deg, shore.distance_m, "land")

    # -- land ahead (package 37d) --------------------------------------------------------

    def _land_ahead(
        self, world: Any, pos: Position, found: list[Sighting], heading: float
    ) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """The lookout's warning that she is standing into the land: a notable line when
        the first dry ground or danger in sight along her course made good would be
        reached in under `LAND_AHEAD_NOTABLE_MIN` minutes at her present speed over the
        ground, an urgent one under `LAND_AHEAD_URGENT_MIN`, each once an approach. Her
        course and speed are her true motion since the last look, a minute ago (the eye's
        judgement of a bearing that does not change and a distance that does); nothing at
        anchor, aground or without way, and nothing beyond what he can see of the
        shore."""
        tick = int(world.clock.tick)
        was = self._looked_from
        self._looked_from = (tick, pos.lat_deg, pos.lon_deg)
        hit: tuple[float, float, Sighting | None] | None = None
        speed = 0.0
        if was is not None and 0 < tick - was[0] <= LAND_AHEAD_LOOK_GAP_S and not _riding(world):
            dx, dy = Position(was[1], was[2]).offset_to(pos)
            speed = math.hypot(dx, dy) / float(tick - was[0])  # metres a second, made good
            if speed >= units.knots_to_ms(LAND_AHEAD_WAY_KN):
                course = math.atan2(dx, dy)
                reach = min(
                    self._shore_limit_nm * units.NAUTICAL_MILE,
                    speed * LAND_AHEAD_CLEAR_MIN * 60.0,
                )
                tide_m = float(getattr(world, "tide_height_m", 0.0))
                hit = self._first_ahead(pos, course, reach, tide_m, found)
        if hit is None:
            self._ahead_clear += 1
            if self._ahead_clear >= LAND_AHEAD_CLEAR_LOOKS:
                self._ahead_notable = self._ahead_urgent = False
            return []
        self._ahead_clear = 0
        distance_m, bearing_rad, danger = hit
        minutes = distance_m / speed / 60.0
        urgent = minutes < LAND_AHEAD_URGENT_MIN
        if urgent and not self._ahead_urgent:
            self._ahead_urgent = self._ahead_notable = True
        elif minutes < LAND_AHEAD_NOTABLE_MIN and not self._ahead_notable:
            self._ahead_notable = True
            urgent = False
        else:
            return []
        # by estimation, with the eye's error of the sighting it is (the danger's own,
        # the shore's for the land)
        ep = self._episodes.get(danger.feature.id if danger is not None else SHORE_ID)
        estimate_m = distance_m * (ep.factor if ep is not None else 1.0)
        estimate = estimate_words(estimate_m)
        relative = units.wrap_pi(bearing_rad - heading)
        where = ahead_words(relative)
        forward = units.rad_to_points(abs(relative)) < 6.0
        name = _head(danger.feature.name) if danger is not None else "Land"
        them = "them" if danger is not None and _plural(danger.feature.name) else "it"
        if urgent:
            if where == "right ahead":
                place = "close ahead"
            elif forward:
                place = f"close ahead, {where}"
            else:
                place = f"close {where}"
            soon = "within the minute" if minutes < 1.0 else f"in {_minutes_words(int(minutes))}"
            text = f"{name} {place}, {estimate}! She will be on {them} {soon}."
        else:
            if where == "right ahead":
                place = "right ahead"
            elif forward:
                place = f"ahead, {where}"
            else:
                place = where
            into = (
                "she is standing into danger"
                if danger is not None
                else ("she is standing into it" if forward else "she is setting down on it")
            )
            text = f"{name} {place}, {estimate}: {into}."
        data = {
            "what": "danger" if danger is not None else "land",
            "id": danger.feature.id if danger is not None else SHORE_ID,
            "name": danger.feature.name if danger is not None else "the land",
            "relative": where,
            "bearing": units.point_name(bearing_rad % units.TWO_PI),
            "estimate_m": round(estimate_m),
            "estimate": estimate,
            "minutes": round(minutes, 1),
            "urgent": urgent,
        }
        severity = Severity.URGENT if urgent else Severity.NOTABLE
        return [(severity, "lookout.land_ahead", text, data)]

    def _first_ahead(
        self, pos: Position, course: float, reach_m: float, tide_m: float, found: list[Sighting]
    ) -> tuple[float, float, Sighting | None] | None:
        """The nearest thing she is standing into within `reach_m`: (its distance in
        metres, its bearing in radians, the danger's sighting or None for the land). The
        charted dangers in sight within a point of her course, and the first dry ground
        at the tide's present height along her course and a point on either side. A
        danger is as near as its edge and as wide as it lies (its extent on the chart, a
        cable at the least, as the grounding takes it: a ship strikes a ledge's edge
        well before she is up with its mark)."""
        spread = units.points_to_rad(LAND_AHEAD_POINTS)
        best: tuple[float, float, Sighting | None] | None = None
        for s in found:
            if s.seen_as != "danger":
                continue
            extent = max(float(s.feature.extent_m), units.CABLE)
            edge = max(0.0, s.distance_m - extent)
            if edge > reach_m:
                continue
            bearing = math.radians(s.bearing_deg)
            wide = math.asin(min(1.0, extent / max(s.distance_m, extent)))
            if abs(units.wrap_pi(bearing - course)) <= spread + wide and (
                best is None or edge < best[0]
            ):
                best = (edge, bearing, s)
        dangers = [s for s in found if s.seen_as == "danger"]
        for off in (0.0, -spread, spread):
            within = reach_m if best is None else min(reach_m, best[0])
            d = self._dry_ground_along(pos, course + off, within, tide_m)
            if d is None or (best is not None and d >= best[0]):
                continue
            # the dry ground of a charted danger in sight (a rock that shows is ground
            # in the tiles too) is that danger, by its name
            bearing = course + off
            hit = pos.advanced(d * math.sin(bearing), d * math.cos(bearing))
            named = None
            for s in dangers:
                dx, dy = hit.offset_to(s.feature.position)
                if math.hypot(dx, dy) <= max(float(s.feature.extent_m), units.CABLE):
                    named = s
                    break
            best = (d, bearing, named)
        return best

    def _dry_ground_along(
        self, pos: Position, bearing: float, reach_m: float, tide_m: float
    ) -> float | None:
        """How far along a line from the ship the first dry ground lies at the tide's
        present height, within `reach_m`; None when the line is clear. The chart's
        distance field bounds each step (no shore can be nearer than it says), so a line
        over open water is a read or two and one along a shore a read every few yards."""
        chart = self.chart
        sin_b, cos_b = math.sin(bearing), math.cos(bearing)
        t = 0.0
        while t <= reach_m:
            p = pos.advanced(t * sin_b, t * cos_b)
            found = chart.coast_distance(p)
            if found is None:
                return None  # off the chart's field: nothing to be said of it
            if found[0] > LAND_AHEAD_MARGIN_M + LAND_AHEAD_STEP_M:
                t += found[0] - LAND_AHEAD_MARGIN_M
                continue
            depth = chart.depth_at(p)
            if depth is not None and depth + tide_m <= 0.0:
                return t
            t += LAND_AHEAD_STEP_M
        return None

    # -- the nearest land (package 37d) ---------------------------------------------------

    def nearest_land(self, heading_rad: float) -> dict[str, Any] | None:
        """`the nearest land`: the shore as the last look had it (where it lies from the
        ship's head, its bearing to the point, its distance by estimation in the
        lookout's own words, the coast's name where the chart has one), with the distance
        as said for the dialect to compare (`when the nearest land is under half a mile
        then ...`), never the chart's own metres; None when no shore is in sight
        (`no_nearest_land_words` says which: none within a league, or none seen within what
        the night or the weather allows)."""
        shore = next((s for s in self.sightings if s.feature.id == SHORE_ID), None)
        if shore is None:
            return None
        point = units.point_name(math.radians(shore.bearing_deg))
        relative = relative_words(math.radians(shore.bearing_deg) - heading_rad)
        estimate = estimate_words(shore.judged_m)
        return {
            "metres": _said_metres(shore.judged_m),
            "words": f"{shore.feature.name}, {relative}, bearing {point}, {estimate}",
            "name": shore.feature.name,
            "relative": relative,
            "bearing": point,
            "estimate": estimate,
        }

    def no_nearest_land_words(self) -> str:
        """Why `the nearest land` has nothing: no land within a league by day in clear
        weather; else none seen within what the night or the weather lets him see, and
        nothing to be told of what lies beyond it. Package 37l (the review of gate 5c's
        playtests, G2 and G5): the words were "not to be seen: in this weather the shore
        shows within a cable at most", which an officer read as land within a cable and
        hove to in mid-Channel; they now say first that none is seen."""
        if self._shore_bound in ("night", "weather"):
            reach = estimate_words(self._shore_limit_nm * units.NAUTICAL_MILE)
            when = "by night" if self._shore_bound == "night" else "in this weather"
            return (
                f"none seen within {reach}; {when} the shore shows no further off than that, "
                f"and land beyond it cannot be told"
            )
        return "no land within a league"

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
            close = (
                " close aboard" if s.judged_m < SHORE_CLOSE_ABOARD_NM * units.NAUTICAL_MILE else ""
            )
            return f"{head}{close} {relative}, bearing {point}, distant {distance}."
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
                named = [
                    s
                    for s in sails
                    if rig in _key(s.feature.name)
                    or rig in _key(self._sail_known.get(s.feature.id, ""))
                ]
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
        """`the land`: in sight or not, with the nearest land or light sighted: the
        nearest of the chart's own when one is in sight (a headland, a mark, a light, as
        it always was), the shore itself when it alone is; `the nearest land` is the
        shore's own reading (package 37d)."""
        # the land: the shore, its marks and its lights; a rock in sight is a danger, not land
        land = [s for s in self.sightings if s.seen_as in ("land", "light", "mark")]
        if not land:
            return {"in_sight": False, "words": "not in sight", "nearest": None}
        charted = [s for s in land if s.feature.id != SHORE_ID]
        nearest = min(charted or land, key=lambda s: s.distance_m)
        return {
            "in_sight": True,
            "words": "in sight",
            "nearest": nearest.to_dict() | {"words": self.words(nearest, heading_rad).rstrip(".")},
        }


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


def _ward(edges: list[str]) -> str:
    return " and the ".join(f"{e}ward" for e in edges)


def _riding(world: Any) -> bool:
    """At anchor, moored or aground: she is standing into nothing."""
    if getattr(world, "at_anchor", False):
        return True
    return bool((getattr(world.ship, "extra", None) or {}).get("aground"))


def _plural(name: str) -> bool:
    """'The Manacles' are 'them'; 'the Black Rock' is 'it'."""
    last = name.split()[-1].lower() if name.split() else ""
    return last.endswith("s") and not last.endswith("ss")


_MINUTES = ("no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


def _minutes_words(n: int) -> str:
    """'one minute', 'three minutes': the whole minutes left, said short of the time."""
    n = max(1, n)
    words = _MINUTES[n] if n < len(_MINUTES) else str(n)
    return f"{words} minute{'' if n == 1 else 's'}"


def _said_metres(estimate_m: float) -> float:
    """An estimate as the lookout says it, in metres: whole cables under a mile, whole
    miles under two leagues, whole leagues beyond (`geo.estimate_words`' own grain), for
    the dialect to compare what was said and not what was judged."""
    nm = estimate_m / units.NAUTICAL_MILE
    if nm < 0.95:
        return max(1, round(nm * 10.0)) * units.NAUTICAL_MILE / 10.0
    if nm < 6.0:
        return max(1, round(nm)) * units.NAUTICAL_MILE
    return max(2, round(nm / 3.0)) * 3.0 * units.NAUTICAL_MILE
