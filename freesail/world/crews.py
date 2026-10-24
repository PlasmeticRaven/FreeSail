"""The crewed promotion (package 43; spec M6 §19 and §20; M5 §25's seam filled).

Within `CREWED_NM` of the centre (the player's ship) a far-detail vessel with a brain
becomes **a full part-and-crew ship from her file**: a World of her own (`CrewedWorld`)
with her hull and rig under the same physics, her company mustered, her stations bound,
her own account, lookout and book, and her rules-based captain (`captains.Captain`) giving
his orders through the same channel as the player's, his state folded in from the far
brain (`brains.FarCaptain.fold_in`). Beyond `CREWED_DEMOTE_NM` she is demoted, her state
folded back (position, heading, sail set, the brain's state) and the World dropped, or kept
in the far shape when a station is seated on her (§20, `far_shape`). A hard cap
(`CREWED_CAP`) holds the number of crewed ships: the nearest first, and a ship in dealings
with the player (a chase, a hail, within the last glass) before a nearer one that is not;
the hysteresis of two miles keeps a ship at the edge from flapping between bodies. The
figures are the measurement's (docs/dev/TuningNotes.md, package 43: a crewed ship costs
what the player's frigate costs, the physics of her sails four substeps a tick, so a dozen
at once would halve the owner's sixty times; three keep the whole over twice it on the
build machine).

**One brain, two bodies**: the promotion changes the body only. The crewed World shares
the parent's chart, tide table and weather (its wind follows the parent's systems at her
own place on the parent's plane, `_follow_weather`; the sky and the visibility are the
parent's at the ship, as the brief wants the same visibility the player's lookout has), and
sees the other sail and the player's ship through a view of the parent's vessels
(`CrewView`), so that her lookout hails the player as the player's hails her. Her log is
her own, and nothing of her promotion is a line of the player's log: the player's lookout
sees a sail that is the same sail, which is the design point held hardest (spec M6 §4).

A vessel within a port's reach, at anchor, in port or running for shelter is not
promoted, and a crewed vessel that comes to an anchor is demoted: the port's business
(the pilot, the boat, the market) is the player's ship's machinery and the far brain's
wait (`brains.IN_PORT_WAIT_S`), not a crewed stranger's, until the world's business (43b).

**The director's hand** (spec M7b §3; package 62; `hand`): an order of a ship's own grammar
given to her captain's station as his own, by the world order `ship "X": order ...`.
Crewed, through her World as his order under his rules' actor; at far detail through the
far shape's orders (`far_order` on the far body, or `submit_far` where a station keeps her
World in the far shape); her log says it as his, a far body with no World keeping the line
in her short story (`Vessel.story`). Her captain holds by it a glass (`HAND_HOLD_S`) or
until the next order to her, then sails by his intent again; `ask_crewed` makes a far ship
within the range a crewed one first, the cap and its order unchanged.
"""

from __future__ import annotations

import math
import re
import zlib
from dataclasses import replace
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.world.geo import Position, bearing_and_distance

__all__ = [
    "CREWED_CAP",
    "CREWED_DEMOTE_NM",
    "crewed_settings_of",
    "settings",
    "CREWED_FLOOR_TICKS_S",
    "CREWED_NM",
    "DEALING_S",
    "CrewView",
    "CrewedWorld",
    "HAND_HOLD_S",
    "ask_crewed",
    "captain_held_by",
    "crewed",
    "hand",
    "her_log",
    "demote",
    "promote",
    "switch",
]

# The promotion range and its hysteresis (package 43, from the measurement; spec M6 §19):
# promoted within four miles of the centre, where the tops make out her rig and read her
# sails' state (`ships.RIG_MADE_OUT_NM`), demoted beyond six, half an hour's sailing
# apart at four knots so that a ship at the edge does not flap; judgement on the
# measurement's cost of a crewed ship (docs/dev/TuningNotes.md, package 43).
CREWED_NM = 4.0
CREWED_DEMOTE_NM = 6.0
# The cap: three crewed ships beside the player's. Measured on the build machine: a crewed
# ship costs what the frigate costs (the sails' physics), the frigate alone 560 ticks a
# second quiet, with three crewed about 140, twice the sixty the owner plays at and four
# times it on his machine; twelve would be near fifty (docs/dev/TuningNotes.md, package
# 43). The floor the pace truth of §19 asserts with the cap full (`CREWED_FLOOR_TICKS_S`):
# the sixty times the owner plays at, on the build machine, half the figure measured.
CREWED_CAP = 3
CREWED_FLOOR_TICKS_S = 60.0
# A dealing with the player (a chase, a hail) counts for a glass (judgement).
DEALING_S = 1800
# The doubt of a crewed vessel's own account at her promotion: half a mile (judgement:
# her master has kept his reckoning as the player's has, and the far body gave no error).
PROMOTION_ACCOUNT_SIGMA_NM = 0.5
# The states a crewed vessel is demoted in, and a far one not promoted in: the port's
# business is not the crewed body's (see the module's head).
_NOT_CREWED_STATES = frozenset({"at anchor", "in port", "running for shelter", "in distress"})
# The roles never crewed: none since package 56 (spec M7b §21a; the owner, 2026-10-17:
# "the crewed promotion includes the fishermen"). Package 43b kept the fisherman of the
# world's business at far detail only; a fishing vessel near the player is now promoted
# like any other, the cap's order unchanged, and fishes at full detail by the same
# evolutions under her rules-based captain (`world.fishing.captain_work`). The name is
# kept, empty, for the rule's one place.
FAR_ONLY_ROLES: frozenset[str] = frozenset()


class CrewView:
    """The other sail as a crewed vessel's World sees them: the parent's vessels but
    herself, and the player's ship as a vessel (`Vessels.player_shadow`); nothing is
    moved from here (the parent moves them), and a vessel added here (a pilot's boat sent
    off for her) goes to the parent's sea."""

    def __init__(self, crew: CrewedWorld) -> None:
        self.crew = crew
        self.serial = 0

    @property
    def vessels(self) -> list[Any]:
        parent = self.crew.parent
        own = self.crew.vessel
        out = [v for v in parent.vessels.vessels if v is not own and not v.done]
        shadow = parent.vessels.player_shadow(parent)
        if shadow is not None:
            out.append(shadow)
        return out

    def active(self) -> list[Any]:
        return list(self.vessels)

    def get(self, vessel_id: str) -> Any:
        for v in self.vessels:
            if v.id == vessel_id:
                return v
        return None

    def find(self, words: str) -> Any:
        key = " ".join(str(words).lower().split()).removeprefix("the ")
        for v in self.vessels:
            if key in (v.id.lower(), v.name.lower(), v.name.lower().removeprefix("the ")):
                return v
        return None

    def add(self, vessel: Any) -> Any:
        return self.crew.parent.vessels.add(vessel)

    def tick(self, world: Any, dt: float = 60.0) -> list[tuple[Any, ...]]:
        return []

    def tick_near(self, world: Any, dt: float = 1.0) -> list[tuple[Any, ...]]:
        return []

    def in_sight(self, pos: Position, height_of_eye_m: float, visibility_nm: Any, daylight: str):
        from freesail.world.ships import Vessels

        view = Vessels.__new__(Vessels)
        view.world = self.crew
        view.vessels = self.vessels
        return Vessels.in_sight(view, pos, height_of_eye_m, visibility_nm, daylight)

    def to_dict(self) -> list[dict[str, Any]]:
        return []


