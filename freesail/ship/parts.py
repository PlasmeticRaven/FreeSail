"""Runtime parts: the state of every spar, sail and line, and the hull's motion.

Specs (schema.py) say what a part *is*. Parts here say what state it is *in*:
set or furled, braced to what angle, how loaded, how worn. Physics reads
these; evolutions and level-0 orders change them.

Milestone 3b (docs/TechnicalSpec-M3b.md §6) makes canvas a thing. A sail is
made of canvas of a number (`Sail.canvas_no`, 1 the heaviest) whose strength
Luce's Appendix E gives, and it has a condition that wears with use; a worn
sail bears less than a new one (`Sail.effective_cloth_rating_kn`), and the
strain model judges it against that. The sail room (`SailRoom`, reached by
`sail_room(ship)`) holds the sails that are not bent: the second sail of a
kind, the heavy-weather sails, the storm canvas and the occasional sails,
each with its canvas number and condition. Bending draws a sail from it and
unbending returns one to it; nothing mends canvas until milestone 8.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from freesail import units
from freesail.ship.schema import HullSpec, LineSpec, SailSpec, SparSpec

# ---------------------------------------------------------------------------
# Canvas (spec 3b §6.1 and §6.2)
# ---------------------------------------------------------------------------

# The strength of flax canvas by number: the pounds a strip one inch wide bears, cut
# crosswise of the cloth. Luce 1884, App. E pp. 610-611, read from the page image
# (docs/references/Tables.md §2). Nos. 8 and 9 were tested on strips an inch and a quarter
# wide; their printed 300 and 280 lb are reduced to the inch here, as Tables.md does.
CANVAS_CROSSWISE_LB_PER_IN: dict[int, float] = {
    1: 470.0,
    2: 420.0,
    3: 370.0,
    4: 340.0,
    5: 320.0,
    6: 300.0,
    7: 280.0,
    8: 300.0 / 1.25,  # 240
    9: 280.0 / 1.25,  # 224
}

# The number the cloth ratings are anchored on: courses and topsails are of No. 2 (Luce
# 1884 ch. X p. 171, Tables.md §1; Steel 1794 vol. I, 'Main-course', 'Main-topsail').
WORKING_CANVAS_NO = 2

# The cloth rating of No. 2 canvas, kN per m2 of sail: the rating milestone 2 gave courses
# and topsails (tools/gen_ships.py, the 'course' and 'topsail' rows of CLOTH_KN_PER_M2 as
# it was), kept so that every sail of No. 2 keeps its rating exactly (spec 3b §6.1). Every
# other number scales from it by the strengths above.
# No. 2 canvas. Milestone 2's tuned light-sail ratings divided by Luce App. E's strengths put
# No. 2 at 0.36 to 0.44 kN/m2; truth 27 (a worn royal blows out before its yard) holds from
# 0.30 to 0.36. Set at 3b integration; the first draft's 0.9 was an untuned default (TuningNotes).
CLOTH_KN_PER_M2_NO2 = 0.36

# What worn canvas keeps: a sail at condition 0 bears this share of its new rating, a new
# one all of it, in a straight line between (spec 3b §6.2: the effective rating is
# cloth_rating * (0.4 + 0.6 * condition / 100)).
WORN_CLOTH_STRENGTH = 0.4

# Made-up sails in the sail room of a ship whose file lists none (milestone 3, package 19:
# the count the M3 sail scripts used when the ship file gives no stores; judgement).
DEFAULT_SPARE_SAILS = 3


def canvas_strength(canvas_no: int) -> float:
    """The crosswise strength of this canvas relative to No. 2 (1.12 for No. 1, 0.57 for No. 8)."""
    return CANVAS_CROSSWISE_LB_PER_IN[canvas_no] / CANVAS_CROSSWISE_LB_PER_IN[WORKING_CANVAS_NO]


def cloth_rating_for(area_m2: float, canvas_no: int) -> float:
    """A sail's cloth rating, kN, from its area and canvas (spec 3b §6.1): No. 2 canvas at
    CLOTH_KN_PER_M2_NO2 a square metre, other numbers in proportion to their strength."""
    return round(CLOTH_KN_PER_M2_NO2 * canvas_strength(canvas_no) * area_m2, 1)


def worn_cloth_fraction(condition: float) -> float:
    """The share of its new strength a sail of this condition (0..100) still bears."""
    c = min(max(condition, 0.0), 100.0) / 100.0
    return WORN_CLOTH_STRENGTH + (1.0 - WORN_CLOTH_STRENGTH) * c


class SailState(StrEnum):
    FURLED = "furled"  # stowed on its spar
    IN_THE_GEAR = "in_the_gear"  # hauled up by clewlines and buntlines, not furled
    LOOSED = "loosed"  # gaskets off, hanging
    SHEETED = "sheeted"  # sheets home but not hoisted (topsails) / not fully drawing
    SET = "set"  # drawing
    BLOWN_OUT = "blown_out"  # cloth gone
    UNBENT = "unbent"  # no sail on the yard: unbent and sent down to the sail room
    GOOSE_WINGED = "goose_winged"  # a course or topsail with the lee clew hauled up, half drawing


class LineState(StrEnum):
    BELAYED = "belayed"
    FREE = "free"  # let go, running
    PARTED = "parted"


@dataclass
class Part:
    id: str
    cls: str
    rating_kn: float
    condition: float = 100.0  # 0..100
    load_kn: float = 0.0  # current load, set by physics each substep
    wrecked: bool = False

    @property
    def strain_ratio(self) -> float:
        return self.load_kn / self.rating_kn if self.rating_kn > 0 else 0.0


@dataclass
class Spar(Part):
    x_m: float = 0.0
    height_m: float = 0.0
    length_m: float = 0.0
    parent: str | None = None
    side: str | None = None
    brace_limit: float = 0.0  # radians, for yards
    rake: float = 0.0  # radians, for masts: positive aft, negative forward
    brace_angle: float = 0.0  # radians; 0 square, +ve = braced up for the starboard tack
    sent_down: bool = False  # struck below (topgallant masts in a gale)
    rigged_out: bool = True  # studding sail booms: run out along the yard, ready for the sail

    @classmethod
    def from_spec(cls, s: SparSpec) -> Spar:
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=s.rating_kn or 0.0,
            x_m=s.x_m or 0.0,
            height_m=s.height_m or 0.0,
            length_m=s.length_m or 0.0,
            parent=s.parent,
            side=s.side,
            brace_limit=units.deg_to_rad(s.brace_limit_deg or 0.0),
            rake=units.deg_to_rad(s.rake_deg or 0.0),
        )

    @property
    def is_yard(self) -> bool:
        return self.cls in {"yard", "lug_yard", "lateen_yard"}


@dataclass
class Sail(Part):
    area_m2: float = 0.0
    x_m: float = 0.0
    centre_height_m: float = 0.0
    reef_bands: int = 0
    side: str | None = None
    roles: dict[str, str] = field(default_factory=dict)
    cloth_rating_kn: float = 0.0
    canvas_no: int | None = None  # the canvas of the sail now bent (spec 3b §6.1)
    in_place_of: str | None = None  # the sail this one is bent instead of (spec 3b §6.4)
    state: SailState = SailState.FURLED
    reefs: int = 0
    sheet_angle: float = 0.0  # radians from the centreline; fore-and-aft sails
    # physics outputs, refreshed each substep
    backed: bool = False
    force_kn: float = 0.0
    thrust_kn: float = 0.0
    side_force_kn: float = 0.0
    area_effective_m2: float = 0.0

    @classmethod
    def from_spec(cls, s: SailSpec) -> Sail:
        cloth = s.cloth_rating_kn if s.cloth_rating_kn is not None else 0.9 * s.area_m2
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=cloth,
            area_m2=s.area_m2,
            x_m=s.x_m,
            centre_height_m=s.centre_height_m,
            reef_bands=s.reef_bands,
            side=s.side,
            roles=dict(s.roles),
            cloth_rating_kn=cloth,
            canvas_no=s.canvas_no,
            in_place_of=s.in_place_of,
            # storm canvas and the occasional sails start the voyage in the sail room
            state=SailState.FURLED if s.bent else SailState.UNBENT,
        )

    @property
    def effective_cloth_rating_kn(self) -> float:
        """What the cloth bears now (spec 3b §6.2): its rating times the share a sail of
        its condition keeps, from 0.4 worn out to all of it new."""
        return self.rating_kn * worn_cloth_fraction(self.condition)

    @property
    def strain_ratio(self) -> float:
        """Load over the effective cloth rating: a worn sail strains sooner than a new one
        and blows out at BLOW_OUT_RATIO of what it bears now (spec 3b §6.2)."""
        effective = self.effective_cloth_rating_kn
        return self.load_kn / effective if effective > 0 else 0.0

    def bend_canvas(self, canvas_no: int | None, condition: float) -> None:
        """Bend a sail of this canvas and condition to the part: the cloth rating follows the
        number by Luce's strengths (a heavy No. 1 topsail in place of the No. 2 bears 1.12 of
        it), and the condition is the new sail's."""
        if canvas_no is not None and self.canvas_no is not None and canvas_no != self.canvas_no:
            factor = canvas_strength(canvas_no) / canvas_strength(self.canvas_no)
            self.cloth_rating_kn *= factor
            self.rating_kn *= factor
        if canvas_no is not None:
            self.canvas_no = canvas_no
        self.condition = min(max(condition, 0.0), 100.0)

    @property
    def is_set(self) -> bool:
        return self.state is SailState.SET and not self.wrecked

    @property
    def is_fore_and_aft(self) -> bool:
        return self.cls in {"gaff", "jibheaded", "lug", "lateen", "sprit"}

    def describe_state(self) -> str:
        if self.wrecked:
            return "wrecked"
        if self.state is SailState.SET and self.reefs:
            return f"set, {self.reefs} reef{'s' if self.reefs > 1 else ''}"
        return self.state.value.replace("_", " ")


