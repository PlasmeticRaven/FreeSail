"""Orders, the imperative dialect: a table of orders against both reference ships.

Each row of TABLE is (ship, order text, expectation). An expectation is
either `ok(...)`, which says what should have happened (the log kind, the
evolutions the runner was asked to start, the parts named), or `no(...)`,
which says the order is refused and what its sentence must mention. The
runner (package 7) is stood in for by FakeRunner, which records what it was
asked to start and refuses subjects it was told to refuse.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from freesail import orders, units
from freesail.core.world import Scenario, World
from freesail.orders import resolve
from freesail.orders.errors import AmbiguousNounError, OrderError, UnknownNounError
from freesail.orders.grammar import parse
from freesail.ship.graph import Ship
from freesail.ship.loader import load_spec
from freesail.ship.parts import HelmMode, LineState, SailState

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = {
    "frigate": ROOT / "data" / "ships" / "frigate-36.yaml",
    "schooner": ROOT / "data" / "ships" / "topsail-schooner.yaml",
    "cutter": ROOT / "data" / "ships" / "cutter.yaml",
    "brig": ROOT / "data" / "ships" / "brig.yaml",
}
SPECS = {name: load_spec(path) for name, path in SHIP_FILES.items()}


class FakeRunner:
    """Stands in for package 7's Runner: records starts, refuses named subjects."""

    def __init__(self, refuse: dict[str, str] | None = None):
        self.started: list[tuple[str, str, dict[str, Any]]] = []
        self.refuse = refuse or {}

    def start(self, ship: Ship, evolution_id: str, subject_id: str, params=None) -> str:
        if subject_id in self.refuse:
            raise OrderError(self.refuse[subject_id])
        self.started.append((evolution_id, subject_id, dict(params or {})))
        return f"Started {evolution_id} on {subject_id}."


def make(which: str, tack: str = "starboard", refuse: dict[str, str] | None = None):
    ship = Ship(SPECS[which])
    runner = FakeRunner(refuse)
    ship.extra["evolutions"] = runner
    ship.dyn.apparent_wind_angle = math.radians(40 if tack == "starboard" else -40)
    ship.dyn.apparent_wind_speed = 8.0  # "to the wind" needs a wind to brace to
    return ship, runner


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------


@dataclass
class ok:
    kind: str = "evolution.started"
    evo: str | None = None  # every started evolution has this id
    subjects: list[str] | set[str] | None = None  # exactly these subjects (set: any order)
    count: int | None = None  # this many evolutions started
    params: dict[str, Any] | None = None  # these keys and values in every start
    text: list[str] = field(default_factory=list)  # substrings of the log line
    data: dict[str, Any] | None = None  # these keys and values in the returned data


@dataclass
class no:
    mentions: list[str] = field(default_factory=list)  # substrings of the refusal
    kind: type = OrderError


F, S, C, B = "frigate", "schooner", "cutter", "brig"

