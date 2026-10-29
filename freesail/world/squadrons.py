"""The squadron as a genuine set (spec M7 §21 to §23; package 72;
`docs/design/Design-Squadrons.md`, written before this module).

A `Squadron` is a commander, the members in their order of sailing, one goal, a kind (a
squadron or a convoy, which decides whose book her signals are), a formation with its
interval, the divisions she is split into, her stragglers, her rendezvous and her book;
nothing more is fixed. Ships join her and leave her by the scenario file (`squadrons:`
beside `ships:`, or a ship's `squadron:` key), by the director's forms (`world/orders.py`,
the `squadron` channel), by her commander's signals and by the world (a straggler lost, a
prize taken: 74's hook). **Membership is the set's one truth**: `Vessel.squadron` is the
back-reference, and the set writes 71's least relation `under_orders_of` on every member
(her commander's id, her division's leader's while the division is detached), so that
every reader 71 built (the signal obeyed, the succession's rank, the challenge withheld
from a ship under his orders, the convoy book chosen) works unchanged, and a ship under
orders outside any set keeps the field as the scenario or the director set it.

**One brain moves the set at far detail.** The commander's own brain sails his intent;
each member's far body is on a `station` leg (`ships.Vessel.tick`), steered each minute
for her formation offset in the commander's frame (`Squadron.stations`: along his course
over the ground and across it, the across-axis positive to leeward by the wind at him),
going with him when within `STATION_TOLERANCE_M` and closing at her own pace when beyond;
the set's pace is the slowest member's (`pace_cap_kn`, a cap on the commander's far body).
A member more than the book's `straggler_nm` from her station for `straggler_minutes` is
a straggler; beyond `lost_nm` she is lost to the set and sails for the destination alone.
The whole costs arithmetic a minute a member, which is the brief's pace figure.

Nothing here is a line of the player's log but through the commander's own orders and
the lookout: a set is shown to the player by his own ship's membership (`the squadron`,
`the station`) and never as the world's object.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.events import Severity
from freesail.world.geo import Position, bearing_and_distance, distance_words
from freesail.world.ships import PLAYER_ID

__all__ = [
    "CONVOY_PACE_FACTOR",
    "FORMATIONS",
    "INTERVAL_M",
    "KINDS",
    "PLAYER_ID",
    "STATION_TOLERANCE_M",
    "Division",
    "Squadron",
    "Squadrons",
    "load_book",
    "plan_state_of",
]

SQUADRONS_DIR = Path(__file__).resolve().parents[2] / "data" / "squadrons"

# The player's ship as a commander or a member: `ships.PLAYER_ID`, the followed hull's
# vessel's id (package 84, step 7), imported above.

KINDS: tuple[str, ...] = ("squadron", "convoy")
FORMATIONS: tuple[str, ...] = ("line ahead", "line abreast", "order of sailing", "close order")

# The interval between ships in a line: two cables, the period's close order (the 1799
# book's instructions and the convoy instructions, "in close order, two cables apart", from
# memory); a convoy's columns the same apart.
INTERVAL_M = 2.0 * units.CABLE
# A member within this of her station is in it and goes with the commander: half a cable
# (judgement: a ship's length or two, the station keeping of a good officer).
STATION_TOLERANCE_M = 0.5 * units.CABLE
# The set's pace is the slowest member's best on the course, times this: the commodore
# keeps his convoy under the slowest ship's best so that she can keep up (judgement after
# the convoy instructions' "the convoy to sail at the rate of the dullest sailer").
CONVOY_PACE_FACTOR = 0.9
# A member astern of her station closes it at her own pace; one ahead of it drops back by
# so many knots under the commander's pace (sail shortened; judgement), never going astern.
DROP_BACK_KN = 1.5
# The book's defaults where a set has no book (judgement, said in each book file).
STRAGGLER_NM = 1.0
STRAGGLER_MINUTES = 10
LOST_NM = 6.0
SEPARATED_NM = 10.0

# The states of a member's machine that mean she is at her station (the plan states map
# to it: `plan_state_of`).
IN_COMPANY = "in company"
_PLAN_STATES = frozenset({"on passage", "beating", "keeping station"})


def plan_state_of(world: Any, vessel_id: str, state: str) -> str:
    """The state a member of a set enters where her doctrine would enter a plan state (on
    passage, beating, keeping station): `in company`, her station in the set. Any other
    state, and any state of a ship in no set or of a set's commander, is itself."""
    if state not in _PLAN_STATES:
        return state
    sets = getattr(world, "squadrons", None)
    if sets is None:
        return state
    sq = sets.of(vessel_id)
    if sq is None or sq.commander == vessel_id or sq.is_division_leader(vessel_id):
        return state
    return IN_COMPANY


# ---------------------------------------------------------------------------
# The books of the squadrons (data/squadrons/<kind>.yaml)
# ---------------------------------------------------------------------------

_BOOKS: dict[str, dict[str, Any]] = {}


def load_book(name: str) -> dict[str, Any]:
    """The squadron's book by its name (`data/squadrons/<name>.yaml`), read once; an empty
    book for a name no file has, so that a set made in a test stands on the defaults."""
    key = str(name or "").strip() or "squadron"
    if key in _BOOKS:
        return _BOOKS[key]
    path = SQUADRONS_DIR / f"{key}.yaml"
    raw: dict[str, Any] = {}
    if path.is_file():
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rules = []
    for rule in raw.get("rules") or []:
        if isinstance(rule, dict):
            # YAML 1.1 reads a bare `on:` as the boolean key True (as the doctrine loader
            # notes): the key is given its word again
            rule = {("on" if k is True else str(k)): v for k, v in rule.items()}
        rules.append(rule)
    raw["rules"] = rules
    _BOOKS[key] = raw
    return raw


def book_names() -> list[str]:
    return sorted(p.stem for p in SQUADRONS_DIR.glob("*.yaml")) if SQUADRONS_DIR.is_dir() else []


# ---------------------------------------------------------------------------
# The set
# ---------------------------------------------------------------------------


@dataclass
class Division:
    """A named subset of the set with a leader: detached (in chase, or inshore) her members
    keep their stations on the leader and read his signals; recalled, they are the set's
    again."""

    name: str
    leader: str
    members: list[str]
    since: int = 0
    detached: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "leader": self.leader,
            "members": list(self.members),
            "since": self.since,
            "detached": self.detached,
        }