@dataclass
class Line(Part):
    of: str = ""
    side: str | None = None
    state: LineState = LineState.BELAYED
    hauled: float = 1.0  # 0 = fully eased, 1 = hauled home (halyards, sheets)

    @classmethod
    def from_spec(cls, ln: LineSpec) -> Line:
        return cls(id=ln.id, cls=ln.cls, rating_kn=ln.rating_kn or 0.0, of=ln.of, side=ln.side)

    @property
    def is_standing(self) -> bool:
        return self.cls in {"stay", "shroud", "backstay"}


# ---------------------------------------------------------------------------
# The sail room (spec 3b §6.3)
# ---------------------------------------------------------------------------

# Words for a sail's condition in the log and the muster (judgement: a sail that has done a
# few weeks' duty is still "new" to a purser; below half its cloth is thin).
CONDITION_WORDS: tuple[tuple[float, str], ...] = (
    (95.0, "new"),
    (75.0, "sound"),
    (50.0, "worn"),
    (25.0, "much worn"),
    (0.0, "worn out"),
)

# The ship file's groups that name the sail room's own canvas (tools/gen_ships.py).
STORM_GROUP = "storm canvas"
OCCASIONAL_GROUP = "occasional sails"


def condition_words(condition: float) -> str:
    for floor, words in CONDITION_WORDS:
        if condition >= floor:
            return words
    return CONDITION_WORDS[-1][1]