TABLE: list[tuple[str, str, ok | no]] = [
    # -- setting sail, plain and period phrasings ------------------------------
    (F, "set the fore topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "Set the fore topsail.", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "SET THE FORE TOPSAIL", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "set fore topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "set fore.topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "set the fore tops'l", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "set the fore topsl", ok(evo="set_square", subjects=["fore.topsail"])),
    (F, "loose and set the main topsail", ok(evo="set_square", subjects=["main.topsail"])),
    (F, "make sail on the main topgallant", ok(evo="set_square", subjects=["main.topgallant"])),
    (F, "set the main t'gallant", ok(evo="set_square", subjects=["main.topgallant"])),
    (F, "set the main topgallant sail", ok(evo="set_square", subjects=["main.topgallant"])),
    (F, "set the fore royal", ok(evo="set_square", subjects=["fore.royal"])),
    (F, "set the foresail", ok(evo="set_square", subjects=["fore.course"])),
    (F, "set the fore course", ok(evo="set_square", subjects=["fore.course"])),
    (F, "set the mainsail", ok(evo="set_square", subjects=["main.course"])),
    (F, "set the spanker", ok(evo="set_gaff", subjects=["mizzen.spanker"])),
    (F, "set the driver", ok(evo="set_gaff", subjects=["mizzen.spanker"])),
    (F, "set the mizzen", ok(evo="set_gaff", subjects=["mizzen.spanker"])),
    (F, "hoist the jib", ok(evo="set_jibheaded", subjects=["jib"])),
    (F, "set the flying jib", ok(evo="set_jibheaded", subjects=["flying_jib"])),
    (
        F,
        "set the fore topmast staysail",
        ok(evo="set_jibheaded", subjects=["fore.topmast_staysail"]),
    ),
    (
        F,
        "set the fore topmast stays'l",
        ok(evo="set_jibheaded", subjects=["fore.topmast_staysail"]),
    ),
    (F, "set the topsails", ok(evo="set_square", count=3)),
    (
        F,
        "set the royals",
        ok(evo="set_square", subjects={"fore.royal", "main.royal", "mizzen.royal"}),
    ),
    (F, "set the t'gallants", ok(evo="set_square", count=3)),
    (F, "set the courses", ok(evo="set_square", subjects={"fore.course", "main.course"})),
    (F, "set the headsails", ok(evo="set_jibheaded", count=3)),
    (F, "set the square sails", ok(evo="set_square", count=11)),
    (F, "set the fore-and-aft sails", ok(count=5)),
    (F, "set plain sail", ok(count=11, text=["Set plain sail"])),
    (F, "set the plain sail", ok(count=11)),
    (F, "make all sail", ok(count=26, text=["Make all sail"])),
    # -- studding sails and sides ------------------------------------------------
    (F, "set studdingsails, both sides", ok(evo="set_studding", count=10)),
    (F, "set the stuns'ls both sides", ok(evo="set_studding", count=10)),
    (F, "set the kites", ok(evo="set_studding", count=10)),
    (F, "set the studdingsails, starboard", ok(evo="set_studding", count=5)),
    (F, "set the studding sails, port", ok(evo="set_studding", count=5, data={"side": "larboard"})),
    (
        F,
        "set the fore topmast studdingsail, starboard",
        ok(evo="set_studding", subjects=["fore.topmast.studdingsail.starboard"]),
    ),
    (
        F,
        "set the larboard fore topmast stuns'l",
        ok(evo="set_studding", subjects=["fore.topmast.studdingsail.larboard"]),
    ),
    (
        F,
        "set the port fore topmast studdingsail",
        ok(evo="set_studding", subjects=["fore.topmast.studdingsail.larboard"]),
    ),
    (
        F,
        "set the fore topmast studdingsails",
        ok(evo="set_studding", count=2),
    ),
    (F, "set the fore topmast studdingsail", no(["Which fore topmast studdingsail", "both sides"])),
    (F, "set the fore topsail, weather", no(["has no weather side"])),
    (F, "set the studdingsails, starboard, larboard", no(["Two sides"])),
    # -- ambiguity and unknown nouns ------------------------------------------
    (
        F,
        "set the topsail",
        no(["fore topsail", "main topsail", "mizzen topsail", "say which"], AmbiguousNounError),
    ),
    (F, "set the topgallant", no(["fore topgallant", "mizzen topgallant"], AmbiguousNounError)),
    (
        F,
        "set the mizzen topgallant studdingsail",
        no(["no such part", "did you mean"], UnknownNounError),
    ),
    (F, "set the fore topsel", no(["no such part", "fore topsail"], UnknownNounError)),
    (F, "set the gaff topsail", no(["no such part"], UnknownNounError)),
    (F, "set", no(["Set what?"])),
    # the anchor let go (package 34): a ground-tackle order, not a line's
    (F, "let go the best bower", ok(kind="evolution.started")),
    (F, "let go the anchor", ok(kind="evolution.started")),
    (F, "come to an anchor with the small bower", ok(kind="evolution.started")),
    (F, "veer to ninety fathoms", ok(kind="evolution.started")),
    (F, "veer cable", ok(kind="evolution.started")),
    (F, "veer to the moon", no(["Veer how much?"])),
    (F, "heave short", ok(kind="evolution.started")),
    (F, "weigh", ok(kind="evolution.started")),
    (F, "weigh anchor", ok(kind="evolution.started")),
    (F, "up anchor", ok(kind="evolution.started")),
    # -- verbs that make no sense for the part --------------------------------
    (F, "set the fore topsail yard", no(["You set sails", "is a yard", "fore topsail"])),
    (F, "set the main brace", no(["Which main brace"])),
    (F, "set the starboard main brace", no(["You set sails", "a brace"])),
    (
        F,
        "haul the fore topsail",
        no(["You haul lines", "fore topsail sheet", "fore topsail brace"]),
    ),
    (F, "haul the main shrouds, starboard", no(["standing rigging"])),
    (F, "brace the mizzen gaff sharp up", no(["gaff, not a yard"])),
    (F, "brace the spanker square", no(["gaff sail", "no yard to brace"])),
    (F, "furl the spanker", no(["gaff sail is not furled", "take it in"])),
    (F, "reef the fore royal", no(["no reef bands"])),
    (F, "shake out the reef in the fore topsail", no(["no reef in the fore topsail"])),
    (F, "take in the royals", no(["Nothing done", "already furled"])),
    (F, "clew up the main course", no(["already furled"])),
    (F, "set the fore topsail sharp up", no(["'sharp up' belongs with 'brace'"])),
    (F, "haul the main brace, weather, two reefs", no(["reefs belongs with"])),
    # -- unknown verbs, console commands, empty ------------------------------
    # ("splice the main brace" was the unknown verb here until package 31b made `splice`
    # an order on a parted line; the rum is still not served)
    (F, "splice the main brace", no(["Which main brace", "'splice' was understood"])),
    (F, "splice the mainbrace", no(["no such part"], UnknownNounError)),
    (F, "sett the fore topsail", no(["not an order", "did you mean 'set'"])),
    (F, "hold", no(["console command"])),
    (F, "time 10", no(["console command"])),
    (F, "", no(["No order given"])),
    (F, "set the fore topsail handsomely quickly", no(["'set' was understood, but not 'quickly'"])),
    # -- take in, furl, reef, shake out ---------------------------------------
    (F, "take in the fore topsail", no(["already furled"])),
    (F, "reef the topsails, one reef", ok(evo="reef_square", count=3, params={"reefs": 1})),
    (F, "reef the topsails", ok(evo="reef_square", count=3, params={"reefs": 1})),
    (F, "reef the fore topsail two reefs", ok(evo="reef_square", params={"reefs": 2})),
    (F, "reef the fore topsail, 2 reefs", ok(evo="reef_square", params={"reefs": 2})),
    (F, "reef the fore topsail, close", ok(evo="reef_square", params={"close": True})),
    (F, "close reef the fore topsail", ok(evo="reef_square", params={"close": True})),
    (F, "reef the fore topsail four reefs", no(["3 reef bands", "only 3 more"])),
    (F, "take a reef in the spanker", ok(evo="reef_gaff", subjects=["mizzen.spanker"])),
    (F, "reef the jib", no(["no reef bands"])),
    # -- bracing --------------------------------------------------------------
    (
        F,
        "brace the fore yards sharp up on the starboard tack",
        ok(evo="brace", count=4, params={"mode": "sharp up", "tack": "starboard"}),
    ),
    (
        F,
        "brace the fore yards sharp up on the larboard tack",
        ok(evo="brace", count=4, params={"tack": "larboard"}),
    ),
    (
        F,
        "brace the fore yards sharp up on the port tack",
        ok(evo="brace", params={"tack": "larboard"}),
    ),
    (F, "brace the yards square", ok(evo="brace", count=12, params={"target_deg": 0.0})),
    (F, "brace up", ok(evo="brace", count=12, params={"mode": "up"})),
    (F, "brace sharp up", ok(evo="brace", count=12, params={"mode": "sharp up"})),
    (
        F,
        "brace the main yard in",
        ok(evo="brace", subjects=["main.yard"], params={"target_deg": 15.0}),
    ),
    (
        F,
        "brace the main yard in on the larboard tack",
        ok(evo="brace", subjects=["main.yard"], params={"target_deg": 15.0, "tack": "larboard"}),
    ),
    (F, "brace the after yards up on the larboard tack", ok(evo="brace", count=8)),
    (F, "brace the head yards square", ok(evo="brace", count=4)),
    (
        F,
        "brace round the cro'jack yard square",
        ok(evo="brace", subjects=["mizzen.crossjack.yard"]),
    ),
    (F, "brace the crossjack yard square", ok(evo="brace", subjects=["mizzen.crossjack.yard"])),
    (F, "brace the fore topsail sharp up", ok(evo="brace", subjects=["fore.topsail.yard"])),
    (F, "brace the fore yards", no(["Brace them how"])),
    (F, "brace the fore yards on the weather tack", no(["not a tack"])),
    # -- level 0: lines -------------------------------------------------------
    (
        F,
        "haul the weather main brace",
        ok(kind="line.hauled", text=["starboard (weather) main brace"]),
    ),
    (F, "haul the lee main brace", ok(kind="line.hauled", text=["larboard (lee) main brace"])),
    (F, "haul the main brace, starboard", ok(kind="line.hauled", text=["starboard main brace"])),
    (F, "haul the main brace, port", ok(kind="line.hauled", text=["larboard main brace"])),
    (F, "haul the starboard main brace", ok(kind="line.hauled", text=["starboard main brace"])),
    (
        F,
        "haul the main yard brace starboard",
        ok(kind="line.hauled", text=["starboard main brace"]),
    ),
    (F, "haul the main brace", no(["Which main brace", "weather or the lee"])),
    (F, "haul the brace", no(["could be"], AmbiguousNounError)),
    (F, "ease the weather fore topsail brace", ok(kind="line.eased", text=["fore topsail yard"])),
    (F, "haul the starboard cro'jack brace", ok(kind="line.hauled", text=["crossjack"])),
    # package 32e: a haul or an ease is a fathom of the fall; the sail's angle follows by
    # the boom's geometry from its floor of 18 degrees (the spanker's sheet is flat aft)
    (F, "ease the spanker sheet", ok(kind="line.eased", text=["mizzen spanker now 24°"])),
    (F, "ease the spanker sheet a fathom", ok(kind="line.eased", text=["24° off the centreline"])),
    (
        F,
        "ease the spanker sheet two fathoms",
        ok(kind="line.eased", text=["29° off the centreline"]),
    ),
    (F, "ease the spanker sheet handsomely", ok(kind="line.eased", text=["handsomely"])),
    (F, "start the spanker sheet", ok(kind="line.eased")),
    (F, "haul the spanker sheet", no(["already hard in"])),
    (F, "haul the fore topsail halyard", no(["already hauled home"])),
    (F, "ease the fore topsail halyard", ok(kind="line.eased", text=["nine-tenths hauled"])),
    (F, "ease the fore topsail halyard a little", ok(kind="line.eased", text=["nine-tenths"])),
    (F, "check the fore topsail halyard", ok(kind="line.eased")),
    (F, "ease the jib sheet, lee", ok(kind="line.eased", text=["larboard (lee) jib sheet"])),
    (F, "haul the jib sheet", no(["already hard in"])),  # the lee sheet (package 32e)
    (F, "haul the jib sheet to windward", ok(kind="line.hauled", text=["to windward", "aback"])),
    (F, "let fly the jib sheet", ok(kind="line.let_go", text=["flogging"])),
    (F, "let go the fore topsail sheet, starboard", ok(kind="line.let_go", text=["ran free"])),
    (F, "let go the starboard fore topsail sheet", ok(kind="line.let_go")),
    (F, "cast off the fore course tack, weather", ok(kind="line.let_go")),
    (F, "belay the fore topsail halyard", ok(kind="line.belay", text=["Belayed"])),
    (F, "make fast the main topsail halyard", ok(kind="line.belay")),
    (F, "haul the spanker peak halyard", no(["already hauled home"])),
    (F, "ease the spanker peak halyard", ok(kind="line.eased", text=["mizzen gaff peak halyard"])),
    (F, "ease the mainsail sheet, lee", ok(kind="line.eased", text=["main course sheet"])),
    (F, "ease the main sheet", no(["Which main sheet", "weather or the lee"])),
    (F, "haul down the jib", no(["already furled"])),  # a take-in synonym
    # -- helm -----------------------------------------------------------------
    (F, "steer south-west by west", ok(kind="helm.order", text=["SW by W (236°)"])),
    (F, "steer sou'west by west", ok(kind="helm.order", text=["SW by W"])),
    (F, "steer SW by W", ok(kind="helm.order", text=["SW by W"])),
    (F, "steer 245", ok(kind="helm.order", text=["(245°)"])),
    (F, "steer 245 degrees", ok(kind="helm.order", text=["(245°)"])),
    (F, "steer 245°", ok(kind="helm.order", text=["(245°)"])),
    (F, "steer to the north", ok(kind="helm.order", text=["N (0°)"])),
    (F, "steer north-east by north", ok(kind="helm.order", text=["NE by N (34°)"])),
    (F, "steer two points to starboard", ok(kind="helm.order", text=["two points to starboard"])),
    (F, "steer 2 points to port", ok(kind="helm.order", text=["two points to larboard"])),
    (F, "steer two points", no(["which way"])),
    (F, "steer", no(["Steer where?"])),
    (F, "steer for the harbour", no(["'steer' was understood, but not"])),
    (F, "come up a point", ok(kind="helm.order", text=["come up a point"])),
    (F, "come up two points", ok(kind="helm.order", text=["come up two points"])),
    (F, "luff", ok(kind="helm.order", text=["come up a point"])),
    (F, "come up", ok(kind="helm.order")),
    (F, "bear away three points", ok(kind="helm.order", text=["bear away three points"])),
    (F, "keep away", ok(kind="helm.order", text=["bear away a point"])),
    (F, "bear up two points", ok(kind="helm.order", text=["bear away two points"])),
    (F, "keep her full", ok(kind="helm.order", text=["full and by"])),
    (F, "full and by", ok(kind="helm.order", text=["full and by"])),
    # -- ship evolutions ------------------------------------------------------
    (F, "tack ship", ok(evo="tack", subjects=["ship"])),
    (F, "ready about", ok(evo="tack", subjects=["ship"])),
    (F, "go about", ok(evo="tack", subjects=["ship"])),
    (F, "wear ship", ok(evo="wear", subjects=["ship"])),
    (F, "heave to", ok(evo="heave_to", subjects=["ship"], params={})),
    (F, "heave to on the larboard tack", ok(evo="heave_to", params={"tack": "larboard"})),
    (F, "heave to on the port tack", ok(evo="heave_to", params={"tack": "larboard"})),
    (F, "fill away", ok(evo="fill_away", subjects=["ship"])),
    (F, "fill", ok(evo="fill_away")),
    (F, "tack ship on the larboard tack", no(["takes no tack"])),
    (F, "shorten sail", ok(evo="reef_square", count=3, text=["Shorten sail", "Not done"])),
    # -- the schooner: a different vocabulary from the same rules --------------
    (S, "set the topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (S, "set the fore topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (S, "set the topsails", ok(evo="set_square", subjects=["fore.topsail"])),
    (S, "set the topgallant", ok(evo="set_square", subjects=["fore.topgallant"])),
    (S, "set the fore t'gallant", ok(evo="set_square", subjects=["fore.topgallant"])),
    (S, "set the foresail", ok(evo="set_gaff", subjects=["fore.sail"])),
    (S, "set the fore", ok(evo="set_gaff", subjects=["fore.sail"])),
    (S, "set the mainsail", ok(evo="set_gaff", subjects=["main.sail"])),
    (S, "set the main", ok(evo="set_gaff", subjects=["main.sail"])),
    (S, "set the gaff topsail", ok(evo="set_jibheaded", subjects=["main.gaff_topsail"])),
    (S, "set the main gaff topsail", ok(evo="set_jibheaded", subjects=["main.gaff_topsail"])),
    (S, "set the staysail", ok(evo="set_jibheaded", subjects=["fore.staysail"])),
    (S, "set the fore staysail", ok(evo="set_jibheaded", subjects=["fore.staysail"])),
    (S, "set the jib", ok(evo="set_jibheaded", subjects=["jib"])),
    (S, "set the flying jib", ok(evo="set_jibheaded", subjects=["flying_jib"])),
    (S, "set the headsails", ok(evo="set_jibheaded", count=3)),
    (S, "set the fore-and-aft sails", ok(count=6)),
    (S, "set the square sails", ok(evo="set_square", count=2)),
    (S, "set plain sail", ok(count=6)),
    (S, "make all sail", ok(count=10)),
    (S, "set the studdingsails, both sides", ok(evo="set_studding", count=2)),
    (
        S,
        "set the stuns'ls, starboard",
        ok(evo="set_studding", subjects=["fore.topmast.studdingsail.starboard"]),
    ),
    (S, "set the fore topmast studdingsail", no(["Which fore topmast studdingsail"])),
    (S, "set the royals", no(["no such part as the royals"], UnknownNounError)),
    (S, "set the spanker", no(["no such part as the spanker"], UnknownNounError)),
    (S, "set the main course", no(["no such part"], UnknownNounError)),
    (S, "furl the mainsail", no(["gaff sail is not furled"])),
    (
        S,
        "reef the mainsail, two reefs",
        ok(evo="reef_gaff", subjects=["main.sail"], params={"reefs": 2}),
    ),
    (S, "reef the foresail, three reefs", no(["2 reef bands"])),
    (S, "reef the topsail close", ok(evo="reef_square", params={"close": True})),
    (S, "brace the yards sharp up on the starboard tack", ok(evo="brace", count=2)),
    (S, "brace the fore yards square", ok(evo="brace", count=2, params={"target_deg": 0.0})),
    (S, "brace the topsail yard up", ok(evo="brace", subjects=["fore.topsail.yard"])),
    (S, "brace the main yard in", no(["no such part as the main yard"], UnknownNounError)),
    (S, "brace the main gaff sharp up", no(["gaff, not a yard"])),
    (S, "haul the weather main brace", no(["no such part as the main brace"], UnknownNounError)),
    (
        S,
        "haul the weather topsail brace",
        ok(kind="line.hauled", text=["starboard (weather) fore topsail brace"]),
    ),
    (S, "haul the lee fore topsail brace", ok(kind="line.hauled", text=["larboard (lee)"])),
    (S, "ease the main sheet", ok(kind="line.eased", text=["main sail now 20°"])),
    (S, "ease the main sheet a fathom", ok(kind="line.eased", text=["20° off"])),
    (S, "ease the mainsail sheet two fathoms", ok(kind="line.eased", text=["22° off"])),
    (S, "ease the fore sheet, lee", ok(kind="line.eased", text=["larboard (lee) fore sail sheet"])),
    (S, "haul the fore sheet, lee", no(["already hard in"])),
    (S, "haul the jib sheet", no(["already hard in"])),  # the lee sheet (package 32e)
    (S, "haul the jib sheet, weather", no(["already hard in"])),
    (
        S,
        "ease the jib sheet, weather",
        ok(kind="line.eased", text=["starboard (weather) jib sheet"]),
    ),
    (S, "let go the jib halyard", ok(kind="line.let_go", text=["Let go the jib halyard"])),
    (S, "ease the main peak halyard", ok(kind="line.eased", text=["main gaff peak halyard"])),
    (
        S,
        "ease the mainsail throat halyard",
        ok(kind="line.eased", text=["main gaff throat halyard"]),
    ),
    (S, "ease the main outhaul", ok(kind="line.eased", text=["main sail outhaul"])),
    (S, "haul the main vang, lee", no(["already hauled home"])),
    (S, "ease the main vang, lee", ok(kind="line.eased", text=["larboard (lee) main gaff vang"])),
    (S, "haul the bobstay", no(["standing rigging"])),
    (S, "steer west-north-west", ok(kind="helm.order", text=["WNW (292°)"])),
    (S, "steer nor'-nor'-east", ok(kind="helm.order", text=["NNE (22°)"])),
    (S, "come up two points", ok(kind="helm.order")),
    (S, "bear away", ok(kind="helm.order")),
    (S, "keep her full and by", ok(kind="helm.order", text=["full and by"])),
    (S, "tack ship", ok(evo="tack", subjects=["ship"])),
    (S, "wear ship", ok(evo="wear", subjects=["ship"])),
    (S, "heave to on the starboard tack", ok(evo="heave_to", params={"tack": "starboard"})),
    (S, "shorten sail", ok(evo="reef_square", count=1, text=["Shorten sail"])),
    (S, "set the cro'jack", no(["no such part"], UnknownNounError)),
    (S, "splice the mainbrace", no(["no such part"], UnknownNounError)),
    (S, "splice the fore topsail sheets", no(["sound and rove", "only a parted line is spliced"])),
    # -- package 15: the period forms the primer reached for ------------------
    # squaring, bracing round, to the wind, aback
    (
        F,
        "square the yards",
        ok(evo="brace", count=12, params={"target_deg": 0.0}, text=["Squared"]),
    ),
    (F, "square the after yards", ok(evo="brace", count=8, params={"mode": "square"})),
    (F, "square the yards sharp up", no(["says how already"])),
    (F, "lay the head yards square", ok(evo="brace", count=4, params={"target_deg": 0.0})),
    (
        F,
        "brace round the yards",
        ok(evo="brace", count=12, params={"mode": "sharp up", "tack": "starboard"}, text=["round"]),
    ),
    (F, "brace round the yards on the larboard tack", ok(evo="brace", params={"tack": "larboard"})),
    (F, "brace round the yards square", ok(evo="brace", params={"target_deg": 0.0})),
    (
        F,
        "brace the yards to the wind",
        ok(
            evo="brace",
            count=12,
            params={"mode": "to the wind"},
            text=["twelve yards to the wind"],
        ),
    ),
    (
        F,
        "brace the head yards to the wind",
        ok(evo="brace", count=4, text=["head yards to the wind"]),
    ),
    (
        F,
        "back the main topsail",
        ok(
            evo="brace",
            subjects=["main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"],
            params={"mode": "aback", "tack": "larboard"},
            text=["Laid the main yard, main topsail yard", "aback"],
        ),
    ),
    (
        F,
        "lay the main topsail aback",
        ok(
            evo="brace",
            subjects=["main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"],
        ),
    ),
    (F, "brace the main topsail yard aback", ok(evo="brace", params={"tack": "larboard"})),
    (F, "brace the head yards sharp aback", ok(evo="brace", count=4, params={"tack": "larboard"})),
    (F, "back", no(["Back what?"])),
    (F, "back the spanker", no(["gaff sail", "no yard"])),
    (S, "square the yards", ok(evo="brace", count=2, params={"target_deg": 0.0})),
    (
        S,
        "back the topsail",
        ok(evo="brace", subjects=["fore.topsail.yard", "fore.topgallant.yard"]),
    ),
    # the words for taking in, and the sails they suit
    (F, "haul up the mainsail", no(["already furled"])),
    (F, "haul up the courses", no(["already furled"])),
    (F, "haul up the spanker", no(["already furled"])),
    (F, "brail up the spanker", no(["already furled"])),
    (F, "clew up the topsails", no(["already furled"])),
    (F, "clew up the spanker", no(["brailed up, not clewed up", "brail up the mizzen spanker"])),
    (F, "haul up the topsails", no(["clewed up, not hauled up"])),
    (F, "haul down the spanker", no(["brailed up, not hauled down"])),
    (F, "lower the mainsail", no(["hauled up, not lowered"])),
    (S, "lower the mainsail", no(["already furled"])),
    (S, "haul up the mainsail", no(["already furled"])),
    (S, "brail up the foresail", no(["already furled"])),
    (S, "clew up the mainsail", no(["brailed up, not clewed up"])),
    (F, "scandalise the spanker", no(["cannot be scandalised", "no state"])),
    (S, "scandalise the mainsail", no(["cannot be scandalised"])),
    (S, "scandalize the main", no(["cannot be scandalised"])),
    (F, "scandalise the fore topsail", no(["no peak to drop"])),
    (S, "gybe", ok(evo="wear", subjects=["ship"], text=["Gybe", "wear ship"])),
    (S, "jibe", ok(evo="wear", subjects=["ship"])),
    (F, "gybe", ok(evo="wear", subjects=["ship"])),
    # sheets: aft, home, sheet home, plural families, the frigate's main sheet
    (F, "haul aft the spanker sheet", no(["already hard in"])),
    (F, "haul the jib sheet aft", no(["already hard in"])),
    (F, "haul the lee jib sheet aft", no(["already hard in"])),
    (F, "sheet home the fore topsail", no(["sheeted home already"])),
    (F, "haul home the topsail sheets", no(["Nothing done", "already hauled home"])),
    (F, "ease the fore topsail sheets home", no(["'home' and 'aft' belong with 'haul'"])),
    (
        F,
        "ease the fore topsail sheets, both sides",
        ok(kind="line.eased", text=["starboard fore topsail sheet", "larboard fore topsail sheet"]),
    ),
    (
        F,
        "ease the fore topsail sheets",
        ok(kind="line.eased", text=["starboard fore topsail sheet", "larboard fore topsail sheet"]),
    ),
    (F, "ease the topsail sheets", ok(kind="line.eased", text=["mizzen topsail sheet"])),
    (
        F,
        "ease the weather fore topsail sheets",
        ok(kind="line.eased", text=["starboard (weather) fore topsail sheet"]),
    ),
    (F, "let go the braces", ok(kind="line.let_go", text=["ran free"])),
    (F, "haul the fore topsail sheets, both sides", no(["already hauled home"])),
    (
        F,
        "ease the weather main sheet",
        ok(kind="line.eased", text=["starboard (weather) main course sheet", "nine-tenths"]),
    ),
    (
        F,
        "ease the main sheets",
        ok(kind="line.eased", text=["starboard main course sheet", "larboard main course sheet"]),
    ),
    (F, "haul the fore tack", no(["Which fore tack"])),
    (F, "ease the lee fore tack", ok(kind="line.eased", text=["larboard (lee) fore course tack"])),
    (F, "ease the main bowline, weather", ok(kind="line.eased", text=["main course bowline"])),
    (
        F,
        "ease the fore sheet, lee",
        ok(kind="line.eased", text=["larboard (lee) fore course sheet"]),
    ),
    # the conning words
    (F, "steady", ok(kind="helm.order", text=["steady"], data={"helm_mode": "heading"})),
    (F, "steady as she goes", ok(kind="helm.order", text=["steady as she goes", "steady on"])),
    (F, "very well thus", ok(kind="helm.order", text=["steady on"])),
    (F, "nothing off", ok(kind="helm.order", text=["nothing off", "full and by"])),
    (
        F,
        "no higher",
        ok(kind="helm.order", text=["full and by"], data={"helm_mode": "full_and_by"}),
    ),
    (F, "meet her", ok(kind="helm.order", text=["meet her", "steady on"])),
    (
        F,
        "right the helm",
        ok(kind="helm.order", text=["rudder amidships"], data={"helm_mode": "rudder"}),
    ),
    (F, "helm amidships", ok(kind="helm.order", text=["amidships"])),
    (
        F,
        "hard a-lee",
        ok(
            kind="helm.order",
            text=["hard a-lee", "to windward", "starboard"],
            data={"helm_mode": "rudder"},
        ),
    ),
    (F, "helm's a-lee", ok(kind="helm.order", text=["helm's a-lee", "coming up to the wind"])),
    (F, "hard up", ok(kind="helm.order", text=["hard up", "to leeward", "larboard", "paying off"])),
    (F, "helm a-weather", ok(kind="helm.order", text=["helm a-weather"])),
    (F, "up helm", ok(kind="helm.order", text=["paying off"])),
    (F, "down helm", ok(kind="helm.order", text=["coming up to the wind"])),
    (F, "bring her by the wind", ok(kind="helm.order", text=["full and by"])),
    (F, "steer by the wind", ok(kind="helm.order", text=["full and by"])),
    (F, "luff and touch her", ok(kind="helm.order", text=["luff and touch her", "full and by"])),
    (F, "come up half a point", ok(kind="helm.order", text=["come up half a point"])),
    (F, "bear away a point and a half", ok(kind="helm.order", text=["a point and a half"])),
    (
        F,
        "steer two and a half points to starboard",
        ok(kind="helm.order", text=["two and a half points to starboard"]),
    ),
    (F, "steady two points", no(["takes no heading or points"])),
    # compound objects
    (F, "set the topsails and topgallants", ok(evo="set_square", count=6)),
    (F, "set the jib and the spanker", ok(count=2, subjects=["jib", "mizzen.spanker"])),
    (
        F,
        "brace the fore and main yards square",
        ok(evo="brace", count=8, params={"target_deg": 0.0}),
    ),
    (
        F,
        "set the fore and main topsails",
        ok(evo="set_square", subjects=["fore.topsail", "main.topsail"]),
    ),
    (
        F,
        "haul the weather fore and main braces",
        ok(
            kind="line.hauled",
            text=["starboard (weather) fore brace", "starboard (weather) main brace"],
        ),
    ),
    (S, "set the jib and the spanker", no(["no such part as the spanker"], UnknownNounError)),
    (S, "set the fore and main sails", ok(evo="set_gaff", subjects=["fore.sail", "main.sail"])),
    # reefs by the verb
    (F, "close reef the topsails", ok(evo="reef_square", count=3, params={"close": True})),
    (F, "double reef the topsails", ok(evo="reef_square", count=3, params={"reefs": 2})),
    (F, "single reef the fore topsail", ok(evo="reef_square", params={"reefs": 1})),
    (F, "treble reef the fore topsail", ok(evo="reef_square", params={"reefs": 3})),
    (F, "double reef the fore topsail, one reef", no(["says how already"])),
    (F, "take in one reef in the topsails", ok(evo="reef_square", count=3, params={"reefs": 1})),
    (F, "take in two reefs in the fore topsail", ok(evo="reef_square", params={"reefs": 2})),
    (F, "shake out the reefs in the topsails", no(["no reef in the fore topsail"])),
    (F, "furl the topsails two reefs", no(["reefs belongs with"])),
    # -- package 32b: the cutter Sherbourne, a one-master with a running bowsprit --------
    (C, "set the mainsail", ok(evo="set_gaff", subjects=["main.sail"])),
    (C, "set the main", ok(evo="set_gaff", subjects=["main.sail"])),
    (C, "set the foresail", ok(evo="set_jibheaded", subjects=["fore.staysail"])),
    (C, "set the fore", ok(evo="set_jibheaded", subjects=["fore.staysail"])),
    (C, "set the staysail", ok(evo="set_jibheaded", subjects=["fore.staysail"])),
    (C, "set the jib", ok(evo="set_jibheaded", subjects=["jib"])),
    (C, "set the square sail", ok(evo="set_square", subjects=["square_sail"])),
    (C, "set the crossjack", ok(evo="set_square", subjects=["square_sail"])),
    (C, "set the topsail", ok(evo="set_square", subjects=["topsail"])),
    (C, "set the topsails", ok(evo="set_square", subjects=["topsail"])),
    (C, "set the main topsail", ok(evo="set_square", subjects=["topsail"])),
    (C, "set the topgallant", ok(evo="set_square", subjects=["topgallant"])),
    (C, "set the gaff topsail", ok(evo="set_jibheaded", subjects=["main.gaff_topsail"])),
    (C, "set the head sails", ok(evo="set_jibheaded", subjects=["fore.staysail", "jib"])),
    (C, "set the square sails", ok(evo="set_square", count=3)),
    (C, "set the fore-and-aft sails", ok(count=4)),
    (C, "set plain sail", ok(count=4, text=["main sail, fore staysail, jib and topsail"])),
    (C, "make all sail", ok(count=7)),
    (C, "set the jib and the mainsail", ok(count=2, subjects=["jib", "main.sail"])),
    (C, "set the studdingsails", no(["no such part as the studdingsails"], UnknownNounError)),
    (C, "set the stuns'ls, both sides", no(["no such part as the stuns'ls"], UnknownNounError)),
    (C, "set the flying jib", no(["no such part as the flying jib"], UnknownNounError)),
    (C, "set the royals", no(["no such part as the royals"], UnknownNounError)),
    (C, "set the spanker", no(["no such part as the spanker"], UnknownNounError)),
    (C, "set the mizzen", no(["no such part as the mizzen"], UnknownNounError)),
    (C, "set the fore topsail", no(["no such part as the fore topsail"], UnknownNounError)),
    (C, "set the fore course", no(["no such part as the fore course"], UnknownNounError)),
    (C, "set the storm jib", no(["storm jib is unbent", "Bend one first"])),
    (C, "furl the mainsail", no(["gaff sail is not furled"])),
    (C, "reef the mainsail, two reefs", ok(evo="reef_gaff", params={"reefs": 2})),
    (C, "reef the mainsail, four reefs", ok(evo="reef_gaff", params={"reefs": 4})),
    (C, "reef the mainsail, five reefs", no(["4 reef bands"])),
    (C, "reef the foresail", no(["no reef bands"])),
    (C, "reef the topsail close", ok(evo="reef_square", params={"close": True})),
    (C, "reef the topsail, two reefs", no(["1 reef band"])),
    # the running bowsprit: reefed, run in, rigged out (the runner's own refusals are in
    # test_catalogue, where the real runner checks a jib set on it or a standing bowsprit)
    (C, "reef the bowsprit", ok(evo="reef_bowsprit", subjects=["bowsprit"])),
    (C, "run in the bowsprit", ok(evo="reef_bowsprit", subjects=["bowsprit"])),
    (C, "rig in the bowsprit", ok(evo="reef_bowsprit", subjects=["bowsprit"])),
    (C, "rig out the bowsprit", ok(evo="rig_out_bowsprit", subjects=["bowsprit"])),
    (C, "run out the bowsprit", ok(evo="rig_out_bowsprit", subjects=["bowsprit"])),
    (C, "reef the mast", no(["You reef sails; the main mast is a mast"])),
    (C, "ease the heel rope", ok(kind="line.eased", text=["bowsprit heel rope"])),
    (C, "haul the heel rope", no(["already hauled home"])),
    (C, "brace the yards sharp up on the starboard tack", ok(evo="brace", count=3)),
    (C, "square the yards", ok(evo="brace", count=3, params={"target_deg": 0.0})),
    (C, "brace the topsail yard up", ok(evo="brace", subjects=["topsail.yard"])),
    (C, "brace the crossjack yard square", ok(evo="brace", subjects=["square_sail.yard"])),
    (C, "brace the main yard in", no(["no such part as the main yard"], UnknownNounError)),
    (C, "brace the head yards square", no(["no such part as the head yards"], UnknownNounError)),
    (C, "brace the gaff sharp up", no(["gaff, not a yard"])),
    (C, "back the topsail", ok(evo="brace", count=3, params={"mode": "aback"})),
    (C, "back the mainsail", no(["gaff sail", "no yard"])),
    (C, "brace the yards to the wind", ok(evo="brace", count=3, text=["three yards to the wind"])),
    (C, "haul the weather topsail brace", ok(kind="line.hauled", text=["(weather) topsail brace"])),
    (C, "haul the weather main brace", no(["no such part as the main brace"], UnknownNounError)),
    (C, "ease the main sheet", ok(kind="line.eased", text=["main sail now 21°"])),
    (
        C,
        "ease the fore sheet, lee",
        ok(kind="line.eased", text=["larboard (lee) fore staysail sheet"]),
    ),
    (C, "haul the jib sheet", no(["already hard in"])),  # the lee sheet (package 32e)
    (C, "ease the jib sheet, weather", ok(kind="line.eased", text=["(weather) jib sheet"])),
    (C, "ease the main peak halyard", ok(kind="line.eased", text=["main gaff peak halyard"])),
    (C, "ease the throat halyard", ok(kind="line.eased", text=["main gaff throat halyard"])),
    (C, "ease the main vang, lee", ok(kind="line.eased", text=["larboard (lee) main gaff vang"])),
    (C, "haul the bobstay", no(["standing rigging"])),
    (C, "haul up the mainsail", no(["already furled"])),
    (C, "haul down the foresail", no(["fore staysail is already furled"])),
    (C, "scandalise the mainsail", no(["cannot be scandalised"])),
    (C, "tack ship", ok(evo="tack", subjects=["ship"])),
    (C, "wear ship", ok(evo="wear", subjects=["ship"])),
    (C, "gybe", ok(evo="wear", subjects=["ship"], text=["Gybe"])),
    (C, "heave to on the starboard tack", ok(evo="heave_to", params={"tack": "starboard"})),
    (C, "shorten sail", ok(evo="reef_square", count=1, text=["Shorten sail"])),
    (C, "send down the topgallant mast", ok(evo="send_down_topgallant_masts", subjects=["ship"])),
    (C, "strike the topmast", ok(evo="strike_topmasts", subjects=["ship"])),
    (C, "steer west-north-west", ok(kind="helm.order", text=["WNW (292°)"])),
    (C, "keep her full and by", ok(kind="helm.order", text=["full and by"])),
    (C, "splice the mainbrace", no(["no such part"], UnknownNounError)),
    # -- package 32b: the brig Harpy, the frigate less a mast --------------------------
    (B, "set the fore topsail", ok(evo="set_square", subjects=["fore.topsail"])),
    (B, "set the topsails", ok(evo="set_square", subjects=["fore.topsail", "main.topsail"])),
    (B, "set the royals", ok(evo="set_square", subjects={"fore.royal", "main.royal"})),
    (B, "set the courses", ok(evo="set_square", count=2)),
    (B, "set the mainsail", ok(evo="set_square", subjects=["main.course"])),
    (B, "set the spanker", ok(evo="set_gaff", subjects=["main.spanker"])),
    (B, "set the driver", ok(evo="set_gaff", subjects=["main.spanker"])),
    (B, "set the boom mainsail", ok(evo="set_gaff", subjects=["main.spanker"])),
    (B, "set the jib", ok(evo="set_jibheaded", subjects=["jib"])),
    (B, "set the flying jib", ok(evo="set_jibheaded", subjects=["flying_jib"])),
    (B, "set the middle staysail", ok(evo="set_jibheaded", subjects=["main.topmast_staysail"])),
    (B, "set the headsails", ok(evo="set_jibheaded", count=3)),
    (B, "set the staysails", ok(evo="set_jibheaded", count=4)),
    (B, "set the square sails", ok(evo="set_square", count=8)),
    (B, "set plain sail", ok(count=9)),
    (B, "make all sail", ok(count=25)),
    (B, "set the studdingsails, both sides", ok(evo="set_studding", count=10)),
    (B, "set the stuns'ls, starboard", ok(evo="set_studding", count=5)),
    (B, "set the main topmast studdingsail", no(["Which main topmast studdingsail"])),
    (B, "set the jib and the spanker", ok(count=2, subjects=["jib", "main.spanker"])),
    (B, "set the fore and main topsails", ok(evo="set_square", count=2)),
    (B, "set the topsails and topgallants", ok(evo="set_square", count=4)),
    (B, "set the mizzen", no(["no such part as the mizzen"], UnknownNounError)),
    (B, "set the mizzen topsail", no(["no such part as the mizzen topsail"], UnknownNounError)),
    (B, "set the crossjack", no(["no such part as the crossjack"], UnknownNounError)),
    (B, "set the gaff topsail", no(["no such part as the gaff topsail"], UnknownNounError)),
    (B, "set the square sail", no(["no such part as the square sail"], UnknownNounError)),
    (B, "set the storm trysail", no(["storm trysail is unbent"])),
    (B, "furl the spanker", no(["gaff sail is not furled"])),
    (B, "haul up the mainsail", no(["main course is already furled"])),
    (B, "lower the mainsail", no(["hauled up, not lowered"])),
    (B, "haul down the spanker", no(["brailed up, not hauled down"])),
    (B, "clew up the spanker", no(["brailed up, not clewed up", "brail up the main spanker"])),
    (B, "close reef the topsails", ok(evo="reef_square", count=2, params={"close": True})),
    (B, "reef the spanker, two reefs", ok(evo="reef_gaff", params={"reefs": 2})),
    (B, "reef the spanker, four reefs", no(["3 reef bands"])),
    (B, "brace the yards sharp up on the starboard tack", ok(evo="brace", count=8)),
    (B, "square the yards", ok(evo="brace", count=8, params={"target_deg": 0.0})),
    (B, "square the after yards", ok(evo="brace", count=4, params={"mode": "square"})),
    (B, "brace the head yards square", ok(evo="brace", count=4)),
    (B, "brace the fore and main yards square", ok(evo="brace", count=8)),
    (
        B,
        "brace the mizzen yards square",
        no(["no such part as the mizzen yards"], UnknownNounError),
    ),
    (
        B,
        "brace the cro'jack yard square",
        no(["no such part as the cro'jack yard"], UnknownNounError),
    ),
    (
        B,
        "back the main topsail",
        ok(
            evo="brace",
            subjects=["main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"],
            params={"mode": "aback", "tack": "larboard"},
        ),
    ),
    (B, "brace the yards to the wind", ok(evo="brace", count=8, text=["eight yards to the wind"])),
    (B, "haul the weather main brace", ok(kind="line.hauled", text=["(weather) main brace"])),
    (
        B,
        "haul the weather mizzen brace",
        no(["no such part as the mizzen brace"], UnknownNounError),
    ),
    (
        B,
        "ease the main sheets",
        ok(kind="line.eased", text=["starboard main course sheet", "larboard main course sheet"]),
    ),
    (B, "ease the lee fore tack", ok(kind="line.eased", text=["larboard (lee) fore course tack"])),
    (B, "haul aft the spanker sheet", no(["already hard in"])),
    (B, "ease the spanker outhaul", ok(kind="line.eased", text=["main spanker outhaul"])),
    (
        B,
        "ease the main vang, lee",
        no(["no such part as the main vang", "spanker vang"], UnknownNounError),
    ),
    (B, "haul the martingale", no(["standing rigging"])),
    (B, "reef the bowsprit", ok(evo="reef_bowsprit", subjects=["bowsprit"])),  # the runner refuses
    (B, "tack ship", ok(evo="tack", subjects=["ship"])),
    (B, "wear ship", ok(evo="wear", subjects=["ship"])),
    (B, "box haul", ok(evo="boxhaul", subjects=["ship"])),
    (B, "heave to on the starboard tack", ok(evo="heave_to", params={"tack": "starboard"})),
    (B, "shorten sail", ok(evo="reef_square", count=2, text=["Shorten sail"])),
    (B, "send down the topgallant masts", ok(evo="send_down_topgallant_masts", subjects=["ship"])),
    (B, "send down the royal yards", no(["light yards go down together"])),
    (
        B,
        "rig out the fore topmast studdingsail boom, starboard",
        ok(evo="rig_out_studdingsail_boom", subjects=["fore.topmast.studdingsail_boom.starboard"]),
    ),
    (B, "steer west-north-west", ok(kind="helm.order", text=["WNW (292°)"])),
    (B, "splice the mainbrace", no(["no such part"], UnknownNounError)),
]


@pytest.mark.parametrize("which,text,expect", TABLE, ids=[f"{w}: {t}" for w, t, _ in TABLE])
def test_table(which: str, text: str, expect: ok | no):
    ship, runner = make(which)
    if isinstance(expect, no):
        with pytest.raises(expect.kind) as info:
            orders.handle(ship, text)
        message = str(info.value)
        for m in expect.mentions:
            assert m in message, f"{text!r}: expected {m!r} in {message!r}"
        assert runner.started == [], "a refused order must start nothing"
        return
    kind, log, data = orders.handle(ship, text)
    assert kind == expect.kind, f"{text!r}: kind {kind!r}, log {log!r}"
    assert log and log[0].isupper() and log.endswith("."), log
    if expect.evo is not None:
        assert runner.started, f"{text!r} started nothing: {log}"
        assert all(e == expect.evo for e, _, _ in runner.started), runner.started
    if expect.subjects is not None:
        subjects = [s for _, s, _ in runner.started]
        if isinstance(expect.subjects, set):
            assert set(subjects) == expect.subjects and len(subjects) == len(expect.subjects)
        else:
            assert subjects == expect.subjects
    if expect.count is not None:
        assert len(runner.started) == expect.count, runner.started
    if expect.params is not None:
        for _, _, p in runner.started:
            for k, v in expect.params.items():
                assert p.get(k) == v, f"{text!r}: params {p}"
    for m in expect.text:
        assert m in log, f"{text!r}: expected {m!r} in {log!r}"
    if expect.data is not None:
        for k, v in expect.data.items():
            assert data.get(k) == v, f"{text!r}: data {data}"


def test_table_is_large_enough():
    assert len(TABLE) >= 100
    assert sum(1 for w, _, _ in TABLE if w == S) >= 30
    assert sum(1 for w, _, _ in TABLE if w == C) >= 30  # package 32b
    assert sum(1 for w, _, _ in TABLE if w == B) >= 30


# ---------------------------------------------------------------------------
# Sides: weather and lee resolve from the tack at parse time
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tack,word,side",
    [
        ("starboard", "weather", "starboard"),
        ("starboard", "lee", "larboard"),
        ("larboard", "weather", "larboard"),
        ("larboard", "lee", "starboard"),
        ("larboard", "port", "larboard"),
        ("larboard", "starboard", "starboard"),
    ],
)
def test_weather_and_lee_resolve_from_the_tack(tack, word, side):
    ship, _ = make("frigate", tack=tack)
    kind, log, data = orders.handle(ship, f"haul the {word} main brace")
    assert data["subjects"] == [f"main.yard.brace.{side}"]
    assert data["side"] == side
    assert f"{side} " in log
    if word in ("weather", "lee"):
        assert f"({word})" in log
    assert "port" not in log  # port is echoed as larboard


def test_port_is_echoed_as_larboard_in_the_log():
    ship, _ = make("frigate")
    _, log, data = orders.handle(ship, "let go the fore topsail sheet, port")
    assert "larboard fore topsail sheet" in log
    assert data["side"] == "larboard"


# ---------------------------------------------------------------------------
# Level 0 effects on parts
# ---------------------------------------------------------------------------


def test_hauling_the_larboard_brace_braces_up_for_the_starboard_tack():
    """brace_angle > 0 = braced up for the starboard tack, starboard yardarm forward."""
    ship, _ = make("frigate")
    yard = ship.spars["main.yard"]
    assert yard.brace_angle == 0.0
    orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(5))
    orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(10))
    orders.handle(ship, "haul the starboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(5))
    orders.handle(ship, "ease the larboard main brace")
    assert yard.brace_angle == pytest.approx(0.0)
    orders.handle(ship, "ease the larboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(-5))
    assert ship.lines["main.yard.brace.larboard"].state is LineState.BELAYED


def test_a_brace_stops_at_the_yards_limit():
    ship, _ = make("frigate")
    yard = ship.spars["main.yard"]
    limit_deg = round(math.degrees(yard.brace_limit))
    steps_short = limit_deg // 5 - (1 if limit_deg % 5 == 0 else 0)
    for _ in range(steps_short):
        orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(5 * steps_short))
    _, log, _ = orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(yard.brace_limit)
    assert f"{limit_deg}°" in log and "starboard tack" in log
    with pytest.raises(OrderError, match="will come no further"):
        orders.handle(ship, "haul the larboard main brace")
    assert yard.brace_angle == pytest.approx(yard.brace_limit)


def test_hauling_by_fathoms_takes_several_steps():
    ship, _ = make("frigate")
    yard = ship.spars["fore.yard"]
    orders.handle(ship, "haul the lee fore brace two fathoms")
    assert yard.brace_angle == pytest.approx(units.deg_to_rad(10))


def test_sheet_of_a_fore_and_aft_sail_changes_its_angle():
    """Package 32e: the sheet holds the trim. A haul or an ease is a fathom of the fall
    (a threefold purchase on the schooner's main boom), and the sail's angle is read from
    the sheet's length through the boom's geometry, from its floor (flat aft)."""
    from freesail.evolutions import trim

    ship, _ = make("schooner")
    sail = ship.sails["main.sail"]
    geo = trim.sheet_geometry(ship, sail)
    assert ship.lines["main.sail.sheet"].hauled == 1.0  # flat aft: the floor
    with pytest.raises(OrderError, match="already hard in"):
        orders.handle(ship, "haul the main sheet")
    orders.handle(ship, "ease the main sheet")
    after_one = sail.sheet_angle
    assert after_one > geo.floor
    assert ship.lines["main.sail.sheet"].hauled == pytest.approx(1.0 - trim.FATHOM_M / geo.scope_m)
    orders.handle(ship, "ease the main sheet three fathoms")
    assert sail.sheet_angle > after_one
    assert sail.sheet_angle == pytest.approx(
        geo.angle_from_hauled(1.0 - 4 * trim.FATHOM_M / geo.scope_m)
    )
    _, log, _ = orders.handle(ship, "haul the main sheet")
    assert sail.sheet_angle == pytest.approx(
        geo.angle_from_hauled(1.0 - 3 * trim.FATHOM_M / geo.scope_m)
    )
    assert "off the centreline" in log


def test_sheet_of_a_square_sail_and_a_halyard_move_the_hoist():
    ship, _ = make("frigate")
    halyard = ship.lines["fore.topsail.yard.halyard"]
    sheet = ship.lines["fore.topsail.sheet.starboard"]
    assert halyard.hauled == 1.0
    orders.handle(ship, "ease the fore topsail halyard")
    assert halyard.hauled == pytest.approx(0.9)
    orders.handle(ship, "ease the fore topsail halyard a fathom")
    assert halyard.hauled == pytest.approx(0.8)
    _, log, _ = orders.handle(ship, "haul the fore topsail halyard")
    assert halyard.hauled == pytest.approx(0.9)
    assert "nine-tenths" in log
    orders.handle(ship, "ease the starboard fore topsail sheet")
    assert sheet.hauled == pytest.approx(0.9)


def test_let_go_and_belay_change_line_state():
    ship, _ = make("frigate")
    line = ship.lines["fore.topsail.sheet.starboard"]
    assert line.state is LineState.BELAYED
    kind, log, data = orders.handle(ship, "let go the fore topsail sheet, starboard")
    assert kind == "line.let_go" and line.state is LineState.FREE
    assert data["changes"] == [{"line": line.id, "state": "free"}]
    with pytest.raises(OrderError, match="already running free"):
        orders.handle(ship, "let go the starboard fore topsail sheet")
    kind, log, _ = orders.handle(ship, "belay the starboard fore topsail sheet")
    assert kind == "line.belay" and line.state is LineState.BELAYED
    # hauling a free line belays it
    orders.handle(ship, "let go the starboard fore topsail sheet")
    orders.handle(ship, "haul the starboard fore topsail sheet")
    assert line.state is LineState.BELAYED


def test_a_parted_line_cannot_be_worked():
    ship, _ = make("frigate")
    ship.lines["fore.topsail.yard.halyard"].state = LineState.PARTED
    with pytest.raises(OrderError, match="parted"):
        orders.handle(ship, "haul the fore topsail halyard")


# ---------------------------------------------------------------------------
# Helm
# ---------------------------------------------------------------------------


def test_steer_sets_the_helm_targets():
    ship, _ = make("frigate")
    ship.dyn.steady = True
    kind, log, data = orders.handle(ship, "steer south-west by west")
    assert kind == "helm.order"
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(236.25))
    assert ship.dyn.steady is False
    assert data["target_heading"] == pytest.approx(units.deg_to_rad(236.25))