@dataclass
class Squadron:
    id: str
    name: str
    kind: str = "squadron"
    nation: str = ""
    commander: str = PLAYER_ID
    members: list[str] = field(
        default_factory=list
    )  # the order of sailing, the commander among them
    goal: str = ""
    formation: str = "line ahead"
    interval_m: float = INTERVAL_M
    columns: int = 2
    divisions: dict[str, Division] = field(default_factory=dict)
    stragglers: dict[str, int] = field(default_factory=dict)  # id -> the tick she straggled
    rendezvous: str = ""
    book: str = ""
    regime: str = ""
    made: dict[str, int] = field(default_factory=dict)  # the book's rules fired, by key
    prizes: set[str] = field(default_factory=set)
    # the minute's work, kept for the readings and the tests: the stations computed and the
    # tick they were, each member's distance from her station
    _stations: dict[str, Position] = field(default_factory=dict)
    _stations_tick: int = -1
    off_station_m: dict[str, float] = field(default_factory=dict)
    off_since: dict[str, int] = field(default_factory=dict)
    history: list[tuple[int, str]] = field(default_factory=list)  # the set's own record

    # -- what the book says -----------------------------------------------------------

    def book_data(self) -> dict[str, Any]:
        return load_book(self.book or self.kind)

    def knob(self, key: str, default: Any = None) -> Any:
        raw = self.book_data().get(key)
        if isinstance(raw, dict) and "value" in raw:
            return raw["value"]
        return default if raw is None else raw

    @property
    def straggler_nm(self) -> float:
        return float(self.knob("straggler_nm", STRAGGLER_NM))

    @property
    def lost_nm(self) -> float:
        return float(self.knob("lost_nm", LOST_NM))

    @property
    def separated_nm(self) -> float:
        return float(self.knob("separated_nm", SEPARATED_NM))

    @property
    def pace_factor(self) -> float:
        return float(self.knob("pace_factor", CONVOY_PACE_FACTOR))

    # -- membership -------------------------------------------------------------------

    def has(self, vessel_id: str) -> bool:
        return str(vessel_id) in self.members

    def others(self) -> list[str]:
        """The members but the commander, in the order of sailing."""
        return [m for m in self.members if m != self.commander]

    def division_of(self, vessel_id: str) -> Division | None:
        for d in self.divisions.values():
            if vessel_id in d.members or vessel_id == d.leader:
                return d
        return None

    def is_division_leader(self, vessel_id: str) -> bool:
        d = self.division_of(vessel_id)
        return d is not None and d.detached and d.leader == vessel_id

    def leader_of(self, vessel_id: str) -> str:
        """Whose signals command this member: her detached division's leader, else the
        commander; the commander himself and a detached leader answer to the commander."""
        if vessel_id == self.commander:
            return ""
        d = self.division_of(vessel_id)
        if d is not None and d.detached and d.leader != vessel_id:
            return d.leader
        return self.commander

    def under(self, sender_id: str) -> list[str]:
        """The members under a sender's orders in the order of sailing: the whole set's
        others for the commander (a detached division's members answer to their leader
        and are left out), a detached division's members for its leader."""
        out = []
        for m in self.members:
            if m == sender_id:
                continue
            if self.leader_of(m) == sender_id:
                out.append(m)
        return out

    def join(
        self, world: Any, vessel_id: str, at: int | None = None, as_prize: bool = False
    ) -> None:
        """A ship joins the set at the end of the order (or at `at`), her far body put on
        the station leg; a prize joins in her captor's company (74's hook)."""
        vid = str(vessel_id)
        if vid not in self.members:
            if at is None or at < 0 or at > len(self.members):
                self.members.append(vid)
            else:
                self.members.insert(at, vid)
        if as_prize:
            self.prizes.add(vid)
        self._mark(world, vid)
        self._rewrite_orders(world)
        self._note(world, f"{self._name_of(world, vid)} joins {self.name}")

    def leave(self, world: Any, vessel_id: str, why: str = "") -> None:
        vid = str(vessel_id)
        if vid in self.members:
            self.members.remove(vid)
        for d in list(self.divisions.values()):
            if vid in d.members:
                d.members.remove(vid)
            if d.leader == vid or not d.members:
                del self.divisions[d.name]
        self.stragglers.pop(vid, None)
        self.prizes.discard(vid)
        self.off_station_m.pop(vid, None)
        self.off_since.pop(vid, None)
        self._stations.pop(vid, None)
        body = _body(world, vid)
        if body is not None:
            if getattr(body, "squadron", "") == self.id:
                body.squadron = ""
            if str(getattr(body, "under_orders_of", "") or "") in (self.commander, *self.members):
                body.under_orders_of = ""
            _drop_station_leg(body)
            crew = getattr(body, "crew", None)
            if crew is not None:
                crew.under_orders_of = ""
        if vid == self.commander and self.members:
            self.commander = self.members[0]
        self._rewrite_orders(world)
        self._note(
            world, f"{self._name_of(world, vid)} leaves {self.name}" + (f": {why}" if why else "")
        )

    def set_commander(self, world: Any, vessel_id: str) -> None:
        vid = str(vessel_id)
        if vid not in self.members:
            self.members.insert(0, vid)
        self.commander = vid
        self._mark(world, vid)
        self._rewrite_orders(world)
        self._note(world, f"{self._name_of(world, vid)} commands {self.name}")

    def detach(self, world: Any, name: str, leader: str, ids: list[str]) -> Division:
        """A division detached under a leader (in chase, or to the inshore station): its
        members keep their stations on him and read his signals; he reads the commander's."""
        lead = str(leader)
        members = [str(i) for i in ids if str(i) != lead and str(i) in self.members]
        if lead not in self.members:
            self.join(world, lead)
        for d in list(self.divisions.values()):
            for m in (lead, *members):
                if m in d.members:
                    d.members.remove(m)
            if d.leader in (lead, *members) or not d.members:
                del self.divisions[d.name]
        d = Division(str(name), lead, members, since=int(world.clock.tick), detached=True)
        self.divisions[d.name] = d
        self._rewrite_orders(world)
        self._note(world, f"the {d.name} division detached under {self._name_of(world, lead)}")
        return d

    def recall(self, world: Any, name: str) -> Division | None:
        d = self.divisions.pop(str(name), None)
        if d is None:
            return None
        d.detached = False
        self._rewrite_orders(world)
        self._note(world, f"the {d.name} division recalled")
        return d

    def split(self, world: Any, name: str, leader: str, ids: list[str]) -> Squadron:
        """A division made a set of its own, under its leader, with the set's book."""
        lead = str(leader)
        members = [lead] + [str(i) for i in ids if str(i) != lead and str(i) in self.members]
        for m in members:
            if m in self.members:
                self.members.remove(m)
            for d in list(self.divisions.values()):
                if m in d.members:
                    d.members.remove(m)
                if d.leader == m or not d.members:
                    self.divisions.pop(d.name, None)
        new = Squadron(
            id=f"{self.id}-{_slug(name)}",
            name=str(name),
            kind=self.kind,
            nation=self.nation,
            commander=lead,
            members=members,
            goal=self.goal,
            formation="line ahead",
            interval_m=self.interval_m,
            columns=self.columns,
            rendezvous=self.rendezvous,
            book=self.book,
            regime=self.regime,
        )
        sets = getattr(world, "squadrons", None)
        if sets is not None:
            sets.add(new, world)
        self._rewrite_orders(world)
        self._note(world, f"{new.name} parts company under {self._name_of(world, lead)}")
        return new

    def _mark(self, world: Any, vid: str) -> None:
        body = _body(world, vid)
        if body is None:
            return
        body.squadron = self.id

    def _rewrite_orders(self, world: Any) -> None:
        """The set writes 71's relation on every member: her leader's id (the commander,
        or her detached division's leader), the commander's own left as it was."""
        self._stations_tick = -1  # the formation changed: the stations are laid again
        for m in self.members:
            body = _body(world, m)
            if body is None:
                continue
            body.squadron = self.id
            boss = self.leader_of(m)
            if m == self.commander:
                continue
            body.under_orders_of = boss
            crew = getattr(body, "crew", None)
            if crew is not None:
                crew.under_orders_of = boss
            if getattr(body, "brain", None) is None and getattr(body, "crew", None) is None:
                _lay_station_leg(body, self)

    # -- the formation ----------------------------------------------------------------

    def slots(self, world: Any) -> dict[str, tuple[float, float]]:
        """Each member's slot in the formation as (along, across) metres in the guide's
        frame: along the course (negative astern), across positive to leeward. The
        members of a detached division are left out (their slots are on their leader,
        `_division_slots`)."""
        # a detached division's leader sails her own intent and has no slot; her members
        # keep their stations on her (`stations`)
        detached = {
            m for d in self.divisions.values() if d.detached for m in (d.leader, *d.members)
        }
        order = [m for m in self.members if m not in detached]
        interval = float(self.interval_m)
        out: dict[str, tuple[float, float]] = {}
        if self.formation == "line abreast":
            for i, m in enumerate(order):
                k = (i + 1) // 2
                sign = 1.0 if i % 2 else -1.0
                out[m] = (0.0, sign * k * interval)
            return out
        if self.formation in ("order of sailing", "close order") and self.kind == "convoy":
            close = self.formation == "close order"
            gap = interval * (0.5 if close else 1.0)
            escorts = [m for m in order if self._is_escort(world, m)]
            body = [m for m in order if m not in escorts]
            c = max(1, int(self.columns))
            rows = max(1, (len(body) + c - 1) // c)
            # the body to leeward of the escort by one interval, its columns about the
            # guide's across-axis; in close order about the commodore himself
            lee = 0.0 if close else gap
            for k, m in enumerate(body):
                row, col = divmod(k, c)
                out[m] = (-row * gap, lee + (col - (c - 1) / 2.0) * gap)
            mid = -((rows - 1) / 2.0) * gap
            for j, m in enumerate(escorts):
                if j == 0:
                    out[m] = (mid, 0.0 if close else -gap)  # the commodore to windward, abeam
                elif j == 1:
                    out[m] = (-rows * gap, lee)  # a second escort astern of the body
                else:
                    out[m] = (mid, lee + (c + 1) / 2.0 * gap)  # a third to leeward abeam
            return out
        # line ahead (the default; a squadron's close order is the line at half the interval)
        gap = interval * (0.5 if self.formation == "close order" else 1.0)
        for i, m in enumerate(order):
            out[m] = (-i * gap, 0.0)
        return out

    def _is_escort(self, world: Any, vid: str) -> bool:
        if vid == self.commander:
            return True
        body = _body(world, vid)
        if body is None:
            return False
        role = str(getattr(getattr(body, "brain", None), "role", "") or "")
        if role in ("kings-ship", "cruiser", "commodore"):
            return True
        return str(getattr(body, "description", "") or "") in ("frigate", "brig-sloop")

    def stations(self, world: Any) -> dict[str, Position]:
        """Every member's station point now, by the commander's frame (his position less
        his own slot the guide; his course over the ground when he has way, his last
        course when he has none; leeward by the wind at him); a detached division's
        members on their leader in line ahead. Cached for the minute."""
        tick = int(world.clock.tick)
        if self._stations_tick == tick and self._stations:
            return self._stations
        out: dict[str, Position] = {}
        guide = self._guide_frame(world)
        if guide is not None:
            pos, course, lee_sign = guide
            slots = self.slots(world)
            own = slots.get(self.commander, (0.0, 0.0))
            gx, gy = _rotate(own[0], own[1], course, lee_sign)
            guide_pos = pos.advanced(-gx, -gy)
            for m, (along, across) in slots.items():
                if m == self.commander:
                    continue
                dx, dy = _rotate(along, across, course, lee_sign)
                out[m] = guide_pos.advanced(dx, dy)
        for d in self.divisions.values():
            if not d.detached:
                continue
            frame = _frame_of(world, d.leader)
            if frame is None:
                continue
            pos, course, lee_sign = frame
            gap = float(self.interval_m)
            for i, m in enumerate(d.members, start=1):
                dx, dy = _rotate(-i * gap, 0.0, course, lee_sign)
                out[m] = pos.advanced(dx, dy)
        self._stations, self._stations_tick = out, tick
        return out

    def station_of(self, world: Any, vessel_id: str) -> Position | None:
        return self.stations(world).get(str(vessel_id))

    # the guide's dead reckoning while the commander is away: (position, course, tick)
    _guide_dr: tuple[Position, float, float, int] | None = None

    def _commander_on_detour(self, world: Any) -> bool:
        """The commander off his plan (chasing, investigating, engaging, evading): the
        convoy stands on by the guide's reckoning and does not follow him."""
        if self.commander == PLAYER_ID:
            cap = getattr(world, "captain", None)
            state = getattr(cap, "state", None) if cap is not None and cap.commands else None
        else:
            body = _body(world, self.commander)
            crew = getattr(body, "crew", None) if body is not None else None
            if crew is not None and getattr(crew, "shape", "full") == "full":
                state = getattr(getattr(crew, "captain", None), "state", None)
            else:
                state = getattr(getattr(body, "brain", None), "state", None)
        return state in ("chasing", "investigating a stranger", "engaging", "evading")

    def _guide_frame(self, world: Any) -> tuple[Position, float, float] | None:
        """The frame the stations are laid in: the commander's while he keeps his plan;
        while he is on a detour the guide stands on from where he left it, at the set's
        pace along his last course (the convoy does not chase with its escort), and he
        takes it up again where it has got to."""
        tick = int(world.clock.tick)
        if not self._commander_on_detour(world):
            self._guide_dr = None
            return _frame_of(world, self.commander)
        if self._guide_dr is None:
            frame = _frame_of(world, self.commander)
            if frame is None:
                return None
            pos, course, lee = frame
            body = _body(world, self.commander)
            kn = float(getattr(body, "speed_kn", 0.0) or 0.0) if body is not None else 0.0
            if body is not None and getattr(body, "pace_cap_kn", None) is not None:
                kn = min(kn, float(body.pace_cap_kn)) if kn > 0 else float(body.pace_cap_kn)
            self._guide_dr = (pos, course, max(kn, 2.0), tick)
            return pos, course, lee
        pos, course, kn, since = self._guide_dr
        step = units.knots_to_ms(kn) * float(tick - since)
        rad = math.radians(course)
        here = pos.advanced(step * math.sin(rad), step * math.cos(rad))
        self._guide_dr = (here, course, kn, tick)
        wind_from = _wind_from_at(world, here)
        rel = units.rad_to_deg(units.wrap_pi(math.radians(wind_from - course)))
        return here, course, (1.0 if rel <= 0.0 else -1.0)

    def guide_velocity(self, world: Any, vessel_id: str) -> tuple[float, float]:
        """The way over the ground (m/s east, north) of the ship this member keeps her
        station on: her division's leader when detached, else the commander."""
        boss = self.leader_of(str(vessel_id)) or self.commander
        return _velocity_of(world, boss)

    def pace_cap_kn(
        self, world: Any, course_deg: float, wind_from_deg: float, wind_kn: float
    ) -> float | None:
        """The set's pace: the slowest member's best on the course at the wind, times the
        book's factor; None when no member sails in company (the commander alone)."""
        best: float | None = None
        detached = {
            m for d in self.divisions.values() if d.detached for m in (d.leader, *d.members)
        }
        for m in self.others():
            if m in detached or m in self.prizes or m == PLAYER_ID:
                continue
            body = _body(world, m)
            if body is None or getattr(body, "done", False):
                continue
            plan = getattr(body, "plan", None) or []
            if not plan or plan[0][0] != "station":
                continue  # on a detour of her own: she does not set the pace
            kn = float(body.pace_kn(course_deg, wind_from_deg, wind_kn))
            if best is None or kn < best:
                best = kn
        if best is None:
            return None
        return max(units.ms_to_knots(0.25), best * self.pace_factor)

    # -- the minute -------------------------------------------------------------------

    def minute(self, world: Any) -> list[tuple[Any, ...]]:
        """Once a minute: the stations computed, each member's distance from hers, the
        stragglers counted and the lost let go, the commander's pace cap set. Returns the
        lines for the commander's log (the player's, when he commands)."""
        tick = int(world.clock.tick)
        lines: list[tuple[Any, ...]] = []
        stations = self.stations(world)
        strag_m = self.straggler_nm * units.NAUTICAL_MILE
        lost_m = self.lost_nm * units.NAUTICAL_MILE
        for m in list(self.others()):
            body = _body(world, m)
            at = stations.get(m)
            if body is None or at is None:
                continue
            if getattr(body, "done", False):
                self.leave(world, m, "gone")
                continue
            _, off = bearing_and_distance(body.position, at)
            self.off_station_m[m] = off
            on_detour = not _in_station_leg(body)
            if off > strag_m and not on_detour:
                since = self.off_since.setdefault(m, tick)
                if m not in self.stragglers and tick - since >= STRAGGLER_MINUTES * 60:
                    self.stragglers[m] = tick
                    lines.append(self._straggler_line(world, m, off))
                if off > lost_m and m not in self.prizes:
                    self._lost(world, m)
                    lines.append(self._lost_line(world, m))
                    continue
            elif off <= strag_m * 0.5:
                self.off_since.pop(m, None)
                if m in self.stragglers:
                    del self.stragglers[m]
                    lines.append(self._regained_line(world, m))
        self._cap_the_pace(world)
        lines.extend(self._released(world))
        self._read_commanders_signals(world)
        lines.extend(self._commanders_minute(world))
        return lines

    # -- the commander's signals, read on the set ---------------------------------------

    def _released(self, world: Any) -> list[tuple[Any, ...]]:
        """A member whose relation no longer names her leader was released by signal
        (71's `release`: part company, the convoy to disperse): she leaves the set."""
        lines: list[tuple[Any, ...]] = []
        for m in list(self.others()):
            body = _body(world, m)
            if body is None:
                continue
            if str(getattr(body, "under_orders_of", "") or "") != self.leader_of(m):
                self.leave(world, m, "released by signal")
                lines.append(
                    (
                        Severity.ROUTINE,
                        "squadron.parted",
                        f"{self._name_of(world, m)} has parted company with {self.name}.",
                        {"id": m, "squadron": self.id},
                    )
                )
        return lines

    def _read_commanders_signals(self, world: Any) -> None:
        """The commander's own hoists (made by his rule, by the player or by a model) are
        the command for the set: the formations formed, the ships pointed out to chase
        detached as a division under the first named, the chase discontinued recalling
        them. Each hoist read once."""
        locker = _locker_of(world, self.commander)
        if locker is None:
            return
        for h in list(getattr(locker, "made", ()) or ()):
            key = h.key
            if key in self.made:
                continue
            low = str(h.meaning or "").lower()
            if h.book not in ("numerary", "convoy", "night", "fog"):
                continue
            self.made[key] = int(world.clock.tick)
            if "order of sailing" in low:
                self.formation = "order of sailing"
                if "two columns" in low:
                    self.columns = 2
                self._note(world, "the order of sailing formed by signal")
            elif "line of battle ahead" in low or "line ahead" in low or "line of bearing" in low:
                self.formation = "line ahead"
                self._note(world, "the line ahead formed by signal")
            elif "abreast" in low:
                self.formation = "line abreast"
                self._note(world, "the line abreast formed by signal")
            elif (
                "closer order" in low or "close round the commodore" in low or "close order" in low
            ):
                self.formation = "close order"
                self._note(world, "close order by signal")
            elif "pointed out to chase" in low and h.to and h.to in self.members:
                if not self.is_division_leader(h.to) and h.to != self.commander:
                    self.detach(world, "chasing", h.to, [])
            elif "discontinue the chase" in low or "rejoin" in low:
                for name in list(self.divisions):
                    if name == "chasing":
                        self.recall(world, name)
            self._stations_tick = -1

    # -- the commander's minute: his book's rules -----------------------------------------

    def _commander(self, world: Any) -> tuple[Any, Any, str] | None:
        """(the captain-like, his perception, the body: 'far' | 'crewed' | 'player') of a
        rules commander; None when a model or the player holds the commander's station, or
        the director's hand holds him (then the signals are theirs)."""
        if self.commander == PLAYER_ID:
            cap = getattr(world, "captain", None)
            if cap is None or not getattr(cap, "commands", False):
                return None
            from freesail.world.captains import Perception

            return cap, Perception.read(world), "player"
        body = _body(world, self.commander)
        if body is None:
            return None
        crew = getattr(body, "crew", None)
        if crew is not None and getattr(crew, "shape", "full") == "full":
            cap = getattr(crew, "captain", None)
            if cap is None or not getattr(cap, "commands", False):
                return None
            from freesail.world.captains import Perception

            return cap, Perception.read(crew), "crewed"
        brain = getattr(body, "brain", None)
        if brain is None or getattr(brain, "over_head", None) is not None:
            return None
        from freesail.world.brains import perceive_vessel

        return brain, perceive_vessel(world, body, brain), "far"

    def _commanders_minute(self, world: Any) -> list[tuple[Any, ...]]:
        rules = self.book_data().get("rules") or []
        if not rules:
            return []
        found = self._commander(world)
        if found is None:
            return []
        cap, p, kind = found
        tick = int(world.clock.tick)
        percept = self._set_perception(world, cap, p)
        lines: list[tuple[Any, ...]] = []
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            key = str(rule.get("key") or rule.get("on") or "")
            if rule.get("near_only") and kind == "far":
                continue
            if rule.get("far_only") and kind != "far":
                continue
            fired = f"rule:{key}" in self.made
            if fired:
                rearm = rule.get("rearm")
                if rearm and self._stimulus(str(rearm), percept):
                    del self.made[f"rule:{key}"]
                    on_rearm = rule.get("on_rearm")
                    if isinstance(on_rearm, dict):
                        lines.extend(self._perform(world, on_rearm, cap, kind, percept))
                    continue
                repeat = rule.get("repeat_minutes")
                if (
                    repeat
                    and tick - int(self.made[f"rule:{key}"]) >= float(repeat) * 60.0
                    and self._stimulus(str(rule.get("on") or ""), percept)
                ):
                    # by steps while the stimulus holds (the commodore shortening sail
                    # again for a convoy still astern)
                    lines.extend(self._perform(world, rule, cap, kind, percept))
                    self.made[f"rule:{key}"] = tick
                continue
            if self._stimulus(str(rule.get("on") or ""), percept):
                done = self._perform(world, rule, cap, kind, percept)
                self.made[f"rule:{key}"] = tick
                lines.extend(done)
        return lines

    def _set_perception(self, world: Any, cap: Any, p: Any) -> dict[str, Any]:
        """What the set's rules judge by: the enemies the commander's people have made out
        (his own `_is_enemy`), the nearest enemy's distance to any member, a straggler
        threatened (an enemy within the book's cover distance of her), the light, the
        members astern of their stations, the commander's state."""
        enemies: list[tuple[str, float]] = []
        for s in getattr(p, "strangers", []) or []:
            sid = str(s.get("id") or "")
            if not sid or s.get("estimate_m") is None:
                continue
            try:
                hostile = bool(cap._is_enemy(s))
            except Exception:  # noqa: BLE001
                hostile = False
            if hostile:
                enemies.append((sid, float(s["estimate_m"])))
        close_nm = float(self.knob("convoy_close_nm", 4.0))
        cover_nm = float(self.knob("cover_nm", 2.0))
        nearest_nm = min((d for _, d in enemies), default=math.inf) / units.NAUTICAL_MILE
        threatened: list[tuple[str, str]] = []
        for sid, _ in enemies:
            enemy = _body(world, sid)
            if enemy is None:
                continue
            for m in self.stragglers:
                mb = _body(world, m)
                if mb is None:
                    continue
                _, d = bearing_and_distance(enemy.position, mb.position)
                if d <= cover_nm * units.NAUTICAL_MILE:
                    threatened.append((m, sid))
        tol = STATION_TOLERANCE_M
        astern = [
            m for m, off in self.off_station_m.items() if off > 3.0 * tol and self._behind(world, m)
        ]
        in_station = all(off <= 2.0 * tol for off in self.off_station_m.values())
        from freesail.world.signals import light_now

        state = str(getattr(cap, "state", "") or "")
        return {
            "enemies": enemies,
            "nearest_enemy_nm": nearest_nm,
            "enemy_in_sight": bool(enemies) and nearest_nm <= close_nm,
            "enemy_lost": not enemies or nearest_nm > close_nm * 1.5,
            "threatened": threatened,
            "astern": astern,
            "in_station": in_station and bool(self.off_station_m),
            "light": light_now(world),
            "state": state,
            "wind_kn": float(getattr(p, "wind_kn", 0.0) or 0.0),
            "wind_from": float(getattr(p, "wind_from_deg", 0.0) or 0.0),
            "in_port": bool(getattr(p, "in_port", "")),
            "stragglers": list(self.stragglers),
        }

    def _behind(self, world: Any, vid: str) -> bool:
        body = _body(world, vid)
        at = self._stations.get(vid)
        frame = self._guide_frame(world)
        if body is None or at is None or frame is None:
            return False
        bearing, _ = bearing_and_distance(at, body.position)
        rel = units.rad_to_deg(units.wrap_pi(math.radians(bearing - frame[1])))
        return abs(rel) > 90.0

    def _stimulus(self, name: str, percept: dict[str, Any]) -> bool:
        if name == "enemy in sight":
            return bool(percept["enemy_in_sight"])
        if name == "enemy lost":
            return bool(percept["enemy_lost"])
        if name == "straggler":
            return bool(percept["stragglers"])
        if name == "in station":
            return not percept["stragglers"]
        if name == "straggler threatened":
            return bool(percept["threatened"])
        if name == "member astern":
            return bool(percept["astern"])
        if name == "all in station":
            return bool(percept["in_station"])
        if name == "night":
            return percept["light"] == "night"
        if name == "day":
            return percept["light"] == "day"
        if name == "fog":
            return percept["light"] == "fog"
        if name == "clear":
            return percept["light"] != "fog"
        if name == "commander in port":
            return percept["state"] == "in port" or percept["in_port"]
        if name == "gale from the west":
            blown = self.book_data().get("blown_off") or {}
            kn = float(_val(blown.get("wind_kn"), 34.0))
            lo, hi = blown.get("from_deg") or [225.0, 315.0]
            frm = percept["wind_from"]
            return percept["wind_kn"] >= kn and float(lo) <= frm <= float(hi)
        if name == "gale over":
            blown = self.book_data().get("blown_off") or {}
            kn = float(_val(blown.get("wind_kn"), 34.0))
            return percept["wind_kn"] < kn - 6.0
        return False

    def _perform(
        self, world: Any, rule: dict[str, Any], cap: Any, kind: str, percept: dict[str, Any]
    ) -> list[tuple[Any, ...]]:
        lines: list[tuple[Any, ...]] = []
        tick = int(world.clock.tick)
        signal = rule.get("signal")
        if signal:
            to = None
            if rule.get("to") == "straggler" and percept["stragglers"]:
                to = percept["stragglers"][0]
            lines.extend(self._make_signal(world, cap, kind, str(signal), to))
        order = rule.get("order")
        if order:
            lines.extend(self._give(world, cap, kind, str(order), str(rule.get("why") or "")))
        formation = rule.get("formation")
        if formation in FORMATIONS:
            self.formation = str(formation)
            self._stations_tick = -1
            self._note(world, f"{self.formation} by the book")
        do = rule.get("do")
        if do == "cover" and percept["threatened"]:
            straggler, enemy = percept["threatened"][0]
            self._cover(world, cap, straggler, enemy)
        elif do == "recall":
            if str(getattr(cap, "state", "") or "") == "chasing" and cap._business.get("covering"):
                cap._business.pop("covering", None)
                try:
                    cap._enter("on passage")
                except Exception:  # noqa: BLE001
                    pass
        goal = rule.get("goal")
        if goal:
            lines.extend(self._set_goal(world, str(goal)))
        if rule.get("goal") == "restore" or do == "restore the goal":
            lines.extend(self._restore_goal(world))
        self._note(world, f"the book: {rule.get('key') or rule.get('on')} at {tick}")
        return lines

    def _make_signal(
        self, world: Any, cap: Any, kind: str, words: str, to: str | None
    ) -> list[tuple[Any, ...]]:
        from freesail.world import signals as S

        if kind != "far":
            try:
                cap.give(f"make the signal: {words}", why="the squadron's book")
            except Exception:  # noqa: BLE001 - refused in words (no hands, the book lacks it)
                pass
            return []
        body = _body(world, self.commander)
        if body is None:
            return []
        locker = S.vessel_locker(body)
        nations = getattr(world, "nations", None)
        books = S.books_for_nation(nations, str(body.nation))
        light = S.light_now(world)
        book = S.BOOKS_BY_LIGHT[light]
        found = None
        if self.kind == "convoy" and book == "numerary":
            found = books.find(words, "convoy")
        if found is None:
            found = books.find(words, book)
        if found is None and book == "numerary":
            found = books.find(words, "convoy")
        if found is None:
            return []
        entry, qualifiers = found
        h = S.make_hoist(
            locker, books, entry, qualifiers, str(body.id), int(world.clock.tick), to=to
        )
        _story(body, int(world.clock.tick), f"made the signal: {h.words()} (the book)")
        return []

    def _give(self, world: Any, cap: Any, kind: str, order: str, why: str) -> list[tuple[Any, ...]]:
        if kind == "far":
            from freesail.world.signals import far_perform

            body = _body(world, self.commander)
            if body is not None:
                done = far_perform(world, body, order)
                if done:
                    _story(body, int(world.clock.tick), f"by the book: {done}")
            return []
        try:
            cap.give(order, why=why or "the squadron's book")
        except Exception:  # noqa: BLE001
            pass
        return []

    def _cover(self, world: Any, cap: Any, straggler: str, enemy: str) -> None:
        """The escort covers a straggler: he chases the enemy that threatens her, and
        `covering` in his business brings him back when she is lost (`do: recall`)."""
        if str(getattr(cap, "state", "") or "") in ("chasing", "engaging"):
            return
        cap._stranger = enemy
        cap._business["covering"] = straggler
        try:
            cap._enter("chasing")
        except Exception:  # noqa: BLE001
            cap._business.pop("covering", None)
            return
        self._note(
            world,
            f"covering {self._name_of(world, straggler)} against {self._name_of(world, enemy)}",
        )

    def _set_goal(self, world: Any, words: str) -> list[tuple[Any, ...]]:
        """The set's goal changed by the book (the blockade blown off to its rendezvous):
        every leader's intent set, the old kept to be restored."""
        words = words.replace("{rendezvous}", self.rendezvous or self.destination_words(world))
        saved = self.made.setdefault("__goals__", {})  # type: ignore[arg-type]
        if not isinstance(saved, dict):
            saved = {}
            self.made["__goals__"] = saved  # type: ignore[assignment]
        leaders = [self.commander] + [d.leader for d in self.divisions.values() if d.detached]
        for lead in leaders:
            if lead == PLAYER_ID:
                cap = getattr(world, "captain", None)
                if cap is not None and getattr(cap, "commands", False):
                    saved.setdefault(lead, cap.intent_words)
                    try:
                        cap.set_intent(words)
                    except Exception:  # noqa: BLE001
                        pass
                continue
            body = _body(world, lead)
            brain = getattr(body, "brain", None) if body is not None else None
            if brain is None:
                continue
            saved.setdefault(lead, brain.intent_words)
            try:
                crew = getattr(body, "crew", None)
                if crew is not None and getattr(crew, "captain", None) is not None:
                    crew.captain.set_intent(words)
                brain.set_intent(words)
                brain._plan()
                brain.state = None
            except Exception:  # noqa: BLE001
                continue
        self._note(world, f"the goal by the book: {words}")
        return []

    def _restore_goal(self, world: Any) -> list[tuple[Any, ...]]:
        saved = self.made.pop("__goals__", None)  # type: ignore[arg-type]
        if not isinstance(saved, dict):
            return []
        for lead, words in saved.items():
            if not words:
                continue
            if lead == PLAYER_ID:
                cap = getattr(world, "captain", None)
                if cap is not None:
                    try:
                        cap.set_intent(words)
                    except Exception:  # noqa: BLE001
                        pass
                continue
            body = _body(world, lead)
            brain = getattr(body, "brain", None) if body is not None else None
            if brain is None:
                continue
            try:
                crew = getattr(body, "crew", None)
                if crew is not None and getattr(crew, "captain", None) is not None:
                    crew.captain.set_intent(words)
                brain.set_intent(words)
                brain._plan()
                brain.state = None
            except Exception:  # noqa: BLE001
                continue
        self._note(world, "the goal restored by the book")
        return []

    def _cap_the_pace(self, world: Any) -> None:
        body = _body(world, self.commander)
        if body is None or self.commander == PLAYER_ID:
            return
        plan = getattr(body, "plan", None) or []
        if not plan or plan[0][0] not in ("to", "home"):
            body.pace_cap_kn = None
            return
        wind_from, wind_ms = body._wind_at(world)
        wind_kn = units.ms_to_knots(wind_ms)
        body.pace_cap_kn = self.pace_cap_kn(world, float(body.heading_deg), wind_from, wind_kn)

    def _lost(self, world: Any, vid: str) -> None:
        """A straggler beyond `lost_nm` is lost to the set: she sails for the destination
        alone (her own brain's intent, or her goal's plan)."""
        body = _body(world, vid)
        dest = self.destination_words(world)
        self.leave(world, vid, "lost to the set, beyond the flags' reach")
        if body is None or not dest:
            return
        brain = getattr(body, "brain", None)
        try:
            if brain is not None:
                brain.set_intent(f"bound for {dest}")
                brain._plan()
                brain.state = None
            else:
                from freesail.world.ships import _goal_plan

                plan, cycle, goal = _goal_plan(world, f"bound for {dest}", body.position)
                body.plan, body.cycle, body.goal = plan, cycle, goal
                body.state = "on passage"
        except Exception:  # noqa: BLE001 - no way to lay it: she lies to, as a goal's end
            body.plan = [("lie_to", math.inf)]

    def destination_words(self, world: Any) -> str:
        """The set's destination in words: the rendezvous when one is given, else the
        goal's destination (a port's name, a feature's)."""
        if self.rendezvous:
            return self.rendezvous
        words = self.goal or ""
        if not words:
            return ""
        try:
            from freesail.world.captains import read_intent

            intent = read_intent(world, words)
        except Exception:  # noqa: BLE001
            return ""
        dest = intent.destination
        ports = getattr(world, "dealings", None)
        port = (getattr(ports, "ports", None) or {}).get(dest) if ports is not None else None
        if port is not None:
            return str(port.name)
        chart = getattr(world, "chart", None)
        f = chart.feature(dest) if chart is not None and dest else None
        return str(f.name) if f is not None else dest

    # -- words ------------------------------------------------------------------------

    def _name_of(self, world: Any, vid: str) -> str:
        body = _body(world, vid)
        return str(getattr(body, "name", vid) or vid)

    def _note(self, world: Any, words: str) -> None:
        self.history.append((int(world.clock.tick), words))
        if len(self.history) > 60:
            del self.history[:-60]

    def _straggler_line(self, world: Any, vid: str, off_m: float) -> tuple[Any, ...]:
        from freesail.core.events import Severity

        body = _body(world, vid)
        if body is not None:
            _story(body, int(world.clock.tick), "out of her station, a straggler")
        return (
            Severity.NOTABLE,
            "squadron.straggler",
            f"{self._name_of(world, vid)} is a straggler: {distance_words(off_m)} out of "
            f"her station in {self.name}.",
            {"id": vid, "squadron": self.id, "off_m": round(off_m)},
        )

    def _regained_line(self, world: Any, vid: str) -> tuple[Any, ...]:
        from freesail.core.events import Severity

        return (
            Severity.ROUTINE,
            "squadron.in_station",
            f"{self._name_of(world, vid)} has regained her station in {self.name}.",
            {"id": vid, "squadron": self.id},
        )

    def _lost_line(self, world: Any, vid: str) -> tuple[Any, ...]:
        from freesail.core.events import Severity

        return (
            Severity.NOTABLE,
            "squadron.lost",
            f"{self._name_of(world, vid)} is lost to {self.name}: beyond the flags' reach, she "
            f"proceeds alone.",
            {"id": vid, "squadron": self.id},
        )

    def words(self, world: Any) -> str:
        names = [self._name_of(world, m) for m in self.members]
        return (
            f"{self.name} ({self.kind}): {self._name_of(world, self.commander)} commanding; "
            f"{self.formation}, {distance_words(self.interval_m)} apart; " + ", ".join(names)
        )

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "nation": self.nation,
            "commander": self.commander,
            "members": list(self.members),
            "goal": self.goal,
            "formation": self.formation,
            "interval_m": round(self.interval_m),
            "columns": self.columns,
        }
        if self.divisions:
            d["divisions"] = [x.to_dict() for x in self.divisions.values()]
        if self.stragglers:
            d["stragglers"] = sorted(self.stragglers)
        if self.rendezvous:
            d["rendezvous"] = self.rendezvous
        if self.book:
            d["book"] = self.book
        if self.regime:
            d["regime"] = self.regime
        if self.prizes:
            d["prizes"] = sorted(self.prizes)
        return d

    @classmethod
    def from_spec(cls, world: Any, spec: dict[str, Any]) -> Squadron:
        """A set from a scenario's `squadrons:` entry or the director's form."""
        sid = _slug(str(spec.get("id") or spec.get("name") or "squadron"))
        kind = str(spec.get("kind") or "squadron").lower().strip()
        if kind not in KINDS:
            raise ValueError(
                f"'{spec.get('kind')}' is no kind of squadron; say squadron or convoy."
            )
        formation = str(
            spec.get("formation") or ("order of sailing" if kind == "convoy" else "line ahead")
        )
        formation = " ".join(formation.lower().split())
        if formation not in FORMATIONS:
            raise ValueError(
                f"'{spec.get('formation')}' is no formation; say one of {', '.join(FORMATIONS)}."
            )
        commander = str(spec.get("commander") or PLAYER_ID)
        if commander.lower() in ("the ship", "us", "the player", "the player's ship", "our ship"):
            commander = PLAYER_ID
        else:
            v = world.vessels.find(commander)
            if v is None:
                raise ValueError(
                    f"no ship named {commander!r} is on the sea to command "
                    f"{spec.get('name') or sid}"
                )
            commander = str(v.id)
        members: list[str] = []
        for m in spec.get("members") or []:
            m = str(m)
            if m.lower() in ("the ship", "us"):
                members.append(PLAYER_ID)
                continue
            v = world.vessels.find(m)
            if v is None:
                raise ValueError(
                    f"no ship named {m!r} is on the sea to join {spec.get('name') or sid}"
                )
            members.append(str(v.id))
        if commander not in members:
            members.insert(0, commander)
        interval = spec.get("interval_cables")
        nation = str(spec.get("nation") or "")
        if not nation:
            body = _body(world, commander)
            nation = str(
                getattr(body, "nation", "")
                or getattr(getattr(world, "dealings", None), "ship_nation", "")
                or ""
            )
        goal = str(spec.get("goal") or "")
        if not goal:
            body = _body(world, commander)
            goal = str(getattr(body, "intent_words", "") or "") if body is not None else ""
            if not goal and commander == PLAYER_ID:
                goal = str(getattr(getattr(world, "scenario", None), "intent", "") or "")
        return cls(
            id=sid,
            name=str(spec.get("name") or f"the {sid} {kind}"),
            kind=kind,
            nation=nation,
            commander=commander,
            members=members,
            goal=goal,
            formation=formation,
            interval_m=float(interval) * units.CABLE if interval is not None else INTERVAL_M,
            columns=int(spec.get("columns") or 2),
            rendezvous=str(spec.get("rendezvous") or ""),
            book=str(spec.get("book") or kind),
            regime=str(spec.get("regime") or ("in convoy" if kind == "convoy" else "")),
        )


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------