class CrewedWorld(World):
    """A vessel's own World while she is promoted: her ship from her file at her truth,
    her company, her stations, her captain with the brain's intent and state; the chart,
    the tide and the weather the parent's. `shape` is "full" while her body is the
    physics', and "far" while a station seated on her is kept across a demotion (spec M6
    §20): then the far body moves her and this World only mirrors it for the station's
    readings (`far_tick`)."""

    def __init__(self, parent: World, vessel: Any) -> None:
        from freesail.api.session import attach_crew, make_ship

        self.parent = parent
        self.vessel = vessel
        self.shape = "full"
        sc = _crew_scenario(parent, vessel)
        seed = (int(parent.seed) * 1009 + zlib.crc32(str(vessel.id).encode("utf-8"))) % (2**31)
        ship = make_ship(vessel.ship_file, sc)
        ship.name = vessel.name  # her own name over her file's (package 70: two cutters in a log)
        super().__init__(seed=seed, scenario=sc, ship=ship)
        attach_crew(self)
        # package 71: her signal locker is her far body's (one object: the colours she
        # shows, the hoists flying, her lights), so that nothing is mirrored
        from freesail.world.signals import vessel_locker

        self.ship.extra["signals"] = vessel_locker(vessel)
        self.vessels = CrewView(self)
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["vessels_view"] = True
        self.conditions = parent.conditions
        _set_sail(self, vessel.sail_state)
        # a fishing vessel's fishery is one object for her two bodies (package 56): the
        # gear in the water and the catch the far body had, or this World's made from her
        # file given to the far body
        shared = getattr(vessel, "fishing", None)
        if shared is not None:
            self.fishery = shared
        elif getattr(self, "fishery", None) is not None:
            vessel.fishing = self.fishery
        if getattr(self, "fishery", None) is not None:
            from freesail.world.fishing import rig_gear_drag

            rig_gear_drag(self, self.fishery)
        if self.navigation is not None and self.position is not None:
            self.navigation.reckoning.set_position(
                self.position, self.clock.tick, sigma_nm=PROMOTION_ACCOUNT_SIGMA_NM
            )
        brain = vessel.brain
        if brain is not None:
            self.captain.intent_words = brain.intent_words
            brain.fold_in(self.captain)
        self.record(
            Severity.ROUTINE,
            "crew.promoted",
            f"{vessel.name} at full detail: her company mustered, her captain "
            f"{self.captain.name} in command ({self.captain.state or 'on passage'}).",
            data={"id": vessel.id, "state": self.captain.state},
        )

    # -- the parent's weather at her place -------------------------------------------

    def _plane_km(self) -> tuple[float, float] | None:
        pos = self.position
        plane = self.parent.plane_of(pos) if pos is not None else None
        if plane is None:
            return None
        return plane[0] / 1000.0, plane[1] / 1000.0

    def _follow_weather(self) -> None:
        parent = self.parent
        if parent.systems is not None and parent.weather is None:
            km = self._plane_km()
            if km is not None:
                self.wind.follow(*parent.systems.surface_wind_at(km[0], km[1]))
            self.wind.air_mass = parent.wind.air_mass
        elif self.weather is not None:
            super()._follow_weather()
        else:
            self.wind.follow(parent.wind.base_direction, parent.wind.base_speed)
            self.wind.air_mass = parent.wind.air_mass

    def _tick_weather_minute(self) -> None:
        # the sky and the visibility are the parent's at the ship: the same visibility the
        # player's lookout has (the brief); no line of the weather's in her log
        self.conditions = self.parent.conditions

    # -- the far shape (spec M6 §20) ----------------------------------------------------

    def submit(
        self, text: str, actor: str = "captain", said: str | None = None, routine: bool = False
    ) -> Any:
        """An order to the crewed ship: the World's own at full detail; in the far shape
        the plan layer's (`submit_far`: the far-shape orders on the body, the readings and
        the conversation through the grammar, the rest refused in words)."""
        if getattr(self, "shape", "full") == "far":
            return submit_far(self, text, actor, said, routine)
        return super().submit(text, actor=actor, said=said, routine=routine)

    def mirror_far(self) -> None:
        """The far body's truth into this World's ship and position (the far shape):
        called each second of the tick and again after the far body has moved at the
        minute, so that the station's readings and the body are one."""
        v = self.vessel
        self._position = v.position
        self._geo_last = (self.ship_x, self.ship_y)
        dyn = getattr(self.ship, "dyn", None)
        if dyn is not None:
            dyn.heading = units.deg_to_rad(v.heading_deg)
            dyn.target_heading = dyn.heading
            dyn.u = dyn.speed = units.knots_to_ms(v.speed_kn)
            dyn.v = 0.0

    def far_tick(self) -> None:
        """The World in the far shape, each second: the clock kept with the parent's,
        the body's truth mirrored into the ship and the account, the lookout once a
        minute, the stations sampled; no physics, no book, no judgement of the near
        captain's (the brain has her)."""
        self.clock.advance()
        self.mirror_far()
        self._follow_weather()
        self.wind.step(1.0, self.wind_record.mean_speed())
        self.wind_record.add(self.wind.effective_speed, self.wind.direction_from)
        if self.clock.ship_time.second == 0:
            self.conditions = self.parent.conditions
            if self.navigation is not None:
                self.navigation.reckoning.set_position(
                    self.vessel.position, self.clock.tick, sigma_nm=0.25
                )
            if self.lookout is not None:
                for severity, kind, text, data in self.lookout.look(self):
                    self.record(severity, kind, text, data=data)
        self._tick_sun()
        bells = self.clock.bells()
        if bells is not None:
            self.record(
                Severity.ROUTINE,
                "clock.bell",
                f"{units.format_bells(bells).capitalize()}.",
                data={"bells": bells},
            )
        for agent in list(self.agents.values()):
            agent.on_tick()


