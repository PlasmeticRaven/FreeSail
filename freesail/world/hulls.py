"""The Hull: what a World keeps of one ship (package 84, step 1; the design in
`docs/design/Design-OneWorld.md` §2.2 and its migration's first step).

A `World` holds two kinds of thing, and until this package nothing told them apart (the
study's §1.1): the world's own, one of each in a game (the clock, the seeded streams, the
chart, the tide table, the weather systems, the nations, the far bodies of the other sail,
the sets, the business, the world orders, the director); and **one ship's own** (her hull
and rig, her place on the sphere, the wind, sea, motion, sky, glass, tide and ground at
her, her lookout, her sun, her reckoning, her places, people, stations, papers, hold,
purse and stores, her ports' dealings, her fishery, her needs, her water and her health,
her book of standing orders, her rules captain, the harnesses at her stations, the
player's seat, her log, her readings view). This module gives the second kind an object
of its own, the `Hull`, kept as `world.own`.

**The façade.** Nothing that reads a World moves for it: every per-ship attribute of
`World` is a property to `own` (installed from `PER_SHIP_FIELDS` by `core/world.py`), with
a setter, so `world.ship`, `world.log`, `world.people` and the rest read and write the
Hull's fields under the names the grammar's and the readings' thousands of lines use. The
other way about, the Hull exposes the World's shared fields as properties (`hull.clock`,
`hull.rng`, `hull.chart`, `hull.vessels`, ...) and forwards `record`, `submit` and
`readings`, so that a consumer written against `world.<name>` reads the same name on a
hull. This is the ground the later steps stand on: `CrewedWorld` is a World that copies and
empties the shared things; a `Hull` is a ship that delegates them. In this step the methods
that work the fields stay on the World (its `tick` in today's order calling them, `record`,
`submit`, the `_tick_*`), so that no order of operations can move and the World's text
stands beside the sibling package editing it; they come to the Hull at the step that makes
it the container (step 6). The Hull's own surface here is the small set of pure reads of her
state (`ship_x`, `position`, `at_anchor`, `name`).

**The checkpoint.** A checkpoint written before this step pickles the per-ship fields on
the World's own dict; `World.__setstate__` lifts them into a Hull (`lift_old_state`) so that
the three fixture saves and the owner's saves load by the checkpoint road as before, a
`CrewedWorld` found in one converting the same way (it is a World). A field a newer Hull has
and an older checkpoint lacks is a class default here, as the World's were.

**The id.** A hull has an id (`Hull.id`): the vessel's for a crewed ship's World, and the
far brains' word for the player's ship (`brains.PLAYER_ID`) for the World's own, which the
registry of persons (step 2) names as a person's whereabouts and the save (step 8) keys by.
"""

from __future__ import annotations

from typing import Any

from freesail import units

__all__ = ["PER_SHIP_FIELDS", "SHARED_FIELDS", "Hull", "delegated", "lift_old_state", "own_id"]

_MISSING = object()