@dataclass
class SpareSail:
    """A sail in the sail room: made for one sail of the ship (`kind`, the sail's id), of a
    canvas number, and worn to a condition. A `kind` of None is a made-up sail the
    sailmaker fits to any yard: the room of a ship whose file lists no sails."""

    kind: str | None
    canvas_no: int | None = None
    condition: float = 100.0


@dataclass
class SailRoom:
    """The sails that are not bent. `names` gives a sailor's name for each sail of the ship,
    `working` each sail's canvas number as the ship file makes it, and `category` which
    kinds are storm canvas or the occasional light-weather sails, for the muster."""

    sails: list[SpareSail]
    names: dict[str, str] = field(default_factory=dict)
    working: dict[str, int | None] = field(default_factory=dict)
    category: dict[str, str] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.sails)

    def fitting(self, kind: str) -> list[SpareSail]:
        """The sails in the room that can be bent in the place of sail `kind`."""
        return [s for s in self.sails if s.kind == kind or s.kind is None]

    def number_of(self, spare: SpareSail, kind: str) -> int | None:
        """The canvas number of a spare as bent to `kind` (a made-up sail is of its number)."""
        return spare.canvas_no if spare.canvas_no is not None else self.working.get(kind)

    def choose(
        self, kind: str, canvas_no: int | None = None, heavy: bool = False
    ) -> SpareSail | None:
        """The sail to bend in the place of `kind`: of the number named if one is, else the
        heaviest heavy-weather sail if `heavy`, else the best of the working number, else the
        best there is. "Best" is the highest condition; the heavy-weather sails are kept for
        a blow and come up for fine weather only when nothing else is left."""
        fits = self.fitting(kind)
        working = self.working.get(kind)
        if canvas_no is not None:
            fits = [s for s in fits if self.number_of(s, kind) == canvas_no]
        elif heavy:
            if working is None:
                return None
            fits = [s for s in fits if (self.number_of(s, kind) or working) < working]
            fits.sort(key=lambda s: self.number_of(s, kind) or working)  # heaviest first
        else:
            same = [s for s in fits if self.number_of(s, kind) in (working, None)]
            fits = same or fits
        if not fits:
            return None
        return max(fits, key=lambda s: s.condition)  # the first of equals: stable

    def take(self, spare: SpareSail) -> None:
        for i, s in enumerate(self.sails):
            if s is spare:
                del self.sails[i]
                return
        raise ValueError("that sail is not in the sail room")

    def stow(self, spare: SpareSail) -> None:
        self.sails.append(spare)

    # -- words ---------------------------------------------------------------

    def name(self, kind: str | None) -> str:
        if kind is None:
            return "made-up sail"
        return self.names.get(kind, kind.replace("_", " ").replace(".", " "))

    def describe(self, spare: SpareSail, kind: str | None = None) -> str:
        """'the fore topsail, No. 1 canvas, new' (for the log and the inventory)."""
        kind = spare.kind or kind
        no = self.number_of(spare, kind) if kind else spare.canvas_no
        what = f"the {self.name(kind)}"
        if no is not None:
            what += f", No. {no} canvas"
        return f"{what}, {condition_words(spare.condition)}"

    def _kind_of(self, spare: SpareSail) -> str:
        """'storm', 'occasional', 'heavy', 'working' or 'made-up'."""
        if spare.kind is None:
            return "made-up"
        cat = self.category.get(spare.kind)
        if cat:
            return cat
        working = self.working.get(spare.kind)
        if working is not None and spare.canvas_no is not None and spare.canvas_no < working:
            return "heavy"
        return "working"

    def _names(self, spares: list[SpareSail]) -> str:
        names = [self.name(s.kind) for s in spares]
        if len(names) <= 1:
            return "".join(names)
        return ", ".join(names[:-1]) + " and " + names[-1]

    def muster_line(self) -> str:
        """One line for the muster: what the sail room holds, by kind of canvas."""
        n = len(self.sails)
        if n == 0:
            return "Sail room: empty; there is no spare canvas aboard."
        by: dict[str, list[SpareSail]] = {}
        for s in self.sails:
            by.setdefault(self._kind_of(s), []).append(s)
        parts: list[str] = []
        if by.get("working"):
            k = len(by["working"])
            parts.append(f"{k} spare{'s' if k != 1 else ''} of the working canvas")
        if by.get("made-up"):
            k = len(by["made-up"])
            parts.append(f"{k} made-up sail{'s' if k != 1 else ''}")
        if by.get("heavy"):
            parts.append(f"for heavy weather the {self._names(by['heavy'])}")
        if by.get("storm"):
            parts.append(f"the storm canvas ({self._names(by['storm'])})")
        if by.get("occasional"):
            parts.append(f"for light fair winds the {self._names(by['occasional'])}")
        line = f"Sail room: {n} sail{'s' if n != 1 else ''}, " + "; ".join(parts)
        worst = min(self.sails, key=lambda s: s.condition)
        if worst.condition < CONDITION_WORDS[0][0]:
            line += (
                f"; the most worn, the {self.name(worst.kind)}, {condition_words(worst.condition)}"
            )
        return line + "."

    def inventory_lines(self) -> list[str]:
        """The `the sail room` query: every sail in the room, by kind of canvas."""
        if not self.sails:
            return ["The sail room is empty; there is no spare canvas aboard."]
        n = len(self.sails)
        lines = [f"The sail room holds {n} sail{'s' if n != 1 else ''}."]
        heads = (
            ("working", "Spares of the working canvas"),
            ("made-up", "Made-up sails, for any yard"),
            ("heavy", "For heavy weather"),
            ("storm", "Storm canvas"),
            ("occasional", "For light fair winds"),
        )
        by: dict[str, list[SpareSail]] = {}
        for s in self.sails:
            by.setdefault(self._kind_of(s), []).append(s)
        for key, head in heads:
            spares = by.get(key)
            if spares:
                lines.append(f"{head}: " + "; ".join(self.describe(s)[4:] for s in spares) + ".")
        return lines