def _crew_scenario(parent: World, vessel: Any) -> Scenario:
    """The scenario of a crewed vessel's World: the parent's chart, start and weather
    script, her own position, heading and way, her nation; no systems of her own (the
    parent's are followed), no sky, no sea, no glass, no ports (see the head), no ships."""
    ps = parent.scenario
    wind_from, wind_ms = vessel._wind_at(parent)
    sc = replace(
        ps,
        name=f"{ps.name}: {vessel.name} at full detail",
        start_time=parent.clock.ship_time,
        wind_from_deg=float(wind_from),
        wind_speed_kn=units.ms_to_knots(float(wind_ms)),
        ship_x=0.0,
        ship_y=0.0,
        ship_heading_deg=float(vessel.heading_deg),
        ship_speed_kn=float(vessel.speed_kn),
        position=vessel.position.to_dict(),
        systems=[],
        climatology=False,
        background={},
        glass=False,
        sea=False,
        sky=None,
        chronometer=None,
        current=None,
        nation=str(vessel.nation),
        people=[],
        papers={},
        cargo={},
        ports=[],
        ships=[],
        world_orders=[],
        intent=str(vessel.intent_words or ""),
        books=[],
        fit=(getattr(vessel, "fit", "") or None),  # her own fit of guns, not the player's
    )
    sc.latitude_deg = vessel.position.lat_deg
    return sc


def _set_sail(crew: CrewedWorld, sail_state: str) -> None:
    """Her sail as the far body had it, set on the rig directly at the promotion (no
    evolution: the far body's word was the truth of her sail): plain sail, or the
    topsails reefed with the courses in, or the storm canvas lying to; trimmed to the
    wind as `trim sails` trims them."""
    from freesail.ship.parts import SailState
    from freesail.world.ships import _trim_for

    ship = crew.ship
    groups = getattr(ship, "groups", {}) or {}
    plain = [sid for sid in groups.get("plain sail", []) if sid in ship.sails]
    topsails = set(groups.get("topsails", []))
    courses = set(groups.get("courses", []))
    for sid in plain:
        sail = ship.sails[sid]
        if sail_state == "under plain sail":
            sail.state = SailState.SET
        elif sail_state == "under reefed topsails":
            if sid in courses:
                sail.state = SailState.FURLED
            else:
                sail.state = SailState.SET
                if sid in topsails and hasattr(sail, "reefs"):
                    sail.reefs = min(2, int(getattr(sail, "max_reefs", 2) or 2))
        elif sail_state in ("lying to", "at anchor"):
            sail.state = SailState.SET if sid in topsails else SailState.FURLED
    try:
        # the apparent wind from her heading, her way and the wind at her, as the polar
        # trims for it (`ships._balanced_speed_ms`), so that she is not promoted aback
        theta = units.wrap_pi(crew.wind.direction_from - float(ship.dyn.heading))
        tw = float(crew.wind.base_speed)
        u = float(getattr(ship.dyn, "u", 0.0) or 0.0)
        awa = math.atan2(math.sin(theta) * tw, math.cos(theta) * tw + u)
        ship.dyn.apparent_wind_angle = awa
        _trim_for(ship, awa)
        # the yards' brace is signed by the tack (`parts.Spar.brace_angle`: positive for
        # the starboard tack), which the polar's trimmer, always on one tack, leaves out
        sign = 1.0 if theta >= 0.0 else -1.0
        for y in ship.spars.values():
            if getattr(y, "is_yard", False):
                y.brace_angle = math.copysign(abs(y.brace_angle), sign)
    except Exception:  # noqa: BLE001 - a rig the trimmer cannot read: left as bent
        pass


def _sail_state_of(crew: CrewedWorld) -> str:
    """The far body's word for her sail from the crewed ship's rig."""
    if crew.at_anchor:
        return "at anchor"
    manoeuvre = str(crew.readings.value("manoeuvre_in_hand") or "")
    if manoeuvre in ("hove to", "heaving to"):
        return "lying to"
    ship = crew.ship
    groups = getattr(ship, "groups", {}) or {}
    for sid in groups.get("topsails", []):
        sail = ship.sails.get(sid)
        if sail is not None and sail.is_set and int(getattr(sail, "reefs", 0) or 0) > 0:
            return "under reefed topsails"
    return "under plain sail"


def mirror(vessel: Any, crew: CrewedWorld, minute: bool) -> None:
    """The crewed body's truth into the far body's record every tick, so that the
    parent's lookout, the brains and the save see one ship."""
    pos = crew.position
    if pos is not None:
        vessel.position = pos
    dyn = getattr(crew.ship, "dyn", None)
    if dyn is not None:
        vessel.heading_deg = units.rad_to_deg(float(dyn.heading)) % 360.0
        vessel.speed_kn = units.ms_to_knots(float(getattr(dyn, "speed", 0.0) or 0.0))
    if minute:
        vessel.sail_state = _sail_state_of(crew)
        state = crew.captain.state or vessel.state
        brain = vessel.brain
        if brain is not None and state and (not brain.history or brain.history[-1][1] != state):
            # the brain's record runs on through the near body (one brain, two bodies)
            brain.history.append((crew.parent.clock.tick, state))
            brain.state = state
        vessel.state = state


# ---------------------------------------------------------------------------
# The switch
# ---------------------------------------------------------------------------


def _crew_ids(world: World) -> tuple[str, ...]:
    """Every vessel with a World of her own, full or far in shape: the parent ticks each
    (`Vessels.tick_crews`, gated on `crewed_ids`)."""
    return tuple(v.id for v in world.vessels.vessels if v.crew is not None and not v.done)


def crewed(world: World) -> list[Any]:
    """The vessels at full detail now (a station's World kept in the far shape is not
    one: it costs little and counts nothing against the cap)."""
    return [
        v
        for v in world.vessels.vessels
        if v.crew is not None and v.crew.shape == "full" and not v.done
    ]


def promote(world: World, vessel: Any) -> CrewedWorld:
    """A far-detail vessel made a crewed ship beside the player's (spec M6 §19)."""
    if vessel.crew is not None:
        if vessel.crew.shape == "far":
            _to_full(vessel)
        return vessel.crew
    crew = CrewedWorld(world, vessel)
    vessel.crew = crew
    vessel.detail = "crewed"
    world.vessels.crewed_ids = _crew_ids(world)
    return crew