class Squadrons:
    """The sets of one World (`world.squadrons`), ticked once a minute from `Vessels.tick`
    after the brains have judged and before the bodies move."""

    def __init__(self, world: Any = None) -> None:
        self.world = world
        self.sets: list[Squadron] = []
        self.serial = 0

    def add(self, sq: Squadron, world: Any = None) -> Squadron:
        world = world or self.world
        if any(s.id == sq.id for s in self.sets):
            raise ValueError(f"a squadron '{sq.id}' is on the sea already")
        self.sets.append(sq)
        self.serial += 1
        for m in sq.members:
            sq._mark(world, m)
        sq._rewrite_orders(world)
        for m in sq.others():
            body = _body(world, m)
            brain = getattr(body, "brain", None) if body is not None else None
            if brain is not None and brain.state in _PLAN_STATES:
                brain.state = None  # her next judgement enters `in company`
            elif body is not None and brain is None and getattr(body, "crew", None) is None:
                _lay_station_leg(body, sq)
        sq._note(world, f"{sq.name} formed: {sq.words(world)}")
        return sq

    def remove(self, sq: Squadron, world: Any = None) -> None:
        world = world or self.world
        for m in list(sq.members):
            sq.leave(world, m, "the set dissolved")
        self.sets = [s for s in self.sets if s is not sq]

    def of(self, vessel_id: str) -> Squadron | None:
        vid = str(vessel_id)
        for s in self.sets:
            if vid in s.members:
                return s
        return None

    def commanded_by(self, vessel_id: str) -> Squadron | None:
        vid = str(vessel_id)
        for s in self.sets:
            if s.commander == vid:
                return s
        return None

    def find(self, words: str) -> Squadron | None:
        key = " ".join(str(words).lower().split()).strip(" .'\"").removeprefix("the ")
        for s in self.sets:
            if key in (s.id.lower(), s.name.lower(), s.name.lower().removeprefix("the ")):
                return s
        for s in self.sets:
            if key in s.name.lower():
                return s
        return None

    def tick(self, world: Any) -> list[tuple[Any, ...]]:
        lines: list[tuple[Any, ...]] = []
        for s in list(self.sets):
            if not s.others():
                continue
            lines.extend(s.minute(world))
        lines.extend(far_captures(world))
        return lines

    def to_dict(self) -> list[dict[str, Any]]:
        return [s.to_dict() for s in self.sets]


