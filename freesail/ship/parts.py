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

Package 30b (milestone 5) keeps the spare spars the same way: the booms (`Booms`, reached
by `booms(ship)`) hold them by class, with the counts the ship file gives, and a spar that
has carried away is shifted for a spare of its class from them.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from freesail import units
from freesail.ship.schema import (
    GUN_KINDS,
    FitSpec,
    GroundTackleSpec,
    GunSpec,
    HullSpec,
    LineSpec,
    SailSpec,
    SparSpec,
)

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
# No. 2 at 0.36 to 0.44 kN/m2; truth 27 (a worn royal blows out before its yard, a new one
# loses the yard) held from 0.30 to 0.36 on the milestone 2 square curve and from 0.30 to
# 0.32 on the 3b curve (its peak five degrees later). Set at 3b integration to 0.32; the first
# draft's 0.9 was an untuned default (TuningNotes).
CLOTH_KN_PER_M2_NO2 = 0.32

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


# Storm canvas is rated for the wind it is cut for (package 45, Part B item 7; the gale
# trials of 37p and the owner's runs: the mizzen storm staysail "split and blew out of the
# bolt-ropes" at 10:01 in a gust of the whole gale). Rated by the square metre as the
# working canvas is, at 1.12 of No. 2 (Luce 1884 App. E), a storm staysail of 36 m2 bore
# 12.9 kN and the model's force on it reached that at 40 knots apparent, so it was blowing
# out, by the strain's rule, at 55 to 60 knots in the wind it exists for. Luce 1884 ch. X:
# "Storm-sails are made of the strongest canvas", and they are the sail she lies to under
# in a whole gale (Luce 1866's journal scale, "10. Whole gale; close reefed main topsail",
# "11. Storm"; Luce 1884 ch. XXIX, 'Lying to'). So a storm sail's cloth rating is the
# model's own force on a jib-headed sail at STORM_CANVAS_APPARENT_KN of apparent wind
# (seventy knots: force 11, with the way she makes lying to; judgement on the scale),
# divided by STORM_CANVAS_RATIO (1.35: the sail wears there and stands, and blows out for
# certain, at BLOW_OUT_RATIO, at about eighty knots apparent). The force per square metre
# is the model's at a jib-headed sail's working angle (physics/sails.py: 0.536 kN/m2 at 46
# knots apparent, measured in the probe of docs/dev/TuningNotes.md, package 45), scaled
# as the square of the wind. The jib and the fore topmast staysail keep their ratings
# and 37p's rule (taken in at three quarters of their rating).
STORM_CANVAS_APPARENT_KN = 70.0
STORM_CANVAS_RATIO = 1.35
STORM_FORCE_KN_PER_M2_AT_46_KN = 0.536


def storm_cloth_rating_for(area_m2: float) -> float:
    """A storm sail's cloth rating, kN: what stands STORM_CANVAS_APPARENT_KN apparent at a
    strain ratio of STORM_CANVAS_RATIO (above)."""
    force = STORM_FORCE_KN_PER_M2_AT_46_KN * (STORM_CANVAS_APPARENT_KN / 46.0) ** 2 * area_m2
    return round(force / STORM_CANVAS_RATIO, 1)


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


# The spar classes that are rigged in and out (spec 3b §7): the studding sail booms, the
# ringtail's among them. A gaff sail's `boom` is not: the water sail spread under the main
# boom has nothing to rig out.
RIGGED_IN_CLASSES = frozenset({"studdingsail_boom"})


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
    # Studding sail booms (milestone 3b, spec 3b §7): run out along the yard, ready for the
    # sail. A boom starts rigged in, as at sea: it is rigged out only to set its sail (Luce
    # 1884, ch. XXIII: "Set taut! Rig out! Hoist away!"; RigGeometryNotes §5). Only the
    # classes in RIGGED_IN_CLASSES take this default from the ship file; a gaff sail's
    # boom is never rigged in, and reads as out (`from_spec`).
    rigged_out: bool = False
    # Milestone 3b (spec 3b §3). `brace_limit` above is the limit the rigging allows
    # now, and every reader reads it; `rigged_brace_limit` is the ship file's, with the
    # lower rigging as rigged. They differ only for a lower yard whose mast has its
    # catharpins swiftered in (see `sync_catharpins`).
    rigged_brace_limit: float = 0.0  # radians, for yards: the ship file's brace_limit_deg
    swiftered_in: bool = False  # lower masts: the catharpins swiftered in
    # Lower masts: the strain model's allowance for the catharpins, set by strain.py each
    # tick while they are swiftered in; 1.0 when the lower rigging stands as rigged.
    rating_factor: float = 1.0
    # A running bowsprit (package 32b, spec M5 §23: a cutter's, run in and out on the deck
    # through the gammoning iron and fidded at its reefs). `running` marks it; `length_m`
    # is its outboard length now, between `housed_length_m` (reefed) and `full_length_m`
    # (rigged out), which the two bowsprit evolutions move it between; `rigged_out` says
    # which it stands at. A standing bowsprit has `running` false and reads rigged out.
    running: bool = False
    housed_length_m: float = 0.0
    full_length_m: float = 0.0
    # A gaff sail's boom (package 32e): the breadth of the horse its sheet travels on
    # (Steel 1794 vol. I, p. 167, HORSE); the sheet's geometry reads it (evolutions/trim.py).
    # 0: no horse given; the geometry takes a quarter of the boom's length.
    horse_m: float = 0.0
    # A jury mast (package 73, spec M7 §14): a lower mast carried away standing again on a
    # spare topmast stepped in its stump, at a share of its rating (`rating_whole_kn` the
    # file's figure, kept for the dockyard); dataclass defaults, so older saves load
    jury: bool = False
    rating_whole_kn: float = 0.0

    @classmethod
    def from_spec(cls, s: SparSpec) -> Spar:
        limit = units.deg_to_rad(s.brace_limit_deg or 0.0)
        running = bool(s.running)
        rigged_out = s.rigged_out if s.rigged_out is not None else s.cls not in RIGGED_IN_CLASSES
        full = s.length_m or 0.0
        housed = s.housed_length_m or 0.0
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=s.rating_kn or 0.0,
            x_m=s.x_m or 0.0,
            height_m=s.height_m or 0.0,
            # a running bowsprit the file starts reefed stands at its housed length
            length_m=housed if running and not rigged_out else full,
            parent=s.parent,
            side=s.side,
            brace_limit=limit,
            rake=units.deg_to_rad(s.rake_deg or 0.0),
            rigged_brace_limit=limit,
            # the ship file's starting state where it gives one; otherwise a studding sail
            # boom (the ringtail's among them) starts rigged in and every other spar reads out
            rigged_out=rigged_out,
            running=running,
            housed_length_m=housed if running else 0.0,
            full_length_m=full if running else 0.0,
            horse_m=s.horse_m or 0.0,
        )

    @property
    def is_yard(self) -> bool:
        """A yard that is braced. A lug's yard has no braces and no lifts ("les ralingues
        en font l'office", Forfait 1788 p. 53): its sail is trimmed by the sheet, as a
        fore-and-aft sail's is (package 43b), so it is no yard of the braces' orders."""
        return self.cls in {"yard", "lateen_yard"}

    @property
    def strain_ratio(self) -> float:
        rating = self.rating_kn * self.rating_factor
        return self.load_kn / rating if rating > 0 else 0.0


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
    # A dipping lug (package 43b): the side of its mast its yard and cloth lie on now,
    # 'starboard' or 'larboard' (None: not yet hoisted on a side, as a sail furled or
    # drawn for a polar). On the lee side it stands clear of the mast; on the weather side,
    # after a tack with no dip, it lies against the mast and draws badly
    # (`physics.sails.LUG_AGAINST_MAST_AREA`) until it is dipped (dip_lug.yaml).
    dipping: bool = False
    lug_side: str | None = None
    # Package 57: a sail set flying (the lug topsails, the royals of 1794): furled, it is on
    # deck with its yard, sent down whole; its yard is swayed up with it bent when it is set
    # (data/evolutions/set_flying.yaml). A lug topsail's lower lug, to whose yard its clew is
    # sheeted (`sheeted_to`): it lies as that lug lies (evolutions/trim.py, `read_sheet`).
    flying: bool = False
    sheeted_to: str | None = None
    corners_m: list[tuple[float, float]] | None = None  # the cut, for the drawing (package 57)
    # Package 70 (spec M7 §9): the area shot out of the sail, square metres, which the
    # physics takes off its drawing area and the strain off what the cloth bears; nothing
    # mends it until a new sail is bent (the sailmaker's patch is 73's).
    holed_m2: float = 0.0
    state: SailState = SailState.FURLED
    reefs: int = 0
    # A fore-and-aft sail's angle from the centreline, radians: since package 32e (spec M5
    # open item 13) a reading of its sheet, refreshed from the sheet's length hauled through
    # the boom's or the clew's geometry (`evolutions.trim.read_sheet`) whenever the sheet
    # is worked and each time the physics reads the rig, never set on its own. The line
    # holds the trim; this is what the viewer and the log show.
    sheet_angle: float = 0.0
    # physics outputs, refreshed each substep
    backed: bool = False
    # A studding sail with the wind forward of its limit (spec 3b §7): lift going or gone,
    # the cloth shaking in its gear; flogging as the strain model counts it (sails.py).
    shivering: bool = False
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
            dipping=bool(getattr(s, "dipping", False)),
            flying=bool(getattr(s, "flying", False)),
            sheeted_to=getattr(s, "sheeted_to", None),
            corners_m=getattr(s, "corners_m", None),
            # storm canvas and the occasional sails start the voyage in the sail room
            state=SailState.FURLED if s.bent else SailState.UNBENT,
        )

    @property
    def effective_cloth_rating_kn(self) -> float:
        """What the cloth bears now (spec 3b §6.2): its rating times the share a sail of
        its condition keeps, from 0.4 worn out to all of it new."""
        whole = max(0.0, 1.0 - self.holed_share)
        return self.rating_kn * worn_cloth_fraction(self.condition) * whole

    @property
    def holed_share(self) -> float:
        """The share of the sail shot out of it (package 70), 0 to 1."""
        if self.area_m2 <= 0.0:
            return 0.0
        return min(1.0, max(0.0, self.holed_m2 / self.area_m2))

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
        self.holed_m2 = 0.0  # a new sail bent is whole (package 70)

    @property
    def is_set(self) -> bool:
        return self.state is SailState.SET and not self.wrecked

    @property
    def is_fore_and_aft(self) -> bool:
        return self.cls in {"gaff", "jibheaded", "lug", "lateen", "sprit"}

    @property
    def sent_down(self) -> bool:
        """A flying sail stowed: on deck with its yard (package 57)."""
        return self.flying and self.state is SailState.FURLED

    def describe_state(self) -> str:
        if self.wrecked:
            return "wrecked"
        if self.sent_down:
            return "sent down"
        if self.state is SailState.SET and self.reefs:
            return f"set, {self.reefs} reef{'s' if self.reefs > 1 else ''}"
        return self.state.value.replace("_", " ")