def test_steer_degrees_wraps():
    ship, _ = make("frigate")
    orders.handle(ship, "steer 370")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(10))


def test_come_up_and_bear_away_turn_toward_and_away_from_the_wind():
    # starboard tack: the wind is on the starboard side, so coming up turns to starboard
    ship, _ = make("frigate", tack="starboard")
    ship.dyn.heading = units.deg_to_rad(90)
    ship.dyn.target_heading = ship.dyn.heading
    orders.handle(ship, "come up two points")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 + 22.5))
    orders.handle(ship, "bear away a point")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 + 11.25))
    # larboard tack: the reverse
    ship, _ = make("frigate", tack="larboard")
    ship.dyn.heading = units.deg_to_rad(90)
    ship.dyn.target_heading = ship.dyn.heading
    orders.handle(ship, "luff")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 - 11.25))
    orders.handle(ship, "bear away two points")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 + 11.25))


def test_relative_orders_build_on_the_current_target_when_steering_a_heading():
    ship, _ = make("frigate")
    ship.dyn.heading = units.deg_to_rad(0)
    orders.handle(ship, "steer 90")
    orders.handle(ship, "steer two points to starboard")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(112.5))
    orders.handle(ship, "steer a point to larboard")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(101.25))


def test_full_and_by_sets_the_mode_and_a_later_course_order_clears_it():
    ship, _ = make("frigate")
    orders.handle(ship, "keep her full")
    assert ship.dyn.helm_mode is HelmMode.FULL_AND_BY
    assert ship.dyn.steady is False
    ship.dyn.heading = units.deg_to_rad(45)
    orders.handle(ship, "bear away a point")  # from the heading, since no heading was ordered
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(45 - 11.25))