def _sailor_name(ship: Any, part_id: str) -> str:
    """A sailor's name for a part: the ship file's first plain alias, else the id in words
    with the side first (as evolutions.runner.part_name, which this module cannot import)."""
    for alias, target in getattr(ship, "aliases", {}).items():
        if target == part_id and not alias.startswith("the "):
            return alias
    words = part_id.replace("_", " ").split(".")
    if len(words) > 1 and words[-1] in ("starboard", "larboard"):
        words = [words[-1], *words[:-1]]
    return " ".join(words)


def _stores_of(ship: Any) -> Any:
    crew = getattr(getattr(ship, "spec", None), "crew", None)
    return getattr(crew, "stores", None) if crew is not None else None


def sail_room(ship: Any) -> SailRoom:
    """The ship's sail room, kept in `ship.extra["sail_room"]`.

    Made on first use from the ship file's `crew.stores.sails` list (spec 3b §6.3); a ship
    whose file gives only a count (`spare_sails`, milestone 3) has that many made-up sails
    that fit any yard, and a ship with no stores DEFAULT_SPARE_SAILS of them. The stores are
    read defensively: they may be a StoresSpec, a mapping or any object with the fields.
    `ship.extra["spare_sails"]` is kept as the count, for anything that reads it; the ship's
    crew, when mustered, is given the room for its muster line."""
    room = ship.extra.get("sail_room")
    if not isinstance(room, SailRoom):
        stores = _stores_of(ship)
        get = stores.get if isinstance(stores, dict) else lambda k: getattr(stores, k, None)
        listed = get("sails") if stores is not None else None
        if listed is not None:
            spares = [
                SpareSail(
                    kind=str(e["kind"] if isinstance(e, dict) else e.kind),
                    canvas_no=e.get("canvas_no") if isinstance(e, dict) else e.canvas_no,
                    condition=float(
                        e.get("condition", 100.0) if isinstance(e, dict) else e.condition
                    ),
                )
                for e in listed
            ]
        else:
            count = get("spare_sails") if stores is not None else None
            ok = isinstance(count, int | float) and not isinstance(count, bool) and count >= 0
            spares = [
                SpareSail(kind=None) for _ in range(int(count) if ok else DEFAULT_SPARE_SAILS)
            ]
        groups = getattr(ship, "groups", {}) or {}
        category = {sid: "storm" for sid in groups.get(STORM_GROUP, [])}
        category.update({sid: "occasional" for sid in groups.get(OCCASIONAL_GROUP, [])})
        room = SailRoom(
            sails=spares,
            names={sid: _sailor_name(ship, sid) for sid in ship.sails},
            working={sid: s.canvas_no for sid, s in ship.sails.items()},
            category=category,
        )
        ship.extra["sail_room"] = room
    ship.extra["spare_sails"] = len(room)
    crew = ship.extra.get("crew")
    if crew is not None and getattr(crew, "sail_room", None) is not room:
        crew.sail_room = room
    return room