def _to_full(vessel: Any) -> None:
    """A station's World kept in the far shape brought back to the full surface (spec M6
    §20): the body remade from her file at her truth under the same World object, so that
    the station is not reseated. Said in her log."""
    crew = vessel.crew
    from freesail.api.session import attach_crew, make_ship

    sc = _crew_scenario(crew.parent, vessel)
    ship = make_ship(vessel.ship_file, sc)
    ship.name = vessel.name  # package 70
    old_extra = getattr(crew.ship, "extra", None) or {}
    crew.ship = ship
    crew.ship.extra["rng"] = crew.rng
    attach_crew(crew)
    for key in ("agents", "agent_journals", "stations", "navigation", "standing", "player_seat"):
        if key in old_extra:
            crew.ship.extra[key] = old_extra[key]
    crew._geo_last = (0.0, 0.0)
    crew._position = vessel.position
    crew.shape = "full"
    _set_sail(crew, vessel.sail_state)
    if getattr(crew, "fishery", None) is not None:
        from freesail.world.fishing import rig_gear_drag

        rig_gear_drag(crew, crew.fishery)  # the trawl down on the new body (package 56)
    brain = vessel.brain
    if brain is not None:
        brain.fold_in(crew.captain)
    crew.record(
        Severity.URGENT,
        "crew.promoted",
        f"{vessel.name} at full detail again: her company at their stations, the deck "
        "and the sails hers to work by every order.",
        data={"id": vessel.id, "state": crew.captain.state},
    )


def demote(world: World, vessel: Any) -> None:
    """A crewed ship folded back to far detail: her truth and her captain's state into
    the far body and the brain; her World dropped, or kept in the far shape while a
    station is seated on her (spec M6 §20)."""
    crew = vessel.crew
    if crew is None:
        return
    mirror(vessel, crew, minute=True)
    brain = vessel.brain
    if brain is not None and crew.shape == "full":
        brain.fold_back(crew.captain)
    seated = any(not h.agent.released for h in crew.agents.values())
    if seated:
        # urgent in her log (package 43): the station's whole surface changes, and a
        # station standing by is woken to be told its shape
        crew.shape = "far"
        crew.record(
            Severity.URGENT,
            "crew.demoted",
            f"{vessel.name} at far detail: beyond the range of the ship, her body is the "
            "plan's; the station keeps, in the plan layer's shape (a course shaped, sail as "
            "a state, heaving to, the chase, the intent), until she is near again.",
            data={"id": vessel.id},
        )
    else:
        vessel.crew = None
        vessel.detail = "far"
    world.vessels.crewed_ids = _crew_ids(world)


def _dealing(world: World, vessel: Any) -> bool:
    return vessel.dealing_tick >= 0 and world.clock.tick - vessel.dealing_tick <= DEALING_S


def enforce_budgets(world: World) -> None:
    """The director's seats' budgets (spec M6 §23; `orders._seat`): a station held under a
    director's seat is stood down, with the reason, when its samples or its hours are
    spent, and the seat given back; once a minute. Package 67 widened the seats to every
    station and to a person's voice, and keeps them in `world.seats.enforce`."""
    if not (getattr(world, "director_seats", None) or {}):
        return
    from freesail.world.seats import enforce

    enforce(world)


def crewed_settings_of(raw: Any, where: str = "the scenario") -> dict[str, Any]:
    """`crewed: {cap: N, range_nm: X}` read from a scenario file or a driver's flags: the
    cap a whole number (0 promotes nobody), the range in miles over nought; refused in
    words otherwise."""
    if not isinstance(raw, dict):
        raise ValueError(f"{where}: `crewed` is a mapping with `cap` and `range_nm`, not {raw!r}.")
    out: dict[str, Any] = {}
    if raw.get("cap") is not None:
        cap = int(raw["cap"])
        if cap < 0:
            raise ValueError(f"{where}: the crewed cap is a whole number, not {raw['cap']!r}.")
        out["cap"] = cap
    if raw.get("range_nm") is not None:
        rng = float(raw["range_nm"])
        if rng <= 0:
            raise ValueError(f"{where}: the crewed range is in miles over nought, not {rng!r}.")
        out["range_nm"] = rng
    return out


def settings(world: Any) -> tuple[int, float, float]:
    """The promotion's budget for this world: (the cap, the range in miles, the demotion
    distance), the build machine's constants unless a driver's flags
    (`world.crewed_settings`) or the scenario (`scenario.crewed`) say otherwise; the
    demotion keeps its two miles of hysteresis beyond the range (the lead, 2026-10-17, on
    the owner's machine ticking twelve crewed ships above sixty a second)."""
    chosen: dict[str, Any] = {}
    sc = getattr(world, "scenario", None)
    if isinstance(getattr(sc, "crewed", None), dict):
        chosen.update(sc.crewed)
    if isinstance(getattr(world, "crewed_settings", None), dict):
        chosen.update(world.crewed_settings)
    cap = int(chosen.get("cap", CREWED_CAP))
    rng = float(chosen.get("range_nm", CREWED_NM))
    return cap, rng, rng + (CREWED_DEMOTE_NM - CREWED_NM)


def switch(world: World) -> None:
    """The crewed promotion by the distance from the centre, once a minute: demoted
    beyond `CREWED_DEMOTE_NM` or when she anchors; promoted within `CREWED_NM` up to the
    cap, a ship in dealings with the player before a nearer one that is not, and a
    dealing ship within the range taking the place of the farthest crewed ship that has
    none when the cap is full."""
    centre = world.position
    if centre is None:
        return
    cap, within_nm, demote_nm = settings(world)
    vessels = world.vessels
    with_brain = [v for v in vessels.vessels if v.brain is not None and not v.done]
    if not with_brain and not vessels.crewed_ids:
        return
    far_nm: dict[str, float] = {}
    for v in with_brain:
        far_nm[v.id] = bearing_and_distance(centre, v.position)[1] / units.NAUTICAL_MILE
    # demotions
    for v in list(crewed(world)):
        state = v.crew.captain.state if v.crew.shape == "full" else v.brain.state
        beyond = far_nm.get(v.id, math.inf) > demote_nm
        if (beyond and not _dealing(world, v)) or state in _NOT_CREWED_STATES:
            demote(world, v)
    # promotions, dealings first and then the nearest
    wanted = [
        v
        for v in with_brain
        if (v.crew is None or v.crew.shape == "far")
        and far_nm[v.id] <= within_nm
        and (v.brain.state or "on passage") not in _NOT_CREWED_STATES
        and getattr(v.brain, "role", "") not in FAR_ONLY_ROLES
    ]
    wanted.sort(key=lambda v: (not _dealing(world, v), far_nm[v.id]))
    for v in wanted:
        held = crewed(world)
        if len(held) < cap:
            promote(world, v)
            continue
        if not _dealing(world, v):
            break
        # the cap full: the farthest crewed ship without dealings gives her place
        idle = [c for c in held if not _dealing(world, c)]
        if not idle:
            break
        farthest = max(idle, key=lambda c: far_nm.get(c.id, 0.0))
        demote(world, farthest)
        promote(world, v)


# ---------------------------------------------------------------------------
# A station on another ship, kept across the switch (spec M6 §20; decision 40)
# ---------------------------------------------------------------------------

