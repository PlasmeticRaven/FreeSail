"""The brain on the far body (package 43; spec M6 §4 "one brain, two bodies", §19).

A far-detail vessel of `freesail.world.ships` whose scenario entry or world order gives her
an `intent:` carries a rules-based captain of her own, `FarCaptain`: the same doctrine and
the same judgement as the player's `captains.Captain` (`captains.Judgement`, the stimuli
and the trend shared), on a perception built from **her own truth** once a minute at the
roll-up's cadence (`perceive_vessel`: her position, the wind at her, the player's visibility
and the daylight, the nearest land and the land to leeward by the chart from where she
is, her anchor, the port she lies off, and the ships in sight from her masthead by the
horizon, the player's ship among them under `PLAYER_ID`, each made out at the lookout's
distances), and every state of the machine resolved into a plan of the far body
(`resolve_state`) instead of a book. This module reads the truth, since the far body is
the truth: it lives apart from `captains.py`, whose proof (`tests/test_captains.py`) is
that the player's captain reads none. Nothing of a far captain's mind is a line of the
player's log: he keeps his own history of states (`FarCaptain.history`), which the tests
and the tuning notes read as they read the truth, and the player's lookout sees only
what the ship does. Across the crewed promotion (`crews.py`) his state is folded into the
near body's `Captain` and back (`fold_in`, `fold_back`).
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.world.captains import (
    FREE,
    IN_PORT_NM,
    JUDGE_EVERY_S,
    SIZE_RANK,
    STATES,
    Captain,
    Doctrine,
    Intent,
    Judgement,
    Leg,
    Perception,
    Planner,
    _lee_land_nm,
    _mark,
    load_doctrine,
    read_intent,
    station_off,
)
from freesail.world.geo import Position, bearing_and_distance, destination
from freesail.world.ships import PLAYER_ID

__all__ = [
    "AT_ANCHOR_LEAST_S",
    "FAR_DETAIL_STATES",
    "HAIL_REACH_M",
    "IN_PORT_WAIT_S",
    "PLAYER_ID",
    "FarCaptain",
    "perceive_vessel",
    "resolve_state",
    "role_of_vessel",
]

# The far-detail brain's figures (package 43; spec M6 §4 and §19). A vessel whose scenario
# entry or world order gives her an `intent:` carries a rules-based captain of her own, who
# judges once a minute at the roll-up's cadence from a perception built of her own truth
# (`perceive_vessel`: her position, the wind at her, the nearest land and the sea room
# by the chart, the ships in sight by the horizon and the player's visibility, the player's
# ship among them, her nation's stance to each), runs the doctrine of her role on it and
# resolves each state into a plan of the far body. What is in her mind is never a line of
# the player's log: the brain keeps its own history of states (`FarCaptain.history`), which
# the tests and the tuning notes read as they read the truth, and the player's lookout sees
# only what she does. Her business in port is a wait (`IN_PORT_WAIT_S`: a tide and a day's
# dealing, judgement; the small economy is 43b's), her anchorage in shelter is kept until
# the weather clears by day and `AT_ANCHOR_LEAST_S` has passed (judgement: an hour, so that
# a clearing of a minute does not weigh her). The player's ship is a sail to her under the
# id `PLAYER_ID`, her colours taken as shown (a King's ship wears them; a merchantman
# shows them when asked, and nothing of the player's models his colours yet).
IN_PORT_WAIT_S = 12 * 3600
AT_ANCHOR_LEAST_S = 3600
# The states the far-detail body resolves without a brain (spec M6 §4; package 40): on
# passage is her plan, hove to is no way. A vessel with a brain resolves every state.
FAR_DETAIL_STATES: tuple[str, ...] = ("on passage", "hove to for weather", "in company")


def perceive_vessel(world: Any, vessel: Any, brain: Any = None) -> Perception:
    """The perception of a far-detail vessel's captain, built from her own truth at
    the roll-up's cadence (package 43; spec M6 §4: "at far detail that is pairwise
    distance and visibility"): her position, the wind at her, the player's visibility
    and the daylight, the nearest land and the land to leeward by the chart from where
    she is, her anchor, the port she lies off, and the ships in sight from her masthead
    by the horizon (`Vessels.strangers_of`: the player's ship among them, each made out
    at the lookout's distances, her colours when she shows them). No almanac, no glass:
    the tide serves her, and her trend is the wind's."""
    p = Perception(tick=world.clock.tick, now=world.clock.ship_time)
    p.own_size = SIZE_RANK.get(str(getattr(vessel, "description", "") or ""), 0)
    wind_from, wind_ms = vessel._wind_at(world)
    p.wind_kn = units.ms_to_knots(float(wind_ms))
    p.wind_from_deg = float(wind_from) % 360.0
    p.heading_deg = float(vessel.heading_deg) % 360.0
    p.speed_kn = float(vessel.speed_kn)
    conditions = getattr(world, "conditions", None)
    if conditions is not None:
        p.visibility = str(conditions.visibility)
        p.visibility_nm = float(conditions.visibility_nm)
    p.daylight = str(world.daylight)
    chart = getattr(world, "chart", None)
    here = vessel.position
    if chart is not None:
        try:
            found = chart.coast_distance(here)
        except Exception:  # noqa: BLE001 - beyond the chart's field
            found = None
        if found is not None:
            metres, toward = found
            nm = float(metres) / units.NAUTICAL_MILE
            p.coast_by_account_nm = nm
            p.coast_by_account_bearing_deg = float(toward)
            # the land the lookout would give: within the shore's reach by day, and
            # within the visibility; else the chart alone speaks for it
            limit = 3.0 if p.daylight == "day" else 1.0
            if p.visibility_nm is not None:
                limit = min(limit, p.visibility_nm)
            if nm <= limit:
                p.nearest_land_nm = nm
                p.nearest_land_bearing = units.point_name(math.radians(float(toward)))
                p.land_in_sight = True
        p.lee_land_nm = _lee_land_nm(world, p, here=here)
    plan = getattr(vessel, "plan", None) or []
    p.anchor_down = bool(plan) and plan[0][0] == "anchor"
    ports = getattr(world, "ports", None)
    if ports is not None and getattr(ports, "ports", None):
        best = None
        for port in ports.ports.values():
            _, d = bearing_and_distance(here, port.outer_road.position)
            d_nm = d / units.NAUTICAL_MILE
            if best is None or d_nm < best[1]:
                best = (port, d_nm)
        if best is not None:
            p.port_distance_nm = best[1]
            p.reach_nm = float(getattr(best[0], "reach_nm", IN_PORT_NM))
            if p.anchor_down and best[1] <= p.reach_nm:
                p.in_port = best[0].id
    spoken = brain.spoken_ids if brain is not None else set()
    glass_for = brain._stranger if brain is not None else None
    p.strangers = world.vessels.strangers_of(world, vessel, spoken, glass_for)
    return p


# ---------------------------------------------------------------------------
# The far-detail body: the brain on it (package 43; spec M6 §4, §19)
# ---------------------------------------------------------------------------


def role_of_vessel(vessel: Any, intent: Intent | None) -> str:
    """The doctrine a far-detail vessel's captain sails by, by her description and her
    intent (package 43: "a doctrine by nation and role"): a frigate is a King's ship; a
    brig-sloop is a cruiser, and so is a cutter on a station; a letter or the mail is the
    packet's; a merchant brig, a schooner or a cutter in trade is the merchant's. A role
    her scenario gave her (`Vessel.role`, package 75) comes first, whatever the rest say;
    the sixty-four, the razee and the seventy-four are King's ships as the frigate is."""
    own = str(getattr(vessel, "role", "") or "")
    if own:
        return own  # package 75 (docs/design/Build-Ships.md §8.1): her scenario's `role:`
    key = str(getattr(vessel, "description", "") or "")
    kind = intent.kind if intent is not None else ""
    if kind == "fish":
        return "fisherman"  # package 43b: the smack and the lugger on a ground
    if kind == "letter":
        return "packet"
    if kind == "station" and intent is not None and getattr(intent, "prizes", False):
        return "privateer"  # package 70: a letter of marque cruising for prizes
    if intent is not None and getattr(intent, "convoy", False):
        # package 72 (found on the way): a far escort given `convoy the trade from A to B`
        # sailed by the cruiser's doctrine (`role_for` had the row, this function had not),
        # and left her convoy to investigate every stranger
        return "commodore"
    if key in ("frigate", "sixty-four", "razee", "seventy-four"):
        return "kings-ship"  # package 75: the new men of war's descriptions with the frigate
    if key == "brig-sloop":
        return "cruiser"
    if key == "cutter" and kind == "station":
        return "cruiser"
    if kind == "station":
        return "kings-ship"
    return "merchant"


# The states in which the far body is on a detour from her intent's plan, which is saved
# and taken up again when she returns to a plan state.
_DETOUR_STATES = frozenset(
    {
        "hove to for weather",
        "investigating a stranger",
        "chasing",
        "evading",
        "running for shelter",
        "at anchor",
        "in distress",
    }
)
_PLAN_STATES = frozenset({"on passage", "beating", "keeping station", "in company"})


def _plan_of_legs(legs: list[Leg]) -> list[tuple[Any, ...]]:
    """The far body's plan from the planner's legs: each mark steered to, and the
    anchorage's mark followed by the anchor."""
    plan: list[tuple[Any, ...]] = []
    for leg in legs:
        if leg.kind == "out":
            continue  # the outer road is passed on the way out; the body needs no mark for it
        name = "the station" if leg.kind == "station" else leg.words
        plan.append(("to", leg.position, name))
        if leg.kind == "anchorage":
            plan.append(("anchor", leg.port or ""))
    return plan


def _station_square(mark: Position, radius_nm: float) -> list[tuple[Any, ...]]:
    """The station kept as the far body keeps a patrol (`ships._goal_plan`): four marks
    about the station's point, cycled."""
    return [
        ("to", destination(mark, bearing, radius_nm * units.NAUTICAL_MILE), "the station")
        for bearing in (270.0, 0.0, 90.0, 180.0)
    ]


class FarCaptain(Judgement):
    """The rules-based captain of a far-detail vessel (package 43; spec M6 §4 "one brain,
    two bodies", §19): the same doctrine and the same judgement as `Captain`, on a
    perception built from her own truth once a minute (`Perception.of_vessel`), each
    state resolved into a plan of the far body (`resolve_state`) instead of a book. He
    keeps the history of his states for the record the tests and the notes read; nothing
    of his mind is a line in the player's log. Across the crewed promotion his state is
    folded into the near body's `Captain` and back (`fold_in`, `fold_back`)."""

    def __init__(
        self,
        world: Any,
        vessel: Any,
        intent: str,
        role: str = "",
        free: bool = False,
        given: Intent | None = None,
    ) -> None:
        self.world = world
        self.vessel = vessel
        self.intent_words = " ".join(str(intent).split())
        # `given`: the intent read already (a scenario ship's `free_intent:`, always free)
        self.intent: Intent | None = (
            given if given is not None else read_intent(world, self.intent_words, free)
        )
        self.role = role or role_of_vessel(vessel, self.intent)
        self.doctrine: Doctrine | None = load_doctrine(self.role)
        self.state: str | None = None
        self.trend = ""
        self._wind_log: list[tuple[int, float]] = []
        self._gale_over_since: int | None = None
        self._stranger: str | None = None
        self.spoken_ids: set[str] = set()
        self.given_up: set[str] = set()
        self.fired_on: set[str] = set()  # the ships that fired on her (package 70)
        self.recognised: dict[str, dict[str, Any]] = {}  # package 71: by signal or hail
        self.pirates: set[str] = set()  # seen to fire under false colours (package 71)
        self._business: dict[str, Any] = {}
        self._waiting_at_road = False
        self.last_judged = -1
        self._state_entered: int | None = None
        self._departing = ""
        self.history: list[tuple[int, str]] = []
        self.planned = False  # the intent's plan laid on the body

    # -- who and what ------------------------------------------------------------------

    def words(self) -> str:
        what = f"{self.role}; the intent: {self.intent.words if self.intent else ''}"
        if self.state:
            what += f"; {self.state}"
        if self.intent is not None and self.intent.done:
            what += " (done)"
        return what

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "intent": self.intent.to_dict() if self.intent else None,
            "state": self.state,
            "stranger": self._stranger,
            "spoken": sorted(self.spoken_ids),
            "history": [list(h) for h in self.history],
        }

    def set_intent(self, words: str, free: bool = False) -> str:
        """`ship "X": intent <words>`: the intent read anew, the plan laid again; `free`
        takes words no form reads as a free intent, for which no plan is laid and under
        which her captain keeps the role and the doctrine of her service he had (package
        86's fold-in, the review's finding)."""
        self.intent = read_intent(self.world, words, free)
        self.intent_words = " ".join(words.split())
        if not (self.intent.kind == FREE and self.role):
            self.role = role_of_vessel(self.vessel, self.intent)
        self.doctrine = load_doctrine(self.role)
        self.planned = False
        self.vessel.saved_plan = None
        self.state = None
        return f"the captain's intent: {self.intent.words}"

    # -- the tick ---------------------------------------------------------------------

    def tick(self) -> None:
        """Once a minute, at the roll-up's cadence, before the body moves: perceive from
        her truth, judge the doctrine's transitions, and work the state."""
        world = self.world
        tick = world.clock.tick
        if self.last_judged >= 0 and tick - self.last_judged < JUDGE_EVERY_S:
            return
        self.last_judged = tick
        if self.vessel.done:
            return
        held = getattr(self, "over_head", None)
        if held is not None:
            # an order given over his head by the director's hand (package 62): he holds by
            # it until the director's next order to her or a glass, then his plan again
            event = str(held.get("event") or "")
            if tick < int(held["until"]) and not (
                event and _hold_event_came(world, self.vessel, event)
            ):
                return
            self.take_up_again()
        crew = getattr(self.vessel, "crew", None)
        near = getattr(crew, "captain", None) if crew is not None else None
        if near is not None and near.seated and not near.stand_in:
            # a model (or the player) at the captain's station of this ship, kept across
            # the switch in the far shape (spec M6 §20): the body is theirs to work; the
            # brain stands in when the door is silent, as the near captain does
            return
        p = perceive_vessel(world, self.vessel, self)
        self._read_trend(p)
        if self.state is None:
            self._enter(self._first_state(p))
        self._transitions(p)
        self._work(p)
        # the signals (package 71): the flying hoists of the sail in sight read, answered
        # and obeyed; the private signal; the colours by doctrine
        from freesail.world import signalling

        signalling.far_minute(self, p)

    def _first_state(self, p: Perception) -> str:
        if p.anchor_down and p.in_port:
            self._departing = p.in_port
            return "in port"
        if p.anchor_down:
            return "at anchor"
        if self._in_a_set():
            return "in company"  # package 72: a member of a set starts at her station
        if self._stationed() and self._on_station():
            return "keeping station"
        return "on passage"

    def _in_a_set(self) -> bool:
        """A member of a squadron or a convoy who is not its commander nor a detached
        division's leader (package 72): her station is the set's and her plan the station
        leg, not her intent's legs."""
        from freesail.world.squadrons import plan_state_of

        return plan_state_of(self.world, str(self.vessel.id), "on passage") == "in company"

    def _stationed(self) -> bool:
        """A station's intent, or a fishing trip's ground worked as one (package 43b)."""
        return self.intent is not None and self.intent.kind in ("station", "fish")

    def _enter(self, state: str) -> None:
        from freesail.world.squadrons import plan_state_of

        # package 72: a member of a set enters `in company` where her doctrine would enter
        # a plan state (her station is the set's); the commander and a ship alone as before
        state = plan_state_of(self.world, str(self.vessel.id), state)
        old = self.state
        self.state = state
        self._state_entered = self.world.clock.tick
        self.history.append((self.world.clock.tick, state))
        if state in _PLAN_STATES and state != "in company" and not self.planned:
            self._plan()
        resolve_state(self.vessel, state, self)
        if state == "keeping station":
            self._business.pop("hauled_off", None)
            self._business.pop("fishing_tick", None)  # the trip's hours counted on the ground
        if state in ("investigating a stranger", "chasing", "evading"):
            self._business["since"] = self.world.clock.tick
        if old in ("investigating a stranger", "chasing", "evading") and state not in (
            "investigating a stranger",
            "chasing",
            "evading",
        ):
            self._stranger = None

    # -- the plan ----------------------------------------------------------------------

    def _plan(self) -> None:
        """The intent's legs over the chart from where she is (`Planner`, the ports'
        tracks and the common tracks, a headland given an offing), as the far body's
        plan; refused in words into the vessel's `warning` when a mark is not the
        chart's."""
        if self.intent is None:
            return
        if self.intent.kind == FREE:
            # a free intent (2026-10-26): no legs to lay, and a plan with none is a voyage
            # done; she lies to where she is until her captain's station sails her
            self.vessel.plan = [("lie_to", math.inf)]
            self.vessel.cycle = False
            self.vessel.saved_plan = None
            self.vessel.tack = 0.0
            self.planned = True
            return
        try:
            legs = Planner(self.world).legs_for(self.intent, self.vessel.position, self._departing)
        except ValueError as e:
            self.vessel.warning = f"cannot lay the plan for {self.intent.words}: {e}"
            legs = []
        plan = _plan_of_legs(legs)
        self.vessel.plan = plan
        self.vessel.cycle = False
        self.vessel.saved_plan = None
        self.vessel.tack = 0.0
        self.planned = True

    def _station_mark(self) -> Position | None:
        if not self._stationed():
            return None
        place = _mark(self.world, self.intent.destination)
        if place is None:
            return None
        if self.intent.kind == "fish":
            return place[1]  # the ground itself (package 56; `Planner.legs_for`)
        return station_off(self.world, place[1], self.intent.radius_nm)

    def _on_station(self) -> bool:
        mark = self._station_mark()
        if mark is None or self.intent is None:
            return False
        _, d = bearing_and_distance(self.vessel.position, mark)
        return d / units.NAUTICAL_MILE <= self.intent.radius_nm * 2.0

    # -- the hooks the stimuli ask -----------------------------------------------------

    def _is_enemy(self, s: dict[str, Any]) -> bool:
        known = self._known_enemy(s)  # package 71: the shot, the private signal, the hail
        if known is not None:
            return known
        nation = s.get("nation")
        if not nation:
            return False
        nations = getattr(self.world, "nations", None)
        return bool(nations is not None and nations.at_war(str(nation), self.vessel.nation))

    def _enemy_within(self, p: Perception, within_nm: float) -> dict[str, Any] | None:
        # the far body never takes the engaging transition (package 70): the far fight is
        # 74's, and a far ship that lay to in "engaging" with no battery would neither fight
        # nor close to hail; she chases and speaks as M6 had her (`combat/far.py` is the
        # measure of the far fight, run apart)
        return None

    def _stranger_struck(self, s: dict[str, Any]) -> bool:
        v = self.world.vessels.get(str(s.get("id") or ""))
        return bool(v is not None and getattr(v, "struck", False))

    def _enemy_struck(self, p: Perception) -> bool:
        # the far body has no battery: the nearest enemy within the breaking-off distance
        # struck is the mark struck (the far fight is 74's; `combat/far.py` the measure)
        th = self.doctrine.threshold if self.doctrine is not None else (lambda k, v=None: v)
        for s in p.strangers:
            if not self._is_enemy(s) or s.get("estimate_m") is None:
                continue
            if float(s["estimate_m"]) / units.NAUTICAL_MILE > float(th("break_off_nm", 2.0)):
                continue
            if self._stranger_struck(s):
                return True
        return False

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

    def _shelter_port(self, p: Perception) -> Any:
        ports = getattr(self.world, "ports", None)
        nations = getattr(self.world, "nations", None)
        if ports is None or not getattr(ports, "ports", None) or nations is None:
            return None
        d = self.doctrine
        reach = float(d.threshold("shelter_within_nm", 20)) if d else 20.0
        best = None
        for port in ports.ports.values():
            stance = nations.stance(
                port.nation,
                self.vessel.nation,
                port.closed_to,
                blockaded_by=getattr(port, "blockaded_by", None),
            )
            if stance in ("hostile", "closed"):
                continue
            _, dist = bearing_and_distance(self.vessel.position, port.outer_road.position)
            nm = dist / units.NAUTICAL_MILE
            if nm <= reach and (best is None or nm < best[1]):
                best = (port, nm)
        return best[0] if best else None

    def _ready_for_sea(self, p: Perception) -> bool:
        """In port her business is a wait (`IN_PORT_WAIT_S`), the tide taken to serve."""
        since = self._state_entered
        # a ship the world's business drew lying in port (package 43b) has had some hours of
        # her wait before the draw
        before = float(self._business.get("drawn_in_port_s", 0.0) or 0.0)
        return bool(p.in_port and since is not None and p.tick - since >= IN_PORT_WAIT_S - before)

    # -- the work of each state ---------------------------------------------------------

    def _work(self, p: Perception) -> None:
        state = self.state
        if state == "on passage":
            if self._stationed() and self._on_station():
                self._enter("keeping station")
        elif state == "keeping station" and self.intent is not None and self.intent.kind == "fish":
            self._fishing(p)
        elif state in ("investigating a stranger", "chasing"):
            if self._stranger is None or not any(
                s.get("id") == self._stranger for s in p.strangers
            ):
                near = self._nearest_stranger(p)
                self._stranger = near.get("id") if near else None
                self.vessel.plan = [("chase", self._stranger, HAIL_REACH_M)]
            self._spoken_if_within_hail(p)
        elif state == "evading":
            enemy = self._overmatched(p, 1e9) or self._nearest_enemy(p, 1e9)
            if enemy is not None:
                self._stranger = enemy.get("id")
                self.vessel.plan = [("away", self._stranger)]
        elif state == "at anchor":
            since = self._state_entered or 0
            clear = p.visibility not in ("a mile", "a cable")
            if clear and p.daylight == "day" and p.tick - since >= AT_ANCHOR_LEAST_S:
                self._weigh()
        elif state == "in port":
            self._in_port(p)

    def _fishing(self, p: Perception) -> None:
        """The fishing trip (package 43b): the hours of the intent worked on the ground, the
        time kept across a detour (a gale, a stranger run from), then home to the port she
        sailed from, where she goes in and is gone from the sea (`_in_port`)."""
        intent = self.intent
        assert intent is not None
        from freesail.world import fishing

        b = self._business
        last = b.get("fishing_tick")
        step = 0.0 if last is None else float(p.tick - int(last))
        b["fishing_s"] = float(b.get("fishing_s", 0.0)) + step
        b["fishing_tick"] = p.tick
        # package 56: her gear worked on the ground by the same evolutions' times and the
        # same catch function as the player's (truth 106), the take struck below
        if step > 0.0:
            fishing.far_work(self.world, self.vessel, step)
        if b["fishing_s"] < float(intent.hours or 0.0) * 3600.0:
            return
        fishing.trip_done_far(self.world, self.vessel)
        home = intent.origin
        port = getattr(self.world, "ports", None)
        found = port.find(home) if port is not None and getattr(port, "ports", None) else None
        name = found.name if found is not None else home
        self.set_intent(f"run home to {name}")
        self.role = "fisherman"
        self.doctrine = load_doctrine("fisherman")
        self._enter("on passage")

    def _nearest_stranger(self, p: Perception) -> dict[str, Any] | None:
        items = self._unspoken(p)
        if not items:
            return None
        return min(items, key=lambda s: s.get("estimate_m") or math.inf)

    def _spoken_if_within_hail(self, p: Perception) -> None:
        """Within hail of the stranger in hand she speaks her (`stranger spoken` next
        minute): a sail spoken is a stranger no more, for both captains (the other's
        brain is told, when she has one)."""
        for s in p.strangers:
            if s.get("id") != self._stranger or s.get("estimate_m") is None:
                continue
            if float(s["estimate_m"]) <= HAIL_REACH_M:
                self.speak(str(s["id"]))

    def speak(self, other_id: str) -> None:
        """A sail spoken by this captain, and he by her."""
        if other_id in self.spoken_ids:
            return
        self.spoken_ids.add(other_id)
        vessels = self.world.vessels
        other = vessels.get(other_id)
        brain = getattr(other, "brain", None) if other is not None else None
        if brain is not None:
            brain.spoken_ids.add(self.vessel.id)
            # the standard exchange between two rules captains (package 71, spec M7 §4):
            # each reads the other's nation from his answer (a liar's words believed)
            from freesail.world import hail as H
            from freesail.world import signalling

            nations = getattr(self.world, "nations", None)
            words = H.exchange_words(self.world, self.vessel, other)
            answers = [w for w in words.split("'") if w.strip()]
            theirs = answers[1] if len(answers) > 1 else ""
            mine = answers[3] if len(answers) > 3 else ""
            n_theirs = H.nation_in_words(nations, theirs)
            n_mine = H.nation_in_words(nations, mine)
            if n_theirs and nations is not None:
                signalling.recognise(
                    self,
                    other_id,
                    n_theirs,
                    "the hail",
                    nations.at_war(n_theirs, str(self.vessel.nation)),
                )
            if n_mine and nations is not None:
                signalling.recognise(
                    brain,
                    str(self.vessel.id),
                    n_mine,
                    "the hail",
                    nations.at_war(n_mine, str(other.nation)),
                )
            self._exchange = words
        if other_id != PLAYER_ID and hasattr(vessels, "spoke"):
            vessels.spoke(self.vessel, other_id)

    def _weigh(self) -> None:
        """Under way again from an anchorage: the plan taken up (`under way` fires next)."""
        v = self.vessel
        if v.saved_plan is not None:
            v.plan = list(v.saved_plan)
            v.saved_plan = None
        else:
            v.plan = []
        if not v.plan:
            self.planned = False
            self._plan()
        v.tack = 0.0

    def _in_port(self, p: Perception) -> None:
        """The business in port: the voyage's end (a passage, a letter or a run home
        done, she has gone in and is gone from the sea), a cargo bought or sold by the
        wait, and under way again when ready."""
        if self.intent is None:
            return
        port = p.in_port
        if self.intent.kind in ("passage", "home", "letter") and port == self.intent.destination:
            if self.role == "fisherman":
                self._land_the_catch(port)
            self.intent.done = True
            self.vessel.done = True
            return
        if self.intent.kind == "trade" and port == self.intent.destination:
            if self._ready_for_sea(p):
                from freesail.world.business import transact

                if transact(self.world, self, port):
                    # package 84, step 4 (the owner's decision 5): her cargo sold, a return
                    # cargo bought, and she sails again by her new intent's plan
                    self._departing = port
                    self._plan()
                    self.vessel.tack = 0.0
                    self._enter("on passage")
                    return
                self.intent.done = True
                self.vessel.done = True
            return
        if self._ready_for_sea(p):
            self._departing = port
            self.planned = False
            self.vessel.saved_plan = None
            self._plan()
            self.vessel.tack = 0.0

    def _land_the_catch(self, port_id: str) -> None:
        """The fisherman home (package 56): her catch sold at her port's fish quay at the
        player's price (`fishing.land_far`), the sale in the business's record."""
        from freesail.world import fishing

        ports = getattr(self.world, "ports", None)
        port = ports.ports.get(port_id) if ports is not None else None
        if port is None:
            return
        record = fishing.land_far(self.world, self.vessel, port)
        business = getattr(self.world, "business", None)
        if record is None or business is None:
            return
        for d in business.drawn:
            if d.id == self.vessel.id:
                tons = sum(record["sold"].values())
                d.landed = f"{tons:.1f} tons sold at {port.name} for £{record['pounds']:.0f}" + (
                    f", {sum(record['spoiled'].values()):.1f} spoiled" if record["spoiled"] else ""
                )

    # -- an order over his head (spec M7b §3; package 62) ------------------------------

    # the director's order he holds by: {order, until, plan, saved, sail_order}, the plan as
    # it stood before the first of them; None when he sails by his own judgement (a class
    # default, so that a checkpoint from before loads with none)
    over_head: dict[str, Any] | None = None

    def over_his_head(
        self,
        order: str,
        until: int,
        stash: tuple[list[Any], list[Any] | None, str],
        event: str = "",
    ) -> None:
        """An order of the far shape's given to her as his own by the director's hand: he
        is told it came over his head, so that he holds by it until `until` (or the
        director's next order to her, which sets it again) and does not fight it with his
        own judgement, his plan as it stood before the first of them kept to be taken up
        again (`take_up_again`)."""
        held = self.over_head
        if held is None:
            plan, saved, sail_order = stash
            self.over_head = {
                "order": order,
                "until": int(until),
                "plan": list(plan),
                "saved": None if saved is None else list(saved),
                "sail_order": sail_order,
            }
            if event:
                self.over_head["event"] = event  # the hold named (package 66)
        else:
            held["order"], held["until"] = order, int(until)
            if event:
                held["event"] = event
            else:
                held.pop("event", None)

    def take_up_again(self) -> None:
        """The glass out (or `carry on`): his plan as it stood before the director's order
        laid on the far body again, his sail his own, and his judgement given from this
        minute; said in her log."""
        held = self.over_head
        if held is None:
            return
        self.over_head = None
        v = self.vessel
        v.plan = list(held.get("plan") or [])
        saved = held.get("saved")
        v.saved_plan = None if saved is None else list(saved)
        v.sail_order = str(held.get("sail_order") or "")
        v.lying_to_s = 0.0
        v.tack = 0.0
        if not v.plan and self.intent is not None and not self.intent.done:
            self.planned = False
            self._plan()
        self.last_judged = self.world.clock.tick
        from freesail.world.crews import her_log

        her_log(
            self.world,
            v,
            f"The captain takes up his plan again ({self.intent.words if self.intent else ''}).",
        )

    # -- across the crewed promotion (spec M6 §19, §20) --------------------------------

    def fold_in(self, captain: Captain) -> None:
        """The brain's state carried into the near body's `Captain` at the promotion:
        the intent and the role, the state (whose book the near captain loads), the
        stranger in hand, the sails spoken, the trend's memory."""
        captain.intent = self.intent
        captain.intent_words = self.intent_words
        captain.error = ""  # her World read a free intent's words, and refused them
        captain.role = self.role
        own = str(getattr(self.vessel, "role", "") or "")
        if own:
            # package 75 (Build-Ships.md §8.1): her scenario's role, which her captain takes
            # again when his intent is changed (`Captain.set_intent`); unset without one, so
            # that his checkpoint is as before
            captain.scenario_role = own
        captain.doctrine = self.doctrine
        captain.trend = self.trend
        captain._wind_log = list(self._wind_log)
        captain._gale_over_since = self._gale_over_since
        captain._stranger = self._stranger
        captain.spoken_ids = set(self.spoken_ids)
        captain.recognised = dict(self.recognised)  # package 71
        captain.pirates = set(self.pirates)
        captain.given_up = set(self.given_up)
        captain.last_judged = -1
        held = getattr(self, "over_head", None)
        if held is not None and self.world.clock.tick < int(held["until"]):
            # an order over his head carried across (package 62): the near captain holds by
            # it for the rest of its glass, then takes her up from where she is
            self.over_head = None
            # the parent's tick into her World's own, which counts from her promotion
            left = int(held["until"]) - int(self.world.clock.tick)
            captain.over_head_until = int(captain.world.clock.tick) + left
            captain.over_head_order = str(held.get("order") or "")
            captain.over_head_event = str(held.get("event") or "")
            plan = self.vessel.plan
            if plan and plan[0][0] == "lie_to":
                # the far body lay to by his order: the near body heaves to by it, his words
                # the first of her new log's
                from freesail.world.captains import actor_for

                captain.world.submit(
                    "heave to",
                    actor=actor_for(self.state or "on passage"),
                    said="By the captain: heaving to",
                )
            return
        self.over_head = None
        if self.state is not None and self.state not in ("in distress",):
            captain._enter(self.state)

    def fold_back(self, captain: Captain) -> None:
        """The near body's state folded back into the brain at the demotion."""
        self.intent = captain.intent
        self.trend = captain.trend
        self._wind_log = list(captain._wind_log)
        self._gale_over_since = captain._gale_over_since
        self._stranger = captain._stranger
        self.spoken_ids |= set(getattr(captain, "spoken_ids", set()))
        self.recognised.update(getattr(captain, "recognised", {}) or {})  # package 71
        self.pirates |= set(getattr(captain, "pirates", set()) or set())
        self.given_up |= set(getattr(captain, "given_up", set()) or set())
        state = captain.state or "on passage"
        if state in ("beating", "in distress"):
            state = "on passage"
        self.planned = False
        self.vessel.saved_plan = None
        self.state = None
        self.last_judged = -1
        self._enter(state)
        near_until = getattr(captain, "over_head_until", None)
        near_world = getattr(captain, "world", None)
        left = None
        if near_until is not None and near_world is not None:
            # her World's own tick (it counts from her promotion) into the parent's
            left = int(near_until) - int(near_world.clock.tick)
        if left is not None and left > 0:
            # an order over his head carried back (package 62): the plan just laid kept to be
            # taken up when the glass is out, the far body lying to if the near one was
            until = int(self.world.clock.tick) + left
            v = self.vessel
            stash = (list(v.plan), None if v.saved_plan is None else list(v.saved_plan), "")
            readings = getattr(getattr(captain, "world", None), "readings", None)
            manoeuvre = str(readings.value("manoeuvre_in_hand") or "") if readings else ""
            if manoeuvre in ("hove to", "heaving to"):
                v.plan = [("lie_to", math.inf)]
            self.over_his_head(
                str(getattr(captain, "over_head_order", "") or ""),
                until,
                stash,
                event=str(getattr(captain, "over_head_event", "") or ""),
            )


