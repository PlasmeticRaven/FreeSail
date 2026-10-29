"""The ship file format: what a ship definition may contain, and its validation.

A ship file (YAML, see docs/TechnicalSpec-M0-M2.md §6) lists a hull, spars,
sails and lines, with *role links* between them (`on`, `steps_on`, `yard`,
`mast`, `gaff`, `boom`, `stay`, `of`). This module turns the raw dictionary
into typed specs and rejects anything the engine could not reason about,
with an error written as a sentence naming the file and the part.

Nothing here knows about any particular rig. It knows about part classes and
what each class requires.

An optional `crew:` section (docs/TechnicalSpec-M3.md §2.3) establishes the
ship's company: complement, stations, ratings, posts, idlers by trade and
stores. It is parsed into a `CrewSpec`; a file without it has `crew = None`.

Milestone 3b (docs/TechnicalSpec-M3b.md §6) adds canvas: a sail may give its
`canvas_no` (the number of the canvas it is made of, 1 the heaviest), say
that it starts the voyage in the sail room (`bent: false`: storm canvas and
the occasional sails), and name the sail it is bent `in_place_of` (a storm
mizzen for the spanker). The stores may list the sail room's contents
(`sails:`, each with the sail it is made for, its canvas number and its
condition); the old `spare_sails` count is then derived from the list.

Package 30b (milestone 5) makes the spare spars a store by class: the stores'
`spare_spars` may map a spar class to the number of spares of it on the booms
(`{topmast: 2, studdingsail_boom: 4}`), and the count is then derived from it. A
plain number is still taken: that many spars of no class, which the carpenter can
fit to any spar.

Package 34 (spec M5 §18; decision 30) adds the ground tackle: an optional
`ground_tackle:` section listing the anchors (bowers, a sheet anchor, a stream and a
kedge, each with its weight and the cable bent to it by the fathom, with its size and
rating) and whether the cable is chain (`chain: true`, where the era allows it; hemp in
1805). It is parsed into a `GroundTackleSpec`; a file without it has
`ground_tackle = None`, and the anchor orders are refused on such a ship.

Package 35 (spec M5 §22, §23) adds the hold, the boats and the people's roles: an
optional `hold:` section (`capacity_tons`, what she can stow beyond her own stores, a
`HoldSpec`), an optional `boats:` list (each boat with its kind, name, length, oars, crew
and the tons it carries, a `BoatSpec`), and under `crew:` an optional `people:` list of
the named roles beyond the posts (a master's mate, a midshipman as messenger: each a role
drawn from a station at muster, a `PersonRoleSpec`). A file without them has
`hold = None`, no boats, and the posts alone for people; the ports' orders are refused
in words on such a ship.

Package 56 (spec M7b §21a) adds the fishing gear: an optional `gear:` list (each piece
with its kind, the trawl, the drift nets, the seine or the lines, its name and its size
where the file gives it, a `GearSpec`); a file without it carries none, and the fishing
orders are refused in words on such a ship.

Package 57 (the rig through the generator) adds three keys to a sail: `flying: true`, a
sail set flying (its yard swayed up from the deck with the sail bent, sent down whole when
it is taken in, never reefed aloft: the lugger's lug topsails, the royals of 1794);
`sheeted_to`, a lug topsail's lower lug, to whose yard its clew is sheeted; and
`corners_m`, the sail's corners as it is cut, for the drawing (a lug's tack, throat, peak
and clew; a staysail's tack, nock, peak and clew, or tack, peak and clew for a triangle).

Package 75 (the new ships; docs/design/Build-Ships.md §3.1, §5) adds the hull's `profile:`, the
side, the decks and the ports in the fore-and-aft plane (a `HullProfile`, read through
`freesail.ship.profile`; strict, so a misspelt key inside it is refused rather than lost); a
gun's `deck`, one of `DECK_WORDS`; and the fit `unarmed`, a ship of the file with no guns
(`ArmamentSpec.fit` gives None). No file of the eight carries any of them, so each is inert
until a ship's builder writes it. A pivot gun's own `arc_deg` is now required: the one pivot
on file, the privateer schooner's long Tom, gives it already.

Package 75's stage 0E (docs/design/Design-ShipsEngineExtensions.md §8) adds the engine
extensions' three keys: a sail's `settee: true`, the bilander's main, a dipping lug set and
clewed up as a square sail (§5.1-§5.2); a sail's `cut_at_mast: true`, the 64's and the 74's
mizen course, a lateen with its fore part cut away and its luff laced to the mast (§3.1); and a
lower mast's `heave_to_aback: true`, the one mast whose yards are laid aback to heave to
(§5.7). Unknown keys are dropped silently, so each is a field here, refused in words where it
cannot stand. No file of the eight carries any of them. Beyond the refusals here, only
`Sail.curve_class`, the runner's `class: settee` and the served graph and snapshot read them,
none of which differs for a ship without them, until the engine's steps build their behaviour.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

# the profile's readers (package 75): pure, and importing this module only for its types
from freesail.ship.profile import interp, rail_at

# ---------------------------------------------------------------------------
# Part classes
# ---------------------------------------------------------------------------

SPAR_CLASSES = frozenset(
    {
        "mast",
        "topmast",
        "topgallant_mast",
        "royal_mast",
        "bowsprit",
        "jib_boom",
        "flying_jib_boom",
        "yard",
        "gaff",
        "boom",
        "studdingsail_boom",
        "lug_yard",
        "lateen_yard",
        "sprit",
    }
)

# Spars that stand on the hull itself and therefore need no `on`/`steps_on`.
ROOT_SPAR_CLASSES = frozenset({"mast", "bowsprit"})

# Spars that behave as a "yard": braced, and carrying a square-family sail.
YARD_LIKE_CLASSES = frozenset({"yard", "lug_yard", "lateen_yard"})

SAIL_CLASSES = frozenset({"square", "gaff", "jibheaded", "lug", "lateen", "sprit", "studding"})

# Role links each sail class must have, and the spar classes each may point at.
SAIL_ROLE_REQUIREMENTS: dict[str, dict[str, frozenset[str]]] = {
    "square": {"yard": frozenset({"yard"})},
    "gaff": {"mast": frozenset({"mast", "topmast"}), "gaff": frozenset({"gaff"})},
    "jibheaded": {},  # needs a stay OR a mast; checked in validate()
    "lug": {"yard": frozenset({"lug_yard"})},
    "lateen": {"yard": frozenset({"lateen_yard"})},
    "sprit": {"mast": frozenset({"mast"}), "sprit": frozenset({"sprit"})},
    # a studding-class sail is spread by a studding sail boom, or (a water sail) laced under
    # a gaff sail's own boom (spec 3b §6.4; Steel 1794 vol. I, 'Sloop's water-sail')
    "studding": {"boom": frozenset({"studdingsail_boom", "boom"})},
}
SAIL_OPTIONAL_ROLES: dict[str, dict[str, frozenset[str]]] = {
    "gaff": {"boom": frozenset({"boom"})},
    "jibheaded": {
        "stay": frozenset(),  # a stay is a line, checked separately
        "mast": frozenset({"mast", "topmast", "topgallant_mast"}),
        "halyard_spar": frozenset(),
    },
    "lug": {"mast": frozenset({"mast", "topmast"})},
    "lateen": {"mast": frozenset({"mast"})},
    "studding": {"yard": frozenset({"yard"})},
}

LINE_CLASSES = frozenset(
    {
        "halyard",
        "throat_halyard",
        "peak_halyard",
        "sheet",
        "tack",
        "brace",
        "lift",
        "clewline",
        "buntline",
        "leechline",
        "bowline",
        "reef_tackle",
        "downhaul",
        "outhaul",
        "vang",
        "guy",
        "stay",
        "shroud",
        "backstay",
    }
)
STANDING_LINE_CLASSES = frozenset({"stay", "shroud", "backstay"})

# What kind of part each line class may be "of".
LINE_TARGET_KINDS: dict[str, frozenset[str]] = {
    "halyard": frozenset({"spar", "sail"}),
    "throat_halyard": frozenset({"spar"}),
    "peak_halyard": frozenset({"spar"}),
    "sheet": frozenset({"sail"}),
    "tack": frozenset({"sail"}),
    "brace": frozenset({"spar"}),
    "lift": frozenset({"spar"}),
    "clewline": frozenset({"sail"}),
    "buntline": frozenset({"sail"}),
    "leechline": frozenset({"sail"}),
    "bowline": frozenset({"sail"}),
    "reef_tackle": frozenset({"sail"}),
    "downhaul": frozenset({"sail", "spar"}),
    "outhaul": frozenset({"sail", "spar"}),
    "vang": frozenset({"spar"}),
    "guy": frozenset({"spar"}),
    "stay": frozenset({"spar"}),
    "shroud": frozenset({"spar"}),
    "backstay": frozenset({"spar"}),
}

SIDES = frozenset({"starboard", "larboard"})

# Spars a fore-and-aft sail is spread on. A ringtail boom run out on one of these, and the
# ringtail or water sail it spreads, lie in the gaff sail's plane and have no fixed side
# (spec 3b §6.4; Kipping 1847, 'Ringtail Sails': it "sets like a topmast studding sail,
# outside of the after-leech of the main-trysail").
FORE_AND_AFT_SPAR_CLASSES = frozenset({"boom", "gaff"})

# The canvas numbers the engine knows the strength of: Luce 1884 App. E pp. 610-611
# (docs/references/Tables.md §2) tabulates Nos. 1 to 9, No. 1 the heaviest.
CANVAS_NUMBERS = range(1, 10)

# The anchors a ship file may list (spec M5 §18; Falconer 1780, ANCHOR: "the sheet, the
# best bower and small bower ... the stream-anchor, the kedge and grappling").
ANCHOR_KINDS = ("bower", "sheet", "stream", "kedge")
ANCHOR_KEYS = ("id", "kind", "name", "weight_kg", "cable_fathoms", "cable_in", "cable_kn")

# The armament (spec M7 §7; package 70): a gun is a part of the graph by its position. Its
# kinds are the period's three (the long gun, the carronade of 1779 on, and the swivel on
# the rail), its places the broadside (by number and side, the pair of one number sharing a
# crew), the bow and stern chasers, and the rail. A ship file carries the armament in one
# or more **fits** the scenario chooses between (`ship: {fit: ...}`): the cutter's
# carronades of 1805 and her long 3-pounders of the hired cutters' fit (the owner,
# 2026-10-23). Each fit names its magazine: cartridges by calibre and shot by kind.
# Practice and resupply (between packages 72 and 73; docs/design/Build-PracticeAndResupply.md
# §1.2): the filled cartridges and their charges by the gun's kind and calibre (a calibre's
# cartridges may still be said alone where one kind of the fit has it), the powder below in
# barrels, and a King's fit's allowance of charges for exercise a month.
# PROVISIONAL (the owner's ask of 2026-10-25, ahead of package 75): the **pivot**, a long
# gun on a slide carriage turning about a bolt on the deck's racers, amidships and firing
# over either side (the Baltimore privateers' "long Tom"); it has no side, and trains to
# the mark (`combat/guns.py`).
GUN_KINDS = ("long", "carronade", "swivel")
GUN_PLACES = ("broadside", "bow", "stern", "rail", "pivot")
SHOT_KINDS = ("round", "chain", "grape")
GUN_KEYS = (
    "id",
    "kind",
    "pounder",
    "place",
    "number",
    "side",
    "x_m",
    "height_m",
    "crew",
    "weight_cwt",
    "arc_deg",
    "deck",  # package 75: the deck it stands on, one of DECK_WORDS
)
# A ship of a file that carries no guns (package 75; docs/design/Build-Ships.md §8.1): the
# word a scenario or a description gives for her fit, and a file may give as its default;
# `ArmamentSpec.fit` gives None for it, as for a file with no armament.
UNARMED = "unarmed"
FIT_KEYS = (
    "source",
    "guns",
    "cartridges",
    "charges",
    "powder_barrels",
    "exercise_charges",
    "shot",
)
ARMAMENT_KEYS = ("default", "fits")
# The quarter bill beyond the gun crews (spec M7 §8a; `docs/design/Design-WorkInAction.md`):
# the sail trimmers by station, the hands at the helm, the powder, and the fighting book's
# priority between the sails and the guns when hands are short; package 73's small-arms
# men and boarders; and (practice and resupply) the men of the powder who fill cartridges.
QUARTER_BILL_KEYS = ("trimmers", "helm", "powder", "priority", "small_arms", "boarders", "filling")
PRIORITIES = ("sail before guns", "guns before sail")

# The hull's profile (package 75; docs/design/Build-Ships.md §5.1): the side, the decks and the
# ports in the fore-and-aft plane, x forward of midships and z above the file's waterline (the
# load line its sill source states), metres, for the drawing and the lee ports' rule (§6, §7).
# The deck words are shared with a gun's `deck` and the 74's bill by deck; a frigate's, a
# sloop's and a cutter's single gun deck is `upper`, and so is the razee's (ZAZ2374's title;
# Winfield 1793-1817 p. 99: docs/design/Design-Ship-Indefatigable.md §3.1).
DECK_WORDS = ("lower", "middle", "upper", "quarterdeck", "forecastle", "roundhouse")
# The profile's keys in the order the generator writes them (`gen_ships.hull_profile`): the
# rail and the half-breadths required, the rest optional.
PROFILE_KEYS = (
    "rail_m",  # [x, z]: the top of the side, taffrail to stem head
    "breadth_m",  # [x, hb_water, hb_rail]: the half-breadths at the water and the rail
    "keel_m",  # [x, z]: K, the post's heel to the forefoot
    "stem_m",  # [x, z]: the stem's fore edge, low to high
    "stern_m",  # [x, z]: the post, the counter, the taffrail, low to high
    "wales_m",  # [x, z_lower, z_upper]: the main wale
    "section_m",  # [z, half_breadth]: the midship section, plank on
    "decks_m",  # {deck: [[x, z], ...]}: each deck at side, over its extent
    "ports_m",  # {deck: [[x, sill_z, half_breadth], ...]}: one side's ports, by deck
    "port_size_m",  # {deck: [width, depth]}
)
# A gun placed so has a port, and stands on one of the profile's port decks where it gives
# them; a pivot and a rail gun fire over the rail (`combat.ports.PORT_PLACES`).
_PORT_GUN_PLACES = ("broadside", "bow", "stern")

# Default load ratings (kN) by class, used with a warning when a file omits one.
DEFAULT_SPAR_RATING_KN: dict[str, float] = {
    "mast": 400.0,
    "topmast": 120.0,
    "topgallant_mast": 45.0,
    "royal_mast": 20.0,
    "bowsprit": 250.0,
    "jib_boom": 60.0,
    "flying_jib_boom": 25.0,
    "yard": 80.0,
    "gaff": 50.0,
    "boom": 60.0,
    "studdingsail_boom": 15.0,
    "lug_yard": 40.0,
    "lateen_yard": 60.0,
    "sprit": 30.0,
}
DEFAULT_LINE_RATING_KN: dict[str, float] = {
    "halyard": 40.0,
    "throat_halyard": 30.0,
    "peak_halyard": 25.0,
    "sheet": 35.0,
    "tack": 35.0,
    "brace": 25.0,
    "lift": 20.0,
    "clewline": 12.0,
    "buntline": 8.0,
    "leechline": 8.0,
    "bowline": 12.0,
    "reef_tackle": 15.0,
    "downhaul": 10.0,
    "outhaul": 15.0,
    "vang": 12.0,
    "guy": 15.0,
    "stay": 150.0,
    "shroud": 120.0,
    "backstay": 100.0,
}


# ---------------------------------------------------------------------------
# The crew section (docs/TechnicalSpec-M3.md §2.3)
# ---------------------------------------------------------------------------

# The stations of a ship's company, in the order the watch bill lists them. The first six
# are the seamen's stations; the ratings line divides the seamen among them.
CREW_STATIONS = (
    "forecastle",
    "fore_top",
    "main_top",
    "mizzen_top",
    "afterguard",
    "waisters",
    "marines",
    "idlers",
)
SEAMAN_STATIONS = CREW_STATIONS[:6]

# The ratings a ship file may share its seamen among, best first.
SEAMAN_RATINGS = ("able", "ordinary", "landsman")
# The ratings a named role may be drawn by (package 73): the seamen's, and the marines'
# for the detachment's officer and sergeant (`crew.model.Rating`).
PERSON_RATINGS = SEAMAN_RATINGS + ("marine", "petty officer", "idler", "officer")
RATINGS_SUM_TOLERANCE = 1e-6  # the shares must add up to one within this

# The idlers' trades (spec §2.1): what the `idlers_by_trade` mapping may name.
IDLER_TRADES = (
    "carpenter's crew",
    "sailmaker's crew",
    "cooper",
    "armourer",
    "cook",
    "steward",
    "servant",
    "surgeon's mate",
    "clerk",
    "master-at-arms's party",
)

# The ship's stores (spec §2.3): numbers only in milestone 3.
STORE_KEYS = (
    "water_tons",
    "provisions_days",
    "spare_sails",
    "spare_spars",
    "cordage_fathoms",
    "sails",  # milestone 3b: the sail room's contents, one entry a sail (spec 3b §6.3)
    "shot_plugs",  # package 73 (spec M7 §14): the carpenter's shot plugs, counted
)
SPARE_SAIL_KEYS = ("kind", "canvas_no", "condition")


class ShipFileError(ValueError):
    """A ship file the engine cannot accept. The message is a sentence."""


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------


@dataclass
class RudderSpec:
    area_m2: float = 2.0
    max_angle_deg: float = 35.0
    rate_deg_s: float = 4.0
    # Package 32e: the blade's depth (its span, keel to the top of the blade), which with
    # the area gives its aspect ratio and so its lift slope (physics/hull.py). None: a
    # blade three times as deep as it is broad.
    span_m: float | None = None


@dataclass(frozen=True)
class HullProfile:
    """The hull's profile as the file gives it (package 75; docs/design/Build-Ships.md §5.1):
    x forward of midships, z above the file's waterline, metres; each line a tuple of points
    in the file's order, and each by-deck line a tuple of (deck word, its points). Read
    through `freesail.ship.profile`, which interpolates it."""

    rail_m: tuple[tuple[float, float], ...]
    breadth_m: tuple[tuple[float, float, float], ...]
    keel_m: tuple[tuple[float, float], ...] = ()
    stem_m: tuple[tuple[float, float], ...] = ()
    stern_m: tuple[tuple[float, float], ...] = ()
    wales_m: tuple[tuple[float, float, float], ...] = ()
    section_m: tuple[tuple[float, float], ...] = ()
    decks_m: tuple[tuple[str, tuple[tuple[float, float], ...]], ...] = ()
    ports_m: tuple[tuple[str, tuple[tuple[float, float, float], ...]], ...] = ()
    port_size_m: tuple[tuple[str, tuple[float, float]], ...] = ()


@dataclass
class HullSpec:
    length_waterline_m: float
    beam_m: float
    draught_m: float
    displacement_kg: float
    gm_m: float
    clr_x_m: float = 0.0
    lateral_area_m2: float | None = None
    hull_speed_kn: float | None = None
    deck_height_m: float = 1.5
    rudder: RudderSpec = field(default_factory=RudderSpec)
    # Package 75: the hull's profile (`HullProfile`); None, a file that gives none (the eight
    # until the shared work writes theirs), drawn and gunned as before.
    profile: HullProfile | None = None

    def __getstate__(self) -> dict[str, Any]:
        """Its state for the checkpoint, the profile only where the file gives one (package
        75), so that a hull without one is pickled as before it."""
        state = dict(self.__dict__)
        if state.get("profile") is None:
            state.pop("profile", None)
        return state


@dataclass
class SparSpec:
    id: str
    cls: str
    x_m: float | None = None
    height_m: float | None = None
    length_m: float | None = None
    on: str | None = None  # the spar this one is hoisted/fixed on (yard on a mast)
    steps_on: str | None = None  # the spar this mast stands on (topmast on lower mast)
    side: str | None = None  # studding sail booms
    brace_limit_deg: float | None = None  # yards
    rake_deg: float | None = None  # masts: positive rakes aft, negative forward (a polacre's fore)
    rating_kn: float | None = None
    # studding sail booms: rigged out at the start or not (spec 3b §7); None takes the default.
    # Package 32b: a running bowsprit takes it too (true: run out to its full length, false:
    # reefed to its housed length).
    rigged_out: bool | None = None
    # Package 32b (spec M5 §23): a cutter's running bowsprit, which runs in and out on the
    # deck through the gammoning iron and is fidded at its reefs. `running` marks it;
    # `housed_length_m` is its outboard length reefed, `length_m` its full outboard length.
    running: bool | None = None
    housed_length_m: float | None = None
    # Package 32e (spec M5 open item 13): a gaff sail's boom names the breadth of the horse
    # its sheet travels on (Steel 1794 vol. I, p. 167, HORSE: "a thick iron rod, fastened
    # at the ends to the inside of the stern of vessels that carry a fore and aft mainsail,
    # for the main sheet to travel on"); the sheet's geometry reads it (evolutions/trim.py).
    horse_m: float | None = None
    # Package 75 (docs/design/Design-ShipsEngineExtensions.md §5.7): the lower mast whose
    # yards are laid aback to heave to, where the file names one (the bilander's main: her
    # main topsail goes to the mast, D4(a)); None, the mast of the most square sail, as
    # before. A lower mast's key, and one mast's at most (`validate`).
    heave_to_aback: bool | None = None

    def __getstate__(self) -> dict[str, Any]:
        """Its state for the checkpoint, `heave_to_aback` only where the file gives it
        (package 75), so that a spar without it is pickled as before it."""
        state = dict(self.__dict__)
        if state.get("heave_to_aback") is None:
            state.pop("heave_to_aback", None)
        return state

    @property
    def parent(self) -> str | None:
        return self.on or self.steps_on


@dataclass
class SailSpec:
    id: str
    cls: str
    area_m2: float
    x_m: float
    centre_height_m: float
    reef_bands: int = 0
    side: str | None = None  # studding sails
    roles: dict[str, str] = field(default_factory=dict)  # yard/mast/gaff/boom/stay/sprit
    cloth_rating_kn: float | None = None
    canvas_no: int | None = None  # the canvas it is made of, 1 the heaviest (spec 3b §6.1)
    bent: bool = True  # false: the sail starts the voyage in the sail room (spec 3b §6.4)
    in_place_of: str | None = None  # the sail it is bent instead of (a storm mizzen: spanker)
    # Package 43b (the proposal's §4.4, the lugger's rig-specific evolution): a dipping lug,
    # its yard slung at a third of its length on one side of the mast and its tack shifted
    # in going about (Forfait 1788 pp. 5 to 6; Steel 1794 vol. I, LUGGER), which must be
    # dipped round the mast to the new lee side; a standing lug (a mizen, the taille-vent
    # tacked at the foot of the mast) is not dipped.
    dipping: bool = False
    # Package 57 (the owner's note of 2026-10-17 on the lug topsail; Steel 1794 vol. I p. 214,
    # ROYALS "Are set flying"): a sail set flying, its yard swayed up from the deck with the
    # sail bent and sent down whole when it is taken in, worked by hands on deck, never
    # reefed aloft. Furled, it is on deck, sent down ("sent down" in the log's words).
    flying: bool = False
    # Package 57: a lug topsail's clew sheeted to the lower lug's yard (its peak), so that it
    # lies as the lower lug lies and on its side of the mast: the lower lug's sail id.
    sheeted_to: str | None = None
    # Package 57: the sail's corners in the fore-and-aft plane as it is cut, for the
    # drawing: [x forward of midships, height above the deck] in metres, as the spars'
    # heights. A lug's [tack, throat, peak, clew]; a staysail's [tack, nock, peak, clew] when
    # it is four-sided, [tack, peak, clew] when it is a triangle. None: drawn by its class's
    # rule from its spars and its area.
    corners_m: list[tuple[float, float]] | None = None
    # Package 75 (docs/design/Design-ShipsEngineExtensions.md §5.1-§5.2): a settee, the
    # bilander's main, a four-cornered sail on a yard hung obliquely and peaked over the stern
    # (Falconer 1780, BILANDER), set and clewed up as a square sail and dipped round the mast
    # as a lug (Lescallier p. 390; D1(a)). A dipping lug with this key, which routes it to its
    # own evolutions: it names its mast and gives its [tack, throat, peak, clew], and is never
    # set flying or sheeted to another sail.
    settee: bool = False
    # Package 75 (Ext §3.1): a lateen mizen course cut at the mast, the 64's and the 74's: its
    # head laced to the yard abaft the mast, its luff to the mast, its foot loose, the yard
    # running on forward with no sail there (Lavery I31-I32). Handled and drawn as a sail on
    # a yard; its curve and trim are the gaff's (`Sail.curve_class`). It names its mast and
    # gives its [tack, throat, peak, clew].
    cut_at_mast: bool = False

    def __getstate__(self) -> dict[str, Any]:
        """Its state for the checkpoint, `settee` and `cut_at_mast` only where the file sets
        them (package 75), so that a sail without them is pickled as before them."""
        state = dict(self.__dict__)
        for key in ("settee", "cut_at_mast"):
            if not state.get(key):
                state.pop(key, None)
        return state


@dataclass
class LineSpec:
    id: str
    cls: str
    of: str
    side: str | None = None
    rating_kn: float | None = None
    # Package 32e: the parts of a sheet's purchase (a threefold purchase: 3), which the
    # sheet's scope in fathoms of fall reads (evolutions/trim.py); 1 for a single rope.
    parts: int = 1


@dataclass
class PostSpec:
    """A station holder: the post, and a name when the file gives one."""

    post: str
    name: str | None = None


@dataclass
class SpareSailSpec:
    """A sail in the sail room (spec 3b §6.3): the sail it is made for, the canvas it is
    made of, and how worn it is."""

    kind: str  # the id of the sail it is made for: "fore.topsail"
    canvas_no: int | None = None  # None: the same number as the sail it is made for
    condition: float = 100.0  # 0..100, as Sail.condition


@dataclass
class StoresSpec:
    water_tons: float = 0.0
    provisions_days: float = 0.0
    spare_sails: int = 0  # with a `sails` list, derived: the number of sails in it
    spare_spars: int = 0  # with a `spars` mapping, derived: the number of spares in it
    cordage_fathoms: float = 0.0
    sails: list[SpareSailSpec] | None = None  # the sail room, when the file lists it
    spars: dict[str, int] | None = None  # the booms by spar class (package 30b), when given so
    shot_plugs: float = 0.0  # the carpenter's shot plugs (package 73, spec M7 §14)


@dataclass
class RationSpec:
    """The ration the ship is victualled by (spec M7b §19; package 54): the table of
    `data/crew/ration.yaml` it is served from, and the water drawn from the ground tier a
    man a day, in gallons, for his drink, his grog and the coppers."""

    table: str = "navy"
    water_gallons: float = 1.0


RATION_KEYS = ("table", "water_gallons")


@dataclass
class PersonRoleSpec:
    """A named role beyond the posts (package 35, spec M5 §22): the role's words, the
    station the person is drawn from at muster, the rating wanted (None: any), and
    whether he is the ship's messenger (the midshipman who passes the word)."""

    role: str
    station: str
    rating: str | None = None
    messenger: bool = False