def sets_from_scenario(world: Any) -> None:
    """The scenario's sets (`squadrons:` beside `ships:`, each a spec `Squadron.from_spec`
    reads; and the short form, a ship's `squadron: <id>` key, which adds her to the set of
    that id, made with the defaults under the player's command when `squadrons:` has no
    entry for it). Called once when the World is made, after the ships."""
    sc = getattr(world, "scenario", None)
    sets = getattr(world, "squadrons", None)
    if sc is None or sets is None:
        return
    specs = [dict(s) for s in (getattr(sc, "squadrons", None) or [])]
    by_id = {_slug(str(s.get("id") or s.get("name") or "squadron")): s for s in specs}
    short: dict[str, list[str]] = {}
    for ship in getattr(sc, "ships", None) or []:
        key = ship.get("squadron")
        if key:
            short.setdefault(_slug(str(key)), []).append(
                str(ship.get("id") or ship.get("name") or "")
            )
    for sid, ids in short.items():
        spec = by_id.setdefault(sid, {"id": sid})
        members = [str(m) for m in (spec.get("members") or [])]
        for vid in ids:
            if vid and vid not in members:
                members.append(vid)
        spec["members"] = members
        if not spec.get("kind"):
            descs = [
                str(getattr(world.vessels.find(m), "description", "") or "")
                for m in members
                if world.vessels.find(m) is not None
            ]
            spec["kind"] = "convoy" if any("merchant" in d for d in descs) else "squadron"
    for spec in by_id.values():
        sq = Squadron.from_spec(world, spec)
        sets.add(sq, world)