@dataclass
class Line(Part):
    of: str = ""
    side: str | None = None
    state: LineState = LineState.BELAYED
    # 0 = fully eased, 1 = hauled home (halyards, square sails' sheets). A fore-and-aft
    # sail's sheet (package 32e): the fraction of its scope hauled in, 1 flat aft (the
    # sail at its class's floor angle), 0 eased right off (the sail squared off as far as
    # its class allows); the sail's angle follows by the boom's or the clew's geometry
    # (evolutions/trim.py).
    hauled: float = 1.0
    # A sheet's purchase: the parts its fall is rove with (a threefold purchase: 3). A
    # fathom of the fall eased moves the boom a third of a fathom.
    parts: int = 1
    # A single sheet (a boom's) held over to one side by hand or tackle, "the spanker boom
    # well over to the windward" (Luce 1866, ch. XXIV, 'Tacking'): the sail lies on that
    # side whatever the wind does, and is aback when the wind is on it. None: the sail
    # lies to leeward, as a sheet lets it. A sail with a sheet each side needs no such
    # flag: it lies on the side whose sheet is hauled.
    held_side: str | None = None
    # A preventer rove beside it (package 73, spec M7 §14: the preventer braces and
    # backstays and the chain slings before an action): when the line parts or is shot
    # away the preventer takes the strain and the line keeps its office, the preventer
    # consumed (`physics.strain._part_line`); a dataclass default, so older saves load
    preventer: bool = False

    @classmethod
    def from_spec(cls, ln: LineSpec) -> Line:
        line = cls(
            id=ln.id,
            cls=ln.cls,
            rating_kn=ln.rating_kn or 0.0,
            of=ln.of,
            side=ln.side,
            parts=max(int(ln.parts or 1), 1),
        )
        if line.cls == "bowline":
            # Rove, with its fall clear on deck, but not hauled out: a bowline is hauled
            # on a wind by hands and let go again when the yards come in (spec 3b §4).
            line.state = LineState.FREE
        return line

    @property
    def is_standing(self) -> bool:
        return self.cls in {"stay", "shroud", "backstay"}

    @property
    def bowline_hauled(self) -> bool:
        """A bowline hauled out and belayed, holding its sail's leech taut forward (spec
        3b §4). Eased, let go, slacked or parted, it holds nothing."""
        return (
            self.cls == "bowline" and self.state is LineState.BELAYED and self.hauled >= 1.0 - 1e-9
        )


# ---------------------------------------------------------------------------
# The guns (spec M7 §7; package 70)
# ---------------------------------------------------------------------------


class Charge(StrEnum):
    """What a gun is loaded with. `double` is two round shot on one cartridge (the
    double-shotted broadside at pistol shot); `blank` a cartridge and a wad alone, the
    signal gun and the gun to leeward (Falconer 1780, GUN; the Regulations, the gun to
    leeward as the signal of distress)."""

    ROUND = "round"
    CHAIN = "chain"
    GRAPE = "grape"
    DOUBLE = "double"
    BLANK = "blank"


# The words of a gun's kind, for the log and the readings.
GUN_KIND_WORDS = {"long": "long gun", "carronade": "carronade", "swivel": "swivel"}