@dataclass
class Hull:
    spec: HullSpec
    water_in_well_m: float = 0.0

    @property
    def length(self) -> float:
        return self.spec.length_waterline_m

    @property
    def hull_speed(self) -> float:
        """Metres per second. Default 1.34 * sqrt(LWL in feet) knots."""
        if self.spec.hull_speed_kn is not None:
            return units.knots_to_ms(self.spec.hull_speed_kn)
        return units.knots_to_ms(1.34 * math.sqrt(units.m_to_feet(self.spec.length_waterline_m)))

    @property
    def lateral_area(self) -> float:
        if self.spec.lateral_area_m2 is not None:
            return self.spec.lateral_area_m2
        return 0.75 * self.spec.length_waterline_m * self.spec.draught_m

    @property
    def wetted_area(self) -> float:
        """A rough estimate from principal dimensions (Denny-Mumford style)."""
        L, B, T = self.spec.length_waterline_m, self.spec.beam_m, self.spec.draught_m
        return L * (1.7 * T + 0.7 * B)


class HelmMode(StrEnum):
    HEADING = "heading"  # steer a compass heading
    RUDDER = "rudder"  # hold a rudder angle (helm a-lee, hard over)
    FULL_AND_BY = "full_and_by"  # keep her as close to the wind as she will lie, full