# The orders the far shape works, in the plan layer's own terms (spec M6 §20: "courses
# shaped, sail made or shortened as a state, heaving to, the chase and the intent's
# changes"); everything else of the ship's is refused in words naming these, and the
# readings, the deck's conversation and the book's listing are answered as at full
# detail, from what the far body has.
FAR_SHAPE_WORDS = (
    "shape a course for <a place or a position>",
    "steer <a course>",
    "heave to",
    "fill away",
    "give chase",
    "haul off",
    "make sail",
    "shorten sail",
    "come to an anchor",
    "weigh",
    "keep the station",
)
FAR_SHAPE_REFUSAL = (
    "She is at far detail, beyond the range of the ship: her body is the plan's, and the "
    "orders that work it are " + ", ".join(FAR_SHAPE_WORDS) + ". The readings, the "
    "conversation and the book's listing are answered; the whole surface returns when she "
    "is near again, with no reseat."
)


def station_world(parent: World, words: str) -> tuple[Any, CrewedWorld]:
    """The World a station on another ship is seated in (`--station captain --ship <id>`):
    the vessel by her id or her name, her crewed World (promoted when she is within the
    range, else made in the far shape, where it mirrors the far body for the station's
    readings until the promotion brings the full surface back beneath the same station).
    Refused in words (ValueError) for a ship not on the sea or one without a captain of
    her own (no intent: give her one with `ship "<name>": intent <words>`)."""
    vessel = parent.vessels.find(words)
    if vessel is None or vessel.done:
        names = ", ".join(v.name for v in parent.vessels.active() if v.description) or "none"
        raise ValueError(f"No ship named {words!r} is on the sea; the sail: {names}.")
    if vessel.brain is None:
        raise ValueError(
            f"{vessel.name} has no captain of her own to be seated for: give her an intent "
            f"first (the world order 'ship \"{vessel.name}\": intent <the intent>')."
        )
    if vessel.crew is not None:
        return vessel, vessel.crew
    centre = parent.position
    nm = (
        bearing_and_distance(centre, vessel.position)[1] / units.NAUTICAL_MILE
        if centre is not None
        else math.inf
    )
    full = nm <= CREWED_NM and len(crewed(parent)) < CREWED_CAP
    crew = CrewedWorld(parent, vessel)
    vessel.crew = crew
    vessel.detail = "crewed"
    if not full:
        crew.shape = "far"
        crew.record(
            Severity.NOTABLE,
            "crew.demoted",
            f"{vessel.name} at far detail: beyond the range of the ship, her body is the "
            "plan's; a station here works it in the plan layer's shape (a course shaped, sail "
            "as a state, heaving to, the chase, the intent) until she is near again.",
            data={"id": vessel.id},
        )
    parent.vessels.crewed_ids = _crew_ids(parent)
    return vessel, crew


def _place_for(world: World, words: str) -> tuple[Position, str] | None:
    from freesail.world.ships import place_position

    return place_position(world, words)


def far_order(crew: CrewedWorld, text: str) -> tuple[str, str, dict[str, Any]] | None:
    """An order of the far shape carried out on the far body (the plan): (kind, the
    line, data); None when the words are none of the far shape's. Refused in words
    (OrderError) when a place is not the chart's."""
    import re

    from freesail.orders.errors import OrderError

    v = crew.vessel
    brain = v.brain
    low = " ".join(text.lower().split()).rstrip(".")
    m = re.match(r"^(?:shape|lay) (?:a |the )?course for (?P<place>.+)$", low)
    if m:
        found = _place_for(crew.parent, m.group("place"))
        if found is None:
            raise OrderError(f"The chart knows no place named {m.group('place')!r}.")
        v.saved_plan = None
        v.plan = [("to", found[0], found[1])]
        v.tack = 0.0
        if brain is not None:
            brain.planned = True
        return "helm.set", f"Shaped a course for {found[1]} (the plan's leg).", {"place": found[1]}
    m = re.match(r"^steer (?P<course>.+)$", low)
    if m:
        try:
            rad = units.parse_course(m.group("course"))
        except Exception:  # noqa: BLE001 - the units' own reader
            rad = None
        if rad is None:
            raise OrderError(f"{m.group('course')!r} is no course to steer.")
        from freesail.world.geo import destination

        far = destination(v.position, units.rad_to_deg(rad) % 360.0, 60.0 * units.NAUTICAL_MILE)
        v.saved_plan = None
        v.plan = [("to", far, f"a course {units.point_name(rad)}")]
        v.tack = 0.0
        return "helm.set", f"Helm ordered: steer {units.point_name(rad)} (the plan's course).", {}
    if low in ("heave to", "lie to", "bring her to"):
        if not v.plan or v.plan[0][0] != "lie_to":
            v.saved_plan = list(v.plan)
            v.plan = [("lie_to", math.inf)]
        return "ship.hove_to", "Hove to (the far body lies to, drifting a knot to leeward).", {}
    if low in ("fill away", "fill", "get her way on"):
        if v.plan and v.plan[0][0] == "lie_to":
            v.plan = list(v.saved_plan or [])
            v.saved_plan = None
            v.lying_to_s = 0.0
        return "ship.filled_away", "Filled away; the plan's leg again.", {}
    if low in ("give chase", "chase", "chase the stranger", "stand after her"):
        if brain is None:
            return None
        from freesail.world.brains import HAIL_REACH_M, perceive_vessel

        p = perceive_vessel(crew.parent, v, brain)
        near = brain._nearest_stranger(p)
        if near is None:
            raise OrderError("No sail in sight to chase.")
        brain._stranger = str(near["id"])
        v.saved_plan = v.saved_plan or list(v.plan)
        v.plan = [("chase", brain._stranger, HAIL_REACH_M)]
        return "helm.set", f"Gave chase to {near.get('known') or 'a sail'} {near['relative']}.", {}
    if low in ("haul off", "haul off from her", "bear up and run"):
        if brain is None:
            return None
        from freesail.world.brains import perceive_vessel

        p = perceive_vessel(crew.parent, v, brain)
        near = brain._nearest_stranger(p)
        if near is None:
            raise OrderError("No sail in sight to haul off from.")
        brain._stranger = str(near["id"])
        v.saved_plan = v.saved_plan or list(v.plan)
        v.plan = [("away", brain._stranger)]
        return (
            "helm.set",
            f"Hauled off from {near.get('known') or 'a sail'} {near['relative']}.",
            {},
        )
    if low in ("make sail", "make all sail", "set plain sail", "set all plain sail"):
        v.sail_order = "under plain sail"
        return "sail.set", "Plain sail made (as a state of the far body).", {}
    if low in ("shorten sail", "reef the topsails", "shorten sail for weather"):
        v.sail_order = "under reefed topsails"
        return "sail.reefed", "Sail shortened: the topsails reefed, the courses in (a state).", {}
    if low in ("come to an anchor", "let go the anchor", "anchor", "let go the best bower"):
        if not (v.plan and v.plan[0][0] == "anchor"):
            v.saved_plan = list(v.plan)
        v.plan = [("anchor", "")]
        return (
            "ship.anchored",
            "Came to an anchor where she is (the far body rides head to wind).",
            {},
        )
    if low in ("weigh", "weigh anchor", "get under way", "up anchor"):
        if v.plan and v.plan[0][0] == "anchor":
            v.plan = list(v.saved_plan or [])
            v.saved_plan = None
        if not v.plan and brain is not None:
            brain.planned = False
            brain._plan()
        return "ship.under_way", "Under way again; the plan's leg.", {}
    if low in ("keep the station", "back to the station", "resume the station"):
        if brain is None or brain.intent is None or brain.intent.kind != "station":
            raise OrderError("She has no station to keep: her intent is not a station's.")
        brain._enter("keeping station")
        return "helm.set", "The station kept again (the plan's square about it).", {}
    return None