# ---------------------------------------------------------------------------
# Level 1 through the runner
# ---------------------------------------------------------------------------


def test_group_order_starts_one_evolution_per_member():
    ship, runner = make("frigate")
    _, log, data = orders.handle(ship, "set the topsails")
    assert [s for _, s, _ in runner.started] == ["fore.topsail", "main.topsail", "mizzen.topsail"]
    assert data["subjects"] == ["fore.topsail", "main.topsail", "mizzen.topsail"]
    assert data["evolutions"][0] == {
        "evolution": "set_square",
        "subject": "fore.topsail",
        "params": {},
    }


def test_group_order_reports_failures_and_starts_the_rest():
    ship, runner = make("frigate", refuse={"main.topsail": "the main topsail yard is on the cap"})
    kind, log, data = orders.handle(ship, "set the topsails")
    assert kind == "evolution.started"
    assert [s for _, s, _ in runner.started] == ["fore.topsail", "mizzen.topsail"]
    assert "Not done" in log and "main topsail yard is on the cap" in log
    assert data["failed"] == ["the main topsail: the main topsail yard is on the cap"]


def test_group_order_where_every_member_fails_is_rejected():
    ship, runner = make("frigate")
    for sid in ("fore.royal", "main.royal", "mizzen.royal"):
        ship.sails[sid].state = SailState.SET
    with pytest.raises(OrderError, match="Nothing done: the fore royal is already set"):
        orders.handle(ship, "set the royals")
    assert runner.started == []


def test_sail_already_set_is_refused_before_the_runner():
    ship, runner = make("frigate")
    ship.sails["fore.topsail"].state = SailState.SET
    with pytest.raises(OrderError, match="The fore topsail is already set."):
        orders.handle(ship, "set the fore topsail")
    assert runner.started == []
    _, log, _ = orders.handle(ship, "take in the fore topsail")
    assert runner.started == [("take_in_square", "fore.topsail", {})]


def test_reef_counts_respect_the_bands_and_the_reefs_already_in():
    ship, runner = make("frigate")
    sail = ship.sails["fore.topsail"]  # 3 bands
    sail.state = SailState.SET
    sail.reefs = 2
    with pytest.raises(OrderError, match="only 1 more"):
        orders.handle(ship, "reef the fore topsail, two reefs")
    orders.handle(ship, "reef the fore topsail")
    assert runner.started[-1] == ("reef_square", "fore.topsail", {"reefs": 1})
    orders.handle(ship, "shake out two reefs in the fore topsail")
    assert runner.started[-1] == ("shake_out_square", "fore.topsail", {"reefs": 2})
    with pytest.raises(OrderError, match="only 2 reefs in"):
        orders.handle(ship, "shake out three reefs in the fore topsail")
    orders.handle(ship, "shake out all reefs in the fore topsail")
    assert runner.started[-1][2] == {"reefs": 2, "close": True}
    sail.reefs = 3
    with pytest.raises(OrderError, match="already close reefed"):
        orders.handle(ship, "reef the fore topsail")


def test_brace_targets_are_signed_by_the_tack_and_limited_by_the_yard():
    ship, runner = make("frigate")
    orders.handle(ship, "brace the fore yards sharp up on the starboard tack")
    by_yard = {s: p for _, s, p in runner.started}
    fore_limit = round(math.degrees(ship.spars["fore.yard"].brace_limit), 2)
    topsail_limit = round(math.degrees(ship.spars["fore.topsail.yard"].brace_limit), 2)
    assert by_yard["fore.yard"]["target_deg"] == fore_limit
    assert by_yard["fore.topsail.yard"]["target_deg"] == topsail_limit
    assert topsail_limit > fore_limit  # upper yards brace sharper
    assert by_yard["fore.yard"]["target_angle"] == pytest.approx(
        ship.spars["fore.yard"].brace_limit
    )
    runner.started.clear()
    # brace.yaml reads target_deg unsigned and takes the sign from the tack;
    # target_angle carries the signed value for anything that wants it
    orders.handle(ship, "brace the fore yards sharp up on the larboard tack")
    assert all(p["target_deg"] > 0 and p["tack"] == "larboard" for _, _, p in runner.started)
    assert all(p["target_angle"] < 0 for _, _, p in runner.started)
    runner.started.clear()
    orders.handle(ship, "brace the fore yards up on the larboard tack")
    assert all(p["target_deg"] == 30.0 and p["tack"] == "larboard" for _, _, p in runner.started)
    assert all(
        p["target_angle"] == pytest.approx(-units.deg_to_rad(30)) for _, _, p in runner.started
    )
    runner.started.clear()
    # no tack given: the current one (starboard here)
    orders.handle(ship, "brace the main yard in")
    assert runner.started == [
        (
            "brace",
            "main.yard",
            {
                "target_deg": 15.0,
                "target_angle": pytest.approx(units.deg_to_rad(15)),
                "mode": "in",
                "tack": "starboard",
            },
        )
    ]


def test_brace_skips_a_wrecked_or_sent_down_yard():
    ship, runner = make("frigate")
    ship.spars["fore.royal.yard"].sent_down = True
    ship.spars["fore.topgallant.yard"].wrecked = True
    _, log, data = orders.handle(ship, "brace the fore yards square")
    assert [s for _, s, _ in runner.started] == ["fore.yard", "fore.topsail.yard"]
    assert "fore royal yard is sent down" in log and "carried away" in log


def test_back_braces_the_whole_mast_for_the_other_tack():
    """Aback is sharp up for the other tack, as heave to does (scripts.py), and a
    yard is laid aback with the rest of its mast's yards: braced against the
    yards above and below, its sail would foul theirs."""
    ship, runner = make("frigate", tack="starboard")
    ship.sails["main.topsail"].state = SailState.SET
    _, log, data = orders.handle(ship, "back the main topsail")
    yard = ship.spars["main.topsail.yard"]
    main_yards = {"main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"}
    assert {s for _, s, _ in runner.started} == main_yards
    for _, sid, params in runner.started:
        assert params["mode"] == "aback" and params["tack"] == "larboard"
        assert params["target_angle"] == pytest.approx(-ship.spars[sid].brace_limit)
    topsail = next(p for _, sid, p in runner.started if sid == "main.topsail.yard")
    assert topsail["target_deg"] == round(math.degrees(yard.brace_limit), 2)
    assert "the main topsail to the mast" in log and data["tack"] == "larboard"
    notes = ship.drain_notes()
    assert notes[-1][1] == "yard.laid_aback"
    assert notes[-1][2].startswith("Laid the main yard, main topsail yard")
    assert notes[-1][2].endswith("braced up for the larboard tack; the main topsail to the mast.")
    ship, runner = make("frigate", tack="larboard")
    orders.handle(ship, "lay the main topsail aback")
    assert all(p["target_angle"] > 0 for _, _, p in runner.started)
    # a tack said is the tack laid aback from
    ship, runner = make("frigate", tack="larboard")
    orders.handle(ship, "brace the head yards aback on the larboard tack")
    assert all(p["tack"] == "starboard" and p["target_angle"] > 0 for _, _, p in runner.started)


def test_brace_to_the_wind_trims_only_the_yards_named():
    ship, runner = make("frigate", tack="starboard")
    kind, log, data = orders.handle(ship, "brace the head yards to the wind")
    assert kind == "evolution.started"
    assert {s for _, s, _ in runner.started} == set(ship.groups["head yards"])
    assert all(p["mode"] == "to the wind" and p["target_angle"] > 0 for _, _, p in runner.started)
    assert data["trimmed_sheets"] == [] and data["mode"] == "to the wind"


def test_plural_sided_lines_mean_both_sides_unless_a_side_is_said():
    ship, _ = make("frigate", tack="larboard")
    _, log, data = orders.handle(ship, "ease the fore topsail sheets")
    assert data["subjects"] == ["fore.topsail.sheet.starboard", "fore.topsail.sheet.larboard"]
    assert data["side"] == "both"
    _, log, data = orders.handle(ship, "ease the lee fore topsail sheets")
    assert data["subjects"] == ["fore.topsail.sheet.starboard"]
    _, log, data = orders.handle(ship, "ease the topsail sheets")
    assert len(data["subjects"]) == 6  # every topsail sheet on three masts
    # the frigate's main sheet is the main course's, a sided family
    _, log, data = orders.handle(ship, "ease the weather main sheet")
    assert data["subjects"] == ["main.course.sheet.larboard"]
    assert "larboard (weather) main course sheet" in log
    with pytest.raises(OrderError, match="Which main sheet"):
        orders.handle(ship, "haul the main sheet")


def test_a_line_order_works_the_lines_it_can_and_reports_the_rest():
    ship, _ = make("frigate")
    ship.lines["fore.topsail.sheet.starboard"].hauled = 0.5
    kind, log, data = orders.handle(ship, "haul home the fore topsail sheets")
    assert kind == "line.hauled"
    assert data["subjects"] == ["fore.topsail.sheet.starboard"]
    assert ship.lines["fore.topsail.sheet.starboard"].hauled == 1.0
    assert "Hauled the starboard fore topsail sheet home" in log
    assert "Not done: the larboard fore topsail sheet is already hauled home" in log