# ---------------------------------------------------------------------------
# The frame, the bodies and the station leg
# ---------------------------------------------------------------------------


def _slug(words: str) -> str:
    return (
        "-".join("".join(ch if ch.isalnum() else " " for ch in words.lower()).split()) or "squadron"
    )


def _body(world: Any, vid: str) -> Any:
    """A member's body on the sea: a vessel of it, the player's ship among them (package 84,
    step 7: `Vessels.own`, under `PLAYER_ID`)."""
    sea = getattr(world, "vessels", None)
    return sea.get(vid) if sea is not None else None


def _followed_hull(body: Any) -> Any:
    """The followed hull when `body` is her vessel (package 84, step 7), else None: her way
    and her frame are her ship's own, as the shadow's were, where another hull's are her
    far body's mirrored record."""
    hull = getattr(body, "crew", None) if body is not None else None
    return hull if hull is not None and getattr(hull, "is_followed", False) else None


def _velocity_of(world: Any, vid: str) -> tuple[float, float]:
    body = _body(world, vid)
    hull = _followed_hull(body)
    if hull is not None:
        from freesail.world.ships import _ship_velocity

        return _ship_velocity(hull)
    if body is None:
        return 0.0, 0.0
    ms = units.knots_to_ms(float(body.speed_kn))
    rad = math.radians(float(body.heading_deg))
    return ms * math.sin(rad), ms * math.cos(rad)