@dataclass
class Dynamics:
    """The ship's motion state. Physics owns the numbers; orders set the targets."""

    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0  # radians clockwise from north
    u: float = 0.0  # surge, m/s (forward +)
    v: float = 0.0  # sway, m/s (to starboard +)
    r: float = 0.0  # yaw rate, rad/s (clockwise +)
    heel: float = 0.0  # radians, +ve = heeled to starboard
    rudder: float = 0.0  # radians, +ve = rudder to starboard (turns the ship to starboard)
    helm_mode: HelmMode = HelmMode.HEADING
    target_heading: float = 0.0
    target_rudder: float = 0.0
    steady: bool = True
    # readings refreshed by physics each tick
    speed: float = 0.0  # through the water, m/s
    leeway: float = 0.0  # radians, +ve = set to starboard
    weather_helm: float = 0.0  # radians, positive when she wants to round up (weather helm)
    apparent_wind_angle: float = 0.0  # radians, +ve on the starboard bow
    apparent_wind_speed: float = 0.0

    @property
    def tack(self) -> str:
        """The side the wind is on: 'starboard' or 'larboard'."""
        return "starboard" if self.apparent_wind_angle >= 0 else "larboard"

    def state(self) -> dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "heading": self.heading,
            "speed": self.speed,
            "u": self.u,
            "v": self.v,
            "r": self.r,
            "leeway": self.leeway,
            "heel": self.heel,
            "rudder": self.rudder,
            "weather_helm": self.weather_helm,
            "helm_mode": self.helm_mode.value,
            "target_heading": self.target_heading,
            "apparent_wind_angle": self.apparent_wind_angle,
            "apparent_wind_speed": self.apparent_wind_speed,
        }