@dataclass
class QuarterBillSpec:
    """The quarter bill beyond the gun crews (spec M7 §8a; package 70): the sail trimmers
    by station (the men who leave the guns for a brace or a sail), the hands at the helm,
    the powder (the boys and the landsmen passing cartridges), and the fighting book's
    priority when sail work wants more hands than the trimmers give. The gun crews are
    the fit's (`GunSpec.crew`)."""

    trimmers: dict[str, int] = field(default_factory=dict)
    helm: int = 2
    powder: int = 0
    priority: str = "sail before guns"
    # package 73 (spec M7 §11): the small-arms men with the stand of arms' muskets, and
    # the boarders told off from the guns' crews (Luce 1884 ch. XX), beside the marines
    small_arms: int = 0
    boarders: int = 0
    # practice and resupply (between packages 72 and 73): the men who fill cartridges, the
    # quarter gunners and the gunner's crew, one to every four cannon (Falconer 1780,
    # QUARTER-GUNNER, l.14283-14289); None, reckoned so from the guns (`combat.filling`). A
    # plain default, so that a bill pickled before it loads.
    filling: int | None = None


@dataclass
class CrewSpec:
    """The ship's company as the ship file establishes it (spec M3 §2.3)."""

    complement: int
    names: str  # which list in data/crew/names.yaml
    stations: dict[str, int]  # every station in CREW_STATIONS order; absent ones are 0
    ratings: dict[str, float]  # share of the seamen by rating, SEAMAN_RATINGS order
    posts: list[PostSpec]
    idlers_by_trade: dict[str, int]  # in the file's order
    stores: StoresSpec = field(default_factory=StoresSpec)
    people: list[PersonRoleSpec] = field(default_factory=list)  # package 35
    ration: RationSpec = field(default_factory=RationSpec)  # package 54
    quarter_bill: QuarterBillSpec | None = None  # package 70; None: the bill is reckoned

    @property
    def seamen(self) -> int:
        return sum(self.stations[s] for s in SEAMAN_STATIONS)