def _is_a_reading(crew: CrewedWorld, text: str) -> bool:
    """Whether the words ask a reading, a query or the deck's conversation, which the far
    shape answers through the ship's grammar (nothing of them moves the body)."""
    from freesail.orders import prompt, read_whole, stations
    from freesail.orders.errors import OrderError
    from freesail.orders.vocabulary import load_vocabulary
    from freesail.standing import grammar as standing

    ship = crew.ship
    if stations.recognises(text, ship) is not None:
        return True
    if standing.recognises(text) in ("standing orders", "show standing order"):
        return True
    vocab = load_vocabulary()
    try:
        order = read_whole(ship, text, vocab)
    except OrderError:
        try:
            return prompt.answer_unparsed(ship, text, vocab) is not None
        except OrderError:
            return False
    return order.verb in vocab.readings


def submit_far(crew: CrewedWorld, text: str, actor: str, said: str | None, routine: bool) -> Any:
    """`World.submit` in the far shape: a far-shape order on the plan, a reading or the
    conversation through the grammar, anything else refused in words."""
    from freesail.orders.errors import OrderError

    text = " ".join(text.split())
    if _is_a_reading(crew, text):
        return World.submit(crew, text, actor=actor, said=said, routine=routine)
    try:
        found = far_order(crew, text)
    except OrderError as e:
        return crew.record(
            Severity.ROUTINE,
            "order.rejected",
            f"Order not carried out ({text!r}): {e}",
            actor=actor,
            data={"order": text, "reason": str(e)},
        )
    if found is None:
        return crew.record(
            Severity.ROUTINE,
            "order.rejected",
            f"Order not carried out ({text!r}): {FAR_SHAPE_REFUSAL}",
            actor=actor,
            data={"order": text, "reason": FAR_SHAPE_REFUSAL, "far_shape": True},
        )
    kind, words, data = found
    crew.record(
        Severity.ROUTINE,
        "order.accepted",
        f"{said}." if said else f"Order: {text}.",
        actor=actor,
        data={"order": text, "far_shape": True},
    )
    return crew.record(Severity.ROUTINE, kind, words, actor=actor, data=data | {"far_shape": True})


def shape_words(crew: CrewedWorld) -> str:
    """The notice a station on another ship is given of her shape (spec M6 §20: the
    sample says which)."""
    v = crew.vessel
    if crew.shape == "far":
        return (
            f"{v.name} is at far detail, beyond the range of the player's ship: her body is "
            "the plan's, moved once a minute by her polar in the wind at her. Your orders "
            "work it in the plan layer's shape: " + ", ".join(FAR_SHAPE_WORDS) + ". The "
            "readings are the far body's (her place, the wind, what her lookout sees); the "
            "sails, the hands and the book are as they stood when she was last at full "
            "detail. When she is near the ship again the whole surface returns beneath this "
            "station, with no reseat, and the log says so."
        )
    return (
        f"{v.name} is at full detail beside the player's ship: her hull and rig under the "
        "physics, her company at their stations, every order of the ship's yours."
    )


# ---------------------------------------------------------------------------
# The director's hand (spec M7b §3; package 62): an order of a ship's own grammar given to
# her captain's station as his own
# ---------------------------------------------------------------------------

# How long her captain holds by an order given over his head before his intent is his
# again (the lead's reading of the brief, item 1: a heave-to held until the director's next
# order to her or a glass, then his intent again; judgement: a glass is long enough for a
# boat to board and search and for his own rules not to undo the order at their next
# judgement, short enough that a forgotten order does not keep her lying to all day). The
# director's next order to her sets it again from then; `carry on` ends it sooner.
HAND_HOLD_S = 1800
# The words that give her back to her captain before the glass is out (`captain: carry
# on`'s word, said of another ship).
CARRY_ON_WORDS = ("carry on", "carry on with your intent", "as you were")

# The hold named (package 66; the dispatches test's finding 4: steering a frigate across
# eight miles of sea took two orders and still failed, a glass being three miles and a half
# at seven knots): `... for a watch`, `... for two glasses`, `... for an hour`, or `...
# until <an event>`, the hold so named in place of the glass. An event she is held until
# ends it when it comes to her, or a day at most (judgement: a forgotten order does not
# keep her lying to for ever; a day is longer than any chase or passage the hand is for).
HOLD_UNTIL_MAX_S = 24 * 3600
HOLD_SPANS_S = {"glass": 1800, "hour": 3600, "watch": 4 * 3600, "day": 24 * 3600}
_COUNTS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
}
# The events a hold may be named until, by their words (`hold_event_came`): her own, read
# from her truth as her captain perceives it (`brains.perceive_vessel`).
HOLD_EVENTS: dict[str, str] = {
    "a sail within hail": "hail",
    "a sail in hail": "hail",
    "within hail": "hail",
    "a sail sighted": "sail",
    "a sail in sight": "sail",
    "a landfall": "land",
    "landfall": "land",
    "land in sight": "land",
    "the land in sight": "land",
    "hove to": "hove to",
    "she is hove to": "hove to",
    "at anchor": "anchor",
    "anchored": "anchor",
}
# The events in the words a refusal names them by, one for each.
HOLD_EVENT_NAMES = ("a sail within hail", "a sail in sight", "a landfall", "hove to", "at anchor")
_HOLD_TAIL = re.compile(
    r"^(?P<order>.+?)\s+(?:for\s+(?P<n>a|an|one|two|three|four|five|six|seven|eight|\d+)\s+"
    r"(?P<unit>glass(?:es)?|hours?|watch(?:es)?|days?)|until\s+(?P<until>.+?))\s*$",
    re.I,
)