_LAST_COURSE: dict[str, float] = {}


def _frame_of(world: Any, vid: str) -> tuple[Position, float, float] | None:
    """(the position, the course over the ground in degrees, the sign that turns 'across
    to leeward' into a bearing offset) of the ship a station is kept on. Her course is her
    heading when she has way and her last course when she has none, so that a stopped
    commodore's drift does not swing the set (71's finding)."""
    hull = _followed_hull(_body(world, vid))
    if hull is not None:
        pos = getattr(hull, "position", None)
        ship = getattr(hull, "ship", None)
        if pos is None or ship is None:
            return None
        heading = units.rad_to_deg(float(ship.heading)) % 360.0
        east, north = _velocity_of(world, vid)
        way = math.hypot(east, north)
        key = f"{id(world)}:{vid}"
    else:
        body = _body(world, vid)
        if body is None:
            return None
        pos = body.position
        heading = float(body.heading_deg) % 360.0
        way = units.knots_to_ms(float(body.speed_kn))
        key = f"{id(world)}:{vid}"
    if way > 0.3:
        course = heading
        _LAST_COURSE[key] = course
    else:
        course = _LAST_COURSE.get(key, heading)
    wind_from = _wind_from_at(world, pos)
    rel = units.rad_to_deg(units.wrap_pi(math.radians(wind_from - course)))
    # the wind from the larboard side (rel < 0): leeward is to starboard (+90°)
    lee_sign = 1.0 if rel <= 0.0 else -1.0
    return pos, course, lee_sign