@dataclass
class GunSpec:
    """One gun of a fit (spec M7 §7; package 70): its kind (long, carronade, swivel), the
    weight of its shot in pounds, its place (broadside, bow, stern, rail), its number and
    side where the place has them, where it stands along the hull (metres from midships,
    forward positive) and its muzzle's height above the water upright, the men who serve
    it by the quarter bill, and its weight in hundredweight (the crew's rule and the
    dismount's). A pivot gun's `arc_deg` is the arc it fires through over either side, from
    and to so many degrees off the bow (PROVISIONAL, the owner's pivot gun folded in by
    package 86: each pivot's arc its own ship's, as `docs/design/Proposal-PivotGun.md` §3
    proposes; since package 75 a pivot must give one, and any other gun has None). Its
    `deck` (package 75) is the deck it stands on, one of `DECK_WORDS`; None, a file that does
    not say (read by nothing yet: the lee ports and the 74's bill by deck will)."""

    id: str
    kind: str
    pounder: float
    place: str
    number: int | None
    side: str | None
    x_m: float
    height_m: float
    crew: int
    weight_cwt: float
    arc_deg: tuple[float, float] | None = None
    deck: str | None = None

    def __getstate__(self) -> dict[str, Any]:
        """Its state for the checkpoint, its deck only where the file names one (package
        75), so that a gun without one is pickled as before it."""
        state = dict(self.__dict__)
        if state.get("deck") is None:
            state.pop("deck", None)
        return state


@dataclass
class FitSpec:
    """A fit of guns with its magazine: the guns, the filled cartridges by the gun's kind and
    calibre, the shot by calibre and kind, and the source the generator names for the whole;
    and (practice and resupply, between packages 72 and 73) a cartridge's charge in pounds by
    kind and calibre (None: `ship.parts.charge_lb`'s), the powder below in barrels, and a
    King's fit's allowance of charges for exercise a month (the Regulations 1806, the
    Gunner, Art. XXI, l.13122-13144). A fit pickled before them has calibre-keyed
    `cartridges` and reads the plain defaults (`ship.parts.fit_levels` splits the keys)."""

    name: str
    guns: list[GunSpec]
    cartridges: dict[tuple[str, float], int] = field(default_factory=dict)
    shot: dict[float, dict[str, int]] = field(default_factory=dict)
    source: str = ""
    charges: dict[tuple[str, float], float] | None = None
    powder_barrels: int = 0
    exercise_charges: int = 0


@dataclass
class ArmamentSpec:
    """The ship's armament: the fits she may carry, and the default the scenario takes
    when it names none. The default may be `UNARMED` (package 75), a file whose ship
    sails with no guns unless a scenario names a fit."""

    default: str
    fits: dict[str, FitSpec]

    def fit(self, name: str | None = None) -> FitSpec | None:
        """The fit named, else the default; None for `UNARMED`, named or by default (package
        75: she carries no guns, as a ship whose file lists no armament)."""
        key = str(name or self.default)
        if key == UNARMED:
            return None
        if key not in self.fits:
            known = ", ".join(sorted(self.fits))
            raise ShipFileError(f"She carries no fit named '{key}'; her fits are {known}.")
        return self.fits[key]


@dataclass
class AnchorSpec:
    """One anchor of the ground tackle (package 34): its kind, the name the hands use,
    its weight, and the cable bent to it: the fathoms (the cables spliced end to end,
    120 fathoms each, Falconer 1780, CABLE), the circumference in inches and the rating
    in kN (the working load, as a line's)."""

    id: str
    kind: str
    name: str
    weight_kg: float
    cable_fathoms: float
    cable_in: float
    cable_kn: float


@dataclass
class GroundTackleSpec:
    anchors: list[AnchorSpec]
    chain: bool = False  # chain cable, where the era allows it; hemp in 1805


@dataclass
class HoldSpec:
    """The hold (package 35, spec M5 §23): what she can stow in tons beyond her own
    stores, which the manifest counts the cargo against."""

    capacity_tons: float
    # Package 43b: a fishing smack's well (Holdsworth 1874 pp. 139 to 140; Steel 1805,
    # WELL), the water-tight compartment amidships open to the sea, in cubic metres; it
    # gives her no buoyancy and its water moves with her (the hull's displacement counts
    # it). None: she has none.
    well_m3: float | None = None


@dataclass
class BoatSpec:
    """One of the ship's boats (package 35, spec M5 §23): its kind (launch, barge,
    pinnace, cutter, yawl, jolly boat, punt), the name the hands use, its length, its
    oars, the crew that mans it and the tons it carries."""

    id: str
    kind: str
    name: str
    length_ft: float
    oars: int
    crew: int
    tons: float


@dataclass
class GearSpec:
    """A piece of fishing gear the vessel carries (package 56, spec M7b §21a): its kind
    (the trawl, the drift nets, the seine, the lines), the name the hands use, and its
    size in the period's terms where the file gives it (a trawl's beam in feet, a fleet's
    or a seine's length in fathoms, the nets in a fleet, the hooks on the lines). The
    gear's evolutions (`data/evolutions/shoot_*.yaml`, `haul_*.yaml`) and its fishing
    (`freesail/world/fishing.py`) read the kind; a vessel shoots only what she carries."""

    id: str
    kind: str
    name: str
    beam_ft: float | None = None
    length_fathoms: float | None = None
    nets: int | None = None
    hooks: int | None = None


@dataclass
class PumpSpec:
    """One of the ship's pumps (package 73, spec M7 §13): its kind (the chain pump of Cole
    and Bentinck, standard in the King's ships by 1805, or the common brake pump), the
    name the hands use, the tons of water an hour it lifts with its hands fresh at it and
    the hands it wants (Falconer 1780, PUMP: the chain pump "wrought by four men,
    discharged a ton of water in 43 seconds and a half"). Read by `freesail/world/water.py`."""

    id: str
    kind: str
    name: str
    tons_per_hour: float
    hands: int


PUMP_KINDS = ("chain", "hand")
PUMP_KEYS = ("id", "kind", "name", "tons_per_hour", "hands")

GEAR_KINDS = ("trawl", "drift nets", "seine", "lines")
GEAR_KEYS = ("id", "kind", "name", "beam_ft", "length_fathoms", "nets", "hooks")

BOAT_KINDS = ("launch", "long-boat", "barge", "pinnace", "cutter", "yawl", "jolly boat", "punt")
BOAT_KEYS = ("id", "kind", "name", "length_ft", "oars", "crew", "tons")
PERSON_ROLE_KEYS = ("role", "station", "rating", "messenger")


@dataclass
class ShipSpec:
    name: str
    rig: str
    hull: HullSpec
    spars: list[SparSpec]
    sails: list[SailSpec]
    lines: list[LineSpec]
    groups: dict[str, list[str]]
    aliases: dict[str, str]
    era_notes: str = ""
    source: str = "<memory>"
    warnings: list[str] = field(default_factory=list)
    crew: CrewSpec | None = None  # None: no crew, and the runner has unlimited hands
    ground_tackle: GroundTackleSpec | None = None  # None: no anchors (package 34)
    hold: HoldSpec | None = None  # None: no room for a cargo (package 35)
    boats: list[BoatSpec] = field(default_factory=list)  # none: no boat to send (package 35)
    gear: list[GearSpec] = field(default_factory=list)  # none: no fishing gear (package 56)
    armament: ArmamentSpec | None = None  # None: no guns, and the gunnery refused in words
    pumps: list[PumpSpec] = field(default_factory=list)  # none: no pumps (package 73)


# ---------------------------------------------------------------------------
# Parsing and validation
# ---------------------------------------------------------------------------

_SAIL_ROLE_KEYS = ("yard", "mast", "gaff", "boom", "stay", "sprit", "halyard_spar")


def _num(d: dict[str, Any], key: str, where: str, source: str, required: bool = True):
    v = d.get(key)
    if v is None:
        if required:
            raise ShipFileError(f"{source}: {where} is missing '{key}'.")
        return None
    if isinstance(v, bool) or not isinstance(v, int | float):
        raise ShipFileError(f"{source}: {where} has '{key}' = {v!r}, which is not a number.")
    return float(v)


def _str(d: dict[str, Any], key: str, where: str, source: str, required: bool = True):
    v = d.get(key)
    if v is None:
        if required:
            raise ShipFileError(f"{source}: {where} is missing '{key}'.")
        return None
    return str(v)