def test_haul_aft_and_home_take_the_line_all_the_way():
    ship, _ = make("frigate")
    spanker = ship.sails["mizzen.spanker"]
    floor = units.deg_to_rad(18.0)  # a gaff sail's floor (trim.TRIM_RANGE)
    orders.handle(ship, "ease the spanker sheet three fathoms")
    assert spanker.sheet_angle > floor + units.deg_to_rad(5)
    _, log, _ = orders.handle(ship, "haul aft the spanker sheet")
    assert spanker.sheet_angle == pytest.approx(floor) and "flat aft" in log
    orders.handle(ship, "ease the spanker sheet")
    orders.handle(ship, "haul the spanker sheet aft")
    assert spanker.sheet_angle == pytest.approx(floor)
    halyard = ship.lines["fore.topsail.yard.halyard"]
    orders.handle(ship, "ease the fore topsail halyard four fathoms")
    assert halyard.hauled == pytest.approx(0.6)
    orders.handle(ship, "haul the fore topsail halyard home")
    assert halyard.hauled == 1.0
    yard = ship.spars["main.yard"]
    orders.handle(ship, "haul the larboard main brace home")
    assert yard.brace_angle == pytest.approx(yard.brace_limit)


def test_sheet_home_hauls_every_sheet_of_the_sail():
    ship, _ = make("frigate")
    for side in ("starboard", "larboard"):
        ship.lines[f"fore.topsail.sheet.{side}"].hauled = 0.3
    ship.lines["fore.topsail.sheet.larboard"].state = LineState.FREE
    kind, log, data = orders.handle(ship, "sheet home the fore topsail")
    assert kind == "line.hauled" and log == "Sheeted home the fore topsail."
    for side in ("starboard", "larboard"):
        line = ship.lines[f"fore.topsail.sheet.{side}"]
        assert line.hauled == 1.0 and line.state is LineState.BELAYED
    with pytest.raises(OrderError, match="sheeted home already"):
        orders.handle(ship, "sheet home the fore topsail")
    # a fore-and-aft sail: the sheet hauled flat aft, to the sail's floor (package 32e)
    from freesail.evolutions import trim

    spanker = ship.sails["mizzen.spanker"]
    trim.set_sheet_angle(ship, spanker, units.deg_to_rad(25))
    _, log, _ = orders.handle(ship, "sheet home the spanker")
    assert spanker.sheet_angle == pytest.approx(units.deg_to_rad(18)) and "flat aft" in log
    with pytest.raises(OrderError, match="You sheet home sails"):
        orders.handle(ship, "sheet home the fore topsail sheet, starboard")


def test_take_in_words_start_the_take_in_when_they_suit_the_sail():
    ship, runner = make("frigate")
    for sid in ("main.course", "mizzen.spanker", "fore.topsail", "jib"):
        ship.sails[sid].state = SailState.SET
    orders.handle(ship, "haul up the mainsail")
    orders.handle(ship, "brail up the spanker")
    orders.handle(ship, "clew up the fore topsail")
    orders.handle(ship, "haul down the jib")
    assert [(e, s) for e, s, _ in runner.started] == [
        ("take_in_square", "main.course"),
        ("take_in_gaff", "mizzen.spanker"),
        ("take_in_square", "fore.topsail"),
        ("take_in_jibheaded", "jib"),
    ]
    ship, runner = make("schooner")
    ship.sails["main.sail"].state = SailState.SET
    _, log, _ = orders.handle(ship, "lower the mainsail")
    assert runner.started == [("take_in_gaff", "main.sail", {})]
    with pytest.raises(OrderError, match="cannot be scandalised"):
        orders.handle(ship, "scandalise the mainsail")
    assert len(runner.started) == 1


def test_take_in_with_a_count_of_reefs_is_a_reef():
    ship, runner = make("frigate")
    ship.sails["fore.topsail"].state = SailState.SET
    orders.handle(ship, "take in one reef in the fore topsail")
    orders.handle(ship, "take in two reefs in the fore topsail")
    assert runner.started == [
        ("reef_square", "fore.topsail", {"reefs": 1}),
        ("reef_square", "fore.topsail", {"reefs": 2}),
    ]
    o = parse(ship, "take in one reef in the topsails")
    assert o.verb == "reef" and o.modifiers == {"reefs": 1}


def test_shake_out_the_reefs_takes_them_all():
    ship, runner = make("frigate")
    sail = ship.sails["fore.topsail"]
    sail.state = SailState.SET
    sail.reefs = 2
    orders.handle(ship, "shake out the reefs in the fore topsail")
    assert runner.started[-1] == ("shake_out_square", "fore.topsail", {"reefs": 2, "close": True})
    orders.handle(ship, "shake the reefs out of the fore topsail")
    assert runner.started[-1][2] == {"reefs": 2, "close": True}
    orders.handle(ship, "shake out the reef in the fore topsail")
    assert runner.started[-1][2] == {"reefs": 1}


def test_compound_objects_join_their_parts():
    ship, runner = make("frigate")
    orders.handle(ship, "set the topsails and topgallants")
    assert [s for _, s, _ in runner.started] == ship.groups["topsails"] + ship.groups["topgallants"]
    runner.started.clear()
    _, log, data = orders.handle(ship, "brace the fore and main yards square")
    assert {s for _, s, _ in runner.started} == set(
        ship.groups["fore yards"] + ship.groups["main yards"]
    )
    assert data["object"] == "fore yards and main yards"
    o = parse(ship, "set the fore and main topsails")
    assert o.object == "fore and main topsails"
    with pytest.raises(UnknownNounError, match="no such part as the spanker"):
        orders.handle(make("schooner")[0], "set the jib and the spanker")


def test_half_points_are_kept():
    ship, _ = make("frigate", tack="starboard")
    ship.dyn.heading = units.deg_to_rad(90)
    ship.dyn.target_heading = ship.dyn.heading
    _, log, data = orders.handle(ship, "come up half a point")
    assert data["points"] == 0.5 and "come up half a point" in log
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 + 5.625))
    orders.handle(ship, "bear away a point and a half")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 + 5.625 - 16.875))
    orders.handle(ship, "steer two and a half points to starboard")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(90 - 11.25 + 28.125))
    assert parse(ship, "come up a half point").modifiers["points"] == 0.5


def test_conning_words_set_the_helm_modes():
    ship, _ = make("frigate", tack="starboard")
    ship.dyn.heading = units.deg_to_rad(293)
    orders.handle(ship, "hard a-lee")
    assert ship.dyn.helm_mode is HelmMode.RUDDER
    assert ship.dyn.target_rudder == pytest.approx(
        units.deg_to_rad(35)
    )  # to starboard: to windward
    orders.handle(ship, "hard up")
    assert ship.dyn.target_rudder == pytest.approx(units.deg_to_rad(-35))
    orders.handle(ship, "right the helm")
    assert ship.dyn.helm_mode is HelmMode.RUDDER and ship.dyn.target_rudder == 0.0
    ship.dyn.heading = units.deg_to_rad(300)
    _, log, _ = orders.handle(ship, "steady")
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(300))
    assert ship.dyn.steady is False and "NW by W (300°)" in log
    ship.dyn.heading = units.deg_to_rad(310)
    orders.handle(ship, "meet her")
    assert ship.dyn.target_heading == pytest.approx(units.deg_to_rad(310))
    orders.handle(ship, "nothing off")
    assert ship.dyn.helm_mode is HelmMode.FULL_AND_BY
    # on the larboard tack a-lee is to larboard
    ship, _ = make("frigate", tack="larboard")
    orders.handle(ship, "helm's a-lee")
    assert ship.dyn.target_rudder == pytest.approx(units.deg_to_rad(-35))


def test_ship_evolutions_use_the_ship_as_subject():
    ship, runner = make("frigate")
    orders.handle(ship, "heave to on the larboard tack")
    assert runner.started == [("heave_to", "ship", {"tack": "larboard"})]


def test_runner_refusal_is_the_order_refusal():
    ship, _ = make("frigate", refuse={"ship": "she has not way enough to stay"})
    with pytest.raises(OrderError, match="not way enough"):
        orders.handle(ship, "tack ship")


def test_missing_runner_is_a_sentence():
    ship = Ship(SPECS["frigate"])
    with pytest.raises(OrderError, match="no evolution runner"):
        orders.handle(ship, "set the fore topsail")
    # helm and level 0 need no runner
    orders.handle(ship, "steer north")
    orders.handle(ship, "ease the fore topsail halyard")


# ---------------------------------------------------------------------------
# Group evolutions from the vocabulary
# ---------------------------------------------------------------------------


def test_make_all_sail_skips_what_the_ship_lacks_and_reports_what_fails():
    ship, runner = make("schooner")
    ship.sails["flying_jib"].state = SailState.SET
    kind, log, data = orders.handle(ship, "make all sail")
    started = [s for _, s, _ in runner.started]
    assert "fore.royal" not in started  # no royals: passed over in silence
    assert "royals" not in log
    assert "flying jib is already set" in log  # a real failure is reported
    assert set(started) == {
        "fore.sail",
        "main.sail",
        "fore.topsail",
        "fore.topgallant",
        "fore.staysail",
        "jib",
        "main.gaff_topsail",
        "fore.topmast.studdingsail.starboard",
        "fore.topmast.studdingsail.larboard",
    }
    assert data["group"] is True and data["verb"] == "make all sail"


def test_shorten_sail_on_a_ship_under_all_sail():
    ship, runner = make("frigate")
    for sail in ship.sails.values():
        sail.state = SailState.SET
    _, log, _ = orders.handle(ship, "shorten sail")
    evos = {(e, s) for e, s, _ in runner.started}
    assert ("take_in_studding", "fore.topmast.studdingsail.starboard") in evos
    assert ("take_in_square", "main.royal") in evos
    assert ("take_in_jibheaded", "flying_jib") in evos
    assert ("take_in_square", "mizzen.topgallant") in evos
    assert ("reef_square", "main.topsail") in evos
    assert "Not done" not in log


def test_group_evolution_with_nothing_to_do_is_rejected():
    ship, _ = make("schooner")
    for sail in ship.sails.values():
        sail.state = SailState.SET
    with pytest.raises(OrderError, match="Could not set plain sail"):
        orders.handle(ship, "set plain sail")


# ---------------------------------------------------------------------------
# Parsing and resolution details
# ---------------------------------------------------------------------------


def test_parse_gives_an_order_with_verb_object_modifiers_and_side():
    ship, _ = make("frigate")
    o = parse(ship, "Brace the fore yards sharp up on the larboard tack, handsomely")
    assert o.verb == "brace"
    assert o.object == "fore yards"
    assert o.modifiers == {"brace_mode": "sharp up", "tack": "larboard", "manner": "handsomely"}
    assert o.side_word is None
    o = parse(ship, "haul the weather main brace")
    assert (o.verb, o.object, o.side_word) == ("haul", "main brace", "weather")
    o = parse(ship, "set studdingsails, both sides")
    assert (o.object, o.side_word) == ("studdingsails", "both")
    o = parse(ship, "steer sou'-west by west")
    assert o.modifiers["heading"] == pytest.approx(units.deg_to_rad(236.25))
    assert o.modifiers["heading_text"] == "south-west by west"


def test_generated_names_cover_ids_aliases_groups_and_contractions():
    ship, _ = make("frigate")
    table = resolve.noun_table(ship)
    for phrase, ids in [
        ("fore.topsail", ["fore.topsail"]),
        ("fore topsail", ["fore.topsail"]),
        ("the fore topsail", None),  # 'the' is stripped by the parser, not the table
        ("fore tops'l", ["fore.topsail"]),
        ("main t'gallant", ["main.topgallant"]),
        ("main tgallant", ["main.topgallant"]),
        ("cro'jack yard", ["mizzen.crossjack.yard"]),
        ("mizzen crossjack yard", ["mizzen.crossjack.yard"]),
        ("mizzen crojack yard", ["mizzen.crossjack.yard"]),
        ("main brace", ["main.yard.brace.starboard", "main.yard.brace.larboard"]),
        ("weather main brace", None),  # sides are resolved by resolve(), not the table
        ("starboard main brace", ["main.yard.brace.starboard"]),
        ("main brace starboard", ["main.yard.brace.starboard"]),
        ("port main brace", ["main.yard.brace.larboard"]),
        ("main yard brace larboard", ["main.yard.brace.larboard"]),
        ("fore topsail halyard", ["fore.topsail.yard.halyard"]),
        ("fore topsail yard halyard", ["fore.topsail.yard.halyard"]),
        ("spanker sheet", ["mizzen.spanker.sheet"]),
        ("driver sheet", ["mizzen.spanker.sheet"]),
        ("spanker peak halyard", ["mizzen.gaff.peak_halyard"]),
        ("foresail tack", ["fore.course.tack.starboard", "fore.course.tack.larboard"]),
        ("royals", ["fore.royal", "main.royal", "mizzen.royal"]),
        ("stuns'ls", ship.groups["studdingsails"]),
        ("kites", ship.groups["studdingsails"]),
        ("fore and aft sails", ship.groups["fore-and-aft sails"]),
    ]:
        noun = table.lookup(phrase)
        if ids is None:
            assert noun is None, phrase
        else:
            assert noun is not None, phrase
            assert noun.ids == ids, (phrase, noun)


def test_the_noun_table_is_built_once_and_cached_on_the_ship():
    ship, _ = make("frigate")
    assert "orders.nouns" not in ship.extra
    orders.handle(ship, "steer north")
    assert "orders.nouns" not in ship.extra  # helm orders need no nouns
    orders.handle(ship, "ease the fore topsail halyard")
    table = ship.extra["orders.nouns"]
    orders.handle(ship, "ease the fore topsail halyard")
    assert ship.extra["orders.nouns"] is table


def test_display_names_read_as_a_sailor_would_say_them():
    ship, _ = make("frigate")
    assert resolve.display_name(ship, "main.yard.brace.starboard") == "starboard main brace"
    assert resolve.display_name(ship, "fore.topmast_staysail") == "fore topmast staysail"
    assert resolve.display_name(ship, "fore.topsail.yard") == "fore topsail yard"
    assert resolve.display_name(ship, "fore.topsail.yard.halyard") == "fore topsail halyard"
    assert (
        resolve.display_name(ship, "fore.topmast.studdingsail.larboard.halyard")
        == "larboard fore topmast studdingsail halyard"
    )
    assert resolve.display_name(ship, "mizzen.gaff.peak_halyard") == "mizzen gaff peak halyard"


def test_suggestions_are_deterministic_and_plainly_spelt():
    ship, _ = make("frigate")
    messages = set()
    for _ in range(3):
        with pytest.raises(UnknownNounError) as info:
            orders.handle(ship, "set the fore topsl yard sheet")
        messages.add(str(info.value))
    assert len(messages) == 1
    message = messages.pop()
    assert "did you mean" in message
    assert "'" not in message.split("did you mean")[1].split("?")[0]  # no contractions offered
    assert "." not in message.split("did you mean")[1].split("?")[0]  # no raw ids offered


def test_unknown_word_after_a_good_verb_and_object_is_named():
    ship, _ = make("frigate")
    with pytest.raises(OrderError) as info:
        orders.handle(ship, "brace the fore yards sharp up smartish")
    assert "'brace' was understood, but not 'smartish'" in str(info.value)
    assert "did you mean 'smartly'" in str(info.value)
    # a stray word right after the noun reads as a longer noun the ship lacks
    with pytest.raises(UnknownNounError) as info2:
        orders.handle(ship, "brace the fore yards sharply up")
    assert "no such part as the fore yards sharply" in str(info2.value)
    assert "did you mean the fore yards" in str(info2.value)


# ---------------------------------------------------------------------------
# In the World
# ---------------------------------------------------------------------------


def test_the_world_logs_an_accepted_order_and_journals_it():
    ship, runner = make("frigate")
    ship.order_handler = orders.handle
    world = World(seed=1, scenario=Scenario(ship_heading_deg=90), ship=ship)
    event = world.submit("set the fore topsail")
    # the World logs the acceptance; the runner (a fake here) writes the "started" line itself
    assert event.kind == "order.accepted"
    assert world.journal == [(0, "captain", "set the fore topsail")]
    assert [e.kind for e in world.log][-1:] == ["order.accepted"]
    assert runner.started == [("set_square", "fore.topsail", {})]