def _wind_from_at(world: Any, pos: Position) -> float:
    systems = getattr(world, "systems", None)
    if (
        systems is not None
        and getattr(world, "weather", None) is None
        and getattr(world, "origin", None)
    ):
        plane = world.plane_of(pos) if hasattr(world, "plane_of") else None
        if plane is not None:
            direction, _ = systems.surface_wind_at(plane[0] / 1000.0, plane[1] / 1000.0)
            return math.degrees(direction) % 360.0
    wind = getattr(world, "wind", None)
    return math.degrees(float(wind.base_direction)) % 360.0 if wind is not None else 0.0


def _rotate(along: float, across: float, course_deg: float, lee_sign: float) -> tuple[float, float]:
    """A slot in the guide's frame into east and north metres."""
    c = math.radians(course_deg)
    ax, ay = math.sin(c), math.cos(c)  # along the course
    px, py = lee_sign * math.cos(c), -lee_sign * math.sin(c)  # across, positive to leeward
    return along * ax + across * px, along * ay + across * py


def _in_station_leg(body: Any) -> bool:
    plan = getattr(body, "plan", None) or []
    return bool(plan) and plan[0][0] == "station"


def _lay_station_leg(body: Any, sq: Squadron) -> None:
    body.plan = [("station", sq.id)]
    body.cycle = False
    body.saved_plan = None
    body.tack = 0.0
    body.lying_to_s = 0.0
    if getattr(body, "state", "") in _PLAN_STATES or not getattr(body, "state", ""):
        body.state = IN_COMPANY


def _drop_station_leg(body: Any) -> None:
    plan = getattr(body, "plan", None) or []
    if plan and plan[0][0] == "station":
        body.plan = [leg for leg in plan if leg[0] != "station"]
    if getattr(body, "state", "") == IN_COMPANY:
        body.state = "on passage"


def _story(vessel: Any, tick: int, words: str) -> None:
    story = list(getattr(vessel, "story", ()) or ())
    story.append((tick, words))
    vessel.story = tuple(story[-30:])


def _val(raw: Any, default: Any) -> Any:
    if isinstance(raw, dict) and "value" in raw:
        return raw["value"]
    return default if raw is None else raw


def _locker_of(world: Any, vid: str) -> Any:
    from freesail.world import signals as S

    body = _body(world, vid)
    return S.vessel_locker(body) if body is not None else None