def parse_ship(data: dict[str, Any], source: str = "<memory>") -> ShipSpec:
    """Turn a loaded YAML dictionary into a validated ShipSpec."""
    if not isinstance(data, dict):
        raise ShipFileError(f"{source}: the file is not a mapping at the top level.")
    ship = data.get("ship") or {}
    name = str(ship.get("name") or "").strip()
    if not name:
        raise ShipFileError(f"{source}: 'ship.name' is missing.")
    rig = str(ship.get("rig") or "unspecified")
    era_notes = str(ship.get("era_notes") or "")
    warnings: list[str] = []

    hull = _parse_hull(data.get("hull"), source)
    spars = [_parse_spar(s, i, source) for i, s in enumerate(data.get("spars") or [])]
    sails = [_parse_sail(s, i, source) for i, s in enumerate(data.get("sails") or [])]
    lines = [_parse_line(ln, i, source) for i, ln in enumerate(data.get("lines") or [])]
    groups = {str(k): [str(x) for x in (v or [])] for k, v in (data.get("groups") or {}).items()}
    aliases = {str(k): str(v) for k, v in (data.get("aliases") or {}).items()}

    spec = ShipSpec(
        name=name,
        rig=rig,
        hull=hull,
        spars=spars,
        sails=sails,
        lines=lines,
        groups=groups,
        aliases=aliases,
        era_notes=era_notes,
        source=source,
        warnings=warnings,
        crew=_parse_crew(data["crew"], source) if data.get("crew") is not None else None,
        ground_tackle=(
            _parse_ground_tackle(data["ground_tackle"], source)
            if data.get("ground_tackle") is not None
            else None
        ),
        hold=_parse_hold(data["hold"], source) if data.get("hold") is not None else None,
        boats=_parse_boats(data["boats"], source) if data.get("boats") is not None else [],
        gear=_parse_gear(data["gear"], source) if data.get("gear") is not None else [],
        armament=(
            _parse_armament(data["armament"], source) if data.get("armament") is not None else None
        ),
        pumps=_parse_pumps(data["pumps"], source) if data.get("pumps") is not None else [],
    )
    validate(spec)
    return spec


def _parse_pumps(raw: Any, source: str) -> list[PumpSpec]:
    """The `pumps:` list (package 73, spec M7 §13): each a mapping of PUMP_KEYS."""
    if not isinstance(raw, list):
        raise ShipFileError(f"{source}: 'pumps' is not a list of pumps.")
    pumps: list[PumpSpec] = []
    seen: set[str] = set()
    for i, p in enumerate(raw):
        where = f"pump #{i + 1}"
        if not isinstance(p, dict):
            raise ShipFileError(f"{source}: {where} is not a mapping.")
        for key in p:
            if key not in PUMP_KEYS:
                raise ShipFileError(
                    f"{source}: {where} has '{key}', which is no key of a pump; the keys are "
                    f"{', '.join(PUMP_KEYS)}."
                )
        pid = _str(p, "id", where, source)
        if pid in seen:
            raise ShipFileError(f"{source}: the pump id '{pid}' is given twice.")
        seen.add(pid)
        kind = _str(p, "kind", where, source)
        if kind not in PUMP_KINDS:
            raise ShipFileError(
                f"{source}: {where} is a '{kind}' pump; the kinds are {' or '.join(PUMP_KINDS)}."
            )
        tons = _num(p, "tons_per_hour", where, source)
        hands_n = p.get("hands")
        if isinstance(hands_n, bool) or not isinstance(hands_n, int) or hands_n < 1:
            raise ShipFileError(
                f"{source}: {where} wants {hands_n!r} hands; say a number, one or more."
            )
        pumps.append(PumpSpec(pid, kind, _str(p, "name", where, source), float(tons), int(hands_n)))
    return pumps


def _parse_armament(raw: Any, source: str) -> ArmamentSpec:
    """The `armament:` section (spec M7 §7; package 70): the fits, each with its guns and
    its magazine, and the default fit."""
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: 'armament' is not a mapping.")
    for key in raw:
        if key not in ARMAMENT_KEYS:
            raise ShipFileError(f"{source}: the armament has '{key}', which it does not take.")
    raw_fits = raw.get("fits")
    if not isinstance(raw_fits, dict) or not raw_fits:
        raise ShipFileError(f"{source}: the armament names no fits.")
    fits: dict[str, FitSpec] = {}
    for name, f in raw_fits.items():
        if str(name) == UNARMED:
            # the word is the fit of no guns (package 75): a fit so named could never be had
            raise ShipFileError(
                f"{source}: the armament names a fit '{UNARMED}', the word for no guns; "
                "give the fit another name."
            )
        fits[str(name)] = _parse_fit(str(name), f, source)
    default = str(raw.get("default") or next(iter(fits)))
    if default not in fits and default != UNARMED:
        raise ShipFileError(
            f"{source}: the armament's default fit '{default}' is none of its fits "
            f"({', '.join(fits)}) and not '{UNARMED}'."
        )
    return ArmamentSpec(default=default, fits=fits)


def _parse_fit(name: str, raw: Any, source: str) -> FitSpec:
    where = f"the fit '{name}'"
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: {where} is not a mapping.")
    for key in raw:
        if key not in FIT_KEYS:
            raise ShipFileError(f"{source}: {where} has '{key}', which a fit does not take.")
    raw_guns = raw.get("guns")
    if not isinstance(raw_guns, list) or not raw_guns:
        raise ShipFileError(f"{source}: {where} lists no guns.")
    guns = [_parse_gun(g, i, where, source) for i, g in enumerate(raw_guns)]
    kinds_of: dict[float, list[str]] = {}
    for g in guns:
        kinds = kinds_of.setdefault(g.pounder, [])
        if g.kind not in kinds:
            kinds.append(g.kind)
            kinds.sort(key=GUN_KINDS.index)
    cartridges: dict[tuple[str, float], int] = {}
    for key, n, what in _by_kind(raw.get("cartridges"), "cartridges", where, source):
        if isinstance(key, float):
            # a calibre's cartridges said alone (the shape of packages 70 to 72): for the one
            # kind of the fit that has it
            kinds = kinds_of.get(key, [])
            if len(kinds) > 1:
                p = f"{key:g}"
                raise ShipFileError(
                    f"{source}: {where}'s cartridges of {p} are for guns of two kinds "
                    f"({', '.join(kinds)}); say them by kind: cartridges: "
                    f"{{{', '.join(f'{k}: {{{p}: n}}' for k in kinds)}}}."
                )
            if not kinds:
                raise ShipFileError(
                    f"{source}: {where}'s magazine holds {key:g}-pounder cartridges or shot, "
                    f"and no gun of that calibre."
                )
            key = (kinds[0], key)
        cartridges[key] = cartridges.get(key, 0) + _count(n, what, source)
    charges: dict[tuple[str, float], float] | None = None
    if raw.get("charges") is not None:
        charges = {}
        for key, v, what in _by_kind(raw.get("charges"), "charges", where, source):
            if not isinstance(key, tuple):
                raise ShipFileError(
                    f"{source}: {where}'s charges are said by calibre alone; say them by kind: "
                    f"charges: {{long: {{{key:g}: pounds}}}}."
                )
            if isinstance(v, bool) or not isinstance(v, int | float) or v <= 0:
                raise ShipFileError(
                    f"{source}: {what} is {v!r}; say the pounds of powder in a cartridge."
                )
            charges[key] = float(v)
    for key in list(cartridges) + list(charges or {}):
        if key[1] not in kinds_of or key[0] not in kinds_of[key[1]]:
            raise ShipFileError(
                f"{source}: {where}'s magazine holds cartridges for "
                f"{_gun_words(key[0], key[1])}, and no gun of that kind and calibre."
            )
    shot: dict[float, dict[str, int]] = {}
    for k, kinds in (raw.get("shot") or {}).items():
        if not isinstance(kinds, dict):
            raise ShipFileError(f"{source}: {where}'s shot of {k} is not a mapping by kind.")
        by_kind: dict[str, int] = {}
        for kind, n in kinds.items():
            if str(kind) not in SHOT_KINDS:
                raise ShipFileError(
                    f"{source}: {where}'s shot names the kind '{kind}'; the kinds are "
                    f"{', '.join(SHOT_KINDS)}."
                )
            by_kind[str(kind)] = _count(n, f"{where}'s {kind} shot of {k}", source)
        shot[_pounder(k, where, source)] = by_kind
    calibres = {g.pounder for g in guns}
    for p in shot:
        if p not in calibres:
            raise ShipFileError(
                f"{source}: {where}'s magazine holds {p:g}-pounder cartridges or shot, and no "
                f"gun of that calibre."
            )
    return FitSpec(
        name=name,
        guns=guns,
        cartridges=cartridges,
        shot=shot,
        source=str(raw.get("source") or ""),
        charges=charges,
        powder_barrels=_count(raw.get("powder_barrels", 0), f"{where}'s powder barrels", source),
        exercise_charges=_count(
            raw.get("exercise_charges", 0), f"{where}'s charges for exercise", source
        ),
    )


def _by_kind(raw: Any, what: str, where: str, source: str) -> list[tuple[Any, Any, str]]:
    """A fit's `cartridges:` or `charges:` as (key, value, words) entries: by the gun's kind
    and then its calibre (`long: {12: 55}`), the key `(kind, calibre)`; or by calibre alone
    (`12: 275`, the shape of packages 70 to 72), the key the calibre (practice and resupply,
    between packages 72 and 73)."""
    if raw is None:
        return []
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: {where}'s {what} is not a mapping by kind and calibre.")
    out: list[tuple[Any, Any, str]] = []
    for k, v in raw.items():
        if isinstance(k, str):
            if k not in GUN_KINDS:
                raise ShipFileError(
                    f"{source}: {where}'s {what} name the kind '{k}'; the kinds are "
                    f"{', '.join(GUN_KINDS)}."
                )
            if not isinstance(v, dict):
                raise ShipFileError(
                    f"{source}: {where}'s {what} for the {k} guns is not a mapping by calibre."
                )
            for p, n in v.items():
                pounder = _pounder(p, where, source)
                out.append(((k, pounder), n, f"{where}'s {what} for {_gun_words(k, pounder)}"))
        else:
            out.append((_pounder(k, where, source), v, f"{where}'s {what} of {k}"))
    return out


def _gun_words(kind: str, pounder: float) -> str:
    """'long 12-pounders', '12-pounder carronades', 'half-pounder swivels'."""
    calibre = "half" if pounder == 0.5 else f"{pounder:g}"
    if kind == "long":
        return f"long {calibre}-pounders"
    return f"{calibre}-pounder {kind}s"


def _pounder(v: Any, where: str, source: str) -> float:
    if isinstance(v, bool) or not isinstance(v, int | float) or v <= 0:
        raise ShipFileError(f"{source}: {where} names a calibre of {v!r}; say the pounds of shot.")
    return float(v)


def _parse_gun(g: Any, i: int, where: str, source: str) -> GunSpec:
    at = f"{where}, gun #{i + 1}"
    if not isinstance(g, dict):
        raise ShipFileError(f"{source}: {at} is not a mapping.")
    for key in g:
        if key not in GUN_KEYS:
            raise ShipFileError(f"{source}: {at} has '{key}', which a gun does not take.")
    gid = str(g.get("id") or "").strip()
    if not gid:
        raise ShipFileError(f"{source}: {at} has no id.")
    kind = str(g.get("kind") or "long")
    if kind not in GUN_KINDS:
        raise ShipFileError(
            f"{source}: {at} is a '{kind}'; a gun is one of {', '.join(GUN_KINDS)}."
        )
    place = str(g.get("place") or "broadside")
    if place not in GUN_PLACES:
        raise ShipFileError(
            f"{source}: {at} is placed '{place}'; a gun's place is one of {', '.join(GUN_PLACES)}."
        )
    side = g.get("side")
    if side is not None and str(side) not in SIDES:
        raise ShipFileError(f"{source}: {at} is on the '{side}' side; say starboard or larboard.")
    number = g.get("number")
    if number is not None:
        number = _count(number, f"{at}'s number", source)
    if place == "broadside" and (number is None or side is None):
        raise ShipFileError(f"{source}: {at} is a broadside gun and wants a number and a side.")
    if place == "pivot" and side is not None:
        raise ShipFileError(
            f"{source}: {at} is a pivot gun and has no side; it trains to either side."
        )
    crew = _count(g.get("crew", 1), f"{at}'s crew", source)
    if crew < 1:
        raise ShipFileError(f"{source}: {at} has no crew; a gun wants a man at the least.")
    arc = _pivot_arc(g.get("arc_deg"), place, at, source)
    if place == "pivot" and arc is None:
        # package 75 (Build-Ships.md §3.1 item 13): each pivot's arc is its own ship's, from
        # her rig (§9.2); refused after the side, so a pivot with a side hears of that first
        raise ShipFileError(
            f"{source}: {at} is a pivot gun and gives no arc_deg; a pivot fires through its "
            "own arc, [from, to] degrees off the bow, reckoned from its ship's rig."
        )
    deck = g.get("deck")
    return GunSpec(
        id=gid,
        kind=kind,
        pounder=_pounder(g.get("pounder"), at, source),
        place=place,
        number=number,
        side=str(side) if side is not None else None,
        x_m=float(_num(g, "x_m", at, source, required=False) or 0.0),
        height_m=float(_num(g, "height_m", at, source, required=False) or 0.0),
        crew=crew,
        weight_cwt=float(_num(g, "weight_cwt", at, source, required=False) or 0.0),
        arc_deg=arc,
        deck=str(deck) if deck is not None else None,  # its word checked in validate()
    )