def test_the_world_logs_a_rejected_order_and_does_not_journal_it():
    ship, runner = make("frigate")
    ship.order_handler = orders.handle
    world = World(seed=1, ship=ship)
    event = world.submit("set the topsail")
    assert event.kind == "order.rejected"
    assert "fore topsail" in event.text and "mizzen topsail" in event.text
    assert world.journal == []
    assert runner.started == []


def test_the_resolved_side_is_in_the_event_data_for_replay():
    ship, _ = make("frigate", tack="larboard")
    ship.order_handler = orders.handle
    world = World(seed=1, ship=ship)
    event = world.submit("haul the weather main brace")
    assert event.kind == "line.hauled"
    assert event.data["side"] == "larboard"
    assert event.data["subjects"] == ["main.yard.brace.larboard"]


def test_decimal_headings_survive_normalisation():
    ship, _ = make("frigate")
    _, text, data = orders.handle(ship, "steer 280.0")
    assert "280" in text and abs(units.rad_to_deg(ship.dyn.target_heading) - 280.0) < 1e-6
    _, text, data = orders.handle(ship, "steer 280.5")
    assert abs(units.rad_to_deg(ship.dyn.target_heading) - 280.5) < 1e-6


# ---------------------------------------------------------------------------
# Belaying work (package 29c): which verb a "belay" is
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, verb, obj",
    [
        # the bare word to stop is "belay that": the last order's work
        ("belay", "belay that", None),
        ("Belay!", "belay that", None),
        ("avast", "belay that", None),
        ("belay that", "belay that", None),
        ("belay that order", "belay that", None),
        ("cancel that", "belay that", None),
        ("belay there", "belay that", None),
        # everything in hand or waiting
        ("belay all work", "belay all work", None),
        ("belay all", "belay all work", None),
        ("belay all orders", "belay all work", None),
        ("cancel all orders", "belay all work", None),
        ("cancel all work", "belay all work", None),
        ("cancel orders", "belay all work", None),
        ("avast all", "belay all work", None),
        # the work by its name, its order, its kind or its sail
        ("belay reefing the mainsail", "belay the work", "reefing the mainsail"),
        ("belay reef the mainsail, one reef", "belay the work", "reef the mainsail, one reef"),
        ("belay the reef", "belay the work", "the reef"),
        ("belay the mainsail", "belay the work", "the mainsail"),
        ("avast bracing", "belay the work", "bracing"),
        ("cancel the reef in the mainsail", "belay the work", "the reef in the mainsail"),
        ("belay the work on the jib", "belay the work", "the jib"),
        # a line is still the line verb
        ("belay the jib sheet", "belay", "jib sheet"),
        ("belay the main sheet", "belay", "main sheet"),
        ("make fast the jib sheet", "belay", "jib sheet"),
    ],
)
def test_belay_is_read_as_work_or_as_a_line(text, verb, obj):
    ship, _ = make("schooner")
    order = parse(ship, text)
    assert order.verb == verb
    assert order.object == obj


def test_a_belay_that_names_nothing_is_the_line_verbs_refusal():
    """Words that read as neither work nor a line are left to the line verb, whose
    refusal names the nearest lines."""
    ship, _ = make("schooner")
    with pytest.raises(UnknownNounError, match="did you mean the main sheet"):
        parse(ship, "belay the mian sheet")


def test_belaying_with_no_runner_that_keeps_work_is_refused_in_words():
    ship, _ = make("frigate")
    ship.extra.pop("evolutions")
    with pytest.raises(OrderError, match="no evolution runner"):
        orders.handle(ship, "belay that")


# ---------------------------------------------------------------------------
# Package 30b: clearing a wreck, shifting a spar, the booms (playtest 10, finding 1)
# ---------------------------------------------------------------------------

BOOM = "fore.topmast.studdingsail_boom.larboard"
STUNSL = "fore.topmast.studdingsail.larboard"


def wrecked(which: str = "schooner", spar: str = BOOM):
    """A ship with a spar carried away, as the strain model leaves it."""
    from freesail.physics import strain

    ship, runner = make(which)
    ship.sails[STUNSL].state = SailState.SET
    strain._wreck_spar(ship, strain.strain_state(ship), ship.spars[spar], 2.0)
    ship.drain_notes()
    return ship, runner


@pytest.mark.parametrize(
    ("text", "verb", "obj"),
    [
        (
            "cut away the larboard fore topmast studdingsail boom",
            "cut away",
            "fore topmast studdingsail boom",
        ),
        ("cut away the larboard fore topmast stuns'l", "cut away", "fore topmast stuns'l"),
        ("clear away the wreck of the fore topsail yard", "cut away", "fore topsail yard"),
        ("clear the wreck of the fore topsail yard", "cut away", "fore topsail yard"),
        ("cut adrift the wreck of the fore topmast", "cut away", "fore topmast"),
        ("clear the wreck", "cut away", None),
        ("clear away the wreck", "cut away", None),
        ("cut away the wreck", "cut away", None),
        ("send down the fore topsail yard", "send down", "fore topsail yard"),
        ("send down the wreck of the fore topsail yard", "send down", "fore topsail yard"),
        ("shift the fore topsail yard", "shift", "fore topsail yard"),
        ("the booms", "the booms", None),
        ("the spare spars", "the booms", None),
        ("the sail room", "the sail room", None),
        # a line cleared away is let go, as it always was
        ("clear away the weather bowlines", "let go", "bowlines"),
    ],
)
def test_the_words_for_a_wreck_and_the_booms_parse(text, verb, obj):
    ship, _ = make("schooner")
    order = parse(ship, text)
    assert order.verb == verb
    assert order.object == obj


def test_the_playtests_five_orders_now_clear_the_wreck_or_say_how():
    """Playtest 10: five orders to deal with the carried-away boom, all refused. Now the
    wreck is cleared by `send down` of the boom, `cut away` of the sail and `clear away`
    of the boom (each the whole wreck), the sail is unbent out of it, and `shift` of the
    sail says what to do first."""
    ship, runner = wrecked()
    orders.handle(ship, "Send down the larboard fore topmast studdingsail boom")
    orders.handle(ship, "Unbend the larboard fore topmast studding sail")
    orders.handle(ship, "Cut away the larboard fore topmast studding sail")
    orders.handle(ship, "Clear away the larboard fore topmast studdingsail boom")
    assert runner.started == [
        ("clear_wreck", BOOM, {"part": BOOM, "send_down": True}),
        ("unbend_sail", STUNSL, {"sail": STUNSL}),
        ("clear_wreck", BOOM, {"part": BOOM}),
        ("clear_wreck", BOOM, {"part": BOOM}),
    ]
    with pytest.raises(OrderError) as refused:
        orders.handle(ship, "Shift the larboard fore topmast studding sail")
    assert str(refused.value) == (
        "The larboard fore topmast studdingsail went with the larboard fore topmast "
        "studdingsail boom when it carried away; cut away the wreck, then shift the larboard "
        "fore topmast studdingsail boom for a spare."
    )
    with pytest.raises(OrderError, match="went with the larboard fore topmast studdingsail"):
        orders.handle(ship, "set the larboard fore topmast studdingsail")


def test_clear_the_wreck_clears_every_wreck_aboard_and_says_when_there_is_none():
    ship, runner = make("schooner")
    with pytest.raises(OrderError) as refused:
        orders.handle(ship, "clear the wreck")
    assert str(refused.value) == (
        "There is no wreck aboard to clear: every spar stands and no sail hangs in rags."
    )
    ship, runner = wrecked()
    ship.sails["fore.topsail"].state = SailState.BLOWN_OUT
    orders.handle(ship, "clear the wreck")
    assert [(e, s) for e, s, _ in runner.started] == [
        ("clear_wreck", BOOM),
        ("clear_wreck", "fore.topsail"),
    ]


@pytest.mark.parametrize(
    ("text", "words"),
    [
        ("cut away the jib", "The jib is sound and furled; there is no wreck to cut away."),
        (
            "cut away the fore topsail yard",
            "The fore topsail yard stands sound; there is no wreck to cut away.",
        ),
        (
            "send down the fore topgallant mast",
            "The fore topgallant mast stands sound; the topgallant masts go down together: "
            "'send down the topgallant masts'.",
        ),
        (
            "send down the starboard fore topmast studdingsail boom",
            "The starboard fore topmast studdingsail boom stands sound; a studding-sail boom is "
            "rigged in, not sent down: 'rig in the starboard fore topmast studdingsail boom'.",
        ),
        (
            "send down the jib",
            "The jib is not carried away; a sail is unbent and sent down with 'unbend the jib'.",
        ),
        ("send down", "Send down what?"),
        ("shift the main boom for the heavy one", "A spar has no canvas"),
        ("shift the main boom for the jib", "A spar is shifted for a spare of its class"),
        ("the booms please", "'the booms' is a question and takes nothing after it"),
    ],
)
def test_a_wreck_order_on_a_sound_part_is_refused_in_words_that_teach(text, words):
    ship, runner = wrecked()
    with pytest.raises(OrderError) as refused:
        orders.handle(ship, text)
    assert str(refused.value).startswith(words)
    assert runner.started == []


def test_shift_of_a_spar_starts_shift_spar_and_the_runner_refuses_in_its_words():
    ship, runner = wrecked()
    orders.handle(ship, "shift the larboard fore topmast studdingsail boom for a spare")
    assert runner.started == [("shift_spar", BOOM, {"part": BOOM})]
    ship, runner = wrecked()
    runner.refuse = {BOOM: "No spare studding-sail boom aboard; the dockyard must supply one."}
    with pytest.raises(OrderError) as refused:
        orders.handle(ship, "shift the larboard fore topmast studdingsail boom")
    assert str(refused.value) == "No spare studding-sail boom aboard; the dockyard must supply one."


def test_the_booms_and_the_sail_room_are_queries_answered_by_the_ship():
    """In the form of `the sail room` (spec 3b §6.3): the console answers them itself,
    and the browser's command line through the ship, as a `query.` kind the World logs
    and does not journal."""
    ship, _ = make("frigate")
    kind, text, _ = orders.handle(ship, "the booms")
    assert kind == "query.booms"
    assert text == (
        "The booms hold 12 spare spars: 2 topmasts, 2 topgallant masts, 2 yards, 4 "
        "studding-sail booms, 1 jib-boom and 1 flying jib-boom."
    )
    kind, text, _ = orders.handle(ship, "the sail room")
    assert kind == "query.sail_room" and text.startswith("The sail room holds 21 sails.")
    ship.order_handler = orders.handle
    world = World(seed=1, scenario=Scenario(), ship=ship)
    e = world.submit("the spare spars")
    assert e.kind == "query.booms" and world.journal == []


def test_completion_offers_the_wreck_and_the_spar_to_shift():
    from freesail.orders import complete

    ship, _ = wrecked()
    offered = complete.suggestions(ship, "cut away the ", limit=20)
    assert "cut away the larboard fore topmast studdingsail boom" in offered
    assert "cut away the larboard fore topmast studdingsail" in offered
    assert not any("starboard" in o or "jib" in o for o in offered)  # sound parts are not
    offered = complete.suggestions(ship, "shift the larboard fore topmast studdingsail b")
    assert offered == ["shift the larboard fore topmast studdingsail boom"]
    offered = complete.suggestions(ship, "the bo")
    # package 31b; the boat and the boats (package 35) stand before the booms
    assert "the booms" in offered[:3] and "the boatswains store" in offered
    assert "the boat" in offered and "the boats" in offered


# ---------------------------------------------------------------------------
# Package 33c: the forty-nine orders refused in gate 5b's playtests, each with what it
# does now (the refused orders of playtests 12 and 13, `refused.md`, `refused-cutter.md`
# and `refused-brig.md` in their folders under docs/playtests/, with the lead's reading).
# Each is given through `World.submit`, the one path the console and the browser share,
# to its ship on the chart of the western Channel at seed 7, at a position and an hour
# like the session's; those to be taken give their new answer, those still refused keep
# their words.
# ---------------------------------------------------------------------------


@dataclass
class took:
    kinds: tuple[str, ...]  # the kind of the line `submit` returns
    mentions: tuple[str, ...] = ()  # substrings of its text
    started: tuple[str, ...] = ()  # evolutions the runner holds afterwards


@dataclass
class still:
    mentions: tuple[str, ...] = ()  # substrings of the refusal


def voyage(ship: str, lat: float, lon: float, hhmm: str) -> World:
    from datetime import datetime

    from freesail.api.session import make_world

    h, m = (int(x) for x in hhmm.split(":"))
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, h, m),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
    )
    return make_world(7, str(SHIP_FILES[ship]), scenario)


def _set(*sail_ids: str):
    def setup(w: World) -> None:
        for sid in sail_ids:
            w.ship.sails[sid].state = SailState.SET
        w.run(5)  # the apparent wind on deck, that a trim is made to

    return setup


def _sheets_eased_off(*sail_ids: str):
    def setup(w: World) -> None:
        _set(*sail_ids)(w)
        for line in w.ship.lines.values():
            if line.cls == "sheet" and line.of in sail_ids:
                line.hauled = 0.0

    return setup


def _close_reefed_topsail(w: World) -> None:
    sail = w.ship.sails["topsail"]
    sail.state, sail.reefs = SailState.SET, sail.reef_bands


def _orders(*texts: str):
    def setup(w: World) -> None:
        for t in texts:
            w.submit(t)

    return setup


def _reaching(w: World) -> None:
    w.submit("set plain sail")
    w.submit("steer east")
    w.run(600)


def _plain_sail(w: World) -> None:
    for sid in w.ship.groups["plain sail"]:
        w.ship.sails[sid].state = SailState.SET


# The passage's frigate well out from the Lizard, as at half past noon (the Lizard was
# raised at 15:42); the cutter off Falmouth at four in the afternoon with Manacle Point in
# sight and the Manacles not; the same a little south with the Old Wall not in sight; the
# brig off Ushant at dawn.
OFFING = (49.20, -5.30)
OFF_FALMOUTH = (50.11, -4.97)
SOUTH_OF_IT = (50.06, -5.00)
OFF_USHANT = (48.53, -4.98)
TRIM_FAIR = ("evolution.started", "order.accepted", "sail.trimmed")
QUERY = ("query.reading",)
HELD = ("Held until the ship can carry it out", "no well to sound yet")
SCANDALISE = "cannot be scandalised: the physics has no state for a gaff sail with its peak"
MANACLES = (
    "The Manacles are not in sight (a danger of the chart); Manacle Point, in sight, is "
    "another feature"
)
BLIND_LEAD = 'standing order "Blind Lead": every 10 minutes then heave the lead'
TRIM_BY_THE_WIND = (
    'standing order "Trim Sails by the Wind": when the true wind veers 1 point or backs 1 '
    "point then trim sails"
)