@dataclass
class Gun(Part):
    """A gun as a part of the graph (spec M7 §7): its kind, calibre and place, its load
    state (empty; loaded with round, chain, grape or double; run in or out; primed), its
    elevation and train, and whether it is dismounted (a part out of the bill, as a sprung
    spar is out of the sail plan). `condition` is the carriage's, the tackles' and the
    breeching's together (a shot that strikes the gun wears it before it dismounts it).
    The crew at it is the quarter bill's (`crew/quarters.py`); the cycle that serves it is
    `combat/guns.py`'s; the shot it throws `combat/shot.py`'s."""

    kind: str = "long"
    pounder: float = 0.0
    place: str = "broadside"
    number: int | None = None
    side: str | None = None
    x_m: float = 0.0
    height_m: float = 0.0
    crew_n: int = 1  # the men who serve it by the bill
    weight_cwt: float = 0.0
    cast_loose: bool = False  # the breechings cast off and the tackles manned
    loaded: Charge | None = None  # None: empty
    run_out: bool = False
    primed: bool = False
    elevation_deg: float = 0.0  # the quoin: positive is the muzzle raised
    # from abeam (a broadside gun) or from the bow or stern line; a pivot gun's is the
    # relative bearing it points, from the bow, starboard positive, nought secured fore
    # and aft (PROVISIONAL, 2026-10-25)
    train_deg: float = 0.0
    dismounted: bool = False
    fired: int = 0  # rounds fired, for the log and the gunner's count
    # a pivot gun's own arc over either side, degrees off the bow (package 86; None, and a
    # gun pickled before it, the default arc of `combat.guns.pivot_arc`)
    arc_deg: tuple[float, float] | None = None

    @classmethod
    def from_spec(cls, g: GunSpec) -> Gun:
        return cls(
            id=g.id,
            cls=g.kind,
            rating_kn=0.0,
            kind=g.kind,
            pounder=float(g.pounder),
            place=g.place,
            number=g.number,
            side=g.side,
            x_m=float(g.x_m),
            height_m=float(g.height_m),
            crew_n=int(g.crew),
            weight_cwt=float(g.weight_cwt),
            arc_deg=tuple(g.arc_deg) if g.arc_deg is not None else None,
        )

    @property
    def kind_words(self) -> str:
        """'12-pounder carronade', 'long 18-pounder', 'half-pounder swivel'."""
        calibre = _pounder_words(self.pounder)
        if self.kind == "long":
            return f"long {calibre}-pounder"
        return f"{calibre}-pounder {GUN_KIND_WORDS[self.kind]}"

    @property
    def name(self) -> str:
        """The gun's name as the deck says it: 'No. 3 starboard gun', 'the starboard bow
        chaser', 'the stern chaser', 'the No. 2 larboard swivel'."""
        side = f"{self.side} " if self.side else ""
        if self.place == "broadside":
            return f"No. {self.number} {side}gun"
        if self.place in ("bow", "stern"):
            return f"the {side}{self.place} chaser"
        if self.place == "pivot":
            return f"the No. {self.number} pivot gun" if self.number else "the pivot gun"
        n = f"No. {self.number} " if self.number is not None else ""
        return f"the {n}{side}swivel"

    @property
    def serves(self) -> bool:
        """Whether it can be served at all: mounted and whole."""
        return not self.dismounted and not self.wrecked

    @property
    def state_words(self) -> str:
        if self.dismounted:
            return "dismounted"
        if not self.cast_loose:
            return "secured"
        parts = []
        parts.append(f"loaded with {self.loaded.value}" if self.loaded else "empty")
        parts.append("run out" if self.run_out else "run in")
        if self.primed:
            parts.append("primed")
        return ", ".join(parts)

    @property
    def pair_key(self) -> str:
        """The key of the gun crew that serves it: the broadside pair by number, else the
        gun itself (a chaser or a swivel has its own small crew)."""
        if self.place == "broadside":
            return f"gun:{self.number}"
        return f"gun:{self.id}"


def _pounder_words(pounder: float) -> str:
    if pounder == 0.5:
        return "half"
    return f"{pounder:g}"


# The powder below and the filled cartridges (practice and resupply, between packages 72
# and 73; docs/design/Build-PracticeAndResupply.md §1.1, §2).

# A barrel of powder holds a hundred pounds: Falconer 1780, the French glossary, "Baril de
# poudre, a powder-cask, containing an hundred pounds of gun-powder" (l.22563-22564). The
# English barrel's weight is UNVERIFIED.
BARREL_LB = 100.0
# A cartridge's powder as a share of its shot's weight by the gun's kind, until the
# Regulations' Table No. 29 (OCR l.27498-27502, its figures lost in the OCR) is read from
# the page image (package 75). A long gun a third: Falconer 1780, CANNON (from l.4037),
# quoting Robins at l.4826-4831, the present allowance is half the ball in the smaller
# pieces and seven sixteenths in the 32-pounders, and a third or even less would be an
# advantage; that the service charge of 1805 was a third is from memory, UNVERIFIED. A
# carronade a twelfth, from memory, UNVERIFIED (Falconer 1780 is before the carronade). A
# swivel a half, Falconer's smaller pieces (l.4827) applied to a half-pounder (judgement).
CHARGE_SHARE: dict[str, float] = {"long": 1 / 3, "carronade": 1 / 12, "swivel": 1 / 2}
# The powder below at completion, as a share of the filled powder (judgement: the period
# kept most of its powder in the barrels).
RESERVE_SHARE = 0.5
# The man-seconds to fill one cartridge: a fixed part, and a part by the pound of its
# charge (judgement).
FILL_S_BASE = 120.0
FILL_S_PER_LB = 15.0
# The magazine's layout: 1, the cartridges and the rounds fired by calibre (packages 70 to
# 72); 2, the filled cartridges by kind and calibre, with the powder below.
MAGAZINE_LAYOUT = 2


def charge_lb(kind: str, pounder: float) -> float:
    """A cartridge's powder in pounds for a gun of the kind and calibre, to the ounce."""
    share = CHARGE_SHARE.get(kind, CHARGE_SHARE["long"])
    return round(share * float(pounder) * 16.0) / 16.0


def fill_seconds(charge: float) -> float:
    """The man-seconds to fill one cartridge of `charge` pounds."""
    return FILL_S_BASE + FILL_S_PER_LB * float(charge)


def kind_rank(kind: str) -> int:
    """The gun kinds' order (`GUN_KINDS`: long, carronade, swivel), any other after."""
    return GUN_KINDS.index(kind) if kind in GUN_KINDS else len(GUN_KINDS)


def split_by_kind(
    by_calibre: Mapping[float, int], guns: Iterable[Any]
) -> dict[tuple[str, float], int]:
    """Counts by calibre split over the gun kinds of each calibre in proportion to their
    number of guns, by the largest remainder with ties in `GUN_KINDS` order: the long Tom's
    275 cartridges of 12 for one long gun and four carronades are 55 and 220, 100 are 20 and
    80, 101 are 20 and 81. A calibre no gun has keeps its count under the long gun's kind,
    so that nothing is lost (the schema refuses such a fit)."""
    guns_of: dict[float, dict[str, int]] = {}
    for g in guns:
        kinds = guns_of.setdefault(float(g.pounder), {})
        kinds[str(g.kind)] = kinds.get(str(g.kind), 0) + 1
    out: dict[tuple[str, float], int] = {}
    for pounder, count in by_calibre.items():
        p, n = float(pounder), int(count)
        kinds = guns_of.get(p)
        if not kinds:
            out[("long", p)] = out.get(("long", p), 0) + n
            continue
        order = sorted(kinds, key=kind_rank)
        total = sum(kinds.values())
        quota = {k: divmod(n * kinds[k], total) for k in order}
        counts = {k: q for k, (q, _) in quota.items()}
        left = n - sum(counts.values())
        # the rest by the largest remainder; equal remainders in GUN_KINDS order
        ranked = sorted((-quota[k][1], i, k) for i, k in enumerate(order))
        for _, _, k in ranked[:left]:
            counts[k] += 1
        for k in order:
            out[(k, p)] = out.get((k, p), 0) + counts[k]
    return out


def fit_levels(fit: FitSpec | None) -> dict[tuple[str, float], int]:
    """The fit's filled allowance by kind and calibre, from her `cartridges:` in either key
    shape: by kind and calibre, or by calibre alone (a fit of packages 70 to 72, or one
    pickled then), split over her guns by `split_by_kind`."""
    if fit is None:
        return {}
    out: dict[tuple[str, float], int] = {}
    by_calibre: dict[float, int] = {}
    for key, n in (getattr(fit, "cartridges", None) or {}).items():
        if isinstance(key, tuple):
            k = (str(key[0]), float(key[1]))
            out[k] = out.get(k, 0) + int(n)
        else:
            by_calibre[float(key)] = by_calibre.get(float(key), 0) + int(n)
    if by_calibre:
        for k, n in split_by_kind(by_calibre, getattr(fit, "guns", None) or ()).items():
            out[k] = out.get(k, 0) + n
    return out


@dataclass(frozen=True)
class Wanting:
    """What the magazine wants to be complete (`Magazine.wanting`): the powder in pounds,
    the same to the nearest whole barrel, and the shot by calibre and kind. Never
    pickled."""

    powder_lb: float
    barrels: int
    shot: dict[float, dict[str, int]]

    @property
    def empty(self) -> bool:
        """Nothing wanted: no barrel and no shot."""
        return self.barrels <= 0 and not any(
            n > 0 for kinds in self.shot.values() for n in kinds.values()
        )