def _pivot_arc(raw: Any, place: str, at: str, source: str) -> tuple[float, float] | None:
    """A pivot gun's `arc_deg: [from, to]`, degrees off the bow over either side (package
    86: per gun, where it had been one arc for every pivot); only a pivot gun takes one."""
    if raw is None:
        return None
    if place != "pivot":
        raise ShipFileError(
            f"{source}: {at} is placed '{place}' and has an arc_deg; only a pivot gun takes "
            "its own arc."
        )
    if not isinstance(raw, list) or len(raw) != 2:
        raise ShipFileError(
            f"{source}: {at}'s arc_deg is [from, to], degrees off the bow; it is {raw!r}."
        )
    try:
        lo, hi = float(raw[0]), float(raw[1])
    except (TypeError, ValueError):
        raise ShipFileError(f"{source}: {at}'s arc_deg is not two numbers: {raw!r}.") from None
    if not 0.0 <= lo < hi <= 180.0:
        raise ShipFileError(
            f"{source}: {at}'s arc_deg runs from {lo:g} to {hi:g} degrees off the bow; it runs "
            "from nought to a hundred and eighty, the first the less."
        )
    return (lo, hi)


def _parse_quarter_bill(raw: Any, source: str) -> QuarterBillSpec:
    """The crew's `quarter_bill:` block (spec M7 §8a; package 70)."""
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: the crew's 'quarter_bill' is not a mapping.")
    for key in raw:
        if key not in QUARTER_BILL_KEYS:
            raise ShipFileError(
                f"{source}: the quarter bill has '{key}', which it does not take "
                f"({', '.join(QUARTER_BILL_KEYS)})."
            )
    trimmers: dict[str, int] = {}
    raw_trimmers = raw.get("trimmers") or {}
    if not isinstance(raw_trimmers, dict):
        raise ShipFileError(f"{source}: the quarter bill's 'trimmers' is not a mapping.")
    for k, v in raw_trimmers.items():
        station = _known(k, CREW_STATIONS, "the station", source)
        trimmers[station] = _count(v, f"the trimmers of the {station}", source)
    priority = str(raw.get("priority") or PRIORITIES[0])
    if priority not in PRIORITIES:
        raise ShipFileError(
            f"{source}: the quarter bill's priority is '{priority}'; say one of "
            f"{', '.join(PRIORITIES)}."
        )
    filling = raw.get("filling")
    return QuarterBillSpec(
        trimmers=trimmers,
        helm=_count(raw.get("helm", 2), "the hands at the helm", source),
        powder=_count(raw.get("powder", 0), "the powder's hands", source),
        priority=priority,
        small_arms=_count(raw.get("small_arms", 0), "the small-arms men", source),
        boarders=_count(raw.get("boarders", 0), "the boarders", source),
        filling=_count(filling, "the hands filling cartridges", source)
        if filling is not None
        else None,
    )


def _parse_hold(raw: Any, source: str) -> HoldSpec:
    """The `hold:` section (package 35): the room for a cargo, in tons."""
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: 'hold' is not a mapping.")
    for key in raw:
        if key not in ("capacity_tons", "well_m3"):
            raise ShipFileError(f"{source}: the hold has '{key}', which it does not take.")
    tons = _num(raw, "capacity_tons", "the hold", source)
    if tons < 0.0:
        raise ShipFileError(
            f"{source}: the hold's capacity is {tons:g} tons; it cannot be less than nothing."
        )
    well = _num(raw, "well_m3", "the hold", source, required=False)
    if well is not None and well < 0.0:
        raise ShipFileError(f"{source}: the well is {well:g} cubic metres; it cannot be less.")
    return HoldSpec(capacity_tons=tons, well_m3=well)


def _parse_boats(raw: Any, source: str) -> list[BoatSpec]:
    """The `boats:` list (package 35): each boat with its kind, name, length, oars, crew
    and tons."""
    if not isinstance(raw, list):
        raise ShipFileError(f"{source}: 'boats' is not a list.")
    boats: list[BoatSpec] = []
    seen: set[str] = set()
    for i, b in enumerate(raw):
        where = f"boat #{i + 1}"
        if not isinstance(b, dict):
            raise ShipFileError(f"{source}: {where} is not a mapping.")
        for key in b:
            if key not in BOAT_KEYS:
                raise ShipFileError(f"{source}: {where} has '{key}', which a boat does not take.")
        bid = _str(b, "id", where, source)
        if bid in seen:
            raise ShipFileError(f"{source}: the boats list '{bid}' twice.")
        seen.add(bid)
        where = f"boat '{bid}'"
        kind = _str(b, "kind", where, source)
        if kind not in BOAT_KINDS:
            raise ShipFileError(
                f"{source}: {where} is of kind '{kind}'; say one of {', '.join(BOAT_KINDS)}."
            )
        boats.append(
            BoatSpec(
                id=bid,
                kind=kind,
                name=_str(b, "name", where, source, required=False) or f"the {kind}",
                length_ft=_num(b, "length_ft", where, source),
                oars=_count(b.get("oars"), f"{where}'s oars", source),
                crew=_count(b.get("crew"), f"{where}'s crew", source),
                tons=_num(b, "tons", where, source),
            )
        )
        if boats[-1].length_ft <= 0.0 or boats[-1].crew <= 0:
            raise ShipFileError(f"{source}: {where} has no length or no crew.")
    return boats


def _parse_gear(raw: Any, source: str) -> list[GearSpec]:
    """The `gear:` list (package 56): each piece of fishing gear with its kind and name,
    and its size where the file gives it."""
    if not isinstance(raw, list):
        raise ShipFileError(f"{source}: 'gear' is not a list.")
    gear: list[GearSpec] = []
    seen: set[str] = set()
    for i, g in enumerate(raw):
        where = f"gear #{i + 1}"
        if not isinstance(g, dict):
            raise ShipFileError(f"{source}: {where} is not a mapping.")
        for key in g:
            if key not in GEAR_KEYS:
                raise ShipFileError(f"{source}: {where} has '{key}', which gear does not take.")
        gid = _str(g, "id", where, source)
        if gid in seen:
            raise ShipFileError(f"{source}: the gear lists '{gid}' twice.")
        seen.add(gid)
        where = f"gear '{gid}'"
        kind = _str(g, "kind", where, source)
        if kind not in GEAR_KINDS:
            raise ShipFileError(
                f"{source}: {where} is of kind '{kind}'; say one of {', '.join(GEAR_KINDS)}."
            )
        nets = _num(g, "nets", where, source, required=False)
        hooks = _num(g, "hooks", where, source, required=False)
        gear.append(
            GearSpec(
                id=gid,
                kind=kind,
                name=_str(g, "name", where, source, required=False) or f"the {kind}",
                beam_ft=_num(g, "beam_ft", where, source, required=False),
                length_fathoms=_num(g, "length_fathoms", where, source, required=False),
                nets=int(nets) if nets is not None else None,
                hooks=int(hooks) if hooks is not None else None,
            )
        )
    return gear


def _parse_ground_tackle(raw: Any, source: str) -> GroundTackleSpec:
    """The `ground_tackle:` section (package 34): the anchors with their cables."""
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: 'ground_tackle' is not a mapping.")
    for key in raw:
        if key not in ("anchors", "chain"):
            raise ShipFileError(f"{source}: the ground tackle has '{key}', which it does not take.")
    chain = raw.get("chain", False)
    if not isinstance(chain, bool):
        raise ShipFileError(f"{source}: the ground tackle's chain = {chain!r}; say true or false.")
    anchors_raw = raw.get("anchors")
    if not isinstance(anchors_raw, list) or not anchors_raw:
        raise ShipFileError(f"{source}: the ground tackle lists no anchors.")
    anchors: list[AnchorSpec] = []
    seen: set[str] = set()
    for i, a in enumerate(anchors_raw):
        where = f"anchor #{i + 1}"
        if not isinstance(a, dict):
            raise ShipFileError(f"{source}: {where} is not a mapping.")
        for key in a:
            if key not in ANCHOR_KEYS:
                raise ShipFileError(
                    f"{source}: {where} has '{key}', which an anchor does not take."
                )
        aid = _str(a, "id", where, source)
        if aid in seen:
            raise ShipFileError(f"{source}: the ground tackle lists '{aid}' twice.")
        seen.add(aid)
        where = f"anchor '{aid}'"
        kind = _str(a, "kind", where, source)
        if kind not in ANCHOR_KINDS:
            raise ShipFileError(
                f"{source}: {where} is of kind '{kind}'; say one of {', '.join(ANCHOR_KINDS)}."
            )
        anchors.append(
            AnchorSpec(
                id=aid,
                kind=kind,
                name=_str(a, "name", where, source, required=False) or aid.replace("_", " "),
                weight_kg=_num(a, "weight_kg", where, source),
                cable_fathoms=_num(a, "cable_fathoms", where, source),
                cable_in=_num(a, "cable_in", where, source),
                cable_kn=_num(a, "cable_kn", where, source),
            )
        )
        for field_name in ("weight_kg", "cable_fathoms", "cable_in", "cable_kn"):
            if getattr(anchors[-1], field_name) <= 0.0:
                raise ShipFileError(f"{source}: {where} has {field_name} of nothing.")
    return GroundTackleSpec(anchors=anchors, chain=chain)


def _parse_hull(h: Any, source: str) -> HullSpec:
    if not isinstance(h, dict):
        raise ShipFileError(f"{source}: 'hull' is missing.")
    where = "hull"
    r = h.get("rudder") or {}
    rudder = RudderSpec(
        area_m2=_num(r, "area_m2", "hull.rudder", source, required=False) or 2.0,
        max_angle_deg=_num(r, "max_angle_deg", "hull.rudder", source, required=False) or 35.0,
        rate_deg_s=_num(r, "rate_deg_s", "hull.rudder", source, required=False) or 4.0,
        span_m=_num(r, "span_m", "hull.rudder", source, required=False),
    )
    return HullSpec(
        length_waterline_m=_num(h, "length_waterline_m", where, source),
        beam_m=_num(h, "beam_m", where, source),
        draught_m=_num(h, "draught_m", where, source),
        displacement_kg=_num(h, "displacement_kg", where, source),
        gm_m=_num(h, "gm_m", where, source),
        clr_x_m=_num(h, "clr_x_m", where, source, required=False) or 0.0,
        lateral_area_m2=_num(h, "lateral_area_m2", where, source, required=False),
        hull_speed_kn=_num(h, "hull_speed_kn", where, source, required=False),
        deck_height_m=_num(h, "deck_height_m", where, source, required=False) or 1.5,
        rudder=rudder,
        profile=_parse_profile(h["profile"], source) if h.get("profile") is not None else None,
    )


# The lines of the hull's profile (package 75; Build-Ships.md §5.1, §5.2), by key: the numbers
# in a point, its words in a refusal, the number that must increase from point to point
# (None: none must) and the numbers that are half-breadths, each more than nothing. The
# by-deck keys' lines are `decks_m`'s and `ports_m`'s.
_PROFILE_LINES: dict[str, tuple[int, str, int | None, tuple[int, ...]]] = {
    "rail_m": (2, "x, z", 0, ()),
    "breadth_m": (3, "x, hb_water, hb_rail", 0, (1, 2)),
    "keel_m": (2, "x, z", 0, ()),
    "stem_m": (2, "x, z", 1, ()),
    "stern_m": (2, "x, z", 1, ()),
    "wales_m": (3, "x, z_lower, z_upper", 0, ()),
    "section_m": (2, "z, half_breadth", None, (1,)),
    "decks_m": (2, "x, z", 0, ()),
    "ports_m": (3, "x, sill_z, half_breadth", 0, (2,)),
}
_PROFILE_BY_DECK = ("decks_m", "ports_m", "port_size_m")
_NUMBER_WORDS = {2: "two", 3: "three"}
# A deck read at the rail's own height is at it and not above it, whatever the last bit of an
# interpolation says.
_PROFILE_EPS_M = 1e-9


def _deck_name(word: str) -> str:
    """A deck word as a refusal says it: the upper deck, but the quarterdeck, the forecastle
    and the roundhouse by their own names."""
    return f"{word} deck" if word in ("lower", "middle", "upper") else word