PLAYTEST_REFUSALS: list[tuple[str, str, tuple[float, float], str, Any, took | still]] = [
    # -- playtest 12, the frigate's passage (refused.md: fifteen) ------------------------
    (
        "frigate",
        "04:00",
        OFFING,
        'standing order "sound the well": every glass then sound the well',
        None,
        took(("standing.given",), HELD),
    ),
    ("frigate", "08:01", OFFING, "Trim the spanker sheet", _set("mizzen.spanker"), took(TRIM_FAIR)),
    ("frigate", "08:02", OFFING, "Tend the spanker sheet", _set("mizzen.spanker"), took(TRIM_FAIR)),
    (
        "frigate",
        "12:29",
        OFFING,
        "The reckoning",
        None,
        took(QUERY, ("The reckoning: ", "account")),
    ),
    (
        "frigate",
        "12:29",
        OFFING,
        "the reckoning",
        None,
        took(QUERY, ("The reckoning: ", "account")),
    ),
    ("frigate", "12:30", OFFING, "the master", None, took(QUERY, ("The master: Mr ", "on deck"))),
    (
        "frigate",
        "12:32",
        OFFING,
        "the bearing of the Lizard",
        None,
        took(QUERY, ("The bearing of the Lizard: not in sight.",)),
    ),
    (
        "frigate",
        "12:32",
        OFFING,
        "What is the bearing of the lizard",
        None,
        took(QUERY, ("The bearing of the lizard: not in sight.",)),
    ),
    (
        "frigate",
        "12:32",
        OFFING,
        "Ask the master the reckoning",
        None,
        took(QUERY, ("The reckoning: ",)),
    ),
    (
        "frigate",
        "12:37",
        OFFING,
        "work up a reckoning",
        None,
        took(("reckoning.worked",), ("The reckoning worked up: ",)),
    ),
    ("frigate", "12:37", OFFING, "take a bearing of the Lizard", None, still(("in sight",))),
    (
        "frigate",
        "12:38",
        OFFING,
        "work up the reckoning's uncertainty",
        None,
        took(("reckoning.worked",), ("I would not trust the reckoning",)),
    ),
    (
        "frigate",
        "12:38",
        OFFING,
        "take the reckoning's uncertainty",
        None,
        took(QUERY, ("The reckoning's uncertainty: I would not trust",)),
    ),
    (
        "frigate",
        "18:11",
        OFFING,
        "Steer for falmouth",
        None,
        took(("helm.set",), ("Shaped a course for Falmouth", "Helm ordered: steer")),
    ),
    (
        "frigate",
        "18:18",
        OFFING,
        "Take a sounding",
        None,
        took(("order.accepted",), started=("heave_lead",)),
    ),
    # -- playtest 13, the cutter (refused-cutter.md: sixteen) ----------------------------
    (
        "cutter",
        "04:02",
        OFF_FALMOUTH,
        "Set the mainsail, one reef",
        None,
        took(("order.accepted",), started=("set_gaff", "reef_gaff")),
    ),
    (
        "cutter",
        "05:21",
        OFF_FALMOUTH,
        "Ease the jib sheet a fathom",
        _sheets_eased_off("jib"),
        still(("already eased right off",)),
    ),
    (
        "cutter",
        "05:21",
        OFF_FALMOUTH,
        "Ease the fore staysail sheet a fathom",
        _sheets_eased_off("fore.staysail"),
        still(("already eased right off",)),
    ),
    (
        "cutter",
        "10:01",
        OFF_FALMOUTH,
        "Reef the topsail, one reef",
        _close_reefed_topsail,
        still(("already close reefed (1 reef in)",)),
    ),
    (
        "cutter",
        "10:56",
        OFF_FALMOUTH,
        "Reef the topsail, one reef",
        _close_reefed_topsail,
        still(("already close reefed (1 reef in)",)),
    ),
    (
        "cutter",
        "16:17",
        OFF_FALMOUTH,
        "take a bearing of manacle",
        None,
        took(("bearing.taken",), ("Manacle Point bore ",)),
    ),
    ("cutter", "16:33", OFF_FALMOUTH, "sightings", None, took(QUERY, ("The sightings: ",))),
    (
        "cutter",
        "16:34",
        OFF_FALMOUTH,
        "takc a bearing of old wall",
        None,
        still(("is not an order this ship understands",)),
    ),
    (
        "cutter",
        "16:34",
        OFF_FALMOUTH,
        "take a bearing of black rock",
        None,
        still(("The Black Rock is not in sight (a danger of the chart)", "in sight: ")),
    ),
    (
        "cutter",
        "16:34",
        OFF_FALMOUTH,
        "Take a bearing of rosemullian head",
        None,
        still(("Rosemullian head is not in sight; did you mean Rosemullion Head",)),
    ),
    ("cutter", "16:51", OFF_FALMOUTH, "take a bearing of manacles", None, still((MANACLES,))),
    (
        "cutter",
        "16:51",
        OFF_FALMOUTH,
        "take a bearing of manacle",
        None,
        took(("bearing.taken",), ("Manacle Point bore ",)),
    ),
    (
        "cutter",
        "17:06",
        SOUTH_OF_IT,
        "take a bearing of the old wall",
        None,
        still(("The Old Wall is not in sight (a danger of the chart)",)),
    ),
    (
        "cutter",
        "17:41",
        OFF_FALMOUTH,
        "belay heave the lead",
        _orders("heave the lead"),
        took(("work.belayed",), ("Belayed heaving lead",)),
    ),
    (
        "cutter",
        "17:41",
        OFF_FALMOUTH,
        "avast heave lead",
        _orders("heave the lead"),
        took(("work.belayed",), ("Belayed heaving lead",)),
    ),
    ("cutter", "17:41", OFF_FALMOUTH, "tack ship", _reaching, still(("She is not close-hauled",))),
    # -- playtest 13, the brig (refused-brig.md: eighteen) -------------------------------
    (
        "brig",
        "04:19",
        OFF_USHANT,
        'Standing order "Trim Sails by the Glass" Every glass then trim the sails',
        None,
        still(("After the name say a colon",)),
    ),
    (
        "brig",
        "04:31",
        OFF_USHANT,
        "Bend the ringtail",
        None,
        still(("no such part as the ringtail",)),
    ),
    ("brig", "04:53", OFF_USHANT, "Take a bearing", None, still(("Take a bearing of what?",))),
    ("brig", "04:53", OFF_USHANT, "Take a bearing of", None, still(("Take a bearing of what?",))),
    ("brig", "04:53", OFF_USHANT, "Take a bearing of f", None, still(("F is not in sight",))),
    (
        "brig",
        "05:16",
        OFF_USHANT,
        "Bend the save-alls",
        None,
        still(("no such part as the save alls",)),
    ),
    (
        "brig",
        "12:11",
        OFF_USHANT,
        "Set the lee stuns'ls",
        _plain_sail,
        still(("rigged in; rig it out first",)),
    ),
    (
        "brig",
        "12:23",
        OFF_USHANT,
        'Belay "blind lead"',
        _orders(BLIND_LEAD),
        took(("standing.belayed",), ("Standing order 'Blind Lead' belayed.",)),
    ),
    (
        "brig",
        "16:14",
        OFF_USHANT,
        'Standing order "Night Sails": When the daylight is night then clew up the royals',
        None,
        took(("standing.given",), ("when the daylight is night then clew up the royals",)),
    ),
    (
        "brig",
        "04:36",
        OFF_USHANT,
        'Resume standing order "trim by the wind"',
        _orders(TRIM_BY_THE_WIND, 'belay standing order "Trim Sails by the Wind"'),
        took(("standing.resumed",), ("Standing order 'Trim Sails by the Wind' resumed.",)),
    ),
    # the table's "order as typed" is the refusal's own tail, a copy's slip; the order was
    # `rig out the topmast stuns'ls`, as the refusal and the lead's reading have it
    (
        "brig",
        "12:31",
        OFF_USHANT,
        "rig out the topmast stuns'ls",
        None,
        took(("order.accepted",), started=("rig_out_studdingsail_boom",)),
    ),
    (
        "brig",
        "13:16",
        OFF_USHANT,
        "Haul the starboard fore main brace",
        None,
        still(("no such part as the fore main brace",)),
    ),
    ("brig", "13:16", OFF_USHANT, "Haul the foresail brace", None, still(("Which fore brace",))),
    (
        "brig",
        "13:20",
        OFF_USHANT,
        "Square the sails",
        _plain_sail,
        took(("order.accepted",), started=("brace",)),
    ),
    (
        "brig",
        "13:52",
        OFF_USHANT,
        "Clew up the sails",
        _plain_sail,
        took(("order.accepted", "evolution.started"), started=("take_in_square",)),
    ),
    (
        "brig",
        "13:52",
        OFF_USHANT,
        "Clew up the driver",
        _set("main.spanker"),
        still(("brailed up, not clewed up",)),
    ),
    ("brig", "13:52", OFF_USHANT, "Tryce the driver", _set("main.spanker"), still((SCANDALISE,))),
    (
        "brig",
        "13:52",
        OFF_USHANT,
        "Scandalize the driver",
        _set("main.spanker"),
        still((SCANDALISE,)),
    ),
]


def test_the_playtests_refusals_are_forty_nine():
    assert len(PLAYTEST_REFUSALS) == 49
    ships = [s for s, *_ in PLAYTEST_REFUSALS]
    assert (ships.count("frigate"), ships.count("cutter"), ships.count("brig")) == (15, 16, 18)
    taken = sum(1 for *_, e in PLAYTEST_REFUSALS if isinstance(e, took))
    assert taken == 26  # and twenty-three still refused, each in its words


@pytest.mark.parametrize(
    "ship,when,where,text,setup,expect",
    PLAYTEST_REFUSALS,
    ids=[f"{s} {t}: {x}" for s, t, _, x, _, _ in PLAYTEST_REFUSALS],
)
def test_the_playtests_refusals_now(ship, when, where, text, setup, expect):
    world = voyage(ship, *where, when)
    if setup is not None:
        setup(world)
    journal = len(world.journal)
    e = world.submit(text)
    if isinstance(expect, still):
        assert e.kind == "order.rejected", (e.kind, e.text)
        for m in expect.mentions:
            assert m in e.text, f"{text!r}: expected {m!r} in {e.text!r}"
        assert len(world.journal) == journal
        return
    assert e.kind in expect.kinds, (e.kind, e.text)
    for m in expect.mentions:
        assert m in e.text, f"{text!r}: expected {m!r} in {e.text!r}"
    held = {inst.evo.id for inst in world.ship.extra["evolutions"].instances}
    for evo in expect.started:
        assert evo in held, (text, held)
    if e.kind == "query.reading":
        assert len(world.journal) == journal  # a question is never journaled


# ---------------------------------------------------------------------------
# Package 37d: `take a fix`, an order of the master's where `take a bearing of` is
# ---------------------------------------------------------------------------


def test_take_a_fix_is_a_navigation_order_with_the_words_a_seaman_would_type():
    """The forms: `take a fix`; `take a fix by <mark> and <mark>`; the synonyms; all at
    the level and with the object of `take a bearing of`, so the same refusals apply."""
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    spec, bearing = vocab.verbs["take a fix"], vocab.verbs["take a bearing of"]
    assert (spec.object, spec.level) == (bearing.object, bearing.level)
    assert spec.object == "navigation"
    for said in (
        "take a fix",
        "take a fix by",
        "fix her position",
        "fix the position",
        "take cross bearings",
        "take cross bearings of",
        "cross bearings",
        "get a fix",
    ):
        assert vocab.phrase_to_verb[said] == "take a fix", said
    w = voyage("frigate", 50.08, -4.95, "10:00")
    for said in ("take a fix", "fix her position", "take cross bearings", "get a fix"):
        e = w.submit(said)
        assert e.kind == "reckoning.fix" and e.text.startswith("Fixed by cross bearings: "), said
    e = w.submit("Take a fix by Black Head and St Anthony's Head.")
    assert e.kind == "reckoning.fix" and e.data["by"] == ["Black Head", "St Anthony's Head"]
    # on a ship that keeps no reckoning it is refused as every navigation order is
    from freesail.api.session import make_world

    plane = make_world(7, str(SHIP_FILES["frigate"]), Scenario())
    refused = plane.submit("take a fix")
    assert refused.kind == "order.rejected" and "No reckoning is kept" in refused.text


def test_take_a_fix_is_completed_from_the_marks_in_sight():
    from freesail.orders.complete import FIX_OFFER_MARKS, suggestions

    w = voyage("frigate", 50.08, -4.95, "10:00")
    assert "take a fix " in suggestions(w.ship, "take a f")
    offered = suggestions(w.ship, "take a fix ", limit=40)
    marks = [s.feature.name for s in w.navigation._fix_marks()[:FIX_OFFER_MARKS]]
    assert offered[: len(marks)] == [f"take a fix by {name}" for name in marks]
    assert f"take a fix by {marks[0]} and {marks[1]}" in offered
    third = suggestions(w.ship, f"take a fix by {marks[0]} and {marks[1]} ", limit=40)
    assert f"take a fix by {marks[0]} and {marks[1]} and {marks[2]}" in third
    for line in offered[:8] + third[:4]:
        assert w.submit(line).kind in ("reckoning.fix", "order.rejected"), line
    # with fewer than two marks in sight there is nothing to offer but the order itself
    w.lookout.sightings = []
    assert suggestions(w.ship, "take a fix ") == []


def test_the_three_forms_of_allow_are_offered_and_each_is_taken_and_logged_as_whose_it_is():
    """Package 37e, item 8: after "allow" the completion offers the tide handed back to
    the master, no set, and the captain's own set; each is taken, and its line and the
    reading say whose allowance stands. A course shaped then gives the line and the
    course to make it good against that allowance."""
    from freesail.orders.complete import ALLOW_OFFERS, suggestions

    w = voyage("frigate", 49.70, -5.10, "10:00")
    assert suggestions(w.ship, "allow ") == list(ALLOW_OFFERS)
    assert "allow the tide by the book" in suggestions(w.ship, "allow the t")
    w.submit("set plain sail")
    w.run(1800)
    w.submit("heave the log")
    w.run(120)
    own = w.submit("allow two knots of set to the west")
    assert own.kind == "reckoning.set_allowance" and own.text == (
        "Allowing two knots of set to the west in the reckoning, by the captain's order, in "
        "place of the master's own tide."
    )
    assert w.readings["reckoning"]["tide"]["by"] == "captain"
    assert w.readings.words("reckoning").endswith(
        "; the tide allowed: by the captain's order, two knots to the westward"
    )
    shaped = w.submit("shape a course for 50 02 N 4 58 W")
    assert shaped.kind == "helm.set" and shaped.data["allowing"]["by"] == "captain"
    assert " of set to the westward by the captain's order, steer " in shaped.text
    assert " to make it good. Helm ordered: steer " in shaped.text
    line, steer = shaped.data["line_deg"], shaped.data["allowing"]["steer_deg"]
    assert 2.0 < (steer - line) % 360.0 < 40.0  # her head up-tide of the line, to the eastward
    none = w.submit("allow no set")
    assert none.text.startswith("No set allowed for in the reckoning, by the captain's order")
    assert w.readings.words("reckoning").endswith("the tide allowed: none, by the captain's order")
    back = w.submit("allow the tide by the book")
    assert back.kind == "reckoning.set_allowance" and back.text.startswith(
        "The tide in the reckoning handed back to the master, by the book: "
    )
    assert w.readings["reckoning"]["tide"]["by"] == "book"
    assert " by the directions for the open Channel and high water at " in w.readings.words(
        "reckoning"
    )
    for line in ALLOW_OFFERS:
        assert w.submit(line).kind == "reckoning.set_allowance", line
    # a course across a headland says so, and is ordered all the same
    across = w.submit("shape a course for Brest")
    assert across.kind == "helm.set" and "; the line crosses the land about " in across.text


# ---------------------------------------------------------------------------
# Package 37l: the words. A course with a half point, first (game 10: `steer south by west
# half west` was steered west, its last word); one reader for numbers; the phrasings of
# the review's G17, each taken or refused with what to say instead
# ---------------------------------------------------------------------------

_CARDINALS = {0: "north", 8: "east", 16: "south", 24: "west"}
_FRACTION_SAID = {
    1: ("quarter", "1/4", "¼"),
    2: ("half", "1/2", "½"),
    3: ("three quarters", "3/4", "¾"),
}