def gun_words(kind: str, pounder: float, n: int = 2) -> str:
    """Guns of a kind and calibre in the deck's words, without the article: 'long
    12-pounder' for one, 'long 12-pounders', '12-pounder carronades', 'half-pounder
    swivels' for more (`Gun.kind_words`, and its plural)."""
    calibre = _pounder_words(float(pounder))
    if kind == "long":
        words = f"long {calibre}-pounder"
    else:
        words = f"{calibre}-pounder {GUN_KIND_WORDS.get(kind, kind)}"
    return words if n == 1 else words + "s"


def powder_words(lb: float, none: str = "no powder") -> str:
    """Powder by the barrel of a hundred pounds and the pound: '2 barrels and 40 pounds',
    '1 barrel', '31 pounds', 'under a pound'; `none` for none."""
    lb = max(0.0, float(lb))
    if lb <= 0.0:
        return none
    total = int(round(lb))
    if total == 0:
        return "under a pound"
    barrels, pounds = divmod(total, int(BARREL_LB))
    parts = []
    if barrels:
        parts.append(f"{barrels} barrel{'s' if barrels != 1 else ''}")
    if pounds:
        parts.append(f"{pounds} pound{'s' if pounds != 1 else ''}")
    return " and ".join(parts)


@dataclass
class Magazine:
    """The magazine and the shot lockers (spec M7 §7; practice and resupply, between
    packages 72 and 73, docs/design/Build-PracticeAndResupply.md §1.1): the cartridges
    filled, by the gun's kind and calibre, against the fit's allowance (`level`); the loose
    powder below in the barrels, from which the gunner fills them (`fill`, called by
    `combat.filling.fill_tick`); and the shot by calibre and kind, counted by the gunner and
    the purser. Each round fired takes one filled cartridge of the gun's kind and one shot
    of its calibre (two shot for double, none for blank). Made from the fit's figures at
    the first call (`magazine(ship)`): a function of the ship file, the fit, the rounds
    fired, the gunner's filling and the ports' issues (`receive`), so a replay has it
    again. Every field after the first three is a plain class default, so that a magazine
    pickled by packages 70 to 72 (`layout` 1, the cartridges and the rounds fired by
    calibre) loads, and `magazine` converts it once (`_convert_70`)."""

    # FILLED: {(kind, pounder): n}; layout 1 {pounder: n}
    cartridges: dict = field(default_factory=dict)
    shot: dict[float, dict[str, int]] = field(default_factory=dict)
    fired: dict = field(default_factory=dict)  # {(kind, pounder): n}; layout 1 {pounder: n}
    # practice and resupply (between packages 72 and 73; the build design's §1.1): plain
    # class defaults, so that a magazine pickled before them loads. Layout 2 keys
    # `cartridges` and `fired` by (kind, pounder).
    layout: int = 1
    level: dict | None = None  # {(kind, pounder): n}, the fit's filled allowance
    charges: dict | None = None  # {(kind, pounder): lb}
    shot_level: dict | None = None  # the fit's shot, {pounder: {kind: n}}
    reserve_lb: float = 0.0  # the barrels' establishment
    powder_lb: float = 0.0  # loose powder below, in the barrels
    short: bool = False  # some kind below its level (the filling's early out): `recount`
    fill_s: float = 0.0  # man-seconds in hand toward the next cartridge
    filled_by_gunner: int = 0
    barrels_emptied: int = 0  # for the Ordnance's shilling (the Gunner, Art. IX)
    filling_held: bool = False  # `cease filling`
    report_filled: bool = False  # say `guns.filled` when back at the level
    said_powder_out: bool = False
    account: tuple = ()  # ((when, words), ...): reassigned, never mutated
    gun_count: dict | None = None  # {(kind, pounder): guns}, for the words; None: plural
    # a cartridge filled since the report was asked for (`combat.filling`): the report is
    # said when the last kind is back, and forgotten when nothing was short to come back
    report_due: bool = False

    def has(self, kind: str, pounder: float, charge: Charge) -> bool:
        """A filled cartridge for a gun of the kind and calibre, and its shot: two round for
        double, none for blank."""
        if self.cartridges.get((kind, float(pounder)), 0) <= 0:
            return False
        if charge is Charge.BLANK:
            return True
        shot_kind = "round" if charge is Charge.DOUBLE else charge.value
        need = 2 if charge is Charge.DOUBLE else 1
        return self.shot.get(float(pounder), {}).get(shot_kind, 0) >= need

    def take(self, kind: str, pounder: float, charge: Charge) -> None:
        """The cartridge and the shot taken for one round, and the round counted."""
        if not self.has(kind, pounder, charge):
            raise ValueError(f"the magazine has no {charge.value} for a {pounder:g}-pounder")
        key = (kind, float(pounder))
        self.cartridges[key] -= 1
        if charge is not Charge.BLANK:
            shot_kind = "round" if charge is Charge.DOUBLE else charge.value
            self.shot[float(pounder)][shot_kind] -= 2 if charge is Charge.DOUBLE else 1
        self.fired[key] = self.fired.get(key, 0) + 1
        if self.cartridges[key] < (self.level or {}).get(key, 0):
            self.short = True

    def spoil(self, share: float) -> int:
        """Cartridges found damp (package 70; the director's hand): that share of every
        kind's filled cartridges struck off, rounded down, the barrels below left alone; the
        number struck off."""
        lost = 0
        for key, n in list(self.cartridges.items()):
            gone = int(n * max(0.0, min(1.0, share)))
            self.cartridges[key] = n - gone
            lost += gone
        self.recount()
        return lost

    def recount(self) -> bool:
        """Whether some kind is below its level, kept in `short` (the filling's early out).
        Every method that moves a count keeps it; a hand that sets `cartridges` itself (a
        test, the director) calls this after."""
        level = self.level or {}
        self.short = any(self.cartridges.get(k, 0) < n for k, n in level.items())
        return self.short

    def set_filled(self, kind: str, pounder: float, n: int) -> None:
        """The filled count of a kind set by hand (a test, the director), `short` kept."""
        self.cartridges[(kind, float(pounder))] = max(0, int(n))
        self.recount()

    # -- the filling and the receipts (practice and resupply) -----------------------------

    def filled_of(self, kind: str, pounder: float) -> int:
        """The filled cartridges for guns of the kind and calibre (layout 1: the
        calibre's)."""
        if self.layout >= MAGAZINE_LAYOUT:
            return int(self.cartridges.get((kind, float(pounder)), 0))
        return int(self.cartridges.get(float(pounder), 0))

    def charge_of(self, kind: str, pounder: float) -> float:
        """A cartridge's powder in pounds: the fit's `charges:`, else `charge_lb`."""
        got = (self.charges or {}).get((kind, float(pounder)))
        return float(got) if got is not None else charge_lb(kind, pounder)

    def can_fill(self, kind: str, pounder: float) -> bool:
        """Whether the gunner can fill a cartridge of the kind now: its charge below and the
        filling not held."""
        return not self.filling_held and self.powder_lb >= self.charge_of(kind, pounder)

    def neediest(self) -> tuple[str, float] | None:
        """The kind the gunner fills next: of those below their level that he can fill, the
        lowest share of its level, equal shares in `GUN_KINDS` order and then the larger
        calibre; None when there is none."""
        best: tuple[tuple[float, int, float], tuple[str, float]] | None = None
        for key, lvl in (self.level or {}).items():
            n = self.cartridges.get(key, 0)
            if lvl <= 0 or n >= lvl or not self.can_fill(*key):
                continue
            rank = (n / lvl, kind_rank(key[0]), -float(key[1]))
            if best is None or rank < best[0]:
                best = (rank, key)
        return best[1] if best is not None else None

    def fill(self, man_seconds: float) -> list[tuple[str, float]]:
        """The gunner's man-seconds at the filling: banked in `fill_s`, and a cartridge of
        the neediest kind filled for each `fill_seconds(charge)` of them, its charge taken
        from the powder below (a barrel emptied counted for the Ordnance's shilling, the
        Gunner, Art. IX). The keys filled, in order; it logs nothing and draws nothing. With
        nothing to fill, the man-seconds in hand go back to nought."""
        out: list[tuple[str, float]] = []
        self.fill_s = float(self.fill_s) + max(0.0, float(man_seconds))
        while True:
            key = self.neediest()
            if key is None:
                self.fill_s = 0.0
                break
            charge = self.charge_of(*key)
            cost = fill_seconds(charge)
            if self.fill_s + 1e-9 < cost:
                break
            self.fill_s -= cost
            before = _barrels_open(self.powder_lb)
            self.powder_lb = max(0.0, float(self.powder_lb) - charge)
            after = _barrels_open(self.powder_lb)
            if after < before:
                self.barrels_emptied = int(self.barrels_emptied) + before - after
            self.cartridges[key] = self.cartridges.get(key, 0) + 1
            self.filled_by_gunner = int(self.filled_by_gunner) + 1
            out.append(key)
        self.recount()
        return out

    def receive(
        self,
        powder_lb: float = 0.0,
        shot: Mapping[float, Mapping[str, int]] | None = None,
        *,
        when: str = "",
        words: str = "",
    ) -> None:
        """Powder and shot taken in, as one transaction: the powder into the barrels below,
        the shot into the lockers by calibre (a float, whatever the payload's key) and
        kind, and the receipt entered in the gunner's account when it has words; the
        gunner then reports the cartridges filled, and the powder's running out may be
        said again."""
        self.powder_lb = float(self.powder_lb) + max(0.0, float(powder_lb))
        for pounder, kinds in (shot or {}).items():
            locker = self.shot.setdefault(float(pounder), {})
            for kind, n in kinds.items():
                locker[str(kind)] = locker.get(str(kind), 0) + max(0, int(n))
        if words:
            self.enter(when, words)
        self.report_filled = True
        self.report_due = False
        self.said_powder_out = False

    def wanting(self) -> Wanting:
        """What she wants to be complete: the establishment (the filled allowance's powder
        and the barrels') less what is held (the filled cartridges' powder and the powder
        below), in pounds and to the nearest whole barrel; and the fit's shot less what is
        in the lockers. Never below nought."""
        level = self.level or {}
        established = sum(n * self.charge_of(*k) for k, n in level.items())
        established += float(self.reserve_lb)
        held = sum(
            n * self.charge_of(*k) for k, n in self.cartridges.items() if isinstance(k, tuple)
        )
        held += float(self.powder_lb)
        deficit = max(0.0, established - held)
        shot: dict[float, dict[str, int]] = {}
        for p, kinds in (self.shot_level or {}).items():
            for k, n in kinds.items():
                want = int(n) - int(self.shot.get(float(p), {}).get(k, 0))
                if want > 0:
                    shot.setdefault(float(p), {})[str(k)] = want
        return Wanting(deficit, int((deficit + BARREL_LB / 2.0) // BARREL_LB), shot)

    def enter(self, when: str, words: str) -> None:
        """One line of the gunner's account."""
        self.account = (*self.account, (str(when), str(words)))

    def account_lines(self, last: int = 12) -> list[str]:
        """The gunner's account's page: its last entries, each with its date where it has
        one."""
        if last <= 0:
            return []
        return [f"{when}: {words}" if when else words for when, words in self.account[-last:]]

    def return_barrels(self) -> int:
        """The barrels emptied since the last return, counted from nought again."""
        n = int(self.barrels_emptied)
        if n:
            self.barrels_emptied = 0
        return n

    def words_of(self, key: tuple[str, float]) -> str:
        """The guns of a kind as the magazine's lines name them: 'long 12-pounder' for one
        gun, '12-pounder carronades' for more (more where the count is not known)."""
        return gun_words(key[0], key[1], int((self.gun_count or {}).get(key, 2)))

    def short_by(self) -> int:
        """The cartridges short of the allowance, all kinds together."""
        level = self.level or {}
        return sum(max(0, n - int(self.cartridges.get(k, 0))) for k, n in level.items())

    def describe(self, stopped: str = "") -> list[str]:
        """The `the magazine` reading's lines: the gunner's count of the filled cartridges
        against the allowance (and what he fills for, or why he is not filling for it now:
        `stopped`, the words of `combat.filling.not_filling`, " by night"; the review's
        finding: the reading said "the gunner filling" by night, with the hoy alongside and
        struck, when nothing was filled), the powder below against the barrels'
        establishment, the shot by calibre, and the rounds fired."""
        level = self.level or {}
        keys = list(level) + [k for k in self.cartridges if k not in level]
        any_shot = any(n for kinds in self.shot.values() for n in kinds.values())
        if not keys and self.powder_lb <= 0.0 and not any_shot:
            return ["The magazine is empty: she carries no powder."]
        parts = []
        for k in keys:
            n = int(self.cartridges.get(k, 0))
            of = f" of {level[k]}" if k in level else ""
            parts.append(f"{n}{of} for the {self.words_of(k)}")
        head = "Filled cartridges: " + (", ".join(parts) if parts else "none")
        if self.short:
            needy = self.neediest()
            if self.filling_held:
                head += "; the filling stopped by order"
            elif needy is not None and stopped:
                head += f"; the gunner not filling for the {self.words_of(needy)}{stopped}"
            elif needy is not None:
                head += f"; the gunner filling for the {self.words_of(needy)}"
            elif self.powder_lb > 1e-9:
                head += "; too little powder below to fill more"
            else:
                head += "; no powder below to fill more"
        out = [head + "."]
        established = int(round(float(self.reserve_lb) / BARREL_LB))
        below = powder_words(self.powder_lb, "none")
        if established > 0:
            plural = "s" if established != 1 else ""
            out.append(f"Powder below: {below}, of {established} barrel{plural} established.")
        else:
            out.append(f"Powder below: {below}; no barrels established.")
        shots = []
        for p in sorted(self.shot, reverse=True):
            kinds = ", ".join(
                f"{n} {k}" for k, n in (self.shot.get(p) or {}).items() if n or k == "round"
            )
            shots.append(f"{_pounder_words(p)}-pounder {kinds or 'none'}")
        out.append("Shot: " + ("; ".join(shots) if shots else "none") + ".")
        fired = sum(int(n) for n in self.fired.values())
        if fired:
            out.append(f"{fired} round{'s' if fired != 1 else ''} fired.")
        return out


def _barrels_open(lb: float) -> int:
    """The barrels the powder below is in, the last broached: the ceiling of its hundreds
    of pounds."""
    return math.ceil(max(0.0, float(lb)) / BARREL_LB - 1e-9)


def _gun_count(fit: Any) -> dict[tuple[str, float], int] | None:
    if fit is None:
        return None
    out: dict[tuple[str, float], int] = {}
    for g in getattr(fit, "guns", None) or ():
        key = (str(g.kind), float(g.pounder))
        out[key] = out.get(key, 0) + 1
    return out


def _charges_of(
    fit: Any, levels: Mapping[tuple[str, float], int]
) -> dict[tuple[str, float], float]:
    """A cartridge's charge for every kind of the fit's allowance: the file's `charges:`,
    else `charge_lb` (a fit pickled before them, or a hand-written file without)."""
    given = getattr(fit, "charges", None) or {}
    out: dict[tuple[str, float], float] = {}
    for key in levels:
        got = given.get(key)
        out[key] = float(got) if got is not None else charge_lb(key[0], key[1])
    return out


def _split_store(counts: Mapping[Any, int], guns: Iterable[Any]) -> dict[tuple[str, float], int]:
    """A layout-1 store's counts by kind and calibre: the calibre keys split over the fit's
    guns (`split_by_kind`), a key already by kind kept."""
    out: dict[tuple[str, float], int] = {}
    by_calibre: dict[float, int] = {}
    for key, n in (counts or {}).items():
        if isinstance(key, tuple):
            k = (str(key[0]), float(key[1]))
            out[k] = out.get(k, 0) + int(n)
        else:
            by_calibre[float(key)] = by_calibre.get(float(key), 0) + int(n)
    for k, n in split_by_kind(by_calibre, guns).items():
        out[k] = out.get(k, 0) + n
    return out


def _convert_70(store: Magazine, fit: FitSpec | None) -> None:
    """A magazine of packages 70 to 72 (layout 1) brought to layout 2 once, logging and
    drawing nothing: each calibre's cartridges and rounds fired split over the fit's guns of
    that calibre by kind (`split_by_kind`); the allowance, the charges and the shot's level
    from the fit (an old fit's calibre keys split the same way, its charges `charge_lb`'s);
    no powder below, and the barrels' establishment the fit's (an old fit's nought, so an
    old game has no reserve until she takes powder in)."""
    guns = list(getattr(fit, "guns", None) or ()) if fit is not None else []
    store.cartridges = _split_store(store.cartridges, guns)
    store.fired = _split_store(store.fired, guns)
    levels = fit_levels(fit)
    store.level = dict(levels)
    store.charges = _charges_of(fit, levels)
    store.shot_level = {float(k): dict(v) for k, v in fit.shot.items()} if fit is not None else None
    store.powder_lb = 0.0
    store.reserve_lb = float(getattr(fit, "powder_barrels", 0) or 0) * BARREL_LB
    store.gun_count = _gun_count(fit)
    store.layout = MAGAZINE_LAYOUT
    store.recount()


def magazine(ship: Any) -> Magazine:
    """The ship's magazine, kept in `ship.extra["magazine"]`: a function of the ship file,
    the fit, the rounds fired, the gunner's filling and the ports' issues. Made at the
    first call from the fit's figures, the cartridges filled to the allowance and the powder
    below at the barrels' establishment; a magazine of packages 70 to 72 converted once."""
    extra = getattr(ship, "extra", None)
    if extra is None:
        return Magazine(layout=MAGAZINE_LAYOUT)
    store = extra.get("magazine")
    if isinstance(store, Magazine):
        if store.layout < MAGAZINE_LAYOUT:
            _convert_70(store, getattr(ship, "fit_spec", None))
        return store
    fit: FitSpec | None = getattr(ship, "fit_spec", None)
    if fit is None:
        store = Magazine(layout=MAGAZINE_LAYOUT)
    else:
        levels = fit_levels(fit)
        reserve = float(getattr(fit, "powder_barrels", 0) or 0) * BARREL_LB
        store = Magazine(
            cartridges=dict(levels),
            shot={float(k): dict(v) for k, v in fit.shot.items()},
            layout=MAGAZINE_LAYOUT,
            level=dict(levels),
            charges=_charges_of(fit, levels),
            shot_level={float(k): dict(v) for k, v in fit.shot.items()},
            reserve_lb=reserve,
            powder_lb=reserve,
            gun_count=_gun_count(fit),
        )
    extra["magazine"] = store
    return store


# ---------------------------------------------------------------------------
# Catharpins (spec 3b §3)
# ---------------------------------------------------------------------------

# Swiftering in the catharpins draws the lower shrouds in below the top, so that the
# lower yard can be braced sharper before its lee yardarm and its sail come against
# the lee rigging: Steel 1794, vol. I, CATHARPINS ("Short ropes, to keep the lower
# shrouds in tight, after they are braced in by swifter, and to afford room to brace
# the yards sharp"); Lever 1808, fig. 182 (the shrouds "bowsed in" by a swifter and the
# legs seized); Fincham 1843, art. 102 (Hardy's short ship, by "such measures as would
# allow the yards to be braced sharper up", lay a point closer). How much sharper no
# source says: four degrees is judgement, less than the short ship's gain over the long
# ships in art. 102, which her other measures shared. The topmast rigging is not
# touched, so only the lower yard gains.
CATHARPIN_GAIN_DEG = 4.0


def flying_down(ship: Any, spar: Spar) -> bool:
    """A yard sent down on deck with the flying sail bent to it (package 57: a royal of
    1794, a lug topsail): every sail on it set flying and stowed."""
    sails = [sl for sl in ship.sails.values() if sl.roles.get("yard") == spar.id]
    return bool(sails) and all(sl.sent_down for sl in sails)


def lower_yards(ship: Any, mast: Spar) -> list[Spar]:
    """The yards slung on a lower mast itself: a ship's course yard, the crossjack.
    A topsail schooner's masts have none (her topsail yard is on the fore topmast)."""
    return [y for y in ship.spars.values() if y.parent == mast.id and y.is_yard]


def sync_catharpins(ship: Any) -> list[tuple[Spar, float]]:
    """Make every lower yard's brace limit agree with its mast's catharpins.

    The mast's `swiftered_in` is the state; its lower yards' `brace_limit` follows it,
    `CATHARPIN_GAIN_DEG` beyond the ship file's while swiftered in. A yard braced
    sharper than the limit it is left with (the catharpins eased with the yard sharp
    up) comes in to it, as the shrouds going out bear it in. Returns the yards that
    came in, each with the angle it came in from, for the log. Idempotent: the strain
    model calls it every tick, and whatever reads a limit may call it first."""
    came_in: list[tuple[Spar, float]] = []
    gain = units.deg_to_rad(CATHARPIN_GAIN_DEG)
    for mast in ship.spars.values():
        if mast.cls != "mast":
            continue
        for yard in lower_yards(ship, mast):
            if yard.rigged_brace_limit <= 0.0:
                continue  # the file gives this yard no limit; nothing to gain or keep
            limit = yard.rigged_brace_limit + (gain if mast.swiftered_in else 0.0)
            yard.brace_limit = limit
            if abs(yard.brace_angle) > limit + 1e-9:
                came_in.append((yard, yard.brace_angle))
                yard.brace_angle = math.copysign(limit, yard.brace_angle)
    return came_in


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


# ---------------------------------------------------------------------------
# The booms: spare spars (package 30b)
# ---------------------------------------------------------------------------

# The spare spars were stowed amidships between the fore and main masts, on the boat skids,
# and were called "the booms" there: "LASHING OF BOOMS, that is, the spare topmasts, yards,
# &c. stowed on the boat skids" (Steel 1794, vol. I); Luce 1866, ch. XVII Spare Spars,
# 'Stowing Booms between the fore and mainmast'. A spar that carries away is replaced by a
# spare of its class (`shift the <spar>`, data/evolutions/shift_spar.yaml); the ship file
# gives the store by class (`crew.stores.spare_spars`), with its source in the comment.

# A spar class in words, for the log and the refusals.
SPAR_CLASS_WORDS: dict[str, str] = {
    "mast": "lower mast",
    "topmast": "topmast",
    "topgallant_mast": "topgallant mast",
    "royal_mast": "royal mast",
    "bowsprit": "bowsprit",
    "jib_boom": "jib-boom",
    "flying_jib_boom": "flying jib-boom",
    "yard": "yard",
    "gaff": "gaff",
    "boom": "boom",
    "studdingsail_boom": "studding-sail boom",
    "lug_yard": "lug yard",
    "lateen_yard": "lateen yard",
    "sprit": "sprit",
}


def spar_class_words(cls: str | None, n: int = 1) -> str:
    """'studding-sail boom', or 'studding-sail booms' for more than one; a spar of no class
    (a file that gives only a count) is 'spar'."""
    words = SPAR_CLASS_WORDS.get(cls or "", (cls or "spar").replace("_", " "))
    return words if n == 1 else words + "s"


@dataclass
class Booms:
    """The spare spars aboard, by class (`counts`, in the ship file's order), and `any`
    spars of no class that the carpenter fits to any spar: the store of a ship whose file
    gives only a count. Shifting a spar takes one of its class, else one of these."""

    counts: dict[str, int] = field(default_factory=dict)
    any: int = 0

    def __len__(self) -> int:
        return sum(self.counts.values()) + self.any

    def have(self, cls: str) -> int:
        """How many spares could replace a spar of this class."""
        return self.counts.get(cls, 0) + self.any

    def take(self, cls: str) -> None:
        """Take a spare for a spar of this class: one of its class if there is one."""
        if self.counts.get(cls, 0) > 0:
            self.counts[cls] -= 1
        elif self.any > 0:
            self.any -= 1
        else:
            raise ValueError(f"there is no spare {spar_class_words(cls)} on the booms")

    def _listed(self) -> str:
        items = [f"{n} {spar_class_words(cls, n)}" for cls, n in self.counts.items() if n > 0]
        if self.any:
            items.append(f"{self.any} spar{'s' if self.any != 1 else ''} to fit any")
        if len(items) <= 1:
            return "".join(items)
        return ", ".join(items[:-1]) + " and " + items[-1]

    def muster_line(self) -> str:
        n = len(self)
        if n == 0:
            return "The booms: no spare spar aboard."
        return f"The booms: {n} spare spar{'s' if n != 1 else ''}, {self._listed()}."

    def inventory_lines(self) -> list[str]:
        """The `the booms` query: the spare spars by class, in the form of the sail room's."""
        n = len(self)
        if n == 0:
            return ["The booms are bare; there is no spare spar aboard."]
        return [f"The booms hold {n} spare spar{'s' if n != 1 else ''}: {self._listed()}."]


def booms(ship: Any) -> Booms:
    """The ship's spare spars, kept in `ship.extra["booms"]`: made on first use from the
    ship file's `crew.stores.spare_spars` (by class, or a plain count of spars that fit
    any), else none. `ship.extra["spare_spars"]` is kept as the count. Like the sail room,
    the store is a function of the ship file and the orders given, so a replay rebuilds
    it as the game had it."""
    store = ship.extra.get("booms")
    if not isinstance(store, Booms):
        stores = _stores_of(ship)
        get = stores.get if isinstance(stores, dict) else lambda k: getattr(stores, k, None)
        by_class = get("spars") if stores is not None else None
        if isinstance(by_class, dict):
            store = Booms(counts={str(k): int(v) for k, v in by_class.items()})
        else:
            count = get("spare_spars") if stores is not None else None
            if isinstance(count, dict):  # a raw mapping of stores, as a test may give
                store = Booms(counts={str(k): int(v) for k, v in count.items()})
            else:
                ok = isinstance(count, int) and not isinstance(count, bool) and count >= 0
                store = Booms(any=int(count) if ok else 0)
        ship.extra["booms"] = store
    ship.extra["spare_spars"] = len(store)
    return store


# ---------------------------------------------------------------------------
# The boatswain's store: spare cordage (package 31b)
# ---------------------------------------------------------------------------

# The spare rope a ship carries when her file gives no `crew.stores.cordage_fathoms`: one
# coil. Rope for running rigging was laid in lengths that "stand 120 to 130 fathoms" (Steel
# 1794, vol. I, 'Rope-making', of hawser-laid rope); one coil is judgement, as
# DEFAULT_SPARE_SAILS is for the sail room.
DEFAULT_CORDAGE_FATHOMS = 120.0


@dataclass
class Cordage:
    """The spare cordage in the boatswain's store, in fathoms, from which a parted line is
    rove afresh (`data/evolutions/reeve_line.yaml`, package 31b). "Running rigging had
    better be got out in the coil, and cut to proper lengths when reeved on board" (Steel
    1794, vol. I, the note to the tables of standing and running rigging); the spare
    cordage is kept in the store-room forward with "all small spare articles furnished for
    the use of the boatswain" (Luce 1884, ch. XII, the yeoman's store-room). Taken by the
    fathom, as the sail room is taken by the sail; a replay rebuilds it from the ship file
    and the orders given."""

    fathoms: float = 0.0

    def take(self, fathoms: float) -> None:
        if fathoms > self.fathoms + 1e-9:
            raise ValueError("there is not that much spare cordage in the boatswain's store")
        self.fathoms = max(0.0, self.fathoms - fathoms)

    def describe(self) -> str:
        """'570 fathoms of spare cordage', 'no spare cordage'."""
        n = round(self.fathoms)
        if n <= 0:
            return "no spare cordage"
        return f"{n} fathom{'s' if n != 1 else ''} of spare cordage"

    def inventory_lines(self) -> list[str]:
        """The `the boatswain's store` query, in the form of the sail room's."""
        if self.fathoms < 1.0:
            return [
                "The boatswain's store has no spare cordage; a parted line can be spliced, "
                "but not rove afresh until the dockyard supplies rope."
            ]
        return [f"The boatswain's store holds {self.describe()}."]


def cordage(ship: Any) -> Cordage:
    """The ship's spare cordage, kept in `ship.extra["cordage"]`: made on first use from the
    ship file's `crew.stores.cordage_fathoms`, else one coil (`DEFAULT_CORDAGE_FATHOMS`)
    for a ship whose file gives no stores. `ship.extra["spare_cordage_fathoms"]` is kept
    as the count."""
    store = ship.extra.get("cordage")
    if not isinstance(store, Cordage):
        stores = _stores_of(ship)
        get = stores.get if isinstance(stores, dict) else lambda k: getattr(stores, k, None)
        given = get("cordage_fathoms") if stores is not None else None
        ok = isinstance(given, int | float) and not isinstance(given, bool) and given >= 0
        store = Cordage(float(given) if ok else DEFAULT_CORDAGE_FATHOMS)
        ship.extra["cordage"] = store
    ship.extra["spare_cordage_fathoms"] = store.fathoms
    return store


# ---------------------------------------------------------------------------
# The ground tackle: the anchors and their cables (package 34, spec M5 §18)
# ---------------------------------------------------------------------------

# "Every ship has, or ought to have, three principal anchors, with a cable to each, viz.
# the sheet, the best bower and small bower, so called from their usual situation on the
# ship's bows. There are besides smaller anchors, for removing a ship from place to place
# in a harbour or river ... the stream-anchor, the kedge and grappling" (Falconer 1780,
# ANCHOR). "In the Royal Navy, the two Bower, and Sheet Anchors are of the same size, as
# are their Cables" (Lever 1808, 'Anchors', p. 67). The anchors are parts the ship file
# lists (`ground_tackle:`, written by tools/gen_ships.py by the ship's size), each with
# the cable bent to it; the state is kept here, in `ship.extra["ground_tackle"]`, and the
# physics of the cable's pull, the holding and the dragging is `physics/anchor.py`.


class AnchorState(StrEnum):
    STOWED = "at the bows"  # catted and fished, the cable bent (Lever: the anchors "hung")
    READY = "a-cockbill"  # "ready to be sunk from the bow at a moment's warning" (Falconer)
    DOWN = "down"  # let go, the ship riding by it or dragging it
    AWEIGH = "aweigh"  # broken out of the ground and hove up to the bows, not yet catted
    CATTED = "catted"  # hooked to the cat and hove up to the cat-head, not yet fished
    LOST = "lost"  # the cable parted or cut: the anchor on the bottom with its buoy


# The kinds in the log's words, for a line that names one by its kind.
ANCHOR_KIND_WORDS: dict[str, str] = {
    "bower": "bower",
    "sheet": "sheet anchor",
    "stream": "stream anchor",
    "kedge": "kedge",
}


@dataclass
class Anchor:
    """One anchor with its cable: the file's figures, and the state."""

    id: str
    kind: str
    name: str  # "the best bower"
    weight_kg: float
    cable_fathoms: float  # the cable bent to it, whole
    cable_in: float  # the cable's circumference, inches
    cable_kn: float  # the cable's rating, the working load (parts at 1.5 of it, spec §7.5)
    state: AnchorState = AnchorState.STOWED
    scope_m: float = 0.0  # the cable veered, metres, while down
    ground_x: float | None = None  # where it lies, metres east and north of the start
    ground_y: float | None = None
    depth_m: float = 0.0  # the water over it now (the chart's depth and the tide)
    bottom: str = ""  # the ground it lies in, from the chart's bottom note
    cable_condition: float = 100.0  # as a line's (spec §7.5): worn by the strain
    cable_load_kn: float = 0.0  # the tension now, set by the physics each tick
    holding_kn: float = 0.0  # what it holds now, set by the physics
    dragging: bool = False  # it is dragging: come home for DRAG_SAY_S together (physics/anchor)
    came_home: bool = False  # it moved this tick (set by the physics each substep it does)
    drag_s: float = 0.0  # the seconds it has been coming home
    hold_s: float = 0.0  # the seconds it has held since it last came home
    # package 37f: how far it has come home, metres: this tick (the physics adds each
    # substep's move, `judge_cables` takes it), and since this dragging began (for the
    # log's "a cable since it began"); plain defaults, so an older checkpoint loads
    moved_m: float = 0.0
    drag_m: float = 0.0
    # whether the log has said she is brought up by it (package 37f: `let go the anchor`
    # never did); true by default, so that an anchor down in an older checkpoint is not
    # said to bring her up a second time, and cleared when one is let go
    brought_up: bool = True
    taut: bool = False  # the cable bar-taut (she is riding by it), else slack
    heaving: bool = False  # the cable being hove in at the capstan (weighing, heaving short)

    @property
    def weight_kn(self) -> float:
        return self.weight_kg * units.G / 1000.0

    @property
    def scope_fathoms(self) -> float:
        return units.m_to_fathoms(self.scope_m)

    @property
    def cable_strain_ratio(self) -> float:
        return self.cable_load_kn / self.cable_kn if self.cable_kn > 0 else 0.0

    @property
    def down(self) -> bool:
        return self.state is AnchorState.DOWN

    @property
    def kind_words(self) -> str:
        return ANCHOR_KIND_WORDS.get(self.kind, self.kind)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "name": self.name,
            "weight_kg": self.weight_kg,
            "state": self.state.value,
            "scope_fathoms": round(self.scope_fathoms, 1),
            "cable_fathoms": self.cable_fathoms,
            "cable_in": self.cable_in,
            "cable_kn": self.cable_kn,
            "cable_load_kn": round(self.cable_load_kn, 1),
            "cable_condition": round(self.cable_condition, 1),
            "holding_kn": round(self.holding_kn, 1),
            "depth_m": round(self.depth_m, 2),
            "bottom": self.bottom,
            "dragging": self.dragging,
            "taut": self.taut,
            "come_home_m": round(self.drag_m, 1),
        }


@dataclass
class GroundTackle:
    """The ship's anchors, in the file's order (the best bower first), and whether the
    cable is chain."""

    anchors: list[Anchor]
    chain: bool = False

    @classmethod
    def from_spec(cls, spec: GroundTackleSpec) -> GroundTackle:
        return cls(
            anchors=[
                Anchor(a.id, a.kind, a.name, a.weight_kg, a.cable_fathoms, a.cable_in, a.cable_kn)
                for a in spec.anchors
            ],
            chain=spec.chain,
        )

    def get(self, anchor_id: str) -> Anchor | None:
        for a in self.anchors:
            if a.id == anchor_id:
                return a
        return None

    def by_words(self, words: str | None) -> Anchor | None:
        """The anchor the words name: 'the best bower', 'small bower', 'the sheet', 'the
        stream', 'the kedge', 'the second anchor' (the bower not yet down), or 'the
        anchor' (the one she rides by if one is down, else the best bower); None when no
        anchor answers to them."""
        cleaned = "".join(c if c.isalnum() or c.isspace() else " " for c in (words or "").lower())
        key = " ".join(w for w in cleaned.split() if w not in ("the", "anchor", "anchors", "cable"))
        bowers = self.bowers()
        if key in ("", "best", "an", "a"):
            riding = self.riding_by()
            if riding is not None:
                return riding
            return bowers[0] if bowers else (self.anchors[0] if self.anchors else None)
        if key in ("second", "other", "lee", "weather", "second bower"):
            for a in bowers:
                if a.state is not AnchorState.DOWN:
                    return a
            return None
        for a in self.anchors:
            name = a.name.lower().replace("the ", "").replace("anchor", "").strip()
            if key in (a.id.replace("_", " "), name, a.kind, f"{a.kind} anchor", a.id):
                return a
        return None

    def carries(self, words: str | None) -> bool:
        """Whether she carries an anchor the words name, whatever its state (package 37k:
        `let go the sheet anchor` in a cutter, which has none, was taken while the hands
        were at other work and failed four minutes later): `by_words`, with 'the second
        anchor' any bower, down or not."""
        if self.by_words(words) is not None:
            return True
        cleaned = "".join(c if c.isalnum() or c.isspace() else " " for c in (words or "").lower())
        key = " ".join(w for w in cleaned.split() if w not in ("the", "anchor", "anchors", "cable"))
        return key in ("second", "other", "lee", "weather", "second bower") and bool(self.bowers())

    def names_words(self) -> str:
        """'the best bower, the small bower and the kedge': her anchors, for a refusal."""
        names = [a.name for a in self.anchors]
        if len(names) <= 1:
            return "".join(names)
        return ", ".join(names[:-1]) + " and " + names[-1]

    def bowers(self) -> list[Anchor]:
        return [a for a in self.anchors if a.kind == "bower"]

    def down(self) -> list[Anchor]:
        return [a for a in self.anchors if a.state is AnchorState.DOWN]

    def riding_by(self) -> Anchor | None:
        """The anchor she rides by: the one down with the most cable out."""
        down = self.down()
        if not down:
            return None
        return max(down, key=lambda a: a.scope_m)

    def at_anchor(self) -> bool:
        return bool(self.down())

    @property
    def cable_words(self) -> str:
        return "chain" if self.chain else "cable"

    def describe(self) -> list[str]:
        """The `the ground tackle` query: every anchor, its weight, its cable, its state."""
        out = []
        for a in self.anchors:
            cwt = a.weight_kg / 50.802
            cable = f"{a.cable_fathoms:g} fathoms of {a.cable_in:g}-inch {self.cable_words}"
            state = a.state.value
            if a.state is AnchorState.DOWN:
                state = f"down, {a.scope_fathoms:.0f} fathoms out"
            out.append(f"{a.name[:1].upper()}{a.name[1:]}, {cwt:.0f} cwt, {cable}: {state}.")
        return out

    def muster_line(self) -> str:
        names = [a.name.replace("the ", "") for a in self.anchors]
        return f"Ground tackle: {len(self.anchors)} anchors, the {', the '.join(names)}."


def ground_tackle(ship: Any) -> GroundTackle | None:
    """The ship's anchors and cables, kept in `ship.extra["ground_tackle"]`: made on first
    use from the ship file's `ground_tackle:` section; None for a ship whose file lists
    none (the anchor orders are then refused in words). Like the sail room, a function
    of the ship file and the orders given, so a replay rebuilds it."""
    extra = getattr(ship, "extra", None)
    if extra is None:
        return None
    store = extra.get("ground_tackle")
    if isinstance(store, GroundTackle):
        return store
    spec = getattr(getattr(ship, "spec", None), "ground_tackle", None)
    if spec is None:
        return None
    store = GroundTackle.from_spec(spec)
    extra["ground_tackle"] = store
    return store


@dataclass
class Hull:
    spec: HullSpec
    water_in_well_m: float = 0.0
    # the free surface's loss of metacentric height (package 73, spec M7 §13; written by
    # `freesail/world/water.py` from the water in the ship, nought with a dry well); a
    # dataclass default, so that a checkpoint from before loads with none
    free_surface_m: float = 0.0

    @property
    def gm_m(self) -> float:
        """The metacentric height as she floats now: the file's figure less the free
        surface's, floored at the motion's own floor. The heel's balance
        (`physics/hull.py`) and the roll (`physics/motion.py`) read this in place of the
        file's figure: the one place the water's quantity reaches the stability (the
        physics itself is not changed)."""
        fs = float(getattr(self, "free_surface_m", 0.0) or 0.0)
        return max(0.05, float(self.spec.gm_m) - fs)

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