def _parse_profile(raw: Any, source: str) -> HullProfile:
    """The hull's `profile:` (package 75; Build-Ships.md §5.1), **strict**: a key it does not
    take is refused, as a gun's is, where an unknown hull key outside it is passed over. The
    refusals are §5.2's. That each port gun stands on a triple of its deck is the generator's
    assertion and a test, not a refusal: a hand-written file may carry guns between ports."""
    where = "the hull's profile"
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: {where} is not a mapping.")
    for key in raw:
        if key not in PROFILE_KEYS:
            raise ShipFileError(
                f"{source}: {where} has '{key}', which it does not take; its keys are "
                f"{', '.join(PROFILE_KEYS)}."
            )
    if raw.get("rail_m") is None or raw.get("breadth_m") is None:
        raise ShipFileError(
            f"{source}: {where} wants rail_m and breadth_m, the top of the side and the "
            "half-breadths along it."
        )
    lines = {
        key: _profile_line(raw[key], key, key, source)
        for key in PROFILE_KEYS
        if key not in _PROFILE_BY_DECK and raw.get(key) is not None
    }
    decks = _profile_by_deck(raw.get("decks_m"), "decks_m", None, source)
    deck_lines = dict(decks)
    ports = _profile_by_deck(raw.get("ports_m"), "ports_m", deck_lines, source)
    sizes = _profile_by_deck(raw.get("port_size_m"), "port_size_m", deck_lines, source)
    profile = HullProfile(
        rail_m=lines["rail_m"],
        breadth_m=lines["breadth_m"],
        keel_m=lines.get("keel_m", ()),
        stem_m=lines.get("stem_m", ()),
        stern_m=lines.get("stern_m", ()),
        wales_m=lines.get("wales_m", ()),
        section_m=lines.get("section_m", ()),
        decks_m=decks,
        ports_m=ports,
        port_size_m=sizes,
    )
    for word, pts in decks:
        for x, z in pts:
            rail = rail_at(profile, x)
            if z > rail + _PROFILE_EPS_M:
                raise ShipFileError(
                    f"{source}: the profile's {_deck_name(word)} stands {z:g} m above the water "
                    f"at x {x:g}, above the rail ({rail:.2f} m there)."
                )
    for word, triples in ports:
        for x, sill, _half_breadth in triples:
            rail = rail_at(profile, x)
            if sill >= rail:
                raise ShipFileError(
                    f"{source}: the profile's port on the {_deck_name(word)} at x {x:g} has its "
                    f"sill at {sill:g} m, at or above the rail ({rail:.2f} m there)."
                )
            floor = interp(deck_lines[word], x)
            if sill < floor - _PROFILE_EPS_M:
                raise ShipFileError(
                    f"{source}: the profile's port on the {_deck_name(word)} at x {x:g} has its "
                    f"sill at {sill:g} m, below its deck ({floor:.2f} m there)."
                )
    return profile


def _profile_point(p: Any, n: int, shape: str, what: str, source: str) -> tuple[float, ...]:
    """One point of a profile's line: `n` numbers, each finite."""
    if (
        not isinstance(p, list | tuple)
        or len(p) != n
        or not all(
            isinstance(c, int | float) and not isinstance(c, bool) and math.isfinite(c) for c in p
        )
    ):
        raise ShipFileError(
            f"{source}: the profile's {what} has {p!r}, which is not {_NUMBER_WORDS[n]} "
            f"numbers [{shape}]."
        )
    return tuple(float(c) for c in p)


def _profile_line(raw: Any, key: str, what: str, source: str) -> tuple[tuple[float, ...], ...]:
    """A line of the profile by its key's shape (`_PROFILE_LINES`): one or more points, the
    increasing number increasing and each half-breadth more than nothing."""
    n, shape, rising, breadths = _PROFILE_LINES[key]
    if not isinstance(raw, list) or not raw:
        raise ShipFileError(
            f"{source}: the profile's {what} is not a list of [{shape}] points; give one or more."
        )
    pts = tuple(_profile_point(p, n, shape, what, source) for p in raw)
    if rising is not None:
        axis, way = ("x", "aft to forward") if rising == 0 else ("z", "low to high")
        for a, b in zip(pts, pts[1:], strict=False):
            if not b[rising] > a[rising]:
                raise ShipFileError(
                    f"{source}: the profile's {what} goes from {axis} {a[rising]:g} to "
                    f"{b[rising]:g}; its points run {way}, each {axis} greater than the last."
                )
    for p in pts:
        for i in breadths:
            if not p[i] > 0.0:
                raise ShipFileError(
                    f"{source}: the profile's {what} has a half-breadth of {p[i]:g} m at "
                    f"{list(p)!r}; a half-breadth is more than nothing."
                )
    return pts


def _profile_by_deck(
    raw: Any, key: str, decks: dict[str, Any] | None, source: str
) -> tuple[tuple[str, Any], ...]:
    """A by-deck key of the profile (`decks_m`, `ports_m`, `port_size_m`): each deck a word of
    `DECK_WORDS` and, but in `decks_m` itself, a deck `decks_m` gives; its line (or its port's
    width and depth) in the file's order."""
    if raw is None:
        return ()
    if not isinstance(raw, dict):
        raise ShipFileError(f"{source}: the profile's {key} is not a mapping by deck.")
    out: list[tuple[str, Any]] = []
    for word, v in raw.items():
        word = str(word)
        if word not in DECK_WORDS:
            raise ShipFileError(
                f"{source}: the profile's {key} names the deck '{word}'; a deck is one of "
                f"{', '.join(DECK_WORDS)}."
            )
        if decks is not None and word not in decks:
            raise ShipFileError(
                f"{source}: the profile's {key} gives the {_deck_name(word)}, which its decks_m "
                "does not."
            )
        what = f"{key}.{word}"
        if key == "port_size_m":
            out.append((word, _profile_point(v, 2, "width, depth", what, source)))
        else:
            out.append((word, _profile_line(v, key, what, source)))
    return tuple(out)