# The straggler cut out at far detail (rule 5's least; docs/design/Design-Squadrons.md):
# a ship whose doctrine yields when caught, brought to within hail by an armed enemy who
# has her for his chase (the far chase comes to at hailing distance, where the privateer
# hailed her to strike), with no friendly man of war within the cover distance, strikes by
# rule and joins her captor's company. The figures are judgements after the prize courts'
# Channel record (a merchantman brought to by a privateer alongside struck without a fight
# more often than not); 74 replaces the rule with `combat/far.py`'s rounds for the ships
# that fight. The design note said pistol shot; the far chase never comes nearer than hail.
CUT_OUT_M = 0.4 * units.NAUTICAL_MILE
COVER_NM = 2.0
_ARMED_ROLES = frozenset({"privateer", "cruiser", "kings-ship", "commodore"})
_MAN_OF_WAR_DESCRIPTIONS = frozenset({"frigate", "brig-sloop"})


def _yields(body: Any) -> bool:
    brain = getattr(body, "brain", None)
    d = getattr(brain, "doctrine", None) if brain is not None else None
    if d is not None:
        return bool(d.threshold("yields_when_caught", False))
    return "merchant" in str(getattr(body, "description", "") or "")


def _armed_enemy_alongside(world: Any, prey: Any) -> Any:
    nations = getattr(world, "nations", None)
    if nations is None:
        return None
    for o in world.vessels.vessels:
        if o is prey or getattr(o, "done", False) or getattr(o, "struck", False):
            continue
        brain = getattr(o, "brain", None)
        if brain is None or brain.state not in ("chasing", "engaging", "investigating a stranger"):
            continue
        if str(getattr(brain, "_stranger", "") or "") != str(prey.id):
            continue
        if getattr(brain, "role", "") not in _ARMED_ROLES:
            continue
        if not nations.at_war(str(o.nation), str(prey.nation)):
            continue
        if getattr(o, "crew", None) is not None and o.crew.shape == "full":
            continue  # the near fight is 70's
        _, d = bearing_and_distance(o.position, prey.position)
        if d <= CUT_OUT_M:
            return o
    return None


def _covered(world: Any, prey: Any) -> bool:
    for o in world.vessels.vessels:
        if o is prey or getattr(o, "done", False) or str(o.nation) != str(prey.nation):
            continue
        brain = getattr(o, "brain", None)
        role = getattr(brain, "role", "") if brain is not None else ""
        if (
            role not in _ARMED_ROLES
            and str(getattr(o, "description", "")) not in _MAN_OF_WAR_DESCRIPTIONS
        ):
            continue
        _, d = bearing_and_distance(o.position, prey.position)
        if d <= COVER_NM * units.NAUTICAL_MILE:
            return True
    shadow_pos = getattr(world, "position", None)
    ports = getattr(world, "dealings", None)
    own_nation = getattr(ports, "ship_nation", None) if ports is not None else None
    if shadow_pos is not None and own_nation == str(prey.nation):
        _, d = bearing_and_distance(shadow_pos, prey.position)
        from freesail.world.captains import _is_kings_ship

        if d <= COVER_NM * units.NAUTICAL_MILE and _is_kings_ship(world):
            return True
    return False


def far_captures(world: Any) -> list[tuple[Any, ...]]:
    """Once a minute: every far ship that yields when caught, brought to by an armed enemy
    with no cover, strikes and joins her captor's company."""
    lines: list[tuple[Any, ...]] = []
    sea = getattr(world, "vessels", None)
    sets = getattr(world, "squadrons", None)
    if sea is None or sets is None:
        return lines
    tick = int(world.clock.tick)
    for prey in list(sea.vessels):
        if getattr(prey, "done", False) or getattr(prey, "struck", False) or not _yields(prey):
            continue
        if getattr(prey, "crew", None) is not None and prey.crew.shape == "full":
            continue
        captor = _armed_enemy_alongside(world, prey)
        if captor is None or _covered(world, prey):
            continue
        from freesail.world import signals as S

        prey.struck = True
        S.set_colours(
            S.vessel_locker(prey).colours, getattr(world, "nations", None), "struck", "", tick
        )
        prey.state = "struck"
        prey.plan = [("lie_to", math.inf)]
        prey.saved_plan = None
        brain = getattr(prey, "brain", None)
        if brain is not None:
            brain.state = "struck"
            brain.history.append((tick, "struck"))
        old = sets.of(prey.id)
        if old is not None:
            old.leave(world, prey.id, f"cut out by {captor.name}")
        company = sets.commanded_by(captor.id)
        if company is None:
            company = Squadron(
                id=f"{captor.id}-company",
                name=f"{captor.name}'s company",
                kind="squadron",
                nation=str(captor.nation),
                commander=str(captor.id),
                members=[str(captor.id)],
                goal=str(getattr(captor, "intent_words", "") or ""),
                formation="line ahead",
            )
            sets.add(company, world)
        company.join(world, prey.id, as_prize=True)
        _story(prey, tick, f"brought to by {captor.name} alongside, no help in sight: struck")
        _story(captor, tick, f"{prey.name} struck to us alongside: a prize, in company")
        lines.append(
            (
                Severity.NOTABLE,
                "squadron.cut_out",
                f"{prey.name} is cut out: brought to by {captor.name} with no help near, she "
                "strikes and is carried off in company.",
                {"id": prey.id, "captor": captor.id},
            )
        )
    return lines


def keep_station(vessel: Any, world: Any, dt: float, wind_from: float, wind_kn: float) -> None:
    """The `station` leg of a member's far body (`Vessel.tick`): within the tolerance she
    goes with the guide's way on his course; astern of her station she steers for it under
    her polar's course rule at her own pace; ahead of it she drops back under his pace on
    his course until it comes up to her; separated beyond the book's distance she steers
    for the rendezvous when the set has one. A ship in no set drops the leg."""
    sets = getattr(world, "squadrons", None)
    sq = sets.of(vessel.id) if sets is not None else None
    if sq is None or vessel.id == sq.commander:
        _drop_station_leg(vessel)
        return
    at = sq.station_of(world, vessel.id)
    if at is None:
        # the guide is gone (the commander lost to the sea): hold her course
        vessel.speed_kn = vessel.pace_kn(vessel.heading_deg, wind_from, wind_kn)
        step = units.knots_to_ms(vessel.speed_kn) * dt
        rad = math.radians(vessel.heading_deg)
        vessel.position = vessel.position.advanced(step * math.sin(rad), step * math.cos(rad))
        vessel.distance_run_m += step
        return
    east, north = sq.guide_velocity(world, vessel.id)
    guide_ms = math.hypot(east, north)
    guide_course = (
        math.degrees(math.atan2(east, north)) % 360.0 if guide_ms > 0.05 else vessel.heading_deg
    )
    bearing, distance = bearing_and_distance(vessel.position, at)
    if distance <= STATION_TOLERANCE_M:
        vessel.position = vessel.position.advanced(east * dt, north * dt)
        vessel.speed_kn = units.ms_to_knots(guide_ms)
        if guide_ms > 0.05:
            vessel.heading_deg = guide_course
        vessel.distance_run_m += guide_ms * dt
        vessel.tack = 0.0
        vessel._stream(world, dt)
        return
    if distance > sq.separated_nm * units.NAUTICAL_MILE and sq.rendezvous:
        from freesail.world.ships import place_position

        found = place_position(world, sq.rendezvous)
        if found is not None:
            bearing, distance = bearing_and_distance(vessel.position, found[0])
    # ahead of the station (it bears abaft her beam, by the guide's course): drop back on
    # his course under his pace, sail shortened; astern: the best she can make toward it
    rel = abs(units.rad_to_deg(units.wrap_pi(math.radians(bearing - guide_course))))
    if rel > 100.0 and guide_ms > 0.05 and distance < 2.0 * units.NAUTICAL_MILE:
        course = guide_course
        speed_kn = max(0.0, units.ms_to_knots(guide_ms) - DROP_BACK_KN)
    else:
        course = vessel._course_for(bearing, wind_from, wind_kn)
        speed_kn = vessel.pace_kn(course, wind_from, wind_kn)
    vessel.heading_deg = course
    vessel.speed_kn = speed_kn
    step = units.knots_to_ms(speed_kn) * dt
    if course == bearing and step > distance:
        step = distance
    rad = math.radians(course)
    vessel.position = vessel.position.advanced(step * math.sin(rad), step * math.cos(rad))
    vessel.distance_run_m += step
    vessel._stream(world, dt)