# Every per-ship field of a World (the study's §1.1), by the name the World's consumers read
# it under; each becomes a property of `World` to `World.own`, and each is a field of the
# Hull. The order is the World's constructor's, for the reader.
PER_SHIP_FIELDS: tuple[str, ...] = (
    # her seed and her streams, her scenario (the game's for the followed hull, her own copy
    # for another: her nation, her intent, her fit) and the sail she sees (the `Vessels` of
    # the sea for the followed hull, a `HullView` of every far body but her own for another),
    # each hull's since step 6; before it the crewed World's own copies
    "seed",
    "scenario",
    "rng",
    "vessels",
    # her hull and rig, and her place on the sphere (spec M5 §9)
    "ship",
    "origin",
    "_position",
    "_geo_last",
    # her lookout, the ground under her and her anchors' dragging (spec M5 §12, §18)
    "lookout",
    "ground",
    "_aground",
    "_dragging",
    "_drag_said",
    "_drag_seen",
    "_brought_up_s",
    # the tide's height and stream at her (spec M5 §16)
    "tide_state",
    "_tide_was_flood",
    # the sky and the visibility at her, her glass (spec M5 §2, §5)
    "glass",
    "conditions",
    "_last_conditions",
    # the sea and her motion (spec M5 §4)
    "sea",
    "motion",
    "_last_sea_words",
    "_last_sea_height",
    "_last_motion_words",
    "_motion_pending",
    # the wind at her, with her own gust stream, and the wind-shift bookkeeping
    "wind",
    "wind_record",
    "_last_logged_wind_direction",
    "_wind_shift_held_s",
    "wind_settled",
    "_wind_unsettled_s",
    "_wind_settling_s",
    "_wind_unsettled_why",
    "_wind_swing_ref",
    "_wind_settle_ref",
    "_wind_shifts_said",
    # the sun at her latitude (spec M4 §5)
    "sun",
    "_daylight",
    # her reckoning (spec M5 §13 to §15)
    "navigation",
    "_nav_pending",
    # her log, and the recurring kinds' last words (package 58a)
    "log",
    "_recurring_said",
    # her places aboard, her people, her stations, her papers, her hold, purse and stores,
    # her dealings with the ports (step 3; the port files are the world's `ports`), her
    # fishery, her needs, her water and her health (spec M5 §22 to §25; M7b §19 to §21a;
    # M7 §13, §16)
    "places",
    "people",
    "stations",
    "papers",
    "hold",
    "purse",
    "stores",
    "dealings",
    "fishery",
    "needs",
    "water",
    "ship_lost",
    "health",
    # the readings view cached per tick (spec M4 §2)
    "_readings_key",
    "_readings_view",
    # her book of standing orders and its runtime, her rules captain, the harnesses at her
    # stations and their journals, the player's seat (spec M4 §3, §4, §11; M6 §4)
    "standing",
    "captain",
    "agents",
    "agent_journals",
    "player_seat",
)

# The World's shared fields a Hull exposes under the same names (the design's §2.2), so
# that a consumer given a hull reads what it reads of a World.
SHARED_FIELDS: tuple[str, ...] = (
    "clock",
    "chart",
    "tide",
    "systems",
    "weather",
    "nations",
    "registry",
    "ports",
    "squadrons",
    "business",
    "world_orders",
    "marks_of_interest",
    "director_brief",
    "director_state",
    "director_seats",
    "journal",
    "inputs",
    "station_acts",
    "compression",
)


def delegated(target: str, name: str) -> property:
    """A property that reads, writes and deletes `name` on the attribute `target` of its
    object: `delegated("own", "ship")` on the World is `world.own.ship` under the name
    `world.ship`. A name the target lacks raises AttributeError as a plain attribute
    would, so `getattr(world, name, None)` and `hasattr` read as before."""

    def fget(self: Any) -> Any:
        return getattr(getattr(self, target), name)

    def fset(self: Any, value: Any) -> None:
        setattr(getattr(self, target), name, value)

    def fdel(self: Any) -> None:
        delattr(getattr(self, target), name)

    return property(fget, fset, fdel, doc=f"the {target}'s `{name}`")


def own_id() -> str:
    """The id of the World's own hull, the player's ship: the far brains' word for her
    (`brains.PLAYER_ID`, "the ship"), so that the id the sets, the action and the signals
    know her by is the hull's. Step 7 defines it once, in `ships.py`."""
    from freesail.world.brains import PLAYER_ID

    return str(PLAYER_ID)