def _parse_spar(s: Any, i: int, source: str) -> SparSpec:
    if not isinstance(s, dict):
        raise ShipFileError(f"{source}: spar #{i + 1} is not a mapping.")
    sid = _str(s, "id", f"spar #{i + 1}", source)
    where = f"spar '{sid}'"
    cls = _str(s, "class", where, source)
    if cls not in SPAR_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a spar class. "
            f"Known: {', '.join(sorted(SPAR_CLASSES))}."
        )
    side = _str(s, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    running = _running(s, cls, where, source)
    return SparSpec(
        id=sid,
        cls=cls,
        x_m=_num(s, "x_m", where, source, required=False),
        height_m=_num(s, "height_m", where, source, required=False),
        length_m=_num(s, "length_m", where, source, required=False),
        on=_str(s, "on", where, source, required=False),
        steps_on=_str(s, "steps_on", where, source, required=False),
        side=side,
        brace_limit_deg=_num(s, "brace_limit_deg", where, source, required=False),
        rake_deg=_num(s, "rake_deg", where, source, required=False),
        rating_kn=_num(s, "rating_kn", where, source, required=False),
        rigged_out=_rigged_out(s, cls, where, source, running=bool(running)),
        running=running,
        housed_length_m=_housed_length(s, cls, where, source, running=bool(running)),
        horse_m=_num(s, "horse_m", where, source, required=False),
        heave_to_aback=_heave_to_aback(s, where, source),
    )


def _rigged_out(s: dict, cls: str, where: str, source: str, running: bool = False) -> bool | None:
    """A studding sail boom's starting state (spec 3b §7), if the file gives one; a running
    bowsprit's too (package 32b: out to its full length, or reefed)."""
    value = s.get("rigged_out")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ShipFileError(
            f"{source}: {where} has rigged_out = {value!r}; say true (run out along its yard) "
            "or false (rigged in)."
        )
    if cls != "studdingsail_boom" and not running:
        raise ShipFileError(
            f"{source}: {where} is a {cls.replace('_', ' ')}; only a studding sail boom or a "
            "running bowsprit is rigged out or in."
        )
    return value


def _running(s: dict, cls: str, where: str, source: str) -> bool | None:
    """Whether a bowsprit runs in and out (package 32b), if the file says."""
    value = s.get("running")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ShipFileError(
            f"{source}: {where} has running = {value!r}; say true (a running bowsprit, reefed "
            "and rigged out on deck) or leave it out."
        )
    if cls != "bowsprit":
        raise ShipFileError(
            f"{source}: {where} is a {cls.replace('_', ' ')}; only a bowsprit runs in and out."
        )
    return value


def _housed_length(s: dict, cls: str, where: str, source: str, running: bool) -> float | None:
    """A running bowsprit's outboard length when reefed (package 32b)."""
    value = _num(s, "housed_length_m", where, source, required=False)
    if value is None:
        if running:
            raise ShipFileError(
                f"{source}: {where} is a running bowsprit but gives no 'housed_length_m', its "
                "outboard length when reefed."
            )
        return None
    if not running:
        raise ShipFileError(
            f"{source}: {where} has 'housed_length_m' but is not a running bowsprit "
            "(say running: true on a bowsprit)."
        )
    full = _num(s, "length_m", where, source, required=False)
    if full is None or not 0.0 < value < full:
        raise ShipFileError(
            f"{source}: {where} has housed_length_m = {value:g}; a reefed bowsprit is shorter "
            f"than its full outboard length_m ({full!r}) and longer than nothing."
        )
    return value


def _heave_to_aback(s: dict, where: str, source: str) -> bool | None:
    """Whether this is the mast whose yards are laid aback to heave to (package 75), if the
    file says; `validate` refuses it off a lower mast and on a second one."""
    value = s.get("heave_to_aback")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ShipFileError(
            f"{source}: {where} has heave_to_aback = {value!r}; say true (her yards on this "
            "mast are laid aback to heave to) or leave it out."
        )
    return value


def _parse_sail(s: Any, i: int, source: str) -> SailSpec:
    if not isinstance(s, dict):
        raise ShipFileError(f"{source}: sail #{i + 1} is not a mapping.")
    sid = _str(s, "id", f"sail #{i + 1}", source)
    where = f"sail '{sid}'"
    cls = _str(s, "class", where, source)
    if cls not in SAIL_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a sail class. "
            f"Known: {', '.join(sorted(SAIL_CLASSES))}."
        )
    side = _str(s, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    roles = {k: str(s[k]) for k in _SAIL_ROLE_KEYS if s.get(k) is not None}
    reef = s.get("reef_bands", 0)
    if isinstance(reef, bool) or not isinstance(reef, int) or reef < 0:
        raise ShipFileError(f"{source}: {where} has reef_bands = {reef!r}; use a whole number.")
    bent = s.get("bent", True)
    if not isinstance(bent, bool):
        raise ShipFileError(
            f"{source}: {where} has bent = {bent!r}; say true (bent to its spar) or false "
            f"(in the sail room)."
        )
    dipping = s.get("dipping", False)
    if not isinstance(dipping, bool):
        raise ShipFileError(f"{source}: {where} has dipping = {dipping!r}; say true or false.")
    if dipping and cls != "lug":
        raise ShipFileError(f"{source}: {where} is a {cls} sail; only a lug is dipped.")
    flying = s.get("flying", False)
    if not isinstance(flying, bool):
        raise ShipFileError(f"{source}: {where} has flying = {flying!r}; say true or false.")
    if flying and reef > 0:
        raise ShipFileError(
            f"{source}: {where} is set flying and has {reef} reef band(s); a flying sail is "
            "never reefed aloft, it is taken in whole."
        )
    sheeted_to = _str(s, "sheeted_to", where, source, required=False)
    if sheeted_to is not None and cls != "lug":
        raise ShipFileError(
            f"{source}: {where} is a {cls} sail; only a lug topsail is sheeted to another sail."
        )
    settee = _settee(s, cls, roles, where, source, dipping, flying, sheeted_to)
    cut_at_mast = _cut_at_mast(s, cls, roles, where, source)
    return SailSpec(
        id=sid,
        cls=cls,
        area_m2=_num(s, "area_m2", where, source),
        x_m=_num(s, "x_m", where, source),
        centre_height_m=_num(s, "centre_height_m", where, source),
        reef_bands=reef,
        side=side,
        roles=roles,
        cloth_rating_kn=_num(s, "cloth_rating_kn", where, source, required=False),
        canvas_no=_canvas_no(s.get("canvas_no"), where, source),
        bent=bent,
        in_place_of=_str(s, "in_place_of", where, source, required=False),
        dipping=dipping,
        flying=flying,
        sheeted_to=sheeted_to,
        corners_m=_corners(s.get("corners_m"), where, source),
        settee=settee,
        cut_at_mast=cut_at_mast,
    )


def _settee(
    s: dict,
    cls: str,
    roles: dict[str, str],
    where: str,
    source: str,
    dipping: bool,
    flying: bool,
    sheeted_to: str | None,
) -> bool:
    """Whether the sail is a settee (package 75; docs/design/Design-ShipsEngineExtensions.md
    §5.1-§5.2): a dipping lug that names its mast and gives its four corners, never set
    flying and never sheeted to another sail."""
    value = s.get("settee", False)
    if not isinstance(value, bool):
        raise ShipFileError(f"{source}: {where} has settee = {value!r}; say true or false.")
    if not value:
        return False
    if cls != "lug":
        raise ShipFileError(f"{source}: {where} is a {cls} sail; only a lug is a settee.")
    if not dipping:
        raise ShipFileError(
            f"{source}: {where} is a settee and is not dipping; a settee is a dipping lug "
            "(say dipping: true)."
        )
    if "mast" not in roles:
        raise ShipFileError(
            f"{source}: {where} is a settee and names no 'mast'; a settee names the mast it is "
            "dipped round."
        )
    corners = _corners(s.get("corners_m"), where, source)
    if corners is None or len(corners) != 4:
        raise ShipFileError(
            f"{source}: {where} is a settee and does not give four corners_m; a settee gives its "
            "tack, throat, peak and clew."
        )
    if sheeted_to is not None:
        raise ShipFileError(
            f"{source}: {where} is a settee sheeted to '{sheeted_to}'; a settee's sheet leads "
            "aft to the taffrail, not to another sail."
        )
    if flying:
        raise ShipFileError(
            f"{source}: {where} is a settee set flying; a settee is set and furled on its yard "
            "aloft, never sent down whole."
        )
    return True


def _cut_at_mast(s: dict, cls: str, roles: dict[str, str], where: str, source: str) -> bool:
    """Whether the sail is a lateen cut at the mast (package 75;
    docs/design/Design-ShipsEngineExtensions.md §3.1): a lateen that names the mast its luff
    is laced to and gives its four corners."""
    value = s.get("cut_at_mast", False)
    if not isinstance(value, bool):
        raise ShipFileError(f"{source}: {where} has cut_at_mast = {value!r}; say true or false.")
    if not value:
        return False
    if cls != "lateen":
        raise ShipFileError(f"{source}: {where} is a {cls} sail; only a lateen is cut at the mast.")
    if "mast" not in roles:
        raise ShipFileError(
            f"{source}: {where} is cut at the mast and names no 'mast'; it names the mast its "
            "luff is laced to."
        )
    corners = _corners(s.get("corners_m"), where, source)
    if corners is None or len(corners) != 4:
        raise ShipFileError(
            f"{source}: {where} is cut at the mast and does not give four corners_m; it gives "
            "its tack, throat, peak and clew."
        )
    return True


def _corners(v: Any, where: str, source: str) -> list[tuple[float, float]] | None:
    """A sail's corners (package 57): three or four [x, height] pairs of numbers, or None."""
    if v is None:
        return None
    ok = isinstance(v, list) and len(v) in (3, 4)
    pts: list[tuple[float, float]] = []
    for p in v if ok else []:
        if (
            not isinstance(p, list | tuple)
            or len(p) != 2
            or not all(isinstance(c, int | float) and not isinstance(c, bool) for c in p)
        ):
            ok = False
            break
        pts.append((float(p[0]), float(p[1])))
    if not ok:
        raise ShipFileError(
            f"{source}: {where} has corners_m = {v!r}; give three or four [x, height] pairs "
            "in metres."
        )
    return pts


def _canvas_no(v: Any, where: str, source: str) -> int | None:
    """A canvas number from 1 (the heaviest) to 9, or None when the file gives none."""
    if v is None:
        return None
    if isinstance(v, bool) or not isinstance(v, int) or v not in CANVAS_NUMBERS:
        raise ShipFileError(
            f"{source}: {where} has canvas_no = {v!r}; canvas is numbered 1 (the heaviest) "
            f"to {CANVAS_NUMBERS[-1]} (Luce 1884, App. E)."
        )
    return v


def _parse_line(ln: Any, i: int, source: str) -> LineSpec:
    if not isinstance(ln, dict):
        raise ShipFileError(f"{source}: line #{i + 1} is not a mapping.")
    lid = _str(ln, "id", f"line #{i + 1}", source)
    where = f"line '{lid}'"
    cls = _str(ln, "class", where, source)
    if cls not in LINE_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a line class. "
            f"Known: {', '.join(sorted(LINE_CLASSES))}."
        )
    side = _str(ln, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    parts = ln.get("parts", 1)
    if isinstance(parts, bool) or not isinstance(parts, int) or parts < 1:
        raise ShipFileError(f"{source}: {where} has parts = {parts!r}; a purchase has whole parts.")
    return LineSpec(
        id=lid,
        cls=cls,
        of=_str(ln, "of", where, source),
        side=side,
        rating_kn=_num(ln, "rating_kn", where, source, required=False),
        parts=parts,
    )


def validate(spec: ShipSpec) -> None:
    """Reject a spec the engine could not reason about. Fills in default ratings with warnings."""
    src = spec.source
    spars = {s.id: s for s in spec.spars}
    sails = {s.id: s for s in spec.sails}
    lines = {ln.id: ln for ln in spec.lines}

    # unique ids across all parts
    seen: dict[str, str] = {}
    for kind, items in (("spar", spec.spars), ("sail", spec.sails), ("line", spec.lines)):
        for it in items:
            if it.id in seen:
                raise ShipFileError(
                    f"{src}: id '{it.id}' is used for both a {seen[it.id]} and a {kind}."
                )
            seen[it.id] = kind

    missing_ratings: dict[tuple[str, str, float], list[str]] = {}

    # spars: parents exist, are spars, classes make sense, chains reach the hull, no cycles
    for s in spec.spars:
        if s.on and s.steps_on:
            raise ShipFileError(f"{src}: spar '{s.id}' has both 'on' and 'steps_on'; use one.")
        parent = s.parent
        if parent is None:
            if s.cls not in ROOT_SPAR_CLASSES:
                raise ShipFileError(
                    f"{src}: spar '{s.id}' is class '{s.cls}' but has no 'on' or 'steps_on'; "
                    f"only a mast or bowsprit stands on the hull by itself."
                )
        elif parent not in spars:
            raise ShipFileError(
                f"{src}: spar '{s.id}' is on '{parent}', but there is no spar with that id."
            )
        if s.cls == "studdingsail_boom" and s.side is None and not _on_fore_and_aft(s, spars):
            raise ShipFileError(f"{src}: studding sail boom '{s.id}' needs a 'side'.")
        if s.rake_deg is not None:
            if s.cls not in ("mast", "topmast", "topgallant_mast", "royal_mast"):
                raise ShipFileError(
                    f"{src}: spar '{s.id}' is a {s.cls}; only a mast takes 'rake_deg'."
                )
            if not -30.0 <= s.rake_deg <= 30.0:
                raise ShipFileError(
                    f"{src}: spar '{s.id}' has rake_deg = {s.rake_deg:g}; a mast rakes between "
                    f"-30 (forward) and 30 (aft) degrees."
                )
        if s.heave_to_aback is not None and s.cls != "mast":
            raise ShipFileError(
                f"{src}: spar '{s.id}' is a {s.cls.replace('_', ' ')}; only a lower mast takes "
                "'heave_to_aback', its yards laid aback to heave to."
            )
        if s.rating_kn is None:
            s.rating_kn = DEFAULT_SPAR_RATING_KN[s.cls]
            missing_ratings.setdefault(("spar", s.cls, s.rating_kn), []).append(s.id)
    for s in spec.spars:
        chain: list[str] = []
        cur: SparSpec | None = s
        while cur is not None:
            if cur.id in chain:
                path = " -> ".join(chain + [cur.id])
                raise ShipFileError(f"{src}: spar '{s.id}' stands on itself through {path}.")
            chain.append(cur.id)
            cur = spars.get(cur.parent) if cur.parent else None
    # the mast laid aback to heave to (package 75): one at most
    aback = [s.id for s in spec.spars if s.heave_to_aback]
    if len(aback) > 1:
        raise ShipFileError(
            f"{src}: spar '{aback[1]}' is laid aback to heave to as well as '{aback[0]}'; she "
            "heaves to with one mast's yards laid aback, so name one mast."
        )

    # sails: class requirements, roles exist and are the right kind
    for sl in spec.sails:
        req = SAIL_ROLE_REQUIREMENTS[sl.cls]
        opt = SAIL_OPTIONAL_ROLES.get(sl.cls, {})
        for role, allowed in req.items():
            target = sl.roles.get(role)
            if target is None:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is class '{sl.cls}' but has no '{role}'."
                )
            _check_sail_role(spec, sl, role, target, allowed, spars, lines)
        for role, allowed in opt.items():
            target = sl.roles.get(role)
            if target is not None:
                _check_sail_role(spec, sl, role, target, allowed, spars, lines)
        for role in sl.roles:
            if role not in req and role not in opt:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is class '{sl.cls}' and does not take a '{role}'."
                )
        if sl.cls == "studding" and sl.side is None:
            boom = spars.get(sl.roles.get("boom", ""))
            if boom is None or not (
                boom.cls in FORE_AND_AFT_SPAR_CLASSES or _on_fore_and_aft(boom, spars)
            ):
                raise ShipFileError(f"{src}: studding sail '{sl.id}' needs a 'side'.")
        if sl.sheeted_to is not None:
            host = sails.get(sl.sheeted_to)
            if host is None or host is sl or host.cls != "lug":
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is sheeted to '{sl.sheeted_to}', which is not "
                    "another lug in the ship."
                )
        if sl.in_place_of is not None:
            other = sails.get(sl.in_place_of)
            if other is None or other is sl:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is bent in place of '{sl.in_place_of}', which is not "
                    f"another sail in the ship."
                )
        if sl.cls == "jibheaded" and "stay" not in sl.roles and "mast" not in sl.roles:
            raise ShipFileError(
                f"{src}: sail '{sl.id}' is jib-headed but names neither a 'stay' to hank to "
                f"nor a 'mast' to hoist on."
            )

    # lines: target exists and is a permitted kind
    for ln in spec.lines:
        kinds = LINE_TARGET_KINDS[ln.cls]
        if ln.of in spars:
            kind = "spar"
        elif ln.of in sails:
            kind = "sail"
        else:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is of '{ln.of}', but there is no spar or sail with that id."
            )
        if kind not in kinds:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is a {ln.cls}, which cannot be of a {kind} ('{ln.of}')."
            )
        if ln.cls == "brace" and spars[ln.of].cls not in YARD_LIKE_CLASSES:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is a brace of '{ln.of}', which is a {spars[ln.of].cls}, "
                f"not a yard."
            )
        if ln.rating_kn is None:
            ln.rating_kn = DEFAULT_LINE_RATING_KN[ln.cls]
            missing_ratings.setdefault(("line", ln.cls, ln.rating_kn), []).append(ln.id)

    for (kind, cls, rating), ids in missing_ratings.items():
        shown = ", ".join(ids[:3]) + (", ..." if len(ids) > 3 else "")
        spec.warnings.append(
            f"{len(ids)} {kind}{'s' if len(ids) > 1 else ''} of class {cls} have no rating_kn "
            f"({shown}); using the default of {rating:g} kN."
        )

    # groups and aliases: members exist; names do not collide with ids
    for g, members in spec.groups.items():
        if g in seen:
            raise ShipFileError(f"{src}: group '{g}' has the same name as a part.")
        for m in members:
            if m not in seen:
                raise ShipFileError(f"{src}: group '{g}' lists '{m}', which is not a part.")
    for a, target in spec.aliases.items():
        if a in seen:
            raise ShipFileError(f"{src}: alias '{a}' has the same name as a part.")
        if target not in seen and target not in spec.groups:
            raise ShipFileError(
                f"{src}: alias '{a}' points at '{target}', which is not a part or a group."
            )

    # the sail room: every sail in it is made for a sail of this ship
    room = spec.crew.stores.sails if spec.crew is not None else None
    for spare in room or []:
        if spare.kind not in sails:
            raise ShipFileError(
                f"{src}: the sail room holds a sail made for '{spare.kind}', which is not a sail "
                f"in the ship."
            )

    # the armament (package 70): a gun's id is a part's, unique against the rig's and within
    # its fit; a broadside number is one gun a side. A gun's deck (package 75) is a deck word,
    # and where the hull's profile gives ports, a gun with a port names a deck that has them.
    profile = spec.hull.profile
    port_decks = [word for word, _triples in profile.ports_m] if profile is not None else []
    if spec.armament is not None:
        for fit in spec.armament.fits.values():
            ids: set[str] = set()
            pairs: set[tuple[int, str]] = set()
            for g in fit.guns:
                if g.id in seen:
                    raise ShipFileError(
                        f"{src}: the gun '{g.id}' of the fit '{fit.name}' has a part's id."
                    )
                if g.id in ids:
                    raise ShipFileError(
                        f"{src}: the fit '{fit.name}' lists the gun '{g.id}' twice."
                    )
                ids.add(g.id)
                if g.deck is not None and g.deck not in DECK_WORDS:
                    raise ShipFileError(
                        f"{src}: the gun '{g.id}' of the fit '{fit.name}' stands on the "
                        f"'{g.deck}' deck; a deck is one of {', '.join(DECK_WORDS)}."
                    )
                if (
                    g.deck is not None
                    and port_decks
                    and g.place in _PORT_GUN_PLACES
                    and g.deck not in port_decks
                ):
                    raise ShipFileError(
                        f"{src}: the gun '{g.id}' of the fit '{fit.name}' is a {g.place} gun "
                        f"on the {_deck_name(g.deck)}, where the hull's profile gives no ports "
                        f"(the decks with ports: {', '.join(port_decks)})."
                    )
                if g.place == "broadside":
                    key = (int(g.number or 0), str(g.side))
                    if key in pairs:
                        raise ShipFileError(
                            f"{src}: the fit '{fit.name}' has two No. {g.number} guns to {g.side}."
                        )
                    pairs.add(key)
    # the quarter bill's trimmers are men of their stations
    bill = spec.crew.quarter_bill if spec.crew is not None else None
    if bill is not None:
        for station, n in bill.trimmers.items():
            if n > spec.crew.stations.get(station, 0):
                raise ShipFileError(
                    f"{src}: the quarter bill wants {n} trimmers of the {station}, and the "
                    f"station has {spec.crew.stations.get(station, 0)}."
                )