def hold_of(text: str) -> tuple[str, int | None, str]:
    """(the order, the hold in seconds or None for the default, the event's key or "")
    from the hand's words: 'give chase for a watch' -> ('give chase', 14400, ''); 'heave
    to until a sail within hail' -> ('heave to', None, 'hail'). Raises ValueError in words
    for an event a hold cannot be named until."""
    m = _HOLD_TAIL.match(" ".join(str(text).split()))
    if m is None:
        return text, None, ""
    order = m.group("order").strip()
    if m.group("until") is not None:
        said = " ".join(m.group("until").lower().split()).rstrip(".")
        key = HOLD_EVENTS.get(said) or HOLD_EVENTS.get(said.removeprefix("the "))
        if key is None:
            raise ValueError(
                f"a hold is named until one of her own events ({', '.join(HOLD_EVENT_NAMES)}), "
                "or for a time ('for a watch', 'for two glasses', 'for an hour')"
            )
        return order, None, key
    n_word = m.group("n").lower()
    n = int(n_word) if n_word.isdigit() else _COUNTS[n_word]
    unit = m.group("unit").lower().rstrip("s")
    unit = "glass" if unit.startswith("glas") else ("watch" if unit.startswith("watch") else unit)
    return order, n * HOLD_SPANS_S[unit], ""


def hold_event_came(parent: World, vessel: Any, event: str) -> bool:
    """Whether the event a hold was named until has come to her (package 66): a sail within
    hail (four cables) or in sight from her masthead, the land in sight, she hove to, she
    at anchor; read from her truth as her far captain perceives it, whichever body moves
    her (the crewed body is mirrored into the far record every tick)."""
    if not event:
        return False
    from freesail.world.brains import HAIL_REACH_M, perceive_vessel

    if event == "hove to":
        crew = getattr(vessel, "crew", None)
        if crew is not None and crew.shape == "full":
            readings = getattr(crew, "readings", None)
            try:
                said = str(readings.value("manoeuvre_in_hand") or "") if readings else ""
            except Exception:  # noqa: BLE001
                said = ""
            return said == "hove to"
        plan = getattr(vessel, "plan", None) or []
        return bool(plan) and plan[0][0] == "lie_to"
    try:
        p = perceive_vessel(parent, vessel)
    except Exception:  # noqa: BLE001  (a body that cannot be perceived: nothing came)
        return False
    if event == "hail":
        return any(float(s.get("estimate_m", math.inf)) <= HAIL_REACH_M for s in p.strangers)
    if event == "sail":
        return bool(p.strangers)
    if event == "land":
        return bool(p.land_in_sight)
    if event == "anchor":
        return bool(p.anchor_down) or bool(
            getattr(getattr(vessel, "crew", None), "at_anchor", False)
        )
    return False


def hold_words(parent: World, until: int, event: str) -> str:
    """'until 14:30', 'until a sail within hail comes to her (a day at most, 10:01
    tomorrow)'."""
    when = _until_words(parent, until)
    if int(until) - int(parent.clock.tick) >= 24 * 3600 - 60:
        when += " tomorrow"
    if not event:
        return f"until {when}"
    said = next(k for k, v in HOLD_EVENTS.items() if v == event)
    return f"until {said} comes to her (a day at most, {when})"


class _FarBody:
    """The far body as `far_order` reads it, for a vessel with no World of her own: her
    vessel and the parent's sea, which is all the far shape's orders want."""

    def __init__(self, parent: World, vessel: Any) -> None:
        self.parent = parent
        self.vessel = vessel


def captain_held_by(vessel: Any) -> tuple[str, str] | None:
    """(her captain's name, who holds his station: "a model" or "the player at his seat")
    when a model or the player holds the captain's station of her World, kept at full
    detail or in the far shape; None when nobody does (spec M7b §3, the rule of reach)."""
    crew = getattr(vessel, "crew", None)
    if crew is None:
        return None
    from freesail.agents.agent import CAPTAIN
    from freesail.agents.harness import _stations_held

    seat = getattr(crew, "player_seat", None)
    for h in _stations_held(crew):
        if h.station.name != CAPTAIN:
            continue
        who = "the player at his seat" if h is seat else "a model"
        try:
            person = crew.stations.holder(CAPTAIN)
        except Exception:  # noqa: BLE001 - a muster that cannot run binds nobody
            person = None
        return (person.name if person is not None else "her captain"), who
    return None


def _as_said(ship: Any, text: str) -> str:
    """'heave to' -> 'heaving to', by her own ship's grammar where she has one."""
    from freesail.standing.runtime import said_as_done

    try:
        return said_as_done(ship, text)
    except Exception:  # noqa: BLE001 - a far body has no parts to read the words by
        from freesail.evolutions.runner import gerund

        words = text.split()
        return " ".join([gerund(words[0]), *words[1:]]) if words else text


def her_log(parent: World, vessel: Any, text: str) -> None:
    """A line of her own log: her World's when she has one, else the far body's short
    story (`Vessel.story`; spec M7b §12b's ground, since a far ship has no log of her own)."""
    crew = getattr(vessel, "crew", None)
    if crew is not None:
        crew.record(Severity.ROUTINE, "captain.order", text, data={"id": vessel.id})
        return
    vessel.story = (*tuple(getattr(vessel, "story", ()) or ()), (parent.clock.tick, text))


def _until_words(parent: World, until: int) -> str:
    from datetime import timedelta

    when = parent.clock.ship_time + timedelta(seconds=int(until) - int(parent.clock.tick))
    return when.strftime("%H:%M")


def hand(parent: World, vessel: Any, text: str) -> str:
    """**The director's hand** (spec M7b §3; package 62): `text`, an order of her own
    grammar, given to her captain's station as his own. Crewed, through her World as his
    order under his rules' actor, his own domain and nothing more (her grammar refuses what
    he could not do), her log saying it as his ("By the captain: heaving to"); at far detail
    through the far shape's orders (`far_order`, and `submit_far` where a station keeps her
    World in the far shape), the line in her log or the far body's story. Her captain is
    told it came over his head: he holds by it until the director's next order to her or a
    glass (`HAND_HOLD_S`), then sails by his intent again; `carry on` gives her back sooner.
    The rule of reach is the channel's (`orders.reach`). Returns the words for the
    channel's line; raises ValueError in words when she cannot carry it as said."""
    from freesail.world import orders as world_orders

    text = " ".join(str(text).split()).rstrip(".")
    if not text:
        raise ValueError("an order to her captain wants its words ('order heave to')")
    if world_orders.recognises(text):
        raise ValueError(
            "that is an order to the world, not to her: her captain orders his ship, and the "
            "world's orders are the channel's own, given as themselves"
        )
    if text.lower() in CARRY_ON_WORDS:
        return _carry_on(vessel)
    # the hold named (package 66): 'for a watch', 'until a sail within hail'
    text, span, event = hold_of(text)
    if text.lower() in CARRY_ON_WORDS:
        return _carry_on(vessel)
    if event:
        span = HOLD_UNTIL_MAX_S
    until = int(parent.clock.tick) + (HAND_HOLD_S if span is None else span)
    crew = vessel.crew
    full = crew is not None and crew.shape == "full"
    if full:
        words = _hand_crewed(vessel, crew, text, until, event)
    else:
        words = _hand_far(parent, vessel, text, until, event)
    if vessel.brain is None and not full:
        return (
            f"{words}; she has no captain of her own beyond her goal, and the order stands "
            "until the next ('fill away', 'shape a course for <a place>')"
        )
    return (
        f"{words}; her captain holds by it {hold_words(parent, until, event)} or the next "
        "order to her, then sails by his intent again"
    )