class Hull:
    """One ship as a World keeps her: the fields of `PER_SHIP_FIELDS`, set by the World's
    constructor through its properties, and a `world` back-reference. `id` is the vessel's
    for a crewed ship's World and `own_id()` for the World's own."""

    # Class defaults for the fields a checkpoint from before their package lacks (each
    # was the World's class default before step 1, with its reason):
    # the wind-shift bookkeeping (package 37c, 37f, 58a; `World._log_wind_shift`)
    _wind_shift_held_s = 0
    wind_settled = True
    _wind_unsettled_s = 0
    _wind_settling_s = 0
    _wind_unsettled_why = ""  # "light" or "swing" while `wind_settled` is false
    _wind_swing_ref: float | None = None  # where an unsteady wind's mean last stood
    _wind_settle_ref: float | None = None  # where a light air's settling began (58a)
    _wind_shifts_said: tuple[tuple[int, int], ...] = ()  # the last shifts logged: tick, sense
    # the last words of each recurring kind of line (package 58a, `RECURRING_KINDS`)
    _recurring_said: dict[str, str] | None = None
    # the dragging's lines and "Brought up" (package 37f, 37k)
    _drag_said: dict[str, tuple[int, float]] | None = None
    _brought_up_s: int = 0
    _drag_seen: dict[str, tuple[float, float]] | None = None
    # the player's seat (package 40) and the keepers made at their first tick when a
    # checkpoint from before lacks them (`World.tick`, `_tick_needs`)
    player_seat: Any = None
    ship_lost: bool = False
    # the container (package 84, step 6): whether her physics run (`awake`; a sleeping
    # hull's body is her far body's, the plan's), her far body on the sea (`vessel`, None
    # for the followed hull until step 7), and the far body's anchor said once
    awake: bool = True
    vessel: Any = None
    _far_anchored: bool = False
    _bell_said: int = -1  # the tick her bell last struck (`World._bells_struck`)

    def __init__(self, world: Any, hull_id: str) -> None:
        self.world = world
        self.id = str(hull_id)

    def __repr__(self) -> str:
        name = getattr(getattr(self, "ship", None), "name", "") or self.id
        return f"Hull({name!r})"

    # -- the façade (package 84, step 6): a Hull stands where a World stood -----------------
    #
    # Her systems (`People`, `Dealings`, `Navigation`, the standing runtime, her captain, her
    # harnesses) hold her as their `world`, and the grammar's and the readings' functions
    # take her as one. Her per-ship fields are her own attributes; the World's shared fields
    # are properties to the World (installed below from `SHARED_FIELDS`); and every other
    # name of the World's (its methods, `_tick_*`, `plane_of`, `world_order`, `run`, the
    # properties over per-ship fields) is reached through `__getattr__`, which runs it with
    # this hull current (`World.as_hull`), so that `self.<per-ship field>` inside the World's
    # text reads and writes hers. Nothing of the World's text moves for it.

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") or "world" not in self.__dict__ or name in PER_SHIP_FIELDS:
            # a per-ship field she has not got is missing, not the World's (whose property
            # for it would read her again)
            raise AttributeError(name)
        world = self.__dict__["world"]
        attr = getattr(type(world), name, _MISSING)
        if attr is _MISSING:
            if name in world.__dict__:
                return world.__dict__[name]  # a shared thing set on the instance
            raise AttributeError(name)
        if isinstance(attr, property):
            with world.as_hull(self):
                return getattr(world, name)
        if callable(attr):
            hull = self

            def bound(*args: Any, **kw: Any) -> Any:
                with world.as_hull(hull):
                    return attr(world, *args, **kw)

            bound.__name__ = name
            return bound
        return attr

    @property
    def parent(self) -> Any:
        """The followed hull's façade (the player's ship), the name a crewed ship's World had
        for the World it sailed in: its per-ship names (`parent.ship`, `parent.position`,
        `parent.vessels`, `parent.record`) are the player's whichever hull is current, where
        the World's own would read the current hull; None for the followed hull herself, as a
        World has no parent."""
        world = self.world
        followed = world.hulls.get(world.followed)
        return None if followed is self else followed

    @property
    def shape(self) -> str:
        """ "full" awake, "far" asleep: the word the far shape of a station's World had."""
        return "full" if self.awake else "far"

    @shape.setter
    def shape(self, value: str) -> None:
        self.awake = str(value) == "full"

    @property
    def is_followed(self) -> bool:
        """Whether this is the World's followed hull (the player's ship until step 7)."""
        return self.world.hulls.get(self.world.followed) is self

    # -- her own, read from her state -------------------------------------------------

    @property
    def name(self) -> str:
        """Her name, her file's or the one her vessel was given."""
        return str(getattr(getattr(self, "ship", None), "name", "") or "")

    @property
    def ship_x(self) -> float:
        """Metres east of the start: the ship's own easting, whatever ship she is."""
        dyn = getattr(self.ship, "dyn", None)
        if dyn is not None:
            return float(dyn.x)
        return float(getattr(self.ship, "x", 0.0))

    @property
    def ship_y(self) -> float:
        """Metres north of the start."""
        dyn = getattr(self.ship, "dyn", None)
        if dyn is not None:
            return float(dyn.y)
        return float(getattr(self.ship, "y", 0.0))

    @property
    def ship_x_km(self) -> float:
        return self.ship_x / 1000.0

    @property
    def ship_y_km(self) -> float:
        return self.ship_y / 1000.0

    @property
    def position(self) -> Any:
        """Where she is on the sphere (spec M5 §9): the truth; None on the endless plane."""
        return getattr(self, "_position", None)

    @property
    def tide_height_m(self) -> float:
        """The tide's height above the chart's datum at the ship now (spec M5 §16)."""
        state = getattr(self, "tide_state", None)
        return float(state.height_m) if state is not None else 0.0

    @property
    def at_anchor(self) -> bool:
        tackle = (getattr(self.ship, "extra", None) or {}).get("ground_tackle")
        return bool(tackle) and tackle.at_anchor()

    @property
    def heading_deg(self) -> float:
        return units.rad_to_deg(float(self.ship.heading)) % 360.0

    # -- her persons (package 84, step 2; the registry's views) -------------------------

    @property
    def company(self) -> list[Any]:
        """The persons she keeps (her muster's named few and whoever her World made),
        wherever each is now: the registry's list for her."""
        return self.world.registry.company(self.id)

    @property
    def aboard(self) -> list[Any]:
        """The persons in her now, hers or another hull's."""
        return self.world.registry.aboard(self.id)

    # -- the World's, forwarded -------------------------------------------------------

    def record(self, *args: Any, **kw: Any) -> Any:
        """A line of her log, by the World's `record` with this hull current."""
        with self.world.as_hull(self):
            return self.world.record(*args, **kw)

    def submit(self, *args: Any, **kw: Any) -> Any:
        """An order of hers, by the World's `submit` with this hull current."""
        with self.world.as_hull(self):
            return self.world.submit(*args, **kw)

    @property
    def readings(self) -> Any:
        """The readings registry's view of her now (`World.readings`)."""
        with self.world.as_hull(self):
            return self.world.readings

    @property
    def daylight(self) -> str:
        with self.world.as_hull(self):
            return self.world.daylight