def _on_fore_and_aft(spar: SparSpec, spars: dict[str, SparSpec]) -> bool:
    """A spar that stands on a gaff sail's boom or gaff (a ringtail boom), which lies in the
    sail's plane and has no side of its own."""
    parent = spars.get(spar.parent) if spar.parent else None
    return parent is not None and parent.cls in FORE_AND_AFT_SPAR_CLASSES


def _check_sail_role(
    spec: ShipSpec,
    sl: SailSpec,
    role: str,
    target: str,
    allowed: frozenset[str],
    spars: dict[str, SparSpec],
    lines: dict[str, LineSpec],
) -> None:
    src = spec.source
    if role == "stay":
        ln = lines.get(target)
        if ln is None or ln.cls not in STANDING_LINE_CLASSES:
            raise ShipFileError(
                f"{src}: sail '{sl.id}' hanks to stay '{target}', "
                f"which is not a stay in the lines list."
            )
        return
    sp = spars.get(target)
    if sp is None:
        raise ShipFileError(
            f"{src}: sail '{sl.id}' names '{target}' as its {role}, but there is no such spar."
        )
    if allowed and sp.cls not in allowed:
        raise ShipFileError(
            f"{src}: sail '{sl.id}' names '{target}' as its {role}, but that is a {sp.cls}; "
            f"expected {' or '.join(sorted(allowed))}."
        )


# ---------------------------------------------------------------------------
# The crew section
# ---------------------------------------------------------------------------


def _count(v: Any, what: str, source: str) -> int:
    """A whole number of men (or casks, or sails), not negative."""
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise ShipFileError(f"{source}: {what} is {v!r}; it must be a whole number, not negative.")
    return v


def _parse_spare_spars(raw: dict[Any, Any], source: str) -> dict[str, int]:
    """The stores' `spare_spars` given by class (package 30b): each key a spar class, each
    value the number of spares of it on the booms, in the file's order."""
    out: dict[str, int] = {}
    for k, v in raw.items():
        cls = str(k).strip()
        if cls not in SPAR_CLASSES:
            raise ShipFileError(
                f"{source}: the spare spars name the class '{cls}', which is not a spar class. "
                f"Known: {', '.join(sorted(SPAR_CLASSES))}."
            )
        out[cls] = _count(v, f"the number of spare {cls.replace('_', ' ')}s", source)
    return out


def _known(name: Any, known: tuple[str, ...], what: str, source: str) -> str:
    name = str(name)
    if name not in known:
        raise ShipFileError(
            f"{source}: the crew section names {what} '{name}', which is not one the engine "
            f"knows. Known: {', '.join(known)}."
        )
    return name


def _parse_sail_room(raw: Any, source: str) -> list[SpareSailSpec]:
    """The stores' `sails:` list (spec 3b §6.3): each entry a sail in the sail room."""
    if not isinstance(raw, list):
        raise ShipFileError(f"{source}: the sail room ('stores.sails') is not a list of sails.")
    out: list[SpareSailSpec] = []
    for i, e in enumerate(raw):
        where = f"sail #{i + 1} in the sail room"
        if not isinstance(e, dict) or not str(e.get("kind") or "").strip():
            raise ShipFileError(f"{source}: {where} does not say which sail it is made for.")
        for key in e:
            if key not in SPARE_SAIL_KEYS:
                raise ShipFileError(f"{source}: {where} has '{key}', which it does not take.")
        condition = e.get("condition", 100.0)
        if (
            isinstance(condition, bool)
            or not isinstance(condition, int | float)
            or not 0.0 <= condition <= 100.0
        ):
            raise ShipFileError(
                f"{source}: {where} has condition = {condition!r}; a sail's condition runs from "
                f"0 (worn out) to 100 (new)."
            )
        out.append(
            SpareSailSpec(
                kind=str(e["kind"]).strip(),
                canvas_no=_canvas_no(e.get("canvas_no"), where, source),
                condition=float(condition),
            )
        )
    return out


def _parse_crew(c: Any, source: str) -> CrewSpec:
    """Parse and check the ship file's `crew:` section (spec M3 §2.3)."""
    if not isinstance(c, dict):
        raise ShipFileError(f"{source}: 'crew' is not a mapping.")
    for key in c:
        if key not in (
            "complement",
            "names",
            "stations",
            "ratings",
            "posts",
            "idlers_by_trade",
            "stores",
            "people",  # package 35
            "ration",  # package 54
            "quarter_bill",  # package 70
        ):
            raise ShipFileError(f"{source}: the crew section has '{key}', which it does not take.")

    if c.get("complement") is None:
        raise ShipFileError(f"{source}: the crew section is missing 'complement'.")
    complement = _count(c["complement"], "the crew's complement", source)
    if complement == 0:
        raise ShipFileError(f"{source}: the crew's complement is 0; a ship needs hands.")

    names = str(c.get("names") or "").strip()
    if not names:
        raise ShipFileError(
            f"{source}: the crew section is missing 'names', the list the company is drawn from."
        )

    raw_stations = c.get("stations")
    if not isinstance(raw_stations, dict) or not raw_stations:
        raise ShipFileError(f"{source}: the crew section is missing 'stations'.")
    stations = {s: 0 for s in CREW_STATIONS}
    for k, v in raw_stations.items():
        name = _known(k, CREW_STATIONS, "the station", source)
        stations[name] = _count(v, f"the {name} station's number", source)

    seamen = sum(stations[s] for s in SEAMAN_STATIONS)
    raw_ratings = c.get("ratings") or {}
    if not isinstance(raw_ratings, dict):
        raise ShipFileError(f"{source}: the crew's 'ratings' is not a mapping.")
    if seamen and not raw_ratings:
        raise ShipFileError(
            f"{source}: the crew section has {seamen} seamen but no 'ratings' to rate them by."
        )
    ratings = {r: 0.0 for r in SEAMAN_RATINGS}
    for k, v in raw_ratings.items():
        name = _known(k, SEAMAN_RATINGS, "the rating", source)
        if isinstance(v, bool) or not isinstance(v, int | float) or not 0.0 <= v <= 1.0:
            raise ShipFileError(
                f"{source}: the {name} rating's share is {v!r}; a share is a number from 0 to 1."
            )
        ratings[name] = float(v)
    if raw_ratings:
        total = sum(ratings.values())
        if abs(total - 1.0) > RATINGS_SUM_TOLERANCE:
            raise ShipFileError(
                f"{source}: the crew's ratings add up to {total:g}; they are shares of the "
                f"seamen and must add up to one."
            )

    raw_posts = c.get("posts") or []
    if not isinstance(raw_posts, list):
        raise ShipFileError(f"{source}: the crew's 'posts' is not a list.")
    posts: list[PostSpec] = []
    for i, p in enumerate(raw_posts):
        if not isinstance(p, dict) or not str(p.get("post") or "").strip():
            raise ShipFileError(
                f"{source}: post #{i + 1} in the crew section does not say which post it is."
            )
        name = p.get("name")
        posts.append(
            PostSpec(post=str(p["post"]).strip(), name=str(name).strip() if name else None)
        )

    on_stations = sum(stations.values())
    if on_stations + len(posts) != complement:
        raise ShipFileError(
            f"{source}: the crew's stations hold {on_stations} and the posts {len(posts)}, "
            f"which make {on_stations + len(posts)}; the complement is {complement}. "
            f"The stations and the posts together must make up the complement."
        )

    raw_trades = c.get("idlers_by_trade") or {}
    if not isinstance(raw_trades, dict):
        raise ShipFileError(f"{source}: the crew's 'idlers_by_trade' is not a mapping.")
    trades: dict[str, int] = {}
    for k, v in raw_trades.items():
        name = _known(k, IDLER_TRADES, "the trade", source)
        trades[name] = _count(v, f"the number of the {name}", source)
    if sum(trades.values()) != stations["idlers"]:
        raise ShipFileError(
            f"{source}: the crew has {stations['idlers']} idlers, but 'idlers_by_trade' makes "
            f"{sum(trades.values())}; the trades must make up the idlers."
        )

    raw_stores = c.get("stores") or {}
    if not isinstance(raw_stores, dict):
        raise ShipFileError(f"{source}: the crew's 'stores' is not a mapping.")
    stores = StoresSpec()
    for k, v in raw_stores.items():
        name = _known(k, STORE_KEYS, "the store", source)
        if name == "sails":
            stores.sails = _parse_sail_room(v, source)
        elif name == "spare_spars" and isinstance(v, dict):
            stores.spars = _parse_spare_spars(v, source)
            stores.spare_spars = sum(stores.spars.values())
        elif name in ("spare_sails", "spare_spars"):
            setattr(stores, name, _count(v, f"the {name.replace('_', ' ')}", source))
        else:
            if isinstance(v, bool) or not isinstance(v, int | float) or v < 0:
                raise ShipFileError(
                    f"{source}: the store '{name}' is {v!r}; it must be a number, not negative."
                )
            setattr(stores, name, float(v))
    if stores.sails is not None:
        if "spare_sails" in raw_stores and stores.spare_sails != len(stores.sails):
            raise ShipFileError(
                f"{source}: the stores give {stores.spare_sails} spare sails but the sail room "
                f"lists {len(stores.sails)}; give the list alone, and the count follows from it."
            )
        stores.spare_sails = len(stores.sails)

    raw_people = c.get("people") or []
    if not isinstance(raw_people, list):
        raise ShipFileError(f"{source}: the crew's 'people' is not a list.")
    people: list[PersonRoleSpec] = []
    for i, p in enumerate(raw_people):
        where = f"person #{i + 1} of the crew's people"
        if not isinstance(p, dict) or not str(p.get("role") or "").strip():
            raise ShipFileError(f"{source}: {where} does not say which role it is.")
        for key in p:
            if key not in PERSON_ROLE_KEYS:
                raise ShipFileError(f"{source}: {where} has '{key}', which a role does not take.")
        station = _known(p.get("station", "afterguard"), CREW_STATIONS, "the station", source)
        rating = p.get("rating")
        if rating is not None:
            # package 73: the marines' officer and sergeant are drawn by the rating `marine`
            rating = _known(rating, PERSON_RATINGS, "the rating", source)
        messenger = p.get("messenger", False)
        if not isinstance(messenger, bool):
            raise ShipFileError(
                f"{source}: {where}'s messenger = {messenger!r}; say true or false."
            )
        people.append(
            PersonRoleSpec(
                role=str(p["role"]).strip(), station=station, rating=rating, messenger=messenger
            )
        )

    return CrewSpec(
        complement=complement,
        names=names,
        stations=stations,
        ratings=ratings,
        posts=posts,
        idlers_by_trade=trades,
        stores=stores,
        people=people,
        ration=_parse_ration(c.get("ration"), source),
        quarter_bill=(
            _parse_quarter_bill(c["quarter_bill"], source)
            if c.get("quarter_bill") is not None
            else None
        ),
    )


def _parse_ration(r: Any, source: str) -> RationSpec:
    """The crew's `ration:` block (package 54): the table's name and the water a man a
    day; absent, the Navy's table and a gallon."""
    if r is None:
        return RationSpec()
    if not isinstance(r, dict):
        raise ShipFileError(f"{source}: the crew's 'ration' is not a mapping.")
    for key in r:
        if key not in RATION_KEYS:
            raise ShipFileError(f"{source}: the crew's ration has '{key}', which it does not take.")
    spec = RationSpec()
    if r.get("table") is not None:
        spec.table = str(r["table"]).strip()
    if r.get("water_gallons") is not None:
        v = r["water_gallons"]
        if isinstance(v, bool) or not isinstance(v, int | float) or v < 0:
            raise ShipFileError(
                f"{source}: the ration's water_gallons is {v!r}; it must be a number, not negative."
            )
        spec.water_gallons = float(v)
    return spec