def _hold_event_came(world: Any, vessel: Any, event: str) -> bool:
    from freesail.world.crews import hold_event_came

    return hold_event_came(world, vessel, event)


# Within hail, in metres (`ships.HAIL_NM`, four cables), the distance a chase or an
# investigation closes to and speaks her at.
HAIL_REACH_M = 0.4 * units.NAUTICAL_MILE


def resolve_state(vessel: Any, state: str, brain: FarCaptain | None = None) -> bool:
    """The state machine's state resolved into a far-detail plan on a vessel of
    `freesail.world.ships` (one brain, two bodies). Without a brain (package 40's
    interface): `hove to for weather` is no way, she lies to until told otherwise; `on
    passage` is her goal's plan, kept; the rest are refused (False) so that no body is
    moved by a state it cannot resolve. With a brain (package 43) every state resolves:
    the plan states (on passage, beating, keeping station) take up the intent's plan or
    the station's square; a detour (hove to, investigating, chasing, evading, running
    for shelter, at anchor) saves the plan and lays its own (no way; a chase of the
    stranger in hand to hailing distance; a course away from her; the nearest open road
    and the anchor; the anchor where she is); in port she lies at anchor; in distress and
    engaging she lies to. Returns whether the state was resolved."""
    if state not in STATES:
        raise ValueError(f"'{state}' is no state of the machine.")
    if brain is None:
        if state not in FAR_DETAIL_STATES:
            return False
        if state == "in company":
            # package 72: a member with no brain keeps her station in her set; the station
            # leg is the set's to lay (`squadrons._lay_station_leg`), and is kept here
            vessel.lying_to_s = 0.0
        elif state == "hove to for weather":
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
    was = vessel.state
    if state in _DETOUR_STATES and was not in _DETOUR_STATES:
        vessel.saved_plan = list(vessel.plan)
    if state in _PLAN_STATES:
        if was in _DETOUR_STATES and vessel.saved_plan is not None:
            vessel.plan = list(vessel.saved_plan)
            vessel.saved_plan = None
            vessel.lying_to_s = 0.0
        if state == "in company":
            # package 72 (spec M7 §21): her station in her set, the station leg; her own
            # intent's legs are the commander's business
            sets = getattr(brain.world, "squadrons", None)
            sq = sets.of(vessel.id) if sets is not None else None
            vessel.plan = [("station", sq.id)] if sq is not None else list(vessel.plan)
            vessel.cycle = False
            vessel.saved_plan = None
            vessel.lying_to_s = 0.0
        elif state == "keeping station":
            mark = brain._station_mark()
            if mark is not None and brain.intent is not None:
                vessel.plan = _station_square(mark, brain.intent.radius_nm)
                vessel.cycle = True
        elif vessel.cycle and brain.intent is not None and brain.intent.kind != "station":
            vessel.cycle = False
    elif state == "hove to for weather":
        vessel.plan = [("lie_to", math.inf)]
    elif state in ("investigating a stranger", "chasing"):
        vessel.plan = [("chase", brain._stranger, HAIL_REACH_M)]
    elif state == "evading":
        vessel.plan = [("away", brain._stranger)]
    elif state == "running for shelter":
        port = brain._shelter_port(perceive_vessel(brain.world, vessel, brain))
        if port is None:
            vessel.plan = [("lie_to", math.inf)]
        else:
            vessel.plan = [
                ("to", port.outer_road.position, port.outer_road.name),
                ("anchor", port.id),
            ]
    elif state in ("at anchor", "in port"):
        if not vessel.plan or vessel.plan[0][0] != "anchor":
            vessel.plan = [("anchor", "")]
    elif state in ("in distress", "engaging", "struck"):
        vessel.plan = [("lie_to", math.inf)]
    vessel.tack = 0.0
    vessel.state = state
    return True