for _name in SHARED_FIELDS:
    setattr(Hull, _name, delegated("world", _name))
del _name


def lift_old_state(world: Any, state: dict[str, Any]) -> dict[str, Any]:
    """The converter for a checkpoint written before step 1 (`World.__setstate__`): the
    per-ship fields lifted off the World's pickled dict into a Hull set as `own`, the
    hull's id the vessel's where the World is a crewed ship's (`CrewedWorld.vessel`) and
    the player's ship's otherwise. Returns the state to set; a state that holds `own`
    already is returned as it is."""
    if "own" in state:
        # a checkpoint of steps 1 to 5: `own` on the dict, which step 6 keeps as `_own`
        # behind the `own` property; the fields that became hers at step 6 lifted too
        hull = state.pop("own")
        for name in ("seed", "scenario", "rng", "vessels", "vessel"):
            if name in state and name not in hull.__dict__:
                hull.__dict__[name] = state.pop(name)
        state["_own"] = hull
        return state
    if "_own" in state:
        return state
    vessel = state.get("vessel")
    hull = Hull.__new__(Hull)
    hull.world = world
    hull.id = str(getattr(vessel, "id", "") or own_id())
    for name in PER_SHIP_FIELDS + ("vessel",):
        if name in state:
            hull.__dict__[name] = state.pop(name)
    state["_own"] = hull
    return state