_READING_WORDS = (
    "that is a reading or a word on her deck, not an order: her captain reads her for "
    "himself, and the truth reads her for the director"
)


def _hand_crewed(vessel: Any, crew: CrewedWorld, text: str, until: int, event: str = "") -> str:
    from freesail.world.captains import actor_for

    if _is_a_reading(crew, text):
        raise ValueError(_READING_WORDS)
    cap = crew.captain
    said = f"By the captain: {_as_said(crew.ship, text)}"
    e = crew.submit(text, actor=actor_for(cap.state or "on passage"), said=said)
    if e.kind == "order.rejected":
        why = str((e.data or {}).get("reason") or e.text).rstrip(".")
        raise ValueError(f"{vessel.name}'s captain could not give it as said: {why}")
    # her own clock: a crewed World counts its ticks from her promotion
    cap.over_his_head(
        text, int(crew.clock.tick) + (until - int(crew.parent.clock.tick)), event=event
    )
    return f"{vessel.name}'s captain gave it as his own, at full detail ({said})"


def _hand_far(parent: World, vessel: Any, text: str, until: int, event: str = "") -> str:
    from freesail.orders.errors import OrderError
    from freesail.world.captains import actor_for

    crew = vessel.crew
    brain = vessel.brain
    stash = (
        list(vessel.plan),
        None if vessel.saved_plan is None else list(vessel.saved_plan),
        str(getattr(vessel, "sail_order", "") or ""),
    )
    said = f"By the captain: {_as_said(None, text)}"
    if crew is not None:
        # a station keeps her World in the far shape: the far orders through it, as the
        # station's own are (`submit_far`), her World's log saying it as his
        if _is_a_reading(crew, text):
            raise ValueError(_READING_WORDS)
        actor = actor_for(getattr(brain, "state", None) or vessel.state or "on passage")
        e = submit_far(crew, text, actor, said, False)
        if e.kind == "order.rejected":
            data = e.data or {}
            if data.get("far_shape"):
                raise ValueError(far_no_way(parent, vessel))
            raise ValueError(str(data.get("reason") or e.text).rstrip("."))
        words = e.text.rstrip(".")
    else:
        try:
            found = far_order(_FarBody(parent, vessel), text)  # type: ignore[arg-type]
        except OrderError as e:
            raise ValueError(str(e).rstrip(".")) from None
        if found is None:
            raise ValueError(far_no_way(parent, vessel))
        words = found[1].rstrip(".")
        her_log(parent, vessel, f"{said}.")
    if brain is not None:
        brain.over_his_head(text, until, stash, event=event)
    return f"{vessel.name}'s captain gave it as his own, at far detail ({said}): {words}"


def far_no_way(parent: World, vessel: Any) -> str:
    """Why the far shape cannot carry an order, in words: the orders it carries, and, when
    she is within the promotion's range, that the director may ask for her crewed first."""
    why = (
        f"{vessel.name} is at far detail: her body is the plan's, and the orders the far shape "
        "carries are " + ", ".join(FAR_SHAPE_WORDS)
    )
    centre = parent.position
    if centre is None or vessel.brain is None:
        return why
    cap, within_nm, _ = settings(parent)
    nm = bearing_and_distance(centre, vessel.position)[1] / units.NAUTICAL_MILE
    if nm <= within_nm:
        why += (
            f"; she is within the range of the ship ({nm:.1f} miles), so you may ask for her "
            f"crewed first ('ship \"{vessel.name}\": crewed'), the cap allowing "
            f"({len(crewed(parent))} of {cap} at full detail now), and give it her at full "
            "detail"
        )
    return why


def ask_crewed(parent: World, vessel: Any) -> str:
    """`ship "<name>": crewed` (package 62): a far ship within the promotion's range made a
    crewed ship now, so that an order the far shape cannot carry may be given her at full
    detail; refused in words beyond the range, in a state no ship is crewed in, or with the
    cap full (the owner's budget and the cap's order stand). Returns the words."""
    crew = vessel.crew
    if crew is not None and crew.shape == "full":
        raise ValueError(f"{vessel.name} is at full detail already")
    if vessel.brain is None:
        raise ValueError(
            f"{vessel.name} has no captain of her own to be crewed for: give her an intent "
            f"first ('ship \"{vessel.name}\": intent <the intent>')"
        )
    centre = parent.position
    cap, within_nm, _ = settings(parent)
    nm = (
        bearing_and_distance(centre, vessel.position)[1] / units.NAUTICAL_MILE
        if centre is not None
        else math.inf
    )
    if nm > within_nm:
        raise ValueError(
            f"{vessel.name} is {nm:.1f} miles from the ship, beyond the promotion's range of "
            f"{within_nm:g}: a ship is crewed only near the ship (the owner's budget)"
        )
    state = vessel.brain.state or "on passage"
    if state in _NOT_CREWED_STATES:
        raise ValueError(
            f"{vessel.name} is {state}, and a ship {state} is not crewed: the port's business "
            "is her far captain's"
        )
    held = crewed(parent)
    if len(held) >= cap:
        names = ", ".join(v.name for v in held)
        raise ValueError(
            f"the crewed cap is full ({cap}: {names}); the cap and its order stand (the "
            "nearest first, a ship in dealings with the player before a nearer one), and she "
            "takes her turn"
        )
    crew = promote(parent, vessel)
    return (
        f"{vessel.name} at full detail: her company mustered, her captain "
        f"{crew.captain.name} in command"
    )


def _carry_on(vessel: Any) -> str:
    """`ship "<name>": order carry on`: her captain given her back before the glass is out,
    his intent and his plan taken up again."""
    crew = vessel.crew
    none = f"{vessel.name}'s captain is under no order of yours: he sails by his intent"
    if crew is not None and crew.shape == "full":
        cap = crew.captain
        if getattr(cap, "over_head_until", None) is None:
            raise ValueError(none)
        cap.take_up_again()
        return f"{vessel.name}'s captain carries on: his intent again"
    brain = vessel.brain
    if brain is None or getattr(brain, "over_head", None) is None:
        raise ValueError(none)
    brain.take_up_again()
    return f"{vessel.name}'s captain carries on: his plan taken up again"