def _card(q: int) -> list[tuple[str, float]]:
    """Every way the card's quarter point `q` (0 to 127) is said: from the whole point at
    or before it toward the cardinal point ahead (clockwise), and from the whole point
    after it back toward the cardinal point behind, each in words, figures and the signs,
    and in the long names and the short; with its heading in degrees."""
    deg = q * 360.0 / 128
    k, f = divmod(q, 4)
    if f == 0:
        full = units.COMPASS_NAMES[k]
        return [(full, deg), (units.COMPASS_ABBREVIATIONS[k], deg)]
    out: list[tuple[str, float]] = []
    ahead = (k // 8 + 1) * 8 % 32
    behind_k = (k + 1) % 32
    behind = (k // 8) * 8
    for base, frac, toward in ((k, f, ahead), (behind_k, 4 - f, behind)):
        for said in _FRACTION_SAID[frac]:
            out.append((f"{units.COMPASS_NAMES[base]} {said} {_CARDINALS[toward]}", deg))
            out.append(
                (
                    f"{units.COMPASS_ABBREVIATIONS[base]} {said} "
                    f"{units.COMPASS_ABBREVIATIONS[toward]}",
                    deg,
                )
            )
    return out


CARD = [form for q in range(128) for form in _card(q)]


def test_the_whole_card_in_words_is_read_to_the_quarter_point():
    """Item 1 (the course with a half point): every one of the card's 128 quarter points,
    said from either neighbouring whole point toward a cardinal point, in words, in
    figures and in the signs, long names and short, is read whole and steered to it."""
    assert len(CARD) > 128 * 4
    ship, _ = make("frigate")
    for said, deg in CARD:
        o = parse(ship, f"steer {said}")
        got = units.rad_to_deg(o.modifiers["heading"]) % 360.0
        assert got == pytest.approx(deg % 360.0, abs=1e-9), (said, got, deg)
        assert units.parse_course(said) == pytest.approx(math.radians(deg % 360.0), abs=1e-12)


@pytest.mark.parametrize(
    "said,deg,shown",
    [
        ("south by west half west", 196.875, "S by W ½ W (197°)"),
        ("S by W 1/2 W", 196.875, "S by W ½ W (197°)"),
        ("S by W ½ W", 196.875, "S by W ½ W (197°)"),
        ("WNW 1/2 W", 286.875, "WNW ½ W (287°)"),
        ("west north west half west", 286.875, "WNW ½ W (287°)"),
        ("west-north-west half west", 286.875, "WNW ½ W (287°)"),
        ("NE by N 1/4 N", 30.9375, "NE by N ¼ N (31°)"),
        ("north east by north quarter north", 30.9375, "NE by N ¼ N (31°)"),
        ("NNE 3/4 E", 30.9375, "NNE ¾ E (31°)"),
        ("north half east", 5.625, "N ½ E (6°)"),
        ("N by W ½ N", 354.375, "N by W ½ N (354°)"),
        ("south by west half a point west", 196.875, "S by W ½ W (197°)"),
    ],
)
def test_a_course_with_a_half_point_is_steered_to_it_and_shown_as_the_card_has_it(
    said: str, deg: float, shown: str
):
    ship, _ = make("frigate")
    kind, text, data = orders.handle(ship, f"steer {said}")
    assert kind == "helm.order" and text == f"Helm ordered: steer {shown}."
    assert ship.dyn.helm_mode is HelmMode.HEADING
    assert units.rad_to_deg(ship.dyn.target_heading) == pytest.approx(deg)
    assert data["target_heading"] == pytest.approx(math.radians(deg))


@pytest.mark.parametrize(
    "said,words",
    [
        ("steer south by west half", ["toward which point", "'south by west half west'"]),
        ("steer north half south", ["is no course", "within eight points", "'north half east'"]),
        ("steer west two", ["gives a course", "and a number of points", "say one"]),
        ("steer south west, 245", ["Two courses were given", "say one"]),
        ("steer south west 245", ["Two courses were given"]),
        ("fill away and steer S by W half", ["toward which point"]),
        ("steer S by W 1/2 Q", ["toward which point"]),
    ],
)
def test_an_unreadable_course_is_refused_and_never_steered_to_its_last_word(
    said: str, words: list[str]
):
    ship, _ = make("frigate")
    before = (ship.dyn.helm_mode, ship.dyn.target_heading)
    with pytest.raises(OrderError) as info:
        orders.handle(ship, said)
    for w in words:
        assert w in str(info.value), (said, str(info.value))
    assert (ship.dyn.helm_mode, ship.dyn.target_heading) == before


def test_the_ground_tackle_and_the_set_take_a_course_with_a_half_point():
    """`get under way ... and steer <course>`, `lay out a kedge to <point>` and `allow ...
    set to <point>` read the same course; a fraction they cannot read is refused."""
    from freesail.orders.ground_tackle import _course as tackle_course
    from freesail.orders.navigation import _course as nav_course

    assert units.rad_to_deg(tackle_course("s by w half w")) == pytest.approx(196.875)
    assert units.rad_to_deg(nav_course("south west half west")) == pytest.approx(230.625)
    with pytest.raises(OrderError, match="toward which point"):
        tackle_course("s by w half")


@pytest.mark.parametrize(
    "said,value,used",
    [
        ("sixteen", 16, 1),
        ("thirteen", 13, 1),
        ("seventeen", 17, 1),
        ("nineteen", 19, 1),
        ("twenty five", 25, 2),
        ("forty", 40, 1),
        ("a hundred", 100, 2),
        ("a hundred and eighty five", 185, 5),
        ("one hundred eighty five", 185, 4),
        ("two hundred and five", 205, 4),
        ("three hundred and sixty", 360, 4),
        ("a thousand", 1000, 2),
        ("two thousand three hundred", 2300, 4),
        ("a", 1, 1),
        ("an", 1, 1),
        ("half", 0.5, 1),
        ("half a", 0.5, 2),
        ("a half", 0.5, 2),
        ("a quarter", 0.25, 2),
        ("quarter", 0.25, 1),
        ("a quarter of a", 0.25, 4),
        ("three quarters", 0.75, 2),
        ("two and a half", 2.5, 4),
        ("one and a quarter", 1.25, 4),
        ("16", 16, 1),
        ("16.5", 16.5, 1),
        ("a dozen", 12, 2),
    ],
)
def test_one_reader_reads_every_number_in_words_and_figures(said: str, value: float, used: int):
    """Item 2: every number to a hundred, the hundreds and the thousands, the halves and
    the quarters, by one reader."""
    from freesail.orders import numbers

    assert numbers.read(said.split()) == (pytest.approx(value), used)


def test_every_number_to_a_hundred_said_in_words_is_read():
    from freesail.orders import numbers

    units_ = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen"]
    teens += ["seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    for n in range(1, 100):
        if n < 10:
            said = units_[n]
        elif n < 20:
            said = teens[n - 10]
        else:
            said = f"{tens[n // 10]} {units_[n % 10]}".strip()
        assert numbers.read_all(said) == n, said
        assert numbers.read_all(f"a hundred and {said}") == 100 + n, said


@pytest.mark.parametrize(
    "text,fathoms",
    [
        ("veer five fathoms", 5.0),
        ("veer sixteen fathoms", 16.0),
        ("veer a hundred and eighty-five fathoms", 185.0),
        ("veer to ninety fathoms", 90.0),
        ("veer 45 fathoms", 45.0),
        ("heave in twenty five fathoms", 25.0),
        ("let go the best bower and veer to forty-five fathoms", 45.0),
    ],
)
def test_the_ground_tackles_fathoms_are_read_by_the_one_reader(text: str, fathoms: float):
    from freesail.orders.ground_tackle import _fathoms

    o = parse(make("frigate")[0], text)
    n, _ = _fathoms(o.object or "")
    assert n == pytest.approx(fathoms)


def test_a_word_before_fathoms_that_is_no_number_is_refused():
    from freesail.orders.ground_tackle import _fathoms

    with pytest.raises(OrderError, match="not a number of fathoms"):
        _fathoms("veer umpteen fathoms")


def test_a_quarter_fathom_and_the_provisions_days_and_the_knots_of_set():
    from freesail.orders.navigation import _knots
    from freesail.orders.port import _days

    o = parse(make("cutter")[0], "haul in the starboard jib sheet a quarter fathom")
    assert o.modifiers["fathoms"] == pytest.approx(0.25)
    o = parse(make("cutter")[0], "ease the main sheet three quarters of a fathom")
    assert o.modifiers["fathoms"] == pytest.approx(0.75)
    assert _days("for sixteen days") == 16
    assert _days("for a month") == 30
    assert _days("for six weeks") == 42
    assert _days("thirty") == 30
    assert _days("") is None
    with pytest.raises(OrderError, match="not a time to provision for"):
        _days("for a good while")
    assert _knots("one and a half") == 1.5
    assert _knots("half a") == 0.5
    assert _knots("a knot and a half") == 1.5
    assert _knots("no") == 0.0


def test_two_bargains_in_one_order_are_two():
    from freesail.orders.port import _bargains

    assert _bargains("20 tons of salt fish and 8 tons of pilchards") == [
        "20 tons of salt fish",
        "8 tons of pilchards",
    ]
    assert _bargains("twenty tons of fish and chips") == ["twenty tons of fish and chips"]
    assert _bargains("ten tons of tin and a ton of copper") == [
        "ten tons of tin",
        "a ton of copper",
    ]


@pytest.mark.parametrize(
    "which,text,expect",
    [
        # the helm
        ("frigate", "steady on", ok(kind="helm.order", text=["Helm ordered: steady on N"])),
        ("frigate", "close hauled", ok(kind="helm.order", text=["keep her full and by"])),
        ("frigate", "keep her close hauled", ok(kind="helm.order", text=["full and by"])),
        ("frigate", "bring her up", ok(kind="helm.order", text=["come up a point"])),
        ("frigate", "bring her up two points", ok(kind="helm.order", text=["two points"])),
        # the sheets of a group of sails
        (
            "cutter",
            "trim the headsail sheets",
            ok(kind="sail.trimmed", text=["The sheets of the fore staysail and the jib"]),
        ),
        # a headsail backed by its sheet, hauled to windward
        (
            "cutter",
            "back the fore staysail",
            ok(kind="line.hauled", text=["Backed the fore staysail"]),
        ),
        # a jib told to furl is taken in; lower is said of a jib; clew up is refused with
        # what to say
        ("cutter", "furl the jib", ok(evo="take_in_jibheaded")),
        ("cutter", "lower the jib", ok(evo="take_in_jibheaded")),
        ("cutter", "clew up the jib", no(["hauled down, not clewed up", "'haul down the jib'"])),
        # the water sail is a sail, not the stores
        ("schooner", "take in the water sail", ok(evo="take_in_studding")),
        ("schooner", "lower the water sail", ok(evo="take_in_studding")),
        ("schooner", "furl the water sail", ok(evo="take_in_studding")),
        ("schooner", "clew up the water sail", no(["not clewed up", "'take in the water sail'"])),
        ("frigate", "take in the water sail", no(["There is no such part as the water sail"])),
        # the words refused with what to say, or the milestone
        ("frigate", "hoist our colours", no(["milestone 7"])),
        ("frigate", "show your colours", no(["milestone 7"])),
        ("frigate", "man the pumps", no(["not worked in this game yet", "Sound the well"])),
        ("frigate", "as you were", no(["'belay that'"])),
        (
            "frigate",
            "put the helm over",
            no(["says not which way", "'helm a-lee'", "'hard a-weather'"]),
        ),
        ("frigate", "put the helm over to starboard", no(["says not which way"])),
        ("frigate", "lay out the stream anchor astern", no(["'lay out a kedge astern'"])),
    ],
    ids=lambda v: v if isinstance(v, str) else "",
)
def test_the_phrasings_of_g17_on_a_ship(which: str, text: str, expect: ok | no):
    ship, runner = make(which)
    if which == "cutter":
        for sid in ("jib", "fore.staysail"):
            ship.sails[sid].state = SailState.SET
    if which == "schooner":
        ship.sails["water_sail"].state = SailState.SET
    if isinstance(expect, no):
        with pytest.raises(OrderError) as info:
            orders.handle(ship, text)
        for m in expect.mentions:
            assert m in str(info.value), (text, str(info.value))
        return
    kind, line, data = orders.handle(ship, text)
    assert kind == expect.kind, (text, kind, line)
    for m in expect.text:
        assert m in line, (text, line)
    if expect.evo is not None:
        assert runner.started and all(e == expect.evo for e, _, _ in runner.started), runner.started


@pytest.mark.parametrize(
    "said,hint",
    [
        # `hail the pilot` is an order since package 37h, merged after this test was
        # written: its wrong hint ("did you mean 'haul'?") is gone with it
        ("man the boats", None),
        ("as you like it", None),
        ("mr pearce make sail", None),
        ("stear south", "'steer'"),
        ("lett go the anker", "'let go'"),
    ],
)
def test_a_hint_points_the_right_way_or_is_not_given(said: str, hint: str | None):
    """The hints that pointed the wrong way (`hail the pilot`, "did you mean 'haul'?"): a
    verb is hinted only when it is near in spelling."""
    from freesail.orders.errors import UnknownVerbError

    with pytest.raises(UnknownVerbError) as info:
        parse(make("frigate")[0], said)
    words = str(info.value)
    if hint is None:
        assert "did you mean" not in words, words
    else:
        assert hint in words, words


def test_marks_by_their_names_without_accents_or_apostrophes():
    from freesail.world.geo import name_words

    assert name_words("La Lavandière") == ["la", "lavandiere"]
    assert name_words("St Anthony's Head") == ["st", "anthonys", "head"]
    assert name_words("St Anthony’s Head") == name_words("st anthonys head")
    assert name_words("Béniguet") == ["beniguet"]
    w = voyage("frigate", 49.9, -5.5, "10:00")
    chart = w.chart
    feature = chart.find_feature("St Anthony's Head")
    assert feature is not None and chart.find_feature("st anthonys head") is feature
    accented = next(f for f in chart.features.values() if any(ord(c) > 127 for c in f.name))
    from unicodedata import combining, normalize

    folded = "".join(c for c in normalize("NFKD", accented.name) if not combining(c))
    assert chart.find_feature(folded) is accented, accented.name


def test_where_is_a_mark_says_it_in_sight_or_by_account():
    w = voyage("frigate", 49.9, -5.5, "10:00")
    seen = w.submit("where is the lizard")
    assert seen.kind == "query.reading"
    assert seen.text.startswith("The Lizard: in sight, bearing ")
    far = w.submit("where is ushant")
    assert far.kind == "query.reading"
    assert far.text.startswith("Ushant: not in sight; by account it bears ")
    assert far.text.endswith(" miles.")
    person = w.submit("where is mr harvey")
    assert person.kind == "query.reading" and "Mr Harvey" in person.text
    nobody = w.submit("where is atlantis")
    assert nobody.kind == "order.rejected"
    assert "the chart has no mark of that name" in nobody.text


def test_a_course_shaped_for_a_point_off_a_place_of_the_chart():
    """`shape a course for a mile west of ushant` (game 10): the point laid off from the
    chart's place by the distance and the point said, and the course shaped for it."""
    from freesail.world.geo import bearing_and_distance

    w = voyage("frigate", 49.9, -5.5, "10:00")
    e = w.submit("shape a course for two miles south of the lizard")
    assert e.kind == "helm.set", e.text
    assert e.text.startswith("Shaped a course for two miles south of the Lizard: ")
    lizard = w.chart.find_feature("the Lizard")
    from freesail.orders.navigation import _off_a_place

    target, said = _off_a_place(w, "two miles south of the lizard")
    bearing, metres = bearing_and_distance(lizard.position, target)
    assert bearing == pytest.approx(180.0, abs=0.01)
    assert metres == pytest.approx(2 * units.NAUTICAL_MILE, rel=1e-6)
    assert said == "two miles south of the Lizard"
    target, said = _off_a_place(w, "a mile west of ushant")
    assert said == "a mile west of Ushant"
    refused = w.submit("shape a course for a mile west of atlantis")
    assert refused.kind == "order.rejected" and "no place named 'atlantis'" in refused.text
    refused = w.submit("shape a course for a mile sideways of the lizard")
    assert refused.kind == "order.rejected" and "not a point of the compass" in refused.text


def test_pipe_down_and_call_a_watch_by_its_side():
    w = voyage("frigate", 49.9, -5.5, "10:00")
    deck = w.submit("pipe down the watch")
    assert deck.kind == "crew.order" and "Nobody is turned up" in deck.text
    on_deck = w.submit("call the starboard watch")
    assert on_deck.kind == "crew.order", on_deck.text
    below = "larboard" if "starboard watch has the deck" in on_deck.text else "starboard"
    called = w.submit(f"call the {below} watch")
    assert called.kind == "crew.order"
    assert called.text.startswith(f"The boatswain's mates call the {below} watch")
    assert "They stay up until piped down." in called.text
    again = w.submit("call the watch below")
    assert again.text == f"The {below} watch is coming up already."
    w.run(120)
    piped = w.submit(f"pipe down the {below} watch")
    assert piped.kind == "crew.piped_down", piped.text


def test_send_for_the_master_where_the_master_is_the_captain_says_so():
    w = voyage("schooner", 49.9, -5.5, "10:00")
    e = w.submit("send for the master")
    assert e.kind == "order.rejected"
    assert "In this vessel the master is the captain" in e.text
    assert "say 'send for the mate'" in e.text
    frigate = voyage("frigate", 49.9, -5.5, "10:00")
    assert frigate.submit("send for the master").kind == "person.sent_for"


def test_a_word_to_a_station_nobody_holds_is_kept_and_said():
    w = voyage("frigate", 49.9, -5.5, "10:00")
    e = w.submit("tell the watcher keep a sharp lookout for the Lizard light")
    assert e.kind == "agent.told", e.text
    assert e.text == (
        "The captain to the watcher: keep a sharp lookout for the Lizard light (nobody holds "
        "the station; the words are kept in its journal for whoever takes it)"
    )
    journal = w.agent_journals["watcher"]
    assert journal.kept_words() == [
        "The captain's word, kept for whoever takes the station: keep a sharp lookout for "
        "the Lizard light"
    ]
    assert w.submit("ask the watcher how she goes").kind == "order.rejected"


def test_belay_get_under_way_names_the_work_by_the_order():
    from freesail.orders import work

    vocab = orders.load_vocabulary()
    assert work._evolution_ids("get under way", vocab) == {"get_under_way"}
    assert work._evolution_ids("weigh", vocab) == {"weigh_anchor"}
